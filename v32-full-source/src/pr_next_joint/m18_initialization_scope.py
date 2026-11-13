"""Expose unresolved initial authority setup without inventing an owner rule."""
from .m03_p_paths import walk,key
from .m03_p_route import effective_permission
from .m11_policy import once_latch
from .m04_logic import Unsupported

def observations(state):
    result=[]
    for tid,lookup in state['lookups'].items():
        program={f:ps for (t,f),ps in state['paths'].items() if t==tid};providers={}
        from .source_entry_identity import builtin_call,builtin_object
        bases=set(lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']]))
        tree=[n for base in bases for n in walk(lookup.nodes.get(base,{}))]
        for n in tree:
            if n.get('nodeType')!='FunctionCall' or not builtin_call(n,lookup):continue
            for call in walk(n.get('arguments',[])):
                expr=call.get('expression',{});receiver=expr.get('expression',{});root=receiver.get('referencedDeclaration')
                if call.get('nodeType')!='FunctionCall' or expr.get('nodeType')!='MemberAccess' or not lookup.nodes.get(root,{}).get('stateVariable'):continue
                if not any(v.get('nodeType')=='MemberAccess' and v.get('memberName')=='sender' and builtin_object(v.get('expression',{}),lookup,'msg') for v in walk(call.get('arguments',[]))):continue
                providers.setdefault(root,[]).append(lookup.anchor(call))
        for fn,paths in program.items():
            for pi,path in enumerate(paths):
                if path['flow'] not in ('normal','returned'):continue
                for write in path['writes']:
                    root=write['path']['root']
                    if root not in providers or write['path'].get('segments') or write['value'].get('kind')!='parameter':continue
                    try:
                        if effective_permission(path['guards'],lookup):continue
                        latch=once_latch(path,program,lookup)
                    except (ValueError,Unsupported):latch=None
                    result.append({'target':tid,'function':fn,'path':pi,'phase':'authority_initialization_scope',
                        'reason':'source_authorization_provider_reconfiguration_needs_provider_and_deployment_evidence',
                        'provider_write':write['source'],'guard_consumers':providers[root],'one_time_latch':latch,
                        'missing':['provider authorization semantics','whether initialization is atomic with deployment'],
                        'not_a_confirmed_risk':True,'not_safe_evidence':True})
    return result
