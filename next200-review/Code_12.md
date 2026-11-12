# 源码文本 · 12

## source/src/pr_next_joint/investigation/goal_search.py

原文件 SHA-256 `8ab5379cf2f847295ba8c0037d13eb98daa9f647cceb8c29ab8ced087d75efd2`

````python
"""Bounded backward prerequisites and forward checked symbolic target states.

Search results contain the actual ordered frames, not a list of writer names.
All addresses remain separate symbolic inputs unless the source/request binds
them. A finite queue ending never certifies universal unreachability.
"""
from collections import deque
import copy
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key
from pr_next_joint.frontend.storage import selectors, selector_relation
from pr_next_joint.verification.sequence import read
from .summary import unique


def prerequisites(b, operation, goal=None):
    needed = []
    for _, path in b.f.operation_paths(operation):
        needed.extend(selectors([path['guards'], path.get('evaluated_terms', []),
                                 [w['value'] for w in path['writes']]]))
    needed.extend((goal or {}).get('positions', []))
    return unique(needed)


class TargetSearch:
    def __init__(self, backend, operation, goal=None, plan=None):
        self.b, self.operation = backend, operation
        self.goal, self.plan = goal or {}, plan or {}
        self.record = {'kind': 'target_state_search', 'operation': operation,
                       'goal': self.goal, 'plan': self.plan, 'candidates_executed': [],
                       'pruned': [], 'states': [], 'frontier': [], 'exhausted_is_not_unreachable': True,
                       'depth_limit': backend.f.options.prefix_depth,
                       'candidate_limit': backend.f.options.max_prefixes}
        backend.__dict__.setdefault('target_search_records',[]).append(self.record)

    def __iter__(self):
        b, oid, f = self.b, self.operation, self.b.f
        queue, queued, states = deque([()]), {()}, set()
        target = f.operations[oid]['target']
        goal_cells = prerequisites(b, oid, self.goal)
        # The closure identifies writers of prerequisites of other writers.
        # Ordering is established only by the subsequent source frames.
        closure = list(goal_cells)
        for _ in range(f.options.prefix_depth):
            writers = b.graph.writers(target, closure, 'goal-state backwards prerequisite')
            closure = unique(closure + [c for w in writers for c in prerequisites(b, w)])
        while queue and len(self.record['candidates_executed']) < f.options.max_prefixes:
            b.check()
            sequence = queue.popleft()
            result = b.reach(oid, sequence, plan=self.plan, goal=self.goal)
            self.record['candidates_executed'].append(result)
            # Expand and record the queue before yielding a target state. The
            # consumer may stop after this state, and must still retain the
            # other untried preparations rather than lose the generator tail.
            if len(sequence) >= f.options.prefix_depth:
                self.record['frontier'].append({'prefix': list(sequence), 'reason': 'depth_bound'})
            else:
                head = prerequisites(b, sequence[0]) if sequence else goal_cells
                before = b.graph.writers(target, head, 'first-frame source prerequisites')
                after = b.graph.writers(target, goal_cells, 'target source prerequisites')
                extensions = [((w,) + sequence,w) for w in before] + [(sequence + (w,),w) for w in after]
                for candidate,added in extensions:
                    if candidate in queued:continue
                    queued.add(candidate)
                    changed = [w['raw']['path'] for w in f.writes.values() if w['operation'] == added]
                    if not any(selector_relation(a, c) == 'same_shape' for a in changed for c in closure):
                        self.record['pruned'].append({'prefix': list(candidate), 'reason': 'no_write_to_prerequisite_closure'})
                        continue
                    queue.append(candidate)
            self.record['pending_prefixes'] = [list(s) for s in queue]
            for world in result.get('worlds', []):
                if not world.get('committed'):
                    continue
                frames = world.get('prefix_frames', [])
                writes = [w for fr in frames for w in fr['writes']]
                # Preserve guards, frame identities and complete keyed values.
                # Only exact equivalent symbolic states are pruned, never a
                # function merely because it has occurred earlier.
                signature = digest([f.identity, self.goal, self.plan,
                    [(c, read(c, writes, f.lookup(oid))) for c in closure],
                    [fr['guards'] for fr in frames], [fr['caller'] for fr in frames]])
                if signature in states:
                    self.record['pruned'].append({'prefix': list(sequence), 'reason': 'identical_typed_state_and_conditions'})
                    continue
                states.add(signature)
                reached = {'id': 'state_' + signature[:20], 'prefix': list(sequence),
                           'frames': copy.deepcopy(frames), 'writes': copy.deepcopy(writes),
                           'target_frame': copy.deepcopy(world['target_frame']),
                           'baseline_probe': world['query'], 'goal': copy.deepcopy(self.goal),
                           'plan': copy.deepcopy(self.plan), 'source_identity': f.identity,
                           'initial_prefix_policy': 'constructor_only_for_explicit_prefix'}
                self.record['states'].append(reached)
                yield reached
        self.record['frontier'] += [{'prefix': list(s), 'reason': 'candidate_bound'} for s in queue]
        self.record['search_complete_within_enumerated_scope'] = not queue
        self.record['unfound_is_not_unreachable'] = True


def search(b, oid, goal=None, plan=None, stop_on_first=True):
    searcher = TargetSearch(b, oid, goal, plan)
    for _ in searcher:
        if stop_on_first:
            searcher.record['stopped_on_target'] = True
            break
    r = searcher.record
    return dict(r, kind='prefix_search', reached_with_nonempty_prefix=any(s['prefix'] for s in r['states']),
                target_property=goal or {}, state_kind='source_checked_ordered_symbolic_target_states',
                providers=sorted({o for x in r['candidates_executed'] for o in x['prefix']}),
                excluded_unrelated_providers=r['pruned'], search_complete=False)

````

## source/src/pr_next_joint/investigation/graph.py

原文件 SHA-256 `f857ada0630f3e2f3af8d038e4acea5fe7170c7c2362ed84318dfd332384dd22`

````python
"""M1 neutral program graph, M2 hypotheses and M4 evidence in separate layers."""
import copy,collections,re,time
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import walk,key
from pr_next_joint.frontend.storage import selectors,selector_relation,keys
from .contracts import ident
from .request_scope import use_reads, unique_cells

