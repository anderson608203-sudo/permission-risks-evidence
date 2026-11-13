"""M03 inference: source facts -> LLM proposal -> bound policy -> M3/M4/report.

No expectation, case-id dispatch, or fixed attack sequence. A proposal is a
hypothesis; final results still come from the shared validator.
"""
import json, pathlib
from .core import require, digest

_ACTOR_SRC = {'file': 'method_builtin_controlled_accounts', 'locator': 'fixed controlled test accounts', 'sha256': digest('m03-controlled-accounts-v1')}
DEFAULT_ACTORS = {
    'A': {'kind': 'eoa', 'address': '0x00000000000000000000000000000000000000a1', 'control': 'honest_environment', 'source': dict(_ACTOR_SRC)},
    'B': {'kind': 'eoa', 'address': '0x00000000000000000000000000000000000000b2', 'control': 'controlled', 'source': dict(_ACTOR_SRC)},
    'C': {'kind': 'eoa', 'address': '0x00000000000000000000000000000000000000c3', 'control': 'honest_environment', 'source': dict(_ACTOR_SRC)},
}

def build_context(bundle, contract, native):
    fns = [{'signature': f['signature'], 'visibility': f['visibility'], 'reads': f['reads'], 'writes': f['writes'],
            'source': f.get('source'), 'modifiers': f.get('modifiers', []),
            'nodes': len(f.get('nodes', []))}
           for f in native.get('functions', []) if f.get('contract') == contract['name']]
    from .m03_object_binding import source_structure
    structure, _ = source_structure(bundle, contract, native, DEFAULT_ACTORS)
    return {'source_structure': structure, 'program_id': bundle['program_id'], 'build_id': bundle['build_id'],
            'contract': {'file': contract['file'], 'name': contract['name']},
            'abi': contract.get('abi', []), 'functions': fns,
            'actors': {k: {'address': v['address'], 'control': v['control']} for k, v in DEFAULT_ACTORS.items()},
            'schema': 'm03-permission-proposal-v1',
            'required': ['rule', 'function', 'effect_state', 'authority_state', 'subject']}

def messages(context, project_description=None):
    import json
    prompt = {'task': 'Propose source-grounded permission relations using only the supplied program facts. ' +
                       'Return one JSON object matching the proposal schema. Missing support goes to unresolved.',
              'context': context, 'schema': proposal_schema()}
    if project_description:
        prompt['normal_project_description'] = project_description
    return [{'role': 'system', 'content': 'Return JSON only. Distinguish program facts from inferred policy. JSON.'},
            {'role': 'user', 'content': json.dumps(prompt, sort_keys=True)}]

def propose(client, context, project_description=None, schema_version='v1'):
    """Call the existing Client; provider-default omits max_tokens."""
    # Client.call defaults to 4096/120: omitting Python kwargs does NOT omit
    # the HTTP output limit. None selects the existing provider-default path.
    from .llm_limits import PROVIDER_DEFAULT_CALL_POLICY
    content, receipt = client.call(
        (messages_v2 if schema_version == 'v2' else messages)(context, project_description), 'm03_permission_proposal',
        max_tokens=None, timeout=PROVIDER_DEFAULT_CALL_POLICY['timeout_seconds'],
        reasoning_effort='high', thinking=True)
    return content, receipt


RULES_V2 = {
    'AC-01': 'A subject without the required permission can cause a protected effect; legitimate public operations are not risks.',
    'AC-02': 'A subject without management qualification improperly changes permission state; normal administrator grants are not attacks.',
    'AC-03': 'The checked identity or credential does not match the actual object acted on, with no applicable delegation.',
    'AC-04': 'A qualification that is not yet effective, revoked, expired, or stage-invalid is still accepted.',
    'AC-05': 'A signature or credential has an authorization flaw in subject, resource, domain, nonce, expiry, or replay use.',
    'FCR-TRANSFER': 'A privilege transfers another holder\'s interest without applicable consent.',
    'FCR-MINT': 'A privilege creates new interest, distinguished from ordinary transfer or duplicate accounting.',
    'FCR-DESTROY': 'A privilege destroys another holder\'s interest, distinguished from self-operation or valid delegation.',
    'FCR-PAUSE': 'A fixed privilege blocks transfers in the declared normal domain; check non-empty domain and all relevant paths.',
    'FCR-FREEZE': 'The blocking is specific to a holder; a few failed transactions do not prove a global conclusion.'}

