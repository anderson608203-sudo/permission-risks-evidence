## source/src/pr_next_joint/investigation/policy_binding.py

~~~~python
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


def effect_duty(text):
    """Identify the subject of a responsibility, not the subjects of nearby observations.

    Subject phrases are open vocabulary. Only the positive argument of a
    permission, duty, assignment or required consent can enter source binding.
    """
    if not isinstance(text, str): return None
    roles = []
    qualified = False
    alternative = False
    noun = r"(?P<actor>[\w$][\w$.'’ -]*?)"
    frames = (
        r"\bonly\s+" + noun + r"\s+(?:may|can|is entitled to|is allowed to)\s+\w+",
        r"^(?:only\s+)?" + noun + r"\s+(?:is|are|remains?)\s+(?:solely\s+)?(?:responsible for|entrusted with|authorized to|in charge of)\s+\w+",
        r"^" + noun + r"\s+(?:who\s+)?(?:governs?|has authority over|has the right to decide)\s+\w+",
        r"^" + noun + r"\s+(?:must|shall)\s+(?:also\s+)?(?:consent|authorize|approve)\b",
        r"\b(?:assigns?|entrusts?|reserves?)\s+[^,;.!?]*\b(?:decision|responsibility|approval|authority|right|appointment|discretion)\b[^,;.!?]*?\s+to\s+" + noun + r"$",
        r"\b(?:decided by|authorized solely by)\s+" + noun + r"$",
        r"\b(?:decisions?|authority|responsibility)\s+(?:is|are|remains?)\s+" + noun + r"['’]s(?:\s+\w+)?$",
        r"\bat\s+" + noun + r"['’]s\s+discretion\b",
        r"\b(?:responsibility|right|authority|decision)\b[^;,.]*?\b(?:belongs to|lies with|rests with|is reserved for)\s+" + noun + r"$",
        r"\b(?:requires?|needs?|without)\s+" + noun + r"(?:['’]s|\s+)\s*(?:approval|consent|authorization)\b",
        # "also" adds a prerequisite; it must not make the whole consent
        # clause disappear while a different actor's authority remains normal.
        # Keep it inside the positive requirement grammar, so "not required"
        # and "also not required" do not become affirmative holder consent.
        noun + r"(?:['’]s|\s+)\s*(?:approval|consent|authorization)\s+(?:is\s+(?:also\s+)?(?:required|necessary)|must\s+(?:also\s+)?be\s+obtained)\b",
        r"(?:只有|仅限)\s*(?P<actor>[\w$]+?)\s*(?:有权|才可|才能)",
        r"(?:须经|必须经|应由)\s*(?P<actor>[\w$]+?)\s*(?:同意|授权|批准|决定)",
    )
    for part in re.split(r"[;；。!?，,]|\.(?=\s|$)|\b(?:but|yet|whereas|although|however)\b", text, flags=re.I):
        clause = part.strip()
        # The subject of an executable check describes a precondition. It does
        # not assign the authority to make the business decision.
        if re.match(r"^(?:(?:in|under|according to)\s+)?(?:the\s+)?(?:actual\s+|current\s+|implemented\s+)?(?:implementation|source(?:\s+code)?|code|runtime|guard|[\w$]+\s+(?:guard|check))\b", clause, re.I):
            continue
        restriction = re.search(r"\b(only if|if|unless|provided(?: that)?|subject to|together with|in addition to|as well as|with(?= (?:the )?(?:[\w’'-]+\s+){0,4}(?:consent|approval)))\s+(.*)$", clause, re.I)
        additional = None
        if restriction:
            # Separate the approval of another actor from a condition on the
            # first actor's identity. Unknown qualifiers cannot certify a normal.
            rest = restriction[2]
            if restriction[1].casefold() != 'unless':
                agreed = (re.match(r"(?:the\s+)?(?:consent|approval|authorization)\s+(?:of|from)\s+" + noun + r"$", rest, re.I)
                          or re.match(noun + r"(?:['’]s\s+|\s+)(?:also\s+)?(?:consents?|approves?|authoriz(?:es|ation)|approval)\b", rest, re.I))
                if agreed:
                    additional = agreed['actor']
            clause = clause[:restriction.start()].strip()
            if not clause and roles:
                if additional and not alternative:
                    roles.append(additional)
                else:
                    qualified = True
                continue
        for pattern in frames:
            match = re.search(pattern, clause, re.I)
            if not match:
                continue
            if re.search(r"\b(?:not|never|neither|whether|if)\s+(?:solely\s+)?$", clause[:match.start()], re.I):
                continue
            actor = match['actor'].strip()
            if re.search(r"\b(?:not|never|neither|whether|if|unless)\b", actor, re.I):
                continue
            names = re.split(r"\s+(and|or)\s+", actor, flags=re.I)
            joins = {s.casefold() for s in names[1::2]}
            qualified |= len(joins) > 1 or bool(roles and (alternative or 'or' in joins))
            alternative |= 'or' in joins
            actors = names[::2]
            if restriction:
                if additional:
                    actors.append(additional)
                    qualified |= alternative
                else:
                    qualified = True
            for value in actors:
                value = re.sub(r"^(?:(?:only|the|a|an|same)\s+)+", "", value.strip(), flags=re.I)
                if value and value.casefold() not in ('their','his','her','its','it','they'):
                    if value.casefold() not in [v.casefold() for v in roles]:
                        roles.append(value)
            break
    if not roles:
        return None
    return {'actors': roles, 'alternative': alternative, 'qualified': qualified}


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
    # Retain the payment subject through a nominal complement. The modal
    # predicate below still decides sufficiency, denial and contradictions.
    text=re.sub(r'\bpayment of (?:the |a )?(?:fee|charge)\b','payment',text)
    for sentence in re.split(r'[;；。!?\n]|(?<=\.)\s+', text):
        if re.search(role+r'\s+or\s+(?:an? |the )?(?:customer|holder|caller)\s+paying\b',sentence) and re.search(r'\bmay independently authorize\b',sentence):
            relations.add('independent')
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
            explicit_requirement = re.fullmatch(r'both\s+(?:the\s+)?'+role+
                r"(?:'s)?(?:\s+(?:approval|authorization|consent))?\s+and\s+(?:the\s+)?(?:payment|fee)\s+(?:are|remain)\s+(?:required|necessary)",clause)
            normative_joint = bool(policy or explicit_requirement or same_effect and re.search(r'\b(?:must|required|necessary|needed)\b',obj))
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

