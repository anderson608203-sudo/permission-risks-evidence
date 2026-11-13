"""Source-backed participant stages and listed-object purchases.
These certificates displace inapplicable peer rules, never an explicit guard.
"""
import copy
from .m03_p_paths import key,walk,op,lit
from .m03_p_route import keys,fields,selectors,value_type,effective_permission
from .m03_p_assets import deltas,negative
from .m09_shared_policy import implies as model_implies
from .m04_logic import Unsupported
SENDER={'kind':'actual_sender'};PAID={'kind':'transaction_value','type':'uint256'}

def implies(lookup,path,predicate):
    # A source conjunct is a conditional fact of this route. This shortcut
    # does not certify route feasibility: the risk query still goes through
    # the full path/evaluation model. It avoids requiring unrelated payment
    # arithmetic to re-prove an explicitly present owner/listing guard.
    def atoms(v):
        if v.get('kind')=='op' and v.get('op')=='and':
            return [a for x in v['args'] for a in atoms(x)]
        return [v]
    known={key(a) for g in path.get('guards',[]) for a in atoms(g)}
    if all(key(a) in known for a in atoms(predicate)):return True
    return model_implies(lookup,path,predicate)

def clean(p):return p['flow'] in ('normal','returned') and not p['issues'] and not p.get('evaluation_gaps')
def aligned(x,source,target):
    from .m05_mechanism_core import remap
    a=keys(source);b=keys(target)
    if len(a)!=len(b):return None
    mapping={}
    for left,right in zip(a,b):
        if left.get('kind')=='parameter':mapping[left['id']]=right
        elif key(left)!=key(right):return None
    return remap(x,mapping)

def source_certificates(lookup,program):
    out=[];limits=[]
    for fn,paths in program.items():
        for pi,p in enumerate(paths):
            if not clean(p):continue
            try:
                for owner_write in p['writes']:
                    owner=owner_write['path']
                    if owner_write['value']!=SENDER or value_type(owner,lookup) not in ('address','address payable'):continue
                    # Buyer replaces owner of the same listed record.
                    if keys(owner):
                        flags=[w for w in p['writes'] if key(keys(w['path']))==key(keys(owner)) and key(w['path'].get('instance'))==key(owner.get('instance')) and w['value']==lit(False) and value_type(w['path'],lookup)=='bool' and implies(lookup,p,w['path'])]
                        for flag in flags:
                            prices=[s for g in p['guards'] for s in selectors(g) if key(keys(s))==key(keys(owner)) and key(s.get('instance'))==key(owner.get('instance')) and str(value_type(s,lookup)).startswith('uint') and implies(lookup,p,op('>=',PAID,s))]
                            if not prices:continue # an owner may explicitly list an object for zero consideration
                            listings=[];unsafe=False
                            for other,branches in program.items():
                                for branch in branches:
                                    if branch['flow'] not in ('normal','returned'):continue
                                    from .m03_p_resource_relations import stored_values
                                    for raw in branch['writes']:
                                        if raw['path']['root']!=flag['path']['root']:continue
                                        for selector,value in stored_values(raw):
                                            if fields(selector)!=fields(flag['path']) or len(keys(selector))!=len(keys(flag['path'])):continue
                                            if value==lit(False) or clean(branch) and implies(lookup,branch,op('==',value,lit(False))):continue
                                            allocation=raw['value'].get('kind')=='record' and any(k.get('kind')=='storage' and k.get('root')==owner['root'] and any(s.get('length') for s in k.get('segments',[])) for k in keys(raw['path']))
                                            if allocation:continue
                                            bound=aligned(owner,owner,selector)
                                            if bound is None or not clean(branch) or not implies(lookup,branch,op('==',SENDER,bound)):unsafe=True
                                            else:listings.append(raw['source'])
                            if unsafe or not listings:continue
                            # Listing consent includes its source-controlled price.
                            # A public price edit must not manufacture a valid sale.
                            price_writers=[]
                            for price in prices:
                                for other,branches in program.items():
                                    for branch in branches:
                                        if branch['flow'] not in ('normal','returned'):continue
                                        for raw in branch['writes']:
                                            if raw['path']['root']!=price['root']:continue
                                            for selector,value in stored_values(raw):
                                                if fields(selector)!=fields(price) or len(keys(selector))!=len(keys(price)):continue
                                                if value==lit(0) and any(fields(clear['path'])==fields(flag['path']) and clear['path']['root']==flag['path']['root'] and keys(clear['path'])==keys(selector) and clear['value']==lit(False) for clear in branch['writes']):continue
                                                bound=aligned(owner,price,selector)
                                                if bound is None or not clean(branch) or not implies(lookup,branch,op('==',SENDER,bound)):unsafe=True
                                                else:price_writers.append(raw['source'])
                            if unsafe or not price_writers:continue
                            sources=[owner_write['source'],flag['source']];payments=[]
                            for pay in p.get('native_transfers',[]):
                                if key(pay['recipient'])==key(owner) and implies(lookup,p,op('<=',pay['amount'],PAID)) and all(implies(lookup,p,op('>=',pay['amount'],price)) for price in prices) and implies(lookup,p,op('>=',pay['amount'],lit(0))) and implies(lookup,p,pay['success']):payments.append(pay['source'])
                            fee_certificate=None
                            if not payments:
                                from .m24_market import fee_sale
                                fee_certificate=fee_sale(lookup,program,p,owner,prices)
                                if fee_certificate:payments=fee_certificate['payment_sources']
                            if not payments:continue
                            sources.extend(payments)
                            # Associated owner-count accounting has the exact old
                            # owner / new owner and balanced +/- one updates.
                            changes=deltas(p)
                            for d in changes:
                                sel=d['write']['path']
                                if not keys(sel):continue
                                k=keys(sel)[0]
                                if d['delta']=={'#':-1} and key(k)==key(owner) and any(x['write']['path']['root']==sel['root'] and x['delta']=={'#':1} and keys(x['write']['path'])==[SENDER] for x in changes):
                                    sources.extend(x['source'] for x in p['writes'] if x['path']['root']==sel['root'])
                            out.append({'kind':'source_owner_listed_paid_object_purchase','function':fn,'path_index':pi,'owner':owner,'flag':flag['path'],'prices':prices,'listing_sources':listings,'price_management_sources':price_writers,'effect_sources':sources,'payment_sources':payments,'fee_certificate':fee_certificate})
                    else:
                        # Replace an offer/bid, then cancel/consume it as its
                        # recorded participant. Cancellation is not creation.
                        for flag in p['writes']:
                            if flag['path'].get('segments') or flag['value']!=lit(True) or value_type(flag['path'],lookup)!='bool':continue
                            for price in p['writes']:
                                if price['path'].get('segments') or not str(value_type(price['path'],lookup)).startswith('uint'):continue
                                oldprice=price['path'];newprice=price['value']
                                if not implies(lookup,p,op('or',op('!',flag['path']),op('<',newprice,oldprice))) and not implies(lookup,p,op('or',op('!',flag['path']),op('>',newprice,oldprice))):continue
                                cancellation=[]
                                for other,branches in program.items():
                                    for branch in branches:
                                        if not clean(branch) or not implies(lookup,branch,op('==',SENDER,owner)):continue
                                        by={key(w['path']):w for w in branch['writes']}
                                        if by.get(key(owner),{}).get('value')==lit(0) and by.get(key(flag['path']),{}).get('value')==lit(False) and by.get(key(oldprice),{}).get('value')==lit(0):cancellation.append(other)
                                if not cancellation:continue
                                # A global administrator with unrelated powers
                                # is not relabelled a market participant.
                                unrelated=False
                                for other,branches in program.items():
                                    for branch in branches:
                                        if other in cancellation or not clean(branch):continue
                                        if any(any(key(s)==key(owner) for s in selectors(g)) for g in effective_permission(branch['guards'],lookup)):
                                            unrelated=True
                                if unrelated:continue
                                payment_sources=[]
                                if newprice==PAID:
                                    if not implies(lookup,p,op('!',flag['path'])):
                                        refunds=[e for e in p.get('native_transfers',[]) if key(e['recipient'])==key(owner) and key(e['amount'])==key(oldprice)]
                                        if not refunds:continue
                                        payment_sources=[e['source'] for e in refunds]
                                sources=[owner_write['source'],flag['source'],price['source']]
                                out.append({'kind':'source_participant_offer_creation_not_cancellation','function':fn,'path_index':pi,'participant':owner,'price':oldprice,'active':flag['path'],'cancel_functions':cancellation,'effect_sources':sources,'payment_sources':payment_sources,'refund_when_replacing_paid_bid':newprice==PAID})
            except (Unsupported,ValueError) as e:limits.append({'phase':'participant_stage_certificate','function':fn,'path':pi,'reason':str(e)})
    return out,limits

