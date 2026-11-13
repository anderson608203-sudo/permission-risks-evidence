# 实跑源码文本 · 第 4 页

## file-4e5070a6fc9275

`source/src/pr_next_joint/frontend/read_calls.py` · 原字节 SHA-256 `60561ec9166a8476ff2112abd5dff92e0afcebaa29861b27863b0c5ff05c7529`

~~~~python
"""Compiler-resolved read-only call summaries for the bounded P analyzer.

Direct construction or explicitly conditional concrete-source instance bindings.
No interface/proxy guessing, external writes, transactions, or substitution of
the outer user's identity for the callee's actual calling-contract identity.
"""
import copy,json
import re
from pr_next_joint.frontend.source_entry_identity import function_kind, function_mutability
from pr_next_joint.frontend.path_ir import clean, key, walk, op, lit, conditions_possible


def boolean_union(operator, terms):
    """Remove explicit true/false return branches without solving arithmetic."""
    conjunction=operator=='and';identity=conjunction;kept=[]
    for term in terms:
        if term==lit(not identity):return lit(not identity)
        if term!=lit(identity):kept.append(term)
    if not kept:return lit(identity)
    return kept[0] if len(kept)==1 else op(operator,*kept)


class ReadCalls:
    def __init__(self, paths):
        self.p=paths
        self.active_contract=paths.contract_node['id']
        self.instance=None  # Preserve existing root storage representation.
        self.stack=[]
        self.instances={}
        self.gaps=[]
        self.summaries={}
        self.receiver_terms={}

    def address(self):
        return {'kind':'contract_address','instance':self.instance or
                {'kind':'root_instance','contract':self.p.contract_node['id']}}

    def state(self, value, declaration):
        mapped=getattr(self.p,'_delegate_storage_map',None)
        if mapped is not None:
            if declaration not in mapped:raise ValueError('delegate_storage_declaration_not_mapped')
            return {**value,'root':mapped[declaration]}
        if self.instance is not None:
            scope=self.p.nodes.get(declaration,{}).get('scope')
            bases=self.p.nodes[self.active_contract].get('linearizedBaseContracts',[self.active_contract])
            if scope in bases:return {**value,'instance':copy.deepcopy(self.instance)}
        return value

    def created_type(self, ref):
        """A concrete creation expression, not a static interface type guess."""
        decl=self.p.nodes.get(ref,{})
        if not decl.get('stateVariable'):return None
        scope=self.p.nodes.get(decl.get('scope'),{})
        candidates=[]
        if decl.get('value'):candidates.append(decl['value'])
        for fn in scope.get('nodes',[]):
            if fn.get('nodeType')!='FunctionDefinition' or function_kind(fn)!='constructor':continue
            for stmt in (fn.get('body') or {}).get('statements',[]):
                e=stmt.get('expression',{})
                if e.get('nodeType')=='Assignment' and e.get('operator')=='=' and e.get('leftHandSide',{}).get('referencedDeclaration')==ref:
                    candidates.append(e['rightHandSide'])
        writes=[n for n in walk(scope) if n.get('nodeType')=='Assignment' and
                n.get('leftHandSide',{}).get('referencedDeclaration')==ref]
        if len(candidates)!=1 or len(writes)+(1 if decl.get('value') else 0)!=1:return None
        rhs=candidates[0]
        while rhs.get('nodeType')=='FunctionCall' and rhs.get('kind')=='typeConversion' and len(rhs.get('arguments',[]))==1:
            rhs=rhs['arguments'][0]
        new=rhs.get('expression',{})
        if rhs.get('nodeType')!='FunctionCall' or new.get('nodeType')!='NewExpression':return None
        typ=new.get('typeName',{});cid=typ.get('referencedDeclaration',typ.get('pathNode',{}).get('referencedDeclaration'))
        target=self.p.nodes.get(cid,{})
        if target.get('nodeType')!='ContractDefinition' or target.get('contractKind')=='interface':return None
        return cid,new

    def destination(self, receiver, source_receiver=None):
        if receiver.get('kind')=='contract_address':
            obj=receiver['instance'];return obj.get('contract'),obj
        # A supplied concrete type may be assigned through an argument or a
        # runtime setter. Its code is an explicit conditional environment,
        # never a claim that an arbitrary address implements that code.
        source_receiver=source_receiver or {}
        reference=source_receiver.get('referencedDeclaration')
        decl=self.p.nodes.get(reference,{})
        typ=decl.get('typeName',{})
        if source_receiver.get('nodeType')=='FunctionCall' and source_receiver.get('kind')=='typeConversion':
            typ=source_receiver.get('expression',{})
        cid=typ.get('referencedDeclaration',typ.get('pathNode',{}).get('referencedDeclaration'))
        concrete=self.p.nodes.get(cid,{})
        if (receiver.get('kind')!='storage' or receiver.get('segments')):
            if (concrete.get('nodeType')!='ContractDefinition' or concrete.get('contractKind')!='contract'
                    or not any(n.get('body') for n in concrete.get('nodes',[]) if n.get('nodeType')=='FunctionDefinition')):
                return None
            instance={'kind':'source_typed_instance','parent':self.instance or
                      {'kind':'root_instance','contract':self.p.contract_node['id']},
                      'address_term':copy.deepcopy(receiver),'contract':cid}
            self.instances[key(instance)]={'instance':instance,'binding':'conditional_compiled_concrete_type',
                'source':self.p.anchor(source_receiver),
                'assumption':'this call destination executes the supplied concrete type; address/code identity not verified',
                'not_universal_external_code':True}
            return cid,instance
        found=self.created_type(receiver['root'])
        if not found:
            # Concrete source types describe a conditional environment, not a
            # verified deployed code address. Keep instance identity separate.
            decl=self.p.nodes.get(receiver['root'],{});typ=decl.get('typeName',{})
            cid=typ.get('referencedDeclaration',typ.get('pathNode',{}).get('referencedDeclaration'))
            target=self.p.nodes.get(cid,{})
            if target.get('nodeType')!='ContractDefinition' or target.get('contractKind')!='contract':return None
            scope=self.p.nodes.get(decl.get('scope'),{})
            writes=[n for n in walk(scope) if n.get('nodeType')=='Assignment' and n.get('leftHandSide',{}).get('referencedDeclaration')==receiver['root']]
            constructors=[f for f in scope.get('nodes',[]) if function_kind(f)=='constructor']
            constructor_ids={n.get('id') for f in constructors for n in walk(f)}
            if not writes:return None
            instance={'kind':'source_typed_instance','parent':receiver.get('instance') or {'kind':'root_instance','contract':self.p.contract_node['id']},'reference':receiver['root'],'contract':cid}
            self.instances[key(instance)]={'instance':instance,'binding':'conditional_compiled_concrete_type','source':self.p.anchor(writes[0]),'assumption':'configured instance implements this supplied concrete contract; deployment identity not verified', 'not_universal_external_code':True}
            return cid,instance
        cid,new=found
        instance={'kind':'created_instance','parent':receiver.get('instance') or
                  {'kind':'root_instance','contract':self.p.contract_node['id']},
                  'reference':receiver['root'],'creation_ast':new['id'],'contract':cid}
        self.instances[key(instance)]={'instance':instance,'binding':'immutable_direct_new' if self.p.nodes[receiver['root']].get('mutability')=='immutable' else 'constructor_single_assignment_direct_new','source':self.p.anchor(new)}
        return cid,instance

    def implementation(self, cid, referenced):
        from pr_next_joint.frontend.source_paths import SourcePaths
        declaration=self.p.nodes[cid];anchor=self.p.anchor(declaration)
        contracts=[c for c in self.p.bundle['contracts'] if c['name']==declaration.get('name') and c['file']==anchor['file']]
        if len(contracts)!=1:return None
        lookup=SourcePaths(self.p.bundle,contracts[0])
        if referenced.get('nodeType')=='VariableDeclaration':
            matches=[f for f in contracts[0]['functions'] if lookup.entry_identity.getter_shape(referenced,f)]
        else:
            selector=self.p.function_selector(referenced)
            matches=[f for f in contracts[0]['functions'] if selector and f['selector']==selector]
        if len(matches)!=1:return None
        return lookup.function(matches[0]['signature'])

    def bound_library(self, node, target):
        from pr_next_joint.frontend.source_library_binding import compiler_bound_receiver, storage_identity
        typ=node.get('expression',{}).get('expression',{}).get('typeDescriptions',{}).get('typeIdentifier','')
        supported=bool(re.fullmatch(r't_(?:u?int\d+|address(?:_payable)?|bool|bytes\d+)',typ) or storage_identity(typ))
        return bool(supported and target and function_mutability(target) in ('pure','view') and
                    compiler_bound_receiver(self.p,node,target))

    def bound_ancestor(self,node,target):
        """An explicit base-contract qualifier is not an external address."""
        expr=node.get('expression',{});receiver=expr.get('expression',{})
        if not target or expr.get('nodeType')!='MemberAccess' or receiver.get('nodeType')!='Identifier':return False
        if not expr.get('typeDescriptions',{}).get('typeIdentifier','').startswith('t_function_internal_'):return False
        cid=receiver.get('referencedDeclaration');decl=self.p.nodes.get(cid,{})
        active=self.p.nodes.get(self.active_contract,{})
        if decl.get('nodeType')!='ContractDefinition' or decl.get('contractKind')!='contract':return False
        if cid not in active.get('linearizedBaseContracts',[]):return False
        return bool(target.get('body') and target.get('scope') in decl.get('linearizedBaseContracts',[cid]))

    def call(self, node, env):
        p=self.p;s=p.current;expr=node.get('expression',{})
        target=p.fns.get(expr.get('referencedDeclaration'))
        declaration=p.nodes.get(expr.get('referencedDeclaration'),{})
        getter=declaration.get('nodeType')=='VariableDeclaration' and declaration.get('visibility')=='public' and declaration.get('stateVariable')
        if not target and not getter:return None
        if node.get('names'):return self.reject(node,'named_call_arguments_not_lowered')
        library_bound=self.bound_library(node,target)
        ancestor_bound=self.bound_ancestor(node,target)
        external=expr.get('nodeType')=='MemberAccess' and not library_bound and not ancestor_bound
        if not external and not library_bound and not ancestor_bound and expr.get('nodeType')!='Identifier':return None
        args=([p.value(expr['expression'],env)] if library_bound else [])
        args += [p.value(x,env) for x in node.get('arguments',[])]
        cid=self.active_contract;instance=self.instance;sender=p.sender
        if target and not external and not library_bound and not ancestor_bound:
            from pr_next_joint.frontend.dispatch import resolve
            target=resolve(p,target,cid)
        if external:
            receiver=p.value(expr['expression'],env)
            self.receiver_terms[node.get('id')]=copy.deepcopy(receiver)
            destination=self.destination(receiver,expr['expression'])
            if not destination:return self.reject(node,'external_destination_not_bound')
            cid,instance=destination
            sender=self.address()
            try:target=self.implementation(cid,declaration)
            except (ValueError,KeyError,TypeError):return self.reject(node,'external_entry_identity_unresolved')
            if not target:return self.reject(node,'external_entry_identity_unresolved')
            getter='generated_getter' in target
            if getter:declaration=target['generated_getter']
            if getter:
                if declaration.get('scope') not in p.nodes[cid].get('linearizedBaseContracts',[cid]):return self.reject(node,'getter_contract_mismatch')
                typ=declaration.get('typeName',{});segments=[]
                for arg in args:
                    if typ.get('nodeType')!='Mapping':return self.reject(node,'getter_key_arity')
                    segments.append({'key':arg});typ=typ['valueType']
                concrete_type=self.p.nodes.get(typ.get('referencedDeclaration',typ.get('pathNode',{}).get('referencedDeclaration')),{})
                if typ.get('nodeType')!='ElementaryTypeName' and concrete_type.get('nodeType')!='ContractDefinition':return self.reject(node,'getter_result_not_scalar')
                result={'kind':'storage','root':declaration['id'],'segments':segments,'instance':copy.deepcopy(instance)}
                s.setdefault('read_calls',[]).append({'source':p.anchor(node),'target':p.anchor(declaration),'instance':instance,'callee_sender':sender,'arguments':clean(args),'return_value':clean(result),'binding':self.instances.get(key(instance),{}).get('binding'),'generated_getter':True})
                return result
        if external and target and function_mutability(target) not in ('view','pure'):
            from pr_next_joint.checks.access.destruction import terminal_created_call
            terminal=terminal_created_call(self,node,target,cid,instance,args)
            if terminal is not None:return terminal
        if not target or function_mutability(target) not in ('view','pure'):
            return self.reject(node,'call_not_read_only_or_implementation_missing')
        params=target.get('parameters',{}).get('parameters',[])
        returns=target.get('returnParameters',{}).get('parameters',[])
        if len(params)!=len(args) or not returns:return self.reject(node,'call_arity_not_supported')
        if not external:
            from pr_next_joint.frontend.pure_reads import summarize as pure_word_summary
            pure_word=pure_word_summary(p,node,target,args)
            if pure_word is not None:return pure_word
        identity=(target['id'],key(instance))
        if identity in self.stack or len(self.stack)>=8:return self.reject(node,'read_call_recursion_or_depth_limit')
        saved=(self.active_contract,self.instance,p.sender,p.current,p.unknown,getattr(p,'_entry_selector',None))
        self.active_contract,self.instance,p.sender=cid,instance,sender
        if external:p._entry_selector=p.function_selector(target)
        p.unknown=[];self.stack.append(identity)
        child={'env':{},'guards':[],'writes':copy.deepcopy(s['writes']),'issues':[],'flow':'normal'}
        try:
            from pr_next_joint.frontend.source_work_budget import metric
            # Fully serialized inputs are immutable cache keys. Include all
            # writes (and their anchors), instance, caller and call depth.
            text=json.dumps({"build":p.bundle["build_id"],"target":target["id"],"contract":cid,
                 "instance":instance,"sender":sender,"args":args,"writes":s["writes"],
                 "stack":self.stack,"calldata":p.calldata,"actual_entry_selector":getattr(p,"_entry_selector",None)},sort_keys=True,separators=(",",":"))
            cache_key=text if len(text)<=32768 else None
            cached=self.summaries.get(cache_key) if cache_key else None
            if cached is not None:
                paths=copy.deepcopy(cached);unknown=[]
                metric("readonly_call_summary_hits")
            else:
                paths=p.invoke(target,args,child,depth=len(self.stack))
                unknown=list(p.unknown);metric("readonly_call_summary_misses")
                if cache_key and len(self.summaries)<128 and not unknown and not any(x["issues"] or x.get("evaluation_gaps") for x in paths):
                    self.summaries[cache_key]=copy.deepcopy(paths)
        finally:
            self.stack.pop()
            self.active_contract,self.instance,p.sender,p.current,p.unknown,p._entry_selector=saved
        # A finished bounded path is usable even when a different loop path
        # is truncated. Only that exact continuation (including its guards)
        # is summarized; incomplete paths do not supply return values.
        unfinished=[x for x in paths if x['flow']=='truncated']
        complete=[x for x in paths if x['flow']!='truncated']
        incomplete=[x for x in complete if x['issues'] or x.get('evaluation_gaps') or len(x['writes'])!=len(s['writes'])]
        complete=[x for x in complete if x not in incomplete]
        unfinished += incomplete
        if unknown and not complete:return self.reject(node,'read_call_body_unresolved')
        if unfinished:
            s.setdefault('bounded_read_call_limits',[]).append({'source':p.anchor(node),'target':p.anchor(target),
                'reason':'incomplete_read_call_paths_excluded','excluded_paths':len(unfinished),
                'issues':[copy.deepcopy(i) for path in unfinished for i in path['issues']],
                'scope':'only fully returned continuations with their original guards; other states remain unanalyzed'})
            if not any(x['flow']=='returned' and 'return_value' in x for x in complete):
                return self.reject(node,'read_call_no_complete_return_path')
        paths=complete
        successes=[x for x in paths if x['flow']=='returned' and 'return_value' in x and conditions_possible(x['guards'])]
        if any(x['flow']=='normal' for x in paths):return self.reject(node,'implicit_return_not_lowered')
        if not successes:
            # This call is actually executed and has no supported returning
            # continuation. Preserve the reverted caller instead of erasing
            # every path when an enclosing require forks its return value.
            # Reversion is a control outcome, not a false successful-path
            # guard. A surrounding short-circuit may skip this whole call.
            s['flow']='reverted'
            s['rejection']={'source':p.anchor(node),'target':p.anchor(target),
                            'reason':'compiler_bound_read_call_has_no_returning_continuation'}
            return lit(False)
        success=boolean_union('or',[boolean_union('and',x['guards']) for x in successes])
        # require/assert may already have restricted a successful path without
        # materializing a second reverted branch. Every successful call still
        # requires its continuation guards, including those in pure libraries.
        if success!=lit(True):s['guards'].append(success)
        def returned_value(path,index):
            value=path['return_value']
            if len(returns)==1:return value
            if value.get('kind')!='tuple' or len(value.get('items',[]))!=len(returns):
                raise ValueError('read_call_return_tuple_arity')
            return value['items'][index]
        try:
            values=[]
            for index,declaration in enumerate(returns):
                from pr_next_joint.frontend.language import scalar_type
                typ=scalar_type(declaration.get('typeDescriptions',{}).get('typeString',''),p,declaration.get('typeName',{}))
                if not re.fullmatch(r'(?:u?int\d*|bool|address(?: payable)?|bytes\d+)',typ):
                    return self.reject(node,'read_call_return_type_not_scalar:'+typ)
                result=returned_value(successes[-1],index)
                for branch in reversed(successes[:-1]):
                    condition=boolean_union('and',branch['guards']);yes=returned_value(branch,index)
                    # Exact identity 0*x=0 eliminates exponential duplication
                    # in repeated checked multiplication summaries. Evaluation
                    # and successful-call guards below remain branch-scoped.
                    same=key(yes)==key(result)
                    zero_product=False
                    if condition.get('kind')=='op' and condition.get('op')=='==' and yes==lit(0) and result.get('kind')=='op' and result.get('op')=='*':
                        a,b=condition['args']
                        if a==lit(0):a,b=b,a
                        zero_product=b==lit(0) and any(key(a)==key(factor) for factor in result['args'])
                    if not same and not zero_product:
                        result={'kind':'conditional','condition':condition,'when_true':yes,'when_false':result,'type':typ}
                values.append(result)
            result=values[0] if len(values)==1 else {'kind':'tuple','items':values}
        except (ValueError,KeyError,TypeError) as ex:return self.reject(node,str(ex))
        s.setdefault('read_calls',[]).append({'source':p.anchor(node),'target':p.anchor(target),
            'instance':instance,'callee_sender':sender,'arguments':clean(args),'return_value':clean(result),
            'binding':('compiler_bound_qualified_ancestor' if ancestor_bound else 'compiler_bound_internal_pure_library' if library_bound else
                self.instances.get(key(instance),{}).get('binding','compiled_same_instance') if external else 'compiler_internal_declaration'),
            **({'receiver_parameter_index':0,'compiler_call_type':expr['typeDescriptions']['typeIdentifier'],
                'library_declaration':target['scope'],'resolved_function':target['id']} if library_bound else {})})
        for path in successes:
            s['read_calls'].extend(path.get('read_calls',[]))
            s.setdefault('loop_scopes',[]).extend({**copy.deepcopy(scope),'call_source':p.anchor(node),'continuation_guard':boolean_union('and',path['guards'])} for scope in path.get('loop_scopes',[]))
            s.setdefault('bounded_read_call_limits',[]).extend(copy.deepcopy(path.get('bounded_read_call_limits',[])))
        # Downstream consumers may require successful evaluation even when a
        # local/return is unused. Preserve a single actual continuation. Do
        # not conjoin effects from mutually exclusive read-call branches.
        if len(successes)==1:
            s.setdefault('evaluated_terms',[]).extend(copy.deepcopy(successes[0].get('evaluated_terms',[])))
            s.setdefault('evaluation_gaps',[]).extend(successes[0].get('evaluation_gaps',[]))
        else:
            for path in successes:
                if path.get('evaluated_terms'):
                    s.setdefault('evaluated_terms',[]).append({'kind':'guarded_evaluation',
                        'condition':boolean_union('and',path['guards']),
                        'values':copy.deepcopy(path['evaluated_terms']),'type':'bool'})
                s.setdefault('evaluation_gaps',[]).extend(path.get('evaluation_gaps',[]))
        return result

    def reject(self,node,reason):
        expr=node.get('expression',{})
        receiver=expr.get('expression') if expr.get('nodeType')=='MemberAccess' else None
        # Record the already lowered receiver at the invocation state; do not
        # re-execute a receiver expression with side effects for diagnostics.
        actual=copy.deepcopy(self.receiver_terms.get(node.get('id')))
        if actual is None and receiver and receiver.get('nodeType')=='Identifier':
            ref=receiver.get('referencedDeclaration')
            actual=copy.deepcopy(self.p.current.get('env',{}).get(ref))
            if actual is None and self.p.nodes.get(ref,{}).get('stateVariable'):
                actual={'kind':'storage','root':ref,'segments':[]}
        item={'reason':reason,'source':self.p.anchor(node),
              'receiver_term':actual,
              'callpoint_writes':copy.deepcopy(self.p.current.get('writes', [])),
              'callpoint_guards':copy.deepcopy(self.p.current.get('guards', [])),
              'callpoint_evaluations':copy.deepcopy(self.p.current.get('evaluated_terms', []))}
        self.p.current['issues'].append(item)
        self.gaps.append(item)
        return {'kind':'unknown','reason':reason}

