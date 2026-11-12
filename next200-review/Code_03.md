# 源码文本 · 3

## source/src/pr_next_joint/frontend/assembly.py

原文件 SHA-256 `6624384a6498a7846b03418859e3949e102778954902c667107a30c454fde792`

````python
"""Narrow, compiler-bound summary of terminal delegate forwarding assembly.
This recognizes invocation and termination only, never arbitrary callee effects.
Unrecognized assembly retains the existing unsupported path diagnostic.
"""
import copy,re
from pr_next_joint.frontend.path_ir import lit

_IDENT=r'[A-Za-z_$][A-Za-z0-9_$]*'
_PATTERN=re.compile(
 r'\{let(?P<result>'+_IDENT+r'):=delegatecall\((?:sub\(gas(?:\(\))?,(?P<reserve>0x[0-9a-fA-F]+|[0-9]+)\)|gas(?:\(\))?),'
 r'(?P<dst>'+_IDENT+r'),add\((?P<data>'+_IDENT+r'),(?:0x20|32)\),mload\((?P=data)\),0,0\)'
 r'let(?P<size>'+_IDENT+r'):=returndatasize(?:\(\))?let(?P<ptr>'+_IDENT+r'):=mload\((?:0x40|64)\)'
 r'returndatacopy\((?P=ptr),0,(?P=size)\)switch(?P=result)case0\{revert\((?P=ptr),(?P=size)\)\}'
 r'default\{return\((?P=ptr),(?P=size)\)\}\}')


