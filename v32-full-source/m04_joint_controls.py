"""Source-bound checks for M2-reviewed controls, and policy applicability.

Model reviews are consumed, not treated as safety proofs. No verdict is copied
from M1 candidates. Unknown function reviews and unsupported semantics remain.
"""
import copy,re
from .core import digest
from .m03_p_paths import key,normalize,op
from .m03_p_route import keys,selectors

def cleaned(row):
    q=copy.deepcopy(row)
    for k in ('status','reason','reportable','solver','solver_status','id','project_row_id'):q.pop(k,None)
    return q

def add_controls(queries,coverage,context,state):
    added=[];reviews={(c['target'],c['function']):c for c in coverage['function_reviews']}
    existing={(q['target'],q['function'],q['rule'],key(q['effect']['selector']),q['path_index']) for q in queries}
    for ref,item in state['bindings'].items():
        if 'row' not in item:continue
        decision=next((d['decision'] for d in coverage.get('policy_decisions',[]) if d['binding_ref']==ref and d['rule']==item['row']['rule']),None)
        if decision in ('uncertain','revise'):continue
        row=item['row'];pair=(item['target'],row['function']);review=reviews.get(pair)
        if not review or review['disposition']=='unresolved':continue
        # The normal asset accounting question is distinct from privileged
        # transfer/burn proposals, which remain outside this stage's scope.
        if row['rule'] not in ('AC-01','AC-02','AC-03','AC-04','FCR-MINT'):continue
        scope=(*pair,row['rule'],key(row['effect']['selector']),row['path_index'])
        if scope in existing:continue
        basis=row.get('policy_basis',{})
        ordinary=(basis.get('ordinary_route') or basis.get('native_value_equal_backing')
                  or basis.get('fresh_native_backing') or basis.get('conserved_conversion')
                  or (basis.get('ledger_delta')=={} and basis.get('supply_delta')=={}))
        negative_only=decision=='reject' or review['disposition'] in ('no_risk_hypothesis','normal_review','not_applicable')
        if not ordinary and not negative_only:continue # A normal review cannot manufacture an alarm.
        q=cleaned(row);q.update(target=item['target'],binding_ref=ref,proposal_id=None,policy_scope='program_derived_asset_model',
            query_origin='M2_reviewed_normal_control',llm_function_review=copy.deepcopy(review),
            llm_policy_basis={'kind':'program_relation','source_ast_ids':[row['effect']['source']['ast_id']],
                             'explanation':'M2 function review plus matched source accounting; independently test net entitlement creation'},
            llm_rationale=review['explanation'],alternatives=[],source_remarks=[])
        q['negative_control_only']=negative_only
        q['source_evaluation_terms']=copy.deepcopy(state['paths'][(item['target'],row['function'])][row['path_index']].get('evaluated_terms',[]))
        q['id']='q_'+digest(q);queries.append(q);existing.add(scope);added.append(q['id'])
    for ref,item in state['bindings'].items():
        if 'write' not in item:continue
        pair=(item['target'],item['function']);review=reviews.get(pair)
        if not review or review['disposition'] not in ('no_risk_hypothesis','normal_review'):continue
        if any(q.get('binding_ref')==ref for q in queries):continue
        w=item['write'];ks=keys(w['path'])
        # A personal storage slot selected by the actual caller is a sourced
        # subject/object equality, not an invented global administrator.
        if not ks or ks[-1]!={'kind':'actual_sender'} or item['path']['issues']:continue
        if any(s['root']==w['path']['root'] for (tid,fn),paths in state['paths'].items() if tid==item['target']
               for path in paths for g in path['guards'] for s in selectors(g)):continue
        lookup=state['lookups'][item['target']]
        q={'rule':'AC-01','target':item['target'],'function':item['function'],'path_index':item['path_index'],
           'conditions':copy.deepcopy(item['path']['guards']),'issues':[],
           'effect':{'object':lookup.nodes[w['path']['root']]['name'],'selector':copy.deepcopy(w['path']),
                     'value':copy.deepcopy(w['value']),'operator':w['operator'],'source':w['source']},
           'required_policy_candidate':op('==',{'kind':'actual_sender'},ks[-1]),
           'policy_basis':{'basis':'source_caller_indexed_personal_effect'},'structure':'caller_indexed_resource',
           'program_id':context['identity']['program_id'],'build_id':context['identity']['build_id'],
           'binding_ref':ref,'proposal_id':None,'policy_scope':'inferred_policy','query_origin':'M2_reviewed_normal_control',
           'llm_function_review':copy.deepcopy(review),'llm_rationale':review['explanation'],
           'llm_policy_basis':{'kind':'program_relation','source_ast_ids':[w['source']['ast_id']],
                             'explanation':'M2 normal-control review and actual caller-selected storage key'},
           'source_remarks':[],'alternatives':[]}
        q['id']='q_'+digest(q);queries.append(q);added.append(q['id'])
    retained=[];not_applicable=[]
    for gap in coverage['uncovered']:
        pair=(gap.get('target'),gap.get('function'))
        if gap.get('reason','').startswith('no_bound_formal_query'):
            if any(q.get('binding_ref')==ref for q in queries):continue
            paths=state['paths'].get(pair,[])
            lookup=state['lookups'].get(pair[0])
            try:node=lookup.function(pair[1])
            except Exception:node={}
            if paths and not any(p['writes'] or p['issues'] for p in paths) and node.get('stateMutability') in ('view','pure'):
                not_applicable.append({**gap,'reason':'M2_reviewed_source_read_only_no_state_effect_query','formal_safety_claim':False});continue
        retained.append(gap)
    coverage.update(uncovered=retained,derived_control_queries=added,non_state_effect_reviews=not_applicable)
    return queries,coverage

