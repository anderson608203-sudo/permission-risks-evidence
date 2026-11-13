"""Account partitions, not risk queries. Contracts are never merged into EOAs."""
import copy
from .core import require,digest
from .facts import walk

SCHEMA='subject-partitions-v1'

def subject(name):return {'kind':'subject','symbol':name}

def partitions(names):
 """Canonical set partitions, independent of names and fixture outcomes."""
 def visit(index,groups):
  if index==len(names):
   yield copy.deepcopy(groups);return
  for group in groups:
   group.append(names[index]);yield from visit(index+1,groups);group.pop()
  groups.append([names[index]]);yield from visit(index+1,groups);groups.pop()
 yield from visit(0,[])

def normalize(value,mapping):
 if isinstance(value,dict):
  if value.get('kind')=='subject':
   require(value['symbol'] in mapping,'undeclared_subject');return copy.deepcopy(mapping[value['symbol']])
  return {k:normalize(v,mapping) for k,v in value.items()}
 if isinstance(value,list):return [normalize(v,mapping) for v in value]
 return value

def enumerate_cases(declarations,template,premises=()):
 names=sorted(declarations);require(names and len(names)<=3,'subject_partition_bound')
 for name,d in declarations.items():
  require(d.get('kind')=='eoa','subject_must_be_top_level_account:'+name)
  require(isinstance(d.get('source'),dict),'subject_declaration_requires_source')
  require(isinstance(d.get('address'),str) and len(d['address'])==42 and int(d['address'],16)>=0,'subject_address')
 require(len({d['address'].lower() for d in declarations.values()})==len(names),'base_representatives_must_be_distinct')
 result=[]
 for groups in partitions(names):
  mapping={};accounts=[];reasons=[];unresolved=[]
  for group in groups:
   address=declarations[group[0]]['address'].lower();control={declarations[n].get('control','unspecified') for n in group}
   if len(control-{'unspecified'})>1:
    reasons.append({'reason':'incompatible_declared_controls','subjects':group,'declarations':[declarations[n] for n in group]})
   if 'unspecified' in control:unresolved.append({'reason':'control_not_declared','subjects':group})
   account={'kind':'account','address':address}
   for name in group:mapping[name]=account
   accounts.append({'identity':account,'members':group,'control':next(iter(control)) if len(control)==1 else 'conflict','sources':[declarations[n]['source'] for n in group]})
  normalized_premises=[]
  instance_addresses={str(n['address']).lower() for n in walk(template) if n.get('kind')=='contract_instance' and n.get('address')}
  collisions=instance_addresses & {v['address'] for v in mapping.values()}
  if collisions:reasons.append({'reason':'contract_address_cannot_be_top_level_EOA','addresses':sorted(collisions)})
  for premise in premises:
   require(premise.get('source'),'premise_requires_source')
   p=normalize(premise,mapping);op=p.get('operator');a=p.get('left');b=p.get('right')
   known=isinstance(a,dict) and isinstance(b,dict) and a.get('kind')==b.get('kind')=='account'
   truth=(a==b if op=='eq' else a!=b) if known and op in ['eq','ne'] else None
   normalized_premises.append({**p,'evaluated':truth})
   if truth is False:reasons.append({'reason':'declared_premise_false_after_merge','premise':p})
   elif truth is None:unresolved.append({'reason':'premise_unresolved','premise':p})
  result.append({'schema':SCHEMA,'id':'|'.join('='.join(g) for g in groups),'groups':groups,'mapping':mapping,'accounts':accounts,'premises':normalized_premises,'normalized':normalize(template,mapping),'status':'semantic_not_applicable' if reasons else 'relation_unresolved' if unresolved else 'applicable','reasons':reasons,'unresolved':unresolved,'evidence_strength':'declared_account_partition_only','execution_status':'not_executed','derivation':'canonical set partition; one EOA per equivalence class; re-evaluate declared premises and controls','input_sha256':digest({'declarations':declarations,'template':template,'premises':premises})})
 return result

def service_plan(case,template):
 """Normalize typed accounts before the v3 wire boundary; retain instance IDs."""
 require(case['status']=='applicable','non_applicable_partition')
 plan=normalize(copy.deepcopy(template),case['mapping'])
 def address(term):
  require(isinstance(term,dict) and term.get('kind')=='account','service_sender_requires_account')
  return term['address']
 for tx in plan['transactions']:
  tx['sender']=address(tx['sender'])
  tx['arguments']=[address(x) if isinstance(x,dict) and x.get('kind')=='account' else x for x in tx['arguments']]
 for ob in plan['observers']:
  ob['caller']=address(ob['caller'])
  ob['arguments']=[address(x) if isinstance(x,dict) and x.get('kind')=='account' else x for x in ob['arguments']]
 plan['accounts']=sorted(set([address(x) for x in plan['accounts']]))
 plan['id']=plan['id']+':'+case['id']
 from .multi_service import validate_plan
 validate_plan(plan);return plan
