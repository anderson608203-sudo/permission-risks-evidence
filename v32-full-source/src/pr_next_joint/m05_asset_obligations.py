from .m20_solver import solve as bounded_solve
"""M2-triggered, source-reconstructed holder interference queries.

Native-redeemable ledgers and proportional shares reuse the existing M1 asset
relations. M4 encodes actual guards, net holder changes and consent, rather than
copying an LLM verdict. Unknown assets/calls/consent remain explicit gaps.
"""
import copy,hashlib
from .m05_writer_scope import gaps_for
from .core import digest
from .m03_p_paths import key,walk,op,lit
from .m03_p_route import keys,selectors,permission_atoms,value_type
from .m03_p_assets import AssetPaths,asset_models,deltas,term,negative,holder_path,unsafe_integer_cast
from .m04_asset_math import proportional_models
from .m04_joint_formal import JointEncoder
from .m04_logic import Unsupported
from .m05_state_relations import changes as state_changes,scalar
from .m05_mechanism_core import program as mechanism_program,MechanismEncoder,execution_terms


def privilege(guards,lookup,holder_root):
    from .m03_p_route import effective_permission
    result=[]
    for guard in effective_permission(guards,lookup):
        for atom in [guard]:
            roots=selectors(atom)
            if not roots or any(s['root']==holder_root for s in roots):continue
            # The role/address is independent of the debited holder. Relational
            # owner/delegate predicates need their own consumer, not this one.
            if any(any(n.get('kind')=='parameter' for n in walk(keys(s))) for s in roots):continue
            instances=getattr(getattr(lookup,'read_calls',None),'instances',{})
            if all(not s.get('instance') or instances.get(key(s['instance']),{}).get('binding') in
                   ('immutable_direct_new','constructor_single_assignment_direct_new','conditional_compiled_concrete_type')
                   for s in roots):result.append(atom)
    return list({key(x):x for x in result}.values())


