# 实跑源码文本 · 第 15 页

## file-e163d7395879cc

`source/src/pr_next_joint/verification/expressions.py` · 原字节 SHA-256 `57fe986e34c11643995e8551c99920d037a01783f52136e5c41ea0edf53f0a0f`

~~~~python
from pr_next_joint.verification.solver import solve as bounded_solve
"""Z3 checks for source-bound permission predicates, not execution proofs.

Unsigned values use mathematical integers with explicit width constraints;
bitwise operations use unsigned BV conversions. No unknown term is replaced by
an unconstrained atom. Storage is represented by functions of actual keys so
congruence is preserved. SAT is conditional on the stated pre-state, not proof
of deployment reachability or business intent.
"""
import hashlib
from pr_next_joint.frontend.path_ir import key, normalize

class Unsupported(ValueError): pass

class Encoder:
    def __init__(self, lookup):
        import z3
        self.z=z3;self.lookup=lookup;self.constraints=[];self.symbols={};self.functions={};self.domain_constraints=[]

    def name(self,v):return hashlib.sha256(key(v).encode()).hexdigest()[:24]

    def typ(self,v):
        if v.get('kind')=='index' and v.get('base',{}).get('kind')=='parameter':
            typ=v['base'].get('type','')
            if '[' not in typ:raise Unsupported('index_base_not_array')
            element=typ.split('[')[0]
            if typ.count('[')!=1:raise Unsupported('nested_parameter_array_not_lowered')
            return element
        if v.get('kind')=='storage':
            from pr_next_joint.frontend.storage import value_type
            typ=value_type(v,self.lookup)
            if not typ:raise Unsupported('storage_type_not_resolved')
            return typ
        if v.get('kind') in ('actual_sender','contract_address','transaction_origin'):return 'address'
        from pr_next_joint.frontend.language import scalar_type
        return scalar_type(v.get('type','uint256'),self.lookup)

    def width(self,typ):
        import re
        if typ in ('address','address payable') or typ.startswith('contract '):return 160
        if typ.startswith('enum '):return 8
        m=re.fullmatch(r'u?int(\d*)',typ)
        if m:return int(m[1] or 256)
        m=re.fullmatch(r'bytes(\d+)',typ)
        if m:return 8*int(m[1])
        raise Unsupported('unsupported_scalar_type:'+typ)

    def bound(self,x,typ):
        if typ!='bool':
            import re
            signed=bool(re.fullmatch(r'int\d*',typ));bits=self.width(typ)
            domain=[x>=(-2**(bits-1) if signed else 0),x<2**(bits-int(signed))]
            self.constraints.extend(domain);self.domain_constraints.extend(domain)
        return x

    def atom(self,v,typ=None):
        z=self.z;typ=typ or self.typ(v);n=self.name(v)
        if n not in self.symbols:
            self.symbols[n]=z.Bool('b_'+n) if typ=='bool' else self.bound(z.Int('n_'+n),typ)
        elif typ!='bool':self.bound(self.symbols[n],typ)
        return self.symbols[n]

    def expr(self,v):
        z=self.z;v=normalize(v);kind=v.get('kind')
        if not getattr(self,'_encoding_initial',False) and ((kind=='environment' and v.get('field') in ('timestamp','number')) or (kind=='parameter' and v.get('sequence_role') in ('timestamp','number'))):
            self.__dict__.setdefault('_state_times',{})[key(v)]=v
        # All permission routes consume the same source-produced scalar IR.
        # Reuse exact casts/branch constraints; no new policy or symbolic unknown.
        if kind=='op' and v.get('op')=='ite':
            condition,yes,no=v['args']
            return self.expr({'kind':'conditional','condition':condition,'when_true':yes,'when_false':no})
        if kind in ('typed_integer_arithmetic','integer_cast'):
            from pr_next_joint.verification.typed_integer import encode
            return encode(self,v)
        if kind in ('conditional','guarded_evaluation'):
            condition=self.expr(v['condition'])
            if not z.is_bool(condition):raise Unsupported('conditional_guard_not_boolean')
            def branch(value,guard):
                start=len(self.constraints)
                result=self.expr(value)
                constraints=self.constraints[start:];del self.constraints[start:]
                self.constraints.extend(z.Implies(guard,c) for c in constraints)
                return result
            if kind=='guarded_evaluation':
                for value in v['values']:branch(value,condition)
                return z.BoolVal(True)
            positive=branch(v['when_true'],condition)
            negative=branch(v['when_false'],z.Not(condition))
            if positive.sort()!=negative.sort():raise Unsupported('conditional_branch_sort_mismatch')
            return z.If(condition,positive,negative)
        if kind=='literal':
            if type(v['value']) is bool:return z.BoolVal(v['value'])
            if type(v['value']) is int:return z.IntVal(v['value'])
            raise Unsupported('literal_type')
        if kind=='array_length':
            import re
            base=v.get('array',{})
            if base.get('kind')!='parameter':raise Unsupported('array_length_source_not_parameter')
            typ=base.get('type','')
            if typ.count('[')!=1:raise Unsupported('array_length_dimension_not_lowered')
            fixed=re.match(r'^[^\[]+\[(\d+)\]',typ)
            return z.IntVal(int(fixed.group(1))) if fixed else self.atom(v,'uint256')
        if kind in ('actual_sender','transaction_origin','contract_address','environment','transaction_value'):
            return self.atom(v)
        if kind=='parameter':
            if '[' in v.get('type',''):raise Unsupported('array_used_as_scalar')
            return self.atom(v)
        if kind=='storage':
            if not getattr(self,'_encoding_initial',False):
                self.__dict__.setdefault('_state_cells',{})[key(v)]=v
            args=[];shape=[]
            declaration=self.lookup.nodes.get(v['root'],{}).get('typeName',{})
            for seg in v.get('segments',[]):
                if 'key' in seg:
                    index=seg['key']
                    if index.get('kind')=='fixed_bytes_literal':
                        from pr_next_joint.graph.object_equivalence import literal_key
                        arg=z.IntVal(literal_key(index,declaration))
                    else:
                        arg=self.expr(index)
                    args.append(arg);shape.append({'key_sort':str(arg.sort())})
                    declaration=declaration.get('valueType',declaration.get('baseType',{}))
                elif 'field' in seg:
                    shape.append({'field':seg['field']})
                    declaration=self.lookup.nodes.get(seg['field'],{}).get('typeName',{})
                elif seg.get('length'):shape.append({'array_length':True})
                else:raise Unsupported('storage_segment')
            if not args:return self.atom(v)
            typ=self.typ(v);ident={'root':v['root'],'instance':v.get('instance'),'shape':shape,'type':typ};n=self.name(ident)
            if n not in self.functions:self.functions[n]=z.Function('s_'+n,*[a.sort() for a in args],z.BoolSort() if typ=='bool' else z.IntSort())
            return self.bound(self.functions[n](*args),typ)
        if kind=='index' and v['base'].get('kind')=='parameter':
            import re
            base=v['base'];typ=self.typ(v);arg=self.expr(v['key']);n=self.name(base)
            if n not in self.functions:self.functions[n]=z.Function('a_'+n,z.IntSort(),z.BoolSort() if typ=='bool' else z.IntSort())
            length=self.expr({'kind':'array_length','array':base,'type':'uint256'})
            self.constraints.extend([arg>=0,arg<length]);return self.bound(self.functions[n](arg),typ)
        if kind=='uint_narrow':return self.expr(v['input']) % 2**v['bits']
        if kind!='op':raise Unsupported('term_not_encoded:'+str(kind))
        if v['op'] in ('and','&&','or','||'):
            conjunction=v['op'] in ('and','&&');prefix=z.BoolVal(True);values=[]
            for term in v['args']:
                start=len(self.constraints);value=self.expr(term)
                if not z.is_bool(value):raise Unsupported('logical_operand_not_boolean')
                branch_constraints=self.constraints[start:];del self.constraints[start:]
                self.constraints.extend(z.Implies(prefix,c) for c in branch_constraints)
                values.append(value);prefix=z.And(prefix,value if conjunction else z.Not(value))
            return z.And(*values) if conjunction else z.Or(*values)
        if v['op']=='**':
            base,exponent=v['args']
            if exponent.get('kind')!='literal':
                # Exact finite no-overflow subdomain for a source constant base.
                # Preserve the exponent as a state/input value; never invent decimals.
                if base.get('kind')!='literal' or type(base.get('value')) is not int or base['value']<2:raise Unsupported('exponent_base_not_source_constant')
                values=[1]
                while len(values)<=256 and values[-1]*base['value']<2**256:values.append(values[-1]*base['value'])
                power=self.expr(exponent)
                if not z.is_int(power):raise Unsupported('exponent_not_integer')
                self.constraints.extend([power>=0,power<len(values)])
                result=z.IntVal(values[-1])
                for i in range(len(values)-2,-1,-1):result=z.If(power==i,z.IntVal(values[i]),result)
                return result
            if type(exponent.get('value')) is not int or not 0<=exponent['value']<=256:
                raise Unsupported('exponent_not_bounded_source_constant')
            if base.get('kind')!='literal' and self.typ(base) not in ('uint','uint256'):
                raise Unsupported('exponent_base_width_not_lowered')
            value=self.expr(base);result=z.IntVal(1)
            for _ in range(exponent['value']):result=result*value
            self.constraints.extend([result>=0,result<2**256])
            return result
        op=v['op'];a=[self.expr(x) for x in v['args']]
        if op in ('and','&&'):return z.And(*a)
        if op in ('or','||'):return z.Or(*a)
        if op=='!':
            if len(a)!=1 or not z.is_bool(a[0]):raise Unsupported('negation_operand_not_boolean')
            return z.Not(a[0])
        if op=='==':return a[0]==a[1]
        if op=='!=':return a[0]!=a[1]
        if op=='<':return a[0]<a[1]
        if op=='<=':return a[0]<=a[1]
        if op=='>':return a[0]>a[1]
        if op=='>=':return a[0]>=a[1]
        if op in ('&','|','^'):
            left,right=[z.Int2BV(x,256) for x in a]
            return z.BV2Int({'&':lambda:left&right,'|':lambda:left|right,'^':lambda:left^right}[op](),is_signed=False)
        if op in ('+','-','*','/','%'):
            from pr_next_joint.frontend.path_ir import walk
            for term in v['args']:
                if term.get('kind') in ('parameter','storage') and self.typ(term) not in ('uint','uint256'):
                    raise Unsupported('arithmetic_width_not_lowered:'+self.typ(term))
            if op in ('/','%'):self.constraints.append(a[1]>0)
            value={'+':lambda:a[0]+a[1],'-':lambda:a[0]-a[1],'*':lambda:a[0]*a[1],'/':lambda:a[0]/a[1],'%':lambda:a[0]%a[1]}[op]()
            self.constraints.extend([value>=0,value<2**256]);return value
        raise Unsupported('operator_not_encoded:'+op)

