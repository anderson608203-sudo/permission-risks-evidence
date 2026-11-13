"""Source-qualified static relationships. No feasibility, risk or safety verdicts."""
import copy
from .core import require,digest
from .facts import walk
from .source_paths import SourcePaths,paths_in,stable

SCHEMA='sourced-bindings-v2'

class BindingTrace(SourcePaths):
 def __init__(self,owner,instance,frame):
  spec=owner.instances[instance];bundle=owner.bundles[spec['program']]
  contract=next(c for c in bundle['contracts'] if (c['file'],c['name'])==(spec['file'],spec['contract']))
  super().__init__(bundle,contract)
  self.owner=owner;self.instance=instance;self.frame=frame;self.occurrences=[];self.external=[]
 def anchor(self,node):
  a=super().anchor(node)
  hashes={x['source_anchor']['file']:x['source_anchor']['sha256'] for x in self.bundle['functions']}
  return {**a,'source_sha256':hashes.get(a['file']),'program_id':self.bundle['program_id'],'build_id':self.bundle['build_id']}
 def declaration(self,ast_id):
  n=self.nodes.get(ast_id)
  if not n:return {'unresolved':'declaration_not_loaded','ast_id':ast_id}
  return {'ast_id':ast_id,'name':n.get('name'),'type':n.get('typeDescriptions',{}).get('typeString'),'source':self.anchor(n)}
 def origins(self,node,seen=()):
  """Compiler/dataflow provenance, without a type-to-business-role rule."""
  if not node:return [{'kind':'unresolved_origin','reason':'missing_expression'}]
  k=node.get('nodeType');rd=node.get('referencedDeclaration')
  if k in ['Identifier','IdentifierPath']:
   declaration=self.decls.get(rd)
   if declaration:
    parameters={p['id'] for f in self.fns.values() for p in f.get('parameters',{}).get('parameters',[])}
    if rd in parameters or declaration.get('stateVariable'):
     if rd in parameters and any((x.get('nodeType')=='Assignment' and x.get('leftHandSide',{}).get('referencedDeclaration')==rd) or (x.get('nodeType')=='UnaryOperation' and x.get('operator') in ['++','--','delete'] and x.get('subExpression',{}).get('referencedDeclaration')==rd) for x in self.nodes.values()):
      return [{'kind':'unresolved_origin','source':self.anchor(node),'declaration':self.declaration(rd),'reason':'parameter_reassigned; flow_sensitive_origin_not_implemented'}]
     return [{'kind':'parameter' if rd in parameters else 'state_declaration','declaration':self.declaration(rd),'use_source':self.anchor(node)}]
    definitions=[]
    for item in self.nodes.values():
     if item.get('nodeType')=='VariableDeclarationStatement' and any(d and d['id']==rd for d in item.get('declarations',[])) and item.get('initialValue'):definitions.append((item,item['initialValue']))
     if item.get('nodeType')=='Assignment' and item.get('leftHandSide',{}).get('referencedDeclaration')==rd:definitions.append((item,item['rightHandSide']))
    if rd not in seen and len(definitions)==1:
     defining,expression=definitions[0]
     return self.origins(expression,seen+(rd,))+[{'kind':'single_definition_flow','declaration':self.declaration(rd),'definition_source':self.anchor(defining),'use_source':self.anchor(node),'limit':'source dependency, not reachability'}]
   return [{'kind':'unresolved_origin','source':self.anchor(node),'reason':'no_unique_parameter_or_definition'}]
  if k=='MemberAccess' and node['expression'].get('name')=='msg' and node['memberName']=='sender':
   return [{'kind':'frame_caller','source':self.anchor(node),'identity':self.frame['caller']}]
  if k=='FunctionCall' and node.get('kind')=='typeConversion':
   return [{'kind':'conversion_origin','source':self.anchor(node),'inputs':[self.origins(x,seen) for x in node.get('arguments',[])],'reason':'conversion_does_not_by_itself_prove_identity_preservation'}]
  return [{'kind':'expression_origin','source':self.anchor(node),'expression_kind':k,'reason':'business_role_not_inferred_from_expression_type'}]
 def qualify(self,value):
  if isinstance(value,list):return [self.qualify(v) for v in value]
  if not isinstance(value,dict):return value
  if value.get('kind')=='storage':
   declaration=self.declaration(value['root']);typ=self.nodes[value['root']].get('typeName',{});segments=[]
   for segment in value['segments']:
    if 'key' in segment:
     keytype=typ.get('keyType',{}).get('typeDescriptions',{}).get('typeString')
     segments.append({'key':self.qualify(segment['key']),'compiler_key_type':keytype,'index_source':segment.get('index_source'),'origins':segment.get('origins',[]),'business_role':{'status':'unresolved','role':None,'reasons':['no_business_role_evidence_evaluated']}})
     typ=typ.get('valueType',{})
    else:
     field=self.declaration(segment.get('field'));segments.append({'field':field});typ=self.nodes.get(segment.get('field'),{}).get('typeName',{})
   return {'kind':'storage_binding','program_id':self.bundle['program_id'],'build_id':self.bundle['build_id'],'instance_id':self.instance,'instance_address':self.owner.instances[self.instance].get('address'),'declaration':declaration,'segments':segments}
  return {k:self.qualify(v) for k,v in value.items()}
 def value(self,n,env):
  v=self.evaluate(n,env)
  for p in paths_in(v):
   self.reads.append(p)
   if n:self.occurrences.append({'operation':'read','path':p,'source':self.anchor(n),'function_ast_id':self.stack[-1] if self.stack else None})
  return v
 def evaluate(self,n,env):
  if not n:return self.literal(None)
  if n.get('nodeType')=='Identifier' and n.get('name')=='this':return self.owner.instance_term(self.instance)
  if n.get('nodeType')=='IndexAccess':
   base=self.evaluate(n['baseExpression'],env);key=self.value(n.get('indexExpression'),env)
   if base.get('kind')=='storage':return {**base,'segments':base['segments']+[{'key':key,'index_source':self.anchor(n.get('indexExpression') or n),'origins':self.origins(n.get('indexExpression'))}]}
   return {'kind':'index','base':base,'key':key,'index_source':self.anchor(n)}
  if n.get('nodeType')=='UnaryOperation' and n.get('operator') in ['++','--']:
   value=self.value(n['subExpression'],env)
   self.assign(n['subExpression'],{'kind':'op','op':n['operator'],'args':[value]},env,n,n['operator'])
   return {'kind':'unresolved','reason':'increment_expression_value_not_evaluated','source':self.anchor(n)}
  if n.get('nodeType')=='FunctionCall':
   e=n['expression'];base=e.get('expression',{});bt=base.get('typeDescriptions',{}).get('typeString','')
   if e.get('nodeType')=='MemberAccess' and (bt.startswith('contract ') or e.get('memberName') in ['call','delegatecall','staticcall','callcode','send','transfer']):
    args=[self.value(a,env) for a in n.get('arguments',[])];target=self.value(base,env)
    resolution=None
    if target.get('kind')=='storage':
     resolution=self.owner.constants.get((self.instance,target['root']))
     if resolution:target=resolution['value']
    targets=[iid for iid,spec in self.owner.instances.items() if target==self.owner.instance_term(iid) or (target.get('kind')=='literal' and str(target['value']).lower()==str(spec.get('address')).lower())]
    declaration=self.fns.get(e.get('referencedDeclaration'));selector=self.function_selector(declaration or {})
    record={'source':self.anchor(n),'parent_frame':self.frame,'target_expression':self.qualify(target),'target_resolution':resolution,'arguments':args,'dispatch':'ordinary_external_call','caller_in_callee':self.owner.instance_term(self.instance)}
    if len(targets)==1 and selector and e.get('memberName') not in ['delegatecall','callcode']:
     iid=targets[0];spec=self.owner.instances[iid];bundle=self.owner.bundles[spec['program']];contract=next(c for c in bundle['contracts'] if c['file']==spec['file'] and c['name']==spec['contract'])
     matches=[f for f in contract['functions'] if f['selector']==selector]
     if len(matches)==1:
      record.update(target_instance=iid,function=matches[0]['signature'],status='static_known_target',child_frame=self.owner.trace(iid,matches[0]['signature'],args,self.owner.instance_term(self.instance),self.frame['top_level_caller'],self.frame['id'],self.anchor(n)))
     else:record.update(status='relation_unresolved',reason='callee_selector_not_unique')
    else:record.update(status='relation_unresolved',reason='unknown_target_or_unsupported_dispatch')
    self.external.append(record)
    if record['status']=='relation_unresolved':self.unknown.append(record)
    return {'kind':'external_return_unresolved','source':self.anchor(n)}
  return super().evaluate(n,env)
 def run(self,function,args,caller):
  self.reads=[];self.writes=[];self.guards=[];self.calls=[];self.unknown=[];self.stack=[]
  f=self.function(function)
  require(f and 'generated_getter' not in f,'binding_entry_requires_function_body')
  types=self.contract['constructor_types'] if function=='constructor' else self.abi[function]['types']
  require(len(args)==len(types),'binding_argument_count')
  self.sender=caller;self.entry=f;self.arguments=args
  values=[self.literal(v,t) for v,t in zip(args,types)];self.calldata={'kind':'calldata','selector':self.function_selector(f),'arguments':values}
  self.call(f,values,{})
  return f

