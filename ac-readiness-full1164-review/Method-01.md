# 实际运行源码完整分段

完整文件按原路径列出，哈希指原文件字节。

## runtime/common.py

SHA-256 `cc6b8f04edbcecb3a5bfa5e758ca888c88b7d86dce23d7345ef8dd1f9380dcc3`

```python
from pathlib import Path
import json,hashlib,sys
R=Path(__file__).resolve().parents[1]
SOURCE=R/'source'
sys.path[:0]=[str(SOURCE/'src'),str(SOURCE/'runtime')]
from pr_next_joint.core import digest
from pr_next_joint.investigation.contracts import write
ROUND='ac_readiness_full1164_r1'
def read(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def wire(messages):return {'model':'deepseek-flash','messages':messages,
 'response_format':{'type':'json_object'},'thinking':{'type':'enabled'},
 'reasoning_effort':'high','stream':False,'max_tokens':32768}
def safe_error(e):return type(e).__name__+':'+digest(str(e))


def runtime_versions():
    from importlib.metadata import version
    from Crypto.Hash import keccak
    from eth_keys.datatypes import Signature
    import tokenizers, z3
    required = dict(line.strip().split('==') for line in (SOURCE/'requirements.txt').read_text().splitlines() if line.strip())
    versions = {name:version(name) for name in required}
    if sys.version_info < (3,11) or versions != required:
        raise ValueError('existing_runtime_dependency_identity_changed')
    return versions

def member_wall_seconds(plan, configuration):
    options = configuration['options']
    seconds = (options['seconds'] + options['attempt_limit'] * plan['member_api_timeout_seconds']
               + plan['member_save_allowance_seconds'])
    if seconds != plan['sample_hard_seconds'] or plan['member_api_timeout_seconds'] != 1800:
        raise ValueError('member_deadline_and_method_config_disagree')
    return seconds

```

## runtime/input_links.py

SHA-256 `b126ceba835af33e1cf9532bd58f007f2c9ec6a7ac3c2d095005b6f609ca8478`

```python
"""Use precisely the fixed locally pinned compilation identities checked against instance files on launch; no compiler or Gold."""
from pathlib import Path
from common import R,SOURCE,read,write,sha,digest

def source_identity():
 actual={p.relative_to(SOURCE/'src/pr_next_joint').as_posix():sha(p) for p in sorted((SOURCE/'src/pr_next_joint').rglob('*.py'))}
 identity=read(R/'IDENTITY.json')
 if actual!=read(R/'METHOD_SHA.json') or digest(actual)!=identity['method_sha256'] or len(actual)!=identity['method_python_files']:
  raise ValueError('frozen_successor_method_identity')
 if sha(R/'METHOD_CONFIG.json')!=identity['config_sha256'] or sha(SOURCE/identity['active_config'])!=identity['config_sha256'] or sha(SOURCE/'configs/full.json')!=identity['previous_full_config_sha256']:
  raise ValueError('frozen_successor_config_identity')
 for n,h in read(R/'SOURCE_AUX.json')['bridge_files'].items():
  if sha(SOURCE/'runtime'/n)!=h:raise ValueError('source_auxiliary_identity:'+n)
 return {'method':digest(actual),'files':len(actual),'config':sha(R/'METHOD_CONFIG.json')}

def prepare_links():
 rows=read(R/'INPUTS.json');groups=read(R/'MEMBERS.json');jobs={}
 if set(rows)!=set(groups['SmartBug']+groups['JANUS']) or len(rows)!=len(read(R/'PLAN.json')['execution_order']):raise ValueError('frozen_roster_identity')
 for member,row in rows.items():
  root=Path(row['root']).resolve();p=Path(row['descriptor']).resolve()
  if not p.is_relative_to(root) or sha(p)!=row['descriptor_sha256']:raise ValueError('descriptor_identity:'+member)
  spec=read(p)
  if spec['input_id']!=member or spec.get('description') or set(spec['artifacts'])!={'ProgramBundle.json','native_ssa.json','standard-input.json','standard-output.json','extract_receipt.json'}:raise ValueError('neutral_compilation_identity:'+member)
  for ref in spec['artifacts'].values():
   q=(root/ref['path']).resolve()
   if not q.is_relative_to(root) or not q.is_file() or sha(q)!=ref["sha256"]:raise ValueError('missing_compilation:'+member)
  jobs[member]={k:row[k] for k in ('root','descriptor','task','expected')}
 dest=R/'run/JOBS.json'
 if dest.exists() and read(dest)!=jobs:raise ValueError('existing_jobs_identity_changed')
 if not dest.exists():write(dest,jobs)
 return jobs

def tokenizer():
 from reference_counter import Counter
 pins=read(R/'SOURCE_AUX.json')['tokenizer_files']
 for name in [R/'tokenizer',*read(R/'PLAN.json')['tokenizer_candidates']]:
  d=Path(name)
  if all((d/n).is_file() and sha(d/n)==h for n,h in pins.items()):
   Counter(d)
   return {'path':str(d),'files':pins,'representation_changed':False}
 raise ValueError('existing_pinned_tokenizer_missing_no_install')

```

## runtime/ledger.py

SHA-256 `e43fabb1c3b749bf4523bead2b67512e2ada9769990f7bbfffb280941168f824`

```python
"""Atomic request COUNTS and actual usage; no money reservations or wait queues."""
import sqlite3,json,time
from pathlib import Path
from common import read

class Ledger:
    def __init__(self,path):self.path=Path(path)
    def connect(self):
        c=sqlite3.connect(self.path,timeout=30);c.row_factory=sqlite3.Row;return c
    def initialize(self,grant,simulated=False):
        self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.connect() as c:
            c.execute('PRAGMA journal_mode=WAL')
            c.execute('CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY,v TEXT)')
            c.execute('CREATE TABLE IF NOT EXISTS requests(member TEXT,idx INTEGER,body_sha TEXT,state TEXT,simulated INTEGER,input_tokens INTEGER,submitted REAL,usage TEXT,upper_usd REAL,lower_usd REAL,model TEXT,error TEXT,PRIMARY KEY(member,idx))')
            if c.execute("SELECT 1 FROM meta WHERE k='grant'").fetchone():raise ValueError('existing_ledger_preserved_use_resume')
            for k,v in {'grant':grant,'simulated':bool(simulated),'halt':''}.items():c.execute('INSERT INTO meta VALUES(?,?)',(k,json.dumps(v)))
    def meta(self,k):
        with self.connect() as c:
            r=c.execute('SELECT v FROM meta WHERE k=?',(k,)).fetchone()
            return json.loads(r[0]) if r else None
    def halt(self,reason):
        with self.connect() as c:
            c.execute('BEGIN IMMEDIATE')
            old=c.execute("SELECT v FROM meta WHERE k='halt'").fetchone()
            if old and json.loads(old[0]):return
            c.execute("INSERT OR REPLACE INTO meta VALUES('halt',?)",(json.dumps(reason),))
    def row(self,member,index):
        with self.connect() as c:
            r=c.execute('SELECT * FROM requests WHERE member=? AND idx=?',(member,index)).fetchone()
            return dict(r) if r else None
    def dispatch(self,member,index,body_sha,input_tokens,simulated):
        with self.connect() as c:
            c.execute('BEGIN IMMEDIATE')
            old=c.execute('SELECT * FROM requests WHERE member=? AND idx=?',(member,index)).fetchone()
            if old:
                if old['body_sha']!=body_sha:raise ValueError('saved_request_identity_changed')
                if old['state']=='settled':return False
                raise ValueError('request_inflight_or_unknown_no_automatic_resend')
            meta={r['k']:json.loads(r['v']) for r in c.execute('SELECT * FROM meta')};g=meta['grant']
            if meta['halt']:raise ValueError('new_dispatch_stopped:'+meta['halt'])
            if time.time()>=g['deadline_epoch']:raise ValueError('original_full_deadline')
            if member not in g['members'] or index not in (0,1):raise ValueError('member_or_attempt_identity')
            n=c.execute('SELECT COUNT(*) FROM requests').fetchone()[0]
            k=c.execute('SELECT COUNT(*) FROM requests WHERE member=?',(member,)).fetchone()[0]
            if n>=g['max_requests'] or k>=g['per_member_max']:raise ValueError('request_count_limit')
            if index==1:
                first=c.execute('SELECT state FROM requests WHERE member=? AND idx=0',(member,)).fetchone()
                if not first or first[0]!='settled':raise ValueError('first_request_not_settled')
            if g['max_requests']*0.049152>g['max_usd']:raise ValueError('whole_batch_bound_not_covered')
            if type(input_tokens)is not int or not 0<=input_tokens<=32768:raise ValueError('input_capacity_before_dispatch')
            paid=c.execute('SELECT COALESCE(SUM(upper_usd),0) FROM requests WHERE simulated=0').fetchone()[0]
            if paid>=g['max_usd']:raise ValueError('settled_budget_limit')
            c.execute('INSERT INTO requests(member,idx,body_sha,state,simulated,input_tokens,submitted) VALUES(?,?,?,?,?,?,?)',
                (member,index,body_sha,'sent',int(simulated),input_tokens,time.time()))
        return True
    def settle(self,member,index,usage,upper,lower,model,halt=None):
        with self.connect() as c:
            c.execute('BEGIN IMMEDIATE')
            c.execute("UPDATE requests SET state='settled',usage=?,upper_usd=?,lower_usd=?,model=? WHERE member=? AND idx=?",
                (json.dumps(usage),upper,lower,model,member,index))
            if halt:c.execute("UPDATE meta SET v=? WHERE k='halt'",(json.dumps(halt),))
    def unknown(self,member,index,error):
        with self.connect() as c:
            c.execute('BEGIN IMMEDIATE')
            c.execute("UPDATE requests SET state='unknown',error=? WHERE member=? AND idx=? AND state!='settled'",(error,member,index))
            # Network-unknown slots remain charged at their worst case; other members continue.
    def recover(self):
        # Run only after the supervisor lock is acquired and old writers ended.
        with self.connect() as c:
            c.execute('BEGIN IMMEDIATE')
            n=c.execute("SELECT COUNT(*) FROM requests WHERE state='sent'").fetchone()[0]
            if n:
                c.execute("UPDATE requests SET state='unknown',error='interrupted_after_send_intent' WHERE state='sent'")
                # Unknown slots are preserved and never resent; unused members may continue.
    def resume_user_stop(self):
        with self.connect() as c:
            c.execute('BEGIN IMMEDIATE')
            halted=json.loads(c.execute("SELECT v FROM meta WHERE k='halt'").fetchone()[0])
            unknown=c.execute("SELECT COUNT(*) FROM requests WHERE state IN ('sent','unknown')").fetchone()[0]
            if halted=='user_stop':c.execute("UPDATE meta SET v=? WHERE k='halt'",(json.dumps(''),))
    def snapshot(self,member=None):
        with self.connect() as c:
            rows=[dict(r) for r in c.execute('SELECT * FROM requests'+(' WHERE member=?' if member else ''),((member,) if member else ()))]
        real=[r for r in rows if not r['simulated']];settled=[r for r in rows if r['state']=='settled']
        usages=[json.loads(r['usage']) for r in settled if r['usage']]
        return {'requests':len(rows),'real_model_calls':len(real),'simulated_service_requests':len(rows)-len(real),
          'unknown_or_inflight_upper_usd':sum(r['state'] in ('sent','unknown') and not r['simulated'] for r in rows)*0.049152,
          'unknown_cost_upper_usd':sum(r['state']=='unknown' and not r['simulated'] for r in rows)*0.049152,
          'inflight':sum(r['state']=='sent' for r in rows),'unknown':sum(r['state']=='unknown' for r in rows),
          'settled_cost_usd_upper':sum(r['upper_usd'] for r in settled if not r['simulated']),
          'settled_cost_usd_lower':sum(r['lower_usd'] for r in settled if not r['simulated']),
          'simulated_cost_usd_upper':sum(r['upper_usd'] for r in settled if r['simulated']),
          'prompt_tokens':sum(u['prompt_tokens'] for u in usages),'completion_tokens':sum(u['completion_tokens'] for u in usages),
          'usage_records':usages,'service_models':sorted({r['model'] for r in settled if r['model']}),
          'actual_provider_billed_usd':None,'cost_basis':'actual usage × public peak/off-peak prices; not supplier invoice',
          'per_request_money_reservation':False,'halt':self.meta('halt'),
          'nature':'real_service' if real else 'zero_actual_calls',
          'unknown_fee_is_not_zero':True}

```

## runtime/live_client.py

SHA-256 `d85c3e1be02a42cb367a7bca6dea7b4cc88ae994f00bd0202e6426417e7cdeda`

```python
"""Pinned HTTP contract, body digests and shared count/usage ledger."""
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

def refresh_service(run):
    import fcntl
    folder=Path(run)/'service'
    with (folder/'refresh.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        current=read(folder/'SERVICE_ACTUAL.json')
        if time.time()-current['epoch']<82800:
            return
        history=folder/'rechecks'/str(time.time_ns())
        observed=verify_service(history)
        write(folder/'SERVICE_ACTUAL.json',observed)

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
            # The locked service recheck runs before each new ledger dispatch.
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
        if not self.simulated:
            try:refresh_service(self.run)
            except Exception:
                self.ledger.halt('service_identity_recheck_failed')
                raise
        body=wire(messages);body_sha=digest(body);out=self.run/'requests'/self.case_id/str(index);out.mkdir(parents=True,exist_ok=True)
        existing=self.ledger.row(self.case_id,index)
        if existing:
            if existing['body_sha']!=body_sha:raise ValueError('saved_request_identity_changed')
            # No durable response body exists in this version. A settled
            # request must not be submitted again after an interrupted worker.
            if existing['state']=='settled':
                raise ValueError('settled_response_not_retained_no_automatic_replay_or_resend')
            raise ValueError('unknown_or_inflight_request_preserved_no_resend')
        write(out/'intent.json',{'body_retained':False,'body_sha256':body_sha,'messages_sha256':digest(messages),
            'host_program_identity':self.program_identity,'offline_input_tokens':count,'simulated':self.simulated})
        self.ledger.dispatch(self.case_id,index,body_sha,count,self.simulated)
        raw=None
        try:
            raw=self.sender(body,max(.001,min(1800,self.grant['deadline_epoch']-time.time())))
            raw_digest=__import__('hashlib').sha256(raw).hexdigest()
            write(out/'response_body_receipt.json',{'sha256':raw_digest,'bytes':len(raw),'body_retained':False})
            response=json.loads(raw)
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
                'replayed_from_saved_response':False,'raw_http_sha256':raw_digest,'response_body_retained':False}
            write(out/'receipt.json',receipt);return content,receipt
        except BaseException as error:
            if raw is None and hasattr(error,'saved_body'):write(out/'http_error_receipt.json',{'sha256':__import__('hashlib').sha256(error.saved_body).hexdigest(),'bytes':len(error.saved_body),'body_retained':False})
            state=self.ledger.row(self.case_id,index)
            if state and state['state']!='settled':self.ledger.unknown(self.case_id,index,safe_error(error))
            network_unknown=raw is None and isinstance(error,(TimeoutError,ConnectionError,urllib.error.URLError)) and not isinstance(error,urllib.error.HTTPError)
            if not network_unknown and (not state or state['state']!='settled'):self.ledger.halt('service_or_cost_contract:'+safe_error(error))
            write(out/'error.json',{'error':safe_error(error),'epoch':time.time(),
                'simulated':self.simulated,'accounting':self.attempt_record(index)})
            raise

```

## runtime/start.py

SHA-256 `0254bc18325b764502845062721f551bdc4cc271f9418b59d04d6df19762861f`

```python
"""Chat-authorized, user-started Full1164; reuse environment, detached supervisor."""
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
 if not (R/'PREP_READY.json').is_file() or read(R/'PREP_READY.json')['manifest']!=sha(R/'MANIFEST.json'):
  raise ValueError('missing_current_instance_readiness')
 if read(R/'OFFLINE_GATE.json').get('allow_paid_launch_after_explicit_authorization') is not True:
  raise ValueError('offline_engineering_gate_not_released')
 if (v.get('authorized') is not True or v.get('round')!='ac_readiness_full1164_r1'
  or v.get('run_id')!=read(R/'PLAN.json')['run_id'] or R.name!=v['run_id']
  or v.get('limits')!=read(R/'PLAN.json')['limits']
  or v.get('instance_fee_cny_limit')!=read(R/'PLAN.json')['instance_fee_cny_limit']
  or v.get('total_activity_seconds')!=read(R/'PLAN.json')['all_instance_activity_seconds']
  or v.get('instance_max_hourly_cny')!=read(R/'PLAN.json')['instance_max_hourly_cny_at_full_time']
  or v.get('group')!='Full_only' or v.get('source')!='explicit_user_current_chat'
  or v.get('implementation_sha256')!=read(R/'IDENTITY.json')['method_sha256']
  or v.get('config_sha256')!=sha(R/'METHOD_CONFIG.json')
  or v.get('prep_seconds')!=read(R/'PLAN.json')['prep_seconds']
  or v.get('collection_seconds')!=read(R/'PLAN.json')['collection_seconds']
  or v.get('package_manifest_sha256')!=sha(R/'MANIFEST.json')):
  raise ValueError('specific_chat_approval_or_package_identity')
 if read(R/'PLAN.json').get('prep_already_used_seconds') is None and not (OUT/'PREPARATION.json').exists():
  raise ValueError('existing_preparation_usage_not_bound_to_local_receipt')
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
 check="import sys;sys.path.insert(0,sys.argv[1]);from common import runtime_versions;runtime_versions()"
 errors=[]
 for name in dict.fromkeys(choices):
  if not Path(name).is_file():continue
  p=subprocess.run([name,'-B','-c',check,str(R/'runtime')],capture_output=True,text=True,timeout=30)
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

def workers_active(root):
    for path in Path('/proc').glob('[0-9]*/cmdline'):
        try:args=path.read_bytes().split(b'\0')
        except (FileNotFoundError,ProcessLookupError,PermissionError):continue
        if str(root/'runtime/worker.py').encode() in args:return True
    return False

def launch(resume=False):
 import fcntl
 OUT.mkdir(exist_ok=True)
 lock=(OUT/'START_LOCK').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 checklock=(OUT/'SUPERVISOR_LOCK').open('a')
 try:fcntl.flock(checklock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 except BlockingIOError:
  print('本批后台仍在运行；自动进入进度显示，不重复启动。',flush=True);view();return
 finally:checklock.close()
 if workers_active(R):raise ValueError('previous_workers_still_active_no_redispatch')
 for item in read(R/'MANIFEST.json')['files']:
  p=R/item['path']
  if not p.is_file() or sha(p)!=item['sha256']:raise ValueError('package_file_identity:'+item['path'])
 approved=approval()
 if not resume and (OUT/'AUTHORIZATION.json').exists():
  print('本批已有运行记录；请用--follow查看，异常恢复使用--resume。',flush=True);return
 sys.path.insert(0,str(R/'runtime'))
 from common import runtime_versions,member_wall_seconds
 from input_links import source_identity,prepare_links,tokenizer
 from ledger import Ledger
 from live_client import verify_service
 dependencies=runtime_versions()
 wall_limit=member_wall_seconds(read(R/'PLAN.json'),read(R/'METHOD_CONFIG.json'))
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
  'used_seconds':read(R/'PLAN.json')['prep_already_used_seconds']+read(R/'PREP_USED.json')['seconds']+read(R/'PLAN.json').get('upload_seconds_ceiling',0),
  'initial_time_basis':'batch-specific instance setup time; manual upload separate, no prior inventory time attributed','runs':[]}
 if prep['used_seconds']>=approved['prep_seconds']:raise ValueError('preparation_allowance_exhausted')
 prep_deadline=BOOT_EPOCH+max(0,approved['prep_seconds']-prep['used_seconds'])
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
  if resume and (OUT/'service/SERVICE_ACTUAL.json').exists() and time.time()-read(OUT/'service/SERVICE_ACTUAL.json')['epoch']<82800:
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
  grant={'run_id':read(R/'PLAN.json')['run_id'],'round':'ac_readiness_full1164_r1','authorized':True,'group':'Full_only','members':ids,
   'max_requests':approved['limits']['requests'],'per_member_max':approved['limits']['per_member'],'max_usd':approved['limits']['usd'],'wall_seconds':approved['limits']['Full_seconds'],
   'start_epoch':now,'deadline_epoch':now+approved['limits']['Full_seconds'],'input_root':str(R),
   'package_manifest_sha256':sha(R/'MANIFEST.json'),'source':'explicit user approval in current chat',
   'chat_approval_sha256':sha(R/'CHAT_APPROVAL.json'),'implementation_sha256':approved['implementation_sha256'],'config_sha256':approved['config_sha256'],
   'history':'HISTORY.json; old unknown and billed-use records not reset or spent as new allowance'}
  if now>=grant['deadline_epoch']:raise ValueError('original_full_deadline_expired')
  grant['prior_usage']={k:v for k,v in read(R/'HISTORY.json').items() if k in ('previous_cumulative_requests','previous_cumulative_usd_upper','provider_unsettled_by_reference','sha256')}
  assert grant['max_requests']*.049152<=grant['max_usd']
  save(OUT/'AUTHORIZATION.json',grant);Ledger(OUT/'requests.sqlite').initialize(grant)
 identity={'run_id':read(R/'PLAN.json')['run_id'],'source':source,'runtime':{p.name:sha(p) for p in (R/'runtime').glob('*.py')},
  'inputs_sha256':sha(R/'INPUTS.json'),'jobs_sha256':sha(OUT/'JOBS.json'),'config_sha256':sha(R/'METHOD_CONFIG.json'),
  'plan_sha256':sha(R/'PLAN.json'),'chat_approval_sha256':sha(R/'CHAT_APPROVAL.json'),
  'manifest_sha256':sha(R/'MANIFEST.json'),'service':service,'python':sys.executable,
  'model_parameters':{'model':'deepseek-flash','thinking':{'type':'enabled'},'reasoning_effort':'high','max_tokens':32768},
  'dependency_versions':dependencies,'member_hard_seconds':wall_limit,'method_config_unchanged_live_grant_checked_by_external_factory':True,'no_Gold':True,'no_scoring':True}
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

```