def check(lookup,guards,required,timeout_ms=1500):
    try:
        e=Encoder(lookup);z=e.z
        g=z.And(*[e.expr(x) for x in guards]);q=e.expr(required)
        solver=z.Solver();solver.set(timeout=timeout_ms);solver.add(*e.constraints);solver.add(g)
        premise=bounded_solve(solver)
        base={'engine':'z3','version':z.get_version_string(),'premise':str(premise),'query':'not_checked',
              'scope':'declared source path and pre-state, not transaction reachability','timeout_ms':timeout_ms}
        if premise!=z.sat:return {**base,'status':'inconclusive','reason':'premise_unsat' if premise==z.unsat else solver.reason_unknown()}
        solver.add(z.Not(q));answer=bounded_solve(solver);base['query']=str(answer)
        if answer==z.unknown:return {**base,'status':'inconclusive','reason':solver.reason_unknown()}
        return {**base,'status':'supported' if answer==z.sat else 'refuted_in_scope',
                'formula_sha256':hashlib.sha256(solver.sexpr().encode()).hexdigest(),
                'encoding':'unsigned bounded Int, unsigned BV bitwise, keyed storage functions'}
    except (ImportError,Unsupported) as error:
        return {'status':'inconclusive','engine':'z3','reason':str(error),'query':'not_encoded'}

