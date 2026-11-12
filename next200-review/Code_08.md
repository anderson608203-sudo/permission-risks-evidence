# 源码文本 · 8

## source/src/pr_next_joint/investigation/blocking.py

原文件 SHA-256 `2e1677896c366aa6d2f3171ebb901c56409d6fd07dff565ed56b3affacf66961`

````python
"""Productive-request comparison with a shared real prefix and scoped exclusion."""
import itertools
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import selectors, keys, selector_relation
from pr_next_joint.verification.source_worlds import frame, encode_frame, serialize_world
from pr_next_joint.verification.program_encoding import MechanismEncoder
from pr_next_joint.verification.sequence import qualify
from pr_next_joint.verification.expressions import Unsupported
from .ledger import movements, unit_origin, flow, grant_for, native_only_position
from .roles import path_qualification, fixed_role_terms


def continuation_frontier_covered(b, operation):
    """Every unexpanded continuation has an explicit source prefix.

    Loop prefixes and unresolved calls retain necessary guards. A failed
    frontend or a discarded path frontier does not provide that coverage.
    """
    rows=list(b.f.operation_paths(operation))
    return bool(rows) and not any(g.get('kind')=='path_extraction' for g in b.f.operations[operation]['gaps']) and not any(
        'source_path_frontier_bound_exceeded' in str(i.get('reason',''))
        for _,p in rows for i in p.get('issues',[]))


def may_continue(b,e,operation,pid,writes,slot,request=None,primary=False):
    """Necessary source guards overapproximate an unmodeled continuation.

    This formula is usable only under NOT to prove *no* productive bypass.
    SAT of it is not a real transfer, and UNSAT of the overall risk query is
    not a refutation when this approximation participated.
    """
    from pr_next_joint.verification.sequence import read
    p=b.f.paths[pid]['raw'];z=e.z
    guards=list(p['guards']);dropped=[]
    for call in b.f.call_summaries.rows.values():
        if call['operation']!=operation or call['path']!=pid:continue
        if call['mode']!='STATICCALL' and call['unresolved_implementation']:
            # Unknown callbacks may change storage. Only guards evaluated
            # before the actual call remain necessary source conditions.
            permitted={key(g)for g in call['callpoint_guards']} if call['callpoint_exact'] else set()
            dropped += [g for g in guards if key(g)not in permitted]
            guards=[g for g in guards if key(g)in permitted]
    opaque={'unknown','external_return','read_call','call_unresolved','credential_recovery','index','array_length'}
    kept=[];terms=[];variables={}
    mc,md=len(e.constraints),len(e.domain_constraints)
    def local_input(node):
        # Intervention and prefix inputs are already fixed for this shared
        # state. Only this alternative transaction may choose new inputs.
        return (node.get('kind')=='parameter' and node.get('step')==slot or
                node.get('kind')=='transaction_origin' and node.get('sequence_step')==slot)
    for guard in guards:
        if any(n.get('kind')in opaque or n.get('kind')=='parameter' and '[' in n.get('type','') for n in walk(guard)):
            dropped.append(guard);continue
        g=read(qualify(guard,slot),writes,e.lookup)
        markc,markd=len(e.constraints),len(e.domain_constraints)
        try:
            term=e.expr(g);terms.append(term);kept.append(guard)
            if not primary:
                for n in walk(g):
                    if local_input(n):
                        value=e.expr(n)
                        if z.is_const(value) and not (z.is_int_value(value)or z.is_true(value)or z.is_false(value)):
                            variables[str(value)]=value
        except Unsupported:
            del e.constraints[markc:];del e.domain_constraints[markd:];dropped.append(guard)
    # A source-derived holder mapping narrows an alternate route to the
    # original holder. Ambiguous mapping remains an overapproximation.
    if not primary and request is not None:
        hs=[keys(w['path'])[0]for w in p['writes'] if len(keys(w['path']))==1 and
            unit_origin(b,operation,w['path']) and w['path']in movements(b,operation,p)['-']]
        if hs and all(key(h)==key(hs[0])for h in hs):
            try:
                h=read(qualify(hs[0],slot),writes,e.lookup);value=e.expr(h)
                terms.append(value==request['holder'])
                for atom in walk(h):
                    if local_input(atom):
                        v=e.expr(atom);variables[str(v)]=v
            except Unsupported:pass
    local=e.constraints[mc:]+e.domain_constraints[md:]
    del e.constraints[mc:];del e.domain_constraints[md:]
    value=z.And(*terms,*local)
    if variables:value=z.Exists(list(variables.values()),value)
    return value,{'operation':operation,'path':pid,'kind':'necessary_source_guard_overapproximation',
        'retained_guards':kept,'omitted_guards':dropped,'not_a_productive_witness':True,
        'only_excluding_this_continuation_supports_blockage':True}


def request_terms(b, e, fr, operation):
    path = b.f.paths[fr['path']]['raw']
    lookup = b.f.lookup(operation)
    moves = movements(b, operation, path)
    from .summary import local_delta, unique
    debits = unique(w['path'] for w in path['writes'] if local_delta(w)[0] == '-' and unit_origin(b, operation, w['path']))
    credits = unique(w['path'] for w in path['writes'] if local_delta(w)[0] == '+' and unit_origin(b, operation, w['path']))
    holders = {str(flow(e, lookup, fr, c)[0]): flow(e, lookup, fr, c)[0] for c in debits}
    recipients = {str(flow(e, lookup, fr, c)[0]): flow(e, lookup, fr, c)[0] for c in credits}
    numeric = [b.f.terms[p['term']]['expression'] for p in b.f.operations[operation]['parameters']
               if b.f.terms[p['term']]['expression'].get('type','').startswith('uint')]
    # This adapter is source typed. Ambiguous multi-asset/multi-quantity entries
    # remain an explicit dependency rather than using parameter names/order.
    if len(holders) != 1 or len(recipients) != 1 or len(numeric) != 1:
        return None
    return {'holder': next(iter(holders.values())), 'recipient': next(iter(recipients.values())),
            'amount': e.expr(qualify(numeric[0], fr['slot']))}


