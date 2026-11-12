# 源码文本 · 13

## source/src/pr_next_joint/investigation/local_properties.py

原文件 SHA-256 `3872bd9b8dc58de4ba4145ea8003ea1e68faf165f2a03e646a8a5df4a5c88bde`

````python
"""Typed, source-effect queries for a compiled property."""
import copy
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, selector_relation
from pr_next_joint.verification.sequence import qualify, read
from pr_next_joint.verification.source_worlds import frame, encode_frame
from pr_next_joint.verification.program_encoding import MechanismEncoder
from pr_next_joint.verification.expressions import Unsupported
from .ledger import movements, unit_origin, flow, grant_for
from .roles import path_qualification, fixed_role_terms
from .relations import beneficiary_condition


def safe_path(b, oid, pid, path):
    deps = b.condition_dependencies(oid, pid, path)
    if not path.get('source_call_subcases') and any(r['operation'] == oid and r['path'] == pid for r in b.f.call_summaries.rows.values()):
        roots = getattr(b,'active_property_roots',None) or {s['root'] for s in selectors([path['guards'],path['writes']])}
        # Demand-driven may analysis is shared between properties by its full
        # source/callpoint/root identity. It never turns an opaque return into
        # a successful call or a source-policy certificate.
        refinement = b.f.call_summaries.refine(b, oid, pid, roots)
        b.call_refinements = getattr(b,'call_refinements',{})
        b.call_refinements[refinement['id']] = refinement
        if any(c.get('same_storage_unresolved') or c.get('callback_projection') in
               ('may_influence','source_callpoint_not_precisely_lowered') for c in refinement['calls']):
            return False
    # Credential formulas are admitted to the backend, which checks exact
    # invalid-return domains and concretely verifies a candidate signature.
    # A symbolic recovered address alone never qualifies as a witness.
    return not deps['unknown_dependencies']


def _effect(e, fr, lookup):
    """Committed net effects, not merely returning from the entry."""
    z = e.z
    cells = {key(w['path']): w['path'] for w in fr['writes']}
    deltas = [e.expr(read(c, fr['before'] + fr['writes'], lookup)) !=
              e.expr(read(c, fr['before'], lookup)) for c in cells.values()]
    deltas += [e.expr(v['amount']) > 0 for v in fr['effects'] if v.get('amount') is not None]
    return z.Or(*deltas)


def necessary_effect_exclusion(b,oid,pid,context):
    """A pure necessary condition can refute a route with an unknown read.

    Unknown STATICCALL results are omitted, never assumed successful/false.
    An unresolved state-changing call cannot use this projection.
    """
    f=b.f;p=f.paths[pid]['raw'];req=context['observable']
    if req.get('measure')!='direct_effect' or p['flow'] not in ('normal','returned'):return None
    calls=[c for c in f.call_summaries.rows.values()if c['operation']==oid and c['path']==pid]
    if not calls or any(c['mode']!='STATICCALL' and c['unresolved_implementation']for c in calls):return None
    role=path_qualification(f,oid,p)
    if not role:return None
    try:
        e=MechanismEncoder(f.lookup(oid));z=e.z
        opaque={'unknown','external_return','read_call','call_unresolved','credential_recovery'}
        projection=dict(p,issues=[],evaluation_gaps=[],evaluated_terms=[],
            guards=[g for g in p['guards']if not any(n.get('kind')in opaque for n in walk(g))])
        fr=frame(f,oid,pid,0,path_override=projection)
        fr['evidence_world']='necessary_condition_projection_not_execution'
        guards=fr['guards']
        terms=[]
        for g in guards:
            mc,md=len(e.constraints),len(e.domain_constraints)
            try:terms.append(e.expr(g))
            except Unsupported:del e.constraints[mc:];del e.domain_constraints[md:]
        effects=[]
        for cell in (context.get('compiled_property')or{}).get('objects',[]):
            holder,start,end,_,_=flow(e,f.lookup(oid),fr,cell)
            effects.append(end>start if req['category']=='FCR-MINT' else end<start)
        if not effects:return None
        roles,origins=fixed_role_terms(e,role,0)
        detail={'operation':oid,'target':f.operations[oid]['target'],'use_path':pid,
            'property_identity':context.get('property_identity'),'semantic_version':context.get('semantic_version'),
            'category':req['category'],'property_validated':True,'necessary_condition_only':True,
            'omitted_read_results_are_unconstrained_not_assumed':True,'retained_guards':guards,
            'role_origins':origins,'unknown_read_cannot_modify_local_storage':True}
        q=b._query(e,z.And(*terms,*roles,e.expr(fr['caller'])!=0,z.Or(*effects)),
                   'source_necessary_condition',detail)
        if q['answer']=='unsat' and (q.get('exclusion_certificate',{}).get('excludes_only_this_formula') or
                q.get('details',{}).get('prestate',{}).get('global_reachability_exhausted')):
            return q
    except Unsupported:pass
    return None


