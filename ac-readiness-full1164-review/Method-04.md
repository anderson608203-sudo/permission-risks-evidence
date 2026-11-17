# 实际运行源码完整分段

完整文件按原路径列出，哈希指原文件字节。

## source/src/pr_next_joint/investigation/context.py

SHA-256 `c6543bbd54a49b0f3552a2aa1dac806b08b57551362f92c307c05ff17ec7c110`

```python
"""Source-first, graph-organized views. Complete original facts stay local."""
import copy,json,re
from collections import defaultdict,deque
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import walk
from .contracts import VERSION
from .protocol import instruction,REVISION_GUIDANCE,question_entity

class Catalog:
    def __init__(self,program,graph=None):
        self.program=program if hasattr(program,'context') else None
        self.context=program.context if self.program else program
        self.identity=self.program.identity if self.program else digest(program)
        self.graph=graph
        self.sources={s['file']:s for s in self.context['sources']}
        self.operations={o['id']:o for o in self.context['operations']}
        self.targets=sorted({o['target'] for o in self.operations.values()})
        self.target_alias={t:'T'+str(i+1) for i,t in enumerate(self.targets)}
        self.labels={};self.label_locations={};self.aliases=defaultdict(list);self.declarations={};self.declaration_aliases=defaultdict(list)
        for oid,o in self.operations.items():
            for name in (o['target']+'.'+o['function'],self.target_alias[o['target']]+'.'+o['function'],
                         o['function'],o['target'].split(':',1)[-1]+'.'+o['function']):self.aliases[name].append(oid)
        # A declaring base name is not necessarily a selected creation target.
        # Join the exact compiler-selected entry declaration to its source owner;
        # never resolve an overridden body merely by a matching spelling.
        self.declaration_entries=defaultdict(list)
        if self.program and hasattr(self.program,'lookup'):
            for oid,o in self.operations.items():
                lookup=self.program.lookup(oid);node=lookup.function(o['function'])
                node=node.get('generated_getter',node)
                owner=next((c for c in lookup.nodes.values() if c.get('nodeType')=='ContractDefinition'
                    and any(n.get('id')==node.get('id') for n in c.get('nodes',[]))),None)
                if owner is None or node.get('nodeType')!='FunctionDefinition':continue
                actual=lookup.anchor(node)
                if any(actual.get(k)!=o['source'].get(k) for k in ('file','start','length','ast_id')):continue
                aliases=(actual['file']+':'+owner['name']+'.'+o['function'],owner['name']+'.'+o['function'])
                for alias in aliases:
                    self.aliases[alias].append(oid)
                    self.declaration_entries[alias].append({'operation':oid,'declaring_contract':owner['name'],
                        'applied_target':o['target'],'ast_id':node['id'],'source':actual,
                        'basis':'compiler-selected implementation and exact declaration containment/span'})
        # Internal declarations supply source evidence, never external transactions.
        if self.program and hasattr(self.program,'lookups'):
            from pr_next_joint.frontend.source_entry_identity import declared_type_pair
            for target,lookup in self.program.lookups.items():
                bases=lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
                # Old compiler ASTs omit scope on functions. The owning contract
                # is still exact from AST containment, including inherited bases.
                owners={child['id']:c['id'] for c in lookup.nodes.values() if c.get('nodeType')=='ContractDefinition' for child in c.get('nodes',[]) if isinstance(child,dict)}
                for n in lookup.nodes.values():
                    if n.get('nodeType') not in ('FunctionDefinition','ModifierDefinition') or n.get('scope',owners.get(n['id'])) not in bases:continue
                    if n.get('nodeType')=='FunctionDefinition' and n.get('visibility') not in ('internal','private'):continue
                    pairs=[declared_type_pair(p.get('typeName',{}),lookup) for p in n.get('parameters',{}).get('parameters',[])]
                    if any(p is None for p in pairs):continue
                    sig=n.get('name','')+'('+','.join(p[1] for p in pairs)+')';ref='decl_'+digest([target,n['id']])[:20]
                    self.declarations[ref]={'id':ref,'target':target,'ast_id':n['id'],'function':sig,'source':lookup.anchor(n),'external_transaction':False}
                    owner=lookup.nodes.get(n.get('scope',owners.get(n['id'])),{})
                    declared=(lookup.anchor(n)['file']+':'+owner.get('name','')+'.'+sig,owner.get('name','')+'.'+sig)
                    for alias in (target+'.'+sig,target.split(':',1)[-1]+'.'+sig,sig)+declared:
                        self.declaration_aliases[alias].append(ref)
            from pr_next_joint.frontend.dispatch import resolve as dispatch
            for alias,refs in list(self.declaration_aliases.items()):
                targets={self.declarations[r]['target'] for r in refs}
                if len(targets)!=1 or len(refs)<2:continue
                lookup=self.program.lookups[next(iter(targets))]
                resolved={dispatch(lookup,lookup.nodes[self.declarations[r]['ast_id']])['id'] for r in refs}
                chosen=[r for r in refs if self.declarations[r]['ast_id'] in resolved]
                if len(resolved)==len(chosen)==1:self.declaration_aliases[alias]=chosen
        self.internal_callers=defaultdict(list)
        if self.program and hasattr(self.program,'lookup'):
            def reaches(lookup,body,nid,seen):
                from pr_next_joint.frontend.dispatch import resolve as dispatch,member_target
                refs=set()
                for n in walk(body):
                    if n.get('nodeType')!='FunctionCall':continue
                    ref=n.get('expression',{}).get('referencedDeclaration');node=lookup.nodes.get(ref,{})
                    if node.get('nodeType')!='FunctionDefinition':continue
                    try:
                        dest=dispatch(lookup,node) if n['expression'].get('nodeType')=='Identifier' else member_target(lookup,n,node)
                    except (KeyError,ValueError,TypeError,AttributeError):
                        dest=None
                    if dest:refs.add(dest['id'])
                refs|={n.get('modifierName',{}).get('referencedDeclaration') for n in walk(body) if n.get('nodeType')=='ModifierInvocation'}
                if nid in refs:return True
                for ref in refs-seen:
                    node=lookup.nodes.get(ref,{})
                    if node.get('nodeType') in ('FunctionDefinition','ModifierDefinition') and reaches(lookup,node,nid,seen|{ref}):return True
                return False
            for ref,decl in self.declarations.items():
                for oid,operation in self.operations.items():
                    if operation['target']!=decl['target']:continue
                    lookup=self.program.lookup(oid)
                    if reaches(lookup,lookup.function(operation['function']),decl['ast_id'],set()):self.internal_callers[ref].append(oid)
        self.frontier=self.context['frontier'];self.adj=defaultdict(set)
        for edge in self.frontier:
            self.adj[edge['from']].add(edge['to']);self.adj[edge['to']].add(edge['from'])
    def name(self,oid):
        o=self.operations[oid];return o['target']+'.'+o['function']
    def slice(self,anchor):
        s=self.sources[anchor['file']]['content'].encode('utf-8')
        return s[anchor['start']:anchor['start']+anchor['length']].decode('utf-8',errors='replace')
    def lines(self,anchor):
        s=self.sources[anchor['file']]['content'].encode('utf-8')
        return [s[:anchor['start']].count(b'\n')+1,s[:anchor['start']+anchor['length']].count(b'\n')+1]
    def resolve(self,anchor):
        if not isinstance(anchor,str):return []
        if anchor in self.labels:return list(self.labels[anchor])
        if anchor in self.aliases:return sorted(set(self.aliases[anchor]))
        # A literal placeholder is not an ABI type. Resolve its exact qualified
        # declaration family only when the compiler catalog has a single entry.
        # Concrete wrong signatures (including enum/uint mismatches) are NOT repaired.
        placeholder=re.fullmatch(r'(.+)\((?:function|\.\.\.|\?)\)',anchor)
        if placeholder:
            family=placeholder[1]+'('
            return sorted({o for alias,ids in self.aliases.items() if alias.startswith(family)
                           for o in ids})
        # Short names only enumerate exact declarations. Never fuzzy-select one.
        if re.fullmatch(r'[A-Za-z_$][\w$]*',anchor):
            return sorted(o for o,x in self.operations.items() if x['function'].split('(')[0]==anchor)
        m=re.fullmatch(r'(.+\.sol):(\d+)(?:[-:](\d+))?',anchor)
        if m and m[1] in self.sources:
            lo=int(m[2]);hi=int(m[3] or lo)
            return sorted(o for o,x in self.operations.items() if x['source']['file']==m[1] and
                          self.lines(x['source'])[0]<=lo<=self.lines(x['source'])[1] and hi>=lo)
        return []
    def target_branches(self,anchors,core=None):
        initial=core or (anchors[0] if anchors else None)
        ids=self.resolve(initial)
        if len(ids)<2:return []
        # A short, ABI-qualified or line anchor can denote the very same
        # compiler declaration in several layouts. Verify its actual source
        # identity on every applied operation, independently of alias spelling.
        locations={tuple(self.operations[o]['source'].get(k) for k in ('file','ast_id','start','length')) for o in ids}
        if len(locations)!=1 or None in next(iter(locations)):return []
        targets=[self.operations[o]['target'] for o in ids]
        return sorted(targets) if len(set(targets))==len(ids) else []
    def bind(self,anchors,core=None,prior=None,target=None):
        def allowed(ids):
            return [oid for oid in ids if target is None or self.operations[oid]['target']==target]

        located={};unresolved=[];ambiguous=[];internal=[]
        for anchor in anchors:
            ids=allowed(self.resolve(anchor))
            if not ids:
                refs=[r for r in self.declaration_aliases.get(anchor,[]) if target is None or self.declarations[r]['target']==target]
                if refs:
                    internal.extend(copy.deepcopy(self.declarations[r]) for r in dict.fromkeys(refs))
                    if len(refs)>1:ambiguous.append({'anchor':anchor,'declaration_contexts':list(dict.fromkeys(refs))})
                else:unresolved.append(anchor)
            elif len(ids)>1:ambiguous.append({'anchor':anchor,'candidates':ids});located[anchor]=ids
            else:located[anchor]=ids
        requested=core if isinstance(core,str) else anchors[0] if anchors else None
        core_ids=allowed(self.resolve(requested)) if requested else []
        protected_ambiguity=len(core_ids)>1 and (self.target_branches(anchors,requested) or self.declaration_entries.get(requested) or
            re.fullmatch(r'.+\((?:function|\.\.\.|\?)\)',requested or ''))
        if core is None and len(core_ids)!=1 and not protected_ambiguity:
            core_ids=next((v for v in located.values() if len(v)==1),[])
        # A valid old core is retained only when the revision did not request a
        # different explicit root. An invalid new core cannot replace it silently.
        internal_contexts={r['id']:self.internal_callers.get(r['id'],[]) for r in internal}
        contexts=sorted({i for ids in internal_contexts.values() for i in ids})
        # An internal-only clue starts in its real external caller context. A
        # unique caller is exact; multiple callers remain ambiguous, never an
        # invented directly callable internal transaction.
        if not core_ids and len(contexts)==1 and requested in self.declaration_aliases:core_ids=contexts
        selection='explicit_root' if core is not None else 'initial_source_anchor'
        old_core=(prior or {}).get('core_operation')
        if core is None and (prior or {}).get('core_exact') and old_core in self.operations:
            # Ordering, adding or dropping supplementary references is not a
            # request to relocate the existing root. accept validates genuine
            # semantic corrections separately, without requiring a root field.
            core_ids=[old_core];selection='preserved_prior_core'
        core_operation=core_ids[0] if len(core_ids)==1 else None
        core_anchor=((prior or {}).get('core_anchor') or self.name(old_core)) if selection=='preserved_prior_core' else (
            core if core is not None and len(self.resolve(core))==1 else next((a for a,ids in located.items() if ids==core_ids),None))
        return {'applied_context':target,'located':located,'operations':sorted({i for ids in located.values() for i in ids}|set(contexts)|set(core_ids)),
                'unresolved':unresolved,'ambiguous':ambiguous,'internal_references':internal,
                'internal_external_caller_contexts':internal_contexts,
                'core_operation':core_operation,'core_exact':core_operation is not None,
                'core_anchor':core_anchor,'core_selection':selection,
                'exact':core_operation is not None,'all_references_exact':bool(located) and not unresolved and not ambiguous,
                'supplementary_gaps':unresolved+ambiguous,
                'declaration_entry_bindings':{a:copy.deepcopy(self.declaration_entries[a]) for a in anchors if a in self.declaration_entries},
                'candidate_core_operations':sorted(set(core_ids or contexts or [i for v in located.values() for i in v])),
                'placeholder_clarifications':[{'original':a,'resolved':self.name(ids[0]),
                    'source':copy.deepcopy(self.operations[ids[0]]['source']),
                    'basis':'literal placeholder; unique exact target/declaration family, not fuzzy ABI matching'}
                    for a,ids in located.items() if len(ids)==1 and re.fullmatch(r'.+\((?:function|\.\.\.|\?)\)',a)]}
    def related(self,oid):return sorted(self.adj[oid])
    def card(self,oid):
        o=self.operations[oid];return {'anchor':self.name(oid),'operation_id_for_host':oid,
            'source':copy.deepcopy(o['source']),'lines':self.lines(o['source']),
            'code':self.slice(o['source']),'parameters':[{k:v for k,v in p.items() if k=='name'} for p in o['parameters']]}
    def support(self,oid):
        """Actual declarations, modifiers and internal calls, not normality templates."""
        if not self.program or not hasattr(self.program,'lookup'):
            # Read-only prepared-message previews can reuse the exact saved M1 graph.
            graph=self.graph if isinstance(self.graph,dict) else {};nodes={n['id']:n for n in graph.get('nodes',[])}
            anchors=[];o=self.operations[oid]
            for edge in graph.get('edges',[]):
                if edge['from']==oid and edge['kind'] in ('calls','modifier'):
                    a=nodes.get(edge['to'],{}).get('data',{}).get('source')
                    if a:anchors.append(a)
            roots={n['root'] for p in o['paths'] for ref in p.get('guards',[])+[w['selector'] for w in p.get('writes',[])]
                   for n in walk(self.context['terms'].get(ref,{}).get('expression',{})) if n.get('kind')=='storage'}
            anchors +=[r['source'] for r in self.context['references'].values() if r['target']==o['target'] and r['ast_id'] in roots]
            return [{'source':a,'code':self.slice(a),'kind':'saved_exact_source_dependency'} for a in {tuple(sorted(a.items())):a for a in anchors if a['file'] in self.sources}.values()]
        lookup=self.program.lookup(oid);o=self.operations[oid];body=lookup.function(o['function'])
        needed=[]
        for n in walk(body):
            if n.get('nodeType')=='ModifierInvocation':needed.append(n.get('modifierName',{}).get('referencedDeclaration'))
            if n.get('nodeType')=='FunctionCall':needed.append(n.get('expression',{}).get('referencedDeclaration'))
        roots={n['root'] for p in o['paths'] for t in p.get('guards',[]) for n in walk(self.context['terms'].get(t,{}).get('expression',{})) if n.get('kind')=='storage'}
        for w in (self.program.writes.values()):
            if w['operation']==oid:roots.add(w['raw']['path']['root'])
        needed+=sorted(roots)
        result=[]
        for nid in dict.fromkeys(needed):
            node=lookup.nodes.get(nid)
            if not node or node.get('nodeType') not in ('VariableDeclaration','ModifierDefinition','FunctionDefinition'):continue
            a=lookup.anchor(node)
            if a['length'] and a['file'] in self.sources:
                result.append({'source':a,'code':self.slice(a),'kind':node['nodeType']})
        return result
    def index(self):
        result={'targets':{a:t for t,a in self.target_alias.items()},'entries':[
            self.target_alias[o['target']]+'.'+o['function'] for o in sorted(self.operations.values(),key=lambda x:(x['target'],x['function']))],
            'meaning':'T aliases denote exact targets; repeated inherited source remains target-specific.'}
        if self.program:
            from pr_next_joint.frontend.source_entry_identity import function_kind
            declarations={}
            for target,lookup in self.program.lookups.items():
                bases=lookup.contract_node.get('linearizedBaseContracts',[])
                inst=[]
                for bid in bases:
                    base=lookup.nodes[bid]
                    names=[n['id'] for n in base.get('nodes',[]) if n.get('nodeType')=='FunctionDefinition'
                           and function_kind(n)=='constructor']
                    inst.append([base.get('name'),names])
                declarations[self.target_alias.get(target,target)]=inst
            result['construction_by_target']=declarations
            result['dispatch_note']='Entries are runtime entries; base names and constructor declaration IDs refer to the compiler-selected linearization.'
        return result

    def required_context(self,operations):
        """AST-bound declaration/call closure for one feedback unit, not top-k.

        Include contract headers, base declarations and referenced helpers. If an
        exact closure cannot be built, the caller must not send a partial unit.
        """
        fragments={};identities=[];missing=[]
        def add(anchor,kind,target):
            if not anchor or anchor.get('file') not in self.sources:return
            loc=(anchor['file'],anchor['start'],anchor['length'])
            entry=fragments.setdefault(loc,{'source':{k:v for k,v in anchor.items() if k!='ast_id'},
                'kind':kind,'code':self.slice(anchor),'targets':[]})
            if target not in entry['targets']:entry['targets'].append(target)
        for oid in dict.fromkeys(operations):
            if oid not in self.operations:continue
            o=self.operations[oid]
            if not self.program or not hasattr(self.program,'lookup'):
                missing.append({'operation':oid,'reason':'compiler_declaration_context_unavailable'});continue
            lookup=self.program.lookup(oid);body=lookup.function(o['function'])
            if not body:missing.append({'operation':oid,'reason':'exact_entry_declaration_unavailable'});continue
            declaration=body.get('generated_getter',body)
            from pr_next_joint.frontend.source_entry_identity import function_kind
            owners={n['id']:c for c in lookup.nodes.values() if c.get('nodeType')=='ContractDefinition'
                    for n in c.get('nodes',[]) if isinstance(n,dict)}
            declaring=owners.get(declaration.get('id'),lookup.contract_node)
            identities.append({'anchor':self.name(oid),'entry_kind':'generated_getter' if 'generated_getter' in body else function_kind(body),
                'declaring_contract':declaring.get('name'),'applied_target':o['target'],
                'basis':'compiler AST kind and declaration containment, not function spelling',
                'constructor_declarations':[{'declaring_contract':c.get('name'),'compiler_kind':'constructor',
                    'source':lookup.anchor(n),'external_transaction':False}
                    for c in lookup.nodes.values() if c.get('nodeType')=='ContractDefinition' and
                        c['id'] in lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
                    for n in c.get('nodes',[]) if function_kind(n)=='constructor']})
            bases=lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
            queue=[declaration['id']]
            for cid in bases:
                c=lookup.nodes.get(cid,{})
                if not c:continue
                a=lookup.anchor(c);children=[lookup.anchor(n)['start'] for n in c.get('nodes',[]) if lookup.anchor(n).get('file')==a['file']]
                header_length=min(children)-a['start'] if children else a['length']
                if header_length<=0:missing.append({'target':o['target'],'reason':'contract_header_not_locatable'});continue
                add({**a,'length':header_length},'contract_header_and_inheritance',o['target'])
                # Declaration context is conservative and neutral; no business
                # classification is inferred from state-variable names.
                queue += [n['id'] for n in c.get('nodes',[]) if n.get('nodeType') in
                          ('VariableDeclaration','StructDefinition','EnumDefinition','UserDefinedValueTypeDefinition')]
                queue += [n['id'] for n in c.get('nodes',[]) if function_kind(n)=='constructor']
            for n in lookup.nodes.values():
                if n.get('nodeType') in ('PragmaDirective','ImportDirective'):
                    add(lookup.anchor(n),n['nodeType'],o['target'])
            seen=set()
            while queue:
                nid=queue.pop()
                if nid in seen:continue
                seen.add(nid);n=lookup.nodes.get(nid,{})
                if n.get('nodeType') not in ('FunctionDefinition','ModifierDefinition','VariableDeclaration',
                      'StructDefinition','EnumDefinition','EventDefinition','UserDefinedValueTypeDefinition'):continue
                owner=owners.get(nid)
                if owner and owner['id'] not in bases:
                    a=lookup.anchor(owner);children=[lookup.anchor(x)['start'] for x in owner.get('nodes',[]) if lookup.anchor(x).get('file')==a['file']]
                    add({**a,'length':min(children)-a['start'] if children else a['length']},'referenced_declaration_contract_header',o['target'])
                add(lookup.anchor(n),n['nodeType'],o['target'])
                # referencedDeclaration denotes the lexical declaration, not
                # necessarily the implementation executed by this target.
                # Reuse the same dispatch as source execution, including the
                # lexical owner of super and explicit/private bindings.
                from pr_next_joint.frontend.dispatch import resolve,member_target
                call_expressions=set()
                for call in walk(n):
                    if call.get('nodeType')!='FunctionCall':continue
                    expr=call.get('expression',{});ref=expr.get('referencedDeclaration')
                    target=lookup.nodes.get(ref,{})
                    internal=expr.get('typeDescriptions',{}).get('typeIdentifier','').startswith('t_function_internal_')
                    if target.get('nodeType')!='FunctionDefinition':
                        if internal:
                            missing.append({'target':o['target'],'source':lookup.anchor(call),
                                'reason':'internal_call_implementation_context_unresolved'})
                        continue
                    call_expressions.add(expr.get('id'))
                    try:
                        owner=owners.get(ref,{})
                        if (target.get('visibility')!='private' and owner.get('id') in bases and len(bases)>1
                                and (target.get('scope')!=owner.get('id') or any(not p.get('typeDescriptions',{}).get('typeIdentifier')
                                    for p in target.get('parameters',{}).get('parameters',[])))):
                            raise ValueError('compiler_dispatch_metadata_incomplete')
                        if expr.get('nodeType')=='Identifier':bound=resolve(lookup,target)
                        else:bound=member_target(lookup,call,target)
                        if bound is None:
                            # An external/interface declaration is source
                            # context, not a proven implementation binding.
                            queue.append(ref)
                            if internal:raise ValueError('internal_dispatch_not_resolved')
                        else:queue.append(bound['id'])
                    except (ValueError,KeyError,TypeError,AttributeError) as error:
                        queue.append(ref)
                        missing.append({'target':o['target'],'source':lookup.anchor(call),
                            'reason':'required_call_dispatch_context_unresolved',
                            'detail':type(error).__name__+':'+str(error)})
                for child in walk(n):
                    ref=child.get('referencedDeclaration')
                    if ref in lookup.nodes and child.get('id') not in call_expressions:queue.append(ref)
                    if child.get('nodeType')=='ModifierInvocation':
                        queue.append(child.get('modifierName',{}).get('referencedDeclaration'))
            # Exact source closure has no function-name or dataset-ID exceptions.
        ordered=sorted(fragments.items())
        # Do not send nested source twice (e.g. a struct member inside its struct).
        kept=[]
        for loc,entry in sorted(ordered,key=lambda x:(x[0][0],x[0][1],-x[0][2])):
            if any(loc[0]==p['source']['file'] and p['source']['start']<=loc[1] and
                   loc[1]+loc[2]<=p['source']['start']+p['source']['length'] for p in kept):continue
            kept.append(entry)
        return kept,identities,missing

class SourceContext:
    def __init__(self,program,catalog,counter):
        self.program,self.catalog,self.counter=program,catalog,counter;self.initial_view=None;self.initial_scope=None;self.last_manifest=None
    def _messages(self,value,recovery=False):
        kind=None
        if 'questions' in value:
            question=next(iter(value['questions']),{})
            choice=next(iter(question.get('semantic_questions',[])),{})
            choice=value.get('shared_rows',{}).get(choice.get('shared'),choice)
            kind='local_effect' if question.get('local_effect_review') else choice.get('kind','issue')
        revisable_amount=(self.program.options.scope=='FCR' and
                         any('on' in card for card in value.get('supports',())))
        audit_revision = (' To withdraw your own displayed interpretation use hypotheses[{withdraw:audit_ref,effect_ref,reason}].'
                          if any(q.get('audit_ref') for q in value.get('questions',())) else '')
        return [{'role':'system','content':instruction(self.program.options.scope,recovery or value.get('purpose')=='protocol_recovery',
                                                      kind=kind,annotation_revision=revisable_amount,policy_revision=any('effect' in card for card in value.get('supports',()))) + audit_revision},
                {'role':'user','content':json.dumps(value,ensure_ascii=False,separators=(',',':'))}]
    def _count(self,value):return self.counter.count(self._messages(value))
    def _model_card(self,oid):
        c=self.catalog.card(oid);c.pop('operation_id_for_host');c['support']=self.catalog.support(oid)
        # Fact payloads and expression graphs never re-enter M2 through this view.
        for x in [c,*c['support']]:
            if 'source' in x:x['source']={k:v for k,v in x['source'].items() if k!='ast_id'}
        return c
    def _focus(self):
        graph=self.catalog.graph
        if graph is None:
            return None, []
        front=graph.neutral_frontier()
        r=front['primary']
        if r is None:
            return None, []
        names=self.catalog.name
        focus={'write':names(r['writer']),'use':names(r['use']),'cell':r['declaration'],
               'read_in':r['role_of_read'],'question':'Which actual subject and right are affected? What observable distinguishes the applicable explanations?'}
        use_cells=[w['raw']['path'] for w in self.program.writes.values() if w['operation']==r['use']]
        related=graph.closure_operations(r['use'],[r['ordered_read_key'],*use_cells])
        return focus,list(dict.fromkeys([r['writer'],r['use'],*related]))

    @staticmethod
    def _share(value):
        """Intern only identical rows across questions; branch, key and role are part of identity."""
        if len(value['questions'])<2:
            return value
        value=copy.deepcopy(value)
        occurrences=defaultdict(list)
        for qi,q in enumerate(value['questions']):
            for field in ('entry_identity_facts','evidence'):
                for i,v in enumerate(q.get(field,[])):
                    occurrences[(field,digest(v))].append((qi,i))
        shared={}
        for (field,h),sites in occurrences.items():
            if len(sites)<2:
                continue
            qi,i=sites[0];row=value['questions'][qi][field][i]
            if len(json.dumps(row))<100:
                continue
            ref='s'+str(len(shared)+1);shared[ref]=row
            for qi,i in sites:
                value['questions'][qi][field][i]={'shared':ref}
        if shared:
            value['shared_rows']=shared
        return value

    def initial(self):
        p=self.program;cat=self.catalog;target=p.options.input_target;limit=p.options.input_limit
        base={'presentation':VERSION,'task':p.options.scope,'entry_index':cat.index(),
              'semantic_focus':('Assess the actual caller against the applicable duty at the highlighted effects.' if p.options.scope=='AC'
                                else 'Clarify the unit or consent of the highlighted account position if material.')}
        complete={**base,'source_files':[{'file':f,'content':s['content']} for f,s in cat.sources.items()]}
        focus,focus_ops=self._focus()
        if self._count(complete)<=limit:
            manifest={'mode':'complete_source','expanded_operations':sorted(cat.operations),'unexpanded_operations':[],
                      'complete_source_files':sorted(cat.sources),'fragments':[],'requested_reading':'whole_task',
                      'focus_operations':focus_ops,'open_clues_allowed':True,
                      'over_target_reason':'retain_complete_source_once' if self._count(complete)>target else None}
            if focus and self._count({**complete,'primary_question':focus})<=target:
                complete['primary_question']=focus
                manifest['focus_delivery']='compact_source_locator'
            elif focus:
                short={'write':focus['write'],'use':focus['use']}
                if self._count({**complete,'primary_question':short})<=target:
                    complete['primary_question']=short
                    manifest['focus_delivery']='minimal_two_entry_locator'
                else:
                    manifest['focus_delivery']='summary_omitted_to_preserve_full_source'
            else:
                manifest['focus_delivery']='no_supported_meeting; source open'
            # The effect cards carry the exact applied positions of extra writes and exits.
            return complete,manifest
        # Structural degree and per-target round robin; never labels, file polarity or old hits.
        queues=[]
        for t in cat.targets:
            ordered=sorted((i for i,o in cat.operations.items() if o['target']==t),key=lambda i:(cat.operations[i].get('generated_getter',False),-len(cat.adj[i]),cat.name(i)))
            queues.append(deque(ordered))
        order=[]
        while any(queues):
            for q in queues:
                if q:order.append(q.popleft())
        value={**base,'source_fragments':[]};expanded=[];seen=set();partial=[]
        focus_missing=[];focus_placed=False
        if focus:
            closure,identities,focus_missing=cat.required_context(focus_ops)
            trial={**value,'primary_question':focus,'related_source':closure}
            if not focus_missing and self._count(trial)<=target:
                value=trial;focus_placed=True;expanded.extend(focus_ops)
                for frag in closure:
                    loc=frag['source'];seen.add((loc['file'],loc['start'],loc['length']))
            elif not focus_missing:
                focus_missing=[{'reason':'source_focus_closure_exceeds_soft_target','operations':focus_ops}]
        order=list(dict.fromkeys(focus_ops+order))
        for oid in order:
            c=self._model_card(oid);a=cat.operations[oid]['source'];loc=(a['file'],a['start'],a['length'])
            if loc in seen:
                # Share exact source bytes but retain each target application in the index/manifest.
                expanded.append(oid);continue
            candidate={**value,'source_fragments':value['source_fragments']+[c]}
            if self._count(candidate)<=target or (not value['source_fragments'] and self._count(candidate)<=limit):
                value=candidate;expanded.append(oid);seen.add(loc)
                for neighbor in cat.related(oid):
                    if neighbor in expanded:continue
                    nc=self._model_card(neighbor);na=cat.operations[neighbor]['source'];nl=(na['file'],na['start'],na['length'])
                    if nl in seen:expanded.append(neighbor);continue
                    trial={**value,'source_fragments':value['source_fragments']+[nc]}
                    if self._count(trial)<=target:value=trial;expanded.append(neighbor);seen.add(nl)
            if self._count(value)>=target:break
        # Oversized single functions: use whole AST statements, explicitly recording partial scope.
        if not expanded and cat.program and hasattr(cat.program,'lookup'):
            for oid in order:
                o=cat.operations[oid];lookup=cat.program.lookup(oid);body=lookup.function(o['function'])
                for node in body.get('body',{}).get('statements',[]):
                    a=lookup.anchor(node);c={'anchor':cat.name(oid),'source':{k:v for k,v in a.items() if k!='ast_id'},
                        'code':cat.slice(a),'partial_function':True}
                    trial={**value,'source_fragments':value['source_fragments']+[c]}
                    if self._count(trial)<=target:value=trial;partial.append(oid)
                if partial:break
        for i,c in enumerate(value['source_fragments']):
            c['fragment']='S'+str(i+1);cat.labels[c['fragment']]=cat.resolve(c['anchor'])
            cat.label_locations[c['fragment']]=copy.deepcopy(c['source'])
        missing=sorted(set(cat.operations)-set(expanded))
        value['unexpanded_entry_count']=len(missing)
        # Exact missing IDs stay in the host manifest; all source names already
        # occur in the complete compact entry index, so do not duplicate them.
        return value,{'mode':'graph_source_fragments','expanded_operations':sorted(set(expanded)),
            'partially_expanded_operations':sorted(set(partial)),'unexpanded_operations':missing,
            'requested_reading':'delivered_scope','focus_operations':focus_ops,'focus_context_gaps':focus_missing,
            'focus_delivery':'source_closure' if focus_placed else 'open_source_view','open_clues_allowed':True,
            'complete_source_files':[],'fragments':[{'fragment':c['fragment'],'anchor':c['anchor'],'partial':c.get('partial_function',False)} for c in value['source_fragments']]}
    def focused(self,feedback):
        base={'presentation':VERSION,'task':self.program.options.scope,
              'purpose':'Revise only these issues using the original source and new local evidence; omitted issues remain.',
              'source_and_explanation_are_distinct':True,'questions':[]}
        complete={**base,'source_files':[{'file':f,'content':s['content']} for f,s in self.catalog.sources.items()]}
        units=[];deduplicated=0;selected_entities={};shared_consumers={}
        host_questions={};observed_amount_disputes=set()
        for q in feedback['questions']:
            item=copy.deepcopy(q);ops=item.pop('operations',[])
            requested=item.pop('requested_effects',[])
            if requested:item['effect']='effect:'+requested[0][2:14]
            for qrow in item.get('semantic_questions',[]):
                host_questions[qrow['id']]=qrow
                if qrow.get('_observed_amount_dispute'):
                    observed_amount_disputes.add((q['id'],qrow['id']))
            for field in ('sent_evidence','sent_semantics','sent_message_identity','internal_external_caller_contexts'):
                item.pop(field,None)
            # Only byte/structure-equivalent evidence is merged. Caller, key,
            # branch, assumptions and formula identity remain part of equality.
            for e in item.get('evidence',[]):
                for field in ('probe_results','comparisons'):
                    if not isinstance(e.get(field),list):continue
                    rows={}
                    for v in e[field]:rows.setdefault(digest(v),v)
                    deduplicated+=len(e[field])-len(rows);e[field]=list(rows.values())
            for field in item.get('evidence',[]):
                if 'probe_results' in field:
                    field['probe_results']=[{k:p[k] for k in ('id','label','answer','bounded_condition_confirmed') if k in p} for p in field['probe_results']]
            fragments,identity,missing=self.catalog.required_context(ops)
            item['entry_identity_facts']=[{k:v for k,v in r.items() if k in ('anchor','entry_kind','declaring_contract','applied_target','constructor_declarations')} for r in identity]
            choices=item.get('semantic_questions',[])
            if not choices:units.append((q['id'],item,ops,fragments,missing))
            for proposal in choices:
                visible={k:proposal[k] for k in ('id','kind','question','choices','source_name','target') if k in proposal}
                if proposal.get('quantity_scope'):
                    visible['scope']='same holder-issued grant, spender, unit and request at this use'
                units.append((q['id'],dict(item,semantic_questions=[visible]),ops,fragments,missing))
        # A model decision is useful when competing readings predict different
        # consequences, or a still-unbound right/policy controls the judgment.
        # A local type error or an already-settled scalar fact is not a reason
        # to spend the remaining response. Source order breaks equal priority.
        def priority(unit):
            item=unit[1]
            # A typed, source-bound missing meaning is directly answerable.
            # A generic neutral task disagreement must not consume the only
            # revision while an actual amount/policy question remains unsent.
            return (not bool(item.get('audit_ref') and item.get('evidence') and item.get('alternative')),
                    not any((unit[0],q.get('id')) in observed_amount_disputes for q in item.get('semantic_questions',[])),not any(q.get('kind')=='scoped_support_dispute' for q in item.get('semantic_questions',[])),not bool(item.get('local_effect_review') or item.get('semantic_questions')),
                    not bool(item.get('task_conflict') or item.get('alternative') and item.get('evidence')),
                    not bool(item.get('alternative')))
        units.sort(key=priority)
        value={**base,'related_source':[]}
        selected=[];omitted=[];used=set();seen={};full_mode=False
        for qid,item,ops,fragments,missing in units:
            semantic=item.get('semantic_questions',[])
            decision=digest([sorted(ops),item.get('category'),item.get('claim'),item.get('alternative'),
                item.get('distinguishing_question'),[s.get('id') for s in semantic],item.get('evidence')])
            descriptor=host_questions.get(semantic[0]['id']) if semantic else None
            entity_key=digest([descriptor.get(k) for k in ('kind','target','operation','cell','semantic_scope','quantity_scope','choices')]) if descriptor and descriptor.get('kind') in ('financial_consent','authorization','resource') else None
            if entity_key in selected_entities and entity_key is not None:
                shared_consumers.setdefault(selected_entities[entity_key],[]).append(qid)
                omitted.append({'issue':qid,'reason':'shared_displayed_source_question','representative':selected_entities[entity_key]})
                continue
            if decision in seen:
                omitted.append({'issue':qid,'reason':'same_dispute_and_evidence','representative':seen[decision]});continue
            if selected:
                omitted.append({'issue':qid,'reason':'independent_dispute_retained_locally','priority':list(priority((qid,item)))})
                continue
            if not (semantic or item.get('local_effect_review') or item.get('task_conflict') or item.get('alternative') and item.get('evidence')):
                omitted.append({'issue':qid,'reason':'no_unresolved_semantic_distinction'});continue
            # Prefer the actual dependency closure of the single disputed effect.
            merged={}
            for frag in fragments:
                k=digest(frag['source'])
                if k in merged:merged[k]['targets']=sorted(set(merged[k]['targets']+frag['targets']))
                else:merged[k]=copy.deepcopy(frag)
            local={**base,'questions':[item],'related_source':list(merged.values())}
            full={**complete,'questions':[item]}
            local_tokens=self._count(self._share(local)) if merged and not missing else None
            full_tokens=self._count(self._share(full))
            full_mode=local_tokens is None or full_tokens<=local_tokens
            trial,tokens=(full,full_tokens) if full_mode else (local,local_tokens)
            if not merged and missing and tokens>self.program.options.input_limit:
                omitted.append({'issue':qid,'reason':'required_context_unavailable','actual_trial_input_tokens':tokens})
                continue
            if tokens<=self.program.options.input_limit:
                value=trial;selected.append(qid);used.update(ops);seen[decision]=qid
                if entity_key:selected_entities[entity_key]=qid
            else:omitted.append({'issue':qid,'reason':'whole_required_source_and_evidence_unit_exceeds_remaining_capacity',
                                 'actual_trial_input_tokens':tokens,'input_limit':self.program.options.input_limit})
        value=self._share(value)
        visible={};semantic_wire={}
        for question in value['questions']:
            labels={}
            for field in question.get('evidence',[]):
                row=value.get('shared_rows',{}).get(field.get('shared'),field)
                if isinstance(row.get('id'),str):
                    labels[row['id']]=[p['id'] for p in row.get('probe_results',[]) if 'id' in p]
            visible[question['id']]=labels
            for supplied in question.get('semantic_questions',[]):
                row=value.get('shared_rows',{}).get(supplied.get('shared'),supplied)
                if row.get('id'):
                    semantic_wire[row['id']]={'display':digest(row),'entity':question_entity(host_questions[row['id']]),'issue':question['id']}
        return value,{'mode':'focused_evidence','source_mode':'complete_source_once' if full_mode else 'compiler_bound_local_context',
            'disputed_effects':sorted({e for sid in semantic_wire for e in host_questions[sid].get('affected_effects',[])}|{e for q in feedback['questions'] if q['id'] in selected for e in q.get('requested_effects',())}),'shared_question_consumers':shared_consumers,'wire_evidence':visible,'semantic_wire':semantic_wire,'shared_row_count':len(value.get('shared_rows',{})),
            'selected_issues':selected,'unexpanded_feedback_issues':omitted,'expanded_operations':sorted(used),
            'selection_rule':'one_source_scoped_decision; capacity and complete necessary context checked per candidate',
            'complete_source_files':sorted(self.catalog.sources) if full_mode else [],'deduplicated_exact_evidence_rows':deduplicated,
            'necessary_context_not_silently_clipped':True,'no_full_facts_or_graph_or_unrelated_history':True}
    def visible_semantics(self,data,manifest,operations,feedback=False):
        rules=getattr(self,'rules',None)
        if not rules:return
        manifest['visible_spans']=[x['source'] for field in ('source_fragments','related_source') for x in data.get(field,[]) if isinstance(x.get('source'),dict)]
        cards,index=rules.cards_for(manifest,operations)
        selected=[]
        base=self._count(data)
        room=min(self.program.options.input_limit-base,max(128,min(self.program.options.input_target//12,base//5)))
        total=0
        for card in cards:
            size=len(self.counter.plain_tokenizer.encode(json.dumps(card,ensure_ascii=False,separators=(',',':')),add_special_tokens=False).ids)+1
            if total+size+8>room:continue
            selected.append(card);total+=size
        while selected and self._count(dict(data,typed_refs=selected))>base+room:selected.pop()
        if selected:data['typed_refs']=selected
        manifest['typed_index']={c[0]:index[c[0]] for c in selected}
        manifest['registered_sensitive_effects']=len(rules.sensitive_effects)
        manifest['displayed_effect_handles']=[index[c[0]] for c in selected if index[c[0]] in rules.effects]
        manifest['omitted_effect_handles']=sorted(set(rules.sensitive_effects)-set(manifest['displayed_effect_handles']))
        if feedback:
            wire={}
            chosen_effects=set(manifest.get('disputed_effects',()))
            relevant_supports=rules.support_inputs(chosen_effects)
            def in_chosen(entry):
                if not chosen_effects:return True
                handle=rules.facts[entry['fact']]['handle']
                if entry['support'] in relevant_supports or handle in chosen_effects:return True
                fact=rules.facts[entry['fact']]
                # An unresolved input cannot propagate an affirmative fact yet. It can
                # still answer the same disputed output when the compiler records an
                # exact scoped value route (e.g. a parameter copied into the balance).
                return fact['meaning'] in ('unknown','other_source_meaning','other_source_policy') and any(
                    effect in chosen_effects and exact and kind=='value' and fact['scope'] in (None,effect)
                    for effect,kind,_,exact in rules.routes.get(handle,()))

            for oid in operations:wire.update(rules.labels_for(oid,manifest))
            shown={};exposed=[]
            for ref,entry in sorted(wire.items()):
                if not rules.remaining():break
                if not in_chosen(entry):continue
                locator='effect' if entry['field']=='policies' else 'on'
                card={'ref':ref,locator:entry['source'],'meaning':entry['meaning']}
                card.update({key:entry[key] for key in ('role','subject','scope','payment_policy') if entry.get(key)})
                if self._count(dict(data,supports=exposed+[card]))>self.program.options.input_limit:continue
                exposed.append(card);shown[ref]=entry
            if exposed:
                data['supports']=exposed;manifest['shown_supports']=shown
            manifest['semantic_supports_omitted']=len(wire)-len(shown)
    def messages(self,feedback=None,recovery=False):
        if recovery:
            if self.initial_view is None:self.initial_view,self.initial_scope=self.initial()
            data=copy.deepcopy(self.initial_view);data['purpose']='protocol_recovery'
            if feedback and feedback.get('binding_diagnostics'):
                data['binding_diagnostics']=copy.deepcopy(feedback['binding_diagnostics'])
            manifest={**copy.deepcopy(self.initial_scope),'mode':'protocol_recovery_reused_source','reused_initial_source_view':True}
        elif feedback is None:
            if self.initial_view is None:self.initial_view,self.initial_scope=self.initial()
            data,manifest=copy.deepcopy(self.initial_view),copy.deepcopy(self.initial_scope)
        else:data,manifest=self.focused(feedback)
        operations=manifest.get('focus_operations',[]) if feedback is None or recovery else manifest.get('expanded_operations',[])
        self.visible_semantics(data,manifest,operations,feedback is not None and not recovery)
        manifest['offered_audit_refs'] = [q['audit_ref'] for q in data.get('questions',())
                                          if q.get('audit_ref') and q.get('audit_ref') == q['id']]
        if any(q.get('local_effect_review') and q.get('effect') not in manifest.get('typed_index',{}) for q in data.get('questions',())):
            manifest['selected_issues']=[]
        messages=self._messages(data,recovery);manifest.update(input_tokens=self.counter.count(messages),
            counter_identity=self.counter.identity,messages_sha256=digest(messages),
            counting_scope='complete V4.1 text message envelope including high/JSON markers; offline count, service usage recorded separately')
        manifest['sent_semantic_rows']={row['id']:row for item in data.get('questions',[]) for ref in item.get('semantic_questions',[])
            for row in [data.get('shared_rows',{}).get(ref.get('shared'),ref)] if 'id' in row}
        self.last_manifest=manifest
        return messages,manifest

```

