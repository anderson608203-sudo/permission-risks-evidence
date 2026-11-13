"""One applicability gate for all AC consumers, followed by sourced new duties.
The gate can reject a wrong policy, not certify the whole operation as safe.
"""
import copy
from .core import digest
from .m03_p_paths import key,walk,op,lit
from .m03_p_route import selectors,keys,fields,value_type,effective_permission,relocate
from .m04_logic import Unsupported
SENDER={'kind':'actual_sender'}

def family(sel):return (sel.get('root'),tuple(fields(sel)),key(sel.get('instance')))
def role_evidence(lookup,program,principal):
    evidence=[]
    for fn,paths in program.items():
        for pi,p in enumerate(paths):
            if p['flow'] not in ('normal','returned'):continue
            try:permissions=effective_permission(p['guards'],lookup)
            except (Unsupported,ValueError):continue
            for permission in permissions:
                for a in walk(permission):
                    if a.get('kind')!='op' or a.get('op')!='==':continue
                    aa=a.get('args',[])
                    if len(aa)!=2:continue
                    for caller,subject in (aa,aa[::-1]):
                        if caller.get('kind')=='actual_sender' and subject.get('kind')=='storage' and family(subject)==family(principal):
                            evidence.append({'function':fn,'path_index':pi,'guard':permission,
                                'principal':subject,'kind':'positive_source_authority_in_effective_guard','role_use_only_not_execution_proof':True,'unrelated_path_limits':copy.deepcopy(p.get('issues',[]))+copy.deepcopy(p.get('evaluation_gaps',[]))})
    return evidence

def _origin(q):
    b=q.get('policy_basis',{})
    return b.get('basis') or b.get('relation') or b.get('kind')


def own_native_claim(path,lookup,effect):
    """Normal single-call payout consumes the caller's exact recorded quantity.
    Field ledgers retain their complete selector; another field is not a match.
    This certifies no reentrancy or all-history property.
    """
    from .m03_p_assets import polynomial,negative
    from .m05_state_relations import changes
    from .m20_ledger import account_record
    if path['issues'] or path.get('evaluation_gaps'):return None
    updates=changes(path,lookup)
    for payment in path.get('native_transfers',[]):
        if payment['recipient']!=SENDER:continue
        amount=polynomial(payment['amount'])
        if not amount:continue
        for d in updates:
            sel=d['write']['path']
            if not account_record(sel,lookup) or keys(sel)[0]!=SENDER or d['delta']!=negative(amount):continue
            if effect.get('source') not in (payment['source'],d['write']['source']):continue
            # All successful path outcomes must include success or revert.
            from .m03_p_paths import conditions_possible
            if conditions_possible(path['guards'],payment['success']):continue
            return {'kind':'caller_claims_exact_source_recorded_native_amount','holder':SENDER,
                'selector':sel,'debit_source':d['write']['source'],'payment':payment,
                'amount':amount,'scope':'same source path and complete holder/field binding; no all-history or reentrancy proof'}
    return None

