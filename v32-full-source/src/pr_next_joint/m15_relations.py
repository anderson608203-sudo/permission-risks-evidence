"""Source-bound role/stage/resource proposals shared by AC and FCR.
Labels and descriptions are never predicates. Source identities bind proposals;
program paths/certificates alone confirm their applicability.
"""
import copy
from .core import digest
from .m03_p_paths import key,walk,op
from .m03_p_route import selectors,keys,effective_permission,value_type
from .m05_relation_model_scope import source_term
from .m04_logic import Unsupported
from .m15_schema import FIELDS
SENDER={'kind':'actual_sender'}

def compile_scopes(context,relations,state):
    operations={x['id']:x for x in context['operations']};refs=context['references'];out={}
    for relation in relations['relations']:
        main=operations[relation['op_ref']];lookup=state['lookups'][main['target']]
        compiled={'relation_id':relation['id'],'target':main['target'],'function':main['function'],
                  'actors':[],'resources':[],'conditions':[],'links':copy.deepcopy(relation.get('operation_links',[])),
                  'rejections':[],'events':[],'structured':any(relation.get(f) for f in FIELDS)}
        def reject(field,row,reason):compiled['rejections'].append({'field':field,'proposal':copy.deepcopy(row),'reason':reason})
        from .m16_source_bindings import resolve,path_key
        def term(ref,oid,path,purpose=None):
            operation=operations[oid];node=lookup.nodes[refs[ref]['ast_id']]
            if not node.get('stateVariable') and node.get('id') not in operation['source_ast_ids']:
                raise ValueError('source_reference_not_in_operation')
            return resolve(node,lookup,operation['function'],path,purpose)
        actor_rows=relation.get('actor_bindings',[])
        if relation.get('subject_ref'):
            actor_rows=[*actor_rows,{'role':'unspecified','ref':relation['subject_ref'],'op_ref':relation['op_ref']}]
        for field,rows in [('actor',actor_rows),('resource',relation.get('resource_bindings',[])),('condition',relation.get('condition_bindings',[]))]:
            for row in rows:
                fn=operations[row['op_ref']]['function'];paths=state['paths'].get((main['target'],fn),[])
                if not paths:reject(field,row,'operation_has_no_source_paths')
                for pi,path in enumerate(paths):
                    if path['flow'] not in ('normal','returned'):continue
                    base={**copy.deepcopy(row),'function':fn,'path_indices':[pi],'path_guards':copy.deepcopy(path['guards']),'path_key':path_key(path)}
                    try:
                        if field=='actor':
                            value=term(row['ref'],row['op_ref'],path)
                            typ=value_type(value,lookup) if value.get('kind')=='storage' else value.get('type')
                            source_type=lookup.nodes[refs[row['ref']]['ast_id']].get('typeDescriptions',{}).get('typeString')
                            if typ not in ('address','address payable') and source_type not in ('address','address payable') and value.get('kind')!='actual_sender':raise ValueError('actor_not_address_term')
                            if row['role']=='caller' and value!=SENDER:raise ValueError('caller_not_actual_sender')
                            compiled['actors'].append({**base,'term':value,'status':'source_bound_role_proposal_not_authority_proof'})
                        elif field=='resource':
                            value=term(row['resource_ref'],row['op_ref'],path,'resource')
                            if value.get('kind')!='storage':raise ValueError('resource_not_exact_storage_selector')
                            holder=term(row['holder_ref'],row['op_ref'],path) if row.get('holder_ref') else None
                            bound_keys=[term(r,row['op_ref'],path) for r in row['key_refs']]
                            if bound_keys and key(keys(value))!=key(bound_keys):raise ValueError('resource_key_order_or_value_mismatch')
                            if holder is not None and (not keys(value) or key(holder)!=key(keys(value)[0])):raise ValueError('holder_not_first_source_storage_key')
                            quantity=term(row['quantity_ref'],row['op_ref'],path) if row.get('quantity_ref') else None
                            compiled['resources'].append({**base,'selector':value,'holder':holder,'quantity':quantity,'status':'source_bound_resource_proposal'})
                        else:
                            value=term(row['condition_ref'],row['op_ref'],path)
                            if not any(key(value)==key(g) for g in path['guards']):raise ValueError('condition_not_observed_in_declared_operation')
                            compiled['conditions'].append({**base,'term':value,'status':'source_observed_condition_not_universal_policy'})
                    except (ValueError,Unsupported) as e:
                        reject(field,row,str(e));compiled['rejections'][-1].update(function=fn,path_indices=[pi],path_guards=copy.deepcopy(path['guards']),path_key=path_key(path))
        out[relation['id']]=compiled
    return out

