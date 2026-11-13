# 实跑源码文本 · 第 8 页

## file-ad4b4d3ce67e36

`source/src/pr_next_joint/investigation/context.py` · 原字节 SHA-256 `c9502c9d3be3f18b10088b3a3361fe4a32e3f47f94c07595b72c97f9dfb3385a`

~~~~python
"""Source-first, graph-organized views. Complete original facts stay local."""
import copy,json,re
from collections import defaultdict,deque
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import walk
from .contracts import VERSION
from .protocol import INSTRUCTION,instruction,REVISION_GUIDANCE

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
                from pr_next_joint.frontend.dispatch import resolve as dispatch
                refs=set()
                for n in walk(body):
                    if n.get('nodeType')!='FunctionCall':continue
                    ref=n.get('expression',{}).get('referencedDeclaration');node=lookup.nodes.get(ref,{})
                    if n.get('expression',{}).get('nodeType')=='Identifier' and node.get('nodeType')=='FunctionDefinition':ref=dispatch(lookup,node)['id']
                    refs.add(ref)
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
        self.program,self.catalog,self.counter=program,catalog,counter;self.initial_view=None;self.initial_scope=None
    def _messages(self,value,recovery=False):
        return [{'role':'system','content':instruction(self.program.options.scope,recovery)},
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
              'scope_note':'Unexpanded relevant obligations not otherwise resolved remain uncovered; source delivery is not completion.',
              'semantic_focus':'Explain the actual resource/right and applicable authorization using the shown source; category and judgment are proposals.'}
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
            locators=[{'entry':cat.name(r['operation']),'question':r['kind'],'positions':[cat.program.lookup(r['operation']).nodes.get(w['position']['root'],{}).get('name') for w in r['extra_effects']]} for r in p.source_candidates]
            shown=[]
            for locator in locators:
                if self._count({**complete,'additional_source_questions':shown+[locator]})>target:break
                shown.append(locator)
            if shown:complete['additional_source_questions']=shown
            manifest['additional_source_questions']={'delivered':len(shown),'total':len(locators),'full_source_preserved':True}
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
              'source_and_explanation_are_distinct':True,'questions':[],'revision_rule':REVISION_GUIDANCE}
        complete={**base,'source_files':[{'file':f,'content':s['content']} for f,s in self.catalog.sources.items()]}
        units=[];deduplicated=0
        for q in feedback['questions']:
            item=copy.deepcopy(q);ops=item.pop('operations',[])
            for field in ('sent_evidence','sent_semantics','sent_message_identity'):
                item.pop(field,None)
            # Only byte/structure-equivalent evidence is merged. Caller, key,
            # branch, assumptions and formula identity remain part of equality.
            for e in item.get('evidence',[]):
                for field in ('probe_results','comparisons'):
                    if not isinstance(e.get(field),list):continue
                    rows={}
                    for v in e[field]:rows.setdefault(digest(v),v)
                    deduplicated+=len(e[field])-len(rows);e[field]=list(rows.values())
            fragments,identity,missing=self.catalog.required_context(ops)
            item['entry_identity_facts']=identity
            units.append((q['id'],item,ops,fragments,missing))
        # A model decision is useful when competing readings predict different
        # consequences, or a still-unbound right/policy controls the judgment.
        # A local type error or an already-settled scalar fact is not a reason
        # to spend the remaining response. Source order breaks equal priority.
        def priority(unit):
            item=unit[1]
            # A typed, source-bound missing meaning is directly answerable.
            # A generic neutral task disagreement must not consume the only
            # revision while an actual amount/policy question remains unsent.
            return (not bool(item.get('semantic_questions')),
                    not bool(item.get('task_conflict') or item.get('alternative') and item.get('evidence')),
                    not bool(item.get('alternative')))
        units.sort(key=priority)
        value={**base,'related_source':[]}
        selected=[];omitted=[];used=set();seen={};full_mode=False
        for qid,item,ops,fragments,missing in units:
            semantic=item.get('semantic_questions',[])
            decision=digest([sorted(ops),item.get('category'),item.get('claim'),item.get('alternative'),
                item.get('distinguishing_question'),[s.get('id') for s in semantic],item.get('evidence')])
            if decision in seen:
                omitted.append({'issue':qid,'reason':'same_dispute_and_evidence','representative':seen[decision]});continue
            seen[decision]=qid
            if selected:
                omitted.append({'issue':qid,'reason':'independent_dispute_retained_locally','priority':list(priority((qid,item)))})
                continue
            if not (semantic or item.get('task_conflict') or item.get('alternative') and item.get('evidence')):
                omitted.append({'issue':qid,'reason':'no_unresolved_semantic_distinction'});continue
            trial={**complete,'questions':[item]}
            tokens=self._count(self._share(trial))
            full_mode=tokens<=self.program.options.input_limit
            if not full_mode:
                if missing:
                    omitted.append({'issue':qid,'reason':'required_source_context_not_resolved','details':missing});continue
                merged={}
                for f in fragments:
                    k=digest(f['source'])
                    if k in merged:merged[k]['targets']=sorted(set(merged[k]['targets']+f['targets']))
                    else:merged[k]=copy.deepcopy(f)
                trial={**base,'questions':[item],'related_source':list(merged.values())}
                tokens=self._count(self._share(trial))
            if tokens<=self.program.options.input_limit:
                value=trial;selected.append(qid);used.update(ops)
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
                    semantic_wire[row['id']]={'display':digest(row),'entity':digest([
                        row.get(k) for k in ('id','operation','target','kind','cell','semantic_scope','core_operation','quantity_scope')])}
        return value,{'mode':'focused_evidence','source_mode':'complete_source_once' if full_mode else 'compiler_bound_local_context',
            'wire_evidence':visible,'semantic_wire':semantic_wire,'shared_row_count':len(value.get('shared_rows',{})),
            'selected_issues':selected,'unexpanded_feedback_issues':omitted,'expanded_operations':sorted(used),
            'selection_rule':'one_source_scoped_decision; capacity and complete necessary context checked per candidate',
            'complete_source_files':sorted(self.catalog.sources) if full_mode else [],'deduplicated_exact_evidence_rows':deduplicated,
            'necessary_context_not_silently_clipped':True,'no_full_facts_or_graph_or_unrelated_history':True}
    def messages(self,feedback=None,recovery=False):
        if recovery:
            if self.initial_view is None:self.initial_view,self.initial_scope=self.initial()
            data=copy.deepcopy(self.initial_view);data['purpose']='Return a consumable final issues JSON; the first response had no usable final analysis.'
            if feedback and feedback.get('binding_diagnostics'):
                data['binding_diagnostics']=copy.deepcopy(feedback['binding_diagnostics'])
            manifest={**copy.deepcopy(self.initial_scope),'mode':'protocol_recovery_reused_source','reused_initial_source_view':True}
        elif feedback is None:
            if self.initial_view is None:self.initial_view,self.initial_scope=self.initial()
            data,manifest=copy.deepcopy(self.initial_view),copy.deepcopy(self.initial_scope)
        else:data,manifest=self.focused(feedback)
        messages=self._messages(data,recovery);manifest.update(input_tokens=self.counter.count(messages),
            counter_identity=self.counter.identity,messages_sha256=digest(messages),
            counting_scope='complete V4.1 text message envelope including high/JSON markers; offline count, service usage recorded separately')
        return messages,manifest

