## source/src/pr_next_joint/investigation/property_model.py

~~~~python
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


def authorization_expression(inv,q,policy,*,unresolved=None):
    from .relations import authorization
    return authorization(inv,q,policy,unresolved=unresolved)


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
            unresolved=set()
            predicate=authorization_expression(inv,q,policy,unresolved=unresolved)
            if (not predicate and not unresolved and policy.get('source') == 'focused_model_answer'
                    and item.get('_opinion_message') and item.get('_scope_effects')):
                from .policy_binding import effect_duty
                original_policy = policy_basis(item)
                if (original_policy and effect_duty(original_policy['text'])
                        and not effect_duty(policy.get('basis',''))):
                    # An uninformative reply cannot silently replace a previously bound duty.
                    policy = original_policy
                    predicate = authorization_expression(inv,q,policy,unresolved=unresolved)
            if unresolved:policy=dict(policy,unresolved_relations=sorted(unresolved))
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
        scoped=set(item.get('_scope_effects',())) if item.get('_opinion_message') else set()
        if scoped:
            from .summary import local_delta
            from .dependencies import control_candidates
            applicable=set()
            for handle in scoped:
                effect=inv.semantics.rules.effects.get(handle,{})
                if effect.get('oid')!=root or 'cell' not in effect:continue
                cell=effect['cell'];direction,_=local_delta(effect['write'])
                if holder(cell,f.lookup(root)) and not summaries.control_only(cell,target):
                    if direction=='-':applicable.update(('FCR-TRANSFER','FCR-DESTROY'))
                    if direction=='+':applicable.update(('FCR-TRANSFER','FCR-MINT'))
                for use in control_uses|value_uses:
                    for row in summaries.rows(use):
                        productive=[v['holder'] for v in row['numeric_effects'] if v['holder'] is not None and 'debit' in v['may_directions']]
                        if not productive:continue
                        if any(selector_relation(cell,s)=='same_shape' for s in selectors(row['guards'])):
                            applicable.update(control_candidates(cell,productive))
                        if use in value_uses and any(s['root']==cell['root'] for w in row['ordered_writes'] for s in selectors(w['value'])):
                            applicable.update(possible & {'FCR-TRANSFER','FCR-MINT','FCR-DESTROY'})
            if not item.get('category'):
                possible.intersection_update(applicable)
                # Missing unit remains an open, source-anchored consumer.
                if not possible:possible.update(applicable)
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
        nonstorage=any('kind' in inv.semantics.rules.effects.get(e,{}) for e in item.get('_scope_effects',()))
        reason = next(('original_root_has_no_committing_path' if r.get('no_committing_path')
                       else 'original_root_net_effect_is_unchanged' for r in inspections
                       if r.get('no_committing_path') or (not nonstorage and r.get('net_effect_proved_unchanged'))), None)
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
        result['reportable'] = bool(positives or source_support) and not (label=='denied_qualified' and expected.get('necessary_only'))
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
            if not acquire and not expected.get('necessary_only') and all_paths and all_paths <= excluded and subcases_complete and inv.backend.complete(root) and not expected.get('competing_interpretations'):
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
            scoped={}
            for ev in current:
                if not ev.get('scope_supported'):continue
                financial=ev.get('financial_scope') or {}
                group=financial.get('ordinary_holder_family')
                for probe in ev.get('queries',[]):
                    detail=probe.get('details') or {}
                    if cat=='FCR-PAUSE' and group and not financial.get('collective_source_control'):
                        if (not detail.get('all_continuations_exact') or not detail.get('same_request')
                            or detail.get('change')!=root or detail.get('observe')!=financial.get('declared_use')):continue
                    scoped[probe['id']]=(group,detail.get('observe'))
            positive = [probe for probe in positive if probe['id'] in scoped]
            if positive and scoped[positive[0]['id']][0]:
                group,use=scoped[positive[0]['id']]
                scope['ordinary_holder_family']=group
                if use in inv.f.operations:scope['ordinary_use_location']=inv.f.operations[use]['source']
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
    required=((q.get('property') or {}).get('expected_authorization') or {}).get('compiled_authorization') or {}
    if required.get('necessary_only') and basis['status']=='normal':
        basis={'status':'open','reason':'policy_missing','locations':basis['locations']}
    current=q.get('changed_validation_key')
    if current and basis['status']=='risk' and not any(
            inv.evidence[e].get('property_validation_key')==current or
            inv.evidence[e].get('kind')=='source_inspection' and inv.evidence[e].get('operation')==result['root']
            for e in q['evidence']) and not q.get('office_effects') and not q['current'].get('_semantic_consumer'):
        # An unexamined semantic revision cannot inherit a delayed program result.
        # Independent, scoped source readings remain usable without a new solver query.
        basis={'status':'open','reason':'revised_policy_not_read','locations':basis['locations']}
    if (result.get('root') and basis['status'] in ('normal','excluded') and any(
            g['kind'] in ('source_expression_limit','dependent_source_expression_limit')
            for g in inv.f.operations[result['root']]['gaps'])):
        basis={'status':'open','reason':'unexpanded_source_dependency','locations':basis['locations']}
        result.update(reportable=False,reasons=['unexpanded_source_dependency'])
        scope['route_status']='open'
    status = scope.get('route_status')
    blocked = {'source_ir_disagreement','changed_business_effect_requires_source_rebinding',
               'same_property_domain_conflicting_evidence','source_identity_ambiguous_or_unresolved',
               'derived_obligation_replaced_by_current_parent'}
    if status == 'excluded' or set(result['reasons']) & blocked or status == 'superseded':
        judgment = 'excluded' if status == 'excluded' else 'open'
        reason = 'source_check_excluded' if judgment == 'excluded' else 'core_mismatch'
    elif basis.get('decisive_consent_gap'):
        judgment,reason='open',basis['reason']
        result.update(reportable=False,reasons=[reason]);scope['route_status']='open'
    elif basis.get('same_scope_authorized') or basis['status'] == 'excluded' or basis['reason'] in ('ordinary_paid_credit','nominee_acceptance','no_debit_in_scope','applicable_payment_qualification','same_position_restored','no_new_controlled_credit','intra_ledger_transfer','parameter_only','zero_quantity','incoming_only','same_request_bypass','partial_quota','guarded_state_change','guarded_source_effect','local_bookkeeping'):
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
    # A program-level authorization proof is attached to its exact write
    # when every committing branch shares just that occurrence.
    if judgment=='risk' and cat=='AC' and reason=='program_support' and result.get('root'):
        actual=inv.f.summaries.rows(result['root'])
        sites={key(w['source']):w['source'] for row in actual if row['committing'] for w in row['ordered_writes']}
        if len(sites)==1 and all(not r['effects'] and not r['residuals'] for r in actual if r['committing']):
            locations=list(sites.values())
            basis=dict(basis,exact_write=True)
    details=inv.semantics.rules.describe_source(result['root'],cat,reason,locations,q['id']) if getattr(inv.semantics,'rules',None) else {'explanation':describe(cat,reason)}
    scope['decision']={'status':judgment,'reason':reason,'locations':locations,**details}
    if basis.get('source_relation') and judgment==basis['status']:
        scope['decision']['source_relation']=basis['source_relation']
        scope['decision']['causal_root']=locations[0]
    if basis.get('semantic_local'):
        scope['decision']['opinion_source']='source_bound_local_semantic_reading'
        scope['decision']['effects']=list(q['current'].get('_scope_effects',()))
        if judgment=='risk' and basis['status']=='risk' and reason=='scoped_semantic_conflict':result['evidence_level']='scoped_semantic_prediction'
    if result.get('root'):
        scope['decision']['application_location']=inv.f.operations[result['root']]['source']
    if len(locations)==1 and (basis.get('semantic_local') or basis.get('productive_use') or basis.get('protected_use') or basis.get('exact_write')):
        scope['decision']['causal_root']=locations[0]
    if scope.get('ordinary_holder_family') and judgment=='risk':
        scope['decision']['holder_family']=scope['ordinary_holder_family']
        if scope.get('ordinary_use_location'):scope['decision']['productive_use']=scope['ordinary_use_location']
    if basis.get('holder_family') and judgment=='risk':
        scope['decision']['holder_family']=basis['holder_family']
    if basis.get('productive_use') and judgment=='risk':
        scope['decision'].update(productive_use=basis['productive_use'],basis_probe=basis['basis_probe'])
        if basis.get('conditional_agent'):
            scope['decision']['conditional_agent']=basis['conditional_agent']
            scope['decision']['explanation']+=' An already exempt agent may serve the same request if the holder granted the required allowance.'
    if basis.get('protected_use') and judgment=='risk':
        scope['decision']['protected_use']=basis['protected_use']
        scope['decision']['explanation']+=' A separate entry consumes the changed qualification at the linked source location.'
    if locs := [r for r in locations if r.get('file') and 'start' in r]:
        scope['decision_identity']=digest([inv.f.identity,cat,result['root'],[(v['file'],v['start'],v.get('length')) for v in locs],reason])

    result['reportable']=judgment=='risk' and bool(cat and result.get('root'))
    return result