def consent_model(path,holder,amount,lookup,program,ledger_root,supply_root,credential=None,recipient=None,sufficient_only=False):
    self_consent=op('==',{'kind':'actual_sender'},holder)
    if holder.get('kind')=='actual_sender':
        return lit(True),[{'kind':'actual_caller_is_debited_holder','source_holder':holder,'scope':'direct own-balance action; no delegated consent inferred'}]
    if holder.get('kind')=='contract_address':
        raise Unsupported('contract_held_beneficial_ownership_unresolved')
    consent=[self_consent];known={ledger_root,supply_root};known_selectors=set();certificates=[]
    from .m24_consent import operation_scope
    action_scope=operation_scope(path,holder,amount,lookup,ledger_root,recipient)
    from .m05_equity_relations import linear_quantity
    from .m05_bound_relations import holder_authorized_request,family
    requests=holder_authorized_request(path,holder,linear_quantity(amount),lookup,program,recipient,
        excluded_roots={ledger_root,supply_root})
    for request in requests:
        consent.append(request['predicate']);certificates.append(request['certificate'])
    if credential:
        consent.append(credential['holder_consent']);certificates.append(credential['certificate'])
        from .m05_credential_obligations import nonce_bookkeeping
        for write in path['writes']:
            if nonce_bookkeeping(write,credential['certificate']['credential'],path['guards']):
                known.add(write['path']['root'])
    for change in state_changes(path,lookup):
        sel=change['write']['path'];idx=keys(sel)
        if sel['root'] in (ledger_root,supply_root):continue
        if len(idx) not in (1,2) or key(idx[0])!=key(holder):continue
        if len(idx)==2 and idx[1].get('kind')!='actual_sender':continue
        from .m24_consent import same_quantity
        if not same_quantity(change['delta'],negative(amount),lookup):continue
        setters=[];record_address_scope=False
        for fn,paths in program.items():
            for candidate in paths:
                if candidate['flow']=='reverted' or candidate['issues']:continue
                for w in candidate['writes']:
                    kk=keys(w['path'])
                    if (family(w['path'],sel) and len(kk)==len(idx) and
                        kk[0].get('kind')=='actual_sender' and (len(kk)==1 or kk[1].get('kind')=='parameter') and
                        w['value'].get('kind')=='parameter'):
                        setters.append({'function':fn,'source':w['source']})
                        # A quantity field in a holder-created record with an
                        # address field is not an unscoped scalar allowance.
                        # Only the typed request consumer may certify its
                        # destination relationship. Missing scope stays open.
                        for peer in candidate['writes']:
                            pp=peer['path']
                            if (pp['root']==w['path']['root'] and pp.get('instance')==w['path'].get('instance')
                                    and keys(pp)==kk and key(pp)!=key(w['path'])
                                    and value_type(pp,lookup) in ('address','address payable')):
                                record_address_scope=True
        from .m03_p_paths import conditions_possible
        # Consent data written by an unrelated authority is not holder consent.
        for fn,paths in program.items() if setters else []:
            for candidate in paths:
                if candidate['flow']=='reverted':continue
                for w in candidate['writes']:
                    kk=keys(w['path'])
                    if w['path']['root']==sel['root'] and kk:
                        consumption=next((d['delta'] for d in state_changes(candidate,lookup) if d['write'] is w or d['write']==w),None)
                        if consumption and all(v<=0 for v in consumption.values()):continue
                        if key(kk[0])==key({'kind':'actual_sender'}):continue
                        if candidate['issues'] or conditions_possible(candidate['guards'],op('==',kk[0],{'kind':'actual_sender'})):
                            raise Unsupported('consent_state_has_non_holder_writer')
        if setters and not (recipient is not None and record_address_scope):
            if gaps_for(lookup,{sel['root']}):raise Unsupported('allowance_writer_inventory_incomplete')
            number=linear_quantity(amount)
            consent.append(op('>=',sel,number));known_selectors.add(key(sel))
            certificates.append({'allowance':sel,'holder_controlled_setters':setters,'consumption':change['write'],'action_applicability':action_scope,
                'scope':'holder, spender, resource, quantity and actual source consumption; shared transfer/burn allowance is allowed when supported by these same checks'})
    # Proving a sufficient authorization is distinct from claiming absence of
    # every possible authorization. Keep the original strict default for FCR.
    if sufficient_only and certificates:
        from .m09_shared_policy import implies
        predicate=op('or',*consent)
        if implies(lookup,path,predicate):
            return predicate,certificates+[{'kind':'source_sufficient_authorization',
                'scope':'full amount and bound subject/object; all path guards retained'}]
    # A holder-related guard might be signed/delegated/protocol consent. Do not
    # silently interpret absence of a known allowance as absence of all consent.
    for guard in path['guards']:
        for sel in selectors(guard):
            if any(key(sel)==key(r['selector']) or key(sel)==key(r['certificate'].get('recipient')) for r in requests):continue
            if sel['root'] in known or key(sel) in known_selectors:continue
            if any(key(x)==key(holder) for x in keys(sel)):
                if gaps_for(lookup,{sel['root']}):raise Unsupported('holder_state_writer_inventory_incomplete')
                from .m05_consent_state import revocation_only,automatic_deposit_clock
                clock=automatic_deposit_clock(sel,holder,lookup,program,ledger_root)
                if clock:
                    certificates.append(clock);known_selectors.add(key(sel));continue
                # A cooldown written only by the same privileged service is
                # not holder-issued consent. Conversely, any holder-writable
                # state remains a consent dependency until its use is modeled.
                from .m03_p_route import fields
                writers=[];holder_writable=False
                for f,branches in program.items():
                    for branch in branches:
                        if branch['flow']=='reverted':continue
                        for w in branch['writes']:
                            if w['path']['root']!=sel['root'] or fields(w['path'])!=fields(sel):continue
                            if family(w['path'],sel):
                                revoked=revocation_only(branch,w,sel,path,holder,linear_quantity(amount),lookup)
                                if revoked:
                                    certificates.append(revoked);writers.append({'function':f,'source':w['source'],'revocation_only':True});continue
                            kk=keys(w['path']);independent=privilege(branch['guards'],lookup,ledger_root)
                            own=kk and kk[0].get('kind')=='actual_sender'
                            if branch['issues'] or own or not independent:holder_writable=True
                            writers.append({'function':f,'source':w['source'],'independent_privilege':independent})
                if not writers or holder_writable:raise Unsupported('holder_related_consent_guard_requires_model')
                certificates.append({'selector':sel,'relation':'source_writers_are_privileged_not_holder_authorizers',
                                     'writers':writers,'scope':'on-chain writer relation only; off-chain authorization not inferred'})
                known_selectors.add(key(sel))
    if any(n.get('kind')=='unknown' or n.get('kind')=='hash' and not credential for g in path['guards'] for n in walk(g)):
        raise Unsupported('credential_or_unknown_consent_condition')
    return op('or',*consent),certificates


