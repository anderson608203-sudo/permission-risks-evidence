"""Source-backed scope for consented handoff and issued record credentials.

Only exact selectors/guards/writes are used. Names, labels and case IDs are not
inputs. These models do not certify business intent or deployment reachability.
"""
import copy
from .m03_p_paths import key,lit,op,walk,normalize,conditions_possible
from .m03_p_resource_relations import stored_values

SENDER={'kind':'actual_sender'}

def address_equality(policy,lookup):
    from .m03_p_route import value_type
    p=normalize(policy)
    if p.get('kind')!='op' or p['op']!='==':return None
    for a,b in (p['args'],p['args'][::-1]):
        if a==SENDER and b.get('kind')=='storage' and value_type(b,lookup) in ('address','address payable'):return b

def handoffs(program,lookup):
    from .m03_p_route import effective_permission,value_type
    models=[]
    for fn,paths in program.items():
        for path in paths:
            if path['issues'] or path['flow']!='normal':continue
            for write in path['writes']:
                authority=write['path'];pending=write['value']
                if authority.get('segments') or pending.get('kind')!='storage' or pending.get('segments'):continue
                if value_type(authority,lookup) not in ('address','address payable') or value_type(pending,lookup) not in ('address','address payable'):continue
                if key(authority)==key(pending) or conditions_possible(path['guards'],op('==',SENDER,pending)):continue
                nominations=[];valid=True
                for other,paths2 in program.items():
                    for path2 in paths2:
                        if path2['flow']=='reverted':continue
                        for w in path2['writes']:
                            if key(w['path'])!=key(pending):continue
                            if other==fn and w['value']==lit(0):continue
                            if path2['issues'] or conditions_possible(path2['guards'],op('==',SENDER,authority)):
                                valid=False;continue
                            if w['value'].get('kind')=='parameter' and w['value'].get('type') in ('address','address payable'):
                                nominations.append({'function':other,'source':w['source'],'conditions':path2['guards']})
                if valid and nominations:
                    models.append({'kind':'current_authority_nomination_and_nominee_acceptance','authority':authority,'pending':pending,
                        'accept_function':fn,'accept_source':write['source'],'nominations':nominations,
                        'accept_condition':op('==',SENDER,pending),'scope':'source-bound two-step consent, not deployment reachability'})
    return models

def handoff_alternative(peer,write,function,models):
    for model in models:
        old=op('==',SENDER,model['authority']);nominee=op('==',SENDER,model['pending'])
        if function==model['accept_function'] and key(normalize(peer['policy']))==key(normalize(old)):
            return {'reason':'nominee_acceptance_of_authorized_nomination','model':model,'decision':'use_acceptance_guard_in_its_own_transition'}
        if peer['function']==model['accept_function'] and function!=peer['function'] and key(normalize(peer['policy']))==key(normalize(nominee)):
            return {'reason':'acceptance_permission_not_required_for_nomination_management','model':model,'decision':'do_not_transfer_acceptance_policy_to_other_phase'}

def record_credential_alternative(peer,write,path,function,lookup):
    from .m03_p_route import value_type,relocate,effective_permission
    # A guarded initializer issues the credential. The designated delegate,
    # not the issuer, subsequently consumes it. Require both exact identity and
    # validity checks; a mere address in a struct is insufficient.
    source=peer['write'];target=write['path']
    if source['value'].get('kind')!='record' or source['path']['root']!=target['root']:return None
    if not effective_permission(peer['guards'],lookup):return None
    values=stored_values(source);active=[];delegates=[]
    for selector,value in values:
        try:bound=relocate(selector,source['path'],target)
        except ValueError:continue
        if value==lit(True) and value_type(selector,lookup)=='bool':active.append(bound)
        if value_type(selector,lookup) in ('address','address payable') and value.get('kind')=='parameter':delegates.append(bound)
    for active_selector in active:
        if conditions_possible(path['guards'],active_selector):continue
        for delegate in delegates:
            if conditions_possible(path['guards'],op('==',SENDER,delegate)):continue
            if any(key(w['path'])==key(delegate) for w in path['writes']):continue
            return {'reason':'issued_record_credential_consumed_by_designated_delegate','issuer_function':peer['function'],
                'issuer_source':source['source'],'credential':delegate,'validity':active_selector,
                'decision':'retain_delegate_and_lifecycle_checks_without_issuer_exclusivity'}

def initialized_policy(policy,write,path,lookup):
    """Bind reads of a newly assigned record to its exact assigned fields.

    A caller permission obtained only from the designated delegate of a guarded
    initializer belongs to the consumption phase, not the issuing phase.
    """
    from .m03_p_route import effective_permission,selectors
    if write['value'].get('kind')!='record':return policy,None
    assignments={key(selector):value for selector,value in stored_values(write)}
    def replace(value):
        if isinstance(value,dict):
            if key(value) in assignments:return copy.deepcopy(assignments[key(value)])
            return {k:replace(v) for k,v in value.items()}
        return [replace(v) for v in value] if isinstance(value,list) else value
    bound=replace(policy)
    if key(bound)==key(policy):return policy,None
    addresses=[address_equality(atom,lookup) for atom in walk(policy)]
    for address in addresses:
        if not address or key(address) not in assignments:continue
        independent=[g for g in effective_permission(path['guards'],lookup) if all(s['root']!=write['path']['root'] for s in selectors(g))]
        if independent and assignments[key(address)].get('kind')=='parameter':
            return None,{'reason':'guarded_record_issuer_may_designate_another_delegate','original_condition':policy,'issued_value':assignments[key(address)],'issuer_conditions':independent}
    return bound,{'reason':'record_policy_bound_to_values_assigned_by_initializer','original_condition':policy,'bound_condition':bound,
        'scope':'same record/key/field, initialization transition only'}

def alternate_authority_scope(hypothesis,guards,lookup):
    """A different effective scalar authority prevents exclusive-policy claims.

    This is uncertainty, not an exemption or proof of a trustworthy forwarder.
    Same-family object/role selector mismatches are deliberately not suppressed.
    """
    from .m03_p_route import effective_permission,selectors
    required=selectors(hypothesis['required'])
    if not required or any(s.get('segments') for s in required):return None
    for guard in effective_permission(guards,lookup):
        normalized=normalize(guard)
        if normalized.get('kind')=='op' and normalized['op']=='or':
            branches=[address_equality(a,lookup) for a in normalized['args']]
            if len(branches)>1 and all(s is not None and not s.get('segments') for s in branches):
                if any(key(normalize(op('==',SENDER,s)))==key(normalize(hypothesis['required'])) for s in branches):
                    return {'reason':'additional_explicit_scalar_authority_on_current_operation','observed_permission':guard,
                            'candidate_permission':hypothesis['required'],'scope':'a peer operation does not establish exclusive authority over this operation'}
        observed=selectors(guard)
        if observed and all(not s.get('segments') for s in observed) and {s['root'] for s in observed}.isdisjoint(s['root'] for s in required):
            return {'reason':'different_explicit_authority_requires_policy_scope','observed_permission':guard,'candidate_permission':hypothesis['required'],
                    'scope':'possible legitimate alternate authority or trusted forwarder; trust not established'}
