"""M2 source proposals -> key-aware plans -> separately instantiated R2 rules."""
import copy
from .core import *
from .source_paths import SourcePaths,compatible,paths_in
from .relations import generate_lifecycles,observer_paths,declining,financial_binding
from .policies import management_policy,allowed_expression,key_requirements
from . import SCHEMA_VERSION

def all_of(*items):
 items=[x for x in items if x is not None]
 return lit('Bool',True) if not items else items[0] if len(items)==1 else operator('and','Bool',*items)
def negate(x):return operator('not','Bool',x)
def changed(spec,step):
 return operator('ne','Bool',obs(spec['id']+'.'+str(step),spec['type']),obs(spec['id']+'.'+str(step-1),spec['type']))
def protected_effect(candidate,step):
 specs=[o for o in candidate['plan']['observers'] if o['id'] in ['effect','balance','supply']]
 if candidate['financial']['applicable']:
  return all_of(*[operator('int_gt','Bool',delta(obs(o['id']+'.'+str(step),o['type']),obs(o['id']+'.'+str(step-1),o['type'])),lit('IntDelta',0)) for o in specs if o['id'] in ['balance','supply']])
 return all_of(*[changed(o,step) for o in specs])

def construct_candidates(record,bundle,contract,actors):
 # The current finite generator expands distinct role bindings only. Detect
 # aliases by address before inference; never treat different labels as proof
 # of distinct people or conflicting control rights. The engine itself retains
 # equal-address account unification and SourcePaths accepts explicit aliases.
 classes={}
 for name,a in actors.items():classes.setdefault(a['address'].lower(),[]).append(name)
 require(all(len(names)==1 for names in classes.values()),'unresolved_actor_alias_case_requires_separate_canonical_binding')
 tracer=SourcePaths(bundle,contract);answers=[]
 for case_no,case in enumerate(generate_lifecycles(record,bundle,contract)):
  txs=case['transactions'];observers=case['observers'];q=observers[0];qp,qt=observer_paths(tracer,q)
  traces=[tracer.trace(t['function'],t['arguments'],'$'+t['sender']) for t in txs]
  require(all(t['native_agreement'] for t in traces),'native_disagreement')
  grant=[];revoke=[];use=[]
  eps=[p for o in observers[1:] for p in observer_paths(tracer,o)[0]]
  for i,(tx,t) in enumerate(zip(txs,traces),1):
   relevant=[w for w in t['writes'] if any(compatible(w['path'],p) for p in qp)]
   if i>1 and tx['sender']=='A' and relevant:
    (revoke if all(declining(w) for w in relevant) else grant).append(i)
   if tx['sender']=='B' and any(compatible(w['path'],p) for w in t['writes'] for p in eps):
    guards=[p for g in t['guards'] for p in paths_in(g['condition'])]
    require(any(compatible(a,b) for a in guards for b in qp),'sensitive_action_not_bound_to_same_subject_credential')
    use.append(i)
  bindings=[(g,u,r,p) for g in grant for u in use for r in revoke for p in use if g<u<r<p]
  require(len(bindings)==1,'ambiguous_lifecycle_order_finite_split_required')
  g,u,r,p=bindings[0]
  require(txs[u-1]['function']==txs[p-1]['function'],'post_revoke_different_action_class')
  require(all(not any(compatible(w['path'],qpath) for w in t['writes'] for qpath in qp) for t in traces[r:p-1]),'intervening_regrant_not_excluded')
  policy=management_policy(tracer,txs,q,g)
  policy['independent_lifecycle_sources']={'grant':traces[g-1]['entry'],'revoke':traces[r-1]['entry'],'protected_effect':traces[u-1]['entry'],'original_documentation':[{'source':tracer.anchor(n),'documentation':n['documentation']} for n in tracer.nodes.values() if n.get('documentation') and n.get('id') in {traces[g-1]['entry']['ast_id'],traces[r-1]['entry']['ast_id'],traces[u-1]['entry']['ast_id']}]}
  observers=observers+[{k:v for k,v in o.items() if k!='source'} for o in policy['observers']]
  finance=financial_binding(tracer,txs,observers,u)
  base_id=bundle['id']+':completion:'+digest({'record':case['raw_record_ref'],'plan':txs})[:12]
  state=all_of(negate(obs('qualified.'+str(g-1),'Bool')),obs('qualified.'+str(g),'Bool'))
  proposal={'schema_version':SCHEMA_VERSION,'id':base_id+':proposal','revision':record.get('candidate_revision',0),'program_id':bundle['program_id'],'build_id':bundle['build_id'],'target_refs':[str(traces[u-1]['entry']['ast_id'])],'actors':[{'symbol':k,'kind':v['kind'],'control':v['control'],'identity_ref':v['address'],'evidence_refs':[]} for k,v in actors.items()],'guard_claims':[],'state_claims':[state],'assumptions':[],'evidence_refs':[{'artifact':ref(bundle),'locator':'native_ir and ast_sources','origin':'compiler'}],'transaction_plan_refs':[],'unresolved_items':['other inputs, amounts, sequences, delegated signatures and symbolic EVM paths not covered']}
  common={'input_id':bundle['id'],'source_bundle_sha256':digest(bundle),'contract_file':contract['file'],'contract_name':contract['name'],'proposal':proposal,'policy':policy,'financial':finance,'source_relation':{'qualification_state_ids':sorted({x['root'] for x in qp}),'financial_observer_state_ids':[[p['root'] for p in observer_paths(tracer,o)[0]] for o in observers if o['id'] in ['balance','supply']]},'source_binding_repairs':case['normalization'],'generation':case['generation'],'source_certificate':{'native_ir_ref':bundle['native_ir']['sha256'],'qualifier':qt,'lifecycle_traces':traces,'qualification_paths':qp,'protected_effect_paths':eps,'policy':policy,'financial':finance,'raw_proposal_ref':case['raw_record_ref'],'binding_order':'before_execution','llm_step_indexes_trusted':False},'automatic_scope_gaps':['finite concrete plans; not symbolic search']}
  plan={'id':base_id+':lifecycle','actors':copy.deepcopy(actors),'transactions':txs,'observers':observers}
  lifecycle={**copy.deepcopy(common),'id':plan['id'],'group':plan['id'],'track':'automatic_lifecycle','plan':plan,'grant_step':g,'effect_step':u,'revoke_step':r,'post_step':p,'relation':{'before_step':g-1,'after_step':g},'relation_expression':state}
  lifecycle['proposal']['transaction_plan_refs']=[ref(plan)];answers.append(lifecycle)
  # Finite mutation of the same source-bound management operation. It tests the
  # controlled caller BEFORE any honest grant, then actual downstream use.
  bad=copy.deepcopy(txs[:g]);bad[-1].update(sender='B',environment_prefix=False);bad.append(copy.deepcopy(txs[u-1]))
  badplan={**copy.deepcopy(plan),'id':base_id+':unauthorized_management','transactions':bad}
  unauthorized={**copy.deepcopy(common),'id':badplan['id'],'group':badplan['id'],'track':'automatic_unauthorized_management','plan':badplan,'grant_step':g,'effect_step':g+1,'relation':{'before_step':g-1,'after_step':g},'relation_expression':state}
  unauthorized['proposal']['transaction_plan_refs']=[ref(badplan)];answers.append(unauthorized)
 return answers

