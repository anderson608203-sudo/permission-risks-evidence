"""Mixed-sign reset assignment, retaining the actual before/after expression."""
from .m05_state_relations import changes
from .m22_assets import matches
from .m03_p_assets import add
from .m03_p_paths import key
from .m03_p_route import keys,value_type

def supply_replacement(path,profile,lookup):
    """A contract-wide supply and the caller's balance are both replaced with
    the same total. This is different from claiming a caller-scoped reward."""
    if profile.get('family')!='conditional_reset_increase' or path['guards'] or path.get('native_transfers'):
        return None
    credit=profile['credits'][0]['write']
    if keys(credit['path'])!=[{'kind':'actual_sender'}]:return None
    peers=[w for w in path['writes'] if w['path']['root']!=credit['path']['root'] and
           not w['path'].get('segments') and value_type(w['path'],lookup).startswith('uint') and
           w.get('operator')=='=' and key(w['value'])==key(credit['value'])]
    if len(peers)!=1:return None
    # Validate the aggregate independently: another path burns the same
    # quantity from an individual balance and this scalar in lockstep.
    return peers[0]

def aggregate_source(program,asset,peer,lookup):
    from .m03_p_assets import polynomial
    from .m04_logic import Unsupported
    for fn,paths in program.items():
        for p in paths:
            if p['flow'] not in ('normal','returned') or p['issues'] or p.get('evaluation_gaps'):continue
            try:updates=changes(p,lookup)
            except (Unsupported,ValueError):continue
            totals=[d for d in updates if key(d['write']['path'])==key(peer['path']) and d['delta']]
            balances=[d for d in updates if matches(d['write']['path'],asset)]
            if len(totals)!=1:continue
            total=totals[0]
            for balance in balances:
                w=balance['write']
                if total['delta']==balance['delta'] or (w.get('operator')=='=' and all(v>0 for v in total['delta'].values()) and polynomial(w['value'])==total['delta']):
                    return {'function':fn,'aggregate_update':total['write']['source'],'balance_update':w['source']}
    return None
def reset_profile(path,asset,lookup):
    updates=[d for d in changes(path,lookup) if matches(d['write']['path'],asset)]
    if len(updates)!=1 or updates[0]['delta'] is None:return None
    d=updates[0];w=d['write']
    # A whole balance replacement can increase it when the old balance is low.
    # Net increase remains in the solver query; negative outcomes are not mint.
    if w.get('operator')!='=':return None
    return {'updates':updates,'debits':[],'credits':updates,'total':d['delta'],'family':'conditional_reset_increase'}
