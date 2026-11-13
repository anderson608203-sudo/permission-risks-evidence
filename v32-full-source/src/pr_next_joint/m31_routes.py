"""Additional routes from a shared access/effect graph. All routes require independent, committed observations."""
from .facts import walk
from .m30_graph import root_of, typename
from .source_entry_identity import builtin_call


def caller(expr, lookup):
    if expr.get("nodeType") == "MemberAccess":
        return expr.get("memberName") == "sender" and expr.get("expression", {}).get("name") == "msg"
    if expr.get("nodeType") == "FunctionCall":
        decl = lookup.nodes.get(expr.get("expression", {}).get("referencedDeclaration"), {})
        statements = (decl.get("body") or {}).get("statements", [])
        if len(statements) == 1 and statements[0].get("nodeType") == "Return":
            result = statements[0].get("expression", {})
            return result.get("memberName") == "sender" and result.get("expression", {}).get("name") == "msg"
    return False


def caller_gates(info, lookup):
    gates = {}
    for site in info["guard_sites"]:
        n = lookup.nodes[site]
        if n.get("operator") not in ("==", "!="):
            continue
        left, right = n.get("leftExpression", {}), n.get("rightExpression", {})
        for subject, role in ((left, right), (right, left)):
            root = root_of(role)
            if (caller(subject, lookup) and role.get("nodeType") == "Identifier"
                    and lookup.decls.get(root, {}).get("stateVariable") and typename(role) == "address"):
                gates.setdefault(root, []).append(site)
    return gates


def payout_sites(info, lookup):
    sites = []
    for k in info["sites"]:
        n = lookup.nodes.get(k, {})
        if n.get("nodeType") != "FunctionCall":
            continue
        expr = n.get("expression", {})
        if expr.get("memberName") in ("transfer", "send") and typename(expr.get("expression", {})) == "address":
            sites.append(k)
        elif expr.get("nodeType") == "FunctionCallOptions" and "value" in expr.get("names", []):
            sites.append(k)
        elif expr.get("nodeType") == "FunctionCall" and expr.get("expression", {}).get("memberName") == "value":
            sites.append(k)
    return sorted(sites)


def initial_issue_totals(lookup, root, observable):
    """A constructor seeds the holder's actual spendable balance from this scalar."""
    totals=set()
    for decl in lookup.nodes.values():
        if decl.get("nodeType")!="FunctionDefinition" or not (decl.get("kind")=="constructor" or decl.get("isConstructor")):
            continue
        for n in walk(decl.get("body") or {}):
            if n.get("nodeType")!="Assignment" or n.get("operator")!="=":
                continue
            lhs=n.get("leftHandSide",{}); rhs=n.get("rightHandSide",{})
            if root_of(lhs)!=root or not caller(lhs.get("indexExpression",{}),lookup) or rhs.get("nodeType")!="Identifier":
                continue
            getter=observable.get(root_of(rhs))
            if getter and lookup.abi[getter]["types"]==[] and lookup.abi[getter]["outputs"]==["uint256"]:
                totals.add(getter)
    return sorted(totals)


def terminal_precedes_guards(info, lookup):
    """A later conditional in the same body cannot guard an unconditional EVM halt."""
    entry = lookup.function(info["op"]["function"]) or {}
    if entry.get("modifiers"):
        return False
    for statement in (entry.get("body") or {}).get("statements", []):
        expr = statement.get("expression", {})
        if (statement.get("nodeType") == "ExpressionStatement" and expr.get("id") in info["end"]
                and builtin_call(expr, lookup, ("suicide", "selfdestruct"))):
            return True
        # Only local declarations without initializers can precede the terminal.
        if statement.get("nodeType") != "VariableDeclarationStatement" or statement.get("initialValue"):
            return False
    return False


