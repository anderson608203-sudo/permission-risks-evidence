"""Bounded source relationship: issued per-subject quota vs repeatable usage.

No names or labels. Only checked additive usage, a positive quantity, a matching
quota guard and a source-backed issuer assignment qualify. Asset issuance is
handled separately; arbitrary credit balances are not called lifecycle quotas.
"""
import copy
from .core import digest
from .m03_p_paths import key,op,lit,normalize,conditions_possible,walk

def analyze_quotas(bundle,lookup,program,requested,asset_models):
    from .m03_p_route import keys,selectors,value_type,effective_permission
    roots={m['balance_root'] for m in asset_models}|{m['supply_root'] for m in asset_models}
    grants=[];rows=[];alternatives=[]
    for fn,paths in program.items():
        for p in paths:
            if p['flow']=='reverted' or p['issues']:continue
            permission=effective_permission(p['guards'],lookup)
            if not permission:continue
            for w in p['writes']:
                ks=keys(w['path'])
                if w['path']['root'] in roots or len(ks)!=1:continue
                if ks[0].get('kind')!='parameter' or ks[0].get('type') not in ('address','address payable'):continue
                if w['value'].get('kind')!='parameter' or not str(value_type(w['path'],lookup)).startswith('uint'):continue
                grants.append({'function':fn,'source':w['source'],'quota':w['path'],'assigned_quantity':w['value'],'permission':permission})
    for fn,paths in program.items():
        for pi,p in enumerate(paths):
            if p['flow']=='reverted':continue
            for grant in grants:
                quota={**grant['quota'],'segments':[{'key':{'kind':'actual_sender'}}]}
                for effect in p['writes']:
                    target=effect['path'];v=normalize(effect['value'])
                    if target['root'] in roots or target['root']==quota['root'] or keys(target)!=[{'kind':'actual_sender'}]:continue
                    if v.get('kind')!='op' or v['op']!='+' or key(v['args'][0])!=key(target):continue
                    quantity=v['args'][1]
                    if quantity.get('kind')!='parameter' or not str(quantity.get('type','')).startswith('uint'):continue
                    if conditions_possible(p['guards'],op('>',quantity,lit(0))) or conditions_possible(p['guards'],op('>=',quota,quantity)):continue
                    updates=[w for w in p['writes'] if key(w['path'])==key(quota)]
                    after=updates[-1]['value'] if updates else quota
                    required=op('==',after,op('-',quota,quantity))
                    issues=copy.deepcopy(p['issues']);status='inconclusive';reason='quota_transition_not_resolved'
                    unknown=any(n.get('kind') in ('unknown','call_unresolved','choice','symbol','member','external_return_unresolved') for n in walk(p['guards']+[v,after]))
                    if not issues and not unknown:
                        if key(normalize(after))==key(normalize(op('-',quota,quantity))):
                            status='refuted_in_scope';reason='positive_usage_decrements_matching_subject_quota'
                        elif key(normalize(after))==key(quota):
                            changed={w['path']['root'] for w in p['writes']}
                            guard_roots={s['root'] for g in p['guards'] for s in selectors(g)}
                            if not changed & guard_roots:
                                status='supported';reason='positive_usage_leaves_issued_quota_and_action_guards_unchanged'
                            else:reason='other_action_guard_changes_prevent_quota_repetition_inference'
                    name=lookup.nodes[target['root']]['name']
                    selected=not requested or any(x.get('rule')=='AC-04' and x.get('function')==fn and str((x.get('effect') or {}).get('object',x.get('effect_state',''))).split('.')[-1]==name for x in requested)
                    synthetic=bundle.get('material_origin','compiler_artifacts')!='compiler_artifacts'
                    row={'schema':'m03-p-result-v2','route':'P','rule':'AC-04','status':status,'reason':reason,'function':fn,'subject':'actual_sender',
                        'structure':'issued_subject_usage_quota','program_id':bundle['program_id'],'build_id':bundle['build_id'],'policy_scope':'inferred_policy',
                        'required_policy_candidate':required,'policy_basis':{'basis':'privileged_quota_assignment_guarded_positive_usage','grant':grant,'quota_before':quota,'quota_after':after,'quantity':quantity},
                        'effect':{'object':name,'selector':target,'value':effect['value'],'operator':effect['operator'],'source':effect['source']},
                        'path_index':pi,'conditions':p['guards'],'issues':issues,'execution_status':'not_run','solver_status':'not_called','no_execution_required':True,
                        'reportable':status=='supported' and not synthetic,'diagnostic_only':synthetic,'material_origin':bundle.get('material_origin','compiler_artifacts'),
                        'limitations':['conditional inferred consumable quota semantics from issuer/guard/additive usage relationship',
                            'repeated usage conditional on a positive issued quota and checked-arithmetic headroom; no deployed trace or universal reachability',
                            'other guard updates, nonlinear consumption, asset issuance and arbitrary protocols not covered'],
                        'coverage':'same subject, quota, additive usage and declared source path','not_a_safety_conclusion':True}
                    row['id']=digest({k:row[k] for k in ('program_id','build_id','rule','function','effect','conditions','policy_basis')})
                    if selected:rows.append(row)
                    if status=='refuted_in_scope':
                        alternatives.append({'function':fn,'path_index':pi,'reason':'holder_consumes_authorized_usage_quota','issuer_functions':[grant['function']],
                            'effect_sources':[w['source']['ast_id'] for w in updates],'quota_evidence':row['policy_basis'],
                            'decision':'issuer controls allocation; a holder can consume own issued quota without issuer identity'})
    return list({r['id']:r for r in rows}.values()),alternatives