def messages_v2(context, project_description=None):
    import json
    schema = {'schema': 'm03-permission-proposal-v2',
              'rule': 'one of the approved rule IDs',
              'function': 'compiled external function signature',
              'subject': 'declared actor symbol A|B|C; control comes from context, not model choice',
              'authorization': {'kind': 'sender_equals_state|credential|none', 'state': 'state name when applicable'},
              'effect': {'object': 'state object name', 'field': 'specific field name or null for whole object'},
              'basis': 'program_fact|project_description|program_inferred',
              'unresolved': ['one item per unresolved fact, not a string'],
              'covered': {'functions': [], 'objects': []}}
    ctx = dict(context); ctx['schema'] = 'm03-permission-proposal-v2'
    ctx['required'] = ['rule','function','subject','authorization','effect','basis','unresolved','covered']
    prompt = {'task': 'Propose source-grounded permission hypotheses. The rules below are approved meanings. ' +
                       'Return one JSON object matching the v2 schema. Do not treat a missing guard as proof that a risk cannot be proposed. ' +
                       'Separate program facts, inferred policy, and unresolved facts. Whole-object effects must not be silently narrowed to one field.',
              'rules': RULES_V2, 'context': ctx, 'schema': schema}
    if project_description:
        prompt['normal_project_description'] = project_description
    return [{'role': 'system', 'content': 'Return JSON only. Use the approved rule IDs and v2 schema.'},
            {'role': 'user', 'content': json.dumps(prompt, sort_keys=True)}]

def proposal_schema():
    return {'schema': 'm03-permission-proposal-v1', 'rule': 'AC-01|AC-02|AC-03|AC-04',
            'function': 'existing external function signature', 'effect_state': 'state name written by function',
            'authority_state': 'state name written by constructor', 'subject': 'A|B|C',
            'guard': 'optional explanatory text; not an executable condition or independent specification',
            'effect_field': 'optional compiler field name or ast_id for mapping/struct effects',
            'authorization': {'kind': 'sender_equals_state', 'state': 'existing authority state name; required for object effects'},
            'unresolved': 'missing facts; optional references [{kind:function,signature:existing signature,aspect:local_body}]; model criticality flags are not authoritative'}

def _state_name(write):
    return str(write).split('.')[-1]

from .m03_proposal_support import normalize_v2

