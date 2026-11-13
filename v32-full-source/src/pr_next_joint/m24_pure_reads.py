"""Narrow compiler-bound, side-effect-free memory-word helper summary.
An opaque returned word is never usable as a permission or effect proof. It
allows unrelated authority writes to survive a pure metadata conversion.
"""
import re,copy
from .m20_assembly import yul_text,bound_reference
def summarize(p,node,target,args):
    from .source_entry_identity import function_mutability
    if function_mutability(target) in ('view','pure'):
        present=code_presence(p,target,args)
        if present is not None:return present
    if function_mutability(target)!='pure':return None
    ps=target.get('parameters',{}).get('parameters',[])
    rs=target.get('returnParameters',{}).get('parameters',[])
    body=target.get('body',{}).get('statements',[])
    if len(ps)!=1 or len(rs)!=1 or len(args)!=1 or len(body)!=1 or body[0].get('nodeType')!='InlineAssembly':return None
    if not ps[0].get('typeDescriptions',{}).get('typeIdentifier','').startswith(('t_string_memory','t_bytes_memory')):return None
    if rs[0].get('typeDescriptions',{}).get('typeString')!='bytes32':return None
    asm=body[0]
    try:text=asm.get('operations') or yul_text(asm.get('AST',{}))
    except (ValueError,KeyError,TypeError):return None
    text=re.sub(r'\s+','',text)
    m=re.fullmatch(r'\{([A-Za-z_$][\w$]*):=mload\(add\(([A-Za-z_$][\w$]*),(?:32|0x20)\)\)\}',text)
    if not m or bound_reference(asm,m[1],p)!=rs[0]['id'] or bound_reference(asm,m[2],p)!=ps[0]['id']:return None
    result={'kind':'source_pure_memory_word','input':copy.deepcopy(args[0]),'source':p.anchor(asm),'type':'bytes32',
            'scope':'pure memory read; output-dependent risk checks remain unsupported, gas exhaustion not modeled'}
    p.current.setdefault('read_calls',[]).append({'source':p.anchor(node),'target':p.anchor(target),'arguments':copy.deepcopy(args),
        'return_value':result,'binding':'compiler_verified_single_pure_memory_read','no_storage_external_or_control_effect':True})
    return result


def code_presence(lookup, target, arguments):
    """Exactly: uint local; assembly { local := extcodesize(address) }; return local > 0."""
    params = target.get('parameters', {}).get('parameters', [])
    statements = (target.get('body') or {}).get('statements', [])
    if len(params) != 1 or len(arguments) != 1 or len(statements) != 3:
        return None
    declaration, assembly, returned = statements
    variables = declaration.get('declarations', [])
    if (declaration.get('nodeType') != 'VariableDeclarationStatement' or declaration.get('initialValue')
            or len(variables) != 1 or not variables[0] or assembly.get('nodeType') != 'InlineAssembly'
            or returned.get('nodeType') != 'Return' or params[0].get('typeDescriptions', {}).get('typeString') not in ('address','address payable')):
        return None
    typ = variables[0].get('typeDescriptions', {}).get('typeString')
    if typ not in ('uint256','uint'):return None
    expression = returned.get('expression', {})
    if (expression.get('nodeType') != 'BinaryOperation' or expression.get('operator') != '>'
            or expression.get('leftExpression', {}).get('referencedDeclaration') != variables[0]['id']
            or expression.get('rightExpression', {}).get('nodeType') != 'Literal'
            or expression['rightExpression'].get('value') != '0'):
        return None
    try:text = assembly.get('operations') or yul_text(assembly.get('AST', {}))
    except (ValueError, KeyError, TypeError):return None
    match = re.fullmatch(r'\s*\{\s*([\w$]+)\s*:=\s*extcodesize\s*\(\s*([\w$]+)\s*\)\s*\}\s*',text)
    if (not match or bound_reference(assembly,match[1],lookup) != variables[0]['id']
            or bound_reference(assembly,match[2],lookup) != params[0]['id']):
        return None
    return {'kind':'address_has_runtime_code','address':copy.deepcopy(arguments[0]),'type':'bool'}
