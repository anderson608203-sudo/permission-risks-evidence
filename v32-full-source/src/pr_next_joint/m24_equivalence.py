"""Bidirectional source condition equivalence; unknown is not equivalence."""
from .m03_p_paths import op
from .m04_logic import Unsupported
def equivalent_conditions(lookup,left,right):
    from .m09_shared_policy import implies
    try:
        return implies(lookup,{'guards':left,'evaluated_terms':[]},op('and',*right)) and implies(lookup,{'guards':right,'evaluated_terms':[]},op('and',*left))
    except (Unsupported,ValueError,KeyError,TypeError):return False


def equivalent_effect(lookup,source,target):
    # Exact object/instance/key alignment first. Final stored values, rather
    # than assignment spelling, decide whether the effects agree.
    from .m21_admission import unify,substitute
    from .m03_p_paths import walk,key
    from .m09_shared_policy import implies
    if source.get('selector',{}).get('kind')!='storage' or target.get('selector',{}).get('kind')!='storage':return None
    binding={}
    if not unify(source['selector'],target['selector'],binding,lookup):return None
    before=substitute(source.get('value',{}),binding);after=target.get('value',{})
    # Unmapped arguments must bind unambiguously by exact typed occurrences.
    # We do not guess a permutation solely because a solver can find one.
    target_terms={key(n) for n in walk(after)}
    missing={key(x):x for x in walk(before) if x.get('kind')=='parameter' and key(x) not in target_terms}
    if missing:return None
    try:
        if implies(lookup,{'guards':[],'evaluated_terms':[]},op('==',before,after)):return binding
    except (Unsupported,ValueError):pass
    return None


# Query-local lookup objects are immutable during applicability analysis.
# Reuse exactly identical equivalence requests, including rejected requests;
# no result is shared between programs or different source environments.
def _memoized(function):
    from functools import wraps
    import json, copy
    @wraps(function)
    def wrapper(lookup,*args):
        raw=json.dumps(args,sort_keys=True,separators=(',',':'))
        if len(raw)>262144:return function(lookup,*args)
        cache=getattr(lookup,'_v24_equivalence_cache',None)
        if cache is None:cache={};lookup._v24_equivalence_cache=cache
        k=(function.__name__,raw)
        stats=getattr(lookup,'_v24_equivalence_metrics',None)
        if stats is None:stats={'calls':0,'hits':0,'cache_characters':0};lookup._v24_equivalence_metrics=stats
        stats['calls']+=1
        if k in cache:stats['hits']+=1;return copy.deepcopy(cache[k])
        result=function(lookup,*args)
        if len(cache)<8192 and stats['cache_characters']+len(raw)<=16777216:
            cache[k]=copy.deepcopy(result);stats['cache_characters']+=len(raw)
        return result
    return wrapper

equivalent_conditions=_memoized(equivalent_conditions)
equivalent_effect=_memoized(equivalent_effect)
