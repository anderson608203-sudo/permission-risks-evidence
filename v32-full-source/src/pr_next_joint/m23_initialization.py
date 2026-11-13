"""Approved conditional first-initializer authority takeover; no name-based rule."""
import copy
from .m03_p_paths import op,lit,key,walk
from .m03_p_route import selectors,keys,value_type,effective_permission
from .m20_policy import role_evidence
from .m11_policy import make_query,once_latch
from .m09_shared_policy import implies
from .m04_logic import Unsupported


def constructor_closed(lookup,program,selector):
    """Sufficient inductive nonzero-authority proof, with explicit environment.
    Unsupported constructors, opaque updates or unknown solves reject the proof.
    """
    from .m22_local_state import complete_relevant_updates,clean,_lhs_root
    from .m05_mechanism_core import MechanismPaths,MechanismEncoder
    from .source_entry_identity import function_kind
    from .m20_solver import solve
    root=selector['root'];decl=lookup.nodes.get(root,{})
    if decl.get('scope')!=lookup.contract_node['id'] or not complete_relevant_updates(lookup,program,[root]):return None
    constructors=[f for f in lookup.implementations if function_kind(f)=='constructor']
    if len(constructors)!=1 or constructors[0].get('scope')!=lookup.contract_node['id']:return None
    if any(n.get('nodeType')=='InlineAssembly' or n.get('memberName') in ('delegatecall','callcode') for n in walk(lookup.implementations)):return None
    from .operation_scope import source_operation
    scope=source_operation(lookup,'constructor')
    if scope.get('external') or scope.get('unknown_reasons'):return None
    invariant=op('!=',selector,lit(0));nonzero=op('!=',{'kind':'actual_sender'},lit(0))
    try:
        ps=MechanismPaths(lookup.bundle,lookup.contract).run('constructor');normal=[p for p in ps if p['flow'] not in ('reverted','revert')]
        if not normal or any(not clean(p) for p in normal):return None
        initial=[]
        for p in normal:
            ws=[w for w in p['writes'] if key(w['path'])==key(selector)]
            if not ws or not implies(lookup,{**p,'guards':p['guards']+[nonzero]},op('!=',ws[-1]['value'],lit(0))):return None
            initial.append(ws[-1])
        required={n['id'] for f in lookup.implementations if function_kind(f)!='constructor' for n in walk(f.get('body'))
                  if (n.get('nodeType')=='Assignment' or n.get('nodeType')=='UnaryOperation' and n.get('operator') in ('++','--','delete'))
                  and _lhs_root(n.get('leftHandSide',n.get('subExpression')))==root}
        seen=set();proofs=[]
        for fn,paths in program.items():
            for pi,p in enumerate(paths):
                ws=[w for w in p['writes'] if w['path'].get('root')==root]
                if not ws or p['flow'] in ('reverted','revert'):continue
                if not clean(p):return None
                enc=MechanismEncoder(lookup);z=enc.z
                for t in p.get('evaluated_terms',[]):enc.expr(t)
                guards=[enc.expr(t) for t in p['guards']+[invariant,nonzero]]
                post=enc.expr(op('==',ws[-1]['value'],lit(0)));solver=z.Solver();solver.add(*enc.constraints,*guards,post)
                if solve(solver)!=z.unsat:return None
                seen.update(w['source']['ast_id'] for w in ws)
                proofs.append({'function':fn,'path_index':pi,'post_zero_unsat':True,'sources':[w['source'] for w in ws]})
        if not required<=seen:return None
        return {'kind':'source_constructor_and_all_updates_keep_authority_nonzero','predicate':invariant,'initialization':initial,'preservation':proofs,
                'environment':'nonzero normal external/constructor caller; zero remains a data value','not_whole_contract_safety':True}
    except (Unsupported,ValueError,KeyError,TypeError):return None


def duties(context,state,index):
    rows=[];limits=[]
    for tid,lookup in state['lookups'].items():
        program={f:ps for (t,f),ps in state['paths'].items() if t==tid};proofs={}
        for record in index.by_target[tid]:
            effect=record['effect'];sel=effect.get('selector')
            if not sel or value_type(sel,lookup) not in ('address','address payable'):continue
            role=role_evidence(lookup,program,sel)
            if not role:continue
            p=program[record['function']][record['path_index']]
            if p['flow'] not in ('normal','returned') or p['issues'] or p.get('evaluation_gaps'):continue
            w=effect['original_write'];chosen=w['value']
            if chosen.get('kind')!='actual_sender' and not (chosen.get('kind')=='parameter' and chosen.get('type') in ('address','address payable')):continue
            try:
                empty=op('==',sel,lit(0));latch=once_latch(p,program,lookup)
                if not latch and not implies(lookup,p,empty):continue
                from .m24_normal_boundaries import local_record_allocation
                allocation=local_record_allocation(lookup,program,p,sel,chosen,role)
                if allocation:
                    limits.append({'phase':'initial_authority','target':tid,'function':record['function'],'reason':'source_local_empty_record_registration','certificate':allocation});continue
                if key(sel) not in proofs:proofs[key(sel)]=constructor_closed(lookup,program,sel) if not sel.get('segments') else None
                if proofs[key(sel)]:
                    state.setdefault('_v23_initialization_invariants',{}).setdefault(tid,{})[key(sel)]=proofs[key(sel)]
                    limits.append({'phase':'initial_authority','target':tid,'function':record['function'],'reason':'source_proved_constructor_closed','certificate':proofs[key(sel)]});continue
                model=copy.deepcopy(p);model['guards']+= [empty,op('!=',chosen,lit(0))]
                perms=effective_permission(p['guards'],lookup)
                required=op('or',op('==',{'kind':'actual_sender'},sel),*perms)
                basis={'basis':'source_first_initializer_selects_authority','approved_decision':'v23_D02_initialization',
                    'authority_use_evidence':role,'one_way_latch':latch,'source_chosen_authority':chosen,
                    'scope':'conditional on post-deployment authority still uninitialized; deployment/atomic factory initialization not established; single-use is not caller authorization',
                    'deployment_confirmation':'not_proved','not_a_whole_history_claim':True}
                q=make_query(context,tid,record['function'],record['path_index'],model,w,required,basis,'AC-02');rows.append(q)
                index.use(record,'first_authority_initialization',q['id'])
            except (Unsupported,ValueError) as e:limits.append({'phase':'initial_authority','target':tid,'function':record['function'],'reason':str(e)})
    return rows,limits


def unreachable_initialization(query,state):
    from .m05_mechanism_core import MechanismEncoder
    from .m20_solver import solve
    tid=query['target'];certs=state.get('_v23_initialization_invariants',{}).get(tid,{})
    relevant={s['root'] for s in selectors(query.get('conditions',[]))}
    selected=[c for c in certs.values() if any(s['root'] in relevant for s in selectors(c['predicate']))]
    if not selected:return None
    try:
        e=MechanismEncoder(state['lookups'][tid]);z=e.z
        conditions=[e.expr(x) for x in query['conditions']+[c['predicate'] for c in selected]]
        s=z.Solver();s.add(*e.constraints,*conditions)
        if solve(s)!=z.unsat:return None
        return {'decision':'source_proved_initialization_path_unreachable','source_certificate':selected,
                'scope':'constructor and all relevant updates preserve a state predicate contradicting this path; nonzero normal caller premise',
                'not_whole_contract_safety':True}
    except (Unsupported,ValueError):return None
