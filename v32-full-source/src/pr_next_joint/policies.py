"""Source-backed policy instances, separately bound from success/effect checks."""
import copy,itertools
from .core import *
from .source_paths import paths_in,compatible,stable
from .relations import return_value,observer_paths

def find_getter(tracer,path,domain):
 matches=[]
 for f in tracer.contract['functions']:
  if not f['readonly'] or len(f['outputs'])!=1 or len(f['types'])>2:continue
  if f['outputs'][0] not in ['bool','address'] and not f['outputs'][0].startswith('uint'):continue
  options=[]
  for typ in f['types']:
   options.append([v for v in domain if (typ=='address' and v.startswith('$')) or (typ.startswith('uint') and v.isdecimal())])
  if any(not x for x in options):continue
  for args in itertools.islice(itertools.product(*options),32):
   try:
    t=tracer.trace(f['signature'],list(args),'$A')
    if return_value(t)==path and t['native_agreement']:
     out=f['outputs'][0];typ='Bool' if out=='bool' else 'Address160' if out=='address' else 'BV'+(out[4:] or '256')
     matches.append({'function':f['signature'],'arguments':list(args),'output_index':0,'type':typ,'source':t['entry']})
   except Invalid:continue
 require(matches,'unobservable_policy_key')
 # All retained alternatives return this exact path; choosing one transport
 # representation does not resolve semantically different bindings.
 return sorted(matches,key=lambda x:digest(x))[0],matches

def management_policy(tracer,transactions,qualification,grant_index):
 qpaths,qtrace=observer_paths(tracer,qualification);grant=copy.deepcopy(transactions[grant_index-1]);grant['sender']='B'
 managed=tracer.trace(grant['function'],grant['arguments'],'$B')
 require(managed['native_agreement'],'management_native_mismatch')
 prefix=[tracer.trace(t['function'],t['arguments'],'$'+t['sender']) for t in transactions[:grant_index-1]]
 bootstrap=[w for t in prefix for w in t['writes']]
 domain=sorted(set(v for t in transactions for v in t['arguments']))
 bindings=[];requirements=[];allowed=None;independent=[]
 qfunc=tracer.function(qualification['function']);qid=qfunc.get('id')
 calls=[c for c in managed['calls'] if c['function']==qid] if qid else []
 expected=[tracer.literal(v,t) for v,t in zip(qualification['arguments'],tracer.abi[qualification['function']]['types'])]
 if calls:
  require(len({stable(c['arguments']) for c in calls})==1,'ambiguous_management_credential')
  for actual,want in zip(calls[0]['arguments'],expected):
   if actual==want:continue
   require(actual.get('kind')=='storage' and want.get('kind')=='literal','unresolved_credential_key')
   g,alternatives=find_getter(tracer,actual,domain);g['id']='policy_key_'+str(len(bindings));bindings.append(g)
   requirements.append({'observer':g['id'],'type':g['type'],'equals':want['value'],'source_path':actual,'equivalent_getters':alternatives})
  # Independent constructor/initializer grants the corresponding credential
  # to the declared setup principal, not to the investigated caller.
  for p in qpaths:
   p=copy.deepcopy(p)
   for s in p['segments']:
    if s.get('key')=={'kind':'literal','value':'$B'}:s['key']={'kind':'literal','value':'$A'}
   independent.extend(w for w in bootstrap if compatible(w['path'],p))
  allowed={'kind':'qualification','observer':'qualified'}
 else:
  # A direct caller-to-administrative-account equality. It is accepted only
  # when an independent deployment prefix actually sources that account.
  for guard in managed['guards']:
   condition=guard['condition']
   if condition.get('kind')!='op' or condition.get('op')!='==':continue
   args=condition['args']
   for account,subject in [args,args[::-1]]:
    if account.get('kind')=='storage' and subject=={'kind':'literal','value':'$B'}:
     matches=[w for w in bootstrap if compatible(w['path'],account) and w['value']=={'kind':'literal','value':'$A'}]
     if not matches:continue
     g,alternatives=find_getter(tracer,account,domain);g['id']='management_authority';bindings.append(g)
     independent.extend(matches);allowed={'kind':'account_equality','observer':g['id'],'subject':'B','source_guard':guard,'equivalent_getters':alternatives}
  # Direct qualification guard, common in flat role maps.
  if allowed is None:
   in_guards=[p for g in managed['guards'] for p in paths_in(g['condition'])]
   if any(compatible(a,b) for a in in_guards for b in qpaths):
    for p in qpaths:
     p=copy.deepcopy(p)
     for s in p['segments']:
      if s.get('key')=={'kind':'literal','value':'$B'}:s['key']={'kind':'literal','value':'$A'}
     independent.extend(w for w in bootstrap if compatible(w['path'],p))
    allowed={'kind':'qualification','observer':'qualified'}
 require(allowed is not None and independent,'insufficient_independent_management_policy')
 return {'kind':'program_inferred','protected_object':'source-bound qualification and downstream effects','subject':'B','credential_paths':qpaths,'management_source':managed['entry'],'independent_bootstrap_writes':independent,'allowed_binding':allowed,'key_requirements':requirements,'observers':bindings,'alternative_authorization_scope':'fixed direct EOA calls; no injected state, delegated signatures, unknown external code or contract-origin branch','open_alternatives':[],'normal_exclusions':['honest setup principal actions','currently qualified caller','a later successful legitimate regrant'], 'inference_not_external_business_specification':True}

def allowed_expression(policy,step,actors):
 a=policy['allowed_binding']
 if a['kind']=='qualification':return obs(a['observer']+'.'+str(step),'Bool')
 return operator('eq','Bool',obs(a['observer']+'.'+str(step),'Address160'),lit('Address160',actors[a['subject']]['address']))

def key_requirements(policy,step):
 return [operator('eq','Bool',obs(x['observer']+'.'+str(step),x['type']),lit(x['type'],x['equals'])) for x in policy['key_requirements']]
