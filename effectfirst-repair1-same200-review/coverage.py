"""Property dependency accounting, separate from findings and risk definitions."""
from .contracts import CATEGORIES
from pr_next_joint.frontend.path_ir import walk
from .protocol import category_scope
from .request_scope import coverage_facts, claim_entries, privileged_intervention
from .ledger import movements, unit_origin, native_only_position
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
    controls=_control_categories(inv);cats=set()
    for oid in entries:
        if oid not in inv.f.operations:continue
        token=(inv.semantics.dependency_identity([oid]),digest(inv.semantics.active_scope),oid)
        if token not in cache:cache[token]=directory(inv,oid,controls.get(oid,[]))
        cats.update(cache[token]['possible_categories'])
    return sorted(cats)


def _control_categories(inv):
    from pr_next_joint.core import digest
    from pr_next_joint.frontend.storage import selector_relation
    from .ledger import native_only_position
    from .key_roles import relation
    from .scope_relevance import potential_role
    stamp=inv.f.identity
    cached=getattr(inv,'_coverage_control_index',None)
    if cached and cached[0]==stamp:return cached[1]
    inv._coverage_control_routes={}
    f=inv.f;index={};writers={}
    for w in f.writes.values():
        token=(f.operations[w['operation']]['target'],w['raw']['path']['root'])
        writers.setdefault(token,[]).append(w)
    for use,entry in f.operations.items():
        for _,p in f.operation_paths(use,True):
            # Immutable structural index. Currency semantics are read by the local consumer.
            minus=[c for c in movements(inv.backend,use,p)['-'] if not (relation(c,f.lookup(use)) or {}).get('kind')=='authorization_quantity']
            if not minus:continue
            for control in selectors(p['guards']):
                typ=value_type(control,f.lookup(use)) or ''
                if typ!='bool' and not typ.startswith(('uint','int')):continue
                # Ledger sufficiency is not a distinct freeze/pause control.
                if any(selector_relation(control,c)=='same_shape' for c in minus):continue
                if (relation(control,f.lookup(use)) or {}).get('kind')=='authorization_quantity':continue
                for w in writers.get((entry['target'],control['root']),[]):
                    writer=w['operation']
                    if writer==use:continue
                    if selector_relation(w['raw']['path'],control)!='same_shape' or inv.graph._disjoint_keys(w['raw']['path'],control):continue
                    if potential_role(f,writer,f.paths[w['path']]['raw']):
                        from .dependencies import control_candidates
                        from .summary import holder
                        for cat in control_candidates(control,[holder(c,f.lookup(use)) for c in minus]):
                            index.setdefault(use,set()).add(cat);index.setdefault(writer,set()).add(cat)
                            inv.__dict__.setdefault('_coverage_control_routes',{}).setdefault((writer,cat),set()).add(use)
    inv._coverage_control_index=(stamp,index)
    return index








from .source_opinion import describe, simple_holder_grant
from .summary import local_delta
from pr_next_joint.core import digest