~~~~

## file-ea1302f181404d

`source/src/pr_next_joint/verification/hash_confirmation.py` · 原字节 SHA-256 `2c21ab1686e5e4c9b7eb9a1695a5899b71c86ebcf235f1bf7202a046fdda9b39`

~~~~python
"""Hash-abstraction status, without model or candidate extraction.

Literal hashes keep exact source semantics. An active symbolic hash is not
accepted as a positive source proof. No concrete ABI/preimage data is built.
"""

def status(encoder, solver):
    z=encoder.z; rows=getattr(encoder,'hash_terms',{})
    if not rows:return {'status':'not_required'}
    declarations={row['application'].decl() for row in rows.values()}
    pending=[z.simplify(z.And(*solver.assertions()))];seen=set()
    while pending:
        node=pending.pop()
        if node.get_id() in seen:continue
        seen.add(node.get_id())
        if z.is_app(node) and node.decl() in declarations:
            return {'status':'unverified','reason':'symbolic_hash_requires_exact_nonconstructive_proof'}
        if z.is_quantifier(node):pending.append(node.body())
        elif z.is_app(node):pending.extend(node.children())
    return {'status':'not_required','only_inactive_hash_terms':True}

~~~~

## file-3f7b60d04860f8

`source/src/pr_next_joint/verification/joint_encoding.py` · 原字节 SHA-256 `79ce9d8c227056be9754765ccdc17b03ae58fa391f3d4681f321eef168dbd8df`

~~~~python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""
from pr_next_joint.verification.expressions import Encoder, Unsupported
from pr_next_joint.frontend.path_ir import key, op, lit, walk

class JointEncoder(Encoder):
    def __init__(self,lookup):
        super().__init__(lookup);self.encoding_notes=[];self.abstract_hash_used=False
    def expr(self,v):
        if v.get('kind')=='source_linear_quantity':
            terms=v.get('terms',[])
            if not all(type(t.get('coefficient')) is int for t in terms):raise Unsupported('source_delta_coefficient')
            # Signed mathematical difference, not Solidity executed arithmetic.
            # Source execution constraints are still checked separately.
            return self.z.Sum(*[t['coefficient']*self.expr(t['value']) for t in terms]) if terms else self.z.IntVal(0)
        from pr_next_joint.frontend.bytes import encode
        byte_value=encode(self,v)
        if byte_value is not None:return byte_value
        if v.get('kind')=='op' and v.get('op')=='ite':
            condition,yes,no=v['args']
            return super().expr({'kind':'conditional','condition':condition,'when_true':yes,'when_false':no})
        if v.get('kind') in ('typed_integer_arithmetic','integer_cast'):
            from pr_next_joint.verification.typed_integer import encode
            return encode(self,v)
        if v.get('kind')=='guarded_evaluation':
            condition=self.expr(v['condition'])
            if not self.z.is_bool(condition):raise Unsupported('guarded_evaluation_condition_not_boolean')
            values=v.get('values')
            if values is None and 'input' in v:values=[v['input']]
            if not isinstance(values,list):raise Unsupported('guarded_evaluation_values_not_list')
            mark=len(self.constraints)
            for value in values:self.expr(value)
            extra=self.constraints[mark:];del self.constraints[mark:]
            self.constraints.append(self.z.Implies(condition,self.z.And(*extra)))
            return self.z.BoolVal(True)
        if v.get('kind')=='op' and v.get('op') in ('and','&&','or','||'):
            conjunction=v['op'] in ('and','&&');parts=[]
            for arg in v['args']:
                gate=self.z.And(*parts) if conjunction else self.z.Not(self.z.Or(*parts))
                mark=len(self.constraints);value=self.expr(arg);extra=self.constraints[mark:];del self.constraints[mark:]
                if not self.z.is_bool(value):raise Unsupported('logical_operand_not_boolean')
                self.constraints.append(self.z.Implies(gate,self.z.And(*extra)));parts.append(value)
            return self.z.And(*parts) if conjunction else self.z.Or(*parts)
        if v.get('kind')=='checked_evaluation':
            if v.get('type')!='uint256':raise Unsupported('checked_evaluation_type_not_supported')
            result=self.expr(v['input']);self.constraints.extend([result>=0,result<2**256]);return result
        if v.get('kind')=='op' and v.get('op')=='&':
            a,b=v['args']
            if a.get('kind')=='literal':a,b=b,a
            if b.get('kind')=='literal' and type(b.get('value')) is int and 0<=b['value']<2**256:
                bits=[i for i in range(256) if b['value'] & (1<<i)]
                if len(bits)<=16:
                    # Exact unsigned bit extraction. Avoid expensive Int/BV
                    # conversion for a small constant permission mask.
                    x=self.expr(a)
                    return self.z.Sum(*[((x/(1<<i))%2)*(1<<i) for i in bits]) if bits else self.z.IntVal(0)
        from pr_next_joint.verification.joint_intrinsics import intrinsic
        special=intrinsic(self,v)
        if special is not None:return special
        if v.get('kind')=='member' and v.get('member')=='value' and v.get('base',{}).get('kind')=='symbol':
            declaration=v['base'].get('declaration')
            from pr_next_joint.frontend.source_entry_identity import builtin_object
            sourced=any(n.get('nodeType')=='MemberAccess' and n.get('memberName')=='value'
                and n.get('expression',{}).get('nodeType')=='Identifier'
                and n['expression'].get('name')=='msg' and n['expression'].get('referencedDeclaration')==declaration
                and builtin_object(n['expression'],self.lookup,'msg')
                for n in self.lookup.nodes.values())
            if not sourced:raise Unsupported('member_value_not_verified_builtin')
            return self.expr({'kind':'transaction_value','type':'uint256'})
        if v.get('kind')=='source_calldata_length':
            self.encoding_notes.append('source-bound calldata byte length; no ABI minimum or transaction reachability assumed')
            return self.atom(v,'uint256')
        if v.get('kind') in ('transition_caller','transaction_value','native_reserve'):
            return self.atom(v,'address' if v['kind']=='transition_caller' else 'uint256')
        if v.get('kind')=='native_call_success':return self.atom(v,'bool')
        if v.get('kind')=='source_gas_available':
            self.encoding_notes.append('available gas symbolic; no gas sufficiency or transaction execution proof')
            return self.atom(v,'uint256')
        if v.get('kind')=='op' and v.get('op') in ('+','-','*','/','%'):
            # Only arithmetic OPERANDS determine the width; an address used as
            # a mapping index is not an address-valued arithmetic operand.
            args=v['args']
            if len(args)!=2:raise Unsupported('arithmetic_arity')
            for arg in args:
                if arg.get('kind') not in ('op','literal') and self.typ(arg) not in ('uint','uint256'):
                    raise Unsupported('arithmetic_operand_width_not_lowered:'+self.typ(arg))
            left,right=[self.expr(x) for x in args]
            if not self.z.is_int(left) or not self.z.is_int(right):raise Unsupported('arithmetic_operand_sort')
            op=v['op']
            if op in ('/','%'):self.constraints.append(right>0)
            result={'+':lambda:left+right,'-':lambda:left-right,'*':lambda:left*right,'/':lambda:left/right,'%':lambda:left%right}[op]()
            self.constraints.extend([result>=0,result<2**256]);return result
        return super().expr(v)

