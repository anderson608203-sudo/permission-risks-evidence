"""Exact Solidity literal keys in the declared mapping domain. No hash axioms."""
import re

from .m04_logic import Unsupported
from .m05_credential_encoding import fixed_literal


def literal_key(term, declaration):
    raw, length = fixed_literal(term)
    target = declaration.get('keyType', {})
    typ = target.get('name') or target.get('typeDescriptions', {}).get('typeString')
    if declaration.get('nodeType') != 'Mapping':
        raise Unsupported('literal_index_without_mapping_domain')
    if typ in ('string', 'bytes'):
        # Prefixing a byte preserves length, including empty and leading NULs.
        return int('01' + raw, 16)
    match = re.fullmatch(r'bytes([1-9]|[12][0-9]|3[0-2])', typ or '')
    if match and length <= int(match[1]):
        # Solidity pads a string literal with zeros on the right on conversion.
        return int(raw.ljust(2 * int(match[1]), '0'), 16)
    raise Unsupported('literal_key_conversion_outside_mapping_domain')


def selector_equalities(left, right, lookup):
    from .m03_p_paths import lit, op
    declaration = lookup.nodes[left['root']].get('typeName', {})
    tests = []
    # Callers have checked storage root, receiver, field sequence and arity.
    if len(left['segments']) != len(right['segments']):
        raise Unsupported('literal_selector_structure')
    for a, b in zip(left['segments'], right['segments']):
        if 'key' in a and 'key' in b:
            x, y = a['key'], b['key']
            if x.get('kind') == y.get('kind') == 'fixed_bytes_literal':
                tests.append(lit(literal_key(x, declaration) == literal_key(y, declaration)))
            else:
                tests.append(op('==', x, y))
            declaration = declaration.get('valueType', declaration.get('baseType', {}))
        elif a == b and 'field' in a:
            declaration = lookup.nodes[a['field']].get('typeName', {})
        elif a != b:
            raise Unsupported('literal_selector_structure')
    return tests