~~~~

## source/src/pr_next_joint/investigation/prestate.py

~~~~python
"""Narrow initial-state invariants. Never equate a deployment choice with a current value."""
from functools import lru_cache
from pr_next_joint.frontend.path_ir import walk,key
from pr_next_joint.frontend.storage import selectors


def literal(node):
    if not isinstance(node,dict):return None
    if node.get('nodeType')=='FunctionCall' and node.get('kind')=='typeConversion' and len(node.get('arguments',[]))==1:
        type_name=node.get('expression',{}).get('typeName',{})
        target=type_name.get('name') if isinstance(type_name,dict) else type_name if isinstance(type_name,str) else None
        value=literal(node['arguments'][0])
        if type(value)is not int:return None
        import re
        numeric=re.fullmatch(r'uint(\d*)',target or '')
        width=160 if target in ('address','address payable') else int(numeric[1] or 256) if numeric else None
        return value if width and 0<=value<2**width else None
    if node.get('nodeType')!='Literal':return None
    typ=node.get('kind'); v=str(node.get('value',''))
    if typ in ('bool','boolean') and v in ('true','false'):return v=='true'
    if typ in ('number','hexNumber') and not node.get('subdenomination'):
        try:return int(v.replace('_',''),0)
        except ValueError:return None
    return None


def _legacy_state_facts(lookup):
    if hasattr(lookup,'_relational_initial'):return lookup._relational_initial
    bases=lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
    declarations=[n for b in bases for n in lookup.nodes[b].get('nodes',[])]
    # Assembly, delegate execution or a storage-reference alias can defeat AST write exclusion.
    functions=[n for n in declarations if n.get('nodeType') in ('FunctionDefinition','ModifierDefinition')]
    opaque=any(n.get('nodeType') in ('InlineAssembly','YulBlock') or n.get('memberName') in ('delegatecall','callcode')
         or n.get('nodeType')=='VariableDeclaration' and n.get('storageLocation')=='storage' for fn in functions for n in walk(fn))
    table={}
    for var in declarations:
        typ=var.get('typeDescriptions',{}).get('typeString','')
        if not var.get('stateVariable') or not (typ=='bool' or typ.startswith('uint') or typ in ('address','address payable')):continue
        vid=var['id']; row={'declaration':vid,'name':var['name'],'type':typ,'declaration_source':lookup.anchor(var),
            'origin':'conditional_symbolic','encoded':False}
        table[vid]=row; assigns=[]; runtime=False
        for fn in functions:
            is_ctor=fn.get('kind')=='constructor' or fn.get('isConstructor')
            body=fn.get('body') or {}
            for n in walk(body):
                if n.get('nodeType') not in ('Assignment','UnaryOperation'):continue
                lhs=n.get('leftHandSide') or n.get('subExpression') or {}
                if n.get('nodeType')=='UnaryOperation' and n.get('operator') not in ('++','--','delete'):continue
                if not any(x.get('referencedDeclaration')==vid for x in walk(lhs)):continue
                if is_ctor:assigns.append((fn,n))
                else:runtime=True
        if opaque and not var.get('constant'):row['limit']='indirect storage writes not excluded';continue
        if runtime:
            row['origin']='constructor_choice_with_possible_later_write' if assigns else 'conditional_state_with_source_writer'
            row['constructor_sources']=[lookup.anchor(n) for _,n in assigns]
            continue
        v=literal(var.get('value'))
        if var.get('value') is None:v=False if typ=='bool' else 0
        if not assigns:
            if v is not None:row.update(origin='fixed_declared_initializer' if var.get('value') is not None else 'fixed_type_default',value=v,encoded=True)
            continue
        row['origin']='constructor_configuration';row['writes']=[lookup.anchor(n) for _,n in assigns]
        if len(assigns)!=1:continue
        ctor,assignment=assigns[0]
        direct={st.get('expression',{}).get('id') for st in (ctor.get('body') or {}).get('statements',[]) if st.get('nodeType')=='ExpressionStatement'}
        if assignment['id'] not in direct or assignment.get('operator')!='=' or ctor.get('modifiers'):continue
        rhs=assignment.get('rightHandSide') or {}; v=literal(rhs)
        if v is not None:row.update(origin='fixed_constructor_literal',value=v,encoded=True)
        elif rhs.get('memberName')=='sender' and rhs.get('expression',{}).get('name')=='msg':
            row.update(origin='fixed_deployer_address',nonzero=True,encoded=True)
    lookup._relational_initial=table
    return table


