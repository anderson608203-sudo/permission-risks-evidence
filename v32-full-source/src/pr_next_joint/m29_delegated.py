"""A third-party balance transfer can create an AC question without an owner guard."""
from .m03_p_paths import key, lit, op, walk
from .m03_p_route import effective_permission, keys, selectors
from .m04_logic import Unsupported
from .m05_asset_obligations import consent_model
from .m05_control_baseline import transfer_summary
from .m11_policy import make_query
from .m22_assets import matches, unique
from .m27_effect_checks import SENDER, semantic_assets


def duties(context, state, shared, relations, queue):
    rows = []
    for target, lookup in state['lookups'].items():
        program = {fn: ps for (t, fn), ps in state['paths'].items() if t == target}
        assets = unique(list(shared.get(target, {}).get('assets', ())) +
                        semantic_assets(context, relations, state, target, program))
        for asset in assets:
            routes = []
            for fn, pi in queue.asset_paths(target, asset):
                path = program[fn][pi]
                if path.get('native_transfers') or path.get('sensitive_effects'):
                    continue
                try:
                    route = transfer_summary(path, asset, lookup)
                except Unsupported as exc:
                    queue.note(target, fn, pi, 'unsupported', str(exc))
                    continue
                if route and not route.get('source_fee_witness') and not route.get('asset_keys'):
                    routes.append((fn, pi, path, route))
            own = [route['debit']['source'] for _, _, _, route in routes
                   if route['holder'] == SENDER and route['recipient'].get('kind') == 'parameter']
            if not own:
                continue
            for fn, pi, path, route in routes:
                holder, recipient = route['holder'], route['recipient']
                if holder.get('kind') != 'parameter' or recipient.get('kind') not in ('parameter', 'actual_sender'):
                    continue
                if lookup.function(fn).get('stateMutability') == 'payable':
                    continue
                # Consider a plain transfer only. A different custody/price/claim
                # record can authorize a settlement and needs its own consumer.
                if any(not matches(w['path'], asset) for w in path['writes']):
                    continue
                if any(s['root'] != asset['balance_root'] for s in selectors(path['guards'])):
                    continue
                if any(n.get('kind') in ('hash','credential_recovery','unknown','environment','external_call')
                       for n in walk(path['guards'])):
                    continue
                try:
                    consent, certs = consent_model(path,holder,route['amount_terms'],lookup,program,
                        asset['balance_root'],asset.get('supply_root'),recipient=recipient)
                except Unsupported as exc:
                    queue.note(target,fn,pi,'unsupported',str(exc),route['debit']['source'])
                    continue
                required = op('or',consent,*effective_permission(path['guards'],lookup))
                model = dict(path)
                model['guards'] = [*path['guards'], op('!=',holder,SENDER),op('==',recipient,SENDER),
                                   op('!=',holder,lit(0)),op('>',route['amount'],lit(0))]
                basis = {'basis':'source_third_party_transfer_to_caller_without_applicable_holder_authority',
                         'self_service_debit_sites':own,'asset':asset['balance_root'],
                         'holder':holder,'credit_site':route['credit']['source'],'consent_evidence':certs,
                         'relation_ids':[asset['relation_id']] if asset.get('relation_id') else [],
                         'scope':'committed transfer of independently self-spendable units to an unrelated caller'}
                q = make_query(context,target,fn,pi,model,route['debit'],required,basis,'AC-03')
                rows.append(q)
                queue.note(target,fn,pi,'dispatched','third_party_transfer',route['debit']['source'],basis['relation_ids'])
    return rows
