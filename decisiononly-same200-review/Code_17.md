# 实跑源码文本 · 第 17 页

## file-cd9bd2e3e63c21

`supplement/two.py` · 原字节 SHA-256 `12f996a0e3b2e1c5b822b98432802c9af542070a1fba13f7105c7101e500ac85`

~~~~python
"""Independent decision-only supplement. Main run, ledger and freeze are read-only."""
from pathlib import Path
import concurrent.futures,fcntl,getpass,hashlib,json,os,shutil,signal,sqlite3,subprocess,sys,time

R=Path(__file__).resolve().parent
P=R.parents[1]
MAIN=P/'run'
O=R/'run'
IDS=('RQ1_a906c0b62c0b','RQ1_aaeb3f57cfd0')
def rd(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,data):
    temp=p.with_suffix('.tmp');temp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');temp.replace(p)
def run():
    fd=(R/'LOCK').open('a');fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    assert not (O/'AUTHORIZATION.json').exists(),'supplement already attempted: no automatic resend'
    for row in rd(R/'MANIFEST.json')['files']:assert sha(R/row['path'])==row['sha256']
    root_grant=rd(MAIN/'AUTHORIZATION.json');end=rd(MAIN/'ENDED.json')
    assert sha(MAIN/'PREDICTIONS_FROZEN.json')==rd(R/'REPAIR.json')['main_freeze_sha256']
    assert end['reason']=='normal_completion'
    parent=sqlite3.connect('file:'+str(MAIN/'requests.sqlite')+'?mode=ro',uri=True)
    assert parent.execute('select count(*) from requests').fetchone()[0]==374
    for m in IDS:assert parent.execute('select idx,state from requests where member=?',(m,)).fetchall()==[(0,'settled')]
    assert end['ledger']['unknown']==end['ledger']['inflight']==0 and root_grant['max_requests']>=376
    assert end['ledger']['settled_cost_usd_upper']+2*.049152<=root_grant['max_usd']
    assert time.time()<root_grant['deadline_epoch'],'original deadline expired'
    sys.path.insert(0,str(R/'runtime'))
    from input_links import source_identity
    from ledger import Ledger
    source=source_identity()
    assert source['method']==rd(R/'REPAIR.json')['method_sha256']
    key=os.environ.get('DEEPSEEK_API_KEY') or getpass.getpass('DeepSeek API key（不回显）：')
    if not key.strip():raise SystemExit('未输入密钥，未启动')
    O.mkdir(exist_ok=True);(O/'service').mkdir(exist_ok=True)
    shutil.copy2(MAIN/'service/SERVICE_ACTUAL.json',O/'service/SERVICE_ACTUAL.json')
    assert time.time()-rd(O/'service/SERVICE_ACTUAL.json')['epoch']<86400
    shutil.copy2(MAIN/'TOKENIZER_ROOT.json',O/'TOKENIZER_ROOT.json')
    jobs=rd(MAIN/'JOBS.json');put(O/'JOBS.json',{m:jobs[m] for m in IDS})
    grant=dict(root_grant,implementation_sha256=source['method'],package_manifest_sha256=sha(R/'MANIFEST.json'),
        members=list(IDS),max_requests=2,per_member_max=1,max_usd=.098304,
        parent_grant_sha256=sha(MAIN/'AUTHORIZATION.json'),supplement='explicit_user_requested_new_first_answer_in_last_available_slot')
    put(O/'AUTHORIZATION.json',grant);Ledger(O/'requests.sqlite').initialize(grant)
    env=dict(os.environ,DEEPSEEK_API_KEY=key,PYTHONDONTWRITEBYTECODE='1',PYTHONUNBUFFERED='1',
        PYTHONPATH=os.pathsep.join(map(str,[R/'runtime',R/'source/src',R/'source/runtime'])))
    with (O/'progress.log').open('ab') as log:
        child=subprocess.Popen([sys.executable,'-B',str(__file__),'--execute'],env=env,stdin=subprocess.DEVNULL,
            stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
    print('两份补跑已启动，PID',child.pid,flush=True)
def execute():
    sys.path.insert(0,str(R/'runtime'))
    from ledger import Ledger
    ledger=Ledger(O/'requests.sqlite');deadline=rd(O/'AUTHORIZATION.json')['deadline_epoch'];results={}
    def one(m):
        out=O/'members'/m;out.mkdir(parents=True)
        cmd=[sys.executable,'-B',str(R/'runtime/worker.py'),'--member',m,'--task','FCR','--inputs',str(R),'--out',str(out/'attempt_1'),'--run',str(O)]
        with (out/'worker.log').open('wb') as log:
            proc=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
            try:proc.wait(timeout=max(.01,min(3720,deadline-time.time())))
            except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
        e=out/'attempt_1/ENTRY_RESULT.json';v=rd(e) if e.exists() else {'member':m,'report_saved':False,'reason':'worker_exit_or_deadline'}
        if v.get('report_saved'):
            report=out/'attempt_1/analysis/report.json';mf=rd(out/'attempt_1/analysis/prediction_manifest.json')
            assert mf['report_sha256']==sha(report) and mf['implementation_sha256']==rd(R/'REPAIR.json')['method_sha256']
            assert mf['predictions']==rd(out/'attempt_1/prediction_export.json')['predictions']
            assert ledger.snapshot(m)['real_model_calls']==1
            if not v.get('analysis_available'):v['selection_ineligible']='no_usable_analysis'
        return v
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        pending={pool.submit(one,m):m for m in IDS}
        while pending:
            done,_=concurrent.futures.wait(pending,timeout=20,return_when=concurrent.futures.FIRST_COMPLETED)
            for f in done:
                m=pending.pop(f)
                try:results[m]=f.result()
                except Exception as ex:results[m]={'member':m,'report_saved':False,'technical_error':type(ex).__name__}
            print('补跑进度',len(results),'/2；新请求',ledger.snapshot()['real_model_calls'],flush=True)
    ledger.recover(); summary=ledger.snapshot()
    put(O/'SUPPLEMENT_FROZEN.json',{'main_freeze_sha256':sha(MAIN/'PREDICTIONS_FROZEN.json'),
        'members':results,'files':{str(p.relative_to(O)):sha(p) for base in (O/'requests',O/'members') for p in base.rglob('*') if p.is_file()},
        'parent_reports':198,'new_result_provenance':'separate_compatibility_source_and_new_response',
        'main_request_count':374,'supplement_accounting':{k:v for k,v in summary.items() if k!='usage_records'},
        'prediction_frozen_before_scoring':True,'end_epoch':time.time()})
    print('补跑结束；有效报告',sum(bool(v.get('report_saved') and not v.get('selection_ineligible')) for v in results.values()),'/2；可打包',flush=True)
if __name__=='__main__':
    if '--execute' in sys.argv:execute()
    else:run()

~~~~
