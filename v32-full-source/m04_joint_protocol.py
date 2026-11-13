"""Typed protocol adapters; never repair explicit identities or infer policies."""
import copy
from .core import require, digest
from .m03_p_paths import key, normalize
from .m05_joint_obligations import NEW_RULES

LEGACY_RULES = frozenset(('AC-01', 'AC-02', 'AC-03', 'AC-04', 'FCR-MINT'))


def bind_envelope(raw, expected, authenticated=False):
    """Call only AFTER authenticating the exact request and original response."""
    require(isinstance(raw, dict), 'JOINT_ENVELOPE_OBJECT')
    result = copy.deepcopy(raw)
    records = []
    for field, value in expected.items():
        if field in result:
            require(result[field] == value, 'JOINT_EXPLICIT_ENVELOPE_MISMATCH:' + field)
        else:
            require(authenticated, 'JOINT_MISSING_ENVELOPE_REQUIRES_AUTHENTIC_RECEIPT')
            result[field] = copy.deepcopy(value)
            records.append({'field': field, 'conversion': 'missing_envelope_from_verified_exact_request',
                            'value': copy.deepcopy(value)})
    return result, {'raw_sha256': digest(raw), 'normalized_sha256': digest(result),
                    'authenticated_request': authenticated, 'records': records}


def route_response(response, state):
    """Move only explicitly bound questions to their existing consumer carrier.

    This adapter does not change anchor/resource validation or manufacture a
    required policy. Unrouteable questions stay in their original carrier.
    """
    result = copy.deepcopy(response)
    records, errors = [], []
    legacy = result.get('proposals', [])
    source = result.get('source_obligations', [])
    if not isinstance(legacy, list) or not isinstance(source, list):
        return result, {'records': records, 'errors': [{'reason': 'route_carrier_not_list'}]}
    source_ids = {p.get('id') for p in source if isinstance(p, dict) and isinstance(p.get('id'), str)}
    kept_legacy, kept_source, to_source = [], [], []
    for carrier, items in (('proposals', legacy), ('source_obligations', source)):
        for p in items:
            kept = kept_legacy if carrier == 'proposals' else kept_source
            if not isinstance(p, dict):
                kept.append(p)
                continue
            rule = p.get('rule')
            destination = ('source_obligations' if carrier == 'proposals' and isinstance(rule, str) and rule in NEW_RULES
                           else None)
            if carrier == 'source_obligations' and isinstance(rule, str) and rule in LEGACY_RULES:
                # Never bypass the stricter source scope validator by moving a
                # source question into a legacy carrier before source binding.
                errors.append({'carrier':carrier,'proposal_id':p.get('id'),
                               'reason':'ROUTE_SOURCE_TO_LEGACY_REQUIRES_VALIDATED_SOURCE_BINDING'})
            if destination is None:
                kept.append(p)
                continue
            try:
                require(isinstance(p.get('id'), str) and p['id'], 'ROUTE_ID_REQUIRED')
                candidate, write = p.get('candidate_id'), p.get('write_id')
                require(bool(candidate) != bool(write), 'ROUTE_ONE_EXPLICIT_BINDING_REQUIRED')
                item = state['bindings'].get(candidate or write)
                require(isinstance(item, dict), 'ROUTE_BINDING_NOT_FOUND')
                require(('row' if candidate else 'write') in item, 'ROUTE_BINDING_KIND')
                fn = item.get('function', item.get('row', {}).get('function'))
                pair = (item['target'], fn)
                for field, value in zip(('target', 'function'), pair):
                    if field in p: require(p[field] == value, 'ROUTE_OPERATION_MISMATCH')
                routed = copy.deepcopy(p)
                routed['id'] = 'routed_' + p['id']
                ids = source_ids
                require(routed['id'] not in ids, 'ROUTE_DUPLICATE_ID')
                if destination == 'source_obligations':
                    require(p.get('required') is None, 'ROUTE_CANNOT_DISCARD_REQUIRED_POLICY')
                    require(p.get('policy_decision', 'endorse') == 'endorse', 'ROUTE_DECISION_NEEDS_SOURCE_REVIEW')
                    basis = p.get('basis')
                    require(isinstance(basis, dict) and isinstance(basis.get('source_ast_ids'), list), 'ROUTE_SOURCE_ANCHORS_REQUIRED')
                    routed.update(target=pair[0], function=pair[1],
                                  source_ast_ids=copy.deepcopy(p.get('source_ast_ids',basis['source_ast_ids'])),
                                  review_kind=p.get('review_kind', 'uncertain'),
                                  mechanism=copy.deepcopy(p.get('mechanism', {})))
                    to_source.append(routed)
                ids.add(routed['id'])
                records.append({'from': carrier, 'to': destination, 'original_id': p['id'],
                                'routed_id': routed['id'], 'original_proposal_sha256': digest(p),
                                'target': pair[0], 'function': pair[1],
                                'scope': 'carrier conversion only; original validators still required'})
            except (ValueError, TypeError, KeyError) as ex:
                kept.append(p)
                errors.append({'carrier': carrier, 'proposal_id': p.get('id'), 'reason': str(ex)})
    result['proposals'] = kept_legacy
    result['source_obligations'] = kept_source + to_source
    return result, {'records': records, 'errors': errors}


def revised_model_condition(row, condition):
    """Only the typed boundary of the SAME issued expiry model is replaceable."""
    original = row['required_policy_candidate']
    require(row['rule'] == 'AC-04' and row.get('policy_basis', {}).get('basis') == 'issued_future_expiry',
            'JOINT_MODEL_REVISION_NOT_SUPPORTED')
    require(original.get('kind') == condition.get('kind') == 'op'
            and original.get('op') in ('<', '<=') and condition.get('op') in ('<', '<=')
            and len(original.get('args', [])) == len(condition.get('args', [])) == 2
            and key(normalize(original['args'])) == key(normalize(condition['args'])),
            'JOINT_EXPIRY_REVISION_MUST_PRESERVE_OPERANDS')
    return copy.deepcopy(condition)
