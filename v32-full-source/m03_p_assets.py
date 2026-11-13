"""Conditional native-redeemable ledger model for the FCR-MINT P route.

Infer asset identity from address-indexed debit and same-holder native payout,
plus a matching scalar supply reduction. No variable/function-name heuristics.
The source relation is not execution, reserve solvency, or callback validation.
"""
import copy
from .source_entry_identity import elementary_expression_name
from .core import digest
from .m03_p_paths import Paths,key,walk,clean,op,lit,normalize,conditions_possible


class AssetPaths(Paths):
    def evaluate(self,n,env):
        if n and n.get('nodeType')=='MemberAccess':
            base=n.get('expression',{})
            if base.get('nodeType')=='Identifier' and base.get('name')=='msg' and n['memberName']=='value':
                return {'kind':'transaction_value','type':'uint256'}
            if n['memberName']=='balance' and self.value(base,env).get('kind')=='contract_address':
                return {'kind':'native_reserve','instance':self.value(base,env)}
        if n and n.get('nodeType')=='FunctionCall':
            from .m11_calls import native_call
            result=native_call(self,n,env)
            if result is not None:return result
            options=n.get('expression',{});member=options.get('expression',{})
            from .source_entry_identity import builtin_call
            if builtin_call(n,self,('selfdestruct','suicide')):
                args=n.get('arguments',[])
                if len(args)==1:
                    recipient=self.value(args[0],env)
                    effect={'kind':'native_selfdestruct','recipient':recipient,
                        'amount':{'kind':'native_reserve','instance':self.read_calls.address()},
                        'source':self.anchor(n),'scope':'native balance disposition; code/storage destruction depends on EVM revision'}
                    self.current.setdefault('sensitive_effects',[]).append(effect)
                    self.current['flow']='returned'
                    self.current['_evm_halted']=True
                    return {'kind':'literal','value':True}
            if options.get('nodeType')=='MemberAccess' and options.get('memberName') in ('transfer','send'):
                typ=options.get('expression',{}).get('typeDescriptions',{}).get('typeString','')
                if typ in ('address','address payable') and len(n.get('arguments',[]))==1:
                    recipient=self.value(options['expression'],env);amount=self.value(n['arguments'][0],env)
                    success={'kind':'native_call_success','source_id':n['id']}
                    effect={'kind':'native_transfer','recipient':recipient,'amount':amount,'success':success,
                        'source':self.anchor(n),'scope':'source native payout conditional on successful external call'}
                    self.current.setdefault('native_transfers',[]).append(copy.deepcopy(effect))
                    self.current.setdefault('sensitive_effects',[]).append(effect)
                    if options['memberName']=='transfer':self.current['guards'].append(success)
                    return success
            from .m18_code_control import builtin_delegate
            if builtin_delegate(options,self):
                # Evaluate invocation arguments before claiming the call is
                # reachable. A pure literal hash selector cannot revert; its
                # numeric value is irrelevant to target controllability.
                from .m18_code_control import literal_selector
                for argument in n.get('arguments',[]):
                    if literal_selector(argument,self):continue
                    value=self.value(argument,env)
                    if any(x.get('kind') in ('unknown','call_unresolved') for x in walk(value)):
                        self.current['issues'].append({'reason':'delegate_argument_not_lowered','source':self.anchor(argument)})
                    if any(x.get('kind')=='index' for x in walk(value)):
                        self.current.setdefault('evaluated_terms',[]).append(copy.deepcopy(value))
                effect={'kind':'dangerous_external_call','recipient':self.value(options['expression'],env),
                    'source':self.anchor(n),'scope':'external behavior not resolved',
                    'prefix_conditions':copy.deepcopy(self.current['guards']),
                    'prefix_issues':copy.deepcopy(self.current['issues']),
                    'prefix_evaluation_terms':copy.deepcopy(self.current.get('evaluated_terms',[]))}
                self.current.setdefault('sensitive_effects',[]).append(effect)
                self.current['issues'].append({'reason':'dangerous_external_effect_not_resolved','source':self.anchor(n)})
                success={'kind':'native_call_success','source_id':n['id']}
                effect['success']=success
                if n.get('typeDescriptions',{}).get('typeString')=='bool':return success
                return {'kind':'tuple','items':[success,{'kind':'native_return_data','source_id':n['id']}]}

            if options.get('nodeType')=='FunctionCallOptions' and member.get('nodeType')=='MemberAccess' and member.get('memberName')=='call':
                args=n.get('arguments',[])
                if options.get('names')==['value'] and len(args)==1 and args[0].get('nodeType')=='Literal' and args[0].get('value')=='':
                    recipient=self.value(member['expression'],env);amount=self.value(options['options'][0],env)
                    success={'kind':'native_call_success','source_id':n['id']}
                    self.current.setdefault('native_transfers',[]).append({'recipient':recipient,'amount':amount,'success':success,'source':self.anchor(n),
                        'scope':'source payout relation, conditional on success; external recipient behavior not executed'})
                    self.current.setdefault('sensitive_effects',[]).append({'kind':'native_transfer','recipient':recipient,
                        'amount':amount,'success':success,'source':self.anchor(n),
                        'scope':'conditional native transfer; callee behavior not executed'})
                    return {'kind':'tuple','items':[success,{'kind':'native_return_data','source_id':n['id']}]}
        return super().evaluate(n,env)

    def statement(self,n,s,depth):
        if n and n.get('nodeType')=='VariableDeclarationStatement' and len(n.get('declarations',[]))==1 and (n.get('initialValue') or {}).get('nodeType')=='Conditional':
            expr=n['initialValue'];condition=self.expr(expr['condition'],s);out=[]
            for sign,name in ((True,'trueExpression'),(False,'falseExpression')):
                child=copy.deepcopy(s);child['guards'].append(condition if sign else op('!',condition))
                if conditions_possible(child['guards']):
                    selected=copy.deepcopy(n);selected['initialValue']=expr[name];out.extend(self.statement(selected,child,depth))
            return out
        if n and n.get('nodeType')=='VariableDeclarationStatement' and len(n.get('declarations',[]))>1:
            v=self.expr(n.get('initialValue'),s)
            for i,d in enumerate(n['declarations']):
                if d:s['env'][d['id']]=v['items'][i] if v.get('kind')=='tuple' and i<len(v['items']) else {'kind':'unknown','reason':'tuple_local'}
            return [s]
        return super().statement(n,s,depth)


