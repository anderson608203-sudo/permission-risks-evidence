# 源码文本 · 6

## source/src/pr_next_joint/frontend/source_paths.py

原文件 SHA-256 `aad1a722cbe2a9df8453f42746c260628609f1054f29506ec0afb2ab3830124f`

````python
"""Source-derived storage paths with parameter/caller substitution.

This is a conservative provenance tracer, NEVER an EVM state interpreter. Unknown
values remain terms. Branch unions cannot prove effects; original execution does.
"""
import copy,json,re
from pr_next_joint.frontend.source_entry_identity import elementary_expression_name
from pr_next_joint.frontend.facts import walk
from pr_next_joint.core import require, digest
from pr_next_joint.frontend.source_entry_identity import EntryIdentity, function_kind, source_file

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

````

## source/src/pr_next_joint/frontend/source_work_budget.py

原文件 SHA-256 `85e9a8260a1d3a7313af1426dacc96ada6f8b2bd147d6b5cfdae098c27028134`

````python
"""One finite per-entry budget and measurable normalization work."""
from contextvars import ContextVar
active=ContextVar("source_operation_work",default=None)
from pr_next_joint.reporting.effective_parameters import current
MAX_VISITS=current()["normalization_visits_per_operation_max"]
def begin():return active.set({"visits":0,"clean_calls":0,"shared_subtree_hits":0,"normalization_cache_hits":0,"max_expression_nodes":0,"max_depth":0})
def snapshot():return dict(active.get() or {})
def end(token):active.reset(token)
def metric(name,value=1,maximum=False):
    state=active.get()
    if state is not None:state[name]=max(state.get(name,0),value) if maximum else state.get(name,0)+value
def visit():
    state=active.get()
    if state is not None:
        state["visits"]+=1
        if state["visits"]>MAX_VISITS:raise ValueError("source_operation_normalization_bound_exceeded:"+str(MAX_VISITS))

````

## source/src/pr_next_joint/frontend/storage.py

原文件 SHA-256 `bef8225cc614829ee90c2248f6d4db6b0859bcf651dc17676a60cccb518e7ccc`

````python
"""Source object identity and typed selectors."""
import copy
from pr_next_joint.frontend.path_ir import key, walk, normalize, op, conditions_possible

def keys(path):return [s['key'] for s in path.get('segments',[]) if 'key' in s]

def fields(path):return [s['field'] for s in path.get('segments',[]) if 'field' in s]

def selectors(expr):return [n for n in walk(expr) if n.get('kind')=='storage']

def value_type(path,lookup):
    typ=lookup.nodes.get(path['root'],{}).get('typeName',{})
    for seg in path.get('segments',[]):
        if seg.get('length'):return 'uint256'
        typ=(typ.get('valueType',{}) if typ.get('nodeType')=='Mapping' else typ.get('baseType',{})) if 'key' in seg else lookup.nodes.get(seg['field'],{}).get('typeName',{})
    from pr_next_joint.frontend.language import scalar_type
    return scalar_type(typ.get('typeDescriptions',{}).get('typeString') or typ.get('name'),lookup,typ)

def relocate(policy,source_path,target_path):
    if source_path['root']!=target_path['root']:raise ValueError('P_RESOURCE_ROOT_MISMATCH')
    a,b=keys(source_path),keys(target_path)
    if len(a)!=len(b):raise ValueError('P_RESOURCE_KEY_ARITY')
    mapping={}
    for left,right in zip(a,b):
        if left.get('kind')=='parameter':
            if left.get('type')!=right.get('type') and right.get('kind')=='parameter':raise ValueError('P_RESOURCE_KEY_TYPE')
            if left['id'] in mapping and mapping[left['id']]!=right:raise ValueError('P_KEY_BINDING_CONFLICT')
            mapping[left['id']]=right
        elif key(left)!=key(right):raise ValueError('P_KEY_IDENTITY_UNRESOLVED')
    def sub(v):
        if isinstance(v,dict):
            if v.get('kind')=='parameter':
                if v['id'] not in mapping:raise ValueError('P_POLICY_PARAMETER_UNBOUND')
                return copy.deepcopy(mapping[v['id']])
            return {k:sub(x) for k,x in v.items()}
        return [sub(x) for x in v] if isinstance(v,list) else v
    return sub(policy)

