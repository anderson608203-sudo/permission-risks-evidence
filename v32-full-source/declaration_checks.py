"""Actual evaluation of supported proposal declarations.

A declaration is accepted only when its evidence kind/sha/locator resolves to
an independent object and its check id is in this closed set. The check is
re-evaluated at validate_component time; a failed check cannot be overridden by
a SAT result or a successful external execution.
"""
from .core import require

SUPPORTED = {'source_effect_matches_candidate', 'alias_case_applicable', 'policy_source_present'}

def expected_for(check, item):
    if check == 'source_effect_matches_candidate':
        relation = item.get('source_relation', {})
        return {'function': relation.get('frame', {}).get('entry', {}).get('function'),
                'effect': relation.get('effect', {}).get('path', {}).get('declaration', {}).get('name')}
    if check == 'alias_case_applicable':
        return 'applicable'
    if check == 'policy_source_present':
        return bool(item.get('policy', {}).get('source'))
    return None

def evaluate(item):
    failures = []
    for record in item.get('proposal_application', {}).get('declaration_checks', []):
        check = record.get('check')
        expected = record.get('expected')
        if check == 'source_effect_matches_candidate':
            actual = expected_for(check, item)
            ok = actual == expected and bool(actual.get('function')) and bool(actual.get('effect'))
        elif check == 'alias_case_applicable':
            case = item.get('alias_case', {})
            ok = case.get('status') == 'applicable' and not case.get('unresolved')
        elif check == 'policy_source_present':
            ok = bool(item.get('policy', {}).get('source'))
        else:
            ok = False
        if not ok:
            failures.append({'claim': record.get('claim'), 'check': check, 'expected': expected, 'actual': expected_for(check, item) if check in SUPPORTED else None})
    return failures
