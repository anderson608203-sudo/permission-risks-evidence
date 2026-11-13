"""Small proved state facts. No labels, names, or LLM verdicts are inputs.
Inductive scalar facts retain the engine's explicit non-wrapping uint256 scope.
"""
import copy
from .m03_p_paths import key,walk,op,lit
from .m03_p_route import selectors,keys,fields,value_type
from .m04_logic import Unsupported

def clean(p):return p['flow'] in ('normal','returned') and not p['issues'] and not p.get('evaluation_gaps')

def _lhs_root(n):
    while n and n.get('nodeType') in ('IndexAccess','MemberAccess'):
        n=n.get('baseExpression',n.get('expression'))
    return n.get('referencedDeclaration') if n and n.get('nodeType')=='Identifier' else None

def complete_relevant_updates(lookup,program,roots):
    """A writer observed once does not cover its truncated control-flow paths.
    Unrelated incomplete read-only operations do not invalidate a local fact.
    """
    from .operation_scope import source_operation
    roots=set(roots)
    opaque={'entry_identity_unresolved','missing_function_body','assembly_effects_unknown',
            'modifier_unresolved','call_target_unresolved','write_alias_unresolved',
            'array_mutation_alias_unresolved'}
    for fn,paths in program.items():
        scope=source_operation(lookup,fn)
        if scope.get('delegate') or opaque.intersection(scope.get('unknown_reasons',[])):
            return False
        if not roots.intersection(scope.get('writes',[])):continue
        if not paths:return False
        for path in paths:
            # Reverted transactions commit no writes. Every other relevant
            # path must terminate normally with complete effect semantics.
            if path['flow'] in ('reverted','revert'):continue
            if not clean(path):return False
    return True

def positive_scalar(lookup,program,selector):
    cache=getattr(lookup,'_v22_local_state_facts',None)
    if cache is None:cache={};lookup._v22_local_state_facts=cache
    ck=key(['positive',selector])
    if ck in cache:return copy.deepcopy(cache[ck])
    cache[ck]=None
    if selector.get('kind')!='storage' or selector.get('segments') or value_type(selector,lookup) not in ('uint','uint256'):return None
    root=selector['root'];decl=lookup.nodes.get(root,{})
    if not complete_relevant_updates(lookup,program,[root]):return None
    if decl.get('scope')!=lookup.contract_node['id']:return None
    from .source_entry_identity import function_kind
    from .m09_shared_policy import implies
    from .m05_mechanism_core import MechanismPaths
    from .source_scalar_semantics import constant_integer
    bodies=lookup.implementations
    # Opaque writes can invalidate an otherwise convincing scalar invariant.
    for fn in bodies:
        for n in walk(fn):
            if n.get('nodeType')=='InlineAssembly' or n.get('memberName') in ('delegatecall','callcode'):return None
            if n.get('nodeType')=='VariableDeclaration' and n.get('storageLocation')=='storage':return None
    required=set();constructors=[]
    for fn in bodies:
        ctor=function_kind(fn)=='constructor'
        if ctor:constructors.append(fn)
        for n in walk(fn.get('body')):
            if n.get('nodeType')=='Assignment' or n.get('nodeType')=='UnaryOperation' and n.get('operator') in ('++','--','delete'):
                if _lhs_root(n.get('leftHandSide',n.get('subExpression')))==root and not ctor:required.add(n['id'])
    if len(constructors)>1:return None
    invariant=op('>',selector,lit(0));initial=[]
    try:
        initial_value=constant_integer(decl.get('value')) if decl.get('value') else 0
        if constructors:
            ctor=constructors[0]
            if ctor.get('scope')!=lookup.contract_node['id']:return None
            from .operation_scope import source_operation
            scope=source_operation(lookup,'constructor')
            if scope.get('external') or scope.get('unknown_reasons'):return None
            tracer=MechanismPaths(lookup.bundle,lookup.contract);ps=tracer.run('constructor')
            if any(p['flow'] not in ('reverted','revert') and not clean(p) for p in ps):return None
            normal=[p for p in ps if p['flow'] in ('normal','returned')]
            if not normal or any(not clean(p) for p in normal):return None
            for p in normal:
                ws=[w for w in p['writes'] if key(w['path'])==key(selector)]
                if ws:
                    if not implies(lookup,p,op('>',ws[-1]['value'],lit(0))):return None
                    initial.append({'source':ws[-1]['source'],'value':ws[-1]['value'],'conditions':p['guards']})
                elif initial_value is None or initial_value<=0:return None
                else:initial.append({'source':lookup.anchor(decl),'value':lit(initial_value)})
        elif initial_value is not None and initial_value>0:initial=[{'source':lookup.anchor(decl),'value':lit(initial_value)}]
        else:return None
        seen=set();preserved=[]
        for fn,ps in program.items():
            # Relevant AST writers must all be represented; a missing path is
            # never evidence that the write preserves the invariant.
            for pi,p in enumerate(ps):
                ws=[w for w in p['writes'] if w['path'].get('root')==root]
                if not ws:continue
                if p['flow'] not in ('normal','returned'):continue
                if not clean(p):return None
                proof={**p,'guards':p['guards']+[invariant]}
                for w in ws:
                    if key(w['path'])!=key(selector) or not implies(lookup,proof,op('>',w['value'],lit(0))):return None
                    seen.add(w['source'].get('ast_id'))
                    preserved.append({'function':fn,'path_index':pi,'write':w,'source_conditions':p['guards'],'induction_hypothesis':invariant,'proved_postcondition':op('>',w['value'],lit(0))})
        if not required<=seen:return None
        cert={'kind':'source_inductive_positive_scalar','predicate':invariant,'initialization':initial,'preservation':preserved,
              'writer_ast_ids':sorted(required),'covered_writer_ast_ids':sorted(seen),'arithmetic_scope':'existing_nonwrapping_uint256_subcase; not a proof for wrapping executions',
              'solver_result':'initial and preservation obligations proved; unknown rejects fact','not_whole_contract_safety':True}
        cache[ck]=cert;return copy.deepcopy(cert)
    except (Unsupported,ValueError,KeyError,TypeError):return None

