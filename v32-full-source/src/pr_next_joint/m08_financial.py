from .m20_solver import solve as bounded_solve
"""Program-built finite financial mechanism queries; no model-supplied verdicts."""
import copy,time
from .core import digest
from .m03_p_paths import key,walk,op,lit,conditions_possible
from .m03_p_route import keys,selectors,effective_permission,value_type
from .m03_p_assets import asset_models,negative,add,term,polynomial,holder_path
from .m05_state_relations import changes,compose_read
from .m05_asset_obligations import privilege,consent_model
from .m05_mechanism_core import MechanismEncoder,remap
from .m04_logic import Unsupported
from .m22_assets import holder as field_holder, matches as asset_matches, unique as unique_assets, identity as asset_identity

CATEGORIES=("FCR-MINT","FCR-TRANSFER","FCR-DESTROY","FCR-PAUSE","FCR-FREEZE")

def quantity(form):
    if form is None:raise Unsupported("nonlinear_delta_not_bound")
    terms=[]
    for k,n in form.items():
        import json
        v=lit(1) if k=="#" else json.loads(k)
        terms.append(op("*",lit(n),v) if n!=1 else v)
    import json
    return {"kind":"source_linear_quantity","terms":[{"coefficient":n,"value":lit(1) if k=="#" else json.loads(k)} for k,n in form.items()]}

def quantity_tail(items):
    if len(items)==1:return items[0]
    return op("+",items[0],quantity_tail(items[1:]))

def probe(lookup,conditions,violation,metadata,source,fn,rule):
    started=time.perf_counter()
    e=MechanismEncoder(lookup);z=e.z
    for evaluated in metadata.pop("evaluation_terms",[]):e.expr(evaluated)
    domain=[e.expr(c) for c in conditions];risk=e.expr(violation)
    if not all(z.is_bool(x) for x in domain+[risk]):raise Unsupported("risk_query_boolean_required")
    s=z.Solver();s.set(timeout=3000);s.add(*e.constraints,*domain)
    premise=bounded_solve(s);status="not_matched";answer="not_checked"
    if premise==z.sat:
        s.add(risk);answer=str(bounded_solve(s,upgrade=True))
        if answer=="sat" and not e.abstract_hash_used:status="supported"
        elif answer=="unknown" or e.abstract_hash_used:status="limited"
    elif premise==z.unknown:status="limited"
    formula=s.to_smt2()
    row={"id":"q_"+digest([rule,fn,source,conditions,violation]),"rule":rule,
         "function":fn,"source":source,"conditions":conditions,"risk_condition":violation,
         "status":status,"formal":{"solver_called":True,"premise":str(premise),"query":answer,
         "formula_sha256":digest(formula),"smt2":formula,"status":status,"wall_seconds":time.perf_counter()-started},
         "source_model":metadata,"reportable":status=="supported",
         "limitations":["conditional source mechanism; deployed prestate and complete business intent not proven"]}
    return row

def models(lookup,program):
    cached=getattr(lookup,'_v22_asset_models',None)
    if cached is not None:return copy.deepcopy(cached)
    found=asset_models(lookup,program)
    from .m04_asset_math import proportional_models
    found+=proportional_models(lookup,program)
    # A directly redeemable caller ledger is sufficient without a total-supply variable.
    for fn,paths in program.items():
        for pi,p in enumerate(paths):
            if p["flow"] not in ("normal","returned") or p["issues"]:continue
            for payment in p.get("native_transfers",[]):
                if payment["recipient"].get("kind")!="actual_sender":continue
                if conditions_possible(p["guards"],payment["success"]):continue
                amount=polynomial(payment["amount"])
                for d in changes(p,lookup):
                    if amount and d["delta"]==negative(amount) and field_holder(d["write"]["path"],lookup) and keys(d["write"]["path"])[0].get("kind")=="actual_sender":
                        found.append({"kind":"direct_native_redeemable_ledger","balance_root":d["write"]["path"]["root"],
                          "supply_root":None,"balance_effect":d["write"],"native_payment":payment,
                          "redemption_function":fn,"path_index":pi,"unit_relation":"source checked one-to-one native redemption"})
    from .m14_financial_relations import proposed_field_models
    found.extend(proposed_field_models(lookup,program,None))
    result=unique_assets(found)
    lookup._v22_asset_models=copy.deepcopy(result)
    return result

