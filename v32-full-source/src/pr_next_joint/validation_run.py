"""Shared original-program check/replay/report transport, for targets or controls."""
import copy,hashlib,json,pathlib,time,uuid
from .core import *
from .backend import execute_plan
from .completion import instantiate_queries
from .artifacts import Artifacts,compile_query,result_transport
from .result_semantics import classify_outcome, component_status, aggregate_r4_status
from .declaration_checks import evaluate as evaluate_declarations

def build_component_result(query,item,bundle,execution=None,replay=None,solved=None,execution_error=None,replay_error=None,tool_error=None,timeout=False,declaration_error=None):
 """Pure result construction for success, refusal, unknown and failure states."""
 solved=solved or {'premise':'not_called','query':'not_called'}
 replay_equal=bool(replay and replay.get('equal'))
 if item.get('unresolved_critical', bool(item.get('unresolved'))):
  verdict='inconclusive';outcome='critical_unresolved'
 elif declaration_error:
  verdict='inconclusive';outcome='declaration_failed'
 elif timeout:
  verdict='inconclusive';outcome='timeout'
 elif tool_error is not None:
  verdict='inconclusive';outcome='tool_error'
 elif execution_error is not None:
  verdict='inconclusive';outcome='concrete_execution_failed'
 elif replay_error is not None:
  verdict='inconclusive';outcome='replay_failed'
 elif replay is not None and not replay_equal:
  verdict='inconclusive';outcome='replay_failed'
 elif replay is None:
  verdict='inconclusive';outcome='unknown'
 else:
  verdict=interpret_result(query['query_form'],solved.get('premise'),solved.get('query','unknown'),'completed','complete_for_declared_query','exact_for_query',replay_equal)
  outcome=classify_outcome(premise=solved.get('premise'),solver=solved.get('query'),execution='completed',replay=replay_equal,unresolved=(item.get('unresolved') if item.get('unresolved_critical', bool(item.get('unresolved'))) else None),verdict=verdict,source='concrete')
 execution_status='tool_error' if execution_error is not None else ('completed' if execution is not None else 'not_executed')
 search_scope=item.get('path_search_scope') or {}
 replay_status='passed' if replay_equal else ('failed' if (replay is not None or replay_error is not None) else 'not_called')
 coverage='complete_for_declared_query' if execution_status=='completed' and replay_status=='passed' and not search_scope.get('incomplete') and outcome not in ['critical_unresolved','timeout','tool_error','concrete_execution_failed','replay_failed','unknown','no_model','model_unsat','truncated','unsupported','infeasible_premise'] else 'partial'
 model_fidelity='exact_for_query' if coverage=='complete_for_declared_query' else 'unverified'
 premise_status={'sat':'satisfiable','unsat':'unsatisfiable'}.get(solved.get('premise'),'unknown')
 transactions=(execution or {}).get('transactions',[])
 row={'id':query['id'],'input_id':item['input_id'],'track':'approved_mechanism_component','rule':query['rule_id'],'query_form':query['query_form'],'verdict':verdict,'solver':solved,'outcome_kind':outcome,'execution_status':execution_status,'coverage':coverage,'whole_program_coverage':'partial','model_fidelity':model_fidelity,'premise_status':premise_status,'policy_scope':item.get('policy_scope','explicit_or_approved'),'unresolved':item.get('unresolved',[]),'same_engine_replay_equal':replay_equal,'replay_status':replay_status,'applicability_status':item['query']['applicability'],'rule_checks':item['query']['required_rule_checks'],'plan_ref':ref(item['plan']),'program_id':bundle['program_id'],'build_id':bundle['build_id'],'alias_case_id':item['alias_case']['id'],'scenario':item['scenario'],'purpose':item.get('purpose','risk_candidate'),'declaration_error':declaration_error,'path_search_incomplete':bool(search_scope.get('incomplete')),'path_search_truncated':bool(search_scope.get('truncated')),'path_search_timeout':bool(search_scope.get('timeout')),'path_search_unvisited_nodes':search_scope.get('unvisited_nodes',0),'path_search_leaf_errors':search_scope.get('leaf_errors',[]),'status_per_step':[t.get('status') for t in transactions],'path_search_evidence_ref':item.get('path_search_evidence_ref'),'joint_method_acceptance':False,'no_safety_conclusion':outcome not in ['supported'],'source_remarks':item.get('source_remarks',[]),'proposal_subject':item['query'].get('proposal_subject'),'proposal_effect_state':item['query'].get('proposal_effect_state'),'proposal_guard':item['query'].get('proposal_guard')}
 if execution_error is not None:row['execution_error']={'error_class':type(execution_error).__name__,'error':str(execution_error)}
 if replay_error is not None:row['replay_error']={'error_class':type(replay_error).__name__,'error':str(replay_error)}
 if tool_error is not None and not isinstance(tool_error,Exception):row['tool_error']=str(tool_error)
 return row