def basic_entry(inv,oid,rows,cat,effect_locations=None):
    """Read concrete declaration effects before assigning any category eligibility.

    Produces a detection opinion for this family, not an absence proof.
    In particular an opinion about one entry cannot read another target by proxy.
    """
    from .summary import local_delta,holder
    from .policy_binding import conjuncts
    from .source_opinion import office_use,quantity_forced_zero,identity_guard,role_ids
    from .initial_state import initial_for_lookup
    from pr_next_joint.frontend.path_ir import key
    from pr_next_joint.frontend.storage import value_type
    f=inv.f;lk=f.lookup(oid);entry=f.operations[oid]
    committing=[r for r in rows if r['committing']]
    if not rows:return 'unread','not_reviewed'
    if cat=='AC':
        from .source_opinion import handover,covered_delegation
        if handover(inv,oid,committing):return 'reviewed','nominee_acceptance'
        if covered_delegation(inv,oid,committing) and not any(r['effects'] for r in committing):return 'reviewed','covered_holder_grant'
        for r in committing:
            for w in r['ordered_writes']:
                cell=w['path']
                if not keys(cell) and value_type(cell,lk) in ('address','address payable') and office_use(inv,oid,cell):
                    guards=[g for v in r['guards'] for g in conjuncts(v)]
                    if not any(identity_guard(g,{cell['root']}) for g in guards):
                        return 'dispute','unassessed_role_change'
            if any('selfdestruct' in str(e.get('kind','')).lower() for e in r['effects']):
                return 'dispute','policy_missing'
        if not committing:return ('reviewed','no_effect_in_scope') if rows and inv.backend.complete(oid) else ('unread','not_reviewed')
        # This finite AC opinion concerns the examined paths and effects only.
        if simple_holder_grant(inv,oid,rows):return 'reviewed','covered_holder_grant'
        if any(r['effects'] or r['residuals'] for r in committing):return 'dispute','policy_missing'
        return 'reviewed','source_task_reading'
    from .source_opinion import paid_credit
    if cat=='FCR-MINT' and committing:
        if all(paid_credit(inv,oid,r) for r in committing):return 'reviewed','ordinary_paid_credit'
    if cat in ('FCR-FREEZE','FCR-PAUSE'):
        linked=inv.__dict__.get('_coverage_control_routes',{}).get((oid,cat),set())
        if linked:
            has_unit=any(unit_origin(inv.backend,use,cell) for use in linked for _,branch in f.operation_paths(use,True) for cell in movements(inv.backend,use,branch)['-'])
            return 'dispute','scope_missing' if has_unit else 'source_unit_missing'
        return 'reviewed','source_task_reading'
    if cat=='FCR-MINT':
        writers={w['path']['root'] for r in committing if role_ids(inv,oid,r) for w in r['ordered_writes']}
        if writers:
            for rid in writers:
                for use in inv.graph.access.get((entry['target'],rid),{}).get('readers',()):
                    if use==oid:continue
                    for branch in f.summaries.rows(use):
                        buy=paid_credit(inv,use,branch)
                        if buy and any(c['root']==rid for c in selectors(local_delta(buy)[1])):
                            return 'dispute','scope_missing'
    for r in committing:
        if not role_ids(inv,oid,r):continue
        from .scope_relevance import nonfinancial
        effects=[(w,*local_delta(w)) for w in r['ordered_writes']
                 if holder(w['path'],lk) is not None and not nonfinancial(inv.backend,oid,w['path'])]

        guards=[g for t in r['guards'] for g in conjuncts(t)]
        for w,sign,amount in effects:
            if effect_locations is not None and tuple(w['source'].get(k) for k in ('file','start','length')) not in effect_locations:continue
            if sign not in ('+','-') or not amount:continue
            ac=holder(w['path'],lk);others=[(ow,os,oq) for ow,os,oq in effects if ow['path']['root']==w['path']['root'] and os!=sign]
            if quantity_forced_zero(guards,amount,lk):continue
            matched=[ow for ow,os,oq in others if key(oq)==key(amount)]
            reason='scope_missing' if unit_origin(inv.backend,oid,w['path']) else 'source_unit_missing'
            if cat=='FCR-MINT' and sign=='+' and not matched:return 'dispute',reason
            if cat=='FCR-TRANSFER' and sign=='-' and matched and ac.get('kind')!='actual_sender':
                return 'dispute',reason
            if cat=='FCR-DESTROY' and sign=='-' and ac.get('kind')!='actual_sender' and not matched:
                return 'dispute',reason
    return 'reviewed','source_task_reading'


