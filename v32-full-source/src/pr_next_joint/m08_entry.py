"""v9 input->M1->mandatory M2->program M3/M4, with checkpointed two-call recovery."""
import argparse,importlib,json,time
from pathlib import Path
from .core import require,digest
from .llm_stream import expected_wire_request
from .m08_light import build,messages
from .m08_protocol import normalize,recovery_messages,UnusableResponse

def read(p):return json.loads(Path(p).read_text(encoding="utf-8-sig"))
def save(p,v):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.name+".tmp");tmp.write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");tmp.replace(p)

def authentic(response,receipt,msg):
    expected={"model":"deepseek-flash","messages":msg,"response_format":{"type":"json_object"},
        "thinking":{"type":"enabled"},"reasoning_effort":"high","stream":False}
    require(receipt.get("source_nature")=="real" and receipt.get("simulated") is False,"V9_AUTHENTIC_LLM_REQUIRED")
    require(receipt.get("request_sha256")==digest(expected_wire_request(expected,receipt)),"V9_REQUEST_IDENTITY")
    if response is not None:require(receipt.get("response_sha256")==digest(response),"V9_RESPONSE_IDENTITY")

def obtain(context,msg,client,out,stage,fixture=None):
    attempts=[]
    if fixture is not None:
        result,repair=normalize(fixture,context)
        return result,{"source_nature":"explicit_test_double","simulated":True,"status":"json_received"},repair,[]
    request=msg
    for number in range(2):
        label="m08_relations_initial" if number==0 else "m08_relations_recovery"
        saved=out/("llm_attempt_"+str(number)+".json")
        if saved.exists():
            record=read(saved);require(record["messages_sha256"]==digest(request),"V9_CHECKPOINT_REQUEST_CHANGED")
            response,receipt=record["response"],record["receipt"]
        else:
            dispatch=out/("llm_dispatch_"+str(number)+".json")
            require(not dispatch.exists(),"V14_UNCHECKPOINTED_DISPATCH_REQUIRES_RECONCILIATION")
            save(out/("llm_messages_"+str(number)+".json"),request)
            # A crash or incomplete stream never silently opens a second request.
            save(dispatch,{"messages_sha256":digest(request),"attempt":number+1,
                "state":"dispatch_intent_saved","automatic_redispatch_allowed":False})
            stage("M2","calling",attempt=number+1)
            try:
                response,receipt=client.call(request,label,max_tokens=None,timeout=1800,reasoning_effort="high",thinking=True)
            except Exception as error:
                save(out/"llm_failure_diagnostic.json",{"attempt":number+1,"stage":"client_call",
                    "reason":type(error).__name__+":"+str(error),"automatic_retry_allowed":False,
                    "requires_request_reconciliation":True,"classification_available":False})
                raise
            # Save even an unusable receipt BEFORE acceptance; storage is not acceptance.
            save(saved,{"messages_sha256":digest(request),"response":response,"receipt":receipt})
        attempts.append(receipt);save(out/"llm_attempts.json",attempts)
        try:authentic(response,receipt,request)
        except Exception as error:
            save(out/"llm_failure_diagnostic.json",{"attempt":number+1,"stage":"response_acceptance",
                "reason":type(error).__name__+":"+str(error),"request_id":receipt.get("request_id"),
                "transport":receipt.get("http_response",{}),"usage_received":bool(receipt.get("usage")),
                "automatic_retry_allowed":False,"requires_request_reconciliation":not bool(receipt.get("usage")),
                "classification_available":False})
            raise
        try:
            if receipt.get("status")!="json_received" or response is None:raise UnusableResponse("response_unusable:"+str(receipt.get("status")))
            result,repair=normalize(response,context)
            save(out/"llm_attempts.json",attempts);save(out/"raw_response.json",response);save(out/"m2_consumed_messages.json",request)
            return result,receipt,repair,attempts
        except UnusableResponse as ex:
            error=str(ex)
            save(out/("unusable_response_"+str(number)+".json"),{"reason":error,"retry_reason":"protocol_or_transport_only","request_id":receipt.get("request_id")})
            # An uncertain/unsettled remote request must not be duplicated.
            if receipt.get("dispatch_started") and not receipt.get("usage"):raise ValueError("V9_UNSETTLED_RESPONSE_REQUIRES_RECONCILIATION")
            if number==0:
                request=recovery_messages(msg,error);save(out/"recovery_reason.json",{"reason":error,"same_semantic_task":True})
    save(out/"llm_attempts.json",attempts)
    raise ValueError("V9_LLM_RECOVERY_EXHAUSTED:"+error)

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--route",default="joint");p.add_argument("--targets",default="project")
    for k in ("root","case","out"):p.add_argument("--"+k,required=True)
    for k in ("manifest","bundle","native","compiled-unit","llm-module","fixture-response"):p.add_argument("--"+k)
    p.add_argument("--analysis-scope",choices=("AC","FCR"),required=True)
    p.add_argument("--proposal-scope",default="source_obligations_v1")
    p.add_argument("--phase",choices=("prepare","all"),default="all")
    a=p.parse_args(argv);root=Path(a.root).resolve();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
    require(not (out/"joint_report.json").exists(),"V9_REPORT_ALREADY_EXISTS")
    stages=[];started=time.perf_counter();active="M1"
    def stage(module,status,**kw):
        nonlocal active
        active=module;item={"module":module,"status":status,"elapsed_since_entry_seconds":time.perf_counter()-started,**kw}
        stages.append(item);save(out/"stage_log.json",stages);print(json.dumps(item,ensure_ascii=False),flush=True)
    try:
        stage("M1","started");selected=None;description=None
        if a.compiled_unit:
            from .dataset_intake import load_compiled_unit
            data=load_compiled_unit(root,a.compiled_unit);require(a.case==data["unit_id"],"V9_UNIT_IDENTITY")
            bundle,native,sources=data["bundle"],data["native"],data["sources"]
            selected=data["selected_targets"];description=data["description"]
            save(out/"intake_receipt.json",data["receipt"]);save(out/"artifact_binding.json",data["binding"])
        else:
            from .m03_source import inspect_manifest,validate_loaded_artifacts
            inspected=inspect_manifest(root,a.manifest,target_mode="project");case=next(c for c in inspected["cases"] if c["case_id"]==a.case)
            bundle,native=read(a.bundle),read(a.native);binding=validate_loaded_artifacts(case,bundle,native)
            sources=[]
            for s in binding["sources"]:
                f=(root/s["file"]).resolve();require(f.is_relative_to(root),"V9_SOURCE_PATH")
                sources.append({"file":s["file"],"sha256":s["sha256"],"content":f.read_text(encoding="utf-8")})
            save(out/"artifact_binding.json",binding)
        context,light=build(bundle,native,sources,selected,a.analysis_scope,description)
        msg=messages(context);save(out/"m1_context.json",context);save(out/"m2_messages.json",msg)
        save(out/"target_inventory.json",light["target_inventory"])
        save(out/"context_identity.json",{"schema":context["schema"],"context_sha256":digest(context),"messages_sha256":digest(msg)})
        stage("M1","completed",operations=len(context["operations"]),targets=len(light["selected_targets"]))
        if a.phase=="prepare":
            save(out/"entry_result.json",{"status":"awaiting_real_llm","real_llm":False});return 0
        require(bool(a.llm_module)!=bool(a.fixture_response),"V9_LLM_OR_EXPLICIT_FIXTURE_REQUIRED")
        client=None;fixture=read(a.fixture_response) if a.fixture_response else None
        if a.llm_module:
            module,attr=a.llm_module.split(":",1);client=getattr(importlib.import_module(module),attr)()
        stage("M2","started")
        relations,receipt,repair,attempts=obtain(context,msg,client,out,stage,fixture)
        save(out/"llm_receipt.json",receipt);save(out/"normalized_response.json",relations);save(out/"response_conversion.json",repair)
        if fixture is not None:save(out/"raw_response.json",fixture)
        stage("M2","completed",calls=len(attempts),usable_relations=len(relations["relations"]))
        from .m08_engine import analyze
        stage("M3","program_detection_started")
        report=analyze(context,light,relations,stage)
        stage("M4","checks_completed",queries=len(report["checks"]),scanned_operations=len(report["operation_scan"]))
        stage("M4","reporting")
        report["dataset_intake"]=data["receipt"] if a.compiled_unit else {}
        report["target_inventory"]=light["target_inventory"];report["targets"]=light["selected_targets"]
        report["request_id"]=receipt.get("request_id")
        report["messages_digest"]=digest(read(out/"m2_consumed_messages.json") if fixture is None else msg)
        report["real_llm"]=fixture is None
        report["diagnostic_only"]=fixture is not None
        report["llm_participation"]={"usable":True,"attempts":len(attempts),"source_nature":receipt["source_nature"]}
        if fixture is not None:
            report["status"]="diagnostic_complete";report["not_real_performance"]=True
        save(out/"joint_report.json",report)
        stage("M4","completed",classification=report["classification"])
        save(out/"entry_result.json",{"status":report["status"],"real_llm":fixture is None,"wall_seconds":time.perf_counter()-started})
        return 0
    except Exception as ex:
        save(out/"entry_result.json",{"status":"failed","stage":active,"reason":type(ex).__name__+":"+str(ex),"traceback":__import__("traceback").format_exc(),"wall_seconds":time.perf_counter()-started})
        stage(active,"failed",reason=type(ex).__name__+":"+str(ex));return 1
