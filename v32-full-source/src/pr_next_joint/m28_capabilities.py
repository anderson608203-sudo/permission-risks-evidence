"""Construct capability questions from committed effects and their source guards.

The same caller and request must be refused before a state change and be
able to commit a consequential action afterwards. A managed grant provides
independent policy evidence. Sharing a variable alone never establishes it.
"""
from collections import defaultdict
from .core import digest
from .m03_p_paths import key, lit, op, walk
from .m03_p_route import effective_permission, keys, fields, selectors, value_type
from .m04_logic import Unsupported
from .m05_bound_relations import family
from .m05_mechanism_core import remap
from .m05_state_relations import compose_read
from .m11_policy import make_query
from .m20_sequence import qualify, read, request_states
from .m21_admission import atoms
from .m22_assets import matches
from .m25_phase import clean

SENDER = {'kind': 'actual_sender'}


def conjunction(terms):
    return op('and', *terms) if terms else lit(True)


def later(term):
    # Distinct call arguments, but the principal testing this capability is the
    # same before/after and need not collude with an administrator.
    return remap(qualify(term, 1), {-9000001: SENDER})


def direct_admin(term, lookup):
    if term.get('op') != '==':
        return None
    left, right = term['args']
    if right == SENDER:
        left, right = right, left
    if left == SENDER and right.get('kind') == 'storage' and not right.get('segments') and value_type(right,lookup) in ('address','address payable'):
        return right
    return None


def actual_effects(path, lookup, assets, authorities=()):
    for e in path.get('native_transfers', []):
        if e['recipient'].get('kind') not in ('actual_sender','parameter','storage'):
            continue
        condition=[op('==',e['recipient'],SENDER), op('>',e['amount'],{'kind':'transaction_value','type':'uint256'}),
                   op('!=',SENDER,lookup.read_calls.address())]
        if e.get('success'):
            condition.append(e['success'])
        yield 'caller_receives_native_value', e['source'], condition
    for w in path['writes']:
        cell=w['path']
        if (not cell.get('segments') and cell['root'] in authorities and w['value'].get('kind') in ('actual_sender','parameter')
                and value_type(cell,lookup) in ('address','address payable')):
            final=compose_read(cell,path['writes'],lookup)
            yield 'replacement_of_live_principal',w['source'],[op('!=',cell,lit(0)),op('!=',cell,SENDER),op('==',final,SENDER)]
        if len(keys(cell))!=1 or keys(cell)[0].get('kind')!='parameter':
            continue
        if not any(matches(cell,a) for a in assets):
            continue
        # Read the committed balance, including later writes to aliased keys.
        final=compose_read(cell,path['writes'],lookup)
        yield 'other_holder_debit',w['source'],[op('!=',keys(cell)[0],SENDER),op('>',cell,final)]


def grant_candidates(path,lookup,linked_roots):
    """Allow source-bound semantic links to suggest a nonstandard caller gate.
    Validation still requires independent issuer and state-transition evidence."""
    effective={key(g) for g in effective_permission(path['guards'],lookup)}
    for guard in atoms(path['guards']):
        slots=selectors(guard)
        if len(slots)!=1:
            continue
        cell=slots[0]
        direct=direct_admin(guard,lookup)
        keyed=keys(cell)==[SENDER]
        if not direct and not keyed:
            continue
        if cell.get('instance'):
            continue
        static=key(guard) in effective
        if not static:
            if cell['root'] not in linked_roots or not keyed:
                continue
            if any(n.get('kind') not in ('storage','literal','op','actual_sender') for n in walk(guard) if n.get('kind')):
                continue
        yield guard,cell,static


def source_links(context,relations):
    ops={o['id']:o for o in context['operations']}
    refs=context['references']
    links=defaultdict(list)
    for rel in relations['relations']:
        for link in rel.get('operation_links',[]):
            if link['kind'] not in ('authorization_use','approval_execution'):
                continue
            writer=ops[link['from_op_ref']];user=ops[link['to_op_ref']]
            if writer['target']!=user['target']:
                continue
            cited={refs[s]['ast_id'] for s in link['source_refs']}
            consumer_evidence=set(user['source_ast_ids'])
            links[user['target'],user['function']].append((writer['function'],rel['id'],cited,consumer_evidence))
    return links


