"""M4 checks bound queries; never copies a static/LLM predicted verdict.

SMT certifies only the declared source model and pre-state. Business-policy
inference, deployment reachability and cryptography are not proved by SAT.
"""
import copy,hashlib,json
from .m04_logic import Encoder,Unsupported
from .m03_p_paths import key,walk
from .m03_p_lifecycle import leaves

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
        from .m21_bytes import encode
        byte_value=encode(self,v)
        if byte_value is not None:return byte_value
        if v.get('kind')=='op' and v.get('op')=='ite':
            condition,yes,no=v['args']
            return super().expr({'kind':'conditional','condition':condition,'when_true':yes,'when_false':no})
        if v.get('kind') in ('typed_integer_arithmetic','integer_cast'):
            from .typed_integer import encode
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
        from .m04_joint_intrinsics import intrinsic
        special=intrinsic(self,v)
        if special is not None:return special
        if v.get('kind')=='member' and v.get('member')=='value' and v.get('base',{}).get('kind')=='symbol':
            declaration=v['base'].get('declaration')
            from .source_entry_identity import builtin_object
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

def substitute(value,mapping):
    if isinstance(value,dict):
        if value.get('kind')=='storage' and key(value) in mapping:return copy.deepcopy(mapping[key(value)])
        return {k:substitute(v,mapping) for k,v in value.items()}
    return [substitute(v,mapping) for v in value] if isinstance(value,list) else value

def effects_changed(e,effect,post=None):
    if effect.get('kind') in ('source_entitlement_contract_destruction','source_managed_lifecycle_destruction'):
        from .m21_destruction import PROFILE
        from .source_entry_identity import builtin_call
        node=e.lookup.nodes.get(effect.get('source',{}).get('ast_id'),{})
        if effect.get('execution_environment')!=PROFILE or not builtin_call(node,e.lookup,('selfdestruct','suicide')):
            raise Unsupported('D02_destruction_environment_or_source_unbound')
        e.encoding_notes.append('D02 legacy AC code/storage deletion; modern EIP-6780 restriction remains explicit')
        return e.z.BoolVal(True)
    if effect.get('kind') in ('native_transfer','native_selfdestruct'):
        amount=e.expr(effect['amount']);recipient=e.expr(effect['recipient'])
        conditions=[amount>0,recipient!=e.expr(e.lookup.read_calls.address())]
        if effect.get('success'):conditions.append(e.expr(effect['success']))
        return e.z.And(*conditions)
    if effect.get('kind')=='protected_delegate_entry':
        # Only reachability of the protected delegate invocation is claimed.
        return e.expr(effect['recipient'])!=e.expr({'kind':'literal','value':0})
    if effect.get('kind')=='dangerous_external_call':raise Unsupported('dangerous_external_effect_not_resolved')
    write={'path':effect['selector'],'value':effect['value'],'operator':effect['operator'],'source':effect['source']}
    changes=[]
    for w in leaves(write):
        before=substitute(effect.get('sequence_before_value',w['path']),post or {});after=substitute(w['value'],post or {})
        if after.get('kind')=='zero_of_storage_type':
            typ=e.typ(w['path'])
            if typ!='bool':e.width(typ) # Reject unresolved containers/structs.
            after={'kind':'literal','value':False if typ=='bool' else 0}
        changes.append(e.expr(before)!=e.expr(after))
    if not changes:raise Unsupported('no_observable_scalar_effect')
    return e.z.Or(*changes)

def sum_delta(e,delta):
    # Mathematical net change is signed; do not apply uint wrap/bounds to it.
    return e.z.Sum([int(coef)*e.expr(json.loads(term)) for term,coef in delta.items()]) if delta else e.z.IntVal(0)

