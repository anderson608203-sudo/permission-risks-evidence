# 实跑源码文本 · 第 13 页

## file-3a88e176692f41

`source/src/pr_next_joint/investigation/quantity_checks.py` · 原字节 SHA-256 `76494dba6b641ba95e676747c13fbececaef8582867bb370487c1fd1139a079f`

~~~~python
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

~~~~

## file-97040322171b99

`source/src/pr_next_joint/investigation/relations.py` · 原字节 SHA-256 `99363b9f2add2df626519580a2ee0e621428b6414e2d2ad4dec7d63d0abb0bdf`

~~~~python
"""Source-bound semantic relations shared by property formation and feedback."""
import copy
import re
from pr_next_joint.frontend.path_ir import key, op, lit, walk
from pr_next_joint.frontend.storage import keys, selectors, value_type
from .policy_binding import source_requirement, compile_requirement, compare_requirement, positive_role_reference


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
        "guard_is_execution_fact_not_policy": True,
    }


def policy(item):
    text = str(item.get("policy_basis") or item.get("claim") or "")
    if not text.strip() or item.get("_host_source_question"):
        return None
    row = statement(text)
    if (item.get('assessment')=='normal' and row['meaning']!='unknown'
            and re.search(r"\b(?:own|self|msg\.sender.s)\b",text,re.I)
            and re.search(r"\b(?:checks?|subject to|self.service)\b",text,re.I)
            and not re.search(r'\b(?:bypass(?:es)?|unauthorized|without consent)\b',text,re.I)):
        row['meaning']='normal_authorization'
    row["source_anchors"] = copy.deepcopy(item.get("anchors", []))
    row["level"] = "H"
    return row


def _exact_name(text, name):
    return bool(name and re.search(r"(?<![\w$])" + re.escape(name) + r"(?![\w$])", text))


def authorization(inv, q, explanation):
    if not explanation or explanation.get("meaning") == "unknown":
        return None
    f = inv.f
    oid = inv.root(q)
    lookup = f.lookup(oid)
    text = explanation.get("text", explanation.get("basis", ""))
    # Binding an intended policy is distinct from proving a committing path.
    # A known write before an unresolved call still identifies the issuer or
    # stage. The actual query separately retains that call's exit/residual.
    rows = [(pid,p) for pid,p in f.operation_paths(oid) if p['flow'] in ('normal','returned')]
    declaration = lookup.nodes.get(f.operations[oid]['source'].get('ast_id'), {})
    required = source_requirement(inv,q,explanation,rows)
    if required:
        compiled = compile_requirement(required,explanation,lookup)
        match = compare_requirement(required,compiled,oid,declaration.get('id'),f.operations[oid]['target'])
        compiled['source_ir_check'] = match
        if not match['matches']:
            q['authorization_binding_diagnostic'] = {'reason':'source_ir_disagreement','comparison':match}
            return None
        return compiled
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
        if (_exact_name(text, declaration.get('name')) or
                _exact_name(text, owner_name + '.' + declaration.get('name', ''))):
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
        if any(o and positive_role_reference(text,o+'.'+n.get('name','')) for o in qualifiers):
            qualified.append(c)
        elif positive_role_reference(text, n.get("name")):
            named.append(c)
    explicit = qualified or named
    modifier_subjects = []
    body = lookup.nodes.get(f.operations[oid]['source'].get('ast_id'), {})
    for call in body.get('modifiers', []):
        modifier = lookup.nodes.get(call.get('modifierName', {}).get('referencedDeclaration'), {})
        if not _exact_name(text, modifier.get('name')):
            continue
        roots = {n.get('referencedDeclaration') for n in walk(modifier) if isinstance(n,dict)}
        for _, path in rows:
            for guard in path['guards']:
                if not any(v.get('kind') == 'actual_sender' for v in walk(guard)):
                    continue
                modifier_subjects += [c for c in selectors(guard) if c['root'] in roots and not keys(c) and
                                     value_type(c,lookup) in ('address','address payable')]
    guard_subjects = re.findall(r"\b(?:checks|reads|requires)\s+([A-Za-z_$][\w$]*\.[A-Za-z_$][\w$]*)", text)
    exact_guard = [c for c in qualified if any(
        lookup.nodes.get(lookup.nodes[c['root']].get('scope'),{}).get('name','') + '.' + lookup.nodes[c['root']].get('name','') == n
        for n in guard_subjects)]
    subjects = re.findall(r"\b(?:only|required(?: by| from)?|authorized by|permission (?:of|from))\s+(?:(?:an?|the|authorized|existing)\s+)*'?([A-Za-z_$][\w.$]*)", text, re.I)
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
    if subjects and not described and not modifier_subjects and not exact_guard and not qualified and any(
            s.lower() in ('owner','handler','admin','administrator','controller') for s in subjects):
        q['authorization_binding_diagnostic']={'reason':'described_authority_has_no_matching_source_declaration',
            'described_subjects':subjects,'mentioned_state_is_not_automatically_the_authority':True}
        return None
    kind = "authority_before_effect"
    if len(candidates) == 1:
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
    for _, path in rows:
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
    for _, path in rows:
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
    return {"predicate": op("or", *list({key(x): x for x in allow}.values())),
            "subject": subject, "kind": kind, "normal_alternatives": allow[1:],
            "source_bound_alternatives": alternatives, "business_basis": explanation,
            "acquisition_uses": acquisition, "property_family": "acquire" if acquisition or acquisition_intent else "use",
            "binding": {"original_relation": text, "declaration": subject.get("root"), "frame": "before_effect",
                        "source": lookup.anchor(lookup.nodes[subject["root"]]) if subject.get("root") in lookup.nodes else None}}


