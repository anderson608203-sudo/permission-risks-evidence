"""One explicit M2 relation follow-up, never an automatic retry loop.

The caller authenticates a new receipt (or labels a wholly diagnostic fixture).
Old references are reviews, new obligations are separate candidates. Identity
failures reject the response; item failures are isolated. No prose changes a
predicate, discharges an unresolved dependency, or overwrites an old verdict.
"""
import copy
from .core import require


def questions(inventory):
    result={x['id']:{'target':x['target'],'function':x['function'],'rules':[x['rule']],'source_ast_ids':x['source_ast_ids']}
            for x in inventory['obligations'] if x['route'] in ('relation_explanation_needed','partially_checked_relation','checked_policy_alternative_review')}
    for item in inventory['relations_without_checked_obligation']:
        if item['status']=='missing_m2_review':
            q=item['question'];result[q['id']]={**q,'rules':q['rule_options']}
    selected=inventory.get('followup_selection',{}).get('selected_ids')
    return result if selected is None else {k:v for k,v in result.items() if k in selected}


def validate(response,context,inventory,old_ids):
    require(isinstance(response,dict) and response.get('identity')==context['identity'],'SEMANTIC_REVIEW_IDENTITY')
    require(response.get('review_digest')==inventory['digest'],'SEMANTIC_REVIEW_PARENT')
    reviews=response.get('reviews');additions=response.get('source_obligations')
    require(isinstance(reviews,list) and isinstance(additions,list),'SEMANTIC_REVIEW_SCHEMA')
    pending=questions(inventory);seen=set();links={}
    for review in reviews:
        qid=review.get('question_id');require(qid in pending and qid not in seen,'SEMANTIC_REVIEW_QUESTION')
        seen.add(qid);q=pending[qid]
        require(review.get('disposition') in ('risk_hypothesis','normal_review','uncertain','not_applicable'),'SEMANTIC_REVIEW_DISPOSITION')
        require(isinstance(review.get('explanation'),str) and review['explanation'].strip(),'SEMANTIC_REVIEW_EXPLANATION')
        ids=review.get('source_ast_ids');refs=review.get('obligation_ids')
        require(isinstance(ids,list) and ids and all(type(x)is int and x in q['source_ast_ids'] for x in ids),'SEMANTIC_REVIEW_SOURCE_SCOPE')
        require(isinstance(refs,list) and all(isinstance(x,str) for x in refs),'SEMANTIC_REVIEW_LINKS')
        for ref in refs:links.setdefault(ref,[]).append(q)
    require(seen==set(pending),'SEMANTIC_REVIEW_INCOMPLETE')
    names=set(old_ids)
    for ob in additions:
        oid=ob.get('id');require(isinstance(oid,str) and oid.startswith('semantic_') and oid not in names and oid in links,'SEMANTIC_REVIEW_NEW_ID')
        names.add(oid)
        require(any(ob.get('target')==q['target'] and ob.get('function')==q['function'] and ob.get('rule') in q['rules'] for q in links[oid]),'SEMANTIC_REVIEW_OPERATION')
    require(set(links)=={x['id'] for x in additions},'SEMANTIC_REVIEW_DANGLING_LINK')
    return copy.deepcopy(additions),copy.deepcopy(reviews)


