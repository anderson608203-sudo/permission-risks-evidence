# 源码文本 · 10

## source/src/pr_next_joint/investigation/coverage.py

原文件 SHA-256 `c88fc47a3ee36ce0eef9295c6e1a88c773c62e106819ceb4601cef475e109ef4`

````python
"""Property dependency accounting, separate from findings and risk definitions."""
from .contracts import CATEGORIES
from .protocol import category_scope
from .request_scope import coverage_facts, claim_entries, privileged_intervention
from .ledger import movements, unit_origin
from .roles import path_qualification
from .initial_state import domain, initial_for_lookup
from pr_next_joint.frontend.storage import selectors, keys, value_type

HARD = {'original_root_has_no_committing_path','original_root_net_effect_is_unchanged',
        'same_scope_actual_full_settlement','single_holder_scope_not_collective_pause',
        'same_control_has_no_dependency_on_declared_entry_effect',
        'matched_direct_effect_impossible_on_all_applicable_positions_and_paths',
        'authorization_acquisition_premise_refuted','expected_authorization_covers_all_applicable_paths',
        'source_supported_applicable_normal_authorization'}
UNKNOWN = {'source_identity_ambiguous_or_unresolved','minimum_source_inspection_not_executed',
           'unique_critical_external_guard_not_established','signature_dependent_success_not_verified',
           'E1_cumulative_numeric_bound_mapping_pending','financial_intervention_source_unresolved'}


def possible_properties(inv, entries):
    if inv.f.options.scope == 'AC':return ['AC']
    from .scope_relevance import directory
    from pr_next_joint.core import digest
    cache=inv.__dict__.setdefault('_directory_certificates',{})
    stamp=(inv.semantics.version,digest(inv.semantics.active_scope))
    controls=_control_categories(inv);cats=set()
    for oid in entries:
        if oid not in inv.f.operations:continue
        token=(stamp,oid)
        if token not in cache:cache[token]=directory(inv,oid,controls.get(oid,[]))
        cats.update(cache[token]['possible_categories'])
    return sorted(cats)


def _control_categories(inv):
    from pr_next_joint.core import digest
    from pr_next_joint.frontend.storage import selector_relation
    from .ledger import native_only_position
    from .key_roles import relation
    from .scope_relevance import potential_role,nonfinancial
    stamp=(inv.semantics.version,digest(inv.semantics.active_scope))
    cached=getattr(inv,'_coverage_control_index',None)
    if cached and cached[0]==stamp:return cached[1]
    inv._coverage_control_routes={}
    f=inv.f;index={};writers={}
    for w in f.writes.values():
        token=(f.operations[w['operation']]['target'],w['raw']['path']['root'])
        writers.setdefault(token,[]).append(w)
    for use,entry in f.operations.items():
        for _,p in f.operation_paths(use,True):
            minus=[c for c in movements(inv.backend,use,p)['-'] if not nonfinancial(inv.backend,use,c)]
            if not minus:continue
            for control in selectors(p['guards']):
                typ=value_type(control,f.lookup(use)) or ''
                if typ!='bool' and not typ.startswith(('uint','int')):continue
                # Ledger sufficiency is not a distinct freeze/pause control.
                if any(selector_relation(control,c)=='same_shape' for c in minus):continue
                if unit_origin(inv.backend,use,control):continue
                if (relation(control,f.lookup(use)) or {}).get('kind')=='authorization_quantity':continue
                for w in writers.get((entry['target'],control['root']),[]):
                    writer=w['operation']
                    if writer==use:continue
                    if selector_relation(w['raw']['path'],control)!='same_shape' or inv.graph._disjoint_keys(w['raw']['path'],control):continue
                    if potential_role(f,writer,f.paths[w['path']]['raw']):
                        cat='FCR-FREEZE' if keys(control) else 'FCR-PAUSE'
                        index.setdefault(use,set()).add(cat);index.setdefault(writer,set()).add(cat)
                        inv.__dict__.setdefault('_coverage_control_routes',{}).setdefault((writer,cat),set()).add(use)
    inv._coverage_control_index=(stamp,index)
    return index








