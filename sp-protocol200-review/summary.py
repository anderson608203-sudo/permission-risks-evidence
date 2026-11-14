"""Neutral committed effects and source-bound semantic interpretations.

This is one shared access layer for planning, encoding and coverage.  The source
paths already contain compiler-resolved calls/modifiers; no business detector or
new state interpreter is introduced here.  An interpretation never changes M1's
frozen initial-state eligibility.
"""
import copy
import re
from collections import deque
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, value_type, selector_relation
from pr_next_joint.verification.sequence import read
from .initial_state import family, domain
from pr_next_joint.verification.expressions import Unsupported


def unique(values):
    return list({key(v): v for v in values}.values())


def has_basis(text):
    # A short source explanation may be Chinese or another unspaced language;
    # an English word-count threshold is not a semantic protocol requirement.
    return isinstance(text,str) and len(re.sub(r'\W','',text,flags=re.UNICODE))>=6


def holder(cell, lookup):
    """A holder is an actual address key, not a field name or arbitrary integer."""
    from .key_roles import relation
    bound=relation(cell,lookup)
    if bound and len(keys(cell))>bound['holder_key']:return keys(cell)[bound['holder_key']]
    addresses=[k for k in keys(cell) if k.get('kind') in ('actual_sender','contract_address') or
               k.get('type') in ('address','address payable')]
    if len(addresses)==1:return addresses[0]
    if len(addresses)>1:return None
    # Reuse the existing source-owned record case: a non-address record ID
    # may contain one unambiguous address field holding the entitlement owner.
    # An integer key itself is never reinterpreted as that owner.
    segments=cell.get('segments',[])
    if keys(cell) and segments and 'field' in segments[-1]:
        node=lookup.nodes.get(segments[-1]['field'],{})
        record=lookup.nodes.get(node.get('scope'),{})
        addresses=[n for n in record.get('members',[]) if
                   n.get('typeDescriptions',{}).get('typeString') in ('address','address payable')]
        if len(addresses)==1:
            return {'kind':'storage','root':cell['root'],
                    'segments':copy.deepcopy(segments[:-1])+[{'field':addresses[0]['id']}]}
    return None


def directions(cell, after):
    # Only a may classification. All positive/negative claims use actual values.
    if key(cell) == key(after):
        return []
    if after.get('kind') == 'literal' and after.get('value') in (0, '0'):
        return ['debit']
    if after.get('kind') == 'op' and len(after.get('args', [])) == 2:
        a, b = after['args']
        if key(a) == key(cell):
            if after['op'] == '+': return ['credit']
            if after['op'] == '-': return ['debit']
        if key(b) == key(cell) and after['op'] == '+': return ['credit']
    return ['debit', 'credit']


def local_delta(write):
    """Source write delta before cross-key alias composition; never a net claim."""
    inc=write.get('local_increment');operator=write.get('operator')
    if inc is not None:
        if inc.get('op')=='-' and len(inc.get('args',[]))==2 and inc['args'][0].get('value')==0:
            return '-',inc['args'][1]
        return '+',inc
    v=write['value'];args=v.get('args',[])
    if v.get('op') in ('+','-') and len(args)==2 and key(args[0])==key(write['path']):return v['op'],args[1]
    if v.get('kind')=='literal' and type(v.get('value')) is int and v['value']==0:
        return '-',write['path']
    return None,None


def debited_positions(f,oid):
    """Who is actually used as the debit operand, with its source quantity."""
    rows=[]
    for pid,p in f.operation_paths(oid,True):
        for w in p['writes']:
            sign,amount=local_delta(w)
            if sign!='-':continue
            account=holder(w['path'],f.lookup(oid))
            from .key_roles import relation
            if account is None or (relation(w['path'],f.lookup(oid)) or {}).get('kind')=='authorization_quantity':continue
            rows.append({'cell':w['path'],'holder':account,'amount':amount,'path':pid,'source':w['source']})
    return unique(rows)


