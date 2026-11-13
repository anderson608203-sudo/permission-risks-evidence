"""Small source certificates for related financial roots, never LLM verdicts."""
import copy
from .m03_p_paths import key,walk,op,lit
from .m03_p_route import keys,selectors,value_type
from .m03_p_assets import polynomial,add,negative,holder_path
from .m05_state_relations import changes

def equity_components(lookup,program,assets,hints):
    """ERC balance accessor + actual same-holder conversion + transferable root.

    An arbitrary sum/getter or unrelated two-asset conversion is insufficient.
    Keep source accessor and conversion witnesses and the unit assumption visible.
    """
    result=[];known={a['balance_root']:a for a in assets}
    accessors={fn:ps for fn,ps in program.items() if fn=='balanceOf(address)' and ps}
    if not accessors and 'balanceOf(address)' in lookup.abi:
        try:accessors['balanceOf(address)']=lookup.run('balanceOf(address)')
        except (ValueError,KeyError,TypeError):accessors={}
    # Explicit source endpoints can locate nonstandard summaries. No name guesses.
    proposed={}
    for hint in hints:
        for fn in hint.get('functions',[]):
            body=lookup.function(fn)
            if not body or body.get('generated_getter'):continue
            from .source_entry_identity import function_mutability
            params=body.get('parameters',{}).get('parameters',[])
            returns=body.get('returnParameters',{}).get('parameters',[])
            if (function_mutability(body) not in ('view','pure') or len(params)!=1 or len(returns)!=1
                or params[0].get('typeDescriptions',{}).get('typeString') not in ('address','address payable')
                or returns[0].get('typeDescriptions',{}).get('typeString') not in ('uint','uint256')):continue
            if fn not in accessors and fn in program:proposed.setdefault(fn,[]).append(hint)
    for fn in proposed:
        try:accessors[fn]=program.get(fn) or lookup.run(fn)
        except (ValueError,KeyError,TypeError):accessors[fn]=[]
    for accessor,paths in accessors.items():
        located=accessor!='balanceOf(address)'
        if located:
            completed=[p for p in paths if p['flow']!='reverted']
            if not completed or any(p['flow']!='returned' or p['issues'] or p.get('evaluation_gaps') or p.get('writes') for p in completed):continue
            # A conditional getter cannot attest a different total on another path.
            forms={key(polynomial(p.get('return_value',{}))) for p in completed}
            if len(forms)!=1:continue
        for p in paths:
            if p['flow']!='returned' or p['issues'] or p.get('writes'):continue
            form=polynomial(p.get('return_value',{}))
            if not form or len(form)!=2 or any(c!=1 for c in form.values()):continue
            import json
            terms=[json.loads(t) for t in form if t!='#']
            if len(terms)!=2 or not all(component_shape(t,lookup) is not None for t in terms):continue
            if key(keys(terms[0]))!=key(keys(terms[1])) or key(terms[0].get('instance'))!=key(terms[1].get('instance')):continue
            roots={t['root'] for t in terms}
            shapes={component_shape(t,lookup) for t in terms}
            if len(shapes)!=2 or not any(component_shape(a['balance_effect']['path'],lookup) in shapes for a in assets):continue
            for fn,branches in program.items():
                candidate_hints=[h for h in proposed.get(accessor,[]) if fn in h['functions'] and roots.issubset(set(h.get('resource_roots',[h.get('resource_root')])))]
                if located and not candidate_hints:continue
                for pi,b in enumerate(branches):
                    if b.get('evaluation_gaps'):continue
                    if b['flow'] not in ('normal','returned') or b['issues'] or b.get('native_transfers'):continue
                    shapes={component_shape(t,lookup) for t in terms}
                    updates=[d for d in changes(b,lookup) if component_shape(d['write']['path'],lookup) in shapes]
                    if len(updates)!=2 or not updates[0]['delta'] or updates[1]['delta']!=negative(updates[0]['delta']):continue
                    if {d['write']['path']['root'] for d in updates}!=roots:continue
                    if not all(component_shape(d['write']['path'],lookup) is not None for d in updates):continue
                    if key(keys(updates[0]['write']['path']))!=key(keys(updates[1]['write']['path'])):continue
                    if any(key(d['write']['path'].get('instance'))!=key(terms[0].get('instance')) for d in updates):continue
                    used=[]
                    if located:
                        from .m15_relations import financial_scope
                        from .m03_p_assets import term
                        amount=next((term(negative(d['delta'])) for d in updates if all(v<0 for v in d['delta'].values())),None)
                        used=[h['id'] for h in candidate_hints if all(financial_scope(h,b,fn,d['write']['path'],lookup,amount,[keys(d['write']['path'])[0]]) for d in updates)]
                        if not used:continue
                    result.append({'construction_origin':'M2_located_source_combination' if located else 'independent_standard_accessor', 'construction_relation_ids':sorted(set(used)), 'roots':sorted(roots),'component_selectors':terms,'component_shapes':sorted(shapes),'accessor':accessor,'accessor_source':p.get('entry_source'),'conversion_function':fn,'path_index':pi,'conversion_writes':[d['write']['source'] for d in updates],'basis':'source accessor explicitly totals same-holder components and source converts them one-to-one; one root has independently established transfer/redemption meaning','relation_ids':sorted(set(used)) if located else [h['id'] for h in hints if roots.intersection(h.get('resource_roots',[h.get('resource_root')])) and fn in h['functions']]})
    unique={}
    for certificate in result:
        identity=tuple(certificate['component_shapes']);previous=unique.get(identity)
        if previous and previous.get('construction_origin')=='independent_standard_accessor' and certificate.get('construction_origin')!='independent_standard_accessor':
            previous['relation_ids']=sorted(set(previous.get('relation_ids',[])+certificate.get('relation_ids',[])))
            continue
        if previous:certificate['relation_ids']=sorted(set(previous.get('relation_ids',[])+certificate.get('relation_ids',[])))
        unique[identity]=certificate
    return list(unique.values())

