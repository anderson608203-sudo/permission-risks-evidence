"""Bounded P analysis of administratively activated/deactivated credentials.

This is a source-derived transition hypothesis, not an executed transaction
sequence. No names, example identifiers, labels or externally supplied policy.
Checked unsigned affine credential counters are supported in the declared transition pair; timestamp and general version/cross-contract lifecycles are not.
"""
import copy
from .core import digest
from .m03_p_lifecycle_values import needs_counter_model,compose,rewrite
from .m03_p_paths import clean,key,walk,op,lit,normalize,conditions_possible


def leaves(write):
    value=write['value']
    if value.get('kind')=='record':
        for field in value['fields']:
            yield from leaves({**write,'path':{**write['path'],'segments':write['path']['segments']+[{'field':field['field']}]},'value':field['value']})
    else:yield write


def fold(value):
    """Only exact constant operations used by credential bit masks."""
    if isinstance(value,list):return [fold(x) for x in value]
    if not isinstance(value,dict):return value
    value={k:fold(v) for k,v in value.items()};value=normalize(value)
    if value.get('kind')=='op' and value['op'] in ('&','|','^') and len(value['args'])==2:
        a,b=value['args']
        if all(x.get('kind')=='literal' and type(x.get('value')) is int and x['value']>=0 for x in (a,b)):
            x,y=a['value'],b['value'];return lit({'&':x&y,'|':x|y,'^':x^y}[value['op']])
    return value


def same_record(a,b):
    from .m03_p_route import keys,fields
    return a['root']==b['root'] and key(a.get('instance'))==key(b.get('instance')) and key(keys(a))==key(keys(b)) and fields(a)[:-1]==fields(b)[:-1]


def managed_credential_alternative(hypothesis,write,function,lifecycle_rows):
    """A manager-created resource need not be manager-exclusive forever.

    Retain an explicit record when the same manager can issue/revoke a credential
    consumed by this action on the SAME object. Lifecycle analysis still checks
    missing validity; an unknown lifecycle or unrelated object grants no waiver.
    """
    from .m03_p_route import keys
    if hypothesis.get('basis')!='same_resource_guarded_operation':return None
    object_keys=keys(write['path'])
    if not object_keys:return None
    for row in lifecycle_rows:
        if row['function']!=function or row['status'] not in ('supported','refuted_in_scope'):continue
        if key(row['effect']['selector'])!=key(write['path']):continue
        basis=row['policy_basis'];credential=basis['credential']
        if key(credential.get('instance'))!=key(write['path'].get('instance')):continue
        if not all(key(k) in {key(c) for c in keys(credential)} for k in object_keys):continue
        if key(normalize(hypothesis['required'])) not in {key(normalize(p)) for p in basis['management_permissions']}:continue
        return {'reason':'manager_control_does_not_establish_manager_exclusive_action',
                'narrower_hypothesis':hypothesis,'credential':credential,
                'activation':basis['activation'],'deactivation':basis['deactivation'],
                'function':function,'effect':write['path'],'lifecycle_evidence_row':row['id'],
                'decision':'use_source_derived_credential_policy; missing validity remains reportable by lifecycle analysis'}
    return None


