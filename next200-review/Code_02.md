# 源码文本 · 2

## runtime/live_client.py

原文件 SHA-256 `1a00588b166eab4a4b5cd49e3805a6a5ad8fc39c291f88f55a9ef5793e86defa`

````python
"""Pinned HTTP contract, durable raw replies and shared count/usage ledger."""
from pathlib import Path
import os,time,json,urllib.request,urllib.error,re,html.parser
from common import R,SOURCE,ROUND,read,write,digest,sha,wire,safe_error
from ledger import Ledger
from reference_counter import Counter
MODELS={'deepseek-flash','deepseek-v4.1-flash-1017','DeepSeek-V4.1-Flash-1017'}

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None

def http_sender(body,timeout):
    req=urllib.request.Request('https://api.deepseek.com/chat/completions',data=json.dumps(body,ensure_ascii=False).encode(),
        headers={'Content-Type':'application/json','Authorization':'Bearer '+os.environ['DEEPSEEK_API_KEY']},method='POST')
    try:
        with urllib.request.build_opener(NoRedirect()).open(req,timeout=timeout) as response:return response.read()
    except urllib.error.HTTPError as e:
        # Error bodies are retained by the caller too, without saving request headers.
        e.saved_body=e.read();raise

class PriceTable(html.parser.HTMLParser):
    def __init__(self):super().__init__();self.rows=[];self.row=None;self.cell=None
    def handle_starttag(self,tag,attrs):
        if tag=='tr':self.row=[]
        if tag in ('td','th'):self.cell=[]
    def handle_data(self,data):
        if self.cell is not None:self.cell.append(data)
    def handle_endtag(self,tag):
        if tag in ('td','th') and self.cell is not None:
            if self.row is not None:self.row.append(''.join(self.cell))
            self.cell=None
        if tag=='tr' and self.row is not None:self.rows.append(self.row);self.row=None

def parse_prices(raw):
    text=raw.decode('utf-8');parser=PriceTable();parser.feed(text);values=[]
    for row in parser.rows:
        prices=[float(v) for cell in row for v in re.findall(r'\$\s*(\d+(?:\.\d+)?)',cell)]
        if prices:values.append(prices[0])
    if 'DeepSeek-V4.1-Flash-1017' not in text or values[:6]!=[.003,.006,.15,.3,.6,1.2]:
        raise ValueError('public_model_or_price_table_changed_no_paid_dispatch')
    return {'peak':{'hit':.006,'miss':.3,'output':1.2},'off_peak':{'hit':.003,'miss':.15,'output':.6},
        'flash_price_rows':values[:6],'parsed_from_actual_public_HTML':True}

def verify_service(out):
    out=Path(out);opener=urllib.request.build_opener(NoRedirect())
    with opener.open('https://api-docs.deepseek.com/quick_start/pricing/',timeout=30) as r:pricing=r.read()
    out.mkdir(parents=True,exist_ok=True);(out/'pricing_public.html').write_bytes(pricing)
    prices=parse_prices(pricing)
    req=urllib.request.Request('https://api.deepseek.com/models',headers={'Authorization':'Bearer '+os.environ['DEEPSEEK_API_KEY']})
    with opener.open(req,timeout=30) as r:raw=r.read()
    (out/'authenticated_models.json').write_bytes(raw)
    model=next((x for x in json.loads(raw)['data'] if x['id']=='deepseek-flash'),None)
    if (not model or model.get('name') not in ('DeepSeek-V4.1-Flash','DeepSeek-V4.1-Flash-1017') or
        model.get('context_window')!=1048576 or model.get('max_output_tokens',0)<32768 or
        'high' not in model.get('effort',{}).get('supported_levels',[])):
        raise ValueError('authenticated_model_identity_or_capacity_changed')
    evidence={'epoch':time.time(),'model':model,'prices':prices,'LLM_generation_requests':0,
        'pricing_sha256':sha(out/'pricing_public.html'),'metadata_sha256':sha(out/'authenticated_models.json')}
    write(out/'SERVICE_ACTUAL.json',evidence);return evidence

def priced_usage(usage):
    if not isinstance(usage,dict):raise ValueError('provider_usage_missing')
    for k in ('prompt_tokens','completion_tokens'):
        if type(usage.get(k))is not int or usage[k]<0:raise ValueError('provider_usage_invalid:'+k)
    prompt=usage['prompt_tokens'];output=usage['completion_tokens']
    cache_known='prompt_cache_hit_tokens' in usage or 'prompt_cache_miss_tokens' in usage
    hit=usage.get('prompt_cache_hit_tokens',prompt-usage['prompt_cache_miss_tokens'] if 'prompt_cache_miss_tokens' in usage else 0)
    miss=usage.get('prompt_cache_miss_tokens',prompt-hit)
    if any(type(n)is not int or n<0 for n in (hit,miss)) or hit+miss!=prompt:raise ValueError('provider_cache_usage_invalid')
    upper=(hit*.006+miss*.3+output*1.2)/1e6
    # Completion includes reasoning; never add reasoning_tokens a second time.
    lower=upper/2 if cache_known else (prompt*.003+output*.6)/1e6
    return upper,lower

class Client:
    def __init__(self,member,program_identity,run,package=R,*,sender=None,simulated=False):
        self.case_id=member;self.program_identity=program_identity;self.run=Path(run);self.package=Path(package)
        self.simulated=simulated;self.index=0;self.sender=sender or http_sender
        if simulated and sender is None:raise ValueError('explicit_zero_call_sender_required')
        self.ledger=Ledger(self.run/'requests.sqlite');self.grant=self.ledger.meta('grant')
        if not simulated:
            g=read(self.run/'AUTHORIZATION.json')
            if not g.get('authorized') or g.get('round')!=ROUND or g!=self.grant:raise ValueError('fresh_specific_grant_required')
            if g['package_manifest_sha256']!=sha(self.package/'MANIFEST.json'):raise ValueError('authorized_package_changed')
            service=read(self.run/'service/SERVICE_ACTUAL.json')
            if time.time()-service['epoch']>86400:raise ValueError('service_price_identity_record_expired')
        self.live_authorized=not simulated
        initial=self.package/'messages'/member/'initial_request.json'
        if initial.exists() and read(initial).get('host_identity')!=program_identity:
            raise ValueError('frozen_host_program_identity_changed_no_send')
        self.counter=Counter(os.environ.get('SI_TOKENIZER_ROOT') or read(self.run/'TOKENIZER_ROOT.json')['path'])
    def attempt_record(self,index):
        row=self.ledger.row(self.case_id,index)
        if not row:return {'actual_model_submissions':0,'state':'not_dispatched'}
        return {'actual_model_submissions':0 if row['simulated'] else 1,'state':row['state'],
            'submitted_epoch':row['submitted'],'usage':json.loads(row['usage']) if row['usage'] else None,
            'cost_usd_upper':row['upper_usd'],'cost_usd_lower':row['lower_usd'],
            'simulated':bool(row['simulated']),'cost_unknown':row['state'] in ('sent','unknown'),
            'possibly_submitted_not_blindly_retried':True}
    def accounting(self):return self.ledger.snapshot(self.case_id)
    def call(self,messages,tag,**parameters):
        index=self.index;self.index+=1
        if index not in (0,1) or tag!=('semantic_initial' if index==0 else 'semantic_feedback'):raise ValueError('attempt_or_phase_contract')
        if parameters!={'max_tokens':32768,'thinking':True,'reasoning_effort':'high','timeout':1800}:raise ValueError('frozen_request_parameters')
        if len(messages)!=2:raise ValueError('frozen_two_message_contract')
        if index==0 and (self.package/'messages'/self.case_id/'initial_request.json').exists():
            expected=read(self.package/'messages'/self.case_id/'initial_request.json')
            if digest(messages)!=expected['manifest']['messages_sha256']:raise ValueError('frozen_initial_message_changed_no_send')
        count=self.counter.count(messages)
        if count>32768:raise ValueError('capacity_exceeded_no_truncation_no_send')
        body=wire(messages);body_sha=digest(body);out=self.run/'requests'/self.case_id/str(index);out.mkdir(parents=True,exist_ok=True)
        existing=self.ledger.row(self.case_id,index)
        if existing:
            if existing['body_sha']!=body_sha:raise ValueError('saved_request_identity_changed')
            if existing['state']=='settled' and (out/'receipt.json').exists() and (out/'raw_http.json').exists():
                receipt=read(out/'receipt.json')
                if receipt['program_identity']!=self.program_identity:raise ValueError('saved_program_identity_changed')
                receipt={**receipt,'replayed_from_saved_response':True}
                response=read(out/'raw_http.json')
                return response['choices'][0]['message']['content'],receipt
            raise ValueError('unknown_or_inflight_request_preserved_no_resend')
        write(out/'intent.json',{'body':body,'body_sha256':body_sha,'messages_sha256':digest(messages),
            'host_program_identity':self.program_identity,'offline_input_tokens':count,'simulated':self.simulated})
        self.ledger.dispatch(self.case_id,index,body_sha,count,self.simulated)
        raw=None
        try:
            raw=self.sender(body,max(.001,min(1800,self.grant['deadline_epoch']-time.time())))
            (out/'raw_http.body').write_bytes(raw)
            response=json.loads(raw);write(out/'raw_http.json',response)
            if response.get('model') not in MODELS:raise ValueError('response_model_changed')
            upper,lower=priced_usage(response.get('usage'))
            usage=response['usage'];halt=None
            if usage['prompt_tokens']!=count:halt='provider_input_token_count_mismatch'
            if usage['prompt_tokens']>32768 or usage['completion_tokens']>32768:halt='provider_capacity_contract_mismatch'
            self.ledger.settle(self.case_id,index,usage,upper,lower,response['model'],halt)
            content=response['choices'][0]['message']['content']
            if not isinstance(content,str):raise ValueError('response_content_not_text')
            receipt={'case_id':self.case_id,'program_identity':self.program_identity,'call_index':index,
                'messages_sha256':digest(messages),'request_sha256':body_sha,'response_sha256':digest(content),
                'simulated':self.simulated,'actual_model_submissions':0 if self.simulated else 1,
                'source':'explicit zero-call live-client wiring' if self.simulated else 'actual DeepSeek HTTP response',
                'model':response['model'],'usage':usage,'cost_usd':None,'cost_usd_upper':upper,'cost_usd_lower':lower,
                'cost_basis':'actual usage; frozen public peak upper/off-peak lower; not supplier invoice',
                'finish_reason':response['choices'][0].get('finish_reason'),'received_epoch':time.time(),
                'authenticated_service_identity_file':None if self.simulated else 'service/SERVICE_ACTUAL.json',
                'authenticated_service_identity_sha256':None if self.simulated else sha(self.run/'service/SERVICE_ACTUAL.json'),
                'replayed_from_saved_response':False,'raw_http_sha256':sha(out/'raw_http.body')}
            write(out/'receipt.json',receipt);return content,receipt
        except BaseException as error:
            if raw is None and hasattr(error,'saved_body'):(out/'http_error.body').write_bytes(error.saved_body)
            state=self.ledger.row(self.case_id,index)
            if state and state['state']!='settled':self.ledger.unknown(self.case_id,index,safe_error(error))
            network_unknown=raw is None and isinstance(error,(TimeoutError,ConnectionError,urllib.error.URLError)) and not isinstance(error,urllib.error.HTTPError)
            if not network_unknown and (not state or state['state']!='settled'):self.ledger.halt('service_or_cost_contract:'+safe_error(error))
            write(out/'error.json',{'error':safe_error(error),'epoch':time.time(),
                'simulated':self.simulated,'accounting':self.attempt_record(index)})
            raise

