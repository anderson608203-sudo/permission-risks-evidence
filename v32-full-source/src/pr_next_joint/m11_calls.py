"""Compiler-bound internal library calls and native CALL syntax.
No assumed token implementation or transfer-name matching.
"""
import copy
from .m03_p_paths import key,walk,op,lit,conditions_possible
from .source_entry_identity import function_mutability,builtin_call
from .m03_p_calls import boolean_union

def bound_library(lookup,node,target):
    from .source_library_binding import compiler_bound_receiver
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
    from .m10_dispatch import member_target,resolve
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
        from .m26_condition_paths import contains_effect_call
        if not contains_effect_call(p,call):return None
    from .m26_condition_paths import values
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
        from .m10_dispatch import member_target
        target=member_target(p,call,target)
        if target is None:return None
    source_args=bind_arguments(p,call,target)
    if source_args is None:return None
    arguments=([expr['expression']] if bound else [])+source_args
    if any(n.get('nodeType') in ('Assignment',) or n.get('nodeType')=='UnaryOperation' and n.get('operator') in ('++','--','delete') or n.get('nodeType')=='FunctionCall' and n.get('kind')!='typeConversion' for n in walk(arguments)):return None
    if not bound and expr.get('nodeType')=='Identifier':
        from .m10_dispatch import resolve
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
