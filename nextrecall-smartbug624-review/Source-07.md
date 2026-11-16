## source/src/pr_next_joint/investigation/blocking.py

~~~~python
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


def root_reason(error):
    message=str(error).split(':',1)[0]
    return message if message.isidentifier() else type(error).__name__


def bool_under(term, control, enabled, holders, ordinary=True):
    """Truth forced by the selected control and the non-exempt request domain."""
    op=term.get('op'); args=term.get('args',[])
    if term.get('kind')=='literal' and type(term.get('value')) is bool:return term['value']
    if term.get('kind')=='storage':
        if selector_relation(term,control)=='same_shape' and (not keys(term) or keys(term)==holders):return enabled
        return None
    if op=='!' and len(args)==1:
        value=bool_under(args[0],control,enabled,holders,ordinary)
        return None if value is None else not value
    if op in ('&&','and','||','or'):
        values=[bool_under(x,control,enabled,holders,ordinary) for x in args]
        if op in ('&&','and'):return False if False in values else True if all(v is True for v in values) else None
        return True if True in values else False if all(v is False for v in values) else None
    if op in ('==','!=') and len(args)==2:
        l=bool_under(args[0],control,enabled,holders);r=bool_under(args[1],control,enabled,holders)
        if l is not None and r is not None:return (l==r)==(op=='==')
    return None


def ordinary_exemptions(b,oid,guards,control,holder=None):
    """Identify governed exception tables for the caller or the actual debit holder."""
    from .roles import _role_index
    from pr_next_joint.frontend.storage import value_type
    f=b.f;target=f.operations[oid]['target'];registry=_role_index(f,target)
    actors=[{'kind':'actual_sender'}]+([holder] if holder else [])
    result=set();cache=b.__dict__.setdefault('_governed_exception_tables',{})
    for term in selectors(guards):
        rid=term['root'];idx=keys(term)
        if rid==control['root'] or len(idx)!=1 or idx[0] not in actors or value_type(term,f.lookup(oid))!='bool':continue
        stamp=(target,rid)
        if stamp not in cache:
            writers=[w for w in f.writes.values() if w['raw']['path']['root']==rid
                     and f.operations[w['operation']]['target']==target
                     and w['raw']['value'].get('value') is not False]
            protected=bool(writers) and all(
                f.paths[w['path']]['raw']['flow'] in ('returned','normal')
                and not f.operations[w['operation']]['gaps']
                and path_qualification(f,w['operation'],f.paths[w['path']]['raw'])
                for w in writers)
            cache[stamp]=bool(protected or registry.get(rid,{}).get('kind')=='caller_membership')
        if cache[stamp]:result.add(rid)
    return result


def gates_ordinary(b,oid,path,control,blocked,holder):
    """Rules out this productive branch for the same ordinary unexempt request."""
    from .behavior import _replace
    exemptions=ordinary_exemptions(b,oid,path['guards'],control,holder)
    replace={key(s):{'kind':'literal','value':False} for s in selectors(path['guards'])
             if s['root'] in exemptions and keys(s) in ([{'kind':'actual_sender'}],[holder])}
    return any(bool_under(_replace(g,replace),control,blocked,[holder]) is False for g in path['guards'])


def delegated_exception(b,routes,control,blocked):
    """Find a source-defined alternate for the same economic request, conditional on
    a holder grant and independently governed sender privilege. No grant is assumed.
    Unconditional alternatives are tested separately by gates_ordinary.
    """
    from .behavior import _replace
    from .summary import holder, local_delta
    for alternate in routes:
        oid=alternate['operation'];lk=b.f.lookup(oid);p=b.f.paths[alternate['path']]['raw']
        payer=holder(alternate['debit'],lk)
        if not payer or payer.get('kind')!='parameter' or p.get('sensitive_effects') or p.get('issues') or p.get('evaluation_gaps'):continue
        grants=grant_for(b,oid,p,alternate['debit'])
        if not grants or not any(key(w['path'])==key(grants) and local_delta(w)[0]=='-' for w in p['writes']):continue
        exceptions=ordinary_exemptions(b,oid,p['guards'],control)
        if not exceptions or not gates_ordinary(b,oid,p,control,blocked,payer):continue
        # A privileged flag must turn an actual necessary outgoing guard from
        # false to satisfiable under the disabled switch; other guards still apply.
        flagged=[s for s in selectors(p['guards']) if s['root'] in exceptions and keys(s)==[{'kind':'actual_sender'}]]
        for flag in flagged:
            for g in p['guards']:
                no=_replace(g,{key(flag):{'kind':'literal','value':False}})
                yes=_replace(g,{key(flag):{'kind':'literal','value':True}})
                if bool_under(no,control,blocked,[payer]) is not False or bool_under(yes,control,blocked,[payer]) is not True:continue
                if any(bool_under(_replace(other,{key(flag):{'kind':'literal','value':True}}),control,blocked,[payer]) is False for other in p['guards']):continue
                amount=[v for v in b.f.operations[oid]['parameters'] if b.f.terms[v['term']]['expression'].get('type','').startswith('uint')]
                recipient=holder(alternate['credit'],lk)
                if len(amount)!=1 or not recipient or recipient.get('kind')!='parameter' or key(recipient)==key(payer):continue
                request=b.f.terms[amount[0]['term']]['expression']
                if not any(key(w['path'])==key(grants) and local_delta(w)[0]=='-' and
                           key(local_delta(w)[1])==key(request) for w in p['writes']):continue
                return {'scope':'same_ledger_holder_recipient_and_request_quantity','use':b.f.operations[oid]['source'],
                        'requires_prior_holder_grant':True,'requires_exempt_spender':True,'availability':'conditional_on_existing_grant_and_membership'}
    return None


