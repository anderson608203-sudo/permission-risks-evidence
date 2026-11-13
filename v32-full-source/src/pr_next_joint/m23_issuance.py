"""Approved AC issuance boundary: caller-selected unbacked transferable rights.
No owner is invented. The source asset model and the actual amount/guard/effect
are retained in the query. Partial paths or unexplained restrictions stay gaps.
"""
import copy
from .m03_p_paths import key,walk,op,lit
from .m03_p_route import effective_permission,selectors
from .m11_policy import update_profile,value_backed,make_query,once_latch
from .m08_financial import quantity
from .m04_logic import Unsupported


def duties(context,state,shared,index):
    rows=[];limits=[]
    for tid,lookup in state['lookups'].items():
        for (target,fn),paths in state['paths'].items():
            if target!=tid:continue
            for pi,p in enumerate(paths):
                if p['flow'] not in ('normal','returned') or p['issues'] or p.get('evaluation_gaps'):continue
                for asset in shared.get(tid,{}).get('assets',[]):
                    try:
                        profile=update_profile(p,asset['balance_root'],asset['balance_effect']['path'].get('instance'),lookup,asset)
                        if not profile:
                            from .m24_issuance import reset_profile
                            profile=reset_profile(p,asset,lookup)
                        if not profile or profile['debits'] or not profile['credits']:continue
                        amount=quantity(profile['total'])
                        chosen={n['id'] for n in walk(amount) if n.get('kind')=='parameter'}
                        program={f:ps for (t,f),ps in state['paths'].items() if t==tid}
                        if not chosen and once_latch(p,program,lookup):continue
                        from .m24_issuance import supply_replacement,aggregate_source
                        peer=supply_replacement(p,profile,lookup)
                        aggregate=aggregate_source(program,asset,peer,lookup) if peer else None
                        if not chosen:
                            credit_selectors={key(d['write']['path']) for d in profile['credits']}
                            dependencies=[n for n in walk(amount) if n.get('kind')=='storage' and key(n) not in credit_selectors]
                            if dependencies and not aggregate:
                                limits.append({'phase':'issuance_boundary','target':tid,'function':fn,'reason':'source_computed_earnings_or_quantity_requires_backing_model','dependencies':dependencies});continue
                        if value_backed(profile['total'],lookup):continue
                        # Existing normal local certificates remain in force.
                        normals=[n for n in shared.get(tid,{}).get('normal_effects',[]) if n['function']==fn and n['path_index']==pi and n['root']==asset['balance_root']]
                        if normals:continue
                        restricted=[]
                        for g in p['guards']:
                            if any(n.get('kind')=='parameter' and n['id'] in chosen for n in walk(g)):
                                restricted.append(g)
                        if restricted:
                            # An amount constraint may be a paid allocation, cap or
                            # claim. Do not erase it or claim arbitrary issuance.
                            limits.append({'phase':'issuance_boundary','target':tid,'function':fn,'reason':'quantity_restriction_requires_backing_or_cap_model','conditions':restricted})
                            continue
                        # A separate debit may be a redeemed/consumed claim even
                        # if its record is not itself a transferable asset.
                        from .m05_state_relations import changes
                        other_debits=[d for d in changes(p,lookup) if d['write']['path']['root']!=asset['balance_root'] and
                                     not (aggregate and d['write']['path']==peer['path']) and d['delta'] and any(c<0 for c in d['delta'].values())]
                        if other_debits:
                            limits.append({'phase':'issuance_boundary','target':tid,'function':fn,'reason':'other_consumed_right_requires_unit_and_holder_binding','sources':[d['write']['source'] for d in other_debits]})
                            continue
                        permission=effective_permission(p['guards'],lookup)
                        required=op('or',op('<=',amount,lit(0)),*permission)
                        for credit in profile['credits']:
                            basis={'basis':'source_caller_selected_unbacked_issuance','approved_decision':'v23_D01_issuance_boundary',
                                'transferable_asset':copy.deepcopy(asset),'net_increase':amount,'caller_quantity_parameters':sorted(chosen),
                                'issuance_form':'quantity_selected' if chosen else 'fixed_or_reset_repeatable',
                                'source_authorization_alternatives':permission,
                                'scope':'issuance authorization boundary; intentionally open unlimited free issuance can be flagged; no realized financial loss claim',
                                'no_owner_inferred':True}
                            if aggregate:basis['source_supply_reset']={'aggregate_use':aggregate,'supply_write':peer['source']}
                            q=make_query(context,tid,fn,pi,p,credit['write'],required,basis,'AC-01');rows.append(q)
                    except (Unsupported,ValueError) as ex:limits.append({'phase':'issuance_boundary','target':tid,'function':fn,'reason':str(ex)})
    return rows,limits
