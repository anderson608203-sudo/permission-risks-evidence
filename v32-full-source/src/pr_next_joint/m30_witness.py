"""Compare verifiable, executable alternatives. Failed searches stay explicitly limited."""
from .m30_evm import Unavailable


def limited(why, **details):
    return {"status":"not_established","reason":why,**details}


def acquisition(world, plan):
    fn, peer, getter = plan["fn"],plan["peer"],plan["getter"]
    if world.read(getter)!=int.from_bytes(world.admin,"big"):
        return limited("no_pre_existing_global_deployer_authority")
    base=world.snapshot()
    args=world.arguments(peer,world.other,1)
    authorized=world.call(peer,world.admin,args)
    if not authorized["ok"] or world.read(getter)!=int.from_bytes(world.other,"big"):
        return limited("comparison_does_not_observably_replace_existing_authority")
    world.restore(base)
    direct=world.call(peer,world.user,args)
    if direct["ok"] or direct["error"] not in ("Revert","InvalidInstruction"):
        return limited("stranger_not_refused_by_original_route")
    world.restore(base)
    grant=world.call(fn,world.user,address=world.user,value=0)
    if not grant["ok"] or world.read(getter)!=int.from_bytes(world.user,"big"):
        return limited("unprivileged_writer_cannot_acquire_live_authority")
    after=world.call(peer,world.user,args)
    if not after["ok"] or world.read(getter)!=int.from_bytes(world.other,"big"):
        return limited("new_authority_cannot_commit_comparison_effect")
    return {"status":"witness","reason":"uninvited_replacement_of_live_managing_authority",
            "normal":[authorized],"before":[direct],"attack":[grant,after],
            "observed":"same request/arguments and initial state; public grant then use; previously governed address replaced",
            "limitation":"source-supported control-boundary mechanism in the disclosed deployment; no asset-loss claim"}


def repeat_credit(world, plan):
    base=world.snapshot()
    cold=credit_cycle(world,plan,False)
    if cold["status"]=="witness" or cold["reason"] not in (
            "additional_entitlement_reserve_or_compensation_changed_over_the_cycle",
            "comparison_is_not_transfer_of_the_callers_existing_balance"):
        return cold
    world.restore(base)
    # Seed a new recipient by the original credit operation when the initial transfer is blocked.
    # The full checked spend/reset cycle still has to increase only the independent recipient slot.
    seed=world.call(plan["fn"],world.recipient,address=world.recipient,number=64)
    if seed["ok"] and not seed["nested_calls"] and not seed["beneficiaries"]:
        seeded=credit_cycle(world,plan,False)
        if seeded["status"]=="witness":
            return {**seeded,"recipient_setup":seed,"new_recipient_observation":cold["reason"]}
    world.restore(base)
    result=credit_cycle(world,plan,True)
    result["new_recipient_observation"]=cold["reason"]
    return result


