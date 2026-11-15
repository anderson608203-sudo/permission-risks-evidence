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
            physical_key=(target,family(cell))
            if temporal and physical_key not in cache:cache[physical_key]=_unit_origin(backend,oid,cell)
            if temporal and not cache[physical_key]:
                backend.__dict__.setdefault('unit_conflicts',{})[ck]={'cell':cell,'source_clock_comparisons':temporal,
                    'semantic_binding':bound['id'],'reason':'semantic amount not independently bound against source time dimension'}
                return None
            return {'kind':'source_bound_semantic_unit','binding':bound}
        original=_unit_origin(backend,oid,cell)
        return dict(original,semantic_conflict=bound) if original else None
    token=(backend.f.operations[oid]['target'],family(cell))
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


def same_unit_transfers(facts,target):
    """A conserved, spendable account quantity on an actual committing branch."""
    from .summary import holder,local_delta
    from .key_roles import relation
    from .initial_state import family
    from .policy_binding import conjuncts
    cache=facts.summaries.__dict__.setdefault('_transfer_unit_evidence',{})
    if target in cache:return cache[target]
    units={}
    for oid,operation in facts.operations.items():
        if operation['target']!=target:continue
        lookup=facts.lookup(oid)
        for row in facts.summaries.rows(oid):
            writes=row['ordered_writes']
            if len(writes)!=2 or row['residuals'] or row['effects']:continue
            moves={local_delta(w)[0]:w for w in writes}
            if not {'-','+'}<=moves.keys():continue
            debit,credit=(moves[s]['path'] for s in ('-','+'))
            if selector_relation(debit,credit)!='same_shape' or (relation(debit,lookup) or {}).get('kind')=='authorization_quantity':continue
            src,dst=holder(debit,lookup),holder(credit,lookup)
            if not src or not dst or key(src)==key(dst):continue
            if any(a.get('kind') not in ('actual_sender','parameter') for a in [src,dst]):continue
            qty=local_delta(moves['-'])[1]
            if not qty or qty.get('kind')!='parameter' or not qty.get('type','').startswith('uint'):continue
            if key(qty)!=key(local_delta(moves['+'])[1]):continue
            guards=[g for term in row['guards'] for g in conjuncts(term)]
            if not any((g.get('op') in ('>=','>') and list(map(key,g.get('args',())))==[key(debit),key(qty)])
                       or (g.get('op') in ('<=','<') and list(map(key,g.get('args',())))==[key(qty),key(debit)]) for g in guards):continue
            units.setdefault(family(debit),[]).append({'operation':oid,'path':row['path'],
                'source':moves['-']['source'],'credit_source':moves['+']['source']})
    cache[target]=units
    return units


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
    if keys(cell):
        # Financial unit belongs to the applied storage family, not the entry used to query it.
        # Confirm equal increment of a distinct scalar supply view on a real issuance branch.
        from .summary import local_delta
        for use,entry in facts.operations.items():
            if entry['target']!=target:continue
            for pid,p in backend.paths(use):
                moves=[(w,local_delta(w)) for w in p['writes']]
                for w,(sg,qty) in moves:
                    if sg!='+' or selector_relation(w['path'],cell)!='same_shape':continue
                    for sw,(other_sign,other_qty) in moves:
                        if other_sign!='+' or keys(sw['path']) or sw['path']['root']==cell['root'] or key(other_qty)!=key(qty):continue
                        if any(supply['root']==sw['path']['root'] for _,_,supply in supplies):
                            return {'kind':'source_supply_linked_token_unit','issuance_path':pid,'supply_declaration':sw['path']['root']}
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
    # A native deposit account also supports redistribution. That fact alone does
    # not establish an additional token unit under E1.
    if keys(cell) and not origins:
        from .initial_state import family
        use=same_unit_transfers(facts,target).get(family(cell))
        if use:return {'kind':'source_disposable_account_shares','unit_source':'program','origins':use}
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
            holder_indices=[i for i,k in enumerate(idx) if key(k)==key(holder)]
            if len(idx) != 2 or len(holder_indices)!=1 or idx[1-holder_indices[0]].get('kind') != 'actual_sender':
                continue
            holder_index=holder_indices[0]
            for w in facts.writes.values():
                other = w['operation']
                if facts.operations[other]['target'] != facts.operations[oid]['target']:
                    continue
                dst, val = w['raw']['path'], w['raw']['value']
                writer = facts.paths[w['path']]['raw']
                if (selector_relation(dst, cell) == 'same_shape' and len(keys(dst)) == 2
                        and keys(dst)[holder_index].get('kind') == 'actual_sender' and keys(dst)[1-holder_index].get('kind') == 'parameter'
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
            if not feasible['bounded_condition_confirmed']:
                rows.append({'feasible_probe':feasible['id'],'state':'premise_'+feasible['answer'],'scope':details})
                continue
            result = backend._query(e,z.And(base,violation),MEASURES[measure],details)
            queries.append(result)
            if measure=='ledger_grant' and result['bounded_condition_confirmed']:
                # Ask the actual extra predicate, not a test of one extracted
                # assignment. No address, amount or parameter is materialized.
                destination=backend._query(e,z.And(base,violation,h!=r,end1<h1,rend1-r1>effective),
                    'destination_credit_exceeds_grant',dict(details,measurement_only=True))
                queries.append(destination)
                result['predicate_checks']={'destination_credit_exceeds_grant':destination['bounded_condition_confirmed'],
                                            'check_id':destination['id']}
            rows.append({'feasible_probe':feasible['id'],'result_probe':result['id'],'state':result['answer'],
                         'scope':details})
        except Unsupported as error:
            errors.append({'path':p1,'before':p0,'change':cid,'reason':str(error)})
    return {'kind':'causal_compare','observed_measure':measure,'change':change,'observe':use,'queries':queries,
            'ledger_measurements':rows,'comparisons':[],'worlds':[],'alternative_uses':[],'holder_consent_counterexamples':[],
            'local_errors':errors,'net_measurements':[],'net_pair_budget':{'pairs':checked,'truncated':truncated},
            'evidence_scope':{'target':f.operations[use]['target'],'controls':spec['control_selectors'],
                              'request_context':context,'unit_origin':cells['origin']},
            'complete_for_modeled_observe_branches':backend.complete(use),'business_policy_proved':False,
            'no_program_mutation':True}