class BindingAnalysis:
 def __init__(self,bundles,instances,native=None):
  self.bundles=bundles;self.instances=instances;self.native=native or {};self.records=[];self.constants={};self.active=[]
  self.context_id=None;self.invocation=0
  for key,n in self.native.items():
   b=bundles[key];require((n['program_id'],n['build_id'])==(b['program_id'],b['build_id']),'native_program_identity')
   require(digest(n)==b['native_ir']['sha256'],'native_content_identity')
  require(len({s.get('address') for s in instances.values() if s.get('address')})==len([s for s in instances.values() if s.get('address')]),'duplicate_instance_address')
 def instance_term(self,iid):return {'kind':'contract_instance','instance_id':iid,'address':self.instances[iid].get('address')}
 def corroborate(self,tracer,occurrence):
  native=self.native.get(self.instances[tracer.instance]['program'])
  if not native:return {'status':'compiler_static_only','unresolved_reason':'matching_native_ssa_not_supplied'}
  anchor=occurrence['source'];matches=[];chains=[]
  fnode=tracer.nodes.get(occurrence.get('function_ast_id'));fanchor=tracer.anchor(fnode) if fnode else None
  for fi,f in enumerate(native['functions']):
   s=f['source']
   if not fanchor or s['start']!=fanchor['start'] or not s['file'].replace('\\','/').endswith('/'+fanchor['file']) and s['file']!=fanchor['file']:continue
   expected_keys=[s for s in occurrence['path']['segments'] if 'key' in s]
   if expected_keys:
    from .native_reference_paths import correlate
    related,paths=correlate(f,fi,tracer,occurrence,fnode)
    matches.extend(related);chains.extend(paths)
   else:
    for ni,node in enumerate(f['nodes']):
     a=node['source'];end=a['start']+a['length']
     if a['start']<=anchor['start'] and anchor['start']+anchor['length']<=end:
      for oi,op in enumerate(node['ssa']):
       if op['operation'] in ['Index','Member','Assignment','Binary','SolidityCall','HighLevelCall']:
        matches.append({'json_pointer':f'/functions/{fi}/nodes/{ni}/ssa/{oi}','node_source':a,'operation':op['operation'],'text':op['text']})
  expected_keys=[s for s in occurrence['path']['segments'] if 'key' in s]
  verified=bool(matches) and (not expected_keys or any(c['keys_match'] for c in chains))
  return {'status':'compiler_and_native_keys_correlated' if verified and expected_keys else 'compiler_and_native_source_correlated' if verified else 'compiler_static_only','native_sha256':digest(native),'matches':matches,'key_chains':chains,'basis':'same program/build, exact function source and containing SSA node; field identity comes from compiler declaration IDs','unresolved_reason':None if verified else 'native_key_chain_or_node_not_resolved'}
 def trace(self,instance,function,args,caller,top=None,parent=None,callsite=None):
  key=(instance,function)
  if key in self.active or len(self.active)>=12:
   return {'status':'relation_unresolved','reason':'bounded_static_call_recursion'}
  bundle=self.bundles[self.instances[instance]['program']]
  self.invocation+=1
  frame={'analysis_id':self.context_id,'invocation':self.invocation,'instance_id':instance,'program_id':bundle['program_id'],'build_id':bundle['build_id'],'caller':caller,'top_level_caller':top or caller,'parent_frame':parent,'callsite':callsite}
  frame['id']=digest({**frame,'function':function,'arguments':args})
  tracer=BindingTrace(self,instance,frame);self.active.append(key)
  try:f=tracer.run(function,args,caller)
  finally:self.active.pop()
  occurrences=tracer.occurrences+[{'operation':'write','path':w['path'],'source':w['source'],'function_ast_id':w['function'],'value':w['value'],'operator':w['operator']} for w in tracer.writes]
  records=[]
  for o in tracer.unique(occurrences):
   records.append({**tracer.qualify(o),'path':tracer.qualify(o['path']),'frame_id':frame['id'],'basis':'compiler referencedDeclaration, nested IndexAccess/MemberAccess and argument/caller substitution','corroboration':self.corroborate(tracer,o),'execution_confirmed':False})
  # Constructor-derived immutable address substitutions are allowed only for one
  # unconditional assignment in that constructor. Mutable storage is not guessed.
  if function=='constructor':
   branched=any(n.get('nodeType') in ['IfStatement','ForStatement','WhileStatement','DoWhileStatement','Conditional'] for n in walk(f.get('body')))
   for w in tracer.writes:
    root=w['path']['root'];d=tracer.nodes[root]
    if d.get('mutability')=='immutable' and not branched and not f.get('modifiers') and not tracer.calls and not tracer.unknown and not tracer.external and w['operator']=='=' and not w['path']['segments'] and len([x for x in tracer.writes if x['path']['root']==root])==1:
     self.constants[(instance,root)]={'value':w['value'],'source':w['source'],'declaration':tracer.declaration(root),'basis':'single unconditional constructor assignment to compiler-declared immutable; supplied constructor argument, not deployed-code proof'}
  record={'frame':frame,'entry':{'function':function,'arguments':args,'argument_bindings':[{'parameter':tracer.declaration(p['id']),'term':v,'basis':'declared call scenario argument by ABI position, not a business role'} for p,v in zip(f['parameters']['parameters'],args)],'source':tracer.anchor(f)},'relationships':records,'guards':tracer.qualify(tracer.guards),'external_calls':tracer.external,'unresolved':tracer.unknown,'evidence_strength':'static_source_derivation','execution_confirmed':False}
  self.records.append(record);return frame['id']
 def output(self):return {'schema':SCHEMA,'frames':self.records,'programs':{k:{'program_id':b['program_id'],'build_id':b['build_id']} for k,b in self.bundles.items()},'instances':self.instances,'scope':'static possible relationships, not path feasibility, actual effects, risk or safety','execution_confirmed':False}

def analyze(bundles,instances,calls,native=None,policy=None):
 analysis=BindingAnalysis(bundles,instances,native)
 analysis.context_id=digest({'instances':instances,'calls':calls,'programs':{k:[b['program_id'],b['build_id']] for k,b in bundles.items()}})
 for c in calls:analysis.trace(c['instance_id'],c['function'],c['arguments'],c['caller'])
 result=analysis.output()
 from .static_roles import associate_roles
 associate_roles(result,bundles,instances,policy)
 return result
