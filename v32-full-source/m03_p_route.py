"""Shared P consumer for sourced, conditional AC hypotheses (R26).

 No name matching, execution, RPC, expected labels or predetermined verdicts.
Finite source-path checks are deliberately not whole-program reachability proofs.
"""
import copy,json
from pathlib import Path
from .core import require,digest
from .m03_p_resource_relations import project_policy
from .m03_p_policy_context import peer_phase_conflict,managed_target_check
from .m03_p_paths import Paths,clean,key,walk,op,lit,normalize,dnf,conditions_possible


def keys(path):return [s['key'] for s in path.get('segments',[]) if 'key' in s]
def fields(path):return [s['field'] for s in path.get('segments',[]) if 'field' in s]
def selectors(expr):return [n for n in walk(expr) if n.get('kind')=='storage']


def value_type(path,lookup):
    typ=lookup.nodes.get(path['root'],{}).get('typeName',{})
    for seg in path.get('segments',[]):
        if seg.get('length'):return 'uint256'
        typ=(typ.get('valueType',{}) if typ.get('nodeType')=='Mapping' else typ.get('baseType',{})) if 'key' in seg else lookup.nodes.get(seg['field'],{}).get('typeName',{})
    from .m11_language import scalar_type
    return scalar_type(typ.get('typeDescriptions',{}).get('typeString') or typ.get('name'),lookup,typ)


def contains_sender(v):return any(x.get('kind')=='actual_sender' for x in walk(v))


def permission_atoms(expr,lookup,allow_parameter=False,_normalized=False):
    """Recognize semantic predicates; never infer a policy from a variable name."""
    e=expr if _normalized else normalize(expr)
    from .m22_record_roles import numeric_atom
    if numeric_atom(e,lookup):return [e]
    if e.get('kind')=='op' and e['op']=='==':
        for a,b in (e['args'],e['args'][::-1]):
            eligible=a.get('kind')=='actual_sender' or allow_parameter and a.get('kind')=='parameter' and a.get('type')=='address'
            if eligible and b.get('kind')=='storage' and value_type(b,lookup) in ('address','address payable'):
                return [e]
    if e.get('kind')=='storage' and value_type(e,lookup)=='bool':
        if contains_sender(e) or allow_parameter and any(x.get('kind')=='parameter' and x.get('type')=='address' for x in keys(e)):
            return [e]
    if e.get('kind')=='op' and e['op'] in ('and','&&','or','||'):
        return [a for x in e['args'] for a in permission_atoms(x,lookup,allow_parameter,_normalized=True)]
    return []


def effective_permission(guards,lookup):
    # Cache by content within one compiled target, never by mutable object id.
    # Returning a copy preserves isolation from downstream candidate edits.
    signature=key(guards)
    cache=lookup.__dict__.setdefault('_effective_permission_cache',{})
    if signature in cache:return copy.deepcopy(cache[signature])
    normalized_guards=[normalize(g) for g in guards]
    def formula(e,within_alternative=False):
        if permission_atoms(e,lookup,_normalized=True) and not (e.get('kind')=='op' and e['op'] in ('and','&&','or','||')):return e
        if e.get('kind')=='op' and e['op'] in ('and','&&','or','||'):
            parts=[formula(a,e['op'] in ('or','||')) for a in e['args']]
            if e['op'] in ('or','||') and any(a is None for a in parts):return None
            parts=[a for a in parts if a is not None]
            # Conditions qualifying a permission alternative (role==X AND
            # sponsor) are part of that permission, not disposable business
            # preconditions. Keep the complete branch inside a disjunction.
            if within_alternative and e['op'] in ('and','&&') and parts:return e
            if parts:return op(e['op'],*parts)
        return None
    atoms=[formula(g) for g in normalized_guards];atoms=[a for a in atoms if a is not None]
    # A mention in one OR branch is not an effective guard for the full path.
    result=[]
    for a in atoms:
        if not conditions_possible(guards,a):result.append(a)
    result=list({key(x):x for x in result}.values())
    if len(cache)>=512:cache.pop(next(iter(cache)))
    cache[signature]=copy.deepcopy(result)
    return result