def alternate_continuation(b, e, other, pid, after_writes, request, slot):
    path = b.f.paths[pid]['raw']
    if path_qualification(b.f, other, path):
        return None, 'privileged_assistance_is_not_an_ordinary_bypass'
    dependencies = b.condition_dependencies(other, pid, path)
    if dependencies['unknown_dependencies'] or dependencies['credential_dependencies']:
        return None, 'alternative_has_decisive_call_or_credential_dependency'
    mark_constraints, mark_domain = len(e.constraints), len(e.domain_constraints)
    fr = frame(b.f, other, pid, slot, after_writes)
    use, _ = productive(b, e, fr, other)
    if e.z.is_false(e.z.simplify(use)):
        # A known return-false/no-effect branch needs no request adapter.
        return e.z.BoolVal(False), None
    own = request_terms(b, e, fr, other)
    if own is None:
        return None, 'alternative_typed_request_mapping_ambiguous'
    equality = [own[k] == request[k] for k in ('holder','recipient','amount')]
    local = list(e.constraints[mark_constraints:]) + list(e.domain_constraints[mark_domain:])
    del e.constraints[mark_constraints:]
    del e.domain_constraints[mark_domain:]
    variables = [e.expr(fr['caller'])]
    variables += [e.expr(qualify(b.f.terms[p['term']]['expression'], slot)) for p in b.f.operations[other]['parameters']]
    return e.z.Exists(variables, e.z.And(use, *equality, *local)), None


def productive(b, e, fr, use):
    z = e.z
    mark = len(e.constraints)
    path = b.f.paths[fr['path']]['raw']
    terms, objects = [], []
    for cell in movements(b, use, path)['-']:
        if not unit_origin(b, use, cell) or native_only_position(b, use, cell):
            continue
        h, start, end, debit, credit = flow(e, b.f.lookup(use), fr, cell)
        credited=[]
        for other in movements(b,use,path)['+']:
            if selector_relation(cell,other)!='same_shape' or key(cell)==key(other):continue
            recipient,before,after,_,_=flow(e,b.f.lookup(use),fr,other)
            credited.append(z.And(recipient!=h,recipient!=0,after>before))
        terms.append(z.And(h != 0, start > end, z.Or(*credited)))
        objects.append(cell)
    success = encode_frame(e, fr)
    local = e.constraints[mark:]
    del e.constraints[mark:]
    return z.And(success, z.Or(*terms), *local), objects


def preserved_by_source_transition(b, change, use, prop, qualified_changes):
    """Prove one use cannot be blocked, independently of prefix enumeration.

    A constructor may disable a use, so a productive-state search starts with
    a nonempty enabling prefix. UNSAT for just that prefix is not a general
    exclusion. The backend's separate persistent-invariant overapproximation
    can prove the actual source transition preserves *any* productive input.
    Only that UNSAT certificate is consumed here; SAT is never a finding and
    no constructor/explicit initial value is relaxed for positive evidence.
    Keeping the original use available suffices even if other routes exist.
    """
    if not b.complete(change) or not b.complete(use):return False,[]
    from .scope_relevance import potential_role
    if any(potential_role(b.f,change,path) and not path_qualification(b.f,change,path)
           for _,path in b.paths(change)):return False,[]
    paths=list(b.paths(use))
    for oid,rows in ((change,qualified_changes),(use,paths)):
        for pid,path in rows:
            deps=b.condition_dependencies(oid,pid,path)
            if deps['unknown_dependencies'] or deps['credential_dependencies']:return False,[]
    queries=[]
    for cpid,cp in qualified_changes:
        b.check()
        try:
            e=MechanismEncoder(b.f.lookup(use));z=e.z
            cf=frame(b.f,change,cpid,0)
            role=path_qualification(b.f,change,cp)
            roles,origins=fixed_role_terms(e,role,0)
            base=z.And(encode_frame(e,cf),*roles,e.expr(cf['caller'])!=0)
            before=[];after=[]
            for pid,_ in paths:
                a=frame(b.f,use,pid,1)
                c=frame(b.f,use,pid,1,cf['writes'])
                before.append(productive(b,e,a,use)[0])
                after.append(productive(b,e,c,use)[0])
            detail={'operation':change,'target':b.f.operations[use]['target'],
                'change':change,'observe':use,'change_path':cpid,
                'property_identity':prop['id'],'semantic_version':prop['semantic_version'],
                'property_validated':True,'same_request':True,'role_origins':origins,
                'use_only_for_exclusion':True,'positive_result_usable':False,
                'initial_prefix_policy':'constructor_only_for_explicit_prefix',
                'all_source_use_paths':[pid for pid,_ in paths],
                'proof_required':'persistent_source_invariants_overapproximation',
                'another_use_or_controller_not_excluded':True}
            q=b._query(e,z.And(base,z.Or(*before),z.Not(z.Or(*after))),
                'control_transition_preservation',detail)
            queries.append(q)
            if not q.get('exclusion_certificate',{}).get('excludes_only_this_formula'):
                return False,queries
        except Unsupported:
            return False,queries
    return bool(qualified_changes),queries


