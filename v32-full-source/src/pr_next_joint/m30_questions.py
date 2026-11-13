"""Source-bound behavioral questions. No verdict, policy expression or executable text on the wire."""
from .core import digest

KINDS = {
    "AC": {"acquire_then_use", "early_termination", "repeat_credit"},
    "FCR": {"restrict_account", "holder_loss"},
}
FIELDS = {"kind", "operation", "comparison", "operation_refs", "comparison_refs",
          "alternative_refs", "normal_explanation", "expected_difference", "preparation"}


def normalize_questions(rows, context):
    if not isinstance(rows, list):
        return [], [{"path": "$.behavior_questions", "reason": "questions_not_array"}]
    ops = {o["id"]: o for o in context["operations"]}
    refs = context["references"]
    allowed = KINDS[context["analysis_scope"]]
    result, errors = {}, []
    for i, q in enumerate(rows):
        try:
            if not isinstance(q, dict) or set(q) - (FIELDS | {"id"}):
                raise ValueError("unrecognized_question_field")
            if not isinstance(q.get("kind"), str) or q["kind"] not in allowed:
                raise ValueError("kind_outside_requested_scope")
            ends = []
            for k in ("operation", "comparison"):
                if not isinstance(q.get(k), str) or q[k] not in ops:
                    raise ValueError("unknown_" + k)
                ends.append(ops[q[k]])
            a, b = ends
            if a["target"] != b["target"] or a["id"] == b["id"]:
                raise ValueError("requires_two_distinct_entries_of_same_target")
            item = {k: q[k] for k in ("kind", "operation", "comparison")}
            allowed_ids = set()
            for op, k in zip(ends, ("operation_refs", "comparison_refs")):
                ids = set(op["source_ast_ids"])
                allowed_ids.update(ids)
                raw = q.get(k)
                if not isinstance(raw, list) or not raw or len(raw) > 12:
                    raise ValueError("missing_or_excessive_" + k)
                if any(not isinstance(v, str) or v not in refs or refs[v]["target"] != op["target"]
                       or refs[v]["ast_id"] not in ids for v in raw):
                    raise ValueError("source_not_in_" + k)
                item[k] = sorted(set(raw))
            alt = q.get("alternative_refs", [])
            if not isinstance(alt, list) or len(alt) > 12 or any(not isinstance(v,str) or v not in refs or
                    refs[v]["target"] != a["target"] or refs[v]["ast_id"] not in allowed_ids for v in alt):
                raise ValueError("invalid_normal_alternative_source")
            item["alternative_refs"] = sorted(set(alt))
            if "preparation" in q:
                setup=q["preparation"]
                if not isinstance(setup,dict) or set(setup)!={"operation","actor","source_refs"}:
                    raise ValueError("invalid_preparation_shape")
                entry=ops.get(setup["operation"]) if isinstance(setup["operation"],str) else None
                if (not entry or entry["target"]!=a["target"] or entry in ends or
                        setup["actor"] not in ("subject","independent_holder")):
                    raise ValueError("invalid_preparation_entry_or_subject")
                marks=setup["source_refs"]
                if not isinstance(marks,list) or not 1<=len(marks)<=8 or any(
                        not isinstance(v,str) or v not in refs or refs[v]["target"]!=a["target"] or
                        refs[v]["ast_id"] not in entry["source_ast_ids"] for v in marks):
                    raise ValueError("invalid_preparation_source")
                item["preparation"]={"operation":entry["id"],"actor":setup["actor"],"source_refs":sorted(set(marks))}
            for field in ("normal_explanation", "expected_difference"):
                if not isinstance(q.get(field), str) or not 0 < len(q[field].strip()) <= 800:
                    raise ValueError("missing_or_oversized_" + field)
                item[field] = q[field].strip()
            # Text is descriptive only. A verifier must independently bind each effect.
            identity = {k:v for k,v in item.items() if k not in ("normal_explanation", "expected_difference")}
            item["id"] = "behavior_" + digest(identity)[:20]
            result.setdefault(item["id"], item)
        except ValueError as e:
            errors.append({"path": "$.behavior_questions[" + str(i) + "]", "reason": str(e)})
    return list(result.values()), errors


def prompt(scope):
    kinds = ", ".join(sorted(KINDS[scope]))
    return (
        "\nYou may initiate a NEW comparison even when no established authorization relation exists. "
        "In the response object put optional behavior_questions, independent of relations. "
        "Each question has kind (" + kinds + "), operation, comparison (distinct operation IDs on one target), "
        "operation_refs and comparison_refs (source IDs INSIDE the respective entries or their reachable helpers), "
        "expected_difference, normal_explanation, and alternative_refs (actual source IDs or [] if absent). "
        "For acquire_then_use use the writer then the privileged consumer. For early_termination use the possibly "
        "early exit then the normal terminating service or an independent holder redemption that could be interrupted. "
        "For an unset or private global role, cite the entry that establishes it and a distinct guarded use, even without a public getter. "
        "For repeat_credit use the credit/reset then the spending "
        "entry. For restrict_account or holder_loss use the privileged setter then an actual asset operation. "
        "For holder_loss you may also compare privileged destruction with spending under the same allowance. For restrict_account consider an approved delegated or time-bound delivery. "
        "If reaching the relevant starting state needs one additional public operation, you may include preparation "
        "with operation, actor (subject or independent_holder) and source_refs marking its real state update. "
        "The program will independently check the dependency and execute it from deployment for BOTH branches. "
        "State who acts, their starting state, whose rights change, which committed difference to test and what "
        "legitimate explanation could refute it. Do not give a verdict, authority without evidence, formulas, "
        "arbitrary addresses or code. Return few distinct, supported questions; [] is valid."
    )