def _direct_baseline(b,change,cpid,route,control,blocked,cat):
    """Check the actual positive use and committing controller transition in one source state.
    Search only useful enabling and grant writers; normal initial and prefix bounds apply.
    """
    from pr_next_joint.verification.sequence import read
    from .behavior import ordered_clocks
    from .summary import holder
    f=b.f;use=route['operation'];pid=route['path'];lk=f.lookup(use)
    cp=f.paths[cpid]['raw'];p=f.paths[pid]['raw'];grant=grant_for(b,use,p,route['debit'])
    delegated=holder(route['debit'],lk).get('kind')!='actual_sender'
    if delegated and not grant:return None
    extra=[]
    for oid in f.operations:
        if f.operations[oid]['target']!=f.operations[change]['target']:continue
        for wpid,wp in f.operation_paths(oid,True):
            for w in wp['writes']:
                if grant and selector_relation(w['path'],grant)=='same_shape' and w['value'].get('kind')=='parameter' and any(k.get('kind')=='actual_sender' for k in keys(w['path'])):
                    extra.append((0,len(wp['writes']),len(wp['guards']),oid,wpid))
                elif w['path']['root']==control['root'] and w['path'].get('segments')==control.get('segments') and (
                        w['value'].get('kind')!='literal' or w['value'].get('value')!=blocked):
                    extra.append((1,len(wp['writes']),len(wp['guards']),oid,wpid))
    # Prefer a grant or enabling write with fewer unrelated committed changes.
    # The actual prefix and every guard are still checked by the same encoder.
    ordered=list(dict.fromkeys((oid,wpid) for *_,oid,wpid in sorted(extra)))
    from itertools import chain, islice, permutations
    singles=((item,) for item in ordered) if f.options.prefix_depth>=1 else ()
    pairs=permutations(ordered,2) if f.options.prefix_depth>=2 else ()
    for sequence in islice(chain([()],singles,pairs),f.options.max_prefixes):
        b.check()
        try:
            e=MechanismEncoder(lk);z=e.z;prior=[];terms=[]
            for slot,(oid,wpid) in enumerate(sequence):
                prefix=frame(f,oid,wpid,slot,prior);terms.extend([encode_frame(e,prefix),e.expr(prefix['caller'])!=0])
                prior=prior+prefix['writes']
            slot=len(sequence);cf=frame(f,change,cpid,slot,prior);uf=frame(f,use,pid,slot+1,prior)
            terms.extend([encode_frame(e,cf),encode_frame(e,uf),*ordered_clocks(e,slot+1)])
            actor=e.expr(cf['caller']);user=e.expr(uf['caller'])
            h,before,after,_,_=flow(e,lk,uf,route['debit'])
            recipient,rb,ra,_,_=flow(e,lk,uf,route['credit'])
            terms.extend([actor!=0,user!=0,h!=0,h!=actor,user!=actor,recipient!=0,recipient!=h,before>after,ra>rb])
            if any(n.get('kind')=='contract_address' for n in walk(cp['guards'])):
                terms.append(actor!=e.expr({'kind':'contract_address','type':'address'}))
            payer=holder(route['debit'],lk)
            flags=ordinary_exemptions(b,use,p['guards'],control,payer)
            for flag in selectors(p['guards']):
                if flag['root'] in flags and keys(flag) in ([{'kind':'actual_sender'}],[payer]):
                    terms.append(z.Not(e.expr(read(qualify(flag,slot+1),prior,lk))))
            # Match the *effective* control on the holder, after all setter writes.
            use_cell={**control,'segments':[{'key':qualify(holder(route['debit'],lk),slot+1)}] if keys(control) else []}
            terms.extend([e.expr(read(use_cell,prior,lk))!=blocked,
                          e.expr(read(use_cell,prior+cf['writes'],lk))==blocked])
            final_control=qualify(control,slot)
            if keys(control):terms.append(e.expr(keys(final_control)[0])==h)
            q=b._query(e,z.And(*terms),'productive_control_transition',{
                'operation':change,'observe':use,'target':f.operations[use]['target'],'category':cat,
                'same_request':True,'baseline_commit_not_assumed':True,'effect_required':True,
                'initial_prefix_policy':'constructor_only_for_explicit_prefix','measurement_only':True})
            if q.get('bounded_condition_confirmed'):return q['id']
        except (Unsupported,ValueError) as error:
            b.__dict__.setdefault('_control_limit_reasons',set()).add((root_reason(error),use))
            continue
    return None