~~~~

## file-bd42be126f99eb

`source/src/pr_next_joint/verification/joint_intrinsics.py` · 原字节 SHA-256 `f7abeba1589e49b957d3fbd10b7ee63c95c3915ec0b561ab720d264ab20c6ff7`

~~~~python
"""Conservative symbolic intrinsics for source-bound M4 obligations.

Keccak over fixed ABI tuples is a congruent uninterpreted function, without
injectivity or a preimage oracle. UNSAT is usable in that overapproximation;
SAT involving this abstraction is never promoted to a confirmed prediction.
"""
from pr_next_joint.verification.expressions import Unsupported
from pr_next_joint.frontend.path_ir import walk

def intrinsic(e,v):
    z=e.z
    if v.get('kind')=='source_block_hash':
        height=e.expr(v['height']);current=e.expr(v['current'])
        if not z.is_int(height) or not z.is_int(current):raise Unsupported('block_hash_height_sort')
        name='environment_block_hash_by_height'
        if name not in e.functions:e.functions[name]=z.Function(name,z.IntSort(),z.IntSort())
        value=e.bound(e.functions[name](height),'bytes32')
        e.encoding_notes.append({'kind':'source_block_hash_environment','height':v['height'],
            'window':'the 256 preceding blocks; zero outside that window',
            'assumption':'shared conditional chain environment; historical chain values not verified'})
        return z.If(z.And(height<current,current-height<=256),value,z.IntVal(0))
    if v.get('kind')=='hash':
        from pr_next_joint.checks.credentials.credential_encoding import layout
        enc=layout(v)
        types=enc.get('types',[]);args=enc.get('arguments',[])
        if not types or len(types)!=len(args):raise Unsupported('hash_ABI_arity')
        normalized=[]
        for typ in types:
            if '[' in typ or typ in ('bytes','string') or typ.startswith(('struct ','tuple')):raise Unsupported('hash_dynamic_ABI_not_encoded')
            if typ!='bool' and not typ.startswith('fixed_bytes_literal:'):e.width(typ)
            normalized.append('address' if typ.startswith('contract ') else typ)
        from pr_next_joint.checks.credentials.credential_encoding import fixed_literal
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
        application=e.functions[name](*values)
        e.__dict__.setdefault('hash_terms',{})[application.sexpr()]={
            'application':application,'arguments':values,'types':normalized,'mode':enc['mode']}
        return e.bound(application,'bytes32')
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

~~~~

## file-ffe6c34058a481

`source/src/pr_next_joint/verification/program_encoding.py` · 原字节 SHA-256 `4285b3982a5e24bcbffc52e8a19b30e8ac5fddb35ef07041dfa454d60092938e`

~~~~python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""
import copy
from functools import lru_cache
from pr_next_joint.graph.state_relations import scalar as scalar_write
from pr_next_joint.verification.joint_encoding import JointEncoder
from pr_next_joint.verification.expressions import Unsupported
from pr_next_joint.frontend.path_ir import key, op, lit, walk

SECP256K1_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


@lru_cache(maxsize=256)
def exact_recovery(digest, v, r, s):
    """Pure local precompile semantics, not EVM execution or a signing oracle."""
    if v not in (27, 28) or not (0 < r < SECP256K1_ORDER and 0 < s < SECP256K1_ORDER):
        return 0
    if not 0 <= digest < 2 ** 256: raise Unsupported('ecrecover_digest_width')
    from eth_keys.datatypes import Signature
    from eth_keys.backends.native import NativeECCBackend
    from eth_keys.exceptions import BadSignature
    try:
        public = Signature(vrs=(v - 27, r, s), backend=NativeECCBackend()).recover_public_key_from_msg_hash(digest.to_bytes(32, 'big'))
    except BadSignature:
        return 0
    return int.from_bytes(public.to_canonical_address(), 'big')


