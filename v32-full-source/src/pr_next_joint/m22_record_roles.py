"""Source-qualified record roles shared by AC authorization and FCR effects.
Roles are evidence about use, never names or predicted risk labels.
"""
import copy
from .m03_p_paths import key,walk,normalize,op,lit
from .m03_p_route import keys,fields,selectors,value_type
from .m04_logic import Unsupported
SENDER={'kind':'actual_sender'}

def shape(sel):
    return key([sel.get('root'),fields(sel),sel.get('instance'),len(keys(sel))])

def clean(p):
    return p['flow'] in ('normal','returned') and not p['issues'] and not p.get('evaluation_gaps')

def _numeric_comparison(e,lookup):
    e=normalize(e)
    if e.get('kind')!='op' or e.get('op') not in ('>=','>','<=','<','=='):return None
    args=e.get('args',[])
    if len(args)!=2:return None
    for a,b in (args,args[::-1]):
        if a.get('kind')!='storage' or len(keys(a))!=1 or keys(a)[0]!=SENDER:continue
        if not str(value_type(a,lookup)).startswith(('uint','enum ')):continue
        if b.get('kind')=='literal' and type(b.get('value')) is int and b['value']>0:return a,b
        if b.get('kind')=='enum_value':return a,b
        if b.get('kind')=='storage' and not keys(b) and str(value_type(b,lookup)).startswith(('uint','enum ')):return a,b
    return None

