# 实际运行源码完整分段

完整文件按原路径列出，哈希指原文件字节。

## source/src/pr_next_joint/investigation/quantity_checks.py

SHA-256 `76494dba6b641ba95e676747c13fbececaef8582867bb370487c1fd1139a079f`

```python
"""Prove or leave open equality of recorded amount versions on one source path.

An equality result is a fact about accounting. It is not holder consent and
does not by itself establish either a vulnerability or a category exclusion.
This checker does not build transaction sequences or return input assignments.
"""
import hashlib

from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys
from pr_next_joint.verification.expressions import Unsupported
from pr_next_joint.verification.program_encoding import MechanismEncoder
from pr_next_joint.verification.sequence import qualify
from pr_next_joint.verification.solver import solve
from pr_next_joint.verification.source_worlds import encode_frame


def compare_gate(gate,expressions,frame,slot=0):
    signature=(gate['operator'],gate['operand_index'],key(qualify(gate['grant'],slot)),
               key(qualify(expressions[gate['quantity_expression']],slot)))
    for node in walk(frame['guards']):
        args=node.get('args',[])
        if len(args)!=2:continue
        i=gate['operand_index']
        if (node.get('op'),i,key(args[i]),key(args[1-i]))==signature:
            return True
    return False


def check_quantities(b,prop):
    matrix=[]
    cache=b.__dict__.setdefault('_accounting_equalities',{})
    dep=b.f.summaries.dependencies
    for use,identity in (prop.get('quantity_routes') or {}).items():
        rows=dep.amounts_for(use)
        if identity!=digest(rows):
            matrix.append({'operation':use,'result':'source_ir_mismatch'});continue
        for row in rows:
            for gate in row['allowance_gates']:
                holder=keys(gate['grant'])[gate['issuer_key']]
                for debit in row['deltas']:
                    if debit['sign']!='-' or debit['key_role']=='authorization_quantity' or key(debit['holder'])!=key(holder):
                        continue
                    a,c=debit['amount_expression'],gate['quantity_expression']
                    record={'operation':use,'target':b.f.operations[use]['target'],'path':row['path'],
                            'holder':holder,'ledger':debit['cell'],'issuer_spender_keys':keys(gate['grant']),
                            'debit_expression':a,'allowance_operand':c,'allowance_operator':gate['operator'],
                            'gate_operand_index':gate['operand_index'],'stage':'committed_source_path',
                            'semantics':'amount correspondence only; consent requires source-backed policy'}
                    token=digest([b.f.identity,record,prop['domain'],prop['initial_identity'],dep.identity])
                    if token in cache:
                        matrix.append(dict(cache[token],reused=True));continue
                    if b.remaining()<=0:
                        matrix.append(dict(record,result='not_executed',reason='shared_budget'))
                        return matrix
                    fr=b.source_frame(use,row['path'],0)
                    if not compare_gate(gate,dep.expressions,fr):
                        record.update(result='source_ir_mismatch',reason='allowance_key_operator_or_amount_version')
                    elif a==c:
                        record['result']='same_source_expression'
                    elif row['residuals']:
                        record.update(result='open',reason='relevant_path_has_unresolved_semantics')
                    elif b.remaining()<=0:
                        record.update(result='not_executed',reason='shared_budget')
                    else:
                        try:
                            e=MechanismEncoder(b.f.lookup(use))
                            frame_terms=encode_frame(e,fr)
                            da=e.expr(qualify(dep.expressions[a],0));ga=e.expr(qualify(dep.expressions[c],0))
                            solver=e.z.Solver()
                            solver.add(frame_terms,*e.constraints,*e.domain_constraints)
                            def check(s):
                                b.check()
                                return str(solve(s,initial_ms=max(1,min(b.f.options.solver_timeout_ms,int(b.remaining()*1000)))))
                            premise=check(solver)
                            record['premise']=premise
                            if premise=='sat':
                                solver.add(da!=ga)
                                answer=check(solver)
                                formula=solver.sexpr();ref=hashlib.sha256(formula.encode()).hexdigest()
                                b.formulas.setdefault(ref,{'sha256':ref,'text':formula,
                                    'scope_context':{'operation':use,'path':row['path'],'scope':'amount equality in single modeled frame'}})
                                record.update(answer=answer,formula_ref=ref,result={
                                    'unsat':'equal_on_modeled_path','sat':'equality_not_entailed'}.get(answer,'open'))
                            else:
                                record.update(result='open',reason='premise_'+premise)
                        except (Unsupported,TimeoutError) as error:
                            record.update(result='open',reason=str(error))
                    if record['result'] in ('same_source_expression','equal_on_modeled_path','equality_not_entailed'):
                        cache[token]=record
                    matrix.append(record)
    return matrix

```

## source/src/pr_next_joint/investigation/relations.py

SHA-256 `983c6600cac7be81deca4d0a36f12db2f78317c3c656b4c83e41026b4c402f30`

```python
"""Source-bound semantic relations shared by property formation and feedback."""
import copy
import re
from pr_next_joint.frontend.path_ir import key, op, lit, walk
from pr_next_joint.frontend.storage import keys, selectors, value_type
from .policy_binding import effect_duty, source_requirement, compile_requirement, compare_requirement, positive_role_reference


def statement(text, choice=None):
    """Preserve the asserted relation and its negation, not a risk-word score."""
    text = str(text or "").strip()
    label = str(choice or "").split(":", 1)[0].strip()
    negative = bool(re.search(
        r"\b(?:no unauthorized|not unauthorized|no wrongful|neither unauthorized|"
        r"not (?:an? )?(?:access.control|authorization) (?:bug|issue|violation)|"
        r"does not (?:permit|allow|grant|show|demonstrate).{0,35}(?:unauthorized|unqualified|takeover)|"
        r"not (?:an? )?unauthorized|cannot .{0,35}without (?:the )?authorization|"
        r"no .{0,20}takeover path)\b|不存在越权|并非越权", text, re.I))
    unknown = label == "unknown" or bool(re.search(r"\b(?:unclear|cannot determine|unknown whether)\b", text, re.I))
    normal = label == "normal_authorization" or negative
    return {
        "text": text, "meaning": "unknown" if unknown else "normal_authorization" if normal else "required_authorization",
        "polarity": "unresolved" if unknown else "denied_violation" if negative else "asserted",
        "relation_source": "source_anchored_model_explanation",
        "default_interpretation_only": not (label or normal or unknown),
        "guard_is_execution_fact_not_policy": True,
    }


def policy(item):
    text = item.get("policy_basis") or item.get("claim") or ""
    if not isinstance(text, str): return None
    if not text.strip() or item.get("_host_source_question"):
        return None
    scoped = bool(item.get('_opinion_message') and item.get('_scope_effects'))
    if scoped and item.get('policy_basis') and not effect_duty(text) and effect_duty(item.get('claim','')):
        text = item['claim']
    row = statement(text)
    if (item.get('assessment')=='normal' and row['meaning']!='unknown'
            and re.search(r"\b(?:own|self|msg\.sender.s)\b",text,re.I)
            and re.search(r"\b(?:checks?|subject to|self.service)\b",text,re.I)
            and not re.search(r'\b(?:bypass(?:es)?|unauthorized|without consent)\b',text,re.I)):
        row['meaning']='normal_authorization'
    row["source_anchors"] = copy.deepcopy(item.get("anchors", []))
    if scoped:
        row['localized_effect_opinion'] = True
    row["level"] = "H"
    return row


def _exact_name(text, name):
    return bool(name and re.search(r"(?<![\w$])" + re.escape(name) + r"(?![\w$])", text))


def bound_effect(inv, explanation, compiled):
    """Scope the query to this applied write. A sibling effect cannot witness it."""
    eid = explanation.get('binding_effect')
    if not eid:return compiled
    effect=inv.semantics.rules.effects[eid]
    compiled['binding_effect']=eid
    if 'write' in effect:
        compiled['effect_write']={'path':effect['path'],'version':effect['version'],'cell':effect['cell']}
    return compiled


def opinion_principals(inv, item, effect, duty):
    """Bind only the policy's actor to this target and this exact effect operand."""
    from .summary import holder
    lookup = inv.f.lookup(effect['oid'])
    bases = lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']])
    scoped = item.get('_opinion_subject')
    explicit = inv.semantics.rules.objects[scoped]['decl'] if scoped else None
    principals = []
    for phrase in duty['actors']:
        possessor = bool(re.search(r"\b(?:holder|depositor|owner of (?:the |their |this )?(?:account|balance|assets?|entitlement))\b|持有人|存款人", phrase, re.I))
        if possessor:
            operand = holder(effect['cell'], lookup) if 'cell' in effect else None
            relation = 'holder'
        else:
            slots = [node for node in lookup.decls.values()
                     if node.get('stateVariable') and node.get('scope') in bases and node.get('name')
                     and _exact_name(phrase.casefold(), node['name'].strip('_').casefold())]
            qualified = [n for n in slots if _exact_name(phrase.casefold(),
                         (lookup.nodes.get(n.get('scope'),{}).get('name','')+'.'+n['name']).casefold())]
            slots = qualified or slots
            if explicit is not None and any(n['id'] == explicit for n in slots):
                slots = [n for n in slots if n['id'] == explicit]
            operand = None
            relation = 'abstract' if not slots else 'ambiguous'
            if len(slots) == 1:
                cell = {'kind':'storage','root':slots[0]['id'],'segments':[]}
                typ = value_type(cell, lookup)
                if typ in ('address','address payable') or typ.startswith('mapping('):
                    operand = cell
                    relation = 'office'
        if explicit is not None and (operand or {}).get('id',(operand or {}).get('root')) != explicit:
            # A genuine abstract duty can use the explicitly shown source subject.
            # Never use that locator to replace a mismatching holder or named slot.
            if relation == 'abstract' and not possessor and explicit in lookup.nodes:
                cell = {'kind':'storage','root':explicit,'segments':[]}
                n = lookup.nodes[explicit]
                if n.get('stateVariable') and n.get('scope') in bases and value_type(cell,lookup) in ('address','address payable'):
                    operand, relation = cell, 'office'
                else:
                    relation = 'conflict'
            else:
                relation = 'conflict'
        principals.append((relation,operand))
    return principals


def authorization(inv, q, explanation, *, unresolved=None):
    if not isinstance(explanation, dict) or explanation.get("meaning") == "unknown":
        return None
    f = inv.f
    oid = inv.root(q)
    lookup = f.lookup(oid)
    mode=explanation.get('explicit_policy_kind')
    text = explanation.get("text", explanation.get("basis", ""))
    # Binding an intended policy is distinct from proving a committing path.
    # A known write before an unresolved call still identifies the issuer or
    # stage. The actual query separately retains that call's exit/residual.
    rows = [(pid,p) for pid,p in f.operation_paths(oid) if p['flow'] in ('normal','returned')]
    declaration = lookup.nodes.get(f.operations[oid]['source'].get('ast_id'), {})
    focused = explanation.get('source') == 'focused_model_answer'
    scoped = explanation.get('localized_effect_opinion', False) or (
        focused and q['current'].get('_opinion_message') and q['current'].get('_scope_effects'))
    duty = effect_duty((explanation.get('basis') if focused else None) or text) if scoped else None
    scoped_subject = None
    bound = {}
    if scoped and duty:
        rules = inv.semantics.rules
        bound = {e: opinion_principals(inv, q['current'], rules.effects[e], duty)
                 for e in q['current'].get('_scope_effects', ()) if rules.effects[e]['oid'] == oid}
        if bound and len({key(v) for v in bound.values()}) == 1:
            actors = next(iter(bound.values()))
            if len(actors) == 1 and actors[0][0] in ('office','holder') and actors[0][1] is not None:
                scoped_subject = actors[0]
    required = source_requirement(inv,q,explanation,rows) if not mode or mode=='current_authority_required' else None
    if scoped and required and duty and required['kind'] in ('source_role_payment_policy','source_grant_issuer','source_guarded_eligibility'):
        # A condition described in the behaviour clause is not a substitute
        # for consent by the specified principal.
        if not scoped_subject or key(required.get('subject', required.get('grant',{}).get('issuer'))) != key(scoped_subject[1]):
            required = None
    if required and required['kind']=='unresolved_role_payment_policy':
        if unresolved is not None:unresolved.add('role_payment_relation')
        return None
    if mode and required and required['kind']!='source_role_payment_policy':
        required=None
    if required:
        compiled = compile_requirement(required,explanation,lookup)
        match = compare_requirement(required,compiled,oid,declaration.get('id'),f.operations[oid]['target'])
        compiled['source_ir_check'] = match
        if not match['matches']:
            q['authorization_binding_diagnostic'] = {'reason':'source_ir_disagreement','comparison':match}
            return None
        return bound_effect(inv,explanation,compiled)
    if mode in ('current_authority_required','holder_authorization_applies','initialization_stage'):
        sub=explanation.get('qualified_cell')
        if not sub:return None
        predicate=op('!',sub) if mode=='initialization_stage' else op('==',{'kind':'actual_sender'},sub)
        return bound_effect(inv,explanation,{'predicate':predicate,'subject':sub,'kind':'scope_bound_'+mode,
                'property_family':'use','acquisition_uses':[],'source_bound_alternatives':[],
                'normal_alternatives':[],'binding':{'declaration':sub.get('root',sub.get('id')),'frame':'before_source_effect','source':f.operations[oid]['source']}})
    anchored = [o for o in q['binding']['operations'] if f.operations[o]['target'] == f.operations[oid]['target']]
    related = [p for o in anchored for _, p in f.operation_paths(o, True)]
    bases = set(lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']]))
    # A one-time initialization policy refers to its actual stage flag, not
    # to the new administrator supplied by this very call.
    if re.search(r'one.time|only.once|already initialized|after initialization',text,re.I):
        flags={w['path']['root']:w['path'] for _,p in rows for w in p['writes'] if
            not keys(w['path']) and value_type(w['path'],lookup)=='bool' and w['value']==lit(True) and
            _exact_name(text,lookup.nodes[w['path']['root']].get('name'))}
        if len(flags)==1:
            flag=next(iter(flags.values()))
            return {'predicate':op('!',flag),'subject':flag,'kind':'source_once_only_initialization',
                'property_family':'use','normal_alternatives':[],'source_bound_alternatives':[],
                'business_basis':explanation,'acquisition_uses':[],
                'binding':{'original_relation':text,'declaration':flag['root'],'frame':'before_initialization',
                           'source':lookup.anchor(lookup.nodes[flag['root']])}}
    # Enrollment of zero is meaningful only with the supplied downstream
    # recovery/membership relation. It is not a generic "zero address bug".
    if re.search(r'(?:malformed|invalid|bad|failed).{0,25}signature|signature.{0,35}(?:zero|address\(0\))',text,re.I):
        for _,p in rows:
            for w in p['writes']:
                ks=keys(w['path'])
                if len(ks)!=1 or ks[0].get('kind')!='parameter' or value_type(w['path'],lookup)!='bool' or w['value']!=lit(True):continue
                if not _exact_name(text,lookup.nodes[w['path']['root']].get('name')):continue
                uses=[]
                for use,entry in f.operations.items():
                    if entry['target']!=f.operations[oid]['target']:continue
                    for pid,up in f.operation_paths(use,True):
                        if any(c['root']==w['path']['root'] and any(t.get('kind')=='credential_recovery' or
                            t.get('kind')=='conditional' and t.get('when_true')==lit(0) for t in walk(keys(c)))
                            for c in selectors(up['guards'])):
                            uses.append({'operation':use,'path':pid,'authority':w['path']})
                if uses:
                    return {'predicate':op('!=',ks[0],lit(0)),'subject':ks[0],'kind':'valid_nonzero_signer_enrollment',
                        'property_family':'acquire','normal_alternatives':[],'source_bound_alternatives':[],
                        'business_basis':explanation,'acquisition_uses':uses,
                        'binding':{'original_relation':text,'declaration':w['path']['root'],'frame':'enrollment_then_signature_use',
                                   'source':w['source'],'zero_recovery_is_not_a_forged_valid_signature':True}}
    if explanation.get('meaning') == 'normal_authorization' and re.search(
            r'\bpublic payable\b|\bcaller\b.{0,35}\b(?:supplies|pays)\b.{0,25}(?:msg\.value|payment)',text,re.I):
        from .summary import debited_positions, local_delta, holder
        has_payment = any(v.get('kind') == 'transaction_value' for _,p in rows for v in walk([p['guards'],p['writes']]))
        own_credit = any(local_delta(w)[0] == '+' and key(holder(w['path'],lookup)) == key({'kind':'actual_sender'})
                         for _,p in rows for w in p['writes'])
        third_party_debit = any(x['holder'].get('kind') not in ('actual_sender','contract_address')
                                for x in debited_positions(f,oid))
        changes_authority = any(not keys(w['path']) and value_type(w['path'],lookup) in ('address','address payable')
                                for _,p in rows for w in p['writes'])
        if has_payment and own_credit and not third_party_debit and not changes_authority:
            payer = {'kind':'actual_sender'}
            return {'predicate':op('==',payer,payer), 'subject':payer, 'kind':'source_payer_self_acquisition',
                    'property_family':'use','normal_alternatives':[], 'source_bound_alternatives':[],
                    'business_basis':explanation,'acquisition_uses':[],
                    'binding':{'original_relation':text,'frame':'same transaction payer and recipient',
                               'payment':'actual msg.value','source':lookup.anchor(declaration)}}
    if scoped and (not scoped_subject or duty['qualified'] or len(bound) != 1):
        # Specialised policies above can stand independently. A source inventory,
        # an abstract duty or a compound condition cannot sign a guessed predicate.
        return None
    role_text = duty['actors'][0] if scoped else text
    cells = {key(c): c for p in related for c in selectors([p["guards"], p["writes"]])
             if not keys(c) and value_type(c, lookup) in ("address", "address payable")}
    # A missing authorization check may leave its intended authority entirely
    # absent from executable guards. Bind an explicitly named source declaration
    # in this applied storage layout as well; never invent an owner from a name
    # or pick a same-named declaration in another target.
    bases = set(lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']]))
    for declaration in lookup.decls.values():
        if not declaration.get('stateVariable') or declaration.get('scope') not in bases:
            continue
        cell = {'kind': 'storage', 'root': declaration['id'], 'segments': []}
        if value_type(cell, lookup) not in ('address', 'address payable'):
            continue
        owner_name = lookup.nodes.get(declaration.get('scope'), {}).get('name', '')
        if (_exact_name(role_text, declaration.get('name')) or
                _exact_name(role_text, owner_name + '.' + declaration.get('name', ''))):
            cells[key(cell)] = cell
    written = {w["path"]["root"] for _, p in rows for w in p["writes"]}
    downstream = []
    for use, entry in f.operations.items():
        if entry["target"] != f.operations[oid]["target"]:
            continue
        for pid, path in f.operation_paths(use, True):
            for guard in path['guards']:
                if any(v.get('kind') == 'actual_sender' for v in walk(guard)):
                    for c in selectors(guard):
                        if not keys(c) and value_type(c,lookup) in ('address','address payable'):
                            cells[key(c)] = c
            for c in selectors(path["guards"]):
                if c["root"] in written and not keys(c) and value_type(c, lookup) in ("address", "address payable"):
                    cells[key(c)] = c
                    downstream.append({"operation": use, "path": pid, "authority": c})
                elif c['root'] in written and keys(c):
                    from .key_roles import relation as source_key_role
                    role = source_key_role(c,lookup)
                    if role and role.get('kind') == 'authorization_quantity':
                        downstream.append({'operation':use,'path':pid,'authority':c})
    qualified, named = [], []
    for c in cells.values():
        n = lookup.nodes.get(c["root"], {})
        owner = lookup.nodes.get(n.get("scope"), {}).get("name")
        # A business explanation may qualify an inherited field by the
        # applied contract. Resolve that spelling through the actual C3 bases;
        # it still denotes the original declaration, not a fresh storage slot.
        qualifiers={lookup.nodes[b].get('name') for b in bases if n.get('scope') in
                    lookup.nodes[b].get('linearizedBaseContracts',[b])}
        if any(o and positive_role_reference(role_text,o+'.'+n.get('name','')) for o in qualifiers):
            qualified.append(c)
        elif positive_role_reference(role_text, n.get("name")):
            named.append(c)
    explicit = qualified or named
    modifier_subjects = []
    body = lookup.nodes.get(f.operations[oid]['source'].get('ast_id'), {})
    for call in body.get('modifiers', []):
        modifier = lookup.nodes.get(call.get('modifierName', {}).get('referencedDeclaration'), {})
        if not _exact_name(role_text, modifier.get('name')):
            continue
        roots = {n.get('referencedDeclaration') for n in walk(modifier) if isinstance(n,dict)}
        for _, path in rows:
            for guard in path['guards']:
                if not any(v.get('kind') == 'actual_sender' for v in walk(guard)):
                    continue
                modifier_subjects += [c for c in selectors(guard) if c['root'] in roots and not keys(c) and
                                     value_type(c,lookup) in ('address','address payable')]
    guard_subjects = re.findall(r"\b(?:checks|reads|requires)\s+([A-Za-z_$][\w$]*\.[A-Za-z_$][\w$]*)", role_text)
    exact_guard = [c for c in qualified if any(
        lookup.nodes.get(lookup.nodes[c['root']].get('scope'),{}).get('name','') + '.' + lookup.nodes[c['root']].get('name','') == n
        for n in guard_subjects)]
    subjects = re.findall(r"\b(?:only|required(?: by| from)?|authorized by|permission (?:of|from))\s+(?:(?:an?|the|authorized|existing)\s+)*'?([A-Za-z_$][\w.$]*)", role_text, re.I)
    described = [c for c in explicit if any(
        lookup.nodes[c["root"]].get("name") == s.split(".")[-1] for s in subjects)]
    candidates = list({key(c): c for c in modifier_subjects or exact_guard or described or explicit}.values())
    if len(candidates)>1 and not (modifier_subjects or exact_guard or described):
        # An explanation can mention a role and an unrelated bookkeeping
        # address with similar spelling. Resolve that ambiguity through the
        # actual caller guard, never through name case or the new written
        # value. This binds a proposed policy; it does not prove the policy or
        # authorize its current caller.
        used={};candidate_keys={key(c) for c in candidates}
        for use,entry in f.operations.items():
            if entry['target']!=f.operations[oid]['target']:continue
            for pid,path in f.operation_paths(use,True):
                for term in walk(path['guards']):
                    if term.get('op') not in ('==','!=') or len(term.get('args',[]))!=2:continue
                    a,b=term['args']
                    for caller,role in ((a,b),(b,a)):
                        if caller.get('kind')=='actual_sender' and key(role) in candidate_keys:
                            used.setdefault(key(role),[]).append({'operation':use,'path':pid,'guard':term})
        narrowed=[c for c in candidates if key(c) in used]
        if len(narrowed)==1:
            q['authorization_relation_disambiguation']={'candidates':copy.deepcopy(candidates),
                'selected':copy.deepcopy(narrowed[0]),'source_guard_uses':used[key(narrowed[0])],
                'basis':'the proposed source fields have one actual caller-qualification use',
                'binding_frame':'before_effect','policy_truth_not_inferred_from_guard':True}
            candidates=narrowed
    if not scoped and subjects and not described and not modifier_subjects and not exact_guard and not qualified and any(
            s.lower() in ('owner','handler','admin','administrator','controller') for s in subjects):
        q['authorization_binding_diagnostic']={'reason':'described_authority_has_no_matching_source_declaration',
            'described_subjects':subjects,'mentioned_state_is_not_automatically_the_authority':True}
        return None
    kind = "authority_before_effect"
    if scoped_subject is not None:
        relation, subject = scoped_subject
        if relation == 'holder':
            kind = 'entitlement_holder'
        elif value_type(subject,lookup) not in ('address','address payable'):
            return None
    elif len(candidates) == 1:
        subject = candidates[0]
    elif not candidates and re.search(r"\b(?:holder|depositor|owner of (?:the )?(?:balance|asset)|spender|allowance)\b|持有人|存款人", text, re.I):
        from .summary import debited_positions
        hs = {key(x["holder"]): x["holder"] for x in debited_positions(f, oid)}
        if not hs:
            from .key_roles import relation as source_key_role
            for _,p in rows:
                for w in p['writes']:
                    relation = source_key_role(w['path'],lookup)
                    if relation and relation.get('kind')=='authorization_quantity':
                        h=keys(w['path'])[relation['holder_key']];hs[key(h)]=h
            if hs:kind='source_grant_issuer'
        if len(hs) != 1:
            return None
        subject = next(iter(hs.values()))
        if kind != 'source_grant_issuer':kind = "entitlement_holder"
    else:
        q["authorization_binding_diagnostic"] = {
            "reason": "authorization_subject_not_uniquely_source_bound", "candidates": candidates, "text": text}
        return None
    caller = {"kind": "actual_sender"}
    allow = [op("==", caller, subject)]
    from .authorization_normal import numeric_delegations, payment_qualification
    alternatives = numeric_delegations(inv, oid, subject, explanation) + payment_qualification(inv, q, subject)
    if scoped and kind == 'entitlement_holder':
        from .source_opinion import covered_delegation
        per_effect = [f.summaries.paths[r['path']] for r in (inv.semantics.rules.effects[e] for e in bound) if 'path' in r]
        if not per_effect or not covered_delegation(inv, oid, per_effect):
            alternatives = []
    if kind == 'entitlement_holder' and subject.get('kind') != 'actual_sender' and re.search(r'\b(?:allowance|quota|grant)\b',text,re.I):
        from .key_roles import relation as source_key_role
        gates = [c for _,p in rows for c in selectors(p['guards']) if
                 (source_key_role(c,lookup)or{}).get('kind')=='authorization_quantity']
        if gates and not alternatives:
            q['authorization_binding_diagnostic']={'reason':'holder_grant_provenance_not_established',
                'gates':gates,'holder':subject,'source_text':text,
                'cannot_default_to_holder_only_and_report_normal_spending_as_a_violation':True}
            return None
    allow.extend(x["predicate"] for x in alternatives)
    def requires_owner(guard):
        if guard.get('op') in ('and','&&'):
            return any(requires_owner(g) for g in guard['args'])
        return (guard.get('op') == '==' and
                {key(x) for x in guard.get('args',[])} == {key(caller), key(subject)})
    office_alternative_paths = [] if scoped and kind == 'entitlement_holder' else rows
    for _, path in office_alternative_paths:
        for term in walk(path['guards']):
            if term.get('op') != '==' or not any(x.get('kind') == 'actual_sender' for x in term.get('args',[])):
                continue
            for cell in selectors(term):
                if keys(cell) or key(cell) == key(subject) or value_type(cell,lookup) not in ('address','address payable'):
                    continue
                writers = [w for w in f.writes.values() if w['raw']['path']['root'] == cell['root'] and
                           f.operations[w['operation']]['target'] == f.operations[oid]['target'] and
                           w['raw']['value'].get('value') not in (0,False)]
                if writers and all(f.paths[w['path']]['raw']['flow'] in ('normal','returned') and
                                   not f.paths[w['path']]['raw'].get('issues') and
                                   any(requires_owner(g) for g in f.paths[w['path']]['raw']['guards']) for w in writers):
                    allow.append(op('==',caller,cell))
                    alternatives.append({'predicate': op('==',caller,cell),
                                         'kind':'source_owner_protected_nomination','source_paths':[w['path']for w in writers]})
    for _, path in office_alternative_paths:
        for term in selectors(path["guards"]):
            ks = keys(term)
            if value_type(term, lookup) != "bool" or len(ks) != 2:
                continue
            writers = [w for w in f.writes.values() if w["raw"]["path"]["root"] == term["root"] and
                       f.operations[w["operation"]]["target"] == f.operations[oid]["target"]]
            if (writers and all(keys(w["raw"]["path"]) and keys(w["raw"]["path"])[0].get("kind") == "actual_sender" for w in writers)
                    and key(ks[0]) == key(subject) and ks[1].get("kind") == "actual_sender"):
                allow.append(term)
    acquisition_intent = bool(re.search(r"\b(?:grant|gain|acquir\w*|becom\w*|takeover|install|replac\w*).{0,45}(?:owner|authority|role|withdraw right)", text, re.I))
    acquisition = [r for r in downstream if r["operation"] != oid and (
        r["authority"]["root"] == subject.get("root") or acquisition_intent or
        kind == 'source_grant_issuer' and r['authority']['root'] in written)]
    result = {"predicate": op("or", *list({key(x): x for x in allow}.values())),
            "subject": subject, "kind": kind, "normal_alternatives": allow[1:],
            "source_bound_alternatives": alternatives, "business_basis": explanation,
            "acquisition_uses": acquisition, "property_family": "acquire" if acquisition or acquisition_intent else "use",
            "binding": {"original_relation": text, "declaration": subject.get("root"), "frame": "before_effect",
                        "source": lookup.anchor(lookup.nodes[subject["root"]]) if subject.get("root") in lookup.nodes else None}}

    if scoped and len(bound) == 1:
        return bound_effect(inv, {'binding_effect':next(iter(bound))}, result)
    return result


def beneficiary_condition(encoder, frame, position, holder, *, controller_frame=None):
    """Conditional ability with all original source address restrictions."""
    requester=encoder.expr(frame["caller"])
    caller=encoder.expr((controller_frame or frame)["caller"])
    if holder.eq(caller):
        return holder == caller, {"kind": "self", "conditional": False}
    selectable = any(k.get("kind") == "parameter" and k.get("type") in ("address", "address payable") for k in keys(position))
    if selectable and getattr(encoder.lookup, "analysis_scope", None) == "FCR":
        from pr_next_joint.verification.sequence import qualify
        selected = [qualify(k,frame['slot']) for k in keys(position) if k.get('kind') == 'parameter']
        def conjuncts(g):
            return [x for a in g['args'] for x in conjuncts(a)] if g.get('op') in ('and','&&') else [g]
        fixed = [g for guard in frame['guards'] for g in conjuncts(guard) if g.get('op') == '==' and
                 any(key(x)==key(p) for x in g.get('args',[]) for p in selected) and
                 any(x.get('kind') in ('storage','literal','contract_address') for x in g.get('args',[]))]
        if fixed:
            return holder == caller, {'kind':'source_fixed_beneficiary_requires_established_control',
                                       'restrictions':fixed,'arbitrary_recipient_control_not_assumed':True}
        # Only the actual caller of the crediting entry chooses its arguments.
        # A separate ordinary buyer does not choose on behalf of the setter.
        controlled=encoder.z.Or(holder==caller,encoder.z.And(requester==caller,holder!=0))
        return controlled, {"kind": "selectable_self_controlled_address",
                             "conditional": True, "source_restrictions_in_frame": True,
                             "not_arbitrary_observed_recipient_control": True}
    return holder == caller, {"kind": "self_only_without_third_party_control_source",
                              "other_beneficiary_control_unestablished": True}


def source_violation(inv, q, prop):
    """A small source theorem, not a second business detector or SMT fallback.

    An unguarded scalar-role assignment can give the requester an authority
    whose actual source use has exactly that role guard and a freely selectable
    address update. The same compiled policy is needed; no policy is invented
    from a Solidity field name. All other shapes go to the ordinary backend.
    """
    expected = ((prop or {}).get('expected_authorization') or {}).get('compiled_authorization') or {}
    subject = expected.get('subject') or {}
    if (prop.get('task') != 'AC' or expected.get('property_family') != 'acquire' or
            expected.get('competing_interpretations') or expected.get('normal_alternatives') or
            subject.get('kind') != 'storage' or keys(subject)):
        return None
    caller = {'kind':'actual_sender'}
    if key(expected.get('predicate')) != key(op('or',op('==',caller,subject))):
        return None
    root = inv.root(q); f = inv.f
    if value_type(subject,f.lookup(root)) not in ('address','address payable'):
        return None
    for pid,path in f.operation_paths(root,True):
        if any(g != lit(True) for g in path['guards']) or path.get('evaluated_terms') or path.get('sensitive_effects'):
            continue
        granting = [w for w in path['writes'] if key(w['path']) == key(subject) and
                    (w['value'].get('kind') == 'actual_sender' or
                     w['value'].get('kind') == 'parameter' and w['value'].get('type') in ('address','address payable'))]
        if not granting:
            continue
        # Side expressions cannot hide a revert/constraint from this proof.
        if any(w['value'].get('kind') not in ('parameter','actual_sender','literal') for w in path['writes']):
            continue
        for use in expected.get('acquisition_uses',[]):
            p = f.paths[use['path']]['raw']
            if p.get('issues') or p.get('evaluation_gaps') or p.get('evaluated_terms') or p.get('sensitive_effects'):
                continue
            def role_guard(g):
                if g == lit(True):return True
                if g.get('op') in ('and','&&'):return all(role_guard(x) for x in g['args'])
                return g.get('op') == '==' and {key(x) for x in g['args']} == {key(caller),key(subject)}
            if not p['guards'] or not all(role_guard(g) for g in p['guards']):
                continue
            updates = [w for w in p['writes'] if not keys(w['path']) and
                       value_type(w['path'],f.lookup(use['operation'])) in ('address','address payable') and
                       w['value'].get('kind') == 'parameter' and w['value'].get('type') in ('address','address payable')]
            if not updates:
                continue
            return {'kind':'source_property_certificate','operation':root,'property_identity':prop['id'],
                    'property_validated':True,'level':'P','supports':'authorization_violation',
                    'source_paths':[pid,use['path']], 'authority':subject, 'grant':granting,
                    'actual_authority_use':use,'productive_update':updates,
                    'source_constraints':{'old_authority_and_requester':'different nonzero address values exist',
                        'grant_argument':'the requester when present',
                        'use_actor':'same requester after the real grant',
                        'use_update':'a free address argument distinct from its previous stored value'},
                    'proof':'straight-line typed address assignment; exact subsequent role equality; actual free address update',
                    'not_a_full_SMT_or_EVM_execution':True,'queries':[]}
    return None

```

