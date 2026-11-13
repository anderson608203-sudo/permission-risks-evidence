"""Source-bound lifecycle and authority transitions; AC exclusions only.
No names, dataset identities or expected labels are policy evidence.
"""
import copy
from .m03_p_paths import key,walk,op,lit
from .m03_p_route import selectors,keys,value_type,effective_permission
from .m05_state_relations import changes
from .m09_shared_policy import implies
from .m05_writer_scope import gaps_for
from .m04_logic import Unsupported
SENDER={'kind':'actual_sender'}

def source_allocation_role(lookup,fn,root):
    """A source replacement of indexed holdings is distinct from conservation.
    Used only when a normal holder action is already established locally and
    the peer has no complete path profile. No absent profile implies legality.
    """
    body=lookup.function(fn)
    if not body:return None
    evidence=[]
    for node in walk(body):
        if node.get('nodeType')!='Assignment' or node.get('operator')!='=':continue
        lhs=node.get('leftHandSide',{});rhs=node.get('rightHandSide',{})
        if lhs.get('nodeType')!='IndexAccess':continue
        if not any(n.get('referencedDeclaration')==root for n in walk(lhs)):continue
        if any(n.get('referencedDeclaration')==root for n in walk(rhs)):continue
        # Only a parameter-bound allocation, not an arbitrary opaque call.
        if any(n.get('nodeType')=='FunctionCall' for n in walk(rhs)):continue
        refs=[lookup.nodes.get(n.get('referencedDeclaration'),{}) for n in walk(rhs)]
        params={p['id'] for p in body.get('parameters',{}).get('parameters',[])}
        # Literal or scalar source allocations also establish the allocator role.
        if any(r.get('nodeType')=='VariableDeclaration' and not r.get('stateVariable') and r.get('id') not in params for r in refs):continue
        evidence.append(lookup.anchor(node))
    return {'kind':'parameter_driven_holding_replacement','sources':evidence,
            'scope':'peer allocation is not evidence that holder transfer needs its governor'} if evidence else None

def clean(p):return p['flow'] in ('normal','returned') and not p['issues'] and not p.get('evaluation_gaps')

def facts(state,shared):
    limits=[]
    for tid,lookup in state['lookups'].items():
        data=shared[tid];out=data['normal_state_transitions']=[]
        program={fn:ps for (t,fn),ps in state['paths'].items() if t==tid}
        certificates,gaps=nomination_certificates(lookup,program,tid)
        out.extend(certificates);limits.extend(gaps)
        # A reached distribution bound can close the claim even if this call
        # credits zero. Derive the relationship from positive sibling paths,
        # then check the actual zero path and flag rather than copying its result.
        visited_closings=set()
        for normal in data.get('normal_effects',[]):
            if normal['kind'] not in ('bounded_self_claim_with_consumed_eligibility','source_value_backed_self_purchase'):continue
            counters=set(normal.get('accounting_counter_roots',[]))
            if not counters:continue
            ps=program[normal['function']];origin=ps[normal['path_index']]
            for closing in origin['writes']:
                flag=closing['path']
                if flag.get('segments') or closing['value']!=lit(True) or value_type(flag,lookup)!='bool':continue
                # A generic transfer lock is not a distribution-only close.
                transfer_use=any(f['family']=='transfer' and any(s['root']==flag['root'] for g in program[f['function']][f['path_index']]['guards'] for s in selectors(g)) for f in data.get('effect_profiles',[]))
                if transfer_use:continue
                signature=key([normal['function'],normal['root'],closing['source'],sorted(counters)])
                if signature in visited_closings:continue
                visited_closings.add(signature)
                for pi,p in enumerate(ps):
                    if not clean(p) or not any(w['source']==closing['source'] and w['value']==lit(True) for w in p['writes']):continue
                    try:
                        if not implies(lookup,p,op('==',flag,lit(False))):continue
                        bound=[]
                        for g in p['guards']:
                            for atom in walk(g):
                                if atom.get('kind')!='op' or atom.get('op') not in ('>=','>','==','<','<=') or len(atom.get('args',[]))!=2:continue
                                left,right=atom['args'];relation=atom['op']
                                if not any(s['root'] in counters for s in selectors(left)):
                                    left,right=right,left;relation={'>=':'<=','>':'<','<=':'>=','<':'>','==':'=='}[relation]
                                if not any(s['root'] in counters for s in selectors(left)):continue
                                if any(s['root'] in counters for s in selectors(right)):continue
                                if any(n.get('kind') in ('parameter','actual_sender','unknown') for n in walk(right)):continue
                                # Negated or reversed bounds are checked by implication,
                                # not by syntactic presence of a comparison.
                                relation={'<':'>=','<=':'>'}.get(relation,relation)
                                reached=op(relation,left,right)
                                if implies(lookup,p,reached):bound.append(reached)
                        if not bound:continue
                        same=next((f for f in data.get('normal_effects',[]) if f['function']==normal['function'] and f['path_index']==pi and f['kind']==normal['kind']),None)
                        zero=all(not d['delta'] or implies(lookup,p,op('==',d['write']['value'],d['write']['path'])) for d in changes(p,lookup) if d['write']['path']['root'] in counters|{normal['root']})
                        if not same and not zero:continue
                        out.append({'kind':'source_bound_distribution_completion','function':normal['function'],'path_index':pi,
                            'effect_sources':[closing['source']],'counter_roots':sorted(counters),'bound_conditions':bound,
                            'zero_increment_path':not bool(same),'positive_sibling_effect_sources':normal['effect_sources']})
                    except (Unsupported,ValueError) as ex:limits.append({'target':tid,'function':normal['function'],'phase':'distribution_completion','reason':str(ex)})
        unique={key(x):x for x in out};data['normal_state_transitions']=list(unique.values())
    return limits

