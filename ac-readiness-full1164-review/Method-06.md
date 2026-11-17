# 实际运行源码完整分段

完整文件按原路径列出，哈希指原文件字节。

## source/src/pr_next_joint/investigation/ledger.py

SHA-256 `4b4c9fe813c4624dc84713183354b40069daeaa73191c2256776c623bc94ef45`

```python
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


def same_unit_transfers(facts,target,*,include_checked_arithmetic=False):
    """A conserved, spendable account quantity on an actual committing branch."""
    from .summary import holder,local_delta
    from .key_roles import relation
    from .initial_state import family
    from .policy_binding import conjuncts
    cache=facts.summaries.__dict__.setdefault('_transfer_unit_evidence',{})
    stamp=(target,include_checked_arithmetic)
    if stamp in cache:return cache[stamp]
    version=facts.bundle.get('compiler',{}).get('compiler_version','')
    major,minor,*_=version.split('.')+['0','0']
    checked=include_checked_arithmetic and major.isdigit() and minor.isdigit() and (int(major),int(minor))>=(0,8)
    unchecked=[facts.lookups[target].anchor(n) for n in facts.lookups[target].nodes.values()
               if checked and n.get('nodeType')=='UncheckedBlock']
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
            src_loc=moves['-']['source']
            checked_debit=checked and not any(u['file']==src_loc['file'] and u['start']<=src_loc['start']<u['start']+u['length'] for u in unchecked)
            if not checked_debit and not any((g.get('op') in ('>=','>') and list(map(key,g.get('args',())))==[key(debit),key(qty)])
                       or (g.get('op') in ('<=','<') and list(map(key,g.get('args',())))==[key(qty),key(debit)]) for g in guards):continue
            units.setdefault(family(debit),[]).append({'operation':oid,'path':row['path'],
                'source':moves['-']['source'],'credit_source':moves['+']['source']})
    cache[stamp]=units
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
    # A readable address account and an independently reduced aggregate can
    # identify this unit even when the aggregate has no public supply getter.
    # Match the final writes on one committing path, never the spelling of a field.
    if getter:
        from .summary import holder, local_delta
        for use, entry in facts.operations.items():
            if entry['target']!=target:continue
            for pid,p in backend.paths(use):
                if p.get('issues') or p.get('evaluation_gaps') or p.get('sensitive_effects'):continue
                changes=[(w,*local_delta(w)) for w in p['writes']]
                accounts=[(w,sg,q) for w,sg,q in changes if selector_relation(w['path'],cell)=='same_shape']
                if len(accounts)!=1:continue
                w,sg,q=accounts[0]
                if sg!='-' or holder(w['path'],facts.lookup(use)) is None:continue
                for scalar,other,amount in changes:
                    position=scalar['path']
                    if other!='-' or keys(position) or position['root']==cell['root'] or key(q)!=key(amount):continue
                    if value_type(position,facts.lookup(use))!=value_type(cell,facts.lookup(oid)):continue
                    if sum(v['path']['root']==position['root'] for v in p['writes'])!=1:continue
                    return {'kind':'source_synchronized_account_reduction','path':pid,
                            'account_declaration':cell['root'],'supply_declaration':position['root'],
                            'holder_read':getter[0], 'account_location':w['source'], 'supply_location':scalar['source']}
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


```

## source/src/pr_next_joint/investigation/local_properties.py

SHA-256 `9733c67e1b55723c1a24e3f860d0ea6e8eb2854ed84daa6f75cff1fe1aecc18a`

```python
"""Typed, source-effect queries for a compiled property."""
import copy
import hashlib
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, selector_relation
from pr_next_joint.verification.sequence import qualify, read
from pr_next_joint.verification.source_worlds import frame, encode_frame
from pr_next_joint.verification.program_encoding import MechanismEncoder
from pr_next_joint.verification.expressions import Unsupported
from .ledger import movements, unit_origin, flow, grant_for
from .roles import path_qualification, fixed_role_terms
from .relations import beneficiary_condition


def audit_use_guards(b,policy):
    """Check each supplied use in its own frame, without synthesizing a grant sequence.

    This is a local well-formedness/consistency check. SAT here is never evidence
    of unauthorized acquisition. No input assignments are read from the solver.
    """
    from pr_next_joint.verification.solver import solve
    from pr_next_joint.core import digest
    results=[]
    for use in policy.get('acquisition_uses',[]):
        if b.remaining()<=0:
            results.append({'operation':use['operation'],'path':use['path'],'status':'not_executed','reason':'shared_budget'})
            continue
        oid,pid=use['operation'],use['path']
        record={'operation':oid,'path':pid,'target':b.f.operations[oid]['target'],
                'status':'open','scope':'individual_use_only','supports_takeover':False}
        results.append(record)
        try:
            p=b.f.paths[pid]['raw']
            if not safe_path(b,oid,pid,p):
                record['reason']='use_has_relevant_residual';continue
            e=MechanismEncoder(b.f.lookup(oid))
            fr=b.source_frame(oid,pid,0)
            term=encode_frame(e,fr)
            effect=_effect(e,fr,b.f.lookup(oid))
            solver=e.z.Solver()
            solver.add(term,effect,*e.constraints,*e.domain_constraints)
            text=solver.sexpr()
            formula_ref=hashlib.sha256(text.encode()).hexdigest()
            b.formulas.setdefault(formula_ref,{'sha256':formula_ref,'text':text,'scope_context':{
                'operation':oid,'path':pid,'scope':'individual use, no acquisition prefix or deployment reachability'}})
            b.check()
            answer=solve(solver,initial_ms=max(1,min(b.f.options.solver_timeout_ms,int(b.remaining()*1000))))
            record.update(status=str(answer),formula_ref=formula_ref,variable_domain='single isolated use frame',
                          source_guard_roots=sorted({s['root'] for s in selectors(p['guards'])}))
        except Unsupported as error:
            record.update(status='unsupported',reason=str(error))
        except TimeoutError:
            record.update(status='not_executed',reason='shared_budget')
        finally:
            evidence_key=digest([b.f.identity,oid,pid,record.get('formula_ref'),record['status']])
            b.__dict__.setdefault('use_guard_evidence',{})[evidence_key]=dict(record)
    return results


def safe_path(b, oid, pid, path):
    deps = b.condition_dependencies(oid, pid, path)
    if not path.get('source_call_subcases') and any(r['operation'] == oid and r['path'] == pid for r in b.f.call_summaries.rows.values()):
        roots = getattr(b,'active_property_roots',None) or {s['root'] for s in selectors([path['guards'],path['writes']])}
        # Demand-driven may analysis is shared between properties by its full
        # source/callpoint/root identity. It never turns an opaque return into
        # a successful call or a source-policy certificate.
        refinement = b.f.call_summaries.refine(b, oid, pid, roots)
        b.call_refinements = getattr(b,'call_refinements',{})
        b.call_refinements[refinement['id']] = refinement
        if any(c.get('same_storage_unresolved') or c.get('callback_projection') in
               ('may_influence','source_callpoint_not_precisely_lowered') for c in refinement['calls']):
            return False
    # Credential formulas are admitted to the backend, which checks exact
    # invalid-return domains and concretely verifies a candidate signature.
    # A symbolic recovered address alone never qualifies as a witness.
    return not deps['unknown_dependencies']


def _effect(e, fr, lookup):
    """Committed net effects, not merely returning from the entry."""
    z = e.z
    cells = {key(w['path']): w['path'] for w in fr['writes']}
    deltas = [e.expr(read(c, fr['before'] + fr['writes'], lookup)) !=
              e.expr(read(c, fr['before'], lookup)) for c in cells.values()]
    deltas += [e.expr(v['amount']) > 0 for v in fr['effects'] if v.get('amount') is not None]
    return z.Or(*deltas)


def necessary_effect_exclusion(b,oid,pid,context):
    """A pure necessary condition can refute a route with an unknown read.

    Unknown STATICCALL results are omitted, never assumed successful/false.
    An unresolved state-changing call cannot use this projection.
    """
    f=b.f;p=f.paths[pid]['raw'];req=context['observable']
    if req.get('measure')!='direct_effect' or p['flow'] not in ('normal','returned'):return None
    calls=[c for c in f.call_summaries.rows.values()if c['operation']==oid and c['path']==pid]
    if not calls or any(c['mode']!='STATICCALL' and c['unresolved_implementation']for c in calls):return None
    role=path_qualification(f,oid,p)
    if not role:return None
    try:
        e=MechanismEncoder(f.lookup(oid));z=e.z
        opaque={'unknown','external_return','read_call','call_unresolved','credential_recovery'}
        projection=dict(p,issues=[],evaluation_gaps=[],evaluated_terms=[],
            guards=[g for g in p['guards']if not any(n.get('kind')in opaque for n in walk(g))])
        fr=frame(f,oid,pid,0,path_override=projection)
        fr['evidence_world']='necessary_condition_projection_not_execution'
        guards=fr['guards']
        terms=[]
        for g in guards:
            mc,md=len(e.constraints),len(e.domain_constraints)
            try:terms.append(e.expr(g))
            except Unsupported:del e.constraints[mc:];del e.domain_constraints[md:]
        effects=[]
        for cell in (context.get('compiled_property')or{}).get('objects',[]):
            holder,start,end,_,_=flow(e,f.lookup(oid),fr,cell)
            effects.append(end>start if req['category']=='FCR-MINT' else end<start)
        if not effects:return None
        roles,origins=fixed_role_terms(e,role,0)
        detail={'operation':oid,'target':f.operations[oid]['target'],'use_path':pid,
            'property_identity':context.get('property_identity'),'semantic_version':context.get('semantic_version'),
            'category':req['category'],'property_validated':True,'necessary_condition_only':True,
            'omitted_read_results_are_unconstrained_not_assumed':True,'retained_guards':guards,
            'role_origins':origins,'unknown_read_cannot_modify_local_storage':True}
        q=b._query(e,z.And(*terms,*roles,e.expr(fr['caller'])!=0,z.Or(*effects)),
                   'source_necessary_condition',detail)
        if q['answer']=='unsat' and (q.get('exclusion_certificate',{}).get('excludes_only_this_formula') or
                q.get('details',{}).get('prestate',{}).get('global_reachability_exhausted')):
            return q
    except Unsupported:pass
    return None


def check_local(b, oid, primary_use, context):
    f = b.f
    lookup = f.lookup(oid)
    req = context['observable']
    kind = req['measure']
    queries, rows, gaps = [], [], []
    prop = context.get('compiled_property') or {}
    if kind in ('authorization_violation','denied_qualified'):
        from .policy_binding import audit_authorization
        audit=audit_authorization(f,oid,req.get('authorization'))
        if any(not r['matches'] for r in audit):
            return {'kind':'causal_compare','change':oid,'observe':primary_use,'queries':[],'property_excluded':False,
                    'local_errors':[{'reason':'source_ir_disagreement','checks':audit}],
                    'worlds':[],'comparisons':[],'property_identity':prop.get('id')}
    b.active_property_roots = {s['root'] for s in selectors([
        prop.get('objects',[]), (req.get('authorization') or {}).get('predicate',{})])}
    if kind in ('authorization_violation','denied_qualified'):
        # AC's effect predicate observes committed writes, including grant and
        # stage cells that are not financial asset objects. Their callbacks
        # must not be declared disjoint merely because objects is empty.
        uses=(req.get('authorization') or {}).get('acquisition_uses',[])
        related=[p for _,p in f.operation_paths(oid)]+[f.paths[u['path']]['raw'] for u in uses]
        b.active_property_roots.update(s['root'] for p in related for s in selectors([p['guards'],p['writes']]))
    b.active_property_objects = {s['root'] for s in selectors(prop.get('objects',[]))}
    necessary_closed={}
    for source_pid,source_path in f.operation_paths(oid):
        if not source_path.get('issues') and not source_path.get('evaluation_gaps'):continue
        exclusion=necessary_effect_exclusion(b,oid,source_pid,context)
        if exclusion:
            necessary_closed[source_pid]=exclusion['id'];queries.append(exclusion)
            rows.append({'state':'necessary_condition_unsat','scope':exclusion['details'],'result_probe':exclusion['id']})
    if any(e['operation']==oid and e['raw'].get('kind') in ('native_transfer','native_selfdestruct')
           for e in f.effects.values()):
        b.active_property_roots.add(-1)
    for source_pid, source_path in f.operation_paths(oid):
        if source_pid in necessary_closed:continue
        if any(c['operation']==oid and c['path']==source_pid for c in f.call_summaries.rows.values()):
            # Unresolved call paths cannot be upgraded to witness paths, but
            # their actual callpoint/guard projections still enter the shared
            # obligation and feedback records rather than vanishing at paths().
            if not b.source_path(oid,source_pid,source_path).get('source_call_subcases'):
                f.call_summaries.refine(b,oid,source_pid,b.active_property_roots)

    def pair(e, base, extra, details, values):
        details = dict(details, property_identity=context.get('property_identity'),
                       semantic_version=context.get('semantic_version'),
                       prefix_state_handoff=reached, prefix=reached.get('prefix',[]),
                       **({'initial_prefix_policy':'constructor_only_for_explicit_prefix'} if reached else {}),
                       property_validated=details.get('property_validated',True), validation='typed source entities and actual committed effect')
        feasible = b._query(e, base, 'local_premises_feasible', details)
        queries.append(feasible)
        if not feasible['bounded_condition_confirmed']:
            rows.append({'feasible_probe': feasible['id'], 'state': 'premise_' + feasible['answer'], 'scope': details})
            return
        tested = b._query(e, e.z.And(base, extra), kind, details)
        queries.append(tested)
        rows.append({'feasible_probe': feasible['id'], 'result_probe': tested['id'],
                     'state': tested['answer'], 'scope': details})

    reached=context.get('reached_state') or {}
    prefix_frames=reached.get('frames',[])
    prefix_writes=reached.get('writes',[])
    slot=len(prefix_frames)
    def current_frame(pid):
        return b.source_frame(oid,pid,slot,prefix_writes)
    def prefix_conditions(e):
        from .behavior import ordered_clocks
        return [encode_frame(e,pf) for pf in prefix_frames]+[e.expr(pf['caller'])!=0 for pf in prefix_frames]+ordered_clocks(e,slot)

    separate_uses=[]
    if kind == 'authorization_violation':
        policy = req.get('authorization')
        if not policy:
            gaps.append({'reason': 'authorization_relationship_not_bound'})
        else:
            acquiring = policy.get('property_family') == 'acquire'
            uses = policy.get('acquisition_uses', []) if acquiring else [None]
            if acquiring and not uses:
                gaps.append({'reason':'acquired_authority_has_no_bound_actual_use'})
            for pid, p in b.paths(oid):
                b.check()
                scoped_write=policy.get('effect_write')
                if scoped_write and scoped_write['path']!=pid:continue
                if not safe_path(b, oid, pid, p):
                    gaps.append({'path': pid, 'reason': 'authorization_path_dependency_unresolved'})
                    continue
                # A joint grant/use query owns its entire encoder. In particular
                # an unsupported sibling cannot leave domains, constraints,
                # credential/hash terms or symbols in a supported sibling.
                for row in uses:
                    b.check()
                    check = {'grant_path':pid,'operation':row['operation'] if row else oid,
                             'path':row['path'] if row else pid,'scope':'joint_grant_then_use',
                             'supports_takeover':False,'status':'open'}
                    if row: separate_uses.append(check)
                    try:
                        e = MechanismEncoder(lookup)
                        z = e.z
                        fr = current_frame(pid)
                        actor = e.expr(fr['caller'])
                        expected = e.expr(read(qualify(policy['predicate'],slot),prefix_writes,lookup))
                        if scoped_write:
                            cell=fr['writes'][scoped_write['version']]['path']
                            before=e.expr(read(cell,fr['before'],lookup))
                            after=e.expr(read(cell,fr['before']+fr['writes'],lookup))
                            effect=before!=after
                            if len(fr['writes'])>1:
                                version=scoped_write['version']
                                earlier=fr['before']+fr['writes'][:version]
                                at_write=e.expr(read(cell,earlier+[fr['writes'][version]],lookup))
                                effect=z.And(effect,at_write!=e.expr(read(cell,earlier,lookup)),at_write==after)
                        else:
                            effect=_effect(e,fr,lookup)
                        detail = {'operation':oid,'target':f.operations[oid]['target'],'use_path':pid,
                            'expected_authorization':policy,'actual_guards':fr['guards'],
                            'argument_domain':'all_source_inputs_on_this_committing_path',
                            'effect_required':True,'acquisition_use_required':acquiring}
                        values = {'caller':actor,'authorization_holds':expected}
                        clocks = []
                        if row:
                            up = f.paths[row['path']]['raw']
                            if not safe_path(b,row['operation'],row['path'],up):
                                raise Unsupported('acquired_authority_use_unresolved')
                            authority = row.get('authority') or policy.get('subject')
                            roots = {s['root'] for s in selectors(authority)}
                            if isinstance(authority,dict) and 'root' in authority: roots.add(authority['root'])
                            def conjuncts(term):
                                return [g for a in term['args'] for g in conjuncts(a)] if term.get('op') in ('and','&&') else [term]
                            gates = [g for guard in up['guards'] for g in conjuncts(guard)
                                     if roots & {s['root'] for s in selectors(g)}]
                            if not gates: raise Unsupported('acquired_authority_not_used_by_downstream_guard')
                            after = b.source_frame(row['operation'],row['path'],slot+1,prefix_writes+fr['writes'])
                            # The same request did not possess this qualification
                            # before the grant. A preexisting successful use is
                            # not evidence of newly acquired authority.
                            mark = len(e.constraints)
                            before_permission = z.And(*[e.expr(read(qualify(g,slot+1),prefix_writes,lookup)) for g in gates])
                            pre_checks = e.constraints[mark:];del e.constraints[mark:]
                            after_permission = z.And(*[e.expr(read(qualify(g,slot+1),prefix_writes+fr['writes'],lookup)) for g in gates])
                            productive = _effect(e,after,lookup)
                            use_caller=e.expr(after['caller'])
                            actor_links=[use_caller==actor];nominees=[]
                            # A requester can explicitly select a fresh
                            # controlled address in an unrestricted address
                            # grant. This is a conditional source subcase,
                            # not control of an arbitrary observed recipient.
                            for w in p['writes']:
                                value=w['value']
                                if w['path']['root'] not in roots or value.get('kind')!='parameter' or value.get('type') not in ('address','address payable'):continue
                                fixed=[g for guard in p['guards'] for g in conjuncts(guard)
                                       if g.get('op')=='==' and any(key(x)==key(value) for x in g.get('args',[])) and
                                       any(x.get('kind') in ('storage','literal','contract_address') for x in g.get('args',[]))]
                                if fixed:continue
                                selected=e.expr(qualify(value,slot))
                                actor_links.append(z.And(use_caller==selected,selected!=0))
                                nominees.append({'argument':value,'kind':'selectable_self_controlled_address',
                                    'conditional':True,'all_actual_source_restrictions_retained':True,
                                    'arbitrary_observed_recipient_control_not_assumed':True})
                            effect = z.And(effect,encode_frame(e,after),productive,
                                *pre_checks,z.Not(before_permission),after_permission,
                                z.Or(*actor_links))
                            from .behavior import ordered_clocks
                            clocks = ordered_clocks(e,slot+1)
                            detail.update(acquired_use=row,authority_gates=gates,
                                acquisition_precondition='same request lacks this authority before the actual grant',
                                actor_scope='same requester or a source-selectable controlled nominee; not a universal identity assumption',
                                nominee_control_subcases=nominees,
                                before_writes=prefix_writes,after_writes=prefix_writes+fr['writes'],
                                new_authority_required=True,downstream_effect_required=True)
                            values.update(use_caller=use_caller,
                                authority_before=before_permission,authority_after=after_permission,
                                downstream_effect=productive)
                        values['sensitive_effect']=effect
                        first=len(queries)
                        pair(e,z.And(encode_frame(e,fr),actor!=0,*prefix_conditions(e),*clocks),
                             z.And(effect,z.Not(expected)),detail,values)
                        checked=queries[first:]
                        check.update(status=checked[-1]['answer'] if checked else 'open',
                            probes=[x['id'] for x in checked],
                            supports_takeover=any(x['label']==kind and x['bounded_condition_confirmed'] for x in checked))
                    except Unsupported as error:
                        check.update(status='unsupported',reason=str(error))
                        gaps.append({'path':pid,'use':row,'reason':str(error)})
    elif kind == 'denied_qualified':
        policy = req.get('authorization')
        if not policy:
            gaps.append({'reason': 'qualified_denial_policy_not_bound'})
        else:
            subject = policy.get('subject')
            denial_roots={s['root'] for s in selectors(policy.get('predicate',{}))}
            if isinstance(subject,dict) and 'root' in subject:denial_roots.add(subject['root'])
            rejecting = [(pid, p) for pid, p in f.operation_paths(oid) if p['flow'] == 'reverted']
            for pid, p in rejecting:
                b.check()
                if not p['guards'] or not safe_path(b, oid, pid, p):
                    continue
                for spid, sp in b.paths(oid):
                  try:
                    if not safe_path(b,oid,spid,sp):
                        raise Unsupported('qualified_denial_productive_path_unresolved')
                    e = MechanismEncoder(lookup)
                    z = e.z
                    actor = e.expr(qualify({'kind': 'actual_sender'}, slot))
                    allowed = e.expr(read(qualify(policy['predicate'], slot),prefix_writes,lookup))
                    controls = {s['root'] for s in selectors(p['guards'][-1])}
                    if not (controls & denial_roots):
                        continue
                    sf = current_frame(spid)
                    def conjuncts(g):
                        return [v for a in g['args'] for v in conjuncts(a)] if g.get('op') in ('and','&&') else [g]
                    def only_authorization(g):
                        roots={s['root'] for s in selectors(g)}
                        return bool(roots & denial_roots) and roots<=denial_roots and any(
                            v.get('sequence_role')=='caller' for v in walk(g))
                    guards=[g for term in sf['guards'] for g in conjuncts(term)]
                    removed=[g for g in guards if only_authorization(g)]
                    if not removed:continue
                    conditioned=dict(sf,guards=[g for g in guards if not only_authorization(g)])
                    productive=z.And(encode_frame(e,conditioned),_effect(e,sf,lookup))
                    original_denial=z.And(*[e.expr(read(qualify(g,slot),prefix_writes,lookup)) for g in p['guards']])
                    detail = {'operation': oid, 'target': f.operations[oid]['target'], 'use_path': pid,
                              'productive_path':spid,'corrected_authorization_guards':removed,
                              'expected_authorization': policy, 'actual_denial': p['guards'],
                              'counterfactual_change': 'only the matched authorization guard is corrected',
                              'other_request_preconditions_retained': True, 'effect_required': True,
                              'argument_domain': 'all_source_inputs_on_this_rejecting_path'}
                    pair(e, z.And(actor != 0, allowed,productive,*prefix_conditions(e)),
                         original_denial, detail, {'caller': actor, 'authorization_holds': allowed})
                  except Unsupported as error:
                    gaps.append({'path':pid,'productive_path':spid,'reason':str(error)})
    elif kind == 'direct_effect':
        cat = req['category']
        if b.complete(oid) and not f.summaries.positions(oid) and all(
                not p.get('sensitive_effects') for _,p in b.paths(oid)):
            rows.append({'state':'not_privileged','operation':oid,
                'reason':'complete_source_has_no_direct_holder_quantity_effect',
                'scope':'local entry only; dependent value uses have separate obligations'})
        for pid, p in b.paths(oid):
            b.check()
            if not safe_path(b, oid, pid, p):
                gaps.append({'path': pid, 'reason': 'effect_path_dependency_unresolved'})
                continue
            qualification = path_qualification(f, oid, p)
            if not qualification:
                # Absence of a privileged path is a scoped exclusion when the
                # source is complete, not a new full-business detector.
                rows.append({'state': 'not_privileged', 'path': pid})
                continue
            try:
                e = MechanismEncoder(lookup)
                z = e.z
                fr = current_frame(pid)
                actor = e.expr(fr['caller'])
                roles, origins = fixed_role_terms(e, qualification, slot)
                moves = movements(b, oid, p)
                for cell in moves['+' if cat == 'FCR-MINT' else '-']:
                    b.check()
                    unit = unit_origin(b, oid, cell)
                    if not unit:
                        gaps.append({'path': pid, 'position': cell, 'reason': 'financial_unit_not_bound'})
                        continue
                    from .ledger import native_only_position
                    if native_only_position(b,oid,cell):
                        rows.append({'state':'not_privileged','path':pid,'position':cell,
                            'reason':'native_account_entitlement_without_source_token_unit_is_additional_scope'})
                        continue
                    holder, start, end, debit, credit = flow(e, lookup, fr, cell)
                    conditions = [end > start] if cat == 'FCR-MINT' else [end < start, holder != actor, holder != 0]
                    details = {'operation': oid, 'target': f.operations[oid]['target'], 'use_path': pid,
                               'role_provenance': qualification, 'encoded_role_origins': origins,
                               'ledger': cell, 'unit': unit, 'category_hypothesis': cat,
                               'argument_domain': 'all_source_inputs_on_this_committing_path',
                               'conditional_call_summary':fr.get('source_call_subcases',[]),
                               'predicate': 'source_bound_financial_effect'}
                    opposite = [c for c in moves['-' if cat == 'FCR-MINT' else '+']
                                if selector_relation(c, cell) == 'same_shape' and key(c) != key(cell)]
                    if cat == 'FCR-MINT':
                        controlled, basis = beneficiary_condition(e, fr, cell, holder)
                        conditions.append(controlled)
                        details['beneficiary'] = basis
                        # A transfer of an existing balance is not issuance.
                        conditions.extend(flow(e, lookup, fr, c)[1] <= flow(e, lookup, fr, c)[2] for c in opposite)
                    elif cat == 'FCR-TRANSFER':
                        destinations = []
                        for c in opposite:
                            from .summary import local_delta
                            debit_amounts = [local_delta(w)[1]
                                             for w in p['writes'] if selector_relation(w['path'],cell)=='same_shape' and
                                             local_delta(w)[0]=='-']
                            credit_amounts = [local_delta(w)[1]
                                              for w in p['writes'] if key(w['path'])==key(c) and
                                              local_delta(w)[0]=='+']
                            if not any(key(d)==key(part) for d in debit_amounts for a in credit_amounts for part in walk(a)):
                                gaps.append({'path':pid,'debit':cell,'credit':c,
                                             'reason':'same_ledger_credit_not_causally_bound_to_debit_quantity'})
                                continue
                            recipient, before, after, _, _ = flow(e, lookup, fr, c)
                            destinations.append(z.And(after > before, recipient != holder, recipient != 0))
                        conditions.append(z.Or(*destinations))
                        details['corresponding_same_ledger_credit'] = opposite
                    elif cat == 'FCR-DESTROY':
                        # Corresponding full token transfers preserve the right.
                        from .financial_value import distributed_value, native_settlement
                        paid,settlement=native_settlement(b,e,oid,fr,cell,holder)
                        conditions.append(start-end>distributed_value(b,e,oid,p,fr,cell,holder,all_transfers=False)+paid)
                        details['same_holder_settlement']=settlement
                    consent_resolved=True
                    if cat!='FCR-MINT':
                        from .financial_value import consent,interpretation_for
                        permitted,consent_resolved,basis=consent(b,e,oid,p,fr,cell,holder,start-end,
                            interpretation_for(prop,oid,pid,cell))
                        details['holder_consent']=basis
                        details['property_validated']=consent_resolved
                        conditions.append(z.Not(permitted))
                    bound = [e.expr(qualify(x['parameter'], slot)) == e.expr(x['value']) for x in context.get('bindings', [])]
                    pair(e, z.And(encode_frame(e, fr), actor != 0, *prefix_conditions(e), *roles, *bound), z.And(*conditions), details,
                         {'actor': actor, 'affected_account': holder, 'before': start, 'after': end, 'gross_debit': debit})
                    if not consent_resolved and queries[-1].get('answer')!='unsat':
                        gaps.append({'path':pid,'position':cell,'reason':'holder_authorization_quantity_basis_unresolved'})
            except Unsupported as error:
                gaps.append({'path': pid, 'reason': str(error)})
    else:
        # Preserve existing finite missing-control and qualified-denial probes.
        # Their output is evidence; the shared property consumer checks its
        # applicability before it can change a finding.
        return auxiliary_property(b, oid, primary_use, context)
    source_rows=list(f.operation_paths(oid))
    covered_with_necessary=bool(necessary_closed) and all(p['flow']=='reverted' or pid in necessary_closed or
        p['flow']in('normal','returned') and not p.get('issues') and not p.get('evaluation_gaps')
        for pid,p in source_rows) and not any(g['kind']=='path_extraction'for g in f.operations[oid]['gaps'])
    exclusion = not reached and bool(rows) and not gaps and (b.complete(oid) or covered_with_necessary) and all(
        r.get('state') in ('unsat', 'not_privileged','necessary_condition_unsat','premise_unsat') for r in rows)
    tested = [x for x in queries if x.get('label') in (kind,'source_necessary_condition') or x.get('label')=='local_premises_feasible' and x.get('answer')=='unsat']
    # Bounded UNSAT closes only its recorded domain unless the source
    # invariant certificate excludes every remaining initial stage.
    exclusion = exclusion and all(x.get('exclusion_certificate', {}).get('excludes_only_this_formula') or
                                  x.get('details', {}).get('prestate', {}).get('global_reachability_exhausted') for x in tested)
    from .quantity_checks import check_quantities
    amount_checks=check_quantities(b,prop) if kind=='direct_effect' else []
    return {'kind': 'causal_compare', 'observed_measure': kind, 'property_identity': context.get('property_identity'),
            'amount_correspondence':amount_checks,
            'independent_use_checks':separate_uses,
            'change': oid, 'observe': primary_use, 'queries': queries, 'property_measurements': rows,
            'property_excluded': exclusion, 'local_errors': gaps or ([] if rows else [{'reason': 'no_applicable_property_path'}]),
            'necessary_condition_route_coverage':{'source_identity':f.identity,'operation':oid,
                'excluded_paths':necessary_closed,'all_source_routes_accounted':covered_with_necessary} if necessary_closed else None,
            'worlds': [], 'comparisons': [], 'evidence_scope': {'target': f.operations[oid]['target'], 'request_context': context},
            'alternative_uses': [], 'holder_consent_counterexamples': [], 'net_measurements': []}

import re
from .request_scope import positive_caller_gate


def auxiliary_property(b,oid,primary_use,context):
    req=context['observable'];kind=req['measure']; f=b.f; lookup=f.lookup(oid)
    queries=[];rows=[];gaps=[]
    def pair(e,base,extra,details,values=None):
        feasible=b._query(e,base,'local_premises_feasible',details); queries.append(feasible)
        if not feasible['bounded_condition_confirmed']:
            rows.append({'feasible_probe':feasible['id'],'state':'premise_'+feasible['answer'],'scope':details});return
        tested=b._query(e,e.z.And(base,extra),kind,details);queries.append(tested)
        rows.append({'feasible_probe':feasible['id'],'result_probe':tested['id'],'state':tested['answer'],'scope':details})
    if kind=='authorization_violation':
        policy=req['authorization']
        for pid,p in b.paths(oid):
            b.check()
            if len(rows)>=f.options.max_prefixes:break
            if not safe_path(b,oid,pid,p):gaps.append({'path':pid,'reason':'authorization_path_dependency_unresolved'});continue
            try:
                e=MechanismEncoder(lookup);z=e.z;fr=frame(f,oid,pid,0)
                actor=e.expr(fr['caller']);expected=e.expr(qualify(policy['predicate'],0))
                detail={'operation':oid,'target':f.operations[oid]['target'],'use_path':pid,
                    'expected_authorization':policy,'actual_guards':fr['guards'],
                    'property_identity':context.get('property_identity'),'semantic_version':context.get('semantic_version',0),
                    'argument_domain':'all_source_inputs_on_this_committing_path'}
                pair(e,z.And(encode_frame(e,fr),actor!=0),z.Not(expected),detail,{'caller':actor,'authorization_holds':expected})
            except Unsupported as err:gaps.append({'path':pid,'reason':str(err)})
    elif kind=='missing_control':
        # Bind a flag to the very holder being debited on a real successful alternative,
        # after a committing writer. Unknowns on that alternative cannot establish a bypass.
        for alt in req['alternatives']:
            use=alt['use'];lookup=f.lookup(use)
            if not b.complete(use):gaps.append({'use':use,'reason':'incomplete_alternative_paths'})
            for cid,cp in b.paths(oid):
                for pid,p in b.paths(use):
                    b.check()
                    if len(rows)>=f.options.max_prefixes:break
                    if not safe_path(b,oid,cid,cp) or not safe_path(b,use,pid,p):
                        gaps.append({'path':pid,'reason':'unknown_on_selected_trace'});continue
                    try:
                        e=MechanismEncoder(lookup);z=e.z;cf=frame(f,oid,cid,0);uf=frame(f,use,pid,1,cf['writes'])
                        for cell in movements(b,use,p)['-']:
                            holder=keys(cell)[0]
                            controls=[w for w in cf['writes'] if len(keys(w['path']))==1 and value_type(w['path'],lookup)=='bool'
                                      and any(x['root']==w['path']['root'] for x in alt['control_writers'])]
                            if len(controls)!=1:continue
                            ctrl=controls[0]; h,_,_,debit,_=flow(e,lookup,uf,cell)
                            zc=e.expr(ctrl['value']);actor=e.expr(cf['caller']);requester=e.expr(uf['caller'])
                            from .behavior import ordered_clocks
                            base=z.And(encode_frame(e,cf),encode_frame(e,uf),*ordered_clocks(e,1),actor!=0,requester!=0,
                                       e.expr(keys(ctrl['path'])[0])==h,h!=0,zc)
                            detail={'change':oid,'observe':use,'change_path':cid,'use_path':pid,'object':cell,'active_holder_control':ctrl['path'],
                                    'control_value':True,'actual_guard_reads':alt['control_reads'],'peer_controlled_uses':alt['peer_controlled_uses'],
                                    'policy_requires_blocking_this_entry':'semantic_hypothesis_only'}
                            pair(e,base,debit>0,detail,{'holder':h,'caller':requester,'gross_debit':debit})
                    except Unsupported as err:gaps.append({'path':pid,'reason':str(err)})
    elif kind=='direct_effect':
        for pid,p in b.paths(oid):
            b.check()
            if len(rows)>=f.options.max_prefixes:break
            if not safe_path(b,oid,pid,p):gaps.append({'path':pid,'reason':'unresolved_dependency'});continue
            qualification=path_qualification(f,oid,p)
            if not qualification:gaps.append({'path':pid,'reason':'no_direct_positive_runtime_role_gate'});continue
            try:
                e=MechanismEncoder(lookup);z=e.z;fr=frame(f,oid,pid,0);actor=e.expr(fr['caller'])
                role_terms, fixed_origins=fixed_role_terms(e,qualification,0)
                moves=movements(b,oid,p); cat=req.get('category')
                for cell in moves['+' if cat=='FCR-MINT' else '-']:
                    origin=unit_origin(b,oid,cell)
                    if not origin:gaps.append({'path':pid,'reason':'unresolved_financial_unit'});continue
                    holder,start,end,dr,cr=flow(e,lookup,fr,cell)
                    detail={'operation':oid,'target':f.operations[oid]['target'],'use_path':pid,'role_guards':[x['guard'] for x in qualification],
                            'role_provenance':qualification,'encoded_role_origins':fixed_origins,'ledger':cell,'unit':origin,
                            'category_hypothesis':cat,'extent':'direct role-gated change of one ledger position; no global supply/consent or compensation judgment'}
                    detail.update(property_identity=context.get('property_identity'),semantic_version=context.get('semantic_version',0))
                    values={'actor':actor,'affected_account':holder,'before':start,'after':end,'gross_debit':dr,'gross_credit':cr}
                    if cat=='FCR-MINT':
                        # This specific probe tests the controller as actual beneficiary.
                        values['self_beneficiary']=holder==actor
                        condition=z.And(end>start,holder==actor)
                    else:condition=z.And(end<start,holder!=actor,holder!=0)
                    if cat=='FCR-TRANSFER':
                        destinations=[]
                        for c in moves['+']:
                            if selector_relation(c,cell)!='same_shape' or key(c)==key(cell):continue
                            recipient,pre,post,_,_=flow(e,lookup,fr,c)
                            destinations.append(z.And(post>pre,recipient!=holder,recipient!=0))
                        condition=z.And(condition,z.Or(*destinations))
                        detail['destination_credit_required']=True
                    bound=[]
                    for binding in context.get('bindings',[]):
                        bound.append(e.expr(qualify(binding['parameter'],0))==e.expr(binding['value']))
                    for a,c,relation in context.get('request_aliases',[]):
                        aa=e.expr(qualify(a,0));cc=e.expr(qualify(c,0));bound.append(aa==cc if relation=='==' else aa!=cc)
                    detail['predicate']='positive_credit_to_caller' if cat=='FCR-MINT' else 'negative_delta_of_other_nonzero_holder'
                    detail['argument_domain']='all_source_inputs_on_this_committing_path'
                    if context.get('request_aliases'):
                        detail.update(argument_domain='recorded_claim_aliases',claim_aliases=context['request_aliases'])
                    pair(e,z.And(encode_frame(e,fr),actor!=0,*role_terms,*bound),condition,detail,values)
            except Unsupported as err:gaps.append({'path':pid,'reason':str(err)})
    elif kind=='denied_qualified':
        # Eligibility is a named source role backed by a positive use on another
        # applied entry. Its applicability to this use remains an explicit hypothesis.
        for pid,p in f.operation_paths(oid):
            if p['flow']!='reverted' or not p['guards'] or len(rows)>=f.options.max_prefixes:continue
            b.check()
            if not safe_path(b,oid,pid,p):gaps.append({'path':pid,'reason':'unknown_rejection_dependency'});continue
            cause=p['guards'][-1]
            leaf=cause
            while leaf.get('op')=='!' and len(leaf['args'])==1:leaf=leaf['args'][0]
            if leaf.get('op') not in ('==','!=') or not any(x.get('kind')=='actual_sender' for x in leaf['args']):continue
            roles=[c for c in selectors(leaf) if not keys(c) and value_type(c,lookup) in ('address','address payable')]
            if len(roles)!=1:continue
            role=roles[0]; name=b._storage_name(oid,role)
            if not re.search(r'(?<![\w$])'+re.escape(name)+r'(?![\w$])',req['claim'],re.I):continue
            peers=[j for j,o in f.operations.items() if j!=oid and o['target']==f.operations[oid]['target'] and any(
                positive_caller_gate(g,lookup) and any(key(c)==key(role) for c in selectors(g)) for _,v in b.paths(j) for g in v['guards'])]
            if not peers:continue
            if p.get('writes') or p.get('sensitive_effects'):gaps.append({'path':pid,'reason':'complex_pre_rejection_effects'});continue
            try:
                e=MechanismEncoder(lookup);z=e.z;actor=e.expr(qualify({'kind':'actual_sender'},0))
                for term in p.get('evaluated_terms',[]):e.expr(qualify(term,0))
                earlier=[e.expr(qualify(g,0)) for g in p['guards'][:-1]]
                policy=actor==e.expr(qualify(role,0))
                base=z.And(actor!=0,policy,*earlier)
                detail={'operation':oid,'revert_path':pid,'role':role,'positive_role_use_sources':peers,'non_authorization_prefix':p['guards'][:-1],
                        'denial_condition':cause,'role_eligibility_at_use':'source-backed semantic hypothesis','failed_request_commits_writes':False}
                pair(e,base,e.expr(qualify(cause,0)),detail,{'caller':actor,'role':e.expr(qualify(role,0))})
            except Unsupported as err:gaps.append({'path':pid,'reason':str(err)})
    return {'kind':'causal_compare','observed_measure':kind,'change':oid,'observe':primary_use,'queries':queries,'property_measurements':rows,
            'local_errors':gaps or ([] if rows else [{'reason':'no_source_supported_path_for_property'}]),'worlds':[],'comparisons':[],
            'evidence_scope':{'target':f.operations[oid]['target'],'request_context':context,'controls':[]},
            'alternative_uses':[],'holder_consent_counterexamples':[],'net_measurements':[],'business_policy_proved':False}

```

