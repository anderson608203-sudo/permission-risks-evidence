"""Shared, source-keyed balances, grants and parameter-dependent settlement."""
from .m03_p_paths import key, lit, op, walk
from .m03_p_route import keys, fields, effective_permission, value_type
from .m05_bound_relations import family
from .m05_state_relations import compose_read
from .m04_logic import Unsupported
from .m22_assets import matches, identity

SENDER = {'kind':'actual_sender'}


def committed(path):
    return path['flow'] in ('normal','returned') and not path['issues'] and not path.get('evaluation_gaps')


def semantic_assets(context, relations, state, tid, program):
    """A holder/claim proposal may seed a ledger only after actual redemption
    by the same holder or a source-conserved transfer has been established."""
    from .m09_shared_policy import bind_resource
    from .m05_control_baseline import transfer_summary
    ops = {o['id']: o for o in context['operations']}
    lookup = state['lookups'][tid]
    found = {}
    for relation in relations['relations']:
        operation = ops[relation['op_ref']]
        if operation['target'] != tid or relation['relation_kind'] not in ('holder_of','delegates_to','debits_for_redemption'):
            continue
        val, _ = bind_resource(relation,context,state)
        if not val or val.get('kind') != 'storage':
            continue
        for fn in dict.fromkeys([operation['function']]+[ops[o]['function'] for o in relation['related_op_refs']]):
            for p in program.get(fn,[]):
                if not committed(p):continue
                for w in p['writes']:
                    sel = w['path']
                    if sel['root'] != val['root'] or len(keys(sel))!=1 or fields(val)!=fields(sel):continue
                    if not (value_type(sel,lookup) or '').startswith('uint'):continue
                    asset={'balance_root':sel['root'],'supply_root':None,'balance_effect':w,
                           'kind':'verified_semantic_holder_transfer','relation_id':relation['id']}
                    try:s = transfer_summary(p,asset,lookup)
                    except Unsupported:continue
                    if s and s.get('recipient') and s['holder']==SENDER and s['recipient'].get('kind')=='parameter':
                        found.setdefault(identity(sel),asset)
    return list(found.values())


def operations(index,tid,asset):
    seen=set()
    for r in index.writers.get((tid,asset['balance_root'],tuple(fields(asset['balance_effect']['path']))),[]):
        pos=(r['function'],r['path_index'])
        if pos not in seen and matches(r['effect']['selector'],asset):
            seen.add(pos)
            yield pos


def management_grants(context,state,index):
    """Reverse a concrete authority-replacement effect to its membership grant.
    Exclude personal registration and roles which only gate a local service."""
    from .m11_policy import make_query
    from .m20_policy import role_evidence
    from .m21_admission import atoms
    rows=[]
    for tid,lookup in state['lookups'].items():
        program={fn:ps for (t,fn),ps in state['paths'].items() if t==tid}
        roles={}
        for r in index.by_target[tid]:
            e=r['effect'];principal=e.get('selector')
            if not principal or principal.get('segments') or principal.get('instance') or value_type(principal,lookup) not in ('address','address payable'):continue
            w=e.get('original_write');fn=r['function'];p=program[fn][r['path_index']]
            if not w or w['value'].get('kind') not in ('parameter','actual_sender') or not committed(p):continue
            for guard in atoms(p['guards']):
                if guard.get('kind')!='storage' or keys(guard)!=[SENDER] or value_type(guard,lookup)!='bool':continue
                if guard.get('instance') or fields(guard):continue
                proof=roles.setdefault(key(principal),None)
                if proof is None:
                    roles[key(principal)]=proof=[u for u in role_evidence(lookup,program,principal)
                        if u['function']!=fn and committed(program[u['function']][u['path_index']])
                        and program[u['function']][u['path_index']].get('writes')]
                if not proof:continue
                for grant in index.writers[tid,guard['root'],()]:
                    ge=grant['effect'];cell=ge['selector'];subjects=keys(cell)
                    if not family(cell,guard) or len(subjects)!=1 or subjects[0].get('kind') not in ('actual_sender','parameter'):continue
                    setter=grant['function'];sp=program[setter][grant['path_index']]
                    if not committed(sp) or ge['value']!=lit(True):continue
                    # Both stages must be jointly feasible for the new member
                    # and old nonzero administrator in the same state history.
                    from .m20_sequence import qualify,read
                    subject=subjects[0]
                    def stage2(term):
                        from .m05_mechanism_core import remap
                        term=remap(qualify(term,1),{-9000001:subject})
                        return read(term,sp['writes'],lookup)
                    model=dict(sp)
                    model['guards']=[*sp['guards'],op('!=',principal,lit(0)),op('!=',subject,lit(0)),op('!=',subject,principal),
                        op('!',cell),*[stage2(g) for g in p['guards']],op('!=',stage2(principal),stage2(w['value']))]
                    model['evaluated_terms']=[*sp.get('evaluated_terms',[]),*[stage2(x) for x in p.get('evaluated_terms',[])]]
                    required=op('or',op('==',SENDER,principal),guard,*effective_permission(sp['guards'],lookup))
                    basis={'basis':'membership_grants_replacement_of_active_authority','consumer':fn,'consumer_effect':e['source'],
                           'authority':principal,'role_use':proof,'granted_subject':subject,
                           'scope':'conditional local access to replacing an extant administrative principal'}
                    q=make_query(context,tid,setter,grant['path_index'],model,ge['original_write'],required,basis,'AC-02')
                    rows.append(q);index.use(grant,'grants_management_capability',q['id'])
    return rows


