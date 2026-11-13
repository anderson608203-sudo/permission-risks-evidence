"""Program relationship graph used to derive permission queries.

NetworkX graph edges carry source anchors, selectors and path conditions.
Consumers traverse management/use/data relations, not example or symbol names.
"""
import copy
import networkx as nx
from .core import digest
from .m03_p_paths import key,walk,op,lit,normalize

SENDER={'kind':'actual_sender'}

class Relations:
    def __init__(self,lookup,program):
        from .m03_p_route import permission_atoms,selectors
        self.lookup=lookup;self.program=program;self.graph=nx.MultiDiGraph();self.writes=[];self.uses=[]
        for fn,paths in program.items():
            fid=self.node('function',{'signature':fn})
            for pi,path in enumerate(paths):
                if path['flow']=='reverted':continue
                for guard in path['guards']:
                    for selector in selectors(guard):self.edge(self.state(selector),fid,'guard_read',{'path_index':pi,'guard':guard,'source':path['entry_source']})
                    for atom in permission_atoms(guard,lookup,True):
                        for selector in selectors(atom):
                            self.uses.append({'function':fn,'selector':selector,'atom':atom,'path':path})
                            self.edge(self.state(selector),fid,'permission_use',{'path_index':pi,'predicate':atom,'source':path['entry_source']})
                for write in path['writes']:
                    self.writes.append({'function':fn,'path_index':pi,'path':path,'write':write})
                    sid=self.state(write['path']);self.edge(fid,sid,'writes',{'path_index':pi,'value':write['value'],'source':write['source']})
                    for selector in selectors(write['value']):self.edge(self.state(selector),sid,'assigned_from',{'function':fn,'source':write['source']})
        self.id=digest(self.export())
        from .m04_handoff_graph import discover
        self.handoffs=discover(lookup,program)

    def node(self,kind,value):
        n=digest({'kind':kind,'value':value});self.graph.add_node(n,kind=kind,value=copy.deepcopy(value));return n
    def state(self,selector,register=True):
        value={'root':selector['root'],'instance':selector.get('instance'),'fields':[s['field'] for s in selector.get('segments',[]) if 'field' in s],
               'selector_layout':[('field',s['field']) if 'field' in s else ('length',True) if s.get('length') else ('key',None) for s in selector.get('segments',[])]}
        return self.node('state_family',value) if register else digest({'kind':'state_family','value':value})
    def edge(self,a,b,relation,data):self.graph.add_edge(a,b,relation=relation,**copy.deepcopy(data))
    def writes_of(self,selector):
        sid=self.state(selector,False)
        if sid not in self.graph:return []
        fns={a for a,_,d in self.graph.in_edges(sid,data=True) if d['relation']=='writes'}
        return [w for w in self.writes if digest({'kind':'function','value':{'signature':w['function']}}) in fns and self.state(w['write']['path'],False)==sid]
    def export(self):
        return {'nodes':[{'id':n,**d} for n,d in sorted(self.graph.nodes(data=True))],
                'edges':sorted([{'from':a,'to':b,**d} for a,b,d in self.graph.edges(data=True)],key=key)}

    def queries(self,fn,path,write):
        from .m03_p_route import permission_atoms,selectors,keys,value_type,effective_permission
        tasks=[];effect=write['path'];effectkeys=keys(effect)
        def add(rule,required,relation,evidence):
            tasks.append({'rule':rule,'required':required,'relation':relation,'evidence':evidence,'graph_id':self.id})
        for handoff in self.handoffs:
            if fn==handoff['accept_function'] and write['source']==handoff['accept_source']:
                add('AC-02',handoff['required'],'nomination_to_actual_authority_transfer',handoff)
        # A source guard containing a managed role is not evidence that this
        # role is exclusive. Preserve the complete predicate, including legal
        # alternatives. Independent peer, subject and handoff duties remain.
        for guard in path['guards']:
            for atom in permission_atoms(guard,self.lookup):
                for s in selectors(atom):
                    managed=[w for w in self.writes_of(s) if not w['path']['issues'] and effective_permission(w['path']['guards'],self.lookup) and w['function']!=fn]
                    if managed and not effective_permission(path['guards'],self.lookup) and not any('field' in x for x in s.get('segments',[])) and normalize(guard)!=normalize(atom):
                        add('AC-01',guard,'managed_credential_used_in_action',{'use':path['entry_source'],'managers':[w['write']['source'] for w in managed],'visible_alternative_retained':guard,'role_atom':atom,'policy_scope':'complete_source_guard_not_exclusive_role','no_independent_exclusivity_evidence':True})
        # Compare management of the same credential family across single and
        # bulk entrypoints. Preserve qualifications inside OR alternatives.
        authority_uses=[u for u in self.uses if self.state(u['selector'],False)==self.state(effect,False)]
        # Consuming/clearing a pending credential is not an independent grant.
        # Its holder may legitimately differ from the party who issued it.
        def creates_authority(w):
            v=normalize(w['value'])
            return not (v.get('kind')=='literal' and (v.get('value') is False or v.get('value')==0))
        if authority_uses and creates_authority(write):
            from .m03_p_resource_relations import project_policy
            for peer in self.writes_of(effect):
                if peer['path']['issues'] or peer['function']==fn or not creates_authority(peer['write']):continue
                for policy in effective_permission(peer['path']['guards'],self.lookup):
                    try:required,relations=project_policy({'write':peer['write'],'function':peer['function'],'policy':policy},write,fn)
                    except ValueError:continue
                    add('AC-02',required,'credential_management_edges_to_same_family',{'manager':peer['write']['source'],'origin_function':peer['function'],'consumers':[u['path']['entry_source'] for u in authority_uses],'relations':relations})
            # A domain-limited role writing an unscoped credential drops the
            # issuing scope. Its own source manager supplies a candidate.
            for guard in path['guards']:
                for atom in permission_atoms(guard,self.lookup):
                    for s in selectors(atom):
                        scoped=[k for k in keys(s) if k!=SENDER and k.get('type') not in ('address','address payable')]
                        if not scoped or any(key(k) in {key(x) for x in effectkeys} for k in scoped):continue
                        for issuer in self.writes_of(s):
                            for policy in effective_permission(issuer['path']['guards'],self.lookup):
                                if any(x.get('kind')=='parameter' for x in walk(policy)):continue
                                add('AC-02',policy,'scoped_manager_writes_unscoped_authority',{'issuer':issuer['write']['source'],'consumer':write['source'],'dropped_scope':scoped})
        # Self-enrolment gives identity-specific entitlement, not authority over
        # arbitrary accounts. Any explicit delegation is handled separately.
        for guard in path['guards']:
            for atom in permission_atoms(guard,self.lookup):
                if atom.get('kind')!='storage' or keys(atom)!=[SENDER]:continue
                self_grants=[w for w in self.writes_of(atom) if keys(w['write']['path'])==[SENDER] and w['write']['value']==lit(True) and not w['path']['guards'] and not w['path']['issues']]
                if not self_grants:continue
                for k in effectkeys:
                    if k.get('type') not in ('address','address payable') and k!=SENDER:continue
                    add('AC-03',op('==',SENDER,k),'self_issued_credential_to_account_effect',{'issuers':[w['write']['source'] for w in self_grants],'action':write['source']})
        # A storage owner read for the same resource is not replaced by a
        # caller-supplied address. It is a candidate, retaining inferred policy.
        for guard in path['guards']:
            for selector in selectors(guard):
                if effective_permission(path['guards'],self.lookup):continue
                if value_type(selector,self.lookup) not in ('address','address payable') or not keys(selector):continue
                if key(keys(selector))!=key(effectkeys):continue
                if selector['root']==effect['root']:continue
                add('AC-03',op('==',SENDER,selector),'same_resource_owner_read_to_effect',{'owner_read':selector,'effect':effect,'source':write['source']})
        for guard in path['guards']:
            for term in walk(guard):
                if term.get('kind')=='op' and term.get('op')=='==':
                    for a,b in (term['args'],term['args'][::-1]):
                        if a.get('kind')=='transaction_origin' and b.get('kind')=='storage' and value_type(b,self.lookup) in ('address','address payable'):
                            add('AC-01',op('==',SENDER,b),'transaction_origin_is_not_immediate_caller',{'guard':term,'source':path['entry_source'],'scope':'calling context may contain an intermediary; no delegation inferred from origin alone'})
            for selector in selectors(guard):
                if value_type(selector,self.lookup)!='bool' or not selector.get('instance'):continue
                ks=keys(selector)
                if not ks:continue
                selected=ks[-1]
                if selected.get('kind')=='storage' and value_type(selected,self.lookup) in ('address','address payable'):
                    required=copy.deepcopy(selector);required['segments'][-1]={'key':SENDER}
                    add('AC-03',required,'external_credential_checks_state_identity_not_actor',{'observed':selector,'source':path['entry_source']})
                # Bind a domain-membership argument to the actual affected
                # resource's source-initialized scalar association.
                if len(ks)<2 or ks[-1]!=SENDER or not effectkeys:continue
                ctor=self.lookup.function('constructor');initializers=[]
                if ctor:
                    initializers=[x for x in walk(ctor.get('body',{})) if x.get('nodeType')=='Assignment' and x.get('leftHandSide',{}).get('nodeType')=='IndexAccess']
                associations={x['leftHandSide']['baseExpression'].get('referencedDeclaration') for x in initializers}
                choices=[]
                for root in associations:
                    decl=self.lookup.nodes.get(root,{});typ=decl.get('typeName',{})
                    if typ.get('nodeType')=='Mapping' and typ.get('keyType',{}).get('name')==effectkeys[0].get('type') and typ.get('valueType',{}).get('name')==ks[0].get('type') and root!=effect['root']:
                        choices.append({'kind':'storage','root':root,'segments':[{'key':effectkeys[0]}]})
                if len(choices)==1:
                    required=copy.deepcopy(selector);required['segments'][0]={'key':choices[0]}
                    add('AC-03',required,'resource_domain_association_to_external_membership',{'association':choices[0],'observed':selector,'source':path['entry_source']})
        # Controlled calls in another supplied contract + a configured scalar
        # authority give a callback boundary hypothesis. Direct public entry
        # is checked independently of the guarded wrapper's call path.
        entry=self.lookup.function(fn)
        if entry and not entry.get('generated_getter') and not effectkeys:
            incoming=[]
            for other in self.lookup.nodes.values():
                if other.get('nodeType')!='FunctionDefinition' or other.get('scope')==self.lookup.contract_node['id']:continue
                calls=[n for n in walk(other.get('body',{})) if n.get('nodeType')=='FunctionCall' and n.get('expression',{}).get('referencedDeclaration')==entry['id']]
                guards=[n for n in walk(other.get('body',{})) if n.get('nodeType')=='FunctionCall' and n.get('expression',{}).get('name') in ('require','assert')]
                if calls and guards:incoming.extend(self.lookup.anchor(c) for c in calls)
            if incoming and not effective_permission(path['guards'],self.lookup):
                ctor=self.lookup.function('constructor');configured=[]
                for n in walk(ctor.get('body',{}) if ctor else {}):
                    if n.get('nodeType')!='Assignment':continue
                    root=n.get('leftHandSide',{}).get('referencedDeclaration');decl=self.lookup.nodes.get(root,{})
                    if decl.get('stateVariable') and decl.get('typeName',{}).get('name') in ('address','address payable'):
                        configured.append({'kind':'storage','root':root,'segments':[]})
                if len(configured)==1:
                    add('AC-01',op('==',SENDER,configured[0]),'configured_callback_authority_with_controlled_incoming_call',{'configuration':self.lookup.anchor(ctor),'incoming_calls':incoming,'direct_entry':path['entry_source']})
        # Resource aliases inherit the live permission of the resource selected
        # by the alias. A cached owner is not automatically a current owner.
        for resource_key in effectkeys:
            if resource_key.get('kind')!='storage':continue
            for link in self.writes_of(resource_key):
                if link['path']['issues'] or link['write']['value'].get('kind')!='parameter':continue
                binding={key(link['write']['value']):resource_key}
                for left,right in zip(keys(link['write']['path']),keys(resource_key)):binding[key(left)]=right
                def substitute(v):
                    if isinstance(v,dict):
                        if key(v) in binding:return copy.deepcopy(binding[key(v)])
                        if v.get('kind')=='parameter':raise ValueError('alias_unbound_parameter')
                        return {k:substitute(x) for k,x in v.items()}
                    return [substitute(x) for x in v] if isinstance(v,list) else v
                for permission in effective_permission(link['path']['guards'],self.lookup):
                    if not any(key(link['write']['value'])==key(x) for x in walk(permission)):continue
                    try:required=substitute(permission)
                    except ValueError:continue
                    add('AC-03',required,'alias_creation_links_to_current_resource_permission',{'link':link['write']['source'],'selected_resource':resource_key,'permission_at_link':permission,'origin_function':link['function']})
        return list({key((x['rule'],x['required'])):x for x in tasks}.values())