~~~~

## file-7682c342ab1431

`source/src/pr_next_joint/investigation/contracts.py` · 原字节 SHA-256 `290357f6a66e617abcf7e6daa3bd000664b9decbff87f9ace460970a88adc35d`

~~~~python
"""Finite investigation controls and host-owned artifacts; no business detectors."""
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib, json, os, tempfile
from pr_next_joint.core import digest

VERSION = 'permission-risks-next-decision-only-r2'
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
        if not 1<=self.max_paths<=48:raise ValueError('path_bound')
        if (self.input_target,self.input_limit,self.output_limit)!=(16384,32768,32768):raise ValueError('frozen_message_limits')
        if self.attempt_limit not in (1,2) or not 0<=self.prefix_depth<=2 or not 1<=self.max_prefixes<=24:raise ValueError('frozen_call_or_prefix_bound')
        if not 1<=self.max_actions<=64 or not 0<self.seconds<=120 or not 0<self.solver_timeout_ms<=3000:raise ValueError('frozen_investigation_bound')
    def record(self):return asdict(self)

~~~~

## file-f5190790d1aab5

`source/src/pr_next_joint/investigation/coverage.py` · 原字节 SHA-256 `d5fe63d5aa1acb9c30a0b5abacc400088f9882de9cac83143553810253e96457`

