"""Exact source relationships for proportional shares and controlled rewards.

Integer floor expressions are retained structurally. This is not a solver,
solvency model, callback check or a proof that every declared state is reachable.
"""
from .m03_p_paths import key,walk,op,lit,normalize,conditions_possible

def same(a,b):return key(normalize(a))==key(normalize(b))
def product(v,a,b):
 return v.get('kind')=='op' and v.get('op')=='*' and (same(v['args'][0],a) and same(v['args'][1],b) or same(v['args'][1],a) and same(v['args'][0],b))

def proportional_models(lookup,program):
 from .m03_p_assets import deltas,negative,term,holder_path,scalar_path,unsafe_integer_cast
 from .m03_p_route import keys
 models=[]
 for fn,paths in program.items():
  for pi,p in enumerate(paths):
   if p['flow']=='reverted' or p['issues'] or unsafe_integer_cast(p,lookup):continue
   changes=deltas(p)
   for payment in p.get('native_transfers',[]):
    a=payment['amount']
    if payment['recipient']!={'kind':'actual_sender'} or conditions_possible(p['guards'],payment['success']):continue
    if a.get('kind')!='op' or a['op']!='/':continue
    for balance in changes:
     if not holder_path(balance['write']['path'],lookup) or keys(balance['write']['path'])!=[{'kind':'actual_sender'}] or not balance['delta']:continue
     quantity=term(negative(balance['delta']))
     if quantity is None or quantity==lit(0):continue
     for supply in changes:
      total=supply['write']['path']
      if not scalar_path(total,lookup) or supply['delta']!=balance['delta'] or not same(a['args'][1],total):continue
      reserves=[v for v in walk(a['args'][0]) if v.get('kind')=='native_reserve']
      if len(reserves)!=1 or not product(a['args'][0],quantity,reserves[0]):continue
      models.append({'kind':'proportional_native_shares','balance_root':balance['write']['path']['root'],'supply_root':total['root'],
       'basis':'same_holder_share_debit_total_share_debit_and_proportional_native_redemption','redemption_function':fn,'path_index':pi,
       'balance_effect':balance['write'],'supply_effect':supply['write'],'native_payment':payment,'conditions':p['guards'],
       'quantity':quantity,'reserve':reserves[0],'total_before':total,'unit_relation':'floor(redeemed_shares * native_reserve / total_shares_before)',
       'scope':'conditional share entitlement; original division order and checked arithmetic, no solvency/deployment proof'})
 return list({(m['balance_root'],m['supply_root']):m for m in models}.values())

def proportional_backing(model,amount,path,lookup,fn):
 if model.get('kind')!='proportional_native_shares' or not amount or lookup.function(fn).get('stateMutability')!='payable':return None
 value={'kind':'transaction_value','type':'uint256'};total=model['total_before'];reserve=model['reserve']
 if conditions_possible(path['guards'],op('>',value,lit(0))):return None
 initial=not conditions_possible(path['guards'],op('==',total,lit(0))) and same(amount,value)
 proportional=amount.get('kind')=='op' and amount['op']=='/' and product(amount['args'][0],value,total) and same(amount['args'][1],op('-',reserve,value))
 if proportional and conditions_possible(path['guards'],op('!=',total,lit(0))):proportional=False
 if not (initial or proportional):return None
 return {'basis':'source_matched_payable_share_pricing','initial_zero_supply':initial,'amount':amount,'fresh_native_value':value,
  'total_before':total,'reserve_before':op('-',reserve,value),'scope':'source pricing equality with original floor/denominator; no fairness/solvency claim'}

def controlled_creation(amount,path,controls,lookup,model):
 if not amount or model.get('kind')=='proportional_native_shares' or path.get('native_transfers') or path['issues']:return None
 value={'kind':'transaction_value','type':'uint256'}
 for c in controls:
  state=c['assigned_state'];assigned=c['assigned_value']
  if state.get('segments') or assigned.get('kind')!='parameter':continue
  # Administrator-set multiplier of fresh native deposit, with a source-
  # feasible setting >1. Multiplying display units without changing the
  # redeemable ledger cannot reach this consumer.
  if product(amount,value,state) and not conditions_possible(path['guards'],op('>',value,lit(0))):
   if not conditions_possible(c['issuer_conditions']+[op('>',assigned,lit(1))]):continue
   return {'reason':'privileged_rate_creates_entitlement_above_fresh_native_value','controller':c,'amount':amount,
    'prediction_conditions':[op('>',value,lit(0)),op('>',state,lit(1))],
    'scope':'conditional permitted multiplier >1 with checked arithmetic; finite rates are not described as unlimited'}
  # Reward index delta, same-holder checkpoint update, and exact positive
  # scaling divisor. Retain the minimum positive rounded reward explicitly.
  if amount.get('kind')!='op' or amount['op']!='/':continue
  numerator,scale=amount['args']
  if scale.get('kind')!='literal' or type(scale.get('value')) is not int or scale['value']<=0:continue
  if numerator.get('kind')!='op' or numerator['op']!='*':continue
  for stake,difference in (numerator['args'],numerator['args'][::-1]):
   if stake.get('kind')!='storage' or stake.get('segments')!=[{'key':{'kind':'actual_sender'}}]:continue
   if difference.get('kind')!='op' or difference['op']!='-' or not same(difference['args'][0],state):continue
   snapshot=difference['args'][1]
   if snapshot.get('kind')!='storage' or snapshot.get('segments')!=stake['segments']:continue
   if not any(same(w['path'],snapshot) and same(w['value'],state) for w in path['writes']):continue
   if not conditions_possible(c['issuer_conditions']+[op('>',assigned,state)]):continue
   return {'reason':'privileged_index_creates_source_bound_redeemable_rewards','controller':c,'stake':stake,'snapshot':snapshot,
    'amount':amount,'divisor':scale,'prediction_conditions':[op('>',stake,lit(0)),op('>',state,snapshot),op('>=',numerator,scale)],
    'scope':'conditional positive rounded reward at an authorized index increment; reachable stake and reserve solvency not proven'}
 return None