def compare(b, change, use, context):
    f = b.f
    prop = context['compiled_property']
    rows, queries, worlds, gaps = [], [], [], []
    globally_excluded_paths=set()
    target = f.operations[use]['target']
    if f.operations[change]['target'] != target:
        raise Unsupported('cross_storage_context_without_binding')
    controls = [w['path'] for _, p in b.paths(change) for w in p['writes']
                if not unit_origin(b,change,w['path'])]
    relevant = [r for r in b.graph.request_reads(use) if any(
        selector_relation(r, c) == 'same_shape' for c in controls)]
    if not relevant and b.complete(change) and b.complete(use):
        return {'kind': 'causal_compare', 'change': change, 'observe': use,
                'observed_measure': 'financial_block', 'property_identity': prop['id'],
                'queries': [], 'local_errors': [], 'property_excluded': True,
                'scope_supported': False, 'financial_scope': {'reason': 'no_control_dependency_on_this_use'}}
    qualified_changes=[(pid,p)for pid,p in b.paths(change)if path_qualification(f,change,p)]
    if not qualified_changes:
        # Prefixes cannot manufacture a missing source qualification. This
        # stops an inapplicable query, not the still-open category obligation.
        return {'kind':'causal_compare','change':change,'observe':use,
                'observed_measure':'financial_block','property_identity':prop['id'],
                'queries':[],'worlds':[],'property_measurements':[],
                'local_errors':[{'reason':'intervention_has_no_source_bound_privileged_path',
                                 'operation':change,'not_a_negative_certificate':True}],
                'property_excluded':False,'scope_supported':False,
                'financial_scope':{'reason':'privilege_prerequisite_unresolved_or_not_applicable',
                                   'declared_use':use,'controls':relevant}}
    all_use_paths = list(b.paths(use))
    # Prefix search can satisfy guards, but cannot add an absent debit/credit
    # expression to a selected source path. Avoid spending the entire budget
    # preparing an entry whose modeled paths cannot realize this request (for
    # example ticket creation). Incomplete source remains an open dependency;
    # only a complete use receives this local, same-use exclusion.
    productive_candidates = []
    for pid, path in all_use_paths:
        moves = movements(b, use, path)
        if any(unit_origin(b, use, debit) and not native_only_position(b, use, debit)
               and selector_relation(debit, credit) == 'same_shape' and key(debit) != key(credit)
               for debit in moves['-'] for credit in moves['+']):
            productive_candidates.append(pid)
    if not productive_candidates:
        complete_use = b.complete(use)
        return {'kind':'causal_compare','change':change,'observe':use,
                'observed_measure':'financial_block','property_identity':prop['id'],
                'queries':[],'worlds':[],'property_measurements':[],
                'local_errors':[] if complete_use else [{
                    'reason':'no_supported_productive_baseline_path',
                    'operation':use,'unmodeled_continuations_remain_open':True}],
                'property_excluded':complete_use,'scope_supported':False,
                'financial_scope':{'reason':'selected_use_has_no_source_productive_transfer_candidate',
                    'declared_use':use,'productive_paths':[], 'complete':complete_use,
                    'prefix_search_cannot_create_a_missing_source_effect':True}}
    preserved,preservation_queries=preserved_by_source_transition(b,change,use,prop,qualified_changes)
    queries.extend(preservation_queries)
    if preserved:
        return {'kind':'causal_compare','change':change,'observe':use,
                'observed_measure':'financial_block','property_identity':prop['id'],
                'queries':queries,'worlds':[],'property_measurements':[],
                'local_errors':[],'property_excluded':True,'scope_supported':False,
                'financial_scope':{'reason':'source_transition_preserves_every_productive_input',
                    'declared_use':use,'all_change_paths':[pid for pid,_ in qualified_changes],
                    'positive_initial_domain_unchanged':True,
                    'other_controllers_or_uses_not_excluded':True}}
    from .goal_search import TargetSearch
    target_search = TargetSearch(b, use, {'measure':'productive_request', 'category':prop['category']})
    prefixes = []
    primary_families = {key(c['family']) for r in f.summaries.rows(use) for c in r['numeric_effects']
                        if c['holder'] is not None and 'debit' in c['may_directions']}
    alternatives = [o for o, entry in f.operations.items() if o != use and entry['target'] == target and
                    (any(key(c['family']) in primary_families and 'debit' in c['may_directions']
                        for r in f.summaries.rows(o) for c in r['numeric_effects']) or
                     any(c['operation']==o and c['mode']=='DELEGATECALL' and c['unresolved_implementation']
                         for c in f.call_summaries.rows.values()))]
    exact = b.complete(use) and all(b.complete(o) for o in alternatives)
    complete = all(continuation_frontier_covered(b,o) for o in [use]+alternatives)
    approximation_records=[]
    unrefined_unconditional=[]
    for reached_state in target_search:
        prefix = tuple(reached_state['prefix'])
        prefixes.append(prefix)
        # The exact checked frame sequence is reused. No writer re-enumeration.
        for chosen in [reached_state['frames']]:
            for cpid, cp in qualified_changes:
                b.check()
                role = path_qualification(f, change, cp)
                if not role:
                    continue
                try:
                    e = MechanismEncoder(f.lookup(use))
                    z = e.z
                    writes, premises, prefix_frames = [], [], []
                    for pf in chosen:
                        premises.append(encode_frame(e,pf))
                        premises.append(e.expr(pf['caller']) != 0)
                        writes += pf['writes']
                        prefix_frames.append(pf)
                    if key(writes) != key(reached_state['writes']):
                        raise Unsupported('goal_state_handoff_changed_ordered_writes')
                    cf = frame(f, change, cpid, len(prefix), writes)
                    roles, origins = fixed_role_terms(e, role, len(prefix))
                    from .behavior import ordered_clocks
                    base = z.And(*premises, encode_frame(e, cf), *roles, e.expr(cf['caller']) != 0,
                                 *ordered_clocks(e,len(prefix)+1))
                    before, after, request_objects, request_holders = [], [], [], []
                    local_approximations=[]
                    request = None
                    slot = len(prefix) + 1
                    for pid, p in all_use_paths:
                        b.check()
                        deps = b.condition_dependencies(use, pid, p)
                        if deps['unknown_dependencies'] or deps['credential_dependencies']:
                            continue
                        a = frame(f, use, pid, slot, writes)
                        c = frame(f, use, pid, slot, writes + cf['writes'])
                        usable0, cells = productive(b, e, a, use)
                        usable1, _ = productive(b, e, c, use)
                        request_objects += cells
                        request_holders += [flow(e, f.lookup(use), a, cell)[0] for cell in cells]
                        request = request or request_terms(b, e, a, use)
                        before.append(usable0)
                        after.append(usable1)
                    exact_primary={pid for pid,p in all_use_paths if not (
                        b.condition_dependencies(use,pid,p)['unknown_dependencies'] or b.condition_dependencies(use,pid,p)['credential_dependencies'])}
                    for pid,p in f.operation_paths(use):
                        if p['flow']=='reverted' or pid in exact_primary:continue
                        value,rec=may_continue(b,e,use,pid,writes+cf['writes'],slot,primary=True)
                        after.append(value);local_approximations.append(rec)
                        if z.is_true(z.simplify(value)):unrefined_unconditional.append(rec)
                    # A targeted outgoing restriction must address the actual
                    # debited holder, never only the recipient's address.
                    controlled_holders = []
                    for cell in [w['path'] for w in cf['writes']
                                 if any(selector_relation(w['path'], c) == 'same_shape' for c in relevant)]:
                        ks = keys(cell)
                        if len(ks) == 1:
                            controlled_holders.append(e.expr(ks[0]))
                    holder_matches = [h == c for h in request_holders for c in controlled_holders]
                    if prop['category'] == 'FCR-FREEZE':
                        if not holder_matches:
                            gaps.append({'path':cpid,'reason':'controlled_outgoing_holder_scope_unresolved',
                                         'controls':relevant,'request_objects':request_objects})
                            complete=False
                            continue
                        base = z.And(base, z.Or(*holder_matches))
                    if request_holders:
                        base = z.And(base, z.Or(*[h != e.expr(cf['caller']) for h in request_holders]))
                    alternate_rows = []
                    for other in alternatives:
                        known={pid for pid,_ in b.paths(other)}
                        for apid, ap in f.operation_paths(other):
                            b.check()
                            if ap['flow']=='reverted':continue
                            if path_qualification(f,other,ap):continue
                            # An incomplete *entry* can still contain an exact
                            # terminal path with no state/effect at all (for
                            # example a batch call with an empty array). That
                            # path cannot realize a positive request. Keeping
                            # it as an opaque continuation would invent a
                            # permanent possible bypass of every restriction.
                            # This exclusion is path-local; unresolved sibling
                            # loops, calls and delegated writes stay below.
                            no_effect = (apid in known and not ap.get('issues') and
                                not ap.get('evaluation_gaps') and not ap['writes'] and
                                not ap.get('sensitive_effects') and not any(
                                    b.condition_dependencies(other,apid,ap)[kind]
                                    for kind in ('unknown_dependencies','credential_dependencies')))
                            if no_effect:
                                value,error=z.BoolVal(False),'exact_terminal_path_without_productive_effect'
                            elif request is None:
                                value, error = None, 'primary_typed_request_mapping_ambiguous'
                            elif apid in known and b.complete(other):
                                value, error = alternate_continuation(b, e, other, apid, writes + cf['writes'],
                                                                      request, slot + 10)
                            else:
                                # Start incomplete entries with their necessary
                                # guard summary. Expanding a bounded loop body
                                # cannot close its unexpanded continuation, and
                                # can create exponentially repeated write terms.
                                # The overapproximation may prove no bypass; it
                                # can never prove a bypass or a negative verdict.
                                value,error=None,'source_continuation_requires_guard_overapproximation'
                            alternate_rows.append({'operation': other, 'path': apid, 'mapping': error or 'source_typed_same_request'})
                            if value is not None:
                                after.append(value)
                            elif error != 'privileged_assistance_is_not_an_ordinary_bypass':
                                value,rec=may_continue(b,e,other,apid,writes+cf['writes'],slot+10,request)
                                after.append(value);local_approximations.append(rec)
                                if z.is_true(z.simplify(value)):unrefined_unconditional.append(rec)
                    approximation_records += local_approximations
                    detail = {'operation': change, 'target': target, 'change': change, 'observe': use,
                              'change_path': cpid, 'prefix': list(prefix), 'property_identity': prop['id'],
                              'semantic_version': prop['semantic_version'], 'property_validated': True,
                              'same_request': True, 'objects': request_objects, 'controls': relevant,
                              'prefix_state_handoff': {'writes': writes, 'frames': prefix_frames,
                                  'reached_state':reached_state['id'], 'baseline_probe':reached_state['baseline_probe'],
                                  'exact_ordered_frame_reuse':True},
                              'alternative_request_mappings': alternate_rows,
                              'role_origins': origins, 'all_productive_paths_checked': complete,
                              'continuation_approximations':local_approximations,
                              'all_continuations_exact':exact and not local_approximations}
                    detail['initial_prefix_policy'] = 'constructor_only_for_explicit_prefix'
                    baseline = b._query(e, z.And(base, z.Or(*before)), 'baseline_usable', detail)
                    queries.append(baseline)
                    if not baseline['validated_bounded_witness']:
                        if not prefix and baseline.get('exclusion_certificate',{}).get('excludes_only_this_formula'):
                            globally_excluded_paths.add(cpid)
                        continue
                    # The productive before/after formulas share source inputs
                    # and state variables. No existential external failure is
                    # allowed to stand in for exclusion of successful routes.
                    if complete:
                        actual_after = z.Or(*after)
                        # One over-limit request does not establish FREEZE or
                        # PAUSE while a positive amount of the same holder's
                        # same resource remains usable. Keep the original
                        # request comparison as a mechanism observation and
                        # use this stronger range check for main classification.
                        if request is not None:
                            quantity = z.Int('remaining_positive_quantity_'+str(len(queries)))
                            actual_after = z.Exists([quantity], z.And(quantity>0, quantity<2**256,
                                z.substitute(actual_after,(request['amount'],quantity))))
                            detail['main_scope_range_check'] = 'same holder, resource, recipient and authority; any legal positive amount'
                        q = b._query(e, z.And(base, z.Or(*before), z.Not(actual_after)),
                                     'financial_block', detail)
                        queries.append(q)
                        if not prefix and exact and not local_approximations and q.get('exclusion_certificate',{}).get('excludes_only_this_formula'):
                            globally_excluded_paths.add(cpid)
                        rows.append({'baseline_probe': baseline['id'], 'block_probe': q['id'],
                                     'result': q['answer'], 'prefix': list(prefix)})
                        worlds.append({'prefix': [serialize_world(x, 'COMMON_PREFIX') for x in prefix_frames],
                                       'intervention': serialize_world(cf, 'INTERVENTION'),
                                       'same_request_slot': slot, 'actual_prefix_writes': writes})
                        if q['validated_bounded_witness']:
                            break
                except Unsupported as error:
                    gaps.append({'prefix': list(prefix), 'reason': str(error)})
            if any(q['label'] == 'financial_block' and q['validated_bounded_witness'] for q in queries):
                break
        if any(q['label'] == 'financial_block' and q['validated_bounded_witness'] for q in queries):
            break
        if unrefined_unconditional:
            # Changing the prefix cannot refine missing code/guard semantics
            # represented by True. Retain the concrete dependency/frontier;
            # do not spend the remaining budget replaying it or call it safe.
            target_search.record['stopped_on_unresolved_continuation']=unrefined_unconditional
            gaps.append({'reason':'unrefined_continuation_has_no_excluding_source_guard',
                         'continuations':unrefined_unconditional,'not_a_bypass_witness':True})
            break
        necessary={pid for pid,p in b.paths(change) if path_qualification(f,change,p)}
        if not prefix and necessary and necessary<=globally_excluded_paths and exact and b.complete(change):
            target_search.record['stopped_by_source_invariant_exclusion']=sorted(globally_excluded_paths)
            break
    # Collective scope needs a source-parametric common control. A mapped
    # per-person control remains a local restriction, regardless of two models.
    def common_guard(guard):
        roots = {c['root'] for c in relevant if not keys(c)}
        terms = list(guard.get('args', [])) if guard.get('op') in ('and', '&&') else [guard]
        return any(any(c['root'] in roots and not keys(c) for c in selectors(t)) and
                   not any(v.get('kind') in ('actual_sender','parameter') or
                           v.get('kind') == 'storage' and keys(v) for v in walk(t)) for t in terms)
    # No-effect return branches do not provide a productive escape route.
    productive_source_paths=[p for _,p in all_use_paths if movements(b,use,p)['-'] and movements(b,use,p)['+']]
    collective = bool(relevant) and bool(productive_source_paths) and all(
        any(common_guard(g) for g in p['guards']) for p in productive_source_paths)
    scope_supported = complete and (prop['category'] != 'FCR-PAUSE' or collective)
    necessary={pid for pid,p in b.paths(change) if path_qualification(f,change,p)}
    excluded=bool(necessary) and necessary<=globally_excluded_paths and exact and b.complete(change)
    return {'kind': 'causal_compare', 'observed_measure': 'financial_block',
            'property_identity': prop['id'], 'change': change, 'observe': use,
            'queries': queries, 'worlds': worlds, 'comparisons': [], 'property_measurements': rows,
            'local_errors': gaps, 'scope_supported': scope_supported, 'alternative_uses': [],
            'property_excluded':excluded,
            'source_invariant_excluded_intervention_paths':sorted(globally_excluded_paths),
            'holder_consent_counterexamples': [], 'net_measurements': [],
            'target_state_search':target_search.record,
            'continuation_approximations':approximation_records,
            'financial_scope': {'target': target, 'declared_use': use, 'controls': relevant,
                                'productive_paths': [p for p, _ in all_use_paths], 'complete': complete,
                                'collective_source_control': collective, 'prefixes_tried': [list(x) for x in prefixes]}}