def analyze_lifecycle(bundle,lookup,program,requested):
    from .m03_p_route import keys,fields,selectors,value_type,effective_permission,contains_sender,relocate
    transitions=[];rows=[];gaps=[]
    for fn,paths in program.items():
        for pi,path in enumerate(paths):
            if path['flow']=='reverted' or path['issues']:continue
            permissions=effective_permission(path['guards'],lookup)
            if not permissions:continue
            writes=[w for item in path['writes'] for w in leaves(item)]
            for w in writes:
                if not keys(w['path']) or not fields(w['path']) or value_type(w['path'],lookup)!='bool':continue
                if w['value'] not in (lit(True),lit(False)):continue
                transitions.append({'function':fn,'path_index':pi,'source':path['entry_source'],'write':w,'writes':writes,'permissions':permissions,'guards':path['guards']})
    for fn,paths in program.items():
        for pi,path in enumerate(paths):
            if path['flow']=='reverted':continue
            # Bind lifecycle to the very credential record used by the action.
            observed=list({key(s):s for g in path['guards'] for s in selectors(g)
                           if keys(s) and fields(s) and contains_sender(s)}.values())
            for cred in observed:
                for disabled in (t for t in transitions if t['write']['value']==lit(False)):
                    d=disabled['write']['path']
                    if d['root']!=cred['root'] or fields(d)[:-1]!=fields(cred)[:-1]:continue
                    try:active=relocate(d,d,cred)
                    except ValueError:continue
                    for enabled in (t for t in transitions if t['write']['value']==lit(True)):
                        e=enabled['write']['path']
                        if e['root']!=d['root'] or fields(e)!=fields(d):continue
                        try:
                            if key(relocate(e,e,cred))!=key(active):continue
                            ep=[relocate(a,e,cred) for a in enabled['permissions']]
                            dp=[relocate(a,d,cred) for a in disabled['permissions']]
                        except ValueError:continue
                        if not set(map(key,ep))&set(map(key,dp)):continue
                        # Require an independently checked sibling field. A free
                        # boolean in an unrelated record does not establish policy.
                        siblings=[s for s in observed if same_record(s,active) and fields(s)!=fields(active)]
                        if not siblings:continue
                        post={};issues=copy.deepcopy(path['issues']);established=set()
                        valid_transition=True
                        for phase,t in [('activation',enabled),('deactivation',disabled)]:
                            for w in t['writes']:
                                if w['path']['root']!=active['root']:continue
                                try:
                                    selector=relocate(w['path'],t['write']['path'],cred)
                                    value=relocate(w['value'],t['write']['path'],cred)
                                except ValueError:
                                    issues.append({'reason':'transition_object_or_value_unbound','phase':phase,'source':w['source']});continue
                                if not same_record(selector,active):
                                    issues.append({'reason':'transition_other_key_alias_unresolved','phase':phase,'source':w['source']});continue
                                if w['operator']!='=':
                                    issues.append({'reason':'transition_nonassignment_not_lowered','source':w['source']});continue
                                post[key(selector)]=value
                                if phase=='activation':established.add(key(selector))
                            if post.get(key(active))!=lit(phase=='activation'):valid_transition=False
                        numeric=None
                        if needs_counter_model(enabled,disabled):
                            post,established,issues,valid_transition,numeric=compose(lookup,enabled,disabled,active,cred,path['issues'])
                        if not valid_transition:
                            if numeric:gaps.append({'function':fn,'source':path['entry_source'],'reason':'lifecycle_transition_pair_infeasible','credential':active})
                            continue
                        if not all(key(s) in established for s in siblings):
                            gaps.append({'function':fn,'source':path['entry_source'],'reason':'lifecycle_activation_credential_value_unbound','credential':active})
                            continue
                        def substitute(v):
                            if isinstance(v,dict):
                                if v.get('kind')=='storage' and key(v) in post:return copy.deepcopy(post[key(v)])
                                return {k:substitute(x) for k,x in v.items()}
                            return [substitute(x) for x in v] if isinstance(v,list) else v
                        guards=[fold(substitute(g)) for g in path['guards']]
                        if numeric:
                            guards=[rewrite(g,issues) for g in guards]+numeric['conditions']
                        for g in path['guards']:
                            for node in walk(g):
                                if node.get('kind')=='op' and node['op'] in ('||','or') and any(same_record(s,active) for s in selectors(node)):
                                    issues.append({'reason':'visible_alternative_to_lifecycle_needs_policy_scope','condition':node})
                        unknown=any(n.get('kind') in ('unknown','choice','call_unresolved','symbol','member','tuple','array') for g in guards for n in walk(g))
                        status='inconclusive';reason='lifecycle_transition_or_action_unresolved'
                        if not issues and not unknown:
                            try:
                                status='supported' if conditions_possible(guards) else 'refuted_in_scope'
                                reason='deactivated_credential_can_satisfy_action_path' if status=='supported' else 'deactivation_blocks_this_action_path'
                            except ValueError as ex:issues.append({'reason':str(ex)})
                        for write in path['writes']:
                            target=write['path'];decl=lookup.nodes[target['root']]
                            if target['root']==active['root'] or key(target)==key(write['value']):continue
                            matches=[p for p in requested if p.get('rule')=='AC-04' and p.get('function')==fn and str((p.get('effect') or {}).get('object',p.get('effect_state',''))).split('.')[-1]==decl['name']]
                            matches=[p for p in matches if (p.get('effect') or {}).get('field') is None or
                                     any(lookup.nodes.get(fid,{}).get('name')==(p.get('effect') or {}).get('field') for fid in fields(target))]
                            if requested and not matches:continue
                            row_status=status;row_reason=reason
                            if any(n.get('kind') in ('unknown','call_unresolved','choice') for n in walk(write['value'])):
                                row_status='inconclusive';row_reason='effect_value_unresolved'
                            synthetic=bundle.get('material_origin','compiler_artifacts')!='compiler_artifacts'
                            basis={'basis':'source_derived_credential_activation_deactivation','activation':{k:enabled[k] for k in ('function','path_index','source')},
                                   'deactivation':{k:disabled[k] for k in ('function','path_index','source')},'management_permissions':ep,
                                   'management_permission_context':'transition caller, separate from action actual_sender; successful authorized transition is a declared precondition',
                                   'credential':active,'post_deactivation_values':post,'action_conditions_after_deactivation':guards}
                            row={'schema':'m03-p-result-v2','route':'P','rule':'AC-04','status':row_status,'reason':row_reason,
                                 'function':fn,'subject':'actual_sender','structure':'role_membership','program_id':bundle['program_id'],'build_id':bundle['build_id'],
                                 'policy_scope':'inferred_policy','required_policy_candidate':active,'policy_basis':basis,
                                 'effect':{'object':decl['name'],'selector':target,'value':write['value'],'operator':write['operator'],'source':write['source']},
                                 'path_index':pi,'conditions':path['guards'],'issues':issues,'execution_status':'not_run','solver_status':'not_called',
                                 'no_execution_required':True,'reportable':row_status=='supported' and not synthetic,'diagnostic_only':synthetic,
                                 'material_origin':bundle.get('material_origin','compiler_artifacts'),'source_remarks':[p.get('unresolved',[]) for p in matches],
                                 'limitations':['inferred credential validity policy from privileged activation/deactivation and checked sibling fields',
                                                'conditional on successful authorized lifecycle transitions; deployment/prefix reachability not proven',
                                                'boolean record lifecycle only; expiry/version/cross-contract mechanisms not covered'],
                                 'coverage':'declared transition pair and action path only','not_a_safety_conclusion':True}
                            if numeric:
                                basis['numeric_transition_model']=numeric
                                row['limitations'][-1]='same-record boolean activation with checked unsigned affine counters; general expiry/stale-version protocols not covered'
                            row['id']=digest({k:row[k] for k in ('program_id','build_id','rule','function','effect','conditions','required_policy_candidate','policy_basis')})
                            rows.append(row)
    return list({r['id']:r for r in rows}.values()),list({key(g):g for g in gaps}.values())