def credit_cycle(world, plan, initialize_recipient):
    getter=plan["getter"]
    base=world.snapshot()
    first=world.call(plan["fn"],world.user,address=world.user,number=64)
    if not first["ok"]:
        return limited("unpaid_credit_unavailable")
    setup=[first]
    if initialize_recipient:
        distribution=world.call(plan["peer"],world.user,[world.recipient,1])
        reset=world.call(plan["fn"],world.user,address=world.user,number=64)
        if not distribution["ok"] or not reset["ok"] or world.read(getter,world.recipient)<1:
            return limited("preexisting_recipient_cannot_be_reached_by_public_operations")
        setup.extend((distribution,reset))
    start=world.read(getter,world.user)
    receiver=world.read(getter,world.recipient)
    if start<=0:
        return limited("credit_produced_no_spendable_units")
    amount=max(1,min(16,start//2))
    original=world.snapshot()
    move=world.call(plan["peer"],world.user,[world.recipient,amount])
    spent=world.read(getter,world.user)
    received=world.read(getter,world.recipient)
    if not move["ok"] or spent>=start or received<=receiver:
        return limited("comparison_is_not_transfer_of_the_callers_existing_balance")
    credit=world.call(plan["fn"],world.user,address=world.user,number=64)
    owner_end=world.read(getter,world.user)
    recipient_end=world.read(getter,world.recipient)
    if not credit["ok"] or owner_end!=start or recipient_end!=received:
        return limited("cannot_recover_spent_balance_while_recipient_keeps_the_credit")
    if any(r["nested_calls"] or r["beneficiaries"] for r in (move, credit)):
        return limited("cycle_has_external_or_lifecycle_effects_requiring_compensation_analysis")
    # Check every modified storage cell of both transactions, including callees. A ticket,
    # quota, reserve or other right consumed over the cycle ordinarily changes a second cell.
    keys={(a,s) for row in (move,credit) for a,s,_,_ in row["changed_slots"]}
    recipient_cell=world.unique_getter_slot(getter,world.recipient)
    if recipient_cell not in keys:
        return limited("increment_not_bound_to_recipient_storage")
    after=world.snapshot()
    addresses={world.address,world.admin,world.recipient,world.delegate,world.other}
    balances={a:world.state.get_balance(a) for a in addresses}
    new={k:world.state.get_storage(bytes.fromhex(k[0]),int(k[1],16)) for k in keys}
    world.restore(original)
    changed={k for k in keys if world.state.get_storage(bytes.fromhex(k[0]),int(k[1],16))!=new[k]}
    if changed!={recipient_cell} or any(world.state.get_balance(a)!=balances[a] for a in addresses):
        return limited("additional_entitlement_reserve_or_compensation_changed_over_the_cycle")
    # Reject externally funded values/calls not represented by the token observations.
    world.restore(base)
    before=world.read(getter,world.user)
    world.restore(after)
    return {"status":"witness","reason":"repeatable_unpaid_recovery_of_spent_transferable_credit",
            "before_balance":before,"cycle_start":start,"after_spending":spent,"after_reset":owner_end,
            "recipient_before":receiver,"recipient_after":recipient_end,"transactions":[*setup,move,credit],
            "recipient_was_initialized":initialize_recipient,
            "unchanged_other_modified_cells":len(keys)-1,"independent_recipient_cell":list(recipient_cell),
            "limitation":"issuing authority boundary, including intentionally open repeated issuance; no market-value claim"}


def early_termination(world,plan):
    if world.name in ("cancun","prague"):
        return limited("fork_does_not_delete_persistent_code")
    fn,normal=plan["fn"],plan["peer"]
    witness_claims={g:world.read(g,world.other) for g in plan["claim_getters"]}
    fund=world.call(normal,world.other,value=1)
    if not fund["ok"] or not world.state.get_code(world.address) or world.state.get_balance(world.address)<1:
        return limited("no_live_stage_after_small_independent_contribution")
    pending=[g for g,v in witness_claims.items() if world.read(g,world.other)>v]
    claim_values={g:world.read(g,world.other) for g in pending}
    before=world.snapshot()
    normal_low=world.call(normal,world.user,value=0)
    if not world.state.get_code(world.address):
        return limited("normal_path_already_allows_termination")
    world.restore(before)
    early=world.call(fn,world.user,value=0)
    if not early["ok"] or world.state.get_code(world.address) or not early["beneficiaries"]:
        return limited("alternative_cannot_terminate_in_the_same_live_state")
    for amount in plan["threshold_values"]:
        world.restore(before)
        regular=world.call(normal,world.user,value=amount)
        if not regular["ok"] or world.state.get_code(world.address) or regular["beneficiaries"]!=early["beneficiaries"]:
            continue
        detail={"low_normal":[fund,normal_low],"early":[fund,early],"normal_completion":[fund,regular]}
        # Having contributed to a goal is not proof of a right to continued service.
        # The source must link a live claim to an actual payout for the same holder.
        for getter in pending:
            for payout in plan["redemption_entries"].get(getter,[]):
                world.restore(before)
                out=world.call(payout,world.other,number=1)
                if (out["ok"] and any(n["success"] and n["to"]==world.other.hex() and n["value"]>0 for n in out["nested_calls"])
                        and world.state.get_code(world.address) and world.read(getter,world.other)<claim_values[getter]):
                    return {"status":"witness","reason":"early_termination_disables_independently_redeemable_third_party_claim",
                            "redeem":out,"claim_getter":getter,**detail}
        return limited("different_termination_stage_observed_but_no_independent_live_right",**detail)
    return limited("normal_completion_at_same_destination_not_observed")


def fund_holders(world,getter,move):
    supply=world.read(getter,world.admin)
    q=min(1024,supply//4)
    if q<4:
        raise Unavailable("deployer_has_insufficient_observed_transferable_units")
    receipts=[]
    for who in (world.user,world.other):
        before=world.read(getter,who)
        reserve=world.read(getter,world.admin)
        r=world.call(move,world.admin,[who,q])
        credited=world.read(getter,who)-before
        if not r["ok"] or credited<=0 or reserve-world.read(getter,world.admin)<credited:
            raise Unavailable("no_ordinary_distribution_to_test_accounts")
        receipts.append(r)
    return receipts, max(1,min(world.read(getter,world.user),world.read(getter,world.other),q)//2)


def freeze(world,plan):
    setter,move=plan["fn"],plan["peer"]
    marker=plan["getter"];balance=plan["asset_getter"]
    if world.funcs[setter]["types"] not in (["address"],["address","bool"],["address","uint256"]):
        return limited("setter_argument_profile_not_executable")
    funds,n=fund_holders(world,balance,move)
    before=world.snapshot()
    for receiver_side in (False,True):
        world.restore(before)
        holder=world.user
        to=world.recipient
        selected=to if receiver_side else holder
        original=world.read(marker,selected)
        args=world.arguments(setter,selected,1)
        normal_before=world.read(balance,to)
        normal=world.call(move,holder,[to,n])
        if not normal["ok"] or world.read(balance,to)<=normal_before:continue
        world.restore(before)
        denied=world.call(setter,world.delegate,args)
        if world.read(marker,selected)!=original or denied["ok"]:continue
        world.restore(before)
        priv=world.call(setter,world.admin,args)
        if not priv["ok"] or world.read(marker,selected)==original:continue
        held=world.read(balance,holder)
        blocked=world.call(move,holder,[to,n])
        if blocked["ok"] and blocked["output"]!="00"*32:continue
        if world.read(balance,holder)!=held or world.read(balance,to)!=normal_before:continue
        dest=world.delegate
        other_before=world.read(balance,dest)
        other=world.call(move,world.other,[dest,n])
        if not other["ok"] or world.read(balance,dest)<=other_before:continue
        return {"status":"witness","reason":"privileged_account_specific_block_of_a_working_asset_request",
                "selected_endpoint":"recipient" if receiver_side else "holder","setup":funds,"normal":normal,
                "stranger_configuration":denied,"privileged_configuration":priv,"blocked":blocked,"unaffected":other}
    return limited("no_account_specific_differential_with_independent_transfer_control")


def genesis_holder_loss(world,plan):
    setter,move=plan["fn"],plan["peer"]
    balance,allowance=plan["asset_getter"],plan["allowance"]
    for ordinary in plan["moves"][:2]:
        world.restore(world.origin)
        try:
            funds,n=fund_holders(world,balance,ordinary)
        except Unavailable:
            continue
        if n<2:continue
        funded=world.snapshot()
        for grant in plan["grants"][:2]:
            world.restore(funded)
            # Deliberately grant strictly less than the gross request.
            limit=n-1
            consent=world.call(grant,world.user,[world.delegate,limit])
            if not consent["ok"] or world.read(allowance,world.user,world.delegate)!=limit:continue
            base=world.snapshot()
            args=[world.user,world.recipient,n]
            ordinary_try=world.call(move,world.delegate,args)
            if ordinary_try["ok"] and ordinary_try["output"]!="00"*32:continue
            for rate in (1,10,100):
                world.restore(base)
                old=world.read(plan["getter"])
                deny=world.call(setter,world.delegate,[rate])
                if deny["ok"] or world.read(plan["getter"])!=old:continue
                world.restore(base)
                before_credit=world.read(balance,world.recipient)
                before_debit=world.read(balance,world.user)
                configured=world.call(setter,world.admin,[rate])
                if not configured["ok"] or world.read(plan["getter"])==old:continue
                if world.read(balance,world.user)!=before_debit or world.read(balance,world.recipient)!=before_credit:continue
                supplies={g:world.read(g) for g in plan["aggregate_getters"]}
                admitted=world.call(move,world.delegate,args)
                gross=before_debit-world.read(balance,world.user)
                net=world.read(balance,world.recipient)-before_credit
                if not admitted["ok"] or not (0<net<=limit<gross):continue
                difference=gross-net
                consumed=limit-world.read(allowance,world.user,world.delegate)
                if consumed!=net:continue
                lost=[g for g,v in supplies.items() if v-world.read(g)==difference]
                # A scalar alone cannot establish that it is total supply. Require an
                # independently bound total-supply model from the source analysis.
                if not set(lost).intersection(plan.get("source_supply_getters",[])):continue
                if admitted["nested_calls"] or admitted["beneficiaries"]:continue
                allowed_slots={world.unique_getter_slot(balance,world.user),world.unique_getter_slot(balance,world.recipient),
                    world.unique_getter_slot(allowance,world.user,world.delegate)}
                allowed_slots.update(world.unique_getter_slot(g) for g in set(lost).intersection(plan["source_supply_getters"]))
                if any((a,s) not in allowed_slots for a,s,_,_ in admitted["changed_slots"]):continue
                return {"status":"witness","reason":"privileged_configuration_disposes_more_holder_units_than_transfer_consent",
                        "setup":funds,"grant":consent,"old_request":ordinary_try,"stranger_setter":deny,
                        "new_setting":configured,"new_request":admitted,"gross":gross,"net":net,"charged":consumed,
                        "verified_supply_loss":difference}
    return limited("no_reproducible_uncompensated_loss_beyond_real_allowance")


def holder_loss(world,plan):
    old=genesis_holder_loss(world,plan)
    if old["status"]=="witness":
        return old
    from .m31_fee import compare_rate
    world.restore(world.origin)
    contrast=compare_rate(world,plan)
    if contrast["status"]=="witness":
        return contrast
    return {**old,"rate_contrast_limit":contrast["reason"]}


RUNNERS={"acquire_then_use":acquisition,"repeat_credit":repeat_credit,"early_termination":early_termination,
         "restrict_account":freeze,"holder_loss":holder_loss}