~~~~python
"""Property dependency accounting, separate from findings and risk definitions."""
from .contracts import CATEGORIES
from .protocol import category_scope
from .request_scope import coverage_facts, claim_entries, privileged_intervention
from .ledger import movements, unit_origin
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
    stamp=(inv.semantics.version,digest(inv.semantics.active_scope))
    controls=_control_categories(inv);cats=set()
    for oid in entries:
        if oid not in inv.f.operations:continue
        token=(stamp,oid)
        if token not in cache:cache[token]=directory(inv,oid,controls.get(oid,[]))
        cats.update(cache[token]['possible_categories'])
    return sorted(cats)


def _control_categories(inv):
    from pr_next_joint.core import digest
    from pr_next_joint.frontend.storage import selector_relation
    from .ledger import native_only_position
    from .key_roles import relation
    from .scope_relevance import potential_role,nonfinancial
    stamp=(inv.semantics.version,digest(inv.semantics.active_scope))
    cached=getattr(inv,'_coverage_control_index',None)
    if cached and cached[0]==stamp:return cached[1]
    inv._coverage_control_routes={}
    f=inv.f;index={};writers={}
    for w in f.writes.values():
        token=(f.operations[w['operation']]['target'],w['raw']['path']['root'])
        writers.setdefault(token,[]).append(w)
    for use,entry in f.operations.items():
        for _,p in f.operation_paths(use,True):
            minus=[c for c in movements(inv.backend,use,p)['-'] if not nonfinancial(inv.backend,use,c)]
            if not minus:continue
            for control in selectors(p['guards']):
                typ=value_type(control,f.lookup(use)) or ''
                if typ!='bool' and not typ.startswith(('uint','int')):continue
                # Ledger sufficiency is not a distinct freeze/pause control.
                if any(selector_relation(control,c)=='same_shape' for c in minus):continue
                if unit_origin(inv.backend,use,control):continue
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








