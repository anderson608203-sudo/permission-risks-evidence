# 实跑源码文本 · 第 10 页

## file-e6333c56c66113

`source/src/pr_next_joint/investigation/financial_value.py` · 原字节 SHA-256 `6f44217c3eb44448d0835d5a7a10f51e41443a874eef43570bbdbf218b4575bb`

~~~~python
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
    row=prop.get('financial_consents',{}).get(use) or prop.get('financial_consent')
    if row and any(s['path']==pid and selector_relation(s['ledger'],cell)=='same_shape'
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


def credited_elsewhere(b,e,oid,path,fr,cell,holder):
    z=e.z;lookup=b.f.lookup(oid);seen=[];parts=[]
    for c in causal_credits(b,oid,path,cell):
        h,start,end,_,_=flow(e,lookup,fr,c)
        probe=qualify(c,fr['slot'])
        ks=[e.expr(read(k,fr['before'],lookup)) for k in keys(probe)]
        duplicate=z.Or(*[z.And(*[a==v for a,v in zip(ks,prior)]) for prior in seen])
        parts.append(z.If(z.And(h!=holder,h!=0,z.Not(duplicate),end>start),end-start,0));seen.append(ks)
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
            controlled,why=beneficiary_condition(e,dict(uf,caller=cf['caller']),cell,h)
            no_debit=[flow(e,lookup,uf,c)[2]>=flow(e,lookup,uf,c)[1] for c in movements(b,use,path)['-']
                      if selector_relation(c,cell)=='same_shape']
            harmful=z.And(end>start,controlled,*no_debit)
        else:
            credited=credited_elsewhere(b,e,use,path,uf,cell,h)
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
                controlled,why=beneficiary_condition(e,dict(fr,caller=cf['caller']),cell,holder)
                no_debit=[flow(e,lookup,fr,c)[2]>=flow(e,lookup,fr,c)[1] for c in movements(b,use,p)['-']
                          if selector_relation(c,cell)=='same_shape']
                condition=z.And(new>old,controlled,*no_debit)
            else:
                credit=credited_elsewhere(b,e,use,p,fr,cell,holder)
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
            'baseline_commit_not_assumed':True,'baseline_branch_coverage':coverage,'baseline_residuals':gaps,
            'same_request':'same caller, arguments, holder, asset and environment in both worlds',
            'conditional_call_summary':after.get('source_call_subcases',[])}
        label='financial_value' if resolved or cat=='FCR-MINT' else 'financial_consent_unresolved'
        q=b._query(e,base,label,detail)
        return {'queries':[q],'local_errors':gaps}
    return b.memo('value_enabled_effect',[change,use,cid,pid,cell,prop],calculate)


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
        return {'kind':'causal_compare','observed_measure':'financial_value','change':change,'observe':use,
            'property_identity':prop['id'],'queries':[], 'property_measurements':[],
            'local_errors':[{'reason':'value_dependency_requires_intermediate_source_transition','use':use}],
            'property_excluded':False,'value_route_checked':False}
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
    def candidates():
        for equal in (True,False):
            for cid,cp in sorted(change_paths):
                if not roles[cid]:continue
                for p0,before in sorted(use_paths):
                    for p1,after in sorted(use_paths):
                        if (p0==p1)!=equal:continue
                        for cell,unit in positions[p1]:
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
                    beneficiary,why=beneficiary_condition(e,dict(w1,caller=cf['caller']),cell,h1)
                    detail['beneficiary']=why
                    no_debit=[flow(e,lookup,w1,c)[2]>=flow(e,lookup,w1,c)[1] for c in cells['-']
                              if selector_relation(c,cell)=='same_shape']
                    violation=z.And(end1>start1,end1>end0,total1>0,total1>total0,beneficiary,*no_debit)
                else:
                    # Purely reduced receipt, with unchanged holder debit,
                    # remains an additional quantity fact under the contract.
                    violation=z.And(net1>0,h1!=controller,z.Not(permitted))
                    credited=credited_elsewhere(b,e,use,after,w1,cell,h1)
                    credited0=credited_elsewhere(b,e,use,before,w0,cell,h0)
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

~~~~

## file-0e60ca97f5ca66

`source/src/pr_next_joint/investigation/goal_search.py` · 原字节 SHA-256 `95d5689142d7329752527800490337f844a15a9d691ba2d132b16432804e2ad7`

~~~~python
"""Bounded backward prerequisites and forward checked symbolic target states.

Search results contain the actual ordered frames, not a list of writer names.
All addresses remain separate symbolic inputs unless the source/request binds
them. A finite queue ending never certifies universal unreachability.
"""
from collections import deque
import copy
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key
from pr_next_joint.frontend.storage import selectors, selector_relation
from pr_next_joint.verification.sequence import read
from .summary import unique


def prerequisites(b, operation, goal=None):
    needed = []
    for _, path in b.f.operation_paths(operation):
        needed.extend(selectors([path['guards'], path.get('evaluated_terms', []),
                                 [w['value'] for w in path['writes']]]))
    needed.extend((goal or {}).get('positions', []))
    return unique(needed)


