"""Source-scoped upstream authority for public entitlement creation.

Resolve an administrator-assigned, consumed issuance allowance. A public draw
does not erase the issuer's control. Arbitrary dependencies remain named gaps.
"""
from .m03_p_paths import key,walk,op,lit,conditions_possible

def issuance_controls(path,amount,changes,lookup,program,models):
    from .m03_p_route import effective_permission,selectors,keys,value_type
    from .m03_p_assets import negative
    atom_roots={m['balance_root'] for m in models}|{m['supply_root'] for m in models}
    dependencies={s['root'] for g in path['guards'] for s in selectors(g)}
    dependencies.update(s['root'] for c in changes for s in selectors(c['write']['value']) if s['root'] not in atom_roots)
    controls=[];resolved=[]
    for fn,paths in program.items():
        for origin in paths:
            if origin['flow']=='reverted' or origin['issues']:continue
            permission=effective_permission(origin['guards'],lookup)
            if not permission:continue
            for assigned in origin['writes']:
                target=assigned['path'];value=assigned['value']
                if target['root'] not in dependencies or target['root'] in atom_roots:continue
                evidence={'issuer_function':fn,'issuer_permission':permission,'assigned_state':target,
                          'assigned_value':value,'source':assigned['source'],'issuer_conditions':origin['guards']}
                controls.append(evidence)
                if amount is None or value.get('kind')!='parameter' or not str(value_type(target,lookup)).startswith('uint'):continue
                # An exact discretionary assignment, no simultaneous funding or
                # entitlement conversion. Arbitrary computed/paid credits do not
                # qualify as privileged issuance by this relation alone.
                if origin.get('native_transfers') or any(w['path']['root'] in atom_roots for w in origin['writes']):continue
                if any(x.get('kind')=='transaction_value' for x in walk(origin)):continue
                producer_keys=keys(target)
                if len(producer_keys)!=1 or producer_keys[0].get('kind')!='parameter' or producer_keys[0].get('type') not in ('address','address payable'):continue
                for consumed in changes:
                    selector=consumed['write']['path']
                    if selector['root']!=target['root'] or consumed['delta']!=negative(amount):continue
                    if keys(selector)!=[{'kind':'actual_sender'}]:continue
                    from .m03_p_assets import term
                    quantity=term(amount)
                    if quantity is None:continue
                    if conditions_possible(path['guards'],op('>=',selector,quantity)):continue
                    if conditions_possible(path['guards'],op('>',quantity,lit(0))):continue
                    resolved.append({**evidence,'consumed_allowance':consumed['write'],
                        'quantity':quantity,'holder':{'kind':'actual_sender'},
                        'scope':'conditional source composition: privileged assignment followed by holder draw; no deployment or transaction claim'})
    return resolved,controls
