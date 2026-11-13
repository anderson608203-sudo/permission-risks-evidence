"""Source-corroborated authorization lifetime queries, independent of field names."""
import copy
from .core import digest
from .m03_p_paths import key,walk,op,lit
from .m03_p_route import keys,selectors,effective_permission,value_type,contains_sender,relocate

def temporal_queries(context,state):
    rows=[]
    for tid,lookup in state["lookups"].items():
        program={fn:paths for (target,fn),paths in state["paths"].items() if target==tid}
        grants=[]
        for issuer,branches in program.items():
            for p in branches:
                if p["flow"] not in ("normal","returned") or p["issues"] or not effective_permission(p["guards"],lookup):continue
                enabled=[w for w in p["writes"] if w["value"]==lit(True) and value_type(w["path"],lookup)=="bool" and keys(w["path"])]
                for role in enabled:
                    for deadline in p["writes"]:
                        if value_type(deadline["path"],lookup) not in ("uint","uint256") or key(keys(role["path"]))!=key(keys(deadline["path"])):continue
                        value=deadline["value"]
                        future=any(n.get("kind")=="op" and n.get("op") in (">",">=","<","<=")
                            and any(x.get("kind")=="environment" and x.get("field")=="timestamp" for x in walk(n))
                            and any(key(x)==key(value) for x in walk(n)) for g in p["guards"] for n in walk(g))
                        if future:grants.append((issuer,role,deadline))
        for fn,branches in program.items():
            for pi,path in enumerate(branches):
                if path["flow"] not in ("normal","returned") or path["issues"]:continue
                actual=[s for a in effective_permission(path["guards"],lookup) for s in selectors(a) if value_type(s,lookup)=="bool" and contains_sender(s)]
                for issuer,role,deadline in grants:
                    for check in actual:
                        if check["root"]!=role["path"]["root"]:continue
                        expected=relocate(deadline["path"],role["path"],check)
                        valid=op("<",{"kind":"environment","field":"timestamp"},expected)
                        for w in path["writes"]:
                            if w["path"]["root"] in (role["path"]["root"],deadline["path"]["root"]):continue
                            row={"rule":"AC-04","target":tid,"function":fn,"path_index":pi,
                                "program_id":context["identity"]["program_id"],"build_id":context["identity"]["build_id"],
                                "conditions":copy.deepcopy(path["guards"]),"issues":[],
                                "effect":{"object":lookup.nodes[w["path"]["root"]]["name"],"selector":w["path"],"value":w["value"],
                                    "operator":w["operator"],"source":w["source"]},
                                "required_policy_candidate":valid,
                                "policy_basis":{"basis":"issued_future_expiry","validity_assumptions":[op(">",expected,lit(0))],
                                    "issuer":issuer,"grant_source":role["source"],"deadline_source":deadline["source"],
                                    "scope":"co-issued caller-indexed authorization and future expiry; finite current-use check"},
                                "source_evaluation_terms":path.get("evaluated_terms",[])}
                            row["id"]="q_"+digest(row);rows.append(row)
    return rows

