"""Source-relation permission hypotheses, not business-policy or risk proofs.

Consumes the existing M1 source_structure. No compiler, model, solver or RPC.
Candidates retain their provenance and still require M3 applicability checks
and M4 original execution. Shared writes are a retrieval relation, not a proof
that two operations must have identical permissions.
"""
import copy
import hashlib
import json


def stable(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def fingerprint(value):
    return hashlib.sha256(stable(value).encode()).hexdigest()


def resolve_effect(context, reference):
    if not isinstance(reference, str) or not reference:
        raise ValueError('effect_reference_missing')
    names = reference.split('.')
    if len(names) > 2 or len(names) == 2 and names[0] != context['contract']['name']:
        raise ValueError('effect_qualifier_not_bound')
    # Inherited qualified names require additional owning-declaration evidence.
    hits = [d for d in context['source_structure']['declarations'] if d['name'] == names[-1]]
    if len(hits) != 1:
        raise ValueError('effect_declaration_not_unique')
    return copy.deepcopy(hits[0])


def term(value):
    """Keep semantic identities; ignore spelling and source-display decoration."""
    kind = value.get('kind')
    if kind in ('subject', 'frame_caller'):
        return {'kind': 'actual_sender'}
    if kind == 'parameter':
        return {'kind': 'parameter', 'id': value['declaration']['ast_id'],
                'type': value.get('compiler_type', value['declaration'].get('type'))}
    if kind == 'literal':
        return {'kind': 'literal', 'value': value['value']}
    if kind == 'storage_binding':
        segments = []
        for segment in value['segments']:
            if 'key' in segment:
                segments.append({'key': term(segment['key']), 'type': segment.get('compiler_key_type')})
            elif 'field' in segment:
                segments.append({'field_id': segment['field']['ast_id'], 'type': segment['field'].get('type')})
            else:
                raise ValueError('unresolved_storage_segment')
        value_type = value['declaration'].get('type')
        if segments and 'field_id' in segments[-1]:
            value_type = segments[-1]['type']
        elif segments:
            # Require the original compiler type to state the terminal value.
            import re
            match = re.search(r'=>\s*(bool|address(?: payable)?)\s*\)+\s*$', value_type or '')
            value_type = match.group(1) if match else None
        return {'kind': 'state_selector', 'program_id': value['program_id'],
                'build_id': value['build_id'], 'instance_id': value['instance_id'],
                'declaration_id': value['declaration']['ast_id'], 'segments': segments,
                'value_type': value_type}
    if kind == 'op':
        return {'kind': 'op', 'op': value['op'], 'args': [term(v) for v in value['args']]}
    raise ValueError('unresolved_term:' + str(kind))


def contains(value, kind):
    if isinstance(value, dict):
        return value.get('kind') == kind or any(contains(v, kind) for v in value.values())
    return isinstance(value, list) and any(contains(v, kind) for v in value)


def permission_part(condition):
    """Extract known authorization clauses without narrowing alternative paths."""
    node = term(condition)

    def select(expr):
        if expr.get('kind') == 'state_selector':
            return expr if expr['value_type'] == 'bool' and contains(expr['segments'], 'actual_sender') else None
        if expr.get('kind') != 'op':
            return None
        op, args = expr['op'], expr['args']
        if op == '==' and len(args) == 2:
            sender = [x for x in args if x.get('kind') == 'actual_sender']
            state = [x for x in args if x.get('kind') == 'state_selector' and x['value_type'] in ('address', 'address payable')]
            if len(sender) == len(state) == 1:
                return {'kind': 'op', 'op': '==', 'args': [sender[0], state[0]]}
            for left, right in (args, list(reversed(args))):
                if right.get('kind') == 'literal' and right.get('value') is True:
                    return select(left)
        if op in ('&&', 'and', '||', 'or'):
            selected = [select(x) for x in args]
            if op in ('||', 'or') and any(x is None for x in selected):
                raise ValueError('alternative_authorization_branch_unresolved')
            selected = [x for x in selected if x is not None]
            if not selected:
                return None
            return selected[0] if len(selected) == 1 else {'kind':'op', 'op':'or' if op in ('||','or') else 'and','args':selected}
        return None

    return select(node)


def root(selector):
    return tuple(selector[k] for k in ('program_id','build_id','instance_id','declaration_id'))


def object_keys(selector):
    return [s['key'] for s in selector['segments'] if 'key' in s]


def substitution(source, target):
    if root(source) != root(target):
        raise ValueError('different_resource_identity')
    old, new = object_keys(source), object_keys(target)
    if len(old) != len(new):
        raise ValueError('different_resource_key_shape')
    result = {}
    for a,b in zip(old,new):
        if a.get('kind') == 'parameter':
            if a.get('type') != b.get('type'):
                raise ValueError('resource_key_type_mismatch')
            if a['id'] in result and result[a['id']] != b:
                raise ValueError('conflicting_resource_key_binding')
            result[a['id']] = b
        elif a != b:
            raise ValueError('resource_key_not_unified')
    return result


def relocate(value, mapping):
    if isinstance(value, dict):
        if value.get('kind') == 'parameter':
            if value['id'] not in mapping:
                raise ValueError('permission_parameter_not_bound_to_resource')
            return copy.deepcopy(mapping[value['id']])
        return {k:relocate(v,mapping) for k,v in value.items()}
    return [relocate(v,mapping) for v in value] if isinstance(value,list) else value


def classify(condition):
    selectors=[]
    def walk(v):
        if isinstance(v,dict):
            if v.get('kind')=='state_selector':selectors.append(v)
            for child in v.values():walk(child)
        elif isinstance(v,list):
            for child in v:walk(child)
    walk(condition)
    forms=set()
    for s in selectors:
        forms.add('role_membership' if s['value_type']=='bool' else 'per_object_owner' if object_keys(s) else 'global_address')
    return sorted(forms)


def discover(context, proposal, project_description=None):
    """Propose, never certify, permissions from actual source relations.

    Produces the same typed selector vocabulary for global, object and role
    relations. The caller must not turn candidate availability into a finding.
    """
    effect=proposal.get('effect',{})
    declaration=resolve_effect(context,effect.get('object'))
    requested=effect.get('field')
    if requested is not None and not any(requested in (f['name'],f['ast_id']) for f in declaration['fields']):
        raise ValueError('effect_field_not_bound')
    entries=context['source_structure']['entries']
    target=[e for e in entries if e.get('entry',{}).get('function')==proposal['function']]
    if len(target)!=1:raise ValueError('target_entry_not_unique')
    target=target[0]
    def writes(entry):
        return [r for r in entry.get('relationships',[]) if r.get('operation')=='write'
                and r.get('path',{}).get('declaration',{}).get('ast_id')==declaration['ast_id']]
    target_writes=writes(target)
    if not target_writes:raise ValueError('target_effect_not_written')
    # Validate each path against the actual context before considering joins.
    for e in entries:
        for r in writes(e):
            p=r['path']
            if p['program_id']!=context['program_id'] or p['build_id']!=context['build_id']:
                raise ValueError('resource_build_identity_mismatch')
    targets=[term(r['path']) for r in target_writes]
    candidates={}; unresolved=[]
    for peer in entries:
        peer_name=peer.get('entry',{}).get('function')
        peer_writes=writes(peer)
        if not peer_writes:continue
        parts=[]; guard_problem=False
        for g in peer.get('guards',[]):
            try:
                p=permission_part(g['condition'])
                if p is not None:parts.append(p)
            except (ValueError,KeyError) as exc:
                guard_problem=True
                unresolved.append({'function':peer_name,'reason':str(exc),'guard':copy.deepcopy(g)})
        if guard_problem or not parts:continue
        condition=parts[0] if len(parts)==1 else {'kind':'op','op':'and','args':parts}
        for write in peer_writes:
            for target_path in targets:
                try:
                    source_path=term(write['path'])
                    mapping=substitution(source_path,target_path)
                    bound=relocate(condition,mapping)
                    def check_ids(value):
                        if isinstance(value,dict):
                            if value.get('kind')=='state_selector' and (value['program_id']!=context['program_id'] or value['build_id']!=context['build_id']):
                                raise ValueError('permission_build_identity_mismatch')
                            for child in value.values():check_ids(child)
                        elif isinstance(value,list):
                            for child in value:check_ids(child)
                    check_ids(bound)
                except (ValueError,KeyError) as exc:
                    unresolved.append({'function':peer_name,'reason':str(exc)})
                    continue
                record={'function':proposal['function'],'subject':proposal['subject'],
                    'effect':copy.deepcopy(effect),'required_policy_candidate':bound,
                    'structures':classify(bound),'policy_scope':'inferred_policy',
                    'status':'hypothesis_for_analysis','reportable':False,
                    'basis':{'kind':'program_inferred','origin_entry':peer_name,
                      'relation':'observed_target_guard' if peer is target else 'same_resource_guarded_operation',
                      'source_guards':copy.deepcopy(peer.get('guards',[])),
                      'peer_write':copy.deepcopy(write),'target_paths':copy.deepcopy(targets),
                      'parameter_binding':copy.deepcopy(mapping)},
                    'remaining_checks':['policy applicability and ordinary public/self/delegated behavior',
                      'reachable initialization and permitted actor steps','M4 original execution and query-specific obligations'],
                    'limitations':['shared state and a guarded peer suggest a policy; they do not prove exclusive business authority'],
                    'raw_observed_authorization':copy.deepcopy(proposal.get('authorization'))}
                key=fingerprint({'condition':bound,'origin':peer_name,'effect':effect})
                candidates[key]=dict(record,id=key)
    return {'schema':'m03-source-permission-hypotheses-v1',
        'source_identity':{k:context[k] for k in ('program_id','build_id')},
        'original_proposal_sha256':fingerprint(proposal),
        'normal_project_description':project_description,
        'description_semantically_interpreted_by_this_component':False,
        'description_use':'retain for M2 applicability; do not ignore conflicts or call it a formal specification',
        'candidates':list(candidates.values()),'unresolved':unresolved,
        'status':'candidates_proposed' if candidates else 'no_candidate_from_supported_source_relations',
        'not_a_risk_result':True}
