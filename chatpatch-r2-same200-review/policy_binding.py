"""Scope source explanations before compiling an authorization predicate.

The source signature is derived from the located explanation and the applied
entry's committed paths. The compiled signature is read back from the IR.
Only the supported equivalences of boolean literals and ordered cells are used.
"""
import re

from pr_next_joint.frontend.path_ir import key, lit, op
from pr_next_joint.frontend.storage import keys, value_type
from pr_next_joint.frontend.source_entry_identity import function_kind
from .key_roles import relation as key_role


def mentioned(text, name):
    return bool(name and re.search(r'(?<![\w$])' + re.escape(name) + r'(?![\w$])', text))


def positive_role_reference(text, name):
    """A denial of the relevance of a named role is not a policy in its favour."""
    for part in re.split(r'[;；,，]|(?<=[.!?])\s+|\b(?:but|whereas|however)\b', text, flags=re.I):
        if not mentioned(part, name):
            continue
        qualifier=r'(?:[A-Za-z_$][\w$]*\.)*' if '.' not in name else ''
        token = r'(?<![\w$])' + qualifier + re.escape(name) + r'(?![\w$])'
        denial = (r'\b(?:no|not|without|neither)\s+(?:(?:the|an?|any|require[sd]?|requiring|need[s]?|be|being)\s+){0,4}'
                  + token + r'|' + token + r'.{0,28}\b(?:not (?:required|needed|applicable)|irrelevant)\b')
        if not re.search(denial, part, re.I):
            return True
    return False


def creation_source(text, entry, operations):
    """Bind normative deployment language to its subject, not a distant use."""
    name = entry['function'].split('(')[0]
    names = {o['function'].split('(')[0] for o in operations.values() if o['target']==entry['target']}
    focus = set()
    for clause in re.split(r'[;；，,]|(?<=[.!?。])\s+|\b(?:but|whereas|however)\b', text, flags=re.I):
        creation = re.search(r'\b(?:deployment.only|only (?:at|during) (?:construction|creation|deployment)|'
                             r'(?:intended|meant|supposed|required|should|must)\b.{0,38}\b(?:constructor|deployment|creation)\b|'
                             r'constructor.only|constructor\s+(?:only|semantics))', clause, re.I)
        # Objects listed as effects after "deployment-only" are not the
        # grammatical subject of that restriction.
        head=clause[:creation.start()] if creation else clause
        found={n for n in names if mentioned(head,n)}
        if found:
            focus=found
        elif not re.search(r'\b(?:it|this|the function|required|authorization|deployment.only)\b',clause,re.I):
            focus=set()
        if focus=={name} and creation:
            return clause.strip()
    return None


def boolean_leaf(term):
    """Return the storage atom and truth value for one committing-path guard."""
    if not isinstance(term, dict):
        return None
    if term.get('kind')=='storage':
        return term, True
    args=term.get('args', [])
    if term.get('op') in ('!', 'not') and len(args)==1:
        child=boolean_leaf(args[0])
        return (child[0], not child[1]) if child else None
    if term.get('op') in ('==','!=') and len(args)==2:
        for atom,const in (args, reversed(args)):
            if const.get('kind')=='literal' and type(const.get('value')) is bool:
                child=boolean_leaf(atom)
                if child:
                    return child[0], child[1] == (const['value'] == (term['op']=='=='))
    return None


def conjuncts(term):
    if term.get('op') in ('&&','and'):
        return [a for v in term['args'] for a in conjuncts(v)]
    return [term]


def stated_boolean(text,name):
    token=r'(?<![\w$])'+re.escape(name)+r'(?![\w$])'
    sub=token+r'(?:\s*\[[^\]]+\]){0,3}'
    values=set()
    if re.search(r'!\s*'+sub,text) or re.search(sub+r'\s*(?:==|is|must be)\s*false\b',text,re.I):
        values.add(False)
    if re.search(sub+r'\s*(?:==|is|must be)\s*true\b',text,re.I):
        values.add(True)
    collective=re.search(r'\bboth\s+(?:be\s+)?(true|false)\b',text,re.I)
    if collective and mentioned(text,name):values.add(collective[1].lower()=='true')
    return values