def applicable_normal_authorization(inv,q,policy):
    """Only a checked applicable predicate can close a normal proposal.

    A stage/quantity guard, or the word normal, is never a certificate. The
    query must use this exact property, its actual operands and every complete
    committing path. Partial normal evidence stays local.
    """
    root=inv.root(q);p=q.get('property') or {}
    if not root or inv._direction_contradictions(q):return False
    if (policy or {}).get('property_family')=='acquire' or (
        ((p.get('expected_authorization') or {}).get('compiled_authorization') or {}).get('necessary_only')
        or (p.get('expected_authorization') or {}).get('unresolved_relations')):return False
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
        expected.get('necessary_only',False),(p.get('expected_authorization') or {}).get('unresolved_relations'),
        sorted(key(x.get('predicate')) for x in expected.get('competing_interpretations',[])),sorted(key(x) for x in resources),
        p.get('value_dependence'),p.get('quantity_routes'),canonical_resource(p.get('financial_consent')),
        {o:canonical_resource(c) for o,c in (p.get('financial_consents') or {}).items()},p.get('original_category'),p.get('category_obligations')])

~~~~

## source/src/pr_next_joint/investigation/protocol.py

~~~~python
"""Tolerant local normalization. The model never supplies AST, SMT or host identity."""
import copy,json,re,time
from pr_next_joint.core import digest
from .contracts import VERSION,ident,write
from .decision_output import receipt as body_receipt,context_summary,diagnostic

ANSWER_CHOICES = {
    'resource': ('financial_right', 'nonfinancial_counter', 'other_source_explanation', 'unknown'),
    'authorization': ('required_authorization', 'normal_authorization', 'other_source_explanation', 'unknown'),
    'financial_consent': ('gross_debit_bound', 'net_request_with_fee', 'other_source_explanation', 'unknown'),
}
AMOUNT_ROLES = ('original_request','request','gross_debit','debit','net_receipt','net','compensation')
STAGE_GUIDANCE = 'initialization_stage requires subject (its source stage flag).'
AMOUNT_GUIDANCE = 'amount_role requires role: ' + '/'.join(AMOUNT_ROLES) + '.'


def role_error(row, meaning, inherited=None):
    if 'role' not in row:
        return 'field_absent' if meaning=='amount_role' and inherited not in AMOUNT_ROLES else None
    if not isinstance(row['role'],str):return 'wrong_field_type'
    if row['role'] not in AMOUNT_ROLES:return 'outside_facet_vocabulary'
    return None


REVISION_ACTIONS = ('confirm', 'correct', 'narrow', 'withdraw')
REVISION_GUIDANCE = 'Use the shown support ref in its original facet, with action ' + '/'.join(REVISION_ACTIONS) + ' and a short reason for any change.'
INSTRUCTION = 'Read the displayed source for the actual target. Return one JSON object. Keep actors, ordered grants, phase and units distinct. No concrete actors, arguments, sequences or private reasoning.'