def state_facts(lookup, selected_domain=None):
    from .initial_state import domain,initial_for_lookup,CAPABILITY,DEPLOYMENT
    from .state_encoding import _initial_term
    from pr_next_joint.verification.sequence import read
    selected_domain=selected_domain or domain(lookup)
    if selected_domain not in (CAPABILITY,DEPLOYMENT):return _legacy_state_facts(lookup)
    model=initial_for_lookup(lookup)
    if model is None:return {}
    cache=lookup.__dict__.setdefault('_domain_state_facts',{})
    token=(selected_domain,model['identity'])
    if token in cache:return cache[token]
    from .initial_state import family
    context={**model,'_lookup':lookup,'_amount_families':{family(r['cell']) for r in model['candidate_amount_leaves']}}
    table={}
    clean=[p for p in model['constructor_paths'] if p['flow'] in ('normal','returned') and not p.get('issues') and not p.get('evaluation_gaps')]
    for rid,row in model['declarations'].items():
        typ=row['type'];value={'declaration':rid,'name':row['name'],'type':typ,'declaration_source':row['source'],
            'origin':'constructor_configuration' if row['constructor_writes'] or row['explicit_initializer'] else
                     'abstract_initial_scalar' if selected_domain==CAPABILITY and (typ.startswith(('uint','int')) or typ in ('address','address payable')) else 'fixed_type_default',
            'encoded':False,'analysis_domain':selected_domain,'initial_model_identity':model['identity'],
            'runtime_assignment_sites':row['runtime_sites']}
        table[rid]=value
        if row['runtime_sites'] or model['runtime_writers']['opaque_storage_writes']:
            value['origin']='constructor_choice_with_possible_later_write';continue
        if not clean or any(p.get('issues') or p.get('evaluation_gaps') for p in model['constructor_paths']):continue
        cell={'kind':'storage','root':rid,'segments':[]}
        try:values=[_initial_term(read(cell,p['writes'],lookup),context,selected_domain) for p in clean]
        except (ValueError,KeyError,TypeError):continue
        if values and all(v==values[0] for v in values):
            v=values[0]
            if v.get('kind')=='literal' and type(v.get('value')) in (bool,int):value.update(value=v['value'],encoded=True,
                origin='fixed_constructor_or_declaration' if row['constructor_writes'] else 'fixed_type_default')
            elif v.get('initial_identity')=='deployment_caller':value.update(nonzero=True,encoded=True,origin='fixed_deployer_address')
    cache[token]=table
    return table


def encode_state(e,details=None):
    from .initial_state import domain,CAPABILITY,DEPLOYMENT
    if domain(e.lookup) in (CAPABILITY,DEPLOYMENT):
        from .state_encoding import encode
        return encode(e,details)
    items=[];constraints=[]
    for vid,v in state_facts(e.lookup).items():
        if not v['encoded']:continue
        cell=e.expr({'kind':'storage','root':vid,'segments':[]})
        constraints.append(cell!=0 if v.get('nonzero') else cell==v['value'])
        items.append(v)
    return constraints,items


def prestate_receipt(details,initial):
    d=details or {}
    if isinstance(initial,dict):
        return dict(initial,executed_prefix=d.get('prefix',[]),encoded_case=d.get('encoded_case',[]),
            encoded_request_bindings=d.get('encoded_request_bindings',d.get('request_context',{}).get('bindings',[])))
    return {'analysis_domain':'ac_checked_prestate_r1','analysis':'conditional_symbolic_with_checked_fixed_initializers','encoded_invariant_declarations':initial,
            'executed_prefix':d.get('prefix',[]),'encoded_case':d.get('encoded_case',[]),
            'encoded_request_bindings':d.get('encoded_request_bindings',d.get('request_context',{}).get('bindings',[])),
            'explicit_constructor_prefix_executed':False,'author_run_initial_state_verified':False}


def impossible_role(inv,oid):
    """P exclusion only if every clean committing path needs caller == fixed zero."""
    if not inv.backend.complete(oid):return False
    original=inv.backend.paths(oid)
    if not original:return False
    fixed=state_facts(inv.f.lookup(oid))
    from .request_scope import positive_caller_gate
    def zero(g):
        if g.get('op') in ('and','&&'):return any(zero(x) for x in g.get('args',[]))
        return positive_caller_gate(g,inv.f.lookup(oid)) and g.get('op') in ('==','!') and any(
            fixed.get(c['root'],{}).get('encoded') and fixed[c['root']].get('value')==0 for c in selectors(g))
    def value(x):
        if x.get('kind')=='literal':
            a=x.get('value')
            if isinstance(a,bool) or isinstance(a,int):return a
            if str(a).lower() in ('true','false'):return str(a).lower()=='true'
            try:return int(a,0)
            except (ValueError,TypeError):return None
        if x.get('kind')=='storage' and not x.get('segments'):return fixed.get(x.get('root'),{}).get('value')
        op=x.get('op');args=[value(v) for v in x.get('args',[])]
        if op=='!' and len(args)==1 and args[0] is not None:return not args[0]
        if len(args)!=2:return None
        a,b=args
        if op in ('and','&&') and False in args:return False
        if op in ('or','||') and True in args:return True
        if a is None or b is None:return None
        if op=='==':return a==b
        if op=='!=':return a!=b
        if op=='>=':return a>=b
        if op=='<=':return a<=b
        if op=='<':return a<b
        if op=='>':return a>b
        return None
    return all(any(zero(g) or value(g) is False for g in p['guards']) for pid,p in original)


