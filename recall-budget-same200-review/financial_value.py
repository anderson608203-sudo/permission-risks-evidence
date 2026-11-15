"""Source-bound value intervention and the same holder request in two worlds.

Quantity facts are not consent policies. Every financial capability retains
its own holder, ledger, request, privilege and normal-explanation conditions.
"""
from itertools import product
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import selectors, keys, selector_relation
from pr_next_joint.verification.program_encoding import MechanismEncoder
from pr_next_joint.verification.sequence import qualify, read
from pr_next_joint.verification.source_worlds import encode_frame
from pr_next_joint.verification.expressions import Unsupported
from .ledger import movements, flow, unit_origin, grant_for, native_only_position
from .roles import path_qualification, fixed_role_terms


def family_delta(e, lookup, fr, positions, family):
    """Sum final net changes once per *runtime* position, including aliases."""
    z=e.z;seen=[];parts=[]
    for cell in positions:
        if selector_relation(cell,family)!='same_shape':continue
        probe=qualify(cell,fr['slot'])
        ks=[e.expr(read(k,fr['before'],lookup)) for k in keys(probe)]
        duplicate=z.Or(*[z.And(*[a==b for a,b in zip(ks,prior)]) for prior in seen])
        before=e.expr(read(probe,fr['before'],lookup))
        after=e.expr(read(probe,fr['before']+fr['writes'],lookup))
        parts.append(z.If(duplicate,0,after-before));seen.append(ks)
    return z.Sum(*parts) if parts else z.IntVal(0)


def consent(b,e,oid,path,fr,cell,holder,net_debit,interpretation=None):
    """Sufficient scoped consent and the residual when an amount basis differs.

    Self requests and an exclusively holder-issued bound covering final debit
    can refute an unauthorized-loss claim. An under-covered numeric guard is
    not automatically a normative requirement for gross authorization.
    """
    z=e.z;lookup=b.f.lookup(oid);caller=e.expr(fr['caller'])
    grant=grant_for(b,oid,path,cell)
    allowed=[holder==caller];basis={'self_request_checked':True,'grant':grant}
    if grant is None:
        # Boolean delegation is meaningful only if every non-revocation
        # writer addresses the actual issuer's own ordered holder key.
        from .summary import holder as source_holder
        who=source_holder(cell,lookup)
        def conjuncts(g):
            return [x for a in g['args'] for x in conjuncts(a)] if g.get('op') in ('and','&&') else [g]
        for raw in path['guards']:
            for g in conjuncts(raw):
                if g.get('kind')!='storage' or len(keys(g))!=2:continue
                indices=keys(g);matches=[i for i,k in enumerate(indices) if key(k)==key(who)]
                if len(matches)!=1 or indices[1-matches[0]].get('kind')!='actual_sender':continue
                h=matches[0]
                writers=[w for w in b.f.writes.values() if b.f.operations[w['operation']]['target']==b.f.operations[oid]['target']
                         and selector_relation(w['raw']['path'],g)=='same_shape']
                if writers and all(len(keys(w['raw']['path']))==2 and
                    (keys(w['raw']['path'])[h].get('kind')=='actual_sender' or
                     w['raw']['value'].get('kind')=='literal' and str(w['raw']['value'].get('value')).lower() in ('false','0')) for w in writers):
                    allowed.append(e.expr(read(qualify(g,fr['slot']),fr['before'],lookup)))
                    basis.setdefault('boolean_holder_delegations',[]).append(g)
        return z.Or(*allowed),True,basis
    from .summary import holder as source_holder
    who=source_holder(cell,lookup)
    indices=[i for i,k in enumerate(keys(grant)) if key(k)==key(who)]
    if len(indices)!=1:
        return z.Or(*allowed),False,dict(basis,reason='grant_issuer_key_not_uniquely_source_bound')
    # Direct program consumers already supply the unique path-bound grant. A wire
    # interpretation additionally has to match its explicit issued quantity scope.
    if interpretation and 'quantity_scope' in interpretation and not any(key(route['grant'])==key(grant) and route['issuer_key']==indices[0] and
                                  route['spender_key']==1-indices[0] for route in interpretation.get('quantity_scope',())):
        interpretation=None
    h=indices[0]
    writers=[w for w in b.f.writes.values() if b.f.operations[w['operation']]['target']==b.f.operations[oid]['target']
             and selector_relation(w['raw']['path'],grant)=='same_shape']
    foreign=[]
    for w in writers:
        dst,val=w['raw']['path'],w['raw']['value'];args=val.get('args',[])
        holder_issued=len(keys(dst))==2 and keys(dst)[h].get('kind')=='actual_sender'
        reduction=val.get('op')=='-' and args and key(args[0])==key(dst)
        if not holder_issued and not reduction:foreign.append(w['operation'])
    effective=e.expr(read(qualify(grant,fr['slot']),fr['before'],lookup))
    basis.update(holder_key=h,foreign_writers=sorted(set(foreign)),
        amount_rule='cover the final same-holder debit, including same-path refunds',
        normative_gross_rule_inferred=False)
    if foreign:
        # An installable allowance cannot certify actual holder issuance.
        # Its provenance is a separate obligation, not an invented consent.
        return z.Or(*allowed),False,dict(basis,reason='grant_provenance_has_nonholder_writers')
    allowed.append(effective>=net_debit)
    meaning=(interpretation or {}).get('meaning')
    if meaning=='net_request_with_fee':
        # This H interpretation is scoped to the source-bound grant/use and
        # keeps the actual checked gate and fee computation in the execution.
        # A default/used-up zero slot is not evidence that this holder issued
        # an active fee-bearing authorization. A net-amount interpretation
        # alone cannot turn it into unconditional consent for a positive
        # gross debit. Retain that provenance gap; do not infer a new gross
        # policy or automatically classify the gap as a financial violation.
        allowed.append(effective>0)
    basis.update(interpretation=interpretation,quantity_basis_resolved=meaning in ('gross_debit_bound','net_request_with_fee'),
        positive_active_grant_required_for_net_fee_consent=meaning=='net_request_with_fee',
        zero_grant_is_not_holder_issuance=meaning=='net_request_with_fee')
    return z.Or(*allowed),meaning=='gross_debit_bound',basis


