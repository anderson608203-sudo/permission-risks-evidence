"""M2-reviewed frame obligations from a consumed source dependency graph.

No labels or name heuristics enter here. The graph is deliberately coarse at
storage-root granularity. M4 reconstructs the footprint and graph, then encodes
the source frame rule as pre/post equalities. This proves a scoped absence of
permission/ledger change, not all contract behavior or reachable deployment.
"""
import copy
import networkx as nx
from .core import digest
from .m03_p_paths import walk, key
from .m03_p_route import selectors, keys
from .m04_logic import Unsupported


def root_set(value):
    return {s['root'] for s in selectors(value)}


def source_graph(lookup):
    graph=nx.MultiDiGraph();program={};guard_roots=set();unknown=set();failures=[]
    for f in lookup.contract['functions']:
        fn=f['signature'];node='function:'+fn;graph.add_node(node,kind='function')
        try:paths=lookup.run(fn)
        except Exception as ex:
            paths=[];unknown.add(node)
            failures.append({'function':fn,'reason':type(ex).__name__+':'+str(ex)})
        program[fn]=paths
        # AST references include pure return expressions that do not appear as
        # writes. This prevents display/pricing dependencies from disappearing.
        try: ast=lookup.function(fn)
        except Exception: ast={}
        ast_reads={n.get('referencedDeclaration') for n in walk(ast)
                   if lookup.nodes.get(n.get('referencedDeclaration'),{}).get('stateVariable')}
        for root in sorted(ast_reads):
            graph.add_node('state:'+str(root),kind='state',ast_id=root)
            graph.add_edge('state:'+str(root),node,relation='source_reference')
        for pi,path in enumerate(paths):
            if path['flow']=='reverted':continue
            if path['issues']:unknown.add(node)
            guards=root_set(path['guards']);guard_roots.update(guards)
            reads=guards | root_set([w['value'] for w in path['writes']])
            for root in sorted(reads):
                graph.add_node('state:'+str(root),kind='state',ast_id=root)
                graph.add_edge('state:'+str(root),node,relation='read',path_index=pi)
            for w in path['writes']:
                root=w['path']['root'];graph.add_node('state:'+str(root),kind='state',ast_id=root)
                graph.add_edge(node,'state:'+str(root),relation='write',path_index=pi,source=w['source'])
    data={'engine':'NetworkX MultiDiGraph','kind':'post_M2_state_dependency',
          'nodes':[{'id':n,**d} for n,d in sorted(graph.nodes(data=True))],
          'edges':[{'from':a,'to':b,**d} for a,b,d in graph.edges(data=True)],
          'unknown_functions':sorted(unknown),'extraction_failures':failures,'guard_roots':sorted(guard_roots),
          'scope':'declared target source paths, state-root overapproximation; unknown effects block affected cones'}
    data['id']='graph_'+digest(data)
    return graph,program,data


def certificate(graph,program,data,fn,pi,protected):
    if fn not in program or pi>=len(program[fn]):raise Unsupported('frame_source_path_missing')
    path=program[fn][pi]
    if path['flow']=='reverted' or path['issues']:raise Unsupported('frame_source_path_unresolved')
    if not path['writes']:raise Unsupported('frame_no_source_write')
    if any(w['path'].get('instance') for w in path['writes']):raise Unsupported('frame_external_storage_instance')
    changed=sorted({w['path']['root'] for w in path['writes']})
    reached=set()
    for root in changed:
        node='state:'+str(root);reached.add(node)
        if node in graph:reached.update(nx.descendants(graph,node))
    if any('state:'+str(root) in reached for root in protected):raise Unsupported('frame_dependency_reaches_protected_state')
    if reached.intersection(data['unknown_functions']):raise Unsupported('frame_dependency_reaches_unknown_effect')
    if not protected:raise Unsupported('frame_empty_protected_state')
    return {'graph_id':data['id'],'changed_roots':changed,'protected_roots':sorted(protected),
            'reached_nodes':sorted(reached),'source_path_digest':digest(path),
            'relation':'changed-state forward closure disjoint from protected state and unknown effects'}


def models_from_source(lookup):
    from .m03_p_assets import AssetPaths,asset_models
    from .m04_asset_math import proportional_models
    asset_lookup=AssetPaths(lookup.bundle,lookup.contract,lookup.limit)
    program={f['signature']:asset_lookup.run(f['signature']) for f in lookup.contract['functions']}
    return asset_models(asset_lookup,program)+proportional_models(asset_lookup,program)


