"""Execute conditional expressions containing bound internal transitions, in Solidity order."""
import copy

from .m03_p_paths import conditions_possible, lit, normalize, op
from .m11_calls import internal_value_target, invoke_value


def children(node):
    kind = node.get('nodeType')
    if kind == 'BinaryOperation' and node.get('operator') in ('&&', '||') and not node.get('function'):
        return node['leftExpression'], node['rightExpression']
    if kind == 'Conditional':
        return node['condition'], node['trueExpression'], node['falseExpression']
    if kind == 'UnaryOperation' and node.get('operator') == '!' and not node.get('function'):
        return (node['subExpression'],)
    if kind == 'TupleExpression' and not node.get('isInlineArray') and len(node['components']) == 1 and node['components'][0]:
        return tuple(node['components'])
    return ()


def contains_effect_call(lookup, node):
    return any(internal_value_target(lookup, child) or contains_effect_call(lookup, child)
               for child in children(node))


def values(lookup, node, state, depth, shape=None):
    shape = shape or internal_value_target(lookup, node)
    if shape:
        yield from invoke_value(lookup, node, state, depth, shape)
        return
    parts = children(node)
    if not parts:
        value = lookup.expr(node, state)
        yield state, value if state['flow'] == 'normal' else None
        return
    for branch, first in values(lookup, parts[0], state, depth):
        if first is None or len(parts) == 1:
            if first is not None and node.get('operator') == '!':
                first = normalize(op('!', first))
            yield branch, first
            continue
        for truth in (True, False):
            guard = first if truth else op('!', first)
            if not conditions_possible(branch['guards'] + [guard]):
                continue
            selected = copy.deepcopy(branch)
            selected['guards'].append(guard)
            selected.setdefault('branch_choices', []).append({
                'condition': first, 'sign': truth, 'source': lookup.anchor(parts[0])})
            if len(parts) == 3:
                yield from values(lookup, parts[1 if truth else 2], selected, depth)
            elif truth == (node['operator'] == '&&'):
                yield from values(lookup, parts[1], selected, depth)
            else:
                yield selected, lit(truth)