class TargetSearch:
    def __init__(self, backend, operation, goal=None, plan=None):
        self.b, self.operation = backend, operation
        self.goal, self.plan = goal or {}, plan or {}
        self.record = {'kind': 'target_state_search', 'operation': operation,
                       'goal': self.goal, 'plan': self.plan, 'candidates_executed': [],
                       'pruned': [], 'states': [], 'frontier': [], 'exhausted_is_not_unreachable': True,
                       'depth_limit': backend.f.options.prefix_depth,
                       'candidate_limit': backend.f.options.max_prefixes}
        backend.__dict__.setdefault('target_search_records',[]).append(self.record)

    def __iter__(self):
        b, oid, f = self.b, self.operation, self.b.f
        queue, queued, states = deque([()]), {()}, set()
        target = f.operations[oid]['target']
        goal_cells = prerequisites(b, oid, self.goal)
        # The closure identifies writers of prerequisites of other writers.
        # Ordering is established only by the subsequent source frames.
        closure = list(goal_cells)
        for _ in range(f.options.prefix_depth):
            writers = b.graph.writers(target, closure, 'goal-state backwards prerequisite')
            closure = unique(closure + [c for w in writers for c in prerequisites(b, w)])
        while queue and len(self.record['candidates_executed']) < f.options.max_prefixes:
            b.check()
            sequence = queue.popleft()
            result = b.reach(oid, sequence, plan=self.plan, goal=self.goal)
            self.record['candidates_executed'].append(result)
            if result.get('stopped_reason')=='action_slice_exhausted':
                self.record['stopped_reason']='action_slice_exhausted'
                self.record['pending_prefixes']=[list(sequence)]+[list(s) for s in queue]
                self.record['frontier'].append({'prefix':list(sequence),'reason':'incomplete_source_frame_retained'})
                self.record['search_complete_within_enumerated_scope']=False
                return
            # Expand and record the queue before yielding a target state. The
            # consumer may stop after this state, and must still retain the
            # other untried preparations rather than lose the generator tail.
            if len(sequence) >= f.options.prefix_depth:
                self.record['frontier'].append({'prefix': list(sequence), 'reason': 'depth_bound'})
            else:
                head = prerequisites(b, sequence[0]) if sequence else goal_cells
                before = b.graph.writers(target, head, 'first-frame source prerequisites')
                after = b.graph.writers(target, goal_cells, 'target source prerequisites')
                extensions = [((w,) + sequence,w) for w in before] + [(sequence + (w,),w) for w in after]
                for candidate,added in extensions:
                    if candidate in queued:continue
                    queued.add(candidate)
                    changed = [w['raw']['path'] for w in f.writes.values() if w['operation'] == added]
                    if not any(selector_relation(a, c) == 'same_shape' for a in changed for c in closure):
                        self.record['pruned'].append({'prefix': list(candidate), 'reason': 'no_write_to_prerequisite_closure'})
                        continue
                    queue.append(candidate)
            self.record['pending_prefixes'] = [list(s) for s in queue]
            for world in result.get('worlds', []):
                if not world.get('committed'):
                    continue
                frames = world.get('prefix_frames', [])
                writes = [w for fr in frames for w in fr['writes']]
                # Preserve guards, frame identities and complete keyed values.
                # Only exact equivalent symbolic states are pruned, never a
                # function merely because it has occurred earlier.
                signature = digest([f.identity, self.goal, self.plan,
                    [(c, read(c, writes, f.lookup(oid))) for c in closure],
                    [fr['guards'] for fr in frames], [fr['caller'] for fr in frames]])
                if signature in states:
                    self.record['pruned'].append({'prefix': list(sequence), 'reason': 'identical_typed_state_and_conditions'})
                    continue
                states.add(signature)
                reached = {'id': 'state_' + signature[:20], 'prefix': list(sequence),
                           'frames': copy.deepcopy(frames), 'writes': copy.deepcopy(writes),
                           'target_frame': copy.deepcopy(world['target_frame']),
                           'baseline_probe': world['query'], 'goal': copy.deepcopy(self.goal),
                           'plan': copy.deepcopy(self.plan), 'source_identity': f.identity,
                           'initial_prefix_policy': 'constructor_only_for_explicit_prefix'}
                self.record['states'].append(reached)
                yield reached
        self.record['frontier'] += [{'prefix': list(s), 'reason': 'candidate_bound'} for s in queue]
        self.record['search_complete_within_enumerated_scope'] = not queue
        self.record['unfound_is_not_unreachable'] = True


def search(b, oid, goal=None, plan=None, stop_on_first=True):
    searcher = TargetSearch(b, oid, goal, plan)
    for _ in searcher:
        if stop_on_first:
            searcher.record['stopped_on_target'] = True
            break
    r = searcher.record
    return dict(r, kind='prefix_search', reached_with_nonempty_prefix=any(s['prefix'] for s in r['states']),
                target_property=goal or {}, state_kind='source_checked_ordered_symbolic_target_states',
                providers=sorted({o for x in r['candidates_executed'] for o in x['prefix']}),
                excluded_unrelated_providers=r['pruned'], search_complete=False)

~~~~

## file-91f1722e1f17eb

`source/src/pr_next_joint/investigation/graph.py` · 原字节 SHA-256 `f857ada0630f3e2f3af8d038e4acea5fe7170c7c2362ed84318dfd332384dd22`

~~~~python
"""M1 neutral program graph, M2 hypotheses and M4 evidence in separate layers."""
import copy,collections,re,time
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import walk,key
from pr_next_joint.frontend.storage import selectors,selector_relation,keys
from .contracts import ident
from .request_scope import use_reads, unique_cells

