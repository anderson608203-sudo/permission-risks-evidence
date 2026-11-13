"""Bounded M3 object-effect plans from source-bound M1 frames and an M2 claim.

No compiler/LLM/backend calls. No project names or expected results. The current
shape is one mapping key, a flat struct field, and one legitimate whole-record
initializer. Every generated plan still requires original execution and replay.
"""
import copy

from .core import require, digest, ref, lit, obs, operator
from .environment import environment
from .facts import walk
from .instances import descriptor
from .multi_service import PLAN_SCHEMA, validate_plan
from .source_observers import bind_getter, describe_getter
from .source_paths import SourcePaths


def _parameter(term):
    require(term.get('kind') == 'parameter', 'object_parameter_origin_unresolved')
    return term['declaration']['ast_id']


def _field(segment):
    value = segment.get('field')
    return value.get('ast_id') if isinstance(value, dict) else value


def _family(path):
    return (path['program_id'], path['build_id'], path['instance_id'], path['declaration']['ast_id'])


def _path(lookup, path):
    require(path.get('kind') == 'storage_binding', 'object_qualified_path_required')
    require(path['program_id'] == lookup.bundle['program_id'] and path['build_id'] == lookup.bundle['build_id'],
            'object_path_identity')
    require(path['instance_id'] == lookup.contract['file'] + ':' + lookup.contract['name'], 'object_instance_identity')
    segments = path['segments']
    require(len(segments) == 2 and 'key' in segments[0] and 'field' in segments[1],
            'object_single_key_flat_field_shape')
    return _parameter(segments[0]['key']), _field(segments[1])


def _same_object(left, right):
    return _family(left) == _family(right) and _parameter(left['segments'][0]['key']) == _parameter(right['segments'][0]['key'])


def _positive_paths(condition):
    if condition.get('kind') == 'storage_binding':
        yield condition
    elif condition.get('kind') == 'op' and condition.get('op') == '&&':
        for child in condition['args']:
            yield from _positive_paths(child)


def _corroborated(write):
    status = write.get('corroboration', {}).get('status')
    require(status == 'compiler_and_native_keys_correlated', 'object_native_key_correspondence_unresolved')


def _arguments(frame, values):
    ids = [binding['parameter']['ast_id'] for binding in frame['entry']['argument_bindings']]
    require(len(ids) == len(set(ids)) and set(ids) == set(values), 'object_unbound_or_extra_argument')
    return [str(values[i]) for i in ids]


def _parameter_type(frame, ident):
    bindings = [b for b in frame['entry']['argument_bindings'] if b['parameter']['ast_id'] == ident]
    require(len(bindings) == 1, 'object_parameter_not_in_entry')
    return bindings[0]['term']['compiler_type']


def _value(typ, number):
    require(type(number) is int and 0 <= number < 2 ** 256, 'object_test_value_range')
    if typ == 'bytes32':
        return '0x' + format(number, '064x')
    if typ == 'uint256':
        return str(number)
    raise ValueError('object_effect_value_type_unsupported:' + typ)


