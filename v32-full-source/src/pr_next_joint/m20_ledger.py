"""Approved abstract-account MINT and DESTROY; other labels still require assets."""
import copy,os
from .m03_p_paths import key,walk,op,lit
from .m03_p_route import keys,fields,value_type,selectors
from .m03_p_assets import add,negative
from .m05_state_relations import changes
from .m05_asset_obligations import privilege,consent_model
from .m04_logic import Unsupported

def mode():
    value=os.environ.get('PR_NEXT_DESTROY_SCOPE','abstract_account_ledger')
    if value not in ('abstract_account_ledger','strict_financial'):raise ValueError('invalid_destroy_scope')
    return value

def account_record(selector,lookup):
    typ=lookup.nodes.get(selector['root'],{}).get('typeName',{})
    first=keys(selector)
    # An address-indexed scalar or an address-indexed struct's scalar field.
    return (typ.get('nodeType')=='Mapping' and typ.get('keyType',{}).get('name') in ('address','address payable')
        and len(first)==1 and str(value_type(selector,lookup)).startswith('uint'))

def credential_roots(program):
    out=set()
    for paths in program.values():
        for p in paths:
            for n in walk(p.get('guards',[])+p.get('evaluated_terms',[])):
                if n.get('kind') in ('credential_recovery','hash','signed_message_hash'):
                    out.update(s['root'] for s in selectors(n))
    return out


def component_certificate(selector,updates,lookup,program):
    """An explicit source getter totals same-subject components in one unit.
    A coincidental credit to another root or another subject is not compensation.
    """
    import json
    from .m03_p_assets import polynomial
    from .m13_financial_relations import component_shape
    from .source_entry_identity import function_mutability
    shape=component_shape(selector,lookup)
    if shape is None:return None
    cache=getattr(lookup,'_v20_account_summaries',None)
    if cache is None:
        cache=[];lookup._v20_account_summaries=cache
        for fn in lookup.abi:
            body=lookup.function(fn)
            if not body or body.get('generated_getter') or function_mutability(body) not in ('view','pure'):continue
            params=body.get('parameters',{}).get('parameters',[])
            returns=body.get('returnParameters',{}).get('parameters',[])
            if len(params)!=1 or len(returns)!=1 or params[0].get('typeDescriptions',{}).get('typeString') not in ('address','address payable'):continue
            try:branches=program.get(fn) or lookup.run(fn)
            except (Unsupported,ValueError,KeyError,TypeError):continue
            valid=[p for p in branches if p['flow']!='reverted']
            if not valid or any(p['flow']!='returned' or p['issues'] or p.get('evaluation_gaps') or p['writes'] for p in valid):continue
            forms=[polynomial(p.get('return_value',{})) for p in valid]
            if any(f!=forms[0] for f in forms) or not forms[0] or not 2<=len(forms[0])<=3 or any(c!=1 for c in forms[0].values()) or '#' in forms[0]:continue
            terms=[json.loads(t) for t in forms[0]]
            shapes=[component_shape(t,lookup) for t in terms]
            if None in shapes or len(set(shapes))!=len(shapes) or any(key(keys(t))!=key(keys(terms[0])) for t in terms):continue
            if any(key(t.get('instance'))!=key(terms[0].get('instance')) for t in terms):continue
            cache.append({'kind':'explicit_same_holder_account_sum','function':fn,'source':lookup.anchor(body),
                          'shapes':shapes,'terms':terms,'unit_assumption':'declared abstract account aggregate; no market-value claim'})
    for c in cache:
        if shape not in c['shapes']:continue
        affected=[d for d in updates if component_shape(d['write']['path'],lookup) in c['shapes']
            and key(d['write']['path'].get('instance'))==key(selector.get('instance'))]
        if not affected or any(d['delta'] is None for d in affected):continue
        # Same subject conversion; third-party credits cannot excuse its destruction.
        same=[d for d in affected if key(keys(d['write']['path']))==key(keys(selector))]
        delta={}
        for d in affected:delta=add(delta,d['delta'])
        if len(affected)>=2 and delta=={}:
            return {**copy.deepcopy(c),'source_writes':[d['write']['source'] for d in affected],
                    'holder':keys(selector)[0],'net_change':delta,
                    'kind':'source_same_holder_conversion' if len(same)==len(affected) else 'source_conserved_account_component_transfer'}
    return None