def path_summary(f, oid, pid, p):
    lookup = f.lookup(oid)
    cells = unique(w['path'] for w in p.get('writes', []))
    numeric = [];local_residuals=[]
    for c in cells:
        try:
            typ = value_type(c, lookup)
            if not re.fullmatch(r'u?int\d*', typ or ''): continue
            after = read(c, p['writes'], lookup)
        except (Unsupported,ValueError,TypeError,KeyError) as error:
            local_residuals.append({'cell':copy.deepcopy(c),'reason':'summary_position:'+type(error).__name__+':'+str(error)})
            continue
        from .key_roles import relation
        role=relation(c,lookup)
        numeric.append({'cell': copy.deepcopy(c), 'family': family(c),'key_role':copy.deepcopy(role),
            'before': copy.deepcopy(c), 'after': after, 'type': typ,
            'holder': holder(c, lookup), 'may_directions': directions(c, after),
            'sources': [w['source'] for w in p['writes'] if selector_relation(w['path'], c) == 'same_shape']})
        if len([a for a in keys(c) if a.get('kind') in ('actual_sender','contract_address') or
                a.get('type') in ('address','address payable')])>1 and not role:
            local_residuals.append({'cell':copy.deepcopy(c),'reason':'multiple_address_keys_need_source_holder_binding'})
    gaps = copy.deepcopy(p.get('issues', []) + p.get('evaluation_gaps', []))+local_residuals
    return {'operation': oid, 'path': pid, 'target': f.operations[oid]['target'],
        'flow': p.get('flow'), 'committing': p.get('flow') in ('normal', 'returned'),
        'guards': copy.deepcopy(p.get('guards', [])), 'ordered_writes': copy.deepcopy(p.get('writes', [])),
        'numeric_effects': numeric, 'effects': copy.deepcopy(p.get('sensitive_effects', [])),
        'return_value': copy.deepcopy(p.get('return_value')), 'residuals': gaps,
        'precision': 'path_conditioned' if not gaps else 'may_with_residual',
        'net_effect_not_operation_spelling': True}