def delegation_conditions(guards,required,lookup):
    """A visible caller-to-credential relation limits every related risk claim.

    It is evidence of a possible legitimate alternative, not proof of delegation.
    Do not suppress only AC-03 while reporting the same relation as AC-01.
    Unrelated address keys do not qualify.
    """
    roots={s['root'] for s in selectors(required)}
    credentials=set()
    for g in guards:
        for atom in permission_atoms(g,lookup,True):
            if contains_sender(atom):continue
            if not any(s['root'] in roots for s in selectors(atom)):continue
            credentials.update(key(x) for x in walk(atom) if x.get('kind')=='parameter' and x.get('type') in ('address','address payable'))
    return [s for g in guards for s in selectors(g) if value_type(s,lookup)=='bool' and contains_sender(s)
            and any(key(x) in credentials for x in walk(keys(s)))]


def structure(policy,lookup):
    ss=selectors(policy)
    if any(value_type(s,lookup)=='bool' for s in ss):return 'role_membership'
    if any(keys(s) for s in ss):return 'per_object_owner'
    return 'global_address'


def relocate(policy,source_path,target_path):
    if source_path['root']!=target_path['root']:raise ValueError('P_RESOURCE_ROOT_MISMATCH')
    a,b=keys(source_path),keys(target_path)
    if len(a)!=len(b):raise ValueError('P_RESOURCE_KEY_ARITY')
    mapping={}
    for left,right in zip(a,b):
        if left.get('kind')=='parameter':
            if left.get('type')!=right.get('type') and right.get('kind')=='parameter':raise ValueError('P_RESOURCE_KEY_TYPE')
            if left['id'] in mapping and mapping[left['id']]!=right:raise ValueError('P_KEY_BINDING_CONFLICT')
            mapping[left['id']]=right
        elif key(left)!=key(right):raise ValueError('P_KEY_IDENTITY_UNRESOLVED')
    def sub(v):
        if isinstance(v,dict):
            if v.get('kind')=='parameter':
                if v['id'] not in mapping:raise ValueError('P_POLICY_PARAMETER_UNBOUND')
                return copy.deepcopy(mapping[v['id']])
            return {k:sub(x) for k,x in v.items()}
        return [sub(x) for x in v] if isinstance(v,list) else v
    return sub(policy)


def state_overlap(a,b):
    if a['root']!=b['root'] or key(a.get('instance'))!=key(b.get('instance')):return False
    # For authority classification, keys describe independent members of a family.
    af,bf=fields(a),fields(b)
    return not af or not bf or af==bf


def load_profile():
    p=Path(__file__).resolve().parents[2]/'configs/method_evidence.r1.json'
    cfg=json.loads(p.read_text(encoding='utf-8'))
    require(cfg['approval']=='PR_NEXT_METHOD_REQUIREMENTS_AMENDMENT_20261022_R1','P_PROFILE_APPROVAL')
    return cfg


