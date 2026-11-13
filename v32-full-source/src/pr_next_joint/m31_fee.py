"""Compare the same real allowance and transfer under two reachable fee settings."""
from .m30_witness import fund_holders, limited
from .m30_evm import Unavailable


def unchanged_request(w, operation, actor, args, observations):
    before = [w.read(getter, *keys) for getter, keys in observations]
    receipt = w.call(operation, actor, args)
    after = [w.read(getter, *keys) for getter, keys in observations]
    if before != after or receipt["changed_slots"] or receipt["beneficiaries"]:
        return None
    if receipt["ok"]:
        return receipt if receipt["output"] == "00" * 32 else None
    return receipt if receipt["error"] in ("Revert","InvalidInstruction") else None


def reference_rate(w, p, n, balance, allowance, grants):
    # A positive minimum rate may round to zero for this particular amount.
    # Establish absence of a charge on the identical transfer, using real transactions.
    start = w.snapshot()
    current = w.read(p["getter"])
    for reference in dict.fromkeys((0, current, 1)):
        w.restore(start)
        setting = w.call(p["fn"], w.admin, [reference])
        if not setting["ok"] or w.read(p["getter"]) != reference:
            continue
        at_rate = w.snapshot()
        for grant in grants:
            w.restore(at_rate)
            permission = w.call(grant, w.user, [w.delegate, n])
            if not permission["ok"] or w.read(allowance,w.user,w.delegate) != n:
                continue
            debit, credit = w.read(balance,w.user), w.read(balance,w.recipient)
            transfer = w.call(p["peer"],w.delegate,[w.user,w.recipient,n])
            if (transfer["ok"] and debit-w.read(balance,w.user)==n and w.read(balance,w.recipient)-credit==n
                    and w.read(allowance,w.user,w.delegate)==0):
                w.restore(at_rate)
                return setting, reference
    return None


def compare_rate(w, p):
    amount_getter, allowance, rate=p["asset_getter"],p["allowance"],p["getter"]
    supply=set(p.get("source_supply_getters",[])) | set(p.get("initial_issue_totals",[]))
    supply=sorted(supply.intersection(p["aggregate_getters"]))
    if not supply:
        return limited("no_independently_bound_issuance_total")
    for ordinary in p["moves"][:4]:
        w.restore(w.origin)
        try:receipts,n=fund_holders(w,amount_getter,ordinary)
        except Unavailable:continue
        if n<2:continue
        funded=w.snapshot()
        # Use an administrator transaction, not a fabricated zero-valued storage cell.
        grants=p["grants"][:4]
        reference=reference_rate(w,p,n,amount_getter,allowance,grants)
        if reference is None:continue
        neutral,normal_rate=reference
        neutral_state=w.snapshot()
        for grant in p["grants"][:4]:
            w.restore(neutral_state)
            full=w.call(grant,w.user,[w.delegate,n])
            if not full["ok"] or w.read(allowance,w.user,w.delegate)!=n:continue
            debit=w.read(amount_getter,w.user); credit=w.read(amount_getter,w.recipient)
            totals={g:w.read(g) for g in supply}
            args=[w.user,w.recipient,n]
            transfer=w.call(p["peer"],w.delegate,args)
            conserved=[g for g,t in totals.items() if t>0 and t==w.read(g)]
            if not(transfer["ok"] and conserved and debit-w.read(amount_getter,w.user)==n
                   and w.read(amount_getter,w.recipient)-credit==n and w.read(allowance,w.user,w.delegate)==0):
                continue
            w.restore(neutral_state)
            limit=n-1
            grant_proof=w.call(grant,w.user,[w.delegate,limit])
            if not grant_proof["ok"] or w.read(allowance,w.user,w.delegate)!=limit:continue
            base=w.snapshot()
            observations=[(amount_getter,[w.user]),(amount_getter,[w.recipient]),(allowance,[w.user,w.delegate])]
            old=unchanged_request(w,p["peer"],w.delegate,args,observations)
            if old is None:continue
            for value in (1,10,30,100):
                if value==normal_rate:continue
                w.restore(base)
                refused=unchanged_request(w,p["fn"],w.other,[value],[(rate,[])])
                if refused is None:continue
                w.restore(base)
                before=w.read(amount_getter,w.user);recipient=w.read(amount_getter,w.recipient)
                setting=w.call(p["fn"],w.admin,[value])
                if not setting["ok"] or w.read(rate)!=value or w.read(amount_getter,w.user)!=before or w.read(amount_getter,w.recipient)!=recipient or w.read(allowance,w.user,w.delegate)!=limit:continue
                totals={g:w.read(g) for g in conserved}
                actual=w.call(p["peer"],w.delegate,args)
                gross=before-w.read(amount_getter,w.user)
                net=w.read(amount_getter,w.recipient)-recipient
                used=limit-w.read(allowance,w.user,w.delegate)
                if not(actual["ok"] and 0<used==net<=limit<gross and not actual["nested_calls"] and not actual["beneficiaries"]):continue
                falls=[g for g in conserved if totals[g]-w.read(g)==gross-net]
                if not falls:continue
                allowed={w.unique_getter_slot(amount_getter,w.user),w.unique_getter_slot(amount_getter,w.recipient),
                         w.unique_getter_slot(allowance,w.user,w.delegate)}
                allowed.update(w.unique_getter_slot(g) for g in falls)
                if any((a,s) not in allowed for a,s,*_ in actual["changed_slots"]):continue
                return {"status":"witness","reason":"privileged_rate_introduces_verified_uncompensated_holder_loss_beyond_general_allowance",
                        "reference_rate":normal_rate,"changed_rate":value,
                        "distribution":receipts,"neutral_setting":neutral,"ordinary_full_grant":full,"ordinary_transfer":transfer,
                        "general_limit":limit,"grant":grant_proof,"neutral_request":old,"stranger_setting":refused,"changed_setting":setting,
                        "request":actual,"gross":gross,"net":net,"allowance_used":used,"issued_total_decline":gross-net,
                        "aggregate_observers":falls,"restriction":"conditional on the two reachable on-chain configurations and recorded deployment"}
        w.restore(funded)
    return limited("neutral_comparator_and_conserved_uncompensated_settlement_not_established")

