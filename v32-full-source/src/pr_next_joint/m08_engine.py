"""M3/M4 finite program checks and explicit classification after mandatory M2."""
import copy,time
from .core import digest,require
from .m03_p_paths import op,lit,key,walk
from .m03_p_route import selectors,keys,value_type,effective_permission,relocate
from .m04_joint_formal import check
from .m04_logic import Unsupported
from .m08_financial import CATEGORIES

def semantic_candidates(context,relations,state,scopes=None):
    """Turn located M2 relationships into policy queries only with source checks."""
    from .m15_relations import compile_scopes,scoped_resources,policy_allowed,directed_stage_exclusion
    scopes=compile_scopes(context,relations,state) if scopes is None else scopes
    result=[];consumption=[]
    ops={x["id"]:x for x in context["operations"]};refs=context["references"]
    for relation in relations["relations"]:
        record={"relation_id":relation["id"],"queries":[],"status":"not_applicable_to_program_policy"}
        consumption.append(record)
        if relation["relation_kind"] not in ("controlled_by","checks_permission","holder_of","delegates_to"):continue
        scoped=scopes[relation["id"]]
        operation=ops[relation["op_ref"]];tid=operation["target"];fn=operation["function"]
        lookup=state["lookups"][tid];resource_ref=relation.get("resource_ref")
        if not resource_ref:resource_ref=next((v["resource_ref"] for v in scoped["resources"] if v["function"]==fn),None)
        if not resource_ref:record["status"]="no_resource_reference";continue
        from .m05_relation_model_scope import source_term
        from .m09_shared_policy import bind_resource
        resource,binding=bind_resource({**relation,"resource_ref":resource_ref},context,state)
        record["resource_binding"]=binding
        resource_roots={s["root"] for s in selectors(resource)}|{v["selector"]["root"] for v in scoped["resources"] if v["function"]==fn}
        if not resource_roots:record["status"]="resource_not_source_storage";continue
        policies=[]
        related=list(dict.fromkeys([ops[x]["function"] for x in relation["related_op_refs"]]+[ops[link[k]]["function"] for link in relation.get("operation_links",[]) if relation["op_ref"] in (link["from_op_ref"],link["to_op_ref"]) for k in ("from_op_ref","to_op_ref") if link[k]!=relation["op_ref"]]))
        for peer in related:
            for source_pi,path in enumerate(state["paths"].get((tid,peer),[])):
                for w in path["writes"]:
                    if w["path"]["root"] in resource_roots:
                        policies += [(a,w,peer,source_pi) for a in effective_permission(path["guards"],lookup)]
        for ref in relation["condition_refs"]:
            expr=source_term(lookup.nodes[refs[ref]["ast_id"]],lookup,fn)
            # A located predicate supplies a hypothesis, not a classification.
            if expr is not None and selectors(expr):
                matched=False
                for (target,peer),paths in state["paths"].items():
                    if target!=tid:continue
                    for source_pi,p in enumerate(paths):
                        if not any(key(expr)==key(a) for a in effective_permission(p['guards'],lookup)):continue
                        for w in p['writes']:
                            if w['path']['root'] in resource_roots:
                                policies.append((expr,w,peer,source_pi));matched=True
                if not matched:record.setdefault('normal_source_exclusions',[]).append('cited_condition_not_observed_permission_on_matching_resource')
        for located in scoped["conditions"]:
            peer=located["function"]
            for pi in located["path_indices"]:
                path=state["paths"][(tid,peer)][pi]
                if not any(key(located["term"])==key(g) for g in effective_permission(path["guards"],lookup)):continue
                for w in path["writes"]:
                    if w["path"]["root"] in resource_roots:policies.append((located["term"],w,peer,pi))
        # Exact duplicate locations have the same origin; keep other origins
        # distinct so normal applicability cannot leak across policy sources.
        policies=list({key([required,origin,peer,source_pi]):(required,origin,peer,source_pi) for required,origin,peer,source_pi in policies}.values())
        for pi,path in enumerate(state["paths"].get((tid,fn),[])):
            if path["flow"] not in ("normal","returned"):continue
            if any(x['field'] in ('resource','condition','actor') and x.get('function')==fn and pi in x.get('path_indices',[]) for x in scoped['rejections']):
                scoped['events'].append({'kind':'local_binding_rejection','function':fn,'path_index':pi});continue
            for w in path["writes"]:
                if w["path"]["root"] not in resource_roots:continue
                if not scoped_resources(scoped,fn,w["path"],pi=pi):
                    scoped["events"].append({"kind":"resource_scope_restriction","function":fn,"effect_source":w["source"]});continue
                for required,origin_write,origin_function,origin_pi in policies:
                    origin=origin_write["path"]
                    stage_reason=directed_stage_exclusion(scoped,fn,pi,path,w,required,origin_function,lookup)
                    if stage_reason:
                        scoped["events"].append({"kind":"policy_scope_restriction","function":fn,"origin_function":origin_function,"reason":stage_reason,"effect_source":w["source"]});continue
                    from .m10_applicability import route_for
                    if route_for(lookup,origin_function or fn,required,origin):
                        record.setdefault('normal_source_exclusions',[]).append('business_branch_not_universal_permission');continue
                    try:
                        from .m03_p_resource_relations import project_policy
                        source_path=state["paths"][(tid,origin_function)][origin_pi]
                        peer={"function":origin_function,"policy":required,"write":origin_write,
                              "guards":source_path["guards"],"path":source_path,"path_index":origin_pi}
                        from .m21_policy import source_projection_limit
                        projection_limit=source_projection_limit(peer,w,path,fn,lookup)
                        if projection_limit:
                            record.setdefault("projection_exclusions",[]).append(projection_limit)
                            continue
                        expected,projection_evidence=project_policy(peer,w,fn)
                        from .m04_policy_relations import initialized_policy
                        expected,initialization=initialized_policy(expected,w,path,lookup)
                        if initialization:record.setdefault("projection_initializations",[]).append(initialization)
                        if expected is None:continue
                        allowed,reason=policy_allowed(scoped,fn,pi,path,w,expected,origin_function,lookup,relation)
                        if not allowed:
                            scoped["events"].append({"kind":"policy_scope_restriction","function":fn,"origin_function":origin_function,"reason":reason,"effect_source":w["source"]});continue
                        available={n["id"] for n in walk(path) if n.get("kind")=="parameter"}
                        if not {n["id"] for n in walk(expected) if n.get("kind")=="parameter"}<=available:continue
                        row={"rule":"AC-01","analysis_direction":None,"target":tid,"function":fn,"path_index":pi,
                            "program_id":context["identity"]["program_id"],"build_id":context["identity"]["build_id"],
                            "conditions":copy.deepcopy(path["guards"]),"issues":copy.deepcopy(path["issues"]),
                            "effect":{"object":lookup.nodes[w["path"]["root"]]["name"],"selector":w["path"],"value":w["value"],
                            "operator":w["operator"],"source":w["source"]},"required_policy_candidate":expected,
                            "policy_basis":{"basis":"source_checked_M2_relation","relation_id":relation["id"],"origin_function":origin_function,"origin_path_index":origin_pi,"source_projection":projection_evidence},
                            "source_evaluation_terms":path.get("evaluated_terms",[])}
                        row["id"]="q_"+digest(row);result.append(row);record["queries"].append(row["id"])
                    except ValueError as ex:record.setdefault("limitations",[]).append(str(ex))
        if record["queries"]:record["status"]="consumed_in_program_risk_queries"
    return result,consumption

