"""Consume bound M2 questions; separate source location from formal evidence."""
import copy
from .core import digest
from .m05_question_trace import evidence_state,trace
from .m05_asset_obligations import check as asset_check

def check(obligation,state):
    rule=obligation['rule']
    from .operation_scope import source_operation,exclusion
    lookup=state['lookups'][obligation['target']]
    proof=exclusion(rule,source_operation(lookup,obligation['function']),obligation['identity'],obligation['target'],obligation['function'])
    if proof:
        return [{'id':'p_'+digest([obligation['id'],proof]),'obligation_id':obligation['id'],
                 'rule':rule,'target':obligation['target'],'function':obligation['function'],
                 'status':'refuted_in_scope','reportable':False,'program_analysis_certificate':proof,
                 'formal':{'solver_called':False,'query':'not_required_P','premise':'source_checked','status':'refuted_in_scope','reason':proof['reason']},
                 'source_model':{'kind':'source_necessary_condition_absent'},
                 'assumptions':['resolved supplied operation; does not exclude a different detector family']}],[]
    if rule in ('AC-01','AC-02','AC-03','AC-04','FCR-MINT'):
        route=obligation.get('legacy_bridge',{})
        return [],[{'reason':'original_source_question_retained; ordinary_query_links_separate',
            'bridge_status':route.get('status','not_routed'),'query_ids':route.get('query_ids',[]),
            'bridge_gaps':copy.deepcopy(route.get('gaps',[]))}]
    if rule in ('FCR-PAUSE','FCR-FREEZE'):
        from .m05_control_obligations import check as consume
    elif rule=='AC-05':
        from .m05_credential_obligations import check as consume
    else:consume=asset_check
    return consume(obligation,state)

def assess_remarks(obligation,rows,gaps):
    """Keep natural-language gaps separate from a completed bounded theorem.

    No text substring is accepted as a semantic proof. The model certificate
    describes exactly what was checked; unclassified decisive concerns remain
    report limitations rather than silently disappearing.
    """
    return [{'text':r['text'],'declared_impact':r['impact'],
             'assessment':'retained_scope_limitation' if r['impact']!='query_blocking' else 'not_automatically_discharged',
             'associated_model_refs':[row['id'] for row in rows],
             'dependency_relation':'unclassified',
             'remaining_model_gaps':copy.deepcopy(gaps)}
            for r in obligation['original_proposal']['unresolved']]

def claim_certificate(obligation,row):
    """A bounded theorem is narrower than the original natural-language claim.

    Do not pretend to resolve arbitrary prose. Preserve it and the original
    claim as unresolved; publish only the independently constructed conditional
    model claim with its source/model/formula identities and assumptions.
    """
    formal=row.get('formal',{});model=row.get('source_model',{})
    bound=obligation.get('source_binding_status')=='source_anchors_bound'
    encoded=(formal.get('solver_called') is True and formal.get('premise')=='sat'
             and formal.get('query') in ('sat','unsat') and bool(formal.get('semantic_formula_sha256')))
    grounded=bool(model.get('graph') or row.get('asset_relation'))
    operation=row.get('common_operation') or {};consumption=operation.get('consumption') or {}
    trace_bound=bool(operation.get('phase')=='consumed_by_risk_formula'
        and operation.get('identity')==obligation.get('identity')
        and operation.get('proposal_sha256')==obligation['proposal_sha256']
        and operation.get('target')==row.get('target') and operation.get('function')==row.get('function')
        and operation.get('model_sha256')==formal.get('semantic_formula_sha256')==digest(model)
        and consumption.get('formula_sha256')==formal.get('formula_sha256') and consumption.get('fields'))
    eligible=(bound and encoded and grounded and trace_bound and evidence_state(row)['model_conclusive']
        and bool(row.get('assumptions')) and not model.get('unresolved_dependencies'))
    return {'source_proposal_sha256':obligation['proposal_sha256'],
            'model_sha256':formal.get('semantic_formula_sha256'),
            'formula_sha256':formal.get('formula_sha256'),
            'claim_kind':'conditional_source_model', 'eligible':bool(eligible),
            'source_binding':bound,'semantic_encoding_checked':encoded,'relation_model_present':grounded,
            'exact_consumption_trace_bound':trace_bound,
            'exact_dependencies':{'question_refs':model.get('question_refs',[]),'model_kind':model.get('kind'),
                'resource':operation.get('resource'),'holder':operation.get('holder'),
                'consumed_input_fields':consumption.get('fields',[]),'consumed_inputs_sha256':consumption.get('inputs_sha256'),
                'policy_relation_origin':model.get('validity_relation_origin'),
                'local_unresolved_dependencies':model.get('unresolved_dependencies',[])},
            'original_natural_language_claim':'not_independently_discharged',
            'assumptions':copy.deepcopy(row.get('assumptions',[])),
            'scope':'exact modeled operation, holder/resource and source conditions only; no inference that all original concerns were resolved'}

