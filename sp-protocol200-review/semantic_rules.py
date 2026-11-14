"""Typed semantic supports over the existing source summaries. No graph edge or model label is a verdict."""
from collections import defaultdict, deque
import copy
import re
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key,walk
from pr_next_joint.frontend.storage import keys, value_type
from .summary import local_delta, holder, has_basis
from .initial_state import domain
from .key_roles import relation as key_relation

RESOURCE={'financial_right','nonfinancial_counter'}
AMOUNTS={'original_request','request','gross_debit','debit','net_receipt','net','compensation'}
CONSENT={'gross_debit_bound','net_request_with_fee'}
AUTH={'current_authority_required','holder_authorization_applies','initialization_stage'}
def loc_key(loc):
    return (loc.get('file'),loc.get('start'),loc.get('length'))
def field_node(cell):
    return next((seg['field'] for seg in reversed(cell.get('segments',())) if 'field' in seg),cell['root'])


class SupportIndex:
    """Input and derived facts share identities. Re-ground only descendants of edited roots."""
    def __init__(self, remaining):
        self.remaining=remaining
        self.roots=defaultdict(set)
        self.edges=defaultdict(set)
        self.children=defaultdict(set)
        self.live=set()
        self.pending=set()
        self.cut=False
        self.visits=0
        self.certificates={};self.proof_rules={}

    def rule(self, conclusion, inputs, rule):
        clause=(rule,tuple(sorted(set(inputs))))
        if not clause[1] or clause in self.edges[conclusion]:return
        self.edges[conclusion].add(clause)
        for fact in clause[1]:self.children[fact].add(conclusion)
        self.pending.add(conclusion)

    def update(self, fact, support, active):
        changed=(support in self.roots[fact])!=bool(active)
        if active:self.roots[fact].add(support)
        else:self.roots[fact].discard(support)
        if changed:self.pending.add(fact)

    def valid(self,fact):
        if self.roots.get(fact):return True
        certificate=self.certificates.get(fact)
        return fact in self.live and bool(certificate) and all(sid in self.roots.get(node,()) for node,sid in certificate)

    def settle(self):
        if not self.pending:return set()
        self.cut=False
        affected=set(self.pending); todo=deque(sorted(affected))
        before={node for node in affected if node in self.live}
        while todo:
            node=todo.popleft()
            for child in self.children[node]:
                if child not in affected:
                    affected.add(child);todo.append(child)
                    if child in self.live:before.add(child)
            if self.remaining()<=0:
                # A stale positive must never survive an incomplete retraction.
                self.cut=True
                return {x for x in affected if (x in before)!=self.valid(x)}
        self.live.difference_update(affected)
        ready=deque(sorted(affected))
        while ready:
            if self.remaining()<=0:
                self.cut=True;break
            node=ready.popleft();self.visits+=1
            if node in self.live:continue
            roots=self.roots.get(node)
            proof=None;used_rules=set()
            if roots:proof=frozenset(((node,min(roots)),))
            else:
                for rule,terms in sorted(self.edges.get(node,())):
                    if all(x in self.live and self.valid(x) for x in terms):
                        proof=frozenset().union(*(self.certificates[x] for x in terms))
                        used_rules={rule}.union(*(self.proof_rules.get(x,()) for x in terms))
                        break
            if proof:
                self.certificates[node]=proof;self.proof_rules[node]=used_rules;self.live.add(node)
                ready.extend(n for n in self.children[node] if n in affected and n not in self.live)
        if not self.cut:self.pending.clear()
        return before.symmetric_difference({x for x in affected if self.valid(x)})

    def basis(self, fact):
        # Already grounded provenance stays readable even at the cutoff; no rule runs here.
        if not self.valid(fact):return [],[]
        origins=set(self.roots.get(fact,()));rules=set()
        cert=self.certificates.get(fact,())
        if cert and all(sid in self.roots.get(node,()) for node,sid in cert):
            origins.update(sid for _,sid in cert);rules.update(self.proof_rules.get(fact,()))
        todo=[fact];seen=set()
        while todo and self.remaining()>0:
            n=todo.pop()
            if n in seen or not self.valid(n):continue
            seen.add(n);origins.update(self.roots[n])
            for rule,terms in self.edges[n]:
                if all(self.valid(x) for x in terms):rules.add(rule);todo.extend(terms)
        return sorted(origins),sorted(rules)