def check_local(b, oid, primary_use, context):
    f = b.f
    lookup = f.lookup(oid)
    req = context['observable']
    kind = req['measure']
    queries, rows, gaps = [], [], []
    prop = context.get('compiled_property') or {}
    b.active_property_roots = {s['root'] for s in selectors([
        prop.get('objects',[]), (req.get('authorization') or {}).get('predicate',{})])}
    if kind in ('authorization_violation','denied_qualified'):
        # AC's effect predicate observes committed writes, including grant and
        # stage cells that are not financial asset objects. Their callbacks
        # must not be declared disjoint merely because objects is empty.
        uses=(req.get('authorization') or {}).get('acquisition_uses',[])
        related=[p for _,p in f.operation_paths(oid)]+[f.paths[u['path']]['raw'] for u in uses]
        b.active_property_roots.update(s['root'] for p in related for s in selectors([p['guards'],p['writes']]))
    b.active_property_objects = {s['root'] for s in selectors(prop.get('objects',[]))}
    necessary_closed={}
    for source_pid,source_path in f.operation_paths(oid):
        if not source_path.get('issues') and not source_path.get('evaluation_gaps'):continue
        exclusion=necessary_effect_exclusion(b,oid,source_pid,context)
        if exclusion:
            necessary_closed[source_pid]=exclusion['id'];queries.append(exclusion)
            rows.append({'state':'necessary_condition_unsat','scope':exclusion['details'],'result_probe':exclusion['id']})
    if any(e['operation']==oid and e['raw'].get('kind') in ('native_transfer','native_selfdestruct')
           for e in f.effects.values()):
        b.active_property_roots.add(-1)
    for source_pid, source_path in f.operation_paths(oid):
        if source_pid in necessary_closed:continue
        if any(c['operation']==oid and c['path']==source_pid for c in f.call_summaries.rows.values()):
            # Unresolved call paths cannot be upgraded to witness paths, but
            # their actual callpoint/guard projections still enter the shared
            # obligation and feedback records rather than vanishing at paths().
            f.call_summaries.refine(b,oid,source_pid,b.active_property_roots)

    def pair(e, base, extra, details, values):
        details = dict(details, property_identity=context.get('property_identity'),
                       semantic_version=context.get('semantic_version'),
                       prefix_state_handoff=reached, prefix=reached.get('prefix',[]),
                       **({'initial_prefix_policy':'constructor_only_for_explicit_prefix'} if reached else {}),
                       property_validated=True, validation='typed source entities and actual committed effect')
        feasible = b._query(e, base, 'local_premises_feasible', details)
        queries.append(feasible)
        if not feasible['validated_bounded_witness']:
            rows.append({'feasible_probe': feasible['id'], 'state': 'premise_' + feasible['answer'], 'scope': details})
            return
        tested = b._query(e, e.z.And(base, extra), kind, details, values)
        queries.append(tested)
        rows.append({'feasible_probe': feasible['id'], 'result_probe': tested['id'],
                     'state': tested['answer'], 'scope': details, 'values': tested.get('observed_values', {})})

    reached=context.get('reached_state') or {}
    prefix_frames=reached.get('frames',[])
    prefix_writes=reached.get('writes',[])
    slot=len(prefix_frames)
    def current_frame(pid):
        return b.source_frame(oid,pid,slot,prefix_writes)
    def prefix_conditions(e):
        from .behavior import ordered_clocks
        return [encode_frame(e,pf) for pf in prefix_frames]+[e.expr(pf['caller'])!=0 for pf in prefix_frames]+ordered_clocks(e,slot)

    if kind == 'authorization_violation':
        policy = req.get('authorization')
        if not policy:
            gaps.append({'reason': 'authorization_relationship_not_bound'})
        else:
            for pid, p in b.paths(oid):
                b.check()
                if not safe_path(b, oid, pid, p):
                    gaps.append({'path': pid, 'reason': 'authorization_path_dependency_unresolved'})
                    continue
                try:
                    e = MechanismEncoder(lookup)
                    z = e.z
                    fr = current_frame(pid)
                    actor = e.expr(fr['caller'])
                    expected = e.expr(read(qualify(policy['predicate'], slot),prefix_writes,lookup))
                    effect = _effect(e, fr, lookup)
                    uses = []
                    if policy.get('property_family') == 'acquire':
                        for row in policy['acquisition_uses']:
                            b.check()
                            if not safe_path(b, row['operation'], row['path'], f.paths[row['path']]['raw']):
                                gaps.append({'path': row['path'], 'reason': 'acquired_authority_use_unresolved'})
                                continue
                            after = b.source_frame(row['operation'], row['path'], slot+1, prefix_writes+fr['writes'])
                            uses.append(z.And(encode_frame(e, after), _effect(e, after, lookup),
                                              e.expr(after['caller']) == actor))
                        effect = z.And(effect, z.Or(*uses))
                    detail = {'operation': oid, 'target': f.operations[oid]['target'], 'use_path': pid,
                              'expected_authorization': policy, 'actual_guards': fr['guards'],
                              'argument_domain': 'all_source_inputs_on_this_committing_path',
                              'effect_required': True, 'acquisition_use_required': bool(policy.get('acquisition_uses'))}
                    pair(e, z.And(encode_frame(e, fr), actor != 0, *prefix_conditions(e)), z.And(effect, z.Not(expected)), detail,
                         {'caller': actor, 'authorization_holds': expected, 'sensitive_effect': effect})
                except Unsupported as error:
                    gaps.append({'path': pid, 'reason': str(error)})
    elif kind == 'denied_qualified':
        policy = req.get('authorization')
        if not policy:
            gaps.append({'reason': 'qualified_denial_policy_not_bound'})
        else:
            subject = policy['subject']
            rejecting = [(pid, p) for pid, p in f.operation_paths(oid) if p['flow'] == 'reverted']
            for pid, p in rejecting:
                b.check()
                if not p['guards'] or not safe_path(b, oid, pid, p):
                    continue
                try:
                    e = MechanismEncoder(lookup)
                    z = e.z
                    actor = e.expr(qualify({'kind': 'actual_sender'}, 0))
                    allowed = e.expr(read(qualify(policy['predicate'], slot),prefix_writes,lookup))
                    controls = {s['root'] for s in selectors(p['guards'][-1])}
                    if subject.get('root') not in controls:
                        continue
                    productive_if_authorized = []
                    for spid, sp in b.paths(oid):
                        sf = frame(f, oid, spid, 0)
                        kept = [g for g in sf['guards'] if not (
                            any(s['root'] == subject.get('root') for s in selectors(g)) and
                            any(v.get('sequence_role') == 'caller' for v in walk(g)))]
                        conditioned = dict(sf, guards=kept)
                        productive_if_authorized.append(z.And(encode_frame(e, conditioned), _effect(e, sf, lookup)))
                    original_denial = z.And(*[e.expr(qualify(g, 0)) for g in p['guards']])
                    detail = {'operation': oid, 'target': f.operations[oid]['target'], 'use_path': pid,
                              'expected_authorization': policy, 'actual_denial': p['guards'],
                              'counterfactual_change': 'only the matched authorization guard is corrected',
                              'other_request_preconditions_retained': True, 'effect_required': True,
                              'argument_domain': 'all_source_inputs_on_this_rejecting_path'}
                    pair(e, z.And(actor != 0, allowed, z.Or(*productive_if_authorized)),
                         original_denial, detail, {'caller': actor, 'authorization_holds': allowed})
                except Unsupported as error:
                    gaps.append({'path': pid, 'reason': str(error)})
    elif kind == 'direct_effect':
        cat = req['category']
        for pid, p in b.paths(oid):
            b.check()
            if not safe_path(b, oid, pid, p):
                gaps.append({'path': pid, 'reason': 'effect_path_dependency_unresolved'})
                continue
            qualification = path_qualification(f, oid, p)
            if not qualification:
                # Absence of a privileged path is a scoped exclusion when the
                # source is complete, not a new full-business detector.
                rows.append({'state': 'not_privileged', 'path': pid})
                continue
            try:
                e = MechanismEncoder(lookup)
                z = e.z
                fr = current_frame(pid)
                actor = e.expr(fr['caller'])
                roles, origins = fixed_role_terms(e, qualification, slot)
                moves = movements(b, oid, p)
                for cell in moves['+' if cat == 'FCR-MINT' else '-']:
                    b.check()
                    unit = unit_origin(b, oid, cell)
                    if not unit:
                        gaps.append({'path': pid, 'position': cell, 'reason': 'financial_unit_not_bound'})
                        continue
                    holder, start, end, debit, credit = flow(e, lookup, fr, cell)
                    conditions = [end > start] if cat == 'FCR-MINT' else [end < start, holder != actor, holder != 0]
                    details = {'operation': oid, 'target': f.operations[oid]['target'], 'use_path': pid,
                               'role_provenance': qualification, 'encoded_role_origins': origins,
                               'ledger': cell, 'unit': unit, 'category_hypothesis': cat,
                               'argument_domain': 'all_source_inputs_on_this_committing_path',
                               'conditional_call_summary':fr.get('source_call_subcases',[]),
                               'predicate': 'source_bound_financial_effect'}
                    opposite = [c for c in moves['-' if cat == 'FCR-MINT' else '+']
                                if selector_relation(c, cell) == 'same_shape' and key(c) != key(cell)]
                    if cat == 'FCR-MINT':
                        controlled, basis = beneficiary_condition(e, fr, cell, holder)
                        conditions.append(controlled)
                        details['beneficiary'] = basis
                        # A transfer of an existing balance is not issuance.
                        conditions.extend(flow(e, lookup, fr, c)[1] <= flow(e, lookup, fr, c)[2] for c in opposite)
                    elif cat == 'FCR-TRANSFER':
                        destinations = []
                        for c in opposite:
                            from .summary import local_delta
                            debit_amounts = [local_delta(w)[1]
                                             for w in p['writes'] if selector_relation(w['path'],cell)=='same_shape' and
                                             local_delta(w)[0]=='-']
                            credit_amounts = [local_delta(w)[1]
                                              for w in p['writes'] if key(w['path'])==key(c) and
                                              local_delta(w)[0]=='+']
                            if not any(key(d)==key(part) for d in debit_amounts for a in credit_amounts for part in walk(a)):
                                gaps.append({'path':pid,'debit':cell,'credit':c,
                                             'reason':'same_ledger_credit_not_causally_bound_to_debit_quantity'})
                                continue
                            recipient, before, after, _, _ = flow(e, lookup, fr, c)
                            destinations.append(z.And(after > before, recipient != holder, recipient != 0))
                        conditions.append(z.Or(*destinations))
                        details['corresponding_same_ledger_credit'] = opposite
                    elif cat == 'FCR-DESTROY':
                        # Corresponding full token transfers preserve the right.
                        if opposite:
                            total_credit = z.Sum(*[flow(e, lookup, fr, c)[2] - flow(e, lookup, fr, c)[1] for c in opposite])
                            conditions.append(start - end > total_credit)
                    consent = grant_for(b, oid, p, cell) if cat != 'FCR-MINT' else None
                    if consent:
                        # Checked holder-issued allowance remains meaningful.
                        details['holder_grant'] = consent
                        conditions.append(e.expr(read(qualify(consent, slot),prefix_writes,lookup)) < debit)
                    bound = [e.expr(qualify(x['parameter'], slot)) == e.expr(x['value']) for x in context.get('bindings', [])]
                    pair(e, z.And(encode_frame(e, fr), actor != 0, *prefix_conditions(e), *roles, *bound), z.And(*conditions), details,
                         {'actor': actor, 'affected_account': holder, 'before': start, 'after': end, 'gross_debit': debit})
            except Unsupported as error:
                gaps.append({'path': pid, 'reason': str(error)})
    else:
        # Preserve existing finite missing-control and qualified-denial probes.
        # Their output is evidence; the shared property consumer checks its
        # applicability before it can change a finding.
        return auxiliary_property(b, oid, primary_use, context)
    source_rows=list(f.operation_paths(oid))
    covered_with_necessary=bool(necessary_closed) and all(p['flow']=='reverted' or pid in necessary_closed or
        p['flow']in('normal','returned') and not p.get('issues') and not p.get('evaluation_gaps')
        for pid,p in source_rows) and not any(g['kind']=='path_extraction'for g in f.operations[oid]['gaps'])
    exclusion = not reached and bool(rows) and not gaps and (b.complete(oid) or covered_with_necessary) and all(
        r.get('state') in ('unsat', 'not_privileged','necessary_condition_unsat','premise_unsat') for r in rows)
    tested = [x for x in queries if x.get('label') in (kind,'source_necessary_condition') or x.get('label')=='local_premises_feasible' and x.get('answer')=='unsat']
    # Bounded UNSAT closes only its recorded domain unless the source
    # invariant certificate excludes every remaining initial stage.
    exclusion = exclusion and all(x.get('exclusion_certificate', {}).get('excludes_only_this_formula') or
                                  x.get('details', {}).get('prestate', {}).get('global_reachability_exhausted') for x in tested)
    return {'kind': 'causal_compare', 'observed_measure': kind, 'property_identity': context.get('property_identity'),
            'change': oid, 'observe': primary_use, 'queries': queries, 'property_measurements': rows,
            'property_excluded': exclusion, 'local_errors': gaps or ([] if rows else [{'reason': 'no_applicable_property_path'}]),
            'necessary_condition_route_coverage':{'source_identity':f.identity,'operation':oid,
                'excluded_paths':necessary_closed,'all_source_routes_accounted':covered_with_necessary} if necessary_closed else None,
            'worlds': [], 'comparisons': [], 'evidence_scope': {'target': f.operations[oid]['target'], 'request_context': context},
            'alternative_uses': [], 'holder_consent_counterexamples': [], 'net_measurements': []}

