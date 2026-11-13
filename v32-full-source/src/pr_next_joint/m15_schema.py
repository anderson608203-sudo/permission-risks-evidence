"""Optional typed relationships: syntax/identity only, never semantic approval."""
import json
FIELDS=('actor_bindings','resource_bindings','condition_bindings','operation_links','authorization_hypotheses')
ROLES=('caller','holder','delegate','governor','nominee','recipient','beneficiary','approver','payer')
LINKS=('nomination_acceptance','authorization_use','same_holder_conversion','authorization_revocation','approval_execution')

def normalize_scope(row,ops,refs,target,error):
    def ref(x):
        if not isinstance(x,str) or x not in refs or refs[x]['target']!=target:raise error('scoped_reference_identity_mismatch')
        return x
    def operation(x):
        if not isinstance(x,str) or x not in ops or ops[x]['target']!=target:raise error('scoped_operation_identity_mismatch')
        return x
    out={}
    for field in FIELDS:
        items=row.get(field,[])
        if not isinstance(items,list):raise error(field+'_not_array')
        values=[]
        for item in items:
            if not isinstance(item,dict):raise error(field+'_not_object')
            if field=='actor_bindings':
                if item.get('role') not in ROLES:raise error('actor_role_not_allowed')
                v={'role':item['role'],'ref':ref(item.get('ref')),'op_ref':operation(item.get('op_ref'))}
            elif field=='resource_bindings':
                v={'resource_ref':ref(item.get('resource_ref')),'op_ref':operation(item.get('op_ref'))}
                for name in ('holder_ref','quantity_ref'):
                    v[name]=None if item.get(name) is None else ref(item[name])
                keys=item.get('key_refs',[])
                if not isinstance(keys,list):raise error('key_refs_not_array')
                # Key order is semantic: owner->spender cannot be sorted.
                v['key_refs']=[ref(x) for x in keys]
            elif field=='condition_bindings':
                v={'condition_ref':ref(item.get('condition_ref')),'op_ref':operation(item.get('op_ref'))}
            elif field=='authorization_hypotheses':
                if item.get('kind') not in ('existing_authority','holder_consent','threshold_approval','single_initialization'):raise error('authorization_hypothesis_kind')
                evidence=item.get('source_refs');conditions=item.get('condition_refs',[])
                if not isinstance(evidence,list) or not evidence or not isinstance(conditions,list):raise error('authorization_hypothesis_evidence')
                v={'kind':item['kind'],'op_ref':operation(item.get('op_ref')),
                   'actor_ref':ref(item.get('actor_ref')),'resource_ref':ref(item.get('resource_ref')),
                   'effect_ref':ref(item.get('effect_ref')),'source_refs':sorted(set(ref(x) for x in evidence)),
                   'condition_refs':sorted(set(ref(x) for x in conditions))}
            else:
                if item.get('kind') not in LINKS:raise error('operation_link_kind_not_allowed')
                evidence=item.get('source_refs')
                if not isinstance(evidence,list) or not evidence:raise error('operation_link_evidence_missing')
                v={'kind':item['kind'],'from_op_ref':operation(item.get('from_op_ref')),
                   'to_op_ref':operation(item.get('to_op_ref')),'source_refs':sorted(set(ref(x) for x in evidence))}
                if v['kind']!='same_holder_conversion' and v['from_op_ref']==v['to_op_ref']:raise error('operation_link_requires_distinct_stages')
            if set(item)-set(v):raise error('unknown_scoped_field')
            values.append(v)
        out[field]=sorted({json.dumps(x,sort_keys=True):x for x in values}.values(),key=lambda x:json.dumps(x,sort_keys=True))
    return out