## source/src/pr_next_joint/investigation/report.py

SHA-256 `91460185d78cefe201ee1984763458089080dd3d3abf1648445e3192eeb9da19`

```python
"""Source-backed risk prediction, scoped hard counterevidence and dependency output."""
import copy,re
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import walk,key
from pr_next_joint.frontend.storage import selectors,keys,value_type,selector_relation
from .contracts import VERSION,CATEGORIES
from .protocol import category_scope
from .request_scope import coverage_facts, observation_applies, compare_relevant, linked_controls



def evaluate(inv,q):
    from .property_model import compose
    from .source_opinion import reading_version
    inv.semantics.scope(q['current'])
    prop=q.get('property') or {}
    stamp=(q['version'],prop.get('id'),tuple(q['evidence']),bool(q.get('task_conflict')),
           q.get('retired_property_parent'),tuple(sorted(q.get('office_effects',{}).items())),
           tuple(q.get('effect_scope',())),len(q.get('observations',())),reading_version(inv,q['binding']['operations'],prop.get('category')))
    cached=q.get('_composed_snapshot')
    if not cached or cached[0]!=stamp:
        cached=(stamp,compose(inv,q,None));q['_composed_snapshot']=cached
    return cached[1]

def reading_scope(inv,blocked,assessments=None):
    from .coverage import obligation_scope
    assessments=assessments or {qid:evaluate(inv,q) for qid,q in inv.issues.items()}
    return obligation_scope(inv,assessments,blocked)



def build(inv):
    findings={};records=[];suppressed=[];decisive_records=[];blocked_categories=set();assessments={}
    for qid,q in sorted(inv.issues.items()):
        assessment=evaluate(inv,q);assessments[qid]=assessment;item=q['current'];records.append({'id':qid,'version':q['version'],
            'current':copy.deepcopy(item),'history':copy.deepcopy(q['history']),'binding':q['binding'],
            'distinguishing_plan':copy.deepcopy(q.get('plan')),'claim_source_scope':copy.deepcopy(q['claim_source_scope']),
            'task_conflict':q.get('task_conflict',False),'semantic_task_review':copy.deepcopy(q.get('task_review')),
            'compiled_property':copy.deepcopy(q.get('property')),'semantic_answers':copy.deepcopy(q.get('semantic_answers',[])),
            'assessment_result':assessment,'evidence_refs':q['evidence'],'revision_evidence':q['revision_evidence'],
            'scoped_observations':copy.deepcopy(q.get('observations',[])),
            'source_observation_reuse':copy.deepcopy(q.get('source_decisions',[]))})
        decision=assessment['scope']['decision']
        if decision['status'] in ('risk','normal','excluded') and not q.get('task_conflict'):
            decisive_records.append(qid)
        mapping=assessment['scope'].get('comparison_alignment',{})
        if decision['status']!='risk':
            if item['assessment']=='risk':suppressed.append({'issue':qid,'reasons':assessment['reasons']})
            continue
        oid=assessment['root'];o=inv.f.operations[oid]
        location=copy.deepcopy(o['source']);anchor=q['binding'].get('core_anchor') or inv.catalog.name(oid);fine=False
        if anchor in inv.catalog.label_locations:location=copy.deepcopy(inv.catalog.label_locations[anchor]);fine=True
        else:
            m=re.fullmatch(r'(.+\.sol):(\d+)(?:[-:](\d+))?',anchor)
            if m and m[1] in inv.catalog.sources:
                chunks=inv.catalog.sources[m[1]]['content'].encode().splitlines(keepends=True);lo=int(m[2]);hi=int(m[3] or lo)
                start=sum(map(len,chunks[:lo-1]));end=sum(map(len,chunks[:hi]));location={'file':m[1],'start':start,'length':end-start};fine=True
        # Conservative source-root grouping. Do not equate different unlocated
        # business mechanisms merely because they share a variable/function.
        precise=assessment['scope'].get('decision',{}).get('locations',[])
        cause_location=assessment['scope']['decision'].get('causal_root')
        if cause_location:
            location=copy.deepcopy(cause_location);fine=True
        elif len(precise)==1 and precise[0].get('start') is not None and not fine:
            location=copy.deepcopy(precise[0]);fine=location!=o['source']
        effective=assessment['scope']['decision']
        # One actual incumbent replacement has the same cause whether policy was
        # stated in an issue, supplied as a scoped seed, or independently inferred.
        scoped_role=effective['reason']=='source_role_reassignment' and effective.get('effects') and 'current_authority_required' in effective.get('meanings',())
        if effective.get('opinion_source') and effective.get('effects'):
            cause=['located_effect',sorted(effective['effects']),item.get('phase'),item.get('actor'),item.get('subject')]
        elif scoped_role:
            cause=['incumbent_replacement',sorted(effective['effects']),item.get('phase'),item.get('scope'),item.get('assumptions') or []]
        else:
            cause=[assessment['scope'].get('claim_identity'),item.get('object'),item.get('actor'),
                   item.get('phase'),item.get('scope'),item.get('assumptions'),effective.get('effects',[])]
        identity=[inv.f.identity,assessment['category'],o['target'],location,cause]
        fid='finding_'+digest(identity)[:20]
        f=findings.setdefault(fid,{'id':fid,'category':assessment['category'],'target':o['target'],
            'root_location':location,'root_cause':{'operation':oid,'source_anchors':[location]},
            'operation':oid,'function':o['function'],'related_operations':q['binding']['operations'],
            'actor':item.get('actor'),'object':item.get('object'),'mechanism':assessment.get('composed_claim',item['claim']),
            'original_model_claim':item['claim'],'original_model_assessment':item['assessment'],
            'normal_explanation_considered':item.get('alternative'),'scope':assessment['scope'],
            'assumptions':item.get('assumptions',[]),'evidence_level':assessment.get('evidence_level','source_prediction'),
            'comparison_scope':mapping.get('status','main'),'formal_risk_query_required':False,'evidence_refs':[],'issue_ids':[]})
        f['evidence_refs']=sorted(set(f['evidence_refs']+q['evidence']));f['issue_ids'].append(qid)
    scope=reading_scope(inv,blocked_categories,assessments)
    blocked_categories={c for gap in scope['known_category_gaps'] for c in gap.get('affected_categories',[])}
    from pr_next_joint.reporting.effective_parameters import investigation_profile
    return {'effective_investigation_parameters':investigation_profile(inv.f.options),'method':VERSION,'program_identity':inv.f.identity,'task':inv.f.options.scope,'options':inv.f.options.record(),
        'implementation_sha256':inv.f.context['implementation_sha256'],
        'findings':list(findings.values()),'main_finding_ids':[k for k,v in findings.items() if v['comparison_scope']=='main'],
        'additional_finding_ids':[k for k,v in findings.items() if v['comparison_scope']=='additional'],
        'unresolved_mapping_ids':[k for k,v in findings.items() if v['comparison_scope']=='unresolved'],'inspection_records':records,
        'diagnostics':{'issues':inv.diagnostics,'unexecuted_actions':copy.deepcopy(inv.ready),
            'suppressed_source_predictions':suppressed,'program_gaps':copy.deepcopy(inv.f.gaps),
            'source_context_scope':inv.initial_manifest,'no_finding_is_not_contract_safety':True,
            'E1_not_formal_FREEZE':True},
        'model_analysis_available':inv.model_analysis_available,
        'prediction_basis_available':bool(findings or scope['negative_eligible_categories'] or decisive_records),
        'prediction_basis_issues':decisive_records,'unresolved_category_judgments':sorted(blocked_categories),
        'task_analysis':{'model_analysis_available':inv.model_analysis_available,'fixture_analysis_available':getattr(inv,'fixture_analysis_available',False),'usable_task_opinion':inv.usable_task_opinion,
            'empty_response_present':inv.explicit_empty_analysis,
            'explicit_empty_task_reading':bool(inv.explicit_empty_analysis and scope['whole_reading_eligible']),
            'model_declaration':inv.task_declaration,'reading_scope':scope,'local_judgment_not_global_safety':True,
            'unexecuted_actions':len(inv.ready),'task_conflicts':[qid for qid,q in inv.issues.items() if q.get('task_conflict')]},
        'model_reading_declarations_not_proof':inv.reading_declarations,
        'usage':{'attempts':copy.deepcopy(inv.session.attempts),**inv.session.accounting()},
        'provenance':{'refinement_decisions':copy.deepcopy(inv.refinements),'structural_references':{k:v['structural'] for k,v in inv.shared_reads.items() if v['result'] is not None},'shared_source_facts':{k:sorted(v['consumers']) for k,v in inv.shared_reads.items() if v['result'] is not None},'source_candidate_investigations':copy.deepcopy(getattr(inv,'candidate_trace',[])),'actions':copy.deepcopy(inv.actions),'revisions':copy.deepcopy(inv.updates),
            'evidence_labels':sorted(inv.evidence),'feedback_trace':copy.deepcopy(inv.feedback_trace),'cache_hits':inv.backend.cache_hits,
            'computation_reuse':copy.deepcopy(inv.backend.cache_stats),'model_call_decisions':copy.deepcopy(inv.call_decisions),
            'mechanism_attribution_not_a_new_detection_admission_gate':True},
        'prediction_frozen_before_gold':True,'scoring_performed':False,
        'risk_absence_statement':'No risk detected in the actual analyzed source scope; not proof of safety.'}

def evaluation_projection(report):
    """No Gold access, scoring or legacy query gate. Preserve positive source predictions."""
    cats=('AC',) if report['task']=='AC' else CATEGORIES[1:]
    found={f['category'] for f in report['findings'] if f.get('comparison_scope','main')=='main'}
    unknown=set(report.get('unresolved_category_judgments',[]))
    task=report.get('task_analysis',{});reading=task.get('reading_scope',{})
    # Archived reports retain their original projection; new reports carry prospective eligibility.
    if 'reading_scope' in task:
        eligible=set(reading['negative_eligible_categories'])
    else:
        eligible=set()
        unknown.update(set(cats) - found)
    obligations=reading.get('obligations',[])
    active=bool(report.get('model_analysis_available') or obligations or found or report.get('inspection_records'))
    if reading.get('schema') not in ('source-category-decision-r1','source-category-public-r1') and not obligations:eligible.clear()
    if report.get('method') in (VERSION,'permission-risks-semantic-propagation-r2','permission-risks-source-prediction-integration-r1','permission-risks-next-decision-only-r2'):
        states={c:'alarm' if c in found else 'not_run' if not active else
                'not_detected' if c in eligible and c not in unknown else 'unsupported' for c in cats}
    else:
        states={c:'alarm' if c in found else 'unsupported' if c in unknown else
                'not_detected' if c in reading.get('negative_eligible_categories',[]) else 'not_run' for c in cats}
    return {'predictions':states,
        'scope':report['diagnostics']['source_context_scope'],
        'coverage_basis':('Source opinions and actual scoped reading; optional refinement is independent.' if report.get('method') in (VERSION,'permission-risks-semantic-propagation-r2','permission-risks-source-prediction-integration-r1') else 'Finite source obligations, actual semantic/program completion and scoped residuals; delivery/declarations are records, not completion gates.'),
        'no_finding_does_not_prove_safety':True,'not_a_score':True,
        'enhancement_unfinished_does_not_erase_source_predictions':True}

```

## source/src/pr_next_joint/investigation/request_scope.py

SHA-256 `756330123ee084b1e802e36698d1936dbb089a348121df6485a73306cbc9f6c2`