## source/src/pr_next_joint/investigation/policy_binding.py

SHA-256 `ca3834eda4f4a6174b381116ab14d31cb09de380fec655d4b6a0bbfa97aad145`

```python
"""Scope source explanations before compiling an authorization predicate.

The source signature is derived from the located explanation and the applied
entry's committed paths. The compiled signature is read back from the IR.
Only the supported equivalences of boolean literals and ordered cells are used.
"""
import re

from pr_next_joint.frontend.path_ir import key, lit, op
from pr_next_joint.frontend.storage import keys, value_type
from pr_next_joint.frontend.source_entry_identity import function_kind
from .key_roles import relation as key_role


def mentioned(text, name):
    return bool(name and re.search(r'(?<![\w$])' + re.escape(name) + r'(?![\w$])', text))


def effect_duty(text):
    """Identify the subject of a responsibility, not the subjects of nearby observations.

    Subject phrases are open vocabulary. Only the positive argument of a
    permission, duty, assignment or required consent can enter source binding.
    """
    if not isinstance(text, str): return None
    roles = []
    qualified = False
    alternative = False
    noun = r"(?P<actor>[\w$][\w$.'’ -]*?)"
    frames = (
        r"\bonly\s+" + noun + r"\s+(?:may|can|is entitled to|is allowed to)\s+\w+",
        r"^(?:only\s+)?" + noun + r"\s+(?:is|are|remains?)\s+(?:solely\s+)?(?:responsible for|entrusted with|authorized to|in charge of)\s+\w+",
        r"^" + noun + r"\s+(?:who\s+)?(?:governs?|has authority over|has the right to decide)\s+\w+",
        r"^" + noun + r"\s+(?:must|shall)\s+(?:also\s+)?(?:consent|authorize|approve)\b",
        r"\b(?:assigns?|entrusts?|reserves?)\s+[^,;.!?]*\b(?:decision|responsibility|approval|authority|right|appointment|discretion)\b[^,;.!?]*?\s+to\s+" + noun + r"$",
        r"\b(?:decided by|authorized solely by)\s+" + noun + r"$",
        r"\b(?:decisions?|authority|responsibility)\s+(?:is|are|remains?)\s+" + noun + r"['’]s(?:\s+\w+)?$",
        r"\bat\s+" + noun + r"['’]s\s+discretion\b",
        r"\b(?:responsibility|right|authority|decision)\b[^;,.]*?\b(?:belongs to|lies with|rests with|is reserved for)\s+" + noun + r"$",
        r"\b(?:requires?|needs?|without)\s+" + noun + r"(?:['’]s|\s+)\s*(?:approval|consent|authorization)\b",
        # "also" adds a prerequisite; it must not make the whole consent
        # clause disappear while a different actor's authority remains normal.
        # Keep it inside the positive requirement grammar, so "not required"
        # and "also not required" do not become affirmative holder consent.
        noun + r"(?:['’]s|\s+)\s*(?:approval|consent|authorization)\s+(?:is\s+(?:also\s+)?(?:required|necessary)|must\s+(?:also\s+)?be\s+obtained)\b",
        r"(?:只有|仅限)\s*(?P<actor>[\w$]+?)\s*(?:有权|才可|才能)",
        r"(?:须经|必须经|应由)\s*(?P<actor>[\w$]+?)\s*(?:同意|授权|批准|决定)",
    )
    for part in re.split(r"[;；。!?，,]|\.(?=\s|$)|\b(?:but|yet|whereas|although|however)\b", text, flags=re.I):
        clause = part.strip()
        # The subject of an executable check describes a precondition. It does
        # not assign the authority to make the business decision.
        if re.match(r"^(?:(?:in|under|according to)\s+)?(?:the\s+)?(?:actual\s+|current\s+|implemented\s+)?(?:implementation|source(?:\s+code)?|code|runtime|guard|[\w$]+\s+(?:guard|check))\b", clause, re.I):
            continue
        restriction = re.search(r"\b(only if|if|unless|provided(?: that)?|subject to|together with|in addition to|as well as|with(?= (?:the )?(?:[\w’'-]+\s+){0,4}(?:consent|approval)))\s+(.*)$", clause, re.I)
        additional = None
        if restriction:
            # Separate the approval of another actor from a condition on the
            # first actor's identity. Unknown qualifiers cannot certify a normal.
            rest = restriction[2]
            if restriction[1].casefold() != 'unless':
                agreed = (re.match(r"(?:the\s+)?(?:consent|approval|authorization)\s+(?:of|from)\s+" + noun + r"$", rest, re.I)
                          or re.match(noun + r"(?:['’]s\s+|\s+)(?:also\s+)?(?:consents?|approves?|authoriz(?:es|ation)|approval)\b", rest, re.I))
                if agreed:
                    additional = agreed['actor']
            clause = clause[:restriction.start()].strip()
            if not clause and roles:
                if additional and not alternative:
                    roles.append(additional)
                else:
                    qualified = True
                continue
        for pattern in frames:
            match = re.search(pattern, clause, re.I)
            if not match:
                continue
            if re.search(r"\b(?:not|never|neither|whether|if)\s+(?:solely\s+)?$", clause[:match.start()], re.I):
                continue
            actor = match['actor'].strip()
            if re.search(r"\b(?:not|never|neither|whether|if|unless)\b", actor, re.I):
                continue
            names = re.split(r"\s+(and|or)\s+", actor, flags=re.I)
            joins = {s.casefold() for s in names[1::2]}
            qualified |= len(joins) > 1 or bool(roles and (alternative or 'or' in joins))
            alternative |= 'or' in joins
            actors = names[::2]
            if restriction:
                if additional:
                    actors.append(additional)
                    qualified |= alternative
                else:
                    qualified = True
            for value in actors:
                value = re.sub(r"^(?:(?:only|the|a|an|same)\s+)+", "", value.strip(), flags=re.I)
                if value and value.casefold() not in ('their','his','her','its','it','they'):
                    if value.casefold() not in [v.casefold() for v in roles]:
                        roles.append(value)
            break
    if not roles:
        return None
    return {'actors': roles, 'alternative': alternative, 'qualified': qualified}


def positive_role_reference(text, name):
    """A denial of the relevance of a named role is not a policy in its favour."""
    for part in re.split(r'[;；,，]|(?<=[.!?])\s+|\b(?:but|whereas|however)\b', text, flags=re.I):
        if not mentioned(part, name):
            continue
        qualifier=r'(?:[A-Za-z_$][\w$]*\.)*' if '.' not in name else ''
        token = r'(?<![\w$])' + qualifier + re.escape(name) + r'(?![\w$])'
        denial = (r'\b(?:no|not|without|neither)\s+(?:(?:the|an?|any|require[sd]?|requiring|need[s]?|be|being)\s+){0,4}'
                  + token + r'|' + token + r'.{0,28}\b(?:not (?:required|needed|applicable)|irrelevant)\b')
        if not re.search(denial, part, re.I):
            return True
    return False


def creation_source(text, entry, operations):
    """Bind normative deployment language to its subject, not a distant use."""
    name = entry['function'].split('(')[0]
    names = {o['function'].split('(')[0] for o in operations.values() if o['target']==entry['target']}
    focus = set()
    for clause in re.split(r'[;；，,]|(?<=[.!?。])\s+|\b(?:but|whereas|however)\b', text, flags=re.I):
        creation = re.search(r'\b(?:deployment.only|only (?:at|during) (?:construction|creation|deployment)|'
                             r'(?:intended|meant|supposed|required|should|must)\b.{0,38}\b(?:constructor|deployment|creation)\b|'
                             r'constructor.only|constructor\s+(?:only|semantics))', clause, re.I)
        # Objects listed as effects after "deployment-only" are not the
        # grammatical subject of that restriction.
        head=clause[:creation.start()] if creation else clause
        found={n for n in names if mentioned(head,n)}
        if found:
            focus=found
        elif not re.search(r'\b(?:it|this|the function|required|authorization|deployment.only)\b',clause,re.I):
            focus=set()
        if focus=={name} and creation:
            return clause.strip()
    return None


def boolean_leaf(term):
    """Return the storage atom and truth value for one committing-path guard."""
    if not isinstance(term, dict):
        return None
    if term.get('kind')=='storage':
        return term, True
    args=term.get('args', [])
    if term.get('op') in ('!', 'not') and len(args)==1:
        child=boolean_leaf(args[0])
        return (child[0], not child[1]) if child else None
    if term.get('op') in ('==','!=') and len(args)==2:
        for atom,const in (args, reversed(args)):
            if const.get('kind')=='literal' and type(const.get('value')) is bool:
                child=boolean_leaf(atom)
                if child:
                    return child[0], child[1] == (const['value'] == (term['op']=='=='))
    return None


def conjuncts(term):
    if term.get('op') in ('&&','and'):
        return [a for v in term['args'] for a in conjuncts(v)]
    return [term]


def stated_boolean(text,name):
    token=r'(?<![\w$])'+re.escape(name)+r'(?![\w$])'
    sub=token+r'(?:\s*\[[^\]]+\]){0,3}'
    values=set()
    if re.search(r'!\s*'+sub,text) or re.search(sub+r'\s*(?:==|is|must be)\s*false\b',text,re.I):
        values.add(False)
    if re.search(sub+r'\s*(?:==|is|must be)\s*true\b',text,re.I):
        values.add(True)
    collective=re.search(r'\bboth\s+(?:be\s+)?(true|false)\b',text,re.I)
    if collective and mentioned(text,name):values.add(collective[1].lower()=='true')
    return values


def payment_policy(text, role_name, scope_names):
    """Read the asserted relation between actual role and payment operands."""
    pay = r'\b(?:payment|paying|paid|fee)\b'
    role = r'(?<![\w$])' + re.escape(role_name.lower()) + r'(?![\w$])'
    names = {n.lower() for n in scope_names if n}
    relations = set()
    text = re.sub(r'["“][^"”]*["”]|(?<!\w)\x27[^\x27\n]+\x27(?!\w)', ' ', text.lower())
    # Retain the payment subject through a nominal complement. The modal
    # predicate below still decides sufficiency, denial and contradictions.
    text=re.sub(r'\bpayment of (?:the |a )?(?:fee|charge)\b','payment',text)
    for sentence in re.split(r'[;；。!?\n]|(?<=\.)\s+', text):
        if re.search(role+r'\s+or\s+(?:an? |the )?(?:customer|holder|caller)\s+paying\b',sentence) and re.search(r'\bmay independently authorize\b',sentence):
            relations.add('independent')
        payment_subject = False
        # A role-only requirement in a following contrastive clause still
        # qualifies an earlier claimed payment permission in this sentence.
        sentence_mentions_payment = bool(re.search(pay, sentence))
        for clause in re.split(r'\b(?:but|whereas|however)\b', sentence):
            clause = clause.strip(' ,.'); scoped = re.search(r'\b(?:policy|rule) (?:for|of|on) (?:the )?([\w.$]+)', clause)
            if scoped and scoped[1].split('.')[-1] not in names | {'entry','effect','action','operation'}:
                continue
            if re.search(r'\b(?:implementation|implemented|hypothetically|supposed|mistakenly|incorrectly)\b', clause):
                continue
            if payment_subject and re.match(r'^it\b', clause):
                clause = 'payment' + clause[2:]
            clause = re.sub(r'^(?:under|according to) (?:the )?(?:policy|rule)(?: for [\w.$]+)?,\s*', '', clause)
            payment_subject = bool(re.match(r'^(?:(?:the|a|threshold|qualifying)\s+)*'+pay, clause))
            mentions_pay = bool(re.search(pay, clause))
            if re.search(r'\b(?:unclear|unresolved|unknown|uncertain|whether|undetermined)\b', clause):
                if mentions_pay: relations.add('unresolved')
                continue
            # Modal qualifiers qualify the entitlement itself. An additional
            # condition of unknown meaning cannot yield unrestricted permission.
            restricted = re.search(r'\b(?:if|unless|provided|subject to|except|conditional on)\b',clause)
            same_effect = any(mentioned(clause,n) for n in names) or re.search(r'\b(?:this|same) (?:action|effect|entry)\b',clause)
            exclusive = re.search(r'\bonly\s+(?:(?:the|a|current|authorized|incumbent)\s+)*'+role+
                                  r'(?:\s+holder)?\s+(?:may|can|must|is (?:authorized|permitted) to)\s+\w+',clause)
            if exclusive and not restricted and not re.search(r'\b(?:not|denies|rejects?)\s+$',clause[:exclusive.start()]):
                if same_effect or re.search(r'\b(?:authorize|approve)$',clause):
                    relations.add('role_required')
            if not mentions_pay:
                # Do not let 'payment can substitute, but callers must ALSO
                # hold the office' become an unconditional OR authorization.
                # This expresses a conflict with a purported independent
                # alternative; it does not prove a new authorization policy.
                caller_requires_role = re.search(
                    r'\b(?:caller|applicant|requester)\b.{0,35}\b'
                    r'(?:must|shall|needs? to|is required to)\s+(?:also\s+)?'
                    r'(?:be\s+)?(?:the\s+)?'+role, clause)
                role_is_required = re.search(role+r'\s+(?:is|remains)\s+'
                    r'(?:also\s+)?(?:required|necessary|mandatory)\b', clause)
                if sentence_mentions_payment and (caller_requires_role or role_is_required):
                    relations.add('role_required')
                continue
            policy = re.match(r'^(?:(?:the|this|applicable|approved|authorization|stated|intended|business)\s+)*'
                              r'(?:policy|rule)(?:\s+(?:for|of|on)\s+[\w.$()]+)?\s+'
                              r'(?:(?:expressly|explicitly|strictly|specifically)\s+)?'
                              r'(?:(?:does|can|may)\s+)?'
                              r'(?:(?:expressly|explicitly|strictly|specifically)\s+)?'
                              r'(?P<neg>not\s+|never\s+)?(?P<verb>allows?|permits?|accepts?|forbids?|rejects?|requires?)\b(?P<object>.*)',clause)
            obj = policy['object'] if policy else clause
            has_role = bool(re.search(role,obj))
            joint = has_role and (re.search(r'\b(?:only\s+)?(?:in addition to|together with|in conjunction with)\b',obj)
                    or re.search(r'\bboth\b.+\band\b',obj) and
                    (re.search(r'\b(?:required|necessary|needed)\b',obj) or policy and policy['verb'].startswith('require')))
            denied = bool(policy and (bool(policy['neg']) != policy['verb'].startswith(('forbid','reject'))))
            denies_alternative = re.search(r'\b(?:not|never)\s+(?:as\s+)?(?:an?\s+)?(?:alternative|substitute|authorization|qualification)\b',obj)
            explicit_requirement = re.fullmatch(r'both\s+(?:the\s+)?'+role+
                r"(?:'s)?(?:\s+(?:approval|authorization|consent))?\s+and\s+(?:the\s+)?(?:payment|fee)\s+(?:are|remain)\s+(?:required|necessary)",clause)
            normative_joint = bool(policy or explicit_requirement or same_effect and re.search(r'\b(?:must|required|necessary|needed)\b',obj))
            either_or = bool(has_role and re.search(r'\beither\b.+\bor\b',obj))
            if joint and normative_joint:
                negated_joint = re.search(r'\b(?:not|never)\s+(?:only|together|required|necessary|needed)\b',obj)
                relations.add('unresolved' if restricted or denied or negated_joint or either_or else 'joint')
                continue
            if not policy and not payment_subject: continue
            if policy and policy['neg'] and policy['verb'].startswith(('forbid','reject')):
                relations.add('unresolved')
                continue
            if restricted or re.search(r'\bonly\b(?! (?:the|a|current) )',obj):
                relations.add('unresolved')
                continue
            alternative = re.search(r'\b(?:alternative|either\b.+\bor|in place of|instead of|replace[sd]?|substitut\w*)\b',obj)
            authority = re.search(r'\b(?:authoriz\w*|sufficient|qualif\w*|constitut\w* authorization)\b',obj)
            if not alternative and not authority: continue
            if payment_subject:
                # Only a predication about the payment establishes its force.
                atom = re.match(r'^(?:(?:the|a|qualifying|threshold)\s+)*'+pay+
                                r'(?:\s+(?:the\s+)?threshold)?(?:\s+(?:alone|itself|independently))?\s+'
                                r'(?:(?:does|can|is|may)\s+)?(?P<sign>not\s+|never\s+|cannot\s+)?'
                                r'(?:independently\s+)?(?:authoriz\w*|sufficient|a qualification|constitut\w*|replace\w*|substitut\w*)\b',obj)
                if not atom: continue
                denied = bool(atom['sign'])
            if denied or denies_alternative:
                relations.add('role_required')
            elif policy and policy['verb'].startswith('require'):
                # Being required makes payment necessary; it need not authorize on its own.
                relations.add('independent' if either_or else 'unresolved')
            elif alternative or authority and re.search(r'\b(?:as authorization|to authorize|sufficient|authorizes?|constitut\w* authorization)\b',obj):
                relations.add('independent')
            else:
                relations.add('unresolved')
    if 'unresolved' in relations or 'independent' in relations and len(relations)>1:
        return 'unresolved'
    return next((mode for mode in ('joint','role_required','independent') if mode in relations),None)


def scoped_payment_denial(text, role_name, entry_name, scope_names):
    """Allow role inference only for an explicit policy denying pay on THIS effect.

    The inferred role is a *necessary* guard operand, never a free-standing
    authorization source. Vague claims, alternate authorities or statements
    about a different effect do not qualify.
    """
    if not entry_name or mentioned(text, role_name):
        return False
    clauses = [v.strip() for v in re.split(r'[;；\n]|(?<=[.!?。])\s+', text) if v.strip()]
    if len(clauses) != 1:
        return False
    clause = clauses[0]
    if not mentioned(clause, entry_name) or not re.search(r'\b(?:policy|rule)\b', clause, re.I):
        return False
    # No inference across competing, conditional or hypothetical policy claims.
    if re.search(r'\b(?:but|however|whereas|unless|except|provided|subject to|'
                 r'unknown|unclear|whether|hypothetically|instead|another|other|either|if)\b', clause, re.I):
        return False
    # A second claimed authorizer in the same sentence must not be silently
    # erased by assuming the observed role is the only legitimate source.
    if re.search(r'\band\b.{0,100}\b(?:authoriz\w*|qualif\w*|approv\w*|permitt\w*|grant\w*)\b',
                 clause, re.I):
        return False
    return payment_policy(clause, role_name, scope_names) == 'role_required'


def role_payments(rows, lookup, text, subject=None, *, derive_role_from_source=False):
    """Find actual alternative operands. Their occurrence proves no business permission.

    `derive_role_from_source` may only be used after independently checking a
    narrowly scoped normative payment exclusion and one stable source role.
    """
    scoped = {}
    for _, path in rows:
        for guard in path['guards']:
            for disj in conjuncts(guard):
                if disj.get('op') not in ('or','||') or len(disj.get('args',())) != 2:
                    continue
                for role, condition in (disj['args'], reversed(disj['args'])):
                    args = role.get('args', ())
                    if role.get('op') != '==' or not any(t.get('kind')=='actual_sender' for t in args):
                        continue
                    cell = next((t for t in args if t.get('kind')=='storage' and not keys(t)), None)
                    if not cell or (cell != subject if subject is not None else
                                    not derive_role_from_source and not positive_role_reference(
                                        text, lookup.nodes[cell['root']].get('name'))):
                        continue
                    pay = condition.get('args', ())
                    if len(pay)!=2 or condition.get('op') not in ('>=','>','<=','<'):
                        continue
                    value, threshold = pay if condition['op'] in ('>=','>') else reversed(pay)
                    if value.get('kind')=='transaction_value' and threshold.get('kind') in ('literal','storage'):
                        scoped[key([role,condition,cell])] = (role,condition,cell)
    return list(scoped.values())


def source_requirement(inv, q, explanation, rows):
    entry=inv.f.operations[inv.root(q)]
    lookup=inv.f.lookup(inv.root(q))
    declaration=lookup.nodes.get(entry['source'].get('ast_id'),{})
    text=str(explanation.get('text') or explanation.get('basis') or '')
    signature={'target':entry['target'],'operation':inv.root(q),'declaration':declaration.get('id'),
               'frame':'before_effect','path_sources':[pid for pid,_ in rows]}
    clause=creation_source(text,entry,inv.f.operations)
    if clause and declaration.get('nodeType')=='FunctionDefinition' and function_kind(declaration)!='constructor':
        return dict(signature,kind='creation_only_source_policy',clause=clause,frame='runtime entry')
    # Use the already source-derived role of each ordered key, never a function name.
    grants={}
    if re.search(r'\b(?:allowance|grant|approval|spender)\b|额度|受托|授权额度',text,re.I):
        for _,p in rows:
            for write in p['writes']:
                cell=write['path']
                role=key_role(cell,lookup)
                if role and role['kind']=='authorization_quantity':
                    idx=keys(cell)
                    if len(idx)==2:
                        h=role['holder_key']
                        grants[key(cell)]={'cell':cell,'issuer':idx[h],'spender':idx[1-h],'quantity':write['value']}
    own=re.search(r"\b(?:own|self|issuer|holder.s|on behalf of|someone else.s|another holder.s)\b|本人|持有人",text,re.I)
    additional_policy=any(positive_role_reference(text,n['name']) for n in lookup.decls.values()
                          if n.get('stateVariable') and n.get('name') and
                          (n.get('typeDescriptions',{}).get('typeString') or '').startswith('address'))
    if grants and own and len(grants)==1 and not additional_policy:
        return dict(signature,kind='source_grant_issuer',grant=next(iter(grants.values())))
    # A named source check identifies its precise relation only if every
    # committing branch agrees. Do not promote a branch-specific atom.
    if not rows:
        return None
    # Both interfaces use the same normative relation and the same source operands.
    typed = explanation.get('explicit_policy_kind') == 'current_authority_required'
    entry_name = entry['function'].split('(')[0]
    names = {entry_name} | {lookup.nodes.get(w['path']['root'],{}).get('name')
                            for _, path in rows for w in path['writes']}
    candidates = role_payments(rows, lookup, text, explanation.get('qualified_cell') if typed else None)
    if not candidates and not typed and rows:
        # A legacy issue can locate the exact effect without repeating the
        # source role's identifier. Only derive that role when (a) the policy
        # explicitly excludes payment as authorization for THIS entry, and
        # (b) every committing path has the same unique role-or-pay guard.
        # The derived role is a necessary authorization prerequisite, not a
        # proof that this role alone is sufficient for any other effect.
        inferred = role_payments(rows, lookup, text, derive_role_from_source=True)
        if len(inferred) == 1:
            role, payment, cell = inferred[0]
            role_name = lookup.nodes[cell['root']].get('name')
            same_in_all_paths = all(
                len(row_candidates := role_payments([(pid, path)], lookup, text,
                    derive_role_from_source=True)) == 1 and key(row_candidates[0]) == key(inferred[0])
                for pid, path in rows)
            if same_in_all_paths and scoped_payment_denial(text, role_name, entry_name, names):
                candidates = inferred
    if candidates:
        role, payment, cell = candidates[0]
        sign = (explanation.get('payment_policy') or 'role_required') if typed else payment_policy(text, lookup.nodes[cell['root']]['name'],names)
        if sign in ('independent','joint','role_required') and len(candidates) == 1:
            return dict(signature,kind='source_role_payment_policy',role=role,payment=payment,subject=cell,
                        payment_relation=sign, permits_payment=sign=='independent')
        # Describing the actual guard or naming its role is insufficient to
        # select one of its authorization branches as the governing rule.
        return dict(signature,kind='unresolved_role_payment_policy')
    if typed and explanation.get('payment_policy') in ('unresolved','independent','joint'):
        return dict(signature,kind='unresolved_role_payment_policy')
    paths=[]
    for _,p in rows:
        atoms={}
        for guard in p['guards']:
            for term in conjuncts(guard):
                leaf=boolean_leaf(term)
                if not leaf:continue
                cell,truth=leaf
                if keys(cell) and value_type(cell,lookup)=='bool' and mentioned(text,lookup.nodes[cell['root']].get('name')):
                    atoms[key([cell,truth])]=(cell,truth)
        paths.append(atoms)
    if paths[0] and all(set(p)==set(paths[0]) for p in paths):
        atoms=[]
        for c,observed in paths[0].values():
            name=lookup.nodes[c['root']].get('name')
            truths=stated_boolean(text,name)
            if len(truths)>1:return None
            observed_normal=(explanation.get('meaning')=='normal_authorization' and
                re.search(r'\b(?:own|self|msg\.sender.s)\b',text,re.I) and
                re.search(r'\b(?:checks?|requires?|subject to)\b',text,re.I))
            if not truths and not observed_normal:return None
            truth=next(iter(truths)) if truths else observed
            atoms.append({'cell':c,'permitted_truth':truth,'observed_guard_truth':observed,
                'basis':'explicit_source_bound_condition' if truths else 'stated_normal_use_subject_to_actual_check'})
        return dict(signature,kind='source_guarded_eligibility',atoms=atoms)
    return None


def compile_requirement(requirement,explanation,lookup):
    kind=requirement['kind']
    subject=None
    if kind=='source_role_payment_policy':
        subject=requirement['subject']
        mode=requirement['payment_relation']
        predicate=requirement['role'] if mode=='role_required' else op(
            'and' if mode=='joint' else 'or', requirement['role'], requirement['payment'])
    elif kind=='source_grant_issuer':
        subject=requirement['grant']['issuer']
        predicate=op('==',{'kind':'actual_sender'},subject)
    elif kind=='source_guarded_eligibility':
        terms=[a['cell'] if a['permitted_truth'] else op('!',a['cell']) for a in requirement['atoms']]
        predicate=terms[0] if len(terms)==1 else op('and',*terms)
        if len(terms)==1:subject=requirement['atoms'][0]['cell']
    else:
        predicate=lit(False)
    return {'predicate':predicate,'subject':subject,'kind':kind,'property_family':'use',
            'normal_alternatives':[],'source_bound_alternatives':[],'business_basis':explanation,
            'necessary_only':kind=='source_role_payment_policy' and requirement['payment_relation']!='independent',
            'acquisition_uses':[],'binding':{'declaration':requirement['declaration'],'frame':requirement['frame'],
            'source':lookup.anchor(lookup.nodes[requirement['declaration']])},'source_requirement':requirement}


def compare_requirement(required,compiled,entry_id,declaration,target):
    """Check independent source facts against the expression consumed by M4."""
    p=compiled.get('predicate') or {}
    binding=compiled.get('binding') or {}
    scope_ok=(entry_id==required['operation'] and target==required['target'] and
              binding.get('declaration')==declaration==required['declaration'] and binding.get('frame')==required['frame'])
    if required['kind']=='source_role_payment_policy':
        mode=required['payment_relation']
        if mode=='role_required':
            actual,wanted=key(p),key(required['role'])
        else:
            actual=[p.get('op'),sorted(key(t) for t in p.get('args',[]))]
            wanted=[{'joint':'and','independent':'or'}[mode],sorted(key(required[t]) for t in ('role','payment'))]
        equal=actual==wanted and compiled.get('necessary_only')==(mode!='independent')
    elif required['kind']=='source_guarded_eligibility':
        leaves=[boolean_leaf(t) for t in conjuncts(p)]
        actual=sorted(key([c,b]) for leaf in leaves if leaf for c,b in [leaf])
        wanted=sorted(key([a['cell'],a['permitted_truth']]) for a in required['atoms'])
        equal=len(actual)==len(leaves) and actual==wanted
    elif required['kind']=='source_grant_issuer':
        actual=sorted(key(t) for t in p.get('args',[]))
        wanted=sorted(key(t) for t in ({'kind':'actual_sender'},required['grant']['issuer']))
        equal=p.get('op')=='==' and actual==wanted
    else:
        actual=[p.get('kind'),p.get('value'),compiled.get('acquisition_uses')]
        wanted=['literal',False,[]]
        equal=actual==wanted and type(p.get('value')) is bool
    return {'matches':scope_ok and equal,'scope_matches':scope_ok,'source':wanted,'compiled':actual,
            'frame':binding.get('frame'),'operator':p.get('op',p.get('kind'))}


def audit_authorization(f,oid,compiled):
    """Recheck at consumption, including each independently scoped alternative."""
    if not isinstance(compiled,dict):return []
    alternatives=compiled.get('competing_interpretations')
    if alternatives:
        expected=[p['predicate'] for p in alternatives]
        actual=compiled.get('predicate',{})
        results=[r for p in alternatives for r in audit_authorization(f,oid,p)]
        results.append({'matches':actual.get('op')=='or' and
                        sorted(map(key,actual.get('args',[])))==sorted(map(key,expected)),
                        'scope':'surviving_source_interpretations'})
        return results
    requirement=compiled.get('source_requirement')
    if not requirement:return []
    op_info=f.operations[oid]
    return [compare_requirement(requirement,compiled,oid,op_info['source'].get('ast_id'),op_info['target'])]


def source_excludes_violation(f,oid,compiled):
    """A local proof over all the located committing paths, for this policy only."""
    required=compiled.get('source_requirement') or {}
    # A source-scoped before/after check for a stage flag: once it is true,
    # setting that identical cell to true cannot commit the prohibited change.
    # Independent sibling effects have separate policy/coverage consumers.
    scoped=compiled.get('effect_write')
    if compiled.get('kind')=='scope_bound_initialization_stage' and scoped and not compiled.get('competing_interpretations'):
        cell=scoped['cell']
        if key(cell)!=key(compiled.get('subject')) or compiled.get('predicate')!=op('!',cell):return None
        path=next((p for pid,p in f.operation_paths(oid,True) if pid==scoped['path']),None)
        if not path or path.get('issues') or path.get('evaluation_gaps') or path.get('sensitive_effects'):return None
        writes=[w for w in path['writes'] if w['path'].get('root')==cell['root']]
        if not writes or any(w['path']!=cell for w in writes) or writes[-1]['value']!=lit(True):return None
        return {'basis':'already_set_stage_flag_has_no_further_net_change','source_identity':f.identity,'operation':oid,
                'target':f.operations[oid]['target'],'paths':[scoped['path']],'scope':'only the bound stage flag',
                'other_policies_or_effects_closed':False}
    if compiled.get('competing_interpretations') or required.get('kind') not in ('source_grant_issuer','source_guarded_eligibility'):
        return None
    paths=list(f.operation_paths(oid))
    if not paths or f.operations[oid].get('gaps') or any(
            p['flow'] not in ('normal','returned','reverted') or p.get('issues') or p.get('evaluation_gaps')
            for _,p in paths):return None
    commits=[(pid,p) for pid,p in paths if p['flow'] in ('normal','returned')]
    if not commits or set(required['path_sources'])!={pid for pid,_ in commits}:return None
    if required['kind']=='source_grant_issuer':
        issuer=required['grant']['issuer']
        if issuer!={'kind':'actual_sender'}:return None
        cell=required['grant']['cell']
        # Other state updates/effects require independent policies.
        if any(p.get('sensitive_effects') or any(key(w['path'])!=key(cell) for w in p['writes']) for _,p in commits):
            return None
        reason='exact_caller_owns_written_grant_key'
    else:
        needed={key([a['cell'],a['permitted_truth']]) for a in required['atoms']}
        for _,p in commits:
            actual=set()
            for g in p['guards']:
                for t in conjuncts(g):
                    leaf=boolean_leaf(t)
                    if leaf:actual.add(key(list(leaf)))
            if not needed<=actual:return None
        reason='authorized_boolean_condition_is_necessary_on_each_committing_path'
    return {'basis':reason,'source_identity':f.identity,'operation':oid,'target':required['target'],
            'paths':[pid for pid,_ in commits],'scope':'only this use of this source-verified policy',
            'other_policies_or_effects_closed':False}

```

