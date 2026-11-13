"""Compare committed delegations under two source-bound parameter settings."""
from collections import defaultdict

from .m03_p_paths import key, lit, op, walk
from .m03_p_route import fields, keys, selectors, value_type
from .m04_logic import Unsupported
from .m05_asset_obligations import privilege
from .m05_state_relations import compose_read
from .m08_financial import probe
from .m20_sequence import qualify, read
from .m27_effect_checks import SENDER, committed


def legs(path):
    grouped = defaultdict(list)
    for w in path['writes']:
        sel = w['path']
        if len(keys(sel)) == 1 and not fields(sel) and not sel.get('instance'):
            grouped[sel['root']].append(w)
    for root, ws in grouped.items():
        if len(ws) != 2:
            continue
        debit, credit = ws
        if (debit['value'].get('op') == '-' and debit['value']['args'][0] == debit['path']
                and credit['value'].get('op') == '+' and keys(credit['path'])[0].get('kind') == 'parameter'):
            yield root, debit, credit


def general_grants(queue,target,limit):
    sites = []
    for r in queue.writer_paths(target,limit):
        sel = r['effect']['selector']
        ks = keys(sel)
        if fields(sel) or sel.get('instance') or len(ks)!=2 or ks[0]!=SENDER or ks[1].get('kind')!='parameter':
            continue
        path = queue.committed[target].get((r['function'],r['path_index']))
        if (path and len(path['writes'])==1 and not path.get('sensitive_effects') and
            r['effect']['value'].get('kind')=='parameter' and not path.get('native_transfers')):
            sites.append(r['effect']['source'])
    return sites


def scratch_only(root,lookup,program):
    # An accumulated pot or reimbursable credit must never be treated as burnt.
    # Expanded path expressions substitute same-call writes. Any use of the
    # incoming stored value, opaque effects, or a public getter blocks this proof.
    decl=lookup.nodes[root]
    if decl.get('visibility')=='public' or any(n.get('nodeType')=='InlineAssembly' or
            n.get('memberName') in ('delegatecall','callcode') for n in walk(lookup.implementations)):
        return False
    for paths in program.values():
        for p in paths:
            if p['flow'] in ('revert','reverted'):
                continue
            if not committed(p):
                return False
            reads=[p['guards'],p.get('return_value'),p.get('native_transfers',[]),p.get('sensitive_effects',[])]
            for w in p['writes']:
                reads.extend([w['value'],w['path'].get('segments',[])])
            if any(s['root']==root for s in selectors(reads)):
                return False
    return True