def obligation_scope(inv, assessments, blocked):
    """Routes and directory residuals share the same dependency records."""
    from pr_next_joint.core import digest
    from pr_next_joint.frontend.path_ir import key
    from .summary import get_summaries
    categories = {'AC'} if inv.f.options.scope == 'AC' else set(CATEGORIES[1:])
    summaries = get_summaries(inv.f)
    local = {}
    by_entry = {}
    for qid, q in inv.issues.items():
        a = assessments[qid]
        p = q.get('property') or {}
        root = inv.root(q)
        cat = a.get('category')
        excluded = a['scope'].get('route_status') == 'excluded'
        supported = a['reportable']
        relevant = {cat} if cat in categories else set(p.get('possible_categories', [])) & categories
        if not relevant:
            # A missing resource answer can leave the compiled category empty.
            # Keep the original bound claim's task category so a independently
            # false necessary condition (for example no privilege) can close
            # that route; its unanswered question is then nondecisive.
            relevant.update(category_scope(q['current'],inv.f.options.scope))
        if root and not relevant:
            relevant.update(possible_properties(inv, {root}))
        status = 'supported' if supported else 'excluded' if excluded else 'open'
        source_exclusion=None
        if root and inv.f.options.scope=='FCR' and not supported:
            actual=set(possible_properties(inv,{root}))
            # A false source necessary condition closes this claim even when
            # a different (nondecisive) return value remains unknown.
            if relevant and not (relevant & actual):
                source_exclusion={'categories':sorted(relevant),'basis':'whole_source_route_necessary_condition_absent',
                    'source_identity':inv.f.identity,'operation':root}
                excluded=True;status='excluded'
        row = {'issue': qid, 'target': p.get('target'), 'analysis_domain': p.get('domain'),
               'property': p.get('id'), 'category': cat, 'entries': [root] if root else [],
               'closed': supported or excluded, 'state': status,
               'affected_categories': [] if supported or excluded else sorted(relevant),
               'reason': a['reasons'], 'dependencies': a['scope'].get('property_support', []),
               'exclusion': a['scope'].get('authorization_counterevidence', []),
               'conditions_are_not_closed_by_mutual_reference': True}
        if source_exclusion:row['necessary_condition_certificate']=source_exclusion
        local[qid] = row
        by_entry.setdefault(root, []).append(row)
    # A checked writer->use comparison is also evidence for the use's control
    # obligation. It is not a new finding rooted at that use, and must not
    # close a different writer, effect class, property version or source.
    control_exclusions={}
    for qid,q in inv.issues.items():
        row=local[qid];prop=q.get('property')or{};writer=inv.root(q)
        if row['state']!='excluded' or row['category'] not in ('FCR-FREEZE','FCR-PAUSE'):continue
        for label in q['evidence']:
            ev=inv.evidence[label]
            if (ev.get('source_identity')==inv.f.identity and ev.get('property_identity')==prop.get('id') and
                ev.get('change')==writer and ev.get('property_excluded') and not ev.get('local_errors')):
                control_exclusions.setdefault((writer,ev.get('observe'),row['category']),[]).append(label)
    obligations, gaps = [], []
    for oid, operation in inv.f.operations.items():
        rows = summaries.rows(oid, False)
        cats = set(possible_properties(inv, {oid}))
        directory_certificate=None
        if inv.f.options.scope=='FCR':
            directory_certificate=getattr(inv,'_directory_certificates',{}).get(
                ((inv.semantics.version,digest(inv.semantics.active_scope)),oid))
        related = by_entry.get(oid, [])
        cats.update(c for row in related for c in row['affected_categories'])
        effects = [r for r in rows if r['committing'] and (r['ordered_writes'] or r['effects'])]
        residuals = [x for r in rows for x in r['residuals']]
        states = {}
        for cat in categories:
            known = [r for r in related if r['category'] == cat or cat in r['affected_categories']]
            open_rows = [r for r in known if not r['closed']]
            necessary_certificates=[]
            for q in inv.issues.values():
                if inv.root(q)!=oid or local[q['id']]['category']!=cat or not local[q['id']]['closed']:continue
                prop=q.get('property')or{}
                for label in q['evidence']:
                    ev=inv.evidence[label];cert=ev.get('necessary_condition_route_coverage')or{}
                    if (ev.get('property_identity')==prop.get('id') and ev.get('property_excluded') and
                        cert.get('source_identity')==inv.f.identity and cert.get('operation')==oid and
                        cert.get('all_source_routes_accounted')):necessary_certificates.append(label)
            control_writers={writer for (writer,control_cat),uses in
                getattr(inv,'_coverage_control_routes',{}).items() if control_cat==cat and oid in uses}
            control_certificates=[{'writer':writer,'use':oid,
                'evidence':control_exclusions.get((writer,oid,cat),[])} for writer in sorted(control_writers)]
            controls_closed=(bool(control_writers) and all(c['evidence'] for c in control_certificates) and
                cat in ('FCR-FREEZE','FCR-PAUSE') and inv.backend.complete(oid) and directory_certificate and
                not directory_certificate.get('unresolved_same_storage_calls') and
                not directory_certificate.get('unread_effect_residuals') and
                not any(cat in route.get('possible_categories',[]) for route in directory_certificate.get('source_routes',[])))
            if cat not in cats and not open_rows:
                states[cat] = {'state': 'excluded', 'basis': 'source_effect_and_privilege_relevance',
                               'source_paths': [r['path'] for r in rows],
                               'dependency_certificate':digest(directory_certificate) if directory_certificate else None}
            elif open_rows or residuals and not necessary_certificates:
                states[cat] = {'state': 'open', 'basis': 'decisive_property_or_source_residual',
                               'issues': [r['issue'] for r in open_rows], 'residuals': residuals}
            elif controls_closed:
                states[cat] = {'state':'excluded','basis':'all_source_control_writers_excluded_for_this_use',
                    'control_comparisons':control_certificates,
                    'other_effect_classes_not_closed_by_this_certificate':True}
            elif known and all(r['closed'] for r in known) and (inv.backend.complete(oid) or necessary_certificates):
                # Same category does not imply the same resource. Independent
                # positions require an actual property for their own scope.
                covered = set()
                for q in inv.issues.values():
                    if inv.root(q) == oid and local[q['id']]['closed']:
                        covered.update(key(c) for c in (q.get('property') or {}).get('objects', []))
                cells = {key(e['cell']) for r in effects for e in r['numeric_effects'] if e['holder'] is not None}
                required_uses=getattr(inv,'_coverage_control_routes',{}).get((oid,cat),set())
                checked_uses=set()
                for q in inv.issues.values():
                    if inv.root(q)!=oid or not local[q['id']]['closed'] or local[q['id']]['category']!=cat:continue
                    for label in q['evidence']:
                        ev=inv.evidence[label]
                        if ev.get('property_identity')==(q.get('property') or {}).get('id') and (ev.get('property_excluded') or
                            any(x.get('validated_bounded_witness') and x['label']=='financial_block' for x in ev.get('queries',[]))):
                            checked_uses.add(ev.get('observe'))
                complete=cells<=covered and required_uses<=checked_uses
                states[cat] = {'state': 'excluded' if complete else 'open',
                               'basis': 'source_positions_and_resolved_properties', 'uncovered_positions': sorted(cells-covered),
                               'necessary_condition_certificates':necessary_certificates,
                               'unchecked_control_uses':sorted(required_uses-checked_uses)}
            else:
                states[cat] = {'state': 'open', 'basis': 'relevant_source_scope_without_resolved_property'}
        affected = sorted(c for c in categories if states[c]['state'] == 'open')
        token = digest([operation['target'], oid])
        record = {'id': 'obligation_' + token[:20], 'target': operation['target'], 'operations': [oid],
                  'category_states': states, 'closed': not affected, 'affected_categories': affected,
                  'possible_categories': sorted(cats),
                  'source_dependency_certificate':directory_certificate,
                  'entry_states': [{'operation': oid, 'states': {c: 'open' if c in affected else 'resolved' for c in categories}}],
                  'call_dependencies': inv.f.call_summaries.dependencies(oid, {
                      s['root'] for r in rows for s in selectors([r['guards'], r['ordered_writes']])})}
        obligations.append(record)
        if affected:
            gaps.append(dict(record, reason='source_obligation_not_resolved'))
    # Unbound and rejected source clues are independent residuals. Do not erase
    # them when the directory or model candidate list happens to be empty.
    nondecisive=[]
    for raw in inv.coverage_gaps:
        if raw.get('issue') in local and local[raw['issue']]['closed']:
            continue
        bound=local.get(raw.get('issue'))
        if bound and bound['entries']:
            # A missing optional reply is a dependency of its actual source
            # property, not of all five categories. The directory independently
            # retains unread/effect/call residuals for the same entry.
            affected=sorted(set(bound['affected_categories']) | set(possible_properties(inv,bound['entries'])))
            if not affected:
                nondecisive.append(dict(raw,reason_for_exclusion='no relevant five-class source dependency',
                    entries=bound['entries']))
                continue
            gaps.append(dict(raw,affected_categories=affected,closed=False,
                dependency_scope='bound_property_and_source_directory'))
            continue
        affected = category_scope(raw, inv.f.options.scope)
        if not affected and raw.get('category') in CATEGORIES+('ADDITIONAL',):
            # The independently scanned source directory remains authoritative;
            # an explicitly different task/class is not a missing dependency
            # of every class in this task.
            continue
        if not affected:
            affected = sorted(categories)
        if raw.get('reason')=='unbound_original_claim' and raw.get('assessment')=='normal':
            proved=[c for c in affected if obligations and all(o['category_states'][c]['state']=='excluded' for o in obligations)]
            if proved:
                nondecisive.append(dict(raw,independently_closed_categories=proved,
                    reason_for_exclusion='complete source obligations independently exclude this normal absence claim',
                    certificates=[o['id']for o in obligations]))
                affected=[c for c in affected if c not in proved]
            if not affected:continue
        gaps.append(dict(raw, affected_categories=affected, closed=False))
    open_categories = {c for r in gaps for c in r.get('affected_categories', [])}
    blocked.update(open_categories)
    return {'schema': 'shared-route-dependencies-r1', 'request_scope': (inv.initial_manifest or {}).get('requested_reading'),
            'declaration': inv.task_declaration, 'whole_reading_eligible': not open_categories,
            'eligibility_reasons': ['decisive_dependencies_open'] if open_categories else [],
            'known_category_gaps': gaps, 'source_local_scopes': local, 'obligations': obligations,
            'nondecisive_model_gaps':nondecisive,
            'neutral_scope_scan_executed': bool(inv.f.selected),
            'negative_eligible_categories': sorted(categories - open_categories),
            'delivery_and_model_declaration_are_not_completion': True}

````

