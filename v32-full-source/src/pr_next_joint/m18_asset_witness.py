"""Source transfer witnesses with explicit fee/burn conservation."""
import copy
from .m03_p_paths import key,op,lit
from .m03_p_route import keys,value_type
from .m03_p_assets import add,negative,holder_path
from .m04_logic import Unsupported

def fee_witness(lookup,path,debit,balances,all_changes):
    from .m08_financial import source_signed_changes,quantity
    from .m09_shared_policy import implies
    if len(balances)<2:return None
    if any(d['delta'] is None or not holder_path(d['write']['path'],lookup) for d in balances):return None
    signed=source_signed_changes(lookup,path,balances)
    ds=[d for d in signed if d['source_sign']=='negative']
    cs=[d for d in signed if d['source_sign']=='positive']
    if len(ds)!=1 or not cs or len(ds)+len(cs)!=len(signed):return None
    if key(ds[0]['write']['path'])!=key(debit['write']['path']):return None
    holder=keys(debit['write']['path'])[0]
    if any(key(keys(d['write']['path'])[0])==key(holder) for d in cs):return None
    total={}
    for d in balances:total=add(total,d['delta'])
    supply=None
    if total and not implies(lookup,path,op('==',quantity(total),lit(0))):
        # A debit with unexplained value loss is insufficient. Match an actual
        # scalar supply reduction in the same source path and prove its sign.
        supplies=[d for d in all_changes if not d['write']['path'].get('segments')
                  and str(value_type(d['write']['path'],lookup)).startswith('uint') and d['delta']==total]
        supplies=source_signed_changes(lookup,path,supplies) if supplies else []
        supplies=[d for d in supplies if d['source_sign']=='negative']
        if len(supplies)!=1:return None
        supply=supplies[0]
    return {'credits':cs,'net_ledger_delta':total,'supply':supply,
            'basis':'source_checked_positive_transfer_with_explicit_conservation_or_matching_burn',
            'conditions':copy.deepcopy(path['guards'])}
