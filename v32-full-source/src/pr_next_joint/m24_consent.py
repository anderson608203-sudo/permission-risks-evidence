"""Action-local authorization evidence and algebraic amount agreement."""
import copy
from .m03_p_paths import op,key,lit
from .m04_logic import Unsupported
def same_quantity(left,right,lookup):
    if left==right:return True
    if left is None or right is None:return False
    from .m08_financial import quantity
    from .m09_shared_policy import implies
    try:return implies(lookup,{'guards':[],'evaluated_terms':[]},op('==',quantity(left),quantity(right)))
    except (Unsupported,ValueError):return False

def operation_scope(path,holder,amount,lookup,root,recipient):
    from .m05_state_relations import changes
    from .m03_p_assets import add
    from .m03_p_route import keys
    effects=[d for d in changes(path,lookup) if d['write']['path']['root']==root]
    total={}
    for d in effects:
        if d['delta'] is None:total=None;break
        total=add(total,d['delta'])
    return {'kind':'source_bound_current_asset_action','holder':copy.deepcopy(holder),'requested_quantity':amount,
            'recipient':copy.deepcopy(recipient),'resource_root':root,'net_change':total,
            'source_effects':[{'selector':d['write']['path'],'delta':d['delta'],'source':d['write']['source']} for d in effects],
            'action':'conserved_transfer' if recipient is not None and total=={} else 'decrease_or_redemption' if recipient is None else 'mixed_effect',
            'conditions_retained':copy.deepcopy(path['guards']),
            'policy':'authorization is determined by source holder-controlled creation and applicable consumption; action names and missing approveBurn are not evidence'}
