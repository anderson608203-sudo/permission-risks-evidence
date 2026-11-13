"""Schedule consumers from effects on bounded external-entry paths.

The compiled declaration, ordered key expressions and path stay on the original
record. A root edge indexes candidates; it never grants authority.
"""
from collections import defaultdict

from .m03_p_paths import key
from .m03_p_route import fields, selectors
from .m22_assets import matches


def independent_entitlement(query,lookup):
    """A local guard is not necessary for a source-bound missing-authority query.
    Recheck the sites before deferring to the normal solver and applicability gate."""
    basis=query.get('policy_basis',{})
    kind=basis.get('basis')
    if kind=='source_third_party_transfer_to_caller_without_applicable_holder_authority':
        sites=[*basis.get('self_service_debit_sites',[]),basis.get('credit_site')]
        if not basis.get('self_service_debit_sites') or basis.get('holder',{}).get('kind')!='parameter':
            return False
    elif kind=='redirect_live_prefunded_claim_to_unrelated_caller':
        origins=basis.get('funding',[])
        if not origins or not all(o.get('funding_formula') for o in origins):
            return False
        sites=[basis.get('redemption_site')]+[o[k] for o in origins for k in ('owner_site','deposit_site')]
    else:
        return False
    sites.append(query.get('effect',{}).get('source'))
    return all(s and s.get('ast_id') in lookup.nodes and lookup.anchor(lookup.nodes[s['ast_id']])==s for s in sites)


class OperationQueue:
    def __init__(self, state, index):
        self.index = index
        self.paths = state['paths']
        self.committed = defaultdict(dict)
        self.readers = defaultdict(dict)
        self.locations = defaultdict(list)
        self.seeds = defaultdict(list)
        self.financial_hints = defaultdict(list)
        self.outcomes = defaultdict(list)
        self.unavailable = []
        for (target, fn), paths in self.paths.items():
            for pi, path in enumerate(paths):
                pos = (fn, pi)
                if path['flow'] not in ('normal', 'returned'):
                    continue
                records = [r for r in index.by_operation.get((target, fn), ()) if r['path_index'] == pi]
                if path['issues'] or path.get('evaluation_gaps'):
                    if records or path.get('native_transfers'):
                        self.unavailable.append({'target': target, 'function': fn, 'path_index': pi,
                            'reasons': path['issues'] + path.get('evaluation_gaps', [])})
                    continue
                if not records and not path.get('native_transfers'):
                    continue
                self.committed[target][pos] = path
                for record in records:
                    src = record['effect'].get('source') or {}
                    self.locations[target, fn, src.get('ast_id')].append(record)
                for term in selectors(path['guards'] + [w['value'] for w in path['writes']]):
                    self.readers[target, term['root'], tuple(fields(term))][pos] = True

    def bind(self, context, relations):
        ops = {o['id']: o for o in context['operations']}
        refs = context['references']
        for rel in relations['relations']:
            op = ops[rel['op_ref']]
            for ref in rel['source_refs']:
                src = refs[ref]
                for record in self.locations.get((op['target'], op['function'], src['ast_id']), ()):
                    self.seeds[record['id']].append(rel['id'])
                    cell=record['effect'].get('selector')
                    if not cell or rel['relation_kind'] not in ('holder_of','debits_for_redemption','delegates_to'):
                        continue
                    resources=[rel.get('resource_ref'),*rel.get('resource_refs',[])]
                    resources.extend(b.get('resource_ref') for b in rel.get('resource_bindings',[])
                                     if b.get('op_ref')==op['id'])
                    if any(ref and refs[ref]['ast_id']==cell['root'] for ref in resources):
                        self.financial_hints[record['id']].append(rel['id'])

    def asset_paths(self, target, asset):
        seen = set()
        slots = self.index.writers.get((target, asset['balance_root'], tuple(fields(asset['balance_effect']['path']))), ())
        for record in slots:
            pos = (record['function'], record['path_index'])
            if pos in self.committed[target] and pos not in seen and matches(record['effect']['selector'], asset):
                seen.add(pos)
                yield pos

    def writer_paths(self, target, selector):
        return self.index.writers.get((target, selector['root'], tuple(fields(selector))), ())

    def note(self, target, fn, pi, status, reason, source=None, relations=()):
        item = {'status': status, 'reason': reason, 'source': source, 'relation_ids': sorted(set(relations))}
        bucket = self.outcomes[target, fn, pi]
        if item not in bucket:
            bucket.append(item)

    def report(self, checks):
        # Include specialist-only checks even when the graph could not index the site.
        by_entry = defaultdict(list)
        for q in checks:
            src = q.get('effect', {}).get('source') or q.get('source') or q.get('source_model', {}).get('effect', {}).get('source')
            by_entry[q.get('target'), q.get('function')].append((q, src))
        rows = []
        for target, positions in self.committed.items():
            for (fn, pi), path in positions.items():
                for r in self.index.by_operation.get((target, fn), ()):
                    if r['path_index'] != pi:
                        continue
                    source = r['effect'].get('source')
                    uses = []
                    for q, site in by_entry[target, fn]:
                        qi = q.get('path_index', q.get('source_model', {}).get('path_index'))
                        if site != source or (qi != pi and not (qi is None and key(q.get('conditions')) == key(path['guards']))):
                            continue
                        formal = q.get('formal', {})
                        uses.append({'query': q['id'], 'status': q.get('status'), 'reported': bool(q.get('reportable')),
                            'reason': formal.get('reason'), 'solver_called': formal.get('solver_called'),
                            'formula': formal.get('formula_sha256')})
                    notes = [n for n in self.outcomes.get((target, fn, pi), ()) if n['source'] in (None, source)]
                    rows.append({'effect_id': r['id'], 'source': source, 'target': target, 'function': fn, 'path': pi,
                        'semantic_seeds': sorted(set(self.seeds.get(r['id'], ()))), 'queries': uses, 'decisions': notes,
                        'disposition': 'checked' if uses else 'see_local_review' if notes else 'no_source_supported_duty_for_this_effect'})
        return {'effects': rows, 'incomplete_paths': self.unavailable,
                'specialist_checks': [q['id'] for q in checks], 'missing_duty_is_not_a_safety_proof': True}
