from .m20_solver import solve as bounded_solve
"""Z3 checks for source-bound permission predicates, not execution proofs.

Unsigned values use mathematical integers with explicit width constraints;
bitwise operations use unsigned BV conversions. No unknown term is replaced by
an unconstrained atom. Storage is represented by functions of actual keys so
congruence is preserved. SAT is conditional on the stated pre-state, not proof
of deployment reachability or business intent.
"""
import hashlib
from .m03_p_paths import key, normalize

class Unsupported(ValueError): pass

class Encoder:
    def __init__(self, lookup):
        import z3
        self.z=z3;self.lookup=lookup;self.constraints=[];self.symbols={};self.functions={}

    def name(self,v):return hashlib.sha256(key(v).encode()).hexdigest()[:24]

    def typ(self,v):
        if v.get('kind')=='index' and v.get('base',{}).get('kind')=='parameter':
            typ=v['base'].get('type','')
            if '[' not in typ:raise Unsupported('index_base_not_array')
            element=typ.split('[')[0]
            if typ.count('[')!=1:raise Unsupported('nested_parameter_array_not_lowered')
            return element
        if v.get('kind')=='storage':
            from .m03_p_route import value_type
            typ=value_type(v,self.lookup)
            if not typ:raise Unsupported('storage_type_not_resolved')
            return typ
        if v.get('kind') in ('actual_sender','contract_address','transaction_origin'):return 'address'
        from .m11_language import scalar_type
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
            self.constraints.extend([x>=(-2**(bits-1) if signed else 0),x<2**(bits-int(signed))])
        return x

    def atom(self,v,typ=None):
        z=self.z;typ=typ or self.typ(v);n=self.name(v)
        if n not in self.symbols:
            self.symbols[n]=z.Bool('b_'+n) if typ=='bool' else self.bound(z.Int('n_'+n),typ)
        elif typ!='bool':self.bound(self.symbols[n],typ)
        return self.symbols[n]

    def expr(self,v):
        z=self.z;v=normalize(v);kind=v.get('kind')
        # All permission routes consume the same source-produced scalar IR.
        # Reuse exact casts/branch constraints; no new policy or symbolic unknown.
        if kind=='op' and v.get('op')=='ite':
            condition,yes,no=v['args']
            return self.expr({'kind':'conditional','condition':condition,'when_true':yes,'when_false':no})
        if kind in ('typed_integer_arithmetic','integer_cast'):
            from .typed_integer import encode
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
            args=[];shape=[]
            declaration=self.lookup.nodes.get(v['root'],{}).get('typeName',{})
            for seg in v.get('segments',[]):
                if 'key' in seg:
                    index=seg['key']
                    if index.get('kind')=='fixed_bytes_literal':
                        from .m29_keys import literal_key
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
            from .m03_p_paths import walk
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