## source/src/pr_next_joint/investigation/contracts.py

SHA-256 `ed3733795f4a0a3f006cba7a7bb823b170c0f9f1588d333af87bf22c74aedd29`

```python
"""Finite investigation controls and host-owned artifacts; no business detectors."""
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib, json, os, tempfile
from pr_next_joint.core import digest

VERSION = 'permission-risks-sp200-simplification-r2'
CATEGORIES = ('AC','FCR-TRANSFER','FCR-MINT','FCR-DESTROY','FCR-PAUSE','FCR-FREEZE')

def ident(prefix, value): return prefix+'_'+digest(value)[:20]

def write(path, value):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    data=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
    fd,tmp=tempfile.mkstemp(prefix='.'+path.name,dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as stream:stream.write(data);stream.flush();os.fsync(stream.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
    return hashlib.sha256(data).hexdigest()

@dataclass(frozen=True)
class Options:
    scope: str = 'AC'
    max_paths: int = 48
    input_target: int = 16384
    input_limit: int = 32768
    output_limit: int = 32768
    attempt_limit: int = 2
    feedback: bool = True
    prefix_depth: int = 2
    max_prefixes: int = 24
    max_actions: int = 64
    solver_timeout_ms: int = 3000
    seconds: float = 120
    def __post_init__(self):
        if self.scope not in ('AC','FCR'):raise ValueError('single_AC_or_FCR_task_required')
        if not 1<=self.max_paths<=96:raise ValueError('path_bound')
        if (self.input_target,self.input_limit,self.output_limit)!=(16384,32768,32768):raise ValueError('frozen_message_limits')
        if self.attempt_limit not in (1,2) or not 0<=self.prefix_depth<=2 or not 1<=self.max_prefixes<=64:raise ValueError('frozen_call_or_prefix_bound')
        if not 1<=self.max_actions<=256 or not 0<self.seconds<=900 or not 0<self.solver_timeout_ms<=20000:raise ValueError('frozen_investigation_bound')
    def record(self):return asdict(self)

```