def eligible_writer(program,record,cell,lookup):
    w=record['effect'].get('original_write')
    if not w or not family(w['path'],cell):
        return None
    p=program[record['function']][record['path_index']]
    if not clean(p) or p.get('native_transfers') or p.get('sensitive_effects'):
        return None
    if lookup.function(record['function']).get('stateMutability')=='payable':
        return None
    # Exchanges, payments, ticket purchase and credential consumption require
    # their own entitlement model. This property only covers a pure grant.
    from .m25_reserve import write_only_mark
    same=[v for v in p['writes'] if key(v['path'])==key(w['path'])]
    if not same or same[-1]['source']!=w['source']:
        return None
    incidental=[v for v in p['writes'] if key(v['path'])!=key(w['path']) and not write_only_mark(v,lookup)]
    if incidental:
        from .m11_policy import once_latch
        latch=once_latch(p,program,lookup)
        if not latch or any(v['path']!=latch['latch'] or v['value']!=latch['closed_value'] for v in incidental):
            return None
    ks=keys(w['path'])
    # A caller recording their own membership alone does not establish a
    # power to grant a managed privilege to somebody else.
    if ks and (len(ks)!=1 or ks[0].get('kind')!='parameter'):
        return None
    return p,w


def source_admins(entries,lookup):
    # Each admin must be an actual required caller of a real grant. A guarded
    # revoke alone cannot establish the policy for enrollment.
    out={}
    for _,p,w in entries:
        if w['value'].get('kind')=='literal' and not w['value'].get('value'):
            continue
        for g in effective_permission(p['guards'],lookup):
            admin=direct_admin(g,lookup)
            if admin:
                out[key(admin)]=admin
    return list(out.values())


def plain_setup(path,lookup,latch=None):
    # A guard we cannot identify could be a valid claim, price, signature, time
    # or delegated authority. Do not reinterpret it as a permission violation.
    own={key(x) for x in effective_permission(path['guards'],lookup)}
    for g in atoms(path['guards']):
        if key(g) in own:
            continue
        if latch is not None and key(g) in (key(latch['latch']),key(op('!',latch['latch']))):
            continue
        if g.get('kind')=='literal' and g.get('value') is True:
            continue
        if g.get('op')=='!=' and any(x==lit(0) for x in g['args']) and any(x.get('kind') in ('parameter','actual_sender') for x in g['args']):
            continue
        return False
    return True


def endpoint_citations(links,source,cell,lookup,entry):
    uses=set()
    # The declaration may be cited directly, or through a cited expression in
    # the consuming function. Also require the actual grant statement.
    for writer,rid,cites,consumer_evidence in links:
        if writer!=entry or source['ast_id'] not in cites:
            continue
        others=(cites-{source['ast_id']}) & (consumer_evidence|{cell['root']})
        if any(a==cell['root'] or any(n.get('referencedDeclaration')==cell['root'] for n in walk(lookup.nodes.get(a,{}))) for a in others):
            uses.add(rid)
    return sorted(uses)


