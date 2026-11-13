"""Frozen two-family group boundary, shared by submission and execution adapters.

This module creates pending requests and verifies data; it grants no authority,
reserves no budget and constructs no worker or transport. The trusted adapter
must validate approval, runtime qualification, history and caps BEFORE calling
run_group, and implement claim through its existing persistent claim mechanism.
There is deliberately no direct production CLI here.
"""
import copy
import re
import time

from .core import digest, ref, require
from .joint_flow import _file_ref, _json, _path, _verified, _write, verify_frozen_joint
from .validation_run import validate_component, report_component_results


INPUTS = ('M01_v01', 'M02_v01')
ENTRY_KEYS = {'intent_id', 'input_id', 'target', 'program_id', 'build_id',
              'manifest_ref', 'selected_item_ref', 'item_ref', 'stage', 'plans', 'transactions'}
GROUP_KEYS = {'schema', 'group_id', 'status', 'production_valid', 'input_ids',
              'entries', 'plans', 'transactions', 'simulated_llm', 'runtime_pass', 'r4_a6_credit'}


def _entry(ctx, group_id, manifest_ref, manifest, item, bundle):
    profile = _json(_verified(ctx, manifest['files']['profile']))
    specs = [s for s in profile['inputs'] if s['id'] == manifest['input_id']]
    require(len(specs) == 1, 'joint_group_input_not_unique')
    spec = specs[0]
    # Same target key as c2_component_state.target_key; use its canonical ASCII
    # identity definition, not the method artifact reference encoding.
    from c2_component_state import target_key
    require(type(manifest['plans']) is int and manifest['plans'] == 2 and
            type(manifest['transactions']) is int and manifest['transactions'] > 0,
            'joint_group_count_type')
    entry = {'input_id': manifest['input_id'], 'target': target_key(bundle, spec),
             'program_id': bundle['program_id'], 'build_id': bundle['build_id'],
             'manifest_ref': manifest_ref, 'selected_item_ref': manifest['selected_item_ref'],
             'item_ref': ref(item), 'stage': 'concrete', 'plans': 2,
             'transactions': 2 * len(item['plan']['transactions'])}
    entry['intent_id'] = digest({'kind': 'joint-derived-intent-v1', 'group_id': group_id, **entry})
    return entry


def _shape(group):
    require(isinstance(group, dict) and set(group) == GROUP_KEYS, 'joint_group_shape')
    require(group['schema'] == 'joint-group-request-v1', 'joint_group_schema')
    require(isinstance(group['group_id'], str) and
            re.fullmatch('[A-Za-z0-9_-]{1,80}', group['group_id']), 'joint_group_id')
    require(group['status'] == 'pending_external_approval' and group['production_valid'] is False,
            'joint_group_request_not_authority')
    require(group['runtime_pass'] is False and group['r4_a6_credit'] is False,
            'joint_group_acceptance_not_granted')
    require(group['input_ids'] == list(INPUTS), 'joint_group_input_scope')
    entries = group['entries']
    require(isinstance(entries, list) and len(entries) == len(INPUTS), 'joint_group_cardinality')
    require(all(isinstance(e, dict) and set(e) == ENTRY_KEYS for e in entries), 'joint_group_entry_shape')
    require([e['input_id'] for e in entries] == list(INPUTS), 'joint_group_input_scope')
    require(all(isinstance(e['manifest_ref'], dict) and set(e['manifest_ref']) == {'path', 'sha256'} and
                isinstance(e['manifest_ref']['path'], str) and isinstance(e['item_ref'], dict) and
                set(e['item_ref']) == {'id', 'sha256'} and
                all(type(e[k]) is int and e[k] > 0 for k in ('plans', 'transactions'))
                for e in entries), 'joint_group_entry_fields')
    for key in ('intent_id', 'target'):
        require(len({e[key] for e in entries}) == len(entries), 'joint_group_duplicate_' + key)
    require(len({e['manifest_ref']['path'] for e in entries}) == len(entries), 'joint_group_duplicate_manifest')
    require(len({e['item_ref']['sha256'] for e in entries}) == len(entries), 'joint_group_duplicate_item')
    require(all(type(group[k]) is int and group[k] == sum(e[k] for e in entries)
                for k in ('plans', 'transactions')), 'joint_group_totals')
    require(type(group['simulated_llm']) is bool, 'joint_group_provenance_type')