def polynomial(v):
    """Exact additive form with opaque checked products/quotients; no floor reassociation."""
    v=normalize(v)
    if v.get('kind')=='literal' and type(v.get('value')) is int:return {'#':v['value']}
    if v.get('kind') in ('parameter','storage','transaction_value'):
        return {key(v):1}
    if v.get('kind')=='conditional' and str(v.get('type','')).startswith('uint'):
        # Preserve the exact branch expression as an opaque quantity. M4 must
        # encode both the condition and selected-branch evaluation constraints.
        return {key(v):1}
    if (v.get('kind')=='index' and v.get('base',{}).get('kind')=='parameter'
            and '[' in v['base'].get('type','')
            and v['base']['type'].split('[')[0].startswith('uint')
            and v.get('key',{}).get('kind')=='literal'
            and type(v['key'].get('value')) is int and v['key']['value']>=0):
        # Exact element of an already expanded finite path. The encoder keeps
        # its element type, array identity and index/length constraints.
        return {key(v):1}
    if v.get('kind')=='op' and v['op'] in ('+','-'):
        a=polynomial(v['args'][0]);b=polynomial(v['args'][1])
        if a is None or b is None:return None
        for k,x in b.items():a[k]=a.get(k,0)+(x if v['op']=='+' else -x)
        return {k:x for k,x in a.items() if x}
    if v.get('kind')=='op' and v['op'] in ('*','/') and all(x.get('kind') in ('op','literal','parameter','storage','native_reserve','transaction_value','actual_sender','contract_address','root_instance','new_instance') for x in walk(v) if 'kind' in x):
        # Keep the entire checked integer expression as one term: no division
        # distribution, real-number cancellation or wraparound approximation.
        return {key(v):1}
    return None



