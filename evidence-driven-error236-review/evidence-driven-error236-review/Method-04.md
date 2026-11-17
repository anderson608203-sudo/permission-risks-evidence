# 本批实际完整源码与运行器

源文件完整内容；Source ZIP保留原文件树和原字节。

## source/src/pr_next_joint/investigation/property_model.py

原文件SHA256 `8caa27bcee911b2c0802d569177f3c2e3977dd522aca0722eb1ae57b1c56940a`

```python
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
    rules = getattr(inv.semantics, 'rules', None)
    if rules and getattr(rules, 'bridges_at', None):
        links = sorted({identity for e in q['current'].get('_scope_effects',())
                        for identity in rules.bridges_at.get(e,())})
        if links:
            scope['decision']['source_edge_ids'] = links
    if q['current'].get('_audit_kind'):
        scope['decision']['audit_card'] = {
            'kind': q['current']['_audit_kind'], 'check': q['current']['_audit_check'],
            'bound_effects': list(q['current'].get('_scope_effects', ())),
            'source_relation_independent': bool(basis.get('source_relation')),
            'semantic_reading_used': bool(basis.get('semantic_local') and judgment == basis['status']),
        }
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

```

## source/src/pr_next_joint/investigation/protocol.py

原文件SHA256 `ff7bcb21c319c8df95e540ed9f252391dc5fe8de3cc3be6208e8c8764166941a`

```python
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
    audit = ('For an omitted effect or competing explanations use up to four hypotheses instead: '
             'effect_ref, source_refs (shown refs or qualified functions), issue_kind, actor_holder_relation, '
             'risk_explanation, normal_alternative, decisive_missing_fact, check_kind, requested_target_ref (nullable). '
             'issue_kind: new_sink/untrusted_sensitive_flow/role_write_to_use/authorization_scope/holder_consent_scope/'
             'financial_unit/gross_vs_net/lifecycle_stage/ordinary_transfer_route/privileged_state_difference/'
             'potential_normal_counterexample/unknown. check_kind: actual_call_reachability/untrusted_flow/guard_scope/'
             'role_write_to_use/allowance_scope/same_unit_net_effect/control_change_vs_outgoing/rollback_or_external_dep/none.')
    return ' '.join((common,direction,issue,audit,'Alternatively use annotations[{on,meaning,basis}] or policies[{effect,meaning,basis,subject?}] once.',
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

TOP_LISTS = frozenset(('annotations','policies','issues','answers','reviewed','hypotheses'))
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
    from .semantic_audit_card import parse as parse_card
    cards = []
    for idx, card in enumerate(value['hypotheses']):
        error = 'audit_card_limit' if idx >= 4 else parse_card(card)
        if error:
            diagnostics.append({'stage':phase, 'list':'hypotheses', 'index':idx, 'reason':error})
            bad = True
        else:
            cards.append(card)
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
    kind = 'substantive' if cards or issues or answers or any(seeds.values()) or has_reading else 'explicit_empty' if empty else 'unbound_content' if had_content and not recovered else 'invalid_protocol'
    for row in diagnostics:
        row.setdefault('stage',phase)
        if 'item' in row:row.setdefault('list','issues')
        if 'answer' in row:row.setdefault('list','answers')
    positions={field:[row_ordinals[(field,id(seed))] for seed in entries] for field,entries in seeds.items()}
    return {**seeds,'hypotheses':cards,'located_amount_reads':located_amount_reads,'issues':issues,'answers':answers,'reviewed':[x for x in reviewed if isinstance(x,str)],
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

```

## source/src/pr_next_joint/investigation/quantity_checks.py

原文件SHA256 `76494dba6b641ba95e676747c13fbececaef8582867bb370487c1fd1139a079f`

```python
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

```

## source/src/pr_next_joint/investigation/relations.py

原文件SHA256 `983c6600cac7be81deca4d0a36f12db2f78317c3c656b4c83e41026b4c402f30`

```python
"""Source-bound semantic relations shared by property formation and feedback."""
import copy
import re
from pr_next_joint.frontend.path_ir import key, op, lit, walk
from pr_next_joint.frontend.storage import keys, selectors, value_type
from .policy_binding import effect_duty, source_requirement, compile_requirement, compare_requirement, positive_role_reference


def statement(text, choice=None):
    """Preserve the asserted relation and its negation, not a risk-word score."""
    text = str(text or "").strip()
    label = str(choice or "").split(":", 1)[0].strip()
    negative = bool(re.search(
        r"\b(?:no unauthorized|not unauthorized|no wrongful|neither unauthorized|"
        r"not (?:an? )?(?:access.control|authorization) (?:bug|issue|violation)|"
        r"does not (?:permit|allow|grant|show|demonstrate).{0,35}(?:unauthorized|unqualified|takeover)|"
        r"not (?:an? )?unauthorized|cannot .{0,35}without (?:the )?authorization|"
        r"no .{0,20}takeover path)\b|不存在越权|并非越权", text, re.I))
    unknown = label == "unknown" or bool(re.search(r"\b(?:unclear|cannot determine|unknown whether)\b", text, re.I))
    normal = label == "normal_authorization" or negative
    return {
        "text": text, "meaning": "unknown" if unknown else "normal_authorization" if normal else "required_authorization",
        "polarity": "unresolved" if unknown else "denied_violation" if negative else "asserted",
        "relation_source": "source_anchored_model_explanation",
        "default_interpretation_only": not (label or normal or unknown),
        "guard_is_execution_fact_not_policy": True,
    }


def policy(item):
    text = item.get("policy_basis") or item.get("claim") or ""
    if not isinstance(text, str): return None
    if not text.strip() or item.get("_host_source_question"):
        return None
    scoped = bool(item.get('_opinion_message') and item.get('_scope_effects'))
    if scoped and item.get('policy_basis') and not effect_duty(text) and effect_duty(item.get('claim','')):
        text = item['claim']
    row = statement(text)
    if (item.get('assessment')=='normal' and row['meaning']!='unknown'
            and re.search(r"\b(?:own|self|msg\.sender.s)\b",text,re.I)
            and re.search(r"\b(?:checks?|subject to|self.service)\b",text,re.I)
            and not re.search(r'\b(?:bypass(?:es)?|unauthorized|without consent)\b',text,re.I)):
        row['meaning']='normal_authorization'
    row["source_anchors"] = copy.deepcopy(item.get("anchors", []))
    if scoped:
        row['localized_effect_opinion'] = True
    row["level"] = "H"
    return row


def _exact_name(text, name):
    return bool(name and re.search(r"(?<![\w$])" + re.escape(name) + r"(?![\w$])", text))


def bound_effect(inv, explanation, compiled):
    """Scope the query to this applied write. A sibling effect cannot witness it."""
    eid = explanation.get('binding_effect')
    if not eid:return compiled
    effect=inv.semantics.rules.effects[eid]
    compiled['binding_effect']=eid
    if 'write' in effect:
        compiled['effect_write']={'path':effect['path'],'version':effect['version'],'cell':effect['cell']}
    return compiled


def opinion_principals(inv, item, effect, duty):
    """Bind only the policy's actor to this target and this exact effect operand."""
    from .summary import holder
    lookup = inv.f.lookup(effect['oid'])
    bases = lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']])
    scoped = item.get('_opinion_subject')
    explicit = inv.semantics.rules.objects[scoped]['decl'] if scoped else None
    principals = []
    for phrase in duty['actors']:
        possessor = bool(re.search(r"\b(?:holder|depositor|owner of (?:the |their |this )?(?:account|balance|assets?|entitlement))\b|持有人|存款人", phrase, re.I))
        if possessor:
            operand = holder(effect['cell'], lookup) if 'cell' in effect else None
            relation = 'holder'
        else:
            slots = [node for node in lookup.decls.values()
                     if node.get('stateVariable') and node.get('scope') in bases and node.get('name')
                     and _exact_name(phrase.casefold(), node['name'].strip('_').casefold())]
            qualified = [n for n in slots if _exact_name(phrase.casefold(),
                         (lookup.nodes.get(n.get('scope'),{}).get('name','')+'.'+n['name']).casefold())]
            slots = qualified or slots
            if explicit is not None and any(n['id'] == explicit for n in slots):
                slots = [n for n in slots if n['id'] == explicit]
            operand = None
            relation = 'abstract' if not slots else 'ambiguous'
            if len(slots) == 1:
                cell = {'kind':'storage','root':slots[0]['id'],'segments':[]}
                typ = value_type(cell, lookup)
                if typ in ('address','address payable') or typ.startswith('mapping('):
                    operand = cell
                    relation = 'office'
        if explicit is not None and (operand or {}).get('id',(operand or {}).get('root')) != explicit:
            # A genuine abstract duty can use the explicitly shown source subject.
            # Never use that locator to replace a mismatching holder or named slot.
            if relation == 'abstract' and not possessor and explicit in lookup.nodes:
                cell = {'kind':'storage','root':explicit,'segments':[]}
                n = lookup.nodes[explicit]
                if n.get('stateVariable') and n.get('scope') in bases and value_type(cell,lookup) in ('address','address payable'):
                    operand, relation = cell, 'office'
                else:
                    relation = 'conflict'
            else:
                relation = 'conflict'
        principals.append((relation,operand))
    return principals


def authorization(inv, q, explanation, *, unresolved=None):
    if not isinstance(explanation, dict) or explanation.get("meaning") == "unknown":
        return None
    f = inv.f
    oid = inv.root(q)
    lookup = f.lookup(oid)
    mode=explanation.get('explicit_policy_kind')
    text = explanation.get("text", explanation.get("basis", ""))
    # Binding an intended policy is distinct from proving a committing path.
    # A known write before an unresolved call still identifies the issuer or
    # stage. The actual query separately retains that call's exit/residual.
    rows = [(pid,p) for pid,p in f.operation_paths(oid) if p['flow'] in ('normal','returned')]
    declaration = lookup.nodes.get(f.operations[oid]['source'].get('ast_id'), {})
    focused = explanation.get('source') == 'focused_model_answer'
    scoped = explanation.get('localized_effect_opinion', False) or (
        focused and q['current'].get('_opinion_message') and q['current'].get('_scope_effects'))
    duty = effect_duty((explanation.get('basis') if focused else None) or text) if scoped else None
    scoped_subject = None
    bound = {}
    if scoped and duty:
        rules = inv.semantics.rules
        bound = {e: opinion_principals(inv, q['current'], rules.effects[e], duty)
                 for e in q['current'].get('_scope_effects', ()) if rules.effects[e]['oid'] == oid}
        if bound and len({key(v) for v in bound.values()}) == 1:
            actors = next(iter(bound.values()))
            if len(actors) == 1 and actors[0][0] in ('office','holder') and actors[0][1] is not None:
                scoped_subject = actors[0]
    required = source_requirement(inv,q,explanation,rows) if not mode or mode=='current_authority_required' else None
    if scoped and required and duty and required['kind'] in ('source_role_payment_policy','source_grant_issuer','source_guarded_eligibility'):
        # A condition described in the behaviour clause is not a substitute
        # for consent by the specified principal.
        if not scoped_subject or key(required.get('subject', required.get('grant',{}).get('issuer'))) != key(scoped_subject[1]):
            required = None
    if required and required['kind']=='unresolved_role_payment_policy':
        if unresolved is not None:unresolved.add('role_payment_relation')
        return None
    if mode and required and required['kind']!='source_role_payment_policy':
        required=None
    if required:
        compiled = compile_requirement(required,explanation,lookup)
        match = compare_requirement(required,compiled,oid,declaration.get('id'),f.operations[oid]['target'])
        compiled['source_ir_check'] = match
        if not match['matches']:
            q['authorization_binding_diagnostic'] = {'reason':'source_ir_disagreement','comparison':match}
            return None
        return bound_effect(inv,explanation,compiled)
    if mode in ('current_authority_required','holder_authorization_applies','initialization_stage'):
        sub=explanation.get('qualified_cell')
        if not sub:return None
        predicate=op('!',sub) if mode=='initialization_stage' else op('==',{'kind':'actual_sender'},sub)
        return bound_effect(inv,explanation,{'predicate':predicate,'subject':sub,'kind':'scope_bound_'+mode,
                'property_family':'use','acquisition_uses':[],'source_bound_alternatives':[],
                'normal_alternatives':[],'binding':{'declaration':sub.get('root',sub.get('id')),'frame':'before_source_effect','source':f.operations[oid]['source']}})
    anchored = [o for o in q['binding']['operations'] if f.operations[o]['target'] == f.operations[oid]['target']]
    related = [p for o in anchored for _, p in f.operation_paths(o, True)]
    bases = set(lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']]))
    # A one-time initialization policy refers to its actual stage flag, not
    # to the new administrator supplied by this very call.
    if re.search(r'one.time|only.once|already initialized|after initialization',text,re.I):
        flags={w['path']['root']:w['path'] for _,p in rows for w in p['writes'] if
            not keys(w['path']) and value_type(w['path'],lookup)=='bool' and w['value']==lit(True) and
            _exact_name(text,lookup.nodes[w['path']['root']].get('name'))}
        if len(flags)==1:
            flag=next(iter(flags.values()))
            return {'predicate':op('!',flag),'subject':flag,'kind':'source_once_only_initialization',
                'property_family':'use','normal_alternatives':[],'source_bound_alternatives':[],
                'business_basis':explanation,'acquisition_uses':[],
                'binding':{'original_relation':text,'declaration':flag['root'],'frame':'before_initialization',
                           'source':lookup.anchor(lookup.nodes[flag['root']])}}
    # Enrollment of zero is meaningful only with the supplied downstream
    # recovery/membership relation. It is not a generic "zero address bug".
    if re.search(r'(?:malformed|invalid|bad|failed).{0,25}signature|signature.{0,35}(?:zero|address\(0\))',text,re.I):
        for _,p in rows:
            for w in p['writes']:
                ks=keys(w['path'])
                if len(ks)!=1 or ks[0].get('kind')!='parameter' or value_type(w['path'],lookup)!='bool' or w['value']!=lit(True):continue
                if not _exact_name(text,lookup.nodes[w['path']['root']].get('name')):continue
                uses=[]
                for use,entry in f.operations.items():
                    if entry['target']!=f.operations[oid]['target']:continue
                    for pid,up in f.operation_paths(use,True):
                        if any(c['root']==w['path']['root'] and any(t.get('kind')=='credential_recovery' or
                            t.get('kind')=='conditional' and t.get('when_true')==lit(0) for t in walk(keys(c)))
                            for c in selectors(up['guards'])):
                            uses.append({'operation':use,'path':pid,'authority':w['path']})
                if uses:
                    return {'predicate':op('!=',ks[0],lit(0)),'subject':ks[0],'kind':'valid_nonzero_signer_enrollment',
                        'property_family':'acquire','normal_alternatives':[],'source_bound_alternatives':[],
                        'business_basis':explanation,'acquisition_uses':uses,
                        'binding':{'original_relation':text,'declaration':w['path']['root'],'frame':'enrollment_then_signature_use',
                                   'source':w['source'],'zero_recovery_is_not_a_forged_valid_signature':True}}
    if explanation.get('meaning') == 'normal_authorization' and re.search(
            r'\bpublic payable\b|\bcaller\b.{0,35}\b(?:supplies|pays)\b.{0,25}(?:msg\.value|payment)',text,re.I):
        from .summary import debited_positions, local_delta, holder
        has_payment = any(v.get('kind') == 'transaction_value' for _,p in rows for v in walk([p['guards'],p['writes']]))
        own_credit = any(local_delta(w)[0] == '+' and key(holder(w['path'],lookup)) == key({'kind':'actual_sender'})
                         for _,p in rows for w in p['writes'])
        third_party_debit = any(x['holder'].get('kind') not in ('actual_sender','contract_address')
                                for x in debited_positions(f,oid))
        changes_authority = any(not keys(w['path']) and value_type(w['path'],lookup) in ('address','address payable')
                                for _,p in rows for w in p['writes'])
        if has_payment and own_credit and not third_party_debit and not changes_authority:
            payer = {'kind':'actual_sender'}
            return {'predicate':op('==',payer,payer), 'subject':payer, 'kind':'source_payer_self_acquisition',
                    'property_family':'use','normal_alternatives':[], 'source_bound_alternatives':[],
                    'business_basis':explanation,'acquisition_uses':[],
                    'binding':{'original_relation':text,'frame':'same transaction payer and recipient',
                               'payment':'actual msg.value','source':lookup.anchor(declaration)}}
    if scoped and (not scoped_subject or duty['qualified'] or len(bound) != 1):
        # Specialised policies above can stand independently. A source inventory,
        # an abstract duty or a compound condition cannot sign a guessed predicate.
        return None
    role_text = duty['actors'][0] if scoped else text
    cells = {key(c): c for p in related for c in selectors([p["guards"], p["writes"]])
             if not keys(c) and value_type(c, lookup) in ("address", "address payable")}
    # A missing authorization check may leave its intended authority entirely
    # absent from executable guards. Bind an explicitly named source declaration
    # in this applied storage layout as well; never invent an owner from a name
    # or pick a same-named declaration in another target.
    bases = set(lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']]))
    for declaration in lookup.decls.values():
        if not declaration.get('stateVariable') or declaration.get('scope') not in bases:
            continue
        cell = {'kind': 'storage', 'root': declaration['id'], 'segments': []}
        if value_type(cell, lookup) not in ('address', 'address payable'):
            continue
        owner_name = lookup.nodes.get(declaration.get('scope'), {}).get('name', '')
        if (_exact_name(role_text, declaration.get('name')) or
                _exact_name(role_text, owner_name + '.' + declaration.get('name', ''))):
            cells[key(cell)] = cell
    written = {w["path"]["root"] for _, p in rows for w in p["writes"]}
    downstream = []
    for use, entry in f.operations.items():
        if entry["target"] != f.operations[oid]["target"]:
            continue
        for pid, path in f.operation_paths(use, True):
            for guard in path['guards']:
                if any(v.get('kind') == 'actual_sender' for v in walk(guard)):
                    for c in selectors(guard):
                        if not keys(c) and value_type(c,lookup) in ('address','address payable'):
                            cells[key(c)] = c
            for c in selectors(path["guards"]):
                if c["root"] in written and not keys(c) and value_type(c, lookup) in ("address", "address payable"):
                    cells[key(c)] = c
                    downstream.append({"operation": use, "path": pid, "authority": c})
                elif c['root'] in written and keys(c):
                    from .key_roles import relation as source_key_role
                    role = source_key_role(c,lookup)
                    if role and role.get('kind') == 'authorization_quantity':
                        downstream.append({'operation':use,'path':pid,'authority':c})
    qualified, named = [], []
    for c in cells.values():
        n = lookup.nodes.get(c["root"], {})
        owner = lookup.nodes.get(n.get("scope"), {}).get("name")
        # A business explanation may qualify an inherited field by the
        # applied contract. Resolve that spelling through the actual C3 bases;
        # it still denotes the original declaration, not a fresh storage slot.
        qualifiers={lookup.nodes[b].get('name') for b in bases if n.get('scope') in
                    lookup.nodes[b].get('linearizedBaseContracts',[b])}
        if any(o and positive_role_reference(role_text,o+'.'+n.get('name','')) for o in qualifiers):
            qualified.append(c)
        elif positive_role_reference(role_text, n.get("name")):
            named.append(c)
    explicit = qualified or named
    modifier_subjects = []
    body = lookup.nodes.get(f.operations[oid]['source'].get('ast_id'), {})
    for call in body.get('modifiers', []):
        modifier = lookup.nodes.get(call.get('modifierName', {}).get('referencedDeclaration'), {})
        if not _exact_name(role_text, modifier.get('name')):
            continue
        roots = {n.get('referencedDeclaration') for n in walk(modifier) if isinstance(n,dict)}
        for _, path in rows:
            for guard in path['guards']:
                if not any(v.get('kind') == 'actual_sender' for v in walk(guard)):
                    continue
                modifier_subjects += [c for c in selectors(guard) if c['root'] in roots and not keys(c) and
                                     value_type(c,lookup) in ('address','address payable')]
    guard_subjects = re.findall(r"\b(?:checks|reads|requires)\s+([A-Za-z_$][\w$]*\.[A-Za-z_$][\w$]*)", role_text)
    exact_guard = [c for c in qualified if any(
        lookup.nodes.get(lookup.nodes[c['root']].get('scope'),{}).get('name','') + '.' + lookup.nodes[c['root']].get('name','') == n
        for n in guard_subjects)]
    subjects = re.findall(r"\b(?:only|required(?: by| from)?|authorized by|permission (?:of|from))\s+(?:(?:an?|the|authorized|existing)\s+)*'?([A-Za-z_$][\w.$]*)", role_text, re.I)
    described = [c for c in explicit if any(
        lookup.nodes[c["root"]].get("name") == s.split(".")[-1] for s in subjects)]
    candidates = list({key(c): c for c in modifier_subjects or exact_guard or described or explicit}.values())
    if len(candidates)>1 and not (modifier_subjects or exact_guard or described):
        # An explanation can mention a role and an unrelated bookkeeping
        # address with similar spelling. Resolve that ambiguity through the
        # actual caller guard, never through name case or the new written
        # value. This binds a proposed policy; it does not prove the policy or
        # authorize its current caller.
        used={};candidate_keys={key(c) for c in candidates}
        for use,entry in f.operations.items():
            if entry['target']!=f.operations[oid]['target']:continue
            for pid,path in f.operation_paths(use,True):
                for term in walk(path['guards']):
                    if term.get('op') not in ('==','!=') or len(term.get('args',[]))!=2:continue
                    a,b=term['args']
                    for caller,role in ((a,b),(b,a)):
                        if caller.get('kind')=='actual_sender' and key(role) in candidate_keys:
                            used.setdefault(key(role),[]).append({'operation':use,'path':pid,'guard':term})
        narrowed=[c for c in candidates if key(c) in used]
        if len(narrowed)==1:
            q['authorization_relation_disambiguation']={'candidates':copy.deepcopy(candidates),
                'selected':copy.deepcopy(narrowed[0]),'source_guard_uses':used[key(narrowed[0])],
                'basis':'the proposed source fields have one actual caller-qualification use',
                'binding_frame':'before_effect','policy_truth_not_inferred_from_guard':True}
            candidates=narrowed
    if not scoped and subjects and not described and not modifier_subjects and not exact_guard and not qualified and any(
            s.lower() in ('owner','handler','admin','administrator','controller') for s in subjects):
        q['authorization_binding_diagnostic']={'reason':'described_authority_has_no_matching_source_declaration',
            'described_subjects':subjects,'mentioned_state_is_not_automatically_the_authority':True}
        return None
    kind = "authority_before_effect"
    if scoped_subject is not None:
        relation, subject = scoped_subject
        if relation == 'holder':
            kind = 'entitlement_holder'
        elif value_type(subject,lookup) not in ('address','address payable'):
            return None
    elif len(candidates) == 1:
        subject = candidates[0]
    elif not candidates and re.search(r"\b(?:holder|depositor|owner of (?:the )?(?:balance|asset)|spender|allowance)\b|持有人|存款人", text, re.I):
        from .summary import debited_positions
        hs = {key(x["holder"]): x["holder"] for x in debited_positions(f, oid)}
        if not hs:
            from .key_roles import relation as source_key_role
            for _,p in rows:
                for w in p['writes']:
                    relation = source_key_role(w['path'],lookup)
                    if relation and relation.get('kind')=='authorization_quantity':
                        h=keys(w['path'])[relation['holder_key']];hs[key(h)]=h
            if hs:kind='source_grant_issuer'
        if len(hs) != 1:
            return None
        subject = next(iter(hs.values()))
        if kind != 'source_grant_issuer':kind = "entitlement_holder"
    else:
        q["authorization_binding_diagnostic"] = {
            "reason": "authorization_subject_not_uniquely_source_bound", "candidates": candidates, "text": text}
        return None
    caller = {"kind": "actual_sender"}
    allow = [op("==", caller, subject)]
    from .authorization_normal import numeric_delegations, payment_qualification
    alternatives = numeric_delegations(inv, oid, subject, explanation) + payment_qualification(inv, q, subject)
    if scoped and kind == 'entitlement_holder':
        from .source_opinion import covered_delegation
        per_effect = [f.summaries.paths[r['path']] for r in (inv.semantics.rules.effects[e] for e in bound) if 'path' in r]
        if not per_effect or not covered_delegation(inv, oid, per_effect):
            alternatives = []
    if kind == 'entitlement_holder' and subject.get('kind') != 'actual_sender' and re.search(r'\b(?:allowance|quota|grant)\b',text,re.I):
        from .key_roles import relation as source_key_role
        gates = [c for _,p in rows for c in selectors(p['guards']) if
                 (source_key_role(c,lookup)or{}).get('kind')=='authorization_quantity']
        if gates and not alternatives:
            q['authorization_binding_diagnostic']={'reason':'holder_grant_provenance_not_established',
                'gates':gates,'holder':subject,'source_text':text,
                'cannot_default_to_holder_only_and_report_normal_spending_as_a_violation':True}
            return None
    allow.extend(x["predicate"] for x in alternatives)
    def requires_owner(guard):
        if guard.get('op') in ('and','&&'):
            return any(requires_owner(g) for g in guard['args'])
        return (guard.get('op') == '==' and
                {key(x) for x in guard.get('args',[])} == {key(caller), key(subject)})
    office_alternative_paths = [] if scoped and kind == 'entitlement_holder' else rows
    for _, path in office_alternative_paths:
        for term in walk(path['guards']):
            if term.get('op') != '==' or not any(x.get('kind') == 'actual_sender' for x in term.get('args',[])):
                continue
            for cell in selectors(term):
                if keys(cell) or key(cell) == key(subject) or value_type(cell,lookup) not in ('address','address payable'):
                    continue
                writers = [w for w in f.writes.values() if w['raw']['path']['root'] == cell['root'] and
                           f.operations[w['operation']]['target'] == f.operations[oid]['target'] and
                           w['raw']['value'].get('value') not in (0,False)]
                if writers and all(f.paths[w['path']]['raw']['flow'] in ('normal','returned') and
                                   not f.paths[w['path']]['raw'].get('issues') and
                                   any(requires_owner(g) for g in f.paths[w['path']]['raw']['guards']) for w in writers):
                    allow.append(op('==',caller,cell))
                    alternatives.append({'predicate': op('==',caller,cell),
                                         'kind':'source_owner_protected_nomination','source_paths':[w['path']for w in writers]})
    for _, path in office_alternative_paths:
        for term in selectors(path["guards"]):
            ks = keys(term)
            if value_type(term, lookup) != "bool" or len(ks) != 2:
                continue
            writers = [w for w in f.writes.values() if w["raw"]["path"]["root"] == term["root"] and
                       f.operations[w["operation"]]["target"] == f.operations[oid]["target"]]
            if (writers and all(keys(w["raw"]["path"]) and keys(w["raw"]["path"])[0].get("kind") == "actual_sender" for w in writers)
                    and key(ks[0]) == key(subject) and ks[1].get("kind") == "actual_sender"):
                allow.append(term)
    acquisition_intent = bool(re.search(r"\b(?:grant|gain|acquir\w*|becom\w*|takeover|install|replac\w*).{0,45}(?:owner|authority|role|withdraw right)", text, re.I))
    acquisition = [r for r in downstream if r["operation"] != oid and (
        r["authority"]["root"] == subject.get("root") or acquisition_intent or
        kind == 'source_grant_issuer' and r['authority']['root'] in written)]
    result = {"predicate": op("or", *list({key(x): x for x in allow}.values())),
            "subject": subject, "kind": kind, "normal_alternatives": allow[1:],
            "source_bound_alternatives": alternatives, "business_basis": explanation,
            "acquisition_uses": acquisition, "property_family": "acquire" if acquisition or acquisition_intent else "use",
            "binding": {"original_relation": text, "declaration": subject.get("root"), "frame": "before_effect",
                        "source": lookup.anchor(lookup.nodes[subject["root"]]) if subject.get("root") in lookup.nodes else None}}

    if scoped and len(bound) == 1:
        return bound_effect(inv, {'binding_effect':next(iter(bound))}, result)
    return result


def beneficiary_condition(encoder, frame, position, holder, *, controller_frame=None):
    """Conditional ability with all original source address restrictions."""
    requester=encoder.expr(frame["caller"])
    caller=encoder.expr((controller_frame or frame)["caller"])
    if holder.eq(caller):
        return holder == caller, {"kind": "self", "conditional": False}
    selectable = any(k.get("kind") == "parameter" and k.get("type") in ("address", "address payable") for k in keys(position))
    if selectable and getattr(encoder.lookup, "analysis_scope", None) == "FCR":
        from pr_next_joint.verification.sequence import qualify
        selected = [qualify(k,frame['slot']) for k in keys(position) if k.get('kind') == 'parameter']
        def conjuncts(g):
            return [x for a in g['args'] for x in conjuncts(a)] if g.get('op') in ('and','&&') else [g]
        fixed = [g for guard in frame['guards'] for g in conjuncts(guard) if g.get('op') == '==' and
                 any(key(x)==key(p) for x in g.get('args',[]) for p in selected) and
                 any(x.get('kind') in ('storage','literal','contract_address') for x in g.get('args',[]))]
        if fixed:
            return holder == caller, {'kind':'source_fixed_beneficiary_requires_established_control',
                                       'restrictions':fixed,'arbitrary_recipient_control_not_assumed':True}
        # Only the actual caller of the crediting entry chooses its arguments.
        # A separate ordinary buyer does not choose on behalf of the setter.
        controlled=encoder.z.Or(holder==caller,encoder.z.And(requester==caller,holder!=0))
        return controlled, {"kind": "selectable_self_controlled_address",
                             "conditional": True, "source_restrictions_in_frame": True,
                             "not_arbitrary_observed_recipient_control": True}
    return holder == caller, {"kind": "self_only_without_third_party_control_source",
                              "other_beneficiary_control_unestablished": True}


def source_violation(inv, q, prop):
    """A small source theorem, not a second business detector or SMT fallback.

    An unguarded scalar-role assignment can give the requester an authority
    whose actual source use has exactly that role guard and a freely selectable
    address update. The same compiled policy is needed; no policy is invented
    from a Solidity field name. All other shapes go to the ordinary backend.
    """
    expected = ((prop or {}).get('expected_authorization') or {}).get('compiled_authorization') or {}
    subject = expected.get('subject') or {}
    if (prop.get('task') != 'AC' or expected.get('property_family') != 'acquire' or
            expected.get('competing_interpretations') or expected.get('normal_alternatives') or
            subject.get('kind') != 'storage' or keys(subject)):
        return None
    caller = {'kind':'actual_sender'}
    if key(expected.get('predicate')) != key(op('or',op('==',caller,subject))):
        return None
    root = inv.root(q); f = inv.f
    if value_type(subject,f.lookup(root)) not in ('address','address payable'):
        return None
    for pid,path in f.operation_paths(root,True):
        if any(g != lit(True) for g in path['guards']) or path.get('evaluated_terms') or path.get('sensitive_effects'):
            continue
        granting = [w for w in path['writes'] if key(w['path']) == key(subject) and
                    (w['value'].get('kind') == 'actual_sender' or
                     w['value'].get('kind') == 'parameter' and w['value'].get('type') in ('address','address payable'))]
        if not granting:
            continue
        # Side expressions cannot hide a revert/constraint from this proof.
        if any(w['value'].get('kind') not in ('parameter','actual_sender','literal') for w in path['writes']):
            continue
        for use in expected.get('acquisition_uses',[]):
            p = f.paths[use['path']]['raw']
            if p.get('issues') or p.get('evaluation_gaps') or p.get('evaluated_terms') or p.get('sensitive_effects'):
                continue
            def role_guard(g):
                if g == lit(True):return True
                if g.get('op') in ('and','&&'):return all(role_guard(x) for x in g['args'])
                return g.get('op') == '==' and {key(x) for x in g['args']} == {key(caller),key(subject)}
            if not p['guards'] or not all(role_guard(g) for g in p['guards']):
                continue
            updates = [w for w in p['writes'] if not keys(w['path']) and
                       value_type(w['path'],f.lookup(use['operation'])) in ('address','address payable') and
                       w['value'].get('kind') == 'parameter' and w['value'].get('type') in ('address','address payable')]
            if not updates:
                continue
            return {'kind':'source_property_certificate','operation':root,'property_identity':prop['id'],
                    'property_validated':True,'level':'P','supports':'authorization_violation',
                    'source_paths':[pid,use['path']], 'authority':subject, 'grant':granting,
                    'actual_authority_use':use,'productive_update':updates,
                    'source_constraints':{'old_authority_and_requester':'different nonzero address values exist',
                        'grant_argument':'the requester when present',
                        'use_actor':'same requester after the real grant',
                        'use_update':'a free address argument distinct from its previous stored value'},
                    'proof':'straight-line typed address assignment; exact subsequent role equality; actual free address update',
                    'not_a_full_SMT_or_EVM_execution':True,'queries':[]}
    return None

```

## source/src/pr_next_joint/investigation/report.py

原文件SHA256 `91460185d78cefe201ee1984763458089080dd3d3abf1648445e3192eeb9da19`