def freeze_group(ctx, *, group_id, manifest_refs, output):
    """Freeze a pending exact scope AFTER replies; no selection by array index.

    Manifest refs must already be pinned by the preparation adapter. Each is
    fully reconsumed/reapplied. Failure leaves diagnostics, never a valid group.
    """
    ctx.validate()
    out = _path(ctx, output)
    require(not out.exists(), 'joint_output_exists')
    require(isinstance(group_id, str) and re.fullmatch('[A-Za-z0-9_-]{1,80}', group_id), 'joint_group_id')
    require(isinstance(manifest_refs, list) and len(manifest_refs) == len(INPUTS), 'joint_group_cardinality')
    out.mkdir(parents=True, exist_ok=False)
    entries = []
    provenances = []
    for i, manifest_ref in enumerate(manifest_refs):
        manifest, item, bundle = verify_frozen_joint(ctx, manifest_ref, output + '/verify_' + str(i))
        entries.append(_entry(ctx, group_id, manifest_ref, manifest, item, bundle))
        provenances.append(manifest['simulated_llm'])
    require(len(set(provenances)) == 1, 'joint_group_mixed_provenance')
    group = {'schema': 'joint-group-request-v1', 'group_id': group_id,
             'status': 'pending_external_approval', 'production_valid': False,
             'input_ids': list(INPUTS), 'entries': entries,
             'plans': sum(e['plans'] for e in entries), 'transactions': sum(e['transactions'] for e in entries),
             'simulated_llm': provenances[0], 'runtime_pass': False, 'r4_a6_credit': False}
    _shape(group)
    _write(out / 'group_request.json', group)
    return _file_ref(ctx, out / 'group_request.json')


def _read_group(ctx, group_ref):
    group = _json(_verified(ctx, group_ref))
    _shape(group)
    require(ctx.mode != 'production' or group['simulated_llm'] is False,
            'joint_simulated_production_forbidden')
    return group


def group_dependencies(ctx, group_ref):
    """Exact *joint input* dependency closure for production_selection.add().

    Not a complete production package: caller also includes code, backend,
    approval registry/records, history/caps, dispatch and resource configuration.
    This function never reads arbitrary paths recursively from proposal text.
    Missing or changed references fail; same destination with unequal identity
    fails. It does not perform semantic preflight or grant permission.
    """
    group = _read_group(ctx, group_ref)
    refs = {}
    physical = {}
    def add(record):
        path = _verified(ctx, record)
        relative = path.relative_to(ctx.root).as_posix()
        require(relative == record['path'], 'joint_dependency_noncanonical_path')
        key = str(path).casefold()
        if key in physical:
            require(physical[key] == record, 'joint_dependency_path_conflict')
        if relative in refs:
            require(refs[relative] == record, 'joint_dependency_path_conflict')
        refs[relative] = copy.deepcopy(record)
        physical[key] = copy.deepcopy(record)
    add(group_ref)
    for entry in group['entries']:
        add(entry['manifest_ref'])
        manifest = _json(_verified(ctx, entry['manifest_ref']))
        require(manifest.get('schema') in ('joint-frozen-input-v1', 'joint-frozen-input-v2', 'joint-frozen-input-v3'), 'joint_manifest_schema')
        for record in manifest['files'].values():
            add(record)
    return [refs[key] for key in sorted(refs)]


