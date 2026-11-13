"""Bounded value copies and local composite assignments, never storage aliases."""
import copy
from .m03_p_paths import key,lit
def snapshot(value,typ,lookup,state,depth=0):
    if depth>8:raise ValueError('memory_snapshot_depth_limit')
    if value.get('kind')!='storage':return copy.deepcopy(value)
    if typ.get('nodeType')=='ArrayTypeName':
        length=typ.get('length') or {}
        if length.get('nodeType')!='Literal':raise ValueError('dynamic_storage_to_memory_snapshot_not_lowered')
        size=int(length['value'])
        if size>32:raise ValueError('memory_snapshot_array_bound')
        return {'kind':'array','items':[snapshot({**value,'segments':value.get('segments',[])+[{'key':lit(i)}]},typ['baseType'],lookup,state,depth+1) for i in range(size)]}
    if typ.get('nodeType')=='UserDefinedTypeName':
        node=lookup.nodes.get(typ.get('referencedDeclaration'),{})
        if node.get('nodeType')!='StructDefinition':raise ValueError('memory_snapshot_user_type_unresolved')
        return {'kind':'record','fields':[{'field':f['id'],'value':snapshot({**value,'segments':value.get('segments',[])+[{'field':f['id']}]},f['typeName'],lookup,state,depth+1)} for f in node['members']]}
    result=copy.deepcopy(value)
    from .m03_p_paths import op
    for write in state['writes']:
        path=write['path']
        if path.get('root')!=value.get('root') or key(path.get('instance'))!=key(value.get('instance')):continue
        left=path.get('segments',[]);right=value.get('segments',[])
        if len(left)!=len(right):raise ValueError('memory_snapshot_overlapping_container_write')
        conditions=[];same=True
        for x,y in zip(left,right):
            if 'key' in x and 'key' in y:conditions.append(op('==',x['key'],y['key']))
            elif x!=y:same=False;break
        if not same:continue
        if key(path)==key(value):result=copy.deepcopy(write['value'])
        elif conditions:result={'kind':'conditional','condition':op('and',*conditions),'when_true':copy.deepcopy(write['value']),'when_false':result}
    return result
def local_root(node,lookup):
    if node.get('nodeType')=='Identifier':
        decl=lookup.nodes.get(node.get('referencedDeclaration'),{})
        return decl['id'] if decl.get('storageLocation')=='memory' and not decl.get('stateVariable') else None
    if node.get('nodeType')=='MemberAccess':return local_root(node.get('expression',{}),lookup)
    if node.get('nodeType')=='IndexAccess':return local_root(node.get('baseExpression',{}),lookup)
    return None
def assign(node,value,lookup,state):
    if node.get('nodeType')=='Identifier':state['env'][node['referencedDeclaration']]=copy.deepcopy(value);return
    if node.get('nodeType')=='MemberAccess':
        parent=lookup.evaluate(node['expression'],state['env'])
        if parent.get('kind')!='record':raise ValueError('memory_record_write_not_lowered')
        revised=copy.deepcopy(parent);field=next((x for x in revised['fields'] if x['field']==node.get('referencedDeclaration')),None)
        if field is None:raise ValueError('memory_record_field_unresolved')
        field['value']=copy.deepcopy(value);assign(node['expression'],revised,lookup,state);return
    if node.get('nodeType')=='IndexAccess':
        parent=lookup.evaluate(node['baseExpression'],state['env']);index=lookup.value(node['indexExpression'],state['env'])
        if parent.get('kind')!='array' or index.get('kind')!='literal' or type(index.get('value')) is not int or not 0<=index['value']<len(parent['items']):raise ValueError('memory_array_write_not_lowered')
        revised=copy.deepcopy(parent);revised['items'][index['value']]=copy.deepcopy(value);assign(node['baseExpression'],revised,lookup,state);return
    raise ValueError('memory_assignment_shape_not_lowered')
