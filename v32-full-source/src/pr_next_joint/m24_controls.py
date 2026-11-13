"""Source control mutations that enable a protected sensitive operation.
This is an authorization-lifetime check, not generic denial of service. A
disable-only change cannot satisfy the enabling counterexample.
"""
import copy
from .m03_p_paths import op,lit,key,walk
from .m03_p_route import selectors,effective_permission,keys,value_type
from .m11_policy import make_query
from .m05_state_relations import compose_read
from .m04_logic import Unsupported

def replace_reads(v,writes,lookup):
    if isinstance(v,dict):
        if v.get('kind')=='storage':return compose_read(v,writes,lookup)
        return {k:replace_reads(x,writes,lookup) for k,x in v.items()}
    return [replace_reads(x,writes,lookup) for x in v] if isinstance(v,list) else v

def duties(context,state,shared,index):
    rows=[];limits=[]
    from .m21_admission import atoms
    for tid,lookup in state['lookups'].items():
        program={f:ps for (t,f),ps in state['paths'].items() if t==tid}
        routes=[]
        for fn,ps in program.items():
            for pi,p in enumerate(ps):
                if p['flow'] not in ('normal','returned') or p['issues'] or p.get('evaluation_gaps'):continue
                # A source-protected payout, asset debit, authority/code-target
                # update is required; an arbitrary conditional counter is not.
                effects=p.get('sensitive_effects',[])
                asset_roots={a['balance_root'] for a in shared.get(tid,{}).get('assets',[])}
                sensitive=effects or any(w['path']['root'] in asset_roots for w in p['writes'])
                if not sensitive:continue
                perms=effective_permission(p['guards'],lookup)
                perms=[g for g in perms if selectors(g) and not any(n.get('kind')=='parameter' for n in walk(g))]
                if not perms:continue
                authkeys={key(a) for a in atoms(perms)}
                for condition in atoms(p['guards']):
                    if key(condition) in authkeys:continue
                    controls=[s for s in selectors(condition) if not keys(s) and s['root'] not in asset_roots and value_type(s,lookup).startswith(('uint','bool'))]
                    if not controls:continue
                    # Only explicit time/access flags; financial quantity and
                    # arbitrary business comparisons remain out of this rule.
                    if not any(n.get('kind')=='environment' and n.get('field')=='timestamp' for n in walk(condition)) and not any(value_type(s,lookup)=='bool' for s in controls):continue
                    if any(n.get('kind')=='parameter' for n in walk(condition)):continue
                    from .m24_normal_boundaries import direct_lifetime_condition
                    if not direct_lifetime_condition(condition,lookup):continue
                    routes.append((fn,pi,p,condition,controls,perms))
        for record in index.by_target[tid]:
            effect=record['effect'];sel=effect.get('selector');w=effect.get('original_write')
            if not sel or not w:continue
            p=program[record['function']][record['path_index']]
            if p['flow'] not in ('normal','returned') or p['issues'] or p.get('evaluation_gaps'):continue
            for fn,pi,target,condition,controls,perms in routes:
                if not any(key(sel)==key(s) for s in controls):continue
                try:
                    after=replace_reads(condition,p['writes'],lookup)
                    if key(after)==key(condition):continue
                    # Prove a complete affected operation is feasible after the setter,
                    # with its own legitimate caller/arguments. A single enabled
                    # conjunct is insufficient if another source guard forbids it.
                    from .m05_mechanism_core import remap
                    caller={'kind':'parameter','id':-1700000000-abs(w['source']['ast_id']),'type':'address'}
                    mapping={n['id']:{**n,'id':-1600000000-abs(n['id'])} for n in walk(target) if n.get('kind')=='parameter'}
                    active=replace_reads(remap(target['guards'],mapping,caller),p['writes'],lookup)
                    local=copy.deepcopy(p);local['guards'] += [op('!',condition),after,op('!=',caller,lit(0))]+active
                    local['evaluated_terms']=copy.deepcopy(p.get('evaluated_terms',[]))+replace_reads(remap(target.get('evaluated_terms',[]),mapping,caller),p['writes'],lookup)
                    required=op('or',*perms,*effective_permission(p['guards'],lookup))
                    basis={'basis':'source_authorization_lifetime_control_mutation',
                        'protected_operation':fn,'protected_path_index':pi,'source_permission':perms,
                        'source_control_condition':condition,'post_control_condition':after,'complete_post_operation_guards':active,
                        'sensitive_effect_sources':[e['source'] for e in target.get('sensitive_effects',[])],
                        'scope':'unauthorized change enabling a source-protected operation outside its previous time/control condition; disable-only is excluded; source local-policy inference'}
                    q=make_query(context,tid,record['function'],record['path_index'],local,w,required,basis,'AC-04')
                    rows.append(q);index.use(record,'authorization_lifetime_control',q['id'])
                except (Unsupported,ValueError) as ex:limits.append({'phase':'authorization_control','target':tid,'function':record['function'],'reason':str(ex)})
    return rows,limits