~~~~

## source/src/pr_next_joint/investigation/program.py

~~~~python
"""M1: original compiler identities, paths and structural edges only.

There is deliberately no import of an old detector, policy projection,
asset discovery, LLM consumer or report merger in this module.
"""
import copy
import hashlib
import time
from pathlib import Path
from pr_next_joint.core import digest, require
from pr_next_joint.frontend.inventory import target_inventory
from pr_next_joint.frontend.source_entry_identity import entry_functions
from pr_next_joint.frontend.program_paths import MechanismPaths
from pr_next_joint.frontend.path_ir import walk, key, clean, ExpressionLimit
from pr_next_joint.frontend.storage import selectors
from pr_next_joint.graph.state_relations import expand_write
from .contracts import ident


class Facts:
    def __init__(self, bundle, native, sources, options, selected=None, description=None):
        self.program_clock_origin = time.monotonic()
        require(all(bundle[k] == native[k] for k in ('program_id', 'build_id')), 'input_identity_mismatch')
        require(bundle.get('native_ir', {}).get('sha256') == digest(native), 'native_digest_mismatch')
        self.bundle, self.native, self.options = bundle, native, options
        self.lookups, self.operations, self.paths, self.writes, self.effects, self.terms = {}, {}, {}, {}, {}, {}
        self.references, self.gaps = {}, []
        inventory = target_inventory(bundle)
        available = {x['file'] + ':' + x['contract'] for x in inventory if x['selected']}
        self.selected = sorted(set(selected) if selected is not None else available)
        require(bool(self.selected) and set(self.selected) <= available, 'invalid_selected_targets')
        source_by_name = {s['file']: s for s in sources}
        for file, ast in bundle['ast_sources'].items():
            require(file in source_by_name, 'source_missing:' + file)
            content = source_by_name[file]['content'].encode('utf-8')
            require(hashlib.sha256(content).hexdigest() == source_by_name[file]['sha256'], 'source_hash_mismatch')
        for contract in bundle['contracts']:
            target = contract['file'] + ':' + contract['name']
            if target not in self.selected:
                continue
            lookup = MechanismPaths(bundle, contract, options.max_paths)
            lookup.analysis_scope = options.scope
            self.lookups[target] = lookup
            bases = lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']])
            for n in lookup.nodes.values():
                # All references retain the actual compiler node and file span.
                if n.get('nodeType') in ('VariableDeclaration', 'FunctionDefinition', 'Assignment', 'UnaryOperation',
                                         'FunctionCall', 'BinaryOperation', 'IndexAccess', 'MemberAccess', 'IfStatement'):
                    ref = ident('r', [target, n['id']])
                    self.references[ref] = {'target': target, 'ast_id': n['id'], 'kind': n['nodeType'],
                                            'name': n.get('name', n.get('memberName')), 'source': lookup.anchor(n)}
            for entry in entry_functions(lookup):
                fn = entry['signature']; oid = ident('op', [target, fn])
                body = lookup.function(fn)
                operation = {'id': oid, 'target': target, 'function': fn,
                             'source': lookup.anchor(body.get('generated_getter', body)),
                             'parameters': [], 'paths': [], 'gaps': [], 'generated_getter': bool(body.get('generated_getter'))}
                params = body.get('parameters', {}).get('parameters', [])
                for n in params:
                    operation['parameters'].append({'ref': ident('r', [target, n['id']]), 'name': n['name'],
                        'term': self.term({'kind': 'parameter', 'id': n['id'], 'type': n['typeDescriptions']['typeString']}, target)})
                self.operations[oid] = operation
                try:
                    if time.monotonic()-self.program_clock_origin >= options.seconds:
                        self.gap(oid, 'path_extraction', 'program_time_before_entry')
                        continue
                    paths = lookup.run(fn)
                except ExpressionLimit as error:
                    self.gap(oid,'source_expression_limit',str(error))
                    continue
                except (TypeError, AttributeError):
                    raise
                except Exception as error:
                    self.gap(oid, 'path_extraction', type(error).__name__ + ':' + str(error)); continue
                for index, path in enumerate(paths):
                    pid = ident('path', [oid, index]); path = copy.deepcopy(path)
                    try:
                        path['writes'] = [item for w in path['writes'] for item in expand_write(w, lookup)]
                        # Validate each executable operand independently before publishing
                        # any references. A bounded path cannot poison a sibling path.
                        for expr in [*path['guards'], *(w['path'] for w in path['writes']),
                                     *(w['value'] for w in path['writes']), *path.get('evaluated_terms', []),
                                     path.get('return_value'), *path.get('sensitive_effects', [])]:
                            if expr is not None: clean(expr)
                    except ExpressionLimit as error:
                        self.gap(oid,'source_expression_limit',{'path':pid,'reason':str(error)})
                        continue
                    except (TypeError, AttributeError):
                        raise
                    except Exception as error:
                        path.setdefault('issues', []).append({'reason': 'write_expansion:' + str(error)})
                    self.paths[pid] = {'operation': oid, 'index': index, 'raw': path}
                    card = {'id': pid, 'flow': path['flow'], 'guards': [], 'writes': [], 'effects': [],
                            'issues': copy.deepcopy(path.get('issues', [])), 'evaluation_gaps': path.get('evaluation_gaps', [])}
                    for g in path['guards']:
                        card['guards'].append(self.term(g, target))
                    for wi, w in enumerate(path['writes']):
                        wid = ident('w', [pid, wi]); self.writes[wid] = {'operation': oid, 'path': pid, 'raw': w}
                        card['writes'].append({'id': wid, 'selector': self.term(w['path'], target),
                                              'value': self.term(w['value'], target), 'source': w['source']})
                    for ei, e in enumerate(path.get('sensitive_effects', [])):
                        eid = ident('fx', [pid, ei]); self.effects[eid] = {'operation': oid, 'path': pid, 'raw': e}
                        row = {'id': eid, 'kind': e['kind'], 'source': e['source']}
                        for field in ('recipient', 'amount', 'success'):
                            if e.get(field) is not None: row[field] = self.term(e[field], target)
                        card['effects'].append(row)
                    for value in [path.get('evaluated_terms', []), path.get('return_value')]:
                        for n in walk(value):
                            if n.get('kind'): self.term(n, target)
                    operation['paths'].append(card)
                    if card['issues'] or card['evaluation_gaps']:
                        self.gap(oid, 'program_path', {'path': pid, 'issues': card['issues'], 'evaluation_gaps': card['evaluation_gaps']})
        for target in self.selected:
            self.lookups[target]._investigation_facts=self
            self.term({'kind': 'actual_sender'}, target)
            self.term({'kind': 'transaction_value', 'type': 'uint256'}, target)
        edges = []
        reads={o['id']:{s['root'] for p in o['paths'] for s in selectors(self.paths[p['id']]['raw'])}
               for o in self.operations.values()}
        writes={}
        for w in self.writes.values():
            writes.setdefault(w['operation'],set()).add(w['raw']['path']['root'])
        for a in self.operations.values():
            a_roots=writes.get(a['id'],set())
            if not a_roots:continue
            for b in self.operations.values():
                if a['target'] != b['target']: continue
                b_roots=reads[b['id']]
                roots = sorted(a_roots & b_roots)
                if roots:
                    edges.append({'from': a['id'], 'to': b['id'], 'roots': roots, 'kind': 'may_write_read',
                                  'meaning': 'structural_frontier_not_policy'})
        package = Path(__file__).resolve().parents[1]
        implementation = {p.relative_to(package).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(package.rglob('*.py'))}
        self.context = {'schema': 'scrv-facts-r2-1', 'identity': {k: bundle[k] for k in ('program_id', 'build_id')},
                        'implementation_sha256': digest(implementation), 'finite_options': options.record(),
                        'scope': options.scope, 'sources': sources, 'description': description,
                        'operations': list(self.operations.values()), 'references': self.references,
                        'terms': self.terms, 'frontier': edges, 'program_gaps': self.gaps}
        from .initial_state import model, domain
        self.context['state_analysis']={target:{'analysis_domain':domain(lookup),'initial_model_identity':model(self,target)['identity'],
            'candidate_amount_leaves':model(self,target)['candidate_amount_leaves']} for target,lookup in self.lookups.items()}
        from .summary import get_summaries
        self.summaries=get_summaries(self)
        self.link_unexpanded_effects()
        from .call_summary import CallSummaries
        self.call_summaries = CallSummaries(self)
        self.context['call_summary_identity'] = self.call_summaries.identity
        self.context['effect_summary_identity']=self.summaries.identity
        from .candidates import source_candidates
        self.source_candidates=source_candidates(self)
        self.context['source_candidates']=self.source_candidates
        self.identity = digest(self.context)

    def link_unexpanded_effects(self):
        """Track unavailable storage dependencies without discarding unrelated readers."""
        limited=[g for g in self.gaps if g['kind']=='source_expression_limit']
        for gap in limited:
            entry=self.operations[gap['operation']];lk=self.lookup(entry['id'])
            body=lk.function(entry['function']);pending=[body];seen=set();writes=set();opaque=False
            while pending:
                fn=pending.pop()
                if fn.get('id') in seen:continue
                seen.add(fn.get('id'))
                for n in walk([fn.get('body'),fn.get('modifiers',[])]):
                    if n.get('nodeType') in ('InlineAssembly','YulFunctionCall'):opaque=True
                    if n.get('nodeType') in ('FunctionCall','ModifierInvocation'):
                        expr=n.get('expression',n.get('modifierName',{}))
                        callee=lk.nodes.get(expr.get('referencedDeclaration'),{})
                        if callee.get('body'):pending.append(callee)
                        if expr.get('memberName')=='delegatecall':opaque=True
                    if n.get('nodeType') not in ('Assignment','UnaryOperation'):continue
                    lhs=n.get('leftHandSide',n.get('subExpression',{}))
                    writes.update(v.get('referencedDeclaration') for v in walk(lhs)
                                  if lk.nodes.get(v.get('referencedDeclaration'),{}).get('stateVariable'))
            if body.get('kind')=='constructor':
                raise ExpressionLimit('shared_or_entire_entry_source_expression_unavailable')
            for other in self.operations.values():
                if other['id']==entry['id'] or other['target']!=entry['target'] or other['generated_getter']:continue
                local=gap.get('reason')
                if isinstance(local,dict) and 'declaration' in local:
                    writes={local['declaration']};opaque=False
                reads={s['root'] for card in other['paths'] for s in selectors(self.paths[card['id']]['raw'])}
                if opaque or reads & writes:
                    self.gap(other['id'],'dependent_source_expression_limit',
                             {'source_operation':entry['id'],'scope':'unknown_storage' if opaque else 'shared_declaration'})
        for target in {self.operations[g['operation']]['target'] for g in limited}:
            def usable_scope(operation):
                if operation['target']!=target or operation['generated_getter']:return False
                gaps=[g for g in operation['gaps'] if g['kind']=='source_expression_limit']
                if any(g['kind']=='dependent_source_expression_limit' for g in operation['gaps']):return False
                for card in operation['paths']:
                    here=[g['reason'] for g in gaps if not isinstance(g['reason'],dict) or g['reason'].get('path')==card['id']]
                    if not here:return True
                    # A final-value failure can be isolated from a distinct write in the same path.
                    if all(isinstance(x,dict) and 'declaration' in x for x in here):
                        affected={x['declaration'] for x in here}
                        if any(self.writes[w['id']]['raw']['path']['root'] not in affected for w in card['writes']):return True
                return False
            if not any(usable_scope(op) for op in self.operations.values()):
                raise ExpressionLimit('shared_or_entire_entry_source_expression_unavailable')
    def term(self, value, target):
        ref = ident('e', [target, value])
        self.terms[ref] = {'target': target, 'expression': copy.deepcopy(value)}
        for n in walk(value):
            if n is not value and n.get('kind'):
                nr = ident('e', [target, n]); self.terms[nr] = {'target': target, 'expression': copy.deepcopy(n)}
        return ref

    def gap(self, operation, kind, reason):
        row = {'operation': operation, 'kind': kind, 'reason': reason}
        self.gaps.append(row); self.operations[operation]['gaps'].append(row)

    def operation_paths(self, oid, complete_only=False):
        for card in self.operations[oid]['paths']:
            item = self.paths[card['id']]
            p = item['raw']
            if complete_only and (p['flow'] not in ('normal', 'returned') or p.get('issues') or p.get('evaluation_gaps')):
                continue
            yield card['id'], p

    def lookup(self, oid):
        return self.lookups[self.operations[oid]['target']]

