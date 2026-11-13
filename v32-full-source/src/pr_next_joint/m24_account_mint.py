"""Privileged positive net issue of a source-eligible abstract account record."""
import copy
from .m03_p_paths import op,lit
def mint_row(lookup,p,fn,pi,sel,write,change,total,priv,probe):
    from .m08_financial import quantity
    from .m03_p_route import keys,fields
    # The enclosing account route already rejects control records, credential
    # counters, aggregate conversions and exact same-unit transfers.
    risk=op('and',op('or',*priv),op('>',quantity(change['delta']),lit(0)),op('>',quantity(total),lit(0)))
    meta={'kind':'privileged_abstract_account_net_issuance','asset':{'kind':'abstract_account_ledger','balance_root':sel['root'],'fields':fields(sel),'financial_link_confirmed':False},
          'holder':keys(sel)[0],'credit':change,'family_net_delta':total,'privilege':priv,'path_index':pi,
          'evaluation_terms':copy.deepcopy(p.get('evaluated_terms',[])),
          'scope':'approved abstract account units; no real-value or reachable authority initial-state proof',
          'initial_state_limit':'a declared but never initialized authority can make this mechanism unreachable in a particular deployment'}
    row=probe(lookup,copy.deepcopy(p['guards']),risk,meta,write['source'],fn,'FCR-MINT')
    row['definition_profile']='abstract_account_ledger'
    row['effect']={'kind':'account_net_increase','selector':sel,'value':write['value'],'operator':write['operator'],'source':write['source']}
    return row
