"""Host-compiled properties and evidence composition, shared by Full consumers.

Model judgments are proposals. Program execution does not prove a business
policy; source-backed policy/resource interpretations remain explicit H inputs.
"""
import copy
import re
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key, walk, op
from pr_next_joint.frontend.storage import selectors, keys, selector_relation, value_type
from .summary import get_summaries, holder, unique
from .initial_state import domain, initial_for_lookup
from .roles import path_qualification


def policy_basis(item):
    from .relations import policy
    return policy(item)


def authorization_expression(inv,q,policy):
    from .relations import authorization
    return authorization(inv,q,policy)


def compile_property(inv, q):
    f = inv.f; b = inv.backend; root = inv.root(q); item = q['current']
    if root is None: return None
    from .ledger import movements, unit_origin, native_only_position
    from .key_roles import relation as key_relation
    from .comparison import transfer_shapes
    summaries = get_summaries(f); rows = summaries.rows(root)
    dependencies = summaries.dependencies.forward(root)
    target = f.operations[root]['target']
    cells = unique(c for oid in [root] for c in summaries.positions(oid)
                   if not summaries.control_only(c,target))
    bindings = [unit_origin(b, root, c) for c in cells]
    questions = []
    for c, unit in zip(cells, bindings):
        bound = inv.semantics.lookup(root, c)
        if not unit and not (bound and bound['meaning'] == 'nonfinancial_counter'):
            questions.append(inv.semantics.question(q, root, c))
    known_semantics = [u for u in bindings if u]
    possible = set(); text = item.get('claim', '')
    declared = set(q['claim_source_scope']['source_operations']) | {root}
    # An anchored control can have a real downstream financial use without a
    # second model anchor. This is a source dependency candidate, not a claim
    # expansion based on the exploratory next_check endpoint.
    control_uses=set()
    if f.options.scope=='FCR':
        written=[w['path'] for r in rows for w in r['ordered_writes']]
        for cell in written:
            if unit_origin(b,root,cell):continue
            if (key_relation(cell,f.lookup(root)) or {}).get('kind')=='authorization_quantity':continue
            for use in inv.graph.access[(target,cell['root'])]['readers']:
                if use==root:continue
                if any(selector_relation(cell,c)=='same_shape' and not inv.graph._disjoint_keys(cell,c)
                       for r in summaries.rows(use) for c in selectors(r['guards'])):
                    control_uses.add(use)
    test_uses=set()
    if f.options.scope=='FCR' and item.get('category') in ('FCR-FREEZE','FCR-PAUSE'):
        # A proposed control must be falsifiable even when the graph finds no
        # effect edge. Select an actual ordinary token-flow use, not a clock
        # setter interpreted as issuance, and never infer a different category
        # merely from an administrative number increasing or decreasing.
        candidates={}
        for use,entry in f.operations.items():
            if entry['target']!=target or use==root:continue
            for rr in summaries.rows(use):
                pp=f.paths[rr['path']]['raw']
                if path_qualification(f,use,pp):continue
                mm=movements(b,use,pp)
                for debit,credit in transfer_shapes(b,use,pp):
                    if unit_origin(b,use,debit) and not native_only_position(b,use,debit):
                        candidates.setdefault(key({'root':debit['root'],'fields':[s for s in debit.get('segments',[])if 'field'in s]}),set()).add(use)
        named={use for uses in candidates.values() for use in uses if use in declared}
        if named:test_uses=named
        elif len(candidates)==1:test_uses=next(iter(candidates.values()))
    value_uses={use for use,kinds in dependencies['uses'].items() if 'value' in kinds and summaries.positions(use)}
    property_entries=declared|control_uses|test_uses|value_uses
    # Supplemental anchors are context, not a request to change the root's object.
    cells = unique(cells + [c for use in sorted(control_uses|test_uses|value_uses) for c in summaries.positions(use)])
    bindings = [unit_origin(b, root, c) for c in cells]
    known_semantics = [u for u in bindings if u]
    native_debits=unique(e['cell'] for r in rows for e in r['numeric_effects']
        if e['holder'] is not None and 'debit' in e['may_directions'] and b._native_unit_source(root,e['cell']))
    if f.options.scope == 'AC':
        cat = 'AC'; rules=getattr(inv.semantics,'rules',None)
        policy = (rules.policy(q) if rules and item.get('_semantic_consumer') else None) or q.get('authorization_interpretation') or policy_basis(item)
        prior_policy=next((policy_basis(v) for v in reversed(q.get('history',[])) if policy_basis(v)),None)
        if policy and policy.get('meaning')=='normal_authorization' and prior_policy:
            # A normal proposal does not erase the qualification being tested.
            # It may add a source-bound business alternative to that predicate.
            policy=dict(prior_policy,normal_proposal=copy.deepcopy(policy))
        if policy is None:
            policy=prior_policy
        if policy is None:
            questions.append(inv.semantics.question(q, root, kind='authorization'))
        else:
            predicate=authorization_expression(inv,q,policy)
            if predicate:
                interpretations = [predicate]
                for alternative in q.get('authorization_alternatives', []):
                    other = authorization_expression(inv, q, alternative)
                    if other and all(key(other['predicate']) != key(x['predicate']) for x in interpretations):
                        interpretations.append(other)
                if len(interpretations) > 1:
                    # A witness must violate every still-supported policy.
                    # UNSAT for their conjunction does not refute each policy.
                    predicate = dict(predicate,
                        predicate=op('or', *[x['predicate'] for x in interpretations]),
                        competing_interpretations=interpretations,
                        competition_semantics='one behavior violates all surviving interpretations')
                policy=dict(policy,compiled_authorization=predicate)
            if predicate and not predicate.get('source_bound_alternatives'):
                from .authorization_normal import payment_qualification
                potential=payment_qualification(inv,q,predicate['subject'],require_proposal=False) if predicate.get('subject') is not None else []
                if potential:
                    question=inv.semantics.question(q,root,kind='authorization')
                    question.update(question='Does the recorded actual payment establish a lawful business qualification for acquiring this authority? Explain the source relation and any bypass.',
                        source_qualification_candidates=[{'authority':b._storage_name(root,x['holder']),
                            'recorded_payment':b._storage_name(root,x['bid']),
                            'relation':'actual payment exceeds the previous recorded payment; the same payer receives this authority',
                            'source_path':x['path'],'business_legitimacy_not_proved':True} for x in potential])
                    questions.append(question)
        possible.add(cat)
    else:
        policy = None
        for r in rows:
            # This selects a typed hypothesis from known source writes, not
            # a successful execution. A residual read must reach the actual
            # condition checker instead of erasing the hypothesis/category.
            p = f.paths[r['path']]['raw']; m = movements(b, root, p)
            # A stage counter beside a known native entitlement is not a token
            # ledger merely because both numeric fields change on this path.
            # Unknown units still receive the semantic questions above.
            m={sign:[c for c in values if unit_origin(b,root,c)] for sign,values in m.items()}
            transfers = transfer_shapes(b, root, p)
            if any(unit_origin(b,root,a) and not native_only_position(b,root,a) for a,_ in transfers): possible.add('FCR-TRANSFER')
            if any(not any(selector_relation(d, c) == 'same_shape' and key(d) != key(c)
                           for c in m['+']) and not native_only_position(b,root,d) for d in m['-']): possible.add('FCR-DESTROY')
            if any(not any(selector_relation(c, d) == 'same_shape' and key(c) != key(d)
                           for d in m['-']) and not native_only_position(b,root,c) for c in m['+']): possible.add('FCR-MINT')
        # State controls are discovered by the graph, including numeric/stage
        # guards. This selects a property; it does not assert a freeze/pause.
        for use in property_entries:
            for r in summaries.rows(use):
                if not any('debit' in e['may_directions'] and e['holder'] is not None and
                    unit_origin(b,use,e['cell']) and not native_only_position(b,use,e['cell']) for e in r['numeric_effects']): continue
                for control in inv.graph.request_reads(use):
                    if unit_origin(b,use,control):continue
                    if (key_relation(control,f.lookup(use)) or {}).get('kind')=='authorization_quantity':continue
                    if any(w['raw']['path']['root'] == control['root'] and w['operation'] in declared
                           and w['operation'] != use and path_qualification(f,w['operation'],f.paths[w['path']]['raw']) for w in f.writes.values()):
                        from .dependencies import control_candidates
                        possible.update(control_candidates(control,[e['holder'] for e in r['numeric_effects']
                            if e.get('holder') is not None and 'debit' in e['may_directions']]))
        if value_uses and any(path_qualification(f,root,f.paths[r['path']]['raw']) for r in rows):
            # An actual state-dependent transfer amount can affect value as
            # well as availability. Admission to a category still needs its
            # own source/proof record. No second class is inferred from a name.
            for use in sorted(value_uses):
                for r in summaries.rows(use):
                    units=[e for e in r['numeric_effects'] if e['holder'] is not None and unit_origin(b,use,e['cell'])
                           and not native_only_position(b,use,e['cell'])]
                    directions={d for e in units for d in e['may_directions']}
                    if 'debit' in directions:possible.add('FCR-DESTROY')
                    if {'debit','credit'}<=directions:possible.add('FCR-TRANSFER')
                    if 'credit' in directions and 'debit' not in directions:possible.add('FCR-MINT')
        if not possible and native_debits:
            possible.add('ADDITIONAL')
        hint = item.get('category')
        from .contracts import CATEGORIES
        if hint in CATEGORIES[1:]:
            cat = hint
        elif len(possible) == 1: cat = next(iter(possible))
        else:
            # Only a hint to a corresponding actual effect is usable. Ambiguous
            # tasks stay open instead of sorting effect names into a risk label.
            cat = None
        if hint == 'ADDITIONAL' and not possible: cat = 'ADDITIONAL'
    relation = {'task': f.options.scope, 'target': target, 'operation': root,'source_identity':f.identity,
        'category': cat, 'possible_categories': sorted(possible),
        'domain': domain(f.lookup(root)),
        'initial_identity': initial_for_lookup(f.lookup(root))['identity'],
        'objects': cells, 'resource_bindings': known_semantics,
        'expected_authorization': policy, 'actual_guards': [r['guards'] for r in rows],
        'source_operations': sorted(declared), 'stage': item.get('phase'),
        'source_linked_control_uses':sorted(control_uses),
        'value_dependence':{'closure':dependencies['id'],'value_uses':sorted(value_uses),
            'precision':dependencies['precision']},
        'control_use_frontier':sorted(test_uses),
        'frontier_meaning':'source token-flow uses for testing the control hypothesis; not inferred effect edges',
        'native_redemption_debits':native_debits,
        'financial_consent':copy.deepcopy(q.get('financial_consent_interpretation')),
        'claim_assumptions':copy.deepcopy(item.get('assumptions',[])),
        # An interpretation belongs to the actual downstream holder/use. A
        # control property that depends on that use must be recompiled even
        # when the wire happened to ask a separate direct-use question.
        'semantic_dependency_operations': sorted(set(q['binding']['operations'])|property_entries),
        'consent_dependency_operations': sorted(value_uses|{root}) if cat in ('FCR-TRANSFER','FCR-DESTROY') else [],
        'semantic_version': inv.semantics.dependency_identity(set(q['binding']['operations'])|property_entries,
            consent_operations=value_uses|{root} if cat in ('FCR-TRANSFER','FCR-DESTROY') else []),
        'semantic_questions': questions, 'summary_identity': summaries.identity,
        'residuals': [x for r in rows for x in r['residuals']] + [r for (t, _),r in
            getattr(b,'unit_conflicts',{}).items() if t==target and any(
                selector_relation(r['cell'],c)=='same_shape' for c in cells)],
        'kind': 'host_typed_source_property', 'model_category_hint': item.get('category'),
        'minimum_evidence': 'applicable source/semantic/program support; no universal SMT requirement'}
    if f.options.scope=='FCR':
        original=item.get('_original_model_category') or item.get('category')
        relation['original_category']=original
        relation['consent_rows']=[]
        if cat in ('FCR-TRANSFER','FCR-MINT','FCR-DESTROY'):
            relation['quantity_routes']={use:digest(summaries.dependencies.amounts_for(use)) for use in sorted(value_uses|{root})}
            relation['financial_consents']={}
            if cat in ('FCR-TRANSFER','FCR-DESTROY'):
                for use in sorted(value_uses|{root}):
                    for amounts in summaries.dependencies.amounts_for(use):
                        for gate in amounts['allowance_gates']:
                            issuer=keys(gate['grant'])[gate['issuer_key']]
                            for debit in amounts['deltas']:
                                if debit['sign']!='-' or debit.get('key_role')=='authorization_quantity' or key(debit.get('holder'))!=key(issuer):continue
                                scope={'path':amounts['path'],'grant':gate['grant'],
                                       'issuer_key':gate['issuer_key'],'spender_key':gate['spender_key'],
                                       'debit_expression':debit['amount_expression'],
                                       'checked_quantity_expression':gate['quantity_expression'],'ledger':debit['cell']}
                                interpretation=inv.semantics.lookup_consent(use,debit['cell'],scope)
                                if interpretation:
                                    if interpretation not in relation['consent_rows']:relation['consent_rows'].append(interpretation)
                                elif debit['amount_expression']!=gate['quantity_expression']:
                                    sq=inv.semantics.question(q,use,debit['cell'],kind='financial_consent',quantity_scope=scope)
                                    current=inv.semantics.questions[sq['id']]
                                    current.setdefault('quantity_scope',[])
                                    if scope not in current['quantity_scope']:current['quantity_scope'].append(scope)
                                    # One registered source entity remains identical
                                    # on the wire and at answer consumption.
                                    questions[:]=[x for x in questions if x.get('id')!=sq['id']]
                                    questions.append(copy.deepcopy(current))
        for use in sorted(value_uses|{root}):
            cs=[c for c in relation['consent_rows'] if c['operation']==use]
            if len(cs)==1:relation['financial_consents'][use]=cs[0]
        relation['category_obligations']=[{'category':category,'source_candidate':category in possible,
            'original':category==original,'operation':root,'closure':dependencies['id'],
            'validation':'requires_same_scope_evidence'} for category in
            sorted(possible | ({original} if original in CATEGORIES[1:] else set()))]
    if q.get('history') and item['claim'].strip()!=q['history'][-1]['claim'].strip():
        rootname=f.operations[root]['function'].split('(')[0]
        root_named=bool(re.search(r'(?<![\w$])'+re.escape(rootname)+r'(?![\w$])',text))
        pointed=[]
        for oid,o in f.operations.items():
            if oid==root or o['target']!=target:continue
            name=o['function'].split('(')[0]
            explicit=re.search(r'(?<![\w$])'+re.escape(name)+r'\s*\(',text) or re.search(r'`'+re.escape(name)+r'`',text)
            if re.search(r'[a-z][A-Z]',name):explicit=explicit or re.search(r'(?<![\w$])'+re.escape(name)+r'(?![\w$])',text)
            if explicit:pointed.append(oid)
        origins={key(a) for a in summaries.operations[root]['source_closure']}
        foreign=[o for o in pointed if not {key(a) for a in summaries.operations[o]['source_closure']}<=origins]
        root_role_write=any(not keys(w['path']) and value_type(w['path'],f.lookup(root)) in ('address','address payable') for r in rows for w in r['ordered_writes'])
        changed_kind=(item.get('category') not in possible and f.options.scope=='FCR' or
                      root_role_write and any(summaries.positions(o) for o in foreign) and not re.search(r'\b(?:acquir\w*|takeover|becom\w*|install\w*)\b',text,re.I))
        if foreign and not root_named and changed_kind:
            relation['core_rebinding_required']={'old_core':root,'source_named_candidates':foreign,
                'reason':'revised actual effect does not have the old core source; no old-root credit inherited'}
    # Business identity is not the consumption/cache identity. New evidence,
    # search branches and supplementary-anchor ordering do not change a policy.
    relation['claim_identity'] = digest([f.options.scope, target, root, cat,
        sorted(key(c) for c in cells), item.get('actor'), item.get('object'), item.get('phase'),
        (policy or {}).get('meaning'),((policy or {}).get('compiled_authorization') or {}).get('predicate'),
        relation.get('core_rebinding_required')])
    rules=getattr(inv.semantics,'rules',None)
    if rules:relation['scoped_semantics']=rules.signature(root)
    relation['id'] = 'property_' + digest(relation)[:20]
    return relation