def construct(e,row):
    z=e.z;basis=row.get('policy_basis',{});rule=row['rule']
    for evaluated in row.get('source_evaluation_terms',[]):e.expr(evaluated)
    if row.get('graph_frame_obligation'):
        from .m04_joint_graph_obligations import frame_formula
        return frame_formula(e,row)
    if rule=='FCR-MINT' and (basis.get('composed_creation') or basis.get('resolved_issuance_allowance')):
        if not basis.get('asset_model'):raise Unsupported('asset_entitlement_relation_missing')
        from .m04_joint_composition import composed_asset
        return composed_asset(e,row,effects_changed)
    guards=[e.expr(v) for v in row['conditions']]
    change=effects_changed(e,row['effect'])
    if basis.get('basis')=='source_caller_selected_code_execution_boundary':
        from .m18_code_control import formula
        return formula(e,row,guards,change)
    if rule in ('AC-01','AC-02','AC-03') or (rule=='AC-04' and basis.get('basis')=='holder_gross_debit_exceeds_applicable_spend_limit'):
        required=e.expr(row['required_policy_candidate'])
        if not z.is_bool(required):raise Unsupported('permission_predicate_is_not_boolean')
        return z.And(*guards),z.And(z.Not(required),change),{'kind':'permission_and_effect','checks':['original path','required permission violated','same resource actually changes']}
    if rule=='AC-04':
        if 'action_conditions_after_deactivation' in basis:
            model=basis.get('numeric_transition_model',{})
            domain=[e.expr(v) for v in model.get('conditions',[])]
            # The source-derived transition model already separates transition
            # caller from the eventual action caller; preserve that distinction.
            action=z.And(*[e.expr(v) for v in basis['action_conditions_after_deactivation']])
            effect=effects_changed(e,row['effect'],basis.get('post_deactivation_values',{}))
            return z.And(*domain),z.And(action,effect),{'kind':'bounded_lifecycle','checks':['source-bound activation/deactivation conditions','post-deactivation action conditions','post-transition resource effect'], 'assumption':'successful source-matched transition pair; deployment prefix not proved'}
        if basis.get('basis') in ('issued_future_expiry','issued_time_interval','issued_epoch_snapshot'):
            domain=z.And(*[e.expr(v) for v in basis.get('validity_assumptions',[])])
            return domain,z.And(*guards,z.Not(e.expr(row['required_policy_candidate'])),change),{'kind':'credential_validity','checks':['issued validity relation','invalid credential and action path compatible','resource changes']}
        if basis.get('basis')=='source_authorization_lifetime_control_mutation':
            return z.And(*guards),z.And(z.Not(e.expr(row['required_policy_candidate'])),change),{'kind':'source_control_transition','checks':['source-protected sensitive operation','previous condition false and changed condition true','control writer lacks applicable authorization']}
        if basis.get('basis')=='privileged_quota_assignment_guarded_positive_usage':
            return z.And(*guards),z.And(z.Not(e.expr(row['required_policy_candidate'])),change),{'kind':'consumable_quota','checks':['issued quota and positive usage','same subject quota decrement relation','usage effect changes'], 'assumption':'inferred consumable quota semantics; no all-history proof'}
        if basis.get('basis')=='credential_issued_in_controlled_phase':
            model=basis['model'];phase=e.expr(model['phase']);after=e.expr(model['transition']['to'])
            return phase==after,z.And(*guards,z.Not(e.expr(row['required_policy_candidate'])),change),{'kind':'phase_transition','checks':['source-bound controlled exit phase','credential action after exit','effect changes'], 'assumption':'successful authorized phase transition; reopening protocols outside scope'}
        raise Unsupported('lifecycle_formal_model_not_bound:'+str(basis.get('basis')))
    if rule!='FCR-MINT':raise Unsupported('rule_formal_model_not_implemented:'+rule)
    if not basis.get('asset_model'):raise Unsupported('asset_entitlement_relation_missing')
    if basis['asset_model'].get('kind')=='source_transferable_ledger':
        from .m03_p_assets import deltas,add
        actual={}
        for update in deltas({'writes':row['ledger_effects']}):actual=add(actual,update['delta'])
        if actual is None or actual!=basis['ledger_delta']:raise Unsupported('transferable_ledger_delta_not_source_matched')
        ledger=sum_delta(e,actual);privilege=basis.get('privilege_conditions',[])
        if not privilege and actual!={}:raise Unsupported('transferable_ledger_issuer_privilege_not_bound')
        for write in row['ledger_effects']:e.expr(write['value'])
        return z.And(*guards),z.And(ledger>0,change,*[e.expr(v) for v in privilege]),{
            'kind':'source_transferable_ledger_creation','checks':['source holder transfer relation','net ledger increase','original privileged path'],
            'supply_required':False,'assumption':'source ledger units, not market value or deployment proof'}
    if basis['asset_model'].get('kind')=='record_native_entitlement':
        from .m03_p_assets import deltas,polynomial
        # Recompute the liability delta rather than trusting a Boolean match.
        face=e.expr(basis['face']);supply_rows=row.get('supply_effects',[])
        if len(supply_rows)!=1:raise Unsupported('record_liability_effect_not_unique')
        actual=deltas({'writes':supply_rows})
        if (not basis.get('matched_liability') or len(actual)!=1 or actual[0]['delta']!=polynomial(basis['face'])
            or supply_rows[0]['path']['root']!=basis['asset_model']['supply_root']):
            raise Unsupported('record_face_liability_relation_not_matched')
        liability=e.expr(supply_rows[0]['value'])-e.expr(supply_rows[0]['path'])
        positive=z.And(face>0,liability==face,change)
        if basis.get('fresh_native_backing'):
            violation=z.And(positive,face>e.expr({'kind':'transaction_value','type':'uint256'}))
        elif basis.get('privilege_conditions'):
            violation=z.And(positive,*[e.expr(x) for x in basis['privilege_conditions']])
        else:raise Unsupported('record_issuer_privilege_not_bound')
        return z.And(*guards),violation,{'kind':'record_entitlement_accounting','checks':['source-bound holder/face/native payout relation','positive face','matching liability change','fresh backing or privileged issuance'],
            'assumption':'conditional source entitlement; later payout success, solvency and deployment not proved'}
    ledger=sum_delta(e,basis['ledger_delta']);supply=sum_delta(e,basis['supply_delta'])
    positive=z.And(ledger>0,supply>0,change)
    ordinary=basis.get('ordinary_route');privilege=basis.get('privilege_conditions',[])
    details={'kind':'asset_accounting','checks':['source-bound entitlement relation','net holder balance change','supply change','fresh backing/privilege distinction'],
             'asset_relation_digest':hashlib.sha256(key(basis['asset_model']).encode()).hexdigest(),
             'assumption':'source-derived redemption/entitlement relation; solvency and transaction reachability not proved'}
    if basis.get('native_value_equal_backing'):
        violation=z.And(positive,ledger>e.expr({'kind':'transaction_value','type':'uint256'}))
        details['claim']='creation exceeding source-matched fresh native backing'
    elif basis.get('proportional_backing'):
        pricing=basis['proportional_backing']
        violation=z.And(positive,ledger>e.expr(pricing['amount']))
        details['claim']='creation differing from source-matched proportional deposit price'
    elif basis.get('conserved_conversion'):
        conversion=basis['conserved_conversion']
        debit=conversion['source_debit'];supply_debit=conversion['source_supply_debit']
        debit_change=e.expr(debit['value'])-e.expr(debit['path'])
        supply_change=e.expr(supply_debit['value'])-e.expr(supply_debit['path'])
        violation=z.And(change,z.Or(ledger+debit_change>0,supply+supply_change>0))
        details['claim']='net creation across same-holder same-native-unit conversion'
    elif (ordinary and (not basis.get('positive_creation_condition') or not basis.get('supply_delta'))) or (basis.get('ledger_delta')=={} and basis.get('supply_delta')=={}):
        violation=positive;details['claim']='net new entitlement rather than reduction/conserved transfer'
    elif privilege:
        violation=z.And(positive,*[e.expr(x) for x in privilege]);details['claim']='privileged positive entitlement creation'
    else:
        # Upstream privilege needs a composed issuer->claim model, not a Boolean
        # "privileged" label supplied by the model or by the old heuristic.
        raise Unsupported('asset_upstream_control_or_backing_requires_composed_model')
    return z.And(*guards),violation,details

