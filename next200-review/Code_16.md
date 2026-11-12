# 源码文本 · 16

## source/src/pr_next_joint/investigation/state_encoding.py

原文件 SHA-256 `51d42be24fc7cf77dca41812b2eb0062700c2ce3270c56a28328fc404375ba26`

````python
"""Encode a shared constructor state and only committed bounded prefix writes.

Numerical abstract leaves remain congruent functions. Constructor/prefix branch
obligations are inside their disjunction, never unconditional side effects.
"""
import copy
import itertools
import re
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key, walk, lit
from pr_next_joint.frontend.storage import keys, selectors, value_type
from pr_next_joint.verification.sequence import qualify, read
from pr_next_joint.verification.expressions import Unsupported
from .initial_state import CAPABILITY, DEPLOYMENT, domain, initial_for_lookup, family


def _initial_term(value, model, selected_domain):
    if isinstance(value, list): return [_initial_term(x, model, selected_domain) for x in value]
    if not isinstance(value, dict): return value
    kind = value.get('kind')
    if kind == 'actual_sender':
        return {'kind': 'parameter', 'id': -990000001, 'type': 'address', 'initial_identity': 'deployment_caller'}
    if kind == 'parameter':
        return {**value, 'initial_identity': 'constructor_parameter'} if value.get('constructor_parameter') or value.get('id') in model['constructor_parameters'] else value
    if kind in ('environment', 'transaction_value', 'transaction_origin'):
        return {**value, 'initial_identity': 'constructor_environment'}
    if kind == 'storage' and not value.get('instance'):
        row = model['declarations'].get(value['root'])
        if row is None: raise Unsupported('initial_storage_declaration_unresolved')
        segments = _initial_term(value.get('segments', []), model, selected_domain)
        prepared = {**value, 'segments': segments}
        typ = value_type(prepared, model['_lookup'])
        symbolic = selected_domain == CAPABILITY and not row['explicit_initializer'] and (
            not segments and bool(re.fullmatch(r'(?:address(?: payable)?|u?int\d*)', typ or '')) or
            family(value) in model['_amount_families'])
        if symbolic:
            return {**prepared, 'instance': 'initial_storage:' + selected_domain + ':' + model['identity']}
        if typ == 'bool': return lit(False)
        if re.fullmatch(r'(?:address(?: payable)?|u?int\d*|bytes\d+)', typ or '') or (typ or '').startswith(('contract ', 'enum ')):
            return lit(0)
        raise Unsupported('initial_default_type_not_encoded:' + str(typ))
    return {k: _initial_term(v, model, selected_domain) for k, v in value.items()}


def _runtime_candidates(facts, lookup, model, queried):
    """Only real writers of constrained queried roots and their guard prerequisites."""
    relevant = set()
    for cell in queried:
        row = model['declarations'].get(cell['root'], {})
        if row.get('explicit_initializer') or row.get('constructor_writes') or value_type(cell, lookup) == 'bool' or family(cell) not in model['_amount_families'] and keys(cell):
            relevant.add(cell['root'])
    paths = []
    # Include prerequisite role writers; never seed a default-false role table.
    for _ in range(facts.options.prefix_depth + 1):
        before = set(relevant)
        for oid, entry in facts.operations.items():
            if entry['target'] != model['target'] or entry.get('generated_getter'): continue
            for pid, p in facts.operation_paths(oid, True):
                if not any(w['path']['root'] in relevant for w in p['writes']): continue
                if not any(x[1] == pid for x in paths): paths.append((oid, pid, p))
                relevant.update(s['root'] for s in selectors(p['guards']))
        if relevant == before: break
    paths.sort(key=lambda x: (facts.operations[x[0]]['source']['start'], x[1]))
    return paths, relevant


def encode(e, details=None, selected_domain=None):
    selected_domain = selected_domain or domain(e.lookup)
    saved = initial_for_lookup(e.lookup)
    if saved is None: raise Unsupported('host_initial_state_model_missing')
    facts = e.lookup._investigation_facts
    # Non-serialized helpers never enter the domain identity.
    model = {**saved, '_lookup': e.lookup, '_amount_families': {family(r['cell']) for r in saved['candidate_amount_leaves']}}
    queried = [v for _, v in sorted(getattr(e, '_state_cells', {}).items()) if not v.get('instance')]
    prefix_limit=getattr(e,'_initial_prefix_limit',1)
    times=list(getattr(e,'_state_times',{}).values())
    token = digest([selected_domain, saved['identity'], queried,times,prefix_limit])
    cache = e.__dict__.setdefault('_initial_encoding_cache', {})
    if token in cache: return cache[token]
    z = e.z; branches = []; receipts = []; limits = []; before_encoding = getattr(e, '_encoding_initial', False)
    e._encoding_initial = True
    candidates, relevant = _runtime_candidates(facts, e.lookup, model, queried)
    sequences = [()]
    max_count = min(facts.options.max_prefixes,prefix_limit)
    for length in range(1, facts.options.prefix_depth + 1):
        for seq in itertools.product(range(len(candidates)), repeat=length):
            if len(sequences) >= max_count:
                limits.append({'reason': 'initial_prefix_frontier_bound', 'maximum': max_count}); break
            sequences.append(seq)
        if len(sequences) >= max_count: break
    incomplete = [r for rid in relevant for r in saved['runtime_writers']['paths'].get(rid, []) if not r['complete'] and r['flow'] != 'reverted']
    if incomplete: limits.append({'reason': 'initial_relevant_writer_path_incomplete', 'paths': sorted({r['path'] for r in incomplete})})
    def expr(v): return e.expr(_initial_term(v, model, selected_domain))
    try:
        for pi, cp in enumerate(saved['constructor_paths']):
            if cp['flow'] not in ('normal', 'returned'): continue
            if cp.get('issues') or cp.get('evaluation_gaps'):
                limits.append({'reason': 'constructor_effect_unresolved', 'constructor_path': pi,
                               'details': cp.get('issues', []) + cp.get('evaluation_gaps', [])}); continue
            for seq in sequences:
                start = len(e.constraints)
                writes = copy.deepcopy(cp['writes']); terms = []; prefix = []
                try:
                    terms.extend(expr(g) for g in cp['guards'])
                    for value in cp.get('evaluated_terms', []): expr(value)
                    for w in writes:
                        typ=value_type(w['path'],e.lookup)
                        if typ in ('string','bytes') and w['value'].get('kind') in ('parameter','literal','fixed_bytes_literal','storage'):continue
                        expr(w['value'])
                    deployer = expr({'kind': 'actual_sender'})
                    terms.append(deployer != 0)
                    for index, candidate in enumerate(seq):
                        oid, pid, path = candidates[candidate]; previous = copy.deepcopy(writes)
                        translate = lambda v: read(qualify(v, 20 + index), previous, e.lookup)
                        terms.extend(expr(translate(g)) for g in path['guards'])
                        for v in path.get('evaluated_terms', []): expr(translate(v))
                        caller = expr(qualify({'kind': 'actual_sender'}, 20 + index)); terms.append(caller != 0)
                        if any(n.get('kind') in ('unknown', 'external_return') for n in walk(path)):
                            raise Unsupported('initial_prefix_critical_external_effect')
                        for w in path['writes']:
                            dst = qualify(w['path'], 20 + index)
                            dst['segments'] = read(dst.get('segments', []), previous, e.lookup)
                            value = translate(w['value']); expr(value)
                            writes.append({**w, 'path': dst, 'value': value})
                        prefix.append({'operation': oid, 'path': pid, 'caller': qualify({'kind': 'actual_sender'}, 20 + index)})
                    # All runtime requests follow the constructor and committed
                    # prefixes. A future setter cannot enable a past request.
                    for field in ('timestamp','number'):
                        relevant_times=[v for v in times if v.get('field',v.get('sequence_role'))==field]
                        if not relevant_times:continue
                        base={'kind':'environment','field':field,'type':'uint256'}
                        previous=expr(base)
                        for index in range(len(seq)):
                            current=expr(qualify(base,20+index));terms.append(current>=previous);previous=current
                        terms.extend(e.expr(v)>=previous for v in relevant_times)
                    for cell in queried:
                        actual = e.expr(cell)
                        expected = expr(read(cell, writes, e.lookup))
                        terms.append(actual == expected)
                    evaluated = e.constraints[start:]; del e.constraints[start:]
                    condition = z.And(*terms, *evaluated)
                    selector = z.Bool('initial_branch_' + token[:16] + '_' + str(len(receipts)))
                    branches.append(z.And(selector, condition))
                    e.__dict__.setdefault('_initial_branch_conditions', {})[str(selector)] = z.And(selector, condition)
                    receipts.append({'selector': str(selector), 'constructor_path': pi, 'prefix': prefix,
                        'explicit_writes': [w['source'] for w in cp['writes']]})
                except (Unsupported, ValueError, KeyError, TypeError) as error:
                    del e.constraints[start:]
                    limits.append({'reason': str(error), 'constructor_path': pi, 'prefix_candidates': list(seq)})
        if not branches:
            # A proved reverting constructor differs from unsupported modeling.
            all_revert = bool(saved['constructor_paths']) and all(p['flow'] == 'reverted' and not p.get('issues') for p in saved['constructor_paths'])
            if not all_revert: raise Unsupported('initial_state_not_encoded:' + str(limits[:2]))
            branches = [z.BoolVal(False)]
        abstract = []
        for cell in queried:
            base = _initial_term(cell, model, selected_domain)
            if any(str(s.get('instance', '')).startswith('initial_storage:') for s in selectors(base)):
                abstract.append({'cell': cell, 'basis': 'uninitialized_typed_scalar_or_frozen_amount_leaf'})
        result = ([z.Or(*branches)], {'analysis_domain': selected_domain, 'initial_model_identity': saved['identity'],
            'analysis': selected_domain, 'shared_constructor_and_prefix': True, 'branches': receipts,
            'encoded_cells': queried, 'abstract_initial_assumptions': abstract, 'limits': limits,
            'prefix_depth_bound': facts.options.prefix_depth, 'prefixes_included': len(sequences),
            'more_prefixes_available':bool(candidates) and prefix_limit<facts.options.max_prefixes,
            'global_reachability_exhausted': not candidates and not limits,
            'explicit_constructor_prefix_executed': False, 'constructor_symbolic_transitions_encoded': True,
            'author_run_initial_state_verified': False})
        cache[token] = result
        return result
    finally:
        e._encoding_initial = before_encoding

