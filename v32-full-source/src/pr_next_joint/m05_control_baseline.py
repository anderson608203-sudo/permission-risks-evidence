"""Ordinary holder baselines and complete finite same-entry continuations."""
import copy
from .m05_writer_scope import gaps_for
from .m03_p_paths import key,op,conditions_possible,walk
from .m03_p_route import keys,selectors,permission_atoms,value_type
from .m03_p_assets import negative
from .m03_p_asset_dimensions import ledger_projection
from .m04_logic import Unsupported
from .m05_state_relations import changes,compose_read
from .m05_equity_relations import linear_quantity
from .m05_mechanism_core import (MechanismEncoder,successful,checked_subtractions,
    execution_terms,reject_changed_selector_keys)

def asset_projection(selector,asset,lookup):
    if selector['root']!=asset['balance_root']:raise Unsupported('blocking_balance_root_mismatch')
    if key(selector.get('instance'))!=key(asset['balance_effect']['path'].get('instance')):
        raise Unsupported('blocking_balance_instance_mismatch')
    if asset.get('field_ledger_shape'):
        from .m13_financial_relations import component_shape
        if component_shape(selector,lookup)!=asset['field_ledger_shape']:raise Unsupported('blocking_field_shape_mismatch')
        return {'holder':copy.deepcopy(keys(selector)[0]),'asset_keys':[]}
    shape=asset.get('ledger_shape',{'holder_index':0,'asset_key_types':[]})
    p=ledger_projection(selector,lookup,shape['holder_index']==1)
    if not p or p['holder_index']!=shape['holder_index'] or p['asset_key_types']!=shape['asset_key_types']:
        raise Unsupported('blocking_ledger_dimensions_not_bound')
    return p

def transfer_summary(action,asset,lookup):
    updates=changes(action,lookup)
    from .m13_financial_relations import component_updates
    balances=component_updates(action,lookup,asset) if asset.get('field_ledger_shape') else [r for r in updates if r['write']['path']['root']==asset['balance_root']]
    if not balances:return None
    if any(r['delta'] is None for r in balances):raise Unsupported('blocking_balance_net_effect_unresolved')
    balances=[r for r in balances if r['delta']]
    if not balances:return None
    if all(all(c>0 for c in r['delta'].values()) for r in balances) or all(all(c<0 for c in r['delta'].values()) for r in balances):return None
    debits=[r for r in balances if all(c<0 for c in r['delta'].values())]
    if len(balances)!=2 or len(debits)!=1:raise Unsupported('blocking_transfer_pair_not_supported')
    debit=debits[0];credits=[r for r in balances if r['delta']==negative(debit['delta'])]
    if len(credits)!=1:
        from .m18_asset_witness import fee_witness
        fee=fee_witness(lookup,action,debit,balances,updates)
        if not fee or len(fee['credits'])!=1:raise Unsupported('blocking_transfer_not_conserved_or_source_fee_matched')
        credit=fee['credits'][0]
        left=asset_projection(debit['write']['path'],asset,lookup);right=asset_projection(credit['write']['path'],asset,lookup)
        if key(left['asset_keys'])!=key(right['asset_keys']):raise Unsupported('blocking_transfer_asset_dimension_mismatch')
        amount=negative(debit['delta'])
        return {'holder':left['holder'],'recipient':right['holder'],'asset_keys':left['asset_keys'],
            'amount':linear_quantity(amount),'amount_terms':amount,'debit':copy.deepcopy(debit['write']),
            'credit':copy.deepcopy(credit['write']),'source_fee_witness':fee}
    credit=credits[0];left=asset_projection(debit['write']['path'],asset,lookup);right=asset_projection(credit['write']['path'],asset,lookup)
    if key(left['asset_keys'])!=key(right['asset_keys']):raise Unsupported('blocking_transfer_asset_dimension_mismatch')
    for row in updates:
        sel=row['write']['path']
        if sel['root']!=asset['supply_root']:continue
        if key(sel.get('instance'))!=key(asset['supply_effect']['path'].get('instance')):raise Unsupported('blocking_supply_instance_mismatch')
        if row['delta'] is None or row['delta']:raise Unsupported('blocking_transfer_changes_supply')
    amount=negative(debit['delta'])
    return {'holder':left['holder'],'recipient':right['holder'],'asset_keys':left['asset_keys'],
        'amount':linear_quantity(amount),'amount_terms':amount,'debit':copy.deepcopy(debit['write']),'credit':copy.deepcopy(credit['write'])}