def ordinary_control_uses(inv,root,category):
    """Rank real outgoing uses of the final control. A source route is not a successful request."""
    from .comparison import ledger_routes
    from .summary import holder
    from .coverage import _control_categories
    from pr_next_joint.frontend.storage import value_type
    _control_categories(inv)
    candidates=inv._coverage_control_routes.get((root,category),set())
    if not candidates:return ()
    f=inv.f;target=f.operations[root]['target']
    stamp=(root,category,inv.semantics.dependency_identity(candidates|{root}))
    cache=inv.__dict__.setdefault('_ordinary_control_uses',{})
    if stamp in cache:return cache[stamp]
    controls={}
    for row in f.summaries.rows(root):
        if not row['committing']:continue
        for w in row['ordered_writes']:
            cell=w['path']
            typ=value_type(cell,f.lookup(root)) or ''
            if bool(keys(cell))==(category=='FCR-FREEZE') and (typ=='bool' or typ.startswith(('uint','int'))):
                controls[(row['path'],key(cell))]=cell
    ranked={}
    for route in ledger_routes(inv.backend,target):
        oid=route['operation']
        if oid not in candidates:continue
        p=f.paths[route['path']]['raw'];payer=holder(route['debit'],f.lookup(oid))
        if not payer or path_qualification(f,oid,p):continue
        if not any(s['root']==ctrl['root'] and (not keys(ctrl) or keys(s)==[payer]) for s in selectors(p['guards']) for ctrl in controls.values()):continue
        delegated=payer.get('kind')!='actual_sender'
        if delegated and not grant_for(inv.backend,oid,p,route['debit']):continue
        rank=(bool(p.get('issues') or p.get('evaluation_gaps')),delegated,f.operations[oid]['source']['start'],oid)
        ranked[oid]=min(ranked.get(oid,rank),rank)
    cache[stamp]=tuple(sorted(ranked,key=ranked.get))
    return cache[stamp]


def ordinary_family(b, change, use, controls):
    """Classify an exact outgoing comparison for an arbitrary non-exempt account."""
    from .comparison import ledger_routes
    from .summary import holder
    f=b.f;target=f.operations[change]['target']
    if f.operations[use]['target']!=target:return None
    routes=ledger_routes(b,target)
    for ctrl in controls:
        if keys(ctrl):continue
        for main in routes:
            if main['operation']!=use:continue
            account=holder(main['debit'],f.lookup(use))
            if not account:continue
            raw=f.paths[main['path']]['raw']
            if not any(s['root']==ctrl['root'] for s in selectors(raw['guards'])):continue
            same=[r for r in routes if r['debit']['root']==main['debit']['root']]
            # Residuals on a source capable of providing the same ordinary
            # request remain decisive. A disjoint effect is outside this scope.
            if not same or any(not continuation_frontier_covered(b,r['operation']) for r in same):continue
            for mode in (True,False):
                admissible=True;governed=set()
                for route in same:
                    oid=route['operation'];branch=f.paths[route['path']]['raw']
                    payer=holder(route['debit'],f.lookup(oid))
                    if not payer or branch.get('issues') or branch.get('evaluation_gaps'):
                        admissible=False;break
                    if path_qualification(f,oid,branch):continue
                    if not gates_ordinary(b,oid,branch,ctrl,mode,payer):
                        admissible=False;break
                    governed.update(ordinary_exemptions(b,oid,branch['guards'],ctrl,payer))
                if admissible and gates_ordinary(b,use,raw,ctrl,mode,account):
                    return {'population':'arbitrary_nonexempt_holder' if governed else 'ordinary_source_holders',
                            'request':'same_holder_asset_recipient_and_positive_quantity',
                            'exemptions':'governed_membership' if governed else 'none_required',
                            'bypass':'checked_applied_productive_routes'}
    return None