def solve(lookup,model,path,pi,fn,rule,obligation,amount,debit,credit,priv,consent,certificates,holder_scope):
    from .m05_common_semantics import prepare, consumed
    from time import perf_counter
    started=perf_counter()
    owner=keys(debit['write']['path'])[0]
    symbolic={'kind':'privileged_holder_interference','rule':rule,'model':model,'function':fn,
              'path_index':pi,'guards':path['guards'],'debit':debit,'credit':credit,
              'privilege':priv,'consent':consent,'amount':amount,'writes':path['writes'],
              'consent_sources':certificates,'same_holder_compensation':path.get('native_transfers',[]),
              'holder_scope':holder_scope,
              'successful_evaluation':execution_terms(path,lookup),
              'integer_semantics':'checked bounded unsigned source values; signed mathematical net deltas',
              'policy_scope':'source_derived_financial_interest_and_onchain_consent',
              'assumptions':['source-derived asset or conserved transferable ledger; redemption only if established by selected model','current symbolic pre-state',
                             'off-chain authorization is not encoded; model alternatives retained']}
    from .m05_equity_relations import compensation_basis,linear_quantity
    quantity=linear_quantity(amount)
    symbolic['compensation_basis']=compensation_basis(model,quantity,path.get('native_transfers',[]))
    instances=getattr(getattr(lookup,'read_calls',None),'instances',{})
    cross=[copy.deepcopy(instances[key(s['instance'])]) for p in priv for s in selectors(p)
           if s.get('instance') and key(s['instance']) in instances]
    if cross:
        symbolic['privilege_instance_origins']=cross
        symbolic['assumptions'].append('external permission reads retain supplied concrete instance identity; configured code identity is conditional, not deployed evidence')
    if holder_scope['kind']=='bounded_distinct_holder_batch':
        symbolic['assumptions'].append(holder_scope['scope'])
    from .m05_relation_model_scope import constrain_model
    constrain_model(obligation,lookup,symbolic)
    attempt={'id':'ma_'+digest({'obligation':obligation['id'],'model':symbolic}),
        'model_sha256':digest(symbolic),'kind':symbolic['kind'],'function':fn,
        'question_refs':[],'phase':'model_constructed','formal_attempted':False}
    obligation.setdefault('_model_attempts',[]).append(attempt)
    try:
        common, inputs=prepare(obligation,fn,symbolic,model['balance_root'],owner)
        encoder=MechanismEncoder(lookup);z=encoder.z
        guards,violation=interference_formula(encoder,inputs,lookup)
    except Exception as ex:
        attempt.update(phase='formula_construction_failed',reason=type(ex).__name__+':'+str(ex));raise
    credential_certificates=[c for c in certificates if c.get('kind')=='fixed_source_payload_signer_holder_relation']
    premise_formula=z.And(*encoder.constraints,guards);formula=z.And(premise_formula,violation)
    solver=z.Solver();solver.set(timeout=3000,random_seed=0);solver.add(formula)
    smt=solver.to_smt2()
    premise_solver=z.Solver();premise_solver.set(timeout=3000,random_seed=0);premise_solver.add(premise_formula)
    attempt.update(phase='formal_attempted',formal_attempted=True)
    solver_started=perf_counter();premise=bounded_solve(premise_solver);answer=None
    result={'engine':'z3','version':z.get_version_string(),'solver_called':True,'premise':str(premise),
            'query':'not_checked','status':'inconclusive','timeout_ms':3000,
            'semantic_formula_sha256':digest(symbolic),'reason':'premise_not_satisfiable',
            'scope':'same target source path and declared pre-state; no deployed reachability or off-chain-consent proof'}
    if premise==z.sat:
        answer=bounded_solve(solver);result['query']=str(answer)
        result.update(status='supported' if answer==z.sat else 'refuted_in_scope' if answer==z.unsat else 'inconclusive',
                      reason='privileged_holder_interference_satisfiable' if answer==z.sat else
                             'privileged_holder_interference_unsatisfiable' if answer==z.unsat else solver.reason_unknown())
        if answer==z.sat:result['witness']={str(d):str(solver.model()[d]) for d in solver.model().decls()}
    elif premise==z.unknown:result['reason']=premise_solver.reason_unknown()
    if answer==z.sat and encoder.abstract_hash_used and not credential_certificates:
        result.update(status='inconclusive',reason='cryptographic_abstraction_witness_requires_confirmation')
    result.update(smt2=smt,formula_sha256=hashlib.sha256(smt.encode()).hexdigest())
    result['timing_seconds']={'construct_and_solve':perf_counter()-started,'solver_checks':perf_counter()-solver_started}
    attempt.update(phase='formal_returned',status=result['status'],query=result['query'],premise=result['premise'],
        formula_sha256=result['formula_sha256'],timing_seconds=result['timing_seconds'])
    from .m05_formal_diagnostics import diagnostics
    result['model_diagnostics']=diagnostics(premise_formula,violation,formula,solver,answer,smt)
    return {'id':'soq_'+digest({'proposal':obligation['proposal_sha256'],'model':symbolic}),
            'obligation_id':obligation['id'],'rule':rule,'target':obligation['target'],'function':fn,
            'path_index':pi,'holder':owner,'asset_root':model['balance_root'],
            'effect':{'debit':debit['write'],'credit':credit['write'] if credit else None},
            'asset_relation':copy.deepcopy(model),'privilege':priv,'technical_consent':consent,
            'source_model':copy.deepcopy(symbolic),
            'compensation_sources':copy.deepcopy(path.get('native_transfers',[])),
            'consent_sources':certificates,'common_operation':consumed(common,inputs,result),
            'formal':result,'status':result['status'],
            'execution_status':'not_run','evidence_types':['P','M'],
            'policy_scope':'source_derived_financial_interest_and_onchain_consent',
            'source_remarks':copy.deepcopy(obligation['original_proposal']['unresolved']),
            'assumptions':['source-derived asset or conserved transferable ledger; redemption only if established by selected model','current symbolic pre-state',
                           'off-chain authorization is not encoded; model alternatives retained',holder_scope['scope']]+
                           [a for c in credential_certificates for a in c['assumptions']]+symbolic['assumptions'],
            'llm_proposal_sha256':obligation['proposal_sha256']}


