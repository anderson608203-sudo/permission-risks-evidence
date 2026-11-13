"""Source-anchored questions which do not yet have a formal query translator.

This is a proposal carrier, not a detector. It never constructs an effect, an
authorization predicate or a solver verdict. Existing M04 queries remain a
separate channel; their results cannot complete these obligations by proxy.
"""
import copy
import hashlib
import json

SCHEMA = 'joint-source-obligations-v1'
RULES = ('AC-01', 'AC-02', 'AC-03', 'AC-04', 'AC-05',
         'FCR-MINT', 'FCR-TRANSFER', 'FCR-DESTROY', 'FCR-PAUSE', 'FCR-FREEZE')
NEW_RULES = frozenset(('AC-05', 'FCR-TRANSFER', 'FCR-DESTROY',
                      'FCR-PAUSE', 'FCR-FREEZE'))
MECHANISM_FIELDS = frozenset(('participants', 'resources', 'credential',
                             'consent', 'control', 'amount', 'related_operations'))


def empty_rule_progress():
    """One schema even when this channel has not received a rule yet."""
    return {'received': 0, 'source_bound': 0, 'binding_errors': 0,
            'normal_reviews': 0, 'not_encoded': 0,
            'formal_checks_called': 0, 'supported': 0,
            'refuted_in_scope': 0, 'formal_attempted': 0,
            'conclusive_models': 0, 'inconclusive_models': 0,
            'work_accounting_unknown': False, 'capability_demonstrated': False,
            'progress_scope': 'local constructed models only; not original question or rule completeness'}


def extension_instruction(context=None):
    """Instructions for the opt-in extension; legacy message bytes stay intact."""
    from .m05_question_plan import catalog
    from .task_scope import requested
    active=requested(context or {})
    model_catalog=catalog();model_catalog['rules']={k:v for k,v in model_catalog['rules'].items() if k in active}
    return 'ACTIVE RULES ONLY: '+','.join(active)+'\n'+json.dumps(model_catalog,ensure_ascii=False)+'\n'+'''SOURCE-OBLIGATION CARRIER v3: In the primary response, return
source_obligations in addition to proposals and coverage. In a follow-up return
the review envelope requested above. AC-05, FCR-TRANSFER, FCR-DESTROY,
FCR-PAUSE and FCR-FREEZE use source_obligations, never legacy proposals.
AC-01, AC-02 and AC-03 may use proposals with a matching candidate_id or a
write_id plus an explicit source-bound required permission expression.
AC-04 and FCR-MINT proposals require a matching candidate_id of the SAME rule;
write_id cannot create either model. Otherwise preserve the question as a
source obligation with the actual missing model recorded, not a guessed query.
If a supported exact reference and policy become available,
include policy_decision (endorse/revise/reject/uncertain), preserve required and
basis; the application validates source binding before using the ordinary query
route. Missing decisions/policies remain gaps; never invent them for routing.
The source carrier can describe all ten rules; this does not mean each has
a formal translator in this carrier. A source question is not a solver result.

Each source obligation is {id, rule, target, function, source_ast_ids,
review_kind: "risk_hypothesis"|"normal_review"|"not_applicable"|"uncertain", mechanism,
basis: {kind:"program_relation"|"normal_description"|"combined", explanation},
rationale, alternatives:[strings], unresolved:[{text,impact:
"query_blocking"|"policy_scope"|"unrelated"}]}.
For AC-01/02/03/04 source questions intended for checking, include explicit top-level policy_decision,
candidate_id/write_id and required describe a possible source-to-query bridge.
policy_decision is endorse/revise/reject/uncertain and must express the actual
policy assessment; review_kind is not a substitute. A matching candidate may
be endorsed with required:null to retain its model, or revised with a complete
supported required expression. Without a matching candidate, AC-01/02/03
can use an exact write_id and required expression to create a permission query. AC-04 and FCR-MINT source questions do not require an existing candidate: the planner can construct supported lifecycle/transferable-asset models from the cited source relations. Declare related operations exactly. Missing lifecycle policy remains unknown; a mere source reference is not a model.
If the policy or model is not established, retain uncertainty and the missing
condition. Never add endorse or fabricate required merely to pass a validator.
Use exact target/function/source IDs in source_function_anchors. A source write
is NOT required. All ten approved rules are expressible in this carrier.
For an automatic public state getter, anchor_kind is state_getter and
declaration_ast_id is its source VariableDeclaration; function_ast_id is null
because no source FunctionDefinition exists. It is a real ABI entry with a
source declaration, not an unknown function or a proved runtime observation.
Optional candidate_id/write_id may cite an existing reference from the same
target/function. Use at most one; never put a related operation's write in the
top-level reference or change an expression ID into a write ID.

Normal controls and uncertain mechanisms are legitimate reviews, not forced
positive hypotheses or safety verdicts. Never read expected labels into the
analysis. A missing guard alone is insufficient.
A source question may be not_applicable only as a proposed exclusion; the program
must independently check its necessary conditions. Do not invent a credential
model for random hashes or a transfer-control model for a pure mint/burn.
Amounts belong in mechanism.amount, distinct from actor and asset locations.
Normal operations, rejected candidates and real unknowns are distinct.
AC-05 concerns credential/signature use and binding/replay/validity. The FCR
rules concern source-bound privileged asset/transferable-ledger control mechanisms and applicable
holder consent. This is a mechanism prediction, not proof of funded deployed exploitation.
Record missing initial balances/configuration separately; source structure and operation semantics still require checking. PAUSE concerns a privileged transfer-blocking control in the
declared domain; FREEZE concerns holder-specific blocking. Preserve entrypoints,
holders and exceptions; an all-path universal blocking proof is not required.

Rejection sites in the input are SOURCE ANCHORS ONLY; the ordinary path extractor
has not supplied a complete rejection model. A source-anchored obligation is not
a checked formal query. M3 will preserve these questions and reconstruct
supported models for M4. Missing translators/models remain explicit gaps;
do not predict a solver answer.''' 