def source_signed_changes(lookup,path,updates):
    """Classify deltas under the source constraints, not coefficient signs."""
    e=MechanismEncoder(lookup);z=e.z
    for v in path.get("evaluated_terms",[]):e.expr(v)
    guards=[e.expr(v) for v in path["guards"]]
    values=[e.expr(quantity(d["delta"])) for d in updates]
    solver=z.Solver();solver.set(timeout=3000);solver.add(*e.constraints,*guards)
    premise=bounded_solve(solver)
    if premise==z.unsat:return []
    if premise==z.unknown:raise Unsupported('delta_source_domain_solver_unknown:'+solver.reason_unknown())
    if e.abstract_hash_used:raise Unsupported('delta_source_domain_abstract_hash')
    result=[]
    for change,value in zip(updates,values):
        solver.push();solver.add(value>0);positive=bounded_solve(solver);solver.pop()
        solver.push();solver.add(value<0);negative_result=bounded_solve(solver);solver.pop()
        if z.unknown in (positive,negative_result):raise Unsupported("delta_sign_solver_limit")
        sign="positive" if positive==z.sat and negative_result==z.unsat else "negative" if negative_result==z.sat and positive==z.unsat else "zero" if positive==negative_result==z.unsat else "conditional"
        result.append({**change,"source_sign":sign})
    return result

def interference(lookup,program,assets,rows,limitations,verified_links=()):
    for fn,paths in program.items():
        for pi,p in enumerate(paths):
            if p["flow"] not in ("normal","returned"):continue
            if p["issues"]:
                limitations.append({"function":fn,"path":pi,"reason":"local_effect_path_limit","details":p["issues"]});continue
            for asset in assets:
                try:
                    root=asset["balance_root"]
                    from .m14_financial_relations import require_field_guard_scope
                    require_field_guard_scope(p,asset,lookup)
                    from .m13_financial_relations import component_updates,component_holder
                    updates=component_updates(p,lookup,asset)
                    if not updates:continue
                    total={}
                    for d in updates:total=add(total,d["delta"])
                    if total is None:raise Unsupported("ledger_net_delta_not_bound")
                    priv=privilege(p["guards"],lookup,root)
                    if not priv:continue
                    # Existence of positive net creation is queried with source
                    # constraints; algebraic coefficients alone are insufficient.
                    if total:
                        net_creation=total;backing=None
                        if asset.get('unit_relation') in ('one ledger unit to one native value unit in this source path','source checked one-to-one native redemption','source checked one-to-one same-holder native redemption'):
                            # One-to-one native claims are created against actual
                            # transaction value. Extra credited units remain tested.
                            incoming={'kind':'transaction_value','type':'uint256'}
                            net_creation=add(total,negative(polynomial(incoming)))
                            backing={'kind':'same_unit_native_inflow','amount':incoming,'source_relation':asset.get('unit_relation')}
                        q=quantity(net_creation)
                        rows.append(probe(lookup,p["guards"],op("and",op("or",*priv),op(">",q,lit(0))),
                            {"asset":asset,"kind":"privileged_net_creation","backing_adjustment":backing,"arithmetic_scope":p.get('arithmetic_scope',[]),"evaluation_terms":p.get("evaluated_terms",[])},
                            updates[0]["write"]["source"],fn,"FCR-MINT"))
                    signed=source_signed_changes(lookup,p,updates)
                    if any(x["source_sign"]=="conditional" for x in signed):
                        raise Unsupported("mixed_effect_direction_requires_source_partition")
                    debits=[d for d in signed if d["source_sign"]=="negative"]
                    credits=[d for d in signed if d["source_sign"]=="positive"]
                    # With multiple debtors and recipients, a total balance equation
                    # does not uniquely say whose debit funded which credit.
                    if len(debits)>1 and credits:
                        raise Unsupported("multiple_debtor_component_allocation_not_bound")
                    for debit in debits:
                        selector=debit["write"]["path"]
                        if not component_holder(selector,asset,lookup):continue
                        holder=keys(selector)[0];amount=negative(debit["delta"])
                        from .m13_custody import inspect as custody_inspect
                        rows.extend(custody_inspect(lookup,program,asset,p,fn,debit,credits,amount,priv,probe,quantity))
                        if holder.get("kind")=="actual_sender":continue
                        payments=p.get("native_transfers",[])
                        matched_payments=[x for x in payments if polynomial(x["amount"])==amount]
                        if any(key(x["recipient"])==key(holder) for x in matched_payments):continue
                        recipient=keys(credits[0]["write"]["path"])[0] if len(credits)==1 and component_holder(credits[0]["write"]["path"],asset,lookup) else matched_payments[0]["recipient"] if len(matched_payments)==1 else None
                        consent,cert=consent_model(p,holder,amount,lookup,program,root,asset.get("supply_root"),recipient=recipient)
                        local_certificate=cert
                        from .m16_shared_links import exact_consent
                        shared_consent=exact_consent(verified_links,fn,pi,selector,amount,debit['write']['source'])
                        if shared_consent:consent,cert,used_link=shared_consent
                        common=[op("or",*priv),op(">",quantity(amount),lit(0)),op("!",consent)]
                        meta={"asset":asset,"kind":"privileged_holder_interference","holder":holder,"debit":debit,
                              "credits":credits,"consent":consent,"consent_sources":cert,
                              "total_debit":amount,"net_delta":total,"arithmetic_scope":p.get("arithmetic_scope",[]),"evaluation_terms":p.get("evaluated_terms",[])}
                        if shared_consent:
                            meta['verified_relation_ids']=[used_link['relation_id']]
                            meta['shared_authorization_certificate']=used_link['certificate']
                        transfer_options=[]
                        for credit in credits:
                            if component_holder(credit["write"]["path"],asset,lookup):
                                transfer_options.append(op("and",op(">",quantity(credit["delta"]),lit(0)),op("!=",holder,keys(credit["write"]["path"])[0])))
                        for payment in matched_payments:
                            transfer_options.append(op("and",payment["success"],op("!=",holder,payment["recipient"])))
                        # Net-positive mixed creation is a separate mechanism; no
                        # arbitrary allocation of newly minted units to a debit.
                        if transfer_options:
                            risk=op("and",*common,op("<=",quantity(total),lit(0)),op("or",*transfer_options))
                            rows.append(probe(lookup,p["guards"],risk,copy.deepcopy(meta),debit["write"]["source"],fn,"FCR-TRANSFER"))
                        # Net loss is a separately evidenced component even when
                        # another part is transferred. Unknown compensation prevents
                        # inventing a loss component.
                        if not payments:
                            loss=negative(total) if len(debits)==1 else amount
                            from .m25_asset_services import shared_spend_limit
                            shared_limit=shared_spend_limit(lookup,program,asset,fn,local_certificate) if not credits else None
                            if shared_limit:
                                # Retain the path's allowance checks and actual consumption.
                                # An explicit burn request or signature has a distinct certificate.
                                limited=op("and",op("or",*priv),op("!=",holder,{"kind":"actual_sender"}),
                                           op(">=",local_certificate[0]['allowance'],quantity(amount)),op(">",quantity(amount),lit(0)),op(">",quantity(loss),lit(0)))
                                rows.append(probe(lookup,p["guards"],limited,{**copy.deepcopy(meta),"kind":"privileged_destruction_within_general_spend_limit",
                                    "shared_limit":shared_limit,"scope":"third-party loss limited by holder-issued general spending allowance"},
                                    debit["write"]["source"],fn,"FCR-DESTROY"))
                            risk=op("and",*common,op(">",quantity(loss),lit(0)))
                            rows.append(probe(lookup,p["guards"],risk,{**copy.deepcopy(meta),"loss_component":loss},
                                              debit["write"]["source"],fn,"FCR-DESTROY"))
                except Unsupported as ex:limitations.append({"function":fn,"path":pi,"reason":str(ex),"asset":asset["balance_root"]})

