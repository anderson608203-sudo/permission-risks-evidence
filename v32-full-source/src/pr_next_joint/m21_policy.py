"""Canonical source policy provenance and one applicability boundary.
Source relations are hypotheses. A rejection is not a whole-operation proof.
"""
import copy
from .core import digest
from .m03_p_paths import key, normalize
from .m03_p_route import effective_permission, selectors, fields
from .m04_logic import Unsupported

PROJECTED = {
    'same_resource_guarded_operation','source_checked_M2_relation',
    'credential_management_edges_to_same_family','v20_semantic_source_authority',
    'same_source_native_reserve_guard','same_source_delegate_target_guard','observed_guard',
    'alias_creation_links_to_current_resource_permission'
}

def basis_kind(q):
    b=q.get('policy_basis',{})
    return b.get('basis') or b.get('relation') or b.get('kind')

def source_origin(q):
    b=q.get('policy_basis',{});ev=b.get('evidence',{})
    return b.get('origin_function') or b.get('peer') or ev.get('origin_function')

def _same_family(a,b):
    return a.get('root')==b.get('root') and key(a.get('instance'))==key(b.get('instance')) and fields(a)==fields(b)

def source_records(q,state):
    tid=q['target'];lookup=state['lookups'][tid];origin=source_origin(q)
    if not origin:return []
    effect=q.get('effect',{});selector=effect.get('selector',{})
    b=q.get('policy_basis',{});chosen=b.get('origin_path_index')
    cache=state.setdefault('_policy_source_cache',{})
    cache_key=key([tid,origin,chosen,selector.get('root'),selector.get('instance'),fields(selector),effect.get('kind')])
    if cache_key in cache:return list(cache[cache_key])
    matches=[]
    for pi,p in enumerate(state['paths'].get((tid,origin),[])):
        if chosen is not None and pi!=chosen:continue
        if p['flow'] not in ('normal','returned'):continue
        effects=[{'selector':w['path'],'source':w['source']} for w in p['writes'] if _same_family(w['path'],selector)]
        if selector.get('kind')!='storage':
            effects=[{'kind':e['kind'],'source':e['source']} for e in p.get('sensitive_effects',[])
                     if e['kind']==effect.get('kind') or effect.get('kind')=='protected_delegate_entry' and e['kind']=='dangerous_external_call']
        if not effects:continue
        try:predicates=effective_permission(p['guards'],lookup)
        except (Unsupported,ValueError):predicates=[]
        record={'target':tid,'function':origin,'path_index':pi,'source_conditions':p['guards'],
                'permission_predicates':predicates,'effects':effects,
                'branch_choices':p.get('branch_choices',[]),'issues':p.get('issues',[]),
                'policy_is_source_hypothesis_not_business_specification':True}
        rid='policy_source_'+digest(record)[:24]
        state.setdefault('_policy_source_registry',{})[rid]=record
        matches.append(rid)
    cache[cache_key]=tuple(matches)
    return matches

