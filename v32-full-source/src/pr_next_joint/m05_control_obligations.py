"""M2-triggered privileged transfer blocking, scoped to source paths/holders."""
import copy
import networkx as nx
from .core import digest
from .m03_p_paths import key, walk, op, lit
from .m03_p_route import keys, fields, selectors, value_type, effective_permission
from .m03_p_assets import asset_models, deltas, negative, term, holder_path
from .m04_asset_math import proportional_models
from .m04_logic import Unsupported
from .m05_state_relations import control_type,changes,control_contribution,consumed_control_with_asset
from .m05_mechanism_core import program, successful, remap, post, relevant, solve, scalar_write, checked_subtractions, retime
from .m05_mechanism_core import execution_terms
from .m05_control_baseline import transfer_summary,entry_alternatives,normal_baseline,blocking_formula as scoped_blocking_formula


def privilege(guards, lookup, excluded=()):
    out = []
    predicates=effective_permission(guards, lookup)
    # A closed owner/role OR current-contract-self guard is administrative.
    # Do not accept arbitrary caller-controlled alternatives or drop OR branches.
    from .m03_p_route import permission_atoms
    from .m03_p_paths import normalize,conditions_possible
    def self_guard(e):
        if e.get('kind')!='op' or e.get('op')!='==':return False
        return any(a.get('kind')=='actual_sender' and b.get('kind')=='contract_address'
            and b.get('instance',{}).get('kind') in ('root_instance','new_instance')
            for a,b in (e['args'],e['args'][::-1]))
    for raw in guards:
        g=normalize(raw)
        if g.get('kind')!='op' or g.get('op') not in ('or','||'):continue
        if not any(self_guard(a) for a in g['args']):continue
        if not all(self_guard(a) or (a.get('op') not in ('or','||','and','&&') and permission_atoms(a,lookup)) for a in g['args']):continue
        if not conditions_possible(guards,g):predicates.append(g)
    for predicate in predicates:
        ss = selectors(predicate)
        if not ss or any(s['root'] in excluded or s.get('instance') for s in ss):
            continue
        if any(n.get('kind') == 'parameter' for s in ss for n in walk(keys(s))):
            continue
        out.append(predicate)
    return op('or', *out) if out else lit(False)


def graph_record(setter, write, action, control, asset):
    g = nx.DiGraph()
    edges = [(setter, 'state:' + key(control), 'writes_control'),
             ('state:' + key(control), action, 'guards_action'),
             (action, 'asset:' + str(asset), 'conserved_holder_transfer')]
    for a, b, relation in edges:
        g.add_edge(a, b, relation=relation)
    data = {'engine': 'NetworkX DiGraph', 'edges': edges,
            'setter_write': write['source'], 'path': nx.shortest_path(g, setter, 'asset:' + str(asset))}
    data['sha256'] = digest(data)
    return data

def bind_key(pattern,value,mapping):
    """Unify a source key expression, retaining transforms and fixed fields."""
    if isinstance(pattern,dict) and pattern.get('kind')=='parameter':
        ident=pattern['id']
        if ident in mapping and key(mapping[ident])!=key(value):raise Unsupported('blocking_control_key_conflict')
        mapping[ident]=value;return
    if isinstance(pattern,dict) and isinstance(value,dict) and set(pattern)==set(value):
        for k in pattern:bind_key(pattern[k],value[k],mapping)
        return
    if isinstance(pattern,list) and isinstance(value,list) and len(pattern)==len(value):
        for a,b in zip(pattern,value):bind_key(a,b,mapping)
        return
    if pattern!=value:raise Unsupported('blocking_control_key_relation_not_bound')


