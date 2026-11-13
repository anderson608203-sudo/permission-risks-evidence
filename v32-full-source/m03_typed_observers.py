"""Lower typed M1/M2 permission selectors and complete object observations.

This builds observations/expressions, not transactions or policy applicability.
It uses compiler-bound getters and the existing expression language. No RPC,
raw storage slots, constructor-owner assumption, case names or risk relabeling.
"""
import copy
from .core import require, digest, lit, obs, operator, expression
from .source_observers import bind_getter


def _address(value):
    expression(lit('Address160',value))
    return value.lower()


def _key(value, parameters, sender):
    kind=value.get('kind')
    if kind=='actual_sender':return sender
    if kind=='parameter':
        require(value['id'] in parameters,'permission_parameter_unbound')
        return parameters[value['id']]
    if kind=='literal':return value['value']
    raise ValueError('permission_key_expression_not_supported:'+str(kind))


def _selector_path(lookup, selector):
    require(selector.get('kind')=='state_selector','permission_state_selector_required')
    require(selector['program_id']==lookup.bundle['program_id'] and selector['build_id']==lookup.bundle['build_id'],
            'permission_selector_build_identity')
    iid=lookup.contract['file']+':'+lookup.contract['name']
    require(selector['instance_id']==iid,'permission_selector_instance_requires_adapter')
    state=lookup.decls.get(selector['declaration_id'])
    require(state is not None and state.get('stateVariable'),'permission_selector_declaration')
    segments=[]
    for s in selector['segments']:
        if 'key' in s:segments.append({'key':copy.deepcopy(s['key'])})
        elif 'field_id' in s:segments.append({'field':s['field_id']})
        else:raise ValueError('permission_selector_segment')
    return {'kind':'storage','root':state['id'],'segments':segments}


def lower_permission(lookup, condition, *, sender, parameter_values, point):
    """Return exact Bool permission expression and getter observer definitions.

    `point` is the caller-verified authorization decision snapshot. The caller
    must insert these definitions into the actual plan for this same instance.
    Parameter values must come from that plan, not a model's invented binding.
    """
    require(type(point) is int and point>=1,'permission_decision_point')
    sender=_address(sender);bindings={};registry={};cache={}
    def lower(node):
        kind=node.get('kind')
        if kind=='actual_sender':return lit('Address160',sender)
        if kind=='state_selector':
            path=_selector_path(lookup,node)
            args=[_key(s['key'],parameter_values,sender) for s in node['segments'] if 'key' in s]
            binding=bind_getter(lookup,path,args)
            claimed=node.get('value_type')
            expected={'address':'Address160','address payable':'Address160','bool':'Bool',
                      'uint256':'BV256','bytes32':'BV256'}.get(claimed)
            require(expected is not None and binding['type']==expected,'permission_selector_value_type')
            identity=digest({'path':path,'arguments':args})
            if identity not in cache:
                oid='permission_'+str(len(cache));cache[identity]=oid
                bindings[oid]=binding
                registry[oid+'.'+str(point)]={'type':binding['type'],'point':point}
            return obs(cache[identity]+'.'+str(point),binding['type'])
        if kind=='literal':
            value=node['value']
            if type(value) is bool:return lit('Bool',value)
            if type(value) is int:return lit('BV256',value)
            if isinstance(value,str) and len(value)==42:return lit('Address160',_address(value))
            raise ValueError('permission_literal_type_unsupported')
        require(kind=='op','permission_term_not_supported')
        mapping={'==':'eq','!=':'ne','and':'and','&&':'and','or':'or','||':'or','!':'not','not':'not'}
        require(node.get('op') in mapping,'permission_operator_not_supported')
        return operator(mapping[node['op']],'Bool',*(lower(x) for x in node['args']))
    allowed=lower(condition)
    require(expression(allowed,registry,point=point)[0]=='Bool','permission_must_be_boolean')
    return {'policy_allowed':allowed,'observer_bindings':bindings,
            'observers':[{'id':oid,'caller':sender,**b['observer_fields']} for oid,b in bindings.items()],
            'observer_registry':registry,'decision_point':point,
            'instance_id':lookup.contract['file']+':'+lookup.contract['name'],
            'policy_applicability_verified':False,'original_execution_performed':False}


def lower_object_effect(lookup, object_selector, *, field_ids, sender, parameter_values, before, after):
    """Observe all declared flat fields for field_ids=None; never narrow silently.

    The same object keys are used before/after. `+=` or other write arithmetic
    is not interpreted here: values come from original-program observations.
    """
    require(type(before) is int and type(after) is int and 1<=before<after,'effect_observation_points')
    sender=_address(sender);path=_selector_path(lookup,object_selector)
    require(all('key' in s for s in path['segments']),'effect_object_path_must_exclude_field')
    state=lookup.decls[path['root']];typ=state['typeName']
    while typ.get('nodeType')=='Mapping':typ=typ['valueType']
    node=lookup.nodes.get(typ.get('referencedDeclaration'),{})
    require(node.get('nodeType')=='StructDefinition','effect_flat_struct_required')
    members={m['id']:m for m in node['members']}
    wanted=list(members) if field_ids is None else list(field_ids)
    require(wanted and len(wanted)==len(set(wanted)) and set(wanted)<=set(members),'effect_field_identity')
    args=[_key(s['key'],parameter_values,sender) for s in object_selector['segments'] if 'key' in s]
    bindings={};changes=[];registry={}
    for ident in wanted:
        field_path=copy.deepcopy(path);field_path['segments'].append({'field':ident})
        binding=bind_getter(lookup,field_path,args)
        oid='object_field_'+str(ident);bindings[oid]=binding
        for point in (before,after):registry[oid+'.'+str(point)]={'type':binding['type'],'point':point}
        changes.append(operator('ne','Bool',obs(oid+'.'+str(after),binding['type']),obs(oid+'.'+str(before),binding['type'])))
    changed=changes[0] if len(changes)==1 else operator('or','Bool',*changes)
    expression(changed,registry,point=after)
    return {'effect_expression':changed,'observer_bindings':bindings,
            'observers':[{'id':oid,'caller':sender,**b['observer_fields']} for oid,b in bindings.items()],
            'observer_registry':registry,'field_ids':wanted,
            'scope':'whole_object' if field_ids is None else 'explicit_fields',
            'instance_id':lookup.contract['file']+':'+lookup.contract['name'],
            'original_execution_performed':False}