```python
"""Source-backed risk prediction, scoped hard counterevidence and dependency output."""
import copy,re
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import walk,key
from pr_next_joint.frontend.storage import selectors,keys,value_type,selector_relation
from .contracts import VERSION,CATEGORIES
from .protocol import category_scope
from .request_scope import coverage_facts, observation_applies, compare_relevant, linked_controls



def evaluate(inv,q):
    from .property_model import compose
    from .source_opinion import reading_version
    inv.semantics.scope(q['current'])
    prop=q.get('property') or {}
    stamp=(q['version'],prop.get('id'),tuple(q['evidence']),bool(q.get('task_conflict')),
           q.get('retired_property_parent'),tuple(sorted(q.get('office_effects',{}).items())),
           tuple(q.get('effect_scope',())),len(q.get('observations',())),reading_version(inv,q['binding']['operations'],prop.get('category')))
    cached=q.get('_composed_snapshot')
    if not cached or cached[0]!=stamp:
        cached=(stamp,compose(inv,q,None));q['_composed_snapshot']=cached
    return cached[1]

def reading_scope(inv,blocked,assessments=None):
    from .coverage import obligation_scope
    assessments=assessments or {qid:evaluate(inv,q) for qid,q in inv.issues.items()}
    return obligation_scope(inv,assessments,blocked)



def build(inv):
    findings={};records=[];suppressed=[];decisive_records=[];blocked_categories=set();assessments={}
    for qid,q in sorted(inv.issues.items()):
        assessment=evaluate(inv,q);assessments[qid]=assessment;item=q['current'];records.append({'id':qid,'version':q['version'],
            'current':copy.deepcopy(item),'history':copy.deepcopy(q['history']),'binding':q['binding'],
            'distinguishing_plan':copy.deepcopy(q.get('plan')),'claim_source_scope':copy.deepcopy(q['claim_source_scope']),
            'task_conflict':q.get('task_conflict',False),'semantic_task_review':copy.deepcopy(q.get('task_review')),
            'compiled_property':copy.deepcopy(q.get('property')),'semantic_answers':copy.deepcopy(q.get('semantic_answers',[])),
            'assessment_result':assessment,'evidence_refs':q['evidence'],'revision_evidence':q['revision_evidence'],
            'scoped_observations':copy.deepcopy(q.get('observations',[])),
            'source_observation_reuse':copy.deepcopy(q.get('source_decisions',[]))})
        decision=assessment['scope']['decision']
        if decision['status'] in ('risk','normal','excluded') and not q.get('task_conflict'):
            decisive_records.append(qid)
        mapping=assessment['scope'].get('comparison_alignment',{})
        if decision['status']!='risk':
            if item['assessment']=='risk':suppressed.append({'issue':qid,'reasons':assessment['reasons']})
            continue
        oid=assessment['root'];o=inv.f.operations[oid]
        location=copy.deepcopy(o['source']);anchor=q['binding'].get('core_anchor') or inv.catalog.name(oid);fine=False
        if anchor in inv.catalog.label_locations:location=copy.deepcopy(inv.catalog.label_locations[anchor]);fine=True
        else:
            m=re.fullmatch(r'(.+\.sol):(\d+)(?:[-:](\d+))?',anchor)
            if m and m[1] in inv.catalog.sources:
                chunks=inv.catalog.sources[m[1]]['content'].encode().splitlines(keepends=True);lo=int(m[2]);hi=int(m[3] or lo)
                start=sum(map(len,chunks[:lo-1]));end=sum(map(len,chunks[:hi]));location={'file':m[1],'start':start,'length':end-start};fine=True
        # Conservative source-root grouping. Do not equate different unlocated
        # business mechanisms merely because they share a variable/function.
        precise=assessment['scope'].get('decision',{}).get('locations',[])
        cause_location=assessment['scope']['decision'].get('causal_root')
        if cause_location:
            location=copy.deepcopy(cause_location);fine=True
        elif len(precise)==1 and precise[0].get('start') is not None and not fine:
            location=copy.deepcopy(precise[0]);fine=location!=o['source']
        effective=assessment['scope']['decision']
        # One actual incumbent replacement has the same cause whether policy was
        # stated in an issue, supplied as a scoped seed, or independently inferred.
        scoped_role=effective['reason']=='source_role_reassignment' and effective.get('effects') and 'current_authority_required' in effective.get('meanings',())
        if effective.get('opinion_source') and effective.get('effects'):
            cause=['located_effect',sorted(effective['effects']),item.get('phase'),item.get('actor'),item.get('subject')]
        elif scoped_role:
            cause=['incumbent_replacement',sorted(effective['effects']),item.get('phase'),item.get('scope'),item.get('assumptions') or []]
        else:
            cause=[assessment['scope'].get('claim_identity'),item.get('object'),item.get('actor'),
                   item.get('phase'),item.get('scope'),item.get('assumptions'),effective.get('effects',[])]
        identity=[inv.f.identity,assessment['category'],o['target'],location,cause]
        fid='finding_'+digest(identity)[:20]
        f=findings.setdefault(fid,{'id':fid,'category':assessment['category'],'target':o['target'],
            'root_location':location,'root_cause':{'operation':oid,'source_anchors':[location]},
            'operation':oid,'function':o['function'],'related_operations':q['binding']['operations'],
            'actor':item.get('actor'),'object':item.get('object'),'mechanism':assessment.get('composed_claim',item['claim']),
            'original_model_claim':item['claim'],'original_model_assessment':item['assessment'],
            'normal_explanation_considered':item.get('alternative'),'scope':assessment['scope'],
            'assumptions':item.get('assumptions',[]),'evidence_level':assessment.get('evidence_level','source_prediction'),
            'comparison_scope':mapping.get('status','main'),'formal_risk_query_required':False,'evidence_refs':[],'issue_ids':[]})
        f['evidence_refs']=sorted(set(f['evidence_refs']+q['evidence']));f['issue_ids'].append(qid)
    scope=reading_scope(inv,blocked_categories,assessments)
    blocked_categories={c for gap in scope['known_category_gaps'] for c in gap.get('affected_categories',[])}
    from pr_next_joint.reporting.effective_parameters import investigation_profile
    return {'effective_investigation_parameters':investigation_profile(inv.f.options),'method':VERSION,'program_identity':inv.f.identity,'task':inv.f.options.scope,'options':inv.f.options.record(),
        'implementation_sha256':inv.f.context['implementation_sha256'],
        'findings':list(findings.values()),'main_finding_ids':[k for k,v in findings.items() if v['comparison_scope']=='main'],
        'additional_finding_ids':[k for k,v in findings.items() if v['comparison_scope']=='additional'],
        'unresolved_mapping_ids':[k for k,v in findings.items() if v['comparison_scope']=='unresolved'],'inspection_records':records,
        'diagnostics':{'issues':inv.diagnostics,'unexecuted_actions':copy.deepcopy(inv.ready),
            'suppressed_source_predictions':suppressed,'program_gaps':copy.deepcopy(inv.f.gaps),
            'source_context_scope':inv.initial_manifest,'no_finding_is_not_contract_safety':True,
            'E1_not_formal_FREEZE':True},
        'model_analysis_available':inv.model_analysis_available,
        'prediction_basis_available':bool(findings or scope['negative_eligible_categories'] or decisive_records),
        'prediction_basis_issues':decisive_records,'unresolved_category_judgments':sorted(blocked_categories),
        'task_analysis':{'model_analysis_available':inv.model_analysis_available,'fixture_analysis_available':getattr(inv,'fixture_analysis_available',False),'usable_task_opinion':inv.usable_task_opinion,
            'empty_response_present':inv.explicit_empty_analysis,
            'explicit_empty_task_reading':bool(inv.explicit_empty_analysis and scope['whole_reading_eligible']),
            'model_declaration':inv.task_declaration,'reading_scope':scope,'local_judgment_not_global_safety':True,
            'unexecuted_actions':len(inv.ready),'task_conflicts':[qid for qid,q in inv.issues.items() if q.get('task_conflict')]},
        'model_reading_declarations_not_proof':inv.reading_declarations,
        'usage':{'attempts':copy.deepcopy(inv.session.attempts),**inv.session.accounting()},
        'provenance':{'refinement_decisions':copy.deepcopy(inv.refinements),'structural_references':{k:v['structural'] for k,v in inv.shared_reads.items() if v['result'] is not None},'shared_source_facts':{k:sorted(v['consumers']) for k,v in inv.shared_reads.items() if v['result'] is not None},'source_candidate_investigations':copy.deepcopy(getattr(inv,'candidate_trace',[])),'actions':copy.deepcopy(inv.actions),'revisions':copy.deepcopy(inv.updates),
            'evidence_labels':sorted(inv.evidence),'feedback_trace':copy.deepcopy(inv.feedback_trace),'cache_hits':inv.backend.cache_hits,
            'computation_reuse':copy.deepcopy(inv.backend.cache_stats),'model_call_decisions':copy.deepcopy(inv.call_decisions),
            'mechanism_attribution_not_a_new_detection_admission_gate':True},
        'prediction_frozen_before_gold':True,'scoring_performed':False,
        'risk_absence_statement':'No risk detected in the actual analyzed source scope; not proof of safety.'}

def evaluation_projection(report):
    """No Gold access, scoring or legacy query gate. Preserve positive source predictions."""
    cats=('AC',) if report['task']=='AC' else CATEGORIES[1:]
    found={f['category'] for f in report['findings'] if f.get('comparison_scope','main')=='main'}
    unknown=set(report.get('unresolved_category_judgments',[]))
    task=report.get('task_analysis',{});reading=task.get('reading_scope',{})
    # Archived reports retain their original projection; new reports carry prospective eligibility.
    if 'reading_scope' in task:
        eligible=set(reading['negative_eligible_categories'])
    else:
        eligible=set()
        unknown.update(set(cats) - found)
    obligations=reading.get('obligations',[])
    active=bool(report.get('model_analysis_available') or obligations or found or report.get('inspection_records'))
    if reading.get('schema') not in ('source-category-decision-r1','source-category-public-r1') and not obligations:eligible.clear()
    if report.get('method') in (VERSION,'permission-risks-semantic-propagation-r2','permission-risks-source-prediction-integration-r1','permission-risks-next-decision-only-r2'):
        states={c:'alarm' if c in found else 'not_run' if not active else
                'not_detected' if c in eligible and c not in unknown else 'unsupported' for c in cats}
    else:
        states={c:'alarm' if c in found else 'unsupported' if c in unknown else
                'not_detected' if c in reading.get('negative_eligible_categories',[]) else 'not_run' for c in cats}
    return {'predictions':states,
        'scope':report['diagnostics']['source_context_scope'],
        'coverage_basis':('Source opinions and actual scoped reading; optional refinement is independent.' if report.get('method') in (VERSION,'permission-risks-semantic-propagation-r2','permission-risks-source-prediction-integration-r1') else 'Finite source obligations, actual semantic/program completion and scoped residuals; delivery/declarations are records, not completion gates.'),
        'no_finding_does_not_prove_safety':True,'not_a_score':True,
        'enhancement_unfinished_does_not_erase_source_predictions':True}

```

## source/src/pr_next_joint/investigation/request_scope.py

原文件SHA256 `756330123ee084b1e802e36698d1936dbb089a348121df6485a73306cbc9f6c2`

```python
"""Bind an investigation to program uses named in the claim, separately from its finding anchor."""
import re

from pr_next_joint.frontend.path_ir import key, walk
from .roles import path_qualification
from pr_next_joint.frontend.storage import keys, selectors, selector_relation, value_type


def unique_cells(cells):
    return list({key(cell): cell for cell in cells}.values())


def use_reads(path):
    # A destination on the left of an assignment is not a read of its old value.
    values = [w['value'] for w in path['writes']]
    positions = [keys(w['path']) for w in path['writes']]
    return selectors([path['guards'], values, positions, path.get('sensitive_effects', []),
                      path.get('return_value'), path.get('evaluated_terms', [])])


def claim_entries(inv, binding, item):
    root = binding.get('core_operation')
    if not root:
        return set()
    operations = inv.f.operations
    target = operations[root]['target']
    applied = [[oid for oid in ids if operations[oid]['target']==target] for ids in binding['located'].values()]
    located = {ids[0] for ids in applied if len(ids)==1}
    wording = ' '.join(str(item.get(k, '')) for k in ('claim', 'distinguish', 'distinguishing_question'))
    tokens = set(re.findall(r'\b([A-Za-z_$][\w$]*)\s*\(', wording))
    by_name = {}
    for oid, op in operations.items():
        if op['target'] == target:
            by_name.setdefault(op['function'].split('(')[0], []).append(oid)
    # Use the already bound target. A bare overloaded name cannot nominate a use.
    located.update(ids[0] for name, ids in by_name.items() if name in tokens and len(ids) == 1)
    return {root} | {oid for oid in located if operations[oid]['target'] == target}


def holder_effect(inv, oid):
    # Shape of a possible effect, not a judgment that a mapping is a financial right.
    for _, path in inv.f.operation_paths(oid, True):
        if any(fx.get('kind') == 'native_transfer' for fx in path.get('sensitive_effects', [])):
            return True
        for w in path['writes']:
            cell = w['path']
            if keys(cell) and value_type(cell, inv.f.lookup(oid)).startswith(('uint','int')):
                return True
    return False


def linked_controls(inv, change, use):
    writes = [w['path'] for _, p in inv.f.operation_paths(change, True) for w in p['writes']]
    return [cell for cell in inv.graph.request_reads(use) if any(
        selector_relation(cell, w) == 'same_shape' and not inv.graph._disjoint_keys(cell, w) for w in writes)]


def request_target(inv, binding, item, plan, measure):
    """Resolve a claim endpoint before evaluating Boolean predictions on it."""
    root = binding['core_operation']
    claimed = claim_entries(inv, binding, item)
    request = item['observation']
    hint = item.get('next_check')
    hint = hint if isinstance(hint, dict) else {}
    at = request.get('at')
    after = request.get('after')
    target=inv.f.operations[root]['target']
    at_ids=[i for i in inv.catalog.resolve(at) if inv.f.operations[i]['target']==target] if at else []
    after_ids=[i for i in inv.catalog.resolve(after) if inv.f.operations[i]['target']==target] if after else []
    if at and (len(at_ids) != 1 or at_ids[0] not in claimed):
        return None, [], 'observation_entry_outside_or_ambiguous_in_claim'
    if after and (len(after_ids) != 1 or inv.f.operations[after_ids[0]]['target'] != inv.f.operations[root]['target']):
        return None, [], 'intervention_target_ambiguous_or_different'
    pairs = plan['selected_pairs'] + plan['deferred_pairs']
    downstream = list(dict.fromkeys(p['observe'] for p in pairs if p['change'] == root
                                     and p['observe'] != root and p['observe'] in claimed))
    # A financial effect must not silently become a setter's authorization guard.
    if inv.f.options.scope == 'FCR':
        downstream = [u for u in downstream if holder_effect(inv, u)]
    preferred = at_ids or (inv.catalog.resolve(hint.get('observe')) if hint.get('action') == 'compare' else [])
    if len(preferred) == 1 and preferred[0] in downstream:
        downstream.remove(preferred[0])
        downstream.insert(0, preferred[0])
    if at_ids and at_ids[0] != root and at_ids[0] not in downstream:
        return None, downstream, 'no_source_dependency_from_claim_to_requested_use'
    if at_ids == [root]:
        use = root
    elif downstream and (measure not in ('holder_grant','holder_net') or
                         after_ids == [root] or at_ids or not holder_effect(inv, root)):
        use = downstream[0]
    else:
        use = root
    if inv.f.options.scope == 'FCR' and measure in ('opens','blocks') and not holder_effect(inv, use):
        return None, downstream, 'no_claimed_holder_request; role_evidence_only'
    if use == root and measure in ('opens','blocks') and inv.f.options.scope == 'FCR':
        # No invented upstream administrator as a financial intervention.
        if not any(p['observe'] == root and p['change'] in claimed and p['change'] != root for p in pairs) and not after_ids:
            return None, downstream, 'no_identified_intervention_on_holder_request'
    return use, downstream, None


def select_controls(inv, use, candidates, request, item):
    candidates = unique_cells(candidates)
    name = request.get('control')
    if name:
        if not isinstance(name, str):
            return []
        return [c for c in candidates if name in (inv.backend._storage_name(use, c),
                    inv.f.lookup(use).nodes.get(c['root'], {}).get('name'))]
    # Preserve explicit ordered keys in natural-language claims, including this vs msg.sender.
    text = re.sub(r'\s*([.\[\]])\s*', r'\1', str(item.get('claim','')))
    indexed = [c for c in candidates if keys(c) and re.search(
        r'(?<![\w$])' + re.escape(inv.backend._storage_name(use,c)) + r'(?![\w$\[])', text)]
    return indexed or candidates


def compare_relevant(inv, q, evidence):
    root = inv.root(q)
    change, use = evidence.get('change'), evidence.get('observe')
    if not root or not change or not use:
        return False
    choice = q.get('plan', {}).get('observation_choice') or {}
    resolution = choice.get('request_resolution')
    if not resolution:
        if inv.f.options.scope == 'FCR' and use == root and not holder_effect(inv,root):
            # A legacy upstream qualifier is contextual only when a separately
            # sourced downstream holder request is the subject of this claim.
            if any(u != root and holder_effect(inv,u) and linked_controls(inv,root,u)
                   for u in claim_entries(inv,q['binding'],q['current'])):
                return False
        return True
    if resolution['use'] is None and inv.f.options.scope == 'FCR':
        hint=q['current'].get('next_check')
        claimed=use in claim_entries(inv,q['binding'],q['current'])
        scoped_probe=isinstance(hint,dict) and hint.get('action')=='compare' and inv.catalog.resolve(hint.get('change'))==[change] and inv.catalog.resolve(hint.get('observe'))==[use]
        return change==root and holder_effect(inv,use) and (claimed or scoped_probe and bool(linked_controls(inv,change,use)))
    selected=choice.get('selected')
    if selected and selected['measure'] in ('direct_effect','denied_qualified','missing_control','ledger_receipt','ledger_debit','ledger_grant'):
        return (evidence.get('observed_measure'),change,use)==(selected['measure'],selected['change'],selected['observe'])
    if resolution['use'] != root:
        return change == root and use == resolution['use']
    if inv.f.options.scope == 'FCR' and use != root:
        return False
    return True


def observation_applies(inv, q, result):
    pick = (q.get('plan', {}).get('observation_choice') or {}).get('selected')
    if not pick or pick['observe'] != result['observe'] or pick['change'] != result['change']:
        return False
    return (pick['measure'] == result['measure'] and pick['scope'] == result['scope']
            and pick['context'] == result.get('request_context', pick['context'])
            and pick.get('expectations') == result.get('expectations'))


def account_term(term, lookup):
    if term.get('kind') in ('actual_sender','transaction_origin'):
        return True
    return term.get('kind') == 'storage' and not term.get('segments') and value_type(term, lookup) in ('address','address payable')


def positive_caller_gate(node, lookup):
    if node.get('op') in ('and','&&'):
        return any(positive_caller_gate(v, lookup) for v in node.get('args', []))
    args = node.get('args', [])
    if node.get('op') == '!' and len(args) == 1 and args[0].get('op') == '!=':
        args = args[0]['args']
    elif node.get('op') != '==':
        return False
    return (len(args) == 2 and any(x.get('kind') == 'actual_sender' for x in args) and
            any(x.get('kind') == 'storage' and account_term(x, lookup) for x in args))


def privileged_intervention(inv, binding, item):
    """Scope an explicit mixed actor claim to a real guarded writer and dependent use."""
    if not binding.get('core_exact') or item.get('category') not in (
            'FCR-TRANSFER','FCR-MINT','FCR-DESTROY','FCR-PAUSE','FCR-FREEZE'):
        return []
    claimed = claim_entries(inv, binding, item)
    root = binding['core_operation']
    links = []
    for writer in sorted(claimed):
        paths = list(inv.f.operation_paths(writer, True))
        if not inv.backend.complete(writer) or not paths or not all(
                path_qualification(inv.f,writer,path) for _, path in paths):
            continue
        for use in sorted(claimed - {writer}):
            if root not in (writer,use) or not holder_effect(inv, use):
                continue
            controls = linked_controls(inv, writer, use)
            if controls:
                links.append({'change':writer,'use':use,'controls':controls,'status':'source_dependency_not_proof_of_harm'})
    return links


def opaque_paths(inv, oid):
    """An incomplete effect or actual external dependency cannot certify a local exclusion."""
    if inv.f.operations[oid].get('generated_getter'):
        return False
    if not inv.backend.complete(oid):
        return True
    for pid, path in inv.f.operation_paths(oid, True):
        deps = inv.backend.condition_dependencies(oid, pid, path)
        if deps['unknown_dependencies'] or deps['credential_dependencies']:
            return True
        if any(effect.get('kind') != 'native_transfer' for effect in path.get('sensitive_effects', [])):
            return True
    return False


def bounded_availability_scope(inv, q):
    """Limit an existing availability question only when the control changes admission alone."""
    item = q['current']
    if inv.f.options.scope != 'FCR' or item.get('category') != 'AC':
        return None
    obs = item.get('observation') or {}
    if not isinstance(obs,dict) or obs.get('measure') != 'blocks' or not q['binding'].get('core_exact'):
        return None
    if q['binding'].get('ambiguous') or q['binding'].get('unresolved'):
        return None
    root = inv.root(q)
    if opaque_paths(inv, root) or not any(inv.evidence[k].get('operation') == root
            and inv.evidence[k]['kind'] == 'source_inspection' for k in q['evidence']):
        return None
    cells = unique_cells(w['path'] for _,p in inv.f.operation_paths(root,True) for w in p['writes'])
    if len(cells) != 1 or value_type(cells[0],inv.f.lookup(root)) != 'bool':
        return None
    if any(p.get('sensitive_effects') for _,p in inv.f.operation_paths(root,True)):
        return None
    target = inv.f.operations[root]['target']
    claimed = claim_entries(inv, q['binding'], item)
    matched = []
    for use in sorted(inv.graph.access[(target,cells[0]['root'])]['readers'] - {root}):
        if inv.f.operations[use].get('generated_getter'):
            continue
        if opaque_paths(inv,use):
            return None
        paths = list(inv.f.operation_paths(use,True))
        if not any(s['root']==cells[0]['root'] for _,path in paths for s in use_reads(path)):
            continue
        if use not in claimed or not paths:
            return None
        shapes = set()
        for _,path in paths:
            outputs = [path['writes'],path.get('sensitive_effects',[]),path.get('return_value')]
            if any(s['root']==cells[0]['root'] for s in selectors(outputs)):
                return None
            if not any(s['root']==cells[0]['root'] for s in selectors(path['guards'])):
                return None
            # Only ordinary use of the caller's own right, not a transfer/mint on another's behalf.
            if not any(w['value'].get('op')=='-' and key(w['value']['args'][0])==key(w['path'])
                       and (inv.backend._holder(use,w['path']) or {}).get('kind')=='actual_sender'
                       for w in path['writes']):
                return None
            shapes.add(key(outputs))
        if len(shapes)!=1:
            return None
        matched.append(use)
    if matched:
        return {'reason':'bounded_holder_availability_question','effect_entries':matched,
                'control':cells[0],'affected_categories':['FCR-PAUSE','FCR-FREEZE'],
                'limits':'only this pending blocking observation; no finding or whole-task conclusion'}
    return None


def coverage_facts(inv, q):
    if inv.f.options.scope != 'FCR' or not q.get('task_conflict'):
        return None
    token = (q['version'], tuple(q['evidence']))
    cached = q.get('_coverage_facts')
    if cached and cached[0] == token:
        return cached[1]
    try:
        result = local_task_scope(inv,q) or bounded_availability_scope(inv,q)
        if result is None and explicit_outside_scope(inv,q):
            result = {'reason':'recorded_explicit_non_task_clue','affected_categories':[],
                      'effect_entries':sorted(claim_entries(inv,q['binding'],q['current'])),
                      'limits':'source bounded, independent findings preserved'}
    except (KeyError,ValueError,TypeError,IndexError,NotImplementedError,TimeoutError) as error:
        inv.diagnostics.append({'issue':q['id'],'reason':'coverage_scope_unestablished',
                                'details':str(error),'no_new_negative':True})
        result = None
    q['_coverage_facts'] = token,result
    return result


def explicit_outside_scope(inv, q):
    if q.get('task_review',{}).get('status') != 'explicit_out_of_task_clue':
        return False
    binding = q['binding']
    if not binding.get('core_exact') or binding.get('ambiguous') or binding.get('unresolved'):
        return False
    entries = claim_entries(inv,binding,q['current'])
    for oid in entries:
        if opaque_paths(inv,oid):
            return False
        for _,path in inv.f.operation_paths(oid,True):
            for w in path['writes']:
                readers = inv.graph.access[(inv.f.operations[oid]['target'],w['path']['root'])]['readers']
                if any(opaque_paths(inv,u) for u in readers):
                    return False
    return True


def local_task_scope(inv, q):
    """A local certificate for an explicitly non-financial clue, never a whole-task negative."""
    item, binding = q['current'], q['binding']
    if inv.f.options.scope != 'FCR' or item.get('category') != 'AC' or not binding.get('core_exact'):
        return None
    if binding.get('ambiguous') or binding.get('unresolved'):
        return None
    root = binding['core_operation']
    entries = claim_entries(inv, binding, item)
    lookup = inv.f.lookup(root)
    # A local, scoped normal conclusion requires actual accepted source inspection.
    inspected = {inv.evidence[e].get('operation') for e in q['evidence']
                 if inv.evidence[e]['kind'] == 'source_inspection' and not inv.evidence[e].get('local_errors')}
    if root not in inspected or not entries:
        return None
    pure_event = True
    role_writes = set()
    role_readers = set()
    for oid in entries:
        declaration = lookup.nodes.get(inv.f.operations[oid]['source'].get('ast_id'), {})
        if (oid != root and declaration.get('nodeType') == 'VariableDeclaration'
                and declaration.get('stateVariable') and declaration.get('visibility') == 'public'
                and declaration.get('typeDescriptions', {}).get('typeString') in ('address','address payable')):
            continue  # compiler-generated read-only identity accessor, not an unexamined action
        if not inv.backend.complete(oid):
            return None
        commits = list(inv.f.operation_paths(oid, True))
        if not commits:
            return None
        for pid, path in commits:
            audit = inv.backend.condition_dependencies(oid, pid, path)
            if (path.get('sensitive_effects') or audit['unknown_dependencies'] or audit['credential_dependencies']
                    or path.get('return_value') is not None and not account_term(path['return_value'], lookup)):
                return None
            if path['writes']:
                pure_event = False
                if item.get('assessment') != 'normal' or not path_qualification(inv.f,oid,path):
                    return None
            for w in path['writes']:
                dest, val = w['path'], w['value']
                if not account_term(dest, lookup) or not (account_term(val, lookup) or val.get('kind') in ('parameter','literal')):
                    return None
                role_writes.add(dest['root'])
                role_readers.update(s['root'] for g in path['guards'] for s in selectors(g))
        # payable entry or opaque effects cannot be certified event/role-only.
        if lookup.function(inv.f.operations[oid]['function']).get('stateMutability') == 'payable':
            return None
    if pure_event:
        for oid in entries:
            fn = lookup.function(inv.f.operations[oid]['function'])
            body = fn.get('body') or {}
            if fn.get('modifiers') or not body.get('statements') or any(
                    n.get('nodeType') != 'EmitStatement' for n in body['statements']):
                return None
            # A helper called by another entry can affect an enclosing transaction.
            if any(n.get('nodeType') == 'FunctionCall' and
                   n.get('expression',{}).get('referencedDeclaration') == fn.get('id')
                   for other, op in inv.f.operations.items() if other != oid and op['target'] == inv.f.operations[oid]['target']
                   for n in walk(lookup.function(op['function']))):
                return None
    else:
        # An address-valued setter can also select the recipient of a payout or an external
        # implementation. Only role positions used solely for authorization/role updates qualify.
        for cell in role_writes:
            for use in inv.graph.access[(inv.f.operations[root]['target'], cell)]['readers']:
                if not inv.backend.complete(use):
                    return None
                for _, path in inv.f.operation_paths(use, True):
                    returned = path.get('return_value')
                    plain_getter = not path['writes'] and returned and account_term(returned, lookup)
                    payload = [path.get('sensitive_effects', []), None if plain_getter else returned,
                               [keys(w['path']) for w in path['writes']],
                               [w['value'] for w in path['writes'] if not (use in entries and account_term(w['path'], lookup))]]
                    if any(s['root'] == cell for s in selectors(payload)):
                        return None
                    for guard in path['guards']:
                        if any(s['root'] == cell for s in selectors(guard)) and not positive_caller_gate(guard, lookup):
                            # Nonzero/nominee inequality on the local handover itself is harmless.
                            if use not in entries:
                                return None
        for cell in role_writes:
            writers = inv.graph.access[(inv.f.operations[root]['target'], cell)]['writers']
            if not writers <= entries:
                return None
        if not role_writes & role_readers:
            return None
    return {'reason':'source_local_event' if pure_event else 'source_local_normal_authority',
            'effect_entries':sorted(entries), 'affected_categories':[],
            'limits':'only this issue; external/asset dependencies and other issues assessed independently'}


```

## source/src/pr_next_joint/investigation/roles.py

原文件SHA256 `20ca479c38e69e318b8e46c56a3a5f29b1c40cd572c952e5d0e8973315fd025d`

```python
"""Source-grounded qualifications for a specific compiled target and committing path."""
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys,selectors


def _roots(node, allowed, positive=True):
    """Return role declarations required by the condition; all arms of a disjunction must qualify."""
    args, op = node.get('args', []), node.get('op')
    if op == '!' and len(args) == 1:
        return _roots(args[0], allowed, not positive)
    if op in ('and', '&&', 'or', '||') and args:
        roots = [_roots(x, allowed, positive) for x in args]
        conjunction = (op in ('and', '&&')) == positive
        return set().union(*roots) if conjunction or all(roots) else set()
    if op in ('==', '!=') and len(args) == 2:
        equality = (op == '==') == positive
        for side, other in (args, args[::-1]):
            if other.get('kind') == 'literal' and type(other.get('value')) is bool:
                return _roots(side, allowed, equality == other['value'])
            if equality and other.get('kind') == 'actual_sender' and side.get('kind') == 'storage':
                rid = side['root']
                if not side.get('segments') and not side.get('instance') and rid in allowed:
                    return {rid}
    if positive and node.get('kind') == 'storage' and not node.get('instance') and node['root'] in allowed:
        idx = keys(node)
        if len(node.get('segments', [])) == len(idx) == 1 and idx[0].get('kind') == 'actual_sender':
            return {node['root']}
    return set()


def effective_roots(guard, allowed):
    """An explicit self-call arm does not remove the qualified outsider arm.
    Used for privilege existence only. The encoded guard keeps both alternatives.
    """
    roots = _roots(guard,allowed)
    if roots or guard.get('op') not in ('or','||'):
        return roots
    arms = guard['args']
    external = [arm for arm in arms if not (arm.get('op') == '==' and
                {v.get('kind') for v in arm.get('args',[])} == {'actual_sender','contract_address'})]
    if len(external) != 1 or len(external) == len(arms):
        return set()
    return _roots(external[0],allowed)


def _seed_address(node, parameters):
    if not node:return None
    if node.get('memberName') == 'sender' and node.get('expression', {}).get('name') == 'msg':
        return {'term':'deployer'}
    if node.get('referencedDeclaration') in parameters:
        return {'term':'constructor_parameter','id':node['referencedDeclaration']}
    if node.get('nodeType') == 'FunctionCall' and node.get('kind') == 'typeConversion' and len(node.get('arguments', [])) == 1:
        return _seed_address(node['arguments'][0], parameters)
    if node.get('nodeType') == 'Literal':
        try:value = int(node.get('value',''),0)
        except (ValueError,TypeError):return None
        if 0 < value < 2**160:return {'term':'address_literal','value':value}
    return None


def _is_table(decl):
    typ = decl.get('typeName') or {}
    return (typ.get('nodeType')=='Mapping' and typ.get('keyType',{}).get('name')=='address'
            and typ.get('valueType',{}).get('name')=='bool')


def constructor_supports(path,rid,lookup):
    if path['flow'] not in ('normal','returned'):return False
    gaps=list(path.get('issues',()))+list(path.get('evaluation_gaps',()))
    from .initial_state import assigned_roots
    for gap in gaps:
        site=gap.get('source') or gap.get('where') or {}
        node=lookup.nodes.get(site.get('ast_id'))
        if not node:return False
        # Only a direct unrelated copy/literal can be discharged locally. An
        # unexpanded arithmetic/index/call may still abort the entire constructor.
        rhs=node.get('rightHandSide',{})
        if (node.get('nodeType')!='Assignment' or node.get('operator')!='=' or
                rhs.get('nodeType') not in ('Identifier','Literal','MemberAccess')):return False
        roots=assigned_roots(node.get('leftHandSide') or node.get('subExpression') or node,lookup)
        if not roots:
            roots=set().union(*(assigned_roots(n.get('leftHandSide') or n.get('subExpression'),lookup)
                    for n in walk(node) if isinstance(n,dict) and (n.get('leftHandSide') or n.get('subExpression'))))
        if not roots or rid in roots:return False
        for n in walk(node):
            if n.get('nodeType') in ('InlineAssembly','RevertStatement','Throw'):return False
            if n.get('nodeType')=='FunctionCall' and n.get('kind')!='typeConversion':return False
        if any(word in str(gap.get('reason','')).lower() for word in ('revert','out_of_bounds','unresolved_call','frontier','limit')):return False
    return True


def _role_index(facts, target):
    from .initial_state import model,domain,CAPABILITY
    initial=model(facts,target);lookup=facts.lookups[target]
    token=(target,domain(lookup),initial['identity'])
    cache=facts.__dict__.setdefault('_authority_by_target',{})
    if token in cache:return cache[token]
    decls={rid:lookup.nodes[rid] for rid,row in initial['declarations'].items() if
        _is_table(lookup.nodes[rid]) or row['type'] in ('address','address payable')}
    origins={r:[] for r in decls};writers={r:[] for r in decls};invalid=set();seen={r:set() for r in decls}
    clean=[p for p in initial['constructor_paths'] if p['flow'] in ('normal','returned')]
    def seed(term):
        if term.get('kind')=='actual_sender':return {'term':'deployer'}
        if term.get('kind')=='parameter' and term.get('id') in initial['constructor_parameters']:
            return {'term':'constructor_parameter','id':term['id']}
        if term.get('kind')=='literal' and type(term.get('value')) is int and 0<term['value']<2**160:
            return {'term':'address_literal','value':term['value']}
        return None
    for rid,decl in decls.items():
        row=initial['declarations'][rid]
        if any(p['flow'] in ('normal','returned') and not constructor_supports(p,rid,lookup) for p in initial['constructor_paths']):
            if row['constructor_writes'] or row['explicit_constructor_sites'] or row['explicit_initializer']:invalid.add(rid)
        for pi,p in enumerate(clean):
            if not constructor_supports(p,rid,lookup):continue
            relevant=[w for w in p['writes'] if w['path']['root']==rid]
            if not _is_table(decl):relevant=relevant[-1:]
            for w in relevant:
                v=w['value'];idx=keys(w['path'])
                origin=seed(idx[0]) if _is_table(decl) and len(idx)==1 and v.get('kind')=='literal' and v.get('value') is True else seed(v) if not _is_table(decl) else None
                if origin:origins[rid].append(dict(origin,source=w['source'],constructor_path=pi,guards=p['guards'],source_kind='constructor'))
                elif not _is_table(decl) and v.get('kind')=='literal' and v.get('value')==0:pass
                elif not _is_table(decl):invalid.add(rid)
        if not origins[rid] and domain(lookup)==CAPABILITY and row['type'] in ('address','address payable') and not row['explicit_initializer'] and not row['constructor_writes'] and not row['explicit_constructor_sites']:
            origins[rid].append({'term':'abstract_initial_role','declaration':rid,'source':row['source'],
                'source_kind':'declared_conditional_initial_assumption','analysis_domain':CAPABILITY})
    for rid,rows in initial['runtime_writers']['paths'].items():
        if rid not in decls:continue
        for row in rows:
            seen[rid].add(row['source'].get('ast_id'))
            if row['flow']=='reverted':continue
            if not row['complete']:invalid.add(rid);continue
            p=facts.paths[row['path']]['raw'];dst=row['cell'];value=row['value']
            if key(dst)==key(value) or value.get('kind')=='literal' and value.get('value') in (False,0):continue
            writers[rid].append({'operation':row['operation'],'path':row['path'],'guards':p['guards'],'site':row['source'].get('ast_id')})
    for rid in decls:
        missing=set(initial['runtime_writers']['sites'].get(rid,[]))-seen[rid]
        # A source site on a fully known reverting path cannot grant authority.
        if missing:invalid.add(rid)
    known={r for r in decls if r not in invalid and (origins[r] or writers[r])}
    if initial['runtime_writers']['opaque_storage_writes']:known.clear()
    # For FCR, an incumbent OR this-contract guard preserves the incumbent
    # arm only when the public body cannot forward a selector into the grant.
    # Built-in send/transfer have empty calldata; other unresolved CALLs stay open.
    def can_forward(call):
        if facts.operations[call['operation']]['target']!=target or call['mode']=='STATICCALL':return False
        node=lookup.nodes.get(call['source'].get('ast_id'),{})
        builtin=node.get('expression',{}).get('typeDescriptions',{}).get('typeIdentifier','')
        return not builtin.startswith(('t_function_send','t_function_transfer'))
    role_guard=effective_roots if facts.options.scope=='FCR' and not any(can_forward(c) for c in facts.call_summaries.rows.values()) else _roots
    def protected(writer,roots):return set().union(*(role_guard(g,roots) for g in writer['guards']))
    def close(s):
        while True:
            keep={r for r in s if all(protected(w,s) for w in writers[r])}
            if keep==s:return keep
            s=keep
    known=close(known);active={r for r in known if origins[r]}
    while True:
        add={r for r in known-active if any(protected(w,active) for w in writers[r])}
        if not add:break
        active.update(add)
    active=close(active)
    records={r:{'declaration':r,'target':target,'kind':'caller_membership' if _is_table(decls[r]) else 'caller_equals_account',
        'source':lookup.anchor(decls[r]),'deployment_origins':[o for o in origins[r] if o['term']!='abstract_initial_role'],
        'abstract_origins':[o for o in origins[r] if o['term']=='abstract_initial_role'],
        'source_origins':origins[r],'analysis_domain':domain(lookup),'initial_model_identity':initial['identity'],
        'guarded_grant_paths':[{'operation':w['operation'],'path':w['path'],'site':w['site'],
            'qualifying_declarations':sorted(protected(w,active)),
            'qualification_guards':[g for g in w['guards'] if role_guard(g,active)]} for w in writers[r]],
        'has_runtime_assignment':bool(initial['runtime_writers']['sites'].get(r))} for r in sorted(active)}
    facts.__dict__.setdefault('_authority_diagnostics',{})[target]={'analysis_domain':domain(lookup),'unresolved_declarations':sorted(invalid),
        'reachable_function_ids':initial['runtime_writers']['functions'],'opaque_storage_writes':initial['runtime_writers']['opaque_storage_writes']}
    cache[token]=records
    return records


def _same_public_effect(facts,oid,path,registry):
    """Both sides of an if can implement an identical operation. A caller test alone then confers no advantage."""
    def effect(p):
        return key([[(w['path'],w['value']) for w in p['writes']],p.get('sensitive_effects',[]),p.get('return_value')])
    guards=set(map(key,path['guards']))
    for _,other in facts.operation_paths(oid,True):
        if other is path or any(_roots(g,registry) for g in other['guards']):continue
        opposite=set(map(key,other['guards']))
        for g in path['guards']:
            if not _roots(g,registry):continue
            neg=g['args'][0] if g.get('op')=='!' else {'kind':'op','op':'!','args':[g]}
            if opposite==(guards-{key(g)})|{key(neg)} and effect(path)==effect(other):return True
    return False


def path_qualification(facts, oid, path):
    cache=facts.__dict__.setdefault('_path_qualifications',{})
    from .initial_state import domain
    token=(oid,id(path),domain(facts.lookup(oid)))
    if token in cache:return cache[token]
    target=facts.operations[oid]['target']
    registry=_role_index(facts,target)
    proof=[]
    for g in path['guards']:
        ids=(effective_roots if facts.options.scope=='FCR' else _roots)(g,registry)
        if ids:proof.append({'guard':g,'roles':[registry[i] for i in sorted(ids)]})
    if proof and _same_public_effect(facts,oid,path,registry):proof=[]
    if proof:
        principal_ids={r['declaration'] for row in proof for r in row['roles']}
        # A second source read may alias the very deployer denoted by the qualifying table.
        related={c['root'] for c in selectors([path['guards'],path['writes']]) if c['root'] in registry}
        proof[0]['related_fixed_accounts']=[registry[i] for i in sorted(related-principal_ids)
                    if registry[i]['kind']=='caller_equals_account' and not registry[i]['has_runtime_assignment']]
    cache[token]=proof
    return proof


def fixed_role_terms(encoder, qualification, slot):
    """Use the same deployment identities across fixed membership tables and fixed scalar roles."""
    from pr_next_joint.verification.sequence import qualify
    roles={r['declaration']:r for row in qualification for r in row['roles']+row.get('related_fixed_accounts',[])}
    from .initial_state import domain,CAPABILITY,DEPLOYMENT,initial_for_lookup
    if domain(encoder.lookup) in (CAPABILITY,DEPLOYMENT) and initial_for_lookup(encoder.lookup):
        return [],[{'declaration':rid,'origins':r.get('source_origins',r['deployment_origins']),
            'scope':'constructor and committed prefix encoded by shared initial state model',
            'analysis_domain':domain(encoder.lookup)} for rid,r in roles.items()]
    z=encoder.z;terms=[];receipt=[]
    caller=encoder.expr(qualify({'kind':'actual_sender'},slot))
    for rid,role in roles.items():
        if role['guarded_grant_paths'] or not role['deployment_origins']:continue
        if role['kind']=='caller_equals_account' and len(role['deployment_origins'])!=1:continue
        values=[]
        for origin in role['deployment_origins']:
            if origin['term']=='address_literal':values.append(z.IntVal(origin['value']));continue
            symbol='deployment_caller' if origin['term']=='deployer' else 'deployment_address_parameter_'+str(origin['id'])
            value=z.Int(symbol);terms.extend([value>=0,value<2**160])
            if origin['term']=='deployer':terms.append(value!=0)
            values.append(value)
        cell={'kind':'storage','root':rid,'segments':[]}
        if role['kind']=='caller_membership':
            cell['segments']=[{'key':{'kind':'actual_sender'}}]
            member=encoder.expr(qualify(cell,slot))
            seeded=z.Or(*[caller==v for v in values])
            terms.append(z.Implies(member,seeded) if role['has_runtime_assignment'] else member==seeded)
        else:
            account=encoder.expr(cell)
            terms.append(z.Or(account==0,account==values[-1]) if role['has_runtime_assignment'] else account==values[-1])
        receipt.append({'declaration':rid,'origins':role['deployment_origins'],
                        'scope':'cannot add members; revocation possible' if role['has_runtime_assignment'] else 'fixed original role at queried caller'})
    return terms,receipt


```

