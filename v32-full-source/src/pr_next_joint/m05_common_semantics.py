"""Common, pre-solve inputs for bounded source-mechanism consumers.

This module neither discovers source references nor infers missing consent.
The source builders supply already typed models. Consumers read those models
before constructing their risk-specific formulas. Report aggregation performs
no extra solver calls and never uses a previous verdict as a premise.
"""
import copy
from collections.abc import Mapping
from .core import digest
from .m04_logic import Unsupported

SCHEMA = 'm05-common-operation-model-v2'
GROUPS = {'AC-05': 'credential',
          'FCR-TRANSFER': 'equity', 'FCR-DESTROY': 'equity',
          'FCR-PAUSE': 'control', 'FCR-FREEZE': 'control'}
REQUIRED = {
    'credential_invalid_r_zero_acceptance':('credential','conditions','effect','writes','successful_evaluation','authority_acceptance'),
    'credential_declared_expiry_use':('credential','alternative_credential','effect','alternative_effect',
        'conditions','alternative_conditions','deadline','strict_deadline','original_time','later_time',
        'writes','alternative_writes','validity_relation_origin','successful_evaluation','alternative_evaluation'),
    'credential_revoked_boolean_use':('credential','effect','conditions','validity_before','validity_after',
        'revocation_conditions','revocation_writes','post_credential','post_conditions','post_effect',
        'post_selector','post_writes','validity_relation_origin','successful_evaluation','revocation_evaluation','post_evaluation','lifecycle_times'),
    'credential_source_expiry_use': ('credential','alternative_credential','effect','alternative_effect',
        'conditions','alternative_conditions','deadline','strict_deadline','original_time','later_time'),
    'privileged_transfer_blocking': ('pre_action', 'post_action', 'reference_post_action',
        'privilege', 'transition_guards', 'writes', 'holder', 'recipient', 'amount',
        'action_writes', 'transition_time', 'required_scope_matches', 'control',
        'normal_baseline','transfer_request','entry_alternatives','transition_execution_terms'),
    'credential_alternative_use_binding': ('credential', 'alternative_credential', 'effect',
        'alternative_effect', 'conditions', 'alternative_conditions'),
    'credential_same_payload_replay': ('credential', 'post_credential', 'effect', 'conditions',
        'post_conditions', 'post_effect', 'replay_before', 'state_transition'),
    'credential_cross_instance_binding': ('credential', 'second_credential', 'effect',
        'conditions', 'second_instance', 'second_effect', 'own_address', 'other_address'),
    'credential_cross_action_binding': ('credential', 'alternative_credential', 'effect',
        'conditions', 'alternative_conditions', 'alternative_effect'),
    'credential_duplicate_signer_acceptance': ('recovered_signers', 'duplicated_pair', 'effect', 'conditions'),
    'privileged_holder_interference': ('guards', 'debit', 'credit', 'privilege', 'consent',
        'amount', 'same_holder_compensation', 'model', 'writes', 'consent_sources', 'compensation_basis', 'holder_scope','successful_evaluation'),
}


class ModelInputs(Mapping):
    """Immutable-from-consumer inputs plus the fields actually read by it."""
    def __init__(self, data):
        self._data = copy.deepcopy(data)
        self.reads = set()

    def __getitem__(self, field):
        self.reads.add(field)
        return copy.deepcopy(self._data[field])

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)


