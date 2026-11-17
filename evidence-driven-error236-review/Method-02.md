# 本批实际完整源码与运行器

源文件完整内容；Source ZIP保留原文件树和原字节。

## source/src/pr_next_joint/investigation/behavior.py

原文件SHA256 `3b4c29decaf2339a66866d478a6bfa3a746198981d3846c1a1507c4beb32fe8a`

```python
"""Neutral original-program probes. No risk candidate creation or legacy Binder.

Frames share initial storage and observe-call arguments. Only real change calls
modify W1. Failed continuations are negated as a whole, including arithmetic.
"""
import copy,itertools,hashlib,time
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key,op,lit,walk
from pr_next_joint.frontend.storage import selectors,keys,fields,value_type,selector_relation
from pr_next_joint.verification.program_encoding import MechanismEncoder
from pr_next_joint.verification.sequence import qualify,read
from pr_next_joint.verification.source_worlds import frame,encode_frame,serialize_world
from pr_next_joint.verification.solver import solve
from pr_next_joint.verification.expressions import Unsupported

def family(a,b):return selector_relation(a,b)=='same_shape'
def exact(a,b):return family(a,b) and key(keys(a))==key(keys(b))
def ordered_clocks(encoder,last_slot):
    """Retained transaction-world law: later real calls cannot go back in time."""
    forms=({'kind':'environment','field':'timestamp'},{'kind':'environment','field':'number'},
           {'kind':'block_timestamp'},{'kind':'block_number'})
    return [encoder.expr(qualify(value,slot))>=encoder.expr(qualify(value,slot-1))
            for slot in range(1,last_slot+1) for value in forms]
def _replace(v,mapping):
    if isinstance(v,dict):
        if key(v) in mapping:return copy.deepcopy(mapping[key(v)])
        return {k:_replace(x,mapping) for k,x in v.items()}
    return [_replace(x,mapping) for x in v] if isinstance(v,list) else v

class Backend:
    def __init__(self,program,catalog,graph):
        self.f,self.catalog,self.graph=program,catalog,graph
        self.cache={};self.cache_hits=0;self.records=[];self.formulas={};self.solve_cache={};self.math_answers={}
        self.cache_stats={'source_hits':0,'behavior_hits':0,'formula_hits':0,'computations':0};self.deadline=None
        for lookup in self.f.lookups.values():lookup.encoding_remaining=self.remaining
    def remaining(self):
        local=max(0.,self.deadline-time.monotonic()) if self.deadline is not None else self.f.options.seconds
        clock=getattr(self,'shared_remaining',None)
        return min(local,clock()) if clock else local
    def check(self):
        if self.remaining()<=0:raise TimeoutError('program_investigation_budget_exhausted')
    def cache_key(self,kind,identity):
        from .initial_state import domain
        domains={target:domain(lookup) for target,lookup in self.f.lookups.items()}
        def operation_refs(v):
            if isinstance(v,str):return [v] if v in self.f.operations else []
            if isinstance(v,dict):return [o for x in v.values() for o in operation_refs(x)]
            if isinstance(v,(list,tuple)):return [o for x in v for o in operation_refs(x)]
            return []
        semantics=getattr(self,'semantics',None)
        version=semantics.dependency_identity(operation_refs(identity)) if semantics and not kind.startswith('source') else 0
        return digest([self.f.identity,kind,identity,self.f.options.record(),domains,version,'bounded-source-semantic-properties-r1'])
    def reusable(self,action,args):
        if action=='inspect':kind,identity=('source_enhanced' if args.get('enhance') else 'source_core'),args['operation']
        elif action=='sources':kind,identity='source_dependencies',args['operation']
        elif action=='compare':kind,identity='compare',[args['change'],args['observe'],args.get('context') or {}]
        else:return False
        return self.cache_key(kind,identity) in self.cache
    def memo(self,kind,identity,compute):
        token=self.cache_key(kind,identity)
        if token in self.cache:
            self.cache_hits+=1;self.cache_stats['source_hits' if kind.startswith('source') else 'behavior_hits']+=1
            r=copy.deepcopy(self.cache[token]);r['computation_reused']=True;return r
        self.check();r=compute();self.cache_stats['computations']+=1
        if not r.get('local_errors') and not r.get('stopped_reason') and all(q.get('answer') not in ('unknown','unsupported') for q in r.get('queries',[])):
            self.cache[token]=copy.deepcopy(r)
        r['computation_reused']=False;return r
    def paths(self,oid):
        rows=[]
        for pid,p in self.f.operation_paths(oid):
            if p['flow'] not in ('normal','returned'):continue
            reduced=self.source_path(oid,pid,p)
            if not reduced.get('issues') and not reduced.get('evaluation_gaps'):
                rows.append((pid,reduced))
        return rows
    def source_path(self,oid,pid,p):
        # A verified conditional CALL summary is an original-program subcase,
        # not a replacement for an unknown callee's behavior on every input.
        cache=self.__dict__.setdefault('_source_path_cache',{})
        if pid in cache:return cache[pid]
        if not p.get('issues') and not p.get('evaluation_gaps'):
            native=self._native_no_code_subcase(oid,pid,p)
            if native is not None:cache[pid]=native;return native
            return p
        if p.get('evaluation_gaps'):return p
        audit=self.condition_dependencies(oid,pid,p)
        subcases=audit['conditional_source_subcases']
        if not subcases or audit['unknown_dependencies'] or audit['credential_dependencies']:return p
        sources={s['call_source']['ast_id'] for s in subcases}
        if any(i.get('source',{}).get('ast_id') not in sources for i in p['issues']):return p
        reasons={i['reason'] for i in p['issues']}
        q=copy.deepcopy(p)
        def discard(v):
            if isinstance(v,dict) and v.get('kind') in ('unknown','call_unresolved') and v.get('reason') in reasons:
                return lit(True)  # discarded evaluation, never a return/guard value
            if isinstance(v,dict):return {k:discard(x) for k,x in v.items()}
            return [discard(x) for x in v] if isinstance(v,list) else v
        q['evaluated_terms']=discard(q.get('evaluated_terms',[]))
        # No opaque result may remain in a guard, key, write or actual effect.
        if any(n.get('kind') in ('unknown','call_unresolved','external_return','read_call') for n in walk(
                [q['guards'],q['writes'],q.get('sensitive_effects',[])])):return p
        for s in subcases:
            q['guards'] += [op('>',s['receiver'],lit(65535)),
                            op('!=',s['receiver'],{'kind':'contract_address','instance':{'kind':'root_instance','contract':self.f.lookup(oid).contract_node['id']}})]
        q['issues']=[]
        q['source_call_subcases']=copy.deepcopy(subcases)
        cache[pid]=q
        return q

    def _native_no_code_subcase(self,oid,pid,p):
        """Exact transfer/send behavior for a selectable ordinary no-code address.

        This is an existential original-source subcase, never a universal
        guarantee about recipients. It retains insufficient-balance failure
        for send, propagating failure for transfer, and sequential payouts.
        No gas-pricing or hard-fork assumption is introduced.
        """
        payouts=[x for x in p.get('sensitive_effects',[]) if x.get('kind')=='native_transfer']
        if not payouts or p.get('issues') or p.get('evaluation_gaps'):return None
        lookup=self.f.lookup(oid);sites={x['source']['ast_id'] for x in payouts}
        calls=[c for c in self.f.call_summaries.rows.values() if c['operation']==oid and c['path']==pid]
        if any(c['source']['ast_id'] not in sites and c['mode']!='STATICCALL' for c in calls):return None
        for fx in payouts:
            node=lookup.nodes.get(fx['source']['ast_id'],{});expr=node.get('expression',{})
            if (expr.get('nodeType')!='MemberAccess' or expr.get('memberName') not in ('transfer','send') or
                    expr.get('expression',{}).get('typeDescriptions',{}).get('typeString') not in ('address','address payable') or
                    fx['recipient'].get('kind') not in ('parameter','actual_sender')):return None
        this={'kind':'contract_address','instance':{'kind':'root_instance','contract':lookup.contract_node['id']}}
        reserve=op('+',{'kind':'native_reserve','instance':this},{'kind':'transaction_value','type':'uint256'})
        mapping={};subcases=[];extra=[]
        for fx in payouts:
            paid=op('>=',reserve,fx['amount'])
            mapping[key(fx['success'])]=paid
            reserve=op('-',reserve,{'kind':'conditional','condition':paid,'when_true':fx['amount'],'when_false':lit(0)})
            extra.extend([op('>',fx['recipient'],lit(65535)),op('!=',fx['recipient'],this)])
            subcases.append({'operation':oid,'path':pid,'call_source':fx['source'],'receiver':fx['recipient'],
                'constructible_callee_runtime':'0x','native_value_transfer_supported':True,
                'success_condition':paid,'conditions':['recipient has no runtime code and is not a precompile or this contract',
                    'sufficient caller transaction gas for this recorded source path'],
                'no_callee_code_or_reentrant_side_effect_in_this_subcase':True,
                'scope':'conditional original-source subcase; not every recipient, deployment reachability or EVM execution'})
        q=_replace(p,mapping);q['guards']+=extra;q['source_call_subcases']=subcases
        q['universal_call_coverage']=False
        return q
    def source_frame(self,oid,pid,slot,before=()):
        p=self.source_path(oid,pid,self.f.paths[pid]['raw'])
        from pr_next_joint.frontend.storage import value_type
        objects=getattr(self,'active_property_objects',set())
        if objects and any(w['path']['root'] in objects for w in p['writes']):
            lookup=self.f.lookup(oid)
            observed={s['root'] for s in selectors([p['guards'],p.get('evaluated_terms',[]),p.get('sensitive_effects',[]),
                [w for w in p['writes'] if value_type(w['path'],lookup) not in ('string','bytes')]])}
            omitted=[w for w in p['writes'] if value_type(w['path'],lookup) in ('string','bytes') and
                w['path']['root'] not in observed|objects and w['value'].get('kind') in
                ('parameter','literal','fixed_bytes_literal','storage')]
            if omitted:
                p=copy.deepcopy(p);p['writes']=[w for w in p['writes'] if w not in omitted]
                p['noncritical_metadata_writes']=omitted
        fr=frame(self.f,oid,pid,slot,before,path_override=p)
        if p.get('source_call_subcases'):fr['source_call_subcases']=copy.deepcopy(p['source_call_subcases'])
        if p.get('noncritical_metadata_writes'):fr['noncritical_metadata_writes']=copy.deepcopy(p['noncritical_metadata_writes'])
        return fr
    def complete(self,oid):
        o=self.f.operations[oid]
        return bool(o['paths']) and not o['gaps'] and all(not p.get('issues') and not p.get('evaluation_gaps') and
            not p.get('bounded_read_call_limits') and not any(x.get('kind')=='native_transfer' for x in p.get('sensitive_effects',[])) and p['flow']!='truncated' and not any(
                c.get('binding')=='conditional_compiled_concrete_type' for c in p.get('read_calls',[]))
            for _,p in self.f.operation_paths(oid))
    def _query(self,e,formula,label,details=None):
        self.check()
        from .prestate import encode_state,prestate_receipt
        original_details=copy.deepcopy(details or {})
        e._initial_prefix_limit=1
        fixed,initial=encode_state(e,original_details)
        z=e.z
        def setup_solver(initial,fixed):
            details=dict(original_details,prestate=prestate_receipt(original_details,initial))
            solver=z.Solver();solver.add(z.simplify(z.And(formula,*fixed,*e.constraints,*e.domain_constraints)))
            text=solver.sexpr();h=hashlib.sha256(text.encode()).hexdigest()
            context={'program':self.f.identity,'target':e.lookup.contract['file']+':'+e.lookup.contract['name'],
                'options':self.f.options.record(),'backend':'source-relational-revision-r1','abstract_hash':e.abstract_hash_used,
                'analysis_domain':details['prestate'].get('analysis_domain'),
                'initial_model_identity':details['prestate'].get('initial_model_identity'),
                'semantic_binding_identity':original_details.get('property_identity'),
                'semantic_version':original_details.get('semantic_version',0)}
            # Reuse only the identical mathematical problem. Business
            # applicability is freshly composed under the current property.
            mathematical_context={k:v for k,v in context.items() if k not in ('semantic_binding_identity','semantic_version')}
            # Distinct path predicates can both simplify to false at deployment.
            # Their persistent exclusions and need for a writer prefix can differ.
            extension_key = None
            if isinstance(initial,dict) and not initial.get('global_reachability_exhausted'):
                extension_key = digest([z.simplify(z.And(formula,*e.constraints,*e.domain_constraints)).sexpr(),
                                    initial.get('encoded_cells'),initial.get('more_prefixes_available'),
                                        bool(original_details.get('measurement_only')),original_details.get('initial_prefix_policy')])
            token=digest([h,extension_key,mathematical_context,'risk_decision_only_v1'])
            self.formulas.setdefault(h,{'sha256':h,'scope_context_sha256':digest(context),'formula_saved':False})
            return solver,details,h,context,token
        s,details,h,context,token=setup_solver(initial,fixed)
        if token in self.solve_cache:
            self.cache_stats['formula_hits']+=1
            q=copy.deepcopy(self.solve_cache[token]);q.update(label=label,details=details,computation_reused=True)
            q['rebound_from']={'probe':q['id'],'property':self.solve_cache[token].get('details',{}).get('property_identity'),
                'to_property':details.get('property_identity'),'math_key':token,
                'binding_sha256':digest([details.get(k) for k in ('target','operation','change','observe','change_path','use_path','ledger','unit','beneficiary','holder_consent','semantic_version','property_identity')]),
                'domain':details['prestate'].get('analysis_domain')}
            q['id']='probe_'+digest([q['formula_ref'],context,label,q['details']])[:20]
            if not any(x['id']==q['id'] for x in self.records):self.records.append(q)
            return q
        def decide(solver, formula_hash):
            self.check()
            if formula_hash in self.math_answers:
                return self.math_answers[formula_hash]
            answer=solve(solver,initial_ms=min(self.f.options.solver_timeout_ms,max(1,int(self.remaining()*1000))))
            if answer in (z.sat,z.unsat):
                self.math_answers[formula_hash]=answer
            return answer
        def exclusion(context):
            from .prestate import state_facts
            invariants=[]; sources=[]
            for row in state_facts(e.lookup).values():
                if not row.get('encoded'):continue
                cell={'kind':'storage','root':row['declaration'],'segments':[]}
                previous=getattr(e,'_encoding_initial',False);e._encoding_initial=True
                try:value=e.expr(cell)
                finally:e._encoding_initial=previous
                if 'value' in row:invariants.append(value==row['value'])
                elif row.get('nonzero'):invariants.append(value!=0)
                else:continue
                sources.append(row)
            proof=z.Solver();proof.add(z.simplify(z.And(formula,*invariants,*e.constraints,*e.domain_constraints)))
            proof_text=proof.sexpr();ph=hashlib.sha256(proof_text.encode()).hexdigest()
            result=decide(proof,ph)
            self.formulas.setdefault(ph,{'sha256':ph,'scope_context_sha256':digest(context),
                'proof_method':'persistent_source_invariants_overapproximation','formula_saved':False})
            return {'answer':str(result),'formula_ref':ph,'persistent_source_facts':sources,
                'same_analysis_domain':context['analysis_domain'],'initial_model_identity':context['initial_model_identity'],
                'all_runtime_states_overapproximated':True,'excludes_only_this_formula':result==z.unsat,
                'positive_result_usable':False}
        answer=decide(s,h);stages=[];certificate=None
        if answer==z.unsat and isinstance(initial,dict) and not initial.get('global_reachability_exhausted') and not original_details.get('measurement_only'):
            certificate=exclusion(context)
            if not certificate['excludes_only_this_formula'] and initial.get('more_prefixes_available') and original_details.get('initial_prefix_policy')!='constructor_only_for_explicit_prefix':
                stages.append({'formula_ref':h,'answer':'unsat','scope':'constructor state before runtime prefixes'})
                e._initial_prefix_limit=self.f.options.max_prefixes
                fixed,initial=encode_state(e,original_details)
                s,details,h,context,token=setup_solver(initial,fixed);answer=decide(s,h)
                if answer!=z.unsat:certificate=None
        credential={'status':'not_applicable'};hash_confirmation={'status':'not_required'}
        if answer==z.sat:
            from pr_next_joint.verification.hash_confirmation import status
            hash_confirmation=status(e,s)
            credential=e.credential_status(s)
            if credential['status']=='unverified':
                restricted=e.invalid_recovery_subdomain(s)
                if restricted is not None:
                    sub_identity=hashlib.sha256(restricted.sexpr().encode()).hexdigest()
                    sub_answer=decide(restricted,sub_identity)
                    sub_hash=status(e,restricted)
                    credential=dict(credential,exact_invalid_subdomain_answer=str(sub_answer),
                        exact_invalid_subdomain_sha256=sub_identity,subset_failure_does_not_refute_property=True)
                    if sub_answer==z.sat and sub_hash['status']=='not_required':
                        credential.update(status='verified_invalid_domain',
                            reason='exact_invalid_recovery_domain_without_assignments')
                        hash_confirmation=sub_hash
                        details=dict(details,credential_subdomain='exact_invalid_recovery_domain')
        valid=(answer==z.sat and credential['status'] in ('not_required','verified_invalid_domain') and
               hash_confirmation['status']=='not_required')
        q={'label':label,'answer':str(answer),'formula_ref':h,'formula_sha256':h,
           'credential':credential,'abstract_hash':e.abstract_hash_used,'hash_confirmation':hash_confirmation,
           'bounded_condition_confirmed':valid,
           'evidence_kind':'bounded_condition_check_without_assignment_extraction',
           'scope':'original-source bounded symbolic condition; not concrete execution or deployment reachability',
           'details':details,'initial_stage_search':stages}
        q['id']='probe_'+digest([h,context,label,details])[:20]
        if certificate:q['exclusion_certificate']=certificate
        if str(answer) in ('sat','unsat') and credential.get('status')!='unverified' and hash_confirmation.get('status') in ('not_required','verified'):
            self.solve_cache[token]=copy.deepcopy(q)
        if not any(x['id']==q['id'] for x in self.records):self.records.append(q)
        return q
    def _storage_name(self,oid,s):
        lookup=self.f.lookup(oid);parts=[lookup.nodes.get(s['root'],{}).get('name',str(s['root']))]
        for seg in s.get('segments',[]):
            if 'field' in seg:parts.append('.'+lookup.nodes.get(seg['field'],{}).get('name',str(seg['field'])))
            elif 'key' in seg:
                def display(v):
                    if v.get('kind')=='actual_sender':return 'msg.sender'
                    if v.get('kind')=='contract_address':return 'this'
                    if v.get('kind')=='parameter':return lookup.nodes.get(v['id'],{}).get('name','request argument')
                    if v.get('kind')=='literal':return str(v['value'])
                    if v.get('kind')=='op':return '('+(' '+v['op']+' ').join(display(a) for a in v['args'])+')'
                    return 'source-bound key'
                parts.append('['+display(seg['key'])+']')
            elif seg.get('length'):parts.append('.length')
        return ''.join(parts)
    def _holder(self,oid,s):
        from .summary import holder
        return holder(s,self.f.lookup(oid))
    def _native_unit_source(self,oid,s):
        """Exact source quantity provenance only; no name-based asset classification."""
        found=[]
        for w in self.f.writes.values():
            if self.f.operations[w['operation']]['target']!=self.f.operations[oid]['target'] or not family(w['raw']['path'],s):continue
            v=w['raw']['value'];p=w['raw']['path']
            one=(v.get('kind')=='transaction_value' or v.get('kind')=='op' and v.get('op')=='+' and
                 any(a.get('kind')=='transaction_value' for a in v['args']) and any(key(a)==key(p) for a in v['args']))
            if one:found.append({'operation':w['operation'],'source':w['raw']['source'],'quantity_origin':'one native value unit per stored unit'})
        return found
    def inspect(self,oid,enhance=True):
        return self.memo('source_enhanced' if enhance else 'source_core',oid,
                         lambda:self._inspect(oid) if enhance else self._source_core(oid))
    def _ignored_call_subcase(self,oid,pid,p,bindings,origin):
        """An explicit no-code, zero-value source subcase, not a CALL emulator.

        Only an original standalone bare CALL with an unconstrained address
        parameter qualifies. The discarded result is not set to true. Unknown
        typed calls, return guards, effectful arguments and other dependencies
        remain opaque. No business interpretation is generated here.
        """
        if not origin.startswith('executed_evaluation') or len(bindings)!=1:return None
        lookup=self.f.lookup(oid);site=bindings[0].get('source',{});node=lookup.nodes.get(site.get('ast_id'),{})
        expr=node.get('expression',{});receiver=expr.get('expression',{})
        if node.get('nodeType')!='FunctionCall' or expr.get('nodeType')!='MemberAccess':return None
        declaration=lookup.nodes.get(expr.get('referencedDeclaration'),{})
        typed_void=(declaration.get('nodeType')=='FunctionDefinition' and
                    not declaration.get('returnParameters',{}).get('parameters',[]))
        bare=(expr.get('memberName')=='call' and expr.get('typeDescriptions',{}).get('typeIdentifier','').startswith('t_function_barecall_'))
        if not (bare or typed_void):return None
        if receiver.get('nodeType')!='Identifier':return None
        if not any(n.get('nodeType')=='ExpressionStatement' and n.get('expression',{}).get('id')==node['id'] for n in lookup.nodes.values()):return None
        entry=lookup.function(self.f.operations[oid]['function']);params=entry.get('parameters',{}).get('parameters',[])
        rid=receiver.get('referencedDeclaration')
        if rid not in {x['id'] for x in params}:return None
        # Do not assume a no-code witness if original conditions restrict the
        # receiver (for example receiver==this or an extcodesize test).
        if any(n.get('kind')=='parameter' and n.get('id')==rid for n in walk(p['guards'])):return None
        from pr_next_joint.frontend.source_entry_identity import builtin_call
        def pure_arg(n):
            if n.get('nodeType')=='Literal':return True
            if n.get('nodeType')=='Identifier':return n.get('referencedDeclaration') in {x['id'] for x in params}
            return (n.get('nodeType')=='FunctionCall' and
                (n.get('kind')=='typeConversion' and n.get('expression',{}).get('nodeType')=='ElementaryTypeNameExpression'
                 or builtin_call(n,lookup,('keccak256','sha3'))) and all(pure_arg(x) for x in n.get('arguments',[])))
        if not all(pure_arg(a) for a in node.get('arguments',[])):return None
        # This subcase supports original local state effects, never an
        # assertion that the no-code destination performed an asset transfer.
        prefix_writes=[w for w in p['writes'] if w.get('source',{}).get('file')==site.get('file') and
            w['source']['start']+w['source']['length']<=site.get('start',-1) and
            not any(n.get('kind') in ('unknown','call_unresolved','external_return','read_call') for n in walk([w['path'],w['value']]))]
        if not prefix_writes:return None
        return {'supported_local_prefix_writes':copy.deepcopy(prefix_writes),
            'external_transfer_or_compensation_not_established':True,
            'path':pid,'operation':oid,'call_source':site,'receiver':{'kind':'parameter','id':rid,'type':receiver['typeDescriptions']['typeString']},
            'source_semantics':('standalone typed zero-value CALL with no return values; caller selects a compatible contract that commits without callbacks'
                if typed_void else 'standalone bare CALL; no native value option; discarded return does not control continuation'),
            'constructible_callee_runtime':'0x00' if typed_void else '0x',
            'callee_runtime_semantics':'STOP returns empty bytes successfully, without storage changes or callbacks; compatible with a void-return ABI' if typed_void else 'no-code account',
            'conditions':['destination has the recorded compatible runtime and is not a precompile or this contract',
                          'transaction has sufficient gas for the displayed straight-line continuation'],
            'preserved_guards':copy.deepcopy(p['guards']),'discarded_result_not_assigned_a_favorable_boolean':True,
            'no_callee_code_or_reentrant_side_effect_in_this_subcase':True,
            'scope':'conditional original-source prediction only; not arbitrary destinations, EVM execution or universal call success'}
    def condition_dependencies(self,oid,pid,p):
        # This audit depends only on the frozen original source path and its
        # compiler binding, not on a model interpretation, state or query frame.
        # paths()/unit discovery used to repeat this same traversal thousands
        # of times before any investigation could run. Cache only paths owned
        # by this Backend's immutable Facts (or its frozen source subcase).
        owned = (self.f.paths.get(pid,{}).get('raw') is p or
                 self.__dict__.get('_source_path_cache',{}).get(pid) is p)
        if not owned:
            return self._condition_dependencies(oid,pid,p)
        cache = self.__dict__.setdefault('_source_condition_audit_cache',{})
        token = (oid,pid,id(p))
        if token in cache:
            self.cache_stats['source_condition_audit_hits'] = self.cache_stats.get('source_condition_audit_hits',0)+1
            return cache[token][1]
        result = self._condition_dependencies(oid,pid,p)
        # Keep the source object alive as well: an unrelated temporary object
        # can neither reuse its identity nor be mistaken for this source path.
        cache[token] = (p,result)
        self.cache_stats['source_condition_audit_computations'] = self.cache_stats.get('source_condition_audit_computations',0)+1
        return result
    def _condition_dependencies(self,oid,pid,p):
        """Actual ordered evaluation dependencies, not all syntactic children.

        Existing frontend retains conditional evaluation guards even when a
        return is simplified away. Never infer a useful value for an unknown.
        """
        from pr_next_joint.frontend.path_ir import conditions_possible
        unknown=[];credentials=[];skipped=[];subcases=[];lookup=self.f.lookup(oid)
        opaque={'unknown','call_unresolved','external_return','read_call','address_has_runtime_code'}
        # Only established non-opaque source facts can eliminate a call's
        # execution branch. An unknown guard cannot certify itself harmless.
        facts=[g for g in p['guards'] if not any(n.get('kind') in opaque|{'credential_recovery'} for n in walk(g))]
        excluded_cache={}
        def impossible(g):
            if g==lit(True):return False
            if g==lit(False):return True
            try:
                token=key(g)
                if token not in excluded_cache:excluded_cache[token]=not conditions_possible(facts+[g])
                return excluded_cache[token]
            except (ValueError,KeyError,TypeError):return False
        def binding(value):
            origins=[x for x in p.get('issues',[]) if x.get('reason')==value.get('reason') and isinstance(x.get('source'),dict)]
            calls=[]
            for origin in origins:
                n=lookup.nodes.get(origin['source'].get('ast_id'),{});expr=n.get('expression',{})
                ref=expr.get('referencedDeclaration');target=lookup.nodes.get(ref,{})
                local=(expr.get('nodeType')=='Identifier' and target.get('nodeType')=='FunctionDefinition')
                calls.append({'source':origin['source'],'declaration':ref,'binding':'compiler_bound_local_helper' if local else 'external_or_unresolved_call',
                              'return_and_success_effects_not_established':True})
            return calls
        def visit(value,gate,origin):
            if isinstance(value,list):
                for x in value:visit(x,gate,origin)
                return
            if not isinstance(value,dict):return
            if impossible(gate):
                skipped.append({'origin':origin,'execution_condition':gate,'basis':'source path facts exclude evaluation; no unknown return chosen'});return
            kind=value.get('kind')
            if kind in opaque or kind=='credential_recovery':
                row={'path':pid,'operation':oid,'origin':origin,'execution_condition':gate,'term':copy.deepcopy(value),
                     'call_binding':binding(value)}
                subcase=self._ignored_call_subcase(oid,pid,p,row['call_binding'],origin) if kind in ('unknown','call_unresolved') else None
                if subcase:
                    subcases.append(subcase)
                    skipped.append({'origin':origin,'execution_condition':gate,'basis':'call is executed, but its discarded result is not a critical success guard in the explicit no-code zero-value subcase',
                                    'not_an_unexecuted_short_circuit_branch':True,'source_subcase':subcase})
                else:(credentials if kind=='credential_recovery' else unknown).append(row)
                return
            if kind=='guarded_evaluation':
                condition=value['condition'];visit(condition,gate,origin+':evaluation_gate')
                visit(value.get('input',value.get('values',[])),op('and',gate,condition),origin+':conditional_evaluation');return
            if kind in ('conditional','choice') and isinstance(value.get('condition'),dict):
                c=value['condition'];visit(c,gate,origin+':condition')
                yes=value.get('when_true',(value.get('alternatives') or [None,None])[0])
                no=value.get('when_false',(value.get('alternatives') or [None,None])[1])
                visit(yes,op('and',gate,c),origin+':true_branch');visit(no,op('and',gate,op('!',c)),origin+':false_branch');return
            if kind=='op' and value.get('op') in ('and','&&','or','||'):
                prefix=gate
                for term in value['args']:
                    visit(term,prefix,origin+':ordered_boolean')
                    prefix=op('and',prefix,term if value['op'] in ('and','&&') else op('!',term))
                return
            for k,x in value.items():
                if isinstance(x,(dict,list)):visit(x,gate,origin+':'+k)
        if p['flow'] in ('normal','returned'):
            visit(p['guards'],lit(True),'guard')
            visit(p.get('evaluated_terms',[]),lit(True),'executed_evaluation')
        return {'path':pid,'operation':oid,'flow':p['flow'],'unknown_dependencies':unknown,
                'credential_dependencies':credentials,'skipped_evaluations':skipped,'conditional_source_subcases':subcases,
                'successful_local_read_summaries':copy.deepcopy(p.get('read_calls',[])),
                'scope':'this original path and entry only; unrelated success cannot discharge it'}
    def _source_core(self,oid):
        """Bounded cheap expression/AST facts, no solver.check or batch probing."""
        self.check();f=self.f;o=f.operations[oid];lookup=f.lookup(oid)
        out={'kind':'source_inspection','operation':oid,'anchor':self.catalog.name(oid),'source_card':self.catalog.card(oid),
          'actual_guards':[{'path':pid,'guards':p['guards'],'flow':p['flow']} for pid,p in f.operation_paths(oid)],
          'writes':[w['raw'] for w in f.writes.values() if w['operation']==oid],
          'effects':[w['raw'] for w in f.effects.values() if w['operation']==oid],
          'source_gaps':copy.deepcopy(o['gaps']),'complete_for_bounded_paths':self.complete(oid),
          'local_errors':[],'path_commit_queries':[],'queries':[],'settlements':[],'debit_objects':[],
          'no_committing_path':False,'net_effect_proved_unchanged':False,
          'unknown_guard_paths':[],'credential_paths':[],'credential_success_verified':False,
          'verified_success_paths':[],'condition_dependency_audit':[],
          'cheap_core_source_check':True,'solver_invocations':0,'business_policy_not_inferred_from_guard':True}
        feasible=[];unchanged=[]
        for pid,p in f.operation_paths(oid):
            self.check()
            audit=self.condition_dependencies(oid,pid,p);out['condition_dependency_audit'].append(audit)
            if audit['unknown_dependencies']:out['unknown_guard_paths'].append(pid)
            if audit['credential_dependencies']:out['credential_paths'].append(pid)
            if p['flow'] not in ('normal','returned'):continue
            try:
                e=MechanismEncoder(lookup);z=e.z;fr=frame(f,oid,pid,0)
                success=z.simplify(z.And(encode_frame(e,fr),e.expr(fr['caller'])!=0,*e.domain_constraints))
                feasible.append(not z.is_false(success))
                if z.is_false(success):continue
                delta=[]
                for s in {key(w['path']):w['path'] for w in p['writes']}.values():
                    pre=e.expr(read(qualify(s,0),[],lookup));post=e.expr(read(qualify(s,0),fr['writes'],lookup));delta.append(z.simplify(pre!=post))
                    if value_type(s,lookup) not in ('uint','uint256'):continue
                    debit=z.simplify(pre-post)
                    if z.is_true(z.simplify(debit==0)):continue
                    holder=self._holder(oid,s);units=self._native_unit_source(oid,s)
                    out['debit_objects'].append({'path':pid,'object':s,'holder':holder,'unit_source':units,'answer':'source_quantity_change','debit_query':None})
                    if holder is None or not units:continue
                    h=e.expr(read(qualify(holder,0),[],lookup))
                    def conjuncts(g):
                        return [v for a in g['args'] for v in conjuncts(a)] if g.get('op') in ('and','&&') else [g]
                    required={key(g) for guard in fr['guards'] for g in conjuncts(guard)}
                    payments=[z.If(z.And(e.expr(fx['recipient'])==h,
                        z.BoolVal(True) if key(fx.get('success',lit(True))) in required else e.expr(fx.get('success',lit(True)))),
                        e.expr(fx['amount']),z.IntVal(0)) for fx in fr['effects'] if fx['kind']=='native_transfer']
                    if payments:out['settlements'].append({'path':pid,'object':s,'holder':holder,'unit_source':units,
                      'same_holder_and_unit_full_settlement':z.is_true(z.simplify(z.Sum(*payments)==debit)),
                      'method':'exact source expression identity, not new execution','counterexample_query':None,'debit_query':None})
                unchanged.append(bool(delta) and not fr['effects'] and all(z.is_false(x) for x in delta))
            except TimeoutError:raise
            except Exception as error:
                feasible.append(True);unchanged.append(False);out['local_errors'].append({'path':pid,'reason':type(error).__name__+':'+str(error)})
        complete=self.complete(oid) and not out['local_errors']
        out['no_committing_path']=complete and not any(feasible)
        out['net_effect_proved_unchanged']=complete and bool(unchanged) and all(unchanged)
        # Constant recovery failure may simplify all successful paths away;
        # symbolic credentials still require the existing exact witness check.
        out['credential_success_verified']=False
        return out
    def _inspect(self,oid):
        f=self.f;o=f.operations[oid];lookup=f.lookup(oid);queries=[];committing=[];critical=[];settlements=[];net=[];debit_objects=[]
        for pid,p in self.paths(oid):
            self.check()
            try:
                e=MechanismEncoder(lookup);z=e.z;fr=frame(f,oid,pid,0);success=z.And(encode_frame(e,fr),e.expr(fr['caller'])!=0)
                q=self._query(e,success,'original_path_commit',{'operation':oid,'path':pid});queries.append(q);committing.append(q)
                if q['answer']!='sat':continue
                changes=[]
                for s in {key(w['path']):w['path'] for w in fr['writes']}.values():
                    before=qualify(s,0);before=read(before,[],lookup);after=read(qualify(s,0),fr['writes'],lookup)
                    changes.append(e.expr(before)!=e.expr(after))
                if changes and not fr['effects']:
                    n=self._query(e,z.And(success,z.Or(*changes)),'net_state_change',{'operation':oid,'path':pid});queries.append(n);net.append(n)
                for raw in p['writes']:
                    s=raw['path'];typ=value_type(s,lookup)
                    if typ not in ('uint','uint256'):continue
                    pre=e.expr(read(qualify(s,0),[],lookup));post=e.expr(read(qualify(s,0),fr['writes'],lookup));debit=pre-post
                    debit_q=self._query(e,z.And(success,debit>0),'source_quantity_debit',{'operation':oid,'path':pid,'object':s});queries.append(debit_q)
                    holder=self._holder(oid,s);units=self._native_unit_source(oid,s)
                    if debit_q['answer']!='unsat':debit_objects.append({'path':pid,'object':s,'object_name':self._storage_name(oid,s),
                        'holder':holder,'unit_source':units,'answer':debit_q['answer'],'debit_query':debit_q['id']})
                    if holder is None or not units:continue
                    h=e.expr(read(qualify(holder,0),[],lookup))
                    payments=[z.If(z.And(e.expr(fx['recipient'])==h,e.expr(fx.get('success',lit(True)))),
                        e.expr(fx['amount']),z.IntVal(0)) for fx in fr['effects'] if fx['kind']=='native_transfer']
                    if not payments:continue
                    paid=z.Sum(*payments)
                    q=self._query(e,z.And(success,debit>0,z.Not(paid==debit)),'same_holder_native_settlement_counterexample',{'operation':oid,'path':pid,'object':s});queries.append(q)
                    feasible=self._query(e,z.And(success,debit>0),'actual_debit_exists',{'operation':oid,'path':pid,'object':s});queries.append(feasible)
                    settlements.append({'path':pid,'object':s,'object_name':self._storage_name(oid,s),'holder':holder,
                        'unit_source':units,'same_holder_and_unit_full_settlement':q['answer']=='unsat' and feasible['bounded_condition_confirmed'],
                        'counterexample_query':q['id'],'debit_query':feasible['id']})
            except TimeoutError:raise
            except Exception as error:critical.append({'path':pid,'reason':type(error).__name__+':'+str(error)})
        # Unknown guards are decisive to path feasibility; unrelated events are not.
        unknown_guard_paths=[];credential_paths=[];audits=[]
        for pid,p in f.operation_paths(oid):
            audit=self.condition_dependencies(oid,pid,p);audits.append(audit)
            if audit['unknown_dependencies']:unknown_guard_paths.append(pid)
            if audit['credential_dependencies']:credential_paths.append(pid)
        return {'kind':'source_inspection','operation':oid,'anchor':self.catalog.name(oid),'source_card':self.catalog.card(oid),
            'actual_guards':[{'path':pid,'guards':p['guards'],'flow':p['flow']} for pid,p in f.operation_paths(oid)],
            'writes':[w['raw'] for w in f.writes.values() if w['operation']==oid],
            'effects':[w['raw'] for w in f.effects.values() if w['operation']==oid],
            'source_gaps':copy.deepcopy(o['gaps']),'complete_for_bounded_paths':self.complete(oid),'local_errors':critical,
            'path_commit_queries':[q['id'] for q in committing],
            'no_committing_path':self.complete(oid) and not critical and not any(q['answer']!='unsat' for q in committing),
            'net_effect_proved_unchanged':bool(net) and len(net)==len([q for q in committing if q['answer']=='sat']) and
                self.complete(oid) and not critical and all(q['answer']=='unsat' for q in net),
            'unknown_guard_paths':unknown_guard_paths,'credential_paths':credential_paths,
            'credential_success_verified':any(q['bounded_condition_confirmed'] for q in committing),
            'verified_success_paths':[q['details']['path'] for q in committing if q['bounded_condition_confirmed'] and q['details'].get('operation')==oid],
            'condition_dependency_audit':audits,
            'settlements':settlements,'debit_objects':debit_objects,'queries':queries,
            'business_policy_not_inferred_from_guard':True}
    def sources(self,oid):
        return self.memo('source_dependencies',oid,lambda:self._sources(oid))
    def _sources(self,oid):
        target=self.f.operations[oid]['target'];guards=[s for _,p in self.f.operation_paths(oid) for s in selectors(p['guards'])]
        used=[s for _,p in self.f.operation_paths(oid) for s in selectors([p['guards'],p['writes']])]
        writers=self.graph.writers(target,used,'semantic investigation: actual state sources')
        return {'kind':'state_sources','operation':oid,'guard_selectors':guards,'used_selectors':used,'writers':writers,
                'writer_cards':[self.catalog.card(i) for i in writers],
                'same_full_key_not_yet_established':True,'ready_pairs':[{'change':i,'observe':oid} for i in writers if i!=oid]}
    def seed(self,oid):
        """A declared-initial exploration seed, never a universal live-state premise."""
        lookup=self.f.lookup(oid);result=[]
        constructors=[n for n in lookup.nodes.values() if n.get('nodeType')=='FunctionDefinition' and n.get('kind')=='constructor']
        for node in lookup.nodes.values():
            if not node.get('stateVariable') or node.get('typeDescriptions',{}).get('typeString')!='bool':continue
            # Omit any field assigned by constructor: no guessed constructor execution.
            if any(n.get('nodeType')=='Identifier' and n.get('referencedDeclaration')==node['id'] for c in constructors for n in walk(c.get('body',{}))):continue
            val=node.get('value');constant=False if val is None else (val.get('value')=='true' if val.get('kind')=='bool' else None)
            if constant is not None:result.append({'path':{'kind':'storage','root':node['id'],'segments':[]},'value':lit(constant)})
        existing={key(x['path']) for x in result}
        for _,p in self.f.operation_paths(oid):
            for s in selectors(p['guards']):
                if key(s) in existing or value_type(s,lookup)!='bool':continue
                if not keys(s):continue
                if any(n.get('nodeType')=='Identifier' and n.get('referencedDeclaration')==s['root'] for c in constructors for n in walk(c.get('body',{}))):continue
                result.append({'path':copy.deepcopy(s),'value':lit(False)});existing.add(key(s))
        return result
    def reach(self,oid,prefix=(),*,version=0,plan=None,goal=None):
        from .initial_state import initial_for_lookup,domain
        identity=[oid,list(prefix),plan or {},goal or {},domain(self.f.lookup(oid)),initial_for_lookup(self.f.lookup(oid))['identity']]
        return self.memo('reach',identity,lambda:self._reach(oid,prefix,plan or {},goal or {}))
    def _frame_bindings(self,e,frames,plan):
        terms=[]
        for binding in plan.get('bindings',[]):
            index=binding['frame']
            if type(index)is not int or not 0<=index<len(frames):raise Unsupported('prefix_binding_frame_outside_plan')
            fr=frames[index]
            if binding.get('parameter') is not None:
                params=self.f.operations[fr['operation']]['parameters']
                found=[self.f.terms[p['term']]['expression'] for p in params if p['name']==binding['parameter']]
                if len(found)!=1:raise Unsupported('prefix_parameter_binding_not_unique')
                left=qualify(found[0],fr['slot'])
            else:left=fr['caller']
            right=binding.get('value')
            if 'equals_frame' in binding:
                other=binding['equals_frame']
                if type(other)is not int or not 0<=other<len(frames):raise Unsupported('prefix_related_frame_outside_plan')
                right=frames[other]['caller']
            if not isinstance(right,dict):raise Unsupported('prefix_binding_requires_typed_source_term')
            terms.append(e.expr(left)==e.expr(right))
        return terms
    def _goal_terms(self,e,fr,goal):
        from .ledger import flow
        from .summary import get_summaries,unique
        category=goal.get('category');predicates=[];values={}
        if goal.get('measure')=='productive_request':
            from .blocking import productive
            use, objects = productive(self,e,fr,fr['operation'])
            return [use], values
        if goal.get('measure')!='positive_effect':return [],values
        positions=goal.get('positions') or get_summaries(self.f).positions(fr['operation'])
        for cell in positions:
            h,start,end,_,_=flow(e,e.lookup,fr,cell);actor=e.expr(fr['caller'])
            from .relations import beneficiary_condition
            controlled, control_basis = beneficiary_condition(e, fr, cell, h)
            condition=e.z.And(end>start,controlled) if category=='FCR-MINT' else e.z.And(end<start,h!=actor,h!=0)
            predicates.append(condition);values.update(holder=h,before=start,after=end,caller=actor)
        if not predicates:raise Unsupported('positive_effect_goal_has_no_bound_numeric_position')
        return [e.z.Or(*predicates)],values
    def _reach(self,oid,prefix=(),plan=None,goal=None):
        f=self.f;lookup=f.lookup(oid);queries=[];worlds=[]
        plan=plan or {};goal=goal or {}
        progress=self.__dict__.setdefault('_reach_progress',{})
        progress_key=self.cache_key('reach_progress',[oid,list(prefix),plan,goal])
        saved=progress.get(progress_key,{})
        queries=list(saved.get('queries',[]));worlds=list(saved.get('worlds',[]))
        completed=saved.get('completed',0);job_index=0
        if any(f.operations[p]['target']!=f.operations[oid]['target'] for p in prefix):
            return {'kind':'reachability','operation':oid,'prefix':list(prefix),'queries':[],'worlds':[],
                    'reached':False,'local_errors':[{'reason':'prefix_cross_target_not_supported'}]}
        choices=[self.paths(x) for x in prefix]
        for selected in itertools.islice(itertools.product(*choices),f.options.max_prefixes):
            for pid,_ in self.paths(oid):
                job_index+=1
                if job_index<=completed:continue
                try:
                    self.check()
                    if goal.get('require_privileged'):
                        from .roles import path_qualification
                        # A structural prerequisite does not depend on the
                        # chosen prefix. Check it before expanding financial
                        # expressions, especially array/loop write chains.
                        if not path_qualification(f,oid,f.paths[pid]['raw']):continue
                    unresolved=[]
                    for po,(pp,path) in zip(prefix,selected):
                        deps=self.condition_dependencies(po,pp,path)
                        if deps['unknown_dependencies']:unresolved.append({'operation':po,'path':pp,'dependencies':deps['unknown_dependencies']})
                    deps=self.condition_dependencies(oid,pid,f.paths[pid]['raw'])
                    if deps['unknown_dependencies']:unresolved.append({'operation':oid,'path':pid,'dependencies':deps['unknown_dependencies']})
                    if unresolved:
                        queries.append({'answer':'unsupported','reason':'critical_unknown_in_explicit_prefix_or_target','dependencies':unresolved})
                        continue
                    e=MechanismEncoder(lookup);z=e.z;writes=[];premises=[];frames=[]
                    for slot,(po,(pp,_)) in enumerate(zip(prefix,selected)):
                        fr=self.source_frame(po,pp,slot,writes);premises.append(encode_frame(e,fr));writes+=fr['writes'];frames.append(fr)
                    fr=self.source_frame(oid,pid,len(prefix),writes);premises.append(encode_frame(e,fr))
                    premises+=ordered_clocks(e,len(prefix))
                    premises.extend(e.expr(x['caller'])!=0 for x in frames+[fr])
                    premises+=self._frame_bindings(e,frames+[fr],plan)
                    extra,observed=self._goal_terms(e,fr,goal);premises+=extra
                    q=self._query(e,z.And(*premises),'prefix_reachability',{'operation':oid,'prefix':list(prefix),'path':pid,
                        'per_frame_plan':plan,'target_property':goal,'initial_prefix_policy':'constructor_only_for_explicit_prefix'})
                    queries.append(q);worlds.append({'prefix':[serialize_world(x,'PREFIX') for x in frames],'target':serialize_world(fr,'TARGET'),
                        'bindings':plan,'goal':goal,'query':q['id'],'committed':q['bounded_condition_confirmed'],
                        'prefix_frames':copy.deepcopy(frames),'target_frame':copy.deepcopy(fr)})
                    if goal.get('measure')=='productive_request' and q['bounded_condition_confirmed']:
                        # The blocking consumer needs one *actual* productive
                        # baseline state. It separately checks every relevant
                        # post-intervention continuation. Enumerating all
                        # baseline paths before handing over this state only
                        # delays that necessary universal check.
                        progress.pop(progress_key,None)
                        return {'kind':'reachability','operation':oid,'prefix':list(prefix),'queries':queries,'worlds':worlds,
                            'reached':True,'goal':goal,'frame_plan':plan,'stopped_on_productive_target':True,
                            'all_target_paths_exhausted':False,'negative_conclusion_allowed':False,
                            'initial_state':'same frozen host domain, no legacy seed override','same_requester_scenario':False}
                except TimeoutError as error:
                    # Preserve completed source frames at a fair action
                    # boundary. Resume the incomplete frame under the same
                    # typed/domain identity; never treat the frontier as UNSAT.
                    progress[progress_key]={'completed':job_index-1,'queries':queries,'worlds':worlds}
                    return {'kind':'reachability','operation':oid,'prefix':list(prefix),'queries':queries,'worlds':worlds,
                        'reached':any(q.get('bounded_condition_confirmed') for q in queries),'goal':goal,'frame_plan':plan,
                        'stopped_reason':'action_slice_exhausted','local_errors':[{'reason':str(error),'path':pid}],
                        'completed_source_frames':job_index-1,'next_source_frame':job_index,
                        'negative_conclusion_allowed':False}
                except Exception as error:queries.append({'answer':'unsupported','reason':type(error).__name__+':'+str(error)})
        progress.pop(progress_key,None)
        return {'kind':'reachability','operation':oid,'prefix':list(prefix),'queries':queries,'worlds':worlds,
                'reached':any(q.get('bounded_condition_confirmed') for q in queries),
            'initial_state':'same frozen host domain, no legacy seed override','same_requester_scenario':False,
            'goal':goal,'frame_plan':plan}
    def prefix_search(self,oid,*,version=0,interpretation_identity=None,plan=None,goal=None):
        from .goal_search import search
        return search(self,oid,goal=goal,plan=plan,
                      stop_on_first=(goal or {}).get('measure')!='positive_effect')
    def _paired(self,change,observe,cpid,prefix=(),prefix_paths=(),caller_mode=None,context=None):
        self.check();context=context or {}
        f=self.f;lookup=f.lookup(observe);e=MechanismEncoder(lookup);z=e.z;writes=[];premises=[];frames=[]
        for slot,(oid,pid) in enumerate(zip(prefix,prefix_paths)):
            fr=frame(f,oid,pid,slot,writes);premises.append(encode_frame(e,fr));writes+=fr['writes'];frames.append(fr)
        cslot=len(prefix);uslot=cslot+1;changefr=frame(f,change,cpid,cslot,writes)
        changeok=encode_frame(e,changefr)
        if cpid in context.get('observable',{}).get('qualified_writer_paths',[]):
            from .roles import path_qualification, fixed_role_terms
            role_terms,_=fixed_role_terms(e,path_qualification(f,change,f.paths[cpid]['raw']),cslot)
            changeok=z.And(changeok,*role_terms)
        before=[];after=[];beforeframes=[];afterframes=[]
        for pid,_ in self.paths(observe):
            self.check()
            a=frame(f,observe,pid,uslot,writes);b=frame(f,observe,pid,uslot,writes+changefr['writes'])
            before.append(encode_frame(e,a));after.append(encode_frame(e,b));beforeframes.append(a);afterframes.append(b)
        c=e.expr(changefr['caller']);u=e.expr(qualify({'kind':'actual_sender'},uslot))
        caller_mode=caller_mode or ('same_requester' if f.options.scope=='AC' else 'independent_actors')
        scenario=([c==u] if caller_mode=='same_requester' else [])+[c!=0,u!=0]
        # A single unequivocal source role is an observation reference, not business policy.
        rolecells={key(s):s for _,p in f.operation_paths(observe) for s in selectors(p['guards'])
                   if not keys(s) and value_type(s,lookup) in ('address','address payable')}
        if context.get('exclude_preexisting_authority') and len(rolecells)==1:
            role=next(iter(rolecells.values()));scenario.append(c!=e.expr(read(role,writes,lookup)))
        quantities={key(w['value']['args'][1]):w['value']['args'][1] for _,p in self.paths(observe) for w in p['writes']
                    if w['value'].get('kind')=='op' and w['value'].get('op')=='-' and key(w['value']['args'][0])==key(w['path'])}
        if f.options.scope=='FCR' and len(quantities)==1:
            scenario.append(e.expr(qualify(next(iter(quantities.values())),uslot))>0)
        scenario+=ordered_clocks(e,uslot)
        # Only source-bound request inputs are admitted, not arbitrary model SMT.
        for binding in context.get('bindings',[]):
            scenario.append(e.expr(qualify(binding['parameter'],uslot))==e.expr(binding['value']))
        from .ledger import scenario_terms
        scenario+=scenario_terms(e,lookup,context.get('encoded_case',[]),writes,writes+changefr['writes'],uslot)
        ok0,ok1=z.Or(*before),z.Or(*after)
        use0,use1=ok0,ok1
        if context.get('observable',{}).get('hold_other_request_cells'):
            use0=z.Or(*[self._holder_commit(e,fr,observe,uslot,context) for fr in beforeframes])
            use1=z.Or(*[self._holder_commit(e,fr,observe,uslot,context) for fr in afterframes])
        return e,z.And(*premises,changeok,*scenario),ok0,ok1,use0,use1,{
          'prefix':[serialize_world(x,'COMMON_PREFIX') for x in frames],
          'change':serialize_world(changefr,'INTERVENTION'),
          'before':[serialize_world(x,'W0') for x in beforeframes],'after':[serialize_world(x,'W1') for x in afterframes],
          'invariants':'same initial storage, observe caller/arguments/environment and target; change call is the sole intervention',
          'caller_scenario':caller_mode,'same_requester_pre_role_inequality_applied':caller_mode=='same_requester' and len(rolecells)==1,
          'positive_financial_request_quantity_applied':f.options.scope=='FCR' and len(quantities)==1,
          'financial_use_witness':context.get('observable',{}).get('holder_delta'),
          'availability_polarity':'same productive request before and after; every applicable productive continuation excluded',
          'environment':'same observe environment across W0/W1; timestamps/block numbers nondecreasing on each real prefix/change/observe sequence',
          'role_reference_cells':list(rolecells.values()),'business_qualification_still_semantic':True},changefr,afterframes
    def compare(self,change,observe,*,version=0,context=None):
        context=context or {}
        # Semantic wording, qid and revision counters do not change programs.
        return self.memo('compare',[change,observe,context],lambda:self._compare(change,observe,context))
    def net_unit(self,oid,obj):
        """Use native units only when this storage family has consistent source provenance."""
        if value_type(obj,self.f.lookup(oid)) not in ('uint','uint256') or self._holder(oid,obj) is None:
            return []
        origins=self._native_unit_source(oid,obj)
        if not origins:
            return []
        for w in self.f.writes.values():
            if self.f.operations[w['operation']]['target']!=self.f.operations[oid]['target']:
                continue
            s,v=w['raw']['path'],w['raw']['value']
            if not family(s,obj):
                continue
            args=v.get('args',[])
            if v.get('kind')=='transaction_value' or v.get('kind')=='literal' and v.get('value') in (0,'0'):
                continue
            if len(args)==2 and v.get('op')=='-' and key(args[0])==key(s):
                continue
            if len(args)==2 and v.get('op')=='+' and any(key(x)==key(s) for x in args) and any(x.get('kind')=='transaction_value' for x in args):
                continue
            return []
        return origins

    def _net_probes(self,e,base,cf,frames,world,change,observe,context,queries,measurements,work):
        """Compare the same holder's payout less debit, conditional on both scoped requests committing."""
        f=self.f; lookup=f.lookup(observe);z=e.z;slot=cf['slot']+1
        spec=context['observable'];controls=spec['control_selectors']
        change_keys=[w['path'] for w in f.paths[cf['path']]['raw']['writes']]
        if not any(family(c,w) and not self.graph._disjoint_keys(c,w) for c in controls for w in change_keys):
            return
        def eligible(pid):
            p=f.paths[pid]['raw']
            audit=self.condition_dependencies(observe,pid,p)
            return not audit['unknown_dependencies'] and not audit['credential_dependencies']
        change_audit=self.condition_dependencies(change,cf['path'],f.paths[cf['path']]['raw'])
        if change_audit['unknown_dependencies'] or change_audit['credential_dependencies']:
            return
        for obj in spec['objects']:
            units=self.net_unit(observe,obj)
            if not units:
                continue
            holder=self._holder(observe,obj)
            candidates=[]
            for fr1 in frames:
                self.check()
                pid=fr1['path']
                if not eligible(pid) or not any(key(w['path'])==key(obj) for w in f.paths[pid]['raw']['writes']):
                    continue
                fr0=frame(f,observe,pid,slot,cf['before'])
                candidates.append((fr0,fr1))
            def quantities(fr):
                history=fr['before']
                cell=qualify(obj,slot)
                pre=e.expr(read(cell,history,lookup))
                post=e.expr(read(cell,history+fr['writes'],lookup))
                who=e.expr(read(qualify(holder,slot),history,lookup))
                amounts=[z.If(e.expr(fx['recipient'])==who,e.expr(fx['amount']),z.IntVal(0)) for fx in fr['effects'] if fx['kind']=='native_transfer']
                # Unsupported payments/external effects cannot be silently valued at zero.
                if not amounts or any(fx['kind']!='native_transfer' for fx in fr['effects']):
                    return None
                return who,pre,pre-post,z.Sum(*amounts)
            for (before,_),(_,after) in itertools.product(candidates,repeat=2):
                self.check()
                if work['pairs']>=f.options.max_prefixes:
                    work['truncated']=True
                    return
                work['pairs']+=1
                a,b=quantities(before),quantities(after)
                if a is None or b is None:
                    work['unsupported_pairs']+=1
                    continue
                h0,pre0,debit0,paid0=a;h1,pre1,debit1,paid1=b
                # Keys can also depend on storage changed by the intervention.
                key_constraints=[e.expr(read(qualify(k,slot),before['before'],lookup))==
                                 e.expr(read(qualify(k,slot),after['before'],lookup)) for k in keys(obj)]
                actual_control=z.Or(*[e.expr(read(qualify(c,slot),before['before'],lookup))!=
                                       e.expr(read(qualify(c,slot),after['before'],lookup)) for c in controls])
                common=z.And(base,actual_control,encode_frame(e,before),encode_frame(e,after),h0==h1,h0!=e.expr(cf['caller']),
                             pre0==pre1,debit0==debit1,debit0>0,*key_constraints)
                details={'target':f.operations[observe]['target'],'change':change,'observe':observe,'change_path':cf['path'],
                         'before_path':before['path'],'after_path':after['path'],'object':obj,'holder':holder,'unit':'native base unit',
                         'unit_sources':units,'changed_writes':change_keys,'observed_controls':controls,
                         'before_net':str(paid0-debit0),'after_net':str(paid1-debit1),
                         'before_debit':str(debit0),'after_debit':str(debit1),'before_paid':str(paid0),'after_paid':str(paid1),
                         'assumptions':'same symbolic prestate, same request and account/key, positive equal debit; different controller and holder; deployability and business consent not proved'}
                feasible=self._query(e,common,'comparable_holder_requests',details);queries.append(feasible)
                if not feasible['bounded_condition_confirmed']:
                    continue
                result=self._query(e,z.And(common,paid1-debit1<paid0-debit0),'holder_net_lower_after',details)
                queries.append(result)
                measurements.append({'scope':details,'feasible_probe':feasible['id'],'result_probe':result['id'],
                                     'answer':result['answer'],'validated':result['bounded_condition_confirmed']})

    def _holder_deltas(self, observe):
        """A source ledger delta. Financial meaning remains the model's hypothesis."""
        lookup = self.f.lookup(observe)
        debits, credits = {}, {}
        for _,path in self.paths(observe):
            for w in path['writes']:
                dst, val = w['path'], w['value']
                who = self._holder(observe,dst)
                if not who or who.get('kind') not in ('actual_sender','parameter'):
                    continue
                if not str(value_type(dst,lookup)).startswith('uint'):
                    continue
                args = val.get('args',[])
                if len(args)!=2:
                    continue
                # Earlier writes to the same map may expand the old value to an
                # alias-conditioned read. This only nominates a cell; the formula checks
                # its actual pre/post balance with all original writes and ordered keys.
                uses_old=lambda expr:any(key(s)==key(dst) for s in selectors(expr))
                if val.get('op')=='-' and uses_old(args[0]):
                    debits[key(dst)]=(dst,who,'debit')
                elif val.get('op')=='+' and any(uses_old(t) for t in args):
                    credits[key(dst)]=(dst,who,'credit')
        return list((debits or credits).values())

    def _holder_commit(self,e,fr,observe,slot,context,mapping=None):
        normal = encode_frame(e,fr)
        if not context.get('observable',{}).get('hold_other_request_cells'):
            return normal
        mapping = mapping or {}
        ledger = context['observable']['holder_delta']
        cell,holder = (qualify(ledger[k],slot) for k in ('cell','holder'))
        if mapping:
            cell,holder = _replace(cell,mapping),_replace(holder,mapping)
        pre = e.expr(read(cell,fr['before'],e.lookup))
        post = e.expr(read(cell,fr['before']+fr['writes'],e.lookup))
        who = e.expr(read(holder,fr['before'],e.lookup))
        controller = e.expr(qualify({'kind':'actual_sender'},slot-1))
        movement = post < pre if ledger['direction']=='debit' else post > pre
        return e.z.And(normal,movement,who!=0,who!=controller)

    def _group_holder(self, observe):
        """The second request must belong to a different holder, not just a different spender."""
        holders = {}
        for _, path in self.paths(observe):
            for w in path['writes']:
                args = w['value'].get('args', [])
                if w['value'].get('op') != '-' or not args or key(args[0]) != key(w['path']):
                    continue
                who = self._holder(observe,w['path'])
                if who and who.get('kind') in ('actual_sender','parameter'):
                    holders[key(who)] = who
        if len(holders) == 1:
            return next(iter(holders.values()))
        return None

    def _compare(self,change,observe,context):
        f=self.f
        if f.operations[change]['target']!=f.operations[observe]['target']:
            return {'kind':'causal_compare','status':'unsupported','reason':'cross_target_world_not_supported','change':change,'observe':observe}
        from .ledger import MEASURES,compare_ledger
        from .local_properties import check_local
        measure=context.get('observable',{}).get('measure')
        if measure == 'financial_block':
            from .blocking import compare
            return compare(self,change,observe,context)
        if measure == 'financial_value':
            from .financial_value import compare
            return compare(self,change,observe,context)
        if measure in MEASURES:return compare_ledger(self,change,observe,context)
        if measure in ('missing_control','direct_effect','denied_qualified','authorization_violation'):return check_local(self,change,observe,context)
        queries=[];worlds=[];comparisons=[];errors=[];alternatives=[];consent_counterexamples=[]
        observable=context.get('observable',{});measure=observable.get('measure')
        measurements=[];net_work={'pairs':0,'truncated':False,'unsupported_pairs':0}
        # A common prefix consumes at most one of the two pre-observe transaction slots.
        # A later call can use the same function with different parameters/state.
        # Frame slots, not function-name exclusion, establish transaction identity.
        # The unseeded paired prestate already spans all encoded prestates.
        # A prefix is executed only when the semantic question specifically needs
        # an established state, not once for every neighboring state writer.
        candidates=context.get('prefix_providers',[])
        prefixes=[()]+[(i,) for i in candidates] if f.options.prefix_depth>=2 else [()]
        for prefix in prefixes[:f.options.max_prefixes]:
            self.check()
            products=itertools.product(*[self.paths(i) for i in prefix])
            for selected in itertools.islice(products,f.options.max_prefixes):
                self.check();modes=context.get('caller_modes') or (('same_requester','independent_actors') if f.options.scope=='AC' else ('independent_actors',))
                for (cpid,_),caller_mode,case in itertools.product(self.paths(change),modes,context.get('premise_cases') or [[]]):
                    self.check()
                    if len(worlds)>=f.options.max_prefixes:break
                    qualified=observable.get('qualified_writer_paths')
                    if qualified and cpid not in qualified:continue
                    try:
                        local_context=dict(context,encoded_case=case)
                        e,base,ok0,ok1,use0,use1,world,cf,afterframes=self._paired(change,observe,cpid,prefix,[pid for pid,_ in selected],caller_mode,local_context)
                        z=e.z;qs=[]
                        if measure in ('opens','blocks'):
                            ctrl=observable['control_selectors'];slot=cf['slot']+1
                            before=cf['before'];after=before+cf['writes']
                            changed=z.Or(*[e.expr(read(qualify(s,slot),before,f.lookup(observe)))!=
                                           e.expr(read(qualify(s,slot),after,f.lookup(observe))) for s in ctrl])
                            base=z.And(base,changed)
                            if observable.get('hold_other_request_cells'):
                                selected_positions = {key(cell) for cell in ctrl}
                                for cell in self.graph.request_reads(observe):
                                    # Isolate different keys of the named position. All other genuine
                                    # writes of the intervention remain in W1, including coupled effects.
                                    if key(cell) in selected_positions or not any(family(cell, s) for s in ctrl):
                                        continue
                                    position = qualify(cell, slot)
                                    base=z.And(base, e.expr(read(position,before,f.lookup(observe))) ==
                                               e.expr(read(position,after,f.lookup(observe))))
                        forms=[('baseline_usable',ok0),('opened_by_change',z.And(z.Not(ok0),use1)),
                               ('blocked_by_change',z.And(use0,z.Not(use1))),('both_usable',z.And(ok0,ok1))]
                        profile=context.get('profile','all')
                        needed={'blocking':{'baseline_usable','blocked_by_change','both_usable'},
                          'authorization':{'baseline_usable','opened_by_change','both_usable'},
                          'effect':{'baseline_usable','opened_by_change','both_usable'}}.get(profile)
                        if measure=='holder_net':
                            self._net_probes(e,base,cf,afterframes,world,change,observe,context,queries,measurements,net_work)
                            needed={'both_usable'}
                        elif measure in ('opens','blocks'):
                            needed={'opened_by_change' if measure=='opens' else 'blocked_by_change','baseline_usable'}
                        if measure in ('opens','blocks'):
                            prem=self._query(e,z.And(base,z.Or(use0,use1)),'scenario_feasible',{'encoded_case':case,'change':change,'observe':observe,'change_path':cpid,'prefix':list(prefix),'caller_mode':caller_mode})
                            queries.append(prem)
                        for label,condition in forms:
                            if needed and label not in needed:continue
                            q=self._query(e,z.And(base,condition),label,{'change':change,'observe':observe,'prefix':list(prefix),'change_path':cpid,'caller_mode':caller_mode,'request_context':local_context,'encoded_case':case})
                            queries.append(q);qs.append(q)
                        comparisons.append({'prefix':list(prefix),'change_path':cpid,'caller_mode':caller_mode,'results':{q['label']:q['answer'] for q in qs},
                            'validated':{q['label']:q['bounded_condition_confirmed'] for q in qs},
                            'absence_claim_complete_for_modeled_branches':self.complete(observe)})
                        worlds.append(world)
                        if f.options.scope=='AC' and caller_mode=='same_requester':
                            for opid,p in self.paths(observe):
                                after=next((fr for fr in afterframes if fr['path']==opid),None)
                                if after is None:continue
                                for w in p['writes']:
                                    if measure=='holder_grant' and not any(key(w['path'])==key(obj) for obj in observable['objects']):
                                        continue
                                    holder=self._holder(observe,w['path'])
                                    if holder is None:continue
                                    h=e.expr(read(qualify(holder,len(prefix)+1),cf['before'],f.lookup(observe)))
                                    # A witness for a different observe branch cannot
                                    # refute this object's authorization explanation.
                                    scoped_ok1=encode_frame(e,after)
                                    # Opening a frozen route is not acquiring its
                                    # allowance. Require an actual transition of
                                    # a source grant guard on this ordered key.
                                    controls=[x['path'] for x in self.f.paths[cpid]['raw']['writes']]
                                    transitions=[];grant_details=[];slot=len(prefix)+1
                                    for guard in p['guards']:
                                        cells=selectors(guard)
                                        if not any(n.get('kind')=='actual_sender' for n in walk(guard)):continue
                                        grants=[g for g in cells if g['root']!=w['path']['root'] and
                                            any(key(k)==key(holder) for k in keys(g)) and
                                            any(family(g,c) and not self.graph._disjoint_keys(g,c) for c in controls)]
                                        # A mixed guard cannot use an unrelated
                                        # control's transition as a grant proof.
                                        remaining_cells=selectors(_replace(guard,{key(g):{'kind':'source_grant_placeholder'} for g in grants}))
                                        holder_cells={key(s) for s in selectors(holder)}
                                        if not grants or any(key(c) not in holder_cells for c in remaining_cells):continue
                                        if measure=='holder_grant' and not all(any(key(g)==key(c) for c in observable['control_selectors']) for g in grants):
                                            continue
                                        before_guard=read(qualify(guard,slot),cf['before'],f.lookup(observe))
                                        after_guard=read(qualify(guard,slot),cf['before']+cf['writes'],f.lookup(observe))
                                        gf=lambda v:dict(after,guards=[v],writes=[],evaluated_terms=[])
                                        changed_cells=z.Or(*[e.expr(read(qualify(g,slot),cf['before'],f.lookup(observe)))!=
                                            e.expr(read(qualify(g,slot),cf['before']+cf['writes'],f.lookup(observe))) for g in grants])
                                        transitions.append(z.And(z.Not(encode_frame(e,gf(before_guard))),encode_frame(e,gf(after_guard)),changed_cells))
                                        grant_details.append({'guard':guard,'grant_selectors':grants,'before':before_guard,'after':after_guard})
                                    if not transitions:continue
                                    q=self._query(e,z.And(base,z.Not(ok0),scoped_ok1,e.expr(cf['caller'])!=h,z.Or(*transitions)),
                                        'requester_opens_other_holders_gate',{'change':change,'observe':observe,'holder_candidate':holder,'object':w['path'],
                                            'authorization_gate_transition':True,'grant_transition_scope':grant_details,
                                            'observe_path':opid,'change_path':cpid,'target':f.operations[observe]['target'],
                                            'caller_mode':caller_mode,'prefix':list(prefix),
                                            'observe_guard_selectors':selectors(p['guards']),
                                            'intervened_controls':[x['path'] for x in self.f.paths[cpid]['raw']['writes']]})
                                    queries.append(q);consent_counterexamples.append(q)
                        if f.options.scope=='FCR' and profile in ('all','blocking'):
                            if measure=='opens':
                                # Group-block and blocked-route alternatives both imply this same-world prerequisite.
                                # Preserve the requested opening result; skip only logically impossible extensions.
                                block_seed=self._query(e,z.And(base,ok0,z.Not(ok1)),'block_prerequisite_for_extensions',
                                    {'change':change,'observe':observe,'change_path':cpid,'prefix':list(prefix),'caller_mode':caller_mode,'encoded_case':case})
                                queries.append(block_seed)
                                if block_seed['answer']=='unsat' and not block_seed.get('abstract_hash'):
                                    comparisons[-1]['inapplicable_extensions']={'blocking_prerequisite':block_seed['id'],'checks':['two_distinct_holders_blocked_same_change','same_right_alternative_after_change']}
                                    continue
                            # A second requester is a separate scope probe, never silently mixed into W0/W1.
                            holder = observable.get('holder_delta',{}).get('holder') or self._group_holder(observe)
                            if holder is None or any(key(b['parameter']) == key(holder) for b in context.get('bindings',[])):
                                alternatives += self.alternatives(e,base,z.And(ok0,z.Not(ok1)),change,observe,cf,len(prefix)+1)
                                continue
                            slot = len(prefix)+1
                            original_holder = qualify(holder,slot)
                            newcaller={'kind':'parameter','id':-79000001,'type':'address'}
                            u=e.expr(original_holder)
                            mapping={key(original_holder):newcaller}
                            other0=[];other1=[]
                            for pid,_ in self.paths(observe):
                                self.check()
                                a=_replace(frame(f,observe,pid,len(prefix)+1,cf['before']),mapping)
                                b=_replace(frame(f,observe,pid,len(prefix)+1,cf['before']+cf['writes']),mapping)
                                other0.append(self._holder_commit(e,a,observe,slot,context,mapping));other1.append(encode_frame(e,b))
                            two=z.And(use0,z.Not(ok1),z.Or(*other0),z.Not(z.Or(*other1)),u!=e.expr(newcaller),e.expr(newcaller)!=0,e.expr(newcaller)!=e.expr(cf['caller']))
                            q=self._query(e,z.And(base,two),'two_distinct_holders_blocked_same_change',{'change':change,'observe':observe,'scope_probe':True,'distinct_source_holder':holder})
                            queries.append(q)
                            alternatives +=self.alternatives(e,base,z.And(ok0,z.Not(ok1)),change,observe,cf,len(prefix)+1)
                    except TimeoutError:raise
                    except Exception as error:errors.append({'prefix':list(prefix),'path':cpid,'reason':type(error).__name__+':'+str(error)})
                    if len(worlds)>=f.options.max_prefixes:break
                if len(worlds)>=f.options.max_prefixes:break
            if len(worlds)>=f.options.max_prefixes:break
        qualified=observable.get('qualified_writer_paths')
        omitted=[pid for pid,_ in self.paths(change) if qualified and pid not in qualified]
        controls=[w['raw']['path'] for w in f.writes.values() if w['operation']==change]
        used=[s for _,p in f.operation_paths(observe) for s in selectors([p['guards'],p['writes'],p.get('sensitive_effects',[])])]
        relevant=[s for s in controls if any(family(s,t) and not self.graph._disjoint_keys(s,t) for t in used)]
        unknown=any(n.get('kind') in ('unknown','external_return','read_call','call_unresolved') for _,p in f.operation_paths(observe) for n in walk(p))
        return {'kind':'causal_compare','change':change,'observe':observe,'comparisons':comparisons,'worlds':worlds,
            'queries':queries,'local_errors':errors,'alternative_uses':alternatives,
            'observed_measure':measure,'net_measurements':measurements,'net_pair_budget':net_work,
            'holder_consent_counterexamples':consent_counterexamples,
            'complete_for_modeled_observe_branches':self.complete(observe),'all_prefixes_exhausted':len(worlds)<f.options.max_prefixes,
            'complete_for_modeled_change_branches':self.complete(change) and not omitted,
            'evidence_scope':{'target':f.operations[observe]['target'],'change':change,'observe':observe,
                 'change_paths_outside_privilege_scope':omitted,
                 'controls':controls,'relevant_controls':relevant,'request_context':context,'prefixes':prefixes,
                 'semantic_quantity_and_holder_not_proven':True},
            'control_noninterference':{'proved':bool(controls) and not relevant and self.complete(observe) and not unknown,
                 'controls':controls,'observe':observe,'scope':'complete encoded source dependencies, not selected-prefix UNSAT'},
            'no_program_mutation':True,'SAT_is_behavior_not_legitimate_policy':True}
    def alternatives(self,e,base,original_request_blocked,change,observe,cf,slot):
        """Same object, request quantity/recipient and requester; exact key equations."""
        f=self.f;lookup=f.lookup(observe);z=e.z;out=[]
        original=[]
        for _,p in self.paths(observe):
            for w in p['writes']:
                v=w['value']
                if v.get('kind')=='op' and v.get('op')=='-' and key(v['args'][0])==key(w['path']):
                    original.append((w['path'],v['args'][1]))
        if not original:return out
        sourcepaths=[p for _,p in self.paths(observe)]
        for alt in self.graph.writers(f.operations[observe]['target'],[s for s,_ in original],'same-object alternative investigation'):
            self.check()
            if alt in (change,observe):continue
            for pid,p in self.paths(alt):
                self.check()
                if not p.get('sensitive_effects') and not any(w['value'].get('kind')=='op' and w['value'].get('op')=='+' for w in p['writes']):continue
                for s,quantity in original:
                    candidates=[w for w in p['writes'] if family(w['path'],s) and w['value'].get('kind')=='op' and w['value'].get('op')=='-']
                    for w in candidates:
                        try:
                            fr=frame(f,alt,pid,slot,cf['before']+cf['writes']);eq=[]
                            for a,b in zip(keys(w['path']),keys(s)):
                                # Preserve the actual request object argument before evaluating an offset key.
                                # Otherwise asset+1 could be called with asset-1 and silently change the request.
                                params={key(x):x for x in walk(a) if x.get('kind')=='parameter'}
                                if a.get('kind')=='op' and len(params)==1 and b.get('kind')=='parameter':
                                    eq.append(e.expr(qualify(next(iter(params.values())),slot))==e.expr(qualify(b,slot)))
                                eq.append(e.expr(qualify(a,slot))==e.expr(qualify(b,slot)))
                            aq=w['value']['args'][1];eq.append(e.expr(qualify(aq,slot))==e.expr(qualify(quantity,slot)))
                            # Target and alternative native payouts must go to the same recipient.
                            original_fx=[fx for p0 in sourcepaths for fx in p0.get('sensitive_effects',[]) if fx['kind']=='native_transfer']
                            alt_fx=[fx for fx in p.get('sensitive_effects',[]) if fx['kind']=='native_transfer']
                            if original_fx and alt_fx:
                                eq.append(e.expr(qualify(original_fx[0]['recipient'],slot))==e.expr(qualify(alt_fx[0]['recipient'],slot)))
                            success=encode_frame(e,fr,eq)
                            q=self._query(e,z.And(base,original_request_blocked,success),'same_right_alternative_after_change',{'observe':observe,'alternative':alt,'path':pid,'object':s,'original_same_request_is_blocked_in_W1':True})
                            out.append({'operation':alt,'path':pid,'object':s,'query':q,
                              'same_request_bindings':eq and [str(x) for x in eq],'usable':q['bounded_condition_confirmed'],
                              'admin_only_route_not_assumed_holder_usable':True})
                        except TimeoutError:raise
                        except Exception as error:out.append({'operation':alt,'path':pid,'usable':False,'reason':str(error)})
        return out

```