class ScopedRules:
    """Indexes refer to compiler-selected declarations and individual applied source writes."""
    def __init__(self,inv):
        self.inv=inv;self.f=inv.f;self.logic=SupportIndex(inv.program_remaining)
        self.objects={};self.effects={};self.aliases=defaultdict(set);self.used=defaultdict(set)
        self.by_decl=defaultdict(set);self.by_operation=defaultdict(set);self.routes=defaultdict(list)
        self.supports={};self.facts={};self.by_handle=defaultdict(set)
        self.built=False;self.incomplete=set();self.declaration_lookups=set()
        self.events=[];self.history=[];self.last_changes=set();self.epoch=0

    def remaining(self):
        return self.inv.program_remaining()>0

    def obj(self,target,rid,oid=None):
        return 'o_'+digest([self.f.bundle['build_id'],target,rid,oid])[:20]

    def index(self):
        if self.built:return
        self.built=True
        for oid,operation in self.f.operations.items():
            if not self.remaining():self.incomplete.update(set(self.f.operations)-set(self.by_operation));break
            if operation.get('generated_getter'):continue
            target=operation['target'];lookup=self.f.lookup(oid)
            for row in self.f.summaries.rows(oid):
                if not self.remaining():self.incomplete.add(oid);break
                self.index_observed_effects(oid,row)
                raw=self.f.paths[row['path']]['raw']
                for wi,w in enumerate(row['ordered_writes']):
                    if not self.remaining():self.incomplete.add(oid);break
                    cell=w['path'];rid=field_node(cell);loc=w['source']
                    effect='w_'+digest([self.f.bundle['build_id'],target,oid,row['path'],wi,loc,cell])[:20]
                    desc=dict(oid=oid,target=target,path=row['path'],where=loc,cell=cell,
                              version=wi,conditions=digest(row['guards']),write=w,clean=not row['residuals'])
                    self.effects[effect]=desc;self.by_operation[oid].add(effect)
                    name=lookup.nodes.get(rid,{}).get('name')
                    if not name:continue
                    obj=self._declare(target,rid,None,lookup)
                    self.by_decl[obj].add(effect)
                    fn=operation['function']
                    self._names(effect,target,fn+'#'+name)
                    sign,_=local_delta(w)
                    if sign:self._names(effect,target,fn+'#'+name+('~debit' if sign=='-' else '~credit'))
                    self._names(effect,target,fn)
                    self.aliases['effect:'+effect[2:]].add(effect)
                    self.used[obj].add(oid)
                    sign,qty=local_delta(w)
                    if row['residuals']:continue
                    # Read provenance comes from the evaluated, substituted expression; a shared root is insufficient.
                    for kind,expr in [('value',qty if qty is not None else w['value']),('key',keys(cell)),('guard',row['guards'])]:
                        for term in walk(expr):
                            if not self.remaining():self.incomplete.add(oid);break
                            if term.get('kind') not in ('parameter','storage'):continue
                            pid=term['id'] if term['kind']=='parameter' else field_node(term)
                            source=self._declare(target,pid,oid if term['kind']=='parameter' else None,lookup)
                            self.used[source].add(oid)
                            rules=['P03'] if term['kind']=='storage' else []
                            if kind=='guard':rules.append('P05')
                            if row['guards']:rules.append('P06')
                            if kind=='value':
                                if qty is not None:rules.append('P04')
                                if any(k.get('kind')=='parameter' and k.get('id')==pid for k in walk(raw.get('copy_origins',[]))):rules.append('P01')
                                for call in raw.get('read_calls',[]):
                                    if call.get('binding') not in ('compiler_internal_declaration','compiler_bound_qualified_ancestor','compiler_bound_internal_pure_library'):continue
                                    if key(call.get('return_value'))==key(term) and any(key(a)==key(term) for a in call.get('arguments',[])):
                                        rules.append('P02')
                                        if any(key(x.get('value'))==key(term) for x in call.get('copies',[])):rules.append('P01')
                            route=(effect,kind,tuple(dict.fromkeys(rules)),key(expr)==key(term))
                            if route not in self.routes[source]:self.routes[source].append(route)


    def index_observed_effects(self,oid,row):
        """Index a compiler-located effect as an occurrence, never as an inferred write.
        Distinct branches share the source occurrence and keep their own conditions."""
        target=self.f.operations[oid]['target'];fn=self.f.operations[oid]['function']
        for term in row['effects']:
            if not self.remaining():self.incomplete.add(oid);return
            loc=term.get('source') or {};kind=term.get('kind')
            if not kind or not loc.get('file') or loc.get('start') is None:continue
            effect='e_'+digest([self.f.bundle['build_id'],target,oid,loc_key(loc),kind])[:20]
            d=self.effects.setdefault(effect,dict(oid=oid,target=target,where=loc,kind=kind,branches={}))
            d['branches'][row['path']]={'conditions':digest(row['guards']),'has_residuals':bool(row['residuals'])}
            self.by_operation[oid].add(effect)
            self._names(effect,target,fn);self._names(effect,target,fn+'#'+kind)

    def declaration_by_ref(self,reference):
        # Bind a uniquely named declaration in the actual applied inheritance scope on demand.
        if reference in self.declaration_lookups:return
        self.declaration_lookups.add(reference)
        for target in self.inv.catalog.targets:
            aliases=(target+'.',target.rsplit(':',1)[-1]+'.')
            name=next((reference[len(prefix):] for prefix in aliases if reference.startswith(prefix)),None)
            if not name or not re.fullmatch(r'[\w$]+',name):continue
            lookup=self.f.lookups[target]
            bases=lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
            for base in bases:
                if not self.remaining():return
                for node in lookup.nodes[base].get('nodes',()):
                    if node.get('stateVariable') and node.get('name')==name:
                        self._declare(target,node['id'],None,lookup)

    def _names(self,h,target,name):
        for t in (target,target.rsplit(':',1)[-1]):self.aliases[t+'.'+name].add(h)

    def _declare(self,target,rid,oid,lookup):
        handle=self.obj(target,rid,oid)
        if handle in self.objects:return handle
        node=lookup.nodes.get(rid,{})
        name=node.get('name','')
        self.objects[handle]=dict(target=target,decl=rid,oid=oid,where=lookup.anchor(node) if node.get('src') else {},name=name)
        if name:
            self._names(handle,target,self.f.operations[oid]['function']+'#'+name if oid else name)
        self.aliases['obj:'+handle[2:]].add(handle)
        return handle

    def visible(self,handle,manifest):
        rec=self.objects.get(handle) or self.effects.get(handle)
        if not rec:return False
        where=rec['where']
        if where.get('file') in manifest.get('complete_source_files',[]):return True
        for a in manifest.get('visible_spans',()):
            if where.get('file')==a.get('file') and a['start']<=where['start'] and where['start']+where['length']<=a['start']+a['length']:return True
        return False

    def bind(self,ref,manifest,kind=None):
        if not isinstance(ref,str):return None
        if ref.startswith(('obj:','effect:')):
            hs={manifest.get('typed_index',{}).get(ref)}
        else:
            if kind!='effect':self.declaration_by_ref(ref)
            hs=self.aliases.get(ref,set())
        if not hs and isinstance(ref,str) and not ref.startswith(('obj:','effect:','sem:')):
            # A source span may denote a declaration or a write if there is a unique applied identity.
            m=re.fullmatch(r'(.+[.]sol)@(\d+)\+(\d+)',ref)
            if m:
                at=(m[1],int(m[2]),int(m[3]))
                pool=self.objects if kind=='obj' else self.effects if kind=='effect' else {**self.objects,**self.effects}
                hs={hh for hh,r in pool.items() if loc_key(r['where'])==at}
        hs={v for v in hs if v and ((kind!='effect' and v in self.objects) or (kind!='obj' and v in self.effects)) and self.visible(v,manifest)}
        # A declaration/entry label cannot arbitrarily pick one of its writes.
        return next(iter(hs)) if len(hs)==1 else None

    def cards_for(self,manifest,focus):
        self.index()
        selected=[]
        for oid in dict.fromkeys(focus):
            for e in sorted(self.by_operation[oid]):
                d=self.effects[e]
                obj=self.obj(d['target'],field_node(d['cell'])) if 'cell' in d else None
                for k in ([e,obj] if obj in self.objects else [e]):
                    if k in selected or not self.visible(k,manifest):continue
                    selected.append(k)
                    if len(selected)>=4:break
                if len(selected)>=4:break
            if len(selected)>=4:break
        cards=[];index={}
        for h in selected:
            d=self.effects.get(h) or self.objects[h]
            k=('effect:' if h in self.effects else 'obj:')+str(len(cards)+1)
            if h in self.effects:
                suffix=self.f.lookup(d['oid']).nodes[field_node(d['cell'])]['name'] if 'cell' in d else d['kind']
                name=self.inv.catalog.name(d['oid'])+'#'+suffix
            else:
                name=(self.inv.catalog.name(d['oid'])+'#' if d.get('oid') else d['target'].rsplit(':',1)[-1]+'.')+d['name']
            cards.append([k,name]);index[k]=h
        return cards,index

    def fact(self,h,meaning,subject=None,scope=None,role=None):
        fid='fact_'+digest([self.f.identity,h,meaning,subject,scope,role])[:20]
        if fid not in self.facts:
            self.facts[fid]=dict(handle=h,meaning=meaning,subject=subject,scope=scope,role=role)
            self.by_handle[h].add(fid)
        return fid

    def row_scope(self,field,row,manifest,previous=None):
        meaning=row.get('meaning',previous and previous['meaning'])
        if not isinstance(meaning,str):return None
        locator,kind=('on','obj') if field=='annotations' else ('effect','effect')
        h=previous['handle'] if previous else None
        if locator in row:
            named=self.bind(row[locator],manifest,kind)
            if named is None or h is not None and named!=h:return None
            h=named
        if not h:return None
        def qualifier(name):
            if name in row:return self.bind(row[name],manifest)
            return previous.get(name) if previous else None
        subject=qualifier('subject');scope=qualifier('scope')
        if any(name in row and not val for name,val in [('subject',subject),('scope',scope)]):return None
        d=self.effects.get(h) or self.objects[h]
        if any((self.effects.get(v) or self.objects[v])['target']!=d['target'] for v in (subject,scope) if v):return None
        if subject and meaning in RESOURCE|CONSENT and subject not in self.objects:return None
        if scope and scope!=h and scope not in self.by_decl.get(h,set()) and not any(e==scope for e,_,_,_ in self.routes.get(h,())):return None
        if meaning in AUTH|CONSENT|RESOURCE and subject and subject not in self.objects:return None
        if meaning in CONSENT and not list(self.quantity_scopes(h)):return None
        role=row.get('role',previous.get('role') if previous else None)
        if role is not None and (not isinstance(role,str) or role not in AMOUNTS):return None
        if h in self.effects and meaning in CONSENT and subject:
            decl=self.objects[subject]['decl']
            if not all(any(t.get('id')==decl for t in walk(keys(route['grant'])[route['issuer_key']])) for route in self.quantity_scopes(h)):return None
        if meaning=='amount_role' and role not in AMOUNTS:return None
        return dict(handle=h,meaning=meaning,subject=subject,scope=scope,role=role)

    def quantity_scopes(self,e):
        d=self.effects.get(e)
        if not d or 'write' not in d:return
        for a in self.f.summaries.dependencies.amounts_for(d['oid']):
            if a['path']!=d['path']:continue
            for dec in a['deltas']:
                if dec['sign']!='-' or dec['write_index']!=d['version'] or dec.get('key_role')=='authorization_quantity':continue
                for gate in a['allowance_gates']:
                    grant=gate['grant'];issuer=keys(grant)[gate['issuer_key']]
                    if key(issuer)!=key(dec.get('holder')):continue
                    yield {'path':a['path'],'grant':grant,'issuer_key':gate['issuer_key'],'spender_key':gate['spender_key'],
                           'debit_expression':dec['amount_expression'],'checked_quantity_expression':gate['quantity_expression'],'ledger':dec['cell']}

    def register(self,fid,sid,origin,field):
        if sid in self.supports and (self.supports[sid]['active'] or self.supports[sid].get('withdrawn')):return False
        self.supports[sid]=dict(fact=fid,origin=origin,field=field,active=True,version=1+self.supports.get(sid,{}).get('version',0))
        self.logic.update(fid,sid,True)
        return True

    @staticmethod
    def revision_reason(row,proposed):
        """Location is authenticated separately. Discard output instructions and bare labels,
        leaving the model's own semantic explanation (in any source vocabulary)."""
        reason=row.get('basis','')
        if not has_basis(reason):return False
        clauses=re.split(r'[.;!?。；！？\n]+|\b(?:because|since)\b|因为|由于',reason,flags=re.I)
        directive=r'^(?:(?:please|just|kindly|we should|you should)\s+)*(?:remove|withdraw|cancel|drop|suppress|change|relabel|mark|classify|report|delete|downgrade|upgrade|dismiss|ignore)\b'
        for clause in clauses:
            clause=clause.strip()
            if not clause or re.match(directive,clause,re.I) or re.match(r'^(?:请|应当|应该|仅需|只要)*(?:撤回|删除|取消|改为|标记|移除|忽略)',clause):continue
            words=re.findall(r'[^\W_]+',clause.casefold())
            meta={'the','this','is','a','an','of','as','only','it','should','be','alarm','warning','finding','risk','safe','not','false','positive','wrong','correct','label','incorrect','unsupported'}
            meta.update(re.findall(r'[^\W_]+',proposed['meaning']))
            supplied={word for word in words if word not in meta}
            if len(supplied)>=2 or re.search(r'[\u3400-\u9fff]{4,}',clause):return True
        return False

    def hard_unit_conflict(self,proposal):
        if proposal['meaning']!='nonfinancial_counter':return False
        from .ledger import _unit_origin
        h=proposal['handle']
        candidates=self.by_decl.get(h,set())|{e for e,k,_,exact in self.routes.get(h,()) if k=='value' and exact}
        for e in candidates:
            if not self.remaining():return 'semantic_budget'
            if proposal['scope'] and proposal['scope']!=e:continue
            d=self.effects[e]
            if proposal['subject']:
                declared=self.objects[proposal['subject']]['decl']
                if not any(t.get('id')==declared for t in walk(keys(d['cell']))):continue
            if d['clean'] and holder(d['cell'],self.f.lookup(d['oid'])) and _unit_origin(self.inv.backend,d['oid'],d['cell']):return 'scoped_source_unit_conflict'
        return False

    def apply(self,value,manifest,revision=False):
        """Stage unrelated updates separately; an ambiguous alias can never displace a valid support."""
        rows=[(field,r) for field in ('annotations','policies') for r in value.get(field,())]
        requests=defaultdict(list)
        for field,row in rows:
            identity=row.get('ref') or row.get('id')
            if isinstance(identity,str):requests[identity].append((field,row))
        conflicting={k for k,items in requests.items() if len({digest(x) for x in items})>1}
        accepted=[];rejected=[];changed=set();self.submission=manifest.get('messages_sha256')
        for field,row in rows:
            if not self.remaining():rejected.append('semantic_budget');break
            ref=row.get('ref');name=ref or row.get('id')
            if name is not None and (not isinstance(name,str) or name in conflicting):rejected.append('ambiguous_seed_id');continue
            old=None;sid=None;action=row.get('action','add')
            current=None
            if ref:
                wire=manifest.get('shown_supports',{}).get(ref,{})
                sid=wire.get('support');old=self.supports.get(sid)
                if not revision or not old or not old['active'] or old['origin'] not in ('fixture','verified_service') or old['version']!=wire.get('version') or old['fact']!=wire.get('fact'):
                    rejected.append('stale_or_undisplayed_support');continue
                if field!=old['field'] or field!=wire.get('field'):
                    rejected.append('wrong_semantic_facet');continue
                current=self.facts[old['fact']]
                locator,kind=('on','obj') if field=='annotations' else ('effect','effect')
                if locator in row and self.bind(row[locator],manifest,kind)!=current['handle']:
                    rejected.append('revision_object_mismatch');continue
            proposed=self.row_scope(field,row,manifest,current)
            if not proposed:
                rejected.append('unbound_or_inapplicable_seed');continue
            if current:
                if action in ('confirm','withdraw') and proposed!=current:
                    rejected.append('revision_conflicts_with_displayed_support');continue
                if action=='confirm':
                    accepted.append(sid);continue
                if action=='narrow':
                    if current['scope'] or proposed['scope'] not in self.effects or proposed['scope']==current['handle'] or any(proposed[k]!=current[k] for k in ('meaning','subject','role')):
                        rejected.append('scope_not_strictly_narrower');continue
                elif proposed['scope']!=current['scope']:
                    rejected.append('scope_change_requires_narrow');continue
                if not self.revision_reason(row,proposed):
                    rejected.append('revision_without_scoped_reason');continue
                if action=='correct':
                    conflict=self.hard_unit_conflict(proposed)
                    if conflict:
                        rejected.append(conflict);continue
            fid=None if action=='withdraw' else self.fact(proposed['handle'],proposed['meaning'],proposed['subject'],proposed['scope'],proposed['role'])
            if old:
                if fid==old['fact']:accepted.append(sid);continue
                self.history.append({'action':action,'support':sid,'before':old['fact'],'after':fid,'from_version':old['version'],'to_version':old['version']+1})
                self.logic.update(old['fact'],sid,False);changed.add(old['fact'])
                old.update(active=False,withdrawn=True,version=old['version']+1)
            if fid:
                sid=sid or 'support_'+digest([value['origin'],manifest.get('messages_sha256'),fid])[:20]
                if old:
                    old.update(active=True,withdrawn=False,fact=fid);self.logic.update(fid,sid,True)
                else:self.register(fid,sid,value['origin'],field)
                self.derive(fid);changed.add(fid)
            accepted.append(sid)
        live_delta=self.logic.settle()
        self.last_changes={self.facts[f]['handle'] for f in live_delta if f in self.facts}
        self.epoch+=bool(live_delta)
        for fid in changed:self.events.append({'fact':fid,'active':self.logic.valid(fid),'sources':len(self.logic.roots[fid])})
        return accepted,rejected

    def derive(self,fid):
        queue=deque([fid]);visited=set()
        while queue and self.remaining():
            source=queue.popleft()
            if source in visited:continue
            visited.add(source)
            queue.extend(self._derive_one(source))
        for source in queue:self.incomplete.update(self.related_ops(self.facts[source]['handle']))

    def _derive_one(self,fid):
        src=self.facts[fid];h=src['handle']
        if h not in self.objects:return
        meaning=src['meaning']; role=src['role']
        if meaning in ('unknown','other_source_meaning','other_source_policy'):return
        for e,k,rules,exact in self.routes.get(h,()):
            if not self.remaining():self.incomplete.add(self.effects[e]['oid']);break
            if not self.effects[e]['clean']:continue
            if src['subject'] and src['subject']!=h:
                # A bound subject is never generalized to an entire mapping family.
                ref=self.objects.get(src['subject'],{})
                relevant=keys(self.effects[e]['cell'])
                if not any(t.get('id')==ref.get('decl') for t in walk(relevant) if 'id' in t):continue
            if src['scope'] and e!=src['scope']:continue
            if meaning=='transfer_condition' and k!='guard':continue
            if meaning in RESOURCE|{'fee_rule','price','amount_role'} and k!='value':continue
            if meaning in RESOURCE and (not exact or h in self.objects and self.objects[h]['oid'] is None):continue
            if meaning in {'management_role','eligibility_state'} and k not in ('guard','value','key'):continue
            if meaning=='authorization_quantity' and k!='guard':continue
            if meaning not in RESOURCE|{'fee_rule','price','amount_role','transfer_condition','authorization_quantity','management_role','eligibility_state'}:continue
            dest=self.fact(e,meaning,src['subject'],e,role)
            pre=fid
            # Intermediate facts carry the exact applied path. They are never global node labels.
            for rule in rules:
                link='der_'+digest([fid,e,k,rule,pre])[:20]
                self.logic.rule(link,[pre],rule);pre=link
            # The semantic interpretation and the committing source expression are independent premises.
            observed='sourcefact_'+digest([e,k,self.effects[e]['conditions'],self.effects[e]['version']])[:20]
            self.logic.update(observed,'source_'+observed[11:],True)
            self.logic.rule(dest,[pre,observed],{'key':'P03','value':'P04','guard':'P05'}[k])
            if k=='value' and exact and not src['scope'] and not src['subject']:
                following=self.index_transfer(h,e,fid,pre,'P07')
                if following:yield following

    def for_effect(self,e):
        d=self.effects[e]
        if 'cell' not in d:
            return sorted(fid for fid in self.by_handle[e] if self.logic.valid(fid) and self.facts[fid]['scope'] in (None,e))
        obj=self.obj(d['target'],field_node(d['cell']))
        def applicable(fid):
            f=self.facts[fid]
            if f['scope'] not in (None,e):return False
            if f['handle']==e:return True
            if f['subject']:
                ident=self.objects.get(f['subject'],{}).get('decl')
                if not any(t.get('id')==ident for t in walk(keys(d['cell'])) if 'id' in t):return False
            return True
        return sorted(f for f in self.by_handle[e]|self.by_handle[obj] if self.logic.valid(f) and applicable(f))

    def resource(self,oid,cell):
        """A source-level family reading or an exact, uniform reading of the committing writes."""
        target=self.f.operations[oid]['target'];obj=self.obj(target,field_node(cell))
        roots=[f for f in self.by_handle.get(obj,()) if self.logic.valid(f) and self.facts[f]['meaning'] in RESOURCE and not self.facts[f]['scope'] and not self.facts[f]['subject']]
        es=[e for e in self.by_operation.get(oid,()) if 'cell' in self.effects[e] and key(self.effects[e]['cell'])==key(cell)]
        local=[]
        for e in es:
            rows=[f for f in self.for_effect(e) if self.facts[f]['meaning'] in RESOURCE]
            if not rows:local=[];break
            local.extend(rows)
        effective=roots+local
        meanings={self.facts[f]['meaning'] for f in effective}
        if len(meanings)!=1:return None
        return {'meaning':meanings.pop(),'id':digest(sorted(set(effective))),'target':target,'operation':oid,
                'family':key(cell),'source':'scoped_semantic_support','business_policy_formally_proved':False}

    def managed_resource(self,oid,cell):
        obj=self.obj(self.f.operations[oid]['target'],field_node(cell))
        return any(self.facts[f]['meaning'] in RESOURCE for f in self.by_handle.get(obj,()) if not self.facts[f]['subject'] and not self.facts[f]['scope'])

    def signature(self,oid):
        return sorted({f for e in self.by_operation.get(oid,()) for f in self.for_effect(e)})

    def public(self):
        return {'retired_supports':[{'support':sid,'fact':s['fact'],'field':s['field'],'version':s['version']} for sid,s in self.supports.items() if not s['active']], 'active_supports':[{'support':sid,'fact':row['fact'],'origin':row['origin'],'field':row['field'],'version':row['version']} for sid,row in sorted(self.supports.items()) if row['active']],
                'updates':list(self.events),'revisions':list(self.history),
                'referenced_abstract_effects':[{'effect':h,'operation':self.effects[h]['oid'],'target':self.effects[h]['target'],
                         'kind':self.effects[h]['kind'],'location':self.effects[h]['where'],'committing_branches':len(self.effects[h]['branches']),
                         'dependent_residual':any(b['has_residuals'] for b in self.effects[h]['branches'].values())}
                    for h in sorted({f['handle'] for f in self.facts.values() if f['handle'] in self.effects and 'kind' in self.effects[f['handle']]})],
                'facts':[{'id':fid,'object_or_effect':f['handle'],'meaning':f['meaning'],'role':f['role'],
                          'subject':f['subject'],'scope':f['scope'],'grounded':self.logic.valid(fid)}
                         for fid,f in sorted(self.facts.items())],
                'rule_visits':self.logic.visits,'budget_cut':self.logic.cut,
                'unfinished_operations':sorted(self.incomplete)}

    def related_ops(self, h):
        if h in self.effects:return {self.effects[h]['oid']}
        return set(self.used.get(h,()))

    def focused_consent(self,row):
        """A displayed quantity answer joins the same support as a seed on that debit."""
        origin=getattr(self,'input_origin',None);submission=getattr(self,'submission',None)
        if origin not in ('fixture','verified_service') or not submission or row['meaning'] not in CONSENT:return
        if row['scope'].get('phase') or row['scope'].get('assumptions'):return
        applicable={key(route) for route in row['quantity_scope']};facts=set()
        for e in self.by_operation.get(row['operation'],()):
            if not self.remaining():self.incomplete.add(row['operation']);break
            known={key(route) for route in self.quantity_scopes(e)}
            if not known or not known<=applicable:continue
            fid=self.fact(e,row['meaning'])
            sid='support_'+digest([origin,submission,fid])[:20]
            self.register(fid,sid,origin,'policies');facts.add(fid)
        if facts:
            row['fact_ids']=sorted(facts)
            delta=self.logic.settle()
            self.epoch+=bool(delta)

    def financial_consent(self,oid,route):
        found=set()
        for e in self.by_operation.get(oid,()):
            if self.effects[e].get('path')!=route['path'] or key(self.effects[e]['cell'])!=key(route['ledger']):continue
            for f in self.for_effect(e):
                if self.facts[f]['meaning'] in CONSENT and any(key(s)==key(route) for s in self.quantity_scopes(e)):
                    found.add(f)
        if not found:return None
        modes={self.facts[f]['meaning'] for f in found}
        return {'id':'consent_'+digest(sorted(found))[:20],'meaning':next(iter(modes)) if len(modes)==1 else 'unknown',
                'target':self.f.operations[oid]['target'],'operation':oid,'family':key(route['ledger']),
                'quantity_scope':[route],'scope':{},'source':'scoped_supports','fact_ids':sorted(found)}

    def consumers_for(self,h):
        """Instantiate only operations with a matching source effect, then let compile_property select categories."""
        f=self.f
        effects={h} if h in self.effects else set(self.by_decl.get(h,()))|{t[0] for t in self.routes.get(h,())}
        result=defaultdict(set)
        for e in effects:
            if not self.remaining():self.incomplete.add(self.effects[e]['oid']);break
            d=self.effects[e];oid=d['oid'];facts=self.for_effect(e)
            for fact in facts:
                seed=self.facts[fact];meaning=seed['meaning']
                if f.options.scope=='AC':
                    if meaning in AUTH|{'management_role','eligibility_state','authorization_quantity','other_source_policy','unknown'}:result[(oid,'AC')].add(e)
                    continue
                if meaning in CONSENT:
                    # Intervening controls are structural candidates; the financial consumer still tests the actual effect.
                    for x in f.summaries.dependencies.amounts_for(oid):
                        if x['path']!=d['path']:continue
                        for delta in x['deltas']:
                            if key(delta['cell'])!=key(d['cell']):continue
                            for gate in x['allowance_gates']:
                                for woid in self.writers_for_amount(oid,gate['quantity_expression']):
                                    result[(woid,None)].add(e)
                    continue
                if meaning in RESOURCE|{'price','fee_rule','amount_role','transfer_condition','authorization_quantity','management_role','eligibility_state','unknown','other_source_meaning'}:
                    if meaning=='transfer_condition':
                        for writer in self.by_decl.get(h,()):
                            result[(self.effects[writer]['oid'],None)].add(writer)
                    else:result[(oid,None)].add(e)
        return result

    def writers_for_amount(self,oid,expr):
        dep=self.f.summaries.dependencies
        term=dep.expressions.get(expr,{})
        target=self.f.operations[oid]['target']
        for t in walk(term):
            if t.get('kind')!='storage':continue
            for e in self.by_decl.get(self.obj(target,field_node(t)),()):
                if not self.remaining():return
                wid=self.effects[e]['oid']
                if wid!=oid:yield wid

    def seed_consumers(self,changed):
        relevant=defaultdict(set)
        for h in changed:
            for dest,es in self.consumers_for(h).items():relevant[dest].update(es)
        for (oid,category),es in sorted(relevant.items(),key=lambda r:str(r[0])):
            self.create_consumer(oid,category,es)

    def create_consumer(self,oid,cat,effects):
        inv=self.inv
        qid='scope_'+digest([self.f.identity,oid,cat,sorted(effects)])[:20]
        if qid in inv.issues:return inv.issues[qid]
        item={'id':qid,'anchors':[inv.catalog.name(oid)],'assessment':'investigate','category':cat,
              'claim':'Review the applicable source effect and bound meaning.',
              '_scope_effects':sorted(effects),'_host_source_question':True,'_semantic_consumer':True}
        inv.accept({'issues':[item],'answers':[],'reviewed':[],'diagnostics':[],'usable_analysis':False},host_target=self.f.operations[oid]['target'])
        return inv.issues.get(qid)

    def wire_name(self,h,manifest):
        if not self.visible(h,manifest):return None
        entry=self.effects.get(h) or self.objects[h]
        if h in self.effects:
            if 'cell' in entry:
                name=self.f.lookup(entry['oid']).nodes[field_node(entry['cell'])]['name']
                candidate=self.inv.catalog.name(entry['oid'])+'#'+name
            else:candidate=self.inv.catalog.name(entry['oid'])+'#'+entry['kind']
        elif entry.get('oid'):
            candidate=self.inv.catalog.name(entry['oid'])+'#'+entry['name']
        else:candidate=entry['target'].rsplit(':',1)[-1]+'.'+entry['name']
        if self.bind(candidate,manifest)==h:return candidate
        direct=next((r for r,k in manifest.get('typed_index',{}).items() if k==h),None)
        if direct:return direct
        loc=entry['where']
        span=f"{loc['file']}@{loc['start']}+{loc['length']}"
        return span if self.bind(span,manifest)==h else None

    def labels_for(self,oid,manifest):
        result={}
        for sid,s in self.supports.items():
            if not s['active'] or s['origin'] not in ('fixture','verified_service'):continue
            fact=self.facts[s['fact']];h=fact['handle']
            if oid not in self.related_ops(h) and not any(self.effects[e]['oid']==oid for e in self.by_decl.get(h,())):continue
            name=self.wire_name(h,manifest)
            if not name:continue
            tag='sem:'+sid.split('_')[-1][:12]
            qualifiers={}
            for k in ('scope','subject'):
                qualifier=fact.get(k)
                if qualifier:qualifiers[k]=self.wire_name(qualifier,manifest)
            if any(v is None for v in qualifiers.values()):continue
            result[tag]={'source':name,'support':sid,'version':s['version'],'fact':s['fact'],
                         'field':s['field'],'meaning':fact['meaning'],**qualifiers}
            if fact['role']:result[tag]['role']=fact['role']
        return result

    def describe(self,oid,cat,reason,locations,decision):
        from .source_opinion import DETAIL,EFFECT
        matching={loc_key(loc) for loc in locations}
        es=[e for e in self.by_operation.get(oid,()) if loc_key(self.effects[e]['where']) in matching]
        ids=set()
        for e in es:ids.update(self.for_effect(e))
        att=self.inv.issues.get(decision,{}).get('property') or {}
        for c in att.get('consent_rows',[]):
            for fact in c.get('fact_ids',[]):
                ids.add(fact)
                effect=self.facts[fact]['handle']
                if effect in self.effects and effect not in es:es.append(effect)
        if self.inv.issues.get(decision,{}).get('current',{}).get('_semantic_consumer'):
            for e in self.inv.issues[decision]['current'].get('_scope_effects',()):ids.update(self.for_effect(e))
        origins=set();rules=set();types=set()
        for fid in ids:
            roots,applied=self.logic.basis(fid);origins.update(roots);rules.update(applied)
            types.add(self.facts[fid]['meaning'])
        statement=next(iter(sorted(matching,key=str)),None)
        position=' at source offset '+str(statement[1]) if statement and isinstance(statement[1],int) else ''
        kind=EFFECT.get(cat,'the scoped program effect')
        basis=DETAIL.get(reason,DETAIL['scope_missing'])
        if cat=='AC' and reason in ('source_role_reassignment','applicable_role_guard','guarded_state_change','guarded_source_effect','unguarded_governed_effect') and 'current_authority_required' in types:rules.add('P09')
        interprets=sorted({c['meaning'] for c in att.get('consent_rows',[])})
        if interprets:types.update(interprets)
        lead='The assessment concerns '+kind+position
        if types:lead+=' under '+', '.join(sorted(types))
        wording=lead+'. '+basis
        return {'explanation':wording,'facts':sorted(ids),'rules':sorted(rules),'supports':sorted(origins),'effects':sorted(es),
                'meanings':sorted(types)}

    def source_offices(self,oid):
        from .source_opinion import office_use, identity_guard, blocked_positive
        from .policy_binding import conjuncts
        from .initial_state import initial_for_lookup
        lookup=self.f.lookup(oid)
        state=initial_for_lookup(lookup)
        found={}
        for e in sorted(self.by_operation.get(oid,())):
            if not self.remaining():self.incomplete.add(oid);break
            d=self.effects[e]
            if 'write' not in d:continue
            cell=d['cell'];w=d['write'];rid=cell['root']
            if not d['clean'] or keys(cell) or value_type(cell,lookup) not in ('address','address payable'):continue
            if w['value'].get('kind') not in ('parameter','actual_sender'):continue
            established=(state or {}).get('declarations',{}).get(rid,{})
            use=office_use(self.inv,oid,cell)
            if not use:continue
            startup=bool(established.get('constructor_writes')) and all(p.get('flow') in ('normal','returned') and not p.get('issues') and not p.get('evaluation_gaps') for p in state.get('constructor_paths',())) and all(x.get('value',{}).get('kind') in ('actual_sender','parameter') for x in established.get('constructor_writes',()))
            if not startup:continue
            row=self.f.paths[d['path']]['raw']
            guards=[g for term in row['guards'] for g in conjuncts(term)]
            status='normal' if any(identity_guard(g,{rid}) for g in guards) else 'risk' if not guards else 'open'
            if status=='open':continue
            subject=self.obj(d['target'],rid)
            fid=self.fact(e,'current_authority_required',subject)
            sid='source_'+digest([self.f.identity,e,use,'incumbent_role_use'])[:20]
            self.register(fid,sid,'source_policy_deduction','policies')
            found[e]=(status,fid)
        self.logic.settle()
        return found

    def scope_offices(self):
        if self.f.options.scope!='AC':return
        inv=self.inv
        roots={inv.root(q) for q in inv.issues.values() if not q['current'].get('_host_source_question') or q['current'].get('_semantic_consumer')}
        for oid in sorted(x for x in roots if x):
            offices=self.source_offices(oid)
            if not offices:continue
            for q in list(inv.issues.values()):
                if inv.root(q)!=oid:continue
                locs=q['current'].get('_scope_effects',[])
                if locs:
                    q['office_effects']={e:v for e,v in offices.items() if e in locs}
                    continue
                from .source_opinion import statement_focus
                focus=statement_focus(inv,q,self.f.summaries.rows(oid))
                if focus:
                    matches=[e for e in self.by_operation[oid] if loc_key(self.effects[e]['where'])==loc_key(focus[1]['source'])]
                    q['effect_scope']=matches
                    q['office_effects']={e:v for e,v in offices.items() if e in matches}
                else:q['office_effects']=dict(offices)
            for e in offices:
                if not any(e in q.get('office_effects',{}) for q in inv.issues.values() if inv.root(q)==oid):
                    q=self.create_consumer(oid,'AC',{e})
                    if q:q['office_effects']={e:offices[e]}
            for q in inv.issues.values():
                if inv.root(q)==oid:q.pop('_source_opinion',None)

    def office_opinion(self,q,rows):
        from .source_opinion import opinion,blocked_positive
        lookup=self.f.lookup(self.inv.root(q))
        candidates=dict(q.get('office_effects',{}))
        es=q.get('effect_scope') or q['current'].get('_scope_effects',())
        for e in es:
            d=self.effects[e]
            if 'write' not in d:continue
            for fid in self.for_effect(e):
                f=self.facts[fid]
                if f['meaning']!='current_authority_required':continue
                subject=f.get('subject')
                if subject and self.objects.get(subject,{}).get('decl')!=d['cell']['root']:continue
                if self.f.operations[d['oid']]['target']!=d['target']:continue
                from .source_opinion import office_use,identity_guard
                from .policy_binding import conjuncts
                if not d['clean'] or not office_use(self.inv,d['oid'],d['cell']):continue
                path=self.f.paths[d['path']]['raw'];guards=[g for t in path['guards'] for g in conjuncts(t)]
                status='normal' if any(identity_guard(g,{d['cell']['root']}) for g in guards) else 'risk' if not guards else 'open'
                if status!='open':candidates[e]=(status,fid)
        if not candidates:return None
        for e,(status,fid) in candidates.items():
            d=self.effects[e]
            if status=='risk' and not blocked_positive(self.inv,q,d['path'],'AC'):
                return opinion('risk','source_role_reassignment',[d['where']])
        covered={d['path'] for e,(status,_) in candidates.items() if status=='normal' for d in [self.effects[e]]}
        if covered and {r['path'] for r in rows}<=covered:
            return opinion('normal','applicable_role_guard',[self.effects[e]['where'] for e in candidates])
        return None


    def disputed(self,q):
        oid=self.inv.root(q)
        if not oid:return False
        groups=defaultdict(set)
        for e in self.by_operation.get(oid,()):
            for fid in self.for_effect(e):
                m=self.facts[fid]['meaning']
                if m in RESOURCE:groups[e,'unit'].add(m)
                if m in CONSENT:groups[e,'consent'].add(m)
                if m=='unknown':return True
        return any(len(ms)>1 for ms in groups.values())

    def route_scopes(self,q):
        oid=self.inv.root(q)
        item=q['current']
        explicit=item.get('_scope_effects',()) or q.get('effect_scope',())
        if explicit:return set(explicit)
        from .source_opinion import statement_focus
        if not oid:return set()
        focus=statement_focus(self.inv,q,self.f.summaries.rows(oid))
        if focus:return {e for e in self.by_operation[oid] if loc_key(self.effects[e]['where'])==loc_key(focus[1]['source'])}
        return set(self.by_operation.get(oid,()))

    def authority_cell(self,e,subject):
        d=self.effects[e];lk=self.f.lookup(d['oid'])
        if subject:
            obj=self.objects.get(subject)
            if not obj or obj['target']!=d['target'] or obj['oid'] is not None:return None
            cell={'kind':'storage','root':obj['decl'],'segments':[]}
        else:
            cell=d.get('cell')
        if cell and not cell.get('segments') and value_type(cell,lk) in ('address','address payable'):return cell
        return None

    def authority_effect(self,e,subject):
        """Assess only the located action and the stated principal. Never assume a
        declared address is the policy for every write to a different position."""
        from .policy_binding import conjuncts
        from .source_opinion import identity_guard
        d=self.effects[e];role=self.authority_cell(e,subject)
        if 'cell' not in d:
            if d['kind']=='dangerous_external_call':return 'external_dependency',role
            if not role:return 'policy_scope_unsubstantiated',None
            # Check the guard at the actual effect, before returning to the caller.
            for pid in d['branches']:
                if not self.remaining():return 'policy_effect_unresolved',role
                branch=self.f.summaries.paths[pid]
                occurrences=[term for term in branch['effects'] if term.get('kind')==d['kind'] and loc_key(term['source'])==loc_key(d['where'])]
                if branch['residuals'] or not occurrences:return 'policy_effect_unresolved',role
                for term in occurrences:
                    guards=[g for x in term.get('callpoint_guards',()) for g in conjuncts(x)]
                    if any(key(w['path'])==key(role) for w in term.get('callpoint_writes',())) or not any(identity_guard(g,{role['root']}) for g in guards):
                        return 'policy_scope_unsubstantiated',role
            return 'guarded_source_effect',role
        if role==d['cell']:return 'office',role
        if not role:return 'policy_scope_unsubstantiated',None
        row=self.f.summaries.paths[d['path']]
        def guarded(r):
            # A guard on a prior version cannot authenticate a newly replaced authority.
            return any(identity_guard(g,{role['root']}) for term in r['guards'] for g in conjuncts(term))
        if not d['clean'] or row['effects'] or any(key(w['path'])==key(role) for w in row['ordered_writes'][:d['version']]):
            return 'policy_effect_unresolved',role
        if guarded(row):return 'guarded_state_change',role
        if row['guards']:return 'policy_effect_unresolved',role
        obj=self.obj(d['target'],field_node(d['cell']))
        for other in self.by_decl[obj]:
            if not self.remaining():return 'policy_effect_unresolved',role
            peer=self.effects[other]
            if peer['oid']==d['oid'] or not peer['clean'] or key(peer['cell'])!=key(d['cell']):continue
            # Cross-entry consent for keyed state requires additional holder/key evidence.
            if d['cell'].get('segments') or value_type(d['cell'],self.f.lookup(d['oid']))!='bool':continue
            now,other_value=d['write']['value'],peer['write']['value']
            if not all(x.get('kind')=='literal' and type(x.get('value')) is bool for x in (now,other_value)) or now['value']==other_value['value']:continue
            comp=self.f.summaries.paths[peer['path']]
            if comp['effects'] or any(key(w['path'])==key(role) for w in comp['ordered_writes'][:peer['version']]) or not guarded(comp):continue
            # A known public writer of the same applied setting and same outcome
            # is a normal alternative to the claimed control over that outcome.
            for writer in self.by_decl[obj]:
                if not self.remaining():return 'policy_effect_unresolved',role
                other=self.effects[writer]
                if other['oid']==d['oid'] or key(other['cell'])!=key(d['cell']) or key(other['write']['value'])!=key(now):continue
                other_row=self.f.summaries.paths[other['path']]
                if other['clean'] and not other_row['effects'] and not other_row['guards']:return 'policy_scope_unsubstantiated',role
            return 'unguarded_governed_effect',role
        return 'policy_scope_unsubstantiated',role

    def effect_policy_opinion(self,q):
        if self.f.options.scope!='AC' or not q['current'].get('_semantic_consumer'):return None
        from .source_opinion import opinion,blocked_positive
        out=[];located=[];policy_sources=set()
        for e in self.route_scopes(q):
            d=self.effects[e]
            if d['oid']!=self.inv.root(q):continue
            for fid in self.for_effect(e):
                fact=self.facts[fid]
                if fact['meaning']=='current_authority_required':
                    status,role=self.authority_effect(e,fact['subject'])
                    if status=='office':continue
                    if status=='unguarded_governed_effect' and blocked_positive(self.inv,q,d['path'],'AC'):status='policy_effect_unresolved'
                    out.append(status);located.append(d['where']);policy_sources.add(fact['subject'])
                elif 'cell' not in d and fact['meaning'] in ('unknown','other_source_policy'):
                    out.append('external_dependency' if d['kind']=='dangerous_external_call' else 'policy_missing')
                    located.append(d['where'])
        if not out:return None
        if len(policy_sources)>1:return opinion('open','policy_scope_unsubstantiated',located)
        if 'unguarded_governed_effect' in out:return opinion('risk','unguarded_governed_effect',located)
        protected={'guarded_state_change','guarded_source_effect'}
        if set(out)<=protected:return opinion('normal','guarded_source_effect' if 'guarded_source_effect' in out else 'guarded_state_change',located)
        reason=next(v for v in out if v not in protected)
        return opinion('open',reason,located)

    def policy(self,q):
        if not self.inv.root(q):return None
        fs=[(self.facts[f],f,e) for e in sorted(self.route_scopes(q)) for f in self.for_effect(e) if self.facts[f]['meaning'] in AUTH]
        if not fs:return None
        if len({(r['meaning'],r['subject'],e) for r,f,e in fs})!=1:return None
        r,fid,e=fs[0];d=self.effects[e];lookup=self.f.lookup(d['oid'])
        if r['meaning']=='holder_authorization_applies':
            if 'cell' not in d:return None
            grant=key_relation(d['cell'],lookup);ordered=keys(d['cell'])
            if not grant or grant.get('kind')!='authorization_quantity' or len(ordered)!=2:return None
            subject=ordered[grant['holder_key']]
            if r['subject'] and self.objects[r['subject']]['decl']!=subject.get('id',subject.get('root')):return None
            return {'meaning':'required_authorization','polarity':'asserted','level':'H','semantic_fact':fid,
                    'explicit_policy_kind':r['meaning'],'qualified_cell':subject,'binding_effect':e,
                    'text':'The actual holder issues this grant.','source_anchors':q['current']['anchors']}
        if r['meaning']=='initialization_stage':
            if not r.get('subject'):return None
            flag={'kind':'storage','root':self.objects[r['subject']]['decl'],'segments':[]}
            if value_type(flag,lookup)!='bool':return None
            if not any(key(w['path'])==key(flag) and w['value'].get('value') is True for row in self.f.summaries.rows(d['oid']) for w in row['ordered_writes']):return None
            return {'meaning':'required_authorization','polarity':'asserted','level':'H','semantic_fact':fid,'explicit_policy_kind':r['meaning'],
                    'qualified_cell':flag,'binding_effect':e,'text':'The located one-time stage limits this effect.','source_anchors':q['current']['anchors']}
        if r['meaning']=='current_authority_required':
            reason,sub=self.authority_effect(e,r['subject'])
            if reason not in ('office','guarded_state_change','guarded_source_effect','unguarded_governed_effect') or not sub:return None
            return {'meaning':'required_authorization','polarity':'asserted','level':'H','semantic_fact':fid,
                    'explicit_policy_kind':r['meaning'],'qualified_cell':sub,'binding_effect':e,
                    'text':'The incumbent qualifies the recorded change.','source_anchors':q['current']['anchors']}
        return None


    def disputed_effects(self,q):
        oid=self.inv.root(q)
        if not oid:return set()
        pairs=[]
        effects=set(q['current'].get('_scope_effects',())) or self.by_operation.get(oid,set())
        for e in effects:
            groups=defaultdict(set)
            for fid in self.for_effect(e):
                meaning=self.facts[fid]['meaning']
                if meaning in RESOURCE:groups['resource'].add(meaning)
                if meaning in CONSENT:groups['consent'].add(meaning)
            if any(len(s)>1 for s in groups.values()):pairs.append(e)
        return set(pairs)

    def describe_source(self,oid,cat,reason,locations,qid):
        row=self.describe(oid,cat,reason,locations,qid)
        q=self.inv.issues[qid]
        evidence=[self.inv.evidence[e] for e in q['evidence']]
        prop=q.get('property') or {}
        modes={v['meaning'] for v in prop.get('consent_rows',[])}
        if modes=={'net_request_with_fee'} and cat=='FCR-DESTROY' and reason in ('scope_missing','scoped_fee_consent','program_support'):
            row['explanation']=('The matched holder allowance uses the net request and its disclosed fee. '+
               ('The applicable check excludes an uncompensated debit under that effective grant.' if reason=='scoped_fee_consent' else
                'The authorization may be zero on the pertinent debit; the recorded net interpretation alone cannot exclude loss.' if reason=='scope_missing' else
                'The matched debit still has a source-supported loss after applicable consent.'))
        if modes=={'gross_debit_bound'} and cat in ('FCR-TRANSFER','FCR-DESTROY') and reason in ('program_support','source_certificate'):
            row['explanation']='The holder-issued bound applies to the gross debit of this request. The same-scope program evidence supports loss beyond the bound.'
        if any(v.get('kind')=='source_inspection' for v in evidence):row['origins']=['source_observation']
        else:row['origins']=[]
        row['origins']+=sorted({self.supports[s]['origin'] for s in row['supports'] if s in self.supports})
        if row['rules']:row['origins'].append('rule_derivation')
        if reason in ('program_support','source_check_excluded') and any(v.get('queries') for v in evidence):row['origins'].append('scoped_program_check')
        if modes:
            if any(c.get('source')=='focused_source_bound_semantic_answer' for c in prop.get('consent_rows',[])):row['origins'].append('source_bound_semantic_answer')
        return row

    def matching_dispute(self,q):
        """A source-typed financial interpretation stays unresolved only when its two meanings matter."""
        es=self.disputed_effects(q)
        if not es:
            why=self.unresolved(q)
            if why:return dict(status='open',reason=why,locations=[self.f.operations[self.inv.root(q)]['source']])
            if self.f.options.scope=='FCR' and q['current'].get('_semantic_consumer') and not q['current'].get('category'):
                effects=self.route_scopes(q)
                if effects and all('write' in self.effects[e] and self.effects[e]['clean'] and local_delta(self.effects[e]['write'])[0] and
                        {self.facts[f]['meaning'] for f in self.for_effect(e)}=={'nonfinancial_counter'} and
                        self.local_counter(e) for e in effects):
                    return dict(status='normal',reason='scoped_counter',locations=[self.effects[e]['where'] for e in sorted(effects)])
            return None
        return {'status':'open','reason':'conflicting_scoped_meanings','locations':[self.effects[e]['where'] for e in sorted(es)]}



    def local_counter(self,e):
        # Use the already registered dependency summary. An unfinished search cannot close a use.
        d=self.effects[e]
        summary=self.f.summaries.dependencies.forward_cache.get(d['oid'])
        if not summary or not summary['fixed_point_over_indexed_definitions'] or summary['residuals']:return False
        uses=summary['uses']
        if any(not self.f.operations[u].get('generated_getter') for u in uses):return False
        from .ledger import _unit_origin
        return not _unit_origin(self.inv.backend,d['oid'],d['cell'])

    def legacy_resource(self,oid,cell,meaning,scope):
        receipt=getattr(self,'legacy_receipt',None)
        if not receipt or not self.built or scope.get('phase') or scope.get('assumptions'):return
        target=self.f.operations[oid]['target'];obj=self.obj(target,field_node(cell))
        if obj not in self.objects:return
        source,submission=receipt
        if source not in ('verified_service','fixture') or not submission:return
        fid=self.fact(obj,meaning)
        sid='support_'+digest([source,submission,fid])[:20]
        if self.register(fid,sid,source,'annotations'):
            self.derive(fid);self.logic.settle()

    def planning_read(self,q):
        if not q['current'].get('_semantic_consumer'):return
        for e in q['current'].get('_scope_effects',()):
            if e not in self.effects:continue
            d=self.effects[e]
            for fid in self.for_effect(e):
                meaning=self.facts[fid]['meaning']
                if not self.remaining():self.incomplete.add(d['oid']);return
                if meaning in ('price','fee_rule','amount_role') and 'cell' in d:
                    obj=self.obj(d['target'],field_node(d['cell']))
                    for sink,k,rs,exact in self.routes.get(obj,()):
                        if not self.remaining():self.incomplete.add(d['oid']);return
                        use=self.effects[sink]['oid']
                        if k=='value' and use!=d['oid']:
                            q.setdefault('semantic_read_dependencies',set()).add(use)
                            self.inv.enqueue(q['id'],'inspect',{'operation':use,'enhance':False},2,'source_quantity_consumer')
                if meaning in ('authorization_quantity','eligibility_state','transfer_condition'):
                    self.inv.enqueue(q['id'],'inspect',{'operation':d['oid'],'enhance':False},1,'condition_subject_and_use')


    def withdrawn_dependency(self,e):
        d=self.effects[e]
        if any(self.facts[f]['meaning'] in RESOURCE for f in self.for_effect(e)):return False
        for support in self.supports.values():
            if support['active'] or not support.get('withdrawn'):continue
            row=self.facts[support['fact']];h=row['handle']
            if row['meaning'] not in RESOURCE:continue
            if h==e or h==self.obj(d['target'],field_node(d['cell'])) or any(dest==e and kind=='value' for dest,kind,_,_ in self.routes.get(h,())):return True
        return False

    def index_transfer(self,src,e,fid,pre,rule):
        dest=self.facts[fid]
        obj=self.obj(self.effects[e]['target'],field_node(self.effects[e]['cell']))
        if self.objects.get(src,{}).get('oid') is not None or src==obj or not self.effects[e]['clean']:return
        w=self.effects[e]['write']
        if keys(w['path']) or w['value'].get('kind')!='storage' or keys(w['value']):return
        # Only cells whose every committing writer copies this very source may export that interpretation.
        # It describes a value family, not the existence of a reachable transition or consent.
        writers=self.by_decl[obj]
        if any(not self.effects[q]['clean'] or key(self.effects[q]['write']['value'])!=key(w['value']) for q in writers):return
        if dest['meaning'] not in ('price','fee_rule','amount_role','eligibility_state','management_role'):return
        nxt=self.fact(obj,dest['meaning'],None,None,dest['role'])
        self.logic.rule(nxt,[pre],rule)
        return nxt

    def semantic_questions_for(self,q):
        oid=self.inv.root(q)
        if not oid:return []
        effects=q['current'].get('_scope_effects') or self.by_operation.get(oid,set())
        await_more=set()
        for e in effects:
            if e not in self.effects:continue
            fs=self.for_effect(e)
            for fid in fs:
                m=self.facts[fid]['meaning']
                if m in ('unknown','other_source_meaning','other_source_policy'):
                    await_more.add(e)
        await_more.update(self.disputed_effects(q))
        if not await_more:return []
        return [{'kind':'scoped_support_dispute','id':'dispute_'+digest([oid,sorted(await_more)])[:12],
                 'question':'Clarify the shown meaning on this effect. Correct, narrow or withdraw its support using an applicable source reason.'}]

    def unresolved(self,q):
        if self.disputed_effects(q):return 'conflicting_scoped_meanings'
        for e in self.route_scopes(q):
            if e not in self.effects:continue
            d=self.effects[e]
            if 'cell' not in d:continue
            lookup=self.f.lookup(d['oid']);roots=self.for_effect(e)
            labels={self.facts[f]['meaning'] for f in roots}
            quantity_only='amount_role' in labels and not labels.intersection(RESOURCE) and q['current'].get('_semantic_consumer')
            if self.withdrawn_dependency(e) or quantity_only or 'unknown' in labels and not labels-{'unknown','other_source_meaning','other_source_policy'}:
                if keys(d['cell']) and holder(d['cell'],lookup) is not None:
                    from .ledger import _unit_origin
                    if _unit_origin(self.inv.backend,d['oid'],d['cell']) is None:return 'source_unit_missing'
        return None
