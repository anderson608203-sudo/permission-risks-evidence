"""Narrow, compiler-bound summary of terminal delegate forwarding assembly.
This recognizes invocation and termination only, never arbitrary callee effects.
Unrecognized assembly retains the existing unsupported path diagnostic.
"""
import copy,re
from .m03_p_paths import lit

_IDENT=r'[A-Za-z_$][A-Za-z0-9_$]*'
_PATTERN=re.compile(
 r'\{let(?P<result>'+_IDENT+r'):=delegatecall\((?:sub\(gas\(\),(?P<reserve>0x[0-9a-fA-F]+|[0-9]+)\)|gas\(\)),'
 r'(?P<dst>'+_IDENT+r'),add\((?P<data>'+_IDENT+r'),(?:0x20|32)\),mload\((?P=data)\),0,0\)'
 r'let(?P<size>'+_IDENT+r'):=returndatasize\(\)let(?P<ptr>'+_IDENT+r'):=mload\((?:0x40|64)\)'
 r'returndatacopy\((?P=ptr),0,(?P=size)\)switch(?P=result)case0\{revert\((?P=ptr),(?P=size)\)\}'
 r'default\{return\((?P=ptr),(?P=size)\)\}\}')


_BYTES_PATTERN=re.compile(
 r'\{let(?P<result>'+_IDENT+r'):=delegatecall\((?:sub\(gas\(\),(?P<reserve>0x[0-9a-fA-F]+|[0-9]+)\)|gas\(\)),'
 r'(?P<dst>'+_IDENT+r'),add\((?P<data>'+_IDENT+r'),(?:0x20|32)\),mload\((?P=data)\),0,0\)'
 r'let(?P<size>'+_IDENT+r'):=returndatasize\(\)(?P<ptr>'+_IDENT+r'):=mload\((?:0x40|64)\)'
 r'mstore\((?:0x40|64),add\((?P=ptr),and\(add\(add\((?P=size),(?:0x20|32)\),(?:0x1f|31)\),not\((?:0x1f|31)\)\)\)\)'
 r'mstore\((?P=ptr),(?P=size)\)returndatacopy\(add\((?P=ptr),(?:0x20|32)\),0,(?P=size)\)'
 r'switchiszero\((?P=result)\)case1\{revert\(add\((?P=ptr),(?:0x20|32)\),(?P=size)\)\}\}')

def bound_reference(n,name,lookup):
    refs=n.get('externalReferences',[])
    if isinstance(refs,dict):refs=list(refs.values())
    refs=[x for r in refs for x in ([r] if 'declaration' in r else r.values())]
    ids={r.get('declaration') for r in refs if not r.get('isSlot') and not r.get('isOffset')
         and lookup.nodes.get(r.get('declaration'),{}).get('name')==name}
    return next(iter(ids)) if len(ids)==1 else None

def yul_text(node):
    """Serialize only the compiler Yul syntax accepted by the exact matcher."""
    kind=node.get('nodeType')
    if kind=='YulBlock':return '{'+''.join(yul_text(x) for x in node['statements'])+'}'
    if kind in ('YulIdentifier','YulTypedName'):return node['name']
    if kind=='YulLiteral' and node.get('kind')=='number':return node['value']
    if kind=='YulFunctionCall':return yul_text(node['functionName'])+'('+','.join(yul_text(x) for x in node['arguments'])+')'
    if kind=='YulAssignment' and len(node['variableNames'])==1:
        return yul_text(node['variableNames'][0])+':='+yul_text(node['value'])
    if kind=='YulExpressionStatement':return yul_text(node['expression'])
    if kind=='YulVariableDeclaration' and len(node['variables'])==1 and node.get('value'):
        return 'let'+yul_text(node['variables'][0])+':='+yul_text(node['value'])
    if kind=='YulSwitch':return 'switch'+yul_text(node['expression'])+''.join(yul_text(x) for x in node['cases'])
    if kind=='YulCase':return ('default' if node['value']=='default' else 'case'+yul_text(node['value']))+yul_text(node['body'])
    raise ValueError('assembly_syntax_outside_terminal_forward_summary')

def forward(lookup,n,state):
    if n.get('nodeType')!='InlineAssembly':return None
    try:text=n.get('operations') or yul_text(n.get('AST',{}))
    except (ValueError,KeyError,TypeError):return None
    text=re.sub(r'/\*.*?\*/|//[^\n]*',' ',text,flags=re.S)
    compact=re.sub(r'\s+','',text)
    match=_PATTERN.fullmatch(compact)
    terminal=bool(match)
    if not match:match=_BYTES_PATTERN.fullmatch(compact)
    if not match:return None
    names=match.groupdict()
    # Distinct assembly temporaries must not shadow target/input bindings.
    if len({names[k] for k in ('result','size','ptr','dst','data')})!=5:return None
    reserve=names.get('reserve') or '0'
    if not 0<=int(reserve,0 if reserve.startswith('0x') else 10)<2**64:return None
    dst_id=bound_reference(n,names['dst'],lookup);data_id=bound_reference(n,names['data'],lookup)
    if dst_id is None or data_id is None:return None
    data_decl=lookup.nodes[data_id];dst_decl=lookup.nodes[dst_id]
    if data_decl.get('stateVariable') or not data_decl.get('typeDescriptions',{}).get('typeIdentifier','').startswith('t_bytes_memory'):return None
    if dst_decl.get('typeDescriptions',{}).get('typeString') not in ('address','address payable'):return None
    data=state['env'].get(data_id)
    if not data or not (data.get('kind')=='source_calldata_bytes' or data.get('kind')=='parameter' and data.get('type','').startswith('bytes')):return None
    if dst_id in state['env']:destination=copy.deepcopy(state['env'][dst_id])
    elif dst_decl.get('stateVariable'):destination={'kind':'storage','root':dst_id,'segments':[]}
    else:return None
    if not terminal:
        response_id=bound_reference(n,names['ptr'],lookup)
        response_decl=lookup.nodes.get(response_id,{})
        if response_id is None or response_decl.get('stateVariable') or not response_decl.get('typeDescriptions',{}).get('typeIdentifier','').startswith('t_bytes_memory'):return None
        state['env'][response_id]={'kind':'unknown','reason':'delegated_return_bytes_not_modeled'}
    source=lookup.anchor(n)
    effect={'kind':'dangerous_external_call','recipient':destination,'source':source,
        'scope':'exact compiler-bound terminal delegate forwarding; callee state, return bytes and gas sufficiency not modeled',
        'prefix_conditions':copy.deepcopy(state['guards']),
        'prefix_issues':copy.deepcopy(state['issues']),
        'prefix_evaluation_terms':copy.deepcopy(state.get('evaluated_terms',[])),
        'assembly_binding':{'destination_declaration':dst_id,'bytes_declaration':data_id,
                            'complete_block_matched':True,'failure_reverts':True,'success_halts_evm':terminal}}
    state.setdefault('sensitive_effects',[]).append(effect)
    state['issues'].append({'reason':'dangerous_external_effect_not_resolved','source':source,
                            'invocation_prefix_separately_available':True})
    if terminal:state['flow']='returned';state['_evm_halted']=True
    state.setdefault('source_assembly_summaries',[]).append({'source':source,'kind':'terminal_delegate_forward' if terminal else 'delegate_bytes_forward',
        'not_arbitrary_assembly_support':True,'only_invocation_prefix_can_support_code_boundary_query':True})
    return [state]