## source/src/pr_next_joint/investigation/blocking.py

原文件SHA256 `72cb565570430278396cdf5297478f329857c8d02a7908670fe85db7e660401a`

```python
"""Productive-request comparison with a shared real prefix and scoped exclusion."""
import itertools
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import selectors, keys, selector_relation
from pr_next_joint.verification.source_worlds import frame, encode_frame, serialize_world
from pr_next_joint.verification.program_encoding import MechanismEncoder
from pr_next_joint.verification.sequence import qualify
from pr_next_joint.verification.expressions import Unsupported
from .ledger import movements, unit_origin, flow, grant_for, native_only_position
from .roles import path_qualification, fixed_role_terms


def continuation_frontier_covered(b, operation):
    """Every unexpanded continuation has an explicit source prefix.

    Loop prefixes and unresolved calls retain necessary guards. A failed
    frontend or a discarded path frontier does not provide that coverage.
    """
    rows=list(b.f.operation_paths(operation))
    return bool(rows) and not any(g.get('kind')=='path_extraction' for g in b.f.operations[operation]['gaps']) and not any(
        'source_path_frontier_bound_exceeded' in str(i.get('reason',''))
        for _,p in rows for i in p.get('issues',[]))


def may_continue(b,e,operation,pid,writes,slot,request=None,primary=False):
    """Necessary source guards overapproximate an unmodeled continuation.

    This formula is usable only under NOT to prove *no* productive bypass.
    SAT of it is not a real transfer, and UNSAT of the overall risk query is
    not a refutation when this approximation participated.
    """
    from pr_next_joint.verification.sequence import read
    p=b.f.paths[pid]['raw'];z=e.z
    guards=list(p['guards']);dropped=[]
    for call in b.f.call_summaries.rows.values():
        if call['operation']!=operation or call['path']!=pid:continue
        if call['mode']!='STATICCALL' and call['unresolved_implementation']:
            # Unknown callbacks may change storage. Only guards evaluated
            # before the actual call remain necessary source conditions.
            permitted={key(g)for g in call['callpoint_guards']} if call['callpoint_exact'] else set()
            dropped += [g for g in guards if key(g)not in permitted]
            guards=[g for g in guards if key(g)in permitted]
    opaque={'unknown','external_return','read_call','call_unresolved','credential_recovery','index','array_length'}
    kept=[];terms=[];variables={}
    mc,md=len(e.constraints),len(e.domain_constraints)
    def local_input(node):
        # Intervention and prefix inputs are already fixed for this shared
        # state. Only this alternative transaction may choose new inputs.
        return (node.get('kind')=='parameter' and node.get('step')==slot or
                node.get('kind')=='transaction_origin' and node.get('sequence_step')==slot)
    for guard in guards:
        if any(n.get('kind')in opaque or n.get('kind')=='parameter' and '[' in n.get('type','') for n in walk(guard)):
            dropped.append(guard);continue
        g=read(qualify(guard,slot),writes,e.lookup)
        markc,markd=len(e.constraints),len(e.domain_constraints)
        try:
            term=e.expr(g);terms.append(term);kept.append(guard)
            if not primary:
                for n in walk(g):
                    if local_input(n):
                        value=e.expr(n)
                        if z.is_const(value) and not (z.is_int_value(value)or z.is_true(value)or z.is_false(value)):
                            variables[str(value)]=value
        except Unsupported:
            del e.constraints[markc:];del e.domain_constraints[markd:];dropped.append(guard)
    # A source-derived holder mapping narrows an alternate route to the
    # original holder. Ambiguous mapping remains an overapproximation.
    if not primary and request is not None:
        hs=[keys(w['path'])[0]for w in p['writes'] if len(keys(w['path']))==1 and
            unit_origin(b,operation,w['path']) and w['path']in movements(b,operation,p)['-']]
        if hs and all(key(h)==key(hs[0])for h in hs):
            try:
                h=read(qualify(hs[0],slot),writes,e.lookup);value=e.expr(h)
                terms.append(value==request['holder'])
                for atom in walk(h):
                    if local_input(atom):
                        v=e.expr(atom);variables[str(v)]=v
            except Unsupported:pass
    local=e.constraints[mc:]+e.domain_constraints[md:]
    del e.constraints[mc:];del e.domain_constraints[md:]
    value=z.And(*terms,*local)
    if variables:value=z.Exists(list(variables.values()),value)
    return value,{'operation':operation,'path':pid,'kind':'necessary_source_guard_overapproximation',
        'retained_guards':kept,'omitted_guards':dropped,'not_a_productive_witness':True,
        'only_excluding_this_continuation_supports_blockage':True}


def request_terms(b, e, fr, operation):
    path = b.f.paths[fr['path']]['raw']
    lookup = b.f.lookup(operation)
    moves = movements(b, operation, path)
    from .summary import local_delta, unique
    debits = unique(w['path'] for w in path['writes'] if local_delta(w)[0] == '-' and unit_origin(b, operation, w['path']))
    credits = unique(w['path'] for w in path['writes'] if local_delta(w)[0] == '+' and unit_origin(b, operation, w['path']))
    holders = {str(flow(e, lookup, fr, c)[0]): flow(e, lookup, fr, c)[0] for c in debits}
    recipients = {str(flow(e, lookup, fr, c)[0]): flow(e, lookup, fr, c)[0] for c in credits}
    numeric = [b.f.terms[p['term']]['expression'] for p in b.f.operations[operation]['parameters']
               if b.f.terms[p['term']]['expression'].get('type','').startswith('uint')]
    # This adapter is source typed. Ambiguous multi-asset/multi-quantity entries
    # remain an explicit dependency rather than using parameter names/order.
    if len(holders) != 1 or len(recipients) != 1 or len(numeric) != 1:
        return None
    return {'holder': next(iter(holders.values())), 'recipient': next(iter(recipients.values())),
            'amount': e.expr(qualify(numeric[0], fr['slot']))}


def alternate_continuation(b, e, other, pid, after_writes, request, slot):
    path = b.f.paths[pid]['raw']
    if path_qualification(b.f, other, path):
        return None, 'privileged_assistance_is_not_an_ordinary_bypass'
    dependencies = b.condition_dependencies(other, pid, path)
    if dependencies['unknown_dependencies'] or dependencies['credential_dependencies']:
        return None, 'alternative_has_decisive_call_or_credential_dependency'
    mark_constraints, mark_domain = len(e.constraints), len(e.domain_constraints)
    fr = frame(b.f, other, pid, slot, after_writes)
    use, _ = productive(b, e, fr, other)
    if e.z.is_false(e.z.simplify(use)):
        # A known return-false/no-effect branch needs no request adapter.
        return e.z.BoolVal(False), None
    own = request_terms(b, e, fr, other)
    if own is None:
        return None, 'alternative_typed_request_mapping_ambiguous'
    equality = [own[k] == request[k] for k in ('holder','recipient','amount')]
    local = list(e.constraints[mark_constraints:]) + list(e.domain_constraints[mark_domain:])
    del e.constraints[mark_constraints:]
    del e.domain_constraints[mark_domain:]
    variables = [e.expr(fr['caller'])]
    variables += [e.expr(qualify(b.f.terms[p['term']]['expression'], slot)) for p in b.f.operations[other]['parameters']]
    return e.z.Exists(variables, e.z.And(use, *equality, *local)), None


def productive(b, e, fr, use):
    z = e.z
    mark = len(e.constraints)
    path = b.f.paths[fr['path']]['raw']
    terms, objects = [], []
    for cell in movements(b, use, path)['-']:
        if not unit_origin(b, use, cell) or native_only_position(b, use, cell):
            continue
        h, start, end, debit, credit = flow(e, b.f.lookup(use), fr, cell)
        credited=[]
        for other in movements(b,use,path)['+']:
            if selector_relation(cell,other)!='same_shape' or key(cell)==key(other):continue
            recipient,before,after,_,_=flow(e,b.f.lookup(use),fr,other)
            credited.append(z.And(recipient!=h,recipient!=0,after>before))
        terms.append(z.And(h != 0, start > end, z.Or(*credited)))
        objects.append(cell)
    success = encode_frame(e, fr)
    local = e.constraints[mark:]
    del e.constraints[mark:]
    return z.And(success, z.Or(*terms), *local), objects


def root_reason(error):
    message=str(error).split(':',1)[0]
    return message if message.isidentifier() else type(error).__name__


def bool_under(term, control, enabled, holders, ordinary=True):
    """Truth forced by the selected control and the non-exempt request domain."""
    op=term.get('op'); args=term.get('args',[])
    if term.get('kind')=='literal' and type(term.get('value')) is bool:return term['value']
    if term.get('kind')=='storage':
        if selector_relation(term,control)=='same_shape' and (not keys(term) or keys(term)==holders):return enabled
        return None
    if op=='!' and len(args)==1:
        value=bool_under(args[0],control,enabled,holders,ordinary)
        return None if value is None else not value
    if op in ('&&','and','||','or'):
        values=[bool_under(x,control,enabled,holders,ordinary) for x in args]
        if op in ('&&','and'):return False if False in values else True if all(v is True for v in values) else None
        return True if True in values else False if all(v is False for v in values) else None
    if op in ('==','!=') and len(args)==2:
        l=bool_under(args[0],control,enabled,holders);r=bool_under(args[1],control,enabled,holders)
        if l is not None and r is not None:return (l==r)==(op=='==')
    return None


def ordinary_exemptions(b,oid,guards,control,holder=None):
    """Identify governed exception tables for the caller or the actual debit holder."""
    from .roles import _role_index
    from pr_next_joint.frontend.storage import value_type
    f=b.f;target=f.operations[oid]['target'];registry=_role_index(f,target)
    actors=[{'kind':'actual_sender'}]+([holder] if holder else [])
    result=set();cache=b.__dict__.setdefault('_governed_exception_tables',{})
    for term in selectors(guards):
        rid=term['root'];idx=keys(term)
        if rid==control['root'] or len(idx)!=1 or idx[0] not in actors or value_type(term,f.lookup(oid))!='bool':continue
        stamp=(target,rid)
        if stamp not in cache:
            writers=[w for w in f.writes.values() if w['raw']['path']['root']==rid
                     and f.operations[w['operation']]['target']==target
                     and w['raw']['value'].get('value') is not False]
            protected=bool(writers) and all(
                f.paths[w['path']]['raw']['flow'] in ('returned','normal')
                and not f.operations[w['operation']]['gaps']
                and path_qualification(f,w['operation'],f.paths[w['path']]['raw'])
                for w in writers)
            cache[stamp]=bool(protected or registry.get(rid,{}).get('kind')=='caller_membership')
        if cache[stamp]:result.add(rid)
    return result


def gates_ordinary(b,oid,path,control,blocked,holder):
    """Rules out this productive branch for the same ordinary unexempt request."""
    from .behavior import _replace
    exemptions=ordinary_exemptions(b,oid,path['guards'],control,holder)
    replace={key(s):{'kind':'literal','value':False} for s in selectors(path['guards'])
             if s['root'] in exemptions and keys(s) in ([{'kind':'actual_sender'}],[holder])}
    return any(bool_under(_replace(g,replace),control,blocked,[holder]) is False for g in path['guards'])


def delegated_exception(b,routes,control,blocked):
    """Find a source-defined alternate for the same economic request, conditional on
    a holder grant and independently governed sender privilege. No grant is assumed.
    Unconditional alternatives are tested separately by gates_ordinary.
    """
    from .behavior import _replace
    from .summary import holder, local_delta
    for alternate in routes:
        oid=alternate['operation'];lk=b.f.lookup(oid);p=b.f.paths[alternate['path']]['raw']
        payer=holder(alternate['debit'],lk)
        if not payer or payer.get('kind')!='parameter' or p.get('sensitive_effects') or p.get('issues') or p.get('evaluation_gaps'):continue
        grants=grant_for(b,oid,p,alternate['debit'])
        if not grants or not any(key(w['path'])==key(grants) and local_delta(w)[0]=='-' for w in p['writes']):continue
        exceptions=ordinary_exemptions(b,oid,p['guards'],control)
        if not exceptions or not gates_ordinary(b,oid,p,control,blocked,payer):continue
        # A privileged flag must turn an actual necessary outgoing guard from
        # false to satisfiable under the disabled switch; other guards still apply.
        flagged=[s for s in selectors(p['guards']) if s['root'] in exceptions and keys(s)==[{'kind':'actual_sender'}]]
        for flag in flagged:
            for g in p['guards']:
                no=_replace(g,{key(flag):{'kind':'literal','value':False}})
                yes=_replace(g,{key(flag):{'kind':'literal','value':True}})
                if bool_under(no,control,blocked,[payer]) is not False or bool_under(yes,control,blocked,[payer]) is not True:continue
                if any(bool_under(_replace(other,{key(flag):{'kind':'literal','value':True}}),control,blocked,[payer]) is False for other in p['guards']):continue
                amount=[v for v in b.f.operations[oid]['parameters'] if b.f.terms[v['term']]['expression'].get('type','').startswith('uint')]
                recipient=holder(alternate['credit'],lk)
                if len(amount)!=1 or not recipient or recipient.get('kind')!='parameter' or key(recipient)==key(payer):continue
                request=b.f.terms[amount[0]['term']]['expression']
                if not any(key(w['path'])==key(grants) and local_delta(w)[0]=='-' and
                           key(local_delta(w)[1])==key(request) for w in p['writes']):continue
                return {'scope':'same_ledger_holder_recipient_and_request_quantity','use':b.f.operations[oid]['source'],
                        'requires_prior_holder_grant':True,'requires_exempt_spender':True,'availability':'conditional_on_existing_grant_and_membership'}
    return None


def _direct_baseline(b,change,cpid,route,control,blocked,cat):
    """Check the actual positive use and committing controller transition in one source state.
    Search only useful enabling and grant writers; normal initial and prefix bounds apply.
    """
    from pr_next_joint.verification.sequence import read
    from .behavior import ordered_clocks
    from .summary import holder
    f=b.f;use=route['operation'];pid=route['path'];lk=f.lookup(use)
    cp=f.paths[cpid]['raw'];p=f.paths[pid]['raw'];grant=grant_for(b,use,p,route['debit'])
    delegated=holder(route['debit'],lk).get('kind')!='actual_sender'
    if delegated and not grant:return None
    extra=[]
    for oid in f.operations:
        if f.operations[oid]['target']!=f.operations[change]['target']:continue
        for wpid,wp in f.operation_paths(oid,True):
            for w in wp['writes']:
                if grant and selector_relation(w['path'],grant)=='same_shape' and w['value'].get('kind')=='parameter' and any(k.get('kind')=='actual_sender' for k in keys(w['path'])):
                    extra.append((0,len(wp['writes']),len(wp['guards']),oid,wpid))
                elif w['path']['root']==control['root'] and w['path'].get('segments')==control.get('segments') and (
                        w['value'].get('kind')!='literal' or w['value'].get('value')!=blocked):
                    extra.append((1,len(wp['writes']),len(wp['guards']),oid,wpid))
    # Prefer a grant or enabling write with fewer unrelated committed changes.
    # The actual prefix and every guard are still checked by the same encoder.
    ordered=list(dict.fromkeys((oid,wpid) for *_,oid,wpid in sorted(extra)))
    from itertools import chain, islice, permutations
    singles=((item,) for item in ordered) if f.options.prefix_depth>=1 else ()
    pairs=permutations(ordered,2) if f.options.prefix_depth>=2 else ()
    for sequence in islice(chain([()],singles,pairs),f.options.max_prefixes):
        b.check()
        try:
            e=MechanismEncoder(lk);z=e.z;prior=[];terms=[]
            for slot,(oid,wpid) in enumerate(sequence):
                prefix=frame(f,oid,wpid,slot,prior);terms.extend([encode_frame(e,prefix),e.expr(prefix['caller'])!=0])
                prior=prior+prefix['writes']
            slot=len(sequence);cf=frame(f,change,cpid,slot,prior);uf=frame(f,use,pid,slot+1,prior)
            terms.extend([encode_frame(e,cf),encode_frame(e,uf),*ordered_clocks(e,slot+1)])
            actor=e.expr(cf['caller']);user=e.expr(uf['caller'])
            h,before,after,_,_=flow(e,lk,uf,route['debit'])
            recipient,rb,ra,_,_=flow(e,lk,uf,route['credit'])
            terms.extend([actor!=0,user!=0,h!=0,h!=actor,user!=actor,recipient!=0,recipient!=h,before>after,ra>rb])
            if any(n.get('kind')=='contract_address' for n in walk(cp['guards'])):
                terms.append(actor!=e.expr({'kind':'contract_address','type':'address'}))
            payer=holder(route['debit'],lk)
            flags=ordinary_exemptions(b,use,p['guards'],control,payer)
            for flag in selectors(p['guards']):
                if flag['root'] in flags and keys(flag) in ([{'kind':'actual_sender'}],[payer]):
                    terms.append(z.Not(e.expr(read(qualify(flag,slot+1),prior,lk))))
            # Match the *effective* control on the holder, after all setter writes.
            use_cell={**control,'segments':[{'key':qualify(holder(route['debit'],lk),slot+1)}] if keys(control) else []}
            terms.extend([e.expr(read(use_cell,prior,lk))!=blocked,
                          e.expr(read(use_cell,prior+cf['writes'],lk))==blocked])
            final_control=qualify(control,slot)
            if keys(control):terms.append(e.expr(keys(final_control)[0])==h)
            q=b._query(e,z.And(*terms),'productive_control_transition',{
                'operation':change,'observe':use,'target':f.operations[use]['target'],'category':cat,
                'same_request':True,'baseline_commit_not_assumed':True,'effect_required':True,
                'initial_prefix_policy':'constructor_only_for_explicit_prefix','measurement_only':True})
            if q.get('bounded_condition_confirmed'):return q['id']
        except (Unsupported,ValueError) as error:
            b.__dict__.setdefault('_control_limit_reasons',set()).add((root_reason(error),use))
            continue
    return None


def source_block_exclusion(inv,q,rows):
    from .source_opinion import opinion
    from .comparison import ledger_routes
    from .summary import holder
    b=inv.backend;f=inv.f;root=inv.root(q);prop=q.get('property') or {};target=f.operations[root]['target']
    changes=[(r['path'],f.paths[r['path']]['raw']) for r in rows if r['committing'] and path_qualification(f,root,f.paths[r['path']]['raw'])]
    if not changes or any(r['effects'] or r['residuals'] for r in rows):return None
    controls={w['path']['root'] for r in rows for w in r['ordered_writes']}
    routes=ledger_routes(b,target)
    affected=[r for r in routes if any(s['root'] in controls for s in selectors(f.paths[r['path']]['raw']['guards']))]
    if not affected:return None
    probes=[]
    # Releasing a flag or granting an exemption cannot remove the original use.
    uses=sorted({r['operation'] for r in affected})
    all_preserved=True
    for use in uses:
        ok,qs=preserved_by_source_transition(b,root,use,prop,changes);probes.extend(q['id'] for q in qs)
        if not ok:all_preserved=False;break
    if all_preserved:
        ans=opinion('normal','same_request_preserved',[w['source'] for r in rows for w in r['ordered_writes']])
        ans.update(same_scope_authorized=True,source_relation={'family':'source_transition_preserves_request','duty':'same_request_preserved','support_location':f.operations[root]['source'],'checks':probes})
        return ans
    # A genuine alternate entry must execute the same holder/asset/recipient/amount.
    # Its input adaptation is existentially bound, not inferred from a name.
    for main in affected:
        use=main['operation'];pid=main['path'];main_path=f.paths[pid]['raw']
        candidates=[r for r in routes if r['debit']['root']==main['debit']['root'] and r['operation']!=use
                    and not any(s['root'] in controls for s in selectors(f.paths[r['path']]['raw']['guards']))]
        covered=False
        for alt in candidates:
            altpath=f.paths[alt['path']]['raw'];altuse=alt['operation']
            if path_qualification(f,altuse,altpath):continue
            valid=True;local=[]
            for cpid,cp in changes:
                try:
                    b.check();e=MechanismEncoder(f.lookup(use));z=e.z;cf=frame(f,root,cpid,0)
                    fr=frame(f,use,pid,1);request=request_terms(b,e,fr,use)
                    if request is None:valid=False;break
                    before,_=productive(b,e,fr,use)
                    after,why=alternate_continuation(b,e,altuse,alt['path'],cf['writes'],request,2)
                    if after is None:valid=False;break
                    roles,origins=fixed_role_terms(e,path_qualification(f,root,cp),0)
                    formula=z.And(encode_frame(e,cf),*roles,before,z.Not(after))
                    query=b._query(e,formula,'control_transition_preservation',{
                        'operation':root,'change':root,'observe':use,'alternative':altuse,
                        'target':target,'property_identity':prop['id'],'semantic_version':prop['semantic_version'],
                        'property_validated':True,'same_request':True,'use_only_for_exclusion':True,
                        'positive_result_usable':False,'proof_required':'persistent_source_invariants_overapproximation',
                        'scope':'same source holder asset recipient and positive amount on actual alternate dispatch'})
                    local.append(query['id'])
                    if not query.get('exclusion_certificate',{}).get('excludes_only_this_formula'):valid=False;break
                except (Unsupported,TimeoutError):valid=False;break
            if valid:covered=True;probes.extend(local);break
        if not covered:return None
    ans=opinion('normal','same_request_bypass',[w['source'] for r in rows for w in r['ordered_writes']])
    ans.update(same_scope_authorized=True,source_relation={'family':'same_request_actual_alternate','duty':'same_asset_holder_request_available','support_location':f.operations[root]['source'],'checks':probes})
    return ans


def ordinary_control_uses(inv,root,category):
    """Rank real outgoing uses of the final control. A source route is not a successful request."""
    from .comparison import ledger_routes
    from .summary import holder
    from .coverage import _control_categories
    from pr_next_joint.frontend.storage import value_type
    _control_categories(inv)
    from .shared_effect_bridge import authority_effect_links
    candidates = set(inv._coverage_control_routes.get((root,category), ()))
    f=inv.f;target=f.operations[root]['target']
    controls={}
    for row in f.summaries.rows(root):
        if not row['committing']:continue
        for w in row['ordered_writes']:
            cell=w['path']
            typ=value_type(cell,f.lookup(root)) or ''
            if bool(keys(cell))==(category=='FCR-FREEZE') and (typ=='bool' or typ.startswith(('uint','int'))):
                controls[(row['path'],key(cell))]=cell
                candidates.update(edge['use'] for edge, reader in authority_effect_links(f, target, cell))
    if not candidates:return ()
    stamp=(root,category,inv.semantics.dependency_identity(candidates|{root}))
    cache=inv.__dict__.setdefault('_ordinary_control_uses',{})
    if stamp in cache:return cache[stamp]
    ranked={}
    for route in ledger_routes(inv.backend,target):
        oid=route['operation']
        if oid not in candidates:continue
        p=f.paths[route['path']]['raw'];payer=holder(route['debit'],f.lookup(oid))
        if not payer:continue
        if path_qualification(f,oid,p):
            # A holder membership that is the selected restrictive control is
            # tested by the ordinary-state comparator, not an admin bypass.
            qualifying={x['declaration'] for proof in path_qualification(f,oid,p) for x in proof['roles']}
            if qualifying-{c['root'] for c in controls.values()}:continue
        if not any(s['root']==ctrl['root'] and (not keys(ctrl) or keys(s)==[payer]) for s in selectors(p['guards']) for ctrl in controls.values()):continue
        delegated=payer.get('kind')!='actual_sender'
        if delegated and not grant_for(inv.backend,oid,p,route['debit']):continue
        rank=(bool(p.get('issues') or p.get('evaluation_gaps')),delegated,f.operations[oid]['source']['start'],oid)
        ranked[oid]=min(ranked.get(oid,rank),rank)
    cache[stamp]=tuple(sorted(ranked,key=ranked.get))
    return cache[stamp]


def ordinary_family(b, change, use, controls):
    """Classify an exact outgoing comparison for an arbitrary non-exempt account."""
    from .comparison import ledger_routes
    from .summary import holder
    f=b.f;target=f.operations[change]['target']
    if f.operations[use]['target']!=target:return None
    routes=ledger_routes(b,target)
    for ctrl in controls:
        if keys(ctrl):continue
        for main in routes:
            if main['operation']!=use:continue
            account=holder(main['debit'],f.lookup(use))
            if not account:continue
            raw=f.paths[main['path']]['raw']
            if not any(s['root']==ctrl['root'] for s in selectors(raw['guards'])):continue
            same=[r for r in routes if r['debit']['root']==main['debit']['root']]
            # Residuals on a source capable of providing the same ordinary
            # request remain decisive. A disjoint effect is outside this scope.
            if not same or any(not continuation_frontier_covered(b,r['operation']) for r in same):continue
            for mode in (True,False):
                admissible=True;governed=set()
                for route in same:
                    oid=route['operation'];branch=f.paths[route['path']]['raw']
                    payer=holder(route['debit'],f.lookup(oid))
                    if not payer or branch.get('issues') or branch.get('evaluation_gaps'):
                        admissible=False;break
                    if path_qualification(f,oid,branch):continue
                    if not gates_ordinary(b,oid,branch,ctrl,mode,payer):
                        admissible=False;break
                    governed.update(ordinary_exemptions(b,oid,branch['guards'],ctrl,payer))
                if admissible and gates_ordinary(b,use,raw,ctrl,mode,account):
                    return {'population':'arbitrary_nonexempt_holder' if governed else 'ordinary_source_holders',
                            'request':'same_holder_asset_recipient_and_positive_quantity',
                            'exemptions':'governed_membership' if governed else 'none_required',
                            'bypass':'checked_applied_productive_routes'}
    return None


def direct_control_result(b,root,use,cat):
    from .comparison import ledger_routes
    from .source_opinion import opinion
    from .summary import holder
    from pr_next_joint.frontend.storage import value_type
    f=b.f;rows=f.summaries.rows(root)
    target=f.operations[root]['target'];routes=ledger_routes(b,target)
    for row in rows:
        path=f.paths[row['path']]['raw']
        if not path_qualification(f,root,path) or row['residuals'] or row['effects']:continue
        final={}
        for w in row['ordered_writes']:final[key(w['path'])]=w
        for w in final.values():
            ctrl=w['path'];indexed=bool(keys(ctrl))
            if value_type(ctrl,f.lookup(root))!='bool' or indexed!=(cat=='FCR-FREEZE'):continue
            if indexed and len(keys(ctrl))!=1:continue
            for route in routes:
                oid=route['operation'];pid=route['path'];p=f.paths[pid]['raw'];lk=f.lookup(oid)
                h=holder(route['debit'],lk)
                if oid!=use or not h or p.get('sensitive_effects') or path_qualification(f,oid,p):continue
                family=route['debit']['root']
                for blocked in (True,False):
                    # At least one real guard reads this exact control/holder.
                    if not any(s['root']==ctrl['root'] and (not indexed or keys(s)==[h]) for s in selectors(p['guards'])):continue
                    if not gates_ordinary(b,oid,p,ctrl,blocked,h):continue
                    candidates=[r for r in routes if r['debit']['root']==family]
                    if any(not path_qualification(f,r['operation'],rp) and
                           not gates_ordinary(b,r['operation'],rp,ctrl,blocked,holder(r['debit'],f.lookup(r['operation'])))
                           for r in candidates for rp in [f.paths[r['path']]['raw']]):continue
                    # A frontier with a possible independently committing transfer is open
                    # unless its already-established guards also exclude the ordinary use.
                    siblings={r['operation'] for r in candidates}
                    if any(c['mode']=='DELEGATECALL' and c['unresolved_implementation'] and
                           f.operations[c['operation']]['target']==target for c in f.call_summaries.rows.values()):continue
                    if any(not continuation_frontier_covered(b,o) or any(
                           rp['flow']!='reverted' and (rp.get('issues') or rp.get('evaluation_gaps')) and
                           not gates_ordinary(b,o,rp,ctrl,blocked,holder(r['debit'],f.lookup(o)))
                           for _,rp in f.operation_paths(o)) for r in candidates for o in [r['operation']]):continue
                    stamp=(root,row['path'],key(ctrl),oid,pid,blocked,b.semantics.dependency_identity(siblings|{root}))
                    cache=b.__dict__.setdefault('_productive_control_checks',{})
                    if stamp not in cache:
                        cache[stamp]=_direct_baseline(b,root,row['path'],route,ctrl,blocked,cat)
                    if cache[stamp]:
                        result=opinion('risk','productive_outgoing_control',[w['source']])
                        result.update(productive_use=f.operations[oid]['source'],basis_probe=cache[stamp],controller_path=row['path'])
                        if cat=='FCR-PAUSE':
                            group=ordinary_family(b,root,oid,[ctrl])
                            if not group:continue
                            result['holder_family']=group
                        exception=delegated_exception(b,candidates,ctrl,blocked)
                        if exception:result['conditional_agent']=exception
                        return result
    return None


def preserved_by_source_transition(b, change, use, prop, qualified_changes):
    """Prove one use cannot be blocked, independently of prefix enumeration.

    A constructor may disable a use, so a productive-state search starts with
    a nonempty enabling prefix. UNSAT for just that prefix is not a general
    exclusion. The backend's separate persistent-invariant overapproximation
    can prove the actual source transition preserves *any* productive input.
    Only that UNSAT certificate is consumed here; SAT is never a finding and
    no constructor/explicit initial value is relaxed for positive evidence.
    Keeping the original use available suffices even if other routes exist.
    """
    if not b.complete(change) or not b.complete(use):return False,[]
    from .scope_relevance import potential_role
    if any(potential_role(b.f,change,path) and not path_qualification(b.f,change,path)
           for _,path in b.paths(change)):return False,[]
    paths=list(b.paths(use))
    for oid,rows in ((change,qualified_changes),(use,paths)):
        for pid,path in rows:
            deps=b.condition_dependencies(oid,pid,path)
            if deps['unknown_dependencies'] or deps['credential_dependencies']:return False,[]
    queries=[]
    for cpid,cp in qualified_changes:
        b.check()
        try:
            e=MechanismEncoder(b.f.lookup(use));z=e.z
            cf=frame(b.f,change,cpid,0)
            role=path_qualification(b.f,change,cp)
            roles,origins=fixed_role_terms(e,role,0)
            base=z.And(encode_frame(e,cf),*roles,e.expr(cf['caller'])!=0)
            before=[];after=[]
            for pid,_ in paths:
                a=frame(b.f,use,pid,1)
                c=frame(b.f,use,pid,1,cf['writes'])
                before.append(productive(b,e,a,use)[0])
                after.append(productive(b,e,c,use)[0])
            detail={'operation':change,'target':b.f.operations[use]['target'],
                'change':change,'observe':use,'change_path':cpid,
                'property_identity':prop['id'],'semantic_version':prop['semantic_version'],
                'property_validated':True,'same_request':True,'role_origins':origins,
                'use_only_for_exclusion':True,'positive_result_usable':False,
                'initial_prefix_policy':'constructor_only_for_explicit_prefix',
                'all_source_use_paths':[pid for pid,_ in paths],
                'proof_required':'persistent_source_invariants_overapproximation',
                'another_use_or_controller_not_excluded':True}
            q=b._query(e,z.And(base,z.Or(*before),z.Not(z.Or(*after))),
                'control_transition_preservation',detail)
            queries.append(q)
            if not q.get('exclusion_certificate',{}).get('excludes_only_this_formula'):
                return False,queries
        except Unsupported:
            return False,queries
    return bool(qualified_changes),queries


def compare(b, change, use, context):
    f = b.f
    prop = context['compiled_property']
    rows, queries, worlds, gaps = [], [], [], []
    globally_excluded_paths=set()
    target = f.operations[use]['target']
    if f.operations[change]['target'] != target:
        raise Unsupported('cross_storage_context_without_binding')
    controls = [w['path'] for _, p in b.paths(change) for w in p['writes']
                if not unit_origin(b,change,w['path'])]
    relevant = [r for r in b.graph.request_reads(use) if any(
        selector_relation(r, c) == 'same_shape' for c in controls)]
    if not relevant and b.complete(change) and b.complete(use):
        return {'kind': 'causal_compare', 'change': change, 'observe': use,
                'observed_measure': 'financial_block', 'property_identity': prop['id'],
                'queries': [], 'local_errors': [], 'property_excluded': True,
                'scope_supported': False, 'financial_scope': {'reason': 'no_control_dependency_on_this_use'}}
    qualified_changes=[(pid,p)for pid,p in b.paths(change)if path_qualification(f,change,p)]
    if not qualified_changes:
        # Prefixes cannot manufacture a missing source qualification. This
        # stops an inapplicable query, not the still-open category obligation.
        return {'kind':'causal_compare','change':change,'observe':use,
                'observed_measure':'financial_block','property_identity':prop['id'],
                'queries':[],'worlds':[],'property_measurements':[],
                'local_errors':[{'reason':'intervention_has_no_source_bound_privileged_path',
                                 'operation':change,'not_a_negative_certificate':True}],
                'property_excluded':False,'scope_supported':False,
                'financial_scope':{'reason':'privilege_prerequisite_unresolved_or_not_applicable',
                                   'declared_use':use,'controls':relevant}}
    start=len(b.records)
    direct=direct_control_result(b,change,use,prop['category'])
    if direct:
        return {'kind':'causal_compare','change':change,'observe':use,'observed_measure':'financial_block',
                'property_identity':prop['id'],'queries':b.records[start:],'source_control_result':direct,
                'scope_supported':True,'property_excluded':False,'local_errors':[]}
    all_use_paths = list(b.paths(use))
    # Prefix search can satisfy guards, but cannot add an absent debit/credit
    # expression to a selected source path. Avoid spending the entire budget
    # preparing an entry whose modeled paths cannot realize this request (for
    # example ticket creation). Incomplete source remains an open dependency;
    # only a complete use receives this local, same-use exclusion.
    productive_candidates = []
    for pid, path in all_use_paths:
        moves = movements(b, use, path)
        if any(unit_origin(b, use, debit) and not native_only_position(b, use, debit)
               and selector_relation(debit, credit) == 'same_shape' and key(debit) != key(credit)
               for debit in moves['-'] for credit in moves['+']):
            productive_candidates.append(pid)
    if not productive_candidates:
        complete_use = b.complete(use)
        return {'kind':'causal_compare','change':change,'observe':use,
                'observed_measure':'financial_block','property_identity':prop['id'],
                'queries':[],'worlds':[],'property_measurements':[],
                'local_errors':[] if complete_use else [{
                    'reason':'no_supported_productive_baseline_path',
                    'operation':use,'unmodeled_continuations_remain_open':True}],
                'property_excluded':complete_use,'scope_supported':False,
                'financial_scope':{'reason':'selected_use_has_no_source_productive_transfer_candidate',
                    'declared_use':use,'productive_paths':[], 'complete':complete_use,
                    'prefix_search_cannot_create_a_missing_source_effect':True}}
    preserved,preservation_queries=preserved_by_source_transition(b,change,use,prop,qualified_changes)
    queries.extend(preservation_queries)
    if preserved:
        return {'kind':'causal_compare','change':change,'observe':use,
                'observed_measure':'financial_block','property_identity':prop['id'],
                'queries':queries,'worlds':[],'property_measurements':[],
                'local_errors':[],'property_excluded':True,'scope_supported':False,
                'financial_scope':{'reason':'source_transition_preserves_every_productive_input',
                    'declared_use':use,'all_change_paths':[pid for pid,_ in qualified_changes],
                    'positive_initial_domain_unchanged':True,
                    'other_controllers_or_uses_not_excluded':True}}
    from .goal_search import TargetSearch
    target_search = TargetSearch(b, use, {'measure':'productive_request', 'category':prop['category']})
    prefixes = []
    primary_families = {key(c['family']) for r in f.summaries.rows(use) for c in r['numeric_effects']
                        if c['holder'] is not None and 'debit' in c['may_directions']}
    alternatives = [o for o, entry in f.operations.items() if o != use and entry['target'] == target and
                    (any(key(c['family']) in primary_families and 'debit' in c['may_directions']
                        for r in f.summaries.rows(o) for c in r['numeric_effects']) or
                     any(c['operation']==o and c['mode']=='DELEGATECALL' and c['unresolved_implementation']
                         for c in f.call_summaries.rows.values()))]
    exact = b.complete(use) and all(b.complete(o) for o in alternatives)
    complete = all(continuation_frontier_covered(b,o) for o in [use]+alternatives)
    approximation_records=[]
    unrefined_unconditional=[]
    for reached_state in target_search:
        prefix = tuple(reached_state['prefix'])
        prefixes.append(prefix)
        # The exact checked frame sequence is reused. No writer re-enumeration.
        for chosen in [reached_state['frames']]:
            for cpid, cp in qualified_changes:
                b.check()
                role = path_qualification(f, change, cp)
                if not role:
                    continue
                try:
                    e = MechanismEncoder(f.lookup(use))
                    z = e.z
                    writes, premises, prefix_frames = [], [], []
                    for pf in chosen:
                        premises.append(encode_frame(e,pf))
                        premises.append(e.expr(pf['caller']) != 0)
                        writes += pf['writes']
                        prefix_frames.append(pf)
                    if key(writes) != key(reached_state['writes']):
                        raise Unsupported('goal_state_handoff_changed_ordered_writes')
                    cf = frame(f, change, cpid, len(prefix), writes)
                    roles, origins = fixed_role_terms(e, role, len(prefix))
                    from .behavior import ordered_clocks
                    base = z.And(*premises, encode_frame(e, cf), *roles, e.expr(cf['caller']) != 0,
                                 *ordered_clocks(e,len(prefix)+1))
                    before, after, request_objects, request_holders = [], [], [], []
                    local_approximations=[]
                    request = None
                    slot = len(prefix) + 1
                    exact_primary=set()
                    for pid, p in all_use_paths:
                        b.check()
                        deps = b.condition_dependencies(use, pid, p)
                        if deps['unknown_dependencies'] or deps['credential_dependencies']:
                            continue
                        snapshot=e.checkpoint()
                        try:
                            a = b.source_frame(use,pid,slot,writes)
                            c = b.source_frame(use,pid,slot,writes+cf['writes'])
                            usable0,cells=productive(b,e,a,use)
                            usable1,_=productive(b,e,c,use)
                            holders=[flow(e,f.lookup(use),a,cell)[0] for cell in cells]
                            typed_request=request or request_terms(b,e,a,use)
                        except Unsupported as error:
                            e.rollback(snapshot);exact=False
                            gaps.append({'operation':use,'path':pid,'reason':str(error),
                                'scope':'isolated primary continuation; siblings remain executable'})
                            continue
                        request_objects+=cells;request_holders+=holders
                        request=typed_request;before.append(usable0);after.append(usable1)
                        exact_primary.add(pid)
                    for pid,p in f.operation_paths(use):
                        if p['flow']=='reverted' or pid in exact_primary:continue
                        value,rec=may_continue(b,e,use,pid,writes+cf['writes'],slot,primary=True)
                        after.append(value);local_approximations.append(rec)
                        if z.is_true(z.simplify(value)):unrefined_unconditional.append(rec)
                    # A targeted outgoing restriction must address the actual
                    # debited holder, never only the recipient's address.
                    controlled_holders = []
                    for cell in [w['path'] for w in cf['writes']
                                 if any(selector_relation(w['path'], c) == 'same_shape' for c in relevant)]:
                        ks = keys(cell)
                        if len(ks) == 1:
                            controlled_holders.append(e.expr(ks[0]))
                    holder_matches = [h == c for h in request_holders for c in controlled_holders]
                    if prop['category'] == 'FCR-FREEZE':
                        if not holder_matches:
                            gaps.append({'path':cpid,'reason':'controlled_outgoing_holder_scope_unresolved',
                                         'controls':relevant,'request_objects':request_objects})
                            complete=False
                            continue
                        base = z.And(base, z.Or(*holder_matches))
                    if request_holders:
                        base = z.And(base, z.Or(*[h != e.expr(cf['caller']) for h in request_holders]))
                    alternate_rows = []
                    for other in alternatives:
                        known={pid for pid,_ in b.paths(other)}
                        for apid, ap in f.operation_paths(other):
                            b.check()
                            if ap['flow']=='reverted':continue
                            if path_qualification(f,other,ap):continue
                            # An incomplete *entry* can still contain an exact
                            # terminal path with no state/effect at all (for
                            # example a batch call with an empty array). That
                            # path cannot realize a positive request. Keeping
                            # it as an opaque continuation would invent a
                            # permanent possible bypass of every restriction.
                            # This exclusion is path-local; unresolved sibling
                            # loops, calls and delegated writes stay below.
                            no_effect = (apid in known and not ap.get('issues') and
                                not ap.get('evaluation_gaps') and not ap['writes'] and
                                not ap.get('sensitive_effects') and not any(
                                    b.condition_dependencies(other,apid,ap)[kind]
                                    for kind in ('unknown_dependencies','credential_dependencies')))
                            if no_effect:
                                value,error=z.BoolVal(False),'exact_terminal_path_without_productive_effect'
                            elif request is None:
                                value, error = None, 'primary_typed_request_mapping_ambiguous'
                            elif apid in known and b.complete(other):
                                snapshot=e.checkpoint()
                                try:
                                    value,error=alternate_continuation(b,e,other,apid,writes+cf['writes'],request,slot+10)
                                except Unsupported as error_:value,error=None,str(error_)
                                if value is None:
                                    e.rollback(snapshot);exact=False
                            else:
                                # Start incomplete entries with their necessary
                                # guard summary. Expanding a bounded loop body
                                # cannot close its unexpanded continuation, and
                                # can create exponentially repeated write terms.
                                # The overapproximation may prove no bypass; it
                                # can never prove a bypass or a negative verdict.
                                value,error=None,'source_continuation_requires_guard_overapproximation'
                            alternate_rows.append({'operation': other, 'path': apid, 'mapping': error or 'source_typed_same_request'})
                            if value is not None:
                                after.append(value)
                            elif error != 'privileged_assistance_is_not_an_ordinary_bypass':
                                value,rec=may_continue(b,e,other,apid,writes+cf['writes'],slot+10,request)
                                after.append(value);local_approximations.append(rec)
                                if z.is_true(z.simplify(value)):unrefined_unconditional.append(rec)
                    approximation_records += local_approximations
                    detail = {'operation': change, 'target': target, 'change': change, 'observe': use,
                              'change_path': cpid, 'prefix': list(prefix), 'property_identity': prop['id'],
                              'semantic_version': prop['semantic_version'], 'property_validated': True,
                              'same_request': True, 'objects': request_objects, 'controls': relevant,
                              'prefix_state_handoff': {'writes': writes, 'frames': prefix_frames,
                                  'reached_state':reached_state['id'], 'baseline_probe':reached_state['baseline_probe'],
                                  'exact_ordered_frame_reuse':True},
                              'alternative_request_mappings': alternate_rows,
                              'role_origins': origins, 'all_productive_paths_checked': complete,
                              'continuation_approximations':local_approximations,
                              'all_continuations_exact':exact and not local_approximations}
                    detail['initial_prefix_policy'] = 'constructor_only_for_explicit_prefix'
                    baseline = b._query(e, z.And(base, z.Or(*before)), 'baseline_usable', detail)
                    queries.append(baseline)
                    if not baseline['bounded_condition_confirmed']:
                        if not prefix and baseline.get('exclusion_certificate',{}).get('excludes_only_this_formula'):
                            globally_excluded_paths.add(cpid)
                        continue
                    # The productive before/after formulas share source inputs
                    # and state variables. No existential external failure is
                    # allowed to stand in for exclusion of successful routes.
                    if complete:
                        actual_after = z.Or(*after)
                        # One over-limit request does not establish FREEZE or
                        # PAUSE while a positive amount of the same holder's
                        # same resource remains usable. Keep the original
                        # request comparison as a mechanism observation and
                        # use this stronger range check for main classification.
                        if request is not None:
                            quantity = z.Int('remaining_positive_quantity_'+str(len(queries)))
                            actual_after = z.Exists([quantity], z.And(quantity>0, quantity<2**256,
                                z.substitute(actual_after,(request['amount'],quantity))))
                            detail['main_scope_range_check'] = 'same holder, resource, recipient and authority; any legal positive amount'
                        q = b._query(e, z.And(base, z.Or(*before), z.Not(actual_after)),
                                     'financial_block', detail)
                        queries.append(q)
                        if q['answer']=='unknown':
                            gaps.append({'reason':'quantified_blockage_not_decided_without_parameter_extraction',
                                         'query':q['id'],'not_a_negative_result':True})
                        if (not prefix and exact and not local_approximations and
                            not q['details'].get('pinned_UNSAT_not_a_universal_negative') and
                            q.get('exclusion_certificate',{}).get('excludes_only_this_formula')):
                            globally_excluded_paths.add(cpid)
                        rows.append({'baseline_probe': baseline['id'], 'block_probe': q['id'],
                                     'result': q['answer'], 'prefix': list(prefix)})
                        worlds.append({'prefix': [serialize_world(x, 'COMMON_PREFIX') for x in prefix_frames],
                                       'intervention': serialize_world(cf, 'INTERVENTION'),
                                       'same_request_slot': slot, 'actual_prefix_writes': writes})
                        if q['bounded_condition_confirmed']:
                            break
                except Unsupported as error:
                    gaps.append({'prefix': list(prefix), 'reason': str(error)})
            if any(q['label'] == 'financial_block' and q['bounded_condition_confirmed'] for q in queries):
                break
        if any(q['label'] == 'financial_block' and q['bounded_condition_confirmed'] for q in queries):
            break
        if unrefined_unconditional:
            # Changing the prefix cannot refine missing code/guard semantics
            # represented by True. Retain the concrete dependency/frontier;
            # do not spend the remaining budget replaying it or call it safe.
            target_search.record['stopped_on_unresolved_continuation']=unrefined_unconditional
            gaps.append({'reason':'unrefined_continuation_has_no_excluding_source_guard',
                         'continuations':unrefined_unconditional,'not_a_bypass_witness':True})
            break
        necessary={pid for pid,p in b.paths(change) if path_qualification(f,change,p)}
        if not prefix and necessary and necessary<=globally_excluded_paths and exact and b.complete(change):
            target_search.record['stopped_by_source_invariant_exclusion']=sorted(globally_excluded_paths)
            break
    # Collective scope needs a source-parametric common control. A mapped
    # per-person control remains a local restriction, regardless of two models.
    def common_guard(guard):
        roots = {c['root'] for c in relevant if not keys(c)}
        terms = list(guard.get('args', [])) if guard.get('op') in ('and', '&&') else [guard]
        return any(any(c['root'] in roots and not keys(c) for c in selectors(t)) and
                   not any(v.get('kind') in ('actual_sender','parameter') or
                           v.get('kind') == 'storage' and keys(v) for v in walk(t)) for t in terms)
    # No-effect return branches do not provide a productive escape route.
    productive_source_paths=[p for _,p in all_use_paths if movements(b,use,p)['-'] and movements(b,use,p)['+']]
    collective = bool(relevant) and bool(productive_source_paths) and all(
        any(common_guard(g) for g in p['guards']) for p in productive_source_paths)
    group=None
    if prop['category']=='FCR-PAUSE' and any(
            q.get('label')=='financial_block' and q.get('bounded_condition_confirmed')
            and q.get('details',{}).get('all_continuations_exact') for q in queries):
        group=ordinary_family(b,change,use,relevant)
    scope_supported = complete and (prop['category'] != 'FCR-PAUSE' or collective or bool(group))
    necessary={pid for pid,p in b.paths(change) if path_qualification(f,change,p)}
    excluded=bool(necessary) and necessary<=globally_excluded_paths and exact and b.complete(change)
    return {'kind': 'causal_compare', 'observed_measure': 'financial_block',
            'property_identity': prop['id'], 'change': change, 'observe': use,
            'queries': queries, 'worlds': worlds, 'comparisons': [], 'property_measurements': rows,
            'local_errors': gaps, 'scope_supported': scope_supported, 'alternative_uses': [],
            'property_excluded':excluded,
            'source_invariant_excluded_intervention_paths':sorted(globally_excluded_paths),
            'holder_consent_counterexamples': [], 'net_measurements': [],
            'target_state_search':target_search.record,
            'stopped_reason':target_search.record.get('stopped_reason'),
            'continuation_approximations':approximation_records,
            'financial_scope': {'target': target, 'declared_use': use, 'controls': relevant,
                                'productive_paths': [p for p, _ in all_use_paths], 'complete': complete,
                                'collective_source_control': collective, 'ordinary_holder_family':group, 'prefixes_tried': [list(x) for x in prefixes]}}

```