def instruction(task, recovery=False, *, kind=None, annotation_revision=False, policy_revision=False):
    common = INSTRUCTION
    if kind == 'scoped_support_dispute':
        return common + ' ' + REVISION_GUIDANCE + (' ' + AMOUNT_GUIDANCE if annotation_revision else '') + (' ' + STAGE_GUIDANCE if policy_revision else '')
    if kind in ANSWER_CHOICES:
        return common + ' Reply with answers[{question,answer,basis}] for the displayed question, using its choices and a brief source-based reason.' + (' A shown annotation may be revised by ref. ' + AMOUNT_GUIDANCE if annotation_revision else '') + (' ' + STAGE_GUIDANCE if policy_revision else '')
    if kind == 'local_effect':
        return common+' For the displayed effect answer issues[{effect,assessment,claim}]. Compare the applicable duty with who decides; give the actual local reason once.'
    if kind == 'issue':
        return common + ' Revise the displayed issue only. Cite its anchor, new evidence, assessment (risk, normal or investigate) and short reason.'
    meanings = sorted(ANNOTATIONS - (set() if task == 'FCR' else {'price','fee_rule','amount_role','transfer_condition'}))
    policies = sorted(POLICIES - (set() if task == 'FCR' else {'gross_debit_bound','net_request_with_fee'}))
    issue='Use issues[{effect or anchors,assessment,claim,policy_basis?,normal_explanation?}]. Give a short scoped comparison; assessment is risk, normal or investigate.'
    direction=('AC: state the applicable duty, who actually controls the effect and whether they conflict.' if task=='AC' else 'FCR: distinguish unit, holder consent, compensation and productive bypass; category is optional.')
    return ' '.join((common,direction,issue,'Alternatively use annotations[{on,meaning,basis}] or policies[{effect,meaning,basis,subject?}] once.',
        'Annotations: '+', '.join(meanings)+'. Policies: '+', '.join(policies)+'.',
        AMOUNT_GUIDANCE if 'amount_role' in meanings else '',STAGE_GUIDANCE,
        'For a scoped empty reading use task_analysis {task,anchors,basis}.' if not recovery else 'Correct the malformed reply using this source.'))

def question_entity(question):
    return digest([question.get(k) for k in ('id','operation','target','kind','cell','semantic_scope','core_operation','quantity_scope')])

def revision_support(item,previous,available):
    """Locate a model-supplied reason; never synthesize its business explanation.

    available is the actual new evidence sent for this issue. Exact probe IDs
    identify their containing evidence without making the model repeat labels.
    """
    texts=[item[k] for k in ('claim','revision_reason','reason','explanation')
           if isinstance(item.get(k),str)]
    refs=item.get('evidence',[])
    if isinstance(refs,str):refs=[refs]
    if not isinstance(refs,list):refs=[]
    locators={x for x in refs if isinstance(x,str)}
    for text in texts:locators.update(re.findall(r'\b(?:E\d+|probe_[a-f0-9]{20})\b',text))
    cited=set();matches=[]
    for label,record in available.items():
        ids={q['id'] for group in ('queries','holder_consent_counterexamples')
             for q in record.get(group,[]) if isinstance(q,dict) and q.get('id')}
        found=locators & ({label}|ids)
        if found:cited.add(label);matches.extend({'locator':x,'evidence':label} for x in sorted(found))
    reason=next((item[k].strip() for k in ('revision_reason','reason','explanation')
                 if isinstance(item.get(k),str) and item[k].strip()),None)
    if reason is None and isinstance(item.get('claim'),str) and item['claim'].strip()!=previous.get('claim','').strip():
        reason=item['claim'].strip()
    if reason and not re.sub(r'\b(?:E\d+|probe_[a-f0-9]{20})\b|[\W_]+','',reason):reason=None
    return sorted(cited),reason,matches


def category_value(category, task=None):
    """Finite spelling normalization, never infer a financial class from an action."""
    if category is None and task == 'AC':
        return 'AC'
    if not isinstance(category, str):
        return category
    token = re.sub(r'[\s_-]+', '-', category.strip().upper())
    if token in ('AC', 'ACCESS-CONTROL', 'ACCESS-CONTROL-VULNERABILITY'):
        return 'AC'
    # Permission/authorization is a single-task alias, not a rule classifying arbitrary prose.
    if task == 'AC' and (token in ('PERMISSION', 'AUTHORIZATION', 'AUTHORISATION') or
                         token.startswith(('ACCESS-CONTROL/', 'AUTHORIZATION/', 'AUTHORISATION/'))):
        return 'AC'
    names = ('TRANSFER', 'MINT', 'DESTROY', 'PAUSE', 'FREEZE')
    if token in names or token in tuple('FCR-' + n for n in names):
        return token if token.startswith('FCR-') else 'FCR-' + token
    m = re.fullmatch(r'FCR[/:]\s*(TRANSFER|MINT|DESTROY|PAUSE|FREEZE)|(TRANSFER|MINT|DESTROY|PAUSE|FREEZE)-?\(FCR\)', token)
    if m:return 'FCR-' + (m[1] or m[2])
    names_in_label=[n for n in names if re.search(r'(?<![A-Z])'+n+r'(?![A-Z])',token)]
    tagged=re.match(r'^FCR[-:/]-?(TRANSFER|MINT|DESTROY|PAUSE|FREEZE)(?:$|[-:/])',token)
    # An explicit namespace/class followed by explanation stays that class;
    # a multi-class label is still unresolved, not split into invented findings.
    return 'FCR-'+tagged[1] if tagged and names_in_label==[tagged[1]] else category


def normal_alternative(item):
    """Return only model-supplied original-program interpretation, with provenance."""
    obs = item.get('observation'); obs = obs if isinstance(obs, dict) else {}
    text = next((v.strip() for v in (item.get('alternative'), item.get('normal_explanation'),
                                    obs.get('normal_explanation')) if isinstance(v, str) and v.strip()), None)
    origin = 'explicit_field'
    if text is None:
        match = re.search(r'(?:relevant\s+)?normal (?:alternative|explanation)\s*:\s*(.+)', item.get('claim', ''), re.I | re.S)
        if match:
            text = match[1].strip(); origin = 'explicit_inline_claim'
    if text is None:
        return {'text': None, 'status': 'not_supplied', 'origin': None}
    hypothetical = re.search(r'\bif\b[^.!?]{0,180}\b(?:were (?:guarded|restricted|added)|had been (?:guarded|set|initialized)|guard were added)\b|'
                             r'\b(?:add|insert|introduce) (?:an? |the )?(?:guard|require|modifier)\b', text, re.I)
    return {'text': text, 'origin': origin,
            'status': 'counterfactual_program_not_normal_path' if hypothetical else 'supplied_not_program_proved'}


