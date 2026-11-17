# 实际运行源码完整分段

完整文件按原路径列出，哈希指原文件字节。

## source/src/pr_next_joint/investigation/shared_effect_bridge.py

SHA-256 `30ead2c5051213ed45638587b755dcb6d4e64dc85e2191f5e70baba47b5d758a`

```python
"""Read-only joins over applied compiler paths. No task labels enter either join."""
from pr_next_joint.frontend.path_ir import key
from pr_next_joint.frontend.storage import keys, selector_relation
from .dependencies import may_alias
from .summary import holder, local_delta


def authority_effect_links(facts, target, cell):
    """Locate guard readers; equal declarations across frames still need a key binding."""
    deps = facts.summaries.dependencies
    for edge_id in deps.readers.get((target, cell['root']), ()):
        edge = deps.rows[edge_id]
        if edge['kind'] != 'guard' or not may_alias(cell, edge['read']):
            continue
        row = facts.summaries.paths[edge['path']]
        if row['committing'] and (row['ordered_writes'] or row['effects']):
            yield edge, row


def equity_impact_links(backend, oid, row):
    """Final arithmetic deltas in one applied branch. Keep unrelated units separate."""
    from .ledger import unit_origin, native_only_position
    lookup = backend.f.lookup(oid)
    writes = row['ordered_writes']
    moves = []
    for write in writes:
        cell = write['path']
        account = holder(cell, lookup)
        sign, quantity = local_delta(write)
        if not account or not sign or not quantity:
            continue
        if not unit_origin(backend, oid, cell) or native_only_position(backend, oid, cell):
            continue
        moves.append((sign, quantity, cell, account, write['source']))
    return moves


def independent_holder_debit(rules, effect):
    """An arbitrary third-party debit has an independent baseline in the same ledger."""
    from .initial_state import family
    from .ledger import same_unit_transfers
    from .policy_binding import conjuncts
    from .source_opinion import caller_input_conditions

    d = rules.effects[effect]
    oid = d['oid']
    row = rules.f.summaries.paths[d['path']]
    if not row['committing'] or row['effects'] or row['residuals'] or len(row['ordered_writes']) != 2:
        return None
    moves = equity_impact_links(rules.inv.backend, oid, row)
    if len(moves) != 2:
        return None
    debit = next((m for m in moves if m[0] == '-' and key(m[4]) == key(d['where'])), None)
    credit = next((m for m in moves if m[0] == '+'), None)
    if not debit or not credit or debit[3].get('kind') != 'parameter':
        return None
    if credit[3].get('kind') not in ('parameter', 'actual_sender') or key(debit[3]) == key(credit[3]):
        return None
    qty = debit[1]
    if qty.get('kind') != 'parameter' or not qty.get('type', '').startswith('uint'):
        return None
    if key(qty) != key(credit[1]) or selector_relation(debit[2], credit[2]) != 'same_shape':
        return None
    # Only a balance floor or a freely chosen positive quantity is established
    # here. Identity, payment, allowance or time controls require their own check.
    for guard in (g for term in row['guards'] for g in conjuncts(term)):
        args = list(map(key, guard.get('args', ())))
        floor = ((guard.get('op') in ('>', '>=') and args == [key(debit[2]), key(qty)])
                 or (guard.get('op') in ('<', '<=') and args == [key(qty), key(debit[2])]))
        if not floor and not caller_input_conditions([guard]):
            return None
    baselines = same_unit_transfers(rules.f, d['target'], include_checked_arithmetic=True)
    for route in baselines.get(family(debit[2]), ()):
        if route['operation'] == oid:
            continue
        for other in rules.f.summaries.paths[route['path']]['ordered_writes']:
            if key(other['source']) != key(route['source']):
                continue
            sender = holder(other['path'], rules.f.lookup(route['operation']))
            if sender and sender.get('kind') == 'actual_sender':
                return dict(family='holder_disposition', duty='separate_holder_spending_route',
                            path=d['path'], support=route['source'], use=route['operation'])
    return None


def zero_key_spendable(backend, oid, cell):
    """A caller-selected debit can spend a positive zero-key credit in this family."""
    rules = getattr(getattr(backend, 'semantics', None), 'rules', None)
    if rules is None:
        return False
    from .initial_state import family
    target = rules.f.operations[oid]['target']
    stamp = (target, family(cell), rules.epoch)
    cache = backend.__dict__.setdefault('_source_spendable_zero_key', {})
    if stamp not in cache:
        for effect in rules.by_decl.get(rules.obj(target, cell['root']), ()):
            if not rules.remaining():
                return False
            d = rules.effects[effect]
            if selector_relation(d['cell'],cell) != 'same_shape' or local_delta(d['write'])[0] != '-':
                continue
            if independent_holder_debit(rules, effect):
                cache[stamp] = True
                break
        else:
            cache[stamp] = False
    return cache[stamp]


def index_authority_consumers(rules):
    """Use guard dependencies to locate actual consumers of each authority write.

    Source co-occurrence is not a control proof. In particular an office can
    be real yet freely assignable, which affects AC and FCR differently.
    """
    from pr_next_joint.core import digest
    from .roles import effective_roots
    facts = rules.f
    qualified_readers = {}
    links = {}
    for writer, focus in rules.sensitive_effects.items():
        if focus != 'qualification':
            continue
        w = rules.effects[writer]
        if not rules.remaining():
            rules.incomplete.add(w['oid'])
            break
        if 'cell' not in w or rules.overwritten(writer):
            continue
        for edge, branch in authority_effect_links(facts, w['target'], w['cell']):
            if not rules.remaining():
                rules.incomplete.add(w['oid'])
                break
            use = edge['use']
            if use == w['oid']:
                continue
            role = w['cell']['root']
            # A balance floor and a freeze bit are real guard reads too. Only
            # an applied caller qualification links a role writer to a financial
            # use. Other guard reads stay with the ordinary control comparator.
            path_id = (w['target'], branch['path'])
            if path_id not in qualified_readers:
                allowed = facts.lookup(use).nodes.keys()
                qualified_readers[path_id] = set().union(*(
                    effective_roots(guard, allowed) for guard in branch['guards']))
            if role not in qualified_readers[path_id]:
                continue
            for impact in rules.by_operation[use]:
                output = rules.effects[impact]
                if output.get('path') != branch['path'] or 'write' not in output or rules.overwritten(impact):
                    continue
                sign, amount = local_delta(output['write'])
                if not sign or not amount or not holder(output['cell'], facts.lookup(use)):
                    continue
                # The stable ID is shared across tasks. A solver answer,
                # model interpretation, or classification is never an edge.
                uid = digest([facts.bundle['build_id'],w['target'],writer,edge['path'],
                              edge['position'],impact,edge['expression']])
                links[uid] = dict(writer=writer, reader=impact, operation=use,
                    producer=w['oid'], target=w['target'], declaration=role,
                    guard_position=edge['position'], read_path=edge['path'],
                    write_version=w['version'], consumer_version=output['version'],
                    ordered_writer_keys=digest(keys(w['cell'])), ordered_reader_keys=digest(keys(edge['read'])),
                    direction=sign, writer_location=w['where'], reader_location=output['where'],
                    status='actual_guard_read' if not keys(w['cell']) else 'source_read_key_binding_required')
    return links


def financial_refinements(rules):
    """Coalesce role readers at the applied write; ordinary routes retain their own checks."""
    from collections import defaultdict
    from .source_opinion import role_ids
    from .scope_relevance import nonfinancial
    groups = defaultdict(set)
    readers = {link['reader'] for link in rules.authority_bridges.values()}
    for effect in sorted(readers):
        if not rules.remaining():
            break
        d = rules.effects[effect]
        oid = d['oid']
        row = rules.f.summaries.paths[d['path']]
        if not role_ids(rules.inv, oid, row):
            continue
        cell = d['cell']
        if nonfinancial(rules.inv.backend, oid, cell):
            continue
        sign, quantity = local_delta(d['write'])
        account = holder(cell, rules.f.lookup(oid))
        if not account or not quantity:
            continue
        # The privileged role may govern a paid transfer of its own balance.
        # Keep the ordinary reading; this bridge adds no third-party loss there.
        if sign == '-' and account.get('kind') == 'actual_sender':
            continue
        others = [local_delta(write) for write in row['ordered_writes']
                  if selector_relation(cell, write['path']) == 'same_shape']
        if sign == '+':
            if any(direction == '-' for direction, _ in others):
                continue
            categories = ('FCR-MINT',)
        else:
            matched = any(direction == '+' and key(qty) == key(quantity) for direction, qty in others)
            categories = ('FCR-TRANSFER',) if matched else ('FCR-DESTROY', 'FCR-TRANSFER')
        location = d['where']
        for category in categories:
            groups[(oid, category, cell['root'], location['file'], location['start'],
                    location['length'])].add(effect)
    for (oid, category, *_), effects in sorted(groups.items()):
        yield oid, category, effects

```

## source/src/pr_next_joint/investigation/source_opinion.py

SHA-256 `b7623ba0379c6b3b1c560a11d5fe9651387396283a1c1f7446513c7743dbfed8`

