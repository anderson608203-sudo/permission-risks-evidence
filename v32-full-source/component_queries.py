"""Source-bound component queries; no project names or expected outcomes.

This is an M3/M4 component consumer of M1/M2 static material, not a replacement
for the joint method's LLM proposal stage. Unsupported associations stay leads.
Policy selection uses typed policy_kind, never a fixed natural-language sentence.
"""
import copy
from .core import require,digest,ref,lit,obs,operator
from .facts import walk
from .source_paths import SourcePaths
from .static_roles import same_path_family
from .instances import descriptor
from .environment import environment
from .multi_service import PLAN_SCHEMA,validate_plan

def unique(items,reason):
 items=list({digest(x):x for x in items}.values());require(len(items)==1,reason);return items[0]

def parameter(term):
 require(term.get('kind')=='parameter','non_parameter_value_requires_adapter')
 return term['declaration']['ast_id']

def getter(lookup,state_id):
 matches=[]
 for abi in lookup.contract['functions']:
  if not abi['readonly']:continue
  node=lookup.function(abi['signature'])
  if node.get('generated_getter',{}).get('id')==state_id:matches.append(abi)
 return unique(matches,'unique_compiler_getter_required')

def frames(static,candidate):
 analysis=static['source_analyses'][candidate['analysis_ref']['id']]
 require(digest(analysis)==candidate['analysis_ref']['sha256'],'static_analysis_identity')
 require(analysis.get('schema')=='sourced-bindings-v2' and len(analysis['frames'])==1,'single_source_frame_adapter_required')
 frame=analysis['frames'][0]
 require(not frame['external_calls'] and not frame['unresolved'],'unresolved_source_path')
 return frame

def args_for(frame,bindings):
 ids=[x['parameter']['ast_id'] for x in frame['entry']['argument_bindings']]
 require(set(ids)==set(bindings),'unbound_or_extra_parameter')
 return [str(bindings[i]) for i in ids]

def constructor_authority(lookup,state_id):
 # A source proof of deployment ownership; actual constructor and getter still run.
 trace=lookup.trace('constructor',[],caller='$DEPLOYER')
 require(trace['native_agreement'] and not trace['unresolved'],'constructor_source_unresolved')
 writes=[w for w in trace['writes'] if w['path']['root']==state_id and not w['path']['segments']]
 require(len(writes)==1 and writes[0]['value']=={'kind':'literal','value':'$DEPLOYER'},'authority_not_constructor_caller')
 return {'constructor':trace,'authority_getter':getter(lookup,state_id)}

def authority_guard(lookup,frame):
 matches=[]
 for g in frame['guards']:
  condition=g['condition']
  if condition.get('kind')!='op' or condition.get('op')!='==':continue
  terms=condition.get('args',[])
  paths=[t for t in terms if t.get('kind')=='storage_binding' and not t['segments']]
  callers=[t for t in terms if t.get('kind') in ['frame_caller','subject']]
  if len(paths)==len(callers)==1:
   path=paths[0];proof=constructor_authority(lookup,path['declaration']['ast_id'])
   matches.append({'guard':g,'path':path,'proof':proof})
 return unique(matches,'legitimate_prefix_authority_unresolved')

def _sig(value):
 return ''.join(str(value or '').split())

def _check_m04_binding(policy,frame,grant,qualification,effect):
 binding=policy.get('binding') or {}
 require(binding.get('qualification',{}).get('declaration')==qualification['declaration']['name'],'m04_binding_qualification_mismatch')
 require(_sig(binding.get('use',{}).get('function_signature'))==_sig(frame['entry']['function']),'m04_binding_use_function_mismatch')
 require(_sig(binding.get('assignment',{}).get('function_signature'))==_sig(grant['frame']['entry']['function']),'m04_binding_grant_function_mismatch')
 require(binding.get('qualification',{}).get('compiler_type')==qualification['declaration']['type'],'m04_binding_qualification_type_mismatch')
 require('value' in str(binding.get('use',{}).get('protected_effect','')) and effect['path']['declaration']['name']=='value','m04_binding_effect_mismatch')
 require('timestamp' in str(binding.get('time',{}).get('validity','')) and 'boundary' in binding.get('time',{}),'m04_binding_time_semantics_missing')
 return binding

