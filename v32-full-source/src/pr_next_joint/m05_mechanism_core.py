from .m20_solver import solve as bounded_solve
"""Shared source transitions and query-scoped proofs for M2 obligations.

This consumer is downstream of the immutable M2 request. It does not alter
messages, synthesize a policy from a case identifier, or execute Solidity.
"""
import copy
import hashlib
from .source_entry_identity import elementary_expression_name
from .core import digest
from .m03_p_paths import key, walk, op, lit, normalize, conditions_possible
from .m03_p_assets import AssetPaths
from .m03_p_route import keys, fields, value_type
from .m04_joint_formal import JointEncoder
from .m04_logic import Unsupported
from .source_entry_identity import function_kind


class MechanismPaths(AssetPaths):
    captures_evaluated_terms=True
    def __init__(self, *args):
        super().__init__(*args)
        self.expression_depth = 0
        self.source_evaluation_steps=0
        self.max_source_evaluation_steps=2048

    def evaluate(self, node, env):
        self.source_evaluation_steps+=1
        if self.source_evaluation_steps>self.max_source_evaluation_steps:
            raise ValueError('source_operation_evaluation_bound_exceeded:2048')
        # Preserve evaluated arithmetic even if a local is later overwritten.
        # This is downstream expression lowering, not source-anchor discovery.
        state=self.current
        start=len(state.get('evaluated_terms',[])) if state is not None else 0
        counts={k:len(state.get(k,[])) for k in ('guards','issues','evaluation_gaps','source_calls','read_calls')} if state is not None else {}
        value=self._evaluate(node,env)
        typ=(node or {}).get('typeDescriptions',{}).get('typeString','')
        if typ.startswith('int_const'):
            from .source_scalar_semantics import constant_integer
            constant=constant_integer(node)
            if constant is not None:value=lit(constant)
        if state is not None:
            if (node and (node.get('nodeType')=='Conditional')
                    and (len(state.get('evaluated_terms',[]))>start or any(len(state.get(k,[]))!=v for k,v in counts.items()))):
                state.setdefault('evaluation_gaps',[]).append('conditional_fallible_evaluation_order_not_lowered')
            source_math=bool(node and node.get('nodeType')=='BinaryOperation' and node.get('operator') in ('+','-','*','/','%','**') and typ in ('uint','uint256'))
            fallible=(source_math or value.get('kind') in ('index','uint_narrow','enum_cast','typed_integer_arithmetic','integer_cast','unknown','call_unresolved') or
                value.get('kind')=='op' and value.get('op') in ('+','-','*','/','%','**','<<','>>'))
            if fallible:
                typ=(node or {}).get('typeDescriptions',{}).get('typeString','')
                if value.get('kind')=='op' and typ.startswith(('uint','int')) and not typ.startswith('int_const') and typ!='uint256':
                    state.setdefault('evaluation_gaps',[]).append('evaluated_arithmetic_width_not_uint256')
                saved=({'kind':'checked_evaluation','type':typ,'input':copy.deepcopy(value)}
                    if (value.get('kind')=='op' or source_math) and typ in ('uint','uint256') else copy.deepcopy(value))
                state.setdefault('evaluated_terms',[]).append(saved)
            if node and node.get('nodeType')=='IndexAccess' and value.get('kind')=='storage':
                base_type=node.get('baseExpression',{}).get('typeDescriptions',{}).get('typeString','')
                base_id=node.get('baseExpression',{}).get('typeDescriptions',{}).get('typeIdentifier','')
                # mapping(address => T[]) indexes an address, not an array.
                # Bounds apply only when the indexed expression itself is an array.
                is_array=base_id.startswith('t_array') or (not base_id and not base_type.lstrip().startswith('mapping') and '[' in base_type)
                if is_array:
                    length_node={'nodeType':'MemberAccess','memberName':'length','expression':node['baseExpression']}
                    length=super().evaluate(length_node,env);index=self.value(node['indexExpression'],env)
                    if length.get('kind')=='unknown':state.setdefault('evaluation_gaps',[]).append('storage_array_bounds_not_lowered')
                    else:state['guards'].append(op('and',op('>=',index,lit(0)),op('<',index,length)))
        return value

    def put(self,node,value,state,source,operator='='):
        from .source_local_defaults import constant_local_update
        constant=constant_local_update(self,node,value,state,source,operator)
        if constant is not None:return constant
        if (node.get('nodeType')=='Identifier' and node.get('referencedDeclaration') in state['env']
                and operator not in ('=','delete')):
            before=copy.deepcopy(state['env'][node['referencedDeclaration']])
            typ=node.get('typeDescriptions',{}).get('typeString','')
            if typ!='uint256':
                from .typed_integer import integer_type,checked_mode
                if integer_type(typ):
                    actual={'kind':'typed_integer_arithmetic','type':typ,'operator':operator[:-1],
                        'args':[before,copy.deepcopy(value)],'checked':checked_mode(self,state)}
                    state.setdefault('evaluated_terms',[]).append(copy.deepcopy(actual))
                    state['env'][node['referencedDeclaration']]=actual
                    return copy.deepcopy(actual)
                state.setdefault('evaluation_gaps',[]).append('local_compound_arithmetic_type_unresolved')
            else:state.setdefault('evaluated_terms',[]).append({'kind':'checked_evaluation','type':typ,
                'input':op(operator[:-1],before,copy.deepcopy(value))})
        mark=len(state['writes'])
        result=super().put(node,value,state,source,operator)
        # Every modeled uint256 write participates in the explicit no-wrap
        # subcase, including compound storage updates inside unchecked blocks.
        from .m03_p_route import value_type
        for write in state['writes'][mark:]:
            if value_type(write['path'],self) in ('uint','uint256') and write['value'].get('kind')=='op':
                state.setdefault('evaluated_terms',[]).append({'kind':'checked_evaluation','type':'uint256','input':copy.deepcopy(write['value'])})
        return result

    def run(self,signature):
        self.source_evaluation_steps=0
        self.read_calls.summaries={}
        from .source_work_budget import begin,end,snapshot
        token=begin()
        try:result=super().run(signature)
        finally:
            if not hasattr(self,"normalization_profiles"):self.normalization_profiles={}
            self.normalization_profiles[signature]={**snapshot(),"source_evaluation_steps":self.source_evaluation_steps}
            end(token)
        for path in result:
            path.setdefault('evaluated_terms',[])
            path.setdefault('evaluation_gaps',[])
            path['evaluation_trace_kind']='downstream_evaluated_expressions_v1'
        return result

    def _evaluate(self, node, env):
        if (node and node.get('nodeType')=='MemberAccess' and node.get('memberName')=='length'
                and node.get('expression',{}).get('nodeType')=='Identifier'
                and node['expression'].get('typeDescriptions',{}).get('typeIdentifier','').startswith('t_bytes_')):
            base=self.value(node['expression'],env)
            if base.get('kind')=='parameter' and base.get('type','').startswith('bytes'):
                from .m21_bytes import length
                return length(base)
        from .typed_integer import integer_type,checked_mode
        typ=(node or {}).get('typeDescriptions',{}).get('typeString','');integer=integer_type(typ)
        if node and node.get('nodeType')=='BinaryOperation' and typ=='uint256' and node.get('operator') in ('+','-','*','/','%'):
            operands=(node['leftExpression'],node['rightExpression'])
            types=[integer_type(a.get('typeDescriptions',{}).get('typeString')) for a in operands]
            if any(t and not t[0] and t[1]<256 for t in types):
                return {'kind':'typed_integer_arithmetic','type':typ,'operator':node['operator'],
                        'args':[self.value(a,env) for a in operands],'checked':checked_mode(self,self.current)}
        if node and node.get('nodeType')=='BinaryOperation' and node.get('operator') in ('==','!='):
            # Solidity right-pads a literal when converted to a typed bytesN in a comparison.
            import re
            operands=(node['leftExpression'],node['rightExpression'])
            for literal,other in (operands,operands[::-1]):
                size=re.fullmatch(r'bytes([1-9]|[12][0-9]|3[0-2])',other.get('typeDescriptions',{}).get('typeString',''))
                if not size or literal.get('nodeType')!='Literal' or literal.get('kind') not in ('string','unicodeString','hexString'):continue
                raw=literal.get('hexValue')
                if isinstance(raw,str) and len(raw)%2==0 and len(raw)<=2*int(size[1]) and re.fullmatch('[0-9a-fA-F]*',raw):
                    return op(node['operator'],self.value(other,env),lit(int(raw.ljust(2*int(size[1]),'0'),16)))
        if node and integer and typ not in ('uint','uint256'):
            if node.get('nodeType')=='BinaryOperation' and node.get('operator') in ('+','-','*','/','%'):
                return {'kind':'typed_integer_arithmetic','type':typ,'operator':node['operator'],
                    'args':[self.value(node['leftExpression'],env),self.value(node['rightExpression'],env)],
                    'checked':checked_mode(self,self.current)}
            if node.get('nodeType')=='UnaryOperation' and node.get('operator')=='-':
                return {'kind':'typed_integer_arithmetic','type':typ,'operator':'-',
                    'args':[self.value(node['subExpression'],env)],'checked':checked_mode(self,self.current)}
            if node.get('nodeType')=='FunctionCall' and node.get('kind')=='typeConversion' and len(node.get('arguments',[]))==1:
                return {'kind':'integer_cast','type':typ,'input':self.value(node['arguments'][0],env)}

        if node and node.get('nodeType')=='BinaryOperation' and node.get('operator') in ('&&','||'):
            left=self.value(node['leftExpression'],env);state=self.current
            mark=len(state.get('evaluated_terms',[]));guard_mark=len(state.get('guards',[]));write_mark=len(state.get('writes',[]));env_before=copy.deepcopy(env)
            # A source path can already establish a short-circuit branch.
            # Do not evaluate an external call on a proven inactive branch.
            if node['operator']=='||' and not conditions_possible(state['guards'],left):return left
            if node['operator']=='&&' and not conditions_possible(state['guards'],op('!',left)):return left
            right=self.value(node['rightExpression'],env)
            gate=left if node['operator']=='&&' else op('!',left)
            evaluated=state.get('evaluated_terms',[])[mark:]
            state['evaluated_terms']=state.get('evaluated_terms',[])[:mark]+[{'kind':'guarded_evaluation','condition':copy.deepcopy(gate),'input':x} for x in evaluated]
            guards=state.get('guards',[])
            state['guards']=guards[:guard_mark]+[op('or',op('!',gate),g) for g in guards[guard_mark:]]
            if len(state.get('writes',[]))!=write_mark or env!=env_before:state.setdefault('evaluation_gaps',[]).append('short_circuit_side_effect_not_lowered')
            return normalize(op(node['operator'],left,right))
        if (node and node.get('nodeType')=='Literal'
                and node.get('kind') in ('string','unicodeString','hexString')):
            raw=node.get('hexValue')
            value={'kind':'fixed_bytes_literal','hex':raw,
                   'byte_length':len(raw)//2 if isinstance(raw,str) else None,
                   'source':self.anchor(node)}
            from .m05_credential_encoding import fixed_literal
            fixed_literal(value)
            return value
        if node and node.get('nodeType') == 'FunctionCall':
            callee = node.get('expression', {})
            if node.get('kind')=='typeConversion' and len(node.get('arguments',[]))==1:
                import re
                target=elementary_expression_name(callee);arg=node['arguments'][0]
                if re.fullmatch(r'uint(\d*)',target) and arg.get('typeDescriptions',{}).get('typeString') in ('address','address payable'):
                    bits=int(target[4:] or 256)
                    return {'kind':'uint_narrow','bits':bits,'from_bits':160,'type':target,'input':self.value(arg,env)}
            enum = self.nodes.get(callee.get('referencedDeclaration'), {})
            if node.get('kind')=='typeConversion' and enum.get('nodeType')=='EnumDefinition' and len(node.get('arguments',[]))==1:
                return {'kind':'enum_cast','enum_ast_id':enum['id'],'members':len(enum['members']),
                        'type':'enum '+enum.get('canonicalName',enum['name']),
                        'input':self.value(node['arguments'][0],env)}
            decl = callee.get('referencedDeclaration')
            from .source_entry_identity import builtin_call
            if builtin_call(node,self,('gasleft',)):
                return {'kind':'source_gas_available','type':'uint256','source_id':node['id'],'scope':'symbolic available gas; no execution sufficiency claim'}
            if builtin_call(node,self,('ecrecover',)):
                args = [self.value(x, env) for x in node.get('arguments', [])]
                if len(args) != 4:
                    raise Unsupported('credential_recovery_arity')
                return {'kind': 'credential_recovery', 'digest': args[0],
                        'signature': args[1:], 'type': 'address', 'source': self.anchor(node)}
            # ReadCalls handles typed scalar/tuple and branch-dependent returns
            # for both the ordinary and mechanism routes. Preserve one summary.
        return super().evaluate(node, env)

    def statements(self,stmts,states,depth):
        abandoned=0;first_overflow=None
        for position,node in enumerate(stmts):
            out=[]
            for state in states:
                out.extend(self.statement(node,state,depth) if state['flow']=='normal' else [state])
            if len(out)>self.limit-1:
                # Preserve successful/frontier paths first. An abandoned branch
                # remains decisive unknown; its writes never prove a finding.
                ranked=sorted(enumerate(out),key=lambda x:(x[1]['flow'] in ('reverted','truncated'),x[0]))
                kept=[s for _,s in ranked[:self.limit-1]]
                abandoned+=len(out)-len(kept)
                if first_overflow is None:first_overflow=self.anchor(node)
                states=kept
            else:states=out
        if abandoned:
            base=copy.deepcopy(states[0]);base['flow']='truncated'
            base['issues'].append({'reason':'source_path_frontier_bound_exceeded','source':first_overflow,
                'abandoned_frontier_states':abandoned,'max_source_paths':self.limit,'not_explored_scope_is_unknown':True})
            states.append(base)
        return states

    def statement(self, node, state, depth):
        from .m11_calls import expand_value_statement
        expanded=expand_value_statement(self,node,state,depth) if node else None
        if expanded is not None:return expanded
        if node and node.get('nodeType')=='IfStatement':
            from .source_entry_identity import builtin_call
            def bare_revert(branch):
                if not branch:return None
                statements=branch.get('statements',[]) if branch.get('nodeType')=='Block' else [branch]
                if len(statements)!=1:return None
                stmt=statements[0];call=stmt.get('expression',{}) if stmt.get('nodeType')=='ExpressionStatement' else {}
                # Only the pure builtin rejection itself is normalized. Complex
                # error construction/side effects remain on the ordinary path.
                if builtin_call(call,self,('revert',)) and all(a.get('nodeType')=='Literal' for a in call.get('arguments',[])):return call
                return None
            true=bare_revert(node.get('trueBody'));false=bare_revert(node.get('falseBody'))
            if bool(true)!=bool(false):
                condition=self.expr(node['condition'],state)
                predicate=normalize(op('!',condition) if true else condition)
                rejected=copy.deepcopy(state);rejected['guards'].append(op('!',predicate));rejected['flow']='reverted'
                rejected['rejection']={'predicate':copy.deepcopy(predicate),'source':self.anchor(true or false),
                    'normalized_from':'compiler_if_builtin_revert','conditional_source':self.anchor(node)}
                normal=copy.deepcopy(state);normal['guards'].append(predicate)
                result=[]
                if conditions_possible(normal['guards']):result.extend(self.statement(node.get('falseBody') if true else node.get('trueBody'),normal,depth))
                if conditions_possible(rejected['guards']):result.append(rejected)
                return result
        if node and node.get('nodeType')=='EmitStatement':
            return self.event_statement(node.get('eventCall'),state)
        if node and node.get('nodeType') == 'ExpressionStatement':
            call = node.get('expression', {})
            fun = call.get('expression', {})
            decl = fun.get('referencedDeclaration')
            from .source_entry_identity import builtin_call
            if builtin_call(call,self):
                from .source_scalar_semantics import pure_message_argument
                if any(not pure_message_argument(a,self) for a in call.get('arguments',[])[1:]):
                    state.setdefault('evaluation_gaps',[]).append('dynamic_rejection_argument_evaluation_not_lowered')
                predicate = self.expr(call['arguments'][0], state)
                rejected = copy.deepcopy(state)
                rejected['guards'].append(op('!', predicate))
                rejected['rejection'] = {'predicate': predicate, 'source': self.anchor(call)}
                rejected['flow'] = 'reverted'
                state['guards'].append(predicate)
                out = []
                if conditions_possible(state['guards']):
                    out.append(state)
                if conditions_possible(rejected['guards']):
                    out.append(rejected)
                return out
        return super().statement(node, state, depth)


