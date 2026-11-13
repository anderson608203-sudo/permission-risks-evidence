"""Privileged whole-contract destruction in the explicitly approved comparison EVM."""
import copy
from .m03_p_paths import op,lit,key
from .m03_p_route import keys
from .m03_p_assets import holder_path
from .m05_asset_obligations import privilege
from .m04_logic import Unsupported

def analyze(lookup,program,assets,probe,rows,limitations):
    from .effective_parameters import current
    environment=current()['fcr_execution_environment']
    for fn,paths in program.items():
        for pi,path in enumerate(paths):
            if path['flow'] not in ('normal','returned') or path['issues']:continue
            for effect in path.get('sensitive_effects',[]):
                if effect.get('kind')!='native_selfdestruct':continue
                for asset in assets:
                    if asset['balance_effect']['path'].get('instance'):continue
                    if not holder_path(asset['balance_effect']['path'],lookup):continue
                    priv=privilege(path['guards'],lookup,asset['balance_root'])
                    if not priv:continue
                    # This is an existential holder of an established transferable
                    # ledger, not an invented function argument or initialized fund.
                    holder={'kind':'environment','field':'existing_financial_holder','type':'address'}
                    balance={'kind':'storage','root':asset['balance_root'],'segments':[{'key':holder}]}
                    conditions=[op('or',*priv),op('!=',holder,{'kind':'actual_sender'}),op('!=',holder,lit(0)),op('>',balance,lit(0))]
                    metadata={'asset':asset,'kind':'privileged_whole_contract_destruction','effect':effect,
                        'holder':holder,'affected_balance':balance,'execution_environment':environment,
                        'environment_basis':'user-approved JANUS comparison assumption; not compiler-version inference',
                        'modern_evm_limit':'under EIP-6780, code/storage survive unless created in the same transaction',
                        'prestate_limit':'conditional existing holder balance; deployment/reachability not established',
                        'evaluation_terms':path.get('evaluated_terms',[])}
                    try:
                        rule='FCR-DESTROY' if environment=='janus_comparison_pre_eip_6780' else 'EXT-FCR-CONTRACT-DESTRUCTION-CONDITIONAL'
                        rows.append(probe(lookup,path['guards'],op('and',*conditions),metadata,effect['source'],fn,rule))
                    except Unsupported as ex:limitations.append({'function':fn,'path':pi,'asset':asset['balance_root'],'reason':str(ex),'effect':'selfdestruct'})