def interpretation_for(prop,use,pid,cell):
    rows=[c for c in prop.get('consent_rows',()) if c.get('operation')==use and any(s['path']==pid and key(s['ledger'])==key(cell) for s in c.get('quantity_scope',()))]
    if rows and len({c['meaning'] for c in rows})!=1:return None
    row=rows[0] if rows else prop.get('financial_consents',{}).get(use) or prop.get('financial_consent')
    if row and any(s['path']==pid and key(s['ledger'])==key(cell)
                   for s in row.get('quantity_scope',[])):return row
    return None


def proved_exclusion(query):
    return query['answer']=='unsat' and (query.get('exclusion_certificate',{}).get('excludes_only_this_formula') or
        query['details'].get('prestate',{}).get('global_reachability_exhausted'))


def causal_credits(b,oid,path,cell):
    """Same-ledger receivers tied to the debit's source quantity expression."""
    from .summary import local_delta
    debits=[local_delta(w)[1] for w in path['writes'] if key(w['path'])==key(cell) and local_delta(w)[0]=='-']
    result=[]
    for candidate in movements(b,oid,path)['+']:
        if selector_relation(candidate,cell)!='same_shape' or key(candidate)==key(cell):continue
        amounts=[local_delta(w)[1] for w in path['writes'] if key(w['path'])==key(candidate) and local_delta(w)[0]=='+']
        if any(key(a)==key(part) for a in debits for amount in amounts for part in walk(amount)):
            result.append(candidate)
    return result


def payment_part(amount,whole):
    if not isinstance(amount,dict) or not isinstance(whole,dict):return False
    if key(amount)==key(whole):return True
    args=amount.get('args',[])
    if len(args)!=2:return False
    if amount.get('op')=='-':return payment_part(args[0],whole)
    if amount.get('op')=='/' and args[1].get('kind')=='literal' and isinstance(args[1].get('value'),int) and args[1]['value']>0:
        return payment_part(args[0],whole) or (args[0].get('op')=='*' and any(key(v)==key(whole) for v in args[0].get('args',[])))
    return False

def distributed_value(b,e,oid,path,fr,cell,holder,*,all_transfers):
    """Final same-unit distributions. The holder's own credits are already in flow().
    Count all causally paired recipients for a movement check. For destruction,
    allocate only the portion backed by a real transfer of these units; unrelated
    credits, e.g. independent issuance in the same entry, never offset a debit.
    """
    z=e.z;lookup=b.f.lookup(oid);seen=[];parts=[]
    from .summary import local_delta
    related=causal_credits(b,oid,path,cell)
    debits=[local_delta(w)[1] for w in path['writes'] if key(w['path'])==key(cell) and local_delta(w)[0]=='-']
    for c in related:
        if not all_transfers:
            credits=[local_delta(w)[1] for w in path['writes'] if key(w['path'])==key(c) and local_delta(w)[0]=='+']
            # Amount provenance must be a payment or a portion of the debit.
            # Merely mentioning the amount (e.g. minting a multiple) is not allocation.
            if not credits or not all(any(payment_part(amount,whole) for whole in debits) for amount in credits):continue
        h,start,end,_,_=flow(e,lookup,fr,c)
        probe=qualify(c,fr['slot'])
        ks=[e.expr(read(k,fr['before'],lookup)) for k in keys(probe)]
        duplicate=z.Or(*[z.And(*[a==v for a,v in zip(ks,prior)]) for prior in seen])
        real_credit=z.And(h!=holder,h!=0,z.Not(duplicate),end>start)
        if not all_transfers:
            # A credit larger than the entire causally debited quantity may be independent
            # issuance. Count it as payment only in a state where the allocation fits.
            if any(key(amount)!=key(whole) for amount in credits for whole in debits) and not all(
                    amount.get('op')=='-' and any(key(amount['args'][0])==key(whole) for whole in debits)
                    for amount in credits):
                available=sum((e.expr(read(qualify(amount,fr['slot']),fr['before'],lookup)) for amount in debits),z.IntVal(0))
                real_credit=z.And(real_credit,end-start<=available)
        parts.append(z.If(real_credit,end-start,0));seen.append(ks)
    return z.Sum(*parts) if parts else z.IntVal(0)