def direct_control_result(b,root,use,cat):
    from .comparison import ledger_routes
    from .source_opinion import opinion
    from .summary import holder
    from pr_next_joint.frontend.storage import value_type
    f=b.f;rows=f.summaries.rows(root)
    target=f.operations[root]['target'];routes=ledger_routes(b,target)
    for row in rows:
        path=f.paths[row['path']]['raw']
        if not path_qualification(f,root,path) or row['residuals'] or row['effects']:continue
        final={}
        for w in row['ordered_writes']:final[key(w['path'])]=w
        for w in final.values():
            ctrl=w['path'];indexed=bool(keys(ctrl))
            if value_type(ctrl,f.lookup(root))!='bool' or indexed!=(cat=='FCR-FREEZE'):continue
            if indexed and len(keys(ctrl))!=1:continue
            for route in routes:
                oid=route['operation'];pid=route['path'];p=f.paths[pid]['raw'];lk=f.lookup(oid)
                h=holder(route['debit'],lk)
                if oid!=use or not h or p.get('sensitive_effects') or path_qualification(f,oid,p):continue
                family=route['debit']['root']
                for blocked in (True,False):
                    # At least one real guard reads this exact control/holder.
                    if not any(s['root']==ctrl['root'] and (not indexed or keys(s)==[h]) for s in selectors(p['guards'])):continue
                    if not gates_ordinary(b,oid,p,ctrl,blocked,h):continue
                    candidates=[r for r in routes if r['debit']['root']==family]
                    if any(not path_qualification(f,r['operation'],rp) and
                           not gates_ordinary(b,r['operation'],rp,ctrl,blocked,holder(r['debit'],f.lookup(r['operation'])))
                           for r in candidates for rp in [f.paths[r['path']]['raw']]):continue
                    # A frontier with a possible independently committing transfer is open
                    # unless its already-established guards also exclude the ordinary use.
                    siblings={r['operation'] for r in candidates}
                    if any(c['mode']=='DELEGATECALL' and c['unresolved_implementation'] and
                           f.operations[c['operation']]['target']==target for c in f.call_summaries.rows.values()):continue
                    if any(not continuation_frontier_covered(b,o) or any(
                           rp['flow']!='reverted' and (rp.get('issues') or rp.get('evaluation_gaps')) and
                           not gates_ordinary(b,o,rp,ctrl,blocked,holder(r['debit'],f.lookup(o)))
                           for _,rp in f.operation_paths(o)) for r in candidates for o in [r['operation']]):continue
                    stamp=(root,row['path'],key(ctrl),oid,pid,blocked,b.semantics.dependency_identity(siblings|{root}))
                    cache=b.__dict__.setdefault('_productive_control_checks',{})
                    if stamp not in cache:
                        cache[stamp]=_direct_baseline(b,root,row['path'],route,ctrl,blocked,cat)
                    if cache[stamp]:
                        result=opinion('risk','productive_outgoing_control',[w['source']])
                        result.update(productive_use=f.operations[oid]['source'],basis_probe=cache[stamp],controller_path=row['path'])
                        if cat=='FCR-PAUSE':
                            group=ordinary_family(b,root,oid,[ctrl])
                            if not group:continue
                            result['holder_family']=group
                        exception=delegated_exception(b,candidates,ctrl,blocked)
                        if exception:result['conditional_agent']=exception
                        return result
    return None


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
    start=len(b.records)
    direct=direct_control_result(b,change,use,prop['category'])
    if direct:
        return {'kind':'causal_compare','change':change,'observe':use,'observed_measure':'financial_block',
                'property_identity':prop['id'],'queries':b.records[start:],'source_control_result':direct,
                'scope_supported':True,'property_excluded':False,'local_errors':[]}
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
                    exact_primary=set()
                    for pid, p in all_use_paths:
                        b.check()
                        deps = b.condition_dependencies(use, pid, p)
                        if deps['unknown_dependencies'] or deps['credential_dependencies']:
                            continue
                        snapshot=e.checkpoint()
                        try:
                            a = b.source_frame(use,pid,slot,writes)
                            c = b.source_frame(use,pid,slot,writes+cf['writes'])
                            usable0,cells=productive(b,e,a,use)
                            usable1,_=productive(b,e,c,use)
                            holders=[flow(e,f.lookup(use),a,cell)[0] for cell in cells]
                            typed_request=request or request_terms(b,e,a,use)
                        except Unsupported as error:
                            e.rollback(snapshot);exact=False
                            gaps.append({'operation':use,'path':pid,'reason':str(error),
                                'scope':'isolated primary continuation; siblings remain executable'})
                            continue
                        request_objects+=cells;request_holders+=holders
                        request=typed_request;before.append(usable0);after.append(usable1)
                        exact_primary.add(pid)
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
                                snapshot=e.checkpoint()
                                try:
                                    value,error=alternate_continuation(b,e,other,apid,writes+cf['writes'],request,slot+10)
                                except Unsupported as error_:value,error=None,str(error_)
                                if value is None:
                                    e.rollback(snapshot);exact=False
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
                    if not baseline['bounded_condition_confirmed']:
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
                        if q['answer']=='unknown':
                            gaps.append({'reason':'quantified_blockage_not_decided_without_parameter_extraction',
                                         'query':q['id'],'not_a_negative_result':True})
                        if (not prefix and exact and not local_approximations and
                            not q['details'].get('pinned_UNSAT_not_a_universal_negative') and
                            q.get('exclusion_certificate',{}).get('excludes_only_this_formula')):
                            globally_excluded_paths.add(cpid)
                        rows.append({'baseline_probe': baseline['id'], 'block_probe': q['id'],
                                     'result': q['answer'], 'prefix': list(prefix)})
                        worlds.append({'prefix': [serialize_world(x, 'COMMON_PREFIX') for x in prefix_frames],
                                       'intervention': serialize_world(cf, 'INTERVENTION'),
                                       'same_request_slot': slot, 'actual_prefix_writes': writes})
                        if q['bounded_condition_confirmed']:
                            break
                except Unsupported as error:
                    gaps.append({'prefix': list(prefix), 'reason': str(error)})
            if any(q['label'] == 'financial_block' and q['bounded_condition_confirmed'] for q in queries):
                break
        if any(q['label'] == 'financial_block' and q['bounded_condition_confirmed'] for q in queries):
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
    group=None
    if prop['category']=='FCR-PAUSE' and any(
            q.get('label')=='financial_block' and q.get('bounded_condition_confirmed')
            and q.get('details',{}).get('all_continuations_exact') for q in queries):
        group=ordinary_family(b,change,use,relevant)
    scope_supported = complete and (prop['category'] != 'FCR-PAUSE' or collective or bool(group))
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
            'stopped_reason':target_search.record.get('stopped_reason'),
            'continuation_approximations':approximation_records,
            'financial_scope': {'target': target, 'declared_use': use, 'controls': relevant,
                                'productive_paths': [p for p, _ in all_use_paths], 'complete': complete,
                                'collective_source_control': collective, 'ordinary_holder_family':group, 'prefixes_tried': [list(x) for x in prefixes]}}