def redemption_control_summary(action,asset,lookup):
    from .m05_equity_relations import linear_quantity
    updates=[d for d in changes(action,lookup) if asset_matches(d['write']['path'],asset) and d['delta']]
    if len(updates)!=1 or not updates[0]['delta'] or not all(c<0 for c in updates[0]['delta'].values()):return None
    debit=updates[0];selector=debit['write']['path']
    if not field_holder(selector,lookup):return None
    holder=keys(selector)[0]
    for payment in action.get('native_transfers',[]):
        if key(payment['recipient'])!=key(holder) or conditions_possible(action['guards'],payment['success']):continue
        amount=negative(debit['delta'])
        return {'holder':holder,'recipient':holder,'asset_keys':[], 'amount':linear_quantity(amount),'amount_terms':amount,
            'debit':debit['write'],'native_payment':payment,'kind':'holder_native_redemption'}
    return None

def blocking(lookup,program,assets,rows,limitations,queue=None,target=None):
    from .m05_control_obligations import bind_key,privilege as control_privilege
    from .m05_control_baseline import transfer_summary,normal_baseline,transfer_route_predicates
    transfer_routes={}
    from .m05_state_relations import control_type,control_contribution,consumed_control_with_asset
    for fn,paths in program.items():
        for pi,action in enumerate(paths):
            if action["flow"] not in ("normal","returned") or action["issues"]:continue
            if queue and (fn,pi) not in queue.committed[target]:continue
            for asset in assets:
                try:
                    from .m14_financial_relations import require_field_guard_scope
                    require_field_guard_scope(action,asset,lookup)
                    summary=transfer_summary(action,asset,lookup) or redemption_control_summary(action,asset,lookup)
                except Unsupported as ex:limitations.append({"function":fn,"reason":str(ex)});continue
                if not summary:continue
                root=asset["balance_root"]
                for control in {key(s):s for s in selectors(action["guards"]) if s["root"] not in (root,asset.get("supply_root")) and control_type(value_type(s,lookup))}.values():
                    if control.get("segments"):
                        control_keys=keys(control)
                        if len(control_keys)!=1:continue
                        if key(control_keys[0])==key(summary['holder']):rule='FCR-FREEZE'
                        elif summary.get('recipient') is not None and key(control_keys[0])==key(summary['recipient']):rule='FCR-FREEZE'
                        else:continue
                    else:rule="FCR-PAUSE"
                    try:
                        from .m10_applicability import control_conditions
                        route_key=(fn,asset_identity(asset['balance_effect']['path']))
                        if route_key not in transfer_routes:transfer_routes[route_key]=transfer_route_predicates(paths,asset,lookup)
                        permit,role_evidence=control_conditions(action['guards'],control,action.get('evaluated_terms',[]),transfer_routes[route_key])
                        if not permit:
                            limitations.append({'function':fn,'control':control,'reason':'calculation_condition_not_transfer_permission','source_role':role_evidence});continue
                        from .m25_asset_services import service_baseline,required_on_delivery
                        service=service_baseline(action,summary,control,fn,asset,lookup) if rule=='FCR-FREEZE' else None
                        try:
                            baseline=normal_baseline(action,summary,control,asset,lookup,program)
                        except Unsupported:
                            if not service:raise
                            baseline=service
                        # The normal user's ability must not itself require independent administrator privilege.
                        if queue:
                            setters={}
                            for rec in queue.writer_paths(target,control):
                                pos=rec['function'],rec['path_index']
                                if pos in queue.committed[target]:
                                    setters.setdefault(pos[0],{})[pos[1]]=queue.committed[target][pos]
                            transitions_by_entry=((s,ts.items()) for s,ts in setters.items())
                            if not setters:
                                queue.note(target,fn,pi,'no_reachable_setter','no_committed_write_to_this_control',source=summary['debit']['source'])
                        else:
                            transitions_by_entry=((s,enumerate(ts)) for s,ts in program.items())
                        for setter,transitions in transitions_by_entry:
                            for ti,t in transitions:
                                if t["flow"] not in ("normal","returned") or t["issues"]:continue
                                priv=control_privilege(t["guards"],lookup,(root,control["root"]))
                                if priv==lit(False):continue
                                for w in t["writes"]:
                                    if w["path"]["root"]!=control["root"] or key(w["path"].get("instance"))!=key(control.get("instance")):continue
                                    mapping={}
                                    if len(keys(w["path"]))!=len(keys(control)):continue
                                    for a,b in zip(keys(w["path"]),keys(control)):bind_key(a,b,mapping)
                                    caller={"kind":"transition_caller","function":setter,"type":"address"}
                                    actual=remap(t,mapping,caller)
                                    available_service=service if service and required_on_delivery(paths,action,permit,asset,lookup,actual) else None
                                    if baseline is service and not available_service:continue
                                    if consumed_control_with_asset(actual["writes"],control,root,lookup):continue
                                    before=op("and",*permit)
                                    contribution=control_contribution(before,actual["writes"],control,lookup)
                                    controlled=contribution["control_writes"]
                                    after=contribution["post_action"]
                                    reference=contribution["reference_post_action"]
                                    # The affected request belongs to an ordinary caller, not
                                    # the same independent authority that can set this control.
                                    # Otherwise an owner's sale inventory can impersonate
                                    # a public holder merely by satisfying caller == owner.
                                    ordinary_caller=op("!",remap(priv,mapping,{"kind":"actual_sender"}))
                                    normal_request=op("and",baseline["predicate"],ordinary_caller)
                                    if available_service:
                                        account=available_service['affected_account']
                                        # It is an ordinary account being denied service,
                                        # even when an authorized intermediary submits the transfer.
                                        service_request=op("and",service['predicate'],op("!",remap(priv,mapping,account)))
                                        normal_request=service_request if baseline is service else op("or",normal_request,service_request)
                                    risk=op("and",normal_request,remap(priv,mapping,caller),
                                        op(">",summary["amount"],lit(0)),reference,op("!",after))
                                    rows.append(probe(lookup,action["guards"]+actual["guards"],risk,
                                        {"asset":asset,"kind":"local_privileged_transfer_blocking","control":control,
                                         "setter":setter,"holder":summary["holder"],"affected_direction":('incoming' if keys(control) and key(keys(control)[0])!=key(summary['holder']) else 'outgoing'),"normal_baseline":baseline,"ordinary_caller_not_control_authority":ordinary_caller,"control_role":role_evidence,
                                       "service_scope":available_service,"before":before,"after":after,"transition":controlled,"control_contribution":contribution,
                                         "evaluation_terms":action.get("evaluated_terms",[])+actual.get("evaluated_terms",[])},
                                        w["source"],fn,rule))
                    except Unsupported as ex:limitations.append({"function":fn,"control":control,"reason":str(ex)})