## source/src/pr_next_joint/investigation/scope_relevance.py

原文件SHA256 `f996a843ba5bf16b6687ce5cc1663320fcaa6e0bece213f00e5b9d1f29fab7a9`

```python
"""Source necessary conditions for per-entry, per-category obligations.

An excluded necessary condition can close a route without resolving an
unrelated call. This is a dependency certificate, not candidate-list emptiness.
"""
from pr_next_joint.frontend.path_ir import walk, key
from pr_next_joint.frontend.storage import keys, selectors, value_type, selector_relation
from .contracts import CATEGORIES


def source_role_may(f,oid):
    """Whole resolved body scan, including statements beyond a loop frontier."""
    cache=f.__dict__.setdefault('_source_role_may',{})
    if oid in cache:return cache[oid]
    lookup=f.lookup(oid);entry=lookup.function(f.operations[oid]['function'])
    pending=[entry];seen=set();bodies=[]
    while pending:
        body=pending.pop();bid=body.get('id')
        if bid in seen:continue
        seen.add(bid);bodies.append(body)
        for n in walk(body):
            if n.get('nodeType')=='ModifierInvocation':
                d=lookup.nodes.get(n.get('modifierName',{}).get('referencedDeclaration'),{})
                if d:pending.append(d)
            if n.get('nodeType')=='FunctionCall':
                exp=n.get('expression',{});d=lookup.nodes.get(exp.get('referencedDeclaration'),{})
                if d.get('body') and (exp.get('nodeType')=='Identifier' or
                    't_function_internal' in exp.get('typeDescriptions',{}).get('typeIdentifier','')):
                    pending.append(d)
    def sender(n):
        return (n.get('nodeType')=='MemberAccess' and n.get('memberName') in ('sender','origin') and
                n.get('expression',{}).get('name') in ('msg','tx'))
    tainted=set()
    nodes=list(walk(bodies))
    while True:
        old=set(tainted)
        for n in nodes:
            rhs=n.get('rightHandSide') if n.get('nodeType')=='Assignment' else n.get('initialValue')
            if rhs and any(sender(t) or t.get('referencedDeclaration') in tainted for t in walk(rhs)):
                dst=n.get('leftHandSide',{}).get('referencedDeclaration')
                if dst is not None:tainted.add(dst)
                tainted.update(d['id'] for d in n.get('declarations',[]) if d)
        if old==tainted:break
    result=False
    for n in nodes:
        if n.get('nodeType')=='BinaryOperation' and n.get('operator') in ('==','!='):
            for a,b in ((n['leftExpression'],n['rightExpression']),(n['rightExpression'],n['leftExpression'])):
                if (sender(a) or a.get('referencedDeclaration') in tainted) and not (
                    b.get('nodeType')=='Literal' and b.get('value') in ('0','0x0')):result=True
        if n.get('nodeType')=='IndexAccess' and n.get('typeDescriptions',{}).get('typeString')=='bool':
            if any(sender(t) or t.get('referencedDeclaration') in tainted for t in walk(n.get('indexExpression'))):result=True
    cache[oid]=result;return result


def potential_role(f,oid,path):
    from .roles import path_qualification, effective_roots
    if path_qualification(f,oid,path):return True
    lookup=f.lookup(oid)
    allowed={n['id'] for n in lookup.decls.values() if n.get('stateVariable') and
        (n.get('typeDescriptions',{}).get('typeString') in ('address','address payable') or
         n.get('typeName',{}).get('nodeType')=='Mapping')}
    for guard in path['guards']:
        if effective_roots(guard,allowed):return True
        for term in walk(guard):
            if term.get('op') in ('==','!=') and any(a.get('kind')=='actual_sender' for a in term.get('args',[])):
                if any(a.get('kind') in ('literal','parameter') for a in term.get('args',[])):return True
            if term.get('kind') in ('unknown','external_return','read_call','call_unresolved'):
                origins=[i for i in path.get('issues',[]) if i.get('reason')==term.get('reason')]
                # A low-level CALL's success flag is not itself a privileged
                # qualification. Callback entry guards are inspected separately.
                if not origins:return True
                for row in origins:
                    node=lookup.nodes.get(row.get('source',{}).get('ast_id'),{})
                    calls=[n for n in walk(node) if n.get('nodeType')=='MemberAccess']
                    if not any(n.get('memberName') in ('call','send','transfer') and
                        n.get('typeDescriptions',{}).get('typeIdentifier','').startswith(('t_function_barecall','t_function_send','t_function_transfer')) for n in calls):
                        return True
    return False


def nonfinancial(backend,oid,cell):
    from .key_roles import relation
    from .ledger import unit_origin,native_only_position
    lookup=backend.f.lookup(oid)
    if (relation(cell,lookup) or {}).get('kind')=='authorization_quantity':return 'holder_authorization_quantity'
    if native_only_position(backend,oid,cell):return 'native_redemption_not_five_class_token_unit'
    semantic=getattr(backend,'semantics',None)
    binding=semantic.lookup(oid,cell) if semantic else None
    if binding and binding['meaning']=='nonfinancial_counter' and not unit_origin(backend,oid,cell):
        return 'source_bound_nonfinancial_interpretation'
    # Clocks and control flags do not become minted tokens merely because a
    # setter changes a numeric value. Require source evidence of dual use.
    temporal=any(any(selector_relation(s,cell)=='same_shape' for s in selectors(g)) and
        any(n.get('kind') in ('block_timestamp','block_number') or n.get('kind')=='environment' and
            n.get('field') in ('timestamp','number') for n in walk(g))
        for other,o in backend.f.operations.items() if o['target']==backend.f.operations[oid]['target']
        for _,p in backend.f.operation_paths(other) for g in p['guards'])
    if temporal and not unit_origin(backend,oid,cell):return 'source_time_dimension_without_asset_use'
    return None


def detached_holder_switch(inv,oid):
    """Resolve one local account switch against the actual public outgoing paths.
    A query getter is not a holder action. Independent external contracts and
    their balances remain outside this conclusion."""
    cache=inv.__dict__.setdefault('_detached_holder_switch',{})
    if oid in cache:return cache[oid]
    if inv.program_remaining()<=0:return None
    f=inv.f;lookup=f.lookup(oid);target=f.operations[oid]['target']
    rows=f.summaries.rows(oid)
    writes=[w for r in rows for w in r['ordered_writes']]
    toggles=[w for w in writes if keys(w['path']) and value_type(w['path'],lookup)=='bool']
    if not toggles or not inv.backend.complete(oid) or any(
            r['residuals'] or r['effects'] or any(local.get('may_directions') and local['holder'] is not None
            and value_type(local['cell'],lookup)!='bool' and local['cell']['root'] not in {w['path']['root'] for w in writes if w['value'].get('kind')=='parameter'}
            for local in r['numeric_effects']) for r in rows):
        cache[oid]=None;return None
    if any(w['value'].get('kind') not in ('parameter','literal') for w in writes):
        cache[oid]=None;return None
    roots={w['path']['root'] for w in writes}
    transfers=[];dependent=False
    downstream=f.summaries.dependencies.forward(oid)['uses']
    for use,op in f.operations.items():
        if op['target']!=target or op.get('generated_getter'):continue
        if inv.program_remaining()<=0:return None
        for r in f.summaries.rows(use,False):
            from .key_roles import relation
            spending=any(e.get('holder') is not None and 'debit' in e['may_directions']
                         and (relation(e['cell'],lookup) or {}).get('kind')!='authorization_quantity'
                         and e['cell']['root'] not in roots for e in r['numeric_effects'])
            if not spending:continue
            # Direct and transitive value/guard dependencies both remain open.
            transfers.append(use)
            if (use in downstream or any(c['root'] in roots for c in selectors([r['guards'],
                    [(w['path'].get('segments',()),w['value']) for w in r['ordered_writes']]]))
                    or any(v.get('reason') not in ('external_destination_not_bound','multiple_address_keys_need_source_holder_binding')
                           for v in r['residuals'])):dependent=True
            # Only the dependence on this local switch is being closed. Keep
            # independent external calls in their own entry's coverage record.
            if any(c['root'] in roots for c in selectors([r.get('effects',[]),
                    f.paths[r['path']]['raw'].get('evaluated_terms',[])])):dependent=True
        if not inv.backend.complete(use):
            if use in downstream or any(g.get('kind') in ('path_extraction','source_expression_limit','dependent_source_expression_limit') for g in op.get('gaps',())):dependent=True
            # An unresolved ordinary foreign call does not read local storage
            # unless its result flows back to the outgoing effect or a callback
            # has a local reader. Keep opaque local code open.
            if any(any(v in str(issue.get('reason','')) for v in ('unsupported_statement','unresolved_storage','write_expansion','source_path_frontier','assembly'))
                   for _,path in f.operation_paths(use) for issue in path.get('issues',())):dependent=True
    if any(c['mode']=='DELEGATECALL' and c.get('unresolved_implementation') and
           f.operations[c['operation']]['target']==target for c in f.call_summaries.rows.values()):dependent=True
    result=None
    if transfers and not dependent:
        result={'reason':'detached_local_holder_switch','operation':oid,'target':target,
                'locations':[w['source'] for w in toggles],'outgoing_entries':sorted(set(transfers))}
    cache[oid]=result
    return result


def directory(inv,oid,control_categories):
    from .ledger import unit_origin
    f=inv.f;lookup=f.lookup(oid);operation=f.operations[oid]
    if operation.get('generated_getter'):
        return {'operation':oid,'target':operation['target'],'possible_categories':[],
            'source_routes':[],'excluded_necessary_condition':'compiler_generated_readonly_getter',
            'absence_certificates':{c:{'necessary':'stateful intervention or affected transfer',
                'basis':'compiler_generated_readonly_getter','operation':oid,'target':operation['target'],
                'source':operation['source'],'domain':inv.f.identity,'decisive_residuals':[]} for c in CATEGORIES[1:]},
            'source':operation['source'],'control_categories':[],
            'unresolved_same_storage_calls':[],'unread_effect_residuals':[]}
    rows=f.summaries.rows(oid,False);cats=set(control_categories);routes=[]
    calls=[r for r in f.call_summaries.rows.values() if r['operation']==oid]
    delegate=[c for c in calls if c['mode']=='DELEGATECALL' and c['unresolved_implementation']]
    if delegate:cats.update(CATEGORIES[1:])
    for row in rows:
        p=f.paths[row['path']]['raw'];possible=set();facts=[]
        if p['flow']=='reverted':
            routes.append({'path':row['path'],'possible_categories':[], 'excluded_necessary_condition':'outer_transaction_does_not_commit'})
            continue
        role=potential_role(f,oid,p) or (p['flow']=='truncated' and source_role_may(f,oid))
        if not role and not delegate:
            facts.append('no_privileged_qualification_on_this_source_route')
        else:
            moves={s:[] for s in ('-','+')}
            for e in row['numeric_effects']:
                if e['holder'] is None:continue
                why=nonfinancial(inv.backend,oid,e['cell'])
                if why:
                    facts.append({'position':e['cell'],'excluded_financial_unit':why});continue
                for sign,direction in (('-','debit'),('+','credit')):
                    if direction in e['may_directions']:moves[sign].append(e['cell'])
            paired=lambda a,others:any(selector_relation(a,b)=='same_shape' and key(a)!=key(b) for b in others)
            if any(paired(d,moves['+']) for d in moves['-']):possible.add('FCR-TRANSFER')
            # A structural cross-key credit is not necessarily compensation, and a
            # paired debit need not account for the entire credit. Compare amounts later.
            if moves['-']:possible.add('FCR-DESTROY')
            if moves['+']:possible.add('FCR-MINT')
            for call in calls:
                if call['path']!=row['path'] or not call['unresolved_implementation']:continue
                n=lookup.nodes.get(call['source'].get('ast_id'),{})
                declaration=lookup.nodes.get(n.get('expression',{}).get('referencedDeclaration'),{})
                # A source-declared ordinary external method can affect its
                # separate asset ledger; native value calls alone cannot mint
                # or destroy a local token ledger. Known callback writes are
                # retained under their own original entries and qualifications.
                if call['mode']=='DELEGATECALL':possible.update(CATEGORIES[1:])
                elif call['mode']!='STATICCALL' and declaration.get('nodeType')=='FunctionDefinition':
                    possible.update(('FCR-TRANSFER','FCR-MINT','FCR-DESTROY'))
        cats.update(possible)
        routes.append({'path':row['path'],'possible_categories':sorted(possible),
            'qualification_may_hold':role,'necessary_condition_facts':facts,
            'residuals':row['residuals'],'flow':p['flow']})
    # A failed frontend or a path abandoned before its body was inspected
    # cannot supply a no-effect certificate. Loop frontier residuals retain
    # the classes of their actual body effects; arbitrary assembly does not.
    hard=[g for g in operation.get('gaps',[]) if g.get('kind') in ('path_extraction','source_expression_limit','dependent_source_expression_limit')]
    opaque=[i for _,p in f.operation_paths(oid) for i in p.get('issues',[]) if
        any(s in str(i.get('reason','')) for s in ('unsupported_statement','unresolved_storage','write_expansion','source_path_frontier_bound_exceeded'))]
    if not rows or hard or opaque:cats.update(CATEGORIES[1:])
    closure=f.summaries.dependencies.forward(oid)
    amount_uses=[]
    for use,kinds in closure['uses'].items():
        if 'value' not in kinds:continue
        if any(not nonfinancial(inv.backend,use,c) for c in f.summaries.positions(use)):
            amount_uses.append(use)
    if amount_uses:
        # This is a conservative investigation frontier, not evidence that a
        # transfer, issue or loss really occurred.
        cats.update(('FCR-TRANSFER','FCR-MINT','FCR-DESTROY'))
    exclusions={}
    complete=bool(rows) and inv.backend.complete(oid) and not (hard or opaque or delegate)
    committed=[row for row in rows if row['committing']]
    harmless=all(not row['ordered_writes'] and not row['effects'] and not row['residuals'] for row in committed)
    effect_calls=[c for c in calls if c['mode']!='STATICCALL']
    basis=None
    if complete and not committed:
        basis='all_extracted_exits_revert'
    elif complete and harmless and not effect_calls:
        basis='committed_exits_have_no_state_or_external_effect'
    elif complete and not effect_calls and not any(r['effects'] for r in committed):
        # A pure getter may expose a flag without affecting a holder request.
        # Establish this from ALL resolved public bodies, including reverted
        # guards and subscripts, independently of the candidate edge index.
        target=operation['target']
        scans=inv.__dict__.setdefault('_public_effect_reads',{})
        if target not in scans:
            members=[o for o,v in f.operations.items() if v['target']==target and not v.get('generated_getter')]
            all_resolved=all(inv.backend.complete(o) for o in members) and not any(
                call['operation'] in members and call.get('unresolved_implementation')
                for call in f.call_summaries.rows.values())
            reads={}
            for use in members:
                roots=set()
                for _,p in f.operation_paths(use):
                    terms=[p['guards'],p.get('return_value'),p.get('evaluated_terms'),p.get('sensitive_effects')]
                    for w in p['writes']:terms.extend([w['value'],keys(w['path'])])
                    roots.update(s['root'] for s in selectors(terms))
                reads[use]=roots
            scans[target]=(all_resolved,reads)
        all_resolved,reads=scans[target]
        cells=[w['path'] for r in committed for w in r['ordered_writes']]
        roots={c['root'] for c in cells}
        if all_resolved and cells and not any(r['residuals'] for r in committed) and not any(
                roots & used for other,used in reads.items() if other!=oid):
            if all(value_type(c,lookup)=='bool' for c in cells) and not any(roots & used for used in reads.values()):
                basis='isolated_flag_no_nongenerated_reader_in_resolved_public_bodies'
            elif all(nonfinancial(inv.backend,oid,c)=='source_bound_nonfinancial_interpretation' for c in cells):
                basis='source_bound_counter_only_no_outgoing_effect_dependence'
    if basis:
        for c in CATEGORIES[1:]:
            exclusions[c]={'necessary':'committed state change or value/availability effect','basis':basis,
                'operation':oid,'target':operation['target'],'domain':f.identity,'source':operation['source'],
                'path_ids':[r['path'] for r in rows],'decisive_residuals':[]}
    return {'operation':oid,'target':operation['target'],'possible_categories':sorted(cats),
        'quantity_dependence_uses':sorted(amount_uses),'value_control_closure':closure['id'],
        'absence_certificates':exclusions,
        'source_routes':routes,'unresolved_same_storage_calls':[c['id'] for c in delegate],
        'unread_effect_residuals':hard+opaque,'control_categories':sorted(control_categories),
        'callback_entries_have_independent_source_obligations':True}

```

## source/src/pr_next_joint/investigation/selection.py

原文件SHA256 `fd3702be585d8836fbbc8bdf71974750d992cd03f6685be64598e373e104567f`

```python
"""Choose a source-bound observation by its power to separate two stated interpretations.

The model supplies expected outcomes, never a witness. Storage identifiers below
are resolved only among selectors of the actual entry. This layer produces actions,
not new risk items. The legacy first-pair order is retained for engineering comparison.
"""
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, selector_relation
from .protocol import normal_alternative
from .request_scope import claim_entries, linked_controls, request_target, select_controls, unique_cells


def _named(inv, oid, selectors_, name):
    if not isinstance(name, str) or not name:
        return []
    nodes = inv.f.lookup(oid).nodes
    return list({key(cell): cell for cell in selectors_ if nodes.get(cell['root'], {}).get('name') == name
                 or inv.backend._storage_name(oid,cell)==name}.values())


def plan_observation(inv, binding, item, plan):
    from .properties import interpret, plan_property, premise_cases, source_target
    from .ledger import MEASURES
    request = interpret(item)
    if isinstance(request,dict) and request.get('measure') in set(MEASURES)|{'direct_effect','denied_qualified','missing_control','authorization_violation'}:
        plan_property(inv,binding,item,plan,request)
        return
    item = dict(item,observation=request)
    if request is None:
        return
    root = binding.get('core_operation')
    empty = {'pool': [], 'selected': None, 'status':'indeterminate'}
    plan['observation_choice'] = empty
    if not root or not isinstance(request, dict):
        empty['reason'] = 'observation_or_applied_core_not_resolved'
        return
    explanation=normal_alternative(item);empty['normal_interpretation']=explanation
    predictions={k:request[k] for k in ('risk','normal') if type(request.get(k)) is bool}
    distinct=len(predictions)==2 and predictions['risk']!=predictions['normal']
    f = inv.f
    measure = request.get('measure')
    if not isinstance(measure,str) or measure not in ('holder_grant','holder_net','opens','blocks'):
        empty.update(status='unsupported',reason='no_program_observable_for_this_semantic_question')
        return
    finding_root = root
    root, possible_uses, reason = request_target(inv, binding, item, plan, measure)
    empty['request_resolution'] = {'finding_root': finding_root, 'use': root, 'possible_uses': possible_uses,
                                   'unmeasured_uses': [u for u in possible_uses if u != root]}
    if reason:
        empty.update(status='infeasible_scope', reason=reason)
        return
    if (measure=='holder_grant' and f.options.scope!='AC') or (measure=='holder_net' and f.options.scope!='FCR'):
        empty.update(status='infeasible_scope', reason='observation_task_mismatch')
        return
    paths = [p for _,p in f.operation_paths(root,True)]
    guard_cells = [s for p in paths for s in selectors(p['guards'])]
    reads = [s for p in paths for s in selectors([p['guards'],p['writes'],p.get('sensitive_effects',[])])]
    writable=[w['path'] for p in paths for w in p['writes']]
    control_pool=guard_cells if measure=='holder_grant' else reads
    objects=_named(inv,root,writable,request.get('object')) if 'object' in request else [
        o for o in {key(s):s for s in writable}.values() if inv.backend._holder(root,o) is not None]
    controls=_named(inv,root,control_pool,request.get('control')) if 'control' in request else list(
        {key(s):s for s in guard_cells}.values())
    if root != finding_root:
        controls = select_controls(inv, root, linked_controls(inv, finding_root, root), request, item)
    elif f.options.scope == 'FCR' and measure in ('opens','blocks'):
        writers = claim_entries(inv, binding, item) - {root}
        if request.get('after'):
            writers = set(inv.catalog.resolve(request['after']))
        connected = unique_cells(c for w in writers for c in linked_controls(inv, w, root))
        controls = select_controls(inv, root, connected, request, item)
    if 'control' not in request and measure=='holder_grant':
        controls=[s for s in controls if any(n.get('kind')=='actual_sender' for n in walk(keys(s)))]
    if 'control' not in request and measure=='holder_net':
        # A requested payout-mode change may be guarded by a unique non-right state cell.
        controls=[s for s in controls if not any(selector_relation(s,o)=='same_shape' for o in objects)]
    def one_position(cells):
        return len({key(c) for c in cells})==1
    if not one_position(controls) or measure in ('holder_grant','holder_net') and not one_position(objects):
        empty.update(status='infeasible_scope',reason='control_or_right_not_bound_to_unique_source_declaration')
        return
    if measure=='holder_grant':
        # A holder key and immediate caller must occur in the tested guard itself.
        holders = [inv.backend._holder(root,o) for o in objects]
        controls = [g for g in controls if any(h and any(key(k)==key(h) for k in keys(g)) for h in holders)
                    and any(n.get('kind')=='actual_sender' for n in walk(keys(g)))]
    if measure=='holder_net':
        objects = [o for o in objects if inv.backend.net_unit(root,o)]
    if not controls or measure in ('holder_grant','holder_net') and not objects:
        empty.update(status='unsupported',reason='holder_direction_or_financial_unit_not_established')
        return
    after = request.get('after')
    after_ids = source_target(inv,after,f.operations[root]['target']) if after is not None else []
    cases,gaps=premise_cases(inv,root,item)
    if gaps:
        empty.update(status='unsupported',reason='; '.join(gaps));return
    if after is not None and (len(after_ids)!=1 or f.operations[after_ids[0]]['target']!=f.operations[root]['target']):
        empty.update(status='infeasible_scope',reason='intervention_target_ambiguous_or_different')
        return
    graph_pairs = plan['selected_pairs'] + plan['deferred_pairs']
    writers = list(dict.fromkeys(p['change'] for p in graph_pairs if p['observe']==root))
    target=f.operations[root]['target']
    hint=item.get('next_check');hint=hint if isinstance(hint,dict) else {}
    explicit=inv.catalog.resolve(hint.get('change')) if hint.get('action')=='compare' and inv.catalog.resolve(hint.get('observe'))==[root] else []
    # A real explicit prior probe remains in the shared pool even when it tests a different control.
    if len(explicit)==1 and f.operations[explicit[0]]['target']==target:
        writers=list(dict.fromkeys(explicit+writers))
    for control in controls:
        for writer in sorted(inv.graph.access[(target,control['root'])]['writers']):
            if writer!=root and writer not in writers:
                writers.append(writer)
    if root != finding_root:
        writers = [finding_root]
    elif f.options.scope == 'FCR' and measure in ('opens','blocks'):
        allowed = claim_entries(inv, binding, item) - {root}
        if after_ids:
            allowed = set(after_ids)
        writers = [w for w in writers if w in allowed]
    delta = None
    if f.options.scope == 'FCR' and measure in ('opens','blocks'):
        deltas = inv.backend._holder_deltas(root)
        if request.get('object'):
            deltas = [row for row in deltas if any(key(o)==key(row[0]) for o in objects)]
        if len(deltas)!=1:
            empty.update(status='unsupported', reason='holder_position_or_ledger_direction_not_unique; ordinary source use preserved')
            return
        cell, holder, direction = deltas[0]
        delta = {'cell':cell,'holder':holder,'direction':direction}
        objects = [cell]
    if after_ids == [root] and finding_root == root and linked_controls(inv,root,root) and root not in writers:
        writers.append(root)
    pool = empty['pool']
    for writer in writers[:f.options.max_actions]:
        ws=[w['raw']['path'] for w in f.writes.values() if w['operation']==writer]
        matching=[c for c in controls if any(selector_relation(c,w)=='same_shape' and
                  not inv.graph._disjoint_keys(c,w) for w in ws)]
        if measure=='holder_grant':
            # In the same-requester experiment a caller writing their own holder slot
            # cannot install a grant in another holder's slot, even when roots coincide.
            def possible_other_holder(g):
                pos={i for i,k in enumerate(keys(g)) if any(key(k)==key(inv.backend._holder(root,o)) for o in objects)}
                return any(selector_relation(w,g)=='same_shape' and not inv.graph._disjoint_keys(w,g)
                           and all(keys(w)[i].get('kind')!='actual_sender' for i in pos) for w in ws)
            matching=[c for c in matching if possible_other_holder(c)]
        candidates = list(dict.fromkeys(['availability',measure]))
        for kind in candidates:
            context=inv._compare_context({'current':item},writer,root)
            # Generic commit probes have no measured entitlement delta.
            state='indeterminate'
            if after_ids and writer!=after_ids[0] or not matching:
                state='infeasible_scope'
            elif kind==measure:
                state='distinguishing' if distinct else 'shared_technical_fact'
            elif measure=='holder_net':
                # Knowing only that a call commits is compatible with both a full and a short payout.
                state='same_expected_observation'
            if kind!='availability':
                context['premise_cases']=cases
                context['observable']={'measure':kind,'control_selectors':matching,'objects':objects}
                if f.options.scope == 'FCR' and measure in ('opens','blocks'):
                    from .properties import privileged_paths
                    context['observable']['qualified_writer_paths']=privileged_paths(inv,writer)
                    companion = [s for s in linked_controls(inv,writer,root) if s['root'] not in {v['root'] for v in matching}]
                    context['observable'].update(hold_other_request_cells=True,holder_delta=delta,
                                                 other_intervention_inputs=companion)
                if kind=='holder_grant':
                    context['caller_modes']=['same_requester']
            pool.append({'action':'compare','change':writer,'observe':root,'measure':kind,'status':state,
                         'expectations':predictions if distinct and kind==measure else {},
                         'scope':{'target':target,'controls':matching,'objects':objects, 'finding_root':finding_root,
                                   'use':root,'intervention':writer, 'measure':kind, 'holder_delta':delta,
                                   'extent':'one source-bound request; other routes and amounts not certified'},
                         'context':context,
                         'cached':inv.backend.reusable('compare',{'change':writer,'observe':root,'context':context})})
    chosen = [p for p in pool if p['status'] in ('distinguishing','shared_technical_fact')]
    if chosen:
        pick=min(chosen,key=lambda p:(not p['cached'],writers.index(p['change'])))
        empty.update(selected=pick,status=pick['status'],reason='distinct explicit predictions' if distinct else 'grounded common fact; normative alternatives remain open')
    else:
        empty.update(status='infeasible_scope',
                     reason='no scoped test with differing explicit predictions')
    legacy=next((p for p in pool if p['measure']=='availability' and (not explicit or explicit==[p['change']])),None)
    empty['prior_candidate']=legacy
    empty['legacy_graph_first']=plan['selected_pairs']
    if empty['selected']:
        pick=empty['selected']
        plan['selected_pairs']=[{'change':pick['change'],'observe':root,
                                 'source_reason':'same scope and conflicting predicted observation'}]
        plan['deferred_pairs']=[p for p in graph_pairs if (p['change'],p['observe'])!=(pick['change'],root)]
    inv.graph.events.append({'action':'disagreement_selection','operation':root,'question':plan['question'],
                             'status':empty['status'],'selected':None if not chosen else [pick['change'],root,pick['measure']],
                             'pool_size':len(pool),'old_explicit_or_graph_pair':None if legacy is None else [legacy['change'],root]})
    empty['unexamined_writer_count']=max(0,len(writers)-f.options.max_actions)

```

## source/src/pr_next_joint/investigation/semantic_audit_card.py

原文件SHA256 `bb9b3fb11b03055bf5f8d49699dc664d9f2c5c9a688de1396b05f6203c85d95f`

```python
"""Validate a bounded model hypothesis and delegate to the ordinary issue consumer."""
from pr_next_joint.core import digest

KINDS = frozenset(("new_sink", "untrusted_sensitive_flow", "role_write_to_use", "authorization_scope",
                   "holder_consent_scope", "financial_unit", "gross_vs_net", "lifecycle_stage",
                   "ordinary_transfer_route", "privileged_state_difference", "potential_normal_counterexample", "unknown"))
CHECKS = frozenset(("actual_call_reachability", "untrusted_flow", "guard_scope", "role_write_to_use",
                    "allowance_scope", "same_unit_net_effect", "control_change_vs_outgoing",
                    "rollback_or_external_dep", "none"))
TEXT = {"effect_ref":180, "actor_holder_relation":240, "risk_explanation":360,
        "normal_alternative":360, "decisive_missing_fact":240}
FIELDS = set(TEXT) | {"issue_kind", "source_refs", "check_kind", "requested_target_ref"}


def parse(card):
    if isinstance(card, dict) and set(card) == {'withdraw','effect_ref','reason'}:
        if all(isinstance(card[k],str) and 0 < len(card[k].strip()) <= limit
               for k, limit in [('withdraw',80),('effect_ref',180),('reason',240)]):
            return None
        return 'invalid_audit_withdrawal'
    if not isinstance(card, dict) or set(card) != FIELDS:
        return "audit_card_fields"
    if any(not isinstance(card[k], str) or len(card[k]) > n for k, n in TEXT.items()):
        return "audit_card_text"
    for k, choices in (("issue_kind", KINDS), ("check_kind", CHECKS)):
        if not isinstance(card[k], str) or card[k] not in choices:
            return "audit_card_" + k
    refs = card['source_refs']
    if not isinstance(refs, list) or not 1 <= len(refs) <= 6 or not all(isinstance(r, str) and 0 < len(r.strip()) <= 180 for r in refs):
        return "audit_card_source_refs"
    target = card['requested_target_ref']
    if target is not None and (not isinstance(target, str) or not 0 < len(target.strip()) <= 180):
        return "audit_card_check_target"
    if not card['effect_ref'].strip() or not (card['risk_explanation'].strip() or card['normal_alternative'].strip()):
        return "audit_card_empty_claim"
    return None


def bind(inv, card, manifest):
    rules = inv.semantics.rules
    effect = rules.bind(card['effect_ref'], manifest, 'effect')
    if not effect:
        return None, 'audit_effect_unbound'
    d = rules.effects[effect]
    oid = d['oid']
    shown = set(manifest.get('expanded_operations', ())) - set(manifest.get('partially_expanded_operations', ()))
    def source(ref):
        handle = rules.bind(ref, manifest)
        if handle:
            record = rules.effects.get(handle) or rules.objects[handle]
            if record['target'] == d['target']:
                return (handle, record.get('oid'))
            return None
        found = inv.catalog.resolve(ref)
        if len(found) == 1 and found[0] in shown and inv.f.operations[found[0]]['target'] == d['target']:
            return (None, found[0])
        return None

    refs = [source(ref) for ref in card['source_refs']]
    if not all(refs) or not any(handle == effect or op == oid for handle, op in refs):
        return None, 'audit_source_scope_mismatch'
    requested = source(card['requested_target_ref']) if card['requested_target_ref'] else (effect, oid)
    if not requested or not requested[1]:
        return None, 'audit_check_target_unbound'
    peer = requested[1]
    check = card['check_kind']
    name = inv.catalog.name(oid)
    hint = {}
    if check in ('role_write_to_use', 'same_unit_net_effect', 'allowance_scope', 'control_change_vs_outgoing'):
        hint = dict(action='compare', change=name, observe=inv.catalog.name(peer))
    elif check != 'none':
        hint = dict(action='inspect', function=inv.catalog.name(peer))
    claim = card['risk_explanation'] or card['normal_alternative']
    # This is a proposed conflict, consumed with the applied policy and guards below.
    # A location/check by itself has no predicted polarity.
    normative = card['issue_kind'] in ('authorization_scope', 'holder_consent_scope', 'lifecycle_stage')
    assessment = 'risk' if normative and card['actor_holder_relation'].strip() and card['risk_explanation'].strip() else 'investigate'
    row = dict(id='audit_'+digest([effect, card['issue_kind']])[:18], anchors=[name], effect=card['effect_ref'],
               assessment=assessment, claim=claim, policy_basis=card['actor_holder_relation'],
               normal_explanation=card['normal_alternative'], distinguishing_question=card['decisive_missing_fact'],
               next_check=hint, category='AC' if inv.f.options.scope=='AC' else None,
               _audit_check=check, _audit_kind=card['issue_kind'])
    return row, None

```

## source/src/pr_next_joint/investigation/semantic_claims.py

原文件SHA256 `da974255a59bd894c809094d3a0d375a7d5ac3c8fed4b4f7126e33e4e3dc883b`