~~~~

## source/src/pr_next_joint/investigation/call_summary.py

~~~~python
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

    def effect_dependencies(self,row,effect,*,initiation=False):
        """Residuals that can change this path's selected operation or committed result."""
        from pr_next_joint.frontend.storage import selectors
        at=effect.get('where') or {}
        value=effect.get('write',{})
        guards=row['guards']
        origin_call=next((term for term in row['effects'] if term.get('kind')==effect.get('kind') and term.get('source')==at),None)
        if initiation and origin_call is not None and 'callpoint_guards' in origin_call:
            guards=origin_call['callpoint_guards']
        terms=[guards,value.get('value'),effect.get('cell')]
        if origin_call:
            terms.extend(origin_call.get(k) for k in ('recipient','amount','beneficiary','target') if origin_call.get(k) is not None)
        if any(n.get('kind') in ('unknown','external_return','native_call_success','credential_recovery') for n in walk(terms)):
            return ['condition_or_value_requires_external_result']
        roots={s['root'] for s in selectors(terms)}
        unresolved=[]
        for call in self.rows.values():
            if call['operation']!=row['operation'] or call['path']!=row['path'] or not call['unresolved_implementation']:continue
            same=call['source'].get('ast_id') is not None and call['source'].get('ast_id')==at.get('ast_id')
            if same and initiation and effect.get('kind')=='native_transfer':continue
            if call['mode']=='DELEGATECALL' or roots.intersection(call['may_callback_writes']):
                unresolved.append('same_scope_possible_storage_change')
            elif call['catch_semantics'].startswith('high-level'):
                unresolved.append('same_path_propagating_revert')
        for gap in row['residuals']:
            if gap.get('cell') and gap['cell'].get('root') not in roots:continue
            if gap.get('reason')=='multiple_address_keys_need_source_holder_binding' and initiation and not effect.get('cell'):continue
            loc=gap.get('source') or {}
            associated=bool(loc) and any(call['path']==row['path'] and call['source']==loc for call in self.rows.values())
            if gap.get('reason') and not associated:unresolved.append('unresolved_source_expression')
        return sorted(set(unresolved))

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

