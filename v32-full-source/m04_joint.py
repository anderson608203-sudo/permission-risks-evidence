"""One project through M1 graph, mandatory M2, bound M3 and formal M4."""
from .llm_stream import expected_wire_request
import argparse,copy,importlib,json,time
from pathlib import Path
from .core import digest,require
from .m03_source import inspect_manifest,validate_loaded_artifacts
from .m04_joint_context import build,messages,SCHEMA
from .m04_joint_queries import bind
from .m04_joint_formal import check
from .m04_joint_normalize import normalize_response
from .m04_joint_protocol import bind_envelope
from .m04_joint_controls import add_controls,assess_policy,assess_remarks
from .m04_joint_graph_obligations import add_graph_controls
from .m05_joint_obligations import enrich,extension_instruction,bind_obligations,NEW_RULES
from .m05_common_semantics import analyze as analyze_common,attach_report as attach_common

def save(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    temp=p.with_name(p.name+'.tmp');temp.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8');temp.replace(p)
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def check_queries(queries,rows,context,state,real,out):
    from .task_scope import requested
    for q in queries:
        if q['rule'] not in requested(context):continue
        if q["id"] in {r["id"] for r in rows}:continue
        stable=[r for r in rows if r.get('reportable') and not (r.get('policy_scope')=='inferred_policy' and r.get('alternatives'))]
        supports=[r['id'] for r in stable if context.get('analysis_scope')=='AC' or r['rule']==q['rule']]
        if real and supports:
            state.setdefault('classification_stops',[]).append({'query_id':q['id'],'rule':q['rule'],'support_ids':supports,'reason':'target_classification_already_supported','solver_called':False})
            continue
        assessments,blocking=assess_remarks(q)
        applicability=assess_policy(q,context)
        if blocking:
            result={'status':'inconclusive','reason':'M2_query_blocking_gap','solver_called':False,'query':'not_encoded'}
        else:
            started=time.perf_counter();result=check(state['lookups'][q['target']],q);result['wall_seconds']=time.perf_counter()-started
        smt=result.pop('smt2',None)
        if smt:
            artifact=out/'formal'/f"{q['id']}.smt2";artifact.parent.mkdir(exist_ok=True);artifact.write_text(smt,encoding='utf8');result['smt2_artifact']='formal/'+artifact.name
        # SAT under an unjustified narrower policy is not a risk finding.
        status='inconclusive' if applicability else result['status']
        if q.get('negative_control_only') and status=='supported':
            status='inconclusive'
            result['negative_control_conflict']='candidate not refuted; a rejected/normal review is not a positive endorsement'
        rows.append({**q,'status':status,'formal':result,'remark_assessments':assessments,'policy_assessment':applicability,
                     'program_analysis_certificate':copy.deepcopy(result.get('program_analysis_certificate',{})),
                     'reportable':status=='supported' and real,
                     'diagnostic_only':not real,'execution_status':'not_run','evidence_types':['P','M'] if result.get('solver_called') else ['P']})


def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('--route',choices=['joint'],default='joint');p.add_argument('--targets',choices=['project'],default='project')
    for name in ('root','case','out'):p.add_argument('--'+name,required=True)
    for name in ('manifest','bundle','native'):p.add_argument('--'+name)
    p.add_argument('--compiled-unit',help='identity-checked retained compilation unit; no compilation or label input')
    p.add_argument('--phase',choices=['prepare','all'],default='all');p.add_argument('--llm-module');p.add_argument('--fixture-response')
    p.add_argument('--analysis-scope',choices=['AC','FCR','joint'],required=True)
    p.add_argument('--proposal-scope',choices=['legacy','source_obligations_v1'],default='legacy')
    p.add_argument('--coverage-llm-module')
    p.add_argument('--coverage-fixture-response')
    p.add_argument('--semantic-review-llm-module')
    p.add_argument('--semantic-review-fixture-response')
    a=p.parse_args(argv);root=Path(a.root).resolve();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
    require(not (out/'joint_report.json').exists(),'JOINT_PRESERVE_EXISTING_REPORT')
    require(not ((a.coverage_llm_module or a.coverage_fixture_response) and (a.semantic_review_llm_module or a.semantic_review_fixture_response)),'ONE_SHARED_FOLLOWUP_CHANNEL_ONLY')
    stages=[];active='M1';receipt=None;wall_started=time.perf_counter();last_stage=wall_started
    def stage(name,status,**detail):
        nonlocal active,last_stage
        stamp=time.perf_counter();active=name;stages.append({'module':name,'status':status,'elapsed_since_previous_stage_seconds':stamp-last_stage,'elapsed_since_entry_seconds':stamp-wall_started,**detail});last_stage=stamp;save(out/'stage_log.json',stages)
    try:
        stage('M1','started')
        selected_targets=None;intake=None
        if a.compiled_unit:
            require(not any((a.manifest,a.bundle,a.native)),'DATASET_CONFLICTING_INTAKES')
            from .dataset_intake import load_compiled_unit
            intake=load_compiled_unit(root,a.compiled_unit)
            require(a.case==intake['unit_id'],'DATASET_CASE_ID_MISMATCH')
            bundle,native,binding=intake['bundle'],intake['native'],intake['binding']
            sources,description=intake['sources'],intake['description']
            selected_targets=intake['selected_targets']
            save(out/'intake_receipt.json',intake['receipt'])
            save(out/'target_inventory.json',intake['receipt']['target_inventory'])
        else:
            require(all((a.manifest,a.bundle,a.native)),'JOINT_LEGACY_INPUT_REQUIRED')
            inspection=inspect_manifest(root,a.manifest,target_mode='project');case=next(c for c in inspection['cases'] if c['case_id']==a.case)
            bundle,native=read(a.bundle),read(a.native);binding=validate_loaded_artifacts(case,bundle,native)
            description=None
            if case.get('project_description'):
                file=(root/case['project_description']).resolve();require(file.is_relative_to(root),'JOINT_DESCRIPTION_PATH');description=file.read_text(encoding='utf-8-sig')
            sources=[]
            for s in binding['sources']:
                file=(root/s['file']).resolve();require(file.is_relative_to(root),'JOINT_SOURCE_PATH')
                sources.append({'file':s['file'],'sha256':s['sha256'],'content':file.read_bytes().decode('utf8')})
        save(out/'artifact_binding.json',binding)
        context,state=build(bundle,native,description,sources,selected_targets=selected_targets,analysis_scope=a.analysis_scope)
        if intake is not None:
            # Failed/omitted targets remain visible even when no M2 target can be built.
            save(out/'target_inventory.json',state['analysis']['target_inventory'])
            save(out/'target_preparation_failures.json',state['analysis']['failures'])
            require(bool(context['targets']),'DATASET_NO_ANALYZABLE_TARGETS')
        extended=a.proposal_scope=='source_obligations_v1'
        if extended:context=enrich(context,state)
        msg=messages(context)
        if extended:msg[0]['content']+='\n'+extension_instruction(context)
        save(out/'m1_context.json',context);save(out/'m2_messages.json',msg)
        stage('M1','completed',targets=len(context['targets']),graph_ids=[t['graph']['id'] for t in context['targets']])
        if a.phase=='prepare':
            save(out/'entry_result.json',{'status':'awaiting_real_llm','messages_digest':digest(msg),'real_llm':False});return 0
        stage('M2','started');require(bool(a.llm_module)!=bool(a.fixture_response),'JOINT_REAL_LLM_REQUIRED_OR_EXPLICIT_DIAGNOSTIC')
        if a.fixture_response:
            response=read(a.fixture_response);receipt={'source_nature':'explicit_test_double','simulated':True};real=False
        else:
            module,attr=a.llm_module.split(':',1);client=getattr(importlib.import_module(module),attr)()
            response,receipt=client.call(msg,'m04_joint_proposal',max_tokens=None,timeout=1800,reasoning_effort='high',thinking=True)
            save(out/'llm_receipt.json',receipt);save(out/'raw_response.json',response)
            require(response is not None and receipt.get('status')=='json_received','JOINT_LLM_RESPONSE_FAILED')
            expected={'model':'deepseek-flash','messages':msg,'response_format':{'type':'json_object'},'thinking':{'type':'enabled'},'reasoning_effort':'high','stream':False}
            require(receipt.get('request_sha256')==digest(expected_wire_request(expected,receipt)) and receipt.get('response_sha256')==digest(response),'JOINT_LLM_RECEIPT_IDENTITY')
            real=receipt.get('source_nature')=='real' and receipt.get('simulated') is False
            require(real,'JOINT_CLIENT_NOT_AUTHENTIC')
        save(out/'raw_response.json',response);save(out/'llm_receipt.json',receipt)
        stage('M2','completed',real_llm=real,request_id=receipt.get('request_id'))
        stage('M3','started')
        normalized,conversion=normalize_response(response,context,state,authenticated=real)
        save(out/'normalized_response.json',normalized);save(out/'response_conversion.json',conversion)
        obligations=bind_obligations(normalized,context,state) if extended else None
        queries,coverage=bind(normalized,context,state)
        from .m05_existing_query_bridge import SourceQueryBridge
        source_bridge=SourceQueryBridge()
        if extended:source_bridge.enqueue(obligations,context,state,queries,coverage,{'channel':'primary','request_id':receipt.get('request_id'),'response_sha256':digest(response),'diagnostic_only':not real})
        candidate_coverage=None
        if extended:
            from .m05_candidate_coverage import inventory,supplement_messages,validate_supplement
            candidate_coverage=inventory(context,state,normalized,obligations,bound_queries=queries)
            save(out/'candidate_coverage.json',candidate_coverage)
            candidate_coverage['supplement_status']='not_requested'
            if (a.coverage_llm_module or a.coverage_fixture_response) and candidate_coverage['pending_count']:
                supplement_msg=supplement_messages(context,candidate_coverage,receipt)
                save(out/'coverage_messages.json',supplement_msg)
                candidate_coverage['supplement_messages_digest']=digest(supplement_msg)
                # A distinct authenticated request, never a rewrite or replay
                # of the original response. Failure preserves the base result.
                try:
                    require(not(a.coverage_llm_module and a.coverage_fixture_response),'COVERAGE_ONE_SOURCE')
                    if a.coverage_fixture_response:
                        require(bool(a.fixture_response) and not real,'COVERAGE_FIXTURE_REQUIRES_DIAGNOSTIC_BASE')
                        supplement=read(a.coverage_fixture_response)
                        supplement_receipt={'source_nature':'explicit_test_double','simulated':True,'status':'diagnostic_only'}
                    else:
                        module,attr=a.coverage_llm_module.split(':',1)
                        supplement_client=getattr(importlib.import_module(module),attr)()
                        supplement,supplement_receipt=supplement_client.call(supplement_msg,'m05_coverage_supplement',max_tokens=None,timeout=1800,reasoning_effort='high',thinking=True)
                    save(out/'coverage_receipt.json',supplement_receipt);save(out/'coverage_raw_response.json',supplement)
                    if not a.coverage_fixture_response:
                        require(supplement is not None and supplement_receipt.get('status')=='json_received','COVERAGE_RESPONSE_FAILED')
                        expected_supplement={'model':'deepseek-flash','messages':supplement_msg,'response_format':{'type':'json_object'},'thinking':{'type':'enabled'},'reasoning_effort':'high','stream':False}
                        require(supplement_receipt.get('request_sha256')==digest(expected_wire_request(expected_supplement,supplement_receipt)) and supplement_receipt.get('response_sha256')==digest(supplement),'COVERAGE_RECEIPT_IDENTITY')
                        require(supplement_receipt.get('source_nature')=='real' and supplement_receipt.get('simulated') is False,'COVERAGE_CLIENT_NOT_AUTHENTIC')
                    supplement,envelope=bind_envelope(supplement,{
                        'identity':context['identity'],'inventory_digest':candidate_coverage['inventory_digest'],
                        'primary_request_sha256':receipt.get('request_sha256')},
                        authenticated=real and not a.coverage_fixture_response)
                    save(out/'coverage_normalized_response.json',supplement)
                    save(out/'coverage_response_conversion.json',envelope)
                    additions,reviews=validate_supplement(supplement,context,candidate_coverage,receipt,{o['id'] for o in normalized.get('source_obligations',[])},state)
                    combined={**normalized,'source_obligations':normalized.get('source_obligations',[])+additions}
                    next_obligations=bind_obligations(combined,context,state)
                    next_bridge=copy.deepcopy(source_bridge);next_queries=copy.deepcopy(queries);next_coverage=copy.deepcopy(coverage)
                    next_bridge.enqueue(next_obligations,context,state,next_queries,next_coverage,{'channel':'coverage','request_id':supplement_receipt.get('request_id'),'response_sha256':digest(supplement),'diagnostic_only':not real})
                    next_inventory=copy.deepcopy(candidate_coverage)
                    next_inventory.update(supplement_status='diagnostic_fixture_bound' if a.coverage_fixture_response else 'authenticated_review_bound',supplement_request_id=supplement_receipt.get('request_id'),supplement_reviews=reviews,supplement_obligation_ids=[o['id'] for o in additions])
                    save(out/'combined_response.json',combined)
                    obligations,source_bridge,queries,coverage,candidate_coverage=next_obligations,next_bridge,next_queries,next_coverage,next_inventory
                except Exception as ex:
                    candidate_coverage.update(supplement_status='failed_base_preserved',supplement_error=type(ex).__name__+':'+str(ex))
            save(out/'candidate_coverage.json',candidate_coverage)
        if extended:save(out/'source_obligations.json',obligations)
        stage('M3','completed',bound_queries=len(queries),errors=len(coverage['proposal_binding_errors']))
        stage('M4','started');rows=[];common_model=None
        queries,coverage=add_controls(queries,coverage,context,state)
        queries,coverage,query_graphs=add_graph_controls(queries,coverage,context,state)
        save(out/'query_graphs.json',query_graphs)
        check_queries(queries,rows,context,state,real,out)
        if extended:
            from .m05_obligation_checks import evaluate
            obligations=evaluate(obligations,state,real)
            save(out/'before_followup.json',{'ordinary_results':rows,'source_results':obligations,'identity':context['identity']})
            semantic_followup={'status':'not_requested','new_api_automatically_requested':False}
            if a.semantic_review_llm_module or a.semantic_review_fixture_response:
                from .m05_candidate_coverage import semantic_review_inventory,semantic_review_messages
                from .m05_semantic_followup import questions,partition,stage_checked
                from .m05_relation_contributions import prepare as prepare_contributions,consumption
                prior_review=semantic_review_inventory(context,candidate_coverage,obligations,state,ordinary_rows=rows)
                save(out/'semantic_review_prior_inventory.json',prior_review)
                save(out/'semantic_review_parent_binding.json',{
                    'identity':context['identity'],
                    'primary_request_id':receipt.get('request_id'),
                    'primary_request_sha256':receipt.get('request_sha256'),
                    'primary_response_sha256':digest(response),
                    'review_digest':prior_review['digest'],
                    'review_inventory_sha256':digest(prior_review)})
                supplement_receipt=None
                followup_work=None
                def record_followup_work(phase,bound,checked):
                    nonlocal followup_work
                    calls=None if checked is None else sum(bool(r.get('formal',{}).get('solver_called')) for r in checked['source_obligation_checks'])
                    unknown=checked is None or any(p.get('work_accounting_unknown') for p in checked['rule_stage_progress'].values())
                    followup_work={'phase':phase,'known_formal_checks_called':calls,
                        'work_accounting_unknown':unknown,'admitted_to_results':False,
                        'artifact_persisted':False,
                        'evidence_artifact':'semantic_review_staged_work.json',
                        'scope':'actual attempted work; not an accepted risk conclusion'}
                    saved_work={**followup_work,'artifact_persisted':True}
                    save(out/'semantic_review_staged_work.json',{'work':saved_work,'bound':bound,'checked':checked})
                    followup_work=saved_work
                try:
                    require(bool(a.semantic_review_llm_module)!=bool(a.semantic_review_fixture_response),'SEMANTIC_REVIEW_ONE_SOURCE')
                    if not questions(prior_review):
                        semantic_followup['status']='no_pending_relation_questions'
                    else:
                        review_msg=semantic_review_messages(context,prior_review,obligations)
                        save(out/'semantic_review_request_messages.json',review_msg)
                        if a.semantic_review_fixture_response:
                            require(bool(a.fixture_response) and not real,'SEMANTIC_REVIEW_FIXTURE_REQUIRES_DIAGNOSTIC_BASE')
                            supplement=read(a.semantic_review_fixture_response)
                            supplement_receipt={'source_nature':'explicit_test_double','simulated':True}
                        else:
                            module,attr=a.semantic_review_llm_module.split(':',1)
                            client=getattr(importlib.import_module(module),attr)()
                            supplement,supplement_receipt=client.call(review_msg,'m05_semantic_relation_review',max_tokens=None,timeout=1800,reasoning_effort='high',thinking=True)
                        save(out/'semantic_review_response.json',supplement);save(out/'semantic_review_receipt.json',supplement_receipt)
                        if not a.semantic_review_fixture_response:
                            require(supplement is not None and supplement_receipt.get('status')=='json_received','SEMANTIC_REVIEW_RESPONSE_FAILED')
                            expected_review={'model':'deepseek-flash','messages':review_msg,'response_format':{'type':'json_object'},'thinking':{'type':'enabled'},'reasoning_effort':'high','stream':False}
                            require(supplement_receipt.get('request_sha256')==digest(expected_wire_request(expected_review,supplement_receipt)) and supplement_receipt.get('response_sha256')==digest(supplement),'SEMANTIC_REVIEW_RECEIPT_IDENTITY')
                            require(supplement_receipt.get('source_nature')=='real' and supplement_receipt.get('simulated') is False,'SEMANTIC_REVIEW_NOT_AUTHENTIC')
                        supplement,envelope=bind_envelope(supplement,{
                            'identity':context['identity'],'review_digest':prior_review['digest']},
                            authenticated=real and not a.semantic_review_fixture_response)
                        save(out/'semantic_review_normalized_response.json',supplement)
                        save(out/'semantic_review_response_conversion.json',envelope)
                        accepted=partition(supplement,context,prior_review,obligations['source_obligations'])
                        save(out/'semantic_review_partition.json',accepted)
                        extra,choice_errors=prepare_contributions(accepted,supplement,prior_review,obligations,context,state,supplement_receipt.get('request_id'))
                        from .m05_checked_revisions import validate_requests
                        revision_requests,revision_errors=validate_requests(supplement,obligations,extra,rows)
                        choice_errors.extend(revision_errors)
                        staged=stage_checked(obligations,extra,source_bridge,context,state,queries,coverage,{'channel':'semantic','request_id':supplement_receipt.get('request_id'),'response_sha256':digest(supplement),'diagnostic_only':not real},real,record_followup_work)
                        next_obligations,next_extra,checked_extra,next_bridge,next_queries,next_coverage=staged
                        next_followup=consumption(accepted,next_extra,checked_extra,choice_errors,supplement_receipt.get('request_id'),real)
                        next_followup['work_receipt']={**followup_work,'phase':'committed','admitted_to_results':True,
                            'counting':'already included in source_obligation_checks; do not add twice'}
                        obligations,source_bridge,queries,coverage=next_obligations,next_bridge,next_queries,next_coverage
                        next_followup['revision_requests']=revision_requests
                        semantic_followup=next_followup
                except Exception as ex:
                    semantic_followup={'status':'failed_base_preserved','error':type(ex).__name__+':'+str(ex),
                        'request_id':(supplement_receipt or {}).get('request_id'),
                        'receipt_status':(supplement_receipt or {}).get('status'),
                        'error_class':(supplement_receipt or {}).get('error_class'),
                        'delivery':(supplement_receipt or {}).get('delivery'),
                        'new_api_automatically_requested':False,'original_results_preserved':True,
                        'non_admitted_work':followup_work}
                save(out/'semantic_followup.json',semantic_followup)
            for checked in obligations['source_obligation_checks']:
                smt=checked['formal'].pop('smt2',None)
                if smt:
                    artifact=out/'formal'/f"{checked['id']}.smt2";artifact.parent.mkdir(exist_ok=True)
                    artifact.write_text(smt,encoding='utf8');checked['formal']['smt2_artifact']='formal/'+artifact.name
            save(out/'source_obligations.json',obligations)
            common_model=analyze_common(context,normalized,obligations)
        save(out/'queries.json',queries);save(out/'coverage.json',coverage)
        check_queries(queries,rows,context,state,real,out)
        if extended:
            bridge_execution=source_bridge.report(rows)
            semantic_links=[d for d in bridge_execution['derivations'] if d['origin']['channel']=='semantic']
            semantic_ids={qid for d in semantic_links for qid in d['query_ids']}
            called={r['id'] for r in rows if r['id'] in semantic_ids and r['formal'].get('solver_called')}
            semantic_followup['legacy_query_ids']=sorted(semantic_ids)
            semantic_followup['legacy_formal_checks']=len(called)
            semantic_followup['new_formal_checks_scope']='source_obligation_checks only; legacy_formal_checks counted separately in ordinary results'
            for contribution in semantic_followup.get('contributions',[]):
                qids={qid for d in semantic_links if d['source_obligation_id']==contribution['obligation_id'] for qid in d['query_ids']}
                contribution['legacy_query_ids']=sorted(qids)
                contribution['legacy_formal_check_ids']=sorted(qids&called)
                if qids&called:contribution['stage']='formally_checked_in_ordinary_query_channel'
            if called:semantic_followup['status']='authenticated_ordinary_formal_checks' if real else 'diagnostic_ordinary_formal_checks'
            save(out/'semantic_followup.json',semantic_followup)
        if extended:
            from .m05_checked_revisions import apply_checked
            semantic_followup['checked_revisions']=apply_checked(semantic_followup.get('revision_requests',[]),obligations,rows)
            from .m05_question_plan import execution_ledger,annotate_fcr
            for row in rows+obligations['source_obligation_checks']:annotate_fcr(row)
            question_ledger=execution_ledger(obligations,rows,source_bridge.report(rows))
            save(out/'question_execution_ledger.json',question_ledger)
            save(out/'after_followup.json',{'ordinary_results':rows,'source_results':obligations,'identity':context['identity'],
                'checked_revisions':semantic_followup['checked_revisions']})
            save(out/'semantic_followup.json',semantic_followup)
        groups={}
        for row in rows:
            if not row['reportable']:continue
            selector=row['effect']['selector'];scope={'target':row['target'],'function':row['function'],'root':selector.get('root'),'effect_kind':row['effect'].get('kind','storage_write'),'effect_source':selector.get('source_id'),
                'keys':[x['key'] for x in selector.get('segments',[]) if 'key' in x]}
            group=groups.setdefault(digest(scope),{'scope':scope,'rules':[],'queries':[]})
            if row['rule'] not in group['rules']:group['rules'].append(row['rule'])
            group['queries'].append(row['id'])
        formal_count=sum(bool(r['formal']['solver_called']) for r in rows)
        if extended:
            for checked in obligations['source_obligation_checks']:
                if not checked['reportable']:continue
                scope={'target':checked['target'],'function':checked['function'],
                       'root':checked['asset_root'],'keys':[checked['holder']]}
                group=groups.setdefault(digest(scope),{'scope':scope,'rules':[],'queries':[]})
                if checked['rule'] not in group['rules']:group['rules'].append(checked['rule'])
                group['queries'].append(checked['id'])
        gaps=coverage['uncovered']+[{'target':t['id'],**s,'reason':'special_entry_not_lowered'} for t in context['targets'] for s in t['special_entries'] if not s.get('lowered')]
        gaps += [{'query':r['id'],'reason':(r['policy_assessment'] or {}).get('reason',r['formal']['reason'])} for r in rows if r['status']=='inconclusive']
        for t in context['targets']:gaps.extend({'target':t['id'],**g} for g in t['unlowered'])
        full=bool(real and queries and formal_count)
        report={'schema':'m04-joint-report-v1','identity':context['identity'],'status':'joint_partial' if full and (gaps or coverage['proposal_binding_errors']) else 'joint_completed' if full else 'joint_incomplete' if real else 'diagnostic_only',
                'full_framework_executed':full,'real_llm':real,'request_id':receipt.get('request_id'),'messages_digest':digest(msg),
                'graph_ids':[t['graph']['id'] for t in context['targets']],'proposal_count':len(response['proposals']),'bound_query_count':len(queries),
                'formal_checks_called':formal_count,'results':rows,'risk_groups':list(groups.values()),'reportable_findings':len(groups),
                'failures':coverage['proposal_binding_errors']+coverage['coverage_errors'],'uncovered':gaps,
                'scope':'conditional inferred policies, source-bound paths/transitions/accounting; no whole-program or deployed reachability guarantee',
                'not_a_safety_conclusion':True,'targets':[t['id'] for t in context['targets']], 'function_reviews':coverage['function_reviews'],
                'response_conversion':conversion,'derived_control_queries':coverage['derived_control_queries'],
                'non_state_effect_reviews':coverage['non_state_effect_reviews'],
                'query_graphs':query_graphs,'graph_frame_controls':coverage['graph_frame_controls']}
        if extended:
            report['question_execution_ledger']=question_ledger
            report['definition_revision']='fcr-mechanism-r1-20261027'
            report['proposal_scope']=a.proposal_scope
            report['semantic_followup']=semantic_followup
            report['candidate_coverage']=candidate_coverage
            report.update({k:obligations[k] for k in ('source_obligations','source_obligation_errors','rule_stage_progress','source_obligation_checks')})
            report['new_direction_formal_checks_called']=obligations['formal_checks_called']
            report['total_formal_checks_called']=formal_count+obligations['formal_checks_called']
            work=semantic_followup.get('non_admitted_work') or {}
            report['non_admitted_followup_work']=work
            report['actual_formal_work_accounting']={'accepted_checks':report['total_formal_checks_called'],
                'non_admitted_known_checks':work.get('known_formal_checks_called',0),
                'unknown_internal_work':bool(work.get('work_accounting_unknown') or any(p.get('work_accounting_unknown') for p in obligations['rule_stage_progress'].values())),
                'scope':'known attempted work separated from accepted conclusions; no extra findings'}
            report['rule_stage_progress_scope']='source_obligation_channel_only; legacy queries remain in results and formal_checks_called'
            checked=obligations['source_obligation_checks']
            actual=[q for q in obligations['source_obligations'] if q['rule'] in NEW_RULES]
            errors=[q for q in obligations['source_obligation_errors'] if q.get('rule') in NEW_RULES]
            requested=sorted({q['rule'] for q in actual+errors})
            called={q['obligation_id'] for q in checked if q['formal']['solver_called']}
            from .m05_question_trace import evidence_state
            conclusive={q['obligation_id'] for q in checked if evidence_state(q)['model_conclusive']}
            completed=[rule for rule in requested if not any(q['rule']==rule for q in errors)
                and all(q['id'] in conclusive and q.get('question_trace',{}).get('original_question_completion')=='complete'
                    and not q.get('model_gaps') and not any(
                    r['assessment']=='not_automatically_discharged' for r in q.get('remark_assessments',[]))
                    for q in actual if q['rule']==rule)]
            report['framework_has_checked_queries']=bool(real and (formal_count or obligations['formal_checks_called']))
            report['full_framework_executed']=bool(real and (formal_count or obligations['formal_checks_called']))
            report['full_framework_criterion']='M1 source context, authenticated real M2 response, M3 bound query/model and at least one M4 formal attempt; execution is not conclusive coverage'
            report['all_requested_source_questions_complete']=bool(requested and completed==requested)
            report['question_completion_criterion']='explicit original-question completion certificate; local attempted or conclusive models do not establish whole-question completion'
            report['requested_direction_scope']=requested
            report['requested_directions_completed']=completed
            report['directions_with_checked_questions']=sorted({q['rule'] for q in checked if q['formal']['solver_called']})
            report['directions_with_attempted_questions']=report['directions_with_checked_questions']
            report['directions_with_conclusive_local_models']=sorted({q['rule'] for q in checked if evidence_state(q)['model_conclusive']})
            report['question_trace']=[{'obligation_id':q['id'],**q.get('question_trace',{})} for q in obligations['source_obligations']]
            report['formal_count_scope']='query records with solver work; not raw solver.check calls, successful samples, distinct vulnerabilities or complete risk directions'
            report['new_direction_model_status']='bounded source rejection, credential self-composition, transfer/control transitions and net holder interference'
            report['status']='joint_partial' if full or real and obligations['formal_checks_called'] else 'joint_incomplete' if real else 'diagnostic_only'
            report['failures']+=obligations['source_obligation_errors']
            report['uncovered']+=[{'obligation_id':q['id'],'rule':q['rule'],'target':q['target'],
                'function':q['function'],**gap} for q in obligations['source_obligations'] for gap in q.get('model_gaps',[])]
            for q in actual:
                if any(r['assessment']=='not_automatically_discharged' for r in q.get('remark_assessments',[])):
                    report['uncovered'].append({'scope':'source_obligations_v1','obligation_id':q['id'],
                        'rule':q['rule'],'reason':'original_decisive_concerns_retained_with_model_scope'})
            if not requested:
                report['uncovered'].append({'scope':'source_obligations_v1','reason':'no_new_direction_question_proposed'})
        if common_model is not None:
            attach_common(report,common_model);save(out/'common_operation_model.json',common_model)
            from .m05_candidate_coverage import semantic_review_inventory,semantic_review_messages
            semantic_review=semantic_review_inventory(context,candidate_coverage,obligations,state,ordinary_rows=rows)
            report['semantic_relation_review']=semantic_review
            save(out/'semantic_relation_review.json',semantic_review)
            # The inventory is retained for review. Do not construct a second
            # full request that will never be sent by this invocation.
        if intake is not None:
            report['dataset_intake']=intake['receipt']
            report['target_inventory']=state['analysis']['target_inventory']
            report['target_preparation_failures']=state['analysis']['failures']
            report['failures']+=state['analysis']['failures']
            if state['analysis']['failures']:
                report['full_framework_executed']=False
                if report['status']=='joint_completed':report['status']='joint_partial'
        report['analysis_scope']=context['analysis_scope']
        report['requested_rules']=list(context['requested_rules'])
        report['implementation_revision']='joint-operation-scoped-r1-rq1-v7-20261028'
        report['proposal_routing']=conversion.get('routing',{'records':[],'errors':[]})
        from .m05_question_trace import evidence_state
        report['query_execution_trace']=[{'query_id':r['id'],'rule':r['rule'],'target':r['target'],
            'function':r['function'],'channel':channel,'proposal_id':r.get('proposal_id'),
            'proposal_sha256':r.get('llm_proposal_sha256'),'obligation_id':r.get('obligation_id'),
            'binding_ref':r.get('binding_ref'),'formula_sha256':r.get('formal',{}).get('formula_sha256'),
            'query_requirements':r.get('query_requirements'),**evidence_state(r),
            'reportable_conditional_result':bool(r.get('reportable'))}
            for channel,items in [('bound_query',rows),('source_obligation',obligations['source_obligation_checks'] if extended else [])]
            for r in items]
        if extended:
            report['source_to_ordinary_query_bridge']=source_bridge.report(rows)
            save(out/'source_query_bridge.json',report['source_to_ordinary_query_bridge'])
        report['query_trace_scope']='all actually constructed rule queries; missing proposals, unsupported directions and unclassified questions remain separate gaps'
        from .m05_completion_scope import summarize as completion_scope
        report['classification_completion']=completion_scope(context,state,report)
        report['task_classification']=report['classification_completion']['task_classification']
        report['classification_stops']=state.get('classification_stops',[])
        report['auxiliary_findings']=[{'query_id':r['id'],'target':r['target'],'function':r['function'],**r['auxiliary_finding']} for r in report.get('source_obligation_checks',[]) if r.get('auxiliary_finding')]
        if real and (report['task_classification']['classification_available'] or any(r.get('program_analysis_certificate',{}).get('verified') for r in report.get('source_obligation_checks',[]))):
            report['framework_has_checked_queries']=True
            report['full_framework_executed']=not bool(state['analysis']['failures'])
            report['full_framework_criterion']='actual requested P/M checks or completed source-bound detector scan; not solver quota'
            report['status']='joint_completed' if report['task_classification']['all_requested_labels_classified'] and not state['analysis']['failures'] else 'joint_partial'
        save(out/'classification_completion.json',report['classification_completion'])
        save(out/'joint_report.json',report);stage('M4',report['status'],queries=len(rows),formal_checks_called=formal_count)
        save(out/'entry_result.json',{k:report[k] for k in ('status','full_framework_executed','real_llm','bound_query_count','formal_checks_called','reportable_findings')});return 0
    except Exception as ex:
        stage(active,'failed',reason=type(ex).__name__+':'+str(ex));save(out/'entry_result.json',{'status':'failed','module':active,'reason':str(ex),'real_llm':bool(receipt and receipt.get('source_nature')=='real')});return 1