def gate(q,state,shared,index):
    from .m20_policy import gate as local_gate
    kind=basis_kind(q);origin=source_origin(q)
    q['authorization_obligation']={
        'source_kind':kind,'origin_function':origin,
        'source_record_ids':source_records(q,state),
        'subject_and_resource_terms':copy.deepcopy(selectors(q.get('required_policy_candidate',{}))),
        'operation':{'target':q['target'],'function':q['function'],'path_index':q.get('path_index'),
                     'effect_source':q.get('effect',{}).get('source')},
        'initial_required_policy':copy.deepcopy(q.get('required_policy_candidate')),
        'source_inference_or_direct_mechanism':'projected_hypothesis' if kind in PROJECTED else 'specific_source_mechanism',
        'sat_does_not_establish_business_policy':True}
    from .m23_initialization import unreachable_initialization
    from .m25_authority import holder_sale
    sale=holder_sale(q,state,shared)
    if sale:
        q['authorization_obligation']['decision']=sale['decision']
        return q,sale
    closed=unreachable_initialization(q,state)
    if closed:
        q['authorization_obligation']['decision']=closed['decision']
        return q,closed
    # The graph producer stores provenance in evidence; normalize it before all
    # existing stage/authorization consumers, not only one selected exclusion.
    canonical=copy.deepcopy(q)
    if origin:canonical.setdefault('policy_basis',{})['origin_function']=origin
    if kind in ('credential_management_edges_to_same_family','v20_semantic_source_authority'):
        canonical['policy_basis']['basis']='source_checked_M2_relation'
    if kind in PROJECTED:
        # Same-function alternate paths can contain legitimate business routes.
        # Do not transplant a branch atom as an exclusive policy.
        from .m10_applicability import route_for
        selector=q.get('effect',{}).get('selector',{})
        if origin and selector.get('kind')=='storage':
            lookup=state['lookups'][q['target']]
            route=route_for(lookup,origin,q.get('required_policy_candidate',{}),selector)
            if route:
                q['authorization_obligation']['decision']='source_branch_not_exclusive_authorization'
                return q,{'decision':'source_branch_not_exclusive_authorization',
                    'source_certificate':route,'not_safety_certificate':True,
                    'scope':'only this branch predicate projected as exclusivity; independent duties remain'}
    allowance_stage=allowance_stage_alternative(canonical,state,shared)
    if allowance_stage:
        canonical['authorization_obligation']['decision']=allowance_stage['decision']
        return canonical,allowance_stage
    from .m23_subject_scope import participant_scope
    participant=participant_scope(canonical,state)
    if participant:
        canonical['authorization_obligation']['decision']=participant['decision']
        return canonical,participant
    from .m22_authorization import managed_record_subject, paid_authority_transition
    subject_selection=managed_record_subject(canonical,state) or paid_authority_transition(canonical,state) or managed_list_subject(canonical,state)
    if subject_selection:
        canonical['authorization_obligation']['decision']=subject_selection['decision']
        return canonical,subject_selection
    canonical,alternative=local_gate(canonical,state,shared,index)
    # Preserve original provenance; only the checked current predicate and
    # applicability result may change. No M2 verdict or caller intent is copied.
    original_basis=q.get('policy_basis',{})
    canonical['policy_basis']=original_basis
    canonical['authorization_obligation']['effective_required_policy']=copy.deepcopy(canonical.get('required_policy_candidate'))
    canonical['authorization_obligation']['decision']=alternative.get('decision') if alternative else 'retained_conditional_source_obligation'
    if alternative:
        alternative=copy.deepcopy(alternative)
        if alternative.get('decision')=='unsupported_authorization_projection':
            alternative['assessment_kind']='policy_not_established'
        else:alternative['assessment_kind']='source_normal_or_inapplicable_policy'
    if not alternative and kind in PROJECTED:
        from .m21_admission import qualify
        certificate,limit=qualify(canonical,state)
        admission={'decision':'source_operation_authorization_admitted' if certificate else 'cooccurrence_only_policy_not_admitted',
                   'certificate':certificate,'limit':limit,'approved_decision':'D01'}
        canonical['authorization_obligation']['admission']=admission
        canonical['authorization_obligation']['decision']=admission['decision']
        if not certificate:
            alternative={'decision':admission['decision'],'assessment_kind':'policy_not_established',
                         'source_certificate':admission,'not_safety_certificate':True,
                         'scope':'candidate preserved; borrowed authorization lacks operation-specific support'}
    return canonical,alternative

def identical_program_obligation(original,current):
    """An earlier P certificate cannot certify a subsequently changed query."""
    names=('conditions','required_policy_candidate','effect','source_evaluation_terms')
    return (not current.get('issues') and not current.get('commit_effect') and
            all(key(original.get(k))==key(current.get(k)) for k in names))

