"""Auditable permission/equity relation view over existing graph/path/certificate objects.
This is provenance, not an additional risk classifier or proof of causal improvement.
"""
import copy
from .core import digest

def build(context,ledger,checks):
    nodes={};edges=[]
    def node(kind,payload):
        identity=kind+'_'+digest([context['identity'],payload])[:24]
        nodes.setdefault(identity,{'id':identity,'kind':kind,'data':copy.deepcopy(payload)})
        return identity
    operation_ids={o['id']:node('compiler_operation',{'target':o['target'],'function':o['function'],'source':o['source']}) for o in context['operations']}
    checks_by={q['id']:q for q in checks}
    for record in ledger:
        rid=record['relation_id'];proposal=node('LLM_relation_proposal',{'relation_id':rid})
        for field,rows in record['source_bindings'].items():
            for row in rows:
                bound=node('source_bound_'+field.rstrip('s'),row)
                edges.append({'from':proposal,'to':bound,'kind':'proposed_source_location'})
                edges.append({'from':bound,'to':operation_ids[row['op_ref']],'kind':'scoped_to_operation'})
        for link in record['operation_links']:
            if not link['status'].startswith('program_verified'):continue
            certificate=node('program_checked_relationship',link)
            edges.append({'from':proposal,'to':certificate,'kind':'located_or_corroborated'})
            for field in ('from_op_ref','to_op_ref'):
                edges.append({'from':certificate,'to':operation_ids[link[field]],'kind':field})
        for certificate_data in record.get('equity_certificates',[]):
            certificate=node('program_checked_equity_relationship',certificate_data)
            edges.append({'from':proposal,'to':certificate,'kind':'located_or_corroborated_equity'})
        for field in ('additional_check_ids','corroborated_program_check_ids','shared_authorization_check_ids'):
            for qid in record.get(field,[]):
                q=checks_by.get(qid)
                if q is None:raise ValueError('source_relation_view_unknown_check_identity')
                check=node('program_risk_check',{'query_id':qid,'target':q['target'],'function':q['function']})
                edges.append({'from':proposal,'to':check,'kind':field})
    return {'schema':'permission_equity_relation_view_v1','identity':copy.deepcopy(context['identity']),
        'nodes':list(nodes.values()),'edges':list({digest(e):e for e in edges}.values()),
        'source_navigation_graph_schema':'compiler operations, assignments, calls and writes; separate from certified relations',
        'graph_storage_format_not_claimed_as_innovation':True,'causal_accuracy_gain_requires_controls':True}