def prepare_static_candidates(bundle,contract,native,actors,policy=None,premises=(),lifecycle_records=()):
 """C2 static production entry; never enters instantiate_queries or a backend."""
 from .static_candidates import prepare
 return prepare(bundle,contract,native,actors,policy,premises,lifecycle_records)

def instantiate_queries(c):
 if 'control_queries' in c:return c['control_queries']
 g=c['grant_step'];u=c['effect_step'];actors=c['plan']['actors'];policy=c['policy']
 initial=all_of(*[obs('tx'+str(i)+'.success','Bool') for i in range(1,g)],*key_requirements(policy,g-1))
 effect=protected_effect(c,u);queries=[]
 def add(rule,premise,expr,allowed,checks,form='EXISTS_VIOLATION'):
  queries.append({'rule':rule,'query_form':form,'premise':premise,'expression':expr,'allowed':allowed,'required_rule_checks':checks,'applicability':'source_bound_before_execution'})
 if c['track']=='automatic_unauthorized_management':
  management_allowed=allowed_expression(policy,g-1,actors)
  add('AC-02',initial,all_of(lit('Bool',actors['B']['control']!='honest_environment'),negate(management_allowed),negate(obs('qualified.'+str(g-1),'Bool')),obs('tx'+str(g)+'.success','Bool'),obs('qualified.'+str(g),'Bool'),obs('tx'+str(u)+'.success','Bool'),effect),management_allowed,['independent management policy','controlled subject B','pre-state manager qualification','same-key real qualification change','ordered illegal acquisition and downstream protected effect','honest grant excluded'])
  allowed=obs('qualified.'+str(u-1),'Bool')
  add('AC-01',initial,all_of(negate(allowed),obs('tx'+str(u)+'.success','Bool'),effect),allowed,['independent policy basis','same B credential and protected resource','policy forbids B','successful original transaction','committed protected effect'])
 else:
  r=c['revoke_step'];p=c['post_step'];prefix=all_of(initial,obs('tx'+str(g)+'.success','Bool'))
  claim=all_of(c['relation_expression'],obs('qualified.'+str(u-1),'Bool'),obs('tx'+str(u)+'.success','Bool'),effect,obs('tx'+str(r)+'.success','Bool'),negate(obs('qualified.'+str(r),'Bool')))
  add('relation',prefix,negate(claim),lit('Bool',True),['same-subject qualification','guarded sensitive effect','source-bound revocation'],'CHECK_IMPLICATION')
  lifecycle=all_of(prefix,obs('qualified.'+str(u-1),'Bool'),obs('tx'+str(u)+'.success','Bool'),effect,obs('tx'+str(r)+'.success','Bool'),negate(obs('qualified.'+str(r),'Bool')))
  add('AC-04',lifecycle,all_of(negate(obs('qualified.'+str(p-1),'Bool')),obs('tx'+str(p)+'.success','Bool'),protected_effect(c,p)),obs('qualified.'+str(p-1),'Bool'),['same subject and credential keys','legitimate prior activation and sensitive use','successful original revocation','no intervening legal regrant','later accepted call and actual protected effect'])
  if c['financial']['applicable']:
   add('FCR-MINT',prefix,all_of(obs('qualified.'+str(u-1),'Bool'),obs('tx'+str(u)+'.success','Bool'),effect),lit('Bool',True),['source-backed privilege and management','spendable holder-resource and supply binding','same sourced quantity creation rather than transfer','actual positive mathematical deltas','full deployment replay'])
 return queries

