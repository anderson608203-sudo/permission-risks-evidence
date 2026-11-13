"""Bounded source path analysis, not an EVM or a symbolic execution backend.

Reuse compiler declaration resolution. Preserve branch polarity, modifier order,
write/guard order and reverting exits. Unsupported semantics remain named gaps.
"""
import copy
import json
import re
from .source_paths import SourcePaths
from .source_work_budget import visit as budget_visit


def clean(v):
    # Memo is local to this read-only traversal: it never survives mutation.
    from .source_work_budget import metric
    metric("clean_calls");memo={};remaining=50000;string_bytes=0
    def visit(value,depth):
        nonlocal remaining,string_bytes
        metric("max_depth",depth,True)
        if depth>100:raise ValueError('SOURCE_EXPRESSION_EXPANSION_LIMIT:nodes=50000,depth=100')
        ident=id(value)
        if isinstance(value,(dict,list)) and ident in memo:
            result,nodes,chars,subdepth=memo[ident];remaining-=nodes;string_bytes+=chars
            metric("shared_subtree_hits")
            if remaining<0 or depth+subdepth>100:raise ValueError('SOURCE_EXPRESSION_EXPANSION_LIMIT:nodes=50000,depth=100')
            if string_bytes>1048576:raise ValueError('SOURCE_EXPRESSION_STRING_LIMIT:bytes=1048576')
            return result
        budget_visit();remaining-=1
        if remaining<0:raise ValueError('SOURCE_EXPRESSION_EXPANSION_LIMIT:nodes=50000,depth=100')
        before=remaining;before_bytes=string_bytes
        if isinstance(value,str):
            string_bytes+=len(value.encode('utf8'))
            if string_bytes>1048576:raise ValueError('SOURCE_EXPRESSION_STRING_LIMIT:bytes=1048576')
        if isinstance(value,list):result=[visit(x,depth+1) for x in value]
        elif isinstance(value,dict):result={k:visit(x,depth+1) for k,x in value.items() if k not in ('label','name','source','index_source','origins')}
        else:return value
        # Depth is calculated from the already cleaned representation, not
        # by traversing the original symbolic state again.
        def child_depth(x):
            return memo[id(x)][3]+1 if isinstance(x,(dict,list)) and id(x) in memo else 1
        children=value.values() if isinstance(value,dict) else value
        subdepth=max((child_depth(x) for x in children),default=0)
        memo[ident]=(result,1+before-remaining,string_bytes-before_bytes,subdepth)
        return result
    result=visit(v,0);metric("max_expression_nodes",50000-remaining,True)
    return result

def _clean_key(v):
    text=json.dumps(v,sort_keys=True,separators=(',',':'))
    if len(text)>262144:raise ValueError('SOURCE_EXPRESSION_KEY_LIMIT:characters=262144')
    return text

def key(v):return _clean_key(clean(v))

def lit(v): return {'kind':'literal','value':v}
def op(name,*args): return {'kind':'op','op':name,'args':list(args)}


def walk(v):
    if isinstance(v,dict):
        yield v
        # Binding observations are provenance, not additional executable effects.
        for name,x in v.items():
            if name not in ('_source_value_bindings','_source_lvalue_bindings'):yield from walk(x)
    elif isinstance(v,list):
        for x in v: yield from walk(x)


from functools import lru_cache
@lru_cache(maxsize=256)
def _normalized_text(text):
    return _clean_key(_normalize_clean(json.loads(text)))

def normalize(v):
    try:text=key(v)
    except ValueError as error:
        # The text key bounds only optional memoization. Normalize the original
        # bounded expression directly if its serialized cache key is too large.
        # Core expression/depth/work limits still apply; no term is dropped.
        if not str(error).startswith('SOURCE_EXPRESSION_KEY_LIMIT:'):raise
        return _normalize_clean(clean(v))
    if len(text)>16384:return _normalize_clean(json.loads(text))
    before=_normalized_text.cache_info().hits
    result=_normalized_text(text)
    if _normalized_text.cache_info().hits>before:
        from .source_work_budget import metric
        metric("normalization_cache_hits")
    # A fresh value prevents callers changing cached objects.
    return json.loads(result)


def _normalize_clean(v):
    if not isinstance(v,dict) or v.get('kind')!='op': return v
    args=[_normalize_clean(x) for x in v['args']]; operator=v['op']
    if operator in ('and','&&','or','||'):
        conjunction=operator in ('and','&&');flat=[]
        for a in args:
            if a==lit(not conjunction):return a
            if a==lit(conjunction):continue
            if a.get('kind')=='op' and (a['op'] in ('and','&&') if conjunction else a['op'] in ('or','||')):flat.extend(a['args'])
            else:flat.append(a)
        args=list({_clean_key(x):x for x in flat}.values())
        if not args:return lit(conjunction)
        if len(args)==1:return args[0]
        operator='and' if conjunction else 'or'
    if len(args)==2:
        if operator in ('+','-','*') and all(x.get('kind')=='literal' and type(x.get('value')) is int for x in args):
            a,b=[x['value'] for x in args];return lit({'+':lambda:a+b,'-':lambda:a-b,'*':lambda:a*b}[operator]())
        if operator in ('<','<=','>','>='):
            a,b=args
            if a==b:return lit(operator in ('<=','>='))
            if all(x.get('kind')=='literal' and type(x.get('value')) is int for x in args):
                x,y=a['value'],b['value']
                return lit({'<':x<y,'<=':x<=y,'>':x>y,'>=':x>=y}[operator])
        if operator in ('+','-') and args[1]==lit(0):return args[0]
        if operator=='*' and args[1]==lit(1):return args[0]
        if operator=='*' and args[0]==lit(1):return args[1]
    if operator in ('==','!=') and len(args)==2:
        a,b=args
        if a==b:return lit(operator=='==')
        if a.get('kind')==b.get('kind')=='literal':return lit((a['value']==b['value'])==(operator=='=='))
        for a,b in (args,args[::-1]):
            if b.get('kind')=='literal' and isinstance(b.get('value'),bool):
                return a if b['value']==(operator=='==') else op('!',a)
        if operator=='!=':return op('!',_normalize_clean(op('==',*args)))
        args=sorted(args,key=_clean_key)
    if operator=='!' and args[0].get('kind')=='literal':return lit(not args[0]['value'])
    if operator=='!' and args[0].get('kind')=='op' and args[0]['op']=='!':return args[0]['args'][0]
    return op(operator,*args)