def gate(q,state,shared,index):
    if q.get('rule') not in ('AC-01','AC-02','AC-03'):return q,None
    tid=q['target'];lookup=state['lookups'][tid];fn=q['function']
    program={f:ps for (t,f),ps in state['paths'].items() if t==tid}
    path=program.get(fn,[])
    pi=q.get('path_index')
    if not isinstance(pi,int) or pi>=len(path):return q,None
    path=path[pi];origin=_origin(q);required=q.get('required_policy_candidate',{})
    principal=[s for s in selectors(required) if value_type(s,lookup) in ('address','address payable')]
    # An address read with the same object key is not an ownership declaration.
    if origin in ('same_resource_owner_read_to_effect','owner_read_to_effect'):
        supported=[]
        for s in principal:supported.extend(role_evidence(lookup,program,s))
        if not supported:
            recipients=[e.get('recipient') for ps in program.values() for p in ps for e in p.get('sensitive_effects',[]) if e.get('recipient')]
            matches=[s for s in principal if any(family(t)==family(s) for r in recipients for t in selectors(r))]
            return q,{'decision':'unsupported_authorization_projection','not_safety_certificate':True,
                      'reason':'payout_recipient_is_not_authorizer' if matches else 'address_read_does_not_establish_resource_ownership',
                      'source_certificate':{'principal_reads':principal,'recipient_uses':matches},
                      'scope':'only this inferred principal-to-effect hypothesis; other risk queries remain'}
        q['policy_applicability']={'decision':'source_principal_role_observed','evidence':supported,'sat_does_not_prove_policy':True}
    # Heuristic peer guards do not override an explicit authorization on this
    # actual branch. Wrong-subject/key/order and direct mechanism obligations
    # are separate queries and are deliberately not discharged here.
    inferred=origin in ('same_resource_guarded_operation','source_checked_M2_relation','observed_guard','same_source_native_reserve_guard','credential_management_edges_to_same_family')
    if inferred and not path['issues'] and not path.get('evaluation_gaps'):
        try:
            local=effective_permission(path['guards'],lookup)
            same_family_conflict=any(family(a)==family(b) and key(a)!=key(b)
                for g in local for a in selectors(g) for b in principal)
            if local and not same_family_conflict:
                certificate={'local_permissions':local,'source_conditions':path['guards'],
                    'function':fn,'path_index':pi,'effect_source':q.get('effect',{}).get('source'),
                    'rejected_exclusive_peer_policy':required,'independent_mismatch_queries_remain':True}
                q['required_policy_candidate']=op('or',required,*local)
                return q,{'decision':'explicit_local_authorization_not_overridden_by_peer','source_certificate':certificate,
                    'scope':'only the inferred exclusivity of a peer/other branch; not a safety certificate'}
            claim=own_native_claim(path,lookup,q.get('effect',{}))
            if claim:
                return q,{'decision':'source_holder_native_claim_not_peer_administration','source_certificate':claim,
                    'scope':'this matched payout or consumed account field; other effects remain checked'}
        except (Unsupported,ValueError) as ex:
            q.setdefault('applicability_limits',[]).append(str(ex))
    # All older exclusion paths are routed through this same gate.
    from .m19_authorization_scope import alternative as use
    from .m18_policy_scope import alternative as precise
    from .m12_policy import alternative as transition
    from .m11_policy import applicability
    from .m09_shared_policy import alternative as normal
    from .m04_joint_controls import assess_policy
    normalized=q
    if origin=='v20_semantic_source_authority':
        normalized=copy.deepcopy(q);normalized['policy_basis']['basis']='source_checked_M2_relation'
    excluded=use(normalized,state,shared) or precise(normalized,state,shared) or transition(normalized,state,shared) or applicability(normalized,state,shared) or normal(normalized,shared) or assess_policy(normalized,state['_v20_old_context'])
    if excluded:return q,excluded
    if origin in ('same_resource_guarded_operation','source_checked_M2_relation','v20_semantic_source_authority'):
        from .m20_quorum import certificate
        cert=certificate(lookup,program,fn,pi,path,index)
        if cert:return q,{'decision':'source_verified_quorum_authorization','source_certificate':cert,
                         'scope':'this path and operation identity; no cryptographic or deployment proof'}
    # Combine source-qualified legal alternatives only for policies inferred from
    # peers, never erase an explicit operation-specific restriction by any guard.
    projected=origin in ('same_resource_guarded_operation','source_checked_M2_relation','v20_semantic_source_authority')
    if projected:
        effect=q.get('effect',{});source=effect.get('source')
        normals=[n for label in ('normal_transfers','normal_effects','object_delegation_use')
                 for n in shared.get(tid,{}).get(label,[]) if n.get('function')==fn
                 and n.get('path_index')==pi and source in n.get('effect_sources',[])]
        alternatives=[]
        for n in normals:
            predicate=n.get('consent') or n.get('use_predicate') or n.get('authorization')
            if predicate:alternatives.append(predicate)
        if alternatives:
            q['required_policy_candidate']=op('or',required,*alternatives)
            q['policy_applicability']={'decision':'union_of_source_qualified_legal_authorizations',
                'original':required,'alternatives':alternatives,'effect_source':source,'sat_does_not_prove_policy':True}
    return q,None