def amount_duties(context,state,index,relations,shared):
    from .m11_policy import make_query
    from .m05_asset_obligations import consent_model
    from .m05_state_relations import changes
    from .m03_p_assets import negative
    from .m22_assets import unique
    rows=[]; gaps=[]
    for tid,lookup in state['lookups'].items():
        program={fn:ps for (target,fn),ps in state['paths'].items() if target==tid}
        assets=unique(list(shared.get(tid,{}).get('assets',[]))+semantic_assets(context,relations,state,tid,program))
        for asset in assets:
            for fn,pi in operations(index,tid,asset):
                p=program[fn][pi]
                if not committed(p):continue
                # A real allowance expenditure has both holder and caller keys.
                allowances=[w['path'] for w in p['writes'] if len(keys(w['path']))==2 and keys(w['path'])[1]==SENDER and w['path']['root']!=asset['balance_root']]
                if not allowances:continue
                try:
                    updates=changes(p,lookup)
                    for d in updates:
                        w=d['write'];sel=w['path'];subjects=keys(sel)
                        if not matches(sel,asset) or len(subjects)!=1 or subjects[0].get('kind')!='parameter':continue
                        holder=subjects[0]
                        for debit in updates:
                            current=debit['write']['path'];quantity=debit['delta']
                            if current not in allowances or keys(current)[0]!=holder or not quantity:continue
                            # Reuse the original grant, writer, scope and quantity
                            # checks for the amount actually charged to the allowance.
                            consent,certs=consent_model(p,holder,negative(quantity),lookup,program,asset['balance_root'],asset.get('supply_root'),sufficient_only=True)
                            cert=next((c for c in certs if c.get('allowance')==current),None)
                            if not cert:continue
                            post=compose_read(sel,p['writes'],lookup)
                            # Mathematical difference of the two proven state
                            # versions. Do not evaluate an unsigned Solidity subtraction.
                            covered=op('<=',op('-',sel,post),current)
                            required=op('or',covered,op('==',holder,SENDER),*effective_permission(p['guards'],lookup))
                            basis={'basis':'holder_gross_debit_exceeds_applicable_spend_limit','allowance':cert,
                                   'pre_balance':sel,'post_balance':post,'post_allowance':compose_read(current,p['writes'],lookup),
                                   'semantic_asset_relation':asset.get('relation_id'),'source_unit':'same holder balance and certified spend limit'}
                            q=make_query(context,tid,fn,pi,p,w,required,basis,'AC-04')
                            q['conditions'].extend([consent,op('>',current,compose_read(current,p['writes'],lookup))])
                            from .core import digest
                            q['id']='q_'+digest(q)
                            rows.append(q)
                except Unsupported as ex:
                    gaps.append({'phase':'quantity_authorization','target':tid,'function':fn,'reason':str(ex)})
    return rows,gaps


def parameter_checks(tid,index,lookup,program,assets):
    """Compare the very same user request before/after a privileged setter.
    Keep parameter evidence separate from a destruction verdict."""
    from .m08_financial import probe
    from .m05_asset_obligations import privilege
    from .m20_sequence import qualify,read,request_states
    observations=[];risk_checks=[]
    for asset in assets:
        for fn,pi in operations(index,tid,asset):
            p=program[fn][pi]
            if not committed(p):continue
            writes=[w for w in p['writes'] if matches(w['path'],asset)]
            roots={t['root'] for w in writes for t in walk(w['value']) if t.get('kind')=='storage' and not t.get('segments') and (value_type(t,lookup) or '').startswith('uint')}
            if not roots:continue
            visited=set()
            for root in sorted(roots):
                for record in index.writers.get((tid,root,()),[]):
                    setter,si=record['function'],record['path_index']
                    s=program[setter][si];effect=record['effect']
                    if setter==fn or (setter,si) in visited or not committed(s) or s.get('native_transfers') or s.get('sensitive_effects'):continue
                    # Model all outputs of an atomic configuration update.
                    # Refuse mixed changes to balances, supply, or unrelated state.
                    if any(w['path'].get('segments') or w['path'].get('instance') or w['path']['root'] not in roots or
                           w['path']['root'] in (asset['balance_root'],asset.get('supply_root')) for w in s['writes']):continue
                    visited.add((setter,si))
                    priv=privilege(s['guards'],lookup,asset['balance_root'])
                    if not priv:continue
                    step=qualify(s,1); sw=step['writes']
                    for sel in {key(w['path']):w['path'] for w in writes}.values():
                        try:
                            old,new=request_states(compose_read(sel,p['writes'],lookup),sw,lookup)
                            if key(new)==key(old):continue
                            before=p['guards'];after=read(before,sw,lookup)
                            conditions=[*step['guards'],qualify(op('or',*priv),1),op('!=',qualify(SENDER,1),SENDER),*before,*after]
                            meta={'kind':'privileged_parameter_changes_same_request_settlement','setter':setter,'consumer':fn,
                                  'setter_source':effect['source'],'setter_writes':[w['source'] for w in s['writes']],'account':sel,'before':old,'after':new,
                                  'all_request_writes':p['writes'],'evaluation_terms':step.get('evaluated_terms',[])+p.get('evaluated_terms',[])+read(p.get('evaluated_terms',[]),sw,lookup)}
                            q=probe(lookup,conditions,op('!=',old,new),dict(meta),effect['source'],fn,'parameter_influence')
                            observations.append({'phase':'financial_parameter_check','mechanism_only':True,'check':q})
                            index.use(record,'financial_parameter_comparison',reason=q['formal']['query'])
                            if q['reportable']:
                                risk=settlement_loss(lookup,program,asset,p,fn,sel,old,new,sw,conditions,meta)
                                if risk:risk_checks.append(risk)
                        except Unsupported as ex:observations.append({'phase':'financial_parameter_check','reason':str(ex),'function':fn})
        from .m28_settlement import switched_requests
        extra,notes=switched_requests(tid,lookup,program,index,asset)
        risk_checks.extend(extra);observations.extend(notes)
    return risk_checks,observations