def check(lookup,row,timeout_ms=3000):
    from time import perf_counter
    started=perf_counter();upgrade_used=False;timing={'construct_and_solve':None,'solver_checks':0.0,'solver_check_calls_attempted':0}
    def timed_check(solver):
        nonlocal upgrade_used
        began=perf_counter();timing['solver_check_calls_attempted']+=1
        try:
            from .m20_solver import solve
            from .m20_solver import status
            before=status().get('upgrades',0)
            result=solve(solver,initial_ms=timeout_ms,upgrade=not upgrade_used)
            upgrade_used=upgrade_used or status().get('upgrades',0)>before
            return result
        finally:timing['solver_checks']+=perf_counter()-began
    base={'engine':'z3','query':'not_encoded','premise':'not_checked','status':'inconclusive','solver_called':False,
          'timing_seconds':timing,
          'scope':'bounded original-source model and declared pre-state; not whole-program or transaction proof','timeout_ms':timeout_ms}
    from .operation_scope import source_operation,exclusion
    proof=exclusion(row['rule'],source_operation(lookup,row['function']),
        {k:row.get(k,lookup.bundle.get(k)) for k in ('program_id','build_id')},row.get('target'),row['function'])
    if proof and proof.get('reason')=='no_checked_authorization_or_lifecycle_condition':
        from .m29_worklist import independent_entitlement
        if independent_entitlement(row,lookup):
            proof=None
    if proof and proof.get('reason')=='no_checked_authorization_or_lifecycle_condition' and row.get('policy_basis',{}).get('basis')=='source_authorization_lifetime_control_mutation':
        target=source_operation(lookup,row['policy_basis']['protected_operation'])
        current=source_operation(lookup,row['function'])
        from .m03_p_route import selectors
        basis=row['policy_basis']
        # M3 derived this guard from the actual inlined path. Bind its source
        # state to both operations rather than dropping a helper's return reads.
        roots={s['root'] for s in selectors(basis['source_control_condition'])}
        bound=roots.intersection(current.get('writes',[]),target.get('reads',[]))
        if bound and basis.get('complete_post_operation_guards') and target.get('guard_sources') and (target.get('native') or target.get('destroy') or target.get('writes')):
            proof=None # condition is in the affected operation, not its setter
    if proof:
        return {**base,'engine':'program_source','query':'not_required_P','premise':'source_checked',
                'status':'refuted_in_scope','reason':proof['reason'],'program_analysis_certificate':proof}
    if row.get('issues'):
        return {**base,'reason':'source_path_has_unresolved_semantics','issues':row['issues']}
    try:
        e=JointEncoder(lookup);z=e.z;domain,violation,details=construct(e,row)
        solver=z.Solver();solver.set(timeout=timeout_ms);solver.add(*e.constraints,domain)
        base['solver_called']=True
        premise=timed_check(solver);base.update(solver_called=True,premise=str(premise),version=z.get_version_string(),formal_obligation=details,
                                          encoding_notes=e.encoding_notes)
        if premise!=z.sat:
            return {**base,'reason':'premise_unsat' if premise==z.unsat else solver.reason_unknown(),'smt2':solver.to_smt2()}
        solver.add(violation);answer=timed_check(solver);smt=solver.to_smt2()
        base.update(query=str(answer),smt2=smt,formula_sha256=hashlib.sha256(smt.encode()).hexdigest())
        if answer==z.unknown:return {**base,'reason':solver.reason_unknown()}
        if answer==z.unsat and row.get('effect',{}).get('kind')=='native_selfdestruct':
            # Payout semantics alone cannot refute a self/zero-balance destruction:
            # storage/code effects depend on the EVM revision and creation history.
            effect=row['effect'];boundary=z.Solver();boundary.set(timeout=timeout_ms)
            possible_revision_effect=z.Or(e.expr(effect['recipient'])==e.expr(e.lookup.read_calls.address()),e.expr(effect['amount'])==0)
            boundary.add(*e.constraints,domain,z.Not(e.expr(row['required_policy_candidate'])),possible_revision_effect)
            revision_answer=timed_check(boundary)
            if revision_answer!=z.unsat:
                return {**base,'status':'inconclusive','reason':'selfdestruct_non_payout_effect_requires_EVM_revision_and_creation_scope',
                        'boundary_query':str(revision_answer),'boundary_smt2':boundary.to_smt2()}
        if answer==z.sat and e.abstract_hash_used:
            return {**base,'status':'inconclusive','reason':'hash_abstraction_sat_requires_concrete_confirmation',
                    'witness':{str(d):str(solver.model()[d]) for d in solver.model().decls()},'abstract_witness_only':True}
        return {**base,'status':'supported' if answer==z.sat else 'refuted_in_scope',
                'reason':'formal_violation_satisfiable' if answer==z.sat else 'formal_violation_unsatisfiable_in_scope',
                'witness':{str(d):str(solver.model()[d]) for d in solver.model().decls()} if answer==z.sat else None}
    except (Unsupported,ValueError) as error:
        return {**base,'reason':str(error)}
    except Exception as error:
        return {**base,'reason':'formal_encoding_error:'+type(error).__name__+':'+str(error),'implementation_error':True}
    finally:
        timing['construct_and_solve']=perf_counter()-started