def check(obligation,state):
    rule=obligation['rule']
    if rule not in ('FCR-TRANSFER','FCR-DESTROY'):
        return [],[{'reason':'rule_formal_model_not_implemented','rule':rule}]
    base=state['lookups'][obligation['target']]
    lookup,program,extraction_errors=mechanism_program(state,obligation['target'])
    models=asset_models(lookup,program)+proportional_models(lookup,program)
    if not models:return [],[{'reason':'source_financial_interest_not_bound'}]
    rows=[];gaps=[];fn=obligation['function']
    referenced=set(obligation['source_ast_ids'])
    from .m05_relation_consumers import bound_slot_roots
    declared_roots,_=bound_slot_roots(obligation,lookup,'resources')
    referenced |= declared_roots
    # A hypothesis about one resource must not authorize checking another asset
    # merely because it happens to occur in the same function.
    reachable_roots={s['root'] for pi,p in enumerate(program.get(fn,[])) for w in p['writes']
                     if w['source']['ast_id'] in referenced for s in [w['path']]}
    referenced |= reachable_roots
    for model in models:
        if model['balance_root'] not in referenced:
            gaps.append({'reason':'proposal_asset_resource_not_bound','balance_root':model['balance_root']});continue
        for pi,path in enumerate(program.get(fn,[])):
            if path['flow']=='reverted':continue
            try:
                if path['issues']:raise Unsupported('asset_source_path_has_unresolved_semantics')
                if unsafe_integer_cast(path,lookup):raise Unsupported('asset_integer_cast_not_lowered')
                changes=state_changes(path,lookup)
                balances=[d for d in changes if d['write']['path']['root']==model['balance_root']]
                if any(d['delta'] is None for d in balances):
                    raise Unsupported('asset_balance_net_delta_not_encoded')
                debits=[d for d in balances if d['delta'] and all(v<0 for v in d['delta'].values())]
                for debit in debits:
                    if not holder_path(debit['write']['path'],lookup):raise Unsupported('asset_holder_selector_not_bound')
                    amount=negative(debit['delta']);credit=None
                    holder_scope={'kind':'single_holder','conditions':[],'scope':'one declared holder effect'}
                    if rule=='FCR-TRANSFER':
                        credits=[d for d in balances if d['delta']==amount]
                        supply=[d for d in changes if d['write']['path']['root']==model['supply_root']]
                        if len(credits)==1 and len(balances)==2:
                            credit=credits[0]
                            if any(d['delta'] for d in supply):raise Unsupported('transfer_supply_not_conserved')
                        else:
                            from .m05_equity_relations import transfer_scope
                            holder_scope=transfer_scope(balances,supply)
                    else:
                        supply=[d for d in changes if d['write']['path']['root']==model['supply_root']]
                        from .m05_equity_relations import destruction_scope
                        holder_scope=destruction_scope(balances,supply)
                    holder=keys(debit['write']['path'])[0]
                    priv=privilege(path['guards'],lookup,model['balance_root'])
                    from .m05_consent_relations import credential_consent
                    from .m05_equity_relations import linear_quantity
                    recipient=keys(credit['write']['path'])[0] if credit else None
                    if rule=='FCR-TRANSFER' and credit is None:recipient={'kind':'unresolved_split_recipient'}
                    credential=credential_consent(path,holder,linear_quantity(amount),lookup,recipient)
                    if credential:priv+=credential['privilege']
                    # A split transfer cannot consume a single-destination
                    # request as authorization for all recipients.
                    if rule=='FCR-TRANSFER' and credit is None:recipient={'kind':'unresolved_split_recipient'}
                    consent,cert=consent_model(path,holder,amount,lookup,program,model['balance_root'],model['supply_root'],credential,recipient)
                    if not priv and holder.get('kind')!='actual_sender' and not credential:
                        from .m03_p_route import permission_atoms
                        known_roots={model['balance_root'],model.get('supply_root')}
                        for certificate in cert:
                            known_roots.update(s['root'] for s in selectors(certificate))
                        unbound=[a for g in path['guards'] for a in permission_atoms(g,lookup,True) if any(s['root'] not in known_roots for s in selectors(a))]
                        if unbound or path.get('evaluation_gaps'):
                            raise Unsupported('privilege_relation_not_bound_for_external_holder')
                        from .m05_mechanism_core import execution_terms
                        execution_terms(path,lookup)
                        evidence={'analyzer':'source-no-independent-privilege-v1','verified':True,'identity':obligation['identity'],
                            'function':fn,'path_index':pi,'conditions_sha256':digest(path['guards']),
                            'scope':'this complete source path lacks independent privileged control; not an AC safety verdict'}
                        rows.append({'id':'soq_'+digest([obligation['proposal_sha256'],evidence]),'obligation_id':obligation['id'],
                            'rule':rule,'target':obligation['target'],'function':fn,'asset_root':model['balance_root'],'holder':holder,
                            'status':'refuted_in_scope','reportable':False,'program_analysis_certificate':evidence,
                            'formal':{'solver_called':False,'query':'not_required_P','premise':'source_checked','status':'refuted_in_scope','reason':'no_independent_source_privilege'},
                            'source_model':{'kind':'source_no_independent_privilege','guards':path['guards']},
                            'asset_relation':model,'assumptions':['complete supplied source path; no off-source role assumed']})
                        continue
                    rows.append(solve(lookup,model,path,pi,fn,rule,obligation,amount,debit,credit,priv,consent,cert,holder_scope))
            except (Unsupported,ValueError,TypeError,KeyError) as ex:
                gaps.append({'reason':str(ex),'function':fn,'path_index':pi,'asset_root':model['balance_root']})
    if not rows and not gaps:gaps=[{'reason':'no_matching_interference_effect'}]
    return rows,gaps