def native_settlement(b,e,oid,fr,cell,holder):
    """Only exact native-unit provenance can bind a native payment to a debit.

    A token name, a coincident payment or another asset never supplies an
    exchange rate. Success and recipient conditions are those of this same
    committed source frame. A partial payment offsets only its actual amount.
    """
    z=e.z;origin=b._native_unit_source(oid,cell)
    payments=[fx for fx in fr['effects'] if fx.get('kind')=='native_transfer']
    basis={'unit_source':origin,'same_frame_payments':payments,
           'same_holder_required':True,'cross_asset_rate_assumed':False}
    if not origin or not payments:return z.IntVal(0),basis
    from pr_next_joint.frontend.path_ir import lit
    paid=z.Sum(*[z.If(z.And(e.expr(fx['recipient'])==holder,e.expr(fx.get('success',lit(True)))),e.expr(fx['amount']),0) for fx in payments])
    return paid,basis


def post_exclusion(b,change,use,cid,cp,pid,path,cell,prop):
    """Check a necessary harmful effect without assuming W0 could commit.

    Only UNSAT can close this route. SAT here is not a causal intervention
    finding. This prevents an infeasible baseline from becoming 'no risk'.
    """
    def calculate():
        from .behavior import ordered_clocks
        e=MechanismEncoder(b.f.lookup(use));z=e.z;lookup=e.lookup
        cf=b.source_frame(change,cid,0);uf=b.source_frame(use,pid,1,cf['writes'])
        qualification=path_qualification(b.f,change,cp)
        roles,origins=fixed_role_terms(e,qualification,0)
        h,start,end,_,_=flow(e,lookup,uf,cell);actor=e.expr(cf['caller']);requester=e.expr(uf['caller'])
        net=start-end;cat=prop['category']
        permitted,resolved,basis=consent(b,e,use,path,uf,cell,h,net,interpretation_for(prop,use,pid,cell))
        if cat=='FCR-MINT':
            from .relations import beneficiary_condition
            controlled,why=beneficiary_condition(e,uf,cell,h,controller_frame=cf)
            no_debit=[flow(e,lookup,uf,c)[2]>=flow(e,lookup,uf,c)[1] for c in movements(b,use,path)['-']
                      if selector_relation(c,cell)=='same_shape']
            harmful=z.And(end>start,controlled,*no_debit)
        else:
            credited=distributed_value(b,e,use,path,uf,cell,h,all_transfers=cat=='FCR-TRANSFER')
            paid,settlement=native_settlement(b,e,use,uf,cell,h)
            harmful=z.And(net>0,h!=actor,z.Not(permitted),credited>0 if cat=='FCR-TRANSFER' else net>credited+paid)
        detail={'operation':change,'change':change,'observe':use,'target':prop['target'],
            'change_path':cid,'use_path':pid,'ledger':cell,'category_hypothesis':cat,
            'property_identity':prop['id'],'semantic_version':prop['semantic_version'],
            'property_validated':True,'proof_use':'UNSAT necessary post-effect exclusion only',
            'baseline_success_not_assumed':True,'holder_consent':basis,'role_origins':origins}
        q=b._query(e,z.And(encode_frame(e,cf),encode_frame(e,uf),*roles,*ordered_clocks(e,1),
                          actor!=0,requester!=0,h!=0,harmful),'financial_value_post_exclusion',detail)
        return {'queries':[q],'local_errors':[]}
    result=b.memo('value_post_exclusion',[change,use,cid,pid,cell,prop],calculate)
    return result['queries'][0]


