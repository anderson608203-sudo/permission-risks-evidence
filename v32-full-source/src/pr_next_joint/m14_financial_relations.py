from .m20_solver import solve as bounded_solve
"""M2 locates field-ledger relations; original-source effects certify them."""
import copy
from .core import digest
from .m03_p_paths import key,op,lit,conditions_possible
from .m03_p_route import keys,fields,selectors
from .m03_p_assets import add,negative,term
from .m05_state_relations import changes
from .m13_financial_relations import component_shape
from .m04_logic import Unsupported

def feasible_transfer(lookup,path,debit,credits):
    from .m05_mechanism_core import MechanismEncoder
    from .m08_financial import quantity
    enc=MechanismEncoder(lookup);z=enc.z
    try:
        for value in path.get('evaluated_terms',[]):enc.expr(value)
        guards=[enc.expr(g) for g in path['guards']]
        amount=enc.expr(quantity(negative(debit['delta'])))
        holder=enc.expr(keys(debit['write']['path'])[0])
        recipients=[enc.expr(keys(d['write']['path'])[0]) for d in credits]
        # Preserve actual final writes and type/overflow constraints, not only delta names.
        for d in [debit]+credits:
            enc.expr(d['write']['path']);enc.expr(d['write']['value'])
        solver=z.Solver();solver.set(timeout=3000)
        solver.add(*enc.constraints,*guards,amount>0,z.Or(*[holder!=r for r in recipients]))
        answer=bounded_solve(solver)
        if answer!=z.sat or enc.abstract_hash_used:return None
        return {'basis':'feasible_positive_conserved_source_transfer','result':'sat',
            'formula_sha256':digest(solver.to_smt2()),'path_conditions':copy.deepcopy(path['guards']),
            'source_effects':[d['write']['source'] for d in [debit]+credits],
            'source_prestate_is_conditional':True}
    except Unsupported:return None

def proposed_field_models(lookup,program,hints):
    static=hints is None
    if static:
        hints=[{'kind':'holder_of','id':None,'functions':list(program),'resource_root':None,
                'resource_roots':sorted({w['path']['root'] for ps in program.values() for p in ps for w in p['writes'] if fields(w['path'])})}]
    found={}
    for h in hints:
        if h['kind'] not in ('holder_of','guards_transfer','credits_from_deposit','debits_for_redemption'):continue
        for fn in h['functions']:
            for pi,p in enumerate(program.get(fn,[])):
                if p['flow'] not in ('normal','returned') or p['issues'] or p.get('evaluation_gaps') or p.get('native_transfers'):continue
                groups={}
                for d in changes(p,lookup):
                    sel=d['write']['path'];shape=component_shape(sel,lookup)
                    if sel['root'] not in h.get('resource_roots',[h['resource_root']]) or not fields(sel) or shape is None:continue
                    groups.setdefault(shape,[]).append(d)
                for shape,ds in groups.items():
                    if any(d['delta'] is None for d in ds):continue
                    ds=[d for d in ds if d['delta']]
                    debits=[d for d in ds if all(v<0 for v in d['delta'].values())]
                    credits=[d for d in ds if all(v>0 for v in d['delta'].values())]
                    total={}
                    for d in ds:total=add(total,d['delta'])
                    if len(debits)!=1 or not credits or len(ds)!=len(debits)+len(credits) or total!={}:continue
                    debit=debits[0];sel=debit['write']['path'];holder=keys(sel)[0]
                    from .m15_relations import financial_scope
                    if not static and not financial_scope(h,p,fn,sel,lookup,amount=term(negative(debit['delta'])),recipients=[keys(d['write']['path'])[0] for d in credits]):continue
                    if term(negative(debit['delta'])) is None:continue
                    if any(key(keys(d['write']['path'])[0])==key(holder) for d in credits):continue
                    distinct=op('or',*[op('!=',holder,keys(d['write']['path'])[0]) for d in credits])
                    if not conditions_possible(p['guards']+[distinct]):continue
                    certificate=feasible_transfer(lookup,p,debit,credits)
                    if certificate is None:continue
                    model={'kind':'source_checked_semantic_transferable_field','balance_root':sel['root'],
                        'supply_root':None,'supply_effect':None,'balance_effect':copy.deepcopy(debit['write']),
                        'transfer_credits':[copy.deepcopy(d['write']) for d in credits],
                        'transfer_function':fn,'path_index':pi,'conditions':copy.deepcopy(p['guards']),
                        'relation_id':h['id'],'relation_ids':[] if static else [h['id']],'financial_certificate':certificate,
                        'field_ledger_shape':shape,'unit_relation':'same-source conserved transferable field units',
                        'basis':('source effect inventory' if static else 'M2 locates function/root')+'; source confirms same-field debit and distinct-holder credit, conserved quantity and instance',
                        'scope':'conditional transferable field; no market value or deployed-prestate claim'}
                    model['id']='asset_'+digest([shape,fn,pi])
                    if shape in found and not static:found[shape]['relation_ids']=sorted(set(found[shape]['relation_ids']+[h['id']]))
                    else:found[shape]=model
    return list(found.values())

def require_field_guard_scope(path,asset,lookup):
    if not asset.get('field_ledger_shape'):return
    # Root equality alone cannot erase consent stored in a sibling struct field.
    allowed={asset['field_ledger_shape']}|set(asset.get('equity_certificate',{}).get('component_shapes',[]))
    for sel in selectors(path['guards']):
        if sel['root']==asset['balance_root'] and component_shape(sel,lookup) not in allowed:
            raise Unsupported('field_ledger_sibling_guard_requires_consent_model')