```python
"""Small, polarity-preserving interpretation of source-bound semantic proposals.

This layer does not infer asset meaning from Solidity names.  It distinguishes
an assertion from its negation/question before the existing source binder can
use it. Ambiguous free text requires a focused answer; a keyword is not proof.
"""
import re


FINANCIAL = re.compile(
    r"\b(?:tokens?|tokenized|redeemable|financial\s+(?:assets?|rights?|balances?)|"
    r"holders?['’]?s?\s+(?:balances?|rights?)|asset\s+ledger)\b|代币|可兑付|金融资产|资产权益", re.I)
COUNTER = re.compile(
    r"\b(?:non[- ]?financial(?:\s+counter)?|(?:service|request|usage|event|call)\s+(?:requests?|counts?|counter|number)|"
    r"(?:counts?|records?)\s+(?:only\s+)?(?:service\s+)?requests?)\b|非金融|服务请求|普通计数|调用次数|事件次数", re.I)
UNCERTAIN = re.compile(
    r"\b(?:whether|unclear|unknown|uncertain|determine|investigate|question|might|may\s+(?:be|represent)|"
    r"could\s+(?:be|represent)|not\s+(?:yet\s+)?(?:established|determined|known|clear)|"
    r"assuming|suppos(?:e|ing)|if\s+(?:this|the\s+\w+)\s+(?:is|represents))\b|"
    r"是否|尚不|无法确定|不确定|待确定|含义未明|假设|假如|若.{0,18}(?:代表|表示|属于)", re.I)
NEGATION = re.compile(
    r"\b(?:not|never|neither|nor|no|without|non[- ]|doesn't|isn't|aren't|isnt|doesnt|cannot)\b|"
    r"(?:不|并非|不是|不属于|不表示|不代表|不涉及|无)(?:是|属于|表示|代表|涉及)?", re.I)
NEGATED_NEGATION = re.compile(r"\b(?:not\s+only|not\s+merely|not\s+just)\b|不仅|不只是", re.I)
ASSERTION = re.compile(
    r"\b(?:is|are|represent\w*|record\w*|hold\w*|store\w*|track\w*|balance|ledger|"
    r"mint\w*|issu\w*|burn\w*|destroy\w*|transfer\w*|debit\w*|credit\w*|clear\w*|"
    r"reset\w*|withdraw\w*|redeem\w*|freeze\w*|block\w*|token)\b|"
    r"表示|代表|记录|保存|持有|余额|账本|发行|增发|转账|销毁|冻结|扣减|清零|权益", re.I)
MEANING_VERB=re.compile(r'\b(?:represent\w*|denot\w*|constitut\w*|signif\w*|mean\w*|record\w*|store\w*|track\w*)\b|表示|代表|属于|构成|记录|保存',re.I)
ACTION_VERB=re.compile(r'\b(?:transfer\w*|withdraw\w*|redeem\w*|mint\w*|issu\w*|burn\w*|destroy\w*|freeze\w*|block\w*|debit\w*|credit\w*|reduce\w*|clear\w*|spend\w*)\b|转移|转账|提取|兑付|增发|销毁|冻结|扣减|清零',re.I)


def negates_meaning(prefix):
    """Negation of an operation is not negation of the object's asset meaning."""
    prefix=NEGATED_NEGATION.sub('',prefix[-140:])
    negatives=list(NEGATION.finditer(prefix))
    if not negatives:return False
    tail=prefix[negatives[-1].end():]
    semantic=list(MEANING_VERB.finditer(tail));actions=list(ACTION_VERB.finditer(tail))
    if actions and (not semantic or actions[-1].end()>semantic[-1].end()):return False
    if semantic:return True
    # Direct adjectival/copular negation; long unidentified clauses are not
    # guessed to be asset denials.
    return bool(re.fullmatch(r"\s*(?:(?:a|an|the|any|actual|really|necessarily|genuine|longer|as|be|being|of|assets?|rights?|tokens?|balances?|or|nor|and)\s+){0,8}",tail,re.I)
                or re.fullmatch(r'(?:是|属于|表示|代表|任何|真正的|实际的|一种|一个|可)?\s*',tail))


def clauses(text):
    # Contrast and punctuation delimit negation scope. A question/conditional
    # marks the full sentence, including clauses after a comma or semicolon.
    result=[]
    for sentence in re.split(r'(?<=[.!?。！？])\s*|\n+', str(text or '')):
        if not sentence.strip():continue
        uncertain=bool(UNCERTAIN.search(sentence) or '?' in sentence or '？' in sentence)
        for part in re.split(r';|；|,|，|\bbut\b|\bwhereas\b|\bhowever\b|但是|但(?:是)?|而非',sentence,flags=re.I):
            part=part.strip()
            if part:result.append((part,uncertain))
    return result


def resource_assertion(text, answer=None):
    """Return supported polarity and original spans, never a truth boolean.

    Exact short choices remain supported. Their explanation cannot expressly
    contradict the choice. Mixed/conditional claims are left unresolved.
    """
    text=str(text or '').strip();positive=[];negative=[];questions=[];counter=[];incidental=[]
    for clause,uncertain in clauses(text):
        terms=list(FINANCIAL.finditer(clause))
        counter_terms=list(COUNTER.finditer(clause))
        if uncertain and (terms or counter_terms):
            questions.append(clause);continue
        for match in counter_terms:
            if negates_meaning(clause[:match.start()]):
                continue
            counter.append(clause)
        if not terms:continue
        if uncertain:questions.append(clause);continue
        for term in terms:
            before=clause[:term.start()]
            # Denying that an action is an asset event does not assert either
            # asset ownership or nonfinancial meaning. Preserve an independent
            # explicit meaning statement instead of manufacturing a conflict
            # from the noun inside this denied event relation.
            if re.search(r'\b(?:is|are|constitutes?)\s+(?:not|never)\s+(?:an?\s+)?'
                         r'(?:destruction|transfer|issuance|minting|redemption|withdrawal|'
                         r'freezing|payment|burning)\s+of\s+(?:the\s+)?$',before,re.I):
                incidental.append({'span':clause,'term':term.group(),'relation':'denied_event_not_resource_assertion'})
                continue
            # Negation after an independent finite verb belongs to that other
            # statement. The supported language deliberately avoids guessing
            # through nested explanations and reported speech.
            window=before[-140:]
            if re.search(r"\b(?:claim\w*|alleg\w*|suggest\w*)\b.{0,35}$",window,re.I):
                questions.append(clause);continue
            neg=negates_meaning(window)
            if neg:negative.append({'span':clause,'term':term.group(),'polarity':'negative'})
            elif ASSERTION.search(clause):positive.append({'span':clause,'term':term.group(),'polarity':'positive'})
            else:questions.append(clause)
    choices={'financial_right':'financial_right','token_ledger':'financial_right',
             'redeemable_credit':'financial_right','nonfinancial_counter':'nonfinancial_counter'}
    requested=choices.get(str(answer or '').strip())
    negative_only=bool(negative or counter) and not positive
    if requested=='financial_right':
        meaning=None if negative or counter or questions else requested
    elif requested=='nonfinancial_counter':
        meaning=None if positive or questions else requested
    elif positive and not negative and not questions and not counter:
        meaning='financial_right'
    elif (negative or counter) and not positive and not questions:
        meaning='nonfinancial_counter'
    else:meaning=None
    token_positive=any(re.search(r'\btokens?\b|代币',x['term'],re.I) for x in positive)
    return {'meaning':meaning,'positive_spans':positive,'negative_spans':negative,
        'counter_spans':counter,'unresolved_spans':questions,'nonassertive_event_mentions':incidental,'requested_choice':requested,
        'unit_kind':'token' if token_positive else 'unspecified_financial',
        'polarity_preserved':True,'original_text':text,
        'status':'asserted' if meaning else 'semantic_polarity_or_scope_unresolved'}


def normal_proposal(item, explicit=None):
    if explicit and explicit.get('meaning')=='normal_authorization':
        return {'text':explicit.get('basis',''),'source':'focused_model_answer','id':explicit.get('id')}
    if item.get('assessment')!='normal':return None
    text=' '.join(str(item.get(k) or '') for k in ('claim','alternative','revision_reason','normal_basis'))
    return {'text':text,'source':'model_normal_proposal'} if text.strip() else None

```

## source/src/pr_next_joint/investigation/semantic_rules.py

原文件SHA256 `1bd945c0676f63e05a18b733c435f607a222eb2a197360a85fd5d90b3041fd1d`