def transfer_route_predicates(paths,asset,lookup):
    """Branches choosing a fee calculation while preserving the same request.
    Their branch choice alone cannot establish removal of transfer service.
    """
    groups={}
    for path in paths:
        if not successful(path) or path['issues']:continue
        try:summary=transfer_summary(path,asset,lookup)
        except (Unsupported,ValueError):continue
        if not summary:continue
        identity=request_identity(summary)
        for choice in path.get('branch_choices',[]):
            k=key([choice['source'],choice['condition'],identity])
            g=groups.setdefault(k,{'condition':choice['condition'],'source':choice['source'],'signs':set()})
            g['signs'].add(choice['sign'])
    return [{'condition':g['condition'],'source':g['source'],'basis':'both_branches_preserve_source_transfer_request'} for g in groups.values() if g['signs']=={True,False}]


def request_identity(summary):
    return key({**{f:summary[f] for f in ('holder','recipient','asset_keys','amount')},
        'debit_root':summary['debit']['path']['root'],'debit_instance':summary['debit']['path'].get('instance'),
        'credit_root':summary['credit']['path']['root'],'credit_instance':summary['credit']['path'].get('instance')})

def entry_alternatives(function,actions,selected_index,summary,asset,lookup):
    result=[];excluded=[]
    for i,branch in enumerate(actions):
        if branch['flow']=='reverted':
            excluded.append({'path_index':i,'reason':'source_reverted'});continue
        if not successful(branch) or branch['issues']:raise Unsupported('same_entry_continuation_not_fully_modeled')
        evaluated=execution_terms(branch,lookup);other=transfer_summary(branch,asset,lookup)
        if other is None:
            excluded.append({'path_index':i,'reason':'no_net_transfer_of_declared_asset'});continue
        if request_identity(other)!=request_identity(summary):raise Unsupported('same_entry_alternative_effect_requires_model')
        result.append({'function':function,'path_index':i,'conditions':copy.deepcopy(branch['guards']+checked_subtractions(branch)),
            'execution_terms':evaluated,'write_selectors':[copy.deepcopy(w['path']) for w in branch['writes']],
            'transfer':other,'source':copy.deepcopy(branch.get('entry_source'))})
    if not any(r['path_index']==selected_index for r in result):raise Unsupported('selected_transfer_branch_not_in_alternatives')
    return {'branches':result,'excluded':excluded,'scope':'complete existing branches of same entry and exact request; other entries remain exceptions'}

def normal_baseline(action,summary,control,asset,lookup,paths):
    excluded={asset['balance_root'],asset['supply_root']};membership=[]
    for guard in action['guards']:
        for atom in permission_atoms(guard,lookup):
            sources=selectors(atom)
            if not sources or any(s['root'] in excluded for s in sources):continue
            if conditions_possible(action['guards'],atom):continue
            if atom.get('kind')=='storage' and key(atom)==key(control):
                evidence=deposit_membership(control,asset,lookup,paths)
                if evidence:membership.append(evidence);continue
                raise Unsupported('normal_holder_control_membership_requires_independent_basis')
            if any(n.get('kind')=='parameter' for s in sources for n in walk(keys(s))):
                raise Unsupported('normal_holder_management_relation_requires_model')
            if (atom.get('kind')=='op' and atom.get('op')=='==' and any(not s.get('segments')
                    and value_type(s,lookup) in ('address','address payable') for s in sources)):
                raise Unsupported('normal_holder_action_requires_independent_administrator')
            raise Unsupported('normal_holder_role_qualification_requires_model')
    holder=summary['holder'];own=op('==',{'kind':'actual_sender'},holder)
    if holder.get('kind')=='actual_sender' or not conditions_possible(action['guards'],own):
        return {'predicate':own,'kind':'holder_direct_transfer','consent_sources':membership}
    from .m05_asset_obligations import consent_model
    from .m05_consent_relations import credential_consent
    credential=credential_consent(action,holder,summary['amount'],lookup,recipient=summary['recipient'])
    try:
        predicate,certificates=consent_model(action,holder,summary['amount_terms'],lookup,paths,
            asset['balance_root'],asset['supply_root'],credential,summary['recipient'])
    except Unsupported as error:
        if str(error)!='holder_related_consent_guard_requires_model':raise
        # Restrict this witness to the holder calling in person. All original
        # path guards (including allowance/rate conditions) remain in M4.
        # This does not infer consent for a different delegated caller.
        return {'predicate':own,'kind':'holder_self_call_via_parameter',
            'consent_sources':membership,'delegated_consent_unresolved':str(error),
            'scope':'same source path; positive amount and actual caller=affected holder must be feasible'}
    if credential:predicate=op('and',predicate,credential['valid_issued_credential'])
    return {'predicate':predicate,'kind':'holder_or_source_authorized_delegate','consent_sources':copy.deepcopy(certificates)+membership}

