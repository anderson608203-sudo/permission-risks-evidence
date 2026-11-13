"""Nonsemantic normalization, checked references, bounded recovery protocol."""
import json
from .core import digest
from .m08_light import SCHEMA,RELATIONS

class UnusableResponse(ValueError):
    def __init__(self,reason,details=None):
        self.reason=reason;self.details=details or []
        super().__init__(reason+(':'+json.dumps(self.details,separators=(',',':')) if self.details else ''))

def parse_text(text):
    changes=[]
    if not isinstance(text,str):raise UnusableResponse("empty_or_nontext_response")
    s=text.strip()
    if s.startswith("```") and s.endswith("```"):
        first,sep,s=s.partition("\n")
        if not sep or first.lower() not in ("```","```json"):raise UnusableResponse("unrecognized_code_fence")
        s=s[:-3].strip();changes.append("removed_json_code_fence")
    try:obj=json.loads(s)
    except (ValueError,TypeError) as e:raise UnusableResponse("invalid_json") from e
    return obj,changes

def normalize(response,context):
    changes=[];rejected=[]
    if isinstance(response,str):response,changes=parse_text(response)
    if not isinstance(response,dict) or response.get("schema")!=SCHEMA:raise UnusableResponse("wrong_or_missing_schema")
    rows=response.get("relations")
    if isinstance(rows,dict):rows=[rows];changes.append("single_relation_to_list")
    if not isinstance(rows,list):raise UnusableResponse("relations_not_array")
    ops={o["id"]:o for o in context["operations"]};refs=context["references"];good=[]
    for index,original in enumerate(rows):
        try:
            if not isinstance(original,dict):raise UnusableResponse("relation_not_object")
            r=dict(original)
            if not isinstance(r.get("relation_kind"),str) or r.get("relation_kind") not in RELATIONS:raise UnusableResponse("relation_kind_not_allowed")
            if not isinstance(r.get("op_ref"),str) or r.get("op_ref") not in ops:raise UnusableResponse("unknown_operation")
            target=ops[r["op_ref"]]["target"]
            r.setdefault('resource_refs',[])
            for field in ("related_op_refs","condition_refs","source_refs","resource_refs"):
                if field!='source_refs' and r.get(field) is None:r[field]=[];changes.append({'row':index,'field':field,'action':'null_optional_to_empty'})
                if isinstance(r.get(field),str):r[field]=[r[field]];changes.append({"row":index,"field":field,"action":"single_to_list"})
                if not isinstance(r.get(field),list) or not all(isinstance(v,str) for v in r[field]):raise UnusableResponse(field+"_not_array")
            if not r["source_refs"]:raise UnusableResponse("no_source_evidence")
            for field in ("subject_ref","resource_ref"):
                if r.get(field) is not None and not isinstance(r[field],str):raise UnusableResponse(field+"_invalid")
            # The op is already identified by op_ref. Remove only its exact
            # duplicate, and only when all remaining evidence anchors are valid.
            remaining=[x for x in r['source_refs'] if x!=r['op_ref']]
            if len(remaining)!=len(r['source_refs']) and remaining and all(x in refs and refs[x]['target']==target for x in remaining):
                r['source_refs']=remaining
                changes.append({'row':index,'field':'source_refs','action':'removed_redundant_current_op_ref','retained_source_refs':remaining})
            allrefs=r["source_refs"]+r["condition_refs"]+r["resource_refs"]+[r[k] for k in ("subject_ref","resource_ref") if r.get(k)]
            if any(x not in refs or refs[x]["target"]!=target for x in allrefs):raise UnusableResponse("reference_identity_mismatch")
            if any(x not in ops or ops[x]["target"]!=target for x in r["related_op_refs"]):raise UnusableResponse("related_operation_identity_mismatch")
            if not isinstance(r.get("explanation"),str):raise UnusableResponse("explanation_missing")
            allowed=("op_ref","relation_kind","subject_ref","resource_ref","resource_refs","related_op_refs","condition_refs","source_refs","explanation")
            from .m15_schema import normalize_scope,FIELDS
            for field in FIELDS:
                if field in r and r[field] is None:
                    r[field]=[];changes.append({'row':index,'field':field,'action':'null_optional_to_empty'})
            scoped=normalize_scope(r,ops,refs,target,UnusableResponse)
            r={k:r.get(k) for k in allowed}
            r.update(scoped)
            for field in ('related_op_refs','condition_refs','source_refs','resource_refs'):
                r[field]=sorted(set(r[field]))
            r["id"]="rel_"+digest(r)[:20];r["reference_status"]="source_located_semantics_still_checked_by_program"
            good.append(r)
        except UnusableResponse as e:rejected.append({"row":index,"reason":str(e)})
    unique={}
    for r in good:
        identity=digest({k:v for k,v in r.items() if k not in ('id','explanation','reference_status')})
        if identity in unique:
            changes.append({'action':'duplicate_relation_same_bindings','retained_id':unique[identity]['id'],'duplicate_id':r['id'],'explanation':r['explanation']})
        else:unique[identity]=r
    good=list(unique.values())
    # v20-p1: the previous prompt did not unambiguously locate this optional
    # field. Preserve standalone proposals without inventing a parent relation,
    # peer operations, authority, or any semantic evidence.
    from .m15_schema import normalize_scope
    standalone=[];outer=response.get('authorization_hypotheses',[])
    if not isinstance(outer,list):
        rejected.append({'path':'$.authorization_hypotheses','reason':'authorization_hypotheses_not_array'})
    else:
        for i,h in enumerate(outer):
            try:
                if not isinstance(h,dict) or not isinstance(h.get('op_ref'),str) or h['op_ref'] not in ops:
                    raise UnusableResponse('unknown_hypothesis_operation')
                target=ops[h['op_ref']]['target']
                parsed=normalize_scope({'authorization_hypotheses':[h]},ops,refs,target,UnusableResponse)['authorization_hypotheses'][0]
                standalone.append(parsed)
            except UnusableResponse as e:
                rejected.append({'path':'$.authorization_hypotheses['+str(i)+']','reason':str(e)})
    # Unknown semantic material must never disappear without a diagnostic.
    from .m30_questions import normalize_questions
    questions, question_errors = normalize_questions(response.get('behavior_questions', []), context)
    rejected.extend(question_errors)
    for field in sorted(set(response)-{'schema','relations','authorization_hypotheses','behavior_questions'}):
        rejected.append({'path':'$.'+field,'reason':'unsupported_top_level_field_not_consumed'})
    if (rows or outer or rejected) and not good and not standalone and not questions:
        raise UnusableResponse('no_protocol_usable_relationship',rejected)
    nested={digest(h) for r in good for h in r.get('authorization_hypotheses',[])}
    unique_h={}
    for h in standalone:
        identity=digest(h)
        if identity in nested or identity in unique_h:
            changes.append({'action':'duplicate_standalone_hypothesis','hypothesis_digest':identity,
                            'retained_location':'nested' if identity in nested else 'standalone'})
        else:unique_h[identity]=h
    standalone=list(unique_h.values())
    result={'schema':SCHEMA,'relations':good}
    if standalone:result['authorization_hypotheses']=standalone
    if questions:result['behavior_questions']=questions
    return result,{'normalizations':changes,'rejected_items':rejected,
        'standalone_hypotheses_retained':len(standalone),
        'standalone_hypotheses_semantics':'source identities checked; semantic acceptance remains downstream',
        'valid_empty':not rows and not outer and not questions and not rejected,'original_sha256':digest(response),'usable':True}

def recovery_messages(original,error):
    return original+[{"role":"user","content":"The previous answer could not be consumed: "+str(error)+
        ". Repeat the SAME relationship analysis with the supplied schema and references. op_ref/related_op_refs accept operation IDs; source_refs/condition_refs/subject_ref/resource_ref accept source reference IDs only. Never guess missing references. Do not give risk labels or change the task. No extra semantic review is requested."}]
