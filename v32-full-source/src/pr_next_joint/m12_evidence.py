"""Pure-predicate canonicalization and exact local model reuse."""
from .m03_p_paths import normalize,walk,key
def predicate(value):
    if not isinstance(value,dict):return value
    if any(n.get('kind') not in ('op','storage','parameter','actual_sender','literal','contract_address','environment')
           or n.get('kind')=='op' and n.get('op') not in ('and','or','&&','||','!','==','!=','<','<=','>','>=')
           for n in walk(value) if 'kind' in n):return value
    value=normalize(value)
    def order(v):
        if not isinstance(v,dict):return v
        if v.get('kind')=='op':
            v={**v,'args':[order(x) for x in v['args']]}
            if v['op'] in ('and','or','=='):v['args'].sort(key=key)
        return v
    return order(value)

def model_key(row):
    if row['rule'] not in ('AC-01','AC-02','AC-03') or row.get('graph_frame_obligation'):return None
    # These consumers read the same guards/effects/terms. All source and issue
    # fields stay in the key; only policy origin metadata is omitted.
    try:
        return key({k:row.get(k) for k in ('target','function','rule','path_index','effect',
            'conditions','required_policy_candidate','source_evaluation_terms','issues')})
    except ValueError as error:
        # Cache-key construction is optional; a large predicate must still be
        # checked in its original form, never omitted or classified by the cache.
        if not str(error).startswith('SOURCE_EXPRESSION_'):raise
        row.setdefault('verification_cache_diagnostics',[]).append({'reason':str(error),'action':'check_original_query_without_cache'})
        return None
