"""Compiler/source-reference binding for M03 object permission hypotheses.

No program-specific names, supplied policy answers, runtime effects or model
criticality flags are trusted. These helpers do not establish policy truth.
"""
import copy
from .core import require, digest
from .facts import walk
from .source_paths import SourcePaths
from .completion import prepare_static_candidates


def source_structure(bundle, contract, native, actors):
    static = prepare_static_candidates(bundle, contract, native, actors)
    lookup = SourcePaths(bundle, contract)
    scopes = set(lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']]))
    declarations = []
    for node in lookup.decls.values():
        if not node.get('stateVariable') or node.get('scope') not in scopes:
            continue
        typ = node.get('typeName', {})
        while typ.get('nodeType') == 'Mapping':
            typ = typ['valueType']
        struct = lookup.nodes.get(typ.get('referencedDeclaration'), {})
        declarations.append({'ast_id': node['id'], 'name': node['name'],
            'type': node.get('typeDescriptions', {}).get('typeString'), 'source': lookup.anchor(node),
            'fields': [{'ast_id': m['id'], 'name': m['name'], 'type': m.get('typeDescriptions', {}).get('typeString')}
                       for m in struct.get('members', [])]})
    entries = []
    for analysis in static['source_analyses'].values():
        if analysis.get('schema') != 'sourced-bindings-v2':
            entries.append({'entry': analysis.get('entry'), 'unresolved': analysis.get('error')})
            continue
        for frame in analysis['frames']:
            entries.append({k: copy.deepcopy(frame[k]) for k in
                ('entry', 'guards', 'relationships', 'external_calls', 'unresolved')})
    return {'declarations': declarations, 'entries': entries, 'execution_confirmed': False,
            'scope': 'program facts and possible relationships, not permissions or risk labels'}, static


def bind_object(proposal, bundle, contract, native, actors):
    if proposal.get('effect_field') is None:
        return None
    structure, static = source_structure(bundle, contract, native, actors)
    states = structure['declarations']
    def named(name):
        matches = [s for s in states if s['name'] == name]
        require(len(matches) == 1, 'M03_STATE_REFERENCE_NOT_UNIQUE:' + str(name))
        return matches[0]
    effect = named(proposal.get('effect_state'))
    authority = named(proposal.get('authority_state'))
    # A state-name reference denotes the whole object, not an arbitrary member.
    # Preserve that scope and require an actual whole-record write in this entry.
    if proposal['effect_field'] == effect['name'] and effect['fields']:
        require(proposal.get('authorization') == {'kind': 'sender_equals_state', 'state': authority['name']},
                'M03_STRUCTURED_AUTHORIZATION_REQUIRED')
        entries = [e for e in structure['entries'] if e.get('entry', {}).get('function') == proposal['function']]
        require(len(entries) == 1, 'M03_TARGET_SOURCE_FRAME_NOT_UNIQUE')
        writes = [r for r in entries[0]['relationships'] if r.get('operation') == 'write'
                  and r['path']['declaration']['ast_id'] == effect['ast_id']]
        require(len(writes) == 1 and len(writes[0]['path']['segments']) == 1
                and writes[0].get('value', {}).get('kind') == 'record', 'M03_WHOLE_OBJECT_WRITE_UNSUPPORTED')
        ids = [f['ast_id'] for f in effect['fields']]
        written = [f['field'] for f in writes[0]['value']['fields']]
        require(len(written) == len(set(written)) and set(ids) == set(written), 'M03_WHOLE_OBJECT_FIELDS_INCOMPLETE')
        return {'function': proposal['function'], 'subject': proposal['subject'],
                'authority_ast_id': authority['ast_id'],
                'effect': {'state_ast_id': effect['ast_id'], 'field_ast_ids': ids, 'scope': 'whole_record'},
                'authorization': {'kind': 'sender_equals_state', 'state_ast_id': authority['ast_id']}}
    fields = [f for f in effect['fields'] if proposal['effect_field'] in (f['name'], f['ast_id'])]
    require(len(fields) == 1, 'M03_EFFECT_FIELD_NOT_UNIQUE')
    field = fields[0]
    require(proposal.get('authorization') == {'kind': 'sender_equals_state', 'state': authority['name']},
            'M03_STRUCTURED_AUTHORIZATION_REQUIRED')
    entries = [e for e in structure['entries'] if e.get('entry', {}).get('function') == proposal['function']]
    require(len(entries) == 1, 'M03_TARGET_SOURCE_FRAME_NOT_UNIQUE')
    writes = [r for r in entries[0]['relationships'] if r['operation'] == 'write'
              and r['path']['declaration']['ast_id'] == effect['ast_id']
              and r['path']['segments'] and r['path']['segments'][-1].get('field', {}).get('ast_id') == field['ast_id']]
    require(len(writes) == 1, 'M03_EFFECT_FIELD_NOT_WRITTEN_BY_TARGET')
    # Remaining key, initializer, constructor authority and ABI checks are in
    # the actual shared M3 object adapter, not waived by this binding.
    return {'function': proposal['function'], 'subject': proposal['subject'],
            'authority_ast_id': authority['ast_id'],
            'effect': {'state_ast_id': effect['ast_id'], 'field_ast_id': field['ast_id']},
            'authorization': {'kind': 'sender_equals_state', 'state_ast_id': authority['ast_id']}}


def classify_unresolved(raw, item, bundle, contract):
    """Classify uncertainty against the actual plan's source dependency closure.

    Only an explicitly referenced, known other function's local-body limitation
    can be established irrelevant here. Global policy/alternative-authority and
    unknown references remain unresolved for this candidate, not all programs.
    """
    lookup = SourcePaths(bundle, contract)
    roots = [t['function'] for t in item['plan']['transactions']]
    pending = [lookup.function(sig) for sig in roots]
    used = set()
    while pending:
        node = pending.pop()
        if not node or node.get('id') in used:
            continue
        if 'id' in node:
            used.add(node['id'])
        for child in walk(node):
            target = child.get('referencedDeclaration')
            if target in lookup.fns and target not in used:
                pending.append(lookup.fns[target])
    critical, other = [], []
    for original in raw:
        refs = original.get('references') if isinstance(original, dict) else None
        unrelated = isinstance(refs, list) and bool(refs)
        for reference in refs or []:
            if not isinstance(reference, dict) or reference.get('kind') != 'function' or reference.get('aspect') != 'local_body':
                unrelated = False
                break
            if reference.get('program_id', bundle['program_id']) != bundle['program_id'] or reference.get('build_id', bundle['build_id']) != bundle['build_id']:
                unrelated = False
                break
            try:
                node = lookup.function(reference['signature'])
                unrelated = unrelated and bool(node) and 'generated_getter' not in node and node.get('id') not in used
            except (KeyError, ValueError):
                unrelated = False
        record = {'item': copy.deepcopy(original),
                  'classification': 'outside_current_plan_dependency' if unrelated else 'current_query_unresolved',
                  'basis': 'actual plan entry/constructor and AST call/modifier dependency closure',
                  'dependency_ast_ids': sorted(used)}
        (other if unrelated else critical).append(record)
    return other, critical
