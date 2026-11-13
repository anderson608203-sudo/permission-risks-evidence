"""Lazy per-item binding to the existing registered eight-method service."""
import copy,hashlib,json,pathlib
from .core import require,digest,ref
from .multi_service import PROTOCOL,validate_plan
from .service_client import ServiceClient

def freeze_manifest(item,root,name='service_manifest.json'):
    root=pathlib.Path(root).resolve()
    require(pathlib.Path(name).name==name,'manifest_filename')
    plan=validate_plan(copy.deepcopy(item['plan']));query=copy.deepcopy(item['query'])
    rule=query.get('rule') or query.get('rule_id')
    require(rule and query.get('premise') and query.get('expression'),'service_query_fields')
    manifest={'schema':'multi-service-manifest-v1','registrations':[{'plan':plan,'queries':{rule:query}}]}
    data=(json.dumps(manifest,ensure_ascii=False,indent=2)+chr(10)).encode('utf-8')
    root.mkdir(parents=True,exist_ok=True);path=root/name
    if path.exists():require(path.read_bytes()==data,'service_manifest_conflict')
    else:path.write_bytes(data)
    return {'path':str(path),'plan_ref':ref(plan),'query_id':rule,
            'manifest_digest':digest(manifest),'manifest_sha256':hashlib.sha256(data).hexdigest()}

def make_client(root,python,script,manifest,stderr):
    root=pathlib.Path(root).resolve();script=pathlib.Path(script).resolve()
    require(script.parent.parent==root,'worker_method_root_mismatch')
    require(pathlib.Path(manifest).resolve().is_relative_to(root),'worker_manifest_outside_root')
    return ServiceClient(python,script,manifest,stderr,protocol=PROTOCOL)

class BoundClient:
    def __init__(self,item,method_root,service_root,python,script):
        self.item=copy.deepcopy(item);self.method_root=pathlib.Path(method_root).resolve()
        self.root=pathlib.Path(service_root).resolve()/digest({'plan':item['plan'],'query':item['query']})
        require(self.root.is_relative_to(self.method_root),'service_root_outside_method')
        self.python=python;self.script=script;self.client=None;self.selected=False;self.closed=False
        self.receipt={'expected_plan_ref':ref(item['plan']),'status':'not_started','external_process_started':False}
    def save(self):
        self.root.mkdir(parents=True,exist_ok=True)
        (self.root/'binding_receipt.json').write_text(json.dumps(self.receipt,indent=2),encoding='utf-8')
    def select(self,plan_ref):
        require(not self.closed,'service_client_closed')
        require(plan_ref==ref(self.item['plan']),'service_plan_ref_mismatch')
        if self.client is None:
            self.receipt.update(freeze_manifest(self.item,self.root));self.receipt['status']='manifest_frozen';self.save()
            try:
                self.client=make_client(self.method_root,self.python,self.script,self.receipt['path'],self.root/'client.stderr')
            except Exception as error:
                self.receipt.update(status='start_failed',error_class=type(error).__name__,error=str(error));self.save();raise
            self.receipt.update(status='client_started',external_process_started=True);self.save()
        self.client.select(plan_ref);self.selected=True
    def request(self,value,**kwargs):
        require(self.selected and not self.closed,'service_plan_not_selected')
        return self.client.request(value,**kwargs)
    def close(self):
        if self.closed:return
        self.closed=True
        if self.client is None:return
        try:self.client.close()
        except Exception as error:
            self.receipt.update(status='close_failed',error_class=type(error).__name__,error=str(error));self.save();raise
        self.receipt['status']='closed';self.save()