def enabled_effect(b,change,use,cid,cp,pid,path,cell,prop):
    """A privileged change newly permits a harmful *same* request.

    A value property must not require the unauthorized request to commit
    before its enabling change. All baseline source branches are considered;
    an unmodeled branch overapproximates possible baseline harm and therefore
    cannot certify that the capability is new. This is separate from the
    increased-loss comparison between two already committing requests.
    """
    def calculate():
        from .local_properties import safe_path
        from .behavior import ordered_clocks
        from .relations import beneficiary_condition
        f=b.f;lookup=f.lookup(use);e=MechanismEncoder(lookup);z=e.z
        cf=b.source_frame(change,cid,0);after=b.source_frame(use,pid,1,cf['writes'])
        controller=e.expr(cf['caller']);requester=e.expr(after['caller'])
        h,start,end,gross,_=flow(e,lookup,after,cell)
        roles,origins=fixed_role_terms(e,path_qualification(f,change,cp),0)
        cat=prop['category'];gaps=[];coverage=[]
        def harmful(p,fr):
            holder,old,new,_,_=flow(e,lookup,fr,cell);net=old-new
            permitted,resolved,basis=consent(b,e,use,p,fr,cell,holder,net,interpretation_for(prop,use,fr['path'],cell))
            if cat=='FCR-MINT':
                controlled,why=beneficiary_condition(e,fr,cell,holder,controller_frame=cf)
                no_debit=[flow(e,lookup,fr,c)[2]>=flow(e,lookup,fr,c)[1] for c in movements(b,use,p)['-']
                          if selector_relation(c,cell)=='same_shape']
                condition=z.And(new>old,controlled,*no_debit)
            else:
                credit=distributed_value(b,e,use,p,fr,cell,holder,all_transfers=cat=='FCR-TRANSFER')
                paid,_=native_settlement(b,e,use,fr,cell,holder)
                condition=z.And(net>0,holder!=controller,z.Not(permitted),
                    credit>0 if cat=='FCR-TRANSFER' else net>credit+paid)
            return z.And(holder==h,condition),resolved,basis
        after_harm,resolved,basis=harmful(path,after)
        baseline=[]
        for before_id,raw in f.operation_paths(use):
            if raw['flow']=='reverted':continue
            snapshot=e.checkpoint();mark=len(e.constraints)
            try:
                before_path=b.source_path(use,before_id,raw)
                if before_path['flow'] not in ('normal','returned') or not safe_path(b,use,before_id,before_path):
                    raise Unsupported('baseline_value_route_unresolved')
                fr=b.source_frame(use,before_id,1)
                commit=encode_frame(e,fr);bad,_,_=harmful(before_path,fr)
                checks=e.constraints[mark:];del e.constraints[mark:]
                baseline.append(z.And(commit,bad,*checks))
                coverage.append({'path':before_id,'state':'original_same_request_branch_encoded'})
            except Unsupported as error:
                e.rollback(snapshot);baseline.append(z.BoolVal(True))
                gaps.append({'path':before_id,'reason':str(error),'projection':'may already allow harm; never assumed harmless'})
        if not b.complete(use):
            baseline.append(z.BoolVal(True));gaps.append({'reason':'incomplete_baseline_source_routes'})
        base=z.And(encode_frame(e,cf),encode_frame(e,after),*roles,*ordered_clocks(e,1),
                   controller!=0,requester!=0,h!=0,after_harm,z.Not(z.Or(*baseline)))
        detail={'operation':change,'change':change,'observe':use,'target':prop['target'],
            'change_path':cid,'use_path':pid,'ledger':cell,'category_hypothesis':cat,
            'property_identity':prop['id'],'semantic_version':prop['semantic_version'],
            'property_validated':resolved or cat=='FCR-MINT','holder_consent':basis,'role_origins':origins,
            'causal_condition':'actual intervention enables harmful same request absent on every modeled baseline route',
            'beneficiary_rule':'controlled_or_self_only' if cat=='FCR-MINT' else None,'baseline_commit_not_assumed':True,'baseline_branch_coverage':coverage,'baseline_residuals':gaps,
            'same_request':'same caller, arguments, holder, asset and environment in both worlds',
            'conditional_call_summary':after.get('source_call_subcases',[])}
        label='financial_value' if resolved or cat=='FCR-MINT' else 'financial_consent_unresolved'
        q=b._query(e,base,label,detail)
        return {'queries':[q],'local_errors':gaps}
    return b.memo('value_enabled_effect',[change,use,cid,pid,cell,prop],calculate)