def state_overlap(a,b):
    if a['root']!=b['root'] or key(a.get('instance'))!=key(b.get('instance')):return False
    # For authority classification, keys describe independent members of a family.
    af,bf=fields(a),fields(b)
    return not af or not bf or af==bf


def selector_relation(a,b,ignore_fields=False):
    """Typed storage positions. Keys can alias; length and element are siblings."""
    if a['root']!=b['root'] or key(a.get('instance'))!=key(b.get('instance')):return 'disjoint'
    aa,bb=a.get('segments',[]),b.get('segments',[])
    for x,y in zip(aa,bb):
        kx='key' if 'key' in x else 'length' if x.get('length') else 'field'
        ky='key' if 'key' in y else 'length' if y.get('length') else 'field'
        if {kx,ky}=={'length','key'}:return 'disjoint'
        if kx!=ky:return 'unsupported_shape'
        if kx=='field' and not ignore_fields and x['field']!=y['field']:return 'disjoint'
    if len(aa)!=len(bb):return 'parent_child'
    return 'same_shape'

````

## source/src/pr_next_joint/frontend/value_paths.py

原文件 SHA-256 `4f604d2da1f00b95c704ab392af03163b596ae1ef8d9a31bb496121409ff5d33`

````python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""
import copy
from pr_next_joint.frontend.path_ir import Paths, op, lit, walk, conditions_possible