def planning_item(q):
    item = copy.deepcopy(q['current']); p = q.get('property') or {}
    if p.get('category'): item['category'] = p['category']
    if p.get('category')=='AC' and (p.get('expected_authorization') or {}).get('compiled_authorization'):
        if isinstance(item.get('observation'),dict) and item['observation'].get('measure')=='denied_qualified':
            item['observation']['authorization']=p['expected_authorization']['compiled_authorization']
        else:
            item['observation']={'measure':'authorization_violation','authorization':p['expected_authorization']['compiled_authorization']}
    if p.get('category') in ('FCR-TRANSFER', 'FCR-DESTROY', 'FCR-MINT') and p.get('objects'):
        ob = item.get('observation')
        if not isinstance(ob, dict) or ob.get('measure') in (None, 'opens', 'blocks'):
            item['observation'] = {'measure': 'direct_effect'}
    return item


def _typed_assessment(inv, q):
    """One decision from typed obligations. Legacy reportable is never read."""
    prop = q.get('property')
    root = inv.root(q)
    item = q['current']
    scope = {'source_prediction': True, 'concrete_EVM': False,
             'deployment_reachability_proved': False, 'entire_contract_safety_proved': False,
             'compiled_property': copy.deepcopy(prop), 'claim_identity': (prop or {}).get('claim_identity'),
             'only_declared_operations': q['binding'].get('operations', []),
             'scoped_observations': [], 'evidence_dependencies': {}, 'semantic_task_review': q.get('task_review')}
    result = {'root': root, 'category': (prop or {}).get('category'), 'reportable': False,
              'reasons': [], 'scope': scope, 'evidence_refs': list(q['evidence'])}
    if q.get('retired_property_parent'):
        result['reasons']=['derived_obligation_replaced_by_current_parent']
        scope['route_status']='superseded'
        return result
    if not prop or not root or not q['binding'].get('core_exact', q['binding'].get('exact')):
        result['reasons'] = ['source_identity_ambiguous_or_unresolved' if root is None else 'validated_property_not_available']
        return result
    if prop.get('core_rebinding_required'):
        result['reasons'] = ['changed_business_effect_requires_source_rebinding']
        return result
    scope['expected_authorization'] = prop.get('expected_authorization')
    scope['model_original_judgment'] = {'assessment': item.get('assessment'), 'claim': item.get('claim')}
    cat = prop.get('category')
    if not cat:
        result['reasons'] = ['property_task_meaning_unresolved']
        return result
    if cat=='AC':
        from .policy_binding import audit_authorization
        checked=audit_authorization(inv.f,root,(prop.get('expected_authorization') or {}).get('compiled_authorization'))
        scope['source_ir_checks']=checked
        if any(not r['matches'] for r in checked):
            result['reasons']=['source_ir_disagreement']
            return result
    inspections = [inv.evidence[label] for label in q['evidence']
                   if inv.evidence[label].get('kind') == 'source_inspection' and inv.evidence[label].get('operation') == root]
    scope['source_deductions'] = [{'evidence': r['id'], 'no_committing_path': r.get('no_committing_path'),
                                 'net_unchanged': r.get('net_effect_proved_unchanged')} for r in inspections]
    observation = item.get('observation')
    measure = observation.get('measure') if isinstance(observation, dict) else None
    if measure != 'denied_qualified':
        reason = next(('original_root_has_no_committing_path' if r.get('no_committing_path')
                       else 'original_root_net_effect_is_unchanged' for r in inspections
                       if r.get('no_committing_path') or r.get('net_effect_proved_unchanged')), None)
        if reason:
            result['reasons'] = [reason]
            scope['route_status'] = 'excluded'
            scope['necessary_conditions'] = {'actual_effect': 'refuted_by_complete_source',
                                            'other_unknowns_decisive_for_this_route': False}
            return result
    current = [e for label in q['evidence'] for e in [inv.evidence[label]]
               if e.get('source_identity') == inv.f.identity and
               (e.get('property_validation_key') == validation_key(prop) or e.get('property_identity') == prop['id'])]
    queries = [x for e in current for x in e.get('queries', [])
               if x.get('details', {}).get('property_identity') == prop['id'] or
               e.get('property_validation_key') == validation_key(prop)]
    scope['revalidated_evidence'] = [{'evidence': e['id'], 'validation_key': e.get('property_validation_key')}
                                   for e in current]
    if inv.f.options.scope == 'AC':
        policy = prop.get('expected_authorization') or {}
        expected = policy.get('compiled_authorization')
        if not expected:
            result['reasons'] = ['expected_authorization_not_established']
            return result
        label = 'denied_qualified' if measure == 'denied_qualified' else 'authorization_violation'
        relevant = [x for x in queries if x.get('label') == label and x.get('details', {}).get('property_validated')]
        positives = [x for x in relevant if x.get('bounded_condition_confirmed')]
        source_support = [e for e in current if e.get('kind') == 'source_property_certificate' and
                          e.get('property_validated') and e.get('supports') == label]
        all_paths = {pid for pid, _ in inv.f.operation_paths(root, True)}
        excluded = {x['details'].get('use_path') for x in relevant if x.get('answer') == 'unsat'
                    and not x.get('abstract_hash') and (x.get('exclusion_certificate', {}).get('excludes_only_this_formula')
                    or x.get('details', {}).get('prestate', {}).get('global_reachability_exhausted'))}
        scope['property_support'] = [{'policy': policy, 'queries': [x['id'] for x in relevant]}]
        scope['authorization_counterevidence'] = [x['id'] for x in relevant if x.get('answer') == 'unsat']
        result['reportable'] = bool(positives or source_support)
        from .policy_binding import source_excludes_violation
        structural=source_excludes_violation(inv.f,root,expected) if label=='authorization_violation' else None
        if structural:
            scope['local_authorization_exclusion']=structural
            result['reportable']=False
            result['reasons']=['source_supported_applicable_normal_authorization']
            scope['route_status']='excluded'
            return result
        scope['source_property_certificates'] = [e['id'] for e in source_support]
        if not result['reportable']:
            subcases_complete=all(not e.get('local_errors') for e in current if e.get('observed_measure')==label)
            # A same-requester grant/use subcase cannot exclude untested
            # nominee, application or proxy continuations. A complete source
            # authorization exclusion above remains valid for all of them.
            acquire=expected.get('property_family')=='acquire'
            if acquire:scope['acquisition_actor_coverage']='checked source-bound subcases; untested control chains remain open'
            if not acquire and all_paths and all_paths <= excluded and subcases_complete and inv.backend.complete(root) and not expected.get('competing_interpretations'):
                result['reasons'] = ['expected_authorization_covers_all_applicable_paths']
                scope['route_status'] = 'excluded'
            else:
                result['reasons'] = ['authorization_violation_not_established']
        else:
            scope['positive_condition_scopes'] = [{'probe': x['id'], 'details': x['details']} for x in positives]
    else:
        relevant = [x for x in queries if x.get('details', {}).get('property_validated') and
                    x.get('label') in ('direct_effect', 'financial_block','financial_value')]
        positive = [x for x in relevant if x.get('bounded_condition_confirmed')]
        settlements=[]
        if cat=='FCR-DESTROY':
            uses={root}|set(prop.get('value_dependence',{}).get('value_uses',[]))
            for label in q['evidence']:
                ev=inv.evidence[label]
                if ev.get('kind')!='source_inspection' or ev.get('operation') not in uses or ev.get('source_identity')!=inv.f.identity:continue
                for row in ev.get('settlements',[]):
                    if row.get('same_holder_and_unit_full_settlement') and any(
                            selector_relation(row['object'],c)=='same_shape' for c in prop.get('objects',[])):
                        settlements.append(dict(row,operation=ev['operation'],evidence=label))
            scope['matched_settlement_counterevidence']=settlements
            # A complete payment on one source branch cannot refute another
            # holder, unit, path or an independent unresolved callback.
            positive=[x for x in positive if not any(
                x['details'].get('observe',x['details'].get('operation'))==s['operation'] and
                x['details'].get('use_path')==s['path'] and key(x['details'].get('ledger'))==key(s['object'])
                for s in settlements)]
        checks = [e.get('financial_scope') for e in current if e.get('financial_scope')]
        accounting=[r for e in current for r in e.get('amount_correspondence',[])]
        scope['amount_correspondence']=accounting
        mismatches={(r['operation'],r.get('path')) for r in accounting if r.get('result')=='source_ir_mismatch'}
        if mismatches:
            scope['unverified_quantity_routes']=[{'operation':o,'path':p} for o,p in sorted(mismatches,key=str)]
            positive=[x for x in positive if (x['details'].get('observe',x['details'].get('operation')),x['details'].get('use_path')) not in mismatches
                      and (x['details'].get('observe',x['details'].get('operation')),None) not in mismatches]
        scope['comparison_alignment'] = {'status': 'main' if positive else 'unresolved',
                                         'conditions': checks, 'source_basis': prop.get('resource_bindings', []),
                                         'prestate_alignment': prop['domain']}
        if cat in ('FCR-PAUSE', 'FCR-FREEZE'):
            scoped = {probe['id'] for ev in current if ev.get('scope_supported') for probe in ev.get('queries', [])}
            positive = [probe for probe in positive if probe['id'] in scoped]
        closed_paths=set()
        for ev in current:
            cert=ev.get('necessary_condition_route_coverage') or {}
            if (ev.get('property_excluded') and cert.get('source_identity')==inv.f.identity and
                    cert.get('operation')==root and cert.get('all_source_routes_accounted')):
                closed_paths.update(cert.get('excluded_paths',{}))
        contested=[x for x in positive if x.get('details',{}).get('use_path') in closed_paths]
        if contested:
            scope['same_path_evidence_conflict']=[x['id'] for x in contested]
            positive=[x for x in positive if x not in contested]
            if not positive:
                result['reasons']=['same_property_domain_conflicting_evidence']
                return result
        result['reportable'] = bool(positive)
        scope['property_support'] = [{'probe': x['id'], 'details': x['details']} for x in positive]
        if not positive:
            value_uses=set(prop.get('value_dependence',{}).get('value_uses',[])) if cat in (
                'FCR-MINT','FCR-TRANSFER','FCR-DESTROY') else set()
            measured_values={e.get('observe') for e in current if e.get('observed_measure')=='financial_value'
                             and e.get('value_route_checked')}
            unmeasured_values=value_uses-measured_values
            scope['unmeasured_value_consumers']=sorted(unmeasured_values)
            scope['value_effect_evidence']=[{'evidence':e['id'],'use':e.get('observe'),
                'queries':[x['id'] for x in e.get('queries',[])],'residuals':e.get('local_errors',[])}
                for e in current if e.get('observed_measure')=='financial_value']
            closed_values={e.get('observe') for e in current if e.get('observed_measure')=='financial_value' and e.get('property_excluded')}
            local_closed=any(e.get('observed_measure')=='direct_effect' and e.get('property_excluded') for e in current)
            excluded = not mismatches and not unmeasured_values and value_uses<=closed_values and local_closed
            result['reasons'] = ['matched_direct_effect_impossible_on_all_applicable_positions_and_paths'
                                 if excluded else 'financial_property_conditions_not_established']
            if settlements:result['reasons'].append('same_scope_actual_full_settlement')
            if excluded:
                scope['route_status'] = 'excluded'
                scope['comparison_alignment']['status'] = 'refuted'
        scope['normal_explanations'] = copy.deepcopy(q.get('local_normal_explanations', []))+[
            r for e in current for r in e.get('normal_explanations',[])]
    if result['reportable']:
        scope['route_status'] = 'supported'
        result['composed_claim'] = (f"{cat}: {inv.catalog.name(root)} establishes the source-bound "
                                    f"{'authorization violation' if cat == 'AC' else 'financial capability'} "
                                    f"under {prop['domain']}. The recorded property specifies subjects, effects and scope.")
        result['evidence_level'] = 'source_semantic_and_program'
    return result