def materials_from_proposal(proposal, bundle, contract, native, actors=None):
    normalized = None
    if proposal.get('schema') == 'm03-permission-proposal-v2':
        normalized = normalize_v2(proposal)
        proposal = {k: v for k, v in normalized.items() if not k.startswith('_v2')}
    if 'schema' not in proposal and all(k in proposal for k in ('rule','function','effect_state','authority_state','subject')):
        proposal = dict(proposal); proposal['schema'] = 'm03-permission-proposal-v1'
    require(proposal.get('schema') == 'm03-permission-proposal-v1', 'M03_PROPOSAL_SCHEMA')
    require(proposal.get('rule') in {'AC-01', 'AC-02', 'AC-03', 'AC-04', 'FCR-MINT'}, 'M03_RULE_UNSUPPORTED')
    if proposal['rule'] != 'AC-01':
        raise ValueError('M03_RULE_NOT_IMPLEMENTED:' + proposal['rule'])
    fns = [f for f in native.get('functions', []) if f.get('contract') == contract['name']]
    target = [f for f in fns if f['signature'] == proposal.get('function') and f['visibility'] in ('external', 'public')]
    require(len(target) == 1, 'M03_TARGET_FUNCTION_UNRESOLVED')
    target = target[0]
    from .m03_object_binding import bind_object
    object_binding = bind_object(proposal, bundle, contract, native, actors or DEFAULT_ACTORS)
    for p in target.get('parameters', []):
        if p.get('type') not in (('uint256', 'address', 'bool', 'bytes32') if object_binding else ('uint256', 'address', 'bool')):
            raise ValueError('M03_TYPE_NOT_IMPLEMENTED:' + str(p.get('type')))
    if object_binding is None:
        require(all('[' not in w for w in target['writes']), 'M03_OBJECT_PATH_NOT_IMPLEMENTED')
        require(proposal.get('effect_state') in [_state_name(w) for w in target['writes']], 'M03_EFFECT_UNBOUND')
    ctor = [f for f in fns if f['signature'] == 'constructor()' or f['signature'].startswith('constructor(')]
    require(len(ctor) == 1, 'M03_CONSTRUCTOR_UNRESOLVED')
    require(proposal.get('authority_state') in [_state_name(w) for w in ctor[0]['writes']], 'M03_AUTHORITY_UNBOUND')
    require(proposal.get('subject') in (actors or DEFAULT_ACTORS), 'M03_SUBJECT_UNBOUND')
    ac = actors or DEFAULT_ACTORS
    source_sha = proposal.get('source_sha256')
    proposal_sha = digest(proposal)
    pid = 'PROGRAM_INFERRED_' + digest(proposal)[:12]
    policy = {'kind': 'authority_effect', 'rule': proposal['rule'],
              'policy_id': pid,
              'policy_scope': 'program_inferred_development',
              'text': proposal.get('guard') or 'Program-inferred candidate; final check is source-bound.',
              'source': {'file': contract['file'], 'sha256': source_sha,
                         'origin': 'program_inferred', 'record_id': pid,
                         'proposal_basis': proposal.get('proposal_basis')},
              'inferred': True,
              'applies_to': [{'program_id': bundle['program_id'], 'build_id': bundle['build_id'],
                              'contract_file': contract['file'], 'contract_name': contract['name'],
                              'basis': {'kind': 'program_inferred_policy',
                                        'policy_sha256': proposal_sha,
                                        'source_sha256': source_sha},
                              'inferred': True}],
              'typed_relations': {'authority_state': proposal['authority_state'],
                                  'effect_state': proposal['effect_state']}}
    if object_binding:
        policy['typed_relations']['object_effect'] = object_binding
    raw = proposal.get('unresolved')
    raw = [] if raw is None or raw == '' else list(raw) if isinstance(raw, list) else [raw]
    return {'policy': policy, 'actors': ac, 'target_function': target,
            'unresolved': raw, 'critical_unresolved': [], 'inferred': True,
            'normalized_proposal': normalized}