def compare(target,lookup,program,queue):
    rows=[]; notes=[]
    routes=[]; own=set(); getters=set()
    for paths in program.values():
        for p in paths:
            ret=p.get('return_value') or {}
            if isinstance(ret,dict) and ret.get('kind')=='storage' and len(keys(ret))==1 and not fields(ret):
                if committed(p) and keys(ret)[0].get('kind')=='parameter':
                    getters.add(ret['root'])
    for (fn,pi),path in queue.committed[target].items():
        if path.get('sensitive_effects') or path.get('native_transfers'):
            continue
        for root,debit,credit in legs(path):
            if not (value_type(debit['path'],lookup) or '').startswith('uint'):
                continue
            if keys(debit['path'])[0]==SENDER:
                own.add(root)
            else:
                routes.append((fn,pi,path,root,debit,credit))
    scratch={}
    for fn,pi,path,root,debit,credit in routes:
        holder,recipient=keys(debit['path'])[0],keys(credit['path'])[0]
        if holder.get('kind')!='parameter' or holder==recipient:
            continue
        limits=[w for w in path['writes'] if keys(w['path'])==[holder,SENDER] and not fields(w['path'])
                and not w['path'].get('instance') and w['value'].get('op')=='-' and w['value']['args'][0]==w['path']]
        if len(limits)!=1:
            continue
        spend=limits[0]; limit=spend['path']
        grant_sites=general_grants(queue,target,limit)
        if not grant_sites:
            continue
        rids=sorted({rid for rec in queue.locations.get((target,fn,credit['source']['ast_id']),())
                     for rid in queue.financial_hints.get(rec['id'],())})
        # M2 can locate a nonstandard transfer. Require direct source evidence
        # of a holder balance view and holder-issued delegated spending as well.
        if root not in own and not (root in getters and rids):
            continue
        scalar={s['root']:s for s in selectors(credit['value'])
                if not s.get('segments') and not s.get('instance') and (value_type(s,lookup) or '').startswith('uint')}
        for config in scalar.values():
            for rec in queue.writer_paths(target,config):
                setter,si=rec['function'],rec['path_index']
                setup=queue.committed[target].get((setter,si))
                if (not setup or setter==fn or len(setup['writes'])!=1 or setup.get('sensitive_effects')
                        or setup.get('native_transfers') or rec['effect']['value'].get('kind')!='parameter'):
                    continue
                admins=privilege(setup['guards'],lookup,root)
                if not admins:
                    continue
                step=qualify(setup,1); sw=step['writes']
                try:
                    a,b=debit['path'],credit['path']
                    post_a=compose_read(a,path['writes'],lookup);post_b=compose_read(b,path['writes'],lookup)
                    post_limit=compose_read(limit,path['writes'],lookup)
                    gross=op('-',a,post_a);net=op('-',post_b,b);charged=op('-',limit,post_limit)
                    next_gross,next_net,next_charged=[read(x,sw,lookup) for x in (gross,net,charged)]
                    if next_net==net and next_gross==gross:
                        continue
                    actors=[*step['guards'],qualify(op('or',*admins),1),op('!=',qualify(SENDER,1),holder),
                        op('!=',qualify(SENDER,1),SENDER),op('!=',holder,SENDER),op('!=',holder,recipient),
                        op('!=',recipient,lit(0))]
                    conditions=[*actors,*path['guards'],*read(path['guards'],sw,lookup)]
                    terms=step.get('evaluated_terms',[])+path.get('evaluated_terms',[])+read(path.get('evaluated_terms',[]),sw,lookup)
                    meta={'kind':'same_delegated_request_gross_net_allowance','setter':setter,'consumer':fn,'path_index':pi,
                        'holder':holder,'recipient':recipient,'balance_root':root,'limit':limit,'grant_sites':grant_sites,
                        'debit_site':debit['source'],'credit_site':credit['source'],'allowance_site':spend['source'],
                        'semantic_site_hints':rids,'verified_relation_ids':rids if root not in own else [],
                        'construction_origin':'semantic_site_plus_source_grant_and_getter' if root not in own else 'source_self_service_and_grant',
                        'old':[gross,net,charged],'new':[next_gross,next_net,next_charged],
                        'evaluation_terms':terms}
                    diff=op('and',op('>',gross,lit(0)),op('==',gross,net),op('==',gross,charged),
                            op('==',next_gross,gross),op('>=',next_net,lit(0)),op('<',next_net,next_gross),
                            op('==',next_charged,next_net))
                    obs=probe(lookup,conditions,diff,dict(meta),rec['effect']['source'],fn,'parameter_influence')
                    notes.append({'phase':'financial_parameter_check','mechanism_only':True,'check':obs})
                    queue.note(target,fn,pi,'checked_parameter','same_request_gross_net_allowance',credit['source'],rids)
                    if not obs['reportable']:
                        continue
                    # Require more than a lower payout. In the changed world a
                    # real holder loses more than their available approval. No
                    # third credit, ongoing fee entitlement or opaque call.
                    other=[w['path'] for w in path['writes'] if w not in (debit,credit,spend)]
                    for cell in other:
                        if not cell.get('segments') and cell['root'] not in scratch:
                            scratch[cell['root']]=scratch_only(cell['root'],lookup,program)
                    if any(c.get('segments') or not scratch.get(c['root']) for c in other):
                        queue.note(target,fn,pi,'limited','other_write_may_carry_compensation',credit['source'])
                        continue
                    allowed_roots={root,limit['root'],config['root']}
                    if any(s['root'] not in allowed_roots for s in selectors(path['guards'])) or any(
                            n.get('kind') in ('hash','credential_recovery') for n in walk(path['guards'])):
                        queue.note(target,fn,pi,'limited','independent_authorization_requires_binding',credit['source'])
                        continue
                    # The old transaction may REVERT at this smaller allowance.
                    # Only the actual changed-world execution is required to commit.
                    # Compare the old arithmetic separately to distinguish a
                    # pre-existing fee from an impairment caused by this setter.
                    domain=[*actors,*read(path['guards'],sw,lookup)]
                    # Use the old *requested charge*, never an old post-allowance
                    # from a transaction which would have underflowed/reverted.
                    old_charge=spend['value']['args'][1]
                    loss=op('and',op('==',gross,net),op('==',gross,old_charge),op('==',next_gross,gross),
                            op('>',old_charge,limit),op('>=',next_net,lit(0)),op('==',next_charged,next_net),
                            op('<',next_net,next_gross),op('<=',next_charged,limit))
                    risk_meta={**meta,'kind':'privileged_uncompensated_holder_loss_above_general_approval',
                        'setting_scope':'same pre-state and request; old allowance check may revert',
                        'excluded_other_credits':True,'evaluation_terms':step.get('evaluated_terms',[])+read(path.get('evaluated_terms',[]),sw,lookup)}
                    rows.append(probe(lookup,domain,loss,risk_meta,rec['effect']['source'],fn,'FCR-DESTROY'))
                except Unsupported as exc:
                    notes.append({'phase':'financial_parameter_check','function':fn,'reason':str(exc)})
    return rows,notes
