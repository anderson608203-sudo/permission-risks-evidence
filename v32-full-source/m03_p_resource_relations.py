"""Infer a resource policy through values stored by a guarded operation.

Example structural relation: guarded create(key, domain) stores domain in a
record. Reuse that policy on the domain of the affected record, not an unrelated
caller-supplied domain. This is an inferred policy, not a business invariant proof.
"""
import copy
from .m03_p_paths import clean,key,walk


def stored_values(write):
    def descend(path,value):
        if value.get('kind')=='record':
            for field in value['fields']:
                yield from descend({**path,'segments':path['segments']+[{'field':field['field']}]},field['value'])
        else:yield path,value
    return list(descend(write['path'],write['value']))


def project_policy(peer,target_write,target_function):
    source=peer['write']['path'];target=target_write['path']
    if source['root']!=target['root'] or key(source.get('instance'))!=key(target.get('instance')):
        raise ValueError('P_RESOURCE_INSTANCE_MISMATCH')
    # A policy on one field is not automatically a policy on every field
    # of the containing struct. Whole-record assignments retain their scope.
    source_fields=[x['field'] for x in source['segments'] if 'field' in x]
    target_fields=[x['field'] for x in target['segments'] if 'field' in x]
    if source_fields and source_fields!=target_fields:
        raise ValueError('P_PEER_EFFECT_FIELD_DIFFERS')
    if peer['function']==target_function:
        return copy.deepcopy(peer['policy']),[]
    # Appending a newly allocated record and editing an existing record are
    # different roles. Reusing the creator's guard requires separate evidence.
    source_keys=[x['key'] for x in source['segments'] if 'key' in x]
    if peer['write']['value'].get('kind')=='record' and any(k.get('kind')=='storage' and k.get('root')==source['root'] and any(s.get('length') for s in k.get('segments',[])) for k in source_keys):
        raise ValueError('P_ALLOCATION_POLICY_NOT_EXISTING_OBJECT_POLICY')
    left=[x['key'] for x in source['segments'] if 'key' in x]
    right=[x['key'] for x in target['segments'] if 'key' in x]
    if len(left)!=len(right):raise ValueError('P_RESOURCE_KEY_ARITY')
    substitutions={}
    for a,b in zip(left,right):
        # Resource-key alignment must never turn msg.sender into a recipient.
        # Only the origin's formal object parameter can be rebound.
        if a.get('kind')=='parameter':
            if key(a) in substitutions and key(substitutions[key(a)])!=key(b):raise ValueError('P_KEY_BINDING_CONFLICT')
            substitutions[key(a)]=b
        elif key(a)!=key(b):
            # A scalar caller policy remains meaningful across account keys;
            # a policy that uses that account as its resource does not.
            if any(key(a)==key(k) for s in walk(peer['policy']) if s.get('kind')=='storage' for seg in s.get('segments',[]) for k in [seg.get('key',{})]):
                raise ValueError('P_RESOURCE_SUBJECT_IDENTITY_UNRESOLVED')
    relations=[];bindings={}
    needed={key(x) for x in walk(peer['policy']) if x.get('kind')=='parameter'}
    # Only non-key values actually written into a record may supply the missing
    # policy argument. A same-typed unused parameter supplies no relation.
    for path,value in stored_values(peer['write']):
        if value.get('kind')!='parameter' or key(value) in substitutions or key(value) not in needed:continue
        segments=[];ki=0
        for seg in path['segments']:
            if 'key' in seg:
                if ki>=len(right):raise ValueError('P_RELATION_KEY_ARITY')
                segments.append({'key':right[ki]});ki+=1
            else:segments.append(seg)
        projected={**path,'segments':segments}
        if not any('field' in x for x in segments):continue
        bindings.setdefault(key(value),[]).append(projected)
    for parameter,choices in bindings.items():
        choices={key(x):x for x in choices}
        if len(choices)!=1:raise ValueError('P_RESOURCE_FIELD_RELATION_AMBIGUOUS')
        selector=next(iter(choices.values()))
        # Do not silently infer a before-state ownership requirement for an
        # operation replacing the association itself; that needs its own policy.
        target_fields=[x.get('field') for x in target['segments'] if 'field' in x]
        relation_fields=[x.get('field') for x in selector['segments'] if 'field' in x]
        if not target_fields or target_fields==relation_fields:
            raise ValueError('P_RESOURCE_ASSOCIATION_REPLACEMENT_UNRESOLVED')
        substitutions[parameter]=selector
        relations.append({'basis':'guarded_operation_stores_permission_argument',
                          'origin_function':peer['function'],'origin_source':peer['write']['source'],
                          'parameter':parameter,'affected_resource_field':selector})
    def sub(v):
        if isinstance(v,dict):
            if key(v) in substitutions:return copy.deepcopy(substitutions[key(v)])
            if v.get('kind')=='parameter':raise ValueError('P_POLICY_PARAMETER_UNBOUND')
            return {k:sub(x) for k,x in v.items()}
        return [sub(x) for x in v] if isinstance(v,list) else v
    result=sub(peer['policy'])
    used=[r for r in relations if any(key(x)==key(r['affected_resource_field']) for x in walk(result))]
    return clean(result),used