def assess_policy(q,context):
    if q['rule'] not in ('AC-01','AC-02','AC-03'):return None
    target=next(t for t in context['targets'] if t['id']==q['target'])
    for alternative in target['visible_policy_alternatives']:
        if alternative.get('function')!=q['function'] or alternative.get('path_index')!=q['path_index']:continue
        narrower=alternative.get('narrower_hypothesis',{}).get('required')
        if not narrower or key(normalize(narrower))!=key(normalize(q['required_policy_candidate'])):continue
        effect=alternative.get('effect')
        if effect and key(effect)!=key(q['effect']['selector']):continue
        if not (alternative.get('quota_evidence') or alternative.get('allowance_evidence')):continue
        return {'decision':'conditional_alternative_not_established_as_required_policy',
                'reason':'issuer_exclusivity_conflicts_with_source_bound_holder_consumption',
                'source_alternative':copy.deepcopy(alternative),'original_model_hypothesis_retained':True}
    return None

def assess_remarks(q):
    assessments=[];blocking=False
    for r in q.get('source_remarks',[]):
        outcome=r['impact'];reason='model_assessment_retained'
        dependency=r.get('dependency',{})
        if (outcome=='query_blocking' and isinstance(dependency,dict)
                and dependency.get('kind') in ('rejection_path','deployment_prefix')
                and dependency.get('target')==q['target'] and dependency.get('function')==q['function']
                and q['rule'] in ('AC-01','AC-02','AC-03') and not q.get('issues')
                and q.get('required_policy_candidate') is not None and q.get('effect')
                and q.get('query_requirements')==['success_path','permission_policy','resource_effect']):
            # A successful source-write query does not consume a rejection
            # model or claim deployment reachability. No prose or AST repair
            # is used to discharge an actual success-path/policy dependency.
            outcome='conditional_model_scope'
            reason='success_effect_model_only; rejection_history_and_deployment_prefix_not_claimed'
        asset=q.get('policy_basis',{}).get('asset_model',{})
        payment=asset.get('native_payment',{});source_id=payment.get('source',{}).get('ast_id')
        # Only an explicitly named downstream payout call already represented
        # by a conditional source entitlement can be outside issuance's model.
        ids={int(x) for x in re.findall(r'\bAST\s*(\d+)\b',r['text'],re.I)}
        if (outcome=='query_blocking' and q['rule']=='FCR-MINT' and ids=={source_id}
            and q['function']!=asset.get('redemption_function') and not q.get('issues')
            and payment.get('success',{}).get('kind')=='native_call_success'):
            outcome='conditional_entitlement_scope';reason='downstream_payout_not_executed; issuance_formula_does_not_assume_payout_occurred'
        assessments.append({'original':copy.deepcopy(r),'assessment':outcome,'reason':reason,
                            'query_requirements':copy.deepcopy(q.get('query_requirements',[]))})
        blocking|=outcome=='query_blocking'
    return assessments,blocking
