"""Source-bound authorization use, distinct from grant or object identity.
No function names, dataset identities, or labels participate in certificates.
"""
import copy
from .m03_p_paths import key,op,lit
from .m03_p_route import selectors,keys,value_type,relocate
from .m09_shared_policy import implies
from .m04_logic import Unsupported
SENDER={'kind':'actual_sender'}

def clean(path):
    return path['flow'] in ('normal','returned') and not path['issues'] and not path.get('evaluation_gaps')

def prove(lookup,path,predicate):
    try:return implies(lookup,path,predicate)
    except (Unsupported,ValueError):return False

def equality(a,b):return op('==',a,b)

def same_instance(a,b):return key(a.get('instance'))==key(b.get('instance'))

def facts(state,shared):
    for tid,lookup in state['lookups'].items():
        program={f:ps for (t,f),ps in state['paths'].items() if t==tid}
        paths=[(fn,pi,p) for fn,ps in program.items() for pi,p in enumerate(ps) if clean(p)]
        grants={};operators={}
        for fn,pi,p in paths:
            for w in p['writes']:
                sel=w['path'];ks=keys(sel);typ=value_type(sel,lookup)
                if len(ks)==1 and typ in ('address','address payable') and w['value'].get('kind')=='parameter':
                    grants.setdefault(sel['root'],[]).append((fn,pi,p,w))
                if len(ks)==2 and ks[0]==SENDER and ks[1].get('type') in ('address','address payable') and typ=='bool':
                    operators.setdefault(sel['root'],[]).append({'function':fn,'source':w['source'],'selector':sel})
        certs=[]
        for fn,pi,p in paths:
            sels={key(s):s for s in selectors(p['guards'])}
            owners=[s for s in sels.values() if len(keys(s))==1 and str(keys(s)[0].get('type','')).startswith('uint') and value_type(s,lookup) in ('address','address payable')]
            for owner in owners:
                ownership=[w for w in p['writes'] if key(w['path'])==key(owner)]
                if not ownership or ownership[-1]['value'].get('type') not in ('address','address payable'):continue
                recipient=ownership[-1]['value']
                manager=[];manager_sources=[]
                for selected in sels.values():
                    if selected['root'] not in operators or not same_instance(owner,selected):continue
                    ks=keys(selected)
                    if len(ks)==2 and key(ks[0])==key(owner) and ks[1]==SENDER:
                        manager.append(selected);manager_sources.extend(operators[selected['root']])
                grant_authority=op('or',equality(SENDER,owner),*manager)
                for delegate in sels.values():
                    if delegate['root']==owner['root'] or key(keys(delegate))!=key(keys(owner)) or not same_instance(owner,delegate):continue
                    if value_type(delegate,lookup) not in ('address','address payable'):continue
                    clearings=[w for w in p['writes'] if key(w['path'])==key(delegate) and w['value']==lit(0)]
                    if not clearings and not prove(lookup,p,equality(delegate,lit(0))):continue
                    authority=op('or',equality(SENDER,owner),equality(SENDER,delegate),*manager)
                    if not prove(lookup,p,authority):continue
                    source_grants=[]
                    for creator,ci,cp,cw in grants.get(delegate['root'],[]):
                        if not same_instance(cw['path'],delegate):continue
                        try:required=relocate(grant_authority,delegate,cw['path'])
                        except ValueError:continue
                        if prove(lookup,cp,required):source_grants.append({'function':creator,'path_index':ci,'source':cw['source'],'required':required})
                    if not source_grants:continue
                    effects=[w['source'] for w in ownership+clearings]
                    # An object count can accompany the same ownership move.
                    # Prove its local +/-1 effect and old/new holder binding;
                    # this does not authorize unrelated writes in the function.
                    for w in p['writes']:
                        sk=keys(w['path'])
                        if len(sk)!=1 or not str(value_type(w['path'],lookup)).startswith('uint'):continue
                        debit=op('and',equality(sk[0],owner),equality(w['value'],op('-',w['path'],lit(1))))
                        credit_change=op('or',equality(w['value'],op('+',w['path'],lit(1))),op('and',equality(recipient,owner),equality(w['value'],w['path'])))
                        credit=op('and',equality(sk[0],recipient),credit_change)
                        if prove(lookup,p,debit) or prove(lookup,p,credit):effects.append(w['source'])
                    certs.append({'kind':'source_bound_object_delegate_use_and_cleanup','function':fn,'path_index':pi,'owner':owner,'delegate':delegate,'manager_predicates':manager,'manager_sources':manager_sources,'authorization':authority,'grant_authority':grant_authority,'grant_sources':source_grants,'effect_sources':effects,'ownership_transition':ownership,'scope':'same object and source effect only; issuance functions remain separately checked'})
        shared.setdefault(tid,{})['object_delegation_use']=certs
    return shared

def object_identity_query(q,owner,lookup,path):
    basis=q.get('policy_basis',{})
    if basis.get('basis')!='caller_selected_authorization_subject':return False
    observed=basis.get('observed');required=q.get('required_policy_candidate')
    if not isinstance(observed,dict) or observed.get('op')!='==' or len(observed.get('args',[]))!=2:return False
    if not prove(lookup,path,equality(required,equality(SENDER,owner))):return False
    return any(key(a)==key(owner) and b.get('kind')=='parameter' and b.get('type') in ('address','address payable') for a,b in (observed['args'],observed['args'][::-1]))

def alternative(q,state,shared):
    tid=q['target'];fn=q['function'];pi=q.get('path_index');lookup=state['lookups'][tid];paths=state['paths'].get((tid,fn),[])
    if type(pi)is not int or pi>=len(paths):return None
    path=paths[pi]
    if not clean(path):return None
    kind=q.get('policy_basis',{}).get('basis');effect=q.get('effect',{}).get('source')
    for cert in shared.get(tid,{}).get('object_delegation_use',[]):
        if cert['function']!=fn or cert['path_index']!=pi or effect not in cert['effect_sources']:continue
        allowed=False
        if kind=='v22_source_object_authority_replacement':
            allowed=prove(lookup,path,cert['authorization'])
        elif kind in ('same_resource_guarded_operation','source_checked_M2_relation'):
            origin=q['policy_basis'].get('origin_function')
            allowed=origin in {s['function'] for s in cert['grant_sources']} and prove(lookup,path,equality(q['required_policy_candidate'],cert['grant_authority']))
        elif kind=='caller_selected_authorization_subject':allowed=object_identity_query(q,cert['owner'],lookup,path)
        if allowed:return {'decision':'source_authorized_use_not_grant_exclusive_or_caller_identity','source_certificate':copy.deepcopy(cert),'original_policy':q['required_policy_candidate']}
    # Conserved fungible transfers already have a holder-consent certificate.
    # A source argument naming that holder is an object check, not a requirement
    # that the external caller must be the holder despite valid delegation.
    if kind=='caller_selected_authorization_subject':
        for cert in shared.get(tid,{}).get('normal_transfers',[]):
            if cert['function']==fn and cert['path_index']==pi and effect in cert['effect_sources'] and object_identity_query(q,cert['holder'],lookup,path):
                return {'decision':'source_holder_identity_check_with_valid_delegation','source_certificate':copy.deepcopy(cert),'original_policy':q['required_policy_candidate']}
    return None