## runtime/supervisor.py

SHA-256 `dfe213ab2336d19af8a4ecd4940e7700619d7ccdb73562db3297760f209f79d3`

```python
"""User-started, self-contained Full1164 supervisor. No Gold or scoring imports."""
from pathlib import Path
import os,sys,time,signal,subprocess,shutil,traceback,json
from common import R,SOURCE,ROUND,read,write,sha,safe_error,member_wall_seconds
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
    member_hard=member_wall_seconds(plan,read(R/'METHOD_CONFIG.json'))
    started=grant['start_epoch'];deadline=grant['deadline_epoch'];cause='normal_completion';full_size=0;resource_clock=0
    def signal_stop(*args):(out/'STOP').touch()
    signal.signal(signal.SIGTERM,signal_stop);signal.signal(signal.SIGINT,signal_stop)
    def known_result(member):
        p=out/'members'/member/'FINAL_ENTRY.json'
        if p.exists():return read(p)
        # Never redispatch a member after a possible submission or an interrupted attempt.
        home=p.parent
        if home.is_dir() or ledger.snapshot(member)['real_model_calls']:
            result={'member':member,'interrupted':True,'technical_error':'interrupted_no_automatic_resend','not_a_safe_prediction':True}
            reports=sorted(home.glob('attempt_*/analysis/report.json'))
            if len(reports)==1:
                result=recover_report(member,reports[0].parents[1],tasks[member],None)
                result['attempt_directory']=str(reports[0].parents[1])
            write(p,result);return result
        return None
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
        for phase,group in [('first_six',first),('SmartBug',[m for m in members['SmartBug'] if m not in first]),('JANUS',[m for m in members['JANUS'] if m not in first])]:
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
                    member_deadline=min(deadline,time.time()+member_hard)
                    cmd=[sys.executable,'-B',str(R/'runtime/worker.py'),'--member',member,'--task',tasks[member],'--member-deadline-epoch',str(member_deadline),
                        '--inputs',grant['input_root'],'--out',str(attempt),'--run',str(out)]
                    env=dict(os.environ,PYTHONPATH=os.pathsep.join([str(R/'runtime'),str(SOURCE/'src'),str(SOURCE/'runtime')]),
                        PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8',TOKENIZERS_PARALLELISM='false')
                    p=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL,env=env,start_new_session=True)
                    active[member]=(p,log,{'attempt':str(attempt),'start':now,'number':n,'deadline_epoch':member_deadline})
                for member,(p,log,info) in list(active.items()):
                    timed_out=False
                    if p.poll() is None:
                        if now<info['deadline_epoch']:continue
                        timed_out=True
                        kill(p)
                    log.close();del active[member];entry=Path(info['attempt'])/'ENTRY_RESULT.json'
                    result=read(entry) if entry.exists() else recover_report(member,Path(info['attempt']),tasks[member],p.returncode)
                    if timed_out:
                        result.update(stop_reason='member_wall_deadline',deadline_epoch=info['deadline_epoch'],not_a_safe_prediction=True)
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
        write(out/'RESULTS.json',[results[m] for m in plan['execution_order']])
        frozen={n:sha(out/n) for n in ('RESULTS.json','RUN_IDENTITY.json','JOBS.json','AUTHORIZATION.json')}
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

```

## runtime/worker.py

SHA-256 `f5052930ad1296e4fddb53af42bb39260902b356cccaf574627e7041d6e0456a`

```python
"""One isolated member; the approved CLI intake/engine/feedback/report pipeline."""
from pathlib import Path
from types import SimpleNamespace
import os,sys,time,traceback
from common import R,SOURCE,read,write,safe_error,sha,runtime_versions,member_wall_seconds
from live_client import Client
from pr_next_joint.investigation.cli import run

def execute(member,task,input_root,out,run_root,*,sender=None,simulated=False,engineering=None,target=None,member_deadline_epoch=None):
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
        grant=read(Path(run_root)/'AUTHORIZATION.json')
        identity=read(Path(run_root)/'RUN_IDENTITY.json')
        if runtime_versions()!=identity['dependency_versions'] or sha(R/'METHOD_CONFIG.json')!=grant['config_sha256']:
            raise ValueError('worker_dependency_or_configuration_changed')
        maximum=member_wall_seconds(read(R/'PLAN.json'),read(R/'METHOD_CONFIG.json'))
        now=time.time()
        deadline_epoch=min(now+maximum,grant['deadline_epoch'])
        if member_deadline_epoch is not None:
            deadline_epoch=min(deadline_epoch,member_deadline_epoch)
        remaining=deadline_epoch-now
        if remaining<=0:raise ValueError('worker_deadline_expired_before_analysis')
        report=run(args,client_factory=factory,deadline=time.monotonic()+remaining)
        gaps=bool(report['diagnostics']['program_gaps'] or report['diagnostics']['unexecuted_actions'] or
                  report['diagnostics']['issues'] or report['unresolved_category_judgments'])
        result={'member':member,'task':task,'report_saved':True,'analysis_available':report['model_analysis_available'],
            'with_gaps':gaps,'findings':len(report['findings']),'usage':report['usage'],
            'report':str(out/'analysis/report.json'),'prediction_manifest':str(out/'analysis/prediction_manifest.json'),
            'report_sha256':sha(out/'analysis/report.json'),'real_model_validation':not simulated}
    except BaseException as error:
        out.mkdir(parents=True,exist_ok=True)
        write(out/'ENTRY_ERROR.json',{'error':safe_error(error),'traceback_sha256':__import__('hashlib').sha256(traceback.format_exc().encode()).hexdigest(),'not_a_safe_prediction':True})
        result={'member':member,'task':task,'report_saved':False,'technical_error':type(error).__name__,
                'technical_error_group':safe_error(error).replace(member,'<member>'),
                'detail':safe_error(error),'partial_files_preserved':True,'not_a_safe_prediction':True}
    write(out/'ENTRY_RESULT.json',result);return result

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--member',required=True);p.add_argument('--task',choices=['AC','FCR'],required=True)
    p.add_argument('--member-deadline-epoch',type=float,required=True);p.add_argument('--inputs',required=True);p.add_argument('--out',required=True);p.add_argument('--run',required=True)
    a=p.parse_args();r=execute(a.member,a.task,a.inputs,a.out,a.run,member_deadline_epoch=a.member_deadline_epoch)
    print('成员结束：'+a.member+'；报告已保存' if r['report_saved'] else '成员技术异常：'+a.member,flush=True)
    raise SystemExit(0 if r['report_saved'] else 1)

```

## source/configs/full.json

SHA-256 `2ab0557132adf3b6c12a145ab9cef71bc1b1ef39d5cdc5f76bf8660d5e2ca783`

```json
{
  "method": "permission-risks-sp200-simplification-r2",
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
  "notes": "Source-scoped observations, phase-bound semantic decisions and shared mathematical evidence. Decision-only public output."
}

```

## source/configs/full_expanded_900s_20s.json

SHA-256 `40ca33d909fef65652dd9e956d33639b05adb464dd2c7f0a82c140e8d421c7c4`

```json
{
  "method": "permission-risks-sp200-simplification-r2",
  "options": {
    "feedback": true,
    "attempt_limit": 2,
    "max_paths": 96,
    "prefix_depth": 2,
    "max_prefixes": 64,
    "max_actions": 256,
    "seconds": 900,
    "solver_timeout_ms": 20000,
    "input_target": 16384,
    "input_limit": 32768,
    "output_limit": 32768
  },
  "live_model_authorized": false,
  "notes": "Expanded full-population compute profile; early exit, bounded search and two service opportunities."
}

```

## source/configs/full_extended_300s_5s.json

SHA-256 `94bf6ea8bb21efb26e63c0f43d476382e5e87ad4b90fdfbe891ea18843dbc898`

```json
{
  "method": "permission-risks-sp200-simplification-r2",
  "options": {
    "feedback": true,
    "attempt_limit": 2,
    "max_paths": 48,
    "prefix_depth": 2,
    "max_prefixes": 24,
    "max_actions": 64,
    "seconds": 300,
    "solver_timeout_ms": 5000,
    "input_target": 16384,
    "input_limit": 32768,
    "output_limit": 32768
  },
  "live_model_authorized": false,
  "notes": "RecallFocused R2 prospective extended computational profile: 300 program seconds and 5000 ms per solver check; old semantic/search/model bounds retained. Requires Options maximum validation update and scoped offline calibration before use. No live run authorized by this file."
}

```

## source/requirements-dev.txt

SHA-256 `ac3b9daad7613d985567e0c2eed70660e78729ecd1d49484b2952a6e92c6e505`

```text
-r requirements.txt
pytest==8.3.5

```

## source/requirements-frontend.txt

SHA-256 `a2a3fa701ade8c2545e557d2ba11c7c35a7ed799e5d295c863df8913215292b2`

```text
-r requirements.txt
slither-analyzer==0.11.3
crytic-compile==0.3.11
solc-select==1.2.0

```

## source/requirements.txt

SHA-256 `ae9a4281cb7d9c9b64571b1628ce17e38607293893567849800bc675d0eafa9c`

```text
z3-solver==4.15.3.0
eth-keys==0.7.0
pycryptodome==3.24.1
tokenizers==0.22.2

```

## source/runtime/batch.py

SHA-256 `2e504de54a17a74f2a27f3168c29016a6846b92c5c03013da463e01fc4d39073`

```python
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

```

## source/runtime/bridge.py

SHA-256 `2d4b2b06e2aa9db2e17eb0c20b0a77c1b61bb853a80ced203166d213daa77589`

```python
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

```

## source/runtime/reference_counter.py

SHA-256 `557b0bd400a453dbeb5ed46bf1295f244df35ded934331f73bdf09a2bd87dc8e`

```python
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

```

## source/scripts/extract_compiler_facts.py

SHA-256 `387d9702a684d35743b0fac1c9a25ae32175fa04da8b718b166c666be6291eb0`

```python
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

```

## source/scripts/run_batch.py

SHA-256 `ce7036469d7829783a3b06015ad22314943ce839536bad42b4a42addd773f332`

```python
from pathlib import Path
import sys
root=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(root/'src'),str(root/'runtime')]
from batch import main
if __name__=='__main__':raise SystemExit(main())

```

## source/scripts/run_method.py

SHA-256 `89be133ca282f1d3976122cc20cd2baf5dbda35e8899cdc5e50657122067df2d`

```python
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from pr_next_joint.investigation.cli import main
if __name__=='__main__':raise SystemExit(main())

```

## source/src/pr_next_joint/__init__.py

SHA-256 `9972949b00e2339c426220c3f6157d53150928f138b0ac6af3133f0e86e9fd61`

```python
"""Permission Risks: source facts, semantic selection and shared verification."""
__version__ = "decision-only-2.0"
VERSION = 'source-semantic-investigation-r1'
IMPLEMENTATION_PATCH = 'decision-only-r2'
# Historic low-level evidence schema is retained for existing proof artifacts.
SCHEMA_VERSION = 'pr-next-task-b-r2-c1-v1'

```

## source/src/pr_next_joint/__main__.py

SHA-256 `8c1de7da674c56d218ac33d0cdeeca6b3a301ea16ca625d1cc2bbccf4d65ce4c`

```python
from .refinement.cli import main
raise SystemExit(main())

```

## source/src/pr_next_joint/checks/access/__init__.py

SHA-256 `87e3e2f1dba261e0999d37d622e45825e4d2763d9091aa860663f27df53e5d17`

```python
"""Source analysis helpers retained by SCRV."""

```

## source/src/pr_next_joint/checks/access/code_control.py

SHA-256 `f64adc544f2048c65e061ea919347b1d9cecef2e5e0102ee772a637cc93346cf`

```python
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

```

## source/src/pr_next_joint/checks/access/credential_lifecycle.py

SHA-256 `5a0941251ef82663945d16d65a0d6e617b616afeec9f652ce5131a8e17cffc0e`

```python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""


def leaves(write):
    value=write['value']
    if value.get('kind')=='record':
        for field in value['fields']:
            yield from leaves({**write,'path':{**write['path'],'segments':write['path']['segments']+[{'field':field['field']}]},'value':field['value']})
    else:yield write

```

## source/src/pr_next_joint/checks/access/destruction.py

SHA-256 `a9ca610a50590a7d9e3ec13ab69fa51e89b9cea294a08b053ecde124d1129777`

```python
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

```

## source/src/pr_next_joint/checks/access/shared_policy.py

SHA-256 `ea22aded277efa748cf520b36577781ceb523c4775515a0bfb39f78776294af9`

```python
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

```

## source/src/pr_next_joint/checks/credentials/__init__.py

SHA-256 `87e3e2f1dba261e0999d37d622e45825e4d2763d9091aa860663f27df53e5d17`

```python
"""Source analysis helpers retained by SCRV."""

```

## source/src/pr_next_joint/checks/credentials/credential_encoding.py

SHA-256 `7b51447cbd9017a621842296cd03caaaf4a75773b58bdaade17187df8f3788ab`

```python
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

```

## source/src/pr_next_joint/core.py

SHA-256 `6e85487fc5deef2119dbf6f9cea15bf9808a068b4d83c858a89f721448178741`

```python
"""Content identities, typed observation expressions and finite-query semantics."""
import hashlib,json,re
from . import SCHEMA_VERSION

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def digest(value):return hashlib.sha256(canonical(value)).hexdigest()
def ref(value):return {'id':value.get('id',digest(value)),'sha256':digest(value)}
class Invalid(ValueError):pass

def require(ok,reason):
 if not ok:raise Invalid(reason)


```

## source/src/pr_next_joint/frontend/__init__.py

SHA-256 `a9ecbc4f75a0298e4a1f82edab901936fe49977cdd1a2bc1f7154bd3b28040e9`

```python
"""Permission Risks functional package."""

```

## source/src/pr_next_joint/frontend/assembly.py

SHA-256 `6624384a6498a7846b03418859e3949e102778954902c667107a30c454fde792`