class AssetPaths(Paths):
    def evaluate(self,n,env):
        if n and n.get('nodeType')=='MemberAccess':
            base=n.get('expression',{})
            if base.get('nodeType')=='Identifier' and base.get('name')=='msg' and n['memberName']=='value':
                return {'kind':'transaction_value','type':'uint256'}
            if n['memberName']=='balance' and self.value(base,env).get('kind')=='contract_address':
                return {'kind':'native_reserve','instance':self.value(base,env)}
        if n and n.get('nodeType')=='FunctionCall':
            from pr_next_joint.frontend.calls import native_call
            result=native_call(self,n,env)
            if result is not None:return result
            options=n.get('expression',{});member=options.get('expression',{})
            from pr_next_joint.frontend.source_entry_identity import builtin_call
            if builtin_call(n,self,('selfdestruct','suicide')):
                args=n.get('arguments',[])
                if len(args)==1:
                    recipient=self.value(args[0],env)
                    effect={'kind':'native_selfdestruct','recipient':recipient,
                        'amount':{'kind':'native_reserve','instance':self.read_calls.address()},
                        'source':self.anchor(n),'scope':'native balance disposition; code/storage destruction depends on EVM revision'}
                    effect.setdefault('callpoint_writes', copy.deepcopy(self.current.get('writes', [])))
                    effect.setdefault('callpoint_guards', copy.deepcopy(self.current.get('guards', [])))
                    effect.setdefault('callpoint_evaluations', copy.deepcopy(self.current.get('evaluated_terms', [])))
                    self.current.setdefault('sensitive_effects',[]).append(effect)
                    self.current['flow']='returned'
                    self.current['_evm_halted']=True
                    return {'kind':'literal','value':True}
            if options.get('nodeType')=='MemberAccess' and options.get('memberName') in ('transfer','send'):
                typ=options.get('expression',{}).get('typeDescriptions',{}).get('typeString','')
                if typ in ('address','address payable') and len(n.get('arguments',[]))==1:
                    recipient=self.value(options['expression'],env);amount=self.value(n['arguments'][0],env)
                    success={'kind':'native_call_success','source_id':n['id']}
                    effect={'kind':'native_transfer','recipient':recipient,'amount':amount,'success':success,
                        'source':self.anchor(n),'scope':'source native payout conditional on successful external call'}
                    self.current.setdefault('native_transfers',[]).append(copy.deepcopy(effect))
                    effect.setdefault('callpoint_writes', copy.deepcopy(self.current.get('writes', [])))
                    effect.setdefault('callpoint_guards', copy.deepcopy(self.current.get('guards', [])))
                    effect.setdefault('callpoint_evaluations', copy.deepcopy(self.current.get('evaluated_terms', [])))
                    self.current.setdefault('sensitive_effects',[]).append(effect)
                    if options['memberName']=='transfer':self.current['guards'].append(success)
                    return success
            from pr_next_joint.checks.access.code_control import builtin_delegate
            if builtin_delegate(options,self):
                # Evaluate invocation arguments before claiming the call is
                # reachable. A pure literal hash selector cannot revert; its
                # numeric value is irrelevant to target controllability.
                from pr_next_joint.checks.access.code_control import literal_selector
                for argument in n.get('arguments',[]):
                    if literal_selector(argument,self):continue
                    value=self.value(argument,env)
                    if any(x.get('kind') in ('unknown','call_unresolved') for x in walk(value)):
                        self.current['issues'].append({'reason':'delegate_argument_not_lowered','source':self.anchor(argument)})
                    if any(x.get('kind')=='index' for x in walk(value)):
                        self.current.setdefault('evaluated_terms',[]).append(copy.deepcopy(value))
                effect={'kind':'dangerous_external_call','recipient':self.value(options['expression'],env),
                    'source':self.anchor(n),'scope':'external behavior not resolved',
                    'prefix_conditions':copy.deepcopy(self.current['guards']),
                    'prefix_issues':copy.deepcopy(self.current['issues']),
                    'prefix_evaluation_terms':copy.deepcopy(self.current.get('evaluated_terms',[]))}
                effect.setdefault('callpoint_writes', copy.deepcopy(self.current.get('writes', [])))
                effect.setdefault('callpoint_guards', copy.deepcopy(self.current.get('guards', [])))
                effect.setdefault('callpoint_evaluations', copy.deepcopy(self.current.get('evaluated_terms', [])))
                self.current.setdefault('sensitive_effects',[]).append(effect)
                self.current['issues'].append({'reason':'dangerous_external_effect_not_resolved','source':self.anchor(n)})
                success={'kind':'native_call_success','source_id':n['id']}
                effect['success']=success
                if n.get('typeDescriptions',{}).get('typeString')=='bool':return success
                return {'kind':'tuple','items':[success,{'kind':'native_return_data','source_id':n['id']}]}

            if options.get('nodeType')=='FunctionCallOptions' and member.get('nodeType')=='MemberAccess' and member.get('memberName')=='call':
                args=n.get('arguments',[])
                if options.get('names')==['value'] and len(args)==1 and args[0].get('nodeType')=='Literal' and args[0].get('value')=='':
                    recipient=self.value(member['expression'],env);amount=self.value(options['options'][0],env)
                    success={'kind':'native_call_success','source_id':n['id']}
                    self.current.setdefault('native_transfers',[]).append({'recipient':recipient,'amount':amount,'success':success,'source':self.anchor(n),
                        'scope':'source payout relation, conditional on success; external recipient behavior not executed'})
                    self.current.setdefault('sensitive_effects',[]).append({'kind':'native_transfer','recipient':recipient,
                        'amount':amount,'success':success,'source':self.anchor(n),
                        'scope':'conditional native transfer; callee behavior not executed'})
                    return {'kind':'tuple','items':[success,{'kind':'native_return_data','source_id':n['id']}]}
        return super().evaluate(n,env)

    def statement(self,n,s,depth):
        if n and n.get('nodeType')=='VariableDeclarationStatement' and len(n.get('declarations',[]))==1 and (n.get('initialValue') or {}).get('nodeType')=='Conditional':
            expr=n['initialValue'];condition=self.expr(expr['condition'],s);out=[]
            for sign,name in ((True,'trueExpression'),(False,'falseExpression')):
                child=copy.deepcopy(s);child['guards'].append(condition if sign else op('!',condition))
                if conditions_possible(child['guards']):
                    selected=copy.deepcopy(n);selected['initialValue']=expr[name];out.extend(self.statement(selected,child,depth))
            return out
        if n and n.get('nodeType')=='VariableDeclarationStatement' and len(n.get('declarations',[]))>1:
            v=self.expr(n.get('initialValue'),s)
            for i,d in enumerate(n['declarations']):
                if d:s['env'][d['id']]=v['items'][i] if v.get('kind')=='tuple' and i<len(v['items']) else {'kind':'unknown','reason':'tuple_local'}
            return [s]
        return super().statement(n,s,depth)

````

## source/src/pr_next_joint/graph/__init__.py

原文件 SHA-256 `87e3e2f1dba261e0999d37d622e45825e4d2763d9091aa860663f27df53e5d17`

````python
"""Source analysis helpers retained by SCRV."""