def dnf(expr, negative=False, limit=64):
    """Finite propositional expansion; unknown arithmetic is NOT solved."""
    return _dnf_normalized(normalize(expr),negative,limit)

def _dnf_normalized(e,negative=False,limit=64):
    if e.get('kind')=='literal' and isinstance(e.get('value'),bool):return [set()] if e['value']!=negative else []
    if e.get('kind')=='op':
        operator=e['op'];args=e['args']
        if operator=='!':return _dnf_normalized(args[0],not negative,limit)
        if operator in ('&&','and','||','or'):
            conjunction=(operator in ('&&','and'))!=negative
            result=[set()] if conjunction else []
            for a in args:
                pieces=_dnf_normalized(a,negative,limit)
                if conjunction:
                    result=[x|y for x in result for y in pieces if not any((k,not sign) in y for k,sign in x)]
                else: result+=pieces
                if len(result)>limit:raise ValueError('P_BOOLEAN_PATH_LIMIT')
            return result
    return [{(_clean_key(e),not negative)}]


def conditions_possible(guards, required=None):
    expr=op('and',*guards)
    if required is not None:expr=op('and',expr,op('!',required))
    def consistent(branch):
        parent={};terms={}
        atoms=[(json.loads(raw),positive) for raw,positive in branch]
        has_equality=any(positive and a.get('kind')=='op' and a['op']=='==' and all(x.get('kind') in ('actual_sender','parameter','storage','literal') for x in a['args']) for a,positive in atoms)
        for raw,_ in (branch if has_equality else []):
            for term in walk(json.loads(raw)):
                if 'kind' in term:terms[_clean_key(term)]=term
        if len(terms)>2048:raise ValueError('P_EQUALITY_TERM_LIMIT')
        def find(k):
            parent.setdefault(k,k)
            if parent[k]!=k:parent[k]=find(parent[k])
            return parent[k]
        def rank(k):
            # Prefer a known constant over its aliases; otherwise a numeric
            # constraint could survive as an unconstrained parameter predicate.
            return ({'literal':0,'actual_sender':1,'parameter':2,'storage':3}.get(json.loads(k).get('kind'),4),len(k),k)
        def union(x,y):
            x,y=find(x),find(y)
            if x==y:return False
            first,second=sorted((x,y),key=rank);parent[second]=first
            return True
        for term in terms:find(term)
        for raw,positive in branch:
            a=json.loads(raw)
            if positive and a.get('kind')=='op' and a['op']=='==' and all(x.get('kind') in ('actual_sender','parameter','storage','literal') for x in a['args']):
                x,y=map(_clean_key,a['args']);union(x,y)
        # A proven key equality also equates reads of the same storage family.
        # Finite congruence closure is needed before replacing whole terms:
        # sender==owners[y], x==y must imply sender==owners[x].
        def children(v):
            if isinstance(v,dict):
                if 'kind' in v:return {'equivalence_class':find(_clean_key(v))}
                return {k:children(x) for k,x in v.items()}
            return [children(x) for x in v] if isinstance(v,list) else v
        for _ in range(len(terms)+1):
            congruent={};changed=False
            for k,term in terms.items():
                signature=_clean_key({name:children(v) for name,v in term.items()})
                if signature in congruent:changed=union(k,congruent[signature]) or changed
                else:congruent[signature]=k
            if not changed:break
        else:raise ValueError('P_EQUALITY_CLOSURE_LIMIT')
        # Equating a variable to two distinct constants is a contradiction,
        # even though representative substitution would erase that difference.
        constants={}
        for term in list(parent):
            value=json.loads(term)
            if value.get('kind')=='literal':constants.setdefault(find(term),set()).add(term)
        if any(len(values)>1 for values in constants.values()):return False
        def replace(v,active=frozenset()):
            k=_clean_key(v)
            if k in active:raise ValueError('P_CYCLIC_EQUALITY_NOT_LOWERED')
            nested=active|{k}
            if k in parent and find(k)!=k:return replace(json.loads(find(k)),nested)
            if isinstance(v,dict):return {k:replace(x,nested) if isinstance(x,(dict,list)) else x for k,x in v.items()}
            return [replace(x,nested) for x in v] if isinstance(v,list) else v
        seen=set();bounds={}
        for raw,positive in branch:
            a=normalize(replace(json.loads(raw)))
            if a.get('kind')=='literal' and isinstance(a.get('value'),bool):
                if a['value']!=positive:return False
                continue
            k=_clean_key(a)
            if (k,not positive) in seen:return False
            seen.add((k,positive))
            if a.get('kind')=='op' and a['op'] in ('<','<=','>','>='):
                x,y=a['args'];cmp=a['op']
                if x.get('kind')=='literal':
                    x,y=y,x;cmp={'<':'>','<=':'>=','>':'<','>=':'<='}[cmp]
                if y.get('kind')=='literal' and isinstance(y.get('value'),int) and x.get('kind')=='parameter':
                    if not positive:cmp={'<':'>=','<=':'>','>':'<=','>=':'<'}[cmp]
                    lo,hi=bounds.get(_clean_key(x),(0 if str(x.get('type','')).startswith('uint') else None,None))
                    v=y['value']
                    if cmp in ('>','>='):lo=max(lo if lo is not None else v-1,v+(cmp=='>'))
                    else:hi=min(hi if hi is not None else v+1,v-(cmp=='<'))
                    if lo is not None and hi is not None and lo>hi:return False
                    bounds[_clean_key(x)]=(lo,hi)
        return True
    # Search one conjunction at a time. Eager DNF multiplied unrelated ORs
    # even when the first satisfying branch or a direct contradiction sufficed.
    # Keep exactly the previous atom/equality/arithmetic abstraction.
    work=0;stack=[([(normalize(expr),False)],set())]
    while stack:
        pending,atoms=stack.pop()
        while pending:
            work+=1
            if work>20000:raise ValueError('P_BOOLEAN_SEARCH_LIMIT:20000')
            node,neg=pending.pop()
            if node.get('kind')=='literal' and isinstance(node.get('value'),bool):
                if node['value']==neg:break
                continue
            if node.get('kind')=='op':
                name=node['op'];args=node['args']
                if name=='!':pending.append((args[0],not neg));continue
                if name in ('and','&&','or','||'):
                    if (name in ('and','&&'))!=neg:
                        children=[(a,neg) for a in args]
                        children.sort(key=lambda x:x[0].get('kind')=='op' and x[0].get('op') in ('or','||','and','&&'),reverse=True)
                        pending.extend(children);continue
                    for a in reversed(args):stack.append((pending+[(a,neg)],set(atoms)))
                    break
            atom=(_clean_key(node),not neg)
            if (atom[0],not atom[1]) in atoms:break
            atoms.add(atom)
        else:
            if consistent(atoms):return True
    return False