def semantic_direction(item, task, source_unrestricted=False):
    """Check a prediction for explicit task contradictions, not discover business risks.

    No missing controller field is required. Source checks can corroborate an explicitly
    ordinary-caller claim; public syntax alone never excludes a privileged branch.
    """
    # A competing, not-yet-accepted normal explanation is not the model's risk assertion.
    text = re.split(r'(?:relevant\s+)?normal (?:alternative|explanation)\s*:', item.get('claim', ''),
                    maxsplit=1, flags=re.I)[0]
    cat = item.get('category'); assessment = item.get('assessment')
    result = {'status': 'no_explicit_conflict', 'reasons': [], 'source_unrestricted': source_unrestricted}
    if task != 'FCR':
        return result
    outside = re.search(r'\b(?:ordinary (?:reentrancy |unprivileged )?attack|non[- ]FCR|not (?:an? |a privileged )?FCR|'
                        r'not a privileged (?:financial )?(?:risk|FCR))\b', text + ' ' + str(cat), re.I)
    no_controller = re.search(r'\b(?:no (?:actual )?privileged controller|attacker is not (?:an? )?privileged|'
                              r'not an? FCR by an actual privileged controller|no (?:normal|real|non-zero) account can (?:call|invoke))\b', text, re.I)
    anycaller = re.search(r'\bany (?:external )?(?:caller|requester|msg\.sender|account)\b', text, re.I)
    ordinary = item.get('risk_direction') in ('ordinary_exploit', 'unprivileged_attack')
    if assessment == 'risk' and (outside or no_controller or ordinary or anycaller and source_unrestricted):
        result.update(status='inconsistent_task_direction', reasons=['ordinary_attack_or_no_privileged_FCR_controller'])
    # Explicit non-task clues remain recorded without poisoning all five task categories.
    if cat not in ('FCR-TRANSFER', 'FCR-MINT', 'FCR-DESTROY', 'FCR-PAUSE', 'FCR-FREEZE') and (outside or no_controller):
        result.update(status='explicit_out_of_task_clue', reasons=['model_explicitly_distinguishes_non_FCR'])
    return result


def category_scope(item, task):
    """Coverage only: a disjunctive label stays unresolved within its named classes."""
    if task == 'AC':
        return ['AC']
    cat = item.get('category')
    if cat in ('FCR-TRANSFER', 'FCR-MINT', 'FCR-DESTROY', 'FCR-PAUSE', 'FCR-FREEZE'):
        return [cat]
    token = str(cat or '').upper()
    named = sorted({'FCR-' + c for c in ('TRANSFER', 'MINT', 'DESTROY', 'PAUSE', 'FREEZE')
                    if re.search(r'(?<![A-Z])' + c + r'(?![A-Z])', token)})
    return named  # Unscoped dependencies are resolved from actual source in coverage.py.

TOP_LISTS = frozenset(('annotations','policies','issues','answers','reviewed'))
WIRE_FIELDS = TOP_LISTS | {'task_analysis'}
ANNOTATIONS = frozenset(('management_role','eligibility_state','financial_right','nonfinancial_counter',
    'authorization_quantity','price','fee_rule','transfer_condition','amount_role','other_source_meaning','unknown'))
POLICIES = frozenset(('current_authority_required','holder_authorization_applies','initialization_stage',
    'gross_debit_bound','net_request_with_fee','other_source_policy','unknown'))


class AmbiguousKeys(dict):
    def __init__(self,pairs):
        super().__init__();self.duplicates=set()
        for name,val in pairs:
            if name in self:self.duplicates.add(name)
            self[name]=val


def wire_object(pairs):
    return AmbiguousKeys(pairs)


def ambiguous(value):
    if isinstance(value,AmbiguousKeys) and value.duplicates:return True
    if isinstance(value,list):return any(ambiguous(x) for x in value)
    if isinstance(value,dict):return any(ambiguous(x) for x in value.values())
    return False


def partial_envelope(text):
    decoder = json.JSONDecoder(object_pairs_hook=wire_object)
    size = len(text)
    def space(i):
        while i < size and text[i].isspace():
            i += 1
        return i
    i = space(1)
    value = {}
    seen = set()
    duplicates = set()
    if not text.startswith('{'):
        return {}, False
    while i < size:
        try:
            name, i = decoder.raw_decode(text, i)
        except ValueError:
            break
        i = space(i)
        if not isinstance(name, str) or i >= size or text[i] != ':':
            break
        if name in seen:
            duplicates.add(name)
        seen.add(name)
        i = space(i+1)
        if name in TOP_LISTS and i < size and text[i]=='[':
            rows = []
            value[name] = rows
            i = space(i+1)
            while i < size and text[i] != ']':
                try:
                    row, end = decoder.raw_decode(text,i)
                except ValueError:
                    break
                i = space(end)
                if i < size and text[i] not in ',]':
                    break
                rows.append(row)
                if i >= size or text[i] != ',':
                    break
                i = space(i+1)
            if i >= size or text[i] != ']':
                break
            i = space(i+1)
        else:
            try:
                part,end=decoder.raw_decode(text,i)
            except ValueError:
                break
            if name in WIRE_FIELDS:value[name]=part
            i=space(end)
        if i >= size or text[i] != ',':break
        i=space(i+1)
    for name in duplicates:value.pop(name,None)
    return value, bool(any(value.get(k) for k in WIRE_FIELDS))