def fresh_array_element(lookup,path,effect):
    """An actual compiler-bound array.push allocates a zero-initialized cell."""
    sel=effect.get('selector',{});node=lookup.nodes.get(effect.get('source',{}).get('ast_id'),{})
    if node.get('nodeType')!='FunctionCall':return None
    expr=node.get('expression',{})
    if expr.get('nodeType')!='MemberAccess' or expr.get('memberName')!='push':return None
    typ=expr.get('expression',{}).get('typeDescriptions',{}).get('typeString','')
    if '[]' not in typ or typ.count('[')!=1 or len(node.get('arguments',[]))!=1:return None
    raw=[w for w in path['writes'] if w['source']==effect.get('source') and w['path'].get('root')==sel.get('root')]
    cells=[w for w in raw if len(keys(w['path']))==1 and keys(w['path'])==keys(sel)]
    sizes=[w for w in raw if w['path'].get('segments',[])[-1:]==[{'length':True}]]
    for cell in cells:
        for size in sizes:
            if key(size['value'])!=key(op('+',keys(cell['path'])[0],lit(1))):continue
            return {'kind':'compiler_bound_dynamic_array_append','append_source':lookup.anchor(node),'element':sel,
                    'new_length':size['value'],'allocated_index':keys(cell['path'])[0],
                    'proved_precondition':op('==',sel,lit(0)),
                    'basis':'Solidity dynamic array push creates a new default-valued element before writing the supplied value',
                    'scope':'this exact append and cell; no exemption for writes to old indices or other mappings'}
    return None

def _replace_family_with_zero(value,selector):
    from .m22_assets import identity
    if isinstance(value,dict):
        if value.get('kind')=='storage' and identity(value)==identity(selector):return lit(0)
        return {k:_replace_family_with_zero(v,selector) for k,v in value.items()}
    return [_replace_family_with_zero(x,selector) for x in value] if isinstance(value,list) else value