def program(state, target, normalize_writes=True):
    # V1 M2 graph requests retain their original extracted representation.
    # Typed lowering is a downstream model operation, not a mutation of a
    # previously authenticated request. Both views derive from the same source.
    cache = state.setdefault('_source_mechanism_models' if normalize_writes else '_source_mechanism_raw_models', {})
    if target not in cache:
        base = state['lookups'][target]
        lookups=state.setdefault('_source_mechanism_lookup_cache',{})
        if target not in lookups:lookups[target]=MechanismPaths(base.bundle,base.contract,192)
        lookup=lookups[target]
        paths, errors = {}, []
        from .source_entry_identity import entry_functions
        for fn in entry_functions(base):
            signature = fn['signature']
            try:
                raw_cache=state.setdefault('_mechanism_raw_path_cache',{})
                cache_key=(target,signature)
                if cache_key not in raw_cache:raw_cache[cache_key]=lookup.run(signature)
                paths[signature]=copy.deepcopy(raw_cache[cache_key])
                if not normalize_writes:
                    continue
                from .m05_state_relations import expand_write
                for branch in paths[signature]:
                    expanded=[]
                    try:
                        for write in branch['writes']:expanded+=expand_write(write,lookup)
                    except Unsupported as ex:
                        branch['issues'].append({'reason':str(ex),'phase':'typed_state_expansion'})
                    else:
                        if expanded!=branch['writes']:
                            branch['original_writes']=copy.deepcopy(branch['writes'])
                            branch['writes']=expanded
            except (Unsupported, ValueError, KeyError, TypeError) as ex:
                errors.append({'function': signature, 'reason': str(ex)})
        lookup.writer_scan_gaps=copy.deepcopy(errors)
        lookup.writer_scan_gaps.extend({'function':fn,'path_index':pi,'reason':'incomplete_possible_writer_path'}
            for fn,branches in paths.items() for pi,p in enumerate(branches)
            if p['issues'] or p.get('evaluation_gaps') or p['flow'] not in ('normal','returned','reverted'))
        bases=lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
        lookup.writer_scan_gaps.extend({'reason':'special_entry_writer_not_extracted','source':lookup.anchor(n)}
            for n in lookup.nodes.values() if n.get('nodeType')=='FunctionDefinition' and n.get('scope') in bases
            and function_kind(n) in ('fallback','receive','unresolved_kind') and (n.get('body') or {}).get('statements')
            and function_kind(n)+'()' not in paths)
        cache[target] = lookup, paths, errors
    return cache[target]


