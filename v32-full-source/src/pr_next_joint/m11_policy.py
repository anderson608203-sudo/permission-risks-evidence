from .m20_solver import solve as bounded_solve
"""Local effect/authorization evidence. Relationships are proposals, not verdicts.
No case names, labels, expected outcomes or function-name policies are inputs.
"""
import copy
from .core import digest
from .m03_p_paths import key,walk,op,lit
from .m03_p_route import keys,selectors,value_type,effective_permission
from .m03_p_assets import add,negative,holder_path,polynomial
from .m05_state_relations import changes
from .m05_asset_obligations import consent_model
from .m09_shared_policy import implies
from .m04_logic import Unsupported
from .m22_assets import holder as holder_path, matches as asset_matches
SENDER={'kind':'actual_sender'}

def update_profile(path,root,instance,lookup,asset=None):
    updates=[d for d in changes(path,lookup) if (asset_matches(d['write']['path'],asset) if asset else d['write']['path']['root']==root and key(d['write']['path'].get('instance'))==key(instance))]
    debits=[d for d in updates if d['delta'] and all(x<=0 for x in d['delta'].values())]
    credits=[d for d in updates if d['delta'] and all(x>=0 for x in d['delta'].values())]
    if len(debits)+len(credits)!=len(updates) or not updates:return None
    total={}
    for d in updates:total=add(total,d['delta'])
    family='transfer' if debits and credits else 'decrease' if debits else 'increase'
    return {'updates':updates,'debits':debits,'credits':credits,'total':total,'family':family}

def once_latch(path,program,lookup):
    for w in path['writes']:
        if w['path'].get('segments') or w['value'] not in (lit(True),lit(False)):continue
        before=w['path'];after=w['value']
        if not implies(lookup,path,op('!=',before,after)):continue
        writers=[x for paths in program.values() for p in paths if p['flow'] in ('normal','returned') for x in p['writes'] if key(x['path'])==key(before)]
        if writers and all(x['value']==after for x in writers):return {'latch':before,'closed_value':after,'source':w['source']}
    return None

def value_backed(delta,lookup):
    # A mention of msg.value is insufficient: adding a free amount or a caller
    # controlled extra amount must not manufacture a purchase certificate.
    from .m08_financial import quantity
    from .m05_mechanism_core import MechanismEncoder
    expression=quantity(delta)
    if not any(n.get('kind')=='transaction_value' for n in walk(expression)):return False
    if any(n.get('kind')=='parameter' for n in walk(expression)):return False
    try:
        e=MechanismEncoder(lookup);amount=e.expr(expression);paid=e.expr({'kind':'transaction_value','type':'uint256'})
        solver=e.z.Solver();solver.set(timeout=3000);solver.add(*e.constraints,paid==0)
        if bounded_solve(solver)!=e.z.sat:return False
        solver.add(amount!=0)
        return bounded_solve(solver)==e.z.unsat
    except (Unsupported,ValueError):return False