def _walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':')).encode()).hexdigest()


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _function_anchor(target, function, lookup):
    try:
        ast = lookup.function(function)
    except (KeyError, ValueError, TypeError):
        ast = None
    if not isinstance(ast, dict):
        ast = {}
    getter = ast.get('generated_getter')
    is_getter = (isinstance(getter, dict) and getter.get('nodeType') == 'VariableDeclaration'
                 and getter.get('stateVariable') is True and getter.get('visibility') == 'public'
                 and type(getter.get('id')) is int and getter['id'] in lookup.nodes)
    anchor_declaration = getter if is_getter else ast
    anchor_kind = 'state_getter' if is_getter else 'source_function' if ast.get('nodeType') == 'FunctionDefinition' else 'unavailable'
    roots = [ast]
    # Include modifier bodies as source declarations, without inventing a
    # rejection path or changing the existing success-path extractor.
    for modifier in ast.get('modifiers', []):
        declaration = modifier.get('modifierName', {}).get('referencedDeclaration')
        node = lookup.nodes.get(declaration, {})
        if node.get('nodeType') == 'ModifierDefinition':
            roots.append(node)
    nodes = {n['id']: n for root in roots for n in _walk(root)
             if type(n.get('id')) is int}
    state_references = ([{'ast_id': getter['id'], 'name': getter.get('name'),
                          'source': getter.get('src')}] if is_getter else [])
    for node in list(nodes.values()):
        declaration = node.get('referencedDeclaration')
        referenced = lookup.nodes.get(declaration, {})
        if referenced.get('stateVariable') is True:
            state_references.append({'ast_id': declaration,
                                     'name': referenced.get('name'),
                                     'source': referenced.get('src')})
    for ref in state_references:
        nodes[ref['ast_id']] = lookup.nodes[ref['ast_id']]
    rejection_sites, call_sites = [], []
    for node in nodes.values():
        kind = node.get('nodeType')
        if kind == 'RevertStatement':
            rejection_sites.append({'ast_id': node['id'], 'kind': kind,
                                    'source': node.get('src')})
        if kind == 'FunctionCall':
            expression = node.get('expression', {})
            site = {'ast_id': node['id'], 'source': node.get('src'),
                    'callee_ast_id': expression.get('referencedDeclaration'),
                    'callee_name': expression.get('name', expression.get('memberName'))}
            call_sites.append(site)
            # A bare identifier alone is insufficient: require/assert/revert
            # must be compiler-identified builtins, not a same-named method.
            declaration = expression.get('referencedDeclaration')
            from .source_entry_identity import builtin_call
            if builtin_call(node,lookup,('require','assert','revert')):
                rejection_sites.append({**site, 'kind': expression['name']})
    return {'target': target, 'function': function,
            'anchor_kind': anchor_kind,
            'function_ast_id': ast.get('id') if anchor_kind == 'source_function' else None,
            'declaration_ast_id': anchor_declaration.get('id'), 'source': anchor_declaration.get('src'),
            'source_ast_ids': sorted(nodes),
            'rejection_sites': rejection_sites, 'call_sites': call_sites,
            'state_references': sorted({r['ast_id']: r for r in state_references}.values(),
                                       key=lambda x: x['ast_id']),
            'rejection_semantics': 'source_sites_only; rejection_path_model_not_constructed',
            'instance_semantics': 'source_declaration_only; deployment_or_alias_not_proved'}