class MechanismEncoder(JointEncoder):
    def __init__(self, lookup):
        super().__init__(lookup)
        self.credential_terms = {}
        self.expression_cache = {}
        self.expression_cache_hits = 0
        self.expression_visits = 0

    def checkpoint(self):
        """Snapshot every mutable encoder registry for a speculative branch."""
        return {k:(v.copy() if isinstance(v,(dict,list,set)) else v) for k,v in self.__dict__.items()}

    def rollback(self,snapshot):
        self.__dict__.clear()
        self.__dict__.update(snapshot)

    def expr(self,value):
        """Share expression DAGs, replaying their *local* success conditions.

        Returning a cached arithmetic value without its overflow/branch
        conditions would be unsound. Domains and execution conditions are
        therefore stored separately and replayed at each use, where the
        surrounding branch/frame captures them as before. Caches never cross
        an encoder, target, initial/runtime mode or query branch.
        """
        self.expression_visits+=1
        if self.expression_visits%64==1:
            remaining=getattr(self.lookup,'encoding_remaining',None)
            if remaining and remaining()<=0:raise TimeoutError('program_encoding_budget_exhausted')
        token=(bool(getattr(self,'_encoding_initial',False)),key(value))
        cached=self.expression_cache.get(token)
        if cached is not None:
            result,conditions,domains=cached
            if conditions is not None:self.constraints.append(conditions)
            if domains is not None:self.domain_constraints.append(domains)
            self.expression_cache_hits+=1
            return result
        mark,domain_mark=len(self.constraints),len(self.domain_constraints)
        result=self._expr_uncached(value)
        def compact(rows):
            unique={r.get_id():r for r in rows if not self.z.is_true(r)}
            if not unique:return None
            values=list(unique.values())
            # Flatten redundant nested conditions before retaining a DAG.
            # Otherwise serialization can expand repeated And/Implies chains
            # much more than the actual source expression.
            result=self.z.simplify(values[0] if len(values)==1 else self.z.And(*values))
            return None if self.z.is_true(result) else result
        conditions=compact(self.constraints[mark:]);domains=compact(self.domain_constraints[domain_mark:])
        del self.constraints[mark:];del self.domain_constraints[domain_mark:]
        if conditions is not None:self.constraints.append(conditions)
        if domains is not None:self.domain_constraints.append(domains)
        if len(self.expression_cache)>=4096:self.expression_cache.pop(next(iter(self.expression_cache)))
        self.expression_cache[token]=(result,conditions,domains)
        return result

    def credential_status(self, solver):
        """Check exact encoding applicability without requesting assignments.

        Literal recovery and exact invalid domains are already encoded by
        _expr_uncached. An active symbolic recovery function is an unproved
        abstraction: SAT alone cannot establish the original source property.
        """
        z = self.z
        recovery = self.functions.get('source_ecrecover')
        if recovery is None:
            return {'status':'not_required','exact_invalid_domains_preserved':True}
        pending=[z.simplify(z.And(*solver.assertions()))];seen=set()
        while pending:
            node=pending.pop()
            if node.get_id() in seen:continue
            seen.add(node.get_id())
            if z.is_app(node) and node.decl()==recovery:
                return {'status':'unverified','reason':'symbolic_credential_requires_exact_nonconstructive_proof'}
            if z.is_quantifier(node):pending.append(node.body())
            elif z.is_app(node):pending.extend(node.children())
        return {'status':'not_required','exact_invalid_domains_preserved':True}

    def invalid_recovery_subdomain(self,solver):
        """Exact invalid-domain restriction; no concrete signature is chosen.

        It can establish a positive existential subcase only. Failure says
        nothing about valid credentials or the whole original property.
        """
        z=self.z;recovery=self.functions.get('source_ecrecover')
        if recovery is None:return None
        original=z.simplify(z.And(*solver.assertions()))
        pending=[original];seen=set();applications={}
        while pending:
            node=pending.pop()
            if node.get_id() in seen:continue
            seen.add(node.get_id())
            if z.is_quantifier(node):return None
            if z.is_app(node):
                if node.decl()==recovery:applications[node.get_id()]=node
                pending.extend(node.children())
        if not applications:return None
        invalid=[];replacements=[]
        for node in applications.values():
            args=list(node.children())
            if len(args)!=4:return None
            invalid.append(z.Or(z.And(args[1]!=27,args[1]!=28),
                args[2]<=0,args[2]>=SECP256K1_ORDER,args[3]<=0,args[3]>=SECP256K1_ORDER))
            replacements.append((node,z.IntVal(0)))
        # Under these exact precompile failure conditions every recovery
        # application is zero. No symbolic successful recovery is trusted.
        restricted=z.simplify(z.substitute(z.And(original,*invalid),*replacements))
        result=z.Solver();result.add(restricted)
        return result

    def bound(self,x,typ):
        from pr_next_joint.graph.state_relations import enum_size
        size=enum_size(self.lookup,typ)
        if size is not None:
            domain=[x>=0,x<size];self.constraints.extend(domain);self.domain_constraints.extend(domain);return x
        return super().bound(x,typ)

    def _expr_uncached(self, value):
        if isinstance(value,dict) and value.get("kind")=="source_linear_quantity":
            # Mathematical before/after difference, not an executed unsigned
            # Solidity subtraction. Executed arithmetic is checked separately.
            terms=value["terms"]
            if not all(type(x.get("coefficient")) is int for x in terms):raise Unsupported("source_delta_coefficient")
            return self.z.Sum(*[x["coefficient"]*self.expr(x["value"]) for x in terms]) if terms else self.z.IntVal(0)

        if value.get('kind')=='checked_evaluation':
            if value.get('type')!='uint256':raise Unsupported('checked_evaluation_type_not_supported')
            evaluated=self.expr(value['input'])
            # An arithmetic success condition belongs to this path, unlike
            # a symbol's type domain. Keep it inside a negated continuation.
            self.constraints.extend([evaluated>=0,evaluated<2**256])
            return evaluated
        if value.get('kind')=='source_pure_memory_word':
            raise Unsupported('pure_memory_word_required_by_this_check_not_encoded')
        if value.get('kind')=='fixed_bytes_literal':
            raise Unsupported('fixed_bytes_literal_outside_typed_hash_layout')
        if value.get('kind')=='enum_cast':
            node=self.lookup.nodes.get(value['enum_ast_id'],{})
            if node.get('nodeType')!='EnumDefinition' or len(node['members'])!=value['members']:
                raise Unsupported('enum_cast_source_identity')
            x=self.expr(value['input']);self.constraints.extend([x>=0,x<value['members']]);return x
        if value.get('kind')=='op' and value.get('op') in ('%','/'):
            a,b=value['args']
            if a.get('kind')=='uint_narrow' and b.get('kind')=='literal' and type(b.get('value')) is int and 0<b['value']<2**a['bits']:
                x=self.expr(a);d=b['value']
                return x%d if value['op']=='%' else x/d
        if value.get('kind')=='op' and value.get('op') in ('<<','>>'):
            left,right=value['args'];bits=self.width(self.typ(left))
            a,b=self.expr(left),self.expr(right)
            av,bv=self.z.Int2BV(a,bits),self.z.Int2BV(b,bits)
            shifted=(av<<bv) if value['op']=='<<' else self.z.LShR(av,bv)
            return self.z.If(b>=bits,self.z.IntVal(0),self.z.BV2Int(shifted,is_signed=False))
        if (value.get('kind') == 'member' and value.get('member') == 'chainid'
                and value.get('base', {}).get('kind') == 'symbol'):
            decl = value['base'].get('declaration')
            from pr_next_joint.frontend.source_entry_identity import builtin_object
            if not (type(decl) is int and any(
                    n.get('nodeType') == 'MemberAccess' and n.get('memberName') == 'chainid'
                    and n.get('expression', {}).get('referencedDeclaration') == decl
                    and builtin_object(n.get('expression',{}),self.lookup,'block')
                    for n in self.lookup.nodes.values())):
                raise Unsupported('chainid_not_bound_to_source_builtin')
            return self.atom({'kind': 'environment', 'field': 'chainid', 'type': 'uint256'})
        if value.get('kind') == 'op' and value.get('op') == 'ite':
            condition,yes,no=value['args']
            return super().expr({'kind':'conditional','condition':condition,'when_true':yes,'when_false':no})
        if value.get('kind') == 'credential_recovery':
            args = [self.expr(value['digest'])] + [self.expr(x) for x in value['signature']]
            z = self.z
            simplified = [z.simplify(a) for a in args]
            invalid = z.Or(z.And(args[1] != 27, args[1] != 28), args[2] <= 0, args[2] >= SECP256K1_ORDER,
                           args[3] <= 0, args[3] >= SECP256K1_ORDER)
            if z.is_true(z.simplify(invalid)):
                self.encoding_notes.append({'kind': 'ecrecover_exact_failure_domain'})
                return z.IntVal(0)
            if all(z.is_int_value(a) for a in simplified):
                self.encoding_notes.append({'kind': 'ecrecover_exact_constant_arguments'})
                return z.IntVal(exact_recovery(*[a.as_long() for a in simplified]))
            name = 'source_ecrecover'
            if name not in self.functions:
                self.functions[name] = self.z.Function(name, *[a.sort() for a in args], self.z.IntSort())
            self.encoding_notes.append({'kind': 'credential_recovery_congruence',
                'scope': 'same digest and same signature recover same address; not a signature forgery proof'})
            application = self.functions[name](*args)
            recovered = self.bound(application, 'address')
            self.credential_terms[application.sexpr()] = {'args': args, 'application': application}
            self.encoding_notes.append({'kind': 'ecrecover_validity_dependency',
                'scope': 'exact v/r/s failure domains; successful symbolic witnesses require recovery validation'})
            return z.If(invalid, z.IntVal(0), recovered)
        return super().expr(value)

