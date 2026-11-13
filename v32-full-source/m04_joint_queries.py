"""M3 consumes structured M2 policies, with identity/target/type binding."""
import copy
from .core import require,digest
from .m03_p_paths import walk,key,normalize,op
from .m03_p_route import structure,selectors,keys
from .m04_joint_context import SCHEMA,resolve
from .m04_joint_protocol import revised_model_condition

def bind(response,context,state):
    require(isinstance(response,dict) and response.get('schema')==SCHEMA,'JOINT_RESPONSE_SCHEMA')
    require(response.get('identity')==context['identity'],'JOINT_RESPONSE_IDENTITY')
    require(isinstance(response.get('proposals'),list) and isinstance(response.get('coverage'),list),'JOINT_RESPONSE_LISTS')
    queries=[];errors=[];seen=set();decisions=[]
    for pos,p in enumerate(response['proposals']):
        try:
            require(isinstance(p,dict),'JOINT_PROPOSAL_OBJECT')
            ident=p.get('id');require(isinstance(ident,str) and ident and ident not in seen,'JOINT_PROPOSAL_ID');seen.add(ident)
            if 'identity' in p:require(p['identity']==context['identity'],'JOINT_PROPOSAL_IDENTITY')
            for field in ('program_id','build_id'):
                if field in p:require(p[field]==context['identity'][field],'JOINT_PROPOSAL_IDENTITY:'+field)
            candidate=p.get('candidate_id');write=p.get('write_id');effect=p.get('effect_id')
            require(sum(bool(x) for x in (candidate,write,effect))==1,'JOINT_ONE_BINDING_REQUIRED')
            ref=candidate or write or effect;require(ref in state['bindings'],'JOINT_UNKNOWN_BINDING')
            item=state['bindings'][ref];lookup=state['lookups'][item['target']]
            rule=p.get('rule')
            from .task_scope import requested
            require(rule in requested(context),'JOINT_RULE_OUTSIDE_TASK')
            require(rule in ('AC-01','AC-02','AC-03','AC-04','FCR-MINT'),'JOINT_RULE_NOT_IMPLEMENTED')
            basis=p.get('basis');require(isinstance(basis,dict) and basis.get('kind') in ('program_relation','normal_description','combined'),'JOINT_POLICY_BASIS')
            require(isinstance(basis.get('source_ast_ids'),list) and basis['source_ast_ids'] and all(type(x) is int and x in lookup.nodes for x in basis['source_ast_ids']),'JOINT_BASIS_SOURCE_NOT_FOUND')
            require(isinstance(basis.get('explanation'),str) and basis['explanation'].strip() and isinstance(p.get('rationale'),str) and p['rationale'].strip(),'JOINT_BASIS_EXPLANATION')
            missing_description=(basis['kind']=='combined' and not context['normal_project_description'])
            require(basis['kind']!='normal_description' or bool(context['normal_project_description']),'JOINT_DESCRIPTION_NOT_PROVIDED')
            require(isinstance(p.get('alternatives'),list) and all(isinstance(x,str) for x in p['alternatives']),'JOINT_ALTERNATIVES_SHAPE')
            unresolved=p.get('unresolved');require(isinstance(unresolved,list),'JOINT_UNRESOLVED_SHAPE')
            require(all(isinstance(u,dict) and isinstance(u.get('text'),str) and u.get('impact') in ('query_blocking','policy_scope','unrelated') for u in unresolved),'JOINT_UNRESOLVED_IMPACT')
            if candidate:
                require('row' in item,'JOINT_CANDIDATE_ID_KIND')
                require(item['row']['rule']==rule,'JOINT_CANDIDATE_RULE_CHANGED')
            elif effect:require('sensitive_effect' in item and rule=='AC-01','JOINT_EFFECT_MODEL_NOT_BOUND')
            else:require('write' in item and rule in ('AC-01','AC-02','AC-03'),'JOINT_NEW_MODEL_NOT_BOUND')
            operation=(item['target'],item.get('function',item.get('row',{}).get('function')))
            for field,value in zip(('target','function'),operation):
                if field in p:require(p[field]==value,'JOINT_EXPLICIT_OPERATION_MISMATCH')
            decision=p.get('policy_decision',None if context.get('protocol_revision') else 'endorse')
            require(decision in ('endorse','revise','reject','uncertain'),'JOINT_POLICY_DECISION_REQUIRED')
            decisions.append({'proposal_id':ident,'binding_ref':ref,'target':item['target'],
                              'function':item.get('function',item.get('row',{}).get('function')),
                              'rule':rule,'decision':decision,'explanation':p['rationale']})
            if decision in ('reject','uncertain'):
                # A well-formed negative/uncertain review is not a protocol
                # failure or a proof that the operation is safe.
                continue
            if decision=='revise':require(p.get('required') is not None,'JOINT_REVISION_EXPRESSION_REQUIRED')
            if candidate:
                require('row' in item,'JOINT_CANDIDATE_ID_KIND');row=copy.deepcopy(item['row'])
                require(row['rule']==rule,'JOINT_CANDIDATE_RULE_CHANGED')
                if rule in ('AC-04','FCR-MINT') and p.get('required') is not None:
                    require(decision=='revise','JOINT_MODEL_REVISION_MUST_BE_EXPLICIT')
            elif effect:
                actual=copy.deepcopy(item['sensitive_effect']);path=item['path']
                row={'rule':rule,'function':item['function'],'path_index':item['path_index'],
                    'conditions':copy.deepcopy(path['guards']),'issues':copy.deepcopy(path['issues']),
                    'effect':{**actual,'object':actual['kind'],'selector':{'kind':'non_storage_effect','source_id':actual['source']['ast_id']}},
                    'required_policy_candidate':None,'policy_basis':{'basis':'llm_source_bound_sensitive_effect'},
                    'program_id':context['identity']['program_id'],'build_id':context['identity']['build_id']}
            else:
                require('write' in item and rule in ('AC-01','AC-02','AC-03'),'JOINT_NEW_MODEL_NOT_BOUND')
                w=item['write'];path=item['path'];selector=w['path']
                row={'rule':rule,'function':item['function'],'path_index':item['path_index'],
                     'conditions':copy.deepcopy(path['guards']),'issues':copy.deepcopy(path['issues']),
                     'effect':{'object':lookup.nodes[selector['root']]['name'],'selector':selector,'value':w['value'],'operator':w['operator'],'source':w['source']},
                     'required_policy_candidate':None,'policy_basis':{'basis':'llm_source_bound_policy'},
                     'program_id':context['identity']['program_id'],'build_id':context['identity']['build_id']}
            if p.get('required') is not None:
                condition=resolve(p['required'],state,item)
                original=copy.deepcopy(row['required_policy_candidate'])
                if rule in ('AC-04','FCR-MINT'):condition=revised_model_condition(row,condition)
                row['required_policy_candidate']=condition
                row['policy_revision']={'original':original,'accepted':copy.deepcopy(condition),
                                        'proposal_id':ident,'source_ast_ids':copy.deepcopy(basis['source_ast_ids'])}
            require(row['required_policy_candidate'] is not None,'JOINT_REQUIRED_PERMISSION_MISSING')
            if missing_description:
                # A mislabeled combined basis may still carry an independently
                # sourced condition. Retain the model claim and the missing
                # source; do not invent a normal specification or policy text.
                refs={n['ref'] for n in walk(p.get('required')) if isinstance(n.get('ref'),str)}
                require(bool(candidate) or bool(refs) and refs<=set(state['terms']),
                        'JOINT_MISSING_DESCRIPTION_NO_PROGRAM_RELATION')
                row['basis_assessment']={'declared_kind':'combined','effective_kind':'program_relation',
                    'normal_description_available':False,'resolved_expression_refs':sorted(refs),
                    'scope':'only source-bound inference evaluated; no business specification credited'}
            if rule in ('AC-01','AC-02','AC-03'):
                condition=row['required_policy_candidate']
                self_key_policy=any(key(normalize(condition))==key(normalize(op('==',{'kind':'actual_sender'},k))) for k in keys(row['effect']['selector']))
                require(bool(selectors(condition)) or self_key_policy,'JOINT_CONSTANT_OR_UNSOURCED_PERMISSION')
                # Parameters from another function cannot silently become fresh
                # symbols. Explicit, typed source substitution is necessary.
                available={n['id'] for path in state['paths'][(item['target'],row['function'])] for n in walk(path) if n.get('kind')=='parameter'}
                used={n['id'] for n in walk(condition) if n.get('kind')=='parameter'}
                require(used<=available,'JOINT_POLICY_PARAMETER_NOT_BOUND_TO_FUNCTION')
                bases=lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
                known_instances={key(s.get('instance')) for (tid,fn),paths in state['paths'].items() if tid==item['target'] for s in selectors(paths) if s.get('instance')}
                for selector in selectors(condition):
                    declaration=lookup.nodes.get(selector['root'],{})
                    require(declaration.get('stateVariable') is True,'JOINT_POLICY_STATE_DECLARATION')
                    if declaration.get('scope') not in bases:
                        require(bool(selector.get('instance')) and key(selector['instance']) in known_instances,'JOINT_POLICY_EXTERNAL_INSTANCE_UNBOUND')
                row['structure']='caller_indexed_resource' if self_key_policy else structure(condition,lookup)
                if rule=='AC-02' and not candidate:
                    root=row['effect']['selector']['root']
                    require(any(s['root']==root for (tid,fn),paths in state['paths'].items() if tid==item['target'] for path in paths for g in path['guards'] for s in selectors(g)), 'JOINT_AC02_STATE_NOT_CONSUMED_BY_GUARD')
                if rule=='AC-03' and not candidate:
                    required_roots={s['root'] for s in selectors(condition)}
                    require(any(s['root'] in required_roots for g in row['conditions'] for s in selectors(g)), 'JOINT_AC03_CHECKED_CREDENTIAL_RELATION_MISSING')
            # Provisional decisions are never transported as M4 results.
            for field in ('status','reason','reportable','solver','solver_status','id','project_row_id'):
                row.pop(field,None)
            row.update(target=item['target'],proposal_id=ident,binding_ref=ref,policy_scope='inferred_policy',
                       llm_policy_basis=copy.deepcopy(basis),llm_rationale=p['rationale'],alternatives=p['alternatives'],source_remarks=unresolved)
            row['query_requirements']=(['success_path','permission_policy','resource_effect']
                if rule in ('AC-01','AC-02','AC-03') else ['success_path','transition_or_accounting_model','resource_effect'])
            path=state['paths'].get((item['target'],row['function']),[])[row['path_index']]
            row['source_evaluation_terms']=copy.deepcopy(path.get('evaluated_terms',[]))
            row.setdefault('issues',[]).extend({'reason':x} for x in path.get('evaluation_gaps',[]))
            row['id']='q_'+digest(row);queries.append(row)
        except Exception as ex:errors.append({'proposal_index':pos,'proposal_id':p.get('id') if isinstance(p,dict) else None,'reason':str(ex),'original_proposal':copy.deepcopy(p),'rule':p.get('rule') if isinstance(p,dict) else None})
    expected={(t['id'],f['function']) for t in context['targets'] for f in t['functions']}
    covered={};coverage_errors=[]
    for c in response['coverage']:
        if not isinstance(c,dict):coverage_errors.append({'reason':'coverage_not_object'});continue
        pair=(c.get('target'),c.get('function'))
        if pair not in expected or pair in covered or c.get('disposition') not in ('proposed','no_risk_hypothesis','normal_review','not_applicable','unresolved') or not isinstance(c.get('explanation'),str) or not c['explanation'].strip():
            coverage_errors.append({'entry':c,'reason':'coverage_invalid_or_duplicate'});continue
        covered[pair]=c
    gaps=[{'target':t,'function':f,'reason':'M2_function_review_missing'} for t,f in sorted(expected-set(covered))]
    for pair,c in covered.items():
        has_query=any((q['target'],q['function'])==pair for q in queries)
        if not has_query:gaps.append({**c,'reason':'no_bound_formal_query; model review alone is not a no-risk proof'})
    return queries,{'proposal_binding_errors':errors,'policy_decisions':decisions,
                    'coverage_errors':coverage_errors,'function_reviews':list(covered.values()),'uncovered':gaps}
