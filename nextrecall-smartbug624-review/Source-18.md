## source/src/pr_next_joint/investigation/source_opinion.py

~~~~python
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
    readers=inv.graph.access.get((target,cell["root"]),{}).get("readers",())
    for use in sorted(readers):
        if use==oid or inv.f.operations[use]["generated_getter"]:continue
        for row in inv.f.summaries.rows(use):
            if not row["committing"] or row["residuals"] or not (row["ordered_writes"] or row["effects"]):continue
            guards=row['guards']
            if any(office_guard(g,cell) or exception_authority(inv,use,cell,g) for g in guards) and feasible_source_guards(guards):return use
    return None

def replacement_status(inv,oid,cell,path):
    """An alternative acquisition guard is not automatically a bypass."""
    guards=path['guards']
    if not feasible_source_guards(guards):return 'open'
    if any(office_guard(g,cell) for g in guards):return 'normal'
    if not guards:return 'risk'
    # A second stored qualification can authorize a nominee or delegated holder.
    # Keep it for the policy/authorization checker, including OR and short circuit.
    if any(v.get('kind') in ('storage','external_return','unknown','credential_recovery') for v in walk(guards)):return 'open'
    return 'risk'

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
        status='open'; why='policy_missing'
        if candidate['family']=='unbacked_issuance':
            qty=local_delta(d['write'])[1]
            from pr_next_joint.frontend.path_ir import op,lit
            if (caller_input_conditions(row['guards']) and sourced_quantity(qty,inv.f.lookup(oid))
                    and feasible_source_guards([*row['guards'],op('>',qty,lit(0))]) and unit_origin(inv.backend,oid,d['cell'])):
                status,why='risk','unbacked_source_issuance'
        elif candidate['duty']=='holder_issued_grant':
            if candidate['issuer']=='actual_sender':
                status,why='normal','self_delegation'
            elif candidate['issuer']=='parameter' and caller_input_conditions(row['guards']) and not row['residuals']:
                status,why='risk','source_role_reassignment'
        elif candidate['duty']=='guarded_downstream_use':
            handoff=handover(inv,oid,[row])
            if handoff:return handoff
            status=replacement_status(inv,oid,d['cell'],inv.f.paths[pid]['raw'])
            why='source_role_reassignment' if status=='risk' else 'applicable_role_guard'
        elif candidate['family']=='managed_phase':
            if caller_input_conditions(row['guards']) and not row['residuals']:
                status,why='risk','unguarded_governed_effect'
        elif candidate['family']=='managed_lifecycle':
            if candidate['controller_guarded'] or candidate['phase']=='completed':
                status,why='normal','governed_completion'
            elif candidate.get('phase_guard') and caller_input_conditions(row['guards'],candidate['phase_guard']) and not row['residuals']:
                status,why='risk','unqualified_active_termination'
        if status=='open':continue
        ans=opinion(status,why,[d['where']])
        ans['source_relation']={'family':candidate['family'],'duty':candidate['duty'],'support_location':candidate['support']}
        if candidate.get('use'):ans['protected_use']=inv.f.operations[candidate['use']]['source']
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
        moves=[]
        for w in row["ordered_writes"]:
            cell=w["path"];account=holder(cell,lookup)
            if account is None or not unit_origin(inv.backend,oid,cell) or native_only_position(inv.backend,oid,cell):continue
            sign,qty=local_delta(w)
            if sign:moves.append((sign,qty,cell,account,w["source"]))
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

~~~~

## source/src/pr_next_joint/investigation/state_encoding.py

~~~~python
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

~~~~
