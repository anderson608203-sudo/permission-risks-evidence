"""Source-derived credential self-composition across instances and actions."""
import copy
from .m03_p_paths import walk,key,op,lit
from .m03_p_route import keys
from .m04_logic import Unsupported
from .m05_mechanism_core import successful,scalar_write,solve

def instance(value,identity):
    if isinstance(value,dict):
        result={k:instance(v,identity) for k,v in value.items()}
        if value.get('kind') in ('storage','contract_address'):
            result['instance']={'credential_domain':identity,'original':value.get('instance')}
        return result
    return [instance(v,identity) for v in value] if isinstance(value,list) else value

def check_domains(obligation,lookup,paths,fn,path,pi,credential,effect,base,same_payload,recoveries):
    rows=[];root=effect['path']['root'];holder=keys(effect['path'])[0] if keys(effect['path']) else None
    other=instance(path,'second_instance');other_credential=instance(credential,'second_instance')
    other_effect=instance(effect,'second_instance')
    own_address={'kind':'contract_address','instance':{'kind':'root_instance','contract':lookup.contract_node['id']}}
    model={**base,'kind':'credential_cross_instance_binding','second_instance':other,
           'conditions':path['guards'], 'second_credential':other_credential,'second_effect':other_effect,
           'own_address':own_address,'other_address':instance(own_address,'second_instance'),
           'instance_policy':'inferred instance-specific entitlement; shared deployment authority is a premise',
           'assumptions':base['assumptions']+['two same-code instances with valid compatible pre-states; cross-instance credential use hypothesized to require separation']}
    def formula(e, inputs):
        path={'guards': inputs['conditions']}; other=inputs['second_instance']
        credential=inputs['credential']; other_credential=inputs['second_credential']
        effect=inputs['effect']; other_effect=inputs['second_effect']
        z=e.z
        original=z.And(*[e.expr(g) for g in path['guards']])
        second=z.And(*[e.expr(g) for g in other['guards']])
        equal=same_payload(e,credential,other_credential)
        separate=e.expr(inputs['own_address'])!=e.expr(inputs['other_address'])
        return z.And(original,e.expr(credential)!=0,e.expr(effect['value'])!=e.expr(effect['path']),separate),z.And(equal,second,e.expr(other_effect['value'])!=e.expr(other_effect['path']))
    rows.append(solve(lookup,obligation,fn,model,formula,root,holder))
    # Different operations sharing one credential format are alternative uses,
    # not a sequential replay after the nonce has already been consumed.
    for other_fn,branches in paths.items():
        if other_fn==fn:continue
        for oi,alternative in enumerate(branches):
            if not successful(alternative) or alternative['issues']:continue
            cs=recoveries(alternative['guards'])
            if len(cs)!=1:continue
            for w in alternative['writes']:
                if w['path']['root']==root:continue
                # Only materially different resources are checked here;
                # matching roots need a richer operation/field policy.
                alt=scalar_write(w,lookup)
                from .m05_credential_obligations import nonce_bookkeeping
                if nonce_bookkeeping(alt,cs[0],alternative['guards']):continue
                if any(key(n)==key(alt['path']) for n in walk(cs[0]['digest'])):continue
                model={**base,'kind':'credential_cross_action_binding','alternative_function':other_fn,
                       'alternative_path':oi,'alternative_effect':alt,'alternative_conditions':alternative['guards'],
                       'conditions':path['guards'], 'alternative_credential':cs[0],
                       'assumptions':base['assumptions']+['distinct resource effects are hypothesized to require action-specific consent; legitimate multi-action credentials remain a policy alternative']}
                def formula(e, inputs):
                    credential=inputs['credential']; cs=[inputs['alternative_credential']]
                    path={'guards':inputs['conditions']}; alternative={'guards':inputs['alternative_conditions']}
                    effect=inputs['effect']; alt=inputs['alternative_effect']
                    z=e.z
                    equal=same_payload(e,credential,cs[0])
                    return z.And(*[e.expr(g) for g in path['guards']],e.expr(credential)!=0,
                                 e.expr(effect['value'])!=e.expr(effect['path'])),z.And(equal,*[e.expr(g) for g in alternative['guards']],e.expr(alt['value'])!=e.expr(alt['path']))
                try:rows.append(solve(lookup,obligation,fn,model,formula,root,holder))
                except Unsupported:continue
    return rows
