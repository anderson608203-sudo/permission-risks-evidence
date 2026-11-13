"""Source-backed exclusions for the new coverage routes, not name heuristics."""
from .m03_p_paths import key,op,lit,walk,normalize
from .m03_p_route import keys,value_type,effective_permission,selectors
from .m09_shared_policy import implies
from .m04_logic import Unsupported

def direct_lifetime_condition(condition,lookup):
    c=normalize(condition)
    if c.get('kind')=='op' and c.get('op')=='!':c=c['args'][0]
    if c.get('kind')=='storage':return value_type(c,lookup)=='bool' and not keys(c)
    if c.get('kind')!='op' or c.get('op') not in ('>=','>','<=','<','==','!='):return False
    def clock(x):
        ns=list(walk(x));return any(n.get('kind')=='environment' and n.get('field')=='timestamp' for n in ns) and all(n.get('kind') in ('op','literal','environment') for n in ns) and all(n.get('kind')!='op' or n.get('op') in ('+','-') for n in ns)
    a,b=c['args']
    return any(clock(x) and y.get('kind')=='storage' and not keys(y) and value_type(y,lookup).startswith('uint') for x,y in ((a,b),(b,a)))

def local_record_allocation(lookup,program,path,sel,chosen,role):
    if not keys(sel) or chosen.get('kind')!='actual_sender':return None
    if not implies(lookup,path,op('==',sel,lit(0))):return None
    uses={r['function'] for r in role}
    if not uses:return None
    # The recorded owner only governs replacement of that record's owner;
    # it does not establish administration over a separate asset/operation.
    evidence=[]
    for fn in uses:
        for p in program.get(fn,[]):
            if p['flow']=='reverted':continue
            if p['issues'] or p.get('evaluation_gaps') or p.get('sensitive_effects') or p.get('native_transfers'):return None
            if any(w['path']['root']!=sel['root'] for w in p['writes']):return None
            evidence.extend(w['source'] for w in p['writes'])
    return {'kind':'empty_keyed_owner_registration_with_only_local_owner_updates','selector':sel,'owner_update_sources':evidence,'scope':'source-local object registration; not a global-manager initialization'}

def managed_termination_request(lookup,program,path):
    from .m22_local_state import complete_relevant_updates,clean
    if any(n.get('nodeType')=='InlineAssembly' or n.get('memberName') in ('delegatecall','callcode') for n in walk(lookup.implementations)):return None
    for raw in path['guards']:
        flag=normalize(raw)
        if flag.get('kind')!='storage' or keys(flag) or value_type(flag,lookup)!='bool':continue
        if not complete_relevant_updates(lookup,program,[flag['root']]):continue
        writers=[];unsafe=False
        for fn,ps in program.items():
            for p in ps:
                if p['flow']=='reverted':continue
                for w in p['writes']:
                    if key(w['path'])!=key(flag):continue
                    if not clean(p):unsafe=True;continue
                    if w['value']==lit(False):continue
                    # A protected management action explicitly arms shutdown.
                    # The later caller merely completes that authorized request.
                    if w['value']!=lit(True) or not effective_permission(p['guards'],lookup):unsafe=True;continue
                    writers.append({'function':fn,'source':w['source'],'authority':effective_permission(p['guards'],lookup)})
        if writers and not unsafe:return {'kind':'source_management_arms_public_termination','flag':flag,'protected_arming_writers':writers,'scope':'explicit source shutdown request; no payout/settlement safety conclusion'}
    return None
