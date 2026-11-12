# 源码文本 · 17

## source/src/pr_next_joint/verification/program_encoding.py

原文件 SHA-256 `e4a43ac4db3df9cbcb6aa170042462631b07043c38e3cf3d734ba6fd18fb8b6f`

````python
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

    def credential_witness(self, solver, initial_ms=3000):
        """Validate only credential terms used by this successful query.

        A single bounded witness completion may pin candidate signature inputs
        and replace their UF values by exact local recovery. Failure of that
        completion is NOT a refutation of the original existential query.
        """
        z = self.z
        recovery = self.functions.get('source_ecrecover')
        if recovery is None:
            return {'status':'not_required','exact_invalid_domains_preserved':True},solver.model()
        original = z.And(*solver.assertions())
        simplified = z.simplify(original)
        def nodes(value):
            todo=[value];seen=set()
            while todo:
                node=todo.pop();ident=node.get_id()
                if ident in seen:continue
                seen.add(ident);yield node
                if z.is_quantifier(node):todo.append(node.body())
                elif z.is_app(node):todo.extend(node.children())
        all_nodes=list(nodes(simplified))
        # Simplification can change a call's argument syntax. Match the actual
        # recovery function in the consumed formula, not a stale IR string.
        applications = {node.get_id(): node for node in all_nodes
                        if z.is_app(node) and node.decl() == recovery}
        active = [{'application': node, 'args': list(node.children())} for node in applications.values()]
        if not active: return {'status': 'not_required', 'exact_invalid_domains_preserved': True}, solver.model()
        if any(z.is_quantifier(node) for node in all_nodes):
            return {'status': 'unverified', 'reason': 'symbolic_credential_in_quantified_world'}, None
        model = solver.model(); substitutions, pins, evidence = [], [], []
        try:
            for row in active:
                values = [model.eval(arg, model_completion=True) for arg in row['args']]
                if not all(z.is_int_value(v) for v in values):
                    return {'status': 'unverified', 'reason': 'credential_arguments_not_concrete'}, None
                integers = [v.as_long() for v in values]
                recovered = exact_recovery(*integers)
                substitutions.append((row['application'], z.IntVal(recovered)))
                pins.extend(a == v for a, v in zip(row['args'], values))
                pins.append(row['application'] == recovered)
                evidence.append({'arguments': integers, 'recovered_address': recovered,
                                 'method': 'eth_keys_native_exact_recovery', 'evm_execution': False})
        except Exception as error:
            return {'status': 'unverified', 'reason': 'credential_validation:' + type(error).__name__ + ':' + str(error)}, None
        checked = z.substitute(simplified, *substitutions)
        if z.is_true(model.eval(checked, model_completion=True)):
            return {'status': 'verified', 'method': 'original_witness_checked_with_exact_recovery', 'calls': evidence}, model
        from pr_next_joint.verification.solver import solve
        concrete = z.Solver(); concrete.add(*solver.assertions(), *pins)
        answer = solve(concrete, initial_ms=initial_ms)
        record = {'status': 'verified' if answer == z.sat else 'unverified',
                  'method': 'one_bounded_exact_recovery_witness_completion', 'calls': evidence,
                  'completion_answer': str(answer), 'witness_formula': concrete.sexpr(),
                  'completion_failure_is_not_risk_refutation': True}
        if answer != z.sat:
            record['reason'] = 'credential_witness_completion_unfinished' if answer == z.unknown else 'candidate_signature_does_not_validate_risk_witness'
        return record, concrete.model() if answer == z.sat else None

    def bound(self,x,typ):
        from pr_next_joint.graph.state_relations import enum_size
        size=enum_size(self.lookup,typ)
        if size is not None:
            domain=[x>=0,x<size];self.constraints.extend(domain);self.domain_constraints.extend(domain);return x
        return super().bound(x,typ)

    def expr(self, value):
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

````

## source/src/pr_next_joint/verification/sequence.py

原文件 SHA-256 `1d3d3c3409972c4e971cc3cfd0c01db0310478c7a3b07f3fe0fee40c484e90d1`

````python
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

````

## source/src/pr_next_joint/verification/solver.py

原文件 SHA-256 `5c91451537f3982b6af3754b5a0dd3baf12bccc81cb0bd0ac4ea021e67bb7dca`

````python
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

````

## source/src/pr_next_joint/verification/source_worlds.py

原文件 SHA-256 `c154a0498a3ca63a31221e6883e7fcc2e3107a7e197ec728376a4cb76c8f09e3`

````python
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

````

## source/src/pr_next_joint/verification/typed_integer.py

原文件 SHA-256 `69ac684baea6edfaafaf980a1a821cba165b5416c0a973ba60594ea8c01b7697`

````python
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

````

