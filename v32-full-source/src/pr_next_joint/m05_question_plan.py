"""Versioned rule requirements shared by prompts, planning and audit output."""
import copy
from .core import digest

REVISION='joint-question-plan-v1-fcr-mechanism-20261027'
RULES={
    'AC-01':('permission_effect',['policy_decision','required_permission','source_effect']),
    'AC-02':('permission_state',['policy_decision','required_permission','guard_consumed_state']),
    'AC-03':('subject_object_binding',['policy_decision','required_permission','checked_subject_object','actual_effect_object']),
    'AC-04':('credential_lifecycle',['source_issuance','validity_transition','protected_effect']),
    'AC-05':('credential_use',['credential_payload','issuer_subject_domain','protected_effect']),
    'FCR-MINT':('asset_creation',['asset_relation','source_net_creation','privilege']),
    'FCR-TRANSFER':('asset_interference',['asset_relation','holder_debit','disposition','privilege','holder_consent']),
    'FCR-DESTROY':('asset_interference',['asset_relation','holder_loss','privilege','holder_consent','compensation']),
    'FCR-PAUSE':('transfer_blocking',['asset_relation','ordinary_transfer','privileged_control_change','blocked_same_request']),
    'FCR-FREEZE':('holder_transfer_blocking',['asset_relation','ordinary_holder_transfer','holder_control_change','blocked_holder_request']),
}


def catalog():
    return {'revision':REVISION,'rules':{rule:{'model_family':family,'required_relations':fields}
        for rule,(family,fields) in RULES.items()},
        'fcr_main_target':'privileged_asset_control_mechanism',
        'feasibility_is_separate':True,'registry_is_not_implemented_capability_evidence':True}


def execution_ledger(obligations,rows,bridge):
    """Record real source-to-check links without counting bridge work twice."""
    source=obligations or {};byid={r['id']:r for r in rows+source.get('source_obligation_checks',[])}
    result=[]
    for ob in source.get('source_obligations',[]):
        ids=list(dict.fromkeys(ob.get('checks',[])+ob.get('legacy_bridge',{}).get('query_ids',[])))
        actual=[byid[q] for q in ids if q in byid]
        gaps=copy.deepcopy(ob.get('model_gaps',[]))
        record={'id':ob['id'],'rule':ob['rule'],'target':ob['target'],'function':ob['function'],
            'proposal_sha256':ob['proposal_sha256'],'requirements':catalog()['rules'][ob['rule']],
            'source_bound':ob.get('source_binding_status')=='source_anchors_bound',
            'query_ids':ids,'checked_query_ids':[r['id'] for r in actual if r.get('formal',{}).get('solver_called')],
            'conclusive_query_ids':[r['id'] for r in actual if r.get('status') in ('supported','refuted_in_scope')],
            'reportable_query_ids':[r['id'] for r in actual if r.get('reportable')],
            'model_gaps':gaps,'bridge_gaps':copy.deepcopy(ob.get('legacy_bridge',{}).get('gaps',[])),
            'original_claim_proved':False}
        record['stage']='checked' if record['checked_query_ids'] else 'planned' if ids else 'bound_missing_model'
        result.append(record)
    return {'schema':REVISION,'questions':result,'unique_check_ids':sorted({i for q in result for i in q['checked_query_ids']}),
        'source_binding_errors':copy.deepcopy(source.get('source_obligation_errors',[])),
        'counting':'question links may share checks; only unique checks count as executed work',
        'bridge_identity':digest(bridge)}


def annotate_fcr(row):
    if not str(row.get('rule','')).startswith('FCR-'):return row
    model=row.get('asset_relation') or row.get('policy_basis',{}).get('asset_model') or row.get('source_model',{}).get('asset') or {}
    initial=model.get('initial_state',{})
    row.update(prediction_target='privileged_asset_control_mechanism',definition_revision='fcr-mechanism-r1-20261027',
        feasibility={'status':'known_initial_state_limitation' if initial.get('status')=='closed_zero_invariant' else 'not_verified_on_deployment',
            'initial_state':copy.deepcopy(initial),'actual_harm_proved':False,'deployment_executed':False,
            'scope':'mechanism may exist even when its positive balance/configuration precondition is not established'})
    return row