~~~~

## source/src/pr_next_joint/investigation/properties.py

~~~~python
"""Finite, source-bound questions. Wording guides investigation, never certifies harm."""
import re
from itertools import product

from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, selector_relation, value_type
from .request_scope import claim_entries, holder_effect, linked_controls, unique_cells
from .ledger import MEASURES, bind_positions, movements
from .roles import path_qualification


def words(item):
    return ' '.join(str(item.get(k) or '') for k in ('claim','distinguish','distinguishing_question','observation'))


def interpret(item):
    raw = item.get('observation')
    req = dict(raw) if isinstance(raw,dict) else {}
    text = words(item)
    if re.search(r'\b(?:never check|does not (?:read|check)|bypass(?:es)?|missing (?:the )?control)\b',text,re.I) and re.search(r'freez|frozen|guard|control',text,re.I):
        return {**req,'measure':'missing_control'}
    if req.get('measure') in MEASURES or req.get('measure') in ('denied_qualified','direct_effect','authorization_violation'):
        return req
    if req.get('measure') and req['measure'] not in ('opens','blocks'):
        return req
    if re.search(r'allowance.{0,55}(?:gross|actual debit|less than)|more than (?:the |was )?(?:allowance|approved)|(?:gross|actual) debit.{0,70}(?:allowance|grant)',text,re.I):
        return {**req,'measure':'ledger_grant'}
    if re.search(r'(?:recipient|payee|receiver).{0,55}(?:less|zero|smaller|short)|(?:lower|reduced) (?:recipient )?credit|到账减少',text,re.I):
        return {**req,'measure':'ledger_receipt'}
    if re.search(r'(?:debited|debit|charged).{0,22}(?:more|greater|extra)|greater gross debit',text,re.I):
        return {**req,'measure':'ledger_debit'}
    if req.get('measure'):
        return req
    if item.get('category')=='AC' and re.search(r'(?:qualified|entitled|authorized|rightful|rightfully).{0,65}(?:reject|denied|refus)|wrongful.{0,18}(?:denial|reject)',text,re.I):
        return {**req,'measure':'denied_qualified'}
    if item.get('category') in ('FCR-MINT','FCR-TRANSFER','FCR-DESTROY') and re.search(r'\b(mint|issuance|confiscate|seize|destroy|burn|debit|transfer|issu(?:e|es))\b',text,re.I):
        return {**req,'measure':'direct_effect'}
    if item.get('category') in ('FCR-FREEZE','FCR-PAUSE') and re.search(r'block|revert|pause|freeze',text,re.I):
        return {**req,'measure':'blocks'}
    if item.get('category')=='AC' and re.search(r'(?:install|forge|acquire|grant itself).{0,36}(?:grant|allowance|permission)',text,re.I):
        return {**req,'measure':'holder_grant'}
    return None


