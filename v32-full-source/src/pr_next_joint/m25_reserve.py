"""An unaccounted, caller-directed payment exhausting an externally funded reserve."""
from .m03_p_paths import key, lit, op, walk
from .m03_p_route import effective_permission
from .m25_phase import clean


def caller_switch(term):
    if term.get('kind')=='literal':
        return type(term.get('value')) is bool
    if term.get('kind')=='parameter':
        return term.get('type')=='bool'
    return (term.get('kind')=='op' and term.get('op') in ('!','and','or','&&','||')
            and bool(term.get('args')) and all(caller_switch(a) for a in term['args']))


def write_only_mark(write,lookup):
    """Accept only direct constant writes to scalars never read by contract code."""
    loc=write['path']
    if loc.get('segments') or write['value'].get('kind')!='literal' or write['operator']!='=':
        return False
    root=loc['root']
    if root not in lookup.decls or not lookup.decls[root].get('typeDescriptions',{}).get('typeString','').startswith(('uint','bool')):
        return False
    cache=lookup.__dict__.setdefault('_reserve_write_only_scalar',{})
    if root not in cache:
        order=lookup.contract_node['linearizedBaseContracts']
        nodes=[n for owner in order for n in walk(lookup.nodes[owner])]
        refs={n['id'] for n in nodes if n.get('referencedDeclaration')==root}
        simple_lhs={n['leftHandSide']['id'] for n in nodes if n.get('nodeType')=='Assignment' and n.get('operator')=='='
                    and n['leftHandSide'].get('nodeType')=='Identifier' and n['leftHandSide'].get('referencedDeclaration')==root}
        cache[root]=bool(refs) and refs==simple_lhs and not any(n.get('nodeType')=='InlineAssembly' for n in nodes)
    return cache[root]


def reserve_disposition(fn, path, transfer, lookup, program):
    if transfer['kind']!='native_transfer' or not clean(path) or len(path['native_transfers'])!=1:
        return None
    if transfer['recipient'].get('kind')!='parameter' or transfer['amount'].get('kind')!='parameter':
        return None
    if any(g!=transfer['success'] and not caller_switch(g) for g in path['guards']):
        return None
    if not all(write_only_mark(w,lookup) for w in path['writes']):
        return None
    funders=[]
    peers=[]
    for entry, branches in program.items():
        if entry==fn:continue
        for other in branches:
            if not clean(other):continue
            if (lookup.function(entry).get('stateMutability')=='payable' and not other['guards'] and not other.get('sensitive_effects')
                    and not other['writes']):
                funders.append(entry)
            if other['writes'] or len(other.get('native_transfers',[]))!=1:continue
            paid=other['native_transfers'][0]
            if paid['recipient'].get('kind')!='parameter' or paid['amount'].get('kind')!='parameter':continue
            if lookup.function(entry).get('visibility') not in ('public','external'):continue
            for g in effective_permission(other['guards'],lookup):
                if g.get('op')=='==' and any(x.get('kind')=='actual_sender' for x in g['args']) and any(
                        x.get('kind')=='storage' and not x.get('segments') for x in g['args']):
                    peers.append((entry,paid['source'],g))
    if not funders or not peers:return None
    received={'kind':'transaction_value','type':'uint256'}
    reserve={'kind':'native_reserve','instance':lookup.read_calls.address()}
    requirements=op('or',op('<=',transfer['amount'],received),op('>',transfer['amount'],reserve),
                    op('!=',transfer['recipient'],{'kind':'actual_sender'}),*(g for _,_,g in peers))
    return requirements,{'basis':'source_unaccounted_caller_directed_reserve_withdrawal',
        'reserve_funding_entries':sorted(set(funders)),'parallel_managed_payments':peers,
        'non_accounting_scalar_writes':[w['source'] for w in path['writes']],
        'scope':'successful caller-directed withdrawal of pre-existing reserve; conditional on available funds'}
