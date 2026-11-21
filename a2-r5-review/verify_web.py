"""Recompute R5 review metrics from the published, frozen decision records."""

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARMS = ("G", "Simple")
VALID = {"alarm", "not_detected"}


def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8-sig"))


def check(condition, context):
    if not condition:
        raise ValueError(context)


def file_sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def check_manifest():
    manifest = read("Manifest.json")["files"]
    listed = {rec["path"] for rec in manifest}
    actual = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.relative_to(ROOT).parts
    }
    check(len(listed) == len(manifest) and actual == listed | {"Manifest.json"}, "manifest coverage")
    for rec in manifest:
        p = ROOT / rec["path"]
        check(p.stat().st_size == rec["bytes"] and file_sha(p) == rec["sha256"], rec["path"])
    return len(actual)


def measure(cases, arm):
    paired = [c for c in cases if c["arms"][arm]["run_state"] == "completed"]
    runs = [c["arms"][arm] for c in paired]
    tp = sum(len(r["matched_roots"]) for r in runs)
    fp = sum(len({tuple(x) for x in r["extra_locations"]}) for r in runs)
    roots = sum(len(c["reference_roots"]) for c in cases)
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / roots if roots else None
    f1 = 2 * tp / (roots + tp + fp) if roots + tp + fp else None
    return {
        "N": len(cases), "families": len({c["family"] for c in cases}),
        "completed": len(runs), "scored": len(runs), "roots": roots,
        "TP": tp, "FP": fp, "FN": roots - tp, "precision": precision, "recall": recall, "F1": f1,
        "unknown": sum(r["AC_projection"] not in VALID for r in runs),
        "not_run": sum(c["arms"][arm]["run_state"] == "not_run" for c in cases),
        "timeout": sum(c["arms"][arm]["run_state"] == "timeout" for c in cases),
        "error": sum(c["arms"][arm]["run_state"] == "technical_error" for c in cases),
    }


def difference(case):
    g, simple = (case["arms"][arm] for arm in ARMS)
    old_roots, new_roots = set(g["matched_roots"]), set(simple["matched_roots"])
    old_fp, new_fp = {tuple(p) for p in g["extra_locations"]}, {tuple(p) for p in simple["extra_locations"]}
    return {
        "new_tp": sorted(new_roots - old_roots), "lost_tp": sorted(old_roots - new_roots),
        "removed_fp": [list(p) for p in sorted(old_fp - new_fp)],
        "added_fp": [list(p) for p in sorted(new_fp - old_fp)],
    }


def check_ac(cases, scores):
    cases_by_member = {c["member"]: c for c in cases}
    check(len(cases_by_member) == len(cases) == 624, "624 unique AC members")
    check(sum(len(c["reference_roots"]) for c in cases) == 481, "481 author roots")
    check(len({c["family"] for c in cases}) == read("Families.json")["count_families"] == 374, "families")
    for case in cases:
        root_ids = {ref["id"] for ref in case["reference_roots"]}
        g, simple = (case["arms"][arm] for arm in ARMS)
        check(g["run_state"] == simple["run_state"], case["member"])
        check(g["archive_response_sha256"] == simple["archive_response_sha256"], case["member"])
        for run in (g, simple):
            if run["run_state"] == "timeout":
                check(all(run[key] is None for key in ("TP", "FP", "FN")), case["member"])
                continue
            hits, missed = set(run["matched_roots"]), set(run["missed_roots"])
            check((hits | missed) == root_ids and not hits & missed, case["member"])
            check((len(hits), len(run["extra_locations"]), len(missed)) ==
                  (run["TP"], run["FP"], run["FN"]), case["member"])
    groups = [
        (cases, scores["all_ac"], "all"),
        ([c for c in cases if not c["r4_exposed_family"]], scores["r4-family-excluded"], "R4-excluded"),
        ([c for c in cases if c["stratum"] == "heldout_family" and c["family_representative"]],
         scores["untouched_representatives"], "heldout representatives"),
    ]
    for stratum, expected in scores["exposures"].items():
        groups.append(([c for c in cases if c["stratum"] == stratum], expected, stratum))
    for population, expected, group in groups:
        completed = [c for c in population if all(c["arms"][arm]["run_state"] == "completed" for arm in ARMS)]
        check(len(population) == expected["eligible_members"], group)
        check(len(completed) == expected["paired_completed"], group)
        for arm in ARMS:
            check(measure(population, arm) == expected["population_accounting"][arm], (group, arm, "population"))
            check(measure(completed, arm) == expected["complete_case"][arm], (group, arm, "paired"))
        observed = Counter(key for c in completed for key, entries in difference(c).items() for _ in entries)
        check(all(observed[key] == total for key, total in expected["delta"].items()), (group, "delta"))
    evidence = read("Evidence.json")["AC_position_and_author_root_changes"]
    for case in cases:
        if case["arms"]["G"]["run_state"] == "completed":
            delta = difference(case)
            if any(delta.values()):
                check(evidence[case["member"]]["delta"] == delta, case["member"])
    check(len(evidence) == 6, "six changed members")
    timeout = read("Cases/Timeouts.json")
    members = {c["member"] for c in cases if c["arms"]["G"]["run_state"] == "timeout"}
    check(len(members) == timeout["members"] == 14 and set(timeout["cases"]) == members, "timeouts")
    check(sum(len(cases_by_member[m]["reference_roots"]) for m in members) == timeout["reference_roots"] == 9,
          "timeout reference roots")
    check(sum(r["unsealed_report_file_present"] for c in timeout["cases"].values() for r in c["arms"].values())
          == 11, "unsealed report count")