class ProgramGraph:
    def __init__(self,facts):
        self.read_inputs={}
        self.facts=facts;self.nodes={};self.edges={};self.events=[];self.evidence_cache={};self.hypothesis_nodes={};self.ast_locators={}
        def ast_endpoint(target,ast_id,source=None):
            nid=ident('ast',[target,ast_id]);node=facts.lookups[target].nodes.get(ast_id)
            self.ast_locators[nid]={'target':target,'ast_id':ast_id,
                'source':facts.lookups[target].anchor(node) if node else source,
                'declaration_available':node is not None,'synthetic_or_external':node is None}
            return nid
        for target,lookup in facts.lookups.items():
            self.node(target,'contract',{'identity':target})
            for n in lookup.nodes.values():
                nid=ident('ast',[target,n.get('id')])
                if n.get('nodeType') in ('ContractDefinition','FunctionDefinition','ModifierDefinition','VariableDeclaration','EventDefinition','EmitStatement'):
                    self.node(nid,n['nodeType'],{'target':target,'ast_id':n['id'],'source':lookup.anchor(n)})
                if n.get('nodeType')=='ContractDefinition':
                    for base in n.get('linearizedBaseContracts',[])[1:]:self.edge(ast_endpoint(target,n['id']),ast_endpoint(target,base),'inherits')
        for oid,o in facts.operations.items():
            self.node(oid,'operation',o);self.edge(o['target'],oid,'entry')
            body=facts.lookup(oid).function(o['function'])
            if 'id' in body:self.edge(oid,ast_endpoint(o['target'],body['id'],o['source']),'entry_body')
            for n in walk(body):
                if n.get('nodeType')=='ModifierInvocation':self.edge(oid,ast_endpoint(o['target'],n.get('modifierName',{}).get('referencedDeclaration')),'modifier')
                if n.get('nodeType')=='FunctionCall':
                    decl=n.get('expression',{}).get('referencedDeclaration')
                    if type(decl)is int:self.edge(oid,ast_endpoint(o['target'],decl),'calls')
            for p in o['parameters']:
                nid=ident('parameter',[oid,p['ref']]);self.node(nid,'parameter',p);self.edge(oid,nid,'parameter');self.edge(nid,p['term'],'value_expression')
        for rid,r in facts.references.items():
            self.node(rid,'source_reference',r)
            self.edge(rid,ident('ast',[r['target'],r['ast_id']]),'binds_ast')
        for eid,e in facts.terms.items():self.node(eid,'expression',e)
        self.access=collections.defaultdict(lambda: {'writers':set(),'readers':set()})
        for pid,item in facts.paths.items():
            oid=item['operation'];raw=item['raw'];target=facts.operations[oid]['target']
            self.node(pid,'path',{'operation':oid,'flow':raw['flow'],'issues':raw.get('issues',[])})
            self.edge(oid,pid,'has_path')
            for g in raw['guards']:
                gid=ident('e',[target,g]);self.edge(gid,pid,'controls')
            for s in selectors(raw):
                sid=self.storage(target,s);self.edge(pid,sid,'reads');self.access[(target,s['root'])]['readers'].add(oid)
            for wid,w in facts.writes.items():
                if w['path']!=pid:continue
                self.node(wid,'state_effect',{'operation':oid,'path':pid,**w['raw']});self.edge(pid,wid,'commits')
                sid=self.storage(target,w['raw']['path']);self.edge(wid,sid,'writes')
                self.access[(target,w['raw']['path']['root'])]['writers'].add(oid)
                for s in selectors(w['raw']['value']):self.edge(self.storage(target,s),wid,'data_dependency')
            for eid,e in facts.effects.items():
                if e['path']==pid:self.node(eid,'external_effect',{'operation':oid,'path':pid,**e['raw']});self.edge(pid,eid,'external_effect')
            if raw.get('return_value') is not None:
                rid=ident('return',[pid,raw['return_value']]);self.node(rid,'return',{'expression':raw['return_value']});self.edge(pid,rid,'returns')
            for index,term in enumerate(raw.get('evaluated_terms',[])):
                tid=ident('eval',[pid,index]);self.node(tid,'evaluation',{'expression':term});self.edge(pid,tid,'evaluates')
        for (target,root),access in self.access.items():
            for a in access['writers']:
                for b in access['readers']:self.edge(a,b,'may_establish_use',{'target':target,'root':root,'may_alias_only':True})
        for i,g in enumerate(facts.gaps):
            nid=ident('gap',[i,g]);self.node(nid,'program_gap',g);self.edge(g['operation'],nid,'has_gap')
    def node(self,nid,kind,data,layer='program'):
        value={'id':nid,'kind':kind,'layer':layer,'data':copy.deepcopy(data)}
        if nid in self.nodes and self.nodes[nid]!=value:raise ValueError('graph_node_identity_conflict')
        self.nodes[nid]=value;return nid
    def edge(self,a,b,kind,data=None,layer='program'):
        row={'from':a,'to':b,'kind':kind,'layer':layer,'data':data or {}};eid=ident('edge',row);self.edges[eid]=row;return eid
    def storage(self,target,selector):
        nid=ident('object',[target,selector]);self.node(nid,'storage_object',{'target':target,'selector':selector})
        root=ident('ast',[target,selector['root']]);self.edge(nid,root,'storage_root')
        for i,s in enumerate(selector.get('segments',[])):
            kid=ident('selector',[target,selector,i]);self.node(kid,'storage_'+('key' if 'key' in s else 'length' if s.get('length') else 'field'),s);self.edge(nid,kid,'selector_position',{'position':i})
        return nid
    def writers(self,target,selectors_,reason):
        result=set()
        for s in selectors_:result.update(self.access.get((target,s['root']),{}).get('writers',set()))
        self.events.append({'action':'graph_writers','reason':reason,'roots':sorted({s['root'] for s in selectors_}),'operations':sorted(result),'binding_required':True})
        return sorted(result)
    def connected(self,oid,depth=2):
        seen={oid}
        for _ in range(depth):
            seen|={e['to'] for e in self.edges.values() if e['kind']=='may_establish_use' and e['from'] in seen}
            seen|={e['from'] for e in self.edges.values() if e['kind']=='may_establish_use' and e['to'] in seen}
        return sorted(seen)
    def neutral_frontier(self):
        """Index pre-answer source questions. A possible writer is not an authorized actor."""
        if hasattr(self, '_frontier'):
            return self._frontier
        f = self.facts
        writes = collections.defaultdict(list)
        for w in f.writes.values():
            path = w['raw']['path']
            writes[(f.operations[w['operation']]['target'], path['root'])].append(w)
        selected = []
        skipped = []
        # Spend a bounded number of candidate inspections per entry. Source access is independent.
        deadline=getattr(self,'frontier_deadline',time.monotonic()+f.options.seconds)
        for oid, operation in sorted(f.operations.items(), key=lambda x:(x[1]['target'],x[1]['source']['start'],x[0])):
            if time.monotonic()>=deadline:
                skipped.append({'entry':oid,'reason':'neutral_preselection_time_limit; source route open'})
                continue
            if operation['generated_getter']:
                continue
            target = operation['target']
            lookup = f.lookup(oid)
            best = None
            visits = 0
            for pid, path in f.operation_paths(oid, True):
                if not path['writes'] and not path.get('sensitive_effects'):
                    continue
                use = [('guard', s) for s in selectors(path['guards'])]
                use += [('effect_input', s) for s in selectors([w['value'] for w in path['writes']] + path.get('sensitive_effects', []))]
                seen = set()
                for kind, cell in use:
                    signature = kind, key(cell)
                    if signature in seen:
                        continue
                    seen.add(signature)
                    for row in writes.get((target, cell['root']), ()):
                        if visits >= f.options.max_actions:
                            break
                        visits += 1
                        writer = row['operation']
                        ws = row['raw']['path']
                        if writer == oid or selector_relation(ws, cell) != 'same_shape' or self._disjoint_keys(ws, cell):
                            continue
                        raw_writer = f.paths[row['path']]['raw']
                        if raw_writer['flow'] not in ('normal','returned') or raw_writer.get('issues') or raw_writer.get('evaluation_gaps'):
                            continue
                        actor = any(n.get('kind')=='actual_sender' for n in walk([path['guards'], cell, ws, raw_writer['guards']]))
                        rank = (not actor, kind!='guard', not bool(keys(cell)), f.operations[writer]['source']['start'], pid, writer)
                        if best is None or rank < best[0]:
                            best = rank, {'target':target,'writer':writer,'use':oid,'writer_path':row['path'],'use_path':pid,
                                'role_of_read':kind,'declaration':lookup.nodes[cell['root']].get('name'),
                                'ordered_write_key':ws,'ordered_read_key':cell,'write_source':row['raw']['source'],
                                'use_source':operation['source'],'sender_occurs':actor,'writer_guards':raw_writer['guards'],
                                'use_guards':path['guards'],'use_flow':path['flow'],
                                'effect_references':next(({'writes':c['writes'],'effects':c['effects']} for c in operation['paths'] if c['id']==pid),{}),
                                'stage':'possible earlier write then later use; no deployment reachability assertion',
                                'key_binding':'possible common storage position; caller and argument identities require investigation'}
                    if visits >= f.options.max_actions:
                        break
                if visits >= f.options.max_actions:
                    skipped.append({'entry':oid,'reason':'bounded_relation_enumeration'})
                    break
            if best:
                relation=best[1]
                cell=relation['ordered_read_key']
                related=[]
                for record in writes[(target,cell['root'])]:
                    s=record['raw']['path'];raw=f.paths[record['path']]['raw']
                    if raw['flow'] not in ('normal','returned') or raw.get('issues') or raw.get('evaluation_gaps'):
                        continue
                    if selector_relation(s,cell)=='same_shape' and not self._disjoint_keys(s,cell):
                        related.append({'operation':record['operation'],'path':record['path'],'ordered_key':s,
                                        'assigned':record['raw']['value'],'source':record['raw']['source']})
                    if len(related)>=f.options.max_actions:
                        skipped.append({'entry':oid,'reason':'related_write_index_bound'})
                        break
                relation['candidate_prior_writes']=related
                selected.append((best[0],relation))
            else:
                skipped.append({'entry':oid,'reason':'no_supported_cross_entry_meeting; source route open'})
        selected.sort(key=lambda x:(x[0],x[1]['target'],x[1]['use']))
        self._frontier = {'primary':selected[0][1] if selected else None,
                          'relations':[row for _,row in selected], 'limits':skipped,
                          'open_source_entries':sorted(f.operations), 'program_gaps':f.gaps,
                          'meaning':'neutral source relationships; no assertion of entitlement, policy or risk'}
        return self._frontier

    def closure_operations(self,oid,cells):
        """Include other original writers on the same possible key (grants, redemptions, alternative uses)."""
        target=self.facts.operations[oid]['target']
        by_operation={w for s in cells for w in self.access[(target,s['root'])]['writers']}
        return sorted({w['operation'] for w in self.facts.writes.values() if w['operation'] in by_operation
                       and any(selector_relation(s,w['raw']['path'])=='same_shape' and not self._disjoint_keys(s,w['raw']['path']) for s in cells)})

    def request_reads(self, oid):
        if oid not in self.read_inputs:
            self.read_inputs[oid] = unique_cells(cell for _, path in self.facts.operation_paths(oid, True)
                                                 for cell in use_reads(path))
        return self.read_inputs[oid]

    def investigation(self,oid,item,binding):
        """Compile one semantic uncertainty to a small source-grounded plan.

        Matching source names selects dependencies, never a business category.
        Omitted neighbors remain recorded possibilities, not refuted risks.
        """
        f=self.facts;o=f.operations[oid];lookup=f.lookup(oid);hint=item.get('next_check',{})
        hint=hint if isinstance(hint,dict) else {}
        question=item.get('distinguish',item.get('distinguishing_question',hint.get('question','')))
        if isinstance(question,dict):question=question.get('question','')
        text=' '.join(x for x in (item.get('claim'),item.get('alternative'),question) if isinstance(x,str))
        tokens=set(re.findall(r'[A-Za-z_$][\w$]*',text))
        guards=[s for _,p in f.operation_paths(oid) for s in selectors(p['guards'])]
        writes=[w['raw']['path'] for w in f.writes.values() if w['operation']==oid]
        named=[s for s in guards+writes if lookup.nodes.get(s['root'],{}).get('name') in tokens]
        focus=named or guards or writes
        focus=list({key(s):s for s in focus}.values())
        refs=set(binding.get('operations',[]));candidates=[]
        for other,op in f.operations.items():
            if other==oid or op['target']!=o['target']:continue
            ow=[w['raw']['path'] for w in f.writes.values() if w['operation']==other]
            og=self.request_reads(other)
            for change,observe,left,right in ((other,oid,ow,focus),(oid,other,writes,og)):
                shared=[s for s in left if any(selector_relation(s,t)=='same_shape' and not self._disjoint_keys(s,t) for t in right)]
                if not shared:continue
                # Explicit source names/anchors dominate possible root neighbors.
                explicit=other in refs or op['function'].split('(')[0] in tokens
                exact=any(key(s)==key(t) for s in shared for t in right)
                candidates.append({'change':change,'observe':observe,'controls':shared,
                  'rank':[0 if explicit else 1,0 if exact else 1,len(keys(shared[0])),
                          f.operations[change]['source']['start'],f.operations[observe]['source']['start']],
                  'source_reason':'explicit source relation' if explicit else 'matching ordered object in request guard, value, key or call'})
        candidates.sort(key=lambda x:x['rank']);unique={}
        for p in candidates:unique.setdefault((p['change'],p['observe']),p)
        candidates=list(unique.values());selected=candidates[:1]
        plan={'question':question or ('Which source-bound grant/control explains this effect, and does the related normal explanation apply?'),
          'risk_explanation':item['claim'],'normal_explanation':item.get('alternative'),
          'effect_root':oid,'focus_selectors':focus,'selected_pairs':selected,'deferred_pairs':candidates[1:],
          'selection_policy':'source relevance -> exact object shape -> cost; no confidence, Gold or expected score',
          'role_and_request_hints':{k:copy.deepcopy(hint[k]) for k in ('caller_mode','request_bindings') if k in hint}}
        self.events.append({'action':'question_guided_selection','operation':oid,'question':plan['question'],
            'selected':selected,'deferred_count':len(plan['deferred_pairs']),'focus':focus})
        return plan
    @staticmethod
    def _disjoint_keys(a,b):
        aa,bb=keys(a),keys(b)
        if len(aa)!=len(bb):return True
        return any(x.get('kind')==y.get('kind')=='literal' and x.get('value')!=y.get('value') for x,y in zip(aa,bb))
    def evidence(self,qid,record):
        # Store each immutable evidence entity once; graph edges carry its exact
        # scope. The separate evidence store owns formula/world payloads.
        identity=record.get('entity_sha256',digest(record));nid='evidence:'+identity
        card={k:copy.deepcopy(v) for k,v in record.items() if k not in ('worlds','queries','source_card','writer_cards','actual_guards','writes','effects')}
        card={k:v for k,v in card.items() if k not in ('id','question','semantic_version','action')}
        self.node(nid,'behavior_evidence',card,'evidence');self.edge(qid,nid,'supported_or_refuted_by',{'scope':record.get('evidence_scope',{})},layer='evidence')
        for field in ('operation','change','observe'):
            oid=record.get(field)
            if oid in self.facts.operations:self.edge(oid,nid,'evidence_source_operation',layer='evidence')
        def frames(value):
            if isinstance(value,dict):
                if 'operation' in value and 'slot' in value and ('committed_writes' in value or 'writes' in value):yield value
                for v in value.values():yield from frames(v)
            elif isinstance(value,list):
                for v in value:yield from frames(v)
        for fr in frames(record.get('worlds',{})):
            wid=ident('world',fr);self.node(wid,'execution_state_frame',{'sha256':digest(fr),'operation':fr['operation'],'path':fr['path'],'slot':fr['slot'],'full_frame_in':'evidence.json'},'evidence');self.edge(nid,wid,'uses_state_version',layer='evidence');self.edge(fr['operation'],wid,'source_operation_world',layer='evidence')
        return nid
    def record(self):return {'nodes':list(self.nodes.values()),'edges':list(self.edges.values()),'investigation_log':self.events,'semantics_are_not_program_facts':True}

