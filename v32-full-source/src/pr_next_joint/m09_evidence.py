"""Complete query identity and non-destructive, proposed cause grouping."""
import copy
from .core import digest,require

def source(row):
    return row.get("source") or row.get("effect",{}).get("source") or row.get("source_model",{}).get("effect",{}).get("source") or {}

def finalize(rows,identity):
    unique={}
    for raw in rows:
        row=copy.deepcopy(raw)
        require(bool(row.get("target")) and bool(row.get("function")),"V9_QUERY_TARGET_FUNCTION_REQUIRED")
        require(not row.get("reportable") or bool(source(row)),"V9_REPORTABLE_SOURCE_ANCHOR_REQUIRED")
        prior=row.get("id")
        payload={"identity":identity,**{k:row.get(k) for k in
            ("target","function","rule","category","path_index","effect","conditions","required_policy_candidate","risk_condition","policy_basis","source_model")},
            "source":source(row)}
        row["id"]="q_"+digest(payload)
        row["query_identity"]={"source_identity":identity,"target":row["target"],"function":row["function"],"source":source(row)}
        row["origin_query_ids"]=[prior] if prior else []
        if row["id"] in unique:
            kept=unique[row["id"]]
            require(kept.get("reportable")==row.get("reportable"),"V9_IDENTICAL_QUERY_DISAGREEMENT")
            kept["origin_query_ids"]=sorted(set(kept["origin_query_ids"]+row["origin_query_ids"]))
        else:unique[row["id"]]=row
    return list(unique.values())

def group(findings,checks,identity):
    byid={q["id"]:q for q in checks};groups={}
    for finding in findings:
        rows=[byid[x] for x in finding["evidence_query_ids"]]
        # Grouping is only a reviewer suggestion. Raw effect findings survive.
        own=finding.get('function_source');effect=finding.get('source',{})
        def contains(outer,inner):
            return bool(outer and inner and outer.get('file')==inner.get('file')
                and outer.get('start',-1)<=inner.get('start',-2)
                and inner.get('start',0)+inner.get('length',0)<=outer.get('start',0)+outer.get('length',0))
        # Merge propagation only when an independently reported public source
        # entry actually owns this effect. Two wrappers of an internal helper
        # remain distinct when no such public defect entry is present.
        candidates=[f.get('function_source') for f in findings if f['category']==finding['category']
            and contains(f.get('function_source'),effect)]
        origin_source=min(candidates,key=lambda x:x['length']) if candidates else own
        signature={"identity":identity,"function_source":origin_source or {"target":finding["target"],"function":finding["function"]},
                   "category":finding["category"],"cause":__import__(__package__+".m12_evidence",fromlist=["predicate"]).predicate(finding["cause"])}
        # Group only a source-identical authorization defect, never merely a label.
        origin=rows[0].get("policy_basis",{})
        # Several protected peers can support one missing permission at one
        # source entry. Keep those peer origins as evidence, not separate defects.
        finding["root_cause_basis"]={"source":source(rows[0]),"policy_origin":origin,
            "raw_evidence_preserved":True,"counting_requires_reference_match":True}
        gid="cause_"+digest(signature)[:24]
        finding["suggested_cause_group"]=gid
        groups.setdefault(gid,{"id":gid,"basis":signature,"finding_ids":[],"targets":[],"status":"program_suggestion_requires_evaluation_adjudication"})["finding_ids"].append(finding["id"])
    for g in groups.values():
        g['targets']=sorted({f['target'] for f in findings if f['id'] in g['finding_ids']})
        g['cross_target_source_identity']=len(g['targets'])>1
        members=[f for f in findings if f['id'] in g['finding_ids']]
        g['affected_entries']=list({(f['target'],f['function']):{'target':f['target'],'function':f['function'],'source':f.get('function_source')} for f in members}.values())
        g['effect_evidence']=[{'finding_id':f['id'],'source':f['source'],'query_ids':f['evidence_query_ids']} for f in members]
        g['policy_origins']=[copy.deepcopy(byid[q].get('policy_basis',{})) for f in members for q in f['evidence_query_ids']]
        g['counting_boundary']='same source entry and same required policy; independent causes/entries retained; reference matching remains separate'
    return list(groups.values())