````

## runtime/start.py

原文件 SHA-256 `26924ea07da77538ae42b4af027d34f7c217cebac1c0ff51d5dd2f403641dd31`

````python
"""Chat-authorized, user-started Full200; reuse environment, detached supervisor."""
from pathlib import Path
import os,sys,json,time,subprocess,hashlib,traceback,getpass,shutil
R=Path(__file__).resolve().parents[1];OUT=R/'run'
BOOT_EPOCH=float(os.environ.get('SI_PREPARATION_START_EPOCH',time.time()))
sys.dont_write_bytecode=True
if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
def read(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_name(p.name+'.tmp')
 tmp.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');os.replace(tmp,p)

def approval():
 v=read(R/'CHAT_APPROVAL.json')
 if (v.get('authorized') is not True or v.get('round')!='permission-risks-next-revision-full200-20261112-r1'
  or v.get('limits')!=read(R/'PLAN.json')['limits']
  or v.get('group')!='Full_only' or v.get('source')!='explicit_user_current_chat'
  or v.get('implementation_sha256')!=read(R/'IDENTITY.json')['method_sha256']
  or v.get('package_manifest_sha256')!=sha(R/'MANIFEST.json')):
  raise ValueError('specific_chat_approval_or_package_identity')
 return v

def view(offset=None):
 log=OUT/'progress.log';offset=log.stat().st_size if offset is None and log.exists() else offset or 0
 if (OUT/'STATUS.json').exists():print(json.dumps(read(OUT/'STATUS.json'),ensure_ascii=False),flush=True)
 print('每20秒显示进度；Ctrl+C只退出日志，后台继续。',flush=True)
 try:
  while True:
   if log.exists():
    with log.open('rb') as f:f.seek(offset);data=f.read();offset=f.tell()
    if data:print(data.decode('utf-8',errors='replace'),end='',flush=True)
   if (OUT/'ENDED.json').exists():
    e=read(OUT/'ENDED.json');print('运行结束：'+e['reason']+'；结果目录 '+str(OUT),flush=True);return
   time.sleep(.3)
 except KeyboardInterrupt:print('\n已退出显示，未停止后台。',flush=True)

def interpreter():
 if '--python-ready' in sys.argv:return
 choices=read(R/'PLAN.json')['interpreter_candidates']+[sys.executable]
 check="import sys;assert sys.version_info>=(3,11);from importlib.metadata import version;from Crypto.Hash import keccak;from eth_keys.datatypes import Signature;import z3,tokenizers;assert [version(p) for p in ('z3-solver','tokenizers','pycryptodome','eth-keys')]==['4.15.3.0','0.22.2','3.24.1','0.7.0'];print(sys.executable)"
 errors=[]
 for name in dict.fromkeys(choices):
  if not Path(name).is_file():continue
  p=subprocess.run([name,'-B','-c',check],capture_output=True,text=True,timeout=30)
  if p.returncode==0:
   os.execve(name,[name,'-B',str(Path(__file__).resolve()),*sys.argv[1:],'--python-ready'],
    dict(os.environ,PYTHONIOENCODING='utf-8',SI_PREPARATION_START_EPOCH=str(BOOT_EPOCH)))
  errors.append({'python':name,'error':p.stderr[-1200:]})
 save(OUT/'ENVIRONMENT_STOP.json',{'checked_existing':errors,'installed_anything':False})
 raise ValueError('existing_environment_missing_dependency_no_install')

def preserve(name):
 p=OUT/name
 if p.exists():
  d=OUT/'previous_control_records';d.mkdir(exist_ok=True)
  shutil.copy2(p,d/(str(time.time_ns())+'_'+name.replace('/','_')))

def launch(resume=False):
 import fcntl
 OUT.mkdir(exist_ok=True)
 lock=(OUT/'START_LOCK').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 checklock=(OUT/'SUPERVISOR_LOCK').open('a')
 try:fcntl.flock(checklock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 except BlockingIOError:
  print('本批后台仍在运行；自动进入进度显示，不重复启动。',flush=True);view();return
 finally:checklock.close()
 for item in read(R/'MANIFEST.json')['files']:
  p=R/item['path']
  if not p.is_file() or sha(p)!=item['sha256']:raise ValueError('package_file_identity:'+item['path'])
 approved=approval()
 if not resume and (OUT/'AUTHORIZATION.json').exists():
  print('本批已有运行记录；请用--follow查看，异常恢复使用--resume。',flush=True);return
 sys.path.insert(0,str(R/'runtime'))
 from input_links import source_identity,prepare_links,tokenizer
 from ledger import Ledger
 from live_client import verify_service
 source=source_identity();jobs=prepare_links();assets=tokenizer();save(OUT/'TOKENIZER_ROOT.json',assets)
 # These imports catch packaging/actual-adapter errors before any paid request.
 from pr_next_joint.investigation.cli import run
 from live_client import Client
 assert callable(run) and callable(Client.call)
 if resume:
  if not (OUT/'AUTHORIZATION.json').exists():raise ValueError('no_round_to_resume')
  grant=read(OUT/'AUTHORIZATION.json')
  if grant['chat_approval_sha256']!=sha(R/'CHAT_APPROVAL.json'):raise ValueError('original_chat_approval_changed')
  if (OUT/'ENDED.json').exists() and read(OUT/'ENDED.json')['reason']=='normal_completion':
   print('本批正常结束，保留已有结果，不追加请求；目录 '+str(OUT),flush=True);return
  if time.time()>=grant['deadline_epoch']:raise ValueError('original_full_deadline_expired')
  ledger=Ledger(OUT/'requests.sqlite');ledger.recover();ledger.resume_user_stop()
  if ledger.meta('halt'):raise ValueError('preserved_contract_halt_requires_review:'+str(ledger.meta('halt')))
 prepfile=OUT/'PREPARATION.json'
 prep=read(prepfile) if prepfile.exists() else {
  'used_seconds':read(R/'PLAN.json')['prep_already_used_seconds']+read(R/'PLAN.json').get('upload_seconds_ceiling',0),
  'initial_time_basis':'batch-specific instance setup time; manual upload separate, no prior inventory time attributed','runs':[]}
 if prep['used_seconds']>=1200:raise ValueError('preparation_allowance_exhausted')
 prep_deadline=BOOT_EPOCH+max(0,1200-prep['used_seconds'])
 def remaining_prep():
  if time.time()>=prep_deadline:raise ValueError('cumulative_preparation_deadline')
 try:
  remaining_prep()
  key=os.environ.get('DEEPSEEK_API_KEY')
  if not key:
   if not sys.stdin.isatty():raise ValueError('API_key_needs_interactive_terminal_or_environment')
   key=getpass.getpass('DeepSeek API key（不回显、不保存）：')
  if not key.strip():raise ValueError('empty_API_key')
  os.environ['DEEPSEEK_API_KEY']=key;remaining_prep()
  if resume and (OUT/'service/SERVICE_ACTUAL.json').exists() and grant['deadline_epoch']-read(OUT/'service/SERVICE_ACTUAL.json')['epoch']<=86400:
   service=read(OUT/'service/SERVICE_ACTUAL.json')
  else:
   print('核对既定模型、价格和容量；本步骤不生成模型回答。',flush=True)
   if resume and (OUT/'service/SERVICE_ACTUAL.json').exists():
    for prior in (OUT/'service').iterdir():
     if prior.is_file():preserve('service/'+prior.name)
   verify_service(OUT/'service');service=read(OUT/'service/SERVICE_ACTUAL.json')
  remaining_prep()
 finally:
  used=max(0,time.time()-BOOT_EPOCH);prep['used_seconds']+=used
  prep['runs'].append({'start_epoch':BOOT_EPOCH,'end_epoch':time.time(),'seconds':used,'resume':resume})
  save(prepfile,prep)
 if not resume:
  now=time.time();ids=read(R/'PLAN.json')['execution_order']
  grant={'round':'permission-risks-next-revision-full200-20261112-r1','authorized':True,'group':'Full_only','members':ids,
   'max_requests':approved['limits']['requests'],'per_member_max':approved['limits']['per_member'],'max_usd':approved['limits']['usd'],'wall_seconds':approved['limits']['Full_seconds'],
   'start_epoch':now,'deadline_epoch':min(now+approved['limits']['Full_seconds'],service['epoch']+86400),'input_root':str(R),
   'package_manifest_sha256':sha(R/'MANIFEST.json'),'source':'explicit user approval in current chat',
   'chat_approval_sha256':sha(R/'CHAT_APPROVAL.json'),'implementation_sha256':approved['implementation_sha256'],
   'history':'HISTORY.json; old unknown and billed-use records not reset or spent as new allowance'}
  assert grant['max_requests']*.049152<=grant['max_usd']
  save(OUT/'AUTHORIZATION.json',grant);Ledger(OUT/'requests.sqlite').initialize(grant)
 identity={'source':source,'runtime':{p.name:sha(p) for p in (R/'runtime').glob('*.py')},
  'inputs_sha256':sha(R/'INPUTS.json'),'jobs_sha256':sha(OUT/'JOBS.json'),'config_sha256':sha(R/'METHOD_CONFIG.json'),
  'plan_sha256':sha(R/'PLAN.json'),'chat_approval_sha256':sha(R/'CHAT_APPROVAL.json'),
  'manifest_sha256':sha(R/'MANIFEST.json'),'service':service,'python':sys.executable,
  'model_parameters':{'model':'deepseek-flash','thinking':{'type':'enabled'},'reasoning_effort':'high','max_tokens':32768},
  'method_config_unchanged_live_grant_checked_by_external_factory':True,'no_Gold':True,'no_scoring':True}
 if (OUT/'RUN_IDENTITY.json').exists():
  old_identity=read(OUT/'RUN_IDENTITY.json')
  if {k:v for k,v in old_identity.items() if k!='service'}!={k:v for k,v in identity.items() if k!='service'}:raise ValueError('resume_runtime_identity_changed')
 else:save(OUT/'RUN_IDENTITY.json',identity)
 for name in ('ENDED.json','PREDICTIONS_FROZEN.json','RESULTS.json','STATUS.json'):preserve(name)
 if (OUT/'ENDED.json').exists():(OUT/'ENDED.json').unlink()
 if (OUT/'STOP').exists():(OUT/'STOP').unlink()
 env=dict(os.environ,PYTHONPATH=os.pathsep.join([str(R/'runtime'),str(R/'source/src'),str(R/'source/runtime')]),
  SI_TOKENIZER_ROOT=assets['path'],PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8',TOKENIZERS_PARALLELISM='false')
 log=OUT/'progress.log';offset=log.stat().st_size if log.exists() else 0
 with log.open('ab') as h:
  process=subprocess.Popen([sys.executable,'-B',str(R/'runtime/supervisor.py')],stdin=subprocess.DEVNULL,
   stdout=h,stderr=subprocess.STDOUT,env=env,start_new_session=True)
 save(OUT/'BACKGROUND_PROCESS.json',{'pid':process.pid,'epoch':time.time(),'detached_session':True,'key_saved':False,
  'original_deadline_epoch':grant['deadline_epoch']})
 os.environ.pop('DEEPSEEK_API_KEY',None);key=''
 print('后台已启动，断开终端也会继续；结果目录 '+str(OUT),flush=True)
 view(offset)

def main():
 if '--follow' in sys.argv:view();return
 if '--stop' in sys.argv:
  OUT.mkdir(exist_ok=True);(OUT/'STOP').touch();print('已请求安全停止；原始结果与未知费用保留，不重复请求。',flush=True);return
 if '--status' in sys.argv:
  print(json.dumps(read(OUT/'STATUS.json'),ensure_ascii=False,indent=2) if (OUT/'STATUS.json').exists() else '尚无运行状态。');return
 try:approval();interpreter();launch('--resume' in sys.argv)
 except KeyboardInterrupt:print('启动已取消；已有后台不受影响。',flush=True)
 except BaseException as error:
  save(OUT/('STARTUP_ERROR_'+str(time.time_ns())+'.json'),{'error':type(error).__name__+':'+str(error),'traceback':traceback.format_exc()})
  print('启动停止：'+str(error)+'；错误与原件目录 '+str(OUT),flush=True);raise SystemExit(1)
if __name__=='__main__':main()

````

## runtime/supervisor.py

原文件 SHA-256 `88a121da62bf00b319eba575da14e720e5531e35353083de4406a30e6ef12193`

````python
"""User-started, self-contained Full200 supervisor. No Gold or scoring imports."""
from pathlib import Path
import os,sys,time,signal,subprocess,shutil,traceback,json
from common import R,SOURCE,ROUND,read,write,sha,safe_error
from ledger import Ledger

def allowed_parallel(healthy,memory,disk):
    # Inherited resource thresholds; no namespace/cgroup condition.
    if memory<4*1024**3:return 2
    return 8 if healthy and memory>=12*1024**3 and disk>=5*1024**3 else 6

def resources(active,out):
    available=0
    for line in Path('/proc/meminfo').read_text().splitlines():
        if line.startswith('MemAvailable:'):available=int(line.split()[1])*1024
    owned={p.pid for p,_,_ in active.values() if p.poll() is None};rss=0
    for d in Path('/proc').glob('[0-9]*'):
        try:
            stat=(d/'stat').read_text();tail=stat[stat.rindex(')')+2:].split()
            if int(tail[2]) in owned:rss+=int((d/'statm').read_text().split()[1])*os.sysconf('SC_PAGE_SIZE')
        except (OSError,ValueError,IndexError):pass
    return available,shutil.disk_usage(out).free,rss

def kill(proc):
    if proc.poll() is not None:return
    try:os.killpg(proc.pid,signal.SIGTERM);proc.wait(timeout=1)
    except ProcessLookupError:return
    except subprocess.TimeoutExpired:
        try:os.killpg(proc.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        proc.wait()

def gate_first_batch(results):
    protocol=[r['member'] for r in results if r.get('report_saved') and not r.get('analysis_available')]
    errors={}
    for r in results:
        if r.get('technical_error'):errors.setdefault(r.get('technical_error_group',r['technical_error']),[]).append(r['member'])
    blocked=len(protocol)>=4 or any(len(v)>=2 for v in errors.values())
    return {'passed':not blocked,'unusable_protocol_or_consumption':protocol,'uncaught_error_groups':errors,
        'checks_only_technical_chain_not_findings_or_scores':True}


def recover_report(member,attempt,task,returncode):
    path=attempt/'analysis/report.json'
    if path.is_file():
        report=read(path)
        return {'member':member,'task':task,'report_saved':True,'analysis_available':report['model_analysis_available'],
            'with_gaps':True,'findings':len(report['findings']),'report':str(path),'report_sha256':sha(path),
            'wrapper_did_not_finish':True,'real_model_validation':True,'not_a_safe_prediction':True}
    return {'member':member,'task':task,'technical_error':'worker_exit_'+str(returncode),'partial_files':str(attempt),'not_a_safe_prediction':True}

def main():
    import fcntl
    out=R/'run';out.mkdir(exist_ok=True);lock=(out/'SUPERVISOR_LOCK').open('a')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    ledger=Ledger(out/'requests.sqlite');grant=read(out/'AUTHORIZATION.json');ledger.recover()
    if grant!=ledger.meta('grant') or grant['package_manifest_sha256']!=sha(R/'MANIFEST.json'):raise ValueError('runtime_grant_identity')
    members=read(R/'MEMBERS.json');tasks={m:'AC' if k=='SmartBug' else 'FCR' for k,v in members.items() for m in v}
    plan=read(R/'PLAN.json');first=plan['first_six'];rest=sorted(set(tasks)-set(first));active={};results={};last=0;phase='first_six';parallel=6
    started=grant['start_epoch'];deadline=grant['deadline_epoch'];cause='normal_completion';full_size=0;resource_clock=0
    def signal_stop(*args):(out/'STOP').touch()
    signal.signal(signal.SIGTERM,signal_stop);signal.signal(signal.SIGINT,signal_stop)
    def known_result(member):
        p=out/'members'/member/'FINAL_ENTRY.json'
        if not p.exists():return None
        result=read(p)
        if result.get('interrupted') and not result.get('report_saved'):
            money=ledger.snapshot(member)
            if not money['unknown'] and not money['inflight']:
                history=p.parent/'previous_entries';history.mkdir(exist_ok=True)
                shutil.copy2(p,history/(str(time.time_ns())+'_FINAL_ENTRY.json'))
                return None
        return result
    for member in tasks:
        old=known_result(member)
        if old:results[member]=old
    def progress(force=False):
        nonlocal last,full_size,resource_clock
        if not force and time.time()-last<20:return
        last=time.time();mem,disk,rss=resources(active,out)
        if time.time()-resource_clock>=20:
            full_size=0
            for p in out.rglob('*'):
                try:
                    if p.is_file():full_size+=p.stat().st_size
                except FileNotFoundError:pass  # atomic result writer replaced its temporary path
            resource_clock=time.time()
        money=ledger.snapshot();rows=list(results.values())
        status={'phase':phase,'reports_saved':sum(r.get('report_saved',False) for r in rows),
            'with_gaps':sum(r.get('with_gaps',False) for r in rows),'technical_errors':sum(bool(r.get('technical_error')) for r in rows),
            'not_yet_reported':len(tasks)-sum(r.get('report_saved',False) for r in rows),
            'findings':sum(r.get('findings',0) for r in rows),'active':len(active),'parallel':parallel,
            'elapsed_seconds':round(time.time()-started),'model_requests':money['real_model_calls'],
            'settled_upper_usd':money['settled_cost_usd_upper'],'inflight_requests':money['inflight'],
            'unknown_requests':money['unknown'],'inflight_or_unknown_upper_usd':money['unknown_or_inflight_upper_usd'],'money_reservations':False,'dispatch_halt':money['halt'],
            'owned_RSS_GiB':round(rss/1024**3,2),'available_GiB':round(mem/1024**3,2),'run_disk_GiB':round(full_size/1024**3,2)}
        write(out/'STATUS.json',status);print(json.dumps(status,ensure_ascii=False),flush=True)
    progress(True)
    try:
        for phase,group in [('first_six',first),('SmartBug',[m for m in members['SmartBug'] if m not in first]),('JANUS',members['JANUS'])]:
            if phase=='SmartBug':
                check=gate_first_batch([results[m] for m in first if m in results]);write(out/'FIRST_SIX_CHECK.json',check)
                if not check['passed']:cause='first_six_systemic_technical_stop';break
            queue=[m for m in group if m not in results]
            while queue or active:
                mem,disk,rss=resources(active,out);now=time.time()
                if now>=deadline:cause='full_hard_deadline';break
                if (out/'STOP').exists():cause='user_stop';break
                if ledger.snapshot()['halt']:cause='dispatch_stopped:'+str(ledger.snapshot()['halt']);break
                if mem<1024**3 or disk<1024**3 or rss>32*1024**3 or full_size>20*1024**3:cause='resource_guard_stop';break
                recent=list(results.values())[-6:]
                healthy=phase!='first_six' and len(recent)==6 and all(r.get('analysis_available') and not r.get('technical_error') for r in recent)
                parallel=min(6,allowed_parallel(False,mem,disk)) if phase=='first_six' else allowed_parallel(healthy,mem,disk)
                while queue and len(active)<parallel:
                    member=queue.pop(0);home=out/'members'/member;home.mkdir(parents=True,exist_ok=True)
                    n=len(list(home.glob('attempt_*')))+1;attempt=home/('attempt_'+str(n));log=(home/('worker_'+str(n)+'.log')).open('wb')
                    cmd=[sys.executable,'-B',str(R/'runtime/worker.py'),'--member',member,'--task',tasks[member],
                        '--inputs',grant['input_root'],'--out',str(attempt),'--run',str(out)]
                    env=dict(os.environ,PYTHONPATH=os.pathsep.join([str(R/'runtime'),str(SOURCE/'src'),str(SOURCE/'runtime')]),
                        PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8',TOKENIZERS_PARALLELISM='false')
                    p=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL,env=env,start_new_session=True)
                    active[member]=(p,log,{'attempt':str(attempt),'start':now,'number':n})
                for member,(p,log,info) in list(active.items()):
                    if p.poll() is None:
                        if now-info['start']>3720:kill(p)
                        else:continue
                    log.close();del active[member];entry=Path(info['attempt'])/'ENTRY_RESULT.json'
                    result=read(entry) if entry.exists() else recover_report(member,Path(info['attempt']),tasks[member],p.returncode)
                    result['attempt_directory']=info['attempt'];results[member]=result;write(out/'members'/member/'FINAL_ENTRY.json',result)
                progress();time.sleep(.5)
            if cause!='normal_completion':break
    except BaseException as error:
        cause='supervisor_exception:'+safe_error(error);write(out/'SUPERVISOR_ERROR.json',{'reason':safe_error(error),'traceback':traceback.format_exc()})
    finally:
        if cause!='normal_completion':ledger.halt(cause)
        # Preserve independently finished reports; unknown in-flight requests are
        # never resent. A hard Full deadline receives no extra grace interval.
        until=min(deadline,time.time()+20) if cause=='user_stop' else time.time()
        while active and time.time()<until:
            for member,(p,log,info) in list(active.items()):
                if p.poll() is not None:
                    log.close();del active[member];entry=Path(info['attempt'])/'ENTRY_RESULT.json'
                    if entry.exists():
                        result=read(entry);result['attempt_directory']=info['attempt'];results[member]=result
                        write(out/'members'/member/'FINAL_ENTRY.json',result)
            time.sleep(.1)
        for member,(p,log,info) in list(active.items()):
            kill(p);log.close();result=recover_report(member,Path(info['attempt']),tasks[member],p.returncode);result['interrupted']=cause;result['attempt_directory']=info['attempt'];results.setdefault(member,result)
            write(out/'members'/member/'FINAL_ENTRY.json',results[member])
        active.clear();ledger.recover();phase='ended';progress(True)
        for member in tasks:results.setdefault(member,{'member':member,'not_run':cause,'not_a_safe_prediction':True})
        write(out/'RESULTS.json',[results[m] for m in sorted(results)])
        frozen={}
        for folder in (out/'members',out/'requests'):
            for path in folder.rglob('*'):
                if path.is_file():frozen[str(path.relative_to(out))]=sha(path)
        write(out/'PREDICTIONS_FROZEN.json',{'files':frozen,'before_Gold':True,'scoring_performed':False,'evaluation_inputs_read':False,
            'includes_failed_and_unfinished_artifacts':True,'members':sorted(tasks)})
        end={'reason':cause,'epoch':time.time(),'wall_seconds':time.time()-started,'original_deadline':deadline,
            'ledger':ledger.snapshot(),'result_directory':str(out),'owned_processes_stopped':True,
            'no_namespace_or_cgroup_claim':True,'no_scoring':True}
        write(out/'ENDED.json',end)
        print('运行结束：'+cause+'；结果目录 '+str(out)+'；实际/可能已提交请求 '+str(end['ledger']['real_model_calls']),flush=True)
    return 0 if cause=='normal_completion' else 1

if __name__=='__main__':
    try:code=main()
    except BlockingIOError:
        print('已有本轮监督进程，拒绝重复启动。',flush=True);code=2
    except BaseException as error:
        out=R/'run';out.mkdir(exist_ok=True)
        write(out/'SUPERVISOR_START_OR_CLOSE_ERROR.json',{'error':safe_error(error),'traceback':traceback.format_exc()})
        write(out/'ENDED.json',{'reason':'supervisor_initialization_or_close_error:'+safe_error(error),
            'result_directory':str(out),'epoch':time.time(),'not_a_safe_prediction':True})
        print('运行结束：监督器初始化或收尾异常；结果目录 '+str(out),flush=True);code=1
    raise SystemExit(code)

````

## runtime/worker.py

原文件 SHA-256 `be8ae29f8881ce20f07eb8b3bc001a7fca3619175e12bf1c9c9822b8ff6b9a4c`

````python
"""One isolated member; the approved CLI intake/engine/feedback/report pipeline."""
from pathlib import Path
from types import SimpleNamespace
import os,sys,time,traceback
from common import R,SOURCE,read,write,safe_error,sha
from live_client import Client
from pr_next_joint.investigation.cli import run

def execute(member,task,input_root,out,run_root,*,sender=None,simulated=False,engineering=None,target=None):
    out=Path(out)
    job=read(Path(run_root)/'JOBS.json')[member]
    args=SimpleNamespace(root=job['root'],compiled_unit=job['descriptor'],
        engineering_compiled=str(engineering) if engineering else None,target=[target] if target else None,
        task=task,out=str(out),config=str(R/'METHOD_CONFIG.json'),tokenizer=os.environ.get('SI_TOKENIZER_ROOT') or read(Path(run_root)/'TOKENIZER_ROOT.json')['path'],phase='analyze',
        fixture_response=None,fixture_feedback=None,offline_bridge=False,case_id=member)
    def factory(program,args,counter):
        actual=read(out/'intake_receipt.json');expected=job['expected']
        for key in ('program_id','build_id','source_hashes','targets_selected','compiler_version'):
            if actual[key]!=expected[key]:raise ValueError('frozen_input_identity:'+key)
        if expected.get('compiler_sha256') and actual['compiler_sha256']!=expected['compiler_sha256']:
            raise ValueError('frozen_compiler_binary_identity')
        return Client(member,program.identity,run_root,sender=sender,simulated=simulated)
    try:
        report=run(args,client_factory=factory)
        gaps=bool(report['diagnostics']['program_gaps'] or report['diagnostics']['unexecuted_actions'] or
                  report['diagnostics']['issues'] or report['unresolved_category_judgments'])
        result={'member':member,'task':task,'report_saved':True,'analysis_available':report['model_analysis_available'],
            'with_gaps':gaps,'findings':len(report['findings']),'usage':report['usage'],
            'report':str(out/'analysis/report.json'),'prediction_manifest':str(out/'analysis/prediction_manifest.json'),
            'report_sha256':sha(out/'analysis/report.json'),'real_model_validation':not simulated}
    except BaseException as error:
        out.mkdir(parents=True,exist_ok=True)
        write(out/'ENTRY_ERROR.json',{'error':safe_error(error),'traceback':traceback.format_exc(),'not_a_safe_prediction':True})
        result={'member':member,'task':task,'report_saved':False,'technical_error':type(error).__name__,
                'technical_error_group':safe_error(error).replace(member,'<member>'),
                'detail':safe_error(error),'partial_files_preserved':True,'not_a_safe_prediction':True}
    write(out/'ENTRY_RESULT.json',result);return result

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--member',required=True);p.add_argument('--task',choices=['AC','FCR'],required=True)
    p.add_argument('--inputs',required=True);p.add_argument('--out',required=True);p.add_argument('--run',required=True)
    a=p.parse_args();r=execute(a.member,a.task,a.inputs,a.out,a.run)
    print('成员结束：'+a.member+'；报告已保存' if r['report_saved'] else '成员技术异常：'+a.member,flush=True)
    raise SystemExit(0 if r['report_saved'] else 1)

````

## source/configs/full.json

原文件 SHA-256 `b68788d9b0c121d1cae3e880757611f771ea5fad2416c687fa3126551323f6db`

````text
{
  "method": "permission-risks-semantic-properties-r1",
  "options": {
    "feedback": true,
    "attempt_limit": 2,
    "max_paths": 48,
    "prefix_depth": 2,
    "max_prefixes": 24,
    "max_actions": 64,
    "seconds": 120,
    "solver_timeout_ms": 3000,
    "input_target": 16384,
    "input_limit": 32768,
    "output_limit": 32768
  },
  "live_model_authorized": false,
  "notes": "Approved semantic-property Full: shared source summaries and semantic bindings, typed evidence composition and obligation coverage. Offline acceptance only; no live authorization inherited. Runtime limits are local defaults, not a future paid authorization."
}

````

## source/requirements-dev.txt

原文件 SHA-256 `ac3b9daad7613d985567e0c2eed70660e78729ecd1d49484b2952a6e92c6e505`

````text
-r requirements.txt
pytest==8.3.5

````

## source/requirements-frontend.txt

原文件 SHA-256 `a2a3fa701ade8c2545e557d2ba11c7c35a7ed799e5d295c863df8913215292b2`

````text
-r requirements.txt
slither-analyzer==0.11.3
crytic-compile==0.3.11
solc-select==1.2.0

````

## source/requirements.txt

原文件 SHA-256 `ae9a4281cb7d9c9b64571b1628ce17e38607293893567849800bc675d0eafa9c`

````text
z3-solver==4.15.3.0
eth-keys==0.7.0
pycryptodome==3.24.1
tokenizers==0.22.2

````

## source/runtime/batch.py

原文件 SHA-256 `2e504de54a17a74f2a27f3168c29016a6846b92c5c03013da463e01fc4d39073`

````python
"""Offline subprocess assembly; per-case namespaces and owned-process deadlines."""
import argparse,json,time,subprocess,sys,os,signal,traceback,hashlib
from pathlib import Path
from pr_next_joint.investigation.contracts import write

def parallel_limit(healthy,available_gib):
    if available_gib is not None and available_gib<16:return 2
    return 8 if healthy and available_gib is not None and available_gib>=32 else 6

def available_memory():
    p=Path('/proc/meminfo')
    if not p.exists():return None
    for line in p.read_text().splitlines():
        if line.startswith('MemAvailable:'):return int(line.split()[1])/1048576
    return None

def stop_owned(proc):
    if proc.poll() is not None:return
    if os.name=='nt':
        subprocess.run(['taskkill','/PID',str(proc.pid),'/T','/F'],capture_output=True)
    else:
        try:os.killpg(proc.pid,signal.SIGTERM)
        except ProcessLookupError:return
        try:proc.wait(timeout=1)
        except subprocess.TimeoutExpired:
            try:os.killpg(proc.pid,signal.SIGKILL)
            except ProcessLookupError:pass
    try:proc.wait(timeout=2)
    except subprocess.TimeoutExpired:pass

def owned_rss(active):
    total=0
    for proc,_,_ in active.values():
        p=Path('/proc')/str(proc.pid)/'status'
        if p.exists():
            for line in p.read_text().splitlines():
                if line.startswith('VmRSS:'):total+=int(line.split()[1])/1048576
    return total

def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--out',required=True)
    p.add_argument('--tokenizer',required=True);p.add_argument('--wall-seconds',type=float,default=21600)
    args=p.parse_args(argv);out=Path(args.out).resolve();out.mkdir(parents=True,exist_ok=True)
    if any(out.iterdir()):raise ValueError('fresh_batch_directory_required')
    items=json.loads(Path(args.manifest).read_text(encoding='utf-8-sig'));ids=[r['case_id'] for r in items]
    if len(ids)!=len(set(ids)) or any(not i.replace('_','').replace('-','').isalnum() for i in ids):raise ValueError('case_namespace')
    first=[]
    for task in ('AC','FCR'):first+=sorted([x for x in items if x['task']==task],key=lambda x:x['case_id'])[:3]
    first_ids={x['case_id'] for x in first};rest=sorted([x for x in items if x['case_id'] not in first_ids],key=lambda x:x['case_id'])
    started=time.monotonic();deadline=started+args.wall_seconds;last=0;active={};results=[];cause='normal_completion';parallel=6
    def progress(force=False):
        nonlocal last
        if not force and time.monotonic()-last<20:return
        last=time.monotonic()
        value={'reports_saved':sum('analysis_available' in r for r in results),'with_analysis':sum(r.get('analysis_available',False) for r in results),
          'technical_errors':sum('technical_error' in r for r in results),'actual_model_submissions':0,
          'fixture_requests':sum(r.get('fixture_requests',0) for r in results),'settled_usd':0,'active':len(active),'parallel':parallel,
          'elapsed_seconds':round(time.monotonic()-started),'owned_RSS_GiB_sampled':owned_rss(active),'available_GiB':available_memory()}
        print(json.dumps(value),flush=True);write(out/'STATUS.json',value)
    progress(True)
    try:
        for phase,group in enumerate((first,rest)):
            if phase:
                unusable=[r for r in results if not r.get('analysis_available') and 'not_started' not in r]
                errors={}
                for r in unusable:
                    if r.get('technical_error'):errors[r['technical_error']]=errors.get(r['technical_error'],0)+1
                if sum('technical_error' not in r for r in unusable)>=4 or any(n>=2 for n in errors.values()):cause='first_six_systemic_wiring_failure';break
                parallel=parallel_limit(not unusable,available_memory())
            queue=list(group)
            while queue or active:
                if (out/'STOP').exists() or time.monotonic()>=deadline or owned_rss(active)>32:
                    cause='user_stop_or_hard_wall_or_RSS_limit';break
                allowed=parallel_limit(phase>0 and not any('technical_error' in r for r in results),available_memory())
                parallel=min(parallel,allowed)
                while queue and len(active)<parallel:
                    item=queue.pop(0);case=item['case_id'];log=(out/(case+'.log')).open('wb')
                    cmd=[sys.executable,'-B',str(Path(__file__).resolve().parents[1]/'scripts/run_method.py'),
                      '--engineering-compiled',item['engineering_compiled'],'--target',item['target'],'--task',item['task'],
                      '--out',str(out/case),'--tokenizer',args.tokenizer,'--fixture-response',item['fixture_response'],'--case-id',case,'--offline-bridge']
                    if item.get('fixture_feedback'):cmd+=['--fixture-feedback',item['fixture_feedback']]
                    env=dict(os.environ,PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1',TOKENIZERS_PARALLELISM='false')
                    kw={'creationflags':subprocess.CREATE_NEW_PROCESS_GROUP} if os.name=='nt' else {'start_new_session':True}
                    proc=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,env=env,**kw);active[case]=(proc,log,item)
                progress()
                for case,(proc,log,item) in list(active.items()):
                    if proc.poll() is None:continue
                    log.close();del active[case];rp=out/case/'analysis/report.json'
                    if proc.returncode==0 and rp.exists():
                        r=json.loads(rp.read_bytes());results.append({'case_id':case,'analysis_available':r['model_analysis_available'],
                          'findings':len(r['findings']),'fixture_requests':len(r['usage']['attempts'])})
                    else:results.append({'case_id':case,'technical_error':'entry_exit_'+str(proc.returncode),'log':case+'.log'})
                time.sleep(.05)
            if cause!='normal_completion':break
    except KeyboardInterrupt:cause='user_interrupt'
    except Exception as error:
        cause='supervisor_error:'+type(error).__name__;write(out/'SUPERVISOR_ERROR.json',{'reason':str(error),'traceback':traceback.format_exc()})
    finally:
        for case,(proc,log,item) in list(active.items()):
            stop_owned(proc);log.close();results.append({'case_id':case,'technical_error':cause,'partial_files_preserved':True})
        active.clear();finished={r['case_id'] for r in results}
        results +=[{'case_id':i,'not_started':cause} for i in ids if i not in finished]
        progress(True);write(out/'RESULTS.json',sorted(results,key=lambda r:r['case_id']))
        frozen={p.relative_to(out).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*.json') if p.name not in ('STATUS.json','PREDICTIONS_FROZEN.json')}
        write(out/'PREDICTIONS_FROZEN.json',{'files':frozen,'before_Gold':True,'scoring_performed':False})
        write(out/'ENDED.json',{'reason':cause,'actual_model_submissions':0,'seconds':time.monotonic()-started,
          'owned_processes_stopped':True,'namespace_or_cgroup_containment_claimed':False})
        print('运行结束：'+cause+'；实际模型请求0；结果目录 '+str(out),flush=True)
    return 0 if cause=='normal_completion' else 1

if __name__=='__main__':raise SystemExit(main())

````

## source/runtime/bridge.py

原文件 SHA-256 `28b7c0843633df3e49c54555f962dd92b51d3219194de3f5aa78f7f514845e08`

````python
"""Credential-free, atomic file bridge; this delivery's broker is offline only."""
from pathlib import Path
import copy,json,os,tempfile,time,threading
from pr_next_joint.core import digest

def publish(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    data=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    if path.exists():
        if path.read_bytes()!=data:raise ValueError('immutable_packet_conflict')
        return
    fd,tmp=tempfile.mkstemp(prefix='.packet_',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

class FixtureClient:
    def __init__(self,responses,case_id='engineering',program_identity=None):
        self.responses=responses;self.case_id=case_id;self.program_identity=program_identity;self.calls=[]
    def call(self,messages,tag,**parameters):
        i=len(self.calls)
        if i>=2:raise ValueError('two_submissions_limit')
        if parameters!={'max_tokens':32768,'thinking':True,'reasoning_effort':'high','timeout':1800}:raise ValueError('request_parameter_contract')
        self.calls.append({'messages':copy.deepcopy(messages),'tag':tag,'parameters':parameters})
        provider=self.responses[i] if i<len(self.responses) else None
        if provider is None:raise ValueError('offline_response_not_provided')
        raw=provider(messages) if callable(provider) else copy.deepcopy(provider)
        return raw,{'simulated':True,'source':'explicit engineering fixture, not saved real answer',
          'case_id':self.case_id,'program_identity':self.program_identity,'call_index':i,'messages_sha256':digest(messages),'response_sha256':digest(raw),
          'actual_model_submissions':0,'cost_usd':0,'usage':{'prompt_tokens':0,'completion_tokens':0,'reasoning_tokens':0,'nature':'no provider usage; offline tokens in request manifest'}}

class FileClient:
    def __init__(self,folder,case_id,program_identity,deadline_seconds=15):
        self.folder=Path(folder);self.case_id=case_id;self.program_identity=program_identity;self.index=0;self.deadline_seconds=deadline_seconds
    def call(self,messages,tag,**parameters):
        index=self.index
        if index>=2:raise ValueError('two_submissions_limit')
        self.index+=1
        packet={'case_id':self.case_id,'program_identity':self.program_identity,'index':index,'tag':tag,
                'messages':messages,'messages_sha256':digest(messages),'parameters':parameters}
        # Identity is checked in the immutable packet, not encoded in a long Windows filename.
        token='call'+str(index);q=self.folder/(token+'.request.json');r=self.folder/(token+'.response.json')
        publish(q,packet);until=time.monotonic()+self.deadline_seconds
        while not r.exists():
            if time.monotonic()>=until:raise TimeoutError('offline_file_bridge_timeout')
            time.sleep(.01)
        v=json.loads(r.read_bytes())
        for field in ('case_id','program_identity','index','tag','messages_sha256'):
            if v.get(field)!=packet[field]:raise ValueError('bridge_identity_mismatch:'+field)
        if v.get('error'):raise ValueError(v['error'])
        return v['raw'],v['receipt']

class MockBroker:
    """Uses the same on-disk packets as FileClient; never imports an HTTP client."""
    def __init__(self,folder,responses,case_id,program_identity):
        self.folder=Path(folder);self.folder.mkdir(parents=True,exist_ok=True)
        self.fixture=FixtureClient(responses,case_id,program_identity);self.case_id=case_id;self.identity=program_identity
        self.stop=threading.Event();self.thread=None;self.errors=[]
    def __enter__(self):
        def loop():
            seen=set()
            while not self.stop.wait(.005):
                for p in sorted(self.folder.glob('*.request.json')):
                    if p.name in seen:continue
                    seen.add(p.name);v=json.loads(p.read_bytes());response={k:v[k] for k in ('case_id','program_identity','index','tag','messages_sha256')}
                    try:
                        if v['case_id']!=self.case_id or v['program_identity']!=self.identity:raise ValueError('broker_case_identity')
                        raw,receipt=self.fixture.call(v['messages'],v['tag'],**v['parameters']);response.update(raw=raw,receipt=receipt)
                    except Exception as error:response['error']=str(error);self.errors.append(str(error))
                    publish(p.with_name(p.name.replace('.request.','.response.')),response)
        self.thread=threading.Thread(target=loop,daemon=True);self.thread.start();return self
    def __exit__(self,*args):self.stop.set();self.thread.join(1)

class UsageJournal:
    """Record calls/unknown usage. No per-request financial reservations or waiter queue.

    A future authorized batch can use the static *whole round* worst-case bound:
    92*(32768*0.30+32768*1.20)/1e6 = $4.521984 at these illustrative prices.
    This is a bound calculation, not current service verification or live approval.
    """
    def __init__(self,path,max_calls=92,per_case=2):
        self.path=Path(path);self.max_calls=max_calls;self.per_case=per_case;self.lock=threading.Lock()
        self.state={'actual_submissions':0,'fixture_requests':0,'settled_usd':0,'unknown_calls':[], 'events':[],
                    'per_request_money_reservation':False,'live_authorized':False}
    def fixture(self,case,index,request_tokens):
        with self.lock:
            count=sum(e['case']==case for e in self.state['events'])
            if self.state['fixture_requests']>=self.max_calls or count>=self.per_case:raise ValueError('global_or_per_case_request_limit')
            self.state['fixture_requests']+=1;self.state['events'].append({'case':case,'index':index,'offline_input_tokens':request_tokens,'actual_submissions':0,'usd':0})
            publish(self.path.with_name(self.path.name+'.event'+str(self.state['fixture_requests'])),self.state['events'][-1])
            from pr_next_joint.investigation.contracts import write
            write(self.path,self.state)
    @staticmethod
    def full_round_bound(max_calls,input_limit,output_limit,input_price,output_price):
        return max_calls*(input_limit*input_price+output_limit*output_price)/1000000

````

## source/runtime/reference_counter.py

原文件 SHA-256 `557b0bd400a453dbeb5ed46bf1295f244df35ded934331f73bdf09a2bd87dc8e`

````python
"""Runtime-only V4.1 counting for the frozen text-only API request contract.
No change to messages sent to the model. Official source at pinned revisions
defines System/effort/JSON envelope and consecutive user-message joining.
"""
from pathlib import Path
import hashlib,json
PINS={'v41_tokenizer.json':'c90dfa01249db1be4245780a052ede752e1361c612ac6d08e2bdada7d599476b',
      'v41_tokenizer_config.json':'6ac8c8dc065ed118161d02dd532749ae3f52c243deac27872134fae2f50d8547',
      'v41_encoding_encoding.py':'13231c592e958fb39e2af6001dae69d90e7a36b265702b9b390236fb387599e2'}
EFFORT='Reasoning Effort: 75 (range 1-100, the higher the value, the more thorough the reasoning)\n\n'
FORMAT='\n\n## Response Format:\n\nYou MUST strictly adhere to the following schema to reply:\n{"type": "json_object"}'

class Counter:
    def __init__(self,folder):
        from tokenizers import Tokenizer
        folder=Path(folder)
        self.identity={k:hashlib.sha256((folder/k).read_bytes()).hexdigest() for k in PINS}
        if self.identity!=PINS:raise ValueError('v41_reference_artifact_changed')
        self.tokenizer=Tokenizer.from_file(str(folder/'v41_tokenizer.json'))
        # Tokenize untrusted message text as plain text; actual role markers are
        # added separately, matching recipe's explicit special_ranges handling.
        plain_config=json.loads((folder/'v41_tokenizer.json').read_bytes())
        plain_config['added_tokens']=[]
        self.plain_tokenizer=Tokenizer.from_str(json.dumps(plain_config))
    def fragments(self,messages):
        if len(messages) not in (2,3) or [m.get('role') for m in messages]!=['system']+['user']*(len(messages)-1):
            raise ValueError('unsupported_counting_message_contract')
        if any(set(m)!={'role','content'} or not isinstance(m['content'],str) for m in messages):
            raise ValueError('unsupported_message_fields')
        return [('special','<｜begin▁of▁sentence｜>'),('special','<｜System｜>'),
                ('plain',EFFORT+messages[0]['content']+FORMAT),('special','<｜User｜>'),
                ('plain','\n\n'.join(m['content'] for m in messages[1:])),
                ('special','<｜Assistant｜>'),('special','<think>')]
    def render(self,messages):return ''.join(x for _,x in self.fragments(messages))
    def count(self,messages):
        total=0
        for kind,text in self.fragments(messages):
            if kind=='special':
                if self.tokenizer.token_to_id(text) is None:raise ValueError('special_token_missing')
                total+=1
            else:total+=len(self.plain_tokenizer.encode(text,add_special_tokens=False).ids)
        return total

````

## source/scripts/extract_compiler_facts.py

原文件 SHA-256 `387d9702a684d35743b0fac1c9a25ae32175fa04da8b718b166c666be6291eb0`

````python
"""One original solc invocation, retained-output native facts, no program run."""
import argparse,copy,hashlib,json,os,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from pr_next_joint.core import digest, require
from pr_next_joint.frontend.facts import build_bundle

def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def source_paths(standard,root):
    """Check every path before writing any materialized source."""
    items=[]
    for name,item in standard['sources'].items():
        require(isinstance(name,str) and '\\' not in name and ':' not in name,'source_path_format')
        relative=pathlib.PurePosixPath(name)
        require(not relative.is_absolute() and '..' not in relative.parts,'source_path_scope')
        path=(root/name).resolve()
        require(path.is_relative_to(root.resolve()),'source_path_scope')
        require(isinstance(item.get('content'),str),'inline_source_content_required')
        items.append((path,item['content'].encode('utf-8')))
    require(bool(items),'sources_required')
    return items

def extract_retained(standard,compiled,bundle,receipt,work):
    # Same retained-output adapter as c2_static_remote, without running C2.
    # These imports must not require the Linux packages merely to inspect CLI.
    # The retained extractor must not create ~/.solc-select merely on import.
    # No compiler installation/download is performed; only project-scoped cache setup.
    from solc_select import constants as compiler_constants
    cache=pathlib.Path(os.environ.get('PR_SOLC_ARTIFACT_CACHE',str(pathlib.Path(work).resolve().parent/'.compiler-cache')))
    compiler_constants.SOLC_SELECT_DIR=cache
    compiler_constants.ARTIFACTS_DIR=cache/'artifacts'
    from crytic_compile import CryticCompile
    from crytic_compile.compilation_unit import CompilationUnit
    from crytic_compile.compiler.compiler import CompilerVersion
    from crytic_compile.platform.solc_standard_json import SolcStandardJson,parse_standard_json_output
    from slither.slither import Slither
    from pr_next_joint.frontend.native_facts import extract
    class RetainedOutput(SolcStandardJson):
        def compile(self,crytic_compile,**kwargs):
            unit=CompilationUnit(crytic_compile,'m03_retained_output')
            optimizer=standard['settings'].get('optimizer',{})
            unit.compiler_version=CompilerVersion(compiler='solc',version=receipt['compiler_version'],
                optimized=optimizer.get('enabled',False),optimize_runs=optimizer.get('runs'))
            parse_standard_json_output(compiled,unit,solc_working_dir=str(work))
    previous=pathlib.Path.cwd()
    try:
        os.chdir(work)
        return extract(Slither(CryticCompile(RetainedOutput(copy.deepcopy(standard)),cwd=str(work))),bundle,copy.deepcopy(receipt))
    finally:os.chdir(previous)

def run(standard_input,compiler,output,group,expected_version='0.8.20',runner=None,native_loader=None):
    src=pathlib.Path(standard_input).resolve();compiler=pathlib.Path(compiler).resolve()
    out=pathlib.Path(output).resolve();out.mkdir(parents=True,exist_ok=False)
    receipt={'group':group,'status':'started','compiler_path':str(compiler),
             'compiler_invocations':0,'native_extractions':0,'program_execution':False,
             'input_material_origin':'compiler_artifacts',
             'build_comparison':'same output supplied to build_bundle; no independent frozen-version comparison'}
    def streams(stdout,stderr):
        for name,value in [('compiler.stdout',stdout),('compiler.stderr',stderr)]:
            if isinstance(value,bytes):value=value.decode('utf-8',errors='replace')
            (out/name).write_text(value or '',encoding='utf-8')
    try:
        raw=src.read_bytes();standard=json.loads(raw.decode('utf-8-sig'))
        work=out/'sources';paths=source_paths(standard,work)
        receipt.update(compiler_binary_sha256=hashlib.sha256(compiler.read_bytes()).hexdigest(),
            standard_input_sha256=hashlib.sha256(raw).hexdigest(),standard_input_digest=digest(standard))
        (out/'standard-input.json').write_bytes(raw)
        for path,content in paths:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(content)
        receipt['compiler_invocations']=1;save(out/'extract_receipt.json',receipt)
        try:
            process=(runner or subprocess.run)([str(compiler),'--standard-json'],input=json.dumps(standard,ensure_ascii=False),
                capture_output=True,text=True,encoding='utf-8',cwd=work,timeout=120)
        except subprocess.TimeoutExpired as error:
            streams(error.stdout,error.stderr);raise
        streams(process.stdout,process.stderr)
        receipt['compiler_exit_code']=process.returncode
        compiled=None
        try:compiled=json.loads(process.stdout)
        except (ValueError,TypeError):pass
        if isinstance(compiled,dict):save(out/'standard-output.json',compiled)
        require(process.returncode==0,'compiler_exit:'+str(process.returncode))
        require(isinstance(compiled,dict),'compiler_output_not_json')
        errors=[e for e in compiled.get('errors',[]) if e.get('severity')=='error']
        receipt['errors']=errors;require(not errors,'compile_errors')
        versions={json.loads(c['metadata'])['compiler']['version'].split('+')[0]
                  for contracts in compiled['contracts'].values() for c in contracts.values() if c.get('metadata')}
        require(versions=={expected_version},'compiler_metadata_version_mismatch')
        receipt['compiler_version']=expected_version
        receipt['standard_output_sha256']=hashlib.sha256((out/'standard-output.json').read_bytes()).hexdigest()
        bundle=build_bundle(group,standard,compiled,compiled,receipt)
        bundle['ast_sources']={f:x['ast'] for f,x in compiled['sources'].items()}
        native=(native_loader or extract_retained)(standard,compiled,bundle,receipt,work)
        require(all(native.get(k)==bundle[k] for k in ['program_id','build_id']),'native_identity_mismatch')
        bundle['native_ir']={'sha256':digest(native),'functions':[{k:v for k,v in f.items() if k!='nodes'} for f in native['functions']],
            'ssa_operation_count':native.get('ssa_operation_count'),'slither_version':native.get('slither')}
        bundle['coverage']['slither_fresh']='executed_from_retained_original_compiler_output'
        bundle['material_origin']='compiler_artifacts'
        receipt.update(status='compiled_and_extracted',native_extractions=1,native_sha256=digest(native),
            program_id=bundle['program_id'],build_id=bundle['build_id'],native_adapter='retained_original_output')
        save(out/'ProgramBundle.json',bundle);save(out/'native_ssa.json',native)
        save(out/'extract_receipt.json',receipt)
        return {'status':receipt['status'],'program_id':bundle['program_id'],'build_id':bundle['build_id']}
    except Exception as error:
        receipt.update(status='timeout' if isinstance(error,subprocess.TimeoutExpired) else 'failed',
            error_class=type(error).__name__,error=str(error),no_safety_conclusion=True)
        save(out/'extract_receipt.json',receipt)
        raise

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument('--standard-input',required=True);p.add_argument('--compiler',required=True)
    p.add_argument('--out',required=True);p.add_argument('--group',required=True)
    p.add_argument('--compiler-version',default='0.8.20')
    a=p.parse_args(argv)
    result=run(a.standard_input,a.compiler,a.out,a.group,a.compiler_version)
    print(json.dumps(result));return result

if __name__=='__main__':main()

````

## source/scripts/run_batch.py

原文件 SHA-256 `ce7036469d7829783a3b06015ad22314943ce839536bad42b4a42addd773f332`

````python
from pathlib import Path
import sys
root=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(root/'src'),str(root/'runtime')]
from batch import main
if __name__=='__main__':raise SystemExit(main())

````

## source/scripts/run_method.py

原文件 SHA-256 `89be133ca282f1d3976122cc20cd2baf5dbda35e8899cdc5e50657122067df2d`

````python
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from pr_next_joint.investigation.cli import main
if __name__=='__main__':raise SystemExit(main())

````

## source/src/pr_next_joint/__init__.py

原文件 SHA-256 `f18d7b365ca64d6d9a6e9ddac641cf46a86576144bc1edbeedcef44597a5938b`

````python
"""Permission Risks: source facts, semantic selection and shared verification."""
__version__ = "semantic-investigation-1.0"
VERSION = 'source-semantic-investigation-r1'
IMPLEMENTATION_PATCH = 'stage2-r1'
# Historic low-level evidence schema is retained for existing proof artifacts.
SCHEMA_VERSION = 'pr-next-task-b-r2-c1-v1'

````

## source/src/pr_next_joint/__main__.py

原文件 SHA-256 `8c1de7da674c56d218ac33d0cdeeca6b3a301ea16ca625d1cc2bbccf4d65ce4c`

````python
from .refinement.cli import main
raise SystemExit(main())

````

## source/src/pr_next_joint/checks/access/__init__.py

原文件 SHA-256 `87e3e2f1dba261e0999d37d622e45825e4d2763d9091aa860663f27df53e5d17`

````python
"""Source analysis helpers retained by SCRV."""

````

## source/src/pr_next_joint/checks/access/code_control.py

原文件 SHA-256 `f64adc544f2048c65e061ea919347b1d9cecef2e5e0102ee772a637cc93346cf`

````python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""


def builtin_delegate(expr,lookup):
    return (expr.get('nodeType')=='MemberAccess' and expr.get('memberName') in ('delegatecall','callcode')
            and expr.get('expression',{}).get('typeDescriptions',{}).get('typeString') in ('address','address payable')
            and expr.get('referencedDeclaration') not in lookup.fns)

def literal_selector(n,lookup):
    if n.get('nodeType')=='Literal':return True
    if n.get('nodeType')!='FunctionCall':return False
    expr=n.get('expression',{});args=n.get('arguments',[])
    if n.get('kind')=='typeConversion' and n.get('typeDescriptions',{}).get('typeString','').startswith('bytes'):
        return len(args)==1 and literal_selector(args[0],lookup)
    from pr_next_joint.frontend.source_entry_identity import builtin_call
    return builtin_call(n,lookup,('keccak256','sha3','sha256')) and bool(args) and all(a.get('nodeType')=='Literal' for a in args)

````

## source/src/pr_next_joint/checks/access/credential_lifecycle.py

原文件 SHA-256 `5a0941251ef82663945d16d65a0d6e617b616afeec9f652ce5131a8e17cffc0e`

````python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""


def leaves(write):
    value=write['value']
    if value.get('kind')=='record':
        for field in value['fields']:
            yield from leaves({**write,'path':{**write['path'],'segments':write['path']['segments']+[{'field':field['field']}]},'value':field['value']})
    else:yield write

````

## source/src/pr_next_joint/checks/access/destruction.py

原文件 SHA-256 `a9ca610a50590a7d9e3ec13ab69fa51e89b9cea294a08b053ecde124d1129777`

````python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""
import copy
from pr_next_joint.frontend.path_ir import key, walk, lit

def terminal_created_call(calls,node,target,cid,instance,args):
    """Exact one-statement terminal callee, not general external-call success."""
    p=calls.p;s=p.current
    if getattr(p,'analysis_scope',None)!='AC':return None
    proof=calls.instances.get(key(instance),{})
    if proof.get('binding') not in ('immutable_direct_new','constructor_single_assignment_direct_new'):return None
    # A write in a derived contract can invalidate a base constructor binding.
    # Check all concrete root bases, not just the member's declaring contract.
    from pr_next_joint.frontend.source_entry_identity import function_kind
    bases=p.contract_node.get('linearizedBaseContracts',[p.contract_node['id']])
    for base in bases:
        for fn in p.nodes[base].get('nodes',[]):
            if fn.get('nodeType')!='FunctionDefinition' or function_kind(fn)=='constructor':continue
            for n in walk(fn):
                changed=n.get('leftHandSide',{}) if n.get('nodeType')=='Assignment' else n.get('subExpression',{}) if n.get('nodeType')=='UnaryOperation' and n.get('operator')=='delete' else {}
                if changed.get('referencedDeclaration')==instance['reference']:return None
    if target.get('modifiers') or target.get('parameters',{}).get('parameters') or args or target.get('returnParameters',{}).get('parameters'):return None
    body=(target.get('body') or {}).get('statements',[])
    if len(body)!=1 or body[0].get('nodeType')!='ExpressionStatement':return None
    expr=body[0].get('expression',{})
    from pr_next_joint.frontend.source_entry_identity import builtin_call
    if not builtin_call(expr,p,('selfdestruct','suicide')) or len(expr.get('arguments',[]))!=1:return None
    arg=expr['arguments'][0]
    # A literal target is fully evaluated with no storage/call side effects.
    literal=arg
    while literal.get('nodeType')=='FunctionCall' and literal.get('kind')=='typeConversion' and len(literal.get('arguments',[]))==1:
        literal=literal['arguments'][0]
    if literal.get('nodeType')!='Literal' or literal.get('kind')!='number':return None
    saved=(calls.active_contract,calls.instance,p.sender)
    try:
        calls.active_contract,calls.instance,p.sender=cid,instance,calls.address()
        recipient=p.value(arg,{})
    finally:calls.active_contract,calls.instance,p.sender=saved
    live={'kind':'parameter','id':-2000000000-int(instance['reference']),'type':'bool',
          'model_role':'created_callee_code_available','instance':instance}
    s['guards'].append(live)
    s.setdefault('bounded_external_effects',[]).append({'kind':'created_instance_terminal_destruction',
        'call_source':p.anchor(node),'callee_source':p.anchor(expr),'callee_instance':copy.deepcopy(instance),
        'recipient':recipient,'callee_sender':calls.address(),'binding':proof,'successful_call_condition':live,
        'scope':'source-bound live created callee; one terminal instruction; no callback/parent writes; child effects retained separately'})
    # Callee termination returns to caller. Never terminate the parent path.
    return lit(True)

````

## source/src/pr_next_joint/checks/access/shared_policy.py

原文件 SHA-256 `ea22aded277efa748cf520b36577781ceb523c4775515a0bfb39f78776294af9`

````python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""
from pr_next_joint.verification.expressions import Unsupported
from pr_next_joint.verification.solver import solve as bounded_solve
from pr_next_joint.verification.program_encoding import MechanismEncoder
from pr_next_joint.frontend.path_ir import key, op, lit, walk

def _typed_implies(lookup,path,predicate):
    enc=MechanismEncoder(lookup);z=enc.z
    for v in path.get("evaluated_terms",[]):enc.expr(v)
    guards=[enc.expr(v) for v in path["guards"]];wanted=enc.expr(predicate)
    if not z.is_bool(wanted):
        raise Unsupported('applicability_reference_is_not_boolean')
    if not all(z.is_bool(g) for g in guards):
        raise Unsupported('source_path_guard_is_not_boolean')
    s=z.Solver();s.set(timeout=3000);s.add(*enc.constraints,*guards)
    if bounded_solve(s)!=z.sat or enc.abstract_hash_used:return False
    s.add(z.Not(wanted))
    return bounded_solve(s)==z.unsat

def implies(lookup,path,predicate):
    import z3
    try:return _typed_implies(lookup,path,predicate)
    except z3.Z3Exception as error:
        raise Unsupported('applicability_type_or_encoding_error:'+str(error)) from error

````

## source/src/pr_next_joint/checks/credentials/__init__.py

原文件 SHA-256 `87e3e2f1dba261e0999d37d622e45825e4d2763d9091aa860663f27df53e5d17`

````python
"""Source analysis helpers retained by SCRV."""

````

## source/src/pr_next_joint/checks/credentials/credential_encoding.py

原文件 SHA-256 `7b51447cbd9017a621842296cd03caaaf4a75773b58bdaade17187df8f3788ab`

````python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""
import re
MAX_FIXED_LITERAL_BYTES = 4096
from pr_next_joint.verification.expressions import Unsupported

def fixed_literal(value):
    raw=value.get('hex');length=value.get('byte_length')
    if (value.get('kind')!='fixed_bytes_literal' or type(length) is not int
            or not 0<=length<=MAX_FIXED_LITERAL_BYTES or not isinstance(raw,str)
            or len(raw)!=2*length or re.fullmatch('[0-9a-fA-F]*',raw) is None):
        raise Unsupported('fixed_bytes_literal_layout')
    return raw.lower(),length

def layout(digest):
    if digest.get('kind')!='hash' or digest.get('algorithm')!='keccak256':
        raise Unsupported('credential_digest_not_keccak')
    encoded=digest.get('input',{})
    if encoded.get('kind')=='fixed_bytes_literal':
        _,length=fixed_literal(encoded)
        return {'mode':'raw_fixed_bytes','types':['fixed_bytes_literal:'+str(length)],'arguments':[encoded]}
    if encoded.get('kind')!='abi_encoding' or encoded.get('mode') not in ('encode','encodePacked'):
        raise Unsupported('credential_digest_not_fixed_source_encoding')
    types=encoded.get('types',[]);args=encoded.get('arguments',[])
    if not types or len(types)!=len(args):raise Unsupported('credential_payload_arity')
    typed=[]
    for typ,arg in zip(types,args):
        if arg.get('kind')=='fixed_bytes_literal':
            _,length=fixed_literal(arg)
            # A string literal in abi.encode has dynamic length/offset
            # semantics. Only its packed byte spelling is supported here.
            if encoded['mode']!='encodePacked' or not (typ.startswith('literal_string') or typ in
                    ('string','string memory','string calldata','bytes','bytes memory','bytes calldata')):
                raise Unsupported('credential_literal_cast_or_dynamic_ABI_not_lowered')
            typed.append('fixed_bytes_literal:'+str(length))
        else:
            if '[' in typ or typ in ('bytes','string') or typ.startswith(('struct ','tuple','literal_string')):
                raise Unsupported('credential_dynamic_payload_not_lowered')
            typed.append(typ)
    return {**encoded,'types':typed}

````

## source/src/pr_next_joint/core.py

原文件 SHA-256 `6e85487fc5deef2119dbf6f9cea15bf9808a068b4d83c858a89f721448178741`

````python
"""Content identities, typed observation expressions and finite-query semantics."""
import hashlib,json,re
from . import SCHEMA_VERSION

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def digest(value):return hashlib.sha256(canonical(value)).hexdigest()
def ref(value):return {'id':value.get('id',digest(value)),'sha256':digest(value)}
class Invalid(ValueError):pass

def require(ok,reason):
 if not ok:raise Invalid(reason)


````

## source/src/pr_next_joint/frontend/__init__.py

原文件 SHA-256 `a9ecbc4f75a0298e4a1f82edab901936fe49977cdd1a2bc1f7154bd3b28040e9`

````python
"""Permission Risks functional package."""

````

