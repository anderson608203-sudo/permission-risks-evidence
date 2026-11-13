"""Conditional source models for issued time intervals and epoch snapshots.

Discover relationships from typed writes, ordering guards and controlled epoch
updates. No fixed names or external labels. This extends P hypotheses only;
it does not establish deployment reachability or replay transactions.
"""
import copy
from .core import digest
from .m03_p_paths import key,lit,op,walk,normalize,conditions_possible
from .m03_p_lifecycle import leaves

def analyze_validity(bundle,lookup,program,requested):
    from .m03_p_route import selectors,keys,fields,value_type,effective_permission,contains_sender,relocate
    issues=[];models=[];rows=[]
    for fn,paths in program.items():
        for pi,path in enumerate(paths):
            if path['flow']=='reverted' or path['issues']:continue
            managers=effective_permission(path['guards'],lookup)
            if not managers:continue
            for record in path['writes']:
                if record['value'].get('kind')!='record' or not keys(record['path']):continue
                assignments=list(leaves(record))
                numeric=[w for w in assignments if str(value_type(w['path'],lookup)).startswith('uint')]
                timestamp={'kind':'environment','field':'timestamp'}
                for expiry in numeric:
                    endpoint=expiry['value']
                    if endpoint.get('kind')=='parameter' and not conditions_possible(path['guards'],op('>',endpoint,timestamp)):
                        models.append({'kind':'issued_future_expiry','record':record['path'],'expiry':expiry['path'],'function':fn,'path_index':pi,
                            'source':record['source'],'management_permissions':managers,'issuance_condition':op('>',endpoint,timestamp)})
                for low in numeric:
                    for high in numeric:
                        if low is high or any(w['value'].get('kind')!='parameter' for w in (low,high)):continue
                        order=op('<',low['value'],high['value'])
                        # An explicit order relation establishes the two endpoints;
                        # two arbitrary integers or field names do not.
                        if conditions_possible(path['guards'],order):continue
                        models.append({'kind':'issued_time_interval','record':record['path'],'lower':low['path'],'upper':high['path'],
                            'function':fn,'path_index':pi,'source':record['source'],'management_permissions':managers,'ordering':order})
                for snapshot in numeric:
                    clock=snapshot['value']
                    if clock.get('kind')!='storage' or clock.get('segments') or not str(value_type(clock,lookup)).startswith('uint'):continue
                    for transition,paths2 in program.items():
                        for path2 in paths2:
                            if path2['flow']=='reverted' or path2['issues']:continue
                            perms=effective_permission(path2['guards'],lookup)
                            if not set(map(key,managers))&set(map(key,perms)):continue
                            for advance in path2['writes']:
                                v=normalize(advance['value'])
                                if key(advance['path'])!=key(clock) or v.get('kind')!='op' or v['op']!='+':continue
                                a,b=v['args']
                                if key(a)!=key(clock) or b.get('kind')!='literal' or type(b.get('value')) is not int or b['value']<=0:continue
                                models.append({'kind':'issued_epoch_snapshot','record':record['path'],'snapshot':snapshot['path'],'current_epoch':clock,
                                    'function':fn,'path_index':pi,'source':record['source'],'management_permissions':managers,
                                    'transition':{'function':transition,'source':advance['source'],'value':v},
                                    'transition_scope':'checked positive epoch increment, conditional on no overflow and successful authorized call'})
    for fn,paths in program.items():
        for pi,path in enumerate(paths):
            if path['flow']=='reverted':continue
            observed=list({key(s):s for g in path['guards'] for s in selectors(g) if keys(s) and fields(s) and contains_sender(s)}.values())
            for model in models:
                for credential in observed:
                    if credential['root']!=model['record']['root']:continue
                    try:
                        if model['kind']=='issued_time_interval':
                            lower=relocate(model['lower'],model['record'],credential);upper=relocate(model['upper'],model['record'],credential)
                            # At least one endpoint must actually be consumed by
                            # a timestamp condition; arbitrary records excluded.
                            relevant=[g for g in path['guards'] if any(n.get('kind')=='environment' and n.get('field')=='timestamp' for n in walk(g))]
                            if not any(key(s) in (key(lower),key(upper)) for g in relevant for s in selectors(g)):continue
                            timestamp={'kind':'environment','field':'timestamp'}
                            required=op('and',op('>=',timestamp,lower),op('<',timestamp,upper))
                            preconditions=[op('<',lower,upper)]
                        elif model['kind']=='issued_future_expiry':
                            expiry=relocate(model['expiry'],model['record'],credential)
                            required=op('<',{'kind':'environment','field':'timestamp'},expiry);preconditions=[]
                        else:
                            snapshot=relocate(model['snapshot'],model['record'],credential)
                            required=op('==',snapshot,model['current_epoch']);preconditions=[]
                    except ValueError:continue
                    condition=normalize(required);local_issues=copy.deepcopy(path['issues'])
                    unknown=any(n.get('kind') in ('unknown','call_unresolved','choice','symbol','member') for x in path['guards']+[condition] for n in walk(x))
                    status='inconclusive';reason='credential_validity_path_unresolved'
                    if not local_issues and not unknown:
                        try:
                            status='supported' if conditions_possible(path['guards']+preconditions,condition) else 'refuted_in_scope'
                            reason='issued_validity_condition_not_enforced' if status=='supported' else 'action_path_enforces_issued_validity'
                        except ValueError as error:local_issues.append({'reason':str(error)})
                    for write in path['writes']:
                        if write['path']['root']==credential['root']:continue
                        if model['kind']=='issued_epoch_snapshot' and write['path']['root']==model['current_epoch']['root']:continue
                        if key(write['path'])==key(write['value']):continue
                        name=lookup.nodes[write['path']['root']]['name']
                        matches=[p for p in requested if p.get('rule')=='AC-04' and p.get('function')==fn and str((p.get('effect') or {}).get('object',p.get('effect_state',''))).split('.')[-1]==name]
                        if requested and not matches:continue
                        row_status=status;row_reason=reason
                        if any(n.get('kind') in ('unknown','call_unresolved','choice','symbol') for n in walk(write['value'])):
                            row_status='inconclusive';row_reason='effect_value_unresolved'
                        synthetic=bundle.get('material_origin','compiler_artifacts')!='compiler_artifacts'
                        row={'schema':'m03-p-result-v2','route':'P','rule':'AC-04','status':row_status,'reason':row_reason,'function':fn,'subject':'actual_sender',
                            'structure':'credential_validity','program_id':bundle['program_id'],'build_id':bundle['build_id'],'policy_scope':'inferred_policy',
                            'required_policy_candidate':condition,'policy_basis':{'basis':model['kind'],'model':model,'credential':credential,'validity_assumptions':preconditions},
                            'effect':{'object':name,'selector':write['path'],'value':write['value'],'operator':write['operator'],'source':write['source']},
                            'path_index':pi,'conditions':path['guards'],'issues':local_issues,'execution_status':'not_run','solver_status':'not_called','no_execution_required':True,
                            'reportable':row_status=='supported' and not synthetic,'diagnostic_only':synthetic,'material_origin':bundle.get('material_origin','compiler_artifacts'),
                            'source_remarks':[p.get('unresolved',[]) for p in matches],
                            'limitations':['validity policy inferred from issued future expiry, ordered time endpoints or controlled epoch snapshot/update',
                                'conditional source path/pre-state; no deployment reachability, clock progression or transaction execution proof',
                                'arithmetic constraints retained as assumptions; quotas and arbitrary lifecycle protocols not covered'],
                            'coverage':'declared credential, source-backed validity relationship and action path','not_a_safety_conclusion':True}
                        row['id']=digest({k:row[k] for k in ('program_id','build_id','rule','function','effect','conditions','required_policy_candidate','policy_basis')});rows.append(row)
    return list({r['id']:r for r in rows}.values()),issues