```python
"""Typed semantic supports over the existing source summaries. No graph edge or model label is a verdict."""
from collections import defaultdict, deque
import copy
import re
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key,walk
from pr_next_joint.frontend.storage import keys, value_type
from .summary import local_delta, holder, has_basis
from .initial_state import domain
from .key_roles import relation as key_relation
from .protocol import role_error

RESOURCE={'financial_right','nonfinancial_counter'}
CONSENT={'gross_debit_bound','net_request_with_fee'}
AUTH={'current_authority_required','holder_authorization_applies','initialization_stage'}
def loc_key(loc):
    return (loc.get('file'),loc.get('start'),loc.get('length'))
def field_node(cell):
    return next((seg['field'] for seg in reversed(cell.get('segments',())) if 'field' in seg),cell['root'])


class SupportIndex:
    """Input and derived facts share identities. Re-ground only descendants of edited roots."""
    def __init__(self, remaining):
        self.remaining=remaining
        self.roots=defaultdict(set)
        self.edges=defaultdict(set)
        self.children=defaultdict(set)
        self.live=set()
        self.pending=set()
        self.cut=False
        self.visits=0
        self.certificates={};self.proof_rules={}

    def rule(self, conclusion, inputs, rule):
        clause=(rule,tuple(sorted(set(inputs))))
        if not clause[1] or clause in self.edges[conclusion]:return
        self.edges[conclusion].add(clause)
        for fact in clause[1]:self.children[fact].add(conclusion)
        self.pending.add(conclusion)

    def update(self, fact, support, active):
        changed=(support in self.roots[fact])!=bool(active)
        if active:self.roots[fact].add(support)
        else:self.roots[fact].discard(support)
        if changed:self.pending.add(fact)

    def valid(self,fact):
        if self.roots.get(fact):return True
        certificate=self.certificates.get(fact)
        return fact in self.live and bool(certificate) and all(sid in self.roots.get(node,()) for node,sid in certificate)

    def settle(self):
        if not self.pending:return set()
        self.cut=False
        affected=set(self.pending); todo=deque(sorted(affected))
        before={node for node in affected if node in self.live}
        while todo:
            node=todo.popleft()
            for child in self.children[node]:
                if child not in affected:
                    affected.add(child);todo.append(child)
                    if child in self.live:before.add(child)
            if self.remaining()<=0:
                # A stale positive must never survive an incomplete retraction.
                self.cut=True
                return {x for x in affected if (x in before)!=self.valid(x)}
        self.live.difference_update(affected)
        ready=deque(sorted(affected))
        while ready:
            if self.remaining()<=0:
                self.cut=True;break
            node=ready.popleft();self.visits+=1
            if node in self.live:continue
            roots=self.roots.get(node)
            proof=None;used_rules=set()
            if roots:proof=frozenset(((node,min(roots)),))
            else:
                for rule,terms in sorted(self.edges.get(node,())):
                    if all(x in self.live and self.valid(x) for x in terms):
                        proof=frozenset().union(*(self.certificates[x] for x in terms))
                        used_rules={rule}.union(*(self.proof_rules.get(x,()) for x in terms))
                        break
            if proof:
                self.certificates[node]=proof;self.proof_rules[node]=used_rules;self.live.add(node)
                ready.extend(n for n in self.children[node] if n in affected and n not in self.live)
        if not self.cut:self.pending.clear()
        return before.symmetric_difference({x for x in affected if self.valid(x)})

    def basis(self, fact):
        # Already grounded provenance stays readable even at the cutoff; no rule runs here.
        if not self.valid(fact):return [],[]
        origins=set(self.roots.get(fact,()));rules=set()
        cert=self.certificates.get(fact,())
        if cert and all(sid in self.roots.get(node,()) for node,sid in cert):
            origins.update(sid for _,sid in cert);rules.update(self.proof_rules.get(fact,()))
        todo=[fact];seen=set()
        while todo and self.remaining()>0:
            n=todo.pop()
            if n in seen or not self.valid(n):continue
            seen.add(n);origins.update(self.roots[n])
            for rule,terms in self.edges[n]:
                if all(self.valid(x) for x in terms):rules.add(rule);todo.extend(terms)
        return sorted(origins),sorted(rules)


class ScopedRules:
    """Indexes refer to compiler-selected declarations and individual applied source writes."""
    def __init__(self,inv):
        self.inv=inv;self.f=inv.f;self.logic=SupportIndex(inv.program_remaining)
        self.objects={};self.effects={};self.aliases=defaultdict(set);self.used=defaultdict(set)
        self.by_decl=defaultdict(set);self.by_operation=defaultdict(set);self.routes=defaultdict(list)
        self.local_readers=defaultdict(set)
        self.supports={};self.facts={};self.by_handle=defaultdict(set)
        self.built=False;self.incomplete=set();self.declaration_lookups=set()
        self.events=[];self.history=[];self.last_changes=set();self.epoch=0

    def remaining(self):
        return self.inv.program_remaining()>0

    def obj(self,target,rid,oid=None):
        return 'o_'+digest([self.f.bundle['build_id'],target,rid,oid])[:20]

    def index(self):
        if self.built:return
        self.built=True
        from pr_next_joint.frontend.storage import selectors
        self.guard_declarations=set()
        for oid,operation in self.f.operations.items():
            if not self.remaining():self.incomplete.update(set(self.f.operations)-set(self.by_operation));break
            if operation.get('generated_getter'):continue
            target=operation['target'];lookup=self.f.lookup(oid)
            for row in self.f.summaries.rows(oid):
                if not self.remaining():self.incomplete.add(oid);break
                self.guard_declarations.update((target,c['root']) for c in selectors(row['guards']))
                self.index_observed_effects(oid,row)
                raw=self.f.paths[row['path']]['raw']
                for wi,w in enumerate(row['ordered_writes']):
                    if not self.remaining():self.incomplete.add(oid);break
                    cell=w['path'];rid=field_node(cell);loc=w['source']
                    effect='w_'+digest([self.f.bundle['build_id'],target,oid,row['path'],wi,loc,cell])[:20]
                    desc=dict(oid=oid,target=target,path=row['path'],where=loc,cell=cell,
                              version=wi,conditions=digest(row['guards']),write=w,clean=not row['residuals'])
                    self.effects[effect]=desc;self.by_operation[oid].add(effect)
                    name=lookup.nodes.get(rid,{}).get('name')
                    if not name:continue
                    obj=self._declare(target,rid,None,lookup)
                    self.by_decl[obj].add(effect)
                    fn=operation['function']
                    self._names(effect,target,fn+'#'+name)
                    sign,_=local_delta(w)
                    if sign:self._names(effect,target,fn+'#'+name+('~debit' if sign=='-' else '~credit'))
                    self._names(effect,target,fn)
                    self.aliases['effect:'+effect[2:]].add(effect)
                    self.used[obj].add(oid)
                    sign,qty=local_delta(w)
                    # Edges retain evaluated subterms; effects depending on opaque values remain open at consumption.
                    # Read provenance comes from the evaluated, substituted expression; a shared root is insufficient.
                    for kind,expr in [('value',qty if qty is not None else w['value']),('key',keys(cell)),('guard',row['guards'])]:
                        for term in walk(expr):
                            if not self.remaining():self.incomplete.add(oid);break
                            if term.get('kind') not in ('parameter','storage'):continue
                            pid=term['id'] if term['kind']=='parameter' else field_node(term)
                            source=self._declare(target,pid,oid if term['kind']=='parameter' else None,lookup)
                            self.used[source].add(oid)
                            rules=['P03'] if term['kind']=='storage' else []
                            if kind=='guard':rules.append('P05')
                            if row['guards']:rules.append('P06')
                            if kind=='value':
                                if qty is not None:rules.append('P04')
                                if any(k.get('kind')=='parameter' and k.get('id')==pid for k in walk(raw.get('copy_origins',[]))):rules.append('P01')
                                for call in raw.get('read_calls',[]):
                                    if call.get('binding') not in ('compiler_internal_declaration','compiler_bound_qualified_ancestor','compiler_bound_internal_pure_library'):continue
                                    if key(call.get('return_value'))==key(term) and any(key(a)==key(term) for a in call.get('arguments',[])):
                                        rules.append('P02')
                                        if any(key(x.get('value'))==key(term) for x in call.get('copies',[])):rules.append('P01')
                            route=(effect,kind,tuple(dict.fromkeys(rules)),key(expr)==key(term))
                            if route not in self.routes[source]:self.routes[source].append(route)


    def index_observed_effects(self,oid,row):
        """Index a compiler-located effect as an occurrence, never as an inferred write.
        Distinct branches share the source occurrence and keep their own conditions."""
        target=self.f.operations[oid]['target'];fn=self.f.operations[oid]['function']
        for term in row['effects']:
            if not self.remaining():self.incomplete.add(oid);return
            loc=term.get('source') or {};kind=term.get('kind')
            if not kind or not loc.get('file') or loc.get('start') is None:continue
            effect='e_'+digest([self.f.bundle['build_id'],target,oid,loc_key(loc),kind,
                                term.get('to') or term.get('recipient'),term.get('amount'),term.get('callpoint_guards',row['guards'])])[:20]
            d=self.effects.setdefault(effect,dict(oid=oid,target=target,where=loc,kind=kind,branches={}))
            d['branches'][row['path']]={'conditions':digest(row['guards']),'has_residuals':bool(row['residuals'])}
            self.by_operation[oid].add(effect)
            self._names(effect,target,fn);self._names(effect,target,fn+'#'+kind)

    def declaration_by_ref(self,reference):
        # Bind a uniquely named declaration in the actual applied inheritance scope on demand.
        if reference in self.declaration_lookups:return
        self.declaration_lookups.add(reference)
        for target in self.inv.catalog.targets:
            aliases=(target+'.',target.rsplit(':',1)[-1]+'.')
            name=next((reference[len(prefix):] for prefix in aliases if reference.startswith(prefix)),None)
            if not name or not re.fullmatch(r'[\w$]+',name):continue
            lookup=self.f.lookups[target]
            bases=lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
            for base in bases:
                if not self.remaining():return
                for node in lookup.nodes[base].get('nodes',()):
                    if node.get('stateVariable') and node.get('name')==name:
                        self._declare(target,node['id'],None,lookup)

    def _names(self,h,target,name):
        for t in (target,target.rsplit(':',1)[-1]):self.aliases[t+'.'+name].add(h)

    def _declare(self,target,rid,oid,lookup):
        handle=self.obj(target,rid,oid)
        if handle in self.objects:return handle
        node=lookup.nodes.get(rid,{})
        name=node.get('name','')
        self.objects[handle]=dict(target=target,decl=rid,oid=oid,where=lookup.anchor(node) if node.get('src') else {},name=name)
        if name:
            self._names(handle,target,self.f.operations[oid]['function']+'#'+name if oid else name)
        self.aliases['obj:'+handle[2:]].add(handle)
        return handle

    def visible(self,handle,manifest):
        rec=self.objects.get(handle) or self.effects.get(handle)
        if not rec:return False
        where=rec['where']
        if where.get('file') in manifest.get('complete_source_files',[]):return True
        for a in manifest.get('visible_spans',()):
            if where.get('file')==a.get('file') and a['start']<=where['start'] and where['start']+where['length']<=a['start']+a['length']:return True
        return False

    def bind(self,ref,manifest,kind=None):
        if not isinstance(ref,str):return None
        if ref.startswith(('obj:','effect:')):
            hs={manifest.get('typed_index',{}).get(ref)}
        else:
            if kind!='effect':self.declaration_by_ref(ref)
            hs=self.aliases.get(ref,set())
        if not hs and isinstance(ref,str) and not ref.startswith(('obj:','effect:','sem:')):
            # A source span may denote a declaration or a write if there is a unique applied identity.
            m=re.fullmatch(r'(.+[.]sol)@(\d+)\+(\d+)',ref)
            if m:
                at=(m[1],int(m[2]),int(m[3]))
                pool=self.objects if kind=='obj' else self.effects if kind=='effect' else {**self.objects,**self.effects}
                hs={hh for hh,r in pool.items() if loc_key(r['where'])==at}
        hs={v for v in hs if v and ((kind!='effect' and v in self.objects) or (kind!='obj' and v in self.effects)) and self.visible(v,manifest)}
        # A declaration/entry label cannot arbitrarily pick one of its writes.
        return next(iter(hs)) if len(hs)==1 else None

    def effect_focus(self,e):
        # Index actual applied occurrences, including compiler-resolved helper effects.
        d=self.effects[e]
        if 'write' not in d:
            return {'native_selfdestruct': 'termination', 'native_transfer':'funds',
                    'dangerous_external_call':'call_authority'}.get(d['kind'])
        from .summary import holder
        w=d['write'];cell=d['cell'];lookup=self.f.lookup(d['oid'])
        if holder(cell,lookup) and local_delta(w)[0]:
            row=self.f.summaries.paths[d['path']]
            if local_delta(w)[0]=='+' and not any(local_delta(v)[0]=='-' for v in row['ordered_writes']):
                return 'credit'
            return 'account_movement'
        if (d['target'],cell['root']) in self.guard_declarations:
            return 'qualification'
        return None

    def overwritten(self,e):
        d=self.effects[e]
        if 'write' not in d:return False
        later=self.f.summaries.paths[d['path']]['ordered_writes'][d['version']+1:]
        return any(key(w['path'])==key(d['cell']) for w in later)

    def occurrence(self,e):
        d=self.effects[e]
        return (d['target'],d['oid'],loc_key(d['where']),d.get('kind','write'),
                key(d.get('cell')),d.get('conditions') or (e if 'branches' in d else None),d.get('version'))

    def register_sensitive_effects(self):
        self.index()
        if not hasattr(self,'sensitive_effects'):
            from .candidates import source_duty
            self.source_duties={}
            self.sensitive_effects={}
            self.occurrences=defaultdict(list)
            for e,d in self.effects.items():
                if not self.remaining():self.incomplete.add(d['oid']);continue
                kind=self.effect_focus(e)
                if kind:
                    self.sensitive_effects[e]=kind
                    if self.f.options.scope=='AC':
                        relation=source_duty(self,e,kind)
                        if relation:self.source_duties[e]=relation
                    self.occurrences[self.occurrence(e)].append(e)
            from .shared_effect_bridge import index_authority_consumers
            self.authority_bridges = index_authority_consumers(self)
            self.bridges_at = defaultdict(set)
            for identity, link in self.authority_bridges.items():
                for endpoint in (link['writer'], link['reader']):
                    self.bridges_at[endpoint].add(identity)

    def cards_for(self,manifest,focus):
        self.register_sensitive_effects()
        focused=set(focus)
        wanted=set(manifest.get('disputed_effects',()))
        buckets=defaultdict(deque)
        def rank(e):
            d=self.effects[e]
            return (e not in wanted,d['oid'] not in focused,d['where']['start'],e)
        for e in sorted((g[0] for g in self.occurrences.values()),key=rank):
            d=self.effects[e]
            if manifest.get('mode')=='focused_evidence' and d['oid'] not in focused:continue
            if self.visible(e,manifest):buckets[(d['target'],self.sensitive_effects[e])].append(e)
        order=('qualification','funds','termination','call_authority','credit','account_movement')
        queues=[buckets[k] for k in sorted(buckets,key=lambda k:(rank(buckets[k][0])[:2],order.index(k[1]),k[0]))]
        handles=[]
        while queues:
            for q in queues:handles.append(q.popleft())
            queues=[q for q in queues if q]
        if self.f.options.scope=='FCR':
            objs=[]
            for e in handles:
                d=self.effects[e]
                if 'cell' in d and self.sensitive_effects[e] in ('credit','account_movement'):
                    h=self.obj(d['target'],field_node(d['cell']))
                    if h in self.objects and self.visible(h,manifest):objs.append(h)
            handles=list(dict.fromkeys(objs))+handles
        for oid in focus:
            for e in sorted(self.by_operation.get(oid,())):
                d=self.effects[e]
                if 'cell' in d:
                    h=self.obj(d['target'],field_node(d['cell']))
                    if h in self.objects and self.visible(h,manifest):handles.append(h)
        cards=[];index={}
        for h in dict.fromkeys(handles):
            d=self.effects.get(h) or self.objects[h]
            ref=('effect:' if h in self.effects else 'obj:')+h[2:14]
            if ref in index:ref+=h[14:]
            if h in self.effects:
                name=self.f.lookup(d['oid']).nodes[field_node(d['cell'])]['name'] if 'cell' in d else d['kind']
                card=[ref,self.inv.catalog.name(d['oid'])+'#'+name,self.sensitive_effects[h]]
                if 'write' in d:
                    direction=local_delta(d['write'])[0]
                    if direction and keys(d['cell']):
                        party=holder(d['cell'],self.f.lookup(d['oid'])) or {}
                        label='caller' if party.get('kind')=='actual_sender' else self.f.lookup(d['oid']).nodes.get(party.get('id'),{}).get('name','account')
                        card.append(('debit ' if direction=='-' else 'credit ')+label)
            else:
                name=(self.inv.catalog.name(d['oid'])+'#' if d.get('oid') else d['target'].rsplit(':',1)[-1]+'.')+d['name']
                card=[ref,name]
            cards.append(card);index[ref]=h
        return cards,index

    def issue_effect(self,item,manifest):
        """Bind a model locator to the authenticated applied occurrence for this message."""
        anchors=item.get('anchors',[])
        oid=None
        if anchors:
            bind=self.inv.catalog.bind(anchors,core=item.get('root'))
            oid=bind.get('core_operation') if bind.get('core_exact') else None
        named=item.get('effect')
        if named is not None:
            e=self.bind(named,manifest,'effect')
            if not e:return None,'unknown_or_unshown_effect'
            d=self.effects[e]
            if anchors and (oid!=d['oid'] or bind.get('unresolved') or bind.get('ambiguous')):
                return None,'explicit_effect_anchor_conflict'
            if item.get('root') and d['oid'] not in self.inv.catalog.resolve(item['root']):
                return None,'explicit_effect_root_conflict'
        else:
            if not oid:return None,None
            choices={self.occurrence(e):e for e in self.by_operation[oid] if e in self.sensitive_effects and self.visible(e,manifest)}
            if len(choices)!=1:return None,None
            e=next(iter(choices.values()));d=self.effects[e]
        matches=self.occurrences.get(self.occurrence(e),[e])
        return (d['oid'],list(matches)),None

    def scoped_issue(self,item,manifest):
        located,error=self.issue_effect(item,manifest)
        if error or not located:return item,error
        oid,effects=located
        row=dict(item,_scope_effects=effects,_opinion_message=manifest['messages_sha256'])
        if not row['anchors']:row['anchors']=[self.inv.catalog.name(oid)]
        if item.get('subject'):
            subject=self.bind(item['subject'],manifest,'obj')
            if not subject or self.objects[subject]['target']!=self.effects[effects[0]]['target']:return item,'explicit_principal_not_bound'
            row['_opinion_subject']=subject
        return row,None

    def fact(self,h,meaning,subject=None,scope=None,role=None,payment_policy=None):
        identity=[self.f.identity,h,meaning,subject,scope,role]
        if payment_policy is not None:identity.append(payment_policy)
        fid='fact_'+digest(identity)[:20]
        if fid not in self.facts:
            self.facts[fid]=dict(handle=h,meaning=meaning,subject=subject,scope=scope,role=role)
            if payment_policy is not None:self.facts[fid]['payment_policy']=payment_policy
            self.by_handle[h].add(fid)
        return fid

    def row_scope(self,field,row,manifest,previous=None):
        meaning=row.get('meaning',previous and previous['meaning'])
        if not isinstance(meaning,str):return None
        locator,kind=('on','obj') if field=='annotations' else ('effect','effect')
        h=previous['handle'] if previous else None
        if locator in row:
            named=self.bind(row[locator],manifest,kind)
            if named is None or h is not None and named!=h:return None
            h=named
        if not h:return None
        def qualifier(name):
            if name in row:return self.bind(row[name],manifest)
            return previous.get(name) if previous else None
        subject=qualifier('subject');scope=qualifier('scope')
        if any(name in row and not val for name,val in [('subject',subject),('scope',scope)]):return None
        d=self.effects.get(h) or self.objects[h]
        if any((self.effects.get(v) or self.objects[v])['target']!=d['target'] for v in (subject,scope) if v):return None
        if subject and meaning in RESOURCE|CONSENT and subject not in self.objects:return None
        if scope and scope!=h and scope not in self.by_decl.get(h,set()) and not any(e==scope for e,_,_,_ in self.routes.get(h,())):return None
        if meaning in AUTH|CONSENT|RESOURCE and subject and subject not in self.objects:return None
        if meaning in CONSENT and not list(self.quantity_scopes(h)):return None
        role=row.get('role',previous.get('role') if previous else None)
        if h in self.effects and meaning in CONSENT and subject:
            decl=self.objects[subject]['decl']
            if not all(any(t.get('id')==decl for t in walk(keys(route['grant'])[route['issuer_key']])) for route in self.quantity_scopes(h)):return None
        proposal=dict(handle=h,meaning=meaning,subject=subject,scope=scope,role=role)
        if meaning=='current_authority_required' and h in self.effects:
            cell=self.authority_cell(h,subject)
            if cell:
                from .policy_binding import payment_policy
                lookup=self.f.lookup(d['oid'])
                names={self.f.operations[d['oid']]['function'].split('(')[0]}
                if 'cell' in d:names.add(lookup.nodes.get(field_node(d['cell']),{}).get('name'))
                stated=payment_policy(row.get('basis',''),lookup.nodes[cell['root']]['name'],names)
                inherited=(previous or {}).get('payment_policy')
                if stated or inherited:proposal['payment_policy']=stated or inherited
        return proposal

    def quantity_scopes(self,e):
        d=self.effects.get(e)
        if not d or 'write' not in d:return
        for a in self.f.summaries.dependencies.amounts_for(d['oid']):
            if a['path']!=d['path']:continue
            for dec in a['deltas']:
                if dec['sign']!='-' or dec['write_index']!=d['version'] or dec.get('key_role')=='authorization_quantity':continue
                for gate in a['allowance_gates']:
                    grant=gate['grant'];issuer=keys(grant)[gate['issuer_key']]
                    if key(issuer)!=key(dec.get('holder')):continue
                    yield {'path':a['path'],'grant':grant,'issuer_key':gate['issuer_key'],'spender_key':gate['spender_key'],
                           'debit_expression':dec['amount_expression'],'checked_quantity_expression':gate['quantity_expression'],'ledger':dec['cell']}

    def register(self,fid,sid,origin,field):
        if sid in self.supports and (self.supports[sid]['active'] or self.supports[sid].get('withdrawn')):return False
        self.supports[sid]=dict(fact=fid,origin=origin,field=field,active=True,version=1+self.supports.get(sid,{}).get('version',0))
        self.logic.update(fid,sid,True)
        return True

    @staticmethod
    def revision_reason(row,proposed):
        """Location is authenticated separately. Discard output instructions and bare labels,
        leaving the model's own semantic explanation (in any source vocabulary)."""
        reason=row.get('basis','')
        if not has_basis(reason):return False
        clauses=re.split(r'[.;!?。；！？\n]+|\b(?:because|since)\b|因为|由于',reason,flags=re.I)
        directive=r'^(?:(?:please|just|kindly|we should|you should)\s+)*(?:remove|withdraw|cancel|drop|suppress|change|relabel|mark|classify|report|delete|downgrade|upgrade|dismiss|ignore)\b'
        for clause in clauses:
            clause=clause.strip()
            if not clause or re.match(directive,clause,re.I) or re.match(r'^(?:请|应当|应该|仅需|只要)*(?:撤回|删除|取消|改为|标记|移除|忽略)',clause):continue
            words=re.findall(r'[^\W_]+',clause.casefold())
            meta={'the','this','is','a','an','of','as','only','it','should','be','alarm','warning','finding','risk','safe','not','false','positive','wrong','correct','label','incorrect','unsupported'}
            meta.update(re.findall(r'[^\W_]+',proposed['meaning']))
            supplied={word for word in words if word not in meta}
            if len(supplied)>=2 or re.search(r'[\u3400-\u9fff]{4,}',clause):return True
        return False

    def hard_unit_conflict(self,proposal):
        if proposal['meaning']!='nonfinancial_counter':return False
        from .ledger import _unit_origin
        h=proposal['handle']
        candidates=self.by_decl.get(h,set())|{e for e,k,_,exact in self.routes.get(h,()) if k=='value' and exact}
        for e in candidates:
            if not self.remaining():return 'semantic_budget'
            if proposal['scope'] and proposal['scope']!=e:continue
            d=self.effects[e]
            if proposal['subject']:
                declared=self.objects[proposal['subject']]['decl']
                if not any(t.get('id')==declared for t in walk(keys(d['cell']))):continue
            if d['clean'] and holder(d['cell'],self.f.lookup(d['oid'])) and _unit_origin(self.inv.backend,d['oid'],d['cell']):return 'scoped_source_unit_conflict'
        return False

    def apply(self,value,manifest,revision=False):
        """Stage unrelated updates separately; an ambiguous alias can never displace a valid support."""
        rows=[(field,r) for field in ('annotations','policies') for r in value.get(field,())]
        requests=defaultdict(list)
        for field,row in rows:
            identity=row.get('ref') or row.get('id')
            if isinstance(identity,str):requests[identity].append((field,row))
        conflicting={k for k,items in requests.items() if len({digest(x) for x in items})>1}
        accepted=[];rejected=[];changed=set();row_results=[];self.submission=manifest.get('messages_sha256')
        errors_with_rows=[]
        ordinals=defaultdict(int)
        for field,row in rows:
            pos=ordinals[field];ordinals[field]+=1
            wire_positions=value.get('row_positions',{}).get(field,())
            pos=wire_positions[pos] if pos<len(wire_positions) else pos
            outcome={'field':field,'index':pos,'ref':row.get('ref'),'accepted':False}
            row_results.append(outcome)
            def committed(support, fact):
                accepted.append(support)
                outcome.update(accepted=True,support=support,fact=fact)
            def reject(reason,detail=None):
                rejected.append(reason)
                errors_with_rows.append({'reason':reason,'stage':'focused_revision' if revision else (self.inv.session.attempts[-1]['phase'] if self.inv.session.attempts else 'initial'),'list':field,'index':pos,'field':'ref' if row.get('ref') else 'effect' if field=='policies' else 'on','subreason':'source_binding',**(detail or {})})
            if not self.remaining():reject('semantic_budget');break
            ref=row.get('ref');name=ref or row.get('id')
            if name is not None and (not isinstance(name,str) or name in conflicting):reject('ambiguous_seed_id');continue
            old=None;sid=None;action=row.get('action','add')
            current=None
            if ref:
                wire=manifest.get('shown_supports',{}).get(ref,{})
                sid=wire.get('support');old=self.supports.get(sid)
                if not revision or not old or not old['active'] or old['origin'] not in ('fixture','verified_service') or old['version']!=wire.get('version') or old['fact']!=wire.get('fact'):
                    reject('stale_or_undisplayed_support');continue
                if field!=old['field'] or field!=wire.get('field'):
                    reject('wrong_semantic_facet');continue
                current=self.facts[old['fact']]
                locator,kind=('on','obj') if field=='annotations' else ('effect','effect')
                if locator in row and self.bind(row[locator],manifest,kind)!=current['handle']:
                    reject('revision_object_mismatch');continue
            issue=role_error(row,row.get('meaning',(current or {}).get('meaning')),(current or {}).get('role'))
            if issue:
                actual=row.get('role')
                reject('invalid_semantic_row',{'field':'role','subreason':issue,'actual_type':type(actual).__name__,
                    'value_length':len(actual) if isinstance(actual,str) else None,'value_sha256':digest(actual)})
                continue
            if row.get('meaning',(current or {}).get('meaning'))=='initialization_stage' and 'subject' not in row and not (current or {}).get('subject'):
                reject('invalid_semantic_row',{'field':'subject','subreason':'field_absent','actual_type':'NoneType'})
                continue
            proposed=self.row_scope(field,row,manifest,current)
            if not proposed:
                reject('unbound_or_inapplicable_seed');continue
            if current:
                if action in ('confirm','withdraw') and proposed!=current:
                    reject('revision_conflicts_with_displayed_support');continue
                if action=='confirm':
                    committed(sid,old['fact']);continue
                if action=='narrow':
                    if current['scope'] or proposed['scope'] not in self.effects or proposed['scope']==current['handle'] or any(proposed[k]!=current[k] for k in ('meaning','subject','role')):
                        reject('scope_not_strictly_narrower');continue
                elif proposed['scope']!=current['scope']:
                    reject('scope_change_requires_narrow');continue
                if not self.revision_reason(row,proposed):
                    reject('revision_without_scoped_reason');continue
                if action=='correct':
                    conflict=self.hard_unit_conflict(proposed)
                    if conflict:
                        reject(conflict);continue
            fid=None if action=='withdraw' else self.fact(proposed['handle'],proposed['meaning'],proposed['subject'],
                proposed['scope'],proposed['role'],proposed.get('payment_policy'))
            if old:
                if fid==old['fact']:committed(sid,fid);continue
                self.history.append({'action':action,'support':sid,'before':old['fact'],'after':fid,'from_version':old['version'],'to_version':old['version']+1})
                self.logic.update(old['fact'],sid,False);changed.add(old['fact'])
                old.update(active=False,withdrawn=True,version=old['version']+1)
            if fid:
                sid=sid or 'support_'+digest([value['origin'],manifest.get('messages_sha256'),fid])[:20]
                if old:
                    old.update(active=True,withdrawn=False,fact=fid);self.logic.update(fid,sid,True)
                else:self.register(fid,sid,value['origin'],field)
                self.derive(fid);changed.add(fid)
            committed(sid,fid or old['fact'])
        value['semantic_binding_events']=row_results
        live_delta=self.logic.settle()
        self.last_changes={self.facts[f]['handle'] for f in live_delta if f in self.facts}
        self.epoch+=bool(live_delta)
        for fid in changed:self.events.append({'fact':fid,'active':self.logic.valid(fid),'sources':len(self.logic.roots[fid])})
        value['binding_diagnostics']=errors_with_rows
        return accepted,rejected

    def derive(self,fid):
        queue=deque([fid]);visited=set()
        while queue and self.remaining():
            source=queue.popleft()
            if source in visited:continue
            visited.add(source)
            queue.extend(self._derive_one(source))
        for source in queue:self.incomplete.update(self.related_ops(self.facts[source]['handle']))

    def _derive_one(self,fid):
        src=self.facts[fid];h=src['handle']
        if h not in self.objects:return
        meaning=src['meaning']; role=src['role']
        if meaning in ('unknown','other_source_meaning','other_source_policy'):return
        for e,k,rules,exact in self.routes.get(h,()):
            if not self.remaining():self.incomplete.add(self.effects[e]['oid']);break
            if not self.effects[e]['clean']:continue
            if src['subject'] and src['subject']!=h:
                # A bound subject is never generalized to an entire mapping family.
                ref=self.objects.get(src['subject'],{})
                relevant=keys(self.effects[e]['cell'])
                if not any(t.get('id')==ref.get('decl') for t in walk(relevant) if 'id' in t):continue
            if src['scope'] and e!=src['scope']:continue
            if meaning=='transfer_condition' and k!='guard':continue
            if meaning in RESOURCE|{'fee_rule','price','amount_role'} and k!='value':continue
            if meaning in RESOURCE and (not exact or h in self.objects and self.objects[h]['oid'] is None):continue
            if meaning in {'management_role','eligibility_state'} and k not in ('guard','value','key'):continue
            if meaning=='authorization_quantity' and k!='guard':continue
            if meaning not in RESOURCE|{'fee_rule','price','amount_role','transfer_condition','authorization_quantity','management_role','eligibility_state'}:continue
            dest=self.fact(e,meaning,src['subject'],e,role)
            pre=fid
            # Intermediate facts carry the exact applied path. They are never global node labels.
            for rule in rules:
                link='der_'+digest([fid,e,k,rule,pre])[:20]
                self.logic.rule(link,[pre],rule);pre=link
            # The semantic interpretation and the committing source expression are independent premises.
            observed='sourcefact_'+digest([e,k,self.effects[e]['conditions'],self.effects[e]['version']])[:20]
            self.logic.update(observed,'source_'+observed[11:],True)
            self.logic.rule(dest,[pre,observed],{'key':'P03','value':'P04','guard':'P05'}[k])
            if k=='value' and exact and not src['scope'] and not src['subject']:
                following=self.index_transfer(h,e,fid,pre,'P07')
                if following:yield following

    def for_effect(self,e):
        d=self.effects[e]
        if 'cell' not in d:
            return sorted(fid for fid in self.by_handle[e] if self.logic.valid(fid) and self.facts[fid]['scope'] in (None,e))
        obj=self.obj(d['target'],field_node(d['cell']))
        def applicable(fid):
            f=self.facts[fid]
            if f['scope'] not in (None,e):return False
            if f['handle']==e:return True
            if f['subject']:
                ident=self.objects.get(f['subject'],{}).get('decl')
                if not any(t.get('id')==ident for t in walk(keys(d['cell'])) if 'id' in t):return False
            return True
        return sorted(f for f in self.by_handle[e]|self.by_handle[obj] if self.logic.valid(f) and applicable(f))

    def resource(self,oid,cell):
        """A source-level family reading or an exact, uniform reading of the committing writes."""
        target=self.f.operations[oid]['target'];obj=self.obj(target,field_node(cell))
        roots=[f for f in self.by_handle.get(obj,()) if self.logic.valid(f) and self.facts[f]['meaning'] in RESOURCE and not self.facts[f]['scope'] and not self.facts[f]['subject']]
        es=[e for e in self.by_operation.get(oid,()) if 'cell' in self.effects[e] and key(self.effects[e]['cell'])==key(cell)]
        local=[]
        for e in es:
            rows=[f for f in self.for_effect(e) if self.facts[f]['meaning'] in RESOURCE]
            if not rows:local=[];break
            local.extend(rows)
        effective=roots+local
        meanings={self.facts[f]['meaning'] for f in effective}
        if len(meanings)!=1:return None
        return {'meaning':meanings.pop(),'id':digest(sorted(set(effective))),'target':target,'operation':oid,
                'family':key(cell),'source':'scoped_semantic_support','business_policy_formally_proved':False}

    def managed_resource(self,oid,cell):
        obj=self.obj(self.f.operations[oid]['target'],field_node(cell))
        return any(self.facts[f]['meaning'] in RESOURCE for f in self.by_handle.get(obj,()) if not self.facts[f]['subject'] and not self.facts[f]['scope'])

    def support_inputs(self,effects):
        """All active source supports feeding these actual effects, including equivalent independent roots."""
        todo=[f for e in effects for f in self.for_effect(e)]
        seen=set();sids=set()
        while todo and self.remaining():
            fid=todo.pop()
            if fid in seen:continue
            seen.add(fid);sids.update(self.logic.roots.get(fid,()))
            for _,premises in self.logic.edges.get(fid,()):
                if all(self.logic.valid(pr) for pr in premises):todo.extend(premises)
        return sids

    def signature(self,oid):
        return sorted({f for e in self.by_operation.get(oid,()) for f in self.for_effect(e)})

    def public(self):
        return {'source_effect_readings':[{'effect':e,'kind':k,'operation':self.effects[e]['oid'],
                 'where':self.effects[e]['where'],'stage':'constructor' if self.f.lookup(self.effects[e]['oid']).function(self.f.operations[self.effects[e]['oid']]['function']).get('kind')=='constructor' else 'applied_entry',
                 'shown_followup':e in (self.inv.context.last_manifest or {}).get('displayed_effect_handles',()) and (self.inv.context.last_manifest or {}).get('mode')=='focused_evidence',
                 'source_duty':getattr(self,'source_duties',{}).get(e,{}).get('duty'),
                 'source_support_location':getattr(self,'source_duties',{}).get(e,{}).get('support'),
                 'opinion_consumers':sorted(getattr(self,'local_readers',{}).get(e,())),
                 'shown':e in (self.inv.initial_manifest or {}).get('displayed_effect_handles',()),
                 'bound_facts':sorted(self.for_effect(e)),
                 'scoped_consumers':sorted(getattr(self,'effect_consumers',{}).get(e,()))}
                 for e,k in getattr(self,'sensitive_effects',{}).items()],
                'retired_supports':[{'support':sid,'fact':s['fact'],'field':s['field'],'version':s['version']} for sid,s in self.supports.items() if not s['active']], 'active_supports':[{'support':sid,'fact':row['fact'],'origin':row['origin'],'field':row['field'],'version':row['version']} for sid,row in sorted(self.supports.items()) if row['active']],
                'updates':list(self.events),'revisions':list(self.history),
                'referenced_abstract_effects':[{'effect':h,'operation':self.effects[h]['oid'],'target':self.effects[h]['target'],
                         'kind':self.effects[h]['kind'],'location':self.effects[h]['where'],'committing_branches':len(self.effects[h]['branches']),
                         'dependent_residual':any(b['has_residuals'] for b in self.effects[h]['branches'].values())}
                    for h in sorted({f['handle'] for f in self.facts.values() if f['handle'] in self.effects and 'kind' in self.effects[f['handle']]})],
                'facts':[{'id':fid,'object_or_effect':f['handle'],'meaning':f['meaning'],'role':f['role'],
                          'subject':f['subject'],'scope':f['scope'],'grounded':self.logic.valid(fid)}
                         for fid,f in sorted(self.facts.items())],
                'rule_visits':self.logic.visits,'budget_cut':self.logic.cut,
                'unfinished_operations':sorted(self.incomplete)}

    def related_ops(self, h):
        if h in self.effects:return {self.effects[h]['oid']}
        return set(self.used.get(h,()))

    def focused_consent(self,row):
        """A displayed quantity answer joins the same support as a seed on that debit."""
        origin=getattr(self,'input_origin',None);submission=getattr(self,'submission',None)
        if origin not in ('fixture','verified_service') or not submission or row['meaning'] not in CONSENT:return
        if row['scope'].get('phase') or row['scope'].get('assumptions'):return
        applicable={key(route) for route in row['quantity_scope']};facts=set()
        for e in self.by_operation.get(row['operation'],()):
            if not self.remaining():self.incomplete.add(row['operation']);break
            known={key(route) for route in self.quantity_scopes(e)}
            if not known or not known<=applicable:continue
            fid=self.fact(e,row['meaning'])
            sid='support_'+digest([origin,submission,fid])[:20]
            self.register(fid,sid,origin,'policies');facts.add(fid)
        if facts:
            row['fact_ids']=sorted(facts)
            delta=self.logic.settle()
            self.epoch+=bool(delta)

    def financial_consent(self,oid,route):
        found=set()
        for e in self.by_operation.get(oid,()):
            if self.effects[e].get('path')!=route['path'] or key(self.effects[e]['cell'])!=key(route['ledger']):continue
            for f in self.for_effect(e):
                if self.facts[f]['meaning'] in CONSENT and any(key(s)==key(route) for s in self.quantity_scopes(e)):
                    found.add(f)
        if not found:return None
        modes={self.facts[f]['meaning'] for f in found}
        return {'id':'consent_'+digest(sorted(found))[:20],'meaning':next(iter(modes)) if len(modes)==1 else 'unknown',
                'target':self.f.operations[oid]['target'],'operation':oid,'family':key(route['ledger']),
                'quantity_scope':[route],'scope':{},'source':'scoped_supports','fact_ids':sorted(found)}

    def consumers_for(self,h):
        """Instantiate only operations with a matching source effect, then let compile_property select categories."""
        f=self.f
        effects={h} if h in self.effects else set(self.by_decl.get(h,()))|{t[0] for t in self.routes.get(h,())}
        result=defaultdict(set)
        for e in effects:
            if not self.remaining():self.incomplete.add(self.effects[e]['oid']);break
            d=self.effects[e];oid=d['oid'];facts=self.for_effect(e)
            for fact in facts:
                seed=self.facts[fact];meaning=seed['meaning']
                if f.options.scope=='AC':
                    if meaning in AUTH|{'management_role','eligibility_state','authorization_quantity','other_source_policy','unknown'}:result[(oid,'AC')].add(e)
                    continue
                if meaning in CONSENT:
                    # Intervening controls are structural candidates; the financial consumer still tests the actual effect.
                    for x in f.summaries.dependencies.amounts_for(oid):
                        if x['path']!=d['path']:continue
                        for delta in x['deltas']:
                            if key(delta['cell'])!=key(d['cell']):continue
                            for gate in x['allowance_gates']:
                                for woid in self.writers_for_amount(oid,gate['quantity_expression']):
                                    result[(woid,None)].add(e)
                    continue
                if meaning in RESOURCE|{'price','fee_rule','amount_role','transfer_condition','authorization_quantity','management_role','eligibility_state','unknown','other_source_meaning'}:
                    if meaning=='transfer_condition':
                        for writer in self.by_decl.get(h,()):
                            result[(self.effects[writer]['oid'],None)].add(writer)
                    else:result[(oid,None)].add(e)
        return result

    def writers_for_amount(self,oid,expr):
        dep=self.f.summaries.dependencies
        term=dep.expressions.get(expr,{})
        target=self.f.operations[oid]['target']
        for t in walk(term):
            if t.get('kind')!='storage':continue
            for e in self.by_decl.get(self.obj(target,field_node(t)),()):
                if not self.remaining():return
                wid=self.effects[e]['oid']
                if wid!=oid:yield wid

    def inspect_untyped_amount(self,locator,manifest):
        """Only carry the located value use, never the rejected model meaning."""
        if self.f.options.scope!='FCR':return
        handle=self.bind(locator,manifest,'obj')
        if not handle:return
        by_entry=defaultdict(set)
        for eid,kind,_,exact in self.routes.get(handle,()):
            if not self.remaining():return
            if kind!='value' or not exact:continue
            d=self.effects[eid]
            if 'write' not in d or not d['clean']:continue
            oid=d['oid']
            dependencies=self.f.summaries.dependencies.forward(oid)['uses']
            if any('value' in kinds and self.f.summaries.positions(use) for use,kinds in dependencies.items()):
                by_entry[oid].add(eid)
        for oid,effects in by_entry.items():
            if any(self.inv.root(q)==oid and effects<=self.route_scopes(q) and
                   set((q.get('property') or {}).get('possible_categories',()))=={(q.get('property') or {}).get('category')}
                   for q in self.inv.issues.values()):
                continue
            qid='scope_'+digest([self.f.identity,oid,None,sorted(effects)])[:20]
            if qid in self.inv.issues:continue
            question=self.create_consumer(oid,None,effects)
            if question:question['source_only_amount_read']=True

    def seed_consumers(self,changed):
        relevant=defaultdict(set)
        for h in changed:
            for dest,es in self.consumers_for(h).items():relevant[dest].update(es)
        for (oid,category),es in sorted(relevant.items(),key=lambda r:str(r[0])):
            question=self.create_consumer(oid,category,es)
            if question:question.pop('source_only_amount_read',None)

    def create_consumer(self,oid,cat,effects):
        inv=self.inv
        qid='scope_'+digest([self.f.identity,oid,cat,sorted(effects)])[:20]
        if qid in inv.issues:return inv.issues[qid]
        item={'id':qid,'anchors':[inv.catalog.name(oid)],'assessment':'investigate','category':cat,
              'claim':'Review the applicable source effect and bound meaning.',
              '_scope_effects':sorted(effects),'_host_source_question':True,'_semantic_consumer':True}
        inv.accept({'issues':[item],'answers':[],'reviewed':[],'diagnostics':[],'usable_analysis':False},host_target=self.f.operations[oid]['target'])
        consumer=inv.issues.get(qid)
        if consumer:
            if not hasattr(self,'effect_consumers'):self.effect_consumers=defaultdict(set)
            for e in effects:self.effect_consumers[e].add(qid)
        return consumer

    def wire_name(self,h,manifest):
        if not self.visible(h,manifest):return None
        entry=self.effects.get(h) or self.objects[h]
        if h in self.effects:
            if 'cell' in entry:
                name=self.f.lookup(entry['oid']).nodes[field_node(entry['cell'])]['name']
                candidate=self.inv.catalog.name(entry['oid'])+'#'+name
            else:candidate=self.inv.catalog.name(entry['oid'])+'#'+entry['kind']
        elif entry.get('oid'):
            candidate=self.inv.catalog.name(entry['oid'])+'#'+entry['name']
        else:candidate=entry['target'].rsplit(':',1)[-1]+'.'+entry['name']
        if self.bind(candidate,manifest)==h:return candidate
        direct=next((r for r,k in manifest.get('typed_index',{}).items() if k==h),None)
        if direct:return direct
        loc=entry['where']
        span=f"{loc['file']}@{loc['start']}+{loc['length']}"
        return span if self.bind(span,manifest)==h else None

    def labels_for(self,oid,manifest):
        result={}
        for sid,s in self.supports.items():
            if not s['active'] or s['origin'] not in ('fixture','verified_service'):continue
            fact=self.facts[s['fact']];h=fact['handle']
            if oid not in self.related_ops(h) and not any(self.effects[e]['oid']==oid for e in self.by_decl.get(h,())):continue
            name=self.wire_name(h,manifest)
            if not name:continue
            tag='sem:'+sid.split('_')[-1][:12]
            qualifiers={}
            for k in ('scope','subject'):
                qualifier=fact.get(k)
                if qualifier:qualifiers[k]=self.wire_name(qualifier,manifest)
            if any(v is None for v in qualifiers.values()):continue
            result[tag]={'source':name,'support':sid,'version':s['version'],'fact':s['fact'],
                         'field':s['field'],'meaning':fact['meaning'],**qualifiers}
            if fact['role']:result[tag]['role']=fact['role']
            if fact.get('payment_policy'):result[tag]['payment_policy']=fact['payment_policy']
        return result

    def describe(self,oid,cat,reason,locations,decision):
        from .source_opinion import DETAIL,EFFECT
        matching={loc_key(loc) for loc in locations}
        es=[e for e in self.by_operation.get(oid,()) if loc_key(self.effects[e]['where']) in matching]
        ids=set()
        for e in es:ids.update(self.for_effect(e))
        att=self.inv.issues.get(decision,{}).get('property') or {}
        for c in att.get('consent_rows',[]):
            for fact in c.get('fact_ids',[]):
                ids.add(fact)
                effect=self.facts[fact]['handle']
                if effect in self.effects and effect not in es:es.append(effect)
        if self.inv.issues.get(decision,{}).get('current',{}).get('_semantic_consumer'):
            for e in self.inv.issues[decision]['current'].get('_scope_effects',()):ids.update(self.for_effect(e))
        origins=set();rules=set();types=set()
        for fid in ids:
            roots,applied=self.logic.basis(fid);origins.update(roots);rules.update(applied)
            types.add(self.facts[fid]['meaning'])
        statement=next(iter(sorted(matching,key=str)),None)
        position=' at source offset '+str(statement[1]) if statement and isinstance(statement[1],int) else ''
        kind=EFFECT.get(cat,'the scoped program effect')
        basis=DETAIL.get(reason,DETAIL['scope_missing'])
        if cat=='AC' and reason in ('source_role_reassignment','applicable_role_guard','guarded_state_change','guarded_source_effect','unguarded_governed_effect') and 'current_authority_required' in types:rules.add('P09')
        interprets=sorted({c['meaning'] for c in att.get('consent_rows',[])})
        if interprets:types.update(interprets)
        lead='The assessment concerns '+kind+position
        if types:lead+=' under '+', '.join(sorted(types))
        wording=lead+'. '+basis
        return {'explanation':wording,'facts':sorted(ids),'rules':sorted(rules),'supports':sorted(origins),'effects':sorted(es),
                'meanings':sorted(types)}

    def source_offices(self,oid):
        from .source_opinion import office_use, replacement_status
        from .policy_binding import conjuncts
        from .initial_state import initial_for_lookup
        lookup=self.f.lookup(oid)
        state=initial_for_lookup(lookup)
        found={}
        for e in sorted(self.by_operation.get(oid,())):
            if not self.remaining():self.incomplete.add(oid);break
            d=self.effects[e]
            if 'write' not in d:continue
            cell=d['cell'];w=d['write'];rid=cell['root']
            from .roles import _is_table
            table=_is_table(lookup.nodes.get(rid,{}))
            grant=w['value']
            if not d['clean']:continue
            if table:
                if len(keys(cell))!=1 or grant.get('kind')!='literal' or grant.get('value') is not True:continue
            elif keys(cell) or value_type(cell,lookup) not in ('address','address payable') or grant.get('kind') not in ('parameter','actual_sender'):continue
            established=(state or {}).get('declarations',{}).get(rid,{})
            use=office_use(self.inv,oid,cell)
            if not use:continue
            startup=bool(established.get('constructor_writes') or established.get('explicit_initializer'))
            # A separate, actually guarded replacement of the same office is
            # independent incumbent-policy evidence even without a constructor.
            from .source_opinion import office_guard,feasible_source_guards
            protected_peer=False
            for peer in self.by_decl.get(self.obj(d['target'],rid),()):
                pd=self.effects[peer]
                if not self.remaining():break
                if pd['oid']==oid or 'write' not in pd or not pd['clean']:continue
                pr=self.f.paths[pd['path']]['raw']
                if not feasible_source_guards(pr['guards']):continue
                if any(office_guard(g,cell) for g in pr['guards']):
                    protected_peer=True;break
                nominee=pd['write']['value']
                if nominee.get('kind')!='storage' or keys(nominee) or nominee['root']==rid:continue
                if not any(office_guard(g,nominee) for g in pr['guards']):continue
                # An accepted nominee may replace the incumbent, but only after an
                # independent incumbent-authorized nomination. Account for every
                # real positive writer to that applied slot; a public nomination
                # route would invalidate this source policy inference.
                nominations=[a for a in self.f.writes.values() if self.f.operations[a['operation']]['target']==d['target']
                    and key(a['raw']['path'])==key(nominee) and not (a['raw']['value'].get('kind')=='literal' and a['raw']['value'].get('value')==0)]
                if nominations and all(a['raw']['value'].get('kind') in ('parameter','actual_sender') and
                    any(office_guard(g,cell) for g in self.f.paths[a['path']]['raw']['guards']) for a in nominations):
                    protected_peer=True;break
            applied_policy=any(self.facts[f]['meaning']=='current_authority_required' for f in self.for_effect(e))
            # A repeatable installation of the caller into the very office that alone
            # governs another committing use supplies lifecycle evidence in its own right.
            # A protected switch can also define a narrower, conditional exemption.
            from .source_opinion import exception_authority
            branch=self.f.paths[d['path']]['raw']
            repeatable_self=(not table and grant.get('kind')=='actual_sender' and not branch['guards']
                             and any(office_guard(g,cell) for r in self.f.summaries.rows(use)
                                     if r['ordered_writes'] and not r['residuals'] for g in r['guards']))
            governors=set().union(*(exception_authority(self.inv,use,cell,g)
                                    for r in self.f.summaries.rows(use) for g in r['guards']))
            if not (startup or protected_peer or applied_policy or repeatable_self or governors):continue
            row=self.f.paths[d['path']]['raw']
            status=replacement_status(self.inv,d)
            if status=='open':continue
            subject=self.obj(d['target'],rid)
            fid=self.fact(e,'current_authority_required',subject)
            sid='source_'+digest([self.f.identity,e,use,'incumbent_role_use'])[:20]
            self.register(fid,sid,'source_policy_deduction','policies')
            found[e]=(status,fid)
            self.__dict__.setdefault('office_uses',{})[e]=use
        self.logic.settle()
        return found

    def scope_offices(self):
        if self.f.options.scope!='AC':return
        inv=self.inv
        self.index()
        for oid in sorted(self.by_operation):
            if not self.remaining():self.incomplete.add(oid);continue
            offices=self.source_offices(oid)
            if not offices:continue
            for q in list(inv.issues.values()):
                if inv.root(q)!=oid:continue
                locs=q['current'].get('_scope_effects',[])
                if locs:
                    q['office_effects']={e:v for e,v in offices.items() if e in locs}
                    continue
                from .source_opinion import statement_focus
                focus=statement_focus(inv,q,self.f.summaries.rows(oid))
                if focus:
                    matches=[e for e in self.by_operation[oid] if loc_key(self.effects[e]['where'])==loc_key(focus[1]['source'])]
                    q['effect_scope']=matches
                    q['office_effects']={e:v for e,v in offices.items() if e in matches}
                else:q['office_effects']=dict(offices)
            for e in offices:
                if not any(e in q.get('office_effects',{}) for q in inv.issues.values() if inv.root(q)==oid):
                    q=self.create_consumer(oid,'AC',{e})
                    if q:q['office_effects']={e:offices[e]}
            for q in inv.issues.values():
                if inv.root(q)==oid:q.pop('_source_opinion',None)

    def office_opinion(self,q,rows):
        from .source_opinion import opinion,blocked_positive
        lookup=self.f.lookup(self.inv.root(q))
        explicit=set(q['current'].get('_scope_effects',()))
        candidates={e:v for e,v in q.get('office_effects',{}).items() if not explicit or e in explicit}
        es=explicit or q.get('effect_scope') or ()
        for e in es:
            d=self.effects[e]
            if 'write' not in d:continue
            for fid in self.for_effect(e):
                f=self.facts[fid]
                if f['meaning']!='current_authority_required':continue
                subject=f.get('subject')
                if subject and self.objects.get(subject,{}).get('decl')!=d['cell']['root']:continue
                if self.f.operations[d['oid']]['target']!=d['target']:continue
                from .source_opinion import office_use,replacement_status
                from .policy_binding import conjuncts
                if not d['clean'] or not office_use(self.inv,d['oid'],d['cell']):continue
                path=self.f.paths[d['path']]['raw'];guards=[g for t in path['guards'] for g in conjuncts(t)]
                status=replacement_status(self.inv,d)
                if status!='open':candidates[e]=(status,fid)
        if not candidates:return None
        for e,(status,fid) in candidates.items():
            d=self.effects[e]
            if status=='risk' and not blocked_positive(self.inv,q,d['path'],'AC'):
                result=opinion('risk','source_role_reassignment',[d['where']])
                use=getattr(self,'office_uses',{}).get(e)
                if use:result['protected_use']=self.f.operations[use]['source']
                return result
        covered={d['path'] for e,(status,_) in candidates.items() if status=='normal' for d in [self.effects[e]]}
        if covered and {r['path'] for r in rows}<=covered:
            return opinion('normal','applicable_role_guard',[self.effects[e]['where'] for e in candidates])
        return None


    def disputed(self,q):
        oid=self.inv.root(q)
        if not oid:return False
        groups=defaultdict(set)
        for e in self.by_operation.get(oid,()):
            for fid in self.for_effect(e):
                m=self.facts[fid]['meaning']
                if m in RESOURCE:groups[e,'unit'].add(m)
                if m in CONSENT:groups[e,'consent'].add(m)
                if m=='unknown':return True
        return any(len(ms)>1 for ms in groups.values())

    def route_scopes(self,q):
        oid=self.inv.root(q)
        item=q['current']
        explicit=item.get('_scope_effects',()) or q.get('effect_scope',())
        if explicit:return set(explicit)
        from .source_opinion import statement_focus
        if not oid:return set()
        focus=statement_focus(self.inv,q,self.f.summaries.rows(oid))
        if focus:return {e for e in self.by_operation[oid] if loc_key(self.effects[e]['where'])==loc_key(focus[1]['source'])}
        return set(self.by_operation.get(oid,()))

    def authority_cell(self,e,subject):
        d=self.effects[e];lk=self.f.lookup(d['oid'])
        if subject:
            obj=self.objects.get(subject)
            if not obj or obj['target']!=d['target'] or obj['oid'] is not None:return None
            cell={'kind':'storage','root':obj['decl'],'segments':[]}
        else:
            cell=d.get('cell')
        if cell and not cell.get('segments') and value_type(cell,lk) in ('address','address payable'):return cell
        return None

    def authority_binding(self,e,subject):
        """Locate a principal in the actual effect context before judging guard strength."""
        from .source_opinion import identity_guard
        d=self.effects[e]
        cell=self.authority_cell(e,subject)
        if not cell:return None
        if 'write' in d:
            row=self.f.summaries.paths[d['path']]
            changed=any(key(w['path'])==key(cell) for w in row['ordered_writes'][:d['version']])
            # Equality within a disjunction identifies a role operand, not an
            # authorization proof. The backend retains the full committing guard.
            guarded_subject=any(identity_guard(term,{cell['root']}) for term in walk(row['guards']))
            if not changed and (cell==d['cell'] or subject and guarded_subject):
                return cell
        # The existing independent peer-policy and callpoint checks can also
        # establish a role. Being an address or receiving funds cannot do so.
        authority,_=self.authority_effect(e,subject)
        if authority in ('guarded_state_change','unguarded_governed_effect','guarded_source_effect'):
            return cell
        return None

    def authority_effect(self,e,subject):
        """Assess only the located action and the stated principal. Never assume a
        declared address is the policy for every write to a different position."""
        from .policy_binding import conjuncts
        from .source_opinion import identity_guard
        d=self.effects[e];role=self.authority_cell(e,subject)
        if 'cell' not in d:
            if d['kind']=='dangerous_external_call':return 'external_dependency',role
            if not role:return 'policy_scope_unsubstantiated',None
            # Check the guard at the actual effect, before returning to the caller.
            for pid in d['branches']:
                if not self.remaining():return 'policy_effect_unresolved',role
                branch=self.f.summaries.paths[pid]
                occurrences=[term for term in branch['effects'] if term.get('kind')==d['kind'] and loc_key(term['source'])==loc_key(d['where'])]
                if branch['residuals'] or not occurrences:return 'policy_effect_unresolved',role
                for term in occurrences:
                    guards=[g for x in term.get('callpoint_guards',()) for g in conjuncts(x)]
                    if any(key(w['path'])==key(role) for w in term.get('callpoint_writes',())) or not any(identity_guard(g,{role['root']}) for g in guards):
                        return 'policy_scope_unsubstantiated',role
            return 'guarded_source_effect',role
        if role==d['cell']:return 'office',role
        if not role:return 'policy_scope_unsubstantiated',None
        row=self.f.summaries.paths[d['path']]
        def guarded(r):
            # A guard on a prior version cannot authenticate a newly replaced authority.
            return any(identity_guard(g,{role['root']}) for term in r['guards'] for g in conjuncts(term))
        if not d['clean'] or row['effects'] or any(key(w['path'])==key(role) for w in row['ordered_writes'][:d['version']]):
            return 'policy_effect_unresolved',role
        if guarded(row):return 'guarded_state_change',role
        if row['guards']:return 'policy_effect_unresolved',role
        obj=self.obj(d['target'],field_node(d['cell']))
        for other in self.by_decl[obj]:
            if not self.remaining():return 'policy_effect_unresolved',role
            peer=self.effects[other]
            if peer['oid']==d['oid'] or not peer['clean'] or key(peer['cell'])!=key(d['cell']):continue
            # Cross-entry consent for keyed state requires additional holder/key evidence.
            if d['cell'].get('segments') or value_type(d['cell'],self.f.lookup(d['oid']))!='bool':continue
            now,other_value=d['write']['value'],peer['write']['value']
            if not all(x.get('kind')=='literal' and type(x.get('value')) is bool for x in (now,other_value)) or now['value']==other_value['value']:continue
            comp=self.f.summaries.paths[peer['path']]
            if comp['effects'] or any(key(w['path'])==key(role) for w in comp['ordered_writes'][:peer['version']]) or not guarded(comp):continue
            # A known public writer of the same applied setting and same outcome
            # is a normal alternative to the claimed control over that outcome.
            for writer in self.by_decl[obj]:
                if not self.remaining():return 'policy_effect_unresolved',role
                other=self.effects[writer]
                if other['oid']==d['oid'] or key(other['cell'])!=key(d['cell']) or key(other['write']['value'])!=key(now):continue
                other_row=self.f.summaries.paths[other['path']]
                if other['clean'] and not other_row['effects'] and not other_row['guards']:return 'policy_scope_unsubstantiated',role
            return 'unguarded_governed_effect',role
        return 'policy_scope_unsubstantiated',role

    def issuance_control(self,d,row,guards):
        """Read the selected final credit, its funding and who controls the quantity."""
        from .ledger import unit_origin
        from .prestate import state_facts
        from .source_opinion import paid_credit,quantity_forced_zero,sourced_quantity
        oid=d['oid'];lookup=self.f.lookup(oid);w=d['write'];cell=d['cell']
        who=holder(cell,lookup);sign,qty=local_delta(w)
        if sign!='+' or not qty or not who or who.get('kind') not in ('parameter','actual_sender'):
            return None
        if not unit_origin(self.inv.backend,oid,cell):return None
        # Another write in this storage family could replace or fund the credit,
        # including via a differently spelled but aliasing key.
        if any(v['path']['root']==cell['root'] for i,v in enumerate(row['ordered_writes']) if i!=d['version']):
            return None
        if row['effects']:return None
        if paid_credit(self.inv,oid,row):return 'ordinary_paid_credit'
        if quantity_forced_zero(guards,qty,lookup):return 'zero_quantity'
        # Any independently consumed asset/claim needs its own normal explanation.
        # Scalar supply/accounting increments do not finance the selected credit.
        for i,peer in enumerate(row['ordered_writes']):
            if i==d['version']:continue
            direction,_=local_delta(peer)
            if keys(peer['path']) or direction!='+':return None
        fixed=state_facts(lookup)
        def forced_zero(term):
            kind=term.get('kind')
            if kind=='literal':return term.get('value')==0
            if kind=='storage' and not keys(term):
                decl=fixed.get(term['root'],{})
                return decl.get('encoded') and decl.get('value')==0
            args=term.get('args',())
            if args and term.get('op')=='*':return any(forced_zero(v) for v in args)
            if args and term.get('op')=='+':return all(forced_zero(v) for v in args)
            return False
        if forced_zero(qty):return 'zero_quantity'
        if not sourced_quantity(qty,lookup):return None
        inputs={key(t) for t in walk(qty) if t.get('kind')=='parameter'}
        if not inputs:return None
        # A caller-supplied argument constrained to an accrued or fixed amount
        # is not a free choice. Strict positive lower bounds retain discretion.
        for guard in guards:
            if not any(key(t) in inputs for t in walk(guard)):continue
            args=guard.get('args',())
            if len(args)==2:
                left,right=args
                if guard.get('op') in ('<','<='):left,right=right,left
                if guard.get('op') in ('<','<=','>','>=','!=') and key(left) in inputs and right.get('kind')=='literal' and right.get('value')==0:
                    continue
            return None
        return 'discretionary_credit'

    def contextual_authority(self,e,q,subject=None):
        """Apply a located normative responsibility to the actor at the actual effect."""
        from .source_opinion import blocked_positive,feasible_source_guards,role_ids,identity_guard
        from .policy_binding import conjuncts
        d=self.effects[e];oid=d['oid']
        if self.effect_focus(e) not in ('termination','credit','funds'):return None
        role=self.authority_cell(e,subject) if subject else None
        if subject and role is None:return None
        normal={}
        if d.get('kind') in ('native_selfdestruct','native_transfer'):
            branches=d['branches']
        elif 'write' in d:
            branches=[d['path']]
        else:return None
        for pid in branches:
            row=self.f.summaries.paths[pid]
            if not row['committing'] or row['residuals'] or blocked_positive(self.inv,q,pid,'AC'):continue
            guards=[g for term in row['guards'] for g in conjuncts(term)]
            at_effect=guards
            if 'write' in d:
                before=row['ordered_writes'][:d['version']]
            else:
                occurrences=[t for t in row['effects'] if t['kind']==d['kind'] and loc_key(t['source'])==loc_key(d['where'])]
                if not occurrences or any('callpoint_guards' not in t for t in occurrences):continue
                points=[[g for term in t['callpoint_guards'] for g in conjuncts(term)] for t in occurrences]
                if any(key(point)!=key(points[0]) for point in points[1:]):continue
                at_effect=points[0]
                before=[w for t in occurrences for w in t.get('callpoint_writes',())]
            if role:
                if any(w['path']['root']==role['root'] for w in before):continue
                roles={role['root']}
            else:
                roles=role_ids(self.inv,oid,row)
            if any(identity_guard(g,roles) for g in at_effect):
                normal[pid]='guarded_source_effect'
                continue
            if 'write' in d:
                reading=self.issuance_control(d,row,guards)
                if reading in ('ordinary_paid_credit','zero_quantity'):
                    normal[pid]=reading
                    continue
                if reading!='discretionary_credit':continue
            # A guard on a different principal or a mixed payment branch needs
            # its own comparison. Neither establishes this role's authorization.
            if 'write' not in d and {key(g) for g in guards}!={key(g) for g in at_effect}:continue
            if any(t.get('kind') not in ('op','literal','parameter','transaction_origin','storage')
                   for t in walk(guards)):continue
            if any(t.get('kind')=='storage' for t in walk(guards)) and not all(
                    g.get('op')=='==' and any(t.get('kind') in ('transaction_origin','tx_origin') for t in g.get('args',()))
                    for g in guards):continue
            if not feasible_source_guards(guards):continue
            if d.get('kind')=='native_transfer':continue
            if any(t.get('kind')=='transaction_origin' for t in walk(guards)):
                return 'origin_only_decider'
            return 'unrestricted_termination_decision' if 'branches' in d else 'unrestricted_issuance_decision'
        if set(normal)==set(branches) and len(set(normal.values()))==1:return next(iter(normal.values()))
        return None

    def local_opinion(self, q):
        from .policy_binding import conjuncts, effect_duty
        from .relations import opinion_principals
        from .roles import _roots
        from .source_opinion import opinion, blocked_positive, feasible_source_guards, covered_delegation, role_ids
        from pr_next_joint.frontend.path_ir import conditions_possible, op

        item = q['current']
        scopes = item.get('_scope_effects', ())
        if not item.get('_opinion_message') or not scopes or item.get('assessment') not in ('risk','normal'):
            return None
        expected = (q.get('property') or {}).get('expected_authorization') or {}
        compiled = expected.get('compiled_authorization') or {}
        if (expected.get('unresolved_relations') or compiled.get('necessary_only') or compiled.get('competing_interpretations')
                or compiled.get('kind') == 'source_role_payment_policy'):
            return None
        if expected.get('source') == 'focused_model_answer':
            duty = effect_duty(expected.get('basis',''))
        else:
            duty = effect_duty(item.get('policy_basis') or item['claim'])
            if not duty and item.get('policy_basis'):
                duty = effect_duty(item['claim'])
        if not duty:
            # Descriptive text may locate a useful effect. Its source facts and
            # independently established policies still have their own consumers.
            return None
        oid = self.inv.root(q)
        actor = {'kind':'actual_sender'}
        statuses, locations = [], []
        for eid in scopes:
            effect = self.effects[eid]
            if effect['oid'] != oid:
                continue
            principals = opinion_principals(self.inv, item, effect, duty)
            for pid in ([effect['path']] if 'path' in effect else effect['branches']):
                row = self.f.summaries.paths[pid]
                conditions = [g for guard in row['guards'] for g in conjuncts(guard)]
                if not row['committing'] or not feasible_source_guards(conditions):
                    continue
                locations.append(effect['where'])
                if self.f.call_summaries.effect_dependencies(row, effect, initiation=True):
                    statuses.append('open')
                    continue
                if 'write' in effect and any(key(w['path']) == key(effect['cell'])
                        for w in row['ordered_writes'][effect['version']+1:]):
                    statuses.append('open')
                    continue
                if duty['qualified'] or any(kind == 'conflict' for kind, _ in principals):
                    statuses.append('open')
                    continue
                proofs = []
                for kind, term in principals:
                    if term is None or kind == 'conflict':
                        # An abstract duty can govern a publicly selectable action.
                        # It cannot by itself identify a different source guard.
                        proofs.append(False if kind == 'abstract' and not role_ids(self.inv,oid,row) else None)
                        continue
                    if (kind == 'holder' and 'write' in effect and local_delta(effect['write'])[0] == '-'
                            and covered_delegation(self.inv,oid,[row])):
                        proofs.append(True)
                    elif kind == 'office' and value_type(term,self.f.lookup(oid)) not in ('address','address payable'):
                        recognized = role_ids(self.inv,oid,row) & {term['root']}
                        proofs.append(any(_roots(g,recognized) for g in conditions) if recognized else None)
                    else:
                        try:
                            proofs.append(key(actor)==key(term) or not conditions_possible(conditions,op('==',actor,term)))
                        except (ValueError,RecursionError):
                            proofs.append(None)
                sufficient = any(proof is True for proof in proofs) if duty['alternative'] else all(proof is True for proof in proofs)
                missing = all(proof is False for proof in proofs) if duty['alternative'] else any(proof is False for proof in proofs)
                if (duty['alternative'] and not sufficient and all(term is not None and (
                        kind == 'holder' or kind == 'office' and value_type(term,self.f.lookup(oid)) in ('address','address payable'))
                        for kind,term in principals)):
                    # Each allowed identity can occupy a different disjunct of the guard.
                    allowed = op('or', *[op('==',actor,term) for _,term in principals])
                    try:
                        sufficient = not conditions_possible(conditions,allowed)
                    except (ValueError,RecursionError):
                        missing = False
                if (not sufficient and compiled.get('binding_effect') == eid and compiled.get('source_bound_alternatives')
                        and compiled.get('predicate') and not compiled.get('necessary_only')):
                    try:
                        sufficient = not conditions_possible(conditions, compiled['predicate'])
                    except (ValueError,RecursionError):
                        missing = False
                if sufficient:
                    statuses.append('normal')
                elif not missing or blocked_positive(self.inv,q,pid,'AC'):
                    statuses.append('open')
                elif 'write' in effect and self.issuance_control(effect,row,conditions) in ('ordinary_paid_credit','zero_quantity'):
                    # Let the independently recorded source alternative speak for itself.
                    return None
                else:
                    statuses.append('risk' if item['assessment']=='risk' else 'open')
        if not statuses:
            return None
        status = 'risk' if 'risk' in statuses else 'normal' if all(v=='normal' for v in statuses) else 'open'
        reason = {'risk':'scoped_semantic_conflict','normal':'scoped_semantic_normal','open':'scope_missing'}[status]
        result = opinion(status,reason,{loc_key(loc):loc for loc in locations}.values())
        result['semantic_local'] = True
        result['same_scope_authorized'] = status == 'normal'
        return result

    def effect_policy_opinion(self,q):
        if self.f.options.scope!='AC':return None
        from .source_opinion import opinion,blocked_positive
        out=[];located=[];policy_sources=set()
        if not q['current'].get('_semantic_consumer'):
            return self.local_opinion(q)
        for e in self.route_scopes(q):
            d=self.effects[e]
            if d['oid']!=self.inv.root(q):continue
            for fid in self.for_effect(e):
                fact=self.facts[fid]
                if fact['meaning']=='current_authority_required':
                    status,role=self.authority_effect(e,fact['subject'])
                    compiled=((q.get('property') or {}).get('expected_authorization') or {}).get('compiled_authorization') or {}
                    if not compiled and status in ('policy_scope_unsubstantiated','policy_effect_unresolved'):
                        status=self.contextual_authority(e,q,fact['subject']) or status
                    if status=='office' or compiled.get('kind')=='source_role_payment_policy' and compiled.get('binding_effect')==e:
                        continue
                    if status=='unguarded_governed_effect' and blocked_positive(self.inv,q,d['path'],'AC'):status='policy_effect_unresolved'
                    out.append(status);located.append(d['where']);policy_sources.add(fact['subject'])
                elif 'cell' not in d and fact['meaning'] in ('unknown','other_source_policy'):
                    out.append('external_dependency' if d['kind']=='dangerous_external_call' else 'policy_missing')
                    located.append(d['where'])
        if not out:return None
        if len(policy_sources)>1:return opinion('open','policy_scope_unsubstantiated',located)
        for supported in ('unguarded_governed_effect','unrestricted_termination_decision','unrestricted_issuance_decision','origin_only_decider'):
            if supported in out:return opinion('risk',supported,located)
        protected={'guarded_state_change','guarded_source_effect','ordinary_paid_credit','zero_quantity'}
        if set(out)<=protected:return opinion('normal',out[0],located)
        reason=next(v for v in out if v not in protected)
        return opinion('open',reason,located)

    def policy(self,q):
        if not self.inv.root(q):return None
        fs=[(self.facts[f],f,e) for e in sorted(self.route_scopes(q)) for f in self.for_effect(e) if self.facts[f]['meaning'] in AUTH]
        if not fs:return None
        if len({(r['meaning'],r['subject'],r.get('payment_policy'),e) for r,f,e in fs})!=1:return None
        r,fid,e=fs[0];d=self.effects[e];lookup=self.f.lookup(d['oid'])
        if r['meaning']=='holder_authorization_applies':
            if 'cell' not in d:return None
            grant=key_relation(d['cell'],lookup);ordered=keys(d['cell'])
            if not grant or grant.get('kind')!='authorization_quantity' or len(ordered)!=2:return None
            subject=ordered[grant['holder_key']]
            if r['subject'] and self.objects[r['subject']]['decl']!=subject.get('id',subject.get('root')):return None
            return {'meaning':'required_authorization','polarity':'asserted','level':'H','semantic_fact':fid,
                    'explicit_policy_kind':r['meaning'],'qualified_cell':subject,'binding_effect':e,
                    'text':'The actual holder issues this grant.','source_anchors':q['current']['anchors']}
        if r['meaning']=='initialization_stage':
            if not r.get('subject'):return None
            flag={'kind':'storage','root':self.objects[r['subject']]['decl'],'segments':[]}
            if value_type(flag,lookup)!='bool':return None
            if not any(key(w['path'])==key(flag) and w['value'].get('value') is True for row in self.f.summaries.rows(d['oid']) for w in row['ordered_writes']):return None
            return {'meaning':'required_authorization','polarity':'asserted','level':'H','semantic_fact':fid,'explicit_policy_kind':r['meaning'],
                    'qualified_cell':flag,'binding_effect':e,'text':'The located one-time stage limits this effect.','source_anchors':q['current']['anchors']}
        if r['meaning']=='current_authority_required':
            sub=self.authority_binding(e,r['subject'])
            if not sub:return None
            return {'meaning':'required_authorization','polarity':'asserted','level':'H','semantic_fact':fid,
                    'explicit_policy_kind':r['meaning'],'qualified_cell':sub,'binding_effect':e,
                    'payment_policy':r.get('payment_policy'),'text':'The incumbent qualifies the recorded change.','source_anchors':q['current']['anchors']}
        return None


    def disputed_effects(self,q):
        oid=self.inv.root(q)
        if not oid:return set()
        pairs=[]
        effects=set(q['current'].get('_scope_effects',())) or self.by_operation.get(oid,set())
        for e in effects:
            groups=defaultdict(set)
            for fid in self.for_effect(e):
                meaning=self.facts[fid]['meaning']
                if meaning in RESOURCE:groups['resource'].add(meaning)
                if meaning in CONSENT:groups['consent'].add(meaning)
            if any(len(s)>1 for s in groups.values()):pairs.append(e)
        return set(pairs)

    def describe_source(self,oid,cat,reason,locations,qid):
        row=self.describe(oid,cat,reason,locations,qid)
        notes=[v for v in self.inv.__dict__.get('_scoped_dependency_states',{}).values() if v.get('operation')==oid]
        if notes:
            row['dependency_states']=notes
            # Use the existing controlled meanings channel. Public output deliberately
            # strips unapproved dictionaries; no new output schema or raw IR is needed.
            row['meanings']=list(dict.fromkeys(row.get('meanings',[])+['dependency_'+n['state'] for n in notes]))
        q=self.inv.issues[qid]
        evidence=[self.inv.evidence[e] for e in q['evidence']]
        prop=q.get('property') or {}
        modes={v['meaning'] for v in prop.get('consent_rows',[])}
        if reason=='program_support':
            usable=[v for record in evidence for v in record.get('queries',())
                    if v.get('bounded_condition_confirmed') and v.get('details',{}).get('property_validated')
                    and (v['details'].get('property_identity')==prop.get('id') or record.get('property_validation_key')==q.get('changed_validation_key') and q.get('changed_validation_key'))]
            labels={v.get('label') for v in usable}
            anchor=self.f.operations.get(oid,{}).get('function','this entry')
            if cat=='AC' and 'authorization_violation' in labels:
                expected=prop.get('expected_authorization') or {}
                row['explanation']=('At '+anchor+', the committing effect admits a requester outside the applicable source-bound qualification. '+
                    ('The policy concerns acquisition and subsequent protected use.' if expected.get('property_family')=='acquire' else
                     'The check compares the effective guard with the bound authorization requirement, including any alternative qualification.'))
                paid=(expected.get('compiled_authorization') or {}).get('source_requirement') or {}
                if paid.get('kind')=='source_role_payment_policy' and not paid.get('permits_payment'):
                    if paid.get('payment_relation')=='joint':
                        row['explanation']='At '+anchor+', the policy requires both the incumbent role and the qualifying payment. The effective guard admits a committing change without that combination.'
                    else:
                        row['explanation']='At '+anchor+', the incumbent role is necessary for this effect. The payment branch can commit the change without that role.'
            elif cat=='FCR-MINT' and labels & {'direct_effect','financial_value'}:
                row['explanation']=('At '+anchor+', the checked privilege permits positive additional rights for the controller or a beneficiary it can select. '+
                    ('The intervention can enable a new same-request outcome; baseline commitment is not established.' if any(v['details'].get('baseline_commit_not_assumed') for v in usable) else
                     'A balance increase for an independent ordinary buyer alone does not satisfy this condition.'))
            elif cat=='FCR-DESTROY' and labels & {'direct_effect','financial_value'}:
                row['explanation']='At '+anchor+', a privileged effect leaves another holder with fewer rights in the same unit after attributed transfers and applicable settlement.'
            elif cat=='FCR-TRANSFER' and labels & {'direct_effect','financial_value'}:
                row['explanation']='At '+anchor+', the scoped change moves another holder’s existing rights to a separate position without the applicable holder-issued consent.'
            elif cat in ('FCR-PAUSE','FCR-FREEZE') and 'financial_block' in labels:
                group='the designated holder' if cat=='FCR-FREEZE' else 'ordinary holders'
                row['explanation']='At '+anchor+', the checked privileged change restricts the outgoing right of '+group+' for an otherwise usable request within the recorded domain.'
        if reason=='source_check_excluded' and cat=='FCR-MINT' and prop.get('value_dependence',{}).get('value_uses'):
            uses=prop['value_dependence']['value_uses']
            actual_paid_use=any(any(n.get('kind')=='transaction_value' for n in walk([r['guards'],r['ordered_writes']])) for o in uses for r in self.f.summaries.rows(o))
            if actual_paid_use:
                row['explanation']='The price or amount control reaches a paid credit. The applicable source check excludes positive additional rights for the controller or a beneficiary it selects; a separate buyer receiving its own purchase does not establish this capability.'
        if modes=={'net_request_with_fee'} and cat=='FCR-DESTROY' and reason in ('scope_missing','scoped_fee_consent','program_support'):
            row['explanation']=('The matched holder allowance uses the net request and its disclosed fee. '+
               ('The applicable check excludes an uncompensated debit under that effective grant.' if reason=='scoped_fee_consent' else
                'The authorization may be zero on the pertinent debit; the recorded net interpretation alone cannot exclude loss.' if reason=='scope_missing' else
                'The matched debit still has a source-supported loss after applicable consent.'))
        if modes=={'gross_debit_bound'} and cat in ('FCR-TRANSFER','FCR-DESTROY') and reason in ('program_support','source_certificate'):
            row['explanation']=('The holder-issued bound applies to the gross debit of this request. '+
                ('The check finds an unauthorized debit with credit to a separate position; the credit itself need not exceed the grant.'
                 if cat=='FCR-TRANSFER' else 'The check finds a positive uncompensated loss under that gross bound.'))
        if reason=='program_support' and cat in ('FCR-TRANSFER','FCR-DESTROY','FCR-MINT'):
            uses={ev.get('observe') for ev in evidence if ev.get('change')==oid and ev.get('observe')!=oid and
                  any(v.get('label')=='financial_value' and v in usable for v in ev.get('queries',()))}
            if len(uses)==1 and (use:=next(iter(uses))) in self.f.operations:
                before=self.f.operations[oid]['function'];after=self.f.operations[use]['function']
                row['explanation']=('The change at '+before+' affects the same holder request at '+after+'. '+
                        {'FCR-TRANSFER':'The checked difference is a movement of existing rights to a separate position outside applicable consent.',
                         'FCR-DESTROY':'The checked difference is an uncompensated reduction of existing rights under the applicable consent.',
                         'FCR-MINT':'The checked difference is a new positive entitlement for a controlled beneficiary.'}[cat])
        if any(v.get('kind')=='source_inspection' for v in evidence):row['origins']=['source_observation']
        else:row['origins']=[]
        row['origins']+=sorted({self.supports[s]['origin'] for s in row['supports'] if s in self.supports})
        if row['rules']:row['origins'].append('rule_derivation')
        if reason in ('program_support','source_check_excluded') and any(v.get('queries') for v in evidence):row['origins'].append('scoped_program_check')
        if modes:
            if any(c.get('source')=='focused_source_bound_semantic_answer' for c in prop.get('consent_rows',[])):row['origins'].append('source_bound_semantic_answer')
        return row

    def matching_dispute(self,q):
        """A source-typed financial interpretation stays unresolved only when its two meanings matter."""
        es=self.disputed_effects(q)
        if not es:
            why=self.unresolved(q)
            if why:return dict(status='open',reason=why,locations=[self.f.operations[self.inv.root(q)]['source']])
            if self.f.options.scope=='FCR' and q['current'].get('_semantic_consumer') and not q['current'].get('category'):
                effects=self.route_scopes(q)
                if effects and all('write' in self.effects[e] and self.effects[e]['clean'] and local_delta(self.effects[e]['write'])[0] and
                        {self.facts[f]['meaning'] for f in self.for_effect(e)}=={'nonfinancial_counter'} and
                        self.local_counter(e) for e in effects):
                    return dict(status='normal',reason='scoped_counter',locations=[self.effects[e]['where'] for e in sorted(effects)])
            return None
        return {'status':'open','reason':'conflicting_scoped_meanings','locations':[self.effects[e]['where'] for e in sorted(es)]}



    def local_counter(self,e):
        # Use the already registered dependency summary. An unfinished search cannot close a use.
        d=self.effects[e]
        summary=self.f.summaries.dependencies.forward_cache.get(d['oid'])
        if not summary or not summary['fixed_point_over_indexed_definitions'] or summary['residuals']:return False
        uses=summary['uses']
        if any(not self.f.operations[u].get('generated_getter') for u in uses):return False
        from .ledger import _unit_origin
        return not _unit_origin(self.inv.backend,d['oid'],d['cell'])

    def legacy_resource(self,oid,cell,meaning,scope):
        receipt=getattr(self,'legacy_receipt',None)
        if not receipt or not self.built or scope.get('phase') or scope.get('assumptions'):return
        target=self.f.operations[oid]['target'];obj=self.obj(target,field_node(cell))
        if obj not in self.objects:return
        source,submission=receipt
        if source not in ('verified_service','fixture') or not submission:return
        fid=self.fact(obj,meaning)
        sid='support_'+digest([source,submission,fid])[:20]
        if self.register(fid,sid,source,'annotations'):
            self.derive(fid);self.logic.settle()

    def planning_read(self,q):
        if not q['current'].get('_semantic_consumer'):return
        for e in q['current'].get('_scope_effects',()):
            if e not in self.effects:continue
            d=self.effects[e]
            for fid in self.for_effect(e):
                meaning=self.facts[fid]['meaning']
                if not self.remaining():self.incomplete.add(d['oid']);return
                if meaning in ('price','fee_rule','amount_role') and 'cell' in d:
                    obj=self.obj(d['target'],field_node(d['cell']))
                    for sink,k,rs,exact in self.routes.get(obj,()):
                        if not self.remaining():self.incomplete.add(d['oid']);return
                        use=self.effects[sink]['oid']
                        if k=='value' and use!=d['oid']:
                            q.setdefault('semantic_read_dependencies',set()).add(use)
                            self.inv.enqueue(q['id'],'inspect',{'operation':use,'enhance':False},2,'source_quantity_consumer')
                if meaning in ('authorization_quantity','eligibility_state','transfer_condition'):
                    self.inv.enqueue(q['id'],'inspect',{'operation':d['oid'],'enhance':False},1,'condition_subject_and_use')


    def withdrawn_dependency(self,e):
        d=self.effects[e]
        if any(self.facts[f]['meaning'] in RESOURCE for f in self.for_effect(e)):return False
        for support in self.supports.values():
            if support['active'] or not support.get('withdrawn'):continue
            row=self.facts[support['fact']];h=row['handle']
            if row['meaning'] not in RESOURCE:continue
            if h==e or h==self.obj(d['target'],field_node(d['cell'])) or any(dest==e and kind=='value' for dest,kind,_,_ in self.routes.get(h,())):return True
        return False

    def index_transfer(self,src,e,fid,pre,rule):
        dest=self.facts[fid]
        obj=self.obj(self.effects[e]['target'],field_node(self.effects[e]['cell']))
        if self.objects.get(src,{}).get('oid') is not None or src==obj or not self.effects[e]['clean']:return
        w=self.effects[e]['write']
        if keys(w['path']) or w['value'].get('kind')!='storage' or keys(w['value']):return
        # Only cells whose every committing writer copies this very source may export that interpretation.
        # It describes a value family, not the existence of a reachable transition or consent.
        writers=self.by_decl[obj]
        if any(not self.effects[q]['clean'] or key(self.effects[q]['write']['value'])!=key(w['value']) for q in writers):return
        if dest['meaning'] not in ('price','fee_rule','amount_role','eligibility_state','management_role'):return
        nxt=self.fact(obj,dest['meaning'],None,None,dest['role'])
        self.logic.rule(nxt,[pre],rule)
        return nxt

    def semantic_questions_for(self,q):
        oid=self.inv.root(q)
        if not oid:return []
        effects=q['current'].get('_scope_effects') or self.by_operation.get(oid,set())
        await_more=set()
        for e in effects:
            if e not in self.effects:continue
            fs=self.for_effect(e)
            for fid in fs:
                m=self.facts[fid]['meaning']
                if m in ('unknown','other_source_meaning','other_source_policy'):
                    await_more.add(e)
        await_more.update(self.disputed_effects(q))
        if not await_more:return []
        return [{'kind':'scoped_support_dispute','affected_effects':sorted(await_more),'id':'dispute_'+digest([oid,sorted(await_more)])[:12],
                 'question':'Clarify the shown meaning on this effect. Correct, narrow or withdraw its support using an applicable source reason.'}]

    def unresolved(self,q):
        if self.disputed_effects(q):return 'conflicting_scoped_meanings'
        for e in self.route_scopes(q):
            if e not in self.effects:continue
            d=self.effects[e]
            if 'cell' not in d:continue
            lookup=self.f.lookup(d['oid']);roots=self.for_effect(e)
            labels={self.facts[f]['meaning'] for f in roots}
            quantity_only='amount_role' in labels and not labels.intersection(RESOURCE) and q['current'].get('_semantic_consumer')
            if self.withdrawn_dependency(e) or quantity_only or 'unknown' in labels and not labels-{'unknown','other_source_meaning','other_source_policy'}:
                if keys(d['cell']) and holder(d['cell'],lookup) is not None:
                    from .ledger import _unit_origin
                    if _unit_origin(self.inv.backend,d['oid'],d['cell']) is None:return 'source_unit_missing'
        return None

```

