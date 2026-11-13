"""R2 C1 versioned, content-addressed query/plan/result transport artifacts."""
import copy,hashlib,json,pathlib
from .core import *
from . import SCHEMA_VERSION

class Artifacts:
 def __init__(self,path):self.path=pathlib.Path(path);self.path.mkdir(parents=True,exist_ok=True)
 def put(self,value):
  r=ref(value);p=self.path/(r['sha256']+'.json')
  if p.exists():require(canonical(json.loads(p.read_text()))==canonical(value),'artifact_collision')
  else:p.write_text(json.dumps(value,indent=2))
  return r

def compile_query(store,candidate,bundle,contract,name,form,premise,expr,fingerprint,capabilities):
 plan=candidate['plan'];p=candidate['proposal'];group=candidate['group']
 bundle_ref=store.put(bundle);proposal_ref=store.put(p)
 actor_ref=store.put({'id':group+':actors','actors':plan['actors'],'address_aliasing':'equal address is one world account; distinct values are this finite case, not global inequality'})
 environment=store.put({'id':group+':environment','timestamp':'1000000','block_number':'1','chain_id':'1','gas_price_wei':'1','base_fee_wei':'0','coinbase':'0x00000000000000000000000000000000000000d4','funding':'declared EOAs receive 100 ETH in development environment; no contract storage injection'})
 deployment=store.put({'id':group+':deployment','mode':'DEPLOYMENT','program_ref':bundle_ref,'creation_code_sha256':hashlib.sha256(bytes.fromhex(contract['creation'])).hexdigest(),'abi':contract['abi'],'library_links':[],'constructor':plan['transactions'][0],'initializer_prefix':[t for t in plan['transactions'][1:2] if any('string' in f['types'] for f in contract['functions'] if f['signature']==t['function'])],'all_prefixes_counted':True})
 domain=store.put({'id':group+':finite_domain','plan':plan,'all_sequences':False,'symbolic_parameters':False})
 scope={'kind':'one_plan','max_top_level_transactions':len(plan['transactions']),'max_plans':1,'address_domain':'finite_declared','domain_ref':domain,'uncovered_items':candidate['automatic_scope_gaps']+['all other parameter choices and transaction sequences']}
 profile=store.put({'id':'c1-evidence-profile-v1','source':'approved C1 order','minimum':'all query-critical checks plus original execution and same-engine replay for existential financial effect; no independent-EVM claim'})
 evid={'artifact':bundle_ref,'locator':'contracts/'+contract['file']+':'+contract['name'],'origin':'compiler'}
 policy={'kind':'program_inferred' if name.startswith('AC') else 'approved_rule','rule_basis_id':name,'allowed':obs('qualified.'+str(max(1,candidate['effect_step']-1)),'Bool'),'support_refs':[evid],'alternatives':[],'open_alternatives':[],'scope_ref':domain}
 if candidate.get('source_certificate'):
  cert_ref=store.put({'id':group+':source_certificate','certificate':candidate['source_certificate']})
  frame=candidate['query_frame']
  policy.update(allowed=frame['allowed'],support_refs=[{'artifact':cert_ref,'locator':'certificate/policy/independent_bootstrap_writes + independent_lifecycle_sources' if name.startswith('AC') else 'certificate/financial/issuance_writes + spendability_and_transfer_sources' if name=='FCR-MINT' else 'certificate/lifecycle_traces + qualification_paths + protected_effect_paths','origin':'compiler'}])
 rules=store.put({'id':name,'revision':1,'origin':'R2 risk registry' if name!='relation' else 'R2 CHECK_IMPLICATION','no_new_gold_labels':True})
 resources=[]
 if name=='FCR-MINT':resources=[store.put({'id':group+':financial_resource','kind':'original_token_development_instance','getters':[o for o in plan['observers'] if o['id'] in ['balance','supply']],'source_state_declarations':candidate['source_relation']['financial_observer_state_ids'],'claim':'bounded new rights creation with supply increase; not unlimited; no mainnet proxy claim','program_ref':bundle_ref})]
 query={'schema_version':SCHEMA_VERSION,'id':group+':'+name,'revision':p['revision'],'program_id':p['program_id'],'build_id':p['build_id'],'proposal_ref':proposal_ref,'rule_id':name,'rule_revision':1,'query_form':form,'policy_basis':policy,'actor_control_ref':actor_ref,'initial_state_ref':deployment,'resource_refs':resources,'plan_set_ref':domain,'observed_claim':expr,'assumptions':[],'required_checks':['identity','source-bound observers','actor control','nonvacuity','original execution','replay','rule applicability'],'scope':scope,'acceptance_profile_ref':profile}
 if candidate.get('query_frame'):query['required_checks']+=candidate['query_frame']['required_rule_checks']
 query_ref=store.put(query)
 fingerprint={**fingerprint,'actors':plan['actors'],'compiler_evm_target':contract['metadata']['settings']['evmVersion'],'declared_domain_ref':domain}
 backend_ref=store.put(fingerprint);cap_ref=store.put(capabilities)
 runtime_ref=store.put({'id':group+':runtime','runtime_sha256':hashlib.sha256(bytes.fromhex(contract['runtime'])).hexdigest(),'build_id':p['build_id'],'bundle_ref':bundle_ref})
 observers=[]
 for step in range(1,len(plan['transactions'])+1):
  binding=store.put({'id':group+':execution:'+str(step),'kind':'execution_outcome','step':step,'original_engine_exit':True})
  observers.append({'id':'tx'+str(step)+'.success','kind':'execution_outcome','type':'Bool','binding_ref':binding,'world_point':'post:'+str(step),'code_instance':group,'storage_instance':group,'subject_keys':[]})
  for o in plan['observers']:
   binding=store.put({'id':group+':'+o['id']+':'+str(step),'kind':'getter_read','original_abi':next(f for f in contract['functions'] if f['signature']==o['function']),'spec':o,'runtime_ref':runtime_ref,'snapshot_point':'post:'+str(step),'caller':'A','value':'0','frozen_copy':True,'initTx':False,'output_index':o.get('output_index',0),'environment_ref':environment})
   types=next(f['types'] for f in contract['functions'] if f['signature']==o['function'])
   keys=[lit('Address160',plan['actors'][v[1:]]['address'] if v.startswith('$') else v) if typ=='address' else lit('BV'+(typ[4:] or '256'),v) for typ,v in zip(types,o['arguments']) if typ=='address' or typ.startswith('uint')]
   observers.append({'id':o['id']+'.'+str(step),'kind':'getter_read','type':o['type'],'binding_ref':binding,'world_point':'post:'+str(step),'code_instance':group,'storage_instance':group,'subject_keys':keys})
 txs=[]
 for i,t in enumerate(plan['transactions'],1):
  fs=contract['constructor_types'] if t['function']=='constructor' else next(f['types'] for f in contract['functions'] if f['signature']==t['function'])
  args=[]
  # Dynamic initializer arguments live exclusively in the versioned deployment
  # record; the Tx points to it rather than smuggling calldata through Expr.
  dynamic=any(ty=='string' for ty in fs)
  if not dynamic:
   for ty,v in zip(fs,t['arguments']):
    if ty=='address':args.append(lit('Address160',plan['actors'][v[1:]]['address'] if v.startswith('$') else v))
    elif ty=='bool':args.append(lit('Bool',v in ['1','true']))
    elif ty.startswith('uint'):args.append(lit('BV'+(ty[4:] or '256'),v))
    elif ty.startswith('bytes'):args.append(lit('Bytes'+ty[5:],v))
  txs.append({'index':i,'target_ref':group,'origin_symbol':t['sender'],'call_kind':'top_level_eoa','function_ref':('deployment_record:'+deployment['id']+':initializer' if dynamic else t['function']),'arguments':args,'value_wei':lit('BV256',0),'environment_ref':environment,'on_failure':'record_and_continue','must_succeed_for_claim':False})
 limits={'max_top_level_transactions':6,'max_plans_per_target':32,'max_proposal_revisions':2,'solver_timeout_seconds':30,'candidate_timeout_seconds':180,'max_loop_iterations':12000000,'max_call_depth':1024,'max_dynamic_bytes':64,'project_time_seconds':1800,'project_candidate_limit':32,'llm_token_limit':240000,'llm_cost_limit':'10'}
 vp={'schema_version':SCHEMA_VERSION,'id':query['id']+':plan','revision':p['revision'],'program_id':p['program_id'],'build_id':p['build_id'],'query_ref':query_ref,'query_form':form,'runtime_refs':[runtime_ref],'backend_fingerprint':backend_ref,'capability_receipt':cap_ref,'initial_mode':'DEPLOYMENT','initial_state_ref':deployment,'actors':p['actors'],'transactions':txs,'observers':observers,'preconditions':[],'checked_expression':expr,'nonvacuity_expression':premise,'scope':scope,'limits':limits,'expected_sat_meaning':'refutes_claim' if form=='CHECK_IMPLICATION' else 'supports_claim','expected_unsat_meaning':'supports_claim_in_scope' if form=='CHECK_IMPLICATION' else 'refutes_claim_in_scope','fixed_intervention_ref':None,'code_modification_allowed':False,'policy_changes_allowed':False,'unresolved_critical_items':[]}
 return query,vp,store.put(vp),backend_ref

