"""Typed links between issued credentials, principals and affected resources.

This proposes scoped AC-03 conditions for the shared P consumer. Source links,
not names/case IDs or inferred roles from arbitrary address variables, supply
the hypotheses. Program-selected public/managed alternatives remain explicit.
"""
import copy
from .m03_p_paths import key,walk,clean,lit,op,normalize,conditions_possible
from .m03_p_resource_relations import stored_values

SENDER={'kind':'actual_sender'}
def replace(value,mapping):
    if isinstance(value,dict):
        if key(value) in mapping:return copy.deepcopy(mapping[key(value)])
        return {k:replace(v,mapping) for k,v in value.items()}
    return [replace(v,mapping) for v in value] if isinstance(value,list) else value

def selector_instance(pattern,actual,bindings=None):
    """Typed producer arguments may bind, but constants/key order may not change.

    This does not invert hashes: only identically structured ordered encodings
    can unify. Repeated arguments must bind to the same consumer term.
    """
    bindings={} if bindings is None else bindings
    pattern,actual=clean(pattern),clean(actual)
    if isinstance(pattern,dict) and pattern.get('kind')=='parameter':
        if not isinstance(actual,dict):return False
        typ=pattern.get('type');actual_type=actual.get('type') or ('address' if actual.get('kind')=='actual_sender' else None)
        if typ!=actual_type:return False
        previous=bindings.setdefault(key(pattern),actual)
        return key(previous)==key(actual)
    if isinstance(pattern,dict):
        return isinstance(actual,dict) and pattern.keys()==actual.keys() and all(selector_instance(v,actual[k],bindings) for k,v in pattern.items())
    if isinstance(pattern,list):
        return isinstance(actual,list) and len(pattern)==len(actual) and all(selector_instance(p,a,bindings) for p,a in zip(pattern,actual))
    return pattern==actual