## source/src/pr_next_joint/investigation/coverage.py

SHA-256 `c80fab5b05e2bb9936623e02b5f0b0b4b77654fe154ee87fc9cc808a7aeb69d5`

```python
"""Property dependency accounting, separate from findings and risk definitions."""
from .contracts import CATEGORIES
from pr_next_joint.frontend.path_ir import walk
from .protocol import category_scope
from .request_scope import coverage_facts, claim_entries, privileged_intervention
from .ledger import movements, unit_origin, native_only_position
from .roles import path_qualification
from .initial_state import domain, initial_for_lookup
from pr_next_joint.frontend.storage import selectors, keys, value_type

HARD = {'original_root_has_no_committing_path','original_root_net_effect_is_unchanged',
        'same_scope_actual_full_settlement','single_holder_scope_not_collective_pause',
        'same_control_has_no_dependency_on_declared_entry_effect',
        'matched_direct_effect_impossible_on_all_applicable_positions_and_paths',
        'authorization_acquisition_premise_refuted','expected_authorization_covers_all_applicable_paths',
        'source_supported_applicable_normal_authorization'}
UNKNOWN = {'source_identity_ambiguous_or_unresolved','minimum_source_inspection_not_executed',
           'unique_critical_external_guard_not_established','signature_dependent_success_not_verified',
           'E1_cumulative_numeric_bound_mapping_pending','financial_intervention_source_unresolved'}


def possible_properties(inv, entries):
    if inv.f.options.scope == 'AC':return ['AC']
    from .scope_relevance import directory
    from pr_next_joint.core import digest
    cache=inv.__dict__.setdefault('_directory_certificates',{})
    controls=_control_categories(inv);cats=set()
    for oid in entries:
        if oid not in inv.f.operations:continue
        token=(inv.semantics.dependency_identity([oid]),digest(inv.semantics.active_scope),oid)
        if token not in cache:cache[token]=directory(inv,oid,controls.get(oid,[]))
        cats.update(cache[token]['possible_categories'])
    return sorted(cats)


def _control_categories(inv):
    from pr_next_joint.core import digest
    from pr_next_joint.frontend.storage import selector_relation
    from .ledger import native_only_position
    from .key_roles import relation
    from .scope_relevance import potential_role
    stamp=(inv.f.identity,inv.semantics.rules.epoch)
    cached=getattr(inv,'_coverage_control_index',None)
    if cached and cached[0]==stamp:return cached[1]
    inv._coverage_control_routes={}
    f=inv.f;index={};writers={}
    for w in f.writes.values():
        token=(f.operations[w['operation']]['target'],w['raw']['path']['root'])
        writers.setdefault(token,[]).append(w)
    for use,entry in f.operations.items():
        for _,p in f.operation_paths(use,True):
            # Immutable structural index. Currency semantics are read by the local consumer.
            minus=[c for c in movements(inv.backend,use,p)['-'] if not (relation(c,f.lookup(use)) or {}).get('kind')=='authorization_quantity']
            if not minus:continue
            for control in selectors(p['guards']):
                typ=value_type(control,f.lookup(use)) or ''
                if typ!='bool' and not typ.startswith(('uint','int')):continue
                # Ledger sufficiency is not a distinct freeze/pause control.
                if any(selector_relation(control,c)=='same_shape' for c in minus):continue
                if (relation(control,f.lookup(use)) or {}).get('kind')=='authorization_quantity':continue
                for w in writers.get((entry['target'],control['root']),[]):
                    writer=w['operation']
                    if writer==use:continue
                    if selector_relation(w['raw']['path'],control)!='same_shape' or inv.graph._disjoint_keys(w['raw']['path'],control):continue
                    if potential_role(f,writer,f.paths[w['path']]['raw']):
                        from .dependencies import control_candidates
                        from .summary import holder
                        for cat in control_candidates(control,[holder(c,f.lookup(use)) for c in minus]):
                            index.setdefault(use,set()).add(cat);index.setdefault(writer,set()).add(cat)
                            inv.__dict__.setdefault('_coverage_control_routes',{}).setdefault((writer,cat),set()).add(use)
    inv._coverage_control_index=(stamp,index)
    return index








from .source_opinion import describe, simple_holder_grant
from .summary import local_delta
from pr_next_joint.core import digest

def basic_entry(inv,oid,rows,cat,effect_locations=None):
    """Read concrete declaration effects before assigning any category eligibility.

    Produces a detection opinion for this family, not an absence proof.
    In particular an opinion about one entry cannot read another target by proxy.
    """
    from .summary import local_delta,holder
    from .policy_binding import conjuncts
    from .source_opinion import office_use,quantity_forced_zero,identity_guard,role_ids
    from .initial_state import initial_for_lookup
    from pr_next_joint.frontend.path_ir import key
    from pr_next_joint.frontend.storage import value_type
    f=inv.f;lk=f.lookup(oid);entry=f.operations[oid]
    committing=[r for r in rows if r['committing']]
    if not rows:return 'unread','not_reviewed'
    if cat=='AC':
        from .source_opinion import handover,covered_delegation
        if handover(inv,oid,committing):return 'reviewed','nominee_acceptance'
        if covered_delegation(inv,oid,committing) and not any(r['effects'] for r in committing):return 'reviewed','covered_holder_grant'
        for r in committing:
            for w in r['ordered_writes']:
                cell=w['path']
                if not keys(cell) and value_type(cell,lk) in ('address','address payable') and office_use(inv,oid,cell):
                    guards=[g for v in r['guards'] for g in conjuncts(v)]
                    if not any(identity_guard(g,{cell['root']}) for g in guards):
                        return 'dispute','unassessed_role_change'
            if any('selfdestruct' in str(e.get('kind','')).lower() for e in r['effects']):
                return 'dispute','policy_missing'
        if not committing:return ('reviewed','no_effect_in_scope') if rows and inv.backend.complete(oid) else ('unread','not_reviewed')
        # This finite AC opinion concerns the examined paths and effects only.
        if simple_holder_grant(inv,oid,rows):return 'reviewed','covered_holder_grant'
        if any(r['effects'] or r['residuals'] for r in committing):return 'dispute','policy_missing'
        rules=inv.semantics.rules
        if any(e in getattr(rules,'source_duties',{}) and
               (effect_locations is None or tuple(rules.effects[e]['where'].get(k) for k in ('file','start','length')) in effect_locations)
               for e in rules.by_operation.get(oid,())):
            return 'dispute','policy_missing'
        return 'reviewed','source_task_reading'
    if cat=='FCR-DESTROY' and committing and not entry['gaps'] and all(not r['effects'] and not r['residuals'] for r in committing):
        from .scope_relevance import potential_role
        from pr_next_joint.frontend.storage import selector_relation
        local_reasons=[]
        for r in committing:
            raw=f.paths[r['path']]['raw']
            accounts=[(w,local_delta(w)) for w in r['ordered_writes'] if holder(w['path'],lk) is not None]
            if not potential_role(f,oid,raw):
                local_reasons.append('no_privileged_intervention');continue
            if not accounts:
                # A downstream exchange-rate or unit dependency needs its own
                # intervention comparison; a scalar write alone is not a debit.
                if not any(peer!=oid and not f.operations[peer]['generated_getter'] for w in r['ordered_writes']
                           for peer in inv.graph.access.get((entry['target'],w['path']['root']),{}).get('readers',())):
                    local_reasons.append('no_debit_in_scope');continue
                break
            debits=[(w,qty) for w,(sg,qty) in accounts if sg=='-']
            if len(debits)!=1:break
            w,qty=debits[0];cell=w['path'];account=holder(cell,lk)
            if account.get('kind')=='actual_sender':
                local_reasons.append('voluntary_holder_debit');continue
            credits=[(c,v) for c,(sg,v) in accounts if sg=='+' and selector_relation(c['path'],cell)=='same_shape']
            if len(accounts)==2 and len(credits)==1 and key(credits[0][0]['path'])==key(cell) and key(credits[0][1])==key(qty):
                local_reasons.append('same_position_restored');continue
            break
        else:
            if local_reasons:return 'reviewed',local_reasons[0] if len(set(local_reasons))==1 else 'locally_excluded_holder_loss'
    from .source_opinion import paid_credit
    if cat=='FCR-MINT' and committing:
        if all(paid_credit(inv,oid,r) for r in committing):return 'reviewed','ordinary_paid_credit'
    if cat in ('FCR-FREEZE','FCR-PAUSE'):
        linked=inv.__dict__.get('_coverage_control_routes',{}).get((oid,cat),set())
        if linked:
            has_unit=any(unit_origin(inv.backend,use,cell) for use in linked for _,branch in f.operation_paths(use,True) for cell in movements(inv.backend,use,branch)['-'])
            return 'dispute','scope_missing' if has_unit else 'source_unit_missing'
        return 'reviewed','source_task_reading'
    if cat=='FCR-MINT':
        writers={w['path']['root'] for r in committing if role_ids(inv,oid,r) for w in r['ordered_writes']}
        if writers:
            for rid in writers:
                for use in inv.graph.access.get((entry['target'],rid),{}).get('readers',()):
                    if use==oid:continue
                    for branch in f.summaries.rows(use):
                        buy=paid_credit(inv,use,branch)
                        if buy and any(c['root']==rid for c in selectors(local_delta(buy)[1])):
                            return 'dispute','scope_missing'
    from .roles import effective_roots
    from .source_opinion import impossible_role
    for r in committing:
        qualified = role_ids(inv, oid, r)
        # A caller guard without a verified grant chain is still a live mint
        # candidate. A rejected refinement alone supplies no negative evidence.
        if not qualified and not (cat == 'FCR-MINT' and
                any(effective_roots(g, lk.nodes.keys()) for g in r['guards'])):
            continue
        from .scope_relevance import nonfinancial
        effects=[(w,*local_delta(w)) for w in r['ordered_writes']
                 if holder(w['path'],lk) is not None and not nonfinancial(inv.backend,oid,w['path'])]

        guards=[g for t in r['guards'] for g in conjuncts(t)]
        for w,sign,amount in effects:
            if effect_locations is not None and tuple(w['source'].get(k) for k in ('file','start','length')) not in effect_locations:continue
            if sign not in ('+','-') or not amount:continue
            ac=holder(w['path'],lk);others=[(ow,os,oq) for ow,os,oq in effects if ow['path']['root']==w['path']['root'] and os!=sign]
            if quantity_forced_zero(guards,amount,lk):continue
            matched=[ow for ow,os,oq in others if key(oq)==key(amount)]
            if not qualified:
                if sign != '+' or paid_credit(inv, oid, r) or impossible_role(inv, oid):
                    continue
                from pr_next_joint.frontend.storage import selector_relation
                same_family = [(ow, os, oq) for ow, os, oq in effects
                               if selector_relation(w['path'], ow['path']) == 'same_shape']
                if len(same_family) == 2 and any(os == '-' and key(oq) == key(amount)
                                                for _, os, oq in same_family):
                    continue
                return 'dispute', 'mint_role_provenance_unresolved'
            reason='scope_missing' if unit_origin(inv.backend,oid,w['path']) else 'source_unit_missing'
            if cat=='FCR-MINT' and sign=='+' and not matched:return 'dispute',reason
            if cat=='FCR-TRANSFER' and sign=='-' and matched and ac.get('kind')!='actual_sender':
                return 'dispute',reason
            if cat=='FCR-DESTROY' and sign=='-' and ac.get('kind')!='actual_sender' and not matched:
                return 'dispute',reason
    return 'reviewed','source_task_reading'


def obligation_scope(inv, assessments, blocked):
    """Record actual source readings, independent of optional proof completion."""
    categories = tuple(CATEGORIES[1:]) if inv.f.options.scope == 'FCR' else ('AC',)
    manifest=inv.initial_manifest or {}
    delivered=set(manifest.get('expanded_operations',()))-set(manifest.get('partially_expanded_operations',()))
    by_entry={}
    local={}
    gaps=[]
    normal=[]
    agenda=[]
    scope_skips=set()
    seen_gaps=set()
    open_cats=set()
    def gap(oid, cats, reason, issues=()):
        affected=sorted(set(cats)&set(categories))
        if not affected:return
        token=(oid,tuple(affected),reason)
        if token in seen_gaps:return
        seen_gaps.add(token);open_cats.update(affected)
        obj=inv.f.operations.get(oid,{})
        gaps.append(dict(id='gap_'+digest(token)[:16],target=obj.get('target'),operations=[oid] if oid else [],
                         location=obj.get('source',{}),closed=False,affected_categories=affected,
                         reason=reason,issues=list(issues),explanation=describe(affected[0],reason)))
    for qid,q in inv.issues.items():
        a=assessments[qid];cat=a.get('category')
        status=a['scope'].get('route_status')
        decision=a['scope']['decision']
        root=inv.root(q)
        if status=='superseded':continue
        record={'issue':qid,'category':cat,'state':decision['status'],'reason':decision['reason'],
                'closed':decision['status'] in ('risk','normal','excluded'),'entries':[root] if root else [],
                'affected_categories':[]}
        exact=q['current'].get('_scope_effects') or q.get('effect_scope') or []
        by_location={tuple(r.get(k) for k in ('file','start','length')) for r in decision.get('locations',())}
        record['effects']=sorted(set(exact) or {e for e in inv.semantics.rules.by_operation.get(root,()) if
            tuple(inv.semantics.rules.effects[e]['where'].get(k) for k in ('file','start','length')) in by_location})
        local[qid]=record
        if root:by_entry.setdefault(root,[]).append(record)
        if root is None and q['current'].get('assessment')=='risk':
            for candidate in q.get('binding',{}).get('operations',()):
                gap(candidate,category_scope(q['current'],inv.f.options.scope),'core_mismatch',[qid])
    checked=0;obligations=[]; basic_cache=inv.__dict__.setdefault('_basic_entry_opinions',{})
    rules=inv.semantics.rules
    expanded_all=manifest.get('mode')=='complete_source'
    for oid,entry in inv.f.operations.items():
        cats=set(categories)
        states={};related=by_entry.get(oid,[])
        local_counts=[x for x in related if x['reason']=='scoped_counter' and x['state']=='normal']
        rows=inv.f.summaries.rows(oid,False)
        # A generated getter is still a compiler declaration. Inspect real rows or that declaration.
        read=bool(rows or entry['generated_getter']) and oid not in rules.incomplete
        cache=inv.__dict__.setdefault('_scope_candidates',{})
        if categories!=('AC',):
            if oid not in cache and inv.program_remaining()<=0:
                gap(oid,categories,'not_reviewed');continue
            stamp=(inv.semantics.dependency_identity([oid]),digest(inv.semantics.active_scope))
            if cache.get(oid,(None,))[0]!=stamp:
                cache[oid]=(stamp,set(possible_properties(inv,{oid})))
            cats=cache[oid][1]
        explicit=set(x['category'] for x in related if x['category'] in categories)
        if any(x['reason'] in ('conflicting_scoped_meanings','source_unit_missing') and not x['category'] for x in related):
            for x in related:
                if x['reason'] in ('conflicting_scoped_meanings','source_unit_missing'):
                    rules=inv.semantics.rules;q=inv.issues[x['issue']]
                    for e in (rules.disputed_effects(q) if x['reason']=='conflicting_scoped_meanings' else rules.route_scopes(q)):
                        w=inv.semantics.rules.effects[e].get('write')
                        if w is None:continue
                        sign,_=local_delta(w)
                        explicit.update(['FCR-MINT'] if sign=='+' else ['FCR-DESTROY','FCR-TRANSFER'] if sign=='-' else [])
                        gap(oid,['FCR-MINT'] if sign=='+' else ['FCR-DESTROY','FCR-TRANSFER'] if sign=='-' else [],x['reason'],[x['issue']])
        relevant=cats|explicit
        committed=[r for r in rows if r['committing']]
        opaque=any(r['residuals'] or r['flow']=='truncated' or any(e.get('kind')=='dangerous_external_call' for e in r['effects']) for r in rows) or bool(entry['gaps'])
        no_effect=read and not opaque and (entry['generated_getter'] or not any(r['ordered_writes'] or r['effects'] for r in committed))
        unresolved_key_only=bool(rows) and not entry['gaps'] and not any(r['effects'] or r['flow']=='truncated' for r in rows) and all(
            x.get('reason')=='multiple_address_keys_need_source_holder_binding' for r in rows for x in r['residuals'])
        frontier=any(r['flow']=='truncated' for r in rows) or any(g.get('kind') in ('path_extraction','source_expression_limit','dependent_source_expression_limit') for g in entry['gaps'])
        opaque_domain=frontier or any(call['mode']=='DELEGATECALL' and call['unresolved_implementation']
            for call in inv.f.call_summaries.rows.values() if call['operation']==oid)
        if opaque_domain:relevant.update(categories)
        has_view=expanded_all or oid in delivered
        for cat in sorted(categories):
            records=[x for x in related if x['category']==cat]
            active=[x for x in records if not inv.issues[x['issue']]['current'].get('_host_source_question') or
                    x['reason'] in ('conflicting_scoped_meanings','source_unit_missing','policy_scope_unsubstantiated','policy_effect_unresolved','holder_consent_basis_unresolved','unexpanded_source_dependency') or
                    inv.issues[x['issue']]['current'].get('_semantic_consumer') and x['reason'] in ('policy_missing','external_dependency')]
            settled=[x for x in records if x['state'] in ('normal','excluded','risk')]
            covered={e for x in settled for e in x['effects']}
            outstanding=inv.semantics.rules.by_operation.get(oid,set())-covered
            decisive=[]
            for rec in active:
                if rec['state']!='open':continue
                model_issue=inv.issues[rec['issue']]
                prop=model_issue.get('property') or {}
                finance_q=any(s.get('kind')=='financial_consent' and s.get('quantity_scope') for s in prop.get('semantic_questions',[]))
                measured_unbound=any(
                    e.get('property_identity')==prop.get('id') and any(x.get('reason')=='holder_authorization_quantity_basis_unresolved' for x in e.get('local_errors',[]))
                    for label in model_issue['evidence'] for e in [inv.evidence[label]])
                consent_active=any(x.get('meaning')=='net_request_with_fee' and x.get('quantity_scope') for x in prop.get('consent_rows',[]))
                if cat in ('FCR-DESTROY','FCR-TRANSFER') and (finance_q or measured_unbound or consent_active) and rec['reason']=='scope_missing':
                    decisive.append(dict(rec,reason='holder_consent_basis_unresolved'));continue
                if rec['reason'] not in (
                    'conflicting_scoped_meanings','source_unit_missing','policy_effect_unresolved','external_dependency',
                    'policy_missing','policy_scope_unsubstantiated','revised_policy_not_read','holder_consent_basis_unresolved','unexpanded_source_dependency'):continue
                if not rec['effects'] or not set(rec['effects'])<=covered:decisive.append(rec)
            base_status,base_reason='unread','not_reviewed'
            read_effects=set(rules.by_operation.get(oid,()))
            local_opaque=opaque and (opaque_domain or cat in relevant and
                (not outstanding or any(inv.f.call_summaries.effect_dependencies(r,rules.effects[e])
                 for e in outstanding for r in rows if rules.effects[e].get('path')==r['path'] or r['path'] in rules.effects[e].get('branches',{}))))
            local_complete=not outstanding and bool(covered) and not opaque_domain
            # basic_entry reasons about the actual writes and program guards. It does
            # not consume a mutable normative consent, which is applied separately below.
            from .source_opinion import reading_version
            depend=reading_version(inv,[oid],cat) if (oid,cat) in inv.__dict__.get('_coverage_control_routes',{}) else None
            basic_key=(oid,cat,tuple(sorted(outstanding)),stamp if categories!=('AC',) else None,depend)
            from .scope_relevance import detached_holder_switch
            detached=(cat=='FCR-FREEZE' and read and detached_holder_switch(inv,oid))
            if detached:
                base_status,base_reason='reviewed','detached_local_holder_switch'
            elif read and no_effect:
                base_status,base_reason='reviewed','no_effect_in_scope'
            elif read and cat=='FCR-MINT' and not opaque and any(n.get('kind')=='transaction_value' for r in committed for w in r['ordered_writes'] for n in walk(w['value'])) and basic_entry(inv,oid,rows,cat)==('reviewed','ordinary_paid_credit'):
                base_status,base_reason='reviewed','ordinary_paid_credit'
            elif read and cat not in relevant and not opaque_domain:
                base_status,base_reason='reviewed','necessary_effect_absent'
            elif read and local_complete:
                base_status,base_reason='reviewed','effect_range_decided'
            elif not has_view and not local_complete:
                base_reason='source_context_missing'
            elif local_opaque and not (unresolved_key_only and (cat not in cats or simple_holder_grant(inv,oid,rows))):
                base_reason='external_dependency'
            elif read and (basic_key in basic_cache or inv.program_remaining()>0):
                if basic_key not in basic_cache:
                    # Keep companion writes and guards as dependencies of the remaining effect.
                    locs=None
                    if covered and outstanding:
                        locs={tuple(rules.effects[e]['where'].get(k) for k in ('file','start','length')) for e in outstanding}
                    basic_cache[basic_key]=basic_entry(inv,oid,rows,cat,locs)
                base_status,base_reason=basic_cache[basic_key]
            elif not read:base_reason='source_context_missing'
            reason=base_reason if base_status!='reviewed' else None
            if decisive and not detached and not no_effect and (cat in relevant) and base_reason!='nominee_acceptance':
                reason=decisive[0]['reason']
            if reason:
                gap(oid,[cat],reason,[x['issue'] for x in decisive])
                effects={e for record in decisive for e in record['effects']} or outstanding
                states[cat]={'state':'open','basis':reason,'effect_ids':sorted(effects)}
            else:
                states[cat]={'state':'reviewed','basis':base_reason}
            identity=(oid,cat,tuple(sorted(outstanding)))
            if reason in ('scope_missing','source_unit_missing','policy_missing','unassessed_role_change') and not local_opaque and identity not in scope_skips:
                agenda.append({'operation':oid,'category':cat,'effects':sorted(outstanding),'dependency':reason})
                scope_skips.add(identity)
        if any(s['state']=='reviewed' for s in states.values()) or any(rec['closed'] for rec in related):checked+=1
        affected=[c for c in categories if states[c]['state']=='open']
        obligations.append({'id':'obligation_'+digest([inv.f.identity,entry['target'],oid])[:20],
            'target':entry['target'],'operations':[oid],'location':entry['source'],'possible_categories':sorted(relevant),'source_candidate_categories':sorted(cats),'bound_question_categories':sorted(explicit),'category_states':states,
            'closed':not affected,'affected_categories':affected,'entry_states':[{'operation':oid,'states':{c:states[c]['state'] for c in categories}}]})
    if not checked:gap(None,categories,'not_reviewed')
    eligible=sorted(set(categories)-open_cats)
    for cat in eligible:
        if not any(x['category']==cat and x['state']=='risk' for x in local.values()):
            matched=[r for r in local.values() if r['category']==cat and r['state'] in ('normal','excluded')]
            reasons=sorted({r['reason'] for r in matched})
            patterns=sorted({s['category_states'][cat]['basis'] for s in obligations if cat in s['category_states'] and s['category_states'][cat].get('basis')})
            explanation=describe(cat,reasons[0] if reasons else patterns[0] if len(patterns)==1 else 'source_task_reading')
            normal.append({'category':cat,'reason':'source_task_reading','applied_reasons':reasons or patterns,
                           'effects':sorted({e for r in matched for e in r['effects']}),'explanation':explanation})
    return {'schema':'source-category-decision-r1','request_scope':manifest.get('requested_reading'),
            'whole_reading_eligible':bool(checked and not open_cats),
            'negative_eligible_categories':eligible,'known_category_gaps':gaps,'category_readings':normal,
            'source_local_scopes':local,'obligations':obligations,'neutral_scope_scan_executed':bool(checked),
            'basic_source_entries_read':checked,'source_opinion_available':bool(checked),'refinement_requests':agenda,
            'delivery_and_model_declaration_are_not_completion':True}

```