```python
"""Bind an investigation to program uses named in the claim, separately from its finding anchor."""
import re

from pr_next_joint.frontend.path_ir import key, walk
from .roles import path_qualification
from pr_next_joint.frontend.storage import keys, selectors, selector_relation, value_type


def unique_cells(cells):
    return list({key(cell): cell for cell in cells}.values())


def use_reads(path):
    # A destination on the left of an assignment is not a read of its old value.
    values = [w['value'] for w in path['writes']]
    positions = [keys(w['path']) for w in path['writes']]
    return selectors([path['guards'], values, positions, path.get('sensitive_effects', []),
                      path.get('return_value'), path.get('evaluated_terms', [])])


def claim_entries(inv, binding, item):
    root = binding.get('core_operation')
    if not root:
        return set()
    operations = inv.f.operations
    target = operations[root]['target']
    applied = [[oid for oid in ids if operations[oid]['target']==target] for ids in binding['located'].values()]
    located = {ids[0] for ids in applied if len(ids)==1}
    wording = ' '.join(str(item.get(k, '')) for k in ('claim', 'distinguish', 'distinguishing_question'))
    tokens = set(re.findall(r'\b([A-Za-z_$][\w$]*)\s*\(', wording))
    by_name = {}
    for oid, op in operations.items():
        if op['target'] == target:
            by_name.setdefault(op['function'].split('(')[0], []).append(oid)
    # Use the already bound target. A bare overloaded name cannot nominate a use.
    located.update(ids[0] for name, ids in by_name.items() if name in tokens and len(ids) == 1)
    return {root} | {oid for oid in located if operations[oid]['target'] == target}


def holder_effect(inv, oid):
    # Shape of a possible effect, not a judgment that a mapping is a financial right.
    for _, path in inv.f.operation_paths(oid, True):
        if any(fx.get('kind') == 'native_transfer' for fx in path.get('sensitive_effects', [])):
            return True
        for w in path['writes']:
            cell = w['path']
            if keys(cell) and value_type(cell, inv.f.lookup(oid)).startswith(('uint','int')):
                return True
    return False


def linked_controls(inv, change, use):
    writes = [w['path'] for _, p in inv.f.operation_paths(change, True) for w in p['writes']]
    return [cell for cell in inv.graph.request_reads(use) if any(
        selector_relation(cell, w) == 'same_shape' and not inv.graph._disjoint_keys(cell, w) for w in writes)]


def request_target(inv, binding, item, plan, measure):
    """Resolve a claim endpoint before evaluating Boolean predictions on it."""
    root = binding['core_operation']
    claimed = claim_entries(inv, binding, item)
    request = item['observation']
    hint = item.get('next_check')
    hint = hint if isinstance(hint, dict) else {}
    at = request.get('at')
    after = request.get('after')
    target=inv.f.operations[root]['target']
    at_ids=[i for i in inv.catalog.resolve(at) if inv.f.operations[i]['target']==target] if at else []
    after_ids=[i for i in inv.catalog.resolve(after) if inv.f.operations[i]['target']==target] if after else []
    if at and (len(at_ids) != 1 or at_ids[0] not in claimed):
        return None, [], 'observation_entry_outside_or_ambiguous_in_claim'
    if after and (len(after_ids) != 1 or inv.f.operations[after_ids[0]]['target'] != inv.f.operations[root]['target']):
        return None, [], 'intervention_target_ambiguous_or_different'
    pairs = plan['selected_pairs'] + plan['deferred_pairs']
    downstream = list(dict.fromkeys(p['observe'] for p in pairs if p['change'] == root
                                     and p['observe'] != root and p['observe'] in claimed))
    # A financial effect must not silently become a setter's authorization guard.
    if inv.f.options.scope == 'FCR':
        downstream = [u for u in downstream if holder_effect(inv, u)]
    preferred = at_ids or (inv.catalog.resolve(hint.get('observe')) if hint.get('action') == 'compare' else [])
    if len(preferred) == 1 and preferred[0] in downstream:
        downstream.remove(preferred[0])
        downstream.insert(0, preferred[0])
    if at_ids and at_ids[0] != root and at_ids[0] not in downstream:
        return None, downstream, 'no_source_dependency_from_claim_to_requested_use'
    if at_ids == [root]:
        use = root
    elif downstream and (measure not in ('holder_grant','holder_net') or
                         after_ids == [root] or at_ids or not holder_effect(inv, root)):
        use = downstream[0]
    else:
        use = root
    if inv.f.options.scope == 'FCR' and measure in ('opens','blocks') and not holder_effect(inv, use):
        return None, downstream, 'no_claimed_holder_request; role_evidence_only'
    if use == root and measure in ('opens','blocks') and inv.f.options.scope == 'FCR':
        # No invented upstream administrator as a financial intervention.
        if not any(p['observe'] == root and p['change'] in claimed and p['change'] != root for p in pairs) and not after_ids:
            return None, downstream, 'no_identified_intervention_on_holder_request'
    return use, downstream, None


def select_controls(inv, use, candidates, request, item):
    candidates = unique_cells(candidates)
    name = request.get('control')
    if name:
        if not isinstance(name, str):
            return []
        return [c for c in candidates if name in (inv.backend._storage_name(use, c),
                    inv.f.lookup(use).nodes.get(c['root'], {}).get('name'))]
    # Preserve explicit ordered keys in natural-language claims, including this vs msg.sender.
    text = re.sub(r'\s*([.\[\]])\s*', r'\1', str(item.get('claim','')))
    indexed = [c for c in candidates if keys(c) and re.search(
        r'(?<![\w$])' + re.escape(inv.backend._storage_name(use,c)) + r'(?![\w$\[])', text)]
    return indexed or candidates


def compare_relevant(inv, q, evidence):
    root = inv.root(q)
    change, use = evidence.get('change'), evidence.get('observe')
    if not root or not change or not use:
        return False
    choice = q.get('plan', {}).get('observation_choice') or {}
    resolution = choice.get('request_resolution')
    if not resolution:
        if inv.f.options.scope == 'FCR' and use == root and not holder_effect(inv,root):
            # A legacy upstream qualifier is contextual only when a separately
            # sourced downstream holder request is the subject of this claim.
            if any(u != root and holder_effect(inv,u) and linked_controls(inv,root,u)
                   for u in claim_entries(inv,q['binding'],q['current'])):
                return False
        return True
    if resolution['use'] is None and inv.f.options.scope == 'FCR':
        hint=q['current'].get('next_check')
        claimed=use in claim_entries(inv,q['binding'],q['current'])
        scoped_probe=isinstance(hint,dict) and hint.get('action')=='compare' and inv.catalog.resolve(hint.get('change'))==[change] and inv.catalog.resolve(hint.get('observe'))==[use]
        return change==root and holder_effect(inv,use) and (claimed or scoped_probe and bool(linked_controls(inv,change,use)))
    selected=choice.get('selected')
    if selected and selected['measure'] in ('direct_effect','denied_qualified','missing_control','ledger_receipt','ledger_debit','ledger_grant'):
        return (evidence.get('observed_measure'),change,use)==(selected['measure'],selected['change'],selected['observe'])
    if resolution['use'] != root:
        return change == root and use == resolution['use']
    if inv.f.options.scope == 'FCR' and use != root:
        return False
    return True


def observation_applies(inv, q, result):
    pick = (q.get('plan', {}).get('observation_choice') or {}).get('selected')
    if not pick or pick['observe'] != result['observe'] or pick['change'] != result['change']:
        return False
    return (pick['measure'] == result['measure'] and pick['scope'] == result['scope']
            and pick['context'] == result.get('request_context', pick['context'])
            and pick.get('expectations') == result.get('expectations'))


def account_term(term, lookup):
    if term.get('kind') in ('actual_sender','transaction_origin'):
        return True
    return term.get('kind') == 'storage' and not term.get('segments') and value_type(term, lookup) in ('address','address payable')


def positive_caller_gate(node, lookup):
    if node.get('op') in ('and','&&'):
        return any(positive_caller_gate(v, lookup) for v in node.get('args', []))
    args = node.get('args', [])
    if node.get('op') == '!' and len(args) == 1 and args[0].get('op') == '!=':
        args = args[0]['args']
    elif node.get('op') != '==':
        return False
    return (len(args) == 2 and any(x.get('kind') == 'actual_sender' for x in args) and
            any(x.get('kind') == 'storage' and account_term(x, lookup) for x in args))


def privileged_intervention(inv, binding, item):
    """Scope an explicit mixed actor claim to a real guarded writer and dependent use."""
    if not binding.get('core_exact') or item.get('category') not in (
            'FCR-TRANSFER','FCR-MINT','FCR-DESTROY','FCR-PAUSE','FCR-FREEZE'):
        return []
    claimed = claim_entries(inv, binding, item)
    root = binding['core_operation']
    links = []
    for writer in sorted(claimed):
        paths = list(inv.f.operation_paths(writer, True))
        if not inv.backend.complete(writer) or not paths or not all(
                path_qualification(inv.f,writer,path) for _, path in paths):
            continue
        for use in sorted(claimed - {writer}):
            if root not in (writer,use) or not holder_effect(inv, use):
                continue
            controls = linked_controls(inv, writer, use)
            if controls:
                links.append({'change':writer,'use':use,'controls':controls,'status':'source_dependency_not_proof_of_harm'})
    return links


def opaque_paths(inv, oid):
    """An incomplete effect or actual external dependency cannot certify a local exclusion."""
    if inv.f.operations[oid].get('generated_getter'):
        return False
    if not inv.backend.complete(oid):
        return True
    for pid, path in inv.f.operation_paths(oid, True):
        deps = inv.backend.condition_dependencies(oid, pid, path)
        if deps['unknown_dependencies'] or deps['credential_dependencies']:
            return True
        if any(effect.get('kind') != 'native_transfer' for effect in path.get('sensitive_effects', [])):
            return True
    return False


def bounded_availability_scope(inv, q):
    """Limit an existing availability question only when the control changes admission alone."""
    item = q['current']
    if inv.f.options.scope != 'FCR' or item.get('category') != 'AC':
        return None
    obs = item.get('observation') or {}
    if not isinstance(obs,dict) or obs.get('measure') != 'blocks' or not q['binding'].get('core_exact'):
        return None
    if q['binding'].get('ambiguous') or q['binding'].get('unresolved'):
        return None
    root = inv.root(q)
    if opaque_paths(inv, root) or not any(inv.evidence[k].get('operation') == root
            and inv.evidence[k]['kind'] == 'source_inspection' for k in q['evidence']):
        return None
    cells = unique_cells(w['path'] for _,p in inv.f.operation_paths(root,True) for w in p['writes'])
    if len(cells) != 1 or value_type(cells[0],inv.f.lookup(root)) != 'bool':
        return None
    if any(p.get('sensitive_effects') for _,p in inv.f.operation_paths(root,True)):
        return None
    target = inv.f.operations[root]['target']
    claimed = claim_entries(inv, q['binding'], item)
    matched = []
    for use in sorted(inv.graph.access[(target,cells[0]['root'])]['readers'] - {root}):
        if inv.f.operations[use].get('generated_getter'):
            continue
        if opaque_paths(inv,use):
            return None
        paths = list(inv.f.operation_paths(use,True))
        if not any(s['root']==cells[0]['root'] for _,path in paths for s in use_reads(path)):
            continue
        if use not in claimed or not paths:
            return None
        shapes = set()
        for _,path in paths:
            outputs = [path['writes'],path.get('sensitive_effects',[]),path.get('return_value')]
            if any(s['root']==cells[0]['root'] for s in selectors(outputs)):
                return None
            if not any(s['root']==cells[0]['root'] for s in selectors(path['guards'])):
                return None
            # Only ordinary use of the caller's own right, not a transfer/mint on another's behalf.
            if not any(w['value'].get('op')=='-' and key(w['value']['args'][0])==key(w['path'])
                       and (inv.backend._holder(use,w['path']) or {}).get('kind')=='actual_sender'
                       for w in path['writes']):
                return None
            shapes.add(key(outputs))
        if len(shapes)!=1:
            return None
        matched.append(use)
    if matched:
        return {'reason':'bounded_holder_availability_question','effect_entries':matched,
                'control':cells[0],'affected_categories':['FCR-PAUSE','FCR-FREEZE'],
                'limits':'only this pending blocking observation; no finding or whole-task conclusion'}
    return None


def coverage_facts(inv, q):
    if inv.f.options.scope != 'FCR' or not q.get('task_conflict'):
        return None
    token = (q['version'], tuple(q['evidence']))
    cached = q.get('_coverage_facts')
    if cached and cached[0] == token:
        return cached[1]
    try:
        result = local_task_scope(inv,q) or bounded_availability_scope(inv,q)
        if result is None and explicit_outside_scope(inv,q):
            result = {'reason':'recorded_explicit_non_task_clue','affected_categories':[],
                      'effect_entries':sorted(claim_entries(inv,q['binding'],q['current'])),
                      'limits':'source bounded, independent findings preserved'}
    except (KeyError,ValueError,TypeError,IndexError,NotImplementedError,TimeoutError) as error:
        inv.diagnostics.append({'issue':q['id'],'reason':'coverage_scope_unestablished',
                                'details':str(error),'no_new_negative':True})
        result = None
    q['_coverage_facts'] = token,result
    return result


def explicit_outside_scope(inv, q):
    if q.get('task_review',{}).get('status') != 'explicit_out_of_task_clue':
        return False
    binding = q['binding']
    if not binding.get('core_exact') or binding.get('ambiguous') or binding.get('unresolved'):
        return False
    entries = claim_entries(inv,binding,q['current'])
    for oid in entries:
        if opaque_paths(inv,oid):
            return False
        for _,path in inv.f.operation_paths(oid,True):
            for w in path['writes']:
                readers = inv.graph.access[(inv.f.operations[oid]['target'],w['path']['root'])]['readers']
                if any(opaque_paths(inv,u) for u in readers):
                    return False
    return True


def local_task_scope(inv, q):
    """A local certificate for an explicitly non-financial clue, never a whole-task negative."""
    item, binding = q['current'], q['binding']
    if inv.f.options.scope != 'FCR' or item.get('category') != 'AC' or not binding.get('core_exact'):
        return None
    if binding.get('ambiguous') or binding.get('unresolved'):
        return None
    root = binding['core_operation']
    entries = claim_entries(inv, binding, item)
    lookup = inv.f.lookup(root)
    # A local, scoped normal conclusion requires actual accepted source inspection.
    inspected = {inv.evidence[e].get('operation') for e in q['evidence']
                 if inv.evidence[e]['kind'] == 'source_inspection' and not inv.evidence[e].get('local_errors')}
    if root not in inspected or not entries:
        return None
    pure_event = True
    role_writes = set()
    role_readers = set()
    for oid in entries:
        declaration = lookup.nodes.get(inv.f.operations[oid]['source'].get('ast_id'), {})
        if (oid != root and declaration.get('nodeType') == 'VariableDeclaration'
                and declaration.get('stateVariable') and declaration.get('visibility') == 'public'
                and declaration.get('typeDescriptions', {}).get('typeString') in ('address','address payable')):
            continue  # compiler-generated read-only identity accessor, not an unexamined action
        if not inv.backend.complete(oid):
            return None
        commits = list(inv.f.operation_paths(oid, True))
        if not commits:
            return None
        for pid, path in commits:
            audit = inv.backend.condition_dependencies(oid, pid, path)
            if (path.get('sensitive_effects') or audit['unknown_dependencies'] or audit['credential_dependencies']
                    or path.get('return_value') is not None and not account_term(path['return_value'], lookup)):
                return None
            if path['writes']:
                pure_event = False
                if item.get('assessment') != 'normal' or not path_qualification(inv.f,oid,path):
                    return None
            for w in path['writes']:
                dest, val = w['path'], w['value']
                if not account_term(dest, lookup) or not (account_term(val, lookup) or val.get('kind') in ('parameter','literal')):
                    return None
                role_writes.add(dest['root'])
                role_readers.update(s['root'] for g in path['guards'] for s in selectors(g))
        # payable entry or opaque effects cannot be certified event/role-only.
        if lookup.function(inv.f.operations[oid]['function']).get('stateMutability') == 'payable':
            return None
    if pure_event:
        for oid in entries:
            fn = lookup.function(inv.f.operations[oid]['function'])
            body = fn.get('body') or {}
            if fn.get('modifiers') or not body.get('statements') or any(
                    n.get('nodeType') != 'EmitStatement' for n in body['statements']):
                return None
            # A helper called by another entry can affect an enclosing transaction.
            if any(n.get('nodeType') == 'FunctionCall' and
                   n.get('expression',{}).get('referencedDeclaration') == fn.get('id')
                   for other, op in inv.f.operations.items() if other != oid and op['target'] == inv.f.operations[oid]['target']
                   for n in walk(lookup.function(op['function']))):
                return None
    else:
        # An address-valued setter can also select the recipient of a payout or an external
        # implementation. Only role positions used solely for authorization/role updates qualify.
        for cell in role_writes:
            for use in inv.graph.access[(inv.f.operations[root]['target'], cell)]['readers']:
                if not inv.backend.complete(use):
                    return None
                for _, path in inv.f.operation_paths(use, True):
                    returned = path.get('return_value')
                    plain_getter = not path['writes'] and returned and account_term(returned, lookup)
                    payload = [path.get('sensitive_effects', []), None if plain_getter else returned,
                               [keys(w['path']) for w in path['writes']],
                               [w['value'] for w in path['writes'] if not (use in entries and account_term(w['path'], lookup))]]
                    if any(s['root'] == cell for s in selectors(payload)):
                        return None
                    for guard in path['guards']:
                        if any(s['root'] == cell for s in selectors(guard)) and not positive_caller_gate(guard, lookup):
                            # Nonzero/nominee inequality on the local handover itself is harmless.
                            if use not in entries:
                                return None
        for cell in role_writes:
            writers = inv.graph.access[(inv.f.operations[root]['target'], cell)]['writers']
            if not writers <= entries:
                return None
        if not role_writes & role_readers:
            return None
    return {'reason':'source_local_event' if pure_event else 'source_local_normal_authority',
            'effect_entries':sorted(entries), 'affected_categories':[],
            'limits':'only this issue; external/asset dependencies and other issues assessed independently'}


```

## source/src/pr_next_joint/investigation/roles.py

SHA-256 `ee01f4f76769f2f4b5b30a84fbbcd649e848a10eda6bad3e820b5f5904c714b2`

```python
"""Source-grounded qualifications for a specific compiled target and committing path."""
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys,selectors


def _roots(node, allowed, positive=True):
    """Return role declarations required by the condition; all arms of a disjunction must qualify."""
    args, op = node.get('args', []), node.get('op')
    if op == '!' and len(args) == 1:
        return _roots(args[0], allowed, not positive)
    if op in ('and', '&&', 'or', '||') and args:
        roots = [_roots(x, allowed, positive) for x in args]
        conjunction = (op in ('and', '&&')) == positive
        return set().union(*roots) if conjunction or all(roots) else set()
    if op in ('==', '!=') and len(args) == 2:
        equality = (op == '==') == positive
        for side, other in (args, args[::-1]):
            if other.get('kind') == 'literal' and type(other.get('value')) is bool:
                return _roots(side, allowed, equality == other['value'])
            if equality and other.get('kind') == 'actual_sender' and side.get('kind') == 'storage':
                rid = side['root']
                if not side.get('segments') and not side.get('instance') and rid in allowed:
                    return {rid}
    if positive and node.get('kind') == 'storage' and not node.get('instance') and node['root'] in allowed:
        idx = keys(node)
        if len(node.get('segments', [])) == len(idx) == 1 and idx[0].get('kind') == 'actual_sender':
            return {node['root']}
    return set()


def effective_roots(guard, allowed):
    """An explicit self-call arm does not remove the qualified outsider arm.
    Used for privilege existence only. The encoded guard keeps both alternatives.
    """
    roots = _roots(guard,allowed)
    if roots or guard.get('op') not in ('or','||'):
        return roots
    arms = guard['args']
    external = [arm for arm in arms if not (arm.get('op') == '==' and
                {v.get('kind') for v in arm.get('args',[])} == {'actual_sender','contract_address'})]
    if len(external) != 1 or len(external) == len(arms):
        return set()
    return _roots(external[0],allowed)


def _seed_address(node, parameters):
    if not node:return None
    if node.get('memberName') == 'sender' and node.get('expression', {}).get('name') == 'msg':
        return {'term':'deployer'}
    if node.get('referencedDeclaration') in parameters:
        return {'term':'constructor_parameter','id':node['referencedDeclaration']}
    if node.get('nodeType') == 'FunctionCall' and node.get('kind') == 'typeConversion' and len(node.get('arguments', [])) == 1:
        return _seed_address(node['arguments'][0], parameters)
    if node.get('nodeType') == 'Literal':
        try:value = int(node.get('value',''),0)
        except (ValueError,TypeError):return None
        if 0 < value < 2**160:return {'term':'address_literal','value':value}
    return None


def _is_table(decl):
    typ = decl.get('typeName') or {}
    return (typ.get('nodeType')=='Mapping' and typ.get('keyType',{}).get('name')=='address'
            and typ.get('valueType',{}).get('name')=='bool')


def _role_index(facts, target):
    from .initial_state import model,domain,CAPABILITY
    initial=model(facts,target);lookup=facts.lookups[target]
    token=(target,domain(lookup),initial['identity'])
    cache=facts.__dict__.setdefault('_authority_by_target',{})
    if token in cache:return cache[token]
    decls={rid:lookup.nodes[rid] for rid,row in initial['declarations'].items() if
        _is_table(lookup.nodes[rid]) or row['type'] in ('address','address payable')}
    origins={r:[] for r in decls};writers={r:[] for r in decls};invalid=set();seen={r:set() for r in decls}
    clean=[p for p in initial['constructor_paths'] if p['flow'] in ('normal','returned') and not p.get('issues') and not p.get('evaluation_gaps')]
    def seed(term):
        if term.get('kind')=='actual_sender':return {'term':'deployer'}
        if term.get('kind')=='parameter' and term.get('id') in initial['constructor_parameters']:
            return {'term':'constructor_parameter','id':term['id']}
        if term.get('kind')=='literal' and type(term.get('value')) is int and 0<term['value']<2**160:
            return {'term':'address_literal','value':term['value']}
        return None
    for rid,decl in decls.items():
        row=initial['declarations'][rid]
        if any(p.get('issues') or p.get('evaluation_gaps') for p in initial['constructor_paths']):
            if row['constructor_writes'] or row['explicit_constructor_sites'] or row['explicit_initializer']:invalid.add(rid)
        for pi,p in enumerate(clean):
            relevant=[w for w in p['writes'] if w['path']['root']==rid]
            if not _is_table(decl):relevant=relevant[-1:]
            for w in relevant:
                v=w['value'];idx=keys(w['path'])
                origin=seed(idx[0]) if _is_table(decl) and len(idx)==1 and v.get('kind')=='literal' and v.get('value') is True else seed(v) if not _is_table(decl) else None
                if origin:origins[rid].append(dict(origin,source=w['source'],constructor_path=pi,guards=p['guards'],source_kind='constructor'))
                elif not _is_table(decl) and v.get('kind')=='literal' and v.get('value')==0:pass
                elif not _is_table(decl):invalid.add(rid)
        if not origins[rid] and domain(lookup)==CAPABILITY and row['type'] in ('address','address payable') and not row['explicit_initializer'] and not row['constructor_writes'] and not row['explicit_constructor_sites']:
            origins[rid].append({'term':'abstract_initial_role','declaration':rid,'source':row['source'],
                'source_kind':'declared_conditional_initial_assumption','analysis_domain':CAPABILITY})
    for rid,rows in initial['runtime_writers']['paths'].items():
        if rid not in decls:continue
        for row in rows:
            seen[rid].add(row['source'].get('ast_id'))
            if row['flow']=='reverted':continue
            if not row['complete']:invalid.add(rid);continue
            p=facts.paths[row['path']]['raw'];dst=row['cell'];value=row['value']
            if key(dst)==key(value) or value.get('kind')=='literal' and value.get('value') in (False,0):continue
            writers[rid].append({'operation':row['operation'],'path':row['path'],'guards':p['guards'],'site':row['source'].get('ast_id')})
    for rid in decls:
        missing=set(initial['runtime_writers']['sites'].get(rid,[]))-seen[rid]
        # A source site on a fully known reverting path cannot grant authority.
        if missing:invalid.add(rid)
    known={r for r in decls if r not in invalid and (origins[r] or writers[r])}
    if initial['runtime_writers']['opaque_storage_writes']:known.clear()
    # For FCR, an incumbent OR this-contract guard preserves the incumbent
    # arm only when the public body cannot forward a selector into the grant.
    # Built-in send/transfer have empty calldata; other unresolved CALLs stay open.
    def can_forward(call):
        if facts.operations[call['operation']]['target']!=target or call['mode']=='STATICCALL':return False
        node=lookup.nodes.get(call['source'].get('ast_id'),{})
        builtin=node.get('expression',{}).get('typeDescriptions',{}).get('typeIdentifier','')
        return not builtin.startswith(('t_function_send','t_function_transfer'))
    role_guard=effective_roots if facts.options.scope=='FCR' and not any(can_forward(c) for c in facts.call_summaries.rows.values()) else _roots
    def protected(writer,roots):return set().union(*(role_guard(g,roots) for g in writer['guards']))
    def close(s):
        while True:
            keep={r for r in s if all(protected(w,s) for w in writers[r])}
            if keep==s:return keep
            s=keep
    known=close(known);active={r for r in known if origins[r]}
    while True:
        add={r for r in known-active if any(protected(w,active) for w in writers[r])}
        if not add:break
        active.update(add)
    active=close(active)
    records={r:{'declaration':r,'target':target,'kind':'caller_membership' if _is_table(decls[r]) else 'caller_equals_account',
        'source':lookup.anchor(decls[r]),'deployment_origins':[o for o in origins[r] if o['term']!='abstract_initial_role'],
        'abstract_origins':[o for o in origins[r] if o['term']=='abstract_initial_role'],
        'source_origins':origins[r],'analysis_domain':domain(lookup),'initial_model_identity':initial['identity'],
        'guarded_grant_paths':[{'operation':w['operation'],'path':w['path'],'site':w['site'],
            'qualifying_declarations':sorted(protected(w,active)),
            'qualification_guards':[g for g in w['guards'] if role_guard(g,active)]} for w in writers[r]],
        'has_runtime_assignment':bool(initial['runtime_writers']['sites'].get(r))} for r in sorted(active)}
    facts.__dict__.setdefault('_authority_diagnostics',{})[target]={'analysis_domain':domain(lookup),'unresolved_declarations':sorted(invalid),
        'reachable_function_ids':initial['runtime_writers']['functions'],'opaque_storage_writes':initial['runtime_writers']['opaque_storage_writes']}
    cache[token]=records
    return records


def _same_public_effect(facts,oid,path,registry):
    """Both sides of an if can implement an identical operation. A caller test alone then confers no advantage."""
    def effect(p):
        return key([[(w['path'],w['value']) for w in p['writes']],p.get('sensitive_effects',[]),p.get('return_value')])
    guards=set(map(key,path['guards']))
    for _,other in facts.operation_paths(oid,True):
        if other is path or any(_roots(g,registry) for g in other['guards']):continue
        opposite=set(map(key,other['guards']))
        for g in path['guards']:
            if not _roots(g,registry):continue
            neg=g['args'][0] if g.get('op')=='!' else {'kind':'op','op':'!','args':[g]}
            if opposite==(guards-{key(g)})|{key(neg)} and effect(path)==effect(other):return True
    return False


def path_qualification(facts, oid, path):
    cache=facts.__dict__.setdefault('_path_qualifications',{})
    from .initial_state import domain
    token=(oid,id(path),domain(facts.lookup(oid)))
    if token in cache:return cache[token]
    target=facts.operations[oid]['target']
    registry=_role_index(facts,target)
    proof=[]
    for g in path['guards']:
        ids=(effective_roots if facts.options.scope=='FCR' else _roots)(g,registry)
        if ids:proof.append({'guard':g,'roles':[registry[i] for i in sorted(ids)]})
    if proof and _same_public_effect(facts,oid,path,registry):proof=[]
    if proof:
        principal_ids={r['declaration'] for row in proof for r in row['roles']}
        # A second source read may alias the very deployer denoted by the qualifying table.
        related={c['root'] for c in selectors([path['guards'],path['writes']]) if c['root'] in registry}
        proof[0]['related_fixed_accounts']=[registry[i] for i in sorted(related-principal_ids)
                    if registry[i]['kind']=='caller_equals_account' and not registry[i]['has_runtime_assignment']]
    cache[token]=proof
    return proof


def fixed_role_terms(encoder, qualification, slot):
    """Use the same deployment identities across fixed membership tables and fixed scalar roles."""
    from pr_next_joint.verification.sequence import qualify
    roles={r['declaration']:r for row in qualification for r in row['roles']+row.get('related_fixed_accounts',[])}
    from .initial_state import domain,CAPABILITY,DEPLOYMENT,initial_for_lookup
    if domain(encoder.lookup) in (CAPABILITY,DEPLOYMENT) and initial_for_lookup(encoder.lookup):
        return [],[{'declaration':rid,'origins':r.get('source_origins',r['deployment_origins']),
            'scope':'constructor and committed prefix encoded by shared initial state model',
            'analysis_domain':domain(encoder.lookup)} for rid,r in roles.items()]
    z=encoder.z;terms=[];receipt=[]
    caller=encoder.expr(qualify({'kind':'actual_sender'},slot))
    for rid,role in roles.items():
        if role['guarded_grant_paths'] or not role['deployment_origins']:continue
        if role['kind']=='caller_equals_account' and len(role['deployment_origins'])!=1:continue
        values=[]
        for origin in role['deployment_origins']:
            if origin['term']=='address_literal':values.append(z.IntVal(origin['value']));continue
            symbol='deployment_caller' if origin['term']=='deployer' else 'deployment_address_parameter_'+str(origin['id'])
            value=z.Int(symbol);terms.extend([value>=0,value<2**160])
            if origin['term']=='deployer':terms.append(value!=0)
            values.append(value)
        cell={'kind':'storage','root':rid,'segments':[]}
        if role['kind']=='caller_membership':
            cell['segments']=[{'key':{'kind':'actual_sender'}}]
            member=encoder.expr(qualify(cell,slot))
            seeded=z.Or(*[caller==v for v in values])
            terms.append(z.Implies(member,seeded) if role['has_runtime_assignment'] else member==seeded)
        else:
            account=encoder.expr(cell)
            terms.append(z.Or(account==0,account==values[-1]) if role['has_runtime_assignment'] else account==values[-1])
        receipt.append({'declaration':rid,'origins':role['deployment_origins'],
                        'scope':'cannot add members; revocation possible' if role['has_runtime_assignment'] else 'fixed original role at queried caller'})
    return terms,receipt


```

## source/src/pr_next_joint/investigation/scope_relevance.py

SHA-256 `f996a843ba5bf16b6687ce5cc1663320fcaa6e0bece213f00e5b9d1f29fab7a9`

