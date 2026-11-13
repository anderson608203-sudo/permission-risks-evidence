"""Separate failure, declared-expiry and revocation questions for credentials.

All references have passed the existing source carrier. No prose matching,
new source discovery, hash injectivity or signature forgery premise is used.
"""
import copy
from .m03_p_paths import key,walk,op,lit,conditions_possible
from .m03_p_route import keys,fields,value_type,selectors
from .m04_logic import Unsupported
from .m05_mechanism_core import (solve,scalar_write,remap,post,retime,successful,
    execution_terms,reject_changed_selector_keys)
from .m05_credential_encoding import certify_total_digest


def replace_exact(value,before,after):
    if isinstance(value,dict):
        if key(value)==key(before):return copy.deepcopy(after)
        return {k:replace_exact(v,before,after) for k,v in value.items()}
    return [replace_exact(v,before,after) for v in value] if isinstance(value,list) else value


def check_invalid_zero(obligation,lookup,fn,pi,path,credential):
    rows=[];gaps=[]
    if fn!=obligation['function']:return rows,gaps
    declared=obligation['original_proposal'].get('mechanism',{}).get('credential',{})
    protected=declared.get('protected_effect_source_ast_id') if isinstance(declared,dict) else None
    accepted=[]
    for n in walk(path['guards']):
        if n.get('kind')!='op' or n.get('op')!='==' or len(n['args'])!=2:continue
        for recovered,authority in (n['args'],n['args'][::-1]):
            if (key(recovered)==key(credential) and authority.get('kind')=='storage'
                    and value_type(authority,lookup) in ('address','address payable')
                    and not conditions_possible(path['guards'],n)):
                accepted.append(n)
    if not accepted or type(protected) is not int or protected not in obligation['source_ast_ids']:
        return [],[{'reason':'invalid_signature_authority_and_protected_effect_not_bound',
                   'function':fn,'path_index':pi,'dimension':'invalid_ecrecover_r_zero_return_accepted'}]
    for wi,raw in enumerate(path['writes']):
        if raw.get('source',{}).get('ast_id')!=protected:continue
        try:
            effect=scalar_write(raw,lookup)
            evaluated=execution_terms(path,lookup)
            model={'kind':'credential_invalid_r_zero_acceptance','function':fn,'path_index':pi,
                'write_index':wi,'credential':credential,'conditions':path['guards'],
                'effect':effect,'writes':path['writes'],'same_payload_certificate':False,
                'successful_evaluation':evaluated,'authority_acceptance':accepted,
                'protected_effect_source_ast_id':protected,
                'graph':{'engine':'source relation DAG','edges':[['source_ecrecover','r_zero_failure'],
                    ['r_zero_failure','source_authority_guard'],['source_authority_guard','protected_write']]},
                'checked_dimensions':['invalid_ecrecover_r_zero_return_accepted'],
                'unchecked_dimensions':['other_invalid_signature_inputs','valid_credential_protocol'],
                'policy_scope':'source_builtin_failure_return',
                'assumptions':['only r==0 sufficient precompile failure branch',
                    'source digest evaluation is total and irrelevant to recovery under r==0',
                    'bounded source pre-state; no signature forgery or deployment proof']}
            def construct(e,m):
                c=m['credential'];certify_total_digest(e,c['digest'])
                if len(c['signature'])!=3:raise Unsupported('credential_recovery_arity')
                _,r,_=[e.expr(x) for x in c['signature']]
                guards=replace_exact(m['conditions'],c,lit(0))
                writes=replace_exact(m['writes'],c,lit(0))
                selected=replace_exact(m['effect'],c,lit(0))
                evaluated=replace_exact(m['successful_evaluation'],c,lit(0))
                acceptance=replace_exact(m['authority_acceptance'],c,lit(0))
                if any(n.get('kind') in ('hash','credential_recovery') for n in walk([guards,writes,selected,evaluated])):
                    raise Unsupported('invalid_recovery_has_other_hash_dependency')
                for value in evaluated:e.expr(value)
                return r==0,e.z.And(*[e.expr(g) for g in guards+acceptance],
                    e.expr(selected['value'])!=e.expr(selected['path']))
            rows.append(solve(lookup,obligation,fn,model,construct,effect['path']['root'],
                keys(effect['path'])[0] if keys(effect['path']) else None))
        except (Unsupported,ValueError,TypeError,KeyError) as ex:
            gaps.append({'reason':str(ex),'dimension':'invalid_ecrecover_r_zero_return_accepted',
                         'function':fn,'path_index':pi,'write_index':wi})
    return rows,gaps


