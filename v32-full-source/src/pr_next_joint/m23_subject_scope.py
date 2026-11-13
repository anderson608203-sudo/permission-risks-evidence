"""Distinguish a source-qualified participant from the transaction caller.
Only discharges the synthetic replacement of that participant by msg.sender;
all independent authority, holder-consent and amount checks remain in place.
"""
from .m03_p_paths import key,op,lit,walk
from .m03_p_route import selectors,keys,value_type,effective_permission
from .m22_authorization import current
from .m09_shared_policy import implies
from .m04_logic import Unsupported
SENDER={'kind':'actual_sender'}

def participant_scope(q,state):
    b=q.get('policy_basis',{})
    if b.get('basis')!='caller_selected_authorization_subject':return None
    lookup,p=current(q,state)
    partial_effect=False
    if p is None:
        # A known arithmetic-evaluation-order gap does not erase an explicit
        # caller guard. This branch only rejects a synthetic extra caller role;
        # it never certifies the partly modeled balance/timer effect as safe.
        paths=state['paths'].get((q['target'],q['function']),[]);i=q.get('path_index')
        if type(i)is not int or not 0<=i<len(paths):return None
        p=paths[i];lookup=state['lookups'][q['target']]
        if (p['flow'] not in ('normal','returned') or p['issues']
            or not p.get('evaluation_gaps')
            or set(p['evaluation_gaps'])!={'conditional_fallible_evaluation_order_not_lowered'}
            or p.get('external_calls') or p.get('dangerous_calls')):return None
        partial_effect=True
    observed=b.get('observed',{});ks=keys(observed)
    if observed.get('kind')!='storage' or value_type(observed,lookup)!='bool' or len(ks)!=1:return None
    subject=ks[0]
    if subject.get('kind')!='parameter' or subject.get('type') not in ('address','address payable'):return None
    expected={**observed,'segments':[{'key':SENDER} if 'key' in s else s for s in observed['segments']]}
    if key(q.get('required_policy_candidate'))!=key(expected):return None
    effect=q.get('effect',{});sel=effect.get('selector',{})
    if not any(w['source']==effect.get('source') for w in p['writes']):return None
    # Verify that the selected participant actually occurs in the affected
    # record or transfer. No conclusion from an address spelling/name alone.
    linked=any(key(s)==key(subject) for w in p['writes'] for s in keys(w['path']))
    payments=p.get('native_transfers',[])
    linked=linked or any(key(e.get('recipient'))==key(subject) for e in payments)
    if not linked:return None
    try:
        managers=[g for g in effective_permission(p['guards'],lookup) if selectors(g) and all(s['root']!=observed['root'] for s in selectors(g))
                  and not any(n.get('kind')=='parameter' and n.get('id')==subject['id'] for n in walk(g))]
        # Prove the guard implication on a superset of concrete states. Omitted
        # arithmetic effects can remove paths, but cannot bypass this guard.
        guard_proof={'guards':p['guards'],'evaluated_terms':[]} if partial_effect else p
        if managers and implies(lookup,guard_proof,op('or',*managers)):
            return {'decision':'source_independent_caller_authorization_and_qualified_participant',
                'source_certificate':{'qualified_participant':subject,'participant_condition':observed,'caller_authorization':managers,'effect_source':effect.get('source'),
                    'guard_only_proof':partial_effect,'unresolved_effect_gaps_preserved':p.get('evaluation_gaps',[])},
                'scope':'participant membership is not additionally imposed on independently authorized caller; other duties remain',
                'not_safety_certificate':True}
        if partial_effect:return None
        # Permissionless settlement to an already qualified fixed beneficiary.
        # Check every successful path, not just one convenient payout branch.
        paths=state['paths'].get((q['target'],q['function']),[]);normal=[x for x in paths if x['flow'] in ('normal','returned')]
        if not normal or any(x['issues'] or x.get('evaluation_gaps') for x in normal):return None
        seen=[];effects=[]
        for branch in normal:
            if branch.get('external_calls') or branch.get('dangerous_calls'):return None
            for w in branch['writes']:
                if (keys(w['path'])!=[subject] or value_type(w['path'],lookup)!='bool'
                        or w['value']!=lit(True) or w['path']['root']==observed['root']):return None
                effects.append(w['source'])
            for e in branch.get('native_transfers',[]):
                if not implies(lookup,branch,op('==',e['recipient'],subject)):return None
                seen.append({'source':e['source'],'recipient':e['recipient'],'amount':e['amount']})
            # Unmodeled/other effects cannot qualify as this narrow settlement.
            if any(e.get('kind') not in ('native_transfer',) for e in branch.get('sensitive_effects',[])):return None
        if seen and effect.get('source') in effects:
            return {'decision':'source_qualified_beneficiary_settlement_not_caller_role',
                'source_certificate':{'beneficiary':subject,'eligibility':observed,'all_successful_path_payment_recipients':seen,'claim_record_effects':effects},
                'scope':'only caller-membership inference rejected; no claim of contract-wide safety or payout correctness',
                'not_safety_certificate':True}
    except (Unsupported,ValueError):return None
    return None