def payment_policy(text, role_name, scope_names):
    """Read the asserted relation between actual role and payment operands."""
    pay = r'\b(?:payment|paying|paid|fee)\b'
    role = r'(?<![\w$])' + re.escape(role_name.lower()) + r'(?![\w$])'
    names = {n.lower() for n in scope_names if n}
    relations = set()
    text = re.sub(r'["“][^"”]*["”]|(?<!\w)\x27[^\x27\n]+\x27(?!\w)', ' ', text.lower())
    for sentence in re.split(r'[;；。!?\n]|(?<=\.)\s+', text):
        payment_subject = False
        # A role-only requirement in a following contrastive clause still
        # qualifies an earlier claimed payment permission in this sentence.
        sentence_mentions_payment = bool(re.search(pay, sentence))
        for clause in re.split(r'\b(?:but|whereas|however)\b', sentence):
            clause = clause.strip(' ,.'); scoped = re.search(r'\b(?:policy|rule) (?:for|of|on) (?:the )?([\w.$]+)', clause)
            if scoped and scoped[1].split('.')[-1] not in names | {'entry','effect','action','operation'}:
                continue
            if re.search(r'\b(?:implementation|implemented|hypothetically|supposed|mistakenly|incorrectly)\b', clause):
                continue
            if payment_subject and re.match(r'^it\b', clause):
                clause = 'payment' + clause[2:]
            clause = re.sub(r'^(?:under|according to) (?:the )?(?:policy|rule)(?: for [\w.$]+)?,\s*', '', clause)
            payment_subject = bool(re.match(r'^(?:(?:the|a|threshold|qualifying)\s+)*'+pay, clause))
            mentions_pay = bool(re.search(pay, clause))
            if re.search(r'\b(?:unclear|unresolved|unknown|uncertain|whether|undetermined)\b', clause):
                if mentions_pay: relations.add('unresolved')
                continue
            # Modal qualifiers qualify the entitlement itself. An additional
            # condition of unknown meaning cannot yield unrestricted permission.
            restricted = re.search(r'\b(?:if|unless|provided|subject to|except|conditional on)\b',clause)
            same_effect = any(mentioned(clause,n) for n in names) or re.search(r'\b(?:this|same) (?:action|effect|entry)\b',clause)
            exclusive = re.search(r'\bonly\s+(?:(?:the|a|current|authorized|incumbent)\s+)*'+role+
                                  r'(?:\s+holder)?\s+(?:may|can|must|is (?:authorized|permitted) to)\s+\w+',clause)
            if exclusive and not restricted and not re.search(r'\b(?:not|denies|rejects?)\s+$',clause[:exclusive.start()]):
                if same_effect or re.search(r'\b(?:authorize|approve)$',clause):
                    relations.add('role_required')
            if not mentions_pay:
                # Do not let 'payment can substitute, but callers must ALSO
                # hold the office' become an unconditional OR authorization.
                # This expresses a conflict with a purported independent
                # alternative; it does not prove a new authorization policy.
                caller_requires_role = re.search(
                    r'\b(?:caller|applicant|requester)\b.{0,35}\b'
                    r'(?:must|shall|needs? to|is required to)\s+(?:also\s+)?'
                    r'(?:be\s+)?(?:the\s+)?'+role, clause)
                role_is_required = re.search(role+r'\s+(?:is|remains)\s+'
                    r'(?:also\s+)?(?:required|necessary|mandatory)\b', clause)
                if sentence_mentions_payment and (caller_requires_role or role_is_required):
                    relations.add('role_required')
                continue
            policy = re.match(r'^(?:(?:the|this|applicable|approved|authorization|stated|intended|business)\s+)*'
                              r'(?:policy|rule)(?:\s+(?:for|of|on)\s+[\w.$()]+)?\s+'
                              r'(?:(?:expressly|explicitly|strictly|specifically)\s+)?'
                              r'(?:(?:does|can|may)\s+)?'
                              r'(?:(?:expressly|explicitly|strictly|specifically)\s+)?'
                              r'(?P<neg>not\s+|never\s+)?(?P<verb>allows?|permits?|accepts?|forbids?|rejects?|requires?)\b(?P<object>.*)',clause)
            obj = policy['object'] if policy else clause
            has_role = bool(re.search(role,obj))
            joint = has_role and (re.search(r'\b(?:only\s+)?(?:in addition to|together with|in conjunction with)\b',obj)
                    or re.search(r'\bboth\b.+\band\b',obj) and
                    (re.search(r'\b(?:required|necessary|needed)\b',obj) or policy and policy['verb'].startswith('require')))
            denied = bool(policy and (bool(policy['neg']) != policy['verb'].startswith(('forbid','reject'))))
            denies_alternative = re.search(r'\b(?:not|never)\s+(?:as\s+)?(?:an?\s+)?(?:alternative|substitute|authorization|qualification)\b',obj)
            normative_joint = bool(policy or same_effect and re.search(r'\b(?:must|required|necessary|needed)\b',obj))
            either_or = bool(has_role and re.search(r'\beither\b.+\bor\b',obj))
            if joint and normative_joint:
                negated_joint = re.search(r'\b(?:not|never)\s+(?:only|together|required|necessary|needed)\b',obj)
                relations.add('unresolved' if restricted or denied or negated_joint or either_or else 'joint')
                continue
            if not policy and not payment_subject: continue
            if policy and policy['neg'] and policy['verb'].startswith(('forbid','reject')):
                relations.add('unresolved')
                continue
            if restricted or re.search(r'\bonly\b(?! (?:the|a|current) )',obj):
                relations.add('unresolved')
                continue
            alternative = re.search(r'\b(?:alternative|either\b.+\bor|in place of|instead of|replace[sd]?|substitut\w*)\b',obj)
            authority = re.search(r'\b(?:authoriz\w*|sufficient|qualif\w*|constitut\w* authorization)\b',obj)
            if not alternative and not authority: continue
            if payment_subject:
                # Only a predication about the payment establishes its force.
                atom = re.match(r'^(?:(?:the|a|qualifying|threshold)\s+)*'+pay+
                                r'(?:\s+(?:the\s+)?threshold)?(?:\s+(?:alone|itself|independently))?\s+'
                                r'(?:(?:does|can|is|may)\s+)?(?P<sign>not\s+|never\s+|cannot\s+)?'
                                r'(?:independently\s+)?(?:authoriz\w*|sufficient|a qualification|constitut\w*|replace\w*|substitut\w*)\b',obj)
                if not atom: continue
                denied = bool(atom['sign'])
            if denied or denies_alternative:
                relations.add('role_required')
            elif policy and policy['verb'].startswith('require'):
                # Being required makes payment necessary; it need not authorize on its own.
                relations.add('independent' if either_or else 'unresolved')
            elif alternative or authority and re.search(r'\b(?:as authorization|to authorize|sufficient|authorizes?|constitut\w* authorization)\b',obj):
                relations.add('independent')
            else:
                relations.add('unresolved')
    if 'unresolved' in relations or 'independent' in relations and len(relations)>1:
        return 'unresolved'
    return next((mode for mode in ('joint','role_required','independent') if mode in relations),None)