class ProgramGraph:
    def __init__(self,facts):
        self.read_inputs={}
        self.facts=facts;self.nodes={};self.edges={};self.events=[];self.evidence_cache={};self.hypothesis_nodes={};self.ast_locators={}
        def ast_endpoint(target,ast_id,source=None):
            nid=ident('ast',[target,ast_id]);node=facts.lookups[target].nodes.get(ast_id)
            self.ast_locators[nid]={'target':target,'ast_id':ast_id,
                'source':facts.lookups[target].anchor(node) if node else source,
                'declaration_available':node is not None,'synthetic_or_external':node is None}
            return nid
        for target,lookup in facts.lookups.items():
            self.node(target,'contract',{'identity':target})
            for n in lookup.nodes.values():
                nid=ident('ast',[target,n.get('id')])
                if n.get('nodeType') in ('ContractDefinition','FunctionDefinition','ModifierDefinition','VariableDeclaration','EventDefinition','EmitStatement'):
                    self.node(nid,n['nodeType'],{'target':target,'ast_id':n['id'],'source':lookup.anchor(n)})
                if n.get('nodeType')=='ContractDefinition':
                    for base in n.get('linearizedBaseContracts',[])[1:]:self.edge(ast_endpoint(target,n['id']),ast_endpoint(target,base),'inherits')
        for oid,o in facts.operations.items():
            self.node(oid,'operation',o);self.edge(o['target'],oid,'entry')
            body=facts.lookup(oid).function(o['function'])
            if 'id' in body:self.edge(oid,ast_endpoint(o['target'],body['id'],o['source']),'entry_body')
            for n in walk(body):
                if n.get('nodeType')=='ModifierInvocation':self.edge(oid,ast_endpoint(o['target'],n.get('modifierName',{}).get('referencedDeclaration')),'modifier')
                if n.get('nodeType')=='FunctionCall':
                    decl=n.get('expression',{}).get('referencedDeclaration')
                    if type(decl)is int:self.edge(oid,ast_endpoint(o['target'],decl),'calls')
            for p in o['parameters']:
                nid=ident('parameter',[oid,p['ref']]);self.node(nid,'parameter',p);self.edge(oid,nid,'parameter');self.edge(nid,p['term'],'value_expression')
        for rid,r in facts.references.items():
            self.node(rid,'source_reference',r)
            self.edge(rid,ident('ast',[r['target'],r['ast_id']]),'binds_ast')
        for eid,e in facts.terms.items():self.node(eid,'expression',e)
        self.access=collections.defaultdict(lambda: {'writers':set(),'readers':set()})
        for pid,item in facts.paths.items():
            oid=item['operation'];raw=item['raw'];target=facts.operations[oid]['target']
            self.node(pid,'path',{'operation':oid,'flow':raw['flow'],'issues':raw.get('issues',[])})
            self.edge(oid,pid,'has_path')
            for g in raw['guards']:
                gid=ident('e',[target,g]);self.edge(gid,pid,'controls')
            for s in selectors(raw):
                sid=self.storage(target,s);self.edge(pid,sid,'reads');self.access[(target,s['root'])]['readers'].add(oid)
            for wid,w in facts.writes.items():
                if w['path']!=pid:continue
                self.node(wid,'state_effect',{'operation':oid,'path':pid,**w['raw']});self.edge(pid,wid,'commits')
                sid=self.storage(target,w['raw']['path']);self.edge(wid,sid,'writes')
                self.access[(target,w['raw']['path']['root'])]['writers'].add(oid)
                for s in selectors(w['raw']['value']):self.edge(self.storage(target,s),wid,'data_dependency')
            for eid,e in facts.effects.items():
                if e['path']==pid:self.node(eid,'external_effect',{'operation':oid,'path':pid,**e['raw']});self.edge(pid,eid,'external_effect')
            if raw.get('return_value') is not None:
                rid=ident('return',[pid,raw['return_value']]);self.node(rid,'return',{'expression':raw['return_value']});self.edge(pid,rid,'returns')
            for index,term in enumerate(raw.get('evaluated_terms',[])):
                tid=ident('eval',[pid,index]);self.node(tid,'evaluation',{'expression':term});self.edge(pid,tid,'evaluates')
        for (target,root),access in self.access.items():
            for a in access['writers']:
                for b in access['readers']:self.edge(a,b,'may_establish_use',{'target':target,'root':root,'may_alias_only':True})
        for i,g in enumerate(facts.gaps):
            nid=ident('gap',[i,g]);self.node(nid,'program_gap',g);self.edge(g['operation'],nid,'has_gap')
    def node(self,nid,kind,data,layer='program'):
        value={'id':nid,'kind':kind,'layer':layer,'data':copy.deepcopy(data)}
        if nid in self.nodes and self.nodes[nid]!=value:raise ValueError('graph_node_identity_conflict')
        self.nodes[nid]=value;return nid
    def edge(self,a,b,kind,data=None,layer='program'):
        row={'from':a,'to':b,'kind':kind,'layer':layer,'data':data or {}};eid=ident('edge',row);self.edges[eid]=row;return eid
    def storage(self,target,selector):
        nid=ident('object',[target,selector]);self.node(nid,'storage_object',{'target':target,'selector':selector})
        root=ident('ast',[target,selector['root']]);self.edge(nid,root,'storage_root')
        for i,s in enumerate(selector.get('segments',[])):
            kid=ident('selector',[target,selector,i]);self.node(kid,'storage_'+('key' if 'key' in s else 'length' if s.get('length') else 'field'),s);self.edge(nid,kid,'selector_position',{'position':i})
        return nid
    def writers(self,target,selectors_,reason):
        result=set()
        for s in selectors_:result.update(self.access.get((target,s['root']),{}).get('writers',set()))
        self.events.append({'action':'graph_writers','reason':reason,'roots':sorted({s['root'] for s in selectors_}),'operations':sorted(result),'binding_required':True})
        return sorted(result)
    def connected(self,oid,depth=2):
        seen={oid}
        for _ in range(depth):
            seen|={e['to'] for e in self.edges.values() if e['kind']=='may_establish_use' and e['from'] in seen}
            seen|={e['from'] for e in self.edges.values() if e['kind']=='may_establish_use' and e['to'] in seen}
        return sorted(seen)
    def neutral_frontier(self):
        """Index pre-answer source questions. A possible writer is not an authorized actor."""
        if hasattr(self, '_frontier'):
            return self._frontier
        f = self.facts
        writes = collections.defaultdict(list)
        for w in f.writes.values():
            path = w['raw']['path']
            writes[(f.operations[w['operation']]['target'], path['root'])].append(w)
        selected = []
        skipped = []
        # Spend a bounded number of candidate inspections per entry. Source access is independent.
        deadline=getattr(self,'frontier_deadline',time.monotonic()+f.options.seconds)
        for oid, operation in sorted(f.operations.items(), key=lambda x:(x[1]['target'],x[1]['source']['start'],x[0])):
            if time.monotonic()>=deadline:
                skipped.append({'entry':oid,'reason':'neutral_preselection_time_limit; source route open'})
                continue
            if operation['generated_getter']:
                continue
            target = operation['target']
            lookup = f.lookup(oid)
            best = None
            visits = 0
            for pid, path in f.operation_paths(oid, True):
                if not path['writes'] and not path.get('sensitive_effects'):
                    continue
                use = [('guard', s) for s in selectors(path['guards'])]
                use += [('effect_input', s) for s in selectors([w['value'] for w in path['writes']] + path.get('sensitive_effects', []))]
                seen = set()
                for kind, cell in use:
                    signature = kind, key(cell)
                    if signature in seen:
                        continue
                    seen.add(signature)
                    for row in writes.get((target, cell['root']), ()):
                        if visits >= f.options.max_actions:
                            break
                        visits += 1
                        writer = row['operation']
                        ws = row['raw']['path']
                        if writer == oid or selector_relation(ws, cell) != 'same_shape' or self._disjoint_keys(ws, cell):
                            continue
                        raw_writer = f.paths[row['path']]['raw']
                        if raw_writer['flow'] not in ('normal','returned') or raw_writer.get('issues') or raw_writer.get('evaluation_gaps'):
                            continue
                        actor = any(n.get('kind')=='actual_sender' for n in walk([path['guards'], cell, ws, raw_writer['guards']]))
                        rank = (not actor, kind!='guard', not bool(keys(cell)), f.operations[writer]['source']['start'], pid, writer)
                        if best is None or rank < best[0]:
                            best = rank, {'target':target,'writer':writer,'use':oid,'writer_path':row['path'],'use_path':pid,
                                'role_of_read':kind,'declaration':lookup.nodes[cell['root']].get('name'),
                                'ordered_write_key':ws,'ordered_read_key':cell,'write_source':row['raw']['source'],
                                'use_source':operation['source'],'sender_occurs':actor,'writer_guards':raw_writer['guards'],
                                'use_guards':path['guards'],'use_flow':path['flow'],
                                'effect_references':next(({'writes':c['writes'],'effects':c['effects']} for c in operation['paths'] if c['id']==pid),{}),
                                'stage':'possible earlier write then later use; no deployment reachability assertion',
                                'key_binding':'possible common storage position; caller and argument identities require investigation'}
                    if visits >= f.options.max_actions:
                        break
                if visits >= f.options.max_actions:
                    skipped.append({'entry':oid,'reason':'bounded_relation_enumeration'})
                    break
            if best:
                relation=best[1]
                cell=relation['ordered_read_key']
                related=[]
                for record in writes[(target,cell['root'])]:
                    s=record['raw']['path'];raw=f.paths[record['path']]['raw']
                    if raw['flow'] not in ('normal','returned') or raw.get('issues') or raw.get('evaluation_gaps'):
                        continue
                    if selector_relation(s,cell)=='same_shape' and not self._disjoint_keys(s,cell):
                        related.append({'operation':record['operation'],'path':record['path'],'ordered_key':s,
                                        'assigned':record['raw']['value'],'source':record['raw']['source']})
                    if len(related)>=f.options.max_actions:
                        skipped.append({'entry':oid,'reason':'related_write_index_bound'})
                        break
                relation['candidate_prior_writes']=related
                selected.append((best[0],relation))
            else:
                skipped.append({'entry':oid,'reason':'no_supported_cross_entry_meeting; source route open'})
        selected.sort(key=lambda x:(x[0],x[1]['target'],x[1]['use']))
        self._frontier = {'primary':selected[0][1] if selected else None,
                          'relations':[row for _,row in selected], 'limits':skipped,
                          'open_source_entries':sorted(f.operations), 'program_gaps':f.gaps,
                          'meaning':'neutral source relationships; no assertion of entitlement, policy or risk'}
        return self._frontier

    def closure_operations(self,oid,cells):
        """Include other original writers on the same possible key (grants, redemptions, alternative uses)."""
        target=self.facts.operations[oid]['target']
        by_operation={w for s in cells for w in self.access[(target,s['root'])]['writers']}
        return sorted({w['operation'] for w in self.facts.writes.values() if w['operation'] in by_operation
                       and any(selector_relation(s,w['raw']['path'])=='same_shape' and not self._disjoint_keys(s,w['raw']['path']) for s in cells)})

    def request_reads(self, oid):
        if oid not in self.read_inputs:
            self.read_inputs[oid] = unique_cells(cell for _, path in self.facts.operation_paths(oid, True)
                                                 for cell in use_reads(path))
        return self.read_inputs[oid]

    def investigation(self,oid,item,binding):
        """Compile one semantic uncertainty to a small source-grounded plan.

        Matching source names selects dependencies, never a business category.
        Omitted neighbors remain recorded possibilities, not refuted risks.
        """
        f=self.facts;o=f.operations[oid];lookup=f.lookup(oid);hint=item.get('next_check',{})
        hint=hint if isinstance(hint,dict) else {}
        question=item.get('distinguish',item.get('distinguishing_question',hint.get('question','')))
        if isinstance(question,dict):question=question.get('question','')
        text=' '.join(x for x in (item.get('claim'),item.get('alternative'),question) if isinstance(x,str))
        tokens=set(re.findall(r'[A-Za-z_$][\w$]*',text))
        guards=[s for _,p in f.operation_paths(oid) for s in selectors(p['guards'])]
        writes=[w['raw']['path'] for w in f.writes.values() if w['operation']==oid]
        named=[s for s in guards+writes if lookup.nodes.get(s['root'],{}).get('name') in tokens]
        focus=named or guards or writes
        focus=list({key(s):s for s in focus}.values())
        refs=set(binding.get('operations',[]));candidates=[]
        for other,op in f.operations.items():
            if other==oid or op['target']!=o['target']:continue
            ow=[w['raw']['path'] for w in f.writes.values() if w['operation']==other]
            og=self.request_reads(other)
            for change,observe,left,right in ((other,oid,ow,focus),(oid,other,writes,og)):
                shared=[s for s in left if any(selector_relation(s,t)=='same_shape' and not self._disjoint_keys(s,t) for t in right)]
                if not shared:continue
                # Explicit source names/anchors dominate possible root neighbors.
                explicit=other in refs or op['function'].split('(')[0] in tokens
                exact=any(key(s)==key(t) for s in shared for t in right)
                candidates.append({'change':change,'observe':observe,'controls':shared,
                  'rank':[0 if explicit else 1,0 if exact else 1,len(keys(shared[0])),
                          f.operations[change]['source']['start'],f.operations[observe]['source']['start']],
                  'source_reason':'explicit source relation' if explicit else 'matching ordered object in request guard, value, key or call'})
        candidates.sort(key=lambda x:x['rank']);unique={}
        for p in candidates:unique.setdefault((p['change'],p['observe']),p)
        candidates=list(unique.values());selected=candidates[:1]
        plan={'question':question or ('Which source-bound grant/control explains this effect, and does the related normal explanation apply?'),
          'risk_explanation':item['claim'],'normal_explanation':item.get('alternative'),
          'effect_root':oid,'focus_selectors':focus,'selected_pairs':selected,'deferred_pairs':candidates[1:],
          'selection_policy':'source relevance -> exact object shape -> cost; no confidence, Gold or expected score',
          'role_and_request_hints':{k:copy.deepcopy(hint[k]) for k in ('caller_mode','request_bindings') if k in hint}}
        self.events.append({'action':'question_guided_selection','operation':oid,'question':plan['question'],
            'selected':selected,'deferred_count':len(plan['deferred_pairs']),'focus':focus})
        return plan
    @staticmethod
    def _disjoint_keys(a,b):
        aa,bb=keys(a),keys(b)
        if len(aa)!=len(bb):return True
        return any(x.get('kind')==y.get('kind')=='literal' and x.get('value')!=y.get('value') for x,y in zip(aa,bb))
    def evidence(self,qid,record):
        # Store each immutable evidence entity once; graph edges carry its exact
        # scope. The separate evidence store owns formula/world payloads.
        identity=record.get('entity_sha256',digest(record));nid='evidence:'+identity
        card={k:copy.deepcopy(v) for k,v in record.items() if k not in ('worlds','queries','source_card','writer_cards','actual_guards','writes','effects')}
        card={k:v for k,v in card.items() if k not in ('id','question','semantic_version','action')}
        self.node(nid,'behavior_evidence',card,'evidence');self.edge(qid,nid,'supported_or_refuted_by',{'scope':record.get('evidence_scope',{})},layer='evidence')
        for field in ('operation','change','observe'):
            oid=record.get(field)
            if oid in self.facts.operations:self.edge(oid,nid,'evidence_source_operation',layer='evidence')
        def frames(value):
            if isinstance(value,dict):
                if 'operation' in value and 'slot' in value and ('committed_writes' in value or 'writes' in value):yield value
                for v in value.values():yield from frames(v)
            elif isinstance(value,list):
                for v in value:yield from frames(v)
        for fr in frames(record.get('worlds',{})):
            wid=ident('world',fr);self.node(wid,'execution_state_frame',{'sha256':digest(fr),'operation':fr['operation'],'path':fr['path'],'slot':fr['slot'],'full_frame_in':'evidence.json'},'evidence');self.edge(nid,wid,'uses_state_version',layer='evidence');self.edge(fr['operation'],wid,'source_operation_world',layer='evidence')
        return nid
    def record(self):return {'nodes':list(self.nodes.values()),'edges':list(self.edges.values()),'investigation_log':self.events,'semantics_are_not_program_facts':True}