````

## source/src/pr_next_joint/investigation/summary.py

原文件 SHA-256 `b80fa75856bb39f5c6ed65ace46b586c5d7c59b0d013b5cf7ef7e994644f0f91`

````python
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

    def rows(self, oid, committing=True):
        return [self.paths[p] for p in self.operations[oid]['paths']
                if not committing or self.paths[p]['committing']]

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
            'worklist_rounds': self.rounds, 'fixed_point':not any(r['residuals'] for r in self.paths.values()),
            'finite_extracted_worklist_completed':True,
            'scope': 'finite already compiler-resolved paths; residuals are not completed paths'}


def get_summaries(f):
    if not hasattr(f, 'summaries'): f.summaries = Summaries(f)
    return f.summaries


class Semantics:
    """Versioned H bindings. No Gold, source-name rules or mutable state domain."""
    def __init__(self, f):
        self.f = f; self.resources = {}; self.history = []; self.questions = {}
        self.version = 0;self.active_scope={'phase':None,'assumptions':[]}

    def scope(self,item):
        self.active_scope={'phase':copy.deepcopy(item.get('phase')),'assumptions':copy.deepcopy(item.get('assumptions',[]))}
        return self.active_scope

    def lookup(self, oid, cell):
        target=self.f.operations[oid]['target'];scope=self.active_scope
        scoped=self.resources.get(key([target,family(cell),scope]))
        return scoped or self.resources.get(key([target,family(cell)]))

    def dependency_identity(self,operations):
        operations=set(operations)
        families={key([self.f.operations[o]['target'],family(c)]) for o in operations for c in get_summaries(self.f).positions(o)}
        bound=[r['id'] for r in self.resources.values() if
               (key([r['target'],r['family']]) in families or operations.intersection(r['operations'])) and
               (not r.get('scope') or r['scope']==self.active_scope)]
        return digest(sorted(bound))

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
        previous = self.resources.get(k)
        if previous and all(previous.get(x) == row.get(x) for x in ('meaning', 'basis', 'operations')):
            return previous
        self.version += 1; row['version'] = self.version; row['id'] = 'sem_' + digest(row)[:20]
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

    def question(self, q, oid, cell=None, kind='resource'):
        obj = family(cell) if cell is not None else None
        sid = 'sq_' + digest([q['id'], oid, obj, kind,self.active_scope])[:16]
        # A resource question denotes a typed storage family. Keep its first
        # representative cell stable between registration, actual message and
        # answer consumption; encountering the recipient cell must not mutate
        # the same ID after the sender cell was already delivered.
        if sid in self.questions:return copy.deepcopy(self.questions[sid])
        row = {'id': sid, 'issue': q['id'], 'operation': oid, 'kind': kind,
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
        return row

    def consume_answer(self, answer, allowed, issues):
        sid = answer.get('question'); sq = self.questions.get(sid)
        if not sq or sid not in allowed:
            return None, 'semantic_answer_outside_sent_scope'
        text = str(answer.get('answer') or '').strip(); basis = str(answer.get('basis') or '').strip()
        if not text or not has_basis(basis): return None, 'semantic_answer_missing_explanation'
        q = issues.get(sq['issue'])
        if not q: return None, 'semantic_question_issue_missing'
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
                'questions': list(self.questions.values()), 'history': self.history,
                'initial_state_modified_by_semantics': False}

````

## source/src/pr_next_joint/reporting/__init__.py

原文件 SHA-256 `87e3e2f1dba261e0999d37d622e45825e4d2763d9091aa860663f27df53e5d17`

````python
"""Source analysis helpers retained by SCRV."""

````

## source/src/pr_next_joint/reporting/effective_parameters.py

原文件 SHA-256 `0124532d4bc73117bc5289fbef053be6407f7031e03a9246b61856ff9da3b0c3`