def validate_component(client,item,bundle,directory,fingerprint,deadline=None):
 """Actual v3 original execution, replay and formal result; no fabricated rows."""
 from .multi_service import execute_multi
 from .artifacts import compile_component_query
 directory=pathlib.Path(directory);directory.mkdir(parents=True,exist_ok=False);store=Artifacts(directory/'artifacts')
 remaining=lambda:min(120,max(0,(deadline or time.monotonic()+180)-time.monotonic()))
 query,plan,plan_ref,backend_ref=compile_component_query(store,item,bundle,fingerprint)
 # The binder decides query relevance; this layer consumes its classification.
 # Critical or legacy-unclassified gaps must stop before any backend request.
 if item.get('unresolved_critical', bool(item.get('unresolved'))):
  row=build_component_result(query,item,bundle)
  (directory/'critical_unresolved.json').write_text(json.dumps(item.get('unresolved',[]),indent=2))
  evidence=store.put({'id':item['id']+':unresolved-evidence','unresolved':item.get('unresolved',[]),'outcome_kind':'critical_unresolved'})
  transport,_=result_transport(store,query,plan,plan_ref,backend_ref,row,evidence)
  transport['limitations'].append('query-critical unresolved items; no backend execution or query requested')
  row['verification_result_ref']=store.put(transport)
  (directory/'VerificationResult.json').write_text(json.dumps(transport,indent=2));(directory/'summary.json').write_text(json.dumps(row,indent=2));return row
 declaration_failures=evaluate_declarations(item)
 if declaration_failures:
  row=build_component_result(query,item,bundle,declaration_error=declaration_failures)
  (directory/'declaration_error.json').write_text(json.dumps(declaration_failures,indent=2))
  evidence=store.put({'id':item['id']+':declaration-evidence','declaration_failures':declaration_failures,'outcome_kind':'declaration_failed'})
  transport,_=result_transport(store,query,plan,plan_ref,backend_ref,row,evidence)
  transport['limitations'].append('proposal declaration check failed; external execution was not accepted as evidence')
  row['verification_result_ref']=store.put(transport)
  (directory/'VerificationResult.json').write_text(json.dumps(transport,indent=2));(directory/'summary.json').write_text(json.dumps(row,indent=2));return row
 (directory/'pre_execution.json').write_text(json.dumps({'item_ref':ref(item),'query_ref':ref(query),'plan_ref':plan_ref,'service_plan_ref':ref(item['plan'])},indent=2))
 execution=None;replay=None;solved=None;row=None
 try:
  client.select(ref(item['plan']));execution=execute_multi(client,item['plan'])
  (directory/'execution.json').write_text(json.dumps(execution,indent=2))
 except Exception as error:
  row=build_component_result(query,item,bundle,execution=None,replay=None,solved=None,execution_error=error,timeout=isinstance(error,TimeoutError))
  (directory/'execution_error.json').write_text(json.dumps({'error_class':type(error).__name__,'error':str(error)},indent=2))
 else:
  try:
   replay=client.request({'op':'materialize_witness','execution_id':execution['execution_id']},timeout=remaining())
   (directory/'replay.json').write_text(json.dumps(replay,indent=2))
  except Exception as error:
   row=build_component_result(query,item,bundle,execution=execution,replay=None,solved=None,replay_error=error)
   (directory/'replay_error.json').write_text(json.dumps({'error_class':type(error).__name__,'error':str(error)},indent=2))
  else:
   if not replay.get('equal'):
    row=build_component_result(query,item,bundle,execution=execution,replay=replay,solved={'premise':'unknown','query':'not_called'})
   elif item.get('unresolved_critical', bool(item.get('unresolved'))):
    row=build_component_result(query,item,bundle,execution=execution,replay=replay,solved={'premise':'not_called','query':'not_called'})
   elif remaining()<=1:
    row=build_component_result(query,item,bundle,execution=execution,replay=replay,solved={'premise':'unknown','query':'not_called'},timeout=True)
   else:
    try:solved=client.request({'op':'check_formula','execution_id':execution['execution_id'],'query_id':item['query']['rule']},timeout=min(30,remaining()))
    except Exception as error:
     row=build_component_result(query,item,bundle,execution=execution,replay=replay,solved={'premise':'unknown','query':'not_called'},tool_error=error,timeout=isinstance(error,TimeoutError))
     (directory/'query_error.json').write_text(json.dumps({'error_class':type(error).__name__,'error':str(error)},indent=2))
    else:row=build_component_result(query,item,bundle,execution=execution,replay=replay,solved=solved)
 evidence=store.put({'id':item['id']+':evidence','execution':execution,'replay':replay,'condition':solved,'outcome_kind':row['outcome_kind']})
 transport,_=result_transport(store,query,plan,plan_ref,backend_ref,row,evidence)
 if row['coverage']!='complete_for_declared_query':
  transport.update(coverage='partial',model_fidelity='unverified')
  if row.get('execution_error'):transport['limitations'].append('concrete execution failed: '+row['execution_error']['error'])
  if row.get('replay_error'):transport['limitations'].append('replay failed: '+row['replay_error']['error'])
  if row.get('path_search_incomplete'):transport['limitations'].append('symbolic search incomplete: timeout/truncated/unvisited nodes/leaf errors; no complete coverage or model-equivalence claim')
  if row.get('path_search_leaf_errors'):transport['limitations'].append('symbolic leaf errors retained: '+json.dumps(row['path_search_leaf_errors']))
  if row['outcome_kind']!='supported':transport['limitations'].append('outcome_kind='+row['outcome_kind']+'; no safety conclusion')
 row['verification_result_ref']=store.put(transport)
 (directory/'VerificationResult.json').write_text(json.dumps(transport,indent=2));(directory/'summary.json').write_text(json.dumps(row,indent=2));return row

