"""Same-issued-credential self-composition, without solving cryptography.

The model requires identical typed hash preimages and signature inputs. A SAT
witness cannot rely on a hash collision or a newly forged signature. Existence
of an issued valid credential is an explicit conditional premise.
"""
import networkx as nx
from .m03_p_paths import key, walk, op, lit
from .m03_p_route import keys, value_type
from .m04_logic import Unsupported
from .m05_mechanism_core import program, successful, remap, post, solve, relevant, scalar_write


def recoveries(value):
    return list({key(n): n for n in walk(value) if n.get('kind') == 'credential_recovery'}.values())


def payload(credential):
    from .m05_credential_encoding import layout
    return layout(credential['digest'])


def same_payload(e, left, right):
    a, b = payload(left), payload(right)
    if a['mode'] != b['mode'] or a['types'] != b['types'] or len(a['arguments']) != len(b['arguments']):
        raise Unsupported('credential_payload_layout_changed')
    def identical_input(x,y):
        if x.get('kind')=='fixed_bytes_literal' or y.get('kind')=='fixed_bytes_literal':
            from .m05_credential_encoding import fixed_literal
            if x.get('kind')!=y.get('kind'):raise Unsupported('credential_literal_layout_changed')
            return e.z.BoolVal(fixed_literal(x)==fixed_literal(y))
        if x.get('kind')=='hash' or y.get('kind')=='hash':
            if x.get('kind')!=y.get('kind'):raise Unsupported('credential_nested_payload_layout')
            aa,bb=payload({'digest':x}),payload({'digest':y})
            if aa['mode']!=bb['mode'] or aa['types']!=bb['types'] or len(aa['arguments'])!=len(bb['arguments']):raise Unsupported('credential_nested_payload_layout')
            return e.z.And(*[identical_input(xx,yy) for xx,yy in zip(aa['arguments'],bb['arguments'])])
        return e.expr(x)==e.expr(y)
    return e.z.And(*[identical_input(x,y) for x, y in zip(a['arguments'], b['arguments'])],
                   *[e.expr(x) == e.expr(y) for x, y in zip(left['signature'], right['signature'])])


def nonce_bookkeeping(effect, credential, guards):
    """Recognize a consumed signed counter through source equality, not name."""
    selector=effect['path'];value=effect['value']
    if not (value.get('kind')=='op' and value.get('op')=='+' and len(value['args'])==2
            and any(key(x)==key(selector) for x in value['args'])
            and any(x==lit(1) for x in value['args'])):return False
    signed={key(n) for n in walk(credential['digest'])}
    for n in walk(guards):
        if n.get('kind')=='op' and n.get('op')=='==' and len(n['args'])==2:
            a,b=n['args']
            if (key(a)==key(selector) and key(b) in signed) or (key(b)==key(selector) and key(a) in signed):return True
    return False