````

## source/src/pr_next_joint/graph/object_equivalence.py

原文件 SHA-256 `eb3006bac034ff9621c3a4d4e9c26ebfaa5eae629b7fa7a6358c91e528c482fc`

````python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""
import re
from pr_next_joint.checks.credentials.credential_encoding import fixed_literal
from pr_next_joint.verification.expressions import Unsupported


def literal_key(term, declaration):
    raw, length = fixed_literal(term)
    target = declaration.get('keyType', {})
    typ = target.get('name') or target.get('typeDescriptions', {}).get('typeString')
    if declaration.get('nodeType') != 'Mapping':
        raise Unsupported('literal_index_without_mapping_domain')
    if typ in ('string', 'bytes'):
        # Prefixing a byte preserves length, including empty and leading NULs.
        return int('01' + raw, 16)
    match = re.fullmatch(r'bytes([1-9]|[12][0-9]|3[0-2])', typ or '')
    if match and length <= int(match[1]):
        # Solidity pads a string literal with zeros on the right on conversion.
        return int(raw.ljust(2 * int(match[1]), '0'), 16)
    raise Unsupported('literal_key_conversion_outside_mapping_domain')

def selector_equalities(left, right, lookup):
    from pr_next_joint.frontend.path_ir import lit, op
    declaration = lookup.nodes[left['root']].get('typeName', {})
    tests = []
    # Callers have checked storage root, receiver, field sequence and arity.
    if len(left['segments']) != len(right['segments']):
        raise Unsupported('literal_selector_structure')
    for a, b in zip(left['segments'], right['segments']):
        if 'key' in a and 'key' in b:
            x, y = a['key'], b['key']
            if x.get('kind') == y.get('kind') == 'fixed_bytes_literal':
                tests.append(lit(literal_key(x, declaration) == literal_key(y, declaration)))
            else:
                tests.append(op('==', x, y))
            declaration = declaration.get('valueType', declaration.get('baseType', {}))
        elif a == b and 'field' in a:
            declaration = lookup.nodes[a['field']].get('typeName', {})
        elif a != b:
            raise Unsupported('literal_selector_structure')
    return tests

````

## source/src/pr_next_joint/graph/relation_model_scope.py

原文件 SHA-256 `d93047cfbba705204e9854dd460e8936d0df4457f11696de6920ba9abd975aa2`

````python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""
from pr_next_joint.frontend.path_ir import walk

