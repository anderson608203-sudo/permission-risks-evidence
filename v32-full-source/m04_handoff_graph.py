"""Nomination/acceptance relationship queries, including defective transitions.

Find protocol phases from writes and authority guards, before deciding whether
the acceptance is correct. Never require the property being checked in order
to recognize the protocol. No identifiers or development labels are used.
"""
from .m03_p_paths import key,lit,op,conditions_possible,normalize

SENDER={'kind':'actual_sender'}

def discover(lookup,program):
    from .m03_p_route import value_type,effective_permission
    from .m04_policy_relations import address_equality
    models=[]
    for issue,paths in program.items():
        for path in paths:
            if path['flow']=='reverted' or path['issues']:continue
            for guard in effective_permission(path['guards'],lookup):
                authority=address_equality(guard,lookup)
                if not authority or authority.get('segments'):continue
                for nomination in path['writes']:
                    pending=nomination['path'];value=nomination['value']
                    if pending.get('segments') or pending['root']==authority['root']:continue
                    if value_type(pending,lookup) not in ('address','address payable') or value.get('kind')!='parameter' or value.get('type') not in ('address','address payable'):continue
                    for accept,apaths in program.items():
                        if accept==issue:continue
                        for ap in apaths:
                            if ap['flow']=='reverted' or ap['issues']:continue
                            transfers=[w for w in ap['writes'] if key(w['path'])==key(authority)]
                            clears=[w for w in ap['writes'] if key(w['path'])==key(pending) and normalize(w['value'])==lit(0)]
                            if len(transfers)!=1 or not clears:continue
                            model={'authority':authority,'pending':pending,'nomination_function':issue,'nomination_source':nomination['source'],
                                   'accept_function':accept,'accept_source':transfers[0]['source'],'successor':transfers[0]['value'],
                                   'required':op('and',op('==',SENDER,pending),op('==',transfers[0]['value'],pending)),
                                   'basis':'authority-selected nominee; acceptance transfers to that current nominee',
                                   'scope':'inferred two-step handoff protocol; transaction history not established'}
                            models.append(model)
    return list({key((m['authority'],m['pending'],m['accept_function'])):m for m in models}.values())

def alternative(peer,write,function,models):
    for m in models:
        if peer['function']==m['accept_function'] and function!=peer['function']:
            return {'reason':'acceptance_guard_not_a_nomination_management_policy','model':m}
        if function==m['accept_function'] and peer['function']!=function and key(write['path'])!=key(m['authority']):
            return {'reason':'acceptance_consumes_or_clears_issued_nomination','model':m}

def cleanup(write,function,models):
    return next((m for m in models if function==m['accept_function'] and key(write['path'])==key(m['pending']) and normalize(write['value'])==lit(0)),None)
