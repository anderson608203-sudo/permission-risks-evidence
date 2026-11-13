"""Compiler-bound getter descriptions for fixed-word storage observations.

This resolves paths; it does not infer permissions or prove program effects.
Use with SourcePaths and existing plan/program/instance identity validation.
No raw storage slots, model-selected output offsets or project-name dispatch.
"""
import copy
import re

from .core import require


def _elementary(node):
    require(node.get('nodeType') == 'ElementaryTypeName', 'observer_non_elementary_type')
    name = node['name']
    return {'uint': 'uint256', 'int': 'int256', 'address payable': 'address'}.get(name, name)


def describe_getter(lookup, path):
    """Resolve scalar or mapping-chain -> flat struct member against AST + ABI.

    Accept SourcePaths storage paths or normalized storage_binding paths.
    Unbound key terms remain terms; bind_getter requires concrete ABI arguments.
    Unsupported private state/arrays/nested structs are named limitations.
    """
    require(path.get('kind') in ('storage', 'storage_binding'), 'observer_path_kind')
    if path['kind'] == 'storage_binding':
        for key in ('program_id', 'build_id'):
            require(path.get(key) == lookup.bundle[key], 'observer_' + key + '_mismatch')
        root = path['declaration']['ast_id']
    else:
        root = path['root']
    state = lookup.decls.get(root)
    require(state is not None and state.get('stateVariable'), 'observer_state_missing')
    require(state.get('visibility') == 'public', 'observer_public_getter_required')
    bases = lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']])
    require(state.get('scope') in bases, 'observer_state_outside_contract')
    getters = []
    for entry in lookup.contract['functions']:
        if entry['signature'].split('(')[0] != state['name'] or not entry['readonly']:
            continue
        implementation = lookup.function(entry['signature'])
        if implementation.get('generated_getter', {}).get('id') == root:
            getters.append(entry)
    require(len(getters) == 1, 'observer_getter_ambiguous')
    getter = getters[0]
    typ = state['typeName']
    segments = copy.deepcopy(path.get('segments', []))
    key_types, key_terms = [], []
    while typ.get('nodeType') == 'Mapping':
        require(segments and 'key' in segments[0], 'observer_mapping_key_missing')
        key_types.append(_elementary(typ['keyType']))
        key_terms.append(segments.pop(0)['key'])
        typ = typ['valueType']
    require(getter['types'] == key_types, 'observer_getter_input_mismatch')
    field_id = None
    if typ.get('nodeType') == 'UserDefinedTypeName':
        struct = lookup.nodes.get(typ.get('referencedDeclaration'), {})
        require(struct.get('nodeType') == 'StructDefinition', 'observer_struct_required')
        require(len(segments) == 1 and 'field' in segments[0], 'observer_flat_field_required')
        field = segments[0]['field']
        field_id = field.get('ast_id') if isinstance(field, dict) else field
        # Solidity's public getter omits mapping/array members of a struct.
        # bytes/string use ElementaryTypeName and remain ABI outputs.
        returned = [member for member in struct['members']
                    if member['typeName'].get('nodeType') not in ('Mapping', 'ArrayTypeName')]
        require(all(member['typeName'].get('nodeType') == 'ElementaryTypeName'
                    for member in returned), 'observer_nested_struct_unsupported')
        expected_outputs = [_elementary(member['typeName']) for member in returned]
        selected = [index for index, member in enumerate(returned) if member['id'] == field_id]
        require(len(selected) == 1, 'observer_field_not_returned')
        index = selected[0]
    else:
        require(not segments, 'observer_extra_path_segments')
        expected_outputs = [_elementary(typ)]
        index = 0
    require(getter['outputs'] == expected_outputs, 'observer_getter_output_mismatch')
    abi_type = expected_outputs[index]
    value_types = {'bool': 'Bool', 'address': 'Address160', 'uint256': 'BV256', 'bytes32': 'BV256'}
    require(abi_type in value_types, 'observer_fixed_word_type_unsupported:' + abi_type)
    result = {
        'program_id': lookup.bundle['program_id'], 'build_id': lookup.bundle['build_id'],
        'contract_file': lookup.contract['file'], 'contract_name': lookup.contract['name'],
        'root_ast_id': root, 'field_ast_id': field_id,
        'function': getter['signature'], 'selector': getter['selector'],
        'key_types': key_types, 'key_terms': key_terms, 'output_index': index,
        'abi_type': abi_type, 'type': value_types[abi_type],
        'representation': 'abi_word_as_bv256' if abi_type == 'bytes32' else 'native_fixed_word',
    }
    if 'instance_id' in path:
        result['instance_id'] = path['instance_id']
    return result


def bind_getter(lookup, path, arguments):
    """Bind already resolved key values, retaining their ABI order and type.

    Caller still checks that values come from the intended object/subject in
    the current plan. Argument validity alone is NOT a provenance proof.
    """
    result = describe_getter(lookup, path)
    require(len(arguments) == len(result['key_types']), 'observer_argument_count')
    for typ, value in zip(result['key_types'], arguments):
        if typ in ('address', 'bytes32'):
            width = 40 if typ == 'address' else 64
            require(isinstance(value, str) and re.fullmatch('0x[0-9a-fA-F]{' + str(width) + '}', value),
                    'observer_argument_encoding:' + typ)
        elif re.fullmatch('uint([0-9]+)', typ):
            require(not isinstance(value, bool), 'observer_uint_boolean')
            require(isinstance(value, int) or (isinstance(value, str) and re.fullmatch('[0-9]+', value)),
                    'observer_uint_encoding')
            bits = int(typ[4:])
            require(8 <= bits <= 256 and bits % 8 == 0 and 0 <= int(value) < 2 ** bits,
                    'observer_uint_range')
        elif typ == 'bool':
            require(isinstance(value, bool), 'observer_bool_encoding')
        else:
            raise ValueError('observer_key_type_unsupported:' + typ)
    result['arguments'] = copy.deepcopy(list(arguments))
    result['observer_fields'] = {key: result[key] for key in ('function', 'arguments', 'type', 'output_index')}
    return result
