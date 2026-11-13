"""Source policy applicability: object phase and managed credential target.

Exclude a peer-policy transfer only for contradictory bound object preconditions.
An independent management guard may govern a credential being edited; that
credential's current state is not automatically the caller's authentication.
"""
from .m03_p_paths import key,walk,conditions_possible,lit,op


def peer_phase_conflict(peer,write,path):
    from .m03_p_route import relocate,selectors,contains_sender
    guards=path['guards']
    # Direction matters. A creation policy may still apply to later updates.
    # Only exclude a later-operation prerequisite from object initialization
    # when this path explicitly requires absence and establishes existence.
    initialized=[w['path'] for w in path['writes'] if w['value']==lit(True)
                 and not conditions_possible(guards,op('!',w['path']))]
    if not initialized:return None
    retained=[]
    for g in peer.get('guards',[]):
        if contains_sender(g) or not selectors(g):continue
        try:bound=relocate(g,peer['write']['path'],write['path'])
        except ValueError:continue
        if any(x.get('kind') in ('unknown','call_unresolved','choice','symbol','member') for x in walk(bound)):continue
        retained.append(bound)
    if not retained or not any(not conditions_possible(retained,p) for p in initialized):return None
    try:
        if conditions_possible(guards) and not conditions_possible(guards+retained):
            return {'reason':'peer_object_preconditions_disjoint','peer_function':peer['function'],
                    'peer_conditions_bound_to_target':retained,'target_conditions':guards,
                    'decision':'peer_permission_not_applicable_to_this_object_phase'}
    except ValueError:pass
    return None


def managed_target_check(atom,write,guards,lookup):
    from .m03_p_route import selectors,effective_permission,state_overlap
    observed=selectors(atom)
    # Exact selector identity is required: another object/key is not excused.
    if len(observed)!=1 or key(observed[0])!=key(write['path']):return None
    managers=[g for g in effective_permission(guards,lookup)
              if selectors(g) and not any(state_overlap(s,write['path']) for s in selectors(g))]
    if not managers:return None
    return {'reason':'credential_state_check_is_managed_effect_target','checked_target':observed[0],
            'management_permissions':managers,'decision':'retain_management_AC_checks; do_not_replace_target_subject_with_caller'}