## source/src/pr_next_joint/investigation/call_summary.py

原文件SHA256 `3a84f924445e377fee3812392512eff76508db9e56e6d314127fcbff109ca1e2`

```python
"""Finite call-site effects and a checked monotone callback influence closure."""
import copy
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import walk, key
from pr_next_joint.frontend.storage import selectors


class CallSummaries:
    def __init__(self, facts):
        self.f = facts
        self.rows = {}
        self.events = []
        self.refinements = {}
        direct = {}
        edges = {}
        for oid, operation in facts.operations.items():
            direct[oid] = {w['raw']['path']['root'] for w in facts.writes.values() if w['operation'] == oid}
            if any(e['raw'].get('kind') in ('native_transfer','native_selfdestruct')
                   for e in facts.effects.values() if e['operation'] == oid):
                direct[oid].add(-1)  # separate abstract native-asset location
            edges[oid] = set()
            lookup = facts.lookup(oid)
            for pid, path in facts.operation_paths(oid):
                # The original paths already include resolved internal helpers.
                calls = {x.get('source', {}).get('ast_id'): x for x in path.get('issues', [])
                         if x.get('source', {}).get('ast_id') is not None}
                for call in path.get('read_calls', []):
                    calls.setdefault(call.get('source', {}).get('ast_id'), call)
                for call in path.get('resolved_calls', []):
                    calls.setdefault(call.get('source', {}).get('ast_id'), call)
                for effect in path.get('sensitive_effects', []):
                    calls.setdefault(effect.get('source', {}).get('ast_id'), effect)
                for site, record in calls.items():
                    # SELFDESTRUCT transfers the native balance without
                    # invoking beneficiary code. It is an effect, not a CALL
                    # site with possible callbacks or a callee failure value.
                    if record.get('kind')=='native_selfdestruct':
                        continue
                    node = lookup.nodes.get(site, {})
                    assembly = node.get('nodeType') == 'InlineAssembly' and record.get('call_mode') == 'DELEGATECALL'
                    if node.get('nodeType') != 'FunctionCall' and not assembly:
                        continue
                    expr = node.get('expression', {})
                    member = expr.get('memberName')
                    declaration = lookup.nodes.get(expr.get('referencedDeclaration'), {})
                    if not assembly and expr.get('nodeType') != 'MemberAccess' and record.get('kind') not in ('dangerous_external_call','native_transfer','native_selfdestruct'):
                        # Array construction, local arithmetic and internal
                        # helper failures are not external CALL instructions.
                        continue
                    typ = expr.get('typeDescriptions', {}).get('typeIdentifier', '')
                    if (declaration.get('nodeType') == 'FunctionDefinition' and
                            't_function_internal' in typ):
                        continue
                    mutability = declaration.get('stateMutability')
                    mode = ('DELEGATECALL' if assembly or record.get('call_mode')=='DELEGATECALL' or member in ('delegatecall', 'callcode') else
                            'STATICCALL' if member == 'staticcall' or mutability in ('view', 'pure') else 'CALL')
                    resolved_read = 'return_value' in record and record.get('binding') is not None
                    # Source byte intervals determine which writes precede the
                    # call, not the destination name or a model's category.
                    location = lookup.anchor(node)
                    before = record.get('callpoint_writes')
                    if before is None:
                        before = [w for w in path.get('writes', []) if
                              w.get('source', {}).get('file') == location.get('file') and
                              w.get('source', {}).get('start', 0) + w.get('source', {}).get('length', 0) <= location.get('start', 0)]
                    callbacks = [] if mode == 'STATICCALL' or resolved_read else [
                        other for other, entry in facts.operations.items()
                        if entry['target'] == operation['target'] and not entry.get('generated_getter')]
                    edges[oid].update(callbacks)
                    token = digest([operation['target'], pid, site, mode])
                    self.rows[token] = {
                        'id': token, 'operation': oid, 'path': pid, 'source': location, 'mode': mode,
                        'code_target': copy.deepcopy(expr.get('expression')),
                        'receiver_term':copy.deepcopy(record.get('receiver_term') or record.get('recipient')),
                        'storage_context': operation['target'] if mode == 'DELEGATECALL' else 'callee_separate',
                        'caller_relation': 'first callback sender equals actual callee; subsequent external callees are distinct source frames',
                        'callpoint_writes': before, 'callback_candidates': callbacks,
                        'callpoint_guards': copy.deepcopy(record.get('callpoint_guards', [])),
                        'callpoint_evaluations': copy.deepcopy(record.get('callpoint_evaluations', [])),
                        'callpoint_exact': 'callpoint_writes' in record,
                        'argument_sources': copy.deepcopy(node.get('arguments', [])),
                        'return_used': bool(any(x.get('reason') == record.get('reason') for x in path.get('issues', []))),
                        'exit_modes': ['callee_success', 'callee_revert'],
                        'outer_exit': path.get('flow'),
                        'catch_semantics': 'callee failure returns a value; outer source guard decides commit' if member in
                            ('call', 'send', 'delegatecall', 'callcode', 'staticcall') else
                            'high-level call failure propagates unless the source catches it',
                        'unresolved_implementation': not resolved_read,
                        'residuals': ([] if resolved_read else
                                      [{'kind': 'same_storage_unknown_implementation'}] if mode == 'DELEGATECALL'
                                      else [{'kind': 'external_return_or_exit', 'source': location}]),
                        'resolved_read_binding':record.get('binding') if resolved_read else None,
                        'conditional_code_binding':bool(resolved_read and record.get('binding')=='conditional_compiled_concrete_type')
                    }
        effects = {o: set(v) for o, v in direct.items()}
        rounds = 0
        while True:
            nxt = {o: set(effects[o]).union(*(effects[c] for c in edges[o])) for o in effects}
            rounds += 1
            self.events.append({'round': rounds, 'added': {o: sorted(nxt[o] - effects[o]) for o in effects if nxt[o] != effects[o]}})
            if nxt == effects:
                # This extra transfer is the actual post-fixed point check.
                verify = {o: set(nxt[o]).union(*(nxt[c] for c in edges[o])) for o in nxt}
                assert verify == nxt
                break
            effects = nxt
        self.effects = effects
        self.direct = direct
        self.rounds = rounds
        self.identity = digest([self.rows, {o: sorted(s) for o, s in effects.items()}])
        for row in self.rows.values():
            row['may_callback_writes'] = sorted(set().union(*(effects[o] for o in row['callback_candidates'])))
            row['fixed_point_transfer_verified'] = True
            # Possible callback paths keep their original source qualifications.
            row['callback_paths'] = [
                {'operation': o, 'path': pid, 'source_effect_sha256': digest([p['guards'],p['writes'],p['flow']]),
                 'source': 'effect_summaries.paths.' + pid, 'flow': p['flow']}
                for o in row['callback_candidates'] for pid, p in facts.operation_paths(o)]

    def effect_dependencies(self,row,effect,*,initiation=False):
        """Residuals that can change this path's selected operation or committed result."""
        from pr_next_joint.frontend.storage import selectors
        at=effect.get('where') or {}
        value=effect.get('write',{})
        guards=row['guards']
        origin_call=next((term for term in row['effects'] if term.get('kind')==effect.get('kind') and term.get('source')==at),None)
        if initiation and origin_call is not None and 'callpoint_guards' in origin_call:
            guards=origin_call['callpoint_guards']
        terms=[guards,value.get('value'),effect.get('cell')]
        if origin_call:
            terms.extend(origin_call.get(k) for k in ('recipient','amount','beneficiary','target') if origin_call.get(k) is not None)
        if any(n.get('kind') in ('unknown','external_return','native_call_success','credential_recovery') for n in walk(terms)):
            return ['condition_or_value_requires_external_result']
        roots={s['root'] for s in selectors(terms)}
        unresolved=[]
        for call in self.rows.values():
            if call['operation']!=row['operation'] or call['path']!=row['path'] or not call['unresolved_implementation']:continue
            same=call['source'].get('ast_id') is not None and call['source'].get('ast_id')==at.get('ast_id')
            if same and initiation and effect.get('kind')=='native_transfer':continue
            if call['mode']=='DELEGATECALL' or roots.intersection(call['may_callback_writes']):
                unresolved.append('same_scope_possible_storage_change')
            elif call['catch_semantics'].startswith('high-level'):
                unresolved.append('same_path_propagating_revert')
        for gap in row['residuals']:
            if gap.get('cell') and gap['cell'].get('root') not in roots:continue
            if gap.get('reason')=='multiple_address_keys_need_source_holder_binding' and initiation and not effect.get('cell'):continue
            loc=gap.get('source') or {}
            associated=bool(loc) and any(call['path']==row['path'] and call['source']==loc for call in self.rows.values())
            if gap.get('reason') and not associated:unresolved.append('unresolved_source_expression')
        return sorted(set(unresolved))

    def dependencies(self, oid, roots):
        roots = set(roots)
        out = []
        for row in self.rows.values():
            if row['operation'] != oid:
                continue
            relevant = row['mode'] == 'DELEGATECALL' or bool(roots.intersection(row['may_callback_writes']))
            out.append({'summary': row['id'], 'mode': row['mode'], 'relevant_callback_effect': relevant,
                        'matched_roots': sorted(roots.intersection(row['may_callback_writes'])),
                        'return_and_rollback_residuals': copy.deepcopy(row['residuals']),
                        'cannot_discharge_return_dependency_from_storage_independence': True})
        return out

    def refine(self, backend, oid, pid, roots):
        """Refine a finite may-effect closure at the *actual* invocation state.

        These are feasibility overapproximations, not attack witnesses. Unknown
        receivers allow later intermediary callers; they are never silently
        equated to the original user. UNSAT is consumed only with a source
        invariant/complete-domain certificate, and unresolved exits stay open.
        """
        from pr_next_joint.verification.program_encoding import MechanismEncoder
        from pr_next_joint.verification.sequence import qualify
        from pr_next_joint.verification.sequence import read
        from pr_next_joint.verification.source_worlds import frame, encode_frame
        from pr_next_joint.verification.expressions import Unsupported
        roots = set(roots)
        token = digest([self.identity, oid, pid, sorted(roots)])
        if token in self.refinements:
            return copy.deepcopy(dict(self.refinements[token], reused=True))
        f = self.f
        result = {'id': token, 'operation': oid, 'path': pid, 'roots': sorted(roots),
                  'calls': [], 'queries': [], 'may_effect_only': True, 'reused': False}
        for row in self.rows.values():
            if row['operation'] != oid or row['path'] != pid:
                continue
            backend.check()
            affected = roots.intersection(row['may_callback_writes'])
            item = {'summary': row['id'], 'mode': row['mode'],
                    'roots': sorted(affected), 'callbacks': [],
                    'return_exit_residuals': copy.deepcopy(row['residuals']),
                    'same_storage_unresolved': row['mode'] == 'DELEGATECALL' and row['unresolved_implementation']}
            result['calls'].append(item)
            if not affected:
                item['callback_projection'] = 'disjoint_after_checked_fixed_point'
                continue
            if not row['callpoint_exact']:
                item['callback_projection'] = 'source_callpoint_not_precisely_lowered'
                continue
            before = [qualify(w, 0) for w in row['callpoint_writes']]
            for candidate in row['callback_candidates']:
                if not roots.intersection(self.direct[candidate]):
                    continue
                for cpid, path in f.operation_paths(candidate):
                    backend.check()
                    rec = {'operation': candidate, 'path': cpid, 'flow': path['flow']}
                    item['callbacks'].append(rec)
                    if path['flow'] == 'reverted':
                        rec['state'] = 'callback_writes_rolled_back'
                        continue
                    if path.get('issues') or path.get('evaluation_gaps') or path['flow'] not in ('normal', 'returned'):
                        rec['state'] = 'may_influence_with_precise_path_residual'
                        continue
                    try:
                        e = MechanismEncoder(f.lookup(candidate)); z = e.z
                        cf = frame(f, candidate, cpid, 1, before)
                        prefix = [e.expr(qualify(g, 0)) for g in row['callpoint_guards']]
                        # No assertion about an unknown external return is
                        # needed to overapproximate the possible callback.
                        actor = e.expr(cf['caller'])
                        changes = [e.expr(read(w['path'],before+cf['writes'],e.lookup)) !=
                                   e.expr(read(w['path'],before,e.lookup)) for w in cf['writes']
                                   if w['path']['root'] in roots]
                        if -1 in roots:
                            changes += [e.expr(fx['amount'])>0 for fx in cf['effects']
                                        if fx.get('amount') is not None]
                        formula = z.And(*prefix, encode_frame(e, cf), actor != 0, z.Or(*changes))
                        details = {'operation': oid, 'callsite': row['source'], 'callback': candidate,
                                   'use_path': cpid, 'callpoint_writes': before,
                                   'callback_caller': 'arbitrary onward caller overapproximation; first hop checked separately',
                                   'roots': sorted(affected), 'only_may_feasibility': True,
                                   'actual_net_change_required':True,
                                   'property_validated': False}
                        receiver=row.get('receiver_term')
                        if receiver:
                            direct_formula=z.And(formula,actor==e.expr(read(qualify(receiver,0),before,e.lookup)))
                            direct_query=backend._query(e,direct_formula,'direct_callback_influence',dict(details,
                                callback_caller='exact callee address at callpoint',receiver=receiver))
                            result['queries'].append(direct_query)
                            rec['direct_callee_probe']=direct_query['id']
                        query = backend._query(e, formula, 'callback_influence', details)
                        result['queries'].append(query)
                        rec['probe'] = query['id']
                        excluded = query['answer'] == 'unsat' and (
                            query.get('exclusion_certificate', {}).get('excludes_only_this_formula') or
                            query.get('details', {}).get('prestate', {}).get('global_reachability_exhausted'))
                        rec['state'] = 'source_invariant_excludes_callback' if excluded else 'may_influence'
                        rec['midstate_and_guard_formula'] = query['formula_ref']
                    except Unsupported as error:
                        rec['state'] = 'may_influence_with_precise_path_residual'
                        rec['reason'] = str(error)
            records = item['callbacks']
            item['callback_projection'] = ('excluded_on_all_overapproximated_entries' if records and
                all(r['state'] in ('callback_writes_rolled_back', 'source_invariant_excludes_callback') for r in records)
                else 'may_influence')
            # This final projection check preserves every transitive may-root
            # unless all its real source callbacks were actually excluded.
            item['projected_roots'] = [] if item['callback_projection'].startswith('excluded_') else sorted(affected)
        self.refinements[token] = copy.deepcopy(result)
        return result

    def record(self):
        return {'identity': self.identity, 'calls': self.rows, 'rounds': self.rounds,
                'propagation': self.events, 'transfer_verified': True,
                'refinements': self.refinements,
                'precision': 'finite may-effect union; path feasibility and unknown external exits remain separate'}

```