def classify(static,candidate,lookup,policy):
 frame=frames(static,candidate);links=candidate['policy_associations']
 kind=policy.get('kind')
 require(kind in ['authority_effect','caller_resource','temporal_qualification'],'policy_kind_not_implemented:'+str(kind))
 require(policy.get('source') and any(s['program_id']==lookup.bundle['program_id'] and s['build_id']==lookup.bundle['build_id'] and s['contract_file']==lookup.contract['file'] and s['contract_name']==lookup.contract['name'] and s.get('basis') for s in policy.get('applies_to',[])),'policy_scope_unresolved')
 writes=[r for r in frame['relationships'] if r['operation']=='write']
 if kind=='authority_effect':
  authority=[s for link in links for s in link.get('sources',[]) if s.get('kind')=='explicit_policy_state_references']
  require(authority,'authority_policy_association_unresolved')
  association=unique(authority,'ambiguous_policy_authority');effect=unique([w for w in writes if w['path']['declaration']['ast_id']==association['effect_ast_id']],'policy_effect_not_unique')
  require(not effect['path']['segments'],'scalar_effect_adapter_required')
  proof=constructor_authority(lookup,association['authority_ast_id'])
  return {'kind':kind,'rule':'AC-01','frame':frame,'effect':effect,'value_parameter':parameter(effect['value']),'authority':proof,'association':association,'critical_unresolved':[]}
 if kind=='caller_resource':
  matches=[m for link in links for m in link.get('effect_matches',[]) if m.get('basis')=='explicit_policy_resource_parameter_in_guard_and_different_written_object']
  m=unique(matches,'resource_policy_effect_unresolved');effect=unique([w for w in writes if w['source']==m['effect_source']],'effect_source_unresolved')
  require(len(effect['path']['segments'])==1,'resource_path_adapter_required');resource=parameter(effect['path']['segments'][0]['key'])
  q=unique([c['path'] for c in m['usage_correspondences']],'qualification_family_ambiguous');require(len(q['segments'])==2,'qualification_key_arity')
  resource_ix=[i for i,s in enumerate(q['segments']) if s['key'].get('kind')=='parameter' and parameter(s['key'])==resource];require(len(resource_ix)==1,'resource_key_correspondence')
  principal_ix=1-resource_ix[0];segment=q['segments'][principal_ix];term=segment['key']
  require(term.get('kind') in ['parameter','subject','frame_caller','account'],'qualification_key_origin_unresolved')
  origins=segment.get('origins',[])
  checked_kind='parameter' if term.get('kind')=='parameter' else 'frame_caller' if any(o.get('kind')=='frame_caller' for o in origins) else term.get('kind')
  checked_parameter=parameter(term) if checked_kind=='parameter' else None
  # The other key denotes a qualification subject because the independently
  # scoped policy requires caller qualification, not because its ABI is address.
  activation=[]
  for other in static['alias_cases'][0]['candidates']:
   f=frames(static,other)
   for w in f['relationships']:
    if w['operation']=='write' and same_path_family(w['path'],q) and w.get('value')=={'kind':'literal','value':True}:
     activation.append({'candidate':other,'frame':f,'write':w,'authority':authority_guard(lookup,f)})
  grant=unique(activation,'legitimate_qualification_activation_unresolved')
  return {'kind':kind,'rule':'AC-03','frame':frame,'effect':effect,'value_parameter':parameter(effect['value']),'resource_parameter':resource,'qualification':q,'principal_index':principal_ix,'resource_index':resource_ix[0],'credential_parameter':checked_parameter,'checked_subject_kind':checked_kind,'checked_subject_parameter':checked_parameter,'grant':grant,'association':m,'critical_unresolved':[]}
 # temporal_qualification: the explicit R4 M04 binding is the policy source.
 effect=unique(writes,'temporal_effect_not_unique');parameter(effect['value'])
 paths=[p for g in frame['guards'] for p in walk(g['condition']) if p.get('kind')=='storage_binding' and p['declaration']['ast_id']!=effect['path']['declaration']['ast_id'] and len(p['segments'])==1 and p['segments'][0]['key'].get('kind') in ['subject','frame_caller','account']]
 qualification=unique(paths,'caller_qualification_unresolved')
 setters=[]
 for other in static['alias_cases'][0]['candidates']:
  f=frames(static,other)
  for w in f['relationships']:
   if w['operation']=='write' and same_path_family(w['path'],qualification) and w.get('value',{}).get('kind')=='parameter':setters.append({'candidate':other,'frame':f,'write':w,'authority':authority_guard(lookup,f)})
 setter=unique(setters,'temporal_initializer_unresolved')
 binding=_check_m04_binding(policy,frame,setter,qualification,effect)
 temporal=[g for g in frame['guards'] if any(n.get('kind')=='environment' and n.get('field')=='timestamp' for n in walk(g['condition'])) and any(n.get('kind')=='storage_binding' and same_path_family(n,qualification) for n in walk(g['condition']))]
 return {'kind':kind,'rule':'AC-04','frame':frame,'effect':effect,'value_parameter':parameter(effect['value']),'qualification':qualification,'grant':setter,'association':{'policy':policy,'binding':binding,'qualification_use':paths,'timestamp_comparisons':temporal},'program_time_correspondence':'present' if temporal else 'absent','critical_unresolved':[]}

