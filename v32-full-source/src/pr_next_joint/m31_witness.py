"""Bounded rights experiments on original executable code; every branch uses the same initial state."""
from .m30_evm import Unavailable
from .m30_witness import limited, fund_holders


def changed(receipt):
    return receipt["ok"] and (bool(receipt["changed_slots"]) or bool(receipt["beneficiaries"]) or
          any(c["value"] and c["success"] for c in receipt["nested_calls"]))


def denied(r):
    # Gas exhaustion and unmodelled environment are not authorization refusals.
    return (not r["ok"] and r["error"] in ("Revert","InvalidInstruction")) or (r["ok"] and not changed(r))


def authority_race(w, p):
    root=w.snapshot()
    peer, setter=p["peer"],p["fn"]
    args=w.arguments(peer,w.recipient,1)
    def use(actor):
        state=w.state
        read=state.get_storage
        cells=set()
        def observe(address, slot, *a, **kw):
            cells.add((address.hex(),hex(slot)))
            return read(address,slot,*a,**kw)
        state.get_storage=observe
        try:
            r=w.call(peer,actor,args)
            r["observed_cells"]=sorted(cells)
            return r
        finally:
            del state.get_storage
    def claim(actor):
        return w.call(setter,actor,address=actor,number=1)
    def paid_or_external(r):
        return any(c["value"] or c["code_bytes"] for c in r["nested_calls"]) or bool(r["beneficiaries"])
    old_admin=use(w.admin)
    w.restore(root)
    old_user=use(w.user)
    if not denied(old_user):
        return limited("ordinary_actor_could_already_commit_or_failure_not_an_authority_refusal")
    w.restore(root)
    existing=changed(old_admin)
    normal_claim=None
    if not existing:
        if not denied(old_admin):
            return limited("cold_admin_failure_not_attributable_to_unclaimed_role")
        normal_claim=claim(w.admin)
        if not changed(normal_claim) or paid_or_external(normal_claim):
            return limited("ordinary_deployment_then_intended_initialization_not_reproduced")
    normal=w.snapshot()
    normal_use=use(w.admin)
    if not changed(normal_use):
        return limited("the_intended_role_has_no_demonstrated_sensitive_effect")
    w.restore(normal)
    denied_other=use(w.user)
    if not denied(denied_other):
        return limited("same_operation_available_to_unselected_actor")
    # If this is a replacement of an *existing* authority, establish that an independent third
    # actor can take it too; this excludes a preselected nominee supplied by deployment.
    if existing:
        w.restore(root)
        third=claim(w.other)
        if not changed(third) or paid_or_external(third) or not changed(use(w.other)):
            return limited("no_independent_second_takeover_of_existing_authority")
    w.restore(root)
    grant=claim(w.user)
    if not changed(grant) or paid_or_external(grant):
        return limited("free_public_establishment_not_observed")
    taken=w.snapshot()
    impostor=w.call(peer,w.other,args)
    if not denied(impostor):
        return limited("state_change_enables_all_callers_rather_than_the_chosen_manager")
    w.restore(taken)
    attack=use(w.user)
    if not changed(attack):
        return limited("claimed_role_cannot_exercise_the_same_protected_operation")
    # Check that the particular value replaced by the caller is actually read in
    # both the unsuccessful and the successful invocation of the protected entry.
    assigned={(a,s) for a,s,b,end in grant["changed_slots"] if int(end,16)==int.from_bytes(w.user,"big")
              and int(b,16)!=int(end,16) and a==w.address.hex()}
    linked=assigned.intersection(map(tuple,old_user["observed_cells"]),map(tuple,attack["observed_cells"]))
    if not linked:
        return limited("changed_role_not_observed_by_both_permission_branches")
    return {"status":"witness","reason":("unprivileged_replacement_of_independently_active_authority" if existing else
        "uninvited_first_claim_and_use_of_uninitialized_global_authority"),"role_was_active":existing,
        "ordinary_before":old_user,"intended_claim":normal_claim,"intended_use":normal_use,"unauthorized_after_intended":denied_other,
        "first_claim_or_takeover":grant,"unselected_actor":impostor,"selected_actor":attack,"causal_cells":sorted(linked),
        "limit":"concrete code/deployment and independent ordinary callers; first-claim risk requires a public initialization window"}


def paid_to(r, actor):
    return sum(c["value"] for c in r["nested_calls"] if c["success"] and c["to"]==actor.hex())