def normal_transfer_control(base):
 """Finite ordinary-holder transfer derived from the source financial binding."""
 require(base['financial']['applicable'],'no_financial_resource')
 c=copy.deepcopy(base);u=c['effect_step'];plan=c['plan']
 balance=next(o for o in plan['observers'] if o['id']=='balance')
 require(len(balance['arguments'])==1 and balance['arguments'][0].startswith('$'),'transfer_control_holder')
 holder=balance['arguments'][0][1:];recipient='B';require(holder!=recipient,'control_transfer_distinct_recipient')
 source=sorted(c['financial']['spendability_and_transfer_sources'],key=digest)[0]
 plan['transactions']=plan['transactions'][:u]+[{'sender':holder,'function':source['function'],'arguments':['$'+recipient,'1'],'environment_prefix':True}]
 require(len(plan['transactions'])<=6,'control_transaction_bound')
 plan['observers'].append({**balance,'id':'recipient','arguments':['$'+recipient]})
 c['id']+=':ordinary-transfer';c['group']=c['id'];c['track']='original_normal_behavior_control';plan['id']=c['id'];step=u+1
 claim=all_of(obs('tx'+str(step)+'.success','Bool'),operator('eq','Bool',obs('supply.'+str(step)),obs('supply.'+str(step-1))),operator('eq','Bool',delta(obs('balance.'+str(step)),obs('balance.'+str(step-1))),lit('IntDelta',-1)),operator('eq','Bool',delta(obs('recipient.'+str(step)),obs('recipient.'+str(step-1))),lit('IntDelta',1)))
 c['control_queries']=[{'rule':'original-normal-transfer-control','query_form':'CHECK_IMPLICATION','premise':all_of(*[obs('tx'+str(i)+'.success','Bool') for i in range(1,step)]),'expression':negate(claim)}]
 c['source_certificate']['control_derivation']={'kind':'ordinary holder consent via direct sender','source_transfer':source,'holder':holder,'recipient':recipient,'amount':'1','no_research_positive_or_negative_from_control':True}
 return c
def bind_subject_cases(declarations,template,premises=()):
 """Normalize declared actors and resource terms without generating queries."""
 from .subjects import enumerate_cases
 return enumerate_cases(declarations,template,premises)