def execution_terms(path,lookup):
    """Fail closed if a new consumer cannot retain successful evaluation."""
    if path.get('evaluation_trace_kind')!='downstream_evaluated_expressions_v1':
        raise Unsupported('successful_evaluation_trace_missing')
    if path.get('evaluation_gaps'):
        raise Unsupported('successful_evaluation_incomplete:'+','.join(sorted(set(path['evaluation_gaps']))))
    terms=copy.deepcopy(path['evaluated_terms'])
    for raw in path['writes']:
        w=scalar_write(raw,lookup)
        terms.extend([w['path'],w['value']])
    if path.get('return_value') is not None:
        terms.append(copy.deepcopy(path['return_value']))
    return terms

~~~~

## file-84438fe68c1474

`source/src/pr_next_joint/verification/sequence.py` · 原字节 SHA-256 `1d3d3c3409972c4e971cc3cfd0c01db0310478c7a3b07f3fe0fee40c484e90d1`

~~~~python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""
import copy
from pr_next_joint.frontend.path_ir import key, op, lit
from pr_next_joint.graph.state_relations import compose_read, expand_write
from pr_next_joint.verification.expressions import Unsupported

def qualify(value,step):
    if isinstance(value,dict):
        kind=value.get('kind')
        if kind=='actual_sender':return {'kind':'parameter','id':-9000000-step,'type':'address','sequence_role':'caller','step':step}
        if kind=='parameter':return {**value,'id':-((step+1)*10000000+abs(int(value['id']))),'step':step}
        if kind=='environment' and value.get('field') in ('timestamp','number'):
            return {'kind':'parameter','id':-(81000000+step*10+('timestamp','number').index(value['field'])),
                    'type':'uint256','sequence_role':value['field'],'step':step}
        if kind in ('transaction_origin','source_calldata_length','native_call_success'):
            return {**value,'sequence_step':step}
        if kind in ('transaction_value','block_timestamp','block_number'):
            return {'kind':'parameter','id':-(80000000+step*10+('transaction_value','block_timestamp','block_number').index(kind)),
                    'type':'uint256','sequence_role':kind,'step':step}
        return {k:qualify(v,step) for k,v in value.items()}
    return [qualify(v,step) for v in value] if isinstance(value,list) else value