def interference_formula(encoder, inputs, lookup):
    path={'guards':inputs['guards'],'writes':inputs['writes'],
          'native_transfers':inputs['same_holder_compensation']}
    model=inputs['model']; amount=inputs['amount']; debit=inputs['debit']; credit=inputs['credit']
    priv=inputs['privilege']; consent=inputs['consent']; certificates=inputs['consent_sources']
    z=encoder.z
    guards=z.And(*[encoder.expr(x) for x in path['guards']+inputs['holder_scope']['conditions']])
    credential_certificates=[c for c in certificates if c.get('kind')=='fixed_source_payload_signer_holder_relation']
    if credential_certificates:
        from .m05_credential_validity import same_payload_scope
        same_payload_scope(inputs['successful_evaluation'],*[c['credential'] for c in credential_certificates])
    for evaluated in inputs['successful_evaluation']:encoder.expr(evaluated)
    for certificate in credential_certificates:
        guards=z.And(guards,encoder.expr(certificate['credential'])!=0)
    from .m03_p_lifecycle import leaves
    from .m05_mechanism_core import scalar_write
    # Checked arithmetic in allowance/nonces/other state writes is part of the
    # successful source path too; ignoring it can admit impossible violations.
    for write in path['writes']:
        expanded=leaves(write)
        if not expanded:raise Unsupported('asset_path_write_not_scalarized')
        for leaf in expanded:encoder.expr(scalar_write(leaf,lookup)['value'])
    from .m05_equity_relations import linear_quantity
    amount_expr=linear_quantity(amount)
    quantity=encoder.expr(amount_expr)
    owner=keys(debit['write']['path'])[0]
    before=encoder.expr(debit['write']['path']);after=encoder.expr(debit['write']['value'])
    # No arbitrary unprivileged caller is assigned an administrative role. The
    # effective privilege is a formula from the original path itself.
    is_privileged=z.Or(*[encoder.expr(x) for x in priv]) if priv else z.BoolVal(False)
    basis=inputs['compensation_basis']
    compensation=[]
    for payment in basis['payments']:
        compensation.append(z.If(z.And(encoder.expr(payment['recipient'])==encoder.expr(owner),
                                        encoder.expr(payment['success'])),encoder.expr(payment['amount']),0))
    paid=z.Sum(*compensation) if compensation else z.IntVal(0)
    lost_value=encoder.expr(basis['entitlement_value'])
    violation=z.And(quantity>0,before-after==quantity,lost_value>paid,is_privileged,z.Not(encoder.expr(consent)))
    if credit:
        recipient=keys(credit['write']['path'])[0]
        violation=z.And(violation,encoder.expr(owner)!=encoder.expr(recipient),
                        encoder.expr(credit['write']['value'])-encoder.expr(credit['write']['path'])==quantity)
    elif inputs['holder_scope']['kind']=='bounded_conserved_transfer':
        # Check actual net increases/decreases too, not only the polynomial
        # certificate. The common model supplies the same source writes.
        scope=inputs['holder_scope']
        increases=[encoder.expr(c['write']['value'])-encoder.expr(c['write']['path']) for c in scope['credits']]
        decreases=[encoder.expr(d['write']['path'])-encoder.expr(d['write']['value']) for d in scope['debits']]
        violation=z.And(violation,z.Sum(*increases)==z.Sum(*decreases),
                        *[x>0 for x in increases+decreases])
    return guards,violation