```python
"""Scope-limited source opinions consumed by the ordinary property composer.

These records describe a prediction, not the feasibility of a transaction.
External output uses the vocabulary below and compiler locations only.
"""
import re
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, value_type
from .ledger import unit_origin, native_only_position
from .policy_binding import boolean_leaf, conjuncts, mentioned
from .prestate import impossible_role, state_facts
from .roles import path_qualification
from .summary import holder, local_delta
from .contracts import CATEGORIES

EFFECT = {
    "AC": "the policy governing the protected effect",
    "FCR-TRANSFER": "a transfer of another holder's existing rights",
    "FCR-MINT": "a positive new entitlement for a controlled beneficiary",
    "FCR-DESTROY": "an uncompensated loss of another holder's entitlement",
    "FCR-PAUSE": "a common restriction on ordinary outgoing transfers",
    "FCR-FREEZE": "a restriction on the designated holder's outgoing transfer",
}
DETAIL = {
    'untrusted_holder_disposition':'The caller selects another holder and redirects a positive debit. The same ledger independently supports ordinary spending by its holder.',
    'fixed_holder_entitlement':'The source grants the caller one fixed credit and consumes their own non-resettable eligibility for that credit.',
    'holder_own_transfer':'The caller spends their own balance on the same ordinary transfer.',
    'holder_issued_transfer_scope':'This transfer consumes the holder’s same-key grant for this amount. Authority to create such grants is assessed separately.',
    'voluntary_holder_debit':'The caller reduces their own account on this committing path; this does not establish a privileged loss for another holder.',
    "unbacked_source_issuance":"The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.",
    "unqualified_active_termination":"The source governs completion of this active service separately. The current caller can end it before that condition without the governing authority.",
    "governed_completion":"The termination is restricted to the separately governed completed phase or its responsible authority.",
    "applicable_payment_qualification": "The policy permits either the incumbent role or the same entry’s threshold payment to authorize this effect. Every committing branch enforces one of those alternatives.",
    "holder_consent_basis_unresolved": "The holder-issued grant and the final debit use different quantity bases. The applicable consent convention remains unresolved for this use.",
    "source_role_reassignment": "An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification.",
    "applicable_role_guard": "The existing office must authorize the same change under the recorded guard.",
    "self_delegation": "The authority being written belongs to the caller in the source's issuer position.",
    "new_entitlement": "A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary.",
    "existing_rights_moved": "The qualified operation debits another holder and causally credits the same asset without an applicable holder grant.",
    "uncompensated_debit": "The qualified operation reduces another holder's position without a matching credit on this source branch.",
    "intra_ledger_transfer": "The same asset is moved between positions; that movement does not create additional units.",
    "same_position_restored": "The debit is returned to the same position on the applicable branch.",
    "parameter_only": "The source changes configuration without a downstream change to the relevant entitlement.",
    "no_new_controlled_credit": "The credited position is restricted to a fixed independent recipient.",
    "unassessed_role_change": "A change to authority affects a second protected use but has not yet received an applicable policy reading.",
    "unguarded_governed_effect": "A separate entry requires the stated incumbent to govern this same state. The located change has no corresponding guard under the stated policy.",
    "policy_scope_unsubstantiated": "The source identifies the effect, but does not establish the proposed principal as its applicable authority.",
    "guarded_source_effect": "A source guard at the located operation checks the stated incumbent before the effect. The authorization conclusion applies to that operation.",
    "policy_effect_unresolved": "The located effect depends on an unresolved branch, authority version or effect-specific condition.",
    "policy_missing": "The affected effect is locatable, but its intended authority cannot be distinguished from a permitted public use.",
    "conflicting_scoped_meanings": "The same source effect has incompatible applicable interpretations; resolving this meaning can change its judgment.",
    "source_unit_missing": "Whether the account amount represents a financial entitlement depends on an unresolved, source-located use.",
    "scope_missing": "The available source does not distinguish the claimed effect from the applicable normal explanation in this scope.",
    "external_dependency": "A missing implementation or return condition can determine whether this effect commits or has the claimed meaning.",
    "source_context_missing": "A relevant implementation or source region was unavailable for this judgment.",
    "no_effect_in_scope": "The inspected entry has no relevant committing effect for this category.",
    "source_task_reading": "The source opinion and the actual effect directory support a normal reading of the inspected scope.",
    "model_phase_missing": "A usable substantive task opinion was unavailable for this scope.",
    "source_check_excluded": "Source or bounded program evidence excludes the relevant necessary condition in this scope.",
    "program_support": "A scope-matched program check supports this effect under the recorded analysis domain.",
    "source_certificate": "An applicable source deduction supports this policy and effect.",
    "scoped_fee_consent": "The recorded holder-issued amount policy and matching settlement apply to this request and quantity.",
    "productive_outgoing_control": "The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger.",
    "ordinary_paid_credit": "The buyer receives the source-calculated credit for its own payment. This ordinary purchase does not establish a preferential credit under a separate rate change.",
    "nominee_acceptance": "The incumbent alone appoints a candidate, who must personally accept the same office. This judgment covers that handover only.",
    "incoming_only": "The control is applied to the recipient, not to the holder of the debited position.",
    "same_request_bypass": "Another ordinary entry remains available for the same holder, asset and positive transfer request.",
    "partial_quota": "The source restricts transfer size but permits a positive ordinary transfer under the same control.",
    "zero_quantity": "Every relevant credit on this branch is restricted to a zero quantity.",
    "no_debit_in_scope": "The identified operation only credits this financial family; no causal amount use supports the proposed debit.",
    "guarded_state_change": "The located state change is confined to a branch requiring the established role.",
    "covered_holder_grant": "The issuer key belongs to the debited holder and the same spender consumes an allowance covering the actual debit.",
    "scoped_counter": "The committing update records a nonfinancial count. The located use has no independently established entitlement effect.",
    "revised_policy_not_read": "The changed policy or stage has no applicable source reading yet. The prior check concerns a different interpretation.",
    "local_bookkeeping": "The located numerical bookkeeping update has no source-dependent authorization or entitlement use.",
    "debit_without_issuance": "The committed redemption debits existing positions and makes a settlement; no new token entitlement is credited.",
    "core_mismatch": "The interpretation and the underlying source object or condition do not agree.",
    "unrestricted_termination_decision": "The applied entry can end the contract without qualifying the deciding caller. The payout recipient does not authorize that decision.",
    "detached_local_holder_switch": "The applied public outgoing entries do not use this switch to restrict the holder. A getter alone does not restrict spending.",
    "origin_only_decider": "The applied termination condition authenticates the transaction origin. It does not bind the immediate deciding caller to that authority.",
    "unrestricted_issuance_decision": "The applied entry lets a caller choose the amount credited to the bound account without the governing qualification required for this issuance.",
    "scoped_semantic_conflict":"The located duty and the deciding caller conflict at this applied source effect; this is a scoped semantic prediction.",
    "scoped_semantic_normal":"The scoped reading and the actual authorization or ordinary use support this effect.",
    "not_reviewed": "An essential entry in the requested scope was not analyzed.",
}

def opinion(status, reason, locations=()):
    return {"status": status, "reason": reason, "locations": list(locations)}

def describe(category, reason):
    return "Judgment concerns " + EFFECT.get(category, "the stated source effect") + ". " + DETAIL.get(reason, DETAIL["scope_missing"])

def role_ids(inv, oid, row):
    raw=inv.f.paths[row["path"]]["raw"]
    return {role["declaration"] for proof in path_qualification(inv.f,oid,raw) for role in proof["roles"]}

def identity_guard(guard, roles):
    return guard.get("op") == "==" and any(x.get("kind")=="actual_sender" for x in guard.get("args",[])) and any(
        x.get("kind")=="storage" and x["root"] in roles and not x.get("segments") for x in guard.get("args",[]))

def feasible_source_guards(guards):
    from pr_next_joint.frontend.path_ir import conditions_possible
    try:
        return conditions_possible(guards)
    except (ValueError, RecursionError):
        return False

def office_guard(guard, cell):
    """Check whether this declaration is necessary on all disjuncts."""
    from .roles import _roots
    return cell["root"] in _roots(guard,{cell["root"]})

def exception_authority(inv, oid, office, guard):
    """An office can be necessary only while a separately governed restriction is active."""
    args = guard.get('args', [])
    if guard.get('op') not in ('||', 'or') or len(args) != 2:
        return set()
    for exemption, alternative in (args, args[::-1]):
        if not office_guard(exemption, office):
            continue
        switch = alternative['args'][0] if alternative.get('op') == '!' else alternative
        if switch.get('kind') != 'storage' or keys(switch) or value_type(switch, inv.f.lookup(oid)) != 'bool':
            continue
        target = inv.f.operations[oid]['target']
        writers = inv.graph.access.get((target, switch['root']), {}).get('writers', ())
        principal_sets = []
        for writer in writers:
            for branch in inv.f.summaries.rows(writer):
                writes = [w for w in branch['ordered_writes'] if key(w['path']) == key(switch)]
                if not writes:
                    continue
                principals = role_ids(inv, writer, branch)
                if branch['residuals'] or not principals:
                    return set()
                value = writes[-1]['value']
                if value.get('kind') == 'parameter' and value.get('type') == 'bool' or (
                        value.get('kind') == 'literal' and value.get('value') is (alternative.get('op') == '!')):
                    principal_sets.append(principals)
        if principal_sets:
            return set.intersection(*principal_sets)
    return set()


def office_use(inv, oid, cell):
    target=inv.f.operations[oid]["target"]
    from .shared_effect_bridge import authority_effect_links
    for edge, row in authority_effect_links(inv.f, target, cell):
        use = edge['use']
        if use == oid or row['residuals'] or inv.f.operations[use]['generated_getter']:
            continue
        guards = row['guards']
        if any(office_guard(g,cell) or exception_authority(inv,use,cell,g) for g in guards) and feasible_source_guards(guards):
            return use
    return None

def handover(inv,oid,rows):
    """A nomination is local to its incumbent, and acceptance to the nominated caller."""
    from .roles import _role_index
    f=inv.f;target=f.operations[oid]['target'];lk=f.lookup(oid)
    def address_operand(value):
        # A cast to uint160 preserves an address-valued nominee exactly.
        if value.get('kind')=='integer_cast' and value.get('type') in ('uint160','address','address payable'):
            inner=value['input']
            if inner.get('kind')=='storage' and value_type(inner,lk) in ('address','address payable'):return inner
            if inner.get('kind')=='parameter' and lk.nodes.get(inner['id'],{}).get('typeDescriptions',{}).get('typeString') in ('address','address payable'):return inner
        return value
    def nominators(slot,office):
        positive=[]
        for writer in inv.graph.access.get((target,slot['root']),{}).get('writers',()):
            for row in f.summaries.rows(writer):
                for w in row['ordered_writes']:
                    if key(w['path'])!=key(slot) or w['value'].get('kind')=='literal' and w['value'].get('value')==0:continue
                    if row['residuals'] or w['value'].get('kind') not in ('actual_sender','parameter') or not any(office_guard(g,office) for g in row['guards']):return False
                    positive.append(writer)
        return bool(positive)
    for row in rows:
        if row['residuals'] or row['effects'] or not row['ordered_writes']:return None
        # Clearing is part of acceptance only for a slot actually consumed
        # as the source of the incumbent write in this same committing path.
        consumed_slots={key(source) for w in row['ordered_writes'] for source in [address_operand(w['value'])]
                        if source.get('kind')=='storage' and not keys(source)
                        and any(office_guard(g,source) for g in row['guards'])
                        and nominators(source,w['path'])}
        for w in row['ordered_writes']:
            dst=w['path'];v=address_operand(w['value'])
            if keys(dst) or value_type(dst,lk) not in ('address','address payable'):return None
            if v.get('kind')=='literal' and v.get('value')==0 and key(dst) in consumed_slots:continue
            if v.get('kind')=='storage' and key(v) in consumed_slots and nominators(v,dst):continue
            if v.get('kind')=='parameter':
                # The receiver must actually use the nominated slot to become the incumbent.
                if any(key(address_operand(peer['value']))==key(dst) and any(office_guard(g,dst) for g in use['guards'])
                       and not keys(peer['path']) and any(office_guard(g,peer['path']) for g in row['guards']) and nominators(dst,peer['path'])
                       for reader in inv.graph.access.get((target,dst['root']),{}).get('readers',())
                       for use in f.summaries.rows(reader) for peer in use['ordered_writes']):continue
            return None
    if rows and any(w['value'].get('kind')!='literal' for r in rows for w in r['ordered_writes']):
        return opinion('normal','nominee_acceptance',[f.operations[oid]['source']])
    return None


def normal_authorization_reading(inv,q,rows):
    """Check a source-bound normal precondition only on all claimed committing branches."""
    oid=inv.root(q);prop=q.get('property') or {};cat=prop.get('category')
    if not rows or any(r['residuals'] for r in rows):return None
    role_only=cat=='AC' and q['current']['assessment']=='normal'
    if role_only:
        expected=(prop.get('expected_authorization') or {}).get('compiled_authorization') or {}
        if expected.get('competing_interpretations'):return None
        subj=expected.get('subject') or {}
        if q['current'].get('_opinion_message'):
            from pr_next_joint.frontend.path_ir import conditions_possible
            if not expected.get('predicate') or expected.get('necessary_only') or (prop.get('expected_authorization') or {}).get('unresolved_relations'):
                return None
            try:
                if any(conditions_possible(r['guards'], expected['predicate']) for r in rows):
                    return None
            except (ValueError, RecursionError):
                return None
        if subj.get('kind')=='storage' and all(subj['root'] in role_ids(inv,oid,r) for r in rows):
            return opinion('normal','applicable_role_guard',[inv.f.operations[oid]['source']])
    return None

def caller_input_conditions(guards, phase_guard=None):
    """A caller can supply a positive unsigned input; this restriction conveys no office or grant."""
    for term in guards:
        if phase_guard is not None and key(term)==phase_guard:continue
        for atom in conjuncts(term):
            op=atom.get('op');args=atom.get('args',())
            if len(args)!=2:return False
            parameter,bound=args
            if parameter.get('kind')=='literal':
                parameter,bound=bound,parameter
                op={'<':'>','<=':'>=','!=':'!='}.get(op)
            if (parameter.get('kind')!='parameter' or not parameter.get('type','').startswith('uint')
                    or bound.get('kind')!='literal' or type(bound.get('value')) is not int):
                return False
            if (op,bound['value']) not in (('>',0),('!=',0),('>=',0),('>=',1)):return False
    return True


def business_arm(term, lookup):
    """A sufficient non-authorizing alternative. The complete guard is checked separately."""
    from pr_next_joint.frontend.path_ir import op, lit
    if term.get('op') in ('or', '||', 'and', '&&'):
        return op(term['op'], *(business_arm(v, lookup) for v in term['args']))
    for node in walk(term):
        kind = node.get('kind')
        if kind == 'storage':
            if node.get('segments') or value_type(node, lookup) != 'bool':
                return lit(False)
        elif kind == 'environment':
            if node.get('field') not in ('number', 'timestamp'):
                return lit(False)
        elif kind not in (None, 'literal', 'op', 'parameter', 'block_number', 'block_timestamp', 'integer_cast'):
            return lit(False)
    return term


def committing_control(inv, d, candidate, row):
    """Test a caller-controlled effect on the original success frame in the AC domain."""
    from pr_next_joint.verification.source_worlds import frame, encode_frame
    from pr_next_joint.verification.sequence import qualify, read
    from pr_next_joint.verification.program_encoding import MechanismEncoder
    from pr_next_joint.verification.expressions import Unsupported
    from .initial_state import initial_for_lookup
    oid, pid = d['oid'], row['path']
    lookup = inv.f.lookup(oid)
    family = candidate['family']
    cache = inv.backend.__dict__.setdefault('_committing_controls', {})
    token = (oid, pid, key(d['where']), family, candidate['duty'])
    if token in cache:
        return cache[token]
    if not row['committing'] or row['residuals'] or inv.backend.remaining() <= 0:
        return None
    try:
        e = MechanismEncoder(lookup)
        terms = []
        quantities = []
        # Two free choices on identical storage and business circumstances
        # distinguish selectable issuance from a fixed allotment.
        for slot in range(2 if family == 'unbacked_issuance' else 1):
            fr = frame(inv.f, oid, pid, slot)
            sym = lambda term: e.expr(qualify(term, slot))
            actor = e.expr(fr['caller'])
            terms.extend((encode_frame(e, fr), actor != 0))
            for guard in row['guards']:
                arm = business_arm(guard, lookup)
                terms.append(sym(arm))
                # A global phase can be witnessed at deployment when its
                # initializer is the Solidity default. Never invent a reachable phase.
                for cell in selectors(arm):
                    initial = (initial_for_lookup(lookup) or {}).get('declarations', {}).get(cell['root'], {})
                    if not initial:
                        return None
                    if not initial['explicit_initializer'] and not initial['constructor_writes']:
                        terms.append(sym(cell) == False)
                    elif not state_facts(lookup).get(cell['root'], {}).get('encoded'):
                        return None
            if 'cell' in d:
                cell = qualify(d['cell'], slot)
                before = e.expr(cell)
                after = e.expr(read(cell, fr['writes'], lookup))
                terms.append(after != before)
                if family == 'unbacked_issuance':
                    terms.append(after > before)
                    quantities.append(after - before)
                    quantity_parameters = {n['id'] for n in walk(local_delta(d['write'])[1]) if n.get('kind') == 'parameter'}
                    if slot:
                        terms.append(actor == e.expr(qualify({'kind':'actual_sender'}, 0)))
                        for node in walk([row['guards'], d['cell'], local_delta(d['write'])[1]]):
                            if (node.get('kind') in ('environment','block_number','block_timestamp') or
                                node.get('kind') == 'parameter' and node['id'] not in quantity_parameters):
                                terms.append(sym(node) == e.expr(qualify(node, 0)))
                elif candidate['duty'] == 'holder_issued_grant':
                    idx = keys(d['cell'])
                    issuer = candidate['issuer_key']
                    terms.extend((sym(idx[issuer]) != actor, sym(idx[1-issuer]) == actor, after > 0))
                elif candidate['duty'] == 'guarded_downstream_use':
                    if keys(d['cell']):
                        terms.append(sym(keys(d['cell'])[0]) == actor)
                    else:
                        terms.append(after == actor)
        if quantities:
            terms.append(quantities[0] != quantities[1])
        result = inv.backend._query(e, e.z.And(*terms), 'source_committing_untrusted_control',
                                    dict(operation=oid, use_path=pid, category='AC', effect_location=d['where'], duty=candidate['duty']))
        confirmed = result['id'] if result.get('bounded_condition_confirmed') else None
        cache[token] = confirmed
        return confirmed
    except (Unsupported, TimeoutError):
        return None


def replacement_status(inv, effect):
    row = inv.f.summaries.paths[effect['path']]
    if not row['committing'] or not feasible_source_guards(row['guards']):
        return 'open'
    if any(office_guard(g, effect['cell']) for g in row['guards']):
        return 'normal'
    candidate = dict(family='grant_then_use', duty='guarded_downstream_use')
    return 'risk' if committing_control(inv, effect, candidate, row) else 'open'


def source_duty_opinion(inv, q):
    """Apply only the relation bound to this committing source occurrence."""
    from .ledger import unit_origin
    rules=inv.semantics.rules
    for effect in q['current'].get('_scope_effects',()):
        candidate=getattr(rules,'source_duties',{}).get(effect)
        if not candidate:continue
        d=rules.effects[effect];oid=d['oid'];pid=candidate['path'];row=inv.f.summaries.paths[pid]
        if any(g['kind']=='dependent_source_expression_limit' for g in inv.f.operations[oid]['gaps']):continue
        if blocked_positive(inv,q,pid,'AC') or not feasible_source_guards(row['guards']):continue
        status='open'; why='policy_missing'; proof=None
        if candidate['family']=='unbacked_issuance':
            qty=local_delta(d['write'])[1]
            from pr_next_joint.frontend.path_ir import op,lit
            if ((proof := committing_control(inv,d,candidate,row)) and sourced_quantity(qty,inv.f.lookup(oid))
                    and feasible_source_guards([*row['guards'],op('>',qty,lit(0))]) and unit_origin(inv.backend,oid,d['cell'])):
                status,why='risk','unbacked_source_issuance'
        elif candidate['duty']=='separate_holder_spending_route':
            qty = local_delta(d['write'])[1]
            from pr_next_joint.frontend.path_ir import op, lit
            if feasible_source_guards([*row['guards'], op('>', qty, lit(0))]):
                status, why = 'risk', 'untrusted_holder_disposition'
        elif candidate['duty']=='holder_issued_grant':
            if candidate['issuer']=='actual_sender':
                status,why='normal','self_delegation'
            elif candidate['issuer']=='parameter' and (proof := committing_control(inv,d,candidate,row)):
                status,why='risk','source_role_reassignment'
        elif candidate['duty']=='guarded_downstream_use':
            handoff=handover(inv,oid,[row])
            if handoff:return handoff
            if any(office_guard(g,d['cell']) for g in row['guards']):
                status='normal'
            elif (proof := committing_control(inv,d,candidate,row)):
                status='risk'
            why='source_role_reassignment' if status=='risk' else 'applicable_role_guard'
        elif candidate['family']=='managed_phase':
            if (proof := committing_control(inv,d,candidate,row)):
                status,why='risk','unguarded_governed_effect'
        elif candidate['family']=='managed_lifecycle':
            if candidate['controller_guarded'] or candidate['phase']=='completed':
                status,why='normal','governed_completion'
            elif candidate.get('phase_guard') and (proof := committing_control(inv,d,candidate,row)):
                status,why='risk','unqualified_active_termination'
        if status=='open':continue
        ans=opinion(status,why,[d['where']])
        ans['source_relation']={'family':candidate['family'],'duty':candidate['duty'],'support_location':candidate['support']}
        if proof:ans['source_relation']['committing_check']=proof
        if candidate.get('use') and candidate['family'] != 'holder_disposition':
            ans['protected_use']=inv.f.operations[candidate['use']]['source']
        if status=='normal':ans['same_scope_authorized']=True
        return ans
    return None


def paid_service_reading(inv,q,rows):
    """Read an explicit sufficient payment opinion against each actual committing arm."""
    from .policy_binding import payment_policy
    oid=inv.root(q);item=q['current'];lk=inv.f.lookup(oid)
    if item.get('_host_source_question') or not isinstance(item.get('claim'),str):return None
    if not rows or any(r['residuals'] or r['effects'] for r in rows):return None
    where={key(w['source']):w['source'] for r in rows for w in r['ordered_writes']}
    if len(where)!=1:return None
    text=item.get('policy_basis') or item['claim']; entry=inv.f.operations[oid]['function'].split('(')[0]
    scopes=set(lk.contract_node.get('linearizedBaseContracts',[]))
    decls=[node for node in lk.decls.values() if node.get('scope') in scopes and node.get('stateVariable')
           and node.get('typeDescriptions',{}).get('typeString') in ('address','address payable') and node.get('name')]
    def paid(g):
        terms=g.get('args',())
        if len(terms)!=2 or g.get('op') not in ('>','>=','<','<='):return False
        v,threshold=terms if g['op'] in ('>','>=') else reversed(terms)
        return (v.get('kind')=='transaction_value' and threshold.get('kind')=='literal' and type(threshold['value']) is int
                and (threshold['value']>0 or threshold['value']==0 and g['op'] in ('>','<')))
    for role in decls or [{'id':None,'name':'unbound'}]:
        status=payment_policy(text,role['name'],[entry])
        if status!='independent':continue
        names_role=mentioned(text,role['name'])
        def entitled(g):
            if paid(g):return True
            if g.get('op') in ('||','or'):
                return all(paid(arm) or names_role and identity_guard(arm,{role['id']}) for arm in g.get('args',()))
            return names_role and identity_guard(g,{role['id']})
        if all(any(entitled(term) for g in r['guards'] for term in conjuncts(g)) for r in rows if r['committing']):
            result=opinion('normal','applicable_payment_qualification',where.values())
            result['same_scope_authorized']=True
            return result
    return None


def fixed_holder_entitlement(inv,oid,rows):
    """One fixed credit per caller with a consumed, non-resettable eligibility flag."""
    lk=inv.f.lookup(oid);locations=[]
    for row in rows:
        if not row['committing']:continue
        if row['effects'] or row['residuals']:return None
        writes=row['ordered_writes']; credits=[w for w in writes if holder(w['path'],lk) and local_delta(w)[0]=='+']
        if len(credits)!=1:return None
        credit=credits[0];qty=local_delta(credit)[1]
        if not qty or qty.get('kind')!='literal' or type(qty.get('value')) is not int or qty['value']<=0:return None
        if holder(credit['path'],lk)!={'kind':'actual_sender'}:return None
        flag=next((g['args'][0] for t in row['guards'] for g in conjuncts(t)
                   if g.get('op')=='!' and len(g.get('args',()))==1 and
                   g['args'][0].get('kind')=='storage' and keys(g['args'][0])==[{'kind':'actual_sender'}]),None)
        if not flag or not any(key(w['path'])==key(flag) and w['value'].get('value') is True for w in writes):return None
        if any(w['raw']['value'].get('value') is not True for w in inv.f.writes.values()
               if inv.f.operations[w['operation']]['target']==inv.f.operations[oid]['target'] and w['raw']['path']['root']==flag['root']):return None
        if any(w is not credit and key(w['path'])!=key(flag) and (keys(w['path']) or local_delta(w)[0]!='+' or key(local_delta(w)[1])!=key(qty))
               for w in writes):return None
        locations.append(credit['source'])
    if not locations:return None
    result=opinion('normal','fixed_holder_entitlement',locations);result['same_scope_authorized']=True
    return result


def ordinary_transfer_reading(inv,q,rows):
    from .ledger import grant_for
    from pr_next_joint.frontend.storage import selector_relation
    if not rows:return None
    oid=inv.root(q); lk=inv.f.lookup(oid); modes=set();sites=[]
    for r in rows:
        if not r['committing']:continue
        if r['residuals'] or r['effects']:return None
        moves=[(w,*local_delta(w)) for w in r['ordered_writes']]
        pairs=[(w,n,v) for w,sign,n in moves if sign=='-' and holder(w['path'],lk)
               for v,vs,vn in moves if vs=='+' and selector_relation(v['path'],w['path'])=='same_shape'
               and key(n)==key(vn) and key(v['path'])!=key(w['path'])]
        if len(pairs)!=1:return None
        w,n,v=pairs[0];who=holder(w['path'],lk)
        if not unit_origin(inv.backend,oid,w['path']):return None
        normal='holder_own_transfer'
        allowed={key(w['path']),key(v['path'])}
        if who.get('kind')!='actual_sender':
            grant=grant_for(inv.backend,oid,inv.f.paths[r['path']]['raw'],w['path'])
            if not grant:return None
            if not any(key(a['path'])==key(grant) and s=='-' and key(qty)==key(n) for a,s,qty in moves):return None
            if not any(g.get('op') in ('>=','>') and [key(x) for x in g.get('args',[])]==[key(grant),key(n)]
                       for term in r['guards'] for g in conjuncts(term)):return None
            allowed.add(key(grant));normal='holder_issued_transfer_scope'
        if any(key(a['path']) not in allowed for a,_,_ in moves):return None
        sites.append(w['source']);modes.add(normal)
    if len(modes)!=1:return None
    result=opinion('normal',modes.pop(),sites); result['same_scope_authorized']=True
    return result


def ac_opinion(inv, q, rows):
    oid=inv.root(q); item=q["current"]; lookup=inv.f.lookup(oid)
    policy=(q.get("property") or {}).get("expected_authorization") or {}
    hypothesis=policy.get("text") or policy.get("basis") or item.get("claim","")
    rules=getattr(inv.semantics,'rules',None)
    if rules:
        office=rules.office_opinion(q,rows)
        if office:return office
    pred=policy.get('compiled_authorization') or {}
    paid=pred.get('source_requirement') or {}
    if paid.get('kind')=='source_role_payment_policy' and pred.get('source_ir_check',{}).get('matches') and rows:
        # Static implication uses every committing path; a distinct branch cannot be
        # classified normal merely because the disjunction was found once.
        from pr_next_joint.frontend.path_ir import conditions_possible
        if paid['permits_payment'] and not inv.f.operations[oid]['gaps'] and all(
                not r['residuals'] and not conditions_possible(r['guards'],pred['predicate']) for r in rows):
            return opinion('normal','applicable_payment_qualification',[inv.f.operations[oid]['source']])
        if pred.get('necessary_only'):
            # Satisfying a known prerequisite does not establish complete authorization.
            # A scoped violation can still be confirmed by the ordinary program check.
            return opinion('open','policy_missing',[inv.f.operations[oid]['source']])
    if item.get('_host_source_question') or not policy.get('text') and not policy.get('basis'):
        normal=ordinary_transfer_reading(inv,q,rows) or fixed_holder_entitlement(inv,oid,rows)
        if normal:return normal
    transition=handover(inv,oid,rows)
    if transition:return transition
    focused=statement_opinion(inv,q,rows)
    if focused:return focused
    normal=normal_authorization_reading(inv,q,rows)
    if normal:return normal
    for row in rows:
        if row["residuals"] or row["effects"]:continue
        guards=[g for term in row["guards"] for g in conjuncts(term)]
        for w in row["ordered_writes"]:
            cell=w["path"]
            if keys(cell) or value_type(cell,lookup) not in ("address","address payable"):continue
            if w["value"].get("kind") not in ("actual_sender","parameter"):continue
            use=office_use(inv,oid,cell)
            if not use:continue
            # Existing explicit policy bindings can be used even when initialization itself is unavailable.
            compiled=policy.get('compiled_authorization') or {}
            subject=compiled.get('subject') or {}
            if (not guards and subject.get('root')==cell['root'] and policy.get('polarity')=='asserted'
                    and not item.get('_host_source_question') and item.get('assessment')!='normal'
                    and not blocked_positive(inv,q,row['path'],'AC')):
                return opinion("risk","source_role_reassignment",[w["source"]])
    if not item.get('_opinion_message') and rows and all(role_ids(inv,oid,r) for r in rows) and item["assessment"]=="normal":
        # A guard is a normal alternative only for the role actually asserted.
        roles=set.intersection(*(role_ids(inv,oid,r) for r in rows))
        if any(mentioned(hypothesis,lookup.nodes[rid].get("name")) for rid in roles):
            return opinion("normal","applicable_role_guard",[inv.f.operations[oid]["source"]])
    return opinion("open","policy_missing")

def blocked_positive(inv, q, path, cat):
    """Check existing local contradictions before extending a source opinion."""
    prop=q.get("property") or {}
    from .property_model import validation_key
    for eid in q["evidence"]:
        ev=inv.evidence[eid]
        if ev.get("source_identity")!=inv.f.identity:continue
        if ev.get("kind")=="source_inspection" and ev.get("operation")==inv.root(q):
            if path in ev.get("unknown_guard_paths",[]) or path in ev.get("credential_paths",[]):return True
        if not prop or ev.get("property_identity")!=prop.get("id") and ev.get("property_validation_key")!=validation_key(prop):continue
        if any(r.get("result")=="source_ir_mismatch" and r.get("path") in (None,path) for r in ev.get("amount_correspondence",[])):return True
        for probe in ev.get("queries",[]):
            d=probe.get("details",{})
            if probe.get("answer")!="unsat" or d.get("use_path")!=path or not d.get("property_validated"):continue
            if probe.get("label") in ("direct_effect","authorization_violation"):
                return True
            if probe.get("label")=="local_premises_feasible" and ev.get("observed_measure")=="direct_effect" and (
                    probe.get("exclusion_certificate",{}).get("excludes_only_this_formula")
                    or d.get("prestate",{}).get("global_reachability_exhausted")):
                return True
    return False

def boolean_input_branch(guard):
    # A free boolean argument picks the branch. Guards on persistent state,
    # external returns and derived booleans retain their other dependencies.
    if guard.get('op') in ('!','not') and len(guard.get('args',[]))==1:
        guard=guard['args'][0]
    return guard.get('kind')=='parameter' and guard.get('type')=='bool'


def simple_guard(g,roles,beneficiary=None):
    if identity_guard(g,roles) or g=={"kind":"literal","value":True}:return True
    if g.get("kind")=="storage" and g.get("root") in roles and keys(g)==[{"kind":"actual_sender"}]:return True
    args=g.get("args",[])
    return (beneficiary is not None and len(args)==2 and g.get("op")=="!=" and
            any(key(x)==key(beneficiary) for x in args) and any(x.get("kind")=="literal" and x.get("value") in (0,"0") for x in args))

def block_opinion(inv,q,rows):
    """Scope a blocking claim to actual outgoing holders, units and productive alternatives."""
    from .comparison import ledger_routes
    root=inv.root(q);cat=(q.get('property') or {}).get('category') or q['current'].get('category');target=inv.f.operations[root]["target"]
    writes=[w for r in rows for w in r["ordered_writes"] if role_ids(inv,root,r)]
    controls={w["path"]["root"] for w in writes}
    if not controls:return None
    if cat=='FCR-FREEZE':
        from .scope_relevance import detached_holder_switch
        closed=detached_holder_switch(inv,root)
        if closed:return opinion('excluded',closed['reason'],closed['locations'])
    for label in q.get('evidence',()):
        check=inv.evidence[label];direct=check.get('source_control_result')
        if (direct and check.get('change')==root and check.get('property_identity')==(q.get('property') or {}).get('id')
                and not blocked_positive(inv,q,direct['controller_path'],cat)):
            return direct
    routes=ledger_routes(inv.backend,target)
    observed=[]
    for route in routes:
        oid=route["operation"];pid=route["path"];p=inv.f.paths[pid]["raw"]
        if path_qualification(inv.f,oid,p):continue
        src=holder(route["debit"],inv.f.lookup(oid));dst=holder(route["credit"],inv.f.lookup(oid))
        if not src or not dst:continue
        touched=[s for s in selectors(p["guards"]) if s["root"] in controls]
        same=[x for x in touched if keys(x) and key(keys(x)[0])==key(src)]
        receive=[x for x in touched if keys(x) and key(keys(x)[0])==key(dst) and key(src)!=key(dst)]
        moves=[local_delta(w) for w in p["writes"] if key(w["path"])==key(route["debit"])]
        quantity=next((val for sign,val in moves if sign=="-"),None)
        credited=[local_delta(w) for w in p["writes"] if key(w["path"])==key(route["credit"])]
        plain=bool(quantity and any(s=="+" and key(v)==key(quantity) for s,v in credited)
                   and len(p["writes"])==2 and not p.get("sensitive_effects") and not p.get("issues") and not p.get("evaluation_gaps"))
        observed.append((route,src,dst,touched,same,receive,p,quantity,plain))
    affected=[r for r in observed if r[3]]
    if not affected:return None
    locations=[w["source"] for w in writes]
    if cat=="FCR-FREEZE" and all(r[5] and len(r[3])==len(r[5]) and not r[4] for r in affected):
        # Other paths using the same table through a debit or a dependent value invalidate this exclusion.
        if all(r[8] and inv.backend.complete(r[0]["operation"]) for r in affected) and not (q.get('property') or {}).get('value_dependence',{}).get('value_uses'):
            return opinion("normal","incoming_only",locations)
    if cat=="FCR-PAUSE":
        for route,src,dst,cells,_,_,p,qty,plain in affected:
            if not plain:continue
            for alt,asrc,adst,acells,_,_,ap,aqty,aplain in observed:
                if not aplain or acells or ap["guards"] or not aqty or not qty:continue
                # Both implement the same free ordinary sender-to-recipient request,
                # rather than the mere existence of some other successful action.
                if (alt["debit"]["root"]==route["debit"]["root"] and src.get("kind")==asrc.get("kind")=="actual_sender"
                        and dst.get("kind")==adst.get("kind")=="parameter" and qty.get("kind")==aqty.get("kind")=="parameter"
                        and inv.f.operations[alt["operation"]]["target"]==target):
                    if all(a[0]["debit"]["root"]==route["debit"]["root"] for a in affected):
                        return opinion("normal","same_request_bypass",locations)
    # A nonzero quota can bind a quantity but does not establish loss of every positive use.
    if cat in ("FCR-PAUSE","FCR-FREEZE"):
        def positive_quota(row):
            route,src,dst,cells,_,_,path,qty,plain=row
            gs=[g for v in path["guards"] for g in conjuncts(v)]
            if not plain or len(gs)!=1 or len(cells)!=1 or not qty:return False
            g=gs[0]; args=g.get("args",[])
            if not (g.get("op")=="<=" and len(args)==2 and key(args[0])==key(qty) and key(args[1])==key(cells[0])):return False
            setters=[(w,r) for r in rows for w in r["ordered_writes"] if w["path"]["root"]==cells[0]["root"]]
            return bool(setters) and all(any(term.get("op")==">" and key(term["args"][0])==key(w["value"])
                and term["args"][1].get("value")==0 for v in r["guards"] for term in conjuncts(v)) for w,r in setters)
        if all(positive_quota(r) for r in affected):return opinion("normal","partial_quota",locations)
    return None

def quantity_forced_zero(guards,qty,lookup):
    if not qty:return False
    fixed=state_facts(lookup)
    for g in guards:
        if g.get("op") not in ("==","<="):continue
        a,b=g["args"]
        if g["op"]=="==" and key(b)==key(qty):a,b=b,a
        if key(a)!=key(qty):continue
        if b.get("kind")=="literal" and b.get("value")==0:return True
        if b.get("kind")=="storage" and not keys(b) and fixed.get(b["root"],{}).get("encoded") and fixed[b["root"]].get("value")==0:return True
    return False

def paired_reading(inv,q,rows):
    """A source-backed normal reading of the amount norm, scoped to this debit and use."""
    prop=q.get('property') or {};cat=prop.get('category')
    if cat not in ('FCR-TRANSFER','FCR-DESTROY'):return None
    consents=prop.get('financial_consents',{})
    for use,meaning in consents.items():
        if use!=inv.root(q) or meaning.get('meaning')!='net_request_with_fee':continue
        matching=[v for v in q['evidence'] if inv.evidence[v].get('property_identity')==prop['id']
                  and inv.evidence[v].get('observe')==use]
        normal=any(inv.evidence[v].get('property_excluded') for v in matching)
        if normal:return opinion('normal','scoped_fee_consent',[inv.f.operations[use]['source']])
    return None

def covered_delegation(inv,oid,rows):
    from .ledger import grant_for
    from .key_roles import relation
    from pr_next_joint.frontend.storage import selector_relation
    lookup=inv.f.lookup(oid);found=False
    for row in rows:
        if row['residuals'] or row['effects']:return False
        if not row['ordered_writes']:continue
        authorized_path=False
        path=inv.f.paths[row['path']]['raw']
        for w in row['ordered_writes']:
            cell=w['path'];sign,amount=local_delta(w)
            if sign!='-' or holder(cell,lookup) is None or relation(cell,lookup):continue
            # A transfer grant covers movement of the same quantity in this ledger.
            # A stand-alone burn or a debit with another destination still needs its own policy.
            grant=grant_for(inv.backend,oid,path,cell)
            if grant is None:return False
            credits=[v for v in row['ordered_writes'] if selector_relation(v['path'],cell)=='same_shape' and key(v['path'])!=key(cell) and local_delta(v)[0]=='+' and key(local_delta(v)[1])==key(amount)]
            if len(credits)!=1 or any(key(v['path']) not in {key(cell),key(grant),key(credits[0]['path'])} for v in row['ordered_writes']):return False
            if len(row['ordered_writes'])!=3:return False
            # The source-issued bound must cover this debit and be consumed for the same requester.
            limits=[g for guard in row['guards'] for g in conjuncts(guard)]
            if not any(g.get('op') in ('>=','>') and list(map(key,g.get('args',[])))==[key(grant),key(amount)] or
                       g.get('op') in ('<=','<') and list(map(key,g.get('args',[])))==[key(amount),key(grant)] for g in limits):return False
            if not any(key(v['path'])==key(grant) and local_delta(v)[0]=='-' and key(local_delta(v)[1])==key(amount) for v in row['ordered_writes']):return False
            if sum(1 for v in row['ordered_writes'] if key(v['path'])==key(cell) and local_delta(v)[0]=='-')!=1:return False
            roles=relation(grant,lookup)
            if not roles:return False
            for other in inv.f.writes.values():
                if inv.f.operations[other['operation']]['target']!=inv.f.operations[oid]['target']:continue
                otherw=other['raw'];dst=otherw['path']
                if selector_relation(dst,grant)!='same_shape':continue
                index=keys(dst)
                if len(index)!=2:return False
                if index[roles['holder_key']].get('kind')!='actual_sender' and local_delta(otherw)[0]!='-':return False
            authorized_path=True
        if not authorized_path:return False
        found=True
    return found


def sourced_quantity(term,lookup):
    if not isinstance(term,dict):return False
    kind=term.get('kind')
    if kind=='literal':return type(term.get('value')) is int and term['value']>0
    if kind in ('parameter','storage'):
        return str(term.get('type') or (value_type(term,lookup) if kind=='storage' else '') or '').startswith('uint')
    # Identical subtraction, division by zero and arbitrary inequalities do not
    # establish positive capacity merely by syntax. Keep them with the backend.
    if term.get('op') in ('+','*'):
        return len(term.get('args',()))==2 and all(sourced_quantity(v,lookup) for v in term['args'])
    return False

def paid_credit(inv,oid,row):
    """A caller's proportional purchase is one use; rate changes are different effects."""
    if role_ids(inv,oid,row) or row['effects'] or row['residuals']:return None
    positions=[w for w in row['ordered_writes'] if holder(w['path'],inv.f.lookup(oid)) is not None]
    if len(positions)!=1:return None
    for w in positions:
        cell=w['path'];buyer=holder(cell,inv.f.lookup(oid));sign,qty=local_delta(w)
        if not buyer or buyer.get('kind')!='actual_sender' or sign!='+' or not unit_origin(inv.backend,oid,cell):continue
        if not qty or qty.get('op')!='*':continue
        terms=qty.get('args',[])
        if len(terms)!=2 or not any(v.get('kind')=='transaction_value' for v in terms):continue
        price=next((v for v in terms if v.get('kind') in ('literal','storage') and not keys(v)),None)
        if not price:continue
        if not any(g.get('op') in ('!','!=','>') and any(v.get('kind')=='transaction_value' for v in walk(g)) and
                   any(v.get('kind')=='literal' and v.get('value')==0 for v in walk(g)) for g in row['guards']):continue
        return w
    return None


def financial_opinion(inv,q,rows):
    oid=inv.root(q);item=q["current"];prop=q.get('property') or {};cat=prop.get('category') or item.get('category')
    loc=inv.f.operations[oid]["source"];lookup=inv.f.lookup(oid)
    if cat=='FCR-MINT' and rows:
        purchases=[paid_credit(inv,oid,row) for row in rows]
        if all(purchases) and all(sum(1 for w in r['ordered_writes'] if holder(w['path'],lookup) and local_delta(w)[0]=='+')==1 for r in rows):
            return opinion('normal','ordinary_paid_credit',[purchases[0]['source']])
    if cat=='FCR-DESTROY':
        from .financial_value import scoped_final_debit
        consent=scoped_final_debit(inv,q,rows)
        if consent:return consent
    if impossible_role(inv,oid):return opinion("excluded","source_check_excluded",[loc])
    if cat in ("FCR-FREEZE","FCR-PAUSE"):
        scoped=block_opinion(inv,q,rows)
        if scoped:return scoped
    if cat=='FCR-TRANSFER' and covered_delegation(inv,oid,rows):
        return opinion('excluded','covered_holder_grant',[loc])
    specific=paired_reading(inv,q,rows)
    if specific:return specific
    structural=[]; uncertain=False
    for row in rows:
        roles=role_ids(inv,oid,row)
        from .shared_effect_bridge import equity_impact_links
        moves = equity_impact_links(inv.backend, oid, row)
        if not moves:
            if row["effects"] or row["residuals"]:uncertain=True
            continue
        guards=[g for term in row["guards"] for g in conjuncts(term)]
        for sign,qty,cell,account,src in moves:
            # Pair by the declaration AND projection. A change in another unit is not compensation.
            from pr_next_joint.frontend.storage import selector_relation
            opposite=[m for m in moves if m[0]!=sign and selector_relation(cell,m[2])=="same_shape"]
            matched=[m for m in opposite if key(m[1])==key(qty)]
            exact=len([m for m in moves if selector_relation(m[2],cell)=="same_shape"])==2 and len(matched)==1
            owned=account.get("kind")=="actual_sender"
            selectable=account.get("kind")=="parameter" and account.get("type") in ("address","address payable")
            simple_path=all(simple_guard(g,roles,account) for g in guards)
            # Extra source conditions must leave a positive quantity feasible.
            # Complex/external conditions continue through the bounded checker.
            from pr_next_joint.frontend.path_ir import op,lit
            positive_amount=sourced_quantity(qty,lookup) and feasible_source_guards(guards+[op('>',qty,lit(0))])
            ordinary_guards=all(simple_guard(g,roles,account) or
                g.get('op') in ('>','>=','!=','<','<=','==') and all(n.get('kind') not in ('storage','unknown','external_return','credential_recovery')
                for n in walk(g)) for g in guards)
            uncomplicated=not blocked_positive(inv,q,row["path"],cat) and not row["residuals"] and not row["effects"] and (
                simple_path or ordinary_guards or all(simple_guard(g,roles,account) or boolean_input_branch(g) for g in guards))
            if exact and sign=='-' and not uncomplicated and roles and not row['effects'] and not row['residuals'] and not blocked_positive(inv,q,row['path'],cat):
                # A balance floor and the matching credit's checked addition constrain
                # amount, not consent. Recognize only the same ledger and same quantity.
                credit=matched[0][2]
                def move_guard(g):
                    if simple_guard(g,roles,account):return True
                    args=g.get('args',())
                    if len(args)!=2:return False
                    left,right=args
                    if g.get('op')=='>=' and key(left)==key(cell) and key(right)==key(qty):return True
                    if g.get('op')=='>' and key(left)==key(qty) and right.get('value')==0:return True
                    return (g.get('op')=='>' and key(right)==key(credit) and left.get('op')=='+'
                            and sorted(key(a) for a in left.get('args',()))==sorted([key(credit),key(qty)]))
                uncomplicated=all(move_guard(g) for g in guards)
            if quantity_forced_zero(guards,qty,lookup):
                structural.append(opinion("normal","zero_quantity",[src]));continue
            if exact and (cat=="FCR-MINT" or cat=="FCR-DESTROY" and key(account)==key(matched[0][3])):
                structural.append(opinion("normal","intra_ledger_transfer" if cat=="FCR-MINT" else "same_position_restored",[src]))
                continue
            if sign=="+" and cat=="FCR-MINT" and account.get("kind")=="storage":
                decl=lookup.nodes.get(account.get("root"),{})
                apart=any(g.get("op")=="!=" and {key(v) for v in g.get("args",[])}=={key(account),key({"kind":"actual_sender"})} for g in guards)
                wants_fixed=bool(re.search(r'fixed|independent|not controlled|uncontrolled|独立|固定',item.get('claim',''),re.I))
                if decl.get("mutability")=="immutable" and apart:
                    structural.append(opinion("normal","no_new_controlled_credit",[src]));continue
            if not roles or not uncomplicated or not positive_amount:
                uncertain=True;continue
            if cat=="FCR-MINT" and sign=="+" and not opposite and (owned or selectable and all(simple_guard(g,roles,account) for g in guards)):
                return opinion("risk","new_entitlement",[src])
            if sign=="-" and selectable:
                if cat=="FCR-TRANSFER" and exact and key(account)!=key(matched[0][3]) and matched[0][3].get("kind") in ("parameter","actual_sender"):
                    return opinion("risk","existing_rights_moved",[src])
                if cat=="FCR-DESTROY" and not opposite:
                    return opinion("risk","uncompensated_debit",[src])
            uncertain=True
    if structural and not uncertain:return structural[0]
    if (cat in CATEGORIES[1:] and not prop.get("value_dependence",{}).get("value_uses")
        and not prop.get("source_linked_control_uses") and not inv.f.summaries.positions(oid)
        and inv.backend.complete(oid) and not any(r["effects"] for r in rows)
        and cat not in prop.get("possible_categories",[])):
        return opinion("normal","parameter_only",[loc])
    return opinion("open","scope_missing",[loc])

def statement_focus(inv,q,rows):
    """Select an actual statement from source anchoring or unambiguous semantic reference."""
    root=inv.root(q);lookup=inv.f.lookup(root);text=q['current'].get('claim','')
    candidates={}
    for row in rows:
        for w in row['ordered_writes']:
            cell=w['path'];node=lookup.nodes.get(cell['root'],{})
            loc=w.get('source') or {}
            if not loc or not mentioned(text,node.get('name')):continue
            candidates[(loc.get('file'),loc.get('start'),loc.get('length'))]=(row,w,node)
    if len(candidates)==1:return next(iter(candidates.values()))
    return None

def statement_opinion(inv,q,rows):
    focus=statement_focus(inv,q,rows)
    if not focus or q.get("office_effects"):return None
    row,w,node=focus
    if not q['current'].get('_opinion_message') and role_ids(inv,inv.root(q),row) and any(mentioned(q["current"].get("claim",""),inv.f.lookup(inv.root(q)).nodes[r]["name"])
                                                   for r in role_ids(inv,inv.root(q),row)):
        return opinion('normal','guarded_state_change',[w['source']])
    from .summary import local_delta
    sign,amount=local_delta(w)
    if sign and not keys(w['path']) and amount and amount.get('kind')=='literal':
        # Only the located bookkeeping update, provided nothing reads it to exercise a right.
        family=w['path']['root'];target=inv.f.operations[inv.root(q)]['target']
        if not inv.f.summaries.dependencies.readers.get((target,family),[]):
            return opinion('normal','local_bookkeeping',[w['source']])
        others=[edge for edge in inv.f.summaries.dependencies.rows.values() if edge['target']==target and edge['read']['root']==family]
        if not any(x['kind']=='guard' or x['writes'] and x['writes']['root']!=family for x in others):
            return opinion('normal','local_bookkeeping',[w['source']])
    return None

def close_profile(inv, q, basis):
    p=q.get('property') or {}
    if basis['status']!='open' or not p:return basis
    who=inv.root(q); cat=p.get('category')
    if cat in ('FCR-TRANSFER','FCR-DESTROY','FCR-MINT'):
        # Source signs refer to the local operation. Only drop a generated
        # sibling if it also lacks a real amount/control consumer elsewhere.
        if q['current'].get('_host_property_parent') and not p.get('source_linked_control_uses'):
            rows=inv.f.summaries.rows(who)
            sig={local_delta(w)[0] for r in rows for w in r['ordered_writes']
                 if holder(w['path'],inv.f.lookup(who)) is not None}
            if sig=={'+'} and cat!='FCR-MINT' and not any(r['effects'] or r['residuals'] for r in rows):
                from pr_next_joint.frontend.storage import selector_relation
                dependency=inv.f.summaries.dependencies
                closure=dependency.forward(who)
                edges=[dependency.rows[k] for k in closure['edge_ids'] if dependency.rows[k]['use']!=who]
                def carries_prior_balance(edge):
                    if edge['kind']!='value' or not edge['writes'] or selector_relation(edge['writes'],edge['read'])!='same_shape':return False
                    target_row=inv.f.summaries.paths[edge['path']]
                    if target_row['effects'] or target_row['residuals']:return False
                    writes=target_row['ordered_writes'][:edge['position']+1]
                    # A second keyed delta may read through the previous write
                    # on the alias arm. The source increments, including their
                    # amounts and guards, still have to be independent.
                    if not any(key(w['path'])==key(edge['read']) for w in writes):return False
                    for write in writes:
                        if selector_relation(write['path'],edge['read'])!='same_shape':continue
                        sign,amount=local_delta(write)
                        if not sign or amount is None or any(
                                selector_relation(cell,edge['read'])=='same_shape' for cell in selectors(amount)):
                            return False
                    return True
                if (closure['fixed_point_over_indexed_definitions'] and not closure['residuals']
                        and not inv.f.operations[who].get('gaps') and all(carries_prior_balance(edge) for edge in edges)):
                    return opinion('normal','no_debit_in_scope',[inv.f.operations[who]['source']])
    return basis

def reading_version(inv,operations,category=None):
    related=set(operations)
    for op in operations:
        related.update(inv.__dict__.get('_coverage_control_routes',{}).get((op,category),()))
    return inv.semantics.dependency_identity(related)

def scoped_opinion(inv,q):
    root=inv.root(q);p=q.get('property') or {}
    if root is None:return source_opinion(inv,q)
    # A core read or the registered summary is immutable. New binding, domain,
    # policy, scoped evidence or revision must not reuse a previous judgment.
    token=(p.get('id'),q['version'],len(q['evidence']),bool(q.get('task_conflict')),bool(q.get('retired_property_parent')),reading_version(inv,q['binding']['operations'],p.get('category')))
    cached=q.get('_source_opinion')
    if cached and cached[0]==token:return cached[1]
    value=close_profile(inv,q,source_opinion(inv,q))
    q['_source_opinion']=(token,value)
    return value
def native_scope(inv,q,rows):
    root=inv.root(q);cat=(q.get('property') or {}).get('category') or q['current'].get('category')
    if cat not in ('FCR-MINT','FCR-DESTROY','FCR-TRANSFER'):return None
    if any(r['residuals'] for r in rows):return None
    if not any(r['effects'] for r in rows):return None
    if any(e.get('kind')!='native_transfer' for r in rows for e in r['effects']):return None
    if cat=='FCR-MINT':
        if all(local_delta(w)[0]=='-' for r in rows for w in r['ordered_writes']) and all(r['ordered_writes'] for r in rows):
            return opinion('excluded','debit_without_issuance',[r['ordered_writes'][0]['source'] for r in rows])
    if cat=='FCR-DESTROY':
        deltas={(r['path'],key(w['path'])) for r in rows for w in r['ordered_writes']
                if holder(w['path'],inv.f.lookup(root)) is not None and local_delta(w)[0]=='-'}
        paid={(s['path'],key(s['object'])) for eid in q['evidence'] for e in [inv.evidence[eid]]
              if e.get('source_identity')==inv.f.identity and e.get('operation')==root
              for s in e.get('settlements',[]) if s.get('same_holder_and_unit_full_settlement')}
        if deltas and deltas<=paid:return opinion('excluded','same_position_restored',[inv.f.operations[root]['source']])
    return None

def simple_holder_grant(inv,oid,rows):
    """The writer touches only its own nested record and no protected use reads it."""
    if not rows or any(r['effects'] for r in rows):return False
    deps=inv.f.summaries.dependencies;target=inv.f.operations[oid]['target']
    writes=[w for r in rows if r['committing'] for w in r['ordered_writes']]
    if not writes:return False
    for w in writes:
        ix=keys(w['path'])
        if len(ix)!=2 or ix[0].get('kind')!='actual_sender' or ix[1].get('kind')!='parameter':return False
        for eid in deps.readers.get((target,w['path']['root']),()):
            use=deps.rows[eid]['use']
            if use!=oid and not inv.f.operations[use]['generated_getter']:return False
    return True

def source_opinion(inv,q):
    root=inv.root(q);prop=q.get("property") or {};cat=prop.get("category",q["current"].get("category"))
    if not root or q.get("retired_property_parent") or not q["binding"].get("core_exact"):
        return opinion("open","core_mismatch")
    rows=inv.f.summaries.rows(root)
    loc=inv.f.operations[root]["source"]
    if getattr(inv.semantics,'rules',None):
        dispute=inv.semantics.rules.matching_dispute(q)
        if dispute:return dispute
    if q.get("task_conflict") or prop.get("core_rebinding_required"):return opinion("open","core_mismatch",[loc])
    # Reading a guard can settle its execution behaviour, but cannot supply
    # an unresolved business relation at this same effect.
    if rules:=getattr(inv.semantics,'rules',None):
        office=rules.office_opinion(q,rows) if cat=='AC' else None
        if office:return office
        local=rules.effect_policy_opinion(q)
        if local and local['status']!='open':return local
        if cat=='AC':
            independent=source_duty_opinion(inv,q)
            if independent:return independent
        if local:return local
    if cat=='AC' and any(r['committing'] for r in rows):
        paid=paid_service_reading(inv,q,rows)
        if paid:return paid
    if cat=='AC' and (prop.get('expected_authorization') or {}).get('unresolved_relations'):
        return opinion('open','policy_missing',[loc])
    if not prop.get('category') and cat is None:
        return opinion('open','scope_missing',[loc])
    if not rows:
        if inv.backend.complete(root):return opinion("excluded","no_effect_in_scope",[loc])
        return opinion("open","source_context_missing",[loc])
    native=native_scope(inv,q,rows)
    if native:return native
    explicit=set(q['current'].get('_scope_effects',()))
    if explicit:
        effects=[inv.semantics.rules.effects[e] for e in explicit if e in inv.semantics.rules.effects]
        matched=[(r,[d for d in effects if r['path']==d.get('path') or r['path'] in d.get('branches',{})]) for r in rows]
        rows=[r for r,ds in matched if ds]
        clean=[r for r,ds in matched if ds and all(not inv.f.call_summaries.effect_dependencies(r,d) for d in ds)]
    else:clean=[r for r in rows if not r['residuals'] and not any(e.get('kind')=='dangerous_external_call' for e in r['effects'])
           and not any(n.get('kind') in ('credential_recovery','external_return','unknown','native_call_success') for n in walk(r['guards']))]
    if not clean:return opinion('open','external_dependency',[loc])
    result=ac_opinion(inv,q,clean) if cat=='AC' else financial_opinion(inv,q,clean) if cat in CATEGORIES[1:] else opinion('open','scope_missing',[loc])
    if explicit and cat!='AC' and q['current'].get('_opinion_message') and result['status']=='risk':
        where=lambda a:(a.get('file'),a.get('start'),a.get('length'))
        if not {where(d['where']) for d in effects}.intersection(where(loc) for loc in result['locations']):
            return opinion('open','scope_missing',[d['where'] for d in effects])
    if len(clean)!=len(rows) and result['status']!='risk':
        return opinion('open','external_dependency',[loc])
    return result

```

