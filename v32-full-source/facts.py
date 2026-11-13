"""M1 compiler facts. No role inference by project, function or variable names."""
import hashlib,json,pathlib
from .core import digest,require
from .source_entry_identity import function_mutability

def canonical_abi_type(item):
 typ=item['type']
 return '('+','.join(canonical_abi_type(c) for c in item['components'])+')'+typ[5:] if typ.startswith('tuple') else typ

def walk(node):
 if isinstance(node,dict):
  yield node
  for v in node.values():yield from walk(v)
 elif isinstance(node,list):
  for v in node:yield from walk(v)

def build_bundle(group,standard_input,standard_output,original_output,receipt):
 require(not [e for e in standard_output.get('errors',[]) if e['severity']=='error'],'compile_error')
 sources={k:v['content'] for k,v in standard_input['sources'].items()}
 sid={v['id']:k for k,v in standard_output['sources'].items()}
 def anchor(src):
  start,length,fid=map(int,src.split(':'));file=sid.get(fid)
  return {'file':file,'start':start,'length':length,'sha256':hashlib.sha256(sources[file].encode()).hexdigest() if file else None}
 def snippet(a):
  return sources[a['file']].encode()[a['start']:a['start']+a['length']].decode('utf-8') if a['file'] else ''
 nodes={n['id']:n for s in standard_output['sources'].values() for n in walk(s['ast']) if 'id' in n}
 state={i for i,n in nodes.items() if n.get('nodeType')=='VariableDeclaration' and n.get('stateVariable')}
 functions=[];edges=[]
 for i,n in nodes.items():
  if n.get('nodeType') not in ('FunctionDefinition','ModifierDefinition'):continue
  a=anchor(n['src']);body=n.get('body')
  refs={x['referencedDeclaration'] for x in walk(body) if isinstance(x.get('referencedDeclaration'),int)}
  calls=[];conditions=[];writes=set()
  for x in walk(body):
   kind=x.get('nodeType')
   if kind=='FunctionCall':
    expr=x.get('expression',{});target=expr.get('referencedDeclaration');calls.append({'target_ast_id':target,'anchor':anchor(x['src']),'kind':x.get('kind')})
    if target in nodes:edges.append({'from':i,'to':target,'relation':'calls'})
    if expr.get('name') in ('require','assert'):conditions.append(anchor(x['src']))
   if kind in ('IfStatement','Conditional'):conditions.append(anchor(x['condition']['src']))
   if kind in ('Assignment','UnaryOperation'):
    subtree=x.get('leftHandSide',x.get('subExpression',{}))
    writes.update(y.get('referencedDeclaration') for y in walk(subtree) if y.get('referencedDeclaration') in state)
  for d in sorted(refs&state):edges.append({'from':i,'to':d,'relation':'references_state'})
  functions.append({'ast_id':i,'name':n.get('name'),'kind':n.get('kind',n['nodeType']),'visibility':n.get('visibility'),'mutability':n.get('stateMutability'),'selector':n.get('functionSelector'),'implemented':body is not None,'parameters':[{'name':p['name'],'type':p['typeDescriptions']['typeString'],'ast_id':p['id']} for p in n.get('parameters',{}).get('parameters',[])],'modifiers':[m['modifierName'].get('referencedDeclaration') for m in n.get('modifiers',[])],'state_references':sorted(refs&state),'syntactic_writes':sorted(writes),'calls':calls,'conditions':conditions,'source_anchor':a,'source':snippet(a),'unresolved_items':['ast_references_not_effect_proof']})
 contracts=[]
 for file,items in standard_output['contracts'].items():
  for name,c in items.items():
   old=original_output['contracts'][file][name]
   equal={field:c[field]==old[field] for field in ['abi']}
   for typ in ['bytecode','deployedBytecode']:
    equal[typ]=c['evm'][typ]['object']==old['evm'][typ]['object']
   require(all(equal.values()),'old_build_mismatch')
   if not c['evm']['bytecode']['object']:continue
   functions_abi=[]
   for f in c['abi']:
    if f['type']!='function':continue
    signature=f['name']+'('+','.join(canonical_abi_type(a) for a in f['inputs'])+')'
    selector=c['evm']['methodIdentifiers'].get(signature)
    require(selector is not None,'missing_selector')
    mutability=function_mutability(f)
    require(mutability is not None,'abi_function_mutability_unresolved')
    functions_abi.append({'signature':signature,'types':[a['type'] for a in f['inputs']],'selector':selector,'readonly':mutability in ['view','pure'],'outputs':[a['type'] for a in f['outputs']]})
   constructor=next((f for f in c['abi'] if f['type']=='constructor'),{'inputs':[]})
   contracts.append({'file':file,'name':name,'abi':c['abi'],'functions':functions_abi,'constructor_types':[a['type'] for a in constructor['inputs']],'creation':c['evm']['bytecode']['object'],'runtime':c['evm']['deployedBytecode']['object'],'immutable_references':c['evm']['deployedBytecode'].get('immutableReferences',{}),'creation_link_references':c['evm']['bytecode'].get('linkReferences',{}),'runtime_link_references':c['evm']['deployedBytecode'].get('linkReferences',{}),'storage_layout':c.get('storageLayout'),'metadata':json.loads(c['metadata']),'matches_frozen':equal})
 program_id=digest({k:hashlib.sha256(v.encode()).hexdigest() for k,v in sources.items()})
 bundle={'id':group,'program_id':program_id,'build_id':digest({'input':standard_input,'compiler':receipt['compiler_binary_sha256']}),'development_identity':'overlap_unverified','source_kind':'new_original_solc_ast','compiler':receipt,'functions':functions,'state_declarations':[{'ast_id':i,'name':nodes[i]['name'],'type':nodes[i]['typeDescriptions']['typeString'],'source_anchor':anchor(nodes[i]['src'])} for i in sorted(state)],'edges':edges,'contracts':contracts,'coverage':{'all_function_declarations':len(functions),'all_public_external_entries_enumerated':True,'slither_fresh':'not_executed_missing_matching_runtime','unresolved':['syntactic_writes_are_not_transitive_effect_proof','dynamic_calls_not_resolved_by_ast_alone']}}
 return bundle