## source/src/pr_next_joint/investigation/prestate.py

SHA-256 `d985f5498edb16ca90e48d4f06b90eb5e07538b8d91f971666a437c01d832239`

```python
"""Narrow initial-state invariants. Never equate a deployment choice with a current value."""
from functools import lru_cache
from pr_next_joint.frontend.path_ir import walk,key
from pr_next_joint.frontend.storage import selectors


def literal(node):
    if not isinstance(node,dict):return None
    if node.get('nodeType')=='FunctionCall' and node.get('kind')=='typeConversion' and len(node.get('arguments',[]))==1:
        type_name=node.get('expression',{}).get('typeName',{})
        target=type_name.get('name') if isinstance(type_name,dict) else type_name if isinstance(type_name,str) else None
        value=literal(node['arguments'][0])
        if type(value)is not int:return None
        import re
        numeric=re.fullmatch(r'uint(\d*)',target or '')
        width=160 if target in ('address','address payable') else int(numeric[1] or 256) if numeric else None
        return value if width and 0<=value<2**width else None
    if node.get('nodeType')!='Literal':return None
    typ=node.get('kind'); v=str(node.get('value',''))
    if typ in ('bool','boolean') and v in ('true','false'):return v=='true'
    if typ in ('number','hexNumber') and not node.get('subdenomination'):
        try:return int(v.replace('_',''),0)
        except ValueError:return None
    return None


def _legacy_state_facts(lookup):
    if hasattr(lookup,'_relational_initial'):return lookup._relational_initial
    bases=lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
    declarations=[n for b in bases for n in lookup.nodes[b].get('nodes',[])]
    # Assembly, delegate execution or a storage-reference alias can defeat AST write exclusion.
    functions=[n for n in declarations if n.get('nodeType') in ('FunctionDefinition','ModifierDefinition')]
    opaque=any(n.get('nodeType') in ('InlineAssembly','YulBlock') or n.get('memberName') in ('delegatecall','callcode')
         or n.get('nodeType')=='VariableDeclaration' and n.get('storageLocation')=='storage' for fn in functions for n in walk(fn))
    table={}
    for var in declarations:
        typ=var.get('typeDescriptions',{}).get('typeString','')
        if not var.get('stateVariable') or not (typ=='bool' or typ.startswith('uint') or typ in ('address','address payable')):continue
        vid=var['id']; row={'declaration':vid,'name':var['name'],'type':typ,'declaration_source':lookup.anchor(var),
            'origin':'conditional_symbolic','encoded':False}
        table[vid]=row; assigns=[]; runtime=False
        for fn in functions:
            is_ctor=fn.get('kind')=='constructor' or fn.get('isConstructor')
            body=fn.get('body') or {}
            for n in walk(body):
                if n.get('nodeType') not in ('Assignment','UnaryOperation'):continue
                lhs=n.get('leftHandSide') or n.get('subExpression') or {}
                if n.get('nodeType')=='UnaryOperation' and n.get('operator') not in ('++','--','delete'):continue
                if not any(x.get('referencedDeclaration')==vid for x in walk(lhs)):continue
                if is_ctor:assigns.append((fn,n))
                else:runtime=True
        if opaque and not var.get('constant'):row['limit']='indirect storage writes not excluded';continue
        if runtime:
            row['origin']='constructor_choice_with_possible_later_write' if assigns else 'conditional_state_with_source_writer'
            row['constructor_sources']=[lookup.anchor(n) for _,n in assigns]
            continue
        v=literal(var.get('value'))
        if var.get('value') is None:v=False if typ=='bool' else 0
        if not assigns:
            if v is not None:row.update(origin='fixed_declared_initializer' if var.get('value') is not None else 'fixed_type_default',value=v,encoded=True)
            continue
        row['origin']='constructor_configuration';row['writes']=[lookup.anchor(n) for _,n in assigns]
        if len(assigns)!=1:continue
        ctor,assignment=assigns[0]
        direct={st.get('expression',{}).get('id') for st in (ctor.get('body') or {}).get('statements',[]) if st.get('nodeType')=='ExpressionStatement'}
        if assignment['id'] not in direct or assignment.get('operator')!='=' or ctor.get('modifiers'):continue
        rhs=assignment.get('rightHandSide') or {}; v=literal(rhs)
        if v is not None:row.update(origin='fixed_constructor_literal',value=v,encoded=True)
        elif rhs.get('memberName')=='sender' and rhs.get('expression',{}).get('name')=='msg':
            row.update(origin='fixed_deployer_address',nonzero=True,encoded=True)
    lookup._relational_initial=table
    return table


def state_facts(lookup, selected_domain=None):
    from .initial_state import domain,initial_for_lookup,CAPABILITY,DEPLOYMENT
    from .state_encoding import _initial_term
    from pr_next_joint.verification.sequence import read
    selected_domain=selected_domain or domain(lookup)
    if selected_domain not in (CAPABILITY,DEPLOYMENT):return _legacy_state_facts(lookup)
    model=initial_for_lookup(lookup)
    if model is None:return {}
    cache=lookup.__dict__.setdefault('_domain_state_facts',{})
    token=(selected_domain,model['identity'])
    if token in cache:return cache[token]
    from .initial_state import family
    context={**model,'_lookup':lookup,'_amount_families':{family(r['cell']) for r in model['candidate_amount_leaves']}}
    table={}
    clean=[p for p in model['constructor_paths'] if p['flow'] in ('normal','returned') and not p.get('issues') and not p.get('evaluation_gaps')]
    for rid,row in model['declarations'].items():
        typ=row['type'];value={'declaration':rid,'name':row['name'],'type':typ,'declaration_source':row['source'],
            'origin':'constructor_configuration' if row['constructor_writes'] or row['explicit_initializer'] else
                     'abstract_initial_scalar' if selected_domain==CAPABILITY and (typ.startswith(('uint','int')) or typ in ('address','address payable')) else 'fixed_type_default',
            'encoded':False,'analysis_domain':selected_domain,'initial_model_identity':model['identity'],
            'runtime_assignment_sites':row['runtime_sites']}
        table[rid]=value
        if row['runtime_sites'] or model['runtime_writers']['opaque_storage_writes']:
            value['origin']='constructor_choice_with_possible_later_write';continue
        if not clean or any(p.get('issues') or p.get('evaluation_gaps') for p in model['constructor_paths']):continue
        cell={'kind':'storage','root':rid,'segments':[]}
        try:values=[_initial_term(read(cell,p['writes'],lookup),context,selected_domain) for p in clean]
        except (ValueError,KeyError,TypeError):continue
        if values and all(v==values[0] for v in values):
            v=values[0]
            if v.get('kind')=='literal' and type(v.get('value')) in (bool,int):value.update(value=v['value'],encoded=True,
                origin='fixed_constructor_or_declaration' if row['constructor_writes'] else 'fixed_type_default')
            elif v.get('initial_identity')=='deployment_caller':value.update(nonzero=True,encoded=True,origin='fixed_deployer_address')
    cache[token]=table
    return table


def encode_state(e,details=None):
    from .initial_state import domain,CAPABILITY,DEPLOYMENT
    if domain(e.lookup) in (CAPABILITY,DEPLOYMENT):
        from .state_encoding import encode
        return encode(e,details)
    items=[];constraints=[]
    for vid,v in state_facts(e.lookup).items():
        if not v['encoded']:continue
        cell=e.expr({'kind':'storage','root':vid,'segments':[]})
        constraints.append(cell!=0 if v.get('nonzero') else cell==v['value'])
        items.append(v)
    return constraints,items


def prestate_receipt(details,initial):
    d=details or {}
    if isinstance(initial,dict):
        return dict(initial,executed_prefix=d.get('prefix',[]),encoded_case=d.get('encoded_case',[]),
            encoded_request_bindings=d.get('encoded_request_bindings',d.get('request_context',{}).get('bindings',[])))
    return {'analysis_domain':'ac_checked_prestate_r1','analysis':'conditional_symbolic_with_checked_fixed_initializers','encoded_invariant_declarations':initial,
            'executed_prefix':d.get('prefix',[]),'encoded_case':d.get('encoded_case',[]),
            'encoded_request_bindings':d.get('encoded_request_bindings',d.get('request_context',{}).get('bindings',[])),
            'explicit_constructor_prefix_executed':False,'author_run_initial_state_verified':False}


def impossible_role(inv,oid):
    """P exclusion only if every clean committing path needs caller == fixed zero."""
    if not inv.backend.complete(oid):return False
    original=inv.backend.paths(oid)
    if not original:return False
    fixed=state_facts(inv.f.lookup(oid))
    from .request_scope import positive_caller_gate
    def zero(g):
        if g.get('op') in ('and','&&'):return any(zero(x) for x in g.get('args',[]))
        return positive_caller_gate(g,inv.f.lookup(oid)) and g.get('op') in ('==','!') and any(
            fixed.get(c['root'],{}).get('encoded') and fixed[c['root']].get('value')==0 for c in selectors(g))
    def value(x):
        if x.get('kind')=='literal':
            a=x.get('value')
            if isinstance(a,bool) or isinstance(a,int):return a
            if str(a).lower() in ('true','false'):return str(a).lower()=='true'
            try:return int(a,0)
            except (ValueError,TypeError):return None
        if x.get('kind')=='storage' and not x.get('segments'):return fixed.get(x.get('root'),{}).get('value')
        op=x.get('op');args=[value(v) for v in x.get('args',[])]
        if op=='!' and len(args)==1 and args[0] is not None:return not args[0]
        if len(args)!=2:return None
        a,b=args
        if op in ('and','&&') and False in args:return False
        if op in ('or','||') and True in args:return True
        if a is None or b is None:return None
        if op=='==':return a==b
        if op=='!=':return a!=b
        if op=='>=':return a>=b
        if op=='<=':return a<=b
        if op=='<':return a<b
        if op=='>':return a>b
        return None
    return all(any(zero(g) or value(g) is False for g in p['guards']) for pid,p in original)


```