def live_redemption_close(w,p):
    if w.name in ("cancun","prague"):
        return limited("persistent_code_is_not_removed_on_this_fork")
    for dep in p["deposits"][:4]:
        for value in (1,10**17,10**18):
            w.restore(w.origin)
            funding=w.call(dep["entry"],w.other,value=value,number=1)
            if not changed(funding) or not w.state.get_code(w.address) or w.state.get_balance(w.address)<value:
                continue
            live=w.snapshot()
            # Distinguish an existing depositor-specific right from a prize or publicly available faucet.
            for n in (1,value):
                w.restore(live)
                rightful=w.call(p["peer"],w.other,address=w.other,number=n)
                if not rightful["ok"] or paid_to(rightful,w.other)<=0 or not w.state.get_code(w.address):
                    continue
                w.restore(live)
                stranger=w.call(p["peer"],w.user,address=w.user,number=n)
                if paid_to(stranger,w.user) or not (stranger["ok"] or denied(stranger)):
                    continue
                w.restore(live)
                old=w.state.get_balance(w.other)
                destroy=w.call(p["fn"],w.user,address=w.user,number=1)
                if (not destroy["ok"] or w.state.get_code(w.address) or not destroy["beneficiaries"] or
                    w.state.get_balance(w.other)!=old or paid_to(destroy,w.other)):
                    continue
                return {"status":"witness","reason":"outsider_terminates_live_third_party_redemption_without_payment",
                        "deposit":funding,"claim":rightful,"unrelated_account_attempt":stranger,"termination":destroy,
                        "redeemable_native_amount":paid_to(rightful,w.other),"source_linked_deposit":dep["entry"],
                        "limit":"actual previous holder payout in a counterfactual branch; persistent code deletion on the stated old fork only"}
    return limited("independent_unsettled_holder_specific_redemption_then_termination_not_established")


def issued_permission(w,p,holder,spender,n):
    for grant,observable in p["grants"]:
        from_state=w.snapshot()
        r=w.call(grant,holder,[spender,n])
        if (r["ok"] and not r["nested_calls"] and w.read(observable,holder,spender)==n):
            return r
        w.restore(from_state)
    raise Unavailable("could_not_create_a_general_holder_allowance")


def setup_freeze(w,p,operator):
    # State is reached by actual transfers and allowances. No balance or storage edits.
    for move in p["moves"][:4]:
        w.restore(w.origin)
        try:
            funds,n=fund_holders(w,p["asset_getter"],move)
            if p["delegated"]:
                funds += [issued_permission(w,p,owner,operator,n) for owner in (w.user,w.other)]
            return funds,n
        except Unavailable:
            continue
    raise Unavailable("no_reachable_independent_holders_with_required_permissions")


def qualified_freeze(w,p):
    # Some genuine holder-authorized delivery services require a privileged operator as well.
    operators = (w.delegate, w.admin) if p["delegated"] else (w.user,)
    failures = []
    for operator in operators:
        try:
            proof = freeze_branch(w, p, operator)
        except Unavailable as error:
            failures.append(str(error))
            continue
        if proof["status"] == "witness":
            return proof
        failures.append(proof["reason"])
    return {**limited("no_reproduced_restriction_on_tested_delivery_paths"), "tested_routes": failures}