def prepare(obligation, function, model, root, holder=None):
    """Validate an existing typed binding; never invent a missing relation."""
    kind = model.get('kind')
    if kind not in REQUIRED:
        raise Unsupported('common_model_kind_not_registered:' + str(kind))
    if obligation.get('source_binding_status') != 'source_anchors_bound':
        raise Unsupported('common_model_source_binding_missing')
    identity = obligation.get('identity') or {}
    if not all(identity.get(k) for k in ('program_id', 'build_id')):
        raise Unsupported('common_model_program_identity_missing')
    if not obligation.get('proposal_sha256') or not obligation.get('id'):
        raise Unsupported('common_model_proposal_identity_missing')
    missing = [k for k in REQUIRED[kind] if k not in model or
               (model[k] is None and k != 'credit')]
    if missing:
        raise Unsupported('common_model_required_input_missing:' + ','.join(missing))
    if type(root) is not int:
        raise Unsupported('common_model_typed_resource_missing')
    if not model.get('graph') and not model.get('model'):
        raise Unsupported('common_model_relation_origin_missing')
    # Empty privilege lists are explicit builder results; an absent predicate
    # is different and was rejected above. No null -> false conversion occurs.
    original = obligation.get('original_proposal') or {}
    record = {
        'schema': SCHEMA, 'phase': 'prepared_before_formula',
        'id': 'op_' + digest({'obligation': obligation['id'], 'model': model}),
        'obligation_id': obligation['id'],
        'proposal_id': original.get('id'), 'proposal_sha256': obligation['proposal_sha256'],
        'identity': copy.deepcopy(identity), 'target': obligation['target'],
        'function': function, 'proposal_function': obligation['function'],
        'rule': obligation['rule'], 'group': GROUPS.get(obligation['rule'], 'other'),
        'kind': kind, 'resource': {'root': root},
        'holder': {'status': 'bound', 'expression': copy.deepcopy(holder)} if holder is not None else
                  {'status': 'not_required_by_this_query'},
        'source_ast_ids': copy.deepcopy(obligation.get('source_ast_ids', [])),
        'source_graph': copy.deepcopy(obligation.get('source_reference_graph', {})),
        'model_graph': copy.deepcopy(model.get('graph', {})),
        'model_sha256': digest(model), 'model_inputs': copy.deepcopy(model),
        'relation_scope_consumption':copy.deepcopy(model.get('relation_scope_consumption',{})),
        'basis_assessment': copy.deepcopy(obligation.get('basis_assessment', {})),
        'source_remarks': copy.deepcopy(original.get('unresolved', [])),
        'policy_scope': model.get('policy_scope', 'source_derived_conditional_mechanism'),
        'assumptions': copy.deepcopy(model.get('assumptions', [])),
        'scope': 'already bound source paths and finite related operations; not whole-program semantics',
    }
    if obligation.get('relation_contribution'):
        record['relation_contribution']=copy.deepcopy(obligation['relation_contribution'])
    return record, ModelInputs(model)


def consumed(record, inputs, formal):
    """Receipt for this very query, not a new structural SAT check."""
    if not inputs.reads:
        raise Unsupported('common_model_not_consumed')
    result = copy.deepcopy(record)
    result['phase'] = 'consumed_by_risk_formula'
    result['consumption'] = {
        'fields': sorted(inputs.reads),
        'inputs_sha256': digest({k: inputs._data[k] for k in sorted(inputs.reads)}),
        'solver_called': bool(formal.get('solver_called')),
        'formula_sha256': formal.get('formula_sha256'),
        'semantic_formula_sha256': formal.get('semantic_formula_sha256'),
        'premise': formal.get('premise'), 'query': formal.get('query'),
        'status': formal.get('status'), 'additional_solver_calls': 0,
    }
    return result


def analyze(context, normalized, obligations):
    """Collect pre-solve records and untouched unresolved originals for audit."""
    operations, by_obligation, checks = [], {}, {g: [] for g in set(GROUPS.values())}
    for row in obligations.get('source_obligation_checks', []):
        record = row.get('common_operation')
        if not record:
            continue
        record = copy.deepcopy(record)
        operations.append(record)
        by_obligation.setdefault(record['obligation_id'], []).append(record['id'])
        checks[record['group']].append({'operation_id': record['id'], 'query_id': row['id'],
            'rule': row['rule'], **record['consumption']})
    pending, gaps, relations = [], [], []
    for ob in obligations.get('source_obligations', []):
        refs = by_obligation.get(ob['id'], [])
        entry = {'obligation_id': ob['id'], 'proposal_id': (ob.get('original_proposal') or {}).get('id'),
            'proposal_sha256': ob['proposal_sha256'], 'rule': ob['rule'],
            'operation_ids': refs, 'source_remarks': copy.deepcopy((ob.get('original_proposal') or {}).get('unresolved', [])),
            'model_gaps': copy.deepcopy(ob.get('model_gaps', []))}
        relations.append(entry)
        if not refs:
            pending.append({**entry, 'status': 'no_common_query_model', 'solver_called': False})
        for gap in ob.get('model_gaps', []):
            gaps.append({'obligation_id': ob['id'], 'rule': ob['rule'], **copy.deepcopy(gap)})
    counts = {g: len(rows) for g, rows in sorted(checks.items())}
    return {'schema': SCHEMA, 'operations': operations, 'checks': checks, 'counts': counts,
        'source': 'typed models constructed from existing valid bindings and original M2 proposals before solving',
        'obligation_count': len(relations), 'modeled_obligation_count': len(by_obligation),
        'obligation_links': relations, 'unmodeled_obligations': pending, 'gaps': gaps,
        'additional_solver_calls': 0,
        'not_a_safety_conclusion': True,
        'scope': 'query-specific formal evidence; unmodeled proposals and original limitations retained'}


def attach_report(report, model):
    report['common_operation_model'] = {k: v for k, v in model.items() if k != 'checks'}
    report['common_model_checks'] = model['checks']
    report['common_model_checks_called'] = sum(bool(c['solver_called']) for rows in model['checks'].values() for c in rows)
    report['common_model_additional_solver_calls'] = 0
    return report