````

## source/src/pr_next_joint/investigation/call_summary.py

原文件 SHA-256 `c3f55b3d1d3b20eb94b9564ac3902eeac5f271226e87465c3522b9b36e40f5b9`

````python
"""Finite call-site effects and a checked monotone callback influence closure."""
import copy
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import walk, key
from pr_next_joint.frontend.storage import selectors


class CallSummaries:
    def __init__(self, facts):
        self.f = facts
        self.rows = {}
        self.events = []
        self.refinements = {}
        direct = {}
        edges = {}
        for oid, operation in facts.operations.items():
            direct[oid] = {w['raw']['path']['root'] for w in facts.writes.values() if w['operation'] == oid}
            if any(e['raw'].get('kind') in ('native_transfer','native_selfdestruct')
                   for e in facts.effects.values() if e['operation'] == oid):
                direct[oid].add(-1)  # separate abstract native-asset location
            edges[oid] = set()
            lookup = facts.lookup(oid)
            for pid, path in facts.operation_paths(oid):
                # The original paths already include resolved internal helpers.
                calls = {x.get('source', {}).get('ast_id'): x for x in path.get('issues', [])
                         if x.get('source', {}).get('ast_id') is not None}
                for call in path.get('read_calls', []):
                    calls.setdefault(call.get('source', {}).get('ast_id'), call)
                for call in path.get('resolved_calls', []):
                    calls.setdefault(call.get('source', {}).get('ast_id'), call)
                for effect in path.get('sensitive_effects', []):
                    calls.setdefault(effect.get('source', {}).get('ast_id'), effect)
                for site, record in calls.items():
                    # SELFDESTRUCT transfers the native balance without
                    # invoking beneficiary code. It is an effect, not a CALL
                    # site with possible callbacks or a callee failure value.
                    if record.get('kind')=='native_selfdestruct':
                        continue
                    node = lookup.nodes.get(site, {})
                    assembly = node.get('nodeType') == 'InlineAssembly' and record.get('call_mode') == 'DELEGATECALL'
                    if node.get('nodeType') != 'FunctionCall' and not assembly:
                        continue
                    expr = node.get('expression', {})
                    member = expr.get('memberName')
                    declaration = lookup.nodes.get(expr.get('referencedDeclaration'), {})
                    if not assembly and expr.get('nodeType') != 'MemberAccess' and record.get('kind') not in ('dangerous_external_call','native_transfer','native_selfdestruct'):
                        # Array construction, local arithmetic and internal
                        # helper failures are not external CALL instructions.
                        continue
                    typ = expr.get('typeDescriptions', {}).get('typeIdentifier', '')
                    if (declaration.get('nodeType') == 'FunctionDefinition' and
                            't_function_internal' in typ):
                        continue
                    mutability = declaration.get('stateMutability')
                    mode = ('DELEGATECALL' if assembly or record.get('call_mode')=='DELEGATECALL' or member in ('delegatecall', 'callcode') else
                            'STATICCALL' if member == 'staticcall' or mutability in ('view', 'pure') else 'CALL')
                    resolved_read = 'return_value' in record and record.get('binding') is not None
                    # Source byte intervals determine which writes precede the
                    # call, not the destination name or a model's category.
                    location = lookup.anchor(node)
                    before = record.get('callpoint_writes')
                    if before is None:
                        before = [w for w in path.get('writes', []) if
                              w.get('source', {}).get('file') == location.get('file') and
                              w.get('source', {}).get('start', 0) + w.get('source', {}).get('length', 0) <= location.get('start', 0)]
                    callbacks = [] if mode == 'STATICCALL' or resolved_read else [
                        other for other, entry in facts.operations.items()
                        if entry['target'] == operation['target'] and not entry.get('generated_getter')]
                    edges[oid].update(callbacks)
                    token = digest([operation['target'], pid, site, mode])
                    self.rows[token] = {
                        'id': token, 'operation': oid, 'path': pid, 'source': location, 'mode': mode,
                        'code_target': copy.deepcopy(expr.get('expression')),
                        'receiver_term':copy.deepcopy(record.get('receiver_term') or record.get('recipient')),
                        'storage_context': operation['target'] if mode == 'DELEGATECALL' else 'callee_separate',
                        'caller_relation': 'first callback sender equals actual callee; subsequent external callees are distinct source frames',
                        'callpoint_writes': before, 'callback_candidates': callbacks,
                        'callpoint_guards': copy.deepcopy(record.get('callpoint_guards', [])),
                        'callpoint_evaluations': copy.deepcopy(record.get('callpoint_evaluations', [])),
                        'callpoint_exact': 'callpoint_writes' in record,
                        'argument_sources': copy.deepcopy(node.get('arguments', [])),
                        'return_used': bool(any(x.get('reason') == record.get('reason') for x in path.get('issues', []))),
                        'exit_modes': ['callee_success', 'callee_revert'],
                        'outer_exit': path.get('flow'),
                        'catch_semantics': 'callee failure returns a value; outer source guard decides commit' if member in
                            ('call', 'send', 'delegatecall', 'callcode', 'staticcall') else
                            'high-level call failure propagates unless the source catches it',
                        'unresolved_implementation': not resolved_read,
                        'residuals': ([] if resolved_read else
                                      [{'kind': 'same_storage_unknown_implementation'}] if mode == 'DELEGATECALL'
                                      else [{'kind': 'external_return_or_exit', 'source': location}]),
                        'resolved_read_binding':record.get('binding') if resolved_read else None,
                        'conditional_code_binding':bool(resolved_read and record.get('binding')=='conditional_compiled_concrete_type')
                    }
        effects = {o: set(v) for o, v in direct.items()}
        rounds = 0
        while True:
            nxt = {o: set(effects[o]).union(*(effects[c] for c in edges[o])) for o in effects}
            rounds += 1
            self.events.append({'round': rounds, 'added': {o: sorted(nxt[o] - effects[o]) for o in effects if nxt[o] != effects[o]}})
            if nxt == effects:
                # This extra transfer is the actual post-fixed point check.
                verify = {o: set(nxt[o]).union(*(nxt[c] for c in edges[o])) for o in nxt}
                assert verify == nxt
                break
            effects = nxt
        self.effects = effects
        self.direct = direct
        self.rounds = rounds
        self.identity = digest([self.rows, {o: sorted(s) for o, s in effects.items()}])
        for row in self.rows.values():
            row['may_callback_writes'] = sorted(set().union(*(effects[o] for o in row['callback_candidates'])))
            row['fixed_point_transfer_verified'] = True
            # Possible callback paths keep their original source qualifications.
            row['callback_paths'] = [
                {'operation': o, 'path': pid, 'source_effect_sha256': digest([p['guards'],p['writes'],p['flow']]),
                 'source': 'effect_summaries.paths.' + pid, 'flow': p['flow']}
                for o in row['callback_candidates'] for pid, p in facts.operation_paths(o)]

    def dependencies(self, oid, roots):
        roots = set(roots)
        out = []
        for row in self.rows.values():
            if row['operation'] != oid:
                continue
            relevant = row['mode'] == 'DELEGATECALL' or bool(roots.intersection(row['may_callback_writes']))
            out.append({'summary': row['id'], 'mode': row['mode'], 'relevant_callback_effect': relevant,
                        'matched_roots': sorted(roots.intersection(row['may_callback_writes'])),
                        'return_and_rollback_residuals': copy.deepcopy(row['residuals']),
                        'cannot_discharge_return_dependency_from_storage_independence': True})
        return out

    def refine(self, backend, oid, pid, roots):
        """Refine a finite may-effect closure at the *actual* invocation state.

        These are feasibility overapproximations, not attack witnesses. Unknown
        receivers allow later intermediary callers; they are never silently
        equated to the original user. UNSAT is consumed only with a source
        invariant/complete-domain certificate, and unresolved exits stay open.
        """
        from pr_next_joint.verification.program_encoding import MechanismEncoder
        from pr_next_joint.verification.sequence import qualify
        from pr_next_joint.verification.sequence import read
        from pr_next_joint.verification.source_worlds import frame, encode_frame
        from pr_next_joint.verification.expressions import Unsupported
        roots = set(roots)
        token = digest([self.identity, oid, pid, sorted(roots)])
        if token in self.refinements:
            return copy.deepcopy(dict(self.refinements[token], reused=True))
        f = self.f
        result = {'id': token, 'operation': oid, 'path': pid, 'roots': sorted(roots),
                  'calls': [], 'queries': [], 'may_effect_only': True, 'reused': False}
        for row in self.rows.values():
            if row['operation'] != oid or row['path'] != pid:
                continue
            backend.check()
            affected = roots.intersection(row['may_callback_writes'])
            item = {'summary': row['id'], 'mode': row['mode'],
                    'roots': sorted(affected), 'callbacks': [],
                    'return_exit_residuals': copy.deepcopy(row['residuals']),
                    'same_storage_unresolved': row['mode'] == 'DELEGATECALL' and row['unresolved_implementation']}
            result['calls'].append(item)
            if not affected:
                item['callback_projection'] = 'disjoint_after_checked_fixed_point'
                continue
            if not row['callpoint_exact']:
                item['callback_projection'] = 'source_callpoint_not_precisely_lowered'
                continue
            before = [qualify(w, 0) for w in row['callpoint_writes']]
            for candidate in row['callback_candidates']:
                if not roots.intersection(self.direct[candidate]):
                    continue
                for cpid, path in f.operation_paths(candidate):
                    backend.check()
                    rec = {'operation': candidate, 'path': cpid, 'flow': path['flow']}
                    item['callbacks'].append(rec)
                    if path['flow'] == 'reverted':
                        rec['state'] = 'callback_writes_rolled_back'
                        continue
                    if path.get('issues') or path.get('evaluation_gaps') or path['flow'] not in ('normal', 'returned'):
                        rec['state'] = 'may_influence_with_precise_path_residual'
                        continue
                    try:
                        e = MechanismEncoder(f.lookup(candidate)); z = e.z
                        cf = frame(f, candidate, cpid, 1, before)
                        prefix = [e.expr(qualify(g, 0)) for g in row['callpoint_guards']]
                        # No assertion about an unknown external return is
                        # needed to overapproximate the possible callback.
                        actor = e.expr(cf['caller'])
                        changes = [e.expr(read(w['path'],before+cf['writes'],e.lookup)) !=
                                   e.expr(read(w['path'],before,e.lookup)) for w in cf['writes']
                                   if w['path']['root'] in roots]
                        if -1 in roots:
                            changes += [e.expr(fx['amount'])>0 for fx in cf['effects']
                                        if fx.get('amount') is not None]
                        formula = z.And(*prefix, encode_frame(e, cf), actor != 0, z.Or(*changes))
                        details = {'operation': oid, 'callsite': row['source'], 'callback': candidate,
                                   'use_path': cpid, 'callpoint_writes': before,
                                   'callback_caller': 'arbitrary onward caller overapproximation; first hop checked separately',
                                   'roots': sorted(affected), 'only_may_feasibility': True,
                                   'actual_net_change_required':True,
                                   'property_validated': False}
                        receiver=row.get('receiver_term')
                        if receiver:
                            direct_formula=z.And(formula,actor==e.expr(read(qualify(receiver,0),before,e.lookup)))
                            direct_query=backend._query(e,direct_formula,'direct_callback_influence',dict(details,
                                callback_caller='exact callee address at callpoint',receiver=receiver))
                            result['queries'].append(direct_query)
                            rec['direct_callee_probe']=direct_query['id']
                        query = backend._query(e, formula, 'callback_influence', details)
                        result['queries'].append(query)
                        rec['probe'] = query['id']
                        excluded = query['answer'] == 'unsat' and (
                            query.get('exclusion_certificate', {}).get('excludes_only_this_formula') or
                            query.get('details', {}).get('prestate', {}).get('global_reachability_exhausted'))
                        rec['state'] = 'source_invariant_excludes_callback' if excluded else 'may_influence'
                        rec['midstate_and_guard_formula'] = query['formula_ref']
                    except Unsupported as error:
                        rec['state'] = 'may_influence_with_precise_path_residual'
                        rec['reason'] = str(error)
            records = item['callbacks']
            item['callback_projection'] = ('excluded_on_all_overapproximated_entries' if records and
                all(r['state'] in ('callback_writes_rolled_back', 'source_invariant_excludes_callback') for r in records)
                else 'may_influence')
            # This final projection check preserves every transitive may-root
            # unless all its real source callbacks were actually excluded.
            item['projected_roots'] = [] if item['callback_projection'].startswith('excluded_') else sorted(affected)
        self.refinements[token] = copy.deepcopy(result)
        return result

    def record(self):
        return {'identity': self.identity, 'calls': self.rows, 'rounds': self.rounds,
                'propagation': self.events, 'transfer_verified': True,
                'refinements': self.refinements,
                'precision': 'finite may-effect union; path feasibility and unknown external exits remain separate'}