````

## source/src/pr_next_joint/investigation/initial_state.py

原文件 SHA-256 `4a7fb9497b142a11b110ed190ecffc694ed4356990c35a00339d9c4e296318ac`

````python
"""Host-owned initial-state domains, constructor provenance and reachable writers.

This is a source transition summary, not a claim that an abstract state has been
deployed.  Every target freezes its numerical mapping candidates before M2.
"""
import copy
import re
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key, lit, walk
from pr_next_joint.frontend.storage import keys, selectors, fields, value_type
from pr_next_joint.frontend.source_entry_identity import function_kind
from pr_next_joint.frontend.program_paths import MechanismPaths

CAPABILITY = 'fcr_conditional_capability_r1'
DEPLOYMENT = 'solidity_deployment_r1'
AC_DOMAIN = 'ac_checked_prestate_r1'


def domain(lookup):
    return getattr(lookup, 'state_domain_override', None) or (CAPABILITY if getattr(lookup, 'analysis_scope', None) == 'FCR' else AC_DOMAIN)


def family(cell):
    return key({'root': cell['root'], 'segments': [{'key': '*'} if 'key' in s else s for s in cell.get('segments', [])]})


def reachable_functions(facts, target):
    """Resolve runtime roots first. Uncalled private/internal bodies are not writers."""
    lookup = facts.lookups[target]
    roots = [lookup.function(o['function']) for o in facts.operations.values() if o['target'] == target and not o.get('generated_getter')]
    pending = [n for n in roots if n]; found = {}; unresolved = []
    while pending:
        fn = pending.pop()
        if fn.get('id') in found: continue
        found[fn['id']] = fn
        for n in walk(fn):
            expr = n.get('modifierName') if n.get('nodeType') == 'ModifierInvocation' else n.get('expression') if n.get('nodeType') == 'FunctionCall' else None
            if not expr: continue
            ref = expr.get('referencedDeclaration'); callee = lookup.nodes.get(ref, {})
            if callee.get('nodeType') in ('FunctionDefinition', 'ModifierDefinition'):
                # External typed calls do not execute in the caller's storage.
                if expr.get('nodeType') == 'MemberAccess' and expr.get('expression', {}).get('typeDescriptions', {}).get('typeString', '').startswith('contract '):
                    continue
                if callee.get('body'): pending.append(callee)
                else: unresolved.append({'source': lookup.anchor(n), 'reason': 'runtime_callee_body_missing'})
    return found, unresolved