def program_obligation(tid,fn,operation,context):
    seed={"target":tid,"function":fn,"scope":"AC-05","identity":context["identity"],"source_ast_ids":operation["source_ast_ids"]}
    return {"id":"program_"+digest(seed),"proposal_sha256":digest(seed),"identity":context["identity"],"target":tid,
        "function":fn,"rule":"AC-05","source_ast_ids":operation["source_ast_ids"],"source_binding_status":"source_anchors_bound",
        "related_operations":[],"original_proposal":{"id":"program_generated","unresolved":[],"mechanism":{}},
        "generated_by_program":True}

def _analyze_core(context,light,relations,progress=None,*,compose_graph=True):
    from .m04_joint_context import build
    started=time.perf_counter()
    # Deep facts are optional bounded extensions; the complete light inventory already exists.
    old,state=build(light["bundle"],light["native"],context.get("normal_project_description"),context["sources"],
        selected_targets=light["selected_targets"],analysis_scope=context["analysis_scope"])
    source_extraction_seconds=time.perf_counter()-started
    require(set(state["lookups"])==set(light["selected_targets"]),"V9_CORE_TARGET_ANALYSIS_MISSING")
    from .m22_record_roles import prepare as prepare_record_roles
    prepare_record_roles(state)
    from .m20_graph import EffectIndex
    state['_v20_old_context']=old
    effect_index=EffectIndex(state)
    from .m29_worklist import OperationQueue
    queue=OperationQueue(state,effect_index)
    queue.bind(context,relations)
    state['_v20_effect_index']=effect_index
    queries=[];checks=[];limitations=[];scan=[];shared={};semantic_uses=[]
    failures=state["analysis"].get("failures",[])
    unexpected=[f for f in failures if not str(f.get("reason","")).startswith(("ValueError:source_","ValueError:P_","Unsupported:"))]
    require(not unexpected,"V9_CORE_IMPLEMENTATION_FAILURE:"+str(unexpected))
    limits=failures+state["analysis"].get("uncovered",[])
    limitations.extend({"phase":"bounded_source_analysis","detail":x} for x in limits)
    # Reuse extracted paths instead of repeating every function for every consumer.
    for tid,lookup in state["lookups"].items():
        program={fn:paths for (target,fn),paths in state["paths"].items() if target==tid}
        state.setdefault("_source_mechanism_raw_models",{})[tid]=(lookup,program,[])
        state.setdefault("_source_mechanism_models",{})[tid]=(lookup,program,[])
    for operation in context["operations"]:
        tid=operation["target"];fn=operation["function"]
        require(tid in state["lookups"],"V9_SELECTED_TARGET_NOT_SCANNED")
        fact_target=next(t for t in old["targets"] if t["id"]==tid)
        fact_function=next(f for f in fact_target["functions"] if f["function"]==fn)
        effect_scope=getattr(state["lookups"][tid],"effect_scope_inventory",{}).get(fn,{})
        scan.append({"operation":operation["id"],"target":tid,"function":fn,"light_scan_completed":True,
            "bounded_paths":len(state["paths"].get((tid,fn),[])),"effect_scope":effect_scope,
            "limitation":fact_function["extraction_errors"] if fact_function["extraction_status"]=="failed" else None})
    if progress:progress("M3","source_candidates_completed",operations=len(scan))
    if progress:progress("M4","program_and_model_checks_started")
    from .m15_relations import compile_scopes,verify_links,financial_link_certificates,usage_ledger
    scopes=compile_scopes(context,relations,state)
    effect_index.bind_semantics(context,relations,scopes)
    if context["analysis_scope"]=="AC":
        for tid,lookup in state["lookups"].items():
            for b in state["bindings"].values():
                if b.get("target")!=tid or "row" not in b:continue
                row=copy.deepcopy(b["row"])
                if row["rule"] not in ("AC-01","AC-02","AC-03","AC-04","AC-05"):continue
                row["target"]=tid;queries.append(row)
        from .m09_shared_policy import shared_facts,annotate_relations,alternative as normal_alternative
        shared,normal_limits=shared_facts(state);limitations.extend(normal_limits)
        from .m11_policy import facts as effect_facts,applicability,obligations
        limitations.extend(effect_facts(state,shared))
        from .m12_policy import facts as transition_facts,alternative as transition_alternative
        limitations.extend(transition_facts(state,shared))
        from .m19_authorization_scope import facts as authorization_use_facts
        authorization_use_facts(state,shared)
        for scoped in scopes.values():verify_links(scoped,context,state,shared)
        proposed,consumption=semantic_candidates(context,relations,state,scopes);queries.extend(proposed)
        annotate_relations(relations,context,state,shared,consumption)
        duties,duty_limits=obligations(context,state,shared,relations,consumption);queries.extend(duties);limitations.extend(duty_limits)
        from .m08_authorization import temporal_queries,sensitive_queries,dangerous_entry_queries
        queries.extend(temporal_queries(context,state));queries.extend(sensitive_queries(context,state));queries.extend(dangerous_entry_queries(context,state))
        from .m18_code_control import queries as code_queries
        code_rows,code_limits=code_queries(context,state);queries.extend(code_rows);limitations.extend(code_limits)
        from .m18_initialization_scope import observations as initialization_observations
        limitations.extend(initialization_observations(state))
        from .m20_policy import authority_duties,semantic_duties
        state['_v20_shared']=shared
        fresh,fresh_limits=authority_duties(context,state,effect_index)
        semantic,semantic_uses=semantic_duties(context,relations,state,effect_index)
        queries.extend(fresh);queries.extend(semantic);limitations.extend(fresh_limits)
        from .m23_initialization import duties as initial_authority_duties
        init_rows,init_limits=initial_authority_duties(context,state,effect_index)
        queries.extend(init_rows);limitations.extend(init_limits)
        from .m23_issuance import duties as issuance_duties
        issue_rows,issue_limits=issuance_duties(context,state,shared,effect_index)
        queries.extend(issue_rows);limitations.extend(issue_limits)
        from .m21_credential_grants import duties as credential_grants
        grant_rows,grant_limits=credential_grants(context,state,shared,effect_index)
        queries.extend(grant_rows);limitations.extend(grant_limits)
        from .m21_destruction import duties as destruction_duties
        destruction_rows,destruction_limits=destruction_duties(context,state,shared,effect_index)
        queries.extend(destruction_rows);limitations.extend(destruction_limits)
        from .m24_controls import duties as control_duties
        control_rows,control_limits=control_duties(context,state,shared,effect_index)
        queries.extend(control_rows);limitations.extend(control_limits)
        from .m25_phase import duties as phase_duties
        phase_rows,phase_limits=phase_duties(context,state,effect_index)
        queries.extend(phase_rows);limitations.extend(phase_limits)
        from .m24_lifecycle import duties as lifecycle_duties
        lifecycle_rows,lifecycle_limits=lifecycle_duties(context,state,shared,effect_index)
        queries.extend(lifecycle_rows);limitations.extend(lifecycle_limits)
        from .m27_effect_checks import amount_duties,management_grants
        from .m28_capabilities import analyze as capability_queries
        capability_rows,capability_audit=capability_queries(context,state,effect_index,shared,relations,queue) if compose_graph else ([],[])
        from .m29_delegated import duties as delegated_duties
        if compose_graph:capability_rows.extend(delegated_duties(context,state,shared,relations,queue))
        from .m29_claims import duties as claim_duties
        if compose_graph:capability_rows.extend(claim_duties(context,state,queue))
        state['_capability_audit']=capability_audit
        queries.extend(capability_rows)
        uses_by_id={u['relation_id']:u for u in consumption}
        for row in capability_rows:
            for rid in row['policy_basis'].get('relation_ids',[]):
                uses_by_id[rid]['queries'].append(row['id'])
        queries.extend(management_grants(context,state,effect_index))
        amount_rows,amount_limits=amount_duties(context,state,effect_index,relations,shared)
        queries.extend(amount_rows);limitations.extend(amount_limits)
        for row in amount_rows:
            related=row['policy_basis'].get('semantic_asset_relation')
            if related:
                for use in consumption:
                    if use['relation_id']==related:use.setdefault('queries',[]).append(row['id'])
        for use in semantic_uses:
            for record in consumption:
                if record['relation_id']==use['relation_id']:
                    record.setdefault('v20_semantic_uses',[]).append(use)
                    record.setdefault('queries',[]).extend(use.get('query_ids',[]))
        unique={}
        for row in queries:
            fingerprint=digest([row["target"],row["function"],row.get("effect"),row.get("conditions"),row.get("required_policy_candidate"),row.get("policy_basis")])
            unique.setdefault(fingerprint,row)
        formal_cache={}
        for row in unique.values():
            lookup=state["lookups"][row["target"]];q=copy.deepcopy(row)
            from .m11_coverage import scope_query
            q=scope_query(q,state)
            q.setdefault("id","q_"+digest(q));q["analysis_direction"]=q.get("analysis_direction",q["rule"])
            from .m04_joint_controls import assess_policy
            from .m18_policy_scope import alternative as precise_alternative
            from .m19_authorization_scope import alternative as authorization_use_alternative
            from .m21_policy import gate
            q,alternative=gate(q,state,shared,effect_index)
            q.setdefault("policy_applicability",{"basis":q.get("policy_basis",{}).get("basis"),"decision":"excluded_by_local_normal_fact" if alternative else "retained_source_hypothesis","sat_does_not_prove_policy":True})
            # Reuse the existing alternate-authority boundary for later M2
            # and native-effect consumers as well as the original P consumer.
            if not alternative and q.get('policy_basis',{}).get('basis') in ('same_source_native_reserve_guard','source_checked_M2_relation'):
                from .m04_policy_relations import alternate_authority_scope
                observed=alternate_authority_scope({'required':q['required_policy_candidate']},q['conditions'],lookup)
                if observed:q.setdefault('issues',[]).append(observed)
            t=time.perf_counter()
            from .m12_evidence import model_key
            cache_key=model_key(q)
            if alternative:
                unestablished=alternative.get("assessment_kind")=="policy_not_established"
                formal={"status":"inconclusive" if unestablished else "not_matched","solver_called":False,
                    "reason":"authorization_policy_not_established" if unestablished else "source_verified_normal_authorization"}
            elif cache_key is not None and cache_key in formal_cache:
                prior,formal=copy.deepcopy(formal_cache[cache_key])
                formal.update(model_result_reused_from=prior,solver_called=False,
                    timing_seconds={'construct_and_solve':0.0,'solver_checks':0.0,'solver_check_calls_attempted':0})
            else:
                formal=check(lookup,q)
                if cache_key is not None:formal_cache[cache_key]=(q['id'],copy.deepcopy(formal))
            formal["wall_seconds"]=time.perf_counter()-t
            require(not formal.get("implementation_error"),"V9_CORE_FORMAL_IMPLEMENTATION_FAILURE:"+formal.get("reason",""))
            # Formal unsatisfiability overrides a provisional source hypothesis.
            support=formal["status"]=="supported"
            # P can independently certify a simple, fully sourced Boolean case.
            from .m21_policy import identical_program_obligation
            if formal["status"]=="inconclusive" and row.get("status")=="supported" and not alternative and identical_program_obligation(row,q):
                exprs=row.get("conditions",[])+[row.get("required_policy_candidate",{})]
                simple=all(n.get("kind") in ("literal","actual_sender","storage","parameter","op") and
                    (n.get("kind")!="op" or n.get("op") in ("==","!=","!","and","or","&&","||"))
                    for value in exprs for n in walk(value) if "kind" in n)
                support=simple
            if alternative:
                support=False
                formal["source_policy_rejection" if alternative.get("assessment_kind")=="policy_not_established" else "source_normal_alternative"]=alternative
                q["candidate_reason"]=q.get("reason");q["reason"]="authorization_policy_not_established" if alternative.get("assessment_kind")=="policy_not_established" else "excluded_by_source_verified_normal_authorization"
                for record in consumption:
                    if record["relation_id"] in alternative.get("source_certificate",{}).get("relation_ids",[]):
                        record.setdefault("excluded_origin_queries",[]).append(q["id"])
            sequence_checks=[]
            if not alternative and not q.get('issues') and formal.get('status')!='refuted_in_scope':
                from .m20_sequence import candidates as sequence_candidates
                count=state.setdefault('_v20_sequence_count',0)
                variants=sequence_candidates(q,state,context,relations)
                for sq in variants:
                    if state['_v20_sequence_count']>=24:
                        limitations.append({'phase':'finite_state_composition','reason':'24_actual_sequence_checks_per_sample_bound','function':q['function']})
                        break
                    state['_v20_sequence_count']+=1
                    sf=check(lookup,sq)
                    sequence_checks.append({'id':sq['id'],'model':sq['sequence_model'],
                        'conditions':sq['conditions'],'required':sq['required_policy_candidate'],
                        'effect':sq['effect'],'formal':sf})
                    if sf['status']=='supported' and not sf.get('implementation_error'):
                        support=True
                        if formal['status']!='supported':
                            formal={'status':'supported','engine':'z3_finite_source_sequence','finite_sequence_support':sq['id'],
                                'single_step_observation':formal,'solver_called':sf.get('solver_called',False),
                                'scope':sf['scope'],'formula_sha256':sf.get('formula_sha256'),'smt2':sf.get('smt2'),
                                'wall_seconds':formal.get('wall_seconds',0)+sf.get('wall_seconds',0)}
                if sequence_checks:q['finite_state_checks']=sequence_checks
            checks.append({**q,"category":"AC","formal":formal,"status":"supported" if support else formal["status"],
                "reportable":support,"classification_source":"program_source_or_model"})
        # Credential consumers receive a program-generated question, never an LLM category.
        from .m05_credential_obligations import check as credential_check
        for operation in context["operations"]:
            tid=operation["target"];fn=operation["function"]
            paths=state["paths"].get((tid,fn),[])
            if not any(n.get("kind")=="credential_recovery" for p in paths for n in walk(p.get("guards",[]))):continue
            ob=program_obligation(tid,fn,operation,context)
            rows,gaps=credential_check(ob,state)
            for row in rows:
                row.update(category="AC",analysis_direction="AC-05",reportable=row["status"]=="supported",
                    classification_source="program_credential_query",source_query_origin="program")
                checks.append(row)
            limitations.extend({"function":fn,"phase":"credential","detail":g} for g in gaps)
    else:
        consumption=[{"relation_id":r["id"],"status":"source_located_for_model_crosscheck"} for r in relations["relations"]]
        from .m08_financial import analyze as financial
        for tid,lookup in state["lookups"].items():
            program={fn:paths for (target,fn),paths in state["paths"].items() if target==tid}
            hints=[]
            from .m05_relation_model_scope import source_term
            operations={o["id"]:o for o in context["operations"]}
            for relation in relations["relations"]:
                operation=operations[relation["op_ref"]]
                if operation["target"]!=tid:continue
                references=list(dict.fromkeys(([relation['resource_ref']] if relation.get('resource_ref') else [])+relation.get('resource_refs',[])))
                bound_roots=set()
                for ref in references:
                    from .m09_shared_policy import bind_resource
                    candidate,binding_item=bind_resource({**relation,'resource_ref':ref},context,state)
                    bound_roots.update(x['root'] for x in selectors(candidate))
                bound_roots.update(x["selector"]["root"] for x in scopes[relation["id"]]["resources"])
                if not bound_roots:continue
                from .m09_shared_policy import bind_resource
                value,binding=bind_resource(relation,context,state)
                for record in consumption:
                    if record['relation_id']==relation['id']:record['resource_binding']=binding
                source_selectors=selectors(value)
                for root in sorted(bound_roots):
                    hints.append({"id":relation["id"],"kind":relation["relation_kind"],"resource_root":root,'resource_roots':sorted(bound_roots),
                        "functions":list(dict.fromkeys([operation["function"]]+[operations[x]["function"] for x in relation["related_op_refs"]]+[v["function"] for v in scopes[relation["id"]]["resources"]]+[operations[v[k]]["function"] for v in relation.get("operation_links",[]) for k in ("from_op_ref","to_op_ref")])),
                        "scoped_relation":scopes[relation["id"]],"operation_ids_by_function":{fn:[o["id"] for o in context["operations"] if o["target"]==tid and o["function"]==fn] for fn in {o["function"] for o in context["operations"] if o["target"]==tid}}})
            def link_verifier(assets):
                verified=[]
                for scoped in scopes.values():
                    if scoped['target']==tid:verified.extend(verify_links(scoped,context,state,{},assets))
                return verified
            from .m27_effect_checks import parameter_checks,semantic_assets
            rows,gaps,assets=financial(lookup,program,hints,link_verifier,semantic_assets(context,relations,state,tid,program),queue,tid)
            state.setdefault('_v30_assets',{})[tid]=assets
            loss_rows,observations=parameter_checks(tid,effect_index,lookup,program,assets)
            from .m29_settlement import compare as compare_settlements
            extra,notes=compare_settlements(tid,lookup,program,queue) if compose_graph else ([],[])
            loss_rows.extend(extra)
            observations.extend(notes)
            rows.extend(loss_rows)
            for observation in observations:
                if 'check' in observation:
                    state.setdefault('_parameter_observations',[]).append({'target':tid,**observation})
                else:gaps.append(observation)
            for row in rows:row["target"]=tid;row["category"]=row["rule"]
            checks.extend(rows);limitations.extend({"target":tid,**g} for g in gaps)
            # Explicitly correlate M2 asset/control proposals to source-derived models.
            for r,c in zip(relations["relations"],consumption):
                operation=next(o for o in context["operations"] if o["id"]==r["op_ref"])
                if operation["target"]!=tid:continue
                ref=r.get("resource_ref")
                from .m09_shared_policy import bind_resource
                term,binding=bind_resource(r,context,state)
                roots={x['root'] for x in selectors(term)}
                root=next(iter(roots)) if len(roots)==1 else None
                c['resource_binding']=binding
                matched=[m["balance_root"] for m in assets if m["balance_root"]==root]
                linked=[q["id"] for q in rows if q["function"]==operation["function"] and
                    any(context["references"][x]["ast_id"] in {n.get("root") for n in walk(q.get("source_model",{}))}
                        for x in r["source_refs"])]
                generated=[m for m in assets if r["id"] in m.get("relation_ids",[m.get("relation_id")])]
                effective=[q["id"] for q in rows if r["id"] in q.get("source_model",{}).get("asset",{}).get("relation_ids",[q.get("source_model",{}).get("asset",{}).get("relation_id")])]
                scopes[r["id"]]["verified_links"]=[x for x in scopes[r["id"]].get("verified_links",[]) if x["kind"]!="same_holder_conversion"]+financial_link_certificates(scopes[r["id"]],context,state,assets)
                c.update(shared_authorization_check_ids=[q["id"] for q in rows if r["id"] in q.get("source_model",{}).get("verified_relation_ids",[])],source_asset_roots=matched,query_ids=linked,generated_models=generated,
                    generated_model_query_ids=effective,
                    consumption_kind="source_checked_model_construction" if generated else "source_model_corroboration" if matched or linked else "no_confirmed_program_use",
                    causal_classification_gain_requires_control=True,
                    equity_certificates=[m["equity_certificate"] for m in assets if r["id"] in m.get("equity_certificate",{}).get("relation_ids",[])],
                    status="source_confirmed_model_relation" if generated or matched or linked else "relationship_not_confirmed_by_program_model")
                if c['shared_authorization_check_ids']:
                    c.update(consumption_kind='source_checked_shared_authorization_consumption',status='source_confirmed_shared_authorization')
                elif c['equity_certificates']:
                    c.update(consumption_kind='source_checked_equity_construction' if any(x.get('construction_origin')=='M2_located_source_combination' for x in c['equity_certificates']) else 'existing_equity_certificate_corroboration',status='source_confirmed_equity_relation')
    if context['analysis_scope']!='AC':
        # These hypotheses currently compile AC local policy duties only. FCR
        # uses source-checked financial relationships instead. Expose that limit
        # rather than silently dropping optional proposals or misusing an AC duty.
        for r in relations['relations']:
            for h in r.get('authorization_hypotheses',[]):
                semantic_uses.append({'relation_id':r['id'],'hypothesis_location':'nested','hypothesis':copy.deepcopy(h),
                    'status':'not_applicable_to_scope','reason':'AC_local_policy_hypothesis_has_no_FCR_consumer',
                    'query_ids':[],'path_checks':[]})
        for h in relations.get('authorization_hypotheses',[]):
            semantic_uses.append({'relation_id':'standalone_hyp_'+digest(h)[:20],'hypothesis_location':'standalone','hypothesis':copy.deepcopy(h),
                'status':'not_applicable_to_scope','reason':'AC_local_policy_hypothesis_has_no_FCR_consumer',
                'query_ids':[],'path_checks':[]})
    from .m30_compare import run as behavioral_comparisons
    behavioral_checks,behavioral_audit=behavioral_comparisons(context,state,relations) if compose_graph else ([],[])
    checks.extend(behavioral_checks)
    from .m09_evidence import finalize,group
    checks=finalize(checks,context["identity"])
    # Rewrite origin links after target/build-scoped identities have been assigned.
    rewritten={}
    for q in checks:
        for origin in q["origin_query_ids"]:rewritten.setdefault((q["target"],origin),[]).append(q["id"])
    for q in checks:
        formal=q.get('formal',{});prior=formal.get('model_result_reused_from')
        if prior is not None:
            formal['model_result_reused_from_query_ids']=rewritten.get((q['target'],prior),[])
            del formal['model_result_reused_from']
    operation_targets={o["id"]:o["target"] for o in context["operations"]}
    for trial in behavioral_audit:
        if 'origin_query_id' in trial:
            trial['query_ids']=rewritten.get((trial['target'],trial['origin_query_id']),[])
    relation_targets={r["id"]:operation_targets[r["op_ref"]] for r in relations["relations"]}
    for record in consumption:
        target=relation_targets[record["relation_id"]]
        for field in ("queries","query_ids","excluded_origin_queries","generated_model_query_ids","shared_authorization_check_ids"):
            if field in record:record[field]=sorted({new for old in record[field] for new in rewritten.get((target,old),[])})
    effect_index.rewrite_query_ids(rewritten)
    for record in semantic_uses:
        target=operation_targets[record['hypothesis']['op_ref']]
        record['query_ids']=sorted({new for old in record.get('query_ids',[]) for new in rewritten.get((target,old),[])})
        for path_use in record.get('path_checks',[]):
            if 'query_id' in path_use:
                old_id=path_use.pop('query_id');path_use['query_ids']=rewritten.get((target,old_id),[])
    findings={};extension_findings={}
    for row in checks:
        if not row.get("reportable"):continue
        source=row.get("source") or row.get("effect",{}).get("source") or row.get("source_model",{}).get("effect",{}).get("source") or {}
        cause=row.get("required_policy_candidate") or row.get("risk_condition") or row.get("source_model",{}).get("kind")
        identity={"target":row["target"],"function":row["function"],"source":source,"cause":cause,"category":row["category"]}
        fid="finding_"+digest(identity)[:24]
        bucket=extension_findings if str(row["category"]).startswith("EXT-") else findings
        f=bucket.setdefault(fid,{"id":fid,**identity,"evidence_query_ids":[],"analysis_directions":[],"evaluation_match_status":"not_evaluated"})
        f["evidence_query_ids"].append(row["id"])
        direction=row.get("analysis_direction",row["rule"])
        if direction is not None and direction not in f["analysis_directions"]:f["analysis_directions"].append(direction)
    operations_by_key={(o['target'],o['function']):o for o in context['operations']}
    for f in list(findings.values())+list(extension_findings.values()):
        f['function_source']=operations_by_key[(f['target'],f['function'])]['source']
        from .m24_locations import root_locations
        f['source_cause_locations']=root_locations(f,checks,state['lookups'][f['target']])
    cause_groups=group(list(findings.values()),checks,context["identity"])
    from .m11_coverage import coverage
    check_coverage=coverage(context,state,checks)
    categories=["AC"] if context["analysis_scope"]=="AC" else list(CATEGORIES)
    labels={k:any(r["category"]==k and r.get("reportable") for r in checks) for k in categories}
    ledger=usage_ledger(scopes,consumption,checks,context["analysis_scope"])
    from .m16_relation_view import build as relation_view
    view=relation_view(context,ledger,checks)
    limitations.extend(state.get('_v20_sequence_limits',[]))
    effect_index.match_queries(checks)
    return {"schema":"joint-finite-classification-v9","status":"joint_complete","analysis_scope":context["analysis_scope"],
        "effective_parameters":__import__(__package__+".effective_parameters",fromlist=["current"]).current(),
        "condition_role_audit":{tid:getattr(lookup,"routing_records",{}) for tid,lookup in state["lookups"].items()},
        "method_revision":"joint-rights-settlement-rq1-v32-20261104",
        "behavioral_comparisons":behavioral_audit,
        "operation_worklist":queue.report(checks),
        "capability_construction":[{**r,"queries":sorted({new for q in r.get("queries",[]) for new in rewritten.get((r["target"],q),[])})} for r in state.get('_capability_audit',[])],
        "authorization_policy_registry":state.get("_policy_source_registry",{}),
        "source_record_role_certificates":state.get("_source_record_roles",{}),
            "source_local_state_certificates":state.get("_v22_state_certificates",{}),
        "source_fixed_storage_facts":{tid:getattr(lookup,"source_fixed_storage_facts",{}) for tid,lookup in state["lookups"].items()},
        "source_identity":context["identity"],"classification":{"labels":labels,"all_requested_labels_classified":True,
        "status":"positive" if any(labels.values()) else "negative","negative_meaning":"not_detected_by_this_finite_method_not_safety_proof"},
        "findings":list(findings.values()),"extension_findings":list(extension_findings.values()),"extension_scope":"primary freeze includes verified account-specific asset delivery and delegated transfer service restrictions; a single failing branch or seller discretion alone is insufficient","suggested_cause_groups":cause_groups,
        "reported_defect_groups":cause_groups,"sensitive_effect_coverage":check_coverage,
        "finding_counts":{"raw_effect_findings":len(findings),"auxiliary_effect_findings":len(extension_findings),"source_defect_groups":len(cause_groups),"groups_are_not_automatically_reference_vulnerabilities":True},"shared_authorization_facts":shared,"checks":checks,"queries":checks,"operation_scan":scan,
        "relations_consumption":consumption,"relation_usage_ledger":ledger,"permission_equity_relation_view":view,
        "permission_equity_dependency_graph":effect_index.export(),"semantic_hypothesis_usage":semantic_uses,
        "financial_parameter_observations":state.get('_parameter_observations',[]),
        "relationship_contract":{"schema":"joint-task-relations-v20","roles_are_proposals":True,"source_validation_required":True,"absent_optional_relations_do_not_block_classification":True},
        "verification_diagnostics":{"limitations":limitations,"completed_scan":True,"normalization_profiles":{tid:getattr(lookup,"normalization_profiles",{}) for tid,lookup in state["lookups"].items()}},
        "llm_required":True,"llm_classification_used":False,"source_analysis_seconds":time.perf_counter()-started,
        "stage_timings":{"source_extraction_seconds":source_extraction_seconds,
            "program_consumers_seconds":time.perf_counter()-started-source_extraction_seconds,
            "risk_query_seconds":sum(r.get("formal",{}).get("wall_seconds",0) for r in checks)},
        "hypothesis_contract":{"basis":"source-bound local authorization or asset-control semantics",
            "sat_meaning":"satisfiable conditional query, not proof that an invented policy is required",
            "global_relation_closure_required":False,"llm_verdict_used":False},
        "diagnosis_counts":{"queries":len(checks),"normal_exclusions":sum(bool(r.get("formal",{}).get("source_normal_alternative")) for r in checks),
            "supported":sum(bool(r.get("reportable")) for r in checks),"supported_includes_auxiliary":True,"primary_supported":sum(bool(r.get("reportable")) and not r.get("category","").startswith("EXT-") for r in checks),"auxiliary_supported":sum(bool(r.get("reportable")) and r.get("category","").startswith("EXT-") for r in checks),"unmatched":sum(not r.get("reportable") for r in checks)},

        "ac_counting_unit":"location_and_root_cause_instance_matching_after_prediction_freeze",
        "not_final_RQ1_result":True}


def analyze(context,light,relations,progress=None,*,compose_graph=True,use_semantic_proposals=True):
    from .m20_solver import budget
    from .m20_ledger import mode
    with budget(120.0) as resource:
        active=relations if use_semantic_proposals else {**relations,'relations':[],'authorization_hypotheses':[],'behavior_questions':[]}
        report=_analyze_core(context,light,active,progress,compose_graph=compose_graph)
        report['analysis_variant']={'cross_operation_capability_and_settlement':compose_graph,
            'consume_M2_proposals':use_semantic_proposals,'formal_verification':'full',
            'whole_formal_ablation_not_identified':True}
        report['solver_resource']=copy.deepcopy(resource)
        report['destroy_definition_profile']=mode()
        if resource['budget_exhausted']:
            report['verification_diagnostics']['limitations'].append({'phase':'formal_resource','reason':'sample_solver_budget_exhausted','unknown_is_not_refutation':True})
        return report