def compare_intermediate(b,change,use,prop):
    """Carry the same settled transition into both readings of the holder request.

    Only describes supported scoped differences. An incomplete intermediate
    search cannot exclude every effect of a setter.
    """
    from .local_properties import safe_path
    from .behavior import ordered_clocks
    from .relations import beneficiary_condition
    f=b.f; lookup=f.lookup(use); cat=prop['category']
    bridges=f.summaries.dependencies.quantity_bridges(change,use)
    queries=[];gaps=[]; examined=0
    def result(positive=False):
        return {'kind':'causal_compare','observed_measure':'financial_value','change':change,'observe':use,
                'property_identity':prop['id'],'queries':queries,'local_errors':gaps,'property_measurements':[],
                'property_excluded':False,'value_route_checked':bool(queries),'positive_route_sufficient':positive,
                'intermediate_source_checked':bool(queries),'normal_explanations':[]}
    for mid,mpid,cells in bridges:
        middle=f.paths[mpid]['raw']
        for cid,cp in b.paths(change):
            role=path_qualification(f,change,cp)
            if not role:continue
            for pid,p in b.paths(use):
                if b.remaining()<=0 or examined>=f.options.max_prefixes:
                    gaps.append({'reason':'bounded_value_transition_frontier'});return result()
                examined+=1
                if not all(safe_path(b,o,i,path) for o,i,path in [(change,cid,cp),(mid,mpid,middle),(use,pid,p)]):
                    gaps.append({'reason':'relevant_intermediate_semantics_missing'});continue
                try:
                    e=MechanismEncoder(lookup);z=e.z
                    cf=b.source_frame(change,cid,0)
                    before_mid=b.source_frame(mid,mpid,1);after_mid=b.source_frame(mid,mpid,1,cf['writes'])
                    base_writes=before_mid['writes']; post_writes=cf['writes']+after_mid['writes']
                    before=b.source_frame(use,pid,2,base_writes);after=b.source_frame(use,pid,2,post_writes)
                    roles,_=fixed_role_terms(e,role,0)
                    base=z.And(*(encode_frame(e,fr) for fr in (cf,before_mid,after_mid,before,after)),*roles,*ordered_clocks(e,2),
                               *(e.expr(fr['caller'])!=0 for fr in (cf,before_mid,before)))
                    positions=movements(b,use,p);all_cells=positions['+']+positions['-']
                    for cell in positions['+' if cat=='FCR-MINT' else '-']:
                        if not unit_origin(b,use,cell) or native_only_position(b,use,cell):continue
                        h0,start0,end0,_,_=flow(e,lookup,before,cell);h1,start1,end1,_,_=flow(e,lookup,after,cell)
                        controller=e.expr(cf['caller'])
                        matched=[other for other in all_cells if selector_relation(other,cell)=='same_shape']
                        if cat=='FCR-MINT':
                            beneficiary,_=beneficiary_condition(e,after,cell,h1,controller_frame=cf)
                            new=family_delta(e,lookup,after,matched,cell);old=family_delta(e,lookup,before,matched,cell)
                            condition=z.And(end1>start1,end1-start1>end0-start0,new>0,new>old,beneficiary)
                            resolved=True
                        else:
                            net1=start1-end1;net0=start0-end0
                            permitted,resolved,_=consent(b,e,use,p,after,cell,h1,net1,interpretation_for(prop,use,pid,cell))
                            c1=distributed_value(b,e,use,p,after,cell,h1,all_transfers=cat=='FCR-TRANSFER');c0=distributed_value(b,e,use,p,before,cell,h0,all_transfers=cat=='FCR-TRANSFER')
                            if cat=='FCR-TRANSFER':effect=z.And(c1>0,z.Or(net1>net0,c1>c0))
                            else:
                                paid1,_=native_settlement(b,e,use,after,cell,h1);paid0,_=native_settlement(b,e,use,before,cell,h0)
                                effect=z.And(net1-c1-paid1>0,net1-c1-paid1>net0-c0-paid0)
                            condition=z.And(net1>0,h1!=controller,z.Not(permitted),effect)
                        detail={'operation':change,'change':change,'observe':use,'use_path':pid,'property_identity':prop['id'],
                                'category_hypothesis':cat,'property_validated':True,'same_request':True,
                                'intermediate_value_carried':True,'ledger':cell}
                        b.check()
                        check=b._query(e,z.And(base,h1==h0,h1!=0,condition),'financial_value' if resolved else 'financial_consent_unresolved',detail)
                        queries.append(check)
                        if resolved and check['bounded_condition_confirmed']:return result(True)
                except Unsupported:
                    gaps.append({'reason':'intermediate_value_encoding_unsupported'})
    if not queries:gaps.append({'reason':'value_dependency_requires_intermediate_source_transition'})
    return result()


