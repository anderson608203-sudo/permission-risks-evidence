"""Source-verified seller proceeds plus a fixed protocol fee.
Listing and price control are proved by the caller. A buyer-picked recipient,
unpaid transfer, arbitrary fee or missing successful payment is not a sale.
"""
from .m03_p_paths import op,lit,key,walk
from .m03_p_route import selectors,keys,value_type,effective_permission
from .m09_shared_policy import implies
from .m04_logic import Unsupported
PAID={'kind':'transaction_value','type':'uint256'}

def fee_sale(lookup,program,p,owner,prices):
    try:
        payments=p.get('native_transfers',[])
        if len(payments)==1:return retained_fee_sale(lookup,program,p,owner,prices,payments[0])
        if not 2<=len(payments)<=4:return None
        seller=[x for x in payments if key(x['recipient'])==key(owner)]
        fees=[x for x in payments if key(x['recipient'])!=key(owner)]
        if len(seller)!=1 or not fees:return None
        total=lit(0);proof=[]
        for pay in payments:
            if not implies(lookup,p,pay['success']) or not implies(lookup,p,op('>=',pay['amount'],lit(0))):return None
            total=op('+',total,pay['amount'])
        if not implies(lookup,p,op('>=',seller[0]['amount'],lit(0))):return None
        if not all(implies(lookup,p,op('==',total,price)) for price in prices):return None
        if not implies(lookup,p,op('<=',total,PAID)):return None
        for fee in fees:
            recipient=fee['recipient']
            if any(n.get('kind') in ('parameter','actual_sender') for n in walk(recipient)):return None
            if recipient.get('kind')=='literal' and type(recipient.get('value')) is int and recipient['value']>0:continue
            if recipient.get('kind')!='storage' or keys(recipient) or value_type(recipient,lookup) not in ('address','address payable'):return None
            writers=[]
            for fn,ps in program.items():
                for branch in ps:
                    for w in branch['writes']:
                        if key(w['path'])!=key(recipient):continue
                        if branch['flow']=='reverted':continue
                        if branch['issues'] or branch.get('evaluation_gaps') or not effective_permission(branch['guards'],lookup):return None
                        writers.append(w['source'])
            # Complete source writer inventory, including opaque calls, is
            # needed before treating an apparently fixed fee destination so.
            from .m05_writer_scope import gaps_for
            if gaps_for(lookup,{recipient['root']}):return None
            proof.append({'recipient':recipient,'protected_update_sources':writers})
        return {'kind':'listed_price_equals_seller_plus_protocol_fee','payment_sources':[p['source'] for p in payments],
                'seller_payment':seller[0],'fee_payments':fees,'fee_destinations':proof,'price':prices,
                'scope':'source-listed total consideration; not market fairness or reentrancy proof'}
    except (Unsupported,ValueError,KeyError,TypeError):return None


def retained_fee_sale(lookup,program,p,owner,prices,pay):
    """Seller receives the listed gross price minus a source-defined protocol
    fraction retained by the contract, not an arbitrary buyer-selected cut.
    Listing/price/owner consent is still established by the outer consumer.
    """
    if key(pay['recipient'])!=key(owner):return None
    amount=pay['amount']
    if amount.get('kind')!='op' or amount.get('op')!='-':return None
    price,cut=amount.get('args',[None,None])
    if price is None or not all(key(price)==key(x) for x in prices):return None
    if cut.get('kind')!='op' or cut.get('op')!='/':return None
    numerator,denominator=cut['args']
    if denominator.get('kind')!='literal' or type(denominator.get('value')) is not int or denominator['value']<=0:return None
    rate=lit(1) if key(numerator)==key(price) else None
    if numerator.get('kind')=='op' and numerator.get('op')=='*':
        factors=numerator['args']
        for x,y in (factors,factors[::-1]):
            if key(x)==key(price):rate=y
    if rate is None or any(x.get('kind') in ('parameter','actual_sender') for x in walk(rate)):return None
    rates=selectors(rate)
    from .m05_writer_scope import gaps_for
    for r in rates:
        if keys(r) or not value_type(r,lookup).startswith('uint') or gaps_for(lookup,{r['root']}):return None
        for fn,paths in program.items():
            for branch in paths:
                if branch['flow']=='reverted':continue
                if any(w['path']['root']==r['root'] for w in branch['writes']):
                    if branch['issues'] or branch.get('evaluation_gaps') or not effective_permission(branch['guards'],lookup):return None
    if not implies(lookup,p,pay['success']):return None
    if not implies(lookup,p,op('and',op('>=',amount,lit(0)),op('<=',amount,price),op('<=',price,PAID))):return None
    return {'kind':'source_listed_sale_with_retained_protocol_fraction','payment_sources':[pay['source']],
            'seller_payment':pay,'gross_price':price,'retained_fee':cut,'fee_rate':rate,
            'scope':'source-defined current fee and owner-approved listing; fee-governance risk and price fairness not disproved'}
