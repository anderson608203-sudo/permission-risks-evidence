"""Versioned ordinary multi-instance branch of the same eight-method service."""
import copy,json,pathlib,re,subprocess,time,uuid
from .core import require,ref,digest,Invalid
from .instances import InstanceRuntime,load_request
from .environment import validate
from .backend import check_formula

PROTOCOL='pr-next-joint-eight-methods-v3'
PLAN_SCHEMA='concrete-multi-plan-v1'
METHODS=('hello','load_program','create_world','execute_top_transaction','observe','check_formula','materialize_witness','close_world')

class DeadlineNative:
 def __init__(self,native,deadline):self.native=native;self.deadline=deadline
 def request(self,request,timeout=30):
  remaining=self.deadline-time.monotonic();require(remaining>0,'candidate_timeout')
  return self.native.request(request,min(timeout,remaining))

def address(value):
 require(isinstance(value,str) and re.fullmatch('0x[0-9a-f]{40}',value),'canonical_address_required')

def validate_plan(plan):
 require(set(plan)=={'schema','id','programs','instances','accounts','environment','transactions','observers'},'multi_plan_fields')
 require(plan['schema']==PLAN_SCHEMA,'multi_plan_schema');validate(plan['environment'])
 require(plan['accounts']==sorted(set(plan['accounts'])) and plan['accounts'],'initial_accounts')
 for account in plan['accounts']:address(account)
 for key,entry in plan['programs'].items():
  require(key==digest(entry),'program_descriptor_identity');load_request(entry)
 require(0<len(plan['transactions'])<=6,'transaction_cap');require(0<len(plan['instances'])<=6,'instance_cap')
 targets=[]
 for iid,inst in plan['instances'].items():
  require(isinstance(iid,str) and iid and set(inst)=={'program_id','target'},'instance_fields')
  require(inst['program_id'] in plan['programs'],'instance_program');address(inst['target']);targets.append(inst['target'])
 require(len(set(targets))==len(targets) and not set(targets)&set(plan['accounts']),'instance_address_conflict')
 deployed=set();previous=plan['environment']
 for tx in plan['transactions']:
  require(set(tx)=={'program_id','instance_id','target','sender','function','arguments','environment','value','gas'},'transaction_fields')
  binding(plan,tx);require(tx['sender'] in plan['accounts'],'undeclared_sender')
  require(isinstance(tx['arguments'],list) and all(isinstance(x,str) for x in tx['arguments']),'argument_strings')
  require(type(tx['value'])is int and 0<=tx['value']<2**256 and type(tx['gas'])is int and 0<tx['gas']<=30000000,'transaction_limits')
  validate(tx['environment'],previous);previous=tx['environment']
  if tx['function']=='constructor':require(tx['instance_id'] not in deployed,'duplicate_deployment');deployed.add(tx['instance_id'])
  else:require(tx['instance_id'] in deployed,'call_before_deployment')
 ids=set()
 for spec in plan['observers']:
  require(set(spec)=={'id','program_id','instance_id','target','caller','function','arguments','type','output_index'},'observer_fields')
  binding(plan,spec);require(spec['caller'] in plan['accounts'],'observer_caller')
  require(spec['id'] not in ids and isinstance(spec['id'],str),'observer_id');ids.add(spec['id'])
  require(spec['type'] in ['Bool','Address160','BV256'] and type(spec['output_index'])is int and spec['output_index']>=0,'observer_output')
 return plan

def binding(plan,item):
 require(item['instance_id'] in plan['instances'],'unknown_instance')
 require(plan['instances'][item['instance_id']]=={k:item[k] for k in ['program_id','target']},'program_instance_target_mismatch')

def observer_request(world,spec):
 return {'op':'observe','world':world,**{k:spec[k] for k in ['program_id','instance_id','target','caller','function','arguments']}}