def compose(lookup,steps,equalities=(),*,step_offset=0):
    if not 1<=len(steps)<=3:raise Unsupported('v20_transaction_sequence_bound')
    if type(step_offset) is not int or step_offset<0 or step_offset+len(steps)>3:raise Unsupported('sequence_namespace_bound')
    writes=[];guards=[];evaluated=[];trace=[]
    for local_i,(fn,pi,path) in enumerate(steps):
        i=local_i+step_offset
        if path['flow'] not in ('normal','returned') or path['issues'] or path.get('evaluation_gaps'):raise Unsupported('v20_sequence_path_incomplete')
        before=copy.deepcopy(writes)
        g=[read(qualify(x,i),before,lookup) for x in path['guards']]
        guards+=g
        evaluated.extend(read(qualify(v,i),before,lookup) for v in path.get('evaluated_terms',[]))
        stepwrites=[]
        for w in path['writes']:
            for e in expand_write(w,lookup):
                q=qualify(e,i)
                # Each path value already includes same-call substitutions.
                q['value']=read(q['value'],before,lookup)
                # Bind indexed keys using pre-state, never replace the location itself.
                q['path']={**q['path'],'segments':read(q['path'].get('segments',[]),before,lookup)}
                stepwrites.append(q)
        writes+=stepwrites
        if local_i:
            for field in ('timestamp','number'):
                now=qualify({'kind':'environment','field':field},i)
                prev=qualify({'kind':'environment','field':field},i-1)
                guards.append(op('>=',now,prev))
        trace.append({'step':i,'function':fn,'path_index':pi,'caller':qualify({'kind':'actual_sender'},i),'writes':stepwrites,'before_writes':before})
    guards.extend(copy.deepcopy(equalities))
    return {'conditions':guards,'writes':writes,'evaluation_terms':evaluated,'steps':trace,
            'assumption':'source-matched sequence from declared symbolic prestate; deployment prefix not proved'}

def read(value,writes,lookup):
    """Resolve key expressions from the pre-state as well as stored values."""
    if isinstance(value,dict):
        if value.get('kind')=='storage':
            prepared={**value,'segments':read(value.get('segments',[]),writes,lookup)}
            return compose_read(prepared,writes,lookup)
        return {k:read(v,writes,lookup) for k,v in value.items()}
    return [read(v,writes,lookup) for v in value] if isinstance(value,list) else value

~~~~

## file-fb58d6ac8c4d16

`source/src/pr_next_joint/verification/solver.py` · 原字节 SHA-256 `5c91451537f3982b6af3754b5a0dd3baf12bccc81cb0bd0ac4ea021e67bb7dca`

~~~~python
"""Per-analysis finite solver budget; UNKNOWN never becomes refutation."""
import time
from contextlib import contextmanager
from contextvars import ContextVar
_current=ContextVar('v20_solver_budget',default=None)
_remaining_program=ContextVar('remaining_cooperative_program_budget',default=None)

@contextmanager
def budget(seconds=120.0,remaining=None):
    state={'limit_seconds':float(seconds),'used_seconds':0.0,'calls':0,'upgrades':0,'budget_exhausted':0,'events':[]}
    token=_current.set(state);other=_remaining_program.set(remaining)
    try:yield state
    finally:_current.reset(token);_remaining_program.reset(other)

def solve(solver,initial_ms=3000,upgrade=False):
    import z3
    b=_current.get()
    # SCRV's common verifier is always enabled. Legacy variant switches and
    # their report side effects are not part of this successor's entry.
    def remaining():
        solver_ms=max(0,int((b['limit_seconds']-b['used_seconds'])*1000)) if b else initial_ms+10000
        callback=_remaining_program.get()
        return min(solver_ms,max(0,int(callback()*1000))) if callback is not None else solver_ms
    if remaining()<1:
        if b:b['budget_exhausted']+=1
        return z3.unknown
    limit=min(initial_ms,remaining())
    solver.set(timeout=limit,random_seed=0)
    start=time.perf_counter();answer=solver.check();elapsed=time.perf_counter()-start
    if b:b['used_seconds']+=elapsed;b['calls']+=1
    reason=solver.reason_unknown() if answer==z3.unknown else None
    if upgrade and answer==z3.unknown and reason and any(w in reason.lower() for w in ('timeout','canceled')) and remaining()>0:
        limit=min(10000,remaining());solver.set(timeout=limit)
        start=time.perf_counter();answer=solver.check();elapsed2=time.perf_counter()-start
        if b:b['used_seconds']+=elapsed2;b['calls']+=1;b['upgrades']+=1
        if b:b['events'].append({'kind':'bounded_timeout_upgrade','first_seconds':elapsed,'additional_seconds':elapsed2,'answer':str(answer)})
    return answer

def status():
    b=_current.get()
    return dict(b) if b else {'scope':'no_active_analysis_budget'}

~~~~

## file-1a4dd2e9319708

`source/src/pr_next_joint/verification/source_worlds.py` · 原字节 SHA-256 `c154a0498a3ca63a31221e6883e7fcc2e3107a7e197ec728376a4cb76c8f09e3`

~~~~python
"""Explicit source frames and forked worlds. No early-pruning optimization."""
import copy
import itertools
from pr_next_joint.frontend.path_ir import op, lit, key
from pr_next_joint.verification.sequence import qualify, read, compose
from pr_next_joint.verification.expressions import Unsupported


