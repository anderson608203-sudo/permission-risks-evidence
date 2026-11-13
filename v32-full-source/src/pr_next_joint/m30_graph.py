"""Index operations by what they change and what another entry actually reads.
The graph nominates comparisons. It makes no authorization claim.
"""
from collections import defaultdict
import re
from .facts import walk
from .source_entry_identity import builtin_call


def root_of(node):
    while isinstance(node,dict):
        kind=node.get("nodeType")
        if kind=="Identifier":
            return node.get("referencedDeclaration")
        if kind=="IndexAccess":
            node=node.get("baseExpression")
        elif kind=="MemberAccess":
            node=node.get("expression")
        else:
            break
    return None


def typename(node):
    return node.get("typeDescriptions",{}).get("typeString","").replace(" payable","")


def info_for(op, lookup):
    facts={k:[] for k in ("writes","end","guard_roots","guard_sites","read_roots","scalar_comparisons")}
    sites=set(op["source_ast_ids"])
    for aid in op["source_ast_ids"]:
        n=lookup.nodes.get(aid,{})
        ref=n.get("referencedDeclaration")
        if ref in lookup.decls and lookup.decls[ref].get("stateVariable"):
            facts["read_roots"].append(ref)
        if n.get("nodeType")=="Assignment":
            lhs=n.get("leftHandSide",{})
            root=root_of(lhs)
            if root in lookup.decls and lookup.decls[root].get("stateVariable"):
                facts["writes"].append((aid,root,n.get("operator"),lhs,n.get("rightHandSide",{})))
        if n.get("nodeType")=="FunctionCall" and builtin_call(n,lookup,("suicide","selfdestruct")):
            facts["end"].append(aid)
        if n.get("nodeType")=="InlineAssembly":
            ast=n.get("AST") or {}
            assembly=n.get("operations") or ""
            if isinstance(assembly,str):
                assembly=re.sub(r"/\*.*?\*/|//[^\n]*"," ",assembly,flags=re.S)
            if (any(x.get("nodeType")=="YulFunctionCall" and x.get("functionName",{}).get("name") in ("suicide","selfdestruct") for x in walk(ast))
                    or isinstance(assembly,str) and re.search(r"\b(?:suicide|selfdestruct)\s*\(",assembly)):
                facts["end"].append(aid)
        condition=None
        if n.get("nodeType") in ("IfStatement","Conditional"):
            condition=n.get("condition")
        elif n.get("nodeType")=="FunctionCall" and builtin_call(n,lookup,("require","assert")):
            condition=next(iter(n.get("arguments",[])),None)
        elif n.get("nodeType")=="Return":
            condition=n.get("expression")
        if condition:
            for x in walk(condition):
                r=x.get("referencedDeclaration")
                if r in lookup.decls and lookup.decls[r].get("stateVariable"):
                    facts["guard_roots"].append(r)
                if x.get("nodeType")=="BinaryOperation":
                    facts["guard_sites"].append(x["id"])
                    if x.get("operator")=="==":
                        for left,right in [(x.get("leftExpression",{}),x.get("rightExpression",{})),
                                           (x.get("rightExpression",{}),x.get("leftExpression",{}))]:
                            rid=root_of(left)
                            if rid in lookup.decls and lookup.decls[rid].get("stateVariable") and typename(left)=="address" and typename(right)=="address":
                                facts["scalar_comparisons"].append(rid)
    info={**facts,"op":op,"sites":sites}
    for k in ("guard_roots","read_roots","scalar_comparisons"):
        info[k]=set(info[k])
    return info


def getters(lookup, operations):
    by_root={}
    for row in operations:
        op=row["op"];sig=op["function"]
        abi=lookup.abi.get(sig,{})
        if not abi.get("readonly") or len(abi.get("outputs",[]))!=1:
            continue
        entry=lookup.nodes.get(op["entry_ast_id"],{})
        if entry.get("stateVariable"):
            by_root[entry["id"]]=sig
            continue
        body=(entry.get("body") or {}).get("statements",[])
        if len(body)!=1 or body[0].get("nodeType")!="Return" or entry.get("modifiers"):
            continue
        expr=body[0].get("expression") or {}
        keys=[]
        while expr.get("nodeType")=="IndexAccess":
            key=expr.get("indexExpression") or {}
            if key.get("nodeType")!="Identifier":break
            keys.append(key.get("referencedDeclaration"));expr=expr.get("baseExpression") or {}
        root=expr.get("referencedDeclaration")
        parameters=[p.get("id") for p in (entry.get("parameters") or {}).get("parameters",[])]
        if expr.get("nodeType")=="Identifier" and root in lookup.decls and lookup.decls[root].get("stateVariable") and keys[::-1]==parameters:
            by_root.setdefault(root,sig)
    return by_root