def result_transport(store,query,plan,plan_ref,backend_ref,row,evidence_ref):
 execution_status=row.get('execution_status','completed');execution_status='tool_error' if execution_status in ['failed','error'] else execution_status;replay_status=row.get('replay_status','passed' if row.get('same_engine_replay_equal') else 'not_called');replay_status='not_requested' if replay_status=='not_called' else replay_status;witness_status='replayed' if replay_status=='passed' else ('not_needed' if execution_status!='completed' or replay_status in ['not_called','not_requested'] else 'invalid')
 r={'schema_version':SCHEMA_VERSION,'id':query['id']+':result','revision':query['revision'],'program_id':query['program_id'],'build_id':query['build_id'],'query_ref':ref(query),'plan_ref':plan_ref,'query_form':query['query_form'],'verdict':row['verdict'],'solver_status':row['solver'].get('query','unknown'),'execution_status':execution_status,'coverage':row.get('coverage','complete_for_declared_query'),'scope':plan['scope'],'model_fidelity':row.get('model_fidelity','exact_for_query'),'premise_status':row.get('premise_status',{'sat':'satisfiable','unsat':'unsatisfiable'}.get(row['solver'].get('premise'),'unknown')),'witness_status':witness_status,'replay_status':replay_status,'evidence_refs':[{'artifact':evidence_ref,'locator':'transactions/observations','origin':'verification'}],'policy_scope':row['policy_scope'],'unexplored_items':row['unresolved'],'limitations':['ground Z3 query over one concretely executed trace; no symbolic EVM search','same-engine replay; not an independent EVM','compiler target and actual pinned hevm semantics are separately bound'],'backend_fingerprint':backend_ref}
 if row.get('applicability_status')=='not_applicable':
  r.update(verdict='invalid_request',coverage='partial',model_fidelity='unverified',witness_status='not_needed')
  r['limitations'].append('Applicability rejected after the ground query ran; retain actual solver/execution/replay statuses, do not claim not_called.')
 return r,store.put(r)