def analyze(lookup,program,hints=(),link_verifier=None,semantic_balances=(),queue=None,target=None):
    rows=[];limits=[]
    try:assets=models(lookup,program)
    except Unsupported as ex:
        assets=[];limits.append({"phase":"asset_model","reason":str(ex)})
    represented={m['balance_root'] for m in assets}
    limits.extend({'phase':'asset_witness',**g} for g in lookup.__dict__.get('_asset_witness_limits',[]) if g.get('root') not in represented)
    if not assets and not any(g.get('phase')=='asset_witness' for g in limits):
        candidates=sorted({w['path']['root'] for ps in program.values() for p in ps for w in p['writes'] if holder_path(w['path'],lookup)})
        if candidates:limits.append({'phase':'asset_witness','reason':'address_ledger_without_verified_transfer_or_redemption','candidate_roots':candidates,'not_safe_evidence':True})
    existing={m["balance_root"] for m in assets}
    assets.extend(m for m in proposed_asset_models(lookup,program,hints) if m["balance_root"] not in existing)
    from .m14_financial_relations import proposed_field_models
    assets.extend(proposed_field_models(lookup,program,hints))
    assets=unique_assets([*assets,*semantic_balances])
    from .m13_financial_relations import attach_components
    attach_components(lookup,program,assets,hints)
    from .m13_custody import claims
    for asset in assets:asset["custody_claim_certificates"]=claims(lookup,program,asset)
    verified_links=link_verifier(assets) if link_verifier else []
    interference(lookup,program,assets,rows,limits,verified_links)
    blocking(lookup,program,assets,rows,limits,queue,target)
    from .m13_destruction import analyze as destruction
    destruction(lookup,program,assets,probe,rows,limits)
    from .m20_ledger import analyze as abstract_destruction
    extra,gaps=abstract_destruction(lookup,program,assets,probe)
    rows.extend(extra);limits.extend(gaps)
    return rows,limits,assets