## source/src/pr_next_joint/investigation/candidates.py

原文件SHA256 `4fed11855389d608913c1e7ddcb384f0c1d8c386fb3c03acc29426dbb3644c3c`

```python
"""Small source-located questions about applied extra effects and independent exits."""
from pr_next_joint.frontend.path_ir import walk, key
from pr_next_joint.frontend.storage import selectors
from pr_next_joint.core import digest


def source_candidates(facts):
    result=[]
    for oid,op in sorted(facts.operations.items(),key=lambda x:(x[1]['target'],x[1]['source']['start'],x[0])):
        if op.get('generated_getter'):continue
        lookup=facts.lookup(oid);fn=lookup.function(op['function']);origin=fn.get('scope')
        bases=lookup.nodes.get(origin,{}).get('linearizedBaseContracts',[])[1:]
        peers=[n for c in bases for n in lookup.nodes[c].get('nodes',[]) if n.get('nodeType')=='FunctionDefinition'
               and n.get('scope')!=origin and n.get('body') and n.get('name')==fn.get('name') and fn.get('name')
               and len(n.get('parameters',{}).get('parameters',[]))==len(fn.get('parameters',{}).get('parameters',[]))]
        parent_roots={x.get('referencedDeclaration') for p in peers for n in walk(p.get('body') or {})
            if n.get('nodeType')=='Assignment' for x in walk(n.get('leftHandSide') or {})}
        extra=[];exits=[]
        span=lookup.anchor(fn)
        for pid,p in facts.operation_paths(oid,True):
            for w in p['writes']:
                loc=w['source']
                if peers and loc['file']==span['file'] and span['start']<=loc['start']<span['start']+span['length'] and w['path']['root'] not in parent_roots:
                    extra.append({'path':pid,'position':w['path'],'value':w['value'],'source':loc})
            for effect in p.get('sensitive_effects',[]):
                if 'selfdestruct' in str(effect.get('kind','')) or 'selfdestruct' in str(effect.get('operation','')):
                    exits.append({'path':pid,'effect':effect})
        # Actual source effects use a typed `selfdestruct` kind in this frontend.
        groups={}
        for item in extra:
            identity=('applied_extra_effect',key(item['source']),key(item['position']))
            groups.setdefault(identity,{})[key(item)]=item
        for item in exits:
            identity=('independent_sensitive_exit',key(item['effect'].get('source')),item['effect'].get('kind'))
            groups.setdefault(identity,{})[key(item)]=item
        for identity,occurrences in groups.items():
            kind=identity[0];items=list(occurrences.values())
            row={'operation':oid,'target':op['target'],'kind':kind,
                 'extra_effects':items if kind=='applied_extra_effect' else [],
                 'sensitive_exits':items if kind=='independent_sensitive_exit' else [],
                 'candidate_requires_assessment':True,'not_counterevidence':True}
            row['id']='candidate_'+digest(row)[:16];result.append(row)
    return result


def source_duty(rules, effect, kind):
    """Trace an applied write back to independent program uses of its authority or unit."""
    from .ledger import grant_for, unit_origin, native_only_position
    from .source_opinion import office_use, office_guard, feasible_source_guards, role_ids
    from .policy_binding import conjuncts
    from .summary import holder, local_delta
    from pr_next_joint.frontend.storage import keys, value_type, selector_relation
    d=rules.effects[effect]; f=rules.f; oid=d['oid']; lk=f.lookup(oid)
    if kind=='termination':
        # The initial bool value and a separately governed public completion
        # distinguish the ordinary completed phase from discretionary early termination.
        from .initial_state import initial_for_lookup
        for pid in d.get('branches',{}):
            row=f.summaries.paths[pid]
            if not row['committing'] or f.call_summaries.effect_dependencies(row,d): continue
            for branch in (v for g in row['guards'] for v in conjuncts(g)):
                flag=branch['args'][0] if branch.get('op')=='!' and len(branch.get('args',[]))==1 else branch
                if flag.get('kind')!='storage' or keys(flag) or value_type(flag,lk)!='bool': continue
                enabled=branch is flag
                initial=(initial_for_lookup(lk) or {}).get('declarations',{}).get(flag['root'],{})
                # A non-default initial stage must be known, never guessed.
                if initial.get('explicit_initializer') or initial.get('constructor_writes'): continue
                governors=[]; stable=True
                for peer in rules.by_decl.get(rules.obj(d['target'],flag['root']),()):
                    pd=rules.effects[peer]; pr=f.summaries.paths[pd['path']]
                    if not pr['committing']:continue
                    roles=role_ids(rules.inv,pd['oid'],pr)
                    if not roles or pr['residuals']:stable=False;break
                    governors.append((pd,roles))
                if not stable or not governors:continue
                finalizer=next((pd for pd,_ in governors if pd['write']['value'].get('value') is True),None)
                if not finalizer:continue
                sibling=any(other!=oid and f.operations[other]['target']==d['target'] and
                    any(r['committing'] and not r['residuals'] and any(t.get('kind')=='native_selfdestruct' for t in r['effects'])
                        and any(key(g)==key(flag) for g in r['guards']) for r in f.summaries.rows(other))
                    for other in f.operations)
                if enabled or sibling or (not enabled and finalizer):
                    return dict(family='managed_lifecycle', duty='governed_active_phase', path=pid,
                                support=finalizer['where'], phase='completed' if enabled else 'active', phase_guard=key(branch),
                                controller_guarded=bool(role_ids(rules.inv,oid,row)))
        return None
    if 'write' not in d or rules.overwritten(effect):return None
    row=f.summaries.paths[d['path']];w=d['write'];cell=w['path']
    from .source_opinion import dependency_state
    if not row['committing'] or dependency_state(rules.inv,row,d)!='proved_irrelevant':return None
    if not feasible_source_guards(row['guards']):return None
    sign,qty=local_delta(w);idx=keys(cell)
    if kind=='account_movement' and sign=='-':
        from .shared_effect_bridge import independent_holder_debit
        return independent_holder_debit(rules, effect)
    if kind=='credit':
        acct=holder(cell,lk)
        if not acct or acct.get('kind') not in ('actual_sender','parameter'):return None
        if not qty or not any(v.get('kind')=='parameter' for v in walk(qty)):return None
        # A source debit or paid purchase supplies consideration on this path.
        if row['effects'] or any(local_delta(v)[0]=='-' for v in row['ordered_writes']):return None
        if any(n.get('kind') in ('transaction_value','unknown','external_return') for n in walk([row['guards'],qty])):return None
        from .ledger import same_unit_transfers
        from .initial_state import family
        use=same_unit_transfers(f,d['target'],include_checked_arithmetic=True).get(family(cell))
        if not use or not unit_origin(rules.inv.backend,oid,cell) or native_only_position(rules.inv.backend,oid,cell):return None
        # The different, actually conserved holder transfer supplies the duty
        # evidence. The unbacked write itself cannot supply its own norm.
        support=next((r['source'] for r in use if r['operation']!=oid),None)
        if not support:return None
        return dict(family='unbacked_issuance',duty='conservation_of_disposable_holder_unit',
                    path=row['path'],support=support)
    if kind=='qualification' and not idx and value_type(cell,lk)=='bool':
        # A write to a business flag is a phase duty only if the same declaration
        # governs a committed sensitive use and an independently governed writer
        # establishes who controls that transition.
        dependencies=f.summaries.dependencies
        for eid in dependencies.readers.get((d['target'],cell['root']),()):
            use=dependencies.rows[eid]['use']
            if use==oid:continue
            for branch in f.summaries.rows(use):
                if not branch['committing'] or branch['residuals'] or not any(
                        s['root']==cell['root'] for s in selectors(branch['guards'])):continue
                relevant=any(x.get('kind') in ('native_transfer','native_selfdestruct') for x in branch['effects']) or any(
                    holder(v['path'],f.lookup(use)) is not None and local_delta(v)[0] for v in branch['ordered_writes'])
                if not relevant:continue
                peers=[rules.effects[p] for p in rules.by_decl.get(rules.obj(d['target'],cell['root']),()) if rules.effects[p]['oid']!=oid]
                for peer in peers:
                    if not peer.get('clean') or not role_ids(rules.inv,peer['oid'],f.summaries.paths[peer['path']]):continue
                    value=w['value'];governed=peer['write']['value']
                    if value.get('kind')!='parameter' and key(value)!=key(governed):continue
                    return dict(family='managed_phase',duty='separately_governed_effect_transition',path=row['path'],
                                support=peer['where'],use=use)
    if kind!='qualification':return None
    if len(idx)==2 and w['value'].get('kind') in ('parameter','literal') and not sign:
        # The same declaration in the enforced grant identifies the issuer index;
        # swapping the two address keys is not a source-compatible permission.
        deps=f.summaries.dependencies
        uses={deps.rows[e]['use'] for e in deps.readers.get((d['target'],cell['root']),())}
        for use in sorted(uses-{oid}):
            if not rules.remaining():return None
            for pid,raw in f.operation_paths(use,True):
                for output in raw['writes']:
                    payer=holder(output['path'],f.lookup(use))
                    if not payer or local_delta(output)[0]!='-':continue
                    gr=grant_for(rules.inv.backend,use,raw,output['path'])
                    if not gr or selector_relation(gr,cell)!='same_shape':continue
                    issuer=next((i for i,t in enumerate(keys(gr)) if key(t)==key(payer)),None)
                    if issuer is not None:
                        return dict(family='grant_then_use',duty='holder_issued_grant', path=row['path'],
                                    issuer=idx[issuer]['kind'], issuer_key=issuer, support=output['source'],use=use)
    if (not idx and value_type(cell,lk) in ('address','address payable') and w['value'].get('kind') in ('parameter','actual_sender')
        or len(idx)==1 and w['value'].get('value') is True):
        use=office_use(rules.inv,oid,cell)
        if use:return dict(family='grant_then_use',duty='guarded_downstream_use', path=row['path'],
                           support=f.operations[use]['source'],use=use)
    return None


def investigate(inv):
    inv.candidate_trace=[]
    if inv.f.options.scope=='AC':
        rules=inv.semantics.rules
        # One question for each distinct occurrence. Untyped questions do
        # not inherit a model opinion; a real scoped policy can attach later.
        for e,kind in getattr(rules,'sensitive_effects',{}).items():
            if not inv.program_remaining():break
            oid=rules.effects[e]['oid']
            if not any(inv.root(q)==oid and e in q['current'].get('_scope_effects',()) for q in inv.issues.values()):
                rules.create_consumer(oid,'AC',{e})
    if inv.f.options.scope=='FCR':
        from .shared_effect_bridge import financial_refinements
        rules = inv.semantics.rules
        for oid, category, effects in financial_refinements(rules):
            if not inv.program_remaining():
                break
            rules.create_consumer(oid, category, effects)

    for candidate in inv.f.source_candidates:
        oid=candidate['operation'];rules=inv.semantics.rules
        positions={(key(w['position']),key(w['source'])) for w in candidate['extra_effects']}
        wanted={e for e in rules.by_operation.get(oid,()) if 'cell' in rules.effects[e] and (key(rules.effects[e]['cell']),key(rules.effects[e]['where'])) in positions}
        # A single terminating effect with no writes needs no second host question when
        # the existing reading already addresses that exact source entry and policy.
        exit_locs={key(x['effect'].get('source')) for x in candidate['sensitive_exits']}
        wanted.update(e for e in rules.by_operation.get(oid,()) if rules.effects[e].get('kind')=='native_selfdestruct'
                      and key(rules.effects[e]['where']) in exit_locs)
        existing=[q for q in inv.issues.values() if inv.root(q)==oid and
                  wanted and set(q['current'].get('_scope_effects',()))==wanted]
        if existing:
            q=existing[0];q['host_source_candidate']=candidate
            inv.enqueue(q['id'],'inspect',{'operation':oid,'enhance':False},1,'inspect applied extra effect against the existing explanation')
        else:
            item={'id':'host_'+candidate['id'],'anchors':[inv.catalog.name(oid)],'assessment':'investigate',
                  'category':'AC' if inv.f.options.scope=='AC' else 'ADDITIONAL',
                  'claim':'The actual applied entry has a committed '+candidate['kind']+'. Determine the affected subject, authorization and asset, and whether the existing explanation covers this effect.',
                  '_host_source_question':True,'_scope_effects':sorted(wanted)}
            inv.accept({'issues':[item],'reviewed':[],'diagnostics':[],'usable_analysis':True},host_target=candidate['target'])
            q=inv.issues.get(item['id'])
            if q:q['host_source_candidate']=candidate
        inv.candidate_trace.append({**candidate,'question':q['id'] if q else None,
            'state':'queued' if q else 'unresolved_binding','generated_risk_claim':False})


def investigate_obligations(inv,report):
    """Give omitted semantic obligations a place in the existing follow-up.

    No extra session, risk label or gold-driven ordering. Shared object groups
    send one source question; unselected entries remain in the coverage ledger.
    """
    scope=report['task_analysis']['reading_scope'];created=[]
    rules=inv.semantics.rules
    for request in scope.get('refinement_requests',()):
        oid=request['operation'];category=request['category'];effects=set(request['effects'])
        if not effects or not inv.program_remaining():continue
        if any(inv.root(q)==oid and (q.get('property') or q['current']).get('category')==category and
               effects<=set(q['current'].get('_scope_effects',())) for q in inv.issues.values()):continue
        q=rules.create_consumer(oid,category,effects)
        if not q:continue
        q['host_obligation_question']={'selected_operation':oid,'category':category,'other_entries_not_marked_complete':True}
        created.append(q['id'])
        inv.candidate_trace.append({'operation':oid,'target':inv.f.operations[oid]['target'],'question':q['id'],
            'kind':'unresolved_source_obligation','state':'queued','generated_risk_claim':False})
    return created

```