def managed_list_subject(query,state):
    """A source-bound list search selects a managed object, not the caller.
    Requires independent caller authorization and the matched list-cell mutation.
    It does not discharge that manager's authorization or any other operation.
    """
    from .m03_p_paths import op,lit
    from .m03_p_route import keys,effective_permission,selectors,value_type
    from .m09_shared_policy import implies
    b=query.get('policy_basis',{})
    if b.get('basis')!='caller_selected_authorization_subject':return None
    observed=b.get('observed',{})
    if observed.get('kind')!='op' or observed.get('op')!='==' or len(observed.get('args',[]))!=2:return None
    matches=[(a,c) for a,c in (observed['args'],observed['args'][::-1])
             if a.get('kind')=='parameter' and a.get('type') in ('address','address payable')
             and c.get('kind')=='storage']
    if len(matches)!=1:return None
    subject,cell=matches[0];lookup=state['lookups'][query['target']]
    decl=lookup.nodes.get(cell['root'],{})
    if decl.get('typeName',{}).get('nodeType')!='ArrayTypeName' or len(keys(cell))!=1:return None
    if value_type(cell,lookup) not in ('address','address payable'):return None
    paths=state['paths'].get((query['target'],query['function']),[])
    pi=query.get('path_index')
    if type(pi)is not int or not 0<=pi<len(paths):return None
    p=paths[pi]
    if p['issues'] or p.get('evaluation_gaps'):return None
    managers=[g for g in effective_permission(p['guards'],lookup)
              if selectors(g) and all(s['root']!=cell['root'] for s in selectors(g))]
    if not managers:return None
    wanted=op('==',{'kind':'actual_sender'},cell)
    try:
        if not implies(lookup,p,op('==',query['required_policy_candidate'],wanted)):return None
    except (Unsupported,ValueError):return None
    matched=[w for w in p['writes'] if key(w['path'])==key(cell)]
    # The query must concern the selected cell or associated length update.
    length=[w for w in p['writes'] if w['path']['root']==cell['root']
            and any(s.get('length') for s in w['path'].get('segments',[]))]
    effects=matched+length
    if not matched or query.get('effect',{}).get('source') not in [w['source'] for w in effects]:return None
    return {'decision':'source_authorized_manager_selects_list_subject',
            'source_certificate':{'subject_parameter':subject,'matched_cell':cell,
                'source_identity_condition':observed,'manager_permissions':managers,
                'effect_sources':[w['source'] for w in effects]},
            'not_safety_certificate':True,
            'scope':'only caller-equals-selected-member hypothesis; manager and effect checks remain'}



def source_projection_limit(peer,write,path,function,lookup):
    """Shared source-path qualification before static or M2 policy projection."""
    source=peer['path']
    if source['flow'] not in ('normal','returned') or source.get('issues') or source.get('evaluation_gaps'):
        return {'reason':'source_projection_dependency_unresolved',
                'origin_function':peer['function'],'origin_path_index':peer.get('path_index'),
                'source_flow':source['flow'],'source_issues':copy.deepcopy(source.get('issues',[])),
                'not_normal_or_safety_certificate':True}
    from .m04_policy_relations import record_credential_alternative
    from .m03_p_policy_context import peer_phase_conflict
    return (record_credential_alternative(peer,write,path,function,lookup)
            or peer_phase_conflict(peer,write,path))


def allowance_stage_alternative(query,state,shared):
    """Use existing full-amount holder-consent evidence for grant/use stages.
    Discharges only borrowed exclusive peer policies on the bound allowance.
    """
    from .m03_p_route import keys,fields
    from .m03_p_paths import lit
    if basis_kind(query) not in PROJECTED:return None
    tid=query['target'];fn=query['function'];pi=query.get('path_index')
    paths=state['paths'].get((tid,fn),[])
    if type(pi)is not int or not 0<=pi<len(paths):return None
    p=paths[pi]
    if p['issues'] or p.get('evaluation_gaps'):return None
    effect=query.get('effect',{});sel=effect.get('selector',{})
    if sel.get('kind')!='storage':return None
    for normal in shared.get(tid,{}).get('normal_transfers',[]):
        for c in normal.get('consent_sources',[]):
            allowance=c.get('allowance',{})
            if not allowance or not _same_family(sel,allowance):continue
            # The recognized consent model has already checked all writers,
            # bound holder/delegate/quantity and actual path authorization.
            setters=[s for s in c.get('holder_controlled_setters',[])
                     if s['function']==fn and s['source']==effect.get('source')]
            own=keys(sel) and keys(sel)[0]=={'kind':'actual_sender'}
            stage=None
            if setters and own:stage='holder_grants_own_allowance'
            consumption=c.get('consumption',{})
            if (normal['function']==fn and normal['path_index']==pi
                    and consumption.get('source')==effect.get('source')
                    and key(consumption.get('path'))==key(sel)):
                stage='authorized_delegate_consumes_allowance'
            if stage:
                return {'decision':'source_bound_allowance_stage_not_peer_exclusivity',
                    'source_certificate':{'stage':stage,'effect_source':effect.get('source'),
                        'selector':sel,'consent_source':copy.deepcopy(c),
                        'authorized_consumer':{'function':normal['function'],'path_index':normal['path_index'],
                                               'consent':copy.deepcopy(normal['consent']),'holder':copy.deepcopy(normal['holder'])}},
                    'not_safety_certificate':True,'scope':'this allowance effect only; independent bad-subject/key/credential queries remain'}
    return None