def obligation_scope(inv, assessments, blocked):
    """Record actual source readings, independent of optional proof completion."""
    categories = tuple(CATEGORIES[1:]) if inv.f.options.scope == 'FCR' else ('AC',)
    manifest=inv.initial_manifest or {}
    delivered=set(manifest.get('expanded_operations',()))-set(manifest.get('partially_expanded_operations',()))
    by_entry={}
    local={}
    gaps=[]
    normal=[]
    agenda=[]
    scope_skips=set()
    seen_gaps=set()
    open_cats=set()
    def gap(oid, cats, reason, issues=()):
        affected=sorted(set(cats)&set(categories))
        if not affected:return
        token=(oid,tuple(affected),reason)
        if token in seen_gaps:return
        seen_gaps.add(token);open_cats.update(affected)
        obj=inv.f.operations.get(oid,{})
        gaps.append(dict(id='gap_'+digest(token)[:16],target=obj.get('target'),operations=[oid] if oid else [],
                         location=obj.get('source',{}),closed=False,affected_categories=affected,
                         reason=reason,issues=list(issues),explanation=describe(affected[0],reason)))
    for qid,q in inv.issues.items():
        a=assessments[qid];cat=a.get('category')
        status=a['scope'].get('route_status')
        decision=a['scope']['decision']
        root=inv.root(q)
        if status=='superseded':continue
        record={'issue':qid,'category':cat,'state':decision['status'],'reason':decision['reason'],
                'closed':decision['status'] in ('risk','normal','excluded'),'entries':[root] if root else [],
                'affected_categories':[]}
        record['effects']=decision.get('effects',[]) or sorted(inv.semantics.rules.route_scopes(q))
        local[qid]=record
        if root:by_entry.setdefault(root,[]).append(record)
        if root is None and q['current'].get('assessment')=='risk':
            for candidate in q.get('binding',{}).get('operations',()):
                gap(candidate,category_scope(q['current'],inv.f.options.scope),'core_mismatch',[qid])
    checked=0;obligations=[]; basic_cache=inv.__dict__.setdefault('_basic_entry_opinions',{})
    rules=inv.semantics.rules
    expanded_all=manifest.get('mode')=='complete_source'
    for oid,entry in inv.f.operations.items():
        cats=set(categories)
        states={};related=by_entry.get(oid,[])
        local_counts=[x for x in related if x['reason']=='scoped_counter' and x['state']=='normal']
        rows=inv.f.summaries.rows(oid,False)
        # A generated getter is still a compiler declaration. Inspect real rows or that declaration.
        read=bool(rows or entry['generated_getter']) and oid not in rules.incomplete
        if read:checked+=1
        cache=inv.__dict__.setdefault('_scope_candidates',{})
        if categories!=('AC',):
            if oid not in cache and inv.program_remaining()<=0:
                gap(oid,categories,'not_reviewed');continue
            stamp=(inv.semantics.dependency_identity([oid]),digest(inv.semantics.active_scope))
            if cache.get(oid,(None,))[0]!=stamp:
                cache[oid]=(stamp,set(possible_properties(inv,{oid})))
            cats=cache[oid][1]
        explicit=set(x['category'] for x in related if x['category'] in categories)
        if any(x['reason'] in ('conflicting_scoped_meanings','source_unit_missing') and not x['category'] for x in related):
            for x in related:
                if x['reason'] in ('conflicting_scoped_meanings','source_unit_missing'):
                    rules=inv.semantics.rules;q=inv.issues[x['issue']]
                    for e in (rules.disputed_effects(q) if x['reason']=='conflicting_scoped_meanings' else rules.route_scopes(q)):
                        w=inv.semantics.rules.effects[e].get('write')
                        if w is None:continue
                        sign,_=local_delta(w)
                        explicit.update(['FCR-MINT'] if sign=='+' else ['FCR-DESTROY','FCR-TRANSFER'] if sign=='-' else [])
                        gap(oid,['FCR-MINT'] if sign=='+' else ['FCR-DESTROY','FCR-TRANSFER'] if sign=='-' else [],x['reason'],[x['issue']])
        relevant=cats|explicit
        committed=[r for r in rows if r['committing']]
        opaque=any(r['residuals'] or r['flow']=='truncated' or any(e.get('kind')=='dangerous_external_call' for e in r['effects']) for r in rows) or bool(entry['gaps'])
        no_effect=read and not opaque and (entry['generated_getter'] or not any(r['ordered_writes'] or r['effects'] for r in committed))
        unresolved_key_only=bool(rows) and not entry['gaps'] and not any(r['effects'] or r['flow']=='truncated' for r in rows) and all(
            x.get('reason')=='multiple_address_keys_need_source_holder_binding' for r in rows for x in r['residuals'])
        if opaque and not relevant and not unresolved_key_only:relevant=set(categories)
        has_view=expanded_all or oid in delivered
        for cat in sorted(categories):
            records=[x for x in related if x['category']==cat]
            active=[x for x in records if not inv.issues[x['issue']]['current'].get('_host_source_question') or
                    x['reason'] in ('conflicting_scoped_meanings','source_unit_missing','policy_scope_unsubstantiated','policy_effect_unresolved') or
                    inv.issues[x['issue']]['current'].get('_semantic_consumer') and x['reason'] in ('policy_missing','external_dependency')]
            settled=[x for x in records if x['state'] in ('normal','excluded','risk')]
            covered={e for x in settled for e in x['effects']}
            outstanding=inv.semantics.rules.by_operation.get(oid,set())-covered
            decisive=[]
            for rec in active:
                if rec['state']!='open':continue
                model_issue=inv.issues[rec['issue']]
                prop=model_issue.get('property') or {}
                finance_q=any(s.get('kind')=='financial_consent' and s.get('quantity_scope') for s in prop.get('semantic_questions',[]))
                measured_unbound=any(
                    e.get('property_identity')==prop.get('id') and any(x.get('reason')=='holder_authorization_quantity_basis_unresolved' for x in e.get('local_errors',[]))
                    for label in model_issue['evidence'] for e in [inv.evidence[label]])
                consent_active=any(x.get('meaning')=='net_request_with_fee' and x.get('quantity_scope') for x in prop.get('consent_rows',[]))
                if cat in ('FCR-DESTROY','FCR-TRANSFER') and (finance_q or measured_unbound or consent_active) and rec['reason']=='scope_missing':
                    decisive.append(dict(rec,reason='holder_consent_basis_unresolved'));continue
                if rec['reason'] not in (
                    'conflicting_scoped_meanings','source_unit_missing','policy_effect_unresolved','external_dependency',
                    'policy_missing','policy_scope_unsubstantiated','revised_policy_not_read'):continue
                if not rec['effects'] or not set(rec['effects'])<=covered:decisive.append(rec)
            base_status,base_reason='unread','not_reviewed'
            read_effects=set(rules.by_operation.get(oid,()))
            local_complete=not outstanding and bool(covered) and not opaque
            # basic_entry reasons about the actual writes and program guards. It does
            # not consume a mutable normative consent, which is applied separately below.
            from .source_opinion import reading_version
            depend=reading_version(inv,[oid],cat) if (oid,cat) in inv.__dict__.get('_coverage_control_routes',{}) else None
            basic_key=(oid,cat,tuple(sorted(outstanding)),stamp if categories!=('AC',) else None,depend)
            from .scope_relevance import detached_holder_switch
            detached=(cat=='FCR-FREEZE' and read and detached_holder_switch(inv,oid))
            if detached:
                base_status,base_reason='reviewed','detached_local_holder_switch'
            elif read and no_effect:
                base_status,base_reason='reviewed','no_effect_in_scope'
            elif read and cat=='FCR-MINT' and not opaque and any(n.get('kind')=='transaction_value' for r in committed for w in r['ordered_writes'] for n in walk(w['value'])) and basic_entry(inv,oid,rows,cat)==('reviewed','ordinary_paid_credit'):
                base_status,base_reason='reviewed','ordinary_paid_credit'
            elif read and cat not in relevant and not (opaque and not relevant):
                base_status,base_reason='reviewed','necessary_effect_absent'
            elif read and local_complete:
                base_status,base_reason='reviewed','effect_range_decided'
            elif not has_view and not local_complete:
                base_reason='source_context_missing'
            elif opaque and not (unresolved_key_only and (cat not in cats or simple_holder_grant(inv,oid,rows))):
                base_reason='external_dependency'
            elif read and (basic_key in basic_cache or inv.program_remaining()>0):
                if basic_key not in basic_cache:
                    # Keep companion writes and guards as dependencies of the remaining effect.
                    locs=None
                    if covered and outstanding:
                        locs={tuple(rules.effects[e]['where'].get(k) for k in ('file','start','length')) for e in outstanding}
                    basic_cache[basic_key]=basic_entry(inv,oid,rows,cat,locs)
                base_status,base_reason=basic_cache[basic_key]
            elif not read:base_reason='source_context_missing'
            reason=base_reason if base_status!='reviewed' else None
            if decisive and not detached and not no_effect and (cat in relevant) and base_reason!='nominee_acceptance':
                reason=decisive[0]['reason']
            if reason:
                gap(oid,[cat],reason,[x['issue'] for x in decisive])
                effects={e for record in decisive for e in record['effects']} or outstanding
                states[cat]={'state':'open','basis':reason,'effect_ids':sorted(effects)}
            else:
                states[cat]={'state':'reviewed','basis':base_reason}
            identity=(oid,cat,tuple(sorted(outstanding)))
            if reason in ('scope_missing','source_unit_missing','policy_missing','unassessed_role_change') and not opaque and identity not in scope_skips:
                agenda.append({'operation':oid,'category':cat,'effects':sorted(outstanding),'dependency':reason})
                scope_skips.add(identity)
        affected=[c for c in categories if states[c]['state']=='open']
        obligations.append({'id':'obligation_'+digest([inv.f.identity,entry['target'],oid])[:20],
            'target':entry['target'],'operations':[oid],'location':entry['source'],'possible_categories':sorted(relevant),'source_candidate_categories':sorted(cats),'bound_question_categories':sorted(explicit),'category_states':states,
            'closed':not affected,'affected_categories':affected,'entry_states':[{'operation':oid,'states':{c:states[c]['state'] for c in categories}}]})
    if not checked:gap(None,categories,'not_reviewed')
    eligible=sorted(set(categories)-open_cats)
    for cat in eligible:
        if not any(x['category']==cat and x['state']=='risk' for x in local.values()):
            matched=[r for r in local.values() if r['category']==cat and r['state'] in ('normal','excluded')]
            reasons=sorted({r['reason'] for r in matched})
            patterns=sorted({s['category_states'][cat]['basis'] for s in obligations if cat in s['category_states'] and s['category_states'][cat].get('basis')})
            explanation=describe(cat,reasons[0] if reasons else patterns[0] if len(patterns)==1 else 'source_task_reading')
            normal.append({'category':cat,'reason':'source_task_reading','applied_reasons':reasons or patterns,
                           'effects':sorted({e for r in matched for e in r['effects']}),'explanation':explanation})
    return {'schema':'source-category-decision-r1','request_scope':manifest.get('requested_reading'),
            'whole_reading_eligible':bool(checked and not open_cats),
            'negative_eligible_categories':eligible,'known_category_gaps':gaps,'category_readings':normal,
            'source_local_scopes':local,'obligations':obligations,'neutral_scope_scan_executed':bool(checked),
            'basic_source_entries_read':checked,'source_opinion_available':bool(checked),'refinement_requests':agenda,
            'delivery_and_model_declaration_are_not_completion':True}