## source/src/pr_next_joint/investigation/cli.py

原文件SHA256 `261e767348ac7fa261ee77971f497508193da89b676b3e3b282b8f18dc7d6abc`

```python
"""Original compiled source -> source-led semantic investigation (offline stage two)."""
import argparse,json,hashlib,threading,time,traceback,sys
from pathlib import Path
from contextlib import nullcontext
from .contracts import Options,VERSION,write
from .program import Facts
from .graph import ProgramGraph
from .context import Catalog,SourceContext
from .engine import analyze
from .report import evaluation_projection
from .decision_output import context_summary,receipt

def load_program(root,unit,task,config=None,targets=None,engineering=None):
    options=Options(scope=task,**(config or {}))
    if engineering:
        d=Path(engineering);bundle=json.loads((d/'ProgramBundle.json').read_bytes());native=json.loads((d/'native_ssa.json').read_bytes())
        texts={p.relative_to(d/'sources').as_posix():p.read_text(encoding='utf-8-sig') for p in (d/'sources').rglob('*.sol')}
        sources=[{'file':n,'content':s,'sha256':hashlib.sha256(s.encode()).hexdigest()} for n,s in texts.items()]
        receipt={'engineering_fixture':True,'compiler_artifacts_reused':True,'compiler_invocations':0,'native_extractions':0}
        f=Facts(bundle,native,sources,options,targets);return f,receipt
    from pr_next_joint.frontend.dataset_intake import load_compiled_unit
    u=load_compiled_unit(Path(root).resolve(),Path(unit).resolve())
    return Facts(u['bundle'],u['native'],u['sources'],options,targets or u['selected_targets'],u['description']),u['receipt']

def run(args,*,responses=None,client_factory=None,deadline=None):
    source_root=Path(__file__).resolve().parents[3];sys.path.insert(0,str(source_root/'runtime'))
    from reference_counter import Counter
    from bridge import FixtureClient,UsageJournal
    out=Path(args.out).resolve();out.mkdir(parents=True,exist_ok=True)
    if any(out.iterdir()):raise ValueError('fresh_output_required')
    config=json.loads(Path(args.config).read_text(encoding='utf-8-sig')) if args.config else {}
    if config.get('live_model_authorized') or config.get('live_authorized'):raise ValueError('stage2_no_live_authorization')
    if set(config)-{'method','options','live_model_authorized','notes'}:raise ValueError('unknown_config_keys')
    f,intake=load_program(args.root,args.compiled_unit,args.task,config.get('options'),args.target,args.engineering_compiled)
    write(out/'intake_receipt.json',intake);counter=Counter(args.tokenizer)
    if args.phase=='prepare':
        graph=ProgramGraph(f);ctx=SourceContext(f,Catalog(f,graph),counter);messages,manifest=ctx.messages()
        write(out/'prepared_receipt.json',{'manifest':context_summary(manifest),'host_identity':f.identity,**receipt(messages,'prepared_model_request')})
        return {'prepared_only':True,'real_model_calls':0,'manifest':context_summary(manifest)}
    if responses is None:responses=[Path(p).read_text(encoding='utf-8-sig') for p in (args.fixture_response,args.fixture_feedback) if p]
    if client_factory is not None:
        broker=nullcontext();client=client_factory(f,args,counter)
    elif args.offline_bridge:
        raise ValueError('file_bridge_not_available_in_decision_only_build')
    else:broker=nullcontext();client=FixtureClient(responses,args.case_id)
    with broker:report=analyze(f,out/'analysis',counter=counter,client=client,deadline=deadline)
    if client_factory is not None:write(out/'usage_journal.json',client.accounting())
    else:
        journal=UsageJournal(out/'usage_journal.json')
        for row in report['usage']['attempts']:journal.fixture(args.case_id,row['index'],row['input_tokens'])
    write(out/'prediction_export.json',evaluation_projection(report));return report

def parser():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root');p.add_argument('--compiled-unit');p.add_argument('--engineering-compiled')
    p.add_argument('--target',action='append');p.add_argument('--task',choices=('AC','FCR'),required=True)
    p.add_argument('--out',required=True);p.add_argument('--config');p.add_argument('--tokenizer',required=True)
    p.add_argument('--fixture-response');p.add_argument('--fixture-feedback');p.add_argument('--offline-bridge',action='store_true')
    p.add_argument('--phase',choices=('prepare','analyze'),default='analyze');p.add_argument('--case-id',default='engineering')
    return p

def main(argv=None):
    args=parser().parse_args(argv);started=time.monotonic();stop=threading.Event()
    def heartbeat():
        while not stop.wait(20):print(json.dumps({'phase':'offline_engineering','elapsed_seconds':round(time.monotonic()-started),'actual_model_submissions':0}),flush=True)
    thread=threading.Thread(target=heartbeat,daemon=True);thread.start();result=1
    try:
        report=run(args);print(json.dumps({'findings':len(report.get('findings',[])),'prepared_only':report.get('prepared_only',False),'actual_model_submissions':0}),flush=True);result=0
    except Exception as error:
        out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
        write(out/('technical_error_'+str(time.time_ns())+'.json'),{'error':type(error).__name__,'error_sha256':hashlib.sha256(str(error).encode()).hexdigest(),'risk_prediction_synthesized':False})
        print('工程入口停止：'+type(error).__name__,flush=True)
    finally:
        stop.set();thread.join(1);print('运行结束：'+('已保存离线工程结果' if result==0 else '入口异常，错误原件已保存')+'；实际模型调用0；目录 '+str(Path(args.out).resolve()),flush=True)
    return result

```

## source/src/pr_next_joint/investigation/comparison.py

原文件SHA256 `0a715f4212f15412faa3f6455d09b3238af6eb08527f08ba7976045918700c43`

```python
"""Map an already nominated finding to one JANUS capability; never generate a candidate."""
import re
from pr_next_joint.frontend.path_ir import key,walk
from pr_next_joint.frontend.storage import keys,selectors,selector_relation,value_type
from .ledger import movements,grant_for,unit_origin
from .properties import privileged_paths
from .prestate import impossible_role,state_facts
from .request_scope import claim_entries,linked_controls
from .roles import path_qualification
from .summary import holder as bound_holder


GUIDANCE = """FCR blind reading: consider all five conditional capabilities. Unassigned typed address/number inputs may vary under the host state model; explicit initialization, constructors and committed transitions remain binding. Conditional capability does not assert deployment reachability. TRANSFER: privilege can move tokens of another holder without the applicable holder approval. A public use may depend on a privileged upstream change. MINT: a privileged actor can issue tokens to itself or a beneficiary it can control; no other holder debit, user request or price loss is needed. DESTROY: privilege destroys another holder's tokens; distinguish self-burn or actual matching settlement. FREEZE: control can stop outgoing token transfers of a designated holder. PAUSE: common control can stop all ordinary holders transferring tokens; one address, amount, deposit or log failure is insufficient. Administrative purpose, compliance, airdrop, or a cap alone do not negate a capability. Check any claimed consent or compensation against this holder, asset, amount, path and phase. Keep other source-backed financial/business risks as additional, describe the affected use. Keep constructor configuration and runtime power distinct. A pointed transfer, mint, burn or restriction need not be named like those operations."""


def same(a,b):
    return selector_relation(a,b)=='same_shape'


def transfer_shapes(b,oid,path):
    from .summary import local_delta
    moves=movements(b,oid,path)
    # An alias-sensitive post-state may move in either direction. Where actual
    # assignments determine a local sign, preserve the debit/credit orientation.
    def possible(cell, sign):
        signs=[local_delta(w)[0] for w in path['writes'] if key(w['path'])==key(cell)]
        return not signs or None in signs or sign in signs
    return [(d,c) for d in moves['-'] for c in moves['+'] if same(d,c) and key(keys(d))!=key(keys(c))
            and possible(d,'-') and possible(c,'+')]


def ledger_routes(b,target):
    if not hasattr(b,'_comparison_routes'):b._comparison_routes={}
    sem=getattr(b,'semantics',None)
    token=(target,sem.dependency_identity([o for o,e in b.f.operations.items() if e['target']==target]) if sem else 0)
    if token in b._comparison_routes:return b._comparison_routes[token]
    routes=[]
    for oid,op in b.f.operations.items():
        if op['target']!=target:continue
        for pid,path in b.paths(oid):
            for debit,credit in transfer_shapes(b,oid,path):
                # The two address-bound entries must have an independently grounded
                # financial use or match the actual standard token transfer interface.
                funded=unit_origin(b,oid,debit)
                abi=op['function'] in ('transfer(address,uint256)','transferFrom(address,address,uint256)')
                if funded or abi:
                    routes.append({'operation':oid,'path':pid,'debit':debit,'credit':credit,'grounding':funded or 'standard_ABI_and_matching_ledger_effect'})
    b._comparison_routes[token]=routes
    return routes


def gates(path,cell):
    """Necessary Boolean controls and conditional alternatives of other global Booleans."""
    def includes(term):
        if term.get('kind')=='storage':return key(term)==key(cell)
        op=term.get('op');args=term.get('args',[])
        if op=='!' and len(args)==1:
            if args[0].get('op') in ('and','&&'):return False
            return includes(args[0])
        if op in ('and','&&'):return any(includes(x) for x in args)
        if op in ('or','||'):
            return any(includes(x) for x in args) and all(includes(x) or
                x.get('kind')=='storage' and not keys(x) for x in args)
        if op in ('==','!=','<','<=','>','>='):return any(key(s)==key(cell) for s in selectors(term))
        return False
    return any(includes(g) for g in path['guards'])


def can_restrict(b,change,use,p,cell):
    """Check the polarity of the control on this actual outgoing route."""
    def blocked_value(g):
        if key(g)==key(cell):return False
        if g.get('op')=='!' and len(g.get('args',[]))==1:
            inner=blocked_value(g['args'][0])
            return None if inner is None else not inner
        if g.get('op') in ('and','&&','or','||'):
            choices={v for child in g.get('args',[]) for v in [blocked_value(child)] if v is not None}
            if len(choices)==1:return choices.pop()
        return None
    needs={v for g in p['guards'] for v in [blocked_value(g)] if v is not None}
    if len(needs)!=1:return False
    needed=needs.pop()
    for _,cp in b.paths(change):
        guards=cp['guards']
        if not path_qualification(b.f,change,cp):continue
        for w in cp['writes']:
            if not same(cell,w['path']):continue
            term=w['value']
            if term.get('kind')=='literal' and str(term.get('value')).lower()==str(needed).lower():return True
            if term.get('kind')=='parameter' and term.get('type')=='bool':
                if not any(key(term)==key(n) for g in guards for n in walk(g)):return True
    return False


def business_only(item):
    text=item.get('claim','')+' '+str(item.get('revision_reason',''))
    purpose=re.search(r'\b(?:maintenance|emergency|compliance|sanctioned|airdrop|administrative purpose|legitimate admin|incident response)\b',text,re.I)
    return bool(purpose)


def literal_balance_zero(p,lookup):
    return [w['path'] for w in p['writes'] if len(keys(w['path']))==1 and value_type(w['path'],lookup).startswith('uint')
            and w['value'].get('kind')=='literal' and str(w['value'].get('value'))=='0']


def conjuncts(g):
    if g.get('op') in ('and','&&'):
        for a in g['args']:yield from conjuncts(a)
    else:yield g


def holder_only(b,oid,p,debit):
    holder=bound_holder(debit,b.f.lookup(oid))
    if holder is None:return False
    if holder.get('kind')=='actual_sender':return True
    return any(g.get('op')=='==' and {key(a) for a in g.get('args',[])}=={key(holder),key({'kind':'actual_sender'})}
               for guard in p['guards'] for g in conjuncts(guard))


def consent_gate(b,oid,p,debit):
    holder=bound_holder(debit,b.f.lookup(oid))
    if holder is None:return False
    # Only a positive holder -> requester grant on the actual committing path,
    # for which the holder controls issuance. A controller's own permission is distinct.
    for raw in p['guards']:
        for g in conjuncts(raw):
            if g.get('kind')!='storage' or value_type(g,b.f.lookup(oid))!='bool':continue
            pos=keys(g)
            if len(pos)!=2 or key(pos[0])!=key(holder) or pos[1].get('kind')!='actual_sender':continue
            writers=[w for w in b.f.writes.values() if b.f.operations[w['operation']]['target']==b.f.operations[oid]['target'] and same(g,w['raw']['path'])]
            if writers and all(keys(w['raw']['path'])[0].get('kind')=='actual_sender' for w in writers):return True
    return allowance_covers(b,oid,p,debit)


def allowance_covers(b,oid,p,debit):
    grant=grant_for(b,oid,p,debit)
    if grant is None:return False
    writes=[w for w in p['writes'] if key(w['path'])==key(debit)]
    if len(writes)!=1:return False
    expr=writes[0]['value'];args=expr.get('args',[])
    if expr.get('op')!='-' or len(args)!=2 or key(args[0])!=key(debit):return False
    # A grant also installable by an outsider/controller does not certify holder consent.
    for w in b.f.writes.values():
        other=w['operation']; dst=w['raw']['path']
        if b.f.operations[other]['target']!=b.f.operations[oid]['target'] or not same(dst,grant):continue
        if keys(dst)[0].get('kind')=='actual_sender':continue
        val=w['raw']['value'];gargs=val.get('args',[])
        if val.get('op')=='-' and gargs and key(gargs[0])==key(dst):continue
        return False
    return any(n.get('op')=='>=' and len(n.get('args',[]))==2 and key(n['args'][0])==key(grant) and key(n['args'][1])==key(args[1])
               for guard in p['guards'] for n in [guard,*([*guard.get('args',[])] if guard.get('op') in ('and','&&') else [])])


def _direct_results(inv,root,category,q=None):
    """Match actual original-program queries, not a label, issue ID or raw UNSAT."""
    target=inv.f.operations[root]['target']
    from .initial_state import domain, initial_for_lookup
    selected_domain=domain(inv.f.lookup(root)); initial=initial_for_lookup(inv.f.lookup(root))
    predicate='positive_credit_to_caller' if category=='FCR-MINT' else 'negative_delta_of_other_nonzero_holder'
    results={}
    for evidence_id,record in inv.evidence.items():
        if q is not None and evidence_id not in q['evidence']:continue
        if record.get('observed_measure')!='direct_effect' or (record.get('change'),record.get('observe'))!=(root,root):continue
        qs={x['id']:x for x in record.get('queries',[])}
        for row in record.get('property_measurements',[]):
            base=qs.get(row.get('feasible_probe'),{});effect=qs.get(row.get('result_probe'),{})
            d=base.get('details',{}); pid=d.get('use_path'); cell=d.get('ledger')
            if (base.get('label')!='local_premises_feasible' or base.get('abstract_hash') or
                    d.get('target')!=target or d.get('operation')!=root or d.get('category_hypothesis')!=category or
                    d.get('predicate')!=predicate or d.get('argument_domain') not in ('all_source_inputs_on_this_committing_path','recorded_claim_aliases') or
                    pid not in inv.f.paths or inv.f.paths[pid]['operation']!=root or not cell or not d.get('unit')):continue
            if d.get('argument_domain')=='recorded_claim_aliases':
                ctx=((q or {}).get('plan',{}).get('observation_choice',{}).get('selected') or {}).get('context',{})
                if not ctx.get('request_aliases') or key(d.get('claim_aliases'))!=key(ctx['request_aliases']):continue
            state=d.get('prestate',{})
            if (state.get('analysis_domain')!=selected_domain or
                    state.get('initial_model_identity')!=(initial or {}).get('identity') or
                    state.get('executed_prefix') or state.get('encoded_case') or state.get('encoded_request_bindings')):continue
            if not effect and base.get('answer')=='unsat':
                tested=base;value=False;kind='source_path_infeasible_in_this_domain'
            elif (base.get('bounded_condition_confirmed') and effect.get('label')=='direct_effect'
                    and {k:v for k,v in effect.get('details',{}).items() if k!='prestate'}=={k:v for k,v in d.items() if k!='prestate'}
                    and effect.get('details',{}).get('prestate',{}).get('analysis_domain')==selected_domain
                    and effect.get('details',{}).get('prestate',{}).get('initial_model_identity')==(initial or {}).get('identity')
                    and not effect.get('abstract_hash')):
                if effect.get('answer')=='unsat':value=False
                elif effect.get('bounded_condition_confirmed'):value=True
                else:continue
                tested=effect;kind='effect_on_feasible_source_path'
            else:continue
            # Bounded prefix exhaustion does not exclude an unexamined later stage.
            tested_state=tested.get('details',{}).get('prestate',{})
            bounded_exclusion=value is False and not (tested_state.get('global_reachability_exhausted') or tested.get('exclusion_certificate',{}).get('excludes_only_this_formula'))
            position=(pid,key(cell))
            results[position]={'result':value,'kind':kind,'evidence':evidence_id,'probe':tested['id'],'feasibility_probe':base['id'],
                'formula':tested['formula_ref'],'target':target,'operation':root,'path':pid,'position':cell,'predicate':predicate,
                'actor_scope':'beneficiary_equals_caller' if category=='FCR-MINT' else 'debit_other_nonzero_holder',
                'argument_domain':d['argument_domain'],'prestate':tested_state,'bounded_exclusion_only':bounded_exclusion,
                'exclusion_certificate':tested.get('exclusion_certificate')}
    return results


def _all_direct_effects_excluded(b,root,category,excluded):
    """Conservative completeness check for this source claim, never for other entries or classes."""
    if not excluded or any(x.get('bounded_exclusion_only') for x in excluded) or not b.complete(root):return False
    covered={(x['path'],key(x['position'])) for x in excluded}
    for pid,path in b.paths(root):
        if path.get('sensitive_effects'):return False
        for w in path['writes']:
            s=w['path']
            if not keys(s):continue
            if not value_type(s,b.f.lookup(root)).startswith('uint') or (pid,key(s)) not in covered:return False
            # A self-credit check does not exclude a different, controlled third-party beneficiary.
            if category=='FCR-MINT' and (bound_holder(s,b.f.lookup(root)) or {}).get('kind')!='actual_sender':return False
    return True


def alignment(inv,q,scope):
    b=inv.backend;f=inv.f;i=q['current'];root=inv.root(q);cat=i.get('category')
    result={'definition_reference':'JANUS v2 II-B','nominated_category':cat,'status':'unresolved','conditions':[],
            'prestate_alignment':'authors_per_member_initial_state_not_verified','source_basis':[],
            'normative_hypothesis':i['claim'],'scope':'specified actual targets and routes',
            'constructor_path_executed':False,'candidate_generated_here':False}
    def end(status,reason):
        result.update(status=status,reason=reason)
        return result
    if not root:return end('unresolved','applied_target_unresolved')
    from .initial_state import domain, initial_for_lookup
    state_model=initial_for_lookup(f.lookup(root))
    result['analysis_domain']=domain(f.lookup(root))
    result['initial_model_identity']=(state_model or {}).get('identity')
    result['deployment_reachability']='not_separately_established'
    result['conditional_state_assumptions']=[{'declaration':v['declaration'],'origin':v['origin']} for v in state_facts(f.lookup(root)).values() if v.get('origin')=='abstract_initial_scalar']
    target=f.operations[root]['target'];entries=claim_entries(inv,q['binding'],i)
    choice=q.get('plan',{}).get('observation_choice') or {}
    pick=choice.get('selected') or {}
    if pick:entries.update((pick['change'],pick['observe']))
    hint=i.get('next_check') or {}
    if isinstance(hint,dict) and hint.get('action')=='compare':
        for field in ('change','observe'):
            ids=[o for o in inv.catalog.resolve(hint.get(field)) if f.operations[o]['target']==target]
            if len(ids)==1 and (ids[0] in entries or linked_controls(inv,root,ids[0])):entries.update(ids)
    routes=ledger_routes(b,target); controls=[]
    result['prestate_sources']={v['name']:v['origin'] for v in state_facts(f.lookup(root)).values() if
        any(c['root']==v['declaration'] for o in entries for c in inv.graph.request_reads(o))}
    if not routes:result['asset_scope_limit']='no source-resolved transferable ledger route in compiled scope'
    if any(inv.evidence[e].get('operation')==root and inv.evidence[e].get('no_committing_path') for e in q['evidence']):
        return end('refuted','original_source_has_no_committing_path_for_this_capability')
    if impossible_role(inv,root):return end('refuted','committing_path_incompatible_with_fixed_initial_state_or_zero_role')
    if q.get('task_conflict'):return end('unresolved','task_direction_requires_review')
    for change in sorted(entries):
        if not privileged_paths(inv,change) or impossible_role(inv,change):continue
        for use in entries-{change}:
            qualified=privileged_paths(inv,change)
            writes=[w['path'] for pid,p in b.paths(change) if pid in qualified for w in p['writes']]
            for cell in linked_controls(inv,change,use):
                if any(same(cell,w) and not inv.graph._disjoint_keys(cell,w) for w in writes):
                    controls.append((change,use,cell))
    # A privilege change discovered during property binding need not be a second user-supplied anchor.
    evidence=[e for e in scope.get('scoped_observations',[]) if any(o.get('predicate_value') for o in e['outcomes'])]
    result['condition_probes']=[p for e in evidence for p in e['matched_probes']]
    if cat in ('FCR-FREEZE','FCR-PAUSE'):
        coverage=[];related=set()
        for change,use,cell in controls:
            for route in routes:
                if route['operation']!=use:continue
                path=f.paths[route['path']]['raw'];lookup=f.lookup(use)
                if not gates(path,cell):continue
                observed_block=any(e['measure']=='blocks' and e['change']==change and e['observe']==use and
                    any(o['predicate_value'] for o in e['outcomes']) for e in evidence)
                if not observed_block and not can_restrict(b,change,use,path,cell):continue
                ks=keys(cell);holder=bound_holder(route['debit'],lookup)
                if holder is None:continue
                targeted=len(ks)==1 and key(ks[0])==key(holder)
                shared=not ks or all(k.get('kind') in ('contract_address','literal') for k in ks)
                coverage.append({'writer':change,'use':use,'path':route['path'],'control':cell,
                    'outgoing_position':route['debit'],'targeted':targeted,'common_control':shared})
                related.add((change,use))
        result['source_basis']=coverage
        if cat=='FCR-FREEZE' and any(c['targeted'] for c in coverage):
            return end('main','conditional_source_mechanism_on_designated_outgoing_holder')
        if cat=='FCR-PAUSE' and any(c['common_control'] for c in coverage):
            for c in coverage:
                if not c['common_control']:continue
                gaps=[]
                for r in routes:
                    if not same(r['debit'],c['outgoing_position']) or r['path'] in privileged_paths(inv,r['operation']):continue
                    path=f.paths[r['path']]['raw']
                    if not any(same(x,c['control']) and key(keys(x))==key(keys(c['control'])) and gates(path,x) for x in inv.graph.request_reads(r['operation'])):
                        gaps.append(r['operation'])
                if not gaps:return end('main','common_outgoing_transfer_control_source_prediction_not_universal_proof')
                result['other_transfer_routes']=sorted(set(gaps))
            return end('unresolved','independent_outgoing_route_not_covered_by_common_control')
        affected=[r for r in routes if r['operation'] in entries]
        if not affected and any(holder_effect_for_business(b,o) for o in entries) or not affected and (related or evidence):
            return end('additional','limited_to_non_transfer_business_availability')
        if coverage:return end('additional','single_holder_or_different_side_or_common_scope_only')
        return end('unresolved','specific_outgoing_control_or_group_scope_not_established')
    if cat not in ('FCR-TRANSFER','FCR-MINT','FCR-DESTROY'):return end('additional','outside_five_capabilities')
    direct=privileged_paths(inv,root);claimed_effect=False
    checked=_direct_results(inv,root,cat,q);excluded=[]
    result['matched_counterevidence']=excluded
    for pid,p in b.paths(root):
        lookup=f.lookup(root);m=movements(b,root,p); t=transfer_shapes(b,root,p)
        if pid not in direct:continue
        for d in m['-']+literal_balance_zero(p,lookup):
            actual_holder=bound_holder(d,lookup)
            if actual_holder is None:continue
            right=bool(unit_origin(b,root,d) or any(same(d,r['debit']) for r in routes))
            if not right or holder_only(b,root,p,d) or consent_gate(b,root,p,d):continue
            verified=checked.get((pid,key(d)))
            if cat in ('FCR-TRANSFER','FCR-DESTROY') and verified and not verified['result']:
                excluded.append(verified);continue
            claimed_effect=True
            if cat=='FCR-DESTROY' and not any(same(d,c) and key(d)!=key(c) for c in m['+']) and not any(x['path']==pid and key(x['object'])==key(d) and key(x['holder'])==key(actual_holder) and x['same_holder_and_unit_full_settlement'] for e in q['evidence'] for x in inv.evidence[e].get('settlements',[])):
                result['source_basis'].append({'operation':root,'path':pid,'victim':d,'role_guards':p['guards']})
            if cat=='FCR-TRANSFER':
                for payer,payee in t:
                    if key(payer)==key(d):result['source_basis'].append({'operation':root,'path':pid,'payer':payer,'payee':payee,'permission_path':p['guards']})
        if cat=='FCR-MINT':
            for c in m['+']:
                verified=checked.get((pid,key(c)))
                if not (unit_origin(b,root,c) or any(same(c,r['credit']) for r in routes)) or any(same(c,d) for d in m['-']) and not (verified and verified['result']):continue
                if any(n.get('kind')=='transaction_value' for w in p['writes'] if key(w['path'])==key(c) for n in walk(w['value'])):continue
                beneficiary=bound_holder(c,lookup)
                if beneficiary is None:continue
                source_self=beneficiary.get('kind')=='actual_sender'
                verified=checked.get((pid,key(c)))
                if verified and not verified['result']:
                    excluded.append(verified);continue
                actor_receipt=bool(verified and verified['result'] and verified['actor_scope']=='beneficiary_equals_caller')
                parameter=beneficiary.get('kind')=='parameter'
                guard_binds_recipient=any(key(n)==key(beneficiary) for g in p['guards'] for n in walk(g))
                if source_self or actor_receipt or parameter and not guard_binds_recipient:
                    result['source_basis'].append({'operation':root,'path':pid,'credit':c,'role_guard':True,
                        'controller_self_credit':'sender' if source_self else 'verified_self_condition' if actor_receipt else 'free_recipient_argument'})
    if result['source_basis']:return end('main','role_supported_five_class_capability_with_source_effect')
    if _all_direct_effects_excluded(b,root,cat,excluded):
        return end('refuted','matched_direct_effect_impossible_on_all_applicable_positions_and_paths')
    if excluded and any(x.get('bounded_exclusion_only') for x in excluded):
        return end('unresolved','required_positive_effect_not_established_in_checked_transition_scope')
    excess=[o for e in evidence if e['measure']=='ledger_grant' for o in e['outcomes'] if o['predicate_value']]
    routed_excess=any(o.get('predicate_checks',{}).get('destination_credit_exceeds_grant') is True for o in excess)
    if cat=='FCR-TRANSFER' and routed_excess and controls:return end('main','privileged_runtime_intervention_and_destination_credit_above_holder_grant')
    if any(e['measure'] in ('ledger_debit','ledger_receipt','ledger_grant','holder_net') for e in evidence):
        return end('additional','amount_or_redemption_difference_without_matched_five_class_capability')
    if claimed_effect:return end('unresolved','destination_or_consent_scope_not_established')
    return end('unresolved','role_beneficiary_token_or_applicable_effect_not_resolved')


def purpose_only_change(inv,q,proposal,cited):
    if not business_only(proposal) or q['current'].get('assessment')!='risk':return False
    # New independent source facts can demonstrate actual consent or settlement.
    # A compliance rationale plus a witness to the very same power cannot.
    return not any(any(x.get('same_holder_and_unit_full_settlement') and inv.evidence[e].get('operation')==inv.root(q) for x in inv.evidence[e].get('settlements',[])) or inv.evidence[e].get('control_noninterference',{}).get('proved')
                   or inv.evidence[e].get('holder_consent_counterexamples') and inv._direction_contradictions(q)
                   for e in cited) and not any(k in proposal and proposal[k]!=q['current'].get(k) for k in ('actor','object','phase','assumptions'))


def holder_effect_for_business(b,oid):
    return any(p.get('sensitive_effects') or any(w['path'].get('segments') for w in p['writes']) for _,p in b.paths(oid))


```