## source/src/pr_next_joint/investigation/program.py

SHA-256 `552073da5a81930a326cf0da7f01d48dfc823ea400343e5dc700e5804911c96c`

```python
"""M1: original compiler identities, paths and structural edges only.

There is deliberately no import of an old detector, policy projection,
asset discovery, LLM consumer or report merger in this module.
"""
import copy
import hashlib
import time
from pathlib import Path
from pr_next_joint.core import digest, require
from pr_next_joint.frontend.inventory import target_inventory
from pr_next_joint.frontend.source_entry_identity import entry_functions
from pr_next_joint.frontend.program_paths import MechanismPaths
from pr_next_joint.frontend.path_ir import walk, key, clean, ExpressionLimit
from pr_next_joint.frontend.storage import selectors
from pr_next_joint.graph.state_relations import expand_write
from .contracts import ident


class Facts:
    def __init__(self, bundle, native, sources, options, selected=None, description=None):
        self.program_clock_origin = time.monotonic()
        require(all(bundle[k] == native[k] for k in ('program_id', 'build_id')), 'input_identity_mismatch')
        require(bundle.get('native_ir', {}).get('sha256') == digest(native), 'native_digest_mismatch')
        self.bundle, self.native, self.options = bundle, native, options
        self.lookups, self.operations, self.paths, self.writes, self.effects, self.terms = {}, {}, {}, {}, {}, {}
        self.references, self.gaps = {}, []
        inventory = target_inventory(bundle)
        available = {x['file'] + ':' + x['contract'] for x in inventory if x['selected']}
        self.selected = sorted(set(selected) if selected is not None else available)
        require(bool(self.selected) and set(self.selected) <= available, 'invalid_selected_targets')
        source_by_name = {s['file']: s for s in sources}
        for file, ast in bundle['ast_sources'].items():
            require(file in source_by_name, 'source_missing:' + file)
            content = source_by_name[file]['content'].encode('utf-8')
            require(hashlib.sha256(content).hexdigest() == source_by_name[file]['sha256'], 'source_hash_mismatch')
        for contract in bundle['contracts']:
            target = contract['file'] + ':' + contract['name']
            if target not in self.selected:
                continue
            lookup = MechanismPaths(bundle, contract, options.max_paths)
            lookup.analysis_scope = options.scope
            self.lookups[target] = lookup
            bases = lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']])
            for n in lookup.nodes.values():
                # All references retain the actual compiler node and file span.
                if n.get('nodeType') in ('VariableDeclaration', 'FunctionDefinition', 'Assignment', 'UnaryOperation',
                                         'FunctionCall', 'BinaryOperation', 'IndexAccess', 'MemberAccess', 'IfStatement'):
                    ref = ident('r', [target, n['id']])
                    self.references[ref] = {'target': target, 'ast_id': n['id'], 'kind': n['nodeType'],
                                            'name': n.get('name', n.get('memberName')), 'source': lookup.anchor(n)}
            for entry in entry_functions(lookup):
                fn = entry['signature']; oid = ident('op', [target, fn])
                body = lookup.function(fn)
                operation = {'id': oid, 'target': target, 'function': fn,
                             'source': lookup.anchor(body.get('generated_getter', body)),
                             'parameters': [], 'paths': [], 'gaps': [], 'generated_getter': bool(body.get('generated_getter'))}
                params = body.get('parameters', {}).get('parameters', [])
                for n in params:
                    operation['parameters'].append({'ref': ident('r', [target, n['id']]), 'name': n['name'],
                        'term': self.term({'kind': 'parameter', 'id': n['id'], 'type': n['typeDescriptions']['typeString']}, target)})
                self.operations[oid] = operation
                try:
                    if time.monotonic()-self.program_clock_origin >= options.seconds:
                        self.gap(oid, 'path_extraction', 'program_time_before_entry')
                        continue
                    paths = lookup.run(fn)
                except ExpressionLimit as error:
                    self.gap(oid,'source_expression_limit',str(error))
                    continue
                except (TypeError, AttributeError):
                    raise
                except Exception as error:
                    self.gap(oid, 'path_extraction', type(error).__name__ + ':' + str(error)); continue
                for index, path in enumerate(paths):
                    pid = ident('path', [oid, index]); path = copy.deepcopy(path)
                    try:
                        path['writes'] = [item for w in path['writes'] for item in expand_write(w, lookup)]
                        # Validate each executable operand independently before publishing
                        # any references. A bounded path cannot poison a sibling path.
                        for expr in [*path['guards'], *(w['path'] for w in path['writes']),
                                     *(w['value'] for w in path['writes']), *path.get('evaluated_terms', []),
                                     path.get('return_value'), *path.get('sensitive_effects', [])]:
                            if expr is not None: clean(expr)
                    except ExpressionLimit as error:
                        self.gap(oid,'source_expression_limit',{'path':pid,'reason':str(error)})
                        continue
                    except (TypeError, AttributeError):
                        raise
                    except Exception as error:
                        path.setdefault('issues', []).append({'reason': 'write_expansion:' + str(error)})
                    self.paths[pid] = {'operation': oid, 'index': index, 'raw': path}
                    card = {'id': pid, 'flow': path['flow'], 'guards': [], 'writes': [], 'effects': [],
                            'issues': copy.deepcopy(path.get('issues', [])), 'evaluation_gaps': path.get('evaluation_gaps', [])}
                    for g in path['guards']:
                        card['guards'].append(self.term(g, target))
                    for wi, w in enumerate(path['writes']):
                        wid = ident('w', [pid, wi]); self.writes[wid] = {'operation': oid, 'path': pid, 'raw': w}
                        card['writes'].append({'id': wid, 'selector': self.term(w['path'], target),
                                              'value': self.term(w['value'], target), 'source': w['source']})
                    for ei, e in enumerate(path.get('sensitive_effects', [])):
                        eid = ident('fx', [pid, ei]); self.effects[eid] = {'operation': oid, 'path': pid, 'raw': e}
                        row = {'id': eid, 'kind': e['kind'], 'source': e['source']}
                        for field in ('recipient', 'amount', 'success'):
                            if e.get(field) is not None: row[field] = self.term(e[field], target)
                        card['effects'].append(row)
                    for value in [path.get('evaluated_terms', []), path.get('return_value')]:
                        for n in walk(value):
                            if n.get('kind'): self.term(n, target)
                    operation['paths'].append(card)
                    if card['issues'] or card['evaluation_gaps']:
                        self.gap(oid, 'program_path', {'path': pid, 'issues': card['issues'], 'evaluation_gaps': card['evaluation_gaps']})
        for target in self.selected:
            self.lookups[target]._investigation_facts=self
            self.term({'kind': 'actual_sender'}, target)
            self.term({'kind': 'transaction_value', 'type': 'uint256'}, target)
        edges = []
        reads={o['id']:{s['root'] for p in o['paths'] for s in selectors(self.paths[p['id']]['raw'])}
               for o in self.operations.values()}
        writes={}
        for w in self.writes.values():
            writes.setdefault(w['operation'],set()).add(w['raw']['path']['root'])
        for a in self.operations.values():
            a_roots=writes.get(a['id'],set())
            if not a_roots:continue
            for b in self.operations.values():
                if a['target'] != b['target']: continue
                b_roots=reads[b['id']]
                roots = sorted(a_roots & b_roots)
                if roots:
                    edges.append({'from': a['id'], 'to': b['id'], 'roots': roots, 'kind': 'may_write_read',
                                  'meaning': 'structural_frontier_not_policy'})
        package = Path(__file__).resolve().parents[1]
        implementation = {p.relative_to(package).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(package.rglob('*.py'))}
        self.context = {'schema': 'scrv-facts-r2-1', 'identity': {k: bundle[k] for k in ('program_id', 'build_id')},
                        'implementation_sha256': digest(implementation), 'finite_options': options.record(),
                        'scope': options.scope, 'sources': sources, 'description': description,
                        'operations': list(self.operations.values()), 'references': self.references,
                        'terms': self.terms, 'frontier': edges, 'program_gaps': self.gaps}
        from .initial_state import model, domain
        self.context['state_analysis']={target:{'analysis_domain':domain(lookup),'initial_model_identity':model(self,target)['identity'],
            'candidate_amount_leaves':model(self,target)['candidate_amount_leaves']} for target,lookup in self.lookups.items()}
        from .summary import get_summaries
        self.summaries=get_summaries(self)
        self.link_unexpanded_effects()
        from .call_summary import CallSummaries
        self.call_summaries = CallSummaries(self)
        self.context['call_summary_identity'] = self.call_summaries.identity
        self.context['effect_summary_identity']=self.summaries.identity
        from .candidates import source_candidates
        self.source_candidates=source_candidates(self)
        self.context['source_candidates']=self.source_candidates
        self.identity = digest(self.context)

    def link_unexpanded_effects(self):
        """Track unavailable storage dependencies without discarding unrelated readers."""
        limited=[g for g in self.gaps if g['kind']=='source_expression_limit']
        for gap in limited:
            entry=self.operations[gap['operation']];lk=self.lookup(entry['id'])
            body=lk.function(entry['function']);pending=[body];seen=set();writes=set();opaque=False
            while pending:
                fn=pending.pop()
                if fn.get('id') in seen:continue
                seen.add(fn.get('id'))
                for n in walk([fn.get('body'),fn.get('modifiers',[])]):
                    if n.get('nodeType') in ('InlineAssembly','YulFunctionCall'):opaque=True
                    if n.get('nodeType') in ('FunctionCall','ModifierInvocation'):
                        expr=n.get('expression',n.get('modifierName',{}))
                        callee=lk.nodes.get(expr.get('referencedDeclaration'),{})
                        if callee.get('body'):pending.append(callee)
                        if expr.get('memberName')=='delegatecall':opaque=True
                    if n.get('nodeType') not in ('Assignment','UnaryOperation'):continue
                    lhs=n.get('leftHandSide',n.get('subExpression',{}))
                    writes.update(v.get('referencedDeclaration') for v in walk(lhs)
                                  if lk.nodes.get(v.get('referencedDeclaration'),{}).get('stateVariable'))
            if body.get('kind')=='constructor':
                raise ExpressionLimit('shared_or_entire_entry_source_expression_unavailable')
            for other in self.operations.values():
                if other['id']==entry['id'] or other['target']!=entry['target'] or other['generated_getter']:continue
                local=gap.get('reason')
                if isinstance(local,dict) and 'declaration' in local:
                    writes={local['declaration']};opaque=False
                reads={s['root'] for card in other['paths'] for s in selectors(self.paths[card['id']]['raw'])}
                if opaque or reads & writes:
                    self.gap(other['id'],'dependent_source_expression_limit',
                             {'source_operation':entry['id'],'scope':'unknown_storage' if opaque else 'shared_declaration'})
        for target in {self.operations[g['operation']]['target'] for g in limited}:
            def usable_scope(operation):
                if operation['target']!=target or operation['generated_getter']:return False
                gaps=[g for g in operation['gaps'] if g['kind']=='source_expression_limit']
                if any(g['kind']=='dependent_source_expression_limit' for g in operation['gaps']):return False
                for card in operation['paths']:
                    here=[g['reason'] for g in gaps if not isinstance(g['reason'],dict) or g['reason'].get('path')==card['id']]
                    if not here:return True
                    # A final-value failure can be isolated from a distinct write in the same path.
                    if all(isinstance(x,dict) and 'declaration' in x for x in here):
                        affected={x['declaration'] for x in here}
                        if any(self.writes[w['id']]['raw']['path']['root'] not in affected for w in card['writes']):return True
                return False
            if not any(usable_scope(op) for op in self.operations.values()):
                raise ExpressionLimit('shared_or_entire_entry_source_expression_unavailable')
    def term(self, value, target):
        ref = ident('e', [target, value])
        self.terms[ref] = {'target': target, 'expression': copy.deepcopy(value)}
        for n in walk(value):
            if n is not value and n.get('kind'):
                nr = ident('e', [target, n]); self.terms[nr] = {'target': target, 'expression': copy.deepcopy(n)}
        return ref

    def gap(self, operation, kind, reason):
        row = {'operation': operation, 'kind': kind, 'reason': reason}
        self.gaps.append(row); self.operations[operation]['gaps'].append(row)

    def operation_paths(self, oid, complete_only=False):
        for card in self.operations[oid]['paths']:
            item = self.paths[card['id']]
            p = item['raw']
            if complete_only and (p['flow'] not in ('normal', 'returned') or p.get('issues') or p.get('evaluation_gaps')):
                continue
            yield card['id'], p

    def lookup(self, oid):
        return self.lookups[self.operations[oid]['target']]

```