def authority_duties(context,state,index):
    from .m11_policy import make_query,once_latch
    rows=[];limits=[]
    for tid,lookup in state['lookups'].items():
        program={fn:ps for (t,fn),ps in state['paths'].items() if t==tid}
        authorities={}
        for fn,ps in program.items():
            for p in ps:
                try:perms=effective_permission(p['guards'],lookup)
                except (Unsupported,ValueError):continue
                for g in perms:
                    for s in selectors(g):
                        if value_type(s,lookup) in ('address','address payable'):
                            authorities[(family(s),len(keys(s)))]=s
        for r in index.by_target[tid]:
            e=r['effect'];s=e.get('selector')
            if not s or (family(s),len(keys(s))) not in authorities:continue
            # A guard fragment from an incomplete loop/path, or an unrelated
            # address comparison, does not establish a source authority.
            evidence=role_evidence(lookup,program,s)
            if not evidence:continue
            p=program[r['function']][r['path_index']]
            if p['issues'] or p.get('evaluation_gaps'):continue
            from .m22_local_state import fresh_array_element,fresh_counter_element,register
            allocation=fresh_array_element(lookup,p,e) or fresh_counter_element(lookup,program,p,e)
            if allocation:
                index.use(r,'proved_source_initialization',reason=register(state,allocation))
                continue
            try:
                perms=effective_permission(p['guards'],lookup)
                # Clear/uninitialized state is an explicit normal alternative.
                required=op('or',op('==',s,lit(0)),op('==',SENDER,s),*perms)
                latch=once_latch(p,program,lookup)
                if latch:
                    index.use(r,'one_way_initialization',reason='source latch, first caller intent not inferred')
                    continue
                q=make_query(context,tid,r['function'],r['path_index'],p,e['original_write'],required,
                    {'basis':'v22_source_object_authority_replacement' if keys(s) else 'v20_source_authority_replacement','authority_use_evidence':evidence,
                     'scope':'replacing an extant source authority requires existing authority or a source-qualified alternative'},'AC-02')
                q['effect_id']=r['id'];rows.append(q);index.use(r,'authority_replacement',q['id'])
            except (Unsupported,ValueError) as ex:limits.append({'phase':'v20_authority','target':tid,'function':r['function'],'reason':str(ex)})
    return rows,limits

