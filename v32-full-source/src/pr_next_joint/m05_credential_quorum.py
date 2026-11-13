"""Bounded duplicate-approval queries over source-recovered signers."""
from .m03_p_paths import key,walk
from .m03_p_route import keys,value_type
from .m05_mechanism_core import scalar_write,solve

def check_quorum(obligation,lookup,fn,path,pi,credentials,same_payload,nonce_bookkeeping):
    if not 2<=len(credentials)<=8:return []
    effects=[scalar_write(w,lookup) for w in path['writes'] if value_type(w['path'],lookup)!='bool']
    effects=[w for w in effects if not any(nonce_bookkeeping(w,c,path['guards']) or
             any(key(s)==key(w['path']) for s in walk(c['digest'])) for c in credentials)]
    rows=[]
    for effect in effects:
        for i in range(len(credentials)):
            for j in range(i+1,len(credentials)):
                left,right=credentials[i],credentials[j]
                model={'kind':'credential_duplicate_signer_acceptance','function':fn,'path_index':pi,
                       'recovered_signers':credentials,'duplicated_pair':[i,j],'effect':effect,'conditions':path['guards'],
                       'same_payload_certificate':True,
                       'graph':{'engine':'source relationship graph','edges':[['source_recoveries',fn,'accepted_in_same_path'],[fn,str(effect['path']['root']),'protected_effect']]},
                       'assumptions':['source requires several credential recoveries; they are hypothesized to represent distinct approvals',
                                      'one valid issued credential may be presented twice, with exactly the same payload and signature',
                                      'conditional source state, no cryptographic forgery or deployment reachability proof'],
                       'unchecked_dimensions':['general threshold/quorum specification','cryptographic_validity','expiry_intent']}
                def construct(e, inputs):
                    credentials=inputs['recovered_signers']; pair=inputs['duplicated_pair']
                    left,right=[credentials[k] for k in pair]
                    effect=inputs['effect']; path={'guards':inputs['conditions']}
                    z=e.z;equal=same_payload(e,left,right)
                    return z.And(*[e.expr(g) for g in path['guards']],*[e.expr(c)!=0 for c in credentials],
                                 e.expr(effect['value'])!=e.expr(effect['path'])),equal
                rows.append(solve(lookup,obligation,fn,model,construct,effect['path']['root'],keys(effect['path'])[0] if keys(effect['path']) else None))
    return rows