def obligation_scope(inv, assessments, blocked):
    """Routes and directory residuals share the same dependency records."""
    from pr_next_joint.core import digest
    from pr_next_joint.frontend.path_ir import key
    from .summary import get_summaries
    categories = {'AC'} if inv.f.options.scope == 'AC' else set(CATEGORIES[1:])
    summaries = get_summaries(inv.f)
    local = {}
    by_entry = {}
    for qid, q in inv.issues.items():
        a = assessments[qid]
        if a['scope'].get('route_status')=='superseded':
            local[qid]={'issue':qid,'closed':True,'category':None,'affected_categories':[],
                        'state':'superseded','entries':[],'reason':a['reasons']}
            continue
        p = q.get('property') or {}
        root = inv.root(q)
        cat = a.get('category')
        excluded = a['scope'].get('route_status') == 'excluded'
        supported = a['reportable']
        relevant = {cat} if cat in categories else set(p.get('possible_categories', [])) & categories
        if not relevant:
            # A missing resource answer can leave the compiled category empty.
            # Keep the original bound claim's task category so a independently
            # false necessary condition (for example no privilege) can close
            # that route; its unanswered question is then nondecisive.
            relevant.update(category_scope(q['current'],inv.f.options.scope))
        if root and not relevant:
            relevant.update(possible_properties(inv, {root}))
        status = 'supported' if supported else 'excluded' if excluded else 'open'
        source_exclusion=None
        if root and inv.f.options.scope=='FCR' and not supported:
            possible_properties(inv,{root})
            stamp=(inv.semantics.version,digest(inv.semantics.active_scope))
            certs=inv._directory_certificates[(stamp,root)].get('absence_certificates',{})
            if relevant and relevant<=certs.keys():
                source_exclusion={'categories':sorted(relevant),'certificates':[certs[c] for c in sorted(relevant)],
                    'source_identity':inv.f.identity,'operation':root}
                excluded=True;status='excluded'
        row = {'issue': qid, 'target': p.get('target'), 'analysis_domain': p.get('domain'),
               'property': p.get('id'), 'category': cat, 'entries': [root] if root else [],
               'closed': supported or excluded, 'state': status,
               'affected_categories': [] if supported or excluded else sorted(relevant),
               'reason': a['reasons'], 'dependencies': a['scope'].get('property_support', []),
               'exclusion': a['scope'].get('authorization_counterevidence', []),
               'conditions_are_not_closed_by_mutual_reference': True}
        if a['scope'].get('local_authorization_exclusion'):
            row['single_policy_exclusion']=a['scope']['local_authorization_exclusion']
        if source_exclusion:row['necessary_condition_certificate']=source_exclusion
        local[qid] = row
        by_entry.setdefault(root, []).append(row)
    # A checked writer->use comparison is also evidence for the use's control
    # obligation. It is not a new finding rooted at that use, and must not
    # close a different writer, effect class, property version or source.
    control_exclusions={}
    for qid,q in inv.issues.items():
        row=local[qid];prop=q.get('property')or{};writer=inv.root(q)
        if row['state']!='excluded' or row['category'] not in ('FCR-FREEZE','FCR-PAUSE'):continue
        for label in q['evidence']:
            ev=inv.evidence[label]
            if (ev.get('source_identity')==inv.f.identity and ev.get('property_identity')==prop.get('id') and
                ev.get('change')==writer and ev.get('property_excluded') and not ev.get('local_errors')):
                control_exclusions.setdefault((writer,ev.get('observe'),row['category']),[]).append(label)
    obligations, gaps = [], []
    for oid, operation in inv.f.operations.items():
        rows = summaries.rows(oid, False)
        cats = set(possible_properties(inv, {oid}))
        directory_certificate=None
        if inv.f.options.scope=='FCR':
            directory_certificate=getattr(inv,'_directory_certificates',{}).get(
                ((inv.semantics.version,digest(inv.semantics.active_scope)),oid))
        related = by_entry.get(oid, [])
        cats.update(c for row in related for c in row['affected_categories'])
        effects = [r for r in rows if r['committing'] and (r['ordered_writes'] or r['effects'])]
        residuals = [x for r in rows for x in r['residuals']]
        states = {}
        for cat in categories:
            known = [r for r in related if r['category'] == cat or cat in r['affected_categories']]
            open_rows = [r for r in known if not r['closed']]
            necessary_certificates=[]
            for q in inv.issues.values():
                if inv.root(q)!=oid or local[q['id']]['category']!=cat or not local[q['id']]['closed']:continue
                prop=q.get('property')or{}
                for label in q['evidence']:
                    ev=inv.evidence[label];cert=ev.get('necessary_condition_route_coverage')or{}
                    if (ev.get('property_identity')==prop.get('id') and ev.get('property_excluded') and
                        cert.get('source_identity')==inv.f.identity and cert.get('operation')==oid and
                        cert.get('all_source_routes_accounted')):necessary_certificates.append(label)
            control_writers={writer for (writer,control_cat),uses in
                getattr(inv,'_coverage_control_routes',{}).items() if control_cat==cat and oid in uses}
            control_certificates=[{'writer':writer,'use':oid,
                'evidence':control_exclusions.get((writer,oid,cat),[])} for writer in sorted(control_writers)]
            controls_closed=(bool(control_writers) and all(c['evidence'] for c in control_certificates) and
                cat in ('FCR-FREEZE','FCR-PAUSE') and inv.backend.complete(oid) and directory_certificate and
                not directory_certificate.get('unresolved_same_storage_calls') and
                not directory_certificate.get('unread_effect_residuals') and
                not any(cat in route.get('possible_categories',[]) for route in directory_certificate.get('source_routes',[])))
            static_closed=(directory_certificate or {}).get('absence_certificates',{}).get(cat)
            if static_closed and not open_rows:
                states[cat] = {'state': 'excluded', 'basis':static_closed['basis'],
                               'dependency_certificate':static_closed}
            elif open_rows or residuals and not necessary_certificates:
                states[cat] = {'state': 'open', 'basis': 'decisive_property_or_source_residual',
                               'issues': [r['issue'] for r in open_rows], 'residuals': residuals}
            elif controls_closed:
                states[cat] = {'state':'excluded','basis':'all_source_control_writers_excluded_for_this_use',
                    'control_comparisons':control_certificates,
                    'other_effect_classes_not_closed_by_this_certificate':True}
            elif known and all(r['closed'] for r in known) and (inv.backend.complete(oid) or necessary_certificates):
                # Same category does not imply the same resource. Independent
                # positions require an actual property for their own scope.
                covered = set()
                for q in inv.issues.values():
                    if inv.root(q) == oid and local[q['id']]['closed'] and local[q['id']]['category']==cat:
                        covered.update(key(c) for c in (q.get('property') or {}).get('objects', []))
                cells = {key(e['cell']) for r in effects for e in r['numeric_effects'] if e['holder'] is not None}
                required_uses=getattr(inv,'_coverage_control_routes',{}).get((oid,cat),set())
                checked_uses=set()
                for q in inv.issues.values():
                    if inv.root(q)!=oid or not local[q['id']]['closed'] or local[q['id']]['category']!=cat:continue
                    for label in q['evidence']:
                        ev=inv.evidence[label]
                        if ev.get('property_identity')==(q.get('property') or {}).get('id') and (ev.get('property_excluded') or
                            any(x.get('bounded_condition_confirmed') and x['label']=='financial_block' for x in ev.get('queries',[]))):
                            checked_uses.add(ev.get('observe'))
                complete=(cells<=covered and required_uses<=checked_uses and not
                    any(r.get('single_policy_exclusion',{}).get('other_policies_or_effects_closed') is False
                        for r in known))
                states[cat] = {'state': 'excluded' if complete else 'open',
                               'basis': 'source_positions_and_resolved_properties', 'uncovered_positions': sorted(cells-covered),
                               'necessary_condition_certificates':necessary_certificates,
                               'unchecked_control_uses':sorted(required_uses-checked_uses)}
            else:
                states[cat] = {'state': 'open', 'basis': 'relevant_source_scope_without_resolved_property'}
        affected = sorted(c for c in categories if states[c]['state'] == 'open')
        token = digest([operation['target'], oid])
        record = {'id': 'obligation_' + token[:20], 'target': operation['target'], 'operations': [oid],
                  'category_states': states, 'closed': not affected, 'affected_categories': affected,
                  'possible_categories': sorted(cats),
                  'source_dependency_certificate':directory_certificate,
                  'entry_states': [{'operation': oid, 'states': {c: 'open' if c in affected else 'resolved' for c in categories}}],
                  'call_dependencies': inv.f.call_summaries.dependencies(oid, {
                      s['root'] for r in rows for s in selectors([r['guards'], r['ordered_writes']])})}
        obligations.append(record)
        if affected:
            gaps.append(dict(record, reason='source_obligation_not_resolved'))
    # Unbound and rejected source clues are independent residuals. Do not erase
    # them when the directory or model candidate list happens to be empty.
    nondecisive=[]
    for raw in inv.coverage_gaps:
        if raw.get('issue') in local and local[raw['issue']]['closed']:
            continue
        bound=local.get(raw.get('issue'))
        if bound and bound['entries']:
            # A missing optional reply is a dependency of its actual source
            # property, not of all five categories. The directory independently
            # retains unread/effect/call residuals for the same entry.
            affected=sorted(set(bound['affected_categories']) | set(possible_properties(inv,bound['entries'])))
            if not affected:
                nondecisive.append(dict(raw,reason_for_exclusion='no relevant five-class source dependency',
                    entries=bound['entries']))
                continue
            gaps.append(dict(raw,affected_categories=affected,closed=False,
                dependency_scope='bound_property_and_source_directory'))
            continue
        affected = category_scope(raw, inv.f.options.scope)
        if not affected and raw.get('category') in CATEGORIES+('ADDITIONAL',):
            # The independently scanned source directory remains authoritative;
            # an explicitly different task/class is not a missing dependency
            # of every class in this task.
            continue
        if not affected:
            affected = sorted(categories)
        if raw.get('reason')=='unbound_original_claim' and raw.get('assessment')=='normal':
            proved=[c for c in affected if obligations and all(o['category_states'][c]['state']=='excluded' for o in obligations)]
            if proved:
                nondecisive.append(dict(raw,independently_closed_categories=proved,
                    reason_for_exclusion='complete source obligations independently exclude this normal absence claim',
                    certificates=[o['id']for o in obligations]))
                affected=[c for c in affected if c not in proved]
            if not affected:continue
        gaps.append(dict(raw, affected_categories=affected, closed=False))
    open_categories = {c for r in gaps for c in r.get('affected_categories', [])}
    blocked.update(open_categories)
    return {'schema': 'shared-route-dependencies-r1', 'request_scope': (inv.initial_manifest or {}).get('requested_reading'),
            'declaration': inv.task_declaration, 'whole_reading_eligible': not open_categories,
            'eligibility_reasons': ['decisive_dependencies_open'] if open_categories else [],
            'known_category_gaps': gaps, 'source_local_scopes': local, 'obligations': obligations,
            'nondecisive_model_gaps':nondecisive,
            'neutral_scope_scan_executed': bool(inv.f.selected),
            'negative_eligible_categories': sorted(categories - open_categories),
            'delivery_and_model_declaration_are_not_completion': True}