def scoped_payment_denial(text, role_name, entry_name, scope_names):
    """Allow role inference only for an explicit policy denying pay on THIS effect.

    The inferred role is a *necessary* guard operand, never a free-standing
    authorization source. Vague claims, alternate authorities or statements
    about a different effect do not qualify.
    """
    if not entry_name or mentioned(text, role_name):
        return False
    clauses = [v.strip() for v in re.split(r'[;；\n]|(?<=[.!?。])\s+', text) if v.strip()]
    if len(clauses) != 1:
        return False
    clause = clauses[0]
    if not mentioned(clause, entry_name) or not re.search(r'\b(?:policy|rule)\b', clause, re.I):
        return False
    # No inference across competing, conditional or hypothetical policy claims.
    if re.search(r'\b(?:but|however|whereas|unless|except|provided|subject to|'
                 r'unknown|unclear|whether|hypothetically|instead|another|other|either|if)\b', clause, re.I):
        return False
    # A second claimed authorizer in the same sentence must not be silently
    # erased by assuming the observed role is the only legitimate source.
    if re.search(r'\band\b.{0,100}\b(?:authoriz\w*|qualif\w*|approv\w*|permitt\w*|grant\w*)\b',
                 clause, re.I):
        return False
    return payment_policy(clause, role_name, scope_names) == 'role_required'