def alternate_routes(context,tid,lookup,program,index,relations):
    """Compare actual entry routes to the same compiled payout instruction.
    A protected sibling alone is insufficient: the alternate caller must
    control the payout, spend pre-existing funds, and consume no entitlement.
    """
    from .m21_admission import unify
    from .m25_reserve import write_only_mark
    by_site=defaultdict(list)
    for fn,paths in program.items():
        for pi,p in enumerate(paths):
            if not clean(p) or len(p.get('native_transfers',[]))!=1:
                continue
            e=p['native_transfers'][0]
            if e.get('kind')!='native_transfer' or any(not write_only_mark(w,lookup) for w in p['writes']):
                continue
            if len(p.get('sensitive_effects',[]))>1:
                continue
            by_site[(e['source']['file'],e['source']['ast_id'])].append((fn,pi,p,e))
    # M2 can nominate two distinct source sites representing the same service.
    # Bind both exact payment instructions and both external endpoints before
    # checking the amount, recipient, authority and accounting independently.
    ops={o['id']:o for o in context['operations']}
    proposed=defaultdict(set)
    for rel in relations['relations']:
        if rel['relation_kind'] not in ('controlled_by','checks_permission','delegates_to') or ops[rel['op_ref']]['target']!=tid:continue
        cited={context['references'][r]['ast_id'] for r in rel['source_refs']}
        peers={ops[r]['function'] for r in rel['related_op_refs']}
        named=ops[rel['op_ref']]['function']
        cited_routes=[r for (_,aid),rs in by_site.items() if aid in cited for r in rs if r[0]==named or r[0] in peers]
        for x in cited_routes:
            for y in cited_routes:
                if x[0]!=named or y[0] not in peers or x[0]==y[0] or x[3]['source']==y[3]['source']:continue
                pair=tuple(sorted(((x[0],x[1]),(y[0],y[1]))))
                proposed[pair].add(rel['id'])
    route_by_key={(r[0],r[1]):r for rs in by_site.values() for r in rs}
    batches=[(rs,[]) for rs in by_site.values() if len(rs)>1]
    batches.extend(([route_by_key[pos] for pos in pair],sorted(rids)) for pair,rids in proposed.items())
    rows=[];audit=[]
    for routes,relation_ids in batches:
        if len({r[0] for r in routes})<2:
            continue
        for fn,pi,p,e in routes:
            recipient,amount=e['recipient'],e['amount']
            if recipient.get('kind') not in ('actual_sender','parameter') or amount.get('kind')!='parameter':
                continue
            if effective_permission(p['guards'],lookup):
                continue
            # Unknown business, time, signature and state conditions can be
            # evidence of another authorized route; do not transfer the policy.
            business=[g for g in atoms(p['guards']) if g!=e.get('success')]
            if any(n.get('kind') not in ('actual_sender','literal','parameter','op') for g in business for n in walk(g) if n.get('kind')):
                continue
            if any(n.get('op') not in ('!=','==','and','&&','or','||','!') for g in business for n in walk(g) if n.get('kind')=='op'):
                continue
            # A parameter-only condition tying a payout to a signed or fixed
            # amount is outside this particular open-withdrawal property.
            if any(key(n)==key(amount) for g in business for n in walk(g)):continue
            guards=[];origins=[]
            for peer,_,other,other_effect in routes:
                if peer==fn:
                    continue
                ps=effective_permission(other['guards'],lookup)
                if len(ps)!=1 or not direct_admin(ps[0],lookup):
                    continue
                if any(g!=other_effect.get('success') and key(g)!=key(ps[0]) for g in atoms(other['guards'])):
                    continue
                if not unify([other_effect['recipient'],other_effect['amount']],[recipient,amount],{},lookup):
                    continue
                guards.append(ps[0]);origins.append(peer)
            if not guards:continue
            # Without an independently source-supported funded reserve, a
            # payable forwarder is not evidence of theft from a shared pool.
            funded=any(lookup.function(f).get('stateMutability')=='payable' and any(clean(x) and not x['writes'] and not x['guards']
                       and not x.get('sensitive_effects') for x in ps) for f,ps in program.items())
            if not funded:continue
            cond=[*p['guards'],op('==',recipient,SENDER),op('!=',SENDER,lookup.read_calls.address()),
                  op('>',amount,{'kind':'transaction_value','type':'uint256'}),op('<=',amount,{'kind':'native_reserve','instance':lookup.read_calls.address()})]
            guards={key(g):g for g in guards}
            for g in guards.values():
                cond.append(op('!=',direct_admin(g,lookup),lit(0)))
            row={'rule':'AC-01','target':tid,'function':fn,'path_index':pi,'effect':e,'conditions':cond,'issues':[],
                 'required_policy_candidate':op('or',*guards.values()),'source_evaluation_terms':p.get('evaluated_terms',[]),
                 'program_id':context['identity']['program_id'],'build_id':context['identity']['build_id'],
                 'policy_basis':{'basis':'paired_entry_same_unaccounted_reserve_payment','managed_entries':sorted(set(origins)),
                                 'relation_ids':relation_ids,'semantic_seed_required':bool(relation_ids),
                                 'source_sites':list({key(x[3]['source']):x[3]['source'] for x in routes}.values()),
                                 'source':e['source'],'scope':'caller-directed disposition of pre-existing reserve through a matched payout; conditional on available balance'}}
            row['id']='q_'+digest(row);rows.append(row)
            audit.append({'target':tid,'consumer':fn,'path':pi,'effects':[('native_payment',e['source'])],'queries':[row['id']],'limits':[]})
            for record in index.by_operation.get((tid,fn),[]):
                if record['path_index']==pi and record['effect'].get('source')==e['source']:
                    index.use(record,'alternate_entry_same_reserve',row['id'])
    return rows,audit


