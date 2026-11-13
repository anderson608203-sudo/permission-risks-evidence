# 实跑源码文本 · 第 11 页

## file-7ae2c30ebb70af

`source/src/pr_next_joint/investigation/ledger.py` · 原字节 SHA-256 `08e573d64bf5b44bff39cd5b7918678591b49d28867a1a733ec73c50609203d9`

~~~~python
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
            physical_key=(oid,family(cell))
            if temporal and physical_key not in cache:cache[physical_key]=_unit_origin(backend,oid,cell)
            if temporal and not cache[physical_key]:
                backend.__dict__.setdefault('unit_conflicts',{})[ck]={'cell':cell,'source_clock_comparisons':temporal,
                    'semantic_binding':bound['id'],'reason':'semantic amount not independently bound against source time dimension'}
                return None
            return {'kind':'source_bound_semantic_unit','binding':bound}
        original=_unit_origin(backend,oid,cell)
        return dict(original,semantic_conflict=bound) if original else None
    token=(oid,family(cell))
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
    for pid,p in backend.paths(oid):
        for w in p['writes']:
            v=w['value']; args=v.get('args',[])
            if not same_increment(w,cell):continue
            for other,getter,supply in supplies:
                if any(same_increment(sw,supply) and key(sw['value']['args'][1])==key(args[1]) for sw in p['writes']):
                    return {'kind':'source_supply_linked_token_unit','issuance_path':pid,'supply_getter':getter}
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


~~~~

## file-b170caaf9850ee

`source/src/pr_next_joint/investigation/local_properties.py` · 原字节 SHA-256 `0f2c4b8abf9b28e358c4bc9469507dc86e0c73994103b15113c32b9428e17d17`

~~~~python
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
                        effect = _effect(e,fr,lookup)
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
                        from .financial_value import credited_elsewhere, native_settlement
                        paid,settlement=native_settlement(b,e,oid,fr,cell,holder)
                        conditions.append(start-end>credited_elsewhere(b,e,oid,p,fr,cell,holder)+paid)
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

~~~~

## file-8946752535f966

`source/src/pr_next_joint/investigation/policy_binding.py` · 原字节 SHA-256 `2e1d32b6a2f154972c42c450bdcbe5b37be4da9820bbb8361235eeacd9e7d03e`

~~~~python
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
    if kind=='source_grant_issuer':
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
            'acquisition_uses':[],'binding':{'declaration':requirement['declaration'],'frame':requirement['frame'],
            'source':lookup.anchor(lookup.nodes[requirement['declaration']])},'source_requirement':requirement}


def compare_requirement(required,compiled,entry_id,declaration,target):
    """Check independent source facts against the expression consumed by M4."""
    p=compiled.get('predicate') or {}
    binding=compiled.get('binding') or {}
    scope_ok=(entry_id==required['operation'] and target==required['target'] and
              binding.get('declaration')==declaration==required['declaration'] and binding.get('frame')==required['frame'])
    if required['kind']=='source_guarded_eligibility':
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

~~~~

## file-607f6b95bd3fa1

`source/src/pr_next_joint/investigation/prestate.py` · 原字节 SHA-256 `d985f5498edb16ca90e48d4f06b90eb5e07538b8d91f971666a437c01d832239`

~~~~python
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


~~~~
