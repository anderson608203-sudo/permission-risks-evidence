"""Generic key-aware candidate construction. Names identify ABI calls, never risk."""
import copy,itertools
from .core import *
from .source_paths import SourcePaths,compatible,paths_in,stable
from . import SCHEMA_VERSION

def analyze_bindings(bundles,instances,calls,native=None,policy=None):
 """Production static entry, deliberately independent of risk construction."""
 from .bindings import analyze
 return analyze(bundles,instances,calls,native,policy)

def return_value(trace,index=0):
 require(len(trace['returns'])==1,'ambiguous_getter_return')
 value=trace['returns'][0]
 if value.get('kind')=='tuple':value=value['items'][index]
 else:require(index==0,'getter_index')
 return value

def observer_paths(tracer,spec):
 entry=tracer.abi.get(spec['function']);require(entry is not None and entry['readonly'],'observer_original_readonly_abi')
 ix=spec.get('output_index',0);require(type(ix)is int and 0<=ix<len(entry['outputs']),'observer_output_index')
 out=entry['outputs'][ix];expected='Bool' if out=='bool' else 'Address160' if out=='address' else 'BV'+(out[4:] or '256') if out.startswith('uint') else None
 require(spec['type']==expected,'observer_output_type')
 t=tracer.trace(spec['function'],spec['arguments'],'$'+spec.get('caller','A'))
 require(t['native_agreement'],'native_getter_disagreement')
 return list(paths_in(return_value(t,spec.get('output_index',0)))),t

def normalized_abi(d,contract):
 d=copy.deepcopy(d);changes=[];abi={x['signature']:x for x in contract['functions']}
 entries=d.get('transactions',[])+[d['qualification']]+d.get('effect_observers',[])+d.get('financial_observers',[])
 for e in entries:
  name=e['function']
  if name=='constructor':continue
  if name not in abi:
   matches=[f for f in abi if f.split('(')[0]==name and len(abi[f]['types'])==len(e['arguments'])]
   require(len(matches)==1,'ambiguous_short_abi_name')
   e['function']=matches[0];changes.append({'repair':'unique_abi_identifier','before':name,'after':matches[0]})
 if d['transactions'][0]['function']!='constructor':
  require(not contract['constructor_types'],'missing_constructor_arguments')
  d['transactions'].insert(0,{'sender':'A','function':'constructor','arguments':[],'environment_prefix':True});changes.append({'repair':'counted_noarg_original_creation'})
 for i,t in enumerate(d['transactions'],1):
  types=contract['constructor_types'] if t['function']=='constructor' else abi[t['function']]['types']
  require(len(types)==len(t['arguments']),'abi_arity')
  require(t['sender'] in ['A','B','C'],'unknown_subject')
  for typ,v in zip(types,t['arguments']):
   require(isinstance(v,str),'abi_string_input')
   require('[' not in typ and typ not in ['bytes','tuple'],'unsupported_dynamic_abi')
   if typ=='string':require(i<=2 and len(v.encode())<=64 and t['sender']=='A','initializer_only_string')
  t['environment_prefix']=t['sender']=='A'
 return d,changes

def same_subject_path(path,subject):return any(s.get('key')=={'kind':'literal','value':subject} for s in path['segments'])

def boolean_effect_routes(tracer,qualification):
 """Finite scalar setter/getter construction, independent of names and order."""
 qp,_=observer_paths(tracer,qualification);routes=[]
 for f in sorted(tracer.contract['functions'],key=lambda f:f['selector']):
  if f['readonly'] or f['types']!=['address','bool']:continue
  t=tracer.trace(f['signature'],['$C','true'],'$B')
  if not t['native_agreement'] or not any(compatible(r,p) for r in t['reads'] for p in qp):continue
  for getter in sorted(tracer.contract['functions'],key=lambda f:f['selector']):
   if not getter['readonly'] or getter['types']!=['address'] or getter['outputs']!=['bool']:continue
   spec={'id':'effect','function':getter['signature'],'arguments':['$C'],'type':'Bool','output_index':0}
   paths,_=observer_paths(tracer,spec)
   writes=[w for w in t['writes'] if w['value']=={'kind':'literal','value':True} and any(compatible(w['path'],p) for p in paths)]
   if writes and all(same_subject_path(p,'$C') for p in paths):
    routes.append({'use':{'sender':'B','function':f['signature'],'arguments':['$C','true'],'environment_prefix':False},'post':{'sender':'B','function':f['signature'],'arguments':['$C','false'],'environment_prefix':False},'observer':spec,'source_writes':writes})
 return routes

def declining(write):return write['operator']=='delete' or write['value']=={'kind':'literal','value':False} or write['value']=={'kind':'literal','value':0}