def _relation(bundle, contract, static, candidate, record, policy, lookup):
    # Reuse the existing identity-checked, single-frame consumer and deployment
    # authority binding. The new adapter does not invent a weaker identity path.
    from .component_queries import frames, unique, constructor_authority, authority_guard
    claim = policy['typed_relations']['object_effect']
    require(policy['kind'] == 'authority_effect' and policy.get('rule', 'AC-01') == 'AC-01', 'object_rule_scope')
    require(policy.get('source') and any(
        p.get('program_id') == bundle['program_id'] and p.get('build_id') == bundle['build_id']
        and p.get('contract_file') == contract['file'] and p.get('contract_name') == contract['name']
        and p.get('basis') for p in policy.get('applies_to', [])), 'object_policy_scope')
    require(claim.get('authorization') == {'kind': 'sender_equals_state', 'state_ast_id': claim['authority_ast_id']},
            'object_authorization_relation_unsupported')
    frame = frames(static, candidate)
    require(frame['entry']['function'] == claim['function'], 'object_target_function')
    writes = [r for r in frame['relationships'] if r['operation'] == 'write'
              and r['path']['declaration']['ast_id'] == claim['effect']['state_ast_id']
              and r['path']['segments'] and _field(r['path']['segments'][-1]) == claim['effect']['field_ast_id']]
    effect = unique(writes, 'object_effect_field_not_unique')
    require(effect['operator'] == '=', 'object_effect_assignment_adapter')
    key_id, field_id = _path(lookup, effect['path'])
    value_id = _parameter(effect['value'])
    require(value_id != key_id, 'object_key_value_binding_alias')
    _corroborated(effect)
    observed = describe_getter(lookup, effect['path'])
    require(observed['abi_type'] in ('bytes32', 'uint256') and observed['key_types'] == ['uint256'],
            'object_fixed_word_uint_key_shape')
    require(_parameter_type(frame, value_id) == observed['abi_type']
            and _parameter_type(frame, key_id) == 'uint256', 'object_effect_parameter_type')
    required_states = []
    for guard in frame['guards']:
        for guarded in _positive_paths(guard['condition']):
            try:
                _path(lookup, guarded)
                if _same_object(guarded, effect['path']) and describe_getter(lookup, guarded)['type'] == 'Bool':
                    required_states.append(guarded)
            except (ValueError, KeyError):
                continue
    exists = unique(required_states, 'object_positive_existence_guard_unresolved')
    exists_field = _field(exists['segments'][-1])
    authority = constructor_authority(lookup, claim['authority_ast_id'])
    initializers = []
    rejected_prefixes = []
    for other in record['candidates']:
        if other['entry']['function'] == claim['function']:
            continue
        try:
            prefix = frames(static, other)
            for write in prefix['relationships']:
                p = write.get('path', {})
                if write.get('operation') != 'write' or p.get('kind') != 'storage_binding':
                    continue
                if _family(p) != _family(effect['path']) or len(p['segments']) != 1:
                    continue
                require('key' in p['segments'][0] and write.get('operator') == '=', 'object_initializer_assignment')
                prefix_key = _parameter(p['segments'][0]['key'])
                value = write.get('value', {})
                require(value.get('kind') == 'record', 'object_whole_record_initializer_required')
                members = value['fields']
                active = unique([f['value'] for f in members if _field(f) == exists_field], 'object_initializer_existence_field')
                require(active == {'kind': 'literal', 'value': True}, 'object_initializer_does_not_activate')
                init_effect = unique([f['value'] for f in members if _field(f) == field_id], 'object_initializer_effect_field')
                prefix_value = _parameter(init_effect)
                require(_parameter_type(prefix, prefix_key) == 'uint256'
                        and _parameter_type(prefix, prefix_value) == observed['abi_type'], 'object_initializer_parameter_type')
                _corroborated(write)
                guarded = authority_guard(lookup, prefix)
                require(guarded['path']['declaration']['ast_id'] == claim['authority_ast_id'], 'object_prefix_other_authority')
                initializers.append({'candidate': other, 'frame': prefix, 'write': write,
                                     'key_parameter': prefix_key, 'value_parameter': prefix_value, 'authority': guarded})
        except (ValueError, KeyError, IndexError, TypeError) as error:
            rejected_prefixes.append({'entry': other['entry']['function'], 'reason': str(error)})
    prefix = unique(initializers, 'object_legitimate_initializer_not_unique')
    return {'kind': 'authority_effect_object', 'rule': 'AC-01', 'frame': frame, 'effect': effect,
            'key_parameter': key_id, 'value_parameter': value_id, 'existence': exists,
            'authority': authority, 'initializer': prefix, 'observer_binding': observed,
            'association': {'policy': ref(policy), 'typed_claim': claim},
            'unselected_prefix_limits': rejected_prefixes, 'critical_unresolved': []}