~~~~

## source/src/pr_next_joint/investigation/candidates.py

~~~~python
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
        groups={}
        for item in extra:
            identity=('applied_extra_effect',key(item['source']),key(item['position']))
            groups.setdefault(identity,{})[key(item)]=item
        for item in exits:
            identity=('independent_sensitive_exit',key(item['effect'].get('source')),item['effect'].get('kind'))
            groups.setdefault(identity,{})[key(item)]=item
        for identity,occurrences in groups.items():
            kind=identity[0];items=list(occurrences.values())
            row={'operation':oid,'target':op['target'],'kind':kind,
                 'extra_effects':items if kind=='applied_extra_effect' else [],
                 'sensitive_exits':items if kind=='independent_sensitive_exit' else [],
                 'candidate_requires_assessment':True,'not_counterevidence':True}
            row['id']='candidate_'+digest(row)[:16];result.append(row)
    return result


def source_duty(rules, effect, kind):
    """Trace an applied write back to independent program uses of its authority or unit."""
    from .ledger import grant_for, unit_origin, native_only_position
    from .source_opinion import office_use, office_guard, feasible_source_guards, role_ids
    from .summary import holder, local_delta
    from pr_next_joint.frontend.storage import keys, value_type, selector_relation
    d=rules.effects[effect]; f=rules.f; oid=d['oid']; lk=f.lookup(oid)
    if kind=='termination':
        # The initial bool value and a separately governed public completion
        # distinguish the ordinary completed phase from discretionary early termination.
        from .initial_state import initial_for_lookup
        for pid in d.get('branches',{}):
            row=f.summaries.paths[pid]
            if not row['committing'] or f.call_summaries.effect_dependencies(row,d): continue
            for branch in row['guards']:
                flag=branch['args'][0] if branch.get('op')=='!' and len(branch.get('args',[]))==1 else branch
                if flag.get('kind')!='storage' or keys(flag) or value_type(flag,lk)!='bool': continue
                enabled=branch is flag
                initial=(initial_for_lookup(lk) or {}).get('declarations',{}).get(flag['root'],{})
                # A non-default initial stage must be known, never guessed.
                if initial.get('explicit_initializer') or initial.get('constructor_writes'): continue
                governors=[]; stable=True
                for peer in rules.by_decl.get(rules.obj(d['target'],flag['root']),()):
                    pd=rules.effects[peer]; pr=f.summaries.paths[pd['path']]
                    if not pr['committing']:continue
                    roles=role_ids(rules.inv,pd['oid'],pr)
                    if not roles or pr['residuals']:stable=False;break
                    governors.append((pd,roles))
                if not stable or not governors:continue
                finalizer=next((pd for pd,_ in governors if pd['write']['value'].get('value') is True),None)
                if not finalizer:continue
                sibling=any(other!=oid and f.operations[other]['target']==d['target'] and
                    any(r['committing'] and not r['residuals'] and any(t.get('kind')=='native_selfdestruct' for t in r['effects'])
                        and any(key(g)==key(flag) for g in r['guards']) for r in f.summaries.rows(other))
                    for other in f.operations)
                if enabled or sibling:
                    return dict(family='managed_lifecycle', duty='governed_active_phase', path=pid,
                                support=finalizer['where'], phase='completed' if enabled else 'active', phase_guard=key(branch),
                                controller_guarded=bool(role_ids(rules.inv,oid,row)))
        return None
    if 'write' not in d or rules.overwritten(effect):return None
    row=f.summaries.paths[d['path']];w=d['write'];cell=w['path']
    if not row['committing'] or f.call_summaries.effect_dependencies(row,d):return None
    if not feasible_source_guards(row['guards']):return None
    sign,qty=local_delta(w);idx=keys(cell)
    if kind=='credit':
        acct=holder(cell,lk)
        if not acct or acct.get('kind') not in ('actual_sender','parameter'):return None
        if not qty or not any(v.get('kind')=='parameter' for v in walk(qty)):return None
        # A source debit or paid purchase supplies consideration on this path.
        if row['effects'] or any(local_delta(v)[0]=='-' for v in row['ordered_writes']):return None
        if any(n.get('kind') in ('transaction_value','unknown','external_return') for n in walk([row['guards'],qty])):return None
        from .ledger import same_unit_transfers
        from .initial_state import family
        use=same_unit_transfers(f,d['target'],include_checked_arithmetic=True).get(family(cell))
        if not use or not unit_origin(rules.inv.backend,oid,cell) or native_only_position(rules.inv.backend,oid,cell):return None
        # The different, actually conserved holder transfer supplies the duty
        # evidence. The unbacked write itself cannot supply its own norm.
        support=next((r['source'] for r in use if r['operation']!=oid),None)
        if not support:return None
        return dict(family='unbacked_issuance',duty='conservation_of_disposable_holder_unit',
                    path=row['path'],support=support)
    if kind=='qualification' and not idx and value_type(cell,lk)=='bool':
        # A write to a business flag is a phase duty only if the same declaration
        # governs a committed sensitive use and an independently governed writer
        # establishes who controls that transition.
        dependencies=f.summaries.dependencies
        for eid in dependencies.readers.get((d['target'],cell['root']),()):
            use=dependencies.rows[eid]['use']
            if use==oid:continue
            for branch in f.summaries.rows(use):
                if not branch['committing'] or branch['residuals'] or not any(
                        s['root']==cell['root'] for s in selectors(branch['guards'])):continue
                relevant=any(x.get('kind') in ('native_transfer','native_selfdestruct') for x in branch['effects']) or any(
                    holder(v['path'],f.lookup(use)) is not None and local_delta(v)[0] for v in branch['ordered_writes'])
                if not relevant:continue
                peers=[rules.effects[p] for p in rules.by_decl.get(rules.obj(d['target'],cell['root']),()) if rules.effects[p]['oid']!=oid]
                for peer in peers:
                    if not peer.get('clean') or not role_ids(rules.inv,peer['oid'],f.summaries.paths[peer['path']]):continue
                    value=w['value'];governed=peer['write']['value']
                    if value.get('kind')!='parameter' and key(value)!=key(governed):continue
                    return dict(family='managed_phase',duty='separately_governed_effect_transition',path=row['path'],
                                support=peer['where'],use=use)
    if kind!='qualification':return None
    if len(idx)==2 and w['value'].get('kind') in ('parameter','literal') and not sign:
        # The same declaration in the enforced grant identifies the issuer index;
        # swapping the two address keys is not a source-compatible permission.
        deps=f.summaries.dependencies
        uses={deps.rows[e]['use'] for e in deps.readers.get((d['target'],cell['root']),())}
        for use in sorted(uses-{oid}):
            if not rules.remaining():return None
            for pid,raw in f.operation_paths(use,True):
                for output in raw['writes']:
                    payer=holder(output['path'],f.lookup(use))
                    if not payer or local_delta(output)[0]!='-':continue
                    gr=grant_for(rules.inv.backend,use,raw,output['path'])
                    if not gr or selector_relation(gr,cell)!='same_shape':continue
                    issuer=next((i for i,t in enumerate(keys(gr)) if key(t)==key(payer)),None)
                    if issuer is not None:
                        return dict(family='grant_then_use',duty='holder_issued_grant', path=row['path'],
                                    issuer=idx[issuer]['kind'], support=output['source'],use=use)
    if (not idx and value_type(cell,lk) in ('address','address payable') and w['value'].get('kind') in ('parameter','actual_sender')
        or len(idx)==1 and w['value'].get('value') is True):
        use=office_use(rules.inv,oid,cell)
        if use:return dict(family='grant_then_use',duty='guarded_downstream_use', path=row['path'],
                           support=f.operations[use]['source'],use=use)
    return None