~~~~

## file-b17a21d87d4dca

`source/src/pr_next_joint/investigation/initial_state.py` · 原字节 SHA-256 `4a7fb9497b142a11b110ed190ecffc694ed4356990c35a00339d9c4e296318ac`

~~~~python
"""Host-owned initial-state domains, constructor provenance and reachable writers.

This is a source transition summary, not a claim that an abstract state has been
deployed.  Every target freezes its numerical mapping candidates before M2.
"""
import copy
import re
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key, lit, walk
from pr_next_joint.frontend.storage import keys, selectors, fields, value_type
from pr_next_joint.frontend.source_entry_identity import function_kind
from pr_next_joint.frontend.program_paths import MechanismPaths

CAPABILITY = 'fcr_conditional_capability_r1'
DEPLOYMENT = 'solidity_deployment_r1'
AC_DOMAIN = 'ac_checked_prestate_r1'


def domain(lookup):
    return getattr(lookup, 'state_domain_override', None) or (CAPABILITY if getattr(lookup, 'analysis_scope', None) == 'FCR' else AC_DOMAIN)


def family(cell):
    return key({'root': cell['root'], 'segments': [{'key': '*'} if 'key' in s else s for s in cell.get('segments', [])]})


def reachable_functions(facts, target):
    """Resolve runtime roots first. Uncalled private/internal bodies are not writers."""
    lookup = facts.lookups[target]
    roots = [lookup.function(o['function']) for o in facts.operations.values() if o['target'] == target and not o.get('generated_getter')]
    pending = [n for n in roots if n]; found = {}; unresolved = []
    while pending:
        fn = pending.pop()
        if fn.get('id') in found: continue
        found[fn['id']] = fn
        for n in walk(fn):
            expr = n.get('modifierName') if n.get('nodeType') == 'ModifierInvocation' else n.get('expression') if n.get('nodeType') == 'FunctionCall' else None
            if not expr: continue
            ref = expr.get('referencedDeclaration'); callee = lookup.nodes.get(ref, {})
            if callee.get('nodeType') in ('FunctionDefinition', 'ModifierDefinition'):
                # External typed calls do not execute in the caller's storage.
                if expr.get('nodeType') == 'MemberAccess' and expr.get('expression', {}).get('typeDescriptions', {}).get('typeString', '').startswith('contract '):
                    continue
                if callee.get('body'): pending.append(callee)
                else: unresolved.append({'source': lookup.anchor(n), 'reason': 'runtime_callee_body_missing'})
    return found, unresolved


