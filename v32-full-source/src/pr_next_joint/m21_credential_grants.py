"""Infer a grant's subject from actual asset/permission consumption.
Recognition never requires all grant writers to be authorized already: doing
so would make malformed grants invisible. No names, labels or peer-only policy.
"""
import copy
from .core import digest
from .m03_p_paths import key,op,lit
from .m03_p_route import keys,fields,effective_permission
from .m05_state_relations import changes
from .m03_p_assets import negative
from .m05_equity_relations import linear_quantity
from .m04_logic import Unsupported

SENDER={'kind':'actual_sender'}
def family(s):return (s['root'],key(s.get('instance')),tuple(fields(s)))

def duties(context,state,shared,index):
    from .m09_shared_policy import implies
    from .m11_policy import make_query
    rows=[];limits=[]
    for tid,lookup in state['lookups'].items():
        assets=shared.get(tid,{}).get('assets',[])
        asset_families={family(a['balance_effect']['path']) for a in assets if a.get('balance_effect',{}).get('path')}
        if not asset_families:continue
        consumers={}
        for (t,fn),paths in state['paths'].items():
            if t!=tid:continue
            for pi,p in enumerate(paths):
                if p['flow'] not in ('normal','returned') or p['issues'] or p.get('evaluation_gaps'):continue
                try:
                    updates=changes(p,lookup)
                    for debit in updates:
                        balance=debit['write']['path'];bk=keys(balance);delta=debit['delta']
                        if family(balance) not in asset_families or len(bk)!=1 or not delta or any(v>0 for v in delta.values()):continue
                        holder=bk[0]
                        if holder==SENDER:continue
                        amount=linear_quantity(negative(delta))
                        for use in updates:
                            permission=use['write']['path'];pk=keys(permission)
                            if family(permission) in asset_families or len(pk)!=2 or pk[0]!=holder or pk[1]!=SENDER:continue
                            if use['delta']!=delta or not implies(lookup,p,op('>=',permission,amount)):continue
                            proof={'consumer_function':fn,'consumer_path_index':pi,'holder':holder,'spender':SENDER,
                                   'permission':permission,'amount':amount,'asset_debit':debit['write'],
                                   'permission_consumption':use['write'],'consumer_conditions':p['guards'],
                                   'scope':'same holder, caller and full amount on one source path; all writers need not already be valid'}
                            consumers.setdefault(family(permission),[]).append(proof)
                except (Unsupported,ValueError) as ex:
                    limits.append({'phase':'credential_grant_roles','target':tid,'function':fn,'path_index':pi,'reason':str(ex)})
        for r in index.by_target[tid]:
            e=r['effect'];sel=e.get('selector',{})
            if sel.get('kind')!='storage' or family(sel) not in consumers or len(keys(sel))!=2:continue
            p=state['paths'][tid,r['function']][r['path_index']]
            if p['issues'] or p.get('evaluation_gaps'):continue
            try:
                permission=keys(sel);holder=permission[0]
                # Only granting additional spending power is covered here.
                # Revocation/denial is not reintroduced as deleted AC-04D.
                write=e['original_write']
                committed=[w for w in p['writes'] if key(w['path'])==key(sel)]
                if not committed or committed[-1]['source']!=write['source']:continue
                increase=op('>',write['value'],sel)
                required=op('or',op('==',SENDER,holder),*effective_permission(p['guards'],lookup))
                q=make_query(context,tid,r['function'],r['path_index'],p,write,required,
                    {'basis':'source_holder_scoped_spending_grant','holder':holder,'delegate':permission[1],
                     'source_consumers':consumers[family(sel)],'scope':'increasing another holder spending authorization without source-qualified caller authority'},'AC-02')
                q['conditions'].append(increase);q['id']='q_'+digest(q);q['effect_id']=r['id']
                rows.append(q);index.use(r,'holder_scoped_spending_grant',q['id'])
            except (Unsupported,ValueError) as ex:
                limits.append({'phase':'credential_grant_check','target':tid,'function':r['function'],'reason':str(ex)})
    return rows,limits
