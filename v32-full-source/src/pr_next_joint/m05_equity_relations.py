"""Source-denominated compensation, without cross-asset price assumptions."""
import copy,json
from .m03_p_paths import key,op,lit
from .m04_logic import Unsupported


def linear_quantity(terms):
    """Finite nonnegative source terms in ONE already established ledger unit."""
    if terms is None:raise Unsupported('net_interference_amount_not_linear')
    parts=[]
    for encoded,coefficient in sorted(terms.items()):
        if type(coefficient) is not int or coefficient<0:
            raise Unsupported('net_interference_amount_has_mixed_signs')
        if not coefficient:continue
        atom=lit(1) if encoded=='#' else json.loads(encoded)
        parts.append(atom if coefficient==1 else op('*',lit(coefficient),atom))
    if not parts:return lit(0)
    result=parts[0]
    for part in parts[1:]:result=op('+',result,part)
    return result


def transfer_scope(balances,supply):
    """Finite source-conserved transfers, including splits and multiple debits.

    Distinct typed keys form an explicit subcase. No alias-equivalence or new
    cross-contract asset relation is guessed to make the arithmetic close.
    """
    from .m03_p_route import keys
    if len(balances)<2:raise Unsupported('transfer_pair_not_conserved_and_unique')
    debits=[];credits=[];aggregate={};holders=[]
    for change in balances:
        terms=change['delta']
        if not terms:raise Unsupported('transfer_zero_or_unknown_change')
        if all(n<0 for n in terms.values()):debits.append(change)
        elif all(n>0 for n in terms.values()):credits.append(change)
        else:raise Unsupported('transfer_mixed_holder_net_change')
        kk=keys(change['write']['path'])
        if len(kk)!=1:raise Unsupported('transfer_holder_domain_not_scalar')
        holders.append(kk[0])
        for atom,n in terms.items():aggregate[atom]=aggregate.get(atom,0)+n
    if not debits or not credits or any(aggregate.values()):raise Unsupported('transfer_aggregate_not_conserved')
    if any(d['delta']!= {} for d in supply):raise Unsupported('transfer_supply_not_conserved')
    return {'kind':'bounded_conserved_transfer','conditions':[op('!=',a,b) for i,a in enumerate(holders) for b in holders[i+1:]],
            'balance_changes':copy.deepcopy(balances),'debits':copy.deepcopy(debits),'credits':copy.deepcopy(credits),
            'scope':'finite same-ledger source writes; distinct-holder subcase, source-supply conservation'}


def destruction_scope(balances, supply):
    """Close a finite batch of source-bound debits in one ledger/unit.

    Distinct-holder cases are explicit bounded subcases, not an assertion that
    all source arguments must differ. Alias cases remain outside this model.
    """
    from .m03_p_route import keys
    from .m03_p_paths import op
    if not balances:
        raise Unsupported('destruction_no_bound_balance_change')
    aggregate = {}
    holders = []
    for d in balances:
        if not d['delta'] or not all(v < 0 for v in d['delta'].values()):
            raise Unsupported('destruction_mixed_holder_effect_requires_model')
        kk = keys(d['write']['path'])
        if len(kk) != 1:
            raise Unsupported('destruction_holder_domain_not_scalar')
        holders.append(kk[0])
        for term, value in d['delta'].items():
            aggregate[term] = aggregate.get(term, 0) + value
    if supply and (len(supply) != 1 or supply[0]['delta'] not in (aggregate, {})):
        raise Unsupported('destruction_supply_relation_not_closed')
    return {'kind': 'single_holder' if len(balances) == 1 else 'bounded_distinct_holder_batch',
            'holders': copy.deepcopy(holders),
            'conditions': [op('!=',a,b) for i,a in enumerate(holders) for b in holders[i+1:]],
            'balance_changes': copy.deepcopy(balances), 'supply_changes': copy.deepcopy(supply),
            'aggregate_delta': aggregate,
            'scope': 'finite source writes, same ledger/unit; distinct-holder subcase only when multiple writes'}


def compensation_basis(asset, quantity, payments):
    """Use only the redemption relation already established by the asset builder.

    No new asset/source matching happens here. In particular shares are never
    added to native amounts. Their current redemption quote is a separate,
    explicitly conditional comparison unit when a native payment is present.
    """
    if not payments:
        return {'unit': 'bound_ledger_units', 'entitlement_value': quantity,
                'payments': [], 'basis': 'no_native_compensation_on_this_path'}
    if asset.get('kind') == 'proportional_native_shares':
        old_quantity = asset.get('quantity')
        expression = (asset.get('native_payment') or {}).get('amount')
        if not old_quantity or not expression or not asset.get('reserve') or not asset.get('total_before'):
            raise Unsupported('compensation_conversion_not_bound')
        hits = []
        def replace(value):
            if isinstance(value, dict):
                if key(value) == key(old_quantity):
                    hits.append(True)
                    return copy.deepcopy(quantity)
                return {k: replace(v) for k, v in value.items()}
            return [replace(v) for v in value] if isinstance(value, list) else value
        quoted = replace(expression)
        if not hits:
            raise Unsupported('compensation_quote_quantity_not_bound')
        return {'unit': 'native_value_at_source_redemption_quote', 'entitlement_value': quoted,
                'payments': copy.deepcopy(payments), 'source_relation': copy.deepcopy(asset),
                'basis': 'same_source_share_redemption_expression',
                'scope': 'current source reserve/supply and original integer rounding; no market-price or future-value claim'}
    if asset.get('unit_relation') != 'one ledger unit to one native value unit in this source path':
        raise Unsupported('compensation_conversion_not_bound')
    return {'unit': 'native_value', 'entitlement_value': quantity,
            'payments': copy.deepcopy(payments), 'source_relation': copy.deepcopy(asset),
            'basis': 'source_one_to_one_redemption'}