_BYTES_PATTERN=re.compile(
 r'\{let(?P<result>'+_IDENT+r'):=delegatecall\((?:sub\(gas(?:\(\))?,(?P<reserve>0x[0-9a-fA-F]+|[0-9]+)\)|gas(?:\(\))?),'
 r'(?P<dst>'+_IDENT+r'),add\((?P<data>'+_IDENT+r'),(?:0x20|32)\),mload\((?P=data)\),0,0\)'
 r'let(?P<size>'+_IDENT+r'):=returndatasize(?:\(\))?(?P<ptr>'+_IDENT+r'):=mload\((?:0x40|64)\)'
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
        'call_mode':'DELEGATECALL',
        'callpoint_writes':copy.deepcopy(state['writes']),
        'callpoint_guards':copy.deepcopy(state['guards']),
        'callpoint_evaluations':copy.deepcopy(state.get('evaluated_terms',[])),
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

````

## source/src/pr_next_joint/frontend/bytes.py

原文件 SHA-256 `4b436c809c3b777d11c7f10e51f33921b8db84867df6f8a50e522199853730ce`

````python
"""Compiler-bound pure assembly reads, with explicit uses and bounds.
No external call, arbitrary memory write, storage write or signature-validity
assumption is introduced. Raw calldata words remain opaque to risk solving.
"""
import copy,re
from pr_next_joint.frontend.path_ir import op, lit, key
from pr_next_joint.frontend.assembly import bound_reference, yul_text
ID=r'[A-Za-z_$][A-Za-z0-9_$]*'
NUM=r'(?:0x[0-9a-fA-F]+|[0-9]+)'
LOAD=re.compile(r'('+ID+r'):=calldataload\(('+NUM+r')\)')
MEM=re.compile(r'('+ID+r'):=(?:mload\(add\(('+ID+r'),('+NUM+r')\)\)|byte\((0),mload\(add\(('+ID+r'),('+NUM+r')\)\)\))')

def length(value):
    return {'kind':'source_bytes_length','input':copy.deepcopy(value),'type':'uint256'}

def summarize(lookup,node,state):
    try:text=node.get('operations') or yul_text(node.get('AST',{}))
    except (ValueError,KeyError,TypeError):return None
    text=re.sub(r'/\*.*?\*/|//[^\n]*',' ',text,flags=re.S)
    text=re.sub(r'\s+','',text)
    if not text.startswith('{') or not text.endswith('}'):return None
    body=text[1:-1]
    parsed=[];position=0
    while position<len(body):
        match=LOAD.match(body,position)
        mode='calldata'
        if not match:match=MEM.match(body,position);mode='memory'
        if not match:return None
        parsed.append((mode,match));position=match.end()
    if not parsed or len(parsed)>8:return None
    updates={};evidence=[]
    for mode,m in parsed:
        dest=bound_reference(node,m[1],lookup);decl=lookup.nodes.get(dest,{})
        if dest is None or decl.get('stateVariable') or dest not in state['env'] or dest in updates:return None
        typ=decl.get('typeDescriptions',{}).get('typeString','')
        if mode=='calldata':
            if typ not in ('bytes32','uint256'):return None
            offset=int(m[2],16 if m[2].startswith('0x') else 10)
            if offset>=2**256:return None
            value={'kind':'source_calldata_word','input':copy.deepcopy(lookup.calldata),'offset':offset,
                   'type':'bytes32','scope':'opaque raw calldata read; no ABI-layout or permission inference'}
        else:
            base_name=m[2] or m[5];raw=m[3] or m[6];size=1 if m[4] else 32
            if typ not in (('uint8','bytes1') if size==1 else ('bytes32','uint256')):return None
            base_id=bound_reference(node,base_name,lookup)
            base_decl=lookup.nodes.get(base_id,{})
            if not base_decl.get('typeDescriptions',{}).get('typeIdentifier','').startswith('t_bytes_memory'):return None
            base=state['env'].get(base_id)
            if not base or base.get('kind')!='parameter' or not base.get('type','').startswith('bytes'):return None
            offset=int(raw,16 if raw.startswith('0x') else 10)-32
            if offset<0 or offset+size>128:return None
            from pr_next_joint.checks.access.shared_policy import implies
            from pr_next_joint.verification.expressions import Unsupported
            try:valid=implies(lookup,state,op('>=',length(base),lit(offset+size)))
            except (Unsupported,ValueError):return None
            if not valid:return None
            value={'kind':'source_bytes_slice','input':copy.deepcopy(base),'offset':offset,'size':size,
                   'type':typ,'range_validated_at_source':True}
        updates[dest]=value;evidence.append({'declaration':dest,'value':value})
    state['env'].update(updates)
    state.setdefault('source_assembly_summaries',[]).append({'source':lookup.anchor(node),
        'kind':'pure_source_bound_byte_reads','writes':evidence,
        'no_external_or_storage_side_effect':True,'calldata_executable_use_remains_unsupported':True})
    return [state]

def encode(encoder,value):
    kind=value.get('kind')
    if kind=='source_bytes_length':
        base=value.get('input',{})
        if base.get('kind')!='parameter' or not base.get('type','').startswith('bytes'):
            from pr_next_joint.verification.expressions import Unsupported
            raise Unsupported('dynamic_bytes_length_not_bound')
        return encoder.atom(value,'uint256')
    if kind!='source_bytes_slice':return None
    from pr_next_joint.verification.expressions import Unsupported
    base=value.get('input',{});offset=value.get('offset');size=value.get('size')
    if base.get('kind')!='parameter' or not base.get('type','').startswith('bytes') or type(offset)is not int or size not in (1,32) or not 0<=offset<=127 or offset+size>128:
        raise Unsupported('dynamic_bytes_slice_not_bound')
    z=encoder.z
    # Byte congruence preserves overlap across reads and same-input recovery.
    parts=[]
    for i in range(size):
        item={'kind':'input_byte','input':base,'offset':offset+i,'type':'uint8'}
        parts.append(encoder.atom(item,'uint8')*256**(size-1-i))
    encoder.constraints.append(encode(encoder,length(base))>=offset+size)
    return z.Sum(*parts)

````

## source/src/pr_next_joint/frontend/calls.py

原文件 SHA-256 `e5b2a6d156c8dbc0a8f564d2be910f93bfbafd24e43ad978ba7156f610f09710`

````python
"""Compiler-bound internal library calls and native CALL syntax.
No assumed token implementation or transfer-name matching.
"""
import copy
from pr_next_joint.frontend.path_ir import key, walk, op, lit, conditions_possible
from pr_next_joint.frontend.source_entry_identity import function_mutability, builtin_call
from pr_next_joint.frontend.read_calls import boolean_union

def bound_library(lookup,node,target):
    from pr_next_joint.frontend.source_library_binding import compiler_bound_receiver
    return compiler_bound_receiver(lookup,node,target)

def bind_arguments(lookup,call,target):
    args=call.get('arguments',[])
    names=call.get('names',[])
    if not names:return args
    parameters=[p.get('name') for p in target['parameters']['parameters']]
    # Reordering effectful operands would assume an evaluation order. Leave a
    # visible gap in that case; plain local or literal arguments can be mapped.
    if (len(names)!=len(args) or len(set(names))!=len(names) or set(names)!=set(parameters)
            or any(a.get('nodeType') not in ('Identifier','Literal') for a in args)):
        return None
    named=dict(zip(names,args))
    return [named[name] for name in parameters]

def expression_call(p,node,env):
    expr=node.get('expression',{});target=p.fns.get(expr.get('referencedDeclaration'))
    if not target or function_mutability(target) in ('pure','view'):return None
    declared=target
    bound=bound_library(p,node,target)
    from pr_next_joint.frontend.dispatch import member_target, resolve
    if not bound:
        target=resolve(p,target,p.read_calls.active_contract) if expr.get('nodeType')=='Identifier' else member_target(p,node,target)
        if target is None:return None
    params=target.get('parameters',{}).get('parameters',[])
    source_args=bind_arguments(p,node,declared)
    if source_args is None:
        p.current['issues'].append({'reason':'named_internal_arguments_not_bound','source':p.anchor(node)})
        return {'kind':'unknown','reason':'named_internal_arguments_not_bound'}
    args=([p.value(expr['expression'],env)] if bound else [])+[p.value(a,env) for a in source_args]
    if len(args)!=len(params):return None
    stack=getattr(p,'_effect_expression_stack',[])
    if target['id'] in stack or len(stack)>=8:raise ValueError('P_EFFECT_CALL_DEPTH_LIMIT')
    parent=p.current;outer_unknown=p.unknown;p.unknown=[]
    p._effect_expression_stack=stack+[target['id']]
    child=copy.deepcopy(parent);before=len(child['writes'])
    try:
        paths=p.invoke(target,args,child,depth=len(stack)+1);unknown=list(p.unknown)
    finally:
        p.current=parent;p._effect_expression_stack=stack;p.unknown=outer_unknown
    if unknown or any(x['issues'] or x.get('_evm_halted') or x.get('evaluation_gaps') or len(x['writes'])!=before for x in paths):
        # Branch-dependent state writes require a statement-level expansion.
        parent['issues'].append({'reason':'internal_effect_expression_requires_state_expansion','source':p.anchor(node)})
        return {'kind':'unknown','reason':'internal_effect_expression_requires_state_expansion'}
    successes=[x for x in paths if x['flow'] in ('normal','returned') and 'return_value' in x and conditions_possible(x['guards'])]
    if not successes:parent['guards'].append(lit(False));return lit(False)
    gates=[boolean_union('and',x['guards']) for x in successes]
    parent['guards'].append(boolean_union('or',gates))
    evaluated_before=len(parent.get('evaluated_terms',[]))
    for child,gate in zip(successes,gates):
        for field in ('sensitive_effects','native_transfers'):
            old=parent.get(field,[])
            for effect in child.get(field,[]):
                if effect in old:continue
                effect=copy.deepcopy(effect);effect['call_path_conditions']=copy.deepcopy(child['guards'])
                parent.setdefault(field,[]).append(effect)
        terms=child.get('evaluated_terms',[])[evaluated_before:]
        if terms:parent.setdefault('evaluated_terms',[]).append({'kind':'guarded_evaluation','condition':gate,'values':terms})
    result=successes[-1]['return_value']
    for child,gate in reversed(list(zip(successes[:-1],gates[:-1]))):
        result={'kind':'conditional','condition':gate,'when_true':child['return_value'],'when_false':result}
    parent.setdefault('source_calls',[]).append({'source':p.anchor(node),'target':p.anchor(target),'basis':'compiler_internal_library_or_local_body','sender_preserved':True,'conditional_effects_preserved':True})
    return result

def native_call(p,node,env):
    expr=node.get('expression',{});options={}
    if expr.get('nodeType')=='FunctionCallOptions':
        options=dict(zip(expr.get('names',[]),expr.get('options',[])));expr=expr.get('expression',{})
    else:
        while expr.get('nodeType')=='FunctionCall':
            member=expr.get('expression',{})
            if member.get('nodeType')!='MemberAccess' or member.get('memberName') not in ('value','gas') or len(expr.get('arguments',[]))!=1:return None
            if member['memberName'] in options:return None
            options[member['memberName']]=expr['arguments'][0];expr=member['expression']
    if expr.get('nodeType')!='MemberAccess' or expr.get('memberName')!='call' or 'value' not in options:return None
    receiver=expr.get('expression',{});typ=receiver.get('typeDescriptions',{}).get('typeString','')
    args=node.get('arguments',[])
    if typ not in ('address','address payable') or len(args)!=1 or args[0].get('nodeType')!='Literal' or args[0].get('value')!='':return None
    recipient=p.value(receiver,env);amount=p.value(options['value'],env)
    gas=p.value(options['gas'],env) if 'gas' in options else None
    success={'kind':'native_call_success','source_id':node['id'],'recipient':recipient,'amount':amount}
    effect={'kind':'native_transfer','recipient':recipient,'amount':amount,'success':success,'source':p.anchor(node),
            'gas_argument':gas,'scope':'conditional native CALL; actual recipient execution/transaction success not established'}
    p.current.setdefault('native_transfers',[]).append(copy.deepcopy(effect));p.current.setdefault('sensitive_effects',[]).append(effect)
    # Solidity <0.5 returns bool; newer compiler ASTs return (bool,bytes).
    if node.get('typeDescriptions',{}).get('typeString')=='bool':return success
    return {'kind':'tuple','items':[success,{'kind':'native_return_data','source_id':node['id']}]}


def expand_value_statement(p,node,state,depth):
    """Lift one whole internal call out of an evaluated statement position.
    No reordering of short-circuit operands, sibling calls or side-effect arguments.
    """
    from .delegate_calls import expand
    delegated=expand(p,node,state,depth)
    if delegated is not None:return delegated
    kind=node.get('nodeType');route=None
    if kind=='VariableDeclarationStatement':route=('initialValue',)
    elif kind in ('Return','IfStatement'):route=('expression',) if kind=='Return' else ('condition',)
    elif kind=='ExpressionStatement':
        expression=node.get('expression',{})
        if builtin_call(expression,p) and expression.get('arguments'):route=('expression','arguments',0)
        elif expression.get('nodeType')=='Assignment' and expression.get('operator')=='=':
            lhs=expression.get('leftHandSide',{})
            # Complex LHS evaluation ordering is not assumed.
            if lhs.get('nodeType')=='Identifier':route=('expression','rightHandSide')
    if route is None:return None
    call=node
    for part in route:call=(call.get(part) if isinstance(call,dict) else call[part]) if call is not None else None
    if not call:return None
    shape=internal_value_target(p,call)
    if shape is None:
        from pr_next_joint.frontend.condition_paths import contains_effect_call
        if not contains_effect_call(p,call):return None
    from pr_next_joint.frontend.condition_paths import values
    outputs=[]
    for child,value in values(p,call,state,depth,shape):
        if value is None:
            outputs.append(child)
            continue
        replacement=copy.deepcopy(node);cursor=replacement
        for part in route[:-1]:cursor=cursor[part]
        cursor[route[-1]]={'nodeType':'V16EvaluatedValue','id':call.get('id'),'src':call.get('src'),'value':value}
        outputs.extend(p.statement(replacement,child,depth))
        if len(outputs)>p.limit:raise ValueError('P_SOURCE_PATH_LIMIT')
    return outputs

def internal_value_target(p,call):
    if call.get('nodeType')!='FunctionCall':return None
    expr=call.get('expression',{});target=p.fns.get(expr.get('referencedDeclaration'))
    if not target or function_mutability(target) in ('pure','view') or not target.get('returnParameters',{}).get('parameters'):return None
    bound=bound_library(p,call,target)
    if not bound and expr.get('nodeType')!='Identifier':
        from pr_next_joint.frontend.dispatch import member_target
        target=member_target(p,call,target)
        if target is None:return None
    source_args=bind_arguments(p,call,target)
    if source_args is None:return None
    arguments=([expr['expression']] if bound else [])+source_args
    if any(n.get('nodeType') in ('Assignment',) or n.get('nodeType')=='UnaryOperation' and n.get('operator') in ('++','--','delete') or n.get('nodeType')=='FunctionCall' and n.get('kind')!='typeConversion' for n in walk(arguments)):return None
    if not bound and expr.get('nodeType')=='Identifier':
        from pr_next_joint.frontend.dispatch import resolve
        target=resolve(p,target,p.read_calls.active_contract)
    return target,arguments

def invoke_value(p,call,state,depth,shape):
    target,arguments=shape
    if depth>=8:raise ValueError('P_EFFECT_CALL_DEPTH_LIMIT')
    args=[p.expr(a,state) for a in arguments]
    if len(args)!=len(target.get('parameters',{}).get('parameters',[])):
        raise ValueError('P_INTERNAL_ARGUMENT_BINDING')
    outer_env=copy.deepcopy(state['env']);outer_return={k:copy.deepcopy(state[k]) for k in ('_return_ids','_return_pending','return_value') if k in state}
    for child in p.invoke(target,args,copy.deepcopy(state),depth+1):
        if child['flow'] not in ('normal','returned') or child.get('_evm_halted'):
            yield child,None
            continue
        value=child.get('return_value')
        if value is None:
            child['issues'].append({'reason':'internal_value_call_missing_return','source':p.anchor(call)})
            value={'kind':'unknown','reason':'internal_value_call_missing_return'}
        child['env']=copy.deepcopy(outer_env);child['flow']='normal'
        for field in ('_return_ids','_return_pending','return_value'):child.pop(field,None)
        child.update(copy.deepcopy(outer_return))
        child.setdefault('source_calls',[]).append({'source':p.anchor(call),'target':p.anchor(target),'basis':'compiler_bound_internal_value_statement_expansion','sender_preserved':True,'state_and_return_path_preserved':True})
        yield child,value

````

## source/src/pr_next_joint/frontend/compiler_evidence.py

原文件 SHA-256 `83b76fb7f8d83d232ae4f39ec8f4099462960bf2f3f6d7cdbddc2d323869e5a5`

````python
"""Narrow, source-mapped legacy dispatcher evidence; no EVM execution or guesses.

Accept only the complete known linear 0.4 dispatcher grammar. Unsupported layouts
yield no evidence. Original compiler artifacts are never changed.
"""
import hashlib

class CompilerEntryEvidence(dict):
    """In-process provenance marker: cannot be supplied by a JSON artifact."""

def legacy_dispatch(runtime, source_map, selectors):
    try:
        code=bytes.fromhex(runtime.removeprefix('0x'))
        if not source_map:return {}
        maps=[];previous=[-1,-1,-1]
        for item in source_map.split(';'):
            fields=item.split(':')
            for j in range(min(3,len(fields))):
                if fields[j]!='':previous[j]=int(fields[j])
            maps.append(tuple(previous))
        ins=[];pc=0
        while pc<len(code) and len(ins)<len(maps):
            op=code[pc];n=op-95 if 96<=op<=127 else 0
            if pc+1+n>len(code):return {}
            ins.append((pc,op,int.from_bytes(code[pc+1:pc+1+n],'big') if n else None,maps[len(ins)]))
            pc+=n+1
        i=0
        def take(op,value=None):
            nonlocal i
            if i>=len(ins) or ins[i][1]!=op or value is not None and ins[i][2]!=value:raise ValueError('grammar')
            result=ins[i];i+=1;return result
        def push():
            nonlocal i
            if i>=len(ins) or not 96<=ins[i][1]<=127:raise ValueError('push')
            result=ins[i];i+=1;return result
        memory=take(0x60)
        if memory[2] not in (0x60,0x80):return {}
        take(0x60,0x40);take(0x52)
        # Two known 0.4 compiler guards: calldata shorter than a selector,
        # or empty calldata. Match the complete grammar, not a loose scan.
        if i<len(ins) and ins[i][1]==0x36:
            take(0x36);take(0x15)
        else:
            take(0x60,4);take(0x36);take(0x10)
        fallback=push()[2];take(0x57)
        take(0x60,0);take(0x35);take(0x7c,1<<224);take(0x90);take(0x04);take(0x63,0xffffffff);take(0x16)
        branches={}
        while i<len(ins) and ins[i][1]==0x80:
            branch_pc=take(0x80)[0];selector=take(0x63)[2].to_bytes(4,'big').hex();take(0x14)
            target=push()[2];take(0x57)
            if selector in branches:return {}
            branches[selector]={'dispatch_pc':branch_pc,'target_pc':target}
        end=take(0x5b)
        if fallback!=end[0] or set(branches)!=set(selectors):return {}
        bypc={row[0]:row for row in ins}
        result={}
        for selector,branch in branches.items():
            destination=bypc.get(branch['target_pc'])
            if not destination or destination[1]!=0x5b:return {}
            start,length,file_id=destination[3]
            if start<0 or length<=0 or file_id<0:return {}
            result[selector]={**branch,'source_start':start,'source_length':length,'source_file_id':file_id}
        return result
    except (ValueError,TypeError,IndexError,OverflowError):
        return {}

def derive(bundle,compiled,output_sha256):
    evidence=CompilerEntryEvidence()
    if not str(bundle.get('compiler',{}).get('compiler_version','')).startswith('0.4.'):
        return evidence
    for contract in bundle['contracts']:
        target=contract['file']+':'+contract['name']
        output=compiled.get('contracts',{}).get(contract['file'],{}).get(contract['name'],{})
        deployed=output.get('evm',{}).get('deployedBytecode',{})
        runtime=deployed.get('object','');source_map=deployed.get('sourceMap','')
        if not runtime or runtime.removeprefix('0x')!=contract.get('runtime','').removeprefix('0x'):continue
        if deployed.get('linkReferences') or contract.get('runtime_link_references'):continue
        selectors={f['selector'] for f in contract['functions']}
        branches=legacy_dispatch(runtime,source_map,selectors)
        if branches:
            evidence[target]={'program_id':bundle['program_id'],'build_id':bundle['build_id'],
                'standard_output_sha256':output_sha256,'runtime_sha256':hashlib.sha256(bytes.fromhex(runtime.removeprefix('0x'))).hexdigest(),
                'source_map_sha256':hashlib.sha256(source_map.encode()).hexdigest(),'grammar':'legacy_linear_dispatch_v2','branches':branches}
    return evidence

import hashlib,json
from pr_next_joint.core import require

class CompilerSourceEvidence(dict):
    """In-process provenance; JSON input cannot supply this evidence type."""
    def __init__(self,program_id,build_id):
        super().__init__();self.program_id=program_id;self.build_id=build_id

def derive_source_evidence(standard,compiled,bundle,output_sha256):
    evidence=CompilerSourceEvidence(bundle['program_id'],bundle['build_id'])
    anchored={r.get('source_anchor',{}).get('file') for r in bundle.get('functions',[])+bundle.get('state_declarations',[])}
    needed=set(standard['sources'])-anchored
    if not needed:return evidence
    claims={path:[] for path in needed};version=bundle['compiler']['compiler_version']
    for file,contracts in compiled.get('contracts',{}).items():
        for name,output in contracts.items():
            raw=output.get('metadata')
            if not raw:continue
            try:metadata=json.loads(raw)
            except (TypeError,ValueError):continue
            relevant=needed.intersection(metadata.get('sources',{}))
            if not relevant:continue
            require(metadata.get('language')=='Solidity','DATASET_METADATA_LANGUAGE')
            require(metadata.get('settings',{}).get('compilationTarget')=={file:name},'DATASET_METADATA_TARGET')
            require(metadata.get('compiler',{}).get('version','').split('+')[0]==version,'DATASET_METADATA_COMPILER')
            for path in relevant:
                claim=metadata['sources'][path].get('keccak256')
                require(isinstance(claim,str) and len(claim)==66 and claim.startswith('0x'),'DATASET_METADATA_SOURCE_HASH')
                claims[path].append({'target':file+':'+name,'keccak256':claim.lower(),'metadata_sha256':hashlib.sha256(raw.encode('utf8')).hexdigest()})
    # Keccak-256 is Ethereum's original hash, not hashlib.sha3_256.
    from Crypto.Hash import keccak
    for path,records in claims.items():
        if not records:continue
        data=standard['sources'][path]['content'].encode('utf8');h=keccak.new(digest_bits=256);h.update(data)
        expected='0x'+h.hexdigest()
        require({r['keccak256'] for r in records}=={expected},'DATASET_METADATA_SOURCE_MISMATCH:'+path)
        evidence[path]={'source_sha256':hashlib.sha256(data).hexdigest(),'source_keccak256':expected,
            'standard_output_sha256':output_sha256,'compiler_version':version,'metadata_sources':records}
    return evidence

````

## source/src/pr_next_joint/frontend/condition_paths.py

原文件 SHA-256 `df5ca75eaaafd2440739edc39966bc5f58387340014edad5ca2b94236c2d9d32`

````python
"""Execute conditional expressions containing bound internal transitions, in Solidity order."""
import copy

from pr_next_joint.frontend.path_ir import conditions_possible, lit, normalize, op
from pr_next_joint.frontend.calls import internal_value_target, invoke_value


def children(node):
    kind = node.get('nodeType')
    if kind == 'BinaryOperation' and node.get('operator') in ('&&', '||') and not node.get('function'):
        return node['leftExpression'], node['rightExpression']
    if kind == 'Conditional':
        return node['condition'], node['trueExpression'], node['falseExpression']
    if kind == 'UnaryOperation' and node.get('operator') == '!' and not node.get('function'):
        return (node['subExpression'],)
    if kind == 'TupleExpression' and not node.get('isInlineArray') and len(node['components']) == 1 and node['components'][0]:
        return tuple(node['components'])
    return ()


def contains_effect_call(lookup, node):
    return any(internal_value_target(lookup, child) or contains_effect_call(lookup, child)
               for child in children(node))


def values(lookup, node, state, depth, shape=None):
    shape = shape or internal_value_target(lookup, node)
    if shape:
        yield from invoke_value(lookup, node, state, depth, shape)
        return
    parts = children(node)
    if not parts:
        value = lookup.expr(node, state)
        yield state, value if state['flow'] == 'normal' else None
        return
    for branch, first in values(lookup, parts[0], state, depth):
        if first is None or len(parts) == 1:
            if first is not None and node.get('operator') == '!':
                first = normalize(op('!', first))
            yield branch, first
            continue
        for truth in (True, False):
            guard = first if truth else op('!', first)
            if not conditions_possible(branch['guards'] + [guard]):
                continue
            selected = copy.deepcopy(branch)
            selected['guards'].append(guard)
            selected.setdefault('branch_choices', []).append({
                'condition': first, 'sign': truth, 'source': lookup.anchor(parts[0])})
            if len(parts) == 3:
                yield from values(lookup, parts[1 if truth else 2], selected, depth)
            elif truth == (node['operator'] == '&&'):
                yield from values(lookup, parts[1], selected, depth)
            else:
                yield selected, lit(truth)

````

## source/src/pr_next_joint/frontend/dataset_intake.py

原文件 SHA-256 `abf4c9e9a41206457a25bd641fc590073430f20893c2185001a1e4742271658c`

````python
"""Read matched compiler facts using original compiler settings, never labels.

This is an input adapter, not a source-anchor/semantic binding replacement.
The existing strict anchor validator and all M2/M3/M4 checks remain in force.
"""
import copy,hashlib,json,re
from pathlib import Path
from pr_next_joint.core import digest, require
from pr_next_joint.frontend.source_intake import validate_loaded_artifacts
from pr_next_joint.frontend.inventory import target_inventory

FILES=('standard-input.json','standard-output.json','ProgramBundle.json','native_ssa.json','extract_receipt.json')

def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def confined(root,name):
    require(isinstance(name,str) and name,'DATASET_PATH_REQUIRED')
    p=(root/name).resolve();require(p.is_relative_to(root.resolve()),'DATASET_PATH_OUTSIDE_ROOT')
    require(p.is_file(),'DATASET_FILE_MISSING:'+name)
    return p

def load_compiled_unit(root,descriptor):
    root=Path(root).resolve();spec_path=confined(root,str(descriptor));spec=read(spec_path)
    require(spec.get('schema')=='dataset-compiled-unit-v1','DATASET_SCHEMA')
    require(set(spec)<={'schema','input_id','unit_id','artifacts','targets','description'},'DATASET_UNEXPECTED_FIELDS')
    for key in ('input_id','unit_id'):
        require(isinstance(spec.get(key),str) and re.fullmatch(r'[A-Za-z0-9_]+',spec[key]),'DATASET_ID')
    artifacts=spec.get('artifacts',{})
    require(set(artifacts)==set(FILES),'DATASET_ARTIFACT_SET')
    paths={}
    for name,item in artifacts.items():
        require(set(item)=={'path','sha256'},'DATASET_ARTIFACT_SHAPE')
        path=confined(root,item['path']);require(sha(path)==item['sha256'],'DATASET_ARTIFACT_CHANGED:'+name);paths[name]=path
    standard,compiled,bundle,native,receipt=[read(paths[n]) for n in FILES]
    retained = receipt.get('status') == 'extracted'
    require(receipt.get('status')=='compiled_and_extracted' or
            retained and receipt.get('compiler_invocations')==0 and receipt.get('native_extractions')==1,
            'DATASET_FACTS_NOT_READY')
    # An original retained-compiler extraction receipt records the actual old
    # extraction. No replacement success receipt or fresh compilation is claimed.
    for field, name in (('bundle_file_sha256','ProgramBundle.json'),('native_file_sha256','native_ssa.json')):
        if field in receipt: require(receipt[field]==sha(paths[name]),'DATASET_RETAINED_FILE_RECEIPT')
    require(receipt.get('standard_input_sha256')==sha(paths['standard-input.json']),'DATASET_INPUT_RECEIPT')
    if not retained or 'standard_input_digest' in receipt:
        require(receipt.get('standard_input_digest')==digest(standard),'DATASET_INPUT_DIGEST')
    require(receipt.get('standard_output_sha256')==sha(paths['standard-output.json']),'DATASET_OUTPUT_RECEIPT')
    require(standard.get('language')=='Solidity' and isinstance(standard.get('settings'),dict),'DATASET_LANGUAGE_SETTINGS')
    require(not any(e.get('severity')=='error' for e in compiled.get('errors',[])),'DATASET_COMPILER_ERRORS')
    texts=standard.get('sources',{})
    require(bool(texts) and all(isinstance(v.get('content'),str) for v in texts.values()),'DATASET_INLINE_SOURCE_REQUIRED')
    source_hashes={k:hashlib.sha256(v['content'].encode('utf-8')).hexdigest() for k,v in texts.items()}
    require(bundle.get('program_id')==digest(source_hashes),'DATASET_PROGRAM_ID')
    expected_build=digest({'input':standard,'compiler':receipt['compiler_binary_sha256']})
    require(bundle.get('build_id')==expected_build,'DATASET_BUILD_ID')
    require(all(receipt.get(k)==bundle.get(k)==native.get(k) for k in ('program_id','build_id')),'DATASET_FACT_IDENTITIES')
    require(receipt.get('native_sha256')==digest(native),'DATASET_NATIVE_RECEIPT')
    require(bundle.get('ast_sources')=={k:v.get('ast') for k,v in compiled.get('sources',{}).items()},'DATASET_AST_OUTPUT_MISMATCH')
    require(bundle.get('compiler',{}).get('compiler_version')==receipt.get('compiler_version'),'DATASET_COMPILER_VERSION')
    case={'standard_input':standard,'sources':[{'path':k,'sha256':v} for k,v in source_hashes.items()]}
    from pr_next_joint.frontend.compiler_evidence import derive_source_evidence
    compiler_sources=derive_source_evidence(standard,compiled,bundle,sha(paths['standard-output.json']))
    binding=validate_loaded_artifacts(case,bundle,native,compiler_sources=compiler_sources)
    # Derive auxiliary evidence only after original artifact identity validation.
    # The original bundle on disk and its receipt remain unchanged.
    from pr_next_joint.frontend.compiler_evidence import derive
    derived_entries=derive(bundle,compiled,sha(paths['standard-output.json']))
    bundle=copy.deepcopy(bundle)
    from pr_next_joint.runtime.immutable import restore
    immutable_reconstruction=restore(bundle,standard,compiled)
    bundle.pop('_compiler_entry_evidence',None)
    if derived_entries:
        bundle['_compiler_entry_evidence']=derived_entries
    inventory=target_inventory(bundle)
    available={x['file']+':'+x['contract'] for x in inventory if x['selected']}
    selection=spec.get('targets','auto')
    require(selection=='auto' or isinstance(selection,list) and selection and all(isinstance(x,str) for x in selection),'DATASET_TARGET_SPEC')
    requested=None if selection=='auto' else selection
    require(requested is None or len(requested)==len(set(requested)) and set(requested)<=available,'DATASET_TARGET_NOT_AVAILABLE')
    require(bool(available),'DATASET_NO_CONCRETE_TARGET')
    for item in inventory:
        if requested is not None and item['selected'] and item['file']+':'+item['contract'] not in requested:
            item.update(selected=False,reason='not_selected_by_explicit_scope')
    description=None
    if spec.get('description'):
        item=spec['description'];require(set(item)=={'path','sha256'},'DATASET_DESCRIPTION_SPEC')
        path=confined(root,item['path']);require(sha(path)==item['sha256'],'DATASET_DESCRIPTION_CHANGED')
        description=path.read_text(encoding='utf-8-sig')
    record={'schema':'dataset-intake-receipt-v1','input_id':spec['input_id'],'unit_id':spec['unit_id'],
        'descriptor_sha256':sha(spec_path),'program_id':bundle['program_id'],'build_id':bundle['build_id'],
        'compiler_version':receipt['compiler_version'],'compiler_sha256':receipt['compiler_binary_sha256'],
        'settings':standard['settings'],'source_hashes':source_hashes,'targets_requested':selection,
        'targets_selected':sorted(available if requested is None else requested),'target_inventory':inventory,
        'facts_verified':True,'original_extraction_status':receipt['status'],'compiler_invocations':0,'labels_read':False,'method_execution':'not_run',
        'artifact_sha256':{n:sha(p) for n,p in paths.items()},
        'derived_entry_evidence_targets':sorted(derived_entries),
        'compiler_metadata_bound_sources':sorted(compiler_sources)}
    if immutable_reconstruction:
        record['immutable_reconstruction']=immutable_reconstruction
        record['compiler_invocations']+=immutable_reconstruction['invocations']
    return {'unit_id':spec['unit_id'],'bundle':bundle,'native':native,'binding':binding,
        'sources':[{'file':k,'sha256':source_hashes[k],'content':v['content']} for k,v in texts.items()],
        'description':description,'selected_targets':requested,'receipt':record}

````

## source/src/pr_next_joint/frontend/delegate_calls.py

原文件 SHA-256 `493bcc96e4fc7eb41bb6736e9cbde21e9dd2af6f4980c05c97f7b1d891959637`

````python
"""Source-bound DELEGATECALL with explicit selector and a fixed supplied body.

CALL storage separation is never applied to delegate execution. Unknown code,
unknown selectors and unproved layouts fall through to the ordinary residual.
"""
import copy
from .path_ir import lit,walk


def layout(lookup,contract):
    data=contract.get('storage_layout') or {}
    if data.get('storage'):
        types=data['types']
        def shape(t):
            v=types[t]
            if v.get('members'):raise ValueError('delegate_struct_layout_not_supported')
            return (v['encoding'],v['numberOfBytes'],
                shape(v['key']) if 'key'in v else None,shape(v['value']) if 'value'in v else None,
                shape(v['base']) if 'base'in v else None,v.get('label') if v['encoding']=='inplace' else None)
        return {int(row['astId']):(int(row['slot']),int(row['offset']),shape(row['type'])) for row in data['storage']}
    # Exact Solidity packing for elementary values and mapping roots. A
    # complex unavailable layout is not guessed from declaration names.
    node=next(n for n in lookup.nodes.values() if n.get('nodeType')=='ContractDefinition' and
              n.get('name')==contract['name'] and lookup.anchor(n)['file']==contract['file'])
    result={};slot=offset=0
    for cid in reversed(node.get('linearizedBaseContracts',[node['id']])):
        for d in lookup.nodes[cid].get('nodes',[]):
            if d.get('nodeType')!='VariableDeclaration' or not d.get('stateVariable') or d.get('constant') or d.get('mutability')=='immutable':continue
            typ=d.get('typeName',{});kind=typ.get('nodeType')
            if kind=='Mapping':
                if offset:slot+=1;offset=0
                result[d['id']]=(slot,0,('mapping',typ.get('typeDescriptions',{}).get('typeString')));slot+=1;continue
            name=typ.get('name') or d.get('typeDescriptions',{}).get('typeString','')
            if name.startswith('contract '):name='address'
            import re
            if name in ('address','address payable'):size=20;name='address'
            elif name=='bool':size=1
            elif re.fullmatch(r'u?int\d*',name):size=int(re.sub(r'\D','',name) or 256)//8
            elif re.fullmatch(r'bytes\d+',name):size=int(name[5:])
            else:raise ValueError('delegate_layout_unavailable_for:'+name)
            if offset+size>32:slot+=1;offset=0
            result[d['id']]=(slot,offset,('elementary',name));offset+=size
            if offset==32:slot+=1;offset=0
    return result


def expand(p,node,state,depth):
    kind=node.get('nodeType');route=None
    if kind=='VariableDeclarationStatement':route=('initialValue',)
    elif kind=='ExpressionStatement':
        call=node.get('expression',{})
        if call.get('nodeType')=='FunctionCall':route=('expression',)
        elif call.get('nodeType')=='Assignment' and call.get('operator')=='=':route=('expression','rightHandSide')
    if not route:return None
    call=node
    for k in route:call=call.get(k,{}) or {}
    exp=call.get('expression',{})
    if call.get('nodeType')!='FunctionCall' or exp.get('nodeType')!='MemberAccess' or exp.get('memberName')!='delegatecall':return None
    receiver=exp.get('expression',{})
    while receiver.get('nodeType')=='FunctionCall' and receiver.get('kind')=='typeConversion' and len(receiver.get('arguments',[]))==1:
        receiver=receiver['arguments'][0]
    if receiver.get('nodeType')!='Identifier':return None
    found=p.read_calls.created_type(receiver.get('referencedDeclaration'))
    if not found or len(call.get('arguments',[]))!=1:return None
    cid,_=found;payload=call['arguments'][0];abi=payload.get('expression',{})
    if abi.get('memberName')!='encodeWithSelector' or abi.get('expression',{}).get('name')!='abi':return None
    args=payload.get('arguments',[])
    if not args or args[0].get('memberName')!='selector':return None
    declaration=p.nodes.get(args[0].get('expression',{}).get('referencedDeclaration'),{})
    if declaration.get('nodeType')!='FunctionDefinition':return None
    target=p.read_calls.implementation(cid,declaration)
    if not target or not target.get('body') or depth>=8:return None
    if len(args)-1!=len(target.get('parameters',{}).get('parameters',[])):return None
    callee=next(c for c in p.bundle['contracts'] if c['name']==p.nodes[cid]['name'] and c['file']==p.anchor(p.nodes[cid])['file'])
    try:
        original=layout(p,p.contract);other=layout(p,callee);reverse={shape:rid for rid,shape in original.items()}
        mapping={rid:reverse[shape] for rid,shape in other.items() if shape in reverse}
        used={n.get('referencedDeclaration') for n in walk(target) if p.nodes.get(n.get('referencedDeclaration'),{}).get('stateVariable')}
        if not used<=set(mapping):return None
    except (ValueError,KeyError,StopIteration):return None
    actual=[p.expr(a,state) for a in args[1:]]
    saved=(p.current,p.read_calls.active_contract,getattr(p,'_delegate_storage_map',None),getattr(p,'_entry_selector',None))
    p.read_calls.active_contract=cid;p._delegate_storage_map=mapping;p._entry_selector=p.function_selector(target)
    outer_env=copy.deepcopy(state['env']);outer_return={k:copy.deepcopy(state[k]) for k in ('_return_ids','_return_pending','return_value') if k in state}
    try:children=p.invoke(target,actual,copy.deepcopy(state),depth+1)
    finally:p.current,p.read_calls.active_contract,p._delegate_storage_map,p._entry_selector=saved
    out=[]
    for child in children:
        success=child['flow'] in ('normal','returned')
        if child['flow']=='reverted':
            restored=copy.deepcopy(state);restored['guards']=child['guards'];restored['evaluated_terms']=child.get('evaluated_terms',[]);child=restored
        elif not success:out.append(child);continue
        child['flow']='normal';child['env']=copy.deepcopy(outer_env)
        for k in ('_return_ids','_return_pending','return_value'):child.pop(k,None)
        child.update(copy.deepcopy(outer_return))
        record={'source':p.anchor(call),'target':p.anchor(target),'call_mode':'DELEGATECALL',
            'binding':'fixed_created_code_explicit_selector_verified_storage_layout',
            'storage_context':p.contract['file']+':'+p.contract['name'],
            'callee_contract':cid,'storage_declaration_mapping':mapping,
            'sender_preserved':True,'outer_call_context_preserved':True,
            'callee_failure_rolls_back_callee_writes':True,'return_value':lit(success),
            'callpoint_writes':copy.deepcopy(state['writes']),'callpoint_guards':copy.deepcopy(state['guards'])}
        child.setdefault('resolved_calls',[]).append(record)
        val=lit(success) if call.get('typeDescriptions',{}).get('typeString')=='bool' else {
            'kind':'tuple','items':[lit(success),{'kind':'unknown','reason':'delegate_return_bytes_not_decoded'}]}
        replacement=copy.deepcopy(node);cursor=replacement
        for part in route[:-1]:cursor=cursor[part]
        cursor[route[-1]]={'nodeType':'V16EvaluatedValue','src':call.get('src'),'id':call.get('id'),'value':val}
        out.extend(p.statement(replacement,child,depth))
    return out

````

## source/src/pr_next_joint/frontend/dispatch.py

原文件 SHA-256 `b1eb4ebf67f30e20cd734287ed4f85777e312cd98846682828c50b45b3e67926`

````python
"""Unqualified ordinary-function dispatch from compiler-checked C3 inheritance."""
from pr_next_joint.frontend.source_entry_identity import function_kind
def resolve(lookup,target,contract_id=None,after=None):
    if not target or function_kind(target)!='function' or target.get('visibility')=='private':return target
    cid=contract_id or lookup.contract_node['id'];order=lookup.nodes[cid].get('linearizedBaseContracts',[cid])
    if target.get('scope') not in order:return target
    if after is not None:
        if after not in order:raise ValueError('P_SUPER_LEXICAL_SCOPE_NOT_IN_HIERARCHY')
        order=order[order.index(after)+1:]
    def signature(n):
        types=[p.get('typeDescriptions',{}).get('typeIdentifier') for p in n.get('parameters',{}).get('parameters',[])]
        return (n.get('name'),tuple(types)) if all(types) else None
    sig=signature(target)
    if sig is None:return target
    for owner in order:
        matches=[n for n in lookup.fns.values() if function_kind(n)=='function' and n.get('scope')==owner and n.get('visibility')!='private' and signature(n)==sig]
        if len(matches)>1:raise ValueError('internal_dispatch_ambiguous_source_signature')
        if matches and (after is None or matches[0].get('body')):return matches[0]
    if after is not None:raise ValueError('P_SUPER_CONCRETE_TARGET_NOT_FOUND')
    return target

def member_target(lookup,call,target):
    """Distinguish an internal base/super call from an external object method."""
    expr=call['expression'];base=expr.get('expression',{})
    if not target or expr.get('nodeType')!='MemberAccess' or call.get('names'):return None
    if not expr.get('typeDescriptions',{}).get('typeIdentifier','').startswith('t_function_internal_'):return None
    if base.get('nodeType') not in ('Identifier','IdentifierPath'):return None
    order=lookup.contract_node['linearizedBaseContracts']
    if base.get('referencedDeclaration') in order and target.get('scope') in order:
        return target
    if base.get('name')!='super' or 'super' not in base.get('typeDescriptions',{}).get('typeIdentifier',''):return None
    if not hasattr(lookup,'_lexical_call_scopes'):
        from pr_next_joint.frontend.path_ir import walk
        lookup._lexical_call_scopes={n['id']:f['scope'] for f in lookup.fns.values() if f.get('scope') in order
                                    for n in walk(f.get('body')) if n.get('nodeType')=='FunctionCall'}
    owner=lookup._lexical_call_scopes.get(call['id'])
    if owner is None:raise ValueError('P_SUPER_LEXICAL_SCOPE_UNRESOLVED')
    return resolve(lookup,target,lookup.read_calls.active_contract,after=owner)

import copy
from pr_next_joint.frontend.path_ir import key, op, lit, normalize, conditions_possible

def read_after_writes(selector,writes,guards):
    value=selector
    # Only direct equality facts are needed to simplify a key alias. Omitting
    # other guards is conservative: retain an ite when equality is not proved.
    equalities=[]
    def collect(g):
        if g.get('kind')=='op' and g.get('op') in ('and','&&'):
            for a in g['args']:collect(a)
        elif g.get('kind')=='op' and g.get('op') in ('==','!=') and all(a.get('kind') in ('actual_sender','parameter','literal','contract_address') for a in g['args']):equalities.append(g)
        elif g.get('kind')=='op' and g.get('op')=='!' and g['args'][0].get('kind')=='op' and g['args'][0].get('op') in ('==','!='):
            a=g['args'][0]
            if all(x.get('kind') in ('actual_sender','parameter','literal','contract_address') for x in a['args']):equalities.append(g)
    for g in guards:collect(g)
    for w in writes:
        p=w['path']
        if p['root']!=selector['root'] or key(p.get('instance'))!=key(selector.get('instance')):continue
        if [{k:v for k,v in x.items() if k!='key'} for x in p.get('segments',[])]!=[{k:v for k,v in x.items() if k!='key'} for x in selector.get('segments',[])]:continue
        a=[s['key'] for s in selector.get('segments',[]) if 'key' in s];b=[s['key'] for s in p.get('segments',[]) if 'key' in s]
        if len(a)!=len(b):continue
        if key(p)==key(selector):value=w['value'];continue
        same=normalize(op('and',*[op('==',x,y) for x,y in zip(a,b)]))
        if not conditions_possible(equalities,same):value=w['value']
        elif not conditions_possible(equalities+[same]):continue
        else:value=op('ite',same,copy.deepcopy(w['value']),value)
    return copy.deepcopy(value)

````

## source/src/pr_next_joint/frontend/facts.py

原文件 SHA-256 `0a5910b7efbb8db92d877cc0d72a5dc83bf07993d6769fe2ecd8dea5cda7ef5e`

````python
"""M1 compiler facts. No role inference by project, function or variable names."""
import hashlib,json,pathlib
from pr_next_joint.core import digest, require
from pr_next_joint.frontend.source_entry_identity import function_mutability

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

````

## source/src/pr_next_joint/frontend/inventory.py

原文件 SHA-256 `956796560fdb8f24d5d9e55544246caf9d70f83d6ca3462f7f33241f7b8f3a0a`

````python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""
from pr_next_joint.frontend.facts import walk

def target_inventory(bundle):
    nodes={(file,n['name']):n for file,ast in bundle['ast_sources'].items() for n in walk(ast) if n.get('nodeType')=='ContractDefinition'}
    compiled={(c['file'],c['name']):c for c in bundle['contracts']}
    result=[]
    for identity,node in sorted(nodes.items()):
        item={'file':identity[0],'contract':identity[1],'contract_kind':node['contractKind'],'abstract':bool(node.get('abstract'))}
        item['selected']=node['contractKind']=='contract' and not node.get('abstract') and identity in compiled
        item['reason']='concrete_compiled_contract' if item['selected'] else 'interface_library_abstract_or_no_creation_artifact'
        result.append(item)
    return result

````

## source/src/pr_next_joint/frontend/language.py

原文件 SHA-256 `9857dcaa4bd7097baeedd4d400adee7e60abd989ffe4f97fccf1a876a5e25301`

````python
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
    from pr_next_joint.frontend.path_ir import walk, lit
    decl=lookup.nodes.get(ref,{})
    if not decl.get('stateVariable'):return None
    value=decl.get('value');constructor_writer=None
    bases=set(lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']]))
    if decl.get('scope') not in bases:return None
    roots=[lookup.nodes[c] for c in bases]
    if value is None:
        assignments=[n for root in roots for n in walk(root) if n.get('nodeType')=='Assignment' and n.get('operator')=='=' and n.get('leftHandSide',{}).get('nodeType')=='Identifier' and n['leftHandSide'].get('referencedDeclaration')==ref]
        from pr_next_joint.frontend.source_entry_identity import function_kind
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
    # A runtime invariant is not an lvalue or a pre-write value while executing
    # the constructor which establishes it. Constants retain their source value.
    if getattr(lookup,'source_execution_context',{}).get('kind')=='constructor' and not lookup.nodes.get(ref,{}).get('constant'):
        return None
    cache=lookup.__dict__.setdefault('_source_fixed_storage_cache',{})
    if ref not in cache:cache[ref]=_source_fixed_storage(lookup,ref)
    return copy.deepcopy(cache[ref])

````

## source/src/pr_next_joint/frontend/local_constants.py

原文件 SHA-256 `8f6c667150cc172e2183310ed50c54449bd4432b880ac9622aa0fd1707698657`

````python
"""Pure compiler expressions, not inferred permission or safety."""
from fractions import Fraction
def constant_integer(node):
    """Bounded constant folding only; caller must establish compiler constant type."""
    budget=[128]
    def visit(n):
        budget[0]-=1
        if budget[0]<0:raise ValueError('constant_budget')
        k=n.get('nodeType')
        if k=='Literal' and n.get('kind')=='number':
            v=n.get('value','').replace('_','')
            value=Fraction(int(v,16)) if v.lower().startswith('0x') else Fraction(v)
            units={'wei':1,'szabo':10**12,'finney':10**15,'gwei':10**9,'ether':10**18,'seconds':1,'minutes':60,'hours':3600,'days':86400,'weeks':604800,'years':31536000}
            if n.get('subdenomination'):
                value*=units[n['subdenomination']]
            return value
        if k=='TupleExpression' and len(n.get('components',[]))==1:return visit(n['components'][0])
        if k=='UnaryOperation' and n.get('operator') in ('+','-'):
            value=visit(n['subExpression']);return value if n['operator']=='+' else -value
        if k=='BinaryOperation':
            a,b=visit(n['leftExpression']),visit(n['rightExpression']);op=n.get('operator')
            if op=='+':return a+b
            if op=='-':return a-b
            if op=='*':return a*b
            if op=='/' and b:return a/b
            if op=='**' and b.denominator==1 and 0<=b<=1024 and abs(a.numerator).bit_length()*int(b)<=8192:return a**int(b)
            if op=='%' and a.denominator==b.denominator==1 and b:return a%b
        raise ValueError('not_a_supported_constant')
    try:
        value=visit(node)
        return value.numerator if value.denominator==1 else None
    except (ValueError,KeyError,ZeroDivisionError,OverflowError):return None

def pure_message_argument(node,lookup):
    # Reading a string variable cannot call out or change storage. Indexing,
    # concatenation, function calls and computed error arguments are not erased.
    if node.get('nodeType')=='Literal':return True
    if node.get('nodeType')=='Identifier':
        decl=lookup.nodes.get(node.get('referencedDeclaration'),{})
        typ=decl.get('typeDescriptions',{}).get('typeString','')
        return decl.get('nodeType')=='VariableDeclaration' and typ.startswith(('string','bytes '))
    return False

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
    from pr_next_joint.verification.typed_integer import integer_type
    integer=integer_type(typ)
    if integer is None or value.get('kind')!='literal' or type(value.get('value')) is not int:return None
    signed,bits=integer;result=value['value']%(2**bits)
    if signed and result>=2**(bits-1):result-=2**bits
    return {'kind':'literal','value':result}


def constant_local_update(lookup,node,value,state,source,operator):
    from pr_next_joint.verification.typed_integer import integer_type, checked_mode
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
    from pr_next_joint.frontend.source_bindings import observe
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
    from pr_next_joint.frontend.path_ir import walk
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

````

## source/src/pr_next_joint/frontend/native_facts.py

原文件 SHA-256 `3417d735fcd64b2b77a5ece89e1182b8caf431893c56662ce1ffeff6e905aa52`

````python
"""Serialize fresh Slither SSA with original source anchors, no classifier."""
import sys
from importlib.metadata import version

def source(x):
 s=x.source_mapping
 return {'file':str(s.filename.relative),'start':s.start,'length':s.length,'lines':s.lines}
def variable(v):return {'name':str(v),'class':type(v).__name__,'type':str(getattr(v,'type',None)),'canonical_name':getattr(v,'canonical_name',None)}
def extract(slither,bundle,receipt):
 functions=[]
 for contract in slither.contracts:
  for f in contract.functions_and_modifiers_declared:
   nodes=[]
   for n in f.nodes:
    ops=[]
    for ir in n.irs_ssa:
     op={'operation':type(ir).__name__,'text':str(ir),'reads':[variable(v) for v in ir.read],'lvalue':variable(ir.lvalue) if getattr(ir,'lvalue',None) is not None else None}
     for k in ['variable_left','variable_right','function','arguments']:
      if hasattr(ir,k):op[k]=[str(a) for a in ir.arguments] if k=='arguments' else str(getattr(ir,k))
     ops.append(op)
    nodes.append({'id':n.node_id,'type':str(n.type),'source':source(n),'expression':str(n.expression),'ssa':ops,'successors':[s.node_id for s in n.sons]})
   functions.append({'contract':contract.name,'signature':f.full_name,'canonical_name':f.canonical_name,'source':source(f),'visibility':f.visibility,'parameters':[variable(v) for v in f.parameters],'reads':[v.canonical_name for v in f.all_state_variables_read()],'writes':[v.canonical_name for v in f.all_state_variables_written()],'modifiers':[m.canonical_name for m in f.modifiers],'nodes':nodes})
 return {'program_id':bundle['program_id'],'build_id':bundle['build_id'],'python':sys.version,'slither':version('slither-analyzer'),'crytic_compile':version('crytic-compile'),'compiler':receipt,'functions':functions,'ssa_operation_count':sum(len(n['ssa']) for f in functions for n in f['nodes']),'fresh':True}

````

