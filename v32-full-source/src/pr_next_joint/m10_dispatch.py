"""Unqualified internal virtual dispatch from compiler-checked C3 inheritance."""
def resolve(lookup,target,contract_id=None,after=None):
    if not target or target.get('nodeType')!='FunctionDefinition' or target.get('visibility')=='private':return target
    cid=contract_id or lookup.contract_node['id'];order=lookup.nodes[cid].get('linearizedBaseContracts',[cid])
    if target.get('scope') not in order:return target
    if after is not None:
        if after not in order:raise ValueError('P_SUPER_LEXICAL_SCOPE_NOT_IN_HIERARCHY')
        order=order[order.index(after)+1:]
    def signature(n):
        types=[p.get('typeDescriptions',{}).get('typeIdentifier') for p in n.get('parameters',{}).get('parameters',[])]
        return (n.get('name'),tuple(types)) if all(types) else None
    sig=signature(target)
    if sig is None:return target
    for owner in order:
        matches=[n for n in lookup.fns.values() if n.get('nodeType')=='FunctionDefinition' and n.get('scope')==owner and n.get('visibility')!='private' and signature(n)==sig]
        if len(matches)>1:raise ValueError('internal_dispatch_ambiguous_source_signature')
        if matches and (after is None or matches[0].get('body')):return matches[0]
    if after is not None:raise ValueError('P_SUPER_CONCRETE_TARGET_NOT_FOUND')
    return target

def member_target(lookup,call,target):
    """Distinguish an internal base/super call from an external object method."""
    expr=call['expression'];base=expr.get('expression',{})
    if not target or expr.get('nodeType')!='MemberAccess' or call.get('names'):return None
    if not expr.get('typeDescriptions',{}).get('typeIdentifier','').startswith('t_function_internal_'):return None
    if base.get('nodeType') not in ('Identifier','IdentifierPath'):return None
    order=lookup.contract_node['linearizedBaseContracts']
    if base.get('referencedDeclaration') in order and target.get('scope') in order:
        return target
    if base.get('name')!='super' or 'super' not in base.get('typeDescriptions',{}).get('typeIdentifier',''):return None
    if not hasattr(lookup,'_lexical_call_scopes'):
        from .m03_p_paths import walk
        lookup._lexical_call_scopes={n['id']:f['scope'] for f in lookup.fns.values() if f.get('scope') in order
                                    for n in walk(f.get('body')) if n.get('nodeType')=='FunctionCall'}
    owner=lookup._lexical_call_scopes.get(call['id'])
    if owner is None:raise ValueError('P_SUPER_LEXICAL_SCOPE_UNRESOLVED')
    return resolve(lookup,target,lookup.read_calls.active_contract,after=owner)
