from .m20_solver import solve as bounded_solve
"""Shared source facts and narrowly scoped normal-authorization certificates.
No risk label or ground truth is an input. M2 proposals locate facts, not verdicts.
"""
import copy
from .m03_p_paths import key,walk,op,lit
from .m03_p_route import selectors,keys
from .m03_p_assets import negative,add,holder_path
from .m05_state_relations import changes
from .m05_asset_obligations import consent_model
from .m05_mechanism_core import MechanismEncoder
from .m04_logic import Unsupported
from .m22_assets import holder as holder_path, matches as asset_matches, identity as asset_identity

def bind_resource(relation,context,state):
    from .m05_relation_model_scope import source_term
    operation=next(o for o in context["operations"] if o["id"]==relation["op_ref"])
    lookup=state["lookups"][operation["target"]];fn=operation["function"]
    ref=relation.get("resource_ref")
    if not ref:return None,{"status":"no_resource_reference"}
    value=source_term(lookup.nodes[context["references"][ref]["ast_id"]],lookup,fn)
    roots={x["root"] for x in selectors(value)}
    if len(roots)==1:
        return value,{"status":"direct_source_storage","roots":sorted(roots)}
    if not value or value.get("kind") not in ("parameter","actual_sender"):
        return None,{"status":"resource_not_source_storage_or_subject"}
    candidates={}
    # A subject parameter can locate storage only through cited source conditions,
    # not by matching a variable name or guessing the first write.
    for r in relation.get("condition_refs",[])+relation.get("source_refs",[]):
        term=source_term(lookup.nodes[context["references"][r]["ast_id"]],lookup,fn)
        for sel in selectors(term):
            if any(key(n)==key(value) for k in keys(sel) for n in walk(k)):
                candidates[sel["root"]]=sel
    if len(candidates)!=1:return None,{"status":"subject_resource_ambiguous" if candidates else "subject_without_cited_storage","candidate_roots":sorted(candidates)}
    selected=next(iter(candidates.values()))
    return selected,{"status":"source_derived_subject_storage_binding","root":selected["root"],"subject":value,
                     "not_a_format_repair":True}

def implies(lookup,path,predicate):
    import z3
    try:return _typed_implies(lookup,path,predicate)
    except z3.Z3Exception as error:
        raise Unsupported('applicability_type_or_encoding_error:'+str(error)) from error


def _typed_implies(lookup,path,predicate):
    enc=MechanismEncoder(lookup);z=enc.z
    for v in path.get("evaluated_terms",[]):enc.expr(v)
    guards=[enc.expr(v) for v in path["guards"]];wanted=enc.expr(predicate)
    if not z.is_bool(wanted):
        raise Unsupported('applicability_reference_is_not_boolean')
    if not all(z.is_bool(g) for g in guards):
        raise Unsupported('source_path_guard_is_not_boolean')
    s=z.Solver();s.set(timeout=3000);s.add(*enc.constraints,*guards)
    if bounded_solve(s)!=z.sat or enc.abstract_hash_used:return False
    s.add(z.Not(wanted))
    return bounded_solve(s)==z.unsat

