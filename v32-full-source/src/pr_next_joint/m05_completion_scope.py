"""Conclude requested operations from checked evidence, not LLM prose."""
import copy
from .core import digest
from .task_scope import ALL,requested,aggregate
from .task_relevance import inventory

CONCLUSIVE=('supported','refuted_in_scope')
def summarize(context,state,report):
    active=requested(context);relevance=inventory(context,state)
    rows=[r for r in report.get('results',[])+report.get('source_obligation_checks',[]) if not r.get('superseded_by')]
    reviews={(r.get('target'),r.get('function')):r for r in report.get('function_reviews',[])}
    questions=report.get('source_obligations',[])
    scoped={r:{'status':'not_requested','scope_records':[],'unresolved':[],'positive_query_ids':[],
               'analysis_complete_in_scope':False,'operation_dispositions':[]} for r in ALL}
    for rule in active:scoped[rule]['status']='pending'
    excluded=[]
    def gap(rule,target,function,reason,**details):
        if rule not in active:return
        scoped[rule]['unresolved'].append({'target':target,'function':function,'reason':reason,**details})
    for target in context['targets']:
        tid=target['id']
        for function in target['functions']:
            fn=function['function'];rel=relevance[(tid,fn)]
            paths=state['paths'].get((tid,fn),[]);review=reviews.get((tid,fn))
            for rule in active:
                relevant=rule in rel['possible_rules'];proof=rel.get('exclusions',{}).get(rule)
                item={'target':tid,'function':fn,'relevant':relevant,'M2_review':review.get('disposition') if review else None,
                      'source_paths':len(paths),'dependency_index_sha256':digest(rel),
                      'not_relevant_basis':proof or ('resolved_source_operation_dependency_index' if not relevant else None)}
                scoped[rule]['scope_records'].append(item)
                if not relevant:
                    scoped[rule]['operation_dispositions'].append({'target':tid,'function':fn,'status':'not_applicable_checked',
                        'basis':item['not_relevant_basis']})
                    continue
                checked=[r for r in rows if (r.get('target'),r.get('function'),r.get('rule'))==(tid,fn,rule)]
                pending=[o for o in questions if not o.get('superseded_by') and (o.get('target'),o.get('function'),o.get('rule'))==(tid,fn,rule)]
                positive=any(r.get('reportable') for r in checked)
                inconclusive=[r for r in checked if r.get('status') not in CONCLUSIVE]
                # An operation-wide source certificate can close a necessary
                # condition regardless of unrelated value lowering.
                pclosed=any(r.get('status')=='refuted_in_scope' and
                    r.get('program_analysis_certificate',{}).get('verified') and
                    r.get('program_analysis_certificate',{}).get('kind')=='necessary_condition_absent' for r in checked)
                if pclosed:
                    scoped[rule]['operation_dispositions'].append({'target':tid,'function':fn,'status':'not_applicable_checked',
                        'check_ids':[r['id'] for r in checked if r.get('program_analysis_certificate',{}).get('verified')]})
                    continue
                if not review:gap(rule,tid,fn,'M2_relevant_operation_review_missing')
                # A hypothetical rejected candidate is not a proof by itself.
                if not checked and not positive:
                    gap(rule,tid,fn,'relevant_operation_without_program_check')
                path_gaps=[{'path_index':i,'issues':p.get('issues',[]),'evaluation_gaps':p.get('evaluation_gaps',[]),'flow':p.get('flow')}
                           for i,p in enumerate(paths) if p.get('issues') or p.get('evaluation_gaps') or p.get('flow')=='truncated']
                if not paths or function.get('extraction_errors') or path_gaps:
                    gap(rule,tid,fn,'relevant_source_semantics_incomplete',path_gaps=path_gaps,extraction_errors=function.get('extraction_errors',[]))
                for r in inconclusive:gap(rule,tid,fn,'query_inconclusive',evidence_ref=r['id'])
                for ob in pending:
                    ob_rows=[r for r in checked if r.get('obligation_id')==ob['id'] or r['id'] in ob.get('legacy_bridge',{}).get('query_ids',[])]
                    model_gaps=[g for g in ob.get('model_gaps',[]) if g.get('reason')!='original_source_question_retained; ordinary_query_links_separate']
                    if ob.get('classification_stop') and positive:continue
                    if model_gaps or not ob_rows or any(r.get('status') not in CONCLUSIVE for r in ob_rows):
                        gap(rule,tid,fn,'source_question_not_conclusively_checked',evidence_ref=ob['id'],model_gaps=model_gaps)
                if checked and not positive:
                    # Preserve all existing same-rule candidate models; one
                    # refuted query cannot silently retire another candidate.
                    candidates=[c for c in context.get('candidate_relations',[]) if
                                (c['target'],c['function'],c['rule'])==(tid,fn,rule)]
                    handled={r.get('binding_ref') for r in checked if r.get('status') in CONCLUSIVE}
                    for c in candidates:
                        if c['id'] not in handled:
                            gap(rule,tid,fn,'candidate_not_program_checked',evidence_ref=c['id'])
                    if rule in ('AC-01','AC-02','AC-03'):
                        covered={(r.get('path_index'),r.get('effect',{}).get('source',{}).get('ast_id')) for r in checked if r.get('status') in CONCLUSIVE}
                        needed={(i,w.get('source',{}).get('ast_id')) for i,p in enumerate(paths) if p.get('flow') in ('normal','returned')
                            for w in p.get('writes',[])+p.get('sensitive_effects',[])}
                        if rule!='AC-01':
                            needed={(c['path_index'],c.get('source',{}).get('ast_id')) for c in candidates}
                        if not needed<=covered:
                            gap(rule,tid,fn,'sensitive_effect_not_program_checked',path_effect_pairs=sorted(needed-covered,key=str))
                scoped[rule]['operation_dispositions'].append({'target':tid,'function':fn,
                    'status':'risk_supported' if positive else 'checked' if checked else 'unresolved',
                    'check_ids':[r['id'] for r in checked]})
    # Bind errors retain their exact operation/rule; an unlocatable error is
    # conservatively task-wide. An unrelated, source-checked exclusion is saved.
    for error in report.get('failures',[])+report.get('source_obligation_errors',[]):
        proposal=error.get('original_proposal') or error.get('entry') or {}
        tid=error.get('target',proposal.get('target'));fn=error.get('function',proposal.get('function'))
        rule=error.get('rule',proposal.get('rule'))
        if tid is None and isinstance(error.get('target_contract'),dict):
            tc=error['target_contract']
            if tc.get('file') and tc.get('contract'):tid=tc['file']+':'+tc['contract']
        if tid is None or fn is None:
            ref=proposal.get('candidate_id') or proposal.get('write_id') or proposal.get('effect_id')
            bound=state.get('bindings',{}).get(ref,{})
            tid=tid or bound.get('target');fn=fn or bound.get('function',bound.get('row',{}).get('function'))
        rel=relevance.get((tid,fn))
        affected=[rule] if rule in active else [r for r in active if rel is None or r in rel['possible_rules']]
        for r in affected:
            if rel and r not in rel['possible_rules']:
                excluded.append({'target':tid,'function':fn,'rule':r,'error':copy.deepcopy(error),'basis':rel.get('exclusions',{}).get(r,'source_operation_index')})
            else:gap(r,tid,fn,'binding_or_preparation_failure',details=copy.deepcopy(error))
    for rule in active:
        item=scoped[rule]
        positive=[r['id'] for r in rows if r.get('rule')==rule and r.get('reportable')]
        item['positive_query_ids']=positive
        item['unresolved']=list({digest(x):x for x in item['unresolved']}.values())
        complete=bool(item['scope_records']) and not item['unresolved']
        item['status']='positive' if positive else 'completed_without_alarm_in_scope' if complete else 'unknown'
        item['analysis_complete_in_scope']=complete
        if complete and not positive:
            item['negative_scope_certificate']={'kind':'completed_requested_detector_scan','source_identity':context['identity'],
                'reviewed_operation_scope_sha256':digest(item['scope_records']),'dispositions_sha256':digest(item['operation_dispositions']),
                'checks':[r['id'] for r in rows if r.get('rule')==rule],'no_decisive_gap':True,'not_a_safety_proof':True}
    return {'schema':'task-classification-completion-v3','analysis_scope':context.get('analysis_scope','joint'),'rules':scoped,
            'completed_labels':[r for r in active if scoped[r]['analysis_complete_in_scope']],
            'task_classification':aggregate(context.get('analysis_scope','joint'),scoped),
            'excluded_non_target_dependencies':excluded,'relevance_index':list(relevance.values()),
            'scope':'requested detector and supplied source, not whole-program safety','evaluation_labels_read':False}