def check(obligation, state):
    lookup, paths, errors = program(state, obligation['target'])
    rows, gaps = [], []
    for fn, branches in paths.items():
        # Other uses may be compared by the dedicated domain consumer; they
        # cannot replace the primary operation just because they share storage.
        if fn!=obligation['function']:continue
        for pi, path in enumerate(branches):
            if not successful(path):
                continue
            credentials = recoveries(path['guards'])
            if not credentials or not relevant(obligation, fn, path,
                    [w['path']['root'] for w in path['writes']]):
                continue
            try:
                if path['issues']:
                    raise Unsupported('credential_path_has_unresolved_semantics')
                if len(credentials) != 1:
                    from .m05_credential_quorum import check_quorum
                    modeled=check_quorum(obligation,lookup,fn,path,pi,credentials,same_payload,nonce_bookkeeping)
                    rows.extend(modeled)
                    if not modeled:raise Unsupported('multiple_credential_sources_need_joint_model')
                    continue
                credential = credentials[0]
                from .m05_credential_validity import check_invalid_zero
                extra,missing=check_invalid_zero(obligation,lookup,fn,pi,path,credential)
                rows.extend(extra);gaps.extend(missing)
                payload(credential)
                hashes = {key(n) for n in walk(path['guards']) if n.get('kind') == 'hash'}
                if hashes != {key(n) for n in walk(credential['digest']) if n.get('kind')=='hash'}:
                    gaps.append({'reason':'credential_equivalent_signature_encoding_not_modeled',
                                 'function':fn,'path_index':pi,
                                 'dependency':'credential_signature_hash_key_separation_not_established'})
                    raise Unsupported('additional_hash_condition_not_in_same_payload_model')
                signature_ids = {n['id'] for n in walk(credential['signature']) if n.get('kind') == 'parameter'}
                body = lookup.function(fn)
                mapping = {p['id']: {'kind': 'parameter', 'id': p['id'], 'invocation': 'alternative_use',
                                    'type': p['typeDescriptions']['typeString']}
                           for p in body['parameters']['parameters'] if p['id'] not in signature_ids}
                caller2 = {'kind': 'transition_caller', 'use': 'alternative_use', 'type': 'address'}
                alternative = remap(path, mapping, caller2)
                credential2 = recoveries(alternative['guards'])[0]
                # Boolean capability changes are effects too. A consumed flag
                # is checked with its source guard, never assumed reusable.
                effects = [scalar_write(w, lookup) for w in path['writes']]
                if not effects:
                    raise Unsupported('credential_protected_effect_not_bound')
                for wi, effect in enumerate(effects):
                    # Counter bookkeeping used in the signed message is not an
                    # independent protected resource. Other state effects are.
                    if any(key(s) == key(effect['path']) for s in walk(credential['digest']) if s.get('kind') == 'storage'):
                        continue
                    if nonce_bookkeeping(effect,credential,path['guards']):continue
                    alt_effect = remap(effect, mapping, caller2)
                    graph = nx.DiGraph()
                    graph.add_edge('source_payload', 'signature_recovery', relation='typed_preimage')
                    graph.add_edge('signature_recovery', fn, relation='source_guard')
                    graph.add_edge(fn, str(effect['path']['root']), relation='protected_write')
                    base = {'function': fn, 'path_index': pi, 'write_index': wi,
                            'credential': credential, 'effect': effect,
                            'source_calls': path.get('source_calls', []),
                            'graph': {'engine': 'NetworkX DiGraph', 'edges': list(graph.edges(data=True))},
                            'same_payload_certificate': True,
                            'checked_dimensions': ['same_payload_protected_effect_binding', 'same_payload_reuse_with_arbitrary_relayer'],
                            'unchecked_dimensions': ['credential_expiry_intent', 'cross_chain_and_contract_domain', 'cryptographic_validity'],
                            'policy_scope': 'inferred_scope_of_valid_source_credential',
                            'assumptions': ['an issued valid nonzero credential exists for the first use',
                                            'identical typed payload and signature; no hash collision or signature forgery',
                                            'declared effect is hypothesized to be credential-scoped; business intent is not proved',
                                            'bounded source pre-state; no all-history/deployment proof']}
                    # Validity questions are independent of binding/replay
                    # translation and must not disappear if a later model fails.
                    from .m05_credential_validity import check_declared_validity
                    extra,missing=check_declared_validity(obligation,lookup,paths,fn,pi,path,
                        credential,effect,base,same_payload)
                    rows.extend(extra);gaps.extend(missing)
                    model = {**base, 'kind': 'credential_alternative_use_binding',
                             'checked_dimensions':['same_payload_protected_effect_binding'],
                             'alternative_effect': alt_effect, 'conditions': path['guards'],
                             'alternative_conditions': alternative['guards'], 'alternative_credential': credential2}
                    def binding_formula(e, inputs):
                        path = {'guards': inputs['conditions']}
                        alternative = {'guards': inputs['alternative_conditions']}
                        credential = inputs['credential']; credential2 = inputs['alternative_credential']
                        effect = inputs['effect']; alt_effect = inputs['alternative_effect']
                        z = e.z
                        first = z.And(*[e.expr(g) for g in path['guards']])
                        second = z.And(*[e.expr(g) for g in alternative['guards']])
                        equal = same_payload(e, credential, credential2)
                        first_value, second_value = e.expr(effect['value']), e.expr(alt_effect['value'])
                        different = z.Or(*[e.expr(x) != e.expr(y) for x, y in zip(keys(effect['path']), keys(alt_effect['path']))],
                                         first_value != second_value)
                        changed = first_value != e.expr(effect['path'])
                        return z.And(first, equal, e.expr(credential) != 0, changed), z.And(second, different)
                    rows.append(solve(lookup, obligation, fn, model, binding_formula, effect['path']['root'],
                                      keys(effect['path'])[0] if keys(effect['path']) else None))
                    # Replay keeps the exact signed arguments/signature but
                    # permits another relayer. First-use storage writes still
                    # affect the same keys only; no reset of nonce state.
                    relayed=remap(path,sender=caller2)
                    relayed_credential=remap(credential,sender=caller2)
                    relayed_effect=remap(effect,sender=caller2)
                    after_guards = post(relayed['guards'], path['writes'], lookup)
                    after_credential = post(relayed_credential, path['writes'], lookup)
                    after_effect = post(relayed_effect['value'], path['writes'], lookup)
                    replay = {**base, 'kind': 'credential_same_payload_replay', 'conditions': path['guards'],
                              'checked_dimensions':['same_payload_reuse_with_arbitrary_relayer'],
                              'post_conditions': after_guards, 'post_effect': after_effect,
                              'state_transition': path['writes'], 'second_sender':caller2,
                              'post_credential': after_credential,
                              'replay_before': post(relayed_effect['path'],path['writes'],lookup)}
                    def replay_formula(e, inputs):
                        path = {'guards': inputs['conditions']}
                        after_guards = inputs['post_conditions']; after_effect = inputs['post_effect']
                        credential = inputs['credential']; after_credential = inputs['post_credential']
                        effect = inputs['effect']
                        z = e.z
                        first = z.And(*[e.expr(g) for g in path['guards']])
                        second = z.And(*[e.expr(g) for g in after_guards])
                        equal = same_payload(e, credential, after_credential)
                        initial, middle, final = e.expr(effect['path']), e.expr(effect['value']), e.expr(after_effect)
                        replay_before=e.expr(inputs['replay_before'])
                        return z.And(first, e.expr(credential) != 0, middle != initial), z.And(equal, second, final != replay_before)
                    rows.append(solve(lookup, obligation, fn, replay, replay_formula, effect['path']['root'],
                                      keys(effect['path'])[0] if keys(effect['path']) else None))
                    from .m05_credential_temporal import check_temporal
                    rows.extend(check_temporal(obligation,lookup,fn,path,credential,effect,
                        alternative,alt_effect,credential2,base,same_payload))
                    from .m05_credential_domains import check_domains
                    rows.extend(check_domains(obligation,lookup,paths,fn,path,pi,credential,effect,base,same_payload,recoveries))
            except (Unsupported, ValueError) as ex:
                gaps.append({'reason': str(ex), 'function': fn, 'path_index': pi})
    if not rows and not gaps:
        gaps = [{'reason': 'credential_guard_and_protected_effect_not_bound', 'extraction_errors': errors}]
    if rows:
        gaps.append({'reason': 'credential_validity_and_domain_scope_not_checked',
                     'modeled_dimensions': sorted({dimension for row in rows for dimension in row.get('source_model',{}).get('checked_dimensions',[])}),
                     'not_checked': ['business_expiry_intent','cross_chain_domain','cryptographic_validity','arbitrary_validity_protocol'],
                     'impact': 'local results do not complete the entire AC-05 proposal'})
    return rows, gaps
