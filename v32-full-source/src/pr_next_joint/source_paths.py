"""Source-derived storage paths with parameter/caller substitution.

This is a conservative provenance tracer, NEVER an EVM state interpreter. Unknown
values remain terms. Branch unions cannot prove effects; original execution does.
"""
import copy,json,re
from .source_entry_identity import elementary_expression_name
from .facts import walk
from .core import require,digest
from .source_entry_identity import EntryIdentity,function_kind,source_file

def stable(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def paths_in(value):
 if isinstance(value,dict):
  if value.get('kind')=='storage':yield value
  for v in value.values():yield from paths_in(v)
 elif isinstance(value,list):
  for v in value:yield from paths_in(v)

def compatible(a,b):
 """Exact subject/field/array-key equality; whole-struct writes cover children."""
 return a['root']==b['root'] and (a['segments']==b['segments'][:len(a['segments'])] or b['segments']==a['segments'][:len(b['segments'])])

class SourcePaths:
 def __init__(self,bundle,contract,aliases=None):
  self.bundle=bundle;self.contract=contract
  self.aliases=aliases or {}
  self.nodes={n['id']:n for ast in bundle['ast_sources'].values() for n in walk(ast) if 'id' in n}
  self.decls={n['id']:n for n in self.nodes.values() if n.get('nodeType')=='VariableDeclaration'}
  self.fns={n['id']:n for n in self.nodes.values() if n.get('nodeType') in ['FunctionDefinition','ModifierDefinition']}
  file_id=int(bundle['ast_sources'][contract['file']]['src'].split(':')[-1])
  cs=[n for n in self.nodes.values() if n.get('nodeType')=='ContractDefinition' and n['name']==contract['name'] and int(n['src'].split(':')[-1])==file_id]
  require(len(cs)==1,'contract_ast_ambiguous');self.contract_node=cs[0]
  order=self.contract_node.get('linearizedBaseContracts',[self.contract_node['id']])
  self.implementations=[f for cid in order for f in self.nodes[cid].get('nodes',[]) if f.get('nodeType')=='FunctionDefinition' and f.get('body')]
  self.abi={f['signature']:f for f in contract['functions']}
  self.entry_identity=EntryIdentity(self)
 def function(self,sig):
  return self.entry_identity.function(sig)
 def function_selector(self,node):return self.entry_identity.selector(node)
 def anchor(self,n):
  if not isinstance(n,dict):raise ValueError('source_anchor_node_missing')
  origin='compiler_src';raw=n.get('src')
  if not raw and n.get('id') in self.nodes:raw=self.nodes[n['id']].get('src')
  if not raw:
   # Generated expression wrappers inherit only an exact, single-file child span.
   spans=[]
   for child in walk(n):
    if child is n or not isinstance(child.get('src'),str):continue
    a,b,f=map(int,child['src'].split(':'))
    if a>=0 and b>=0 and f>=0:spans.append((a,b,f))
   if not spans or len({x[2] for x in spans})!=1:raise ValueError('source_anchor_unresolved')
   start=min(x[0] for x in spans);length=max(x[0]+x[1] for x in spans)-start;file_id=spans[0][2]
   origin='generated_wrapper_child_span'
  else:start,length,file_id=map(int,raw.split(':'))
  files={int(ast['src'].split(':')[-1]):f for f,ast in self.bundle['ast_sources'].items()}
  return {'file':files.get(file_id),'start':start,'length':length,'ast_id':n.get('id'),**({'anchor_origin':origin} if origin!='compiler_src' else {})}
 def trace(self,sig,args,caller='$B'):
  self.reads=[];self.writes=[];self.guards=[];self.calls=[];self.unknown=[];self.stack=[]
  f=self.function(sig)
  if not f:return {'reads':[],'writes':[],'guards':[],'calls':[],'returns':[],'unresolved':[],'native_agreement':True}
  if 'generated_getter' in f:
   d=f['generated_getter'];p={'kind':'storage','root':d['id'],'segments':[{'key':self.literal(v,t)} for v,t in zip(args,self.abi[sig]['types'])]}
   require(any(d['name']==name.split('.')[-1] for fn in self.bundle['native_ir']['functions'] for name in fn['reads']+fn['writes']),'public_getter_native_state_missing')
   return {'entry':self.anchor(d),'reads':[p],'writes':[],'guards':[],'calls':[],'returns':[p],'unresolved':[],'native_agreement':True,'generated_getter':True}
  self.sender=caller;self.entry=f;self.arguments=args
  values=[self.literal(v,t) for v,t in zip(args,self.contract['constructor_types'] if sig=='constructor' else self.abi[sig]['types'])]
  self.calldata={'kind':'calldata','selector':self.function_selector(f),'arguments':values}
  returns=self.call(f,values,{})
  native=self.entry_identity.native(f)
  require(native,'missing_native_function_binding')
  # Native SSA is an independent gate, not a decorative receipt. Every traced
  # state root must also occur in the native transitive read/write inventory.
  names=lambda key:{str(v).split('.')[-1] for n in native for v in n[key]}
  readnames=names('reads')|names('writes');writenames=names('writes')
  badread=[p for p in self.reads if self.nodes[p['root']]['name'] not in readnames]
  badwrite=[w for w in self.writes if self.nodes[w['path']['root']]['name'] not in writenames]
  return {'entry':self.anchor(f),'reads':self.unique(self.reads),'writes':self.unique(self.writes),'guards':self.unique(self.guards),'calls':self.unique(self.calls),'returns':returns,'unresolved':self.unique(self.unknown),'native_agreement':not badread and not badwrite,'native_disagreements':{'reads':badread,'writes':badwrite},'native_function_sources':[n['source'] for n in native]}
 def unique(self,x):return list({stable(v):v for v in x}.values())
 def literal(self,v,typ=None):
  if isinstance(v,dict):return v
  if isinstance(v,str):v=self.aliases.get(v,v)
  if typ=='bool':v=v in [True,'true','1',1]
  elif typ and (typ.startswith('uint') or typ.startswith('int')):v=int(v)
  return {'kind':'literal','value':v}
 def unknown_value(self,n):return {'kind':'unknown','source':self.anchor(n)}
 def evaluate(self,n,env):
  if not n:return self.literal(None)
  k=n.get('nodeType');rd=n.get('referencedDeclaration')
  if k=='Literal':
   v=n.get('value');v=(v=='true') if n['kind']=='bool' else int(v,0) if n['kind']=='number' else v
   return self.literal(v)
  if k in ['Identifier','IdentifierPath']:
   if rd in env:return env[rd]
   d=self.nodes.get(rd,{})
   if d.get('constant') and d.get('value'):return self.evaluate(d['value'],env)
   if d.get('stateVariable'):return {'kind':'storage','root':rd,'segments':[]}
   if n.get('name')=='this':return self.literal('$contract')
   return {'kind':'symbol','declaration':rd,'name':n.get('name')}
  if k=='MemberAccess':
   e=n['expression'];name=n['memberName'];v=self.evaluate(e,env)
   if v.get('kind')=='solidity_type' and name in ['min','max']:
    typ=v['name'];m=re.fullmatch('(u?int)([0-9]*)',typ)
    if m:
     bits=int(m[2] or 256);signed=m[1]=='int'
     return self.literal((-2**(bits-1) if signed else 0) if name=='min' else 2**(bits-int(signed))-1)
   if e.get('nodeType')=='Identifier' and e.get('name')=='msg':
    if name=='sender':return self.literal(self.sender)
    if name=='data':return self.calldata
    if name=='sig':return self.literal(self.calldata['selector'])
   if e.get('nodeType')=='Identifier' and e.get('name')=='block' and name=='timestamp':return {'kind':'environment','field':'timestamp'}
   if name=='selector':
    d=self.nodes.get(e.get('referencedDeclaration'),{});selector=self.function_selector(d)
    return self.literal(selector) if selector is not None else {'kind':'unknown','reason':'function_selector_unresolved','source':self.anchor(n)}
   if v.get('kind')=='calldata' and name=='length':return self.literal(4+32*len(v['arguments']))
   if v.get('kind')=='storage':return {**v,'segments':v['segments']+[{'field':rd,'label':name}]}
   return {'kind':'member','base':v,'member':name,'declaration':rd}
  if k=='IndexAccess':
   v=self.evaluate(n['baseExpression'],env);key=self.value(n.get('indexExpression'),env)
   if v.get('kind')=='storage':return {**v,'segments':v['segments']+[{'key':key}]}
   return {'kind':'index','base':v,'key':key}
  if k=='IndexRangeAccess':return {'kind':'slice','base':self.evaluate(n['baseExpression'],env),'start':self.value(n.get('startExpression'),env),'end':self.value(n.get('endExpression'),env)}
  if k=='TupleExpression':return {'kind':'tuple','items':[self.value(v,env) if v else self.literal(None) for v in n['components']]}
  if k=='BinaryOperation':return self.binary(n['operator'],self.value(n['leftExpression'],env),self.value(n['rightExpression'],env))
  if k=='UnaryOperation':
   v=self.value(n['subExpression'],env)
   if n['operator']=='!' and v.get('kind')=='literal':return self.literal(not v['value'])
   if n['operator']=='delete':self.assign(n['subExpression'],self.literal(0),env,n,'delete')
   return {'kind':'op','op':n['operator'],'args':[v]}
  if k=='Conditional':return {'kind':'choice','condition':self.value(n['condition'],env),'alternatives':[self.value(n['trueExpression'],env),self.value(n['falseExpression'],env)]}
  if k=='Assignment':
   value=self.value(n['rightHandSide'],env);self.assign(n['leftHandSide'],value,env,n,n['operator']);return value
  if k=='FunctionCall':
   e=n['expression'];args=[self.value(x,env) for x in n.get('arguments',[])];target=e.get('referencedDeclaration');f=self.fns.get(target)
   if e.get('name')=='type' and n.get('arguments'):return {'kind':'solidity_type','name':elementary_expression_name(n['arguments'][0])}
   if n.get('kind')=='structConstructorCall':
    struct=self.nodes.get(target,{})
    return {'kind':'record','fields':[{'field':m['id'],'value':v} for m,v in zip(struct.get('members',[]),args)]}
   if n.get('kind')=='typeConversion':
    if args and args[0].get('kind')=='slice' and args[0]['base'].get('kind')=='calldata':return self.literal(args[0]['base']['selector'])
    return args[0] if args else self.unknown_value(n)
   if e.get('nodeType')=='MemberAccess' and e.get('memberName')=='decode' and e.get('expression',{}).get('name')=='abi':
    v=args[0]
    if v.get('kind')=='slice' and v['base'].get('kind')=='calldata' and v['start'].get('kind')=='literal':
     ix=(v['start']['value']-4)//32
     if ix>=0 and ix<len(v['base']['arguments']):return v['base']['arguments'][ix]
   if f:
    if e.get('nodeType')=='MemberAccess' and len(f['parameters']['parameters'])==len(args)+1:
     args.insert(0,self.value(e['expression'],env))
    if not f.get('body'):
     selector=self.function_selector(f)
     fs=[x for x in self.implementations if selector is not None and self.function_selector(x)==selector]
     order=self.contract_node.get('linearizedBaseContracts',[self.contract_node['id']])
     chosen=self.entry_identity.select(fs,order,'internal_entry_selector_ambiguous')
     if chosen:f=chosen
     else:
      unresolved={'kind':'call_unresolved','reason':'compiler_referenced_body_unresolved','declaration':target,'source':self.anchor(n)}
      self.unknown.append(unresolved);return unresolved
    self.calls.append({'function':f['id'],'arguments':args,'source':self.anchor(n)})
    ret=self.call(f,args,env)
    if len(ret)==1:return ret[0]
    if ret:return {'kind':'choice','alternatives':ret}
   if e.get('name') in ['require','assert']:
    self.guards.append({'condition':args[0],'source':self.anchor(n),'origin':'require'});return self.literal(None)
   if e.get('nodeType')=='MemberAccess' and e.get('memberName') in ['wrap','unwrap']:return args[0] if args else self.unknown_value(n)
   # Event/custom-error constructors have no storage semantics.
   return {'kind':'call_unresolved','declaration':target,'arguments':args,'source':self.anchor(n)}
  self.unknown.append({'kind':k,'source':self.anchor(n)});return self.unknown_value(n)
 def value(self,n,env):
  v=self.evaluate(n,env)
  for p in paths_in(v):self.reads.append(p)
  return v
 def binary(self,op,a,b):
  if a.get('kind')==b.get('kind')=='literal':
   x,y=a['value'],b['value']
   try:
    if op=='==':return self.literal(x==y)
    if op=='!=':return self.literal(x!=y)
    if op=='&&':return self.literal(bool(x and y))
    if op=='||':return self.literal(bool(x or y))
    if op=='<':return self.literal(x<y)
    if op=='<=':return self.literal(x<=y)
    if op=='>':return self.literal(x>y)
    if op=='>=':return self.literal(x>=y)
   except TypeError:pass
  if op=='&&' and any(v.get('kind')=='literal' and v['value'] is False for v in [a,b]):return self.literal(False)
  if op=='||' and any(v.get('kind')=='literal' and v['value'] is True for v in [a,b]):return self.literal(True)
  return {'kind':'op','op':op,'args':[a,b]}
 def assign(self,left,value,env,source,op='='):
  if left.get('nodeType')=='TupleExpression':
   values=value.get('items',[]) if value.get('kind')=='tuple' else []
   for i,n in enumerate(left['components']):
    if n:self.assign(n,values[i] if i<len(values) else {'kind':'tuple_item','base':value,'index':i},env,source,op)
   return
  p=self.evaluate(left,env)
  if p.get('kind')=='storage':self.writes.append({'path':p,'value':value,'operator':op,'source':self.anchor(source),'function':self.stack[-1]})
  elif left.get('nodeType')=='Identifier':env[left['referencedDeclaration']]=value
 def call(self,f,args,outer):
  if f['id'] in self.stack or len(self.stack)>20:
   self.unknown.append({'recursion':f['id']});return []
  env={p['id']:v for p,v in zip(f['parameters']['parameters'],args)}
  self.stack.append(f['id'])
  for m in f.get('modifiers',[]):
   target=m['modifierName'].get('referencedDeclaration')
   if target in self.fns:self.call(self.fns[target],[self.value(a,env) for a in (m.get('arguments') or [])],env)
  returns=[];self.statement(f.get('body'),env,returns)
  self.stack.pop();return self.unique(returns)
 def statement(self,n,env,returns):
  if not n:return False
  k=n.get('nodeType')
  if k in ['Block','UncheckedBlock']:
   for s in n.get('statements',[]):
    if self.statement(s,env,returns):return True
  elif k=='VariableDeclarationStatement':
   v=self.value(n.get('initialValue'),env);decls=n['declarations']
   for i,d in enumerate(decls):
    if d:env[d['id']]=(v.get('items',[])[i] if v.get('kind')=='tuple' and i<len(v['items']) else {'kind':'tuple_item','base':v,'index':i}) if len(decls)>1 else v
  elif k=='ExpressionStatement':self.value(n['expression'],env)
  elif k=='Return':returns.append(self.value(n.get('expression'),env));return True
  elif k=='RevertStatement':return True
  elif k=='IfStatement':
   condition=self.value(n['condition'],env);self.guards.append({'condition':condition,'source':self.anchor(n['condition']),'origin':'branch'})
   if condition.get('kind')=='literal':return self.statement(n.get('trueBody') if condition['value'] else n.get('falseBody'),env,returns)
   yes=copy.deepcopy(env);no=copy.deepcopy(env)
   a=self.statement(n.get('trueBody'),yes,returns);b=self.statement(n.get('falseBody'),no,returns)
   for key in set(yes)|set(no):
    if yes.get(key)==no.get(key):env[key]=yes.get(key)
    else:env[key]={'kind':'choice','condition':condition,'alternatives':[yes.get(key,self.literal(None)),no.get(key,self.literal(None))]}
   return a and b
  elif k in ['EmitStatement','PlaceholderStatement']:pass
  else:self.unknown.append({'statement':k,'source':self.anchor(n)})
  return False