def proposed_asset_models(lookup,program,hints):
    """LLM locates a candidate redemption; program proves the same-holder money relation."""
    found=[]
    for hint in hints:
        if hint["kind"]!="debits_for_redemption":continue
        root=hint.get("resource_root")
        for fn in hint["functions"]:
            for pi,path in enumerate(program.get(fn,[])):
                if path["flow"] not in ("normal","returned") or path["issues"]:continue
                for payment in path.get("native_transfers",[]):
                    amount=polynomial(payment["amount"])
                    if not amount or conditions_possible(path["guards"],payment["success"]):continue
                    for change in changes(path,lookup):
                        selector=change["write"]["path"]
                        if selector["root"]!=root or not holder_path(selector,lookup):continue
                        if key(keys(selector)[0])!=key(payment["recipient"]) or change["delta"]!=negative(amount):continue
                        from .m15_relations import financial_scope
                        if not financial_scope(hint,path,fn,selector,lookup,amount=payment["amount"],recipients=[payment["recipient"]]):continue
                        found.append({"kind":"source_checked_semantic_redemption","balance_root":root,"supply_root":None,
                            "balance_effect":change["write"],"native_payment":payment,"redemption_function":fn,
                            "path_index":pi,"relation_id":hint["id"],
                            "unit_relation":"source checked one-to-one same-holder native redemption",
                            "scope":"actual native disposition establishes financial meaning; no solvency assumption"})
    return found
