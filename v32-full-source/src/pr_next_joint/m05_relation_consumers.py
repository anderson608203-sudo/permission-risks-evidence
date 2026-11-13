"""Consume verified M2 relation references without interpreting role prose.

This module locates source state declarations. It does not infer holder consent,
privilege, key equality or instance equality from a source reference or name.
Those meanings remain obligations of the actual source-path consumers.
"""
import copy


def _state_root(node, lookup, visited=None):
    visited = set() if visited is None else visited
    if not isinstance(node, dict):
        return None
    ident = node.get('id')
    if ident in visited:
        return None
    if ident is not None:
        visited.add(ident)
    if node.get('nodeType') == 'VariableDeclaration' and node.get('stateVariable') is True:
        return node['id']
    kind = node.get('nodeType')
    if kind == 'Identifier':
        declaration = lookup.nodes.get(node.get('referencedDeclaration'), {})
        return _state_root(declaration, lookup, visited)
    if kind in ('MemberAccess', 'IndexAccess', 'IndexRangeAccess'):
        # A struct field declaration alone does not identify a state instance.
        return _state_root(node.get('baseExpression', node.get('expression')), lookup, visited)
    if kind == 'Assignment':
        return _state_root(node.get('leftHandSide'), lookup, visited)
    if kind == 'UnaryOperation':
        return _state_root(node.get('subExpression'), lookup, visited)
    if kind == 'ExpressionStatement':
        return _state_root(node.get('expression'), lookup, visited)
    return None


def _write_syntax(node):
    """Unwrap only compiler statement wrappers around an actual mutation."""
    if not isinstance(node, dict):
        return {}, {}
    while node.get('nodeType') == 'ExpressionStatement':
        node = node.get('expression', {})
    if node.get('nodeType') == 'Assignment':
        return node, node.get('leftHandSide', {})
    if node.get('nodeType') == 'UnaryOperation' and node.get('operator') in ('++', '--', 'delete'):
        return node, node.get('subExpression', {})
    return {}, node


def bound_slot_roots(obligation, lookup, slot):
    """Return source roots referenced by an authenticated mechanism slot.

    Function/block bodies are not expanded to every state they touch. Strings,
    arbitrary ``root`` fields and explanation-only records confer no binding.
    An existing lowered storage term is usable only when the IR marked it bound.
    """
    binding = obligation.get('relation_binding', {})
    records = binding.get('slots', {}).get(slot, [])
    roots = set()
    evidence = []
    for record in records:
        if record.get('status') not in ('source_bound', 'term_bound'):
            continue
        found = set()
        for ident in record.get('source_ast_ids', []):
            if type(ident) is int:
                root = _state_root(lookup.nodes.get(ident), lookup)
                if root is not None:
                    found.add(root)
        term = record.get('term')
        if isinstance(term, dict) and term.get('kind') == 'storage':
            ident = term.get('root')
            declaration = lookup.nodes.get(ident, {})
            if declaration.get('nodeType') == 'VariableDeclaration' and declaration.get('stateVariable') is True:
                found.add(ident)
        if found:
            roots.update(found)
            evidence.append({
                'slot': slot,
                'reference_path': record.get('reference_path'),
                'reference_kind': record.get('reference_kind'),
                'source_ast_ids': copy.deepcopy(record.get('source_ast_ids', [])),
                'storage_roots': sorted(found),
                'reference_provenance': copy.deepcopy(record.get('provenance')),
                'meaning': 'source state location only; no holder, consent, key or instance equivalence',
            })
    return roots, evidence