class Summaries:
    def __init__(self, f):
        self.f = f; self.paths = {}; self.operations = {}; self.propagation = []
        from .key_roles import derive
        self.key_roles=derive(f)
        # Worklist propagates source provenance of actually inlined effects.  It
        # does not re-resolve static referencedDeclaration or override dispatch.
        source_users = {}
        for oid, o in f.operations.items():
            rows = [path_summary(f, oid, pid, p) for pid, p in f.operation_paths(oid)]
            self.operations[oid] = {'operation': oid, 'target': o['target'], 'paths': [],
                'residuals': copy.deepcopy(o.get('gaps', [])), 'source_closure': []}
            for row in rows:
                self.paths[row['path']] = row; self.operations[oid]['paths'].append(row['path'])
                for w in row['ordered_writes']:
                    a = w['source']; token = key([o['target'], a.get('file'), a.get('start'), a.get('length')])
                    source_users.setdefault(token, set()).add(oid)
                    self.operations[oid]['source_closure'].append(a)
            self.operations[oid]['source_closure'] = unique(self.operations[oid]['source_closure'])
        # Finite union lattice over compiler-resolved entry effects.  Shared
        # helper provenance can be reused, but effects/guards remain on paths.
        queue = deque(sorted(self.operations)); seen = set(); rounds = 0
        while queue:
            oid = queue.popleft(); rounds += 1
            for a in self.operations[oid]['source_closure']:
                token = key([f.operations[oid]['target'], a.get('file'), a.get('start'), a.get('length')])
                for other in sorted(source_users.get(token, ())):
                    edge = (oid, other, token)
                    if oid == other or edge in seen: continue
                    seen.add(edge); self.propagation.append({'from': oid, 'to': other,
                        'source': a, 'kind': 'shared_resolved_effect_origin',
                        'guards_and_values_not_cross_merged': True})
        self.identity = digest([self.paths, self.propagation])
        self.rounds = rounds
        self._dependencies = None

    @property
    def dependencies(self):
        if self._dependencies is None:
            from .dependencies import Dependencies
            self._dependencies = Dependencies(self)
        return self._dependencies

    def rows(self, oid, committing=True):
        return [self.paths[p] for p in self.operations[oid]['paths']
                if not committing or self.paths[p]['committing']]

    def structural_fact_key(self, oid):
        cache=self.__dict__.setdefault('_structural_fact_keys',{})
        if oid not in cache:
            entry=self.f.operations[oid]
            cache[oid]=digest([self.f.bundle['program_id'],self.f.bundle['build_id'],entry['target'],entry['source'],
                [(r['path'],r['guards'],r['ordered_writes'],r['effects'],r['residuals']) for r in self.rows(oid,False)]])
        return cache[oid]

    def effect_fact_key(self, oid):
        """Content identity of this applied, ordered source effect in its host domain."""
        from .initial_state import domain, initial_for_lookup
        cache = self.__dict__.setdefault('_effect_fact_keys',{})
        if oid not in cache:
            target=self.f.operations[oid]['target']
            lookup=self.f.lookup(oid)
            rows=self.rows(oid,False)
            cache[oid]=digest([self.f.identity,self.structural_fact_key(oid),target,self.f.operations[oid]['source'],domain(lookup),
                initial_for_lookup(lookup)['identity'],[(r['path'],r['guards'],r['ordered_writes'],
                r['numeric_effects'],r['effects'],r['residuals']) for r in rows]])
        return cache[oid]

    def positions(self, oid):
        return unique(e['cell'] for r in self.rows(oid) for e in r['numeric_effects'] if e['holder'] is not None
                      and (e.get('key_role') or {}).get('kind')!='authorization_quantity')

    def control_only(self,cell,target):
        """A control of another position is not that position's financial unit."""
        from .key_roles import relation
        if (relation(cell,self.f.lookups[target]) or {}).get('kind')=='authorization_quantity':return True
        for oid,o in self.f.operations.items():
            if o['target']!=target:continue
            for r in self.rows(oid):
                if not any(selector_relation(s,cell)=='same_shape' for s in selectors(r['guards'])):continue
                own=[e for e in r['numeric_effects'] if selector_relation(e['cell'],cell)=='same_shape']
                other=[e for e in r['numeric_effects'] if e['holder'] is not None and selector_relation(e['cell'],cell)!='same_shape']
                if other and not own:return True
        return False

    def movements(self, oid, path):
        lookup = self.f.lookup(oid)
        row = path_summary(self.f, oid, 'transient_path', path)
        return {s: unique(e['cell'] for e in row['numeric_effects'] if e['holder'] is not None
                         and (e.get('key_role') or {}).get('kind')!='authorization_quantity'
                         and d in e['may_directions']) for s, d in (('-', 'debit'), ('+', 'credit'))}

    def record(self):
        return {'schema': 'neutral-effect-summary-v1', 'identity': self.identity,
            'operations': self.operations, 'paths': self.paths, 'propagation': self.propagation,'source_key_roles':self.key_roles,
            'value_and_control': {'id':self._dependencies.identity,'artifact':'value_control_dependencies.json'}
            if self._dependencies is not None else None,
            'worklist_rounds': self.rounds, 'fixed_point':not any(r['residuals'] for r in self.paths.values()),
            'finite_extracted_worklist_completed':True,
            'scope': 'finite already compiler-resolved paths; residuals are not completed paths'}


def get_summaries(f):
    if not hasattr(f, 'summaries'): f.summaries = Summaries(f)
    return f.summaries


