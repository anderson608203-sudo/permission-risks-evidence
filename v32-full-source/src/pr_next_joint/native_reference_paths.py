"""Correlate compiler paths with same-function SSA storage references.

This is static provenance only. It establishes neither execution nor policy.
SSA reference addresses and values stored through them are separate: an
Assignment to REF does not redefine the address made by Index/Member.
"""


def correlate(function, function_index, tracer, occurrence, function_node):
    operations = []
    definitions = {}
    for ni, node in enumerate(function['nodes']):
        for oi, op in enumerate(node['ssa']):
            record = (ni, oi, op)
            operations.append(record)
            value = op.get('lvalue')
            if not value:
                continue
            if value.get('class') in ('ReferenceVariableSSA', 'ReferenceVariable'):
                if op['operation'] not in ('Index', 'Member'):
                    continue
            definitions.setdefault(identity(value), []).append(record)

    def pointer(record):
        return '/functions/%d/nodes/%d/ssa/%d' % (function_index, record[0], record[1])

    def read_named(op, name):
        values = [v for v in op.get('reads', []) if v.get('name') == name]
        return values[0] if len(values) == 1 else None

    def join(values):
        if not values or any(v is None for v in values):
            return None
        if any(v[0] != values[0][0] for v in values[1:]):
            return None
        return values[0][0], sorted({p for v in values for p in v[1]})

    def resolve(variable, mode, seen=()):
        if not variable:
            return None
        key = (mode, identity(variable))
        if key in seen:
            return None
        if mode == 'path' and variable.get('class') == 'StateIRVariable':
            canonical = variable.get('canonical_name')
            return ({'root': canonical, 'segments': []}, []) if canonical else None
        defs = definitions.get(identity(variable), [])
        if len(defs) > 1:
            return None
        if not defs:
            if mode != 'term':
                return None
            if variable.get('name') == 'msg.sender' and variable.get('class') == 'SolidityVariableComposed':
                return tracer.frame['caller'], []
            for i, parameter in enumerate(function['parameters']):
                if (variable.get('class') == 'LocalIRVariable'
                    and variable.get('canonical_name')
                    and variable['canonical_name'] == parameter.get('canonical_name')
                    and function_node['id'] == tracer.entry['id'] and i < len(tracer.arguments)):
                    return tracer.literal(tracer.arguments[i]), []
            return None
        record = defs[0]
        op = record[2]
        kind = op['operation']
        seen = seen + (key,)
        result = None
        if kind == 'Assignment' and len(op.get('reads', [])) == 1:
            result = resolve(op['reads'][0], mode, seen)
        elif kind == 'Phi':
            result = join([resolve(v, mode, seen) for v in op.get('reads', [])])
        elif mode == 'path' and kind in ('Index', 'Member'):
            parent = resolve(read_named(op, op.get('variable_left')), 'path', seen)
            if parent is not None:
                path, evidence = parent
                if kind == 'Index':
                    term = resolve(read_named(op, op.get('variable_right')), 'term', seen)
                    if term is not None:
                        result = ({'root': path['root'], 'segments': path['segments'] + [{'key': term[0]}]}, evidence + term[1])
                else:
                    member = read_named(op, op.get('variable_right'))
                    if member and member.get('class') == 'Constant' and member.get('type') == 'string':
                        result = ({'root': path['root'], 'segments': path['segments'] + [{'field': member['name']}]}, evidence)
        if result is None:
            return None
        return result[0], sorted(set(result[1] + [pointer(record)]))

    root = tracer.nodes[occurrence['path']['root']]
    canonical = tracer.nodes.get(root.get('scope'), {}).get('name', '') + '.' + root['name']
    expected = []
    for segment in occurrence['path']['segments']:
        if 'key' in segment:
            expected.append({'key': segment['key']})
        else:
            member = tracer.nodes.get(segment.get('field'))
            if not member:
                return [], []
            expected.append({'field': member['name']})
    wanted = {'root': canonical, 'segments': expected}
    matches, chains = [], []
    anchor = occurrence['source']
    for record in operations:
        ni, oi, op = record
        source = function['nodes'][ni]['source']
        if not (source['start'] <= anchor['start'] and anchor['start'] + anchor['length'] <= source['start'] + source['length']):
            continue
        if occurrence['operation'] == 'write':
            # Use the actual storage target, not a nearby Index for another key.
            if op['operation'] not in ('Assignment', 'Binary', 'Unary', 'Delete'):
                continue
            values = [op.get('lvalue')]
        else:
            values = [op.get('lvalue')] + op.get('reads', [])
        for variable in values:
            result = resolve(variable, 'path')
            if result is None:
                continue
            path, evidence = result
            equal = path == wanted
            chains.append({'canonical_root': path['root'], 'segments': path['segments'],
                'keys': [{'term': s['key']} for s in path['segments'] if 'key' in s],
                'keys_match': equal, 'full_path_match': equal, 'target_ssa_variable': variable['name'],
                'definition_pointers': evidence, 'use_pointer': pointer(record),
                'basis': 'exact SSA references; single Assignment or all-identical Phi inputs; compiler field identity'})
            if equal:
                matches.append({'json_pointer': pointer(record), 'node_source': source,
                    'operation': op['operation'], 'text': op.get('text'), 'definition_pointers': evidence})
    return matches, chains


def identity(variable):
    return variable.get('class'), variable.get('name'), variable.get('canonical_name')
