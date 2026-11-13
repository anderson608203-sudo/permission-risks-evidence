"""D01: qualify a borrowed authorization before proving its violation.
No labels or LLM conclusions are consulted. Failure here is a missing policy
basis, not evidence that the operation is safe.
"""
import copy
from .m03_p_paths import key, walk, normalize
from .m03_p_route import effective_permission, value_type
from .m04_logic import Unsupported


def substitute(v, bindings):
    if isinstance(v, dict):
        if key(v) in bindings:return copy.deepcopy(bindings[key(v)])
        return {k:substitute(x, bindings) for k,x in v.items()}
    return [substitute(x, bindings) for x in v] if isinstance(v,list) else v


def compatible(parameter, actual, lookup):
    typ=parameter.get('type')
    if actual.get('kind')=='actual_sender':return typ in ('address','address payable')
    if actual.get('kind')=='parameter':return typ==actual.get('type')
    if actual.get('kind')=='storage':return typ==value_type(actual,lookup)
    if actual.get('kind')=='literal':
        v=actual.get('value')
        if isinstance(v,bool):return typ=='bool'
        if isinstance(v,int):
            if typ in ('address','address payable'):return 0<=v<2**160
            if typ and typ.startswith('uint') and typ[4:].isdigit():return 0<=v<2**int(typ[4:])
    return bool(typ and typ==actual.get('type'))


def unify(source, actual, bindings, lookup):
    if key(source)==key(actual):return True
    if isinstance(source,dict) and source.get('kind')=='parameter' and isinstance(actual,dict):
        k=key(source)
        if k in bindings:return key(bindings[k])==key(actual)
        if not compatible(source,actual,lookup):return False
        bindings[k]=copy.deepcopy(actual);return True
    if isinstance(source,dict) and isinstance(actual,dict):
        return source.keys()==actual.keys() and all(unify(source[k],actual[k],bindings,lookup) for k in source)
    if isinstance(source,list) and isinstance(actual,list):
        return len(source)==len(actual) and all(unify(a,b,bindings,lookup) for a,b in zip(source,actual))
    return source==actual


def atoms(values):
    out=[]
    for v in values:
        if v.get('kind')=='op' and v.get('op') in ('and','&&'):out.extend(atoms(v['args']))
        elif not (v.get('kind')=='literal' and v.get('value') is True):out.append(v)
    return out


def borrowed_policy_is_not_stronger(required, supported):
    # Added OR alternatives weaken this obligation; AND additions cannot be
    # justified by one matching source permission.
    if key(normalize(required))==key(normalize(supported)):return True
    return required.get('kind')=='op' and required.get('op') in ('or','||') and any(
        borrowed_policy_is_not_stronger(x,supported) for x in required['args'])


def payload(effect):
    if 'path' in effect:
        return {'selector':effect['path'],'value':effect['value'],'operator':effect.get('operator','=')}
    if effect.get('selector',{}).get('kind')=='storage':
        return {'selector':effect['selector'],'value':effect.get('value'),'operator':effect.get('operator','=')}
    # Preserve the actual affected amount, recipient, code target and arguments.
    # A common reserve or operation name alone never matches.
    return {k:v for k,v in effect.items() if k not in ('source','scope','object','selector')}


def qualify(query,state):
    from .m21_policy import source_origin
    tid=query['target'];lookup=state['lookups'][tid];origin=source_origin(query)
    required=query.get('required_policy_candidate',{});effect=query.get('effect',{})
    target_paths=state['paths'].get((tid,query['function']),[]);pi=query.get('path_index')
    if type(pi)is not int or not 0<=pi<len(target_paths):return None,{'reason':'target_path_identity_missing'}
    target=target_paths[pi]
    if target.get('issues') or target.get('evaluation_gaps'):
        return None,{'reason':'target_operation_not_fully_bound','issues':target.get('issues',[])}
    selector=effect.get('selector',{})
    # A scalar address used as an actual caller authority is not merely a
    # co-occurring resource. The existing direct replacement rule covers it.
    # Keep its projected duplicate only when it requires that same authority.
    if selector.get('kind')=='storage' and not selector.get('segments') and value_type(selector,lookup) in ('address','address payable'):
        from .m20_policy import role_evidence
        from .m03_p_paths import op
        permission=op('==',{'kind':'actual_sender'},selector)
        program={f:ps for (t,f),ps in state['paths'].items() if t==tid}
        evidence=role_evidence(lookup,program,selector)
        if evidence and borrowed_policy_is_not_stronger(required,permission):
            return {'kind':'source_authority_state_replacement','authority':selector,'authority_uses':evidence,
                    'effect_source':effect.get('source'),'scope':'this authority only; stage and initialization exclusions run first'},None
    if not origin:return None,{'reason':'source_operation_identity_missing'}
    selected=query.get('policy_basis',{}).get('origin_path_index');attempts=[]
    for oi,source in enumerate(state['paths'].get((tid,origin),[])):
        if selected is not None and selected!=oi:continue
        if source['flow'] not in ('normal','returned') or source.get('issues') or source.get('evaluation_gaps'):
            attempts.append({'source_path_index':oi,'reason':'source_path_incomplete'});continue
        try:permissions=effective_permission(source['guards'],lookup)
        except (Unsupported,ValueError):permissions=[]
        if not permissions:continue
        possible=source['writes'] if selector.get('kind')=='storage' else source.get('sensitive_effects',[])
        for se in possible:
            binding={}
            if not unify(payload(se),payload(effect),binding,lookup):
                from .m24_equivalence import equivalent_effect
                binding=equivalent_effect(lookup,payload(se),payload(effect))
                if binding is None:continue
            matched=[p for p in permissions if borrowed_policy_is_not_stronger(required,substitute(p,binding))]
            if not matched:
                attempts.append({'source_path_index':oi,'reason':'operation_matches_but_authority_does_not'});continue
            permission_atoms={key(normalize(x)) for x in atoms(permissions)}
            remaining=[substitute(g,binding) for g in atoms(source['guards']) if key(normalize(g)) not in permission_atoms]
            # Additional caller/business/stage conditions on either path are
            # not silently erased. Exact normalized agreement is sufficient,
            # not necessary; unmodelled equivalence remains a recorded limit.
            a=sorted(key(normalize(g)) for g in remaining)
            b=sorted(key(normalize(g)) for g in atoms(target['guards']))
            from .m24_equivalence import equivalent_conditions
            equivalent=(a==b or equivalent_conditions(lookup,remaining,target['guards']))
            if not equivalent:
                attempts.append({'source_path_index':oi,'reason':'operation_stage_or_business_conditions_differ',
                    'source_nonpermission_conditions':remaining,'target_conditions':target['guards']});continue
            return {'kind':'source_equivalent_operation_authorization','origin_function':origin,
                    'origin_path_index':oi,'origin_effect_source':se.get('source'),'target_effect_source':effect.get('source'),
                    'source_effect':payload(se),'target_effect':payload(effect),'parameter_bindings':binding,
                    'source_permission':matched[0],'mapped_permission':substitute(matched[0],binding),
                    'nonpermission_conditions':remaining,'condition_alignment':'normalized_identity' if a==b else 'proved_bidirectional_implication',
                    'scope':'source-grounded local policy inference; not unique business intent or global safety proof'},None
    return None,{'reason':'shared_resource_without_qualified_operation_authorization','attempts':attempts,
                 'unmodelled_operation_equivalence_remains_possible':True}
