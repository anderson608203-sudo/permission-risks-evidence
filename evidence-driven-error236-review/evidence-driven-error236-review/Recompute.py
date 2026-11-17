"""Standalone read-only recount. Stdlib only; never imports the detector or opens network."""
from pathlib import Path
from collections import Counter
import argparse,json,zipfile,hashlib,math

def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def main():
 p=argparse.ArgumentParser();p.add_argument('--lite',type=Path,required=True);p.add_argument('--source',type=Path);args=p.parse_args()
 with zipfile.ZipFile(args.lite) as z:
  assert len(z.namelist())==len(set(z.namelist()))
  def read(n):return json.loads(z.read(n))
  roots=read('evaluation/Roots.json');adjudication=read('evaluation/Adjudication.json');published=read('evaluation/Scores.json');refs=read('evaluation/frozen_reference/AC_Refs.json');truth=read('evaluation/frozen_reference/FCR_Refs.json');results=read('original/run/RESULTS.json');frozen=read('original/run/PREDICTIONS_FROZEN.json');jobs=read('original/run/JOBS.json')
  assert len(results)==236 and len({r['member'] for r in results})==236
  predictions={};found={};reports=0
  for r in results:
   m=r['member'];j=jobs[m]['expected']
   snapshot=read(f'original/run/input_snapshots/{m}/identity.json');assert snapshot['source_hashes']==j['source_hashes'] and snapshot['targets']==j['targets_selected']
   for name,h in j['source_hashes'].items():assert sha(z.read(f'original/run/input_snapshots/{m}/sources/{name}'))==h
   if not r.get('report_saved'):
    predictions[m]={'failed':True};continue
   base=f'run/members/{m}/attempt_1/';reportname=base+'analysis/report.json';raw=z.read('original/'+reportname);report=json.loads(raw);manifest=read('original/'+base+'analysis/prediction_manifest.json');export=read('original/'+base+'prediction_export.json')
   assert sha(raw)==r['report_sha256']==manifest['report_sha256']==frozen['files'][reportname[4:]]
   assert report['decision_sha256']==sha(canonical([report['findings'],report['inspection_records'],report['task_analysis']['reading_scope'],report['unresolved_category_judgments']]))
   assert manifest['predictions']==export['predictions'];predictions[m]=export['predictions'];reports+=1
   for f in report['findings']:found[(m,f['id'])]=f
  assert reports==235
  author_ids={v['id'] for m,rs in refs.items() if m in predictions for v in rs};assert author_ids=={r['reference'] for r in roots} and len(author_ids)==296
  hit=set();extra=set()
  for a in adjudication:
   f=found[(a['member'],a['finding'])];assert f['root_location']['start']==a['start'] and f['category']=='AC'
   if a['reference']:
    assert a['reference'] in author_ids;hit.add(a['reference'])
   else:extra.add((a['member'],a['file'],a['start']))
  ac=dict(TP=len(hit),FP=len(extra),FN=len(author_ids)-len(hit));assert all(ac[k]==published['AC'][k] for k in ac)
  fcr={}
  for short in ['TRANSFER','MINT','DESTROY','PAUSE','FREEZE']:
   cat='FCR-'+short;c=dict(Total=0,TP=0,FP=0,FN=0,TN=0,unknown_risk=0,unknown_repair=0,failed_risk=0,failed_repair=0)
   for r in results:
    m=r['member']
    if r['task']!='FCR' or truth[m]['target']!=cat:continue
    c['Total']+=1;pos=truth[m]['positive'];failed=predictions[m].get('failed',False);state=predictions[m].get(cat)
    if pos:
     if state=='alarm':c['TP']+=1
     else:
      c['FN']+=1
      if failed:c['failed_risk']+=1
      elif state!='not_detected':c['unknown_risk']+=1
    elif state=='alarm':c['FP']+=1
    elif state=='not_detected':c['TN']+=1
    elif failed:c['failed_repair']+=1
    else:c['unknown_repair']+=1
   assert all(c[k]==published['FCR'][short][k] for k in c);fcr[short]=c
  intents=[n for n in z.namelist() if n.startswith('original/run/requests/') and n.endswith('/intent.json')];receipts=[read(n.replace('intent.json','receipt.json')) for n in intents]
  assert len(intents)==443 and all(not r['simulated'] and not r['response_body_retained'] for r in receipts)
  assert math.isclose(sum(r['cost_usd_upper'] for r in receipts),2.579596704)
  source_checked=False
  if args.source:
   with zipfile.ZipFile(args.source) as src:
    pins=json.loads(src.read('METHOD_SHA.json'));actual={n:sha(src.read('source/src/pr_next_joint/'+n)) for n in pins};assert len(actual)==99 and sha(canonical(actual))=='fb113462e5d4a7170877357ffad4fef3fe9e16a749cb3a723cf2f85e4d2110fc';source_checked=True
 print(json.dumps(dict(verified=True,AC=ac,FCR=fcr,reports=235,failed=1,requests=443,source99_checked=source_checked,note='Recounts depend on published root adjudication; they do not independently prove semantic vulnerability truth. No model/detection/solver run.'),ensure_ascii=False,indent=2))
if __name__=='__main__':main()

