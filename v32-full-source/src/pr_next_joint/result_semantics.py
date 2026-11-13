"""Result-state semantics and R4.1 aggregation.

No outcome other than an explicit supported finding is a safety conclusion.
No-model is a normal solver outcome, not a tool error. Deferred real-project
items are listed separately and never count as passed.
"""
from .core import require

OUTCOMES = [
    'supported', 'refuted_in_scope', 'infeasible_premise',
    'critical_unresolved', 'unknown', 'no_model', 'model_unsat',
    'model_sat_candidate', 'timeout', 'tool_error', 'truncated', 'unsupported',
    'concrete_execution_failed', 'replay_failed', 'not_executed',
]

R4_ITEMS = ['R4-A1', 'R4-A2', 'R4-A3', 'R4-A4', 'R4-A5', 'R4-A6', 'R4-A7', 'R4-A8']

def classify_outcome(*, premise=None, solver=None, execution='not_executed',
                     replay=None, unresolved=None, tool_error=None, timeout=False,
                     verdict=None, source='concrete', status=None):
    """Return a typed outcome. Never returns a safety claim."""
    if unresolved:
        return 'critical_unresolved'
    if tool_error:
        return 'tool_error'
    if timeout:
        return 'timeout'
    if status in {'no_model', 'model_unsat', 'model_sat_candidate', 'unknown', 'timeout', 'tool_error', 'truncated', 'unsupported'}:
        return status
    if execution in {'failed', 'error'}:
        return 'concrete_execution_failed'
    if replay is False:
        return 'replay_failed'
    if premise == 'unsat':
        return 'infeasible_premise'
    if solver == 'unsat':
        if source == 'abstract':
            return 'model_unsat'
        return 'refuted_in_scope' if execution == 'completed' and replay is True else 'unknown'
    if solver == 'sat':
        if source == 'abstract':
            return 'model_sat_candidate'
        if execution == 'completed' and replay:
            return 'supported' if verdict == 'supported' else 'refuted_in_scope'
        return 'unknown'
    if solver == 'no_model':
        return 'no_model'
    if solver in {None, 'unknown', 'not_called'}:
        return 'unknown'
    return 'unknown'

def is_safety_conclusion(outcome):
    """No component outcome is a safety conclusion, including no-model/UNSAT."""
    return False

def is_reportable_finding(outcome, verdict=None, query_solver=None, replay=None):
    return outcome == 'supported' and verdict == 'supported' and query_solver == 'sat' and replay is True

def aggregate_r4_status(evidence, deferred=None):
    """Compute the R4.1 aggregate from item evidence.

    evidence: mapping R4-A1..A8 -> {'status': passed|partial|not_run|blocked, ...}
    deferred: optional list of deferred_by_R4_scope identifiers; never passed.
    """
    require(isinstance(evidence, dict), 'R4_EVIDENCE_REQUIRED')
    missing = [item for item in R4_ITEMS if item not in evidence]
    if missing:
        return {'status': 'c2_partial_with_named_gaps', 'basis': 'C2_R4_1',
                'named_gaps': ['missing R4 evidence: ' + ','.join(missing)],
                'deferred_by_R4_scope': list(deferred or []), 'scientific_acceptance_claimed': False}
    statuses = {item: evidence[item].get('status') for item in R4_ITEMS}
    blocked = [item for item in R4_ITEMS if statuses[item] == 'blocked']
    if blocked:
        status = 'c2_blocked_for_decision'
    elif all(statuses[item] == 'passed' for item in R4_ITEMS):
        status = 'c2_ready_for_independent_review'
    else:
        status = 'c2_partial_with_named_gaps'
    gaps = []
    for item in R4_ITEMS:
        if statuses[item] != 'passed':
            reason = evidence[item].get('reason') or statuses[item]
            gaps.append(item + ':' + str(reason))
    return {'status': status, 'basis': 'C2_R4_1', 'items': statuses,
            'named_gaps': gaps, 'deferred_by_R4_scope': list(deferred or []),
            'scientific_acceptance_claimed': False,
            'ready_for_review_is_not_scientific_acceptance': True}

def component_status(rows, leads, failures):
    """Component-only status; never upgrades to joint-method or R4.1 pass."""
    counts = {}
    for row in rows:
        kind = row.get('outcome_kind') or classify_outcome(
            premise=(row.get('solver') or {}).get('premise'),
            solver=(row.get('solver') or {}).get('query'),
            execution=row.get('execution_status'), replay=row.get('same_engine_replay_equal'),
            unresolved=row.get('unresolved'), verdict=row.get('verdict'))
        counts[kind] = counts.get(kind, 0) + 1
    for failure in failures or []:
        kind = 'timeout' if failure.get('status') == 'timeout' else 'tool_error'
        counts[kind] = counts.get(kind, 0) + 1
    return {'status': 'c2_partial_with_named_gaps', 'component_only': True,
            'outcome_counts': counts, 'joint_method_acceptance': False,
            'scientific_acceptance_claimed': False}
