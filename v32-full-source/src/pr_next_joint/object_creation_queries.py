"""Whole-record creation from a source-bound AC-01 proposal.

Only a single uint256 mapping key, flat fixed-word fields and a source-proven
absence precondition are supported. No field name or expected result is used.
The plan executes deployment then the proposed creator, without first creating
the same object. Every observed member contributes to whole-object change.
"""
import copy
from .core import require,digest,ref,lit,obs,operator
from .source_paths import SourcePaths
from .source_observers import bind_getter
from .component_queries import frames,unique,constructor_authority,RULE_CHECKS
from .object_effect_queries import _parameter,_field,_family,_corroborated,_arguments,_parameter_type,_value
from .instances import descriptor
from .environment import environment
from .multi_service import PLAN_SCHEMA,validate_plan

def _negated_paths(condition):
    if condition.get('kind')=='op' and condition.get('op')=='!' and len(condition.get('args',[]))==1:
        child=condition['args'][0]
        if child.get('kind')=='storage_binding':yield child
    elif condition.get('kind')=='op' and condition.get('op')=='&&':
        for child in condition['args']:yield from _negated_paths(child)

def _relation(bundle,contract,static,candidate,policy,lookup):
    claim=policy['typed_relations']['object_effect'];effect=claim['effect']
    require(policy['kind']=='authority_effect' and policy['rule']=='AC-01','creation_rule_scope')
    require(policy.get('source') and any(p.get('program_id')==bundle['program_id'] and p.get('build_id')==bundle['build_id']
        and p.get('contract_file')==contract['file'] and p.get('contract_name')==contract['name'] and p.get('basis')
        for p in policy.get('applies_to',[])),'creation_policy_scope')
    require(claim['authorization']=={'kind':'sender_equals_state','state_ast_id':claim['authority_ast_id']},'creation_authorization_relation')
    frame=frames(static,candidate);require(frame['entry']['function']==claim['function'],'creation_function_identity')
    writes=[r for r in frame['relationships'] if r.get('operation')=='write' and r['path']['declaration']['ast_id']==effect['state_ast_id']]
    write=unique(writes,'creation_whole_write_not_unique');path=write['path']
    require(path['program_id']==bundle['program_id'] and path['build_id']==bundle['build_id']
        and path['instance_id']==contract['file']+':'+contract['name'],'creation_object_identity')
    require(write['operator']=='=' and len(path['segments'])==1 and 'key' in path['segments'][0]
            and write['value'].get('kind')=='record','creation_whole_record_assignment')
    _corroborated(write);key_id=_parameter(path['segments'][0]['key'])
    require(_parameter_type(frame,key_id)=='uint256','creation_key_type')
    members=write['value']['fields'];field_ids=[_field(f) for f in members]
    require(len(field_ids)==len(set(field_ids)) and set(field_ids)==set(effect['field_ast_ids']),'creation_all_fields_required')
    authority=constructor_authority(lookup,claim['authority_ast_id'])
    absences=[]
    for guard in frame['guards']:
        for absent in _negated_paths(guard['condition']):
            if _family(absent)!=_family(path) or len(absent['segments'])!=2:continue
            if _parameter(absent['segments'][0]['key'])!=key_id:continue
            fid=_field(absent['segments'][1]);values=[f['value'] for f in members if _field(f)==fid]
            if values==[{'kind':'literal','value':True}]:absences.append(absent)
    absence=unique(absences,'creation_absence_guard_unresolved')
    return {'kind':'authority_effect_object_creation','rule':'AC-01','frame':frame,'effect':write,
        'members':members,'key_parameter':key_id,'absence':absence,'authority':authority,
        'association':{'policy':ref(policy),'typed_claim':claim},'critical_unresolved':[]}