def compare(b,change,use,context):
    from .local_properties import safe_path
    from .behavior import ordered_clocks
    f=b.f;prop=context['compiled_property'];cat=prop['category'];lookup=f.lookup(use)
    if f.operations[change]['target']!=f.operations[use]['target']:
        raise Unsupported('value_intervention_target_mismatch')
    queries=[];rows=[];gaps=[];normal=[];checked=0;truncated=False
    b.active_property_objects={c['root'] for c in prop.get('objects',[])}
    b.active_property_roots=set(b.active_property_objects)
    controls={key(w['path']):w['path'] for _,p in b.paths(change) for w in p['writes']}
    read_cells={key(c):c for _,p in b.paths(use) for c in selectors([p['guards'],p['writes'],p.get('sensitive_effects',[])])}
    linked=[c for c in read_cells.values() if any(selector_relation(c,w)=='same_shape' for w in controls.values())]
    b.active_property_roots.update(c['root'] for c in linked)
    if not linked:
        return compare_intermediate(b,change,use,prop)
    use_paths=list(b.paths(use));change_paths=list(b.paths(change))
    from .summary import local_delta
    jobs=[]
    wanted='+' if cat=='FCR-MINT' else '-'
    # Enumerate only the bounded work actually admitted to this source route.
    # The full path Cartesian product is not materialized before budgeting.
    roles={cid:path_qualification(f,change,cp) for cid,cp in change_paths}
    positions={}
    for p1,after in use_paths:
        positions[p1]=[]
        for cell in movements(b,use,after)[wanted]:
            signs={local_delta(w)[0] for w in after['writes'] if key(w['path'])==key(cell)}
            if signs and None not in signs and wanted not in signs:continue
            unit=unit_origin(b,use,cell)
            if unit and not native_only_position(b,use,cell):positions[p1].append((cell,unit))
            elif not unit:
                semantic=b.semantics.lookup(use,cell) if getattr(b,'semantics',None) else None
                if not semantic or semantic.get('meaning')!='nonfinancial_counter':
                    gaps.append({'path':p1,'position':cell,'reason':'value_position_unit_not_source_bound'})
    total_jobs=sum(bool(r) for r in roles.values())*len(use_paths)*sum(map(len,positions.values()))
    # When semantic feedback rebinds an observed unknown, revisit its exact
    # after-path and ledger first. It is still solved under the new policy.
    from pr_next_joint.core import digest
    prior=getattr(b,'pending_amount_routes',{}).get((change,use,cat),set())
    matched={(pid,ledger) for pid,ledger in prior for cell,_ in positions.get(pid,())
             if digest(cell)==ledger and (interpretation_for(prop,use,pid,cell) or {}).get('meaning') in ('gross_debit_bound','net_request_with_fee')}
    def candidates():
        if matched:
            for cid,cp in sorted(change_paths):
                if not roles[cid]:continue
                for pid,path in sorted(use_paths):
                    for cell,unit in positions[pid]:
                        if (pid,digest(cell)) in matched:
                            yield cid,cp,pid,path,pid,path,cell,roles[cid],unit
        for equal in (True,False):
            for cid,cp in sorted(change_paths):
                if not roles[cid]:continue
                for p0,before in sorted(use_paths):
                    for p1,after in sorted(use_paths):
                        if (p0==p1)!=equal:continue
                        for cell,unit in positions[p1]:
                            if equal and (p1,digest(cell)) in matched:continue
                            yield cid,cp,p0,before,p1,after,cell,roles[cid],unit
    for job in candidates():
        jobs.append(job)
        if len(jobs)>f.options.max_prefixes:break
    cursor=context.get('_value_cursor',0)
    state_key=b.cache_key('financial_value_progress',[change,use,prop,context.get('bindings'),context.get('request_aliases')])
    progress=b.__dict__.setdefault('_financial_value_progress',{})
    if cursor:
        state=progress.get(state_key)
        if not state or state['cursor']!=cursor:raise Unsupported('financial_value_continuation_identity')
        queries,rows,gaps,normal=state['queries'],state['rows'],state['gaps'],state['normal']
    prior_ids={q['id'] for q in queries};prior_rows=len(rows);prior_normal=len(normal)
    def emit(result):
        # Prior slices are immutable evidence already attached to this issue.
        # Keep their identities, not repeated multi-megabyte query receipts.
        result['prior_probe_dependencies']=sorted(prior_ids)
        result['queries']=list({q['id']:q for q in result['queries'] if q['id'] not in prior_ids}.values())
        result['property_measurements']=result['property_measurements'][prior_rows:]
        result['normal_explanations']=result['normal_explanations'][prior_normal:]
        return result
    end=min(cursor+4,len(jobs),f.options.max_prefixes)
    for job_index in range(cursor,end):
            cid,cp,p0,before,p1,after,cell,role,unit=jobs[job_index]
            cells=movements(b,use,after)
            checked=job_index+1
            detail={'operation':change,'change':change,'observe':use,'target':prop['target'],
                'change_path':cid,'before_path':p0,'after_path':p1,'use_path':p1,'ledger':cell,'unit':unit,
                'category_hypothesis':cat,'property_identity':prop['id'],
                'semantic_version':prop['semantic_version'],'property_validated':True,
                'same_request':'same caller, inputs, environment, holder and source ledger in W0/W1',
                'scope':'actual privileged source intervention and committing dependent request',
                'no_universal_gross_allowance_policy':True}
            try:
                b.check()
                if not all(safe_path(b,o,pid,p) for o,pid,p in [(change,cid,cp),(use,p0,before),(use,p1,after)]):
                    raise Unsupported('relevant_value_route_dependency_unresolved')
                post=post_exclusion(b,change,use,cid,cp,p1,after,cell,prop)
                if not any(x['id']==post['id'] for x in queries):queries.append(post)
                if not proved_exclusion(post):
                    enabling=enabled_effect(b,change,use,cid,cp,p1,after,cell,prop)
                    for probe in enabling['queries']:
                        if not any(x['id']==probe['id'] for x in queries):queries.append(probe)
                        if probe['bounded_condition_confirmed']:
                            rows.append({'change_path':cid,'after_path':p1,'position':cell,'result_probe':probe['id'],
                                'state':probe['answer'],'scope':probe['details'],
                                'baseline':'all original branches checked; baseline commit not a premise'})
                            if probe['label']=='financial_value':
                                return emit(finish(b,prop,change,use,queries,rows,gaps,normal,checked,False,positive=True))
                            gaps.append({'path':p1,'position':cell,'reason':'holder_authorization_quantity_basis_unresolved',
                                'measured_probe':probe['id']})
                            result=finish(b,prop,change,use,queries,rows,gaps,normal,checked,True)
                            result['stopped_reason']='await_source_bound_consent_interpretation';return emit(result)
                if proved_exclusion(post) and any(r.get('normal_post_certificate')==post['id'] for r in rows):
                    rows.append({'change_path':cid,'before_path':p0,'after_path':p1,'position':cell,
                        'result_probe':post['id'],'state':'unsat','normal_post_certificate':post['id'],
                        'scope':detail,'reuse':'same post-effect excluded without requiring any baseline path'})
                    continue
                e=MechanismEncoder(lookup);z=e.z
                cf=b.source_frame(change,cid,0)
                w0=b.source_frame(use,p0,1)
                w1=b.source_frame(use,p1,1,cf['writes'])
                roles,origins=fixed_role_terms(e,role,0)
                h0,start0,end0,gross0,credit0=flow(e,lookup,w0,cell)
                h1,start1,end1,gross1,credit1=flow(e,lookup,w1,cell)
                controller=e.expr(cf['caller']);requester=e.expr(w1['caller'])
                base=z.And(encode_frame(e,cf),encode_frame(e,w0),encode_frame(e,w1),*roles,
                    *ordered_clocks(e,1),controller!=0,requester!=0,h0==h1,h1!=0,
                    z.Or(*[e.expr(read(qualify(c,1),[],lookup))!=e.expr(read(qualify(c,1),cf['writes'],lookup)) for c in linked]))
                for arg in context.get('bindings',[]):base=z.And(base,e.expr(qualify(arg['parameter'],1))==e.expr(arg['value']))
                for a,c,relation in context.get('request_aliases',[]):
                    aa,cc=e.expr(qualify(a,1)),e.expr(qualify(c,1));base=z.And(base,aa==cc if relation=='==' else aa!=cc)
                positions=list({key(c):c for c in cells['-']+cells['+']}.values())
                total1=family_delta(e,lookup,w1,positions,cell)
                total0=family_delta(e,lookup,w0,positions,cell)
                net0=start0-end0;net1=start1-end1
                permitted,basis_resolved,consent_basis=consent(b,e,use,after,w1,cell,h1,net1,
                    interpretation_for(prop,use,p1,cell))
                detail.update(role_provenance=role,encoded_role_origins=origins,
                    holder_consent=consent_basis,final_balance_aliases_merged=True,
                    actual_control_selectors=linked)
                values={'holder':h1,'controller':controller,'requester':requester,
                    'balance_before_request':start0,'balance_after_baseline':end0,'balance_after_intervention_request':end1,
                    'gross_debit_before':gross0,'gross_debit_after':gross1,'net_debit_before':net0,'net_debit_after':net1,
                    'family_net_before':total0,'family_net_after':total1,'holder_consent_sufficient':permitted}
                # A quantity observation is retained separately from a main
                # category decision, including fee/receipt-only changes.
                observed=z.And(base,z.Or(net1!=net0,total1!=total0))
                q=b._query(e,observed,'same_request_amount_change',dict(detail,measurement_only=True));queries.append(q)
                if cat=='FCR-MINT':
                    from .relations import beneficiary_condition
                    beneficiary,why=beneficiary_condition(e,w1,cell,h1,controller_frame=cf)
                    detail['beneficiary']=why
                    no_debit=[flow(e,lookup,w1,c)[2]>=flow(e,lookup,w1,c)[1] for c in cells['-']
                              if selector_relation(c,cell)=='same_shape']
                    violation=z.And(end1>start1,end1>end0,total1>0,total1>total0,beneficiary,*no_debit)
                else:
                    # Purely reduced receipt, with unchanged holder debit,
                    # remains an additional quantity fact under the contract.
                    violation=z.And(net1>0,h1!=controller,z.Not(permitted))
                    credited=distributed_value(b,e,use,after,w1,cell,h1,all_transfers=cat=='FCR-TRANSFER')
                    credited0=distributed_value(b,e,use,before,w0,cell,h0,all_transfers=cat=='FCR-TRANSFER')
                    if cat=='FCR-DESTROY':
                        paid1,settlement1=native_settlement(b,e,use,w1,cell,h1)
                        paid0,settlement0=native_settlement(b,e,use,w0,cell,h0)
                        loss1,loss0=net1-credited-paid1,net0-credited0-paid0
                        # Compare uncompensated loss, not just one gross
                        # balance write. Explicit fee consent still excludes
                        # the main category; an unknown norm stays open.
                        violation=z.And(violation,loss1>0,loss1>loss0)
                        detail['same_holder_settlement']={'baseline':settlement0,'intervention':settlement1}
                        values.update(uncompensated_loss_before=loss0,uncompensated_loss_after=loss1)
                    else:
                        violation=z.And(violation,credited>0,z.Or(net1>net0,credited>credited0))
                # An unresolved normative amount basis cannot license an
                # alarm. Test sufficient consent independently so a complete
                # normal source path still closes locally.
                positive_kind='financial_value' if basis_resolved or cat=='FCR-MINT' else 'financial_consent_unresolved'
                if proved_exclusion(post):tested=post
                else:
                    tested=b._query(e,z.And(base,violation),positive_kind,detail);queries.append(tested)
                row={'change_path':cid,'before_path':p0,'after_path':p1,'position':cell,
                     'result_probe':tested['id'],'state':tested['answer'],'scope':detail,
                     'quantity_probe':q['id']}
                if proved_exclusion(post):row['normal_post_certificate']=post['id']
                rows.append(row)
                if tested['answer']=='unsat':
                    normal.append({'probe':tested['id'],'reason':'same_request_no_unauthorized_additional_net_loss_or_issuance',
                                   'scope':detail,'certificate':tested.get('exclusion_certificate')})
                elif positive_kind=='financial_consent_unresolved':
                    gaps.append({'path':p1,'before_path':p0,'position':cell,
                        'reason':'holder_authorization_quantity_basis_unresolved','measured_probe':tested['id']})
                    # More arithmetic variants cannot answer this normative
                    # question. Preserve the measured route and leave time
                    # for the focused H answer and other independent roots.
                    result=finish(b,prop,change,use,queries,rows,gaps,normal,checked,True)
                    result['stopped_reason']='await_source_bound_consent_interpretation'
                    return emit(result)
                if tested['label']=='financial_value' and tested['bounded_condition_confirmed']:
                    return emit(finish(b,prop,change,use,queries,rows,gaps,normal,checked,False,positive=True))
            except Unsupported as error:
                gaps.append({'change_path':cid,'before_path':p0,'path':p1,'position':cell,'reason':str(error)})
            except TimeoutError as error:
                gaps.append({'change_path':cid,'before_path':p0,'path':p1,'reason':str(error)})
                result=finish(b,prop,change,use,queries,rows,gaps,normal,checked,True)
                result['stopped_reason']='shared_program_budget';return emit(result)
    more=end<total_jobs
    result=finish(b,prop,change,use,queries,rows,gaps,normal,end,more)
    result['route_enumeration']={'jobs':total_jobs,'covered':end,'limit':f.options.max_prefixes,
                                 'complete':not more,'source_only_order':True}
    if more and end<f.options.max_prefixes:
        progress[state_key]={'cursor':end,'queries':queries,'rows':rows,'gaps':gaps,'normal':normal}
        result['continuation']={'_value_cursor':end}
        result['stopped_reason']='branch_quantum_yield'
    else:progress.pop(state_key,None)
    return emit(result)


def finish(b,prop,change,use,queries,rows,gaps,normal,checked,truncated,positive=False):
    covered=bool(rows) and not gaps and not truncated and b.complete(change) and b.complete(use)
    post=[q for q in queries if q['label']=='financial_value_post_exclusion']
    excluded=covered and bool(post) and all(proved_exclusion(q) for q in post)
    return {'kind':'causal_compare','observed_measure':'financial_value','change':change,'observe':use,
        'property_identity':prop['id'],'queries':queries,'property_measurements':rows,'local_errors':gaps,
        'normal_explanations':normal,'property_excluded':excluded,'value_route_checked':True,
        'positive_route_sufficient':positive,'pair_budget':{'checked':checked,'truncated':truncated},
        'source_path_coverage':{'change_complete':b.complete(change),'use_complete':b.complete(use)},
        'evidence_scope':{'target':prop['target'],'request_context':'paired actual source frames',
                          'cross_asset_compensation_not_assumed':True}}