def beneficiary_condition(encoder, frame, position, holder):
    """Conditional ability with all original source address restrictions."""
    caller = encoder.expr(frame["caller"])
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
        return holder != 0, {"kind": "selectable_self_controlled_address",
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

~~~~

## file-2904541f32164b

`source/src/pr_next_joint/investigation/report.py` · 原字节 SHA-256 `2b3e0d642b55ead7e45b67aa09f7bca6c46cf77ca066dc6eeb36bb61fb806ea7`

~~~~python
"""Source-backed risk prediction, scoped hard counterevidence and dependency output."""
import copy,re
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import walk,key
from pr_next_joint.frontend.storage import selectors,keys,value_type,selector_relation
from .contracts import VERSION,CATEGORIES
from .protocol import category_scope
from .request_scope import coverage_facts, observation_applies, compare_relevant, linked_controls



def evaluate(inv,q):
    from .property_model import planning_item,compose
    inv.semantics.scope(q['current'])
    return compose(inv,q,None)

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
        unknown={'source_identity_ambiguous_or_unresolved','minimum_source_inspection_not_executed',
           'unique_critical_external_guard_not_established','signature_dependent_success_not_verified',
            'E1_cumulative_numeric_bound_mapping_pending','semantic_task_direction_conflict','financial_intervention_source_unresolved',
            'property_task_meaning_unresolved','expected_authorization_not_established','financial_property_conditions_not_established',
            'changed_business_effect_requires_source_rebinding','normal_authorization_source_scope_unresolved'}
        hard={'original_root_has_no_committing_path','original_root_net_effect_is_unchanged',
              'same_scope_actual_full_settlement','single_holder_scope_not_collective_pause','same_control_has_no_dependency_on_declared_entry_effect',
              'matched_direct_effect_impossible_on_all_applicable_positions_and_paths'}
        if set(assessment['reasons'])&unknown and assessment['category'] in CATEGORIES:blocked_categories.add(assessment['category'])
        decisive=(assessment['reportable'] or
                  bool(set(assessment['reasons'])&hard) and not set(assessment['reasons'])&unknown)
        if decisive and not q.get('task_conflict'):decisive_records.append(qid)
        mapping=assessment['scope'].get('comparison_alignment',{})
        if mapping.get('status')=='unresolved' and item['assessment']=='risk' and assessment['category'] in CATEGORIES:blocked_categories.add(assessment['category'])
        if not assessment['reportable']:
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
        identity=[inv.f.identity,assessment['category'],o['target'],location,assessment['scope'].get('claim_identity'),item.get('object'),item.get('actor'),
                  item.get('phase'),item.get('scope'),item.get('assumptions'),None if fine else ' '.join(item['claim'].split())]
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
    return {'method':VERSION,'program_identity':inv.f.identity,'task':inv.f.options.scope,'options':inv.f.options.record(),
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
        'task_analysis':{'model_analysis_available':inv.model_analysis_available,
            'empty_response_present':inv.explicit_empty_analysis,
            'explicit_empty_task_reading':bool(inv.explicit_empty_analysis and scope['whole_reading_eligible']),
            'model_declaration':inv.task_declaration,'reading_scope':scope,'local_judgment_not_global_safety':True,
            'unexecuted_actions':len(inv.ready),'task_conflicts':[qid for qid,q in inv.issues.items() if q.get('task_conflict')]},
        'model_reading_declarations_not_proof':inv.reading_declarations,
        'usage':{'attempts':copy.deepcopy(inv.session.attempts),**inv.session.accounting()},
        'provenance':{'source_candidate_investigations':copy.deepcopy(getattr(inv,'candidate_trace',[])),'actions':copy.deepcopy(inv.actions),'revisions':copy.deepcopy(inv.updates),
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
    if not obligations:eligible.clear()
    if report.get('method')==VERSION:
        states={c:'alarm' if c in found else 'not_run' if not active else
                'not_detected' if c in eligible and c not in unknown else 'unsupported' for c in cats}
    else:
        states={c:'alarm' if c in found else 'unsupported' if c in unknown else
                'not_detected' if c in reading.get('negative_eligible_categories',[]) else 'not_run' for c in cats}
    return {'predictions':states,
        'scope':report['diagnostics']['source_context_scope'],
        'coverage_basis':'Finite source obligations, actual semantic/program completion and scoped residuals; delivery/declarations are records, not completion gates.',
        'no_finding_does_not_prove_safety':True,'not_a_score':True,
        'enhancement_unfinished_does_not_erase_source_predictions':True}

~~~~

## file-d32e59d10ed96f

`source/src/pr_next_joint/investigation/request_scope.py` · 原字节 SHA-256 `756330123ee084b1e802e36698d1936dbb089a348121df6485a73306cbc9f6c2`

~~~~python
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


~~~~

## file-e6918aaa5165d6

`source/src/pr_next_joint/investigation/roles.py` · 原字节 SHA-256 `cf7b6d13d1a403a99789140156ab9e3b1694fce42de48a37f1a66e3d229cf169`

~~~~python
"""Source-grounded qualifications for a specific compiled target and committing path."""
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys,selectors


def _roots(node, allowed, positive=True):
    """Return role declarations required by the condition; all arms of a disjunction must qualify."""
    args, op = node.get('args', []), node.get('op')
    if op == '!' and len(args) == 1:
        return _roots(args[0], allowed, not positive)
    if op in ('and', '&&', 'or', '||') and len(args) == 2:
        left, right = (_roots(x, allowed, positive) for x in args)
        conjunction = (op in ('and', '&&')) == positive
        return (left | right) if conjunction or (left and right) else set()
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
    def protected(writer,roots):return set().union(*(_roots(g,roots) for g in writer['guards']))
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
            'qualification_guards':[g for g in w['guards'] if _roots(g,active)]} for w in writers[r]],
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
        ids=_roots(g,registry)
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


~~~~

## file-b233937f097276

`source/src/pr_next_joint/investigation/scope_relevance.py` · 原字节 SHA-256 `f75e1018d5e31e067392454a1fb7ffbe7b5e2a5ce019195f6f74c0083e5bb819`

~~~~python
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
    from .roles import path_qualification, _roots
    if path_qualification(f,oid,path):return True
    lookup=f.lookup(oid)
    allowed={n['id'] for n in lookup.decls.values() if n.get('stateVariable') and
        (n.get('typeDescriptions',{}).get('typeString') in ('address','address payable') or
         n.get('typeName',{}).get('nodeType')=='Mapping')}
    for guard in path['guards']:
        if _roots(guard,allowed):return True
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
            if any(not paired(d,moves['+']) for d in moves['-']):possible.add('FCR-DESTROY')
            if any(not paired(c,moves['-']) for c in moves['+']):possible.add('FCR-MINT')
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
    hard=[g for g in operation.get('gaps',[]) if g.get('kind')=='path_extraction']
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

~~~~