def successful(path):
    return path['flow'] in ('normal', 'returned') and not path.get('issues') and not path.get('evaluation_gaps')


def frame(facts, oid, pid, slot, before=(), path_override=None):
    item = facts.paths[pid]
    if item['operation'] != oid: raise Unsupported('frame_operation_identity')
    p = item['raw'] if path_override is None else path_override; lookup = facts.lookup(oid)
    if not successful(p): raise Unsupported('source_semantics_unavailable:' + pid)
    translate = lambda v: read(qualify(v, slot), before, lookup)
    writes = []
    for w in p['writes']:
        q = qualify(w, slot)
        q['path']['segments'] = read(q['path'].get('segments', []), before, lookup)
        q['value'] = read(q['value'], before, lookup)
        writes.append(q)
    effects = [translate(e) for e in p.get('sensitive_effects', [])]
    return {'operation': oid, 'path': pid, 'slot': slot, 'before': copy.deepcopy(list(before)),
            'guards': [translate(g) for g in p['guards']], 'writes': writes, 'effects': effects,
            'evaluated_terms': [translate(x) for x in p.get('evaluated_terms', [])],
            'caller': qualify({'kind': 'actual_sender'}, slot),
            'evidence_world': 'original_source_success_path'}


def encode_frame(encoder, f, extras=()):
    """All evaluation obligations stay inside this world's success formula.

    In particular ATTEMPT arithmetic and guards are not asserted globally
    before negating a success predicate.
    """
    mark = len(encoder.constraints)
    for x in f.get('evaluated_terms', []): encoder.expr(x)
    for w in f.get('writes', []):
        encoder.expr(w['path']); encoder.expr(w['value'])
    terms = [encoder.expr(x) for x in f['guards']] + list(extras)
    conditions = encoder.constraints[mark:]
    del encoder.constraints[mark:]
    return encoder.z.And(*conditions, *terms)


def bind_keys(a, b):
    from pr_next_joint.frontend.storage import keys, fields
    if a['root'] != b['root'] or fields(a) != fields(b) or key(a.get('instance')) != key(b.get('instance')):
        raise Unsupported('world_object_family_mismatch')
    aa, bb = keys(a), keys(b)
    if len(aa) != len(bb): raise Unsupported('world_key_arity')
    return [op('==', x, y) for x, y in zip(aa, bb)]


def serialize_world(f, name):
    return {'world': name, 'operation': f['operation'], 'path': f['path'], 'slot': f['slot'],
            'caller': f['caller'], 'guards': f['guards'], 'committed_writes': f['writes'],
            'before_writes': f['before'], 'evaluated_terms': f['evaluated_terms']}

~~~~

## file-c7ef015a991b87

`source/src/pr_next_joint/verification/typed_integer.py` · 原字节 SHA-256 `69ac684baea6edfaafaf980a1a821cba165b5416c0a973ba60594ea8c01b7697`

~~~~python
"""Compiler-width arithmetic; no unsigned widening of signed source values."""
import re
from pr_next_joint.verification.expressions import Unsupported

def integer_type(typ):
    m=re.fullmatch(r'(u?int)(\d*)',typ or '')
    return (m[1]=='int',int(m[2] or 256)) if m else None

def checked_mode(lookup,state):
    import json
    raw=lookup.bundle.get('compiler',{})
    text=raw.get('version',raw.get('compiler_version','')) if isinstance(raw,dict) else str(raw)
    if not text:text=str(lookup.bundle.get('compiler_version',''))
    m=re.search(r'(\d+)\.(\d+)\.(\d+)',text)
    if not m:raise Unsupported('integer_compiler_version_missing')
    return tuple(map(int,m.groups()))>=(0,8,0) and not state.get('_unchecked_depth',0)

def encode(e,v):
    typ=integer_type(v.get('type'))
    if typ is None:raise Unsupported('integer_type_unresolved')
    signed,bits=typ;z=e.z;low=-2**(bits-1) if signed else 0;high=2**(bits-int(signed))
    if v['kind']=='integer_cast':value=e.expr(v['input'])
    else:
        args=[e.expr(a) for a in v['args']];operator=v['operator']
        if not all(z.is_int(x) for x in args):raise Unsupported('integer_operand_sort')
        if len(args)==1:
            if operator!='-':raise Unsupported('integer_unary_operator')
            value=-args[0]
        else:
            a,b=args
            if operator in ('/','%'):
                e.constraints.append(b!=0)
                absolute=z.Abs(a)/z.Abs(b);quotient=z.If((a<0)!=(b<0),-absolute,absolute)
                value=quotient if operator=='/' else a-quotient*b
            elif operator in ('+','-','*'):value={'+':lambda:a+b,'-':lambda:a-b,'*':lambda:a*b}[operator]()
            else:raise Unsupported('integer_operator_not_lowered')
        if v.get('checked'):
            e.constraints.extend([value>=low,value<high]);return value
    unsigned=value%(2**bits)
    return z.If(unsigned>=2**(bits-1),unsigned-2**bits,unsigned) if signed else unsigned

~~~~

## file-4b671c2a861b4b

`supplement/CHANGE.patch` · 原字节 SHA-256 `382c0dbe4f07d87242365deeb64274911f8509dde717e12f4cd1f27910f1b115`

~~~~text
--- 
+++ 
@@ -504,7 +504,7 @@
                     'property': prop['id'], 'key': validation_key(prop),
                     'reason': 'same source, domain, subjects, effects, assumptions and semantic meaning'})
                 return
-        if self.f.options.scope=='FCR' and not q['current'].get('_host_property_parent'):
+        if q['property'] is not None and self.f.options.scope=='FCR' and not q['current'].get('_host_property_parent'):
             # One source operation may support two distinct capabilities. Fork
             # only its actually typed effects, never a write-point x five grid.
             for category in prop['possible_categories']:

~~~~