def fresh_counter_element(lookup,program,path,effect):
    """Check a future-empty namespace invariant, rather than guessing from ++.
    Quantifier-free instantiations are weaker than the inductive invariant;
    only UNSAT obligations establish the arbitrary-key postcondition.
    """
    from .m22_assets import identity
    from .m05_state_relations import expand_write
    from .m20_sequence import read
    from .m09_shared_policy import implies
    from .m05_mechanism_core import MechanismPaths
    from .source_entry_identity import function_kind
    from .source_scalar_semantics import constant_integer
    sel=effect.get('selector',{});ks=keys(sel)
    if len(ks)!=1 or value_type(sel,lookup) not in ('address','address payable'):return None
    increments=[w for w in path['writes'] if (not w['path'].get('segments') or w['path']['segments']==[{'length':True}]) and value_type(w['path'],lookup) in ('uint','uint256') and key(w['value'])==key(op('+',w['path'],lit(1)))]
    for inc in increments:
        counter=inc['path']
        if not complete_relevant_updates(lookup,program,[sel['root'],counter['root']]):continue
        offset=0 if key(ks[0])==key(counter) else 1 if key(ks[0])==key(inc['value']) else None
        if offset is None:continue
        frontier=op('+',counter,lit(offset)) if offset else counter
        cache=getattr(lookup,'_v22_namespace_facts',None)
        if cache is None:cache={};lookup._v22_namespace_facts=cache
        ck=key([identity(sel),counter,offset])
        if ck in cache:
            result=copy.deepcopy(cache[ck])
            if result:return {**result,'allocated_selector':sel,'proved_precondition':op('==',sel,lit(0))}
            continue
        cache[ck]=None
        try:
            # An opaque own-storage write makes the namespace unprovable.
            if any(n.get('nodeType')=='InlineAssembly' or n.get('memberName') in ('delegatecall','callcode') or n.get('nodeType')=='VariableDeclaration' and n.get('storageLocation')=='storage' for fn in lookup.implementations for n in walk(fn)):continue
            arbitrary={'kind':'parameter','id':-920022,'type':'uint256','role':'arbitrary_namespace_key'}
            generic=copy.deepcopy(sel);generic['segments']=[{'key':arbitrary} if 'key' in s else s for s in generic['segments']]
            expanded=lambda p:[e for w in p['writes'] for e in expand_write(w,lookup)]
            constructors=[f for f in lookup.implementations if function_kind(f)=='constructor']
            if len(constructors)>1:continue
            ctor_paths=[]
            if constructors:
                from .operation_scope import source_operation
                scope=source_operation(lookup,'constructor')
                if scope.get('external') or scope.get('unknown_reasons'):continue
                tracer=MechanismPaths(lookup.bundle,lookup.contract);ctor_paths=tracer.run('constructor')
            else:ctor_paths=[{'guards':[],'writes':[],'issues':[],'flow':'normal','evaluated_terms':[]}]
            initial=[];bad=False
            if any(p['flow'] not in ('reverted','revert') and not clean(p) for p in ctor_paths):continue
            for p in ctor_paths:
                if p['flow'] not in ('normal','returned'):continue
                if not clean(p):bad=True;break
                writes=expanded(p);counter_writes=[w for w in writes if key(w['path'])==key(counter)]
                if counter_writes:initial_counter=counter_writes[-1]['value']
                elif counter.get('segments')==[{'length':True}]:initial_counter=lit(0)
                else:
                    dec=lookup.nodes[counter['root']];value=constant_integer(dec.get('value')) if dec.get('value') else 0
                    if value is None:bad=True;break
                    initial_counter=lit(value)
                init_frontier=op('+',initial_counter,lit(offset)) if offset else initial_counter
                after=_replace_family_with_zero(read(generic,writes,lookup),sel)
                pred=op('or',op('<',arbitrary,init_frontier),op('==',after,lit(0)))
                if not implies(lookup,p,pred):bad=True;break
                initial.append({'conditions':p['guards'],'writes':writes,'frontier':init_frontier,'proved':pred})
            if bad or not initial:continue
            required=set()
            for f in lookup.implementations:
                if function_kind(f)=='constructor':continue
                for n in walk(f.get('body')):
                    lhs=n.get('leftHandSide',n.get('subExpression'))
                    if (n.get('nodeType')=='Assignment' or n.get('nodeType')=='UnaryOperation' and n.get('operator') in ('++','--','delete')) and _lhs_root(lhs) in (sel['root'],counter['root']):required.add(n['id'])
                    if n.get('nodeType')=='FunctionCall' and n.get('expression',{}).get('memberName') in ('push','pop') and _lhs_root(n['expression'].get('expression')) in (sel['root'],counter['root']):required.add(n['id'])
            seen=set();steps=[]
            for fn,ps in program.items():
                for pi,p in enumerate(ps):
                    if p['flow'] not in ('normal','returned'):continue
                    writes=expanded(p);relevant=[w for w in writes if w['path'].get('root') in (sel['root'],counter['root'])]
                    if not relevant:continue
                    if not clean(p):bad=True;break
                    seen.update(w['source'].get('ast_id') for w in relevant)
                    old_reads={key(generic):generic}
                    for term in selectors([p['guards'],p.get('evaluated_terms',[]),writes]):
                        if identity(term)==identity(sel):old_reads[key(term)]=term
                    assumptions=[op('or',op('<',keys(s)[0],frontier),op('==',s,lit(0))) for s in old_reads.values()]
                    post_frontier=read(frontier,writes,lookup);post_owner=read(generic,writes,lookup)
                    wanted=op('or',op('<',arbitrary,post_frontier),op('==',post_owner,lit(0)))
                    environment=op('!=',{'kind':'actual_sender'},lit(0))
                    proof={**p,'guards':p['guards']+assumptions+[environment]}
                    if not implies(lookup,proof,wanted):bad=True;break
                    steps.append({'function':fn,'path_index':pi,'conditions':p['guards'],'induction_instances':assumptions,'environment_predicate':environment,'writes':relevant,'proved':wanted})
                if bad:break
            if bad or not required<=seen:continue
            cert={'kind':'source_inductive_future_empty_namespace','counter':counter,'offset':offset,'field_shape':identity(sel),
                  'initialization':initial,'preservation':steps,'covered_writer_ast_ids':sorted(seen),
                  'arithmetic_scope':'existing_nonwrapping_uint256_subcase; no claim for counter rollover',
                  'explicit_environment_assumption':'all external calls in this namespace proof have nonzero callers; zero-valued storage and null holders remain allowed','environment_decision':'user explicitly approved 20261031 research day','not_whole_contract_safety':True}
            cache[ck]=cert
            return {**copy.deepcopy(cert),'allocated_selector':sel,'proved_precondition':op('==',sel,lit(0))}
        except (Unsupported,ValueError,KeyError,TypeError):continue
    return None


def register(state,certificate):
    if not certificate:return None
    from .core import digest
    core={k:v for k,v in certificate.items() if k not in ('allocated_selector','proved_precondition')}
    identity='state_fact_'+digest(core)[:24]
    state.setdefault('_v22_state_certificates',{})[identity]=core
    return {'certificate_id':identity,'kind':certificate['kind'],**{k:certificate[k] for k in ('allocated_selector','proved_precondition') if k in certificate}}
