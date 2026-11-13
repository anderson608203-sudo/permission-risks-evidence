"""Compiler-bound evidence for shared roles, outstanding balances and ordinary sales."""
from .m03_p_paths import key,op,lit,walk
from .m03_p_route import keys,selectors,effective_permission,value_type
from .m04_logic import Unsupported


def managed_membership(lookup,program,perm):
    from .m05_writer_scope import gaps_for
    if perm.get('kind')!='storage' or keys(perm)!=[{'kind':'actual_sender'}] or value_type(perm,lookup)!='bool':
        return None
    if gaps_for(lookup,{perm['root']}):
        return None
    found=[]
    for fn,paths in program.items():
        for path in paths:
            if path['flow'] not in ('normal','returned'):continue
            for write in path['writes']:
                if write['path']['root']!=perm['root'] or write['value']==lit(False):continue
                if path['issues'] or path.get('evaluation_gaps'):return None
                guards=effective_permission(path['guards'],lookup)
                if not any(g.get('op')=='==' and any(n.get('kind')=='actual_sender' for n in g.get('args',[]))
                           and any(s.get('kind')=='storage' and not s.get('segments') and value_type(s,lookup) in ('address','address payable') for s in g.get('args',[])) for g in guards):
                    return None
                found.append({'function':fn,'source':write['source']})
    return found


def holder_sale(query,state,shared):
    if query.get('policy_basis',{}).get('basis')!='source_holder_entitlement_disposition':return None
    # A transfer of inventory credited to the buyer may be an authorized sale.
    # Require a source-controlled seller, an affirmative listing/price, and a
    # verified successful transfer of the consideration to that same seller.
    from .m09_shared_policy import implies
    from .m05_writer_scope import gaps_for
    tid=query['target'];lookup=state['lookups'][tid]
    path=state['paths'][(tid,query['function'])][query['path_index']]
    holder=query['policy_basis'].get('holder')
    if holder is None:
        # The M2-linked producer verifies the actor against this selector but
        # does not duplicate the actor in its policy_basis payload.
        owners=keys(query['effect'].get('selector',{}))
        if len(owners)!=1:return None
        holder=owners[0]
    sender={'kind':'actual_sender'}
    if path['issues'] or path.get('evaluation_gaps') or not path.get('native_transfers'):return None
    if lookup.function(query['function']).get('stateMutability')!='payable':return None
    paid={'kind':'transaction_value','type':'uint256'}
    from .m05_state_relations import changes
    from .m03_p_assets import negative
    updates=changes(path,lookup)
    debit=next((d for d in updates if d['write']['source']==query['effect']['source']),None)
    if not debit or not debit['delta']:return None
    if not any(d['write']['path']['root']==debit['write']['path']['root'] and keys(d['write']['path'])==[sender]
               and d['delta']==negative(debit['delta']) for d in updates):return None
    for pay in path['native_transfers']:
        if key(pay['recipient'])!=key(holder):continue
        for price in selectors([pay['amount'],path['guards']]):
            if price.get('segments') or not value_type(price,lookup).startswith('uint'):continue
            if gaps_for(lookup,{price['root']}):continue
            writers=[]
            for (target,fn),branches in state['paths'].items():
                if tid!=target:continue
                for branch in branches:
                    if branch['flow'] not in ('normal','returned'):continue
                    for w in branch['writes']:
                        if key(w['path'])!=key(price):continue
                        try:approved=not branch['issues'] and not branch.get('evaluation_gaps') and implies(lookup,branch,op('==',sender,holder))
                        except (Unsupported,ValueError):approved=False
                        writers.append((approved,w['source']))
            if not writers or not all(approved for approved,_ in writers):continue
            from .m08_financial import quantity
            price_due=op('*',price,quantity(negative(debit['delta'])))
            try:proved=implies(lookup,path,op('and',pay['success'],op('>',price,lit(0)),op('>=',paid,price_due),op('>=',pay['amount'],price_due),op('<=',pay['amount'],paid)))
            except (Unsupported,ValueError):proved=False
            if proved:return {'decision':'seller_priced_inventory_paid_to_holder','source_certificate':{'price':price,'writers':writers,'payment':pay['source']}}
    return None