~~~~

## file-48471ae326f2ed

`source/src/pr_next_joint/investigation/decision_output.py` · 原字节 SHA-256 `c110264dd10704ecfa7be0e72f3539174f20dc61065c41c8835790a1979d21d2`

~~~~python
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
    return value if isinstance(value,str) and re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.:-]{0,159}',value) else fallback

def codes(values):
    return [code(v) for v in values if isinstance(v,str)] if isinstance(values,list) else []

def location(value):
    if not isinstance(value,dict):return {}
    out={'file':value['file']} if isinstance(value.get('file'),str) else {}
    out.update({k:value[k] for k in ('start','length','ast_id','line','column') if type(value.get(k)) is int})
    return out

def receipt(value,purpose):
    return {'profile':PROFILE,'purpose':purpose,'content_sha256':digest(value),'body_retained':False}

def diagnostic(row):
    if not isinstance(row,dict):return {'reason':code(row),'detail_sha256':digest(row)}
    out={'reason':code(row.get('reason',row.get('kind'))),'detail_sha256':digest(row)}
    out.update({k:code(row[k]) for k in ('issue','category') if k in row})
    if isinstance(row.get('source'),dict):out['source_location']=location(row['source'])
    return out

def context_summary(value):
    out=receipt(value,'source_delivery_and_capacity')
    out.update({k:value[k] for k in ('input_tokens','input_target','input_limit','output_limit') if type(value.get(k)) is int})
    if isinstance(value.get('messages_sha256'),str):out['messages_sha256']=value['messages_sha256']
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
    return out