def investigate(inv):
    inv.candidate_trace=[]
    if inv.f.options.scope=='AC':
        rules=inv.semantics.rules
        # One question for each distinct occurrence. Untyped questions do
        # not inherit a model opinion; a real scoped policy can attach later.
        for e,kind in getattr(rules,'sensitive_effects',{}).items():
            if not inv.program_remaining():break
            # Full basic reading covers the whole registered directory. Materialize broad
            # source questions on demand; an omitted candidate can get the second slot.
            if e not in rules.source_duties and kind not in ('credit','termination') and e not in (inv.initial_manifest or {}).get('displayed_effect_handles',()):continue
            oid=rules.effects[e]['oid']
            if not any(inv.root(q)==oid and e in q['current'].get('_scope_effects',()) for q in inv.issues.values()):
                rules.create_consumer(oid,'AC',{e})
    for candidate in inv.f.source_candidates:
        oid=candidate['operation'];rules=inv.semantics.rules
        positions={(key(w['position']),key(w['source'])) for w in candidate['extra_effects']}
        wanted={e for e in rules.by_operation.get(oid,()) if 'cell' in rules.effects[e] and (key(rules.effects[e]['cell']),key(rules.effects[e]['where'])) in positions}
        # A single terminating effect with no writes needs no second host question when
        # the existing reading already addresses that exact source entry and policy.
        exit_locs={key(x['effect'].get('source')) for x in candidate['sensitive_exits']}
        wanted.update(e for e in rules.by_operation.get(oid,()) if rules.effects[e].get('kind')=='native_selfdestruct'
                      and key(rules.effects[e]['where']) in exit_locs)
        existing=[q for q in inv.issues.values() if inv.root(q)==oid and
                  wanted and set(q['current'].get('_scope_effects',()))==wanted]
        if existing:
            q=existing[0];q['host_source_candidate']=candidate
            inv.enqueue(q['id'],'inspect',{'operation':oid,'enhance':False},1,'inspect applied extra effect against the existing explanation')
        else:
            item={'id':'host_'+candidate['id'],'anchors':[inv.catalog.name(oid)],'assessment':'investigate',
                  'category':'AC' if inv.f.options.scope=='AC' else 'ADDITIONAL',
                  'claim':'The actual applied entry has a committed '+candidate['kind']+'. Determine the affected subject, authorization and asset, and whether the existing explanation covers this effect.',
                  '_host_source_question':True,'_scope_effects':sorted(wanted)}
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
    rules=inv.semantics.rules
    for request in scope.get('refinement_requests',()):
        oid=request['operation'];category=request['category'];effects=set(request['effects'])
        if not effects or not inv.program_remaining():continue
        if any(inv.root(q)==oid and (q.get('property') or q['current']).get('category')==category and
               effects<=set(q['current'].get('_scope_effects',())) for q in inv.issues.values()):continue
        q=rules.create_consumer(oid,category,effects)
        if not q:continue
        q['host_obligation_question']={'selected_operation':oid,'category':category,'other_entries_not_marked_complete':True}
        created.append(q['id'])
        inv.candidate_trace.append({'operation':oid,'target':inv.f.operations[oid]['target'],'question':q['id'],
            'kind':'unresolved_source_obligation','state':'queued','generated_risk_claim':False})
    return created