## source/src/pr_next_joint/investigation/context.py

原文件SHA256 `c6543bbd54a49b0f3552a2aa1dac806b08b57551362f92c307c05ff17ec7c110`

```python
"""Source-first, graph-organized views. Complete original facts stay local."""
import copy,json,re
from collections import defaultdict,deque
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import walk
from .contracts import VERSION
from .protocol import instruction,REVISION_GUIDANCE,question_entity

class Catalog:
    def __init__(self,program,graph=None):
        self.program=program if hasattr(program,'context') else None
        self.context=program.context if self.program else program
        self.identity=self.program.identity if self.program else digest(program)
        self.graph=graph
        self.sources={s['file']:s for s in self.context['sources']}
        self.operations={o['id']:o for o in self.context['operations']}
        self.targets=sorted({o['target'] for o in self.operations.values()})
        self.target_alias={t:'T'+str(i+1) for i,t in enumerate(self.targets)}
        self.labels={};self.label_locations={};self.aliases=defaultdict(list);self.declarations={};self.declaration_aliases=defaultdict(list)
        for oid,o in self.operations.items():
            for name in (o['target']+'.'+o['function'],self.target_alias[o['target']]+'.'+o['function'],
                         o['function'],o['target'].split(':',1)[-1]+'.'+o['function']):self.aliases[name].append(oid)
        # A declaring base name is not necessarily a selected creation target.
        # Join the exact compiler-selected entry declaration to its source owner;
        # never resolve an overridden body merely by a matching spelling.
        self.declaration_entries=defaultdict(list)
        if self.program and hasattr(self.program,'lookup'):
            for oid,o in self.operations.items():
                lookup=self.program.lookup(oid);node=lookup.function(o['function'])
                node=node.get('generated_getter',node)
                owner=next((c for c in lookup.nodes.values() if c.get('nodeType')=='ContractDefinition'
                    and any(n.get('id')==node.get('id') for n in c.get('nodes',[]))),None)
                if owner is None or node.get('nodeType')!='FunctionDefinition':continue
                actual=lookup.anchor(node)
                if any(actual.get(k)!=o['source'].get(k) for k in ('file','start','length','ast_id')):continue
                aliases=(actual['file']+':'+owner['name']+'.'+o['function'],owner['name']+'.'+o['function'])
                for alias in aliases:
                    self.aliases[alias].append(oid)
                    self.declaration_entries[alias].append({'operation':oid,'declaring_contract':owner['name'],
                        'applied_target':o['target'],'ast_id':node['id'],'source':actual,
                        'basis':'compiler-selected implementation and exact declaration containment/span'})
        # Internal declarations supply source evidence, never external transactions.
        if self.program and hasattr(self.program,'lookups'):
            from pr_next_joint.frontend.source_entry_identity import declared_type_pair
            for target,lookup in self.program.lookups.items():
                bases=lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
                # Old compiler ASTs omit scope on functions. The owning contract
                # is still exact from AST containment, including inherited bases.
                owners={child['id']:c['id'] for c in lookup.nodes.values() if c.get('nodeType')=='ContractDefinition' for child in c.get('nodes',[]) if isinstance(child,dict)}
                for n in lookup.nodes.values():
                    if n.get('nodeType') not in ('FunctionDefinition','ModifierDefinition') or n.get('scope',owners.get(n['id'])) not in bases:continue
                    if n.get('nodeType')=='FunctionDefinition' and n.get('visibility') not in ('internal','private'):continue
                    pairs=[declared_type_pair(p.get('typeName',{}),lookup) for p in n.get('parameters',{}).get('parameters',[])]
                    if any(p is None for p in pairs):continue
                    sig=n.get('name','')+'('+','.join(p[1] for p in pairs)+')';ref='decl_'+digest([target,n['id']])[:20]
                    self.declarations[ref]={'id':ref,'target':target,'ast_id':n['id'],'function':sig,'source':lookup.anchor(n),'external_transaction':False}
                    owner=lookup.nodes.get(n.get('scope',owners.get(n['id'])),{})
                    declared=(lookup.anchor(n)['file']+':'+owner.get('name','')+'.'+sig,owner.get('name','')+'.'+sig)
                    for alias in (target+'.'+sig,target.split(':',1)[-1]+'.'+sig,sig)+declared:
                        self.declaration_aliases[alias].append(ref)
            from pr_next_joint.frontend.dispatch import resolve as dispatch
            for alias,refs in list(self.declaration_aliases.items()):
                targets={self.declarations[r]['target'] for r in refs}
                if len(targets)!=1 or len(refs)<2:continue
                lookup=self.program.lookups[next(iter(targets))]
                resolved={dispatch(lookup,lookup.nodes[self.declarations[r]['ast_id']])['id'] for r in refs}
                chosen=[r for r in refs if self.declarations[r]['ast_id'] in resolved]
                if len(resolved)==len(chosen)==1:self.declaration_aliases[alias]=chosen
        self.internal_callers=defaultdict(list)
        if self.program and hasattr(self.program,'lookup'):
            def reaches(lookup,body,nid,seen):
                from pr_next_joint.frontend.dispatch import resolve as dispatch,member_target
                refs=set()
                for n in walk(body):
                    if n.get('nodeType')!='FunctionCall':continue
                    ref=n.get('expression',{}).get('referencedDeclaration');node=lookup.nodes.get(ref,{})
                    if node.get('nodeType')!='FunctionDefinition':continue
                    try:
                        dest=dispatch(lookup,node) if n['expression'].get('nodeType')=='Identifier' else member_target(lookup,n,node)
                    except (KeyError,ValueError,TypeError,AttributeError):
                        dest=None
                    if dest:refs.add(dest['id'])
                refs|={n.get('modifierName',{}).get('referencedDeclaration') for n in walk(body) if n.get('nodeType')=='ModifierInvocation'}
                if nid in refs:return True
                for ref in refs-seen:
                    node=lookup.nodes.get(ref,{})
                    if node.get('nodeType') in ('FunctionDefinition','ModifierDefinition') and reaches(lookup,node,nid,seen|{ref}):return True
                return False
            for ref,decl in self.declarations.items():
                for oid,operation in self.operations.items():
                    if operation['target']!=decl['target']:continue
                    lookup=self.program.lookup(oid)
                    if reaches(lookup,lookup.function(operation['function']),decl['ast_id'],set()):self.internal_callers[ref].append(oid)
        self.frontier=self.context['frontier'];self.adj=defaultdict(set)
        for edge in self.frontier:
            self.adj[edge['from']].add(edge['to']);self.adj[edge['to']].add(edge['from'])
    def name(self,oid):
        o=self.operations[oid];return o['target']+'.'+o['function']
    def slice(self,anchor):
        s=self.sources[anchor['file']]['content'].encode('utf-8')
        return s[anchor['start']:anchor['start']+anchor['length']].decode('utf-8',errors='replace')
    def lines(self,anchor):
        s=self.sources[anchor['file']]['content'].encode('utf-8')
        return [s[:anchor['start']].count(b'\n')+1,s[:anchor['start']+anchor['length']].count(b'\n')+1]
    def resolve(self,anchor):
        if not isinstance(anchor,str):return []
        if anchor in self.labels:return list(self.labels[anchor])
        if anchor in self.aliases:return sorted(set(self.aliases[anchor]))
        # A literal placeholder is not an ABI type. Resolve its exact qualified
        # declaration family only when the compiler catalog has a single entry.
        # Concrete wrong signatures (including enum/uint mismatches) are NOT repaired.
        placeholder=re.fullmatch(r'(.+)\((?:function|\.\.\.|\?)\)',anchor)
        if placeholder:
            family=placeholder[1]+'('
            return sorted({o for alias,ids in self.aliases.items() if alias.startswith(family)
                           for o in ids})
        # Short names only enumerate exact declarations. Never fuzzy-select one.
        if re.fullmatch(r'[A-Za-z_$][\w$]*',anchor):
            return sorted(o for o,x in self.operations.items() if x['function'].split('(')[0]==anchor)
        m=re.fullmatch(r'(.+\.sol):(\d+)(?:[-:](\d+))?',anchor)
        if m and m[1] in self.sources:
            lo=int(m[2]);hi=int(m[3] or lo)
            return sorted(o for o,x in self.operations.items() if x['source']['file']==m[1] and
                          self.lines(x['source'])[0]<=lo<=self.lines(x['source'])[1] and hi>=lo)
        return []
    def target_branches(self,anchors,core=None):
        initial=core or (anchors[0] if anchors else None)
        ids=self.resolve(initial)
        if len(ids)<2:return []
        # A short, ABI-qualified or line anchor can denote the very same
        # compiler declaration in several layouts. Verify its actual source
        # identity on every applied operation, independently of alias spelling.
        locations={tuple(self.operations[o]['source'].get(k) for k in ('file','ast_id','start','length')) for o in ids}
        if len(locations)!=1 or None in next(iter(locations)):return []
        targets=[self.operations[o]['target'] for o in ids]
        return sorted(targets) if len(set(targets))==len(ids) else []
    def bind(self,anchors,core=None,prior=None,target=None):
        def allowed(ids):
            return [oid for oid in ids if target is None or self.operations[oid]['target']==target]

        located={};unresolved=[];ambiguous=[];internal=[]
        for anchor in anchors:
            ids=allowed(self.resolve(anchor))
            if not ids:
                refs=[r for r in self.declaration_aliases.get(anchor,[]) if target is None or self.declarations[r]['target']==target]
                if refs:
                    internal.extend(copy.deepcopy(self.declarations[r]) for r in dict.fromkeys(refs))
                    if len(refs)>1:ambiguous.append({'anchor':anchor,'declaration_contexts':list(dict.fromkeys(refs))})
                else:unresolved.append(anchor)
            elif len(ids)>1:ambiguous.append({'anchor':anchor,'candidates':ids});located[anchor]=ids
            else:located[anchor]=ids
        requested=core if isinstance(core,str) else anchors[0] if anchors else None
        core_ids=allowed(self.resolve(requested)) if requested else []
        protected_ambiguity=len(core_ids)>1 and (self.target_branches(anchors,requested) or self.declaration_entries.get(requested) or
            re.fullmatch(r'.+\((?:function|\.\.\.|\?)\)',requested or ''))
        if core is None and len(core_ids)!=1 and not protected_ambiguity:
            core_ids=next((v for v in located.values() if len(v)==1),[])
        # A valid old core is retained only when the revision did not request a
        # different explicit root. An invalid new core cannot replace it silently.
        internal_contexts={r['id']:self.internal_callers.get(r['id'],[]) for r in internal}
        contexts=sorted({i for ids in internal_contexts.values() for i in ids})
        # An internal-only clue starts in its real external caller context. A
        # unique caller is exact; multiple callers remain ambiguous, never an
        # invented directly callable internal transaction.
        if not core_ids and len(contexts)==1 and requested in self.declaration_aliases:core_ids=contexts
        selection='explicit_root' if core is not None else 'initial_source_anchor'
        old_core=(prior or {}).get('core_operation')
        if core is None and (prior or {}).get('core_exact') and old_core in self.operations:
            # Ordering, adding or dropping supplementary references is not a
            # request to relocate the existing root. accept validates genuine
            # semantic corrections separately, without requiring a root field.
            core_ids=[old_core];selection='preserved_prior_core'
        core_operation=core_ids[0] if len(core_ids)==1 else None
        core_anchor=((prior or {}).get('core_anchor') or self.name(old_core)) if selection=='preserved_prior_core' else (
            core if core is not None and len(self.resolve(core))==1 else next((a for a,ids in located.items() if ids==core_ids),None))
        return {'applied_context':target,'located':located,'operations':sorted({i for ids in located.values() for i in ids}|set(contexts)|set(core_ids)),
                'unresolved':unresolved,'ambiguous':ambiguous,'internal_references':internal,
                'internal_external_caller_contexts':internal_contexts,
                'core_operation':core_operation,'core_exact':core_operation is not None,
                'core_anchor':core_anchor,'core_selection':selection,
                'exact':core_operation is not None,'all_references_exact':bool(located) and not unresolved and not ambiguous,
                'supplementary_gaps':unresolved+ambiguous,
                'declaration_entry_bindings':{a:copy.deepcopy(self.declaration_entries[a]) for a in anchors if a in self.declaration_entries},
                'candidate_core_operations':sorted(set(core_ids or contexts or [i for v in located.values() for i in v])),
                'placeholder_clarifications':[{'original':a,'resolved':self.name(ids[0]),
                    'source':copy.deepcopy(self.operations[ids[0]]['source']),
                    'basis':'literal placeholder; unique exact target/declaration family, not fuzzy ABI matching'}
                    for a,ids in located.items() if len(ids)==1 and re.fullmatch(r'.+\((?:function|\.\.\.|\?)\)',a)]}
    def related(self,oid):return sorted(self.adj[oid])
    def card(self,oid):
        o=self.operations[oid];return {'anchor':self.name(oid),'operation_id_for_host':oid,
            'source':copy.deepcopy(o['source']),'lines':self.lines(o['source']),
            'code':self.slice(o['source']),'parameters':[{k:v for k,v in p.items() if k=='name'} for p in o['parameters']]}
    def support(self,oid):
        """Actual declarations, modifiers and internal calls, not normality templates."""
        if not self.program or not hasattr(self.program,'lookup'):
            # Read-only prepared-message previews can reuse the exact saved M1 graph.
            graph=self.graph if isinstance(self.graph,dict) else {};nodes={n['id']:n for n in graph.get('nodes',[])}
            anchors=[];o=self.operations[oid]
            for edge in graph.get('edges',[]):
                if edge['from']==oid and edge['kind'] in ('calls','modifier'):
                    a=nodes.get(edge['to'],{}).get('data',{}).get('source')
                    if a:anchors.append(a)
            roots={n['root'] for p in o['paths'] for ref in p.get('guards',[])+[w['selector'] for w in p.get('writes',[])]
                   for n in walk(self.context['terms'].get(ref,{}).get('expression',{})) if n.get('kind')=='storage'}
            anchors +=[r['source'] for r in self.context['references'].values() if r['target']==o['target'] and r['ast_id'] in roots]
            return [{'source':a,'code':self.slice(a),'kind':'saved_exact_source_dependency'} for a in {tuple(sorted(a.items())):a for a in anchors if a['file'] in self.sources}.values()]
        lookup=self.program.lookup(oid);o=self.operations[oid];body=lookup.function(o['function'])
        needed=[]
        for n in walk(body):
            if n.get('nodeType')=='ModifierInvocation':needed.append(n.get('modifierName',{}).get('referencedDeclaration'))
            if n.get('nodeType')=='FunctionCall':needed.append(n.get('expression',{}).get('referencedDeclaration'))
        roots={n['root'] for p in o['paths'] for t in p.get('guards',[]) for n in walk(self.context['terms'].get(t,{}).get('expression',{})) if n.get('kind')=='storage'}
        for w in (self.program.writes.values()):
            if w['operation']==oid:roots.add(w['raw']['path']['root'])
        needed+=sorted(roots)
        result=[]
        for nid in dict.fromkeys(needed):
            node=lookup.nodes.get(nid)
            if not node or node.get('nodeType') not in ('VariableDeclaration','ModifierDefinition','FunctionDefinition'):continue
            a=lookup.anchor(node)
            if a['length'] and a['file'] in self.sources:
                result.append({'source':a,'code':self.slice(a),'kind':node['nodeType']})
        return result
    def index(self):
        result={'targets':{a:t for t,a in self.target_alias.items()},'entries':[
            self.target_alias[o['target']]+'.'+o['function'] for o in sorted(self.operations.values(),key=lambda x:(x['target'],x['function']))],
            'meaning':'T aliases denote exact targets; repeated inherited source remains target-specific.'}
        if self.program:
            from pr_next_joint.frontend.source_entry_identity import function_kind
            declarations={}
            for target,lookup in self.program.lookups.items():
                bases=lookup.contract_node.get('linearizedBaseContracts',[])
                inst=[]
                for bid in bases:
                    base=lookup.nodes[bid]
                    names=[n['id'] for n in base.get('nodes',[]) if n.get('nodeType')=='FunctionDefinition'
                           and function_kind(n)=='constructor']
                    inst.append([base.get('name'),names])
                declarations[self.target_alias.get(target,target)]=inst
            result['construction_by_target']=declarations
            result['dispatch_note']='Entries are runtime entries; base names and constructor declaration IDs refer to the compiler-selected linearization.'
        return result

    def required_context(self,operations):
        """AST-bound declaration/call closure for one feedback unit, not top-k.

        Include contract headers, base declarations and referenced helpers. If an
        exact closure cannot be built, the caller must not send a partial unit.
        """
        fragments={};identities=[];missing=[]
        def add(anchor,kind,target):
            if not anchor or anchor.get('file') not in self.sources:return
            loc=(anchor['file'],anchor['start'],anchor['length'])
            entry=fragments.setdefault(loc,{'source':{k:v for k,v in anchor.items() if k!='ast_id'},
                'kind':kind,'code':self.slice(anchor),'targets':[]})
            if target not in entry['targets']:entry['targets'].append(target)
        for oid in dict.fromkeys(operations):
            if oid not in self.operations:continue
            o=self.operations[oid]
            if not self.program or not hasattr(self.program,'lookup'):
                missing.append({'operation':oid,'reason':'compiler_declaration_context_unavailable'});continue
            lookup=self.program.lookup(oid);body=lookup.function(o['function'])
            if not body:missing.append({'operation':oid,'reason':'exact_entry_declaration_unavailable'});continue
            declaration=body.get('generated_getter',body)
            from pr_next_joint.frontend.source_entry_identity import function_kind
            owners={n['id']:c for c in lookup.nodes.values() if c.get('nodeType')=='ContractDefinition'
                    for n in c.get('nodes',[]) if isinstance(n,dict)}
            declaring=owners.get(declaration.get('id'),lookup.contract_node)
            identities.append({'anchor':self.name(oid),'entry_kind':'generated_getter' if 'generated_getter' in body else function_kind(body),
                'declaring_contract':declaring.get('name'),'applied_target':o['target'],
                'basis':'compiler AST kind and declaration containment, not function spelling',
                'constructor_declarations':[{'declaring_contract':c.get('name'),'compiler_kind':'constructor',
                    'source':lookup.anchor(n),'external_transaction':False}
                    for c in lookup.nodes.values() if c.get('nodeType')=='ContractDefinition' and
                        c['id'] in lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
                    for n in c.get('nodes',[]) if function_kind(n)=='constructor']})
            bases=lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
            queue=[declaration['id']]
            for cid in bases:
                c=lookup.nodes.get(cid,{})
                if not c:continue
                a=lookup.anchor(c);children=[lookup.anchor(n)['start'] for n in c.get('nodes',[]) if lookup.anchor(n).get('file')==a['file']]
                header_length=min(children)-a['start'] if children else a['length']
                if header_length<=0:missing.append({'target':o['target'],'reason':'contract_header_not_locatable'});continue
                add({**a,'length':header_length},'contract_header_and_inheritance',o['target'])
                # Declaration context is conservative and neutral; no business
                # classification is inferred from state-variable names.
                queue += [n['id'] for n in c.get('nodes',[]) if n.get('nodeType') in
                          ('VariableDeclaration','StructDefinition','EnumDefinition','UserDefinedValueTypeDefinition')]
                queue += [n['id'] for n in c.get('nodes',[]) if function_kind(n)=='constructor']
            for n in lookup.nodes.values():
                if n.get('nodeType') in ('PragmaDirective','ImportDirective'):
                    add(lookup.anchor(n),n['nodeType'],o['target'])
            seen=set()
            while queue:
                nid=queue.pop()
                if nid in seen:continue
                seen.add(nid);n=lookup.nodes.get(nid,{})
                if n.get('nodeType') not in ('FunctionDefinition','ModifierDefinition','VariableDeclaration',
                      'StructDefinition','EnumDefinition','EventDefinition','UserDefinedValueTypeDefinition'):continue
                owner=owners.get(nid)
                if owner and owner['id'] not in bases:
                    a=lookup.anchor(owner);children=[lookup.anchor(x)['start'] for x in owner.get('nodes',[]) if lookup.anchor(x).get('file')==a['file']]
                    add({**a,'length':min(children)-a['start'] if children else a['length']},'referenced_declaration_contract_header',o['target'])
                add(lookup.anchor(n),n['nodeType'],o['target'])
                # referencedDeclaration denotes the lexical declaration, not
                # necessarily the implementation executed by this target.
                # Reuse the same dispatch as source execution, including the
                # lexical owner of super and explicit/private bindings.
                from pr_next_joint.frontend.dispatch import resolve,member_target
                call_expressions=set()
                for call in walk(n):
                    if call.get('nodeType')!='FunctionCall':continue
                    expr=call.get('expression',{});ref=expr.get('referencedDeclaration')
                    target=lookup.nodes.get(ref,{})
                    internal=expr.get('typeDescriptions',{}).get('typeIdentifier','').startswith('t_function_internal_')
                    if target.get('nodeType')!='FunctionDefinition':
                        if internal:
                            missing.append({'target':o['target'],'source':lookup.anchor(call),
                                'reason':'internal_call_implementation_context_unresolved'})
                        continue
                    call_expressions.add(expr.get('id'))
                    try:
                        owner=owners.get(ref,{})
                        if (target.get('visibility')!='private' and owner.get('id') in bases and len(bases)>1
                                and (target.get('scope')!=owner.get('id') or any(not p.get('typeDescriptions',{}).get('typeIdentifier')
                                    for p in target.get('parameters',{}).get('parameters',[])))):
                            raise ValueError('compiler_dispatch_metadata_incomplete')
                        if expr.get('nodeType')=='Identifier':bound=resolve(lookup,target)
                        else:bound=member_target(lookup,call,target)
                        if bound is None:
                            # An external/interface declaration is source
                            # context, not a proven implementation binding.
                            queue.append(ref)
                            if internal:raise ValueError('internal_dispatch_not_resolved')
                        else:queue.append(bound['id'])
                    except (ValueError,KeyError,TypeError,AttributeError) as error:
                        queue.append(ref)
                        missing.append({'target':o['target'],'source':lookup.anchor(call),
                            'reason':'required_call_dispatch_context_unresolved',
                            'detail':type(error).__name__+':'+str(error)})
                for child in walk(n):
                    ref=child.get('referencedDeclaration')
                    if ref in lookup.nodes and child.get('id') not in call_expressions:queue.append(ref)
                    if child.get('nodeType')=='ModifierInvocation':
                        queue.append(child.get('modifierName',{}).get('referencedDeclaration'))
            # Exact source closure has no function-name or dataset-ID exceptions.
        ordered=sorted(fragments.items())
        # Do not send nested source twice (e.g. a struct member inside its struct).
        kept=[]
        for loc,entry in sorted(ordered,key=lambda x:(x[0][0],x[0][1],-x[0][2])):
            if any(loc[0]==p['source']['file'] and p['source']['start']<=loc[1] and
                   loc[1]+loc[2]<=p['source']['start']+p['source']['length'] for p in kept):continue
            kept.append(entry)
        return kept,identities,missing

class SourceContext:
    def __init__(self,program,catalog,counter):
        self.program,self.catalog,self.counter=program,catalog,counter;self.initial_view=None;self.initial_scope=None;self.last_manifest=None
    def _messages(self,value,recovery=False):
        kind=None
        if 'questions' in value:
            question=next(iter(value['questions']),{})
            choice=next(iter(question.get('semantic_questions',[])),{})
            choice=value.get('shared_rows',{}).get(choice.get('shared'),choice)
            kind='local_effect' if question.get('local_effect_review') else choice.get('kind','issue')
        revisable_amount=(self.program.options.scope=='FCR' and
                         any('on' in card for card in value.get('supports',())))
        audit_revision = (' To withdraw your own displayed interpretation use hypotheses[{withdraw:audit_ref,effect_ref,reason}].'
                          if any(q.get('audit_ref') for q in value.get('questions',())) else '')
        return [{'role':'system','content':instruction(self.program.options.scope,recovery or value.get('purpose')=='protocol_recovery',
                                                      kind=kind,annotation_revision=revisable_amount,policy_revision=any('effect' in card for card in value.get('supports',()))) + audit_revision},
                {'role':'user','content':json.dumps(value,ensure_ascii=False,separators=(',',':'))}]
    def _count(self,value):return self.counter.count(self._messages(value))
    def _model_card(self,oid):
        c=self.catalog.card(oid);c.pop('operation_id_for_host');c['support']=self.catalog.support(oid)
        # Fact payloads and expression graphs never re-enter M2 through this view.
        for x in [c,*c['support']]:
            if 'source' in x:x['source']={k:v for k,v in x['source'].items() if k!='ast_id'}
        return c
    def _focus(self):
        graph=self.catalog.graph
        if graph is None:
            return None, []
        front=graph.neutral_frontier()
        r=front['primary']
        if r is None:
            return None, []
        names=self.catalog.name
        focus={'write':names(r['writer']),'use':names(r['use']),'cell':r['declaration'],
               'read_in':r['role_of_read'],'question':'Which actual subject and right are affected? What observable distinguishes the applicable explanations?'}
        use_cells=[w['raw']['path'] for w in self.program.writes.values() if w['operation']==r['use']]
        related=graph.closure_operations(r['use'],[r['ordered_read_key'],*use_cells])
        return focus,list(dict.fromkeys([r['writer'],r['use'],*related]))

    @staticmethod
    def _share(value):
        """Intern only identical rows across questions; branch, key and role are part of identity."""
        if len(value['questions'])<2:
            return value
        value=copy.deepcopy(value)
        occurrences=defaultdict(list)
        for qi,q in enumerate(value['questions']):
            for field in ('entry_identity_facts','evidence'):
                for i,v in enumerate(q.get(field,[])):
                    occurrences[(field,digest(v))].append((qi,i))
        shared={}
        for (field,h),sites in occurrences.items():
            if len(sites)<2:
                continue
            qi,i=sites[0];row=value['questions'][qi][field][i]
            if len(json.dumps(row))<100:
                continue
            ref='s'+str(len(shared)+1);shared[ref]=row
            for qi,i in sites:
                value['questions'][qi][field][i]={'shared':ref}
        if shared:
            value['shared_rows']=shared
        return value

    def initial(self):
        p=self.program;cat=self.catalog;target=p.options.input_target;limit=p.options.input_limit
        base={'presentation':VERSION,'task':p.options.scope,'entry_index':cat.index(),
              'semantic_focus':('Assess the actual caller against the applicable duty at the highlighted effects.' if p.options.scope=='AC'
                                else 'Clarify the unit or consent of the highlighted account position if material.')}
        complete={**base,'source_files':[{'file':f,'content':s['content']} for f,s in cat.sources.items()]}
        focus,focus_ops=self._focus()
        if self._count(complete)<=limit:
            manifest={'mode':'complete_source','expanded_operations':sorted(cat.operations),'unexpanded_operations':[],
                      'complete_source_files':sorted(cat.sources),'fragments':[],'requested_reading':'whole_task',
                      'focus_operations':focus_ops,'open_clues_allowed':True,
                      'over_target_reason':'retain_complete_source_once' if self._count(complete)>target else None}
            if focus and self._count({**complete,'primary_question':focus})<=target:
                complete['primary_question']=focus
                manifest['focus_delivery']='compact_source_locator'
            elif focus:
                short={'write':focus['write'],'use':focus['use']}
                if self._count({**complete,'primary_question':short})<=target:
                    complete['primary_question']=short
                    manifest['focus_delivery']='minimal_two_entry_locator'
                else:
                    manifest['focus_delivery']='summary_omitted_to_preserve_full_source'
            else:
                manifest['focus_delivery']='no_supported_meeting; source open'
            # The effect cards carry the exact applied positions of extra writes and exits.
            return complete,manifest
        # Structural degree and per-target round robin; never labels, file polarity or old hits.
        queues=[]
        for t in cat.targets:
            ordered=sorted((i for i,o in cat.operations.items() if o['target']==t),key=lambda i:(cat.operations[i].get('generated_getter',False),-len(cat.adj[i]),cat.name(i)))
            queues.append(deque(ordered))
        order=[]
        while any(queues):
            for q in queues:
                if q:order.append(q.popleft())
        value={**base,'source_fragments':[]};expanded=[];seen=set();partial=[]
        focus_missing=[];focus_placed=False
        if focus:
            closure,identities,focus_missing=cat.required_context(focus_ops)
            trial={**value,'primary_question':focus,'related_source':closure}
            if not focus_missing and self._count(trial)<=target:
                value=trial;focus_placed=True;expanded.extend(focus_ops)
                for frag in closure:
                    loc=frag['source'];seen.add((loc['file'],loc['start'],loc['length']))
            elif not focus_missing:
                focus_missing=[{'reason':'source_focus_closure_exceeds_soft_target','operations':focus_ops}]
        order=list(dict.fromkeys(focus_ops+order))
        for oid in order:
            c=self._model_card(oid);a=cat.operations[oid]['source'];loc=(a['file'],a['start'],a['length'])
            if loc in seen:
                # Share exact source bytes but retain each target application in the index/manifest.
                expanded.append(oid);continue
            candidate={**value,'source_fragments':value['source_fragments']+[c]}
            if self._count(candidate)<=target or (not value['source_fragments'] and self._count(candidate)<=limit):
                value=candidate;expanded.append(oid);seen.add(loc)
                for neighbor in cat.related(oid):
                    if neighbor in expanded:continue
                    nc=self._model_card(neighbor);na=cat.operations[neighbor]['source'];nl=(na['file'],na['start'],na['length'])
                    if nl in seen:expanded.append(neighbor);continue
                    trial={**value,'source_fragments':value['source_fragments']+[nc]}
                    if self._count(trial)<=target:value=trial;expanded.append(neighbor);seen.add(nl)
            if self._count(value)>=target:break
        # Oversized single functions: use whole AST statements, explicitly recording partial scope.
        if not expanded and cat.program and hasattr(cat.program,'lookup'):
            for oid in order:
                o=cat.operations[oid];lookup=cat.program.lookup(oid);body=lookup.function(o['function'])
                for node in body.get('body',{}).get('statements',[]):
                    a=lookup.anchor(node);c={'anchor':cat.name(oid),'source':{k:v for k,v in a.items() if k!='ast_id'},
                        'code':cat.slice(a),'partial_function':True}
                    trial={**value,'source_fragments':value['source_fragments']+[c]}
                    if self._count(trial)<=target:value=trial;partial.append(oid)
                if partial:break
        for i,c in enumerate(value['source_fragments']):
            c['fragment']='S'+str(i+1);cat.labels[c['fragment']]=cat.resolve(c['anchor'])
            cat.label_locations[c['fragment']]=copy.deepcopy(c['source'])
        missing=sorted(set(cat.operations)-set(expanded))
        value['unexpanded_entry_count']=len(missing)
        # Exact missing IDs stay in the host manifest; all source names already
        # occur in the complete compact entry index, so do not duplicate them.
        return value,{'mode':'graph_source_fragments','expanded_operations':sorted(set(expanded)),
            'partially_expanded_operations':sorted(set(partial)),'unexpanded_operations':missing,
            'requested_reading':'delivered_scope','focus_operations':focus_ops,'focus_context_gaps':focus_missing,
            'focus_delivery':'source_closure' if focus_placed else 'open_source_view','open_clues_allowed':True,
            'complete_source_files':[],'fragments':[{'fragment':c['fragment'],'anchor':c['anchor'],'partial':c.get('partial_function',False)} for c in value['source_fragments']]}
    def focused(self,feedback):
        base={'presentation':VERSION,'task':self.program.options.scope,
              'purpose':'Revise only these issues using the original source and new local evidence; omitted issues remain.',
              'source_and_explanation_are_distinct':True,'questions':[]}
        complete={**base,'source_files':[{'file':f,'content':s['content']} for f,s in self.catalog.sources.items()]}
        units=[];deduplicated=0;selected_entities={};shared_consumers={}
        host_questions={};observed_amount_disputes=set()
        for q in feedback['questions']:
            item=copy.deepcopy(q);ops=item.pop('operations',[])
            requested=item.pop('requested_effects',[])
            if requested:item['effect']='effect:'+requested[0][2:14]
            for qrow in item.get('semantic_questions',[]):
                host_questions[qrow['id']]=qrow
                if qrow.get('_observed_amount_dispute'):
                    observed_amount_disputes.add((q['id'],qrow['id']))
            for field in ('sent_evidence','sent_semantics','sent_message_identity','internal_external_caller_contexts'):
                item.pop(field,None)
            # Only byte/structure-equivalent evidence is merged. Caller, key,
            # branch, assumptions and formula identity remain part of equality.
            for e in item.get('evidence',[]):
                for field in ('probe_results','comparisons'):
                    if not isinstance(e.get(field),list):continue
                    rows={}
                    for v in e[field]:rows.setdefault(digest(v),v)
                    deduplicated+=len(e[field])-len(rows);e[field]=list(rows.values())
            for field in item.get('evidence',[]):
                if 'probe_results' in field:
                    field['probe_results']=[{k:p[k] for k in ('id','label','answer','bounded_condition_confirmed') if k in p} for p in field['probe_results']]
            fragments,identity,missing=self.catalog.required_context(ops)
            item['entry_identity_facts']=[{k:v for k,v in r.items() if k in ('anchor','entry_kind','declaring_contract','applied_target','constructor_declarations')} for r in identity]
            choices=item.get('semantic_questions',[])
            if not choices:units.append((q['id'],item,ops,fragments,missing))
            for proposal in choices:
                visible={k:proposal[k] for k in ('id','kind','question','choices','source_name','target') if k in proposal}
                if proposal.get('quantity_scope'):
                    visible['scope']='same holder-issued grant, spender, unit and request at this use'
                units.append((q['id'],dict(item,semantic_questions=[visible]),ops,fragments,missing))
        # A model decision is useful when competing readings predict different
        # consequences, or a still-unbound right/policy controls the judgment.
        # A local type error or an already-settled scalar fact is not a reason
        # to spend the remaining response. Source order breaks equal priority.
        def priority(unit):
            item=unit[1]
            # A typed, source-bound missing meaning is directly answerable.
            # A generic neutral task disagreement must not consume the only
            # revision while an actual amount/policy question remains unsent.
            return (not bool(item.get('audit_ref') and item.get('evidence') and item.get('alternative')),
                    not any((unit[0],q.get('id')) in observed_amount_disputes for q in item.get('semantic_questions',[])),not any(q.get('kind')=='scoped_support_dispute' for q in item.get('semantic_questions',[])),not bool(item.get('local_effect_review') or item.get('semantic_questions')),
                    not bool(item.get('task_conflict') or item.get('alternative') and item.get('evidence')),
                    not bool(item.get('alternative')))
        units.sort(key=priority)
        value={**base,'related_source':[]}
        selected=[];omitted=[];used=set();seen={};full_mode=False
        for qid,item,ops,fragments,missing in units:
            semantic=item.get('semantic_questions',[])
            decision=digest([sorted(ops),item.get('category'),item.get('claim'),item.get('alternative'),
                item.get('distinguishing_question'),[s.get('id') for s in semantic],item.get('evidence')])
            descriptor=host_questions.get(semantic[0]['id']) if semantic else None
            entity_key=digest([descriptor.get(k) for k in ('kind','target','operation','cell','semantic_scope','quantity_scope','choices')]) if descriptor and descriptor.get('kind') in ('financial_consent','authorization','resource') else None
            if entity_key in selected_entities and entity_key is not None:
                shared_consumers.setdefault(selected_entities[entity_key],[]).append(qid)
                omitted.append({'issue':qid,'reason':'shared_displayed_source_question','representative':selected_entities[entity_key]})
                continue
            if decision in seen:
                omitted.append({'issue':qid,'reason':'same_dispute_and_evidence','representative':seen[decision]});continue
            if selected:
                omitted.append({'issue':qid,'reason':'independent_dispute_retained_locally','priority':list(priority((qid,item)))})
                continue
            if not (semantic or item.get('local_effect_review') or item.get('task_conflict') or item.get('alternative') and item.get('evidence')):
                omitted.append({'issue':qid,'reason':'no_unresolved_semantic_distinction'});continue
            # Prefer the actual dependency closure of the single disputed effect.
            merged={}
            for frag in fragments:
                k=digest(frag['source'])
                if k in merged:merged[k]['targets']=sorted(set(merged[k]['targets']+frag['targets']))
                else:merged[k]=copy.deepcopy(frag)
            local={**base,'questions':[item],'related_source':list(merged.values())}
            full={**complete,'questions':[item]}
            local_tokens=self._count(self._share(local)) if merged and not missing else None
            full_tokens=self._count(self._share(full))
            full_mode=local_tokens is None or full_tokens<=local_tokens
            trial,tokens=(full,full_tokens) if full_mode else (local,local_tokens)
            if not merged and missing and tokens>self.program.options.input_limit:
                omitted.append({'issue':qid,'reason':'required_context_unavailable','actual_trial_input_tokens':tokens})
                continue
            if tokens<=self.program.options.input_limit:
                value=trial;selected.append(qid);used.update(ops);seen[decision]=qid
                if entity_key:selected_entities[entity_key]=qid
            else:omitted.append({'issue':qid,'reason':'whole_required_source_and_evidence_unit_exceeds_remaining_capacity',
                                 'actual_trial_input_tokens':tokens,'input_limit':self.program.options.input_limit})
        value=self._share(value)
        visible={};semantic_wire={}
        for question in value['questions']:
            labels={}
            for field in question.get('evidence',[]):
                row=value.get('shared_rows',{}).get(field.get('shared'),field)
                if isinstance(row.get('id'),str):
                    labels[row['id']]=[p['id'] for p in row.get('probe_results',[]) if 'id' in p]
            visible[question['id']]=labels
            for supplied in question.get('semantic_questions',[]):
                row=value.get('shared_rows',{}).get(supplied.get('shared'),supplied)
                if row.get('id'):
                    semantic_wire[row['id']]={'display':digest(row),'entity':question_entity(host_questions[row['id']]),'issue':question['id']}
        return value,{'mode':'focused_evidence','source_mode':'complete_source_once' if full_mode else 'compiler_bound_local_context',
            'disputed_effects':sorted({e for sid in semantic_wire for e in host_questions[sid].get('affected_effects',[])}|{e for q in feedback['questions'] if q['id'] in selected for e in q.get('requested_effects',())}),'shared_question_consumers':shared_consumers,'wire_evidence':visible,'semantic_wire':semantic_wire,'shared_row_count':len(value.get('shared_rows',{})),
            'selected_issues':selected,'unexpanded_feedback_issues':omitted,'expanded_operations':sorted(used),
            'selection_rule':'one_source_scoped_decision; capacity and complete necessary context checked per candidate',
            'complete_source_files':sorted(self.catalog.sources) if full_mode else [],'deduplicated_exact_evidence_rows':deduplicated,
            'necessary_context_not_silently_clipped':True,'no_full_facts_or_graph_or_unrelated_history':True}
    def visible_semantics(self,data,manifest,operations,feedback=False):
        rules=getattr(self,'rules',None)
        if not rules:return
        manifest['visible_spans']=[x['source'] for field in ('source_fragments','related_source') for x in data.get(field,[]) if isinstance(x.get('source'),dict)]
        cards,index=rules.cards_for(manifest,operations)
        selected=[]
        base=self._count(data)
        room=min(self.program.options.input_limit-base,max(128,min(self.program.options.input_target//12,base//5)))
        total=0
        for card in cards:
            size=len(self.counter.plain_tokenizer.encode(json.dumps(card,ensure_ascii=False,separators=(',',':')),add_special_tokens=False).ids)+1
            if total+size+8>room:continue
            selected.append(card);total+=size
        while selected and self._count(dict(data,typed_refs=selected))>base+room:selected.pop()
        if selected:data['typed_refs']=selected
        manifest['typed_index']={c[0]:index[c[0]] for c in selected}
        manifest['registered_sensitive_effects']=len(rules.sensitive_effects)
        manifest['displayed_effect_handles']=[index[c[0]] for c in selected if index[c[0]] in rules.effects]
        manifest['omitted_effect_handles']=sorted(set(rules.sensitive_effects)-set(manifest['displayed_effect_handles']))
        if feedback:
            wire={}
            chosen_effects=set(manifest.get('disputed_effects',()))
            relevant_supports=rules.support_inputs(chosen_effects)
            def in_chosen(entry):
                if not chosen_effects:return True
                handle=rules.facts[entry['fact']]['handle']
                if entry['support'] in relevant_supports or handle in chosen_effects:return True
                fact=rules.facts[entry['fact']]
                # An unresolved input cannot propagate an affirmative fact yet. It can
                # still answer the same disputed output when the compiler records an
                # exact scoped value route (e.g. a parameter copied into the balance).
                return fact['meaning'] in ('unknown','other_source_meaning','other_source_policy') and any(
                    effect in chosen_effects and exact and kind=='value' and fact['scope'] in (None,effect)
                    for effect,kind,_,exact in rules.routes.get(handle,()))

            for oid in operations:wire.update(rules.labels_for(oid,manifest))
            shown={};exposed=[]
            for ref,entry in sorted(wire.items()):
                if not rules.remaining():break
                if not in_chosen(entry):continue
                locator='effect' if entry['field']=='policies' else 'on'
                card={'ref':ref,locator:entry['source'],'meaning':entry['meaning']}
                card.update({key:entry[key] for key in ('role','subject','scope','payment_policy') if entry.get(key)})
                if self._count(dict(data,supports=exposed+[card]))>self.program.options.input_limit:continue
                exposed.append(card);shown[ref]=entry
            if exposed:
                data['supports']=exposed;manifest['shown_supports']=shown
            manifest['semantic_supports_omitted']=len(wire)-len(shown)
    def messages(self,feedback=None,recovery=False):
        if recovery:
            if self.initial_view is None:self.initial_view,self.initial_scope=self.initial()
            data=copy.deepcopy(self.initial_view);data['purpose']='protocol_recovery'
            if feedback and feedback.get('binding_diagnostics'):
                data['binding_diagnostics']=copy.deepcopy(feedback['binding_diagnostics'])
            manifest={**copy.deepcopy(self.initial_scope),'mode':'protocol_recovery_reused_source','reused_initial_source_view':True}
        elif feedback is None:
            if self.initial_view is None:self.initial_view,self.initial_scope=self.initial()
            data,manifest=copy.deepcopy(self.initial_view),copy.deepcopy(self.initial_scope)
        else:data,manifest=self.focused(feedback)
        operations=manifest.get('focus_operations',[]) if feedback is None or recovery else manifest.get('expanded_operations',[])
        self.visible_semantics(data,manifest,operations,feedback is not None and not recovery)
        manifest['offered_audit_refs'] = [q['audit_ref'] for q in data.get('questions',())
                                          if q.get('audit_ref') and q.get('audit_ref') == q['id']]
        if any(q.get('local_effect_review') and q.get('effect') not in manifest.get('typed_index',{}) for q in data.get('questions',())):
            manifest['selected_issues']=[]
        messages=self._messages(data,recovery);manifest.update(input_tokens=self.counter.count(messages),
            counter_identity=self.counter.identity,messages_sha256=digest(messages),
            counting_scope='complete V4.1 text message envelope including high/JSON markers; offline count, service usage recorded separately')
        manifest['sent_semantic_rows']={row['id']:row for item in data.get('questions',[]) for ref in item.get('semantic_questions',[])
            for row in [data.get('shared_rows',{}).get(ref.get('shared'),ref)] if 'id' in row}
        self.last_manifest=manifest
        return messages,manifest

```