def compose(inv, q, old=None):
    from .source_opinion import scoped_opinion, describe
    result = _typed_assessment(inv, q)
    scope = result['scope']
    cat = result['category'] or (q['current'].get('category') if q['current'].get('category') in ('AC','FCR-TRANSFER','FCR-MINT','FCR-DESTROY','FCR-PAUSE','FCR-FREEZE') else None)
    if cat:result['category']=cat
    basis = scoped_opinion(inv, q)
    current=q.get('changed_validation_key')
    if current and basis['status']=='risk' and not any(
            inv.evidence[e].get('property_validation_key')==current or
            inv.evidence[e].get('kind')=='source_inspection' and inv.evidence[e].get('operation')==result['root']
            for e in q['evidence']) and not q.get('office_effects') and not q['current'].get('_semantic_consumer'):
        # An unexamined semantic revision cannot inherit a delayed program result.
        # Independent, scoped source readings remain usable without a new solver query.
        basis={'status':'open','reason':'revised_policy_not_read','locations':basis['locations']}
    status = scope.get('route_status')
    blocked = {'source_ir_disagreement','changed_business_effect_requires_source_rebinding',
               'same_property_domain_conflicting_evidence','source_identity_ambiguous_or_unresolved',
               'derived_obligation_replaced_by_current_parent'}
    if status == 'excluded' or set(result['reasons']) & blocked or status == 'superseded':
        judgment = 'excluded' if status == 'excluded' else 'open'
        reason = 'source_check_excluded' if judgment == 'excluded' else 'core_mismatch'
    elif basis['status'] == 'excluded' or basis['reason'] in ('same_position_restored','no_new_controlled_credit','intra_ledger_transfer','parameter_only','zero_quantity','incoming_only','same_request_bypass','partial_quota','guarded_state_change','guarded_source_effect','local_bookkeeping'):
        judgment, reason = basis['status'], basis['reason']
        result.update(reportable=False,reasons=list(dict.fromkeys([reason]+[r for r in result['reasons'] if r=='same_scope_actual_full_settlement'])))
        scope['route_status'] = 'excluded' if judgment=='excluded' or reason in (
            'same_position_restored','guarded_state_change','intra_ledger_transfer','zero_quantity',
            'incoming_only','same_request_bypass','no_new_controlled_credit') else 'normal_prediction'
    elif basis['reason']=='conflicting_scoped_meanings' and not result['reportable']:
        judgment,reason='open',basis['reason']
    elif result['reportable']:
        judgment = 'risk'
        reason = 'source_certificate' if scope.get('source_property_certificates') and not scope.get('positive_condition_scopes') else 'program_support'
        if basis['status']=='risk':
            reason=basis['reason']
    else:
        judgment, reason = basis['status'], basis['reason']
        if judgment == 'risk' and cat:
            result.update(reportable=True,reasons=[],evidence_level='source_policy_or_right_prediction')
            scope.update(route_status='supported',comparison_alignment={'status':'main','source_scope_checked':True})
        elif judgment == 'normal':
            scope['route_status']='normal_prediction'
    if judgment == 'risk' and reason == 'source_certificate':
        result['evidence_level']='source_deduction'
    locations=basis['locations'] or ([inv.f.operations[result['root']]['source']] if result.get('root') else [])
    details=inv.semantics.rules.describe_source(result['root'],cat,reason,locations,q['id']) if getattr(inv.semantics,'rules',None) else {'explanation':describe(cat,reason)}
    scope['decision']={'status':judgment,'reason':reason,'locations':locations,**details}
    if locs := [r for r in locations if r.get('file') and 'start' in r]:
        scope['decision_identity']=digest([inv.f.identity,cat,result['root'],[(v['file'],v['start'],v.get('length')) for v in locs],reason])

    return result