def compile_component_query(store,item,bundle,fingerprint):
 """The v3 plan branch of the existing query/plan/result artifact transport."""
 inferred=bool(item.get('policy',{}).get('inferred')) or item.get('policy_scope')=='inferred_policy'
 concrete=item['plan'];q=item['query'];scope={'kind':'one_plan','max_top_level_transactions':len(concrete['transactions']),'max_plans':1,'address_domain':'finite_declared','domain_ref':store.put(concrete),'uncovered_items':['all other parameter choices and transaction sequences','joint LLM proposal acceptance','independent EVM']}
 proposal_support=[]
 if item.get('proposal_application'):
  pa=item['proposal_application'];claim_ref=store.put({'id':item['id']+':proposal-claim-bindings','claim_bindings':pa.get('claim_bindings',[]),'replay_scope':'one concrete proposal application; no R4-A6 credit'});proposal_support=[{'artifact':claim_ref,'locator':'proposal claim bindings; engineering-only, not execution evidence','origin':'diagnostic'}];proposal=store.put({'id':item['id']+':consumed-proposal','kind':'consumed_joint_proposal','proposal_ref':pa.get('proposal_ref'),'consumption_ref':pa.get('consumption_ref'),'proposal':pa.get('proposal'),'claim_bindings':pa.get('claim_bindings',[]),'source_kind':pa.get('source_kind'),'substitute':pa.get('substitute',True),'LLM_called':bool(pa.get('llm_called')),'r4_a6_credit':False,'joint_method_acceptance':False,'not_full_joint_method':True})
 else:
  proposal=store.put({'id':item['id']+':component-proposal','kind':'source_derived_component_proposal','candidate_ref':item['candidate_ref'],'static_ref':item['static_ref'],'source_relation':item['source_relation'],'LLM_called':False,'not_full_joint_method':True})
 source=store.put({'id':item['id']+':policy','policy':item['policy'],'source_relation':item['source_relation']})
 deployment=store.put({'id':item['id']+':deployment','mode':'DEPLOYMENT','program_ref':store.put(bundle),'prefix':concrete['transactions'][:-1],'programs':concrete['programs'],'instances':concrete['instances'],'no_storage_injection':True})
 actors=store.put({'id':item['id']+':actors','partition':item['alias_case'],'actual_accounts':concrete['accounts']})
 profile=store.put({'id':'c2-component-evidence-profile','minimum':'scoped policy, source identity, reachable original prefix, original effects, concrete same-engine replay','scope':'approved mechanism component engineering; not full joint method'})
 query={'schema_version':SCHEMA_VERSION,'id':item['id']+':'+q['rule'],'revision':1,'program_id':bundle['program_id'],'build_id':bundle['build_id'],'proposal_ref':proposal,'rule_id':q['rule'],'rule_revision':1,'query_form':q['query_form'],'policy_basis':{'kind':'program_inferred' if inferred else 'explicit_project_spec','rule_basis_id':q['rule'],'allowed':q['policy_allowed'],'support_refs':[{'artifact':source,'locator':'policy/source + source_relation/association','origin':'diagnostic' if inferred else 'project_spec'}]+proposal_support,'alternatives':[],'open_alternatives':item['unresolved'],'scope_ref':scope['domain_ref']},'actor_control_ref':actors,'initial_state_ref':deployment,'resource_refs':[source],'plan_set_ref':scope['domain_ref'],'observed_claim':q['expression'],'assumptions':[],'required_checks':q['required_rule_checks']+(['proposal_claim_binding'] if item.get('proposal_application') else []),'scope':scope,'acceptance_profile_ref':profile}
 backend=store.put({**fingerprint,'id':item['id']+':actual-backend','actual_accounts':concrete['accounts'],'actual_instances':concrete['instances'],'environments':[t['environment'] for t in concrete['transactions']],'gas_limit':12000000,'source_program_id':bundle['program_id'],'build_id':bundle['build_id'],'declared_domain_ref':scope['domain_ref'],'path_search_evidence_ref':item.get('path_search_evidence_ref'),'concrete_condition_scope':'one original trace only'})
 typed_actors=[];symbols={}
 for account in item['alias_case']['accounts']:
  symbol='='.join(account['members']);address=account['identity']['address'];symbols[address]=symbol
  typed_actors.append({'symbol':symbol,'kind':'eoa','control':'attacker' if account['control']=='controlled' else account['control'],'identity_ref':address,'evidence_refs':[{'artifact':actors,'locator':'partition/accounts/'+symbol,'origin':'approved_rule'}]})
 def typed(typ,value):
  if typ=='address':return lit('Address160',value)
  if typ=='bool':return lit('Bool',value in ['true','1'])
  if typ.startswith('uint'):return lit('BV'+(typ[4:] or '256'),value)
  if typ.startswith('bytes'):return lit('Bytes'+typ[5:],value)
  raise Invalid('component_transport_abi_unsupported')
 txs=[];observers=[]
 for i,tx in enumerate(concrete['transactions'],1):
  contract=concrete['programs'][tx['program_id']]['contract'];types=contract['constructor_types'] if tx['function']=='constructor' else next(f['types'] for f in contract['functions'] if f['signature']==tx['function'])
  envref=store.put({'id':item['id']+':context:'+str(i),'environment':tx['environment'],'value':tx['value'],'gas':tx['gas'],'program_id':tx['program_id'],'instance_id':tx['instance_id'],'actual_target':tx['target']})
  txs.append({'index':i,'target_ref':tx['instance_id'],'origin_symbol':symbols[tx['sender']],'call_kind':'top_level_eoa','function_ref':tx['function'],'arguments':[typed(t,v) for t,v in zip(types,tx['arguments'])],'value_wei':lit('BV256',tx['value']),'environment_ref':envref,'on_failure':'record_and_continue','must_succeed_for_claim':i<len(concrete['transactions'])})
  observers.append({'id':'tx'+str(i)+'.success','kind':'execution_outcome','type':'Bool','binding_ref':store.put({'id':item['id']+':exit:'+str(i),'transaction':tx,'step':i}),'world_point':'post:'+str(i),'code_instance':tx['instance_id'],'storage_instance':tx['instance_id'],'subject_keys':[]})
  for ob in concrete['observers']:
   con=concrete['programs'][ob['program_id']]['contract'];abi=next(f for f in con['functions'] if f['signature']==ob['function'])
   observers.append({'id':ob['id']+'.'+str(i),'kind':'getter_read','type':ob['type'],'binding_ref':store.put({'id':item['id']+':observer:'+ob['id']+':'+str(i),'spec':ob,'source_relation':source,'abi':abi,'environment_ref':envref,'frozen_copy':True,'initTx':False}),'world_point':'post:'+str(i),'code_instance':ob['instance_id'],'storage_instance':ob['instance_id'],'subject_keys':[typed(t,v) for t,v in zip(abi['types'],ob['arguments'])]})
 plan={'schema_version':SCHEMA_VERSION,'id':query['id']+':plan','revision':1,'program_id':bundle['program_id'],'build_id':bundle['build_id'],'query_ref':store.put(query),'query_form':q['query_form'],'runtime_refs':[store.put(d) for d in concrete['programs'].values()],'backend_fingerprint':backend,'capability_receipt':store.put(fingerprint),'initial_mode':'DEPLOYMENT','initial_state_ref':deployment,'actors':typed_actors,'transactions':txs,'observers':observers,'preconditions':[],'checked_expression':q['expression'],'nonvacuity_expression':q['premise'],'scope':scope,'limits':{'max_top_level_transactions':6,'max_plans_per_target':32,'max_proposal_revisions':2,'max_loop_iterations':12000000,'max_call_depth':1024,'max_dynamic_bytes':64,'project_time_seconds':1800,'project_candidate_limit':32,'llm_token_limit':240000,'llm_cost_limit':'10','solver_timeout_seconds':30,'candidate_timeout_seconds':180},'expected_sat_meaning':'supports_claim','expected_unsat_meaning':'refutes_claim_in_scope','fixed_intervention_ref':None,'code_modification_allowed':False,'policy_changes_allowed':False,'unresolved_critical_items':item['unresolved']}
 return query,plan,store.put(plan),backend