```python
"""Source necessary conditions for per-entry, per-category obligations.

An excluded necessary condition can close a route without resolving an
unrelated call. This is a dependency certificate, not candidate-list emptiness.
"""
from pr_next_joint.frontend.path_ir import walk, key
from pr_next_joint.frontend.storage import keys, selectors, value_type, selector_relation
from .contracts import CATEGORIES


def source_role_may(f,oid):
    """Whole resolved body scan, including statements beyond a loop frontier."""
    cache=f.__dict__.setdefault('_source_role_may',{})
    if oid in cache:return cache[oid]
    lookup=f.lookup(oid);entry=lookup.function(f.operations[oid]['function'])
    pending=[entry];seen=set();bodies=[]
    while pending:
        body=pending.pop();bid=body.get('id')
        if bid in seen:continue
        seen.add(bid);bodies.append(body)
        for n in walk(body):
            if n.get('nodeType')=='ModifierInvocation':
                d=lookup.nodes.get(n.get('modifierName',{}).get('referencedDeclaration'),{})
                if d:pending.append(d)
            if n.get('nodeType')=='FunctionCall':
                exp=n.get('expression',{});d=lookup.nodes.get(exp.get('referencedDeclaration'),{})
                if d.get('body') and (exp.get('nodeType')=='Identifier' or
                    't_function_internal' in exp.get('typeDescriptions',{}).get('typeIdentifier','')):
                    pending.append(d)
    def sender(n):
        return (n.get('nodeType')=='MemberAccess' and n.get('memberName') in ('sender','origin') and
                n.get('expression',{}).get('name') in ('msg','tx'))
    tainted=set()
    nodes=list(walk(bodies))
    while True:
        old=set(tainted)
        for n in nodes:
            rhs=n.get('rightHandSide') if n.get('nodeType')=='Assignment' else n.get('initialValue')
            if rhs and any(sender(t) or t.get('referencedDeclaration') in tainted for t in walk(rhs)):
                dst=n.get('leftHandSide',{}).get('referencedDeclaration')
                if dst is not None:tainted.add(dst)
                tainted.update(d['id'] for d in n.get('declarations',[]) if d)
        if old==tainted:break
    result=False
    for n in nodes:
        if n.get('nodeType')=='BinaryOperation' and n.get('operator') in ('==','!='):
            for a,b in ((n['leftExpression'],n['rightExpression']),(n['rightExpression'],n['leftExpression'])):
                if (sender(a) or a.get('referencedDeclaration') in tainted) and not (
                    b.get('nodeType')=='Literal' and b.get('value') in ('0','0x0')):result=True
        if n.get('nodeType')=='IndexAccess' and n.get('typeDescriptions',{}).get('typeString')=='bool':
            if any(sender(t) or t.get('referencedDeclaration') in tainted for t in walk(n.get('indexExpression'))):result=True
    cache[oid]=result;return result


def potential_role(f,oid,path):
    from .roles import path_qualification, effective_roots
    if path_qualification(f,oid,path):return True
    lookup=f.lookup(oid)
    allowed={n['id'] for n in lookup.decls.values() if n.get('stateVariable') and
        (n.get('typeDescriptions',{}).get('typeString') in ('address','address payable') or
         n.get('typeName',{}).get('nodeType')=='Mapping')}
    for guard in path['guards']:
        if effective_roots(guard,allowed):return True
        for term in walk(guard):
            if term.get('op') in ('==','!=') and any(a.get('kind')=='actual_sender' for a in term.get('args',[])):
                if any(a.get('kind') in ('literal','parameter') for a in term.get('args',[])):return True
            if term.get('kind') in ('unknown','external_return','read_call','call_unresolved'):
                origins=[i for i in path.get('issues',[]) if i.get('reason')==term.get('reason')]
                # A low-level CALL's success flag is not itself a privileged
                # qualification. Callback entry guards are inspected separately.
                if not origins:return True
                for row in origins:
                    node=lookup.nodes.get(row.get('source',{}).get('ast_id'),{})
                    calls=[n for n in walk(node) if n.get('nodeType')=='MemberAccess']
                    if not any(n.get('memberName') in ('call','send','transfer') and
                        n.get('typeDescriptions',{}).get('typeIdentifier','').startswith(('t_function_barecall','t_function_send','t_function_transfer')) for n in calls):
                        return True
    return False


def nonfinancial(backend,oid,cell):
    from .key_roles import relation
    from .ledger import unit_origin,native_only_position
    lookup=backend.f.lookup(oid)
    if (relation(cell,lookup) or {}).get('kind')=='authorization_quantity':return 'holder_authorization_quantity'
    if native_only_position(backend,oid,cell):return 'native_redemption_not_five_class_token_unit'
    semantic=getattr(backend,'semantics',None)
    binding=semantic.lookup(oid,cell) if semantic else None
    if binding and binding['meaning']=='nonfinancial_counter' and not unit_origin(backend,oid,cell):
        return 'source_bound_nonfinancial_interpretation'
    # Clocks and control flags do not become minted tokens merely because a
    # setter changes a numeric value. Require source evidence of dual use.
    temporal=any(any(selector_relation(s,cell)=='same_shape' for s in selectors(g)) and
        any(n.get('kind') in ('block_timestamp','block_number') or n.get('kind')=='environment' and
            n.get('field') in ('timestamp','number') for n in walk(g))
        for other,o in backend.f.operations.items() if o['target']==backend.f.operations[oid]['target']
        for _,p in backend.f.operation_paths(other) for g in p['guards'])
    if temporal and not unit_origin(backend,oid,cell):return 'source_time_dimension_without_asset_use'
    return None


def detached_holder_switch(inv,oid):
    """Resolve one local account switch against the actual public outgoing paths.
    A query getter is not a holder action. Independent external contracts and
    their balances remain outside this conclusion."""
    cache=inv.__dict__.setdefault('_detached_holder_switch',{})
    if oid in cache:return cache[oid]
    if inv.program_remaining()<=0:return None
    f=inv.f;lookup=f.lookup(oid);target=f.operations[oid]['target']
    rows=f.summaries.rows(oid)
    writes=[w for r in rows for w in r['ordered_writes']]
    toggles=[w for w in writes if keys(w['path']) and value_type(w['path'],lookup)=='bool']
    if not toggles or not inv.backend.complete(oid) or any(
            r['residuals'] or r['effects'] or any(local.get('may_directions') and local['holder'] is not None
            and value_type(local['cell'],lookup)!='bool' and local['cell']['root'] not in {w['path']['root'] for w in writes if w['value'].get('kind')=='parameter'}
            for local in r['numeric_effects']) for r in rows):
        cache[oid]=None;return None
    if any(w['value'].get('kind') not in ('parameter','literal') for w in writes):
        cache[oid]=None;return None
    roots={w['path']['root'] for w in writes}
    transfers=[];dependent=False
    downstream=f.summaries.dependencies.forward(oid)['uses']
    for use,op in f.operations.items():
        if op['target']!=target or op.get('generated_getter'):continue
        if inv.program_remaining()<=0:return None
        for r in f.summaries.rows(use,False):
            from .key_roles import relation
            spending=any(e.get('holder') is not None and 'debit' in e['may_directions']
                         and (relation(e['cell'],lookup) or {}).get('kind')!='authorization_quantity'
                         and e['cell']['root'] not in roots for e in r['numeric_effects'])
            if not spending:continue
            # Direct and transitive value/guard dependencies both remain open.
            transfers.append(use)
            if (use in downstream or any(c['root'] in roots for c in selectors([r['guards'],
                    [(w['path'].get('segments',()),w['value']) for w in r['ordered_writes']]]))
                    or any(v.get('reason') not in ('external_destination_not_bound','multiple_address_keys_need_source_holder_binding')
                           for v in r['residuals'])):dependent=True
            # Only the dependence on this local switch is being closed. Keep
            # independent external calls in their own entry's coverage record.
            if any(c['root'] in roots for c in selectors([r.get('effects',[]),
                    f.paths[r['path']]['raw'].get('evaluated_terms',[])])):dependent=True
        if not inv.backend.complete(use):
            if use in downstream or any(g.get('kind') in ('path_extraction','source_expression_limit','dependent_source_expression_limit') for g in op.get('gaps',())):dependent=True
            # An unresolved ordinary foreign call does not read local storage
            # unless its result flows back to the outgoing effect or a callback
            # has a local reader. Keep opaque local code open.
            if any(any(v in str(issue.get('reason','')) for v in ('unsupported_statement','unresolved_storage','write_expansion','source_path_frontier','assembly'))
                   for _,path in f.operation_paths(use) for issue in path.get('issues',())):dependent=True
    if any(c['mode']=='DELEGATECALL' and c.get('unresolved_implementation') and
           f.operations[c['operation']]['target']==target for c in f.call_summaries.rows.values()):dependent=True
    result=None
    if transfers and not dependent:
        result={'reason':'detached_local_holder_switch','operation':oid,'target':target,
                'locations':[w['source'] for w in toggles],'outgoing_entries':sorted(set(transfers))}
    cache[oid]=result
    return result


def directory(inv,oid,control_categories):
    from .ledger import unit_origin
    f=inv.f;lookup=f.lookup(oid);operation=f.operations[oid]
    if operation.get('generated_getter'):
        return {'operation':oid,'target':operation['target'],'possible_categories':[],
            'source_routes':[],'excluded_necessary_condition':'compiler_generated_readonly_getter',
            'absence_certificates':{c:{'necessary':'stateful intervention or affected transfer',
                'basis':'compiler_generated_readonly_getter','operation':oid,'target':operation['target'],
                'source':operation['source'],'domain':inv.f.identity,'decisive_residuals':[]} for c in CATEGORIES[1:]},
            'source':operation['source'],'control_categories':[],
            'unresolved_same_storage_calls':[],'unread_effect_residuals':[]}
    rows=f.summaries.rows(oid,False);cats=set(control_categories);routes=[]
    calls=[r for r in f.call_summaries.rows.values() if r['operation']==oid]
    delegate=[c for c in calls if c['mode']=='DELEGATECALL' and c['unresolved_implementation']]
    if delegate:cats.update(CATEGORIES[1:])
    for row in rows:
        p=f.paths[row['path']]['raw'];possible=set();facts=[]
        if p['flow']=='reverted':
            routes.append({'path':row['path'],'possible_categories':[], 'excluded_necessary_condition':'outer_transaction_does_not_commit'})
            continue
        role=potential_role(f,oid,p) or (p['flow']=='truncated' and source_role_may(f,oid))
        if not role and not delegate:
            facts.append('no_privileged_qualification_on_this_source_route')
        else:
            moves={s:[] for s in ('-','+')}
            for e in row['numeric_effects']:
                if e['holder'] is None:continue
                why=nonfinancial(inv.backend,oid,e['cell'])
                if why:
                    facts.append({'position':e['cell'],'excluded_financial_unit':why});continue
                for sign,direction in (('-','debit'),('+','credit')):
                    if direction in e['may_directions']:moves[sign].append(e['cell'])
            paired=lambda a,others:any(selector_relation(a,b)=='same_shape' and key(a)!=key(b) for b in others)
            if any(paired(d,moves['+']) for d in moves['-']):possible.add('FCR-TRANSFER')
            # A structural cross-key credit is not necessarily compensation, and a
            # paired debit need not account for the entire credit. Compare amounts later.
            if moves['-']:possible.add('FCR-DESTROY')
            if moves['+']:possible.add('FCR-MINT')
            for call in calls:
                if call['path']!=row['path'] or not call['unresolved_implementation']:continue
                n=lookup.nodes.get(call['source'].get('ast_id'),{})
                declaration=lookup.nodes.get(n.get('expression',{}).get('referencedDeclaration'),{})
                # A source-declared ordinary external method can affect its
                # separate asset ledger; native value calls alone cannot mint
                # or destroy a local token ledger. Known callback writes are
                # retained under their own original entries and qualifications.
                if call['mode']=='DELEGATECALL':possible.update(CATEGORIES[1:])
                elif call['mode']!='STATICCALL' and declaration.get('nodeType')=='FunctionDefinition':
                    possible.update(('FCR-TRANSFER','FCR-MINT','FCR-DESTROY'))
        cats.update(possible)
        routes.append({'path':row['path'],'possible_categories':sorted(possible),
            'qualification_may_hold':role,'necessary_condition_facts':facts,
            'residuals':row['residuals'],'flow':p['flow']})
    # A failed frontend or a path abandoned before its body was inspected
    # cannot supply a no-effect certificate. Loop frontier residuals retain
    # the classes of their actual body effects; arbitrary assembly does not.
    hard=[g for g in operation.get('gaps',[]) if g.get('kind') in ('path_extraction','source_expression_limit','dependent_source_expression_limit')]
    opaque=[i for _,p in f.operation_paths(oid) for i in p.get('issues',[]) if
        any(s in str(i.get('reason','')) for s in ('unsupported_statement','unresolved_storage','write_expansion','source_path_frontier_bound_exceeded'))]
    if not rows or hard or opaque:cats.update(CATEGORIES[1:])
    closure=f.summaries.dependencies.forward(oid)
    amount_uses=[]
    for use,kinds in closure['uses'].items():
        if 'value' not in kinds:continue
        if any(not nonfinancial(inv.backend,use,c) for c in f.summaries.positions(use)):
            amount_uses.append(use)
    if amount_uses:
        # This is a conservative investigation frontier, not evidence that a
        # transfer, issue or loss really occurred.
        cats.update(('FCR-TRANSFER','FCR-MINT','FCR-DESTROY'))
    exclusions={}
    complete=bool(rows) and inv.backend.complete(oid) and not (hard or opaque or delegate)
    committed=[row for row in rows if row['committing']]
    harmless=all(not row['ordered_writes'] and not row['effects'] and not row['residuals'] for row in committed)
    effect_calls=[c for c in calls if c['mode']!='STATICCALL']
    basis=None
    if complete and not committed:
        basis='all_extracted_exits_revert'
    elif complete and harmless and not effect_calls:
        basis='committed_exits_have_no_state_or_external_effect'
    elif complete and not effect_calls and not any(r['effects'] for r in committed):
        # A pure getter may expose a flag without affecting a holder request.
        # Establish this from ALL resolved public bodies, including reverted
        # guards and subscripts, independently of the candidate edge index.
        target=operation['target']
        scans=inv.__dict__.setdefault('_public_effect_reads',{})
        if target not in scans:
            members=[o for o,v in f.operations.items() if v['target']==target and not v.get('generated_getter')]
            all_resolved=all(inv.backend.complete(o) for o in members) and not any(
                call['operation'] in members and call.get('unresolved_implementation')
                for call in f.call_summaries.rows.values())
            reads={}
            for use in members:
                roots=set()
                for _,p in f.operation_paths(use):
                    terms=[p['guards'],p.get('return_value'),p.get('evaluated_terms'),p.get('sensitive_effects')]
                    for w in p['writes']:terms.extend([w['value'],keys(w['path'])])
                    roots.update(s['root'] for s in selectors(terms))
                reads[use]=roots
            scans[target]=(all_resolved,reads)
        all_resolved,reads=scans[target]
        cells=[w['path'] for r in committed for w in r['ordered_writes']]
        roots={c['root'] for c in cells}
        if all_resolved and cells and not any(r['residuals'] for r in committed) and not any(
                roots & used for other,used in reads.items() if other!=oid):
            if all(value_type(c,lookup)=='bool' for c in cells) and not any(roots & used for used in reads.values()):
                basis='isolated_flag_no_nongenerated_reader_in_resolved_public_bodies'
            elif all(nonfinancial(inv.backend,oid,c)=='source_bound_nonfinancial_interpretation' for c in cells):
                basis='source_bound_counter_only_no_outgoing_effect_dependence'
    if basis:
        for c in CATEGORIES[1:]:
            exclusions[c]={'necessary':'committed state change or value/availability effect','basis':basis,
                'operation':oid,'target':operation['target'],'domain':f.identity,'source':operation['source'],
                'path_ids':[r['path'] for r in rows],'decisive_residuals':[]}
    return {'operation':oid,'target':operation['target'],'possible_categories':sorted(cats),
        'quantity_dependence_uses':sorted(amount_uses),'value_control_closure':closure['id'],
        'absence_certificates':exclusions,
        'source_routes':routes,'unresolved_same_storage_calls':[c['id'] for c in delegate],
        'unread_effect_residuals':hard+opaque,'control_categories':sorted(control_categories),
        'callback_entries_have_independent_source_obligations':True}

```

## source/src/pr_next_joint/investigation/selection.py

SHA-256 `fd3702be585d8836fbbc8bdf71974750d992cd03f6685be64598e373e104567f`

```python
"""Choose a source-bound observation by its power to separate two stated interpretations.

The model supplies expected outcomes, never a witness. Storage identifiers below
are resolved only among selectors of the actual entry. This layer produces actions,
not new risk items. The legacy first-pair order is retained for engineering comparison.
"""
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, selector_relation
from .protocol import normal_alternative
from .request_scope import claim_entries, linked_controls, request_target, select_controls, unique_cells


def _named(inv, oid, selectors_, name):
    if not isinstance(name, str) or not name:
        return []
    nodes = inv.f.lookup(oid).nodes
    return list({key(cell): cell for cell in selectors_ if nodes.get(cell['root'], {}).get('name') == name
                 or inv.backend._storage_name(oid,cell)==name}.values())


def plan_observation(inv, binding, item, plan):
    from .properties import interpret, plan_property, premise_cases, source_target
    from .ledger import MEASURES
    request = interpret(item)
    if isinstance(request,dict) and request.get('measure') in set(MEASURES)|{'direct_effect','denied_qualified','missing_control','authorization_violation'}:
        plan_property(inv,binding,item,plan,request)
        return
    item = dict(item,observation=request)
    if request is None:
        return
    root = binding.get('core_operation')
    empty = {'pool': [], 'selected': None, 'status':'indeterminate'}
    plan['observation_choice'] = empty
    if not root or not isinstance(request, dict):
        empty['reason'] = 'observation_or_applied_core_not_resolved'
        return
    explanation=normal_alternative(item);empty['normal_interpretation']=explanation
    predictions={k:request[k] for k in ('risk','normal') if type(request.get(k)) is bool}
    distinct=len(predictions)==2 and predictions['risk']!=predictions['normal']
    f = inv.f
    measure = request.get('measure')
    if not isinstance(measure,str) or measure not in ('holder_grant','holder_net','opens','blocks'):
        empty.update(status='unsupported',reason='no_program_observable_for_this_semantic_question')
        return
    finding_root = root
    root, possible_uses, reason = request_target(inv, binding, item, plan, measure)
    empty['request_resolution'] = {'finding_root': finding_root, 'use': root, 'possible_uses': possible_uses,
                                   'unmeasured_uses': [u for u in possible_uses if u != root]}
    if reason:
        empty.update(status='infeasible_scope', reason=reason)
        return
    if (measure=='holder_grant' and f.options.scope!='AC') or (measure=='holder_net' and f.options.scope!='FCR'):
        empty.update(status='infeasible_scope', reason='observation_task_mismatch')
        return
    paths = [p for _,p in f.operation_paths(root,True)]
    guard_cells = [s for p in paths for s in selectors(p['guards'])]
    reads = [s for p in paths for s in selectors([p['guards'],p['writes'],p.get('sensitive_effects',[])])]
    writable=[w['path'] for p in paths for w in p['writes']]
    control_pool=guard_cells if measure=='holder_grant' else reads
    objects=_named(inv,root,writable,request.get('object')) if 'object' in request else [
        o for o in {key(s):s for s in writable}.values() if inv.backend._holder(root,o) is not None]
    controls=_named(inv,root,control_pool,request.get('control')) if 'control' in request else list(
        {key(s):s for s in guard_cells}.values())
    if root != finding_root:
        controls = select_controls(inv, root, linked_controls(inv, finding_root, root), request, item)
    elif f.options.scope == 'FCR' and measure in ('opens','blocks'):
        writers = claim_entries(inv, binding, item) - {root}
        if request.get('after'):
            writers = set(inv.catalog.resolve(request['after']))
        connected = unique_cells(c for w in writers for c in linked_controls(inv, w, root))
        controls = select_controls(inv, root, connected, request, item)
    if 'control' not in request and measure=='holder_grant':
        controls=[s for s in controls if any(n.get('kind')=='actual_sender' for n in walk(keys(s)))]
    if 'control' not in request and measure=='holder_net':
        # A requested payout-mode change may be guarded by a unique non-right state cell.
        controls=[s for s in controls if not any(selector_relation(s,o)=='same_shape' for o in objects)]
    def one_position(cells):
        return len({key(c) for c in cells})==1
    if not one_position(controls) or measure in ('holder_grant','holder_net') and not one_position(objects):
        empty.update(status='infeasible_scope',reason='control_or_right_not_bound_to_unique_source_declaration')
        return
    if measure=='holder_grant':
        # A holder key and immediate caller must occur in the tested guard itself.
        holders = [inv.backend._holder(root,o) for o in objects]
        controls = [g for g in controls if any(h and any(key(k)==key(h) for k in keys(g)) for h in holders)
                    and any(n.get('kind')=='actual_sender' for n in walk(keys(g)))]
    if measure=='holder_net':
        objects = [o for o in objects if inv.backend.net_unit(root,o)]
    if not controls or measure in ('holder_grant','holder_net') and not objects:
        empty.update(status='unsupported',reason='holder_direction_or_financial_unit_not_established')
        return
    after = request.get('after')
    after_ids = source_target(inv,after,f.operations[root]['target']) if after is not None else []
    cases,gaps=premise_cases(inv,root,item)
    if gaps:
        empty.update(status='unsupported',reason='; '.join(gaps));return
    if after is not None and (len(after_ids)!=1 or f.operations[after_ids[0]]['target']!=f.operations[root]['target']):
        empty.update(status='infeasible_scope',reason='intervention_target_ambiguous_or_different')
        return
    graph_pairs = plan['selected_pairs'] + plan['deferred_pairs']
    writers = list(dict.fromkeys(p['change'] for p in graph_pairs if p['observe']==root))
    target=f.operations[root]['target']
    hint=item.get('next_check');hint=hint if isinstance(hint,dict) else {}
    explicit=inv.catalog.resolve(hint.get('change')) if hint.get('action')=='compare' and inv.catalog.resolve(hint.get('observe'))==[root] else []
    # A real explicit prior probe remains in the shared pool even when it tests a different control.
    if len(explicit)==1 and f.operations[explicit[0]]['target']==target:
        writers=list(dict.fromkeys(explicit+writers))
    for control in controls:
        for writer in sorted(inv.graph.access[(target,control['root'])]['writers']):
            if writer!=root and writer not in writers:
                writers.append(writer)
    if root != finding_root:
        writers = [finding_root]
    elif f.options.scope == 'FCR' and measure in ('opens','blocks'):
        allowed = claim_entries(inv, binding, item) - {root}
        if after_ids:
            allowed = set(after_ids)
        writers = [w for w in writers if w in allowed]
    delta = None
    if f.options.scope == 'FCR' and measure in ('opens','blocks'):
        deltas = inv.backend._holder_deltas(root)
        if request.get('object'):
            deltas = [row for row in deltas if any(key(o)==key(row[0]) for o in objects)]
        if len(deltas)!=1:
            empty.update(status='unsupported', reason='holder_position_or_ledger_direction_not_unique; ordinary source use preserved')
            return
        cell, holder, direction = deltas[0]
        delta = {'cell':cell,'holder':holder,'direction':direction}
        objects = [cell]
    if after_ids == [root] and finding_root == root and linked_controls(inv,root,root) and root not in writers:
        writers.append(root)
    pool = empty['pool']
    for writer in writers[:f.options.max_actions]:
        ws=[w['raw']['path'] for w in f.writes.values() if w['operation']==writer]
        matching=[c for c in controls if any(selector_relation(c,w)=='same_shape' and
                  not inv.graph._disjoint_keys(c,w) for w in ws)]
        if measure=='holder_grant':
            # In the same-requester experiment a caller writing their own holder slot
            # cannot install a grant in another holder's slot, even when roots coincide.
            def possible_other_holder(g):
                pos={i for i,k in enumerate(keys(g)) if any(key(k)==key(inv.backend._holder(root,o)) for o in objects)}
                return any(selector_relation(w,g)=='same_shape' and not inv.graph._disjoint_keys(w,g)
                           and all(keys(w)[i].get('kind')!='actual_sender' for i in pos) for w in ws)
            matching=[c for c in matching if possible_other_holder(c)]
        candidates = list(dict.fromkeys(['availability',measure]))
        for kind in candidates:
            context=inv._compare_context({'current':item},writer,root)
            # Generic commit probes have no measured entitlement delta.
            state='indeterminate'
            if after_ids and writer!=after_ids[0] or not matching:
                state='infeasible_scope'
            elif kind==measure:
                state='distinguishing' if distinct else 'shared_technical_fact'
            elif measure=='holder_net':
                # Knowing only that a call commits is compatible with both a full and a short payout.
                state='same_expected_observation'
            if kind!='availability':
                context['premise_cases']=cases
                context['observable']={'measure':kind,'control_selectors':matching,'objects':objects}
                if f.options.scope == 'FCR' and measure in ('opens','blocks'):
                    from .properties import privileged_paths
                    context['observable']['qualified_writer_paths']=privileged_paths(inv,writer)
                    companion = [s for s in linked_controls(inv,writer,root) if s['root'] not in {v['root'] for v in matching}]
                    context['observable'].update(hold_other_request_cells=True,holder_delta=delta,
                                                 other_intervention_inputs=companion)
                if kind=='holder_grant':
                    context['caller_modes']=['same_requester']
            pool.append({'action':'compare','change':writer,'observe':root,'measure':kind,'status':state,
                         'expectations':predictions if distinct and kind==measure else {},
                         'scope':{'target':target,'controls':matching,'objects':objects, 'finding_root':finding_root,
                                   'use':root,'intervention':writer, 'measure':kind, 'holder_delta':delta,
                                   'extent':'one source-bound request; other routes and amounts not certified'},
                         'context':context,
                         'cached':inv.backend.reusable('compare',{'change':writer,'observe':root,'context':context})})
    chosen = [p for p in pool if p['status'] in ('distinguishing','shared_technical_fact')]
    if chosen:
        pick=min(chosen,key=lambda p:(not p['cached'],writers.index(p['change'])))
        empty.update(selected=pick,status=pick['status'],reason='distinct explicit predictions' if distinct else 'grounded common fact; normative alternatives remain open')
    else:
        empty.update(status='infeasible_scope',
                     reason='no scoped test with differing explicit predictions')
    legacy=next((p for p in pool if p['measure']=='availability' and (not explicit or explicit==[p['change']])),None)
    empty['prior_candidate']=legacy
    empty['legacy_graph_first']=plan['selected_pairs']
    if empty['selected']:
        pick=empty['selected']
        plan['selected_pairs']=[{'change':pick['change'],'observe':root,
                                 'source_reason':'same scope and conflicting predicted observation'}]
        plan['deferred_pairs']=[p for p in graph_pairs if (p['change'],p['observe'])!=(pick['change'],root)]
    inv.graph.events.append({'action':'disagreement_selection','operation':root,'question':plan['question'],
                             'status':empty['status'],'selected':None if not chosen else [pick['change'],root,pick['measure']],
                             'pool_size':len(pool),'old_explicit_or_graph_pair':None if legacy is None else [legacy['change'],root]})
    empty['unexamined_writer_count']=max(0,len(writers)-f.options.max_actions)

```

