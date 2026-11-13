import json,pathlib,selectors,subprocess,uuid
from .core import require
from .backend import read_json_line

class ServiceClient:
 def __init__(self,python,script,manifest,stderr,protocol=None):
  self.protocol=protocol
  self.stderr=pathlib.Path(stderr).open('w');self.plan_ref=None
  self.p=subprocess.Popen([str(python),str(script),str(manifest)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.stderr,text=True,bufsize=1)
 def select(self,plan_ref):self.plan_ref=plan_ref
 def raw(self,envelope,timeout=30):
  self.p.stdin.write(json.dumps(envelope)+'\n');self.p.stdin.flush()
  result=read_json_line(self.p,timeout)
  require(result['request_id']==envelope['request_id'] and result['plan_ref']==envelope['plan_ref'],'response_identity_mismatch')
  require(result.get('protocol')==envelope.get('protocol'),'response_protocol_mismatch')
  return result
 def request(self,request,timeout=30):
  e={'request_id':uuid.uuid4().hex,'plan_ref':self.plan_ref,'op':request['op'],'params':{k:v for k,v in request.items() if k!='op'}}
  if self.protocol is not None:e['protocol']=self.protocol
  result=self.raw(e,timeout);require(result['status']=='ok',result.get('error','service_error'));return result['result']
 def close(self):
  if self.p.poll() is None:
   self.p.stdin.close()
   try:self.p.wait(timeout=4)
   except subprocess.TimeoutExpired:self.p.kill();self.p.wait()
  self.stderr.close()
