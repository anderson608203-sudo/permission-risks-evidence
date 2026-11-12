# 源码文本 · 1

## collect.py

原文件 SHA-256 `a1f4afb64e261fe51c4e6891442136292953554cecd3456ffcab45dbf13a7367`

````python
"""User-run Linux collection. Read the finished run once and hash the compressed stream."""
import fcntl
import gzip
import hashlib
import json
import os
from pathlib import Path
import signal
import sys
import tarfile
import time

def main():
    root=Path(__file__).resolve().parent
    run=root/'run'
    if not (run/'AUTHORIZATION.json').is_file():
        raise SystemExit('尚无本批正式启动记录。')
    locks=[]
    for name in ('START_LOCK','SUPERVISOR_LOCK'):
        lock=(run/name).open('a');locks.append(lock)
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise SystemExit('本批仍在启动或运行，请等待结束后再打包。')
    complete=(run/'ENDED.json').is_file() and (run/'PREDICTIONS_FROZEN.json').is_file()
    if not complete and '--interrupted' not in sys.argv:
        raise SystemExit('缺少结束或冻结记录。如已确认意外中断，可附加 --interrupted 收取原状。')
    destination=root.parent/'PR_Next200_Results.tar.gz'
    checksum=destination.with_suffix(destination.suffix+'.sha256')
    receipt=root/'COLLECTION.json'
    records=json.loads(receipt.read_bytes()) if receipt.exists() else []
    if destination.exists() and checksum.exists():
        print('已有收取包，请下载：',destination,checksum,sep='\n');return
    if destination.exists():
        raise SystemExit('已存在尚无校验回执的结果包，保留原件，请通知 Work。')
    if any(r.get('end') is None for r in records):
        raise SystemExit('前次收取计时未结清，保留现场，请通知 Work。')
    limit=json.loads((root/'CHAT_APPROVAL.json').read_bytes())['collection_seconds']
    remaining=limit-sum(r['elapsed'] for r in records)
    if remaining<=0:raise SystemExit('本批打包时间已用完，保留原始结果。')
    start=time.monotonic()
    records.append({'start':time.time(),'end':None})
    def record():
        tmp=receipt.with_suffix('.tmp');tmp.write_text(json.dumps(records,indent=2));os.replace(tmp,receipt)
    record()
    def alarm(*args):raise TimeoutError('collection_time_limit')
    signal.signal(signal.SIGALRM,alarm);signal.setitimer(signal.ITIMER_REAL,remaining)
    tmp=destination.with_name(destination.name+'.'+str(time.time_ns())+'.part')
    digest=hashlib.sha256()
    class Sink:
        def __init__(self,f):self.f=f
        def write(self,data):
            written=self.f.write(data);digest.update(data[:written]);return written
        def flush(self):self.f.flush()
    try:
        with tmp.open('xb') as output, gzip.GzipFile(filename='',fileobj=Sink(output),mode='wb',compresslevel=1,mtime=0) as gz, tarfile.open(fileobj=gz,mode='w|') as tar:
            shipped=[root/r['path'] for r in json.loads((root/'MANIFEST.json').read_bytes())['files']]
            chosen=set(shipped+[root/'MANIFEST.json',root/'CHAT_APPROVAL.json'])|set(run.rglob('*'))
            for p in sorted(chosen):
                if p.is_symlink():raise ValueError('unexpected symlink: '+str(p.relative_to(root)))
                if not p.is_file() or p==receipt:continue
                if p.name in {'.env','.netrc','credentials','id_rsa','id_ed25519'} or p.suffix in {'.pem','.key'}:
                    raise ValueError('unexpected credential file: '+str(p.relative_to(root)))
                tar.add(p,arcname=p.relative_to(root).as_posix(),recursive=False)
        size=tmp.stat().st_size;os.replace(tmp,destination)
        records[-1].update(bytes=size,sha256=digest.hexdigest(),original_end_and_freeze_present=complete)
        checksum.write_text(digest.hexdigest()+'  '+destination.name+'\n# collection_start_epoch='+str(records[-1]['start'])+' end_epoch='+str(time.time())+' cumulative_seconds='+str(sum(r['elapsed'] for r in records[:-1])+time.monotonic()-start)+'\n',encoding='ascii')
        print('打包完成。请下载下列两个文件：',destination,checksum,sep='\n')
    except BaseException as exc:
        records[-1]['error']=type(exc).__name__+': '+str(exc)
        raise
    finally:
        signal.setitimer(signal.ITIMER_REAL,0);records[-1].update(end=time.time(),elapsed=time.monotonic()-start);record()
if __name__=='__main__':main()

````

## run/technical_recovery_2_r1/changes.patch

原文件 SHA-256 `20bb8aca81acf9927e04c12ccf3a7dd2bca266f7eabde5d4e507d91356e131bf`

````text
--- parent/properties.py
+++ successor/properties.py
@@ -107,7 +107,7 @@
     facts=inv.f; target=facts.operations[use]['target']
     listed=[]
     for cell in unique_cells(inv.graph.request_reads(use)):
-        if keys(cell) or not value_type(cell,facts.lookup(use)).startswith(('uint','bool')):
+        if keys(cell) or not (value_type(cell,facts.lookup(use)) or '').startswith(('uint','bool')):
             continue
         writers=[]
         for oid in sorted(inv.graph.access[target,cell['root']]['writers']):
--- parent/property_model.py
+++ successor/property_model.py
@@ -258,7 +258,9 @@
                    if inv.evidence[label].get('kind') == 'source_inspection' and inv.evidence[label].get('operation') == root]
     scope['source_deductions'] = [{'evidence': r['id'], 'no_committing_path': r.get('no_committing_path'),
                                  'net_unchanged': r.get('net_effect_proved_unchanged')} for r in inspections]
-    if (item.get('observation') or {}).get('measure') != 'denied_qualified':
+    observation = item.get('observation')
+    measure = observation.get('measure') if isinstance(observation, dict) else None
+    if measure != 'denied_qualified':
         reason = next(('original_root_has_no_committing_path' if r.get('no_committing_path')
                        else 'original_root_net_effect_is_unchanged' for r in inspections
                        if r.get('no_committing_path') or r.get('net_effect_proved_unchanged')), None)
@@ -282,7 +284,7 @@
         if not expected:
             result['reasons'] = ['expected_authorization_not_established']
             return result
-        label = 'denied_qualified' if (item.get('observation') or {}).get('measure') == 'denied_qualified' else 'authorization_violation'
+        label = 'denied_qualified' if measure == 'denied_qualified' else 'authorization_violation'
         relevant = [x for x in queries if x.get('label') == label and x.get('details', {}).get('property_validated')]
         positives = [x for x in relevant if x.get('validated_bounded_witness')]
         source_support = [e for e in current if e.get('kind') == 'source_property_certificate' and

````

## run/technical_recovery_2_r1/continue_second.py

原文件 SHA-256 `a8cd1e6aa9209ac15b982c3c9994ca688880735acb06582fa8a99b10f2ac20f6`

````python
"""Rehydrate the original pre-feedback state, then apply the two consumer guards."""
import ast
import importlib.util
import json
import os
import signal
import socket
import sqlite3
import sys
import time
from pathlib import Path

here=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('checked_recovery',here/'recover.py')
rc=importlib.util.module_from_spec(spec);spec.loader.exec_module(rc)
dst=rc.RUN/'technical_continuation_2_r1'
dst.mkdir(exist_ok=False)
m=rc.TARGETS[1]
base=rc.ROOT/'source'
fix=here/'source'
pin=rc.read(here/'IDENTITY.json')
assert rc.digest(rc.module_hashes(base))==pin['parent']
assert rc.digest(rc.module_hashes(fix))==pin['successor']
assert rc.sha((rc.RUN/'PREDICTIONS_FROZEN.json').read_bytes())==rc.MAIN_SHA
os.environ.pop('DEEPSEEK_API_KEY',None)
socket.create_connection=rc.deny;socket.socket.connect=rc.deny;socket.socket.connect_ex=rc.deny
remaining=int(rc.read(rc.RUN/'AUTHORIZATION.json')['deadline_epoch']-time.time())
assert remaining>0
signal.alarm(min(400,remaining))
sys.path[:0]=[str(base/'src'),str(base/'runtime')]
from pr_next_joint.investigation import properties,property_model
from pr_next_joint.investigation.protocol import Session
switches=[]
old_request=Session.request
def until_received(self,**kw):
    value=old_request(self,**kw)
    if len(self.attempts)==2:
        assert not switches and self.attempts[1]['status']=='analysis_received'
        assert self.attempts[1]['actual_model_submissions']==0 and not self.client.live_authorized
        # Keep the original graph, model questions, and all solver/evidence IDs.
        # Replace only the subsequent consumers, including imported function aliases.
        for module,name in ((properties,'stage'),(property_model,'compose')):
            rel=Path(module.__file__).relative_to(base)
            production=fix/rel
            tree=ast.parse(production.read_bytes())
            nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name]
            assert len(nodes)==1
            isolated=ast.Module(body=nodes,type_ignores=[])
            got={}
            exec(compile(isolated,str(production),'exec'),vars(module),got)
            original=getattr(module,name);replacement=got[name]
            assert original.__code__.co_freevars==replacement.__code__.co_freevars==()
            original.__code__=replacement.__code__
            switches.append({'function':module.__name__+'.'+name,'verified_source':str(production.relative_to(rc.RUN)),
                'file_sha256':rc.sha(production.read_bytes()),'after_exact_response_index':1})
    return value