## source/src/pr_next_joint/investigation/properties.py

SHA-256 `cdfff0890436cc5b493a8e3b23f72fe1447b6e416f33d9b711dec2c2a08dc0dd`

```python
"""Finite, source-bound questions. Wording guides investigation, never certifies harm."""
import re
from itertools import product

from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, selector_relation, value_type
from .request_scope import claim_entries, holder_effect, linked_controls, unique_cells
from .ledger import MEASURES, bind_positions, movements
from .roles import path_qualification


def words(item):
    return ' '.join(str(item.get(k) or '') for k in ('claim','distinguish','distinguishing_question','observation'))


def interpret(item):
    raw = item.get('observation')
    req = dict(raw) if isinstance(raw,dict) else {}
    text = words(item)
    if re.search(r'\b(?:never check|does not (?:read|check)|bypass(?:es)?|missing (?:the )?control)\b',text,re.I) and re.search(r'freez|frozen|guard|control',text,re.I):
        return {**req,'measure':'missing_control'}
    if req.get('measure') in MEASURES or req.get('measure') in ('denied_qualified','direct_effect','authorization_violation'):
        return req
    if req.get('measure') and req['measure'] not in ('opens','blocks'):
        return req
    if re.search(r'allowance.{0,55}(?:gross|actual debit|less than)|more than (?:the |was )?(?:allowance|approved)|(?:gross|actual) debit.{0,70}(?:allowance|grant)',text,re.I):
        return {**req,'measure':'ledger_grant'}
    if re.search(r'(?:recipient|payee|receiver).{0,55}(?:less|zero|smaller|short)|(?:lower|reduced) (?:recipient )?credit|到账减少',text,re.I):
        return {**req,'measure':'ledger_receipt'}
    if re.search(r'(?:debited|debit|charged).{0,22}(?:more|greater|extra)|greater gross debit',text,re.I):
        return {**req,'measure':'ledger_debit'}
    if req.get('measure'):
        return req
    if item.get('category')=='AC' and re.search(r'(?:qualified|entitled|authorized|rightful|rightfully).{0,65}(?:reject|denied|refus)|wrongful.{0,18}(?:denial|reject)',text,re.I):
        return {**req,'measure':'denied_qualified'}
    if item.get('category') in ('FCR-MINT','FCR-TRANSFER','FCR-DESTROY') and re.search(r'\b(mint|issuance|confiscate|seize|destroy|burn|debit|transfer|issu(?:e|es))\b',text,re.I):
        return {**req,'measure':'direct_effect'}
    if item.get('category') in ('FCR-FREEZE','FCR-PAUSE') and re.search(r'block|revert|pause|freeze',text,re.I):
        return {**req,'measure':'blocks'}
    if item.get('category')=='AC' and re.search(r'(?:install|forge|acquire|grant itself).{0,36}(?:grant|allowance|permission)',text,re.I):
        return {**req,'measure':'holder_grant'}
    return None


def conflicting_measurements(inv,q,proposal):
    """Only explicit factual negations of the same measured positive condition conflict."""
    from .request_scope import observation_applies
    factual={
        'ledger_receipt':r'\b(?:recipient|payee)\b.{0,28}\b(?:always|necessarily)\b.{0,20}\b(?:full|unchanged)',
        'ledger_debit':r'\b(?:gross|actual) debit (?:never increases|is always unchanged)',
        'ledger_grant':r'\b(?:actual|gross) debit (?:never exceeds|is always within) (?:the )?(?:allowance|grant)',
        'denied_qualified':r'\b(?:qualified|authorized) (?:caller|role|manager) (?:is never (?:rejected|denied)|always succeeds)',
    }
    if any(proposal.get(k)!=q['current'].get(k) for k in ('observation','assumptions','next_check','actor','object','phase')):
        return []
    text=proposal.get('claim','')
    return [o['probe'] for row in q.get('observations',[]) if row['measure'] in factual and row['version']==q['version']
            and observation_applies(inv,q,row) and re.search(factual[row['measure']],text,re.I)
            for o in row['outcomes'] if o['predicate_value']]


def source_target(inv,anchor,target):
    return [o for o in inv.catalog.resolve(anchor) if inv.f.operations[o]['target']==target]


def premise_cases(inv, use, item, changed=()):
    """Separate expressly different values of the same declared cell. No free Boolean substitute."""
    lookup = inv.f.lookup(use)
    cells = unique_cells(s for s in inv.graph.request_reads(use) if not keys(s))
    text = words(item)
    axes, gaps = [], []
    for cell in cells:
        name = lookup.nodes.get(cell['root'],{}).get('name')
        if not name:
            continue
        regex=r'(?<![\w$])'+re.escape(name)+r'\s*(?:==|=)\s*(true|false|\d+)\b'
        values=list(dict.fromkeys(v.lower() for v in re.findall(regex,text,re.I)))
        if not values:
            continue
        if len({s['root'] for s in cells if lookup.nodes.get(s['root'],{}).get('name')==name})!=1:
            gaps.append('ambiguous source declaration '+name);continue
        typ=value_type(cell,lookup)
        if any((v in ('true','false')) != (typ=='bool') or typ!='bool' and not typ.startswith('uint') for v in values):
            gaps.append('literal sort unsupported: '+name);continue
        at='after' if any(selector_relation(cell,c)=='same_shape' for c in changed) else 'before'
        axes.append([{'cell':cell,'source_name':name,'value':v=='true' if typ=='bool' else int(v),'frame':at} for v in values])
    fixed=[]
    assumptions=item.get('assumptions',[])
    if isinstance(assumptions,str):assumptions=[assumptions]
    named=unique_cells(inv.graph.request_reads(use))
    for a in assumptions:
        match=re.fullmatch(r'(before|after)\s+([A-Za-z_$][\w$]*(?:\[[\w$.]+\])*)\s*(?:==|=)\s*(\d+|true|false)',str(a).strip(),re.I)
        if not match:continue
        at,name,value=match.groups(); found=[s for s in named if inv.backend._storage_name(use,s)==name]
        if len(found)!=1:gaps.append('unbound scoped premise '+name);continue
        fixed.append({'cell':found[0],'source_name':name,'frame':at.lower(),'value':value.lower()=='true' if value.lower() in ('true','false') else int(value)})
    if len(axes)>3 or len(axes)>1 and any(len(axis)>1 for axis in axes):
        return [],gaps+['multiple alternative clauses cannot be independently cross-multiplied']
    return [fixed+list(c) for c in product(*axes)] if axes else [fixed],gaps


def privileged_paths(inv,oid):
    return [pid for pid,p in inv.backend.paths(oid) if path_qualification(inv.f,oid,p)]


def stage(inv,use):
    facts=inv.f; target=facts.operations[use]['target']
    listed=[]
    for cell in unique_cells(inv.graph.request_reads(use)):
        if keys(cell) or not (value_type(cell,facts.lookup(use)) or '').startswith(('uint','bool')):
            continue
        writers=[]
        for oid in sorted(inv.graph.access[target,cell['root']]['writers']):
            matches=[pid for pid,p in inv.backend.paths(oid) if any(selector_relation(cell,w['path'])=='same_shape' for w in p['writes'])]
            if matches:
                writers.append({'operation':oid,'paths':matches,'role_guarded_paths':privileged_paths(inv,oid)})
        listed.append({'cell':cell,'name':inv.backend._storage_name(use,cell),'runtime_writers':writers})
    return listed


def source_graph_holes(inv,binding,item):
    root=binding['core_operation']; target=inv.f.operations[root]['target']
    claimed=claim_entries(inv,binding,item)
    controls=unique_cells(w['path'] for _,p in inv.backend.paths(root) for w in p['writes'] if value_type(w['path'],inv.f.lookup(root))=='bool')
    if not controls:
        return []
    related=[]
    for oid in sorted(claimed-{root}):
        ops=[(pid,movements(inv.backend,oid,p)) for pid,p in inv.backend.paths(oid)]
        debit=unique_cells(c for pid,m in ops for c in m['-'])
        if not debit:
            continue
        peers=[]
        for other,entry in inv.f.operations.items():
            if entry['target']!=target or other==oid:continue
            linked=linked_controls(inv,root,other)
            if not any(selector_relation(c,l)=='same_shape' for c in controls for l in linked):continue
            for pid,p in inv.backend.paths(other):
                m=movements(inv.backend,other,p)
                if any(selector_relation(a,b)=='same_shape' for a in debit for b in m['-']):
                    peers.append({'operation':other,'path':pid,'controls':linked})
        reads=linked_controls(inv,root,oid)
        related.append({'use':oid,'debit_positions':debit,'control_reads':reads,'control_writers':controls,'peer_controlled_uses':peers})
    return related


def plan_property(inv,binding,item,plan,req):
    """Select finite typed questions with compiler-resolved endpoints, or disclose a local gap."""
    measure=req['measure']; root=binding['core_operation']; target=inv.f.operations[root]['target']
    entries=claim_entries(inv,binding,item); contexts=[]
    if measure in MEASURES:
        uses=[oid for oid in sorted(entries) if holder_effect(inv,oid)]
        if req.get('at'):uses=[o for o in source_target(inv,req['at'],target) if o in entries]
        elif root in uses and bind_positions(inv.backend,root,item)[0]:uses=[root]
        reasons=[]
        for use in uses:
            pos,err=bind_positions(inv.backend,use,item)
            if err:reasons.append(err);continue
            edges=stage(inv,use)
            forced=source_target(inv,req.get('after'),target) if req.get('after') else []
            if req.get('after') and len(forced)!=1:reasons.append('requested_intervention_not_unique');continue
            choices={}
            for edge in edges:
                if req.get('control') and req['control']!=edge['name']:continue
                for w in edge['runtime_writers']:
                    change=w['operation']
                    if forced and change not in forced or not forced and root!=use and change!=root:continue
                    if not w['role_guarded_paths']:continue
                    choices.setdefault(change,[]).append(edge['cell'])
            if not choices:reasons.append('no_source_bound_runtime_privileged_writer');continue
            for change,controls in choices.items():
                ctx=inv._compare_context({'current':item},change,use)
                ctx['observable']={'measure':measure,'ledger':pos,'control_selectors':controls,
                                   'change_paths':privileged_paths(inv,change)}
                cases,gaps=premise_cases(inv,use,item,controls)
                if gaps:reasons+=gaps;continue
                ctx['premise_cases']=cases
                # An address alias is admitted only for two actual source parameter names.
                params=inv.f.lookup(use).function(inv.f.operations[use]['function']).get('parameters',{}).get('parameters',[])
                addr={p['name']:{'kind':'parameter','id':p['id'],'type':p['typeDescriptions']['typeString']} for p in params if p['typeDescriptions']['typeString'] in ('address','address payable')}
                ctx['request_aliases']=[]
                for a,op,b in re.findall(r'\b(\w+)\s*(==|!=)\s*(\w+)\b',str(item.get('assumptions',[]))):
                    if a in addr and b in addr:ctx['request_aliases'].append([addr[a],addr[b],op])
                contexts.append((change,use,ctx))
        reason=','.join(dict.fromkeys(reasons)) or 'more_than_one_applicable_request_or_intervention'
    elif measure=='missing_control':
        rows=source_graph_holes(inv,binding,item)
        relevant=[r for r in rows if r['peer_controlled_uses'] and not r['control_reads']]
        if relevant:
            contexts=[(root,relevant[0]['use'],{'observable':{'measure':measure,'alternatives':relevant},'operation':root,
                      'checked_uses':[r['use'] for r in relevant],'frame_type':'committed_intervention_then_actual_alternative'})]
        reason='no_same_target_same_right_comparator_or_unresolved_control'
    else:
        ctx=inv._compare_context({'current':item},root,root)
        ctx.update({'observable':{'measure':measure,'claim':item.get('claim',''),'category':item.get('category')},
                    'operation':root,'stage':stage(inv,root),'frame_type':'single_original_entry'})
        if req.get('authorization'):ctx['observable']['authorization']=req['authorization']
        if measure=='direct_effect' and ctx.get('bindings'):
            ctx['exploratory_request_bindings_not_the_claim']=ctx.pop('bindings')
        params=inv.f.lookup(root).function(inv.f.operations[root]['function']).get('parameters',{}).get('parameters',[])
        addr={p['name']:{'kind':'parameter','id':p['id'],'type':p['typeDescriptions']['typeString']} for p in params if p['typeDescriptions']['typeString'] in ('address','address payable')}
        ctx['request_aliases']=[[addr[a],addr[b],op] for a,op,b in re.findall(r'\b(\w+)\s*(==|!=)\s*(\w+)\b',str(item.get('assumptions',[]))) if a in addr and b in addr]
        contexts=[(root,root,ctx)]
        if measure=='direct_effect':
            contexts[0][2]['privileged_paths']=privileged_paths(inv,root)
        reason='unresolved_direct_property'
    pick=None
    if len(contexts)==1:
        change,use,ctx=contexts[0]
        pick={'action':'compare','change':change,'observe':use,'measure':measure,'status':'source_bound',
              'expectations':{},'context':ctx,'scope':{'target':target,'finding_root':root,'use':use,'intervention':change,
                  'measure':measure,'controls':ctx['observable'].get('control_selectors',[]),'objects':[ctx['observable']['ledger'][k] for k in ('debit','credit')] if 'ledger' in ctx['observable'] else [],
                  'checked_uses':ctx.get('checked_uses',[use]),'frame_type':ctx.get('frame_type','same_request_two_worlds'),
                  'extent':'compiler-selected entries, ordered keys and recorded path conditions only'}}
    inherited_pairs=list(plan.get('selected_pairs',[]))
    plan['observation_choice']={'ordinary_pairs':inherited_pairs,'selected':pick,'pool':[pick] if pick else [],'status':'selected_property' if pick else 'unsupported',
        'reason':'source-resolved finite property' if pick else reason,'property_requested':measure,'claim_text':item['claim'],'possible_compilations':len(contexts),
        'stage_evidence':stage(inv,root),'request_resolution':{'finding_root':root,'use':pick['observe'] if pick else None,
        'possible_uses':sorted(entries),'unmeasured_uses':sorted(entries-{pick['observe'],pick['change']}) if pick else sorted(entries)}}
    if pick:
        plan['selected_pairs']=[{'change':pick['change'],'observe':pick['observe'],'source_reason':'typed property and matching applied target'}]
    inv.graph.events.append({'action':'compile_source_property','measure':measure,'root':root,'selected':bool(pick),'reason':plan['observation_choice']['reason']})


```

## source/src/pr_next_joint/investigation/property_model.py

SHA-256 `8caa27bcee911b2c0802d569177f3c2e3977dd522aca0722eb1ae57b1c56940a`