def selector_matches(actual,expected):
    # A declaration can describe its whole storage root. A selected field/key
    # cannot be widened back to a root or to a sibling field/holder.
    if actual.get('root')!=expected.get('root') or key(actual.get('instance'))!=key(expected.get('instance')):return False
    return not expected.get('segments') or key(actual.get('segments'))==key(expected.get('segments'))

def scoped_resources(compiled,fn,selector,pi=None,path=None):
    from .m16_source_bindings import rows_for
    rows=rows_for(compiled,'resources',fn,path,pi)
    specified=any(r['function']==fn for r in compiled['resources']) or any(r['field']=='resource' and r.get('function')==fn for r in compiled['rejections'])
    return not specified or any(selector_matches(selector,r['selector']) for r in rows)

def directed_stage_exclusion(compiled,fn,pi,path,write,required,origin_function,lookup):
    """Verified stage relationships precede cross-function key relocation."""
    # A verified directed handoff scopes only its particular nominated/accepted effect.
    from .m09_shared_policy import implies
    for link in compiled.get('verified_links',[]):
        if link['status']!='program_verified' or link['kind']!='nomination_acceptance':continue
        cert=link['certificate'];principal=None
        if fn==link['from_function'] and origin_function==link['to_function'] and any(n['function']==fn and n['path_index']==pi and n['source']==write['source'] for n in cert['nominations']) and key(write['path'])==key(cert['nominee']):principal=cert['nominee']
        elif fn==link['to_function'] and origin_function==link['from_function'] and pi==cert['path_index'] and write['source'] in cert['effect_sources']:principal=cert['owner']
        if principal is not None and {s['root'] for s in selectors(required)}=={principal['root']}:
            try:
                if implies(lookup,{'guards':[op('==',SENDER,principal)]},required):return 'verified_directed_handoff_has_distinct_stage_authority'
            except (Unsupported,ValueError):pass
    for link in compiled.get('verified_links',[]):
        if link['status']!='program_verified' or link['kind']!='authorization_use':continue
        cert=link['certificate']['use_certificate']
        if fn!=link['to_function'] or origin_function!=link['from_function'] or cert['path_index']!=pi:continue
        sources=cert['effect_sources']+[x['consumption']['source'] for x in cert['consent_sources'] if x.get('consumption')]
        if write['source'] in sources:return 'verified_grant_use_does_not_project_setter_policy'
    return None

def policy_allowed(compiled,fn,pi,path,write,required,origin_function,lookup,relation):
    """Restrict only the proposed M2 candidate; independent program checks stay."""
    # Explicitly scoped conditions must stay in their actual operation. A typed
    # phase edge is not permission to project the acceptance guard backwards.
    if relation.get('condition_bindings'):
        candidates=[r for r in compiled['conditions'] if key(r['term'])==key(required)]
        if not any(r['function']==fn and r['function']==origin_function and pi in r['path_indices'] for r in candidates):
            return False,'condition_belongs_to_another_operation_or_is_unconfirmed'
    # Bind this relationship's candidate to its stated, source-observed actor.
    # This does NOT refute an independent requirement for a second principal;
    # all program-origin candidates and their applicability checks remain.
    from .m09_shared_policy import implies
    for actor in compiled['actors']:
        value=actor['term']
        if relation['relation_kind'] not in ('controlled_by','checks_permission'):continue
        if pi not in actor.get('path_indices',[pi]) or actor['function']!=fn or actor['role'] not in ('governor','unspecified') or value.get('kind')!='storage' or value.get('segments'):continue
        if any(key(value)==key(v) for v in walk(required)):continue
        try:
            if implies(lookup,path,op('==',SENDER,value)):
                return False,'proposed_actor_does_not_support_different_peer_principal'
        except (Unsupported,ValueError):pass
    return True,None