RULE_CHECKS={
 'AC-01':['independent scoped policy','reachable deployment and legitimate prefix','caller/resource/source identity','original effect','same-engine replay'],
 'AC-03':['checked credential/subject identity','actual caller-origin and invocation frame','same resource key and object','no applicable delegation or alternative authorization','successful original call and committed effect','same-engine replay'],
 'AC-04':['same subject and credential key','legitimate prior activation','original revocation or expiry condition','no intervening legal regrant','later accepted call and actual protected effect','same-engine replay']}

def prepare_queries(bundle,contract,static,policy,settings):
 if policy.get('kind')=='authority_effect' and policy.get('typed_relations',{}).get('object_effect'):
  from .object_effect_queries import prepare_object_queries
  return prepare_object_queries(bundle,contract,static,policy,settings)
 require(all(static['input'][k]==bundle[k] for k in ['program_id','build_id']),'static_program_identity')
 require(not contract['constructor_types'],'constructor_arguments_unresolved')
 lookup=SourcePaths(bundle,contract);entry=descriptor(bundle,contract);pid=digest(entry);iid=static['input']['contract_file']+':'+static['input']['contract_name'];prepared=[];leads=[];cases=[]
 for case_record in static['alias_cases']:
  case=case_record['case'];cases.append(copy.deepcopy(case))
  if case['status']!='applicable':continue
  addresses={k:v['address'] for k,v in case['mapping'].items()}
  require(addresses['A']==settings['deployment_address_basis']['sender'],'deployment_address_sender_changed')
  for candidate in case_record['candidates']:
   try:
    relation=classify(static,candidate,lookup,policy);frame=relation['frame'];kind=relation['kind'];rule=relation['rule']
    valueid=relation['value_parameter'];valueabi=next(x for x in frame['entry']['argument_bindings'] if x['parameter']['ast_id']==valueid)['term']['compiler_type'];require(valueabi=='uint256','effect_scalar_type_unsupported')
    scenarios=([('controlled','B',None),('authorized','A',None),('no_effect','B',0)] if kind=='authority_effect' else [('credential_other','B',0),('credential_self','B',1),('qualified_caller','C',0),('other_resource','B',2)] if kind=='caller_resource' else [('before','B',-1),('boundary','B',0),('after','B',1)])
    for scenario,actor,variant in scenarios:
     plan={'schema':PLAN_SCHEMA,'id':digest({'candidate':candidate['id'],'case':case['id'],'scenario':scenario,'settings':settings,'rule':rule}),'programs':{pid:entry},'instances':{iid:{'program_id':pid,'target':settings['deployment_address_basis']['target']}},'accounts':sorted(set(addresses.values())),'environment':environment(settings['block_number'],settings['timestamp']),'transactions':[],'observers':[]}
     def tx(function,args,who,context=None):
      plan['transactions'].append({**plan['instances'][iid],'instance_id':iid,'sender':addresses[who],'function':function,'arguments':list(args),'environment':context or plan['environment'],'value':0,'gas':12000000})
     def observe(oid,path,args,typ):
      g=getter(lookup,path['declaration']['ast_id'] if isinstance(path,dict) else path)
      require(len(g['types'])==len(args),'observer_key_count');plan['observers'].append({**plan['instances'][iid],'instance_id':iid,'id':oid,'caller':addresses['A'],'function':g['signature'],'arguments':list(args),'type':typ,'output_index':0})
     tx('constructor',[],'A');bindings={valueid:str(settings['concrete_scalar'])};
     if scenario=='no_effect':bindings[valueid]='0'
     effectargs=[];allowed=None;prefix_conditions=[];context=None;metadata={}
     if kind=='authority_effect':
      sid=relation['association']['authority_ast_id'];observe('authority',sid,[],'Address160');allowed=operator('eq','Bool',lit('Address160',addresses[actor]),obs('authority.1','Address160'))
      prefix_conditions.append(operator('eq','Bool',obs('authority.1','Address160'),lit('Address160',addresses['A'])))
      metadata={'policy_kind':kind,'authority_source':'constructor_caller'}
     elif kind=='caller_resource':
      grant=relation['grant'];principal=relation['principal_index'];resourceix=relation['resource_index'];q=relation['qualification'];keys=[None,None]
      checked_symbol='C' if scenario in ['credential_other','qualified_caller','other_resource'] else actor
      if relation['checked_subject_kind']=='frame_caller':checked_symbol=actor
      checked=addresses[checked_symbol];actual=addresses[actor]
      keys[principal]=checked;keys[resourceix]=settings['resource_keys'][0]
      gb={parameter(s['key']):keys[i] for i,s in enumerate(grant['write']['path']['segments'])};tx(grant['frame']['entry']['function'],args_for(grant['frame'],gb),'A')
      resource=settings['resource_keys'][1 if variant==2 else 0];bindings[relation['resource_parameter']]=resource
      if relation['credential_parameter'] is not None:bindings[relation['credential_parameter']]=checked
      ids=[x['parameter']['ast_id'] for x in frame['entry']['argument_bindings']]
      remaining=set(ids)-set(bindings);require(len(remaining)<=1,'extra_unbound_credential_parameters')
      for ident in remaining:
       abi=next(x for x in frame['entry']['argument_bindings'] if x['parameter']['ast_id']==ident)['term']['compiler_type']
       bindings[ident]=addresses['C'] if abi=='address' else '1'
      qkeys=list(keys);qkeys[principal]=checked;qkeys[resourceix]=resource;akeys=list(keys);akeys[principal]=actual;akeys[resourceix]=resource
      observe('granted',q,keys,'Bool');observe('checked',q,qkeys,'Bool');observe('actual',q,akeys,'Bool');allowed=obs('checked.2','Bool');prefix_conditions.extend([obs('granted.2','Bool')])
      metadata={'policy_kind':kind,'checked_subject_kind':relation['checked_subject_kind'],'checked_subject_parameter':relation['checked_subject_parameter'],'checked_address':checked,'actual_actor_address':actual,'alternative_authorization':'explicit_no_delegation_in_policy','resource_key':resource}
      effectargs=[resource]
     else:
      grant=relation['grant'];expiry=settings['timestamp']+settings['expiry_offset'];gb={parameter(grant['write']['path']['segments'][0]['key']):addresses[actor],parameter(grant['write']['value']):str(expiry)}
      tx(grant['frame']['entry']['function'],args_for(grant['frame'],gb),'A');context=environment(settings['block_number']+1,expiry+variant)
      observe('qualification',relation['qualification'],[addresses[actor]],'BV256');allowed=operator('and','Bool',operator('ne','Bool',obs('qualification.2'),lit('BV256',0)),operator('ult','Bool',lit('BV256',context['timestamp']),obs('qualification.2')))
      prefix_conditions.append(operator('eq','Bool',obs('qualification.2'),lit('BV256',expiry)))
      metadata={'policy_kind':kind,'policy_binding_sha256':policy.get('binding_source',{}).get('sha256'),'program_time_correspondence':relation['program_time_correspondence'],'validity':'timestamp_strictly_before_expiry','boundary':'timestamp_equals_expiry_is_outside_validity'}
     if kind!='authority_effect':
      bootstrap=relation['grant']['authority'];observe('authority',bootstrap['path'],[],'Address160');prefix_conditions.append(operator('eq','Bool',obs('authority.1','Address160'),lit('Address160',addresses['A'])))
     tx(frame['entry']['function'],args_for(frame,bindings),actor,context);observe('effect',relation['effect']['path'],effectargs,'BV256');step=len(plan['transactions'])
     changed=operator('ne','Bool',obs('effect.'+str(step)),obs('effect.'+str(step-1)))
     if kind=='caller_resource':
      address_distinct=operator('ne','Bool',lit('Address160',metadata['checked_address']),lit('Address160',metadata['actual_actor_address']))
      violation=operator('and','Bool',obs('checked.'+str(step),'Bool'),operator('not','Bool',obs('actual.'+str(step),'Bool')),obs('tx'+str(step)+'.success','Bool'),changed)
      premise=operator('and','Bool',*[obs('tx'+str(i)+'.success','Bool') for i in range(1,step)],*prefix_conditions,address_distinct)
     else:
      violation=operator('and','Bool',operator('not','Bool',allowed),obs('tx'+str(step)+'.success','Bool'),changed)
      premise=operator('and','Bool',*[obs('tx'+str(i)+'.success','Bool') for i in range(1,step)],*prefix_conditions)
     query={'rule':rule,'query_form':'EXISTS_VIOLATION','premise':premise,'expression':violation,'policy_allowed':allowed,'effect_expression':changed,'required_rule_checks':RULE_CHECKS[rule],'applicability':'unresolved' if relation['critical_unresolved'] else 'applicable','policy_kind':kind,'checked_subject':{k:metadata.get(k) for k in ['checked_subject_kind','checked_subject_parameter','checked_address']} if kind=='caller_resource' else None,'actual_actor_address':metadata.get('actual_actor_address') if kind=='caller_resource' else None,'alternative_authorization':metadata.get('alternative_authorization') if kind=='caller_resource' else None}
     if kind=='caller_resource':query['actual_actor_allowed']=obs('actual.'+str(step),'Bool')
     if kind=='temporal_qualification':query['policy_binding_sha256']=metadata.get('policy_binding_sha256');query['program_time_correspondence']=metadata.get('program_time_correspondence');query['validity']=metadata.get('validity');query['boundary']=metadata.get('boundary')
     validate_plan(plan)
     prepared.append({'id':plan['id'],'candidate_ref':ref(candidate),'static_ref':ref(static),'alias_case':case,'scenario':scenario,'source_relation':relation,'policy':policy,'program_id':bundle['program_id'],'build_id':bundle['build_id'],'plan':plan,'query':query,'mode':settings['mode'],'symbolic_parameter_index':next(i for i,x in enumerate(frame['entry']['argument_bindings']) if x['parameter']['ast_id']==valueid),'unresolved':relation['critical_unresolved'],'scope':'one reachable concrete trajectory; other parameters/paths remain uncovered','component_only':True,'LLM_called':False,'control_only':scenario=='no_effect','purpose':'no_effect_control' if scenario=='no_effect' else 'risk_candidate'})
   except (ValueError,KeyError,IndexError,TypeError) as error:leads.append({'candidate_ref':ref(candidate),'case_id':case['id'],'entry':candidate['entry'],'status':'unresolved','reason':str(error),'execution_status':'not_executed'})
 require(len(prepared)*2<=32,'per_target_plan_cap_including_replay')
 return {'prepared':prepared,'leads':leads,'alias_cases':cases,'static_ref':ref(static),'program_id':bundle['program_id'],'build_id':bundle['build_id'],'rule_family':sorted({p['query']['rule'] for p in prepared})}