## source/src/pr_next_joint/investigation/shared_effect_bridge.py

原文件SHA256 `30ead2c5051213ed45638587b755dcb6d4e64dc85e2191f5e70baba47b5d758a`

```python
"""Read-only joins over applied compiler paths. No task labels enter either join."""
from pr_next_joint.frontend.path_ir import key
from pr_next_joint.frontend.storage import keys, selector_relation
from .dependencies import may_alias
from .summary import holder, local_delta


def authority_effect_links(facts, target, cell):
    """Locate guard readers; equal declarations across frames still need a key binding."""
    deps = facts.summaries.dependencies
    for edge_id in deps.readers.get((target, cell['root']), ()):
        edge = deps.rows[edge_id]
        if edge['kind'] != 'guard' or not may_alias(cell, edge['read']):
            continue
        row = facts.summaries.paths[edge['path']]
        if row['committing'] and (row['ordered_writes'] or row['effects']):
            yield edge, row


def equity_impact_links(backend, oid, row):
    """Final arithmetic deltas in one applied branch. Keep unrelated units separate."""
    from .ledger import unit_origin, native_only_position
    lookup = backend.f.lookup(oid)
    writes = row['ordered_writes']
    moves = []
    for write in writes:
        cell = write['path']
        account = holder(cell, lookup)
        sign, quantity = local_delta(write)
        if not account or not sign or not quantity:
            continue
        if not unit_origin(backend, oid, cell) or native_only_position(backend, oid, cell):
            continue
        moves.append((sign, quantity, cell, account, write['source']))
    return moves


def independent_holder_debit(rules, effect):
    """An arbitrary third-party debit has an independent baseline in the same ledger."""
    from .initial_state import family
    from .ledger import same_unit_transfers
    from .policy_binding import conjuncts
    from .source_opinion import caller_input_conditions

    d = rules.effects[effect]
    oid = d['oid']
    row = rules.f.summaries.paths[d['path']]
    if not row['committing'] or row['effects'] or row['residuals'] or len(row['ordered_writes']) != 2:
        return None
    moves = equity_impact_links(rules.inv.backend, oid, row)
    if len(moves) != 2:
        return None
    debit = next((m for m in moves if m[0] == '-' and key(m[4]) == key(d['where'])), None)
    credit = next((m for m in moves if m[0] == '+'), None)
    if not debit or not credit or debit[3].get('kind') != 'parameter':
        return None
    if credit[3].get('kind') not in ('parameter', 'actual_sender') or key(debit[3]) == key(credit[3]):
        return None
    qty = debit[1]
    if qty.get('kind') != 'parameter' or not qty.get('type', '').startswith('uint'):
        return None
    if key(qty) != key(credit[1]) or selector_relation(debit[2], credit[2]) != 'same_shape':
        return None
    # Only a balance floor or a freely chosen positive quantity is established
    # here. Identity, payment, allowance or time controls require their own check.
    for guard in (g for term in row['guards'] for g in conjuncts(term)):
        args = list(map(key, guard.get('args', ())))
        floor = ((guard.get('op') in ('>', '>=') and args == [key(debit[2]), key(qty)])
                 or (guard.get('op') in ('<', '<=') and args == [key(qty), key(debit[2])]))
        if not floor and not caller_input_conditions([guard]):
            return None
    baselines = same_unit_transfers(rules.f, d['target'], include_checked_arithmetic=True)
    for route in baselines.get(family(debit[2]), ()):
        if route['operation'] == oid:
            continue
        for other in rules.f.summaries.paths[route['path']]['ordered_writes']:
            if key(other['source']) != key(route['source']):
                continue
            sender = holder(other['path'], rules.f.lookup(route['operation']))
            if sender and sender.get('kind') == 'actual_sender':
                return dict(family='holder_disposition', duty='separate_holder_spending_route',
                            path=d['path'], support=route['source'], use=route['operation'])
    return None


def zero_key_spendable(backend, oid, cell):
    """A caller-selected debit can spend a positive zero-key credit in this family."""
    rules = getattr(getattr(backend, 'semantics', None), 'rules', None)
    if rules is None:
        return False
    from .initial_state import family
    target = rules.f.operations[oid]['target']
    stamp = (target, family(cell), rules.epoch)
    cache = backend.__dict__.setdefault('_source_spendable_zero_key', {})
    if stamp not in cache:
        for effect in rules.by_decl.get(rules.obj(target, cell['root']), ()):
            if not rules.remaining():
                return False
            d = rules.effects[effect]
            if selector_relation(d['cell'],cell) != 'same_shape' or local_delta(d['write'])[0] != '-':
                continue
            if independent_holder_debit(rules, effect):
                cache[stamp] = True
                break
        else:
            cache[stamp] = False
    return cache[stamp]


def index_authority_consumers(rules):
    """Use guard dependencies to locate actual consumers of each authority write.

    Source co-occurrence is not a control proof. In particular an office can
    be real yet freely assignable, which affects AC and FCR differently.
    """
    from pr_next_joint.core import digest
    from .roles import effective_roots
    facts = rules.f
    qualified_readers = {}
    links = {}
    for writer, focus in rules.sensitive_effects.items():
        if focus != 'qualification':
            continue
        w = rules.effects[writer]
        if not rules.remaining():
            rules.incomplete.add(w['oid'])
            break
        if 'cell' not in w or rules.overwritten(writer):
            continue
        for edge, branch in authority_effect_links(facts, w['target'], w['cell']):
            if not rules.remaining():
                rules.incomplete.add(w['oid'])
                break
            use = edge['use']
            if use == w['oid']:
                continue
            role = w['cell']['root']
            # A balance floor and a freeze bit are real guard reads too. Only
            # an applied caller qualification links a role writer to a financial
            # use. Other guard reads stay with the ordinary control comparator.
            path_id = (w['target'], branch['path'])
            if path_id not in qualified_readers:
                allowed = facts.lookup(use).nodes.keys()
                qualified_readers[path_id] = set().union(*(
                    effective_roots(guard, allowed) for guard in branch['guards']))
            if role not in qualified_readers[path_id]:
                continue
            for impact in rules.by_operation[use]:
                output = rules.effects[impact]
                if output.get('path') != branch['path'] or 'write' not in output or rules.overwritten(impact):
                    continue
                sign, amount = local_delta(output['write'])
                if not sign or not amount or not holder(output['cell'], facts.lookup(use)):
                    continue
                # The stable ID is shared across tasks. A solver answer,
                # model interpretation, or classification is never an edge.
                uid = digest([facts.bundle['build_id'],w['target'],writer,edge['path'],
                              edge['position'],impact,edge['expression']])
                links[uid] = dict(writer=writer, reader=impact, operation=use,
                    producer=w['oid'], target=w['target'], declaration=role,
                    guard_position=edge['position'], read_path=edge['path'],
                    write_version=w['version'], consumer_version=output['version'],
                    ordered_writer_keys=digest(keys(w['cell'])), ordered_reader_keys=digest(keys(edge['read'])),
                    direction=sign, writer_location=w['where'], reader_location=output['where'],
                    status='actual_guard_read' if not keys(w['cell']) else 'source_read_key_binding_required')
    return links


def financial_refinements(rules):
    """Coalesce role readers at the applied write; ordinary routes retain their own checks."""
    from collections import defaultdict
    from .source_opinion import role_ids
    from .scope_relevance import nonfinancial
    groups = defaultdict(set)
    readers = {link['reader'] for link in rules.authority_bridges.values()}
    for effect in sorted(readers):
        if not rules.remaining():
            break
        d = rules.effects[effect]
        oid = d['oid']
        row = rules.f.summaries.paths[d['path']]
        if not role_ids(rules.inv, oid, row):
            continue
        cell = d['cell']
        if nonfinancial(rules.inv.backend, oid, cell):
            continue
        sign, quantity = local_delta(d['write'])
        account = holder(cell, rules.f.lookup(oid))
        if not account or not quantity:
            continue
        # The privileged role may govern a paid transfer of its own balance.
        # Keep the ordinary reading; this bridge adds no third-party loss there.
        if sign == '-' and account.get('kind') == 'actual_sender':
            continue
        others = [local_delta(write) for write in row['ordered_writes']
                  if selector_relation(cell, write['path']) == 'same_shape']
        if sign == '+':
            if any(direction == '-' for direction, _ in others):
                continue
            categories = ('FCR-MINT',)
        else:
            matched = any(direction == '+' and key(qty) == key(quantity) for direction, qty in others)
            categories = ('FCR-TRANSFER',) if matched else ('FCR-DESTROY', 'FCR-TRANSFER')
        location = d['where']
        for category in categories:
            groups[(oid, category, cell['root'], location['file'], location['start'],
                    location['length'])].add(effect)
    for (oid, category, *_), effects in sorted(groups.items()):
        yield oid, category, effects

```

## source/src/pr_next_joint/investigation/source_opinion.py

原文件SHA256 `eac4ddc34caddd021afffdbd4864ca8c94ba74a7b0dc261f0e7e8279ef3d3652`