class Semantics:
    """Versioned H bindings. No Gold, source-name rules or mutable state domain."""
    def __init__(self, f):
        self.f = f; self.resources = {}; self.history = []; self.questions = {};self.consents={}
        self.version = 0;self.active_scope={'phase':None,'assumptions':[]}

    def scope(self,item):
        self.active_scope={'phase':copy.deepcopy(item.get('phase')),'assumptions':copy.deepcopy(item.get('assumptions',[]))}
        return self.active_scope

    def lookup(self, oid, cell):
        target=self.f.operations[oid]['target'];scope=self.active_scope
        scoped=self.resources.get(key([target,family(cell),scope]))
        explicit = self.rules.resource(oid,cell) if getattr(self,'rules',None) else None
        if scoped:return scoped
        if explicit or getattr(self,'rules',None) and self.rules.managed_resource(oid,cell):return explicit
        return self.resources.get(key([target,family(cell)]))

    def dependency_identity(self,operations,consent_operations=None):
        operations=set(operations)
        consent_operations=operations if consent_operations is None else set(consent_operations)
        families={key([self.f.operations[o]['target'],family(c)]) for o in operations for c in get_summaries(self.f).positions(o)}
        bound=[r['id'] for r in self.resources.values() if
               (key([r['target'],r['family']]) in families or operations.intersection(r['operations'])) and
               (not r.get('scope') or r['scope']==self.active_scope)]
        bound += [r['id'] for r in self.consents.values() if consent_operations.intersection(r['operations']) and
                  r.get('scope')==self.active_scope]
        rules=getattr(self,'rules',None)
        if rules:bound.extend(f for oid in operations for f in rules.signature(oid))
        return digest(sorted(set(bound)))

    def lookup_consent(self,oid,cell,route=None):
        if route and getattr(self,'rules',None):
            explicit=self.rules.financial_consent(oid,route)
            if explicit:return explicit
        matches=[v for v in self.consents.values() if v['target']==self.f.operations[oid]['target'] and v['operation']==oid and v['family']==family(cell) and v['scope']==self.active_scope and (not route or route in v['quantity_scope'])]
        return matches[0] if matches and len({v['meaning'] for v in matches})==1 else None

    def _set(self, oid, cell, meaning, basis, issue, source, operations, assertion=None):
        if not has_basis(basis):
            return None
        f = self.f; lookup = f.lookup(oid)
        if holder(cell, lookup) is None or not re.fullmatch(r'u?int\d*', value_type(cell, lookup) or ''):
            return None
        positions = [p for op in operations for p in get_summaries(f).positions(op)
                     if selector_relation(p, cell) == 'same_shape']
        if not positions: return None
        scope=copy.deepcopy(self.active_scope)
        scoped=bool(scope.get('phase') or scope.get('assumptions'))
        k = key([f.operations[oid]['target'], family(cell),scope]) if scoped else key([f.operations[oid]['target'], family(cell)])
        row = {'target': f.operations[oid]['target'], 'family': family(cell),
            'cell': copy.deepcopy(cell), 'meaning': meaning, 'basis': basis,
            'operations': sorted(operations), 'positions': unique(positions), 'issue': issue,
            'source': source, 'evidence_level': 'source_and_semantic_prediction',
            'economic_meaning_formally_proved': False,
            'analysis_domain': domain(lookup), 'semantic_assertion':copy.deepcopy(assertion)}
        row['scope']=scope if scoped else None
        if getattr(self,'rules',None):self.rules.legacy_resource(oid,cell,meaning,scope)
        previous = self.resources.get(k)
        if previous and previous['meaning']==meaning and previous['operations']==row['operations'] and (
                previous.get('semantic_assertion') or {}).get('unit_kind')==(assertion or {}).get('unit_kind'):
            return previous
        self.version += 1; row['version'] = self.version
        row['id']='sem_'+digest([self.f.identity,k,meaning,(assertion or {}).get('unit_kind'),row['operations']])[:20]
        self.history.append({'before': copy.deepcopy(previous), 'after': copy.deepcopy(row),
                             'derived_cache_invalidation': 'affected binding and dependent properties only',
                             'frozen_initial_state_unchanged': True})
        self.resources[k] = row
        return row

    def consume_issue(self, binding, item):
        ops=binding.get('operations',[]);root=binding.get('core_operation')
        if root is None:return []
        from .semantic_claims import resource_assertion,clauses
        text=' '.join(str(item.get(x)or'')for x in ('claim','resource_basis','resource_kind'))
        candidates=unique(c for o in ops for c in get_summaries(self.f).positions(o))
        lookup=self.f.lookup(root);target=self.f.operations[root]['target']
        # Source entities, not a word shared by the whole paragraph, delimit
        # the meaning/negation attached to each individual position.
        all_positions=unique(c for o,v in self.f.operations.items()if v['target']==target
                             for c in get_summaries(self.f).positions(o))
        def labels(c):
            ids=[c['root']]+[s['field']for s in c.get('segments',[])if 'field'in s]
            return [lookup.nodes.get(i,{}).get('name')for i in ids if lookup.nodes.get(i,{}).get('name')]
        def names(part,c):
            return any(re.search(r'(?<![\w$])'+re.escape(n)+r'(?![\w$])',part)for n in labels(c))
        selected=[];parts=[c for c,_ in clauses(text)]
        for cell in candidates:
            if get_summaries(self.f).control_only(cell,target):continue
            anchored=[part for part in parts if names(part,cell)]
            # With one unambiguous source family, the following sentence can
            # refer to "the holder's balance" without repeating its Solidity
            # spelling. Preserve that explanation and its sentence boundaries.
            # Multiple families still require their own named clauses.
            if len({family(c)for c in candidates})==1 and not any(names(text,c)for c in all_positions if family(c)!=family(cell)):
                anchored=[text]
            elif not anchored:continue
            basis='; '.join(anchored);assertion=resource_assertion(basis)
            if not assertion['meaning']:continue
            previous=self.lookup(root,cell)
            if previous and previous.get('source')=='focused_model_answer':selected.append(previous);continue
            row=self._set(root,cell,assertion['meaning'],basis,item['id'],'original_model_source_claim',ops,assertion)
            if row:selected.append(row)
        return selected

    def question(self, q, oid, cell=None, kind='resource',quantity_scope=None):
        obj = family(cell) if cell is not None else None
        core=q['binding'].get('core_operation')
        identity=[q['id'],core,oid,obj,kind,self.active_scope]
        if quantity_scope is not None:identity.append(quantity_scope)
        sid = 'sq_' + digest(identity)[:16]
        # A resource question denotes a typed storage family. Keep its first
        # representative cell stable between registration, actual message and
        # answer consumption; encountering the recipient cell must not mutate
        # the same ID after the sender cell was already delivered.
        if sid in self.questions:return copy.deepcopy(self.questions[sid])
        row = {'id': sid, 'issue': q['id'], 'operation': oid, 'kind': kind,'core_operation':core,
            'cell': copy.deepcopy(cell), 'target': self.f.operations[oid]['target'],
            'semantic_scope':copy.deepcopy(self.active_scope),
            'question': ('What right does this source-bound account field represent, and which shown use supports that meaning?'
                         if kind == 'resource' else 'Which source-backed authorization applies to this effect, including normal alternatives?'),
            'choices': ['financial_right', 'nonfinancial_counter', 'unknown', 'other_source_explanation'] if kind == 'resource'
                       else ['required_authorization', 'normal_authorization', 'unknown', 'other_source_explanation'],
            'source_name': self.f.lookup(oid).nodes.get(cell['root'], {}).get('name') if cell else None,
            'related_uses': [self.f.operations[o]['function'] for o in q['binding']['operations']],
            'answer_contract': 'question + answer + short basis; existing entity is already bound; no risk/AST/SMT required'}
        self.questions[sid] = row
        if kind=='financial_consent':
            row.update(question='For this actual holder-issued authorization and dependent request, what quantity does the holder authorize? Explain whether it bounds the final holder debit including fees, or authorizes the checked net request with its disclosed fee rule; preserve the holder, ordered keys, amount, use and phase. A difference between gross and net alone does not decide this policy.',
                choices=['gross_debit_bound','net_request_with_fee','unknown','other_source_explanation'])
        return row

    def consume_answer(self, answer, allowed, issues):
        sid = answer.get('question'); sq = self.questions.get(sid)
        if not sq or sid not in allowed:
            return None, 'semantic_answer_outside_sent_scope'
        text = str(answer.get('answer') or '').strip(); basis = str(answer.get('basis') or '').strip()
        if not text or not has_basis(basis): return None, 'semantic_answer_missing_explanation'
        q = issues.get(sq['issue'])
        if not q: return None, 'semantic_question_issue_missing'
        if q['binding'].get('core_operation')!=sq.get('core_operation'):
            return None,'semantic_answer_core_changed_since_sent'
        self.scope(q['current'])
        if self.active_scope!=sq['semantic_scope']:return None,'semantic_answer_scope_changed_since_sent'
        if sq['kind'] == 'resource':
            from .semantic_claims import resource_assertion
            assertion=resource_assertion(basis,answer=text)
            if text not in ('financial_right','token_ledger','redeemable_credit','nonfinancial_counter'):
                assertion=resource_assertion(text+' '+basis)
            if not assertion['meaning']: return None, 'semantic_meaning_or_explanation_polarity_unresolved'
            row = self._set(sq['operation'], sq['cell'], assertion['meaning'],
                            basis, q['id'], 'focused_model_answer', q['binding']['operations'],assertion)
            return row, None if row else 'semantic_entity_or_source_effect_not_supported'
        if sq['kind']=='financial_consent':
            if text not in ('gross_debit_bound','net_request_with_fee','unknown'):
                return None,'financial_consent_meaning_unresolved'
            if not sq.get('quantity_scope') or sq['operation'] not in self.f.operations:
                return None,'financial_consent_source_quantity_not_bound'
            row={'id':'consent_'+digest([sq,answer])[:20],'meaning':text,'basis':basis,
                'issue':q['id'],'operation':sq['operation'],'target':sq['target'],'family':family(sq['cell']),
                'quantity_scope':copy.deepcopy(sq['quantity_scope']),'scope':copy.deepcopy(self.active_scope),
                'operations':sorted(set(q['binding']['operations'])|{sq['operation']}),
                'source':'focused_source_bound_semantic_answer','evidence_level':'H',
                'business_policy_formally_proved':False,'original_answer':copy.deepcopy(answer)}
            token=key([sq['target'],sq['operation'],family(sq['cell']),self.active_scope,row['quantity_scope']])
            if getattr(self,'rules',None):self.rules.focused_consent(row)
            previous=self.consents.get(token)
            row['id']='consent_'+digest([self.f.identity,token,text,row['quantity_scope']])[:20]
            if previous and previous['id']==row['id']:return previous,None
            self.consents[token]=row;self.version+=1
            self.history.append({'before':copy.deepcopy(previous),'after':copy.deepcopy(row),
                'derived_cache_invalidation':'dependent quantity properties; other policies unchanged',
                'frozen_initial_state_unchanged':True})
            return row,None
        from .relations import statement
        interpretation = statement(basis + ' ' + text, choice=text)
        row = {'id': 'auth_' + digest([sq, answer])[:20], 'meaning': interpretation['meaning'],
               'text': basis + ' ' + text, 'polarity': interpretation['polarity'],
               'original_answer': copy.deepcopy(answer),
            'basis': basis, 'issue': q['id'], 'operation': sq['operation'],
            'source': 'focused_model_answer', 'target': sq['target'],
            'evidence_level': 'source_and_semantic_prediction'}
        return row, None

    def record(self):
        return {'version': self.version, 'resources': list(self.resources.values()),
                'financial_consents':list(self.consents.values()),
                'questions': list(self.questions.values()), 'history': self.history,
                'scoped_support': self.rules.public() if getattr(self,'rules',None) else {},
                'initial_state_modified_by_semantics': False}
