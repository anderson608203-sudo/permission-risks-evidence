"""Source-derived permission/equity dependency tasks, then path-bound consumers.
Edges locate evidence; only consumers establish authorization/effect semantics.
"""
import copy
from collections import defaultdict
from .core import digest
from .m03_p_paths import walk,key
from .m03_p_route import selectors,keys,fields,value_type

def light_tasks(context,lookups):
    refs=context['references'];by_ast={(r['target'],r['ast_id']):k for k,r in refs.items()}
    read_index=defaultdict(set);write_index=defaultdict(set);inventory=[];operations={o['id']:o for o in context['operations']}
    for o in context['operations']:
        lookup=lookups[o['target']];read=set();write=set();effects=[]
        for aid in o['source_ast_ids']:
            n=lookup.nodes.get(aid,{})
            rd=n.get('referencedDeclaration')
            if lookup.nodes.get(rd,{}).get('stateVariable'):read.add(rd)
        for aid in o['write_ast_ids']:
            n=lookup.nodes.get(aid,{})
            lhs=n.get('leftHandSide',n.get('subExpression',{}))
            roots={x.get('referencedDeclaration') for x in walk(lhs) if lookup.nodes.get(x.get('referencedDeclaration'),{}).get('stateVariable')}
            if not roots:continue
            write.update(roots)
            evidence=by_ast.get((o['target'],aid))
            if evidence:effects.append({'source_ref':evidence,'kind':'indexed_record_update' if any(x.get('nodeType')=='IndexAccess' for x in walk(lhs)) else 'state_replacement','root_refs':[by_ast[o['target'],r] for r in sorted(roots) if (o['target'],r) in by_ast]})
        for aid in o['call_ast_ids']:
            n=lookup.nodes.get(aid,{});expr=n.get('expression',{})
            from .source_entry_identity import builtin_call
            kind=None
            if builtin_call(n,lookup,('selfdestruct','suicide')):kind='contract_destruction'
            elif any(x.get('memberName')=='delegatecall' for x in walk(expr)):kind='code_execution'
            elif any(x.get('memberName') in ('transfer','send','call') for x in walk(expr)):kind='value_or_external_call'
            if kind and (o['target'],aid) in by_ast:effects.append({'source_ref':by_ast[o['target'],aid],'kind':kind,'root_refs':[]})
        for r in read:read_index[o['target'],r].add(o['id'])
        for r in write:write_index[o['target'],r].add(o['id'])
        inventory.append({'operation':o['id'],'effects':effects,'read_roots':sorted(read),'write_roots':sorted(write)})
    tasks=[];edges=[];dependencies={}
    for row in inventory:
        if not row['effects']:continue
        o=operations[row['operation']];neighbors=set()
        for r in row['write_roots']:
            neighbors.update(read_index[o['target'],r]);neighbors.update(write_index[o['target'],r])
        for r in row['read_roots']:neighbors.update(write_index[o['target'],r])
        neighbors.discard(o['id'])
        for peer in sorted(neighbors):edges.append({'from':o['id'],'to':peer,'kind':'source_effect_dependency','not_authorization_proof':True})
        anchored=[]
        for root in sorted(set(row['read_roots']+row['write_roots'])):
            ref=by_ast.get((o['target'],root))
            writers=write_index[o['target'],root]
            readers=read_index[o['target'],root]
            if ref and (writers-{o['id']} or (o['id'] in writers and readers-{o['id']})):
                # Operation IDs already resolve their source statements in the wire context.
                dependencies[ref]=[sorted(writers),sorted(readers)]
                anchored.append(ref)
        tasks.append({'task_id':'task_'+digest([o['id'],row['effects']])[:16],'op_ref':o['id'],
            'effect_sites':[[e['source_ref'],e['kind'],e['root_refs']] for e in row['effects']],
            'state_dependencies':anchored,
            'effect_refs':list(dict.fromkeys(e['source_ref'] for e in row['effects'])),'effect_kinds':sorted(set(e['kind'] for e in row['effects'])),
            'related_op_refs':sorted(neighbors),
            'read_after_write_op_refs':sorted({peer for root in row['write_roots'] for peer in read_index[o['target'],root] if peer!=o['id']}),
            'questions':['identify_actor_and_affected_subject','authorization_creation_use_and_phase','normal_delegation_or_compensation','independent_equity_or_auxiliary_index','gross_net_quantity_and_allowance_when_applicable'],
            'facts_do_not_assert_vulnerability':True})
    return {'schema':'permission-equity-operation-dependencies-v29','tasks':tasks,'edges':edges,
            'state_dependencies_by_declaration':dependencies,'dependency_columns':['writer_operations','reader_operations'],
            'all_source_preserved':True,'scope':'source effect dependency for retrieval; roles and phase remain proposals'}

