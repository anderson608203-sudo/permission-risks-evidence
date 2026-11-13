"""Restricted host adapter over a persistent native hevm worker and real Z3."""
import json,pathlib,selectors,subprocess,time,os
from .core import require,expression,Invalid
Z3='/nix/store/5ic22qpb2f7idlspzimq4ddl1y1x5nsf-z3-4.15.2/bin/z3'

def read_json_line(process,timeout,max_bytes=16*1024*1024):
 deadline=time.monotonic()+timeout;data=bytearray();s=selectors.DefaultSelector();s.register(process.stdout,selectors.EVENT_READ)
 try:
  while True:
   remaining=deadline-time.monotonic()
   if remaining<=0 or not s.select(remaining):process.kill();raise TimeoutError('json_line_deadline')
   chunk=os.read(process.stdout.fileno(),65536)
   require(bool(chunk),'worker_eof');data.extend(chunk);require(len(data)<=max_bytes,'response_size_limit')
   if b'\n' in data:
    line,tail=bytes(data).split(b'\n',1);require(not tail.strip(),'unsolicited_extra_response');return json.loads(line)
 finally:s.close()

class Native:
 def __init__(self,binary,log):
  self.log=pathlib.Path(log);self.log.parent.mkdir(parents=True,exist_ok=True)
  self.stderr=self.log.with_suffix('.stderr').open('w')
  self.p=subprocess.Popen([str(binary),'+RTS','-N1','-M8g','-RTS'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.stderr,text=True,bufsize=1)
 def request(self,request,timeout=30):
  started=time.monotonic()
  self.p.stdin.write(json.dumps(request)+'\n');self.p.stdin.flush()
  response=read_json_line(self.p,timeout)
  with self.log.open('a') as f:f.write(json.dumps({'request':request,'response':response,'elapsed_seconds':time.monotonic()-started})+'\n')
  require('error' not in response,'native_error:'+response.get('error',''))
  return response
 def close(self):
  if self.p.poll() is None:
   self.p.stdin.close()
   try:self.p.wait(timeout=3)
   except subprocess.TimeoutExpired:self.p.kill();self.p.wait()
  self.stderr.close()

def smt_ground(e,registry):
 typ,value=expression(e,registry)
 require(value is not None,'unbound_formula')
 # Ground finite-domain queries retain arithmetic in the submitted SMT formula.
 if e['node']=='op':
  op=e['operator'];a=[smt_ground(x,registry) for x in e['args']]
  maps={'and':'and','or':'or','not':'not','eq':'=','ne':'distinct','int_lt':'<','int_le':'<=','int_gt':'>','int_ge':'>=','delta':'-','ite':'ite'}
  if op in maps:return '('+maps[op]+' '+' '.join(a)+')'
 if typ=='Bool':return 'true' if value else 'false'
 if typ=='Address160':return str(int(value,16))
 if typ=='IntDelta' or typ.startswith('BV'):
  return str(value) if value>=0 else '(- '+str(-value)+')'
 raise Invalid('unsupported_solver_value')

def check_formula(premise,query,registry,evidence_dir,timeout=30):
 require(0<timeout<=30,'solver_timeout_limit')
 evidence_dir=pathlib.Path(evidence_dir);evidence_dir.mkdir(parents=True,exist_ok=False)
 results={};deadline=time.monotonic()+timeout
 for label,e in [('premise',premise),('query',query)]:
  remaining=deadline-time.monotonic();require(remaining>0,'solver_deadline')
  require(expression(e,registry)[0]=='Bool','formula_must_bool')
  formula=smt_ground(e,registry)
  if label=='query':formula='(and '+smt_ground(premise,registry)+' '+formula+')'
  text='(set-option :timeout '+str(max(1,int(remaining*1000)))+')\n(set-logic ALL)\n(assert '+formula+')\n(check-sat)\n'
  (evidence_dir/(label+'.smt.txt')).write_text(text)
  p=subprocess.run([Z3,'-in'],input=text,text=True,capture_output=True,timeout=remaining)
  (evidence_dir/(label+'.stdout')).write_text(p.stdout);(evidence_dir/(label+'.stderr')).write_text(p.stderr)
  results[label]=p.stdout.strip() if p.returncode==0 and p.stdout.strip() in ['sat','unsat','unknown'] else 'unknown'
  if label=='premise' and results[label]!='sat':break
 return results

def program_request(bundle,contract):
 return {'op':'load_program','program_id':bundle['program_id'],'creation':contract['creation'],'constructor_types':contract['constructor_types'],'functions':contract['functions']}

def observe(native,bundle,world,target,spec,caller):
 result=native.request({'op':'observe','world':world,'program_id':bundle['program_id'],'target':target,'caller':caller,'function':spec['function'],'arguments':spec['arguments']})
 require(result['status']=='observed','getter_failed')
 raw=bytes.fromhex(result['output'][2:]);index=spec.get('output_index',0)
 require(len(raw)>=(index+1)*32,'short_getter_output')
 value=int.from_bytes(raw[index*32:(index+1)*32],'big')
 if spec['type']=='Bool':require(value in [0,1],'invalid_bool');value=bool(value)
 elif spec['type']=='Address160':value='0x'+format(value,'040x')
 return value,result

def execute_plan(native,bundle,contract,plan,out):
 out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=False)
 native.request(program_request(bundle,contract))
 actors=plan['actors'];require(all(x['kind']=='eoa' for x in actors.values()),'contract_actor_requires_outer_tx')
 created=native.request({'op':'create_world','accounts':sorted(set(x['address'] for x in actors.values())|{'0x00000000000000000000000000000000000000d4'})})
 w=created['world'];execution_id=created.get('execution_id',w);worlds=[w]
 require(len(plan['transactions'])<=6,'transaction_cap')
 target=None;receipts=[];registry={};observations=[]
 for i,tx in enumerate(plan['transactions'],1):
  sender=actors[tx['sender']]['address']
  args=[actors[v[1:]]['address'] if isinstance(v,str) and v.startswith('$') else str(v) for v in tx['arguments']]
  request={'op':'execute_top_transaction','world':w,'program_id':bundle['program_id'],'sender':sender,'function':tx['function'],'arguments':args,'timestamp':str(tx.get('timestamp',1000000)),'value':str(tx.get('value',0)),'gas':tx.get('gas',12000000)}
  if target:request['target']=target
  receipt=native.request(request);receipt['sender_control']=actors[tx['sender']]['control'];receipt['declared_environment_prefix']=tx.get('environment_prefix',False)
  account_before=next(a for a in receipt['pre'] if a['address'].lower()==sender.lower())
  receipt['sender_nonce_before']=account_before['nonce']
  receipts.append(receipt);w=receipt['world'];target=receipt['target']
  worlds.append(w)
  registry['tx'+str(i)+'.success']={'type':'Bool','value':receipt['status']=='success','point':i}
  if i==1 and receipt['status']=='success':
   from .deployment import verify_runtime
   receipt['deployment_identity']=verify_runtime(contract,receipt['output'])
  for spec in plan.get('observers',[]):
   s=dict(spec);s['arguments']=[actors[v[1:]]['address'] if isinstance(v,str) and v.startswith('$') else str(v) for v in s['arguments']]
   if receipt['status']=='success' or i>1:
    value,r=observe(native,bundle,w,target,s,actors[spec.get('caller','A')]['address'])
    oid=spec['id']+'.'+str(i);registry[oid]={'type':spec['type'],'value':value,'point':i};observations.append({'id':oid,'value':str(value) if type(value)is int else value,'binding':s,'receipt':r})
  if receipt['status']!='success' and tx.get('must_succeed',False):break
 for world in worlds:native.request({'op':'close_world','world':world})
 result={'plan':plan,'execution_id':execution_id,'transactions':receipts,'observations':observations,'registry':registry,'scope':'one_plan','address_domain':'finite_declared'}
 (out/'execution.json').write_text(json.dumps(result,indent=2))
 return result