```python
"""Scope-limited source opinions consumed by the ordinary property composer.

These records describe a prediction, not the feasibility of a transaction.
External output uses the vocabulary below and compiler locations only.
"""
import re
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, value_type
from .ledger import unit_origin, native_only_position
from .policy_binding import boolean_leaf, conjuncts, mentioned
from .prestate import impossible_role, state_facts
from .roles import path_qualification
from .summary import holder, local_delta
from .contracts import CATEGORIES

EFFECT = {
    "AC": "the policy governing the protected effect",
    "FCR-TRANSFER": "a transfer of another holder's existing rights",
    "FCR-MINT": "a positive new entitlement for a controlled beneficiary",
    "FCR-DESTROY": "an uncompensated loss of another holder's entitlement",
    "FCR-PAUSE": "a common restriction on ordinary outgoing transfers",
    "FCR-FREEZE": "a restriction on the designated holder's outgoing transfer",
}
DETAIL = {
    'same_request_preserved':'The actual control transition preserves the inspected positive holder request; the conclusion is limited to that source use.',
    'same_scope_loss_excluded':'The original committing frame and applicable consent exclude the claimed final holder loss in this exact scope.',
    'untrusted_holder_disposition':'The caller selects another holder and redirects a positive debit. The same ledger independently supports ordinary spending by its holder.',
    'fixed_holder_entitlement':'The source grants the caller one fixed credit and consumes their own non-resettable eligibility for that credit.',
    'holder_own_transfer':'The caller spends their own balance on the same ordinary transfer.',
    'holder_issued_transfer_scope':'This transfer consumes the holder’s same-key grant for this amount. Authority to create such grants is assessed separately.',
    'voluntary_holder_debit':'The caller reduces their own account on this committing path; this does not establish a privileged loss for another holder.',
    "unbacked_source_issuance":"The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.",
    "unqualified_active_termination":"The source governs completion of this active service separately. The current caller can end it before that condition without the governing authority.",
    "governed_completion":"The termination is restricted to the separately governed completed phase or its responsible authority.",
    "applicable_payment_qualification": "The policy permits either the incumbent role or the same entry’s threshold payment to authorize this effect. Every committing branch enforces one of those alternatives.",
    "holder_consent_basis_unresolved": "The holder-issued grant and the final debit use different quantity bases. The applicable consent convention remains unresolved for this use.",
    "source_role_reassignment": "An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification.",
    "applicable_role_guard": "The existing office must authorize the same change under the recorded guard.",
    "self_delegation": "The authority being written belongs to the caller in the source's issuer position.",
    "new_entitlement": "A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary.",
    "existing_rights_moved": "The qualified operation debits another holder and causally credits the same asset without an applicable holder grant.",
    "uncompensated_debit": "The qualified operation reduces another holder's position without a matching credit on this source branch.",
    "intra_ledger_transfer": "The same asset is moved between positions; that movement does not create additional units.",
    "same_position_restored": "The debit is returned to the same position on the applicable branch.",
    "parameter_only": "The source changes configuration without a downstream change to the relevant entitlement.",
    "no_new_controlled_credit": "The credited position is restricted to a fixed independent recipient.",
    "unassessed_role_change": "A change to authority affects a second protected use but has not yet received an applicable policy reading.",
    "unguarded_governed_effect": "A separate entry requires the stated incumbent to govern this same state. The located change has no corresponding guard under the stated policy.",
    "policy_scope_unsubstantiated": "The source identifies the effect, but does not establish the proposed principal as its applicable authority.",
    "guarded_source_effect": "A source guard at the located operation checks the stated incumbent before the effect. The authorization conclusion applies to that operation.",
    "policy_effect_unresolved": "The located effect depends on an unresolved branch, authority version or effect-specific condition.",
    "policy_missing": "The affected effect is locatable, but its intended authority cannot be distinguished from a permitted public use.",
    "conflicting_scoped_meanings": "The same source effect has incompatible applicable interpretations; resolving this meaning can change its judgment.",
    "source_unit_missing": "Whether the account amount represents a financial entitlement depends on an unresolved, source-located use.",
    "scope_missing": "The available source does not distinguish the claimed effect from the applicable normal explanation in this scope.",
    "external_dependency": "A missing implementation or return condition can determine whether this effect commits or has the claimed meaning.",
    "source_context_missing": "A relevant implementation or source region was unavailable for this judgment.",
    "no_effect_in_scope": "The inspected entry has no relevant committing effect for this category.",
    "source_task_reading": "The source opinion and the actual effect directory support a normal reading of the inspected scope.",
    "model_phase_missing": "A usable substantive task opinion was unavailable for this scope.",
    "source_check_excluded": "Source or bounded program evidence excludes the relevant necessary condition in this scope.",
    "program_support": "A scope-matched program check supports this effect under the recorded analysis domain.",
    "source_certificate": "An applicable source deduction supports this policy and effect.",
    "scoped_fee_consent": "The recorded holder-issued amount policy and matching settlement apply to this request and quantity.",
    "productive_outgoing_control": "The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger.",
    "ordinary_paid_credit": "The buyer receives the source-calculated credit for its own payment. This ordinary purchase does not establish a preferential credit under a separate rate change.",
    "nominee_acceptance": "The incumbent alone appoints a candidate, who must personally accept the same office. This judgment covers that handover only.",
    "incoming_only": "The control is applied to the recipient, not to the holder of the debited position.",
    "same_request_bypass": "Another ordinary entry remains available for the same holder, asset and positive transfer request.",
    "partial_quota": "The source restricts transfer size but permits a positive ordinary transfer under the same control.",
    "zero_quantity": "Every relevant credit on this branch is restricted to a zero quantity.",
    "no_debit_in_scope": "The identified operation only credits this financial family; no causal amount use supports the proposed debit.",
    "guarded_state_change": "The located state change is confined to a branch requiring the established role.",
    "covered_holder_grant": "The issuer key belongs to the debited holder and the same spender consumes an allowance covering the actual debit.",
    "scoped_counter": "The committing update records a nonfinancial count. The located use has no independently established entitlement effect.",
    "revised_policy_not_read": "The changed policy or stage has no applicable source reading yet. The prior check concerns a different interpretation.",
    "local_bookkeeping": "The located numerical bookkeeping update has no source-dependent authorization or entitlement use.",
    "debit_without_issuance": "The committed redemption debits existing positions and makes a settlement; no new token entitlement is credited.",
    "core_mismatch": "The interpretation and the underlying source object or condition do not agree.",
    "unrestricted_termination_decision": "The applied entry can end the contract without qualifying the deciding caller. The payout recipient does not authorize that decision.",
    "detached_local_holder_switch": "The applied public outgoing entries do not use this switch to restrict the holder. A getter alone does not restrict spending.",
    "origin_only_decider": "The applied termination condition authenticates the transaction origin. It does not bind the immediate deciding caller to that authority.",
    "unrestricted_issuance_decision": "The applied entry lets a caller choose the amount credited to the bound account without the governing qualification required for this issuance.",
    "scoped_semantic_conflict":"The located duty and the deciding caller conflict at this applied source effect; this is a scoped semantic prediction.",
    "scoped_semantic_normal":"The scoped reading and the actual authorization or ordinary use support this effect.",
    "not_reviewed": "An essential entry in the requested scope was not analyzed.",
}

def opinion(status, reason, locations=()):
    return {"status": status, "reason": reason, "locations": list(locations)}

def describe(category, reason):
    return "Judgment concerns " + EFFECT.get(category, "the stated source effect") + ". " + DETAIL.get(reason, DETAIL["scope_missing"])

def role_ids(inv, oid, row):
    raw=inv.f.paths[row["path"]]["raw"]
    return {role["declaration"] for proof in path_qualification(inv.f,oid,raw) for role in proof["roles"]}

def identity_guard(guard, roles):
    return guard.get("op") == "==" and any(x.get("kind")=="actual_sender" for x in guard.get("args",[])) and any(
        x.get("kind")=="storage" and x["root"] in roles and not x.get("segments") for x in guard.get("args",[]))

def feasible_source_guards(guards):
    from pr_next_joint.frontend.path_ir import conditions_possible
    try:
        return conditions_possible(guards)
    except (ValueError, RecursionError):
        return False

def office_guard(guard, cell):
    """Check whether this declaration is necessary on all disjuncts."""
    from .roles import _roots
    return cell["root"] in _roots(guard,{cell["root"]})

def exception_authority(inv, oid, office, guard):
    """An office can be necessary only while a separately governed restriction is active."""
    args = guard.get('args', [])
    if guard.get('op') not in ('||', 'or') or len(args) != 2:
        return set()
    for exemption, alternative in (args, args[::-1]):
        if not office_guard(exemption, office):
            continue
        switch = alternative['args'][0] if alternative.get('op') == '!' else alternative
        if switch.get('kind') != 'storage' or keys(switch) or value_type(switch, inv.f.lookup(oid)) != 'bool':
            continue
        target = inv.f.operations[oid]['target']
        writers = inv.graph.access.get((target, switch['root']), {}).get('writers', ())
        principal_sets = []
        for writer in writers:
            for branch in inv.f.summaries.rows(writer):
                writes = [w for w in branch['ordered_writes'] if key(w['path']) == key(switch)]
                if not writes:
                    continue
                principals = role_ids(inv, writer, branch)
                if branch['residuals'] or not principals:
                    return set()
                value = writes[-1]['value']
                if value.get('kind') == 'parameter' and value.get('type') == 'bool' or (
                        value.get('kind') == 'literal' and value.get('value') is (alternative.get('op') == '!')):
                    principal_sets.append(principals)
        if principal_sets:
            return set.intersection(*principal_sets)
    return set()


def dependency_state(inv, row, effect):
    """Classify the selected effect, never the mere presence of a call."""
    reasons = inv.f.call_summaries.effect_dependencies(row, effect)
    critical = {'condition_or_value_requires_external_result', 'same_scope_possible_storage_change',
                'same_path_propagating_revert'}
    state = 'critical' if critical.intersection(reasons) else 'relevance_unknown' if reasons else 'proved_irrelevant'
    token = (row.get('operation', effect.get('oid')), row['path'], key(effect.get('where', {})))
    inv.__dict__.setdefault('_scoped_dependency_states', {})[token] = {
        'effect': effect.get('id'), 'operation': effect.get('oid'), 'path': row['path'],
        'location': effect.get('where', {}), 'state': state, 'reasons': list(reasons)}
    return state


def high_impact_reader(inv, oid, row, visited=()):
    """A caller qualification is a lead; its use must protect actual influence."""
    f=inv.f;lk=f.lookup(oid);uncertain=bool(row.get('residuals'))
    for effect in row['effects']:
        if effect.get('kind') in ('native_transfer','native_selfdestruct'):
            d=dict(effect,oid=oid,where=effect.get('source',{}))
            if dependency_state(inv,row,d)=='proved_irrelevant': return True
            uncertain=True
        else:uncertain=True
    from .ledger import grant_for
    from pr_next_joint.frontend.storage import selector_relation
    for w in row['ordered_writes']:
        cell=w['path'];sg,qty=local_delta(w);account=holder(cell,lk)
        d=dict(oid=oid,cell=cell,write=w,where=w['source'])
        if dependency_state(inv,row,d)!='proved_irrelevant':
            uncertain=True;continue
        if account and sg and not unit_origin(inv.backend,oid,cell):
            from .scope_relevance import nonfinancial
            if not nonfinancial(inv.backend,oid,cell):uncertain=True
        if account and sg and unit_origin(inv.backend,oid,cell):
            if sg=='-' and account.get('kind')!='actual_sender':
                grant=grant_for(inv.backend,oid,f.paths[row['path']]['raw'],cell)
                if grant is None:return True
            if sg=='+' and not any(local_delta(v)[0]=='-' and selector_relation(v['path'],cell)=='same_shape' for v in row['ordered_writes']):
                if not paid_credit(inv,oid,row,cell):return True
        if (not keys(cell) and value_type(cell,lk) in ('address','address payable') and cell['root'] not in visited):
            if office_use(inv,oid,cell,(*visited,cell['root'])):return True
    return None if uncertain else False


def office_use(inv, oid, cell, visited=()):
    target=inv.f.operations[oid]['target']
    from .shared_effect_bridge import authority_effect_links
    for edge,row in authority_effect_links(inv.f,target,cell):
        use=edge['use']
        if use==oid or inv.f.operations[use]['generated_getter']:continue
        if (any(office_guard(g,cell) or exception_authority(inv,use,cell,g) for g in row['guards'])
                and feasible_source_guards(row['guards']) and high_impact_reader(inv,use,row,visited)):
            return use
    return None

def handover(inv,oid,rows):
    """A nomination is local to its incumbent, and acceptance to the nominated caller."""
    from .roles import _role_index
    f=inv.f;target=f.operations[oid]['target'];lk=f.lookup(oid)
    def address_operand(value):
        # A cast to uint160 preserves an address-valued nominee exactly.
        if value.get('kind')=='integer_cast' and value.get('type') in ('uint160','address','address payable'):
            inner=value['input']
            if inner.get('kind')=='storage' and value_type(inner,lk) in ('address','address payable'):return inner
            if inner.get('kind')=='parameter' and lk.nodes.get(inner['id'],{}).get('typeDescriptions',{}).get('typeString') in ('address','address payable'):return inner
        return value
    def nominators(slot,office):
        positive=[]
        for writer in inv.graph.access.get((target,slot['root']),{}).get('writers',()):
            for row in f.summaries.rows(writer):
                for w in row['ordered_writes']:
                    if key(w['path'])!=key(slot) or w['value'].get('kind')=='literal' and w['value'].get('value')==0:continue
                    if row['residuals'] or w['value'].get('kind') not in ('actual_sender','parameter') or not any(office_guard(g,office) for g in row['guards']):return False
                    positive.append(writer)
        return bool(positive)
    for row in rows:
        if row['residuals'] or row['effects'] or not row['ordered_writes']:return None
        # Clearing is part of acceptance only for a slot actually consumed
        # as the source of the incumbent write in this same committing path.
        consumed_slots={key(source) for w in row['ordered_writes'] for source in [address_operand(w['value'])]
                        if source.get('kind')=='storage' and not keys(source)
                        and any(office_guard(g,source) for g in row['guards'])
                        and nominators(source,w['path'])}
        for w in row['ordered_writes']:
            dst=w['path'];v=address_operand(w['value'])
            if keys(dst) or value_type(dst,lk) not in ('address','address payable'):return None
            if v.get('kind')=='literal' and v.get('value')==0 and key(dst) in consumed_slots:continue
            if v.get('kind')=='storage' and key(v) in consumed_slots and nominators(v,dst):continue
            if v.get('kind')=='parameter':
                # The receiver must actually use the nominated slot to become the incumbent.
                if any(key(address_operand(peer['value']))==key(dst) and any(office_guard(g,dst) for g in use['guards'])
                       and not keys(peer['path']) and any(office_guard(g,peer['path']) for g in row['guards']) and nominators(dst,peer['path'])
                       for reader in inv.graph.access.get((target,dst['root']),{}).get('readers',())
                       for use in f.summaries.rows(reader) for peer in use['ordered_writes']):continue
            return None
    if rows and any(w['value'].get('kind')!='literal' for r in rows for w in r['ordered_writes']):
        return opinion('normal','nominee_acceptance',[f.operations[oid]['source']])
    return None


def normal_authorization_reading(inv,q,rows):
    """Check a source-bound normal precondition only on all claimed committing branches."""
    oid=inv.root(q);prop=q.get('property') or {};cat=prop.get('category')
    if not rows or any(r['residuals'] for r in rows):return None
    role_only=cat=='AC' and q['current']['assessment']=='normal'
    if role_only:
        expected=(prop.get('expected_authorization') or {}).get('compiled_authorization') or {}
        if expected.get('competing_interpretations'):return None
        subj=expected.get('subject') or {}
        if q['current'].get('_opinion_message'):
            from pr_next_joint.frontend.path_ir import conditions_possible
            if not expected.get('predicate') or expected.get('necessary_only') or (prop.get('expected_authorization') or {}).get('unresolved_relations'):
                return None
            try:
                if any(conditions_possible(r['guards'], expected['predicate']) for r in rows):
                    return None
            except (ValueError, RecursionError):
                return None
        if subj.get('kind')=='storage' and all(subj['root'] in role_ids(inv,oid,r) for r in rows):
            return opinion('normal','applicable_role_guard',[inv.f.operations[oid]['source']])
    return None

def caller_input_conditions(guards, phase_guard=None):
    """A caller can supply a positive unsigned input; this restriction conveys no office or grant."""
    for term in guards:
        if phase_guard is not None and key(term)==phase_guard:continue
        for atom in conjuncts(term):
            op=atom.get('op');args=atom.get('args',())
            if len(args)!=2:return False
            parameter,bound=args
            if parameter.get('kind')=='literal':
                parameter,bound=bound,parameter
                op={'<':'>','<=':'>=','!=':'!='}.get(op)
            if (parameter.get('kind')!='parameter' or not parameter.get('type','').startswith('uint')
                    or bound.get('kind')!='literal' or type(bound.get('value')) is not int):
                return False
            if (op,bound['value']) not in (('>',0),('!=',0),('>=',0),('>=',1)):return False
    return True


def business_arm(term, lookup):
    """Retain source conditions; an unsupported shortcut is not literal false."""
    if any(n.get('kind') in ('unknown','external_return','credential_recovery','native_call_success') for n in walk(term)):
        return None
    return term


def committing_control(inv, d, candidate, row):
    """Test a caller-controlled effect on the original success frame in the AC domain."""
    from pr_next_joint.verification.source_worlds import frame, encode_frame
    from pr_next_joint.verification.sequence import qualify, read
    from pr_next_joint.verification.program_encoding import MechanismEncoder
    from pr_next_joint.verification.expressions import Unsupported
    from .initial_state import initial_for_lookup
    oid, pid = d['oid'], row['path']
    lookup = inv.f.lookup(oid)
    family = candidate['family']
    cache = inv.backend.__dict__.setdefault('_committing_controls', {})
    token = (oid, pid, key(d['where']), family, candidate['duty'], reading_version(inv,[oid],'AC'))
    if token in cache:
        return cache[token]
    if not row['committing'] or dependency_state(inv,row,d)!='proved_irrelevant' or inv.backend.remaining() <= 0:
        return None
    try:
        e = MechanismEncoder(lookup)
        terms = []
        quantities = []
        # Two free choices on identical storage and business circumstances
        # distinguish selectable issuance from a fixed allotment.
        for slot in range(2 if family == 'unbacked_issuance' else 1):
            fr = frame(inv.f, oid, pid, slot)
            sym = lambda term: e.expr(qualify(term, slot))
            actor = e.expr(fr['caller'])
            terms.extend((encode_frame(e, fr), actor != 0))
            for guard in row['guards']:
                # encode_frame already checks this original guard. Never strengthen
                # a balance or role test with a synthetic false sufficient arm.
                if business_arm(guard,lookup) is None:return None
                for cell in selectors(guard):
                    if keys(cell) or value_type(cell,lookup)!='bool':continue
                    initial=(initial_for_lookup(lookup) or {}).get('declarations',{}).get(cell['root'],{})
                    if not initial:return None
                    if not initial['explicit_initializer'] and not initial['constructor_writes']:
                        terms.append(sym(cell)==False)
                    elif not state_facts(lookup).get(cell['root'],{}).get('encoded'):
                        return None
            if 'cell' in d:
                cell = qualify(d['cell'], slot)
                before = e.expr(cell)
                after = e.expr(read(cell, fr['writes'], lookup))
                terms.append(after != before)
                if family == 'unbacked_issuance':
                    terms.append(after > before)
                    quantities.append(after - before)
                    quantity_parameters = {n['id'] for n in walk(local_delta(d['write'])[1]) if n.get('kind') == 'parameter'}
                    if slot:
                        terms.append(actor == e.expr(qualify({'kind':'actual_sender'}, 0)))
                        for node in walk([row['guards'], d['cell'], local_delta(d['write'])[1]]):
                            if (node.get('kind') in ('environment','block_number','block_timestamp') or
                                node.get('kind') == 'parameter' and node['id'] not in quantity_parameters):
                                terms.append(sym(node) == e.expr(qualify(node, 0)))
                elif candidate['duty'] == 'holder_issued_grant':
                    idx = keys(d['cell'])
                    issuer = candidate['issuer_key']
                    terms.extend((sym(idx[issuer]) != actor, sym(idx[1-issuer]) == actor, after > 0))
                elif candidate['duty'] == 'guarded_downstream_use':
                    # A verified incumbent/manager grant is a normal source alternative
                    # in this independent acquisition route; stronger H policies still
                    # have their own consumer and same-scope counterchecks.
                    if role_ids(inv,oid,row):return None
                    if keys(d['cell']):
                        terms.append(sym(keys(d['cell'])[0]) == actor)
                    else:
                        terms.append(after == actor)
        if quantities:
            terms.append(quantities[0] != quantities[1])
        result = inv.backend._query(e, e.z.And(*terms), 'source_committing_untrusted_control',
                                    dict(operation=oid, use_path=pid, category='AC', effect_location=d['where'], duty=candidate['duty']))
        confirmed = result['id'] if result.get('bounded_condition_confirmed') else None
        cache[token] = confirmed
        return confirmed
    except (Unsupported, TimeoutError):
        return None


def replacement_status(inv, effect):
    row = inv.f.summaries.paths[effect['path']]
    if not row['committing'] or not feasible_source_guards(row['guards']):
        return 'open'
    if any(office_guard(g, effect['cell']) for g in row['guards']):
        return 'normal'
    candidate = dict(family='grant_then_use', duty='guarded_downstream_use')
    return 'risk' if committing_control(inv, effect, candidate, row) else 'open'


def source_duty_opinion(inv, q):
    """Apply only the relation bound to this committing source occurrence."""
    from .ledger import unit_origin
    rules=inv.semantics.rules
    for effect in q['current'].get('_scope_effects',()):
        candidate=getattr(rules,'source_duties',{}).get(effect)
        if not candidate:continue
        d=rules.effects[effect];oid=d['oid'];pid=candidate['path'];row=inv.f.summaries.paths[pid]
        if any(g['kind']=='dependent_source_expression_limit' for g in inv.f.operations[oid]['gaps']):continue
        if blocked_positive(inv,q,pid,'AC') or not feasible_source_guards(row['guards']):continue
        status='open'; why='policy_missing'; proof=None
        if candidate['family']=='unbacked_issuance':
            qty=local_delta(d['write'])[1]
            from pr_next_joint.frontend.path_ir import op,lit
            if ((proof := committing_control(inv,d,candidate,row)) and sourced_quantity(qty,inv.f.lookup(oid))
                    and feasible_source_guards([*row['guards'],op('>',qty,lit(0))]) and unit_origin(inv.backend,oid,d['cell'])):
                status,why='risk','unbacked_source_issuance'
        elif candidate['duty']=='separate_holder_spending_route':
            qty = local_delta(d['write'])[1]
            from pr_next_joint.frontend.path_ir import op, lit
            if feasible_source_guards([*row['guards'], op('>', qty, lit(0))]):
                status, why = 'risk', 'untrusted_holder_disposition'
        elif candidate['duty']=='holder_issued_grant':
            if candidate['issuer']=='actual_sender':
                status,why='normal','self_delegation'
            elif candidate['issuer']=='parameter' and (proof := committing_control(inv,d,candidate,row)):
                status,why='risk','source_role_reassignment'
        elif candidate['duty']=='guarded_downstream_use':
            handoff=handover(inv,oid,[row])
            if handoff:return handoff
            if any(office_guard(g,d['cell']) for g in row['guards']) or (
                    q['current'].get('_host_source_question') and role_ids(inv,oid,row)
                    and not q['current'].get('_opinion_message')):
                status='normal'
            elif (proof := committing_control(inv,d,candidate,row)):
                status='risk'
            why='source_role_reassignment' if status=='risk' else 'applicable_role_guard'
        elif candidate['family']=='managed_phase':
            if (proof := committing_control(inv,d,candidate,row)):
                status,why='risk','unguarded_governed_effect'
        elif candidate['family']=='managed_lifecycle':
            if candidate['controller_guarded'] or candidate['phase']=='completed':
                status,why='normal','governed_completion'
            elif candidate.get('phase_guard') and (proof := committing_control(inv,d,candidate,row)):
                status,why='risk','unqualified_active_termination'
        if status=='open':continue
        ans=opinion(status,why,[d['where']])
        ans['effects']=[effect]
        ans['source_relation']={'family':candidate['family'],'duty':candidate['duty'],'support_location':candidate['support']}
        if proof:ans['source_relation']['committing_check']=proof
        if candidate.get('use') and candidate['family'] != 'holder_disposition':
            ans['protected_use']=inv.f.operations[candidate['use']]['source']
        if status=='normal':ans['same_scope_authorized']=True
        return ans
    return None


def paid_service_reading(inv,q,rows):
    """Read an explicit sufficient payment opinion against each actual committing arm."""
    from .policy_binding import payment_policy
    oid=inv.root(q);item=q['current'];lk=inv.f.lookup(oid)
    if item.get('_host_source_question') or not isinstance(item.get('claim'),str):return None
    if not rows or any(r['residuals'] or r['effects'] for r in rows):return None
    where={key(w['source']):w['source'] for r in rows for w in r['ordered_writes']}
    if len(where)!=1:return None
    text=item.get('policy_basis') or item['claim']; entry=inv.f.operations[oid]['function'].split('(')[0]
    scopes=set(lk.contract_node.get('linearizedBaseContracts',[]))
    decls=[node for node in lk.decls.values() if node.get('scope') in scopes and node.get('stateVariable')
           and node.get('typeDescriptions',{}).get('typeString') in ('address','address payable') and node.get('name')]
    def paid(g):
        terms=g.get('args',())
        if len(terms)!=2 or g.get('op') not in ('>','>=','<','<='):return False
        v,threshold=terms if g['op'] in ('>','>=') else reversed(terms)
        return (v.get('kind')=='transaction_value' and threshold.get('kind')=='literal' and type(threshold['value']) is int
                and (threshold['value']>0 or threshold['value']==0 and g['op'] in ('>','<')))
    for role in decls or [{'id':None,'name':'unbound'}]:
        status=payment_policy(text,role['name'],[entry])
        if status!='independent':continue
        names_role=mentioned(text,role['name'])
        def entitled(g):
            if paid(g):return True
            if g.get('op') in ('||','or'):
                return all(paid(arm) or names_role and identity_guard(arm,{role['id']}) for arm in g.get('args',()))
            return names_role and identity_guard(g,{role['id']})
        if all(any(entitled(term) for g in r['guards'] for term in conjuncts(g)) for r in rows if r['committing']):
            result=opinion('normal','applicable_payment_qualification',where.values())
            result['same_scope_authorized']=True
            return result
    return None


def fixed_holder_entitlement(inv,oid,rows):
    """One fixed credit per caller with a consumed, non-resettable eligibility flag."""
    lk=inv.f.lookup(oid);locations=[]
    for row in rows:
        if not row['committing']:continue
        if row['effects'] or row['residuals']:return None
        writes=row['ordered_writes']; credits=[w for w in writes if holder(w['path'],lk) and local_delta(w)[0]=='+']
        if len(credits)!=1:return None
        credit=credits[0];qty=local_delta(credit)[1]
        if not qty or qty.get('kind')!='literal' or type(qty.get('value')) is not int or qty['value']<=0:return None
        if holder(credit['path'],lk)!={'kind':'actual_sender'}:return None
        flag=next((g['args'][0] for t in row['guards'] for g in conjuncts(t)
                   if g.get('op')=='!' and len(g.get('args',()))==1 and
                   g['args'][0].get('kind')=='storage' and keys(g['args'][0])==[{'kind':'actual_sender'}]),None)
        if not flag or not any(key(w['path'])==key(flag) and w['value'].get('value') is True for w in writes):return None
        if any(w['raw']['value'].get('value') is not True for w in inv.f.writes.values()
               if inv.f.operations[w['operation']]['target']==inv.f.operations[oid]['target'] and w['raw']['path']['root']==flag['root']):return None
        if any(w is not credit and key(w['path'])!=key(flag) and (keys(w['path']) or local_delta(w)[0]!='+' or key(local_delta(w)[1])!=key(qty))
               for w in writes):return None
        locations.append(credit['source'])
    if not locations:return None
    result=opinion('normal','fixed_holder_entitlement',locations);result['same_scope_authorized']=True
    return result


def ordinary_transfer_reading(inv,q,rows):
    from .ledger import grant_for
    from pr_next_joint.frontend.storage import selector_relation
    if not rows:return None
    oid=inv.root(q); lk=inv.f.lookup(oid); modes=set();sites=[]
    for r in rows:
        if not r['committing']:continue
        if not r['ordered_writes'] and not r['effects'] and not r['residuals']:continue
        selected=set(q['current'].get('_scope_effects',()))
        rules=getattr(inv.semantics,'rules',None)
        focus=[rules.effects[e] for e in selected if rules and e in rules.effects]
        if focus and any(dependency_state(inv,r,d)!='proved_irrelevant' for d in focus):return None
        if not focus and (r['residuals'] or r['effects']):return None
        moves=[(w,*local_delta(w)) for w in r['ordered_writes']]
        pairs=[(w,n,v) for w,sign,n in moves if sign=='-' and holder(w['path'],lk)
               for v,vs,vn in moves if vs=='+' and selector_relation(v['path'],w['path'])=='same_shape'
               and key(n)==key(vn) and key(v['path'])!=key(w['path'])]
        if len(pairs)!=1:return None
        w,n,v=pairs[0];who=holder(w['path'],lk)
        if not unit_origin(inv.backend,oid,w['path']):return None
        normal='holder_own_transfer'
        allowed={key(w['path']),key(v['path'])}
        if who.get('kind')!='actual_sender':
            grant=grant_for(inv.backend,oid,inv.f.paths[r['path']]['raw'],w['path'])
            if not grant:return None
            if not any(key(a['path'])==key(grant) and s=='-' and key(qty)==key(n) for a,s,qty in moves):return None
            if not any(g.get('op') in ('>=','>') and [key(x) for x in g.get('args',[])]==[key(grant),key(n)]
                       for term in r['guards'] for g in conjuncts(term)):return None
            allowed.add(key(grant));normal='holder_issued_transfer_scope'
        extra=any(key(a['path']) not in allowed for a,_,_ in moves)
        if extra and (not focus or any(d.get('kind')=='qualification' or 'cell' not in d or key(d['cell']) not in allowed for d in focus)):
            return None
        sites.append(w['source']);modes.add(normal)
    if len(modes)!=1:return None
    result=opinion('normal',modes.pop(),sites); result['same_scope_authorized']=True
    result['effects']=list(q['current'].get('_scope_effects',()))
    return result


def source_qualification_normal(inv,q,rows):
    """A host-only ordinary qualification scope, not a substitute for an H mandate."""
    if not q['current'].get('_host_source_question') or q['current'].get('_opinion_message'):return None
    rules=inv.semantics.rules;oid=inv.root(q);selected=set(q['current'].get('_scope_effects',()))
    found=[]
    for effect in selected:
        d=rules.effects.get(effect,{})
        if rules.sensitive_effects.get(effect)!='qualification' or 'cell' not in d or 'write' not in d:return None
        r=inv.f.summaries.paths[d['path']]
        if dependency_state(inv,r,d)!='proved_irrelevant':return None
        cell=d['cell']
        if any(office_guard(g,cell) for g in r['guards']):
            found.append(d['where']);continue
        # A source-local self-service marker with no sensitive reader does not
        # become management authority merely because another writer is guarded.
        from .shared_effect_bridge import authority_effect_links
        readers=list(authority_effect_links(inv.f,d['target'],cell))
        if readers and all(high_impact_reader(inv,edge['use'],branch) is False for edge,branch in readers):
            found.append(d['where']);continue
        return None
    if not found:return None
    ans=opinion('normal','guarded_source_effect' if any(office_guard(g,rules.effects[e]['cell']) for e in selected for g in inv.f.summaries.paths[rules.effects[e]['path']]['guards']) else 'local_bookkeeping',found)
    ans.update(same_scope_authorized=True,effects=sorted(selected));return ans


def own_disposition_reading(inv,q,rows):
    """A source-scoped debit of the caller is not authority over another account."""
    oid=inv.root(q);lookup=inv.f.lookup(oid);rules=inv.semantics.rules
    selected=set(q['current'].get('_scope_effects',()))
    focus=[rules.effects[e] for e in selected if e in rules.effects]
    sites=[]
    for row in rows:
        if not row['committing']:continue
        if not row['ordered_writes'] and not row['effects'] and not row['residuals']:continue
        if not focus and (row['effects'] or row['residuals']):return None
        own=[]
        for w in row['ordered_writes']:
            account=holder(w['path'],lookup);sg,amount=local_delta(w)
            if account:
                if account.get('kind')!='actual_sender' or sg!='-' or not unit_origin(inv.backend,oid,w['path']):return None
                own.append(w)
        if not own:return None
        for d in focus:
            if dependency_state(inv,row,d)!='proved_irrelevant':return None
            if d.get('kind')=='qualification':return None
            if d.get('cell') and holder(d['cell'],lookup) is None:return None
        # Only the account debit is concluded normal; aggregate bookkeeping
        # is a different source effect and cannot inherit this conclusion.
        if not selected and len(row['ordered_writes'])!=len(own):return None
        sites.extend(w['source'] for w in own)
    if not sites:return None
    ans=opinion('normal','voluntary_holder_debit',sites);ans['same_scope_authorized']=True
    ans['effects']=sorted(selected)
    return ans


def ac_opinion(inv, q, rows):
    oid=inv.root(q); item=q["current"]; lookup=inv.f.lookup(oid)
    policy=(q.get("property") or {}).get("expected_authorization") or {}
    hypothesis=policy.get("text") or policy.get("basis") or item.get("claim","")
    rules=getattr(inv.semantics,'rules',None)
    if rules:
        office=rules.office_opinion(q,rows)
        if office:return office
    pred=policy.get('compiled_authorization') or {}
    paid=pred.get('source_requirement') or {}
    if paid.get('kind')=='source_role_payment_policy' and pred.get('source_ir_check',{}).get('matches') and rows:
        # Static implication uses every committing path; a distinct branch cannot be
        # classified normal merely because the disjunction was found once.
        from pr_next_joint.frontend.path_ir import conditions_possible
        if paid['permits_payment'] and not inv.f.operations[oid]['gaps'] and all(
                not r['residuals'] and not conditions_possible(r['guards'],pred['predicate']) for r in rows):
            return opinion('normal','applicable_payment_qualification',[inv.f.operations[oid]['source']])
        if pred.get('necessary_only'):
            # Satisfying a known prerequisite does not establish complete authorization.
            # A scoped violation can still be confirmed by the ordinary program check.
            return opinion('open','policy_missing',[inv.f.operations[oid]['source']])
    if item.get('_host_source_question') or not policy.get('text') and not policy.get('basis'):
        normal=ordinary_transfer_reading(inv,q,rows) or own_disposition_reading(inv,q,rows) or fixed_holder_entitlement(inv,oid,rows)
        if normal:return normal
    transition=handover(inv,oid,rows)
    if transition:return transition
    focused=statement_opinion(inv,q,rows)
    if focused:return focused
    normal=normal_authorization_reading(inv,q,rows)
    if normal:return normal
    for row in rows:
        if row["residuals"] or row["effects"]:continue
        guards=[g for term in row["guards"] for g in conjuncts(term)]
        for w in row["ordered_writes"]:
            cell=w["path"]
            if keys(cell) or value_type(cell,lookup) not in ("address","address payable"):continue
            if w["value"].get("kind") not in ("actual_sender","parameter"):continue
            use=office_use(inv,oid,cell)
            if not use:continue
            # Existing explicit policy bindings can be used even when initialization itself is unavailable.
            compiled=policy.get('compiled_authorization') or {}
            subject=compiled.get('subject') or {}
            if (not guards and subject.get('root')==cell['root'] and policy.get('polarity')=='asserted'
                    and not item.get('_host_source_question') and item.get('assessment')!='normal'
                    and not blocked_positive(inv,q,row['path'],'AC')):
                return opinion("risk","source_role_reassignment",[w["source"]])
    if not item.get('_opinion_message') and rows and all(role_ids(inv,oid,r) for r in rows) and item["assessment"]=="normal":
        # A guard is a normal alternative only for the role actually asserted.
        roles=set.intersection(*(role_ids(inv,oid,r) for r in rows))
        if any(mentioned(hypothesis,lookup.nodes[rid].get("name")) for rid in roles):
            return opinion("normal","applicable_role_guard",[inv.f.operations[oid]["source"]])
    return opinion("open","policy_missing")

def blocked_positive(inv, q, path, cat):
    """Check existing local contradictions before extending a source opinion."""
    prop=q.get("property") or {}
    from .property_model import validation_key
    for eid in q["evidence"]:
        ev=inv.evidence[eid]
        if ev.get("source_identity")!=inv.f.identity:continue
        if ev.get("kind")=="source_inspection" and ev.get("operation")==inv.root(q):
            if path in ev.get("unknown_guard_paths",[]) or path in ev.get("credential_paths",[]):return True
        if not prop or ev.get("property_identity")!=prop.get("id") and ev.get("property_validation_key")!=validation_key(prop):continue
        if any(r.get("result")=="source_ir_mismatch" and r.get("path") in (None,path) for r in ev.get("amount_correspondence",[])):return True
        for probe in ev.get("queries",[]):
            d=probe.get("details",{})
            if probe.get("answer")!="unsat" or d.get("use_path")!=path or not d.get("property_validated"):continue
            if probe.get("label") in ("direct_effect","authorization_violation"):
                return True
            if probe.get("label")=="local_premises_feasible" and ev.get("observed_measure")=="direct_effect" and (
                    probe.get("exclusion_certificate",{}).get("excludes_only_this_formula")
                    or d.get("prestate",{}).get("global_reachability_exhausted")):
                return True
    return False

def boolean_input_branch(guard):
    # A free boolean argument picks the branch. Guards on persistent state,
    # external returns and derived booleans retain their other dependencies.
    if guard.get('op') in ('!','not') and len(guard.get('args',[]))==1:
        guard=guard['args'][0]
    return guard.get('kind')=='parameter' and guard.get('type')=='bool'


def simple_guard(g,roles,beneficiary=None):
    if identity_guard(g,roles) or g=={"kind":"literal","value":True}:return True
    if g.get("kind")=="storage" and g.get("root") in roles and keys(g)==[{"kind":"actual_sender"}]:return True
    args=g.get("args",[])
    return (beneficiary is not None and len(args)==2 and g.get("op")=="!=" and
            any(key(x)==key(beneficiary) for x in args) and any(x.get("kind")=="literal" and x.get("value") in (0,"0") for x in args))

def block_opinion(inv,q,rows):
    """Scope a blocking claim to actual outgoing holders, units and productive alternatives."""
    from .comparison import ledger_routes
    root=inv.root(q);cat=(q.get('property') or {}).get('category') or q['current'].get('category');target=inv.f.operations[root]["target"]
    writes=[w for r in rows for w in r["ordered_writes"] if role_ids(inv,root,r)]
    controls={w["path"]["root"] for w in writes}
    if not controls:return None
    if cat=='FCR-FREEZE':
        from .scope_relevance import detached_holder_switch
        closed=detached_holder_switch(inv,root)
        if closed:return opinion('excluded',closed['reason'],closed['locations'])
    for label in q.get('evidence',()):
        check=inv.evidence[label];direct=check.get('source_control_result')
        if (direct and check.get('change')==root and check.get('property_identity')==(q.get('property') or {}).get('id')
                and not blocked_positive(inv,q,direct['controller_path'],cat)):
            return direct
    from .blocking import source_block_exclusion
    excluded=source_block_exclusion(inv,q,rows)
    if excluded:return excluded
    routes=ledger_routes(inv.backend,target)
    observed=[]
    for route in routes:
        oid=route["operation"];pid=route["path"];p=inv.f.paths[pid]["raw"]
        if path_qualification(inv.f,oid,p):continue
        src=holder(route["debit"],inv.f.lookup(oid));dst=holder(route["credit"],inv.f.lookup(oid))
        if not src or not dst:continue
        touched=[s for s in selectors(p["guards"]) if s["root"] in controls]
        same=[x for x in touched if keys(x) and key(keys(x)[0])==key(src)]
        receive=[x for x in touched if keys(x) and key(keys(x)[0])==key(dst) and key(src)!=key(dst)]
        moves=[local_delta(w) for w in p["writes"] if key(w["path"])==key(route["debit"])]
        quantity=next((val for sign,val in moves if sign=="-"),None)
        credited=[local_delta(w) for w in p["writes"] if key(w["path"])==key(route["credit"])]
        plain=bool(quantity and any(s=="+" and key(v)==key(quantity) for s,v in credited)
                   and len(p["writes"])==2 and not p.get("sensitive_effects") and not p.get("issues") and not p.get("evaluation_gaps"))
        observed.append((route,src,dst,touched,same,receive,p,quantity,plain))
    affected=[r for r in observed if r[3]]
    if not affected:return None
    locations=[w["source"] for w in writes]
    if cat=="FCR-FREEZE" and all(r[5] and len(r[3])==len(r[5]) and not r[4] for r in affected):
        # Other paths using the same table through a debit or a dependent value invalidate this exclusion.
        if all(r[8] and inv.backend.complete(r[0]["operation"]) for r in affected) and not (q.get('property') or {}).get('value_dependence',{}).get('value_uses'):
            return opinion("normal","incoming_only",locations)
    if cat=="FCR-PAUSE":
        for route,src,dst,cells,_,_,p,qty,plain in affected:
            if not plain:continue
            for alt,asrc,adst,acells,_,_,ap,aqty,aplain in observed:
                if not aplain or acells or ap["guards"] or not aqty or not qty:continue
                # Both implement the same free ordinary sender-to-recipient request,
                # rather than the mere existence of some other successful action.
                if (alt["debit"]["root"]==route["debit"]["root"] and src.get("kind")==asrc.get("kind")=="actual_sender"
                        and dst.get("kind")==adst.get("kind")=="parameter" and qty.get("kind")==aqty.get("kind")=="parameter"
                        and inv.f.operations[alt["operation"]]["target"]==target):
                    if all(a[0]["debit"]["root"]==route["debit"]["root"] for a in affected):
                        return opinion("normal","same_request_bypass",locations)
    # A nonzero quota can bind a quantity but does not establish loss of every positive use.
    if cat in ("FCR-PAUSE","FCR-FREEZE"):
        def positive_quota(row):
            route,src,dst,cells,_,_,path,qty,plain=row
            gs=[g for v in path["guards"] for g in conjuncts(v)]
            if not plain or len(gs)!=1 or len(cells)!=1 or not qty:return False
            g=gs[0]; args=g.get("args",[])
            if not (g.get("op")=="<=" and len(args)==2 and key(args[0])==key(qty) and key(args[1])==key(cells[0])):return False
            setters=[(w,r) for r in rows for w in r["ordered_writes"] if w["path"]["root"]==cells[0]["root"]]
            return bool(setters) and all(any(term.get("op")==">" and key(term["args"][0])==key(w["value"])
                and term["args"][1].get("value")==0 for v in r["guards"] for term in conjuncts(v)) for w,r in setters)
        if all(positive_quota(r) for r in affected):return opinion("normal","partial_quota",locations)
    return None

def quantity_forced_zero(guards,qty,lookup):
    if not qty:return False
    fixed=state_facts(lookup)
    for g in guards:
        if g.get("op") not in ("==","<="):continue
        a,b=g["args"]
        if g["op"]=="==" and key(b)==key(qty):a,b=b,a
        if key(a)!=key(qty):continue
        if b.get("kind")=="literal" and b.get("value")==0:return True
        if b.get("kind")=="storage" and not keys(b) and fixed.get(b["root"],{}).get("encoded") and fixed[b["root"]].get("value")==0:return True
    return False

def paired_reading(inv,q,rows):
    """A source-backed normal reading of the amount norm, scoped to this debit and use."""
    prop=q.get('property') or {};cat=prop.get('category')
    if cat not in ('FCR-TRANSFER','FCR-DESTROY'):return None
    consents=prop.get('financial_consents',{})
    for use,meaning in consents.items():
        if use!=inv.root(q) or meaning.get('meaning')!='net_request_with_fee':continue
        matching=[v for v in q['evidence'] if inv.evidence[v].get('property_identity')==prop['id']
                  and inv.evidence[v].get('observe')==use]
        normal=any(inv.evidence[v].get('property_excluded') for v in matching)
        if normal:return opinion('normal','scoped_fee_consent',[inv.f.operations[use]['source']])
    return None

def covered_delegation(inv,oid,rows):
    from .ledger import grant_for
    from .key_roles import relation
    from pr_next_joint.frontend.storage import selector_relation
    lookup=inv.f.lookup(oid);found=False
    for row in rows:
        if row['residuals'] or row['effects']:return False
        if not row['ordered_writes']:continue
        authorized_path=False
        path=inv.f.paths[row['path']]['raw']
        for w in row['ordered_writes']:
            cell=w['path'];sign,amount=local_delta(w)
            if sign!='-' or holder(cell,lookup) is None or relation(cell,lookup):continue
            # A transfer grant covers movement of the same quantity in this ledger.
            # A stand-alone burn or a debit with another destination still needs its own policy.
            grant=grant_for(inv.backend,oid,path,cell)
            if grant is None:return False
            credits=[v for v in row['ordered_writes'] if selector_relation(v['path'],cell)=='same_shape' and key(v['path'])!=key(cell) and local_delta(v)[0]=='+' and key(local_delta(v)[1])==key(amount)]
            if len(credits)!=1 or any(key(v['path']) not in {key(cell),key(grant),key(credits[0]['path'])} for v in row['ordered_writes']):return False
            if len(row['ordered_writes'])!=3:return False
            # The source-issued bound must cover this debit and be consumed for the same requester.
            limits=[g for guard in row['guards'] for g in conjuncts(guard)]
            if not any(g.get('op') in ('>=','>') and list(map(key,g.get('args',[])))==[key(grant),key(amount)] or
                       g.get('op') in ('<=','<') and list(map(key,g.get('args',[])))==[key(amount),key(grant)] for g in limits):return False
            if not any(key(v['path'])==key(grant) and local_delta(v)[0]=='-' and key(local_delta(v)[1])==key(amount) for v in row['ordered_writes']):return False
            if sum(1 for v in row['ordered_writes'] if key(v['path'])==key(cell) and local_delta(v)[0]=='-')!=1:return False
            roles=relation(grant,lookup)
            if not roles:return False
            for other in inv.f.writes.values():
                if inv.f.operations[other['operation']]['target']!=inv.f.operations[oid]['target']:continue
                otherw=other['raw'];dst=otherw['path']
                if selector_relation(dst,grant)!='same_shape':continue
                index=keys(dst)
                if len(index)!=2:return False
                if index[roles['holder_key']].get('kind')!='actual_sender' and local_delta(otherw)[0]!='-':return False
            authorized_path=True
        if not authorized_path:return False
        found=True
    return found


def sourced_quantity(term,lookup):
    if not isinstance(term,dict):return False
    kind=term.get('kind')
    if kind=='literal':return type(term.get('value')) is int and term['value']>0
    if kind in ('parameter','storage'):
        return str(term.get('type') or (value_type(term,lookup) if kind=='storage' else '') or '').startswith('uint')
    # Identical subtraction, division by zero and arbitrary inequalities do not
    # establish positive capacity merely by syntax. Keep them with the backend.
    if term.get('op') in ('+','*'):
        return len(term.get('args',()))==2 and all(sourced_quantity(v,lookup) for v in term['args'])
    return False

def paid_credit(inv,oid,row,position=None):
    lookup=inv.f.lookup(oid)
    if not row.get('committing', row.get('flow') in ('normal','returned')):return None
    writes=row.get('ordered_writes',row.get('writes',[]))
    positions=[w for w in writes if holder(w['path'],lookup) and local_delta(w)[0]=='+']
    if position is None and len(positions)!=1:return None
    def price_term(term):
        if term.get('kind')=='transaction_value':return True,True
        if term.get('kind')=='literal' and type(term.get('value')) is int and term['value']>=0:return True,False
        if term.get('kind')=='storage' and not keys(term) and (value_type(term,lookup) or '').startswith('uint'):return True,False
        args=term.get('args',())
        if term.get('op') not in ('*','/','**') or len(args)!=2:return False,False
        values=[price_term(a) for a in args]
        if not all(v[0] for v in values):return False,False
        if term['op']=='/' and values[1][1]:return False,False
        if term['op']=='**' and any(v[1] for v in values):return False,False
        return True,any(v[1] for v in values)
    for w in positions:
        cell=w['path'];buyer=holder(cell,lookup);sg,qty=local_delta(w)
        if position is not None and key(cell)!=key(position):continue
        if buyer.get('kind')!='actual_sender' or not unit_origin(inv.backend,oid,cell):continue
        if not qty or price_term(qty)!=(True,True):continue
        d=dict(oid=oid,where=w['source'],cell=cell,write=w)
        if 'ordered_writes' in row and dependency_state(inv,row,d)!='proved_irrelevant':continue
        if any(local_delta(v)[0]=='-' and v['path']['root']==cell['root'] for v in writes):continue
        return w
    return None


def financial_opinion(inv,q,rows):
    oid=inv.root(q);item=q["current"];prop=q.get('property') or {};cat=prop.get('category') or item.get('category')
    loc=inv.f.operations[oid]["source"];lookup=inv.f.lookup(oid)
    if cat=='FCR-MINT' and rows:
        from .financial_value import paid_intervention
        normal=paid_intervention(inv,q,rows)
        if normal:return normal
        purchases=[paid_credit(inv,oid,row) for row in rows if row['ordered_writes']]
        if purchases and all(purchases) and all(sum(1 for w in r['ordered_writes'] if holder(w['path'],lookup) and local_delta(w)[0]=='+')==1 for r in rows if r['ordered_writes']):
            return opinion('normal','ordinary_paid_credit',[purchases[0]['source']])
    if cat=='FCR-DESTROY':
        from .financial_value import scoped_final_debit
        consent=scoped_final_debit(inv,q,rows)
        if consent:return consent
    if impossible_role(inv,oid):return opinion("excluded","source_check_excluded",[loc])
    if cat in ("FCR-FREEZE","FCR-PAUSE"):
        scoped=block_opinion(inv,q,rows)
        if scoped:return scoped
    if cat=='FCR-TRANSFER' and covered_delegation(inv,oid,rows):
        return opinion('excluded','covered_holder_grant',[loc])
    specific=paired_reading(inv,q,rows)
    if specific:return specific
    structural=[]; uncertain=False
    for row in rows:
        roles=role_ids(inv,oid,row)
        from .shared_effect_bridge import equity_impact_links
        moves = equity_impact_links(inv.backend, oid, row)
        if not moves:
            if row["effects"] or row["residuals"]:uncertain=True
            continue
        guards=[g for term in row["guards"] for g in conjuncts(term)]
        for sign,qty,cell,account,src in moves:
            # Pair by the declaration AND projection. A change in another unit is not compensation.
            from pr_next_joint.frontend.storage import selector_relation
            opposite=[m for m in moves if m[0]!=sign and selector_relation(cell,m[2])=="same_shape"]
            matched=[m for m in opposite if key(m[1])==key(qty)]
            exact=len([m for m in moves if selector_relation(m[2],cell)=="same_shape"])==2 and len(matched)==1
            owned=account.get("kind")=="actual_sender"
            selectable=account.get("kind")=="parameter" and account.get("type") in ("address","address payable")
            simple_path=all(simple_guard(g,roles,account) for g in guards)
            # Extra source conditions must leave a positive quantity feasible.
            # Complex/external conditions continue through the bounded checker.
            from pr_next_joint.frontend.path_ir import op,lit
            positive_amount=sourced_quantity(qty,lookup) and feasible_source_guards(guards+[op('>',qty,lit(0))])
            ordinary_guards=all(simple_guard(g,roles,account) or
                g.get('op') in ('>','>=','!=','<','<=','==') and all(n.get('kind') not in ('storage','unknown','external_return','credential_recovery')
                for n in walk(g)) for g in guards)
            uncomplicated=not blocked_positive(inv,q,row["path"],cat) and not row["residuals"] and not row["effects"] and (
                simple_path or ordinary_guards or all(simple_guard(g,roles,account) or boolean_input_branch(g) for g in guards))
            if exact and sign=='-' and not uncomplicated and roles and not row['effects'] and not row['residuals'] and not blocked_positive(inv,q,row['path'],cat):
                # A balance floor and the matching credit's checked addition constrain
                # amount, not consent. Recognize only the same ledger and same quantity.
                credit=matched[0][2]
                def move_guard(g):
                    if simple_guard(g,roles,account):return True
                    args=g.get('args',())
                    if len(args)!=2:return False
                    left,right=args
                    if g.get('op')=='>=' and key(left)==key(cell) and key(right)==key(qty):return True
                    if g.get('op')=='>' and key(left)==key(qty) and right.get('value')==0:return True
                    return (g.get('op')=='>' and key(right)==key(credit) and left.get('op')=='+'
                            and sorted(key(a) for a in left.get('args',()))==sorted([key(credit),key(qty)]))
                uncomplicated=all(move_guard(g) for g in guards)
            if quantity_forced_zero(guards,qty,lookup):
                structural.append(opinion("normal","zero_quantity",[src]));continue
            if exact and (cat=="FCR-MINT" or cat=="FCR-DESTROY" and key(account)==key(matched[0][3])):
                structural.append(opinion("normal","intra_ledger_transfer" if cat=="FCR-MINT" else "same_position_restored",[src]))
                continue
            if sign=="+" and cat=="FCR-MINT" and account.get("kind")=="storage":
                decl=lookup.nodes.get(account.get("root"),{})
                apart=any(g.get("op")=="!=" and {key(v) for v in g.get("args",[])}=={key(account),key({"kind":"actual_sender"})} for g in guards)
                wants_fixed=bool(re.search(r'fixed|independent|not controlled|uncontrolled|独立|固定',item.get('claim',''),re.I))
                if decl.get("mutability")=="immutable" and apart:
                    structural.append(opinion("normal","no_new_controlled_credit",[src]));continue
            if not roles or not uncomplicated or not positive_amount:
                uncertain=True;continue
            if cat=="FCR-MINT" and sign=="+" and not opposite and (owned or selectable and all(simple_guard(g,roles,account) for g in guards)):
                return opinion("risk","new_entitlement",[src])
            if sign=="-" and selectable:
                if cat=="FCR-TRANSFER" and exact and key(account)!=key(matched[0][3]) and matched[0][3].get("kind") in ("parameter","actual_sender"):
                    return opinion("risk","existing_rights_moved",[src])
                if cat=="FCR-DESTROY" and not opposite:
                    return opinion("risk","uncompensated_debit",[src])
            uncertain=True
    if structural and not uncertain:return structural[0]
    if (cat in CATEGORIES[1:] and not prop.get("value_dependence",{}).get("value_uses")
        and not prop.get("source_linked_control_uses") and not inv.f.summaries.positions(oid)
        and inv.backend.complete(oid) and not any(r["effects"] for r in rows)
        and cat not in prop.get("possible_categories",[])):
        return opinion("normal","parameter_only",[loc])
    return opinion("open","scope_missing",[loc])

def statement_focus(inv,q,rows):
    """Select an actual statement from source anchoring or unambiguous semantic reference."""
    root=inv.root(q);lookup=inv.f.lookup(root);text=q['current'].get('claim','')
    candidates={}
    for row in rows:
        for w in row['ordered_writes']:
            cell=w['path'];node=lookup.nodes.get(cell['root'],{})
            loc=w.get('source') or {}
            if not loc or not mentioned(text,node.get('name')):continue
            candidates[(loc.get('file'),loc.get('start'),loc.get('length'))]=(row,w,node)
    if len(candidates)==1:return next(iter(candidates.values()))
    return None

def statement_opinion(inv,q,rows):
    focus=statement_focus(inv,q,rows)
    if not focus or q.get("office_effects"):return None
    row,w,node=focus
    if not q['current'].get('_opinion_message') and role_ids(inv,inv.root(q),row) and any(mentioned(q["current"].get("claim",""),inv.f.lookup(inv.root(q)).nodes[r]["name"])
                                                   for r in role_ids(inv,inv.root(q),row)):
        return opinion('normal','guarded_state_change',[w['source']])
    from .summary import local_delta
    sign,amount=local_delta(w)
    if sign and not keys(w['path']) and amount and amount.get('kind')=='literal':
        # Only the located bookkeeping update, provided nothing reads it to exercise a right.
        family=w['path']['root'];target=inv.f.operations[inv.root(q)]['target']
        if not inv.f.summaries.dependencies.readers.get((target,family),[]):
            return opinion('normal','local_bookkeeping',[w['source']])
        others=[edge for edge in inv.f.summaries.dependencies.rows.values() if edge['target']==target and edge['read']['root']==family]
        if not any(x['kind']=='guard' or x['writes'] and x['writes']['root']!=family for x in others):
            return opinion('normal','local_bookkeeping',[w['source']])
    return None

def close_profile(inv, q, basis):
    p=q.get('property') or {}
    if basis['status']!='open' or not p:return basis
    who=inv.root(q); cat=p.get('category')
    if cat in ('FCR-TRANSFER','FCR-DESTROY','FCR-MINT'):
        # Source signs refer to the local operation. Only drop a generated
        # sibling if it also lacks a real amount/control consumer elsewhere.
        if q['current'].get('_host_property_parent') and not p.get('source_linked_control_uses'):
            rows=inv.f.summaries.rows(who)
            sig={local_delta(w)[0] for r in rows for w in r['ordered_writes']
                 if holder(w['path'],inv.f.lookup(who)) is not None}
            if sig=={'+'} and cat!='FCR-MINT' and not any(r['effects'] or r['residuals'] for r in rows):
                from pr_next_joint.frontend.storage import selector_relation
                dependency=inv.f.summaries.dependencies
                closure=dependency.forward(who)
                edges=[dependency.rows[k] for k in closure['edge_ids'] if dependency.rows[k]['use']!=who]
                def carries_prior_balance(edge):
                    if edge['kind']!='value' or not edge['writes'] or selector_relation(edge['writes'],edge['read'])!='same_shape':return False
                    target_row=inv.f.summaries.paths[edge['path']]
                    if target_row['effects'] or target_row['residuals']:return False
                    writes=target_row['ordered_writes'][:edge['position']+1]
                    # A second keyed delta may read through the previous write
                    # on the alias arm. The source increments, including their
                    # amounts and guards, still have to be independent.
                    if not any(key(w['path'])==key(edge['read']) for w in writes):return False
                    for write in writes:
                        if selector_relation(write['path'],edge['read'])!='same_shape':continue
                        sign,amount=local_delta(write)
                        if not sign or amount is None or any(
                                selector_relation(cell,edge['read'])=='same_shape' for cell in selectors(amount)):
                            return False
                    return True
                if (closure['fixed_point_over_indexed_definitions'] and not closure['residuals']
                        and not inv.f.operations[who].get('gaps') and all(carries_prior_balance(edge) for edge in edges)):
                    return opinion('normal','no_debit_in_scope',[inv.f.operations[who]['source']])
    return basis

def reading_version(inv,operations,category=None):
    related=set(operations)
    for op in operations:
        related.update(inv.__dict__.get('_coverage_control_routes',{}).get((op,category),()))
    return inv.semantics.dependency_identity(related)

def scoped_opinion(inv,q):
    root=inv.root(q);p=q.get('property') or {}
    if root is None:return source_opinion(inv,q)
    # A core read or the registered summary is immutable. New binding, domain,
    # policy, scoped evidence or revision must not reuse a previous judgment.
    token=(p.get('id'),q['version'],len(q['evidence']),bool(q.get('task_conflict')),bool(q.get('retired_property_parent')),reading_version(inv,q['binding']['operations'],p.get('category')))
    cached=q.get('_source_opinion')
    if cached and cached[0]==token:return cached[1]
    value=close_profile(inv,q,source_opinion(inv,q))
    q['_source_opinion']=(token,value)
    return value
def native_scope(inv,q,rows):
    root=inv.root(q);cat=(q.get('property') or {}).get('category') or q['current'].get('category')
    if cat not in ('FCR-MINT','FCR-DESTROY','FCR-TRANSFER'):return None
    if any(r['residuals'] for r in rows):return None
    if not any(r['effects'] for r in rows):return None
    if any(e.get('kind')!='native_transfer' for r in rows for e in r['effects']):return None
    if cat=='FCR-MINT':
        if all(local_delta(w)[0]=='-' for r in rows for w in r['ordered_writes']) and all(r['ordered_writes'] for r in rows):
            return opinion('excluded','debit_without_issuance',[r['ordered_writes'][0]['source'] for r in rows])
    if cat=='FCR-DESTROY':
        deltas={(r['path'],key(w['path'])) for r in rows for w in r['ordered_writes']
                if holder(w['path'],inv.f.lookup(root)) is not None and local_delta(w)[0]=='-'}
        paid={(s['path'],key(s['object'])) for eid in q['evidence'] for e in [inv.evidence[eid]]
              if e.get('source_identity')==inv.f.identity and e.get('operation')==root
              for s in e.get('settlements',[]) if s.get('same_holder_and_unit_full_settlement')}
        if deltas and deltas<=paid:return opinion('excluded','same_position_restored',[inv.f.operations[root]['source']])
    return None

def simple_holder_grant(inv,oid,rows):
    """The writer touches only its own nested record and no protected use reads it."""
    if not rows or any(r['effects'] for r in rows):return False
    deps=inv.f.summaries.dependencies;target=inv.f.operations[oid]['target']
    writes=[w for r in rows if r['committing'] for w in r['ordered_writes']]
    if not writes:return False
    for w in writes:
        ix=keys(w['path'])
        if len(ix)!=2 or ix[0].get('kind')!='actual_sender' or ix[1].get('kind')!='parameter':return False
        for eid in deps.readers.get((target,w['path']['root']),()):
            use=deps.rows[eid]['use']
            if use!=oid and not inv.f.operations[use]['generated_getter']:return False
    return True

def source_opinion(inv,q):
    root=inv.root(q);prop=q.get("property") or {};cat=prop.get("category",q["current"].get("category"))
    if not root or q.get("retired_property_parent") or not q["binding"].get("core_exact"):
        return opinion("open","core_mismatch")
    rows=inv.f.summaries.rows(root)
    loc=inv.f.operations[root]["source"]
    if getattr(inv.semantics,'rules',None):
        dispute=inv.semantics.rules.matching_dispute(q)
        if dispute:return dispute
    if q.get("task_conflict") or prop.get("core_rebinding_required"):return opinion("open","core_mismatch",[loc])
    # Reading a guard can settle its execution behaviour, but cannot supply
    # an unresolved business relation at this same effect.
    if rules:=getattr(inv.semantics,'rules',None):
        office=rules.office_opinion(q,rows) if cat=='AC' else None
        if office:return office
        local=rules.effect_policy_opinion(q)
        if local and local['status']!='open':return local
        if cat=='AC':
            source_normal=source_qualification_normal(inv,q,rows)
            if source_normal:return source_normal
            independent=source_duty_opinion(inv,q)
            if independent:return independent
        if local:return local
    if cat=='AC' and any(r['committing'] for r in rows):
        paid=paid_service_reading(inv,q,rows)
        if paid:return paid
    if cat=='AC' and (prop.get('expected_authorization') or {}).get('unresolved_relations'):
        # Still inspect actual same-key consent and a legitimate handover. These
        # opinions must cover the selected effects, never unrelated siblings.
        known=ordinary_transfer_reading(inv,q,rows) or own_disposition_reading(inv,q,rows) or handover(inv,root,rows)
        if known:return known
        return opinion('open','policy_missing',[loc])
    if not prop.get('category') and cat is None:
        return opinion('open','scope_missing',[loc])
    if not rows:
        if inv.backend.complete(root):return opinion("excluded","no_effect_in_scope",[loc])
        return opinion("open","source_context_missing",[loc])
    native=native_scope(inv,q,rows)
    if native:return native
    explicit=set(q['current'].get('_scope_effects',()))
    if explicit:
        effects=[inv.semantics.rules.effects[e] for e in explicit if e in inv.semantics.rules.effects]
        matched=[(r,[d for d in effects if r['path']==d.get('path') or r['path'] in d.get('branches',{})]) for r in rows]
        rows=[r for r,ds in matched if ds]
        clean=[r for r,ds in matched if ds and all(not inv.f.call_summaries.effect_dependencies(r,d) for d in ds)]
    else:clean=[r for r in rows if not r['residuals'] and not any(e.get('kind')=='dangerous_external_call' for e in r['effects'])
           and not any(n.get('kind') in ('credential_recovery','external_return','unknown','native_call_success') for n in walk(r['guards']))]
    if not clean:return opinion('open','external_dependency',[loc])
    result=ac_opinion(inv,q,clean) if cat=='AC' else financial_opinion(inv,q,clean) if cat in CATEGORIES[1:] else opinion('open','scope_missing',[loc])
    if explicit and cat!='AC' and q['current'].get('_opinion_message') and result['status']=='risk':
        where=lambda a:(a.get('file'),a.get('start'),a.get('length'))
        if not {where(d['where']) for d in effects}.intersection(where(loc) for loc in result['locations']):
            return opinion('open','scope_missing',[d['where'] for d in effects])
    if len(clean)!=len(rows) and result['status']!='risk':
        return opinion('open','external_dependency',[loc])
    return result

```