def verify_links(compiled,context,state,shared,assets=None):
    operations={x['id']:x for x in context['operations']};facts=shared.get(compiled['target'],{})
    tid=compiled['target'];lookup=state['lookups'][tid]
    program={fn:ps for (t,fn),ps in state['paths'].items() if t==tid};verified=[]
    for link in compiled['links']:
        source=operations[link['from_op_ref']]['function'];dest=operations[link['to_op_ref']]['function'];certificates=[];origin='existing_source_certificate'
        if link['kind']=='nomination_acceptance':
            certificates=[x for x in facts.get('normal_state_transitions',[]) if x['kind']=='governor_nominates_recipient_accepts' and x['function']==dest and any(n['function']==source for n in x['nominations'])]
            if not certificates:
                from .m12_policy import nomination_certificates
                cache=state.setdefault('_v16_nomination_cache',{})
                if (tid,dest) not in cache:cache[(tid,dest)]=nomination_certificates(lookup,program,tid,dest)
                checked,gaps=cache[(tid,dest)];compiled.setdefault('local_check_limits',[]).extend(gaps)
                certificates=[x for x in checked if any(n['function']==source for n in x['nominations'])];origin='M2_located_source_endpoint_check'
            confirmed=[]
            for certificate in certificates:
                valid=True
                for actor in compiled['actors']:
                    if actor['function']==dest and certificate['path_index'] not in actor['path_indices']:continue
                    expected=certificate['owner'] if actor['function']==source and actor['role']=='governor' else certificate['nominee'] if actor['function']==dest and actor['role']=='nominee' else None
                    if expected is not None and key(actor['term'])!=key(expected):valid=False;break
                if valid:confirmed.append(certificate)
            certificates=confirmed
        elif link['kind']=='authorization_use':
            from .m16_shared_links import match_grant,grant_from_endpoints
            # Check all nominated use paths, including authorized burns. Static facts remain.
            certificates=grant_from_endpoints(lookup,program,assets if assets is not None else facts.get('assets',[]),source,dest,compiled)
            origin='M2_located_source_endpoint_check'
        for certificate in certificates:
            verified.append({**link,'from_function':source,'to_function':dest,'status':'program_verified','certificate':copy.deepcopy(certificate),'relation_id':compiled['relation_id'],'verification_origin':origin})
        if not certificates:
            verified.append({**link,'from_function':source,'to_function':dest,'status':'pending_financial_conversion_check' if link['kind']=='same_holder_conversion' else 'not_confirmed_by_source','not_authority_or_safety_proof':True})
    compiled['verified_links']=verified
    return verified

def financial_scope(hint,path,fn,selector,lookup,amount=None,recipients=()):
    """Consume exact subject/resource keys in M2-located asset construction."""
    compiled=hint.get('scoped_relation')
    if not compiled:return True
    from .m16_source_bindings import rows_for,path_key
    if any(x['field'] in ('resource','condition','actor') and x.get('function')==fn and x.get('path_key')==path_key(path) for x in compiled['rejections']):return False
    for condition in rows_for(compiled,'conditions',fn,path):
        if condition['function']==fn and not any(key(condition['term'])==key(g) for g in path['guards']):return False
    if not scoped_resources(compiled,fn,selector,path=path):return False
    resources=[x for x in rows_for(compiled,'resources',fn,path) if selector_matches(selector,x['selector'])]
    holders=[x['term'] for x in rows_for(compiled,'actors',fn,path) if x['role']=='holder']
    holders += [x['holder'] for x in resources if x['holder'] is not None]
    if holders and (not keys(selector) or any(key(x)!=key(keys(selector)[0]) for x in holders)):return False
    proposed_recipients=[x['term'] for x in rows_for(compiled,'actors',fn,path) if x['role'] in ('recipient','beneficiary')]
    if proposed_recipients and any(not any(key(x)==key(y) for y in recipients) for x in proposed_recipients):return False
    quantities=[x['quantity'] for x in resources if x['quantity'] is not None]
    if quantities and (amount is None or any(key(x)!=key(amount) for x in quantities)):return False
    return True