## source/src/pr_next_joint/investigation/state_encoding.py

SHA-256 `b64107887cd866ba2d650dd149c4edb00467e45730fe0073aac0c6e8816fe4fa`

```python
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


def total_value(term, check):
    """Pure fixed-width value with no revert or external dependency when discarded.
    This is used only for a disjoint constructor result. Queried cells, all guards
    and any partial arithmetic still go through the normal expression encoder.
    """
    if not isinstance(term,dict):return False
    kind=term.get('kind')
    if kind in ('actual_sender','literal','parameter','environment','contract_address'):return True
    if kind in ('integer_cast','hash'):return total_value(term.get('input'), check)
    if kind=='abi_encoding':return all(total_value(a,check) for a in term.get('arguments',[]))
    if kind=='source_block_hash':return total_value(term.get('current'),check) and total_value(term.get('height'),check)
    if kind=='op' and term.get('op') in ('+','-','*'):
        check(term)  # Preserve this expression's own arithmetic constraints.
        return True
    if kind=='typed_integer_arithmetic':
        args=term.get('args',[]);sym=term.get('operator')
        if term.get('checked') or len(args)!=2:return False
        if sym not in ('+','-','*') and not (sym in ('%','/') and args[1].get('kind')=='literal' and type(args[1].get('value')) is int and args[1]['value']>0):return False
        return all(total_value(a,check) for a in args)
    return False


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
                    for value in cp.get('evaluated_terms', []):
                        if not total_value(value,expr):expr(value)
                    for w in writes:
                        typ=value_type(w['path'],e.lookup)
                        if typ in ('string','bytes') and w['value'].get('kind') in ('parameter','literal','fixed_bytes_literal','storage'):continue
                        if w['path']['root'] in relevant or not total_value(w['value'],expr):expr(w['value'])
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

```