```python
"""Narrow, compiler-bound summary of terminal delegate forwarding assembly.
This recognizes invocation and termination only, never arbitrary callee effects.
Unrecognized assembly retains the existing unsupported path diagnostic.
"""
import copy,re
from pr_next_joint.frontend.path_ir import lit

_IDENT=r'[A-Za-z_$][A-Za-z0-9_$]*'
_PATTERN=re.compile(
 r'\{let(?P<result>'+_IDENT+r'):=delegatecall\((?:sub\(gas(?:\(\))?,(?P<reserve>0x[0-9a-fA-F]+|[0-9]+)\)|gas(?:\(\))?),'
 r'(?P<dst>'+_IDENT+r'),add\((?P<data>'+_IDENT+r'),(?:0x20|32)\),mload\((?P=data)\),0,0\)'
 r'let(?P<size>'+_IDENT+r'):=returndatasize(?:\(\))?let(?P<ptr>'+_IDENT+r'):=mload\((?:0x40|64)\)'
 r'returndatacopy\((?P=ptr),0,(?P=size)\)switch(?P=result)case0\{revert\((?P=ptr),(?P=size)\)\}'
 r'default\{return\((?P=ptr),(?P=size)\)\}\}')


_BYTES_PATTERN=re.compile(
 r'\{let(?P<result>'+_IDENT+r'):=delegatecall\((?:sub\(gas(?:\(\))?,(?P<reserve>0x[0-9a-fA-F]+|[0-9]+)\)|gas(?:\(\))?),'
 r'(?P<dst>'+_IDENT+r'),add\((?P<data>'+_IDENT+r'),(?:0x20|32)\),mload\((?P=data)\),0,0\)'
 r'let(?P<size>'+_IDENT+r'):=returndatasize(?:\(\))?(?P<ptr>'+_IDENT+r'):=mload\((?:0x40|64)\)'
 r'mstore\((?:0x40|64),add\((?P=ptr),and\(add\(add\((?P=size),(?:0x20|32)\),(?:0x1f|31)\),not\((?:0x1f|31)\)\)\)\)'
 r'mstore\((?P=ptr),(?P=size)\)returndatacopy\(add\((?P=ptr),(?:0x20|32)\),0,(?P=size)\)'
 r'switchiszero\((?P=result)\)case1\{revert\(add\((?P=ptr),(?:0x20|32)\),(?P=size)\)\}\}')

def bound_reference(n,name,lookup):
    refs=n.get('externalReferences',[])
    if isinstance(refs,dict):refs=list(refs.values())
    refs=[x for r in refs for x in ([r] if 'declaration' in r else r.values())]
    ids={r.get('declaration') for r in refs if not r.get('isSlot') and not r.get('isOffset')
         and lookup.nodes.get(r.get('declaration'),{}).get('name')==name}
    return next(iter(ids)) if len(ids)==1 else None

def yul_text(node):
    """Serialize only the compiler Yul syntax accepted by the exact matcher."""
    kind=node.get('nodeType')
    if kind=='YulBlock':return '{'+''.join(yul_text(x) for x in node['statements'])+'}'
    if kind in ('YulIdentifier','YulTypedName'):return node['name']
    if kind=='YulLiteral' and node.get('kind')=='number':return node['value']
    if kind=='YulFunctionCall':return yul_text(node['functionName'])+'('+','.join(yul_text(x) for x in node['arguments'])+')'
    if kind=='YulAssignment' and len(node['variableNames'])==1:
        return yul_text(node['variableNames'][0])+':='+yul_text(node['value'])
    if kind=='YulExpressionStatement':return yul_text(node['expression'])
    if kind=='YulVariableDeclaration' and len(node['variables'])==1 and node.get('value'):
        return 'let'+yul_text(node['variables'][0])+':='+yul_text(node['value'])
    if kind=='YulSwitch':return 'switch'+yul_text(node['expression'])+''.join(yul_text(x) for x in node['cases'])
    if kind=='YulCase':return ('default' if node['value']=='default' else 'case'+yul_text(node['value']))+yul_text(node['body'])
    raise ValueError('assembly_syntax_outside_terminal_forward_summary')

def forward(lookup,n,state):
    if n.get('nodeType')!='InlineAssembly':return None
    try:text=n.get('operations') or yul_text(n.get('AST',{}))
    except (ValueError,KeyError,TypeError):return None
    text=re.sub(r'/\*.*?\*/|//[^\n]*',' ',text,flags=re.S)
    compact=re.sub(r'\s+','',text)
    match=_PATTERN.fullmatch(compact)
    terminal=bool(match)
    if not match:match=_BYTES_PATTERN.fullmatch(compact)
    if not match:return None
    names=match.groupdict()
    # Distinct assembly temporaries must not shadow target/input bindings.
    if len({names[k] for k in ('result','size','ptr','dst','data')})!=5:return None
    reserve=names.get('reserve') or '0'
    if not 0<=int(reserve,0 if reserve.startswith('0x') else 10)<2**64:return None
    dst_id=bound_reference(n,names['dst'],lookup);data_id=bound_reference(n,names['data'],lookup)
    if dst_id is None or data_id is None:return None
    data_decl=lookup.nodes[data_id];dst_decl=lookup.nodes[dst_id]
    if data_decl.get('stateVariable') or not data_decl.get('typeDescriptions',{}).get('typeIdentifier','').startswith('t_bytes_memory'):return None
    if dst_decl.get('typeDescriptions',{}).get('typeString') not in ('address','address payable'):return None
    data=state['env'].get(data_id)
    if not data or not (data.get('kind')=='source_calldata_bytes' or data.get('kind')=='parameter' and data.get('type','').startswith('bytes')):return None
    if dst_id in state['env']:destination=copy.deepcopy(state['env'][dst_id])
    elif dst_decl.get('stateVariable'):destination={'kind':'storage','root':dst_id,'segments':[]}
    else:return None
    if not terminal:
        response_id=bound_reference(n,names['ptr'],lookup)
        response_decl=lookup.nodes.get(response_id,{})
        if response_id is None or response_decl.get('stateVariable') or not response_decl.get('typeDescriptions',{}).get('typeIdentifier','').startswith('t_bytes_memory'):return None
        state['env'][response_id]={'kind':'unknown','reason':'delegated_return_bytes_not_modeled'}
    source=lookup.anchor(n)
    effect={'kind':'dangerous_external_call','recipient':destination,'source':source,
        'scope':'exact compiler-bound terminal delegate forwarding; callee state, return bytes and gas sufficiency not modeled',
        'call_mode':'DELEGATECALL',
        'callpoint_writes':copy.deepcopy(state['writes']),
        'callpoint_guards':copy.deepcopy(state['guards']),
        'callpoint_evaluations':copy.deepcopy(state.get('evaluated_terms',[])),
        'prefix_conditions':copy.deepcopy(state['guards']),
        'prefix_issues':copy.deepcopy(state['issues']),
        'prefix_evaluation_terms':copy.deepcopy(state.get('evaluated_terms',[])),
        'assembly_binding':{'destination_declaration':dst_id,'bytes_declaration':data_id,
                            'complete_block_matched':True,'failure_reverts':True,'success_halts_evm':terminal}}
    state.setdefault('sensitive_effects',[]).append(effect)
    state['issues'].append({'reason':'dangerous_external_effect_not_resolved','source':source,
                            'invocation_prefix_separately_available':True})
    if terminal:state['flow']='returned';state['_evm_halted']=True
    state.setdefault('source_assembly_summaries',[]).append({'source':source,'kind':'terminal_delegate_forward' if terminal else 'delegate_bytes_forward',
        'not_arbitrary_assembly_support':True,'only_invocation_prefix_can_support_code_boundary_query':True})
    return [state]

```

## source/src/pr_next_joint/frontend/bytes.py

SHA-256 `4b436c809c3b777d11c7f10e51f33921b8db84867df6f8a50e522199853730ce`

```python
"""Compiler-bound pure assembly reads, with explicit uses and bounds.
No external call, arbitrary memory write, storage write or signature-validity
assumption is introduced. Raw calldata words remain opaque to risk solving.
"""
import copy,re
from pr_next_joint.frontend.path_ir import op, lit, key
from pr_next_joint.frontend.assembly import bound_reference, yul_text
ID=r'[A-Za-z_$][A-Za-z0-9_$]*'
NUM=r'(?:0x[0-9a-fA-F]+|[0-9]+)'
LOAD=re.compile(r'('+ID+r'):=calldataload\(('+NUM+r')\)')
MEM=re.compile(r'('+ID+r'):=(?:mload\(add\(('+ID+r'),('+NUM+r')\)\)|byte\((0),mload\(add\(('+ID+r'),('+NUM+r')\)\)\))')

def length(value):
    return {'kind':'source_bytes_length','input':copy.deepcopy(value),'type':'uint256'}

def summarize(lookup,node,state):
    try:text=node.get('operations') or yul_text(node.get('AST',{}))
    except (ValueError,KeyError,TypeError):return None
    text=re.sub(r'/\*.*?\*/|//[^\n]*',' ',text,flags=re.S)
    text=re.sub(r'\s+','',text)
    if not text.startswith('{') or not text.endswith('}'):return None
    body=text[1:-1]
    parsed=[];position=0
    while position<len(body):
        match=LOAD.match(body,position)
        mode='calldata'
        if not match:match=MEM.match(body,position);mode='memory'
        if not match:return None
        parsed.append((mode,match));position=match.end()
    if not parsed or len(parsed)>8:return None
    updates={};evidence=[]
    for mode,m in parsed:
        dest=bound_reference(node,m[1],lookup);decl=lookup.nodes.get(dest,{})
        if dest is None or decl.get('stateVariable') or dest not in state['env'] or dest in updates:return None
        typ=decl.get('typeDescriptions',{}).get('typeString','')
        if mode=='calldata':
            if typ not in ('bytes32','uint256'):return None
            offset=int(m[2],16 if m[2].startswith('0x') else 10)
            if offset>=2**256:return None
            value={'kind':'source_calldata_word','input':copy.deepcopy(lookup.calldata),'offset':offset,
                   'type':'bytes32','scope':'opaque raw calldata read; no ABI-layout or permission inference'}
        else:
            base_name=m[2] or m[5];raw=m[3] or m[6];size=1 if m[4] else 32
            if typ not in (('uint8','bytes1') if size==1 else ('bytes32','uint256')):return None
            base_id=bound_reference(node,base_name,lookup)
            base_decl=lookup.nodes.get(base_id,{})
            if not base_decl.get('typeDescriptions',{}).get('typeIdentifier','').startswith('t_bytes_memory'):return None
            base=state['env'].get(base_id)
            if not base or base.get('kind')!='parameter' or not base.get('type','').startswith('bytes'):return None
            offset=int(raw,16 if raw.startswith('0x') else 10)-32
            if offset<0 or offset+size>128:return None
            from pr_next_joint.checks.access.shared_policy import implies
            from pr_next_joint.verification.expressions import Unsupported
            try:valid=implies(lookup,state,op('>=',length(base),lit(offset+size)))
            except (Unsupported,ValueError):return None
            if not valid:return None
            value={'kind':'source_bytes_slice','input':copy.deepcopy(base),'offset':offset,'size':size,
                   'type':typ,'range_validated_at_source':True}
        updates[dest]=value;evidence.append({'declaration':dest,'value':value})
    state['env'].update(updates)
    state.setdefault('source_assembly_summaries',[]).append({'source':lookup.anchor(node),
        'kind':'pure_source_bound_byte_reads','writes':evidence,
        'no_external_or_storage_side_effect':True,'calldata_executable_use_remains_unsupported':True})
    return [state]

def encode(encoder,value):
    kind=value.get('kind')
    if kind=='source_bytes_length':
        base=value.get('input',{})
        if base.get('kind')!='parameter' or not base.get('type','').startswith('bytes'):
            from pr_next_joint.verification.expressions import Unsupported
            raise Unsupported('dynamic_bytes_length_not_bound')
        return encoder.atom(value,'uint256')
    if kind!='source_bytes_slice':return None
    from pr_next_joint.verification.expressions import Unsupported
    base=value.get('input',{});offset=value.get('offset');size=value.get('size')
    if base.get('kind')!='parameter' or not base.get('type','').startswith('bytes') or type(offset)is not int or size not in (1,32) or not 0<=offset<=127 or offset+size>128:
        raise Unsupported('dynamic_bytes_slice_not_bound')
    z=encoder.z
    # Byte congruence preserves overlap across reads and same-input recovery.
    parts=[]
    for i in range(size):
        item={'kind':'input_byte','input':base,'offset':offset+i,'type':'uint8'}
        parts.append(encoder.atom(item,'uint8')*256**(size-1-i))
    encoder.constraints.append(encode(encoder,length(base))>=offset+size)
    return z.Sum(*parts)

```

## source/src/pr_next_joint/frontend/calls.py

SHA-256 `e5b2a6d156c8dbc0a8f564d2be910f93bfbafd24e43ad978ba7156f610f09710`

```python
"""Compiler-bound internal library calls and native CALL syntax.
No assumed token implementation or transfer-name matching.
"""
import copy
from pr_next_joint.frontend.path_ir import key, walk, op, lit, conditions_possible
from pr_next_joint.frontend.source_entry_identity import function_mutability, builtin_call
from pr_next_joint.frontend.read_calls import boolean_union

def bound_library(lookup,node,target):
    from pr_next_joint.frontend.source_library_binding import compiler_bound_receiver
    return compiler_bound_receiver(lookup,node,target)

def bind_arguments(lookup,call,target):
    args=call.get('arguments',[])
    names=call.get('names',[])
    if not names:return args
    parameters=[p.get('name') for p in target['parameters']['parameters']]
    # Reordering effectful operands would assume an evaluation order. Leave a
    # visible gap in that case; plain local or literal arguments can be mapped.
    if (len(names)!=len(args) or len(set(names))!=len(names) or set(names)!=set(parameters)
            or any(a.get('nodeType') not in ('Identifier','Literal') for a in args)):
        return None
    named=dict(zip(names,args))
    return [named[name] for name in parameters]

def expression_call(p,node,env):
    expr=node.get('expression',{});target=p.fns.get(expr.get('referencedDeclaration'))
    if not target or function_mutability(target) in ('pure','view'):return None
    declared=target
    bound=bound_library(p,node,target)
    from pr_next_joint.frontend.dispatch import member_target, resolve
    if not bound:
        target=resolve(p,target,p.read_calls.active_contract) if expr.get('nodeType')=='Identifier' else member_target(p,node,target)
        if target is None:return None
    params=target.get('parameters',{}).get('parameters',[])
    source_args=bind_arguments(p,node,declared)
    if source_args is None:
        p.current['issues'].append({'reason':'named_internal_arguments_not_bound','source':p.anchor(node)})
        return {'kind':'unknown','reason':'named_internal_arguments_not_bound'}
    args=([p.value(expr['expression'],env)] if bound else [])+[p.value(a,env) for a in source_args]
    if len(args)!=len(params):return None
    stack=getattr(p,'_effect_expression_stack',[])
    if target['id'] in stack or len(stack)>=8:raise ValueError('P_EFFECT_CALL_DEPTH_LIMIT')
    parent=p.current;outer_unknown=p.unknown;p.unknown=[]
    p._effect_expression_stack=stack+[target['id']]
    child=copy.deepcopy(parent);before=len(child['writes'])
    try:
        paths=p.invoke(target,args,child,depth=len(stack)+1);unknown=list(p.unknown)
    finally:
        p.current=parent;p._effect_expression_stack=stack;p.unknown=outer_unknown
    if unknown or any(x['issues'] or x.get('_evm_halted') or x.get('evaluation_gaps') or len(x['writes'])!=before for x in paths):
        # Branch-dependent state writes require a statement-level expansion.
        parent['issues'].append({'reason':'internal_effect_expression_requires_state_expansion','source':p.anchor(node)})
        return {'kind':'unknown','reason':'internal_effect_expression_requires_state_expansion'}
    successes=[x for x in paths if x['flow'] in ('normal','returned') and 'return_value' in x and conditions_possible(x['guards'])]
    if not successes:parent['guards'].append(lit(False));return lit(False)
    gates=[boolean_union('and',x['guards']) for x in successes]
    parent['guards'].append(boolean_union('or',gates))
    evaluated_before=len(parent.get('evaluated_terms',[]))
    for child,gate in zip(successes,gates):
        for field in ('sensitive_effects','native_transfers'):
            old=parent.get(field,[])
            for effect in child.get(field,[]):
                if effect in old:continue
                effect=copy.deepcopy(effect);effect['call_path_conditions']=copy.deepcopy(child['guards'])
                parent.setdefault(field,[]).append(effect)
        terms=child.get('evaluated_terms',[])[evaluated_before:]
        if terms:parent.setdefault('evaluated_terms',[]).append({'kind':'guarded_evaluation','condition':gate,'values':terms})
    result=successes[-1]['return_value']
    for child,gate in reversed(list(zip(successes[:-1],gates[:-1]))):
        result={'kind':'conditional','condition':gate,'when_true':child['return_value'],'when_false':result}
    parent.setdefault('source_calls',[]).append({'source':p.anchor(node),'target':p.anchor(target),'basis':'compiler_internal_library_or_local_body','sender_preserved':True,'conditional_effects_preserved':True})
    return result

def native_call(p,node,env):
    expr=node.get('expression',{});options={}
    if expr.get('nodeType')=='FunctionCallOptions':
        options=dict(zip(expr.get('names',[]),expr.get('options',[])));expr=expr.get('expression',{})
    else:
        while expr.get('nodeType')=='FunctionCall':
            member=expr.get('expression',{})
            if member.get('nodeType')!='MemberAccess' or member.get('memberName') not in ('value','gas') or len(expr.get('arguments',[]))!=1:return None
            if member['memberName'] in options:return None
            options[member['memberName']]=expr['arguments'][0];expr=member['expression']
    if expr.get('nodeType')!='MemberAccess' or expr.get('memberName')!='call' or 'value' not in options:return None
    receiver=expr.get('expression',{});typ=receiver.get('typeDescriptions',{}).get('typeString','')
    args=node.get('arguments',[])
    if typ not in ('address','address payable') or len(args)!=1 or args[0].get('nodeType')!='Literal' or args[0].get('value')!='':return None
    recipient=p.value(receiver,env);amount=p.value(options['value'],env)
    gas=p.value(options['gas'],env) if 'gas' in options else None
    success={'kind':'native_call_success','source_id':node['id'],'recipient':recipient,'amount':amount}
    effect={'kind':'native_transfer','recipient':recipient,'amount':amount,'success':success,'source':p.anchor(node),
            'gas_argument':gas,'scope':'conditional native CALL; actual recipient execution/transaction success not established'}
    p.current.setdefault('native_transfers',[]).append(copy.deepcopy(effect));p.current.setdefault('sensitive_effects',[]).append(effect)
    # Solidity <0.5 returns bool; newer compiler ASTs return (bool,bytes).
    if node.get('typeDescriptions',{}).get('typeString')=='bool':return success
    return {'kind':'tuple','items':[success,{'kind':'native_return_data','source_id':node['id']}]}


def expand_value_statement(p,node,state,depth):
    """Lift one whole internal call out of an evaluated statement position.
    No reordering of short-circuit operands, sibling calls or side-effect arguments.
    """
    from .delegate_calls import expand
    delegated=expand(p,node,state,depth)
    if delegated is not None:return delegated
    kind=node.get('nodeType');route=None
    if kind=='VariableDeclarationStatement':route=('initialValue',)
    elif kind in ('Return','IfStatement'):route=('expression',) if kind=='Return' else ('condition',)
    elif kind=='ExpressionStatement':
        expression=node.get('expression',{})
        if builtin_call(expression,p) and expression.get('arguments'):route=('expression','arguments',0)
        elif expression.get('nodeType')=='Assignment' and expression.get('operator')=='=':
            lhs=expression.get('leftHandSide',{})
            # Complex LHS evaluation ordering is not assumed.
            if lhs.get('nodeType')=='Identifier':route=('expression','rightHandSide')
    if route is None:return None
    call=node
    for part in route:call=(call.get(part) if isinstance(call,dict) else call[part]) if call is not None else None
    if not call:return None
    shape=internal_value_target(p,call)
    if shape is None:
        from pr_next_joint.frontend.condition_paths import contains_effect_call
        if not contains_effect_call(p,call):return None
    from pr_next_joint.frontend.condition_paths import values
    outputs=[]
    for child,value in values(p,call,state,depth,shape):
        if value is None:
            outputs.append(child)
            continue
        replacement=copy.deepcopy(node);cursor=replacement
        for part in route[:-1]:cursor=cursor[part]
        cursor[route[-1]]={'nodeType':'V16EvaluatedValue','id':call.get('id'),'src':call.get('src'),'value':value}
        outputs.extend(p.statement(replacement,child,depth))
        if len(outputs)>p.limit:raise ValueError('P_SOURCE_PATH_LIMIT')
    return outputs

def internal_value_target(p,call):
    if call.get('nodeType')!='FunctionCall':return None
    expr=call.get('expression',{});target=p.fns.get(expr.get('referencedDeclaration'))
    if not target or function_mutability(target) in ('pure','view') or not target.get('returnParameters',{}).get('parameters'):return None
    bound=bound_library(p,call,target)
    if not bound and expr.get('nodeType')!='Identifier':
        from pr_next_joint.frontend.dispatch import member_target
        target=member_target(p,call,target)
        if target is None:return None
    source_args=bind_arguments(p,call,target)
    if source_args is None:return None
    arguments=([expr['expression']] if bound else [])+source_args
    if any(n.get('nodeType') in ('Assignment',) or n.get('nodeType')=='UnaryOperation' and n.get('operator') in ('++','--','delete') or n.get('nodeType')=='FunctionCall' and n.get('kind')!='typeConversion' for n in walk(arguments)):return None
    if not bound and expr.get('nodeType')=='Identifier':
        from pr_next_joint.frontend.dispatch import resolve
        target=resolve(p,target,p.read_calls.active_contract)
    return target,arguments

def invoke_value(p,call,state,depth,shape):
    target,arguments=shape
    if depth>=8:raise ValueError('P_EFFECT_CALL_DEPTH_LIMIT')
    args=[p.expr(a,state) for a in arguments]
    if len(args)!=len(target.get('parameters',{}).get('parameters',[])):
        raise ValueError('P_INTERNAL_ARGUMENT_BINDING')
    outer_env=copy.deepcopy(state['env']);outer_return={k:copy.deepcopy(state[k]) for k in ('_return_ids','_return_pending','return_value') if k in state}
    for child in p.invoke(target,args,copy.deepcopy(state),depth+1):
        if child['flow'] not in ('normal','returned') or child.get('_evm_halted'):
            yield child,None
            continue
        value=child.get('return_value')
        if value is None:
            child['issues'].append({'reason':'internal_value_call_missing_return','source':p.anchor(call)})
            value={'kind':'unknown','reason':'internal_value_call_missing_return'}
        child['env']=copy.deepcopy(outer_env);child['flow']='normal'
        for field in ('_return_ids','_return_pending','return_value'):child.pop(field,None)
        child.update(copy.deepcopy(outer_return))
        child.setdefault('source_calls',[]).append({'source':p.anchor(call),'target':p.anchor(target),'basis':'compiler_bound_internal_value_statement_expansion','sender_preserved':True,'state_and_return_path_preserved':True})
        yield child,value

```