def replay_comparison(original,replay):
 normalize=lambda items:[{k:v for k,v in item.items() if k not in ['world','execution_id']} for item in items]
 checks={'transactions_equal':normalize(original['transactions'])==normalize(replay['transactions']),
         'observations_equal':normalize(original['observations'])==normalize(replay['observations']),
         'registry_equal':original['registry']==replay['registry'],
         'world_records_equal':original['world_records']==replay['world_records']}
 return {**checks,'equal':all(checks.values())}

def execute_multi(client,plan):
 """Normal client path, also used for same-engine replay. Every operation is public RPC."""
 hello=client.request({'op':'hello'});require(hello['protocol']==PROTOCOL,'multi_protocol_required')
 for key in plan['programs']:client.request({'op':'load_program','program_id':key})
 created=client.request({'op':'create_world','accounts':plan['accounts'],'environment':plan['environment']})
 world=created['world'];worlds=[world];transactions=[];observations=[];deployed=set()
 try:
  for tx in plan['transactions']:
   receipt=client.request({'op':'execute_top_transaction','world':world,**tx});transactions.append(receipt);world=receipt['world'];worlds.append(world)
   if tx['function']=='constructor' and receipt['status']=='success':deployed.add(tx['instance_id'])
   for spec in plan['observers']:
    if spec['instance_id'] in deployed:observations.append({'id':spec['id'],'step':len(transactions),'receipt':client.request(observer_request(world,spec))})
  return {'execution_id':created['execution_id'],'plan_ref':ref(plan),'transactions':transactions,'observations':observations,'initial_world':created,'scope':'fixed concrete trajectory; no path search'}
 finally:
  for world in worlds:client.request({'op':'close_world','world':world})

