"""Typed source references for M2 relation slots, never inferred predicates.

An AST ID, an existing scoped expression, a source quote and explanatory prose
are different objects. This boundary does not execute/parse model-generated
code or turn text into holder consent, privilege or a required policy.
"""
import copy
import hashlib
import json
import re

from .m03_p_paths import key, walk

SLOTS = ('participants', 'resources', 'amount', 'credential', 'consent', 'control')
BOUND = frozenset(('source_bound', 'term_bound'))
DESCRIPTION_FIELDS = frozenset(('text', 'description', 'explanation', 'kind',
                                'role', 'effect', 'name', 'asset', 'label', 'title'))


def bound_slot_ids(binding, slot):
    return sorted({aid for item in binding.get('slots', {}).get(slot, [])
                   if item.get('status') in BOUND
                   for aid in item.get('source_ast_ids', [])})


def bound_slot_terms(binding, slot):
    return [copy.deepcopy(item['term'])
            for item in binding.get('slots', {}).get(slot, [])
            if item.get('status') == 'term_bound' and 'term' in item]


def _span(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d+:\d+:\d+', value):
        return None
    return tuple(map(int, value.split(':')))


def _lookup_index(context, state, target):
    """Index compiler/source-derived data, not proposal decisions."""
    lookup = state.get('lookups', {}).get(target)
    if lookup is None:
        return None
    identity = context.get('identity', {})
    if any(identity.get(field) != lookup.bundle.get(field)
           for field in ('program_id', 'build_id')):
        return None
    source_values = context.get('sources', [])
    sources = {}
    for source in source_values:
        if not isinstance(source, dict) or not isinstance(source.get('content'), str):
            continue
        raw = source['content'].encode('utf-8')
        expected = source.get('sha256')
        if expected and hashlib.sha256(raw).hexdigest() != expected:
            continue
        sources[source.get('file')] = raw
    files = {}
    for filename, ast in lookup.bundle.get('ast_sources', {}).items():
        span = _span(ast.get('src'))
        if span is not None:
            files[span[2]] = filename
    index = {}
    for aid, node in lookup.nodes.items():
        span = _span(node.get('src'))
        if span is None:
            continue
        start, size, source_id = span
        filename = files.get(source_id)
        raw = sources.get(filename)
        text = None
        if raw is not None and start + size <= len(raw):
            try:
                text = raw[start:start + size].decode('utf-8')
            except UnicodeDecodeError:
                pass
        index[aid] = {'node': node, 'span': span, 'text': text,
                      'location': {'file': filename, 'start': start, 'length': size,
                                   'source_id': source_id, 'ast_id': aid}}
    return lookup, index


def _function_terms(state, target, function):
    values = [state.get('paths', {}).get((target, function), [])]
    for item in state.get('bindings', {}).values():
        if not isinstance(item, dict):
            continue
        fn = item.get('function') or item.get('row', {}).get('function')
        if item.get('target') == target and fn == function:
            values.append(item)
    return {key(node) for value in values for node in walk(value) if node.get('kind')}


def build_relation_binding(proposal, context, state, allowed_ids):
    """Return source-bound slots; unresolved references do not become formulas.

    ``allowed_ids`` is supplied by the independently reconstructed operation
    graph. Its reachability allows locating source only, never equates callers,
    resource keys, instances or temporal states.
    """
    target, function = proposal.get('target'), proposal.get('function')
    allowed = {x for x in allowed_ids if type(x) is int}
    indexed = _lookup_index(context, state, target)
    lookup, index = indexed if indexed else (None, {})
    allowed &= set(index)
    terms = state.get('terms', {})
    scoped_terms = _function_terms(state, target, function)
    slots = {slot: [] for slot in SLOTS}
    unresolved = []
    provenance = {'kind': 'compiler_source_reference', 'target': target,
                  'function': function, 'identity': copy.deepcopy(context.get('identity')),
                  'grants_semantic_equivalence': False}

    def emit(slot, path, kind, value, ids=None, status='source_bound', reason=None,
             term=None, candidates=None):
        if slot in ('participants','resources') and any(
                part in ('amount','quantity','destroyed_amount','transferred_amount','issued_amount')
                for part in path.split('/')):
            slot='amount'
        ids = sorted(set(ids or []))
        record = {'reference_path': path, 'reference_kind': kind,
                  'status': status, 'original_reference': copy.deepcopy(value),
                  'source_ast_ids': ids,
                  'node_types': {str(aid): index[aid]['node'].get('nodeType') for aid in ids},
                  'source_locations': [copy.deepcopy(index[aid]['location']) for aid in ids],
                  'source_types': {str(aid): index[aid]['node'].get('typeDescriptions', {}).get('typeString')
                                   for aid in ids},
                  'provenance': copy.deepcopy(provenance)}
        if reason:
            record['reason'] = reason
        if term is not None:
            record['term'] = copy.deepcopy(term)
        if candidates is not None:
            record['candidate_source_ast_ids'] = sorted(candidates)
        slots[slot].append(record)
        if status == 'unresolved':
            unresolved.append({'slot': slot, 'reference_path': path,
                               'reference_kind': kind, 'reason': reason,
                               'original_reference': copy.deepcopy(value)})

    def source_ids(slot, path, value, multiple=False):
        ids = value if multiple and isinstance(value, list) else [value]
        if multiple and value==[]:
            emit(slot,path,'empty_reference_list',value,status='explanation_only',
                 reason='no_cited_source; absence_is_not_proved_by_this_list')
        elif not ids or any(type(x) is not int for x in ids):
            emit(slot, path, 'source_ast_ids' if multiple else 'source_ast_id', value,
                 status='unresolved', reason='source_reference_shape')
        elif any(x not in allowed for x in ids):
            emit(slot, path, 'source_ast_ids' if multiple else 'source_ast_id', value,
                 status='unresolved', reason='source_reference_outside_bound_operation_scope')
        else:
            emit(slot, path, 'source_ast_ids' if multiple else 'source_ast_id', value, ids)

    def quoted(slot, path, value, explicit=False):
        if not isinstance(value, str) or not value.strip():
            emit(slot, path, 'expression_ref', value, status='unresolved',
                 reason='expression_reference_shape')
            return
        token = value.strip()
        if token in terms:
            term = terms[token]
            if key(term) not in scoped_terms:
                emit(slot, path, 'registered_term', value, status='unresolved',
                     reason='registered_term_not_in_target_function')
                return
            referenced = {n[f] for n in walk(term) for f in ('root', 'id', 'field')
                          if type(n.get(f)) is int and n[f] in index}
            if not referenced <= allowed:
                emit(slot, path, 'registered_term', value, status='unresolved',
                     reason='registered_term_source_outside_scope')
                return
            emit(slot, path, 'registered_term', value, referenced, status='term_bound', term=term)
            return
        if token.startswith('e_'):
            emit(slot, path, 'registered_term', value, status='unresolved',
                 reason='invalid_registered_term')
            return
        span = _span(token)
        kind = 'solc_source_range' if span else 'exact_source_quote'
        candidates = [aid for aid in sorted(allowed)
                      if (index[aid]['span'] == span if span else index[aid]['text'] == token)]
        # Multiple AST wrappers for the same byte range are all source locations
        # of one syntax span. Distinct source occurrences remain ambiguous.
        spans = {index[aid]['span'] for aid in candidates}
        if candidates and len(spans) == 1:
            emit(slot, path, kind, value, candidates)
        elif len(spans) > 1:
            emit(slot, path, kind, value, status='unresolved',
                 reason='source_quote_ambiguous', candidates=candidates)
        elif explicit:
            emit(slot, path, kind, value, status='unresolved',
                 reason='source_quote_or_range_not_found')
        else:
            emit(slot, path, 'explanation', value, status='explanation_only',
                 reason='prose_not_used_as_expression_or_predicate')

    def consistency(slot,value,path):
        # Only syntactically explicit sibling locations can constrain display
        # metadata. Never resolve a description by searching repeated text.
        aids=[]
        for name,child in value.items():
            if name.endswith('_ast_ids') and isinstance(child,list):aids.extend(x for x in child if type(x)is int and x in allowed)
            elif name.endswith('_ast_id') and type(child)is int and child in allowed:aids.append(child)
        if not aids:return
        def lhs(node):
            if node.get('nodeType')=='ExpressionStatement':return lhs(node.get('expression',{}))
            if node.get('nodeType')=='Assignment':return node.get('leftHandSide',{})
            if node.get('nodeType')=='UnaryOperation' and node.get('operator') in ('++','--','delete'):return node.get('subExpression',{})
            return node
        nodes=[lhs(index[aid]['node']) for aid in aids]
        declared=value.get('type')
        if isinstance(declared,str) and re.fullmatch(r'(?:address(?: payable)?|bool|u?int(?:\d+)?|bytes(?:\d+)?)',declared):
            actual={n.get('typeDescriptions',{}).get('typeString','').split(' storage')[0].split(' memory')[0] for n in nodes}
            actual={x for x in actual if x and x!='tuple()' and not x.startswith('function')}
            canon=lambda x: {'uint':'uint256','int':'int256'}.get(x,x)
            if actual and canon(declared) not in {canon(x) for x in actual}:
                emit(slot,path+'/type','source_metadata_conflict',declared,status='unresolved',reason='explicit_type_conflicts_with_cited_source')
        display=value.get('path')
        if isinstance(display,str) and re.fullmatch(r'[A-Za-z_]\w*(?:\[[A-Za-z_]\w*\]|\.[A-Za-z_]\w*)*',display):
            cited=[]
            for n in nodes:
                info=index.get(n.get('id'),{});text=info.get('text')
                if isinstance(text,str):cited.append(re.sub(r'\s+','',text))
            simple=[x for x in cited if re.fullmatch(r'[A-Za-z_]\w*(?:\[[A-Za-z_]\w*\]|\.[A-Za-z_]\w*)*',x)]
            if simple and display not in simple:
                emit(slot,path+'/path','source_metadata_conflict',display,status='unresolved',reason='explicit_display_path_conflicts_with_cited_source')

    def visit(slot, value, path):
        if isinstance(value, list):
            for i, child in enumerate(value):
                visit(slot, child, path + '/' + str(i))
        elif isinstance(value, dict):
            consistency(slot,value,path)
            for name, child in value.items():
                next_path = path + '/' + name
                if name.endswith('_ast_ids'):
                    source_ids(slot, next_path, child, multiple=True)
                elif name.endswith('_ast_id'):
                    source_ids(slot, next_path, child)
                elif name in ('expression_ref', 'ref', 'source_quote', 'source_range', 'src'):
                    quoted(slot, next_path, child, explicit=True)
                elif name in DESCRIPTION_FIELDS and isinstance(child, str):
                    emit(slot, next_path, 'explanation', child, status='explanation_only',
                         reason='prose_not_used_as_expression_or_predicate')
                else:
                    visit(slot, child, next_path)
        elif isinstance(value, str):
            emit(slot,path,'explanation',value,status='explanation_only',reason='only_explicit_reference_fields_locate_source')
        elif value is not None:
            emit(slot, path, 'untyped_value', value, status='explanation_only',
                 reason='untyped_value_not_used_as_predicate')

    mechanism = proposal.get('mechanism', {})
    for slot in SLOTS:
        if isinstance(mechanism, dict) and slot in mechanism:
            visit(slot, mechanism[slot], 'mechanism/' + slot)
    bound = sorted({aid for records in slots.values() for record in records
                    if record['status'] in BOUND for aid in record['source_ast_ids']})
    graph_nodes = [{'id': 'operation', 'kind': 'operation', 'target': target, 'function': function}]
    graph_edges = []
    for slot, records in slots.items():
        for i, record in enumerate(records):
            node = slot + ':' + str(i)
            graph_nodes.append({'id': node, 'kind': 'relation_slot_reference',
                                'slot': slot, 'status': record['status']})
            graph_edges.append({'source': 'operation', 'target': node, 'kind': 'declared_slot'})
            for aid in record['source_ast_ids']:
                graph_edges.append({'source': node, 'target': 'ast:' + str(aid),
                                    'kind': 'compiler_source_binding'})
    graph_nodes += [{'id': 'ast:' + str(aid), 'kind': 'compiler_ast',
                     'source_ast_id': aid, 'node_type': index[aid]['node'].get('nodeType')}
                    for aid in bound]
    return {'schema': 'source-relation-binding-v1', 'target': target, 'function': function,
            'identity': copy.deepcopy(context.get('identity')),
            'slots': slots, 'bound_source_ids': bound, 'unresolved_references': unresolved,
            'graph': {'nodes': graph_nodes, 'edges': graph_edges,
                      'scope': 'source reference edges only; not holder/instance/state equivalence'},
            'prose_consumed_as_predicate': False,
            'scope': 'Typed source references; consumers must reconstruct program semantics and query obligations.'}
