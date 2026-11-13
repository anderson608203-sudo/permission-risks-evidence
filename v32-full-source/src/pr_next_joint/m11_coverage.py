"""Expose effective checking separately from finite binary classification."""
import copy
from .m03_p_paths import key,walk
from .m03_p_route import selectors

def scope_query(q,state):
    paths=state['paths'].get((q['target'],q['function']),[]);pi=q.get('path_index')
    if not isinstance(pi,int) or pi>=len(paths):return q
    path=paths[pi];effect=q.get('effect',{});selector=effect.get('selector',{})
    roots={s['root'] for s in selectors([effect,q.get('required_policy_candidate'),q.get('conditions',[])])}
    q['local_dependency_scope']={'resource_roots':sorted(roots),'conditions_preserved':True,
        'evaluation_terms_preserved':True,'tail_revert_call_and_overwrite_constraints_preserved':True,
        'unrelated_diagnostics_are_not_automatically_dropped':True}
    if selector.get('kind')=='storage' and q.get('rule') in ('AC-01','AC-02','AC-03'):
        matches=[w for w in path['writes'] if key(w['path'])==key(selector)]
        if matches and matches[-1]['source']!=effect.get('source'):
            final=matches[-1]
            q['commit_effect']={'original_source':effect.get('source'),'final_source':final['source'],
                'original_value':copy.deepcopy(effect.get('value')),'basis':'last exact-selector source write on this path'}
            q['effect']['value']=copy.deepcopy(final['value'])
            # Effects observable by an intervening external call cannot be
            # declared harmless solely because final storage is restored.
            if path.get('sensitive_effects'):
                q.setdefault('issues',[]).append({'reason':'intermediate_write_external_observer_requires_composed_query','source':effect.get('source')})
    return q

def coverage(context,state,checks):
    result=[]
    for o in context['operations']:
        relevant=[q for q in checks if q['target']==o['target'] and q['function']==o['function']]
        effects={}
        for pi,p in enumerate(state['paths'].get((o['target'],o['function']),[])):
            if p['flow']=='reverted':continue
            for effect in p['writes']+p.get('sensitive_effects',[]):
                source=effect.get('source',{});identity=key(source)
                item=effects.setdefault(identity,{'source':source,'path_indexes':[],'query_ids':[],
                    'effect_kind':effect.get('kind','storage_write'),'process_status':'no_supported_policy_or_model','path_coverage':[]})
                item['path_indexes'].append(pi)
                matched=[q for q in relevant if (q.get('effect',{}).get('source') or q.get('source') or q.get('source_model',{}).get('effect',{}).get('source'))==source and q.get('path_index',pi)==pi]
                item['query_ids'].extend(q['id'] for q in matched)
                statuses=[]
                for q in matched:
                    f=q.get('formal',{})
                    statuses.append('risk_reported' if q.get('reportable') else
                        'normal_or_inapplicable_source_evidence' if f.get('source_normal_alternative') else
                        'checked_no_risk_matched' if f.get('status')=='refuted_in_scope' else
                        'infeasible_model_premise' if f.get('reason')=='premise_unsat' else 'limited_semantic_check')
                priority=['risk_reported','normal_or_inapplicable_source_evidence','checked_no_risk_matched','infeasible_model_premise','limited_semantic_check']
                local=next((x for x in priority if x in statuses),'no_supported_policy_or_model')
                item['path_coverage'].append({'path_index':pi,'status':local,'query_ids':[q['id'] for q in matched],'source_issue_count':len(p.get('issues',[]))})
                observed={x['status'] for x in item['path_coverage']}
                item['process_status']=next(iter(observed)) if len(observed)==1 else 'mixed_path_results_see_path_coverage'
        result.append({'operation':o['id'],'target':o['target'],'function':o['function'],'effects':list(effects.values()),
                       'is_final_classification':False,'empty_queries_do_not_prove_safety':True})
    return result
