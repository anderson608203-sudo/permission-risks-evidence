"""Source-derived transferable ledgers; names/events are not asset evidence."""
import copy
from .m05_writer_scope import gaps_for
from .core import digest
from .m04_logic import Unsupported
from .m03_p_paths import key,walk,op,lit,conditions_possible
from .m03_p_route import keys,selectors,effective_permission


def roots(model):
    return {model['balance_root']} | ({model['supply_root']} if model.get('supply_root') is not None else set())


def initial_state(lookup,program,root):
    """Prove only the simple closed-zero invariant; otherwise keep conditions.

    No absence-of-mint name heuristic, and no guessed deployment or balance.
    Every source write must be covered; indirect/assembly writes defeat proof.
    """
    from .m03_p_assets import deltas,add
    bases=set(lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']]))
    declarations=[n for n in lookup.nodes.values() if n.get('nodeType')=='ContractDefinition' and n.get('id') in bases]
    tree=[n for declaration in declarations for n in walk(declaration)]
    writes=[]
    for node in tree:
        left=node.get('leftHandSide') if node.get('nodeType')=='Assignment' else node.get('subExpression') if node.get('nodeType')=='UnaryOperation' and node.get('operator') in ('++','--','delete') else None
        if left and any(n.get('referencedDeclaration')==root for n in walk(left)):writes.append(node['id'])
    all_paths=[p for ps in program.values() for p in ps]
    known={w['source']['ast_id'] for p in all_paths for w in p['writes'] if w['path']['root']==root}
    reasons=[]
    if not writes or not set(writes)<=known:reasons.append('not_all_source_writes_modeled_including_constructors')
    if lookup.nodes[root].get('value') is not None:reasons.append('source_initializer_requires_evaluation')
    if any(p['issues'] or p['flow']=='truncated' for p in all_paths):reasons.append('program_semantics_incomplete')
    if gaps_for(lookup,{root}):reasons.append('writer_inventory_incomplete')
    if any(n.get('nodeType')=='InlineAssembly' or n.get('memberName') in ('delegatecall','callcode') for n in tree):reasons.append('indirect_storage_effects')
    for path in all_paths:
        if path['flow']=='reverted':continue
        total={}
        for change in deltas(path):
            if change['write']['path']['root']==root:total=add(total,change['delta'])
        if total is None or total:reasons.append('possible_creation_or_nonconserving_source_write');break
    closed=not reasons
    return {'status':'closed_zero_invariant' if closed else 'conditional_source_prestate',
        'source_write_ast_ids':sorted(set(writes)),'reasons':sorted(set(reasons)),
        'scope':'zero-initialized mapping plus complete conserving source writers' if closed else
            'no deployed reachability claim; explicit source state conditions retained'}


def transferable_models(lookup,program):
    from .m03_p_assets import deltas,negative,holder_path,term,add
    models={}
    for fn,paths in program.items():
        for pi,path in enumerate(paths):
            if path['flow'] not in ('normal','returned') or path['issues'] or path.get('native_transfers'):continue
            changes=deltas(path)
            for debit in changes:
                selector=debit['write']['path'];delta=debit['delta']
                if not holder_path(selector,lookup) or not delta or not all(v<0 for v in delta.values()):continue
                if (selector['root'],key(selector.get('instance'))) in models:continue
                holder=keys(selector)[0];own=op('==',{'kind':'actual_sender'},holder)
                # Transferability and caller privilege are independent checks.
                holder_controlled=(holder.get('kind')=='actual_sender' or not conditions_possible(path['guards'],own))
                balances=[c for c in changes if c['write']['path']['root']==selector['root']
                    and c['write']['path'].get('instance')==selector.get('instance')]
                credits=[c for c in balances if c['delta'] and all(v>0 for v in c['delta'].values())]
                total={}
                for c in balances:total=add(total,c['delta'])
                witness=None
                if len(credits)<1 or len(balances)!=len(credits)+1 or total!={} or term(negative(delta)) is None:
                    try:
                        from .m18_asset_witness import fee_witness
                        witness=fee_witness(lookup,path,debit,balances,changes)
                    except (ValueError, Unsupported) as error:
                        lookup.__dict__.setdefault('_asset_witness_limits',[]).append({'function':fn,'path':pi,'root':selector['root'],'reason':str(error)})
                        witness=None
                    if witness is None:
                        lookup.__dict__.setdefault('_asset_witness_limits',[]).append({'function':fn,'path':pi,'root':selector['root'],'reason':'transfer_witness_conservation_or_positive_credit_not_established'})
                        continue
                    credits=witness['credits']
                if any(key(keys(c['write']['path'])[0])==key(holder) for c in credits):continue
                root=selector['root'];identity=(root,key(selector.get('instance')))
                model={'kind':'source_transferable_ledger','balance_root':root,'supply_root':None,
                    'supply_effect':None,'supply_authoritative':False,
                    'basis':'source_same_unit_address_ledger_debit_and_credit',
                    'holder_controlled_transfer_witness':holder_controlled,
                    'balance_effect':copy.deepcopy(debit['write']),'transfer_credit':copy.deepcopy(credits[0]['write']),
                    'transfer_credits':[copy.deepcopy(c['write']) for c in credits],
                    'transfer_function':fn,'path_index':pi,'redemption_function':None,
                    'conditions':copy.deepcopy(path['guards']),
                    'unit_relation':'same-source transferable ledger units; no native conversion assumed',
                    'initial_state':initial_state(lookup,program,root),
                    'scope':'source-defined transferable balance; no price, liquidity or solvency claim'}
                if witness:model['transfer_witness']=copy.deepcopy(witness);model['basis']=witness['basis']
                model['id']='asset_'+digest(model);models.setdefault(identity,model)
    return list(models.values())


def mint_rows(bundle,lookup,program,model,requested):
    """Generate source models; the joint route subsequently performs M4 checks."""
    from .m03_p_assets import deltas,add
    rows=[];alternatives=[];root=model['balance_root']
    for fn,paths in program.items():
        for pi,path in enumerate(paths):
            if path['flow'] not in ('normal','returned'):continue
            balances=[d for d in deltas(path) if d['write']['path']['root']==root]
            if not balances:continue
            matches=[p for p in requested if p.get('rule')=='FCR-MINT' and p.get('function')==fn]
            if requested and not matches:continue
            delta={}
            for change in balances:delta=add(delta,change['delta'])
            privilege=[g for g in effective_permission(path['guards'],lookup) if selectors(g) and all(s['root']!=root for s in selectors(g))]
            effect=balances[0]['write']
            issues=copy.deepcopy(path['issues'])
            if delta is None:issues.append({'reason':'transferable_ledger_net_change_not_linear'})
            if path.get('native_transfers'):issues.append({'reason':'transferable_ledger_external_compensation_unmodeled'})
            row={'schema':'m03-p-result-v2','route':'P','rule':'FCR-MINT','function':fn,'path_index':pi,
                'subject':'actual_sender','structure':model['kind'],'program_id':bundle['program_id'],'build_id':bundle['build_id'],
                'policy_scope':'program_derived_asset_model','required_policy_candidate':{'kind':'privileged_asset_creation','balance_root':root,'supply_root':None},
                'policy_basis':{'asset_model':copy.deepcopy(model),'ledger_delta':delta,'supply_delta':None,
                    'privilege_conditions':privilege,'ordinary_route':'source_conserved_transfer' if delta=={} else None},
                'effect':{'object':lookup.nodes[root]['name'],'selector':effect['path'],'value':effect['value'],'operator':effect['operator'],'source':effect['source']},
                'ledger_effects':[d['write'] for d in balances],'supply_effects':[],
                'conditions':copy.deepcopy(path['guards']),'issues':issues,
                'status':'inconclusive','reason':'transferable_asset_model_requires_joint_M4',
                'reportable':False,'execution_status':'not_run','solver_status':'not_called',
                'material_origin':bundle.get('material_origin','compiler_artifacts'),
                'source_remarks':[p.get('unresolved',[]) for p in matches],
                'limitations':['source transferable ledger, no market value or deployed reachability proof'],
                'not_a_safety_conclusion':True}
            row['id']=digest(row);rows.append(row)
            if delta=={} and any(keys(d['write']['path'])[0].get('kind')=='actual_sender' and d['delta'] and all(v<0 for v in d['delta'].values()) for d in balances):
                alternatives.append({'function':fn,'path_index':pi,'reason':'holder_moves_own_balance_with_conserved_total',
                    'balance_root':root,'supply_root':None,'source':path['entry_source'],
                    'effect_sources':[d['write']['source']['ast_id'] for d in balances],
                    'decision':'source-bound public holder operation; not peer issuer exclusivity'})
    return rows,alternatives