```python
"""Host-compiled properties and evidence composition, shared by Full consumers.

Model judgments are proposals. Program execution does not prove a business
policy; source-backed policy/resource interpretations remain explicit H inputs.
"""
import copy
import re
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key, walk, op
from pr_next_joint.frontend.storage import selectors, keys, selector_relation, value_type
from .summary import get_summaries, holder, unique
from .initial_state import domain, initial_for_lookup
from .roles import path_qualification


def policy_basis(item):
    from .relations import policy
    return policy(item)


def authorization_expression(inv,q,policy,*,unresolved=None):
    from .relations import authorization
    return authorization(inv,q,policy,unresolved=unresolved)


def compile_property(inv, q):
    f = inv.f; b = inv.backend; root = inv.root(q); item = q['current']
    if root is None: return None
    from .ledger import movements, unit_origin, native_only_position
    from .key_roles import relation as key_relation
    from .comparison import transfer_shapes
    summaries = get_summaries(f); rows = summaries.rows(root)
    dependencies = summaries.dependencies.forward(root)
    target = f.operations[root]['target']
    cells = unique(c for oid in [root] for c in summaries.positions(oid)
                   if not summaries.control_only(c,target))
    bindings = [unit_origin(b, root, c) for c in cells]
    questions = []
    for c, unit in zip(cells, bindings):
        bound = inv.semantics.lookup(root, c)
        if not unit and not (bound and bound['meaning'] == 'nonfinancial_counter'):
            questions.append(inv.semantics.question(q, root, c))
    known_semantics = [u for u in bindings if u]
    possible = set(); text = item.get('claim', '')
    declared = set(q['claim_source_scope']['source_operations']) | {root}
    # An anchored control can have a real downstream financial use without a
    # second model anchor. This is a source dependency candidate, not a claim
    # expansion based on the exploratory next_check endpoint.
    control_uses=set()
    if f.options.scope=='FCR':
        written=[w['path'] for r in rows for w in r['ordered_writes']]
        for cell in written:
            if unit_origin(b,root,cell):continue
            if (key_relation(cell,f.lookup(root)) or {}).get('kind')=='authorization_quantity':continue
            for use in inv.graph.access[(target,cell['root'])]['readers']:
                if use==root:continue
                if any(selector_relation(cell,c)=='same_shape' and not inv.graph._disjoint_keys(cell,c)
                       for r in summaries.rows(use) for c in selectors(r['guards'])):
                    control_uses.add(use)
    test_uses=set()
    if f.options.scope=='FCR' and item.get('category') in ('FCR-FREEZE','FCR-PAUSE'):
        # A proposed control must be falsifiable even when the graph finds no
        # effect edge. Select an actual ordinary token-flow use, not a clock
        # setter interpreted as issuance, and never infer a different category
        # merely from an administrative number increasing or decreasing.
        candidates={}
        for use,entry in f.operations.items():
            if entry['target']!=target or use==root:continue
            for rr in summaries.rows(use):
                pp=f.paths[rr['path']]['raw']
                if path_qualification(f,use,pp):continue
                mm=movements(b,use,pp)
                for debit,credit in transfer_shapes(b,use,pp):
                    if unit_origin(b,use,debit) and not native_only_position(b,use,debit):
                        candidates.setdefault(key({'root':debit['root'],'fields':[s for s in debit.get('segments',[])if 'field'in s]}),set()).add(use)
        named={use for uses in candidates.values() for use in uses if use in declared}
        if named:test_uses=named
        elif len(candidates)==1:test_uses=next(iter(candidates.values()))
    value_uses={use for use,kinds in dependencies['uses'].items() if 'value' in kinds and summaries.positions(use)}
    property_entries=declared|control_uses|test_uses|value_uses
    # Supplemental anchors are context, not a request to change the root's object.
    cells = unique(cells + [c for use in sorted(control_uses|test_uses|value_uses) for c in summaries.positions(use)])
    bindings = [unit_origin(b, root, c) for c in cells]
    known_semantics = [u for u in bindings if u]
    native_debits=unique(e['cell'] for r in rows for e in r['numeric_effects']
        if e['holder'] is not None and 'debit' in e['may_directions'] and b._native_unit_source(root,e['cell']))
    if f.options.scope == 'AC':
        cat = 'AC'; rules=getattr(inv.semantics,'rules',None)
        policy = (rules.policy(q) if rules and item.get('_semantic_consumer') else None) or q.get('authorization_interpretation') or policy_basis(item)
        prior_policy=next((policy_basis(v) for v in reversed(q.get('history',[])) if policy_basis(v)),None)
        if policy and policy.get('meaning')=='normal_authorization' and prior_policy:
            # A normal proposal does not erase the qualification being tested.
            # It may add a source-bound business alternative to that predicate.
            policy=dict(prior_policy,normal_proposal=copy.deepcopy(policy))
        if policy is None:
            policy=prior_policy
        if policy is None:
            questions.append(inv.semantics.question(q, root, kind='authorization'))
        else:
            unresolved=set()
            predicate=authorization_expression(inv,q,policy,unresolved=unresolved)
            if (not predicate and not unresolved and policy.get('source') == 'focused_model_answer'
                    and item.get('_opinion_message') and item.get('_scope_effects')):
                from .policy_binding import effect_duty
                original_policy = policy_basis(item)
                if (original_policy and effect_duty(original_policy['text'])
                        and not effect_duty(policy.get('basis',''))):
                    # An uninformative reply cannot silently replace a previously bound duty.
                    policy = original_policy
                    predicate = authorization_expression(inv,q,policy,unresolved=unresolved)
            if unresolved:policy=dict(policy,unresolved_relations=sorted(unresolved))
            if predicate:
                interpretations = [predicate]
                for alternative in q.get('authorization_alternatives', []):
                    other = authorization_expression(inv, q, alternative)
                    if other and all(key(other['predicate']) != key(x['predicate']) for x in interpretations):
                        interpretations.append(other)
                if len(interpretations) > 1:
                    # A witness must violate every still-supported policy.
                    # UNSAT for their conjunction does not refute each policy.
                    predicate = dict(predicate,
                        predicate=op('or', *[x['predicate'] for x in interpretations]),
                        competing_interpretations=interpretations,
                        competition_semantics='one behavior violates all surviving interpretations')
                policy=dict(policy,compiled_authorization=predicate)
            if predicate and not predicate.get('source_bound_alternatives'):
                from .authorization_normal import payment_qualification
                potential=payment_qualification(inv,q,predicate['subject'],require_proposal=False) if predicate.get('subject') is not None else []
                if potential:
                    question=inv.semantics.question(q,root,kind='authorization')
                    question.update(question='Does the recorded actual payment establish a lawful business qualification for acquiring this authority? Explain the source relation and any bypass.',
                        source_qualification_candidates=[{'authority':b._storage_name(root,x['holder']),
                            'recorded_payment':b._storage_name(root,x['bid']),
                            'relation':'actual payment exceeds the previous recorded payment; the same payer receives this authority',
                            'source_path':x['path'],'business_legitimacy_not_proved':True} for x in potential])
                    questions.append(question)
        possible.add(cat)
    else:
        policy = None
        for r in rows:
            # This selects a typed hypothesis from known source writes, not
            # a successful execution. A residual read must reach the actual
            # condition checker instead of erasing the hypothesis/category.
            p = f.paths[r['path']]['raw']; m = movements(b, root, p)
            # A stage counter beside a known native entitlement is not a token
            # ledger merely because both numeric fields change on this path.
            # Unknown units still receive the semantic questions above.
            m={sign:[c for c in values if unit_origin(b,root,c)] for sign,values in m.items()}
            transfers = transfer_shapes(b, root, p)
            if any(unit_origin(b,root,a) and not native_only_position(b,root,a) for a,_ in transfers): possible.add('FCR-TRANSFER')
            if any(not any(selector_relation(d, c) == 'same_shape' and key(d) != key(c)
                           for c in m['+']) and not native_only_position(b,root,d) for d in m['-']): possible.add('FCR-DESTROY')
            if any(not any(selector_relation(c, d) == 'same_shape' and key(c) != key(d)
                           for d in m['-']) and not native_only_position(b,root,c) for c in m['+']): possible.add('FCR-MINT')
        # State controls are discovered by the graph, including numeric/stage
        # guards. This selects a property; it does not assert a freeze/pause.
        for use in property_entries:
            for r in summaries.rows(use):
                if not any('debit' in e['may_directions'] and e['holder'] is not None and
                    unit_origin(b,use,e['cell']) and not native_only_position(b,use,e['cell']) for e in r['numeric_effects']): continue
                for control in inv.graph.request_reads(use):
                    if unit_origin(b,use,control):continue
                    if (key_relation(control,f.lookup(use)) or {}).get('kind')=='authorization_quantity':continue
                    if any(w['raw']['path']['root'] == control['root'] and w['operation'] in declared
                           and w['operation'] != use and path_qualification(f,w['operation'],f.paths[w['path']]['raw']) for w in f.writes.values()):
                        from .dependencies import control_candidates
                        possible.update(control_candidates(control,[e['holder'] for e in r['numeric_effects']
                            if e.get('holder') is not None and 'debit' in e['may_directions']]))
        if value_uses and any(path_qualification(f,root,f.paths[r['path']]['raw']) for r in rows):
            # An actual state-dependent transfer amount can affect value as
            # well as availability. Admission to a category still needs its
            # own source/proof record. No second class is inferred from a name.
            for use in sorted(value_uses):
                for r in summaries.rows(use):
                    units=[e for e in r['numeric_effects'] if e['holder'] is not None and unit_origin(b,use,e['cell'])
                           and not native_only_position(b,use,e['cell'])]
                    directions={d for e in units for d in e['may_directions']}
                    if 'debit' in directions:possible.add('FCR-DESTROY')
                    if {'debit','credit'}<=directions:possible.add('FCR-TRANSFER')
                    if 'credit' in directions and 'debit' not in directions:possible.add('FCR-MINT')
        if not possible and native_debits:
            possible.add('ADDITIONAL')
        scoped=set(item.get('_scope_effects',())) if item.get('_opinion_message') else set()
        if scoped:
            from .summary import local_delta
            from .dependencies import control_candidates
            applicable=set()
            for handle in scoped:
                effect=inv.semantics.rules.effects.get(handle,{})
                if effect.get('oid')!=root or 'cell' not in effect:continue
                cell=effect['cell'];direction,_=local_delta(effect['write'])
                if holder(cell,f.lookup(root)) and not summaries.control_only(cell,target):
                    if direction=='-':applicable.update(('FCR-TRANSFER','FCR-DESTROY'))
                    if direction=='+':applicable.update(('FCR-TRANSFER','FCR-MINT'))
                for use in control_uses|value_uses:
                    for row in summaries.rows(use):
                        productive=[v['holder'] for v in row['numeric_effects'] if v['holder'] is not None and 'debit' in v['may_directions']]
                        if not productive:continue
                        if any(selector_relation(cell,s)=='same_shape' for s in selectors(row['guards'])):
                            applicable.update(control_candidates(cell,productive))
                        if use in value_uses and any(s['root']==cell['root'] for w in row['ordered_writes'] for s in selectors(w['value'])):
                            applicable.update(possible & {'FCR-TRANSFER','FCR-MINT','FCR-DESTROY'})
            if not item.get('category'):
                possible.intersection_update(applicable)
                # Missing unit remains an open, source-anchored consumer.
                if not possible:possible.update(applicable)
        hint = item.get('category')
        from .contracts import CATEGORIES
        if hint in CATEGORIES[1:]:
            cat = hint
        elif len(possible) == 1: cat = next(iter(possible))
        else:
            # Only a hint to a corresponding actual effect is usable. Ambiguous
            # tasks stay open instead of sorting effect names into a risk label.
            cat = None
        if hint == 'ADDITIONAL' and not possible: cat = 'ADDITIONAL'
    relation = {'task': f.options.scope, 'target': target, 'operation': root,'source_identity':f.identity,
        'category': cat, 'possible_categories': sorted(possible),
        'domain': domain(f.lookup(root)),
        'initial_identity': initial_for_lookup(f.lookup(root))['identity'],
        'objects': cells, 'resource_bindings': known_semantics,
        'expected_authorization': policy, 'actual_guards': [r['guards'] for r in rows],
        'source_operations': sorted(declared), 'stage': item.get('phase'),
        'source_linked_control_uses':sorted(control_uses),
        'value_dependence':{'closure':dependencies['id'],'value_uses':sorted(value_uses),
            'precision':dependencies['precision']},
        'control_use_frontier':sorted(test_uses),
        'frontier_meaning':'source token-flow uses for testing the control hypothesis; not inferred effect edges',
        'native_redemption_debits':native_debits,
        'financial_consent':copy.deepcopy(q.get('financial_consent_interpretation')),
        'claim_assumptions':copy.deepcopy(item.get('assumptions',[])),
        # An interpretation belongs to the actual downstream holder/use. A
        # control property that depends on that use must be recompiled even
        # when the wire happened to ask a separate direct-use question.
        'semantic_dependency_operations': sorted(set(q['binding']['operations'])|property_entries),
        'consent_dependency_operations': sorted(value_uses|{root}) if cat in ('FCR-TRANSFER','FCR-DESTROY') else [],
        'semantic_version': inv.semantics.dependency_identity(set(q['binding']['operations'])|property_entries,
            consent_operations=value_uses|{root} if cat in ('FCR-TRANSFER','FCR-DESTROY') else []),
        'semantic_questions': questions, 'summary_identity': summaries.identity,
        'residuals': [x for r in rows for x in r['residuals']] + [r for (t, _),r in
            getattr(b,'unit_conflicts',{}).items() if t==target and any(
                selector_relation(r['cell'],c)=='same_shape' for c in cells)],
        'kind': 'host_typed_source_property', 'model_category_hint': item.get('category'),
        'minimum_evidence': 'applicable source/semantic/program support; no universal SMT requirement'}
    if f.options.scope=='FCR':
        original=item.get('_original_model_category') or item.get('category')
        relation['original_category']=original
        relation['consent_rows']=[]
        if cat in ('FCR-TRANSFER','FCR-MINT','FCR-DESTROY'):
            relation['quantity_routes']={use:digest(summaries.dependencies.amounts_for(use)) for use in sorted(value_uses|{root})}
            relation['financial_consents']={}
            if cat in ('FCR-TRANSFER','FCR-DESTROY'):
                for use in sorted(value_uses|{root}):
                    for amounts in summaries.dependencies.amounts_for(use):
                        for gate in amounts['allowance_gates']:
                            issuer=keys(gate['grant'])[gate['issuer_key']]
                            for debit in amounts['deltas']:
                                if debit['sign']!='-' or debit.get('key_role')=='authorization_quantity' or key(debit.get('holder'))!=key(issuer):continue
                                scope={'path':amounts['path'],'grant':gate['grant'],
                                       'issuer_key':gate['issuer_key'],'spender_key':gate['spender_key'],
                                       'debit_expression':debit['amount_expression'],
                                       'checked_quantity_expression':gate['quantity_expression'],'ledger':debit['cell']}
                                interpretation=inv.semantics.lookup_consent(use,debit['cell'],scope)
                                if interpretation:
                                    if interpretation not in relation['consent_rows']:relation['consent_rows'].append(interpretation)
                                elif debit['amount_expression']!=gate['quantity_expression']:
                                    sq=inv.semantics.question(q,use,debit['cell'],kind='financial_consent',quantity_scope=scope)
                                    current=inv.semantics.questions[sq['id']]
                                    current.setdefault('quantity_scope',[])
                                    if scope not in current['quantity_scope']:current['quantity_scope'].append(scope)
                                    # One registered source entity remains identical
                                    # on the wire and at answer consumption.
                                    questions[:]=[x for x in questions if x.get('id')!=sq['id']]
                                    questions.append(copy.deepcopy(current))
        for use in sorted(value_uses|{root}):
            cs=[c for c in relation['consent_rows'] if c['operation']==use]
            if len(cs)==1:relation['financial_consents'][use]=cs[0]
        relation['category_obligations']=[{'category':category,'source_candidate':category in possible,
            'original':category==original,'operation':root,'closure':dependencies['id'],
            'validation':'requires_same_scope_evidence'} for category in
            sorted(possible | ({original} if original in CATEGORIES[1:] else set()))]
    if q.get('history') and item['claim'].strip()!=q['history'][-1]['claim'].strip():
        rootname=f.operations[root]['function'].split('(')[0]
        root_named=bool(re.search(r'(?<![\w$])'+re.escape(rootname)+r'(?![\w$])',text))
        pointed=[]
        for oid,o in f.operations.items():
            if oid==root or o['target']!=target:continue
            name=o['function'].split('(')[0]
            explicit=re.search(r'(?<![\w$])'+re.escape(name)+r'\s*\(',text) or re.search(r'`'+re.escape(name)+r'`',text)
            if re.search(r'[a-z][A-Z]',name):explicit=explicit or re.search(r'(?<![\w$])'+re.escape(name)+r'(?![\w$])',text)
            if explicit:pointed.append(oid)
        origins={key(a) for a in summaries.operations[root]['source_closure']}
        foreign=[o for o in pointed if not {key(a) for a in summaries.operations[o]['source_closure']}<=origins]
        root_role_write=any(not keys(w['path']) and value_type(w['path'],f.lookup(root)) in ('address','address payable') for r in rows for w in r['ordered_writes'])
        changed_kind=(item.get('category') not in possible and f.options.scope=='FCR' or
                      root_role_write and any(summaries.positions(o) for o in foreign) and not re.search(r'\b(?:acquir\w*|takeover|becom\w*|install\w*)\b',text,re.I))
        if foreign and not root_named and changed_kind:
            relation['core_rebinding_required']={'old_core':root,'source_named_candidates':foreign,
                'reason':'revised actual effect does not have the old core source; no old-root credit inherited'}
    # Business identity is not the consumption/cache identity. New evidence,
    # search branches and supplementary-anchor ordering do not change a policy.
    relation['claim_identity'] = digest([f.options.scope, target, root, cat,
        sorted(key(c) for c in cells), item.get('actor'), item.get('object'), item.get('phase'),
        (policy or {}).get('meaning'),((policy or {}).get('compiled_authorization') or {}).get('predicate'),
        relation.get('core_rebinding_required')])
    rules=getattr(inv.semantics,'rules',None)
    if rules:relation['scoped_semantics']=rules.signature(root)
    relation['id'] = 'property_' + digest(relation)[:20]
    return relation


def planning_item(q):
    item = copy.deepcopy(q['current']); p = q.get('property') or {}
    if p.get('category'): item['category'] = p['category']
    if p.get('category')=='AC' and (p.get('expected_authorization') or {}).get('compiled_authorization'):
        if isinstance(item.get('observation'),dict) and item['observation'].get('measure')=='denied_qualified':
            item['observation']['authorization']=p['expected_authorization']['compiled_authorization']
        else:
            item['observation']={'measure':'authorization_violation','authorization':p['expected_authorization']['compiled_authorization']}
    if p.get('category') in ('FCR-TRANSFER', 'FCR-DESTROY', 'FCR-MINT') and p.get('objects'):
        ob = item.get('observation')
        if not isinstance(ob, dict) or ob.get('measure') in (None, 'opens', 'blocks'):
            item['observation'] = {'measure': 'direct_effect'}
    return item


def _typed_assessment(inv, q):
    """One decision from typed obligations. Legacy reportable is never read."""
    prop = q.get('property')
    root = inv.root(q)
    item = q['current']
    scope = {'source_prediction': True, 'concrete_EVM': False,
             'deployment_reachability_proved': False, 'entire_contract_safety_proved': False,
             'compiled_property': copy.deepcopy(prop), 'claim_identity': (prop or {}).get('claim_identity'),
             'only_declared_operations': q['binding'].get('operations', []),
             'scoped_observations': [], 'evidence_dependencies': {}, 'semantic_task_review': q.get('task_review')}
    result = {'root': root, 'category': (prop or {}).get('category'), 'reportable': False,
              'reasons': [], 'scope': scope, 'evidence_refs': list(q['evidence'])}
    if q.get('retired_property_parent'):
        result['reasons']=['derived_obligation_replaced_by_current_parent']
        scope['route_status']='superseded'
        return result
    if not prop or not root or not q['binding'].get('core_exact', q['binding'].get('exact')):
        result['reasons'] = ['source_identity_ambiguous_or_unresolved' if root is None else 'validated_property_not_available']
        return result
    if prop.get('core_rebinding_required'):
        result['reasons'] = ['changed_business_effect_requires_source_rebinding']
        return result
    scope['expected_authorization'] = prop.get('expected_authorization')
    scope['model_original_judgment'] = {'assessment': item.get('assessment'), 'claim': item.get('claim')}
    cat = prop.get('category')
    if not cat:
        result['reasons'] = ['property_task_meaning_unresolved']
        return result
    if cat=='AC':
        from .policy_binding import audit_authorization
        checked=audit_authorization(inv.f,root,(prop.get('expected_authorization') or {}).get('compiled_authorization'))
        scope['source_ir_checks']=checked
        if any(not r['matches'] for r in checked):
            result['reasons']=['source_ir_disagreement']
            return result
    inspections = [inv.evidence[label] for label in q['evidence']
                   if inv.evidence[label].get('kind') == 'source_inspection' and inv.evidence[label].get('operation') == root]
    scope['source_deductions'] = [{'evidence': r['id'], 'no_committing_path': r.get('no_committing_path'),
                                 'net_unchanged': r.get('net_effect_proved_unchanged')} for r in inspections]
    observation = item.get('observation')
    measure = observation.get('measure') if isinstance(observation, dict) else None
    if measure != 'denied_qualified':
        nonstorage=any('kind' in inv.semantics.rules.effects.get(e,{}) for e in item.get('_scope_effects',()))
        reason = next(('original_root_has_no_committing_path' if r.get('no_committing_path')
                       else 'original_root_net_effect_is_unchanged' for r in inspections
                       if r.get('no_committing_path') or (not nonstorage and r.get('net_effect_proved_unchanged'))), None)
        if reason:
            result['reasons'] = [reason]
            scope['route_status'] = 'excluded'
            scope['necessary_conditions'] = {'actual_effect': 'refuted_by_complete_source',
                                            'other_unknowns_decisive_for_this_route': False}
            return result
    current = [e for label in q['evidence'] for e in [inv.evidence[label]]
               if e.get('source_identity') == inv.f.identity and
               (e.get('property_validation_key') == validation_key(prop) or e.get('property_identity') == prop['id'])]
    queries = [x for e in current for x in e.get('queries', [])
               if x.get('details', {}).get('property_identity') == prop['id'] or
               e.get('property_validation_key') == validation_key(prop)]
    scope['revalidated_evidence'] = [{'evidence': e['id'], 'validation_key': e.get('property_validation_key')}
                                   for e in current]
    if inv.f.options.scope == 'AC':
        policy = prop.get('expected_authorization') or {}
        expected = policy.get('compiled_authorization')
        if not expected:
            result['reasons'] = ['expected_authorization_not_established']
            return result
        label = 'denied_qualified' if measure == 'denied_qualified' else 'authorization_violation'
        relevant = [x for x in queries if x.get('label') == label and x.get('details', {}).get('property_validated')]
        positives = [x for x in relevant if x.get('bounded_condition_confirmed')]
        source_support = [e for e in current if e.get('kind') == 'source_property_certificate' and
                          e.get('property_validated') and e.get('supports') == label]
        all_paths = {pid for pid, _ in inv.f.operation_paths(root, True)}
        excluded = {x['details'].get('use_path') for x in relevant if x.get('answer') == 'unsat'
                    and not x.get('abstract_hash') and (x.get('exclusion_certificate', {}).get('excludes_only_this_formula')
                    or x.get('details', {}).get('prestate', {}).get('global_reachability_exhausted'))}
        scope['property_support'] = [{'policy': policy, 'queries': [x['id'] for x in relevant]}]
        scope['authorization_counterevidence'] = [x['id'] for x in relevant if x.get('answer') == 'unsat']
        result['reportable'] = bool(positives or source_support) and not (label=='denied_qualified' and expected.get('necessary_only'))
        from .policy_binding import source_excludes_violation
        structural=source_excludes_violation(inv.f,root,expected) if label=='authorization_violation' else None
        if structural:
            scope['local_authorization_exclusion']=structural
            result['reportable']=False
            result['reasons']=['source_supported_applicable_normal_authorization']
            scope['route_status']='excluded'
            return result
        scope['source_property_certificates'] = [e['id'] for e in source_support]
        if not result['reportable']:
            subcases_complete=all(not e.get('local_errors') for e in current if e.get('observed_measure')==label)
            # A same-requester grant/use subcase cannot exclude untested
            # nominee, application or proxy continuations. A complete source
            # authorization exclusion above remains valid for all of them.
            acquire=expected.get('property_family')=='acquire'
            if acquire:scope['acquisition_actor_coverage']='checked source-bound subcases; untested control chains remain open'
            if not acquire and not expected.get('necessary_only') and all_paths and all_paths <= excluded and subcases_complete and inv.backend.complete(root) and not expected.get('competing_interpretations'):
                result['reasons'] = ['expected_authorization_covers_all_applicable_paths']
                scope['route_status'] = 'excluded'
            else:
                result['reasons'] = ['authorization_violation_not_established']
        else:
            scope['positive_condition_scopes'] = [{'probe': x['id'], 'details': x['details']} for x in positives]
    else:
        relevant = [x for x in queries if x.get('details', {}).get('property_validated') and
                    x.get('label') in ('direct_effect', 'financial_block','financial_value')]
        positive = [x for x in relevant if x.get('bounded_condition_confirmed')]
        settlements=[]
        if cat=='FCR-DESTROY':
            uses={root}|set(prop.get('value_dependence',{}).get('value_uses',[]))
            for label in q['evidence']:
                ev=inv.evidence[label]
                if ev.get('kind')!='source_inspection' or ev.get('operation') not in uses or ev.get('source_identity')!=inv.f.identity:continue
                for row in ev.get('settlements',[]):
                    if row.get('same_holder_and_unit_full_settlement') and any(
                            selector_relation(row['object'],c)=='same_shape' for c in prop.get('objects',[])):
                        settlements.append(dict(row,operation=ev['operation'],evidence=label))
            scope['matched_settlement_counterevidence']=settlements
            # A complete payment on one source branch cannot refute another
            # holder, unit, path or an independent unresolved callback.
            positive=[x for x in positive if not any(
                x['details'].get('observe',x['details'].get('operation'))==s['operation'] and
                x['details'].get('use_path')==s['path'] and key(x['details'].get('ledger'))==key(s['object'])
                for s in settlements)]
        checks = [e.get('financial_scope') for e in current if e.get('financial_scope')]
        accounting=[r for e in current for r in e.get('amount_correspondence',[])]
        scope['amount_correspondence']=accounting
        mismatches={(r['operation'],r.get('path')) for r in accounting if r.get('result')=='source_ir_mismatch'}
        if mismatches:
            scope['unverified_quantity_routes']=[{'operation':o,'path':p} for o,p in sorted(mismatches,key=str)]
            positive=[x for x in positive if (x['details'].get('observe',x['details'].get('operation')),x['details'].get('use_path')) not in mismatches
                      and (x['details'].get('observe',x['details'].get('operation')),None) not in mismatches]
        scope['comparison_alignment'] = {'status': 'main' if positive else 'unresolved',
                                         'conditions': checks, 'source_basis': prop.get('resource_bindings', []),
                                         'prestate_alignment': prop['domain']}
        if cat in ('FCR-PAUSE', 'FCR-FREEZE'):
            scoped={}
            for ev in current:
                if not ev.get('scope_supported'):continue
                financial=ev.get('financial_scope') or {}
                group=financial.get('ordinary_holder_family')
                for probe in ev.get('queries',[]):
                    detail=probe.get('details') or {}
                    if cat=='FCR-PAUSE' and group and not financial.get('collective_source_control'):
                        if (not detail.get('all_continuations_exact') or not detail.get('same_request')
                            or detail.get('change')!=root or detail.get('observe')!=financial.get('declared_use')):continue
                    scoped[probe['id']]=(group,detail.get('observe'))
            positive = [probe for probe in positive if probe['id'] in scoped]
            if positive and scoped[positive[0]['id']][0]:
                group,use=scoped[positive[0]['id']]
                scope['ordinary_holder_family']=group
                if use in inv.f.operations:scope['ordinary_use_location']=inv.f.operations[use]['source']
        closed_paths=set()
        for ev in current:
            cert=ev.get('necessary_condition_route_coverage') or {}
            if (ev.get('property_excluded') and cert.get('source_identity')==inv.f.identity and
                    cert.get('operation')==root and cert.get('all_source_routes_accounted')):
                closed_paths.update(cert.get('excluded_paths',{}))
        contested=[x for x in positive if x.get('details',{}).get('use_path') in closed_paths]
        if contested:
            scope['same_path_evidence_conflict']=[x['id'] for x in contested]
            positive=[x for x in positive if x not in contested]
            if not positive:
                result['reasons']=['same_property_domain_conflicting_evidence']
                return result
        result['reportable'] = bool(positive)
        scope['property_support'] = [{'probe': x['id'], 'details': x['details']} for x in positive]
        if not positive:
            value_uses=set(prop.get('value_dependence',{}).get('value_uses',[])) if cat in (
                'FCR-MINT','FCR-TRANSFER','FCR-DESTROY') else set()
            measured_values={e.get('observe') for e in current if e.get('observed_measure')=='financial_value'
                             and e.get('value_route_checked')}
            unmeasured_values=value_uses-measured_values
            scope['unmeasured_value_consumers']=sorted(unmeasured_values)
            scope['value_effect_evidence']=[{'evidence':e['id'],'use':e.get('observe'),
                'queries':[x['id'] for x in e.get('queries',[])],'residuals':e.get('local_errors',[])}
                for e in current if e.get('observed_measure')=='financial_value']
            closed_values={e.get('observe') for e in current if e.get('observed_measure')=='financial_value' and e.get('property_excluded')}
            local_closed=any(e.get('observed_measure')=='direct_effect' and e.get('property_excluded') for e in current)
            excluded = not mismatches and not unmeasured_values and value_uses<=closed_values and local_closed
            result['reasons'] = ['matched_direct_effect_impossible_on_all_applicable_positions_and_paths'
                                 if excluded else 'financial_property_conditions_not_established']
            if settlements:result['reasons'].append('same_scope_actual_full_settlement')
            if excluded:
                scope['route_status'] = 'excluded'
                scope['comparison_alignment']['status'] = 'refuted'
        scope['normal_explanations'] = copy.deepcopy(q.get('local_normal_explanations', []))+[
            r for e in current for r in e.get('normal_explanations',[])]
    if result['reportable']:
        scope['route_status'] = 'supported'
        result['composed_claim'] = (f"{cat}: {inv.catalog.name(root)} establishes the source-bound "
                                    f"{'authorization violation' if cat == 'AC' else 'financial capability'} "
                                    f"under {prop['domain']}. The recorded property specifies subjects, effects and scope.")
        result['evidence_level'] = 'source_semantic_and_program'
    return result


def compose(inv, q, old=None):
    from .source_opinion import scoped_opinion, describe
    result = _typed_assessment(inv, q)
    scope = result['scope']
    cat = result['category'] or (q['current'].get('category') if q['current'].get('category') in ('AC','FCR-TRANSFER','FCR-MINT','FCR-DESTROY','FCR-PAUSE','FCR-FREEZE') else None)
    if cat:result['category']=cat
    basis = scoped_opinion(inv, q)
    required=((q.get('property') or {}).get('expected_authorization') or {}).get('compiled_authorization') or {}
    if required.get('necessary_only') and basis['status']=='normal':
        basis={'status':'open','reason':'policy_missing','locations':basis['locations']}
    current=q.get('changed_validation_key')
    if current and basis['status']=='risk' and not any(
            inv.evidence[e].get('property_validation_key')==current or
            inv.evidence[e].get('kind')=='source_inspection' and inv.evidence[e].get('operation')==result['root']
            for e in q['evidence']) and not q.get('office_effects') and not q['current'].get('_semantic_consumer'):
        # An unexamined semantic revision cannot inherit a delayed program result.
        # Independent, scoped source readings remain usable without a new solver query.
        basis={'status':'open','reason':'revised_policy_not_read','locations':basis['locations']}
    if (result.get('root') and basis['status'] in ('normal','excluded') and any(
            g['kind'] in ('source_expression_limit','dependent_source_expression_limit')
            for g in inv.f.operations[result['root']]['gaps'])):
        basis={'status':'open','reason':'unexpanded_source_dependency','locations':basis['locations']}
        result.update(reportable=False,reasons=['unexpanded_source_dependency'])
        scope['route_status']='open'
    status = scope.get('route_status')
    blocked = {'source_ir_disagreement','changed_business_effect_requires_source_rebinding',
               'same_property_domain_conflicting_evidence','source_identity_ambiguous_or_unresolved',
               'derived_obligation_replaced_by_current_parent'}
    if status == 'excluded' or set(result['reasons']) & blocked or status == 'superseded':
        judgment = 'excluded' if status == 'excluded' else 'open'
        reason = 'source_check_excluded' if judgment == 'excluded' else 'core_mismatch'
    elif basis.get('decisive_consent_gap'):
        judgment,reason='open',basis['reason']
        result.update(reportable=False,reasons=[reason]);scope['route_status']='open'
    elif basis.get('same_scope_authorized') or basis['status'] == 'excluded' or basis['reason'] in ('ordinary_paid_credit','nominee_acceptance','no_debit_in_scope','applicable_payment_qualification','same_position_restored','no_new_controlled_credit','intra_ledger_transfer','parameter_only','zero_quantity','incoming_only','same_request_bypass','partial_quota','guarded_state_change','guarded_source_effect','local_bookkeeping'):
        judgment, reason = basis['status'], basis['reason']
        result.update(reportable=False,reasons=list(dict.fromkeys([reason]+[r for r in result['reasons'] if r=='same_scope_actual_full_settlement'])))
        scope['route_status'] = 'excluded' if judgment=='excluded' or reason in (
            'same_position_restored','guarded_state_change','intra_ledger_transfer','zero_quantity',
            'incoming_only','same_request_bypass','no_new_controlled_credit') else 'normal_prediction'
    elif basis['reason']=='conflicting_scoped_meanings' and not result['reportable']:
        judgment,reason='open',basis['reason']
    elif result['reportable']:
        judgment = 'risk'
        reason = 'source_certificate' if scope.get('source_property_certificates') and not scope.get('positive_condition_scopes') else 'program_support'
        if basis['status']=='risk':
            reason=basis['reason']
    else:
        judgment, reason = basis['status'], basis['reason']
        if judgment == 'risk' and cat:
            result.update(reportable=True,reasons=[],evidence_level='source_policy_or_right_prediction')
            scope.update(route_status='supported',comparison_alignment={'status':'main','source_scope_checked':True})
        elif judgment == 'normal':
            scope['route_status']='normal_prediction'
    if judgment == 'risk' and reason == 'source_certificate':
        result['evidence_level']='source_deduction'
    locations=basis['locations'] or ([inv.f.operations[result['root']]['source']] if result.get('root') else [])
    # A program-level authorization proof is attached to its exact write
    # when every committing branch shares just that occurrence.
    if judgment=='risk' and cat=='AC' and reason=='program_support' and result.get('root'):
        actual=inv.f.summaries.rows(result['root'])
        sites={key(w['source']):w['source'] for row in actual if row['committing'] for w in row['ordered_writes']}
        if len(sites)==1 and all(not r['effects'] and not r['residuals'] for r in actual if r['committing']):
            locations=list(sites.values())
            basis=dict(basis,exact_write=True)
    details=inv.semantics.rules.describe_source(result['root'],cat,reason,locations,q['id']) if getattr(inv.semantics,'rules',None) else {'explanation':describe(cat,reason)}
    scope['decision']={'status':judgment,'reason':reason,'locations':locations,**details}
    if basis.get('source_relation') and judgment==basis['status']:
        scope['decision']['source_relation']=basis['source_relation']
        scope['decision']['causal_root']=locations[0]
    rules = getattr(inv.semantics, 'rules', None)
    if rules and getattr(rules, 'bridges_at', None):
        links = sorted({identity for e in q['current'].get('_scope_effects',())
                        for identity in rules.bridges_at.get(e,())})
        if links:
            scope['decision']['source_edge_ids'] = links
    if q['current'].get('_audit_kind'):
        scope['decision']['audit_card'] = {
            'kind': q['current']['_audit_kind'], 'check': q['current']['_audit_check'],
            'bound_effects': list(q['current'].get('_scope_effects', ())),
            'source_relation_independent': bool(basis.get('source_relation')),
            'semantic_reading_used': bool(basis.get('semantic_local') and judgment == basis['status']),
        }
    if basis.get('semantic_local'):
        scope['decision']['opinion_source']='source_bound_local_semantic_reading'
        scope['decision']['effects']=list(q['current'].get('_scope_effects',()))
        if judgment=='risk' and basis['status']=='risk' and reason=='scoped_semantic_conflict':result['evidence_level']='scoped_semantic_prediction'
    if result.get('root'):
        scope['decision']['application_location']=inv.f.operations[result['root']]['source']
    if len(locations)==1 and (basis.get('semantic_local') or basis.get('productive_use') or basis.get('protected_use') or basis.get('exact_write')):
        scope['decision']['causal_root']=locations[0]
    if scope.get('ordinary_holder_family') and judgment=='risk':
        scope['decision']['holder_family']=scope['ordinary_holder_family']
        if scope.get('ordinary_use_location'):scope['decision']['productive_use']=scope['ordinary_use_location']
    if basis.get('holder_family') and judgment=='risk':
        scope['decision']['holder_family']=basis['holder_family']
    if basis.get('productive_use') and judgment=='risk':
        scope['decision'].update(productive_use=basis['productive_use'],basis_probe=basis['basis_probe'])
        if basis.get('conditional_agent'):
            scope['decision']['conditional_agent']=basis['conditional_agent']
            scope['decision']['explanation']+=' An already exempt agent may serve the same request if the holder granted the required allowance.'
    if basis.get('protected_use') and judgment=='risk':
        scope['decision']['protected_use']=basis['protected_use']
        scope['decision']['explanation']+=' A separate entry consumes the changed qualification at the linked source location.'
    if locs := [r for r in locations if r.get('file') and 'start' in r]:
        scope['decision_identity']=digest([inv.f.identity,cat,result['root'],[(v['file'],v['start'],v.get('length')) for v in locs],reason])

    result['reportable']=judgment=='risk' and bool(cat and result.get('root'))
    return result


def applicable_normal_authorization(inv,q,policy):
    """Only a checked applicable predicate can close a normal proposal.

    A stage/quantity guard, or the word normal, is never a certificate. The
    query must use this exact property, its actual operands and every complete
    committing path. Partial normal evidence stays local.
    """
    root=inv.root(q);p=q.get('property') or {}
    if not root or inv._direction_contradictions(q):return False
    if (policy or {}).get('property_family')=='acquire' or (
        ((p.get('expected_authorization') or {}).get('compiled_authorization') or {}).get('necessary_only')
        or (p.get('expected_authorization') or {}).get('unresolved_relations')):return False
    rows={pid for pid,_ in inv.f.operation_paths(root,True)}
    if not rows or not inv.backend.complete(root):return False
    checked=[x for label in q['evidence'] for x in inv.evidence[label].get('queries',[])
        if x.get('label')=='authorization_violation' and x.get('details',{}).get('property_identity')==p.get('id')]
    if any(x.get('bounded_condition_confirmed') for x in checked):return False
    covered={x['details'].get('use_path') for x in checked if x.get('answer')=='unsat' and not x.get('abstract_hash') and
        x['details'].get('argument_domain')=='all_source_inputs_on_this_committing_path' and
        x['details'].get('prestate',{}).get('analysis_domain')=='ac_checked_prestate_r1'}
    return rows<=covered



def canonical_resource(row):
    if not isinstance(row,dict):return None
    return [row.get(k) for k in ('meaning','target','operation','family','quantity_scope','scope')]

def validation_key(p):
    if not p:
        return None
    resources = []
    for row in p.get('resource_bindings', []):
        binding = row.get('binding') or {}
        resources.append([row.get('kind'), binding.get('meaning'),
                          (binding.get('semantic_assertion') or {}).get('unit_kind')])
    expected = (p.get('expected_authorization') or {}).get('compiled_authorization') or {}
    return digest([p.get('scoped_semantics'),[canonical_resource(c) for c in p.get('consent_rows',())],p.get('source_identity'),p.get('target'),p.get('operation'),p.get('claim_identity'),p.get('domain'),p.get('initial_identity'),
        p.get('summary_identity'),sorted(key(x) for x in p.get('objects',[])),p.get('claim_assumptions'),p.get('stage'),
        expected.get('predicate'),expected.get('property_family'),expected.get('acquisition_uses'),
        expected.get('necessary_only',False),(p.get('expected_authorization') or {}).get('unresolved_relations'),
        sorted(key(x.get('predicate')) for x in expected.get('competing_interpretations',[])),sorted(key(x) for x in resources),
        p.get('value_dependence'),p.get('quantity_routes'),canonical_resource(p.get('financial_consent')),
        {o:canonical_resource(c) for o,c in (p.get('financial_consents') or {}).items()},p.get('original_category'),p.get('category_obligations')])

```