def extend(context, lookup, infos, obs, add):
    ac = context["analysis_scope"] == "AC"
    abi = lookup.abi
    guards = {v["op"]["id"]: caller_gates(v, lookup) for v in infos}
    cash = {v["op"]["id"]: payout_sites(v, lookup) for v in infos} if ac else {}
    def types(v):
        return abi.get(v["op"]["function"], {}).get("types", [])
    for write in infos:
        fn = write["op"]["function"]
        if ac:
            for site, root, op, lhs, rhs in write["writes"]:
                if op != "=" or lhs.get("nodeType") != "Identifier" or typename(lhs) != "address":
                    continue
                # Local role address must come from the caller or an argument. A fixed payout target is insufficient.
                if not (caller(rhs, lookup) or (rhs.get("nodeType") == "Identifier" and typename(rhs) == "address"
                           and not lookup.decls.get(rhs.get("referencedDeclaration"), {}).get("stateVariable"))):
                    continue
                for use in infos:
                    sites = guards[use["op"]["id"]].get(root)
                    if (sites or root in use["read_roots"]) and (use["writes"] or cash[use["op"]["id"]] or use["end"]):
                        add("authority_race", write, use, site, root, {"guard_sites":sites or []}, bool(sites))
            if not write["end"]:
                continue
            if (write["guard_sites"] or write["guard_roots"]) and not terminal_precedes_guards(write, lookup):
                continue
            for redeem in infos:
                pays = cash[redeem["op"]["id"]]
                if not pays or write is redeem:
                    continue
                deposits = []
                for deposit in infos:
                    f = lookup.function(deposit["op"]["function"]) or {}
                    if not (f.get("payable") or f.get("stateMutability") == "payable"):
                        continue
                    # The exact same state declaration must link the independent funding and redemption operations.
                    # A receiver address alone carries no evidence of an active claim.
                    roots = sorted({w[1] for w in deposit["writes"]} & redeem["read_roots"])
                    if roots:
                        deposits.append({"entry":deposit["op"]["function"], "roots":roots})
                if deposits:
                    for site in write["end"]:
                        add("live_redemption_close", write, redeem, site, None, {"deposits":deposits,"payout_sites":pays}, True)
            continue
        for site, root, op, lhs, rhs in write["writes"]:
            getter = obs.get(root)
            if not getter:
                continue
            out = abi[getter]
            if (out["types"] == ["address"] and out["outputs"] in (["bool"],["uint256"])
                    and types(write)[:1] == ["address"] and len(types(write)) <= 4):
                for route in infos:
                    if root not in route["read_roots"] or types(route) not in (["address","uint256"],["address","address","uint256"]):
                        continue
                    for asset in sorted({w[1] for w in route["writes"]}):
                        bal = obs.get(asset)
                        if asset == root or not bal or abi[bal]["types"] != ["address"] or abi[bal]["outputs"] != ["uint256"]:
                            continue
                        moves = [p["op"]["function"] for p in infos if types(p) == ["address","uint256"] and any(w[1] == asset for w in p["writes"])]
                        permissions = []
                        for ar, grantgetter in obs.items():
                            if ar in route["read_roots"] and abi[grantgetter]["types"] == ["address","address"] and abi[grantgetter]["outputs"] == ["uint256"]:
                                permissions.extend((p["op"]["function"],grantgetter) for p in infos if types(p) == ["address","uint256"] and any(w[1]==ar for w in p["writes"]))
                        delegated = len(types(route)) == 3
                        if moves and (permissions or not delegated):
                            add("qualified_freeze",write,route,site,root,{"getter":getter,"asset_getter":bal,"moves":sorted(set(moves)),
                                "grants":sorted(set(permissions)), "delegated":delegated},True)
            if (types(write) != ["address","uint256"] or out["types"] != ["address"] or out["outputs"] != ["uint256"]
                    or not guards[write["op"]["id"]] or lhs.get("nodeType") != "IndexAccess"):
                continue
            # An amount authorised for a normal payment and a privileged destruction of the same holder balance.
            for route in infos:
                if types(route) != ["address","address","uint256"] or not any(w[1]==root for w in route["writes"]):
                    continue
                for ar, allowance in obs.items():
                    if (ar not in route["read_roots"] or ar not in write["read_roots"]
                            or abi[allowance]["types"] != ["address","address"] or abi[allowance]["outputs"] != ["uint256"]):
                        continue
                    grants = [p["op"]["function"] for p in infos if types(p)==["address","uint256"] and any(w[1]==ar for w in p["writes"])]
                    moves = [p["op"]["function"] for p in infos if types(p)==["address","uint256"] and p is not write and any(w[1]==root for w in p["writes"])]
                    if grants and moves:
                        add("privileged_allowance_burn",write,route,site,root,{"asset_getter":getter,"allowance":allowance,
                            "grants":sorted(set(grants)), "moves":sorted(set(moves)),
                            "initial_issue_totals":initial_issue_totals(lookup,root,obs)},True)

