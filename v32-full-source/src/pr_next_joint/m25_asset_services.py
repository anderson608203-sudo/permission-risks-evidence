"""Action-specific permissions on asset forfeiture and selective transfer services."""
from .m03_p_paths import key, lit, op, walk
from .m03_p_route import keys
from .m03_p_assets import negative
from .m04_logic import Unsupported
from .m05_state_relations import changes
from .m05_control_baseline import transfer_summary
from .m05_bound_relations import family


def shared_spend_limit(lookup, program, asset, burn_fn, certificates):
    """Require the *same* holder-issued allowance to fund a conserved transfer."""
    if len(certificates) != 1 or 'allowance' not in certificates[0]:
        return None
    limit = certificates[0]['allowance']
    if len(keys(limit)) != 2:
        return None
    for fn, paths in program.items():
        if fn == burn_fn:
            continue
        for path in paths:
            if path['flow'] not in ('normal','returned') or path['issues'] or path.get('evaluation_gaps'):
                continue
            try:
                transfer = transfer_summary(path,asset,lookup)
                if not transfer or not transfer.get('recipient') or transfer['holder'].get('kind') != 'parameter':
                    continue
                for delta in changes(path,lookup):
                    selector = delta['write']['path']
                    if not family(selector,limit) or keys(selector) != [transfer['holder'],{'kind':'actual_sender'}]:
                        continue
                    if delta['delta'] == negative(transfer['amount_terms']):
                        return {'transfer_function':fn,'transfer_debit':transfer['debit']['source'],
                                'allowance_use':delta['write']['source'],'holder_setters':certificates[0]['holder_controlled_setters']}
            except (Unsupported,ValueError):
                continue
    return None


def service_baseline(action, summary, control, fn, asset, lookup):
    from .m05_asset_obligations import privilege
    if not keys(control) or lookup.function(fn).get('visibility') not in ('external','public'):
        return None
    target = keys(control)[0]
    if target.get('kind') not in ('actual_sender','parameter') or not summary.get('credit'):
        return None
    recipient, holder = summary['recipient'], summary['holder']
    if key(target) not in (key(holder),key(recipient)):
        return None
    seller = privilege(action['guards'],lookup,asset['balance_root'])
    if seller and target.get('kind')=='parameter':
        kind='privileged_account_specific_transfer_service'
        permitted=op('or',*seller)
    elif (key(target)==key(recipient) and target.get('kind')=='actual_sender' and
          lookup.function(fn).get('stateMutability')=='payable' and
          any(n.get('kind')=='transaction_value' for n in walk([summary['amount'],action['guards']]))):
        kind='account_specific_paid_delivery'
        permitted=op('>',{'kind':'transaction_value','type':'uint256'},lit(0))
    else:
        return None
    return {'kind':kind,'affected_account':target,'predicate':op('and',permitted,op('!=',holder,recipient)),
            'debit':summary['debit']['source'],'credit':summary['credit']['source'],
            'scope':'only the identified asset service is blocked; independent holder transfers may remain available'}


def separate_mode(selected, other, setter):
    """Two executions of the same branch can use opposite price modes only if
    that specific scalar mode changes. Inspect it before any uncertain call."""
    if setter['issues'] or setter.get('evaluation_gaps') or setter.get('sensitive_effects'):return False
    writes={w['path']['root'] for w in setter['writes']}
    for choice in selected.get('branch_choices',[]):
        mode=choice['condition']
        if mode.get('kind')!='storage' or mode.get('segments') or mode['root'] in writes:continue
        for rival in other.get('branch_choices',[]):
            if rival['source']!=choice['source'] or key(rival['condition'])!=key(mode) or rival['sign']==choice['sign']:continue
            def follows_choice(event):
                loc=event.get('source',{})
                return loc.get('file')==choice['source']['file'] and loc.get('start',-1)>choice['source']['start']
            if all(all(follows_choice(e) for e in branch['issues']+branch.get('evaluation_gaps',[])+branch.get('sensitive_effects',[])+branch['writes']) for branch in (selected,other)):
                return True
    return False

def required_on_delivery(paths, selected, permit, asset, lookup, setter):
    """A fee/routing alternative that still delivers must not be called a block."""
    from .m21_admission import atoms
    from .m03_p_paths import normalize
    needed={key(normalize(a)) for a in atoms(permit)}
    if not needed or selected.get('evaluation_gaps'):return False
    for branch in paths:
        if branch is selected or branch['flow'] in ('reverted','revert'):continue
        if separate_mode(selected,branch,setter):continue
        if branch['flow'] not in ('normal','returned') or branch['issues'] or branch.get('evaluation_gaps'):return False
        if needed <= {key(normalize(a)) for a in atoms(branch['guards'])}:continue
        if any(w['path']['root']==asset['balance_root'] for w in branch['writes']):
            from .m22_assets import matches
            from .m05_state_relations import compose_read
            from .m09_shared_policy import implies
            # A successful bookkeeping branch with no delivery to the
            # requested account cannot substitute for this asset service.
            if branch.get('sensitive_effects') or branch.get('native_transfers') or not all(matches(w['path'],asset) for w in branch['writes']):
                return False
            try:
                requested=transfer_summary(selected,asset,lookup)
                if not requested or not requested.get('credit'):return False
                cell=requested['credit']['path']
                if keys(cell)!=[requested['recipient']] or requested['recipient'].get('kind') not in ('parameter','actual_sender'):
                    return False
                if not implies(lookup,branch,op('<=',compose_read(cell,branch['writes'],lookup),cell)):
                    return False
            except Unsupported:return False
    return True