def report_component_results(rows,leads,fingerprint,directory,r4_evidence=None,deferred=None):
 """Existing four report areas for component evidence; R4.1 aggregate is separate."""
 seen={}
 for row in rows:
  key=(row['id'],row['program_id'],row['build_id']);require(key not in seen or seen[key]==row,'current_result_identity_conflict');seen[key]=row
 rows=list(seen.values());findings=[r for r in rows if r['verdict']=='supported' and r['solver'].get('query')=='sat' and r['same_engine_replay_equal'] and r.get('purpose')!='no_effect_control'];controls=[r for r in rows if r.get('purpose')=='no_effect_control']
 cs=component_status(rows,leads,[])
 named_gaps=[]
 for row in rows:
  kind=row.get('outcome_kind') or 'unknown'
  if kind not in ['supported','refuted_in_scope']:named_gaps.append(row['input_id']+':'+row['rule']+':'+kind)
 for lead in leads:named_gaps.append('lead:'+str(lead.get('reason')))
 r4=(aggregate_r4_status(r4_evidence,deferred) if r4_evidence is not None else {'status':'not_evaluated','basis':'C2_R4_1','scientific_acceptance_claimed':False})
 report={'status':cs['status'],'component_only':True,'evidence_scope':'approved mechanism component execution; no real project or full joint method claim','backend_fingerprint':fingerprint,'reportable_findings':findings,'leads':leads+[r for r in rows if r['verdict'] in ['inconclusive','infeasible_premise']],'refuted_candidates':[r for r in rows if r['verdict']=='refuted_in_scope' and r.get('purpose')!='no_effect_control'],'control_results':controls,'coverage_and_failures':{'coverage':'partial','query_results':rows,'outcome_counts':cs['outcome_counts'],'named_gaps':named_gaps},'r4_1_aggregate':r4,'deferred_by_r4_scope':list(deferred or ['D-REAL02','D-REAL03','D-REPAIR','D-REAL-SYMBOLIC']),'prediction_ledger':[{'input_id':r['input_id'],'program_id':r['program_id'],'build_id':r['build_id'],'query_id':r['id'],'rule':r['rule'],'prediction':prediction(r in findings,r.get('outcome_kind') in ['critical_unresolved','unknown','no_model','timeout','tool_error','concrete_execution_failed','replay_failed']),'purpose':r.get('purpose','risk_candidate'),'scope':'this component query only; not dataset scoring'} for r in rows],'scientific_acceptance_claimed':False,'joint_method_acceptance':False}
 directory=pathlib.Path(directory);directory.mkdir(parents=True,exist_ok=True)
 (directory/'analysis_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 return report

def report_saved_results(context,static_materials,historical_reports,gaps,directory,previous=None):
 """Report-only public entry; intentionally independent of validate()."""
 from .artifacts import analysis_report,render_analysis_report
 root=pathlib.Path(context['workspace_root']).resolve()
 def verify(source,value):
  path=pathlib.Path(source['path']).resolve()
  require(path.is_relative_to(root) and path.suffix=='.json','report_source_outside_workspace_or_not_json')
  data=path.read_bytes()
  require(hashlib.sha256(data).hexdigest()==source['sha256'],'report_source_file_identity')
  require(digest(json.loads(data))==digest(value),'report_source_content_identity')
 for material in static_materials:verify(material['source'],material['result'])
 for history in historical_reports:
  verify(history['source'],history['report'])
  require(len(history['result_sources'])==len(history['verification_results']),'historical_result_source_count')
  for source,value in zip(history['result_sources'],history['verification_results']):verify(source,value)
 report=analysis_report(context,static_materials,historical_reports,gaps,previous)
 directory=pathlib.Path(directory).resolve();require(directory.is_relative_to(root),'report_output_outside_workspace');directory.mkdir(parents=True,exist_ok=True)
 outputs={'analysis_report.json':json.dumps(report,ensure_ascii=False,indent=2)+'\n','analysis_report_CN.md':render_analysis_report(report)}
 # Verify every existing byte before writes. Resume cannot overwrite another
 # version or append duplicate candidates to a prior delivery.
 for name,text in outputs.items():
  path=directory/name
  if path.exists():require(path.read_bytes()==text.encode('utf-8'),'report_output_identity_conflict:'+name)
 for name,text in outputs.items():
  path=directory/name
  if not path.exists():path.write_bytes(text.encode('utf-8'))
 return report,{'entrypoint':'pr_next_joint.validation_run.report_saved_results','report_ref':ref(report),'outputs':[{'path':str((directory/n).resolve()),'sha256':hashlib.sha256(v.encode('utf-8')).hexdigest()} for n,v in outputs.items()],'new_verification_executed':False}

def validate(client,candidate,bundle,contract,directory,fingerprint,capabilities):
 start=time.monotonic();directory=pathlib.Path(directory);directory.mkdir(parents=True,exist_ok=False)
 queries=instantiate_queries(candidate);store=Artifacts(directory/'artifacts');compiled={}
 for q in queries:
  c={**candidate,'query_frame':q}
  compiled[q['rule']]=compile_query(store,c,bundle,contract,q['rule'],q['query_form'],q['premise'],q['expression'],fingerprint,capabilities)
 (directory/'pre_execution.json').write_text(json.dumps({'candidate_ref':ref(candidate),'plan_ref':ref(candidate['plan']),'source_certificate_ref':ref(candidate['source_certificate']),'queries':{name:{'query_ref':ref(x[0]),'verification_plan_ref':x[2]} for name,x in compiled.items()}},indent=2))
 client.select(ref(candidate['plan']));hello=client.request({'op':'hello'})
 result=execute_plan(client,bundle,contract,candidate['plan'],directory/'execution')
 witness=client.request({'op':'materialize_witness','execution_id':result['execution_id']},timeout=min(120,180-(time.monotonic()-start)))
 require(witness['equal'],'full_replay_mismatch')
 evidence_ref=store.put({'id':candidate['id']+':execution','execution':result,'replay':witness['replay']})
 rows=[]
 for q in queries:
  solved=client.request({'op':'check_formula','query_id':q['rule'],'execution_id':result['execution_id']})
  verdict=interpret_result(q['query_form'],solved['premise'],solved.get('query','unknown'),'completed','complete_for_declared_query','exact_for_query',witness['equal'])
  row={'id':candidate['id']+':'+q['rule'],'input_id':candidate['input_id'],'track':candidate['track'],'rule':q['rule'],'query_form':q['query_form'],'verdict':verdict,'solver':solved,'execution_status':'completed','coverage':'complete_for_declared_query','whole_program_coverage':'partial','policy_scope':'inferred_policy' if q['rule'].startswith('AC') else 'not_a_policy_query','unresolved':candidate['automatic_scope_gaps'],'same_engine_replay_equal':witness['equal'],'applicability_status':'applicable','rule_checks':q['required_rule_checks'],'source_certificate_ref':ref(candidate['source_certificate']),'plan_ref':ref(candidate['plan'])}
  query,plan,plan_ref,backend_ref=compiled[q['rule']]
  transport,tr=result_transport(store,query,plan,plan_ref,backend_ref,row,evidence_ref);row['verification_result_ref']=tr
  rows.append(row)
 summary={'candidate_id':candidate['id'],'input_id':candidate['input_id'],'track':candidate['track'],'plan_ref':ref(candidate['plan']),'status_per_step':[r['status'] for r in result['transactions']],'registry':result['registry'],'queries':rows,'same_engine_replay_equal':True,'method_list':hello['methods'],'elapsed_seconds':time.monotonic()-start}
 (directory/'summary.json').write_text(json.dumps(summary,indent=2));return summary,result