````

## source/src/pr_next_joint/investigation/candidates.py

原文件 SHA-256 `b7ff47569a4908d9d5e5868908c684c4fcc9934a65623b1f05f7193bc168039f`

````python
"""Small source-located questions about applied extra effects and independent exits."""
from pr_next_joint.frontend.path_ir import walk, key
from pr_next_joint.frontend.storage import selectors
from pr_next_joint.core import digest


def source_candidates(facts):
    result=[]
    for oid,op in sorted(facts.operations.items(),key=lambda x:(x[1]['target'],x[1]['source']['start'],x[0])):
        if op.get('generated_getter'):continue
        lookup=facts.lookup(oid);fn=lookup.function(op['function']);origin=fn.get('scope')
        bases=lookup.nodes.get(origin,{}).get('linearizedBaseContracts',[])[1:]
        peers=[n for c in bases for n in lookup.nodes[c].get('nodes',[]) if n.get('nodeType')=='FunctionDefinition'
               and n.get('scope')!=origin and n.get('body') and n.get('name')==fn.get('name') and fn.get('name')
               and len(n.get('parameters',{}).get('parameters',[]))==len(fn.get('parameters',{}).get('parameters',[]))]
        parent_roots={x.get('referencedDeclaration') for p in peers for n in walk(p.get('body') or {})
            if n.get('nodeType')=='Assignment' for x in walk(n.get('leftHandSide') or {})}
        extra=[];exits=[]
        span=lookup.anchor(fn)
        for pid,p in facts.operation_paths(oid,True):
            for w in p['writes']:
                loc=w['source']
                if peers and loc['file']==span['file'] and span['start']<=loc['start']<span['start']+span['length'] and w['path']['root'] not in parent_roots:
                    extra.append({'path':pid,'position':w['path'],'value':w['value'],'source':loc})
            for effect in p.get('sensitive_effects',[]):
                if 'selfdestruct' in str(effect.get('kind','')) or 'selfdestruct' in str(effect.get('operation','')):
                    exits.append({'path':pid,'effect':effect})
        # Actual source effects use a typed `selfdestruct` kind in this frontend.
        if extra or exits:
            row={'operation':oid,'target':op['target'],'kind':'applied_extra_effect' if extra else 'independent_sensitive_exit',
                 'extra_effects':list({key(x):x for x in extra}.values()),'sensitive_exits':exits,
                 'candidate_requires_assessment':True,'not_counterevidence':True}
            row['id']='candidate_'+digest(row)[:16];result.append(row)
    return result