import re
from .request_scope import positive_caller_gate


def auxiliary_property(b,oid,primary_use,context):
    req=context['observable'];kind=req['measure']; f=b.f; lookup=f.lookup(oid)
    queries=[];rows=[];gaps=[]
    def pair(e,base,extra,details,values=None):
        feasible=b._query(e,base,'local_premises_feasible',details); queries.append(feasible)
        if not feasible['validated_bounded_witness']:
            rows.append({'feasible_probe':feasible['id'],'state':'premise_'+feasible['answer'],'scope':details});return
        tested=b._query(e,e.z.And(base,extra),kind,details,values);queries.append(tested)
        rows.append({'feasible_probe':feasible['id'],'result_probe':tested['id'],'state':tested['answer'],'scope':details,'values':tested.get('observed_values',{})})
    if kind=='authorization_violation':
        policy=req['authorization']
        for pid,p in b.paths(oid):
            b.check()
            if len(rows)>=f.options.max_prefixes:break
            if not safe_path(b,oid,pid,p):gaps.append({'path':pid,'reason':'authorization_path_dependency_unresolved'});continue
            try:
                e=MechanismEncoder(lookup);z=e.z;fr=frame(f,oid,pid,0)
                actor=e.expr(fr['caller']);expected=e.expr(qualify(policy['predicate'],0))
                detail={'operation':oid,'target':f.operations[oid]['target'],'use_path':pid,
                    'expected_authorization':policy,'actual_guards':fr['guards'],
                    'property_identity':context.get('property_identity'),'semantic_version':context.get('semantic_version',0),
                    'argument_domain':'all_source_inputs_on_this_committing_path'}
                pair(e,z.And(encode_frame(e,fr),actor!=0),z.Not(expected),detail,{'caller':actor,'authorization_holds':expected})
            except Unsupported as err:gaps.append({'path':pid,'reason':str(err)})
    elif kind=='missing_control':
        # Bind a flag to the very holder being debited on a real successful alternative,
        # after a committing writer. Unknowns on that alternative cannot establish a bypass.
        for alt in req['alternatives']:
            use=alt['use'];lookup=f.lookup(use)
            if not b.complete(use):gaps.append({'use':use,'reason':'incomplete_alternative_paths'})
            for cid,cp in b.paths(oid):
                for pid,p in b.paths(use):
                    b.check()
                    if len(rows)>=f.options.max_prefixes:break
                    if not safe_path(b,oid,cid,cp) or not safe_path(b,use,pid,p):
                        gaps.append({'path':pid,'reason':'unknown_on_selected_trace'});continue
                    try:
                        e=MechanismEncoder(lookup);z=e.z;cf=frame(f,oid,cid,0);uf=frame(f,use,pid,1,cf['writes'])
                        for cell in movements(b,use,p)['-']:
                            holder=keys(cell)[0]
                            controls=[w for w in cf['writes'] if len(keys(w['path']))==1 and value_type(w['path'],lookup)=='bool'
                                      and any(x['root']==w['path']['root'] for x in alt['control_writers'])]
                            if len(controls)!=1:continue
                            ctrl=controls[0]; h,_,_,debit,_=flow(e,lookup,uf,cell)
                            zc=e.expr(ctrl['value']);actor=e.expr(cf['caller']);requester=e.expr(uf['caller'])
                            from .behavior import ordered_clocks
                            base=z.And(encode_frame(e,cf),encode_frame(e,uf),*ordered_clocks(e,1),actor!=0,requester!=0,
                                       e.expr(keys(ctrl['path'])[0])==h,h!=0,zc)
                            detail={'change':oid,'observe':use,'change_path':cid,'use_path':pid,'object':cell,'active_holder_control':ctrl['path'],
                                    'control_value':True,'actual_guard_reads':alt['control_reads'],'peer_controlled_uses':alt['peer_controlled_uses'],
                                    'policy_requires_blocking_this_entry':'semantic_hypothesis_only'}
                            pair(e,base,debit>0,detail,{'holder':h,'caller':requester,'gross_debit':debit})
                    except Unsupported as err:gaps.append({'path':pid,'reason':str(err)})
    elif kind=='direct_effect':
        for pid,p in b.paths(oid):
            b.check()
            if len(rows)>=f.options.max_prefixes:break
            if not safe_path(b,oid,pid,p):gaps.append({'path':pid,'reason':'unresolved_dependency'});continue
            qualification=path_qualification(f,oid,p)
            if not qualification:gaps.append({'path':pid,'reason':'no_direct_positive_runtime_role_gate'});continue
            try:
                e=MechanismEncoder(lookup);z=e.z;fr=frame(f,oid,pid,0);actor=e.expr(fr['caller'])
                role_terms, fixed_origins=fixed_role_terms(e,qualification,0)
                moves=movements(b,oid,p); cat=req.get('category')
                for cell in moves['+' if cat=='FCR-MINT' else '-']:
                    origin=unit_origin(b,oid,cell)
                    if not origin:gaps.append({'path':pid,'reason':'unresolved_financial_unit'});continue
                    holder,start,end,dr,cr=flow(e,lookup,fr,cell)
                    detail={'operation':oid,'target':f.operations[oid]['target'],'use_path':pid,'role_guards':[x['guard'] for x in qualification],
                            'role_provenance':qualification,'encoded_role_origins':fixed_origins,'ledger':cell,'unit':origin,
                            'category_hypothesis':cat,'extent':'direct role-gated change of one ledger position; no global supply/consent or compensation judgment'}
                    detail.update(property_identity=context.get('property_identity'),semantic_version=context.get('semantic_version',0))
                    values={'actor':actor,'affected_account':holder,'before':start,'after':end,'gross_debit':dr,'gross_credit':cr}
                    if cat=='FCR-MINT':
                        # This specific probe tests the controller as actual beneficiary.
                        values['self_beneficiary']=holder==actor
                        condition=z.And(end>start,holder==actor)
                    else:condition=z.And(end<start,holder!=actor,holder!=0)
                    if cat=='FCR-TRANSFER':
                        destinations=[]
                        for c in moves['+']:
                            if selector_relation(c,cell)!='same_shape' or key(c)==key(cell):continue
                            recipient,pre,post,_,_=flow(e,lookup,fr,c)
                            destinations.append(z.And(post>pre,recipient!=holder,recipient!=0))
                        condition=z.And(condition,z.Or(*destinations))
                        detail['destination_credit_required']=True
                    bound=[]
                    for binding in context.get('bindings',[]):
                        bound.append(e.expr(qualify(binding['parameter'],0))==e.expr(binding['value']))
                    for a,c,relation in context.get('request_aliases',[]):
                        aa=e.expr(qualify(a,0));cc=e.expr(qualify(c,0));bound.append(aa==cc if relation=='==' else aa!=cc)
                    detail['predicate']='positive_credit_to_caller' if cat=='FCR-MINT' else 'negative_delta_of_other_nonzero_holder'
                    detail['argument_domain']='all_source_inputs_on_this_committing_path'
                    if context.get('request_aliases'):
                        detail.update(argument_domain='recorded_claim_aliases',claim_aliases=context['request_aliases'])
                    pair(e,z.And(encode_frame(e,fr),actor!=0,*role_terms,*bound),condition,detail,values)
            except Unsupported as err:gaps.append({'path':pid,'reason':str(err)})
    elif kind=='denied_qualified':
        # Eligibility is a named source role backed by a positive use on another
        # applied entry. Its applicability to this use remains an explicit hypothesis.
        for pid,p in f.operation_paths(oid):
            if p['flow']!='reverted' or not p['guards'] or len(rows)>=f.options.max_prefixes:continue
            b.check()
            if not safe_path(b,oid,pid,p):gaps.append({'path':pid,'reason':'unknown_rejection_dependency'});continue
            cause=p['guards'][-1]
            leaf=cause
            while leaf.get('op')=='!' and len(leaf['args'])==1:leaf=leaf['args'][0]
            if leaf.get('op') not in ('==','!=') or not any(x.get('kind')=='actual_sender' for x in leaf['args']):continue
            roles=[c for c in selectors(leaf) if not keys(c) and value_type(c,lookup) in ('address','address payable')]
            if len(roles)!=1:continue
            role=roles[0]; name=b._storage_name(oid,role)
            if not re.search(r'(?<![\w$])'+re.escape(name)+r'(?![\w$])',req['claim'],re.I):continue
            peers=[j for j,o in f.operations.items() if j!=oid and o['target']==f.operations[oid]['target'] and any(
                positive_caller_gate(g,lookup) and any(key(c)==key(role) for c in selectors(g)) for _,v in b.paths(j) for g in v['guards'])]
            if not peers:continue
            if p.get('writes') or p.get('sensitive_effects'):gaps.append({'path':pid,'reason':'complex_pre_rejection_effects'});continue
            try:
                e=MechanismEncoder(lookup);z=e.z;actor=e.expr(qualify({'kind':'actual_sender'},0))
                for term in p.get('evaluated_terms',[]):e.expr(qualify(term,0))
                earlier=[e.expr(qualify(g,0)) for g in p['guards'][:-1]]
                policy=actor==e.expr(qualify(role,0))
                base=z.And(actor!=0,policy,*earlier)
                detail={'operation':oid,'revert_path':pid,'role':role,'positive_role_use_sources':peers,'non_authorization_prefix':p['guards'][:-1],
                        'denial_condition':cause,'role_eligibility_at_use':'source-backed semantic hypothesis','failed_request_commits_writes':False}
                pair(e,base,e.expr(qualify(cause,0)),detail,{'caller':actor,'role':e.expr(qualify(role,0))})
            except Unsupported as err:gaps.append({'path':pid,'reason':str(err)})
    return {'kind':'causal_compare','observed_measure':kind,'change':oid,'observe':primary_use,'queries':queries,'property_measurements':rows,
            'local_errors':gaps or ([] if rows else [{'reason':'no_source_supported_path_for_property'}]),'worlds':[],'comparisons':[],
            'evidence_scope':{'target':f.operations[oid]['target'],'request_context':context,'controls':[]},
            'alternative_uses':[],'holder_consent_counterexamples':[],'net_measurements':[],'business_policy_proved':False}

