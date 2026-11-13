"""Source-proved same-unit claims on a custodial token bucket."""
import copy
from .m03_p_paths import key,op,lit,conditions_possible
from .m03_p_route import keys
from .m03_p_assets import holder_path,negative,add
from .m05_state_relations import changes,compose_read
from .m05_asset_obligations import privilege,consent_model
from .m04_logic import Unsupported

def claims(lookup,program,asset):
    result=[];root=asset['balance_root']
    for fn,paths in program.items():
        for pi,p in enumerate(paths):
            if p['flow'] not in ('normal','returned') or p['issues']:continue
            updates=changes(p,lookup)
            for credit in updates:
                sel=credit['write']['path'];delta=credit['delta']
                if sel['root']!=root or not holder_path(sel,lookup) or keys(sel)[0].get('kind')!='actual_sender' or not delta or not all(c>0 for c in delta.values()):continue
                buckets=[d for d in updates if d['write']['path']['root']==root and holder_path(d['write']['path'],lookup) and d['delta']==negative(delta) and keys(d['write']['path'])[0].get('kind') in ('storage','contract_address')]
                liabilities=[d for d in updates if d['write']['path']['root']!=root and holder_path(d['write']['path'],lookup) and keys(d['write']['path'])[0].get('kind')=='actual_sender' and d['delta']==negative(delta)]
                if len(buckets)!=1 or len(liabilities)!=1 or privilege(p['guards'],lookup,root):continue
                bucket=buckets[0]['write']['path'];claim=liabilities[0]['write']['path']
                if key(bucket.get('instance'))!=key(sel.get('instance')) or key(claim.get('instance'))!=key(sel.get('instance')):continue
                result.append({'bucket':bucket,'claim':claim,'redemption_function':fn,'path_index':pi,'sources':[x['write']['source'] for x in (credit,buckets[0],liabilities[0])],'basis':'ordinary holder redeems one unit of claim for one unit from this fixed custody bucket'})
    return list({key([r['bucket'],r['claim']]):r for r in result}.values())

def inspect(lookup,program,asset,path,fn,debit,credits,amount,priv,probe,quantity):
    """A balance owned by a calling custodian can back somebody else's claim.

    Only one-to-one original-source redemption witnesses enter this consumer.
    The query requires source-solvent before-state and an uncompensated claim
    after-state, so ordinary redemption or unencumbered surplus is not guessed
    to be confiscation merely because the custodian moves its own bucket.
    """
    selector=debit['write']['path'];rows=[]
    for certificate in asset.get('custody_claim_certificates',[]):
        if key(selector)!=key(certificate['bucket']):continue
        holder={'kind':'environment','field':'custodial_beneficiary','type':'address'}
        claim=copy.deepcopy(certificate['claim']);claim['segments']=[{'key':holder}]
        after_claim=compose_read(claim,path['writes'],lookup);after_bucket=compose_read(selector,path['writes'],lookup)
        consent,consent_sources=consent_model(path,holder,amount,lookup,program,claim['root'],None)
        risk=op('and',op('or',*priv),op('!=',holder,{'kind':'actual_sender'}),op('>',claim,lit(0)),op('>=',selector,claim),op('>',after_claim,after_bucket),op('!',consent))
        # Actual outward ledger credits establish disposition; without them a
        # source ledger decrease establishes destruction of backing units.
        rule='FCR-TRANSFER' if credits else 'FCR-DESTROY'
        rows.append(probe(lookup,path['guards'],risk,{'asset':asset,'kind':'custodial_beneficiary_interference','certificate':certificate,'holder':holder,'claim_before':claim,'claim_after':after_claim,'custody_after':after_bucket,'consent_sources':consent_sources,'evaluation_terms':path.get('evaluated_terms',[])},debit['write']['source'],fn,rule))
    return rows