def shared_facts(state):
    from .m08_financial import models
    results={};limits=[]
    for tid,lookup in state["lookups"].items():
        program={f:p for (t,f),p in state["paths"].items() if t==tid}
        try:assets=models(lookup,program)
        except Unsupported as ex:
            assets=[];limits.append({"target":tid,"phase":"shared_asset_model","reason":str(ex)})
        normals=[];issuers=[];nonissuance=[]
        for fn,paths in program.items():
            for pi,path in enumerate(paths):
                if path["flow"] not in ("normal","returned"):continue
                if path["issues"] or path.get("evaluation_gaps"):
                    nonissuance.extend({"function":fn,"root":a["balance_root"],"reason":"path_not_fully_classified"} for a in assets)
                    continue
                for asset in assets:
                    try:
                        root=asset["balance_root"]
                        updates=[d for d in changes(path,lookup) if asset_matches(d["write"]["path"],asset)]
                        total={}
                        for d in updates:total=add(total,d["delta"])
                        from .m08_financial import source_signed_changes
                        signed=source_signed_changes(lookup,path,updates) if updates else []
                        if signed and any(d["source_sign"]=="positive" for d in signed) and all(d["source_sign"] in ("positive","zero") for d in signed):
                            issuers.append({"function":fn,"path_index":pi,"root":root,"instance":asset["balance_effect"]["path"].get("instance")})
                        elif updates:nonissuance.append({"function":fn,"root":root,"reason":"nonissuance_asset_effect"})
                        # This certificate covers conserved ordinary transfers. Other
                        # accounting must use its own specific source certificate.
                        if total!={} or len(updates)<2:continue
                        debits=[d for d in updates if d["delta"] and all(x<0 for x in d["delta"].values())]
                        credits=[d for d in updates if d["delta"] and all(x>0 for x in d["delta"].values())]
                        if len(debits)!=1 or len(debits)+len(credits)!=len(updates):continue
                        debit=debits[0];sel=debit["write"]["path"]
                        if not holder_path(sel,lookup):continue
                        holder=keys(sel)[0];amount=negative(debit["delta"])
                        recipient=keys(credits[0]["write"]["path"])[0] if len(credits)==1 and holder_path(credits[0]["write"]["path"],lookup) else None
                        consent,cert=consent_model(path,holder,amount,lookup,program,root,asset.get("supply_root"),recipient=recipient,sufficient_only=True)
                        if not implies(lookup,path,consent):continue
                        normals.append({"function":fn,"path_index":pi,"root":root,"instance":sel.get("instance"),
                            "kind":"source_verified_holder_or_delegate_conserved_transfer","holder":holder,"asset_identity":asset_identity(sel),
                            "total_debit":amount,"consent":consent,"consent_sources":cert,
                            "effect_sources":[d["write"]["source"] for d in updates],"relation_ids":[]})
                    except Unsupported as ex:
                        nonissuance.append({"function":fn,"root":asset["balance_root"],"reason":str(ex)})
                        limits.append({"target":tid,"function":fn,"phase":"normal_asset_facts","reason":str(ex)})
        results[tid]={"assets":assets,"normal_transfers":normals,"issuance_paths":issuers,"nonissuance_paths":nonissuance}
    return results,limits

def annotate_relations(relations,context,state,facts,consumption):
    records={r["relation_id"]:r for r in consumption}
    for r in relations["relations"]:
        record=records[r["id"]]
        if r["relation_kind"] not in ("delegates_to","checks_permission","holder_of","controlled_by"):continue
        operation=next(o for o in context["operations"] if o["id"]==r["op_ref"])
        value,binding=bind_resource(r,context,state);record["resource_binding"]=binding
        roots={s["root"] for s in selectors(value)}
        paths=state["paths"].get((operation["target"],operation["function"]),[])
        # The relation may cite an allowance resource rather than the asset.
        for normal in facts[operation["target"]]["normal_transfers"]:
            if normal["function"]!=operation["function"]:continue
            certificate_roots={s["root"] for s in selectors(normal["consent_sources"])}|{normal["root"]}
            if roots & certificate_roots:
                normal["relation_ids"].append(r["id"])
                record.setdefault("normal_fact_uses",[]).append({"function":normal["function"],"path_index":normal["path_index"],"kind":normal["kind"]})
                record["status"]="source_verified_normal_relationship"
    return facts

def alternative(query,facts):
    basis=query.get("policy_basis",{}).get("basis")
    if query.get("rule") not in ("AC-01","AC-02","AC-03") or basis not in ("same_resource_guarded_operation","source_checked_M2_relation"):return None
    selector=query.get("effect",{}).get("selector",{})
    for fact in facts.get(query["target"],{}).get("normal_transfers",[]):
        if fact["function"]!=query["function"] or fact["path_index"]!=query.get("path_index"):continue
        if fact["root"]!=selector.get("root") or key(fact["instance"])!=key(selector.get("instance")):continue
        # Holder consent does not erase a genuinely applicable transfer policy.
        # Displace only a permission projected from asset issuance, never from
        # a guarded counterpart transfer or from an unspecified source condition.
        origin=query.get("policy_basis",{}).get("origin_function")
        origin_rows=[r for r in facts[query["target"]]["issuance_paths"] if r["function"]==origin and r["root"]==fact["root"] and key(r["instance"])==key(fact["instance"])]
        normal_origin=any(r["function"]==origin and r["root"]==fact["root"] for r in facts[query["target"]]["nonissuance_paths"])
        if not origin_rows or normal_origin:continue
        return {"decision":"normal_authorization_displaces_peer_only_policy","reason":"holder_or_full_amount_delegate_has_source_authority_for_this_effect",
                "source_certificate":copy.deepcopy(fact),"original_policy":copy.deepcopy(query["required_policy_candidate"]),"issuance_origin":copy.deepcopy(origin_rows)}
    return None