def prepare_object_queries(bundle, contract, static, policy, settings):
    if policy['typed_relations']['object_effect']['effect'].get('scope') == 'whole_record':
        from .object_creation_queries import prepare_creation_queries
        return prepare_creation_queries(bundle, contract, static, policy, settings)
    from .component_queries import RULE_CHECKS
    require(all(static['input'][k] == bundle[k] for k in ('program_id', 'build_id')), 'static_program_identity')
    require(not contract['constructor_types'], 'constructor_arguments_unresolved')
    require(settings.get('mode', 'concrete') == 'concrete', 'object_concrete_adapter_only')
    claim = policy['typed_relations']['object_effect']
    lookup = SourcePaths(bundle, contract)
    prepared, leads, cases = [], [], []
    for record in static['alias_cases']:
        case = copy.deepcopy(record['case'])
        cases.append(case)
        if case['status'] != 'applicable':
            continue
        for candidate in record['candidates']:
            if candidate['entry']['function'] != claim.get('function'):
                continue
            try:
                relation = _relation(bundle, contract, static, candidate, record, policy, lookup)
                addresses = {k: v['address'] for k, v in case['mapping'].items()}
                subject = claim['subject']
                require(subject in addresses, 'object_subject_not_declared')
                sender = addresses[subject]
                deployer = settings['deployment_address_basis']['sender']
                require(deployer in addresses.values(), 'object_deployer_not_declared')
                key = settings.get('object_key', 1)
                require(type(key) is int and 0 <= key < 2 ** 256, 'object_key_range')
                abi_type = relation['observer_binding']['abi_type']
                before_value = _value(abi_type, settings.get('object_initial_value', 1))
                after_value = _value(abi_type, settings.get('object_update_value', 2))
                effect = bind_getter(lookup, relation['effect']['path'], [str(key)])
                exists = bind_getter(lookup, relation['existence'], [str(key)])
                authority = bind_getter(lookup, {'kind': 'storage', 'root': claim['authority_ast_id'], 'segments': []}, [])
                require(authority['type'] == 'Address160', 'object_authority_address_type')
                entry = descriptor(bundle, contract)
                pid = digest(entry)
                iid = contract['file'] + ':' + contract['name']
                plan = {'schema': PLAN_SCHEMA, 'id': digest({'candidate': candidate['id'], 'policy': policy,
                        'alias_case': case['id'], 'settings': settings}), 'programs': {pid: entry},
                        'instances': {iid: {'program_id': pid, 'target': settings['deployment_address_basis']['target']}},
                        'accounts': sorted(set(addresses.values())),
                        'environment': environment(settings['block_number'], settings['timestamp']),
                        'transactions': [], 'observers': []}
                def tx(function, arguments, caller):
                    plan['transactions'].append({**plan['instances'][iid], 'instance_id': iid, 'sender': caller,
                        'function': function, 'arguments': arguments, 'environment': plan['environment'], 'value': 0, 'gas': 12000000})
                tx('constructor', [], deployer)
                prefix = relation['initializer']
                tx(prefix['frame']['entry']['function'], _arguments(prefix['frame'],
                    {prefix['key_parameter']: str(key), prefix['value_parameter']: before_value}), deployer)
                tx(relation['frame']['entry']['function'], _arguments(relation['frame'],
                    {relation['key_parameter']: str(key), relation['value_parameter']: after_value}), sender)
                for oid, binding in [('authority', authority), ('object_exists', exists), ('effect', effect)]:
                    plan['observers'].append({**plan['instances'][iid], 'instance_id': iid,
                        'id': oid, 'caller': deployer, **binding['observer_fields']})
                allowed = operator('eq', 'Bool', lit('Address160', sender), obs('authority.2', 'Address160'))
                changed = operator('ne', 'Bool', obs('effect.3', effect['type']), obs('effect.2', effect['type']))
                premise = operator('and', 'Bool', obs('tx1.success', 'Bool'), obs('tx2.success', 'Bool'),
                    operator('eq', 'Bool', obs('authority.1', 'Address160'), lit('Address160', deployer)),
                    operator('eq', 'Bool', obs('authority.2', 'Address160'), lit('Address160', deployer)),
                    operator('not', 'Bool', obs('object_exists.1', 'Bool')), obs('object_exists.2', 'Bool'))
                query = {'rule': 'AC-01', 'query_form': 'EXISTS_VIOLATION', 'premise': premise,
                         'expression': operator('and', 'Bool', operator('not', 'Bool', allowed),
                                                obs('tx3.success', 'Bool'), changed),
                         'policy_allowed': allowed, 'effect_expression': changed,
                         'required_rule_checks': RULE_CHECKS['AC-01'], 'applicability': 'applicable',
                         'policy_kind': 'authority_effect', 'actual_actor_address': sender,
                         'object_key': str(key), 'proposal_subject': subject,
                         'bound_authorization': copy.deepcopy(claim['authorization'])}
                validate_plan(plan)
                prepared.append({'id': plan['id'], 'input_id': bundle.get('id', contract['name']),
                    'candidate_ref': ref(candidate), 'static_ref': ref(static), 'alias_case': case,
                    'scenario': 'proposed_subject_object_update', 'source_relation': relation,
                    'policy': copy.deepcopy(policy), 'policy_scope': 'inferred_policy' if policy.get('inferred') else 'explicit_or_approved',
                    'program_id': bundle['program_id'], 'build_id': bundle['build_id'],
                    'plan': plan, 'query': query, 'mode': 'concrete', 'unresolved': [], 'unresolved_critical': False,
                    'scope': 'one source-bound concrete object/update trajectory; other inputs and paths remain uncovered',
                    'component_only': True, 'LLM_called': False, 'control_only': False, 'purpose': 'risk_candidate',
                    'object_observer_bindings': {'effect': effect, 'existence': exists, 'authority': authority}})
            except (ValueError, KeyError, IndexError, TypeError) as error:
                leads.append({'candidate_ref': ref(candidate), 'case_id': case['id'], 'entry': candidate['entry'],
                              'status': 'unresolved', 'reason': str(error), 'execution_status': 'not_executed'})
    require(len(prepared) * 2 <= 32, 'per_target_plan_cap_including_replay')
    return {'prepared': prepared, 'leads': leads, 'alias_cases': cases, 'static_ref': ref(static),
            'program_id': bundle['program_id'], 'build_id': bundle['build_id'],
            'rule_family': ['AC-01'] if prepared else []}