````

## source/src/pr_next_joint/investigation/prestate.py

原文件 SHA-256 `d985f5498edb16ca90e48d4f06b90eb5e07538b8d91f971666a437c01d832239`

````python
"""Narrow initial-state invariants. Never equate a deployment choice with a current value."""
from functools import lru_cache
from pr_next_joint.frontend.path_ir import walk,key
from pr_next_joint.frontend.storage import selectors


def literal(node):
    if not isinstance(node,dict):return None
    if node.get('nodeType')=='FunctionCall' and node.get('kind')=='typeConversion' and len(node.get('arguments',[]))==1:
        type_name=node.get('expression',{}).get('typeName',{})
        target=type_name.get('name') if isinstance(type_name,dict) else type_name if isinstance(type_name,str) else None
        value=literal(node['arguments'][0])
        if type(value)is not int:return None
        import re
        numeric=re.fullmatch(r'uint(\d*)',target or '')
        width=160 if target in ('address','address payable') else int(numeric[1] or 256) if numeric else None
        return value if width and 0<=value<2**width else None
    if node.get('nodeType')!='Literal':return None
    typ=node.get('kind'); v=str(node.get('value',''))
    if typ in ('bool','boolean') and v in ('true','false'):return v=='true'
    if typ in ('number','hexNumber') and not node.get('subdenomination'):
        try:return int(v.replace('_',''),0)
        except ValueError:return None
    return None


