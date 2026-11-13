"""Apply a consumed joint proposal to actual M01/M02 prepared material.

This is deliberately narrower than a new method: it proves that an accepted
proposal resolves to a frozen candidate, bundle and policy, and produces a
derived candidate/query/plan linkage. It does not execute or certify it.
"""
import copy, hashlib, json, pathlib, re

from .core import require, digest, ref
from .llm_evidence import validate_llm_evidence
from .declaration_checks import SUPPORTED as SUPPORTED_DECLARATION_CHECKS, expected_for

HEX64 = re.compile('[0-9a-f]{64}')

BASIS_KINDS = {'program_bundle','policy','alias_case','prepared_query','prepared_plan','source_relation'}

def _independent_basis(basis, selected, bundle, policy):
    if not isinstance(basis, dict):
        return None
    kind = basis.get('kind'); sha = basis.get('sha256')
    if kind not in BASIS_KINDS or not isinstance(sha, str) or not HEX64.fullmatch(sha):
        return None
    values = {'program_bundle': bundle, 'policy': policy,
              'alias_case': selected.get('alias_case') if selected else None,
              'prepared_query': selected.get('query') if selected else None,
              'prepared_plan': selected.get('plan') if selected else None,
              'source_relation': selected.get('source_relation') if selected else None}
    target = values.get(kind)
    if target is None or digest(target) != sha:
        return None
    locator = basis.get('locator')
    if not isinstance(locator, str) or not locator:
        return None
    current = target
    for part in locator.replace('/', '.').split('.'):
        if not part or part == '..':
            return None
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            return None
    return {'kind': kind, 'sha256': sha, 'locator': locator, 'locator_sha256': digest(current) if not isinstance(current, (str, int, bool, type(None))) else digest(current), 'ref': ref(target)}

def _constraint(claim):
    value = claim.get('constraint') if isinstance(claim, dict) else None
    if not isinstance(value, dict) or set(value) != {'target','value'}:
        return None
    if value.get('target') != 'required_rule_checks' or not isinstance(value.get('value'), str) or value['value'] not in SUPPORTED_DECLARATION_CHECKS:
        return None
    return {'target': 'required_rule_checks', 'value': value['value']}

def _ref(value, label):
    require(isinstance(value, dict), 'proposal_reference_object:' + label)
    require(value.get('id') and isinstance(value.get('sha256'), str) and HEX64.fullmatch(value['sha256']), 'proposal_reference_shape:' + label)
    return value