## source/src/pr_next_joint/frontend/compiler_evidence.py

SHA-256 `83b76fb7f8d83d232ae4f39ec8f4099462960bf2f3f6d7cdbddc2d323869e5a5`

```python
"""Narrow, source-mapped legacy dispatcher evidence; no EVM execution or guesses.

Accept only the complete known linear 0.4 dispatcher grammar. Unsupported layouts
yield no evidence. Original compiler artifacts are never changed.
"""
import hashlib

class CompilerEntryEvidence(dict):
    """In-process provenance marker: cannot be supplied by a JSON artifact."""

def legacy_dispatch(runtime, source_map, selectors):
    try:
        code=bytes.fromhex(runtime.removeprefix('0x'))
        if not source_map:return {}
        maps=[];previous=[-1,-1,-1]
        for item in source_map.split(';'):
            fields=item.split(':')
            for j in range(min(3,len(fields))):
                if fields[j]!='':previous[j]=int(fields[j])
            maps.append(tuple(previous))
        ins=[];pc=0
        while pc<len(code) and len(ins)<len(maps):
            op=code[pc];n=op-95 if 96<=op<=127 else 0
            if pc+1+n>len(code):return {}
            ins.append((pc,op,int.from_bytes(code[pc+1:pc+1+n],'big') if n else None,maps[len(ins)]))
            pc+=n+1
        i=0
        def take(op,value=None):
            nonlocal i
            if i>=len(ins) or ins[i][1]!=op or value is not None and ins[i][2]!=value:raise ValueError('grammar')
            result=ins[i];i+=1;return result
        def push():
            nonlocal i
            if i>=len(ins) or not 96<=ins[i][1]<=127:raise ValueError('push')
            result=ins[i];i+=1;return result
        memory=take(0x60)
        if memory[2] not in (0x60,0x80):return {}
        take(0x60,0x40);take(0x52)
        # Two known 0.4 compiler guards: calldata shorter than a selector,
        # or empty calldata. Match the complete grammar, not a loose scan.
        if i<len(ins) and ins[i][1]==0x36:
            take(0x36);take(0x15)
        else:
            take(0x60,4);take(0x36);take(0x10)
        fallback=push()[2];take(0x57)
        take(0x60,0);take(0x35);take(0x7c,1<<224);take(0x90);take(0x04);take(0x63,0xffffffff);take(0x16)
        branches={}
        while i<len(ins) and ins[i][1]==0x80:
            branch_pc=take(0x80)[0];selector=take(0x63)[2].to_bytes(4,'big').hex();take(0x14)
            target=push()[2];take(0x57)
            if selector in branches:return {}
            branches[selector]={'dispatch_pc':branch_pc,'target_pc':target}
        end=take(0x5b)
        if fallback!=end[0] or set(branches)!=set(selectors):return {}
        bypc={row[0]:row for row in ins}
        result={}
        for selector,branch in branches.items():
            destination=bypc.get(branch['target_pc'])
            if not destination or destination[1]!=0x5b:return {}
            start,length,file_id=destination[3]
            if start<0 or length<=0 or file_id<0:return {}
            result[selector]={**branch,'source_start':start,'source_length':length,'source_file_id':file_id}
        return result
    except (ValueError,TypeError,IndexError,OverflowError):
        return {}

def derive(bundle,compiled,output_sha256):
    evidence=CompilerEntryEvidence()
    if not str(bundle.get('compiler',{}).get('compiler_version','')).startswith('0.4.'):
        return evidence
    for contract in bundle['contracts']:
        target=contract['file']+':'+contract['name']
        output=compiled.get('contracts',{}).get(contract['file'],{}).get(contract['name'],{})
        deployed=output.get('evm',{}).get('deployedBytecode',{})
        runtime=deployed.get('object','');source_map=deployed.get('sourceMap','')
        if not runtime or runtime.removeprefix('0x')!=contract.get('runtime','').removeprefix('0x'):continue
        if deployed.get('linkReferences') or contract.get('runtime_link_references'):continue
        selectors={f['selector'] for f in contract['functions']}
        branches=legacy_dispatch(runtime,source_map,selectors)
        if branches:
            evidence[target]={'program_id':bundle['program_id'],'build_id':bundle['build_id'],
                'standard_output_sha256':output_sha256,'runtime_sha256':hashlib.sha256(bytes.fromhex(runtime.removeprefix('0x'))).hexdigest(),
                'source_map_sha256':hashlib.sha256(source_map.encode()).hexdigest(),'grammar':'legacy_linear_dispatch_v2','branches':branches}
    return evidence

import hashlib,json
from pr_next_joint.core import require

class CompilerSourceEvidence(dict):
    """In-process provenance; JSON input cannot supply this evidence type."""
    def __init__(self,program_id,build_id):
        super().__init__();self.program_id=program_id;self.build_id=build_id

def derive_source_evidence(standard,compiled,bundle,output_sha256):
    evidence=CompilerSourceEvidence(bundle['program_id'],bundle['build_id'])
    anchored={r.get('source_anchor',{}).get('file') for r in bundle.get('functions',[])+bundle.get('state_declarations',[])}
    needed=set(standard['sources'])-anchored
    if not needed:return evidence
    claims={path:[] for path in needed};version=bundle['compiler']['compiler_version']
    for file,contracts in compiled.get('contracts',{}).items():
        for name,output in contracts.items():
            raw=output.get('metadata')
            if not raw:continue
            try:metadata=json.loads(raw)
            except (TypeError,ValueError):continue
            relevant=needed.intersection(metadata.get('sources',{}))
            if not relevant:continue
            require(metadata.get('language')=='Solidity','DATASET_METADATA_LANGUAGE')
            require(metadata.get('settings',{}).get('compilationTarget')=={file:name},'DATASET_METADATA_TARGET')
            require(metadata.get('compiler',{}).get('version','').split('+')[0]==version,'DATASET_METADATA_COMPILER')
            for path in relevant:
                claim=metadata['sources'][path].get('keccak256')
                require(isinstance(claim,str) and len(claim)==66 and claim.startswith('0x'),'DATASET_METADATA_SOURCE_HASH')
                claims[path].append({'target':file+':'+name,'keccak256':claim.lower(),'metadata_sha256':hashlib.sha256(raw.encode('utf8')).hexdigest()})
    # Keccak-256 is Ethereum's original hash, not hashlib.sha3_256.
    from Crypto.Hash import keccak
    for path,records in claims.items():
        if not records:continue
        data=standard['sources'][path]['content'].encode('utf8');h=keccak.new(digest_bits=256);h.update(data)
        expected='0x'+h.hexdigest()
        require({r['keccak256'] for r in records}=={expected},'DATASET_METADATA_SOURCE_MISMATCH:'+path)
        evidence[path]={'source_sha256':hashlib.sha256(data).hexdigest(),'source_keccak256':expected,
            'standard_output_sha256':output_sha256,'compiler_version':version,'metadata_sources':records}
    return evidence

```

## source/src/pr_next_joint/frontend/condition_paths.py

SHA-256 `df5ca75eaaafd2440739edc39966bc5f58387340014edad5ca2b94236c2d9d32`

```python
"""Execute conditional expressions containing bound internal transitions, in Solidity order."""
import copy

from pr_next_joint.frontend.path_ir import conditions_possible, lit, normalize, op
from pr_next_joint.frontend.calls import internal_value_target, invoke_value


def children(node):
    kind = node.get('nodeType')
    if kind == 'BinaryOperation' and node.get('operator') in ('&&', '||') and not node.get('function'):
        return node['leftExpression'], node['rightExpression']
    if kind == 'Conditional':
        return node['condition'], node['trueExpression'], node['falseExpression']
    if kind == 'UnaryOperation' and node.get('operator') == '!' and not node.get('function'):
        return (node['subExpression'],)
    if kind == 'TupleExpression' and not node.get('isInlineArray') and len(node['components']) == 1 and node['components'][0]:
        return tuple(node['components'])
    return ()


def contains_effect_call(lookup, node):
    return any(internal_value_target(lookup, child) or contains_effect_call(lookup, child)
               for child in children(node))


def values(lookup, node, state, depth, shape=None):
    shape = shape or internal_value_target(lookup, node)
    if shape:
        yield from invoke_value(lookup, node, state, depth, shape)
        return
    parts = children(node)
    if not parts:
        value = lookup.expr(node, state)
        yield state, value if state['flow'] == 'normal' else None
        return
    for branch, first in values(lookup, parts[0], state, depth):
        if first is None or len(parts) == 1:
            if first is not None and node.get('operator') == '!':
                first = normalize(op('!', first))
            yield branch, first
            continue
        for truth in (True, False):
            guard = first if truth else op('!', first)
            if not conditions_possible(branch['guards'] + [guard]):
                continue
            selected = copy.deepcopy(branch)
            selected['guards'].append(guard)
            selected.setdefault('branch_choices', []).append({
                'condition': first, 'sign': truth, 'source': lookup.anchor(parts[0])})
            if len(parts) == 3:
                yield from values(lookup, parts[1 if truth else 2], selected, depth)
            elif truth == (node['operator'] == '&&'):
                yield from values(lookup, parts[1], selected, depth)
            else:
                yield selected, lit(truth)

```

## source/src/pr_next_joint/frontend/dataset_intake.py

SHA-256 `abf4c9e9a41206457a25bd641fc590073430f20893c2185001a1e4742271658c`

```python
"""Read matched compiler facts using original compiler settings, never labels.

This is an input adapter, not a source-anchor/semantic binding replacement.
The existing strict anchor validator and all M2/M3/M4 checks remain in force.
"""
import copy,hashlib,json,re
from pathlib import Path
from pr_next_joint.core import digest, require
from pr_next_joint.frontend.source_intake import validate_loaded_artifacts
from pr_next_joint.frontend.inventory import target_inventory

FILES=('standard-input.json','standard-output.json','ProgramBundle.json','native_ssa.json','extract_receipt.json')

def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def confined(root,name):
    require(isinstance(name,str) and name,'DATASET_PATH_REQUIRED')
    p=(root/name).resolve();require(p.is_relative_to(root.resolve()),'DATASET_PATH_OUTSIDE_ROOT')
    require(p.is_file(),'DATASET_FILE_MISSING:'+name)
    return p

def load_compiled_unit(root,descriptor):
    root=Path(root).resolve();spec_path=confined(root,str(descriptor));spec=read(spec_path)
    require(spec.get('schema')=='dataset-compiled-unit-v1','DATASET_SCHEMA')
    require(set(spec)<={'schema','input_id','unit_id','artifacts','targets','description'},'DATASET_UNEXPECTED_FIELDS')
    for key in ('input_id','unit_id'):
        require(isinstance(spec.get(key),str) and re.fullmatch(r'[A-Za-z0-9_]+',spec[key]),'DATASET_ID')
    artifacts=spec.get('artifacts',{})
    require(set(artifacts)==set(FILES),'DATASET_ARTIFACT_SET')
    paths={}
    for name,item in artifacts.items():
        require(set(item)=={'path','sha256'},'DATASET_ARTIFACT_SHAPE')
        path=confined(root,item['path']);require(sha(path)==item['sha256'],'DATASET_ARTIFACT_CHANGED:'+name);paths[name]=path
    standard,compiled,bundle,native,receipt=[read(paths[n]) for n in FILES]
    retained = receipt.get('status') == 'extracted'
    require(receipt.get('status')=='compiled_and_extracted' or
            retained and receipt.get('compiler_invocations')==0 and receipt.get('native_extractions')==1,
            'DATASET_FACTS_NOT_READY')
    # An original retained-compiler extraction receipt records the actual old
    # extraction. No replacement success receipt or fresh compilation is claimed.
    for field, name in (('bundle_file_sha256','ProgramBundle.json'),('native_file_sha256','native_ssa.json')):
        if field in receipt: require(receipt[field]==sha(paths[name]),'DATASET_RETAINED_FILE_RECEIPT')
    require(receipt.get('standard_input_sha256')==sha(paths['standard-input.json']),'DATASET_INPUT_RECEIPT')
    if not retained or 'standard_input_digest' in receipt:
        require(receipt.get('standard_input_digest')==digest(standard),'DATASET_INPUT_DIGEST')
    require(receipt.get('standard_output_sha256')==sha(paths['standard-output.json']),'DATASET_OUTPUT_RECEIPT')
    require(standard.get('language')=='Solidity' and isinstance(standard.get('settings'),dict),'DATASET_LANGUAGE_SETTINGS')
    require(not any(e.get('severity')=='error' for e in compiled.get('errors',[])),'DATASET_COMPILER_ERRORS')
    texts=standard.get('sources',{})
    require(bool(texts) and all(isinstance(v.get('content'),str) for v in texts.values()),'DATASET_INLINE_SOURCE_REQUIRED')
    source_hashes={k:hashlib.sha256(v['content'].encode('utf-8')).hexdigest() for k,v in texts.items()}
    require(bundle.get('program_id')==digest(source_hashes),'DATASET_PROGRAM_ID')
    expected_build=digest({'input':standard,'compiler':receipt['compiler_binary_sha256']})
    require(bundle.get('build_id')==expected_build,'DATASET_BUILD_ID')
    require(all(receipt.get(k)==bundle.get(k)==native.get(k) for k in ('program_id','build_id')),'DATASET_FACT_IDENTITIES')
    require(receipt.get('native_sha256')==digest(native),'DATASET_NATIVE_RECEIPT')
    require(bundle.get('ast_sources')=={k:v.get('ast') for k,v in compiled.get('sources',{}).items()},'DATASET_AST_OUTPUT_MISMATCH')
    require(bundle.get('compiler',{}).get('compiler_version')==receipt.get('compiler_version'),'DATASET_COMPILER_VERSION')
    case={'standard_input':standard,'sources':[{'path':k,'sha256':v} for k,v in source_hashes.items()]}
    from pr_next_joint.frontend.compiler_evidence import derive_source_evidence
    compiler_sources=derive_source_evidence(standard,compiled,bundle,sha(paths['standard-output.json']))
    binding=validate_loaded_artifacts(case,bundle,native,compiler_sources=compiler_sources)
    # Derive auxiliary evidence only after original artifact identity validation.
    # The original bundle on disk and its receipt remain unchanged.
    from pr_next_joint.frontend.compiler_evidence import derive
    derived_entries=derive(bundle,compiled,sha(paths['standard-output.json']))
    bundle=copy.deepcopy(bundle)
    from pr_next_joint.runtime.immutable import restore
    immutable_reconstruction=restore(bundle,standard,compiled)
    bundle.pop('_compiler_entry_evidence',None)
    if derived_entries:
        bundle['_compiler_entry_evidence']=derived_entries
    inventory=target_inventory(bundle)
    available={x['file']+':'+x['contract'] for x in inventory if x['selected']}
    selection=spec.get('targets','auto')
    require(selection=='auto' or isinstance(selection,list) and selection and all(isinstance(x,str) for x in selection),'DATASET_TARGET_SPEC')
    requested=None if selection=='auto' else selection
    require(requested is None or len(requested)==len(set(requested)) and set(requested)<=available,'DATASET_TARGET_NOT_AVAILABLE')
    require(bool(available),'DATASET_NO_CONCRETE_TARGET')
    for item in inventory:
        if requested is not None and item['selected'] and item['file']+':'+item['contract'] not in requested:
            item.update(selected=False,reason='not_selected_by_explicit_scope')
    description=None
    if spec.get('description'):
        item=spec['description'];require(set(item)=={'path','sha256'},'DATASET_DESCRIPTION_SPEC')
        path=confined(root,item['path']);require(sha(path)==item['sha256'],'DATASET_DESCRIPTION_CHANGED')
        description=path.read_text(encoding='utf-8-sig')
    record={'schema':'dataset-intake-receipt-v1','input_id':spec['input_id'],'unit_id':spec['unit_id'],
        'descriptor_sha256':sha(spec_path),'program_id':bundle['program_id'],'build_id':bundle['build_id'],
        'compiler_version':receipt['compiler_version'],'compiler_sha256':receipt['compiler_binary_sha256'],
        'settings':standard['settings'],'source_hashes':source_hashes,'targets_requested':selection,
        'targets_selected':sorted(available if requested is None else requested),'target_inventory':inventory,
        'facts_verified':True,'original_extraction_status':receipt['status'],'compiler_invocations':0,'labels_read':False,'method_execution':'not_run',
        'artifact_sha256':{n:sha(p) for n,p in paths.items()},
        'derived_entry_evidence_targets':sorted(derived_entries),
        'compiler_metadata_bound_sources':sorted(compiler_sources)}
    if immutable_reconstruction:
        record['immutable_reconstruction']=immutable_reconstruction
        record['compiler_invocations']+=immutable_reconstruction['invocations']
    return {'unit_id':spec['unit_id'],'bundle':bundle,'native':native,'binding':binding,
        'sources':[{'file':k,'sha256':source_hashes[k],'content':v['content']} for k,v in texts.items()],
        'description':description,'selected_targets':requested,'receipt':record}

```

## source/src/pr_next_joint/frontend/delegate_calls.py

SHA-256 `493bcc96e4fc7eb41bb6736e9cbde21e9dd2af6f4980c05c97f7b1d891959637`