def _legacy_state_facts(lookup):
    if hasattr(lookup,'_relational_initial'):return lookup._relational_initial
    bases=lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
    declarations=[n for b in bases for n in lookup.nodes[b].get('nodes',[])]
    # Assembly, delegate execution or a storage-reference alias can defeat AST write exclusion.
    functions=[n for n in declarations if n.get('nodeType') in ('FunctionDefinition','ModifierDefinition')]
    opaque=any(n.get('nodeType') in ('InlineAssembly','YulBlock') or n.get('memberName') in ('delegatecall','callcode')
         or n.get('nodeType')=='VariableDeclaration' and n.get('storageLocation')=='storage' for fn in functions for n in walk(fn))
    table={}
    for var in declarations:
        typ=var.get('typeDescriptions',{}).get('typeString','')
        if not var.get('stateVariable') or not (typ=='bool' or typ.startswith('uint') or typ in ('address','address payable')):continue
        vid=var['id']; row={'declaration':vid,'name':var['name'],'type':typ,'declaration_source':lookup.anchor(var),
            'origin':'conditional_symbolic','encoded':False}
        table[vid]=row; assigns=[]; runtime=False
        for fn in functions:
            is_ctor=fn.get('kind')=='constructor' or fn.get('isConstructor')
            body=fn.get('body') or {}
            for n in walk(body):
                if n.get('nodeType') not in ('Assignment','UnaryOperation'):continue
                lhs=n.get('leftHandSide') or n.get('subExpression') or {}
                if n.get('nodeType')=='UnaryOperation' and n.get('operator') not in ('++','--','delete'):continue
                if not any(x.get('referencedDeclaration')==vid for x in walk(lhs)):continue
                if is_ctor:assigns.append((fn,n))
                else:runtime=True
        if opaque and not var.get('constant'):row['limit']='indirect storage writes not excluded';continue
        if runtime:
            row['origin']='constructor_choice_with_possible_later_write' if assigns else 'conditional_state_with_source_writer'
            row['constructor_sources']=[lookup.anchor(n) for _,n in assigns]
            continue
        v=literal(var.get('value'))
        if var.get('value') is None:v=False if typ=='bool' else 0
        if not assigns:
            if v is not None:row.update(origin='fixed_declared_initializer' if var.get('value') is not None else 'fixed_type_default',value=v,encoded=True)
            continue
        row['origin']='constructor_configuration';row['writes']=[lookup.anchor(n) for _,n in assigns]
        if len(assigns)!=1:continue
        ctor,assignment=assigns[0]
        direct={st.get('expression',{}).get('id') for st in (ctor.get('body') or {}).get('statements',[]) if st.get('nodeType')=='ExpressionStatement'}
        if assignment['id'] not in direct or assignment.get('operator')!='=' or ctor.get('modifiers'):continue
        rhs=assignment.get('rightHandSide') or {}; v=literal(rhs)
        if v is not None:row.update(origin='fixed_constructor_literal',value=v,encoded=True)
        elif rhs.get('memberName')=='sender' and rhs.get('expression',{}).get('name')=='msg':
            row.update(origin='fixed_deployer_address',nonzero=True,encoded=True)
    lookup._relational_initial=table
    return table


def state_facts(lookup, selected_domain=None):
    from .initial_state import domain,initial_for_lookup,CAPABILITY,DEPLOYMENT
    from .state_encoding import _initial_term
    from pr_next_joint.verification.sequence import read
    selected_domain=selected_domain or domain(lookup)
    if selected_domain not in (CAPABILITY,DEPLOYMENT):return _legacy_state_facts(lookup)
    model=initial_for_lookup(lookup)
    if model is None:return {}
    cache=lookup.__dict__.setdefault('_domain_state_facts',{})
    token=(selected_domain,model['identity'])
    if token in cache:return cache[token]
    from .initial_state import family
    context={**model,'_lookup':lookup,'_amount_families':{family(r['cell']) for r in model['candidate_amount_leaves']}}
    table={}
    clean=[p for p in model['constructor_paths'] if p['flow'] in ('normal','returned') and not p.get('issues') and not p.get('evaluation_gaps')]
    for rid,row in model['declarations'].items():
        typ=row['type'];value={'declaration':rid,'name':row['name'],'type':typ,'declaration_source':row['source'],
            'origin':'constructor_configuration' if row['constructor_writes'] or row['explicit_initializer'] else
                     'abstract_initial_scalar' if selected_domain==CAPABILITY and (typ.startswith(('uint','int')) or typ in ('address','address payable')) else 'fixed_type_default',
            'encoded':False,'analysis_domain':selected_domain,'initial_model_identity':model['identity'],
            'runtime_assignment_sites':row['runtime_sites']}
        table[rid]=value
        if row['runtime_sites'] or model['runtime_writers']['opaque_storage_writes']:
            value['origin']='constructor_choice_with_possible_later_write';continue
        if not clean or any(p.get('issues') or p.get('evaluation_gaps') for p in model['constructor_paths']):continue
        cell={'kind':'storage','root':rid,'segments':[]}
        try:values=[_initial_term(read(cell,p['writes'],lookup),context,selected_domain) for p in clean]
        except (ValueError,KeyError,TypeError):continue
        if values and all(v==values[0] for v in values):
            v=values[0]
            if v.get('kind')=='literal' and type(v.get('value')) in (bool,int):value.update(value=v['value'],encoded=True,
                origin='fixed_constructor_or_declaration' if row['constructor_writes'] else 'fixed_type_default')
            elif v.get('initial_identity')=='deployment_caller':value.update(nonzero=True,encoded=True,origin='fixed_deployer_address')
    cache[token]=table
    return table


def encode_state(e,details=None):
    from .initial_state import domain,CAPABILITY,DEPLOYMENT
    if domain(e.lookup) in (CAPABILITY,DEPLOYMENT):
        from .state_encoding import encode
        return encode(e,details)
    items=[];constraints=[]
    for vid,v in state_facts(e.lookup).items():
        if not v['encoded']:continue
        cell=e.expr({'kind':'storage','root':vid,'segments':[]})
        constraints.append(cell!=0 if v.get('nonzero') else cell==v['value'])
        items.append(v)
    return constraints,items


def prestate_receipt(details,initial):
    d=details or {}
    if isinstance(initial,dict):
        return dict(initial,executed_prefix=d.get('prefix',[]),encoded_case=d.get('encoded_case',[]),
            encoded_request_bindings=d.get('encoded_request_bindings',d.get('request_context',{}).get('bindings',[])))
    return {'analysis_domain':'ac_checked_prestate_r1','analysis':'conditional_symbolic_with_checked_fixed_initializers','encoded_invariant_declarations':initial,
            'executed_prefix':d.get('prefix',[]),'encoded_case':d.get('encoded_case',[]),
            'encoded_request_bindings':d.get('encoded_request_bindings',d.get('request_context',{}).get('bindings',[])),
            'explicit_constructor_prefix_executed':False,'author_run_initial_state_verified':False}


def impossible_role(inv,oid):
    """P exclusion only if every clean committing path needs caller == fixed zero."""
    if not inv.backend.complete(oid):return False
    original=inv.backend.paths(oid)
    if not original:return False
    fixed=state_facts(inv.f.lookup(oid))
    from .request_scope import positive_caller_gate
    def zero(g):
        if g.get('op') in ('and','&&'):return any(zero(x) for x in g.get('args',[]))
        return positive_caller_gate(g,inv.f.lookup(oid)) and g.get('op') in ('==','!') and any(
            fixed.get(c['root'],{}).get('encoded') and fixed[c['root']].get('value')==0 for c in selectors(g))
    def value(x):
        if x.get('kind')=='literal':
            a=x.get('value')
            if isinstance(a,bool) or isinstance(a,int):return a
            if str(a).lower() in ('true','false'):return str(a).lower()=='true'
            try:return int(a,0)
            except (ValueError,TypeError):return None
        if x.get('kind')=='storage' and not x.get('segments'):return fixed.get(x.get('root'),{}).get('value')
        op=x.get('op');args=[value(v) for v in x.get('args',[])]
        if op=='!' and len(args)==1 and args[0] is not None:return not args[0]
        if len(args)!=2:return None
        a,b=args
        if op in ('and','&&') and False in args:return False
        if op in ('or','||') and True in args:return True
        if a is None or b is None:return None
        if op=='==':return a==b
        if op=='!=':return a!=b
        if op=='>=':return a>=b
        if op=='<=':return a<=b
        if op=='<':return a<b
        if op=='>':return a>b
        return None
    return all(any(zero(g) or value(g) is False for g in p['guards']) for pid,p in original)