def partition(response, context, inventory, old_records):
    """Validate the authenticated envelope, then retain independently valid items.

    Source scope remains the exact scope of the original question. A source ID
    merely existing elsewhere in the build does not make it usable here.
    """
    require(isinstance(response,dict) and response.get('identity')==context['identity'],'SEMANTIC_REVIEW_IDENTITY')
    require(response.get('review_digest')==inventory['digest'],'SEMANTIC_REVIEW_PARENT')
    raw_reviews=response.get('reviews');raw_additions=response.get('source_obligations')
    require(isinstance(raw_reviews,list) and isinstance(raw_additions,list),'SEMANTIC_REVIEW_SCHEMA')
    pending=questions(inventory);old={o['id']:o for o in old_records}
    errors=[];reviews=[];additions=[];links={};seen=set()
    def error(kind, item, reason):
        errors.append({'item_kind':kind,'item_id':item,'reason':reason,'original_preserved':True})
    def matches(ob,q):
        return (ob.get('target'),ob.get('function'))==(q['target'],q['function']) and ob.get('rule') in q['rules']
    counts={}
    for r in raw_reviews:
        if isinstance(r,dict) and isinstance(r.get('question_id'),str):
            counts[r['question_id']]=counts.get(r['question_id'],0)+1
    names={}
    for ob in raw_additions:
        if isinstance(ob,dict) and isinstance(ob.get('id'),str):names.setdefault(ob['id'],[]).append(ob)
    for index,r in enumerate(raw_reviews):
        qid=r.get('question_id') if isinstance(r,dict) else None
        try:
            require(isinstance(qid,str) and qid in pending,'SEMANTIC_REVIEW_QUESTION')
            seen.add(qid)
            require(counts[qid]==1,'SEMANTIC_REVIEW_DUPLICATE_QUESTION')
            q=pending[qid]
            require(r.get('disposition') in ('risk_hypothesis','normal_review','uncertain','not_applicable'),'SEMANTIC_REVIEW_DISPOSITION')
            require(isinstance(r.get('explanation'),str) and r['explanation'].strip(),'SEMANTIC_REVIEW_EXPLANATION')
            ids=r.get('source_ast_ids');refs=r.get('obligation_ids')
            require(isinstance(ids,list) and ids and all(type(x)is int and x in q['source_ast_ids'] for x in ids),'SEMANTIC_REVIEW_SOURCE_SCOPE')
            require(isinstance(refs,list) and all(isinstance(x,str) for x in refs),'SEMANTIC_REVIEW_LINKS')
            accepted=[];prior=[]
            for ref in dict.fromkeys(refs):
                if ref in old:
                    if matches(old[ref],q):accepted.append(ref);prior.append(ref)
                    else:error('reference',ref,'SEMANTIC_REVIEW_OLD_OPERATION')
                elif ref in names and len(names[ref])==1 and ref.startswith('semantic_'):
                    if matches(names[ref][0],q):
                        accepted.append(ref);links.setdefault(ref,[]).append(qid)
                    else:error('reference',ref,'SEMANTIC_REVIEW_OPERATION')
                else:error('reference',ref,'SEMANTIC_REVIEW_DANGLING_OR_DUPLICATE_LINK')
            record=copy.deepcopy(r);record['original_obligation_ids']=record['obligation_ids']
            record['obligation_ids']=accepted;record['existing_obligation_ids']=prior
            record['effect']='review_only_until_typed_relation_or_new_obligation_is_checked'
            reviews.append(record)
        except Exception as ex:error('review',qid or index,str(ex))
    for qid in sorted(set(pending)-seen):error('review',qid,'SEMANTIC_REVIEW_MISSING_QUESTION')
    for index,ob in enumerate(raw_additions):
        oid=ob.get('id') if isinstance(ob,dict) else None
        try:
            require(isinstance(oid,str) and oid.startswith('semantic_') and oid not in old and len(names.get(oid,[]))==1,'SEMANTIC_REVIEW_NEW_ID')
            require(oid in links,'SEMANTIC_REVIEW_UNLINKED_ADDITION')
            additions.append(copy.deepcopy(ob))
        except Exception as ex:error('obligation',oid or index,str(ex))
    return {'additions':additions,'reviews':reviews,'errors':errors,
            'new_links':links,'requested_questions':len(pending),
            'accepted_questions':len(reviews),'raw_response_unchanged':True}


def _validate_merge_inputs(base,extra):
    from .m05_joint_obligations import RULES,empty_rule_progress
    schema=empty_rule_progress()
    for channel in (base,extra):
        require(set(channel['rule_stage_progress'])==set(RULES),'SEMANTIC_REVIEW_PROGRESS_RULES')
        for progress in channel['rule_stage_progress'].values():
            require(set(progress)==set(schema),'SEMANTIC_REVIEW_PROGRESS_FIELDS')
            for name,default in schema.items():
                value=progress[name]
                require(type(value)is type(default),'SEMANTIC_REVIEW_PROGRESS_TYPE:'+name)
                if type(value)is int:require(value>=0,'SEMANTIC_REVIEW_PROGRESS_NEGATIVE:'+name)
                elif type(value)is str:require(value==default,'SEMANTIC_REVIEW_PROGRESS_SCOPE')
    a={x['id'] for x in base['source_obligations']};b={x['id'] for x in extra['source_obligations']}
    require(not a&b,'SEMANTIC_REVIEW_REPLACES_OLD_OBLIGATION')


def merge_checked(base,extra):
    """Sum actual disjoint checks; never re-solve or overwrite an old proposal."""
    _validate_merge_inputs(base,extra)
    result=copy.deepcopy(base)
    for field in ('source_obligations','source_obligation_checks','source_obligation_errors'):
        result[field]+=copy.deepcopy(extra[field])
    for field in ('formal_checks_called','reportable_findings'):result[field]+=extra[field]
    for rule,progress in extra['rule_stage_progress'].items():
        for key,value in progress.items():
            if type(value)is bool:result['rule_stage_progress'][rule][key] |= value
            elif type(value)is int:result['rule_stage_progress'][rule][key] += value
    return result


def stage_checked(base,extra,bridge,context,state,queries,coverage,origin,real,audit):
    """Keep candidate queries and progress private until the caller commits.

    A bridge or merge failure cannot leak new ordinary queries into the base
    report while claiming the supplement was rejected. Solver work is never
    rolled back or re-run here; the caller retains the exception as unknown.
    """
    from .m05_obligation_checks import evaluate
    _validate_merge_inputs(base,extra)
    staged_extra=copy.deepcopy(extra);staged_bridge=copy.deepcopy(bridge)
    staged_queries=copy.deepcopy(queries);staged_coverage=copy.deepcopy(coverage)
    staged_bridge.enqueue(staged_extra,context,state,staged_queries,staged_coverage,origin)
    audit('evaluation_started',staged_extra,None)
    checked=evaluate(staged_extra,state,real)
    audit('evaluated_pending_commit',staged_extra,checked)
    combined=merge_checked(base,checked)
    return combined,staged_extra,checked,staged_bridge,staged_queries,staged_coverage
