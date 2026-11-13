"""Shared typed state updates; source writes, not label-specific transitions."""
import copy
from .m03_p_paths import key,op,lit
from .m03_p_lifecycle import leaves
from .m03_p_route import value_type
from .m03_p_assets import deltas
from .m04_logic import Unsupported


def enum_size(lookup,typ):
    if not isinstance(typ,str) or not typ.startswith('enum '):return None
    name=typ[5:]
    found=[n for n in lookup.nodes.values() if n.get('nodeType')=='EnumDefinition'
           and (n.get('canonicalName')==name or n.get('name')==name)]
    if len(found)!=1:raise Unsupported('enum_declaration_not_unique:'+name)
    size=len(found[0]['members'])
    if not 0<size<=256:raise Unsupported('enum_domain_size')
    return size


def scalar(write,lookup):
    if write['value'].get('kind')!='zero_of_storage_type':return write
    typ=value_type(write['path'],lookup)
    if typ=='bool':zero=False
    elif typ and (typ.startswith(('uint','bytes','enum ')) or typ in ('address','address payable')):zero=0
    else:raise Unsupported('container_delete_not_scalar')
    return {**write,'value':lit(zero),'zeroing_source_operator':write.get('operator')}


def changes(path,lookup):
    """Use a shared before/after delta for assignment, subtraction and delete."""
    writes=[]
    for w in path['writes']:
        expanded=leaves(w)
        if not expanded:raise Unsupported('state_write_not_scalarized')
        writes.extend(scalar(x,lookup) for x in expanded)
    return deltas({**path,'writes':writes})


def expand_write(write,lookup,depth=0):
    """Expand deletion of an already bound finite struct; no source discovery."""
    if depth>8:raise Unsupported('finite_delete_structure_depth')
    if write['value'].get('kind')=='record':
        return [x for leaf in leaves(write) for x in expand_write(leaf,lookup,depth+1)]
    if write['value'].get('kind')!='zero_of_storage_type':return [write]
    typ=lookup.nodes.get(write['path']['root'],{}).get('typeName',{})
    for segment in write['path'].get('segments',[]):
        typ=typ.get('valueType',{}) if 'key' in segment else lookup.nodes.get(segment['field'],{}).get('typeName',{})
    declaration=lookup.nodes.get(typ.get('referencedDeclaration'),{})
    if declaration.get('nodeType')!='StructDefinition':return [scalar(write,lookup)]
    result=[]
    for member in declaration.get('members',[]):
        if member.get('typeName',{}).get('nodeType') in ('Mapping','ArrayTypeName'):
            raise Unsupported('finite_delete_dynamic_member_not_modeled')
        path={**write['path'],'segments':write['path'].get('segments',[])+[{'field':member['id']}]}
        result+=expand_write({**write,'path':path,'expanded_delete_source':copy.deepcopy(write['path'])},lookup,depth+1)
    if not result:raise Unsupported('finite_delete_empty_structure')
    return result


def compose_read(value,writes,lookup):
    """Source-keyed read-over-write, including updates to an aliased key."""
    from .m03_p_route import fields,keys
    from .m03_p_paths import normalize
    if isinstance(value,dict):
        if value.get('kind')=='storage':
            result=copy.deepcopy(value)
            for w in writes:
                w=scalar(w,lookup);p=w['path']
                if p['root']!=value['root'] or fields(p)!=fields(value) or key(p.get('instance'))!=key(value.get('instance')):continue
                a,b=keys(value),keys(p)
                if len(a)!=len(b):raise Unsupported('transition_selector_arity')
                if any(x.get('kind')=='fixed_bytes_literal' and y.get('kind')=='fixed_bytes_literal' for x,y in zip(a,b)):
                    from .m29_keys import selector_equalities
                    tests=selector_equalities(value,p,lookup)
                else:
                    tests=[op('==',x,y) for x,y in zip(a,b)]
                same=normalize(op('and',*tests))
                result=w['value'] if same==lit(True) else op('ite',same,w['value'],result)
            return result
        return {k:compose_read(v,writes,lookup) for k,v in value.items()}
    return [compose_read(v,writes,lookup) for v in value] if isinstance(value,list) else value


def control_type(typ):
    return typ=='bool' or bool(typ and typ.startswith(('uint','enum ')))


def control_contribution(condition, writes, control, lookup):
    """Contrast full updates with the declared control held at its old value.

    Both expressions use the same original pre-state and the same other writes.
    This is a scoped dependency test, not a claim that the contrast state is an
    executable transaction. Matching reuses the existing typed selector shape.
    """
    from .m03_p_route import fields
    selected = [w for w in writes if w['path']['root'] == control['root']
                and fields(w['path']) == fields(control)
                and key(w['path'].get('instance')) == key(control.get('instance'))]
    if not selected:
        raise Unsupported('control_contribution_without_bound_write')
    others = [w for w in writes if w not in selected]
    return {'post_action': compose_read(condition, writes, lookup),
            'reference_post_action': compose_read(condition, others, lookup),
            'control_writes': copy.deepcopy(selected), 'retained_other_writes': copy.deepcopy(others),
            'scope': 'control-state contribution with other source write expressions held fixed'}


def consumed_control_with_asset(writes, control, asset_root, lookup):
    """A matching numeric debit may consume quota, not disable transfers.

    This does not prove legitimate consent. It identifies a remaining policy
    distinction so a control consumer does not label routine consumption freeze.
    Only already typed, source-bound updates and signed deltas are compared.
    """
    from .m03_p_route import fields
    updates=changes({'writes':writes},lookup)
    controls=[d for d in updates if d['write']['path']['root']==control['root']
              and fields(d['write']['path'])==fields(control)
              and key(d['write']['path'].get('instance'))==key(control.get('instance'))]
    debits=[d for d in updates if d['write']['path']['root']==asset_root and d['delta']
            and all(v<0 for v in d['delta'].values())]
    return any(c['delta'] and c['delta']==d['delta'] for c in controls for d in debits)