def add_graph_controls(queries,coverage,context,state):
    reviews={(x['target'],x['function']):x for x in coverage['function_reviews']}
    graphs=[];added=[];declined=[]
    for target,lookup in state['lookups'].items():
        graph,program,data=source_graph(lookup);graphs.append({'target':target,**data})
        try:models=models_from_source(lookup)
        except Exception as ex:
            declined.append({'target':target,'reason':'frame_asset_extraction_failed:'+type(ex).__name__+':'+str(ex)})
            continue # Decline this optional control; preserve other bound queries.
        for fn,paths in program.items():
            review=reviews.get((target,fn))
            if not review or review['disposition']=='unresolved':continue
            for pi,path in enumerate(paths):
                if not path['writes'] or path['issues'] or path['flow']=='reverted':continue
                w=path['writes'][0]
                # Do not silently supersede any M2 risk/uncertainty for the same
                # property. An additional frame check addresses a different rule.
                options=[]
                personal=(review['disposition']=='no_risk_hypothesis'
                          and all(keys(x['path']) and keys(x['path'])[-1]=={'kind':'actual_sender'} for x in path['writes']))
                if personal:options.append(('AC-02',set(data['guard_roots']),None))
                for model in models:
                    from .m05_asset_registry import roots
                    protected=roots(model)
                    options.append(('FCR-MINT',protected,model))
                for rule,protected,model in options:
                    if any(q['target']==target and q['function']==fn and q['rule']==rule and q['path_index']==pi for q in queries):continue
                    try:proof=certificate(graph,program,data,fn,pi,protected)
                    except Unsupported as ex:
                        declined.append({'target':target,'function':fn,'path_index':pi,'rule':rule,'reason':str(ex)})
                        continue
                    q={'rule':rule,'target':target,'function':fn,'path_index':pi,
                       'conditions':copy.deepcopy(path['guards']),'issues':[],
                       'effect':{'object':lookup.nodes[w['path']['root']]['name'],'selector':copy.deepcopy(w['path']),
                                 'value':copy.deepcopy(w['value']),'operator':w['operator'],'source':copy.deepcopy(w['source'])},
                       'program_id':context['identity']['program_id'],'build_id':context['identity']['build_id'],
                       'required_policy_candidate':None,'policy_basis':{'asset_model':model} if model else {},
                       'proposal_id':None,'policy_scope':'program_derived_frame',
                       'query_origin':'M2_reviewed_graph_frame_control','llm_function_review':copy.deepcopy(review),
                       'llm_rationale':review['explanation'],'llm_policy_basis':{'kind':'program_relation',
                           'source_ast_ids':[x['source']['ast_id'] for x in path['writes']],
                           'explanation':'M2 function review plus program dependency closure; M4 checks source frame relation'},
                       'source_remarks':[],'alternatives':[],
                       'graph_frame_obligation':{'kind':'permission_state_frame' if rule=='AC-02' else 'entitlement_state_frame',
                           'certificate':proof,'asset_model':copy.deepcopy(model),
                           'scope':'unchanged declared permission/entitlement storage; no global safety or payout guarantee'}}
                    q['id']='q_'+digest(q);queries.append(q);added.append(q['id'])
    coverage['derived_control_queries'].extend(added)
    coverage['graph_frame_controls']={'queries':added,'declined':declined}
    return queries,coverage,graphs


def state_sort(e,node):
    z=e.z;kind=node.get('nodeType')
    if kind=='Mapping':return z.ArraySort(state_sort(e,node['keyType']),state_sort(e,node['valueType']))
    if kind!='ElementaryTypeName':raise Unsupported('frame_storage_type_not_lowered')
    typ=node.get('name','')
    if typ=='bool':return z.BoolSort()
    e.width(typ)
    return z.IntSort()


def frame_formula(e,row):
    obligation=row['graph_frame_obligation'];lookup=e.lookup;z=e.z
    graph,program,data=source_graph(lookup)
    protected=obligation['certificate']['protected_roots']
    actual=certificate(graph,program,data,row['function'],row['path_index'],protected)
    if actual!=obligation['certificate']:raise Unsupported('frame_certificate_not_current_source')
    path=program[row['function']][row['path_index']]
    if row['conditions']!=path['guards']:raise Unsupported('frame_conditions_not_current_source')
    effect=row['effect']
    if not any(effect['selector']==w['path'] and effect['value']==w['value'] and effect['source']==w['source'] for w in path['writes']):
        raise Unsupported('frame_effect_not_current_source')
    if row['rule']=='AC-02':
        if protected!=data['guard_roots']:raise Unsupported('frame_permission_roots_not_source_guards')
    elif row['rule']=='FCR-MINT':
        model=obligation['asset_model']
        if model not in models_from_source(lookup):raise Unsupported('frame_asset_relation_not_current_source')
        from .m05_asset_registry import roots
        if protected!=sorted(roots(model)):raise Unsupported('frame_asset_roots_mismatch')
    else:raise Unsupported('frame_rule_not_supported')
    # Each entire mapping (not one sampled holder) is framed. Integer sorts are
    # a conservative enlargement; UNSAT does not depend on tight value bounds.
    equalities=[];differences=[]
    for root in protected:
        node=lookup.nodes.get(root,{})
        if not node.get('stateVariable'):raise Unsupported('frame_not_source_state')
        sort=state_sort(e,node.get('typeName',{}))
        before=z.Const('frame_pre_'+str(root),sort);after=z.Const('frame_post_'+str(root),sort)
        equalities.append(after==before);differences.append(after!=before)
    domain=z.And(*[e.expr(g) for g in path['guards']],*equalities)
    return domain,z.Or(*differences),{'kind':obligation['kind'],
        'checks':['source-reconstructed complete path footprint','dependency cone disjointness',
                  'whole declared storage frame relation','original path premise and forbidden protected-state change'],
        'certificate':actual,'assumption':obligation['scope']}
