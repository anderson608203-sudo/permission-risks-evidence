"""Report existing work without inferring coverage or invoking a solver."""
import copy
from .core import digest

CREDENTIAL_DIMENSIONS={
    'credential_alternative_use_binding':['same_payload_protected_effect_binding'],
    'credential_same_payload_replay':['same_payload_reuse_with_arbitrary_relayer'],
    'credential_cross_instance_binding':['same_issued_credential_cross_instance_use'],
    'credential_cross_action_binding':['same_issued_credential_cross_action_use'],
    'credential_duplicate_signer_acceptance':['duplicate_signer_approval_acceptance'],
    'credential_source_expiry_use':['same_issued_payload_later_use_against_source_deadline'],
    'credential_invalid_r_zero_acceptance':['invalid_ecrecover_r_zero_return_accepted'],
    'credential_declared_expiry_use':['same_issued_credential_use_after_declared_expiry'],
    'credential_revoked_boolean_use':['same_issued_credential_use_after_bound_boolean_revocation'],
}

def evidence_state(row):
    formal=row.get('formal') or {}
    attempted=formal.get('solver_called') is True
    answered=attempted and formal.get('premise')=='sat' and formal.get('query') in ('sat','unsat')
    program_checked=bool((row.get('program_analysis_certificate') or {}).get('verified') and row.get('status')=='refuted_in_scope')
    conclusive=program_checked or bool(answered and formal.get('status') in ('supported','refuted_in_scope')
        and row.get('status') in ('supported','refuted_in_scope'))
    return {'model_constructed':bool(row.get('source_model') or row.get('effect') and row.get('required_policy_candidate')),'formal_attempted':attempted,'program_analysis_checked':program_checked,
        'solver_returned_answer':bool(answered),'model_conclusive':conclusive,
        'formal_inconclusive':attempted and not conclusive,
        'work_accounting_unknown':formal.get('solver_called') is None or bool(formal.get('accounting_incomplete')),
        'reason':formal.get('reason')}

def question_id(obligation,field,index,value):
    return 'cq_'+digest({'proposal_sha256':obligation['proposal_sha256'],
        'field':field,'index':index,'value':value})

def questions(obligation):
    proposal=obligation['original_proposal'];mechanism=proposal.get('mechanism',{})
    credential=mechanism.get('credential',{})
    result=[]
    if isinstance(credential,dict):
        relations=credential.get('validity_relations',[])
        if isinstance(relations,list):
            for i,relation in enumerate(relations):
                result.append({'question_id':question_id(obligation,'credential.validity_relations',i,relation),
                    'field':'credential.validity_relations','index':i,'relation':copy.deepcopy(relation)})
    return result

def trace(obligation,rows,gaps):
    result=[]
    attempts=obligation.get('_model_attempts',[])
    for q in questions(obligation):
        refs=[r for r in rows if q['question_id'] in r.get('source_model',{}).get('question_refs',[])]
        missing=[g for g in gaps if g.get('question_id')==q['question_id']]
        conclusive=[r['id'] for r in refs if evidence_state(r)['model_conclusive']]
        result.append({**q,'proposal_sha256':obligation['proposal_sha256'],
            'scope':{'target':obligation['target'],'function':obligation['function']},
            'model_refs':[a['id'] for a in attempts if q['question_id'] in a.get('question_refs',[])],
            'attempted_query_refs':[r['id'] for r in refs if evidence_state(r)['formal_attempted']],
            'conclusive_query_refs':conclusive,
            'unresolved_model_refs':[r['id'] for r in refs if not evidence_state(r)['model_conclusive']],
            'unmodeled_gaps':copy.deepcopy(missing),
            'local_model_conclusive':bool(conclusive),
            # No all-path enumeration/completion certificate is inferred from
            # the existence of a local SAT or UNSAT result.
            'original_question_completion':'unresolved_scope_coverage'})
    modeled={d for r in rows for d in r.get('source_model',{}).get('checked_dimensions',[])}
    attempted={d for r in rows if evidence_state(r)['formal_attempted'] for d in r.get('source_model',{}).get('checked_dimensions',[])}
    conclusive={d for r in rows if evidence_state(r)['model_conclusive'] for d in r.get('source_model',{}).get('checked_dimensions',[])}
    inconclusive={d for r in rows if evidence_state(r)['formal_attempted'] and not evidence_state(r)['model_conclusive']
        for d in r.get('source_model',{}).get('checked_dimensions',[])}
    return {'explicit_questions':result,'model_attempts':copy.deepcopy(attempts),
        'modeled_dimensions':sorted(modeled),'attempted_dimensions':sorted(attempted),
        'conclusive_dimensions':sorted(conclusive),'inconclusive_dimensions':sorted(inconclusive),
        'original_question_classified':False,'original_question_completion':'unresolved',
        'original_proposal':copy.deepcopy(obligation['original_proposal']),
        'scope':'typed local model evidence; free-text completeness not inferred'}