class MultiService:
 def __init__(self,owner):
  require(len(owner.registrations)<=32,'registered_plan_cap')
  self.owner=owner;self.native=owner.native;self.root=owner.root/'multi';self.root.mkdir(exist_ok=True)
  self.loaded=set();self.worlds={};self.executions={};self.closed=set();self.current=None;self.sequence=0

 def request(self,request,timeout=30):
  response=self.handle({'protocol':PROTOCOL,'request_id':uuid.uuid4().hex,'plan_ref':self.current,'op':request['op'],'params':{k:v for k,v in request.items() if k!='op'}},timeout)
  require(response['status']=='ok',response.get('error','multi_service_error'));return response['result']

 def snapshot(self,runtime,accounts,plan_ref):
  value={'plan_ref':plan_ref,'environment':copy.deepcopy(runtime.environment),'accounts':accounts,'instances':copy.deepcopy(runtime.instances)}
  return {**value,'sha256':digest(value)}

 def handle(self,envelope,timeout=30):
  started=time.monotonic();rid=envelope.get('request_id');op=envelope.get('op');execution=None
  try:
   require(set(envelope)=={'protocol','request_id','plan_ref','op','params'} and envelope['protocol']==PROTOCOL,'explicit_v3_protocol_required')
   require(isinstance(rid,str) and rid and rid not in self.owner.seen,'request_identity_reuse');self.owner.seen.add(rid)
   require(op in METHODS,'unknown_operation');self.owner.select(envelope['plan_ref']);self.current=envelope['plan_ref'];key=self.current['sha256']
   reg=self.owner.registrations[key];plan=validate_plan(reg['candidate']['plan']);args=envelope['params']
   remaining=self.owner.deadlines[key]-time.monotonic();require(remaining>0,'candidate_timeout');timeout=min(timeout,remaining)
   if op=='hello':
    require(not args,'hello_arguments');result={**self.native.request({'op':'hello'},timeout),'protocol':PROTOCOL,'plan_schema':PLAN_SCHEMA,'methods':list(METHODS),'condition_scope':'fixed concrete trajectory only','legacy_compatibility':'v2 accepts legacy single-target plans only; v3 required for multi-instance plans'}
   elif op=='load_program':
    require(set(args)=={'program_id'} and args['program_id'] in plan['programs'],'undeclared_program');pid=args['program_id']
    result=self.native.request(load_request(plan['programs'][pid]),timeout);require(result['loaded']==pid,'loaded_program_mismatch');self.loaded.add(pid)
   elif op=='create_world':
    require(sum(x['plan']==key for x in self.executions.values())<32,'execution_plan_cap')
    require(args=={'accounts':plan['accounts'],'environment':plan['environment']},'undeclared_initial_world')
    require(set(plan['programs'])<=self.loaded,'program_not_loaded');self.sequence+=1
    runtime=InstanceRuntime(DeadlineNative(self.native,self.owner.deadlines[key]),plan['accounts'],self.root/('execution_'+str(self.sequence)),environment=plan['environment'])
    runtime.programs=copy.deepcopy(plan['programs']);eid=runtime.world
    snapshot=self.snapshot(runtime,runtime.created['accounts'],self.current)
    self.executions[eid]={'plan':key,'runtime':runtime,'transactions':[],'observations':[],'registry':{},'world_records':[snapshot]}
    self.worlds[eid]=eid;result={**runtime.created,'execution_id':eid,'world_record':snapshot}
   elif op in ['execute_top_transaction','observe','close_world']:
    world=args.get('world');require(world in self.worlds and world not in self.closed,'closed_or_unknown_world')
    eid=self.worlds[world];execution=self.executions[eid];runtime=execution['runtime'];require(execution['plan']==key,'cross_plan_world')
    if op=='close_world':
     require(set(args)=={'world'},'close_fields');result=self.native.request({'op':op,'world':world},timeout);self.closed.add(world)
     if world in runtime.worlds:runtime.worlds.remove(world)
     if world==runtime.world:runtime.usable=False
    else:
     require(world==runtime.world,'nonlinear_or_reused_world');require(runtime.usable,'closed_or_unverified_session')
     if op=='execute_top_transaction':
      step=runtime.steps;require(step<len(plan['transactions']),'plan_exhausted');tx=plan['transactions'][step]
      require(args=={'world':world,**tx},'transaction_not_in_frozen_plan')
      options={k:tx[k] for k in ['environment','value','gas']}
      if tx['function']=='constructor':result=runtime.deploy(tx['program_id'],tx['instance_id'],tx['sender'],tx['arguments'],**options)
      else:result=runtime.call(tx['instance_id'],tx['sender'],tx['function'],tx['arguments'],**options)
      try:require(result['target'].lower()==tx['target'],'deployed_target_not_in_frozen_plan')
      except Exception:runtime.usable=False;raise
      snapshot=self.snapshot(runtime,result['post'],self.current);result.update(execution_id=eid,world_record=snapshot)
      execution['transactions'].append(copy.deepcopy(result));execution['world_records'].append(snapshot);self.worlds[result['world']]=eid
      execution['registry']['tx'+str(runtime.steps)+'.success']={'type':'Bool','value':result['status']=='success','point':runtime.steps}
     else:
      matches=[spec for spec in plan['observers'] if args=={k:v for k,v in observer_request(world,spec).items() if k!='op'}]
      require(matches,'observer_not_in_frozen_plan');spec=matches[0]
      result=runtime.observe(spec['instance_id'],spec['caller'],spec['function'],spec['arguments'])
      result.update(execution_id=eid,world_ref=execution['world_records'][-1]['sha256'])
      for spec in matches:
       raw=bytes.fromhex(result['output'][2:]);ix=spec['output_index'];require(len(raw)>=32*(ix+1),'short_observation');value=int.from_bytes(raw[ix*32:(ix+1)*32],'big')
       if spec['type']=='Bool':require(value in [0,1],'invalid_bool');value=bool(value)
       elif spec['type']=='Address160':require(value<2**160,'invalid_address');value='0x'+format(value,'040x')
       execution['registry'][spec['id']+'.'+str(runtime.steps)]={'type':spec['type'],'value':value,'point':runtime.steps}
      execution['observations'].append(copy.deepcopy(result))
   else:
    require(set(args)==({'execution_id','query_id'} if op=='check_formula' else {'execution_id'}),'execution_fields')
    eid=args['execution_id'];require(eid in self.executions,'unknown_execution');execution=self.executions[eid];require(execution['plan']==key,'foreign_execution')
    require(len(execution['transactions'])==len(plan['transactions']),'incomplete_trace')
    # Every declared observer at every deployed point is required for a complete replay/condition record.
    deployed=set()
    for step,tx in enumerate(execution['transactions'],1):
     if tx['function']=='constructor' and tx['status']=='success':deployed.add(tx['instance_id'])
     for spec in plan['observers']:
      if spec['instance_id'] in deployed:require(spec['id']+'.'+str(step) in execution['registry'],'incomplete_observations')
    if op=='check_formula':
     query=reg.get('queries',{}).get(args['query_id']);require(query is not None,'unregistered_query');self.sequence+=1
     if query.get('kind')=='bounded_original_path':
      # Opt-in typed query, frozen with this reachable prefix. No raw calldata,
      # source, SMT text, storage injection or target can arrive over the RPC.
      require(set(query)=={'kind','transaction','symbolic_parameter_index','max_nodes','timeout_seconds'},'bounded_search_query_fields')
      tx=query['transaction'];binding(plan,tx)
      require(set(tx)=={'program_id','instance_id','target','sender','function','arguments','environment','value','gas'},'search_transaction_fields')
      require(tx['sender'] in plan['accounts'] and tx['environment']==execution['runtime'].environment and tx['value']==0 and tx['gas']==12000000,'unsupported_search_context')
      require(0<query['max_nodes']<=64 and 0<query['timeout_seconds']<=180 and len(plan['transactions'])<6,'search_bounds')
      require(all(t['status']=='success' for t in execution['transactions']),'unreachable_search_prefix')
      require(execution['runtime'].usable,'search_requires_open_prefix_world')
      result=self.native.request({'op':'search_transaction','world':execution['runtime'].world,**{k:tx[k] for k in ['program_id','instance_id','target','sender','function','arguments']},**{k:query[k] for k in ['symbolic_parameter_index','max_nodes']},'timeout_seconds':min(query['timeout_seconds'],max(1,int(timeout)-1))},timeout)
      result.update(kind='bounded_original_path',execution_id=eid,plan_ref=self.current,prefix_world=execution['world_records'][-1],scope='original bytecode paths from this concrete reachable prefix; symbolic model limits apply; selected inputs require concrete verification')
     else:
      result=check_formula(query['premise'],query['expression'],execution['registry'],self.root/('solver_'+str(self.sequence)),timeout=min(30,timeout))
      result.update(kind='concrete_trace_condition',execution_id=eid,plan_ref=self.current,scope='conditions of this fixed concrete trace; no symbolic path search')
    else:
     replay=execute_multi(self,plan);other=self.executions[replay['execution_id']]
     result={**replay_comparison(execution,other),'same_engine':True,'deployment_reachable':True,'source_execution_id':eid,'replay':replay,'scope':'ordinary concrete replay only'}
   response={'protocol':PROTOCOL,'request_id':rid,'plan_ref':envelope['plan_ref'],'status':'ok','result':result}
  except (Invalid,TimeoutError,subprocess.TimeoutExpired,KeyError,ValueError,TypeError,OSError) as error:
   if isinstance(error,(TimeoutError,subprocess.TimeoutExpired,OSError)):
    for ex in self.executions.values():ex['runtime'].usable=False
   response={'protocol':PROTOCOL,'request_id':rid,'plan_ref':envelope.get('plan_ref'),'status':'error','error':str(error),'error_class':type(error).__name__,'no_safety_conclusion':True}
  with (self.owner.root/'rpc.jsonl').open('a') as f:f.write(json.dumps({'request':envelope,'response':response,'elapsed_seconds':time.monotonic()-started})+'\n')
  return response