def check(obligation, state):
    lookup, paths, extraction_errors = program(state, obligation['target'])
    models = asset_models(lookup, paths,allow_nested=True) + proportional_models(lookup, paths)
    if not models:
        return [], [{'reason': 'blocking_financial_interest_not_bound'}]
    rows, gaps = [], []
    def refute(kind,fn,details):
        certificate={'kind':kind,'verified':True,'target':obligation['target'],'function':fn,
            'identity':obligation['identity'],'source_facts':details,'not_a_safety_proof':True}
        return {'id':'soq_'+digest([obligation['proposal_sha256'],certificate]),'obligation_id':obligation['id'],
            'rule':obligation['rule'],'target':obligation['target'],'function':fn,'status':'refuted_in_scope','reportable':False,
            'program_analysis_certificate':certificate,'source_model':{'kind':kind},
            'formal':{'solver_called':False,'query':'not_required_P','premise':'source_checked','status':'refuted_in_scope','reason':kind},
            'assumptions':['supplied source and approved holder-normal-request definition']}
    for asset in models:
        for fn, actions in paths.items():
            for pi, action in enumerate(actions):
                if not successful(action) or action['issues']:
                    continue
                try:
                    transfer=transfer_summary(action,asset,lookup)
                    if transfer is None:continue
                    continuations=entry_alternatives(fn,actions,pi,transfer,asset,lookup)
                except (Unsupported,ValueError,TypeError,KeyError) as ex:
                    gaps.append({'reason':str(ex),'function':fn,'path_index':pi,'asset_root':asset['balance_root']});continue
                holder=transfer['holder'];recipient=transfer['recipient'];amount=transfer['amount']
                action_conditions=action['guards']+checked_subtractions(action)
                control_map = {key(s): s for guard in action_conditions for s in selectors(guard)
                               if s['root'] not in (asset['balance_root'], asset['supply_root'])
                               and control_type(value_type(s,lookup))}
                for control in control_map.values():
                    scoped = any(x.get('kind') == 'actual_sender' or x.get('type') in ('address', 'address payable')
                                 for x in walk(keys(control)))
                    holder_bound = any(key(n)==key(holder) for n in walk(keys(control)))
                    scope_matches = (scoped and holder_bound) if obligation['rule']=='FCR-FREEZE' else not scoped
                    for setter, transitions in paths.items():
                        # Sharing a state root does not make a different setter
                        # the operation asked about (e.g. unpause vs pause).
                        if obligation['function'] not in (fn,setter):continue
                        for ti, transition in enumerate(transitions):
                            if not successful(transition) or transition['issues']:
                                continue
                            writes = [w for w in transition['writes'] if w['path']['root'] == control['root']
                                      and fields(w['path']) == fields(control)
                                      and key(w['path'].get('instance')) == key(control.get('instance'))]
                            if not writes:
                                continue
                            if not (relevant(obligation, fn, action, (control['root'], asset['balance_root']))
                                    or relevant(obligation, setter, transition, (control['root'],))):
                                continue
                            try:
                                try:baseline=normal_baseline(action,transfer,control,asset,lookup,paths)
                                except Unsupported as error:
                                    if str(error)!='normal_holder_action_requires_independent_administrator':raise
                                    # The approved main definition excludes a purely
                                    # administrator-mediated service. Retain it as
                                    # auxiliary evidence, never a main FREEZE alarm.
                                    excluded=refute('administrator_mediated_request_outside_main_holder_blocking',fn,
                                        {'entry_source':action['entry_source'],'guards':action['guards'],'transfer':transfer,'control':control})
                                    excluded['auxiliary_finding']={'kind':'administrator_service_control','not_main_risk':True,'main_rule':obligation['rule']}
                                    rows.append(excluded);continue
                                mapping = {}
                                key_conditions=[]
                                for w in writes:
                                    a, b = keys(w['path']), keys(control)
                                    if len(a) != len(b):
                                        raise Unsupported('blocking_control_key_arity')
                                    for x, y in zip(a, b):
                                        if x.get('kind') == 'parameter':
                                            if x['id'] in mapping and key(mapping[x['id']]) != key(y):
                                                raise Unsupported('blocking_control_key_conflict')
                                            mapping[x['id']] = y
                                        elif x.get('kind') != 'actual_sender' and key(x) != key(y):
                                            if (x.get('kind')=='index' and x.get('base',{}).get('kind')=='parameter'
                                                    and '[' in x['base'].get('type','')):
                                                # Keep the source array access intact and constrain
                                                # its value; do not substitute a fabricated reference.
                                                key_conditions.append((x,y))
                                            else:bind_key(x,y,mapping)
                                caller = {'kind': 'transition_caller', 'function': setter, 'type': 'address'}
                                transition_time={'kind':'environment','field':'timestamp','invocation':'control_transition'}
                                actual = retime(remap(transition, mapping, caller),transition_time)
                                if key_conditions:
                                    actual['guards'].append(op('or',*[op('and',*[op('==',retime(remap(x,mapping,caller),transition_time),y)
                                        for x,y in zip(keys(w['path']),keys(control))]) for w in writes]))
                                transition_terms=execution_terms(actual,lookup)
                                priv = remap(privilege(transition['guards'], lookup,
                                                       (control['root'], asset['balance_root'])), mapping, caller)
                                before = op('and', *action_conditions)
                                if consumed_control_with_asset(actual['writes'],control,asset['balance_root'],lookup):
                                    raise Unsupported('consumable_control_change_needs_independent_blocking_relation')
                                contribution = control_contribution(before, actual['writes'], control, lookup)
                                after = contribution['post_action']
                                model = {'kind': 'privileged_transfer_blocking', 'rule': obligation['rule'],
                                         'asset': asset, 'action': fn, 'action_path': pi,
                                         'transition': setter, 'transition_path': ti, 'control': control,
                                         'pre_action': before, 'post_action': after, 'transition_guards': actual['guards'],
                                         'reference_post_action':contribution['reference_post_action'],
                                         'control_contribution':contribution, 'action_writes':action['writes'],
                                         'recipient':recipient,'amount':amount,
                                         'privilege': priv, 'writes': actual['writes'], 'holder': holder,
                                         'control_scope': 'debited_holder' if holder_bound else 'other_address' if scoped else 'global',
                                         'required_scope_matches': scope_matches,
                                         'transition_time':transition_time,
                                         'normal_baseline':baseline,'transfer_request':transfer,
                                         'entry_alternatives':continuations,'transition_execution_terms':transition_terms,
                                         'time_relation':'control transition precedes or coincides with attempted action',
                                         'graph': graph_record(setter, writes[0], fn, control, asset['balance_root']),
                                         'assumptions': ['declared financial interest and symbolic pre-state',
                                                         'all retained continuations of this exact request in this entry are compared; other entries may remain available',
                                                         'off-chain consent and deployment reachability not proved',
                                                         'control contribution compares the same other write expressions; contrast state is not a transaction witness']}
                                def construct(e, inputs):
                                    return scoped_blocking_formula(e, inputs, lookup)
                                if obligation['function']==setter:
                                    model['relation_operation_substitution']={'function':setter,'parameters':copy.deepcopy(mapping),'sender':caller,'time':transition_time,
                                        'basis':'same compiler-resolved setter invocation used by this control formula'}
                                rows.append(solve(lookup, obligation, fn, model, construct,
                                                  control['root'], keys(control)[0] if scoped else holder))
                            except (Unsupported, ValueError, TypeError, KeyError) as ex:
                                gaps.append({'reason': str(ex), 'function': fn, 'transition': setter})
    if not rows and not gaps:
        complete=not extraction_errors and bool(paths) and all(not p.get('issues') and not p.get('evaluation_gaps') and p.get('flow')!='truncated' for branches in paths.values() for p in branches)
        if complete:
            rows.append(refute('complete_source_has_no_matching_control_transfer_pair',obligation['function'],
                {'checked_entries':sorted(paths),'asset_roots':[m['balance_root'] for m in models],'program_paths_sha256':digest(paths)}))
        else:gaps = [{'reason': 'no_source_bound_control_transfer_pair', 'extraction_errors': extraction_errors}]
    return rows, gaps