def assigned_roots(node, lookup):
    if not isinstance(node, dict):
        return set()
    typ = node.get('nodeType')
    if typ == 'Identifier':
        rid = node.get('referencedDeclaration')
        return {rid} if lookup.nodes.get(rid, {}).get('stateVariable') else set()
    if typ in ('IndexAccess', 'IndexRangeAccess'):
        return assigned_roots(node.get('baseExpression'), lookup)
    if typ == 'MemberAccess':
        return assigned_roots(node.get('expression'), lookup)
    if typ == 'TupleExpression':
        return set().union(*(assigned_roots(x, lookup) for x in node.get('components', [])))
    return set()


def runtime_writers(facts, target):
    lookup = facts.lookups[target]
    functions, gaps = reachable_functions(facts, target)
    sites = {}; opaque = []
    for fn in functions.values():
        for n in walk(fn.get('body') or {}):
            lhs = n.get('leftHandSide') if n.get('nodeType') == 'Assignment' else n.get('subExpression') if n.get('nodeType') == 'UnaryOperation' and n.get('operator') in ('delete', '++', '--') else None
            if lhs:
                for rid in assigned_roots(lhs, lookup):
                    sites.setdefault(rid, set()).add(n['id'])
            if n.get('nodeType') == 'InlineAssembly' and any(w in str(n).lower() for w in ('sstore', 'delegatecall', 'callcode')) or n.get('memberName') in ('delegatecall', 'callcode'):
                opaque.append(lookup.anchor(n))
    paths = {}
    for oid, operation in facts.operations.items():
        if operation['target'] != target: continue
        for pid, p in facts.operation_paths(oid):
            for w in p['writes']:
                if w['path'].get('instance'): continue
                # Exact IR roots include supported local storage references.
                # Index expressions remain reads, never declaration writes.
                if w.get('source', {}).get('ast_id') is not None:
                    sites.setdefault(w['path']['root'], set()).add(w['source']['ast_id'])
                paths.setdefault(w['path']['root'], []).append({'operation': oid, 'path': pid,
                    'source': w['source'], 'flow': p['flow'], 'value': w['value'], 'cell': w['path'],
                    'complete': p['flow'] in ('normal', 'returned') and not p.get('issues') and not p.get('evaluation_gaps')})
    return {'functions': sorted(functions), 'sites': {r: sorted(v) for r, v in sites.items()},
            'paths': paths, 'opaque_storage_writes': opaque, 'unresolved_calls': gaps}