~~~~

## source/src/pr_next_joint/investigation/cli.py

~~~~python
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
from .decision_output import context_summary,receipt

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

def run(args,*,responses=None,client_factory=None,deadline=None):
    source_root=Path(__file__).resolve().parents[3];sys.path.insert(0,str(source_root/'runtime'))
    from reference_counter import Counter
    from bridge import FixtureClient,UsageJournal
    out=Path(args.out).resolve();out.mkdir(parents=True,exist_ok=True)
    if any(out.iterdir()):raise ValueError('fresh_output_required')
    config=json.loads(Path(args.config).read_text(encoding='utf-8-sig')) if args.config else {}
    if config.get('live_model_authorized') or config.get('live_authorized'):raise ValueError('stage2_no_live_authorization')
    if set(config)-{'method','options','live_model_authorized','notes'}:raise ValueError('unknown_config_keys')
    f,intake=load_program(args.root,args.compiled_unit,args.task,config.get('options'),args.target,args.engineering_compiled)
    write(out/'intake_receipt.json',intake);counter=Counter(args.tokenizer)
    if args.phase=='prepare':
        graph=ProgramGraph(f);ctx=SourceContext(f,Catalog(f,graph),counter);messages,manifest=ctx.messages()
        write(out/'prepared_receipt.json',{'manifest':context_summary(manifest),'host_identity':f.identity,**receipt(messages,'prepared_model_request')})
        return {'prepared_only':True,'real_model_calls':0,'manifest':context_summary(manifest)}
    if responses is None:responses=[Path(p).read_text(encoding='utf-8-sig') for p in (args.fixture_response,args.fixture_feedback) if p]
    if client_factory is not None:
        broker=nullcontext();client=client_factory(f,args,counter)
    elif args.offline_bridge:
        raise ValueError('file_bridge_not_available_in_decision_only_build')
    else:broker=nullcontext();client=FixtureClient(responses,args.case_id)
    with broker:report=analyze(f,out/'analysis',counter=counter,client=client,deadline=deadline)
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
        write(out/('technical_error_'+str(time.time_ns())+'.json'),{'error':type(error).__name__,'error_sha256':hashlib.sha256(str(error).encode()).hexdigest(),'risk_prediction_synthesized':False})
        print('工程入口停止：'+type(error).__name__,flush=True)
    finally:
        stop.set();thread.join(1);print('运行结束：'+('已保存离线工程结果' if result==0 else '入口异常，错误原件已保存')+'；实际模型调用0；目录 '+str(Path(args.out).resolve()),flush=True)
    return result

~~~~
