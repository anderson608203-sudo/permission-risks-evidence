# 源码文本 · 7

## source/src/pr_next_joint/investigation/behavior.py

原文件 SHA-256 `45d048d4063a460f0511ede1e3d40785b7e6476e61a5254bfb1a23af333ada0d`

````python
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
        self.cache={};self.cache_hits=0;self.records=[];self.formulas={};self.solve_cache={}
        self.cache_stats={'source_hits':0,'behavior_hits':0,'formula_hits':0,'computations':0};self.deadline=None
    def remaining(self):return max(0.,self.deadline-time.monotonic()) if self.deadline is not None else self.f.options.seconds
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
        if not p.get('issues') or p.get('evaluation_gaps'):return p
        cache=self.__dict__.setdefault('_source_path_cache',{})
        if pid in cache:return cache[pid]
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
            not p.get('bounded_read_call_limits') and p['flow']!='truncated' and not any(
                c.get('binding')=='conditional_compiled_concrete_type' for c in p.get('read_calls',[]))
            for _,p in self.f.operation_paths(oid))
    def _query(self,e,formula,label,details=None,observed_terms=None):
        self.check()
        from .prestate import encode_state,prestate_receipt
        original_details=copy.deepcopy(details or {})
        e._initial_prefix_limit=1
        fixed,initial=encode_state(e,original_details)
        z=e.z
        def setup_solver(initial,fixed):
            details=dict(original_details,prestate=prestate_receipt(original_details,initial))
            solver=z.Solver();solver.add(formula,*fixed,*e.constraints,*e.domain_constraints)
            text=solver.sexpr();h=hashlib.sha256(text.encode()).hexdigest()
            context={'program':self.f.identity,'target':e.lookup.contract['file']+':'+e.lookup.contract['name'],
                'options':self.f.options.record(),'backend':'source-relational-revision-r1','abstract_hash':e.abstract_hash_used,
                'analysis_domain':details['prestate'].get('analysis_domain'),
                'initial_model_identity':details['prestate'].get('initial_model_identity'),
                'semantic_binding_identity':original_details.get('property_identity'),
                'semantic_version':original_details.get('semantic_version',0)}
            token=digest([h,context,{k:str(v) for k,v in (observed_terms or {}).items()}])
            self.formulas.setdefault(h,{'sha256':h,'text':text,'scope_context':context})
            return solver,details,h,context,token
        s,details,h,context,token=setup_solver(initial,fixed)
        if token in self.solve_cache:
            self.cache_stats['formula_hits']+=1
            q=copy.deepcopy(self.solve_cache[token]);q.update(label=label,details=details,computation_reused=True)
            q['id']='probe_'+digest([q['formula_ref'],context,label,q['details']])[:20]
            if not any(x['id']==q['id'] for x in self.records):self.records.append(q)
            return q
        def decide(s):
            self.check()
            return solve(s,initial_ms=min(self.f.options.solver_timeout_ms,max(1,int(self.remaining()*1000))))
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
            proof=z.Solver();proof.add(formula,*invariants,*e.constraints,*e.domain_constraints)
            result=solve(proof,initial_ms=min(self.f.options.solver_timeout_ms,max(1,int(self.remaining()*1000))))
            proof_text=proof.sexpr();ph=hashlib.sha256(proof_text.encode()).hexdigest()
            self.formulas.setdefault(ph,{'sha256':ph,'text':proof_text,'scope_context':dict(context,
                proof_method='persistent_source_invariants_overapproximation',sat_is_not_a_witness=True)})
            return {'answer':str(result),'formula_ref':ph,'persistent_source_facts':sources,
                'same_analysis_domain':context['analysis_domain'],'initial_model_identity':context['initial_model_identity'],
                'all_runtime_states_overapproximated':True,'excludes_only_this_formula':result==z.unsat,
                'positive_result_usable':False}
        answer=decide(s);initial_token=token;stages=[];certificate=None
        if answer==z.unsat and isinstance(initial,dict) and not initial.get('global_reachability_exhausted'):
            certificate=exclusion(context)
            if not certificate['excludes_only_this_formula'] and initial.get('more_prefixes_available') and original_details.get('initial_prefix_policy')!='constructor_only_for_explicit_prefix':
                stages.append({'formula_ref':h,'answer':'unsat','scope':'constructor state before runtime prefixes'})
                e._initial_prefix_limit=self.f.options.max_prefixes
                fixed,initial=encode_state(e,original_details)
                s,details,h,context,token=setup_solver(initial,fixed);answer=decide(s)
                if answer!=z.unsat:certificate=None
        credential={'status':'not_applicable'};hash_confirmation={'status':'not_required'};model=None
        if answer==z.sat:
            from pr_next_joint.verification.hash_confirmation import confirm
            hash_confirmation,concrete=confirm(e,s,min(self.f.options.solver_timeout_ms,max(1,int(self.remaining()*1000))))
            if concrete is not None:credential,model=e.credential_witness(concrete,min(self.f.options.solver_timeout_ms,max(1,int(self.remaining()*1000))))
        valid=(answer==z.sat and credential['status'] in ('not_required','verified') and
               hash_confirmation['status'] in ('not_required','verified'))
        q={'label':label,'answer':str(answer),'formula_ref':h,'formula_sha256':h,
           'credential':credential,'abstract_hash':e.abstract_hash_used,'hash_confirmation':hash_confirmation,'validated_bounded_witness':valid,
           'witness':{str(d):str(model[d]) for d in model.decls()} if model is not None else None,
           'scope':'original-source bounded symbolic prestate; not concrete EVM or deployment reachability',
           'details':details,'initial_stage_search':stages}
        q['id']='probe_'+digest([h,context,label,details])[:20]
        if certificate:q['exclusion_certificate']=certificate
        if observed_terms and valid and model is not None:
            q['observed_values']={name:str(model.eval(term,model_completion=True)) for name,term in observed_terms.items()}
        if valid and model is not None and isinstance(initial,dict) and initial.get('branches'):
            q['initial_state_witness']=[r for r in initial['branches'] if z.is_true(model.eval(e._initial_branch_conditions[r['selector']],model_completion=True))]
        if str(answer) in ('sat','unsat') and credential.get('status')!='unverified' and hash_confirmation.get('status') in ('not_required','verified'):
            self.solve_cache[token]=copy.deepcopy(q);self.solve_cache[initial_token]=copy.deepcopy(q)
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
                    payments=[z.If(e.expr(fx['recipient'])==h,e.expr(fx['amount']),z.IntVal(0)) for fx in fr['effects'] if fx['kind']=='native_transfer']
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
                    payments=[z.If(e.expr(fx['recipient'])==h,e.expr(fx['amount']),z.IntVal(0)) for fx in fr['effects'] if fx['kind']=='native_transfer']
                    if not payments:continue
                    paid=z.Sum(*payments)
                    q=self._query(e,z.And(success,debit>0,z.Not(paid==debit)),'same_holder_native_settlement_counterexample',{'operation':oid,'path':pid,'object':s});queries.append(q)
                    feasible=self._query(e,z.And(success,debit>0),'actual_debit_exists',{'operation':oid,'path':pid,'object':s});queries.append(feasible)
                    settlements.append({'path':pid,'object':s,'object_name':self._storage_name(oid,s),'holder':holder,
                        'unit_source':units,'same_holder_and_unit_full_settlement':q['answer']=='unsat' and feasible['validated_bounded_witness'],
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
            'credential_success_verified':any(q['validated_bounded_witness'] for q in committing),
            'verified_success_paths':[q['details']['path'] for q in committing if q['validated_bounded_witness'] and q['details'].get('operation')==oid],
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
        if any(f.operations[p]['target']!=f.operations[oid]['target'] for p in prefix):
            return {'kind':'reachability','operation':oid,'prefix':list(prefix),'queries':[],'worlds':[],
                    'reached':False,'local_errors':[{'reason':'prefix_cross_target_not_supported'}]}
        choices=[self.paths(x) for x in prefix]
        for selected in itertools.islice(itertools.product(*choices),f.options.max_prefixes):
            self.check()
            for pid,_ in self.paths(oid):
                self.check()
                try:
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
                        'per_frame_plan':plan,'target_property':goal,'initial_prefix_policy':'constructor_only_for_explicit_prefix'},observed)
                    queries.append(q);worlds.append({'prefix':[serialize_world(x,'PREFIX') for x in frames],'target':serialize_world(fr,'TARGET'),
                        'bindings':plan,'goal':goal,'query':q['id'],'committed':q['validated_bounded_witness'],
                        'prefix_frames':copy.deepcopy(frames),'target_frame':copy.deepcopy(fr)})
                except TimeoutError:raise
                except Exception as error:queries.append({'answer':'unsupported','reason':type(error).__name__+':'+str(error)})
        return {'kind':'reachability','operation':oid,'prefix':list(prefix),'queries':queries,'worlds':worlds,
                'reached':any(q.get('validated_bounded_witness') for q in queries),
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
                if not feasible['validated_bounded_witness']:
                    continue
                result=self._query(e,z.And(common,paid1-debit1<paid0-debit0),'holder_net_lower_after',details,
                    {'holder':h0,'controller':e.expr(cf['caller']),'debit_before':debit0,'debit_after':debit1,
                     'paid_before':paid0,'paid_after':paid1,'net_before':paid0-debit0,'net_after':paid1-debit1})
                queries.append(result)
                measurements.append({'scope':details,'feasible_probe':feasible['id'],'result_probe':result['id'],
                                     'answer':result['answer'],'validated':result['validated_bounded_witness']})

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
                            'validated':{q['label']:q['validated_bounded_witness'] for q in qs},
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
                              'same_request_bindings':eq and [str(x) for x in eq],'usable':q['validated_bounded_witness'],
                              'admin_only_route_not_assumed_holder_usable':True})
                        except TimeoutError:raise
                        except Exception as error:out.append({'operation':alt,'path':pid,'usable':False,'reason':str(error)})
        return out

````