## source/src/pr_next_joint/investigation/contracts.py

原文件SHA256 `ed3733795f4a0a3f006cba7a7bb823b170c0f9f1588d333af87bf22c74aedd29`

```python
"""Finite investigation controls and host-owned artifacts; no business detectors."""
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib, json, os, tempfile
from pr_next_joint.core import digest

VERSION = 'permission-risks-sp200-simplification-r2'
CATEGORIES = ('AC','FCR-TRANSFER','FCR-MINT','FCR-DESTROY','FCR-PAUSE','FCR-FREEZE')

def ident(prefix, value): return prefix+'_'+digest(value)[:20]

def write(path, value):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    data=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
    fd,tmp=tempfile.mkstemp(prefix='.'+path.name,dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as stream:stream.write(data);stream.flush();os.fsync(stream.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
    return hashlib.sha256(data).hexdigest()

@dataclass(frozen=True)
class Options:
    scope: str = 'AC'
    max_paths: int = 48
    input_target: int = 16384
    input_limit: int = 32768
    output_limit: int = 32768
    attempt_limit: int = 2
    feedback: bool = True
    prefix_depth: int = 2
    max_prefixes: int = 24
    max_actions: int = 64
    solver_timeout_ms: int = 3000
    seconds: float = 120
    def __post_init__(self):
        if self.scope not in ('AC','FCR'):raise ValueError('single_AC_or_FCR_task_required')
        if not 1<=self.max_paths<=96:raise ValueError('path_bound')
        if (self.input_target,self.input_limit,self.output_limit)!=(16384,32768,32768):raise ValueError('frozen_message_limits')
        if self.attempt_limit not in (1,2) or not 0<=self.prefix_depth<=2 or not 1<=self.max_prefixes<=64:raise ValueError('frozen_call_or_prefix_bound')
        if not 1<=self.max_actions<=256 or not 0<self.seconds<=900 or not 0<self.solver_timeout_ms<=20000:raise ValueError('frozen_investigation_bound')
    def record(self):return asdict(self)

```

## source/src/pr_next_joint/investigation/coverage.py

原文件SHA256 `ed1d198fe9d56b5476b9d05bd8960006dfc3565bb0ffcf58861e1cff824bda35`

```python
"""Property dependency accounting, separate from findings and risk definitions."""
from .contracts import CATEGORIES
from pr_next_joint.frontend.path_ir import walk
from .protocol import category_scope
from .request_scope import coverage_facts, claim_entries, privileged_intervention
from .ledger import movements, unit_origin, native_only_position
from .roles import path_qualification
from .initial_state import domain, initial_for_lookup
from pr_next_joint.frontend.storage import selectors, keys, value_type

HARD = {'original_root_has_no_committing_path','original_root_net_effect_is_unchanged',
        'same_scope_actual_full_settlement','single_holder_scope_not_collective_pause',
        'same_control_has_no_dependency_on_declared_entry_effect',
        'matched_direct_effect_impossible_on_all_applicable_positions_and_paths',
        'authorization_acquisition_premise_refuted','expected_authorization_covers_all_applicable_paths',
        'source_supported_applicable_normal_authorization'}
UNKNOWN = {'source_identity_ambiguous_or_unresolved','minimum_source_inspection_not_executed',
           'unique_critical_external_guard_not_established','signature_dependent_success_not_verified',
           'E1_cumulative_numeric_bound_mapping_pending','financial_intervention_source_unresolved'}


def possible_properties(inv, entries):
    if inv.f.options.scope == 'AC':return ['AC']
    from .scope_relevance import directory
    from pr_next_joint.core import digest
    cache=inv.__dict__.setdefault('_directory_certificates',{})
    controls=_control_categories(inv);cats=set()
    for oid in entries:
        if oid not in inv.f.operations:continue
        token=(inv.semantics.dependency_identity([oid]),digest(inv.semantics.active_scope),oid)
        if token not in cache:cache[token]=directory(inv,oid,controls.get(oid,[]))
        cats.update(cache[token]['possible_categories'])
    return sorted(cats)


def _control_categories(inv):
    from pr_next_joint.core import digest
    from pr_next_joint.frontend.storage import selector_relation
    from .ledger import native_only_position
    from .key_roles import relation
    from .scope_relevance import potential_role
    stamp=(inv.f.identity,inv.semantics.rules.epoch)
    cached=getattr(inv,'_coverage_control_index',None)
    if cached and cached[0]==stamp:return cached[1]
    inv._coverage_control_routes={}
    f=inv.f;index={};writers={}
    for w in f.writes.values():
        token=(f.operations[w['operation']]['target'],w['raw']['path']['root'])
        writers.setdefault(token,[]).append(w)
    for use,entry in f.operations.items():
        for _,p in f.operation_paths(use,True):
            # Immutable structural index. Currency semantics are read by the local consumer.
            minus=[c for c in movements(inv.backend,use,p)['-'] if not (relation(c,f.lookup(use)) or {}).get('kind')=='authorization_quantity']
            if not minus:continue
            for control in selectors(p['guards']):
                typ=value_type(control,f.lookup(use)) or ''
                if typ!='bool' and not typ.startswith(('uint','int')):continue
                # Ledger sufficiency is not a distinct freeze/pause control.
                if any(selector_relation(control,c)=='same_shape' for c in minus):continue
                if (relation(control,f.lookup(use)) or {}).get('kind')=='authorization_quantity':continue
                for w in writers.get((entry['target'],control['root']),[]):
                    writer=w['operation']
                    if writer==use:continue
                    if selector_relation(w['raw']['path'],control)!='same_shape' or inv.graph._disjoint_keys(w['raw']['path'],control):continue
                    if potential_role(f,writer,f.paths[w['path']]['raw']):
                        from .dependencies import control_candidates
                        from .summary import holder
                        for cat in control_candidates(control,[holder(c,f.lookup(use)) for c in minus]):
                            index.setdefault(use,set()).add(cat);index.setdefault(writer,set()).add(cat)
                            inv.__dict__.setdefault('_coverage_control_routes',{}).setdefault((writer,cat),set()).add(use)
    inv._coverage_control_index=(stamp,index)
    return index








from .source_opinion import describe, simple_holder_grant
from .summary import local_delta
from pr_next_joint.core import digest

def basic_entry(inv,oid,rows,cat,effect_locations=None):
    """Read concrete declaration effects before assigning any category eligibility.

    Produces a detection opinion for this family, not an absence proof.
    In particular an opinion about one entry cannot read another target by proxy.
    """
    from .summary import local_delta,holder
    from .policy_binding import conjuncts
    from .source_opinion import office_use,quantity_forced_zero,identity_guard,role_ids
    from .initial_state import initial_for_lookup
    from pr_next_joint.frontend.path_ir import key
    from pr_next_joint.frontend.storage import value_type
    f=inv.f;lk=f.lookup(oid);entry=f.operations[oid]
    committing=[r for r in rows if r['committing']]
    if not rows:return 'unread','not_reviewed'
    if cat=='AC':
        from .source_opinion import handover,covered_delegation
        if handover(inv,oid,committing):return 'reviewed','nominee_acceptance'
        if covered_delegation(inv,oid,committing) and not any(r['effects'] for r in committing):return 'reviewed','covered_holder_grant'
        for r in committing:
            for w in r['ordered_writes']:
                cell=w['path']
                if not keys(cell) and value_type(cell,lk) in ('address','address payable') and office_use(inv,oid,cell):
                    guards=[g for v in r['guards'] for g in conjuncts(v)]
                    if not any(identity_guard(g,{cell['root']}) for g in guards):
                        return 'dispute','unassessed_role_change'
            if any('selfdestruct' in str(e.get('kind','')).lower() for e in r['effects']):
                return 'dispute','policy_missing'
        if not committing:return ('reviewed','no_effect_in_scope') if rows and inv.backend.complete(oid) else ('unread','not_reviewed')
        # This finite AC opinion concerns the examined paths and effects only.
        if simple_holder_grant(inv,oid,rows):return 'reviewed','covered_holder_grant'
        if any(r['effects'] or r['residuals'] for r in committing):return 'dispute','policy_missing'
        rules=inv.semantics.rules
        if any(e in getattr(rules,'source_duties',{}) and
               (effect_locations is None or tuple(rules.effects[e]['where'].get(k) for k in ('file','start','length')) in effect_locations)
               for e in rules.by_operation.get(oid,())):
            return 'dispute','policy_missing'
        return 'reviewed','source_task_reading'
    if cat=='FCR-DESTROY' and committing and not entry['gaps'] and all(not r['effects'] and not r['residuals'] for r in committing):
        from .scope_relevance import potential_role
        from pr_next_joint.frontend.storage import selector_relation
        local_reasons=[]
        for r in committing:
            raw=f.paths[r['path']]['raw']
            accounts=[(w,local_delta(w)) for w in r['ordered_writes'] if holder(w['path'],lk) is not None]
            if not potential_role(f,oid,raw):
                local_reasons.append('no_privileged_intervention');continue
            if not accounts:
                # A downstream exchange-rate or unit dependency needs its own
                # intervention comparison; a scalar write alone is not a debit.
                if not any(peer!=oid and not f.operations[peer]['generated_getter'] for w in r['ordered_writes']
                           for peer in inv.graph.access.get((entry['target'],w['path']['root']),{}).get('readers',())):
                    local_reasons.append('no_debit_in_scope');continue
                break
            debits=[(w,qty) for w,(sg,qty) in accounts if sg=='-']
            if len(debits)!=1:break
            w,qty=debits[0];cell=w['path'];account=holder(cell,lk)
            if account.get('kind')=='actual_sender':
                local_reasons.append('voluntary_holder_debit');continue
            credits=[(c,v) for c,(sg,v) in accounts if sg=='+' and selector_relation(c['path'],cell)=='same_shape']
            if len(accounts)==2 and len(credits)==1 and key(credits[0][0]['path'])==key(cell) and key(credits[0][1])==key(qty):
                local_reasons.append('same_position_restored');continue
            break
        else:
            if local_reasons:return 'reviewed',local_reasons[0] if len(set(local_reasons))==1 else 'locally_excluded_holder_loss'
    from .source_opinion import paid_credit
    if cat=='FCR-MINT' and committing:
        if all(paid_credit(inv,oid,r) for r in committing):return 'reviewed','ordinary_paid_credit'
    if cat in ('FCR-FREEZE','FCR-PAUSE'):
        linked=inv.__dict__.get('_coverage_control_routes',{}).get((oid,cat),set())
        if linked:
            has_unit=any(unit_origin(inv.backend,use,cell) for use in linked for _,branch in f.operation_paths(use,True) for cell in movements(inv.backend,use,branch)['-'])
            return 'dispute','scope_missing' if has_unit else 'source_unit_missing'
        return 'reviewed','source_task_reading'
    if cat=='FCR-MINT':
        writers={w['path']['root'] for r in committing if role_ids(inv,oid,r) for w in r['ordered_writes']}
        if writers:
            for rid in writers:
                for use in inv.graph.access.get((entry['target'],rid),{}).get('readers',()):
                    if use==oid:continue
                    for branch in f.summaries.rows(use):
                        buy=paid_credit(inv,use,branch)
                        if buy and any(c['root']==rid for c in selectors(local_delta(buy)[1])):
                            return 'dispute','scope_missing'
    from .roles import effective_roots
    from .source_opinion import impossible_role
    for r in committing:
        qualified = role_ids(inv, oid, r)
        # A caller guard without a verified grant chain is still a live mint
        # candidate. A rejected refinement alone supplies no negative evidence.
        if not qualified and not (cat == 'FCR-MINT' and
                any(effective_roots(g, lk.nodes.keys()) for g in r['guards'])):
            from .scope_relevance import potential_role
            if cat in ('FCR-DESTROY','FCR-TRANSFER') and potential_role(f,oid,f.paths[r['path']]['raw']) and any(
                    holder(w['path'],lk) and local_delta(w)[0]=='-' and holder(w['path'],lk).get('kind')!='actual_sender'
                    for w in r['ordered_writes']):
                return 'dispute','role_provenance_unresolved'
            continue
        from .scope_relevance import nonfinancial
        effects=[(w,*local_delta(w)) for w in r['ordered_writes']
                 if holder(w['path'],lk) is not None and not nonfinancial(inv.backend,oid,w['path'])]

        guards=[g for t in r['guards'] for g in conjuncts(t)]
        for w,sign,amount in effects:
            if effect_locations is not None and tuple(w['source'].get(k) for k in ('file','start','length')) not in effect_locations:continue
            if sign not in ('+','-') or not amount:continue
            ac=holder(w['path'],lk);others=[(ow,os,oq) for ow,os,oq in effects if ow['path']['root']==w['path']['root'] and os!=sign]
            if quantity_forced_zero(guards,amount,lk):continue
            matched=[ow for ow,os,oq in others if key(oq)==key(amount)]
            if not qualified:
                if sign != '+' or paid_credit(inv, oid, r) or impossible_role(inv, oid):
                    continue
                from pr_next_joint.frontend.storage import selector_relation
                same_family = [(ow, os, oq) for ow, os, oq in effects
                               if selector_relation(w['path'], ow['path']) == 'same_shape']
                if len(same_family) == 2 and any(os == '-' and key(oq) == key(amount)
                                                for _, os, oq in same_family):
                    continue
                return 'dispute', 'mint_role_provenance_unresolved'
            reason='scope_missing' if unit_origin(inv.backend,oid,w['path']) else 'source_unit_missing'
            if cat=='FCR-MINT' and sign=='+' and not matched:return 'dispute',reason
            if cat=='FCR-TRANSFER' and sign=='-' and matched and ac.get('kind')!='actual_sender':
                return 'dispute',reason
            if cat=='FCR-DESTROY' and sign=='-' and ac.get('kind')!='actual_sender' and not matched:
                return 'dispute',reason
    return 'reviewed','source_task_reading'


def obligation_scope(inv, assessments, blocked):
    """Record actual source readings, independent of optional proof completion."""
    categories = tuple(CATEGORIES[1:]) if inv.f.options.scope == 'FCR' else ('AC',)
    manifest=inv.initial_manifest or {}
    delivered=set(manifest.get('expanded_operations',()))-set(manifest.get('partially_expanded_operations',()))
    by_entry={}
    local={}
    gaps=[]
    normal=[]
    agenda=[]
    scope_skips=set()
    seen_gaps=set()
    open_cats=set()
    def gap(oid, cats, reason, issues=()):
        affected=sorted(set(cats)&set(categories))
        if not affected:return
        token=(oid,tuple(affected),reason)
        if token in seen_gaps:return
        seen_gaps.add(token);open_cats.update(affected)
        obj=inv.f.operations.get(oid,{})
        gaps.append(dict(id='gap_'+digest(token)[:16],target=obj.get('target'),operations=[oid] if oid else [],
                         location=obj.get('source',{}),closed=False,affected_categories=affected,
                         reason=reason,issues=list(issues),explanation=describe(affected[0],reason)))
    for qid,q in inv.issues.items():
        a=assessments[qid];cat=a.get('category')
        status=a['scope'].get('route_status')
        decision=a['scope']['decision']
        root=inv.root(q)
        if status=='superseded':continue
        record={'issue':qid,'category':cat,'state':decision['status'],'reason':decision['reason'],
                'closed':decision['status'] in ('risk','normal','excluded'),'entries':[root] if root else [],
                'affected_categories':[]}
        exact=q['current'].get('_scope_effects') or q.get('effect_scope') or []
        by_location={tuple(r.get(k) for k in ('file','start','length')) for r in decision.get('locations',())}
        record['effects']=sorted(set(exact) or {e for e in inv.semantics.rules.by_operation.get(root,()) if
            tuple(inv.semantics.rules.effects[e]['where'].get(k) for k in ('file','start','length')) in by_location})
        local[qid]=record
        if root:by_entry.setdefault(root,[]).append(record)
        if root is None and q['current'].get('assessment')=='risk':
            for candidate in q.get('binding',{}).get('operations',()):
                gap(candidate,category_scope(q['current'],inv.f.options.scope),'core_mismatch',[qid])
    checked=0;obligations=[]; basic_cache=inv.__dict__.setdefault('_basic_entry_opinions',{})
    rules=inv.semantics.rules
    expanded_all=manifest.get('mode')=='complete_source'
    for oid,entry in inv.f.operations.items():
        cats=set(categories)
        states={};related=by_entry.get(oid,[])
        local_counts=[x for x in related if x['reason']=='scoped_counter' and x['state']=='normal']
        rows=inv.f.summaries.rows(oid,False)
        # A generated getter is still a compiler declaration. Inspect real rows or that declaration.
        read=bool(rows or entry['generated_getter']) and oid not in rules.incomplete
        cache=inv.__dict__.setdefault('_scope_candidates',{})
        if categories!=('AC',):
            if oid not in cache and inv.program_remaining()<=0:
                gap(oid,categories,'not_reviewed');continue
            stamp=(inv.semantics.dependency_identity([oid]),digest(inv.semantics.active_scope))
            if cache.get(oid,(None,))[0]!=stamp:
                cache[oid]=(stamp,set(possible_properties(inv,{oid})))
            cats=cache[oid][1]
        explicit=set(x['category'] for x in related if x['category'] in categories)
        if any(x['reason'] in ('conflicting_scoped_meanings','source_unit_missing') and not x['category'] for x in related):
            for x in related:
                if x['reason'] in ('conflicting_scoped_meanings','source_unit_missing'):
                    rules=inv.semantics.rules;q=inv.issues[x['issue']]
                    for e in (rules.disputed_effects(q) if x['reason']=='conflicting_scoped_meanings' else rules.route_scopes(q)):
                        w=inv.semantics.rules.effects[e].get('write')
                        if w is None:continue
                        sign,_=local_delta(w)
                        explicit.update(['FCR-MINT'] if sign=='+' else ['FCR-DESTROY','FCR-TRANSFER'] if sign=='-' else [])
                        gap(oid,['FCR-MINT'] if sign=='+' else ['FCR-DESTROY','FCR-TRANSFER'] if sign=='-' else [],x['reason'],[x['issue']])
        relevant=cats|explicit
        committed=[r for r in rows if r['committing']]
        opaque=any(r['residuals'] or r['flow']=='truncated' or any(e.get('kind')=='dangerous_external_call' for e in r['effects']) for r in rows) or bool(entry['gaps'])
        no_effect=read and not opaque and (entry['generated_getter'] or not any(r['ordered_writes'] or r['effects'] for r in committed))
        unresolved_key_only=bool(rows) and not entry['gaps'] and not any(r['effects'] or r['flow']=='truncated' for r in rows) and all(
            x.get('reason')=='multiple_address_keys_need_source_holder_binding' for r in rows for x in r['residuals'])
        frontier=any(r['flow']=='truncated' for r in rows) or any(g.get('kind') in ('path_extraction','source_expression_limit','dependent_source_expression_limit') for g in entry['gaps'])
        opaque_domain=frontier or any(call['mode']=='DELEGATECALL' and call['unresolved_implementation']
            for call in inv.f.call_summaries.rows.values() if call['operation']==oid)
        if opaque_domain:relevant.update(categories)
        has_view=expanded_all or oid in delivered
        for cat in sorted(categories):
            records=[x for x in related if x['category']==cat]
            active=[x for x in records if not inv.issues[x['issue']]['current'].get('_host_source_question') or
                    x['reason'] in ('conflicting_scoped_meanings','source_unit_missing','policy_scope_unsubstantiated','policy_effect_unresolved','holder_consent_basis_unresolved','unexpanded_source_dependency','role_provenance_unresolved','scope_missing') or
                    inv.issues[x['issue']]['current'].get('_semantic_consumer') and x['reason'] in ('policy_missing','external_dependency')]
            settled=[x for x in records if x['state'] in ('normal','excluded','risk')]
            covered={e for x in settled for e in x['effects']}
            outstanding=inv.semantics.rules.by_operation.get(oid,set())-covered
            decisive=[]
            for rec in active:
                if rec['state']!='open':continue
                model_issue=inv.issues[rec['issue']]
                prop=model_issue.get('property') or {}
                finance_q=any(s.get('kind')=='financial_consent' and s.get('quantity_scope') for s in prop.get('semantic_questions',[]))
                measured_unbound=any(
                    e.get('property_identity')==prop.get('id') and any(x.get('reason')=='holder_authorization_quantity_basis_unresolved' for x in e.get('local_errors',[]))
                    for label in model_issue['evidence'] for e in [inv.evidence[label]])
                consent_active=any(x.get('meaning')=='net_request_with_fee' and x.get('quantity_scope') for x in prop.get('consent_rows',[]))
                if cat in ('FCR-DESTROY','FCR-TRANSFER') and (finance_q or measured_unbound or consent_active) and rec['reason']=='scope_missing':
                    decisive.append(dict(rec,reason='holder_consent_basis_unresolved'));continue
                if rec['reason']=='scope_missing' and cat in ('FCR-DESTROY','FCR-TRANSFER','FCR-MINT'):
                    # A located unsettled financial effect is not an optional plan.
                    # Do not turn every open into a global veto: require an actual
                    # uncovered effect of this category on the committing entry.
                    selected=set(rec['effects']) or set(inv.semantics.rules.route_scopes(inv.issues[rec['issue']]))
                    live=selected-covered
                    if live and any(e in rules.effects and 'write' in rules.effects[e] and
                        ((cat=='FCR-MINT' and local_delta(rules.effects[e]['write'])[0]=='+') or
                         (cat!='FCR-MINT' and local_delta(rules.effects[e]['write'])[0]=='-')) for e in live):
                        decisive.append(rec);continue
                if rec['reason'] not in (
                    'conflicting_scoped_meanings','source_unit_missing','policy_effect_unresolved','external_dependency',
                    'policy_missing','policy_scope_unsubstantiated','revised_policy_not_read','holder_consent_basis_unresolved','unexpanded_source_dependency','role_provenance_unresolved'):continue
                if not rec['effects'] or not set(rec['effects'])<=covered:decisive.append(rec)
            base_status,base_reason='unread','not_reviewed'
            read_effects=set(rules.by_operation.get(oid,()))
            local_opaque=opaque and (opaque_domain or cat in relevant and
                (not outstanding or any(inv.f.call_summaries.effect_dependencies(r,rules.effects[e])
                 for e in outstanding for r in rows if rules.effects[e].get('path')==r['path'] or r['path'] in rules.effects[e].get('branches',{}))))
            local_complete=not outstanding and bool(covered) and not opaque_domain
            # basic_entry reasons about the actual writes and program guards. It does
            # not consume a mutable normative consent, which is applied separately below.
            from .source_opinion import reading_version
            depend=reading_version(inv,[oid],cat) if (oid,cat) in inv.__dict__.get('_coverage_control_routes',{}) else None
            basic_key=(oid,cat,tuple(sorted(outstanding)),stamp if categories!=('AC',) else None,depend)
            from .scope_relevance import detached_holder_switch
            detached=(cat=='FCR-FREEZE' and read and detached_holder_switch(inv,oid))
            if detached:
                base_status,base_reason='reviewed','detached_local_holder_switch'
            elif read and no_effect:
                base_status,base_reason='reviewed','no_effect_in_scope'
            elif read and cat=='FCR-MINT' and not opaque and any(n.get('kind')=='transaction_value' for r in committed for w in r['ordered_writes'] for n in walk(w['value'])) and basic_entry(inv,oid,rows,cat)==('reviewed','ordinary_paid_credit'):
                base_status,base_reason='reviewed','ordinary_paid_credit'
            elif read and cat not in relevant and not opaque_domain:
                base_status,base_reason='reviewed','necessary_effect_absent'
            elif read and local_complete:
                base_status,base_reason='reviewed','effect_range_decided'
            elif not has_view and not local_complete:
                base_reason='source_context_missing'
            elif local_opaque and not (unresolved_key_only and (cat not in cats or simple_holder_grant(inv,oid,rows))):
                base_reason='external_dependency'
            elif read and (basic_key in basic_cache or inv.program_remaining()>0):
                if basic_key not in basic_cache:
                    # Keep companion writes and guards as dependencies of the remaining effect.
                    locs=None
                    if covered and outstanding:
                        locs={tuple(rules.effects[e]['where'].get(k) for k in ('file','start','length')) for e in outstanding}
                    basic_cache[basic_key]=basic_entry(inv,oid,rows,cat,locs)
                base_status,base_reason=basic_cache[basic_key]
            elif not read:base_reason='source_context_missing'
            reason=base_reason if base_status!='reviewed' else None
            if decisive and not detached and not no_effect and (cat in relevant) and base_reason!='nominee_acceptance':
                reason=decisive[0]['reason']
            if reason:
                gap(oid,[cat],reason,[x['issue'] for x in decisive])
                effects={e for record in decisive for e in record['effects']} or outstanding
                states[cat]={'state':'open','basis':reason,'effect_ids':sorted(effects)}
            else:
                states[cat]={'state':'reviewed','basis':base_reason}
            identity=(oid,cat,tuple(sorted(outstanding)))
            if reason in ('scope_missing','source_unit_missing','policy_missing','unassessed_role_change') and not local_opaque and identity not in scope_skips:
                agenda.append({'operation':oid,'category':cat,'effects':sorted(outstanding),'dependency':reason})
                scope_skips.add(identity)
        if any(s['state']=='reviewed' for s in states.values()) or any(rec['closed'] for rec in related):checked+=1
        affected=[c for c in categories if states[c]['state']=='open']
        obligations.append({'id':'obligation_'+digest([inv.f.identity,entry['target'],oid])[:20],
            'target':entry['target'],'operations':[oid],'location':entry['source'],'possible_categories':sorted(relevant),'source_candidate_categories':sorted(cats),'bound_question_categories':sorted(explicit),'category_states':states,
            'closed':not affected,'affected_categories':affected,'entry_states':[{'operation':oid,'states':{c:states[c]['state'] for c in categories}}]})
    if not checked:gap(None,categories,'not_reviewed')
    eligible=sorted(set(categories)-open_cats)
    for cat in eligible:
        if not any(x['category']==cat and x['state']=='risk' for x in local.values()):
            matched=[r for r in local.values() if r['category']==cat and r['state'] in ('normal','excluded')]
            reasons=sorted({r['reason'] for r in matched})
            patterns=sorted({s['category_states'][cat]['basis'] for s in obligations if cat in s['category_states'] and s['category_states'][cat].get('basis')})
            explanation=describe(cat,reasons[0] if reasons else patterns[0] if len(patterns)==1 else 'source_task_reading')
            normal.append({'category':cat,'reason':'source_task_reading','applied_reasons':reasons or patterns,
                           'effects':sorted({e for r in matched for e in r['effects']}),'explanation':explanation})
    return {'schema':'source-category-decision-r1','request_scope':manifest.get('requested_reading'),
            'whole_reading_eligible':bool(checked and not open_cats),
            'negative_eligible_categories':eligible,'known_category_gaps':gaps,'category_readings':normal,
            'source_local_scopes':local,'obligations':obligations,'neutral_scope_scan_executed':bool(checked),
            'basic_source_entries_read':checked,'source_opinion_available':bool(checked),'refinement_requests':agenda,
            'delivery_and_model_declaration_are_not_completion':True}

```