def conflicting_measurements(inv,q,proposal):
    """Only explicit factual negations of the same measured positive condition conflict."""
    from .request_scope import observation_applies
    factual={
        'ledger_receipt':r'\b(?:recipient|payee)\b.{0,28}\b(?:always|necessarily)\b.{0,20}\b(?:full|unchanged)',
        'ledger_debit':r'\b(?:gross|actual) debit (?:never increases|is always unchanged)',
        'ledger_grant':r'\b(?:actual|gross) debit (?:never exceeds|is always within) (?:the )?(?:allowance|grant)',
        'denied_qualified':r'\b(?:qualified|authorized) (?:caller|role|manager) (?:is never (?:rejected|denied)|always succeeds)',
    }
    if any(proposal.get(k)!=q['current'].get(k) for k in ('observation','assumptions','next_check','actor','object','phase')):
        return []
    text=proposal.get('claim','')
    return [o['probe'] for row in q.get('observations',[]) if row['measure'] in factual and row['version']==q['version']
            and observation_applies(inv,q,row) and re.search(factual[row['measure']],text,re.I)
            for o in row['outcomes'] if o['predicate_value']]


def source_target(inv,anchor,target):
    return [o for o in inv.catalog.resolve(anchor) if inv.f.operations[o]['target']==target]