## source/src/pr_next_joint/investigation/state_encoding.py

原文件SHA256 `b64107887cd866ba2d650dd149c4edb00467e45730fe0073aac0c6e8816fe4fa`

```python
"""Encode a shared constructor state and only committed bounded prefix writes.

Numerical abstract leaves remain congruent functions. Constructor/prefix branch
obligations are inside their disjunction, never unconditional side effects.
"""
import copy
import itertools
import re
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key, walk, lit
from pr_next_joint.frontend.storage import keys, selectors, value_type
from pr_next_joint.verification.sequence import qualify, read
from pr_next_joint.verification.expressions import Unsupported
from .initial_state import CAPABILITY, DEPLOYMENT, domain, initial_for_lookup, family


def total_value(term, check):
    """Pure fixed-width value with no revert or external dependency when discarded.
    This is used only for a disjoint constructor result. Queried cells, all guards
    and any partial arithmetic still go through the normal expression encoder.
    """
    if not isinstance(term,dict):return False
    kind=term.get('kind')
    if kind in ('actual_sender','literal','parameter','environment','contract_address'):return True
    if kind in ('integer_cast','hash'):return total_value(term.get('input'), check)
    if kind=='abi_encoding':return all(total_value(a,check) for a in term.get('arguments',[]))
    if kind=='source_block_hash':return total_value(term.get('current'),check) and total_value(term.get('height'),check)
    if kind=='op' and term.get('op') in ('+','-','*'):
        check(term)  # Preserve this expression's own arithmetic constraints.
        return True
    if kind=='typed_integer_arithmetic':
        args=term.get('args',[]);sym=term.get('operator')
        if term.get('checked') or len(args)!=2:return False
        if sym not in ('+','-','*') and not (sym in ('%','/') and args[1].get('kind')=='literal' and type(args[1].get('value')) is int and args[1]['value']>0):return False
        return all(total_value(a,check) for a in args)
    return False


def _initial_term(value, model, selected_domain):
    if isinstance(value, list): return [_initial_term(x, model, selected_domain) for x in value]
    if not isinstance(value, dict): return value
    kind = value.get('kind')
    if kind == 'actual_sender':
        return {'kind': 'parameter', 'id': -990000001, 'type': 'address', 'initial_identity': 'deployment_caller'}
    if kind == 'parameter':
        return {**value, 'initial_identity': 'constructor_parameter'} if value.get('constructor_parameter') or value.get('id') in model['constructor_parameters'] else value
    if kind in ('environment', 'transaction_value', 'transaction_origin'):
        return {**value, 'initial_identity': 'constructor_environment'}
    if kind == 'storage' and not value.get('instance'):
        row = model['declarations'].get(value['root'])
        if row is None: raise Unsupported('initial_storage_declaration_unresolved')
        segments = _initial_term(value.get('segments', []), model, selected_domain)
        prepared = {**value, 'segments': segments}
        typ = value_type(prepared, model['_lookup'])
        symbolic = selected_domain == CAPABILITY and not row['explicit_initializer'] and (
            not segments and bool(re.fullmatch(r'(?:address(?: payable)?|u?int\d*)', typ or '')) or
            family(value) in model['_amount_families'])
        if symbolic:
            return {**prepared, 'instance': 'initial_storage:' + selected_domain + ':' + model['identity']}
        if typ == 'bool': return lit(False)
        if re.fullmatch(r'(?:address(?: payable)?|u?int\d*|bytes\d+)', typ or '') or (typ or '').startswith(('contract ', 'enum ')):
            return lit(0)
        raise Unsupported('initial_default_type_not_encoded:' + str(typ))
    return {k: _initial_term(v, model, selected_domain) for k, v in value.items()}


def _runtime_candidates(facts, lookup, model, queried):
    """Only real writers of constrained queried roots and their guard prerequisites."""
    relevant = set()
    for cell in queried:
        row = model['declarations'].get(cell['root'], {})
        if row.get('explicit_initializer') or row.get('constructor_writes') or value_type(cell, lookup) == 'bool' or family(cell) not in model['_amount_families'] and keys(cell):
            relevant.add(cell['root'])
    paths = []
    # Include prerequisite role writers; never seed a default-false role table.
    for _ in range(facts.options.prefix_depth + 1):
        before = set(relevant)
        for oid, entry in facts.operations.items():
            if entry['target'] != model['target'] or entry.get('generated_getter'): continue
            for pid, p in facts.operation_paths(oid, True):
                if not any(w['path']['root'] in relevant for w in p['writes']): continue
                if not any(x[1] == pid for x in paths): paths.append((oid, pid, p))
                relevant.update(s['root'] for s in selectors(p['guards']))
        if relevant == before: break
    paths.sort(key=lambda x: (facts.operations[x[0]]['source']['start'], x[1]))
    return paths, relevant


def encode(e, details=None, selected_domain=None):
    selected_domain = selected_domain or domain(e.lookup)
    saved = initial_for_lookup(e.lookup)
    if saved is None: raise Unsupported('host_initial_state_model_missing')
    facts = e.lookup._investigation_facts
    # Non-serialized helpers never enter the domain identity.
    model = {**saved, '_lookup': e.lookup, '_amount_families': {family(r['cell']) for r in saved['candidate_amount_leaves']}}
    queried = [v for _, v in sorted(getattr(e, '_state_cells', {}).items()) if not v.get('instance')]
    prefix_limit=getattr(e,'_initial_prefix_limit',1)
    times=list(getattr(e,'_state_times',{}).values())
    token = digest([selected_domain, saved['identity'], queried,times,prefix_limit])
    cache = e.__dict__.setdefault('_initial_encoding_cache', {})
    if token in cache: return cache[token]
    z = e.z; branches = []; receipts = []; limits = []; before_encoding = getattr(e, '_encoding_initial', False)
    e._encoding_initial = True
    candidates, relevant = _runtime_candidates(facts, e.lookup, model, queried)
    sequences = [()]
    max_count = min(facts.options.max_prefixes,prefix_limit)
    for length in range(1, facts.options.prefix_depth + 1):
        for seq in itertools.product(range(len(candidates)), repeat=length):
            if len(sequences) >= max_count:
                limits.append({'reason': 'initial_prefix_frontier_bound', 'maximum': max_count}); break
            sequences.append(seq)
        if len(sequences) >= max_count: break
    incomplete = [r for rid in relevant for r in saved['runtime_writers']['paths'].get(rid, []) if not r['complete'] and r['flow'] != 'reverted']
    if incomplete: limits.append({'reason': 'initial_relevant_writer_path_incomplete', 'paths': sorted({r['path'] for r in incomplete})})
    def expr(v): return e.expr(_initial_term(v, model, selected_domain))
    try:
        for pi, cp in enumerate(saved['constructor_paths']):
            if cp['flow'] not in ('normal', 'returned'): continue
            if cp.get('issues') or cp.get('evaluation_gaps'):
                limits.append({'reason': 'constructor_effect_unresolved', 'constructor_path': pi,
                               'details': cp.get('issues', []) + cp.get('evaluation_gaps', [])}); continue
            for seq in sequences:
                start = len(e.constraints)
                writes = copy.deepcopy(cp['writes']); terms = []; prefix = []
                try:
                    terms.extend(expr(g) for g in cp['guards'])
                    for value in cp.get('evaluated_terms', []):
                        if not total_value(value,expr):expr(value)
                    for w in writes:
                        typ=value_type(w['path'],e.lookup)
                        if typ in ('string','bytes') and w['value'].get('kind') in ('parameter','literal','fixed_bytes_literal','storage'):continue
                        if w['path']['root'] in relevant or not total_value(w['value'],expr):expr(w['value'])
                    deployer = expr({'kind': 'actual_sender'})
                    terms.append(deployer != 0)
                    for index, candidate in enumerate(seq):
                        oid, pid, path = candidates[candidate]; previous = copy.deepcopy(writes)
                        translate = lambda v: read(qualify(v, 20 + index), previous, e.lookup)
                        terms.extend(expr(translate(g)) for g in path['guards'])
                        for v in path.get('evaluated_terms', []): expr(translate(v))
                        caller = expr(qualify({'kind': 'actual_sender'}, 20 + index)); terms.append(caller != 0)
                        if any(n.get('kind') in ('unknown', 'external_return') for n in walk(path)):
                            raise Unsupported('initial_prefix_critical_external_effect')
                        for w in path['writes']:
                            dst = qualify(w['path'], 20 + index)
                            dst['segments'] = read(dst.get('segments', []), previous, e.lookup)
                            value = translate(w['value']); expr(value)
                            writes.append({**w, 'path': dst, 'value': value})
                        prefix.append({'operation': oid, 'path': pid, 'caller': qualify({'kind': 'actual_sender'}, 20 + index)})
                    # All runtime requests follow the constructor and committed
                    # prefixes. A future setter cannot enable a past request.
                    for field in ('timestamp','number'):
                        relevant_times=[v for v in times if v.get('field',v.get('sequence_role'))==field]
                        if not relevant_times:continue
                        base={'kind':'environment','field':field,'type':'uint256'}
                        previous=expr(base)
                        for index in range(len(seq)):
                            current=expr(qualify(base,20+index));terms.append(current>=previous);previous=current
                        terms.extend(e.expr(v)>=previous for v in relevant_times)
                    for cell in queried:
                        actual = e.expr(cell)
                        expected = expr(read(cell, writes, e.lookup))
                        terms.append(actual == expected)
                    evaluated = e.constraints[start:]; del e.constraints[start:]
                    condition = z.And(*terms, *evaluated)
                    selector = z.Bool('initial_branch_' + token[:16] + '_' + str(len(receipts)))
                    branches.append(z.And(selector, condition))
                    e.__dict__.setdefault('_initial_branch_conditions', {})[str(selector)] = z.And(selector, condition)
                    receipts.append({'selector': str(selector), 'constructor_path': pi, 'prefix': prefix,
                        'explicit_writes': [w['source'] for w in cp['writes']]})
                except (Unsupported, ValueError, KeyError, TypeError) as error:
                    del e.constraints[start:]
                    limits.append({'reason': str(error), 'constructor_path': pi, 'prefix_candidates': list(seq)})
        if not branches:
            # A proved reverting constructor differs from unsupported modeling.
            all_revert = bool(saved['constructor_paths']) and all(p['flow'] == 'reverted' and not p.get('issues') for p in saved['constructor_paths'])
            if not all_revert: raise Unsupported('initial_state_not_encoded:' + str(limits[:2]))
            branches = [z.BoolVal(False)]
        abstract = []
        for cell in queried:
            base = _initial_term(cell, model, selected_domain)
            if any(str(s.get('instance', '')).startswith('initial_storage:') for s in selectors(base)):
                abstract.append({'cell': cell, 'basis': 'uninitialized_typed_scalar_or_frozen_amount_leaf'})
        result = ([z.Or(*branches)], {'analysis_domain': selected_domain, 'initial_model_identity': saved['identity'],
            'analysis': selected_domain, 'shared_constructor_and_prefix': True, 'branches': receipts,
            'encoded_cells': queried, 'abstract_initial_assumptions': abstract, 'limits': limits,
            'prefix_depth_bound': facts.options.prefix_depth, 'prefixes_included': len(sequences),
            'more_prefixes_available':bool(candidates) and prefix_limit<facts.options.max_prefixes,
            'global_reachability_exhausted': not candidates and not limits,
            'explicit_constructor_prefix_executed': False, 'constructor_symbolic_transitions_encoded': True,
            'author_run_initial_state_verified': False})
        cache[token] = result
        return result
    finally:
        e._encoding_initial = before_encoding

```
