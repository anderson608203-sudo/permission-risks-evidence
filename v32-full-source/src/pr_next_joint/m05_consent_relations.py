"""Source-bound signer/holder relations for fixed payload authorization.

Assumes an issued valid credential; never treats an uninterpreted recovery
model as evidence of signature forgery. Unbound payload scope is unresolved.
"""
from .m03_p_paths import key,walk,op,lit
from .m03_p_route import value_type
from .m04_logic import Unsupported

def credential_consent(path,holder,quantity,lookup,recipient=None):
    from .m05_credential_obligations import recoveries,payload
    credentials=recoveries(path['guards'])
    if not credentials:return None
    if len(credentials)!=1:raise Unsupported('consent_multiple_credentials_require_joint_authority_model')
    recovered=credentials[0];encoded=payload(recovered)
    hashes={key(n) for n in walk(path['guards']) if n.get('kind')=='hash'}
    if hashes!={key(n) for n in walk(recovered['digest']) if n.get('kind')=='hash'}:
        raise Unsupported('consent_extra_cryptographic_condition')
    # Exact typed arguments: mere occurrence inside a hash expression does not
    # establish that a holder signed the relevant amount/resource.
    signed={key(n) for n in encoded['arguments']}
    signed_scope=key(holder) in signed and key(quantity) in signed
    recipient_bound=recipient is None or key(recipient) in signed
    if recipient is not None and not recipient_bound:
        from .m03_p_paths import conditions_possible
        # Equality on the actual successful path can bind a transfer argument
        # to an exact signed address. Never infer a destination from its name.
        recipient_bound=any(value_type(n,lookup) in ('address','address payable')
            and not conditions_possible(path['guards'],op('==',recipient,n))
            for n in encoded['arguments'] if n.get('kind')=='storage')
        recipient_bound=recipient_bound or any(n.get('type') in ('address','address payable')
            and not conditions_possible(path['guards'],op('==',recipient,n))
            for n in encoded['arguments'] if n.get('kind')=='parameter')
    def conjuncts(v):
        if v.get('kind')=='op' and v.get('op') in ('and','&&'):
            return [n for a in v['args'] for n in conjuncts(a)]
        return [v]
    authorities=[]
    for guard in path['guards']:
        for atom in conjuncts(guard):
            if atom.get('kind')!='op' or atom.get('op')!='==':continue
            for a,b in (atom['args'],atom['args'][::-1]):
                if key(a)==key(recovered) and (key(b)==key(holder) or b.get('kind')=='storage' and not b.get('segments') and value_type(b,lookup) in ('address','address payable')):
                    authorities.append(b)
    unique={key(x):x for x in authorities}
    if len(unique)!=1:raise Unsupported('credential_signer_authority_not_unique')
    authority=next(iter(unique.values()))
    holder_authority=key(authority)==key(holder)
    if holder_authority and not signed_scope:
        raise Unsupported('credential_holder_or_quantity_not_signed_requires_scope_model')
    if holder_authority and not recipient_bound:
        raise Unsupported('credential_destination_or_open_spender_scope_requires_model')
    equality=op('==',recovered,authority)
    return {'holder_consent':op('==',recovered,holder),
            'privilege':[] if holder_authority else [equality],
            'valid_issued_credential':op('!=',recovered,lit(0)),
            'certificate':{'kind':'fixed_source_payload_signer_holder_relation',
                'authority':authority,'holder':holder,'quantity':quantity,'recipient':recipient,'credential':recovered,
                'recipient_scope_bound':recipient_bound,
                'authority_is_holder_expression':holder_authority,
                'holder_and_quantity_signed':signed_scope,
                'consent_interpretation':'exact holder payload' if holder_authority else
                    'independent administrative signature; equality with holder conservatively retains possible holder consent',
                'graph':{'engine':'source relation DAG','edges':[['typed_holder_quantity_payload','recovered_signer'],['recovered_signer','source_authority_guard'],['source_authority_guard','holder_debit']]},
                'assumptions':['a valid nonzero credential was issued for this exact source payload',
                    'no signature forgery or hash collision is inferred; business consent beyond this payload remains outside the model']}}