def analyze(context,state,index,shared,relations,queue):
    rows=[];audit=[];links=source_links(context,relations)
    for tid,lookup in state['lookups'].items():
        program={f:paths for (t,f),paths in state['paths'].items() if t==tid}
        assets=shared.get(tid,{}).get('assets',[])
        authorities=set()
        for (entry,_),p in queue.committed[tid].items():
            if p.get('native_transfers') or lookup.function(entry).get('stateMutability')=='payable':
                continue
            for g in effective_permission(p['guards'],lookup):
                a=direct_admin(g,lookup)
                if a and any(w['path']==a and w['value'].get('kind')=='parameter' for w in p['writes']):
                    authorities.add(a['root'])
        peers,peer_audit=alternate_routes(context,tid,lookup,program,index,relations)
        rows.extend(peers);audit.extend(peer_audit)
        for fn in dict.fromkeys(fn for fn,pi in queue.committed[tid]):
            paths=program[fn]
            proposals=links.get((tid,fn),[])
            roots_from_links={s['referencedDeclaration'] for _,_,refs,_ in proposals for ref in refs for s in walk(lookup.nodes.get(ref,{})) if 'referencedDeclaration' in s}
            roots_from_links.update(ref for _,_,refs,_ in proposals for ref in refs)
            for pi,path in enumerate(paths):
                if (fn,pi) not in queue.committed[tid] or not clean(path):
                    continue
                try:
                    sinks=list(actual_effects(path,lookup,assets,authorities))
                    if not sinks:
                        continue
                    stats={'target':tid,'consumer':fn,'path':pi,'effects':[(e,s) for e,s,_ in sinks],'queries':[],'limits':[]}
                    audit.append(stats)
                    for guard,cell,static in grant_candidates(path,lookup,roots_from_links):
                        if (fn,pi) not in queue.readers.get((tid,cell['root'],tuple(fields(cell))),{}):
                            continue
                        entries=[]
                        for rec in queue.writer_paths(tid,cell):
                            if rec['function']==fn:
                                continue
                            bound=eligible_writer(program,rec,cell,lookup)
                            if bound:
                                entries.append((rec,*bound))
                        admin=direct_admin(guard,lookup)
                        managers=source_admins(entries,lookup)
                        if admin:
                            managers.append(admin)
                        if not managers:
                            stats['limits'].append('no_independently_supported_grant_authority')
                            continue
                        for rec,setup,w in entries:
                            setter=rec['function']
                            cited=endpoint_citations(proposals,w['source'],cell,lookup,setter)
                            if not static and not cited:
                                continue
                            from .m11_policy import once_latch
                            latch=once_latch(setup,program,lookup) if len(setup['writes'])>1 else None
                            if not plain_setup(setup,lookup,latch):
                                stats['limits'].append('setup_may_have_business_entitlement')
                                continue
                            target_before,target_after=request_states(later(guard),setup['writes'],lookup)
                            if target_after==target_before:
                                continue
                            # Preserve every alternative successful path of the
                            # same entry. If authorization can't be shown absent
                            # on one, don't claim that the caller acquired access.
                            excluded=[];uncertain=False
                            for j,other in enumerate(paths):
                                if j==pi or other['flow'] in ('revert','reverted'):
                                    continue
                                if not clean(other):
                                    uncertain=True;break
                                other_sinks=list(actual_effects(other,lookup,assets,authorities))
                                if not other_sinks:
                                    continue
                                alternate=effective_permission(other['guards'],lookup)
                                if not alternate:
                                    # Only pre-state conditions depending on this same
                                    # grant can establish why the normal route was
                                    # unavailable. Never choose a failing external call.
                                    relevant=[g for g in atoms(other['guards'])
                                              if any(family(s,cell) for s in selectors(g)) and
                                              all(n.get('kind') in ('op','literal','storage','parameter','actual_sender')
                                                  for n in walk(g) if n.get('kind'))]
                                    if not relevant:
                                        uncertain=True;break
                                    alternate=relevant
                                excluded.append(op('!',later(conjunction(alternate))))
                            if uncertain:
                                stats['limits'].append('alternative_entry_path_unresolved')
                                continue
                            for typ,source,terminal in sinks:
                                model=dict(setup)
                                model['guards']=[*setup['guards'],op('!=',SENDER,lit(0)),*[op('!=',m,lit(0)) for m in managers],
                                    op('!',target_before),target_after,*excluded,*read(later(path['guards']+terminal),setup['writes'],lookup)]
                                model['evaluated_terms']=setup.get('evaluated_terms',[])+read(later(path.get('evaluated_terms',[])),setup['writes'],lookup)
                                required=op('or',*[op('==',SENDER,m) for m in managers],*effective_permission(setup['guards'],lookup))
                                basis={'basis':'effect_first_acquisition_of_source_guarded_capability','consumer':fn,'consumer_path':pi,
                                    'effect_kind':typ,'consumer_effect_source':source,'permission_before':target_before,'permission_after':target_after,
                                    'source_authorities':managers,'relation_ids':cited,'semantic_seed_required':not static,
                                    'scope':'same ordinary caller acquires a previously refused local financial operation, from symbolic active-authority state'}
                                q=make_query(context,tid,setter,rec['path_index'],model,w,required,basis,'AC-02')
                                rows.append(q);stats['queries'].append(q['id']);index.use(rec,'acquires_sensitive_capability',q['id'])
                                for rid in cited:index.use(rec,'source_verified_semantic_capability',q['id'],relation=rid)
                    if not stats['queries'] and not stats['limits']:stats['limits'].append('no_supported_state_mediated_grant_for_effect')
                except Unsupported as ex:
                    audit.append({'target':tid,'consumer':fn,'path':pi,'limitations':[str(ex)]})
    return rows,audit
