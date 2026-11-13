"""Directed source checks. Endpoint proposals guide checking, never grant permission."""
import copy
from .m03_p_paths import key,op
from .m03_p_route import selectors,keys
from .m05_state_relations import changes
from .m03_p_assets import negative,holder_path
from .m09_shared_policy import implies
from .m04_logic import Unsupported

def grant_from_endpoints(lookup,program,assets,source,dest,compiled):
    from .m05_asset_obligations import consent_model
    from .m13_financial_relations import component_updates,component_holder
    from .m15_relations import financial_scope
    candidates=[]
    for pi,path in enumerate(program.get(dest,[])):
        if path['flow'] not in ('normal','returned') or path['issues'] or path.get('evaluation_gaps'):continue
        for asset in assets:
            try:
                updates=component_updates(path,lookup,asset)
                debits=[d for d in updates if d['delta'] and all(v<0 for v in d['delta'].values())]
                if len(debits)!=1:continue
                debit=debits[0];sel=debit['write']['path']
                if not component_holder(sel,asset,lookup):continue
                holder=keys(sel)[0];amount=negative(debit['delta'])
                credits=[d for d in updates if d['delta'] and all(v>0 for v in d['delta'].values()) and component_holder(d['write']['path'],asset,lookup)]
                recipient=keys(credits[0]['write']['path'])[0] if len(credits)==1 else None
                from .m03_p_assets import term
                if not financial_scope({'scoped_relation':compiled},path,dest,sel,lookup,term(amount),[recipient] if recipient else []):continue
                consent,evidence=consent_model(path,holder,amount,lookup,program,asset['balance_root'],asset.get('supply_root'),recipient=recipient,sufficient_only=True)
                if not implies(lookup,path,consent):continue
                normal={'function':dest,'path_index':pi,'root':asset['balance_root'],'instance':sel.get('instance'),
                    'kind':'source_verified_directed_authorized_debit','holder':holder,'total_debit':amount,
                    'consent':consent,'consent_sources':evidence,'effect_sources':[debit['write']['source']],
                    'relation_ids':[compiled['relation_id']]}
                cert=match_grant(program,source,normal)
                if cert:candidates.append(cert)
            except (Unsupported,ValueError) as ex:
                compiled.setdefault('local_check_limits',[]).append({'kind':'authorization_use','function':dest,'path_index':pi,'reason':str(ex)})
    return candidates

def match_grant(program,source,normal):
    sender={'kind':'actual_sender'}
    roots={s['root'] for s in selectors(normal.get('consent_sources',[]))}
    for pi,path in enumerate(program.get(source,[])):
        if path['flow'] not in ('normal','returned') or path['issues'] or path.get('evaluation_gaps'):continue
        for write in path['writes']:
            ks=keys(write['path'])
            if (write['path']['root'] in roots and len(ks)==2 and ks[0]==sender and ks[1].get('kind')=='parameter'
                and any(setter['function']==source and setter['source']==write['source'] for item in normal.get('consent_sources',[]) for setter in item.get('holder_controlled_setters',[]))):
                return {'kind':'source_grant_and_consumed_delegation','grant_source':write['source'],'grant_path_index':pi,'use_certificate':copy.deepcopy(normal)}
    return None

def exact_consent(compiled_links,fn,pi,selector,amount,source):
    """Reuse only the proved debit, not every action in a function or contract."""
    for link in compiled_links:
        if link.get('kind')!='authorization_use' or link.get('status')!='program_verified':continue
        normal=link['certificate']['use_certificate']
        if (normal['function']==fn and normal['path_index']==pi and normal['root']==selector['root']
            and key(normal.get('instance'))==key(selector.get('instance')) and key(normal['holder'])==key(keys(selector)[0])
            and normal['total_debit']==amount and source in normal['effect_sources']):
            return copy.deepcopy(normal['consent']),copy.deepcopy(normal['consent_sources']),link
    return None
