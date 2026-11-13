"""Bounded source controller->consumer composition, not execution evidence."""
import copy
from .m03_p_paths import key,walk
from .m03_p_route import keys
from .m04_logic import Unsupported

def transform(v,params=None,caller=False,storage=None):
    params=params or {};storage=storage or {}
    if isinstance(v,dict):
        if v.get('kind')=='actual_sender' and caller:return {'kind':'transition_caller'}
        if v.get('kind')=='parameter' and v['id'] in params:return copy.deepcopy(params[v['id']])
        if v.get('kind')=='storage' and key(v) in storage:return copy.deepcopy(storage[key(v)])
        return {k:transform(x,params,caller,storage) for k,x in v.items()}
    return [transform(x,params,caller,storage) for x in v] if isinstance(v,list) else v

def controller_model(e,row,controller):
    """Use an actual issuer write and match its selector to the consumed state.

    Original issuer caller is renamed before key substitution; the holder is
    never silently required to be the issuer. No arbitrary storage patching.
    """
    z=e.z;lookup=e.lookup
    source=controller['source']['ast_id'];assigned=controller['assigned_state']
    paths=lookup.run(controller['issuer_function'])
    matches=[(p,w) for p in paths if p['flow']!='reverted' and not p['issues'] for w in p['writes']
             if w['source']['ast_id']==source and key(w['path'])==key(assigned) and key(w['value'])==key(controller['assigned_value'])]
    if len(matches)!=1:raise Unsupported('controller_assignment_not_unique_in_original_source')
    path,w=matches[0]
    # Other writes to roots read by the consumer need a larger transition model.
    used={v['root'] for v in walk([row['conditions'],row['effect'],row['policy_basis'].get('ledger_delta',{})]) if v.get('kind')=='storage'}
    if any(x is not w and x['path']['root'] in used for x in path['writes']):raise Unsupported('controller_has_other_consumer_state_writes')
    candidates=[]
    for v in walk([row['conditions'],row['effect'],row['policy_basis'].get('composed_creation'),row['policy_basis'].get('resolved_issuance_allowance')]):
        if v.get('kind')=='storage' and v['root']==assigned['root'] and v.get('instance')==assigned.get('instance'):
            if len(v.get('segments',[]))==len(assigned.get('segments',[])):candidates.append(v)
    # Prefer consumer selector (with holder), not the source issuer parameters.
    candidates=[v for v in candidates if not any(x.get('kind')=='parameter' and x['id'] in {k.get('id') for k in keys(assigned)} for x in walk(v))]
    unique={key(v):v for v in candidates}
    if not unique and not keys(assigned):unique={key(assigned):assigned}
    if len(unique)!=1:raise Unsupported('controller_consumer_selector_not_unique')
    selected=next(iter(unique.values()));params={}
    for old,new in zip(assigned.get('segments',[]),selected.get('segments',[])):
        if 'field' in old:
            if old!=new:raise Unsupported('controller_field_mismatch')
        elif old['key'].get('kind')=='parameter':params[old['key']['id']]=new['key']
        elif key(old)!=key(new):raise Unsupported('controller_key_not_bindable')
    conditions=transform(path['guards'],params,caller=True)
    permissions=transform(controller['issuer_permission'],params,caller=True)
    # Source-matched actual permission atoms already came from M1 graph paths.
    if not permissions:raise Unsupported('controller_privilege_missing')
    value=transform(w['value'],params,caller=True)
    post={key(selected):value}
    return conditions+permissions,post,{'issuer_function':controller['issuer_function'],'source':controller['source'],
        'assigned_selector':selected,'assigned_value':value,'issuer_caller':'transition_caller',
        'consumer_caller':'actual_sender','scope':'one source controller transition then consumer; deployment prefix not established'}

def composed_asset(e,row,effect_fn):
    z=e.z;basis=row['policy_basis'];composed=basis.get('composed_creation');allowances=basis.get('resolved_issuance_allowance',[])
    controller=composed.get('controller') if composed else allowances[0] if len(allowances)==1 else None
    if not controller:raise Unsupported('asset_upstream_control_or_backing_requires_composed_model')
    conditions,post,record=controller_model(e,row,controller)
    guards=[e.expr(transform(g,storage=post)) for g in row['conditions']]
    def delta(values):
        import json
        return z.Sum([int(coef)*e.expr(transform(json.loads(t),storage=post)) for t,coef in values.items()]) if values else z.IntVal(0)
    ledger=delta(basis['ledger_delta']);supply=delta(basis['supply_delta'])
    change=effect_fn(e,row['effect'],post)
    positive=z.And(ledger>0,supply>0,ledger==supply,change)
    if composed and composed.get('reason')=='privileged_rate_creates_entitlement_above_fresh_native_value':
        positive=z.And(positive,ledger>e.expr({'kind':'transaction_value','type':'uint256'}))
    if composed and composed.get('reason')=='privileged_index_creates_source_bound_redeemable_rewards':
        # Compare a positive authorized index increase, retaining issuer bounds.
        state=controller['assigned_state'];value=post[key(state)]
        positive=z.And(positive,e.expr(value)>e.expr(state))
    return z.And(*[e.expr(c) for c in conditions],*guards),positive,{'kind':'composed_asset_accounting',
        'checks':['actual controller path and assignment','distinct issuer and holder','same controlled state consumed','net positive entitlement and supply'],
        'transition':record,'assumption':'source-derived redeemable entitlement and declared pre-state; reserve/transaction reachability not proved'}