def facts(state,shared):
    limits=[]
    for tid,lookup in state['lookups'].items():
        program={f:p for (t,f),p in state['paths'].items() if t==tid}
        data=shared[tid];data['effect_profiles']=[];data['normal_effects']=[]
        for fn,paths in program.items():
            for pi,path in enumerate(paths):
                if path['flow'] not in ('normal','returned') or path['issues'] or path.get('evaluation_gaps'):continue
                for model in data['assets']:
                    root=model['balance_root'];instance=model['balance_effect']['path'].get('instance')
                    try:
                        profile=update_profile(path,root,instance,lookup,model)
                        if not profile:continue
                        item={'function':fn,'path_index':pi,'root':root,'instance':instance,'family':profile['family'],
                              'debit_holders':[keys(d['write']['path'])[0] for d in profile['debits'] if holder_path(d['write']['path'],lookup)],
                              'credit_holders':[keys(d['write']['path'])[0] for d in profile['credits'] if holder_path(d['write']['path'],lookup)],
                              'effect_sources':[d['write']['source'] for d in profile['updates']]}
                        data['effect_profiles'].append(item)
                        cert=None
                        if len(profile['debits'])==1:
                            debit=profile['debits'][0];sel=debit['write']['path']
                            if holder_path(sel,lookup):
                                holder=keys(sel)[0];amount=negative(debit['delta'])
                                recipient=keys(profile['credits'][0]['write']['path'])[0] if len(profile['credits'])==1 else None
                                if holder.get('kind')=='contract_address':
                                    credits=profile['credits']
                                    if profile['total']=={} and len(credits)==1 and keys(credits[0]['write']['path'])[0].get('kind')=='actual_sender' and value_backed(credits[0]['delta'],lookup):
                                        cert={'kind':'source_value_backed_self_purchase','value_relation':credits[0]['write']['local_increment']}
                                else:
                                    consent,evidence=consent_model(path,holder,amount,lookup,program,root,model.get('supply_root'),recipient=recipient,sufficient_only=True)
                                    if implies(lookup,path,consent):cert={'kind':'holder_or_full_amount_delegation','consent':consent,'consent_sources':evidence}
                        if not profile['debits'] and len(profile['credits'])==1:
                            credit=profile['credits'][0];sel=credit['write']['path']
                            if holder_path(sel,lookup) and keys(sel)[0].get('kind')=='actual_sender':
                                value=credit['write'].get('local_increment') or credit['write']['value']
                                paid=value_backed(credit['delta'],lookup)
                                caller_guards=[s for g in path['guards'] for s in selectors(g) if any(k.get('kind')=='actual_sender' for k in keys(s)) and s['root']!=root]
                                consumed=[w for w in path['writes'] if any(key(w['path'])==key(g) for g in caller_guards) and w['value'] in (lit(True),lit(False)) and implies(lookup,path,op('!=',w['path'],w['value']))]
                                fixed=all(n.get('kind')!='parameter' for n in walk(value))
                                if paid:cert={'kind':'source_value_backed_self_purchase','value_relation':value}
                                elif fixed and consumed:cert={'kind':'bounded_self_claim_with_consumed_eligibility','eligibility_sources':[w['source'] for w in consumed],'value_relation':value}
                        if cert:
                            # Companion accounting is attached only to sourced
                            # non-address counters / claim flags on this path.
                            effects=list(item['effect_sources']);companions=[]
                            counter_roots=set()
                            for delta in changes(path,lookup):
                                w=delta['write'];typ=value_type(w['path'],lookup)
                                if not w['path'].get('segments') and typ and typ.startswith('uint') and profile['total'] and delta['delta']==profile['total']:
                                    effects.append(w['source']);companions.append(w['source']);counter_roots.add(w['path']['root'])
                            if cert['kind']=='bounded_self_claim_with_consumed_eligibility':
                                for w in path['writes']:
                                    if w['source'] in cert['eligibility_sources']:effects.append(w['source']);companions.append(w['source'])
                                    # Automatic close is justified only by a
                                    # reached bound on the credited counters.
                            cert['accounting_counter_roots']=sorted(counter_roots)
                            cert['companion_effect_sources']=companions
                            data['normal_effects'].append({**item,**cert,'effect_sources':effects,'relation_ids':[]})
                    except (Unsupported,ValueError) as ex:limits.append({'target':tid,'function':fn,'phase':'local_normal_effect','reason':str(ex)})
    return limits

def applicability(query,state,shared):
    basis=query.get('policy_basis',{});kind=basis.get('basis')
    if kind not in ('same_resource_guarded_operation','source_checked_M2_relation'):return None
    tid=query['target'];fn=query['function'];pi=query.get('path_index');origin=basis.get('origin_function')
    if not origin or origin==fn:return None
    data=shared.get(tid,{})
    source=query.get('effect',{}).get('source',{})
    for init in data.get('normal_initializations',[]):
        if init['function']==fn and init['path_index']==pi and source in init['effect_sources']:
            return {'decision':'one_time_initialization','reason':'source_one_way_latch_limits_reentry','source_certificate':copy.deepcopy(init),'original_policy':query.get('required_policy_candidate')}
    normal=[f for f in data.get('normal_effects',[]) if f['function']==fn and f['path_index']==pi and source in f['effect_sources']]
    for fact in normal:
        peers=[f for f in data.get('effect_profiles',[]) if f['function']==origin and f['root']==fact['root'] and key(f['instance'])==key(fact['instance'])]
        companion=source in fact.get('companion_effect_sources',[])
        if not peers and companion:
            return {'decision':'normal_accounting_companion','reason':'local accounting/eligibility/closing effect paired with source-authorized asset action','source_certificate':copy.deepcopy(fact),'original_policy':query.get('required_policy_candidate')}
        if not peers:
            from .m12_policy import source_allocation_role
            role=source_allocation_role(state['lookups'][tid],origin,fact['root'])
            if fact['kind']=='holder_or_full_amount_delegation' and role:
                return {'decision':'source_allocation_is_not_holder_service',
                    'source_certificate':copy.deepcopy(fact),'origin_source_role':role,
                    'original_policy':query.get('required_policy_candidate')}
            continue
        # A protected counterpart of the same holder-driven service still
        # supplies a candidate; a different economic role does not.
        same_service=any(p['family']==fact['family'] and any(n['function']==origin and n['path_index']==p['path_index'] and n['root']==p['root'] and n['kind']=='holder_or_full_amount_delegation' for n in data.get('normal_effects',[])) for p in peers)
        purchase=fact['kind'] in ('source_value_backed_self_purchase','bounded_self_claim_with_consumed_eligibility')
        if not same_service or purchase:
            return {'decision':'normal_local_effect_displaces_inapplicable_peer_policy',
                'reason':'shared_storage_is_not_shared_authorization; sourced normal action has a distinct effect/subject role',
                'source_certificate':copy.deepcopy(fact),'origin_effect_profiles':peers,
                'original_policy':query.get('required_policy_candidate')}
    return None

