"""Source-typed operation summaries and selectable policy relations.

No anchor parsing or new instance discovery: this module consumes the current
mechanism paths. LLM choices select an existing relation, never supply code,
SMT, arbitrary slot numbers or a pre-decided risk verdict.
"""
import copy
import networkx as nx
from .core import digest
from .m03_p_paths import key,lit,walk
from .m03_p_route import selectors,keys,value_type,effective_permission,relocate
from .m05_bound_relations import family
from .m05_mechanism_core import program,successful


def enrich_inventory(inventory,context,state):
    result=copy.deepcopy(inventory);graph=nx.MultiDiGraph();summaries=[];choices=[]
    targets={x['target'] for x in result['obligations']}
    for item in result['relations_without_checked_obligation']:targets.add(item['question']['target'])
    for target in sorted(targets):
        lookup,paths,errors=program(state,target)
        for fn,branches in paths.items():
            fid=digest([context['identity'],target,fn]);graph.add_node(fid,kind='source_function',target=target,function=fn)
            selected=[]
            for pi,p in enumerate(branches):
                if not successful(p):continue
                entry={'path_index':pi,'conditions':p['guards'],'writes':p['writes'],
                    'native_transfers':p.get('native_transfers',[]),'read_calls':p.get('read_calls',[]),
                    'source_calls':p.get('source_calls',[]),'issues':p['issues'],
                    'source':p.get('entry_source')}
                selected.append(copy.deepcopy(entry))
                for direction,expr in [('reads',p['guards']),('writes',[w['path'] for w in p['writes']])]:
                    for s in selectors(expr):
                        sid=digest([context['identity'],target,s]);graph.add_node(sid,kind='typed_selector',selector=s)
                        graph.add_edge(fid,sid,relation=direction,path_index=pi,
                            scope='exact extracted expression; no key or instance equivalence inferred')
            summaries.append({'target':target,'function':fn,'paths':selected,'extraction_errors':errors,
                'scope':'finite existing source paths; supplied external instance assumptions retained'})
    result.update(relation_catalog={'schema':'typed-relation-catalog-v1','identity':context['identity'],
        'operation_summaries':summaries,'choices':choices,
        'graph':{'engine':'NetworkX MultiDiGraph','nodes':[{'id':n,**d} for n,d in graph.nodes(data=True)],
            'edges':[{'source':a,'target':b,**d} for a,b,d in graph.edges(data=True)]},
        'scope':'existing typed paths only; relations are hypotheses until consumed; no safety verdict'})
    result.pop('digest',None);result['digest']=digest(result)
    return result


def apply_choices(bound,response,inventory):
    from .core import require
    require(not response.get('relation_choices'), 'RETIRED_RELATION_CHOICES')
    return bound