def investigate(inv):
    inv.candidate_trace=[]
    for candidate in inv.f.source_candidates:
        oid=candidate['operation'];existing=[q for q in inv.issues.values() if inv.root(q)==oid]
        if existing:
            q=existing[0];q['host_source_candidate']=candidate
            inv.enqueue(q['id'],'inspect',{'operation':oid,'enhance':False},1,'inspect applied extra effect against the existing explanation')
        else:
            item={'id':'host_'+candidate['id'],'anchors':[inv.catalog.name(oid)],'assessment':'investigate',
                  'category':'AC' if inv.f.options.scope=='AC' else 'ADDITIONAL',
                  'claim':'The actual applied entry has a committed '+candidate['kind']+'. Determine the affected subject, authorization and asset, and whether the existing explanation covers this effect.',
                  '_host_source_question':True}
            inv.accept({'issues':[item],'reviewed':[],'diagnostics':[],'usable_analysis':True},host_target=candidate['target'])
            q=inv.issues.get(item['id'])
            if q:q['host_source_candidate']=candidate
        inv.candidate_trace.append({**candidate,'question':q['id'] if q else None,
            'state':'queued' if q else 'unresolved_binding','generated_risk_claim':False})


def investigate_obligations(inv,report):
    """Give omitted semantic obligations a place in the existing follow-up.

    No extra session, risk label or gold-driven ordering. Shared object groups
    send one source question; unselected entries remain in the coverage ledger.
    """
    scope=report['task_analysis']['reading_scope'];created=[]
    for group in sorted(scope.get('obligations',[]),key=lambda g:(g['target'],g['id'])):
        if group['closed']:continue
        entries=[e['operation'] for e in group['entry_states'] if any(s=='open' for s in e['states'].values())]
        unclaimed=[o for o in entries if not any(inv.root(q)==o for q in inv.issues.values())]
        if not unclaimed:continue
        # Source-only getters/residual bodies without a locatable effect need
        # source recovery, not a fabricated semantic question about an asset.
        useful=[o for o in unclaimed if any(r['ordered_writes'] or r['effects'] for r in inv.f.summaries.rows(o))]
        if not useful:continue
        oid=min(useful,key=lambda o:(inv.f.operations[o]['source']['start'],o))
        item={'id':'obligation_question_'+digest([group['id'],oid])[:16],
            'anchors':[inv.catalog.name(oid)],'assessment':'investigate',
            'category':'AC' if inv.f.options.scope=='AC' else None,
            'claim':'This committed source effect remains an open analysis obligation. Explain the affected right or counter and applicable authorization, including a normal business qualification if present.',
            '_host_source_question':True}
        inv.accept({'issues':[item],'reviewed':[],'diagnostics':[],'usable_analysis':True},host_target=group['target'])
        q=inv.issues.get(item['id'])
        if not q:continue
        q['host_obligation_question']={'obligation':group['id'],'operations':entries,'selected_operation':oid,
            'other_entries_not_marked_complete':True,'shared_existing_session':True}
        created.append(q['id'])
        inv.candidate_trace.append({'operation':oid,'target':group['target'],'question':q['id'],
            'kind':'unresolved_source_obligation','obligation':group['id'],'state':'queued',
            'generated_risk_claim':False,'other_unclaimed_entries':sorted(set(entries)-{oid})})
    return created