def run_proposal(proposal, bundle, contract, native, actors, settings, rpc, fingerprint, output, service_factory=None, project_description=None):
    from .completion import prepare_static_candidates
    from .component_queries import prepare_queries
    from .validation_run import validate_component, report_component_results
    from .m03_object_binding import classify_unresolved
    output = pathlib.Path(output)
    output.mkdir(parents=True, exist_ok=True)
    original_proposal = proposal
    if proposal.get('schema') == 'm03-permission-proposal-v2':
        proposal = {k: v for k, v in normalize_v2(proposal).items() if not k.startswith('_v2')}
    if proposal.get('authorization', {}).get('kind') == 'none':
        from .m03_permission_hypotheses import discover
        context = build_context(bundle, contract, native)
        hypotheses = discover(context, original_proposal if original_proposal is not proposal else proposal, project_description)
        (output / 'permission_hypotheses.json').write_text(json.dumps(hypotheses, ensure_ascii=False, indent=2), encoding='utf-8')
        derived = []
        for candidate in hypotheses.get('candidates', []):
            names = {d['ast_id']: d for d in context['source_structure']['declarations']}
            effect_selector = candidate['effect']
            object_name = str(effect_selector.get('object', '')).split('.')[-1]
            declaration = next((d for d in context['source_structure']['declarations'] if d['name'] == object_name), None)
            if declaration is None: continue
            field_by_id = {f['ast_id']: f for f in declaration['fields']}
            auth_selector = candidate['required_policy_candidate']
            selectors = []
            def collect(v):
                if isinstance(v, dict):
                    if v.get('kind') == 'state_selector' and v.get('value_type') in ('address', 'address payable'):
                        selectors.append(v)
                    for child in v.values(): collect(child)
                elif isinstance(v, list):
                    for child in v: collect(child)
            collect(auth_selector)
            if len(selectors) != 1: continue
            authority = names.get(selectors[0]['declaration_id'])
            if authority is None: continue
            for path in candidate['basis'].get('target_paths', []):
                field_id = path['segments'][-1].get('field_id') if path.get('segments') else None
                field = field_by_id.get(field_id)
                if field is None: continue
                derived.append({'schema': 'm03-permission-proposal-v1', 'rule': 'AC-01',
                    'function': candidate['function'], 'subject': candidate['subject'],
                    'effect_state': declaration['name'], 'effect_field': field['name'],
                    'authority_state': authority['name'],
                    'authorization': {'kind': 'sender_equals_state', 'state': authority['name']},
                    'guard': 'source-relation hypothesis: ' + str(candidate['basis'].get('relation')),
                    'unresolved': [], 'source_remarks': proposal.get('unresolved', []), 'whole_object': True})
        (output / 'derived_proposals.json').write_text(json.dumps(derived, ensure_ascii=False, indent=2), encoding='utf-8')
        if not derived:
            return {'status': 'hypotheses_proposed_no_derived_plan', 'rows': [], 'leads': [], 'unresolved': proposal.get('unresolved', []), 'inferred': True,
                    'candidates': len(hypotheses.get('candidates', [])), 'hypotheses': str(output / 'permission_hypotheses.json'),
                    'reason': 'hypotheses exist but no supported whole/field update plan'}
        from .m03_result_rollup import aggregate
        children = []
        for index, derived_proposal in enumerate(derived):
            try:
                sub = run_proposal(derived_proposal, bundle, contract, native, actors, settings, rpc, fingerprint,
                    output / ('derived_' + str(index)), service_factory=service_factory, project_description=project_description)
            except (ValueError, KeyError, IndexError, TypeError) as error:
                sub = {'status': 'derived_failed', 'rows': [], 'reason': type(error).__name__ + ':' + str(error)}
            children.append(sub)
        result = aggregate(children, {'candidates': len(hypotheses.get('candidates', [])), 'derived': len(derived),
            'hypotheses': str(output / 'permission_hypotheses.json')})
        (output / 'derived_results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        return result
    def save(name, value):
        (output / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    m = materials_from_proposal(proposal, bundle, contract, native, actors)
    m['original_proposal'] = original_proposal if original_proposal is not proposal else None
    save('inferred_materials.json', m)
    settings = dict(settings or {})
    settings.setdefault('concrete_scalar', 1)
    settings.setdefault('expiry_offset', 10)
    settings.setdefault('mode', 'concrete')
    static = prepare_static_candidates(bundle, contract, native, m['actors'], m['policy'])
    prepared = prepare_queries(bundle, contract, static, m['policy'], settings)
    save('prepared_queries.json', prepared)
    if not prepared.get('prepared'):
        return {'status': 'no_prepared_queries', 'rows': [], 'leads': prepared.get('leads', []),
                'unresolved': m['unresolved'], 'inferred': True}
    selected = []
    for item in prepared['prepared']:
        if item.get('source_relation', {}).get('frame', {}).get('entry', {}).get('function') != proposal['function']:
            continue
        # Select by actual sender, not whether a partition string mentions B/C.
        address = item['alias_case'].get('mapping', {}).get(proposal['subject'], {}).get('address')
        if item['plan']['transactions'][-1]['sender'] == address:
            selected.append(item)
    if not selected:
        return {'status': 'no_candidates_for_proposed_subject_and_function', 'rows': [],
                'leads': prepared.get('leads', []), 'unresolved': m['unresolved'], 'inferred': True}
    rows, unresolved = [], []
    for item in selected:
        item.setdefault('input_id', contract['name'])
        other, critical = classify_unresolved(m['unresolved'], item, bundle, contract)
        item['unresolved_details'] = critical + other
        # Frozen transport interfaces require string items; retain the full
        # structured reasons locally and serialize them without dropping facts.
        item['unresolved'] = [json.dumps(x, ensure_ascii=False, sort_keys=True) for x in item['unresolved_details']]
        unresolved.extend(item['unresolved'])
        item['unresolved_critical'] = bool(critical)
        item['proposal_subject'] = proposal['subject']
        item['source_remarks'] = proposal.get('source_remarks', [])
        if proposal.get('whole_object'):
            from .source_paths import SourcePaths
            from .m03_typed_observers import lower_object_effect
            lookup = SourcePaths(bundle, contract)
            claim = m['policy']['typed_relations']['object_effect']
            state = lookup.decls.get(claim['effect']['state_ast_id'])
            if state and state.get('typeName'):
                typ = state['typeName']
                while typ.get('nodeType') == 'Mapping': typ = typ['valueType']
                struct = lookup.nodes.get(typ.get('referencedDeclaration'), {})
                members = [x['id'] for x in struct.get('members', [])]
                tx = item['plan']['transactions'][-1]
                key_value = int(str(tx['arguments'][0]), 0) if tx.get('arguments') else 1
                selector = {'kind': 'state_selector', 'program_id': bundle['program_id'], 'build_id': bundle['build_id'],
                            'instance_id': contract['file'] + ':' + contract['name'], 'declaration_id': state['id'],
                            'segments': [{'key': {'kind': 'parameter', 'id': 0}, 'type': 'uint256'}]}
                widened = lower_object_effect(lookup, selector, field_ids=members, sender=tx['sender'],
                                              parameter_values={0: key_value}, before=2, after=3)
                item['query']['effect_expression'] = widened['effect_expression']
                item['plan']['observers'] = list(item['plan'].get('observers', [])) + widened['observers']
                item['whole_object_effect'] = {'field_ids': members, 'scope': widened['scope'], 'effect_expression': widened['effect_expression']}
                item['assessment_records'] = [{'original': remark, 'disposition': 'retained_policy_or_scope_condition',
                                               'basis': 'M1 programme relation and current query plan; report keeps original and inferred-policy scope'}
                                              for remark in proposal.get('source_remarks', [])]
        item['query']['proposal_subject'] = proposal['subject']
        item['query']['proposal_effect_state'] = proposal['effect_state']
        item['query']['proposal_guard'] = proposal.get('guard')
        item['policy_scope'] = 'inferred_policy'
        save('bound_item_' + item['id'] + '.json', item)
        # Factory constructs a lazy per-item adapter. Validation checks critical
        # gaps/declarations before select(), which is the first process start.
        client = service_factory(item) if service_factory is not None else rpc
        try:
            rows.append(validate_component(client, item, bundle, output / 'items' / item['id'], fingerprint))
        finally:
            if service_factory is not None:
                client.close()
    report_component_results(rows, prepared.get('leads', []), fingerprint, output / 'report')
    blocked = [r for r in rows if r.get('outcome_kind') == 'critical_unresolved']
    status = 'blocked_by_critical_unresolved' if len(blocked) == len(rows) else 'partial_completed' if blocked else 'completed'
    return {'status': status, 'rows': rows, 'leads': prepared.get('leads', []),
            'unresolved': unresolved, 'inferred': True, 'report': str(output / 'report')}