def discover_relations(lookup,program):
    from .m03_p_route import selectors,keys,fields,value_type,permission_atoms,effective_permission,contains_sender
    tasks={};gaps=[];paths=[(fn,p) for fn,ps in program.items() for p in ps if p['flow']!='reverted']
    def add(fn,write,required,basis,evidence,structure='credential_resource_binding'):
        h={'required':normalize(required),'basis':basis,'relation_evidence':evidence,'structure_override':structure,
           'origin_function':fn,'origin_source':write['source']}
        bucket=tasks.setdefault((fn,write['source']['ast_id'],key(path['guards'])),[])
        if not any(key(x[1])==key(h) for x in bucket):bucket.append(('AC-03',h))
    def equality_authority(expr):
        value=normalize(expr)
        if value.get('kind')=='op' and value['op']=='==':
            for a,b in (value['args'],value['args'][::-1]):
                if a==SENDER and b.get('kind')=='storage' and value_type(b,lookup) in ('address','address payable'):return b

    # Captured resource ID in an issued credential record. Its authority check
    # at issuance identifies the field's resource role, independent of names.
    issued=[]
    for creator,path in paths:
        if path['issues']:continue
        permissions=effective_permission(path['guards'],lookup)
        for record in path['writes']:
            if record['value'].get('kind')!='record':continue
            values=stored_values(record)
            for permission in permissions:
                for authority in selectors(permission):
                    for resource in keys(authority):
                        if resource.get('kind')!='parameter':continue
                        bindings=[(s,v) for s,v in values if key(v)==key(resource)]
                        if len(bindings)!=1:continue
                        subjects=[s for s,v in values if value_type(s,lookup) in ('address','address payable') and v.get('kind')=='parameter']
                        active=[s for s,v in values if value_type(s,lookup)=='bool' and v==lit(True)]
                        if len(subjects)==1 and active:
                            issued.append({'creator':creator,'record':record,'resource_field':bindings[0][0],'subject_field':subjects[0],
                                           'active_fields':active,'authority':authority,'permission':permission})
    for fn,path in paths:
        observed=[a for g in path['guards'] for a in permission_atoms(g,lookup)]
        for credential in issued:
            record=credential['record']['path'];origin_keys=keys(record)
            for atom in observed:
                delegate=equality_authority(atom)
                if not delegate or delegate['root']!=record['root'] or fields(delegate)!=fields(credential['subject_field']):continue
                if len(origin_keys)!=len(keys(delegate)):continue
                mapping={key(a):b for a,b in zip(origin_keys,keys(delegate))}
                bound_resource=replace(credential['resource_field'],mapping)
                active=[replace(s,mapping) for s in credential['active_fields']]
                if not all(not conditions_possible(path['guards'],s) for s in active):continue
                for write in path['writes']:
                    if write['path']['root']==record['root']:continue
                    effect_keys=keys(write['path'])
                    compatible=[k for k in effect_keys if k.get('type')==lookup.nodes[fields(bound_resource)[-1]].get('typeDescriptions',{}).get('typeString') or key(k)==key(bound_resource)]
                    if len(effect_keys)!=1 or len(compatible)!=1:continue
                    add(fn,write,op('==',compatible[0],bound_resource),'issued_credential_resource_must_match_effect',
                        {'issuance_function':credential['creator'],'issuance_source':credential['record']['source'],'checked_authority':credential['authority'],
                         'bound_subject':delegate,'bound_validity':active,'bound_resource':bound_resource,'affected_resource':compatible[0]})

    # Self-managed two-address delegation defines the principal/agent key order.
    delegation_roots={}
    for fn,path in paths:
        if path['issues']:continue
        for w in path['writes']:
            ks=keys(w['path'])
            if len(ks)==2 and ks[0]==SENDER and ks[1].get('kind')=='parameter' and ks[1].get('type') in ('address','address payable') and value_type(w['path'],lookup)=='bool':
                delegation_roots[w['path']['root']]={'function':fn,'source':w['source'],'principal_index':0,'agent_index':1}
    for fn,path in paths:
        atoms=[a for g in path['guards'] for a in permission_atoms(g,lookup)]
        principals=[p for atom in atoms if (p:=equality_authority(atom)) and keys(p)]
        for principal in principals:
            for selected in [s for g in path['guards'] for s in selectors(g) if s['root'] in delegation_roots]:
                ks=keys(selected)
                if len(ks)!=2 or {key(k) for k in ks}!={key(SENDER),key(principal)}:continue
                correct={**selected,'segments':[{'key':principal},{'key':SENDER}]}
                # Identical key order is not a binding defect. A separate valid
                # authorization branch must not be erased by this hypothesis.
                if key(selected)==key(correct):continue
                for write in path['writes']:
                    if key(keys(write['path']))!=key(keys(principal)):continue
                    add(fn,write,op('or',op('==',SENDER,principal),correct),'principal_controlled_delegation_key_order',
                        {'delegation_writer':delegation_roots[selected['root']],'resource_principal':principal,'observed_delegation':selected,'required_delegation':correct})

    # Narrowing a credential key does not narrow the actual affected resource.
    for fn,path in paths:
        for g in path['guards']:
            for atom in permission_atoms(g,lookup):
                for authority in selectors(atom):
                    for narrow in [x for k in keys(authority) for x in walk(k) if x.get('kind')=='uint_narrow']:
                        for write in path['writes']:
                            if not any(key(k)==key(narrow['input']) for k in keys(write['path'])):continue
                            corrected=replace(atom,{key(narrow):narrow['input']})
                            add(fn,write,corrected,'authorization_key_truncated_but_effect_key_full_width',
                                {'observed_permission':atom,'narrowing':narrow,'source':write['source'],
                                 'scope':'unsigned cast modulo 2**bits; source bounds retained, not a deployed witness'})

    # A caller-chosen credential must retain a scoped issuer's object key. Global
    # administrator-issued global roles have no object scope and do not qualify.
    grants=[]
    for fn,path in paths:
        if path['issues']:continue
        for a in effective_permission(path['guards'],lookup):
            for issuer in selectors(a):
                if not keys(issuer):continue
                for write in path['writes']:
                    if value_type(write['path'],lookup)!='bool' or write['value']!=lit(True):continue
                    principal_keys=keys(issuer)
                    if len(principal_keys)==1 and principal_keys[0].get('kind')=='parameter':
                        grants.append({'function':fn,'issuer':issuer,'credential':write['path'],'scope':principal_keys[0],'source':write['source']})
    for fn,path in paths:
        atoms=[a for g in path['guards'] for a in permission_atoms(g,lookup)]
        for grant in grants:
            role_reads=[s for atom in atoms for s in selectors(atom) if s['root']==grant['credential']['root'] and contains_sender(s)]
            own_reads=[s for atom in atoms for s in selectors(atom) if s['root']==grant['issuer']['root']]
            for role in role_reads:
                for own in own_reads:
                    if len(keys(own))!=1:continue
                    scope=keys(own)[0]
                    if not selector_instance(grant['credential'],role):continue
                    for write in path['writes']:
                        if not any(key(k)==key(scope) for k in keys(write['path'])):continue
                        # Both producer and consumer must structurally retain
                        # the scope. Hash inputs preserve ordered typed terms.
                        producer=any(key(n)==key(grant['scope']) for k in keys(grant['credential']) for n in walk(k))
                        consumer=any(key(n)==key(scope) for k in keys(role) for n in walk(k))
                        if producer and consumer:
                            required=op('or',op('==',SENDER,own),role)
                        elif not producer and not consumer:
                            # Existing unscoped role cannot establish permission
                            # for an arbitrary namespace. Owner branch remains.
                            required=op('==',SENDER,own)
                        else:
                            gaps.append({'function':fn,'source':write['source'],'reason':'credential_scope_encoding_requires_binding'});continue
                        add(fn,write,required,'scoped_issuer_and_credential_scope_comparison',
                            {'grant':grant,'action_scope':scope,'checked_role':role,'producer_encodes_scope':producer,'consumer_encodes_scope':consumer,
                             'scope':'conditional on role granted in another issuer scope when scope omitted; hashes treated as typed ordered keys, no inversion'})
    return tasks,gaps