def prepare_creation_queries(bundle,contract,static,policy,settings):
    require(all(static['input'][k]==bundle[k] for k in ('program_id','build_id')),'static_program_identity')
    require(not contract['constructor_types'],'constructor_arguments_unresolved')
    require(settings.get('mode','concrete')=='concrete','creation_concrete_only')
    claim=policy['typed_relations']['object_effect'];lookup=SourcePaths(bundle,contract)
    prepared,leads,cases=[],[],[]
    for record in static['alias_cases']:
        case=copy.deepcopy(record['case']);cases.append(case)
        if case['status']!='applicable':continue
        for candidate in record['candidates']:
            if candidate['entry']['function']!=claim['function']:continue
            try:
                relation=_relation(bundle,contract,static,candidate,policy,lookup)
                addresses={k:v['address'] for k,v in case['mapping'].items()};subject=claim['subject']
                require(subject in addresses,'creation_subject_not_declared');sender=addresses[subject]
                deployer=settings['deployment_address_basis']['sender'];require(deployer in addresses.values(),'creation_deployer_not_declared')
                key=settings.get('object_key',1);require(type(key) is int and 0<=key<2**256,'creation_key_range')
                values={relation['key_parameter']:str(key)};bindings={}
                for member in relation['members']:
                    fid=_field(member);path=copy.deepcopy(relation['effect']['path']);path['segments'].append({'field':fid})
                    observed=bind_getter(lookup,path,[str(key)]);bindings[str(fid)]=observed
                    val=member['value']
                    if val.get('kind')=='parameter':
                        pid=_parameter(val);require(pid!=relation['key_parameter'],'creation_key_value_alias')
                        require(_parameter_type(relation['frame'],pid)==observed['abi_type'],'creation_value_type')
                        encoded=_value(observed['abi_type'],settings.get('object_initial_value',1))
                        require(pid not in values or values[pid]==encoded,'creation_conflicting_argument')
                        values[pid]=encoded
                    else:require(val.get('kind')=='literal','creation_value_expression_unsupported')
                args=_arguments(relation['frame'],values)
                absence=bind_getter(lookup,relation['absence'],[str(key)]);require(absence['type']=='Bool','creation_absence_bool')
                authority=bind_getter(lookup,{'kind':'storage','root':claim['authority_ast_id'],'segments':[]},[])
                require(authority['type']=='Address160','creation_authority_type')
                program=descriptor(bundle,contract);pid=digest(program);iid=contract['file']+':'+contract['name']
                plan={'schema':PLAN_SCHEMA,'id':digest({'candidate':candidate['id'],'policy':policy,'alias':case['id'],'settings':settings,'shape':'whole_object_creation'}),
                    'programs':{pid:program},'instances':{iid:{'program_id':pid,'target':settings['deployment_address_basis']['target']}},
                    'accounts':sorted(set(addresses.values())),'environment':environment(settings['block_number'],settings['timestamp']),
                    'transactions':[],'observers':[]}
                for fn,arguments,caller in [('constructor',[],deployer),(claim['function'],args,sender)]:
                    plan['transactions'].append({**plan['instances'][iid],'instance_id':iid,'sender':caller,'function':fn,
                        'arguments':arguments,'environment':plan['environment'],'value':0,'gas':12000000})
                observers={'authority':authority,'object_absent_field':absence,**{'effect_'+fid:b for fid,b in bindings.items()}}
                for oid,binding in observers.items():
                    plan['observers'].append({**plan['instances'][iid],'instance_id':iid,'id':oid,'caller':deployer,**binding['observer_fields']})
                allowed=operator('eq','Bool',lit('Address160',sender),obs('authority.1','Address160'))
                changes=[operator('ne','Bool',obs('effect_'+fid+'.2',b['type']),obs('effect_'+fid+'.1',b['type'])) for fid,b in bindings.items()]
                require(changes,'creation_no_effect_observers');changed=changes[0] if len(changes)==1 else operator('or','Bool',*changes)
                premise=operator('and','Bool',obs('tx1.success','Bool'),
                    operator('eq','Bool',obs('authority.1','Address160'),lit('Address160',deployer)),
                    operator('not','Bool',obs('object_absent_field.1','Bool')))
                query={'rule':'AC-01','query_form':'EXISTS_VIOLATION','premise':premise,
                    'expression':operator('and','Bool',operator('not','Bool',allowed),obs('tx2.success','Bool'),changed),
                    'policy_allowed':allowed,'effect_expression':changed,'required_rule_checks':RULE_CHECKS['AC-01'],
                    'applicability':'applicable','policy_kind':'authority_effect','actual_actor_address':sender,'object_key':str(key),
                    'proposal_subject':subject,'effect_scope':'whole_record','effect_field_ast_ids':list(claim['effect']['field_ast_ids']),
                    'bound_authorization':copy.deepcopy(claim['authorization'])}
                validate_plan(plan)
                prepared.append({'id':plan['id'],'input_id':bundle.get('id',contract['name']),'candidate_ref':ref(candidate),
                    'static_ref':ref(static),'alias_case':case,'scenario':'proposed_subject_whole_object_creation',
                    'source_relation':relation,'policy':copy.deepcopy(policy),'policy_scope':'inferred_policy' if policy.get('inferred') else 'explicit_or_approved',
                    'program_id':bundle['program_id'],'build_id':bundle['build_id'],'plan':plan,'query':query,'mode':'concrete',
                    'unresolved':[],'unresolved_critical':False,'scope':'one source-bound whole-record creation trajectory; other functions and inputs remain uncovered',
                    'component_only':True,'LLM_called':False,'control_only':False,'purpose':'risk_candidate','object_observer_bindings':observers})
            except (ValueError,KeyError,IndexError,TypeError) as error:
                leads.append({'candidate_ref':ref(candidate),'case_id':case['id'],'entry':candidate['entry'],'status':'unresolved',
                    'reason':str(error),'execution_status':'not_executed'})
    require(len(prepared)*2<=32,'per_target_plan_cap_including_replay')
    return {'prepared':prepared,'leads':leads,'alias_cases':cases,'static_ref':ref(static),
        'program_id':bundle['program_id'],'build_id':bundle['build_id'],'rule_family':['AC-01'] if prepared else []}