def premise_cases(inv, use, item, changed=()):
    """Separate expressly different values of the same declared cell. No free Boolean substitute."""
    lookup = inv.f.lookup(use)
    cells = unique_cells(s for s in inv.graph.request_reads(use) if not keys(s))
    text = words(item)
    axes, gaps = [], []
    for cell in cells:
        name = lookup.nodes.get(cell['root'],{}).get('name')
        if not name:
            continue
        regex=r'(?<![\w$])'+re.escape(name)+r'\s*(?:==|=)\s*(true|false|\d+)\b'
        values=list(dict.fromkeys(v.lower() for v in re.findall(regex,text,re.I)))
        if not values:
            continue
        if len({s['root'] for s in cells if lookup.nodes.get(s['root'],{}).get('name')==name})!=1:
            gaps.append('ambiguous source declaration '+name);continue
        typ=value_type(cell,lookup)
        if any((v in ('true','false')) != (typ=='bool') or typ!='bool' and not typ.startswith('uint') for v in values):
            gaps.append('literal sort unsupported: '+name);continue
        at='after' if any(selector_relation(cell,c)=='same_shape' for c in changed) else 'before'
        axes.append([{'cell':cell,'source_name':name,'value':v=='true' if typ=='bool' else int(v),'frame':at} for v in values])
    fixed=[]
    assumptions=item.get('assumptions',[])
    if isinstance(assumptions,str):assumptions=[assumptions]
    named=unique_cells(inv.graph.request_reads(use))
    for a in assumptions:
        match=re.fullmatch(r'(before|after)\s+([A-Za-z_$][\w$]*(?:\[[\w$.]+\])*)\s*(?:==|=)\s*(\d+|true|false)',str(a).strip(),re.I)
        if not match:continue
        at,name,value=match.groups(); found=[s for s in named if inv.backend._storage_name(use,s)==name]
        if len(found)!=1:gaps.append('unbound scoped premise '+name);continue
        fixed.append({'cell':found[0],'source_name':name,'frame':at.lower(),'value':value.lower()=='true' if value.lower() in ('true','false') else int(value)})
    if len(axes)>3 or len(axes)>1 and any(len(axis)>1 for axis in axes):
        return [],gaps+['multiple alternative clauses cannot be independently cross-multiplied']
    return [fixed+list(c) for c in product(*axes)] if axes else [fixed],gaps


def privileged_paths(inv,oid):
    return [pid for pid,p in inv.backend.paths(oid) if path_qualification(inv.f,oid,p)]


def stage(inv,use):
    facts=inv.f; target=facts.operations[use]['target']
    listed=[]
    for cell in unique_cells(inv.graph.request_reads(use)):
        if keys(cell) or not (value_type(cell,facts.lookup(use)) or '').startswith(('uint','bool')):
            continue
        writers=[]
        for oid in sorted(inv.graph.access[target,cell['root']]['writers']):
            matches=[pid for pid,p in inv.backend.paths(oid) if any(selector_relation(cell,w['path'])=='same_shape' for w in p['writes'])]
            if matches:
                writers.append({'operation':oid,'paths':matches,'role_guarded_paths':privileged_paths(inv,oid)})
        listed.append({'cell':cell,'name':inv.backend._storage_name(use,cell),'runtime_writers':writers})
    return listed


def source_graph_holes(inv,binding,item):
    root=binding['core_operation']; target=inv.f.operations[root]['target']
    claimed=claim_entries(inv,binding,item)
    controls=unique_cells(w['path'] for _,p in inv.backend.paths(root) for w in p['writes'] if value_type(w['path'],inv.f.lookup(root))=='bool')
    if not controls:
        return []
    related=[]
    for oid in sorted(claimed-{root}):
        ops=[(pid,movements(inv.backend,oid,p)) for pid,p in inv.backend.paths(oid)]
        debit=unique_cells(c for pid,m in ops for c in m['-'])
        if not debit:
            continue
        peers=[]
        for other,entry in inv.f.operations.items():
            if entry['target']!=target or other==oid:continue
            linked=linked_controls(inv,root,other)
            if not any(selector_relation(c,l)=='same_shape' for c in controls for l in linked):continue
            for pid,p in inv.backend.paths(other):
                m=movements(inv.backend,other,p)
                if any(selector_relation(a,b)=='same_shape' for a in debit for b in m['-']):
                    peers.append({'operation':other,'path':pid,'controls':linked})
        reads=linked_controls(inv,root,oid)
        related.append({'use':oid,'debit_positions':debit,'control_reads':reads,'control_writers':controls,'peer_controlled_uses':peers})
    return related