def preflight_group(ctx, *, group_ref, dispatch_entries, output):
    """Verify ALL manifests and exact dispatch scope before any claim/RPC.

    group_ref must be pinned by the independent approved request/dispatch, not
    supplied by the LLM. The caller checks current approval and cumulative caps.
    This returns re-derived snapshots; execution must use these checked items.
    """
    ctx.validate()
    out = _path(ctx, output)
    require(not out.exists(), 'joint_output_exists')
    group = _read_group(ctx, group_ref)
    require(dispatch_entries == group['entries'], 'joint_group_dispatch_binding')
    dependencies = group_dependencies(ctx, group_ref)
    out.mkdir(parents=True, exist_ok=False)
    verified = []
    for i, entry in enumerate(group['entries']):
        manifest, item, bundle = verify_frozen_joint(ctx, entry['manifest_ref'], output + '/input_' + str(i))
        expected = _entry(ctx, group['group_id'], entry['manifest_ref'], manifest, item, bundle)
        require(entry == expected, 'joint_group_entry_binding')
        require(manifest['simulated_llm'] == group['simulated_llm'], 'joint_group_provenance_binding')
        verified.append({'entry': entry, 'manifest': manifest, 'item': item, 'bundle': bundle})
    # Reject changes while preflight was reading a later input.
    for dependency in dependencies:
        _verified(ctx, dependency)
    _write(out / 'preflight.json', {'group_ref': group_ref, 'entries': group['entries'],
                                   'dependencies': dependencies, 'claims': 0, 'rpc_calls': 0})
    return group, verified


def run_group(ctx, *, group_ref, dispatch_entries, output, claim, rpc_factory,
              fingerprint, simulated_execution, on_result=None):
    """Grouped execution body for a trusted, qualified submission adapter.

    claim and rpc_factory are trusted code boundaries, not JSON approval flags.
    Production adapter must supply its existing persistent claims and real RPC;
    tests inject ONLY these external boundaries. No default/no-op is supplied.
    An invalid later manifest causes zero calls to both boundaries.
    """
    require(callable(claim) and callable(rpc_factory), 'joint_group_boundaries_required')
    require(type(simulated_execution) is bool, 'joint_execution_provenance_required')
    require(ctx.mode != 'isolated' or simulated_execution, 'joint_real_execution_in_isolated_forbidden')
    require(ctx.mode != 'production' or not simulated_execution, 'joint_simulated_production_forbidden')
    require(not _path(ctx, output).exists(), 'joint_output_exists')
    group, verified = preflight_group(ctx, group_ref=group_ref, dispatch_entries=dispatch_entries,
                                     output=output + '/preflight')
    out = _path(ctx, output)
    rows, records = [], []
    for i, checked in enumerate(verified):
        entry, item, bundle = checked['entry'], checked['item'], checked['bundle']
        # All checked item snapshots were produced before this first claim.
        claim(copy.deepcopy(entry))
        folder = out / ('input_' + str(i))
        folder.mkdir(parents=True, exist_ok=False)
        client = rpc_factory(copy.deepcopy(item), folder / 'service')
        try:
            row = validate_component(client, item, bundle, folder / 'verification', fingerprint,
                                     deadline=time.monotonic() + 180)
        finally:
            client.close()
        _write(folder / 'result.json', row)
        record = {'intent_id': entry['intent_id'], 'input_id': entry['input_id'],
                  'manifest_ref': entry['manifest_ref'], 'derived_item_ref': ref(item),
                  'outcome_kind': row['outcome_kind'], 'verification_result_ref': row['verification_result_ref'],
                  'result_ref': _file_ref(ctx, folder / 'result.json')}
        records.append(record)
        rows.append(row)
        if on_result is not None:
            on_result(copy.deepcopy(entry), copy.deepcopy(record), copy.deepcopy(row))
    report_component_results(rows, [], fingerprint, out / 'report')
    envelope = {'schema': 'joint-group-result-v1', 'group_ref': group_ref, 'records': records,
                'plans': group['plans'], 'transactions': group['transactions'],
                'simulated_llm': group['simulated_llm'], 'simulated_execution': simulated_execution,
                'runtime_pass': False, 'r4_a6_credit': False, 'method_acceptance_claimed': False}
    _write(out / 'group_result.json', envelope)
    return envelope