## source/src/pr_next_joint/investigation/semantic_audit_card.py

SHA-256 `bb9b3fb11b03055bf5f8d49699dc664d9f2c5c9a688de1396b05f6203c85d95f`

```python
"""Validate a bounded model hypothesis and delegate to the ordinary issue consumer."""
from pr_next_joint.core import digest

KINDS = frozenset(("new_sink", "untrusted_sensitive_flow", "role_write_to_use", "authorization_scope",
                   "holder_consent_scope", "financial_unit", "gross_vs_net", "lifecycle_stage",
                   "ordinary_transfer_route", "privileged_state_difference", "potential_normal_counterexample", "unknown"))
CHECKS = frozenset(("actual_call_reachability", "untrusted_flow", "guard_scope", "role_write_to_use",
                    "allowance_scope", "same_unit_net_effect", "control_change_vs_outgoing",
                    "rollback_or_external_dep", "none"))
TEXT = {"effect_ref":180, "actor_holder_relation":240, "risk_explanation":360,
        "normal_alternative":360, "decisive_missing_fact":240}
FIELDS = set(TEXT) | {"issue_kind", "source_refs", "check_kind", "requested_target_ref"}


def parse(card):
    if isinstance(card, dict) and set(card) == {'withdraw','effect_ref','reason'}:
        if all(isinstance(card[k],str) and 0 < len(card[k].strip()) <= limit
               for k, limit in [('withdraw',80),('effect_ref',180),('reason',240)]):
            return None
        return 'invalid_audit_withdrawal'
    if not isinstance(card, dict) or set(card) != FIELDS:
        return "audit_card_fields"
    if any(not isinstance(card[k], str) or len(card[k]) > n for k, n in TEXT.items()):
        return "audit_card_text"
    for k, choices in (("issue_kind", KINDS), ("check_kind", CHECKS)):
        if not isinstance(card[k], str) or card[k] not in choices:
            return "audit_card_" + k
    refs = card['source_refs']
    if not isinstance(refs, list) or not 1 <= len(refs) <= 6 or not all(isinstance(r, str) and 0 < len(r.strip()) <= 180 for r in refs):
        return "audit_card_source_refs"
    target = card['requested_target_ref']
    if target is not None and (not isinstance(target, str) or not 0 < len(target.strip()) <= 180):
        return "audit_card_check_target"
    if not card['effect_ref'].strip() or not (card['risk_explanation'].strip() or card['normal_alternative'].strip()):
        return "audit_card_empty_claim"
    return None


def bind(inv, card, manifest):
    rules = inv.semantics.rules
    effect = rules.bind(card['effect_ref'], manifest, 'effect')
    if not effect:
        return None, 'audit_effect_unbound'
    d = rules.effects[effect]
    oid = d['oid']
    shown = set(manifest.get('expanded_operations', ())) - set(manifest.get('partially_expanded_operations', ()))
    def source(ref):
        handle = rules.bind(ref, manifest)
        if handle:
            record = rules.effects.get(handle) or rules.objects[handle]
            if record['target'] == d['target']:
                return (handle, record.get('oid'))
            return None
        found = inv.catalog.resolve(ref)
        if len(found) == 1 and found[0] in shown and inv.f.operations[found[0]]['target'] == d['target']:
            return (None, found[0])
        return None

    refs = [source(ref) for ref in card['source_refs']]
    if not all(refs) or not any(handle == effect or op == oid for handle, op in refs):
        return None, 'audit_source_scope_mismatch'
    requested = source(card['requested_target_ref']) if card['requested_target_ref'] else (effect, oid)
    if not requested or not requested[1]:
        return None, 'audit_check_target_unbound'
    peer = requested[1]
    check = card['check_kind']
    name = inv.catalog.name(oid)
    hint = {}
    if check in ('role_write_to_use', 'same_unit_net_effect', 'allowance_scope', 'control_change_vs_outgoing'):
        hint = dict(action='compare', change=name, observe=inv.catalog.name(peer))
    elif check != 'none':
        hint = dict(action='inspect', function=inv.catalog.name(peer))
    claim = card['risk_explanation'] or card['normal_alternative']
    # This is a proposed conflict, consumed with the applied policy and guards below.
    # A location/check by itself has no predicted polarity.
    normative = card['issue_kind'] in ('authorization_scope', 'holder_consent_scope', 'lifecycle_stage')
    assessment = 'risk' if normative and card['actor_holder_relation'].strip() and card['risk_explanation'].strip() else 'investigate'
    row = dict(id='audit_'+digest([effect, card['issue_kind']])[:18], anchors=[name], effect=card['effect_ref'],
               assessment=assessment, claim=claim, policy_basis=card['actor_holder_relation'],
               normal_explanation=card['normal_alternative'], distinguishing_question=card['decisive_missing_fact'],
               next_check=hint, category='AC' if inv.f.options.scope=='AC' else None,
               _audit_check=check, _audit_kind=card['issue_kind'])
    return row, None

```

## source/src/pr_next_joint/investigation/semantic_claims.py

SHA-256 `da974255a59bd894c809094d3a0d375a7d5ac3c8fed4b4f7126e33e4e3dc883b`

```python
"""Small, polarity-preserving interpretation of source-bound semantic proposals.

This layer does not infer asset meaning from Solidity names.  It distinguishes
an assertion from its negation/question before the existing source binder can
use it. Ambiguous free text requires a focused answer; a keyword is not proof.
"""
import re


FINANCIAL = re.compile(
    r"\b(?:tokens?|tokenized|redeemable|financial\s+(?:assets?|rights?|balances?)|"
    r"holders?['’]?s?\s+(?:balances?|rights?)|asset\s+ledger)\b|代币|可兑付|金融资产|资产权益", re.I)
COUNTER = re.compile(
    r"\b(?:non[- ]?financial(?:\s+counter)?|(?:service|request|usage|event|call)\s+(?:requests?|counts?|counter|number)|"
    r"(?:counts?|records?)\s+(?:only\s+)?(?:service\s+)?requests?)\b|非金融|服务请求|普通计数|调用次数|事件次数", re.I)
UNCERTAIN = re.compile(
    r"\b(?:whether|unclear|unknown|uncertain|determine|investigate|question|might|may\s+(?:be|represent)|"
    r"could\s+(?:be|represent)|not\s+(?:yet\s+)?(?:established|determined|known|clear)|"
    r"assuming|suppos(?:e|ing)|if\s+(?:this|the\s+\w+)\s+(?:is|represents))\b|"
    r"是否|尚不|无法确定|不确定|待确定|含义未明|假设|假如|若.{0,18}(?:代表|表示|属于)", re.I)
NEGATION = re.compile(
    r"\b(?:not|never|neither|nor|no|without|non[- ]|doesn't|isn't|aren't|isnt|doesnt|cannot)\b|"
    r"(?:不|并非|不是|不属于|不表示|不代表|不涉及|无)(?:是|属于|表示|代表|涉及)?", re.I)
NEGATED_NEGATION = re.compile(r"\b(?:not\s+only|not\s+merely|not\s+just)\b|不仅|不只是", re.I)
ASSERTION = re.compile(
    r"\b(?:is|are|represent\w*|record\w*|hold\w*|store\w*|track\w*|balance|ledger|"
    r"mint\w*|issu\w*|burn\w*|destroy\w*|transfer\w*|debit\w*|credit\w*|clear\w*|"
    r"reset\w*|withdraw\w*|redeem\w*|freeze\w*|block\w*|token)\b|"
    r"表示|代表|记录|保存|持有|余额|账本|发行|增发|转账|销毁|冻结|扣减|清零|权益", re.I)
MEANING_VERB=re.compile(r'\b(?:represent\w*|denot\w*|constitut\w*|signif\w*|mean\w*|record\w*|store\w*|track\w*)\b|表示|代表|属于|构成|记录|保存',re.I)
ACTION_VERB=re.compile(r'\b(?:transfer\w*|withdraw\w*|redeem\w*|mint\w*|issu\w*|burn\w*|destroy\w*|freeze\w*|block\w*|debit\w*|credit\w*|reduce\w*|clear\w*|spend\w*)\b|转移|转账|提取|兑付|增发|销毁|冻结|扣减|清零',re.I)


def negates_meaning(prefix):
    """Negation of an operation is not negation of the object's asset meaning."""
    prefix=NEGATED_NEGATION.sub('',prefix[-140:])
    negatives=list(NEGATION.finditer(prefix))
    if not negatives:return False
    tail=prefix[negatives[-1].end():]
    semantic=list(MEANING_VERB.finditer(tail));actions=list(ACTION_VERB.finditer(tail))
    if actions and (not semantic or actions[-1].end()>semantic[-1].end()):return False
    if semantic:return True
    # Direct adjectival/copular negation; long unidentified clauses are not
    # guessed to be asset denials.
    return bool(re.fullmatch(r"\s*(?:(?:a|an|the|any|actual|really|necessarily|genuine|longer|as|be|being|of|assets?|rights?|tokens?|balances?|or|nor|and)\s+){0,8}",tail,re.I)
                or re.fullmatch(r'(?:是|属于|表示|代表|任何|真正的|实际的|一种|一个|可)?\s*',tail))


def clauses(text):
    # Contrast and punctuation delimit negation scope. A question/conditional
    # marks the full sentence, including clauses after a comma or semicolon.
    result=[]
    for sentence in re.split(r'(?<=[.!?。！？])\s*|\n+', str(text or '')):
        if not sentence.strip():continue
        uncertain=bool(UNCERTAIN.search(sentence) or '?' in sentence or '？' in sentence)
        for part in re.split(r';|；|,|，|\bbut\b|\bwhereas\b|\bhowever\b|但是|但(?:是)?|而非',sentence,flags=re.I):
            part=part.strip()
            if part:result.append((part,uncertain))
    return result


def resource_assertion(text, answer=None):
    """Return supported polarity and original spans, never a truth boolean.

    Exact short choices remain supported. Their explanation cannot expressly
    contradict the choice. Mixed/conditional claims are left unresolved.
    """
    text=str(text or '').strip();positive=[];negative=[];questions=[];counter=[];incidental=[]
    for clause,uncertain in clauses(text):
        terms=list(FINANCIAL.finditer(clause))
        counter_terms=list(COUNTER.finditer(clause))
        if uncertain and (terms or counter_terms):
            questions.append(clause);continue
        for match in counter_terms:
            if negates_meaning(clause[:match.start()]):
                continue
            counter.append(clause)
        if not terms:continue
        if uncertain:questions.append(clause);continue
        for term in terms:
            before=clause[:term.start()]
            # Denying that an action is an asset event does not assert either
            # asset ownership or nonfinancial meaning. Preserve an independent
            # explicit meaning statement instead of manufacturing a conflict
            # from the noun inside this denied event relation.
            if re.search(r'\b(?:is|are|constitutes?)\s+(?:not|never)\s+(?:an?\s+)?'
                         r'(?:destruction|transfer|issuance|minting|redemption|withdrawal|'
                         r'freezing|payment|burning)\s+of\s+(?:the\s+)?$',before,re.I):
                incidental.append({'span':clause,'term':term.group(),'relation':'denied_event_not_resource_assertion'})
                continue
            # Negation after an independent finite verb belongs to that other
            # statement. The supported language deliberately avoids guessing
            # through nested explanations and reported speech.
            window=before[-140:]
            if re.search(r"\b(?:claim\w*|alleg\w*|suggest\w*)\b.{0,35}$",window,re.I):
                questions.append(clause);continue
            neg=negates_meaning(window)
            if neg:negative.append({'span':clause,'term':term.group(),'polarity':'negative'})
            elif ASSERTION.search(clause):positive.append({'span':clause,'term':term.group(),'polarity':'positive'})
            else:questions.append(clause)
    choices={'financial_right':'financial_right','token_ledger':'financial_right',
             'redeemable_credit':'financial_right','nonfinancial_counter':'nonfinancial_counter'}
    requested=choices.get(str(answer or '').strip())
    negative_only=bool(negative or counter) and not positive
    if requested=='financial_right':
        meaning=None if negative or counter or questions else requested
    elif requested=='nonfinancial_counter':
        meaning=None if positive or questions else requested
    elif positive and not negative and not questions and not counter:
        meaning='financial_right'
    elif (negative or counter) and not positive and not questions:
        meaning='nonfinancial_counter'
    else:meaning=None
    token_positive=any(re.search(r'\btokens?\b|代币',x['term'],re.I) for x in positive)
    return {'meaning':meaning,'positive_spans':positive,'negative_spans':negative,
        'counter_spans':counter,'unresolved_spans':questions,'nonassertive_event_mentions':incidental,'requested_choice':requested,
        'unit_kind':'token' if token_positive else 'unspecified_financial',
        'polarity_preserved':True,'original_text':text,
        'status':'asserted' if meaning else 'semantic_polarity_or_scope_unresolved'}


def normal_proposal(item, explicit=None):
    if explicit and explicit.get('meaning')=='normal_authorization':
        return {'text':explicit.get('basis',''),'source':'focused_model_answer','id':explicit.get('id')}
    if item.get('assessment')!='normal':return None
    text=' '.join(str(item.get(k) or '') for k in ('claim','alternative','revision_reason','normal_basis'))
    return {'text':text,'source':'model_normal_proposal'} if text.strip() else None

```

## source/src/pr_next_joint/investigation/semantic_rules.py

SHA-256 `53cb584f631422c99928b6dcc0c24311c3a9e8766e58ddbff9e4936e148b55d6`