## source/src/pr_next_joint/investigation/summary.py

SHA-256 `93e0f087549fa794e1e0ba89a6bf69affc3e83d8d6bfdbf92f9e906efce64388`

```python
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
from pr_next_joint.frontend.path_ir import key, walk, ExpressionLimit
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
            direction = directions(c, after)
        except ExpressionLimit as error:
            residual={'path':pid,'declaration':c['root'],'reason':str(error),'scope':'final_storage_value'}
            f.gap(oid,'source_expression_limit',residual)
            p.setdefault('evaluation_gaps',[]).append(residual)
            for card in f.operations[oid]['paths']:
                if card['id']==pid:card['evaluation_gaps']=p['evaluation_gaps']
            local_residuals.append({'cell':copy.deepcopy(c),'reason':'bounded_final_storage_value'})
            continue
        except (Unsupported,ValueError,KeyError) as error:
            local_residuals.append({'cell':copy.deepcopy(c),'reason':'summary_position:'+type(error).__name__+':'+str(error)})
            continue
        from .key_roles import relation
        role=relation(c,lookup)
        numeric.append({'cell': copy.deepcopy(c), 'family': family(c),'key_role':copy.deepcopy(role),
            'before': copy.deepcopy(c), 'after': after, 'type': typ,
            'holder': holder(c, lookup), 'may_directions': direction,
            'sources': [w['source'] for w in p['writes'] if selector_relation(w['path'], c) == 'same_shape']})
        if len([a for a in keys(c) if a.get('kind') in ('actual_sender','contract_address') or
                a.get('type') in ('address','address payable')])>1 and not role:
            local_residuals.append({'cell':copy.deepcopy(c),'reason':'multiple_address_keys_need_source_holder_binding'})
    gaps = copy.deepcopy(p.get('issues', []))
    for gap in p.get('evaluation_gaps', []):
        # Frontend evaluation failures carry a reason code. Detected local
        # expression bounds also carry their path and storage declaration.
        if isinstance(gap, dict):
            gaps.append(copy.deepcopy(gap))
        else:
            reason = gap if isinstance(gap, str) and gap else 'unclassified_evaluation_gap'
            gaps.append({'reason': reason})
    gaps.extend(local_residuals)
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
        self.f = f; self.resources = {}; self.history = []; self.questions = {};self.consents={};self.answer_dispositions={}
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
        from .protocol import ANSWER_CHOICES
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
            'choices': list(ANSWER_CHOICES.get(kind, ANSWER_CHOICES['authorization'])),
            'source_name': self.f.lookup(oid).nodes.get(cell['root'], {}).get('name') if cell else None,
            'related_uses': [self.f.operations[o]['function'] for o in q['binding']['operations']],
            'answer_contract': 'question + answer + short basis; existing entity is already bound; no risk/AST/SMT required'}
        self.questions[sid] = row
        if kind=='financial_consent':
            row.update(question='For this actual holder-issued authorization and dependent request, what quantity does the holder authorize? Explain whether it bounds the final holder debit including fees, or authorizes the checked net request with its disclosed fee rule; preserve the holder, ordered keys, amount, use and phase. A difference between gross and net alone does not decide this policy.',
                choices=list(ANSWER_CHOICES[kind]))
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
        if text not in sq['choices']:
            return None,'semantic_answer_outside_displayed_choices'
        if text in ('other_source_explanation','unknown'):
            return {'issue':q['id'],'meaning':text,'operation':sq['operation'],'target':sq['target'],
                    'policy_resolved':False,'kind':sq['kind'],'scope':copy.deepcopy(sq['semantic_scope']),
                    'quantity_scope':copy.deepcopy(sq.get('quantity_scope')),
                    'alternative_digest':digest(basis)},None
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
                'answer_dispositions':list(self.answer_dispositions.values()),'questions': list(self.questions.values()), 'history': self.history,
                'scoped_support': self.rules.public() if getattr(self,'rules',None) else {},
                'initial_state_modified_by_semantics': False}

```

