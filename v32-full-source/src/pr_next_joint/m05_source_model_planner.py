"""Materialize supported source models after a question, independent of old cards."""
import copy
from .core import digest
from .m05_mechanism_core import program

def materialize(obligation,state):
    rule=obligation['rule'];target=obligation['target'];fn=obligation['function']
    if rule not in ('AC-04','FCR-MINT'):return []
    lookup,paths,errors=program(state,target,normalize_writes=False)
    cache=state.setdefault('_question_model_rows',{})
    if (target,rule) not in cache:
        if rule=='AC-04':
            from .m03_p_lifecycle import analyze_lifecycle
            from .m04_lifecycle_relations import analyze_validity
            from .m04_phase_lifecycle import analyze_phases
            from .m04_quota_lifecycle import analyze_quotas
            from .m03_p_assets import asset_models
            candidates=[]
            for analyzer in (analyze_lifecycle,analyze_validity,analyze_phases):
                rows,gaps=analyzer(lookup.bundle,lookup,paths,[]);candidates.extend(rows)
            rows,_=analyze_quotas(lookup.bundle,lookup,paths,[],asset_models(lookup,paths));candidates.extend(rows)
        else:
            from .m05_asset_registry import transferable_models,mint_rows
            candidates=[]
            for model in transferable_models(lookup,paths):candidates.extend(mint_rows(lookup.bundle,lookup,paths,model,[])[0])
        cache[(target,rule)]=candidates
    result=[]
    existing={digest([b['row']['rule'],b['row']['function'],b['row']['effect'],b['row']['conditions'],b['row'].get('policy_basis')]):ref
        for ref,b in state['bindings'].items() if b.get('target')==target and 'row' in b}
    for row in cache[(target,rule)]:
        if row['function']!=fn:continue
        identity=digest([row['rule'],row['function'],row['effect'],row['conditions'],row.get('policy_basis')])
        ref=existing.get(identity)
        if ref is None:
            ref='source_model_'+digest([target,identity])[:24]
            state['bindings'][ref]={'target':target,'row':copy.deepcopy(row),'constructed_from_source_question':True}
        result.append(ref)
    return result
