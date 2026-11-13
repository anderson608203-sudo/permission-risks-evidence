"""Cross-branch settlement of the identical user request before/after a configuration write."""
from collections import defaultdict
from .m03_p_paths import key,lit,op,walk
from .m03_p_route import selectors,keys,fields,value_type
from .m04_logic import Unsupported
from .m05_asset_obligations import privilege
from .m05_state_relations import compose_read
from .m20_sequence import qualify,read,request_states
from .m22_assets import matches
from .m27_effect_checks import SENDER,committed,operations,settlement_loss

def switched_requests(tid,lookup,program,index,asset):
    from .m08_financial import probe
    rows=[];notes=[];visited=set()
    # Only compare actual opposite outcomes at the very same source branch.
    branches=defaultdict(lambda:{True:[],False:[]})
    for fn,i in operations(index,tid,asset):
        p=program[fn][i]
        if not committed(p) or p.get('native_transfers') or p.get('sensitive_effects'):continue
        for b in p.get('branch_choices',[]):
            # A plain scalar management setting; never treat balance or supply
            # itself as an administrative switch.
            ss=selectors(b['condition'])
            if len(ss)!=1 or ss[0].get('segments') or ss[0].get('instance'):continue
            if ss[0]['root'] in (asset['balance_root'],asset.get('supply_root')):continue
            if value_type(ss[0],lookup) not in ('bool','uint','uint256'):continue
            branches[(fn,b['source']['ast_id'],key(b['condition']),ss[0]['root'])][bool(b['sign'])].append(i)
    for (fn,site,_,root),sides in branches.items():
        if not sides[True] or not sides[False]:continue
        for rec in index.writers.get((tid,root,()),[]):
            writer=rec['function'];wi=rec['path_index'];s=program[writer][wi]
            if writer==fn or not committed(s) or s.get('native_transfers') or s.get('sensitive_effects'):continue
            if len(s['writes'])!=1 or s['writes'][0]['path'].get('segments') or s['writes'][0]['path'].get('instance'):continue
            perms=privilege(s['guards'],lookup,asset['balance_root'])
            if not perms:continue
            step=qualify(s,1);sw=step['writes']
            if len(sides[True])*len(sides[False])>16:
                notes.append({'phase':'financial_parameter_check','function':fn,'reason':'opposite_committed_path_pair_bound_16'});continue
            for sign in (True,False):
                for ai in sides[sign]:
                    for bi in sides[not sign]:
                        a,b=program[fn][ai],program[fn][bi]
                        ident=(writer,wi,fn,ai,bi)
                        if ident in visited:continue
                        visited.add(ident)
                        try:
                            source=rec['effect']['source']
                            cond=[*step['guards'],qualify(op('or',*perms),1),op('!=',qualify(SENDER,1),SENDER),
                                  *a['guards'],*read(b['guards'],sw,lookup)]
                            # Same callee, caller, amount and recipient across
                            # worlds. The material difference must follow the switch.
                            cells={key(w['path']):w['path'] for w in a['writes']+b['writes'] if matches(w['path'],asset)}
                            for cell in cells.values():
                                prior=compose_read(cell,a['writes'],lookup)
                                _,next_value=request_states(compose_read(cell,b['writes'],lookup),sw,lookup)
                                if prior==next_value:continue
                                meta={'kind':'parameter_switches_settlement_path','setter':writer,'consumer':fn,'branch_source_ast_id':site,
                                      'setter_source':source,'old_path':ai,'new_path':bi,'account':cell,'before':prior,'after':next_value,
                                      'evaluation_terms':step.get('evaluated_terms',[])+a.get('evaluated_terms',[])+read(b.get('evaluated_terms',[]),sw,lookup)}
                                obs=probe(lookup,cond,op('!=',prior,next_value),dict(meta),source,fn,'parameter_influence')
                                notes.append({'phase':'financial_parameter_check','mechanism_only':True,'check':obs})
                                index.use(rec,'source_switch_between_request_paths',reason=obs['formal']['query'])
                                if obs['reportable']:
                                    risk=settlement_loss(lookup,program,asset,b,fn,cell,prior,next_value,sw,cond,meta,baseline=a)
                                    if risk:rows.append(risk)
                        except Unsupported as ex:notes.append({'phase':'financial_parameter_check','function':fn,'reason':str(ex)})
    return rows,notes