## source/src/pr_next_joint/reporting/__init__.py

SHA-256 `87e3e2f1dba261e0999d37d622e45825e4d2763d9091aa860663f27df53e5d17`

```python
"""Source analysis helpers retained by SCRV."""

```

## source/src/pr_next_joint/reporting/effective_parameters.py

SHA-256 `53720da2343b7497ad5db094e7ac2c04704b66458db554ba0da4e372cc86470f`

```python
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

def investigation_profile(options):
    return {**options.record(), 'feedback_yield_seconds':min(300.,options.seconds/2),
            'long_action_slice_seconds':max(options.solver_timeout_ms/1000.,min(60.,options.seconds/6.)),
            'cumulative_solver_seconds':options.seconds,'expression_nodes_max':current()['expression_nodes_max'],
            'expression_depth_max':current()['expression_depth_max']}

```

## source/src/pr_next_joint/resources/method_evidence.r1.json

SHA-256 `c906e1486ec2603ce7d43e7f41232df6d123036279e7b4aff481fe6663d6a34d`

```json
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

```

## source/src/pr_next_joint/runtime/__init__.py

SHA-256 `87e3e2f1dba261e0999d37d622e45825e4d2763d9091aa860663f27df53e5d17`

```python
"""Source analysis helpers retained by SCRV."""

```