## source/src/pr_next_joint/investigation/decision_output.py

原文件SHA256 `cd193e366ad47593945dfa3006664329bff721d9718705927f2d840a60026a5b`

```python
"""Fixed decision-only output contract; no detailed-output switch.

The verifier does not extract assignments. This independent output boundary
keeps classifications, source locations, bounded statuses, coverage and cost
receipts. Solver problems, ordered frames and raw model bodies are not saved.
"""
import copy
import re
from pr_next_joint.core import digest

PROFILE = 'risk_decision_only_v1'

def code(value, fallback='unclassified_diagnostic'):
    return value if isinstance(value,str) and re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.:-]{0,159}',value) and not re.search(r'0x[0-9a-fA-F]{8,}',value) else fallback

def codes(values):
    return [code(v) for v in values if isinstance(v,str)] if isinstance(values,list) else []

def location(value):
    if not isinstance(value,dict):return {}
    out={'file':value['file']} if isinstance(value.get('file'),str) else {}
    out.update({k:value[k] for k in ('start','length','ast_id','line','column') if type(value.get(k)) is int})
    return out

def receipt(value,purpose):
    return {'profile':PROFILE,'purpose':purpose,'content_sha256':digest(value),'body_retained':False}

def safe_issue_id(value):
    """Source-visible model IDs may contain arbitrary strings; keep only inert IDs on disk."""
    if isinstance(value,str) and re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.:@-]{0,90}',value) and not re.search(r'0x[0-9a-f]{8,}|[a-f0-9]{40,}',value,re.I):
        return value
    return 'issue_'+digest(value)[:20]

def diagnostic(row):
    if not isinstance(row,dict):return {'reason':code(row),'detail_sha256':digest(row)}
    previous=row.get('detail_sha256')
    out={'reason':code(row.get('reason',row.get('kind'))),'detail_sha256':previous if isinstance(previous,str) and re.fullmatch('[0-9a-f]{64}',previous) else digest(row)}
    for k,allowed in {'stage':{'initial','protocol_recovery','focused_revision'},'list':{'issues','answers','annotations','policies','reviewed','hypotheses'},
                      'field':{'on','effect','meaning','ref','role','subject','basis','question','assessment','category','action'},
                      'subreason':{'field_absent','wrong_field_type','invalid_locator','outside_facet_vocabulary','missing_source_reason','undisplayed_reference','source_binding'},
                      'actual_type':{'str','list','dict','NoneType','bool','int','float'}}.items():
        if row.get(k) in allowed:out[k]=row[k]
    field_path=row.get('field_path')
    if isinstance(field_path,str) and re.fullmatch(r'[a-z_]{1,32}(?:\.[a-z_]{1,32}|\[\])?',field_path):
        out['field_path']=field_path
    ordinal=row.get('index',row.get('item',row.get('answer')))
    if type(ordinal) is int:out['index']=ordinal
    if type(row.get('value_length')) is int:out['value_length']=row['value_length']
    if isinstance(row.get('value_sha256'),str) and re.fullmatch('[0-9a-f]{64}',row['value_sha256']):out['value_sha256']=row['value_sha256']
    if 'list' in out:
        out['contract']='scoped_json_r2'
        if 'field' in out:out['expected_type']='str'
    if 'issue' in row:out['issue']=safe_issue_id(row['issue'])
    if 'category' in row:out['category']=code(row['category'])
    if isinstance(row.get('source'),dict):out['source_location']=location(row['source'])
    return out

def context_summary(value):
    out=receipt(value,'source_delivery_and_capacity')
    out.update({k:value[k] for k in ('input_tokens','input_target','input_limit','output_limit') if type(value.get(k)) is int})
    if isinstance(value.get('messages_sha256'),str):out['messages_sha256']=value['messages_sha256']
    if 'registered_sensitive_effects' in value:
        out['registered_sensitive_effects']=value['registered_sensitive_effects']
        out['displayed_effect_handles']=[code(h) for h in value.get('displayed_effect_handles',())]
    if 'omitted_effect_handles' in value:out['omitted_effect_handles']=[code(h) for h in value['omitted_effect_handles']]
    if 'typed_index' in value:out['typed_cards']=len(value['typed_index'])
    if 'shown_supports' in value:out['shown_supports']=len(value['shown_supports'])
    if 'semantic_supports_omitted' in value:out['omitted_supports']=value['semantic_supports_omitted']
    out['sent_question_bindings']=[{'display_sha256':v['display'],'entity_sha256':v['entity'],'consumers':1+len(set(value.get('shared_question_consumers',{}).get(v['issue'],()))-{v['issue']})} for v in value.get('semantic_wire',{}).values()]
    if value.get('mode'):out['mode']=code(value['mode'])
    if value.get('source_mode'):out['source_mode']=code(value['source_mode'])
    out['source_file_count']=len(value.get('complete_source_files',()))
    out['omission_reasons']=[code(x.get('reason')) for x in value.get('unexpanded_feedback_issues',())]
    for k in ('selected_issues','unexpanded_feedback_issues','omitted_operations','selected_operations'):
        if isinstance(value.get(k),(dict,list)):out[k+'_count']=len(value[k])
    return out

def property_summary(prop):
    if not isinstance(prop,dict):return None
    out={k:copy.deepcopy(prop[k]) for k in ('id','category','original_category','domain','operation',
         'semantic_version','task','property_family') if k in prop and isinstance(prop[k],(str,int,bool))}
    out['content_sha256']=digest(prop)
    return out

def scope_summary(scope):
    if not isinstance(scope,dict):return {}
    out={'scope_sha256':digest(scope)}
    for k in ('route_status','deployment_reachability_proved','entire_contract_safety_proved','analysis_domain','domain'):
        if k in scope and isinstance(scope[k],(str,bool)):out[k]=scope[k]
    if 'compiled_property' in scope:out['compiled_property']=property_summary(scope['compiled_property'])
    if 'decision' in scope:
        d=scope['decision']
        out['decision']={'status':code(d['status']),'reason':code(d['reason']),
                         'explanation':d['explanation'],'locations':[location(x) for x in d.get('locations',[])],
                         **{k:[code(i) for i in d.get(k,[])] for k in ('effects','rules','supports','facts','meanings','origins')}}
        for k in ('application_location','causal_root'):
            if d.get(k):out['decision'][k]=location(d[k])
        if d.get('source_edge_ids'):
            out['decision']['source_edge_ids']=codes(d['source_edge_ids'])
        if card := d.get('audit_card'):
            out['decision']['audit_card'] = {
                'kind':code(card['kind']), 'check':code(card['check']),
                'bound_effects':codes(card['bound_effects']),
                'source_relation_independent':bool(card['source_relation_independent']),
                'semantic_reading_used':bool(card['semantic_reading_used'])}
        if rel:=d.get('source_relation'):
            out['decision']['source_relation']={'family':code(rel['family']), 'duty':code(rel['duty']),
                                               'support_location':location(rel['support_location'])}
        if d.get('holder_family'):
            out['decision']['holder_family']={k:code(v) for k,v in d['holder_family'].items()}
        if d.get('opinion_source'):out['decision']['opinion_source']=code(d['opinion_source'])
        if d.get('protected_use'):out['decision']['protected_use']=location(d['protected_use'])
        if d.get('productive_use'):out['decision']['productive_use']=location(d['productive_use'])
        if d.get('basis_probe'):out['decision']['basis_probe']=code(d['basis_probe'])
        if d.get('conditional_agent'):
            alt=d['conditional_agent'];out['decision']['conditional_agent']={'scope':code(alt['scope']),'use':location(alt['use']),
                'requires_prior_holder_grant':True,'requires_exempt_spender':True,'availability':code(alt['availability'])}
    return out

def assessment_summary(value):
    return {'reportable':value.get('reportable') is True,'category':value.get('category'),
            'reasons':codes(value.get('reasons',[])),'scope':scope_summary(value.get('scope',{}))}

def query_summary(q):
    d=q.get('details',{})
    out={k:q[k] for k in ('id','label','answer','formula_sha256','bounded_condition_confirmed') if k in q}
    out.update(evidence_kind='bounded_condition_check_without_assignment_extraction',
               condition_identity=digest(d),model_extracted=False,formula_saved=False)
    keys=('property_validated','intermediate_value_carried','measurement_only','same_request','effect_required','new_authority_required',
          'downstream_effect_required','acquisition_use_required','baseline_commit_not_assumed',
          'no_universal_gross_allowance_policy','all_productive_paths_checked','all_continuations_exact',
          'original_all_positive_amount_obligation_preserved')
    criteria={k:d[k] for k in keys if type(d.get(k)) is bool}
    if d.get('corresponding_same_ledger_credit'):criteria['corresponding_same_ledger_credit']=True
    for k in ('category_hypothesis','property_identity'):
        if k in d:criteria[k]=code(d[k])
    binding=q.get('rebound_from')
    if binding:out['math_reuse']={k:v if k in ('math_key','binding_sha256') and re.fullmatch('[a-f0-9]{64}',v) else code(v) for k,v in binding.items() if isinstance(v,str)}
    if d.get('beneficiary_rule')=='controlled_or_self_only':criteria['beneficiary_rule']='controlled_or_self_only'
    out['criteria']=criteria
    for name,key in [('credential_status','credential'),('hash_status','hash_confirmation')]:
        out[name]={k:code(v) for k,v in q.get(key,{}).items() if k in ('status','reason')}
    cert=q.get('exclusion_certificate')
    if isinstance(cert,dict):
        out['exclusion_check']={k:cert[k] for k in ('answer','formula_ref','all_runtime_states_overapproximated',
            'excludes_only_this_formula','positive_result_usable') if k in cert}
    return out

def evidence_summary(evidence):
    return {label:{'kind':code(e.get('kind')),'content_sha256':digest(e),
        'queries':[query_summary(q) for q in e.get('queries',[])],
        'local_errors':[diagnostic(x) for x in e.get('local_errors',[])],
        'independent_use_checks':[{k:c[k] for k in ('status','supports_takeover') if k in c}
                                 for c in e.get('independent_use_checks',[])]}
        for label,e in evidence.items()}

def coverage_row(row):
    out={k:copy.deepcopy(row[k]) for k in ('id','target','closed','affected_categories','source_candidate_categories','bound_question_categories') if k in row}
    if row.get('operations'):out['operations']=codes(row['operations'])
    if row.get('location'):out['location']=location(row['location'])
    out['category_states']={c:{'state':code(s.get('state')),'basis':code(s.get('basis')),'detail_sha256':digest(s)}
                            for c,s in row.get('category_states',{}).items()}
    stages={'source_unit_missing':'unit_binding','not_reviewed':'source_reading','source_context_missing':'source_display','external_dependency':'external_effect','holder_consent_basis_unresolved':'authorized_quantity','policy_missing':'policy_binding','scope_missing':'effect_check'}
    for cat,item in out['category_states'].items():
        if item['basis'] in stages:item['first_observable_dependency']=stages[item['basis']]
        effects=row['category_states'][cat].get('effect_ids',[])
        if effects:
            item['open_effects']=codes(effects[:8])
            item['other_open_effect_count']=max(0,len(effects)-8)
    return out

def coverage_summary(value):
    return {'schema':'source-category-public-r1','whole_reading_eligible':value.get('whole_reading_eligible') is True,
        'negative_eligible_categories':copy.deepcopy(value.get('negative_eligible_categories',[])),
        'obligations':[coverage_row(row) for row in value.get('obligations',[])],
        'known_category_gaps':[dict(coverage_row(row),reason=code(row['reason']),location=location(row.get('location')),explanation=row['explanation']) for row in value.get('known_category_gaps',[])],
        'basic_source_entries_read':value.get('basic_source_entries_read',0),
        'category_readings':copy.deepcopy(value.get('category_readings',[])),
        'source_opinion_available':bool(value.get('source_opinion_available')),
        'neutral_scope_scan_executed':value.get('neutral_scope_scan_executed') is True,
        'content_sha256':digest(value),'delivery_and_model_declaration_are_not_completion':True}

def semantic_summary(record):
    out=receipt(record,'source_bound_semantic_interpretations')
    out['scoped_support']=copy.deepcopy(record.get('scoped_support',{}))
    out['answer_dispositions']=copy.deepcopy(record.get('answer_dispositions',[]))
    out['financial_consents']=[{'meaning':code(c.get('meaning')),'identity':digest(c)} for c in record.get('financial_consents',[])]
    return out

def public_report(report):
    if report.get('output_profile')==PROFILE:return copy.deepcopy(report)
    keep=('method','program_identity','task','options','effective_investigation_parameters','implementation_sha256','main_finding_ids',
          'additional_finding_ids','unresolved_mapping_ids','model_analysis_available','prediction_basis_available',
          'unresolved_category_judgments','prediction_frozen_before_gold','scoring_performed','timing')
    out={k:copy.deepcopy(report[k]) for k in keep if k in report}
    out.update(output_profile=PROFILE,replay_material_generated=False,concrete_execution_performed=False,
               risk_absence_statement='No risk detected in analyzed scope is not proof of safety.')
    out['prediction_basis_issues']=[safe_issue_id(x) for x in report.get('prediction_basis_issues',[])]
    out['findings']=[]
    for f in report.get('findings',[]):
        row={k:copy.deepcopy(f[k]) for k in ('id','category','target','operation','comparison_scope','evidence_refs','issue_ids') if k in f}
        row['issue_ids']=[safe_issue_id(i) for i in row.get('issue_ids',[])]
        row.update(root_location=location(f.get('root_location')),evidence_level=code(f.get('evidence_level'),'source_prediction'),
                   evidence_scope=scope_summary(f.get('scope',{})),
                   explanation=f['scope']['decision']['explanation'])
        out['findings'].append(row)
    out['inspection_records']=[{'id':safe_issue_id(r['id']),'version':r.get('version'),
        'compiled_property':property_summary(r.get('compiled_property')),
        'assessment_result':assessment_summary(r['assessment_result']),
        'evidence_refs':copy.deepcopy(r.get('evidence_refs',[]))} for r in report.get('inspection_records',[])]
    d=report['diagnostics']
    out['diagnostics']={'issues':[diagnostic(x) for x in d.get('issues',[])],
        'unexecuted_actions':len(d.get('unexecuted_actions',[])),
        'program_gaps':[diagnostic(x) for x in d.get('program_gaps',[])],
        'source_context_scope':context_summary(d.get('source_context_scope',{})),
        'no_finding_is_not_contract_safety':True,'E1_not_formal_FREEZE':True}
    task=report.get('task_analysis',{})
    out['task_analysis']={k:task[k] for k in ('model_analysis_available','empty_response_present','fixture_analysis_available','usable_task_opinion',
        'explicit_empty_task_reading','local_judgment_not_global_safety','unexecuted_actions') if k in task}
    out['task_analysis']['reading_scope']=coverage_summary(task.get('reading_scope',{}))
    usage=copy.deepcopy(report.get('usage',{}))
    for row in usage.get('attempts',[]):
        if 'normalization_diagnostics' in row:row['normalization_diagnostics']=[diagnostic(x) for x in row['normalization_diagnostics']]
        if 'reason' in row:row['reason']=code(row['reason'])
    out['decision_sha256']=digest([out['findings'],out['inspection_records'],out['task_analysis']['reading_scope'],out['unresolved_category_judgments']])
    out['usage']=usage
    p=report.get('provenance',{})
    out['provenance']={'structural_references':dict(p.get('structural_references',{})),'refinement_decisions':[dict(row,issue=safe_issue_id(row['issue']) if row.get('issue') else None) for row in p.get('refinement_decisions',[])],'shared_source_facts':{k:[safe_issue_id(i) for i in ids] for k,ids in p.get('shared_source_facts',{}).items()},'action_count':len(p.get('actions',[])),'revision_count':len(p.get('revisions',[])),
        'evidence_labels':copy.deepcopy(p.get('evidence_labels',[])),'cache_hits':p.get('cache_hits',0),
        'feedback_trace':[{k:row[k] for k in ('issue','selected','sent','parsed','consumed','simulated','submission_state','changed_finding','semantic_rows_received','semantic_rows_accepted','accepted_other_scopes','other_scope_accepted_rows','answered_unresolved') if k in row}
                          for row in p.get('feedback_trace',[])]}
    for row,trace in zip(out['provenance']['feedback_trace'],p.get('feedback_trace',[])):
        row['issue']=safe_issue_id(row['issue'])
        if trace.get('reason') in ('same_effect_authorization_already_decided',
                'existing_source_and_property_already_support_same_uncontested_claim',
                'same_property_source_or_complete_domain_refutation_already_closes_this_scope'):
            row['reason']=trace['reason']
    out['provenance']['computation_reuse']=copy.deepcopy(p.get('computation_reuse',{}))
    if 'solver_resource' in report:out['solver_resource']=copy.deepcopy(report['solver_resource'])
    return out

```

## source/src/pr_next_joint/investigation/dependencies.py

原文件SHA256 `671f9c840b7b9cb93bc3edf5f0d910dae6f1ca2bdafaf07e12b320a3fbca3d27`

```python
"""Read-only, target-specific def/use index over the frontend's resolved paths.

The index relates state definitions to expressions. An edge never establishes
a permission, an asset type, a committed financial effect or reachability.
"""
from collections import defaultdict, deque

from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key
from pr_next_joint.frontend.storage import keys, selectors, selector_relation
from pr_next_joint.frontend.path_ir import walk


def may_alias(a,b):
    shape=selector_relation(a,b)
    if shape=='disjoint':
        return False
    for left,right in zip(keys(a),keys(b)):
        if left.get('kind')==right.get('kind')=='literal' and left.get('value')!=right.get('value'):
            return False
    return True


def control_candidates(control,debits):
    """Candidate scope depends on the actual outgoing holder, including constant-index switches."""
    if not debits:return set()
    idx=keys(control)
    holders={key(x) for x in debits if x is not None}
    if any(key(k) in holders for k in idx):
        return {'FCR-FREEZE'}
    request_dependent=any(v.get('kind') in ('actual_sender','parameter','transaction_origin') for v in walk(control))
    if not request_dependent:
        return {'FCR-PAUSE'}
    return {'FCR-PAUSE','FCR-FREEZE'}


class Dependencies:
    def __init__(self,summaries):
        self.summaries=summaries
        self.readers=defaultdict(list)
        self.defs=defaultdict(list)
        self.rows={}
        self.forward_cache={}
        self.expressions={}
        self.amounts={}
        self.remaining=None
        for pid,row in summaries.paths.items():
            if not row['committing']:
                continue
            target,oid=row['target'],row['operation']
            for seq,write in enumerate(row['ordered_writes']):
                cell=write['path']
                self.defs[oid].append(cell)
                self.add(pid,target,oid,'value',write['value'],cell,seq,write.get('source'))
                from .summary import local_delta
                sign,amount=local_delta(write)
                if amount is not None:
                    self.add(pid,target,oid,'amount',amount,cell,seq,write.get('source'))
                self.add(pid,target,oid,'key',keys(cell),cell,seq,write.get('source'))
            for seq,guard in enumerate(row['guards']):
                self.add(pid,target,oid,'guard',guard,None,seq,None)
            if row['return_value']:
                self.add(pid,target,oid,'return',row['return_value'],None,0,None)
        self.identity=digest(sorted(self.rows))

    def add(self,pid,target,oid,kind,expr,cell,seq,source):
        # A constant expression defines a value but introduces no state edge.
        def read_values(term):
            if isinstance(term,dict):
                if term.get('kind')=='storage':
                    yield term
                    # Subscripts select the object. Keep them as address/key
                    # dependencies rather than pretending that they set its quantity.
                    if kind!='key':
                        self.add(pid,target,oid,'key',keys(term),cell,seq,source)
                    return
                for k,v in term.items():
                    if not k.startswith('_source_'):yield from read_values(v)
            elif isinstance(term,list):
                for v in term:yield from read_values(v)
        reads={key(v):v for v in read_values(expr)}
        if not reads:
            return
        expr_id=digest(expr)
        self.expressions.setdefault(expr_id,expr)
        for value in reads.values():
            edge={'path':pid,'target':target,'use':oid,'kind':kind,'read':value,'writes':cell,
                  'position':seq,'expression':expr_id,'source':source}
            token=digest(edge)
            if token not in self.rows:
                self.rows[token]=edge
                self.readers[(target,value['root'])].append(token)

    def forward(self,oid):
        if oid in self.forward_cache:
            return self.forward_cache[oid]
        source=self.summaries.operations[oid]
        target=source['target']
        initial={key(c):c for c in self.defs.get(oid,())}
        queue=deque(initial.values());queued=set(initial)
        seen=set();edges=set();via=defaultdict(set);residuals={}
        stopped=False
        while queue:
            if self.remaining is not None and self.remaining()<=0:
                stopped=True;break
            cell=queue.popleft()
            identifier=key(cell)
            if identifier in seen:continue
            seen.add(identifier)
            for edge_id in self.readers.get((target,cell['root']),()):
                edge=self.rows[edge_id]
                if not may_alias(cell,edge['read']):continue
                edges.add(edge_id)
                via[edge['use']].add(edge['kind'])
                if edge['writes'] is not None and edge['kind']!='key':
                    next_key=key(edge['writes'])
                    if next_key not in queued:
                        queue.append(edge['writes']);queued.add(next_key)
                # Only residuals on actual dependent operations are carried.
                row=self.summaries.paths[edge['path']]
                for residual in row['residuals']:
                    residuals[digest([edge['path'],residual])]=[edge['path'],residual]
        for residual in source['residuals']:
            residuals[digest([oid,residual])]=[oid,residual]
        answer={'origin':oid,'target':target,'edge_ids':sorted(edges),
                'uses':{use:sorted(kinds) for use,kinds in sorted(via.items()) if use!=oid},
                'visited_cells':len(seen),'residuals':list(residuals.values()),
                'precision':'may_over_resolved_paths','fixed_point_over_indexed_definitions':not stopped,
                'whole_source_closed':False}
        if stopped:
            answer['residuals'].append({'reason':'dependency_worklist_deadline','pending_cells':len(queue)})
        answer['id']=digest(answer)
        if not stopped:self.forward_cache[oid]=answer
        return answer

    def record(self):
        return {'id':self.identity,'edges':self.rows,'expressions':self.expressions,
                'closures':self.forward_cache,'amount_relations':self.amounts,
                'precision':'source_path_def_use_not_feasibility'}

    def quantity_bridges(self, change, use):
        """Bounded paths of amount dependencies; every intermediate writes a value read downstream."""
        limit=self.summaries.f.options.prefix_depth
        if limit < 2:
            return []
        outs=self.defs.get(change,())
        answers=[]
        mids=set()
        target=self.summaries.f.operations[change]['target']
        def overlap(cells, expr):
            return any(may_alias(w,s) for w in cells for s in selectors(expr))
        for cell in outs:
            for eid in self.readers.get((target,cell['root']),()):
                edge=self.rows[eid]
                if edge['use'] not in (change,use) and edge['kind'] in ('value','amount') and edge['writes'] is not None and may_alias(cell,edge['read']):
                    mids.add(edge['use'])
        use_edges=[edge for edge in self.rows.values() if edge['use']==use and edge['kind'] in ('value','amount')]
        for mid in sorted(mids):
            if self.remaining and self.remaining()<=0:break
            for row in self.summaries.rows(mid):
                written=[w['path'] for w in row['ordered_writes'] if overlap(outs,w['value'])]
                if written and any(overlap(written,self.expressions[edge['expression']]) for edge in use_edges):
                    answers.append((mid,row['path'],written))
                    if len(answers)>=self.summaries.f.options.max_prefixes:return answers
        return answers

    def amounts_for(self,oid):
        """Quantities of one actual reader, retaining their path, key, unit and order."""
        if oid in self.amounts:return self.amounts[oid]
        from .summary import local_delta,holder
        from .key_roles import relation
        f=self.summaries.f
        lookup=f.lookup(oid)
        records=[]
        for row in self.summaries.rows(oid):
            deltas=[];gates=[]
            for seq,w in enumerate(row['ordered_writes']):
                sign,amount=local_delta(w)
                if sign is None or amount is None:continue
                cell=w['path'];role=relation(cell,lookup) or {}
                hid=holder(cell,lookup)
                token=digest(amount)
                self.expressions.setdefault(token,amount)
                deltas.append({'write_index':seq,'cell':cell,'holder':hid,'sign':sign,
                    'amount_expression':token,'source':w['source'],'key_role':role.get('kind'),
                    'stage':'before_source_write','unit_family':cell['root']})
            for guard in row['guards']:
                for comparison in walk(guard):
                    operands=comparison.get('args',[])
                    if comparison.get('op') not in ('>=','<=','>','<','==') or len(operands)!=2:continue
                    for i,operand in enumerate(operands):
                        if operand.get('kind')!='storage':continue
                        role=relation(operand,lookup) or {}
                        if role.get('kind')!='authorization_quantity':continue
                        quantity=operands[1-i];token=digest(quantity)
                        self.expressions.setdefault(token,quantity)
                        gates.append({'grant':operand,'issuer_key':role['holder_key'],
                            'spender_key':1-role['holder_key'],'quantity_expression':token,
                            'operand_index':i,'operator':comparison['op'],'guard_expression':digest(guard)})
            records.append({'path':row['path'],'flow':row['flow'],'deltas':deltas,'allowance_gates':gates,
                'residuals':[x.get('reason') if isinstance(x,dict) else str(x) for x in row['residuals']]})
        self.amounts[oid]=records
        return records

```
