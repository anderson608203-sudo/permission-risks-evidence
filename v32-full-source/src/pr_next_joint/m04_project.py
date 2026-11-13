"""Enumerate compiled project targets without guessing a business main contract.

Each concrete contract is analyzed in its own storage/caller context. This does
not infer deployment wiring or make unknown external calls trusted.
"""
import copy
from .core import digest,require
from .facts import walk
from .m03_p_route import analyze_program

def target_inventory(bundle):
    nodes={(file,n['name']):n for file,ast in bundle['ast_sources'].items() for n in walk(ast) if n.get('nodeType')=='ContractDefinition'}
    compiled={(c['file'],c['name']):c for c in bundle['contracts']}
    result=[]
    for identity,node in sorted(nodes.items()):
        item={'file':identity[0],'contract':identity[1],'contract_kind':node['contractKind'],'abstract':bool(node.get('abstract'))}
        item['selected']=node['contractKind']=='contract' and not node.get('abstract') and identity in compiled
        item['reason']='concrete_compiled_contract' if item['selected'] else 'interface_library_abstract_or_no_creation_artifact'
        result.append(item)
    return result

def analyze_project(bundle,native,description=None,selected_targets=None,path_facts=None,analysis_scope="joint"):
    inventory=target_inventory(bundle);reports=[];failures=[];rows=[];groups=[];uncovered=[]
    if selected_targets is not None:
        requested=set(selected_targets)
        available={x['file']+':'+x['contract'] for x in inventory if x['selected']}
        require(bool(requested) and requested<=available,'PROJECT_TARGET_SELECTION_INVALID')
        for item in inventory:
            if item['selected'] and item['file']+':'+item['contract'] not in requested:
                item.update(selected=False,reason='not_selected_by_explicit_scope')
    contracts={(c['file'],c['name']):c for c in bundle['contracts']}
    for target in [x for x in inventory if x['selected']]:
        identity={'file':target['file'],'contract':target['contract']};ref=identity['file']+':'+identity['contract']
        try:
            facts={} if path_facts is not None else None
            report=analyze_program(bundle,contracts[(target['file'],target['contract'])],native,[],description,path_facts=facts,analysis_scope=analysis_scope)
            if path_facts is not None:path_facts[ref]=facts
            reports.append({'target':identity,'report':report})
            for original in report['results']:
                row=copy.deepcopy(original);row['target_contract']=identity
                row['project_row_id']=digest({'target':identity,'source_row_id':row['id']});rows.append(row)
            for group in report['finding_groups']:groups.append({**copy.deepcopy(group),'target_contract':identity})
            uncovered.extend({**x,'target_contract':identity} for x in report['uncovered'])
            failures.extend({**x,'target_contract':identity} for x in report['failures'])
        except Exception as error:
            failures.append({'target_contract':identity,'reason':type(error).__name__+':'+str(error)})
    require(any(x['selected'] for x in inventory),'P_PROJECT_NO_CONCRETE_TARGETS')
    partial=bool(failures or uncovered or any(x['report']['status']!='analyzed' for x in reports))
    result={'schema':'m04-project-p-report-v1','route':'P','target_mode':'project','target_inventory':inventory,'contracts_analyzed':len(reports),
        'source_identity':{'program_id':bundle['program_id'],'build_id':bundle['build_id']},'results':rows,'finding_groups':groups,'reportable_findings':len(groups),
        'supported_effect_rows':sum(bool(x['reportable']) for x in rows),'uncovered':uncovered,'failures':failures,
        'functions_considered':[{'target':x['target'],'functions':x['report']['functions_considered']} for x in reports],
        'rule_capabilities':reports[0]['report']['rule_capabilities'] if reports else [],
        'status':'partial_analyzed' if partial else 'analyzed' if rows else 'no_analyzable_candidates',
        'counting_unit':'target-contract/operation/resource/policy groups, not independent vulnerabilities',
        'execution_status':'not_run','no_execution_required':True,'not_a_safety_conclusion':True,
        'scope':'all concrete contracts in supplied compiler project; separate target contexts; unresolved deployment wiring is not inferred',
        'target_reports':reports}
    return result