def sensitive_queries(context,state):
    """Include native effects without requiring an unrelated storage write."""
    from .m03_p_assets import deltas,polynomial,negative,holder_path
    rows=[]
    for tid,lookup in state["lookups"].items():
        program={fn:paths for (target,fn),paths in state["paths"].items() if target==tid}
        peers=[]
        for fn,branches in program.items():
            for path in branches:
                if path["flow"] not in ("normal","returned") or path["issues"]:continue
                for effect in path.get("sensitive_effects",[]):
                    for permission in effective_permission(path["guards"],lookup):peers.append((effect["kind"],permission,fn,effect["source"]))
        for fn,branches in program.items():
            for pi,path in enumerate(branches):
                if path["flow"] not in ("normal","returned"):continue
                for effect in path.get("sensitive_effects",[]):
                    if effect["kind"] not in ("native_transfer","native_selfdestruct"):continue
                    amount=polynomial(effect["amount"])
                    ordinary=(effect["recipient"].get("kind")=="actual_sender" and amount and
                        any(holder_path(d["write"]["path"],lookup) and keys(d["write"]["path"])[0].get("kind")=="actual_sender"
                            and d["delta"]==negative(amount) for d in deltas(path)))
                    if ordinary:continue
                    hypotheses=[(p,{"basis":"same_source_native_reserve_guard","peer":peer,"peer_source":source})
                        for kind,p,peer,source in peers if kind==effect["kind"]]
                    from .m25_reserve import reserve_disposition
                    disposition=reserve_disposition(fn,path,effect,lookup,program)
                    if disposition:hypotheses.append(disposition)
                    # Arbitrary caller-selected reserve withdrawal is distinct
                    # from forwarding msg.value or a holder-accounted payout.
                    # Infer local management from source governance of the
                    # selected beneficiary, not from a function name.
                    recipient_roots={s['root'] for s in selectors(effect['recipient'])}
                    caller_amount=any(n.get('kind')=='parameter' for n in walk(effect['amount']))
                    if caller_amount and not any(n.get('kind')=='transaction_value' for n in walk(effect['amount'])):
                        control=[]
                        for controller,paths in program.items():
                            for candidate in paths:
                                if candidate['flow'] not in ('normal','returned') or candidate['issues']:continue
                                if any(w['path']['root'] in recipient_roots for w in candidate['writes']):
                                    control.extend(effective_permission(candidate['guards'],lookup))
                        for recipient in selectors(effect['recipient']):
                            if not recipient.get('segments') and any(any(s['root']==recipient['root'] for s in selectors(g)) for paths in program.values() for candidate in paths for g in effective_permission(candidate['guards'],lookup)):
                                control.append(op('==',{'kind':'actual_sender'},recipient))
                        if control:hypotheses.append((op('or',*list({key(p):p for p in control}.values())),{'basis':'source_managed_reserve_disposition','scope':'caller-selected amount from contract reserve to a governed beneficiary; conditional inferred management policy'}))
                    for guard in path["guards"]:
                        for atom in walk(guard):
                            if atom.get("kind")=="op" and atom.get("op")=="==":
                                for a,b in (atom["args"],atom["args"][::-1]):
                                    if a.get("kind")=="transaction_origin" and b.get("kind")=="storage" and value_type(b,lookup) in ("address","address payable"):
                                        hypotheses.append((op("==",{"kind":"actual_sender"},b),{"basis":"transaction_origin_is_not_immediate_caller"}))
                    for required,basis in hypotheses:
                        available={n["id"] for n in walk(path) if n.get("kind")=="parameter"}
                        if not {n["id"] for n in walk(required) if n.get("kind")=="parameter"}<=available:continue
                        row={"rule":"AC-01","target":tid,"function":fn,"path_index":pi,
                            "program_id":context["identity"]["program_id"],"build_id":context["identity"]["build_id"],
                            "conditions":path["guards"]+effect.get("call_path_conditions",[]),"issues":path["issues"],
                            "effect":{**effect,"object":effect["kind"],"selector":{"kind":"non_storage_effect","source_id":effect["source"]["ast_id"]}},
                            "required_policy_candidate":required,"policy_basis":basis,
                            "source_evaluation_terms":path.get("evaluated_terms",[])}
                        row["id"]="q_"+digest(row);rows.append(row)
    return rows

def dangerous_entry_queries(context,state):
    """Protected delegate invocation itself; does not invent effects of the callee."""
    from .m26_code_paths import committed_invocation
    rows=[]
    for tid,lookup in state["lookups"].items():
        effects=[]
        for (target,fn),paths in state["paths"].items():
            if target!=tid:continue
            for pi,path in enumerate(paths):
                for effect in path.get("sensitive_effects",[]):
                    if effect["kind"]=="dangerous_external_call":
                        evidence=committed_invocation(path,effect)
                        if evidence is not None:effects.append((fn,pi,effect,evidence))
        for fn,pi,effect,(guards,terms) in effects:
            for peer,_,guarded,_ in effects:
                if key(effect["recipient"])!=key(guarded["recipient"]):continue
                for policy in effective_permission(guarded["prefix_conditions"],lookup):
                    # Never import another function's argument identities.
                    if any(n.get("kind")=="parameter" for n in walk(policy)):continue
                    row={"rule":"AC-01","target":tid,"function":fn,"path_index":pi,
                        "program_id":context["identity"]["program_id"],"build_id":context["identity"]["build_id"],
                        "conditions":copy.deepcopy(guards),"issues":[],
                        "effect":{**effect,"kind":"protected_delegate_entry","object":"protected_delegate_entry",
                                  "selector":{"kind":"non_storage_effect","source_id":effect["source"]["ast_id"]}},
                        "required_policy_candidate":policy,
                        "policy_basis":{"basis":"same_source_delegate_target_guard","peer":peer,"peer_source":guarded["source"],
                            "scope":"unauthorized entry to protected delegation; external downstream state effect not claimed"},
                        "source_evaluation_terms":terms}
                    row["id"]="q_"+digest(row);rows.append(row)
    return rows