Session.request=until_received
rc.HOME=dst
rc.freeze=rc.read(rc.RUN/'PREDICTIONS_FROZEN.json')
rc.conn=sqlite3.connect('file:'+str(rc.RUN/'requests.sqlite')+'?mode=ro&immutable=1',uri=True)
beg=time.time()
try:
    row=rc.rerun(m,base,pin['parent'])
    assert len(switches)==2
    checks=rc.read(dst/'audit'/f'{m}.json')
    assert len(checks['matches'])==2
    assert all(q['original_host_identity']==q['successor_host_identity'] for q in checks['matches'])
    rc.save(dst/'PROVENANCE.json',{'result':row,'parent_and_successor':{k:pin[k] for k in ('parent','successor')},
        'execution':'Recorded-response continuation. Original compiled input and original producer/code namespace through both complete, hash-matched HTTP requests. Only the subsequent consumers use the two corrective functions. The ordinary raw report and its manifest describe the original fact namespace; use the separate published provenance manifest for this mixed execution.',
        'switches':switches,'wall_seconds':time.time()-beg,'new_requests':0,'old_requests_used':2})
    published=dst/'published'
    raw=rc.RUN/row['report']
    report=rc.read(raw)
    report['technical_recovery_provenance']={'kind':'post_feedback_consumer_continuation','prefix_sha256':pin['parent'],
        'consumer_source_sha256':pin['successor'],'raw_report_sha256':row['report_sha256'],
        'new_live_calls':0,'historical_live_responses_used':2,'original_evidence_ids_preserved':True}
    rc.save(published/'report.json',report)
    row.update(report=str((published/'report.json').relative_to(rc.RUN)),report_sha256=rc.sha((published/'report.json').read_bytes()),
        source_mode='original_prefix_through_feedback_then_repaired_consumers',program_namespace_sha256=pin['parent'],consumer_source_sha256=pin['successor'])
    rc.save(published/'prediction_manifest.json',{'provenance':report['technical_recovery_provenance'],'report_sha256':row['report_sha256'],
        'projection_sha256':rc.sha((raw.parents[1]/'prediction_export.json').read_bytes()),'Gold_read':False,'new_model_calls':0})
    prior=rc.read(here/'SUMMARY.json')
    first=prior['results'][0]
    assert first['valid_supplement'] and first['member']==rc.TARGETS[0]
    selected=rc.read(here/'SELECTION_200.json')
    selected[m]={'population':'recovered_post_feedback_from_original_state','report':row['report'],'report_sha256':row['report_sha256'],
        'prediction_export':str((raw.parents[1]/'prediction_export.json').relative_to(rc.RUN))}
    assert len(selected)==200
    for member,source in selected.items():
        if source['population']=='frozen_main':
            assert source['report_saved'] and source['report_sha256']
            p=rc.RUN/'members'/member/'attempt_1'/'analysis/report.json'
            assert rc.sha(rc.frozen(p))==source['report_sha256']
        else:assert rc.sha((rc.RUN/source['report']).read_bytes())==source['report_sha256']
    assert rc.sha((rc.RUN/'PREDICTIONS_FROZEN.json').read_bytes())==rc.MAIN_SHA
    assert rc.conn.execute('select count(*) from requests').fetchone()[0]==356
    rc.save(dst/'FINAL_SELECTION_200.json',selected)
    final={'main_reports':198,'zero_call_supplementary_reports':2,'main_technical_errors_preserved':2,'aggregate_saved_reports':200,
        'original_request_count':356,'additional_submissions':0,'unknown_main_service_receipts':0,'new_model_cost_usd':0,
        'main_freeze_sha256':rc.MAIN_SHA,'first_attempt_supplemental_freeze_sha256':rc.sha((here/'SUPPLEMENT_FROZEN.json').read_bytes()),
        'selection_sha256':rc.sha((dst/'FINAL_SELECTION_200.json').read_bytes()),'parent':pin['parent'],'corrective_source':pin['successor'],
        'includes_mixed_technical_recovery_not_new_200_live_run':True,'scoring_performed':False,'cases':[]}
    for x in (first,row):
        final['cases'].append({'member':x['member'],'findings':x['findings'],'AC_projection':x['projection']['predictions'].get('AC'),
            'unresolved_categories':x['unresolved_categories'],'gaps':x['gaps'],'report_sha256':x['report_sha256']})
    rc.save(dst/'FINAL_REVIEW.json',final)
    files={p.relative_to(dst).as_posix():rc.sha(p.read_bytes()) for p in dst.rglob('*') if p.is_file()}
    rc.save(dst/'SUPPLEMENT_FROZEN.json',{'files':files,'parent_freeze':rc.MAIN_SHA,'replay_controller_sha256':rc.sha(Path(__file__).read_bytes()),
        'scoring_performed':False})
    print(json.dumps(final,ensure_ascii=False),flush=True)
except BaseException as exc:
    import traceback
    rc.save(dst/'CONTINUATION_ERROR.json',{'error':repr(exc),'traceback':traceback.format_exc(),'post_feedback_switches':switches})
    raise
finally:rc.conn.close()

````

## run/technical_recovery_2_r1/recover.py

原文件 SHA-256 `02a8c74906050f4a790f324ef303cb3879008ca8a48871ec43d8002de6be2e82`

````python
"""One offline compatibility rerun for the two crashed post-response consumers."""
import difflib
import hashlib
import json
import os
import shutil
import signal
import socket
import sqlite3
import sys
import time
import traceback
from pathlib import Path
from types import SimpleNamespace

ROOT = Path('/root/autodl-tmp/pr-next-joint-task-c/runs/next_revision_full200_r1')
RUN = ROOT/'run'
HOME = RUN/'technical_recovery_2_r1'
TARGETS = ('RQ1_c20b10d094d5','RQ1_e6f04047bff4')
MAIN_SHA = '72fd2d74cf736e1f388bad85d7f51d4d319fb89533bbed598b469032e58e8e22'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def digest(obj):
    return sha(json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())

def read(path):
    return json.loads(path.read_bytes())