~~~~

## file-336e7456aacb59

`source/src/pr_next_joint/frontend/source_bindings.py` · 原字节 SHA-256 `e651583d95018d87018df7f622bc0ec8b54a88a6cf65c4f5b8a0800f1a7fc7f4`

~~~~python
"""Path-local observations for source references. No role or permission inference."""
import copy
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.graph.relation_model_scope import source_term

def observe(path,node,value,env):
    if not node or node.get('id') is None:return
    ids=[node['id']]
    if node.get('nodeType')=='Identifier' and node.get('referencedDeclaration') in env:
        ids.append(node['referencedDeclaration'])
    table=path.setdefault('_source_value_bindings',{})
    for identity in ids:
        row=table.setdefault(str(identity),[])
        if not any(key(x)==key(value) for x in row):
            # Repeated evaluation with different values is ambiguous, never last-write-wins.
            if len(row)<2:row.append(copy.deepcopy(value))

def path_key(path):
    from pr_next_joint.core import digest
    return digest([path.get('guards'),path.get('writes'),path.get('flow'),path.get('_source_value_bindings'),path.get('_source_lvalue_bindings')])

def observe_lvalue(path,node,value):
    if node and node.get('id') is not None and value.get('kind')=='storage':
        table=path.setdefault('_source_lvalue_bindings',{});row=table.setdefault(str(node['id']),[])
        if not any(key(x)==key(value) for x in row) and len(row)<2:row.append(copy.deepcopy(value))