def envelope_shape(raw):
    """Content-free structural diagnostic. Never return a key name or response text."""
    if not isinstance(raw,str):
        return {"root_type":"non_text","recognized_keys":0,"unknown_keys":0,"duplicate_keys":0}
    text=re.sub(r'^\x60\x60\x60(?:json)?\s*','',raw.strip(),flags=re.I)
    text=re.sub(r'\s*\x60\x60\x60$','',text)
    try:
        value=json.loads(text,object_pairs_hook=wire_object)
    except (ValueError,RecursionError):
        first=text[:1]
        return {"root_type":"incomplete_or_invalid_json","opening":"object" if first=='{' else "array" if first=='[' else "other",
                "recognized_keys":0,"unknown_keys":0,"duplicate_keys":0}
    if isinstance(value,dict):
        return {"root_type":"object","recognized_keys":len(WIRE_FIELDS.intersection(value)),
                "unknown_keys":len(set(value)-WIRE_FIELDS),
                "duplicate_keys":len(value.duplicates) if isinstance(value,AmbiguousKeys) else 0}
    return {"root_type":"array" if isinstance(value,list) else "scalar",
            "recognized_keys":0,"unknown_keys":0,"duplicate_keys":0}


def issue_shape(item):
    """Reject only the row whose declared wire value has the wrong shape."""
    text = ('id', 'effect', 'subject', 'category', 'assessment', 'claim', 'policy_basis',
            'alternative', 'normal_explanation', 'risk_direction', 'distinguishing_question',
            'revision_reason', 'explanation', 'reason')
    for field in text:
        if field in item and item[field] is not None and not isinstance(item[field], str):
            return field, item[field]
    for field in ('observation', 'next_check'):
        value = item.get(field)
        if value is not None and not isinstance(value, dict):
            return field, value
        for name in ('measure', 'normal_explanation', 'action', 'change', 'observe',
                     'function', 'caller_mode', 'question', 'resource', 'subject'):
            if isinstance(value, dict) and name in value and not isinstance(value[name], str):
                return field + '.' + name, value[name]
    for field in ('evidence', 'source_refs', 'anchors'):
        value = item.get(field)
        if value is not None and not isinstance(value, (str, list)):
            return field, value
        if isinstance(value, list):
            for entry in value:
                if not isinstance(entry, str):
                    return field + '[]', entry
    hint = item.get('next_check') or {}
    if 'request_bindings' in hint and not isinstance(hint['request_bindings'], dict):
        return 'next_check.request_bindings', hint['request_bindings']
    return None