````

## source/src/pr_next_joint/investigation/cli.py

原文件 SHA-256 `febabd2e9140ea40067e6ca0a2550acfcd044420d264c4f4162827a99733e994`

````python
"""Original compiled source -> source-led semantic investigation (offline stage two)."""
import argparse,json,hashlib,threading,time,traceback,sys
from pathlib import Path
from contextlib import nullcontext
from .contracts import Options,VERSION,write
from .program import Facts
from .graph import ProgramGraph
from .context import Catalog,SourceContext
from .engine import analyze
from .report import evaluation_projection

def load_program(root,unit,task,config=None,targets=None,engineering=None):
    options=Options(scope=task,**(config or {}))
    if engineering:
        d=Path(engineering);bundle=json.loads((d/'ProgramBundle.json').read_bytes());native=json.loads((d/'native_ssa.json').read_bytes())
        texts={p.relative_to(d/'sources').as_posix():p.read_text(encoding='utf-8-sig') for p in (d/'sources').rglob('*.sol')}
        sources=[{'file':n,'content':s,'sha256':hashlib.sha256(s.encode()).hexdigest()} for n,s in texts.items()]
        receipt={'engineering_fixture':True,'compiler_artifacts_reused':True,'compiler_invocations':0,'native_extractions':0}
        f=Facts(bundle,native,sources,options,targets);return f,receipt
    from pr_next_joint.frontend.dataset_intake import load_compiled_unit
    u=load_compiled_unit(Path(root).resolve(),Path(unit).resolve())
    return Facts(u['bundle'],u['native'],u['sources'],options,targets or u['selected_targets'],u['description']),u['receipt']