````

## source/src/pr_next_joint/investigation/program.py

原文件 SHA-256 `ae16a9533e4b8571d7507f169449517e64df0c3197e0d4ade8c6663787496056`

````python
"""M1: original compiler identities, paths and structural edges only.

There is deliberately no import of an old detector, policy projection,
asset discovery, LLM consumer or report merger in this module.
"""
import copy
import hashlib
from pathlib import Path
from pr_next_joint.core import digest, require
from pr_next_joint.frontend.inventory import target_inventory
from pr_next_joint.frontend.source_entry_identity import entry_functions
from pr_next_joint.frontend.program_paths import MechanismPaths
from pr_next_joint.frontend.path_ir import walk, key
from pr_next_joint.frontend.storage import selectors
from pr_next_joint.graph.state_relations import expand_write
from .contracts import ident


class Facts:
    def __init__(self, bundle, native, sources, options, selected=None, description=None):
        require(all(bundle[k] == native[k] for k in ('program_id', 'build_id')), 'input_identity_mismatch')
        require(bundle.get('native_ir', {}).get('sha256') == digest(native), 'native_digest_mismatch')
        self.bundle, self.native, self.options = bundle, native, options
        self.lookups, self.operations, self.paths, self.writes, self.effects, self.terms = {}, {}, {}, {}, {}, {}
        self.references, self.gaps = {}, []
        inventory = target_inventory(bundle)
        available = {x['file'] + ':' + x['contract'] for x in inventory if x['selected']}
        self.selected = sorted(set(selected) if selected is not None else available)
        require(bool(self.selected) and set(self.selected) <= available, 'invalid_selected_targets')
        source_by_name = {s['file']: s for s in sources}
        for file, ast in bundle['ast_sources'].items():
            require(file in source_by_name, 'source_missing:' + file)
            content = source_by_name[file]['content'].encode('utf-8')
            require(hashlib.sha256(content).hexdigest() == source_by_name[file]['sha256'], 'source_hash_mismatch')
        for contract in bundle['contracts']:
            target = contract['file'] + ':' + contract['name']
            if target not in self.selected:
                continue
            lookup = MechanismPaths(bundle, contract, options.max_paths)
            lookup.analysis_scope = options.scope
            self.lookups[target] = lookup
            bases = lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']])
            for n in lookup.nodes.values():
                # All references retain the actual compiler node and file span.
                if n.get('nodeType') in ('VariableDeclaration', 'FunctionDefinition', 'Assignment', 'UnaryOperation',
                                         'FunctionCall', 'BinaryOperation', 'IndexAccess', 'MemberAccess', 'IfStatement'):
                    ref = ident('r', [target, n['id']])
                    self.references[ref] = {'target': target, 'ast_id': n['id'], 'kind': n['nodeType'],
                                            'name': n.get('name', n.get('memberName')), 'source': lookup.anchor(n)}
            for entry in entry_functions(lookup):
                fn = entry['signature']; oid = ident('op', [target, fn])
                body = lookup.function(fn)
                operation = {'id': oid, 'target': target, 'function': fn,
                             'source': lookup.anchor(body.get('generated_getter', body)),
                             'parameters': [], 'paths': [], 'gaps': [], 'generated_getter': bool(body.get('generated_getter'))}
                params = body.get('parameters', {}).get('parameters', [])
                for n in params:
                    operation['parameters'].append({'ref': ident('r', [target, n['id']]), 'name': n['name'],
                        'term': self.term({'kind': 'parameter', 'id': n['id'], 'type': n['typeDescriptions']['typeString']}, target)})
                self.operations[oid] = operation
                try:
                    paths = lookup.run(fn)
                except Exception as error:
                    self.gap(oid, 'path_extraction', type(error).__name__ + ':' + str(error)); continue
                for index, path in enumerate(paths):
                    pid = ident('path', [oid, index]); path = copy.deepcopy(path)
                    try:
                        path['writes'] = [item for w in path['writes'] for item in expand_write(w, lookup)]
                    except Exception as error:
                        path.setdefault('issues', []).append({'reason': 'write_expansion:' + str(error)})
                    self.paths[pid] = {'operation': oid, 'index': index, 'raw': path}
                    card = {'id': pid, 'flow': path['flow'], 'guards': [], 'writes': [], 'effects': [],
                            'issues': copy.deepcopy(path.get('issues', [])), 'evaluation_gaps': path.get('evaluation_gaps', [])}
                    for g in path['guards']:
                        card['guards'].append(self.term(g, target))
                    for wi, w in enumerate(path['writes']):
                        wid = ident('w', [pid, wi]); self.writes[wid] = {'operation': oid, 'path': pid, 'raw': w}
                        card['writes'].append({'id': wid, 'selector': self.term(w['path'], target),
                                              'value': self.term(w['value'], target), 'source': w['source']})
                    for ei, e in enumerate(path.get('sensitive_effects', [])):
                        eid = ident('fx', [pid, ei]); self.effects[eid] = {'operation': oid, 'path': pid, 'raw': e}
                        row = {'id': eid, 'kind': e['kind'], 'source': e['source']}
                        for field in ('recipient', 'amount', 'success'):
                            if e.get(field) is not None: row[field] = self.term(e[field], target)
                        card['effects'].append(row)
                    for value in [path.get('evaluated_terms', []), path.get('return_value')]:
                        for n in walk(value):
                            if n.get('kind'): self.term(n, target)
                    operation['paths'].append(card)
                    if card['issues'] or card['evaluation_gaps']:
                        self.gap(oid, 'program_path', {'path': pid, 'issues': card['issues'], 'evaluation_gaps': card['evaluation_gaps']})
        for target in self.selected:
            self.lookups[target]._investigation_facts=self
            self.term({'kind': 'actual_sender'}, target)
            self.term({'kind': 'transaction_value', 'type': 'uint256'}, target)
        edges = []
        for a in self.operations.values():
            a_roots = {w['raw']['path']['root'] for w in self.writes.values() if w['operation'] == a['id']}
            for b in self.operations.values():
                if a['target'] != b['target']: continue
                b_roots = {s['root'] for p in b['paths'] for s in selectors(self.paths[p['id']]['raw'])}
                roots = sorted(a_roots & b_roots)
                if roots:
                    edges.append({'from': a['id'], 'to': b['id'], 'roots': roots, 'kind': 'may_write_read',
                                  'meaning': 'structural_frontier_not_policy'})
        package = Path(__file__).resolve().parents[1]
        implementation = {p.relative_to(package).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(package.rglob('*.py'))}
        self.context = {'schema': 'scrv-facts-r2-1', 'identity': {k: bundle[k] for k in ('program_id', 'build_id')},
                        'implementation_sha256': digest(implementation), 'finite_options': options.record(),
                        'scope': options.scope, 'sources': sources, 'description': description,
                        'operations': list(self.operations.values()), 'references': self.references,
                        'terms': self.terms, 'frontier': edges, 'program_gaps': self.gaps}
        from .initial_state import model, domain
        self.context['state_analysis']={target:{'analysis_domain':domain(lookup),'initial_model_identity':model(self,target)['identity'],
            'candidate_amount_leaves':model(self,target)['candidate_amount_leaves']} for target,lookup in self.lookups.items()}
        from .summary import get_summaries
        self.summaries=get_summaries(self)
        from .call_summary import CallSummaries
        self.call_summaries = CallSummaries(self)
        self.context['call_summary_identity'] = self.call_summaries.identity
        self.context['effect_summary_identity']=self.summaries.identity
        from .candidates import source_candidates
        self.source_candidates=source_candidates(self)
        self.context['source_candidates']=self.source_candidates
        self.identity = digest(self.context)

    def term(self, value, target):
        ref = ident('e', [target, value])
        self.terms[ref] = {'target': target, 'expression': copy.deepcopy(value)}
        for n in walk(value):
            if n is not value and n.get('kind'):
                nr = ident('e', [target, n]); self.terms[nr] = {'target': target, 'expression': copy.deepcopy(n)}
        return ref

    def gap(self, operation, kind, reason):
        row = {'operation': operation, 'kind': kind, 'reason': reason}
        self.gaps.append(row); self.operations[operation]['gaps'].append(row)

    def operation_paths(self, oid, complete_only=False):
        for card in self.operations[oid]['paths']:
            item = self.paths[card['id']]
            p = item['raw']
            if complete_only and (p['flow'] not in ('normal', 'returned') or p.get('issues') or p.get('evaluation_gaps')):
                continue
            yield card['id'], p

    def lookup(self, oid):
        return self.lookups[self.operations[oid]['target']]

