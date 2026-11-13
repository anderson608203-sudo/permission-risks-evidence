"""C2 production static preparation: facts -> relations -> cases -> candidates.

No query instantiation, solver, backend execution, LLM, or safety classification.
"""
import copy
from .core import digest,require
from .facts import walk
from .bindings import BindingTrace,BindingAnalysis
from .relations import analyze_bindings,declining,generate_lifecycles
from .subjects import subject,enumerate_cases,normalize
from .static_roles import same_path_family
from .source_entry_identity import function_kind

SCHEMA='c2-static-candidate-set-v1'
PREP_VERSION='c2-static-v3'
STATIC_ALGORITHM='static-candidates-v1'

def derived_identity(bundle,native,policy):
 return {'prep_version':PREP_VERSION,'static_algorithm':STATIC_ALGORITHM,
         'program_id':bundle['program_id'],'build_id':bundle['build_id'],
         'bundle_sha256':digest(bundle),'native_sha256':digest(native),
         'policy_sha256':digest(policy),'policy_kind':(policy or {}).get('kind'),
         'policy_binding_sha256':((policy or {}).get('binding_source') or {}).get('sha256')}

def prepare(bundle,contract,native,declarations,policy=None,premises=(),lifecycle_records=()):
 iid=contract['file']+':'+contract['name']
 instances={iid:{'program':'input','file':contract['file'],'contract':contract['name'],'address':None,'scope':'static_declaration_instance_not_deployed'}}
 owner=BindingAnalysis({'input':bundle},instances,{'input':native} if native else None)
 lookup=BindingTrace(owner,iid,{'caller':subject('B')});entries=[];analyses={};inventory=[]
 for abi in contract['functions']:
  function=lookup.function(abi['signature'])
  source=lookup.anchor(function.get('generated_getter',function))
  identity={'function':abi['signature'],'selector':abi['selector'],'source':source,'program_id':bundle['program_id'],'build_id':bundle['build_id'],'instance_id':iid}
  if abi['readonly']:
   inventory.append({**identity,'disposition':'read_only_inventory','reason':'compiler-declared view/pure; no safety conclusion'});continue
  args=[{'kind':'parameter','declaration':lookup.declaration(p['id']),'compiler_type':typ} for p,typ in zip(function['parameters']['parameters'],abi['types'])]
  call={'instance_id':iid,'function':abi['signature'],'arguments':args,'caller':subject('B')}
  identifier=digest(identity)
  try:
   analysis=analyze_bindings({'input':bundle},instances,[call],{'input':native} if native else None,policy)
   require(analysis['schema']=='sourced-bindings-v2','binding_protocol_mismatch')
   frames=analysis['frames'];writes=[r for f in frames for r in f['relationships'] if r['operation']=='write'];external=[c for f in frames for c in f['external_calls']];unresolved=[u for f in frames for u in f['unresolved']]
  except (ValueError,KeyError,IndexError,TypeError,RecursionError) as error:
   analysis={'schema':'static-entry-unresolved-v1','entry':identity,'error_class':type(error).__name__,'error':str(error),'execution_confirmed':False};frames=[];writes=[];external=[];unresolved=[{'reason':'source_trace_incomplete','error_class':type(error).__name__,'error':str(error)}]
  # Native inventories supplement partial traces; they never fabricate a path,
  # resource key, policy scope, or concrete effect.
  native_sources=[{'source':f['source'],'writes':f['writes'],'native_sha256':digest(native)} for f in (native or {}).get('functions',[]) if f['source']['start']==source['start'] and f['source']['file'].replace('\\','/').endswith(source['file'])]
  fallback=bool(any(s['writes'] for s in native_sources))
  effects=[{'kind':'source_write','source':w['source'],'path':w['path'],'operator':w['operator'],'value':w['value'],'evidence_strength':w['corroboration']['status']} for w in writes]
  effects.extend({'kind':'external_call','source':c['source'],'dispatch':c['dispatch'],'target':c['target_expression'],'status':c['status'],'actual_effect':'unresolved_without_execution'} for c in external)
  if not effects and fallback:effects.append({'kind':'native_transitive_write_inventory','sources':native_sources,'keys_and_fields':'unresolved'})
  if not effects:unresolved.append({'reason':'no_effect_identified_in_supported_static_trace; entry retained'})
  links=[f['policy_link'] for f in frames if f.get('policy_link')];matched=any(p['status']=='effect_scope_associated' for p in links)
  guards=[g for f in frames for g in f['guards']]
  item={'id':identifier,'entry':identity,'status':'candidate_pending_checks' if effects and matched else 'lead_unresolved','sources':[{'kind':'independent_policy_and_effect','links':links}] if matched else [{'kind':'program_effect_or_entry_lead','reason':'specific policy/effect association unresolved'}],'effects':effects,'relations':[u for f in frames for u in f.get('key_uses',[])],'policy_associations':links or [{'status':'unlinked','reason':'no completed source relation'}],'guard_observation':{'status':'observed_conditions' if guards else 'not_identified_in_current_analysis','sources':[g['source'] for g in guards],'all_protection_absence_proven':False,'coverage':'supported source traversal only; unresolved edges retained'},'unresolved':unresolved+[{'reason':'role_unresolved','index_source':u.get('index_source')} for f in frames for u in f.get('key_uses',[]) if u['business_role']['status']=='unresolved'],'required_next_capabilities':['review_policy_and_role_scope','complete_unresolved_dataflow','reachable_deployment_and_initialization','bounded_path_search_if_authorized','original_program_verification_if_authorized'],'method_conclusion':None,'analysis_ref':{'id':identifier,'sha256':digest(analysis)},'execution_plan':None}
  entries.append(item);analyses[identifier]=analysis;inventory.append({**identity,'disposition':item['status'],'reason':'retained independent of lifecycle or guard availability'})
  item['caller']={'identity':subject('B'),'basis':'declared static A/B/C scenario; no reachable initialization asserted'}
 # Solidity receive/fallback entries have no ABI function selector. Keep them
 # visible as pending leads rather than silently omitting public entry points.
 scopes=set(lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']]))
 for f in lookup.fns.values():
  if f.get('scope') not in scopes or function_kind(f) not in ['fallback','receive','unresolved_kind']:continue
  identity={'function':function_kind(f),'original_kind':f.get('kind'),'selector':None,'source':lookup.anchor(f),'program_id':bundle['program_id'],'build_id':bundle['build_id'],'instance_id':iid};identifier=digest(identity)
  unresolved=[{'reason':'special_entry_without_ABI_static_adapter; source retained'}]
  analyses[identifier]={'schema':'static-entry-unresolved-v1','entry':identity,'unresolved':unresolved,'execution_confirmed':False}
  entries.append({'id':identifier,'entry':identity,'caller':{'identity':subject('B'),'basis':'declared static scenario'},'status':'lead_unresolved','sources':[{'kind':'compiler_special_public_entry'}],'effects':[],'relations':[],'policy_associations':[{'status':'unlinked'}],'guard_observation':{'status':'not_identified_in_current_analysis','sources':[],'all_protection_absence_proven':False,'coverage':'special entry adapter unresolved'},'unresolved':unresolved,'required_next_capabilities':['special_entry_source_adapter','policy_and_effect_binding'],'method_conclusion':None,'analysis_ref':{'id':identifier,'sha256':digest(analyses[identifier])},'execution_plan':None})
  inventory.append({**identity,'disposition':'lead_unresolved','reason':'special entry retained; unsupported adapter is not safety'})
 # Preserve lifecycle as an additive source, never an admission requirement.
 for item in entries:
  analysis=analyses[item['id']];guard_paths=[p for f in analysis.get('frames',[]) for g in f['guards'] for p in walk(g['condition']) if p.get('kind')=='storage_binding']
  for guarded in guard_paths:
   writers=[(other,e) for other in entries for e in other['effects'] if e['kind']=='source_write' and same_path_family(guarded,e['path'])]
   activations=[(o,e) for o,e in writers if e['value']=={'kind':'literal','value':True}]
   revocations=[(o,e) for o,e in writers if declining(e)]
   if activations and revocations:
    item['sources'].append({'kind':'lifecycle_storage_family','qualification_path':guarded,'activation_sources':[{'entry':o['entry'],'effect_source':e['source']} for o,e in activations],'revocation_sources':[{'entry':o['entry'],'effect_source':e['source']} for o,e in revocations],'same_key_lifecycle':'unresolved; storage family alone is insufficient','basis':'same qualified declaration/instance/fields; existing C1 declining-write predicate reused'})
 # Existing C1 proposal/lifecycle normalizer remains available as another source.
 # The caller supplies only source proposals, never historical verdicts or Gold.
 legacy=[]
 for record in lifecycle_records:
  try:
   for result in generate_lifecycles(record,bundle,contract):legacy.append({'source':'C1_lifecycle_normalizer','raw_record_ref':result['raw_record_ref'],'transactions':result['transactions'],'observers':result['observers'],'normalization':result['normalization'],'status':'static_plan_source_not_executed'})
  except (ValueError,KeyError,IndexError,TypeError) as error:legacy.append({'source':'C1_lifecycle_normalizer','status':'unresolved','reason':str(error)})
 for item in entries:
  item['sources'].extend({'kind':'C1_lifecycle_normalized_proposal','record':r} for r in legacy if any(t.get('function')==item['entry']['function'] for t in r.get('transactions',[])))
 # Cases consume all source relations and candidate effects; no contradictory
 # distinct-account condition is retained after normalization.
 cases=enumerate_cases(declarations,{'candidates':entries,'legacy_lifecycle_sources':legacy},premises)
 normalized=[]
 for case in cases:
  records=[]
  for item in case['normalized']['candidates']:
   records.append({**item,'alias_case_id':case['id'],'case_applicability':{'status':case['status'],'reasons':case['reasons'],'unresolved':case['unresolved']},'case_candidate_status':'semantic_not_applicable' if case['status']=='semantic_not_applicable' else 'lead_unresolved' if case['status']=='relation_unresolved' else item['status']})
  normalized.append({'case':{k:v for k,v in case.items() if k!='normalized'},'candidates':records})
 return {'schema':SCHEMA,'derived_identity':derived_identity(bundle,native,policy),'input':{'program_id':bundle['program_id'],'build_id':bundle['build_id'],'contract_file':contract['file'],'contract_name':contract['name'],'native_sha256':digest(native) if native else None},'entry_inventory':inventory,'source_analyses':analyses,'alias_cases':normalized,'legacy_lifecycle_sources':legacy,'admission':'static preparation only; no frozen execution/query plans','counts':{'entries_in_inventory':len(inventory),'retained_nonview_entries':len(entries),'alias_cases':len(cases),'risk_queries':0,'transactions':0,'LLM_calls':0},'method_conclusion':None,'execution_confirmed':False}