def role_payments(rows, lookup, text, subject=None, *, derive_role_from_source=False):
    """Find actual alternative operands. Their occurrence proves no business permission.

    `derive_role_from_source` may only be used after independently checking a
    narrowly scoped normative payment exclusion and one stable source role.
    """
    scoped = {}
    for _, path in rows:
        for guard in path['guards']:
            for disj in conjuncts(guard):
                if disj.get('op') not in ('or','||') or len(disj.get('args',())) != 2:
                    continue
                for role, condition in (disj['args'], reversed(disj['args'])):
                    args = role.get('args', ())
                    if role.get('op') != '==' or not any(t.get('kind')=='actual_sender' for t in args):
                        continue
                    cell = next((t for t in args if t.get('kind')=='storage' and not keys(t)), None)
                    if not cell or (cell != subject if subject is not None else
                                    not derive_role_from_source and not positive_role_reference(
                                        text, lookup.nodes[cell['root']].get('name'))):
                        continue
                    pay = condition.get('args', ())
                    if len(pay)!=2 or condition.get('op') not in ('>=','>','<=','<'):
                        continue
                    value, threshold = pay if condition['op'] in ('>=','>') else reversed(pay)
                    if value.get('kind')=='transaction_value' and threshold.get('kind') in ('literal','storage'):
                        scoped[key([role,condition,cell])] = (role,condition,cell)
    return list(scoped.values())


def source_requirement(inv, q, explanation, rows):
    entry=inv.f.operations[inv.root(q)]
    lookup=inv.f.lookup(inv.root(q))
    declaration=lookup.nodes.get(entry['source'].get('ast_id'),{})
    text=str(explanation.get('text') or explanation.get('basis') or '')
    signature={'target':entry['target'],'operation':inv.root(q),'declaration':declaration.get('id'),
               'frame':'before_effect','path_sources':[pid for pid,_ in rows]}
    clause=creation_source(text,entry,inv.f.operations)
    if clause and declaration.get('nodeType')=='FunctionDefinition' and function_kind(declaration)!='constructor':
        return dict(signature,kind='creation_only_source_policy',clause=clause,frame='runtime entry')
    # Use the already source-derived role of each ordered key, never a function name.
    grants={}
    if re.search(r'\b(?:allowance|grant|approval|spender)\b|额度|受托|授权额度',text,re.I):
        for _,p in rows:
            for write in p['writes']:
                cell=write['path']
                role=key_role(cell,lookup)
                if role and role['kind']=='authorization_quantity':
                    idx=keys(cell)
                    if len(idx)==2:
                        h=role['holder_key']
                        grants[key(cell)]={'cell':cell,'issuer':idx[h],'spender':idx[1-h],'quantity':write['value']}
    own=re.search(r"\b(?:own|self|issuer|holder.s|on behalf of|someone else.s|another holder.s)\b|本人|持有人",text,re.I)
    additional_policy=any(positive_role_reference(text,n['name']) for n in lookup.decls.values()
                          if n.get('stateVariable') and n.get('name') and
                          (n.get('typeDescriptions',{}).get('typeString') or '').startswith('address'))
    if grants and own and len(grants)==1 and not additional_policy:
        return dict(signature,kind='source_grant_issuer',grant=next(iter(grants.values())))
    # A named source check identifies its precise relation only if every
    # committing branch agrees. Do not promote a branch-specific atom.
    if not rows:
        return None
    # Both interfaces use the same normative relation and the same source operands.
    typed = explanation.get('explicit_policy_kind') == 'current_authority_required'
    entry_name = entry['function'].split('(')[0]
    names = {entry_name} | {lookup.nodes.get(w['path']['root'],{}).get('name')
                            for _, path in rows for w in path['writes']}
    candidates = role_payments(rows, lookup, text, explanation.get('qualified_cell') if typed else None)
    if not candidates and not typed and rows:
        # A legacy issue can locate the exact effect without repeating the
        # source role's identifier. Only derive that role when (a) the policy
        # explicitly excludes payment as authorization for THIS entry, and
        # (b) every committing path has the same unique role-or-pay guard.
        # The derived role is a necessary authorization prerequisite, not a
        # proof that this role alone is sufficient for any other effect.
        inferred = role_payments(rows, lookup, text, derive_role_from_source=True)
        if len(inferred) == 1:
            role, payment, cell = inferred[0]
            role_name = lookup.nodes[cell['root']].get('name')
            same_in_all_paths = all(
                len(row_candidates := role_payments([(pid, path)], lookup, text,
                    derive_role_from_source=True)) == 1 and key(row_candidates[0]) == key(inferred[0])
                for pid, path in rows)
            if same_in_all_paths and scoped_payment_denial(text, role_name, entry_name, names):
                candidates = inferred
    if candidates:
        role, payment, cell = candidates[0]
        sign = (explanation.get('payment_policy') or 'role_required') if typed else payment_policy(text, lookup.nodes[cell['root']]['name'],names)
        if sign in ('independent','joint','role_required') and len(candidates) == 1:
            return dict(signature,kind='source_role_payment_policy',role=role,payment=payment,subject=cell,
                        payment_relation=sign, permits_payment=sign=='independent')
        # Describing the actual guard or naming its role is insufficient to
        # select one of its authorization branches as the governing rule.
        return dict(signature,kind='unresolved_role_payment_policy')
    if typed and explanation.get('payment_policy') in ('unresolved','independent','joint'):
        return dict(signature,kind='unresolved_role_payment_policy')
    paths=[]
    for _,p in rows:
        atoms={}
        for guard in p['guards']:
            for term in conjuncts(guard):
                leaf=boolean_leaf(term)
                if not leaf:continue
                cell,truth=leaf
                if keys(cell) and value_type(cell,lookup)=='bool' and mentioned(text,lookup.nodes[cell['root']].get('name')):
                    atoms[key([cell,truth])]=(cell,truth)
        paths.append(atoms)
    if paths[0] and all(set(p)==set(paths[0]) for p in paths):
        atoms=[]
        for c,observed in paths[0].values():
            name=lookup.nodes[c['root']].get('name')
            truths=stated_boolean(text,name)
            if len(truths)>1:return None
            observed_normal=(explanation.get('meaning')=='normal_authorization' and
                re.search(r'\b(?:own|self|msg\.sender.s)\b',text,re.I) and
                re.search(r'\b(?:checks?|requires?|subject to)\b',text,re.I))
            if not truths and not observed_normal:return None
            truth=next(iter(truths)) if truths else observed
            atoms.append({'cell':c,'permitted_truth':truth,'observed_guard_truth':observed,
                'basis':'explicit_source_bound_condition' if truths else 'stated_normal_use_subject_to_actual_check'})
        return dict(signature,kind='source_guarded_eligibility',atoms=atoms)
    return None