```python
"""Source-bound DELEGATECALL with explicit selector and a fixed supplied body.

CALL storage separation is never applied to delegate execution. Unknown code,
unknown selectors and unproved layouts fall through to the ordinary residual.
"""
import copy
from .path_ir import lit,walk


def layout(lookup,contract):
    data=contract.get('storage_layout') or {}
    if data.get('storage'):
        types=data['types']
        def shape(t):
            v=types[t]
            if v.get('members'):raise ValueError('delegate_struct_layout_not_supported')
            return (v['encoding'],v['numberOfBytes'],
                shape(v['key']) if 'key'in v else None,shape(v['value']) if 'value'in v else None,
                shape(v['base']) if 'base'in v else None,v.get('label') if v['encoding']=='inplace' else None)
        return {int(row['astId']):(int(row['slot']),int(row['offset']),shape(row['type'])) for row in data['storage']}
    # Exact Solidity packing for elementary values and mapping roots. A
    # complex unavailable layout is not guessed from declaration names.
    node=next(n for n in lookup.nodes.values() if n.get('nodeType')=='ContractDefinition' and
              n.get('name')==contract['name'] and lookup.anchor(n)['file']==contract['file'])
    result={};slot=offset=0
    for cid in reversed(node.get('linearizedBaseContracts',[node['id']])):
        for d in lookup.nodes[cid].get('nodes',[]):
            if d.get('nodeType')!='VariableDeclaration' or not d.get('stateVariable') or d.get('constant') or d.get('mutability')=='immutable':continue
            typ=d.get('typeName',{});kind=typ.get('nodeType')
            if kind=='Mapping':
                if offset:slot+=1;offset=0
                result[d['id']]=(slot,0,('mapping',typ.get('typeDescriptions',{}).get('typeString')));slot+=1;continue
            name=typ.get('name') or d.get('typeDescriptions',{}).get('typeString','')
            if name.startswith('contract '):name='address'
            import re
            if name in ('address','address payable'):size=20;name='address'
            elif name=='bool':size=1
            elif re.fullmatch(r'u?int\d*',name):size=int(re.sub(r'\D','',name) or 256)//8
            elif re.fullmatch(r'bytes\d+',name):size=int(name[5:])
            else:raise ValueError('delegate_layout_unavailable_for:'+name)
            if offset+size>32:slot+=1;offset=0
            result[d['id']]=(slot,offset,('elementary',name));offset+=size
            if offset==32:slot+=1;offset=0
    return result


def expand(p,node,state,depth):
    kind=node.get('nodeType');route=None
    if kind=='VariableDeclarationStatement':route=('initialValue',)
    elif kind=='ExpressionStatement':
        call=node.get('expression',{})
        if call.get('nodeType')=='FunctionCall':route=('expression',)
        elif call.get('nodeType')=='Assignment' and call.get('operator')=='=':route=('expression','rightHandSide')
    if not route:return None
    call=node
    for k in route:call=call.get(k,{}) or {}
    exp=call.get('expression',{})
    if call.get('nodeType')!='FunctionCall' or exp.get('nodeType')!='MemberAccess' or exp.get('memberName')!='delegatecall':return None
    receiver=exp.get('expression',{})
    while receiver.get('nodeType')=='FunctionCall' and receiver.get('kind')=='typeConversion' and len(receiver.get('arguments',[]))==1:
        receiver=receiver['arguments'][0]
    if receiver.get('nodeType')!='Identifier':return None
    found=p.read_calls.created_type(receiver.get('referencedDeclaration'))
    if not found or len(call.get('arguments',[]))!=1:return None
    cid,_=found;payload=call['arguments'][0];abi=payload.get('expression',{})
    if abi.get('memberName')!='encodeWithSelector' or abi.get('expression',{}).get('name')!='abi':return None
    args=payload.get('arguments',[])
    if not args or args[0].get('memberName')!='selector':return None
    declaration=p.nodes.get(args[0].get('expression',{}).get('referencedDeclaration'),{})
    if declaration.get('nodeType')!='FunctionDefinition':return None
    target=p.read_calls.implementation(cid,declaration)
    if not target or not target.get('body') or depth>=8:return None
    if len(args)-1!=len(target.get('parameters',{}).get('parameters',[])):return None
    callee=next(c for c in p.bundle['contracts'] if c['name']==p.nodes[cid]['name'] and c['file']==p.anchor(p.nodes[cid])['file'])
    try:
        original=layout(p,p.contract);other=layout(p,callee);reverse={shape:rid for rid,shape in original.items()}
        mapping={rid:reverse[shape] for rid,shape in other.items() if shape in reverse}
        used={n.get('referencedDeclaration') for n in walk(target) if p.nodes.get(n.get('referencedDeclaration'),{}).get('stateVariable')}
        if not used<=set(mapping):return None
    except (ValueError,KeyError,StopIteration):return None
    actual=[p.expr(a,state) for a in args[1:]]
    saved=(p.current,p.read_calls.active_contract,getattr(p,'_delegate_storage_map',None),getattr(p,'_entry_selector',None))
    p.read_calls.active_contract=cid;p._delegate_storage_map=mapping;p._entry_selector=p.function_selector(target)
    outer_env=copy.deepcopy(state['env']);outer_return={k:copy.deepcopy(state[k]) for k in ('_return_ids','_return_pending','return_value') if k in state}
    try:children=p.invoke(target,actual,copy.deepcopy(state),depth+1)
    finally:p.current,p.read_calls.active_contract,p._delegate_storage_map,p._entry_selector=saved
    out=[]
    for child in children:
        success=child['flow'] in ('normal','returned')
        if child['flow']=='reverted':
            restored=copy.deepcopy(state);restored['guards']=child['guards'];restored['evaluated_terms']=child.get('evaluated_terms',[]);child=restored
        elif not success:out.append(child);continue
        child['flow']='normal';child['env']=copy.deepcopy(outer_env)
        for k in ('_return_ids','_return_pending','return_value'):child.pop(k,None)
        child.update(copy.deepcopy(outer_return))
        record={'source':p.anchor(call),'target':p.anchor(target),'call_mode':'DELEGATECALL',
            'binding':'fixed_created_code_explicit_selector_verified_storage_layout',
            'storage_context':p.contract['file']+':'+p.contract['name'],
            'callee_contract':cid,'storage_declaration_mapping':mapping,
            'sender_preserved':True,'outer_call_context_preserved':True,
            'callee_failure_rolls_back_callee_writes':True,'return_value':lit(success),
            'callpoint_writes':copy.deepcopy(state['writes']),'callpoint_guards':copy.deepcopy(state['guards'])}
        child.setdefault('resolved_calls',[]).append(record)
        val=lit(success) if call.get('typeDescriptions',{}).get('typeString')=='bool' else {
            'kind':'tuple','items':[lit(success),{'kind':'unknown','reason':'delegate_return_bytes_not_decoded'}]}
        replacement=copy.deepcopy(node);cursor=replacement
        for part in route[:-1]:cursor=cursor[part]
        cursor[route[-1]]={'nodeType':'V16EvaluatedValue','src':call.get('src'),'id':call.get('id'),'value':val}
        out.extend(p.statement(replacement,child,depth))
    return out

```

## source/src/pr_next_joint/frontend/dispatch.py

SHA-256 `b1eb4ebf67f30e20cd734287ed4f85777e312cd98846682828c50b45b3e67926`

```python
"""Unqualified ordinary-function dispatch from compiler-checked C3 inheritance."""
from pr_next_joint.frontend.source_entry_identity import function_kind
def resolve(lookup,target,contract_id=None,after=None):
    if not target or function_kind(target)!='function' or target.get('visibility')=='private':return target
    cid=contract_id or lookup.contract_node['id'];order=lookup.nodes[cid].get('linearizedBaseContracts',[cid])
    if target.get('scope') not in order:return target
    if after is not None:
        if after not in order:raise ValueError('P_SUPER_LEXICAL_SCOPE_NOT_IN_HIERARCHY')
        order=order[order.index(after)+1:]
    def signature(n):
        types=[p.get('typeDescriptions',{}).get('typeIdentifier') for p in n.get('parameters',{}).get('parameters',[])]
        return (n.get('name'),tuple(types)) if all(types) else None
    sig=signature(target)
    if sig is None:return target
    for owner in order:
        matches=[n for n in lookup.fns.values() if function_kind(n)=='function' and n.get('scope')==owner and n.get('visibility')!='private' and signature(n)==sig]
        if len(matches)>1:raise ValueError('internal_dispatch_ambiguous_source_signature')
        if matches and (after is None or matches[0].get('body')):return matches[0]
    if after is not None:raise ValueError('P_SUPER_CONCRETE_TARGET_NOT_FOUND')
    return target

def member_target(lookup,call,target):
    """Distinguish an internal base/super call from an external object method."""
    expr=call['expression'];base=expr.get('expression',{})
    if not target or expr.get('nodeType')!='MemberAccess' or call.get('names'):return None
    if not expr.get('typeDescriptions',{}).get('typeIdentifier','').startswith('t_function_internal_'):return None
    if base.get('nodeType') not in ('Identifier','IdentifierPath'):return None
    order=lookup.contract_node['linearizedBaseContracts']
    if base.get('referencedDeclaration') in order and target.get('scope') in order:
        return target
    if base.get('name')!='super' or 'super' not in base.get('typeDescriptions',{}).get('typeIdentifier',''):return None
    if not hasattr(lookup,'_lexical_call_scopes'):
        from pr_next_joint.frontend.path_ir import walk
        lookup._lexical_call_scopes={n['id']:f['scope'] for f in lookup.fns.values() if f.get('scope') in order
                                    for n in walk(f.get('body')) if n.get('nodeType')=='FunctionCall'}
    owner=lookup._lexical_call_scopes.get(call['id'])
    if owner is None:raise ValueError('P_SUPER_LEXICAL_SCOPE_UNRESOLVED')
    return resolve(lookup,target,lookup.read_calls.active_contract,after=owner)

import copy
from pr_next_joint.frontend.path_ir import key, op, lit, normalize, conditions_possible

def read_after_writes(selector,writes,guards):
    value=selector
    # Only direct equality facts are needed to simplify a key alias. Omitting
    # other guards is conservative: retain an ite when equality is not proved.
    equalities=[]
    def collect(g):
        if g.get('kind')=='op' and g.get('op') in ('and','&&'):
            for a in g['args']:collect(a)
        elif g.get('kind')=='op' and g.get('op') in ('==','!=') and all(a.get('kind') in ('actual_sender','parameter','literal','contract_address') for a in g['args']):equalities.append(g)
        elif g.get('kind')=='op' and g.get('op')=='!' and g['args'][0].get('kind')=='op' and g['args'][0].get('op') in ('==','!='):
            a=g['args'][0]
            if all(x.get('kind') in ('actual_sender','parameter','literal','contract_address') for x in a['args']):equalities.append(g)
    for g in guards:collect(g)
    for w in writes:
        p=w['path']
        if p['root']!=selector['root'] or key(p.get('instance'))!=key(selector.get('instance')):continue
        if [{k:v for k,v in x.items() if k!='key'} for x in p.get('segments',[])]!=[{k:v for k,v in x.items() if k!='key'} for x in selector.get('segments',[])]:continue
        a=[s['key'] for s in selector.get('segments',[]) if 'key' in s];b=[s['key'] for s in p.get('segments',[]) if 'key' in s]
        if len(a)!=len(b):continue
        if key(p)==key(selector):value=w['value'];continue
        same=normalize(op('and',*[op('==',x,y) for x,y in zip(a,b)]))
        if not conditions_possible(equalities,same):value=w['value']
        elif not conditions_possible(equalities+[same]):continue
        else:value=op('ite',same,copy.deepcopy(w['value']),value)
    return copy.deepcopy(value)

```

## source/src/pr_next_joint/frontend/facts.py

SHA-256 `0a5910b7efbb8db92d877cc0d72a5dc83bf07993d6769fe2ecd8dea5cda7ef5e`

```python
"""M1 compiler facts. No role inference by project, function or variable names."""
import hashlib,json,pathlib
from pr_next_joint.core import digest, require
from pr_next_joint.frontend.source_entry_identity import function_mutability

def canonical_abi_type(item):
 typ=item['type']
 return '('+','.join(canonical_abi_type(c) for c in item['components'])+')'+typ[5:] if typ.startswith('tuple') else typ

def walk(node):
 if isinstance(node,dict):
  yield node
  for v in node.values():yield from walk(v)
 elif isinstance(node,list):
  for v in node:yield from walk(v)

def build_bundle(group,standard_input,standard_output,original_output,receipt):
 require(not [e for e in standard_output.get('errors',[]) if e['severity']=='error'],'compile_error')
 sources={k:v['content'] for k,v in standard_input['sources'].items()}
 sid={v['id']:k for k,v in standard_output['sources'].items()}
 def anchor(src):
  start,length,fid=map(int,src.split(':'));file=sid.get(fid)
  return {'file':file,'start':start,'length':length,'sha256':hashlib.sha256(sources[file].encode()).hexdigest() if file else None}
 def snippet(a):
  return sources[a['file']].encode()[a['start']:a['start']+a['length']].decode('utf-8') if a['file'] else ''
 nodes={n['id']:n for s in standard_output['sources'].values() for n in walk(s['ast']) if 'id' in n}
 state={i for i,n in nodes.items() if n.get('nodeType')=='VariableDeclaration' and n.get('stateVariable')}
 functions=[];edges=[]
 for i,n in nodes.items():
  if n.get('nodeType') not in ('FunctionDefinition','ModifierDefinition'):continue
  a=anchor(n['src']);body=n.get('body')
  refs={x['referencedDeclaration'] for x in walk(body) if isinstance(x.get('referencedDeclaration'),int)}
  calls=[];conditions=[];writes=set()
  for x in walk(body):
   kind=x.get('nodeType')
   if kind=='FunctionCall':
    expr=x.get('expression',{});target=expr.get('referencedDeclaration');calls.append({'target_ast_id':target,'anchor':anchor(x['src']),'kind':x.get('kind')})
    if target in nodes:edges.append({'from':i,'to':target,'relation':'calls'})
    if expr.get('name') in ('require','assert'):conditions.append(anchor(x['src']))
   if kind in ('IfStatement','Conditional'):conditions.append(anchor(x['condition']['src']))
   if kind in ('Assignment','UnaryOperation'):
    subtree=x.get('leftHandSide',x.get('subExpression',{}))
    writes.update(y.get('referencedDeclaration') for y in walk(subtree) if y.get('referencedDeclaration') in state)
  for d in sorted(refs&state):edges.append({'from':i,'to':d,'relation':'references_state'})
  functions.append({'ast_id':i,'name':n.get('name'),'kind':n.get('kind',n['nodeType']),'visibility':n.get('visibility'),'mutability':n.get('stateMutability'),'selector':n.get('functionSelector'),'implemented':body is not None,'parameters':[{'name':p['name'],'type':p['typeDescriptions']['typeString'],'ast_id':p['id']} for p in n.get('parameters',{}).get('parameters',[])],'modifiers':[m['modifierName'].get('referencedDeclaration') for m in n.get('modifiers',[])],'state_references':sorted(refs&state),'syntactic_writes':sorted(writes),'calls':calls,'conditions':conditions,'source_anchor':a,'source':snippet(a),'unresolved_items':['ast_references_not_effect_proof']})
 contracts=[]
 for file,items in standard_output['contracts'].items():
  for name,c in items.items():
   old=original_output['contracts'][file][name]
   equal={field:c[field]==old[field] for field in ['abi']}
   for typ in ['bytecode','deployedBytecode']:
    equal[typ]=c['evm'][typ]['object']==old['evm'][typ]['object']
   require(all(equal.values()),'old_build_mismatch')
   if not c['evm']['bytecode']['object']:continue
   functions_abi=[]
   for f in c['abi']:
    if f['type']!='function':continue
    signature=f['name']+'('+','.join(canonical_abi_type(a) for a in f['inputs'])+')'
    selector=c['evm']['methodIdentifiers'].get(signature)
    require(selector is not None,'missing_selector')
    mutability=function_mutability(f)
    require(mutability is not None,'abi_function_mutability_unresolved')
    functions_abi.append({'signature':signature,'types':[a['type'] for a in f['inputs']],'selector':selector,'readonly':mutability in ['view','pure'],'outputs':[a['type'] for a in f['outputs']]})
   constructor=next((f for f in c['abi'] if f['type']=='constructor'),{'inputs':[]})
   contracts.append({'file':file,'name':name,'abi':c['abi'],'functions':functions_abi,'constructor_types':[a['type'] for a in constructor['inputs']],'creation':c['evm']['bytecode']['object'],'runtime':c['evm']['deployedBytecode']['object'],'immutable_references':c['evm']['deployedBytecode'].get('immutableReferences',{}),'creation_link_references':c['evm']['bytecode'].get('linkReferences',{}),'runtime_link_references':c['evm']['deployedBytecode'].get('linkReferences',{}),'storage_layout':c.get('storageLayout'),'metadata':json.loads(c['metadata']),'matches_frozen':equal})
 program_id=digest({k:hashlib.sha256(v.encode()).hexdigest() for k,v in sources.items()})
 bundle={'id':group,'program_id':program_id,'build_id':digest({'input':standard_input,'compiler':receipt['compiler_binary_sha256']}),'development_identity':'overlap_unverified','source_kind':'new_original_solc_ast','compiler':receipt,'functions':functions,'state_declarations':[{'ast_id':i,'name':nodes[i]['name'],'type':nodes[i]['typeDescriptions']['typeString'],'source_anchor':anchor(nodes[i]['src'])} for i in sorted(state)],'edges':edges,'contracts':contracts,'coverage':{'all_function_declarations':len(functions),'all_public_external_entries_enumerated':True,'slither_fresh':'not_executed_missing_matching_runtime','unresolved':['syntactic_writes_are_not_transitive_effect_proof','dynamic_calls_not_resolved_by_ast_alone']}}
 return bundle

```

## source/src/pr_next_joint/frontend/inventory.py

SHA-256 `956796560fdb8f24d5d9e55544246caf9d70f83d6ca3462f7f33241f7b8f3a0a`

```python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""
from pr_next_joint.frontend.facts import walk

def target_inventory(bundle):
    nodes={(file,n['name']):n for file,ast in bundle['ast_sources'].items() for n in walk(ast) if n.get('nodeType')=='ContractDefinition'}
    compiled={(c['file'],c['name']):c for c in bundle['contracts']}
    result=[]
    for identity,node in sorted(nodes.items()):
        item={'file':identity[0],'contract':identity[1],'contract_kind':node['contractKind'],'abstract':bool(node.get('abstract'))}
        item['selected']=node['contractKind']=='contract' and not node.get('abstract') and identity in compiled
        item['reason']='concrete_compiled_contract' if item['selected'] else 'interface_library_abstract_or_no_creation_artifact'
        result.append(item)
    return result

```

## source/src/pr_next_joint/frontend/language.py

SHA-256 `9857dcaa4bd7097baeedd4d400adee7e60abd989ffe4f97fccf1a876a5e25301`

