"""Committed source paths for the existing caller-selected code-boundary check."""
from .m03_p_paths import key, op, walk
from .m20_sequence import qualify, read


def committed_invocation(path, effect):
    if path['flow'] not in ('normal', 'returned') or path.get('evaluation_gaps'):
        return None
    delegates = [e for e in path.get('sensitive_effects', []) if e['kind'] == 'dangerous_external_call']
    if not 1 <= len(delegates) <= 2 or effect not in delegates:
        return None
    if len(delegates) == 2:
        # One constructible implementation which returns success without
        # changing storage works at both sites, including repeated calldata.
        # This witness does not summarize arbitrary code at a second address.
        if (len({key(d['source']) for d in delegates}) != 2 or
            any(key(d['recipient']) != key(effect['recipient']) or 'success' not in d for d in delegates)):
            return None
    # The controllable target may be a successful no-op. Opaque behavior at
    # any OTHER call site or an unmodelled source expression stays a blocker.
    if any(i.get('reason') != 'dangerous_external_effect_not_resolved'
           or not any(i.get('source') == d['source'] for d in delegates) for i in path['issues']):
        return None
    guards = path['guards'] + effect.get('call_path_conditions', [])
    guards = guards + [d['success'] for d in delegates if 'success' in d]
    return guards, path.get('evaluated_terms', [])


def storage_uses(program):
    uses = {}
    for fn, paths in program.items():
        for pi, path in enumerate(paths):
            for effect in path.get('sensitive_effects', []):
                loc = effect.get('recipient', {})
                if effect['kind'] != 'dangerous_external_call' or loc.get('kind') != 'storage':
                    continue
                complete = committed_invocation(path, effect)
                if complete is not None:
                    uses.setdefault(loc['root'], []).append((fn, pi, effect, *complete))
    return uses


def bind_use(lookup, path, write, use):
    fn, pi, effect, guards, terms = use
    # The first release supports scalar addresses. An indexed cell needs a
    # separate proof that setter and consumer select the same account.
    loc = effect['recipient']
    if loc.get('segments') or key(loc) != key(write['path']):
        return None
    after = path['writes']
    def post(term):
        return read(qualify(term, 1), after, lookup)
    if key(post(loc)) != key(write['value']):
        return None
    from .m18_code_control import authority
    restrictions = authority(guards, loc, lookup, include_caller=False)
    ordered = []
    for field in ('timestamp', 'number'):
        term = {'kind':'environment', 'field':field}
        if any(v.get('kind') == 'environment' and v.get('field') == field
               for v in walk([guards, terms, path['guards'], path.get('evaluated_terms', [])])):
            ordered.append(op('>=', qualify(term, 1), term))
    def witness(term):
        if isinstance(term,list):return [witness(v) for v in term]
        if not isinstance(term,dict):return term
        # In this existential witness the chosen implementation has runtime
        # code. No assumption about code at an unrelated address is permitted.
        if term.get('kind')=='address_has_runtime_code' and key(term['address'])==key(write['value']):
            return {'kind':'literal','value':True}
        return {k:witness(v) for k,v in term.items()}
    return ([witness(post(x)) for x in guards] + ordered, [witness(post(x)) for x in terms], post(restrictions),
            {'function':fn, 'path_index':pi, 'source':effect['source'],
             'basis':'committed_use_after_setter_writes', 'callee_witness':'successful_noop',
             'scope':'separate caller and arguments, conditional on a feasible consumer call'})
