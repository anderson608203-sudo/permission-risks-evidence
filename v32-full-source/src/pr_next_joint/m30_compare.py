"""Source-anchored proposal and concrete-witness consumer shared by AC and FCR."""
from collections import defaultdict
from .core import digest
from .m30_evm import World, Unavailable
from .m30_graph import plans, getters
from .m30_witness import RUNNERS as PRIOR_RUNNERS
from .m31_witness import RUNNERS as RIGHTS_RUNNERS
RUNNERS={**PRIOR_RUNNERS,**RIGHTS_RUNNERS}

RULE={"authority_race":"AC-02","live_redemption_close":"AC-01","qualified_freeze":"FCR-FREEZE",
      "privileged_allowance_burn":"FCR-DESTROY","acquire_then_use":"AC-02","early_termination":"AC-01","repeat_credit":"AC-01",
      "restrict_account":"FCR-FREEZE","holder_loss":"FCR-DESTROY"}


def contexts(graph, operations):
    groups=defaultdict(list)
    targets={o["id"]:o["target"] for o in operations}
    for task in graph["tasks"]:
        for ref,kind,roots in task["effect_sites"]:
            if kind=="contract_destruction":
                groups[targets[task["op_ref"]],kind].append([task["op_ref"],ref])
    # A compact reverse index, deliberately without quadratic lists of entry pairs.
    graph["terminal_routes"]=[{"target":t,"effect":effect,"routes":routes} for (t,effect),routes in groups.items() if len({r[0] for r in routes})>1]
    graph["schema"]="permission-equity-operation-dependencies-v31"


def run(context,state,answer):
    checks,audit=[],[]
    missing=set(q["id"] for q in answer.get("behavior_questions",[]))
    unbound_preparations={q["id"] for q in answer.get("behavior_questions",[]) if q.get("preparation")}
    by_target=defaultdict(list)
    for o in context["operations"]:
        by_target[o["target"]].append(o)
    for tid,operations in by_target.items():
        lookup=state["lookups"][tid]
        search=plans(context,lookup,operations,answer)
        if not search:continue
        votes=defaultdict(int)
        world=None
        startup_error=None
        # New proposals cannot displace a deterministic plan from its allowance.
        for spec in sorted(search,key=lambda c:(not c["structural"], c["kind"], c["fn"],c["peer"], c["site"],c["root"] or -1)):
            hints=spec["nominations"]
            missing.difference_update(hints)
            row={k:spec[k] for k in ("kind","operation","comparison","site","root","structural","nominations","fn","peer","target")}
            if spec.get("preparation"):
                row["preparation"]=spec["preparation"]
                unbound_preparations.difference_update(hints)
            audit.append(row)
            key=(spec["kind"],spec["structural"])
            if votes[key]>=6:
                row.update(status="limited",reason="six_source_comparisons_per_kind_and_origin_per_target")
                continue
            votes[key]+=1
            try:
                if startup_error:raise Unavailable(startup_error)
                if world is None:
                    try:
                        world=World(lookup.contract)
                    except (ImportError,Unavailable) as e:
                        startup_error=str(e);raise Unavailable(startup_error) from e
                world.restore(world.origin)
                if spec["kind"]=="early_termination":
                    from .facts import walk
                    values={32,100,1024}
                    for aid in spec["peer_guards"]:
                        for n in walk(lookup.nodes[aid]):
                            raw=n.get("value")
                            if n.get("nodeType")=="Literal" and isinstance(raw,str) and raw.isdigit() and len(raw)<20:
                                v=int(raw)
                                if 0<v<=10**18:values.update((v,v+1))
                    spec["threshold_values"]=sorted(values)[:12]
                    model=state.get("_v20_shared",{}).get(tid,{}).get("assets",[])
                    obs=getters(lookup,[{"op":o} for o in operations])
                    redeem=defaultdict(list,{g:list(entries) for g,entries in spec["possible_payouts"].items()})
                    for asset in model:
                        g=obs.get(asset.get("balance_root"))
                        if g and asset.get("redemption_function"):
                            redeem[g].append(asset["redemption_function"])
                    spec["redemption_entries"]={g:sorted(set(entries)) for g,entries in redeem.items()}
                if spec["kind"] in ("holder_loss","privileged_allowance_burn"):
                    obs=getters(lookup,[{"op":o} for o in operations])
                    spec["source_supply_getters"]=[obs[m["supply_root"]] for m in state.get("_v30_assets",{}).get(tid,[])
                        if m.get("supply_root") in obs and obs.get(m.get("balance_root"))==spec["asset_getter"]]
                deployment=world.origin
                setup=spec.get("preparation")
                try:
                    if setup:
                        actor=world.user if setup["actor"]=="subject" else world.other
                        receipt=world.call(setup["operation"],actor,address=actor)
                        row["preparation_receipt"]=receipt
                        if (not receipt["ok"] or not receipt["changed_slots"] or receipt["nested_calls"] or receipt["beneficiaries"]
                                or not world.state.get_code(world.address)):
                            raise Unavailable("nominated_initial_state_not_reached_by_bounded_public_operation")
                        world.origin=world.snapshot()
                    proof=RUNNERS[spec["kind"]](world,spec)
                    if setup:proof={**proof,"preparation":setup,"preparation_receipt":receipt}
                finally:
                    world.origin=deployment
                row.update(proof)
                row["environment"]=world.proof()
            except Unavailable as e:
                row.update(status="limited",reason=str(e))
            if row["status"]!="witness":continue
            rule=RULE[spec["kind"]]
            policy={"basis":row["reason"],"kind":spec["kind"],"comparison":spec["peer"],
                    "source_declaration":spec["root"],"environment":row["environment"],"witness_sha256":digest(proof)}
            effect={"kind":"differential_behavior","source":lookup.anchor(lookup.nodes[spec["site"]])}
            cause={"kind":row["reason"],"declaration":spec["root"]}
            formal={"status":"supported","reason":"original_bytecode_transaction_witness","engine":"py-evm",
                    "solver_called":False,"source_and_execution_required":True,"witness":proof,
                    "scope":"one concretely reached state on recorded compiler fork and constructor arguments"}
            q={"target":tid,"function":spec["fn"],"source":effect["source"],"effect":effect,
               "rule":rule,"category":"AC" if rule.startswith("AC") else rule,"analysis_direction":rule,
               "risk_condition":cause,"policy_basis":policy,"formal":formal,"status":"supported","reportable":True,
               "id":"question_"+digest([tid,spec["fn"],spec["peer"],effect,rule,cause])}
            checks.append(q);row["origin_query_id"]=q["id"]
    for q in answer.get("behavior_questions",[]):
        if q["id"] in missing:
            audit.append({"status":"limited","reason":"comparison_or_independent_effect_not_bound_by_program",
                          "nominations":[q["id"]],"kind":q["kind"],"operation":q["operation"],"comparison":q["comparison"]})
        elif q["id"] in unbound_preparations:
            audit.append({"status":"limited","reason":"proposed_setup_is_not_a_bound_write_of_state_used_by_the_compared_entries",
                          "nominations":[q["id"]],"kind":q["kind"],"operation":q["operation"],"comparison":q["comparison"]})
    return checks,audit

