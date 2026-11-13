"""C2-bound joint proposal consumption.

The consumer records what was actually consumed, normalized or rejected. A
substitute response is explicitly marked and can never become a real LLM call
or R4-A6 credit. No network or research API is used here.
"""
import hashlib, json, pathlib, re

from .core import require, digest
from .llm_evidence import validate_llm_evidence

HEX64 = re.compile('[0-9a-f]{64}')
REQUIRED = ['id', 'program_id', 'build_id', 'target_refs', 'actors', 'guard_claims',
            'state_claims', 'assumptions', 'evidence_refs', 'transaction_plan_refs',
            'unresolved_items']
CONTROLS = {'honest_environment', 'controlled', 'honest', 'attacker', 'unspecified'}
FORBIDDEN_TRUE = {'verified', 'authority', 'trusted', 'self_certified', 'llm_called'}

def _normalize_address(value):
    require(isinstance(value, str) and re.fullmatch('0x[0-9a-fA-F]{40}', value), 'actor_address_format')
    return value.lower()

def _normalize_ref(value, field):
    require(isinstance(value, dict), 'reference_object:' + field)
    require(value.get('id'), 'reference_id:' + field)
    require(isinstance(value.get('sha256'), str) and HEX64.fullmatch(value['sha256']), 'reference_sha256:' + field)
    return {'id': value['id'], 'sha256': value['sha256']}