````

## source/src/pr_next_joint/investigation/properties.py

原文件 SHA-256 `8b66ede108f86ccd763905a3b67ef4642478e594a50cf3c8690c830b69305162`

````python
"""Finite, source-bound questions. Wording guides investigation, never certifies harm."""
import re
from itertools import product

from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, selector_relation, value_type
from .request_scope import claim_entries, holder_effect, linked_controls, unique_cells
from .ledger import MEASURES, bind_positions, movements
from .roles import path_qualification


def words(item):
    return ' '.join(str(item.get(k) or '') for k in ('claim','distinguish','distinguishing_question','observation'))


def interpret(item):
    raw = item.get('observation')
    req = dict(raw) if isinstance(raw,dict) else {}
    text = words(item)
    if re.search(r'\b(?:never check|does not (?:read|check)|bypass(?:es)?|missing (?:the )?control)\b',text,re.I) and re.search(r'freez|frozen|guard|control',text,re.I):
        return {**req,'measure':'missing_control'}
    if req.get('measure') in MEASURES or req.get('measure') in ('denied_qualified','direct_effect','authorization_violation'):
        return req
    if req.get('measure') and req['measure'] not in ('opens','blocks'):
        return req
    if re.search(r'allowance.{0,55}(?:gross|actual debit|less than)|more than (?:the |was )?(?:allowance|approved)|(?:gross|actual) debit.{0,70}(?:allowance|grant)',text,re.I):
        return {**req,'measure':'ledger_grant'}
    if re.search(r'(?:recipient|payee|receiver).{0,55}(?:less|zero|smaller|short)|(?:lower|reduced) (?:recipient )?credit|到账减少',text,re.I):
        return {**req,'measure':'ledger_receipt'}
    if re.search(r'(?:debited|debit|charged).{0,22}(?:more|greater|extra)|greater gross debit',text,re.I):
        return {**req,'measure':'ledger_debit'}
    if req.get('measure'):
        return req
    if item.get('category')=='AC' and re.search(r'(?:qualified|entitled|authorized|rightful|rightfully).{0,65}(?:reject|denied|refus)|wrongful.{0,18}(?:denial|reject)',text,re.I):
        return {**req,'measure':'denied_qualified'}
    if item.get('category') in ('FCR-MINT','FCR-TRANSFER','FCR-DESTROY') and re.search(r'\b(mint|issuance|confiscate|seize|destroy|burn|debit|transfer|issu(?:e|es))\b',text,re.I):
        return {**req,'measure':'direct_effect'}
    if item.get('category') in ('FCR-FREEZE','FCR-PAUSE') and re.search(r'block|revert|pause|freeze',text,re.I):
        return {**req,'measure':'blocks'}
    if item.get('category')=='AC' and re.search(r'(?:install|forge|acquire|grant itself).{0,36}(?:grant|allowance|permission)',text,re.I):
        return {**req,'measure':'holder_grant'}
    return None


def conflicting_measurements(inv,q,proposal):
    """Only explicit factual negations of the same measured positive condition conflict."""
    from .request_scope import observation_applies
    factual={
        'ledger_receipt':r'\b(?:recipient|payee)\b.{0,28}\b(?:always|necessarily)\b.{0,20}\b(?:full|unchanged)',
        'ledger_debit':r'\b(?:gross|actual) debit (?:never increases|is always unchanged)',
        'ledger_grant':r'\b(?:actual|gross) debit (?:never exceeds|is always within) (?:the )?(?:allowance|grant)',
        'denied_qualified':r'\b(?:qualified|authorized) (?:caller|role|manager) (?:is never (?:rejected|denied)|always succeeds)',
    }
    if any(proposal.get(k)!=q['current'].get(k) for k in ('observation','assumptions','next_check','actor','object','phase')):
        return []
    text=proposal.get('claim','')
    return [o['probe'] for row in q.get('observations',[]) if row['measure'] in factual and row['version']==q['version']
            and observation_applies(inv,q,row) and re.search(factual[row['measure']],text,re.I)
            for o in row['outcomes'] if o['predicate_value']]


def source_target(inv,anchor,target):
    return [o for o in inv.catalog.resolve(anchor) if inv.f.operations[o]['target']==target]


def premise_cases(inv, use, item, changed=()):
    """Separate expressly different values of the same declared cell. No free Boolean substitute."""
    lookup = inv.f.lookup(use)
    cells = unique_cells(s for s in inv.graph.request_reads(use) if not keys(s))
    text = words(item)
    axes, gaps = [], []
    for cell in cells:
        name = lookup.nodes.get(cell['root'],{}).get('name')
        if not name:
            continue
        regex=r'(?<![\w$])'+re.escape(name)+r'\s*(?:==|=)\s*(true|false|\d+)\b'
        values=list(dict.fromkeys(v.lower() for v in re.findall(regex,text,re.I)))
        if not values:
            continue
        if len({s['root'] for s in cells if lookup.nodes.get(s['root'],{}).get('name')==name})!=1:
            gaps.append('ambiguous source declaration '+name);continue
        typ=value_type(cell,lookup)
        if any((v in ('true','false')) != (typ=='bool') or typ!='bool' and not typ.startswith('uint') for v in values):
            gaps.append('literal sort unsupported: '+name);continue
        at='after' if any(selector_relation(cell,c)=='same_shape' for c in changed) else 'before'
        axes.append([{'cell':cell,'source_name':name,'value':v=='true' if typ=='bool' else int(v),'frame':at} for v in values])
    fixed=[]
    assumptions=item.get('assumptions',[])
    if isinstance(assumptions,str):assumptions=[assumptions]
    named=unique_cells(inv.graph.request_reads(use))
    for a in assumptions:
        match=re.fullmatch(r'(before|after)\s+([A-Za-z_$][\w$]*(?:\[[\w$.]+\])*)\s*(?:==|=)\s*(\d+|true|false)',str(a).strip(),re.I)
        if not match:continue
        at,name,value=match.groups(); found=[s for s in named if inv.backend._storage_name(use,s)==name]
        if len(found)!=1:gaps.append('unbound scoped premise '+name);continue
        fixed.append({'cell':found[0],'source_name':name,'frame':at.lower(),'value':value.lower()=='true' if value.lower() in ('true','false') else int(value)})
    if len(axes)>3 or len(axes)>1 and any(len(axis)>1 for axis in axes):
        return [],gaps+['multiple alternative clauses cannot be independently cross-multiplied']
    return [fixed+list(c) for c in product(*axes)] if axes else [fixed],gaps


def privileged_paths(inv,oid):
    return [pid for pid,p in inv.backend.paths(oid) if path_qualification(inv.f,oid,p)]