def semantic_duties(context,relations,state,index):
    from .m16_source_bindings import resolve,resolve_condition
    from .m11_policy import make_query,once_latch
    from .m09_shared_policy import implies
    rows=[];usage=[];ops={o['id']:o for o in context['operations']};refs=context['references']
    containers=[(r,'nested') for r in relations['relations']]
    for h in relations.get('authorization_hypotheses',[]):
        # Standalone is a transport origin, not an inferred controlled_by edge.
        containers.append(({'id':'standalone_hyp_'+digest(h)[:20],
                            'authorization_hypotheses':[h],'related_op_refs':[]},'standalone'))
    for relation,location in containers:
        for h in relation.get('authorization_hypotheses',[]):
            record={'relation_id':relation['id'],'hypothesis_location':location,
                    'hypothesis':copy.deepcopy(h),'status':'not_supported','path_checks':[],'query_ids':[]}
            usage.append(record);o=ops[h['op_ref']];tid=o['target'];fn=o['function'];lookup=state['lookups'][tid]
            program={f:ps for (t,f),ps in state['paths'].items() if t==tid}
            effect_id=refs[h['effect_ref']]['ast_id']
            for r in index.by_operation[tid,fn]:
                e=r['effect']
                if e.get('source',{}).get('ast_id')!=effect_id or e['kind']!='state_write':continue
                p=program[fn][r['path_index']];item={'path_index':r['path_index']};record['path_checks'].append(item)
                if p['issues'] or p.get('evaluation_gaps'):
                    item['reason']='incomplete_effect_path';continue
                try:
                    actor=resolve(lookup.nodes[refs[h['actor_ref']]['ast_id']],lookup,fn,p)
                    resource=resolve(lookup.nodes[refs[h['resource_ref']]['ast_id']],lookup,fn,p,purpose='resource')
                    # A declaration may locate an indexed family, but cannot supply
                    # invented keys. Concrete key/field claims must match exactly.
                    if resource.get('kind')!='storage' or resource['root']!=e['selector']['root']:
                        item['reason']='resource_does_not_bind_effect';continue
                    if resource.get('segments') and key(resource)!=key(e['selector']):
                        item['reason']='resource_key_or_field_mismatch';continue
                    cited=[refs[x]['ast_id'] for x in h['source_refs']]
                    if effect_id not in cited:
                        item['reason']='effect_not_in_supporting_evidence';continue
                    conditions=[]
                    for ref in h['condition_refs']:
                        value=resolve_condition(lookup.nodes[refs[ref]['ast_id']],lookup,fn,p)
                        conditions.append(value)
                    if any(not implies(lookup,p,value) for value in conditions):
                        item['reason']='proposed_applicability_condition_not_established_on_this_path';continue
                    if h['kind']=='single_initialization':
                        latch=once_latch(p,program,lookup)
                        if latch:
                            item.update(status='source_verified_single_initialization',certificate=latch)
                            index.use(r,'semantic_initialization_scope',relation=relation['id'])
                        else:item['reason']='one_way_latch_not_proved'
                        continue
                    if h['kind']=='threshold_approval':
                        from .m20_quorum import certificate
                        cert=certificate(lookup,program,fn,r['path_index'],p,index)
                        if cert and (actor==SENDER or any(key(actor)==key(x) for conf in cert['confirmations'] for x in selectors(conf['approver_conditions']))):
                            item.update(status='source_verified_quorum',certificate=cert)
                            index.use(r,'semantic_quorum_scope',relation=relation['id'])
                        else:item['reason']='distinct_qualified_approvals_same_object_not_proved'
                        continue
                    if h['kind']=='holder_consent':
                        from .m03_p_assets import negative
                        from .m05_state_relations import changes
                        from .m05_asset_obligations import consent_model
                        updates=[d for d in changes(p,lookup) if key(d['write']['path'])==key(e['selector']) and d['delta']]
                        if len(updates)!=1 or not keys(e['selector']) or key(actor)!=key(keys(e['selector'])[0]):
                            item['reason']='holder_or_debit_not_bound';continue
                        # Only already financially qualified balances can create this AC duty.
                        assets=state.get('_v20_shared',{}).get(tid,{}).get('assets',[])
                        asset=next((a for a in assets if a['balance_root']==resource['root']),None)
                        if not asset:item['reason']='financial_holder_entitlement_not_established';continue
                        consent,proof=consent_model(p,actor,negative(updates[0]['delta']),lookup,program,resource['root'],asset.get('supply_root'))
                        required=op('or',consent,*effective_permission(p['guards'],lookup))
                        basis={'basis':'source_holder_entitlement_disposition','relation_id':relation['id'],'holder_consent':proof}
                        rule='AC-03'
                    else:
                        evidence=role_evidence(lookup,program,actor) if actor.get('kind')=='storage' else []
                        evidence=[x for x in evidence if any(a.get('referencedDeclaration')==actor['root'] or a.get('id')==actor['root']
                            for ast_id in cited for a in walk(lookup.nodes.get(ast_id,{})))]
                        if not evidence:item['reason']='no_cited_independent_source_authority_role';continue
                        peers={ops[x]['function'] for x in relation['related_op_refs'] if ops[x]['target']==tid}
                        connections=[]
                        for proof in evidence:
                            if proof['function'] not in peers:continue
                            pp=program[proof['function']][proof['path_index']]
                            for w in pp['writes']:
                                if family(w['path'])!=family(e['selector']):continue
                                try:
                                    mapped=relocate(proof['guard'],w['path'],e['selector'])
                                    if any(key(t)==key(actor) for t in selectors(mapped)):connections.append(proof)
                                except (Unsupported,ValueError):pass
                        if key(e['selector'])!=key(actor) and not connections:
                            item['reason']='authority_stage_and_effect_not_source_connected';continue
                        required=op('==',SENDER,actor)
                        if key(e['selector'])==key(actor):required=op('or',op('==',actor,lit(0)),required)
                        # Explicit local legal alternatives survive M2 additions.
                        required=op('or',required,*effective_permission(p['guards'],lookup))
                        basis={'basis':'v20_semantic_source_authority','relation_id':relation['id'],
                            'authority_evidence':evidence,'source_refs':h['source_refs'],
                            'origin_function':connections[0]['function'] if connections else evidence[0]['function'],
                            'scope':'source-supported local policy hypothesis; not proof of business intention'}
                        rule='AC-02' if key(e['selector'])==key(actor) else 'AC-01'
                    q=make_query(context,tid,fn,r['path_index'],p,e['original_write'],required,basis,rule)
                    rows.append(q);item.update(status='compiled_source_policy',query_id=q['id'])
                    record.setdefault('query_ids',[]).append(q['id'])
                    index.use(r,'semantic_authorization_hypothesis',q['id'],relation['id'])
                except (Unsupported,ValueError,KeyError) as ex:item['reason']=str(ex)
            statuses=[x.get('status') for x in record['path_checks']]
            if 'compiled_source_policy' in statuses:record['status']='compiled_source_policy'
            elif any(statuses):record['status']='source_verified_local_scope'
            elif not record['path_checks']:record['reason']='effect_not_on_analyzed_operation_path'
    return rows,usage
