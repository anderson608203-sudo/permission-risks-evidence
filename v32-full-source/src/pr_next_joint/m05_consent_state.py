"""Narrow roles of existing holder state; no new source-reference matching."""
import copy
from .m05_writer_scope import gaps_for
from .m03_p_paths import key,op,lit,conditions_possible
from .m03_p_route import keys,selectors
from .m03_p_assets import polynomial
from .m04_logic import Unsupported
from .m05_bound_relations import family,project
from .m05_mechanism_core import remap,post,scalar_write,reject_changed_selector_keys

def revocation_only(branch,write,selector,action,holder,quantity,lookup):
    if branch['issues'] or scalar_write(write,lookup)['value'] not in (lit(0),lit(False)):
        return None
    try:
        source=remap(write['path'],sender=holder)
        updates=project(remap([w for w in branch['writes'] if family(w['path'],write['path'])],sender=holder),source,selector)
        def conjuncts(value):
            if value.get('kind')=='op' and value.get('op') in ('and','&&'):
                return [x for a in value['args'] for x in conjuncts(a)]
            return [value]
        # Only this exact request field may establish revocation. A changed
        # global pause, balance or unrelated business guard is not evidence.
        premise=[atom for g in action['guards'] for atom in conjuncts(g)
            if {key(s) for s in selectors(atom)}=={key(selector)}]
        if key(quantity)==key(selector):premise.append(op('>',quantity,lit(0)))
        if not premise:return None
        reject_changed_selector_keys(premise,updates)
        after=post(premise,updates,lookup)
        if conditions_possible(after):return None
        return {'kind':'same_request_revocation_only','source':write['source'],
            'selector':copy.deepcopy(selector),'post_conditions':after,
            'scope':'this complete clearing operation prevents this positive consumption; not authorization creation'}
    except (Unsupported,ValueError,TypeError,KeyError):return None

def automatic_deposit_clock(selector,holder,lookup,program,ledger_root):
    from .m05_state_relations import changes
    if gaps_for(lookup,{selector['root'],ledger_root}):return None
    records=[]
    for fn,branches in program.items():
        for branch in branches:
            if branch['flow']=='reverted':continue
            for raw in branch['writes']:
                if not family(raw['path'],selector):continue
                if branch['issues']:return None
                write=scalar_write(raw,lookup);value=write['value']
                if value.get('kind')!='op' or value.get('op')!='+' or len(value['args'])!=2:return None
                left,right=value['args']
                if right.get('kind')=='environment':left,right=right,left
                if (left.get('kind')!='environment' or left.get('field')!='timestamp'
                    or right.get('kind')!='literal' or type(right.get('value')) is not int or right['value']<=0):return None
                kk=keys(write['path'])
                if len(kk)!=1 or kk[0].get('kind')!='actual_sender':return None
                if lookup.function(fn).get('stateMutability')!='payable':return None
                deposits=[d for d in changes(branch,lookup) if d['write']['path']['root']==ledger_root
                    and keys(d['write']['path'])==kk and d['delta']==polynomial({'kind':'transaction_value','type':'uint256'})]
                if len(deposits)!=1:return None
                records.append({'function':fn,'source':write['source'],'offset':right['value'],'deposit':deposits[0]['write']})
    if not records:return None
    return {'kind':'automatic_deposit_business_clock','selector':copy.deepcopy(selector),'writers':records,
        'scope':'fixed source time offset on holder native deposit; actual time guards remain, no consent is inferred'}