## source/src/pr_next_joint/investigation/protocol.py

SHA-256 `ff7bcb21c319c8df95e540ed9f252391dc5fe8de3cc3be6208e8c8764166941a`

```python
"""Tolerant local normalization. The model never supplies AST, SMT or host identity."""
import copy,json,re,time
from pr_next_joint.core import digest
from .contracts import VERSION,ident,write
from .decision_output import receipt as body_receipt,context_summary,diagnostic

ANSWER_CHOICES = {
    'resource': ('financial_right', 'nonfinancial_counter', 'other_source_explanation', 'unknown'),
    'authorization': ('required_authorization', 'normal_authorization', 'other_source_explanation', 'unknown'),
    'financial_consent': ('gross_debit_bound', 'net_request_with_fee', 'other_source_explanation', 'unknown'),
}
AMOUNT_ROLES = ('original_request','request','gross_debit','debit','net_receipt','net','compensation')
STAGE_GUIDANCE = 'initialization_stage requires subject (its source stage flag).'
AMOUNT_GUIDANCE = 'amount_role requires role: ' + '/'.join(AMOUNT_ROLES) + '.'


def role_error(row, meaning, inherited=None):
    if 'role' not in row:
        return 'field_absent' if meaning=='amount_role' and inherited not in AMOUNT_ROLES else None
    if not isinstance(row['role'],str):return 'wrong_field_type'
    if row['role'] not in AMOUNT_ROLES:return 'outside_facet_vocabulary'
    return None


REVISION_ACTIONS = ('confirm', 'correct', 'narrow', 'withdraw')
REVISION_GUIDANCE = 'Use the shown support ref in its original facet, with action ' + '/'.join(REVISION_ACTIONS) + ' and a short reason for any change.'
INSTRUCTION = 'Read the displayed source for the actual target. Return one JSON object. Keep actors, ordered grants, phase and units distinct. No concrete actors, arguments, sequences or private reasoning.'

def instruction(task, recovery=False, *, kind=None, annotation_revision=False, policy_revision=False):
    common = INSTRUCTION
    if kind == 'scoped_support_dispute':
        return common + ' ' + REVISION_GUIDANCE + (' ' + AMOUNT_GUIDANCE if annotation_revision else '') + (' ' + STAGE_GUIDANCE if policy_revision else '')
    if kind in ANSWER_CHOICES:
        return common + ' Reply with answers[{question,answer,basis}] for the displayed question, using its choices and a brief source-based reason.' + (' A shown annotation may be revised by ref. ' + AMOUNT_GUIDANCE if annotation_revision else '') + (' ' + STAGE_GUIDANCE if policy_revision else '')
    if kind == 'local_effect':
        return common+' For the displayed effect answer issues[{effect,assessment,claim}]. Compare the applicable duty with who decides; give the actual local reason once.'
    if kind == 'issue':
        return common + ' Revise the displayed issue only. Cite its anchor, new evidence, assessment (risk, normal or investigate) and short reason.'
    meanings = sorted(ANNOTATIONS - (set() if task == 'FCR' else {'price','fee_rule','amount_role','transfer_condition'}))
    policies = sorted(POLICIES - (set() if task == 'FCR' else {'gross_debit_bound','net_request_with_fee'}))
    issue='Use issues[{effect or anchors,assessment,claim,policy_basis?,normal_explanation?}]. Give a short scoped comparison; assessment is risk, normal or investigate.'
    direction=('AC: state the applicable duty, who actually controls the effect and whether they conflict.' if task=='AC' else 'FCR: distinguish unit, holder consent, compensation and productive bypass; category is optional.')
    audit = ('For an omitted effect or competing explanations use up to four hypotheses instead: '
             'effect_ref, source_refs (shown refs or qualified functions), issue_kind, actor_holder_relation, '
             'risk_explanation, normal_alternative, decisive_missing_fact, check_kind, requested_target_ref (nullable). '
             'issue_kind: new_sink/untrusted_sensitive_flow/role_write_to_use/authorization_scope/holder_consent_scope/'
             'financial_unit/gross_vs_net/lifecycle_stage/ordinary_transfer_route/privileged_state_difference/'
             'potential_normal_counterexample/unknown. check_kind: actual_call_reachability/untrusted_flow/guard_scope/'
             'role_write_to_use/allowance_scope/same_unit_net_effect/control_change_vs_outgoing/rollback_or_external_dep/none.')
    return ' '.join((common,direction,issue,audit,'Alternatively use annotations[{on,meaning,basis}] or policies[{effect,meaning,basis,subject?}] once.',
        'Annotations: '+', '.join(meanings)+'. Policies: '+', '.join(policies)+'.',
        AMOUNT_GUIDANCE if 'amount_role' in meanings else '',STAGE_GUIDANCE,
        'For a scoped empty reading use task_analysis {task,anchors,basis}.' if not recovery else 'Correct the malformed reply using this source.'))

def question_entity(question):
    return digest([question.get(k) for k in ('id','operation','target','kind','cell','semantic_scope','core_operation','quantity_scope')])

def revision_support(item,previous,available):
    """Locate a model-supplied reason; never synthesize its business explanation.

    available is the actual new evidence sent for this issue. Exact probe IDs
    identify their containing evidence without making the model repeat labels.
    """
    texts=[item[k] for k in ('claim','revision_reason','reason','explanation')
           if isinstance(item.get(k),str)]
    refs=item.get('evidence',[])
    if isinstance(refs,str):refs=[refs]
    if not isinstance(refs,list):refs=[]
    locators={x for x in refs if isinstance(x,str)}
    for text in texts:locators.update(re.findall(r'\b(?:E\d+|probe_[a-f0-9]{20})\b',text))
    cited=set();matches=[]
    for label,record in available.items():
        ids={q['id'] for group in ('queries','holder_consent_counterexamples')
             for q in record.get(group,[]) if isinstance(q,dict) and q.get('id')}
        found=locators & ({label}|ids)
        if found:cited.add(label);matches.extend({'locator':x,'evidence':label} for x in sorted(found))
    reason=next((item[k].strip() for k in ('revision_reason','reason','explanation')
                 if isinstance(item.get(k),str) and item[k].strip()),None)
    if reason is None and isinstance(item.get('claim'),str) and item['claim'].strip()!=previous.get('claim','').strip():
        reason=item['claim'].strip()
    if reason and not re.sub(r'\b(?:E\d+|probe_[a-f0-9]{20})\b|[\W_]+','',reason):reason=None
    return sorted(cited),reason,matches


def category_value(category, task=None):
    """Finite spelling normalization, never infer a financial class from an action."""
    if category is None and task == 'AC':
        return 'AC'
    if not isinstance(category, str):
        return category
    token = re.sub(r'[\s_-]+', '-', category.strip().upper())
    if token in ('AC', 'ACCESS-CONTROL', 'ACCESS-CONTROL-VULNERABILITY'):
        return 'AC'
    # Permission/authorization is a single-task alias, not a rule classifying arbitrary prose.
    if task == 'AC' and (token in ('PERMISSION', 'AUTHORIZATION', 'AUTHORISATION') or
                         token.startswith(('ACCESS-CONTROL/', 'AUTHORIZATION/', 'AUTHORISATION/'))):
        return 'AC'
    names = ('TRANSFER', 'MINT', 'DESTROY', 'PAUSE', 'FREEZE')
    if token in names or token in tuple('FCR-' + n for n in names):
        return token if token.startswith('FCR-') else 'FCR-' + token
    m = re.fullmatch(r'FCR[/:]\s*(TRANSFER|MINT|DESTROY|PAUSE|FREEZE)|(TRANSFER|MINT|DESTROY|PAUSE|FREEZE)-?\(FCR\)', token)
    if m:return 'FCR-' + (m[1] or m[2])
    names_in_label=[n for n in names if re.search(r'(?<![A-Z])'+n+r'(?![A-Z])',token)]
    tagged=re.match(r'^FCR[-:/]-?(TRANSFER|MINT|DESTROY|PAUSE|FREEZE)(?:$|[-:/])',token)
    # An explicit namespace/class followed by explanation stays that class;
    # a multi-class label is still unresolved, not split into invented findings.
    return 'FCR-'+tagged[1] if tagged and names_in_label==[tagged[1]] else category


def normal_alternative(item):
    """Return only model-supplied original-program interpretation, with provenance."""
    obs = item.get('observation'); obs = obs if isinstance(obs, dict) else {}
    text = next((v.strip() for v in (item.get('alternative'), item.get('normal_explanation'),
                                    obs.get('normal_explanation')) if isinstance(v, str) and v.strip()), None)
    origin = 'explicit_field'
    if text is None:
        match = re.search(r'(?:relevant\s+)?normal (?:alternative|explanation)\s*:\s*(.+)', item.get('claim', ''), re.I | re.S)
        if match:
            text = match[1].strip(); origin = 'explicit_inline_claim'
    if text is None:
        return {'text': None, 'status': 'not_supplied', 'origin': None}
    hypothetical = re.search(r'\bif\b[^.!?]{0,180}\b(?:were (?:guarded|restricted|added)|had been (?:guarded|set|initialized)|guard were added)\b|'
                             r'\b(?:add|insert|introduce) (?:an? |the )?(?:guard|require|modifier)\b', text, re.I)
    return {'text': text, 'origin': origin,
            'status': 'counterfactual_program_not_normal_path' if hypothetical else 'supplied_not_program_proved'}


def semantic_direction(item, task, source_unrestricted=False):
    """Check a prediction for explicit task contradictions, not discover business risks.

    No missing controller field is required. Source checks can corroborate an explicitly
    ordinary-caller claim; public syntax alone never excludes a privileged branch.
    """
    # A competing, not-yet-accepted normal explanation is not the model's risk assertion.
    text = re.split(r'(?:relevant\s+)?normal (?:alternative|explanation)\s*:', item.get('claim', ''),
                    maxsplit=1, flags=re.I)[0]
    cat = item.get('category'); assessment = item.get('assessment')
    result = {'status': 'no_explicit_conflict', 'reasons': [], 'source_unrestricted': source_unrestricted}
    if task != 'FCR':
        return result
    outside = re.search(r'\b(?:ordinary (?:reentrancy |unprivileged )?attack|non[- ]FCR|not (?:an? |a privileged )?FCR|'
                        r'not a privileged (?:financial )?(?:risk|FCR))\b', text + ' ' + str(cat), re.I)
    no_controller = re.search(r'\b(?:no (?:actual )?privileged controller|attacker is not (?:an? )?privileged|'
                              r'not an? FCR by an actual privileged controller|no (?:normal|real|non-zero) account can (?:call|invoke))\b', text, re.I)
    anycaller = re.search(r'\bany (?:external )?(?:caller|requester|msg\.sender|account)\b', text, re.I)
    ordinary = item.get('risk_direction') in ('ordinary_exploit', 'unprivileged_attack')
    if assessment == 'risk' and (outside or no_controller or ordinary or anycaller and source_unrestricted):
        result.update(status='inconsistent_task_direction', reasons=['ordinary_attack_or_no_privileged_FCR_controller'])
    # Explicit non-task clues remain recorded without poisoning all five task categories.
    if cat not in ('FCR-TRANSFER', 'FCR-MINT', 'FCR-DESTROY', 'FCR-PAUSE', 'FCR-FREEZE') and (outside or no_controller):
        result.update(status='explicit_out_of_task_clue', reasons=['model_explicitly_distinguishes_non_FCR'])
    return result


def category_scope(item, task):
    """Coverage only: a disjunctive label stays unresolved within its named classes."""
    if task == 'AC':
        return ['AC']
    cat = item.get('category')
    if cat in ('FCR-TRANSFER', 'FCR-MINT', 'FCR-DESTROY', 'FCR-PAUSE', 'FCR-FREEZE'):
        return [cat]
    token = str(cat or '').upper()
    named = sorted({'FCR-' + c for c in ('TRANSFER', 'MINT', 'DESTROY', 'PAUSE', 'FREEZE')
                    if re.search(r'(?<![A-Z])' + c + r'(?![A-Z])', token)})
    return named  # Unscoped dependencies are resolved from actual source in coverage.py.

TOP_LISTS = frozenset(('annotations','policies','issues','answers','reviewed','hypotheses'))
WIRE_FIELDS = TOP_LISTS | {'task_analysis'}
ANNOTATIONS = frozenset(('management_role','eligibility_state','financial_right','nonfinancial_counter',
    'authorization_quantity','price','fee_rule','transfer_condition','amount_role','other_source_meaning','unknown'))
POLICIES = frozenset(('current_authority_required','holder_authorization_applies','initialization_stage',
    'gross_debit_bound','net_request_with_fee','other_source_policy','unknown'))


class AmbiguousKeys(dict):
    def __init__(self,pairs):
        super().__init__();self.duplicates=set()
        for name,val in pairs:
            if name in self:self.duplicates.add(name)
            self[name]=val


def wire_object(pairs):
    return AmbiguousKeys(pairs)


def ambiguous(value):
    if isinstance(value,AmbiguousKeys) and value.duplicates:return True
    if isinstance(value,list):return any(ambiguous(x) for x in value)
    if isinstance(value,dict):return any(ambiguous(x) for x in value.values())
    return False


def partial_envelope(text):
    decoder = json.JSONDecoder(object_pairs_hook=wire_object)
    size = len(text)
    def space(i):
        while i < size and text[i].isspace():
            i += 1
        return i
    i = space(1)
    value = {}
    seen = set()
    duplicates = set()
    if not text.startswith('{'):
        return {}, False
    while i < size:
        try:
            name, i = decoder.raw_decode(text, i)
        except ValueError:
            break
        i = space(i)
        if not isinstance(name, str) or i >= size or text[i] != ':':
            break
        if name in seen:
            duplicates.add(name)
        seen.add(name)
        i = space(i+1)
        if name in TOP_LISTS and i < size and text[i]=='[':
            rows = []
            value[name] = rows
            i = space(i+1)
            while i < size and text[i] != ']':
                try:
                    row, end = decoder.raw_decode(text,i)
                except ValueError:
                    break
                i = space(end)
                if i < size and text[i] not in ',]':
                    break
                rows.append(row)
                if i >= size or text[i] != ',':
                    break
                i = space(i+1)
            if i >= size or text[i] != ']':
                break
            i = space(i+1)
        else:
            try:
                part,end=decoder.raw_decode(text,i)
            except ValueError:
                break
            if name in WIRE_FIELDS:value[name]=part
            i=space(end)
        if i >= size or text[i] != ',':break
        i=space(i+1)
    for name in duplicates:value.pop(name,None)
    return value, bool(any(value.get(k) for k in WIRE_FIELDS))


def envelope_shape(raw):
    """Content-free structural diagnostic. Never return a key name or response text."""
    if not isinstance(raw,str):
        return {"root_type":"non_text","recognized_keys":0,"unknown_keys":0,"duplicate_keys":0}
    text=re.sub(r'^\x60\x60\x60(?:json)?\s*','',raw.strip(),flags=re.I)
    text=re.sub(r'\s*\x60\x60\x60$','',text)
    try:
        value=json.loads(text,object_pairs_hook=wire_object)
    except (ValueError,RecursionError):
        first=text[:1]
        return {"root_type":"incomplete_or_invalid_json","opening":"object" if first=='{' else "array" if first=='[' else "other",
                "recognized_keys":0,"unknown_keys":0,"duplicate_keys":0}
    if isinstance(value,dict):
        return {"root_type":"object","recognized_keys":len(WIRE_FIELDS.intersection(value)),
                "unknown_keys":len(set(value)-WIRE_FIELDS),
                "duplicate_keys":len(value.duplicates) if isinstance(value,AmbiguousKeys) else 0}
    return {"root_type":"array" if isinstance(value,list) else "scalar",
            "recognized_keys":0,"unknown_keys":0,"duplicate_keys":0}


def issue_shape(item):
    """Reject only the row whose declared wire value has the wrong shape."""
    text = ('id', 'effect', 'subject', 'category', 'assessment', 'claim', 'policy_basis',
            'alternative', 'normal_explanation', 'risk_direction', 'distinguishing_question',
            'revision_reason', 'explanation', 'reason')
    for field in text:
        if field in item and item[field] is not None and not isinstance(item[field], str):
            return field, item[field]
    for field in ('observation', 'next_check'):
        value = item.get(field)
        if value is not None and not isinstance(value, dict):
            return field, value
        for name in ('measure', 'normal_explanation', 'action', 'change', 'observe',
                     'function', 'caller_mode', 'question', 'resource', 'subject'):
            if isinstance(value, dict) and name in value and not isinstance(value[name], str):
                return field + '.' + name, value[name]
    for field in ('evidence', 'source_refs', 'anchors'):
        value = item.get(field)
        if value is not None and not isinstance(value, (str, list)):
            return field, value
        if isinstance(value, list):
            for entry in value:
                if not isinstance(entry, str):
                    return field + '[]', entry
    hint = item.get('next_check') or {}
    if 'request_bindings' in hint and not isinstance(hint['request_bindings'], dict):
        return 'next_check.request_bindings', hint['request_bindings']
    return None


def normalize(raw,task=None,*,phase='initial',sent_questions=()):
    """Parse one top-level envelope. Transport validity and semantic binding are independent."""
    diagnostics=[]
    def empty(kind, reason):
        return dict(issues=[],answers=[],annotations=[],policies=[],reviewed=[],usable_analysis=False,
                    response_kind=kind,diagnostics=[dict(d,stage=phase) for d in diagnostics]+[{'reason':reason,'stage':phase}])
    if raw is None or isinstance(raw,str) and not raw.strip():
        return empty('empty_body','empty_response_body')
    recovered=False
    if isinstance(raw,dict):
        value=copy.deepcopy(raw)
    elif isinstance(raw,str):
        text=re.sub(r'^\x60\x60\x60(?:json)?\s*','',raw.strip(),flags=re.I)
        text=re.sub(r'\s*\x60\x60\x60$','',text)
        try:value=json.loads(text,object_pairs_hook=wire_object)
        except (ValueError,RecursionError):
            try:completed,end=json.JSONDecoder().raw_decode(text)
            except (ValueError,RecursionError):pass
            else:
                if text[end:].strip():return empty('invalid_protocol','trailing_unrelated_content')
            value,recovered=partial_envelope(text)
            if not recovered:return empty('invalid_protocol','unparseable_top_level')
            diagnostics.append({'reason':'truncated_envelope_complete_items_only'})
    else:return empty('invalid_protocol','invalid_response_type')
    if isinstance(value,AmbiguousKeys) and value.duplicates:
        for name in value.duplicates:value.pop(name,None)
        diagnostics.append({'reason':'ambiguous_top_level_field'})
    if not isinstance(value,dict) or not WIRE_FIELDS.intersection(value):
        return empty('invalid_protocol','invalid_top_level_or_duplicate_key')
    # Never infer source or host authority from undeclared fields in a model row.
    bad=bool(diagnostics)
    had_content=False
    row_ordinals={}
    for field in TOP_LISTS:
        vals=value.get(field,[])
        if not isinstance(vals,list):
            diagnostics.append({'reason':field+'_not_list'});bad=True;vals=[]
        had_content|=bool(vals)
        valid=[]
        for idx,row in enumerate(vals):
            row_ordinals[(field,id(row))]=idx
            if ambiguous(row) or (isinstance(row,dict) and any(k.startswith('_') for k in row)):
                diagnostics.append({'reason':'duplicate_or_host_reserved_key','list':field,'index':idx});bad=True
            else:valid.append(row)
        value[field]=valid
    from .semantic_audit_card import parse as parse_card
    cards = []
    for idx, card in enumerate(value['hypotheses']):
        error = 'audit_card_limit' if idx >= 4 else parse_card(card)
        if error:
            diagnostics.append({'stage':phase, 'list':'hypotheses', 'index':idx, 'reason':error})
            bad = True
        else:
            cards.append(card)
    seeds={}
    located_amount_reads=[]
    for field,vocab,refkey in [('annotations',ANNOTATIONS,'on'),('policies',POLICIES,'effect')]:
        seeds[field]=[]
        for fallback,row in enumerate(value[field]):
            idx=row_ordinals.get((field,id(row)),fallback)
            if not isinstance(row,dict) or set(row)-{'id','on','effect','subject','scope','meaning','basis','ref','action','role'}:
                diagnostics.append({'reason':'invalid_seed_fields','list':field,'index':idx});bad=True;continue
            if ('effect' if field=='annotations' else 'on') in row:
                diagnostics.append({'reason':'wrong_semantic_locator_kind','list':field,'index':idx});bad=True;continue
            invalid=next((k for k,v in row.items() if not isinstance(v,str)),None)
            if invalid is not None:
                diagnostics.append({'stage':phase,'list':field,'index':idx,'field_path':invalid,
                    'reason':'invalid_semantic_field_shape','actual_type':type(row[invalid]).__name__})
                bad=True;continue
            revision='ref' in row or 'action' in row
            action=row.get('action','add')
            located=bool(isinstance(row.get(refkey),str) and row[refkey].strip()) if not revision else (
                isinstance(action,str) and action in REVISION_ACTIONS and isinstance(row.get('ref'),str))
            meaning_ok=(revision and action in ('confirm','narrow','withdraw') and 'meaning' not in row or
                        isinstance(row.get('meaning'),str) and row['meaning'] in vocab)
            if not located or not meaning_ok or (action!='confirm' and not (isinstance(row.get('basis'),str) and row['basis'].strip())):
                missing = refkey if not located else 'meaning' if not meaning_ok else 'basis'
                raw_field = row.get(missing)
                diagnostics.append({'reason':'invalid_semantic_row','list':field,'index':idx,'field':missing,
                    'subreason':'field_absent' if raw_field is None else 'invalid_locator' if not located else 'outside_facet_vocabulary' if not meaning_ok else 'missing_source_reason',
                    'actual_type':type(raw_field).__name__,'value_length':len(raw_field) if isinstance(raw_field,str) else None,'value_sha256':digest(raw_field)})
                bad=True;continue
            if row.get('meaning')=='initialization_stage' and not (revision and 'subject' not in row) and not isinstance(row.get('subject'),str):
                actual=row.get('subject')
                diagnostics.append({'reason':'invalid_semantic_row','list':field,'index':idx,'field':'subject',
                    'subreason':'field_absent' if 'subject' not in row else 'wrong_field_type',
                    'actual_type':type(actual).__name__,'value_sha256':digest(actual)})
                bad=True;continue
            # A reply to a shown support can inherit its current role. Its
            # authenticated object and prior fact are checked by the consumer.
            issue=role_error(row,row.get('meaning')) if 'role' in row or not revision else None
            if issue:
                if field=='annotations' and row.get('meaning')=='amount_role' and not revision and not {'scope','subject'} & row.keys():
                    located_amount_reads.append(row[refkey])
                actual=row.get('role')
                diagnostics.append({'reason':'invalid_semantic_row','list':field,'index':idx,
                    'field':'role','subreason':issue,'actual_type':type(actual).__name__,
                    'value_length':len(actual) if isinstance(actual,str) else None,'value_sha256':digest(actual)})
                bad=True;continue
            bound=dict(row);seeds[field].append(bound)
            row_ordinals[(field,id(bound))]=idx
    answers=[]
    for index,row in enumerate(value.get('answers',[]) if isinstance(value.get('answers',[]),list) else []):
        index=row_ordinals.get(('answers',id(row)),index)
        if not isinstance(row,dict) or not all(isinstance(row.get(k),str) and row[k].strip() for k in ('question','answer','basis')):
            diagnostics.append({'answer':index,'reason':'semantic_answer_missing_question_answer_or_basis','original':row});continue
        if phase!='focused_revision' or row['question'] not in sent_questions:
            diagnostics.append({'list':'answers','index':index,'field':'question','reason':'semantic_answer_outside_sent_scope'})
            continue
        answers.append(copy.deepcopy(row))
    issues=[];seen=set()
    for index,item in enumerate(value['issues']):
        index=row_ordinals.get(('issues',id(item)),index)
        if not isinstance(item,dict):diagnostics.append({'item':index,'reason':'issue_not_object'});continue
        shape = issue_shape(item)
        if shape:
            field, value_received = shape
            diagnostics.append({'stage':phase, 'list':'issues', 'index':index,
                'field_path':field, 'actual_type':type(value_received).__name__,
                'reason':'invalid_issue_field_shape', 'subreason':'wrong_field_type'})
            bad=True
            continue
        item={k:v for k,v in item.items() if v is not None}
        claim=item.get('claim');anchors=item.get('anchors',[])
        if isinstance(anchors,str):anchors=[anchors]
        if not isinstance(claim,str) or not claim.strip() or not isinstance(anchors,list) or not (any(isinstance(x,str) and x.strip() for x in anchors) or isinstance(item.get('effect'),str) and item['effect'].strip()):
            diagnostics.append({'item':index,'reason':'missing_claim_or_source_anchor','original':item});continue
        identifier=item.get('id') if isinstance(item.get('id'),str) and item['id'].strip() else ident('issue',[claim,anchors,item.get('effect')])
        if identifier in seen:
            identifier=identifier+'_'+digest([index,item])[:8];diagnostics.append({'item':index,'reason':'duplicate_id_disambiguated'})
        seen.add(identifier)
        issue=copy.deepcopy(item);issue.update(id=identifier,claim=claim.strip(),anchors=[x.strip() for x in anchors if isinstance(x,str) and x.strip()])
        issue['_host_defaulted_fields']=[k for k in ('assessment','category') if k not in item or item.get(k) is None]
        cat=issue.get('category');normalized=category_value(cat,task)
        if normalized!=cat:
            issue['category']=normalized
            issue['_category_normalization']={'original':cat,'normalized':normalized,'basis':'finite task/spelling alias; no inferred financial class'}
        elif normalized is not None and normalized not in ('AC','FCR-TRANSFER','FCR-MINT','FCR-DESTROY','FCR-PAUSE','FCR-FREEZE'):
            diagnostics.append({'item':index,'issue':identifier,'reason':'category_ambiguous_or_outside_supported_task','original_category':cat})
        raw_assessment=issue.get('assessment')
        token=re.sub(r'[\s-]+','_',raw_assessment.strip().lower()) if isinstance(raw_assessment,str) else None
        aliases={'risk':'risk','confirmed_risk':'risk','risk_confirmed':'risk','vulnerable':'risk',
                 'normal':'normal','no_risk':'normal','not_vulnerable':'normal',
                 'investigate':'investigate','uncertain':'investigate','unknown':'investigate'}
        judgment=aliases.get(token);basis='explicit status vocabulary';problem=None
        # Bare "confirmed" is not itself a positive risk judgment. In
        # particular, a risk noun inside a negated sentence is not evidence
        # of affirmative polarity. Only finite explicit affirmative wording
        # is normalized; other prose stays unresolved with its original text.
        # Old confirmations can carry an explicit proposition. Negation of
        # authorization is different from negation of the risk proposition.
        negative_head = re.match(r'^\s*(?:(?:this|that|there)\s+is\s+)?(?:not (?:a |an )?|no )(?:risk|vulnerabilit\w*|unauthorized access)\b',claim,re.I)
        positive_head = re.match(r'^\s*(?:this (?:is|poses|constitutes) (?:a |an )?(?:risk|vulnerability)|(?:the )?(?:caller|spender|requester|actor) (?:gains unauthorized access|lacks (?:applicable )?authorization)|(?:the )?(?:entry|function|operation) (?:does not check|fails to check|omits) (?:the )?(?:applicable|required|holder.s|incumbent.s) authorization)\b',claim,re.I)
        if token=='confirmed':
            if negative_head:judgment='normal'
            elif positive_head and normalized in ('AC','FCR-TRANSFER','FCR-MINT','FCR-DESTROY','FCR-PAUSE','FCR-FREEZE'):judgment='risk'
            else:problem='ambiguous_confirmation_not_a_risk_judgment'
        explicit_false=item.get('is_vulnerable') is False or item.get('risk') is False
        explicit_true=item.get('is_vulnerable') is True or item.get('risk') is True
        if (judgment=='risk' and (negative_head or explicit_false)) or (judgment=='normal' and explicit_true):
            problem='contradictory_explicit_judgment';judgment=None
        if judgment is None:
            judgment='investigate';problem=problem or ('missing_assessment' if raw_assessment is None else 'unknown_assessment_vocabulary')
            diagnostics.append({'item':index,'issue':identifier,'reason':problem,'original_assessment':raw_assessment,
                                'host_unresolved_not_model_choice':True})
        if raw_assessment!=judgment or problem:
            issue['_assessment_normalization']={'original':raw_assessment,'normalized':judgment,'basis':basis if not problem else problem,
                                               'host_unresolved_not_model_choice':bool(problem)}
        issue['assessment']=judgment
        issues.append(issue)
    reviewed=value.get('reviewed',[])
    if not isinstance(reviewed,list):diagnostics.append({'reason':'reviewed_not_list'});reviewed=[]
    declaration=value.get('task_analysis')
    has_reading=(isinstance(declaration,dict) and not ambiguous(declaration)
                 and isinstance(declaration.get('basis'),str) and bool(declaration['basis'].strip())
                 and isinstance(declaration.get('anchors',[]),list)
                 and all(isinstance(a,str) for a in declaration.get('anchors',[])))
    if declaration is not None and not has_reading:
        diagnostics.append({'stage':phase,'field_path':'task_analysis','reason':'invalid_task_reading_shape','actual_type':type(declaration).__name__})
        value.pop('task_analysis',None);bad=True
    empty = not had_content and not recovered and not bad
    kind = 'substantive' if cards or issues or answers or any(seeds.values()) or has_reading else 'explicit_empty' if empty else 'unbound_content' if had_content and not recovered else 'invalid_protocol'
    for row in diagnostics:
        row.setdefault('stage',phase)
        if 'item' in row:row.setdefault('list','issues')
        if 'answer' in row:row.setdefault('list','answers')
    positions={field:[row_ordinals[(field,id(seed))] for seed in entries] for field,entries in seeds.items()}
    return {**seeds,'hypotheses':cards,'located_amount_reads':located_amount_reads,'issues':issues,'answers':answers,'reviewed':[x for x in reviewed if isinstance(x,str)],
            'response_kind':kind,'usable_analysis':kind in ('substantive','explicit_empty'),
            'diagnostics':diagnostics,'row_positions':positions,'recovered_partial_envelope':recovered,'original_envelope':value}

class Session:
    def __init__(self,program,context,out,client):
        self.program,self.context,self.out,self.client=program,context,out,client
        self.attempts=[];self.model_wait_seconds=0.;self.submitted=0
        if hasattr(client,'program_identity') and client.program_identity is None:client.program_identity=program.identity
    def accounting(self):
        if hasattr(self.client,'accounting'):return self.client.accounting()
        return {'real_model_calls':0,'nature':'offline engineering fixture; not a real model experiment'}
    def is_simulated(self):return not bool(getattr(self.client,'live_authorized',False))
    def request(self,*,feedback=None,recovery=False,prepared=None):
        if len(self.attempts)>=self.program.options.attempt_limit:return None
        index=len(self.attempts);messages,manifest=prepared if prepared is not None else self.context.messages(feedback,recovery=recovery)
        if digest(messages)!=manifest['messages_sha256']:raise ValueError('prepared_message_identity_changed')
        row={'index':index,'phase':'protocol_recovery' if recovery else 'initial' if feedback is None else 'focused_revision',
             'messages_sha256':digest(messages),'input_tokens':manifest['input_tokens'],
             'output_limit':self.program.options.output_limit,'actual_model_submissions':0}
        write(self.out/f'request_receipt_{index}.json',{'host_identity':self.program.identity,**body_receipt(messages,'model_request'),'manifest':context_summary(manifest)})
        self.attempts.append(row)
        if manifest['input_tokens']>self.program.options.input_limit:
            row.update(status='not_sent',submission_state='not_dispatched',reason='complete_message_capacity_exceeded');write(self.out/f'attempt_{index}.json',row);return None
        started=time.monotonic()
        try:
            raw,receipt=self.client.call(messages,'semantic_initial' if index==0 else 'semantic_feedback',
              max_tokens=self.program.options.output_limit,thinking=True,reasoning_effort='high',timeout=1800)
            row['response_received']=True
            write(self.out/f'response_digest_{index}.json',{'content_sha256':digest(raw),'body_retained':False});write(self.out/f'receipt_{index}.json',receipt)
            if receipt.get('messages_sha256')!=digest(messages) or receipt.get('response_sha256')!=digest(raw):raise ValueError('bridge_response_identity')
            if receipt.get('program_identity')!=self.program.identity or receipt.get('case_id')!=self.client.case_id:raise ValueError('bridge_program_or_case_identity')
            simulated=receipt.get('simulated')
            if type(simulated)is not bool or not simulated and not getattr(self.client,'live_authorized',False):
                raise ValueError('fresh_runtime_authorization_required')
            row['response_identity_verified']=True
            value=normalize(raw,task=self.program.options.scope,phase=row['phase'],sent_questions=manifest.get('semantic_wire',{}))
            value['origin']='fixture' if simulated else 'verified_service'
            row['response_kind']=value['response_kind'];row['usable']=value['usable_analysis']
            write(self.out/f'normalization_receipt_{index}.json',{'response_kind':value['response_kind'],'normalized_sha256':digest(value),'issues':len(value['issues']),'answers':len(value['answers']),'usable_analysis':value['usable_analysis'],'body_retained':False,
                'envelope_shape':envelope_shape(raw) if not value['usable_analysis'] else None})
            row.update(status='analysis_received' if value['usable_analysis'] else 'protocol_diagnostic',
                       simulated=simulated,usage=receipt.get('usage'),cost_usd=receipt.get('cost_usd'),
                       cost_usd_upper=receipt.get('cost_usd_upper'),service_model=receipt.get('model'),
                       actual_model_submissions=receipt.get('actual_model_submissions',0),
                       normalization_diagnostics=[diagnostic(d) for d in value['diagnostics']])
            return value
        except Exception as error:
            row.update(status='transport_or_identity_error',reason=type(error).__name__,error_sha256=digest(str(error)));return None
        finally:
            if hasattr(self.client,'attempt_record'):
                row['dispatch_accounting']=self.client.attempt_record(index)
                row['actual_model_submissions']=row['dispatch_accounting'].get('actual_model_submissions',0)
            account=row.get('dispatch_accounting') or {}
            # A provider timeout after recording a possible submission is not a confirmed response.
            row['submission_state']=('fixture' if row.get('simulated') or account.get('simulated') else
                'possible' if account.get('state') in ('sent','unknown') and not row.get('response_received') else
                'submitted' if row.get('actual_model_submissions') else 'not_dispatched')
            self.model_wait_seconds+=time.monotonic()-started;write(self.out/f'attempt_{index}.json',row)

```