def plan_property(inv,binding,item,plan,req):
    """Select finite typed questions with compiler-resolved endpoints, or disclose a local gap."""
    measure=req['measure']; root=binding['core_operation']; target=inv.f.operations[root]['target']
    entries=claim_entries(inv,binding,item); contexts=[]
    if measure in MEASURES:
        uses=[oid for oid in sorted(entries) if holder_effect(inv,oid)]
        if req.get('at'):uses=[o for o in source_target(inv,req['at'],target) if o in entries]
        elif root in uses and bind_positions(inv.backend,root,item)[0]:uses=[root]
        reasons=[]
        for use in uses:
            pos,err=bind_positions(inv.backend,use,item)
            if err:reasons.append(err);continue
            edges=stage(inv,use)
            forced=source_target(inv,req.get('after'),target) if req.get('after') else []
            if req.get('after') and len(forced)!=1:reasons.append('requested_intervention_not_unique');continue
            choices={}
            for edge in edges:
                if req.get('control') and req['control']!=edge['name']:continue
                for w in edge['runtime_writers']:
                    change=w['operation']
                    if forced and change not in forced or not forced and root!=use and change!=root:continue
                    if not w['role_guarded_paths']:continue
                    choices.setdefault(change,[]).append(edge['cell'])
            if not choices:reasons.append('no_source_bound_runtime_privileged_writer');continue
            for change,controls in choices.items():
                ctx=inv._compare_context({'current':item},change,use)
                ctx['observable']={'measure':measure,'ledger':pos,'control_selectors':controls,
                                   'change_paths':privileged_paths(inv,change)}
                cases,gaps=premise_cases(inv,use,item,controls)
                if gaps:reasons+=gaps;continue
                ctx['premise_cases']=cases
                # An address alias is admitted only for two actual source parameter names.
                params=inv.f.lookup(use).function(inv.f.operations[use]['function']).get('parameters',{}).get('parameters',[])
                addr={p['name']:{'kind':'parameter','id':p['id'],'type':p['typeDescriptions']['typeString']} for p in params if p['typeDescriptions']['typeString'] in ('address','address payable')}
                ctx['request_aliases']=[]
                for a,op,b in re.findall(r'\b(\w+)\s*(==|!=)\s*(\w+)\b',str(item.get('assumptions',[]))):
                    if a in addr and b in addr:ctx['request_aliases'].append([addr[a],addr[b],op])
                contexts.append((change,use,ctx))
        reason=','.join(dict.fromkeys(reasons)) or 'more_than_one_applicable_request_or_intervention'
    elif measure=='missing_control':
        rows=source_graph_holes(inv,binding,item)
        relevant=[r for r in rows if r['peer_controlled_uses'] and not r['control_reads']]
        if relevant:
            contexts=[(root,relevant[0]['use'],{'observable':{'measure':measure,'alternatives':relevant},'operation':root,
                      'checked_uses':[r['use'] for r in relevant],'frame_type':'committed_intervention_then_actual_alternative'})]
        reason='no_same_target_same_right_comparator_or_unresolved_control'
    else:
        ctx=inv._compare_context({'current':item},root,root)
        ctx.update({'observable':{'measure':measure,'claim':item.get('claim',''),'category':item.get('category')},
                    'operation':root,'stage':stage(inv,root),'frame_type':'single_original_entry'})
        if req.get('authorization'):ctx['observable']['authorization']=req['authorization']
        if measure=='direct_effect' and ctx.get('bindings'):
            ctx['exploratory_request_bindings_not_the_claim']=ctx.pop('bindings')
        params=inv.f.lookup(root).function(inv.f.operations[root]['function']).get('parameters',{}).get('parameters',[])
        addr={p['name']:{'kind':'parameter','id':p['id'],'type':p['typeDescriptions']['typeString']} for p in params if p['typeDescriptions']['typeString'] in ('address','address payable')}
        ctx['request_aliases']=[[addr[a],addr[b],op] for a,op,b in re.findall(r'\b(\w+)\s*(==|!=)\s*(\w+)\b',str(item.get('assumptions',[]))) if a in addr and b in addr]
        contexts=[(root,root,ctx)]
        if measure=='direct_effect':
            contexts[0][2]['privileged_paths']=privileged_paths(inv,root)
        reason='unresolved_direct_property'
    pick=None
    if len(contexts)==1:
        change,use,ctx=contexts[0]
        pick={'action':'compare','change':change,'observe':use,'measure':measure,'status':'source_bound',
              'expectations':{},'context':ctx,'scope':{'target':target,'finding_root':root,'use':use,'intervention':change,
                  'measure':measure,'controls':ctx['observable'].get('control_selectors',[]),'objects':[ctx['observable']['ledger'][k] for k in ('debit','credit')] if 'ledger' in ctx['observable'] else [],
                  'checked_uses':ctx.get('checked_uses',[use]),'frame_type':ctx.get('frame_type','same_request_two_worlds'),
                  'extent':'compiler-selected entries, ordered keys and recorded path conditions only'}}
    inherited_pairs=list(plan.get('selected_pairs',[]))
    plan['observation_choice']={'ordinary_pairs':inherited_pairs,'selected':pick,'pool':[pick] if pick else [],'status':'selected_property' if pick else 'unsupported',
        'reason':'source-resolved finite property' if pick else reason,'property_requested':measure,'claim_text':item['claim'],'possible_compilations':len(contexts),
        'stage_evidence':stage(inv,root),'request_resolution':{'finding_root':root,'use':pick['observe'] if pick else None,
        'possible_uses':sorted(entries),'unmeasured_uses':sorted(entries-{pick['observe'],pick['change']}) if pick else sorted(entries)}}
    if pick:
        plan['selected_pairs']=[{'change':pick['change'],'observe':pick['observe'],'source_reason':'typed property and matching applied target'}]
    inv.graph.events.append({'action':'compile_source_property','measure':measure,'root':root,'selected':bool(pick),'reason':plan['observation_choice']['reason']})


~~~~
