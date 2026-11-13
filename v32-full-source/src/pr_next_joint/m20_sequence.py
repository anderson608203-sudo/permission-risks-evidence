"""Compose up to three source operations with separate transaction identities.
No assertion of deployment reachability; initial symbolic state is explicit.
"""
import copy
from .m03_p_paths import walk,key,op,lit
from .m03_p_route import selectors,keys,fields
from .m05_state_relations import compose_read,expand_write
from .m04_logic import Unsupported

def qualify(value,step):
    if isinstance(value,dict):
        kind=value.get('kind')
        if kind=='actual_sender':return {'kind':'parameter','id':-9000000-step,'type':'address','sequence_role':'caller','step':step}
        if kind=='parameter':return {**value,'id':-((step+1)*10000000+abs(int(value['id']))),'step':step}
        if kind=='environment' and value.get('field') in ('timestamp','number'):
            return {'kind':'parameter','id':-(81000000+step*10+('timestamp','number').index(value['field'])),
                    'type':'uint256','sequence_role':value['field'],'step':step}
        if kind in ('transaction_origin','source_calldata_length','native_call_success'):
            return {**value,'sequence_step':step}
        if kind in ('transaction_value','block_timestamp','block_number'):
            return {'kind':'parameter','id':-(80000000+step*10+('transaction_value','block_timestamp','block_number').index(kind)),
                    'type':'uint256','sequence_role':kind,'step':step}
        return {k:qualify(v,step) for k,v in value.items()}
    return [qualify(v,step) for v in value] if isinstance(value,list) else value

def compose(lookup,steps,equalities=()):
    if not 1<=len(steps)<=3:raise Unsupported('v20_transaction_sequence_bound')
    writes=[];guards=[];evaluated=[];trace=[]
    for i,(fn,pi,path) in enumerate(steps):
        if path['flow'] not in ('normal','returned') or path['issues'] or path.get('evaluation_gaps'):raise Unsupported('v20_sequence_path_incomplete')
        before=copy.deepcopy(writes)
        g=[read(qualify(x,i),before,lookup) for x in path['guards']]
        guards+=g
        evaluated.extend(read(qualify(v,i),before,lookup) for v in path.get('evaluated_terms',[]))
        stepwrites=[]
        for w in path['writes']:
            for e in expand_write(w,lookup):
                q=qualify(e,i)
                # Each path value already includes same-call substitutions.
                q['value']=read(q['value'],before,lookup)
                # Bind indexed keys using pre-state, never replace the location itself.
                q['path']={**q['path'],'segments':read(q['path'].get('segments',[]),before,lookup)}
                stepwrites.append(q)
        writes+=stepwrites
        if i:
            for field in ('timestamp','number'):
                now=qualify({'kind':'environment','field':field},i)
                prev=qualify({'kind':'environment','field':field},i-1)
                guards.append(op('>=',now,prev))
        trace.append({'step':i,'function':fn,'path_index':pi,'caller':qualify({'kind':'actual_sender'},i),'writes':stepwrites,'before_writes':before})
    guards.extend(copy.deepcopy(equalities))
    return {'conditions':guards,'writes':writes,'evaluation_terms':evaluated,'steps':trace,
            'assumption':'source-matched sequence from declared symbolic prestate; deployment prefix not proved'}


def read(value,writes,lookup):
    """Resolve key expressions from the pre-state as well as stored values."""
    if isinstance(value,dict):
        if value.get('kind')=='storage':
            prepared={**value,'segments':read(value.get('segments',[]),writes,lookup)}
            return compose_read(prepared,writes,lookup)
        return {k:read(v,writes,lookup) for k,v in value.items()}
    return [read(v,writes,lookup) for v in value] if isinstance(value,list) else value

def request_states(request_term, committed_setup_writes, lookup):
    """Hold caller, calldata and request-state symbols fixed between both worlds.
    The caller chooses namespaces before calling this routine. Only the
    earlier operation's committed writes can explain a difference."""
    return request_term,read(request_term,committed_setup_writes,lookup)