def make_query(context,tid,fn,pi,path,write,required,basis,rule='AC-01'):
    effect={'object':str(write['path']['root']),'selector':write['path'],'value':write['value'],'operator':write['operator'],'source':write['source']}
    row={'rule':rule,'target':tid,'function':fn,'path_index':pi,'conditions':copy.deepcopy(path['guards']),
         'issues':copy.deepcopy(path['issues']),'effect':effect,'required_policy_candidate':required,'policy_basis':basis,
         'program_id':context['identity']['program_id'],'build_id':context['identity']['build_id'],
         'source_evaluation_terms':copy.deepcopy(path.get('evaluated_terms',[])),
         'policy_applicability':{'basis':'source_sensitive_effect_obligation','effect_source':write['source'],'checked_before_solver':True}}
    row['id']='q_'+digest(row);return row

def obligations(context,state,shared,relations,consumption):
    rows=[];limits=[]
    for tid,lookup in state['lookups'].items():
        program={f:p for (t,f),p in state['paths'].items() if t==tid}
        beneficiaries={}
        authorities={}
        permissions_by_path={}
        for fn,paths in program.items():
            for pi,path in enumerate(paths):
                try:permissions_by_path[id(path)]=effective_permission(path['guards'],lookup)
                except (Unsupported,ValueError) as error:
                    permissions_by_path[id(path)]=None
                    limits.append({'target':tid,'function':fn,'path':pi,'phase':'permission_obligation','reason':str(error),'not_an_unprotected_path':True})
        for fn,paths in program.items():
            for p in paths:
                for permission in permissions_by_path[id(p)] or []:
                    for s in selectors(permission):
                        if not s.get('segments') and value_type(s,lookup) in ('address','address payable'):authorities[key(s)]=s
                for e in p.get('sensitive_effects',[]):
                    if e['kind']!='native_transfer':continue
                    for s in selectors(e['recipient']):
                        if not s.get('segments') and value_type(s,lookup) in ('address','address payable'):
                            beneficiaries.setdefault(s['root'],[]).append({'function':fn,'source':e['source'],'recipient':s,'amount':e['amount']})
        for fn,paths in program.items():
            for pi,p in enumerate(paths):
                if p['flow'] not in ('normal','returned'):continue
                permissions=permissions_by_path[id(p)]
                if permissions is None:continue
                for w in p['writes']:
                    selector=w['path'];root=selector['root']
                    if root in beneficiaries and not selector.get('segments'):
                        related_authorities=[g for paths in program.values() for branch in paths if branch['flow'] in ('normal','returned') and not branch['issues'] and any(x['path']['root']==root for x in branch['writes']) for g in permissions_by_path[id(branch)] or []]
                        if not related_authorities:
                            limits.append({'target':tid,'function':fn,'phase':'beneficiary_policy','reason':'recipient_use_alone_not_authorization','effect_source':w['source'],'payment_uses':beneficiaries[root]});continue
                        # Recipient equality alone is not authority. Independent
                        # protected operations remain subject to D01 admission.
                        for other,branches in program.items():
                            for oi,branch in enumerate(branches):
                                perms=permissions_by_path.get(id(branch)) or []
                                if not perms or branch['issues']:continue
                                if not any(key(z['path'])==key(selector) for z in branch['writes']):continue
                                for perm in perms:
                                    rows.append(make_query(context,tid,fn,pi,p,w,perm,{'basis':'same_resource_guarded_operation','origin_function':other,'origin_path_index':oi,'source_origin':'source_payment_beneficiary_reconfiguration'}))
                        continue
                for model in shared.get(tid,{}).get('assets',[]):
                    root=model['balance_root'];supply=model.get('supply_root')
                    try:
                        # A literal/scalar replacement of outstanding supply and
                        # caller holdings is a reset, not an additive public mint.
                        resets=[w for w in p['writes'] if not w['path'].get('segments') and str(value_type(w['path'],lookup)).startswith('uint') and w.get('operator')=='=' and not any(s['root']==w['path']['root'] for s in selectors(w['value']))]
                        for reset in resets:
                            holdings=[w for w in p['writes'] if w['path']['root']==root and holder_path(w['path'],lookup) and keys(w['path'])[0].get('kind')=='actual_sender' and key(w['value'])==key(reset['value']) and any(n.get('referencedDeclaration')==reset['path']['root'] for n in walk(lookup.nodes.get(w['source']['ast_id'],{}).get('rightHandSide',{})))]
                            if not holdings or p['issues'] or p.get('evaluation_gaps'):continue
                            latch=once_latch(p,program,lookup)
                            if latch:
                                shared[tid].setdefault('normal_initializations',[]).append({'function':fn,'path_index':pi,'effect_sources':[reset['source']]+[w['source'] for w in holdings],'latch':latch})
                                limits.append({'target':tid,'function':fn,'phase':'normal_initialization','reason':'source_one_way_latch','certificate':latch});continue
                            empty=op('==',reset['path'],lit(0));required=op('or',empty,*permissions) if permissions else empty
                            rows.append(make_query(context,tid,fn,pi,p,reset,required,{'basis':'source_outstanding_entitlement_reset',
                                'balance_replacements':[w['source'] for w in holdings],'scope':'replacing extant supply/holder allocation requires authority or uninitialized state'},'AC-02'))
                        profile=update_profile(p,root,model['balance_effect']['path'].get('instance'),lookup,model)
                        if not profile or len(profile['debits'])!=1:continue
                        debit=profile['debits'][0];sel=debit['write']['path']
                        if not holder_path(sel,lookup):continue
                        holder=keys(sel)[0]
                        if holder.get('kind') in ('actual_sender','contract_address'):continue
                        recipient=keys(profile['credits'][0]['write']['path'])[0] if len(profile['credits'])==1 else None
                        consent,cert=consent_model(p,holder,negative(debit['delta']),lookup,program,root,supply,recipient=recipient)
                        # Explicit privileged asset disposition is FCR's target;
                        # AC checks public disposition or malformed delegation.
                        required=op('or',consent,*permissions) if permissions else consent
                        rows.append(make_query(context,tid,fn,pi,p,debit['write'],required,{'basis':'source_holder_entitlement_disposition','holder':holder,'holder_consent':cert,'privileged_alternatives':permissions}))
                    except (Unsupported,ValueError) as ex:limits.append({'target':tid,'function':fn,'phase':'sensitive_effect_obligation','reason':str(ex)})
    operations={o['id']:o for o in context['operations']};records={r['relation_id']:r for r in consumption}
    for relation in relations['relations']:
        if relation['relation_kind'] not in ('controlled_by','holder_of','checks_permission','delegates_to'):continue
        operation=operations[relation['op_ref']]
        referenced={context['references'][r]['ast_id'] for r in relation['source_refs']+([relation['resource_ref']] if relation.get('resource_ref') else [])}
        linked=[q for q in rows if q['target']==operation['target'] and q['function']==operation['function'] and
                (q['effect']['selector']['root'] in referenced or q['effect']['source']['ast_id'] in referenced)]
        if linked:
            record=records[relation['id']];record.setdefault('queries',[]).extend(q['id'] for q in linked)
            record['status']='source_confirmed_sensitive_effect_relationship'
            for q in linked:q.setdefault('supporting_relation_ids',[]).append(relation['id'])
    return rows,limits