def check_fcr(groups, scores):
    members = {}
    per_arm_all = {}
    for category, group in groups.items():
        pairs = group["selected"]
        check(len(pairs) == 3, category)
        for pair in pairs:
            for side in ("risk", "repair"):
                member = pair[side]
                check(member not in members, member)
                members[member] = pair["arms"][side]
                g, s = (members[member][arm] for arm in ARMS)
                check(g["all_task_projections"] == s["all_task_projections"], member)
                check(g["archive_response_sha256"] == s["archive_response_sha256"], member)
        for arm in ARMS:
            count = dict.fromkeys(("TP", "FN_dec", "U+", "FP", "TN", "U-", "pairs", "both"), 0)
            count["pairs"] = len(pairs)
            for pair in pairs:
                risk, repair = (
                    pair["arms"][side][arm]["all_task_projections"][category]
                    for side in ("risk", "repair")
                )
                count[{"alarm": "TP", "not_detected": "FN_dec"}.get(risk, "U+")] += 1
                count[{"alarm": "FP", "not_detected": "TN"}.get(repair, "U-")] += 1
                count["both"] += risk == "alarm" and repair == "not_detected"
            count["F1"] = 2 * count["TP"] / (2 * count["TP"] + count["FP"] + count["FN_dec"] + count["U+"])
            check(count == scores[arm]["categories"][category], (category, arm))
            per_arm_all.setdefault(arm, []).append(count)
    for arm, categories in per_arm_all.items():
        counts = scores[arm]
        for metric, source in (("risk_hits", "TP"), ("repair_correct", "TN"), ("pair_correct", "both")):
            check(sum(c[source] for c in categories) == counts[metric], (arm, metric))
        check(abs(sum(c["F1"] for c in categories) / len(categories) - counts["macro_F1"]) < 1e-12,
              (arm, "FCR macro F1"))
    check(len(members) == 30, "30 unique FCR members")
    return members


def csv_consistency(cases, fcr):
    name = ROOT / "R5_EXPERIMENT_RESULTS.csv"
    check(file_sha(name) == read("Freeze.json")["source_csv_sha256"], "original CSV")
    web = {(c["member"], arm): run for c in cases for arm, run in c["arms"].items()}
    web.update({(member, arm): run for member, arms in fcr.items() for arm, run in arms.items()})
    with name.open(encoding="utf-8-sig", newline="") as data:
        rows = list(csv.DictReader(data))
    check(len(rows) == len(web) == 1308, "1308 execution slots")
    seen = set()
    for csv_row in rows:
        key = (csv_row["member"], csv_row["arm"])
        check(key not in seen, key)
        seen.add(key)
        raw = web[key]
        for field in ("run_state", "archive_response_sha256", "frozen_export_sha256"):
            stored = "" if raw[field] is None else str(raw[field])
            check(csv_row[field] == stored, (key, field))
        check(json.loads(csv_row["all_task_projections"]) == raw["all_task_projections"], key)
        if csv_row["task"] == "AC":
            for field in ("TP", "FP", "FN"):
                stated = "" if raw[field] is None else str(raw[field])
                check(csv_row[field] == stated, (key, field))
    check(set(web) == seen, "CSV member and arm coverage")


def main():
    files = check_manifest()
    scores = read("Scores.json")
    cases = [c for n in sorted((ROOT / "Cases").glob("AC-*.json"))
             for c in read(n.relative_to(ROOT))]
    check_ac(cases, scores)
    fcr = check_fcr(read("Cases/FCR.json"), scores["fcr"])
    csv_consistency(cases, fcr)
    for path, entry in read("Versions.json")["published_files"].items():
        check(file_sha(ROOT / path) == entry["sha256"], ("method file", path))
    print(f"Verified {files} web files, 624 AC cases, 15 FCR pairs and 1308 frozen slots.")


if __name__ == "__main__":
    main()