def generate_lifecycles(record,bundle,contract):
 d,changes=normalized_abi(record['proposal_draft'],contract);tracer=SourcePaths(bundle,contract)
 q={**d['qualification'],'id':'qualified'};qpaths,qtrace=observer_paths(tracer,q)
 require(qpaths and all(same_subject_path(p,'$B') for p in qpaths),'qualification_subject_not_B')
 txs=d['transactions'];traces=[tracer.trace(t['function'],t['arguments'],'$'+t['sender']) for t in txs]
 require(all(t['native_agreement'] for t in traces),'native_write_disagreement')
 relevant=[]
 for i,(tx,t) in enumerate(zip(txs,traces)):
  if i==0 or any(typ=='string' for typ in tracer.abi[tx['function']]['types']):continue
  writes=[w for w in t['writes'] if any(compatible(w['path'],p) for p in qpaths)]
  if writes:relevant.append((i,tx,t,writes))
 grants=[r for r in relevant if any(not declining(w) for w in r[3])]
 revokes=[r for r in relevant if all(declining(w) for w in r[3])]
 require(grants and revokes,'missing_source_bound_lifecycle_actions')
 cases=[]
 for g,rv in itertools.product(grants,revokes):
  if d.get('financial_observers'):
   plan=copy.deepcopy(txs);routes=[{'plan':plan,'observers':d['financial_observers'],'generation':'source-bound existing proposed transaction sequence'}]
  else:
   routes=[]
   for route in boolean_effect_routes(tracer,q):
    grant={**g[1],'sender':'A','environment_prefix':True};revoke={**rv[1],'sender':'A','environment_prefix':True}
    routes.append({'plan':copy.deepcopy(txs[:g[0]])+[grant,route['use'],revoke,route['post']],'observers':[route['observer']],'generation':'generic finite boolean management effect construction from key-matched reads/writes; no diagnostic feedback'})
  for route in routes:
   require(len(route['plan'])<=6,'six_transaction_limit')
   cases.append({'draft':d,'transactions':route['plan'],'observers':[q]+route['observers'],'normalization':changes,'generation':route['generation'],'raw_record_ref':ref(record),'parent_revision':record.get('candidate_revision',0),'source_dependencies':{'qualifier':qtrace,'grant':g[2],'revoke':rv[2]}})
 require(len(cases)<=32,'finite_candidate_bound');return cases

def arithmetic_delta_term(write,sign):
 """Recognize source x := x +/- amount, including internal arithmetic helpers."""
 value=write['value']
 if value.get('kind')=='op' and value.get('op')==sign and len(value['args'])==2:
  a,b=value['args']
  if a.get('kind')=='storage' and compatible(write['path'],a):return b
 if write['operator']==sign+'=':return value
 return None

def financial_binding(tracer,plan,observers,effect):
 specs={o['id']:o for o in observers}
 if not {'balance','supply'}<=set(specs):return {'applicable':False,'reason':'no proposed financial observation pair'}
 bp,_=observer_paths(tracer,specs['balance']);sp,_=observer_paths(tracer,specs['supply'])
 require(len(bp)==len(sp)==1,'ambiguous_financial_getter')
 require(bp[0]['segments'] and not sp[0]['segments'],'financial_resource_shape')
 tx=plan[effect-1];trace=tracer.trace(tx['function'],tx['arguments'],'$'+tx['sender'])
 balance=[w for w in trace['writes'] if compatible(w['path'],bp[0])]
 supply=[w for w in trace['writes'] if compatible(w['path'],sp[0])]
 additions=[(a,b) for a in balance for b in supply if arithmetic_delta_term(a,'+') is not None and arithmetic_delta_term(a,'+')==arithmetic_delta_term(b,'+')]
 transfers=[]
 for f in tracer.contract['functions']:
  if f['readonly'] or f['types']!=['address','uint256']:continue
  t=tracer.trace(f['signature'],['$C','1'],'$B')
  ws=[w for w in t['writes'] if w['path']['root']==bp[0]['root']]
  debit=[w for w in ws if same_subject_path(w['path'],'$B') and arithmetic_delta_term(w,'-') is not None]
  credit=[w for w in ws if same_subject_path(w['path'],'$C') and arithmetic_delta_term(w,'+') is not None]
  if t['native_agreement'] and any(arithmetic_delta_term(a,'-')==arithmetic_delta_term(b,'+') for a in debit for b in credit) and not any(w['path']['root']==sp[0]['root'] for w in t['writes']):
   transfers.append({'function':f['signature'],'source':t['entry'],'debits':debit,'credits':credit})
 return {'applicable':bool(additions and transfers),'balance_path':bp[0],'supply_path':sp[0],'issuance_writes':additions,'spendability_and_transfer_sources':transfers,'rule_basis':'approved_rule','reason':'same sourced quantity added to spendable holder rights and global supply; ordinary same-resource transfer conserves supply' if additions and transfers else 'missing issuance or spendability evidence'}