REPORT_SCHEMA='pr-next-analysis-report-static-v1'

def analysis_report(context,static_materials=(),historical_reports=(),gaps=(),previous=None):
 """M4 report-only intake. Static material cannot become VerificationResult.

 Reuse the existing four report areas and prediction mapping. Historical
 reports remain nested evidence, never current findings or current coverage.
 No query/compiler/backend/LLM operation is invoked by this function.
 """
 if previous is not None:
  require(previous.get('report_schema')==REPORT_SCHEMA,'report_protocol_mismatch')
  require(previous['context']==context,'report_context_changed; keep prior report under its own identity')
  require(not previous['reportable_findings'] and not previous['refuted_candidates'],'static_report_cannot_promote_current_verification')
 # Rebuild from verified source records, not from possibly stale resume rows.
 report={'report_schema':REPORT_SCHEMA,'context':copy.deepcopy(context),'status':'c2_partial_with_named_gaps','scientific_acceptance_claimed':False,'reportable_findings':[],'leads':[],'refuted_candidates':[],'coverage_and_failures':{'coverage':'partial','named_gaps':[],'current_verification_status':'not_executed'},'prediction_ledger':[],'static_material_sources':[],'historical_evidence':[]}
 def merge(field,key,value):
  existing=next((x for x in report[field] if x['id']==key),None)
  if existing is not None:require(existing==value,'report_identity_conflict:'+field+':'+key)
  else:report[field].append(value)
 for material in static_materials:
  data=material['result'];source=material['source'];input_id=material['input_id']
  require(material['purpose'] in ['research_development_input','engineering_only'],'unknown_static_material_purpose')
  require(source.get('path') and source.get('sha256') and source.get('run_id') and source.get('producer_source_version'),'static_material_source_identity')
  require(data['schema']=='c2-static-candidate-set-v1','static_report_input_schema')
  require(data['execution_confirmed'] is False and data['method_conclusion'] is None,'static_material_contains_execution_claim')
  require(all(data['counts'][k]==0 for k in ['risk_queries','transactions','LLM_calls']),'static_material_not_execution_receipt')
  mid=digest({'input_id':input_id,'source':source,'input':data['input']})
  merge('static_material_sources',mid,{'id':mid,'input_id':input_id,'purpose':material['purpose'],'source':copy.deepcopy(source),'input':copy.deepcopy(data['input']),'alias_cases':[copy.deepcopy(c['case']) for c in data['alias_cases']],'entry_inventory':copy.deepcopy(data['entry_inventory']),'static_preparation_status':'completed','execution_status':'not_executed','method_acceptance':False})
  for ci,case in enumerate(data['alias_cases']):
   require(case['case']['status'] in ['applicable','semantic_not_applicable','relation_unresolved'],'case_applicability_unknown')
   for ei,c in enumerate(case['candidates']):
    require(all(c['entry'][k]==data['input'][k] for k in ['program_id','build_id']),'candidate_input_identity_mismatch')
    require(c['method_conclusion'] is None and c['execution_plan'] is None,'static_candidate_not_verified')
    require(c['status'] in ['candidate_pending_checks','lead_unresolved'],'static_material_status')
    require(c['case_applicability']['status']==case['case']['status'],'candidate_case_status_mismatch')
    require(c['caller']['identity']==case['case']['mapping']['B'],'normalized_caller_identity_mismatch')
    require(digest(data['source_analyses'][c['analysis_ref']['id']])==c['analysis_ref']['sha256'],'source_analysis_identity')
    locator=f'/alias_cases/{ci}/candidates/{ei}'
    key=digest({'material':mid,'candidate':c['id'],'alias_case':case['case']['id']})
    item={'id':key,'input_id':input_id,'material_id':mid,'candidate_id':c['id'],'entry':copy.deepcopy(c['entry']),'caller':copy.deepcopy(c['caller']),'alias_case_id':case['case']['id'],'case_applicability':copy.deepcopy(c['case_applicability']),'material_status':c['status'],'case_candidate_status':c['case_candidate_status'],'static_preparation_status':'completed','execution_status':'not_executed','solver_status':'not_called','verdict':None,'evidence_level':None,'candidate_ref':{'artifact':copy.deepcopy(source),'locator':locator,'content_sha256':digest(c)},'source_analysis_ref':{'artifact':copy.deepcopy(source),'locator':'/source_analyses/'+c['analysis_ref']['id'],'content_sha256':c['analysis_ref']['sha256']},'effect_sources':[{'kind':e['kind'],'source':e.get('source'),'evidence_strength':e.get('evidence_strength'),'locator':locator+f'/effects/{i}'} for i,e in enumerate(c['effects'])],'role_bindings':[{'compiler_key_type':r['compiler_key_type'],'key':copy.deepcopy(r['key']),'storage_declaration':copy.deepcopy(r['storage_declaration']),'field_ids':r['field_ids'],'index_source':r['index_source'],'role_status':r['business_role']['status'],'role':r['business_role']['role'],'evidence_locator':locator+f'/relations/{i}'} for i,r in enumerate(c['relations'])],'policy_associations':[{'status':p['status'],'sources':copy.deepcopy(p.get('sources',[])),'unresolved':copy.deepcopy(p.get('unresolved',[])),'locator':locator+f'/policy_associations/{i}'} for i,p in enumerate(c['policy_associations'])],'guard_observation':copy.deepcopy(c['guard_observation']),'unresolved':copy.deepcopy(c['unresolved']),'required_next_capabilities':copy.deepcopy(c['required_next_capabilities'])}
    merge('leads',key,item)
  if material['purpose']=='research_development_input':
   for task in ['AC','FCR_TRANSFER','FCR_MINT','FCR_DESTROY','FCR_PAUSE','FCR_FREEZE']:
    key=digest({'input':input_id,'program':data['input'],'task':task,'material':mid})
    merge('prediction_ledger',key,{'id':key,'group':input_id,'program_id':data['input']['program_id'],'build_id':data['input']['build_id'],'material_id':mid,'task':task,'prediction':prediction(False,True),'coverage':'partial','execution_status':'not_executed','not_gold_scoring':True,'reason':'static material only; no current VerificationResult or complete negative coverage'})
 for history in historical_reports:
  source=history['source'];require(source.get('run_id') and source.get('producer_source_version') and source.get('sha256'),'historical_version_and_run_required')
  require(history.get('verification_results'),'historical_execution_requires_referenced_results')
  for result in history['verification_results']:
   require(all(result.get(k) for k in ['program_id','build_id','query_ref','plan_ref','backend_fingerprint','scope']),'historical_verification_identity_required')
  key=digest(source)
  merge('historical_evidence',key,{'id':key,'source':copy.deepcopy(source),'report':copy.deepcopy(history['report']),'verification_results':copy.deepcopy(history['verification_results']),'result_sources':copy.deepcopy(history['result_sources']),'application':'historical_recorded_version_and_scope_only','counts_as_current_C2_execution':False,'current_version_revalidated':False})
 all_gaps=report['coverage_and_failures']['named_gaps']+list(gaps)
 report['coverage_and_failures']['named_gaps']=sorted({digest(g):copy.deepcopy(g) for g in all_gaps}.values(),key=digest)
 for name in ['leads','prediction_ledger','static_material_sources','historical_evidence']:report[name].sort(key=lambda x:x['id'])
 report['counts']={'static_materials':len(report['static_material_sources']),'static_candidate_case_records':len(report['leads']),'historical_reports':len(report['historical_evidence']),'current_verification_results':0,'current_findings':0,'current_refutations':0}
 if previous is not None:require(previous==report,'report_resume_content_mismatch')
 return report