def nomination_map(context, answer, operations):
    by_op={r["op"]["id"]:r for r in operations}
    result=defaultdict(set)
    for q in answer.get("behavior_questions",[]):
        if q["operation"] in by_op and q["comparison"] in by_op:
            result[q["operation"],q["comparison"],q["kind"]].add(q["id"])
    # Existing replies may identify a linked consumer without the new envelope.
    # Require source evidence and an explicitly named peer, never natural-language label matching.
    for r in answer.get("relations",[]):
        a=r["op_ref"]
        if a not in by_op:continue
        evidence={context["references"][x]["ast_id"] for x in r["source_refs"]}
        if not evidence.intersection(by_op[a]["sites"]):continue
        for link in r.get("operation_links",[]):
            left,right=link["from_op_ref"],link["to_op_ref"]
            if left not in by_op or right not in by_op:continue
            refs={context["references"][v]["ast_id"] for v in link["source_refs"]}
            if not refs.intersection(by_op[left]["sites"]) or not refs.intersection(by_op[right]["sites"]):continue
            kind={"authorization_use":"acquire_then_use","approval_execution":"acquire_then_use"}.get(link["kind"])
            if kind:result[left,right,kind].add(r["id"])
        for peer in r["related_op_refs"]:
            if peer not in by_op or peer==a:continue
            if r["relation_kind"] in ("checks_permission","controlled_by","credential_binds","guards_transfer","holder_of"):
                for kind in ("acquire_then_use","early_termination","repeat_credit","restrict_account","holder_loss"):
                    result[a,peer,kind].add(r["id"])
    return result