```python
"""Compiler-bound scalar types and exact rational constant evaluation."""
from fractions import Fraction

def scalar_type(typ,lookup,node=None):
    node=node or {};ref=node.get('referencedDeclaration')
    declaration=lookup.nodes.get(ref,{})
    if declaration.get('nodeType')=='ContractDefinition':return 'address'
    if declaration.get('nodeType')=='EnumDefinition':return 'enum '+declaration['name']
    if not typ:return typ
    import re
    if re.fullmatch(r'(?:u?int(?:[0-9]+)?|bytes(?:[0-9]+)?|bool|address(?: payable)?|string)',typ):return typ
    if typ.startswith('contract '):return 'address'
    if typ.startswith('enum '):return typ
    matches=[n for n in lookup.nodes.values() if n.get('nodeType') in ('ContractDefinition','EnumDefinition') and n.get('name')==typ]
    kinds={n['nodeType'] for n in matches}
    if kinds=={'ContractDefinition'}:return 'address'
    if kinds=={'EnumDefinition'}:return 'enum '+typ
    return typ

def rational_constant(node,depth=0):
    if not node or depth>64:return None
    kind=node.get('nodeType');r=None
    if kind=='Literal' and node.get('kind')=='number':
        text=node['value'].replace('_','')
        r=Fraction(int(text,16)) if text.lower().startswith('0x') else Fraction(text)
        units={'wei':1,'szabo':10**12,'finney':10**15,'gwei':10**9,'ether':10**18,'seconds':1,'minutes':60,'hours':3600,'days':86400,'weeks':604800,'years':31536000}
        if node.get('subdenomination'):
            if node['subdenomination'] not in units:return None
            r*=units[node['subdenomination']]
    elif kind=='TupleExpression' and not node.get('isInlineArray') and len(node.get('components',[]))==1:
        return rational_constant(node['components'][0],depth+1)
    elif kind=='UnaryOperation' and node.get('operator') in ('+','-'):
        a=rational_constant(node.get('subExpression'),depth+1)
        if a is not None:r=a if node['operator']=='+' else -a
    elif kind=='BinaryOperation':
        # Fold only Solidity's untyped rational expressions, not typed integer
        # arithmetic, overflow, truncating division or explicit conversions.
        typ=node.get('typeDescriptions',{}).get('typeString','')
        if not typ.startswith(('rational_const ','int_const ')):return None
        a=rational_constant(node.get('leftExpression'),depth+1);b=rational_constant(node.get('rightExpression'),depth+1)
        if a is None or b is None:return None
        operator=node.get('operator')
        if operator=='+':r=a+b
        elif operator=='-':r=a-b
        elif operator=='*':r=a*b
        elif operator=='/' and b:r=a/b
        elif operator=='**' and b.denominator==1 and abs(b.numerator)<=512 and (a or b>=0):r=a**b.numerator
        else:return None
    if r is not None and max(r.numerator.bit_length(),r.denominator.bit_length())>8192:return None
    return r


def _source_fixed_storage(lookup,ref):
    from pr_next_joint.frontend.path_ir import walk, lit
    decl=lookup.nodes.get(ref,{})
    if not decl.get('stateVariable'):return None
    value=decl.get('value');constructor_writer=None
    bases=set(lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']]))
    if decl.get('scope') not in bases:return None
    roots=[lookup.nodes[c] for c in bases]
    if value is None:
        assignments=[n for root in roots for n in walk(root) if n.get('nodeType')=='Assignment' and n.get('operator')=='=' and n.get('leftHandSide',{}).get('nodeType')=='Identifier' and n['leftHandSide'].get('referencedDeclaration')==ref]
        from pr_next_joint.frontend.source_entry_identity import function_kind
        constructors={n.get('id') for root in roots for fn in root.get('nodes',[]) if fn.get('nodeType')=='FunctionDefinition' and function_kind(fn)=='constructor' for n in walk(fn)}
        if len(assignments)!=1 or assignments[0].get('id') not in constructors:return None
        constructor_writer=assignments[0]['id'];value=assignments[0]['rightHandSide']

    # Include compiler-bound library/local callees; their assembly can modify
    # caller storage even though its body is outside the inheritance nodes.
    seen=set(bases);pending=list(roots)
    while pending:
        scope=pending.pop()
        for n in walk(scope):
            callee_ref=(n.get('expression',{}) if n.get('nodeType')=='FunctionCall' else n.get('modifierName',{}) if n.get('nodeType')=='ModifierInvocation' else {}).get('referencedDeclaration')
            target=lookup.nodes.get(callee_ref,{})
            if target.get('nodeType') in ('FunctionDefinition','ModifierDefinition') and target.get('body') and callee_ref not in seen:
                seen.add(callee_ref);roots.append(target);pending.append(target)
    # Assembly and delegate execution can write slots without an AST lvalue.
    if any(n.get('nodeType')=='InlineAssembly' or n.get('nodeType')=='MemberAccess' and n.get('memberName') in ('delegatecall','callcode') for root in roots for n in walk(root)):return None
    for root in roots:
        for n in walk(root):
            left=n.get('leftHandSide') if n.get('nodeType')=='Assignment' else n.get('subExpression') if n.get('nodeType')=='UnaryOperation' and n.get('operator') in ('++','--','delete') else None
            if left and any(x.get('referencedDeclaration')==ref for x in walk(left)) and n.get('id')!=constructor_writer:return None
    number=rational_constant(value)
    if number is None or number.denominator!=1:return None
    typ=decl.get('typeDescriptions',{}).get('typeString','')
    import re
    match=re.fullmatch(r'uint(\d*)',typ)
    if not match or not 0<=number.numerator<2**int(match[1] or 256):return None
    lookup.__dict__.setdefault('source_fixed_storage_facts',{})[ref]={'source':lookup.anchor(decl),'value':number.numerator,'basis':'literal declaration or unique constructor assignment, complete source lvalue scan, no assembly/delegate writes in selected inheritance scope','scope':'original compiled contract source; no deployed upgrade/history proof'}
    return lit(number.numerator)


def source_fixed_storage(lookup,ref):
    import copy
    # A runtime invariant is not an lvalue or a pre-write value while executing
    # the constructor which establishes it. Constants retain their source value.
    if getattr(lookup,'source_execution_context',{}).get('kind')=='constructor' and not lookup.nodes.get(ref,{}).get('constant'):
        return None
    cache=lookup.__dict__.setdefault('_source_fixed_storage_cache',{})
    if ref not in cache:cache[ref]=_source_fixed_storage(lookup,ref)
    return copy.deepcopy(cache[ref])

```

## source/src/pr_next_joint/frontend/local_constants.py

SHA-256 `8f6c667150cc172e2183310ed50c54449bd4432b880ac9622aa0fd1707698657`

```python
"""Pure compiler expressions, not inferred permission or safety."""
from fractions import Fraction
def constant_integer(node):
    """Bounded constant folding only; caller must establish compiler constant type."""
    budget=[128]
    def visit(n):
        budget[0]-=1
        if budget[0]<0:raise ValueError('constant_budget')
        k=n.get('nodeType')
        if k=='Literal' and n.get('kind')=='number':
            v=n.get('value','').replace('_','')
            value=Fraction(int(v,16)) if v.lower().startswith('0x') else Fraction(v)
            units={'wei':1,'szabo':10**12,'finney':10**15,'gwei':10**9,'ether':10**18,'seconds':1,'minutes':60,'hours':3600,'days':86400,'weeks':604800,'years':31536000}
            if n.get('subdenomination'):
                value*=units[n['subdenomination']]
            return value
        if k=='TupleExpression' and len(n.get('components',[]))==1:return visit(n['components'][0])
        if k=='UnaryOperation' and n.get('operator') in ('+','-'):
            value=visit(n['subExpression']);return value if n['operator']=='+' else -value
        if k=='BinaryOperation':
            a,b=visit(n['leftExpression']),visit(n['rightExpression']);op=n.get('operator')
            if op=='+':return a+b
            if op=='-':return a-b
            if op=='*':return a*b
            if op=='/' and b:return a/b
            if op=='**' and b.denominator==1 and 0<=b<=1024 and abs(a.numerator).bit_length()*int(b)<=8192:return a**int(b)
            if op=='%' and a.denominator==b.denominator==1 and b:return a%b
        raise ValueError('not_a_supported_constant')
    try:
        value=visit(node)
        return value.numerator if value.denominator==1 else None
    except (ValueError,KeyError,ZeroDivisionError,OverflowError):return None

def pure_message_argument(node,lookup):
    # Reading a string variable cannot call out or change storage. Indexing,
    # concatenation, function calls and computed error arguments are not erased.
    if node.get('nodeType')=='Literal':return True
    if node.get('nodeType')=='Identifier':
        decl=lookup.nodes.get(node.get('referencedDeclaration'),{})
        typ=decl.get('typeDescriptions',{}).get('typeString','')
        return decl.get('nodeType')=='VariableDeclaration' and typ.startswith(('string','bytes '))
    return False

import re

def scalar_default(declaration):
    typ=declaration.get('typeDescriptions',{}).get('typeString','')
    if typ=='bool':return {'kind':'literal','value':False}
    if re.fullmatch(r'(?:u?int\d*|address(?: payable)?|bytes\d+)',typ):return {'kind':'literal','value':0}
    return {'kind':'unknown','reason':'local_default_type_not_lowered'}

def function_scoped_locals(lookup):
    raw=lookup.bundle.get('compiler',{})
    text=raw.get('version',raw.get('compiler_version','')) if isinstance(raw,dict) else str(raw)
    if not text:text=str(lookup.bundle.get('compiler_version',''))
    m=re.search(r'(\d+)\.(\d+)\.(\d+)',text)
    return bool(m and tuple(map(int,m.groups()))<(0,5,0))

def cast_constant(typ,value):
    from pr_next_joint.verification.typed_integer import integer_type
    integer=integer_type(typ)
    if integer is None or value.get('kind')!='literal' or type(value.get('value')) is not int:return None
    signed,bits=integer;result=value['value']%(2**bits)
    if signed and result>=2**(bits-1):result-=2**bits
    return {'kind':'literal','value':result}


def constant_local_update(lookup,node,value,state,source,operator):
    from pr_next_joint.verification.typed_integer import integer_type, checked_mode
    import copy
    if node.get('nodeType')!='Identifier' or operator not in ('+=','-=','*='):return None
    ref=node.get('referencedDeclaration');before=state.get('env',{}).get(ref,{})
    decl=lookup.nodes.get(ref,{})
    typ=decl.get('typeDescriptions',{}).get('typeString','')
    if decl.get('stateVariable') or decl.get('storageLocation')=='storage' or integer_type(typ) is None:return None
    if not all(v.get('kind')=='literal' and type(v.get('value')) is int for v in (before,value)):return None
    if checked_mode(lookup,state):return None
    a,b=before['value'],value['value'];raw={'+=':lambda:a+b,'-=':lambda:a-b,'*=':lambda:a*b}[operator]()
    result=cast_constant(typ,{'kind':'literal','value':raw});state['env'][ref]=copy.deepcopy(result)
    from pr_next_joint.frontend.source_bindings import observe
    observe(state,decl,result,state['env'])
    state.setdefault('exact_constant_arithmetic',[]).append({'source':lookup.anchor(source),'before':copy.deepcopy(before),'after':copy.deepcopy(result),'compiler_wrapping':True})
    return result


def forward_local_defaults(lookup,function):
    """Cache immutable AST facts; initialize only locals used before declaration.

    Ordinary declarations still use the existing statement initialization.
    No path-dependent values or permissions are cached across invocations.
    """
    cache=getattr(lookup,'_legacy_forward_local_defaults',None)
    if cache is None:cache={};lookup._legacy_forward_local_defaults=cache
    identity=function['id']
    if identity in cache:return cache[identity]
    if not function_scoped_locals(lookup):cache[identity]={};return cache[identity]
    from pr_next_joint.frontend.path_ir import walk
    nodes=list(walk(function.get('body')))
    declarations={n['id']:n for n in nodes if n.get('nodeType')=='VariableDeclaration' and not n.get('stateVariable')}
    needed=set()
    for n in nodes:
        ref=n.get('referencedDeclaration')
        if n.get('nodeType')!='Identifier' or ref not in declarations:continue
        use=n.get('src','').split(':');decl=declarations[ref].get('src','').split(':')
        if len(use)==len(decl)==3 and use[2]==decl[2] and int(use[0])<int(decl[0]):needed.add(ref)
    cache[identity]={ref:scalar_default(declarations[ref]) for ref in needed}
    return cache[identity]

```

## source/src/pr_next_joint/frontend/native_facts.py

SHA-256 `3417d735fcd64b2b77a5ece89e1182b8caf431893c56662ce1ffeff6e905aa52`

```python
"""Serialize fresh Slither SSA with original source anchors, no classifier."""
import sys
from importlib.metadata import version

def source(x):
 s=x.source_mapping
 return {'file':str(s.filename.relative),'start':s.start,'length':s.length,'lines':s.lines}
def variable(v):return {'name':str(v),'class':type(v).__name__,'type':str(getattr(v,'type',None)),'canonical_name':getattr(v,'canonical_name',None)}
def extract(slither,bundle,receipt):
 functions=[]
 for contract in slither.contracts:
  for f in contract.functions_and_modifiers_declared:
   nodes=[]
   for n in f.nodes:
    ops=[]
    for ir in n.irs_ssa:
     op={'operation':type(ir).__name__,'text':str(ir),'reads':[variable(v) for v in ir.read],'lvalue':variable(ir.lvalue) if getattr(ir,'lvalue',None) is not None else None}
     for k in ['variable_left','variable_right','function','arguments']:
      if hasattr(ir,k):op[k]=[str(a) for a in ir.arguments] if k=='arguments' else str(getattr(ir,k))
     ops.append(op)
    nodes.append({'id':n.node_id,'type':str(n.type),'source':source(n),'expression':str(n.expression),'ssa':ops,'successors':[s.node_id for s in n.sons]})
   functions.append({'contract':contract.name,'signature':f.full_name,'canonical_name':f.canonical_name,'source':source(f),'visibility':f.visibility,'parameters':[variable(v) for v in f.parameters],'reads':[v.canonical_name for v in f.all_state_variables_read()],'writes':[v.canonical_name for v in f.all_state_variables_written()],'modifiers':[m.canonical_name for m in f.modifiers],'nodes':nodes})
 return {'program_id':bundle['program_id'],'build_id':bundle['build_id'],'python':sys.version,'slither':version('slither-analyzer'),'crytic_compile':version('crytic-compile'),'compiler':receipt,'functions':functions,'ssa_operation_count':sum(len(n['ssa']) for f in functions for n in f['nodes']),'fresh':True}

```

## source/src/pr_next_joint/frontend/path_ir.py

SHA-256 `577e4c48e759f6acca820d6c06d926aaa9277ab9cfac8cc19b8f05a27909e0c3`