def alternative(q,state,shared):
    basis=q.get('policy_basis',{});kind=basis.get('basis') or basis.get('relation') or basis.get('kind');tid=q['target'];fn=q['function'];pi=q.get('path_index')
    allowed=('same_resource_owner_read_to_effect','owner_read_to_effect','same_resource_guarded_operation','source_checked_M2_relation','source_holder_entitlement_disposition','state_controls_authorization; management assumed self-governed','source_payment_beneficiary_reconfiguration','same_source_native_reserve_guard','source_managed_reserve_disposition')
    if kind not in allowed+('v20_source_authority_replacement','v20_semantic_source_authority','v22_source_object_authority_replacement'):return None
    data=shared.get(tid,{})
    if 'participant_stage_certificates' not in data:
        lookup=state['lookups'][tid];program={f:ps for (t,f),ps in state['paths'].items() if t==tid}
        certs,gaps=source_certificates(lookup,program);data['participant_stage_certificates']=certs;data['participant_stage_limits']=gaps
    for cert in data['participant_stage_certificates']:
        if cert['function']!=fn or cert['path_index']!=pi:continue
        origin=basis.get('origin_function')
        if origin and origin!=fn and any(other['function']==origin and other['kind']==cert['kind'] for other in data['participant_stage_certificates']):continue
        source=q.get('effect',{}).get('source')
        relevant=source in cert['effect_sources'] or kind=='same_source_native_reserve_guard' and source in cert['payment_sources']
        if not relevant:continue
        if kind in ('source_holder_entitlement_disposition','source_managed_reserve_disposition') and cert['kind']!='source_owner_listed_paid_object_purchase':continue
        return {'decision':'source_verified_participant_stage_or_sale','source_certificate':copy.deepcopy(cert),'original_policy':q.get('required_policy_candidate'),'scope':'local normal action only; no whole-contract safety conclusion'}
    return None