def source_term(node,lookup,function,function_node=None):
    """Pure, deliberately small AST projection; no calls or local alias guess."""
    fn=function_node or lookup.function(function) or {}
    params={p['id']:p for p in fn.get('parameters',{}).get('parameters',[])}
    def lower(n):
        kind=n.get('nodeType');ref=n.get('referencedDeclaration')
        if kind=='VariableDeclaration' and n.get('stateVariable') and n.get('id') in lookup.decls:
            return {'kind':'storage','root':n['id'],'segments':[]}
        if kind=='VariableDeclaration' and n.get('id') in params:
            return {'kind':'parameter','id':n['id'],'type':params[n['id']]['typeDescriptions']['typeString']}
        if kind=='Identifier':
            # Same authenticated compiler builtins used by the path evaluator.
            # A user declaration named now/block/msg is never a builtin.
            if (n.get('name')=='now' and type(ref) is int and ref not in lookup.nodes
                    and n.get('typeDescriptions',{}).get('typeIdentifier')=='t_uint256'):
                return {'kind':'environment','field':'timestamp','type':'uint256'}
            decl=lookup.nodes.get(ref,{})
            if decl.get('stateVariable'):return {'kind':'storage','root':ref,'segments':[]}
            if ref in params:return {'kind':'parameter','id':ref,'type':params[ref]['typeDescriptions']['typeString']}
        if kind=='Literal':
            if n.get('kind')=='bool':return {'kind':'literal','value':n['value']=='true'}
            if n.get('kind')=='number':
                try:return {'kind':'literal','value':int(n['value'],0)}
                except ValueError:return None
        if kind=='MemberAccess':
            e=n.get('expression',{})
            from pr_next_joint.frontend.source_entry_identity import builtin_object
            if builtin_object(e,lookup,'msg') and n.get('memberName')=='sender':return {'kind':'actual_sender'}
            if builtin_object(e,lookup,'block') and n.get('memberName') in ('timestamp','number'):
                return {'kind':'environment','field':n['memberName'],'type':'uint256'}
            base=lower(e)
            if base and base.get('kind')=='storage' and type(ref)is int and ref>=0:
                return {**base,'segments':base['segments']+[{'field':ref,'label':n['memberName']}]}
        if kind=='IndexAccess':
            base=lower(n.get('baseExpression',{}));index=lower(n.get('indexExpression') or {})
            if base and index and base.get('kind')=='storage':return {**base,'segments':base['segments']+[{'key':index}]}
        if kind=='TupleExpression' and not n.get('isInlineArray'):
            parts=n.get('components',[])
            if len(parts)==1 and parts[0] is not None:return lower(parts[0])
        if kind=='ExpressionStatement':return lower(n.get('expression',{}))
        if kind=='FunctionCall':
            f=n.get('expression',{});ref=f.get('referencedDeclaration')
            from pr_next_joint.frontend.source_entry_identity import builtin_call
            if builtin_call(n,lookup) and n.get('arguments'):
                return lower(n['arguments'][0])
        if kind in ('BinaryOperation','UnaryOperation'):
            nodes=[n.get('subExpression',{})] if kind=='UnaryOperation' else [n.get('leftExpression',{}),n.get('rightExpression',{})]
            args=[lower(a) for a in nodes];operator=n.get('operator')
            if all(a is not None for a in args) and operator in ('!','&&','||','==','!=','<','<=','>','>=','+','-','&','|'):
                from pr_next_joint.frontend.path_ir import normalize
                return normalize({'kind':'op','op':operator,'args':args})
        if kind=='IfStatement':
            condition=lower(n.get('condition',{}))
            if condition is None:return None
            true=n.get('trueBody',{});false=n.get('falseBody')
            def bare_revert(branch):
                statements=branch.get('statements',[]) if branch.get('nodeType')=='Block' else [branch]
                if len(statements)!=1:return False
                x=statements[0];call=x.get('expression',{}) if x.get('nodeType')=='ExpressionStatement' else x
                from pr_next_joint.frontend.source_entry_identity import builtin_call
                return x.get('nodeType')=='RevertStatement' or builtin_call(call,lookup,('revert',))
            from pr_next_joint.frontend.path_ir import normalize, op
            if bare_revert(true) and not false:return normalize(op('!',condition))
            if false and bare_revert(false):return condition
        return None
    if node.get('nodeType') in ('FunctionCall','RevertStatement'):
        from pr_next_joint.frontend.source_entry_identity import builtin_call
        if node.get('nodeType')=='RevertStatement' or builtin_call(node,lookup,('revert',)):
            operation=[fn]
            for modifier in fn.get('modifiers',[]):operation.append(lookup.nodes.get(modifier.get('modifierName',{}).get('referencedDeclaration'),{}))
            candidates=[n for n in walk(operation) if n.get('nodeType')=='IfStatement' and any(v.get('id')==node.get('id') for v in walk(n))]
            candidates.sort(key=lambda n:len(list(walk(n))))
            for ancestor in candidates:
                value=lower(ancestor)
                if value is not None:return value
    return lower(node)

````

## source/src/pr_next_joint/graph/state_relations.py

原文件 SHA-256 `2f9d92d2e1bdc09555568a31f8c6ccf918dd0fb9fb37ba91d5c4fb8820b7e20c`

````python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""
import copy
from pr_next_joint.frontend.path_ir import key, op, lit
from pr_next_joint.frontend.storage import value_type
from pr_next_joint.verification.expressions import Unsupported
from pr_next_joint.checks.access.credential_lifecycle import leaves

def enum_size(lookup,typ):
    if not isinstance(typ,str) or not typ.startswith('enum '):return None
    name=typ[5:]
    found=[n for n in lookup.nodes.values() if n.get('nodeType')=='EnumDefinition'
           and (n.get('canonicalName')==name or n.get('name')==name)]
    if len(found)!=1:raise Unsupported('enum_declaration_not_unique:'+name)
    size=len(found[0]['members'])
    if not 0<size<=256:raise Unsupported('enum_domain_size')
    return size