def consume_proposal(proposal, *, source_kind, batch_binding, output_dir,
                     source_refs=(), root=None, allow_substitute=True, llm_evidence=None):
    """Consume a joint proposal, returning a durable, typed consumption record."""
    require(source_kind in {'llm', 'substitute'}, 'proposal_source_kind')
    require(source_kind != 'substitute' or allow_substitute, 'substitute_proposal_not_allowed')
    require(isinstance(proposal, dict), 'proposal_object')
    require(isinstance(batch_binding, dict) and batch_binding.get('batch'), 'c2_batch_binding_required')
    require(batch_binding.get('c1_ledger_sha256') and batch_binding.get('c2_ledger_sha256'), 'ledger_binding_required')
    root = pathlib.Path(root) if root else pathlib.Path.cwd()
    rejected = []
    SUPPORTED_SCHEMAS = {'c2-joint-proposal-adapter-v1'}
    if proposal.get('schema_version') and proposal.get('schema_version') not in SUPPORTED_SCHEMAS:
        rejected.append({'field': 'schema_version', 'reason': 'unsupported_joint_proposal_schema:' + str(proposal.get('schema_version'))})
    for field in REQUIRED:
        if field not in proposal:
            rejected.append({'field': field, 'reason': 'missing_required_field'})
    if proposal.get('kind') and 'component' in str(proposal['kind']):
        rejected.append({'field': 'kind', 'reason': 'component_proposal_is_not_joint_proposal'})
    for field in FORBIDDEN_TRUE:
        if proposal.get(field) is True:
            rejected.append({'field': field, 'reason': 'proposal_cannot_self_certify_authority_or_llm_call'})
    for field in ['program_id', 'build_id']:
        if field in proposal and not (isinstance(proposal[field], str) and HEX64.fullmatch(proposal[field])):
            rejected.append({'field': field, 'reason': 'invalid_program_or_build_identity'})
    if 'program_id' in proposal and batch_binding.get('program_id') and proposal['program_id'] != batch_binding['program_id']:
        rejected.append({'field': 'program_id', 'reason': 'batch_program_identity_mismatch'})
    if 'build_id' in proposal and batch_binding.get('build_id') and proposal['build_id'] != batch_binding['build_id']:
        rejected.append({'field': 'build_id', 'reason': 'batch_build_identity_mismatch'})

    normalized = {}
    if isinstance(proposal.get('actors'), list):
        actors, seen = [], set()
        for actor in proposal['actors']:
            if not isinstance(actor, dict) or not actor.get('symbol'):
                rejected.append({'field': 'actors', 'reason': 'actor_symbol_required'}); continue
            if actor['symbol'] in seen:
                rejected.append({'field': 'actors', 'reason': 'duplicate_actor_symbol:' + str(actor['symbol'])}); continue
            seen.add(actor['symbol'])
            control = actor.get('control', 'unspecified')
            if control not in CONTROLS:
                rejected.append({'field': 'actors', 'reason': 'unknown_control:' + str(control)}); continue
            actors.append({'symbol': actor['symbol'], 'kind': actor.get('kind', 'eoa'),
                           'control': control,
                           'identity_ref': _normalize_address(actor['identity_ref']) if actor.get('identity_ref') else None})
        normalized['actors'] = actors
    else:
        rejected.append({'field': 'actors', 'reason': 'actor_list_required'})

    for field in ['target_refs', 'evidence_refs', 'transaction_plan_refs']:
        values = proposal.get(field)
        if isinstance(values, list):
            refs = []
            for value in values:
                try:
                    refs.append(_normalize_ref(value, field))
                except ValueError as error:
                    rejected.append({'field': field, 'reason': str(error)})
            normalized[field] = refs
        else:
            rejected.append({'field': field, 'reason': 'reference_list_required'})

    for field in ['guard_claims', 'state_claims', 'assumptions', 'unresolved_items']:
        if isinstance(proposal.get(field), list):
            normalized[field] = proposal[field]
        else:
            rejected.append({'field': field, 'reason': 'typed_list_required'})

    source_checks = []
    for source in source_refs or ():
        try:
            require(isinstance(source, dict) and source.get('path') and source.get('sha256'), 'source_reference_shape')
            path = pathlib.Path(source['path'])
            path = path if path.is_absolute() else root / path
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            require(actual == source['sha256'], 'source_reference_identity')
            source_checks.append({'path': str(path), 'sha256': actual, 'status': 'matched'})
        except (ValueError, OSError) as error:
            source_checks.append({'path': source.get('path') if isinstance(source, dict) else None,
                                  'status': 'rejected', 'reason': str(error)})
            rejected.append({'field': 'source_refs', 'reason': 'source_identity:' + str(error)})

    llm_called = False
    llm_check = None
    if source_kind == 'llm':
        try:
            llm_check = validate_llm_evidence(root, llm_evidence, proposal, batch_binding)
            llm_called = not llm_check.get('simulated')
        except (ValueError, OSError, KeyError) as error:
            rejected.append({'field': 'llm_evidence', 'reason': 'llm_evidence_validation:' + str(error)})
    accepted = not rejected
    record = {
        'schema': 'c2-proposal-consumption-v1',
        'batch': batch_binding['batch'],
        'source_kind': source_kind,
        'substitute': source_kind == 'substitute',
        'llm_called': llm_called,
        'r4_a6_credit': False,
        'proposal_class': 'joint_method_candidate',
        'proposal_schema_version': proposal.get('schema_version'),
        'accepted': accepted,
        'rejected_fields': rejected,
        'normalized': normalized,
        'consumed_fields': sorted(normalized),
        'source_checks': source_checks,
        'missing_fields': [x['field'] for x in rejected if x['reason'] == 'missing_required_field'],
        'batch_binding': {k: batch_binding.get(k) for k in ['batch', 'program_id', 'build_id', 'c1_ledger_sha256', 'c2_ledger_sha256']},
        'no_network': True,
        'no_research_api': True,
        'llm_evidence': llm_check,
        'simulated_llm': bool(llm_check and llm_check.get('simulated')),
        'qualification': 'substitute response does not satisfy R4-A6; real joint execution remains required'
    }
    out = pathlib.Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'proposal_received.json').write_text(json.dumps(proposal, ensure_ascii=False, indent=2), encoding='utf-8')
    (out / 'consumption.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    record['consumption_ref'] = {'id': digest(record), 'sha256': digest(record)}
    return record

def assert_c1_read_only(before_sha, c1_path):
    actual = hashlib.sha256(pathlib.Path(c1_path).read_bytes()).hexdigest()
    require(actual == before_sha, 'C1_LEDGER_CHANGED')
    return actual
