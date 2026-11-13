"""Read-over-write with source-key equality; no arbitrary alias assumptions."""
import copy
from .m03_p_paths import key,op,lit,normalize,conditions_possible

def read_after_writes(selector,writes,guards):
    value=selector
    # Only direct equality facts are needed to simplify a key alias. Omitting
    # other guards is conservative: retain an ite when equality is not proved.
    equalities=[]
    def collect(g):
        if g.get('kind')=='op' and g.get('op') in ('and','&&'):
            for a in g['args']:collect(a)
        elif g.get('kind')=='op' and g.get('op') in ('==','!=') and all(a.get('kind') in ('actual_sender','parameter','literal','contract_address') for a in g['args']):equalities.append(g)
        elif g.get('kind')=='op' and g.get('op')=='!' and g['args'][0].get('kind')=='op' and g['args'][0].get('op') in ('==','!='):
            a=g['args'][0]
            if all(x.get('kind') in ('actual_sender','parameter','literal','contract_address') for x in a['args']):equalities.append(g)
    for g in guards:collect(g)
    for w in writes:
        p=w['path']
        if p['root']!=selector['root'] or key(p.get('instance'))!=key(selector.get('instance')):continue
        if [{k:v for k,v in x.items() if k!='key'} for x in p.get('segments',[])]!=[{k:v for k,v in x.items() if k!='key'} for x in selector.get('segments',[])]:continue
        a=[s['key'] for s in selector.get('segments',[]) if 'key' in s];b=[s['key'] for s in p.get('segments',[]) if 'key' in s]
        if len(a)!=len(b):continue
        if key(p)==key(selector):value=w['value'];continue
        same=normalize(op('and',*[op('==',x,y) for x,y in zip(a,b)]))
        if not conditions_possible(equalities,same):value=w['value']
        elif not conditions_possible(equalities+[same]):continue
        else:value=op('ite',same,copy.deepcopy(w['value']),value)
    return copy.deepcopy(value)