def successful(path):
    return path['flow'] in ('normal', 'returned')


def remap(value, parameters=None, sender=None):
    parameters = parameters or {}
    if isinstance(value, dict):
        if value.get('kind') == 'parameter' and value['id'] in parameters:
            return copy.deepcopy(parameters[value['id']])
        if value.get('kind') == 'actual_sender' and sender is not None:
            return copy.deepcopy(sender)
        return {k: remap(v, parameters, sender) for k, v in value.items()}
    return [remap(v, parameters, sender) for v in value] if isinstance(value, list) else value


def scalar_write(write, lookup):
    from .m05_state_relations import scalar
    return scalar(write,lookup)


def post(value,writes,lookup):
    from .m05_state_relations import compose_read
    return compose_read(value,writes,lookup)


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


def reject_changed_selector_keys(values,writes):
    """Keep the existing read-over-write boundary; never guess a new key."""
    changed={w['path']['root'] for w in writes}
    for node in walk(values):
        if node.get('kind')=='storage':
            for segment in node.get('segments',[]):
                if any(n.get('kind')=='storage' and n['root'] in changed for n in walk(segment.get('key',{}))):
                    raise Unsupported('post_state_selector_key_dependency_not_lowered')


class MechanismEncoder(JointEncoder):
    def bound(self,x,typ):
        from .m05_state_relations import enum_size
        size=enum_size(self.lookup,typ)
        if size is not None:
            self.constraints.extend([x>=0,x<size]);return x
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
            from .source_entry_identity import builtin_object
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
            name = 'source_ecrecover'
            if name not in self.functions:
                self.functions[name] = self.z.Function(name, *[a.sort() for a in args], self.z.IntSort())
            self.encoding_notes.append({'kind': 'credential_recovery_congruence',
                'scope': 'same digest and same signature recover same address; not a signature forgery proof'})
            recovered=self.bound(self.functions[name](*args), 'address')
            self.encoding_notes.append({'kind':'source_ecrecover_r_zero_failure',
                'scope':'r==0 returns zero; other invalid signature inputs remain abstract'})
            return self.z.If(args[2]==0,self.z.IntVal(0),recovered)
        return super().expr(value)


