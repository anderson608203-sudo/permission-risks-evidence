"""Changing a shared latch which controls establishment of an effective authority."""
from .m03_p_paths import key, lit, op, normalize
from .m03_p_route import value_type, effective_permission
from .m04_logic import Unsupported
from .m11_policy import make_query
from .m20_policy import role_evidence
from .m21_admission import atoms
from .m05_mechanism_core import remap


def clean(path):
    return path['flow'] in ('normal','returned') and not (path['issues'] or path.get('evaluation_gaps'))


def closes_role_entry(paths, role, open_guard):
    """A modifier may still assign the role after the guarded body is skipped."""
    for branch in paths:
        if branch['flow'] in ('revert','reverted'):continue
        if not clean(branch):return False
        if any(key(w['path'])==key(role) for w in branch['writes']):
            if key(open_guard) not in {key(normalize(g)) for g in atoms(branch['guards'])}:
                return False
    return True


def duties(context, state, index):
    queries, limits = [], []
    for tid, lookup in state['lookups'].items():
        program = {fn:paths for (target,fn),paths in state['paths'].items() if target == tid}
        guarded_roles = {}
        roles = {}
        for fn, paths in program.items():
            for pi, path in enumerate(paths):
                if not clean(path):
                    continue
                for condition in atoms(path['guards']):
                    guard = normalize(condition)
                    positive = guard.get('op') != '!'
                    flag = guard if positive else guard['args'][0]
                    if flag.get('kind') != 'storage' or flag.get('segments') or value_type(flag,lookup) != 'bool':
                        continue
                    for write in path['writes']:
                        role = write['path']
                        if role.get('segments') or value_type(role,lookup) not in ('address','address payable'):
                            continue
                        if write['value'].get('kind') not in ('actual_sender','parameter'):
                            continue
                        if key(role) not in roles:
                            roles[key(role)] = role_evidence(lookup,program,role)
                        uses = [u for u in roles[key(role)] if u['function'] != fn and clean(program[u['function']][u['path_index']])
                                and (program[u['function']][u['path_index']]['writes'] or program[u['function']][u['path_index']].get('sensitive_effects'))]
                        if uses and closes_role_entry(paths,role,guard):
                            guarded_roles.setdefault(key(flag),[]).append((fn,pi,role,positive,uses))
        for record in index.by_target[tid]:
            effect = record['effect']
            write = effect.get('original_write')
            if not write or key(write['path']) not in guarded_roles:
                continue
            fn, pi = record['function'], record['path_index']
            setter = program[fn][pi]
            if not clean(setter) or len(setter['writes']) != 1 or setter.get('sensitive_effects'):
                continue
            for entry, branch, role, open_value, uses in guarded_roles[key(write['path'])]:
                if entry == fn or write['value'] != lit(not open_value):
                    continue
                # A phase setter guarded by a public completion condition needs its
                # own policy. Do not turn a time/settlement condition into owner-only.
                permissions = effective_permission(setter['guards'],lookup)
                stage_guard=write['path'] if open_value else op('!',write['path'])
                permitted_guards={key(normalize(g)) for g in atoms(permissions)}|{key(normalize(stage_guard))}
                if any(key(normalize(g)) not in permitted_guards for g in atoms(setter['guards'])):
                    continue
                try:
                    peer = program[entry][branch]
                    caller = {'kind':'transition_caller','function':entry,'type':'address'}
                    from .m03_p_paths import walk
                    params = {v['id']:{**v,'id':-1900000000-abs(v['id'])} for v in walk(peer) if v.get('kind')=='parameter'}
                    model = dict(setter)
                    model['guards'] = [*setter['guards'], *remap(peer['guards'],params,caller), op('!=',caller,lit(0)), op('!=',role,lit(0))]
                    model['evaluated_terms'] = [*setter.get('evaluated_terms',[]),*remap(peer.get('evaluated_terms',[]),params,caller)]
                    required = op('or',op('==',{'kind':'actual_sender'},role),*permissions)
                    basis = {'basis':'shared_authority_phase_closed_by_non_manager','authority':role,
                             'guarded_authority_entry':entry,'guarded_path_index':branch,'authority_uses':uses,
                             'open_value':open_value,'phase_selector':write['path'],
                             'scope':'externally reachable disabling of the shared stage for establishing a live administrative role'}
                    query = make_query(context,tid,fn,pi,model,write,required,basis,'AC-02')
                    queries.append(query)
                    index.use(record,'shared_authority_phase',query['id'])
                except (Unsupported,ValueError) as error:
                    limits.append({'phase':'management_stage','function':fn,'reason':str(error)})
    return queries,limits
