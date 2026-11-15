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
        self.program,self.catalog,self.counter=program,catalog,counter;self.initial_view=None;self.initial_scope=None;self.last_manifest=None
    def _messages(self,value,recovery=False):
        kind=None
        if 'questions' in value:
            question=next(iter(value['questions']),{})
            choice=next(iter(question.get('semantic_questions',[])),{})
            choice=value.get('shared_rows',{}).get(choice.get('shared'),choice)
            kind=choice.get('kind','issue')
        revisable_amount=(self.program.options.scope=='FCR' and
                         any('on' in card for card in value.get('supports',())))
        return [{'role':'system','content':instruction(self.program.options.scope,recovery or value.get('purpose')=='protocol_recovery',
                                                      kind=kind,annotation_revision=revisable_amount,policy_revision=any('effect' in card for card in value.get('supports',())))},
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
              'semantic_focus':('For a highlighted effect, say who should decide and why.' if p.options.scope=='AC'
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
            locators=[{'entry':cat.name(r['operation']),'question':r['kind'],'positions':[cat.program.lookup(r['operation']).nodes.get(w['position']['root'],{}).get('name') for w in r['extra_effects']]} for r in p.source_candidates]
            shown=[]
            for locator in locators:
                if self._count({**complete,'additional_source_questions':shown+[locator]})>target:continue
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
              'source_and_explanation_are_distinct':True,'questions':[]}
        complete={**base,'source_files':[{'file':f,'content':s['content']} for f,s in self.catalog.sources.items()]}
        units=[];deduplicated=0;selected_entities={};shared_consumers={}
        host_questions={};observed_amount_disputes=set()
        for q in feedback['questions']:
            item=copy.deepcopy(q);ops=item.pop('operations',[])
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
            return (not any((unit[0],q.get('id')) in observed_amount_disputes for q in item.get('semantic_questions',[])),not any(q.get('kind')=='scoped_support_dispute' for q in item.get('semantic_questions',[])),not bool(item.get('semantic_questions')),
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
            if not (semantic or item.get('task_conflict') or item.get('alternative') and item.get('evidence')):
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
            'disputed_effects':sorted({e for sid in semantic_wire for e in host_questions[sid].get('affected_effects',[])}),'shared_question_consumers':shared_consumers,'wire_evidence':visible,'semantic_wire':semantic_wire,'shared_row_count':len(value.get('shared_rows',{})),
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
        ceiling=min(self.program.options.input_limit,max(self._count(data)+96,self.program.options.input_target))
        for card in cards:
            if self._count(dict(data,typed_refs=selected+[card]))<=ceiling:selected.append(card)
        if selected:
            data['typed_refs']=selected;manifest['typed_index']={card[0]:index[card[0]] for card in selected}
        manifest['registered_sensitive_effects']=len(getattr(rules,'sensitive_effects',{}))
        manifest['displayed_effect_handles']=[index[c[0]] for c in selected if index[c[0]] in rules.effects]
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
        messages=self._messages(data,recovery);manifest.update(input_tokens=self.counter.count(messages),
            counter_identity=self.counter.identity,messages_sha256=digest(messages),
            counting_scope='complete V4.1 text message envelope including high/JSON markers; offline count, service usage recorded separately')
        manifest['sent_semantic_rows']={row['id']:row for item in data.get('questions',[]) for ref in item.get('semantic_questions',[])
            for row in [data.get('shared_rows',{}).get(ref.get('shared'),ref)] if 'id' in row}
        self.last_manifest=manifest
        return messages,manifest
