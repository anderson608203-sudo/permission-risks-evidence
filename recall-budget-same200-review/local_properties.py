"""Typed, source-effect queries for a compiled property."""
import copy
import hashlib
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, selector_relation
from pr_next_joint.verification.sequence import qualify, read
from pr_next_joint.verification.source_worlds import frame, encode_frame
from pr_next_joint.verification.program_encoding import MechanismEncoder
from pr_next_joint.verification.expressions import Unsupported
from .ledger import movements, unit_origin, flow, grant_for
from .roles import path_qualification, fixed_role_terms
from .relations import beneficiary_condition


def audit_use_guards(b,policy):
    """Check each supplied use in its own frame, without synthesizing a grant sequence.

    This is a local well-formedness/consistency check. SAT here is never evidence
    of unauthorized acquisition. No input assignments are read from the solver.
    """
    from pr_next_joint.verification.solver import solve
    from pr_next_joint.core import digest
    results=[]
    for use in policy.get('acquisition_uses',[]):
        if b.remaining()<=0:
            results.append({'operation':use['operation'],'path':use['path'],'status':'not_executed','reason':'shared_budget'})
            continue
        oid,pid=use['operation'],use['path']
        record={'operation':oid,'path':pid,'target':b.f.operations[oid]['target'],
                'status':'open','scope':'individual_use_only','supports_takeover':False}
        results.append(record)
        try:
            p=b.f.paths[pid]['raw']
            if not safe_path(b,oid,pid,p):
                record['reason']='use_has_relevant_residual';continue
            e=MechanismEncoder(b.f.lookup(oid))
            fr=b.source_frame(oid,pid,0)
            term=encode_frame(e,fr)
            effect=_effect(e,fr,b.f.lookup(oid))
            solver=e.z.Solver()
            solver.add(term,effect,*e.constraints,*e.domain_constraints)
            text=solver.sexpr()
            formula_ref=hashlib.sha256(text.encode()).hexdigest()
            b.formulas.setdefault(formula_ref,{'sha256':formula_ref,'text':text,'scope_context':{
                'operation':oid,'path':pid,'scope':'individual use, no acquisition prefix or deployment reachability'}})
            b.check()
            answer=solve(solver,initial_ms=max(1,min(b.f.options.solver_timeout_ms,int(b.remaining()*1000))))
            record.update(status=str(answer),formula_ref=formula_ref,variable_domain='single isolated use frame',
                          source_guard_roots=sorted({s['root'] for s in selectors(p['guards'])}))
        except Unsupported as error:
            record.update(status='unsupported',reason=str(error))
        except TimeoutError:
            record.update(status='not_executed',reason='shared_budget')
        finally:
            evidence_key=digest([b.f.identity,oid,pid,record.get('formula_ref'),record['status']])
            b.__dict__.setdefault('use_guard_evidence',{})[evidence_key]=dict(record)
    return results


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
    if kind in ('authorization_violation','denied_qualified'):
        from .policy_binding import audit_authorization
        audit=audit_authorization(f,oid,req.get('authorization'))
        if any(not r['matches'] for r in audit):
            return {'kind':'causal_compare','change':oid,'observe':primary_use,'queries':[],'property_excluded':False,
                    'local_errors':[{'reason':'source_ir_disagreement','checks':audit}],
                    'worlds':[],'comparisons':[],'property_identity':prop.get('id')}
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
            if not b.source_path(oid,source_pid,source_path).get('source_call_subcases'):
                f.call_summaries.refine(b,oid,source_pid,b.active_property_roots)

    def pair(e, base, extra, details, values):
        details = dict(details, property_identity=context.get('property_identity'),
                       semantic_version=context.get('semantic_version'),
                       prefix_state_handoff=reached, prefix=reached.get('prefix',[]),
                       **({'initial_prefix_policy':'constructor_only_for_explicit_prefix'} if reached else {}),
                       property_validated=details.get('property_validated',True), validation='typed source entities and actual committed effect')
        feasible = b._query(e, base, 'local_premises_feasible', details)
        queries.append(feasible)
        if not feasible['bounded_condition_confirmed']:
            rows.append({'feasible_probe': feasible['id'], 'state': 'premise_' + feasible['answer'], 'scope': details})
            return
        tested = b._query(e, e.z.And(base, extra), kind, details)
        queries.append(tested)
        rows.append({'feasible_probe': feasible['id'], 'result_probe': tested['id'],
                     'state': tested['answer'], 'scope': details})

    reached=context.get('reached_state') or {}
    prefix_frames=reached.get('frames',[])
    prefix_writes=reached.get('writes',[])
    slot=len(prefix_frames)
    def current_frame(pid):
        return b.source_frame(oid,pid,slot,prefix_writes)
    def prefix_conditions(e):
        from .behavior import ordered_clocks
        return [encode_frame(e,pf) for pf in prefix_frames]+[e.expr(pf['caller'])!=0 for pf in prefix_frames]+ordered_clocks(e,slot)

    separate_uses=[]
    if kind == 'authorization_violation':
        policy = req.get('authorization')
        if not policy:
            gaps.append({'reason': 'authorization_relationship_not_bound'})
        else:
            acquiring = policy.get('property_family') == 'acquire'
            uses = policy.get('acquisition_uses', []) if acquiring else [None]
            if acquiring and not uses:
                gaps.append({'reason':'acquired_authority_has_no_bound_actual_use'})
            for pid, p in b.paths(oid):
                b.check()
                scoped_write=policy.get('effect_write')
                if scoped_write and scoped_write['path']!=pid:continue
                if not safe_path(b, oid, pid, p):
                    gaps.append({'path': pid, 'reason': 'authorization_path_dependency_unresolved'})
                    continue
                # A joint grant/use query owns its entire encoder. In particular
                # an unsupported sibling cannot leave domains, constraints,
                # credential/hash terms or symbols in a supported sibling.
                for row in uses:
                    b.check()
                    check = {'grant_path':pid,'operation':row['operation'] if row else oid,
                             'path':row['path'] if row else pid,'scope':'joint_grant_then_use',
                             'supports_takeover':False,'status':'open'}
                    if row: separate_uses.append(check)
                    try:
                        e = MechanismEncoder(lookup)
                        z = e.z
                        fr = current_frame(pid)
                        actor = e.expr(fr['caller'])
                        expected = e.expr(read(qualify(policy['predicate'],slot),prefix_writes,lookup))
                        if scoped_write:
                            cell=fr['writes'][scoped_write['version']]['path']
                            before=e.expr(read(cell,fr['before'],lookup))
                            after=e.expr(read(cell,fr['before']+fr['writes'],lookup))
                            effect=before!=after
                            if len(fr['writes'])>1:
                                version=scoped_write['version']
                                earlier=fr['before']+fr['writes'][:version]
                                at_write=e.expr(read(cell,earlier+[fr['writes'][version]],lookup))
                                effect=z.And(effect,at_write!=e.expr(read(cell,earlier,lookup)),at_write==after)
                        else:
                            effect=_effect(e,fr,lookup)
                        detail = {'operation':oid,'target':f.operations[oid]['target'],'use_path':pid,
                            'expected_authorization':policy,'actual_guards':fr['guards'],
                            'argument_domain':'all_source_inputs_on_this_committing_path',
                            'effect_required':True,'acquisition_use_required':acquiring}
                        values = {'caller':actor,'authorization_holds':expected}
                        clocks = []
                        if row:
                            up = f.paths[row['path']]['raw']
                            if not safe_path(b,row['operation'],row['path'],up):
                                raise Unsupported('acquired_authority_use_unresolved')
                            authority = row.get('authority') or policy.get('subject')
                            roots = {s['root'] for s in selectors(authority)}
                            if isinstance(authority,dict) and 'root' in authority: roots.add(authority['root'])
                            def conjuncts(term):
                                return [g for a in term['args'] for g in conjuncts(a)] if term.get('op') in ('and','&&') else [term]
                            gates = [g for guard in up['guards'] for g in conjuncts(guard)
                                     if roots & {s['root'] for s in selectors(g)}]
                            if not gates: raise Unsupported('acquired_authority_not_used_by_downstream_guard')
                            after = b.source_frame(row['operation'],row['path'],slot+1,prefix_writes+fr['writes'])
                            # The same request did not possess this qualification
                            # before the grant. A preexisting successful use is
                            # not evidence of newly acquired authority.
                            mark = len(e.constraints)
                            before_permission = z.And(*[e.expr(read(qualify(g,slot+1),prefix_writes,lookup)) for g in gates])
                            pre_checks = e.constraints[mark:];del e.constraints[mark:]
                            after_permission = z.And(*[e.expr(read(qualify(g,slot+1),prefix_writes+fr['writes'],lookup)) for g in gates])
                            productive = _effect(e,after,lookup)
                            use_caller=e.expr(after['caller'])
                            actor_links=[use_caller==actor];nominees=[]
                            # A requester can explicitly select a fresh
                            # controlled address in an unrestricted address
                            # grant. This is a conditional source subcase,
                            # not control of an arbitrary observed recipient.
                            for w in p['writes']:
                                value=w['value']
                                if w['path']['root'] not in roots or value.get('kind')!='parameter' or value.get('type') not in ('address','address payable'):continue
                                fixed=[g for guard in p['guards'] for g in conjuncts(guard)
                                       if g.get('op')=='==' and any(key(x)==key(value) for x in g.get('args',[])) and
                                       any(x.get('kind') in ('storage','literal','contract_address') for x in g.get('args',[]))]
                                if fixed:continue
                                selected=e.expr(qualify(value,slot))
                                actor_links.append(z.And(use_caller==selected,selected!=0))
                                nominees.append({'argument':value,'kind':'selectable_self_controlled_address',
                                    'conditional':True,'all_actual_source_restrictions_retained':True,
                                    'arbitrary_observed_recipient_control_not_assumed':True})
                            effect = z.And(effect,encode_frame(e,after),productive,
                                *pre_checks,z.Not(before_permission),after_permission,
                                z.Or(*actor_links))
                            from .behavior import ordered_clocks
                            clocks = ordered_clocks(e,slot+1)
                            detail.update(acquired_use=row,authority_gates=gates,
                                acquisition_precondition='same request lacks this authority before the actual grant',
                                actor_scope='same requester or a source-selectable controlled nominee; not a universal identity assumption',
                                nominee_control_subcases=nominees,
                                before_writes=prefix_writes,after_writes=prefix_writes+fr['writes'],
                                new_authority_required=True,downstream_effect_required=True)
                            values.update(use_caller=use_caller,
                                authority_before=before_permission,authority_after=after_permission,
                                downstream_effect=productive)
                        values['sensitive_effect']=effect
                        first=len(queries)
                        pair(e,z.And(encode_frame(e,fr),actor!=0,*prefix_conditions(e),*clocks),
                             z.And(effect,z.Not(expected)),detail,values)
                        checked=queries[first:]
                        check.update(status=checked[-1]['answer'] if checked else 'open',
                            probes=[x['id'] for x in checked],
                            supports_takeover=any(x['label']==kind and x['bounded_condition_confirmed'] for x in checked))
                    except Unsupported as error:
                        check.update(status='unsupported',reason=str(error))
                        gaps.append({'path':pid,'use':row,'reason':str(error)})
    elif kind == 'denied_qualified':
        policy = req.get('authorization')
        if not policy:
            gaps.append({'reason': 'qualified_denial_policy_not_bound'})
        else:
            subject = policy.get('subject')
            denial_roots={s['root'] for s in selectors(policy.get('predicate',{}))}
            if isinstance(subject,dict) and 'root' in subject:denial_roots.add(subject['root'])
            rejecting = [(pid, p) for pid, p in f.operation_paths(oid) if p['flow'] == 'reverted']
            for pid, p in rejecting:
                b.check()
                if not p['guards'] or not safe_path(b, oid, pid, p):
                    continue
                for spid, sp in b.paths(oid):
                  try:
                    if not safe_path(b,oid,spid,sp):
                        raise Unsupported('qualified_denial_productive_path_unresolved')
                    e = MechanismEncoder(lookup)
                    z = e.z
                    actor = e.expr(qualify({'kind': 'actual_sender'}, slot))
                    allowed = e.expr(read(qualify(policy['predicate'], slot),prefix_writes,lookup))
                    controls = {s['root'] for s in selectors(p['guards'][-1])}
                    if not (controls & denial_roots):
                        continue
                    sf = current_frame(spid)
                    def conjuncts(g):
                        return [v for a in g['args'] for v in conjuncts(a)] if g.get('op') in ('and','&&') else [g]
                    def only_authorization(g):
                        roots={s['root'] for s in selectors(g)}
                        return bool(roots & denial_roots) and roots<=denial_roots and any(
                            v.get('sequence_role')=='caller' for v in walk(g))
                    guards=[g for term in sf['guards'] for g in conjuncts(term)]
                    removed=[g for g in guards if only_authorization(g)]
                    if not removed:continue
                    conditioned=dict(sf,guards=[g for g in guards if not only_authorization(g)])
                    productive=z.And(encode_frame(e,conditioned),_effect(e,sf,lookup))
                    original_denial=z.And(*[e.expr(read(qualify(g,slot),prefix_writes,lookup)) for g in p['guards']])
                    detail = {'operation': oid, 'target': f.operations[oid]['target'], 'use_path': pid,
                              'productive_path':spid,'corrected_authorization_guards':removed,
                              'expected_authorization': policy, 'actual_denial': p['guards'],
                              'counterfactual_change': 'only the matched authorization guard is corrected',
                              'other_request_preconditions_retained': True, 'effect_required': True,
                              'argument_domain': 'all_source_inputs_on_this_rejecting_path'}
                    pair(e, z.And(actor != 0, allowed,productive,*prefix_conditions(e)),
                         original_denial, detail, {'caller': actor, 'authorization_holds': allowed})
                  except Unsupported as error:
                    gaps.append({'path':pid,'productive_path':spid,'reason':str(error)})
    elif kind == 'direct_effect':
        cat = req['category']
        if b.complete(oid) and not f.summaries.positions(oid) and all(
                not p.get('sensitive_effects') for _,p in b.paths(oid)):
            rows.append({'state':'not_privileged','operation':oid,
                'reason':'complete_source_has_no_direct_holder_quantity_effect',
                'scope':'local entry only; dependent value uses have separate obligations'})
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
                    from .ledger import native_only_position
                    if native_only_position(b,oid,cell):
                        rows.append({'state':'not_privileged','path':pid,'position':cell,
                            'reason':'native_account_entitlement_without_source_token_unit_is_additional_scope'})
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
                        from .financial_value import distributed_value, native_settlement
                        paid,settlement=native_settlement(b,e,oid,fr,cell,holder)
                        conditions.append(start-end>distributed_value(b,e,oid,p,fr,cell,holder,all_transfers=False)+paid)
                        details['same_holder_settlement']=settlement
                    consent_resolved=True
                    if cat!='FCR-MINT':
                        from .financial_value import consent,interpretation_for
                        permitted,consent_resolved,basis=consent(b,e,oid,p,fr,cell,holder,start-end,
                            interpretation_for(prop,oid,pid,cell))
                        details['holder_consent']=basis
                        details['property_validated']=consent_resolved
                        conditions.append(z.Not(permitted))
                    bound = [e.expr(qualify(x['parameter'], slot)) == e.expr(x['value']) for x in context.get('bindings', [])]
                    pair(e, z.And(encode_frame(e, fr), actor != 0, *prefix_conditions(e), *roles, *bound), z.And(*conditions), details,
                         {'actor': actor, 'affected_account': holder, 'before': start, 'after': end, 'gross_debit': debit})
                    if not consent_resolved and queries[-1].get('answer')!='unsat':
                        gaps.append({'path':pid,'position':cell,'reason':'holder_authorization_quantity_basis_unresolved'})
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
    from .quantity_checks import check_quantities
    amount_checks=check_quantities(b,prop) if kind=='direct_effect' else []
    return {'kind': 'causal_compare', 'observed_measure': kind, 'property_identity': context.get('property_identity'),
            'amount_correspondence':amount_checks,
            'independent_use_checks':separate_uses,
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
        if not feasible['bounded_condition_confirmed']:
            rows.append({'feasible_probe':feasible['id'],'state':'premise_'+feasible['answer'],'scope':details});return
        tested=b._query(e,e.z.And(base,extra),kind,details);queries.append(tested)
        rows.append({'feasible_probe':feasible['id'],'result_probe':tested['id'],'state':tested['answer'],'scope':details})
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