````python
"""Versioned finite limits; no sample-specific overrides."""
import json
from importlib.resources import files
from functools import lru_cache
@lru_cache(maxsize=1)
def current():
    data=json.loads(files('pr_next_joint').joinpath('resources/method_evidence.r1.json').read_text(encoding='utf8'))
    v=data['effective_parameters'];assert v['normalization_visits_per_operation_max'] in (100000,150000,200000)
    assert v['max_source_paths']==data['P']['max_source_paths']
    fixed={'expression_nodes_max':50000,'expression_depth_max':100,'expression_string_bytes_max':1048576,
        'expression_key_characters_max':262144,'source_evaluations_per_operation_max':2048,'call_depth_max':8,
        'solver_timeout_ms':3000,'variable_loop_frontier':2,'constant_loop_max':32}
    assert all(v[k]==x for k,x in fixed.items()),'UNVALIDATED_FINITE_PARAMETER_CHANGE'
    return {**v,'solver_timeout_upgrade_ms':10000,'solver_sample_seconds':120,'external_sequence_max':3,'dependency_closure_nodes_max':4096,'sequence_checks_per_sample_max':24,'sequence_paths_per_stage_max':8}

````

## source/src/pr_next_joint/resources/method_evidence.r1.json

原文件 SHA-256 `c906e1486ec2603ce7d43e7f41232df6d123036279e7b4aff481fe6663d6a34d`

````text
{
  "schema": "method-evidence-profile-r1",
  "approval": "PR_NEXT_METHOD_REQUIREMENTS_AMENDMENT_20261022_R1",
  "report_schema": "m03-p-report-v2",
  "rules": [
    {
      "id": "AC-01",
      "name_cn": "缺少或绕过授权保护",
      "P": "implemented_bounded",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "适用策略禁止该主体且成功产生受保护效果",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "implementation_scope": "bounded source permissions, program relationship candidates and selective SMT implication; preserves disjunctive authority, callback/caller context; arbitrary dynamic self-calls remain a gap; independently referenced native payout and selfdestruct native disposition; opaque delegatecall effect retained unknown",
      "qualification_scope": "compiler/model engineering contrasts only; new real-pilot performance pending",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof"
    },
    {
      "id": "AC-02",
      "name_cn": "权限状态与管理流程被不当控制",
      "P": "implemented_bounded",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "不具管理资格的受控主体非法修改权限并取得控制",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "implementation_scope": "source-bound role management, scoped grants, bulk-key qualification, nomination and actual successor binding; proxy upgrades and opaque policy modules remain gaps",
      "qualification_scope": "compiler/model engineering contrasts only; new real-pilot performance pending",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof"
    },
    {
      "id": "AC-03",
      "name_cn": "身份资源作用对象错配",
      "P": "implemented_bounded",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "被检查凭据与实际作用对象不匹配且无合法委托",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "implementation_scope": "source resource/subject/delegation/alias and conditionally source-typed read-call relations; unknown proxies and business action-bit interpretation remain gaps",
      "qualification_scope": "compiler/model engineering contrasts only; new real-pilot performance pending",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof"
    },
    {
      "id": "AC-04",
      "name_cn": "条件和生命周期过宽",
      "P": "implemented_bounded",
      "implementation_scope": "same-record boolean validity; issued future expiry and ordered timestamps; epoch snapshots; controlled per-subject additive usage quotas; same-manager enumeration phase exit with persistent issued credential. Arbitrary reopening protocols, nonlinear consumption and cross-contract lifecycles remain gaps",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "撤销/过期/未生效凭据仍被接受并产生效果",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "qualification_scope": "compiler/model engineering contrasts only; new real-pilot performance pending",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof"
    },
    {
      "id": "AC-05",
      "name_cn": "签名凭据使用错误",
      "P": "implemented_bounded",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "合法来源凭据被错误重放或跨域/主体/资源使用，或明确坏签名被接受",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "qualification_scope": "compiler/model engineering contrasts only; new real-pilot performance pending",
      "implementation_scope": "source-bound credential replay/domain/subject/resource/validity models; ordinary random hash excluded; opaque validators retain decisive gaps",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof"
    },
    {
      "id": "FCR-TRANSFER",
      "name_cn": "任意转移",
      "P": "implemented_bounded",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "源码中的特权他人资产/账本权益处分机制，核查持有人同意",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "definition_revision": "fcr-mechanism-r1-20261027",
      "feasibility_reporting": "separate; source mechanism does not prove actual funded exploitability",
      "qualification_scope": "compiler/model engineering contrasts only; new real-pilot performance pending",
      "implementation_scope": "bounded asset/transferable-ledger model, explicit amount consumption, independent privilege and source holder consent; arbitrary compensation and opaque cross-contract assets remain unknown",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof"
    },
    {
      "id": "FCR-MINT",
      "name_cn": "任意增发",
      "P": "implemented_bounded",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "源码中的特权资产或可转移账本权益创建机制",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "implementation_scope": "source-bound native redeemable additive ledgers and exact floor proportional native shares; direct privilege and consumed issuance allowance; bounded administrator-set backing multiplier and same-holder scaled reward-index checkpoint; distinguish equal-value native deposits, correctly priced share deposits and same-holder equal-unit conversion. Record-based notes, cross-contract asset ledgers, arbitrary nonlinear arithmetic and solvency remain gaps; scalar getter-linked migration and holder/face/liability-bound redeemable records; complex cross-contract ledgers and proof-controlled issuance remain gaps",
      "definition_revision": "fcr-mechanism-r1-20261027",
      "feasibility_reporting": "separate; source mechanism does not prove actual funded exploitability",
      "qualification_scope": "compiler/model engineering contrasts only; new real-pilot performance pending",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof"
    },
    {
      "id": "FCR-DESTROY",
      "name_cn": "任意销毁",
      "P": "implemented_bounded",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "特权消减或销毁他人资产权益或可定位主体与数量的抽象账户账本；排除有效同意与已匹配守恒转换",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "definition_revision": "v20-approved-abstract-account-ledger",
      "feasibility_reporting": "separate; source mechanism does not prove actual funded exploitability",
      "qualification_scope": "financial and abstract account mechanisms distinguished; conditional positive prestate not deployment proof",
      "implementation_scope": "bounded asset/transferable-ledger model, explicit amount consumption, independent privilege and source holder consent; arbitrary compensation and opaque cross-contract assets remain unknown",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof",
      "rollback_profile": "strict_financial changes this branch only"
    },
    {
      "id": "FCR-PAUSE",
      "name_cn": "暂停转移",
      "P": "implemented_bounded",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "源码中的特权普通转移阻断机制，声明入口与例外",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "definition_revision": "fcr-mechanism-r1-20261027",
      "feasibility_reporting": "separate; source mechanism does not prove actual funded exploitability",
      "qualification_scope": "compiler/model engineering contrasts only; new real-pilot performance pending",
      "implementation_scope": "same ordinary holder request under privileged control transition, with entry/holder/exception scope; pure issuance/burn excluded from transfer pairing; admin-only service not main FREEZE",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof"
    },
    {
      "id": "FCR-FREEZE",
      "name_cn": "冻结账户",
      "P": "implemented_bounded",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "源码中的特权指定持有人转出阻断机制，声明对象与例外",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "definition_revision": "fcr-mechanism-r1-20261027",
      "feasibility_reporting": "separate; source mechanism does not prove actual funded exploitability",
      "qualification_scope": "compiler/model engineering contrasts only; new real-pilot performance pending",
      "implementation_scope": "same ordinary holder request under privileged control transition, with entry/holder/exception scope; pure issuance/burn excluded from transfer pairing; admin-only service not main FREEZE",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof"
    }
  ],
  "P": {
    "max_source_paths": 48,
    "required": [
      "program_id",
      "build_id",
      "rule",
      "function",
      "required_policy_candidate",
      "effect",
      "conditions",
      "status",
      "route"
    ],
    "forbidden_claims": [
      "actual_execution",
      "whole_program_safety",
      "business_intention_proven"
    ],
    "no_execution_required": true,
    "analyzer": "compiler-source-declaration-and-path-relations",
    "source_loop_scope": "for-loop source expansion 0..2 complete iterations; longer continuation explicit named gap; not whole-loop proof"
  },
  "conditional_fields": {
    "P": [
      "source_identity",
      "analyzer",
      "policy_basis",
      "scope"
    ],
    "M": [
      "model_identity",
      "bounds",
      "approximations"
    ],
    "E": [
      "runtime_identity",
      "execution_plan",
      "backend_identity",
      "actual_execution",
      "replay_when_required"
    ]
  },
  "acceptance": {
    "three_structures": [
      "global_address",
      "per_object_owner",
      "role_membership"
    ],
    "real_analysis_and_synthetic_separated": true,
    "no_name_only_matching": true,
    "no_raw_sat_or_llm_self_certification": true,
    "local_effect_sufficient": true,
    "unknown_not_safe": true,
    "cases_200_all_actual_analysis_not_all_dynamic": true,
    "fixed_normal_risk_ratio_or_zero_errors": false
  },
  "version_boundary": "Task B/C2 originals and prior reports unchanged; only new analysis uses this profile",
  "implementation_revision": "joint-operation-scoped-r1-rq1-v7-20261028",
  "project_input": {
    "mode": "P --targets project",
    "targets": "all concrete compiled contracts; each analyzed in separate storage context",
    "entry_optional_in_project_mode": true,
    "unresolved_external_wiring": "retained, not inferred",
    "compiler_scope": "0.8.20 development input; arbitrary build systems/versions not added"
  },
  "m04_relations_r2": {
    "shared_consumer": true,
    "source_labels_or_case_ids_used": false,
    "hash_terms": "ordered typed encoding, no inversion; dynamic packed encoding unsupported",
    "casts": "unsigned narrowing preserved, erased only when source bound establishes identity",
    "unresolved_controls": "named inconclusive, not public-entry safety",
    "dynamic_execution": "not_required_for_P_and_not_claimed"
  },
  "m04_assets_lifecycle_r3": {
    "proportional_model": "exact structural floor expression, no reassociation or rational cancellation",
    "controlled_arithmetic": "bounded multiplier or same-holder scaled index delta; positive rounded reward explicitly conditional",
    "phase_and_expiry": "program-inferred policy; original definitions unchanged",
    "evidence_route": "P, no new compiler/native/API/EVM"
  },
  "local_tools": {
    "relationship_graph": "networkx 3.4.2",
    "permission_predicates": "z3-solver 4.15.3.0",
    "route": "P",
    "scope": "source predicate checks under declared pre-state; no EVM execution or whole-program reachability"
  },
  "definition_revisions": {
    "FCR": "fcr-mechanism-r1-20261027",
    "AC": "ac-five-directions-r1-20261028"
  },
  "v7_scope": {
    "AC04D_removed": true,
    "active_ac_rules": [
      "AC-01",
      "AC-02",
      "AC-03",
      "AC-04",
      "AC-05"
    ],
    "constant_loop_max": 32,
    "variable_loop_frontier": 2,
    "all_unmodeled_semantics": "decisive local unknown, never safety",
    "real_pilot_status": "not_started",
    "source_evaluations_per_operation_max": 2048,
    "expression_nodes_max": 50000,
    "expression_depth_max": 100,
    "expression_string_bytes_max": 1048576,
    "expression_key_characters_max": 262144
  },
  "effective_parameters": {
    "normalization_visits_per_operation_max": 150000,
    "max_source_paths": 48,
    "expression_nodes_max": 50000,
    "expression_depth_max": 100,
    "expression_string_bytes_max": 1048576,
    "expression_key_characters_max": 262144,
    "source_evaluations_per_operation_max": 2048,
    "call_depth_max": 8,
    "solver_timeout_ms": 3000,
    "variable_loop_frontier": 2,
    "constant_loop_max": 32,
    "fcr_execution_environment": "janus_comparison_pre_eip_6780",
    "arithmetic_query_scope": "explicit nonwrapping uint256 subcases; typed narrow/signed arithmetic encoded separately"
  },
  "current_approved_revision": "joint-concentrated-redesign-rq1-v20-20261031",
  "v20_authorization": "user approved V20_CONCENTRATED_REDESIGN_PLAN_R1_CN and subsequent execution",
  "v20_limits": {
    "maximum_external_operations": 3,
    "sequence_checks_per_sample": 24,
    "composition_paths_per_stage": 8,
    "solver_initial_ms": 3000,
    "solver_one_upgrade_ms": 10000,
    "solver_total_seconds": 120,
    "source_dependency_closure_nodes": 4096
  },
  "v20_scope_notes": {
    "other_FCR_definitions_unchanged": true,
    "LLM_final_classification": false,
    "LLM_formulas": false,
    "default_semantic_followup": 0,
    "additional_training": false
  }
}