def resolve(node,lookup,function,path,purpose=None):
    observed=path.get('_source_lvalue_bindings',{}).get(str(node['id'])) if purpose=='resource' else None
    if observed is None:observed=path.get('_source_value_bindings',{}).get(str(node['id']))
    if observed is not None:
        if len(observed)!=1:raise ValueError('source_reference_has_multiple_values_on_path')
        value=copy.deepcopy(observed[0])
    else:value=source_term(node,lookup,function)
    if value is None or any(x.get('kind') in ('unknown','call_unresolved') for x in walk(value)):
        raise ValueError('source_expression_not_lowered')
    return value

def rows_for(compiled,field,fn,path=None,pi=None):
    result=[]
    for row in compiled[field]:
        if row['function']!=fn:continue
        if pi is not None and pi not in row.get('path_indices',[pi]):continue
        if path is not None and row.get('path_key')!=path_key(path):continue
        result.append(row)
    return result


def resolve_condition(node,lookup,function,path):
    """Resolve a cited predicate, never a statement's dummy return value.
    Only compiler-bound require/assert wrappers are unwrapped. Scalar references
    remain scalars and are rejected by the typed implication boundary.
    """
    from pr_next_joint.frontend.source_entry_identity import builtin_call
    if node.get('nodeType')=='ExpressionStatement':
        return resolve_condition(node.get('expression',{}),lookup,function,path)
    if builtin_call(node,lookup,('require','assert')) and node.get('arguments'):
        return resolve_condition(node['arguments'][0],lookup,function,path)
    if node.get('nodeType')=='IfStatement':
        # Existing projection only accepts a source-established reverting branch;
        # it preserves its polarity rather than guessing which branch is legal.
        value=source_term(node,lookup,function)
        if value is None:raise ValueError('statement_does_not_identify_an_applicability_predicate')
        return value
    return resolve(node,lookup,function,path)

~~~~

## file-43ec49cfd4477b

`source/src/pr_next_joint/frontend/source_entry_identity.py` · 原字节 SHA-256 `405243e63b44046337cba31527c0f11771756d1706f398b026899273b4c68186`

~~~~python
"""Compiler/native corroborated entry metadata, without rewriting original AST.

Old Solidity ASTs omit selectors and kind. A derived binding must join the
compiler ABI and a native full signature at the exact declaring source span.
"""
import json,posixpath
from pr_next_joint.core import require, digest

def function_kind(node):
    if node.get('nodeType')!='FunctionDefinition':return node.get('kind')
    if node.get('kind') in ('function','constructor','fallback','receive'):return node['kind']
    if 'kind' in node:return 'unresolved_kind'
    if type(node.get('isConstructor')) is not bool:return 'unresolved_kind'
    if node['isConstructor']:return 'constructor'
    return 'function' if node.get('name') else 'fallback'

def function_mutability(node):
    value=node.get('stateMutability')
    if value in ('pure','view','payable','nonpayable'):return value
    if 'stateMutability' in node:return None
    if type(node.get('constant')) is bool and type(node.get('payable')) is bool:
        if node['constant'] and not node['payable']:return 'view'
        if not node['constant']:return 'payable' if node['payable'] else 'nonpayable'
    return None

def elementary_expression_name(node):
    value=node.get('typeName')
    if isinstance(value,str):return value
    return value.get('name','') if isinstance(value,dict) else ''

def builtin_call(node,lookup,names=('require','assert')):
    # A return without a value has expression=None and is not a call.
    if not isinstance(node,dict) or node.get('nodeType')!='FunctionCall':return False
    f=node.get('expression')
    if not isinstance(f,dict) or f.get('nodeType')!='Identifier':return False
    name=f.get('name');ref=f.get('referencedDeclaration')
    if name not in names:return False
    if type(ref) is not int or ref in lookup.nodes:return False
    # 0.4.x uses positive virtual declaration IDs. Modern compilers commonly
    # use negative ones. Compiler function type, not the display name, binds it.
    typ=f.get('typeDescriptions',{}).get('typeIdentifier','')
    aliases={'keccak256':('keccak256','sha3'),'sha3':('sha3','keccak256'),'selfdestruct':('selfdestruct','suicide'),'suicide':('suicide','selfdestruct')}
    return any(typ.startswith('t_function_'+kind+'_') for kind in aliases.get(name,(name,)))

def builtin_object(node,lookup,name):
    expected={'msg':'t_magic_message','block':'t_magic_block','tx':'t_magic_transaction'}.get(name)
    ref=node.get('referencedDeclaration')
    return bool(expected and node.get('nodeType')=='Identifier' and node.get('name')==name
        and type(ref) is int and ref not in lookup.nodes and node.get('typeDescriptions',{}).get('typeIdentifier')==expected)

def source_file(path):
    p=str(path or '').replace('\\','/')
    if not p or p.startswith('/') or ':' in p or '..' in p.split('/'):return None
    return posixpath.normpath(p)

def simple_type(node):
    if node.get('nodeType')!='ElementaryTypeName':return None
    name=node.get('name');return {'uint':'uint256','int':'int256','byte':'bytes1','address payable':'address'}.get(name,name)