def compile_requirement(requirement,explanation,lookup):
    kind=requirement['kind']
    subject=None
    if kind=='source_role_payment_policy':
        subject=requirement['subject']
        mode=requirement['payment_relation']
        predicate=requirement['role'] if mode=='role_required' else op(
            'and' if mode=='joint' else 'or', requirement['role'], requirement['payment'])
    elif kind=='source_grant_issuer':
        subject=requirement['grant']['issuer']
        predicate=op('==',{'kind':'actual_sender'},subject)
    elif kind=='source_guarded_eligibility':
        terms=[a['cell'] if a['permitted_truth'] else op('!',a['cell']) for a in requirement['atoms']]
        predicate=terms[0] if len(terms)==1 else op('and',*terms)
        if len(terms)==1:subject=requirement['atoms'][0]['cell']
    else:
        predicate=lit(False)
    return {'predicate':predicate,'subject':subject,'kind':kind,'property_family':'use',
            'normal_alternatives':[],'source_bound_alternatives':[],'business_basis':explanation,
            'necessary_only':kind=='source_role_payment_policy' and requirement['payment_relation']!='independent',
            'acquisition_uses':[],'binding':{'declaration':requirement['declaration'],'frame':requirement['frame'],
            'source':lookup.anchor(lookup.nodes[requirement['declaration']])},'source_requirement':requirement}


def compare_requirement(required,compiled,entry_id,declaration,target):
    """Check independent source facts against the expression consumed by M4."""
    p=compiled.get('predicate') or {}
    binding=compiled.get('binding') or {}
    scope_ok=(entry_id==required['operation'] and target==required['target'] and
              binding.get('declaration')==declaration==required['declaration'] and binding.get('frame')==required['frame'])
    if required['kind']=='source_role_payment_policy':
        mode=required['payment_relation']
        if mode=='role_required':
            actual,wanted=key(p),key(required['role'])
        else:
            actual=[p.get('op'),sorted(key(t) for t in p.get('args',[]))]
            wanted=[{'joint':'and','independent':'or'}[mode],sorted(key(required[t]) for t in ('role','payment'))]
        equal=actual==wanted and compiled.get('necessary_only')==(mode!='independent')
    elif required['kind']=='source_guarded_eligibility':
        leaves=[boolean_leaf(t) for t in conjuncts(p)]
        actual=sorted(key([c,b]) for leaf in leaves if leaf for c,b in [leaf])
        wanted=sorted(key([a['cell'],a['permitted_truth']]) for a in required['atoms'])
        equal=len(actual)==len(leaves) and actual==wanted
    elif required['kind']=='source_grant_issuer':
        actual=sorted(key(t) for t in p.get('args',[]))
        wanted=sorted(key(t) for t in ({'kind':'actual_sender'},required['grant']['issuer']))
        equal=p.get('op')=='==' and actual==wanted
    else:
        actual=[p.get('kind'),p.get('value'),compiled.get('acquisition_uses')]
        wanted=['literal',False,[]]
        equal=actual==wanted and type(p.get('value')) is bool
    return {'matches':scope_ok and equal,'scope_matches':scope_ok,'source':wanted,'compiled':actual,
            'frame':binding.get('frame'),'operator':p.get('op',p.get('kind'))}