def save(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def deny(*args,**kwargs):
    raise RuntimeError('network unavailable for offline reuse')

def frozen(path):
    data=path.read_bytes()
    assert sha(data)==freeze['files'][path.relative_to(RUN).as_posix()],path
    return data

def module_hashes(src):
    root=src/'src/pr_next_joint'
    return {p.relative_to(root).as_posix():sha(p.read_bytes()) for p in sorted(root.rglob('*.py'))}

def apply_fix(path,replacements):
    before=path.read_bytes()
    data=before
    for a,b,count in replacements:
        assert data.count(a)==count,path
        data=data.replace(a,b)
    compile(data,str(path),'exec')
    path.write_bytes(data)
    return list(difflib.unified_diff(before.decode().splitlines(True),data.decode().splitlines(True),
                fromfile='parent/'+path.name,tofile='successor/'+path.name))

def prepare():
    for rec in read(ROOT/'MANIFEST.json')['files']:
        path=ROOT/rec['path'];assert sha(path.read_bytes())==rec['sha256'],path
    original=module_hashes(ROOT/'source')
    assert digest(original)==read(ROOT/'IDENTITY.json')['method_sha256']
    assert sha((RUN/'PREDICTIONS_FROZEN.json').read_bytes())==MAIN_SHA
    assert {entry['member'] for entry in read(RUN/'RESULTS.json') if not entry.get('report_saved')}==set(TARGETS)
    src=HOME/'source'
    shutil.copytree(ROOT/'source',src)
    modules=src/'src/pr_next_joint/investigation'
    patch=apply_fix(modules/'properties.py',[
        (b"not value_type(cell,facts.lookup(use)).startswith(('uint','bool'))",
         b"not (value_type(cell,facts.lookup(use)) or '').startswith(('uint','bool'))",1)])
    line=b"    if (item.get('observation') or {}).get('measure') != 'denied_qualified':"
    file=modules/'property_model.py'
    contents=file.read_bytes()
    nl=contents.split(line,1)[1].split(b'        reason',1)[0]
    assert nl.strip()==b'' and b'\n' in nl
    patch+=apply_fix(file,[
        (line,nl.join((b"    observation = item.get('observation')",
         b"    measure = observation.get('measure') if isinstance(observation, dict) else None",
         b"    if measure != 'denied_qualified':")),1),
        (b"if (item.get('observation') or {}).get('measure') == 'denied_qualified' else",
         b"if measure == 'denied_qualified' else",1)])
    (HOME/'changes.patch').write_bytes(''.join(patch).encode())
    new=module_hashes(src)
    changed=[p for p in new if original[p]!=new[p]]
    assert set(changed)=={'investigation/properties.py','investigation/property_model.py'}
    save(HOME/'IDENTITY.json',{'main_freeze':MAIN_SHA,'parent':digest(original),'successor':digest(new),
        'changed':changed,'method_files':new,'config':sha((ROOT/'METHOD_CONFIG.json').read_bytes()),
        'scope':'Two type guards only; non-scalar stage candidates and absent structured observation measures get the pre-existing unsupported/unspecified treatment. Original text, source conditions and other checks are retained.'})
    return src,digest(new)

def rerun(member,src,method):
    from pr_next_joint.investigation.cli import run
    assert Path(run.__code__.co_filename).resolve().is_relative_to(src)
    old=RUN/'members'/member/'attempt_1'
    job=read(RUN/'JOBS.json')[member]
    old_intake=json.loads(frozen(old/'intake_receipt.json'))
    output=HOME/'cases'/member
    matches=[]
    class ArchivedClient:
        live_authorized=False
        case_id=member
        def __init__(self,program):
            self.program_identity=program.identity
        def accounting(self):
            return {'real_model_calls':0,'reused_historical_real_responses':len(matches),
                    'nature':'offline_reprocessing_of_authenticated_original_HTTP_responses','new_model_cost_usd':0}
        def call(self,messages,tag,**parameters):
            idx=len(matches)
            assert idx<2 and tag==('semantic_initial' if idx==0 else 'semantic_feedback')
            assert parameters=={'max_tokens':32768,'thinking':True,'reasoning_effort':'high','timeout':1800}
            origin=RUN/'requests'/member/str(idx)
            intent=json.loads(frozen(origin/'intent.json'));receipt=json.loads(frozen(origin/'receipt.json'))
            body=frozen(origin/'raw_http.body');raw=json.loads(body)
            saved=json.loads(frozen(old/'analysis/model'/('request_'+str(idx)+'.json')))
            assert raw==json.loads(frozen(origin/'raw_http.json'))
            assert receipt['raw_http_sha256']==sha(body) and not receipt['simulated'] and receipt['actual_model_submissions']==1
            assert receipt['case_id']==member and receipt['call_index']==idx
            assert saved['host_identity']==intent['host_program_identity']==receipt['program_identity']
            assert intent['body']['messages']==saved['messages'] and digest(intent['body'])==receipt['request_sha256']==intent['body_sha256']
            assert conn.execute('select body_sha,state from requests where member=? and idx=?',(member,idx)).fetchone()==(intent['body_sha256'],'settled')
            assert raw['model']==receipt['model']
            raw_text=raw['choices'][0]['message']['content']
            assert digest(raw_text)==receipt['response_sha256']
            if messages!=saved['messages'] or digest(messages)!=receipt['messages_sha256']:
                raise ValueError(f'original messages differ at {idx}; archived answer not applied')
            matches.append({'index':idx,'origin':str(origin.relative_to(RUN)),'wire_message_sha256':digest(messages),
                'http_request_sha256':intent['body_sha256'],'raw_http_sha256':sha(body),'response_text_sha256':digest(raw_text),
                'original_host_identity':receipt['program_identity'],'successor_host_identity':self.program_identity})
            return raw_text,{'case_id':member,'program_identity':self.program_identity,'call_index':idx,
                'messages_sha256':digest(messages),'response_sha256':digest(raw_text),'model':receipt['model'],'simulated':True,
                'source':'archived_real_HTTP_response_exact_message_match_offline','actual_model_submissions':0,
                'original_receipt_sha256':sha(frozen(origin/'receipt.json')),'original_usage':receipt['usage']}
    def factory(program,args,counter):
        intake=read(output/'intake_receipt.json')
        for k,v in job['expected'].items():
            assert old_intake[k]==v==intake[k],(member,k)
        assert program.context['implementation_sha256']==method
        return ArchivedClient(program)
    settings=SimpleNamespace(root=job['root'],compiled_unit=job['descriptor'],engineering_compiled=None,target=None,
        task=job['task'],out=str(output),config=str(ROOT/'METHOD_CONFIG.json'),tokenizer=str(ROOT/'tokenizer'),
        phase='analyze',fixture_response=None,fixture_feedback=None,offline_bridge=False,case_id=member)
    begin=time.monotonic()
    try:
        rep=run(settings,client_factory=factory)
        assert len(matches)==2 and len(rep['usage']['attempts'])==2,rep['usage']['attempts']
        for i,v in enumerate(rep['usage']['attempts']):
            prior=json.loads(frozen(old/'analysis/model'/f'attempt_{i}.json'))
            assert v['status']==prior['status'] and v['status'] in ('analysis_received','protocol_diagnostic') and v['actual_model_submissions']==0
            assert read(output/'analysis/model'/f'normalized_{i}.json')==json.loads(frozen(old/'analysis/model'/f'normalized_{i}.json'))
        rp=output/'analysis/report.json'; manifest=read(output/'analysis/prediction_manifest.json')
        assert manifest['implementation_sha256']==method and manifest['report_sha256']==sha(rp.read_bytes())
        assert manifest['prediction_frozen_before_gold'] and not manifest['Gold_read'] and manifest['real_model_calls']==0
        return {'member':member,'valid_supplement':True,'report':str(rp.relative_to(RUN)),
            'report_sha256':manifest['report_sha256'],'projection':read(output/'prediction_export.json'),
            'findings':len(rep['findings']),'model_analysis_available':rep['model_analysis_available'],
            'unresolved_categories':rep['unresolved_category_judgments'],
            'gaps':{k:len(rep['diagnostics'][k]) for k in ('program_gaps','unexecuted_actions','issues')}}
    finally:
        save(HOME/'audit'/f'{member}.json',{'member':member,'matches':matches,'new_model_calls':0,
            'wall_seconds':time.monotonic()-begin,'references_original_intake_and_original_freeze':True})

if __name__=='__main__':
    os.environ.pop('DEEPSEEK_API_KEY',None)
    socket.create_connection=deny;socket.socket.connect=deny;socket.socket.connect_ex=deny
    deadline=read(RUN/'AUTHORIZATION.json')['deadline_epoch']
    remaining=int(deadline-time.time())
    if remaining<=0:raise SystemExit('original time window expired')
    signal.alarm(min(600,remaining))
    begin=time.time()
    freeze=read(RUN/'PREDICTIONS_FROZEN.json')
    assert not (HOME/'IDENTITY.json').exists()
    conn=sqlite3.connect('file:'+str(RUN/'requests.sqlite')+'?mode=ro&immutable=1',uri=True)
    count=conn.execute('select count(*) from requests').fetchone()[0]
    src,method=prepare();sys.path[:0]=[str(src/'src'),str(src/'runtime')]
    results=[]
    for m in TARGETS:
        try:results.append(rerun(m,src,method))
        except Exception as exc:
            results.append({'member':m,'valid_supplement':False,'error':repr(exc)})
            save(HOME/'audit'/f'{m}-error.json',{'exception':repr(exc),'traceback':traceback.format_exc()})
    assert count==conn.execute('select count(*) from requests').fetchone()[0]==356
    conn.close()
    assert sha((RUN/'PREDICTIONS_FROZEN.json').read_bytes())==MAIN_SHA
    selection={x['member']:{'population':'frozen_main','report_sha256':x.get('report_sha256'),'report_saved':x.get('report_saved',False)} for x in read(RUN/'RESULTS.json')}
    for row in results:
        if row['valid_supplement']:
            selection[row['member']]={'population':'offline_same_answer_compatibility_supplement','report':row['report'],'report_sha256':row['report_sha256']}
    save(HOME/'SELECTION_200.json',selection)
    save(HOME/'SUMMARY.json',{'parent_freeze':MAIN_SHA,'method':method,'original_reports':198,
        'original_paid_requests':count,'new_paid_requests':0,'new_model_cost_usd':0,'start_epoch':begin,
        'elapsed_seconds':time.time()-begin,'results':results,'Gold_read':False,'scoring_performed':False})
    files={p.relative_to(HOME).as_posix():sha(p.read_bytes()) for p in sorted(HOME.rglob('*')) if p.is_file() and p.name!='SUPPLEMENT_FROZEN.json'}
    save(HOME/'SUPPLEMENT_FROZEN.json',{'files':files,'main_freeze_sha256':MAIN_SHA,'members':TARGETS,'scoring_performed':False})
    print(json.dumps(read(HOME/'SUMMARY.json'),ensure_ascii=False),flush=True)
    sys.exit(0 if all(x['valid_supplement'] for x in results) else 2)

````

## run/technical_recovery_2_r1/source/src/pr_next_joint/investigation/properties.py

原文件 SHA-256 `cdfff0890436cc5b493a8e3b23f72fe1447b6e416f33d9b711dec2c2a08dc0dd`

````python
"""Finite, source-bound questions. Wording guides investigation, never certifies harm."""
import re
from itertools import product

from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, selector_relation, value_type
from .request_scope import claim_entries, holder_effect, linked_controls, unique_cells
from .ledger import MEASURES, bind_positions, movements
from .roles import path_qualification


def words(item):
    return ' '.join(str(item.get(k) or '') for k in ('claim','distinguish','distinguishing_question','observation'))


def interpret(item):
    raw = item.get('observation')
    req = dict(raw) if isinstance(raw,dict) else {}
    text = words(item)
    if re.search(r'\b(?:never check|does not (?:read|check)|bypass(?:es)?|missing (?:the )?control)\b',text,re.I) and re.search(r'freez|frozen|guard|control',text,re.I):
        return {**req,'measure':'missing_control'}
    if req.get('measure') in MEASURES or req.get('measure') in ('denied_qualified','direct_effect','authorization_violation'):
        return req
    if req.get('measure') and req['measure'] not in ('opens','blocks'):
        return req
    if re.search(r'allowance.{0,55}(?:gross|actual debit|less than)|more than (?:the |was )?(?:allowance|approved)|(?:gross|actual) debit.{0,70}(?:allowance|grant)',text,re.I):
        return {**req,'measure':'ledger_grant'}
    if re.search(r'(?:recipient|payee|receiver).{0,55}(?:less|zero|smaller|short)|(?:lower|reduced) (?:recipient )?credit|到账减少',text,re.I):
        return {**req,'measure':'ledger_receipt'}
    if re.search(r'(?:debited|debit|charged).{0,22}(?:more|greater|extra)|greater gross debit',text,re.I):
        return {**req,'measure':'ledger_debit'}
    if req.get('measure'):
        return req
    if item.get('category')=='AC' and re.search(r'(?:qualified|entitled|authorized|rightful|rightfully).{0,65}(?:reject|denied|refus)|wrongful.{0,18}(?:denial|reject)',text,re.I):
        return {**req,'measure':'denied_qualified'}
    if item.get('category') in ('FCR-MINT','FCR-TRANSFER','FCR-DESTROY') and re.search(r'\b(mint|issuance|confiscate|seize|destroy|burn|debit|transfer|issu(?:e|es))\b',text,re.I):
        return {**req,'measure':'direct_effect'}
    if item.get('category') in ('FCR-FREEZE','FCR-PAUSE') and re.search(r'block|revert|pause|freeze',text,re.I):
        return {**req,'measure':'blocks'}
    if item.get('category')=='AC' and re.search(r'(?:install|forge|acquire|grant itself).{0,36}(?:grant|allowance|permission)',text,re.I):
        return {**req,'measure':'holder_grant'}
    return None


def conflicting_measurements(inv,q,proposal):
    """Only explicit factual negations of the same measured positive condition conflict."""
    from .request_scope import observation_applies
    factual={
        'ledger_receipt':r'\b(?:recipient|payee)\b.{0,28}\b(?:always|necessarily)\b.{0,20}\b(?:full|unchanged)',
        'ledger_debit':r'\b(?:gross|actual) debit (?:never increases|is always unchanged)',
        'ledger_grant':r'\b(?:actual|gross) debit (?:never exceeds|is always within) (?:the )?(?:allowance|grant)',
        'denied_qualified':r'\b(?:qualified|authorized) (?:caller|role|manager) (?:is never (?:rejected|denied)|always succeeds)',
    }
    if any(proposal.get(k)!=q['current'].get(k) for k in ('observation','assumptions','next_check','actor','object','phase')):
        return []
    text=proposal.get('claim','')
    return [o['probe'] for row in q.get('observations',[]) if row['measure'] in factual and row['version']==q['version']
            and observation_applies(inv,q,row) and re.search(factual[row['measure']],text,re.I)
            for o in row['outcomes'] if o['predicate_value']]


def source_target(inv,anchor,target):
    return [o for o in inv.catalog.resolve(anchor) if inv.f.operations[o]['target']==target]


def premise_cases(inv, use, item, changed=()):
    """Separate expressly different values of the same declared cell. No free Boolean substitute."""
    lookup = inv.f.lookup(use)
    cells = unique_cells(s for s in inv.graph.request_reads(use) if not keys(s))
    text = words(item)
    axes, gaps = [], []
    for cell in cells:
        name = lookup.nodes.get(cell['root'],{}).get('name')
        if not name:
            continue
        regex=r'(?<![\w$])'+re.escape(name)+r'\s*(?:==|=)\s*(true|false|\d+)\b'
        values=list(dict.fromkeys(v.lower() for v in re.findall(regex,text,re.I)))
        if not values:
            continue
        if len({s['root'] for s in cells if lookup.nodes.get(s['root'],{}).get('name')==name})!=1:
            gaps.append('ambiguous source declaration '+name);continue
        typ=value_type(cell,lookup)
        if any((v in ('true','false')) != (typ=='bool') or typ!='bool' and not typ.startswith('uint') for v in values):
            gaps.append('literal sort unsupported: '+name);continue
        at='after' if any(selector_relation(cell,c)=='same_shape' for c in changed) else 'before'
        axes.append([{'cell':cell,'source_name':name,'value':v=='true' if typ=='bool' else int(v),'frame':at} for v in values])
    fixed=[]
    assumptions=item.get('assumptions',[])
    if isinstance(assumptions,str):assumptions=[assumptions]
    named=unique_cells(inv.graph.request_reads(use))
    for a in assumptions:
        match=re.fullmatch(r'(before|after)\s+([A-Za-z_$][\w$]*(?:\[[\w$.]+\])*)\s*(?:==|=)\s*(\d+|true|false)',str(a).strip(),re.I)
        if not match:continue
        at,name,value=match.groups(); found=[s for s in named if inv.backend._storage_name(use,s)==name]
        if len(found)!=1:gaps.append('unbound scoped premise '+name);continue
        fixed.append({'cell':found[0],'source_name':name,'frame':at.lower(),'value':value.lower()=='true' if value.lower() in ('true','false') else int(value)})
    if len(axes)>3 or len(axes)>1 and any(len(axis)>1 for axis in axes):
        return [],gaps+['multiple alternative clauses cannot be independently cross-multiplied']
    return [fixed+list(c) for c in product(*axes)] if axes else [fixed],gaps


def privileged_paths(inv,oid):
    return [pid for pid,p in inv.backend.paths(oid) if path_qualification(inv.f,oid,p)]


def stage(inv,use):
    facts=inv.f; target=facts.operations[use]['target']
    listed=[]
    for cell in unique_cells(inv.graph.request_reads(use)):
        if keys(cell) or not (value_type(cell,facts.lookup(use)) or '').startswith(('uint','bool')):
            continue
        writers=[]
        for oid in sorted(inv.graph.access[target,cell['root']]['writers']):
            matches=[pid for pid,p in inv.backend.paths(oid) if any(selector_relation(cell,w['path'])=='same_shape' for w in p['writes'])]
            if matches:
                writers.append({'operation':oid,'paths':matches,'role_guarded_paths':privileged_paths(inv,oid)})
        listed.append({'cell':cell,'name':inv.backend._storage_name(use,cell),'runtime_writers':writers})
    return listed


def source_graph_holes(inv,binding,item):
    root=binding['core_operation']; target=inv.f.operations[root]['target']
    claimed=claim_entries(inv,binding,item)
    controls=unique_cells(w['path'] for _,p in inv.backend.paths(root) for w in p['writes'] if value_type(w['path'],inv.f.lookup(root))=='bool')
    if not controls:
        return []
    related=[]
    for oid in sorted(claimed-{root}):
        ops=[(pid,movements(inv.backend,oid,p)) for pid,p in inv.backend.paths(oid)]
        debit=unique_cells(c for pid,m in ops for c in m['-'])
        if not debit:
            continue
        peers=[]
        for other,entry in inv.f.operations.items():
            if entry['target']!=target or other==oid:continue
            linked=linked_controls(inv,root,other)
            if not any(selector_relation(c,l)=='same_shape' for c in controls for l in linked):continue
            for pid,p in inv.backend.paths(other):
                m=movements(inv.backend,other,p)
                if any(selector_relation(a,b)=='same_shape' for a in debit for b in m['-']):
                    peers.append({'operation':other,'path':pid,'controls':linked})
        reads=linked_controls(inv,root,oid)
        related.append({'use':oid,'debit_positions':debit,'control_reads':reads,'control_writers':controls,'peer_controlled_uses':peers})
    return related


def plan_property(inv,binding,item,plan,req):
    """Select finite typed questions with compiler-resolved endpoints, or disclose a local gap."""
    measure=req['measure']; root=binding['core_operation']; target=inv.f.operations[root]['target']
    entries=claim_entries(inv,binding,item); contexts=[]
    if measure in MEASURES:
        uses=[oid for oid in sorted(entries) if holder_effect(inv,oid)]
        if req.get('at'):uses=[o for o in source_target(inv,req['at'],target) if o in entries]
        elif root in uses and bind_positions(inv.backend,root,item)[0]:uses=[root]
        reasons=[]
        for use in uses:
            pos,err=bind_positions(inv.backend,use,item)
            if err:reasons.append(err);continue
            edges=stage(inv,use)
            forced=source_target(inv,req.get('after'),target) if req.get('after') else []
            if req.get('after') and len(forced)!=1:reasons.append('requested_intervention_not_unique');continue
            choices={}
            for edge in edges:
                if req.get('control') and req['control']!=edge['name']:continue
                for w in edge['runtime_writers']:
                    change=w['operation']
                    if forced and change not in forced or not forced and root!=use and change!=root:continue
                    if not w['role_guarded_paths']:continue
                    choices.setdefault(change,[]).append(edge['cell'])
            if not choices:reasons.append('no_source_bound_runtime_privileged_writer');continue
            for change,controls in choices.items():
                ctx=inv._compare_context({'current':item},change,use)
                ctx['observable']={'measure':measure,'ledger':pos,'control_selectors':controls,
                                   'change_paths':privileged_paths(inv,change)}
                cases,gaps=premise_cases(inv,use,item,controls)
                if gaps:reasons+=gaps;continue
                ctx['premise_cases']=cases
                # An address alias is admitted only for two actual source parameter names.
                params=inv.f.lookup(use).function(inv.f.operations[use]['function']).get('parameters',{}).get('parameters',[])
                addr={p['name']:{'kind':'parameter','id':p['id'],'type':p['typeDescriptions']['typeString']} for p in params if p['typeDescriptions']['typeString'] in ('address','address payable')}
                ctx['request_aliases']=[]
                for a,op,b in re.findall(r'\b(\w+)\s*(==|!=)\s*(\w+)\b',str(item.get('assumptions',[]))):
                    if a in addr and b in addr:ctx['request_aliases'].append([addr[a],addr[b],op])
                contexts.append((change,use,ctx))
        reason=','.join(dict.fromkeys(reasons)) or 'more_than_one_applicable_request_or_intervention'
    elif measure=='missing_control':
        rows=source_graph_holes(inv,binding,item)
        relevant=[r for r in rows if r['peer_controlled_uses'] and not r['control_reads']]
        if relevant:
            contexts=[(root,relevant[0]['use'],{'observable':{'measure':measure,'alternatives':relevant},'operation':root,
                      'checked_uses':[r['use'] for r in relevant],'frame_type':'committed_intervention_then_actual_alternative'})]
        reason='no_same_target_same_right_comparator_or_unresolved_control'
    else:
        ctx=inv._compare_context({'current':item},root,root)
        ctx.update({'observable':{'measure':measure,'claim':item.get('claim',''),'category':item.get('category')},
                    'operation':root,'stage':stage(inv,root),'frame_type':'single_original_entry'})
        if req.get('authorization'):ctx['observable']['authorization']=req['authorization']
        if measure=='direct_effect' and ctx.get('bindings'):
            ctx['exploratory_request_bindings_not_the_claim']=ctx.pop('bindings')
        params=inv.f.lookup(root).function(inv.f.operations[root]['function']).get('parameters',{}).get('parameters',[])
        addr={p['name']:{'kind':'parameter','id':p['id'],'type':p['typeDescriptions']['typeString']} for p in params if p['typeDescriptions']['typeString'] in ('address','address payable')}
        ctx['request_aliases']=[[addr[a],addr[b],op] for a,op,b in re.findall(r'\b(\w+)\s*(==|!=)\s*(\w+)\b',str(item.get('assumptions',[]))) if a in addr and b in addr]
        contexts=[(root,root,ctx)]
        if measure=='direct_effect':
            contexts[0][2]['privileged_paths']=privileged_paths(inv,root)
        reason='unresolved_direct_property'
    pick=None
    if len(contexts)==1:
        change,use,ctx=contexts[0]
        pick={'action':'compare','change':change,'observe':use,'measure':measure,'status':'source_bound',
              'expectations':{},'context':ctx,'scope':{'target':target,'finding_root':root,'use':use,'intervention':change,
                  'measure':measure,'controls':ctx['observable'].get('control_selectors',[]),'objects':[ctx['observable']['ledger'][k] for k in ('debit','credit')] if 'ledger' in ctx['observable'] else [],
                  'checked_uses':ctx.get('checked_uses',[use]),'frame_type':ctx.get('frame_type','same_request_two_worlds'),
                  'extent':'compiler-selected entries, ordered keys and recorded path conditions only'}}
    inherited_pairs=list(plan.get('selected_pairs',[]))
    plan['observation_choice']={'ordinary_pairs':inherited_pairs,'selected':pick,'pool':[pick] if pick else [],'status':'selected_property' if pick else 'unsupported',
        'reason':'source-resolved finite property' if pick else reason,'property_requested':measure,'claim_text':item['claim'],'possible_compilations':len(contexts),
        'stage_evidence':stage(inv,root),'request_resolution':{'finding_root':root,'use':pick['observe'] if pick else None,
        'possible_uses':sorted(entries),'unmeasured_uses':sorted(entries-{pick['observe'],pick['change']}) if pick else sorted(entries)}}
    if pick:
        plan['selected_pairs']=[{'change':pick['change'],'observe':pick['observe'],'source_reason':'typed property and matching applied target'}]
    inv.graph.events.append({'action':'compile_source_property','measure':measure,'root':root,'selected':bool(pick),'reason':plan['observation_choice']['reason']})


````

## run/technical_recovery_2_r1/source/src/pr_next_joint/investigation/property_model.py

原文件 SHA-256 `15fe7dd91dab3663d73abe87f635252b4ba72fd757adf39ea78b3c0ccc396a38`

````python
"""Host-compiled properties and evidence composition, shared by Full consumers.

Model judgments are proposals. Program execution does not prove a business
policy; source-backed policy/resource interpretations remain explicit H inputs.
"""
import copy
import re
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key, walk, op
from pr_next_joint.frontend.storage import selectors, keys, selector_relation, value_type
from .summary import get_summaries, holder, unique
from .initial_state import domain, initial_for_lookup
from .roles import path_qualification


def policy_basis(item):
    from .relations import policy
    return policy(item)


def authorization_expression(inv,q,policy):
    from .relations import authorization
    return authorization(inv,q,policy)


def compile_property(inv, q):
    f = inv.f; b = inv.backend; root = inv.root(q); item = q['current']
    if root is None: return None
    from .ledger import movements, unit_origin, native_only_position
    from .key_roles import relation as key_relation
    from .comparison import transfer_shapes
    summaries = get_summaries(f); rows = summaries.rows(root)
    target = f.operations[root]['target']
    cells = unique(c for oid in [root] for c in summaries.positions(oid)
                   if not summaries.control_only(c,target))
    bindings = [unit_origin(b, root, c) for c in cells]
    questions = []
    for c, unit in zip(cells, bindings):
        bound = inv.semantics.lookup(root, c)
        if not unit and not (bound and bound['meaning'] == 'nonfinancial_counter'):
            questions.append(inv.semantics.question(q, root, c))
    known_semantics = [u for u in bindings if u]
    possible = set(); text = item.get('claim', '')
    declared = set(q['claim_source_scope']['source_operations']) | {root}
    # An anchored control can have a real downstream financial use without a
    # second model anchor. This is a source dependency candidate, not a claim
    # expansion based on the exploratory next_check endpoint.
    control_uses=set()
    if f.options.scope=='FCR':
        written=[w['path'] for r in rows for w in r['ordered_writes']]
        for cell in written:
            if unit_origin(b,root,cell):continue
            if (key_relation(cell,f.lookup(root)) or {}).get('kind')=='authorization_quantity':continue
            for use in inv.graph.access[(target,cell['root'])]['readers']:
                if use==root:continue
                if any(selector_relation(cell,c)=='same_shape' and not inv.graph._disjoint_keys(cell,c)
                       for r in summaries.rows(use) for c in selectors(r['guards'])):
                    control_uses.add(use)
    test_uses=set()
    if f.options.scope=='FCR' and item.get('category') in ('FCR-FREEZE','FCR-PAUSE'):
        # A proposed control must be falsifiable even when the graph finds no
        # effect edge. Select an actual ordinary token-flow use, not a clock
        # setter interpreted as issuance, and never infer a different category
        # merely from an administrative number increasing or decreasing.
        candidates={}
        for use,entry in f.operations.items():
            if entry['target']!=target or use==root:continue
            for rr in summaries.rows(use):
                pp=f.paths[rr['path']]['raw']
                if path_qualification(f,use,pp):continue
                mm=movements(b,use,pp)
                for debit,credit in transfer_shapes(b,use,pp):
                    if unit_origin(b,use,debit) and not native_only_position(b,use,debit):
                        candidates.setdefault(key({'root':debit['root'],'fields':[s for s in debit.get('segments',[])if 'field'in s]}),set()).add(use)
        named={use for uses in candidates.values() for use in uses if use in declared}
        if named:test_uses=named
        elif len(candidates)==1:test_uses=next(iter(candidates.values()))
    property_entries=declared|control_uses|test_uses
    # Supplemental anchors are context, not a request to change the root's object.
    cells = unique(cells + [c for use in control_uses|test_uses for c in summaries.positions(use)])
    bindings = [unit_origin(b, root, c) for c in cells]
    known_semantics = [u for u in bindings if u]
    native_debits=unique(e['cell'] for r in rows for e in r['numeric_effects']
        if e['holder'] is not None and 'debit' in e['may_directions'] and b._native_unit_source(root,e['cell']))
    if f.options.scope == 'AC':
        cat = 'AC'; policy = q.get('authorization_interpretation') or policy_basis(item)
        prior_policy=next((policy_basis(v) for v in reversed(q.get('history',[])) if policy_basis(v)),None)
        if policy and policy.get('meaning')=='normal_authorization' and prior_policy:
            # A normal proposal does not erase the qualification being tested.
            # It may add a source-bound business alternative to that predicate.
            policy=dict(prior_policy,normal_proposal=copy.deepcopy(policy))
        if policy is None:
            policy=prior_policy
        if policy is None:
            questions.append(inv.semantics.question(q, root, kind='authorization'))
        else:
            predicate=authorization_expression(inv,q,policy)
            if predicate:
                interpretations = [predicate]
                for alternative in q.get('authorization_alternatives', []):
                    other = authorization_expression(inv, q, alternative)
                    if other and all(key(other['predicate']) != key(x['predicate']) for x in interpretations):
                        interpretations.append(other)
                if len(interpretations) > 1:
                    # A witness must violate every still-supported policy.
                    # UNSAT for their conjunction does not refute each policy.
                    predicate = dict(predicate,
                        predicate=op('or', *[x['predicate'] for x in interpretations]),
                        competing_interpretations=interpretations,
                        competition_semantics='one behavior violates all surviving interpretations')
                policy=dict(policy,compiled_authorization=predicate)
            if predicate and not predicate.get('source_bound_alternatives'):
                from .authorization_normal import payment_qualification
                potential=payment_qualification(inv,q,predicate['subject'],require_proposal=False) if predicate.get('subject') is not None else []
                if potential:
                    question=inv.semantics.question(q,root,kind='authorization')
                    question.update(question='Does the recorded actual payment establish a lawful business qualification for acquiring this authority? Explain the source relation and any bypass.',
                        source_qualification_candidates=[{'authority':b._storage_name(root,x['holder']),
                            'recorded_payment':b._storage_name(root,x['bid']),
                            'relation':'actual payment exceeds the previous recorded payment; the same payer receives this authority',
                            'source_path':x['path'],'business_legitimacy_not_proved':True} for x in potential])
                    questions.append(question)
        possible.add(cat)
    else:
        policy = None
        for r in rows:
            # This selects a typed hypothesis from known source writes, not
            # a successful execution. A residual read must reach the actual
            # condition checker instead of erasing the hypothesis/category.
            p = f.paths[r['path']]['raw']; m = movements(b, root, p)
            # A stage counter beside a known native entitlement is not a token
            # ledger merely because both numeric fields change on this path.
            # Unknown units still receive the semantic questions above.
            m={sign:[c for c in values if unit_origin(b,root,c)] for sign,values in m.items()}
            transfers = transfer_shapes(b, root, p)
            if any(unit_origin(b,root,a) and not native_only_position(b,root,a) for a,_ in transfers): possible.add('FCR-TRANSFER')
            if any(not any(selector_relation(d, c) == 'same_shape' and key(d) != key(c)
                           for c in m['+']) and not native_only_position(b,root,d) for d in m['-']): possible.add('FCR-DESTROY')
            if any(not any(selector_relation(c, d) == 'same_shape' and key(c) != key(d)
                           for d in m['-']) and not native_only_position(b,root,c) for c in m['+']): possible.add('FCR-MINT')
        # State controls are discovered by the graph, including numeric/stage
        # guards. This selects a property; it does not assert a freeze/pause.
        for use in property_entries:
            for r in summaries.rows(use):
                if not any('debit' in e['may_directions'] and e['holder'] is not None and
                    unit_origin(b,use,e['cell']) and not native_only_position(b,use,e['cell']) for e in r['numeric_effects']): continue
                for control in inv.graph.request_reads(use):
                    if unit_origin(b,use,control):continue
                    if (key_relation(control,f.lookup(use)) or {}).get('kind')=='authorization_quantity':continue
                    if any(w['raw']['path']['root'] == control['root'] and w['operation'] in declared
                           and w['operation'] != use and path_qualification(f,w['operation'],f.paths[w['path']]['raw']) for w in f.writes.values()):
                        possible.add('FCR-FREEZE' if keys(control) else 'FCR-PAUSE')
        if not possible and native_debits:
            possible.add('ADDITIONAL')
        hint = item.get('category')
        if hint in ('FCR-FREEZE','FCR-PAUSE'):
            # Keep the original model label as provenance, but type the
            # investigated scope from the actual source control. A scalar
            # common switch is not an address-keyed freeze, and an indexed
            # holder flag cannot be promoted to collective pause. Neither
            # choice proves the effect; the selected property is still solved.
            source_control = possible & {'FCR-FREEZE','FCR-PAUSE'}
            cat = next(iter(source_control)) if len(source_control) == 1 else hint
        elif hint in possible: cat = hint
        elif len(possible) == 1: cat = next(iter(possible))
        else:
            # Only a hint to a corresponding actual effect is usable. Ambiguous
            # tasks stay open instead of sorting effect names into a risk label.
            cat = None
        if hint == 'ADDITIONAL' and not possible: cat = 'ADDITIONAL'
    relation = {'task': f.options.scope, 'target': target, 'operation': root,
        'category': cat, 'possible_categories': sorted(possible),
        'domain': domain(f.lookup(root)),
        'initial_identity': initial_for_lookup(f.lookup(root))['identity'],
        'objects': cells, 'resource_bindings': known_semantics,
        'expected_authorization': policy, 'actual_guards': [r['guards'] for r in rows],
        'source_operations': sorted(declared), 'stage': item.get('phase'),
        'source_linked_control_uses':sorted(control_uses),
        'control_use_frontier':sorted(test_uses),
        'frontier_meaning':'source token-flow uses for testing the control hypothesis; not inferred effect edges',
        'native_redemption_debits':native_debits,
        'claim_assumptions':copy.deepcopy(item.get('assumptions',[])),
        'semantic_version': inv.semantics.dependency_identity(q['binding']['operations']),
        'semantic_questions': questions, 'summary_identity': summaries.identity,
        'residuals': [x for r in rows for x in r['residuals']] + [r for (t, _),r in
            getattr(b,'unit_conflicts',{}).items() if t==target and any(
                selector_relation(r['cell'],c)=='same_shape' for c in cells)],
        'kind': 'host_typed_source_property', 'model_category_hint': item.get('category'),
        'minimum_evidence': 'applicable source/semantic/program support; no universal SMT requirement'}
    if q.get('history') and item['claim'].strip()!=q['history'][-1]['claim'].strip():
        rootname=f.operations[root]['function'].split('(')[0]
        root_named=bool(re.search(r'(?<![\w$])'+re.escape(rootname)+r'(?![\w$])',text))
        pointed=[]
        for oid,o in f.operations.items():
            if oid==root or o['target']!=target:continue
            name=o['function'].split('(')[0]
            explicit=re.search(r'(?<![\w$])'+re.escape(name)+r'\s*\(',text) or re.search(r'`'+re.escape(name)+r'`',text)
            if re.search(r'[a-z][A-Z]',name):explicit=explicit or re.search(r'(?<![\w$])'+re.escape(name)+r'(?![\w$])',text)
            if explicit:pointed.append(oid)
        origins={key(a) for a in summaries.operations[root]['source_closure']}
        foreign=[o for o in pointed if not {key(a) for a in summaries.operations[o]['source_closure']}<=origins]
        root_role_write=any(not keys(w['path']) and value_type(w['path'],f.lookup(root)) in ('address','address payable') for r in rows for w in r['ordered_writes'])
        changed_kind=(item.get('category') not in possible and f.options.scope=='FCR' or
                      root_role_write and any(summaries.positions(o) for o in foreign) and not re.search(r'\b(?:acquir\w*|takeover|becom\w*|install\w*)\b',text,re.I))
        if foreign and not root_named and changed_kind:
            relation['core_rebinding_required']={'old_core':root,'source_named_candidates':foreign,
                'reason':'revised actual effect does not have the old core source; no old-root credit inherited'}
    # Business identity is not the consumption/cache identity. New evidence,
    # search branches and supplementary-anchor ordering do not change a policy.
    relation['claim_identity'] = digest([f.options.scope, target, root, cat,
        sorted(key(c) for c in cells), item.get('actor'), item.get('object'), item.get('phase'),
        (policy or {}).get('meaning'),((policy or {}).get('compiled_authorization') or {}).get('predicate'),
        relation.get('core_rebinding_required')])
    relation['id'] = 'property_' + digest(relation)[:20]
    return relation


def planning_item(q):
    item = copy.deepcopy(q['current']); p = q.get('property') or {}
    if p.get('category'): item['category'] = p['category']
    if p.get('category')=='AC' and (p.get('expected_authorization') or {}).get('compiled_authorization'):
        if isinstance(item.get('observation'),dict) and item['observation'].get('measure')=='denied_qualified':
            item['observation']['authorization']=p['expected_authorization']['compiled_authorization']
        else:
            item['observation']={'measure':'authorization_violation','authorization':p['expected_authorization']['compiled_authorization']}
    if p.get('category') in ('FCR-TRANSFER', 'FCR-DESTROY', 'FCR-MINT') and p.get('objects'):
        ob = item.get('observation')
        if not isinstance(ob, dict) or ob.get('measure') in (None, 'opens', 'blocks'):
            item['observation'] = {'measure': 'direct_effect'}
    return item


def compose(inv, q, old=None):
    """One decision from typed obligations. Legacy reportable is never read."""
    prop = q.get('property')
    root = inv.root(q)
    item = q['current']
    scope = {'source_prediction': True, 'concrete_EVM': False,
             'deployment_reachability_proved': False, 'entire_contract_safety_proved': False,
             'compiled_property': copy.deepcopy(prop), 'claim_identity': (prop or {}).get('claim_identity'),
             'only_declared_operations': q['binding'].get('operations', []),
             'scoped_observations': [], 'evidence_dependencies': {}, 'semantic_task_review': q.get('task_review')}
    result = {'root': root, 'category': (prop or {}).get('category'), 'reportable': False,
              'reasons': [], 'scope': scope, 'evidence_refs': list(q['evidence'])}
    if not prop or not root or not q['binding'].get('core_exact', q['binding'].get('exact')):
        result['reasons'] = ['source_identity_ambiguous_or_unresolved' if root is None else 'validated_property_not_available']
        return result
    if prop.get('core_rebinding_required'):
        result['reasons'] = ['changed_business_effect_requires_source_rebinding']
        return result
    scope['expected_authorization'] = prop.get('expected_authorization')
    scope['model_original_judgment'] = {'assessment': item.get('assessment'), 'claim': item.get('claim')}
    cat = prop.get('category')
    if not cat:
        result['reasons'] = ['property_task_meaning_unresolved']
        return result
    inspections = [inv.evidence[label] for label in q['evidence']
                   if inv.evidence[label].get('kind') == 'source_inspection' and inv.evidence[label].get('operation') == root]
    scope['source_deductions'] = [{'evidence': r['id'], 'no_committing_path': r.get('no_committing_path'),
                                 'net_unchanged': r.get('net_effect_proved_unchanged')} for r in inspections]
    observation = item.get('observation')
    measure = observation.get('measure') if isinstance(observation, dict) else None
    if measure != 'denied_qualified':
        reason = next(('original_root_has_no_committing_path' if r.get('no_committing_path')
                       else 'original_root_net_effect_is_unchanged' for r in inspections
                       if r.get('no_committing_path') or r.get('net_effect_proved_unchanged')), None)
        if reason:
            result['reasons'] = [reason]
            scope['route_status'] = 'excluded'
            scope['necessary_conditions'] = {'actual_effect': 'refuted_by_complete_source',
                                            'other_unknowns_decisive_for_this_route': False}
            return result
    current = [e for label in q['evidence'] for e in [inv.evidence[label]]
               if e.get('source_identity') == inv.f.identity and
               (e.get('property_validation_key') == validation_key(prop) or e.get('property_identity') == prop['id'])]
    queries = [x for e in current for x in e.get('queries', [])
               if x.get('details', {}).get('property_identity') == prop['id'] or
               e.get('property_validation_key') == validation_key(prop)]
    scope['revalidated_evidence'] = [{'evidence': e['id'], 'validation_key': e.get('property_validation_key')}
                                   for e in current]
    if inv.f.options.scope == 'AC':
        policy = prop.get('expected_authorization') or {}
        expected = policy.get('compiled_authorization')
        if not expected:
            result['reasons'] = ['expected_authorization_not_established']
            return result
        label = 'denied_qualified' if measure == 'denied_qualified' else 'authorization_violation'
        relevant = [x for x in queries if x.get('label') == label and x.get('details', {}).get('property_validated')]
        positives = [x for x in relevant if x.get('validated_bounded_witness')]
        source_support = [e for e in current if e.get('kind') == 'source_property_certificate' and
                          e.get('property_validated') and e.get('supports') == label]
        all_paths = {pid for pid, _ in inv.f.operation_paths(root, True)}
        excluded = {x['details'].get('use_path') for x in relevant if x.get('answer') == 'unsat'
                    and not x.get('abstract_hash') and (x.get('exclusion_certificate', {}).get('excludes_only_this_formula')
                    or x.get('details', {}).get('prestate', {}).get('global_reachability_exhausted'))}
        scope['property_support'] = [{'policy': policy, 'queries': [x['id'] for x in relevant]}]
        scope['authorization_counterevidence'] = [x['id'] for x in relevant if x.get('answer') == 'unsat']
        result['reportable'] = bool(positives or source_support)
        scope['source_property_certificates'] = [e['id'] for e in source_support]
        if not result['reportable']:
            if all_paths and all_paths <= excluded and inv.backend.complete(root) and not expected.get('competing_interpretations'):
                result['reasons'] = ['expected_authorization_covers_all_applicable_paths']
                scope['route_status'] = 'excluded'
            else:
                result['reasons'] = ['authorization_violation_not_established']
        else:
            scope['positive_condition_scopes'] = [{'probe': x['id'], 'details': x['details']} for x in positives]
    else:
        relevant = [x for x in queries if x.get('details', {}).get('property_validated') and
                    x.get('label') in ('direct_effect', 'financial_block')]
        positive = [x for x in relevant if x.get('validated_bounded_witness')]
        checks = [e.get('financial_scope') for e in current if e.get('financial_scope')]
        scope['comparison_alignment'] = {'status': 'main' if positive else 'unresolved',
                                         'conditions': checks, 'source_basis': prop.get('resource_bindings', []),
                                         'prestate_alignment': prop['domain']}
        if cat in ('FCR-PAUSE', 'FCR-FREEZE'):
            positive = positive if any(e.get('scope_supported') for e in current) else []
        result['reportable'] = bool(positive)
        scope['property_support'] = [{'probe': x['id'], 'details': x['details']} for x in positive]
        if not positive:
            excluded = any(e.get('property_excluded') for e in current)
            result['reasons'] = ['matched_direct_effect_impossible_on_all_applicable_positions_and_paths'
                                 if excluded else 'financial_property_conditions_not_established']
            if excluded:
                scope['route_status'] = 'excluded'
                scope['comparison_alignment']['status'] = 'refuted'
        scope['normal_explanations'] = copy.deepcopy(q.get('local_normal_explanations', []))
    if result['reportable']:
        scope['route_status'] = 'supported'
        result['composed_claim'] = (f"{cat}: {inv.catalog.name(root)} establishes the source-bound "
                                    f"{'authorization violation' if cat == 'AC' else 'financial capability'} "
                                    f"under {prop['domain']}. The recorded property specifies subjects, effects and scope.")
        result['evidence_level'] = 'source_semantic_and_program'
    return result


def applicable_normal_authorization(inv,q,policy):
    """Only a checked applicable predicate can close a normal proposal.

    A stage/quantity guard, or the word normal, is never a certificate. The
    query must use this exact property, its actual operands and every complete
    committing path. Partial normal evidence stays local.
    """
    root=inv.root(q);p=q.get('property') or {}
    if not root or inv._direction_contradictions(q):return False
    rows={pid for pid,_ in inv.f.operation_paths(root,True)}
    if not rows or not inv.backend.complete(root):return False
    checked=[x for label in q['evidence'] for x in inv.evidence[label].get('queries',[])
        if x.get('label')=='authorization_violation' and x.get('details',{}).get('property_identity')==p.get('id')]
    if any(x.get('validated_bounded_witness') for x in checked):return False
    covered={x['details'].get('use_path') for x in checked if x.get('answer')=='unsat' and not x.get('abstract_hash') and
        x['details'].get('argument_domain')=='all_source_inputs_on_this_committing_path' and
        x['details'].get('prestate',{}).get('analysis_domain')=='ac_checked_prestate_r1'}
    return rows<=covered



def validation_key(p):
    if not p:
        return None
    resources = []
    for row in p.get('resource_bindings', []):
        binding = row.get('binding') or {}
        resources.append([row.get('kind'), binding.get('meaning'),
                          (binding.get('semantic_assertion') or {}).get('unit_kind')])
    expected = (p.get('expected_authorization') or {}).get('compiled_authorization') or {}
    return digest([p.get('claim_identity'),p.get('domain'),p.get('initial_identity'),
        p.get('summary_identity'),p.get('objects'),p.get('claim_assumptions'),p.get('stage'),
        expected.get('predicate'),expected.get('property_family'),expected.get('acquisition_uses'),
        expected.get('competing_interpretations'),resources])

````

## runtime/common.py

原文件 SHA-256 `8cd0cf1814b51a833f8bc67e82b96915ed961407e44b6a50b21f04f0cf2f68c8`

````python
from pathlib import Path
import json,hashlib,sys
R=Path(__file__).resolve().parents[1]
SOURCE=R/'source'
sys.path[:0]=[str(SOURCE/'src'),str(SOURCE/'runtime')]
from pr_next_joint.core import digest
from pr_next_joint.investigation.contracts import write
ROUND='permission-risks-next-revision-full200-20261112-r1'
def read(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def wire(messages):return {'model':'deepseek-flash','messages':messages,
 'response_format':{'type':'json_object'},'thinking':{'type':'enabled'},
 'reasoning_effort':'high','stream':False,'max_tokens':32768}
def safe_error(e):return type(e).__name__+':'+str(e)[:600]

````

## runtime/input_links.py

原文件 SHA-256 `b1b8b6d4b9895c66869fbd3d4451f7e8dfb8207f79d5bfe3f4fe00898af9e3af`

````python
"""Use precisely the fixed locally pinned compilation identities checked against instance files on launch; no compiler or Gold."""
from pathlib import Path
from common import R,SOURCE,read,write,sha,digest

def source_identity():
 actual={p.relative_to(SOURCE/'src/pr_next_joint').as_posix():sha(p) for p in sorted((SOURCE/'src/pr_next_joint').rglob('*.py'))}
 identity=read(R/'IDENTITY.json')
 if actual!=read(R/'METHOD_SHA.json') or digest(actual)!=identity['method_sha256'] or len(actual)!=identity['method_python_files']:
  raise ValueError('frozen_successor_method_identity')
 if sha(R/'METHOD_CONFIG.json')!=identity['config_sha256'] or sha(SOURCE/'configs/full.json')!=identity['config_sha256']:
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
   if not q.is_relative_to(root) or not q.is_file():raise ValueError('missing_compilation:'+member)
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

````

## runtime/ledger.py

原文件 SHA-256 `e43fabb1c3b749bf4523bead2b67512e2ada9769990f7bbfffb280941168f824`

````python
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

````