def scalar(write,lookup):
    if write['value'].get('kind')!='zero_of_storage_type':return write
    typ=value_type(write['path'],lookup)
    if typ=='bool':zero=False
    elif typ and (typ.startswith(('uint','bytes','enum ')) or typ in ('address','address payable')):zero=0
    else:raise Unsupported('container_delete_not_scalar')
    return {**write,'value':lit(zero),'zeroing_source_operator':write.get('operator')}

def expand_write(write,lookup,depth=0):
    """Expand deletion of an already bound finite struct; no source discovery."""
    if depth>8:raise Unsupported('finite_delete_structure_depth')
    if write['value'].get('kind')=='record':
        return [x for leaf in leaves(write) for x in expand_write(leaf,lookup,depth+1)]
    if write['value'].get('kind')!='zero_of_storage_type':return [write]
    typ=lookup.nodes.get(write['path']['root'],{}).get('typeName',{})
    for segment in write['path'].get('segments',[]):
        typ=typ.get('valueType',{}) if 'key' in segment else lookup.nodes.get(segment['field'],{}).get('typeName',{})
    declaration=lookup.nodes.get(typ.get('referencedDeclaration'),{})
    if declaration.get('nodeType')!='StructDefinition':return [scalar(write,lookup)]
    result=[]
    for member in declaration.get('members',[]):
        if member.get('typeName',{}).get('nodeType') in ('Mapping','ArrayTypeName'):
            raise Unsupported('finite_delete_dynamic_member_not_modeled')
        path={**write['path'],'segments':write['path'].get('segments',[])+[{'field':member['id']}]}
        result+=expand_write({**write,'path':path,'expanded_delete_source':copy.deepcopy(write['path'])},lookup,depth+1)
    if not result:raise Unsupported('finite_delete_empty_structure')
    return result

def compose_read(value,writes,lookup):
    """Source-keyed read-over-write, including updates to an aliased key."""
    from pr_next_joint.frontend.storage import fields, keys
    from pr_next_joint.frontend.path_ir import normalize
    if isinstance(value,dict):
        if value.get('kind')=='storage':
            result=copy.deepcopy(value)
            for w in writes:
                p=w['path']
                from pr_next_joint.frontend.storage import selector_relation
                relation=selector_relation(value,p)
                if relation=='disjoint':continue
                if relation!='same_shape':raise Unsupported('transition_container_update_not_scalar:'+relation)
                w=scalar(w,lookup)
                a,b=keys(value),keys(p)
                if len(a)!=len(b):raise Unsupported('transition_selector_arity')
                if any(x.get('kind')=='fixed_bytes_literal' and y.get('kind')=='fixed_bytes_literal' for x,y in zip(a,b)):
                    from pr_next_joint.graph.object_equivalence import selector_equalities
                    tests=selector_equalities(value,p,lookup)
                else:
                    tests=[op('==',x,y) for x,y in zip(a,b)]
                same=normalize(op('and',*tests))
                result=w['value'] if same==lit(True) else op('ite',same,w['value'],result)
            return result
        return {k:compose_read(v,writes,lookup) for k,v in value.items()}
    return [compose_read(v,writes,lookup) for v in value] if isinstance(value,list) else value

````

## source/src/pr_next_joint/investigation/__init__.py

原文件 SHA-256 `2b3d1be9fda3394bf48f0a89ed593cfb8bc09bae72fd87010dd2bbd6f074ade8`

````python
"""Source-led semantic investigation; no legacy relation admission."""

````

## source/src/pr_next_joint/investigation/authorization.py

原文件 SHA-256 `bfd67f3bcb5c82cd950b03e0e3b695b0f562a9a91a487fd4f48700bde8e7fec2`

````python
"""Consume a necessary authorization premise from existing text and actual source.

The certificate excludes an asserted causal acquisition, never all access-control
risks in the same function or contract. It does not invent a business policy.
"""
import re
from pr_next_joint.frontend.path_ir import walk, key
from pr_next_joint.frontend.storage import selectors, keys, value_type
from .request_scope import claim_entries
from .initial_state import runtime_writers