def enrich(context, state):
    """Return an independent context copy with source sites for new questions."""
    result = copy.deepcopy(context)
    anchors = []
    for target in context['targets']:
        lookup = state['lookups'][target['id']]
        for function in target['functions']:
            anchors.append(_function_anchor(target['id'], function['function'], lookup))
    result['source_function_anchors'] = anchors
    from .task_scope import requested
    active=requested(context)
    from .m05_question_plan import catalog
    result['question_model_catalog']=catalog()
    result['question_model_catalog']['rules']={k:v for k,v in result['question_model_catalog']['rules'].items() if k in active}
    result['source_obligation_interface'] = {
        'schema': SCHEMA, 'rules': list(active),
        'mechanism_fields': sorted(MECHANISM_FIELDS),
        'source_write_required': False,
        'formal_model_status': 'carrier_is_not_a_verdict; downstream_translation_is_model_specific; unsupported_models_remain_explicit',
        'normal_review_is_safety_verdict': False,
        'source_binding_is_semantic_proof': False}
    return result


def _ids(value, allowed, name, nonempty=False):
    _require(isinstance(value, list) and (bool(value) or not nonempty)
             and all(type(x) is int and x in allowed for x in value),
             'OBLIGATION_SOURCE_AST_NOT_BOUND:' + name)


def _text(value, name):
    _require(isinstance(value, str) and bool(value.strip()), 'OBLIGATION_TEXT:' + name)


def _mechanism_references(value, allowed, state):
    """Validate explicit source references; prose is retained as a hypothesis."""
    for node in _walk(value):
        for field, content in node.items():
            if field.endswith('_ast_ids'):
                _ids(content, allowed, field)
            elif field.endswith('_ast_id'):
                _require(type(content) is int and content in allowed,
                         'OBLIGATION_SOURCE_AST_NOT_BOUND:' + field)
            elif field in ('expression_ref', 'ref'):
                _require(isinstance(content, str) and content in state.get('terms', {}),
                         'OBLIGATION_EXPRESSION_REF_NOT_FOUND')


