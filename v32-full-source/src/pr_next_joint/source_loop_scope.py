"""Choose expansion from a proven constant source counter, never sample identity."""
from .source_scalar_semantics import constant_integer

def loop_limit(node, lookup, state, maximum=32):
    if node.get('nodeType')!='ForStatement':return 2
    condition=node.get('condition') or {};update=(node.get('loopExpression') or {}).get('expression',{})
    left=condition.get('leftExpression',{});right=condition.get('rightExpression',{})
    ident=left.get('referencedDeclaration');initial=state.get('env',{}).get(ident,{})
    if left.get('nodeType')!='Identifier' or initial.get('kind')!='literal' or type(initial.get('value')) is not int:return 2
    stop=constant_integer(right)
    if stop is None:return 2
    if update.get('nodeType')!='UnaryOperation' or update.get('subExpression',{}).get('referencedDeclaration')!=ident:return 2
    step=1 if update.get('operator')=='++' else -1 if update.get('operator')=='--' else 0
    from .m03_p_paths import walk
    for item in walk(node.get('body')):
        dest=item.get('leftHandSide',{}) if item.get('nodeType')=='Assignment' else item.get('subExpression',{}) if item.get('nodeType')=='UnaryOperation' and item.get('operator') in ('++','--','delete') else {}
        if dest.get('referencedDeclaration')==ident:return 2
    operator=condition.get('operator');start=initial['value']
    if step==1 and operator in ('<','<='):count=max(0,stop-start+(operator=='<='))
    elif step==-1 and operator in ('>','>='):count=max(0,start-stop+(operator=='>='))
    else:return 2
    return min(maximum,count) if count<=maximum else 2


def invariant_local_condition(node,lookup):
    """A local scalar test untouched by the loop, with no successful exit.

    Used to avoid repeatedly expanding a source loop whose true branch cannot
    reach its continuation. The branch remains truncated, never assumed safe.
    Old view declarations alone do not suffice: inspect every called body.
    """
    from .m03_p_paths import walk
    from .source_entry_identity import function_mutability,builtin_call
    condition=node.get('condition') or {};ref=condition.get('referencedDeclaration')
    declaration=lookup.nodes.get(ref,{})
    if condition.get('nodeType')!='Identifier' or declaration.get('stateVariable') or declaration.get('typeDescriptions',{}).get('typeString')!='bool':return False
    content=[node.get('body'),node.get('loopExpression')];seen=set()
    def safe(items,depth=0):
        if depth>8:return False
        for item in walk(items):
            k=item.get('nodeType')
            if k in ('Break','Return','InlineAssembly','NewExpression','EmitStatement'):return False
            dest=item.get('leftHandSide',{}) if k=='Assignment' else item.get('subExpression',{}) if k=='UnaryOperation' and item.get('operator') in ('++','--','delete') else {}
            if dest.get('referencedDeclaration')==ref:return False
            if k=='FunctionCall' and item.get('kind') not in ('typeConversion','structConstructorCall'):
                if builtin_call(item,lookup,('require','assert','revert')):continue
                target=lookup.fns.get(item.get('expression',{}).get('referencedDeclaration'))
                if not target or function_mutability(target) not in ('pure','view') or not target.get('body'):return False
                # Return inside a pure/read-only helper ends only that helper.
                if target['id'] in seen:return False
                seen.add(target['id'])
                body=target['body']
                for n in walk(body):
                    if n.get('nodeType') in ('NewExpression','InlineAssembly','EmitStatement'):return False
                    mutation=(n.get('leftHandSide') if n.get('nodeType')=='Assignment' else n.get('subExpression') if n.get('nodeType')=='UnaryOperation' and n.get('operator') in ('++','--','delete') else None)
                    if mutation:
                        d=lookup.nodes.get(mutation.get('referencedDeclaration'),{})
                        if mutation.get('nodeType')!='Identifier' or d.get('nodeType')!='VariableDeclaration' or d.get('stateVariable') or d.get('storageLocation')=='storage':return False
                # Library arithmetic helpers may return, but no other calls
                # may hide global termination or mutation in old compilers.
                calls=[n for n in walk(body) if n.get('nodeType')=='FunctionCall']
                if not safe(calls,depth+1):return False
                seen.remove(target['id'])
        return True
    return safe(content)