```python
"""Typed semantic supports over the existing source summaries. No graph edge or model label is a verdict."""
from collections import defaultdict, deque
import copy
import re
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key,walk
from pr_next_joint.frontend.storage import keys, value_type
from .summary import local_delta, holder, has_basis
from .initial_state import domain
from .key_roles import relation as key_relation
from .protocol import role_error

RESOURCE={'financial_right','nonfinancial_counter'}
CONSENT={'gross_debit_bound','net_request_with_fee'}
AUTH={'current_authority_required','holder_authorization_applies','initialization_stage'}
def loc_key(loc):
    return (loc.get('file'),loc.get('start'),loc.get('length'))
def field_node(cell):
    return next((seg['field'] for seg in reversed(cell.get('segments',())) if 'field' in seg),cell['root'])


class SupportIndex:
    """Input and derived facts share identities. Re-ground only descendants of edited roots."""
    def __init__(self, remaining):
        self.remaining=remaining
        self.roots=defaultdict(set)
        self.edges=defaultdict(set)
        self.children=defaultdict(set)
        self.live=set()
        self.pending=set()
        self.cut=False
        self.visits=0
        self.certificates={};self.proof_rules={}

    def rule(self, conclusion, inputs, rule):
        clause=(rule,tuple(sorted(set(inputs))))
        if not clause[1] or clause in self.edges[conclusion]:return
        self.edges[conclusion].add(clause)
        for fact in clause[1]:self.children[fact].add(conclusion)
        self.pending.add(conclusion)

    def update(self, fact, support, active):
        changed=(support in self.roots[fact])!=bool(active)
        if active:self.roots[fact].add(support)
        else:self.roots[fact].discard(support)
        if changed:self.pending.add(fact)

    def valid(self,fact):
        if self.roots.get(fact):return True
        certificate=self.certificates.get(fact)
        return fact in self.live and bool(certificate) and all(sid in self.roots.get(node,()) for node,sid in certificate)

    def settle(self):
        if not self.pending:return set()
        self.cut=False
        affected=set(self.pending); todo=deque(sorted(affected))
        before={node for node in affected if node in self.live}
        while todo:
            node=todo.popleft()
            for child in self.children[node]:
                if child not in affected:
                    affected.add(child);todo.append(child)
                    if child in self.live:before.add(child)
            if self.remaining()<=0:
                # A stale positive must never survive an incomplete retraction.
                self.cut=True
                return {x for x in affected if (x in before)!=self.valid(x)}
        self.live.difference_update(affected)
        ready=deque(sorted(affected))
        while ready:
            if self.remaining()<=0:
                self.cut=True;break
            node=ready.popleft();self.visits+=1
            if node in self.live:continue
            roots=self.roots.get(node)
            proof=None;used_rules=set()
            if roots:proof=frozenset(((node,min(roots)),))
            else:
                for rule,terms in sorted(self.edges.get(node,())):
                    if all(x in self.live and self.valid(x) for x in terms):
                        proof=frozenset().union(*(self.certificates[x] for x in terms))
                        used_rules={rule}.union(*(self.proof_rules.get(x,()) for x in terms))
                        break
            if proof:
                self.certificates[node]=proof;self.proof_rules[node]=used_rules;self.live.add(node)
                ready.extend(n for n in self.children[node] if n in affected and n not in self.live)
        if not self.cut:self.pending.clear()
        return before.symmetric_difference({x for x in affected if self.valid(x)})

    def basis(self, fact):
        # Already grounded provenance stays readable even at the cutoff; no rule runs here.
        if not self.valid(fact):return [],[]
        origins=set(self.roots.get(fact,()));rules=set()
        cert=self.certificates.get(fact,())
        if cert and all(sid in self.roots.get(node,()) for node,sid in cert):
            origins.update(sid for _,sid in cert);rules.update(self.proof_rules.get(fact,()))
        todo=[fact];seen=set()
        while todo and self.remaining()>0:
            n=todo.pop()
            if n in seen or not self.valid(n):continue
            seen.add(n);origins.update(self.roots[n])
            for rule,terms in self.edges[n]:
                if all(self.valid(x) for x in terms):rules.add(rule);todo.extend(terms)
        return sorted(origins),sorted(rules)


class ScopedRules:
    """Indexes refer to compiler-selected declarations and individual applied source writes."""
    def __init__(self,inv):
        self.inv=inv;self.f=inv.f;self.logic=SupportIndex(inv.program_remaining)
        self.objects={};self.effects={};self.aliases=defaultdict(set);self.used=defaultdict(set)
        self.by_decl=defaultdict(set);self.by_operation=defaultdict(set);self.routes=defaultdict(list)
        self.local_readers=defaultdict(set)
        self.supports={};self.facts={};self.by_handle=defaultdict(set)
        self.built=False;self.incomplete=set();self.declaration_lookups=set()
        self.events=[];self.history=[];self.last_changes=set();self.epoch=0

    def remaining(self):
        return self.inv.program_remaining()>0

    def obj(self,target,rid,oid=None):
        return 'o_'+digest([self.f.bundle['build_id'],target,rid,oid])[:20]

    def index(self):
        if self.built:return
        self.built=True
        from pr_next_joint.frontend.storage import selectors
        self.guard_declarations=set()
        for oid,operation in self.f.operations.items():
            if not self.remaining():self.incomplete.update(set(self.f.operations)-set(self.by_operation));break
            if operation.get('generated_getter'):continue
            target=operation['target'];lookup=self.f.lookup(oid)
            for row in self.f.summaries.rows(oid):
                if not self.remaining():self.incomplete.add(oid);break
                self.guard_declarations.update((target,c['root']) for c in selectors(row['guards']))
                self.index_observed_effects(oid,row)
                raw=self.f.paths[row['path']]['raw']
                for wi,w in enumerate(row['ordered_writes']):
                    if not self.remaining():self.incomplete.add(oid);break
                    cell=w['path'];rid=field_node(cell);loc=w['source']
                    effect='w_'+digest([self.f.bundle['build_id'],target,oid,row['path'],wi,loc,cell])[:20]
                    desc=dict(oid=oid,target=target,path=row['path'],where=loc,cell=cell,
                              version=wi,conditions=digest(row['guards']),write=w,clean=not row['residuals'])
                    self.effects[effect]=desc;self.by_operation[oid].add(effect)
                    name=lookup.nodes.get(rid,{}).get('name')
                    if not name:continue
                    obj=self._declare(target,rid,None,lookup)
                    self.by_decl[obj].add(effect)
                    fn=operation['function']
                    self._names(effect,target,fn+'#'+name)
                    sign,_=local_delta(w)
                    if sign:self._names(effect,target,fn+'#'+name+('~debit' if sign=='-' else '~credit'))
                    self._names(effect,target,fn)
                    self.aliases['effect:'+effect[2:]].add(effect)
                    self.used[obj].add(oid)
                    sign,qty=local_delta(w)
                    # Edges retain evaluated subterms; effects depending on opaque values remain open at consumption.
                    # Read provenance comes from the evaluated, substituted expression; a shared root is insufficient.
                    for kind,expr in [('value',qty if qty is not None else w['value']),('key',keys(cell)),('guard',row['guards'])]:
                        for term in walk(expr):
                            if not self.remaining():self.incomplete.add(oid);break
                            if term.get('kind') not in ('parameter','storage'):continue
                            pid=term['id'] if term['kind']=='parameter' else field_node(term)
                            source=self._declare(target,pid,oid if term['kind']=='parameter' else None,lookup)
                            self.used[source].add(oid)
                            rules=['P03'] if term['kind']=='storage' else []
                            if kind=='guard':rules.append('P05')
                            if row['guards']:rules.append('P06')
                            if kind=='value':
                                if qty is not None:rules.append('P04')
                                if any(k.get('kind')=='parameter' and k.get('id')==pid for k in walk(raw.get('copy_origins',[]))):rules.append('P01')
                                for call in raw.get('read_calls',[]):
                                    if call.get('binding') not in ('compiler_internal_declaration','compiler_bound_qualified_ancestor','compiler_bound_internal_pure_library'):continue
                                    if key(call.get('return_value'))==key(term) and any(key(a)==key(term) for a in call.get('arguments',[])):
                                        rules.append('P02')
                                        if any(key(x.get('value'))==key(term) for x in call.get('copies',[])):rules.append('P01')
                            route=(effect,kind,tuple(dict.fromkeys(rules)),key(expr)==key(term))
                            if route not in self.routes[source]:self.routes[source].append(route)


    def index_observed_effects(self,oid,row):
        """Index a compiler-located effect as an occurrence, never as an inferred write.
        Distinct branches share the source occurrence and keep their own conditions."""
        target=self.f.operations[oid]['target'];fn=self.f.operations[oid]['function']
        for term in row['effects']:
            if not self.remaining():self.incomplete.add(oid);return
            loc=term.get('source') or {};kind=term.get('kind')
            if not kind or not loc.get('file') or loc.get('start') is None:continue
            effect='e_'+digest([self.f.bundle['build_id'],target,oid,loc_key(loc),kind,
                                term.get('to') or term.get('recipient'),term.get('amount'),term.get('callpoint_guards',row['guards'])])[:20]
            d=self.effects.setdefault(effect,dict(oid=oid,target=target,where=loc,kind=kind,branches={}))
            d['branches'][row['path']]={'conditions':digest(row['guards']),'has_residuals':bool(row['residuals'])}
            self.by_operation[oid].add(effect)
            self._names(effect,target,fn);self._names(effect,target,fn+'#'+kind)

    def declaration_by_ref(self,reference):
        # Bind a uniquely named declaration in the actual applied inheritance scope on demand.
        if reference in self.declaration_lookups:return
        self.declaration_lookups.add(reference)
        for target in self.inv.catalog.targets:
            aliases=(target+'.',target.rsplit(':',1)[-1]+'.')
            name=next((reference[len(prefix):] for prefix in aliases if reference.startswith(prefix)),None)
            if not name or not re.fullmatch(r'[\w$]+',name):continue
            lookup=self.f.lookups[target]
            bases=lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
            for base in bases:
                if not self.remaining():return
                for node in lookup.nodes[base].get('nodes',()):
                    if node.get('stateVariable') and node.get('name')==name:
                        self._declare(target,node['id'],None,lookup)

    def _names(self,h,target,name):
        for t in (target,target.rsplit(':',1)[-1]):self.aliases[t+'.'+name].add(h)

    def _declare(self,target,rid,oid,lookup):
        handle=self.obj(target,rid,oid)
        if handle in self.objects:return handle
        node=lookup.nodes.get(rid,{})
        name=node.get('name','')
        self.objects[handle]=dict(target=target,decl=rid,oid=oid,where=lookup.anchor(node) if node.get('src') else {},name=name)
        if name:
            self._names(handle,target,self.f.operations[oid]['function']+'#'+name if oid else name)
        self.aliases['obj:'+handle[2:]].add(handle)
        return handle

    def visible(self,handle,manifest):
        rec=self.objects.get(handle) or self.effects.get(handle)
        if not rec:return False
        where=rec['where']
        if where.get('file') in manifest.get('complete_source_files',[]):return True
        for a in manifest.get('visible_spans',()):
            if where.get('file')==a.get('file') and a['start']<=where['start'] and where['start']+where['length']<=a['start']+a['length']:return True
        return False

    def bind(self,ref,manifest,kind=None):
        if not isinstance(ref,str):return None
        if ref.startswith(('obj:','effect:')):
            hs={manifest.get('typed_index',{}).get(ref)}
        else:
            if kind!='effect':self.declaration_by_ref(ref)
            hs=self.aliases.get(ref,set())
        if not hs and isinstance(ref,str) and not ref.startswith(('obj:','effect:','sem:')):
            # A source span may denote a declaration or a write if there is a unique applied identity.
            m=re.fullmatch(r'(.+[.]sol)@(\d+)\+(\d+)',ref)
            if m:
                at=(m[1],int(m[2]),int(m[3]))
                pool=self.objects if kind=='obj' else self.effects if kind=='effect' else {**self.objects,**self.effects}
                hs={hh for hh,r in pool.items() if loc_key(r['where'])==at}
        hs={v for v in hs if v and ((kind!='effect' and v in self.objects) or (kind!='obj' and v in self.effects)) and self.visible(v,manifest)}
        # A declaration/entry label cannot arbitrarily pick one of its writes.
        return next(iter(hs)) if len(hs)==1 else None

    def effect_focus(self,e):
        # Index actual applied occurrences, including compiler-resolved helper effects.
        d=self.effects[e]
        if 'write' not in d:
            return {'native_selfdestruct': 'termination', 'native_transfer':'funds',
                    'dangerous_external_call':'call_authority'}.get(d['kind'])
        from .summary import holder
        w=d['write'];cell=d['cell'];lookup=self.f.lookup(d['oid'])
        if holder(cell,lookup) and local_delta(w)[0]:
            row=self.f.summaries.paths[d['path']]
            if local_delta(w)[0]=='+' and not any(local_delta(v)[0]=='-' for v in row['ordered_writes']):
                return 'credit'
            return 'account_movement'
        if (d['target'],cell['root']) in self.guard_declarations:
            return 'qualification'
        return None

    def overwritten(self,e):
        d=self.effects[e]
        if 'write' not in d:return False
        later=self.f.summaries.paths[d['path']]['ordered_writes'][d['version']+1:]
        return any(key(w['path'])==key(d['cell']) for w in later)

    def occurrence(self,e):
        d=self.effects[e]
        return (d['target'],d['oid'],loc_key(d['where']),d.get('kind','write'),
                key(d.get('cell')),d.get('conditions') or (e if 'branches' in d else None),d.get('version'))

    def register_sensitive_effects(self):
        self.index()
        if not hasattr(self,'sensitive_effects'):
            from .candidates import source_duty
            self.source_duties={}
            self.sensitive_effects={}
            self.occurrences=defaultdict(list)
            for e,d in self.effects.items():
                if not self.remaining():self.incomplete.add(d['oid']);continue
                kind=self.effect_focus(e)
                if kind:
                    self.sensitive_effects[e]=kind
                    if self.f.options.scope=='AC':
                        relation=source_duty(self,e,kind)
                        if relation:self.source_duties[e]=relation
                    self.occurrences[self.occurrence(e)].append(e)
            from .shared_effect_bridge import index_authority_consumers
            self.authority_bridges = index_authority_consumers(self)
            self.bridges_at = defaultdict(set)
            for identity, link in self.authority_bridges.items():
                for endpoint in (link['writer'], link['reader']):
                    self.bridges_at[endpoint].add(identity)

    def cards_for(self,manifest,focus):
        self.register_sensitive_effects()
        focused=set(focus)
        wanted=set(manifest.get('disputed_effects',()))
        buckets=defaultdict(deque)
        def rank(e):
            d=self.effects[e]
            return (e not in wanted,d['oid'] not in focused,d['where']['start'],e)
        for e in sorted((g[0] for g in self.occurrences.values()),key=rank):
            d=self.effects[e]
            if manifest.get('mode')=='focused_evidence' and d['oid'] not in focused:continue
            if self.visible(e,manifest):buckets[(d['target'],self.sensitive_effects[e])].append(e)
        order=('qualification','funds','termination','call_authority','credit','account_movement')
        queues=[buckets[k] for k in sorted(buckets,key=lambda k:(rank(buckets[k][0])[:2],order.index(k[1]),k[0]))]
        handles=[]
        while queues:
            for q in queues:handles.append(q.popleft())
            queues=[q for q in queues if q]
        if self.f.options.scope=='FCR':
            objs=[]
            for e in handles:
                d=self.effects[e]
                if 'cell' in d and self.sensitive_effects[e] in ('credit','account_movement'):
                    h=self.obj(d['target'],field_node(d['cell']))
                    if h in self.objects and self.visible(h,manifest):objs.append(h)
            handles=list(dict.fromkeys(objs))+handles
        for oid in focus:
            for e in sorted(self.by_operation.get(oid,())):
                d=self.effects[e]
                if 'cell' in d:
                    h=self.obj(d['target'],field_node(d['cell']))
                    if h in self.objects and self.visible(h,manifest):handles.append(h)
        cards=[];index={}
        for h in dict.fromkeys(handles):
            d=self.effects.get(h) or self.objects[h]
            ref=('effect:' if h in self.effects else 'obj:')+h[2:14]
            if ref in index:ref+=h[14:]
            if h in self.effects:
                name=self.f.lookup(d['oid']).nodes[field_node(d['cell'])]['name'] if 'cell' in d else d['kind']
                card=[ref,self.inv.catalog.name(d['oid'])+'#'+name,self.sensitive_effects[h]]
                if 'write' in d:
                    direction=local_delta(d['write'])[0]
                    if direction and keys(d['cell']):
                        party=holder(d['cell'],self.f.lookup(d['oid'])) or {}
                        label='caller' if party.get('kind')=='actual_sender' else self.f.lookup(d['oid']).nodes.get(party.get('id'),{}).get('name','account')
                        card.append(('debit ' if direction=='-' else 'credit ')+label)
            else:
                name=(self.inv.catalog.name(d['oid'])+'#' if d.get('oid') else d['target'].rsplit(':',1)[-1]+'.')+d['name']
                card=[ref,name]
            cards.append(card);index[ref]=h
        return cards,index

    def issue_effect(self,item,manifest):
        """Bind a model locator to the authenticated applied occurrence for this message."""
        anchors=item.get('anchors',[])
        oid=None
        if anchors:
            bind=self.inv.catalog.bind(anchors,core=item.get('root'))
            oid=bind.get('core_operation') if bind.get('core_exact') else None
        named=item.get('effect')
        if named is not None:
            e=self.bind(named,manifest,'effect')
            if not e:return None,'unknown_or_unshown_effect'
            d=self.effects[e]
            if anchors and (oid!=d['oid'] or bind.get('unresolved') or bind.get('ambiguous')):
                return None,'explicit_effect_anchor_conflict'
            if item.get('root') and d['oid'] not in self.inv.catalog.resolve(item['root']):
                return None,'explicit_effect_root_conflict'
        else:
            if not oid:return None,None
            choices={self.occurrence(e):e for e in self.by_operation[oid] if e in self.sensitive_effects and self.visible(e,manifest)}
            if len(choices)!=1:return None,None
            e=next(iter(choices.values()));d=self.effects[e]
        matches=self.occurrences.get(self.occurrence(e),[e])
        return (d['oid'],list(matches)),None

    def scoped_issue(self,item,manifest):
        located,error=self.issue_effect(item,manifest)
        if error or not located:return item,error
        oid,effects=located
        row=dict(item,_scope_effects=effects,_opinion_message=manifest['messages_sha256'])
        if not row['anchors']:row['anchors']=[self.inv.catalog.name(oid)]
        if item.get('subject'):
            subject=self.bind(item['subject'],manifest,'obj')
            if not subject or self.objects[subject]['target']!=self.effects[effects[0]]['target']:return item,'explicit_principal_not_bound'
            row['_opinion_subject']=subject
        return row,None

    def fact(self,h,meaning,subject=None,scope=None,role=None,payment_policy=None):
        identity=[self.f.identity,h,meaning,subject,scope,role]
        if payment_policy is not None:identity.append(payment_policy)
        fid='fact_'+digest(identity)[:20]
        if fid not in self.facts:
            self.facts[fid]=dict(handle=h,meaning=meaning,subject=subject,scope=scope,role=role)
            if payment_policy is not None:self.facts[fid]['payment_policy']=payment_policy
            self.by_handle[h].add(fid)
        return fid

    def row_scope(self,field,row,manifest,previous=None):
        meaning=row.get('meaning',previous and previous['meaning'])
        if not isinstance(meaning,str):return None
        locator,kind=('on','obj') if field=='annotations' else ('effect','effect')
        h=previous['handle'] if previous else None
        if locator in row:
            named=self.bind(row[locator],manifest,kind)
            if named is None or h is not None and named!=h:return None
            h=named
        if not h:return None
        def qualifier(name):
            if name in row:return self.bind(row[name],manifest)
            return previous.get(name) if previous else None
        subject=qualifier('subject');scope=qualifier('scope')
        if any(name in row and not val for name,val in [('subject',subject),('scope',scope)]):return None
        d=self.effects.get(h) or self.objects[h]
        if any((self.effects.get(v) or self.objects[v])['target']!=d['target'] for v in (subject,scope) if v):return None
        if subject and meaning in RESOURCE|CONSENT and subject not in self.objects:return None
        if scope and scope!=h and scope not in self.by_decl.get(h,set()) and not any(e==scope for e,_,_,_ in self.routes.get(h,())):return None
        if meaning in AUTH|CONSENT|RESOURCE and subject and subject not in self.objects:return None
        if meaning in CONSENT and not list(self.quantity_scopes(h)):return None
        role=row.get('role',previous.get('role') if previous else None)
        if h in self.effects and meaning in CONSENT and subject:
            decl=self.objects[subject]['decl']
            if not all(any(t.get('id')==decl for t in walk(keys(route['grant'])[route['issuer_key']])) for route in self.quantity_scopes(h)):return None
        proposal=dict(handle=h,meaning=meaning,subject=subject,scope=scope,role=role)
        if meaning=='current_authority_required' and h in self.effects:
            cell=self.authority_cell(h,subject)
            if cell:
                from .policy_binding import payment_policy
                lookup=self.f.lookup(d['oid'])
                names={self.f.operations[d['oid']]['function'].split('(')[0]}
                if 'cell' in d:names.add(lookup.nodes.get(field_node(d['cell']),{}).get('name'))
                stated=payment_policy(row.get('basis',''),lookup.nodes[cell['root']]['name'],names)
                inherited=(previous or {}).get('payment_policy')
                if stated or inherited:proposal['payment_policy']=stated or inherited
        return proposal

    def quantity_scopes(self,e):
        d=self.effects.get(e)
        if not d or 'write' not in d:return
        for a in self.f.summaries.dependencies.amounts_for(d['oid']):
            if a['path']!=d['path']:continue
            for dec in a['deltas']:
                if dec['sign']!='-' or dec['write_index']!=d['version'] or dec.get('key_role')=='authorization_quantity':continue
                for gate in a['allowance_gates']:
                    grant=gate['grant'];issuer=keys(grant)[gate['issuer_key']]
                    if key(issuer)!=key(dec.get('holder')):continue
                    yield {'path':a['path'],'grant':grant,'issuer_key':gate['issuer_key'],'spender_key':gate['spender_key'],
                           'debit_expression':dec['amount_expression'],'checked_quantity_expression':gate['quantity_expression'],'ledger':dec['cell']}

    def register(self,fid,sid,origin,field):
        if sid in self.supports and (self.supports[sid]['active'] or self.supports[sid].get('withdrawn')):return False
        self.supports[sid]=dict(fact=fid,origin=origin,field=field,active=True,version=1+self.supports.get(sid,{}).get('version',0))
        self.logic.update(fid,sid,True)
        return True

    @staticmethod
    def revision_reason(row,proposed):
        """Location is authenticated separately. Discard output instructions and bare labels,
        leaving the model's own semantic explanation (in any source vocabulary)."""
        reason=row.get('basis','')
        if not has_basis(reason):return False
        clauses=re.split(r'[.;!?。；！？\n]+|\b(?:because|since)\b|因为|由于',reason,flags=re.I)
        directive=r'^(?:(?:please|just|kindly|we should|you should)\s+)*(?:remove|withdraw|cancel|drop|suppress|change|relabel|mark|classify|report|delete|downgrade|upgrade|dismiss|ignore)\b'
        for clause in clauses:
            clause=clause.strip()
            if not clause or re.match(directive,clause,re.I) or re.match(r'^(?:请|应当|应该|仅需|只要)*(?:撤回|删除|取消|改为|标记|移除|忽略)',clause):continue
            words=re.findall(r'[^\W_]+',clause.casefold())
            meta={'the','this','is','a','an','of','as','only','it','should','be','alarm','warning','finding','risk','safe','not','false','positive','wrong','correct','label','incorrect','unsupported'}
            meta.update(re.findall(r'[^\W_]+',proposed['meaning']))
            supplied={word for word in words if word not in meta}
            if len(supplied)>=2 or re.search(r'[\u3400-\u9fff]{4,}',clause):return True
        return False

    def hard_unit_conflict(self,proposal):
        if proposal['meaning']!='nonfinancial_counter':return False
        from .ledger import _unit_origin
        h=proposal['handle']
        candidates=self.by_decl.get(h,set())|{e for e,k,_,exact in self.routes.get(h,()) if k=='value' and exact}
        for e in candidates:
            if not self.remaining():return 'semantic_budget'
            if proposal['scope'] and proposal['scope']!=e:continue
            d=self.effects[e]
            if proposal['subject']:
                declared=self.objects[proposal['subject']]['decl']
                if not any(t.get('id')==declared for t in walk(keys(d['cell']))):continue
            if d['clean'] and holder(d['cell'],self.f.lookup(d['oid'])) and _unit_origin(self.inv.backend,d['oid'],d['cell']):return 'scoped_source_unit_conflict'
        return False

    def apply(self,value,manifest,revision=False):
        """Stage unrelated updates separately; an ambiguous alias can never displace a valid support."""
        rows=[(field,r) for field in ('annotations','policies') for r in value.get(field,())]
        requests=defaultdict(list)
        for field,row in rows:
            identity=row.get('ref') or row.get('id')
            if isinstance(identity,str):requests[identity].append((field,row))
        conflicting={k for k,items in requests.items() if len({digest(x) for x in items})>1}
        accepted=[];rejected=[];changed=set();row_results=[];self.submission=manifest.get('messages_sha256')
        errors_with_rows=[]
        ordinals=defaultdict(int)
        for field,row in rows:
            pos=ordinals[field];ordinals[field]+=1
            wire_positions=value.get('row_positions',{}).get(field,())
            pos=wire_positions[pos] if pos<len(wire_positions) else pos
            outcome={'field':field,'index':pos,'ref':row.get('ref'),'accepted':False}
            row_results.append(outcome)
            def committed(support, fact):
                accepted.append(support)
                outcome.update(accepted=True,support=support,fact=fact)
            def reject(reason,detail=None):
                rejected.append(reason)
                errors_with_rows.append({'reason':reason,'stage':'focused_revision' if revision else (self.inv.session.attempts[-1]['phase'] if self.inv.session.attempts else 'initial'),'list':field,'index':pos,'field':'ref' if row.get('ref') else 'effect' if field=='policies' else 'on','subreason':'source_binding',**(detail or {})})
            if not self.remaining():reject('semantic_budget');break
            ref=row.get('ref');name=ref or row.get('id')
            if name is not None and (not isinstance(name,str) or name in conflicting):reject('ambiguous_seed_id');continue
            old=None;sid=None;action=row.get('action','add')
            current=None
            if ref:
                wire=manifest.get('shown_supports',{}).get(ref,{})
                sid=wire.get('support');old=self.supports.get(sid)
                if not revision or not old or not old['active'] or old['origin'] not in ('fixture','verified_service') or old['version']!=wire.get('version') or old['fact']!=wire.get('fact'):
                    reject('stale_or_undisplayed_support');continue
                if field!=old['field'] or field!=wire.get('field'):
                    reject('wrong_semantic_facet');continue
                current=self.facts[old['fact']]
                locator,kind=('on','obj') if field=='annotations' else ('effect','effect')
                if locator in row and self.bind(row[locator],manifest,kind)!=current['handle']:
                    reject('revision_object_mismatch');continue
            issue=role_error(row,row.get('meaning',(current or {}).get('meaning')),(current or {}).get('role'))
            if issue:
                actual=row.get('role')
                reject('invalid_semantic_row',{'field':'role','subreason':issue,'actual_type':type(actual).__name__,
                    'value_length':len(actual) if isinstance(actual,str) else None,'value_sha256':digest(actual)})
                continue
            if row.get('meaning',(current or {}).get('meaning'))=='initialization_stage' and 'subject' not in row and not (current or {}).get('subject'):
                reject('invalid_semantic_row',{'field':'subject','subreason':'field_absent','actual_type':'NoneType'})
                continue
            proposed=self.row_scope(field,row,manifest,current)
            if not proposed:
                reject('unbound_or_inapplicable_seed');continue
            if current:
                if action in ('confirm','withdraw') and proposed!=current:
                    reject('revision_conflicts_with_displayed_support');continue
                if action=='confirm':
                    committed(sid,old['fact']);continue
                if action=='narrow':
                    if current['scope'] or proposed['scope'] not in self.effects or proposed['scope']==current['handle'] or any(proposed[k]!=current[k] for k in ('meaning','subject','role')):
                        reject('scope_not_strictly_narrower');continue
                elif proposed['scope']!=current['scope']:
                    reject('scope_change_requires_narrow');continue
                if not self.revision_reason(row,proposed):
                    reject('revision_without_scoped_reason');continue
                if action=='correct':
                    conflict=self.hard_unit_conflict(proposed)
                    if conflict:
                        reject(conflict);continue
            fid=None if action=='withdraw' else self.fact(proposed['handle'],proposed['meaning'],proposed['subject'],
                proposed['scope'],proposed['role'],proposed.get('payment_policy'))
            if old:
                if fid==old['fact']:committed(sid,fid);continue
                self.history.append({'action':action,'support':sid,'before':old['fact'],'after':fid,'from_version':old['version'],'to_version':old['version']+1})
                self.logic.update(old['fact'],sid,False);changed.add(old['fact'])
                old.update(active=False,withdrawn=True,version=old['version']+1)
            if fid:
                sid=sid or 'support_'+digest([value['origin'],manifest.get('messages_sha256'),fid])[:20]
                if old:
                    old.update(active=True,withdrawn=False,fact=fid);self.logic.update(fid,sid,True)
                else:self.register(fid,sid,value['origin'],field)
                self.derive(fid);changed.add(fid)
            committed(sid,fid or old['fact'])
        value['semantic_binding_events']=row_results
        live_delta=self.logic.settle()
        self.last_changes={self.facts[f]['handle'] for f in live_delta if f in self.facts}
        self.epoch+=bool(live_delta)
        for fid in changed:self.events.append({'fact':fid,'active':self.logic.valid(fid),'sources':len(self.logic.roots[fid])})
        value['binding_diagnostics']=errors_with_rows
        return accepted,rejected

    def derive(self,fid):
        queue=deque([fid]);visited=set()
        while queue and self.remaining():
            source=queue.popleft()
            if source in visited:continue
            visited.add(source)
            queue.extend(self._derive_one(source))
        for source in queue:self.incomplete.update(self.related_ops(self.facts[source]['handle']))

    def _derive_one(self,fid):
        src=self.facts[fid];h=src['handle']
        if h not in self.objects:return
        meaning=src['meaning']; role=src['role']
        if meaning in ('unknown','other_source_meaning','other_source_policy'):return
        for e,k,rules,exact in self.routes.get(h,()):
            if not self.remaining():self.incomplete.add(self.effects[e]['oid']);break
            if not self.effects[e]['clean']:continue
            if src['subject'] and src['subject']!=h:
                # A bound subject is never generalized to an entire mapping family.
                ref=self.objects.get(src['subject'],{})
                relevant=keys(self.effects[e]['cell'])
                if not any(t.get('id')==ref.get('decl') for t in walk(relevant) if 'id' in t):continue
            if src['scope'] and e!=src['scope']:continue
            if meaning=='transfer_condition' and k!='guard':continue
            if meaning in RESOURCE|{'fee_rule','price','amount_role'} and k!='value':continue
            if meaning in RESOURCE and (not exact or h in self.objects and self.objects[h]['oid'] is None):continue
            if meaning in {'management_role','eligibility_state'} and k not in ('guard','value','key'):continue
            if meaning=='authorization_quantity' and k!='guard':continue
            if meaning not in RESOURCE|{'fee_rule','price','amount_role','transfer_condition','authorization_quantity','management_role','eligibility_state'}:continue
            dest=self.fact(e,meaning,src['subject'],e,role)
            pre=fid
            # Intermediate facts carry the exact applied path. They are never global node labels.
            for rule in rules:
                link='der_'+digest([fid,e,k,rule,pre])[:20]
                self.logic.rule(link,[pre],rule);pre=link
            # The semantic interpretation and the committing source expression are independent premises.
            observed='sourcefact_'+digest([e,k,self.effects[e]['conditions'],self.effects[e]['version']])[:20]
            self.logic.update(observed,'source_'+observed[11:],True)
            self.logic.rule(dest,[pre,observed],{'key':'P03','value':'P04','guard':'P05'}[k])
            if k=='value' and exact and not src['scope'] and not src['subject']:
                following=self.index_transfer(h,e,fid,pre,'P07')
                if following:yield following

    def for_effect(self,e):
        d=self.effects[e]
        if 'cell' not in d:
            return sorted(fid for fid in self.by_handle[e] if self.logic.valid(fid) and self.facts[fid]['scope'] in (None,e))
        obj=self.obj(d['target'],field_node(d['cell']))
        def applicable(fid):
            f=self.facts[fid]
            if f['scope'] not in (None,e):return False
            if f['handle']==e:return True
            if f['subject']:
                ident=self.objects.get(f['subject'],{}).get('decl')
                if not any(t.get('id')==ident for t in walk(keys(d['cell'])) if 'id' in t):return False
            return True
        return sorted(f for f in self.by_handle[e]|self.by_handle[obj] if self.logic.valid(f) and applicable(f))

    def resource(self,oid,cell):
        """A source-level family reading or an exact, uniform reading of the committing writes."""
        target=self.f.operations[oid]['target'];obj=self.obj(target,field_node(cell))
        roots=[f for f in self.by_handle.get(obj,()) if self.logic.valid(f) and self.facts[f]['meaning'] in RESOURCE and not self.facts[f]['scope'] and not self.facts[f]['subject']]
        es=[e for e in self.by_operation.get(oid,()) if 'cell' in self.effects[e] and key(self.effects[e]['cell'])==key(cell)]
        local=[]
        for e in es:
            rows=[f for f in self.for_effect(e) if self.facts[f]['meaning'] in RESOURCE]
            if not rows:local=[];break
            local.extend(rows)
        effective=roots+local
        meanings={self.facts[f]['meaning'] for f in effective}
        if len(meanings)!=1:return None
        return {'meaning':meanings.pop(),'id':digest(sorted(set(effective))),'target':target,'operation':oid,
                'family':key(cell),'source':'scoped_semantic_support','business_policy_formally_proved':False}

    def managed_resource(self,oid,cell):
        obj=self.obj(self.f.operations[oid]['target'],field_node(cell))
        return any(self.facts[f]['meaning'] in RESOURCE for f in self.by_handle.get(obj,()) if not self.facts[f]['subject'] and not self.facts[f]['scope'])

    def support_inputs(self,effects):
        """All active source supports feeding these actual effects, including equivalent independent roots."""
        todo=[f for e in effects for f in self.for_effect(e)]
        seen=set();sids=set()
        while todo and self.remaining():
            fid=todo.pop()
            if fid in seen:continue
            seen.add(fid);sids.update(self.logic.roots.get(fid,()))
            for _,premises in self.logic.edges.get(fid,()):
                if all(self.logic.valid(pr) for pr in premises):todo.extend(premises)
        return sids

    def signature(self,oid):
        return sorted({f for e in self.by_operation.get(oid,()) for f in self.for_effect(e)})

    def public(self):
        return {'source_effect_readings':[{'effect':e,'kind':k,'operation':self.effects[e]['oid'],
                 'where':self.effects[e]['where'],'stage':'constructor' if self.f.lookup(self.effects[e]['oid']).function(self.f.operations[self.effects[e]['oid']]['function']).get('kind')=='constructor' else 'applied_entry',
                 'shown_followup':e in (self.inv.context.last_manifest or {}).get('displayed_effect_handles',()) and (self.inv.context.last_manifest or {}).get('mode')=='focused_evidence',
                 'source_duty':getattr(self,'source_duties',{}).get(e,{}).get('duty'),
                 'source_support_location':getattr(self,'source_duties',{}).get(e,{}).get('support'),
                 'opinion_consumers':sorted(getattr(self,'local_readers',{}).get(e,())),
                 'shown':e in (self.inv.initial_manifest or {}).get('displayed_effect_handles',()),
                 'bound_facts':sorted(self.for_effect(e)),
                 'scoped_consumers':sorted(getattr(self,'effect_consumers',{}).get(e,()))}
                 for e,k in getattr(self,'sensitive_effects',{}).items()],
                'retired_supports':[{'support':sid,'fact':s['fact'],'field':s['field'],'version':s['version']} for sid,s in self.supports.items() if not s['active']], 'active_supports':[{'support':sid,'fact':row['fact'],'origin':row['origin'],'field':row['field'],'version':row['version']} for sid,row in sorted(self.supports.items()) if row['active']],
                'updates':list(self.events),'revisions':list(self.history),
                'referenced_abstract_effects':[{'effect':h,'operation':self.effects[h]['oid'],'target':self.effects[h]['target'],
                         'kind':self.effects[h]['kind'],'location':self.effects[h]['where'],'committing_branches':len(self.effects[h]['branches']),
                         'dependent_residual':any(b['has_residuals'] for b in self.effects[h]['branches'].values())}
                    for h in sorted({f['handle'] for f in self.facts.values() if f['handle'] in self.effects and 'kind' in self.effects[f['handle']]})],
                'facts':[{'id':fid,'object_or_effect':f['handle'],'meaning':f['meaning'],'role':f['role'],
                          'subject':f['subject'],'scope':f['scope'],'grounded':self.logic.valid(fid)}
                         for fid,f in sorted(self.facts.items())],
                'rule_visits':self.logic.visits,'budget_cut':self.logic.cut,
                'unfinished_operations':sorted(self.incomplete)}

    def related_ops(self, h):
        if h in self.effects:return {self.effects[h]['oid']}
        return set(self.used.get(h,()))

    def focused_consent(self,row):
        """A displayed quantity answer joins the same support as a seed on that debit."""
        origin=getattr(self,'input_origin',None);submission=getattr(self,'submission',None)
        if origin not in ('fixture','verified_service') or not submission or row['meaning'] not in CONSENT:return
        if row['scope'].get('phase') or row['scope'].get('assumptions'):return
        applicable={key(route) for route in row['quantity_scope']};facts=set()
        for e in self.by_operation.get(row['operation'],()):
            if not self.remaining():self.incomplete.add(row['operation']);break
            known={key(route) for route in self.quantity_scopes(e)}
            if not known or not known<=applicable:continue
            fid=self.fact(e,row['meaning'])
            sid='support_'+digest([origin,submission,fid])[:20]
            self.register(fid,sid,origin,'policies');facts.add(fid)
        if facts:
            row['fact_ids']=sorted(facts)
            delta=self.logic.settle()
            self.epoch+=bool(delta)

    def financial_consent(self,oid,route):
        found=set()
        for e in self.by_operation.get(oid,()):
            if self.effects[e].get('path')!=route['path'] or key(self.effects[e]['cell'])!=key(route['ledger']):continue
            for f in self.for_effect(e):
                if self.facts[f]['meaning'] in CONSENT and any(key(s)==key(route) for s in self.quantity_scopes(e)):
                    found.add(f)
        if not found:return None
        modes={self.facts[f]['meaning'] for f in found}
        return {'id':'consent_'+digest(sorted(found))[:20],'meaning':next(iter(modes)) if len(modes)==1 else 'unknown',
                'target':self.f.operations[oid]['target'],'operation':oid,'family':key(route['ledger']),
                'quantity_scope':[route],'scope':{},'source':'scoped_supports','fact_ids':sorted(found)}

    def consumers_for(self,h):
        """Instantiate only operations with a matching source effect, then let compile_property select categories."""
        f=self.f
        effects={h} if h in self.effects else set(self.by_decl.get(h,()))|{t[0] for t in self.routes.get(h,())}
        result=defaultdict(set)
        for e in effects:
            if not self.remaining():self.incomplete.add(self.effects[e]['oid']);break
            d=self.effects[e];oid=d['oid'];facts=self.for_effect(e)
            for fact in facts:
                seed=self.facts[fact];meaning=seed['meaning']
                if f.options.scope=='AC':
                    if meaning in AUTH|{'management_role','eligibility_state','authorization_quantity','other_source_policy','unknown'}:result[(oid,'AC')].add(e)
                    continue
                if meaning in CONSENT:
                    # Intervening controls are structural candidates; the financial consumer still tests the actual effect.
                    for x in f.summaries.dependencies.amounts_for(oid):
                        if x['path']!=d['path']:continue
                        for delta in x['deltas']:
                            if key(delta['cell'])!=key(d['cell']):continue
                            for gate in x['allowance_gates']:
                                for woid in self.writers_for_amount(oid,gate['quantity_expression']):
                                    result[(woid,None)].add(e)
                    continue
                if meaning in RESOURCE|{'price','fee_rule','amount_role','transfer_condition','authorization_quantity','management_role','eligibility_state','unknown','other_source_meaning'}:
                    if meaning=='transfer_condition':
                        for writer in self.by_decl.get(h,()):
                            result[(self.effects[writer]['oid'],None)].add(writer)
                    else:result[(oid,None)].add(e)
        return result

    def writers_for_amount(self,oid,expr):
        dep=self.f.summaries.dependencies
        term=dep.expressions.get(expr,{})
        target=self.f.operations[oid]['target']
        for t in walk(term):
            if t.get('kind')!='storage':continue
            for e in self.by_decl.get(self.obj(target,field_node(t)),()):
                if not self.remaining():return
                wid=self.effects[e]['oid']
                if wid!=oid:yield wid

    def inspect_untyped_amount(self,locator,manifest):
        """Only carry the located value use, never the rejected model meaning."""
        if self.f.options.scope!='FCR':return
        handle=self.bind(locator,manifest,'obj')
        if not handle:return
        by_entry=defaultdict(set)
        for eid,kind,_,exact in self.routes.get(handle,()):
            if not self.remaining():return
            if kind!='value' or not exact:continue
            d=self.effects[eid]
            if 'write' not in d or not d['clean']:continue
            oid=d['oid']
            dependencies=self.f.summaries.dependencies.forward(oid)['uses']
            if any('value' in kinds and self.f.summaries.positions(use) for use,kinds in dependencies.items()):
                by_entry[oid].add(eid)
        for oid,effects in by_entry.items():
            if any(self.inv.root(q)==oid and effects<=self.route_scopes(q) and
                   set((q.get('property') or {}).get('possible_categories',()))=={(q.get('property') or {}).get('category')}
                   for q in self.inv.issues.values()):
                continue
            qid='scope_'+digest([self.f.identity,oid,None,sorted(effects)])[:20]
            if qid in self.inv.issues:continue
            question=self.create_consumer(oid,None,effects)
            if question:question['source_only_amount_read']=True

    def seed_consumers(self,changed):
        relevant=defaultdict(set)
        for h in changed:
            for dest,es in self.consumers_for(h).items():relevant[dest].update(es)
        for (oid,category),es in sorted(relevant.items(),key=lambda r:str(r[0])):
            question=self.create_consumer(oid,category,es)
            if question:question.pop('source_only_amount_read',None)

    def create_consumer(self,oid,cat,effects):
        inv=self.inv
        qid='scope_'+digest([self.f.identity,oid,cat,sorted(effects)])[:20]
        if qid in inv.issues:return inv.issues[qid]
        item={'id':qid,'anchors':[inv.catalog.name(oid)],'assessment':'investigate','category':cat,
              'claim':'Review the applicable source effect and bound meaning.',
              '_scope_effects':sorted(effects),'_host_source_question':True,'_semantic_consumer':True}
        inv.accept({'issues':[item],'answers':[],'reviewed':[],'diagnostics':[],'usable_analysis':False},host_target=self.f.operations[oid]['target'])
        consumer=inv.issues.get(qid)
        if consumer:
            if not hasattr(self,'effect_consumers'):self.effect_consumers=defaultdict(set)
            for e in effects:self.effect_consumers[e].add(qid)
        return consumer

    def wire_name(self,h,manifest):
        if not self.visible(h,manifest):return None
        entry=self.effects.get(h) or self.objects[h]
        if h in self.effects:
            if 'cell' in entry:
                name=self.f.lookup(entry['oid']).nodes[field_node(entry['cell'])]['name']
                candidate=self.inv.catalog.name(entry['oid'])+'#'+name
            else:candidate=self.inv.catalog.name(entry['oid'])+'#'+entry['kind']
        elif entry.get('oid'):
            candidate=self.inv.catalog.name(entry['oid'])+'#'+entry['name']
        else:candidate=entry['target'].rsplit(':',1)[-1]+'.'+entry['name']
        if self.bind(candidate,manifest)==h:return candidate
        direct=next((r for r,k in manifest.get('typed_index',{}).items() if k==h),None)
        if direct:return direct
        loc=entry['where']
        span=f"{loc['file']}@{loc['start']}+{loc['length']}"
        return span if self.bind(span,manifest)==h else None

    def labels_for(self,oid,manifest):
        result={}
        for sid,s in self.supports.items():
            if not s['active'] or s['origin'] not in ('fixture','verified_service'):continue
            fact=self.facts[s['fact']];h=fact['handle']
            if oid not in self.related_ops(h) and not any(self.effects[e]['oid']==oid for e in self.by_decl.get(h,())):continue
            name=self.wire_name(h,manifest)
            if not name:continue
            tag='sem:'+sid.split('_')[-1][:12]
            qualifiers={}
            for k in ('scope','subject'):
                qualifier=fact.get(k)
                if qualifier:qualifiers[k]=self.wire_name(qualifier,manifest)
            if any(v is None for v in qualifiers.values()):continue
            result[tag]={'source':name,'support':sid,'version':s['version'],'fact':s['fact'],
                         'field':s['field'],'meaning':fact['meaning'],**qualifiers}
            if fact['role']:result[tag]['role']=fact['role']
            if fact.get('payment_policy'):result[tag]['payment_policy']=fact['payment_policy']
        return result

    def describe(self,oid,cat,reason,locations,decision):
        from .source_opinion import DETAIL,EFFECT
        matching={loc_key(loc) for loc in locations}
        es=[e for e in self.by_operation.get(oid,()) if loc_key(self.effects[e]['where']) in matching]
        ids=set()
        for e in es:ids.update(self.for_effect(e))
        att=self.inv.issues.get(decision,{}).get('property') or {}
        for c in att.get('consent_rows',[]):
            for fact in c.get('fact_ids',[]):
                ids.add(fact)
                effect=self.facts[fact]['handle']
                if effect in self.effects and effect not in es:es.append(effect)
        if self.inv.issues.get(decision,{}).get('current',{}).get('_semantic_consumer'):
            for e in self.inv.issues[decision]['current'].get('_scope_effects',()):ids.update(self.for_effect(e))
        origins=set();rules=set();types=set()
        for fid in ids:
            roots,applied=self.logic.basis(fid);origins.update(roots);rules.update(applied)
            types.add(self.facts[fid]['meaning'])
        statement=next(iter(sorted(matching,key=str)),None)
        position=' at source offset '+str(statement[1]) if statement and isinstance(statement[1],int) else ''
        kind=EFFECT.get(cat,'the scoped program effect')
        basis=DETAIL.get(reason,DETAIL['scope_missing'])
        if cat=='AC' and reason in ('source_role_reassignment','applicable_role_guard','guarded_state_change','guarded_source_effect','unguarded_governed_effect') and 'current_authority_required' in types:rules.add('P09')
        interprets=sorted({c['meaning'] for c in att.get('consent_rows',[])})
        if interprets:types.update(interprets)
        lead='The assessment concerns '+kind+position
        if types:lead+=' under '+', '.join(sorted(types))
        wording=lead+'. '+basis
        return {'explanation':wording,'facts':sorted(ids),'rules':sorted(rules),'supports':sorted(origins),'effects':sorted(es),
                'meanings':sorted(types)}

    def source_offices(self,oid):
        from .source_opinion import office_use, replacement_status
        from .policy_binding import conjuncts
        from .initial_state import initial_for_lookup
        lookup=self.f.lookup(oid)
        state=initial_for_lookup(lookup)
        found={}
        for e in sorted(self.by_operation.get(oid,())):
            if not self.remaining():self.incomplete.add(oid);break
            d=self.effects[e]
            if 'write' not in d:continue
            cell=d['cell'];w=d['write'];rid=cell['root']
            from .roles import _is_table
            table=_is_table(lookup.nodes.get(rid,{}))
            grant=w['value']
            if not d['clean']:continue
            if table:
                if len(keys(cell))!=1 or grant.get('kind')!='literal' or grant.get('value') is not True:continue
            elif keys(cell) or value_type(cell,lookup) not in ('address','address payable') or grant.get('kind') not in ('parameter','actual_sender'):continue
            established=(state or {}).get('declarations',{}).get(rid,{})
            use=office_use(self.inv,oid,cell)
            if not use:continue
            startup=bool(established.get('constructor_writes') or established.get('explicit_initializer'))
            # A separate, actually guarded replacement of the same office is
            # independent incumbent-policy evidence even without a constructor.
            from .source_opinion import office_guard,feasible_source_guards
            protected_peer=False
            for peer in self.by_decl.get(self.obj(d['target'],rid),()):
                pd=self.effects[peer]
                if not self.remaining():break
                if pd['oid']==oid or 'write' not in pd or not pd['clean']:continue
                pr=self.f.paths[pd['path']]['raw']
                if not feasible_source_guards(pr['guards']):continue
                if any(office_guard(g,cell) for g in pr['guards']):
                    protected_peer=True;break
                nominee=pd['write']['value']
                if nominee.get('kind')!='storage' or keys(nominee) or nominee['root']==rid:continue
                if not any(office_guard(g,nominee) for g in pr['guards']):continue
                # An accepted nominee may replace the incumbent, but only after an
                # independent incumbent-authorized nomination. Account for every
                # real positive writer to that applied slot; a public nomination
                # route would invalidate this source policy inference.
                nominations=[a for a in self.f.writes.values() if self.f.operations[a['operation']]['target']==d['target']
                    and key(a['raw']['path'])==key(nominee) and not (a['raw']['value'].get('kind')=='literal' and a['raw']['value'].get('value')==0)]
                if nominations and all(a['raw']['value'].get('kind') in ('parameter','actual_sender') and
                    any(office_guard(g,cell) for g in self.f.paths[a['path']]['raw']['guards']) for a in nominations):
                    protected_peer=True;break
            applied_policy=any(self.facts[f]['meaning']=='current_authority_required' for f in self.for_effect(e))
            # A repeatable installation of the caller into the very office that alone
            # governs another committing use supplies lifecycle evidence in its own right.
            # A protected switch can also define a narrower, conditional exemption.
            from .source_opinion import exception_authority
            branch=self.f.paths[d['path']]['raw']
            repeatable_self=(not table and grant.get('kind')=='actual_sender' and not branch['guards']
                             and any(office_guard(g,cell) for r in self.f.summaries.rows(use)
                                     if r['ordered_writes'] and not r['residuals'] for g in r['guards']))
            governors=set().union(*(exception_authority(self.inv,use,cell,g)
                                    for r in self.f.summaries.rows(use) for g in r['guards']))
            if not (startup or protected_peer or applied_policy or repeatable_self or governors):continue
            row=self.f.paths[d['path']]['raw']
            status=replacement_status(self.inv,d)
            if status=='open':continue
            subject=self.obj(d['target'],rid)
            fid=self.fact(e,'current_authority_required',subject)
            sid='source_'+digest([self.f.identity,e,use,'incumbent_role_use'])[:20]
            self.register(fid,sid,'source_policy_deduction','policies')
            found[e]=(status,fid)
            self.__dict__.setdefault('office_uses',{})[e]=use
        self.logic.settle()
        return found

    def scope_offices(self):
        if self.f.options.scope!='AC':return
        inv=self.inv
        self.index()
        for oid in sorted(self.by_operation):
            if not self.remaining():self.incomplete.add(oid);continue
            offices=self.source_offices(oid)
            if not offices:continue
            for q in list(inv.issues.values()):
                if inv.root(q)!=oid:continue
                locs=q['current'].get('_scope_effects',[])
                if locs:
                    q['office_effects']={e:v for e,v in offices.items() if e in locs}
                    continue
                from .source_opinion import statement_focus
                focus=statement_focus(inv,q,self.f.summaries.rows(oid))
                if focus:
                    matches=[e for e in self.by_operation[oid] if loc_key(self.effects[e]['where'])==loc_key(focus[1]['source'])]
                    q['effect_scope']=matches
                    q['office_effects']={e:v for e,v in offices.items() if e in matches}
                else:q['office_effects']=dict(offices)
            for e in offices:
                if not any(e in q.get('office_effects',{}) for q in inv.issues.values() if inv.root(q)==oid):
                    q=self.create_consumer(oid,'AC',{e})
                    if q:q['office_effects']={e:offices[e]}
            for q in inv.issues.values():
                if inv.root(q)==oid:q.pop('_source_opinion',None)

    def office_opinion(self,q,rows):
        from .source_opinion import opinion,blocked_positive
        lookup=self.f.lookup(self.inv.root(q))
        explicit=set(q['current'].get('_scope_effects',()))
        candidates={e:v for e,v in q.get('office_effects',{}).items() if not explicit or e in explicit}
        es=explicit or q.get('effect_scope') or ()
        for e in es:
            d=self.effects[e]
            if 'write' not in d:continue
            for fid in self.for_effect(e):
                f=self.facts[fid]
                if f['meaning']!='current_authority_required':continue
                subject=f.get('subject')
                if subject and self.objects.get(subject,{}).get('decl')!=d['cell']['root']:continue
                if self.f.operations[d['oid']]['target']!=d['target']:continue
                from .source_opinion import office_use,replacement_status
                from .policy_binding import conjuncts
                if not d['clean'] or not office_use(self.inv,d['oid'],d['cell']):continue
                path=self.f.paths[d['path']]['raw'];guards=[g for t in path['guards'] for g in conjuncts(t)]
                status=replacement_status(self.inv,d)
                if status!='open':candidates[e]=(status,fid)
        if not candidates:return None
        for e,(status,fid) in candidates.items():
            d=self.effects[e]
            if status=='risk' and not blocked_positive(self.inv,q,d['path'],'AC'):
                result=opinion('risk','source_role_reassignment',[d['where']])
                use=getattr(self,'office_uses',{}).get(e)
                if use:result['protected_use']=self.f.operations[use]['source']
                return result
        covered={d['path'] for e,(status,_) in candidates.items() if status=='normal' for d in [self.effects[e]]}
        if covered and {r['path'] for r in rows}<=covered:
            return opinion('normal','applicable_role_guard',[self.effects[e]['where'] for e in candidates])
        return None


    def disputed(self,q):
        oid=self.inv.root(q)
        if not oid:return False
        groups=defaultdict(set)
        for e in self.by_operation.get(oid,()):
            for fid in self.for_effect(e):
                m=self.facts[fid]['meaning']
                if m in RESOURCE:groups[e,'unit'].add(m)
                if m in CONSENT:groups[e,'consent'].add(m)
                if m=='unknown':return True
        return any(len(ms)>1 for ms in groups.values())

    def route_scopes(self,q):
        oid=self.inv.root(q)
        item=q['current']
        explicit=item.get('_scope_effects',()) or q.get('effect_scope',())
        if explicit:return set(explicit)
        from .source_opinion import statement_focus
        if not oid:return set()
        focus=statement_focus(self.inv,q,self.f.summaries.rows(oid))
        if focus:return {e for e in self.by_operation[oid] if loc_key(self.effects[e]['where'])==loc_key(focus[1]['source'])}
        return set(self.by_operation.get(oid,()))

    def authority_cell(self,e,subject):
        d=self.effects[e];lk=self.f.lookup(d['oid'])
        if subject:
            obj=self.objects.get(subject)
            if not obj or obj['target']!=d['target'] or obj['oid'] is not None:return None
            cell={'kind':'storage','root':obj['decl'],'segments':[]}
        else:
            cell=d.get('cell')
        if cell and not cell.get('segments') and value_type(cell,lk) in ('address','address payable'):return cell
        return None

    def authority_binding(self,e,subject):
        """Locate a principal in the actual effect context before judging guard strength."""
        from .source_opinion import identity_guard
        d=self.effects[e]
        cell=self.authority_cell(e,subject)
        if not cell:return None
        if 'write' in d:
            row=self.f.summaries.paths[d['path']]
            changed=any(key(w['path'])==key(cell) for w in row['ordered_writes'][:d['version']])
            # Equality within a disjunction identifies a role operand, not an
            # authorization proof. The backend retains the full committing guard.
            guarded_subject=any(identity_guard(term,{cell['root']}) for term in walk(row['guards']))
            if not changed and (cell==d['cell'] or subject and guarded_subject):
                return cell
        # The existing independent peer-policy and callpoint checks can also
        # establish a role. Being an address or receiving funds cannot do so.
        authority,_=self.authority_effect(e,subject)
        if authority in ('guarded_state_change','unguarded_governed_effect','guarded_source_effect'):
            return cell
        return None

    def authority_effect(self,e,subject):
        """Assess only the located action and the stated principal. Never assume a
        declared address is the policy for every write to a different position."""
        from .policy_binding import conjuncts
        from .source_opinion import identity_guard
        d=self.effects[e];role=self.authority_cell(e,subject)
        if 'cell' not in d:
            if d['kind']=='dangerous_external_call':return 'external_dependency',role
            if not role:return 'policy_scope_unsubstantiated',None
            # Check the guard at the actual effect, before returning to the caller.
            for pid in d['branches']:
                if not self.remaining():return 'policy_effect_unresolved',role
                branch=self.f.summaries.paths[pid]
                occurrences=[term for term in branch['effects'] if term.get('kind')==d['kind'] and loc_key(term['source'])==loc_key(d['where'])]
                if branch['residuals'] or not occurrences:return 'policy_effect_unresolved',role
                for term in occurrences:
                    guards=[g for x in term.get('callpoint_guards',()) for g in conjuncts(x)]
                    if any(key(w['path'])==key(role) for w in term.get('callpoint_writes',())) or not any(identity_guard(g,{role['root']}) for g in guards):
                        return 'policy_scope_unsubstantiated',role
            return 'guarded_source_effect',role
        if role==d['cell']:return 'office',role
        if not role:return 'policy_scope_unsubstantiated',None
        row=self.f.summaries.paths[d['path']]
        def guarded(r):
            # A guard on a prior version cannot authenticate a newly replaced authority.
            return any(identity_guard(g,{role['root']}) for term in r['guards'] for g in conjuncts(term))
        if not d['clean'] or row['effects'] or any(key(w['path'])==key(role) for w in row['ordered_writes'][:d['version']]):
            return 'policy_effect_unresolved',role
        if guarded(row):return 'guarded_state_change',role
        if row['guards']:return 'policy_effect_unresolved',role
        obj=self.obj(d['target'],field_node(d['cell']))
        for other in self.by_decl[obj]:
            if not self.remaining():return 'policy_effect_unresolved',role
            peer=self.effects[other]
            if peer['oid']==d['oid'] or not peer['clean'] or key(peer['cell'])!=key(d['cell']):continue
            # Cross-entry consent for keyed state requires additional holder/key evidence.
            if d['cell'].get('segments') or value_type(d['cell'],self.f.lookup(d['oid']))!='bool':continue
            now,other_value=d['write']['value'],peer['write']['value']
            if not all(x.get('kind')=='literal' and type(x.get('value')) is bool for x in (now,other_value)) or now['value']==other_value['value']:continue
            comp=self.f.summaries.paths[peer['path']]
            if comp['effects'] or any(key(w['path'])==key(role) for w in comp['ordered_writes'][:peer['version']]) or not guarded(comp):continue
            # A known public writer of the same applied setting and same outcome
            # is a normal alternative to the claimed control over that outcome.
            for writer in self.by_decl[obj]:
                if not self.remaining():return 'policy_effect_unresolved',role
                other=self.effects[writer]
                if other['oid']==d['oid'] or key(other['cell'])!=key(d['cell']) or key(other['write']['value'])!=key(now):continue
                other_row=self.f.summaries.paths[other['path']]
                if other['clean'] and not other_row['effects'] and not other_row['guards']:return 'policy_scope_unsubstantiated',role
            return 'unguarded_governed_effect',role
        return 'policy_scope_unsubstantiated',role

    def issuance_control(self,d,row,guards):
        """Read the selected final credit, its funding and who controls the quantity."""
        from .ledger import unit_origin
        from .prestate import state_facts
        from .source_opinion import paid_credit,quantity_forced_zero,sourced_quantity
        oid=d['oid'];lookup=self.f.lookup(oid);w=d['write'];cell=d['cell']
        who=holder(cell,lookup);sign,qty=local_delta(w)
        if sign!='+' or not qty or not who or who.get('kind') not in ('parameter','actual_sender'):
            return None
        if not unit_origin(self.inv.backend,oid,cell):return None
        # Another write in this storage family could replace or fund the credit,
        # including via a differently spelled but aliasing key.
        if any(v['path']['root']==cell['root'] for i,v in enumerate(row['ordered_writes']) if i!=d['version']):
            return None
        if row['effects']:return None
        if paid_credit(self.inv,oid,row):return 'ordinary_paid_credit'
        if quantity_forced_zero(guards,qty,lookup):return 'zero_quantity'
        # Any independently consumed asset/claim needs its own normal explanation.
        # Scalar supply/accounting increments do not finance the selected credit.
        for i,peer in enumerate(row['ordered_writes']):
            if i==d['version']:continue
            direction,_=local_delta(peer)
            if keys(peer['path']) or direction!='+':return None
        fixed=state_facts(lookup)
        def forced_zero(term):
            kind=term.get('kind')
            if kind=='literal':return term.get('value')==0
            if kind=='storage' and not keys(term):
                decl=fixed.get(term['root'],{})
                return decl.get('encoded') and decl.get('value')==0
            args=term.get('args',())
            if args and term.get('op')=='*':return any(forced_zero(v) for v in args)
            if args and term.get('op')=='+':return all(forced_zero(v) for v in args)
            return False
        if forced_zero(qty):return 'zero_quantity'
        if not sourced_quantity(qty,lookup):return None
        inputs={key(t) for t in walk(qty) if t.get('kind')=='parameter'}
        if not inputs:return None
        # A caller-supplied argument constrained to an accrued or fixed amount
        # is not a free choice. Strict positive lower bounds retain discretion.
        for guard in guards:
            if not any(key(t) in inputs for t in walk(guard)):continue
            args=guard.get('args',())
            if len(args)==2:
                left,right=args
                if guard.get('op') in ('<','<='):left,right=right,left
                if guard.get('op') in ('<','<=','>','>=','!=') and key(left) in inputs and right.get('kind')=='literal' and right.get('value')==0:
                    continue
            return None
        return 'discretionary_credit'

    def contextual_authority(self,e,q,subject=None):
        """Apply a located normative responsibility to the actor at the actual effect."""
        from .source_opinion import blocked_positive,feasible_source_guards,role_ids,identity_guard
        from .policy_binding import conjuncts
        d=self.effects[e];oid=d['oid']
        if self.effect_focus(e) not in ('termination','credit','funds'):return None
        role=self.authority_cell(e,subject) if subject else None
        if subject and role is None:return None
        normal={}
        if d.get('kind') in ('native_selfdestruct','native_transfer'):
            branches=d['branches']
        elif 'write' in d:
            branches=[d['path']]
        else:return None
        for pid in branches:
            row=self.f.summaries.paths[pid]
            if not row['committing'] or row['residuals'] or blocked_positive(self.inv,q,pid,'AC'):continue
            guards=[g for term in row['guards'] for g in conjuncts(term)]
            at_effect=guards
            if 'write' in d:
                before=row['ordered_writes'][:d['version']]
            else:
                occurrences=[t for t in row['effects'] if t['kind']==d['kind'] and loc_key(t['source'])==loc_key(d['where'])]
                if not occurrences or any('callpoint_guards' not in t for t in occurrences):continue
                points=[[g for term in t['callpoint_guards'] for g in conjuncts(term)] for t in occurrences]
                if any(key(point)!=key(points[0]) for point in points[1:]):continue
                at_effect=points[0]
                before=[w for t in occurrences for w in t.get('callpoint_writes',())]
            if role:
                if any(w['path']['root']==role['root'] for w in before):continue
                roles={role['root']}
            else:
                roles=role_ids(self.inv,oid,row)
            if any(identity_guard(g,roles) for g in at_effect):
                normal[pid]='guarded_source_effect'
                continue
            if 'write' in d:
                reading=self.issuance_control(d,row,guards)
                if reading in ('ordinary_paid_credit','zero_quantity'):
                    normal[pid]=reading
                    continue
                if reading!='discretionary_credit':continue
            # A guard on a different principal or a mixed payment branch needs
            # its own comparison. Neither establishes this role's authorization.
            if 'write' not in d and {key(g) for g in guards}!={key(g) for g in at_effect}:continue
            if any(t.get('kind') not in ('op','literal','parameter','transaction_origin','storage')
                   for t in walk(guards)):continue
            if any(t.get('kind')=='storage' for t in walk(guards)) and not all(
                    g.get('op')=='==' and any(t.get('kind') in ('transaction_origin','tx_origin') for t in g.get('args',()))
                    for g in guards):continue
            if not feasible_source_guards(guards):continue
            if d.get('kind')=='native_transfer':continue
            if any(t.get('kind')=='transaction_origin' for t in walk(guards)):
                return 'origin_only_decider'
            return 'unrestricted_termination_decision' if 'branches' in d else 'unrestricted_issuance_decision'
        if set(normal)==set(branches) and len(set(normal.values()))==1:return next(iter(normal.values()))
        return None

    def local_opinion(self, q):
        from .policy_binding import conjuncts, effect_duty
        from .relations import opinion_principals
        from .roles import _roots
        from .source_opinion import opinion, blocked_positive, feasible_source_guards, covered_delegation, role_ids
        from pr_next_joint.frontend.path_ir import conditions_possible, op

        item = q['current']
        scopes = item.get('_scope_effects', ())
        if not item.get('_opinion_message') or not scopes or item.get('assessment') not in ('risk','normal'):
            return None
        expected = (q.get('property') or {}).get('expected_authorization') or {}
        compiled = expected.get('compiled_authorization') or {}
        if (expected.get('unresolved_relations') or compiled.get('necessary_only') or compiled.get('competing_interpretations')
                or compiled.get('kind') == 'source_role_payment_policy'):
            return None
        if expected.get('source') == 'focused_model_answer':
            duty = effect_duty(expected.get('basis',''))
        else:
            duty = effect_duty(item.get('policy_basis') or item['claim'])
            if not duty and item.get('policy_basis'):
                duty = effect_duty(item['claim'])
        if not duty:
            # Descriptive text may locate a useful effect. Its source facts and
            # independently established policies still have their own consumers.
            return None
        oid = self.inv.root(q)
        actor = {'kind':'actual_sender'}
        statuses, locations = [], []
        for eid in scopes:
            effect = self.effects[eid]
            if effect['oid'] != oid:
                continue
            principals = opinion_principals(self.inv, item, effect, duty)
            for pid in ([effect['path']] if 'path' in effect else effect['branches']):
                row = self.f.summaries.paths[pid]
                conditions = [g for guard in row['guards'] for g in conjuncts(guard)]
                if not row['committing'] or not feasible_source_guards(conditions):
                    continue
                locations.append(effect['where'])
                if self.f.call_summaries.effect_dependencies(row, effect, initiation=True):
                    statuses.append('open')
                    continue
                if 'write' in effect and any(key(w['path']) == key(effect['cell'])
                        for w in row['ordered_writes'][effect['version']+1:]):
                    statuses.append('open')
                    continue
                if duty['qualified'] or any(kind == 'conflict' for kind, _ in principals):
                    statuses.append('open')
                    continue
                proofs = []
                for kind, term in principals:
                    if term is None or kind == 'conflict':
                        # An abstract duty can govern a publicly selectable action.
                        # It cannot by itself identify a different source guard.
                        proofs.append(False if kind == 'abstract' and not role_ids(self.inv,oid,row) else None)
                        continue
                    if (kind == 'holder' and 'write' in effect and local_delta(effect['write'])[0] == '-'
                            and covered_delegation(self.inv,oid,[row])):
                        proofs.append(True)
                    elif kind == 'office' and value_type(term,self.f.lookup(oid)) not in ('address','address payable'):
                        recognized = role_ids(self.inv,oid,row) & {term['root']}
                        proofs.append(any(_roots(g,recognized) for g in conditions) if recognized else None)
                    else:
                        try:
                            proofs.append(key(actor)==key(term) or not conditions_possible(conditions,op('==',actor,term)))
                        except (ValueError,RecursionError):
                            proofs.append(None)
                sufficient = any(proof is True for proof in proofs) if duty['alternative'] else all(proof is True for proof in proofs)
                missing = all(proof is False for proof in proofs) if duty['alternative'] else any(proof is False for proof in proofs)
                if (duty['alternative'] and not sufficient and all(term is not None and (
                        kind == 'holder' or kind == 'office' and value_type(term,self.f.lookup(oid)) in ('address','address payable'))
                        for kind,term in principals)):
                    # Each allowed identity can occupy a different disjunct of the guard.
                    allowed = op('or', *[op('==',actor,term) for _,term in principals])
                    try:
                        sufficient = not conditions_possible(conditions,allowed)
                    except (ValueError,RecursionError):
                        missing = False
                if (not sufficient and compiled.get('binding_effect') == eid and compiled.get('source_bound_alternatives')
                        and compiled.get('predicate') and not compiled.get('necessary_only')):
                    try:
                        sufficient = not conditions_possible(conditions, compiled['predicate'])
                    except (ValueError,RecursionError):
                        missing = False
                if sufficient:
                    statuses.append('normal')
                elif not missing or blocked_positive(self.inv,q,pid,'AC'):
                    statuses.append('open')
                elif 'write' in effect and self.issuance_control(effect,row,conditions) in ('ordinary_paid_credit','zero_quantity'):
                    # Let the independently recorded source alternative speak for itself.
                    return None
                else:
                    statuses.append('risk' if item['assessment']=='risk' else 'open')
        if not statuses:
            return None
        status = 'risk' if 'risk' in statuses else 'normal' if all(v=='normal' for v in statuses) else 'open'
        reason = {'risk':'scoped_semantic_conflict','normal':'scoped_semantic_normal','open':'scope_missing'}[status]
        result = opinion(status,reason,{loc_key(loc):loc for loc in locations}.values())
        result['semantic_local'] = True
        result['same_scope_authorized'] = status == 'normal'
        return result

    def effect_policy_opinion(self,q):
        if self.f.options.scope!='AC':return None
        from .source_opinion import opinion,blocked_positive
        out=[];located=[];policy_sources=set()
        if not q['current'].get('_semantic_consumer'):
            return self.local_opinion(q)
        for e in self.route_scopes(q):
            d=self.effects[e]
            if d['oid']!=self.inv.root(q):continue
            for fid in self.for_effect(e):
                fact=self.facts[fid]
                if fact['meaning']=='current_authority_required':
                    status,role=self.authority_effect(e,fact['subject'])
                    compiled=((q.get('property') or {}).get('expected_authorization') or {}).get('compiled_authorization') or {}
                    if not compiled and status in ('policy_scope_unsubstantiated','policy_effect_unresolved'):
                        status=self.contextual_authority(e,q,fact['subject']) or status
                    if status=='office' or compiled.get('kind')=='source_role_payment_policy' and compiled.get('binding_effect')==e:
                        continue
                    if status=='unguarded_governed_effect' and blocked_positive(self.inv,q,d['path'],'AC'):status='policy_effect_unresolved'
                    out.append(status);located.append(d['where']);policy_sources.add(fact['subject'])
                elif 'cell' not in d and fact['meaning'] in ('unknown','other_source_policy'):
                    out.append('external_dependency' if d['kind']=='dangerous_external_call' else 'policy_missing')
                    located.append(d['where'])
        if not out:return None
        if len(policy_sources)>1:return opinion('open','policy_scope_unsubstantiated',located)
        for supported in ('unguarded_governed_effect','unrestricted_termination_decision','unrestricted_issuance_decision','origin_only_decider'):
            if supported in out:return opinion('risk',supported,located)
        protected={'guarded_state_change','guarded_source_effect','ordinary_paid_credit','zero_quantity'}
        if set(out)<=protected:return opinion('normal',out[0],located)
        reason=next(v for v in out if v not in protected)
        return opinion('open',reason,located)

    def policy(self,q):
        if not self.inv.root(q):return None
        fs=[(self.facts[f],f,e) for e in sorted(self.route_scopes(q)) for f in self.for_effect(e) if self.facts[f]['meaning'] in AUTH]
        if not fs:return None
        if len({(r['meaning'],r['subject'],r.get('payment_policy'),e) for r,f,e in fs})!=1:return None
        r,fid,e=fs[0];d=self.effects[e];lookup=self.f.lookup(d['oid'])
        if r['meaning']=='holder_authorization_applies':
            if 'cell' not in d:return None
            grant=key_relation(d['cell'],lookup);ordered=keys(d['cell'])
            if not grant or grant.get('kind')!='authorization_quantity' or len(ordered)!=2:return None
            subject=ordered[grant['holder_key']]
            if r['subject'] and self.objects[r['subject']]['decl']!=subject.get('id',subject.get('root')):return None
            return {'meaning':'required_authorization','polarity':'asserted','level':'H','semantic_fact':fid,
                    'explicit_policy_kind':r['meaning'],'qualified_cell':subject,'binding_effect':e,
                    'text':'The actual holder issues this grant.','source_anchors':q['current']['anchors']}
        if r['meaning']=='initialization_stage':
            if not r.get('subject'):return None
            flag={'kind':'storage','root':self.objects[r['subject']]['decl'],'segments':[]}
            if value_type(flag,lookup)!='bool':return None
            if not any(key(w['path'])==key(flag) and w['value'].get('value') is True for row in self.f.summaries.rows(d['oid']) for w in row['ordered_writes']):return None
            return {'meaning':'required_authorization','polarity':'asserted','level':'H','semantic_fact':fid,'explicit_policy_kind':r['meaning'],
                    'qualified_cell':flag,'binding_effect':e,'text':'The located one-time stage limits this effect.','source_anchors':q['current']['anchors']}
        if r['meaning']=='current_authority_required':
            sub=self.authority_binding(e,r['subject'])
            if not sub:return None
            return {'meaning':'required_authorization','polarity':'asserted','level':'H','semantic_fact':fid,
                    'explicit_policy_kind':r['meaning'],'qualified_cell':sub,'binding_effect':e,
                    'payment_policy':r.get('payment_policy'),'text':'The incumbent qualifies the recorded change.','source_anchors':q['current']['anchors']}
        return None


    def disputed_effects(self,q):
        oid=self.inv.root(q)
        if not oid:return set()
        pairs=[]
        effects=set(q['current'].get('_scope_effects',())) or self.by_operation.get(oid,set())
        for e in effects:
            groups=defaultdict(set)
            for fid in self.for_effect(e):
                meaning=self.facts[fid]['meaning']
                if meaning in RESOURCE:groups['resource'].add(meaning)
                if meaning in CONSENT:groups['consent'].add(meaning)
            if any(len(s)>1 for s in groups.values()):pairs.append(e)
        return set(pairs)

    def describe_source(self,oid,cat,reason,locations,qid):
        row=self.describe(oid,cat,reason,locations,qid)
        q=self.inv.issues[qid]
        evidence=[self.inv.evidence[e] for e in q['evidence']]
        prop=q.get('property') or {}
        modes={v['meaning'] for v in prop.get('consent_rows',[])}
        if reason=='program_support':
            usable=[v for record in evidence for v in record.get('queries',())
                    if v.get('bounded_condition_confirmed') and v.get('details',{}).get('property_validated')
                    and (v['details'].get('property_identity')==prop.get('id') or record.get('property_validation_key')==q.get('changed_validation_key') and q.get('changed_validation_key'))]
            labels={v.get('label') for v in usable}
            anchor=self.f.operations.get(oid,{}).get('function','this entry')
            if cat=='AC' and 'authorization_violation' in labels:
                expected=prop.get('expected_authorization') or {}
                row['explanation']=('At '+anchor+', the committing effect admits a requester outside the applicable source-bound qualification. '+
                    ('The policy concerns acquisition and subsequent protected use.' if expected.get('property_family')=='acquire' else
                     'The check compares the effective guard with the bound authorization requirement, including any alternative qualification.'))
                paid=(expected.get('compiled_authorization') or {}).get('source_requirement') or {}
                if paid.get('kind')=='source_role_payment_policy' and not paid.get('permits_payment'):
                    if paid.get('payment_relation')=='joint':
                        row['explanation']='At '+anchor+', the policy requires both the incumbent role and the qualifying payment. The effective guard admits a committing change without that combination.'
                    else:
                        row['explanation']='At '+anchor+', the incumbent role is necessary for this effect. The payment branch can commit the change without that role.'
            elif cat=='FCR-MINT' and labels & {'direct_effect','financial_value'}:
                row['explanation']=('At '+anchor+', the checked privilege permits positive additional rights for the controller or a beneficiary it can select. '+
                    ('The intervention can enable a new same-request outcome; baseline commitment is not established.' if any(v['details'].get('baseline_commit_not_assumed') for v in usable) else
                     'A balance increase for an independent ordinary buyer alone does not satisfy this condition.'))
            elif cat=='FCR-DESTROY' and labels & {'direct_effect','financial_value'}:
                row['explanation']='At '+anchor+', a privileged effect leaves another holder with fewer rights in the same unit after attributed transfers and applicable settlement.'
            elif cat=='FCR-TRANSFER' and labels & {'direct_effect','financial_value'}:
                row['explanation']='At '+anchor+', the scoped change moves another holder’s existing rights to a separate position without the applicable holder-issued consent.'
            elif cat in ('FCR-PAUSE','FCR-FREEZE') and 'financial_block' in labels:
                group='the designated holder' if cat=='FCR-FREEZE' else 'ordinary holders'
                row['explanation']='At '+anchor+', the checked privileged change restricts the outgoing right of '+group+' for an otherwise usable request within the recorded domain.'
        if reason=='source_check_excluded' and cat=='FCR-MINT' and prop.get('value_dependence',{}).get('value_uses'):
            uses=prop['value_dependence']['value_uses']
            actual_paid_use=any(any(n.get('kind')=='transaction_value' for n in walk([r['guards'],r['ordered_writes']])) for o in uses for r in self.f.summaries.rows(o))
            if actual_paid_use:
                row['explanation']='The price or amount control reaches a paid credit. The applicable source check excludes positive additional rights for the controller or a beneficiary it selects; a separate buyer receiving its own purchase does not establish this capability.'
        if modes=={'net_request_with_fee'} and cat=='FCR-DESTROY' and reason in ('scope_missing','scoped_fee_consent','program_support'):
            row['explanation']=('The matched holder allowance uses the net request and its disclosed fee. '+
               ('The applicable check excludes an uncompensated debit under that effective grant.' if reason=='scoped_fee_consent' else
                'The authorization may be zero on the pertinent debit; the recorded net interpretation alone cannot exclude loss.' if reason=='scope_missing' else
                'The matched debit still has a source-supported loss after applicable consent.'))
        if modes=={'gross_debit_bound'} and cat in ('FCR-TRANSFER','FCR-DESTROY') and reason in ('program_support','source_certificate'):
            row['explanation']=('The holder-issued bound applies to the gross debit of this request. '+
                ('The check finds an unauthorized debit with credit to a separate position; the credit itself need not exceed the grant.'
                 if cat=='FCR-TRANSFER' else 'The check finds a positive uncompensated loss under that gross bound.'))
        if reason=='program_support' and cat in ('FCR-TRANSFER','FCR-DESTROY','FCR-MINT'):
            uses={ev.get('observe') for ev in evidence if ev.get('change')==oid and ev.get('observe')!=oid and
                  any(v.get('label')=='financial_value' and v in usable for v in ev.get('queries',()))}
            if len(uses)==1 and (use:=next(iter(uses))) in self.f.operations:
                before=self.f.operations[oid]['function'];after=self.f.operations[use]['function']
                row['explanation']=('The change at '+before+' affects the same holder request at '+after+'. '+
                        {'FCR-TRANSFER':'The checked difference is a movement of existing rights to a separate position outside applicable consent.',
                         'FCR-DESTROY':'The checked difference is an uncompensated reduction of existing rights under the applicable consent.',
                         'FCR-MINT':'The checked difference is a new positive entitlement for a controlled beneficiary.'}[cat])
        if any(v.get('kind')=='source_inspection' for v in evidence):row['origins']=['source_observation']
        else:row['origins']=[]
        row['origins']+=sorted({self.supports[s]['origin'] for s in row['supports'] if s in self.supports})
        if row['rules']:row['origins'].append('rule_derivation')
        if reason in ('program_support','source_check_excluded') and any(v.get('queries') for v in evidence):row['origins'].append('scoped_program_check')
        if modes:
            if any(c.get('source')=='focused_source_bound_semantic_answer' for c in prop.get('consent_rows',[])):row['origins'].append('source_bound_semantic_answer')
        return row

    def matching_dispute(self,q):
        """A source-typed financial interpretation stays unresolved only when its two meanings matter."""
        es=self.disputed_effects(q)
        if not es:
            why=self.unresolved(q)
            if why:return dict(status='open',reason=why,locations=[self.f.operations[self.inv.root(q)]['source']])
            if self.f.options.scope=='FCR' and q['current'].get('_semantic_consumer') and not q['current'].get('category'):
                effects=self.route_scopes(q)
                if effects and all('write' in self.effects[e] and self.effects[e]['clean'] and local_delta(self.effects[e]['write'])[0] and
                        {self.facts[f]['meaning'] for f in self.for_effect(e)}=={'nonfinancial_counter'} and
                        self.local_counter(e) for e in effects):
                    return dict(status='normal',reason='scoped_counter',locations=[self.effects[e]['where'] for e in sorted(effects)])
            return None
        return {'status':'open','reason':'conflicting_scoped_meanings','locations':[self.effects[e]['where'] for e in sorted(es)]}



    def local_counter(self,e):
        # Use the already registered dependency summary. An unfinished search cannot close a use.
        d=self.effects[e]
        summary=self.f.summaries.dependencies.forward_cache.get(d['oid'])
        if not summary or not summary['fixed_point_over_indexed_definitions'] or summary['residuals']:return False
        uses=summary['uses']
        if any(not self.f.operations[u].get('generated_getter') for u in uses):return False
        from .ledger import _unit_origin
        return not _unit_origin(self.inv.backend,d['oid'],d['cell'])

    def legacy_resource(self,oid,cell,meaning,scope):
        receipt=getattr(self,'legacy_receipt',None)
        if not receipt or not self.built or scope.get('phase') or scope.get('assumptions'):return
        target=self.f.operations[oid]['target'];obj=self.obj(target,field_node(cell))
        if obj not in self.objects:return
        source,submission=receipt
        if source not in ('verified_service','fixture') or not submission:return
        fid=self.fact(obj,meaning)
        sid='support_'+digest([source,submission,fid])[:20]
        if self.register(fid,sid,source,'annotations'):
            self.derive(fid);self.logic.settle()

    def planning_read(self,q):
        if not q['current'].get('_semantic_consumer'):return
        for e in q['current'].get('_scope_effects',()):
            if e not in self.effects:continue
            d=self.effects[e]
            for fid in self.for_effect(e):
                meaning=self.facts[fid]['meaning']
                if not self.remaining():self.incomplete.add(d['oid']);return
                if meaning in ('price','fee_rule','amount_role') and 'cell' in d:
                    obj=self.obj(d['target'],field_node(d['cell']))
                    for sink,k,rs,exact in self.routes.get(obj,()):
                        if not self.remaining():self.incomplete.add(d['oid']);return
                        use=self.effects[sink]['oid']
                        if k=='value' and use!=d['oid']:
                            q.setdefault('semantic_read_dependencies',set()).add(use)
                            self.inv.enqueue(q['id'],'inspect',{'operation':use,'enhance':False},2,'source_quantity_consumer')
                if meaning in ('authorization_quantity','eligibility_state','transfer_condition'):
                    self.inv.enqueue(q['id'],'inspect',{'operation':d['oid'],'enhance':False},1,'condition_subject_and_use')


    def withdrawn_dependency(self,e):
        d=self.effects[e]
        if any(self.facts[f]['meaning'] in RESOURCE for f in self.for_effect(e)):return False
        for support in self.supports.values():
            if support['active'] or not support.get('withdrawn'):continue
            row=self.facts[support['fact']];h=row['handle']
            if row['meaning'] not in RESOURCE:continue
            if h==e or h==self.obj(d['target'],field_node(d['cell'])) or any(dest==e and kind=='value' for dest,kind,_,_ in self.routes.get(h,())):return True
        return False

    def index_transfer(self,src,e,fid,pre,rule):
        dest=self.facts[fid]
        obj=self.obj(self.effects[e]['target'],field_node(self.effects[e]['cell']))
        if self.objects.get(src,{}).get('oid') is not None or src==obj or not self.effects[e]['clean']:return
        w=self.effects[e]['write']
        if keys(w['path']) or w['value'].get('kind')!='storage' or keys(w['value']):return
        # Only cells whose every committing writer copies this very source may export that interpretation.
        # It describes a value family, not the existence of a reachable transition or consent.
        writers=self.by_decl[obj]
        if any(not self.effects[q]['clean'] or key(self.effects[q]['write']['value'])!=key(w['value']) for q in writers):return
        if dest['meaning'] not in ('price','fee_rule','amount_role','eligibility_state','management_role'):return
        nxt=self.fact(obj,dest['meaning'],None,None,dest['role'])
        self.logic.rule(nxt,[pre],rule)
        return nxt

    def semantic_questions_for(self,q):
        oid=self.inv.root(q)
        if not oid:return []
        effects=q['current'].get('_scope_effects') or self.by_operation.get(oid,set())
        await_more=set()
        for e in effects:
            if e not in self.effects:continue
            fs=self.for_effect(e)
            for fid in fs:
                m=self.facts[fid]['meaning']
                if m in ('unknown','other_source_meaning','other_source_policy'):
                    await_more.add(e)
        await_more.update(self.disputed_effects(q))
        if not await_more:return []
        return [{'kind':'scoped_support_dispute','affected_effects':sorted(await_more),'id':'dispute_'+digest([oid,sorted(await_more)])[:12],
                 'question':'Clarify the shown meaning on this effect. Correct, narrow or withdraw its support using an applicable source reason.'}]

    def unresolved(self,q):
        if self.disputed_effects(q):return 'conflicting_scoped_meanings'
        for e in self.route_scopes(q):
            if e not in self.effects:continue
            d=self.effects[e]
            if 'cell' not in d:continue
            lookup=self.f.lookup(d['oid']);roots=self.for_effect(e)
            labels={self.facts[f]['meaning'] for f in roots}
            quantity_only='amount_role' in labels and not labels.intersection(RESOURCE) and q['current'].get('_semantic_consumer')
            if self.withdrawn_dependency(e) or quantity_only or 'unknown' in labels and not labels-{'unknown','other_source_meaning','other_source_policy'}:
                if keys(d['cell']) and holder(d['cell'],lookup) is not None:
                    from .ledger import _unit_origin
                    if _unit_origin(self.inv.backend,d['oid'],d['cell']) is None:return 'source_unit_missing'
        return None

```
