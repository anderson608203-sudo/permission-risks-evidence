"""Compiler-version-scoped defaults and exact constant integer conversions."""
import re

def scalar_default(declaration):
    typ=declaration.get('typeDescriptions',{}).get('typeString','')
    if typ=='bool':return {'kind':'literal','value':False}
    if re.fullmatch(r'(?:u?int\d*|address(?: payable)?|bytes\d+)',typ):return {'kind':'literal','value':0}
    return {'kind':'unknown','reason':'local_default_type_not_lowered'}

def function_scoped_locals(lookup):
    raw=lookup.bundle.get('compiler',{})
    text=raw.get('version',raw.get('compiler_version','')) if isinstance(raw,dict) else str(raw)
    if not text:text=str(lookup.bundle.get('compiler_version',''))
    m=re.search(r'(\d+)\.(\d+)\.(\d+)',text)
    return bool(m and tuple(map(int,m.groups()))<(0,5,0))

def cast_constant(typ,value):
    from .typed_integer import integer_type
    integer=integer_type(typ)
    if integer is None or value.get('kind')!='literal' or type(value.get('value')) is not int:return None
    signed,bits=integer;result=value['value']%(2**bits)
    if signed and result>=2**(bits-1):result-=2**bits
    return {'kind':'literal','value':result}


def constant_local_update(lookup,node,value,state,source,operator):
    from .typed_integer import integer_type,checked_mode
    import copy
    if node.get('nodeType')!='Identifier' or operator not in ('+=','-=','*='):return None
    ref=node.get('referencedDeclaration');before=state.get('env',{}).get(ref,{})
    decl=lookup.nodes.get(ref,{})
    typ=decl.get('typeDescriptions',{}).get('typeString','')
    if decl.get('stateVariable') or decl.get('storageLocation')=='storage' or integer_type(typ) is None:return None
    if not all(v.get('kind')=='literal' and type(v.get('value')) is int for v in (before,value)):return None
    if checked_mode(lookup,state):return None
    a,b=before['value'],value['value'];raw={'+=':lambda:a+b,'-=':lambda:a-b,'*=':lambda:a*b}[operator]()
    result=cast_constant(typ,{'kind':'literal','value':raw});state['env'][ref]=copy.deepcopy(result)
    from .m16_source_bindings import observe
    observe(state,decl,result,state['env'])
    state.setdefault('exact_constant_arithmetic',[]).append({'source':lookup.anchor(source),'before':copy.deepcopy(before),'after':copy.deepcopy(result),'compiler_wrapping':True})
    return result


def forward_local_defaults(lookup,function):
    """Cache immutable AST facts; initialize only locals used before declaration.

    Ordinary declarations still use the existing statement initialization.
    No path-dependent values or permissions are cached across invocations.
    """
    cache=getattr(lookup,'_legacy_forward_local_defaults',None)
    if cache is None:cache={};lookup._legacy_forward_local_defaults=cache
    identity=function['id']
    if identity in cache:return cache[identity]
    if not function_scoped_locals(lookup):cache[identity]={};return cache[identity]
    from .m03_p_paths import walk
    nodes=list(walk(function.get('body')))
    declarations={n['id']:n for n in nodes if n.get('nodeType')=='VariableDeclaration' and not n.get('stateVariable')}
    needed=set()
    for n in nodes:
        ref=n.get('referencedDeclaration')
        if n.get('nodeType')!='Identifier' or ref not in declarations:continue
        use=n.get('src','').split(':');decl=declarations[ref].get('src','').split(':')
        if len(use)==len(decl)==3 and use[2]==decl[2] and int(use[0])<int(decl[0]):needed.add(ref)
    cache[identity]={ref:scalar_default(declarations[ref]) for ref in needed}
    return cache[identity]