def catalog(lookup,program,assets=()):
    """Recognize non-monetary uses conservatively, keeping complete field identity."""
    from .m05_state_relations import changes
    from .m03_p_assets import negative
    from .m03_p_route import effective_permission
    paths=[(f,i,p) for f,ps in program.items() for i,p in enumerate(ps) if p['flow'] in ('normal','returned')]
    candidates={};uses={};unsafe=set();updates_by_path={}
    def put(sel,kind,evidence):
        if sel.get('kind')!='storage' or len(keys(sel))!=1 or not str(value_type(sel,lookup)).startswith(('uint','enum ')):return
        sh=shape(sel);candidates.setdefault(sh,{'selector':copy.deepcopy(sel),'roles':set(),'evidence':[]})
        candidates[sh]['roles'].add(kind);candidates[sh]['evidence'].append(evidence)
    for f,pi,p in paths:
        for g in p['guards']:
            for e in walk(g):
                n=_numeric_comparison(e,lookup)
                if n:put(n[0],'numeric_authorization',{'function':f,'path_index':pi,'condition':e,'threshold':n[1]})
                if e.get('kind')=='op' and e.get('op') in ('>=','>','<=','<','=='):
                    a=e.get('args',[])
                    if len(a)==2:
                        for record,clock in (a,a[::-1]):
                            if record.get('kind')=='storage' and clock.get('kind')=='environment' and clock.get('field') in ('timestamp','number'):
                                put(record,'time_control',{'function':f,'path_index':pi,'condition':e})
        if not clean(p):continue
        try:updates=changes(p,lookup);updates_by_path[id(p)]=updates
        except (Unsupported,ValueError):updates_by_path[id(p)]=None;continue
        for d in updates:
            sel=d['write']['path']
            if not d['delta'] or not all(v<0 for v in d['delta'].values()):continue
            other=[x for x in updates if shape(x['write']['path'])!=shape(sel) and x['delta']==d['delta']]
            if not other:continue
            for a in assets:
                matching=[x for x in other if shape(x['write']['path'])==shape(a['balance_effect']['path'])]
                if not matching:continue
                # Quota and actual debit belong to the same source holder.
                if any(key(keys(x['write']['path']))!=key(keys(sel)) for x in matching):continue
                guards=[g for g in p['guards'] if any(shape(x)==shape(sel) for x in selectors(g))]
                if guards:put(sel,'transfer_quota',{'function':f,'path_index':pi,'quota_debit':d['write']['source'],
                    'asset_debits':[x['write']['source'] for x in matching],'asset_selector':a['balance_effect']['path'],'conditions':guards})
    financial={shape(a['balance_effect']['path']) for a in assets}
    for f,pi,p in paths:
        touched={shape(x) for x in selectors(p.get('guards',[])+p.get('evaluated_terms',[])+p.get('writes',[]))}
        if not clean(p):unsafe.update(touched & set(candidates))
        for effect in p.get('native_transfers',[])+p.get('sensitive_effects',[]):
            for x in selectors([effect.get('amount',{}),effect.get('value',{}),effect.get('recipient',{})]):
                unsafe.add(shape(x))
        for update in p['writes']:
            # Feeding a different data record is not a pure control use.
            target=shape(update['path'])
            unsafe.update(shape(x) for x in selectors(update['value']) if shape(x)!=target)
    result={}
    for sh,c in candidates.items():
        if sh in financial or sh in unsafe:continue
        from .m05_writer_scope import gaps_for
        if gaps_for(lookup,{c['selector']['root']}):continue
        writers=[{'function':f,'path_index':pi,'source':x['source'],'conditions':p['guards']}
            for f,pi,p in paths for x in p['writes'] if shape(x['path'])==sh]
        # Authorization also needs a source management operation. Mere balance
        # comparisons at a spending site are not privileged membership.
        if 'numeric_authorization' in c['roles']:
            # A quantity consumed or accumulated in place may be a balance or
            # quota. Its numeric comparison alone does not establish a rank.
            quantity_updates=[w for _,_,p in paths for w in p['writes'] if shape(w['path'])==sh and any(shape(x)==sh for x in selectors(w['value'])) and key(w['path'])!=key(w['value'])]
            if quantity_updates:
                control_uses=[p for _,_,p in paths if clean(p) and (p['writes'] or p.get('sensitive_effects')) and any(_numeric_comparison(e,lookup) and shape(_numeric_comparison(e,lookup)[0])==sh for g in p['guards'] for e in walk(g))]
                decrements=[]
                for _,_,p in paths:
                    if not clean(p):continue
                    try:
                        cached=updates_by_path.get(id(p))
                        if cached is None:raise Unsupported('source quantity updates unavailable')
                        decrements.extend(d for d in cached if shape(d['write']['path'])==sh and (d['delta'] is None or any(v<0 for v in d['delta'].values())))
                    except (Unsupported,ValueError):decrements.append(None)
                if not control_uses or decrements:c['roles'].remove('numeric_authorization')
        if 'numeric_authorization' in c['roles']:
            managed=[]
            for f,pi,p in paths:
                ws=[x for x in p['writes'] if shape(x['path'])==sh]
                if not ws or not clean(p):continue
                perms=effective_permission(p['guards'],lookup)
                if perms:managed.extend({'function':f,'source':x['source'],'authorization':perms} for x in ws)
            if not managed:c['roles'].remove('numeric_authorization')
            else:c['management_evidence']=managed
        if c['roles']:
            c['roles']=sorted(c['roles']);c['writers']=writers
            c['basis']='compiled source use/field/effect relationships; no identifier-name test'
            result[sh]=c
    return result

def prepare(state):
    certificates={}
    for tid,lookup in state['lookups'].items():
        program={f:ps for (t,f),ps in state['paths'].items() if t==tid}
        c=catalog(lookup,program)
        lookup._source_record_roles=c
        lookup._effective_permission_cache={}
        certificates[tid]=c
    state['_source_record_roles']=certificates

def numeric_atom(expr,lookup):
    n=_numeric_comparison(expr,lookup)
    if not n:return False
    c=getattr(lookup,'_source_record_roles',{}).get(shape(n[0]))
    return bool(c and 'numeric_authorization' in c['roles'])

def exclusion(selector,lookup,program,assets):
    cache=getattr(lookup,'_account_record_role_cache',None)
    if cache is None:
        cache=catalog(lookup,program,assets);lookup._account_record_role_cache=cache
    sh=shape(selector)
    if sh not in cache:
        from .m23_record_roles import time_record
        certificate=time_record(selector,lookup,assets)
        cache[sh]=certificate
    return copy.deepcopy(cache.get(sh))
