"""D02: source-bound destruction of currently valid third-party entitlements.
Historical AC EVM is explicit; no source-only claim about a modern deployment.
"""
import copy
from .core import digest
from .m03_p_paths import key,op,lit,walk
from .m03_p_route import keys,effective_permission
from .m05_state_relations import compose_read
from .m04_logic import Unsupported
from .m22_assets import identity as asset_identity

PROFILE='historical_AC_pre_eip_6780'
HOLDER={'kind':'parameter','id':-999000001,'type':'address','model_role':'existential_source_entitlement_holder'}
SENDER={'kind':'actual_sender'}

def claim_scope(v):
    if isinstance(v,dict):
        if v.get('kind')=='actual_sender':return copy.deepcopy(HOLDER)
        if v.get('kind')=='parameter':return {**v,'id':-1000000000-abs(v['id']),'model_role':'source_claim_parameter'}
        return {k:claim_scope(x) for k,x in v.items()}
    return [claim_scope(x) for x in v] if isinstance(v,list) else v


def witnesses(tid,lookup,program,shared,limits):
    from .m05_equity_relations import linear_quantity
    from .m20_policy import own_native_claim
    result=[]
    for n in shared.get(tid,{}).get('normal_transfers',[]):
        if n.get('holder')!=SENDER:continue
        p=program[n['function']][n['path_index']]
        a=next((a for a in shared[tid]['assets'] if a['balance_root']==n['root'] and a['balance_effect']['path'].get('instance')==n.get('instance') and (not n.get('asset_identity') or asset_identity(a['balance_effect']['path'])==n['asset_identity'])),None)
        if not a or a['balance_effect']['path'].get('instance'):continue
        from .m05_asset_registry import initial_state
        initial=a.get('initial_state') or initial_state(lookup,program,a['balance_root'])
        if initial.get('status')=='closed_zero_invariant':
            limits.append({'phase':'D02_entitlement_witness','target':tid,'function':n['function'],
                'reason':'source_proved_zero_ledger_has_no_current_entitlement','certificate':initial});continue
        prototype=a['balance_effect']['path']
        if len(keys(prototype))!=1:continue
        selector={**prototype,'segments':[{'key':SENDER} if 'key' in s else s for s in prototype['segments']]}
        try:quantity=linear_quantity(n['total_debit'])
        except (Unsupported,ValueError) as ex:
            limits.append({'phase':'D02_entitlement_witness','target':tid,'function':n['function'],'reason':str(ex)});continue
        result.append({'kind':'source_holder_transferable_entitlement','function':n['function'],'path_index':n['path_index'],
            'selector':selector,'asset':a,'path':p,'positive_quantity':quantity,
            'effect_sources':n['effect_sources']})
    # A source-proved own-record debit and native payout supplies a currency
    # claim without inventing a token supply or economic price.
    for fn,paths in program.items():
        for pi,p in enumerate(paths):
            if p['flow'] not in ('normal','returned') or p['issues'] or p.get('evaluation_gaps'):continue
            for effect in p.get('native_transfers',[]):
                try:cert=own_native_claim(p,lookup,effect)
                except (Unsupported,ValueError) as ex:
                    limits.append({'phase':'D02_entitlement_witness','target':tid,'function':fn,'reason':str(ex)});continue
                if not cert or cert['selector'].get('instance'):continue
                result.append({'kind':'source_native_redemption_claim','function':fn,'path_index':pi,
                    'selector':cert['selector'],'path':p,'positive_quantity':effect['amount'],'native_claim':cert,
                    'effect_sources':[effect['source'],cert['debit_source']]})
    return list({key([w['kind'],w['function'],w['path_index'],w['selector']]):w for w in result}.values())


def unresolved_authorization(path,lookup,entitlement_selector):
    """Do not equate an unmodeled source authorization with no authorization.
    Preserve the candidate and exact condition for later review. These facts
    are NOT certificates of legitimate policy, even if they prevent this alarm.
    """
    from .m03_p_paths import normalize
    from .m03_p_route import value_type,permission_atoms,fields
    evidence=[]
    for raw in path['guards']:
        guard=normalize(raw)
        for node in walk(guard):
            if node.get('kind')!='op' or node.get('op') not in ('>=','>','<=','<','=='):continue
            from .m22_record_roles import numeric_atom
            if numeric_atom(node,lookup):continue
            for a in node.get('args',[]):
                if a.get('kind')!='storage':continue
                if a.get('root')==entitlement_selector.get('root') and fields(a)==fields(entitlement_selector) and a.get('instance')==entitlement_selector.get('instance'):continue
                if not any(x.get('kind')=='actual_sender' for x in walk(keys(a))):continue
                if value_type(a,lookup).startswith(('uint','int')):
                    evidence.append({'kind':'caller_indexed_numeric_condition','condition':guard,'record':a,
                        'reason':'numeric role, ticket or credential must be distinguished from ordinary data before asserting absent authorization'})
        # A source owner-or-price branch is a visible paid-operation policy.
        # Do not discard its paid branch and re-invent owner-only authorization.
        if guard.get('kind')=='op' and guard.get('op') in ('or','||') and permission_atoms(guard,lookup):
            for node in walk(guard):
                if node.get('kind')!='op' or node.get('op') not in ('>=','>','<=','<'):continue
                args=node.get('args',[])
                if len(args)!=2:continue
                if node['op'] in ('<=','<'):args=args[::-1]
                paid,price=args
                if paid.get('kind')!='transaction_value':continue
                eligible=(price.get('kind')=='literal' and type(price.get('value')) is int and price['value']>0) or (price.get('kind')=='storage' and not keys(price) and value_type(price,lookup).startswith('uint'))
                if eligible:evidence.append({'kind':'explicit_authority_or_paid_shutdown','condition':guard,'price':price,
                    'reason':'visible source public termination alternative; lack of authorization is not established'})
    return list({key(x):x for x in evidence}.values())


