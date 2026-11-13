"""Source-local condition applicability; no names, labels or LLM verdicts."""
import copy
from .m03_p_paths import key,walk,normalize

def routing_records(program):
    result={}
    for fn,paths in program.items():
        groups={}
        for p in paths:
            if p['flow'] not in ('normal','returned') or p['issues']:continue
            resources={(w['path']['root'],key(w['path'].get('instance')),key(normalize(w['path']))) for w in p['writes']}
            for b in p.get('branch_choices',[]):
                k=(b['source'].get('ast_id'),key(normalize(b['condition'])))
                g=groups.setdefault(k,{'condition':b['condition'],'source':b['source'],'sides':{True:set(),False:set()}})
                g['sides'][b['sign']].update(resources)
        result[fn]=[{'condition':copy.deepcopy(g['condition']),'source':g['source'],'resource_root':r,'instance_key':i,'resource_selector_key':selector,
            'basis':'both_source_branch_polarities_commit_to_same_resource','claim':'branch_predicate_not_universal_resource_authorization'}
            for g in groups.values() for r,i,selector in sorted(g['sides'][True]&g['sides'][False],key=str)]
    return result

def branch_atom(expr):
    expr=normalize(expr)
    while expr.get('kind')=='op' and expr.get('op')=='!':expr=expr['args'][0]
    return key(normalize(expr))

def route_for(lookup,fn,predicate,resource):
    atom=branch_atom(predicate)
    for r in getattr(lookup,'routing_records',{}).get(fn,[]):
        if resource.get('root')==r['resource_root'] and key(resource.get('instance'))==r['instance_key'] and key(normalize(resource))==r['resource_selector_key'] and branch_atom(r['condition'])==atom:
            return copy.deepcopy(r)
    return None

def control_conditions(guards,control,evaluated_terms=(),routing_predicates=()):
    selected=[];excluded=[];wanted=key(control)
    def scalar_control(x):
        def visit(n):
            if key(n)==wanted:return True,True
            if n.get('kind')=='literal':return False,True
            if n.get('kind')=='op' and n.get('op') in ('+','-','*','/','%'):
                pairs=[visit(a) for a in n['args']]
                return any(p[0] for p in pairs),all(p[1] for p in pairs)
            return False,False
        found,valid=visit(x);return found and valid
    def direct(x):
        if key(x)==wanted:return True
        if x.get('kind')=='op' and x.get('op')=='!':return direct(x['args'][0])
        if x.get('kind')=='op' and x.get('op') in ('and','&&','or','||'):return any(direct(a) for a in x['args'])
        if x.get('kind')=='op' and x.get('op') in ('==','!=','<','<=','>','>='):
            return any(scalar_control(a) and (b.get('kind') in ('literal','parameter','actual_sender','enum_value')
                or b.get('kind')=='environment' and b.get('field') in ('timestamp','number'))
                for a,b in (x['args'],x['args'][::-1]))
        return False
    # Exact arithmetic-domain guards are not permission controls. Inlined
    # SafeMath may turn 100-fee into require(fee<=100); retain that requirement
    # in the source feasibility domain but never call arithmetic failure PAUSE.
    arithmetic_domains=[]
    for value in walk(evaluated_terms):
        if value.get('kind')!='checked_evaluation' or value.get('type') not in ('uint','uint256'):continue
        expr=value.get('input',{})
        if expr.get('kind')=='op' and expr.get('op')=='-' and len(expr.get('args',[]))==2:
            a,b=expr['args'];arithmetic_domains.extend([normalize({'kind':'op','op':'>=','args':[a,b]}),normalize({'kind':'op','op':'<=','args':[b,a]})])
    arithmetic_keys={key(x) for x in arithmetic_domains}
    arithmetic_excluded=[];route_excluded=[]
    route_keys={key(normalize(r['condition'])) for r in routing_predicates}
    def route_atom(e):
        while e.get('kind')=='op' and e.get('op')=='!':e=e['args'][0]
        return key(normalize(e))
    def visit(v):
        e=normalize(v)
        if e.get('kind')=='op' and e.get('op') in ('and','&&'):
            for a in e['args']:visit(a)
            return
        if not any(n.get('kind')=='storage' and key(n)==wanted for n in walk(e)):return
        if route_atom(e) in route_keys:
            route_excluded.append(e);excluded.append(e)
        elif key(e) in arithmetic_keys:
            arithmetic_excluded.append(e);excluded.append(e)
        else:(selected if direct(e) else excluded).append(e)
    for g in guards:visit(g)
    return selected,{'selected_permission_predicates':selected,'excluded_calculation_dependencies':excluded,'excluded_exact_arithmetic_domain_guards':arithmetic_excluded,'excluded_successful_transfer_branch_choices':route_excluded,
        'claim':'source_local_permission_effect; arithmetic_failure_alone_is_not_pause'}
