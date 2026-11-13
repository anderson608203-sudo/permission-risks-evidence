"""Approved source lifecycle boundary, without a prerequisite asset-loss proof.
Requires an actual management boundary and a still-enabled stateful operation.
No public-selfdestruct heuristic, no modern-code-deletion claim.
"""
import copy
from .core import digest
from .m03_p_paths import op,lit,key,walk
from .m03_p_route import selectors,effective_permission,value_type,keys
from .m21_destruction import unresolved_authorization,PROFILE
from .m04_logic import Unsupported

def duties(context,state,shared,index):
    from .source_entry_identity import builtin_call
    from .m05_mechanism_core import remap
    rows=[];limits=[]
    for tid,lookup in state['lookups'].items():
        program={f:ps for (t,f),ps in state['paths'].items() if t==tid}
        managed=[]
        for fn,ps in program.items():
            for pi,p in enumerate(ps):
                if p['flow'] not in ('normal','returned') or p['issues'] or p.get('evaluation_gaps'):continue
                if not p['writes'] and not p.get('sensitive_effects'):continue
                if any(e.get('kind')=='native_selfdestruct' for e in p.get('sensitive_effects',[])):continue
                for perm in effective_permission(p['guards'],lookup):
                    ss=selectors(perm)
                    if not ss:continue
                    # A global set of managers can be indexed by caller, not
                    # only stored as one scalar address. Require independent
                    # governance of membership; personal flags are not roles.
                    from .m25_authority import managed_membership
                    membership=managed_membership(lookup,program,perm)
                    if not membership and any(keys(s) or value_type(s,lookup) not in ('address','address payable') for s in ss):continue
                    if any(n.get('kind')=='parameter' for n in walk(perm)):continue
                    managed.append((fn,pi,p,perm))
        for record in index.by_target[tid]:
            e=record['effect']
            if e.get('kind')!='native_selfdestruct':continue
            if not builtin_call(lookup.nodes.get(e['source']['ast_id'],{}),lookup,('selfdestruct','suicide')):continue
            p=program[record['function']][record['path_index']]
            if p['issues'] or p.get('evaluation_gaps'):continue
            from .m24_normal_boundaries import managed_termination_request
            requested=managed_termination_request(lookup,program,p)
            if requested:
                limits.append({'phase':'lifecycle_authorization','target':tid,'function':record['function'],'reason':'source_managed_public_completion','certificate':requested});continue
            for fn,pi,active,authority in managed:
                try:
                    # Separate the legitimate service caller from the caller
                    # attempting destruction, retaining shared source state.
                    caller={'kind':'parameter','id':-1900000000-abs(e['source']['ast_id']),'type':'address'}
                    mapping={n['id']:{**n,'id':-1800000000-abs(n['id'])} for n in walk(active) if n.get('kind')=='parameter'}
                    active_guards=remap(active['guards'],mapping,caller)
                    unknown=unresolved_authorization(p,lookup,{'root':None})
                    if unknown:
                        limits.append({'phase':'lifecycle_authorization','target':tid,'function':record['function'],'reason':'source_public_closure_or_unresolved_authorization','evidence':unknown});continue
                    required=op('or',authority,*effective_permission(p['guards'],lookup))
                    basis={'basis':'source_active_managed_lifecycle_destruction','execution_environment':PROFILE,
                        'source_managed_operation':fn,'source_managed_path_index':pi,'source_authority':authority,
                        'active_operation_conditions':active_guards,'source_effects':[w['source'] for w in active['writes']]+[x['source'] for x in active.get('sensitive_effects',[])],
                        'scope':'conditional termination of source-managed still-enabled code/state; no asset-loss prerequisite, no whole-contract availability claim',
                        'modern_evm_limit':'code/storage deletion generally requires creation in the same transaction after EIP-6780'}
                    q={'rule':'AC-01','target':tid,'function':record['function'],'path_index':record['path_index'],
                       'program_id':context['identity']['program_id'],'build_id':context['identity']['build_id'],
                       'conditions':copy.deepcopy(p['guards'])+active_guards+[op('!=',caller,lit(0))],
                       'issues':[],'effect':{**copy.deepcopy(e),'kind':'source_managed_lifecycle_destruction','execution_environment':PROFILE},'required_policy_candidate':required,'policy_basis':basis,
                       'source_evaluation_terms':copy.deepcopy(p.get('evaluated_terms',[]))+remap(active.get('evaluated_terms',[]),mapping,caller),
                       'sequence_extension_disabled':'lifecycle uses a separately bound still-active service caller'}
                    q['id']='q_'+digest(q);rows.append(q);index.use(record,'source_managed_lifecycle',q['id'])
                except (Unsupported,ValueError) as ex:limits.append({'phase':'lifecycle_model','target':tid,'function':record['function'],'reason':str(ex)})
    return rows,limits