def analyze_program(bundle,contract,native,proposals=None,project_description=None,path_facts=None,analysis_scope="joint"):
    require(all(bundle[k]==native[k] for k in ('program_id','build_id')),'P_PROGRAM_IDENTITY')
    require(bundle.get('native_ir',{}).get('sha256')==digest(native),'P_NATIVE_CONTENT_IDENTITY')
    from .task_scope import rules
    active=rules(analysis_scope)
    cfg=load_profile()
    if path_facts is not None:
        from .m05_mechanism_core import MechanismPaths
        lookup=MechanismPaths(bundle,contract,cfg['P']['max_source_paths'])
    else:lookup=Paths(bundle,contract,max_paths=cfg['P']['max_source_paths'])
    lookup.analysis_scope=analysis_scope
    program={};failures=[];lookup.effect_scope_inventory={}
    from .source_entry_identity import entry_functions
    for f in entry_functions(lookup):
        signature=f['signature']
        try:
            node=lookup.function(signature)
            from .source_entry_identity import function_mutability
            # Source-checked read-only entrypoints have no committed sensitive effect in
            # AC/FCR scope. Declarations alone are insufficient on legacy compilers.
            # Their bodies remain available when called by a
            # sensitive entry, so dependent return/guard semantics are retained.
            body_nodes=list(walk((node or {}).get("body",{})))
            may_execute_effect=any(n.get("nodeType") in ("Assignment","FunctionCall","InlineAssembly","NewExpression","EmitStatement")
                or n.get("nodeType")=="UnaryOperation" and n.get("operator") in ("++","--","delete") for n in body_nodes)
            readonly=bool(node and ("generated_getter" in node or function_mutability(node) in ("view","pure") and not may_execute_effect))
            lookup.effect_scope_inventory[signature]={"entry_readonly":readonly,"strategy":"source_readonly_no_committed_effect" if readonly else "bounded_effect_and_guard_paths",
                 "internal_dependencies_preserved":True}
            program[signature]=[] if readonly and analysis_scope in ("AC","FCR") else lookup.run(signature)
        except Exception as ex:
            failures.append({'function':signature,'reason':type(ex).__name__+':'+str(ex)})
    # Per-invocation facts only. Capture before later candidate consumers can
    # enrich paths; this sidecar never becomes a serialized analysis result.
    if path_facts is not None:
        path_facts.update(lookup=lookup,paths=copy.deepcopy(program),failures=copy.deepcopy(failures))
    from .m10_applicability import routing_records,route_for
    lookup.routing_records=routing_records(program)
    pool=[];authority=[]
    for fn,paths in program.items():
        for source_pi,path in enumerate(paths):
            if path['flow']=='reverted' or path['issues']:continue
            for g in path['guards']:
                authority.extend(s for a in permission_atoms(g,lookup,True) for s in selectors(a))
            for a in effective_permission(path['guards'],lookup):
                for w in path['writes']:
                    if not route_for(lookup,fn,a,w['path']):
                        pool.append({'function':fn,'policy':a,'write':w,'source':path['entry_source'],'guards':path['guards'],'path_index':source_pi,'path':path})
    rows=[];uncovered=[]
    for fn,paths in program.items():
        for pi,path in enumerate(paths):
            if path['flow']=='reverted':continue
            uncovered.extend({'function':fn,'path_index':pi,**copy.deepcopy(issue)} for issue in path['issues'])
            uncovered.extend({'function':fn,'path_index':pi,**copy.deepcopy(issue)} for issue in path.get('bounded_read_call_limits',[]))
    requested=proposals or []
    if isinstance(requested,dict):requested=[requested]
    for p in requested:
        reference=str((p.get('effect') or {}).get('object',p.get('effect_state','')))
        require('.' not in reference or reference.split('.')[0]==contract['name'],'P_EFFECT_QUALIFIER_MISMATCH')
        for field in ('program_id','build_id'):
            require(p.get(field,bundle[field])==bundle[field],'P_PROPOSAL_IDENTITY_MISMATCH')
        if p.get('source_sha256'):
            hashes={f.get('source_anchor',{}).get('sha256') for f in bundle['functions']}
            require(p['source_sha256'] in hashes,'P_PROPOSAL_SOURCE_MISMATCH')
    from .m03_p_lifecycle import analyze_lifecycle,managed_credential_alternative
    lifecycle_all,lifecycle_all_gaps=analyze_lifecycle(bundle,lookup,program,[]) if analysis_scope!="FCR" else ([],[])
    from .m03_p_assets import analyze_assets,ordinary_asset_alternative
    asset_rows,asset_gaps,asset_alternatives,asset_models=analyze_assets(bundle,contract,requested,cfg['P']['max_source_paths'],lookup=lookup,program=program) if analysis_scope!='AC' else ([],[],[],[])
    if analysis_scope=='AC':
        from .m03_p_assets import asset_models as shared_asset_models
        from .m04_asset_math import proportional_models
        asset_models=shared_asset_models(lookup,program)+proportional_models(lookup,program)
    from .m04_policy_relations import handoffs,handoff_alternative,record_credential_alternative,initialized_policy,alternate_authority_scope
    handoff_models=handoffs(program,lookup) if analysis_scope!="FCR" else []
    from .m04_handoff_graph import discover as discover_handoff,alternative as handoff_phase_alternative,cleanup as handoff_cleanup
    handoff_phases=discover_handoff(lookup,program) if analysis_scope!="FCR" else []
    from .m04_quota_lifecycle import analyze_quotas
    quota_rows,quota_alternatives=analyze_quotas(bundle,lookup,program,requested,asset_models) if analysis_scope!="FCR" else ([],[])
    asset_alternatives.extend(quota_alternatives)
    from .m04_credential_relations import discover_relations
    relation_tasks,relation_gaps=discover_relations(lookup,program) if analysis_scope!="FCR" else ({},[])
    uncovered.extend(relation_gaps)
    policy_alternatives=[]
    for fn,paths in (program.items() if analysis_scope!="FCR" else []):
        for pi,path in enumerate(paths):
            # No reverted path provides a committed effect.
            if path['flow']=='reverted':continue
            for wi,write in enumerate(path['writes']):
                target=write['path'];decl=lookup.nodes[target['root']]
                prop_matches=[p for p in requested if p.get('function')==fn and str((p.get('effect') or {}).get('object',p.get('effect_state',''))).split('.')[-1]==decl['name']]
                if requested and not prop_matches:continue
                if prop_matches:
                    prop_matches=[p for p in prop_matches if (p.get('effect') or {}).get('field') is None or
                        any(lookup.nodes.get(fid,{}).get('name')==(p.get('effect') or {}).get('field') for fid in fields(target))]
                    if not prop_matches:continue
                if key(normalize(target))==key(normalize(write['value'])):continue
                cleanup=handoff_cleanup(write,fn,handoff_phases)
                if cleanup:
                    policy_alternatives.append({'function':fn,'effect':target,'reason':'nomination_cleanup_is_checked_with_authority_transfer','model':cleanup})
                    continue
                transfer=next((h for h in handoff_phases if fn==h['accept_function'] and write['source']==h['accept_source']),None)
                if transfer:
                    policy_alternatives.append({'function':fn,'effect':target,'reason':'authority_transfer_checked_against_current_nominee_not_old_authority','model':transfer})
                    continue
                hypotheses=[]
                for peer in pool:
                    try:
                        from .m21_policy import source_projection_limit
                        conflict=handoff_phase_alternative(peer,write,fn,handoff_phases) or handoff_alternative(peer,write,fn,handoff_models) or source_projection_limit(peer,write,path,fn,lookup)
                        if conflict:
                            policy_alternatives.append({**conflict,'function':fn,'effect':target});continue
                        policy,relations=project_policy(peer,write,fn)
                        policy,initialization=initialized_policy(policy,write,path,lookup)
                        if initialization:policy_alternatives.append({**initialization,'function':fn,'effect':target})
                        if policy is None:continue
                        hypotheses.append({'required':policy,'basis':'same_resource_guarded_operation' if fn!=peer['function'] else 'observed_guard',
                            'origin_function':peer['function'],'origin_source':peer['source'],'origin_path_index':peer['path_index'],**({'resource_relations':relations} if relations else {})})
                    except ValueError:pass
                # A caller-indexed authorization family supplies a source-based
                # self-governance hypothesis for direct writes to that authority.
                is_authority=any(state_overlap(target,s) for s in authority)
                if is_authority and not hypotheses and target.get('segments')==[] and value_type(target,lookup) in ('address','address payable'):
                    hypotheses.append({'required':op('==',{'kind':'actual_sender'},target),'basis':'state_controls_authorization; management assumed self-governed','origin_function':None})
                # A credential chosen by the caller must be bound to the sender
                # or to a visible delegation condition; do not compare arbitrary AST IDs.
                mismatches=[]
                for g in path['guards']:
                    for a in permission_atoms(g,lookup,True):
                        if contains_sender(a):continue
                        if route_for(lookup,fn,a,write['path']):continue
                        address_keys=[x for x in walk(a) if x.get('kind')=='parameter' and x.get('type')=='address']
                        if not address_keys:continue
                        target_check=managed_target_check(a,write,path['guards'],lookup)
                        if target_check:
                            policy_alternatives.append({**target_check,'function':fn,'effect':target});continue
                        def sender_sub(v):
                            if isinstance(v,dict):
                                if v.get('kind')=='parameter' and v.get('type')=='address':return {'kind':'actual_sender'}
                                return {k:sender_sub(x) for k,x in v.items()}
                            return [sender_sub(x) for x in v] if isinstance(v,list) else v
                        mismatches.append({'required':sender_sub(a),'observed':a,'basis':'caller_selected_authorization_subject',
                            'origin_function':fn,'origin_source':path['entry_source']})
                hypotheses=list({(key(h['required']),h.get('origin_function'),h.get('basis')):h for h in hypotheses}.values())
                alternatives=[];retained=[]
                for h in hypotheses:
                    alternative=managed_credential_alternative(h,write,fn,lifecycle_all) or ordinary_asset_alternative(h,write,fn,pi,asset_alternatives)
                    if alternative:alternatives.append(alternative)
                    else:retained.append(h)
                policy_alternatives.extend(alternatives)
                hypotheses=retained
                tasks=[('AC-01',h) for h in hypotheses]
                if is_authority:tasks += [('AC-02',h) for h in hypotheses]
                tasks += [('AC-03',h) for h in mismatches]
                tasks += relation_tasks.get((fn,write['source']['ast_id'],key(path['guards'])),[])
                # Object-key mismatches use a source-backed required policy
                # relocated to the actual affected object, preserving instance.
                for h in hypotheses:
                    expected=selectors(h['required'])
                    if any(s['root']==t['root'] and key(s)!=key(t) for g in path['guards'] for a in permission_atoms(g,lookup,True) for s in selectors(a) for t in expected):
                        tasks.append(('AC-03',{**h,'basis':'authorization_resource_selector_mismatch'}))
                if prop_matches:
                    allowed={p.get('rule') for p in prop_matches};tasks=[x for x in tasks if x[0] in allowed]
                if not tasks:
                    uncovered.append({'function':fn,'source':write['source'],'reason':'no_supported_permission_hypothesis','effect':target});continue
                for rule,h in tasks:
                    status='inconclusive';reason='source_path_or_condition_not_lowered'
                    condition=normalize(h['required'])
                    issues=copy.deepcopy(path['issues'])
                    alternate_scope=alternate_authority_scope(h,path['guards'],lookup) if not is_authority else None
                    if alternate_scope and h.get('basis')!='observed_guard':issues.append(alternate_scope)
                    unknown=any(x.get('kind') in ('unknown','call_unresolved','choice','symbol','member','external_return_unresolved','tuple','array') for v in path['guards']+[condition] for x in walk(v))
                    # An explicit public/alternative branch may be intended.
                    # Preserve it rather than forcing a narrower peer policy.
                    for g in path['guards']:
                        for node in walk(g):
                            if node.get('kind')=='op' and node['op'] in ('or','||') and permission_atoms(node,lookup) and not effective_permission([node],lookup):
                                issues.append({'reason':'visible_alternative_authorization_needs_policy_scope','condition':node})
                    for selected in delegation_conditions(path['guards'],condition,lookup):
                        issues.append({'reason':'visible_delegation_relation_needs_policy_scope','condition':selected})
                    if not issues and not unknown:
                        try:
                            status='supported' if conditions_possible(path['guards'],condition) else 'refuted_in_scope'
                            reason='conditional_permission_violation_path' if status=='supported' else 'path_conditions_imply_required_permission'
                        except ValueError as ex:issues.append({'reason':str(ex)})
                    # Values from unknown calls cannot establish a sensitive effect.
                    if any(x.get('kind') in ('unknown','call_unresolved') for x in walk(write['value'])):
                        status='inconclusive';reason='effect_value_unresolved'
                    synthetic=bundle.get('material_origin','compiler_artifacts')!='compiler_artifacts'
                    row={'schema':'m03-p-result-v2','route':'P','rule':rule,'status':status,'reason':reason,
                        'function':fn,'subject':'actual_sender','structure':h.get('structure_override') or structure(condition,lookup),
                        'program_id':bundle['program_id'],'build_id':bundle['build_id'],
                        'policy_scope':'inferred_policy','required_policy_candidate':condition,'policy_basis':h,
                        'effect':{'object':decl['name'],'selector':target,'value':write['value'],'operator':write['operator'],'source':write['source']},
                        'path_index':pi,'conditions':path['guards'],'issues':issues,
                        'execution_status':'not_run','solver_status':'not_called','no_execution_required':True,
                        'reportable':status=='supported' and not synthetic,
                        'diagnostic_only':synthetic,'material_origin':bundle.get('material_origin','compiler_artifacts'),
                        'source_remarks':[p.get('unresolved',[]) for p in prop_matches],
                        'limitations':['conditional on inferred policy and declared pre-state; business intention is not proven',
                            'bounded compiler-source paths, no deployment reachability or whole-program safety proof',
                            'arithmetic/environment path predicates are retained as assumptions, not SMT-proven satisfiable'],
                        'coverage':'this function/path/selector only','not_a_safety_conclusion':True}
                    if path.get('loop_scopes'):row['bounded_loop_scope']=path['loop_scopes']
                    if path.get('read_calls'):
                        row['read_call_summaries']=path['read_calls']
                    row['id']=digest({k:row[k] for k in ('program_id','build_id','rule','function','effect','conditions','required_policy_candidate')})
                    require(all(k in row for k in cfg['P']['required']),'P_RESULT_SCHEMA_MISSING_FIELD')
                    rows.append(row)
    from .m03_p_lifecycle import analyze_lifecycle
    lifecycle_rows,lifecycle_gaps=analyze_lifecycle(bundle,lookup,program,requested) if requested and analysis_scope!="FCR" else (lifecycle_all,lifecycle_all_gaps)
    from .m04_lifecycle_relations import analyze_validity
    validity_rows,validity_gaps=analyze_validity(bundle,lookup,program,requested) if analysis_scope!="FCR" else ([],[])
    from .m04_phase_lifecycle import analyze_phases
    phase_rows,phase_gaps=analyze_phases(bundle,lookup,program,requested) if analysis_scope!="FCR" else ([],[])
    lifecycle_rows.extend(validity_rows);lifecycle_rows.extend(quota_rows);lifecycle_rows.extend(phase_rows);lifecycle_gaps.extend(validity_gaps);lifecycle_gaps.extend(phase_gaps)
    rows.extend(lifecycle_rows);uncovered.extend(lifecycle_gaps)
    rows.extend(asset_rows);uncovered.extend(asset_gaps)
    covered={(r['function'],r['effect']['source'].get('ast_id')) for r in lifecycle_rows}
    uncovered=[g for g in uncovered if not (g.get('reason')=='no_supported_permission_hypothesis' and (g['function'],g['source'].get('ast_id')) in covered)]
    asset_covered={(r['function'],e['source']['ast_id']) for r in asset_rows for e in r['ledger_effects']+r['supply_effects']}
    uncovered=[g for g in uncovered if not (g.get('reason')=='no_supported_permission_hypothesis' and (g['function'],g['source'].get('ast_id')) in asset_covered)]
    from .m04_relation_graph import analyze_graph
    graph_rows,relation_graph=analyze_graph(bundle,lookup,program,requested,permission_queries=analysis_scope!="FCR")
    rows.extend(graph_rows)
    graph_covered={(r['function'],r['effect']['source'].get('ast_id')) for r in graph_rows}
    uncovered=[g for g in uncovered if not (g.get('reason')=='no_supported_permission_hypothesis' and (g['function'],g['source'].get('ast_id')) in graph_covered)]
    rows=[r for r in rows if r["rule"] in active]
    unique={r['id']:r for r in rows};rows=list(unique.values())
    findings=[r for r in rows if r['reportable']]
    grouped={}
    for r in findings:
        identity={'program':r['program_id'],'build':r['build_id'],'function':r['function'],
            'object':r['effect']['selector']['root'],'keys':keys(r['effect']['selector']),
            'policy':r['required_policy_candidate']}
        group=grouped.setdefault(digest(identity),{'claim_scope':identity,'rules':[],'evidence_rows':[]})
        if r['rule'] not in group['rules']:group['rules'].append(r['rule'])
        group['evidence_rows'].append(r['id'])
    implemented={r['id'] for r in cfg['rules'] if r.get('P')=='implemented_bounded'}
    require(all(r['rule'] in implemented for r in rows),'P_RULE_PROFILE_MISMATCH')
    report={'schema':cfg['report_schema'],'route':'P','analyzer':'source-conditions-ac-v4',
        'source_identity':{'program_id':bundle['program_id'],'build_id':bundle['build_id']},
        'profile_digest':digest(cfg),'results':rows,'reportable_findings':len(grouped),
        'counting_unit':'conditional operation/resource/policy group; multiple rules or fields are not independent vulnerabilities',
        'supported_effect_rows':len(findings),'finding_groups':list(grouped.values()),
        'uncovered':uncovered,'failures':failures,'functions_considered':list(program),
        'status':'partial_analyzed' if uncovered or failures or any(r['status']=='inconclusive' for r in rows) else 'analyzed' if rows else 'no_analyzable_candidates',
        'execution_status':'not_run','no_execution_required':True,'not_a_safety_conclusion':True,
        'normal_project_description':project_description,'description_semantically_interpreted':False,
        'proposal_origin':'saved_or_explicit_proposals_filtered_by_program' if requested else 'deterministic_source_relation_proposals',
        'rule_capabilities':cfg['rules']}
    report['relation_graph']=relation_graph
    if asset_models:report['asset_models']=asset_models
    if policy_alternatives:
        report['policy_alternatives']=policy_alternatives
    if lookup.read_calls.instances or lookup.read_calls.gaps:
        report['read_call_analysis']={'version':'compiler-read-call-summary-v1',
            'instances':list(lookup.read_calls.instances.values()),
            'unresolved':list({key(x):x for x in lookup.read_calls.gaps}.values()),
            'scope':'compiled direct-new or conditionally source-typed constructor-bound instances; scalar getters and read-only bodies; original entry effects',
            'callee_sender':'calling contract address; explicit actor arguments remain independently bound',
            'not_project_wide_contract_enumeration':True}
    return report


def analyze(bundle,contract,native,proposal,policy=None,project_description=None):
    # Compatibility wrapper: supplied legacy string policies cannot certify findings.
    return analyze_program(bundle,contract,native,[proposal],project_description)