def analyze_graph(bundle,lookup,program,requested,permission_queries=True):
    from .m03_p_route import structure
    from .m04_logic import check
    graph=Relations(lookup,program);rows=[];decisions=[]
    for fn,paths in (program.items() if permission_queries else []):
        for pi,path in enumerate(paths):
            if path['flow']=='reverted':continue
            for write in path['writes']:
                for task in graph.queries(fn,path,write):
                    if requested and not any(p.get('function')==fn and p.get('rule')==task['rule'] for p in requested):continue
                    result=check(lookup,path['guards'],task['required']) if not path['issues'] else {'status':'inconclusive','query':'not_called','reason':'source_path_incomplete'}
                    if any(x.get('kind') in ('unknown','call_unresolved') for x in walk(write['value'])):result={'status':'inconclusive','query':'not_called','reason':'effect_value_unresolved'}
                    condition=normalize(task['required']);selector=write['path'];synthetic=bundle.get('material_origin','compiler_artifacts')!='compiler_artifacts'
                    row={'schema':'m03-p-result-v2','route':'P','rule':task['rule'],'status':result['status'],
                         'reason':'graph_permission_violation' if result['status']=='supported' else 'graph_permission_implied' if result['status']=='refuted_in_scope' else result.get('reason','solver_unknown'),
                         'function':fn,'subject':'actual_sender','structure':structure(condition,lookup),
                         'program_id':bundle['program_id'],'build_id':bundle['build_id'],'policy_scope':'inferred_policy',
                         'required_policy_candidate':condition,'policy_basis':task,
                         'effect':{'object':lookup.nodes[selector['root']]['name'],'selector':selector,'value':write['value'],'operator':write['operator'],'source':write['source']},
                         'path_index':pi,'conditions':path['guards'],'issues':copy.deepcopy(path['issues']),
                         'execution_status':'not_run','solver_status':result.get('query','unknown'),'solver':result,'no_execution_required':True,
                         'reportable':result['status']=='supported' and not synthetic,'diagnostic_only':synthetic,
                         'material_origin':bundle.get('material_origin','compiler_artifacts'),'source_remarks':[],
                         'limitations':['inferred policy; alternate business intent is not excluded','source-path predicate satisfiability is not deployed transaction reachability'],
                         'coverage':'declared function/path/selector','not_a_safety_conclusion':True}
                    row['id']=digest({k:row[k] for k in ('program_id','build_id','rule','function','effect','conditions','required_policy_candidate')})
                    rows.append(row);decisions.append({'row':row['id'],'relation':task['relation'],'solver':result})
    return rows,{'schema':'program-relation-graph-v1','id':graph.id,**graph.export(),'consumer_decisions':decisions,'engine':'NetworkX MultiDiGraph'}