def evaluate(obligations,state,real):
    result=copy.deepcopy(obligations);all_checks=[]
    for ob in result['source_obligations']:
        support=[r['id'] for r in all_checks if r.get('reportable') and (state.get('analysis_scope')=='AC' or r['rule']==ob['rule'])]
        if real and support and ob.get('original_proposal',{}).get('review_kind')=='risk_hypothesis':
            ob.update(status='classification_search_stopped',reportable=False,checks=[],model_gaps=[],
                formal={'solver_called':False,'query':'not_encoded','reason':'target_classification_already_supported'},
                classification_stop={'support_ids':support,'not_an_exhaustive_vulnerability_search':True})
            ob['question_trace']=trace(ob,[],[])
            continue
        try:rows,gaps=check(ob,state)
        except Exception as ex:
            # A consumer failure is not a negative result and must not erase
            # checks of unrelated, independently bound obligations.
            rows=[];gaps=[{'reason':'consumer_exception:'+type(ex).__name__+':'+str(ex),
                          'function':ob['function'],'rule':ob['rule'],
                          'internal_work_accounting_incomplete':True}]
            ob.update(status='inconclusive',reportable=False,
                      formal={'solver_called':None,'status':'inconclusive',
                              'query':'not_completed','premise':'unknown','accounting_incomplete':True,
                              'reason':'consumer_exception; partial internal work not claimed'})
        assessments=assess_remarks(ob,rows,gaps)
        ob['remark_assessments']=assessments
        ob['checks']=[r['id'] for r in rows];ob['model_gaps']=gaps
        if not rows and not ob.get('formal',{}).get('accounting_incomplete'):
            ob['formal']={'solver_called':False,'query':'not_encoded','premise':'not_checked',
                'status':'inconclusive','reason':'no_source_model_constructed',
                'blocking_reasons':[g.get('reason','unclassified_model_gap') for g in gaps]}
        if rows:
            ob['semantic_binding_status']='source_model_constructed_for_declared_paths'
            ob['status']='supported' if any(r['status']=='supported' for r in rows) else 'inconclusive' if gaps or any(r['status']=='inconclusive' for r in rows) else 'refuted_in_scope'
            ob['formal']={'solver_called':any(r['formal']['solver_called'] for r in rows),
                          'status':ob['status'],'reason':'see_individual_source_obligation_checks',
                          'query':'mixed_see_checks','premise':'see_checks'}
            ob['reportable']=bool(real and ob['status']=='supported')
        for r in rows:
            r['evidence_state']=evidence_state(r)
            certificate=claim_certificate(ob,r)
            r['remark_assessments']=copy.deepcopy(assessments)
            r['claim_scope']='conditional result of the declared source model; original M2 concerns retained'
            r['source_basis_assessment']=copy.deepcopy(ob.get('basis_assessment',{}))
            r['unresolved_claim_dependencies']=any(a['assessment']=='not_automatically_discharged' for a in assessments)
            r['conditional_claim_certificate']=certificate
            r['original_claim_reportable']=False
            r['reportable']=bool(real and r['status']=='supported' and certificate['eligible'])
            r['reportable_claim']='conditional_source_model' if r['reportable'] else 'none'
            r['diagnostic_only']=not real;all_checks.append(r)
        ob['reportable']=any(r['reportable'] for r in rows)
        ob['question_trace']=trace(ob,rows,gaps)
        p=result['rule_stage_progress'][ob['rule']]
        p['formal_checks_called']+=sum(bool(r['formal']['solver_called']) for r in rows)
        p['supported']+=sum(r['status']=='supported' for r in rows)
        p['refuted_in_scope']+=sum(r['status']=='refuted_in_scope' for r in rows)
        if rows:p['not_encoded']-=1
        # A local check is evidence for its exact model, not completion of a rule.
        p['formal_attempted']=p.get('formal_attempted',0)+sum(r['evidence_state']['formal_attempted'] for r in rows)
        p['conclusive_models']=p.get('conclusive_models',0)+sum(r['evidence_state']['model_conclusive'] for r in rows)
        p['inconclusive_models']=p.get('inconclusive_models',0)+sum(r['evidence_state']['formal_inconclusive'] for r in rows)
        p['work_accounting_unknown']=p.get('work_accounting_unknown',False) or any(g.get('internal_work_accounting_incomplete') for g in gaps)
        p['capability_demonstrated']=bool(p['conclusive_models'])
        p['progress_scope']='local constructed models only; not original question or rule completeness'
    result['source_obligation_checks']=all_checks
    result['formal_checks_called']=sum(bool(r['formal']['solver_called']) for r in all_checks)
    result['reportable_findings']=sum(r['reportable'] for r in all_checks)
    return result
