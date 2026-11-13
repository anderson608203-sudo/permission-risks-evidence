"""Eight-method bounded service. Public JSON requests reference frozen plans only."""
import json,pathlib,time,uuid,subprocess
from .backend import Native,execute_plan,check_formula
from .core import *

METHODS=('hello','load_program','create_world','execute_top_transaction','observe','check_formula','materialize_witness','close_world')

class Service:
 def __init__(self,binary,root,registrations):
  self.root=pathlib.Path(root);self.root.mkdir(parents=True,exist_ok=True)
  self.native=Native(binary,self.root/'native.jsonl');self.registrations=registrations
  self.seen=set();self.worlds={};self.closed=set();self.executions={};self.deadlines={};self.current=None;self.counter=0
 def select(self,plan_ref):
  key=plan_ref['sha256'];require(key in self.registrations,'unregistered_plan');require(ref(self.registrations[key]['candidate']['plan'])==plan_ref,'stale_plan_ref')
  self.current=plan_ref;self.deadlines.setdefault(key,time.monotonic()+180)
 def request(self,request,timeout=30):
  envelope={'request_id':uuid.uuid4().hex,'plan_ref':self.current,'op':request['op'],'params':{k:v for k,v in request.items() if k!='op'}}
  response=self.handle(envelope,timeout)
  require(response['status']=='ok',response.get('error','service_error'))
  return response['result']
 def handle(self,envelope,timeout=30):
  # New shapes are accepted only through explicit protocol negotiation. Legacy plans retain v2.
  from .multi_service import MultiService,PROTOCOL,PLAN_SCHEMA
  registration=self.registrations.get((envelope.get('plan_ref') or {}).get('sha256'),{}) if hasattr(self,'registrations') else {}
  if envelope.get('protocol')==PROTOCOL or registration.get('candidate',{}).get('plan',{}).get('schema')==PLAN_SCHEMA:
   if not hasattr(self,'multi'):self.multi=MultiService(self)
   return self.multi.handle(envelope,timeout)
  start=time.monotonic();rid=envelope.get('request_id');op=envelope.get('op')
  try:
   require(set(envelope)=={'request_id','plan_ref','op','params'},'envelope_fields')
   require(isinstance(rid,str) and rid and rid not in self.seen,'request_identity_reuse');self.seen.add(rid)
   require(op in METHODS,'unknown_operation')
   self.select(envelope['plan_ref']);key=self.current['sha256'];reg=self.registrations[key];c=reg['candidate'];plan=c['plan'];bundle=reg['bundle'];contract=reg['contract'];args=envelope['params']
   remaining=self.deadlines[key]-time.monotonic();require(remaining>0,'candidate_timeout');timeout=min(timeout,remaining)
   if op=='hello':
    require(not args,'hello_arguments');result={**self.native.request({'op':'hello'},timeout),'protocol':'pr-next-joint-eight-methods-v2','methods':list(METHODS),'plan_ref':self.current,'unrestricted_paths':False}
   elif op=='load_program':
    from .backend import program_request
    require(args=={k:v for k,v in program_request(bundle,contract).items() if k!='op'},'program_identity_mismatch')
    result=self.native.request({'op':op,**args},timeout)
   elif op=='create_world':
    expected=sorted(set(x['address'] for x in plan['actors'].values())|{'0x00000000000000000000000000000000000000d4'})
    require(args=={'accounts':expected},'undeclared_initial_accounts')
    result=self.native.request({'op':op,**args},timeout);eid=result['world'];result['execution_id']=eid
    self.worlds[eid]={'plan':key,'step':0,'execution_id':eid,'target':None}
    self.executions[eid]={'plan':key,'registry':{},'transactions':[],'current_world':eid}
   elif op in ['execute_top_transaction','observe','close_world']:
    world=args.get('world');require(world in self.worlds and world not in self.closed,'closed_or_unknown_world');context=self.worlds[world]
    require(context['plan']==key,'cross_plan_world');eid=context['execution_id'];execution=self.executions[eid]
    if op=='execute_top_transaction':
     require(execution['current_world']==world,'nonlinear_or_reused_world')
     step=context['step']+1;require(step<=len(plan['transactions']),'plan_exhausted');tx=plan['transactions'][step-1]
     expected={'world':world,'program_id':bundle['program_id'],'sender':plan['actors'][tx['sender']]['address'],'function':tx['function'],'arguments':[plan['actors'][v[1:]]['address'] if v.startswith('$') else v for v in tx['arguments']],'timestamp':str(tx.get('timestamp',1000000)),'value':str(tx.get('value',0)),'gas':tx.get('gas',12000000)}
     if context['target']:expected['target']=context['target']
     require(args==expected,'transaction_not_in_frozen_plan')
     result=self.native.request({'op':op,**args},timeout)
     execution['current_world']=result['world']
     self.worlds[result['world']]={'plan':key,'step':step,'execution_id':eid,'target':result['target']}
     execution['transactions'].append(result);execution['registry']['tx'+str(step)+'.success']={'type':'Bool','value':result['status']=='success','point':step}
    elif op=='observe':
     matches=[]
     for spec in plan['observers']:
      expected={'world':world,'program_id':bundle['program_id'],'target':context['target'],'caller':plan['actors'][spec.get('caller','A')]['address'],'function':spec['function'],'arguments':[plan['actors'][v[1:]]['address'] if v.startswith('$') else v for v in spec['arguments']]}
      if args==expected:matches.append(spec)
     require(matches,'observer_not_in_frozen_plan');result=self.native.request({'op':op,**args},timeout)
     require(result['status']=='observed','observation_failed')
     for spec in matches:
      raw=bytes.fromhex(result['output'][2:]);ix=spec.get('output_index',0);require(len(raw)>=32*(ix+1),'short_observation')
      value=int.from_bytes(raw[32*ix:32*(ix+1)],'big')
      if spec['type']=='Bool':require(value in [0,1],'invalid_bool');value=bool(value)
      elif spec['type']=='Address160':require(value<2**160,'invalid_address');value='0x'+format(value,'040x')
      execution['registry'][spec['id']+'.'+str(context['step'])]={'type':spec['type'],'value':value,'point':context['step']}
    else:
     require(set(args)=={'world'},'close_fields');result=self.native.request({'op':op,**args},timeout);self.closed.add(world)
   elif op=='check_formula':
    require(set(args)=={'query_id','execution_id'},'formula_fields');eid=args['execution_id'];require(eid in self.executions and self.executions[eid]['plan']==key,'foreign_execution')
    require(len(self.executions[eid]['transactions'])==len(plan['transactions']),'incomplete_trace')
    query=reg['queries'].get(args['query_id']);require(query is not None,'unregistered_query')
    self.counter+=1;result=check_formula(query['premise'],query['expression'],self.executions[eid]['registry'],self.root/('solver_'+str(self.counter)),timeout=min(30,timeout))
    result.update(query_id=args['query_id'],plan_ref=self.current,execution_id=eid,scope='conditions of this fixed concrete trace')
   else:
    require(set(args)=={'execution_id'},'witness_fields');eid=args['execution_id'];require(eid in self.executions and self.executions[eid]['plan']==key,'foreign_witness')
    original=self.executions[eid];self.counter+=1
    replay=execute_plan(self,bundle,contract,plan,self.root/('replay_'+str(self.counter)))
    equal=[(x['status'],x['output'],x['post']) for x in original['transactions']]==[(x['status'],x['output'],x['post']) for x in replay['transactions']]
    require(original['registry']==replay['registry'],'replay_observation_mismatch')
    result={'equal':equal,'replay':replay,'source_execution_id':eid,'same_engine':True,'deployment_reachable':True}
   response={'request_id':rid,'plan_ref':envelope['plan_ref'],'status':'ok','result':result}
  except (Invalid,TimeoutError,subprocess.TimeoutExpired,KeyError,ValueError,TypeError) as e:
   response={'request_id':rid,'plan_ref':envelope.get('plan_ref'),'status':'error','error':str(e),'error_class':type(e).__name__,'no_safety_conclusion':True}
  with (self.root/'rpc.jsonl').open('a') as f:f.write(json.dumps({'request':envelope,'response':response,'elapsed_seconds':time.monotonic()-start})+'\n')
  return response
 def close(self):self.native.close()