def assessment_summary(value):
    return {'reportable':value.get('reportable') is True,'category':value.get('category'),
            'reasons':codes(value.get('reasons',[])),'scope':scope_summary(value.get('scope',{}))}

def query_summary(q):
    d=q.get('details',{})
    out={k:q[k] for k in ('id','label','answer','formula_sha256','bounded_condition_confirmed') if k in q}
    out.update(evidence_kind='bounded_condition_check_without_assignment_extraction',
               condition_identity=digest(d),model_extracted=False,formula_saved=False)
    keys=('property_validated','measurement_only','same_request','effect_required','new_authority_required',
          'downstream_effect_required','acquisition_use_required','baseline_commit_not_assumed',
          'no_universal_gross_allowance_policy','all_productive_paths_checked','all_continuations_exact',
          'original_all_positive_amount_obligation_preserved')
    criteria={k:d[k] for k in keys if type(d.get(k)) is bool}
    if d.get('corresponding_same_ledger_credit'):criteria['corresponding_same_ledger_credit']=True
    for k in ('category_hypothesis','property_identity'):
        if k in d:criteria[k]=code(d[k])
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
    out={k:copy.deepcopy(row[k]) for k in ('id','target','closed','affected_categories') if k in row}
    out['category_states']={c:{'state':code(s.get('state')),'basis':code(s.get('basis')),'detail_sha256':digest(s)}
                            for c,s in row.get('category_states',{}).items()}
    return out

