"""Conservative symbolic intrinsics for source-bound M4 obligations.

Keccak over fixed ABI tuples is a congruent uninterpreted function, without
injectivity or a preimage oracle. UNSAT is usable in that overapproximation;
SAT involving this abstraction is never promoted to a confirmed prediction.
"""
from .m04_logic import Unsupported
from .m03_p_paths import walk

def intrinsic(e,v):
    z=e.z
    if v.get('kind')=='hash':
        from .m05_credential_encoding import layout
        enc=layout(v)
        types=enc.get('types',[]);args=enc.get('arguments',[])
        if not types or len(types)!=len(args):raise Unsupported('hash_ABI_arity')
        normalized=[]
        for typ in types:
            if '[' in typ or typ in ('bytes','string') or typ.startswith(('struct ','tuple')):raise Unsupported('hash_dynamic_ABI_not_encoded')
            if typ!='bool' and not typ.startswith('fixed_bytes_literal:'):e.width(typ)
            normalized.append('address' if typ.startswith('contract ') else typ)
        from .m05_credential_encoding import fixed_literal
        def argument(x):
            if x.get('kind')=='fixed_bytes_literal':
                raw,_=fixed_literal(x)
                return z.IntVal(int(raw,16) if raw else 0)
            return e.expr(x)
        values=[argument(x) for x in args]
        for typ,value in zip(normalized,values):
            if (typ=='bool' and not z.is_bool(value)) or (typ!='bool' and not z.is_int(value)):
                raise Unsupported('hash_ABI_argument_sort')
        signature={'algorithm':'keccak256','mode':enc['mode'],'types':normalized,'sorts':[str(x.sort()) for x in values]}
        name='h_'+e.name(signature)
        if name not in e.functions:e.functions[name]=z.Function(name,*[x.sort() for x in values],z.IntSort())
        e.encoding_notes.append({'kind':'keccak_fixed_ABI_congruence','signature':signature,
            'model':'uninterpreted function; no collision-free/injective or preimage assumption',
            'SAT_requires_concrete_confirmation':True})
        e.abstract_hash_used=True
        return e.bound(e.functions[name](*values),'bytes32')
    if (v.get('kind')=='member' and v.get('member')=='length'
        and v.get('base',{}).get('kind')=='member' and v['base'].get('member')=='code'):
        receiver=v['base'].get('base',{});typ=e.typ(receiver)
        if typ not in ('address','address payable') and not typ.startswith('contract '):raise Unsupported('code_length_receiver_not_address')
        declarations={x.get('id',x.get('root')) for x in walk(receiver) if x.get('kind') in ('parameter','storage')}
        if not declarations:raise Unsupported('code_length_source_receiver_missing')
        sourced=any(n.get('nodeType')=='MemberAccess' and n.get('memberName')=='code'
                    and declarations <= {x.get('referencedDeclaration') for x in walk(n.get('expression',{}))}
                    for n in e.lookup.nodes.values())
        if not sourced:raise Unsupported('code_length_not_in_source')
        address=e.expr(receiver);name='env_code_size_by_address'
        if name not in e.functions:e.functions[name]=z.Function(name,z.IntSort(),z.IntSort())
        e.encoding_notes.append({'kind':'source_address_code_length','receiver':receiver,
            'scope':'declared external environment; not evidence of actual deployed bytecode'})
        return e.bound(e.functions[name](address),'uint256')
    return None