def checked_subtractions(path):
    """Expose implicit uint subtraction guards used by state controls."""
    return [op('>=',*n['args']) for w in path['writes'] for n in walk(w['value'])
            if n.get('kind')=='op' and n.get('op')=='-' and len(n['args'])==2]


def retime(value, replacement):
    if isinstance(value,dict):
        if value.get('kind')=='environment' and value.get('field')=='timestamp':return copy.deepcopy(replacement)
        return {k:retime(v,replacement) for k,v in value.items()}
    return [retime(x,replacement) for x in value] if isinstance(value,list) else value


def solve(lookup, obligation, function, model, construct, root, holder=None):
    from .m05_relation_model_scope import constrain_model
    constrain_model(obligation,lookup,model)
    from .m05_common_semantics import prepare, consumed
    from .m05_question_trace import CREDENTIAL_DIMENSIONS
    from time import perf_counter
    started=perf_counter()
    if model['kind'] in CREDENTIAL_DIMENSIONS:
        model['checked_dimensions']=copy.deepcopy(CREDENTIAL_DIMENSIONS[model['kind']])
    attempt={'id':'ma_'+digest({'obligation':obligation['id'],'model':model}),
        'model_sha256':digest(model),'kind':model['kind'],'function':function,
        'question_refs':copy.deepcopy(model.get('question_refs',[])),
        'phase':'model_constructed','formal_attempted':False}
    obligation.setdefault('_model_attempts',[]).append(attempt)
    try:
        common, inputs = prepare(obligation, function, model, root, holder)
        encoder = MechanismEncoder(lookup)
        z = encoder.z
        domain, violation = construct(encoder, inputs)
    except Exception as ex:
        attempt.update(phase='formula_construction_failed',reason=type(ex).__name__+':'+str(ex))
        raise
    # Construct BOTH formulas before checking; timeout must not change identity.
    premise_formula=z.And(*encoder.constraints,domain)
    formula = z.And(premise_formula, violation)
    query_solver = z.Solver()
    query_solver.set(timeout=5000, random_seed=0)
    query_solver.add(formula)
    smt = query_solver.to_smt2()
    premise_solver = z.Solver()
    premise_solver.set(timeout=5000, random_seed=0)
    premise_solver.add(premise_formula)
    attempt.update(phase='formal_attempted',formal_attempted=True)
    solver_started=perf_counter()
    premise = bounded_solve(premise_solver)
    answer = bounded_solve(query_solver) if premise == z.sat else None
    solver_seconds=perf_counter()-solver_started
    status = ('supported' if answer == z.sat else 'refuted_in_scope' if answer == z.unsat else 'inconclusive')
    reason = ('source_mechanism_violation_satisfiable' if answer == z.sat else
              'source_mechanism_violation_unsatisfiable' if answer == z.unsat else
              'premise_unsat' if premise == z.unsat else
              premise_solver.reason_unknown() if premise != z.sat else query_solver.reason_unknown())
    if answer == z.sat and encoder.abstract_hash_used and not model.get('same_payload_certificate'):
        status, reason = 'inconclusive', 'cryptographic_abstraction_witness_requires_confirmation'
    formal = {'engine': 'z3', 'version': z.get_version_string(), 'solver_called': True,
              'premise': str(premise), 'query': str(answer) if answer is not None else 'not_checked',
              'status': status, 'reason': reason, 'timeout_ms': 5000,
              'semantic_formula_sha256': digest(model),
              'formula_sha256': hashlib.sha256(smt.encode()).hexdigest(), 'smt2': smt,
              'encoding_notes': encoder.encoding_notes,
              'timing_seconds':{'construct_and_solve':perf_counter()-started,'solver_checks':solver_seconds},
              'scope': 'source-bound symbolic pre-state and stated transition; not deployed reachability or full-program proof'}
    from .m05_formal_diagnostics import diagnostics
    formal['model_diagnostics']=diagnostics(premise_formula,violation,formula,query_solver,answer,smt)
    attempt.update(phase='formal_returned',status=status,query=formal['query'],premise=formal['premise'],
        formula_sha256=formal['formula_sha256'],timing_seconds=formal['timing_seconds'])
    return {'id': 'soq_' + digest({'proposal': obligation['proposal_sha256'], 'model': model}),
            'obligation_id': obligation['id'], 'llm_proposal_sha256': obligation['proposal_sha256'],
            'rule': obligation['rule'], 'target': obligation['target'], 'function': function,
            'proposal_function': obligation['function'], 'asset_root': root, 'holder': holder,
            'source_model': model, 'common_operation': consumed(common, inputs, formal),
            'formal': formal, 'status': status,
            'execution_status': 'not_run', 'evidence_types': ['P', 'M'],
            'policy_scope': model.get('policy_scope', 'source_derived_conditional_mechanism'),
            'source_remarks': copy.deepcopy(obligation['original_proposal']['unresolved']),
            'source_basis_assessment': copy.deepcopy(obligation.get('basis_assessment', {})),
            'assumptions': model.get('assumptions', [])}


def relevant(obligation, function, path, roots=()):
    if function == obligation['function']:
        return True
    if any(x['function'] == function and x['target'] == obligation['target'] for x in obligation['related_operations']):
        return True
    ids = set(obligation['source_ast_ids'])
    return bool(ids.intersection(roots) or path.get('entry_source', {}).get('ast_id') in ids
                or any(w['source'].get('ast_id') in ids for w in path.get('writes', [])))
