"""Path-local observations for source references. No role or permission inference."""
import copy
from .m03_p_paths import key,walk
from .m05_relation_model_scope import source_term

def observe(path,node,value,env):
    if not node or node.get('id') is None:return
    ids=[node['id']]
    if node.get('nodeType')=='Identifier' and node.get('referencedDeclaration') in env:
        ids.append(node['referencedDeclaration'])
    table=path.setdefault('_source_value_bindings',{})
    for identity in ids:
        row=table.setdefault(str(identity),[])
        if not any(key(x)==key(value) for x in row):
            # Repeated evaluation with different values is ambiguous, never last-write-wins.
            if len(row)<2:row.append(copy.deepcopy(value))

def path_key(path):
    from .core import digest
    return digest([path.get('guards'),path.get('writes'),path.get('flow'),path.get('_source_value_bindings'),path.get('_source_lvalue_bindings')])

def observe_lvalue(path,node,value):
    if node and node.get('id') is not None and value.get('kind')=='storage':
        table=path.setdefault('_source_lvalue_bindings',{});row=table.setdefault(str(node['id']),[])
        if not any(key(x)==key(value) for x in row) and len(row)<2:row.append(copy.deepcopy(value))

def resolve(node,lookup,function,path,purpose=None):
    observed=path.get('_source_lvalue_bindings',{}).get(str(node['id'])) if purpose=='resource' else None
    if observed is None:observed=path.get('_source_value_bindings',{}).get(str(node['id']))
    if observed is not None:
        if len(observed)!=1:raise ValueError('source_reference_has_multiple_values_on_path')
        value=copy.deepcopy(observed[0])
    else:value=source_term(node,lookup,function)
    if value is None or any(x.get('kind') in ('unknown','call_unresolved') for x in walk(value)):
        raise ValueError('source_expression_not_lowered')
    return value

def rows_for(compiled,field,fn,path=None,pi=None):
    result=[]
    for row in compiled[field]:
        if row['function']!=fn:continue
        if pi is not None and pi not in row.get('path_indices',[pi]):continue
        if path is not None and row.get('path_key')!=path_key(path):continue
        result.append(row)
    return result


def resolve_condition(node,lookup,function,path):
    """Resolve a cited predicate, never a statement's dummy return value.
    Only compiler-bound require/assert wrappers are unwrapped. Scalar references
    remain scalars and are rejected by the typed implication boundary.
    """
    from .source_entry_identity import builtin_call
    if node.get('nodeType')=='ExpressionStatement':
        return resolve_condition(node.get('expression',{}),lookup,function,path)
    if builtin_call(node,lookup,('require','assert')) and node.get('arguments'):
        return resolve_condition(node['arguments'][0],lookup,function,path)
    if node.get('nodeType')=='IfStatement':
        # Existing projection only accepts a source-established reverting branch;
        # it preserves its polarity rather than guessing which branch is legal.
        value=source_term(node,lookup,function)
        if value is None:raise ValueError('statement_does_not_identify_an_applicability_predicate')
        return value
    return resolve(node,lookup,function,path)
