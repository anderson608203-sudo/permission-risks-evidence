"""Compiler-bound scalar types and exact rational constant evaluation."""
from fractions import Fraction

def scalar_type(typ,lookup,node=None):
    node=node or {};ref=node.get('referencedDeclaration')
    declaration=lookup.nodes.get(ref,{})
    if declaration.get('nodeType')=='ContractDefinition':return 'address'
    if declaration.get('nodeType')=='EnumDefinition':return 'enum '+declaration['name']
    if not typ:return typ
    import re
    if re.fullmatch(r'(?:u?int(?:[0-9]+)?|bytes(?:[0-9]+)?|bool|address(?: payable)?|string)',typ):return typ
    if typ.startswith('contract '):return 'address'
    if typ.startswith('enum '):return typ
    matches=[n for n in lookup.nodes.values() if n.get('nodeType') in ('ContractDefinition','EnumDefinition') and n.get('name')==typ]
    kinds={n['nodeType'] for n in matches}
    if kinds=={'ContractDefinition'}:return 'address'
    if kinds=={'EnumDefinition'}:return 'enum '+typ
    return typ

def rational_constant(node,depth=0):
    if not node or depth>64:return None
    kind=node.get('nodeType');r=None
    if kind=='Literal' and node.get('kind')=='number':
        text=node['value'].replace('_','')
        r=Fraction(int(text,16)) if text.lower().startswith('0x') else Fraction(text)
        units={'wei':1,'szabo':10**12,'finney':10**15,'gwei':10**9,'ether':10**18,'seconds':1,'minutes':60,'hours':3600,'days':86400,'weeks':604800,'years':31536000}
        if node.get('subdenomination'):
            if node['subdenomination'] not in units:return None
            r*=units[node['subdenomination']]
    elif kind=='TupleExpression' and not node.get('isInlineArray') and len(node.get('components',[]))==1:
        return rational_constant(node['components'][0],depth+1)
    elif kind=='UnaryOperation' and node.get('operator') in ('+','-'):
        a=rational_constant(node.get('subExpression'),depth+1)
        if a is not None:r=a if node['operator']=='+' else -a
    elif kind=='BinaryOperation':
        # Fold only Solidity's untyped rational expressions, not typed integer
        # arithmetic, overflow, truncating division or explicit conversions.
        typ=node.get('typeDescriptions',{}).get('typeString','')
        if not typ.startswith(('rational_const ','int_const ')):return None
        a=rational_constant(node.get('leftExpression'),depth+1);b=rational_constant(node.get('rightExpression'),depth+1)
        if a is None or b is None:return None
        operator=node.get('operator')
        if operator=='+':r=a+b
        elif operator=='-':r=a-b
        elif operator=='*':r=a*b
        elif operator=='/' and b:r=a/b
        elif operator=='**' and b.denominator==1 and abs(b.numerator)<=512 and (a or b>=0):r=a**b.numerator
        else:return None
    if r is not None and max(r.numerator.bit_length(),r.denominator.bit_length())>8192:return None
    return r


def _source_fixed_storage(lookup,ref):
    from .m03_p_paths import walk,lit
    decl=lookup.nodes.get(ref,{})
    if not decl.get('stateVariable'):return None
    value=decl.get('value');constructor_writer=None
    bases=set(lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']]))
    if decl.get('scope') not in bases:return None
    roots=[lookup.nodes[c] for c in bases]
    if value is None:
        assignments=[n for root in roots for n in walk(root) if n.get('nodeType')=='Assignment' and n.get('operator')=='=' and n.get('leftHandSide',{}).get('nodeType')=='Identifier' and n['leftHandSide'].get('referencedDeclaration')==ref]
        from .source_entry_identity import function_kind
        constructors={n.get('id') for root in roots for fn in root.get('nodes',[]) if fn.get('nodeType')=='FunctionDefinition' and function_kind(fn)=='constructor' for n in walk(fn)}
        if len(assignments)!=1 or assignments[0].get('id') not in constructors:return None
        constructor_writer=assignments[0]['id'];value=assignments[0]['rightHandSide']

    # Include compiler-bound library/local callees; their assembly can modify
    # caller storage even though its body is outside the inheritance nodes.
    seen=set(bases);pending=list(roots)
    while pending:
        scope=pending.pop()
        for n in walk(scope):
            callee_ref=(n.get('expression',{}) if n.get('nodeType')=='FunctionCall' else n.get('modifierName',{}) if n.get('nodeType')=='ModifierInvocation' else {}).get('referencedDeclaration')
            target=lookup.nodes.get(callee_ref,{})
            if target.get('nodeType') in ('FunctionDefinition','ModifierDefinition') and target.get('body') and callee_ref not in seen:
                seen.add(callee_ref);roots.append(target);pending.append(target)
    # Assembly and delegate execution can write slots without an AST lvalue.
    if any(n.get('nodeType')=='InlineAssembly' or n.get('nodeType')=='MemberAccess' and n.get('memberName') in ('delegatecall','callcode') for root in roots for n in walk(root)):return None
    for root in roots:
        for n in walk(root):
            left=n.get('leftHandSide') if n.get('nodeType')=='Assignment' else n.get('subExpression') if n.get('nodeType')=='UnaryOperation' and n.get('operator') in ('++','--','delete') else None
            if left and any(x.get('referencedDeclaration')==ref for x in walk(left)) and n.get('id')!=constructor_writer:return None
    number=rational_constant(value)
    if number is None or number.denominator!=1:return None
    typ=decl.get('typeDescriptions',{}).get('typeString','')
    import re
    match=re.fullmatch(r'uint(\d*)',typ)
    if not match or not 0<=number.numerator<2**int(match[1] or 256):return None
    lookup.__dict__.setdefault('source_fixed_storage_facts',{})[ref]={'source':lookup.anchor(decl),'value':number.numerator,'basis':'literal declaration or unique constructor assignment, complete source lvalue scan, no assembly/delegate writes in selected inheritance scope','scope':'original compiled contract source; no deployed upgrade/history proof'}
    return lit(number.numerator)


def source_fixed_storage(lookup,ref):
    import copy
    cache=lookup.__dict__.setdefault('_source_fixed_storage_cache',{})
    if ref not in cache:cache[ref]=_source_fixed_storage(lookup,ref)
    return copy.deepcopy(cache[ref])
