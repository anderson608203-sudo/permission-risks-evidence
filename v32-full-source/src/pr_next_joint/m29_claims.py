"""Redirecting another user's pre-funded, still-redeemable claim.

A payment recipient alone establishes no policy. Require a payable origin
establishing the claim, a committed redemption consuming it, and a distinct
uncompensated writer who can redirect that same redemption to themselves.
"""
from .m03_p_paths import key, lit, op
from .m03_p_route import effective_permission, keys, value_type
from .m05_bound_relations import family
from .m05_state_relations import compose_read
from .m11_policy import make_query
from .m20_sequence import read
from .m25_reserve import write_only_mark
from .m28_capabilities import SENDER, later, plain_setup
from .m04_logic import Unsupported


def same_subject(a,b):
    return keys(a)==keys(b) and key(a.get('instance'))==key(b.get('instance'))


def paid_origin(program,lookup,recipient,claim):
    result=[]
    for fn,paths in program.items():
        if lookup.function(fn).get('stateMutability')!='payable':
            continue
        for p in paths:
            if p['flow'] not in ('normal','returned') or p['issues'] or p.get('evaluation_gaps') or p.get('native_transfers') or p.get('sensitive_effects'):
                continue
            for bill in p['writes']:
                dest=bill['path']
                if not family(dest,claim) or bill['value'].get('kind')!='transaction_value':
                    continue
                if compose_read(dest,p['writes'],lookup)!=bill['value']:
                    continue
                for owner in p['writes']:
                    cell=owner['path']
                    if family(cell,recipient) and same_subject(cell,dest) and owner['value']==SENDER:
                        if compose_read(cell,p['writes'],lookup)==SENDER:
                            from .m08_financial import probe
                            evidence=probe(lookup,p['guards'],op('and',op('>',bill['value'],lit(0)),op('!=',SENDER,lit(0))),
                                {'kind':'caller_funds_own_record','evaluation_terms':p.get('evaluated_terms',[])},
                                bill['source'],fn,'funding_witness')
                            if evidence['reportable']:
                                result.append({'entry':fn,'owner_site':owner['source'],'deposit_site':bill['source'],
                                               'funding_formula':evidence['formal']['formula_sha256']})
    return result


def duties(context,state,queue):
    rows=[]
    for target,positions in queue.committed.items():
        lookup=state['lookups'][target]
        program={fn:ps for (t,fn),ps in state['paths'].items() if t==target}
        for (redeem,pi),path in positions.items():
            payments=path.get('native_transfers',[])
            if len(payments)!=1 or len(path.get('sensitive_effects',[]))>1:
                continue
            pay=payments[0];dest=pay['recipient'];claim=pay['amount']
            if pay.get('kind')!='native_transfer' or dest.get('kind')!='storage' or claim.get('kind')!='storage':
                continue
            if not same_subject(dest,claim) or value_type(dest,lookup) not in ('address','address payable'):
                continue
            try:
                if compose_read(claim,path['writes'],lookup)!=lit(0):
                    continue
                origins=paid_origin(program,lookup,dest,claim)
                if not origins:
                    continue
                for r in queue.writer_paths(target,dest):
                    fn,wi=r['function'],r['path_index']; setter=positions.get((fn,wi))
                    write=r['effect'].get('original_write')
                    if (not setter or not write or fn==redeem or not family(write['path'],dest) or
                            setter.get('native_transfers') or setter.get('sensitive_effects') or
                            lookup.function(fn).get('stateMutability')=='payable' or not plain_setup(setter,lookup)):
                        continue
                    if write['value'].get('kind') not in ('parameter','actual_sender'):
                        continue
                    if any(w!=write and not write_only_mark(w,lookup) for w in setter['writes']):
                        continue
                    # Match the actual recipient after all writes; keeping the
                    # callee arguments in their own namespace prevents key swaps.
                    before=later(dest); after=read(before,setter['writes'],lookup)
                    amount=later(claim)
                    model=dict(setter)
                    model['guards']=[*setter['guards'],op('!=',before,SENDER),op('!=',before,lit(0)),
                        op('==',after,SENDER),op('>',amount,lit(0)),op('<=',amount,{'kind':'native_reserve','instance':lookup.read_calls.address()}),
                        *read(later(path['guards']),setter['writes'],lookup)]
                    if pay.get('success'):
                        model['guards'].append(read(later(pay['success']),setter['writes'],lookup))
                    model['evaluated_terms']=[*setter.get('evaluated_terms',[]),*read(later(path.get('evaluated_terms',[])),setter['writes'],lookup)]
                    required=op('or',op('==',SENDER,write['path']),*effective_permission(setter['guards'],lookup))
                    basis={'basis':'redirect_live_prefunded_claim_to_unrelated_caller','funding':origins,
                        'redemption_site':pay['source'],'redeem_entry':redeem,'claim':amount,'payee_before':before,'payee_after':after,
                        'scope':'local committed change to an existing funded claim; no loss asserted for unallocated records'}
                    q=make_query(context,target,fn,wi,model,write,required,basis,'AC-03')
                    rows.append(q)
                    queue.note(target,fn,wi,'dispatched','redirect_of_funded_claim',write['source'])
            except Unsupported as exc:
                queue.note(target,redeem,pi,'unsupported',str(exc),pay['source'])
    return rows
