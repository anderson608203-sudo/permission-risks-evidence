"""Consume authenticated M2 links without interpreting explanatory prose.

New obligations use the ordinary binder. A choice on an existing obligation
creates a separate derived candidate using a source-recomputed catalog entry;
the original proposal, remarks, check and result remain unchanged.
"""
import copy
from .core import digest, require


def prepare(partitioned, response, inventory, base, context, state, request_id):
    from .m05_joint_obligations import bind_obligations
    from .m05_relation_catalog import apply_choices
    additions=copy.deepcopy(partitioned['additions'])
    result=bind_obligations({'identity':context['identity'],'source_obligations':additions},context,state)
    result['source_obligation_checks']=[]
    old={o['id']:o for o in base['source_obligations']}
    records={o['id']:o for o in result['source_obligations']}
    reviews={r['question_id']:r for r in partitioned['reviews']}
    origins={};choice_errors=[];derived={};seen=set()
    for oid in records:
        qids=partitioned['new_links'].get(oid,[])
        origins[oid]={'kind':'new_source_obligation','request_id':request_id,'question_ids':qids,
            'parent_obligation_ids':sorted({p for q in qids for p in reviews[q]['existing_obligation_ids']}),
            'response_identity':copy.deepcopy(context['identity']),
            'review_effect':'hypothesis; no automatic discharge of original concerns'}
    choices=response.get('relation_choices',[])
    if not isinstance(choices,list):
        choice_errors.append({'reason':'RELATION_CHOICE_LIST'});choices=[]
    if choices:
        choice_errors.append({'reason':'RETIRED_RELATION_CHOICES','original_preserved':True})
    for ob in result['source_obligations']:
        ob['relation_contribution']=copy.deepcopy(origins[ob['id']])
    return result,choice_errors


def consumption(partitioned, bound, evaluated, choice_errors, request_id, real):
    """Report actual stages separately; no structural or repeated check inflation."""
    checks=evaluated['source_obligation_checks'];items=[]
    for ob in evaluated['source_obligations']:
        rows=[c for c in checks if c['obligation_id']==ob['id']]
        called=[c for c in rows if c['formal'].get('solver_called')]
        items.append({'obligation_id':ob['id'],'rule':ob['rule'],'target':ob['target'],'function':ob['function'],
            'origin':ob.get('relation_contribution'),
            'source_bound':True,'query_ids':[c['id'] for c in rows],
            'formal_check_ids':[c['id'] for c in called],
            'stage':'formally_checked' if called else 'bound_not_formalized',
            'model_gaps':copy.deepcopy(ob.get('model_gaps',[])),
            'assumptions_preserved':True})
    errors=partitioned['errors']+choice_errors+bound['source_obligation_errors']
    if evaluated['formal_checks_called']:status='authenticated_formal_checks'
    elif evaluated['source_obligations']:status='authenticated_bound_not_formalized'
    elif partitioned['reviews']:status='authenticated_review_only'
    else:status='no_valid_supplement_items'
    return {'status':status if real else 'diagnostic_'+status,'diagnostic_only':not real,
        'request_id':request_id,'new_api_automatically_requested':False,
        'partial_errors':bool(errors),'item_errors':errors,
        'requested_questions':partitioned['requested_questions'],'accepted_questions':partitioned['accepted_questions'],
        'new_obligation_ids':[o['id'] for o in partitioned['additions']],
        'bound_obligations':len(evaluated['source_obligations']),
        'new_formal_checks':evaluated['formal_checks_called'],
        'binding_errors':bound['source_obligation_errors'],
        'reviews':partitioned['reviews'],'contributions':items,
        'source_scope_policy':'original question whitelist unchanged',
        'original_results_preserved':True}
