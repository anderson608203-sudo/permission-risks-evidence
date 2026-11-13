"""Single bounded candidate queue. Evidence validity binds every semantic identity."""
import json,pathlib,time
from .core import digest,require

class Scheduler:
 def __init__(self,path,project_seconds=1800):
  self.path=pathlib.Path(path);self.start=time.monotonic();self.project_seconds=project_seconds
  self.rows=[json.loads(l) for l in self.path.read_text().splitlines()] if self.path.exists() else []
  self.reporting=any(r.get('event')=='reporting_closed_no_reentry' for r in self.rows)
 def emit(self,r):
  self.path.parent.mkdir(parents=True,exist_ok=True)
  with self.path.open('a') as f:f.write(json.dumps(r)+'\n')
  self.rows.append(r)
 def admit(self,candidate):
  require(not self.reporting,'report_cannot_restart_analysis')
  require(time.monotonic()-self.start<self.project_seconds,'project_time_budget')
  p=candidate['proposal'];require(p['revision']<=2,'revision_cap')
  semantic=digest({'program':p['program_id'],'target':p['target_refs'],'actors':p['actors'],'plan':candidate['plan'],'state_claims':p['state_claims']})
  previous=[r for r in self.rows if r.get('semantic_key')==semantic]
  if previous:return None
  require(sum(r.get('event')=='admitted' for r in self.rows)<32,'plans_per_target_cap')
  self.emit({'event':'admitted','proposal_id':p['id'],'revision':p['revision'],'semantic_key':semantic,'identity_hash':digest(candidate),'started_monotonic':time.monotonic()})
  return time.monotonic()+180
 def finish(self,candidate,result):
  self.emit({'event':'checked','identity_hash':digest(candidate),'result_hash':digest(result),'status':'reported' if result.get('verdict')!='inconclusive' else 'unresolved'})
 def report(self):
  self.reporting=True;self.emit({'event':'reporting_closed_no_reentry'})

def evidence_matches(plan,evidence):
 return all(evidence.get(k)==plan.get(k) for k in ['program_id','build_id','query_ref','plan_ref','backend_fingerprint'])