def normalize(raw,task=None,*,phase='initial',sent_questions=()):
    """Parse one top-level envelope. Transport validity and semantic binding are independent."""
    diagnostics=[]
    def empty(kind, reason):
        return dict(issues=[],answers=[],annotations=[],policies=[],reviewed=[],usable_analysis=False,
                    response_kind=kind,diagnostics=[dict(d,stage=phase) for d in diagnostics]+[{'reason':reason,'stage':phase}])
    if raw is None or isinstance(raw,str) and not raw.strip():
        return empty('empty_body','empty_response_body')
    recovered=False
    if isinstance(raw,dict):
        value=copy.deepcopy(raw)
    elif isinstance(raw,str):
        text=re.sub(r'^\x60\x60\x60(?:json)?\s*','',raw.strip(),flags=re.I)
        text=re.sub(r'\s*\x60\x60\x60$','',text)
        try:value=json.loads(text,object_pairs_hook=wire_object)
        except (ValueError,RecursionError):
            try:completed,end=json.JSONDecoder().raw_decode(text)
            except (ValueError,RecursionError):pass
            else:
                if text[end:].strip():return empty('invalid_protocol','trailing_unrelated_content')
            value,recovered=partial_envelope(text)
            if not recovered:return empty('invalid_protocol','unparseable_top_level')
            diagnostics.append({'reason':'truncated_envelope_complete_items_only'})
    else:return empty('invalid_protocol','invalid_response_type')
    if isinstance(value,AmbiguousKeys) and value.duplicates:
        for name in value.duplicates:value.pop(name,None)
        diagnostics.append({'reason':'ambiguous_top_level_field'})
    if not isinstance(value,dict) or not WIRE_FIELDS.intersection(value):
        return empty('invalid_protocol','invalid_top_level_or_duplicate_key')
    # Never infer source or host authority from undeclared fields in a model row.
    bad=bool(diagnostics)
    had_content=False
    row_ordinals={}
    for field in TOP_LISTS:
        vals=value.get(field,[])
        if not isinstance(vals,list):
            diagnostics.append({'reason':field+'_not_list'});bad=True;vals=[]
        had_content|=bool(vals)
        valid=[]
        for idx,row in enumerate(vals):
            row_ordinals[(field,id(row))]=idx
            if ambiguous(row) or (isinstance(row,dict) and any(k.startswith('_') for k in row)):
                diagnostics.append({'reason':'duplicate_or_host_reserved_key','list':field,'index':idx});bad=True
            else:valid.append(row)
        value[field]=valid
    seeds={}
    located_amount_reads=[]
    for field,vocab,refkey in [('annotations',ANNOTATIONS,'on'),('policies',POLICIES,'effect')]:
        seeds[field]=[]
        for fallback,row in enumerate(value[field]):
            idx=row_ordinals.get((field,id(row)),fallback)
            if not isinstance(row,dict) or set(row)-{'id','on','effect','subject','scope','meaning','basis','ref','action','role'}:
                diagnostics.append({'reason':'invalid_seed_fields','list':field,'index':idx});bad=True;continue
            if ('effect' if field=='annotations' else 'on') in row:
                diagnostics.append({'reason':'wrong_semantic_locator_kind','list':field,'index':idx});bad=True;continue
            invalid=next((k for k,v in row.items() if not isinstance(v,str)),None)
            if invalid is not None:
                diagnostics.append({'stage':phase,'list':field,'index':idx,'field_path':invalid,
                    'reason':'invalid_semantic_field_shape','actual_type':type(row[invalid]).__name__})
                bad=True;continue
            revision='ref' in row or 'action' in row
            action=row.get('action','add')
            located=bool(isinstance(row.get(refkey),str) and row[refkey].strip()) if not revision else (
                isinstance(action,str) and action in REVISION_ACTIONS and isinstance(row.get('ref'),str))
            meaning_ok=(revision and action in ('confirm','narrow','withdraw') and 'meaning' not in row or
                        isinstance(row.get('meaning'),str) and row['meaning'] in vocab)
            if not located or not meaning_ok or (action!='confirm' and not (isinstance(row.get('basis'),str) and row['basis'].strip())):
                missing = refkey if not located else 'meaning' if not meaning_ok else 'basis'
                raw_field = row.get(missing)
                diagnostics.append({'reason':'invalid_semantic_row','list':field,'index':idx,'field':missing,
                    'subreason':'field_absent' if raw_field is None else 'invalid_locator' if not located else 'outside_facet_vocabulary' if not meaning_ok else 'missing_source_reason',
                    'actual_type':type(raw_field).__name__,'value_length':len(raw_field) if isinstance(raw_field,str) else None,'value_sha256':digest(raw_field)})
                bad=True;continue
            if row.get('meaning')=='initialization_stage' and not (revision and 'subject' not in row) and not isinstance(row.get('subject'),str):
                actual=row.get('subject')
                diagnostics.append({'reason':'invalid_semantic_row','list':field,'index':idx,'field':'subject',
                    'subreason':'field_absent' if 'subject' not in row else 'wrong_field_type',
                    'actual_type':type(actual).__name__,'value_sha256':digest(actual)})
                bad=True;continue
            # A reply to a shown support can inherit its current role. Its
            # authenticated object and prior fact are checked by the consumer.
            issue=role_error(row,row.get('meaning')) if 'role' in row or not revision else None
            if issue:
                if field=='annotations' and row.get('meaning')=='amount_role' and not revision and not {'scope','subject'} & row.keys():
                    located_amount_reads.append(row[refkey])
                actual=row.get('role')
                diagnostics.append({'reason':'invalid_semantic_row','list':field,'index':idx,
                    'field':'role','subreason':issue,'actual_type':type(actual).__name__,
                    'value_length':len(actual) if isinstance(actual,str) else None,'value_sha256':digest(actual)})
                bad=True;continue
            bound=dict(row);seeds[field].append(bound)
            row_ordinals[(field,id(bound))]=idx
    answers=[]
    for index,row in enumerate(value.get('answers',[]) if isinstance(value.get('answers',[]),list) else []):
        index=row_ordinals.get(('answers',id(row)),index)
        if not isinstance(row,dict) or not all(isinstance(row.get(k),str) and row[k].strip() for k in ('question','answer','basis')):
            diagnostics.append({'answer':index,'reason':'semantic_answer_missing_question_answer_or_basis','original':row});continue
        if phase!='focused_revision' or row['question'] not in sent_questions:
            diagnostics.append({'list':'answers','index':index,'field':'question','reason':'semantic_answer_outside_sent_scope'})
            continue
        answers.append(copy.deepcopy(row))
    issues=[];seen=set()
    for index,item in enumerate(value['issues']):
        index=row_ordinals.get(('issues',id(item)),index)
        if not isinstance(item,dict):diagnostics.append({'item':index,'reason':'issue_not_object'});continue
        shape = issue_shape(item)
        if shape:
            field, value_received = shape
            diagnostics.append({'stage':phase, 'list':'issues', 'index':index,
                'field_path':field, 'actual_type':type(value_received).__name__,
                'reason':'invalid_issue_field_shape', 'subreason':'wrong_field_type'})
            bad=True
            continue
        item={k:v for k,v in item.items() if v is not None}
        claim=item.get('claim');anchors=item.get('anchors',[])
        if isinstance(anchors,str):anchors=[anchors]
        if not isinstance(claim,str) or not claim.strip() or not isinstance(anchors,list) or not (any(isinstance(x,str) and x.strip() for x in anchors) or isinstance(item.get('effect'),str) and item['effect'].strip()):
            diagnostics.append({'item':index,'reason':'missing_claim_or_source_anchor','original':item});continue
        identifier=item.get('id') if isinstance(item.get('id'),str) and item['id'].strip() else ident('issue',[claim,anchors,item.get('effect')])
        if identifier in seen:
            identifier=identifier+'_'+digest([index,item])[:8];diagnostics.append({'item':index,'reason':'duplicate_id_disambiguated'})
        seen.add(identifier)
        issue=copy.deepcopy(item);issue.update(id=identifier,claim=claim.strip(),anchors=[x.strip() for x in anchors if isinstance(x,str) and x.strip()])
        issue['_host_defaulted_fields']=[k for k in ('assessment','category') if k not in item or item.get(k) is None]
        cat=issue.get('category');normalized=category_value(cat,task)
        if normalized!=cat:
            issue['category']=normalized
            issue['_category_normalization']={'original':cat,'normalized':normalized,'basis':'finite task/spelling alias; no inferred financial class'}
        elif normalized is not None and normalized not in ('AC','FCR-TRANSFER','FCR-MINT','FCR-DESTROY','FCR-PAUSE','FCR-FREEZE'):
            diagnostics.append({'item':index,'issue':identifier,'reason':'category_ambiguous_or_outside_supported_task','original_category':cat})
        raw_assessment=issue.get('assessment')
        token=re.sub(r'[\s-]+','_',raw_assessment.strip().lower()) if isinstance(raw_assessment,str) else None
        aliases={'risk':'risk','confirmed_risk':'risk','risk_confirmed':'risk','vulnerable':'risk',
                 'normal':'normal','no_risk':'normal','not_vulnerable':'normal',
                 'investigate':'investigate','uncertain':'investigate','unknown':'investigate'}
        judgment=aliases.get(token);basis='explicit status vocabulary';problem=None
        # Bare "confirmed" is not itself a positive risk judgment. In
        # particular, a risk noun inside a negated sentence is not evidence
        # of affirmative polarity. Only finite explicit affirmative wording
        # is normalized; other prose stays unresolved with its original text.
        # Old confirmations can carry an explicit proposition. Negation of
        # authorization is different from negation of the risk proposition.
        negative_head = re.match(r'^\s*(?:(?:this|that|there)\s+is\s+)?(?:not (?:a |an )?|no )(?:risk|vulnerabilit\w*|unauthorized access)\b',claim,re.I)
        positive_head = re.match(r'^\s*(?:this (?:is|poses|constitutes) (?:a |an )?(?:risk|vulnerability)|(?:the )?(?:caller|spender|requester|actor) (?:gains unauthorized access|lacks (?:applicable )?authorization)|(?:the )?(?:entry|function|operation) (?:does not check|fails to check|omits) (?:the )?(?:applicable|required|holder.s|incumbent.s) authorization)\b',claim,re.I)
        if token=='confirmed':
            if negative_head:judgment='normal'
            elif positive_head and normalized in ('AC','FCR-TRANSFER','FCR-MINT','FCR-DESTROY','FCR-PAUSE','FCR-FREEZE'):judgment='risk'
            else:problem='ambiguous_confirmation_not_a_risk_judgment'
        explicit_false=item.get('is_vulnerable') is False or item.get('risk') is False
        explicit_true=item.get('is_vulnerable') is True or item.get('risk') is True
        if (judgment=='risk' and (negative_head or explicit_false)) or (judgment=='normal' and explicit_true):
            problem='contradictory_explicit_judgment';judgment=None
        if judgment is None:
            judgment='investigate';problem=problem or ('missing_assessment' if raw_assessment is None else 'unknown_assessment_vocabulary')
            diagnostics.append({'item':index,'issue':identifier,'reason':problem,'original_assessment':raw_assessment,
                                'host_unresolved_not_model_choice':True})
        if raw_assessment!=judgment or problem:
            issue['_assessment_normalization']={'original':raw_assessment,'normalized':judgment,'basis':basis if not problem else problem,
                                               'host_unresolved_not_model_choice':bool(problem)}
        issue['assessment']=judgment
        issues.append(issue)
    reviewed=value.get('reviewed',[])
    if not isinstance(reviewed,list):diagnostics.append({'reason':'reviewed_not_list'});reviewed=[]
    declaration=value.get('task_analysis')
    has_reading=(isinstance(declaration,dict) and not ambiguous(declaration)
                 and isinstance(declaration.get('basis'),str) and bool(declaration['basis'].strip())
                 and isinstance(declaration.get('anchors',[]),list)
                 and all(isinstance(a,str) for a in declaration.get('anchors',[])))
    if declaration is not None and not has_reading:
        diagnostics.append({'stage':phase,'field_path':'task_analysis','reason':'invalid_task_reading_shape','actual_type':type(declaration).__name__})
        value.pop('task_analysis',None);bad=True
    empty = not had_content and not recovered and not bad
    kind = 'substantive' if issues or answers or any(seeds.values()) or has_reading else 'explicit_empty' if empty else 'unbound_content' if had_content and not recovered else 'invalid_protocol'
    for row in diagnostics:
        row.setdefault('stage',phase)
        if 'item' in row:row.setdefault('list','issues')
        if 'answer' in row:row.setdefault('list','answers')
    positions={field:[row_ordinals[(field,id(seed))] for seed in entries] for field,entries in seeds.items()}
    return {**seeds,'located_amount_reads':located_amount_reads,'issues':issues,'answers':answers,'reviewed':[x for x in reviewed if isinstance(x,str)],
            'response_kind':kind,'usable_analysis':kind in ('substantive','explicit_empty'),
            'diagnostics':diagnostics,'row_positions':positions,'recovered_partial_envelope':recovered,'original_envelope':value}

