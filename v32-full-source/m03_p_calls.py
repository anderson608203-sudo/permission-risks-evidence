"""Compiler-resolved read-only call summaries for the bounded P analyzer.

Direct construction or explicitly conditional concrete-source instance bindings.
No interface/proxy guessing, external writes, transactions, or substitution of
the outer user's identity for the callee's actual calling-contract identity.
"""
import copy,json
import re
from .source_entry_identity import function_kind,function_mutability
from .m03_p_paths import clean, key, walk, op, lit, conditions_possible


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

    def address(self):
        return {'kind':'contract_address','instance':self.instance or
                {'kind':'root_instance','contract':self.p.contract_node['id']}}

    def state(self, value, declaration):
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
        rhs=candidates[0];new=rhs.get('expression',{})
        if rhs.get('nodeType')!='FunctionCall' or new.get('nodeType')!='NewExpression':return None
        typ=new.get('typeName',{});cid=typ.get('referencedDeclaration',typ.get('pathNode',{}).get('referencedDeclaration'))
        target=self.p.nodes.get(cid,{})
        if target.get('nodeType')!='ContractDefinition' or target.get('contractKind')=='interface':return None
        return cid,new

    def destination(self, receiver):
        if receiver.get('kind')=='contract_address':
            obj=receiver['instance'];return obj.get('contract'),obj
        if receiver.get('kind')!='storage' or receiver.get('segments'):return None
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
            if len(writes)!=1 or writes[0]['id'] not in constructor_ids:return None
            instance={'kind':'source_typed_instance','parent':receiver.get('instance') or {'kind':'root_instance','contract':self.p.contract_node['id']},'reference':receiver['root'],'contract':cid}
            self.instances[key(instance)]={'instance':instance,'binding':'conditional_compiled_concrete_type','source':self.p.anchor(writes[0]),'assumption':'configured instance implements this supplied concrete contract; deployment identity not verified'}
            return cid,instance
        cid,new=found
        instance={'kind':'created_instance','parent':receiver.get('instance') or
                  {'kind':'root_instance','contract':self.p.contract_node['id']},
                  'reference':receiver['root'],'creation_ast':new['id'],'contract':cid}
        self.instances[key(instance)]={'instance':instance,'binding':'immutable_direct_new' if self.p.nodes[receiver['root']].get('mutability')=='immutable' else 'constructor_single_assignment_direct_new','source':self.p.anchor(new)}
        return cid,instance

    def implementation(self, cid, referenced):
        from .source_paths import SourcePaths
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
        from .source_library_binding import compiler_bound_receiver,storage_identity
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
            from .m10_dispatch import resolve
            target=resolve(p,target,cid)
        if external:
            receiver=p.value(expr['expression'],env)
            destination=self.destination(receiver)
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
                if typ.get('nodeType')!='ElementaryTypeName':return self.reject(node,'getter_result_not_scalar')
                result={'kind':'storage','root':declaration['id'],'segments':segments,'instance':copy.deepcopy(instance)}
                s.setdefault('read_calls',[]).append({'source':p.anchor(node),'target':p.anchor(declaration),'instance':instance,'callee_sender':sender,'arguments':clean(args),'return_value':clean(result),'binding':self.instances.get(key(instance),{}).get('binding'),'generated_getter':True})
                return result
        if external and target and function_mutability(target) not in ('view','pure'):
            from .m21_destruction import terminal_created_call
            terminal=terminal_created_call(self,node,target,cid,instance,args)
            if terminal is not None:return terminal
        if not target or function_mutability(target) not in ('view','pure'):
            return self.reject(node,'call_not_read_only_or_implementation_missing')
        params=target.get('parameters',{}).get('parameters',[])
        returns=target.get('returnParameters',{}).get('parameters',[])
        if len(params)!=len(args) or not returns:return self.reject(node,'call_arity_not_supported')
        if not external:
            from .m24_pure_reads import summarize as pure_word_summary
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
            from .source_work_budget import metric
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
        if unknown or any(x['issues'] or len(x['writes'])!=len(s['writes']) for x in complete):
            return self.reject(node,'read_call_body_unresolved')
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
            s['guards'].append(lit(False));return lit(False)
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
                from .m11_language import scalar_type
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
        item={'reason':reason,'source':self.p.anchor(node)}
        self.p.current['issues'].append(item)
        self.gaps.append(item)
        return {'kind':'unknown','reason':reason}
