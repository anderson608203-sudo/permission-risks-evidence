"""Exact affine unsigned counter updates for conditional lifecycle P analysis.

Compose retained source expressions across activation/deactivation snapshots.
Checked arithmetic adds no-wrap conditions; it never assumes modular wraparound.
No solver, transaction, case name, field name, or expected-result dependency.
"""
import copy,re
from .core import digest
from .m03_p_paths import key,walk,op,lit,normalize,conditions_possible


def needs_counter_model(enabled,disabled):
    return any(n.get('kind')=='op' and n.get('op') in ('+','-','*','/','%')
               for t in (enabled,disabled) for w in t['writes'] for n in walk(w['value']))


def affine(expr):
    e=normalize(expr)
    if e.get('kind')=='literal' and type(e.get('value')) is int:return None,e['value']
    if e.get('kind')=='parameter' and str(e.get('type','')).startswith('uint'):return e,0
    if e.get('kind')=='op' and e['op'] in ('+','-') and len(e['args'])==2:
        left=affine(e['args'][0]);right=affine(e['args'][1])
        if left is None or right is None:return None
        a,x=left;b,y=right
        if b is None:return a,x+(y if e['op']=='+' else -y)
        if a is None and e['op']=='+':return b,x+y
        if e['op']=='-' and key(a)==key(b):return None,x-y
    return None


def expression(form):
    base,offset=form
    if base is None:return lit(offset)
    return copy.deepcopy(base) if offset==0 else op('+',copy.deepcopy(base),lit(offset))


def counter_term(v):
    return any(x.get('kind')=='parameter' and str(x.get('id','')).startswith('lifecycle_pre:') for x in walk(v))


def rewrite(v,issues):
    if isinstance(v,list):return [rewrite(x,issues) for x in v]
    if not isinstance(v,dict):return v
    v={k:rewrite(x,issues) for k,x in v.items()};v=normalize(v)
    if v.get('kind')!='op':return v
    operator=v['op'];args=v['args']
    if operator in ('+','-'):
        form=affine(v)
        if form is not None:return expression(form)
    if operator in ('==','!=','<','<=','>','>=') and len(args)==2 and counter_term(v):
        a,b=map(affine,args)
        if a is None or b is None:
            issues.append({'reason':'version_predicate_not_in_affine_profile','condition':v});return v
        left,x=a;right,y=b
        if key(left)==key(right):return normalize(op(operator,lit(x),lit(y)))
        if right is None:return normalize(op(operator,left,lit(y-x)))
        if left is None:return normalize(op(operator,lit(x-y),right))
        issues.append({'reason':'independent_counter_relation_not_lowered','condition':v})
    return v


def compose(lookup,enabled,disabled,active,credential,action_issues):
    from .m03_p_route import value_type,relocate
    from .m03_p_lifecycle import same_record
    post={};established=set();issues=copy.deepcopy(action_issues);constraints=[];initial={};events=[];valid=True
    def domain(selector):
        typ=value_type(selector,lookup);match=re.fullmatch(r'uint(\d*)',typ or '')
        if not match:return None
        bits=int(match[1] or 256)
        return typ,2**bits-1
    def prestate(selector):
        k=key(selector)
        if k not in initial:
            typ,maximum=domain(selector)
            term={'kind':'parameter','id':'lifecycle_pre:'+digest(selector),'type':typ}
            initial[k]={'selector':copy.deepcopy(selector),'symbol':term,'minimum':0,'maximum':maximum}
            constraints.extend([op('>=',term,lit(0)),op('<=',term,lit(maximum))])
        return copy.deepcopy(initial[k]['symbol'])
    def manager(v):
        if isinstance(v,dict):
            if v.get('kind')=='actual_sender':return {'kind':'transition_caller','type':'address'}
            return {k:manager(x) for k,x in v.items()}
        return [manager(x) for x in v] if isinstance(v,list) else v
    for phase,t in [('activation',enabled),('deactivation',disabled)]:
        before=copy.deepcopy(post)
        def resolve(v):
            if isinstance(v,dict):
                if v.get('kind')=='storage':
                    if key(v) in before:return copy.deepcopy(before[key(v)])
                    if same_record(v,active) and domain(v):return prestate(v)
                return {k:resolve(x) for k,x in v.items()}
            return [resolve(x) for x in v] if isinstance(v,list) else v
        # Replace the management caller BEFORE substituting object/actor
        # parameters, so the revoked actor is not changed to the administrator.
        path_guards=t.get('guards',[])
        phase_guards=[]
        for g in path_guards:
            try:phase_guards.append(resolve(relocate(manager(g),t['write']['path'],credential)))
            except ValueError:issues.append({'reason':'transition_precondition_unbound','phase':phase})
        constraints.extend(phase_guards)
        updates=[]
        for w in t['writes']:
            if w['path']['root']!=active['root']:continue
            try:
                selector=relocate(w['path'],t['write']['path'],credential)
                value=relocate(w['value'],t['write']['path'],credential)
            except ValueError:
                issues.append({'reason':'transition_object_or_value_unbound','phase':phase,'source':w['source']});continue
            if not same_record(selector,active):
                issues.append({'reason':'transition_other_key_alias_unresolved','phase':phase,'source':w['source']});continue
            value=resolve(value);integer=domain(selector)
            if integer:
                typ,maximum=integer
                source_node=lookup.nodes.get(w.get('source',{}).get('ast_id'),{})
                if any(n.get('nodeType')=='FunctionCall' and n.get('kind')=='typeConversion' for n in walk(source_node)):
                    issues.append({'reason':'transition_integer_cast_not_lowered','phase':phase,'source':w['source']});continue
                if w['operator'] not in ('=','+=','-=','++','--') or affine(value) is None:
                    issues.append({'reason':'transition_integer_operation_not_lowered','phase':phase,'source':w['source']});continue
                # Paths has already substituted earlier writes in this source
                # function. Resolve all RHS against the phase-start snapshot,
                # not again against every preceding write in the same phase.
                for n in walk(value):
                    if n.get('kind')=='op' and n['op'] in ('+','-'):
                        constraints.extend([op('>=',n,lit(0)),op('<=',n,lit(maximum))])
                value=expression(affine(value))
            elif w['operator']!='=':
                issues.append({'reason':'transition_nonassignment_not_lowered','phase':phase,'source':w['source']});continue
            post[key(selector)]=value
            if phase=='activation':established.add(key(selector))
            updates.append({'selector':selector,'value':value,'operator':w['operator'],'source':w['source']})
        if post.get(key(active))!=lit(phase=='activation'):valid=False
        events.append({'phase':phase,'function':t['function'],'updates':updates,'preconditions':phase_guards})
    constraints=[rewrite(c,issues) for c in constraints]
    if not issues:
        try:
            if not conditions_possible(constraints):valid=False
        except ValueError as ex:issues.append({'reason':str(ex)})
    details={'profile':'checked_unsigned_affine_counter_v1','initial_state':list(initial.values()),
             'transitions':events,'conditions':constraints,
             'arithmetic':'mathematical affine values under original checked-uint no-overflow conditions; no modular wrap',
             'scope':'activation then deactivation of the same credential; no stale-signature, expiry or all-history claim'}
    return post,established,issues,valid,details
