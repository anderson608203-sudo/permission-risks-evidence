"""Concrete, ABI-only program/instance adapter. No risk or search semantics."""
import copy,json,pathlib
from .core import digest,require
from .deployment import linked_artifact,verify_deployment,unhex
from .environment import validate

def descriptor(bundle,contract,libraries=None):
 return {'source_program_id':bundle['program_id'],'build_id':bundle['build_id'],'contract':contract,'libraries':libraries or {}}

def load_request(entry):
 linked=linked_artifact(entry['contract'],entry['libraries'])
 return {'op':'load_program','program_id':digest(entry),'creation':linked['creation'],'constructor_types':entry['contract']['constructor_types'],'functions':entry['contract']['functions']}

class InstanceRuntime:
 def __init__(self,native,accounts,evidence,timestamp=1000000,environment=None):
  self.native=native;self.root=pathlib.Path(evidence);self.root.mkdir(parents=True,exist_ok=False)
  self.programs={};self.instances={};self.worlds=[];self.steps=0;self.usable=True;self.timestamp=timestamp
  require(type(timestamp)is int and timestamp>=0,'timestamp_range')
  hello=native.request({'op':'hello'});require(hello.get('instance_protocol')=='concrete-instances-v1','instance_protocol_mismatch')
  self.environment=copy.deepcopy(environment)
  if environment is not None:validate(environment);require(hello.get('context_protocol')=='block-time-v1','context_protocol_mismatch')
  created=native.request({'op':'create_world','accounts':sorted(set(accounts)),**({'environment':environment} if environment is not None else {})});self.world=created['world'];self.worlds.append(self.world)
  self.created=created
  if environment is not None:require(created['environment']==environment,'created_environment_mismatch')
  self.record('environment',{'hello':hello,'created':created,'environment':copy.deepcopy(created.get('environment')),'legacy_transaction_timestamp':timestamp if environment is None else None,'scope':'ordinary concrete ABI execution; no fork-conformance or risk claim'})

 def record(self,kind,value):
  with (self.root/'events.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps({'kind':kind,**value},ensure_ascii=False)+'\n')

 def register(self,bundle,contract,libraries=None):
  require(self.usable,'closed_or_unverified_session')
  linked=linked_artifact(contract,libraries)
  entry=descriptor(bundle,contract,libraries)
  key=digest(entry)
  request={'op':'load_program','program_id':key,'creation':linked['creation'],'constructor_types':contract['constructor_types'],'functions':contract['functions']}
  response=self.native.request(request);require(response['loaded']==key,'loaded_program_mismatch')
  self.programs[key]=copy.deepcopy(entry);self.record('program',{'program_id':key,**entry,'linked_artifact':linked,'response':response})
  return key

 def execute(self,program_id,instance_id,sender,function,arguments,target=None,environment=None,value=0,gas=12000000):
  require(self.usable,'closed_or_unverified_session');require(program_id in self.programs,'unregistered_program')
  require(self.steps<6,'transaction_cap');require(isinstance(instance_id,str) and instance_id,'instance_id')
  require(all(isinstance(a,str) for a in arguments),'argument_string_required')
  context=self.environment if environment is None else environment
  if self.environment is not None:validate(context,self.environment)
  request={'op':'execute_top_transaction','world':self.world,'program_id':program_id,'instance_id':instance_id,'sender':sender,'function':function,'arguments':arguments,'timestamp':str(context['timestamp'] if context else self.timestamp),'value':str(value),'gas':gas,**({'environment':context} if context is not None else {})}
  if target is not None:request['target']=target
  try:receipt=self.native.request(request)
  except Exception as error:
   self.usable=False;self.record('execution_error',{'request':request,'error_class':type(error).__name__,'error':str(error),'outcome':'unverified; no implicit retry'});raise
  self.record('transaction',{'request':request,'receipt':receipt})
  self.worlds.append(receipt['world']);self.world=receipt['world'];self.steps+=1
  try:
   if context is not None:
    require(receipt['environment']==context and receipt['pre_environment']==self.environment,'transaction_environment_mismatch');self.environment=copy.deepcopy(context)
   require(receipt['program_id']==program_id and receipt['instance_id']==instance_id and receipt['tx_index']==self.steps,'transaction_binding_mismatch')
   if target is not None:require(receipt['target'].lower()==target.lower(),'transaction_target_mismatch')
   for entry in self.instances.values():
    account=next((a for a in receipt['post'] if a['address'].lower()==entry['target'].lower()),None)
    require(account is not None and unhex(account['runtime'])==unhex(entry['runtime']),'instance_runtime_changed_or_missing')
  except Exception as e:
   self.usable=False;self.record('identity_failure',{'error':str(e)});raise
  return receipt

 def deploy(self,program_id,instance_id,sender,arguments,**options):
  require(instance_id not in self.instances,'instance_already_deployed')
  receipt=self.execute(program_id,instance_id,sender,'constructor',arguments,**options)
  if receipt['status']=='success':
   try:
    descriptor=self.programs[program_id];identity=verify_deployment(descriptor['contract'],receipt,arguments,descriptor['libraries'])
    self.instances[instance_id]={'program_id':program_id,'target':receipt['target'],'runtime':identity['actual_deployed_runtime'],'deployment_identity':identity}
    self.record('deployment_identity',{'instance_id':instance_id,'program_id':program_id,**identity})
   except Exception as e:
    self.usable=False;self.record('identity_failure',{'error':str(e)});raise
  return receipt

 def call(self,instance_id,sender,function,arguments,**options):
  require(instance_id in self.instances,'unknown_instance');instance=self.instances[instance_id]
  require(function!='constructor','call_cannot_deploy')
  return self.execute(instance['program_id'],instance_id,sender,function,arguments,instance['target'],**options)

 def observe(self,instance_id,caller,function,arguments=()):
  require(self.usable,'closed_or_unverified_session');require(instance_id in self.instances,'unknown_instance');instance=self.instances[instance_id]
  request={'op':'observe','world':self.world,'program_id':instance['program_id'],'instance_id':instance_id,'target':instance['target'],'caller':caller,'function':function,'arguments':list(arguments)}
  result=self.native.request(request);self.record('observation',{'request':request,'receipt':result})
  require(result['status']=='observed' and result['world_unchanged'] is True,'observation_failed')
  require(result['world']==self.world and result['program_id']==instance['program_id'] and result['instance_id']==instance_id and result['target'].lower()==instance['target'].lower(),'observation_binding_mismatch')
  if self.environment is not None:require(result['environment']==self.environment,'observation_environment_mismatch')
  return result

 def close(self):
  for world in self.worlds:self.native.request({'op':'close_world','world':world})
  self.record('closed',{'worlds':self.worlds});self.worlds=[];self.usable=False