## source/src/pr_next_joint/runtime/immutable.py

SHA-256 `7170290a5ac58d0ab7a95e229813744025997c44c372130b511f2b58810fa2dd`

```python
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

```

## source/src/pr_next_joint/verification/__init__.py

SHA-256 `87e3e2f1dba261e0999d37d622e45825e4d2763d9091aa860663f27df53e5d17`

```python
"""Source analysis helpers retained by SCRV."""

```

## source/src/pr_next_joint/verification/expressions.py

SHA-256 `57fe986e34c11643995e8551c99920d037a01783f52136e5c41ea0edf53f0a0f`

```python
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

```

## source/src/pr_next_joint/verification/hash_confirmation.py

SHA-256 `2c21ab1686e5e4c9b7eb9a1695a5899b71c86ebcf235f1bf7202a046fdda9b39`

```python
"""Hash-abstraction status, without model or candidate extraction.

Literal hashes keep exact source semantics. An active symbolic hash is not
accepted as a positive source proof. No concrete ABI/preimage data is built.
"""

def status(encoder, solver):
    z=encoder.z; rows=getattr(encoder,'hash_terms',{})
    if not rows:return {'status':'not_required'}
    declarations={row['application'].decl() for row in rows.values()}
    pending=[z.simplify(z.And(*solver.assertions()))];seen=set()
    while pending:
        node=pending.pop()
        if node.get_id() in seen:continue
        seen.add(node.get_id())
        if z.is_app(node) and node.decl() in declarations:
            return {'status':'unverified','reason':'symbolic_hash_requires_exact_nonconstructive_proof'}
        if z.is_quantifier(node):pending.append(node.body())
        elif z.is_app(node):pending.extend(node.children())
    return {'status':'not_required','only_inactive_hash_terms':True}

```