def component_updates(path,lookup,asset):
    roots=set(asset.get('equity_component_roots',[asset['balance_root']]))
    shapes=set(asset.get('equity_certificate',{}).get('component_shapes',[])) or ({asset['field_ledger_shape']} if asset.get('field_ledger_shape') else set())
    return [d for d in changes(path,lookup) if (component_shape(d['write']['path'],lookup) in shapes if shapes else d['write']['path']['root'] in roots) and key(d['write']['path'].get('instance'))==key(asset['balance_effect']['path'].get('instance'))]

def attach_components(lookup,program,assets,hints):
    certificates=equity_components(lookup,program,assets,hints)
    for asset in assets:
        matches=[c for c in certificates if component_shape(asset['balance_effect']['path'],lookup) in c['component_shapes']]
        # Do not transitively merge three assets through pairwise coincidences.
        if len(matches)==1:
            asset['equity_component_roots']=matches[0]['roots'];asset['equity_certificate']=matches[0]
    return certificates

def component_shape(selector,lookup):
    if selector.get('kind')!='storage' or len(keys(selector))!=1:return None
    root_type=lookup.nodes.get(selector['root'],{}).get('typeName',{})
    if root_type.get('nodeType')!='Mapping' or root_type.get('keyType',{}).get('name') not in ('address','address payable'):return None
    if not selector.get('segments') or 'key' not in selector['segments'][0]:return None
    if value_type(selector,lookup) not in ('uint','uint256'):return None
    if any(set(segment)-{'key','field','label'} for segment in selector.get('segments',[])):return None
    return key({'root':selector['root'],'segments':[{'holder_key':True} if 'key' in x else {'field':x['field']} for x in selector.get('segments',[])],'instance':selector.get('instance')})

def component_holder(selector,asset,lookup):
    if asset.get('equity_certificate'):return component_shape(selector,lookup) in asset['equity_certificate']['component_shapes']
    if asset.get('field_ledger_shape'):return component_shape(selector,lookup)==asset['field_ledger_shape']
    return holder_path(selector,lookup) or component_shape(selector,lookup) in asset.get('equity_certificate',{}).get('component_shapes',[])
