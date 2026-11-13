"""Source-backed management and payment-stage applicability, not verdicts."""
import copy
from .m03_p_paths import key,walk,op,lit
from .m03_p_route import selectors,keys,fields,value_type,effective_permission
from .m09_shared_policy import implies
from .m04_logic import Unsupported
SENDER={'kind':'actual_sender'};PAID={'kind':'transaction_value','type':'uint256'}
def current(q,state):
    ps=state['paths'].get((q['target'],q['function']),[]);i=q.get('path_index')
    if type(i)is not int or not 0<=i<len(ps):return None,None
    p=ps[i]
    if p['flow'] not in ('normal','returned') or p['issues'] or p.get('evaluation_gaps'):return None,None
    return state['lookups'][q['target']],p

def managed_record_subject(q,state):
    b=q.get('policy_basis',{})
    if b.get('basis')!='caller_selected_authorization_subject':return None
    lookup,p=current(q,state)
    if p is None:return None
    observed=b.get('observed',{})
    # A member-existence test followed by a mutation of that very membership,
    # under an independently checked manager, selects the member being managed.
    if observed.get('kind')!='storage' or value_type(observed,lookup)!='bool':return None
    ks=keys(observed)
    if len(ks)!=1 or ks[0].get('kind')!='parameter' or ks[0].get('type') not in ('address','address payable'):return None
    wanted=copy.deepcopy(observed);wanted['segments']=[{'key':SENDER} if 'key' in s else s for s in observed['segments']]
    if key(wanted)!=key(q['required_policy_candidate']):return None
    managers=[g for g in effective_permission(p['guards'],lookup) if selectors(g) and all(s['root']!=observed['root'] for s in selectors(g))]
    mutations=[w for w in p['writes'] if key(w['path'])==key(observed) and w['value'] in (lit(False),lit(True))]
    if not managers or not mutations:return None
    return {'decision':'source_manager_edits_selected_membership_not_caller_membership',
        'source_certificate':{'object_condition':observed,'manager_permissions':managers,'membership_mutations':mutations},
        'scope':'only the inferred caller-membership predicate; all independent authorization and asset duties remain',
        'not_safety_certificate':True}

def paid_authority_transition(q,state):
    kind=q.get('policy_basis',{}).get('basis')
    allowed=('state_controls_authorization; management assumed self-governed','v20_source_authority_replacement','same_resource_guarded_operation','source_checked_M2_relation','credential_management_edges_to_same_family','same_source_native_reserve_guard')
    if kind not in allowed:return None
    lookup,p=current(q,state)
    if p is None:return None
    effect=q.get('effect',{});owner=effect.get('selector',{})
    if owner.get('kind')!='storage' or owner.get('segments') or value_type(owner,lookup) not in ('address','address payable'):return None
    ws=[w for w in p['writes'] if key(w['path'])==key(owner) and w['source']==effect.get('source')]
    if len(ws)!=1:return None
    try:
        # Source-defined paid succession: the caller becomes the recorded
        # participant and the corresponding stored price becomes exactly the
        # payment, under a strict increase over its old value. An unrelated
        # fee or a mere payable entry is insufficient.
        if ws[0]['value']==SENDER:
            prices=[w for w in p['writes'] if not w['path'].get('segments') and str(value_type(w['path'],lookup)).startswith('uint') and w['value']==PAID]
            for price in prices:
                from .m22_local_state import positive_scalar,register
                program={f:ps for (target,f),ps in state['paths'].items() if target==q['target']}
                invariant=positive_scalar(lookup,program,price['path'])
                qualified={**p,'guards':p['guards']+([invariant['predicate']] if invariant else [])}
                if implies(lookup,qualified,op('>=',PAID,price['path'])) and implies(lookup,qualified,op('>',PAID,lit(0))):
                    return {'decision':'source_paid_role_successor_establishes_new_price',
                        'source_certificate':{'authority':owner,'successor_assignment':ws[0],'price_assignment':price,'source_conditions':p['guards'],'proved_state_fact':register(state,invariant)},
                        'scope':'this source-priced role replacement only; asset disposition and other permissions remain', 'not_safety_certificate':True}
        # A price must be set under the incumbent's source authority, and the
        # incumbent must actually receive at least the price on this path.
        prices=[s for g in p['guards'] for s in selectors(g) if not s.get('segments') and str(value_type(s,lookup)).startswith('uint')]
        prices += [n for g in p['guards'] for n in walk(g) if n.get('kind')=='literal' and type(n.get('value'))is int and n['value']>0]
        prices=list({key(x):x for x in prices}.values())
        for price in prices:
            if not implies(lookup,p,op('>=',PAID,price)):continue
            writers=[];unsafe=False
            if price.get('kind')=='literal':writers=[{'kind':'source_fixed_positive_price','literal':price}]
            for (t,f),ps in state['paths'].items():
                if t!=q['target']:continue
                for branch in ps:
                    if branch['flow'] not in ('normal','returned'):continue
                    for w in branch['writes']:
                        if key(w['path'])!=key(price):continue
                        if branch['issues'] or branch.get('evaluation_gaps') or not implies(lookup,branch,op('==',SENDER,owner)):unsafe=True
                        else:writers.append({'function':f,'source':w['source'],'conditions':branch['guards']})
            if unsafe or not writers:continue
            pays=[e for e in p.get('native_transfers',[]) if key(e['recipient'])==key(owner) and implies(lookup,p,op('>=',e['amount'],price)) and implies(lookup,p,e['success'])]
            if pays:return {'decision':'source_incumbent_priced_and_paid_authority_transfer',
                'source_certificate':{'authority':owner,'price':price,'price_management':writers,'payments':pays,'assignment':ws[0]},
                'scope':'paid replacement of this authority only; no general permission from receiving money', 'not_safety_certificate':True}
    except (Unsupported,ValueError):return None
    return None
