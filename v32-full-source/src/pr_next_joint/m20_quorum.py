"""Source certificates for explicit count/unique-approver quorums.
A bitset, arbitrary threshold specification or cryptographic protocol that
cannot be lowered is a local limitation, never an inferred normal certificate.
"""
import copy
from .m03_p_paths import key,op,lit,walk
from .m03_p_route import keys,fields,selectors,effective_permission,value_type,relocate
from .m03_p_assets import polynomial
from .m09_shared_policy import implies
from .m04_logic import Unsupported
SENDER={'kind':'actual_sender'}

def same_family(a,b):
    return a.get('kind')=='storage' and b.get('kind')=='storage' and a['root']==b['root'] and fields(a)==fields(b) and key(a.get('instance'))==key(b.get('instance'))

def certificate(lookup,program,fn,pi,path,index=None):
    cache=getattr(lookup,'_v20_quorum_cache',None)
    if cache is None:cache={};lookup._v20_quorum_cache=cache
    ck=(fn,pi)
    if ck in cache:return copy.deepcopy(cache[ck])
    cache[ck]=None
    if path['issues'] or path.get('evaluation_gaps'):return None
    comparisons=[n for g in path['guards'] for n in walk(g)
        if n.get('kind')=='op' and n.get('op') in ('>=','==','>') and len(n.get('args',[]))==2]
    for compare in comparisons:
        count,threshold=compare['args']
        if count.get('kind')!='storage' or not keys(count) or value_type(count,lookup) not in ('uint','uint256'):continue
        if any(n.get('kind') in ('actual_sender','parameter','unknown') for n in walk(threshold)):continue
        try:
            if not implies(lookup,path,compare) or not implies(lookup,path,op('>',threshold,lit(0))):continue
            confirmations=[];bad=False
            for approval,paths in program.items():
                for ai,p in enumerate(paths):
                    if p['flow']=='reverted':continue
                    for w in p['writes']:
                        if not same_family(w['path'],count):continue
                        if p['issues'] or p.get('evaluation_gaps'):bad=True;break
                        # Consumption/reset does not manufacture approval counts.
                        if w['value']==lit(0):continue
                        delta=polynomial(op('-',w['value'],w['path']))
                        if delta!={'#':1}:bad=True;break
                        perms=effective_permission(p['guards'],lookup)
                        if not perms:bad=True;break
                        markers=[]
                        for seen in p['writes']:
                            if seen['value']!=lit(True) or value_type(seen['path'],lookup)!='bool':continue
                            sk=keys(seen['path']);ckeys=keys(w['path'])
                            if len(sk)!=len(ckeys)+1 or sk[-1]!=SENDER or key(sk[:-1])!=key(ckeys):continue
                            if not implies(lookup,p,op('!',seen['path'])):continue
                            # No public reset may enable duplicate approvals before execution.
                            untrusted_reset=False
                            for reset_fn,reset_paths in program.items():
                                for reset in reset_paths:
                                    if reset['flow']=='reverted':continue
                                    for rw in reset['writes']:
                                        if not same_family(rw['path'],seen['path']) or rw['value']==lit(True):continue
                                        # A reset must also reset this operation's count and
                                        # preserve object identity, otherwise no quorum proof.
                                        resetcounts=[cw for cw in reset['writes'] if same_family(cw['path'],count) and cw['value']==lit(0)
                                            and key(keys(cw['path']))==key(keys(rw['path'])[:-1])]
                                        if not resetcounts or reset['issues'] or reset.get('evaluation_gaps'):untrusted_reset=True
                            if not untrusted_reset:markers.append(seen)
                        if not markers:bad=True;break
                        confirmations.append({'function':approval,'path_index':ai,'counter':w['path'],
                            'counter_write':w['source'],'approver_conditions':perms,'deduplication_marker':markers[0]['path'],
                            'deduplication_source':markers[0]['source'],'operation_keys':keys(w['path'])})
                    if bad:break
                if bad:break
            if bad or not confirmations:continue
            result={'kind':'source_counted_distinct_qualified_approvals','function':fn,'path_index':pi,
                'execution_threshold':compare,'counter':count,'operation_keys':keys(count),
                'confirmations':confirmations,'initial_count_assumption':'conditional source state; deployment/history not proved',
                'scope':'counter updates, approver checks, duplicate marker and matching object keys; not arbitrary quorum intent'}
            cache[ck]=result
            return copy.deepcopy(result)
        except (Unsupported,ValueError,KeyError):continue
    return None