def audit_authorization(f,oid,compiled):
    """Recheck at consumption, including each independently scoped alternative."""
    if not isinstance(compiled,dict):return []
    alternatives=compiled.get('competing_interpretations')
    if alternatives:
        expected=[p['predicate'] for p in alternatives]
        actual=compiled.get('predicate',{})
        results=[r for p in alternatives for r in audit_authorization(f,oid,p)]
        results.append({'matches':actual.get('op')=='or' and
                        sorted(map(key,actual.get('args',[])))==sorted(map(key,expected)),
                        'scope':'surviving_source_interpretations'})
        return results
    requirement=compiled.get('source_requirement')
    if not requirement:return []
    op_info=f.operations[oid]
    return [compare_requirement(requirement,compiled,oid,op_info['source'].get('ast_id'),op_info['target'])]


def source_excludes_violation(f,oid,compiled):
    """A local proof over all the located committing paths, for this policy only."""
    required=compiled.get('source_requirement') or {}
    # A source-scoped before/after check for a stage flag: once it is true,
    # setting that identical cell to true cannot commit the prohibited change.
    # Independent sibling effects have separate policy/coverage consumers.
    scoped=compiled.get('effect_write')
    if compiled.get('kind')=='scope_bound_initialization_stage' and scoped and not compiled.get('competing_interpretations'):
        cell=scoped['cell']
        if key(cell)!=key(compiled.get('subject')) or compiled.get('predicate')!=op('!',cell):return None
        path=next((p for pid,p in f.operation_paths(oid,True) if pid==scoped['path']),None)
        if not path or path.get('issues') or path.get('evaluation_gaps') or path.get('sensitive_effects'):return None
        writes=[w for w in path['writes'] if w['path'].get('root')==cell['root']]
        if not writes or any(w['path']!=cell for w in writes) or writes[-1]['value']!=lit(True):return None
        return {'basis':'already_set_stage_flag_has_no_further_net_change','source_identity':f.identity,'operation':oid,
                'target':f.operations[oid]['target'],'paths':[scoped['path']],'scope':'only the bound stage flag',
                'other_policies_or_effects_closed':False}
    if compiled.get('competing_interpretations') or required.get('kind') not in ('source_grant_issuer','source_guarded_eligibility'):
        return None
    paths=list(f.operation_paths(oid))
    if not paths or f.operations[oid].get('gaps') or any(
            p['flow'] not in ('normal','returned','reverted') or p.get('issues') or p.get('evaluation_gaps')
            for _,p in paths):return None
    commits=[(pid,p) for pid,p in paths if p['flow'] in ('normal','returned')]
    if not commits or set(required['path_sources'])!={pid for pid,_ in commits}:return None
    if required['kind']=='source_grant_issuer':
        issuer=required['grant']['issuer']
        if issuer!={'kind':'actual_sender'}:return None
        cell=required['grant']['cell']
        # Other state updates/effects require independent policies.
        if any(p.get('sensitive_effects') or any(key(w['path'])!=key(cell) for w in p['writes']) for _,p in commits):
            return None
        reason='exact_caller_owns_written_grant_key'
    else:
        needed={key([a['cell'],a['permitted_truth']]) for a in required['atoms']}
        for _,p in commits:
            actual=set()
            for g in p['guards']:
                for t in conjuncts(g):
                    leaf=boolean_leaf(t)
                    if leaf:actual.add(key(list(leaf)))
            if not needed<=actual:return None
        reason='authorized_boolean_condition_is_necessary_on_each_committing_path'
    return {'basis':reason,'source_identity':f.identity,'operation':oid,'target':required['target'],
            'paths':[pid for pid,_ in commits],'scope':'only this use of this source-verified policy',
            'other_policies_or_effects_closed':False}