def bind_obligations(response, context, state):
    """Bind source declarations, preserving unsupported formal obligations.

    Returns a separate report channel. No returned record is an M04 query and
    no response verdict is consumed. A bad proposal cannot discard good ones.
    """
    progress = {rule: empty_rule_progress() for rule in RULES}
    output = {'schema': SCHEMA, 'source_obligations': [],
              'source_obligation_errors': [], 'rule_stage_progress': progress,
              'scope': 'this source-obligation channel only; other rule checks cannot complete it',
              'formal_checks_called': 0, 'reportable_findings': 0}
    try:
        _require(isinstance(response, dict), 'OBLIGATION_RESPONSE_OBJECT')
        _require(response.get('identity') == context['identity'], 'OBLIGATION_RESPONSE_IDENTITY')
        proposals = response.get('source_obligations', [])
        _require(isinstance(proposals, list), 'OBLIGATION_LIST_REQUIRED')
    except ValueError as error:
        output['source_obligation_errors'].append({'proposal_index': None, 'reason': str(error)})
        return output
    # Recompute anchors from the actual lookup rather than trusting model or
    # mutable context-provided source_function_anchors.
    anchors = {(a['target'], a['function']): a
               for a in enrich(context, state)['source_function_anchors']}
    from .m05_source_graph import SourceGraph
    graphs = {target: SourceGraph(lookup) for target, lookup in state['lookups'].items()}
    seen = set()
    for index, proposal in enumerate(proposals):
        rule = proposal.get('rule') if isinstance(proposal, dict) else None
        if isinstance(rule, str) and rule in progress:
            progress[rule]['received'] += 1
        try:
            _require(isinstance(proposal, dict), 'OBLIGATION_OBJECT')
            ident = proposal.get('id')
            _text(ident, 'id')
            _require(ident not in seen, 'OBLIGATION_DUPLICATE_ID')
            seen.add(ident)
            _require(isinstance(rule, str) and rule in RULES, 'OBLIGATION_RULE_UNKNOWN')
            from .task_scope import requested
            _require(rule in requested(context),'OBLIGATION_RULE_OUTSIDE_TASK')
            if 'identity' in proposal:
                _require(proposal['identity'] == context['identity'], 'OBLIGATION_PROPOSAL_IDENTITY')
            for field in ('program_id', 'build_id'):
                if field in proposal:
                    _require(proposal[field] == context['identity'][field],
                             'OBLIGATION_PROPOSAL_IDENTITY:' + field)
            pair = (proposal.get('target'), proposal.get('function'))
            _require(pair in anchors, 'OBLIGATION_TARGET_FUNCTION_NOT_FOUND')
            anchor = anchors[pair]
            allowed = set(anchor['source_ast_ids'])
            related_ids, graph_binding = graphs[pair[0]].scope(pair[1])
            allowed |= related_ids
            # A proposal can cite its explicitly named related operations.
            # Resolve each against compiler declarations BEFORE checking the
            # proposal-wide anchor list. This grants location, never caller,
            # instance or state-key equivalence to semantic consumers.
            declared_mechanism = proposal.get('mechanism', {})
            declared_related = declared_mechanism.get('related_operations', []) if isinstance(declared_mechanism, dict) else []
            declared_scopes = []
            for operation in declared_related if isinstance(declared_related, list) else []:
                if not isinstance(operation, dict): continue
                rp = (operation.get('target'), operation.get('function'))
                _require(rp in anchors, 'OBLIGATION_RELATED_OPERATION_NOT_FOUND')
                ri, proof = graphs[rp[0]].scope(rp[1])
                allowed |= ri | set(anchors[rp]['source_ast_ids'])
                declared_scopes.append({'target':rp[0], 'function':rp[1], 'graph':proof})
            graph_binding = {**graph_binding, 'explicit_related_locations':declared_scopes,
                             'semantic_equivalence_granted':False}
            _ids(proposal.get('source_ast_ids'), allowed, 'source_ast_ids', nonempty=True)
            mechanism = proposal.get('mechanism')
            _require(isinstance(mechanism, dict)
                     and set(mechanism) <= MECHANISM_FIELDS | {'description'}, 'OBLIGATION_MECHANISM_SHAPE')
            from .m05_relation_binding import build_relation_binding
            relation_binding=build_relation_binding(proposal,context,state,allowed)
            related = mechanism.get('related_operations', [])
            _require(isinstance(related, list), 'OBLIGATION_RELATED_OPERATIONS_LIST')
            related_bindings = []
            for operation in related:
                _require(isinstance(operation, dict), 'OBLIGATION_RELATED_OPERATION_OBJECT')
                related_pair = (operation.get('target'), operation.get('function'))
                _require(related_pair in anchors, 'OBLIGATION_RELATED_OPERATION_NOT_FOUND')
                related_anchor = anchors[related_pair]
                related_ids, related_graph = graphs[related_pair[0]].scope(related_pair[1])
                _mechanism_references(operation, set(related_anchor['source_ast_ids']) | related_ids, state)
                related_bindings.append({'target': related_pair[0], 'function': related_pair[1],
                    'function_ast_id': related_anchor['function_ast_id'],
                    'anchor_kind': related_anchor['anchor_kind'],
                    'declaration_ast_id': related_anchor['declaration_ast_id'],
                    'status': 'source_declaration_bound',
                    'instance_status': 'unresolved_not_proved_by_declaration',
                    'relation_status': 'hypothesis_not_semantically_checked'})
            optional_reference_notes=[]
            for reference in ('candidate_id', 'write_id'):
                value = proposal.get(reference)
                if value is None:
                    continue
                binding = state.get('bindings', {}).get(value)
                if not isinstance(binding,dict):
                    optional_reference_notes.append({'field':reference,'value':value,
                        'status':'not_bound_not_used; exact source anchors remain independently required'})
                    continue
                function = binding.get('function', binding.get('row', {}).get('function'))
                _require((binding.get('target'), function) == pair,
                         'OBLIGATION_REFERENCE_TARGET_MISMATCH')
                _require(('row' if reference == 'candidate_id' else 'write') in binding,
                         'OBLIGATION_REFERENCE_KIND_MISMATCH')
            basis = proposal.get('basis')
            _require(basis is None or isinstance(basis, dict) and basis.get('kind') in
                     ('program_relation', 'normal_description', 'combined'), 'OBLIGATION_BASIS')
            if basis is not None:_text(basis.get('explanation'), 'basis.explanation')
            declared_basis=basis.get('kind') if basis else 'unspecified'
            basis_assessment = {
                'declared_kind': declared_basis,
                'normal_description_available': bool(context.get('normal_project_description')),
                'description_used_as_premise': False,
                'source_relations_require_independent_semantic_check': True,
                'unsupported_description_claim': declared_basis in ('normal_description', 'combined')
                    and not bool(context.get('normal_project_description')),
                'scope': 'source-derived conditional mechanism; unprovided description is never invented or assumed'}
            if basis and 'source_ast_ids' in basis:
                _ids(basis['source_ast_ids'], allowed, 'basis.source_ast_ids')
            _text(proposal.get('rationale'), 'rationale')
            alternatives = proposal.get('alternatives')
            _require(isinstance(alternatives, list) and all(isinstance(x, str) for x in alternatives),
                     'OBLIGATION_ALTERNATIVES')
            unresolved = proposal.get('unresolved')
            _require(isinstance(unresolved, list) and all(isinstance(x, dict)
                     and isinstance(x.get('text'), str) and x['text'].strip()
                     and x.get('impact') in ('query_blocking', 'policy_scope', 'unrelated')
                     for x in unresolved), 'OBLIGATION_UNRESOLVED')
            raw_review_kind = proposal.get('review_kind', 'risk_hypothesis')
            _require(raw_review_kind in ('risk_hypothesis', 'normal_review', 'uncertain',
                                        'normal_control', 'unresolved', 'not_applicable'),
                     'OBLIGATION_REVIEW_KIND')
            review_kind = {'normal_control': 'normal_review', 'unresolved': 'uncertain'}.get(
                raw_review_kind, raw_review_kind)
            record = {'id': ident, 'rule': rule, 'target': pair[0], 'function': pair[1],
                'identity': copy.deepcopy(context['identity']),
                'source_ast_ids': copy.deepcopy(proposal['source_ast_ids']),
                'source_binding_status': 'source_anchors_bound',
                'source_reference_graph': graph_binding, 'relation_binding':relation_binding,
                'semantic_binding_status': 'not_checked',
                'review_kind': review_kind, 'original_proposal': copy.deepcopy(proposal),
                'proposal_sha256': _digest(proposal), 'related_operations': related_bindings,
                'basis_assessment': basis_assessment,
                'optional_reference_notes':optional_reference_notes,
                'status': 'inconclusive', 'reportable': False, 'execution_status': 'not_run',
                'formal': {'solver_called': False, 'query': 'not_encoded', 'premise': 'not_checked',
                    'status': 'inconclusive',
                    'reason': 'source_question_bound_awaiting_model_planning'},
                'not_a_safety_conclusion': True}
            output['source_obligations'].append(record)
            progress[rule]['source_bound'] += 1
            progress[rule]['not_encoded'] += 1
            progress[rule]['normal_reviews'] += review_kind == 'normal_review'
        except (ValueError, TypeError, KeyError) as error:
            if isinstance(rule, str) and rule in progress:
                progress[rule]['binding_errors'] += 1
            output['source_obligation_errors'].append({'proposal_index': index,
                'proposal_id': proposal.get('id') if isinstance(proposal, dict) else None,
                'rule': rule, 'reason': str(error), 'original_proposal': copy.deepcopy(proposal)})
    return output