def settlement_loss(lookup,program,asset,p,fn,cell,old,new,sw,conditions,meta,baseline=None):
    """Narrow incremental third-party burn: the same holder's authorized
    transaction becomes an excess debit and all extra debit is extinguished."""
    from .m05_asset_obligations import consent_model
    from .m05_state_relations import changes
    from .m03_p_assets import negative
    from .m20_sequence import read
    from .m08_financial import probe
    if len(keys(cell))!=1 or keys(cell)[0].get('kind')!='parameter':return None
    holder=keys(cell)[0];supply=asset.get('supply_root')
    if p.get('native_transfers') or p.get('sensitive_effects'):return None
    updates=changes(p,lookup)
    supply_basis='registered_asset_supply'
    if supply is None:
        # An ordinary transfer proves the asset without identifying supply.
        # Obtain the missing link from this settlement's own conservation proof.
        from .m18_asset_witness import fee_witness
        balances=[d for d in updates if matches(d['write']['path'],asset)]
        debit=next((d for d in balances if d['write']['path']==cell),None)
        witness=fee_witness(lookup,p,debit,balances,updates) if debit else None
        if not witness or not witness['supply']:return None
        supply=witness['supply']['write']['path']['root']
        supply_basis='same_path_aggregate_decrement_matches_total_holder_loss'
    supply_cells=[w['path'] for w in p['writes'] if w['path']['root']==supply and not w['path'].get('segments')]
    if not supply_cells or len({key(x) for x in supply_cells})!=1:return None
    supply_cell=supply_cells[0]
    before=p if baseline is None else baseline
    if before.get('native_transfers') or before.get('sensitive_effects'):return None
    supply_before=compose_read(supply_cell,before['writes'],lookup)
    supply_after=read(compose_read(supply_cell,p['writes'],lookup),sw,lookup)
    spend=[d for d in updates if keys(d['write']['path'])==[holder,SENDER] and d['delta']]
    if len(spend)!=1:return None
    limit=spend[0]['write']['path']
    if not all(matches(w['path'],asset) or w['path'] in (supply_cell,limit) for w in p['writes']+before['writes']):return None
    _,certificates=consent_model(p,holder,negative(spend[0]['delta']),lookup,program,asset['balance_root'],supply,sufficient_only=True)
    if not any(c.get('allowance')==limit for c in certificates):return None
    if any(n.get('kind') in ('credential_recovery','hash','unknown') for n in walk(p['guards'])):return None
    protected=set((cell['root'],supply,limit['root']))
    if any(n.get('kind')=='storage' and holder in keys(n) and n['root'] not in protected for n in walk(p['guards'])):return None
    terms=[op('!=',holder,SENDER),op('>=',limit,op('-',cell,old)),op('>',op('-',cell,new),limit),
           op('>',old,new),op('==',op('-',old,new),op('-',supply_before,supply_after))]
    for peer in {key(w['path']):w['path'] for w in p['writes']+before['writes'] if matches(w['path'],asset)}.values():
        if peer==cell:continue
        if len(keys(peer))!=1:return None
        final=compose_read(peer,p['writes'],lookup)
        prior=compose_read(peer,before['writes'],lookup)
        terms.extend([op('!=',holder,keys(peer)[0]),op('==',prior,read(final,sw,lookup))])
    return probe(lookup,conditions,op('and',*terms),
        {**meta,'kind':'privileged_parameter_burn_beyond_delegated_limit','asset':asset,'holder':holder,
         'allowance':limit,'supply_basis':supply_basis,'supply_before_setter_case':supply_before,'supply_after_setter_case':supply_after},
        meta['setter_source'],fn,'FCR-DESTROY')