class Session:
    def __init__(self,program,context,out,client):
        self.program,self.context,self.out,self.client=program,context,out,client
        self.attempts=[];self.model_wait_seconds=0.;self.submitted=0
        if hasattr(client,'program_identity') and client.program_identity is None:client.program_identity=program.identity
    def accounting(self):
        if hasattr(self.client,'accounting'):return self.client.accounting()
        return {'real_model_calls':0,'nature':'offline engineering fixture; not a real model experiment'}
    def is_simulated(self):return not bool(getattr(self.client,'live_authorized',False))
    def request(self,*,feedback=None,recovery=False,prepared=None):
        if len(self.attempts)>=self.program.options.attempt_limit:return None
        index=len(self.attempts);messages,manifest=prepared if prepared is not None else self.context.messages(feedback,recovery=recovery)
        if digest(messages)!=manifest['messages_sha256']:raise ValueError('prepared_message_identity_changed')
        row={'index':index,'phase':'protocol_recovery' if recovery else 'initial' if feedback is None else 'focused_revision',
             'messages_sha256':digest(messages),'input_tokens':manifest['input_tokens'],
             'output_limit':self.program.options.output_limit,'actual_model_submissions':0}
        write(self.out/f'request_receipt_{index}.json',{'host_identity':self.program.identity,**body_receipt(messages,'model_request'),'manifest':context_summary(manifest)})
        self.attempts.append(row)
        if manifest['input_tokens']>self.program.options.input_limit:
            row.update(status='not_sent',submission_state='not_dispatched',reason='complete_message_capacity_exceeded');write(self.out/f'attempt_{index}.json',row);return None
        started=time.monotonic()
        try:
            raw,receipt=self.client.call(messages,'semantic_initial' if index==0 else 'semantic_feedback',
              max_tokens=self.program.options.output_limit,thinking=True,reasoning_effort='high',timeout=1800)
            row['response_received']=True
            write(self.out/f'response_digest_{index}.json',{'content_sha256':digest(raw),'body_retained':False});write(self.out/f'receipt_{index}.json',receipt)
            if receipt.get('messages_sha256')!=digest(messages) or receipt.get('response_sha256')!=digest(raw):raise ValueError('bridge_response_identity')
            if receipt.get('program_identity')!=self.program.identity or receipt.get('case_id')!=self.client.case_id:raise ValueError('bridge_program_or_case_identity')
            simulated=receipt.get('simulated')
            if type(simulated)is not bool or not simulated and not getattr(self.client,'live_authorized',False):
                raise ValueError('fresh_runtime_authorization_required')
            row['response_identity_verified']=True
            value=normalize(raw,task=self.program.options.scope,phase=row['phase'],sent_questions=manifest.get('semantic_wire',{}))
            value['origin']='fixture' if simulated else 'verified_service'
            row['response_kind']=value['response_kind'];row['usable']=value['usable_analysis']
            write(self.out/f'normalization_receipt_{index}.json',{'response_kind':value['response_kind'],'normalized_sha256':digest(value),'issues':len(value['issues']),'answers':len(value['answers']),'usable_analysis':value['usable_analysis'],'body_retained':False,
                'envelope_shape':envelope_shape(raw) if not value['usable_analysis'] else None})
            row.update(status='analysis_received' if value['usable_analysis'] else 'protocol_diagnostic',
                       simulated=simulated,usage=receipt.get('usage'),cost_usd=receipt.get('cost_usd'),
                       cost_usd_upper=receipt.get('cost_usd_upper'),service_model=receipt.get('model'),
                       actual_model_submissions=receipt.get('actual_model_submissions',0),
                       normalization_diagnostics=[diagnostic(d) for d in value['diagnostics']])
            return value
        except Exception as error:
            row.update(status='transport_or_identity_error',reason=type(error).__name__,error_sha256=digest(str(error)));return None
        finally:
            if hasattr(self.client,'attempt_record'):
                row['dispatch_accounting']=self.client.attempt_record(index)
                row['actual_model_submissions']=row['dispatch_accounting'].get('actual_model_submissions',0)
            account=row.get('dispatch_accounting') or {}
            # A provider timeout after recording a possible submission is not a confirmed response.
            row['submission_state']=('fixture' if row.get('simulated') or account.get('simulated') else
                'possible' if account.get('state') in ('sent','unknown') and not row.get('response_received') else
                'submitted' if row.get('actual_model_submissions') else 'not_dispatched')
            self.model_wait_seconds+=time.monotonic()-started;write(self.out/f'attempt_{index}.json',row)