def acquisition_premise(inv,q):
    if inv.f.options.scope!='AC':return None
    item=q['current'];root=inv.root(q)
    if not root or not q['binding'].get('core_exact'):return None
    text=item['claim']+' '+str((item.get('observation') or {}).get('risk','') if isinstance(item.get('observation'),dict) else '')
    if not re.search(r'\b(?:acquir\w*|gain\w*|install\w*|takeover|becom\w*|owner acquisition|effective.*gate)\b|取得|接管|获得',text,re.I):return None
    entries=claim_entries(inv,q['binding'],item)
    if len(entries)<2 or not inv.backend.complete(root):return None
    target=inv.f.operations[root]['target'];lookup=inv.f.lookup(root)
    writes=[w for _,p in inv.f.operation_paths(root,True) for w in p['writes']]
    address_writes=[w for w in writes if value_type(w['path'],lookup) in ('address','address payable') and not keys(w['path'])
                    and w['value'].get('kind') in ('actual_sender','parameter')]
    if not address_writes:return None
    guarded=[]
    for use in sorted(entries-{root}):
        if inv.f.operations[use]['target']!=target or inv.f.operations[use].get('generated_getter'):continue
        if not inv.f.operations[use]['paths']:return None
        for pid,p in inv.f.operation_paths(use,True):
            if any(n.get('kind') in ('unknown','external_return') for n in walk(p['guards'])):return None
            gates=[]
            for g in p['guards']:
                for term in walk(g):
                    if term.get('op')=='==' and any(a.get('kind')=='actual_sender' for a in term.get('args',[])):
                        gates.extend(c for c in selectors(term) if value_type(c,lookup) in ('address','address payable') and not keys(c))
            if gates:guarded.append({'operation':use,'path':pid,'gates':gates})
    if not guarded:return None
    # Check all committed data/control flow to the requested qualification,
    # including helper-expanded operations. A missing/opaque connection stays open.
    rw=runtime_writers(inv.f,target)
    if rw['opaque_storage_writes'] or rw['unresolved_calls']:return None
    gates_needed={s['root'] for row in guarded for s in row['gates']}
    influenced={w['path']['root'] for w in writes}
    changed=True
    while changed:
        changed=False
        for oid,o in inv.f.operations.items():
            if o['target']!=target:continue
            for _,p in inv.f.operation_paths(oid):
                relevant=any(s['root'] in influenced for s in selectors([p['guards'],[w['value'] for w in p['writes']]]))
                if not relevant:continue
                if (p.get('issues') or p.get('evaluation_gaps')) and any(w['path']['root'] in gates_needed for w in p['writes']):return None
                if p['flow'] not in ('normal','returned'):continue
                for w in p['writes']:
                    if w['path']['root'] not in influenced:influenced.add(w['path']['root']);changed=True
    gates={s['root'] for row in guarded for s in row['gates']}
    if gates&influenced:return None
    return {'status':'refuted','necessary_premise':'the cited public write changes the authority read by the cited protected effect',
        'reason':'different_storage_declarations_and_no_committed_data_or_control_flow',
        'target':target,'change':root,'written_authority_cells':[w['path'] for w in address_writes],
        'protected_effects':guarded,'reachable_write_closure':sorted(influenced),
        'retained_fact':'the separate source field can change; independent entry risks are unchanged',
        'whole_contract_safety':False,'business_policy_invented':False}

````

## source/src/pr_next_joint/investigation/authorization_normal.py

原文件 SHA-256 `29c938c7476513a2df4767b24e386b2b8389e28ad9f5311421ea7445dd067a61`

````python
"""Source relations for narrow, reviewable normal authorization alternatives.

The model proposes the business interpretation. These builders require the
corresponding source operands; they never equate an arbitrary guard with policy.
"""
import re
from pr_next_joint.frontend.path_ir import key, op, walk
from pr_next_joint.frontend.storage import keys, selector_relation, value_type
from .summary import unique, directions