class Paths(SourcePaths):
    def __init__(self,bundle,contract,max_paths=48):
        super().__init__(bundle,contract)
        self.limit=max_paths;self.sender={'kind':'actual_sender'}
        self.reads=[];self.writes=[];self.guards=[];self.calls=[];self.unknown=[];self.stack=[]
        self.calldata={'kind':'source_calldata_bytes','scope':'opaque source calldata; content and ABI decoding not modeled'}
        self.current=None
        from .m03_p_calls import ReadCalls
        self.read_calls=ReadCalls(self)

    def evaluate(self,n,env):
        if n and n.get('nodeType')=='V16EvaluatedValue':return copy.deepcopy(n['value'])
        from .m11_language import rational_constant
        from .source_entry_identity import builtin_object
        if (n and n.get('nodeType')=='Identifier' and n.get('name')=='now'
                and type(n.get('referencedDeclaration')) is int
                and n['referencedDeclaration'] not in self.nodes
                and n.get('typeDescriptions',{}).get('typeIdentifier')=='t_uint256'):
            return {'kind':'environment','field':'timestamp','type':'uint256'}
        if (n and n.get('nodeType')=='MemberAccess' and n.get('memberName') in ('number','timestamp')
                and builtin_object(n.get('expression',{}),self,'block')):
            return {'kind':'environment','field':n['memberName'],'type':'uint256'}
        if n and n.get('nodeType')=='MemberAccess' and n.get('memberName')=='length':
            data=n.get('expression',{})
            if (data.get('nodeType')=='MemberAccess' and data.get('memberName')=='data'
                    and builtin_object(data.get('expression',{}),self,'msg')):
                return {'kind':'source_calldata_length','type':'uint256','source':self.anchor(n)}
        if (n and n.get('nodeType')=='MemberAccess' and n.get('memberName')=='sig'
                and builtin_object(n.get('expression',{}),self,'msg')):
            selector=getattr(self,'_entry_selector',None)
            if selector is not None:return lit(selector)
            return {'kind':'unknown','reason':'actual_entry_selector_not_bound'}
        constant=rational_constant(n)
        if constant is not None and constant.denominator==1:return lit(constant.numerator)
        if n and n.get('nodeType')=='Identifier' and n.get('referencedDeclaration') not in env:
            from .m11_language import source_fixed_storage
            fixed=source_fixed_storage(self,n.get('referencedDeclaration'))
            if fixed is not None:return fixed
        if n and (n.get('nodeType')=='Conditional' or n.get('nodeType')=='BinaryOperation' and n.get('operator') in ('&&','||')):
            if any(x.get('nodeType')=='Assignment' or x.get('nodeType')=='UnaryOperation' and x.get('operator') in ('++','--','delete') for x in walk(n)):
                self.current['issues'].append({'reason':'conditional_side_effect_not_lowered','source':self.anchor(n)})
                return {'kind':'unknown','reason':'conditional_side_effect_not_lowered'}
        if n and n.get('nodeType')=='Assignment':
            value=self.value(n['rightHandSide'],env)
            return self.put(n['leftHandSide'],value,self.current,n,n['operator'])
        if n and n.get('nodeType')=='MemberAccess' and n.get('expression',{}).get('name')=='tx' and n.get('memberName')=='origin':
            return {'kind':'transaction_origin','type':'address'}
        if n and n.get('nodeType')=='Literal' and n.get('kind')=='number':
            from fractions import Fraction
            text=n['value'].replace('_','')
            number=Fraction(int(text,16)) if text.lower().startswith('0x') else Fraction(text)
            units={'wei':1,'szabo':10**12,'finney':10**15,'gwei':10**9,'ether':10**18,'seconds':1,'minutes':60,'hours':3600,'days':86400,'weeks':604800,'years':31536000}
            unit=n.get('subdenomination')
            if unit:
                if unit not in units:raise ValueError('P_LITERAL_UNIT_NOT_LOWERED:'+unit)
                number*=units[unit]
            if number.denominator!=1:raise ValueError('P_FRACTIONAL_LITERAL_NOT_LOWERED')
            return lit(number.numerator)
        if (n and n.get('nodeType')=='UnaryOperation'
                and n.get('operator') in ('++','--')
                and n.get('subExpression',{}).get('nodeType')=='Identifier'
                and n['subExpression'].get('referencedDeclaration') in env):
            from .typed_integer import integer_type,checked_mode
            typ=n.get('typeDescriptions',{}).get('typeString','')
            ident=n['subExpression']['referencedDeclaration'];before=env[ident]
            if integer_type(typ) and before.get('kind')=='literal' and type(before.get('value')) is int and not checked_mode(self,self.current):
                from .source_local_defaults import cast_constant
                after=cast_constant(typ,lit(before['value']+(1 if n['operator']=='++' else -1)))
                env[ident]=after
                self.current.setdefault('exact_constant_arithmetic',[]).append({'source':self.anchor(n),'before':copy.deepcopy(before),'after':copy.deepcopy(after),'compiler_wrapping':True})
                return copy.deepcopy(after if n.get('prefix') else before)
        if n and n.get('nodeType')=='UnaryOperation' and n.get('operator') in ('++','--'):
            before=self.value(n['subExpression'],env)
            self.put(n['subExpression'],lit(1),self.current,n,'+=' if n['operator']=='++' else '-=')
            return normalize(op('+' if n['operator']=='++' else '-',before,lit(1))) if n.get('prefix') else before
        if n and n.get('nodeType')=='MemberAccess' and n.get('memberName')=='length':
            base=self.value(n['expression'],env)
            typ=n['expression'].get('typeDescriptions',{}).get('typeString','')
            fixed=re.search(r'\[(\d+)\]',typ)
            if fixed and typ.count('[')==1:return lit(int(fixed[1]))
            if base.get('kind')=='array':return lit(len(base['items']))
            if base.get('kind')=='storage' and '[' in typ:
                path={**base,'segments':base.get('segments',[])+[{'length':True}]}
                return next((copy.deepcopy(w['value']) for w in reversed(self.current['writes']) if key(w['path'])==key(path)),path)
            if base.get('kind')=='parameter' and '[' in base.get('type',''):
                return {'kind':'array_length','array':base,'type':'uint256'}
        # solc uses TupleExpression for ordinary parentheses as well as tuples.
        # Only a non-array singleton is transparent. Do this at the AST boundary
        # so guards, index keys, casts, aliases and assignment targets agree.
        if n and n.get('nodeType')=='TupleExpression':
            parts=n.get('components',[])
            if not n.get('isInlineArray',False) and len(parts)==1 and parts[0] is not None:
                return self.evaluate(parts[0],env)
            return {'kind':'array' if n.get('isInlineArray',False) else 'tuple',
                    'items':[self.value(v,env) if v else lit(None) for v in parts]}
        if n and n.get('nodeType')=='IndexAccess':
            base=self.evaluate(n['baseExpression'],env);index=self.value(n.get('indexExpression'),env)
            if base.get('kind')=='array':
                if index.get('kind')=='literal' and type(index.get('value')) is int and 0<=index['value']<len(base['items']):
                    return copy.deepcopy(base['items'][index['value']])
                self.current['issues'].append({'reason':'memory_array_symbolic_or_oob_index','source':self.anchor(n)})
                return {'kind':'unknown','reason':'memory_array_symbolic_or_oob_index'}
        if n and n.get('nodeType')=='FunctionCall':
            f=n.get('expression',{})
            if f.get('nodeType')=='MemberAccess' and f.get('memberName')=='push':
                receiver=f.get('expression',{});typ=receiver.get('typeDescriptions',{}).get('typeString','')
                args=n.get('arguments',[])
                if '[]' in typ and typ.count('[')==1 and len(args)==1:
                    base=self.evaluate(receiver,env)
                    if base.get('kind')=='storage':
                        length={**base,'segments':base.get('segments',[])+[{'length':True}]}
                        before=next((copy.deepcopy(w['value']) for w in reversed(self.current['writes']) if key(w['path'])==key(length)),length)
                        value=self.value(args[0],env)
                        self.current['guards'].append(op('<',before,lit(2**256-1)))
                        self.current['writes'].extend([
                            {'path':{**base,'segments':base.get('segments',[])+[{'key':copy.deepcopy(before)}]},'value':value,'operator':'=','source':self.anchor(n)},
                            {'path':length,'value':op('+',before,lit(1)),'operator':'=','source':self.anchor(n)}])
                        return op('+',before,lit(1))

            if f.get('nodeType')=='MemberAccess' and f.get('expression',{}).get('name')=='abi' and f.get('memberName') in ('encode','encodePacked'):
                args=[self.value(x,env) for x in n.get('arguments',[])]
                types=[x.get('typeDescriptions',{}).get('typeString','') for x in n.get('arguments',[])]
                if f['memberName']=='encodePacked' and any('[' in typ or typ in ('bytes','string') for typ in types):
                    self.current['issues'].append({'reason':'packed_dynamic_encoding_not_lowered','source':self.anchor(n)})
                    return {'kind':'unknown','reason':'packed_dynamic_encoding_not_lowered'}
                return {'kind':'abi_encoding','mode':f['memberName'],'types':types,'arguments':args}
            if f.get('nodeType')=='Identifier' and f.get('name')=='keccak256':
                args=[self.value(x,env) for x in n.get('arguments',[])]
                if len(args)==1:return {'kind':'hash','algorithm':'keccak256','input':args[0], 'type':'bytes32'}
            if n.get('kind')=='typeConversion' and len(n.get('arguments',[]))==1:
                from .source_entry_identity import elementary_expression_name
                typ=elementary_expression_name(f);source=n['arguments'][0]
                from .source_local_defaults import cast_constant
                from .source_scalar_semantics import constant_integer
                raw=constant_integer(source)
                if raw is not None:
                    converted=cast_constant(typ,lit(raw))
                    if converted is not None:return converted
                src_type=source.get('typeDescriptions',{}).get('typeString','')
                target_bits=re.fullmatch(r'uint(\d*)',typ);source_bits=re.fullmatch(r'uint(\d*)',src_type)
                if target_bits and source_bits:
                    a=int(source_bits[1] or 256);b=int(target_bits[1] or 256);value=self.value(source,env)
                    if b<a:
                        if value.get('kind')=='literal':return lit(value['value']%(2**b))
                        if not conditions_possible(self.current['guards'],op('<',value,lit(2**b))):return value
                        return {'kind':'uint_narrow','bits':b,'from_bits':a,'input':value,'type':typ}
                    return value

            if n.get('kind') not in ('typeConversion','structConstructorCall'):
                if f.get('nodeType')=='MemberAccess' and f.get('memberName') in ('wrap','unwrap'):
                    return self.value(n['arguments'][0],env)
                from .m11_calls import expression_call
                result=expression_call(self,n,env)
                if result is not None:return result
                result=self.read_calls.call(n,env)
                if result is not None:return result
                self.current['issues'].append({'reason':'expression_call_not_lowered','source':self.anchor(n)})
                return {'kind':'unknown','reason':'expression_call_not_lowered'}
        if n and n.get('nodeType')=='MemberAccess':
            from .source_local_values import local_root
            if local_root(n.get('expression',{}),self) is not None:
                base=self.evaluate(n.get('expression'),env)
                if base.get('kind')=='record':
                    field=next((f for f in base['fields'] if f['field']==n.get('referencedDeclaration')),None)
                    if field is not None:return copy.deepcopy(field['value'])
            member=self.nodes.get(n.get('referencedDeclaration'),{})
            if member.get('nodeType')=='EnumValue':
                enums=[e for e in self.nodes.values() if e.get('nodeType')=='EnumDefinition' and any(x.get('id')==member['id'] for x in e.get('members',[]))]
                if len(enums)==1:return lit(next(i for i,x in enumerate(enums[0]['members']) if x['id']==member['id']))
        if n and n.get('nodeType')=='Identifier' and n.get('name')=='this':
            return self.read_calls.address()
        result=super().evaluate(n,env)
        if n and n.get('nodeType') in ('Identifier','IdentifierPath') and result.get('kind')=='storage' and n.get('referencedDeclaration') not in env:
            result=self.read_calls.state(result,n.get('referencedDeclaration'))
        return result

    def value(self,n,env):
        v=self.evaluate(n,env)
        # A local value was captured when assigned. Reading the local again
        # must not re-read a state root changed since then (e.g. a saved ID).
        if n and n.get('nodeType')=='Identifier' and n.get('referencedDeclaration') in env:
            v=copy.deepcopy(v)
        elif v.get('kind')=='storage':
            from .m10_storage_alias import read_after_writes
            v=read_after_writes(v,self.current['writes'],self.current['guards'])
        v=normalize(v)
        from .m16_source_bindings import observe
        observe(self.current,n,v,env)
        return v

    def expr(self,n,s):
        self.current=s
        try:return self.value(n,s['env'])
        except (KeyError,ValueError,TypeError) as ex:
            s['issues'].append({'reason':'expression_unresolved','detail':str(ex),'source':self.anchor(n) if n else None})
            return {'kind':'unknown','reason':'expression_unresolved'}

    def left(self,n,s):
        self.current=s
        value=self.evaluate(n,s['env'])
        from .m16_source_bindings import observe_lvalue
        observe_lvalue(s,n,value)
        return value

    def put(self,n,value,s,source,operator='='):
        from .source_local_defaults import constant_local_update
        constant=constant_local_update(self,n,value,s,source,operator)
        if constant is not None:return constant
        if n.get('nodeType')=='TupleExpression' and not n.get('isInlineArray',False):
            parts=n.get('components',[])
            if len(parts)==1 and parts[0] is not None:return self.put(parts[0],value,s,source,operator)
            if operator!='=' or value.get('kind')!='tuple' or len(parts)!=len(value.get('items',[])):
                s['issues'].append({'reason':'tuple_assignment_shape_not_lowered','source':self.anchor(source)})
                return {'kind':'unknown','reason':'tuple_assignment_shape_not_lowered'}
            # Solidity evaluates the RHS before any LHS is written. Restrict
            # this summary to distinct locals; aliased storage needs ordering.
            locals_=[p.get('referencedDeclaration') for p in parts if p]
            if len(locals_)!=len(set(locals_)) or any(p and (p.get('nodeType')!='Identifier' or p.get('referencedDeclaration') not in s['env']) for p in parts):
                s['issues'].append({'reason':'tuple_assignment_storage_or_alias_not_lowered','source':self.anchor(source)})
                return {'kind':'unknown','reason':'tuple_assignment_storage_or_alias_not_lowered'}
            for part,item in zip(parts,copy.deepcopy(value['items'])):
                if part:s['env'][part['referencedDeclaration']]=item
            return copy.deepcopy(value)
        if any(x.get('nodeType')=='Assignment' or x.get('nodeType')=='FunctionCall' and not (x.get('kind')=='typeConversion' and len(x.get('arguments',[]))==1) or x.get('nodeType')=='UnaryOperation' and x.get('operator') in ('++','--','delete') for x in walk(n)):
            s['issues'].append({'reason':'assignment_lvalue_side_effects_not_lowered','source':self.anchor(source)})
            return {'kind':'unknown','reason':'assignment_lvalue_side_effects_not_lowered'}
        from .source_local_values import local_root,assign
        local_composite=local_root(n,self)
        if local_composite is not None and n.get('nodeType')!='Identifier':
            try:
                if operator not in ('=','delete'):value=normalize(op(operator[:-1],self.left(n,s),value))
                if operator=='delete':value=lit(0)
                assign(n,value,self,s);return copy.deepcopy(value)
            except (ValueError,KeyError,TypeError) as error:
                s['issues'].append({'reason':str(error),'source':self.anchor(source)})
                return {'kind':'unknown','reason':str(error)}
        lhs=self.left(n,s)
        decl=self.nodes.get(n.get('referencedDeclaration'),{})
        local_value=(n.get('nodeType')=='Identifier' and not decl.get('stateVariable')
                     and decl.get('storageLocation')!='storage'
                     and n.get('referencedDeclaration') in s['env'])
        if local_value:
            if operator not in ('=','delete'):
                value=normalize(op(operator[:-1],copy.deepcopy(lhs),value))
            if operator=='delete':
                typ=decl.get('typeDescriptions',{}).get('typeString','')
                value=lit(False) if typ=='bool' else lit(0) if re.fullmatch(r'(?:u?int\d*|address(?: payable)?|bytes\d+)',typ) else {'kind':'unknown','reason':'local_delete_type_not_lowered'}
            s['env'][n['referencedDeclaration']]=copy.deepcopy(value)
            from .m16_source_bindings import observe
            observe(s,decl,value,s['env'])
        elif lhs.get('kind')=='storage':
            from .m10_storage_alias import read_after_writes
            before=read_after_writes(lhs,s['writes'],s['guards'])
            increment=None
            if operator in ('+=','-='):increment=value if operator=='+=' else op('-',lit(0),value)
            if operator not in ('=','delete'):value=normalize(op(operator[:-1],before,value))
            if operator=='delete':value={'kind':'zero_of_storage_type'}
            # Record the sequential read as well as the local additive effect.
            # Consumers must not subtract a pre-transaction slot from a later read.
            if operator=='=' and value.get('kind')=='op' and value.get('op') in ('+','-') and key(value['args'][0])==key(before):
                increment=value['args'][1] if value['op']=='+' else op('-',lit(0),value['args'][1])
            s['writes'].append({'path':clean(lhs),'value':value,'operator':operator,'source':self.anchor(source),
                'local_increment':copy.deepcopy(increment)})
        elif n.get('nodeType')=='Identifier':
            if operator not in ('=','delete'):value=normalize(op(operator[:-1],copy.deepcopy(lhs),value))
            s['env'][n['referencedDeclaration']]=value
        else:
            s['issues'].append({'reason':'assignment_target_not_lowered','source':self.anchor(source)})
            return {'kind':'unknown','reason':'assignment_target_not_lowered'}
        return copy.deepcopy(value)

    def statements(self,stmts,states,depth):
        for n in stmts:
            out=[]
            for s in states:
                out.extend(self.statement(n,s,depth) if s['flow']=='normal' else [s])
            if len(out)>self.limit:raise ValueError('P_SOURCE_PATH_LIMIT')
            states=out
        return states

    def event_statement(self,call,s):
        declaration=self.nodes.get((call or {}).get('expression',{}).get('referencedDeclaration'),{})
        if not call or call.get('nodeType')!='FunctionCall' or declaration.get('nodeType')!='EventDefinition':
            s['issues'].append({'reason':'event_declaration_not_bound','source':self.anchor(call) if call else None})
            return [s]
        arguments=call.get('arguments',[])
        if len(arguments)!=len(declaration.get('parameters',{}).get('parameters',[])):
            s['issues'].append({'reason':'event_argument_arity','source':self.anchor(call)})
        if any(n.get('nodeType')=='Assignment' or
                n.get('nodeType')=='UnaryOperation' and n.get('operator') in ('++','--','delete') for n in walk(arguments)):
            s['issues'].append({'reason':'event_argument_side_effect_not_fully_lowered','source':self.anchor(call)})
        if any(n.get('nodeType')=='IndexAccess' and n.get('baseExpression',{}).get('typeDescriptions',{}).get('typeIdentifier','').startswith(('t_array','t_bytes','t_string')) for n in walk(arguments)):
            s['issues'].append({'reason':'event_argument_array_bounds_not_lowered','source':self.anchor(call)})
        values=[]
        for argument in arguments:
            value=self.expr(argument,s);values.append(value)
            # Evaluation must not vanish because an event's return is unused.
            # Ordinary P queries do not yet encode every unused fallible term;
            # keep this limited case explicitly unresolved rather than ignore it.
            if any(v.get('kind') in ('unknown','call_unresolved','uint_narrow','enum_cast','index') or
                    v.get('kind')=='op' and v.get('op') in ('+','-','*','/','%','**','<<','>>') and not getattr(self,'captures_evaluated_terms',False) for v in walk(value)):
                s['issues'].append({'reason':'event_argument_fallible_value_not_lowered','source':self.anchor(argument)})
        s.setdefault('source_events',[]).append({'source':self.anchor(call),'declaration_ast_id':declaration['id'],
            'arguments':clean(values),'event_not_used_as_effect_proof':True})
        return [s]

    def statement(self,n,s,depth):
        if not n:return [s]
        kind=n.get('nodeType')
        if kind=='InlineAssembly':
            from .m21_bytes import summarize
            pure_reads=summarize(self,n,s)
            if pure_reads is not None:return pure_reads
            from .m20_assembly import forward
            summarized=forward(self,n,s)
            if summarized is not None:return summarized
        from .m11_calls import expand_value_statement
        expanded=expand_value_statement(self,n,s,depth)
        if expanded is not None:return expanded
        if kind in ('Block','UncheckedBlock'):
            if kind=='UncheckedBlock' and not getattr(self,'captures_evaluated_terms',False):
                s['issues'].append({'reason':'unchecked_arithmetic_scope','source':self.anchor(n)})
            previous=s.get('_unchecked_depth',0)
            if kind=='UncheckedBlock':
                s['_unchecked_depth']=previous+1
                s.setdefault('arithmetic_scope',[]).append({'source':self.anchor(n),'scope':'nonwrapping_uint256_subcase; narrow signed types retain exact modular arithmetic','overflow_cases_not_exhausted':True})
            result=self.statements(n.get('statements',[]),[s],depth)
            if kind=='UncheckedBlock':
                for branch in result:branch['_unchecked_depth']=previous
            return result
        if kind=='IfStatement':
            c=self.expr(n['condition'],s);out=[]
            for sign,body in [(True,n.get('trueBody')),(False,n.get('falseBody'))]:
                child=copy.deepcopy(s);child['guards'].append(c if sign else op('!',c))
                child.setdefault('branch_choices',[]).append({'condition':copy.deepcopy(c),'sign':sign,'source':self.anchor(n)})
                if conditions_possible(child['guards']):out+=self.statement(body,child,depth)
            return out
        if kind in ('ForStatement','WhileStatement'):
            states=self.statement(n.get('initializationExpression'),s,depth)
            from .source_loop_scope import loop_limit
            bound=max(loop_limit(n,self,x) for x in states) if states else 0
            from .source_loop_scope import invariant_local_condition
            invariant=invariant_local_condition(n,self)
            if invariant:bound=0
            completed=[]
            for iteration in range(bound+1):
                next_states=[]
                for current in states:
                    condition=self.expr(n.get('condition'),current) if n.get('condition') else lit(True)
                    stop=copy.deepcopy(current);stop['guards'].append(op('!',condition))
                    stop.setdefault('loop_scopes',[]).append({'source':self.anchor(n),'iterations':iteration,'complete_loop':True})
                    if conditions_possible(stop['guards']):completed.append(stop)
                    active=copy.deepcopy(current);active['guards'].append(condition)
                    if not conditions_possible(active['guards']):continue
                    if iteration==bound:
                        active['issues'].append({'reason':'source_loop_bound_exceeded','source':self.anchor(n),'unrolled_iterations':bound,**({'loop_condition_invariant':True,'reason_detail':'local boolean unchanged; no successful exit in compiled loop body'} if invariant else {})})
                        active['flow']='truncated';completed.append(active);continue
                    for body in self.statement(n.get('body'),active,depth):
                        if body['flow'] in ('normal','continue'):
                            body['flow']='normal';next_states.extend(self.statement(n.get('loopExpression'),body,depth))
                        elif body['flow']=='break':
                            body['flow']='normal';completed.append(body)
                        else:completed.append(body)
                if len(completed)+len(next_states)>self.limit:raise ValueError('P_SOURCE_PATH_LIMIT')
                states=next_states
            return completed
        if kind in ('Break','Continue'):s['flow']=kind.lower();return [s]
        if kind in ('RevertStatement','Throw'):s['flow']='reverted';return [s]
        if kind=='Return':
            if n.get('expression'):
                value=self.expr(n['expression'],s);s['return_value']=value
                ids=s.get('_return_ids',[])
                values=[value] if len(ids)==1 else value.get('items',[]) if value.get('kind')=='tuple' else []
                if len(values)!=len(ids):s['issues'].append({'reason':'function_return_arity_not_lowered','source':self.anchor(n)})
                else:
                    for ident,returned in zip(ids,values):s['env'][ident]=copy.deepcopy(returned)
            s['flow']='returned';return [s]
        if kind=='ModifierContinuation':
            results=self.statement(n['body'],s,depth)
            for result in results:
                if result['flow']=='returned' and not result.get('_evm_halted'):
                    result['flow']='normal';result['_return_pending']=True
            return results
        if kind=='EmitStatement':return self.event_statement(n.get('eventCall'),s)
        if kind=='PlaceholderStatement':return [s]
        if kind=='VariableDeclarationStatement':
            v=self.expr(n.get('initialValue'),s)
            ds=n['declarations']
            for i,d in enumerate(ds):
                if d:
                    value=v if len(ds)==1 else copy.deepcopy(v['items'][i]) if v.get('kind')=='tuple' and len(v.get('items',[]))==len(ds) else {'kind':'unknown','reason':'tuple_local_arity'}
                    if n.get('initialValue') is None:
                        typ=d.get('typeDescriptions',{}).get('typeString','')
                        value=lit(False) if typ=='bool' else lit(0) if typ.startswith(('uint','int','address','bytes')) and '[' not in typ else {'kind':'unknown','reason':'uninitialized_local_type_not_lowered'}
                    if d.get('storageLocation')=='memory' and value.get('kind')=='storage':
                        from .source_local_values import snapshot
                        try:value=snapshot(value,d.get('typeName',{}),self,s)
                        except ValueError as error:
                            s['issues'].append({'reason':str(error),'source':self.anchor(n)});value={'kind':'unknown','reason':str(error)}
                    s['env'][d['id']]=value
                    if n.get('initialValue') is not None:
                        from .m16_source_bindings import observe
                        observe(s,d,value,s['env'])
            return [s]
        if kind=='ExpressionStatement':
            e=n['expression'];k=e.get('nodeType')
            if k=='Assignment':self.put(e['leftHandSide'],self.expr(e['rightHandSide'],s),s,e,e['operator']);return [s]
            if k=='UnaryOperation' and e.get('operator') in ('++','--','delete'):
                self.put(e['subExpression'],lit(1),s,e,{'++':'+=','--':'-=','delete':'delete'}[e['operator']]);return [s]
            if k=='FunctionCall':
                f=e['expression'];name=f.get('name')
                if self.nodes.get(f.get('referencedDeclaration'),{}).get('nodeType')=='EventDefinition':
                    return self.event_statement(e,s)
                from .source_entry_identity import builtin_call
                if builtin_call(e,self):
                    s['guards'].append(self.expr(e['arguments'][0],s))
                    if not conditions_possible(s['guards']):s['flow']='reverted'
                    return [s]
                if builtin_call(e,self,('revert',)):s['flow']='reverted';return [s]
                target=self.fns.get(f.get('referencedDeclaration'))
                from .m11_calls import bound_library
                if bound_library(self,e,target):
                    return self.invoke(target,[self.expr(f['expression'],s)]+[self.expr(x,s) for x in e['arguments']],s,depth+1,internal=True)
                if target and f.get('nodeType')=='MemberAccess':
                    from .m10_dispatch import member_target
                    selected=member_target(self,e,target)
                    if selected:
                        return self.invoke(selected,[self.expr(x,s) for x in e['arguments']],s,depth+1,internal=True)
                if target and f.get('nodeType')=='Identifier':
                    from .m11_calls import bind_arguments
                    bound_args=bind_arguments(self,e,target)
                    if bound_args is None:
                        s['issues'].append({'reason':'named_internal_arguments_not_bound','source':self.anchor(e)})
                        return [s]
                    from .m10_dispatch import resolve
                    selected=resolve(self,target,self.read_calls.active_contract)
                    s.setdefault('internal_dispatch',[]).append({'source':self.anchor(e),'referenced':self.anchor(target),'selected':self.anchor(selected),'basis':'compiler_C3_unqualified_internal_call'})
                    return self.invoke(selected,[self.expr(x,s) for x in bound_args],s,depth+1,internal=True)
            self.expr(e,s);return [s]
        s['issues'].append({'reason':'statement_not_lowered','kind':kind,'source':self.anchor(n)})
        return [s]

    def invoke(self,f,args,s,depth=0,internal=False):
        if depth>8:raise ValueError('P_CALL_DEPTH_LIMIT')
        outer_return={k:copy.deepcopy(s[k]) for k in ('_return_ids','_return_pending','return_value') if k in s}
        for name in outer_return:s.pop(name,None)
        outer=copy.deepcopy(s['env']);s['env']={p['id']:a for p,a in zip(f['parameters']['parameters'],args)}
        body=copy.deepcopy(f.get('body'))
        from .source_local_defaults import forward_local_defaults
        for identity,value in forward_local_defaults(self,f).items():
            s['env'].setdefault(identity,copy.deepcopy(value))
        return_parameters=f.get('returnParameters',{}).get('parameters',[])
        s['_return_ids']=[parameter['id'] for parameter in return_parameters]
        for parameter in return_parameters:
            typ=parameter.get('typeDescriptions',{}).get('typeString','')
            s['env'][parameter['id']]=lit(False) if typ=='bool' else lit(0) if typ.startswith(('uint','int','address','bytes')) and '[' not in typ else {'kind':'unknown','reason':'return_default_type_not_lowered'}
        # Expand modifier placeholders in their actual enclosing order.
        for m in reversed(f.get('modifiers',[])):
            mod=self.fns.get(m['modifierName'].get('referencedDeclaration'))
            if not mod or mod.get('nodeType')!='ModifierDefinition':
                s['issues'].append({'reason':'modifier_not_lowered'});continue
            for p,a in zip(mod['parameters']['parameters'],m.get('arguments') or []):s['env'][p['id']]=self.expr(a,s)
            replacement=body
            def expand(v):
                if isinstance(v,dict):
                    if v.get('nodeType')=='PlaceholderStatement':return {'nodeType':'ModifierContinuation','body':copy.deepcopy(replacement)}
                    return {k:expand(x) for k,x in v.items()}
                return [expand(x) for x in v] if isinstance(v,list) else v
            body=expand(mod['body'])
        results=self.statement(body,s,depth)
        for item in results:
            if item['flow'] not in ('normal','returned'):continue
            if return_parameters:
                values=[copy.deepcopy(item['env'][p['id']]) for p in return_parameters]
                item['return_value']=values[0] if len(values)==1 else {'kind':'tuple','items':values}
            if item.pop('_return_pending',False) or return_parameters:item['flow']='returned'
        if internal:
            for item in results:
                item['env']=copy.deepcopy(outer)
                if item['flow']=='returned' and not item.get('_evm_halted'):item['flow']='normal'
                for name in ('_return_ids','_return_pending','return_value'):item.pop(name,None)
                item.update(copy.deepcopy(outer_return))
        return results

    def run(self,signature):
        f=self.function(signature)
        if not f or 'generated_getter' in f:return []
        self._entry_selector=self.function_selector(f)
        args=[{'kind':'parameter','id':p['id'],'type':p.get('typeDescriptions',{}).get('typeString')} for p in f['parameters']['parameters']]
        state={'env':{},'guards':[],'writes':[],'issues':[],'flow':'normal'}
        self.unknown=[]
        result=self.invoke(f,args,state)
        for s in result:
            s['issues']+=self.unknown
            s.pop('env',None)
            s['entry_source']=self.anchor(f)
        return result