def duties(context,state,shared,index):
    from .source_entry_identity import builtin_call
    rows=[];limits=[]
    for tid,lookup in state['lookups'].items():
        program={f:ps for (t,f),ps in state['paths'].items() if t==tid}
        try:claims=witnesses(tid,lookup,program,shared,limits)
        except (Unsupported,ValueError) as ex:
            claims=[];limits.append({'phase':'D02_entitlement_witness','target':tid,'reason':str(ex)})
        for r in index.by_target[tid]:
            effect=r['effect']
            if effect.get('kind')!='native_selfdestruct':continue
            p=program[r['function']][r['path_index']]
            if not builtin_call(lookup.nodes.get(effect['source']['ast_id'],{}),lookup,('selfdestruct','suicide')):continue
            if p['issues'] or p.get('evaluation_gaps'):
                limits.append({'phase':'D02_destruction','target':tid,'function':r['function'],'reason':'destruction_path_dependencies_unresolved'});continue
            if not claims:
                limits.append({'phase':'D02_destruction','target':tid,'function':r['function'],'reason':'no_source_valid_third_party_entitlement_witness'});continue
            # A native compensation paid during shutdown needs its own matching
            # settlement model; do not erase or ignore it to manufacture risk.
            # Match native claims in their source units; token/native exchange
            # rates remain unsupported without an explicit conversion model.
            for witness in claims:
                try:
                    if p.get('native_transfers') and witness['kind']!='source_native_redemption_claim':
                        limits.append({'phase':'D02_destruction','target':tid,'function':r['function'],'reason':'token_shutdown_native_compensation_rate_not_established'});continue
                    before=claim_scope(witness['selector']);remaining=compose_read(before,p['writes'],lookup)
                    compensation=lit(0);payment_evidence=[]
                    for pay in p.get('native_transfers',[]):
                        # Do not ignore a conditional failed payment or infer
                        # payment success from the existence of a call.
                        from .m09_shared_policy import implies
                        if not implies(lookup,p,pay['success']):raise Unsupported('shutdown_payment_success_unresolved')
                        piece={'kind':'conditional','condition':op('==',pay['recipient'],HOLDER),
                               'when_true':pay['amount'],'when_false':lit(0),'type':'uint256'}
                        compensation=op('+',compensation,piece);payment_evidence.append(copy.deepcopy(pay))
                    validity=claim_scope(witness['path']['guards'])
                    amount=claim_scope(witness['positive_quantity'])
                    # A record deletion is not settlement. Entry rights persist unless
                    # a source-grounded payment/expiry model discharges them.
                    # Time/business validity is evaluated at entry. An attacker
                    # cannot erase a valid claim by flipping a pause/closed bit
                    # immediately before destroying the backing contract.
                    active=op('and',*validity,op('>',amount,lit(0)),op('>',before,lit(0)),
                              op('!=',HOLDER,SENDER),op('!=',HOLDER,lit(0)),op('!=',HOLDER,lookup.read_calls.address()))
                    if witness['kind']=='source_native_redemption_claim':
                        # A shutdown paying this holder is not asserted harmful
                        # without a separately checked shortfall/other holder.
                        active=op('and',active,op('!=',HOLDER,effect['recipient']),op('>',before,compensation))
                    permissions=effective_permission(p['guards'],lookup)
                    auth_unknown=unresolved_authorization(p,lookup,before)
                    required=op('or',*permissions,op('!',active))
                    safe_witness={k:v for k,v in witness.items() if k!='path'}
                    transformed={**copy.deepcopy(effect),'kind':'source_entitlement_contract_destruction',
                        'execution_environment':PROFILE,'source_destroy_kind':'native_selfdestruct',
                        'scope':'deletion of source-bound code/storage backing valid third-party entitlement under approved historical AC EVM'}
                    basis={'basis':'source_valid_third_party_entitlement_destruction','approval':'D02',
                        'entitlement':safe_witness,'holder':HOLDER,'entry_validity':validity,
                        'entry_entitlement':before,'post_record':remaining,'active_third_party_claim':active,
                        'source_native_compensation':compensation,'settlement_payments':payment_evidence,
                        'local_authorizations':permissions,'execution_environment':PROFILE,
                        'preceding_created_calls':copy.deepcopy(p.get('bounded_external_effects',[])),
                        'unresolved_source_authorization':auth_unknown,
                        'modern_evm_limit':'EIP-6780 normally preserves code/storage unless created in the same transaction',
                        'scope':'conditional source prestate; no deployment-prefix or actual monetary-loss proof'}
                    q={'rule':'AC-01','target':tid,'function':r['function'],'path_index':r['path_index'],
                       'conditions':copy.deepcopy(p['guards']),'issues':copy.deepcopy(p['issues']),
                       'effect':transformed,'required_policy_candidate':required,'policy_basis':basis,
                       'source_evaluation_terms':copy.deepcopy(p.get('evaluated_terms',[]))+claim_scope(witness['path'].get('evaluated_terms',[])),
                       'program_id':context['identity']['program_id'],'build_id':context['identity']['build_id'],
                       'effect_id':r['id'],'sequence_extension_disabled':'D02 validity state must retain its explicit entry/settlement binding'}
                    if auth_unknown:
                        issue={'reason':'D02_applicable_authorization_not_established','source_evidence':auth_unknown,'not_safety_certificate':True}
                        q['issues'].append(issue);limits.append({'phase':'D02_authorization','target':tid,'function':r['function'],**issue})
                    q['id']='q_'+digest(q);rows.append(q);index.use(r,'D02_third_party_entitlement_destruction',q['id'])
                except (Unsupported,ValueError) as ex:
                    limits.append({'phase':'D02_entitlement_binding','target':tid,'function':r['function'],'reason':str(ex)})
    return rows,limits