def amount_candidates(facts, target):
    """Structural eligibility only: no token names, model decisions or risk labels."""
    result = {}
    def add(cell, oid, pid, reason):
        typ = value_type(cell, facts.lookup(oid))
        if keys(cell) and re.fullmatch(r'u?int\d*', typ or ''):
            result.setdefault(family(cell), {'cell': cell, 'type': typ, 'basis': []})['basis'].append(
                {'operation': oid, 'path': pid, 'reason': reason})
    for oid, operation in facts.operations.items():
        if operation['target'] != target: continue
        for pid, p in facts.operation_paths(oid, True):
            moves = []
            for w in p['writes']:
                cell, value = w['path'], w['value']; args = value.get('args', [])
                if value.get('op') in ('+', '-') and len(args) == 2 and any(key(cell) == key(s) for s in selectors(args[0])):
                    moves.append((w, value['op'], args[1]))
            ledger = []
            for w, sign, amount in moves:
                cell = w['path']
                if len(keys(cell)) != 1: continue
                conserved = any(other['path']['root'] == cell['root'] and family(other['path']) == family(cell)
                    and other_sign != sign and key(other_amount) == key(amount) for other, other_sign, other_amount in moves)
                supply = any(not keys(other['path']) and other_sign == sign and key(other_amount) == key(amount)
                    for other, other_sign, other_amount in moves)
                asset = any(any(key(amount) == key(n) for n in walk(effect)) for effect in p.get('sensitive_effects', []))
                native = any(n.get('kind') == 'transaction_value' for n in walk(amount))
                if conserved or supply or asset or native:
                    add(cell, oid, pid, 'same_quantity_account_flow' if conserved else 'supply_or_asset_linked_account_flow')
                    ledger.append((cell, amount))
            # Holder->spender quantities checked/consumed with an actual account debit.
            # Eligibility is not proof that the holder consented.
            for w, sign, amount in moves:
                if ledger and len(keys(w['path'])) >= 2 and any(key(amount) == key(a) for _, a in ledger):
                    add(w['path'], oid, pid, 'account_flow_related_numeric_grant')
    return [result[k] for k in sorted(result)]