def coverage_summary(value):
    return {'schema':'decision-only-coverage-v1','whole_reading_eligible':value.get('whole_reading_eligible') is True,
        'negative_eligible_categories':copy.deepcopy(value.get('negative_eligible_categories',[])),
        'obligations':[coverage_row(row) for row in value.get('obligations',[])],
        'known_category_gaps':[coverage_row(row) for row in value.get('known_category_gaps',[])],
        'neutral_scope_scan_executed':value.get('neutral_scope_scan_executed') is True,
        'content_sha256':digest(value),'delivery_and_model_declaration_are_not_completion':True}

def semantic_summary(record):
    out=receipt(record,'source_bound_semantic_interpretations')
    out['financial_consents']=[{'meaning':code(c.get('meaning')),'identity':digest(c)} for c in record.get('financial_consents',[])]
    return out

def public_report(report):
    if report.get('output_profile')==PROFILE:return copy.deepcopy(report)
    keep=('method','program_identity','task','options','implementation_sha256','main_finding_ids',
          'additional_finding_ids','unresolved_mapping_ids','model_analysis_available','prediction_basis_available',
          'prediction_basis_issues','unresolved_category_judgments','prediction_frozen_before_gold','scoring_performed','timing')
    out={k:copy.deepcopy(report[k]) for k in keep if k in report}
    out.update(output_profile=PROFILE,replay_material_generated=False,concrete_execution_performed=False,
               risk_absence_statement='No risk detected in analyzed scope is not proof of safety.')
    out['findings']=[]
    for f in report.get('findings',[]):
        row={k:copy.deepcopy(f[k]) for k in ('id','category','target','operation','comparison_scope','evidence_refs','issue_ids') if k in f}
        row.update(root_location=location(f.get('root_location')),evidence_level='source_analysis_and_bounded_condition_checks',
                   evidence_scope=scope_summary(f.get('scope',{})),
                   explanation='Source-supported risk judgment; inspect the recorded location and bounded coverage.')
        out['findings'].append(row)
    out['inspection_records']=[{'id':r['id'],'version':r.get('version'),
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
    out['task_analysis']={k:task[k] for k in ('model_analysis_available','empty_response_present',
        'explicit_empty_task_reading','local_judgment_not_global_safety','unexecuted_actions') if k in task}
    out['task_analysis']['reading_scope']=coverage_summary(task.get('reading_scope',{}))
    usage=copy.deepcopy(report.get('usage',{}))
    for row in usage.get('attempts',[]):
        if 'normalization_diagnostics' in row:row['normalization_diagnostics']=[diagnostic(x) for x in row['normalization_diagnostics']]
        if 'reason' in row:row['reason']=code(row['reason'])
    out['usage']=usage
    p=report.get('provenance',{})
    out['provenance']={'action_count':len(p.get('actions',[])),'revision_count':len(p.get('revisions',[])),
        'evidence_labels':copy.deepcopy(p.get('evidence_labels',[])),'cache_hits':p.get('cache_hits',0),
        'feedback_trace':[{k:row[k] for k in ('issue','selected','sent','parsed','consumed','simulated','changed_finding') if k in row}
                          for row in p.get('feedback_trace',[])]}
    if 'solver_resource' in report:out['solver_resource']=copy.deepcopy(report['solver_resource'])
    return out

~~~~

## file-db35076892bc2e

`source/src/pr_next_joint/investigation/dependencies.py` · 原字节 SHA-256 `60b61f2c66fac42c763acd8b892595709debe1c924c36890e3a7e32afca442f2`

~~~~python
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
        self.forward_cache[oid]=answer
        return answer

    def record(self):
        return {'id':self.identity,'edges':self.rows,'expressions':self.expressions,
                'closures':self.forward_cache,'amount_relations':self.amounts,
                'precision':'source_path_def_use_not_feasibility'}

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

~~~~