## source/src/pr_next_joint/verification/joint_encoding.py

SHA-256 `79ce9d8c227056be9754765ccdc17b03ae58fa391f3d4681f321eef168dbd8df`

```python
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

```

## source/src/pr_next_joint/verification/joint_intrinsics.py

SHA-256 `f7abeba1589e49b957d3fbd10b7ee63c95c3915ec0b561ab720d264ab20c6ff7`

```python
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

```

## source/src/pr_next_joint/verification/program_encoding.py

SHA-256 `7128655ee891f5d43b803541f0b60ef1cdfcce04c114ea6c2badc8503ed92575`

```python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""
import copy
from functools import lru_cache
from pr_next_joint.graph.state_relations import scalar as scalar_write
from pr_next_joint.verification.joint_encoding import JointEncoder
from pr_next_joint.verification.expressions import Unsupported
from pr_next_joint.frontend.path_ir import key, op, lit, walk

SECP256K1_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


@lru_cache(maxsize=256)
def exact_recovery(digest, v, r, s):
    """Pure local precompile semantics, not EVM execution or a signing oracle."""
    if v not in (27, 28) or not (0 < r < SECP256K1_ORDER and 0 < s < SECP256K1_ORDER):
        return 0
    if not 0 <= digest < 2 ** 256: raise Unsupported('ecrecover_digest_width')
    from eth_keys.datatypes import Signature
    from eth_keys.backends.native import NativeECCBackend
    from eth_keys.exceptions import BadSignature
    try:
        public = Signature(vrs=(v - 27, r, s), backend=NativeECCBackend()).recover_public_key_from_msg_hash(digest.to_bytes(32, 'big'))
    except BadSignature:
        return 0
    return int.from_bytes(public.to_canonical_address(), 'big')


class MechanismEncoder(JointEncoder):
    def __init__(self, lookup):
        super().__init__(lookup)
        self.credential_terms = {}
        self.expression_cache = {}
        self.expression_cache_hits = 0
        self.expression_visits = 0

    def checkpoint(self):
        """Snapshot every mutable encoder registry for a speculative branch."""
        return {k:(v.copy() if isinstance(v,(dict,list,set)) else v) for k,v in self.__dict__.items()}

    def rollback(self,snapshot):
        self.__dict__.clear()
        self.__dict__.update(snapshot)

    def expr(self,value):
        """Share expression DAGs, replaying their *local* success conditions.

        Returning a cached arithmetic value without its overflow/branch
        conditions would be unsound. Domains and execution conditions are
        therefore stored separately and replayed at each use, where the
        surrounding branch/frame captures them as before. Caches never cross
        an encoder, target, initial/runtime mode or query branch.
        """
        self.expression_visits+=1
        if self.expression_visits%64==1:
            remaining=getattr(self.lookup,'encoding_remaining',None)
            if remaining and remaining()<=0:raise TimeoutError('program_encoding_budget_exhausted')
        token=(bool(getattr(self,'_encoding_initial',False)),key(value))
        cached=self.expression_cache.get(token)
        if cached is not None:
            result,conditions,domains=cached
            if conditions is not None:self.constraints.append(conditions)
            if domains is not None:self.domain_constraints.append(domains)
            self.expression_cache_hits+=1
            return result
        mark,domain_mark=len(self.constraints),len(self.domain_constraints)
        result=self._expr_uncached(value)
        def compact(rows):
            unique={r.get_id():r for r in rows if not self.z.is_true(r)}
            if not unique:return None
            values=list(unique.values())
            # Flatten redundant nested conditions before retaining a DAG.
            # Otherwise serialization can expand repeated And/Implies chains
            # much more than the actual source expression.
            result=self.z.simplify(values[0] if len(values)==1 else self.z.And(*values))
            return None if self.z.is_true(result) else result
        conditions=compact(self.constraints[mark:]);domains=compact(self.domain_constraints[domain_mark:])
        del self.constraints[mark:];del self.domain_constraints[domain_mark:]
        if conditions is not None:self.constraints.append(conditions)
        if domains is not None:self.domain_constraints.append(domains)
        if len(self.expression_cache)>=4096:self.expression_cache.pop(next(iter(self.expression_cache)))
        self.expression_cache[token]=(result,conditions,domains)
        return result

    def credential_status(self, solver):
        """Check exact encoding applicability without requesting assignments.

        Literal recovery and exact invalid domains are already encoded by
        _expr_uncached. An active symbolic recovery function is an unproved
        abstraction: SAT alone cannot establish the original source property.
        """
        z = self.z
        recovery = self.functions.get('source_ecrecover')
        if recovery is None:
            return {'status':'not_required','exact_invalid_domains_preserved':True}
        pending=[z.simplify(z.And(*solver.assertions()))];seen=set()
        while pending:
            node=pending.pop()
            if node.get_id() in seen:continue
            seen.add(node.get_id())
            if z.is_app(node) and node.decl()==recovery:
                return {'status':'unverified','reason':'symbolic_credential_requires_exact_nonconstructive_proof'}
            if z.is_quantifier(node):pending.append(node.body())
            elif z.is_app(node):pending.extend(node.children())
        return {'status':'not_required','exact_invalid_domains_preserved':True}

    def invalid_recovery_subdomain(self,solver):
        """Exact invalid-domain restriction; no concrete signature is chosen.

        It can establish a positive existential subcase only. Failure says
        nothing about valid credentials or the whole original property.
        """
        z=self.z;recovery=self.functions.get('source_ecrecover')
        if recovery is None:return None
        original=z.simplify(z.And(*solver.assertions()))
        pending=[original];seen=set();applications={}
        while pending:
            node=pending.pop()
            if node.get_id() in seen:continue
            seen.add(node.get_id())
            if z.is_quantifier(node):return None
            if z.is_app(node):
                if node.decl()==recovery:applications[node.get_id()]=node
                pending.extend(node.children())
        if not applications:return None
        invalid=[];replacements=[]
        for node in applications.values():
            args=list(node.children())
            if len(args)!=4:return None
            invalid.append(z.Or(z.And(args[1]!=27,args[1]!=28),
                args[2]<=0,args[2]>=SECP256K1_ORDER,args[3]<=0,args[3]>=SECP256K1_ORDER))
            replacements.append((node,z.IntVal(0)))
        # Under these exact precompile failure conditions every recovery
        # application is zero. No symbolic successful recovery is trusted.
        restricted=z.simplify(z.substitute(z.And(original,*invalid),*replacements))
        result=z.Solver();result.add(restricted)
        return result

    def bound(self,x,typ):
        from pr_next_joint.graph.state_relations import enum_size
        size=enum_size(self.lookup,typ)
        if size is not None:
            domain=[x>=0,x<size];self.constraints.extend(domain);self.domain_constraints.extend(domain);return x
        return super().bound(x,typ)

    def _expr_uncached(self, value):
        if isinstance(value,dict) and value.get("kind")=="source_linear_quantity":
            # Mathematical before/after difference, not an executed unsigned
            # Solidity subtraction. Executed arithmetic is checked separately.
            terms=value["terms"]
            if not all(type(x.get("coefficient")) is int for x in terms):raise Unsupported("source_delta_coefficient")
            return self.z.Sum(*[x["coefficient"]*self.expr(x["value"]) for x in terms]) if terms else self.z.IntVal(0)

        if value.get('kind')=='checked_evaluation':
            if value.get('type')!='uint256':raise Unsupported('checked_evaluation_type_not_supported')
            evaluated=self.expr(value['input'])
            # An arithmetic success condition belongs to this path, unlike
            # a symbol's type domain. Keep it inside a negated continuation.
            self.constraints.extend([evaluated>=0,evaluated<2**256])
            return evaluated
        if value.get('kind')=='source_pure_memory_word':
            raise Unsupported('pure_memory_word_required_by_this_check_not_encoded')
        if value.get('kind')=='fixed_bytes_literal':
            raise Unsupported('fixed_bytes_literal_outside_typed_hash_layout')
        if value.get('kind')=='enum_cast':
            node=self.lookup.nodes.get(value['enum_ast_id'],{})
            if node.get('nodeType')!='EnumDefinition' or len(node['members'])!=value['members']:
                raise Unsupported('enum_cast_source_identity')
            x=self.expr(value['input']);self.constraints.extend([x>=0,x<value['members']]);return x
        if value.get('kind')=='op' and value.get('op') in ('%','/'):
            a,b=value['args']
            if a.get('kind')=='uint_narrow' and b.get('kind')=='literal' and type(b.get('value')) is int and 0<b['value']<2**a['bits']:
                x=self.expr(a);d=b['value']
                return x%d if value['op']=='%' else x/d
        if value.get('kind')=='op' and value.get('op') in ('<<','>>'):
            left,right=value['args'];bits=self.width(self.typ(left))
            a,b=self.expr(left),self.expr(right)
            av,bv=self.z.Int2BV(a,bits),self.z.Int2BV(b,bits)
            shifted=(av<<bv) if value['op']=='<<' else self.z.LShR(av,bv)
            return self.z.If(b>=bits,self.z.IntVal(0),self.z.BV2Int(shifted,is_signed=False))
        if (value.get('kind') == 'member' and value.get('member') == 'chainid'
                and value.get('base', {}).get('kind') == 'symbol'):
            decl = value['base'].get('declaration')
            from pr_next_joint.frontend.source_entry_identity import builtin_object
            if not (type(decl) is int and any(
                    n.get('nodeType') == 'MemberAccess' and n.get('memberName') == 'chainid'
                    and n.get('expression', {}).get('referencedDeclaration') == decl
                    and builtin_object(n.get('expression',{}),self.lookup,'block')
                    for n in self.lookup.nodes.values())):
                raise Unsupported('chainid_not_bound_to_source_builtin')
            return self.atom({'kind': 'environment', 'field': 'chainid', 'type': 'uint256'})
        if value.get('kind') == 'op' and value.get('op') == 'ite':
            condition,yes,no=value['args']
            return super().expr({'kind':'conditional','condition':condition,'when_true':yes,'when_false':no})
        if value.get('kind') == 'credential_recovery':
            args = [self.expr(value['digest'])] + [self.expr(x) for x in value['signature']]
            z = self.z
            simplified = [z.simplify(a) for a in args]
            invalid = z.Or(z.And(args[1] != 27, args[1] != 28), args[2] <= 0, args[2] >= SECP256K1_ORDER,
                           args[3] <= 0, args[3] >= SECP256K1_ORDER)
            if z.is_true(z.simplify(invalid)):
                self.encoding_notes.append({'kind': 'ecrecover_exact_failure_domain'})
                return z.IntVal(0)
            if all(z.is_int_value(a) for a in simplified):
                self.encoding_notes.append({'kind': 'ecrecover_exact_constant_arguments'})
                return z.IntVal(exact_recovery(*[a.as_long() for a in simplified]))
            name = 'source_ecrecover'
            if name not in self.functions:
                self.functions[name] = self.z.Function(name, *[a.sort() for a in args], self.z.IntSort())
            self.encoding_notes.append({'kind': 'credential_recovery_congruence',
                'scope': 'same digest and same signature recover same address; not a signature forgery proof'})
            application = self.functions[name](*args)
            recovered = self.bound(application, 'address')
            self.credential_terms[application.sexpr()] = {'args': args, 'application': application}
            self.encoding_notes.append({'kind': 'ecrecover_validity_dependency',
                'scope': 'exact v/r/s failure domains; successful symbolic witnesses require recovery validation'})
            return z.If(invalid, z.IntVal(0), recovered)
        return super().expr(value)

def execution_terms(path,lookup):
    """Fail closed if a new consumer cannot retain successful evaluation."""
    if path.get('evaluation_trace_kind')!='downstream_evaluated_expressions_v1':
        raise Unsupported('successful_evaluation_trace_missing')
    if path.get('evaluation_gaps'):
        reasons = set()
        for gap in path['evaluation_gaps']:
            reason = gap.get('reason') if isinstance(gap, dict) else gap
            reasons.add(reason if isinstance(reason, str) and reason else 'unclassified_evaluation_gap')
        raise Unsupported('successful_evaluation_incomplete:' + ','.join(sorted(reasons)))
    terms=copy.deepcopy(path['evaluated_terms'])
    for raw in path['writes']:
        w=scalar_write(raw,lookup)
        terms.extend([w['path'],w['value']])
    if path.get('return_value') is not None:
        terms.append(copy.deepcopy(path['return_value']))
    return terms

```

