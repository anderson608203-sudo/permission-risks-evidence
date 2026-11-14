"""Source-backed risk prediction, scoped hard counterevidence and dependency output."""
import copy,re
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import walk,key
from pr_next_joint.frontend.storage import selectors,keys,value_type,selector_relation
from .contracts import VERSION,CATEGORIES
from .protocol import category_scope
from .request_scope import coverage_facts, observation_applies, compare_relevant, linked_controls



def evaluate(inv,q):
    from .property_model import compose
    inv.semantics.scope(q['current'])
    prop=q.get('property') or {}
    stamp=(q['version'],prop.get('id'),tuple(q['evidence']),bool(q.get('task_conflict')),
           q.get('retired_property_parent'),tuple(sorted(q.get('office_effects',{}).items())),
           tuple(q.get('effect_scope',())),len(q.get('observations',())),inv.semantics.rules.epoch)
    cached=q.get('_composed_snapshot')
    if not cached or cached[0]!=stamp:
        cached=(stamp,compose(inv,q,None));q['_composed_snapshot']=cached
    return cached[1]

def reading_scope(inv,blocked,assessments=None):
    from .coverage import obligation_scope
    assessments=assessments or {qid:evaluate(inv,q) for qid,q in inv.issues.items()}
    return obligation_scope(inv,assessments,blocked)



def build(inv):
    findings={};records=[];suppressed=[];decisive_records=[];blocked_categories=set();assessments={}
    for qid,q in sorted(inv.issues.items()):
        assessment=evaluate(inv,q);assessments[qid]=assessment;item=q['current'];records.append({'id':qid,'version':q['version'],
            'current':copy.deepcopy(item),'history':copy.deepcopy(q['history']),'binding':q['binding'],
            'distinguishing_plan':copy.deepcopy(q.get('plan')),'claim_source_scope':copy.deepcopy(q['claim_source_scope']),
            'task_conflict':q.get('task_conflict',False),'semantic_task_review':copy.deepcopy(q.get('task_review')),
            'compiled_property':copy.deepcopy(q.get('property')),'semantic_answers':copy.deepcopy(q.get('semantic_answers',[])),
            'assessment_result':assessment,'evidence_refs':q['evidence'],'revision_evidence':q['revision_evidence'],
            'scoped_observations':copy.deepcopy(q.get('observations',[])),
            'source_observation_reuse':copy.deepcopy(q.get('source_decisions',[]))})
        decision=assessment['scope']['decision']
        if decision['status'] in ('risk','normal','excluded') and not q.get('task_conflict'):
            decisive_records.append(qid)
        mapping=assessment['scope'].get('comparison_alignment',{})
        if not assessment['reportable']:
            if item['assessment']=='risk':suppressed.append({'issue':qid,'reasons':assessment['reasons']})
            continue
        oid=assessment['root'];o=inv.f.operations[oid]
        location=copy.deepcopy(o['source']);anchor=q['binding'].get('core_anchor') or inv.catalog.name(oid);fine=False
        if anchor in inv.catalog.label_locations:location=copy.deepcopy(inv.catalog.label_locations[anchor]);fine=True
        else:
            m=re.fullmatch(r'(.+\.sol):(\d+)(?:[-:](\d+))?',anchor)
            if m and m[1] in inv.catalog.sources:
                chunks=inv.catalog.sources[m[1]]['content'].encode().splitlines(keepends=True);lo=int(m[2]);hi=int(m[3] or lo)
                start=sum(map(len,chunks[:lo-1]));end=sum(map(len,chunks[:hi]));location={'file':m[1],'start':start,'length':end-start};fine=True
        # Conservative source-root grouping. Do not equate different unlocated
        # business mechanisms merely because they share a variable/function.
        precise=assessment['scope'].get('decision',{}).get('locations',[])
        if len(precise)==1 and precise[0].get('start') is not None and not fine:
            location=copy.deepcopy(precise[0]);fine=location!=o['source']
        effective=assessment['scope']['decision']
        # One actual incumbent replacement has the same cause whether policy was
        # stated in an issue, supplied as a scoped seed, or independently inferred.
        scoped_role=effective['reason']=='source_role_reassignment' and effective.get('effects') and 'current_authority_required' in effective.get('meanings',())
        if scoped_role:
            cause=['incumbent_replacement',sorted(effective['effects']),item.get('phase'),item.get('scope'),item.get('assumptions') or []]
        else:
            cause=[assessment['scope'].get('claim_identity'),item.get('object'),item.get('actor'),
                   item.get('phase'),item.get('scope'),item.get('assumptions'),effective.get('effects',[])]
        identity=[inv.f.identity,assessment['category'],o['target'],location,cause]
        fid='finding_'+digest(identity)[:20]
        f=findings.setdefault(fid,{'id':fid,'category':assessment['category'],'target':o['target'],
            'root_location':location,'root_cause':{'operation':oid,'source_anchors':[location]},
            'operation':oid,'function':o['function'],'related_operations':q['binding']['operations'],
            'actor':item.get('actor'),'object':item.get('object'),'mechanism':assessment.get('composed_claim',item['claim']),
            'original_model_claim':item['claim'],'original_model_assessment':item['assessment'],
            'normal_explanation_considered':item.get('alternative'),'scope':assessment['scope'],
            'assumptions':item.get('assumptions',[]),'evidence_level':assessment.get('evidence_level','source_prediction'),
            'comparison_scope':mapping.get('status','main'),'formal_risk_query_required':False,'evidence_refs':[],'issue_ids':[]})
        f['evidence_refs']=sorted(set(f['evidence_refs']+q['evidence']));f['issue_ids'].append(qid)
    scope=reading_scope(inv,blocked_categories,assessments)
    blocked_categories={c for gap in scope['known_category_gaps'] for c in gap.get('affected_categories',[])}
    return {'method':VERSION,'program_identity':inv.f.identity,'task':inv.f.options.scope,'options':inv.f.options.record(),
        'implementation_sha256':inv.f.context['implementation_sha256'],
        'findings':list(findings.values()),'main_finding_ids':[k for k,v in findings.items() if v['comparison_scope']=='main'],
        'additional_finding_ids':[k for k,v in findings.items() if v['comparison_scope']=='additional'],
        'unresolved_mapping_ids':[k for k,v in findings.items() if v['comparison_scope']=='unresolved'],'inspection_records':records,
        'diagnostics':{'issues':inv.diagnostics,'unexecuted_actions':copy.deepcopy(inv.ready),
            'suppressed_source_predictions':suppressed,'program_gaps':copy.deepcopy(inv.f.gaps),
            'source_context_scope':inv.initial_manifest,'no_finding_is_not_contract_safety':True,
            'E1_not_formal_FREEZE':True},
        'model_analysis_available':inv.model_analysis_available,
        'prediction_basis_available':bool(findings or scope['negative_eligible_categories'] or decisive_records),
        'prediction_basis_issues':decisive_records,'unresolved_category_judgments':sorted(blocked_categories),
        'task_analysis':{'model_analysis_available':inv.model_analysis_available,'fixture_analysis_available':getattr(inv,'fixture_analysis_available',False),'usable_task_opinion':inv.usable_task_opinion,
            'empty_response_present':inv.explicit_empty_analysis,
            'explicit_empty_task_reading':bool(inv.explicit_empty_analysis and scope['whole_reading_eligible']),
            'model_declaration':inv.task_declaration,'reading_scope':scope,'local_judgment_not_global_safety':True,
            'unexecuted_actions':len(inv.ready),'task_conflicts':[qid for qid,q in inv.issues.items() if q.get('task_conflict')]},
        'model_reading_declarations_not_proof':inv.reading_declarations,
        'usage':{'attempts':copy.deepcopy(inv.session.attempts),**inv.session.accounting()},
        'provenance':{'refinement_decisions':copy.deepcopy(inv.refinements),'structural_references':{k:v['structural'] for k,v in inv.shared_reads.items() if v['result'] is not None},'shared_source_facts':{k:sorted(v['consumers']) for k,v in inv.shared_reads.items() if v['result'] is not None},'source_candidate_investigations':copy.deepcopy(getattr(inv,'candidate_trace',[])),'actions':copy.deepcopy(inv.actions),'revisions':copy.deepcopy(inv.updates),
            'evidence_labels':sorted(inv.evidence),'feedback_trace':copy.deepcopy(inv.feedback_trace),'cache_hits':inv.backend.cache_hits,
            'computation_reuse':copy.deepcopy(inv.backend.cache_stats),'model_call_decisions':copy.deepcopy(inv.call_decisions),
            'mechanism_attribution_not_a_new_detection_admission_gate':True},
        'prediction_frozen_before_gold':True,'scoring_performed':False,
        'risk_absence_statement':'No risk detected in the actual analyzed source scope; not proof of safety.'}