~~~~

## source/src/pr_next_joint/investigation/quantity_checks.py

~~~~python
"""Prove or leave open equality of recorded amount versions on one source path.

An equality result is a fact about accounting. It is not holder consent and
does not by itself establish either a vulnerability or a category exclusion.
This checker does not build transaction sequences or return input assignments.
"""
import hashlib

from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys
from pr_next_joint.verification.expressions import Unsupported
from pr_next_joint.verification.program_encoding import MechanismEncoder
from pr_next_joint.verification.sequence import qualify
from pr_next_joint.verification.solver import solve
from pr_next_joint.verification.source_worlds import encode_frame


def compare_gate(gate,expressions,frame,slot=0):
    signature=(gate['operator'],gate['operand_index'],key(qualify(gate['grant'],slot)),
               key(qualify(expressions[gate['quantity_expression']],slot)))
    for node in walk(frame['guards']):
        args=node.get('args',[])
        if len(args)!=2:continue
        i=gate['operand_index']
        if (node.get('op'),i,key(args[i]),key(args[1-i]))==signature:
            return True
    return False


def check_quantities(b,prop):
    matrix=[]
    cache=b.__dict__.setdefault('_accounting_equalities',{})
    dep=b.f.summaries.dependencies
    for use,identity in (prop.get('quantity_routes') or {}).items():
        rows=dep.amounts_for(use)
        if identity!=digest(rows):
            matrix.append({'operation':use,'result':'source_ir_mismatch'});continue
        for row in rows:
            for gate in row['allowance_gates']:
                holder=keys(gate['grant'])[gate['issuer_key']]
                for debit in row['deltas']:
                    if debit['sign']!='-' or debit['key_role']=='authorization_quantity' or key(debit['holder'])!=key(holder):
                        continue
                    a,c=debit['amount_expression'],gate['quantity_expression']
                    record={'operation':use,'target':b.f.operations[use]['target'],'path':row['path'],
                            'holder':holder,'ledger':debit['cell'],'issuer_spender_keys':keys(gate['grant']),
                            'debit_expression':a,'allowance_operand':c,'allowance_operator':gate['operator'],
                            'gate_operand_index':gate['operand_index'],'stage':'committed_source_path',
                            'semantics':'amount correspondence only; consent requires source-backed policy'}
                    token=digest([b.f.identity,record,prop['domain'],prop['initial_identity'],dep.identity])
                    if token in cache:
                        matrix.append(dict(cache[token],reused=True));continue
                    if b.remaining()<=0:
                        matrix.append(dict(record,result='not_executed',reason='shared_budget'))
                        return matrix
                    fr=b.source_frame(use,row['path'],0)
                    if not compare_gate(gate,dep.expressions,fr):
                        record.update(result='source_ir_mismatch',reason='allowance_key_operator_or_amount_version')
                    elif a==c:
                        record['result']='same_source_expression'
                    elif row['residuals']:
                        record.update(result='open',reason='relevant_path_has_unresolved_semantics')
                    elif b.remaining()<=0:
                        record.update(result='not_executed',reason='shared_budget')
                    else:
                        try:
                            e=MechanismEncoder(b.f.lookup(use))
                            frame_terms=encode_frame(e,fr)
                            da=e.expr(qualify(dep.expressions[a],0));ga=e.expr(qualify(dep.expressions[c],0))
                            solver=e.z.Solver()
                            solver.add(frame_terms,*e.constraints,*e.domain_constraints)
                            def check(s):
                                b.check()
                                return str(solve(s,initial_ms=max(1,min(b.f.options.solver_timeout_ms,int(b.remaining()*1000)))))
                            premise=check(solver)
                            record['premise']=premise
                            if premise=='sat':
                                solver.add(da!=ga)
                                answer=check(solver)
                                formula=solver.sexpr();ref=hashlib.sha256(formula.encode()).hexdigest()
                                b.formulas.setdefault(ref,{'sha256':ref,'text':formula,
                                    'scope_context':{'operation':use,'path':row['path'],'scope':'amount equality in single modeled frame'}})
                                record.update(answer=answer,formula_ref=ref,result={
                                    'unsat':'equal_on_modeled_path','sat':'equality_not_entailed'}.get(answer,'open'))
                            else:
                                record.update(result='open',reason='premise_'+premise)
                        except (Unsupported,TimeoutError) as error:
                            record.update(result='open',reason=str(error))
                    if record['result'] in ('same_source_expression','equal_on_modeled_path','equality_not_entailed'):
                        cache[token]=record
                    matrix.append(record)
    return matrix

~~~~
