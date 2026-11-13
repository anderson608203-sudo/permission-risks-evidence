"""Scoped policy references and program provenance, never ABI-type heuristics."""
import re
from .facts import walk
from .core import digest,require

def documentation(node):
 d=node.get('documentation',{})
 return d.get('text','') if isinstance(d,dict) else str(d or '')

def declaration_key(declaration):
 s=declaration['source'];return (s['program_id'],s['build_id'],declaration['ast_id'])

def same_path_family(a,b):
 return (a['program_id'],a['build_id'],a['instance_id'],declaration_key(a['declaration']),[s['field']['ast_id'] for s in a['segments'] if 'field' in s])==(b['program_id'],b['build_id'],b['instance_id'],declaration_key(b['declaration']),[s['field']['ast_id'] for s in b['segments'] if 'field' in s])

def associate_roles(result,bundles,instances,policy=None):
 if policy:require(policy.get('source') and policy.get('text'),'neutral_policy_source_required')
 result['policy_context']=({**policy,'sha256':digest(policy),'status':'context_only_until_scoped_link'} if policy else {'status':'not_supplied'})
 result['policy_links']=[]
 for frame in result['frames']:
  spec=instances[frame['frame']['instance_id']];bundle=bundles[spec['program']]
  nodes={n['id']:n for ast in bundle['ast_sources'].values() for n in walk(ast) if 'id' in n}
  entry=nodes[frame['entry']['source']['ast_id']];params={p['name']:p for p in entry.get('parameters',{}).get('parameters',[])}
  doc=documentation(entry);role_claims={};effect_ids=set();policy_sources=[];gaps=[]
  # These are explicit source-authored neutral statements, not interpretations
  # of identifiers. Their selectors are resolved in the documented declaration.
  for parameter,role in re.findall(r'@custom:pr-role\s+(\w+)\s+(principal|principal_id|resource)\b',doc):
   if parameter not in params:gaps.append('annotation_parameter_not_resolved:'+parameter);continue
   role_claims.setdefault(params[parameter]['id'],[]).append({'role':role,'basis':'source_authored_parameter_role_annotation','source':frame['entry']['source'],'documentation':doc,'parameter_ast_id':params[parameter]['id']})
  contract=next(n for n in nodes.values() if n.get('nodeType')=='ContractDefinition' and n.get('name')==spec['contract'] and int(n['src'].split(':')[-1])==int(bundle['ast_sources'][spec['file']]['src'].split(':')[-1]))
  scopes=set(contract.get('linearizedBaseContracts',[contract['id']]))
  states=[n for n in nodes.values() if n.get('stateVariable') and n.get('scope') in scopes]
  def state_named(name):
   matches=[n for n in states if n['name']==name]
   return matches[0] if len(matches)==1 else None
  for target in re.findall(r'@custom:pr-effect\s+(\w+)\b',doc):
   state=state_named(target)
   if state:effect_ids.add(state['id']);policy_sources.append({'kind':'source_authored_effect_scope','source':frame['entry']['source'],'documentation':doc,'state_ast_id':state['id']})
   else:gaps.append('annotation_effect_not_unique:'+target)
  scoped=bool(policy and any(s.get('program_id')==bundle['program_id'] and s.get('build_id')==bundle['build_id'] and s.get('contract_file')==spec['file'] and s.get('contract_name')==spec['contract'] and s.get('basis') for s in policy.get('applies_to',[])))
  if policy and not scoped:gaps.append('policy_not_scoped_to_this_program_and_contract')
  text=policy['text'] if scoped else '';authority_ids=[];resource_parameter=None
  # Small documented grammar. Unrecognized text remains an unlinked policy,
  # and identifier references must resolve uniquely within this program scope.
  typed=policy.get('typed_relations') if scoped else None
  if typed:
   authority=state_named(typed.get('authority_state','')) if typed.get('authority_state') else None
   target=state_named(typed.get('effect_state','')) if typed.get('effect_state') else None
   if authority and target and not typed.get('resource_parameter'):
    effect_ids.add(target['id']);authority_ids.append(authority['id']);policy_sources.append({'kind':'explicit_policy_state_references','policy_source':policy['source'],'policy_sha256':digest(policy),'authority_ast_id':authority['id'],'effect_ast_id':target['id'],'basis':'typed_policy_relation'})
   elif target and not typed.get('resource_parameter'):
    effect_ids.add(target['id']);policy_sources.append({'kind':'explicit_policy_state_references','policy_source':policy['source'],'policy_sha256':digest(policy),'effect_ast_id':target['id'],'basis':'typed_policy_relation'})
   elif target:
    policy_sources.append({'kind':'typed_policy_effect_reference','policy_source':policy['source'],'policy_sha256':digest(policy),'effect_ast_id':target['id'],'basis':'resource_policy_effect_reference'})
   if typed.get('resource_parameter'):
    resource_parameter=params.get(typed['resource_parameter'])
    if resource_parameter:role_claims.setdefault(resource_parameter['id'],[]).append({'role':'resource','basis':'explicit_policy_parameter_reference','policy_source':policy['source'],'policy_sha256':digest(policy),'parameter_ast_id':resource_parameter['id'],'matched_text':None,'typed_relation':True})
    else:gaps.append('typed_policy_resource_not_in_this_entry')
   if typed.get('qualification_state'):
    qualification=state_named(typed['qualification_state'])
    if qualification:policy_sources.append({'kind':'typed_policy_qualification_reference','policy_source':policy['source'],'policy_sha256':digest(policy),'qualification_ast_id':qualification['id']})
    else:gaps.append('typed_policy_qualification_not_unique_in_this_contract')
  else:
   match=re.fullmatch(r'Only (\w+) may change (\w+);.*',text)
   if match:
    authority=state_named(match[1]);target=state_named(match[2])
    if authority and target:
     effect_ids.add(target['id']);authority_ids.append(authority['id']);policy_sources.append({'kind':'explicit_policy_state_references','policy_source':policy['source'],'policy_sha256':digest(policy),'authority_ast_id':authority['id'],'effect_ast_id':target['id'],'matched_text':match[0]})
    else:gaps.append('policy_state_references_not_unique_in_this_contract')
   match=re.fullmatch(r'Only caller with permission for exactly (\w+) may write \1; no delegation\. (\w+) is an untrusted input\.',text)
   if match:
    resource_parameter=params.get(match[1])
    if resource_parameter:
     role_claims.setdefault(resource_parameter['id'],[]).append({'role':'resource','basis':'explicit_policy_parameter_reference','policy_source':policy['source'],'policy_sha256':digest(policy),'parameter_ast_id':resource_parameter['id'],'matched_text':match[0]})
    else:gaps.append('policy_resource_reference_not_in_this_entry')
    if match[2] in params:gaps.append('untrusted_parameter_is_not_proof_of_credential_holder_role')
  uses=[]
  for path in walk(frame):
   if path.get('kind')!='storage_binding':continue
   for segment in path['segments']:
    if 'key' not in segment:continue
    evidence=[]
    for origin in segment.get('origins',[]):
     if origin.get('kind')=='frame_caller':evidence.append({'role':'principal','basis':'program_frame_caller_origin','source':origin['source']})
     if origin.get('kind')=='parameter':
      for claim in role_claims.get(origin['declaration']['ast_id'],[]):evidence.append({**claim,'parameter_declaration':origin['declaration'],'flow_origins':segment['origins']})
    roles={e['role'] for e in evidence}
    status='associated' if len(roles)==1 else 'unresolved'
    segment['business_role']={'status':status,'role':next(iter(roles)) if len(roles)==1 else None,'evidence':evidence,'reasons':[] if status=='associated' else ['conflicting_role_evidence' if evidence else 'no_scoped_policy_or_program_role_evidence'],'not_an_authorization_proof':True}
    uses.append({'storage_declaration':path['declaration'],'instance_id':path['instance_id'],'field_ids':[s['field']['ast_id'] for s in path['segments'] if 'field' in s],'key':segment['key'],'compiler_key_type':segment['compiler_key_type'],'index_source':segment.get('index_source'),'origins':segment.get('origins',[]),'business_role':segment['business_role']})
  writes=[r for r in frame['relationships'] if r['operation']=='write']
  matched=[]
  for write in writes:
   by_target=write['path']['declaration']['ast_id'] in effect_ids
   resource_in=lambda p:resource_parameter and any(o.get('kind')=='parameter' and o['declaration']['ast_id']==resource_parameter['id'] for s in p['segments'] for o in s.get('origins',[]))
   correspondences=[{'guard_source':g['source'],'path':p} for g in frame['guards'] for p in walk(g['condition']) if p.get('kind')=='storage_binding' and p['declaration']['ast_id']!=write['path']['declaration']['ast_id'] and resource_in(p)]
   by_resource=resource_in(write['path']) and bool(correspondences)
   if by_target or by_resource:matched.append({'effect_source':write['source'],'path':write['path'],'basis':'explicit_policy_effect_declaration' if by_target else 'explicit_policy_resource_parameter_in_guard_and_different_written_object','usage_correspondences':correspondences,'business_authorization':'not_proven'})
  if resource_parameter and not matched:gaps.append('resource_reference_alone_does_not_identify_a_policy_governed_effect')
  guard_links=[]
  for guard in frame['guards']:
   paths=[p for p in walk(guard['condition']) if p.get('kind')=='storage_binding']
   relevant=[p for p in paths if p['declaration']['ast_id'] in authority_ids or (resource_parameter and any(o.get('kind')=='parameter' and o['declaration']['ast_id']==resource_parameter['id'] for s in p['segments'] for o in s.get('origins',[])))]
   guard_links.append({'source':guard['source'],'status':'source_reference_correspondence' if relevant and matched else 'policy_association_unresolved','matched_paths':relevant if matched else [],'reason':None if relevant and matched else 'policy_text_does_not_establish_this_guard_effect_association','authorization_sufficiency':'not_proven'})
  frame['key_uses']=list({digest(u):u for u in uses}.values())
  link={'frame_id':frame['frame']['id'],'status':'effect_scope_associated' if matched else 'unlinked','effect_matches':matched,'sources':policy_sources+([{'kind':'explicit_resource_policy','source':policy['source'],'sha256':digest(policy)}] if resource_parameter else []),'guards':guard_links,'unresolved':gaps+([] if matched else ['no_specific_policy_effect_correspondence']),'execution_confirmed':False,'permission_validity':'not_proven'}
  result['policy_links'].append(link);frame['policy_link']=link