## source/src/pr_next_joint/investigation/decision_output.py

SHA-256 `cd193e366ad47593945dfa3006664329bff721d9718705927f2d840a60026a5b`

```python
"""Fixed decision-only output contract; no detailed-output switch.

The verifier does not extract assignments. This independent output boundary
keeps classifications, source locations, bounded statuses, coverage and cost
receipts. Solver problems, ordered frames and raw model bodies are not saved.
"""
import copy
import re
from pr_next_joint.core import digest

PROFILE = 'risk_decision_only_v1'

def code(value, fallback='unclassified_diagnostic'):
    return value if isinstance(value,str) and re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.:-]{0,159}',value) and not re.search(r'0x[0-9a-fA-F]{8,}',value) else fallback

def codes(values):
    return [code(v) for v in values if isinstance(v,str)] if isinstance(values,list) else []

def location(value):
    if not isinstance(value,dict):return {}
    out={'file':value['file']} if isinstance(value.get('file'),str) else {}
    out.update({k:value[k] for k in ('start','length','ast_id','line','column') if type(value.get(k)) is int})
    return out

def receipt(value,purpose):
    return {'profile':PROFILE,'purpose':purpose,'content_sha256':digest(value),'body_retained':False}

def safe_issue_id(value):
    """Source-visible model IDs may contain arbitrary strings; keep only inert IDs on disk."""
    if isinstance(value,str) and re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.:@-]{0,90}',value) and not re.search(r'0x[0-9a-f]{8,}|[a-f0-9]{40,}',value,re.I):
        return value
    return 'issue_'+digest(value)[:20]

def diagnostic(row):
    if not isinstance(row,dict):return {'reason':code(row),'detail_sha256':digest(row)}
    previous=row.get('detail_sha256')
    out={'reason':code(row.get('reason',row.get('kind'))),'detail_sha256':previous if isinstance(previous,str) and re.fullmatch('[0-9a-f]{64}',previous) else digest(row)}
    for k,allowed in {'stage':{'initial','protocol_recovery','focused_revision'},'list':{'issues','answers','annotations','policies','reviewed','hypotheses'},
                      'field':{'on','effect','meaning','ref','role','subject','basis','question','assessment','category','action'},
                      'subreason':{'field_absent','wrong_field_type','invalid_locator','outside_facet_vocabulary','missing_source_reason','undisplayed_reference','source_binding'},
                      'actual_type':{'str','list','dict','NoneType','bool','int','float'}}.items():
        if row.get(k) in allowed:out[k]=row[k]
    field_path=row.get('field_path')
    if isinstance(field_path,str) and re.fullmatch(r'[a-z_]{1,32}(?:\.[a-z_]{1,32}|\[\])?',field_path):
        out['field_path']=field_path
    ordinal=row.get('index',row.get('item',row.get('answer')))
    if type(ordinal) is int:out['index']=ordinal
    if type(row.get('value_length')) is int:out['value_length']=row['value_length']
    if isinstance(row.get('value_sha256'),str) and re.fullmatch('[0-9a-f]{64}',row['value_sha256']):out['value_sha256']=row['value_sha256']
    if 'list' in out:
        out['contract']='scoped_json_r2'
        if 'field' in out:out['expected_type']='str'
    if 'issue' in row:out['issue']=safe_issue_id(row['issue'])
    if 'category' in row:out['category']=code(row['category'])
    if isinstance(row.get('source'),dict):out['source_location']=location(row['source'])
    return out

def context_summary(value):
    out=receipt(value,'source_delivery_and_capacity')
    out.update({k:value[k] for k in ('input_tokens','input_target','input_limit','output_limit') if type(value.get(k)) is int})
    if isinstance(value.get('messages_sha256'),str):out['messages_sha256']=value['messages_sha256']
    if 'registered_sensitive_effects' in value:
        out['registered_sensitive_effects']=value['registered_sensitive_effects']
        out['displayed_effect_handles']=[code(h) for h in value.get('displayed_effect_handles',())]
    if 'omitted_effect_handles' in value:out['omitted_effect_handles']=[code(h) for h in value['omitted_effect_handles']]
    if 'typed_index' in value:out['typed_cards']=len(value['typed_index'])
    if 'shown_supports' in value:out['shown_supports']=len(value['shown_supports'])
    if 'semantic_supports_omitted' in value:out['omitted_supports']=value['semantic_supports_omitted']
    out['sent_question_bindings']=[{'display_sha256':v['display'],'entity_sha256':v['entity'],'consumers':1+len(set(value.get('shared_question_consumers',{}).get(v['issue'],()))-{v['issue']})} for v in value.get('semantic_wire',{}).values()]
    if value.get('mode'):out['mode']=code(value['mode'])
    if value.get('source_mode'):out['source_mode']=code(value['source_mode'])
    out['source_file_count']=len(value.get('complete_source_files',()))
    out['omission_reasons']=[code(x.get('reason')) for x in value.get('unexpanded_feedback_issues',())]
    for k in ('selected_issues','unexpanded_feedback_issues','omitted_operations','selected_operations'):
        if isinstance(value.get(k),(dict,list)):out[k+'_count']=len(value[k])
    return out

def property_summary(prop):
    if not isinstance(prop,dict):return None
    out={k:copy.deepcopy(prop[k]) for k in ('id','category','original_category','domain','operation',
         'semantic_version','task','property_family') if k in prop and isinstance(prop[k],(str,int,bool))}
    out['content_sha256']=digest(prop)
    return out

def scope_summary(scope):
    if not isinstance(scope,dict):return {}
    out={'scope_sha256':digest(scope)}
    for k in ('route_status','deployment_reachability_proved','entire_contract_safety_proved','analysis_domain','domain'):
        if k in scope and isinstance(scope[k],(str,bool)):out[k]=scope[k]
    if 'compiled_property' in scope:out['compiled_property']=property_summary(scope['compiled_property'])
    if 'decision' in scope:
        d=scope['decision']
        out['decision']={'status':code(d['status']),'reason':code(d['reason']),
                         'explanation':d['explanation'],'locations':[location(x) for x in d.get('locations',[])],
                         **{k:[code(i) for i in d.get(k,[])] for k in ('effects','rules','supports','facts','meanings','origins')}}
        for k in ('application_location','causal_root'):
            if d.get(k):out['decision'][k]=location(d[k])
        if d.get('source_edge_ids'):
            out['decision']['source_edge_ids']=codes(d['source_edge_ids'])
        if card := d.get('audit_card'):
            out['decision']['audit_card'] = {
                'kind':code(card['kind']), 'check':code(card['check']),
                'bound_effects':codes(card['bound_effects']),
                'source_relation_independent':bool(card['source_relation_independent']),
                'semantic_reading_used':bool(card['semantic_reading_used'])}
        if rel:=d.get('source_relation'):
            out['decision']['source_relation']={'family':code(rel['family']), 'duty':code(rel['duty']),
                                               'support_location':location(rel['support_location'])}
        if d.get('holder_family'):
            out['decision']['holder_family']={k:code(v) for k,v in d['holder_family'].items()}
        if d.get('opinion_source'):out['decision']['opinion_source']=code(d['opinion_source'])
        if d.get('protected_use'):out['decision']['protected_use']=location(d['protected_use'])
        if d.get('productive_use'):out['decision']['productive_use']=location(d['productive_use'])
        if d.get('basis_probe'):out['decision']['basis_probe']=code(d['basis_probe'])
        if d.get('conditional_agent'):
            alt=d['conditional_agent'];out['decision']['conditional_agent']={'scope':code(alt['scope']),'use':location(alt['use']),
                'requires_prior_holder_grant':True,'requires_exempt_spender':True,'availability':code(alt['availability'])}
    return out

def assessment_summary(value):
    return {'reportable':value.get('reportable') is True,'category':value.get('category'),
            'reasons':codes(value.get('reasons',[])),'scope':scope_summary(value.get('scope',{}))}

def query_summary(q):
    d=q.get('details',{})
    out={k:q[k] for k in ('id','label','answer','formula_sha256','bounded_condition_confirmed') if k in q}
    out.update(evidence_kind='bounded_condition_check_without_assignment_extraction',
               condition_identity=digest(d),model_extracted=False,formula_saved=False)
    keys=('property_validated','intermediate_value_carried','measurement_only','same_request','effect_required','new_authority_required',
          'downstream_effect_required','acquisition_use_required','baseline_commit_not_assumed',
          'no_universal_gross_allowance_policy','all_productive_paths_checked','all_continuations_exact',
          'original_all_positive_amount_obligation_preserved')
    criteria={k:d[k] for k in keys if type(d.get(k)) is bool}
    if d.get('corresponding_same_ledger_credit'):criteria['corresponding_same_ledger_credit']=True
    for k in ('category_hypothesis','property_identity'):
        if k in d:criteria[k]=code(d[k])
    binding=q.get('rebound_from')
    if binding:out['math_reuse']={k:v if k in ('math_key','binding_sha256') and re.fullmatch('[a-f0-9]{64}',v) else code(v) for k,v in binding.items() if isinstance(v,str)}
    if d.get('beneficiary_rule')=='controlled_or_self_only':criteria['beneficiary_rule']='controlled_or_self_only'
    out['criteria']=criteria
    for name,key in [('credential_status','credential'),('hash_status','hash_confirmation')]:
        out[name]={k:code(v) for k,v in q.get(key,{}).items() if k in ('status','reason')}
    cert=q.get('exclusion_certificate')
    if isinstance(cert,dict):
        out['exclusion_check']={k:cert[k] for k in ('answer','formula_ref','all_runtime_states_overapproximated',
            'excludes_only_this_formula','positive_result_usable') if k in cert}
    return out

def evidence_summary(evidence):
    return {label:{'kind':code(e.get('kind')),'content_sha256':digest(e),
        'queries':[query_summary(q) for q in e.get('queries',[])],
        'local_errors':[diagnostic(x) for x in e.get('local_errors',[])],
        'independent_use_checks':[{k:c[k] for k in ('status','supports_takeover') if k in c}
                                 for c in e.get('independent_use_checks',[])]}
        for label,e in evidence.items()}

def coverage_row(row):
    out={k:copy.deepcopy(row[k]) for k in ('id','target','closed','affected_categories','source_candidate_categories','bound_question_categories') if k in row}
    if row.get('operations'):out['operations']=codes(row['operations'])
    if row.get('location'):out['location']=location(row['location'])
    out['category_states']={c:{'state':code(s.get('state')),'basis':code(s.get('basis')),'detail_sha256':digest(s)}
                            for c,s in row.get('category_states',{}).items()}
    stages={'source_unit_missing':'unit_binding','not_reviewed':'source_reading','source_context_missing':'source_display','external_dependency':'external_effect','holder_consent_basis_unresolved':'authorized_quantity','policy_missing':'policy_binding','scope_missing':'effect_check'}
    for cat,item in out['category_states'].items():
        if item['basis'] in stages:item['first_observable_dependency']=stages[item['basis']]
        effects=row['category_states'][cat].get('effect_ids',[])
        if effects:
            item['open_effects']=codes(effects[:8])
            item['other_open_effect_count']=max(0,len(effects)-8)
    return out

def coverage_summary(value):
    return {'schema':'source-category-public-r1','whole_reading_eligible':value.get('whole_reading_eligible') is True,
        'negative_eligible_categories':copy.deepcopy(value.get('negative_eligible_categories',[])),
        'obligations':[coverage_row(row) for row in value.get('obligations',[])],
        'known_category_gaps':[dict(coverage_row(row),reason=code(row['reason']),location=location(row.get('location')),explanation=row['explanation']) for row in value.get('known_category_gaps',[])],
        'basic_source_entries_read':value.get('basic_source_entries_read',0),
        'category_readings':copy.deepcopy(value.get('category_readings',[])),
        'source_opinion_available':bool(value.get('source_opinion_available')),
        'neutral_scope_scan_executed':value.get('neutral_scope_scan_executed') is True,
        'content_sha256':digest(value),'delivery_and_model_declaration_are_not_completion':True}

def semantic_summary(record):
    out=receipt(record,'source_bound_semantic_interpretations')
    out['scoped_support']=copy.deepcopy(record.get('scoped_support',{}))
    out['answer_dispositions']=copy.deepcopy(record.get('answer_dispositions',[]))
    out['financial_consents']=[{'meaning':code(c.get('meaning')),'identity':digest(c)} for c in record.get('financial_consents',[])]
    return out

def public_report(report):
    if report.get('output_profile')==PROFILE:return copy.deepcopy(report)
    keep=('method','program_identity','task','options','effective_investigation_parameters','implementation_sha256','main_finding_ids',
          'additional_finding_ids','unresolved_mapping_ids','model_analysis_available','prediction_basis_available',
          'unresolved_category_judgments','prediction_frozen_before_gold','scoring_performed','timing')
    out={k:copy.deepcopy(report[k]) for k in keep if k in report}
    out.update(output_profile=PROFILE,replay_material_generated=False,concrete_execution_performed=False,
               risk_absence_statement='No risk detected in analyzed scope is not proof of safety.')
    out['prediction_basis_issues']=[safe_issue_id(x) for x in report.get('prediction_basis_issues',[])]
    out['findings']=[]
    for f in report.get('findings',[]):
        row={k:copy.deepcopy(f[k]) for k in ('id','category','target','operation','comparison_scope','evidence_refs','issue_ids') if k in f}
        row['issue_ids']=[safe_issue_id(i) for i in row.get('issue_ids',[])]
        row.update(root_location=location(f.get('root_location')),evidence_level=code(f.get('evidence_level'),'source_prediction'),
                   evidence_scope=scope_summary(f.get('scope',{})),
                   explanation=f['scope']['decision']['explanation'])
        out['findings'].append(row)
    out['inspection_records']=[{'id':safe_issue_id(r['id']),'version':r.get('version'),
        'compiled_property':property_summary(r.get('compiled_property')),
        'assessment_result':assessment_summary(r['assessment_result']),
        'evidence_refs':copy.deepcopy(r.get('evidence_refs',[]))} for r in report.get('inspection_records',[])]
    d=report['diagnostics']
    out['diagnostics']={'issues':[diagnostic(x) for x in d.get('issues',[])],
        'unexecuted_actions':len(d.get('unexecuted_actions',[])),
        'program_gaps':[diagnostic(x) for x in d.get('program_gaps',[])],
        'source_context_scope':context_summary(d.get('source_context_scope',{})),
        'no_finding_is_not_contract_safety':True,'E1_not_formal_FREEZE':True}
    task=report.get('task_analysis',{})
    out['task_analysis']={k:task[k] for k in ('model_analysis_available','empty_response_present','fixture_analysis_available','usable_task_opinion',
        'explicit_empty_task_reading','local_judgment_not_global_safety','unexecuted_actions') if k in task}
    out['task_analysis']['reading_scope']=coverage_summary(task.get('reading_scope',{}))
    usage=copy.deepcopy(report.get('usage',{}))
    for row in usage.get('attempts',[]):
        if 'normalization_diagnostics' in row:row['normalization_diagnostics']=[diagnostic(x) for x in row['normalization_diagnostics']]
        if 'reason' in row:row['reason']=code(row['reason'])
    out['decision_sha256']=digest([out['findings'],out['inspection_records'],out['task_analysis']['reading_scope'],out['unresolved_category_judgments']])
    out['usage']=usage
    p=report.get('provenance',{})
    out['provenance']={'structural_references':dict(p.get('structural_references',{})),'refinement_decisions':[dict(row,issue=safe_issue_id(row['issue']) if row.get('issue') else None) for row in p.get('refinement_decisions',[])],'shared_source_facts':{k:[safe_issue_id(i) for i in ids] for k,ids in p.get('shared_source_facts',{}).items()},'action_count':len(p.get('actions',[])),'revision_count':len(p.get('revisions',[])),
        'evidence_labels':copy.deepcopy(p.get('evidence_labels',[])),'cache_hits':p.get('cache_hits',0),
        'feedback_trace':[{k:row[k] for k in ('issue','selected','sent','parsed','consumed','simulated','submission_state','changed_finding','semantic_rows_received','semantic_rows_accepted','accepted_other_scopes','other_scope_accepted_rows','answered_unresolved') if k in row}
                          for row in p.get('feedback_trace',[])]}
    for row,trace in zip(out['provenance']['feedback_trace'],p.get('feedback_trace',[])):
        row['issue']=safe_issue_id(row['issue'])
        if trace.get('reason') in ('same_effect_authorization_already_decided',
                'existing_source_and_property_already_support_same_uncontested_claim',
                'same_property_source_or_complete_domain_refutation_already_closes_this_scope'):
            row['reason']=trace['reason']
    out['provenance']['computation_reuse']=copy.deepcopy(p.get('computation_reuse',{}))
    if 'solver_resource' in report:out['solver_resource']=copy.deepcopy(report['solver_resource'])
    return out

```