def evaluation_projection(report):
    """No Gold access, scoring or legacy query gate. Preserve positive source predictions."""
    cats=('AC',) if report['task']=='AC' else CATEGORIES[1:]
    found={f['category'] for f in report['findings'] if f.get('comparison_scope','main')=='main'}
    unknown=set(report.get('unresolved_category_judgments',[]))
    task=report.get('task_analysis',{});reading=task.get('reading_scope',{})
    # Archived reports retain their original projection; new reports carry prospective eligibility.
    if 'reading_scope' in task:
        eligible=set(reading['negative_eligible_categories'])
    else:
        eligible=set()
        unknown.update(set(cats) - found)
    obligations=reading.get('obligations',[])
    active=bool(report.get('model_analysis_available') or obligations or found or report.get('inspection_records'))
    if reading.get('schema') not in ('source-category-decision-r1','source-category-public-r1') and not obligations:eligible.clear()
    if report.get('method') in (VERSION,'permission-risks-semantic-propagation-r2','permission-risks-source-prediction-integration-r1','permission-risks-next-decision-only-r2'):
        states={c:'alarm' if c in found else 'not_run' if not active else
                'not_detected' if c in eligible and c not in unknown else 'unsupported' for c in cats}
    else:
        states={c:'alarm' if c in found else 'unsupported' if c in unknown else
                'not_detected' if c in reading.get('negative_eligible_categories',[]) else 'not_run' for c in cats}
    return {'predictions':states,
        'scope':report['diagnostics']['source_context_scope'],
        'coverage_basis':('Source opinions and actual scoped reading; optional refinement is independent.' if report.get('method') in (VERSION,'permission-risks-semantic-propagation-r2','permission-risks-source-prediction-integration-r1') else 'Finite source obligations, actual semantic/program completion and scoped residuals; delivery/declarations are records, not completion gates.'),
        'no_finding_does_not_prove_safety':True,'not_a_score':True,
        'enhancement_unfinished_does_not_erase_source_predictions':True}