def add(a,b):
    if a is None or b is None:return None
    out=dict(a)
    for k,x in b.items():out[k]=out.get(k,0)+x
    return {k:x for k,x in out.items() if x}


def negative(a):return {k:-x for k,x in a.items()}


def term(p):
    import json
    if not p:return lit(0)
    if set(p)=={'#'}:return lit(p['#'])
    if len(p)==1:
        k,n=next(iter(p.items()))
        if n==1:return json.loads(k)
    return None


def deltas(path):
    latest={key(w['path']):w for w in path['writes']}
    out=[]
    for selector,w in latest.items():
        same=[r for r in path['writes'] if key(r['path'])==selector]
        family=[r for r in path['writes'] if r['path']['root']==w['path']['root'] and key(r['path'].get('instance'))==key(w['path'].get('instance'))]
        if family and all(r.get('local_increment') is not None for r in family):
            delta={}
            for r in same:delta=add(delta,polynomial(r['local_increment']))
            basis='sum_of_source_local_increments_alias_preserved_in_write_value'
        else:
            form=polynomial(w['value'])
            delta=add(form,{selector:-1}) if form is not None else None
            basis='exact_before_after_expression'
        out.append({'write':w,'delta':delta,'delta_basis':basis})
    return out


def holder_path(selector,lookup):
    from .m03_p_route import value_type,keys,fields
    typ=lookup.nodes.get(selector['root'],{}).get('typeName',{})
    return (typ.get('nodeType')=='Mapping' and typ.get('keyType',{}).get('name') in ('address','address payable')
            and len(keys(selector))==1 and not fields(selector) and str(value_type(selector,lookup)).startswith('uint'))


def scalar_path(selector,lookup):
    from .m03_p_route import value_type
    return not selector.get('segments') and str(value_type(selector,lookup)).startswith('uint')


def unsafe_integer_cast(path,lookup):
    for w in path['writes']:
        for n in walk(lookup.nodes.get(w['source'].get('ast_id'),{})):
            if n.get('nodeType')=='FunctionCall' and n.get('kind')=='typeConversion':
                typ=elementary_expression_name(n.get('expression',{}))
                if typ.startswith(('uint','int')):return True
    return False


def asset_models(lookup,program,allow_nested=False):
    from .m03_p_route import keys
    models=[]
    for fn,paths in program.items():
        for pi,path in enumerate(paths):
            if path['flow']=='reverted' or path['issues'] or unsafe_integer_cast(path,lookup):continue
            changes=deltas(path)
            for payment in path.get('native_transfers',[]):
                if payment['recipient'].get('kind')!='actual_sender':continue
                amount=polynomial(payment['amount'])
                if not amount or term(amount) is None:continue
                if conditions_possible(path['guards'],payment['success']):continue
                for balance in changes:
                    selector=balance['write']['path']
                    if not holder_path(selector,lookup) or keys(selector)[0].get('kind')!='actual_sender':continue
                    if balance['delta']!=negative(amount):continue
                    for supply in changes:
                        if scalar_path(supply['write']['path'],lookup) and supply['delta']==negative(amount):
                            models.append({'balance_root':selector['root'],'supply_root':supply['write']['path']['root'],
                                'basis':'same_holder_ledger_debit_and_native_redemption_with_matching_supply_reduction',
                                'redemption_function':fn,'path_index':pi,'balance_effect':balance['write'],
                                'supply_effect':supply['write'],'native_payment':payment,'conditions':path['guards'],
                                'unit_relation':'one ledger unit to one native value unit in this source path',
                                'scope':'conditional redeemable entitlement; no reserve-solvency, callback or deployment proof'})
    result=list({(m['balance_root'],m['supply_root']):m for m in models}.values())
    from .m05_asset_registry import transferable_models
    represented={m['balance_root'] for m in result}
    result.extend(m for m in transferable_models(lookup,program) if m['balance_root'] not in represented)
    if allow_nested:
        from .m03_p_asset_dimensions import nested_asset_models
        result.extend(nested_asset_models(lookup,program))
    return result