def deposit_membership(control,asset,lookup,paths):
    """Positive membership is ordinary only with an independent funding route."""
    from .m05_bound_relations import family
    from .m05_mechanism_core import scalar_write
    from .m03_p_assets import polynomial
    from .m03_p_paths import lit
    if gaps_for(lookup,{control['root'],asset['balance_root']}):return None
    found=[]
    for fn,branches in paths.items():
        for path in branches:
            if not successful(path):continue
            for raw in path['writes']:
                if not family(raw['path'],control):continue
                write=scalar_write(raw,lookup)
                if write['value']==lit(False):continue
                kk=keys(write['path'])
                if path['issues'] or write['value']!=lit(True) or len(kk)!=1 or kk[0].get('kind')!='actual_sender':return None
                if lookup.function(fn).get('stateMutability')!='payable':return None
                deposits=[d for d in changes(path,lookup) if d['write']['path']['root']==asset['balance_root']
                    and keys(d['write']['path'])==kk and d['delta']==polynomial({'kind':'transaction_value','type':'uint256'})]
                if len(deposits)!=1:return None
                # A funding route requiring prior membership or an unrelated
                # authority does not independently establish ordinary access.
                if any(permission_atoms(g,lookup) for g in path['guards']):return None
                evaluated=execution_terms(path,lookup)
                found.append({'function':fn,'source':write['source'],'funding':deposits[0]['write'],
                    'conditions':copy.deepcopy(path['guards']),'execution_terms':evaluated})
    return {'kind':'holder_native_deposit_establishes_membership','selector':copy.deepcopy(control),'origins':found} if found else None

class BranchEncoder(MechanismEncoder):
    def __init__(self,lookup):
        self.type_domains=[]
        super().__init__(lookup)
    def bound(self,value,typ):
        start=len(self.constraints);result=super().bound(value,typ)
        self.type_domains.extend(self.constraints[start:]);return result

def finish(parent,child,clauses,label):
    parent.constraints.extend(child.type_domains)
    parent.abstract_hash_used|=child.abstract_hash_used
    parent.encoding_notes.append({'kind':'isolated_complete_source_path','label':label,
        'type_domain_count':len(child.type_domains),'local_constraint_count':len(child.constraints)})
    return child.z.And(*clauses,*child.constraints)

def branch_formula(parent,lookup,record,request,updates=(),baseline=None):
    child=BranchEncoder(lookup)
    reject_changed_selector_keys([record['conditions'],record['execution_terms'],record['write_selectors'],record['transfer']],updates)
    clauses=[child.expr(compose_read(op('and',*record['conditions']),updates,lookup))]
    if baseline is not None:clauses.append(child.expr(baseline))
    for value in record['execution_terms']:child.expr(compose_read(value,updates,lookup))
    for selector in record['write_selectors']:child.expr(selector)
    actual=record['transfer'];debit=actual['debit'];credit=actual['credit'];quantity=child.expr(request['amount'])
    clauses.extend([child.expr(compose_read(debit['path'],updates,lookup))-child.expr(compose_read(debit['value'],updates,lookup))==quantity,
        child.expr(compose_read(credit['value'],updates,lookup))-child.expr(compose_read(credit['path'],updates,lookup))==quantity,
        child.expr(compose_read(actual['holder'],updates,lookup))==child.expr(request['holder']),
        child.expr(compose_read(actual['recipient'],updates,lookup))==child.expr(request['recipient'])])
    if len(actual['asset_keys'])!=len(request['asset_keys']):raise Unsupported('blocking_alternative_asset_arity')
    clauses.extend(child.expr(compose_read(a,updates,lookup))==child.expr(b) for a,b in zip(actual['asset_keys'],request['asset_keys']))
    return finish(parent,child,clauses,{'function':record['function'],'path_index':record['path_index'],'post_transition':bool(updates)})