def alternative(query,state,shared):
    basis=query.get('policy_basis',{})
    if basis.get('basis') not in ('same_resource_guarded_operation','source_checked_M2_relation'):return None
    if not basis.get('origin_function') or basis['origin_function']==query['function']:return None
    tid=query['target'];source=query.get('effect',{}).get('source');lookup=state['lookups'][tid]
    for fact in shared[tid].get('normal_state_transitions',[]):
        # A nominated recipient's acceptance guard is not the incumbent's
        # nomination guard. Apply the same verified handoff to its nomination
        # effect, without exempting unrelated writes or unverified writers.
        if fact['kind']=='governor_nominates_recipient_accepts' and basis['origin_function']==fact['function']:
            nomination=next((n for n in fact['nominations'] if n['function']==query['function']
                and n['path_index']==query.get('path_index') and n['source']==source),None)
            required=query.get('required_policy_candidate',{})
            nominee_guard=op('==',SENDER,fact['nominee'])
            if (nomination and key(query.get('effect',{}).get('selector'))==key(fact['nominee'])
                    and {s['root'] for s in selectors(required)}=={fact['nominee']['root']}):
                try:
                    if implies(lookup,{'guards':[nominee_guard]},required):
                        return {'decision':'source_verified_state_transition',
                            'source_certificate':{**copy.deepcopy(fact),'applied_stage':'nomination',
                                'validated_nomination':copy.deepcopy(nomination)},
                            'original_policy':required,'scope':'verified incumbent nomination effect/path; AC only'}
                except (Unsupported,ValueError):pass
        if fact['function']!=query['function'] or fact['path_index']!=query.get('path_index') or source not in fact['effect_sources']:continue
        if fact['kind']=='governor_nominates_recipient_accepts':
            required=query.get('required_policy_candidate',{})
            roots={s['root'] for s in selectors(required)}
            if roots!={fact['owner']['root']}:continue
            try:
                if not implies(lookup,{'guards':[op('==',SENDER,fact['owner'])]},required):continue
            except (Unsupported,ValueError):continue
        return {'decision':'source_verified_state_transition','source_certificate':copy.deepcopy(fact),
                'original_policy':query.get('required_policy_candidate'),'scope':'this effect and path; AC only'}
    return None

def nomination_certificates(lookup,program,tid,accept_function=None):
    out=[];limits=[]
    # One authorized nominator, a distinct accepting principal and a
    # consumed nomination form a local transition, not two equal guards.
    for fn,paths in program.items():
        if accept_function is not None and fn!=accept_function:continue
        for pi,p in enumerate(paths):
            if not clean(p):continue
            for w in p['writes']:
                owner=w['path'];pending=w['value']
                if owner.get('segments') or pending.get('kind')!='storage' or pending.get('segments') or key(owner)==key(pending):continue
                if value_type(owner,lookup) not in ('address','address payable') or value_type(pending,lookup) not in ('address','address payable'):continue
                cleared=[x for x in p['writes'] if key(x['path'])==key(pending) and x['value']==lit(0)]
                if not cleared or gaps_for(lookup,{pending['root']}):continue
                try:
                    if not implies(lookup,p,op('==',SENDER,pending)):continue
                    nominations=[];valid=True
                    for other,branches in program.items():
                        for nomination_pi,branch in enumerate(branches):
                            if branch['flow']=='reverted':continue
                            for setter in branch['writes']:
                                if key(setter['path'])!=key(pending):continue
                                if setter['value']==lit(0):continue
                                if not clean(branch) or not implies(lookup,branch,op('==',SENDER,owner)):
                                    valid=False;break
                                nominations.append({'function':other,'path_index':nomination_pi,'source':setter['source']})
                    if valid and nominations:
                        out.append({'kind':'governor_nominates_recipient_accepts','function':fn,'path_index':pi,
                            'owner':owner,'nominee':pending,'nominations':nominations,
                            'effect_sources':[w['source']]+[x['source'] for x in cleared]})
                except (Unsupported,ValueError) as ex:limits.append({'target':tid,'function':fn,'phase':'authority_transition','reason':str(ex)})
    return out,limits

