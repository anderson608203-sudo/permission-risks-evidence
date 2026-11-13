"""Narrow source certificates for local policy applicability, not safety claims."""
import copy
from .m03_p_paths import key,op,lit
from .m09_shared_policy import implies
from .m04_logic import Unsupported

def alternative(q,state,shared):
    basis=q.get('policy_basis',{});kind=basis.get('basis');tid=q['target'];fn=q['function'];pi=q.get('path_index')
    ps=state['paths'].get((tid,fn),[])
    if not isinstance(pi,int) or pi>=len(ps):return None
    path=ps[pi];lookup=state['lookups'][tid]
    if kind in ('same_resource_guarded_operation','source_checked_M2_relation'):
        # A self-only callback has a distinct source principal. This excludes
        # only a projected administrator rule, and does not prove its callers safe.
        own={'kind':'contract_address','instance':{'kind':'root_instance','contract':lookup.contract_node['id']}}
        required=op('==',{'kind':'actual_sender'},own)
        try:matched=implies(lookup,path,required)
        except (Unsupported,ValueError):matched=False
        if matched:
            return {'decision':'source_self_only_callback_not_direct_external_admin_bypass',
                    'source_certificate':{'function':fn,'path_index':pi,'self_guard':required,'effect_source':q.get('effect',{}).get('source')},
                    'scope':'direct caller identity only; external paths causing a self-call require their own analysis',
                    'original_policy':q.get('required_policy_candidate')}
    from .m18_market_scope import alternative as market_alternative
    return market_alternative(q,state,shared)