def financial_link_certificates(compiled,context,state,assets):
    operations={x['id']:x for x in context['operations']};out=[]
    for link in compiled['links']:
        if link['kind']!='same_holder_conversion':continue
        source=operations[link['from_op_ref']]['function'];dest=operations[link['to_op_ref']]['function']
        # Current bounded proof handles within-operation conversions only.
        # Cross-transaction order is never inferred from list order.
        certs=[]
        if source==dest:
            requested=[x['selector']['root'] for x in compiled['resources'] if x['function']==source]
            for asset in assets:
                cert=asset.get('equity_certificate',{})
                if cert.get('conversion_function')==source and len([r for r in compiled['resources'] if r['function']==source])>=2 and set(requested)==set(cert['roots']):
                    path=state['paths'][(compiled['target'],source)][cert['path_index']]
                    from .m16_source_bindings import rows_for
                    local_resources=rows_for(compiled,'resources',source,path)
                    writes=[w for w in path['writes'] if w['source'] in cert['conversion_writes']]
                    # Accessor and conversion parameters have different AST IDs;
                    # compare against the actual conversion's writes, not getter keys.
                    lookup=state['lookups'][compiled['target']]
                    from .m05_state_relations import changes
                    from .m03_p_assets import term,negative
                    updates=[d for d in changes(path,lookup) if d['write']['source'] in cert['conversion_writes']]
                    amount=next((term(negative(d['delta'])) for d in updates if d['delta'] and all(v<0 for v in d['delta'].values())),None)
                    hint={'scoped_relation':compiled,'operation_ids_by_function':{source:[link['from_op_ref']]}}
                    if (all(any(selector_matches(w['path'],r['selector']) for w in writes) for r in local_resources)
                            and all(financial_scope(hint,path,source,w['path'],lookup,amount,recipients=[keys(v['path'])[0] for v in writes if keys(v['path'])]) for w in writes)):certs.append(cert)
        out.append({**link,'status':('program_verified_located_conversion' if any(c.get('construction_origin')=='M2_located_source_combination' for c in certs) else 'program_verified_existing_conversion') if certs else 'not_confirmed_by_source',
                    'certificates':copy.deepcopy(certs),'causal_gain':False})
    return out

def usage_ledger(compiled,consumption,checks,scope):
    """Separate source annotation, candidate effects and observed final effects."""
    by={r['relation_id']:r for r in consumption};out=[]
    for rid,c in compiled.items():
        record=by[rid];kinds=[]
        direct=[q for q in checks if q.get('policy_basis',{}).get('relation_id')==rid]
        if direct:kinds.append('additional_policy_checks')
        if c['events']:kinds.append('candidate_scope_restriction')
        if record.get('generated_models'):kinds.append('source_checked_model_proposal_used')
        if record.get('shared_authorization_check_ids'):kinds.append('shared_authorization_certificate_consumed')
        corroborated=[q['id'] for q in checks if rid in q.get('supporting_relation_ids',[])]
        if record.get('normal_fact_uses') or record.get('query_ids') or record.get('source_asset_roots') or record.get('equity_certificates') or corroborated:kinds.append('existing_source_fact_corroboration')
        if any(x['status'].startswith('program_verified') for x in c.get('verified_links',[])):kinds.append('program_verified_operation_relationship')
        if any(x.get('construction_origin')=='M2_located_source_combination' for x in record.get('equity_certificates',[])):kinds.append('source_checked_equity_combination_constructed')
        if not kinds:kinds.append('no_confirmed_decision_use')
        out.append({'relation_id':rid,'usage_kinds':kinds,'scope_events':c['events'],
            'corroborated_program_check_ids':corroborated,'additional_check_ids':[q['id'] for q in direct],'additional_reportable_check_ids':[q['id'] for q in direct if q.get('reportable')],
            'source_bindings':{k:c[k] for k in ('actors','resources','conditions')},
            'operation_links':c.get('verified_links',[]),'rejected_bindings':c['rejections'],'local_check_limits':c.get('local_check_limits',[]),
            'shared_authorization_check_ids':record.get('shared_authorization_check_ids',[]),'equity_certificates':copy.deepcopy(record.get('equity_certificates',[])),
            'does_not_establish_causal_accuracy_gain':True})
    return out