def redemption_witness(parent,lookup,asset,request):
    witness=asset.get('financial_scope_witness')
    if witness is None:
        if asset.get('ledger_shape',{}).get('holder_index',0)!=0:raise Unsupported('nested_asset_financial_scope_witness_missing')
        return parent.z.BoolVal(True)
    path=witness['path']
    if not successful(path) or path['issues']:raise Unsupported('nested_asset_redemption_path_incomplete')
    terms=execution_terms(path,lookup);namespace='redemption_witness:'+witness['id']+':'
    def instantiate(value):
        if isinstance(value,dict):
            if value.get('kind')=='actual_sender':return copy.deepcopy(request['holder'])
            if value.get('kind')=='parameter':return {**copy.deepcopy(value),'id':namespace+str(value['id'])}
            return {k:instantiate(v) for k,v in value.items()}
        return [instantiate(v) for v in value] if isinstance(value,list) else value
    child=BranchEncoder(lookup);clauses=[child.expr(g) for g in instantiate(path['guards'])]
    for value in instantiate(terms):child.expr(value)
    actual=instantiate(witness['asset_keys'])
    if len(actual)!=len(request['asset_keys']):raise Unsupported('nested_asset_redemption_dimension_arity')
    clauses.extend(child.expr(a)==child.expr(b) for a,b in zip(actual,request['asset_keys']))
    quantity=child.expr(request['amount']);balance=instantiate(witness['balance_write']);supply=instantiate(witness['supply_write']);payment=instantiate(witness['payment'])
    clauses.extend([child.expr(instantiate(witness['quantity']))==quantity,quantity>0,
        child.expr(balance['path'])-child.expr(balance['value'])==quantity,
        child.expr(supply['path'])-child.expr(supply['value'])==quantity,
        child.expr(payment['recipient'])==child.expr(request['holder']),
        child.expr(payment['amount'])==quantity,child.expr(payment['success'])])
    return finish(parent,child,clauses,{'kind':'same_asset_redemption_scope_witness','id':witness['id']})

def membership_witness(parent,lookup,baseline,holder):
    evidence=[c for c in baseline['consent_sources'] if c.get('kind')=='holder_native_deposit_establishes_membership']
    requirements=[]
    for ci,certificate in enumerate(evidence):
        alternatives=[]
        for oi,origin in enumerate(certificate['origins']):
            namespace='membership_origin:'+str(ci)+':'+str(oi)+':'
            def instantiate(value):
                if isinstance(value,dict):
                    if value.get('kind')=='actual_sender':return copy.deepcopy(holder)
                    if value.get('kind')=='parameter':return {**copy.deepcopy(value),'id':namespace+str(value['id'])}
                    if value.get('kind')=='transaction_value':return {**copy.deepcopy(value),'invocation':namespace}
                    return {k:instantiate(v) for k,v in value.items()}
                return [instantiate(v) for v in value] if isinstance(value,list) else value
            child=BranchEncoder(lookup)
            clauses=[child.expr(g) for g in instantiate(origin['conditions'])]
            for value in instantiate(origin['execution_terms']):child.expr(value)
            clauses.append(child.expr(instantiate({'kind':'transaction_value','type':'uint256'}))>0)
            alternatives.append(finish(parent,child,clauses,{'kind':'ordinary_membership_funding_origin','function':origin['function']}))
        requirements.append(parent.z.Or(*alternatives))
    return parent.z.And(*requirements)

def blocking_formula(parent,inputs,lookup):
    z=parent.z;alternatives=inputs['entry_alternatives'];request=inputs['transfer_request']
    selected=next(b for b in alternatives['branches'] if b['path_index']==inputs['action_path'])
    before=branch_formula(parent,lookup,selected,request,baseline=inputs['normal_baseline']['predicate'])
    membership=membership_witness(parent,lookup,inputs['normal_baseline'],request['holder'])
    financial=redemption_witness(parent,lookup,inputs['asset'],request)
    setters=[parent.expr(g) for g in inputs['transition_guards']]
    for value in inputs['transition_execution_terms']:parent.expr(value)
    after=z.Or(*[branch_formula(parent,lookup,b,request,inputs['writes']) for b in alternatives['branches']])
    reference=branch_formula(parent,lookup,selected,request,inputs['control_contribution']['retained_other_writes'])
    domain=z.And(before,financial,membership,parent.expr(inputs['amount'])>0,parent.expr(inputs['holder'])!=parent.expr(inputs['recipient']),
        parent.expr(inputs['transition_time'])<=parent.expr({'kind':'environment','field':'timestamp'}),*setters)
    return domain,z.And(z.BoolVal(inputs['required_scope_matches']),parent.expr(inputs['privilege']),reference,z.Not(after))