def apply_proposal(proposal, *, source_kind, prepared_items, bundle, policy, output_dir, batch_binding, independent_actors=None, llm_evidence=None, consumption_ref=None, root=None, input_id=None):
    """Resolve a joint proposal to a concrete prepared item and write the linkage.

    Returns a record with applied=False and named rejections rather than
    silently dropping an invalid proposal.
    """
    require(source_kind in {'llm', 'substitute'}, 'proposal_application_source_kind')
    require(isinstance(proposal, dict), 'proposal_application_object')
    require(proposal.get('schema_version') == 'c2-joint-proposal-adapter-v1', 'proposal_application_schema')
    require(isinstance(prepared_items, list) and prepared_items, 'prepared_items_required')
    require(isinstance(bundle, dict) and bundle.get('program_id') and bundle.get('build_id'), 'independent_bundle_required')
    require(isinstance(policy, dict) and policy.get('source'), 'independent_policy_required')
    rejected = []
    if proposal.get('program_id') != bundle['program_id']:
        rejected.append({'field': 'program_id', 'reason': 'independent_bundle_program_id_mismatch'})
    if proposal.get('build_id') != bundle['build_id']:
        rejected.append({'field': 'build_id', 'reason': 'independent_bundle_build_id_mismatch'})
    if proposal.get('kind') and 'component' in str(proposal['kind']):
        rejected.append({'field': 'kind', 'reason': 'component_proposal_not_joint'})
    llm_called = False
    llm_check = None
    if source_kind == 'llm':
        try:
            llm_check = validate_llm_evidence(pathlib.Path(root) if root else pathlib.Path.cwd(), llm_evidence, proposal, batch_binding)
            llm_called = not llm_check.get('simulated')
        except (ValueError, OSError, KeyError) as error:
            rejected.append({'field': 'llm_evidence', 'reason': 'llm_evidence_validation:' + str(error)})

    # Resolve evidence to the independent bundle or policy, not to itself.
    evidence = proposal.get('evidence_refs') or []
    resolved = []
    bundle_digest = digest(bundle); policy_digest = digest(policy)
    for item in evidence:
        if not isinstance(item, dict) or not item.get('sha256'):
            continue
        if item['sha256'] == bundle_digest:
            resolved.append({'kind': 'program_bundle', 'sha256': item['sha256']})
        if item['sha256'] == policy_digest:
            resolved.append({'kind': 'policy', 'sha256': item['sha256']})
    if not any(x['kind'] == 'program_bundle' for x in resolved):
        rejected.append({'field': 'evidence_refs', 'reason': 'no_reference_to_independent_program_bundle'})
    if not any(x['kind'] == 'policy' for x in resolved):
        rejected.append({'field': 'evidence_refs', 'reason': 'no_reference_to_independent_policy'})

    # Resolve target_refs to frozen prepared candidate refs.
    target_refs = proposal.get('target_refs') or []
    candidates = []
    for target in target_refs:
        try:
            target = _ref(target, 'target_refs')
        except ValueError as error:
            rejected.append({'field': 'target_refs', 'reason': str(error)}); continue
        matches = [item for item in prepared_items if any(target == value for value in [item.get('candidate_ref'), ref(item.get('query')), ref(item.get('plan')), ref(item)])]
        if len(matches) == 1:
            candidates.append(matches[0])
        else:
            rejected.append({'field': 'target_refs', 'reason': 'candidate_ref_not_unique:' + str(target.get('id'))})
    # Exact duplicate candidate refs collapse; two different selected items are ambiguous.
    unique_candidates = {digest(item): item for item in candidates}
    if len(unique_candidates) != 1:
        rejected.append({'field': 'target_refs', 'reason': 'proposal_must_resolve_to_one_candidate_for_this_application'})
    selected = next(iter(unique_candidates.values())) if len(unique_candidates) == 1 else None

    # Resolve actor source addresses through the current alias-case normalization.
    actor_links = []
    alias_accounts = (selected or {}).get('alias_case', {}).get('accounts', [])
    alias_mapping = (selected or {}).get('alias_case', {}).get('mapping', {})
    plan_accounts = {str(a).lower() for a in (selected or {}).get('plan', {}).get('accounts', [])}
    for actor in proposal.get('actors') or []:
        symbol = actor.get('symbol')
        source_address = str(actor.get('identity_ref', '')).lower()
        declared = (independent_actors or {}).get(symbol)
        normalized = str(alias_mapping.get(symbol, {}).get('address', '')).lower()
        group = next((a for a in alias_accounts if symbol in a.get('members', [])), None)
        if not declared:
            rejected.append({'field': 'actors', 'reason': 'missing_independent_actor_declaration:' + str(symbol)})
        elif source_address != str(declared.get('address', '')).lower():
            rejected.append({'field': 'actors', 'reason': 'actor_symbol_address_mismatch:' + str(symbol)})
        elif declared.get('control') and actor.get('control') and declared['control'] != actor['control']:
            rejected.append({'field': 'actors', 'reason': 'control_claim_conflicts_with_independent_actor_source:' + str(symbol)})
        elif not group or not normalized:
            rejected.append({'field': 'actors', 'reason': 'actor_not_in_current_alias_case:' + str(symbol)})
        elif not group.get('identity') or str(group['identity'].get('address', '')).lower() != normalized:
            rejected.append({'field': 'actors', 'reason': 'alias_group_identity_mismatch:' + str(symbol)})
        elif normalized not in plan_accounts:
            rejected.append({'field': 'actors', 'reason': 'normalized_actor_address_not_in_frozen_plan:' + str(symbol)})
        else:
            actor_links.append({'symbol': symbol, 'source_address': source_address, 'normalized_address': normalized,
                                'control': actor.get('control'), 'independent_control': declared.get('control'),
                                'alias_group': group.get('members')})
    if not actor_links:
        rejected.append({'field': 'actors', 'reason': 'no_proposal_actor_resolves_to_frozen_plan'})

    if not proposal.get('state_claims'):
        rejected.append({'field': 'state_claims', 'reason': 'empty_state_claims_cannot_select_effect'})
    claim_bindings = []
    if selected:
        for index, claim in enumerate(proposal.get('state_claims') or []):
            kind = claim.get('kind') if isinstance(claim, dict) else None
            if kind == 'source_effect':
                function = claim.get('function'); effect = claim.get('effect')
                actual_function = selected.get('source_relation', {}).get('frame', {}).get('entry', {}).get('function')
                actual_effect = selected.get('source_relation', {}).get('effect', {}).get('path', {}).get('declaration', {}).get('name')
                if set(claim) - {'kind','function','effect'}:
                    rejected.append({'field': 'state_claims[' + str(index) + ']', 'reason': 'unsupported_state_claim_field'})
                elif function != actual_function or effect != actual_effect:
                    rejected.append({'field': 'state_claims[' + str(index) + ']', 'reason': 'source_effect_does_not_match_frozen_candidate'})
                else:
                    claim_bindings.append({'claim': 'state_claims[' + str(index) + ']', 'function': function, 'effect': effect,
                                           'check': 'source_effect_matches_candidate', 'expected': {'function': function, 'effect': effect},
                                           'query_rule': selected['query']['rule'], 'query_ref': ref(selected['query']), 'plan_ref': ref(selected['plan'])})
            else:
                rejected.append({'field': 'state_claims[' + str(index) + ']', 'reason': 'unsupported_claim_kind:' + str(kind)})
        for index, guard in enumerate(proposal.get('guard_claims') or []):
            if not isinstance(guard, dict) or guard.get('rule') != selected['query']['rule']:
                rejected.append({'field': 'guard_claims[' + str(index) + ']', 'reason': 'guard_claim_rule_does_not_match_frozen_query'})
            elif set(guard) - {'kind','rule','basis','constraint'}:
                rejected.append({'field': 'guard_claims[' + str(index) + ']', 'reason': 'unsupported_guard_field'})
            elif not _independent_basis(guard.get('basis'), selected, bundle, policy):
                rejected.append({'field': 'guard_claims[' + str(index) + ']', 'reason': 'guard_claim_basis_not_independent_or_not_matching'})
            elif not _constraint(guard):
                rejected.append({'field': 'guard_claims[' + str(index) + ']', 'reason': 'guard_constraint_not_supported'})
            else:
                claim_bindings.append({'claim': 'guard_claims[' + str(index) + ']', 'rule': guard['rule'], 'basis': _independent_basis(guard.get('basis'), selected, bundle, policy), 'constraint': _constraint(guard), 'query_ref': ref(selected['query'])})
        for index, assumption in enumerate(proposal.get('assumptions') or []):
            if not isinstance(assumption, dict) or not assumption.get('source') or not assumption.get('basis'):
                rejected.append({'field': 'assumptions[' + str(index) + ']', 'reason': 'assumption_requires_source_and_basis'})
            elif set(assumption) - {'id','source','basis','constraint'}:
                rejected.append({'field': 'assumptions[' + str(index) + ']', 'reason': 'unsupported_assumption_field'})
            elif not _independent_basis(assumption.get('source'), selected, bundle, policy) or not _independent_basis(assumption.get('basis'), selected, bundle, policy):
                rejected.append({'field': 'assumptions[' + str(index) + ']', 'reason': 'assumption_source_or_basis_not_independent_or_not_matching'})
            elif not _constraint(assumption):
                rejected.append({'field': 'assumptions[' + str(index) + ']', 'reason': 'assumption_constraint_not_supported'})
            else:
                claim_bindings.append({'claim': 'assumptions[' + str(index) + ']', 'id': assumption.get('id'), 'source': _independent_basis(assumption.get('source'), selected, bundle, policy), 'basis': _independent_basis(assumption.get('basis'), selected, bundle, policy), 'constraint': _constraint(assumption), 'query_ref': ref(selected['query'])})
        unresolved_items = proposal.get('unresolved_items') or []
        if unresolved_items:
            rejected.append({'field': 'unresolved_items', 'reason': 'proposal_has_unresolved_items; not a successful application'})
    else:
        unresolved_items = proposal.get('unresolved_items') or []
    constraint_checks = [b['constraint']['value'] for b in claim_bindings if b.get('constraint')]
    declaration_checks = [{'claim': b['claim'], 'check': b.get('check') or b.get('constraint', {}).get('value'), 'expected': b.get('expected', expected_for(b.get('constraint', {}).get('value'), selected) if selected else None)} for b in claim_bindings if b.get('check') or b.get('constraint')]
    if not proposal.get('guard_claims') and not proposal.get('state_claims'):
        rejected.append({'field': 'claims', 'reason': 'no_typed_claim_to_apply'})

    output = pathlib.Path(output_dir); output.mkdir(parents=True, exist_ok=True)
    record = {'schema': 'c2-proposal-application-v1', 'source_kind': source_kind,
              'substitute': source_kind == 'substitute', 'llm_called': llm_called,
              'r4_a6_credit': False, 'applied': not rejected,
              'status': 'applied' if not rejected else 'rejected',
              'rejected_fields': rejected, 'batch': batch_binding.get('batch'),
              'proposal_ref': {'id': digest(proposal), 'sha256': digest(proposal)},
              'independent_program': {'program_id': bundle['program_id'], 'build_id': bundle['build_id'], 'bundle_sha256': bundle_digest},
              'independent_policy': {'sha256': policy_digest, 'kind': policy.get('kind')},
              'resolved_evidence': resolved, 'actor_links': actor_links, 'claim_bindings': claim_bindings, 'consumption_ref': consumption_ref, 'llm_evidence': llm_check, 'simulated_llm': bool(llm_check and llm_check.get('simulated')),
              'proposal_snapshot': copy.deepcopy(proposal)}
    if selected and not rejected:
        derived = copy.deepcopy(selected)
        derived['id'] = selected['id'] + ':proposal-' + digest(proposal)[:8]
        if input_id is not None:
            derived['input_id'] = input_id
        derived['query'] = copy.deepcopy(selected['query'])
        derived['query']['proposal_ref'] = record['proposal_ref']
        derived['query']['claim_bindings'] = claim_bindings
        derived['query']['required_rule_checks'] = list(derived['query'].get('required_rule_checks', [])) + constraint_checks
        derived['plan'] = copy.deepcopy(selected['plan'])
        derived['proposal_application'] = {'proposal_ref': record['proposal_ref'], 'proposal': copy.deepcopy(proposal), 'consumption_ref': consumption_ref,
                                           'claim_bindings': claim_bindings, 'declaration_checks': declaration_checks, 'selected_item_ref': ref(selected),
                                           'source_kind': source_kind, 'substitute': source_kind == 'substitute',
                                           'llm_called': llm_called, 'r4_a6_credit': False, 'consumption_ref': consumption_ref}
        record['selected_item_ref'] = ref(selected)
        record['query_ref'] = ref(selected['query'])
        record['plan_ref'] = ref(selected['plan'])
        record['derived_query_ref'] = ref(derived['query'])
        record['derived_plan_ref'] = ref(derived['plan'])
        record['derived_item_ref'] = ref(derived)
        record['field_map'] = {'program_id': 'independent_bundle.program_id', 'build_id': 'independent_bundle.build_id',
                               'target_refs[].sha256': 'prepared_item.plan', 'actors[].identity_ref': 'prepared_item.plan.accounts',
                               'actors[].control': 'independent_actor_declaration',
                               'state_claims[].function': 'prepared.source_relation.frame.entry.function',
                               'state_claims[].effect': 'prepared.source_relation.effect.path.declaration.name',
                               'guard_claims[].rule': 'prepared.query.rule', 'guard_claims[].basis': 'independent evidence kind/sha256/locator',
                               'guard_claims[].constraint': 'prepared.query.required_rule_checks',
                               'assumptions[].source/basis': 'independent evidence kind/sha256/locator',
                               'assumptions[].constraint': 'prepared.query.required_rule_checks',
                               'proposal_application.declaration_checks': 'validate_component declaration gate', 'query_ref': 'prepared.query',
                               'plan_ref': 'prepared.plan', 'derived_query_ref': 'derived.query', 'derived_plan_ref': 'derived.plan'}
        (output / 'derived_item.json').write_text(json.dumps(derived, ensure_ascii=False, indent=2), encoding='utf-8')
    (output / 'application.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    return record


def apply_from_config(proposal, *, input_id, root, source_kind, output_dir, batch_binding, prepared_dir, profile_path='configs/c2_component_profile.json', llm_evidence=None, consumption_ref=None):
    """Production entry: bind input_id, program and build identity from the frozen profile."""
    root = pathlib.Path(root)
    require(prepared_dir, 'prepared_material_path_required')
    profile = json.loads((root / profile_path).read_text(encoding='utf-8'))
    spec = next((x for x in profile.get('inputs', []) if x.get('id') == input_id), None)
    require(spec is not None, 'unknown_input_id:' + str(input_id))
    require(spec.get('bundle', {}).get('local') and spec.get('bundle', {}).get('sha256'), 'profile_bundle_identity_required')
    require(spec.get('prepared_digest'), 'profile_prepared_digest_required')
    derived = spec.get('static_source', {}).get('derived_identity') or {}
    require(all(derived.get(k) for k in ['program_id', 'build_id', 'bundle_sha256', 'policy_sha256']), 'profile_derived_identity_incomplete')
    prepared_path = root / prepared_dir / (input_id + '.json')
    require(prepared_path.is_file(), 'prepared_material_missing')
    prepared = json.loads(prepared_path.read_text(encoding='utf-8'))
    require(digest(prepared) == spec['prepared_digest'], 'prepared_digest_mismatch')
    bundle_path = root / spec['bundle']['local']
    require(bundle_path.is_file(), 'bundle_material_missing')
    require(hashlib.sha256(bundle_path.read_bytes()).hexdigest() == spec['bundle']['sha256'], 'bundle_file_identity_mismatch')
    bundle = json.loads(bundle_path.read_text(encoding='utf-8'))
    require(bundle.get('program_id') == derived['program_id'] and bundle.get('build_id') == derived['build_id'], 'bundle_program_build_binding_mismatch')
    require(prepared.get('program_id') == derived['program_id'] and prepared.get('build_id') == derived['build_id'], 'prepared_program_build_binding_mismatch')
    require(digest(spec['policy']) == derived['policy_sha256'], 'policy_derived_identity_mismatch')
    require(digest(bundle) == derived['bundle_sha256'], 'bundle_derived_identity_mismatch')
    return apply_proposal(proposal, source_kind=source_kind, prepared_items=prepared['prepared'], bundle=bundle,
                          policy=spec['policy'], output_dir=output_dir, batch_binding=batch_binding,
                          independent_actors=profile.get('actors'), llm_evidence=llm_evidence,
                          consumption_ref=consumption_ref, root=root, input_id=input_id)