class EffectIndex:
    def __init__(self,state):
        self.records=[];self.by_target=defaultdict(list);self.by_operation=defaultdict(list);self.writers=defaultdict(list)
        self.operation_summaries=[];self.uses=[];self.semantic_edges=[];self.stage_links=[]
        for (tid,fn),paths in state['paths'].items():
            lookup=state['lookups'][tid]
            for pi,p in enumerate(paths):
                if p['flow'] not in ('normal','returned'):continue
                effects=[]
                from .m05_state_relations import expand_write
                for w in p['writes']:
                    try:expanded=expand_write(w,lookup)
                    except (ValueError,TypeError):expanded=[w]
                    for e in expanded:
                        effects.append({'kind':'state_write','selector':e['path'],'value':e['value'],'operator':e['operator'],'source':e['source'],'original_write':e})
                effects.extend(copy.deepcopy(p.get('sensitive_effects',[])))
                for e in effects:
                    rid='effect_'+digest([tid,fn,pi,e])[:20]
                    r={'id':rid,'target':tid,'function':fn,'path_index':pi,'effect':e,'conditions':p['guards'],
                       'issues':p['issues'],'source_evaluation_terms':p.get('evaluated_terms',[])}
                    self.records.append(r);self.by_target[tid].append(r);self.by_operation[tid,fn].append(r)
                    s=e.get('selector')
                    if s:self.writers[tid,s['root'],tuple(fields(s))].append(r)
                self.operation_summaries.append({'target':tid,'function':fn,'path_index':pi,
                    'condition_roots':sorted({s['root'] for g in p['guards'] for s in selectors(g)}),
                    'effect_ids':[r['id'] for r in self.by_operation[tid,fn] if r['path_index']==pi],
                    'analysis_gaps':copy.deepcopy(p.get('issues',[])+p.get('evaluation_gaps',[])),
                    'state_model':'source paths; caller and indexed instances preserved'})
    def bind_semantics(self,context,relations,scopes):
        operations={o['id']:o for o in context['operations']}
        for relation in relations['relations']:
            scoped=scopes[relation['id']]
            for field in ('actors','resources','conditions'):
                for item in scoped[field]:
                    self.semantic_edges.append({'relation_id':relation['id'],'kind':field,
                        'target':scoped['target'],'binding':copy.deepcopy(item),
                        'status':'source_expression_bound; high-level applicability still requires consumer checks'})
            for link in relation.get('operation_links',[]):
                source=operations[link['from_op_ref']];dest=operations[link['to_op_ref']]
                self.stage_links.append({**copy.deepcopy(link),'relation_id':relation['id'],
                    'target':source['target'],'from_function':source['function'],'to_function':dest['function'],
                    'status':'source_endpoints_located; order and constraints require finite composition'})
    def rewrite_query_ids(self,mapping):
        by_id={r['id']:r for r in self.records}
        for u in self.uses:
            q=u.get('query_id')
            if q is None:continue
            u['origin_query_id']=q;u['query_ids']=mapping.get((by_id[u['effect_id']]['target'],q),[])
            del u['query_id']
    def use(self,record,kind,query=None,relation=None,reason=None):
        self.uses.append({'effect_id':record['id'],'use':kind,'query_id':query,'relation_id':relation,'reason':reason})
    def export(self):
        used=defaultdict(list)
        for u in self.uses:used[u['effect_id']].append(u)
        return {'schema':'permission-equity-operation-dependencies-v20',
            'facts':[{'id':r['id'],'target':r['target'],'function':r['function'],'path_index':r['path_index'],
                'effect':{k:v for k,v in r['effect'].items() if k!='original_write'},
                'condition_digest':digest(r['conditions']),'uses':used.get(r['id'],[])} for r in self.records],
            'operation_summaries':self.operation_summaries,'semantic_bindings':self.semantic_edges,'stage_links':self.stage_links,
            'roles_are_not_inferred_from_shared_roots':True}
    def match_queries(self,checks):
        qmap=defaultdict(list)
        for q in checks:
            src=q.get('effect',{}).get('source') or q.get('source') or q.get('source_model',{}).get('effect',{}).get('source')
            qmap[q.get('target'),q.get('function'),key(src)].append(q)
        for r in self.records:
            qs=qmap.get((r['target'],r['function'],key(r['effect'].get('source'))),[])
            qs=[q for q in qs if q.get('path_index',q.get('source_model',{}).get('path_index'))==r['path_index'] or
                ('path_index' not in q and 'path_index' not in q.get('source_model',{}) and key(q.get('conditions'))==key(r['conditions']))]
            for q in qs:self.use(r,'compiled_check',q.get('id'),reason=q.get('status'))
            if not qs:self.use(r,'no_qualified_risk_query',reason='source_effect_inventory_is_not_a_risk_claim; inspect local restrictions')
