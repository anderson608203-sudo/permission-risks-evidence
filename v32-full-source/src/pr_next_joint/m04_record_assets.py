"""Record-shaped redeemable entitlement, linked by holder/payout/liability.

Uses original record fields and state deltas. A record name, function name or
amount field alone cannot establish an asset. Integer amounts remain exact.
"""
from .core import digest
from .m03_p_paths import key,op,lit,conditions_possible,walk

def analyze_records(bundle,lookup,program,requested):
    from .m03_p_assets import deltas,polynomial,negative
    from .m03_p_route import keys,fields,selectors,value_type,effective_permission
    models=[];rows=[];alternatives=[]
    for fn,paths in program.items():
        for pi,path in enumerate(paths):
            if path['issues'] or path['flow']=='reverted':continue
            for pay in path.get('native_transfers',[]):
                amount=pay['amount']
                if amount.get('kind')!='storage' or not fields(amount) or not keys(amount) or pay['recipient']!={'kind':'actual_sender'}:continue
                if conditions_possible(path['guards'],pay['success']):continue
                holders=[]
                for g in path['guards']:
                    for s in selectors(g):
                        if s['root']!=amount['root'] or key(keys(s))!=key(keys(amount)) or value_type(s,lookup) not in ('address','address payable'):continue
                        if not conditions_possible(path['guards'],op('==',pay['recipient'],s)):holders.append(s)
                if len({key(x) for x in holders})!=1:continue
                reductions=[x['write'] for x in deltas(path) if not x['write']['path'].get('segments') and x['delta']==negative(polynomial(amount))]
                if len(reductions)!=1:continue
                models.append({'kind':'record_native_entitlement','balance_root':amount['root'],'supply_root':reductions[0]['path']['root'],
                               'face_field':fields(amount)[-1],'holder_field':fields(holders[0])[-1],
                               'redemption_function':fn,'native_payment':pay,'holder':holders[0],'liability_reduction':reductions[0],
                               'basis':'same-record authenticated holder native payout and matched scalar liability reduction'})
    models=list({(m['balance_root'],m['supply_root']):m for m in models}.values())
    for model in models:
        for fn,paths in program.items():
            for pi,path in enumerate(paths):
                if path['flow']=='reverted':continue
                # An authenticated holder may transfer the whole existing
                # record; this does not issue a fresh entitlement or require
                # the issuer to become the holder.
                from .m03_p_route import relocate
                owner_writes=[w for w in path['writes'] if w['path']['root']==model['balance_root'] and fields(w['path'])==[model['holder_field']]]
                if not path['issues'] and len(owner_writes)==1:
                    owner_write=owner_writes[0]
                    try:holder=relocate(model['holder'],model['holder'],owner_write['path'])
                    except ValueError:holder=None
                    others=[w for w in path['writes'] if w is not owner_write and w['path']['root'] in (model['balance_root'],model['supply_root'])]
                    if holder is not None and not others and not conditions_possible(path['guards'],op('==',{'kind':'actual_sender'},holder)):
                        alternatives.append({'function':fn,'path_index':pi,'reason':'authenticated_holder_transfers_existing_record_without_new_face_or_liability',
                            'balance_root':model['balance_root'],'supply_root':model['supply_root'],'effect_sources':[owner_write['source']['ast_id']]})
                for w in path['writes']:
                    if w['path']['root']!=model['balance_root'] or w['value'].get('kind')!='record':continue
                    vals={x['field']:x['value'] for x in w['value']['fields']}
                    amount=vals.get(model['face_field']);holder=vals.get(model['holder_field'])
                    if amount is None or holder is None:continue
                    supply=[x for x in deltas(path) if x['write']['path']['root']==model['supply_root']]
                    matched=len(supply)==1 and supply[0]['delta']==polynomial(amount)
                    privilege=effective_permission(path['guards'],lookup)
                    backed=amount=={'kind':'transaction_value','type':'uint256'} and lookup.function(fn).get('stateMutability')=='payable'
                    status='inconclusive';reason='record_entitlement_creation_not_closed'
                    if not path['issues'] and matched:
                        if backed:status='refuted_in_scope';reason='record_face_equals_fresh_native_deposit'
                        elif privilege and not conditions_possible(path['guards'],op('>',amount,lit(0))):status='supported';reason='privileged_creation_of_source_bound_redeemable_record'
                    synthetic=bundle.get('material_origin','compiler_artifacts')!='compiler_artifacts'
                    row={'schema':'m03-p-result-v2','route':'P','rule':'FCR-MINT','status':status,'reason':reason,'function':fn,'subject':'actual_sender',
                         'structure':model['kind'],'program_id':bundle['program_id'],'build_id':bundle['build_id'],'policy_scope':'program_derived_asset_model',
                         'required_policy_candidate':{'kind':'privileged_asset_creation','balance_root':model['balance_root'],'supply_root':model['supply_root']},
                         'policy_basis':{'asset_model':model,'privilege_conditions':privilege,'face':amount,'holder':holder,'matched_liability':matched,'fresh_native_backing':backed},
                         'effect':{'object':lookup.nodes[w['path']['root']]['name'],'selector':w['path'],'value':w['value'],'operator':w['operator'],'source':w['source']},
                         'ledger_effects':[w],'supply_effects':[x['write'] for x in supply],'path_index':pi,'conditions':path['guards'],'issues':path['issues'],
                         'execution_status':'not_run','solver_status':'not_called','no_execution_required':True,'reportable':status=='supported' and not synthetic,
                         'diagnostic_only':synthetic,'material_origin':bundle.get('material_origin','compiler_artifacts'),'source_remarks':[],
                         'limitations':['source-bound record holder/face/native payout/liability only','no solvency, deployment or transaction confirmation'],
                         'coverage':'declared record creation and redemption relationships','not_a_safety_conclusion':True}
                    row['id']=digest({k:row[k] for k in ('program_id','build_id','rule','function','effect','conditions','required_policy_candidate')})
                    if not requested or any(p.get('rule')=='FCR-MINT' and p.get('function')==fn for p in requested):rows.append(row)
                    if backed:alternatives.append({'function':fn,'path_index':pi,'reason':'public_deposit_creates_equal_face_record','balance_root':model['balance_root'],'supply_root':model['supply_root'],'effect_sources':[w['source']['ast_id']]+[x['write']['source']['ast_id'] for x in supply]})
    return rows,models,alternatives
