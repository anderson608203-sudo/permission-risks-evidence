"""Read the actual effect and its normal authorization in one source pass."""
from pr_next_joint.frontend.path_ir import key
from .source_opinion import conjuncts
from .transfer_scope import bind_transfers, bound_test, is_model_use, transfer_request


def assess(inv, q, result, basis):
    if not is_model_use(inv,q,result) or not transfer_request(q):
        return basis, None
    paths, gap = bind_transfers(inv,q)
    record = {'method':'direct','property':q['property']['id'],'paths':[], 'outcome':'unverified'}
    if gap:
        record['reason']=gap
        return basis, record
    for part in paths:
        row=part['row']
        matches=any(bound_test(g,part['grant'],part['amount'])
                    for term in row['guards'] for g in conjuncts(term))
        record['paths'].append({'path':row['path'],'site':part['debit']['source'],'matched_guard':matches,
                                'binding':part['binding']})
        if not matches:
            record['reason']='bound_not_mandatory_on_every_debit'
            return basis,record
    if basis['status'] not in ('open','normal') or result['scope'].get('source_property_certificates'):
        record['reason']='independent_evidence_kept'
        return basis,record
    sites=[p['debit']['source'] for p in paths]
    # A solver observation for a distinct effect must survive this source reading.
    related=set().union(*(p['sites'] for p in paths))
    if any(v['details'].get('effect_location') and key(v['details']['effect_location']) not in related
           for v in result['scope'].get('positive_condition_scopes',())):
        record['reason']='distinct_verified_effect'
        return basis,record
    record.update(outcome='refuted_by_normal',reason='holder_issued_bound_on_all_debits')
    return {'status':'normal','reason':'holder_issued_transfer_scope','locations':sites,
            'same_scope_authorized':True,'exact_write':True},record