def declared_type_pair(typ,lookup):
    """Display/native and ABI type from exact compiler AST declarations.

    Contract references are addresses in ABI. Enums use their compiler-sized
    integer. No conversion is inferred from a name or from a desired ABI.
    """
    basic=simple_type(typ)
    if basic:return basic,basic
    if typ.get('nodeType')=='ArrayTypeName':
        pair=declared_type_pair(typ.get('baseType',{}),lookup)
        if pair is None:return None
        length=typ.get('length')
        if length is None:suffix='[]'
        elif length.get('nodeType')=='Literal' and str(length.get('value','')).isdigit():
            suffix='['+str(int(length['value']))+']'
        else:return None
        return pair[0]+suffix,pair[1]+suffix
    if typ.get('nodeType')!='UserDefinedTypeName':return None
    decl=lookup.nodes.get(typ.get('referencedDeclaration'),{})
    if decl.get('nodeType')=='ContractDefinition' and decl.get('name'):
        return decl['name'],'address'
    if decl.get('nodeType')=='EnumDefinition':
        name=decl.get('canonicalName');count=len(decl.get('members',[]))
        if name and count:return name,'uint'+str(max(8,((count-1).bit_length()+7)//8*8))
    return None


def entry_functions(lookup):
    """ABI functions plus compiler-identified inherited special entrypoints."""
    result=list(lookup.contract['functions']);signatures={f['signature'] for f in result}
    for kind in ('fallback','receive'):
        signature=kind+'()'
        if signature in signatures:continue
        node=lookup.entry_identity.special(kind)
        if node:
            result.append({'signature':signature,'selector':None,'types':[],'outputs':[],
                'source_anchor':lookup.anchor(node),'special_kind':kind})
    return result

class EntryIdentity:
    def __init__(self,lookup):
        self.lookup=lookup;self.records={};self._selectors={};self.dispatch_proofs={}
    def anchor(self,node):return self.lookup.anchor(node)
    def native(self,node):
        anchor=self.anchor(node);scope=self.lookup.nodes.get(node.get('scope'),{})
        matched=[f for f in self.lookup.bundle.get('native_ir',{}).get('functions',[]) if
            f.get('contract')==scope.get('name') and source_file(f.get('source',{}).get('file'))==source_file(anchor['file'])
            and source_file(anchor['file']) is not None
            and f.get('source',{}).get('start')==anchor['start'] and f.get('source',{}).get('length')==anchor['length']]
        # Preserve native source-span identity; canonicalize only types proved
        # by the declaration at that exact span (contract/enum/typed arrays).
        pairs=[declared_type_pair(p.get('typeName',{}),self.lookup)
               for p in node.get('parameters',{}).get('parameters',[])]
        if any(p is None for p in pairs):return matched
        display=node.get('name','')+'('+','.join(p[0] for p in pairs)+')'
        canonical=node.get('name','')+'('+','.join(p[1] for p in pairs)+')'
        return [{**f,'signature':canonical,'source_native_signature':f['signature'],
                 'signature_basis':'exact_source_AST_declared_ABI_type'}
                if display!=canonical and f.get('signature')==display else f for f in matched]
    def declared_contract(self,node):
        decl=self.lookup.nodes.get(node.get('scope'),{});anchor=self.anchor(decl) if decl.get('src') else {}
        matches=[c for c in self.lookup.bundle['contracts'] if c['name']==decl.get('name') and c['file']==anchor.get('file')]
        return matches[0] if len(matches)==1 else None
    def selector(self,node):
        original=node.get('functionSelector')
        if original is not None:
            signatures={n.get('signature') for n in self.native(node)}
            if signatures:
                require(len(signatures)==1,'entry_native_signature_ambiguous')
                matches={f['selector'] for c in self.lookup.bundle['contracts'] for f in c['functions'] if f['signature'] in signatures}
                require(not matches or matches=={original},'entry_native_selector_conflict')
            return original
        if node.get('id') in self._selectors:return self._selectors[node['id']]
        if function_kind(node)!='function':return None
        native=self.native(node);signatures={n.get('signature') for n in native}
        if len(signatures)!=1:return None
        sig=next(iter(signatures))
        # Abstract declarations need not have deployable bytecode. The ABI
        # mapping is signature-wide; entry ownership is checked separately by C3.
        matches={f['selector'] for c in self.lookup.bundle['contracts'] for f in c['functions'] if f['signature']==sig}
        if len(matches)!=1:return None
        value=next(iter(matches))
        self._selectors[node['id']]=value
        self.record(node,sig,value,'compiler_ABI_native_exact_source')
        return value
    def record(self,node,signature,selector,basis):
        anchor=self.anchor(node);bundle=self.lookup.bundle
        hashes={r.get('source_anchor',{}).get('sha256') for r in bundle.get('functions',[])+bundle.get('state_declarations',[]) if r.get('source_anchor',{}).get('file')==anchor['file'] and r.get('source_anchor',{}).get('sha256')}
        self.records[str(node['id'])+':'+signature]={'program_id':bundle['program_id'],'build_id':bundle['build_id'],
            'target':self.lookup.contract['file']+':'+self.lookup.contract['name'],'signature':signature,'selector':selector,
            'ast_id':node['id'],'declaring_scope':node.get('scope'),'source':anchor,'kind':function_kind(node),
            'original_selector':node.get('functionSelector'),'original_kind':node.get('kind'),'basis':basis,
            'ast_source_sha256':digest(bundle['ast_sources'][anchor['file']]),'native_sha256':bundle.get('native_ir',{}).get('sha256'),
            'source_sha256':next(iter(hashes)) if len(hashes)==1 else None,
            'native_matches':[{'signature':n['signature'],'source':n['source'],'contract':n['contract']} for n in self.native(node)]}
        proof=self.dispatch_proofs.get(str(node['id'])+':'+signature)
        if proof:self.records[str(node['id'])+':'+signature]['dispatch_proof']=proof
    def select_entry(self,candidates,order,sig,selector):
        for scope in order:
            matches=list({n['id']:n for n in candidates if n.get('scope')==scope}.values())
            if not matches:continue
            if len(matches)==1:return matches[0]
            # Only resolve an actual same-scope function/getter ambiguity, using
            # validated compiler dispatcher-to-source correspondence.
            p=self.lookup;target=p.contract['file']+':'+p.contract['name']
            from pr_next_joint.frontend.compiler_evidence import CompilerEntryEvidence
            table=p.bundle.get('_compiler_entry_evidence',{})
            proof=table.get(target,{}) if isinstance(table,CompilerEntryEvidence) else {}
            branch=proof.get('branches',{}).get(selector)
            types={n.get('nodeType') for n in matches}
            valid=proof.get('program_id')==p.bundle['program_id'] and proof.get('build_id')==p.bundle['build_id']
            if len(matches)==2 and types=={'FunctionDefinition','VariableDeclaration'} and valid and branch:
                selected=[n for n in matches if tuple(map(int,n['src'].split(':')))==
                    (branch['source_start'],branch['source_length'],branch['source_file_id'])]
                if len(selected)==1:
                    chosen=selected[0]
                    self.dispatch_proofs[str(chosen['id'])+':'+sig]={k:v for k,v in proof.items() if k!='branches'}|{'selector':selector,**branch}
                    return chosen
            require(False,'entry_same_scope_ambiguous:'+sig)
        return None
    def select(self,candidates,order,reason):
        if not candidates:return None
        for scope in order:
            matches=[n for n in candidates if n.get('scope')==scope]
            if matches:
                require(len(matches)==1,reason)
                return matches[0]
        return None
    def getter_shape(self,node,abi):
        if node.get('stateVariable') is not True or node.get('visibility')!='public':return False
        if node.get('functionSelector') is not None:return node['functionSelector']==abi['selector']
        args=[];typ=node.get('typeName',{})
        while typ.get('nodeType') in ('Mapping','ArrayTypeName'):
            if typ['nodeType']=='Mapping':
                pair=declared_type_pair(typ.get('keyType',{}),self.lookup)
                if pair is None:return False
                args.append(pair[1]);typ=typ.get('valueType',{})
            else:args.append('uint256');typ=typ.get('baseType',{})
        pair=declared_type_pair(typ,self.lookup)
        outputs=[pair[1]] if pair else None
        if typ.get('nodeType')=='UserDefinedTypeName':
            decl=self.lookup.nodes.get(typ.get('referencedDeclaration'),{})
            if decl.get('nodeType')=='StructDefinition':
                members=[m.get('typeName',{}) for m in decl.get('members',[]) if m.get('typeName',{}).get('nodeType') not in ('Mapping','ArrayTypeName')]
                pairs=[declared_type_pair(m,self.lookup) for m in members]
                if pairs and all(pairs):outputs=[p[1] for p in pairs]
        return bool(outputs and abi['signature']==node['name']+'('+','.join(args)+')' and abi['types']==args and abi['outputs']==outputs)
    def special(self,kind):
        p=self.lookup;order=p.contract_node.get('linearizedBaseContracts',[p.contract_node['id']])
        nodes=[n for n in p.implementations if function_kind(n)==kind]
        return self.select(nodes,order,'special_entry_ambiguous:'+kind)
    def function(self,sig):
        p=self.lookup;order=p.contract_node.get('linearizedBaseContracts',[p.contract_node['id']])
        if sig not in p.abi and sig in ('fallback','fallback()','()','receive','receive()'):
            kind='receive' if sig.startswith('receive') else 'fallback';node=self.special(kind)
            require(node is not None,'special_entry_not_found:'+kind)
            self.record(node,kind+'()',None,'compiler_special_kind_and_inheritance')
            return node
        if sig=='constructor':
            fs=[n for n in p.implementations if function_kind(n)=='constructor' and n.get('scope')==p.contract_node['id']]
            require(len(fs)<=1,'constructor_ast_ambiguous')
            if fs:self.record(fs[0],sig,None,'compiler_kind_or_legacy_isConstructor')
            return fs[0] if fs else None
        abi=p.abi[sig];selector=abi['selector']
        require(len({f['signature'] for f in p.contract['functions'] if f['selector']==selector})==1,'entry_selector_collision')
        candidates=[];ambiguous=[]
        for node in p.implementations:
            if function_kind(node)!='function' or node.get('visibility') not in ('public','external'):continue
            original=node.get('functionSelector')
            if original is not None:
                if self.selector(node)==selector:
                    signatures={n.get('signature') for n in self.native(node)}
                    require(not signatures or signatures=={sig},'entry_native_signature_conflict:'+sig)
                    candidates.append(node)
                continue
            native=self.native(node);signatures={n.get('signature') for n in native}
            if sig in signatures:
                if len(signatures)!=1:ambiguous.append(node)
                elif self.selector(node)==selector:candidates.append(node)
        require(not ambiguous,'legacy_entry_native_signature_ambiguous:'+sig)
        getters=[n for n in p.decls.values() if n.get('scope') in order and self.getter_shape(n,abi)]
        chosen=self.select_entry(candidates+getters,order,sig,selector)
        if chosen:
            if chosen.get('nodeType')=='VariableDeclaration':
                self.record(chosen,sig,selector,'compiler_public_getter_shape')
                return {'generated_getter':chosen}
            self.record(chosen,sig,selector,'compiler_selector' if chosen.get('functionSelector') is not None else 'compiler_ABI_native_exact_source')
            return chosen
        same_name=[n for n in p.implementations if function_kind(n)=='function' and n.get('name')==sig.split('(')[0]]
        require(not same_name,'implemented_entry_identity_unresolved:'+sig)
        require(False,'missing_implemented_entry:'+sig)

~~~~

## file-afe6f743a0005c

`source/src/pr_next_joint/frontend/source_intake.py` · 原字节 SHA-256 `0332616db2369265a8de051363c1bcaa8e9060823f741e2322f9177e4777449f`

~~~~python
"""M03 source intake: manifest validation, neutral compile inputs, and report adapter boundary.

This module never reads expectations, cases IDs for dispatch, or answer tables. It
accepts ordinary source projects and, once compiled artifacts exist, hands the
result to the existing static/M4/report stack.
"""
import hashlib, json, pathlib, re
from pr_next_joint.core import require, digest

def _sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def _read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def inspect_case(root, case, require_entry=True):
    root = pathlib.Path(root)
    cid = case['case_id']
    require(re.fullmatch(r'[A-Za-z0-9_]+', cid), 'M03_CASE_ID')
    require(case.get('compiler_version') == '0.8.20', 'M03_COMPILER_VERSION')
    files = [root / p for p in case['source_files']]
    require(files and all(p.is_file() for p in files), 'M03_SOURCE_MISSING:' + cid)
    texts = {p.relative_to(root).as_posix(): p.read_text(encoding='utf-8') for p in files}
    require(any(re.search(r'pragma\s+solidity\s+\^?0\.8\.20', t) for t in texts.values()),
            'M03_PRAGMA_MISMATCH:' + cid)
    if require_entry or case.get('entry_source') or case.get('entry_contract'):
        require(bool(case.get('entry_source')) and bool(case.get('entry_contract')), 'M03_ENTRY_IDENTITY_INCOMPLETE:' + cid)
        entry = root / case['entry_source']
        require(entry in files and entry.is_file() and ('contract ' + case['entry_contract']) in entry.read_text(encoding='utf-8'),
                'M03_ENTRY_CONTRACT_MISSING:' + cid)
    # Multi-contract relationships are source facts, not one combined project.
    relations = []
    for rel, text in texts.items():
        for name in re.findall(r'new\s+([A-Za-z_][A-Za-z0-9_]*)', text):
            relations.append({'file': rel, 'creates': name})
    return {'schema': 'm03-source-case-v1', 'case_id': cid,
            'entry_contract': case.get('entry_contract'), 'entry_source': case.get('entry_source'),
            'compiler_version': case['compiler_version'],
            'sources': [{'path': p.relative_to(root).as_posix(), 'sha256': _sha(p),
                         'bytes': p.stat().st_size} for p in files],
            'constructor_relations': sorted(relations, key=lambda x: (x['file'], x['creates'])),
            'project_description': case.get('project_description'),
            'source_only': True, 'compiled': False, 'expectations_read': False}

def standard_input(root, case):
    root = pathlib.Path(root)
    sources = {p: {'content': (root / p).read_bytes().decode('utf-8')}
               for p in case['source_files']}
    return {'language': 'Solidity',
            'sources': sources,
            'settings': {'optimizer': {'enabled': True, 'runs': 200},
                         'evmVersion': 'paris',
                         'outputSelection': {'*': {'*': ['abi', 'evm.bytecode.object',
                                                       'evm.deployedBytecode.object', 'evm.bytecode.sourceMap',
                                                       'evm.deployedBytecode.sourceMap', 'metadata',
                                                       'evm.methodIdentifiers',
                                                       'evm.deployedBytecode.immutableReferences',
                                                       'evm.bytecode.linkReferences',
                                                       'evm.deployedBytecode.linkReferences',
                                                       'storageLayout'],
                                                   '': ['ast']}}}}

def inspect_manifest(root, manifest_path, target_mode='entry'):
    root = pathlib.Path(root); manifest = _read(root / manifest_path)
    require(manifest.get('format_version') == 1 and len(manifest.get('cases', [])) >= 1,
            'M03_CASE_SET_EMPTY')
    out = []
    for case in manifest['cases']:
        audit = inspect_case(root, case, require_entry=target_mode!='project')
        audit['standard_input'] = standard_input(root, case)
        audit['standard_input_sha256'] = digest(audit['standard_input'])
        out.append(audit)
    seen = [x['case_id'] for x in out]
    require(len(seen) == len(set(seen)), 'M03_CASE_DUPLICATE')
    return {'schema': 'm03-manifest-inspection-v1', 'cases': out,
            'case_count': len(out), 'source_file_count': sum(len(x['sources']) for x in out)}

def validate_loaded_artifacts(case, bundle, native, *, compiler_sources=None):
    """Bind cached facts to inspected compiler-input text before calling M2.

    Existing source anchors hash the entire compiler-input source, not a snippet.
    This cache check is not a compiler execution or runtime qualification.
    """
    for field in ('program_id', 'build_id'):
        require(bool(bundle.get(field)) and bundle[field] == native.get(field),
                'M03_NATIVE_' + field.upper() + '_MISMATCH')
    require(bundle.get('native_ir', {}).get('sha256') == digest(native),
            'M03_NATIVE_CONTENT_MISMATCH')
    sources = case['standard_input']['sources']
    require(set(bundle.get('ast_sources', {})) == set(sources),
            'M03_COMPILED_SOURCE_SET_MISMATCH')
    anchors = {}
    for record in bundle.get('functions', []) + bundle.get('state_declarations', []):
        anchor = record.get('source_anchor', {})
        if anchor.get('file') is not None:
            anchors.setdefault(anchor['file'], set()).add(anchor.get('sha256'))
    require(set(anchors) <= set(sources), 'M03_SOURCE_ANCHOR_OUTSIDE_INPUT')
    refs = []
    disk_hashes = {s['path']: s['sha256'] for s in case['sources']}
    for path, value in sources.items():
        # Windows read_text normalizes newlines for the compiler input; preserve
        # that identity separately from the original file-byte identity.
        source_hash = hashlib.sha256(value['content'].encode('utf-8')).hexdigest()
        proof=None
        if path in anchors:
            require(anchors[path] == {source_hash}, 'M03_COMPILED_SOURCE_MISMATCH:' + path)
        else:
            from pr_next_joint.frontend.compiler_evidence import CompilerSourceEvidence
            valid=isinstance(compiler_sources,CompilerSourceEvidence) and compiler_sources.program_id==bundle['program_id'] and compiler_sources.build_id==bundle['build_id']
            proof=compiler_sources.get(path) if valid else None
            require(proof and proof.get('source_sha256')==source_hash, 'M03_COMPILED_SOURCE_IDENTITY_UNAVAILABLE:' + path)
        row={'file': path, 'sha256': source_hash,
                     'file_bytes_sha256': disk_hashes[path],
                     'hash_scope': 'compiler_input_source_utf8'}
        if proof:row['compiler_metadata_proof']=proof
        refs.append(row)
    return {'status': 'matched', 'program_id': bundle['program_id'],
            'build_id': bundle['build_id'], 'sources': refs,
            'compiled_here': False, 'runtime_pass': False}

~~~~

## file-f4f852d29af6b0

`source/src/pr_next_joint/frontend/source_library_binding.py` · 原字节 SHA-256 `099076dbf0fa876c6c3a55600d226bc5bbc78c27ab12dfe351e72a539c856632`

~~~~python
"""Exact compiler-bound internal library receivers, including storage references.

Only top-level storage ref/pointer decoration is normalized. Declaration IDs,
array shapes, mapping key/value types, location and call kind stay distinct.
"""
import re

def storage_identity(typ):
    if not typ.startswith(('t_struct$', 't_array$', 't_mapping$')):
        return None
    return re.sub(r'_storage(?:_ptr|_ref)?$', '_storage', typ) if re.search(r'_storage(?:_ptr|_ref)?$',typ) else None

def receiver_matches(receiver_type, parameter_type):
    if receiver_type and receiver_type==parameter_type:return True
    a,b=storage_identity(receiver_type),storage_identity(parameter_type)
    return a is not None and a==b

def compiler_bound_receiver(lookup,node,target):
    from pr_next_joint.frontend.path_ir import walk
    if not target or target.get('nodeType')!='FunctionDefinition' or node.get('names') or not target.get('body') or target.get('visibility')!='internal':return False
    scope=lookup.nodes.get(target.get('scope'),{})
    if scope.get('nodeType')!='ContractDefinition' or scope.get('contractKind')!='library':return False
    expr=node.get('expression',{});args=node.get('arguments',[])
    params=target.get('parameters',{}).get('parameters',[])
    if expr.get('nodeType')!='MemberAccess' or len(params)!=len(args)+1:return False
    if expr.get('referencedDeclaration')!=target.get('id'):return False
    signature=expr.get('typeDescriptions',{}).get('typeIdentifier','')
    receiver=expr.get('expression',{})
    typ=receiver.get('typeDescriptions',{}).get('typeIdentifier','')
    parameter=params[0].get('typeDescriptions',{}).get('typeIdentifier','')
    if not receiver_matches(typ,parameter):return False
    if not signature.startswith('t_function_internal_'):return False
    if not any(signature.endswith('$'+marker+'$_'+bound+'_$') for marker in ('bound_to','attached_to') for bound in (typ,parameter)):return False
    return not any(n.get('nodeType')=='Assignment' or n.get('nodeType')=='UnaryOperation' and n.get('operator') in ('++','--','delete') for n in walk([receiver,*args]))

~~~~

## file-df65dbc485aef5

`source/src/pr_next_joint/frontend/source_local_values.py` · 原字节 SHA-256 `fa080ffa0ef62752e3f9848330df4a7988eaad4ad02136e02c1cb2d9a1b67cbe`

~~~~python
"""Bounded value copies and local composite assignments, never storage aliases."""
import copy
from pr_next_joint.frontend.path_ir import key, lit
def snapshot(value,typ,lookup,state,depth=0):
    if depth>8:raise ValueError('memory_snapshot_depth_limit')
    if value.get('kind')!='storage':return copy.deepcopy(value)
    if typ.get('nodeType')=='ArrayTypeName':
        length=typ.get('length') or {}
        if length.get('nodeType')!='Literal':raise ValueError('dynamic_storage_to_memory_snapshot_not_lowered')
        size=int(length['value'])
        if size>32:raise ValueError('memory_snapshot_array_bound')
        return {'kind':'array','items':[snapshot({**value,'segments':value.get('segments',[])+[{'key':lit(i)}]},typ['baseType'],lookup,state,depth+1) for i in range(size)]}
    if typ.get('nodeType')=='UserDefinedTypeName':
        node=lookup.nodes.get(typ.get('referencedDeclaration'),{})
        if node.get('nodeType')!='StructDefinition':raise ValueError('memory_snapshot_user_type_unresolved')
        return {'kind':'record','fields':[{'field':f['id'],'value':snapshot({**value,'segments':value.get('segments',[])+[{'field':f['id']}]},f['typeName'],lookup,state,depth+1)} for f in node['members']]}
    result=copy.deepcopy(value)
    from pr_next_joint.frontend.path_ir import op
    for write in state['writes']:
        path=write['path']
        if path.get('root')!=value.get('root') or key(path.get('instance'))!=key(value.get('instance')):continue
        left=path.get('segments',[]);right=value.get('segments',[])
        if len(left)!=len(right):raise ValueError('memory_snapshot_overlapping_container_write')
        conditions=[];same=True
        for x,y in zip(left,right):
            if 'key' in x and 'key' in y:conditions.append(op('==',x['key'],y['key']))
            elif x!=y:same=False;break
        if not same:continue
        if key(path)==key(value):result=copy.deepcopy(write['value'])
        elif conditions:result={'kind':'conditional','condition':op('and',*conditions),'when_true':copy.deepcopy(write['value']),'when_false':result}
    return result
def local_root(node,lookup):
    if node.get('nodeType')=='Identifier':
        decl=lookup.nodes.get(node.get('referencedDeclaration'),{})
        return decl['id'] if decl.get('storageLocation')=='memory' and not decl.get('stateVariable') else None
    if node.get('nodeType')=='MemberAccess':return local_root(node.get('expression',{}),lookup)
    if node.get('nodeType')=='IndexAccess':return local_root(node.get('baseExpression',{}),lookup)
    return None
def assign(node,value,lookup,state):
    if node.get('nodeType')=='Identifier':state['env'][node['referencedDeclaration']]=copy.deepcopy(value);return
    if node.get('nodeType')=='MemberAccess':
        parent=lookup.evaluate(node['expression'],state['env'])
        if parent.get('kind')!='record':raise ValueError('memory_record_write_not_lowered')
        revised=copy.deepcopy(parent);field=next((x for x in revised['fields'] if x['field']==node.get('referencedDeclaration')),None)
        if field is None:raise ValueError('memory_record_field_unresolved')
        field['value']=copy.deepcopy(value);assign(node['expression'],revised,lookup,state);return
    if node.get('nodeType')=='IndexAccess':
        parent=lookup.evaluate(node['baseExpression'],state['env']);index=lookup.value(node['indexExpression'],state['env'])
        if parent.get('kind')!='array' or index.get('kind')!='literal' or type(index.get('value')) is not int or not 0<=index['value']<len(parent['items']):raise ValueError('memory_array_write_not_lowered')
        revised=copy.deepcopy(parent);revised['items'][index['value']]=copy.deepcopy(value);assign(node['baseExpression'],revised,lookup,state);return
    raise ValueError('memory_assignment_shape_not_lowered')

~~~~

## file-126791d06878de

`source/src/pr_next_joint/frontend/source_loop_scope.py` · 原字节 SHA-256 `665d5d9f95981e5d8d237e4fa4204ae87c99c38d14922f661304299083543ad3`

~~~~python
"""Choose expansion from a proven constant source counter, never sample identity."""
from pr_next_joint.frontend.local_constants import constant_integer

def loop_limit(node, lookup, state, maximum=32):
    if node.get('nodeType')!='ForStatement':return 2
    condition=node.get('condition') or {};update=(node.get('loopExpression') or {}).get('expression',{})
    left=condition.get('leftExpression',{});right=condition.get('rightExpression',{})
    ident=left.get('referencedDeclaration');initial=state.get('env',{}).get(ident,{})
    if left.get('nodeType')!='Identifier' or initial.get('kind')!='literal' or type(initial.get('value')) is not int:return 2
    stop=constant_integer(right)
    if stop is None:return 2
    if update.get('nodeType')!='UnaryOperation' or update.get('subExpression',{}).get('referencedDeclaration')!=ident:return 2
    step=1 if update.get('operator')=='++' else -1 if update.get('operator')=='--' else 0
    from pr_next_joint.frontend.path_ir import walk
    for item in walk(node.get('body')):
        dest=item.get('leftHandSide',{}) if item.get('nodeType')=='Assignment' else item.get('subExpression',{}) if item.get('nodeType')=='UnaryOperation' and item.get('operator') in ('++','--','delete') else {}
        if dest.get('referencedDeclaration')==ident:return 2
    operator=condition.get('operator');start=initial['value']
    if step==1 and operator in ('<','<='):count=max(0,stop-start+(operator=='<='))
    elif step==-1 and operator in ('>','>='):count=max(0,start-stop+(operator=='>='))
    else:return 2
    return min(maximum,count) if count<=maximum else 2


def invariant_local_condition(node,lookup):
    """A local scalar test untouched by the loop, with no successful exit.

    Used to avoid repeatedly expanding a source loop whose true branch cannot
    reach its continuation. The branch remains truncated, never assumed safe.
    Old view declarations alone do not suffice: inspect every called body.
    """
    from pr_next_joint.frontend.path_ir import walk
    from pr_next_joint.frontend.source_entry_identity import function_mutability, builtin_call
    condition=node.get('condition') or {};ref=condition.get('referencedDeclaration')
    declaration=lookup.nodes.get(ref,{})
    if condition.get('nodeType')!='Identifier' or declaration.get('stateVariable') or declaration.get('typeDescriptions',{}).get('typeString')!='bool':return False
    content=[node.get('body'),node.get('loopExpression')];seen=set()
    def safe(items,depth=0):
        if depth>8:return False
        for item in walk(items):
            k=item.get('nodeType')
            if k in ('Break','Return','InlineAssembly','NewExpression','EmitStatement'):return False
            dest=item.get('leftHandSide',{}) if k=='Assignment' else item.get('subExpression',{}) if k=='UnaryOperation' and item.get('operator') in ('++','--','delete') else {}
            if dest.get('referencedDeclaration')==ref:return False
            if k=='FunctionCall' and item.get('kind') not in ('typeConversion','structConstructorCall'):
                if builtin_call(item,lookup,('require','assert','revert')):continue
                target=lookup.fns.get(item.get('expression',{}).get('referencedDeclaration'))
                if not target or function_mutability(target) not in ('pure','view') or not target.get('body'):return False
                # Return inside a pure/read-only helper ends only that helper.
                if target['id'] in seen:return False
                seen.add(target['id'])
                body=target['body']
                for n in walk(body):
                    if n.get('nodeType') in ('NewExpression','InlineAssembly','EmitStatement'):return False
                    mutation=(n.get('leftHandSide') if n.get('nodeType')=='Assignment' else n.get('subExpression') if n.get('nodeType')=='UnaryOperation' and n.get('operator') in ('++','--','delete') else None)
                    if mutation:
                        d=lookup.nodes.get(mutation.get('referencedDeclaration'),{})
                        if mutation.get('nodeType')!='Identifier' or d.get('nodeType')!='VariableDeclaration' or d.get('stateVariable') or d.get('storageLocation')=='storage':return False
                # Library arithmetic helpers may return, but no other calls
                # may hide global termination or mutation in old compilers.
                calls=[n for n in walk(body) if n.get('nodeType')=='FunctionCall']
                if not safe(calls,depth+1):return False
                seen.remove(target['id'])
        return True
    return safe(content)

~~~~

## file-a811b86bf973ef

`source/src/pr_next_joint/frontend/source_observers.py` · 原字节 SHA-256 `9d962da5f91132c18f31b42eebf00a18ee7990f285bdd85e1013ac57a8836ce4`

~~~~python
"""Compiler-bound getter descriptions for fixed-word storage observations.

This resolves paths; it does not infer permissions or prove program effects.
Use with SourcePaths and existing plan/program/instance identity validation.
No raw storage slots, model-selected output offsets or project-name dispatch.
"""
import copy
import re

from pr_next_joint.core import require


def _elementary(node):
    require(node.get('nodeType') == 'ElementaryTypeName', 'observer_non_elementary_type')
    name = node['name']
    return {'uint': 'uint256', 'int': 'int256', 'address payable': 'address'}.get(name, name)


def _handwritten_getter(lookup, root, segments):
    """Prove a read-only ABI entry returns this exact storage path.

    Only an unmodified, single-return body without modifiers is accepted.
    Names, documentation and equal return values are not binding evidence.
    Index arguments may be permuted, but storage key order remains explicit.
    """
    matches = []
    for abi in lookup.contract['functions']:
        if not abi.get('readonly') or len(abi.get('outputs', [])) != 1:
            continue
        entry = lookup.function(abi['signature']) or {}
        body = (entry.get('body') or {}).get('statements', [])
        if entry.get('generated_getter') or entry.get('modifiers') or len(body) != 1 or body[0].get('nodeType') != 'Return':
            continue
        expression = body[0].get('expression') or {}
        chain = []
        while expression.get('nodeType') in ('MemberAccess', 'IndexAccess'):
            if expression['nodeType'] == 'MemberAccess':
                chain.append(('field', expression.get('referencedDeclaration')))
                expression = expression.get('expression') or {}
            else:
                index = expression.get('indexExpression') or {}
                if index.get('nodeType') != 'Identifier':
                    break
                chain.append(('key', index.get('referencedDeclaration')))
                expression = expression.get('baseExpression') or {}
        if expression.get('nodeType') != 'Identifier' or expression.get('referencedDeclaration') != root:
            continue
        chain.reverse()
        if len(chain) != len(segments):
            continue
        parameters = [p['id'] for p in entry.get('parameters', {}).get('parameters', [])]
        ordered = []
        compatible = True
        for (kind, value), segment in zip(chain, segments):
            if kind == 'key' and 'key' in segment:
                if value not in parameters or value in ordered:
                    compatible = False; break
                ordered.append(value)
            elif kind == 'field' and 'field' in segment:
                selected = segment['field']
                if value != (selected.get('ast_id') if isinstance(selected, dict) else selected):
                    compatible = False; break
            else:
                compatible = False; break
        if not compatible or len(parameters) != len(ordered) or set(parameters) != set(ordered):
            continue
        matches.append((abi, [ordered.index(p) for p in parameters], entry['id'], body[0]['id']))
    # Multiple source-equivalent aliases do not make the object ambiguous.
    return sorted(matches, key=lambda r: r[0]['signature'])[0] if matches else None


def describe_getter(lookup, path):
    """Resolve scalar or mapping-chain -> flat struct member against AST + ABI.

    Accept SourcePaths storage paths or normalized storage_binding paths.
    Unbound key terms remain terms; bind_getter requires concrete ABI arguments.
    Supports generated getters and proven direct hand-written accessors.
    Computed/conditional getters and unbound key expressions remain unsupported.
    """
    require(path.get('kind') in ('storage', 'storage_binding'), 'observer_path_kind')
    if path['kind'] == 'storage_binding':
        for key in ('program_id', 'build_id'):
            require(path.get(key) == lookup.bundle[key], 'observer_' + key + '_mismatch')
        root = path['declaration']['ast_id']
    else:
        root = path['root']
    state = lookup.decls.get(root)
    require(state is not None and state.get('stateVariable'), 'observer_state_missing')
    bases = lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']])
    require(state.get('scope') in bases, 'observer_state_outside_contract')
    getters = []
    for entry in lookup.contract['functions']:
        if entry['signature'].split('(')[0] != state['name'] or not entry['readonly']:
            continue
        implementation = lookup.function(entry['signature'])
        if implementation.get('generated_getter', {}).get('id') == root:
            getters.append(entry)
    require(len(getters) <= 1, 'observer_getter_ambiguous')
    explicit = _handwritten_getter(lookup, root, path.get('segments', []))
    require(getters or explicit is not None, 'observer_source_bound_getter_required')
    getter = getters[0] if getters else explicit[0]
    generated = bool(getters)
    typ = state['typeName']
    segments = copy.deepcopy(path.get('segments', []))
    key_types, key_terms = [], []
    while typ.get('nodeType') == 'Mapping':
        require(segments and 'key' in segments[0], 'observer_mapping_key_missing')
        key_types.append(_elementary(typ['keyType']))
        key_terms.append(segments.pop(0)['key'])
        typ = typ['valueType']
    argument_order = list(range(len(key_types))) if generated else explicit[1]
    require(getter['types'] == [key_types[i] for i in argument_order], 'observer_getter_input_mismatch')
    field_id = None
    if typ.get('nodeType') == 'UserDefinedTypeName':
        struct = lookup.nodes.get(typ.get('referencedDeclaration'), {})
        require(struct.get('nodeType') == 'StructDefinition', 'observer_struct_required')
        require(len(segments) == 1 and 'field' in segments[0], 'observer_flat_field_required')
        field = segments[0]['field']
        field_id = field.get('ast_id') if isinstance(field, dict) else field
        # Solidity's public getter omits mapping/array members of a struct.
        # bytes/string use ElementaryTypeName and remain ABI outputs.
        returned = [member for member in struct['members']
                    if member['typeName'].get('nodeType') not in ('Mapping', 'ArrayTypeName')]
        require(all(member['typeName'].get('nodeType') == 'ElementaryTypeName'
                    for member in returned), 'observer_nested_struct_unsupported')
        expected_outputs = [_elementary(member['typeName']) for member in returned]
        selected = [index for index, member in enumerate(returned) if member['id'] == field_id]
        require(len(selected) == 1, 'observer_field_not_returned')
        index = selected[0]
        if not generated:
            expected_outputs = [expected_outputs[index]]
            index = 0
    else:
        require(not segments, 'observer_extra_path_segments')
        expected_outputs = [_elementary(typ)]
        index = 0
    require(getter['outputs'] == expected_outputs, 'observer_getter_output_mismatch')
    abi_type = expected_outputs[index]
    value_types = {'bool': 'Bool', 'address': 'Address160', 'uint256': 'BV256', 'bytes32': 'BV256'}
    require(abi_type in value_types, 'observer_fixed_word_type_unsupported:' + abi_type)
    result = {
        'program_id': lookup.bundle['program_id'], 'build_id': lookup.bundle['build_id'],
        'contract_file': lookup.contract['file'], 'contract_name': lookup.contract['name'],
        'root_ast_id': root, 'field_ast_id': field_id,
        'function': getter['signature'], 'selector': getter['selector'],
        'key_types': key_types, 'key_terms': key_terms, 'output_index': index,
        'argument_order': argument_order,
        'abi_type': abi_type, 'type': value_types[abi_type],
        'representation': 'abi_word_as_bv256' if abi_type == 'bytes32' else 'native_fixed_word',
    }
    result['source_proof'] = ({'kind': 'compiler_generated_getter', 'state_ast_id': root} if generated else
                              {'kind': 'source_exact_single_return', 'state_ast_id': root,
                               'function_ast_id': explicit[2], 'return_ast_id': explicit[3],
                               'modifiers': False, 'storage_key_order_preserved': True})
    if 'instance_id' in path:
        result['instance_id'] = path['instance_id']
    return result


def bind_getter(lookup, path, arguments):
    """Bind already resolved key values, retaining their ABI order and type.

    Caller still checks that values come from the intended object/subject in
    the current plan. Argument validity alone is NOT a provenance proof.
    """
    result = describe_getter(lookup, path)
    require(len(arguments) == len(result['key_types']), 'observer_argument_count')
    for typ, value in zip(result['key_types'], arguments):
        if typ in ('address', 'bytes32'):
            width = 40 if typ == 'address' else 64
            require(isinstance(value, str) and re.fullmatch('0x[0-9a-fA-F]{' + str(width) + '}', value),
                    'observer_argument_encoding:' + typ)
        elif re.fullmatch('uint([0-9]+)', typ):
            require(not isinstance(value, bool), 'observer_uint_boolean')
            require(isinstance(value, int) or (isinstance(value, str) and re.fullmatch('[0-9]+', value)),
                    'observer_uint_encoding')
            bits = int(typ[4:])
            require(8 <= bits <= 256 and bits % 8 == 0 and 0 <= int(value) < 2 ** bits,
                    'observer_uint_range')
        elif typ == 'bool':
            require(isinstance(value, bool), 'observer_bool_encoding')
        else:
            raise ValueError('observer_key_type_unsupported:' + typ)
    result['storage_key_arguments'] = copy.deepcopy(list(arguments))
    result['arguments'] = [copy.deepcopy(arguments[i]) for i in result['argument_order']]
    result['observer_fields'] = {key: result[key] for key in ('function', 'arguments', 'type', 'output_index')}
    return result

~~~~

## file-b343e0d94a5a3d

`source/src/pr_next_joint/frontend/source_paths.py` · 原字节 SHA-256 `aad1a722cbe2a9df8453f42746c260628609f1054f29506ec0afb2ab3830124f`

~~~~python
"""Source-derived storage paths with parameter/caller substitution.

This is a conservative provenance tracer, NEVER an EVM state interpreter. Unknown
values remain terms. Branch unions cannot prove effects; original execution does.
"""
import copy,json,re
from pr_next_joint.frontend.source_entry_identity import elementary_expression_name
from pr_next_joint.frontend.facts import walk
from pr_next_joint.core import require, digest
from pr_next_joint.frontend.source_entry_identity import EntryIdentity, function_kind, source_file

def stable(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def paths_in(value):
 if isinstance(value,dict):
  if value.get('kind')=='storage':yield value
  for v in value.values():yield from paths_in(v)
 elif isinstance(value,list):
  for v in value:yield from paths_in(v)

def compatible(a,b):
 """Exact subject/field/array-key equality; whole-struct writes cover children."""
 return a['root']==b['root'] and (a['segments']==b['segments'][:len(a['segments'])] or b['segments']==a['segments'][:len(b['segments'])])

class SourcePaths:
 def __init__(self,bundle,contract,aliases=None):
  self.bundle=bundle;self.contract=contract
  self.aliases=aliases or {}
  self.nodes={n['id']:n for ast in bundle['ast_sources'].values() for n in walk(ast) if 'id' in n}
  self.decls={n['id']:n for n in self.nodes.values() if n.get('nodeType')=='VariableDeclaration'}
  self.fns={n['id']:n for n in self.nodes.values() if n.get('nodeType') in ['FunctionDefinition','ModifierDefinition']}
  file_id=int(bundle['ast_sources'][contract['file']]['src'].split(':')[-1])
  cs=[n for n in self.nodes.values() if n.get('nodeType')=='ContractDefinition' and n['name']==contract['name'] and int(n['src'].split(':')[-1])==file_id]
  require(len(cs)==1,'contract_ast_ambiguous');self.contract_node=cs[0]
  order=self.contract_node.get('linearizedBaseContracts',[self.contract_node['id']])
  self.implementations=[f for cid in order for f in self.nodes[cid].get('nodes',[]) if f.get('nodeType')=='FunctionDefinition' and f.get('body')]
  self.abi={f['signature']:f for f in contract['functions']}
  self.entry_identity=EntryIdentity(self)
 def function(self,sig):
  return self.entry_identity.function(sig)
 def function_selector(self,node):return self.entry_identity.selector(node)
 def anchor(self,n):
  if not isinstance(n,dict):raise ValueError('source_anchor_node_missing')
  origin='compiler_src';raw=n.get('src')
  if not raw and n.get('id') in self.nodes:raw=self.nodes[n['id']].get('src')
  if not raw:
   # Generated expression wrappers inherit only an exact, single-file child span.
   spans=[]
   for child in walk(n):
    if child is n or not isinstance(child.get('src'),str):continue
    a,b,f=map(int,child['src'].split(':'))
    if a>=0 and b>=0 and f>=0:spans.append((a,b,f))
   if not spans or len({x[2] for x in spans})!=1:raise ValueError('source_anchor_unresolved')
   start=min(x[0] for x in spans);length=max(x[0]+x[1] for x in spans)-start;file_id=spans[0][2]
   origin='generated_wrapper_child_span'
  else:start,length,file_id=map(int,raw.split(':'))
  files={int(ast['src'].split(':')[-1]):f for f,ast in self.bundle['ast_sources'].items()}
  return {'file':files.get(file_id),'start':start,'length':length,'ast_id':n.get('id'),**({'anchor_origin':origin} if origin!='compiler_src' else {})}
 def trace(self,sig,args,caller='$B'):
  self.reads=[];self.writes=[];self.guards=[];self.calls=[];self.unknown=[];self.stack=[]
  f=self.function(sig)
  if not f:return {'reads':[],'writes':[],'guards':[],'calls':[],'returns':[],'unresolved':[],'native_agreement':True}
  if 'generated_getter' in f:
   d=f['generated_getter'];p={'kind':'storage','root':d['id'],'segments':[{'key':self.literal(v,t)} for v,t in zip(args,self.abi[sig]['types'])]}
   require(any(d['name']==name.split('.')[-1] for fn in self.bundle['native_ir']['functions'] for name in fn['reads']+fn['writes']),'public_getter_native_state_missing')
   return {'entry':self.anchor(d),'reads':[p],'writes':[],'guards':[],'calls':[],'returns':[p],'unresolved':[],'native_agreement':True,'generated_getter':True}
  self.sender=caller;self.entry=f;self.arguments=args
  values=[self.literal(v,t) for v,t in zip(args,self.contract['constructor_types'] if sig=='constructor' else self.abi[sig]['types'])]
  self.calldata={'kind':'calldata','selector':self.function_selector(f),'arguments':values}
  returns=self.call(f,values,{})
  native=self.entry_identity.native(f)
  require(native,'missing_native_function_binding')
  # Native SSA is an independent gate, not a decorative receipt. Every traced
  # state root must also occur in the native transitive read/write inventory.
  names=lambda key:{str(v).split('.')[-1] for n in native for v in n[key]}
  readnames=names('reads')|names('writes');writenames=names('writes')
  badread=[p for p in self.reads if self.nodes[p['root']]['name'] not in readnames]
  badwrite=[w for w in self.writes if self.nodes[w['path']['root']]['name'] not in writenames]
  return {'entry':self.anchor(f),'reads':self.unique(self.reads),'writes':self.unique(self.writes),'guards':self.unique(self.guards),'calls':self.unique(self.calls),'returns':returns,'unresolved':self.unique(self.unknown),'native_agreement':not badread and not badwrite,'native_disagreements':{'reads':badread,'writes':badwrite},'native_function_sources':[n['source'] for n in native]}
 def unique(self,x):return list({stable(v):v for v in x}.values())
 def literal(self,v,typ=None):
  if isinstance(v,dict):return v
  if isinstance(v,str):v=self.aliases.get(v,v)
  if typ=='bool':v=v in [True,'true','1',1]
  elif typ and (typ.startswith('uint') or typ.startswith('int')):v=int(v)
  return {'kind':'literal','value':v}
 def unknown_value(self,n):return {'kind':'unknown','source':self.anchor(n)}
 def evaluate(self,n,env):
  if not n:return self.literal(None)
  k=n.get('nodeType');rd=n.get('referencedDeclaration')
  if k=='Literal':
   v=n.get('value');v=(v=='true') if n['kind']=='bool' else int(v,0) if n['kind']=='number' else v
   return self.literal(v)
  if k in ['Identifier','IdentifierPath']:
   if rd in env:return env[rd]
   d=self.nodes.get(rd,{})
   if d.get('constant') and d.get('value'):return self.evaluate(d['value'],env)
   if d.get('stateVariable'):return {'kind':'storage','root':rd,'segments':[]}
   if n.get('name')=='this':return self.literal('$contract')
   return {'kind':'symbol','declaration':rd,'name':n.get('name')}
  if k=='MemberAccess':
   e=n['expression'];name=n['memberName'];v=self.evaluate(e,env)
   if v.get('kind')=='solidity_type' and name in ['min','max']:
    typ=v['name'];m=re.fullmatch('(u?int)([0-9]*)',typ)
    if m:
     bits=int(m[2] or 256);signed=m[1]=='int'
     return self.literal((-2**(bits-1) if signed else 0) if name=='min' else 2**(bits-int(signed))-1)
   if e.get('nodeType')=='Identifier' and e.get('name')=='msg':
    if name=='sender':return self.literal(self.sender)
    if name=='data':return self.calldata
    if name=='sig':return self.literal(self.calldata['selector'])
   if e.get('nodeType')=='Identifier' and e.get('name')=='block' and name=='timestamp':return {'kind':'environment','field':'timestamp'}
   if name=='selector':
    d=self.nodes.get(e.get('referencedDeclaration'),{});selector=self.function_selector(d)
    return self.literal(selector) if selector is not None else {'kind':'unknown','reason':'function_selector_unresolved','source':self.anchor(n)}
   if v.get('kind')=='calldata' and name=='length':return self.literal(4+32*len(v['arguments']))
   if v.get('kind')=='storage':return {**v,'segments':v['segments']+[{'field':rd,'label':name}]}
   return {'kind':'member','base':v,'member':name,'declaration':rd}
  if k=='IndexAccess':
   v=self.evaluate(n['baseExpression'],env);key=self.value(n.get('indexExpression'),env)
   if v.get('kind')=='storage':return {**v,'segments':v['segments']+[{'key':key}]}
   return {'kind':'index','base':v,'key':key}
  if k=='IndexRangeAccess':return {'kind':'slice','base':self.evaluate(n['baseExpression'],env),'start':self.value(n.get('startExpression'),env),'end':self.value(n.get('endExpression'),env)}
  if k=='TupleExpression':return {'kind':'tuple','items':[self.value(v,env) if v else self.literal(None) for v in n['components']]}
  if k=='BinaryOperation':return self.binary(n['operator'],self.value(n['leftExpression'],env),self.value(n['rightExpression'],env))
  if k=='UnaryOperation':
   v=self.value(n['subExpression'],env)
   if n['operator']=='!' and v.get('kind')=='literal':return self.literal(not v['value'])
   if n['operator']=='delete':self.assign(n['subExpression'],self.literal(0),env,n,'delete')
   return {'kind':'op','op':n['operator'],'args':[v]}
  if k=='Conditional':return {'kind':'choice','condition':self.value(n['condition'],env),'alternatives':[self.value(n['trueExpression'],env),self.value(n['falseExpression'],env)]}
  if k=='Assignment':
   value=self.value(n['rightHandSide'],env);self.assign(n['leftHandSide'],value,env,n,n['operator']);return value
  if k=='FunctionCall':
   e=n['expression'];args=[self.value(x,env) for x in n.get('arguments',[])];target=e.get('referencedDeclaration');f=self.fns.get(target)
   if e.get('name')=='type' and n.get('arguments'):return {'kind':'solidity_type','name':elementary_expression_name(n['arguments'][0])}
   if n.get('kind')=='structConstructorCall':
    struct=self.nodes.get(target,{})
    return {'kind':'record','fields':[{'field':m['id'],'value':v} for m,v in zip(struct.get('members',[]),args)]}
   if n.get('kind')=='typeConversion':
    if args and args[0].get('kind')=='slice' and args[0]['base'].get('kind')=='calldata':return self.literal(args[0]['base']['selector'])
    return args[0] if args else self.unknown_value(n)
   if e.get('nodeType')=='MemberAccess' and e.get('memberName')=='decode' and e.get('expression',{}).get('name')=='abi':
    v=args[0]
    if v.get('kind')=='slice' and v['base'].get('kind')=='calldata' and v['start'].get('kind')=='literal':
     ix=(v['start']['value']-4)//32
     if ix>=0 and ix<len(v['base']['arguments']):return v['base']['arguments'][ix]
   if f:
    if e.get('nodeType')=='MemberAccess' and len(f['parameters']['parameters'])==len(args)+1:
     args.insert(0,self.value(e['expression'],env))
    if not f.get('body'):
     selector=self.function_selector(f)
     fs=[x for x in self.implementations if selector is not None and self.function_selector(x)==selector]
     order=self.contract_node.get('linearizedBaseContracts',[self.contract_node['id']])
     chosen=self.entry_identity.select(fs,order,'internal_entry_selector_ambiguous')
     if chosen:f=chosen
     else:
      unresolved={'kind':'call_unresolved','reason':'compiler_referenced_body_unresolved','declaration':target,'source':self.anchor(n)}
      self.unknown.append(unresolved);return unresolved
    self.calls.append({'function':f['id'],'arguments':args,'source':self.anchor(n)})
    ret=self.call(f,args,env)
    if len(ret)==1:return ret[0]
    if ret:return {'kind':'choice','alternatives':ret}
   if e.get('name') in ['require','assert']:
    self.guards.append({'condition':args[0],'source':self.anchor(n),'origin':'require'});return self.literal(None)
   if e.get('nodeType')=='MemberAccess' and e.get('memberName') in ['wrap','unwrap']:return args[0] if args else self.unknown_value(n)
   # Event/custom-error constructors have no storage semantics.
   return {'kind':'call_unresolved','declaration':target,'arguments':args,'source':self.anchor(n)}
  self.unknown.append({'kind':k,'source':self.anchor(n)});return self.unknown_value(n)
 def value(self,n,env):
  v=self.evaluate(n,env)
  for p in paths_in(v):self.reads.append(p)
  return v
 def binary(self,op,a,b):
  if a.get('kind')==b.get('kind')=='literal':
   x,y=a['value'],b['value']
   try:
    if op=='==':return self.literal(x==y)
    if op=='!=':return self.literal(x!=y)
    if op=='&&':return self.literal(bool(x and y))
    if op=='||':return self.literal(bool(x or y))
    if op=='<':return self.literal(x<y)
    if op=='<=':return self.literal(x<=y)
    if op=='>':return self.literal(x>y)
    if op=='>=':return self.literal(x>=y)
   except TypeError:pass
  if op=='&&' and any(v.get('kind')=='literal' and v['value'] is False for v in [a,b]):return self.literal(False)
  if op=='||' and any(v.get('kind')=='literal' and v['value'] is True for v in [a,b]):return self.literal(True)
  return {'kind':'op','op':op,'args':[a,b]}
 def assign(self,left,value,env,source,op='='):
  if left.get('nodeType')=='TupleExpression':
   values=value.get('items',[]) if value.get('kind')=='tuple' else []
   for i,n in enumerate(left['components']):
    if n:self.assign(n,values[i] if i<len(values) else {'kind':'tuple_item','base':value,'index':i},env,source,op)
   return
  p=self.evaluate(left,env)
  if p.get('kind')=='storage':self.writes.append({'path':p,'value':value,'operator':op,'source':self.anchor(source),'function':self.stack[-1]})
  elif left.get('nodeType')=='Identifier':env[left['referencedDeclaration']]=value
 def call(self,f,args,outer):
  if f['id'] in self.stack or len(self.stack)>20:
   self.unknown.append({'recursion':f['id']});return []
  env={p['id']:v for p,v in zip(f['parameters']['parameters'],args)}
  self.stack.append(f['id'])
  for m in f.get('modifiers',[]):
   target=m['modifierName'].get('referencedDeclaration')
   if target in self.fns:self.call(self.fns[target],[self.value(a,env) for a in (m.get('arguments') or [])],env)
  returns=[];self.statement(f.get('body'),env,returns)
  self.stack.pop();return self.unique(returns)
 def statement(self,n,env,returns):
  if not n:return False
  k=n.get('nodeType')
  if k in ['Block','UncheckedBlock']:
   for s in n.get('statements',[]):
    if self.statement(s,env,returns):return True
  elif k=='VariableDeclarationStatement':
   v=self.value(n.get('initialValue'),env);decls=n['declarations']
   for i,d in enumerate(decls):
    if d:env[d['id']]=(v.get('items',[])[i] if v.get('kind')=='tuple' and i<len(v['items']) else {'kind':'tuple_item','base':v,'index':i}) if len(decls)>1 else v
  elif k=='ExpressionStatement':self.value(n['expression'],env)
  elif k=='Return':returns.append(self.value(n.get('expression'),env));return True
  elif k=='RevertStatement':return True
  elif k=='IfStatement':
   condition=self.value(n['condition'],env);self.guards.append({'condition':condition,'source':self.anchor(n['condition']),'origin':'branch'})
   if condition.get('kind')=='literal':return self.statement(n.get('trueBody') if condition['value'] else n.get('falseBody'),env,returns)
   yes=copy.deepcopy(env);no=copy.deepcopy(env)
   a=self.statement(n.get('trueBody'),yes,returns);b=self.statement(n.get('falseBody'),no,returns)
   for key in set(yes)|set(no):
    if yes.get(key)==no.get(key):env[key]=yes.get(key)
    else:env[key]={'kind':'choice','condition':condition,'alternatives':[yes.get(key,self.literal(None)),no.get(key,self.literal(None))]}
   return a and b
  elif k in ['EmitStatement','PlaceholderStatement']:pass
  else:self.unknown.append({'statement':k,'source':self.anchor(n)})
  return False

~~~~

## file-8a99a39c03a028

`source/src/pr_next_joint/frontend/source_work_budget.py` · 原字节 SHA-256 `85e9a8260a1d3a7313af1426dacc96ada6f8b2bd147d6b5cfdae098c27028134`

~~~~python
"""One finite per-entry budget and measurable normalization work."""
from contextvars import ContextVar
active=ContextVar("source_operation_work",default=None)
from pr_next_joint.reporting.effective_parameters import current
MAX_VISITS=current()["normalization_visits_per_operation_max"]
def begin():return active.set({"visits":0,"clean_calls":0,"shared_subtree_hits":0,"normalization_cache_hits":0,"max_expression_nodes":0,"max_depth":0})
def snapshot():return dict(active.get() or {})
def end(token):active.reset(token)
def metric(name,value=1,maximum=False):
    state=active.get()
    if state is not None:state[name]=max(state.get(name,0),value) if maximum else state.get(name,0)+value
def visit():
    state=active.get()
    if state is not None:
        state["visits"]+=1
        if state["visits"]>MAX_VISITS:raise ValueError("source_operation_normalization_bound_exceeded:"+str(MAX_VISITS))

~~~~