def _constructor_paths(facts, target):
    original = facts.lookups[target]
    lookup = MechanismPaths(facts.bundle, original.contract, facts.options.max_paths)
    lookup.analysis_scope = facts.options.scope
    order = list(reversed(lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']])))
    constructors = {cid: next((n for n in lookup.nodes[cid].get('nodes', []) if n.get('nodeType') == 'FunctionDefinition' and function_kind(n) == 'constructor'), None) for cid in order}
    states = [{'env': {}, 'guards': [], 'writes': [], 'issues': [], 'flow': 'normal', 'evaluated_terms': []}]
    params = {}; derived = constructors[order[-1]]
    if derived:
        params.update({p['id']: {'kind': 'parameter', 'id': p['id'], 'type': p.get('typeDescriptions', {}).get('typeString'), 'constructor_parameter': True}
                       for p in derived.get('parameters', {}).get('parameters', [])})
    errors = []
    # Base arguments are compiler-resolved expressions in the declaring constructor's parameters.
    for cid in reversed(order):
        node = lookup.nodes[cid]; ctor = constructors[cid]
        specs = [(b.get('baseName', {}).get('referencedDeclaration'), b.get('arguments')) for b in node.get('baseContracts', [])]
        if ctor: specs += [(m['modifierName'].get('referencedDeclaration'), m.get('arguments')) for m in ctor.get('modifiers', [])]
        for bid, expressions in specs:
            if bid not in constructors or expressions is None: continue
            base = constructors[bid]; expected = (base or {}).get('parameters', {}).get('parameters', [])
            state = {'env': copy.deepcopy(params), 'guards': [], 'writes': [], 'issues': [], 'flow': 'normal'}
            try:
                lookup.current = state; lookup.source_evaluation_steps = 0
                values = [lookup.expr(a, state) for a in expressions]
                if state['writes'] or state['issues'] or len(values) != len(expected): raise ValueError('base_constructor_argument_effect_or_binding')
                params.update({p['id']: v for p, v in zip(expected, values)})
            except (ValueError, KeyError, TypeError, NotImplementedError) as ex:
                errors.append({'contract': bid, 'reason': str(ex), 'scope': 'constructor_arguments'})
    for cid in order:
        ctor = constructors[cid]; node = lookup.nodes[cid]
        # Solidity initializes each base's declarations immediately before that base body.
        lookup.source_evaluation_steps = 0; lookup.read_calls.summaries = {}; lookup.unknown = []
        lookup.source_execution_context = {'kind': 'constructor', 'entry_ast_id': (ctor or {}).get('id'), 'basis': 'compiled_linearized_constructor_order'}
        for state in states:
            if state['flow'] not in ('normal', 'returned'): continue
            state['flow'] = 'normal'; state['env'] = copy.deepcopy(params)
            for var in node.get('nodes', []):
                if not var.get('stateVariable') or var.get('value') is None: continue
                try:
                    value = lookup.expr(var['value'], state)
                    state['writes'].append({'path': {'kind': 'storage', 'root': var['id'], 'segments': []},
                        'value': value, 'operator': '=', 'source': lookup.anchor(var)})
                except (ValueError, KeyError, TypeError, NotImplementedError) as ex:
                    state['issues'].append({'reason': str(ex), 'declaration': var['id'], 'source': lookup.anchor(var)})
        if not ctor: continue
        clone = copy.deepcopy(ctor)
        clone['modifiers'] = [m for m in clone.get('modifiers', []) if lookup.nodes.get(m['modifierName'].get('referencedDeclaration'), {}).get('nodeType') != 'ContractDefinition']
        expected = ctor.get('parameters', {}).get('parameters', [])
        if any(p['id'] not in params for p in expected):
            errors.append({'contract': cid, 'reason': 'base_constructor_parameter_not_bound', 'scope': 'constructor_arguments'})
            continue
        out = []
        for state in states:
            if state['flow'] not in ('normal', 'returned'): out.append(state); continue
            state['flow'] = 'normal'
            try:
                out.extend(lookup.invoke(clone, [copy.deepcopy(params[p['id']]) for p in expected], state))
            except (ValueError, KeyError, TypeError, NotImplementedError) as ex:
                state['issues'].append({'reason': str(ex), 'source': lookup.anchor(ctor)}); out.append(state)
        states = out[:facts.options.max_paths]
        if len(out) > len(states): errors.append({'reason': 'constructor_path_frontier_bound_exceeded'})
    for state in states:
        state.pop('env', None)
        state['issues'].extend(copy.deepcopy(errors))
    return states, params


def model(facts, target):
    cache = facts.__dict__.setdefault('_initial_states', {})
    if target in cache: return cache[target]
    lookup = facts.lookups[target]
    bases = lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']])
    declarations = {n['id']: n for c in bases for n in lookup.nodes[c].get('nodes', []) if n.get('stateVariable')}
    candidates = amount_candidates(facts, target)
    writers = runtime_writers(facts, target)
    try: paths, parameters = _constructor_paths(facts, target)
    except (ValueError, KeyError, TypeError, NotImplementedError) as ex:
        paths = [{'flow': 'unknown', 'guards': [], 'writes': [], 'issues': [{'reason': str(ex)}]}]; parameters = {}
    rows = {}
    for rid, var in declarations.items():
        typ = var.get('typeDescriptions', {}).get('typeString', '')
        assigned = [w for p in paths for w in p['writes'] if w['path']['root'] == rid]
        # Unknown explicit writes remain explicit: never introduce a replacement abstract role.
        explicit_ctor_sites = [n['id'] for cid in bases for fn in lookup.nodes[cid].get('nodes', []) if fn.get('nodeType') == 'FunctionDefinition' and function_kind(fn) == 'constructor'
            for n in walk(fn.get('body') or {}) if n.get('nodeType') == 'Assignment' and rid in assigned_roots(n.get('leftHandSide', {}), lookup)]
        rows[rid] = {'declaration': rid, 'name': var.get('name'), 'type': typ, 'source': lookup.anchor(var),
            'explicit_initializer': var.get('value') is not None, 'constructor_writes': assigned,
            'explicit_constructor_sites': explicit_ctor_sites, 'runtime_sites': writers['sites'].get(rid, []),
            'runtime_paths': writers['paths'].get(rid, []), 'constant': bool(var.get('constant')),
            'immutable': var.get('mutability') == 'immutable'}
    value = {'schema': 'source_initial_states_r1', 'target': target, 'declarations': rows,
        'candidate_amount_leaves': candidates, 'constructor_paths': paths, 'constructor_parameters': parameters,
        'runtime_writers': writers, 'source_default_rule': 'typed_default_except_explicit_FCR_symbolic_scalar_or_frozen_amount_leaf',
        'domains': [CAPABILITY, DEPLOYMENT], 'exact_author_runtime_state_verified': False}
    value['identity'] = digest(value); cache[target] = value
    return value


def initial_for_lookup(lookup):
    facts = getattr(lookup, '_investigation_facts', None)
    if facts is None: return None
    return model(facts, lookup.contract['file'] + ':' + lookup.contract['name'])


def receipt(lookup):
    value = initial_for_lookup(lookup)
    return {'analysis_domain': domain(lookup), 'initial_model_identity': value['identity'] if value else None,
        'candidate_amount_leaves': value['candidate_amount_leaves'] if value else [],
        'abstract_capability_is_not_deployment': domain(lookup) == CAPABILITY}

~~~~

## file-31202ac308298f

`source/src/pr_next_joint/investigation/key_roles.py` · 原字节 SHA-256 `6cfe4fdba590227f406dff418f8f4b0a01a9ed604a39528fc76f76d7fe102f7f`

~~~~python
"""Finite key-role relations derived from source transfers and allowance uses.

Names and key order are not evidence. Ambiguous families retain their residual.
These records annotate positions; they do not change the state interpreter.
"""
import re
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, selector_relation, value_type
from .initial_state import family


def derive(f):
    proposals={}
    for oid,o in f.operations.items():
        lookup=f.lookup(oid)
        for pid,p in f.operation_paths(oid,True):
            if p.get('issues') or p.get('evaluation_gaps'):continue
            writes=p['writes'];debits=[];credits=[]
            for w in writes:
                v=w['value'];a=v.get('args',[]);cell=w['path']
                if not re.fullmatch(r'u?int\d*',value_type(cell,lookup) or ''):continue
                from .summary import local_delta
                sign,amount=local_delta(w)
                if sign in ('-','+'):(debits if sign=='-' else credits).append((cell,amount))
            for cell,amount in debits:
                idx=keys(cell)
                if len(idx)<2:continue
                token=(o['target'],family(cell))
                for dst,add in credits:
                    if selector_relation(cell,dst)!='same_shape' or key(amount)!=key(add):continue
                    ds=keys(dst);different=[i for i,(a,b) in enumerate(zip(idx,ds)) if key(a)!=key(b)]
                    if len(different)!=1:continue
                    h=different[0]
                    if idx[h].get('kind')=='actual_sender' and ds[h].get('type') in ('address','address payable'):
                        proposals.setdefault(token,[]).append({'holder_key':h,'kind':'asset_position',
                            'basis':'same_asset_self_debit_and_recipient_credit','operation':oid,'path':pid})
                for asset,spent in debits:
                    aks=keys(asset)
                    if len(aks)!=1 or len(idx)!=2 or not (amount and spent):continue
                    def parameters(term):
                        return {x['id'] for x in walk(term) if x.get('kind')=='parameter'}
                    same_amount=key(amount)==key(spent)
                    if not same_amount and not parameters(amount)&parameters(spent):continue
                    matches=[i for i,k in enumerate(idx) if key(k)==key(aks[0])]
                    if len(matches)!=1 or idx[1-matches[0]].get('kind')!='actual_sender':continue
                    if not any(key(c)==key(cell) for c in selectors(p['guards'])):continue
                    h=matches[0]
                    issuers=[w for w in f.writes.values() if f.operations[w['operation']]['target']==o['target'] and
                        selector_relation(w['raw']['path'],cell)=='same_shape' and len(keys(w['raw']['path']))==2 and
                        keys(w['raw']['path'])[h].get('kind')=='actual_sender' and w['raw']['value'].get('kind')=='parameter']
                    writers=[w for w in f.writes.values() if f.operations[w['operation']]['target']==o['target'] and
                        selector_relation(w['raw']['path'],cell)=='same_shape' and len(keys(w['raw']['path']))==2 and
                        w['raw']['value'].get('kind')=='parameter']
                    # Meaning and legitimate provenance are separate. A
                    # consumed allowance is still an authorization quantity
                    # when its only setter improperly writes another holder's
                    # key. Requiring a safe issuer here hid that very AC case.
                    if writers:
                        proposals.setdefault(token,[]).append({'holder_key':h,'kind':'authorization_quantity',
                            'basis':'holder_key_and_caller_index_linked_to_consumed_grant','asset':asset,
                            'debit_amount':spent,'consumed_amount':amount,'equal_expression':same_amount,
                            'operation':oid,'path':pid,'issuers':[w['operation'] for w in issuers],
                            'writers':[w['operation'] for w in writers],
                            'holder_provenance_proved_by_role_binding':False})
    records=[]
    for target,lookup in f.lookups.items():lookup.source_key_roles={}
    for (target,fam),rows in proposals.items():
        meanings={(r['holder_key'],r['kind']) for r in rows}
        if len(meanings)!=1:continue
        h,kind=next(iter(meanings));record={'holder_key':h,'kind':kind,'origins':rows,'family':fam,'target':target}
        f.lookups[target].source_key_roles[fam]=record;records.append(record)
    return records


def relation(cell,lookup):
    return getattr(lookup,'source_key_roles',{}).get(family(cell))

~~~~