def assigned_roots(node, lookup):
    if not isinstance(node, dict):
        return set()
    typ = node.get('nodeType')
    if typ == 'Identifier':
        rid = node.get('referencedDeclaration')
        return {rid} if lookup.nodes.get(rid, {}).get('stateVariable') else set()
    if typ in ('IndexAccess', 'IndexRangeAccess'):
        return assigned_roots(node.get('baseExpression'), lookup)
    if typ == 'MemberAccess':
        return assigned_roots(node.get('expression'), lookup)
    if typ == 'TupleExpression':
        return set().union(*(assigned_roots(x, lookup) for x in node.get('components', [])))
    return set()


def runtime_writers(facts, target):
    lookup = facts.lookups[target]
    functions, gaps = reachable_functions(facts, target)
    sites = {}; opaque = []
    for fn in functions.values():
        for n in walk(fn.get('body') or {}):
            lhs = n.get('leftHandSide') if n.get('nodeType') == 'Assignment' else n.get('subExpression') if n.get('nodeType') == 'UnaryOperation' and n.get('operator') in ('delete', '++', '--') else None
            if lhs:
                for rid in assigned_roots(lhs, lookup):
                    sites.setdefault(rid, set()).add(n['id'])
            if n.get('nodeType') == 'InlineAssembly' and any(w in str(n).lower() for w in ('sstore', 'delegatecall', 'callcode')) or n.get('memberName') in ('delegatecall', 'callcode'):
                opaque.append(lookup.anchor(n))
    paths = {}
    for oid, operation in facts.operations.items():
        if operation['target'] != target: continue
        for pid, p in facts.operation_paths(oid):
            for w in p['writes']:
                if w['path'].get('instance'): continue
                # Exact IR roots include supported local storage references.
                # Index expressions remain reads, never declaration writes.
                if w.get('source', {}).get('ast_id') is not None:
                    sites.setdefault(w['path']['root'], set()).add(w['source']['ast_id'])
                paths.setdefault(w['path']['root'], []).append({'operation': oid, 'path': pid,
                    'source': w['source'], 'flow': p['flow'], 'value': w['value'], 'cell': w['path'],
                    'complete': p['flow'] in ('normal', 'returned') and not p.get('issues') and not p.get('evaluation_gaps')})
    return {'functions': sorted(functions), 'sites': {r: sorted(v) for r, v in sites.items()},
            'paths': paths, 'opaque_storage_writes': opaque, 'unresolved_calls': gaps}


def amount_candidates(facts, target):
    """Structural eligibility only: no token names, model decisions or risk labels."""
    result = {}
    def add(cell, oid, pid, reason):
        typ = value_type(cell, facts.lookup(oid))
        if keys(cell) and re.fullmatch(r'u?int\d*', typ or ''):
            result.setdefault(family(cell), {'cell': cell, 'type': typ, 'basis': []})['basis'].append(
                {'operation': oid, 'path': pid, 'reason': reason})
    for oid, operation in facts.operations.items():
        if operation['target'] != target: continue
        for pid, p in facts.operation_paths(oid, True):
            moves = []
            for w in p['writes']:
                cell, value = w['path'], w['value']; args = value.get('args', [])
                if value.get('op') in ('+', '-') and len(args) == 2 and any(key(cell) == key(s) for s in selectors(args[0])):
                    moves.append((w, value['op'], args[1]))
            ledger = []
            for w, sign, amount in moves:
                cell = w['path']
                if len(keys(cell)) != 1: continue
                conserved = any(other['path']['root'] == cell['root'] and family(other['path']) == family(cell)
                    and other_sign != sign and key(other_amount) == key(amount) for other, other_sign, other_amount in moves)
                supply = any(not keys(other['path']) and other_sign == sign and key(other_amount) == key(amount)
                    for other, other_sign, other_amount in moves)
                asset = any(any(key(amount) == key(n) for n in walk(effect)) for effect in p.get('sensitive_effects', []))
                native = any(n.get('kind') == 'transaction_value' for n in walk(amount))
                if conserved or supply or asset or native:
                    add(cell, oid, pid, 'same_quantity_account_flow' if conserved else 'supply_or_asset_linked_account_flow')
                    ledger.append((cell, amount))
            # Holder->spender quantities checked/consumed with an actual account debit.
            # Eligibility is not proof that the holder consented.
            for w, sign, amount in moves:
                if ledger and len(keys(w['path'])) >= 2 and any(key(amount) == key(a) for _, a in ledger):
                    add(w['path'], oid, pid, 'account_flow_related_numeric_grant')
    return [result[k] for k in sorted(result)]