def analyze_assets(bundle,contract,requested,max_paths,lookup=None,program=None):
    from .m03_p_route import keys,effective_permission,selectors
    supplied=lookup is not None and program is not None
    lookup=lookup or AssetPaths(bundle,contract,max_paths);program={} if program is None else program;failures=[]
    # No unrelated financial guesses are emitted for ordinary storage programs.
    from .source_entry_identity import entry_functions
    for f in ([] if supplied else entry_functions(lookup)):
        try:program[f['signature']]=lookup.run(f['signature'])
        except Exception as ex:failures.append({'function':f['signature'],'reason':type(ex).__name__+':'+str(ex)})
    from .m04_asset_math import proportional_models,proportional_backing,controlled_creation
    models=asset_models(lookup,program)+proportional_models(lookup,program);rows=[];gaps=[];alternatives=[]
    for model in models:
        if model.get('kind')=='source_transferable_ledger':
            from .m05_asset_registry import mint_rows
            new_rows,new_alternatives=mint_rows(bundle,lookup,program,model,requested)
            rows.extend(new_rows);alternatives.extend(new_alternatives);continue
        root=model['balance_root'];supply_root=model['supply_root']
        for fn,paths in program.items():
            for pi,path in enumerate(paths):
                if path['flow']=='reverted':continue
                changes=deltas(path);balances=[x for x in changes if x['write']['path']['root']==root]
                if not balances:continue
                supply=[x for x in changes if x['write']['path']['root']==supply_root]
                amount={}
                for x in balances:amount=add(amount,x['delta'])
                supply_delta={}
                for x in supply:supply_delta=add(supply_delta,x['delta'])
                issues=copy.deepcopy(path['issues'])
                if unsafe_integer_cast(path,lookup):issues.append({'reason':'asset_integer_cast_not_lowered'})
                privilege=[g for g in effective_permission(path['guards'],lookup) if all(s['root']!=root for s in selectors(g))]
                synthetic=bundle.get('material_origin','compiler_artifacts')!='compiler_artifacts'
                status='inconclusive';reason='asset_delta_or_source_path_unresolved';ordinary=None
                atom=term(amount) if amount is not None else None
                positive=[x for x in balances if x['delta'] is not None and term(x['delta']) not in (None,lit(0))]
                # Exact fresh native-value backing also applies to a named recipient.
                # An administrator selecting that recipient does not create
                # unbacked units. Both ledger and supply must equal msg.value.
                backed=(model.get('kind')!='proportional_native_shares' and len(balances)==1 and atom=={'kind':'transaction_value','type':'uint256'} and supply_delta==amount
                        and lookup.function(fn).get('stateMutability')=='payable')
                share_backing=proportional_backing(model,atom,path,lookup,fn) if supply_delta==amount and len(balances)==1 else None
                conversion=None
                if len(balances)==1 and amount and supply_delta==amount:
                    holder=keys(balances[0]['write']['path'])[0]
                    for other in models:
                        if model.get('kind')=='proportional_native_shares' or other.get('kind') in ('proportional_native_shares','source_transferable_ledger'):continue
                        if other['balance_root']==root or other['supply_root']==supply_root:continue
                        debit=[x for x in changes if x['write']['path']['root']==other['balance_root']]
                        total=[x for x in changes if x['write']['path']['root']==other['supply_root']]
                        if len(debit)==len(total)==1 and key(keys(debit[0]['write']['path'])[0])==key(holder) and debit[0]['delta']==negative(amount) and total[0]['delta']==negative(amount):
                            conversion={'basis':'same_holder_same_native_unit_entitlement_conversion','from_model':other,'holder':holder,'amount':amount,'source_debit':debit[0]['write'],'source_supply_debit':total[0]['write']};break
                from .m04_asset_authority import issuance_controls
                allowance_controls,upstream_controls=issuance_controls(path,amount,changes,lookup,program,models)
                composed_creation=controlled_creation(atom,path,upstream_controls,lookup,model) if supply_delta==amount and len(balances)==1 else None
                self_debit=any(keys(x['write']['path'])[0].get('kind')=='actual_sender' and x['delta'] is not None
                               and any(v<0 for v in x['delta'].values()) for x in balances)
                self_transfer=(amount=={} and not supply and self_debit and len(balances)==2)
                if not issues and amount is not None:
                    if amount=={}:
                        status='refuted_in_scope';reason='conserved_ledger_transfer_not_new_entitlement'
                        if self_transfer:ordinary='holder_moves_own_balance_with_conserved_total'
                    elif backed:
                        status='refuted_in_scope';reason='equal_value_native_deposit_not_discretionary_issuance'
                        if not privilege:ordinary='public_equal_value_deposit_for_sender'
                    elif share_backing:
                        status='refuted_in_scope';reason='proportional_native_deposit_not_discretionary_share_creation'
                        ordinary='public_deposit_receives_source_matched_proportional_shares'
                    elif conversion:
                        status='refuted_in_scope';reason='same_holder_redeemable_entitlement_conversion_not_new_creation'
                        ordinary='conserved_same_holder_entitlement_conversion'
                    elif all(x<=0 for x in amount.values()):
                        status='refuted_in_scope';reason='ledger_reduction_not_new_entitlement'
                        if fn==model['redemption_function'] and pi==model['path_index']:
                            ordinary='holder_redeems_own_source_bound_entitlement'
                    elif composed_creation:
                        status='supported';reason=composed_creation['reason']
                    elif not privilege and allowance_controls and supply_delta==amount and not path.get('native_transfers'):
                        status='supported';reason='privileged_allowance_consumed_for_redeemable_entitlement_creation'
                    elif not privilege and upstream_controls:
                        reason='upstream_privileged_creation_relation_not_closed'
                    elif not privilege:
                        status='refuted_in_scope';reason='no_privileged_creation_on_declared_path'
                    elif supply_delta!=amount:
                        reason='ledger_supply_creation_not_consistent'
                    elif atom and not path.get('native_transfers'):
                        # Require explicit positivity, or a positive constant;
                        # other arithmetic stays unsupported rather than guessed.
                        if atom.get('kind')=='literal' and atom['value']>0 or not conditions_possible(path['guards'],op('>',atom,lit(0))) or (atom.get('kind')=='parameter' and str(atom.get('type','')).startswith('uint') and conditions_possible(path['guards']+[op('>',atom,lit(0))])):
                            status='supported';reason='privileged_creation_of_source_bound_redeemable_entitlement'
                        else:reason='positive_entitlement_creation_not_established'
                if not issues and model.get('kind')=='proportional_native_shares' and atom and privilege and supply_delta==amount and not share_backing and not path.get('native_transfers') and status=='supported':
                    reason='privileged_creation_of_source_bound_proportional_shares'
                effect=next((x['write'] for x in balances if x in positive),balances[0]['write'])
                if allowance_controls:
                    alternatives.append({'function':fn,'path_index':pi,'reason':'holder_consumes_authorized_issuance_allowance',
                        'balance_root':root,'supply_root':supply_root,'source':path['entry_source'],
                        'effect_sources':[c['consumed_allowance']['source']['ast_id'] for c in allowance_controls],
                        'issuer_functions':[c['issuer_function'] for c in allowance_controls],
                        'allowance_evidence':allowance_controls,
                        'decision':'holder may consume the granted allowance; issuer exclusivity applies to allocation, not consumption; FCR creation remains separate'})
                if ordinary:
                    alternatives.append({'function':fn,'path_index':pi,'reason':ordinary,'balance_root':root,'supply_root':supply_root,
                        'source':path['entry_source'],'effect_sources':[x['write']['source']['ast_id'] for x in balances+supply],
                        'decision':'do_not_impose_peer_issuer_exclusivity_on_source_bound_public_or_holder_operation'})
                matches=[p for p in requested if p.get('rule')=='FCR-MINT' and p.get('function')==fn
                    and str((p.get('effect') or {}).get('object',p.get('effect_state',''))).split('.')[-1] in
                        (lookup.nodes[root]['name'],lookup.nodes[supply_root]['name'])]
                if requested and not matches:continue
                row={'schema':'m03-p-result-v2','route':'P','rule':'FCR-MINT','status':status,'reason':reason,
                    'function':fn,'subject':'actual_sender','structure':model.get('kind','native_redeemable_ledger'),
                    'program_id':bundle['program_id'],'build_id':bundle['build_id'],'policy_scope':'program_derived_asset_model',
                    'required_policy_candidate':{'kind':'privileged_asset_creation','balance_root':root,'supply_root':supply_root},
                    'policy_basis':{'asset_model':model,'privilege_conditions':privilege,'ledger_delta':amount,'supply_delta':supply_delta,
                                    'proportional_backing':share_backing,'composed_creation':composed_creation,'upstream_privileged_controls':upstream_controls,'resolved_issuance_allowance':allowance_controls,'native_value_equal_backing':backed,'conserved_conversion':conversion,'ordinary_route':ordinary,'positive_creation_condition':op('>',atom,lit(0)) if atom else None,'positive_creation_scope':'existential positive amount under retained source constraints; zero-only paths excluded'},
                    'effect':{'object':lookup.nodes[root]['name'],'selector':effect['path'],'value':effect['value'],'operator':effect['operator'],'source':effect['source']},
                    'ledger_effects':[x['write'] for x in balances],'supply_effects':[x['write'] for x in supply],
                    'path_index':pi,'conditions':path['guards'],'derived_prediction_conditions':composed_creation.get('prediction_conditions',[]) if composed_creation else [],'issues':issues,'execution_status':'not_run','solver_status':'not_called',
                    'no_execution_required':True,'reportable':status=='supported' and not synthetic,'diagnostic_only':synthetic,
                    'material_origin':bundle.get('material_origin','compiler_artifacts'),'source_remarks':[p.get('unresolved',[]) for p in matches],
                    'limitations':['bounded source-backed native-redeemable ledger profile, not arbitrary asset semantics',
                        'positive deltas are mathematical integers under original checked-arithmetic path assumptions; no wraparound',
                        'source path and declared pre-state conditional; no deployment, reserve, callback, execution or unlimited-issuance proof',
                        'all source cap and consent conditions retained; finite privilege is not dismissed merely because capped'],
                    'coverage':'declared ledger and function/path only','not_a_safety_conclusion':True}
                row['id']=digest({k:row[k] for k in ('program_id','build_id','rule','function','effect','conditions','required_policy_candidate','policy_basis')});rows.append(row)
    from .m04_record_assets import analyze_records
    record_rows,record_models,record_alternatives=analyze_records(bundle,lookup,program,requested)
    rows.extend(record_rows);models.extend(record_models);alternatives.extend(record_alternatives)
    if models:gaps.extend(failures)
    return rows,gaps,alternatives,models


def ordinary_asset_alternative(hypothesis,write,function,path_index,alternatives):
    if hypothesis.get('basis')!='same_resource_guarded_operation':return None
    for a in alternatives:
        if a['function']==function and a['path_index']==path_index and write['source']['ast_id'] in a['effect_sources'] and (not a.get('issuer_functions') or hypothesis.get('origin_function') in a['issuer_functions']):
            return {**a,'narrower_hypothesis':hypothesis,'effect':write['path']}
    return None