def relations(obligation):
    credential=obligation['original_proposal'].get('mechanism',{}).get('credential',{})
    if not isinstance(credential,dict):return []
    result=credential.get('validity_relations',[])
    if not isinstance(result,list):raise Unsupported('credential_validity_relations_not_list')
    return result


def origin(relation,obligation):
    kind=relation.get('basis_kind')
    if kind not in ('program_relation','normal_description','combined'):
        raise Unsupported('credential_validity_basis_missing')
    if kind in ('normal_description','combined') and not obligation['basis_assessment']['normal_description_available']:
        raise Unsupported('credential_validity_description_not_provided')
    return {'declared_relation':copy.deepcopy(relation),'proposal_sha256':obligation['proposal_sha256'],
            'interpretation':'explicit M2 credential policy, not a proof of unique business intent'}


def same_payload_scope(values,*credentials):
    hashes={key(n) for c in credentials for n in walk(c['digest']) if n.get('kind')=='hash'}
    recoveries={key(c) for c in credentials}
    if any(n.get('kind')=='hash' and key(n) not in hashes or
           n.get('kind')=='credential_recovery' and key(n) not in recoveries for n in walk(values)):
        raise Unsupported('credential_validity_has_independent_cryptographic_dependency')


def check_declared_validity(obligation,lookup,paths,fn,pi,path,credential,effect,base,same_payload):
    rows=[];gaps=[]
    if fn!=obligation['function']:return rows,gaps
    try:declared=relations(obligation)
    except (Unsupported,ValueError,TypeError,KeyError) as ex:return [],[{'reason':str(ex),'function':fn}]
    for relation_index,relation in enumerate(declared):
        from .m05_question_trace import question_id
        qid=question_id(obligation,'credential.validity_relations',relation_index,relation)
        try:
            if not isinstance(relation,dict):raise Unsupported('credential_validity_relation_not_object')
            evidence=origin(relation,obligation)
            if relation.get('kind')=='upper_time_bound':
                source=relation.get('deadline_source_ast_id')
                found={key(n):n for n in walk(credential['digest']) if
                    n.get('kind') in ('parameter','storage') and n.get('id',n.get('root'))==source}
                if len(found)!=1:raise Unsupported('credential_expiry_signed_term_not_unique')
                deadline=next(iter(found.values()))
                typ=value_type(deadline,lookup) if deadline['kind']=='storage' else deadline.get('type','')
                if not str(typ).startswith('uint'):raise Unsupported('credential_expiry_not_unsigned_time')
                comparison=relation.get('comparison')
                if comparison not in ('<','<='):raise Unsupported('credential_expiry_boundary_not_explicit')
                if relation['basis_kind']=='program_relation':
                    from .m05_credential_temporal import upper_time_bounds
                    if not any(key(b['deadline'])==key(deadline) and b['strict']==(comparison=='<')
                               for b in upper_time_bounds(path['guards'])):
                        raise Unsupported('credential_expiry_policy_requires_explicit_normal_description')
                later={'kind':'environment','field':'timestamp','type':'uint256','invocation':'declared_credential_later_use'}
                second=retime(path,later);other=retime(effect,later);second_credential=retime(credential,later)
                first_evaluation=execution_terms(path,lookup);second_evaluation=execution_terms(second,lookup)
                if (effect['path']['root']!=other['path']['root'] or fields(effect['path'])!=fields(other['path'])
                        or key(effect['path'].get('instance'))!=key(other['path'].get('instance'))
                        or len(keys(effect['path']))!=len(keys(other['path']))):
                    raise Unsupported('credential_expiry_resource_shape_changed')
                model={**copy.deepcopy(base),'kind':'credential_declared_expiry_use','conditions':path['guards'],
                    'alternative_conditions':second['guards'],'alternative_credential':second_credential,
                    'alternative_effect':other,'deadline':deadline,'strict_deadline':comparison=='<',
                    'original_time':{'kind':'environment','field':'timestamp'},'later_time':later,
                    'writes':path['writes'],'alternative_writes':second['writes'],'validity_relation_origin':evidence,
                    'successful_evaluation':first_evaluation,'alternative_evaluation':second_evaluation,
                    'question_refs':[qid],
                    'checked_dimensions':['same_issued_credential_use_after_declared_expiry'],
                    'assumptions':base['assumptions']+['explicitly sourced expiry is a policy hypothesis',
                        'valid unused credential before expiry; later alternative use is not a prior-use replay']}
                same_payload_scope([path['guards'],first_evaluation,second['guards'],second_evaluation,effect,other],
                                   credential,second_credential)
                def expiry(e,m):
                    e0=m['effect'];e1=m['alternative_effect'];c0=m['credential'];c1=m['alternative_credential']
                    t0=e.expr(m['original_time']);t1=e.expr(m['later_time']);d=e.expr(m['deadline'])
                    for value in m['successful_evaluation']+m['alternative_evaluation']:e.expr(value)
                    initial=e.z.And(*[e.expr(g) for g in m['conditions']],e.expr(c0)!=0,
                        t0<d if m['strict_deadline'] else t0<=d,e.expr(e0['value'])!=e.expr(e0['path']),t1>=t0)
                    violation=e.z.And(same_payload(e,c0,c1),t1>=d if m['strict_deadline'] else t1>d,
                        *[e.expr(a)==e.expr(b) for a,b in zip(keys(e0['path']),keys(e1['path']))],
                        *[e.expr(g) for g in m['alternative_conditions']],e.expr(e1['value'])!=e.expr(e1['path']))
                    return initial,violation
                rows.append(solve(lookup,obligation,fn,model,expiry,effect['path']['root'],
                    keys(effect['path'])[0] if keys(effect['path']) else None))
            elif relation.get('kind')=='revocable_boolean':
                source=relation.get('validity_source_ast_id');operation=relation.get('revocation_operation',{})
                pair=(operation.get('target'),operation.get('function'))
                if pair[0]!=obligation['target'] or not any((r['target'],r['function'])==pair for r in obligation['related_operations']):
                    raise Unsupported('credential_revocation_operation_not_bound_in_current_target')
                selected={key(s):s for s in selectors(path) if s['root']==source and value_type(s,lookup)=='bool'}
                if not selected:
                    # A scalar declared validity flag can be missing entirely
                    # from consumption; its declaration must already be in the
                    # accepted obligation, never discovered by name.
                    node=lookup.nodes.get(source,{})
                    bases=lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
                    if (node.get('stateVariable') is True and node.get('scope') in bases
                            and node.get('typeName',{}).get('name')=='bool'):
                        s={'kind':'storage','root':source,'segments':[]};selected[key(s)]=s
                if len(selected)!=1:raise Unsupported('credential_revocation_validity_selector_not_unique')
                valid=next(iter(selected.values()));made=False
                t0={'kind':'environment','field':'timestamp'}
                tr={'kind':'environment','field':'timestamp','type':'uint256','invocation':'credential_revoke_time'}
                tu={'kind':'environment','field':'timestamp','type':'uint256','invocation':'credential_after_revoke_time'}
                later_path=retime(path,tu);later_credential=retime(credential,tu);later_effect=retime(effect,tu)
                for ri,revoke in enumerate(paths.get(pair[1],[])):
                    if not successful(revoke) or revoke['issues']:continue
                    mapping={n['id']:{**n,'invocation':'credential_revocation'} for n in walk(revoke) if n.get('kind')=='parameter'}
                    transition=retime(remap(revoke,mapping,{'kind':'transition_caller','type':'address','invocation':'credential_revocation'}),tr)
                    if not any(key(w['path'])==key(valid) and scalar_write(w,lookup)['value']==lit(False) for w in transition['writes']):continue
                    if any(n.get('kind') in ('hash','credential_recovery') for n in walk(transition)):
                        raise Unsupported('credential_revocation_independent_crypto_not_modeled')
                    reject_changed_selector_keys([later_path,valid],transition['writes'])
                    before_evaluation=execution_terms(path,lookup)
                    revoke_evaluation=execution_terms(transition,lookup)
                    after_evaluation=post(execution_terms(later_path,lookup),transition['writes'],lookup)
                    model={**copy.deepcopy(base),'kind':'credential_revoked_boolean_use','conditions':path['guards'],
                        'validity_before':valid,'validity_after':post(valid,transition['writes'],lookup),
                        'revocation_conditions':transition['guards'],'revocation_writes':transition['writes'],
                        'post_credential':post(later_credential,transition['writes'],lookup),
                        'post_conditions':post(later_path['guards'],transition['writes'],lookup),
                        'post_effect':post(later_effect['value'],transition['writes'],lookup),
                        'post_selector':post(later_effect['path'],transition['writes'],lookup),
                        'post_writes':post(later_path['writes'],transition['writes'],lookup),
                        'successful_evaluation':before_evaluation,'revocation_evaluation':revoke_evaluation,
                        'post_evaluation':after_evaluation,'lifecycle_times':[t0,tr,tu],
                        'question_refs':[qid],
                        'validity_relation_origin':evidence,'revocation_function':pair[1],'revocation_path_index':ri,
                        'checked_dimensions':['same_issued_credential_use_after_bound_boolean_revocation'],
                        'assumptions':base['assumptions']+['explicit bool validity policy; unused credential revoked before use',
                            'same-target exact existing selector; no arbitrary state-machine or key-rotation inference']}
                    same_payload_scope([model['conditions'],model['post_conditions'],model['post_writes'],
                        model['effect'],model['post_effect'],model['post_selector'],before_evaluation,after_evaluation],credential,model['post_credential'])
                    def revoked(e,m):
                        before=m['effect'];c=m['credential']
                        for value in m['successful_evaluation']+m['revocation_evaluation']+m['post_evaluation']:e.expr(value)
                        t0,tr,tu=[e.expr(t) for t in m['lifecycle_times']]
                        initial=e.z.And(e.expr(m['validity_before']),*[e.expr(g) for g in m['conditions']],
                            *[e.expr(g) for g in m['revocation_conditions']],e.expr(c)!=0,
                            t0<=tr,tr<=tu,
                            e.expr(before['value'])!=e.expr(before['path']))
                        violation=e.z.And(e.z.Not(e.expr(m['validity_after'])),
                            same_payload(e,c,m['post_credential']),*[e.expr(g) for g in m['post_conditions']],
                            e.expr(m['post_effect'])!=e.expr(m['post_selector']))
                        return initial,violation
                    rows.append(solve(lookup,obligation,fn,model,revoked,effect['path']['root'],
                        keys(effect['path'])[0] if keys(effect['path']) else None));made=True
                if not made:raise Unsupported('credential_revocation_exact_false_transition_not_bound')
            else:raise Unsupported('credential_validity_relation_kind_not_supported')
        except (Unsupported,ValueError,TypeError,KeyError) as ex:
            gaps.append({'reason':str(ex),'function':fn,'path_index':pi,'validity_relation':copy.deepcopy(relation),'question_id':qid})
    return rows,gaps