def stage(inv,use):
    facts=inv.f; target=facts.operations[use]['target']
    listed=[]
    for cell in unique_cells(inv.graph.request_reads(use)):
        if keys(cell) or not value_type(cell,facts.lookup(use)).startswith(('uint','bool')):
            continue
        writers=[]
        for oid in sorted(inv.graph.access[target,cell['root']]['writers']):
            matches=[pid for pid,p in inv.backend.paths(oid) if any(selector_relation(cell,w['path'])=='same_shape' for w in p['writes'])]
            if matches:
                writers.append({'operation':oid,'paths':matches,'role_guarded_paths':privileged_paths(inv,oid)})
        listed.append({'cell':cell,'name':inv.backend._storage_name(use,cell),'runtime_writers':writers})
    return listed


def source_graph_holes(inv,binding,item):
    root=binding['core_operation']; target=inv.f.operations[root]['target']
    claimed=claim_entries(inv,binding,item)
    controls=unique_cells(w['path'] for _,p in inv.backend.paths(root) for w in p['writes'] if value_type(w['path'],inv.f.lookup(root))=='bool')
    if not controls:
        return []
    related=[]
    for oid in sorted(claimed-{root}):
        ops=[(pid,movements(inv.backend,oid,p)) for pid,p in inv.backend.paths(oid)]
        debit=unique_cells(c for pid,m in ops for c in m['-'])
        if not debit:
            continue
        peers=[]
        for other,entry in inv.f.operations.items():
            if entry['target']!=target or other==oid:continue
            linked=linked_controls(inv,root,other)
            if not any(selector_relation(c,l)=='same_shape' for c in controls for l in linked):continue
            for pid,p in inv.backend.paths(other):
                m=movements(inv.backend,other,p)
                if any(selector_relation(a,b)=='same_shape' for a in debit for b in m['-']):
                    peers.append({'operation':other,'path':pid,'controls':linked})
        reads=linked_controls(inv,root,oid)
        related.append({'use':oid,'debit_positions':debit,'control_reads':reads,'control_writers':controls,'peer_controlled_uses':peers})
    return related


def plan_property(inv,binding,item,plan,req):
    """Select finite typed questions with compiler-resolved endpoints, or disclose a local gap."""
    measure=req['measure']; root=binding['core_operation']; target=inv.f.operations[root]['target']
    entries=claim_entries(inv,binding,item); contexts=[]
    if measure in MEASURES:
        uses=[oid for oid in sorted(entries) if holder_effect(inv,oid)]
        if req.get('at'):uses=[o for o in source_target(inv,req['at'],target) if o in entries]
        elif root in uses and bind_positions(inv.backend,root,item)[0]:uses=[root]
        reasons=[]
        for use in uses:
            pos,err=bind_positions(inv.backend,use,item)
            if err:reasons.append(err);continue
            edges=stage(inv,use)
            forced=source_target(inv,req.get('after'),target) if req.get('after') else []
            if req.get('after') and len(forced)!=1:reasons.append('requested_intervention_not_unique');continue
            choices={}
            for edge in edges:
                if req.get('control') and req['control']!=edge['name']:continue
                for w in edge['runtime_writers']:
                    change=w['operation']
                    if forced and change not in forced or not forced and root!=use and change!=root:continue
                    if not w['role_guarded_paths']:continue
                    choices.setdefault(change,[]).append(edge['cell'])
            if not choices:reasons.append('no_source_bound_runtime_privileged_writer');continue
            for change,controls in choices.items():
                ctx=inv._compare_context({'current':item},change,use)
                ctx['observable']={'measure':measure,'ledger':pos,'control_selectors':controls,
                                   'change_paths':privileged_paths(inv,change)}
                cases,gaps=premise_cases(inv,use,item,controls)
                if gaps:reasons+=gaps;continue
                ctx['premise_cases']=cases
                # An address alias is admitted only for two actual source parameter names.
                params=inv.f.lookup(use).function(inv.f.operations[use]['function']).get('parameters',{}).get('parameters',[])
                addr={p['name']:{'kind':'parameter','id':p['id'],'type':p['typeDescriptions']['typeString']} for p in params if p['typeDescriptions']['typeString'] in ('address','address payable')}
                ctx['request_aliases']=[]
                for a,op,b in re.findall(r'\b(\w+)\s*(==|!=)\s*(\w+)\b',str(item.get('assumptions',[]))):
                    if a in addr and b in addr:ctx['request_aliases'].append([addr[a],addr[b],op])
                contexts.append((change,use,ctx))
        reason=','.join(dict.fromkeys(reasons)) or 'more_than_one_applicable_request_or_intervention'
    elif measure=='missing_control':
        rows=source_graph_holes(inv,binding,item)
        relevant=[r for r in rows if r['peer_controlled_uses'] and not r['control_reads']]
        if relevant:
            contexts=[(root,relevant[0]['use'],{'observable':{'measure':measure,'alternatives':relevant},'operation':root,
                      'checked_uses':[r['use'] for r in relevant],'frame_type':'committed_intervention_then_actual_alternative'})]
        reason='no_same_target_same_right_comparator_or_unresolved_control'
    else:
        ctx=inv._compare_context({'current':item},root,root)
        ctx.update({'observable':{'measure':measure,'claim':item.get('claim',''),'category':item.get('category')},
                    'operation':root,'stage':stage(inv,root),'frame_type':'single_original_entry'})
        if req.get('authorization'):ctx['observable']['authorization']=req['authorization']
        if measure=='direct_effect' and ctx.get('bindings'):
            ctx['exploratory_request_bindings_not_the_claim']=ctx.pop('bindings')
        params=inv.f.lookup(root).function(inv.f.operations[root]['function']).get('parameters',{}).get('parameters',[])
        addr={p['name']:{'kind':'parameter','id':p['id'],'type':p['typeDescriptions']['typeString']} for p in params if p['typeDescriptions']['typeString'] in ('address','address payable')}
        ctx['request_aliases']=[[addr[a],addr[b],op] for a,op,b in re.findall(r'\b(\w+)\s*(==|!=)\s*(\w+)\b',str(item.get('assumptions',[]))) if a in addr and b in addr]
        contexts=[(root,root,ctx)]
        if measure=='direct_effect':
            contexts[0][2]['privileged_paths']=privileged_paths(inv,root)
        reason='unresolved_direct_property'
    pick=None
    if len(contexts)==1:
        change,use,ctx=contexts[0]
        pick={'action':'compare','change':change,'observe':use,'measure':measure,'status':'source_bound',
              'expectations':{},'context':ctx,'scope':{'target':target,'finding_root':root,'use':use,'intervention':change,
                  'measure':measure,'controls':ctx['observable'].get('control_selectors',[]),'objects':[ctx['observable']['ledger'][k] for k in ('debit','credit')] if 'ledger' in ctx['observable'] else [],
                  'checked_uses':ctx.get('checked_uses',[use]),'frame_type':ctx.get('frame_type','same_request_two_worlds'),
                  'extent':'compiler-selected entries, ordered keys and recorded path conditions only'}}
    inherited_pairs=list(plan.get('selected_pairs',[]))
    plan['observation_choice']={'ordinary_pairs':inherited_pairs,'selected':pick,'pool':[pick] if pick else [],'status':'selected_property' if pick else 'unsupported',
        'reason':'source-resolved finite property' if pick else reason,'property_requested':measure,'claim_text':item['claim'],'possible_compilations':len(contexts),
        'stage_evidence':stage(inv,root),'request_resolution':{'finding_root':root,'use':pick['observe'] if pick else None,
        'possible_uses':sorted(entries),'unmeasured_uses':sorted(entries-{pick['observe'],pick['change']}) if pick else sorted(entries)}}
    if pick:
        plan['selected_pairs']=[{'change':pick['change'],'observe':pick['observe'],'source_reason':'typed property and matching applied target'}]
    inv.graph.events.append({'action':'compile_source_property','measure':measure,'root':root,'selected':bool(pick),'reason':plan['observation_choice']['reason']})


````

