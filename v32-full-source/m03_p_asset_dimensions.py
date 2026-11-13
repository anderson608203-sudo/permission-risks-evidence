"""Finite ledger dimensions, retaining the exact redemption domain."""
import copy,re
from .core import digest
from .m03_p_paths import key
from .m03_p_route import keys,fields,value_type

def uint_name(node):
    name=node.get('name','');match=re.fullmatch(r'uint(\d*)',name)
    if not match:return None
    bits=int(match[1] or 256)
    return name if 8<=bits<=256 and bits%8==0 else None

def ledger_projection(selector,lookup,allow_nested=False):
    if selector.get('kind')!='storage' or fields(selector):return None
    if any('key' not in s for s in selector.get('segments',[])):return None
    declared=lookup.nodes.get(selector['root'],{}).get('typeName',{});typ=declared
    indices=keys(selector);key_types=[]
    for _ in indices:
        if typ.get('nodeType')!='Mapping':return None
        key_types.append(typ.get('keyType',{}).get('name'));typ=typ.get('valueType',{})
    if not uint_name(typ):return None
    if len(indices)==1 and key_types[0] in ('address','address payable'):position=0
    elif allow_nested and len(indices)==2 and uint_name(declared.get('keyType',{})) and key_types[1] in ('address','address payable'):position=1
    else:return None
    return {'holder':copy.deepcopy(indices[position]),'holder_index':position,
        'asset_keys':copy.deepcopy(indices[:position]),'asset_key_types':key_types[:position],
        'instance':copy.deepcopy(selector.get('instance')),'value_type':value_type(selector,lookup)}

def nested_asset_models(lookup,program):
    from .m03_p_assets import deltas,polynomial,negative,term,unsafe_integer_cast
    from .m03_p_paths import conditions_possible
    models=[]
    for fn,branches in program.items():
        for pi,path in enumerate(branches):
            if path['flow'] not in ('normal','returned') or path['issues'] or unsafe_integer_cast(path,lookup):continue
            updates=deltas(path)
            for payment in path.get('native_transfers',[]):
                if payment['recipient'].get('kind')!='actual_sender':continue
                amount=polynomial(payment['amount'])
                if not amount or term(amount) is None or conditions_possible(path['guards'],payment['success']):continue
                for balance in updates:
                    sel=balance['write']['path'];projection=ledger_projection(sel,lookup,True)
                    if not projection or projection['holder_index']!=1 or projection['holder'].get('kind')!='actual_sender' or balance['delta']!=negative(amount):continue
                    for supply in updates:
                        ss=supply['write']['path'];typ=lookup.nodes.get(ss['root'],{}).get('typeName',{})
                        if (supply['delta']!=negative(amount) or fields(ss) or len(keys(ss))!=1
                                or typ.get('nodeType')!='Mapping' or uint_name(typ.get('keyType',{}))!=projection['asset_key_types'][0]
                                or not uint_name(typ.get('valueType',{})) or key(keys(ss))!=key(projection['asset_keys'])):continue
                        witness=copy.deepcopy({'function':fn,'path_index':pi,'path':path,
                            'asset_keys':projection['asset_keys'],'holder':projection['holder'],'quantity':payment['amount'],
                            'balance_write':balance['write'],'supply_write':supply['write'],'payment':payment})
                        witness['id']=digest(witness)
                        models.append({'balance_root':sel['root'],'supply_root':ss['root'],
                            'basis':'same_asset_same_holder_native_redemption_with_matching_supply_reduction',
                            'redemption_function':fn,'path_index':pi,'balance_effect':balance['write'],
                            'supply_effect':supply['write'],'native_payment':payment,'conditions':path['guards'],
                            'unit_relation':'one ledger unit to one native value unit in this source path',
                            'ledger_shape':{'holder_index':1,'asset_key_types':projection['asset_key_types'],
                                'balance_instance':sel.get('instance'),'supply_instance':ss.get('instance')},
                            'financial_scope_witness':witness,
                            'scope':'exact retained redemption domain, asset, holder and amount; no generalization to other asset IDs or deployment'})
    return list({digest(m):m for m in models}.values())