def terminal_created_call(calls,node,target,cid,instance,args):
    """Exact one-statement terminal callee, not general external-call success."""
    p=calls.p;s=p.current
    if getattr(p,'analysis_scope',None)!='AC':return None
    proof=calls.instances.get(key(instance),{})
    if proof.get('binding') not in ('immutable_direct_new','constructor_single_assignment_direct_new'):return None
    # A write in a derived contract can invalidate a base constructor binding.
    # Check all concrete root bases, not just the member's declaring contract.
    from .source_entry_identity import function_kind
    bases=p.contract_node.get('linearizedBaseContracts',[p.contract_node['id']])
    for base in bases:
        for fn in p.nodes[base].get('nodes',[]):
            if fn.get('nodeType')!='FunctionDefinition' or function_kind(fn)=='constructor':continue
            for n in walk(fn):
                changed=n.get('leftHandSide',{}) if n.get('nodeType')=='Assignment' else n.get('subExpression',{}) if n.get('nodeType')=='UnaryOperation' and n.get('operator')=='delete' else {}
                if changed.get('referencedDeclaration')==instance['reference']:return None
    if target.get('modifiers') or target.get('parameters',{}).get('parameters') or args or target.get('returnParameters',{}).get('parameters'):return None
    body=(target.get('body') or {}).get('statements',[])
    if len(body)!=1 or body[0].get('nodeType')!='ExpressionStatement':return None
    expr=body[0].get('expression',{})
    from .source_entry_identity import builtin_call
    if not builtin_call(expr,p,('selfdestruct','suicide')) or len(expr.get('arguments',[]))!=1:return None
    arg=expr['arguments'][0]
    # A literal target is fully evaluated with no storage/call side effects.
    literal=arg
    while literal.get('nodeType')=='FunctionCall' and literal.get('kind')=='typeConversion' and len(literal.get('arguments',[]))==1:
        literal=literal['arguments'][0]
    if literal.get('nodeType')!='Literal' or literal.get('kind')!='number':return None
    saved=(calls.active_contract,calls.instance,p.sender)
    try:
        calls.active_contract,calls.instance,p.sender=cid,instance,calls.address()
        recipient=p.value(arg,{})
    finally:calls.active_contract,calls.instance,p.sender=saved
    live={'kind':'parameter','id':-2000000000-int(instance['reference']),'type':'bool',
          'model_role':'created_callee_code_available','instance':instance}
    s['guards'].append(live)
    s.setdefault('bounded_external_effects',[]).append({'kind':'created_instance_terminal_destruction',
        'call_source':p.anchor(node),'callee_source':p.anchor(expr),'callee_instance':copy.deepcopy(instance),
        'recipient':recipient,'callee_sender':calls.address(),'binding':proof,'successful_call_condition':live,
        'scope':'source-bound live created callee; one terminal instruction; no callback/parent writes; child effects retained separately'})
    # Callee termination returns to caller. Never terminate the parent path.
    return lit(True)