def _constructor_paths(facts, target):
    original = facts.lookups[target]
    lookup = MechanismPaths(facts.bundle, original.contract, facts.options.max_paths)
    lookup.analysis_scope = facts.options.scope
    order = list(reversed(lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']])))
    constructors = {cid: next((n for n in lookup.nodes[cid].get('nodes', []) if n.get('nodeType') == 'FunctionDefinition' and function_kind(n) == 'constructor'), None) for cid in order}
    states = [{'env': {}, 'guards': [], 'writes': [], 'issues': [], 'flow': 'normal', 'evaluated_terms': []}]
    params = {}; derived = constructors[order[-1]]
    if derived:
        params.update({p['id']: {'kind': 'parameter', 'id': p['id'], 'type': p.get('typeDescriptions', {}).get('typeString'), 'constructor_parameter': True}
                       for p in derived.get('parameters', {}).get('parameters', [])})
    errors = []
    # Base arguments are compiler-resolved expressions in the declaring constructor's parameters.
    for cid in reversed(order):
        node = lookup.nodes[cid]; ctor = constructors[cid]
        specs = [(b.get('baseName', {}).get('referencedDeclaration'), b.get('arguments')) for b in node.get('baseContracts', [])]
        if ctor: specs += [(m['modifierName'].get('referencedDeclaration'), m.get('arguments')) for m in ctor.get('modifiers', [])]
        for bid, expressions in specs:
            if bid not in constructors or expressions is None: continue
            base = constructors[bid]; expected = (base or {}).get('parameters', {}).get('parameters', [])
            state = {'env': copy.deepcopy(params), 'guards': [], 'writes': [], 'issues': [], 'flow': 'normal'}
            try:
                lookup.current = state; lookup.source_evaluation_steps = 0
                values = [lookup.expr(a, state) for a in expressions]
                if state['writes'] or state['issues'] or len(values) != len(expected): raise ValueError('base_constructor_argument_effect_or_binding')
                params.update({p['id']: v for p, v in zip(expected, values)})
            except (ValueError, KeyError, TypeError, NotImplementedError) as ex:
                errors.append({'contract': bid, 'reason': str(ex), 'scope': 'constructor_arguments'})
    for cid in order:
        ctor = constructors[cid]; node = lookup.nodes[cid]
        # Solidity initializes each base's declarations immediately before that base body.
        lookup.source_evaluation_steps = 0; lookup.read_calls.summaries = {}; lookup.unknown = []
        lookup.source_execution_context = {'kind': 'constructor', 'entry_ast_id': (ctor or {}).get('id'), 'basis': 'compiled_linearized_constructor_order'}
        for state in states:
            if state['flow'] not in ('normal', 'returned'): continue
            state['flow'] = 'normal'; state['env'] = copy.deepcopy(params)
            for var in node.get('nodes', []):
                if not var.get('stateVariable') or var.get('value') is None: continue
                try:
                    value = lookup.expr(var['value'], state)
                    state['writes'].append({'path': {'kind': 'storage', 'root': var['id'], 'segments': []},
                        'value': value, 'operator': '=', 'source': lookup.anchor(var)})
                except (ValueError, KeyError, TypeError, NotImplementedError) as ex:
                    state['issues'].append({'reason': str(ex), 'declaration': var['id'], 'source': lookup.anchor(var)})
        if not ctor: continue
        clone = copy.deepcopy(ctor)
        clone['modifiers'] = [m for m in clone.get('modifiers', []) if lookup.nodes.get(m['modifierName'].get('referencedDeclaration'), {}).get('nodeType') != 'ContractDefinition']
        expected = ctor.get('parameters', {}).get('parameters', [])
        if any(p['id'] not in params for p in expected):
            errors.append({'contract': cid, 'reason': 'base_constructor_parameter_not_bound', 'scope': 'constructor_arguments'})
            continue
        out = []
        for state in states:
            if state['flow'] not in ('normal', 'returned'): out.append(state); continue
            state['flow'] = 'normal'
            try:
                out.extend(lookup.invoke(clone, [copy.deepcopy(params[p['id']]) for p in expected], state))
            except (ValueError, KeyError, TypeError, NotImplementedError) as ex:
                state['issues'].append({'reason': str(ex), 'source': lookup.anchor(ctor)}); out.append(state)
        states = out[:facts.options.max_paths]
        if len(out) > len(states): errors.append({'reason': 'constructor_path_frontier_bound_exceeded'})
    for state in states:
        state.pop('env', None)
        state['issues'].extend(copy.deepcopy(errors))
    return states, params


def model(facts, target):
    cache = facts.__dict__.setdefault('_initial_states', {})
    if target in cache: return cache[target]
    lookup = facts.lookups[target]
    bases = lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']])
    declarations = {n['id']: n for c in bases for n in lookup.nodes[c].get('nodes', []) if n.get('stateVariable')}
    candidates = amount_candidates(facts, target)
    writers = runtime_writers(facts, target)
    try: paths, parameters = _constructor_paths(facts, target)
    except (ValueError, KeyError, TypeError, NotImplementedError) as ex:
        paths = [{'flow': 'unknown', 'guards': [], 'writes': [], 'issues': [{'reason': str(ex)}]}]; parameters = {}
    rows = {}
    for rid, var in declarations.items():
        typ = var.get('typeDescriptions', {}).get('typeString', '')
        assigned = [w for p in paths for w in p['writes'] if w['path']['root'] == rid]
        # Unknown explicit writes remain explicit: never introduce a replacement abstract role.
        explicit_ctor_sites = [n['id'] for cid in bases for fn in lookup.nodes[cid].get('nodes', []) if fn.get('nodeType') == 'FunctionDefinition' and function_kind(fn) == 'constructor'
            for n in walk(fn.get('body') or {}) if n.get('nodeType') == 'Assignment' and rid in assigned_roots(n.get('leftHandSide', {}), lookup)]
        rows[rid] = {'declaration': rid, 'name': var.get('name'), 'type': typ, 'source': lookup.anchor(var),
            'explicit_initializer': var.get('value') is not None, 'constructor_writes': assigned,
            'explicit_constructor_sites': explicit_ctor_sites, 'runtime_sites': writers['sites'].get(rid, []),
            'runtime_paths': writers['paths'].get(rid, []), 'constant': bool(var.get('constant')),
            'immutable': var.get('mutability') == 'immutable'}
    value = {'schema': 'source_initial_states_r1', 'target': target, 'declarations': rows,
        'candidate_amount_leaves': candidates, 'constructor_paths': paths, 'constructor_parameters': parameters,
        'runtime_writers': writers, 'source_default_rule': 'typed_default_except_explicit_FCR_symbolic_scalar_or_frozen_amount_leaf',
        'domains': [CAPABILITY, DEPLOYMENT], 'exact_author_runtime_state_verified': False}
    value['identity'] = digest(value); cache[target] = value
    return value


def initial_for_lookup(lookup):
    facts = getattr(lookup, '_investigation_facts', None)
    if facts is None: return None
    return model(facts, lookup.contract['file'] + ':' + lookup.contract['name'])


def receipt(lookup):
    value = initial_for_lookup(lookup)
    return {'analysis_domain': domain(lookup), 'initial_model_identity': value['identity'] if value else None,
        'candidate_amount_leaves': value['candidate_amount_leaves'] if value else [],
        'abstract_capability_is_not_deployment': domain(lookup) == CAPABILITY}

````

## source/src/pr_next_joint/investigation/key_roles.py

原文件 SHA-256 `a28f2815de6845d21454c935f44ede46e27da17c4a08a2fce9bab9047f7ff49c`

````python
"""Finite key-role relations derived from source transfers and allowance uses.

Names and key order are not evidence. Ambiguous families retain their residual.
These records annotate positions; they do not change the state interpreter.
"""
import re
from pr_next_joint.frontend.path_ir import key
from pr_next_joint.frontend.storage import keys, selectors, selector_relation, value_type
from .initial_state import family


def derive(f):
    proposals={}
    for oid,o in f.operations.items():
        lookup=f.lookup(oid)
        for pid,p in f.operation_paths(oid,True):
            if p.get('issues') or p.get('evaluation_gaps'):continue
            writes=p['writes'];debits=[];credits=[]
            for w in writes:
                v=w['value'];a=v.get('args',[]);cell=w['path']
                if not re.fullmatch(r'u?int\d*',value_type(cell,lookup) or ''):continue
                from .summary import local_delta
                sign,amount=local_delta(w)
                if sign in ('-','+'):(debits if sign=='-' else credits).append((cell,amount))
            for cell,amount in debits:
                idx=keys(cell)
                if len(idx)<2:continue
                token=(o['target'],family(cell))
                for dst,add in credits:
                    if selector_relation(cell,dst)!='same_shape' or key(amount)!=key(add):continue
                    ds=keys(dst);different=[i for i,(a,b) in enumerate(zip(idx,ds)) if key(a)!=key(b)]
                    if len(different)!=1:continue
                    h=different[0]
                    if idx[h].get('kind')=='actual_sender' and ds[h].get('type') in ('address','address payable'):
                        proposals.setdefault(token,[]).append({'holder_key':h,'kind':'asset_position',
                            'basis':'same_asset_self_debit_and_recipient_credit','operation':oid,'path':pid})
                for asset,spent in debits:
                    aks=keys(asset)
                    if len(aks)!=1 or len(idx)!=2 or key(amount)!=key(spent):continue
                    matches=[i for i,k in enumerate(idx) if key(k)==key(aks[0])]
                    if len(matches)!=1 or idx[1-matches[0]].get('kind')!='actual_sender':continue
                    if not any(selector_relation(cell,c)=='same_shape' and key(c)==key(cell) for c in selectors(p['guards'])):continue
                    h=matches[0]
                    issuers=[w for w in f.writes.values() if f.operations[w['operation']]['target']==o['target'] and
                        selector_relation(w['raw']['path'],cell)=='same_shape' and len(keys(w['raw']['path']))==2 and
                        keys(w['raw']['path'])[h].get('kind')=='actual_sender' and w['raw']['value'].get('kind')=='parameter']
                    if issuers:
                        proposals.setdefault(token,[]).append({'holder_key':h,'kind':'authorization_quantity',
                            'basis':'same_amount_debit_and_caller_indexed_holder_grant','asset':asset,
                            'operation':oid,'path':pid,'issuers':[w['operation'] for w in issuers]})
    records=[]
    for target,lookup in f.lookups.items():lookup.source_key_roles={}
    for (target,fam),rows in proposals.items():
        meanings={(r['holder_key'],r['kind']) for r in rows}
        if len(meanings)!=1:continue
        h,kind=next(iter(meanings));record={'holder_key':h,'kind':kind,'origins':rows,'family':fam,'target':target}
        f.lookups[target].source_key_roles[fam]=record;records.append(record)
    return records


def relation(cell,lookup):
    return getattr(lookup,'source_key_roles',{}).get(family(cell))

````

## source/src/pr_next_joint/investigation/ledger.py

原文件 SHA-256 `306fc244efeeb6c99a620913ad3fa59ab92de2463416bf1b8a58403682d4fbe6`

````python
"""Bounded same-ledger measurements on committed original-source frames."""
from itertools import product
import re

from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, selector_relation, value_type
from pr_next_joint.verification.program_encoding import MechanismEncoder
from pr_next_joint.verification.sequence import qualify, read
from pr_next_joint.verification.source_worlds import frame, encode_frame
from pr_next_joint.verification.expressions import Unsupported

MEASURES = {
    'ledger_receipt': 'same_debit_recipient_receives_less',
    'ledger_debit': 'same_request_holder_debited_more',
    'ledger_grant': 'actual_debit_exceeds_effective_grant',
}


def unique(items):
    return list({key(x): x for x in items}.values())


def movements(backend, oid, path):
    from .summary import get_summaries
    return get_summaries(backend.f).movements(oid,path)


def legacy_movements(backend, oid, path):
    lookup = backend.f.lookup(oid)
    result = {'-': [], '+': []}
    for w in path['writes']:
        cell, expr = w['path'], w['value']
        args = expr.get('args', [])
        sign = expr.get('op')
        if sign not in result or len(args) != 2 or not value_type(cell, lookup).startswith('uint'):
            continue
        indices = keys(cell)
        if len(indices) != 1 or indices[0].get('kind') not in ('actual_sender', 'parameter'):
            continue
        account = indices[0]
        if account.get('kind') == 'parameter' and account.get('type') not in ('address', 'address payable'):
            continue
        candidates = args[:1] if sign == '-' else args
        if any(key(s) == key(cell) for a in candidates for s in selectors(a)):
            result[sign].append(cell)
    return {sign: unique(cells) for sign, cells in result.items()}


def same_increment(write,cell):
    v=write['value']; args=v.get('args',[])
    return selector_relation(write['path'],cell)=='same_shape' and v.get('op')=='+' and len(args)==2 and key(args[0])==key(write['path'])


def unit_origin(backend, oid, cell):
    from .initial_state import family
    from .key_roles import relation
    if (relation(cell,backend.f.lookup(oid)) or {}).get('kind')=='authorization_quantity':return None
    cache=backend.__dict__.setdefault('_unit_origin_cache',{})
    semantics=getattr(backend,'semantics',None)
    bound=semantics.lookup(oid,cell) if semantics else None
    if bound:
        if bound['meaning']=='financial_right':
            # A field participating in a source clock comparison is not an
            # asset quantity merely because the surrounding claim says token.
            # Independent source asset flow can establish a dual use; without
            # it the semantic/source type conflict stays an explicit obligation.
            temporal=[]
            target=backend.f.operations[oid]['target']
            clock_cache=backend.__dict__.setdefault('_clock_position_cache',{})
            ck=(target,family(cell))
            if ck not in clock_cache:
                for other,o in backend.f.operations.items():
                    if o['target']!=target:continue
                    for pid,p in backend.f.operation_paths(other):
                        for g in walk(p['guards']):
                            if g.get('op') not in ('<','<=','>','>=','==','!='):continue
                            if (any(selector_relation(s,cell)=='same_shape' for s in selectors(g)) and
                                any(n.get('kind') in ('block_timestamp','block_number') or
                                    n.get('kind')=='environment' and n.get('field') in ('timestamp','number') for n in walk(g))):
                                temporal.append({'operation':other,'path':pid,'comparison':g})
                clock_cache[ck]=temporal
            temporal=clock_cache[ck]
            physical_key=(oid,family(cell))
            if temporal and physical_key not in cache:cache[physical_key]=_unit_origin(backend,oid,cell)
            if temporal and not cache[physical_key]:
                backend.__dict__.setdefault('unit_conflicts',{})[ck]={'cell':cell,'source_clock_comparisons':temporal,
                    'semantic_binding':bound['id'],'reason':'semantic amount not independently bound against source time dimension'}
                return None
            return {'kind':'source_bound_semantic_unit','binding':bound}
        original=_unit_origin(backend,oid,cell)
        return dict(original,semantic_conflict=bound) if original else None
    token=(oid,family(cell))
    if token not in cache:cache[token]=_unit_origin(backend,oid,cell)
    return cache[token]


def native_only_position(backend,oid,cell):
    if not backend._native_unit_source(oid,cell):return False
    semantics=getattr(backend,'semantics',None)
    binding=semantics.lookup(oid,cell) if semantics else None
    if binding and binding['meaning']=='financial_right' and (binding.get('semantic_assertion') or {}).get('unit_kind')=='token':return False
    cache=backend.__dict__.setdefault('_token_unit_source_cache',{})
    from .initial_state import family
    token=(backend.f.operations[oid]['target'],family(cell))
    if token not in cache:cache[token]=_unit_origin(backend,oid,cell,include_native=False)
    return cache[token] is None


def _unit_origin(backend, oid, cell,include_native=True):
    origins = backend._native_unit_source(oid, cell)
    if origins and include_native:
        return {'kind': 'same_ledger_with_native_deposit_origin', 'origins': origins,'native_redemption_value_proved':False}
    # Issuance-only contracts can identify the token unit via its supply view and
    # the same issuance quantity on the selected holder ledger; no transfer transaction needed.
    facts=backend.f
    target=facts.operations[oid]['target']
    supplies=[(other,pid,p['return_value']) for other,o in facts.operations.items() if o['target']==target
              for pid,p in backend.paths(other) if (p.get('return_value') or {}).get('kind')=='storage' and not keys(p['return_value'])]
    for other,o in facts.operations.items():
        if o['target']!=target:continue
        node=facts.lookup(other).nodes.get(o['source'].get('ast_id'),{})
        if node.get('nodeType')=='VariableDeclaration' and node.get('stateVariable') and node.get('visibility')=='public' and node.get('typeDescriptions',{}).get('typeString','').startswith('uint'):
            supplies.append((other,'public_getter_ast_'+str(node['id']),{'kind':'storage','root':node['id'],'segments':[]}))
    for pid,p in backend.paths(oid):
        for w in p['writes']:
            v=w['value']; args=v.get('args',[])
            if not same_increment(w,cell):continue
            for other,getter,supply in supplies:
                if any(same_increment(sw,supply) and key(sw['value']['args'][1])==key(args[1]) for sw in p['writes']):
                    return {'kind':'source_supply_linked_token_unit','issuance_path':pid,'supply_getter':getter}
    # A public holder-balance query and a holder-initiated transfer of
    # this exact storage family corroborate a token interpretation. A name alone cannot.
    facts = backend.f
    target = facts.operations[oid]['target']
    getter, transfer = [], []
    for other, entry in facts.operations.items():
        if entry['target'] != target:
            continue
        # Query source, independent of the public ABI spelling.
        node=facts.lookup(other).nodes.get(entry['source'].get('ast_id'),{})
        if node.get('nodeType')=='VariableDeclaration' and node.get('visibility')=='public' and cell['root']==node['id']:
            getter.append('public_getter_ast_'+str(node['id']))
        for pid, p in backend.paths(other):
            returned = p.get('return_value') or {}
            if returned.get('kind') == 'storage' and selector_relation(cell, returned) == 'same_shape' and len(keys(returned)) == 1 and keys(returned)[0].get('kind') == 'parameter':
                getter.append(pid)
        for pid, p in backend.paths(other):
            changed = movements(backend, other, p)
            debits = [s for s in changed['-'] if selector_relation(s, cell) == 'same_shape' and keys(s) and keys(s)[0]['kind'] == 'actual_sender']
            credits = [s for s in changed['+'] if selector_relation(s, cell) == 'same_shape' and keys(s)[0]['kind'] == 'parameter']
            if (entry['function']=='transfer(address,uint256)' and debits and credits) or any(key(dw['value']['args'][1])==key(cw['value']['args'][1]) for d in debits for c in credits for dw in p['writes'] for cw in p['writes'] if key(dw['path'])==key(d) and key(cw['path'])==key(c) and len(dw['value'].get('args',[]))==2 and len(cw['value'].get('args',[]))==2):
                transfer.append(pid)
    if getter and transfer:
        return {'kind': 'source_token_ledger_unit', 'balance_query_paths': getter, 'holder_transfer_paths': transfer}
    return None


def grant_for(backend, oid, path, debit):
    """An on-path numeric allowance with its ordered, holder-issued source writer."""
    facts = backend.f
    from .summary import holder as bound_holder
    holder = bound_holder(debit,facts.lookup(oid))
    if holder is None:return None
    possible = []
    for guard in path['guards']:
        for node in walk(guard):
            args = node.get('args', [])
            if len(args) != 2:
                continue
            if node.get('op') in ('>=', '>'):
                cell = args[0]
            elif node.get('op') in ('<=', '<'):
                cell = args[1]
            else:
                continue
            idx = keys(cell) if cell.get('kind') == 'storage' else []
            if len(idx) != 2 or key(idx[0]) != key(holder) or idx[1].get('kind') != 'actual_sender':
                continue
            for w in facts.writes.values():
                other = w['operation']
                if facts.operations[other]['target'] != facts.operations[oid]['target']:
                    continue
                dst, val = w['raw']['path'], w['raw']['value']
                writer = facts.paths[w['path']]['raw']
                if (selector_relation(dst, cell) == 'same_shape' and len(keys(dst)) == 2
                        and keys(dst)[0].get('kind') == 'actual_sender' and keys(dst)[1].get('kind') == 'parameter'
                        and val.get('kind') == 'parameter' and writer['flow'] in ('normal', 'returned')
                        and not writer.get('issues') and not writer.get('evaluation_gaps')):
                    possible.append(cell)
                    break
    cells = unique(possible)
    return cells[0] if len(cells) == 1 else None


def bind_positions(backend, oid, item):
    found = {}
    for pid, p in backend.paths(oid):
        moves = movements(backend, oid, p)
        for debit, credit in product(moves['-'], moves['+']):
            if selector_relation(debit, credit) != 'same_shape':
                continue
            hint = item.get('observation')
            hint = hint if isinstance(hint, dict) else {}
            if any(hint.get(field) and hint[field] != backend._storage_name(oid, cell)
                   for field, cell in [('payer_key', debit), ('recipient_key', credit)]):
                continue
            found[key([debit, credit])] = (debit, credit)
    # A separate recipient parameter remains a separate source position even when its
    # concrete address aliases the payer; a same-expression credit is also measured as a refund.
    if len(found)>1:
        distinct={k:v for k,v in found.items() if key(v[0])!=key(v[1])}
        if len(distinct)==1:found=distinct
    if len(found) != 1:
        return None, 'payer_and_recipient_not_unique_in_one_ledger'
    debit, credit = next(iter(found.values()))
    origin = unit_origin(backend, oid, debit)
    if not origin:
        return None, 'financial_unit_not_source_supported'
    return {'debit': debit, 'credit': credit, 'origin': origin}, None


def flow(encoder, lookup, fr, cell):
    """Translate each already composed write once, including runtime address aliases."""
    z = encoder.z
    history = list(fr['before'])
    probe = qualify(cell, fr['slot'])
    # A parameter/caller key is unchanged during this request.
    from .summary import holder
    account=holder(probe,lookup)
    if account is None:raise Unsupported('ledger_holder_address_not_bound')
    address = encoder.expr(read(account, history, lookup))
    start = encoder.expr(read(probe, history, lookup))
    debits, credits = [], []
    for w in fr['writes']:
        dest = w['path']
        if selector_relation(dest, probe) == 'same_shape' and len(keys(dest)) == len(keys(probe)):
            same = z.And(*[encoder.expr(a)==encoder.expr(read(b,fr['before'],lookup)) for a,b in zip(keys(dest),keys(probe))])
            prior = encoder.expr(read(dest, history, lookup))
            value = encoder.expr(w['value'])
            debits.append(z.If(z.And(same, value < prior), prior - value, 0))
            credits.append(z.If(z.And(same, value > prior), value - prior, 0))
        history.append(w)
    end = encoder.expr(read(probe, history, lookup))
    return address, start, end, z.Sum(debits) if debits else z.IntVal(0), z.Sum(credits) if credits else z.IntVal(0)


def equal_to(e, value, literal):
    if type(literal) is bool and not e.z.is_bool(value) or type(literal) is int and not e.z.is_int(value):
        raise Unsupported('named_assumption_sort_mismatch')
    return value == literal


def scenario_terms(e, lookup, case, before, after, slot):
    terms = []
    for condition in case:
        history = before if condition['frame'] == 'before' else after
        cell = qualify(condition['cell'], slot)
        term = e.expr(read(cell, history, lookup))
        terms.append(equal_to(e, term, condition['value']))
    return terms


def compare_ledger(backend, change, use, context):
    from .behavior import ordered_clocks
    f = backend.f
    spec = context['observable']
    measure, cells = spec['measure'], spec['ledger']
    lookup = f.lookup(use)
    queries, rows, errors = [], [], []
    cases = context.get('premise_cases') or [[]]
    checked = 0
    truncated = False
    baseline_paths=[(None,None)] if measure=='ledger_grant' else backend.paths(use)
    for (cid, cp), (p0, a), (p1, b), case in product(backend.paths(change), baseline_paths, backend.paths(use), cases):
        backend.check()
        if checked >= f.options.max_prefixes:
            truncated = True
            break
        if cid not in spec['change_paths']:continue
        checked += 1
        try:
            if any(backend.condition_dependencies(o, i, p)[k] for o,i,p in ((change,cid,cp),(use,p0,a),(use,p1,b)) if p is not None
                   for k in ('unknown_dependencies','credential_dependencies')):
                raise Unsupported('critical_external_or_credential_on_selected_path')
            e = MechanismEncoder(lookup)
            z = e.z
            cf = frame(f, change, cid, 0)
            w1=frame(f,use,p1,1,cf['writes'])
            w0=frame(f,use,p0,1) if p0 is not None else None
            from .roles import path_qualification, fixed_role_terms
            role_terms, role_origins=fixed_role_terms(e,path_qualification(f,change,cp),0)
            source_constraints = [encode_frame(e,cf), encode_frame(e,w1),*role_terms]
            if measure != 'ledger_grant':
                source_constraints.append(encode_frame(e,w0))
            source_constraints += ordered_clocks(e,1)
            source_constraints.extend(e.expr(fr['caller']) != 0 for fr in (cf,w1))
            for arg in context.get('bindings',[]):
                source_constraints.append(e.expr(qualify(arg['parameter'],1)) == e.expr(arg['value']))
            source_constraints += scenario_terms(e,lookup,case,[],cf['writes'],1)
            for left,right,relation in context.get('request_aliases',[]):
                x,y = (e.expr(qualify(t,1)) for t in (left,right))
                source_constraints.append(x == y if relation == '==' else x != y)
            changed = []
            for control in spec['control_selectors']:
                pos = qualify(control,1)
                changed.append(e.expr(read(pos,[],lookup)) != e.expr(read(pos,cf['writes'],lookup)))
            source_constraints.append(z.Or(*changed))
            h, h1, end1, dr1, _ = flow(e,lookup,w1,cells['debit'])
            r, r1, rend1, _, cr1 = flow(e,lookup,w1,cells['credit'])
            source_constraints.append(h!=0)  # The investigated holder can submit/authorize a request.
            if measure!='ledger_grant':source_constraints.append(r!=0)  # A usable receipt, not a burn sink.
            original_h = e.expr(read(qualify(cells['debit'],1),[],lookup))
            original_r = e.expr(read(qualify(cells['credit'],1),[],lookup))
            values = {'holder':h,'recipient':r,'controller':e.expr(cf['caller']),'requester':e.expr(w1['caller']),
                      'gross_debit_after':dr1,'gross_credit_after':cr1,'request_holder_delta_after':end1-h1,
                      'request_recipient_delta_after':rend1-r1, 'intervention_holder_delta':h1-original_h,
                      'intervention_recipient_delta':r1-original_r,'combined_holder_delta':end1-original_h,
                      'combined_recipient_delta':rend1-original_r}
            if measure == 'ledger_grant':
                grant = grant_for(backend,use,b,cells['debit'])
                if not grant:
                    raise Unsupported('ordered_holder_issued_grant_not_bound_on_commit_path')
                effective = e.expr(read(qualify(grant,1),cf['writes'],lookup))
                source_constraints.extend([e.expr(w1['caller']) != h, dr1 > 0])
                violation = dr1 > effective
                values['effective_grant'] = effective
            else:
                h0, pre0, end0, dr0, _ = flow(e,lookup,w0,cells['debit'])
                r0, rpre0, rend0, _, cr0 = flow(e,lookup,w0,cells['credit'])
                source_constraints += [h==h0, r==r0, dr0>0, dr1>0]
                values.update(gross_debit_before=dr0,gross_credit_before=cr0,request_holder_delta_before=end0-pre0,
                              request_recipient_delta_before=rend0-rpre0)
                if measure == 'ledger_receipt':
                    source_constraints.append(dr0 == dr1)
                    violation = rend1-r1 < rend0-rpre0
                else:
                    violation = dr1 > dr0
            details = {'target':f.operations[use]['target'],'change':change,'observe':use,'change_path':cid,
                       'before_path':p0 if measure!='ledger_grant' else None,'after_path':p1,'unit':cells['origin'],
                       'encoded_writer_role_origins':role_origins,'payer_key':cells['debit'],'recipient_key':cells['credit'],'holder':keys(cells['debit'])[0],
                       'principal_scope':{'holder':'nonzero_authorizing_account','recipient':'unrestricted' if measure=='ledger_grant' else 'nonzero_usable_receiving_account','addresses_may_alias':True},
                       'encoded_case':case,'encoded_request_bindings':context['bindings'],'request_aliases':context.get('request_aliases',[]),
                       'source_assumptions':context.get('declared_assumptions',[]),'unencoded_text_is_not_a_premise':True,
                       'initial_state':'shared symbolic state; no deployment prefix asserted',
                       'scope':'identified ledger and submitted original path(s), no market valuation or universal consent inference'}
            base = z.And(*source_constraints)
            feasible = backend._query(e,base,'ledger_request_feasible',details)
            queries.append(feasible)
            if not feasible['validated_bounded_witness']:
                rows.append({'feasible_probe':feasible['id'],'state':'premise_'+feasible['answer'],'scope':details})
                continue
            result = backend._query(e,z.And(base,violation),MEASURES[measure],details,values)
            queries.append(result)
            rows.append({'feasible_probe':feasible['id'],'result_probe':result['id'],'state':result['answer'],
                         'values':result.get('observed_values',{}),'scope':details})
        except Unsupported as error:
            errors.append({'path':p1,'before':p0,'change':cid,'reason':str(error)})
    return {'kind':'causal_compare','observed_measure':measure,'change':change,'observe':use,'queries':queries,
            'ledger_measurements':rows,'comparisons':[],'worlds':[],'alternative_uses':[],'holder_consent_counterexamples':[],
            'local_errors':errors,'net_measurements':[],'net_pair_budget':{'pairs':checked,'truncated':truncated},
            'evidence_scope':{'target':f.operations[use]['target'],'controls':spec['control_selectors'],
                              'request_context':context,'unit_origin':cells['origin']},
            'complete_for_modeled_observe_branches':backend.complete(use),'business_policy_proved':False,
            'no_program_mutation':True}


````