## source/src/pr_next_joint/verification/sequence.py

SHA-256 `1d3d3c3409972c4e971cc3cfd0c01db0310478c7a3b07f3fe0fee40c484e90d1`

```python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""
import copy
from pr_next_joint.frontend.path_ir import key, op, lit
from pr_next_joint.graph.state_relations import compose_read, expand_write
from pr_next_joint.verification.expressions import Unsupported

def qualify(value,step):
    if isinstance(value,dict):
        kind=value.get('kind')
        if kind=='actual_sender':return {'kind':'parameter','id':-9000000-step,'type':'address','sequence_role':'caller','step':step}
        if kind=='parameter':return {**value,'id':-((step+1)*10000000+abs(int(value['id']))),'step':step}
        if kind=='environment' and value.get('field') in ('timestamp','number'):
            return {'kind':'parameter','id':-(81000000+step*10+('timestamp','number').index(value['field'])),
                    'type':'uint256','sequence_role':value['field'],'step':step}
        if kind in ('transaction_origin','source_calldata_length','native_call_success'):
            return {**value,'sequence_step':step}
        if kind in ('transaction_value','block_timestamp','block_number'):
            return {'kind':'parameter','id':-(80000000+step*10+('transaction_value','block_timestamp','block_number').index(kind)),
                    'type':'uint256','sequence_role':kind,'step':step}
        return {k:qualify(v,step) for k,v in value.items()}
    return [qualify(v,step) for v in value] if isinstance(value,list) else value

def compose(lookup,steps,equalities=(),*,step_offset=0):
    if not 1<=len(steps)<=3:raise Unsupported('v20_transaction_sequence_bound')
    if type(step_offset) is not int or step_offset<0 or step_offset+len(steps)>3:raise Unsupported('sequence_namespace_bound')
    writes=[];guards=[];evaluated=[];trace=[]
    for local_i,(fn,pi,path) in enumerate(steps):
        i=local_i+step_offset
        if path['flow'] not in ('normal','returned') or path['issues'] or path.get('evaluation_gaps'):raise Unsupported('v20_sequence_path_incomplete')
        before=copy.deepcopy(writes)
        g=[read(qualify(x,i),before,lookup) for x in path['guards']]
        guards+=g
        evaluated.extend(read(qualify(v,i),before,lookup) for v in path.get('evaluated_terms',[]))
        stepwrites=[]
        for w in path['writes']:
            for e in expand_write(w,lookup):
                q=qualify(e,i)
                # Each path value already includes same-call substitutions.
                q['value']=read(q['value'],before,lookup)
                # Bind indexed keys using pre-state, never replace the location itself.
                q['path']={**q['path'],'segments':read(q['path'].get('segments',[]),before,lookup)}
                stepwrites.append(q)
        writes+=stepwrites
        if local_i:
            for field in ('timestamp','number'):
                now=qualify({'kind':'environment','field':field},i)
                prev=qualify({'kind':'environment','field':field},i-1)
                guards.append(op('>=',now,prev))
        trace.append({'step':i,'function':fn,'path_index':pi,'caller':qualify({'kind':'actual_sender'},i),'writes':stepwrites,'before_writes':before})
    guards.extend(copy.deepcopy(equalities))
    return {'conditions':guards,'writes':writes,'evaluation_terms':evaluated,'steps':trace,
            'assumption':'source-matched sequence from declared symbolic prestate; deployment prefix not proved'}

def read(value,writes,lookup):
    """Resolve key expressions from the pre-state as well as stored values."""
    if isinstance(value,dict):
        if value.get('kind')=='storage':
            prepared={**value,'segments':read(value.get('segments',[]),writes,lookup)}
            return compose_read(prepared,writes,lookup)
        return {k:read(v,writes,lookup) for k,v in value.items()}
    return [read(v,writes,lookup) for v in value] if isinstance(value,list) else value

```

## source/src/pr_next_joint/verification/solver.py

SHA-256 `f1b29908fdeeccb9412ffb421ff3baa71a8e923a62d9bb54949c99c95f36c4ee`

```python
"""Per-analysis finite solver budget; UNKNOWN never becomes refutation."""
import time
from contextlib import contextmanager
from contextvars import ContextVar
_current=ContextVar('v20_solver_budget',default=None)
_remaining_program=ContextVar('remaining_cooperative_program_budget',default=None)

@contextmanager
def budget(seconds=120.0,remaining=None,timeout_ms=3000):
    state={'limit_seconds':float(seconds),'per_check_ms':timeout_ms,'unknown_reasons':{},'used_seconds':0.0,'calls':0,'upgrades':0,'budget_exhausted':0,'events':[]}
    token=_current.set(state);other=_remaining_program.set(remaining)
    try:yield state
    finally:_current.reset(token);_remaining_program.reset(other)

def solve(solver,initial_ms=None,upgrade=False):
    import z3
    b=_current.get()
    # SCRV's common verifier is always enabled. Legacy variant switches and
    # their report side effects are not part of this successor's entry.
    if initial_ms is None:initial_ms=b["per_check_ms"] if b else 3000
    def remaining():
        solver_ms=max(0,int((b['limit_seconds']-b['used_seconds'])*1000)) if b else initial_ms+10000
        callback=_remaining_program.get()
        return min(solver_ms,max(0,int(callback()*1000))) if callback is not None else solver_ms
    limit=min(initial_ms,remaining())
    if limit<1:
        if b:b['budget_exhausted']+=1
        return z3.unknown
    solver.set(timeout=limit,random_seed=0)
    start=time.perf_counter();answer=solver.check();elapsed=time.perf_counter()-start
    if b:b['used_seconds']+=elapsed;b['calls']+=1
    reason=solver.reason_unknown() if answer==z3.unknown else None
    if reason and b:
        key="timeout" if "timeout" in reason.lower() else ("canceled" if "canceled" in reason.lower() else "other")
        b["unknown_reasons"][key]=b["unknown_reasons"].get(key,0)+1
    retry_ms=min(initial_ms,remaining()) if upgrade else 0
    if retry_ms>0 and answer==z3.unknown and reason and any(w in reason.lower() for w in ('timeout','canceled')):
        solver.set(timeout=retry_ms)
        start=time.perf_counter();answer=solver.check();elapsed2=time.perf_counter()-start
        if b:b['used_seconds']+=elapsed2;b['calls']+=1;b['upgrades']+=1
        if b:b['events'].append({'kind':'bounded_timeout_upgrade','first_seconds':elapsed,'additional_seconds':elapsed2,'answer':str(answer)})
    return answer

def status():
    b=_current.get()
    return dict(b) if b else {'scope':'no_active_analysis_budget'}

```

## source/src/pr_next_joint/verification/source_worlds.py

SHA-256 `c154a0498a3ca63a31221e6883e7fcc2e3107a7e197ec728376a4cb76c8f09e3`

```python
"""Explicit source frames and forked worlds. No early-pruning optimization."""
import copy
import itertools
from pr_next_joint.frontend.path_ir import op, lit, key
from pr_next_joint.verification.sequence import qualify, read, compose
from pr_next_joint.verification.expressions import Unsupported


def successful(path):
    return path['flow'] in ('normal', 'returned') and not path.get('issues') and not path.get('evaluation_gaps')


def frame(facts, oid, pid, slot, before=(), path_override=None):
    item = facts.paths[pid]
    if item['operation'] != oid: raise Unsupported('frame_operation_identity')
    p = item['raw'] if path_override is None else path_override; lookup = facts.lookup(oid)
    if not successful(p): raise Unsupported('source_semantics_unavailable:' + pid)
    translate = lambda v: read(qualify(v, slot), before, lookup)
    writes = []
    for w in p['writes']:
        q = qualify(w, slot)
        q['path']['segments'] = read(q['path'].get('segments', []), before, lookup)
        q['value'] = read(q['value'], before, lookup)
        writes.append(q)
    effects = [translate(e) for e in p.get('sensitive_effects', [])]
    return {'operation': oid, 'path': pid, 'slot': slot, 'before': copy.deepcopy(list(before)),
            'guards': [translate(g) for g in p['guards']], 'writes': writes, 'effects': effects,
            'evaluated_terms': [translate(x) for x in p.get('evaluated_terms', [])],
            'caller': qualify({'kind': 'actual_sender'}, slot),
            'evidence_world': 'original_source_success_path'}


def encode_frame(encoder, f, extras=()):
    """All evaluation obligations stay inside this world's success formula.

    In particular ATTEMPT arithmetic and guards are not asserted globally
    before negating a success predicate.
    """
    mark = len(encoder.constraints)
    for x in f.get('evaluated_terms', []): encoder.expr(x)
    for w in f.get('writes', []):
        encoder.expr(w['path']); encoder.expr(w['value'])
    terms = [encoder.expr(x) for x in f['guards']] + list(extras)
    conditions = encoder.constraints[mark:]
    del encoder.constraints[mark:]
    return encoder.z.And(*conditions, *terms)


def bind_keys(a, b):
    from pr_next_joint.frontend.storage import keys, fields
    if a['root'] != b['root'] or fields(a) != fields(b) or key(a.get('instance')) != key(b.get('instance')):
        raise Unsupported('world_object_family_mismatch')
    aa, bb = keys(a), keys(b)
    if len(aa) != len(bb): raise Unsupported('world_key_arity')
    return [op('==', x, y) for x, y in zip(aa, bb)]


def serialize_world(f, name):
    return {'world': name, 'operation': f['operation'], 'path': f['path'], 'slot': f['slot'],
            'caller': f['caller'], 'guards': f['guards'], 'committed_writes': f['writes'],
            'before_writes': f['before'], 'evaluated_terms': f['evaluated_terms']}

```

## source/src/pr_next_joint/verification/typed_integer.py

SHA-256 `69ac684baea6edfaafaf980a1a821cba165b5416c0a973ba60594ea8c01b7697`

```python
"""Compiler-width arithmetic; no unsigned widening of signed source values."""
import re
from pr_next_joint.verification.expressions import Unsupported

def integer_type(typ):
    m=re.fullmatch(r'(u?int)(\d*)',typ or '')
    return (m[1]=='int',int(m[2] or 256)) if m else None

def checked_mode(lookup,state):
    import json
    raw=lookup.bundle.get('compiler',{})
    text=raw.get('version',raw.get('compiler_version','')) if isinstance(raw,dict) else str(raw)
    if not text:text=str(lookup.bundle.get('compiler_version',''))
    m=re.search(r'(\d+)\.(\d+)\.(\d+)',text)
    if not m:raise Unsupported('integer_compiler_version_missing')
    return tuple(map(int,m.groups()))>=(0,8,0) and not state.get('_unchecked_depth',0)

def encode(e,v):
    typ=integer_type(v.get('type'))
    if typ is None:raise Unsupported('integer_type_unresolved')
    signed,bits=typ;z=e.z;low=-2**(bits-1) if signed else 0;high=2**(bits-int(signed))
    if v['kind']=='integer_cast':value=e.expr(v['input'])
    else:
        args=[e.expr(a) for a in v['args']];operator=v['operator']
        if not all(z.is_int(x) for x in args):raise Unsupported('integer_operand_sort')
        if len(args)==1:
            if operator!='-':raise Unsupported('integer_unary_operator')
            value=-args[0]
        else:
            a,b=args
            if operator in ('/','%'):
                e.constraints.append(b!=0)
                absolute=z.Abs(a)/z.Abs(b);quotient=z.If((a<0)!=(b<0),-absolute,absolute)
                value=quotient if operator=='/' else a-quotient*b
            elif operator in ('+','-','*'):value={'+':lambda:a+b,'-':lambda:a-b,'*':lambda:a*b}[operator]()
            else:raise Unsupported('integer_operator_not_lowered')
        if v.get('checked'):
            e.constraints.extend([value>=low,value<high]);return value
    unsigned=value%(2**bits)
    return z.If(unsigned>=2**(bits-1),unsigned-2**bits,unsigned) if signed else unsigned

```