def numeric_delegations(inv, root, subject):
    """Holder-issued quantity, compared with the actual debit, not a fee net."""
    f=inv.f;target=f.operations[root]['target'];lookup=f.lookup(root);found=[]
    from .summary import debited_positions
    for row in f.summaries.rows(root):
        for effect in debited_positions(f,root):
            if effect['path']!=row['path'] or key(effect['holder'])!=key(subject):continue
            amount=effect['amount']
            from pr_next_joint.frontend.storage import selectors
            for cell in selectors(row['guards']):
                idx=keys(cell)
                if len(idx)!=2 or key(idx[0])!=key(subject) or idx[1].get('kind')!='actual_sender':continue
                if not re.fullmatch(r'u?int\d*',value_type(cell,lookup) or ''):continue
                writers=[w for w in f.writes.values() if f.operations[w['operation']]['target']==target and
                    selector_relation(w['raw']['path'],cell)=='same_shape']
                grants=[];bad=False
                for w in writers:
                    dst=w['raw']['path'];v=w['raw']['value']
                    if 'credit' not in directions(dst,v):continue
                    ks=keys(dst);p=f.paths[w['path']]['raw']
                    if (len(ks)!=2 or ks[0].get('kind')!='actual_sender' or ks[1].get('kind')!='parameter' or
                         any(c['mode']=='DELEGATECALL' and c['unresolved_implementation'] for c in f.call_summaries.rows.values()
                             if f.operations[c['operation']]['target']==target)):
                        # Ordinary CALL cannot change msg.sender of this
                        # source assignment. Its exit/return uncertainty is
                        # separate from the immutable issuer/key invariant.
                        bad=True;break
                    grants.append({'operation':w['operation'],'path':w['path'],'source':w['raw']['source']})
                from .initial_state import initial_for_lookup
                initial=initial_for_lookup(lookup) or {}
                for cp in initial.get('constructor_paths',[]):
                    if cp.get('issues') or cp.get('evaluation_gaps'):bad=True;break
                    for w in cp['writes']:
                        if selector_relation(w['path'],cell)!='same_shape' or w['value'].get('value') in (0,False):continue
                        kk=keys(w['path'])
                        if len(kk)!=2 or kk[0].get('kind')!='actual_sender':bad=True;break
                if grants and not bad:
                    found.append({'predicate':op('>=',cell,amount),'holder':subject,'allowance':cell,
                        'actual_debit':amount,'grant_sources':grants,'use_path':row['path'],
                        'kind':'holder_issued_quantity_covers_actual_debit'})
    return unique(found)


def payment_qualification(inv,q,subject,require_proposal=True):
    """Paid acquisition of a scalar authority, explicitly proposed as lawful.

Supported relation: the new holder is the payer, the stored bid equals the
actual payment, and payment exceeds the previous bid. A payment alone is not
authorization. Other business policies remain unresolved.
"""
    item=q['current'];proposal=q.get('authorization_interpretation') or {}
    text=' '.join(str(item.get(k) or '') for k in ('claim','normal_basis','revision_reason','alternative'))+' '+str(proposal.get('basis',''))
    if require_proposal:
        if item.get('assessment')!='normal' and proposal.get('meaning')!='normal_authorization':return []
        if not re.search(r'\b(?:lawful|legitimate|valid|normal)\b.{0,45}\b(?:auction|bid|paid acquisition|business qualification)\b|合法.{0,15}(?:竞价|拍卖)',text,re.I):return []
    if keys(subject):return []
    root=inv.root(q);lookup=inv.f.lookup(root);found=[]
    for pid,path in inv.f.operation_paths(root,True):
        if path.get('issues') or path.get('evaluation_gaps'):continue
        owner_write=any(key(w['path'])==key(subject) and w['value'].get('kind')=='actual_sender' for w in path['writes'])
        if not owner_write:continue
        payment_writes=[w for w in path['writes'] if not keys(w['path']) and
            re.fullmatch(r'u?int\d*',value_type(w['path'],lookup) or '') and
            w['value'].get('kind')=='transaction_value']
        for w in payment_writes:
            for guard in path['guards']:
                # Do not flatten an OR: the comparison must be necessary for
                # this committing path, not a permissive alternative.
                def conjuncts(g):
                    return [x for a in g['args'] for x in conjuncts(a)] if g.get('op') in ('and','&&') else [g]
                for term in conjuncts(guard):
                    a=term.get('args',[])
                    if len(a)!=2:continue
                    payment,bid=(a[0],a[1]) if term.get('op')=='>' else (a[1],a[0]) if term.get('op')=='<' else ({},{})
                    if payment.get('kind')=='transaction_value' and key(bid)==key(w['path']):
                        found.append({'predicate':op('>',payment,bid),'kind':'paid_bid_acquires_same_authority',
                            'holder':subject,'payer':{'kind':'actual_sender'},'payment':payment,'bid':bid,
                            'path':pid,'source':w['source'],'business_basis':text})
    return unique(found)

````