def run(args,*,responses=None,client_factory=None):
    source_root=Path(__file__).resolve().parents[3];sys.path.insert(0,str(source_root/'runtime'))
    from reference_counter import Counter
    from bridge import FixtureClient,FileClient,MockBroker,UsageJournal
    out=Path(args.out).resolve();out.mkdir(parents=True,exist_ok=True)
    if any(out.iterdir()):raise ValueError('fresh_output_required')
    config=json.loads(Path(args.config).read_text(encoding='utf-8-sig')) if args.config else {}
    if config.get('live_model_authorized') or config.get('live_authorized'):raise ValueError('stage2_no_live_authorization')
    if set(config)-{'method','options','live_model_authorized','notes'}:raise ValueError('unknown_config_keys')
    f,intake=load_program(args.root,args.compiled_unit,args.task,config.get('options'),args.target,args.engineering_compiled)
    write(out/'intake_receipt.json',intake);counter=Counter(args.tokenizer)
    if args.phase=='prepare':
        graph=ProgramGraph(f);ctx=SourceContext(f,Catalog(f,graph),counter);messages,manifest=ctx.messages()
        write(out/'prepared_messages.json',{'messages':messages,'manifest':manifest,'host_identity':f.identity})
        write(out/'program_facts.json',f.context);return {'prepared_only':True,'real_model_calls':0,'manifest':manifest}
    if responses is None:responses=[Path(p).read_text(encoding='utf-8-sig') for p in (args.fixture_response,args.fixture_feedback) if p]
    if client_factory is not None:
        broker=nullcontext();client=client_factory(f,args,counter)
    elif args.offline_bridge:
        broker=MockBroker(out/'ipc',responses,args.case_id,f.identity);client=FileClient(out/'ipc',args.case_id,f.identity)
    else:broker=nullcontext();client=FixtureClient(responses,args.case_id)
    with broker:report=analyze(f,out/'analysis',counter=counter,client=client)
    if client_factory is not None:write(out/'usage_journal.json',client.accounting())
    else:
        journal=UsageJournal(out/'usage_journal.json')
        for row in report['usage']['attempts']:journal.fixture(args.case_id,row['index'],row['input_tokens'])
    write(out/'prediction_export.json',evaluation_projection(report));return report

def parser():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root');p.add_argument('--compiled-unit');p.add_argument('--engineering-compiled')
    p.add_argument('--target',action='append');p.add_argument('--task',choices=('AC','FCR'),required=True)
    p.add_argument('--out',required=True);p.add_argument('--config');p.add_argument('--tokenizer',required=True)
    p.add_argument('--fixture-response');p.add_argument('--fixture-feedback');p.add_argument('--offline-bridge',action='store_true')
    p.add_argument('--phase',choices=('prepare','analyze'),default='analyze');p.add_argument('--case-id',default='engineering')
    return p

def main(argv=None):
    args=parser().parse_args(argv);started=time.monotonic();stop=threading.Event()
    def heartbeat():
        while not stop.wait(20):print(json.dumps({'phase':'offline_engineering','elapsed_seconds':round(time.monotonic()-started),'actual_model_submissions':0}),flush=True)
    thread=threading.Thread(target=heartbeat,daemon=True);thread.start();result=1
    try:
        report=run(args);print(json.dumps({'findings':len(report.get('findings',[])),'prepared_only':report.get('prepared_only',False),'actual_model_submissions':0}),flush=True);result=0
    except Exception as error:
        out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
        write(out/('technical_error_'+str(time.time_ns())+'.json'),{'error':type(error).__name__+':'+str(error),'traceback':traceback.format_exc(),'risk_prediction_synthesized':False})
        print('工程入口停止：'+str(error),flush=True)
    finally:
        stop.set();thread.join(1);print('运行结束：'+('已保存离线工程结果' if result==0 else '入口异常，错误原件已保存')+'；实际模型调用0；目录 '+str(Path(args.out).resolve()),flush=True)
    return result

````