```python
"""Bounded source path analysis, not an EVM or a symbolic execution backend.

Reuse compiler declaration resolution. Preserve branch polarity, modifier order,
write/guard order and reverting exits. Unsupported semantics remain named gaps.
"""
import copy
import json
import re
from pr_next_joint.frontend.source_paths import SourcePaths
from pr_next_joint.frontend.source_work_budget import visit as budget_visit


class ExpressionLimit(ValueError):
    """A local symbolic expression exceeds its original structural budget."""


def clean(v):
    # Memo is local to this read-only traversal: it never survives mutation.
    from pr_next_joint.frontend.source_work_budget import metric
    metric("clean_calls");memo={};remaining=50000;string_bytes=0
    def visit(value,depth):
        nonlocal remaining,string_bytes
        metric("max_depth",depth,True)
        if depth>100:raise ExpressionLimit('SOURCE_EXPRESSION_EXPANSION_LIMIT:nodes=50000,depth=100')
        ident=id(value)
        if isinstance(value,(dict,list)) and ident in memo:
            result,nodes,chars,subdepth=memo[ident];remaining-=nodes;string_bytes+=chars
            metric("shared_subtree_hits")
            if remaining<0 or depth+subdepth>100:raise ExpressionLimit('SOURCE_EXPRESSION_EXPANSION_LIMIT:nodes=50000,depth=100')
            if string_bytes>1048576:raise ValueError('SOURCE_EXPRESSION_STRING_LIMIT:bytes=1048576')
            return result
        budget_visit();remaining-=1
        if remaining<0:raise ExpressionLimit('SOURCE_EXPRESSION_EXPANSION_LIMIT:nodes=50000,depth=100')
        before=remaining;before_bytes=string_bytes
        if isinstance(value,str):
            string_bytes+=len(value.encode('utf8'))
            if string_bytes>1048576:raise ValueError('SOURCE_EXPRESSION_STRING_LIMIT:bytes=1048576')
        if isinstance(value,list):result=[visit(x,depth+1) for x in value]
        elif isinstance(value,dict):result={k:visit(x,depth+1) for k,x in value.items() if k not in ('label','name','source','index_source','origins')}
        else:return value
        # Depth is calculated from the already cleaned representation, not
        # by traversing the original symbolic state again.
        def child_depth(x):
            return memo[id(x)][3]+1 if isinstance(x,(dict,list)) and id(x) in memo else 1
        children=value.values() if isinstance(value,dict) else value
        subdepth=max((child_depth(x) for x in children),default=0)
        memo[ident]=(result,1+before-remaining,string_bytes-before_bytes,subdepth)
        return result
    result=visit(v,0);metric("max_expression_nodes",50000-remaining,True)
    return result

def _clean_key(v):
    text=json.dumps(v,sort_keys=True,separators=(',',':'))
    if len(text)>262144:raise ExpressionLimit('SOURCE_EXPRESSION_KEY_LIMIT:characters=262144')
    return text

def key(v):return _clean_key(clean(v))

def lit(v): return {'kind':'literal','value':v}
def op(name,*args): return {'kind':'op','op':name,'args':list(args)}


def walk(v):
    if isinstance(v,dict):
        yield v
        # Binding observations are provenance, not additional executable effects.
        for name,x in v.items():
            if name not in ('_source_value_bindings','_source_lvalue_bindings'):yield from walk(x)
    elif isinstance(v,list):
        for x in v: yield from walk(x)


from functools import lru_cache
@lru_cache(maxsize=256)
def _normalized_text(text):
    return _clean_key(_normalize_clean(json.loads(text)))

def normalize(v):
    try:text=key(v)
    except ValueError as error:
        # The text key bounds only optional memoization. Normalize the original
        # bounded expression directly if its serialized cache key is too large.
        # Core expression/depth/work limits still apply; no term is dropped.
        if not str(error).startswith('SOURCE_EXPRESSION_KEY_LIMIT:'):raise
        return _normalize_clean(clean(v))
    if len(text)>16384:return _normalize_clean(json.loads(text))
    before=_normalized_text.cache_info().hits
    result=_normalized_text(text)
    if _normalized_text.cache_info().hits>before:
        from pr_next_joint.frontend.source_work_budget import metric
        metric("normalization_cache_hits")
    # A fresh value prevents callers changing cached objects.
    return json.loads(result)


def _normalize_clean(v):
    if not isinstance(v,dict) or v.get('kind')!='op': return v
    args=[_normalize_clean(x) for x in v['args']]; operator=v['op']
    if operator in ('and','&&','or','||'):
        conjunction=operator in ('and','&&');flat=[]
        for a in args:
            if a==lit(not conjunction):return a
            if a==lit(conjunction):continue
            if a.get('kind')=='op' and (a['op'] in ('and','&&') if conjunction else a['op'] in ('or','||')):flat.extend(a['args'])
            else:flat.append(a)
        args=list({_clean_key(x):x for x in flat}.values())
        if not args:return lit(conjunction)
        if len(args)==1:return args[0]
        operator='and' if conjunction else 'or'
    if len(args)==2:
        if operator in ('+','-','*') and all(x.get('kind')=='literal' and type(x.get('value')) is int for x in args):
            a,b=[x['value'] for x in args];return lit({'+':lambda:a+b,'-':lambda:a-b,'*':lambda:a*b}[operator]())
        if operator in ('<','<=','>','>='):
            a,b=args
            if a==b:return lit(operator in ('<=','>='))
            if all(x.get('kind')=='literal' and type(x.get('value')) is int for x in args):
                x,y=a['value'],b['value']
                return lit({'<':x<y,'<=':x<=y,'>':x>y,'>=':x>=y}[operator])
        if operator in ('+','-') and args[1]==lit(0):return args[0]
        if operator=='*' and args[1]==lit(1):return args[0]
        if operator=='*' and args[0]==lit(1):return args[1]
    if operator in ('==','!=') and len(args)==2:
        a,b=args
        if a==b:return lit(operator=='==')
        if a.get('kind')==b.get('kind')=='literal':return lit((a['value']==b['value'])==(operator=='=='))
        for a,b in (args,args[::-1]):
            if b.get('kind')=='literal' and isinstance(b.get('value'),bool):
                return a if b['value']==(operator=='==') else op('!',a)
        if operator=='!=':return op('!',_normalize_clean(op('==',*args)))
        args=sorted(args,key=_clean_key)
    if operator=='!' and args[0].get('kind')=='literal':return lit(not args[0]['value'])
    if operator=='!' and args[0].get('kind')=='op' and args[0]['op']=='!':return args[0]['args'][0]
    return op(operator,*args)


def dnf(expr, negative=False, limit=64):
    """Finite propositional expansion; unknown arithmetic is NOT solved."""
    return _dnf_normalized(normalize(expr),negative,limit)

def _dnf_normalized(e,negative=False,limit=64):
    if e.get('kind')=='literal' and isinstance(e.get('value'),bool):return [set()] if e['value']!=negative else []
    if e.get('kind')=='op':
        operator=e['op'];args=e['args']
        if operator=='!':return _dnf_normalized(args[0],not negative,limit)
        if operator in ('&&','and','||','or'):
            conjunction=(operator in ('&&','and'))!=negative
            result=[set()] if conjunction else []
            for a in args:
                pieces=_dnf_normalized(a,negative,limit)
                if conjunction:
                    result=[x|y for x in result for y in pieces if not any((k,not sign) in y for k,sign in x)]
                else: result+=pieces
                if len(result)>limit:raise ValueError('P_BOOLEAN_PATH_LIMIT')
            return result
    return [{(_clean_key(e),not negative)}]


def conditions_possible(guards, required=None):
    expr=op('and',*guards)
    if required is not None:expr=op('and',expr,op('!',required))
    def consistent(branch):
        parent={};terms={}
        atoms=[(json.loads(raw),positive) for raw,positive in branch]
        has_equality=any(positive and a.get('kind')=='op' and a['op']=='==' and all(x.get('kind') in ('actual_sender','parameter','storage','literal') for x in a['args']) for a,positive in atoms)
        for raw,_ in (branch if has_equality else []):
            for term in walk(json.loads(raw)):
                if 'kind' in term:terms[_clean_key(term)]=term
        if len(terms)>2048:raise ValueError('P_EQUALITY_TERM_LIMIT')
        def find(k):
            parent.setdefault(k,k)
            if parent[k]!=k:parent[k]=find(parent[k])
            return parent[k]
        def rank(k):
            # Prefer a known constant over its aliases; otherwise a numeric
            # constraint could survive as an unconstrained parameter predicate.
            return ({'literal':0,'actual_sender':1,'parameter':2,'storage':3}.get(json.loads(k).get('kind'),4),len(k),k)
        def union(x,y):
            x,y=find(x),find(y)
            if x==y:return False
            first,second=sorted((x,y),key=rank);parent[second]=first
            return True
        for term in terms:find(term)
        for raw,positive in branch:
            a=json.loads(raw)
            if positive and a.get('kind')=='op' and a['op']=='==' and all(x.get('kind') in ('actual_sender','parameter','storage','literal') for x in a['args']):
                x,y=map(_clean_key,a['args']);union(x,y)
        # A proven key equality also equates reads of the same storage family.
        # Finite congruence closure is needed before replacing whole terms:
        # sender==owners[y], x==y must imply sender==owners[x].
        def children(v):
            if isinstance(v,dict):
                if 'kind' in v:return {'equivalence_class':find(_clean_key(v))}
                return {k:children(x) for k,x in v.items()}
            return [children(x) for x in v] if isinstance(v,list) else v
        for _ in range(len(terms)+1):
            congruent={};changed=False
            for k,term in terms.items():
                signature=_clean_key({name:children(v) for name,v in term.items()})
                if signature in congruent:changed=union(k,congruent[signature]) or changed
                else:congruent[signature]=k
            if not changed:break
        else:raise ValueError('P_EQUALITY_CLOSURE_LIMIT')
        # Equating a variable to two distinct constants is a contradiction,
        # even though representative substitution would erase that difference.
        constants={}
        for term in list(parent):
            value=json.loads(term)
            if value.get('kind')=='literal':constants.setdefault(find(term),set()).add(term)
        if any(len(values)>1 for values in constants.values()):return False
        def replace(v,active=frozenset()):
            k=_clean_key(v)
            if k in active:raise ValueError('P_CYCLIC_EQUALITY_NOT_LOWERED')
            nested=active|{k}
            if k in parent and find(k)!=k:return replace(json.loads(find(k)),nested)
            if isinstance(v,dict):return {k:replace(x,nested) if isinstance(x,(dict,list)) else x for k,x in v.items()}
            return [replace(x,nested) for x in v] if isinstance(v,list) else v
        seen=set();bounds={}
        for raw,positive in branch:
            a=normalize(replace(json.loads(raw)))
            if a.get('kind')=='literal' and isinstance(a.get('value'),bool):
                if a['value']!=positive:return False
                continue
            k=_clean_key(a)
            if (k,not positive) in seen:return False
            seen.add((k,positive))
            if a.get('kind')=='op' and a['op'] in ('<','<=','>','>='):
                x,y=a['args'];cmp=a['op']
                if x.get('kind')=='literal':
                    x,y=y,x;cmp={'<':'>','<=':'>=','>':'<','>=':'<='}[cmp]
                if y.get('kind')=='literal' and isinstance(y.get('value'),int) and x.get('kind')=='parameter':
                    if not positive:cmp={'<':'>=','<=':'>','>':'<=','>=':'<'}[cmp]
                    lo,hi=bounds.get(_clean_key(x),(0 if str(x.get('type','')).startswith('uint') else None,None))
                    v=y['value']
                    if cmp in ('>','>='):lo=max(lo if lo is not None else v-1,v+(cmp=='>'))
                    else:hi=min(hi if hi is not None else v+1,v-(cmp=='<'))
                    if lo is not None and hi is not None and lo>hi:return False
                    bounds[_clean_key(x)]=(lo,hi)
        return True
    # Search one conjunction at a time. Eager DNF multiplied unrelated ORs
    # even when the first satisfying branch or a direct contradiction sufficed.
    # Keep exactly the previous atom/equality/arithmetic abstraction.
    work=0;stack=[([(normalize(expr),False)],set())]
    while stack:
        pending,atoms=stack.pop()
        while pending:
            work+=1
            if work>20000:raise ValueError('P_BOOLEAN_SEARCH_LIMIT:20000')
            node,neg=pending.pop()
            if node.get('kind')=='literal' and isinstance(node.get('value'),bool):
                if node['value']==neg:break
                continue
            if node.get('kind')=='op':
                name=node['op'];args=node['args']
                if name=='!':pending.append((args[0],not neg));continue
                if name in ('and','&&','or','||'):
                    if (name in ('and','&&'))!=neg:
                        children=[(a,neg) for a in args]
                        children.sort(key=lambda x:x[0].get('kind')=='op' and x[0].get('op') in ('or','||','and','&&'),reverse=True)
                        pending.extend(children);continue
                    for a in reversed(args):stack.append((pending+[(a,neg)],set(atoms)))
                    break
            atom=(_clean_key(node),not neg)
            if (atom[0],not atom[1]) in atoms:break
            atoms.add(atom)
        else:
            if consistent(atoms):return True
    return False


class Paths(SourcePaths):
    def __init__(self,bundle,contract,max_paths=48):
        super().__init__(bundle,contract)
        self.limit=max_paths;self.sender={'kind':'actual_sender'}
        self.reads=[];self.writes=[];self.guards=[];self.calls=[];self.unknown=[];self.stack=[]
        self.calldata={'kind':'source_calldata_bytes','scope':'opaque source calldata; content and ABI decoding not modeled'}
        self.current=None
        from pr_next_joint.frontend.read_calls import ReadCalls
        self.read_calls=ReadCalls(self)

    def evaluate(self,n,env):
        if n and n.get('nodeType')=='V16EvaluatedValue':return copy.deepcopy(n['value'])
        from pr_next_joint.frontend.language import rational_constant
        from pr_next_joint.frontend.source_entry_identity import builtin_object
        if (n and n.get('nodeType')=='Identifier' and n.get('name')=='now'
                and type(n.get('referencedDeclaration')) is int
                and n['referencedDeclaration'] not in self.nodes
                and n.get('typeDescriptions',{}).get('typeIdentifier')=='t_uint256'):
            return {'kind':'environment','field':'timestamp','type':'uint256'}
        if (n and n.get('nodeType')=='MemberAccess' and n.get('memberName') in ('number','timestamp')
                and builtin_object(n.get('expression',{}),self,'block')):
            return {'kind':'environment','field':n['memberName'],'type':'uint256'}
        if n and n.get('nodeType')=='MemberAccess' and n.get('memberName')=='length':
            data=n.get('expression',{})
            if (data.get('nodeType')=='MemberAccess' and data.get('memberName')=='data'
                    and builtin_object(data.get('expression',{}),self,'msg')):
                return {'kind':'source_calldata_length','type':'uint256','source':self.anchor(n)}
        if (n and n.get('nodeType')=='MemberAccess' and n.get('memberName')=='sig'
                and builtin_object(n.get('expression',{}),self,'msg')):
            selector=getattr(self,'_entry_selector',None)
            if selector is not None:return lit(selector)
            return {'kind':'unknown','reason':'actual_entry_selector_not_bound'}
        constant=rational_constant(n)
        if constant is not None and constant.denominator==1:return lit(constant.numerator)
        if n and n.get('nodeType')=='Identifier' and n.get('referencedDeclaration') not in env:
            from pr_next_joint.frontend.language import source_fixed_storage
            fixed=source_fixed_storage(self,n.get('referencedDeclaration'))
            if fixed is not None:return fixed
        if n and (n.get('nodeType')=='Conditional' or n.get('nodeType')=='BinaryOperation' and n.get('operator') in ('&&','||')):
            if any(x.get('nodeType')=='Assignment' or x.get('nodeType')=='UnaryOperation' and x.get('operator') in ('++','--','delete') for x in walk(n)):
                self.current['issues'].append({'reason':'conditional_side_effect_not_lowered','source':self.anchor(n)})
                return {'kind':'unknown','reason':'conditional_side_effect_not_lowered'}
        if n and n.get('nodeType')=='Assignment':
            value=self.value(n['rightHandSide'],env)
            return self.put(n['leftHandSide'],value,self.current,n,n['operator'])
        if n and n.get('nodeType')=='MemberAccess' and n.get('expression',{}).get('name')=='tx' and n.get('memberName')=='origin':
            return {'kind':'transaction_origin','type':'address'}
        if n and n.get('nodeType')=='Literal' and n.get('kind')=='number':
            from fractions import Fraction
            text=n['value'].replace('_','')
            number=Fraction(int(text,16)) if text.lower().startswith('0x') else Fraction(text)
            units={'wei':1,'szabo':10**12,'finney':10**15,'gwei':10**9,'ether':10**18,'seconds':1,'minutes':60,'hours':3600,'days':86400,'weeks':604800,'years':31536000}
            unit=n.get('subdenomination')
            if unit:
                if unit not in units:raise ValueError('P_LITERAL_UNIT_NOT_LOWERED:'+unit)
                number*=units[unit]
            if number.denominator!=1:raise ValueError('P_FRACTIONAL_LITERAL_NOT_LOWERED')
            return lit(number.numerator)
        if (n and n.get('nodeType')=='UnaryOperation'
                and n.get('operator') in ('++','--')
                and n.get('subExpression',{}).get('nodeType')=='Identifier'
                and n['subExpression'].get('referencedDeclaration') in env):
            from pr_next_joint.verification.typed_integer import integer_type, checked_mode
            typ=n.get('typeDescriptions',{}).get('typeString','')
            ident=n['subExpression']['referencedDeclaration'];before=env[ident]
            if integer_type(typ) and before.get('kind')=='literal' and type(before.get('value')) is int and not checked_mode(self,self.current):
                from pr_next_joint.frontend.local_constants import cast_constant
                after=cast_constant(typ,lit(before['value']+(1 if n['operator']=='++' else -1)))
                env[ident]=after
                self.current.setdefault('exact_constant_arithmetic',[]).append({'source':self.anchor(n),'before':copy.deepcopy(before),'after':copy.deepcopy(after),'compiler_wrapping':True})
                return copy.deepcopy(after if n.get('prefix') else before)
        if n and n.get('nodeType')=='UnaryOperation' and n.get('operator') in ('++','--'):
            before=self.value(n['subExpression'],env)
            self.put(n['subExpression'],lit(1),self.current,n,'+=' if n['operator']=='++' else '-=')
            return normalize(op('+' if n['operator']=='++' else '-',before,lit(1))) if n.get('prefix') else before
        if n and n.get('nodeType')=='MemberAccess' and n.get('memberName')=='length':
            base=self.value(n['expression'],env)
            typ=n['expression'].get('typeDescriptions',{}).get('typeString','')
            fixed=re.search(r'\[(\d+)\]',typ)
            if fixed and typ.count('[')==1:return lit(int(fixed[1]))
            if base.get('kind')=='array':return lit(len(base['items']))
            if base.get('kind')=='storage' and '[' in typ:
                path={**base,'segments':base.get('segments',[])+[{'length':True}]}
                return next((copy.deepcopy(w['value']) for w in reversed(self.current['writes']) if key(w['path'])==key(path)),path)
            if base.get('kind')=='parameter' and '[' in base.get('type',''):
                return {'kind':'array_length','array':base,'type':'uint256'}
        # solc uses TupleExpression for ordinary parentheses as well as tuples.
        # Only a non-array singleton is transparent. Do this at the AST boundary
        # so guards, index keys, casts, aliases and assignment targets agree.
        if n and n.get('nodeType')=='TupleExpression':
            parts=n.get('components',[])
            if not n.get('isInlineArray',False) and len(parts)==1 and parts[0] is not None:
                return self.evaluate(parts[0],env)
            return {'kind':'array' if n.get('isInlineArray',False) else 'tuple',
                    'items':[self.value(v,env) if v else lit(None) for v in parts]}
        if n and n.get('nodeType')=='IndexAccess':
            base=self.evaluate(n['baseExpression'],env);index=self.value(n.get('indexExpression'),env)
            if base.get('kind')=='array':
                if index.get('kind')=='literal' and type(index.get('value')) is int and 0<=index['value']<len(base['items']):
                    return copy.deepcopy(base['items'][index['value']])
                self.current['issues'].append({'reason':'memory_array_symbolic_or_oob_index','source':self.anchor(n)})
                return {'kind':'unknown','reason':'memory_array_symbolic_or_oob_index'}
        if n and n.get('nodeType')=='FunctionCall':
            f=n.get('expression',{})
            if f.get('nodeType')=='MemberAccess' and f.get('memberName')=='push':
                receiver=f.get('expression',{});typ=receiver.get('typeDescriptions',{}).get('typeString','')
                args=n.get('arguments',[])
                if '[]' in typ and typ.count('[')==1 and len(args)==1:
                    base=self.evaluate(receiver,env)
                    if base.get('kind')=='storage':
                        length={**base,'segments':base.get('segments',[])+[{'length':True}]}
                        before=next((copy.deepcopy(w['value']) for w in reversed(self.current['writes']) if key(w['path'])==key(length)),length)
                        value=self.value(args[0],env)
                        self.current['guards'].append(op('<',before,lit(2**256-1)))
                        self.current['writes'].extend([
                            {'path':{**base,'segments':base.get('segments',[])+[{'key':copy.deepcopy(before)}]},'value':value,'operator':'=','source':self.anchor(n)},
                            {'path':length,'value':op('+',before,lit(1)),'operator':'=','source':self.anchor(n)}])
                        return op('+',before,lit(1))

            if f.get('nodeType')=='MemberAccess' and f.get('expression',{}).get('name')=='abi' and f.get('memberName') in ('encode','encodePacked'):
                args=[self.value(x,env) for x in n.get('arguments',[])]
                types=[x.get('typeDescriptions',{}).get('typeString','') for x in n.get('arguments',[])]
                if f['memberName']=='encodePacked' and any('[' in typ or typ in ('bytes','string') for typ in types):
                    self.current['issues'].append({'reason':'packed_dynamic_encoding_not_lowered','source':self.anchor(n)})
                    return {'kind':'unknown','reason':'packed_dynamic_encoding_not_lowered'}
                return {'kind':'abi_encoding','mode':f['memberName'],'types':types,'arguments':args}
            from pr_next_joint.frontend.source_entry_identity import builtin_call, builtin_object
            if builtin_call(n,self,('keccak256','sha3')):
                arguments=n.get('arguments',[]);args=[self.value(x,env) for x in arguments]
                if len(args)==1 and args[0].get('kind') in ('abi_encoding','fixed_bytes_literal'):
                    return {'kind':'hash','algorithm':'keccak256','input':args[0], 'type':'bytes32'}
                # Before 0.5 the compiler-bound intrinsic accepts a fixed
                # packed tuple directly. It is the same concrete encoding as
                # abi.encodePacked, not a new unconstrained digest input.
                compiler=self.bundle.get('compiler',{})
                version=compiler.get('version',compiler.get('compiler_version','')) if isinstance(compiler,dict) else str(compiler)
                match=re.search(r'(\d+)\.(\d+)\.(\d+)',version)
                if args and match and tuple(map(int,match.groups()))<(0,5,0):
                    types=[x.get('typeDescriptions',{}).get('typeString','') for x in arguments]
                    if all(re.fullmatch(r'(?:u?int\d*|bytes\d+|address|bool)',typ) for typ in types):
                        return {'kind':'hash','algorithm':'keccak256','input':{'kind':'abi_encoding',
                            'mode':'encodePacked','types':types,'arguments':args},'type':'bytes32'}
            blockhash_call=builtin_call(n,self,('blockhash',)) or (
                f.get('nodeType')=='MemberAccess' and f.get('memberName')=='blockhash'
                and builtin_object(f.get('expression',{}),self,'block')
                and f.get('typeDescriptions',{}).get('typeIdentifier','').startswith('t_function_blockhash_'))
            if blockhash_call and len(n.get('arguments',[]))==1:
                return {'kind':'source_block_hash','height':self.value(n['arguments'][0],env),
                    'current':{'kind':'environment','field':'number','type':'uint256'},
                    'type':'bytes32','source':self.anchor(n)}
            if n.get('kind')=='typeConversion' and len(n.get('arguments',[]))==1:
                from pr_next_joint.frontend.source_entry_identity import elementary_expression_name
                typ=elementary_expression_name(f);source=n['arguments'][0]
                from pr_next_joint.frontend.local_constants import cast_constant
                from pr_next_joint.frontend.local_constants import constant_integer
                raw=constant_integer(source)
                if raw is not None:
                    converted=cast_constant(typ,lit(raw))
                    if converted is not None:return converted
                src_type=source.get('typeDescriptions',{}).get('typeString','')
                target_bits=re.fullmatch(r'uint(\d*)',typ);source_bits=re.fullmatch(r'uint(\d*)',src_type)
                if target_bits and source_bits:
                    a=int(source_bits[1] or 256);b=int(target_bits[1] or 256);value=self.value(source,env)
                    if b<a:
                        if value.get('kind')=='literal':return lit(value['value']%(2**b))
                        if not conditions_possible(self.current['guards'],op('<',value,lit(2**b))):return value
                        return {'kind':'uint_narrow','bits':b,'from_bits':a,'input':value,'type':typ}
                    return value

            if n.get('kind') not in ('typeConversion','structConstructorCall'):
                if f.get('nodeType')=='MemberAccess' and f.get('memberName') in ('wrap','unwrap'):
                    return self.value(n['arguments'][0],env)
                from pr_next_joint.frontend.calls import expression_call
                result=expression_call(self,n,env)
                if result is not None:return result
                result=self.read_calls.call(n,env)
                if result is not None:return result
                self.current['issues'].append({'reason':'expression_call_not_lowered','source':self.anchor(n)})
                return {'kind':'unknown','reason':'expression_call_not_lowered'}
        if n and n.get('nodeType')=='MemberAccess':
            from pr_next_joint.frontend.source_local_values import local_root
            if local_root(n.get('expression',{}),self) is not None:
                base=self.evaluate(n.get('expression'),env)
                if base.get('kind')=='record':
                    field=next((f for f in base['fields'] if f['field']==n.get('referencedDeclaration')),None)
                    if field is not None:return copy.deepcopy(field['value'])
            member=self.nodes.get(n.get('referencedDeclaration'),{})
            if member.get('nodeType')=='EnumValue':
                enums=[e for e in self.nodes.values() if e.get('nodeType')=='EnumDefinition' and any(x.get('id')==member['id'] for x in e.get('members',[]))]
                if len(enums)==1:return lit(next(i for i,x in enumerate(enums[0]['members']) if x['id']==member['id']))
        if n and n.get('nodeType')=='Identifier' and n.get('name')=='this':
            return self.read_calls.address()
        result=super().evaluate(n,env)
        if n and n.get('nodeType') in ('Identifier','IdentifierPath') and result.get('kind')=='storage' and n.get('referencedDeclaration') not in env:
            result=self.read_calls.state(result,n.get('referencedDeclaration'))
        return result

    def value(self,n,env):
        v=self.evaluate(n,env)
        # A local value was captured when assigned. Reading the local again
        # must not re-read a state root changed since then (e.g. a saved ID).
        if n and n.get('nodeType')=='Identifier' and n.get('referencedDeclaration') in env:
            v=copy.deepcopy(v)
        elif v.get('kind')=='storage':
            from pr_next_joint.frontend.dispatch import read_after_writes
            v=read_after_writes(v,self.current['writes'],self.current['guards'])
        v=normalize(v)
        from pr_next_joint.frontend.source_bindings import observe
        observe(self.current,n,v,env)
        return v

    def expr(self,n,s):
        self.current=s
        try:return self.value(n,s['env'])
        except (KeyError,ValueError,TypeError) as ex:
            s['issues'].append({'reason':'expression_unresolved','detail':str(ex),'source':self.anchor(n) if n else None})
            return {'kind':'unknown','reason':'expression_unresolved'}

    def left(self,n,s):
        self.current=s
        value=self.evaluate(n,s['env'])
        from pr_next_joint.frontend.source_bindings import observe_lvalue
        observe_lvalue(s,n,value)
        return value

    def put(self,n,value,s,source,operator='='):
        from pr_next_joint.frontend.local_constants import constant_local_update
        constant=constant_local_update(self,n,value,s,source,operator)
        if constant is not None:return constant
        if n.get('nodeType')=='TupleExpression' and not n.get('isInlineArray',False):
            parts=n.get('components',[])
            if len(parts)==1 and parts[0] is not None:return self.put(parts[0],value,s,source,operator)
            if operator!='=' or value.get('kind')!='tuple' or len(parts)!=len(value.get('items',[])):
                s['issues'].append({'reason':'tuple_assignment_shape_not_lowered','source':self.anchor(source)})
                return {'kind':'unknown','reason':'tuple_assignment_shape_not_lowered'}
            # Solidity evaluates the RHS before any LHS is written. Restrict
            # this summary to distinct locals; aliased storage needs ordering.
            locals_=[p.get('referencedDeclaration') for p in parts if p]
            if len(locals_)!=len(set(locals_)) or any(p and (p.get('nodeType')!='Identifier' or p.get('referencedDeclaration') not in s['env']) for p in parts):
                s['issues'].append({'reason':'tuple_assignment_storage_or_alias_not_lowered','source':self.anchor(source)})
                return {'kind':'unknown','reason':'tuple_assignment_storage_or_alias_not_lowered'}
            for part,item in zip(parts,copy.deepcopy(value['items'])):
                if part:s['env'][part['referencedDeclaration']]=item
            return copy.deepcopy(value)
        if any(x.get('nodeType')=='Assignment' or x.get('nodeType')=='FunctionCall' and not (x.get('kind')=='typeConversion' and len(x.get('arguments',[]))==1) or x.get('nodeType')=='UnaryOperation' and x.get('operator') in ('++','--','delete') for x in walk(n)):
            s['issues'].append({'reason':'assignment_lvalue_side_effects_not_lowered','source':self.anchor(source)})
            return {'kind':'unknown','reason':'assignment_lvalue_side_effects_not_lowered'}
        from pr_next_joint.frontend.source_local_values import local_root, assign
        local_composite=local_root(n,self)
        if local_composite is not None and n.get('nodeType')!='Identifier':
            try:
                if operator not in ('=','delete'):value=normalize(op(operator[:-1],self.left(n,s),value))
                if operator=='delete':value=lit(0)
                assign(n,value,self,s);return copy.deepcopy(value)
            except (ValueError,KeyError,TypeError) as error:
                s['issues'].append({'reason':str(error),'source':self.anchor(source)})
                return {'kind':'unknown','reason':str(error)}
        lhs=self.left(n,s)
        decl=self.nodes.get(n.get('referencedDeclaration'),{})
        local_value=(n.get('nodeType')=='Identifier' and not decl.get('stateVariable')
                     and decl.get('storageLocation')!='storage'
                     and n.get('referencedDeclaration') in s['env'])
        if local_value:
            if operator not in ('=','delete'):
                value=normalize(op(operator[:-1],copy.deepcopy(lhs),value))
            if operator=='delete':
                typ=decl.get('typeDescriptions',{}).get('typeString','')
                value=lit(False) if typ=='bool' else lit(0) if re.fullmatch(r'(?:u?int\d*|address(?: payable)?|bytes\d+)',typ) else {'kind':'unknown','reason':'local_delete_type_not_lowered'}
            s['env'][n['referencedDeclaration']]=copy.deepcopy(value)
            from pr_next_joint.frontend.source_bindings import observe
            observe(s,decl,value,s['env'])
        elif lhs.get('kind')=='storage':
            from pr_next_joint.frontend.dispatch import read_after_writes
            before=read_after_writes(lhs,s['writes'],s['guards'])
            increment=None
            if operator in ('+=','-='):increment=value if operator=='+=' else op('-',lit(0),value)
            if operator not in ('=','delete'):value=normalize(op(operator[:-1],before,value))
            if operator=='delete':value={'kind':'zero_of_storage_type'}
            # Record the sequential read as well as the local additive effect.
            # Consumers must not subtract a pre-transaction slot from a later read.
            if operator=='=' and value.get('kind')=='op' and value.get('op') in ('+','-') and key(value['args'][0])==key(before):
                increment=value['args'][1] if value['op']=='+' else op('-',lit(0),value['args'][1])
            s['writes'].append({'path':clean(lhs),'value':value,'operator':operator,'source':self.anchor(source),
                'local_increment':copy.deepcopy(increment)})
        elif n.get('nodeType')=='Identifier':
            if operator not in ('=','delete'):value=normalize(op(operator[:-1],copy.deepcopy(lhs),value))
            s['env'][n['referencedDeclaration']]=value
        else:
            s['issues'].append({'reason':'assignment_target_not_lowered','source':self.anchor(source)})
            return {'kind':'unknown','reason':'assignment_target_not_lowered'}
        return copy.deepcopy(value)

    def statements(self,stmts,states,depth):
        for n in stmts:
            out=[]
            for s in states:
                out.extend(self.statement(n,s,depth) if s['flow']=='normal' else [s])
            if len(out)>self.limit:raise ValueError('P_SOURCE_PATH_LIMIT')
            states=out
        return states

    def event_statement(self,call,s):
        declaration=self.nodes.get((call or {}).get('expression',{}).get('referencedDeclaration'),{})
        if not call or call.get('nodeType')!='FunctionCall' or declaration.get('nodeType')!='EventDefinition':
            s['issues'].append({'reason':'event_declaration_not_bound','source':self.anchor(call) if call else None})
            return [s]
        arguments=call.get('arguments',[])
        if len(arguments)!=len(declaration.get('parameters',{}).get('parameters',[])):
            s['issues'].append({'reason':'event_argument_arity','source':self.anchor(call)})
        if any(n.get('nodeType')=='Assignment' or
                n.get('nodeType')=='UnaryOperation' and n.get('operator') in ('++','--','delete') for n in walk(arguments)):
            s['issues'].append({'reason':'event_argument_side_effect_not_fully_lowered','source':self.anchor(call)})
        if any(n.get('nodeType')=='IndexAccess' and n.get('baseExpression',{}).get('typeDescriptions',{}).get('typeIdentifier','').startswith(('t_array','t_bytes','t_string')) for n in walk(arguments)):
            s['issues'].append({'reason':'event_argument_array_bounds_not_lowered','source':self.anchor(call)})
        values=[]
        for argument in arguments:
            value=self.expr(argument,s);values.append(value)
            # Evaluation must not vanish because an event's return is unused.
            # Ordinary P queries do not yet encode every unused fallible term;
            # keep this limited case explicitly unresolved rather than ignore it.
            if any(v.get('kind') in ('unknown','call_unresolved','uint_narrow','enum_cast','index') or
                    v.get('kind')=='op' and v.get('op') in ('+','-','*','/','%','**','<<','>>') and not getattr(self,'captures_evaluated_terms',False) for v in walk(value)):
                s['issues'].append({'reason':'event_argument_fallible_value_not_lowered','source':self.anchor(argument)})
        s.setdefault('source_events',[]).append({'source':self.anchor(call),'declaration_ast_id':declaration['id'],
            'arguments':clean(values),'event_not_used_as_effect_proof':True})
        return [s]

    def statement(self,n,s,depth):
        if not n:return [s]
        kind=n.get('nodeType')
        if kind=='InlineAssembly':
            from pr_next_joint.frontend.bytes import summarize
            pure_reads=summarize(self,n,s)
            if pure_reads is not None:return pure_reads
            from pr_next_joint.frontend.assembly import forward
            summarized=forward(self,n,s)
            if summarized is not None:return summarized
        from pr_next_joint.frontend.calls import expand_value_statement
        expanded=expand_value_statement(self,n,s,depth)
        if expanded is not None:return expanded
        if kind in ('Block','UncheckedBlock'):
            if kind=='UncheckedBlock' and not getattr(self,'captures_evaluated_terms',False):
                s['issues'].append({'reason':'unchecked_arithmetic_scope','source':self.anchor(n)})
            previous=s.get('_unchecked_depth',0)
            if kind=='UncheckedBlock':
                s['_unchecked_depth']=previous+1
                s.setdefault('arithmetic_scope',[]).append({'source':self.anchor(n),'scope':'nonwrapping_uint256_subcase; narrow signed types retain exact modular arithmetic','overflow_cases_not_exhausted':True})
            result=self.statements(n.get('statements',[]),[s],depth)
            if kind=='UncheckedBlock':
                for branch in result:branch['_unchecked_depth']=previous
            return result
        if kind=='IfStatement':
            c=self.expr(n['condition'],s);out=[]
            for sign,body in [(True,n.get('trueBody')),(False,n.get('falseBody'))]:
                child=copy.deepcopy(s);child['guards'].append(c if sign else op('!',c))
                child.setdefault('branch_choices',[]).append({'condition':copy.deepcopy(c),'sign':sign,'source':self.anchor(n)})
                if conditions_possible(child['guards']):out+=self.statement(body,child,depth)
            return out
        if kind in ('ForStatement','WhileStatement'):
            states=self.statement(n.get('initializationExpression'),s,depth)
            from pr_next_joint.frontend.source_loop_scope import loop_limit
            bound=max(loop_limit(n,self,x) for x in states) if states else 0
            from pr_next_joint.frontend.source_loop_scope import invariant_local_condition
            invariant=invariant_local_condition(n,self)
            if invariant:bound=0
            completed=[]
            for iteration in range(bound+1):
                next_states=[]
                for current in states:
                    condition=self.expr(n.get('condition'),current) if n.get('condition') else lit(True)
                    stop=copy.deepcopy(current);stop['guards'].append(op('!',condition))
                    stop.setdefault('loop_scopes',[]).append({'source':self.anchor(n),'iterations':iteration,'complete_loop':True})
                    if conditions_possible(stop['guards']):completed.append(stop)
                    active=copy.deepcopy(current);active['guards'].append(condition)
                    if not conditions_possible(active['guards']):continue
                    if iteration==bound:
                        active['issues'].append({'reason':'source_loop_bound_exceeded','source':self.anchor(n),'unrolled_iterations':bound,**({'loop_condition_invariant':True,'reason_detail':'local boolean unchanged; no successful exit in compiled loop body'} if invariant else {})})
                        active['flow']='truncated';completed.append(active);continue
                    for body in self.statement(n.get('body'),active,depth):
                        if body['flow'] in ('normal','continue'):
                            body['flow']='normal';next_states.extend(self.statement(n.get('loopExpression'),body,depth))
                        elif body['flow']=='break':
                            body['flow']='normal';completed.append(body)
                        else:completed.append(body)
                if len(completed)+len(next_states)>self.limit:raise ValueError('P_SOURCE_PATH_LIMIT')
                states=next_states
            return completed
        if kind in ('Break','Continue'):s['flow']=kind.lower();return [s]
        if kind in ('RevertStatement','Throw'):s['flow']='reverted';return [s]
        if kind=='Return':
            if n.get('expression'):
                value=self.expr(n['expression'],s);s['return_value']=value
                ids=s.get('_return_ids',[])
                values=[value] if len(ids)==1 else value.get('items',[]) if value.get('kind')=='tuple' else []
                if len(values)!=len(ids):s['issues'].append({'reason':'function_return_arity_not_lowered','source':self.anchor(n)})
                else:
                    for ident,returned in zip(ids,values):s['env'][ident]=copy.deepcopy(returned)
            s['flow']='returned';return [s]
        if kind=='ModifierContinuation':
            results=self.statement(n['body'],s,depth)
            for result in results:
                if result['flow']=='returned' and not result.get('_evm_halted'):
                    result['flow']='normal';result['_return_pending']=True
            return results
        if kind=='EmitStatement':return self.event_statement(n.get('eventCall'),s)
        if kind=='PlaceholderStatement':return [s]
        if kind=='VariableDeclarationStatement':
            v=self.expr(n.get('initialValue'),s)
            ds=n['declarations']
            for i,d in enumerate(ds):
                if d:
                    value=v if len(ds)==1 else copy.deepcopy(v['items'][i]) if v.get('kind')=='tuple' and len(v.get('items',[]))==len(ds) else {'kind':'unknown','reason':'tuple_local_arity'}
                    if n.get('initialValue') is None:
                        typ=d.get('typeDescriptions',{}).get('typeString','')
                        value=lit(False) if typ=='bool' else lit(0) if typ.startswith(('uint','int','address','bytes')) and '[' not in typ else {'kind':'unknown','reason':'uninitialized_local_type_not_lowered'}
                    if d.get('storageLocation')=='memory' and value.get('kind')=='storage':
                        from pr_next_joint.frontend.source_local_values import snapshot
                        try:value=snapshot(value,d.get('typeName',{}),self,s)
                        except ValueError as error:
                            s['issues'].append({'reason':str(error),'source':self.anchor(n)});value={'kind':'unknown','reason':str(error)}
                    s['env'][d['id']]=value
                    if value.get('kind')=='parameter' and n.get('initialValue'):
                        s.setdefault('copy_origins',[]).append({'declaration':d['id'],'value':copy.deepcopy(value),'source':self.anchor(n)})
                    if n.get('initialValue') is not None:
                        from pr_next_joint.frontend.source_bindings import observe
                        observe(s,d,value,s['env'])
            return [s]
        if kind=='ExpressionStatement':
            e=n['expression'];k=e.get('nodeType')
            if k=='Assignment':self.put(e['leftHandSide'],self.expr(e['rightHandSide'],s),s,e,e['operator']);return [s]
            if k=='UnaryOperation' and e.get('operator') in ('++','--','delete'):
                self.put(e['subExpression'],lit(1),s,e,{'++':'+=','--':'-=','delete':'delete'}[e['operator']]);return [s]
            if k=='FunctionCall':
                f=e['expression'];name=f.get('name')
                if self.nodes.get(f.get('referencedDeclaration'),{}).get('nodeType')=='EventDefinition':
                    return self.event_statement(e,s)
                from pr_next_joint.frontend.source_entry_identity import builtin_call
                if builtin_call(e,self):
                    s['guards'].append(self.expr(e['arguments'][0],s))
                    if not conditions_possible(s['guards']):s['flow']='reverted'
                    return [s]
                if builtin_call(e,self,('revert',)):s['flow']='reverted';return [s]
                target=self.fns.get(f.get('referencedDeclaration'))
                from pr_next_joint.frontend.calls import bound_library
                if bound_library(self,e,target):
                    return self.invoke(target,[self.expr(f['expression'],s)]+[self.expr(x,s) for x in e['arguments']],s,depth+1,internal=True)
                if target and f.get('nodeType')=='MemberAccess':
                    from pr_next_joint.frontend.dispatch import member_target
                    selected=member_target(self,e,target)
                    if selected:
                        return self.invoke(selected,[self.expr(x,s) for x in e['arguments']],s,depth+1,internal=True)
                if target and f.get('nodeType')=='Identifier':
                    from pr_next_joint.frontend.calls import bind_arguments
                    bound_args=bind_arguments(self,e,target)
                    if bound_args is None:
                        s['issues'].append({'reason':'named_internal_arguments_not_bound','source':self.anchor(e)})
                        return [s]
                    from pr_next_joint.frontend.dispatch import resolve
                    selected=resolve(self,target,self.read_calls.active_contract)
                    s.setdefault('internal_dispatch',[]).append({'source':self.anchor(e),'referenced':self.anchor(target),'selected':self.anchor(selected),'basis':'compiler_C3_unqualified_internal_call'})
                    return self.invoke(selected,[self.expr(x,s) for x in bound_args],s,depth+1,internal=True)
            self.expr(e,s);return [s]
        s['issues'].append({'reason':'statement_not_lowered','kind':kind,'source':self.anchor(n)})
        return [s]

    def invoke(self,f,args,s,depth=0,internal=False):
        if depth>8:raise ValueError('P_CALL_DEPTH_LIMIT')
        outer_return={k:copy.deepcopy(s[k]) for k in ('_return_ids','_return_pending','return_value') if k in s}
        for name in outer_return:s.pop(name,None)
        outer=copy.deepcopy(s['env']);s['env']={p['id']:a for p,a in zip(f['parameters']['parameters'],args)}
        body=copy.deepcopy(f.get('body'))
        from pr_next_joint.frontend.local_constants import forward_local_defaults
        for identity,value in forward_local_defaults(self,f).items():
            s['env'].setdefault(identity,copy.deepcopy(value))
        return_parameters=f.get('returnParameters',{}).get('parameters',[])
        s['_return_ids']=[parameter['id'] for parameter in return_parameters]
        for parameter in return_parameters:
            typ=parameter.get('typeDescriptions',{}).get('typeString','')
            s['env'][parameter['id']]=lit(False) if typ=='bool' else lit(0) if typ.startswith(('uint','int','address','bytes')) and '[' not in typ else {'kind':'unknown','reason':'return_default_type_not_lowered'}
        # Expand modifier placeholders in their actual enclosing order.
        for m in reversed(f.get('modifiers',[])):
            mod=self.fns.get(m['modifierName'].get('referencedDeclaration'))
            if not mod or mod.get('nodeType')!='ModifierDefinition':
                s['issues'].append({'reason':'modifier_not_lowered'});continue
            for p,a in zip(mod['parameters']['parameters'],m.get('arguments') or []):s['env'][p['id']]=self.expr(a,s)
            replacement=body
            def expand(v):
                if isinstance(v,dict):
                    if v.get('nodeType')=='PlaceholderStatement':return {'nodeType':'ModifierContinuation','body':copy.deepcopy(replacement)}
                    return {k:expand(x) for k,x in v.items()}
                return [expand(x) for x in v] if isinstance(v,list) else v
            body=expand(mod['body'])
        results=self.statement(body,s,depth)
        for item in results:
            if item['flow'] not in ('normal','returned'):continue
            if return_parameters:
                values=[copy.deepcopy(item['env'][p['id']]) for p in return_parameters]
                item['return_value']=values[0] if len(values)==1 else {'kind':'tuple','items':values}
            if item.pop('_return_pending',False) or return_parameters:item['flow']='returned'
        if internal:
            for item in results:
                item['env']=copy.deepcopy(outer)
                if item['flow']=='returned' and not item.get('_evm_halted'):item['flow']='normal'
                for name in ('_return_ids','_return_pending','return_value'):item.pop(name,None)
                item.update(copy.deepcopy(outer_return))
        return results

    def run(self,signature):
        f=self.function(signature)
        if not f or 'generated_getter' in f:return []
        self._entry_selector=self.function_selector(f)
        args=[{'kind':'parameter','id':p['id'],'type':p.get('typeDescriptions',{}).get('typeString')} for p in f['parameters']['parameters']]
        state={'env':{},'guards':[],'writes':[],'issues':[],'flow':'normal'}
        self.unknown=[]
        result=self.invoke(f,args,state)
        for s in result:
            s['issues']+=self.unknown
            s.pop('env',None)
            s['entry_source']=self.anchor(f)
        return result

```