def analyze(lookup,program,assets,probe,graph=None):
    if mode()=='strict_financial':return [],[]
    from .m22_assets import identity as asset_identity
    rows=[];limits=[];financial={asset_identity(a['balance_effect']['path']) for a in assets};credentials=credential_roots(program)
    from .m08_financial import quantity
    for fn,paths in program.items():
        for pi,p in enumerate(paths):
            if p['flow'] not in ('normal','returned'):continue
            if p['issues'] or p.get('evaluation_gaps'):continue
            try:
                from .m05_state_relations import expand_write
                expanded=[x for w in p['writes'] for x in expand_write(w,lookup)]
                updates=changes({**p,'writes':expanded},lookup)
            except (Unsupported,ValueError) as e:
                limits.append({'phase':'abstract_ledger_effect','function':fn,'reason':str(e)});continue
            for debit in updates:
                w=debit['write'];sel=w['path'];root=sel['root']
                if asset_identity(sel) in financial or not account_record(sel,lookup):continue
                from .m22_record_roles import exclusion as record_exclusion
                role=record_exclusion(sel,lookup,program,assets)
                if role:
                    limits.append({'phase':'abstract_ledger_eligibility','function':fn,'root':root,'reason':'source_control_record_not_account_entitlement','certificate':role});continue
                if root in credentials:
                    limits.append({'phase':'abstract_ledger_eligibility','function':fn,'root':root,'reason':'credential_related_counter_not_financial_account'});continue
                holder=keys(sel)[0]
                # Self-receipt can be privileged issuance, but not third-party destruction.
                own_holder=holder.get('kind') in ('actual_sender','contract_address')
                if debit['delta'] is None:
                    limits.append({'phase':'abstract_ledger_effect','function':fn,'root':root,'reason':'nonlinear_net_change_not_encoded'});continue
                priv=privilege(p['guards'],lookup,root)
                if not priv:continue
                compensation=component_certificate(sel,updates,lookup,program)
                if compensation:
                    limits.append({'phase':'abstract_ledger_normal_conversion','function':fn,
                        'reason':'source_total_and_same_holder_exact_conservation','certificate':compensation,
                        'not_safety_claim':True})
                    continue
                family=[d for d in updates if d['write']['path']['root']==root and fields(d['write']['path'])==fields(sel)
                    and key(d['write']['path'].get('instance'))==key(sel.get('instance'))]
                total={}
                for d in family:total=add(total,d['delta'])
                if total is None:continue
                if not total:continue # exact ordinary transfer, not net destruction
                try:
                    from .m24_account_mint import mint_row
                    minted=mint_row(lookup,p,fn,pi,sel,w,debit,total,priv,probe)
                    if minted:rows.append(minted)
                    if own_holder:continue
                    amount=negative(debit['delta'])
                    consent,cert=consent_model(p,holder,amount,lookup,program,root,None)
                    risk=op('and',op('or',*priv),op('>',quantity(amount),lit(0)),
                        op('<',quantity(total),lit(0)),op('!',consent))
                    # Same-holder native compensation means this abstract model is
                    # insufficient to establish destruction; actual asset route may handle it.
                    payments=[x for x in p.get('native_transfers',[]) if key(x['recipient'])==key(holder)]
                    if payments:
                        limits.append({'phase':'abstract_ledger_compensation','function':fn,'root':root,
                                       'reason':'same_holder_payment_requires_unit_matched_financial_model'});continue
                    meta={'kind':'privileged_abstract_account_net_destruction',
                        'asset':{'kind':'abstract_account_ledger','balance_root':root,'fields':fields(sel),
                                 'financial_link_confirmed':False,'not_shared_with_other_categories':True},
                        'holder':holder,'debit':debit,'family_net_delta':total,'consent':consent,
                        'consent_sources':cert,'privilege':priv,'path_index':pi,
                        'evaluation_terms':copy.deepcopy(p.get('evaluated_terms',[])),
                        'scope':'approved abstract account units; economic value and reachable positive initial balance not established',
                        'initial_state_limit':'conditional mechanism from symbolic source state, not deployment loss proof'}
                    row=probe(lookup,copy.deepcopy(p['guards']),risk,meta,w['source'],fn,'FCR-DESTROY')
                    row['definition_profile']='abstract_account_ledger'
                    row['effect']={'kind':'account_net_decrease','selector':sel,'value':w['value'],'operator':w['operator'],'source':w['source']}
                    rows.append(row)
                except (Unsupported,ValueError) as e:limits.append({'phase':'abstract_ledger_model','function':fn,'root':root,'reason':str(e)})
    return rows,limits