````

## source/src/pr_next_joint/runtime/__init__.py

原文件 SHA-256 `87e3e2f1dba261e0999d37d622e45825e4d2763d9091aa860663f27df53e5d17`

````python
"""Source analysis helpers retained by SCRV."""

````

## source/src/pr_next_joint/runtime/immutable.py

原文件 SHA-256 `7170290a5ac58d0ab7a95e229813744025997c44c372130b511f2b58810fa2dd`

````python
"""Enrich an old compiler artifact only from identical creation code, runtime and complete metadata."""
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

from pr_next_joint.frontend.facts import walk


def restore(bundle, standard, original):
    if not any(n.get("mutability")=="immutable" for a in bundle.get("ast_sources",{}).values() for n in walk(a)):
        return None
    rows=[c for c in bundle["contracts"] if c.get("runtime") and not c.get("immutable_references")]
    if not rows:
        return None
    trusted=os.environ.get("PRNEXT_IMMUTABLE_SOLC_DIR")
    record={"state":"not_reconstructed","invocations":0,"targets":[]}
    if not trusted:
        return {**record,"reason":"local_trusted_compiler_directory_not_configured"}
    version=(rows[0].get("metadata") or {}).get("compiler",{}).get("version","")
    if not re.fullmatch(r"\d+\.\d+\.\d+\+commit\.[0-9A-Fa-f]{8}",version):
        return {**record,"reason":"full_compiler_version_not_available"}
    root=Path(trusted).resolve()
    names=("solc-windows-amd64-v"+version+".exe","solc-linux-amd64-v"+version,"solc-"+version.split("+")[0])
    compiler=next((root/n for n in names if (root/n).is_file() and (root/n).resolve().parent==root),None)
    if not compiler:
        return {**record,"reason":"matching_compiler_not_installed"}
    source=copy.deepcopy(standard)
    selection=source["settings"].setdefault("outputSelection",{}).setdefault("*",{}).setdefault("*",[])
    for key in ("evm.bytecode.object","evm.deployedBytecode.object","metadata","evm.deployedBytecode.immutableReferences"):
        if key not in selection:selection.append(key)
    record["invocations"]=1
    try:
        run=subprocess.run([str(compiler),"--standard-json"],input=json.dumps(source).encode(),capture_output=True,timeout=60,check=True)
        generated=json.loads(run.stdout)["contracts"]
        certificate=hashlib.sha256(compiler.read_bytes()).hexdigest()
        for c in rows:
            old=original["contracts"][c["file"]][c["name"]]
            new=generated[c["file"]][c["name"]]
            if new["metadata"]!=old["metadata"] or any(new["evm"][k]["object"]!=old["evm"][k]["object"] for k in ("bytecode","deployedBytecode")):
                continue
            ranges=new["evm"]["deployedBytecode"].get("immutableReferences",{})
            if ranges and all(isinstance(p.get("start"),int) and isinstance(p.get("length"),int)
                         and 0 <= p["start"] < p["start"]+p["length"] <= len(c["runtime"])//2 for v in ranges.values() for p in v):
                c["immutable_references"]=ranges
                record["targets"].append({"target":c["file"]+":"+c["name"],"locations":ranges})
        return {**record,"state":"certified" if record["targets"] else "no_matching_ranges",
                "compiler":version,"compiler_binary_sha256":certificate}
    except (OSError,subprocess.SubprocessError,ValueError,KeyError) as error:
        return {**record,"reason":"local_reconstruction_unavailable","exception":type(error).__name__}

````

## source/src/pr_next_joint/verification/__init__.py

原文件 SHA-256 `87e3e2f1dba261e0999d37d622e45825e4d2763d9091aa860663f27df53e5d17`

````python
"""Source analysis helpers retained by SCRV."""

````

## source/src/pr_next_joint/verification/expressions.py

原文件 SHA-256 `57fe986e34c11643995e8551c99920d037a01783f52136e5c41ea0edf53f0a0f`

````python
from pr_next_joint.verification.solver import solve as bounded_solve
"""Z3 checks for source-bound permission predicates, not execution proofs.

Unsigned values use mathematical integers with explicit width constraints;
bitwise operations use unsigned BV conversions. No unknown term is replaced by
an unconstrained atom. Storage is represented by functions of actual keys so
congruence is preserved. SAT is conditional on the stated pre-state, not proof
of deployment reachability or business intent.
"""
import hashlib
from pr_next_joint.frontend.path_ir import key, normalize

class Unsupported(ValueError): pass

class Encoder:
    def __init__(self, lookup):
        import z3
        self.z=z3;self.lookup=lookup;self.constraints=[];self.symbols={};self.functions={};self.domain_constraints=[]

    def name(self,v):return hashlib.sha256(key(v).encode()).hexdigest()[:24]

    def typ(self,v):
        if v.get('kind')=='index' and v.get('base',{}).get('kind')=='parameter':
            typ=v['base'].get('type','')
            if '[' not in typ:raise Unsupported('index_base_not_array')
            element=typ.split('[')[0]
            if typ.count('[')!=1:raise Unsupported('nested_parameter_array_not_lowered')
            return element
        if v.get('kind')=='storage':
            from pr_next_joint.frontend.storage import value_type
            typ=value_type(v,self.lookup)
            if not typ:raise Unsupported('storage_type_not_resolved')
            return typ
        if v.get('kind') in ('actual_sender','contract_address','transaction_origin'):return 'address'
        from pr_next_joint.frontend.language import scalar_type
        return scalar_type(v.get('type','uint256'),self.lookup)

    def width(self,typ):
        import re
        if typ in ('address','address payable') or typ.startswith('contract '):return 160
        if typ.startswith('enum '):return 8
        m=re.fullmatch(r'u?int(\d*)',typ)
        if m:return int(m[1] or 256)
        m=re.fullmatch(r'bytes(\d+)',typ)
        if m:return 8*int(m[1])
        raise Unsupported('unsupported_scalar_type:'+typ)

    def bound(self,x,typ):
        if typ!='bool':
            import re
            signed=bool(re.fullmatch(r'int\d*',typ));bits=self.width(typ)
            domain=[x>=(-2**(bits-1) if signed else 0),x<2**(bits-int(signed))]
            self.constraints.extend(domain);self.domain_constraints.extend(domain)
        return x

    def atom(self,v,typ=None):
        z=self.z;typ=typ or self.typ(v);n=self.name(v)
        if n not in self.symbols:
            self.symbols[n]=z.Bool('b_'+n) if typ=='bool' else self.bound(z.Int('n_'+n),typ)
        elif typ!='bool':self.bound(self.symbols[n],typ)
        return self.symbols[n]

    def expr(self,v):
        z=self.z;v=normalize(v);kind=v.get('kind')
        if not getattr(self,'_encoding_initial',False) and ((kind=='environment' and v.get('field') in ('timestamp','number')) or (kind=='parameter' and v.get('sequence_role') in ('timestamp','number'))):
            self.__dict__.setdefault('_state_times',{})[key(v)]=v
        # All permission routes consume the same source-produced scalar IR.
        # Reuse exact casts/branch constraints; no new policy or symbolic unknown.
        if kind=='op' and v.get('op')=='ite':
            condition,yes,no=v['args']
            return self.expr({'kind':'conditional','condition':condition,'when_true':yes,'when_false':no})
        if kind in ('typed_integer_arithmetic','integer_cast'):
            from pr_next_joint.verification.typed_integer import encode
            return encode(self,v)
        if kind in ('conditional','guarded_evaluation'):
            condition=self.expr(v['condition'])
            if not z.is_bool(condition):raise Unsupported('conditional_guard_not_boolean')
            def branch(value,guard):
                start=len(self.constraints)
                result=self.expr(value)
                constraints=self.constraints[start:];del self.constraints[start:]
                self.constraints.extend(z.Implies(guard,c) for c in constraints)
                return result
            if kind=='guarded_evaluation':
                for value in v['values']:branch(value,condition)
                return z.BoolVal(True)
            positive=branch(v['when_true'],condition)
            negative=branch(v['when_false'],z.Not(condition))
            if positive.sort()!=negative.sort():raise Unsupported('conditional_branch_sort_mismatch')
            return z.If(condition,positive,negative)
        if kind=='literal':
            if type(v['value']) is bool:return z.BoolVal(v['value'])
            if type(v['value']) is int:return z.IntVal(v['value'])
            raise Unsupported('literal_type')
        if kind=='array_length':
            import re
            base=v.get('array',{})
            if base.get('kind')!='parameter':raise Unsupported('array_length_source_not_parameter')
            typ=base.get('type','')
            if typ.count('[')!=1:raise Unsupported('array_length_dimension_not_lowered')
            fixed=re.match(r'^[^\[]+\[(\d+)\]',typ)
            return z.IntVal(int(fixed.group(1))) if fixed else self.atom(v,'uint256')
        if kind in ('actual_sender','transaction_origin','contract_address','environment','transaction_value'):
            return self.atom(v)
        if kind=='parameter':
            if '[' in v.get('type',''):raise Unsupported('array_used_as_scalar')
            return self.atom(v)
        if kind=='storage':
            if not getattr(self,'_encoding_initial',False):
                self.__dict__.setdefault('_state_cells',{})[key(v)]=v
            args=[];shape=[]
            declaration=self.lookup.nodes.get(v['root'],{}).get('typeName',{})
            for seg in v.get('segments',[]):
                if 'key' in seg:
                    index=seg['key']
                    if index.get('kind')=='fixed_bytes_literal':
                        from pr_next_joint.graph.object_equivalence import literal_key
                        arg=z.IntVal(literal_key(index,declaration))
                    else:
                        arg=self.expr(index)
                    args.append(arg);shape.append({'key_sort':str(arg.sort())})
                    declaration=declaration.get('valueType',declaration.get('baseType',{}))
                elif 'field' in seg:
                    shape.append({'field':seg['field']})
                    declaration=self.lookup.nodes.get(seg['field'],{}).get('typeName',{})
                elif seg.get('length'):shape.append({'array_length':True})
                else:raise Unsupported('storage_segment')
            if not args:return self.atom(v)
            typ=self.typ(v);ident={'root':v['root'],'instance':v.get('instance'),'shape':shape,'type':typ};n=self.name(ident)
            if n not in self.functions:self.functions[n]=z.Function('s_'+n,*[a.sort() for a in args],z.BoolSort() if typ=='bool' else z.IntSort())
            return self.bound(self.functions[n](*args),typ)
        if kind=='index' and v['base'].get('kind')=='parameter':
            import re
            base=v['base'];typ=self.typ(v);arg=self.expr(v['key']);n=self.name(base)
            if n not in self.functions:self.functions[n]=z.Function('a_'+n,z.IntSort(),z.BoolSort() if typ=='bool' else z.IntSort())
            length=self.expr({'kind':'array_length','array':base,'type':'uint256'})
            self.constraints.extend([arg>=0,arg<length]);return self.bound(self.functions[n](arg),typ)
        if kind=='uint_narrow':return self.expr(v['input']) % 2**v['bits']
        if kind!='op':raise Unsupported('term_not_encoded:'+str(kind))
        if v['op'] in ('and','&&','or','||'):
            conjunction=v['op'] in ('and','&&');prefix=z.BoolVal(True);values=[]
            for term in v['args']:
                start=len(self.constraints);value=self.expr(term)
                if not z.is_bool(value):raise Unsupported('logical_operand_not_boolean')
                branch_constraints=self.constraints[start:];del self.constraints[start:]
                self.constraints.extend(z.Implies(prefix,c) for c in branch_constraints)
                values.append(value);prefix=z.And(prefix,value if conjunction else z.Not(value))
            return z.And(*values) if conjunction else z.Or(*values)
        if v['op']=='**':
            base,exponent=v['args']
            if exponent.get('kind')!='literal':
                # Exact finite no-overflow subdomain for a source constant base.
                # Preserve the exponent as a state/input value; never invent decimals.
                if base.get('kind')!='literal' or type(base.get('value')) is not int or base['value']<2:raise Unsupported('exponent_base_not_source_constant')
                values=[1]
                while len(values)<=256 and values[-1]*base['value']<2**256:values.append(values[-1]*base['value'])
                power=self.expr(exponent)
                if not z.is_int(power):raise Unsupported('exponent_not_integer')
                self.constraints.extend([power>=0,power<len(values)])
                result=z.IntVal(values[-1])
                for i in range(len(values)-2,-1,-1):result=z.If(power==i,z.IntVal(values[i]),result)
                return result
            if type(exponent.get('value')) is not int or not 0<=exponent['value']<=256:
                raise Unsupported('exponent_not_bounded_source_constant')
            if base.get('kind')!='literal' and self.typ(base) not in ('uint','uint256'):
                raise Unsupported('exponent_base_width_not_lowered')
            value=self.expr(base);result=z.IntVal(1)
            for _ in range(exponent['value']):result=result*value
            self.constraints.extend([result>=0,result<2**256])
            return result
        op=v['op'];a=[self.expr(x) for x in v['args']]
        if op in ('and','&&'):return z.And(*a)
        if op in ('or','||'):return z.Or(*a)
        if op=='!':
            if len(a)!=1 or not z.is_bool(a[0]):raise Unsupported('negation_operand_not_boolean')
            return z.Not(a[0])
        if op=='==':return a[0]==a[1]
        if op=='!=':return a[0]!=a[1]
        if op=='<':return a[0]<a[1]
        if op=='<=':return a[0]<=a[1]
        if op=='>':return a[0]>a[1]
        if op=='>=':return a[0]>=a[1]
        if op in ('&','|','^'):
            left,right=[z.Int2BV(x,256) for x in a]
            return z.BV2Int({'&':lambda:left&right,'|':lambda:left|right,'^':lambda:left^right}[op](),is_signed=False)
        if op in ('+','-','*','/','%'):
            from pr_next_joint.frontend.path_ir import walk
            for term in v['args']:
                if term.get('kind') in ('parameter','storage') and self.typ(term) not in ('uint','uint256'):
                    raise Unsupported('arithmetic_width_not_lowered:'+self.typ(term))
            if op in ('/','%'):self.constraints.append(a[1]>0)
            value={'+':lambda:a[0]+a[1],'-':lambda:a[0]-a[1],'*':lambda:a[0]*a[1],'/':lambda:a[0]/a[1],'%':lambda:a[0]%a[1]}[op]()
            self.constraints.extend([value>=0,value<2**256]);return value
        raise Unsupported('operator_not_encoded:'+op)

def check(lookup,guards,required,timeout_ms=1500):
    try:
        e=Encoder(lookup);z=e.z
        g=z.And(*[e.expr(x) for x in guards]);q=e.expr(required)
        solver=z.Solver();solver.set(timeout=timeout_ms);solver.add(*e.constraints);solver.add(g)
        premise=bounded_solve(solver)
        base={'engine':'z3','version':z.get_version_string(),'premise':str(premise),'query':'not_checked',
              'scope':'declared source path and pre-state, not transaction reachability','timeout_ms':timeout_ms}
        if premise!=z.sat:return {**base,'status':'inconclusive','reason':'premise_unsat' if premise==z.unsat else solver.reason_unknown()}
        solver.add(z.Not(q));answer=bounded_solve(solver);base['query']=str(answer)
        if answer==z.unknown:return {**base,'status':'inconclusive','reason':solver.reason_unknown()}
        return {**base,'status':'supported' if answer==z.sat else 'refuted_in_scope',
                'formula_sha256':hashlib.sha256(solver.sexpr().encode()).hexdigest(),
                'encoding':'unsigned bounded Int, unsigned BV bitwise, keyed storage functions'}
    except (ImportError,Unsupported) as error:
        return {'status':'inconclusive','engine':'z3','reason':str(error),'query':'not_encoded'}

````

## source/src/pr_next_joint/verification/hash_confirmation.py

原文件 SHA-256 `3f4878642365fa4ae7fbba8fb905cce0af877b564704e676ee8855e6d3d8ac6d`

````python
"""Concrete confirmation of a candidate fixed-ABI Keccak witness.

No injectivity/preimage assumption is used. A failed candidate remains open;
it is never an UNSAT certificate for the original symbolic property.
"""
import re
from .expressions import Unsupported


def encoded(types, values, mode):
    result=[]
    packed=mode in ('encodePacked','raw_fixed_bytes')
    for typ,value in zip(types,values):
        if typ.startswith('fixed_bytes_literal:'):
            size=int(typ.split(':')[1]); raw=int(value).to_bytes(size,'big')
        elif typ=='bool':
            raw=bytes([int(bool(value))])
            if not packed:raw=raw.rjust(32,b'\0')
        elif typ=='address' or typ.startswith('contract '):
            raw=int(value).to_bytes(20,'big')
            if not packed:raw=raw.rjust(32,b'\0')
        elif re.fullmatch(r'bytes\d+',typ):
            raw=int(value).to_bytes(int(typ[5:]),'big')
            if not packed:raw=raw.ljust(32,b'\0')
        elif re.fullmatch(r'u?int\d*',typ):
            signed=typ.startswith('int');bits=int((typ[3:] if signed else typ[4:]) or 256)
            size=bits//8 if packed else 32
            raw=int(value).to_bytes(size,'big',signed=signed)
        else:raise Unsupported('concrete_hash_type:'+typ)
        result.append(raw)
    return b''.join(result)


def confirm(encoder, solver, timeout):
    z=encoder.z; rows=getattr(encoder,'hash_terms',{})
    if not rows:return {'status':'not_required'},solver
    formula=z.And(*solver.assertions())
    def walk(n):
        # Z3 expressions are DAGs. Expanding them as trees (and serializing
        # every descendant) made repeated recovery/hash subterms grow into
        # minutes of Python work outside the solver timeout.
        pending=[n];seen=set()
        while pending:
            node=pending.pop();ident=node.get_id()
            if ident in seen:continue
            seen.add(ident);yield node
            if z.is_quantifier(node):pending.append(node.body())
            elif z.is_app(node):pending.extend(node.children())
    nodes=list(walk(formula));active={n.get_id() for n in nodes}
    rows={k:r for k,r in rows.items() if r['application'].get_id() in active}
    if not rows:return {'status':'not_required','only_inactive_hash_terms':True},solver
    if any(z.is_quantifier(n) for n in nodes):
        return {'status':'unverified','reason':'quantified_hash_requires_separate_proof'},None
    model=solver.model(); substitutions=[];pins=[];evidence=[];pending=dict(rows)
    from Crypto.Hash import keccak
    try:
        while pending:
            progress=False
            for k,row in list(pending.items()):
                unresolved_ids={r['application'].get_id()for r in pending.values()}
                if any(n.get_id() in unresolved_ids for arg in row['arguments'] for n in walk(arg)):continue
                args=[z.substitute(a,*substitutions) if substitutions else a for a in row['arguments']]
                vals=[model.eval(a,model_completion=True) for a in args]
                if not all(z.is_int_value(v) or z.is_true(v) or z.is_false(v) for v in vals):
                    raise Unsupported('hash_argument_not_concrete')
                values=[v.as_long() if z.is_int_value(v) else z.is_true(v) for v in vals]
                raw=encoded(row['types'],values,row['mode']); digest=keccak.new(digest_bits=256,data=raw).digest()
                value=int.from_bytes(digest,'big');app=row['application']
                substitutions.append((app,z.IntVal(value)))
                pins.extend(a==v for a,v in zip(row['arguments'],vals));pins.append(app==value)
                evidence.append({'mode':row['mode'],'types':row['types'],'arguments':values,
                    'encoded_hex':raw.hex(),'keccak256':digest.hex()})
                del pending[k];progress=True
            if not progress:raise Unsupported('hash_dependency_cycle')
        from .solver import solve
        concrete=z.Solver();concrete.add(*solver.assertions(),*pins)
        answer=solve(concrete,initial_ms=timeout)
        record={'status':'verified' if answer==z.sat else 'unverified','completion_answer':str(answer),
            'calls':evidence,'witness_formula':concrete.sexpr(),
            'method':'candidate_inputs_pinned_and_actual_keccak_recomputed',
            'failed_completion_is_not_property_refutation':True}
        return record,concrete if answer==z.sat else None
    except (Unsupported,ValueError,OverflowError,ImportError) as error:
        return {'status':'unverified','reason':str(error),'calls':evidence},None

````

## source/src/pr_next_joint/verification/joint_encoding.py

原文件 SHA-256 `79ce9d8c227056be9754765ccdc17b03ae58fa391f3d4681f321eef168dbd8df`

````python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""
from pr_next_joint.verification.expressions import Encoder, Unsupported
from pr_next_joint.frontend.path_ir import key, op, lit, walk

class JointEncoder(Encoder):
    def __init__(self,lookup):
        super().__init__(lookup);self.encoding_notes=[];self.abstract_hash_used=False
    def expr(self,v):
        if v.get('kind')=='source_linear_quantity':
            terms=v.get('terms',[])
            if not all(type(t.get('coefficient')) is int for t in terms):raise Unsupported('source_delta_coefficient')
            # Signed mathematical difference, not Solidity executed arithmetic.
            # Source execution constraints are still checked separately.
            return self.z.Sum(*[t['coefficient']*self.expr(t['value']) for t in terms]) if terms else self.z.IntVal(0)
        from pr_next_joint.frontend.bytes import encode
        byte_value=encode(self,v)
        if byte_value is not None:return byte_value
        if v.get('kind')=='op' and v.get('op')=='ite':
            condition,yes,no=v['args']
            return super().expr({'kind':'conditional','condition':condition,'when_true':yes,'when_false':no})
        if v.get('kind') in ('typed_integer_arithmetic','integer_cast'):
            from pr_next_joint.verification.typed_integer import encode
            return encode(self,v)
        if v.get('kind')=='guarded_evaluation':
            condition=self.expr(v['condition'])
            if not self.z.is_bool(condition):raise Unsupported('guarded_evaluation_condition_not_boolean')
            values=v.get('values')
            if values is None and 'input' in v:values=[v['input']]
            if not isinstance(values,list):raise Unsupported('guarded_evaluation_values_not_list')
            mark=len(self.constraints)
            for value in values:self.expr(value)
            extra=self.constraints[mark:];del self.constraints[mark:]
            self.constraints.append(self.z.Implies(condition,self.z.And(*extra)))
            return self.z.BoolVal(True)
        if v.get('kind')=='op' and v.get('op') in ('and','&&','or','||'):
            conjunction=v['op'] in ('and','&&');parts=[]
            for arg in v['args']:
                gate=self.z.And(*parts) if conjunction else self.z.Not(self.z.Or(*parts))
                mark=len(self.constraints);value=self.expr(arg);extra=self.constraints[mark:];del self.constraints[mark:]
                if not self.z.is_bool(value):raise Unsupported('logical_operand_not_boolean')
                self.constraints.append(self.z.Implies(gate,self.z.And(*extra)));parts.append(value)
            return self.z.And(*parts) if conjunction else self.z.Or(*parts)
        if v.get('kind')=='checked_evaluation':
            if v.get('type')!='uint256':raise Unsupported('checked_evaluation_type_not_supported')
            result=self.expr(v['input']);self.constraints.extend([result>=0,result<2**256]);return result
        if v.get('kind')=='op' and v.get('op')=='&':
            a,b=v['args']
            if a.get('kind')=='literal':a,b=b,a
            if b.get('kind')=='literal' and type(b.get('value')) is int and 0<=b['value']<2**256:
                bits=[i for i in range(256) if b['value'] & (1<<i)]
                if len(bits)<=16:
                    # Exact unsigned bit extraction. Avoid expensive Int/BV
                    # conversion for a small constant permission mask.
                    x=self.expr(a)
                    return self.z.Sum(*[((x/(1<<i))%2)*(1<<i) for i in bits]) if bits else self.z.IntVal(0)
        from pr_next_joint.verification.joint_intrinsics import intrinsic
        special=intrinsic(self,v)
        if special is not None:return special
        if v.get('kind')=='member' and v.get('member')=='value' and v.get('base',{}).get('kind')=='symbol':
            declaration=v['base'].get('declaration')
            from pr_next_joint.frontend.source_entry_identity import builtin_object
            sourced=any(n.get('nodeType')=='MemberAccess' and n.get('memberName')=='value'
                and n.get('expression',{}).get('nodeType')=='Identifier'
                and n['expression'].get('name')=='msg' and n['expression'].get('referencedDeclaration')==declaration
                and builtin_object(n['expression'],self.lookup,'msg')
                for n in self.lookup.nodes.values())
            if not sourced:raise Unsupported('member_value_not_verified_builtin')
            return self.expr({'kind':'transaction_value','type':'uint256'})
        if v.get('kind')=='source_calldata_length':
            self.encoding_notes.append('source-bound calldata byte length; no ABI minimum or transaction reachability assumed')
            return self.atom(v,'uint256')
        if v.get('kind') in ('transition_caller','transaction_value','native_reserve'):
            return self.atom(v,'address' if v['kind']=='transition_caller' else 'uint256')
        if v.get('kind')=='native_call_success':return self.atom(v,'bool')
        if v.get('kind')=='source_gas_available':
            self.encoding_notes.append('available gas symbolic; no gas sufficiency or transaction execution proof')
            return self.atom(v,'uint256')
        if v.get('kind')=='op' and v.get('op') in ('+','-','*','/','%'):
            # Only arithmetic OPERANDS determine the width; an address used as
            # a mapping index is not an address-valued arithmetic operand.
            args=v['args']
            if len(args)!=2:raise Unsupported('arithmetic_arity')
            for arg in args:
                if arg.get('kind') not in ('op','literal') and self.typ(arg) not in ('uint','uint256'):
                    raise Unsupported('arithmetic_operand_width_not_lowered:'+self.typ(arg))
            left,right=[self.expr(x) for x in args]
            if not self.z.is_int(left) or not self.z.is_int(right):raise Unsupported('arithmetic_operand_sort')
            op=v['op']
            if op in ('/','%'):self.constraints.append(right>0)
            result={'+':lambda:left+right,'-':lambda:left-right,'*':lambda:left*right,'/':lambda:left/right,'%':lambda:left%right}[op]()
            self.constraints.extend([result>=0,result<2**256]);return result
        return super().expr(v)

````

## source/src/pr_next_joint/verification/joint_intrinsics.py

原文件 SHA-256 `f7abeba1589e49b957d3fbd10b7ee63c95c3915ec0b561ab720d264ab20c6ff7`

````python
"""Conservative symbolic intrinsics for source-bound M4 obligations.

Keccak over fixed ABI tuples is a congruent uninterpreted function, without
injectivity or a preimage oracle. UNSAT is usable in that overapproximation;
SAT involving this abstraction is never promoted to a confirmed prediction.
"""
from pr_next_joint.verification.expressions import Unsupported
from pr_next_joint.frontend.path_ir import walk

def intrinsic(e,v):
    z=e.z
    if v.get('kind')=='source_block_hash':
        height=e.expr(v['height']);current=e.expr(v['current'])
        if not z.is_int(height) or not z.is_int(current):raise Unsupported('block_hash_height_sort')
        name='environment_block_hash_by_height'
        if name not in e.functions:e.functions[name]=z.Function(name,z.IntSort(),z.IntSort())
        value=e.bound(e.functions[name](height),'bytes32')
        e.encoding_notes.append({'kind':'source_block_hash_environment','height':v['height'],
            'window':'the 256 preceding blocks; zero outside that window',
            'assumption':'shared conditional chain environment; historical chain values not verified'})
        return z.If(z.And(height<current,current-height<=256),value,z.IntVal(0))
    if v.get('kind')=='hash':
        from pr_next_joint.checks.credentials.credential_encoding import layout
        enc=layout(v)
        types=enc.get('types',[]);args=enc.get('arguments',[])
        if not types or len(types)!=len(args):raise Unsupported('hash_ABI_arity')
        normalized=[]
        for typ in types:
            if '[' in typ or typ in ('bytes','string') or typ.startswith(('struct ','tuple')):raise Unsupported('hash_dynamic_ABI_not_encoded')
            if typ!='bool' and not typ.startswith('fixed_bytes_literal:'):e.width(typ)
            normalized.append('address' if typ.startswith('contract ') else typ)
        from pr_next_joint.checks.credentials.credential_encoding import fixed_literal
        def argument(x):
            if x.get('kind')=='fixed_bytes_literal':
                raw,_=fixed_literal(x)
                return z.IntVal(int(raw,16) if raw else 0)
            return e.expr(x)
        values=[argument(x) for x in args]
        for typ,value in zip(normalized,values):
            if (typ=='bool' and not z.is_bool(value)) or (typ!='bool' and not z.is_int(value)):
                raise Unsupported('hash_ABI_argument_sort')
        signature={'algorithm':'keccak256','mode':enc['mode'],'types':normalized,'sorts':[str(x.sort()) for x in values]}
        name='h_'+e.name(signature)
        if name not in e.functions:e.functions[name]=z.Function(name,*[x.sort() for x in values],z.IntSort())
        e.encoding_notes.append({'kind':'keccak_fixed_ABI_congruence','signature':signature,
            'model':'uninterpreted function; no collision-free/injective or preimage assumption',
            'SAT_requires_concrete_confirmation':True})
        e.abstract_hash_used=True
        application=e.functions[name](*values)
        e.__dict__.setdefault('hash_terms',{})[application.sexpr()]={
            'application':application,'arguments':values,'types':normalized,'mode':enc['mode']}
        return e.bound(application,'bytes32')
    if (v.get('kind')=='member' and v.get('member')=='length'
        and v.get('base',{}).get('kind')=='member' and v['base'].get('member')=='code'):
        receiver=v['base'].get('base',{});typ=e.typ(receiver)
        if typ not in ('address','address payable') and not typ.startswith('contract '):raise Unsupported('code_length_receiver_not_address')
        declarations={x.get('id',x.get('root')) for x in walk(receiver) if x.get('kind') in ('parameter','storage')}
        if not declarations:raise Unsupported('code_length_source_receiver_missing')
        sourced=any(n.get('nodeType')=='MemberAccess' and n.get('memberName')=='code'
                    and declarations <= {x.get('referencedDeclaration') for x in walk(n.get('expression',{}))}
                    for n in e.lookup.nodes.values())
        if not sourced:raise Unsupported('code_length_not_in_source')
        address=e.expr(receiver);name='env_code_size_by_address'
        if name not in e.functions:e.functions[name]=z.Function(name,z.IntSort(),z.IntSort())
        e.encoding_notes.append({'kind':'source_address_code_length','receiver':receiver,
            'scope':'declared external environment; not evidence of actual deployed bytecode'})
        return e.bound(e.functions[name](address),'uint256')
    return None

````

