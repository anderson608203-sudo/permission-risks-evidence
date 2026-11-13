"""M03 proposal conversion and observed coverage, without model/backend calls."""
import copy
import json
from .core import require, digest


def normalize_v2(proposal):
    require(isinstance(proposal, dict) and proposal.get('schema') == 'm03-permission-proposal-v2', 'M03_V2_SCHEMA')
    require(all(k in proposal for k in ('rule','function','subject','authorization','effect','basis','unresolved','covered')), 'M03_V2_FIELDS')
    require(all(isinstance(proposal[k], str) and proposal[k] for k in ('rule','function','subject')), 'M03_V2_REFERENCE_SHAPE')
    require(proposal['basis'] in ('program_fact','project_description','program_inferred'), 'M03_V2_BASIS')
    authorization=proposal['authorization'];effect=proposal['effect'];covered=proposal['covered']
    require(isinstance(authorization,dict), 'M03_V2_AUTHORIZATION_SHAPE')
    require(authorization.get('kind') in ('sender_equals_state','none','credential'), 'M03_V2_AUTHORIZATION_UNSUPPORTED')
    require(set(authorization)<= {'kind','state'}, 'M03_V2_AUTHORIZATION_EXTRA_CONDITIONS_UNSUPPORTED')
    auth_state = authorization.get('state')
    if authorization['kind'] == 'none': require(auth_state is None, 'M03_V2_AUTHORIZATION_NONE_STATE')
    elif authorization['kind'] == 'sender_equals_state': require(isinstance(auth_state,str) and auth_state, 'M03_V2_AUTHORIZATION_UNSUPPORTED')
    else: require(auth_state is None or isinstance(auth_state,str) and auth_state, 'M03_V2_CREDENTIAL_STATE')
    require(isinstance(effect,dict) and isinstance(effect.get('object'),str) and effect['object'], 'M03_V2_EFFECT_OBJECT')
    require(set(effect)<= {'object','field'}, 'M03_V2_EFFECT_EXTRA_SCOPE_UNSUPPORTED')
    field=effect.get('field')
    require(field is None or isinstance(field,str) and bool(field) or type(field) is int and field>=0, 'M03_V2_EFFECT_FIELD')
    require(isinstance(covered,dict) and all(isinstance(covered.get(k),list) and all(isinstance(v,str) for v in covered[k]) for k in ('functions','objects')), 'M03_V2_COVERED_SHAPE')
    unresolved=proposal['unresolved']
    if isinstance(unresolved,str):unresolved=[unresolved] if unresolved else []
    require(isinstance(unresolved,list), 'M03_V2_UNRESOLVED_LIST')
    normalized={'schema':'m03-permission-proposal-v1','rule':proposal['rule'],'function':proposal['function'],
        'subject':proposal['subject'],'effect_state':effect['object'],'effect_field':effect['object'] if field is None else field,
        'effect':copy.deepcopy(effect),'effect_scope':'whole_object' if field is None else 'field',
        'authority_state':auth_state,'authorization':copy.deepcopy(authorization),
        'authorization_semantics':'model_observation_requires_source_check','observed_guard':authorization['kind'],'proposal_basis':proposal['basis'],'unresolved':copy.deepcopy(unresolved),'covered':copy.deepcopy(covered),
        '_v2_original':copy.deepcopy(proposal)}
    # Identity constraints must survive conversion so the entry can check them.
    if 'source_sha256' in proposal:normalized['source_sha256']=proposal['source_sha256']
    if isinstance(proposal.get('guard'),str):normalized['guard']=proposal['guard']
    return normalized


def evidence_boundary(receipt, explicit_substitute, rpc_module, service_root):
    receipt=receipt or {}
    simulated=explicit_substitute or receipt.get('simulated') is True or receipt.get('source_nature') in ('fixture','simulated','substitute')
    origin='explicit_substitute' if simulated else 'real_response' if receipt.get('simulated') is False and receipt.get('source_nature')=='real' else 'unverified_client'
    backend='external_rpc_unverified' if rpc_module else 'registered_service' if service_root else 'not_configured'
    return {'schema':'m03-evidence-boundary-v1','proposal_origin':origin,'backend_origin':backend,
        'fixture_or_unverified':simulated or origin!='real_response' or backend!='registered_service',
        'eligible_for_research_evaluation':False,
        'evaluation_note':'development run; independent dataset evaluation is a separate procedure',
        'request_id':receipt.get('request_id'),'receipt_sha256':digest(receipt) if receipt else None,
        'receipt_path':'llm_receipt.json' if receipt else None,'raw_proposal_path':'raw_proposals.json',
        'meaning':'interface/diagnostic result only' if simulated or backend=='external_rpc_unverified' else 'read execution, replay and formula artifacts for actual result'}


def collect_coverage(native, contract_name, raw, normalized, conversions, directory, boundary):
    def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
    entries=sorted({f['signature'] for f in native['functions'] if f.get('contract')==contract_name and f.get('visibility') in ('public','external')})
    observations=[];reports={}
    for i, proposal in enumerate(normalized):
        folder=directory/('proposal_'+str(i))
        for report_path in sorted(folder.rglob('analysis_report.json')):
            if report_path.parent.name=='report':reports[report_path]=read(report_path)
        for path in sorted(folder.rglob('bound_item_*.json')):
            item=read(path); report_path=path.parent/'report/analysis_report.json'
            rows=reports.get(report_path,{}).get('coverage_and_failures',{}).get('query_results',[])
            matches=[r for r in rows if r.get('plan_ref',{}).get('id')==item['plan']['id']]
            row=matches[0] if len(matches)==1 else None
            target=item.get('source_relation',{}).get('frame',{}).get('entry',{}).get('function')
            claim=item.get('policy',{}).get('typed_relations',{})
            observations.append({'proposal_index':i,'function':target,'object':claim.get('effect_state'),
                'effect_scope':claim.get('object_effect',{}).get('effect'),'plan_id':item['plan']['id'],
                'execution_status':row.get('execution_status') if row else 'not_executed',
                'outcome':row.get('outcome_kind') if row else None,'policy_scope':item.get('policy_scope'),
                'evidence_boundary':boundary,'scope':item.get('scope'),
                'bound_item_path':str(path.relative_to(directory)),
                'report_path':str(report_path.relative_to(directory)) if report_path in reports else None})
    prepared=sorted({x['function'] for x in observations if x['function']})
    executed=sorted({x['function'] for x in observations if x['function'] and x['execution_status']=='completed'})
    coverage={'schema':'m03-observed-coverage-v1','model_claimed':[p.get('covered') for p in raw],
        'model_claims_are_execution_evidence':False,'input_public_entries':entries,'prepared_entries':prepared,
        'executed_entries':executed,'not_executed_entries':sorted(set(entries)-set(executed)),
        'actual_queries':observations,'conversion_results':conversions,'whole_program_coverage':'partial',
        'uncovered_scope':['other parameter choices and transaction sequences','rules and objects not represented in actual_queries'],
        'evidence_boundary':boundary}
    for path,report in reports.items():
        report['m03_evidence_boundary']=boundary
        report['m03_observed_coverage']=coverage
        report['m03_result_use']='fixture_or_unverified_diagnostic' if boundary['fixture_or_unverified'] else 'scoped_development_execution'
        path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return coverage