def plans(context,lookup,operations,answer):
    infos=[info_for(o,lookup) for o in operations if not o["generated_getter"] and not lookup.abi.get(o["function"],{}).get("readonly")]
    obs=getters(lookup,[{"op":o} for o in operations])
    from functools import lru_cache
    from .m31_routes import initial_issue_totals
    @lru_cache(maxsize=None)
    def constructor_totals(asset):
        return initial_issue_totals(lookup,asset,obs)
    nominations=nomination_map(context,answer,infos)
    funders=defaultdict(list)
    guards=defaultdict(list)
    transfers=defaultdict(list)
    spending=defaultdict(list)
    terminals=[]
    for info in infos:
        fn=info["op"]["function"]
        if info["end"]:terminals.append(info)
        for root in info["guard_roots"] | info["scalar_comparisons"]:
            guards[root].append(info)
        types=lookup.abi.get(fn,{}).get("types",[])
        for _,root,_,lhs,rhs in info["writes"]:
            if root not in obs:continue
            observable=lookup.abi[obs[root]]
            holder_balance=observable["types"]==["address"] and observable["outputs"]==["uint256"]
            if holder_balance and types==["address","uint256"] and typename(lhs).startswith("uint"):
                transfers[root].append(info)
            if holder_balance and types==["address","address","uint256"] and typename(lhs).startswith("uint"):
                spending[root].append(info)
            if types==["address","uint256"] and typename(lhs).startswith("uint") and lhs.get("baseExpression",{}).get("nodeType")=="IndexAccess":
                funders[root].append(info)
    out={}
    questions={q["id"]:q for q in answer.get("behavior_questions",[])}
    def add(kind,a,b,site,root,extra,structural):
        if a is b:return
        oid,pid=a["op"]["id"],b["op"]["id"]
        hints=[]
        compatible={"authority_race":"acquire_then_use","live_redemption_close":"early_termination",
                    "qualified_freeze":"restrict_account","privileged_allowance_burn":"holder_loss"}
        refs=set(nominations.get((oid,pid,kind),())) | set(nominations.get((oid,pid,compatible.get(kind)),()))
        for ref in sorted(refs):
            if ref in questions:
                q=questions[ref]
                effect_ids={n.get("id") for n in walk(lookup.nodes[site])}
                other_sites={w[0] for w in b["writes"]}|set(b["end"])|set(b["guard_sites"])|set(extra.get("payout_sites",[]))
                other_ids={n.get("id") for loc in other_sites for n in walk(lookup.nodes[loc])}
                if not any(context["references"][v]["ast_id"] in effect_ids for v in q["operation_refs"]):continue
                if not any(context["references"][v]["ast_id"] in other_ids for v in q["comparison_refs"]):continue
            hints.append(ref)
        if not (hints or structural):return
        key=(kind,oid,pid,site,root)
        out[key]={"kind":kind,"fn":a["op"]["function"],"peer":b["op"]["function"],"site":site,
                  "root":root,"nominations":hints,"structural":bool(structural),"target":a["op"]["target"],
                  "operation":oid,"comparison":pid,**extra}
    for a in infos:
        fn=a["op"]["function"]
        types=lookup.abi.get(fn,{}).get("types",[])
        for site,root,operator,lhs,rhs in a["writes"]:
            getter=obs.get(root)
            if not getter:continue
            gt=lookup.abi[getter]
            if context["analysis_scope"]=="AC":
                if operator=="=" and gt["types"]==[] and gt["outputs"]==["address"] and typename(rhs)=="address":
                    for b in infos:
                        if root not in b["guard_roots"] and not nominations.get((a["op"]["id"],b["op"]["id"],"acquire_then_use")):continue
                        # Re-keying an existing global authority is an observable, independently protected capability.
                        if not any(w[1]==root for w in b["writes"]):continue
                        ab=lookup.abi.get(b["op"]["function"],{})
                        if "address" not in ab.get("types",[]):continue
                        add("acquire_then_use",a,b,site,root,{"getter":getter},root in b["scalar_comparisons"])
                if operator=="=" and gt["types"]==["address"] and gt["outputs"]==["uint256"]:
                    # A direct full balance replacement and matched scalar replacement provide static grounds.
                    # With an explicit nomination, independently test a wider balance-writing operation.
                    scalar=[(w[1],obs[w[1]]) for w in a["writes"] if w[1] in obs and
                            lookup.abi[obs[w[1]]]["types"]==[] and lookup.abi[obs[w[1]]]["outputs"]==["uint256"]
                            and w[2]=="=" and (w[4].get("referencedDeclaration") is not None
                                and w[4].get("referencedDeclaration")==rhs.get("referencedDeclaration"))]
                    for b in transfers[root]:
                        # An existing self-service spend is checked again on the original bytecode.
                        if b["op"]["function"]==fn:continue
                        add("repeat_credit",a,b,site,root,{"getter":getter,"aggregate_getters":sorted({g for _,g in scalar})},bool(scalar))
            else:
                targets=set(x["op"]["id"] for x in guards[root])
                if gt["types"]==["address"] and gt["outputs"] in (["bool"],["uint256"]):
                    for asset,peers in transfers.items():
                        if asset==root:continue
                        for b in peers:
                            if root not in b["read_roots"] and not nominations.get((a["op"]["id"],b["op"]["id"],"restrict_account")):continue
                            add("restrict_account",a,b,site,root,{"getter":getter,"asset_getter":obs[asset]},
                                b["op"]["id"] in targets and types in (["address"],["address","bool"],["address","uint256"]))
                if gt["types"]==[] and gt["outputs"]==["uint256"] and types==["uint256"]:
                    for asset,peers in spending.items():
                        for b in peers:
                            if root not in b["read_roots"] and not nominations.get((a["op"]["id"],b["op"]["id"],"holder_loss")):continue
                            allowances=[r for r in b["read_roots"] if r in obs and lookup.abi[obs[r]]["types"]==["address","address"]]
                            for allowance in sorted(allowances):
                                grants=[v["op"]["function"] for v in funders.get(allowance,[])]
                                moves=[v["op"]["function"] for v in transfers.get(asset,[])]
                                supplies=[obs[w[1]] for w in b["writes"] if w[1] in obs and
                                          lookup.abi[obs[w[1]]]["types"]==[] and lookup.abi[obs[w[1]]]["outputs"]==["uint256"] and w[1]!=root]
                                if not (grants and moves and supplies):continue
                                add("holder_loss",a,b,site,root,{"getter":getter,"asset_getter":obs[asset],
                                    "allowance":obs[allowance],"grants":sorted(set(grants)),"moves":sorted(set(moves)),
                                    "aggregate_getters":sorted(set(supplies)),
                                    "initial_issue_totals":constructor_totals(asset)},root in b["read_roots"])
        if context["analysis_scope"]=="AC" and a["end"]:
            for b in terminals:
                if not b["guard_sites"] or not a["end"]:continue
                abi=lookup.function(b["op"]["function"]) or {}
                accepts=abi.get("stateMutability")=="payable" or abi.get("payable") is True
                # Existing external contribution or a protected service must be established separately in M4.
                if not accepts:continue
                for site in a["end"]:
                    claims={r:g for r,g in obs.items() if lookup.abi[g]["types"]==["address"] and lookup.abi[g]["outputs"]==["uint256"]}
                    payouts={g:sorted({v["op"]["function"] for v in infos if v is not a and v is not b and r in v["read_roots"]
                                      and any(w[1]==r for w in v["writes"])}) for r,g in claims.items()}
                    add("early_termination",a,b,site,None,{"claim_getters":list(claims.values()),"possible_payouts":payouts,
                        "peer_sites":b["end"],"peer_guards":b["guard_sites"]},True)
    from .m31_routes import extend
    extend(context,lookup,infos,obs,add)
    result=list(out.values())
    by_op={row["op"]["id"]:row for row in infos}
    for spec in list(result):
        dependencies=by_op[spec["operation"]]["read_roots"] | by_op[spec["comparison"]]["read_roots"]
        for ref in spec["nominations"]:
            setup=questions.get(ref,{}).get("preparation")
            if not setup:continue
            source=by_op.get(setup["operation"])
            if not source:continue
            cited={context["references"][r]["ast_id"] for r in setup["source_refs"]}
            matched=[root for node,root,*_ in source["writes"] if root in dependencies and
                     any(n.get("id") in cited for n in walk(lookup.nodes[node]))]
            if matched:
                result.append({**spec,"structural":False,"nominations":[ref],"preparation":{
                    "operation":source["op"]["function"],"actor":setup["actor"],"bound_roots":sorted(set(matched))}})
    return result