def freeze_branch(w, p, operator):
    setter,route,balance,flag=p["fn"],p["peer"],p["asset_getter"],p["getter"]
    shape=w.funcs[setter]["types"]
    if shape not in (["address"],["address","bool"],["address","uint256"],["address","bool","uint256","uint256"]):
        return limited("setter_shape_not_executable_in_bounded_probe")
    funds,n=setup_freeze(w,p,operator)
    base=w.snapshot()
    def transfer(holder,recipient):
        if p["delegated"]:
            return w.call(route,operator,[holder,recipient,n])
        return w.call(route,holder,[recipient,n])
    # Destination accounts differ on the unaffected branch as well.
    for selected in (w.user,w.recipient):
        w.restore(base)
        dest_before=w.read(balance,w.recipient)
        source_before = w.read(balance,w.user)
        regular=transfer(w.user,w.recipient)
        if not regular["ok"] or w.read(balance,w.recipient)<=dest_before or w.read(balance,w.user)>=source_before:
            continue
        for parameter in ((True,),(False,)) if shape==["address","bool"] else ((),):
            w.restore(base)
            args=w.arguments(setter,selected,1)
            if parameter:args[1]=parameter[0]
            if len(args)==4:args[1:]=[True,w.header.timestamp-1,w.header.timestamp+3600]
            old=w.read(flag,selected)
            ordinary=w.call(setter,w.other,args)
            if not denied(ordinary) or w.read(flag,selected)!=old:continue
            w.restore(base)
            priv=w.call(setter,w.admin,args)
            if not priv["ok"] or w.read(flag,selected)==old:continue
            holder_before=w.read(balance,w.user)
            if w.read(balance,w.recipient)!=dest_before:continue
            blocked=transfer(w.user,w.recipient)
            if not (denied(blocked) or (blocked["ok"] and blocked["output"]=="00"*32)):continue
            if w.read(balance,w.user)!=holder_before or w.read(balance,w.recipient)!=dest_before:continue
            dest=w.delegate if operator==w.admin else w.admin
            other_before=w.read(balance,dest)
            other_holder_before=w.read(balance,w.other)
            independent=transfer(w.other,dest)
            if independent["ok"] and w.read(balance,dest)>other_before and w.read(balance,w.other)<other_holder_before:
                return {"status":"witness","reason":"account_specific_block_of_reachable_authorized_delivery",
                    "service_operator":operator.hex(),
                    "delegated":p["delegated"],"selected_endpoint":"recipient" if selected==w.recipient else "holder",
                    "funds_and_permissions":funds,"regular_request":regular,"ordinary_setting":ordinary,"privileged_setting":priv,
                    "blocked":blocked,"unaffected_request":independent}
    return limited("specific_account_restriction_did_not_block_a_previously_working_request")


def privileged_burn(w,p):
    balance,allowance=p["asset_getter"],p["allowance"]
    supplies=sorted(set(p.get("source_supply_getters",[])) | set(p.get("initial_issue_totals",[])))
    if not supplies:return limited("no_independently_source_bound_supply")
    for move in p["moves"][:4]:
        w.restore(w.origin)
        try:funds,n=fund_holders(w,balance,move)
        except Unavailable:continue
        # Issuance total must be conserved by a real transfer as well.
        start=w.snapshot()
        transferable={g:w.read(g) for g in supplies}
        probe=w.call(move,w.user,[w.recipient,1])
        kept=[g for g in supplies if probe["ok"] and transferable[g]>0 and w.read(g)==transferable[g]]
        if not kept:continue
        w.restore(start)
        for grant in p["grants"][:4]:
            w.restore(start)
            declarations=[w.call(grant,w.user,[who,n]) for who in (w.delegate,w.admin)]
            if not all(r["ok"] and not r["nested_calls"] for r in declarations):continue
            if any(w.read(allowance,w.user,who)!=n for who in (w.delegate,w.admin)):continue
            common=w.snapshot()
            native_payment=w.call(p["peer"],w.delegate,[w.user,w.recipient,n])
            if not native_payment["ok"] or w.read(allowance,w.user,w.delegate)!=0:continue
            w.restore(common)
            ordinary=w.call(p["fn"],w.delegate,[w.user,n])
            if not denied(ordinary):continue
            w.restore(common)
            before=w.read(balance,w.user)
            supply={g:w.read(g) for g in kept}
            burn=w.call(p["fn"],w.admin,[w.user,n])
            if not burn["ok"] or burn["nested_calls"] or burn["beneficiaries"] or w.read(balance,w.user)!=before-n:continue
            lost=[g for g in kept if supply[g]-w.read(g)==n]
            if not lost:continue
            slots={w.unique_getter_slot(balance,w.user),w.unique_getter_slot(allowance,w.user,w.admin)}
            slots.update(w.unique_getter_slot(g) for g in lost)
            if any((a,s) not in slots for a,s,*_ in burn["changed_slots"]):continue
            return {"status":"witness","reason":"privilege_exclusively_allows_destruction_of_another_holders_generally_approved_units",
                    "funding":funds,"general_approvals":declarations,"ordinary_transfer":native_payment,"ordinary_destruction":ordinary,
                    "privileged_destruction":burn,"verified_supply_and_holder_loss":n,"remaining_general_allowance":w.read(allowance,w.user,w.admin),
                    "limit":"within independently verified general transfer authorization; no separate destruction consent observed"}
    return limited("exclusive_privileged_uncompensated_destruction_not_reproduced")


RUNNERS={"authority_race":authority_race,"live_redemption_close":live_redemption_close,
         "qualified_freeze":qualified_freeze,"privileged_allowance_burn":privileged_burn}