def applicable_normal_authorization(inv,q,policy):
    """Only a checked applicable predicate can close a normal proposal.

    A stage/quantity guard, or the word normal, is never a certificate. The
    query must use this exact property, its actual operands and every complete
    committing path. Partial normal evidence stays local.
    """
    root=inv.root(q);p=q.get('property') or {}
    if not root or inv._direction_contradictions(q):return False
    if (policy or {}).get('property_family')=='acquire':return False
    rows={pid for pid,_ in inv.f.operation_paths(root,True)}
    if not rows or not inv.backend.complete(root):return False
    checked=[x for label in q['evidence'] for x in inv.evidence[label].get('queries',[])
        if x.get('label')=='authorization_violation' and x.get('details',{}).get('property_identity')==p.get('id')]
    if any(x.get('bounded_condition_confirmed') for x in checked):return False
    covered={x['details'].get('use_path') for x in checked if x.get('answer')=='unsat' and not x.get('abstract_hash') and
        x['details'].get('argument_domain')=='all_source_inputs_on_this_committing_path' and
        x['details'].get('prestate',{}).get('analysis_domain')=='ac_checked_prestate_r1'}
    return rows<=covered



def canonical_resource(row):
    if not isinstance(row,dict):return None
    return [row.get(k) for k in ('meaning','target','operation','family','quantity_scope','scope')]

def validation_key(p):
    if not p:
        return None
    resources = []
    for row in p.get('resource_bindings', []):
        binding = row.get('binding') or {}
        resources.append([row.get('kind'), binding.get('meaning'),
                          (binding.get('semantic_assertion') or {}).get('unit_kind')])
    expected = (p.get('expected_authorization') or {}).get('compiled_authorization') or {}
    return digest([p.get('scoped_semantics'),[canonical_resource(c) for c in p.get('consent_rows',())],p.get('source_identity'),p.get('target'),p.get('operation'),p.get('claim_identity'),p.get('domain'),p.get('initial_identity'),
        p.get('summary_identity'),sorted(key(x) for x in p.get('objects',[])),p.get('claim_assumptions'),p.get('stage'),
        expected.get('predicate'),expected.get('property_family'),expected.get('acquisition_uses'),
        sorted(key(x.get('predicate')) for x in expected.get('competing_interpretations',[])),sorted(key(x) for x in resources),
        p.get('value_dependence'),p.get('quantity_routes'),canonical_resource(p.get('financial_consent')),
        {o:canonical_resource(c) for o,c in (p.get('financial_consents') or {}).items()},p.get('original_category'),p.get('category_obligations')])