def render_analysis_report(report):
 """Readable view of the same report object; no independent classifications."""
 def text(value):return str(value).replace('|','\\|').replace('\n',' ')
 def link(source,label):return '['+text(label)+'](<'+source['path'].replace('\\','/')+'>)'
 lines=['# C2 已有结果接入报告','',f"状态：{report['status']}。本报告只整理已有证据，没有重新分析或执行程序。",'','当前候选均为静态待核材料；风险结论为空，验证未运行，预测弃权。历史执行结果不计入当前 C2 验证。','','分案状态：applicable 为声明前提下适用；semantic_not_applicable 为前提不适用；relation_unresolved 为关系未决。三者均不是执行结论。','']
 for material in sorted(report['static_material_sources'],key=lambda x:x['input_id']):
  lines+=['## '+material['input_id'],'',link(material['source'],'原始静态结果')+'；程序 '+material['input']['program_id']+'；构建 '+material['input']['build_id']+'。','', '静态生产版本：'+material['source']['producer_source_version']+'；运行：'+material['source']['run_id']+'。','', '| 主体分案 | 适用状态 | 原因 |','|---|---|---|']
  for case in material['alias_cases']:
   reasons=case['reasons']+case['unresolved']
   concise=[(str(r.get('reason',r))+('；主体 '+','.join(r['subjects']) if r.get('subjects') else '')) if isinstance(r,dict) else str(r) for r in reasons]
   lines.append('| '+text(case['id'])+' | '+text(case['status'])+' | '+text('; '.join(concise) or '当前声明前提下无额外未决项；尚未执行')+' |')
  lines+=['','以下每个入口的完整逐分案绑定、来源位置与未解析结构保存在原始结果和 JSON 报告中。','']
  entries={r['candidate_id']:r for r in report['leads'] if r['material_id']==material['id']}
  for c in sorted(entries.values(),key=lambda x:x['entry']['function']):
   reasons=[str(u.get('reason',u)) if isinstance(u,dict) else str(u) for u in c['unresolved']]
   reasons += [str(u) for p in c['policy_associations'] for u in p['unresolved']]
   roles=sorted({'编译类型 '+str(r['compiler_key_type'])+'；来源角色 '+(r['role'] or '未解析')+'（'+r['role_status']+'）' for r in c['role_bindings']})
   positions=[str(e.get('source',{}).get('file'))+':'+str(e.get('source',{}).get('start')) for e in c['effect_sources'] if e.get('source')]
   lines += ['- **'+text(c['entry']['function'])+'**：'+c['material_status']+'；验证 `not_executed`；政策关联 '+text(', '.join(p['status'] for p in c['policy_associations']))+'。', '  效果来源：'+text(', '.join(positions) or '见原始外部调用/原生清单引用')+'；键角色：'+text(', '.join(roles) or '无已解析映射键角色')+'。', '  未解析：'+text('; '.join(dict.fromkeys(reasons)) or '本层没有额外条目；仍需后续原程序验证')+'。', '  后续能力：'+text(', '.join(c['required_next_capabilities']))+'。']
  lines.append('')
 lines+=['## 历史原程序证据','','仅保留原版本、查询和范围；没有将旧证据绑定到当前 C2 源码。','']
 for h in report['historical_evidence']:
  lines += [link(h['source'],'历史报告')+'；运行 '+h['source']['run_id']+'；交付源码版本 '+h['source']['producer_source_version']+'。','']
  for finding in h['report'].get('reportable_findings',[]):lines.append('- '+text(finding.get('claim_cn',finding.get('id')))+' 限制：'+text(finding.get('limits_cn','详见历史报告')))
  lines+=['- 历史核查记录的 program/build/query/plan/backend、范围、solver/execution/replay 和限制逐项原样保留在 JSON 报告中。','']
 lines+=['## 当前缺项','']+[ '- '+text(g.get('capability',g.get('id','gap')))+'：'+text(g.get('status','unresolved'))+'；'+text(g.get('limit',g.get('detail_cn',''))) for g in report['coverage_and_failures']['named_gaps']]
 return '\n'.join(lines)+'\n'