def variant(lookup,query,steps):
    from .core import digest
    combined=compose(lookup,steps);last=len(steps)-1;before=combined['steps'][-1]['before_writes']
    q=copy.deepcopy(query)
    # Preserve operation-specific premises (quantity, authorization phase,
    # candidate scope) as well as source-path guards. Composition may refine
    # an existing check, never silently weaken it.
    original_conditions=[read(qualify(x,last),before,lookup) for x in query.get('conditions',[])]
    q['conditions']=list({key(x):x for x in combined['conditions']+original_conditions}.values())
    original_terms=[read(qualify(x,last),before,lookup) for x in query.get('source_evaluation_terms',[])]
    q['source_evaluation_terms']=list({key(x):x for x in combined['evaluation_terms']+original_terms}.values())
    q['required_policy_candidate']=read(qualify(q['required_policy_candidate'],last),before,lookup)
    effect=q['effect']
    if effect.get('selector',{}).get('kind')=='storage':
        # Effects_changed needs an explicit pre-value; a pre-state expression
        # cannot be used as a storage location.
        location=qualify(effect['selector'],last)
        location={**location,'segments':read(location.get('segments',[]),before,lookup)}
        effect['selector']=location
        effect['sequence_before_value']=read(location,before,lookup)
        effect['value']=read(qualify(effect['value'],last),before,lookup)
    else:
        for name in ('recipient','amount','success'):
            if name in effect:effect[name]=read(qualify(effect[name],last),before,lookup)
    if q['rule']=='AC-04':
        for field in ('validity_assumptions',):
            if field in q['policy_basis']:q['policy_basis'][field]=read(qualify(q['policy_basis'][field],last),before,lookup)
    q['sequence_model']={'steps':combined['steps'],'assumption':combined['assumption'],
                         'maximum_external_operations':3,'original_query_id':query['id']}
    q['id']='seq_'+digest(q)
    return q

def candidates(query,state,context,relations):
    """Refine a sourced obligation with actual connected prior writes.
    Does not create a new permission rule or turn an unsat sequence into safety.
    """
    if query.get('sequence_extension_disabled'):return []
    tid=query['target'];fn=query['function'];pi=query.get('path_index')
    if query['rule'] not in ('AC-01','AC-02','AC-03','AC-04') or pi is None:return []
    if query.get('graph_frame_obligation') or query.get('policy_basis',{}).get('basis')=='source_caller_selected_code_execution_boundary':return []
    if query['rule']=='AC-04' and query.get('policy_basis',{}).get('basis') not in ('issued_future_expiry','issued_time_interval','issued_epoch_snapshot'):return []
    paths=state['paths'].get((tid,fn),[])
    if pi>=len(paths):return []
    lookup=state['lookups'][tid];program={f:p for (t,f),p in state['paths'].items() if t==tid}
    ops={o['id']:o for o in context['operations']};chains=[]
    index=state.get('_v20_effect_index')
    links=index.stage_links if index else []
    for link in links:
        if link['target']!=tid or link['to_function']!=fn or link['kind']=='same_holder_conversion':continue
        chains.append(([link['from_function']],link['relation_id'],link['kind']))
        for earlier in links:
            if earlier['target']==tid and earlier['relation_id']==link['relation_id'] and earlier['to_function']==link['from_function'] and earlier['from_function']!=fn:
                chains.append(([earlier['from_function'],link['from_function']],link['relation_id'],'three_source_linked_operations'))
    basis=query.get('policy_basis',{}).get('basis')
    if basis in ('v20_source_authority_replacement','v20_semantic_source_authority'):
        chains.append(([fn],query.get('policy_basis',{}).get('relation_id'),'repeated_authority_operation'))
    if query['rule']=='AC-04' and query.get('policy_basis',{}).get('issuer') in program:
        chains.append(([query['policy_basis']['issuer']],None,'source_authorization_issuance_then_use'))
    required_roots={s['root'] for s in selectors([query['required_policy_candidate'],query['conditions']])}
    out=[];cache=state.setdefault('_v20_sequence_variant_cache',{})
    for prior,rid,kind in chains:
        branches=[[]]
        for predecessor in prior:
            expanded=[]
            for base in branches:
                for ppi,p in enumerate(program.get(predecessor,[])):
                    if p['flow'] not in ('normal','returned') or p['issues'] or p.get('evaluation_gaps'):continue
                    if not any(w['path']['root'] in required_roots for w in p['writes']):continue
                    expanded.append(base+[(predecessor,ppi,p)])
            if len(expanded)>8:state.setdefault('_v20_sequence_limits',[]).append({'target':tid,'function':fn,'reason':'eight_source_paths_per_composition_bound','omitted':len(expanded)-8})
            branches=expanded[:8]
        for branch in branches:
            if len(out)>=8:break
            steps=branch+[(fn,pi,paths[pi])]
            try:
                q=variant(lookup,query,steps)
                q['sequence_model'].update(relation_id=rid,link_kind=kind,
                    use='actual shared-state constraint refinement; no additional authority inference')
                signature=key([query['id'],[(f,i) for f,i,p in steps]])
                if signature in cache:continue
                cache[signature]=True;out.append(q)
            except (Unsupported,ValueError,KeyError) as e:
                state.setdefault('_v20_sequence_limits',[]).append({'target':tid,'function':fn,'reason':str(e)})
    return out