## source/src/pr_next_joint/investigation/dependencies.py

SHA-256 `671f9c840b7b9cb93bc3edf5f0d910dae6f1ca2bdafaf07e12b320a3fbca3d27`

```python
"""Read-only, target-specific def/use index over the frontend's resolved paths.

The index relates state definitions to expressions. An edge never establishes
a permission, an asset type, a committed financial effect or reachability.
"""
from collections import defaultdict, deque

from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key
from pr_next_joint.frontend.storage import keys, selectors, selector_relation
from pr_next_joint.frontend.path_ir import walk


def may_alias(a,b):
    shape=selector_relation(a,b)
    if shape=='disjoint':
        return False
    for left,right in zip(keys(a),keys(b)):
        if left.get('kind')==right.get('kind')=='literal' and left.get('value')!=right.get('value'):
            return False
    return True


def control_candidates(control,debits):
    """Candidate scope depends on the actual outgoing holder, including constant-index switches."""
    if not debits:return set()
    idx=keys(control)
    holders={key(x) for x in debits if x is not None}
    if any(key(k) in holders for k in idx):
        return {'FCR-FREEZE'}
    request_dependent=any(v.get('kind') in ('actual_sender','parameter','transaction_origin') for v in walk(control))
    if not request_dependent:
        return {'FCR-PAUSE'}
    return {'FCR-PAUSE','FCR-FREEZE'}


class Dependencies:
    def __init__(self,summaries):
        self.summaries=summaries
        self.readers=defaultdict(list)
        self.defs=defaultdict(list)
        self.rows={}
        self.forward_cache={}
        self.expressions={}
        self.amounts={}
        self.remaining=None
        for pid,row in summaries.paths.items():
            if not row['committing']:
                continue
            target,oid=row['target'],row['operation']
            for seq,write in enumerate(row['ordered_writes']):
                cell=write['path']
                self.defs[oid].append(cell)
                self.add(pid,target,oid,'value',write['value'],cell,seq,write.get('source'))
                from .summary import local_delta
                sign,amount=local_delta(write)
                if amount is not None:
                    self.add(pid,target,oid,'amount',amount,cell,seq,write.get('source'))
                self.add(pid,target,oid,'key',keys(cell),cell,seq,write.get('source'))
            for seq,guard in enumerate(row['guards']):
                self.add(pid,target,oid,'guard',guard,None,seq,None)
            if row['return_value']:
                self.add(pid,target,oid,'return',row['return_value'],None,0,None)
        self.identity=digest(sorted(self.rows))

    def add(self,pid,target,oid,kind,expr,cell,seq,source):
        # A constant expression defines a value but introduces no state edge.
        def read_values(term):
            if isinstance(term,dict):
                if term.get('kind')=='storage':
                    yield term
                    # Subscripts select the object. Keep them as address/key
                    # dependencies rather than pretending that they set its quantity.
                    if kind!='key':
                        self.add(pid,target,oid,'key',keys(term),cell,seq,source)
                    return
                for k,v in term.items():
                    if not k.startswith('_source_'):yield from read_values(v)
            elif isinstance(term,list):
                for v in term:yield from read_values(v)
        reads={key(v):v for v in read_values(expr)}
        if not reads:
            return
        expr_id=digest(expr)
        self.expressions.setdefault(expr_id,expr)
        for value in reads.values():
            edge={'path':pid,'target':target,'use':oid,'kind':kind,'read':value,'writes':cell,
                  'position':seq,'expression':expr_id,'source':source}
            token=digest(edge)
            if token not in self.rows:
                self.rows[token]=edge
                self.readers[(target,value['root'])].append(token)

    def forward(self,oid):
        if oid in self.forward_cache:
            return self.forward_cache[oid]
        source=self.summaries.operations[oid]
        target=source['target']
        initial={key(c):c for c in self.defs.get(oid,())}
        queue=deque(initial.values());queued=set(initial)
        seen=set();edges=set();via=defaultdict(set);residuals={}
        stopped=False
        while queue:
            if self.remaining is not None and self.remaining()<=0:
                stopped=True;break
            cell=queue.popleft()
            identifier=key(cell)
            if identifier in seen:continue
            seen.add(identifier)
            for edge_id in self.readers.get((target,cell['root']),()):
                edge=self.rows[edge_id]
                if not may_alias(cell,edge['read']):continue
                edges.add(edge_id)
                via[edge['use']].add(edge['kind'])
                if edge['writes'] is not None and edge['kind']!='key':
                    next_key=key(edge['writes'])
                    if next_key not in queued:
                        queue.append(edge['writes']);queued.add(next_key)
                # Only residuals on actual dependent operations are carried.
                row=self.summaries.paths[edge['path']]
                for residual in row['residuals']:
                    residuals[digest([edge['path'],residual])]=[edge['path'],residual]
        for residual in source['residuals']:
            residuals[digest([oid,residual])]=[oid,residual]
        answer={'origin':oid,'target':target,'edge_ids':sorted(edges),
                'uses':{use:sorted(kinds) for use,kinds in sorted(via.items()) if use!=oid},
                'visited_cells':len(seen),'residuals':list(residuals.values()),
                'precision':'may_over_resolved_paths','fixed_point_over_indexed_definitions':not stopped,
                'whole_source_closed':False}
        if stopped:
            answer['residuals'].append({'reason':'dependency_worklist_deadline','pending_cells':len(queue)})
        answer['id']=digest(answer)
        if not stopped:self.forward_cache[oid]=answer
        return answer

    def record(self):
        return {'id':self.identity,'edges':self.rows,'expressions':self.expressions,
                'closures':self.forward_cache,'amount_relations':self.amounts,
                'precision':'source_path_def_use_not_feasibility'}

    def quantity_bridges(self, change, use):
        """Bounded paths of amount dependencies; every intermediate writes a value read downstream."""
        limit=self.summaries.f.options.prefix_depth
        if limit < 2:
            return []
        outs=self.defs.get(change,())
        answers=[]
        mids=set()
        target=self.summaries.f.operations[change]['target']
        def overlap(cells, expr):
            return any(may_alias(w,s) for w in cells for s in selectors(expr))
        for cell in outs:
            for eid in self.readers.get((target,cell['root']),()):
                edge=self.rows[eid]
                if edge['use'] not in (change,use) and edge['kind'] in ('value','amount') and edge['writes'] is not None and may_alias(cell,edge['read']):
                    mids.add(edge['use'])
        use_edges=[edge for edge in self.rows.values() if edge['use']==use and edge['kind'] in ('value','amount')]
        for mid in sorted(mids):
            if self.remaining and self.remaining()<=0:break
            for row in self.summaries.rows(mid):
                written=[w['path'] for w in row['ordered_writes'] if overlap(outs,w['value'])]
                if written and any(overlap(written,self.expressions[edge['expression']]) for edge in use_edges):
                    answers.append((mid,row['path'],written))
                    if len(answers)>=self.summaries.f.options.max_prefixes:return answers
        return answers

    def amounts_for(self,oid):
        """Quantities of one actual reader, retaining their path, key, unit and order."""
        if oid in self.amounts:return self.amounts[oid]
        from .summary import local_delta,holder
        from .key_roles import relation
        f=self.summaries.f
        lookup=f.lookup(oid)
        records=[]
        for row in self.summaries.rows(oid):
            deltas=[];gates=[]
            for seq,w in enumerate(row['ordered_writes']):
                sign,amount=local_delta(w)
                if sign is None or amount is None:continue
                cell=w['path'];role=relation(cell,lookup) or {}
                hid=holder(cell,lookup)
                token=digest(amount)
                self.expressions.setdefault(token,amount)
                deltas.append({'write_index':seq,'cell':cell,'holder':hid,'sign':sign,
                    'amount_expression':token,'source':w['source'],'key_role':role.get('kind'),
                    'stage':'before_source_write','unit_family':cell['root']})
            for guard in row['guards']:
                for comparison in walk(guard):
                    operands=comparison.get('args',[])
                    if comparison.get('op') not in ('>=','<=','>','<','==') or len(operands)!=2:continue
                    for i,operand in enumerate(operands):
                        if operand.get('kind')!='storage':continue
                        role=relation(operand,lookup) or {}
                        if role.get('kind')!='authorization_quantity':continue
                        quantity=operands[1-i];token=digest(quantity)
                        self.expressions.setdefault(token,quantity)
                        gates.append({'grant':operand,'issuer_key':role['holder_key'],
                            'spender_key':1-role['holder_key'],'quantity_expression':token,
                            'operand_index':i,'operator':comparison['op'],'guard_expression':digest(guard)})
            records.append({'path':row['path'],'flow':row['flow'],'deltas':deltas,'allowance_gates':gates,
                'residuals':[x.get('reason') if isinstance(x,dict) else str(x) for x in row['residuals']]})
        self.amounts[oid]=records
        return records

```
