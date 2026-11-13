"""Ordinary M03 intake and staged analysis; external services require permission.

Cached compiler facts are checked before M2. Errors retain the failing stage.
This entry does not grant API/runtime permission or expand supported semantics.
"""
import argparse
import importlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from pr_next_joint.m03_source import inspect_manifest, validate_loaded_artifacts
from pr_next_joint.m03_inference import build_context, propose, run_proposal, messages, messages_v2, normalize_v2
from pr_next_joint.m03_proposal_support import evidence_boundary, collect_coverage
from pr_next_joint.m03_result_rollup import completed_rows


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def load_obj(path):
    return json.loads(pathlib.Path(path).read_text(encoding='utf-8-sig'))


def rpc_from(spec):
    module, attr = spec.split(':', 1)
    return getattr(importlib.import_module(module), attr)()


class LazyRPC:
    """Do not start a service merely to report a proposal binding refusal."""
    def __init__(self, spec):
        self.spec = spec
        self.client = None

    def __getattr__(self, name):
        if self.client is None:
            self.client = rpc_from(self.spec)
        return getattr(self.client, name)


def main(argv=None):
    selected = sys.argv[1:] if argv is None else argv
    if '--route=joint' in selected or any(selected[i:i+2] == ['--route','joint'] for i in range(len(selected))):
        from pr_next_joint.m08_entry import main as joint_main
        return {'status':'joint_entry_returned','joint_exit':joint_main(selected)}
    p = argparse.ArgumentParser()
    p.add_argument('--manifest', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--root', default=str(ROOT))
    p.add_argument('--case')
    p.add_argument('--bundle')
    p.add_argument('--native')
    p.add_argument('--proposal', help='explicit local substitute; never real LLM evidence')
    p.add_argument('--llm-module', help='module:factory for a separately authorized client')
    p.add_argument('--m2-schema', choices=['v1','v2'], default='v1')
    p.add_argument('--route', choices=['E','P'], default='E')
    p.add_argument('--targets', choices=['entry','project'], default='entry', help='P route: analyze explicit entry or enumerate all concrete project contracts')
    p.add_argument('--p-policy')
    p.add_argument('--rpc-module', help='module:factory for a separately authorized backend')
    p.add_argument('--service-root', help='per-run service artifacts under the method workspace')
    p.add_argument('--worker-python')
    p.add_argument('--worker-script')
    a = p.parse_args(argv)
    root = pathlib.Path(a.root)
    out = pathlib.Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    log = []
    active_stage = 'inspect'
    material_origin = 'not_loaded'
    receipt = None
    boundary = None

    def stage(name, status, **detail):
        nonlocal active_stage
        active_stage = name
        log.append({'stage': name, 'status': status, **detail})
        save(out / 'stage_log.json', log)

    def finish(status, **detail):
        result = {'status': status, 'material_origin': material_origin, **detail, 'stage_log': str(out / 'stage_log.json'), 'evidence_boundary': boundary}
        save(out / 'entry_result.json', result)
        print(json.dumps(result, ensure_ascii=False))
        return result

    try:
        if a.targets=='project' and (a.route!='P' or a.proposal or a.llm_module):
            raise ValueError('P_PROJECT_MODE_USES_PROGRAM_RELATION_CANDIDATES; targeted proposals use entry mode')
        service_options = [a.service_root, a.worker_python, a.worker_script]
        if any(service_options) and not all(service_options):
            raise ValueError('M03_SERVICE_OPTIONS_INCOMPLETE')
        if a.rpc_module and any(service_options):
            raise ValueError('M03_CONFLICTING_BACKENDS')
        stage('inspect', 'started')
        result = inspect_manifest(root, a.manifest, target_mode=a.targets)
        save(out / 'inspection.json', result)
        stage('inspect', 'completed', cases=result['case_count'])
        if not a.case:
            stage('analysis', 'not_run_case_not_selected')
            return finish('inspection_only', cases=result['case_count'])
        case = next((c for c in result['cases'] if c['case_id'] == a.case), None)
        if case is None:
            raise ValueError('M03_CASE_NOT_FOUND')
        stage('compile_artifacts', 'started')
        if not a.bundle or not a.native:
            stage('compile_artifacts', 'required')
            return finish('compile_required', case=a.case)
        bundle, native = load_obj(a.bundle), load_obj(a.native)
        material_origin = bundle.get('material_origin', 'compiler_artifacts')
        binding = validate_loaded_artifacts(case, bundle, native)
        contracts = [c for c in bundle['contracts']
                     if (c['file'], c['name']) == (case['entry_source'], case['entry_contract'])]
        if a.targets=='entry' and len(contracts) != 1:
            raise ValueError('M03_ENTRY_CONTRACT_NOT_UNIQUE_IN_BUNDLE')
        contract = contracts[0] if a.targets=='entry' else None
        save(out / 'artifact_binding.json', binding)
        stage('compile_artifacts', 'loaded_and_source_matched', bundle=bundle['build_id'], material_origin=material_origin)
        stage('m1_context', 'started')
        if a.targets=='project':
            from pr_next_joint.m04_project import target_inventory
            inventory=target_inventory(bundle)
            selected={(x['file'],x['contract']) for x in inventory if x['selected']}
            context={'program_id':bundle['program_id'],'build_id':bundle['build_id'],'targets':inventory,
                'functions':[{**f,'target_contract':{'file':c['file'],'contract':c['name']}} for c in bundle['contracts'] if (c['file'],c['name']) in selected for f in c['functions']]}
        else:
            context = ({'program_id':bundle['program_id'], 'build_id':bundle['build_id'], 'functions':contract['functions']} if a.route == 'P' and not a.llm_module else build_context(bundle, contract, native))
        context['source_refs'] = binding['sources']
        save(out / 'm2_context.json', context)
        stage('m1_context', 'completed', functions=len(context['functions']))
        stage('m2_proposal', 'started')
        description = None
        if case.get('project_description'):
            description_path = (root / case['project_description']).resolve()
            if not description_path.is_relative_to(root.resolve()):
                raise ValueError('M03_PROJECT_DESCRIPTION_OUTSIDE_ROOT')
            description = description_path.read_text(encoding='utf-8-sig')
        if a.proposal and a.llm_module:
            raise ValueError('M03_CONFLICTING_PROPOSAL_SOURCES')
        if a.proposal:
            proposals = load_obj(a.proposal)
            stage('m2_proposal', 'explicit_local_substitute')
        elif a.llm_module:
            client = rpc_from(a.llm_module)
            save(out / 'm2_messages.json', messages_v2(context, description) if a.m2_schema == 'v2' else messages(context, description))
            content, receipt = propose(client, context, description, schema_version=a.m2_schema)
            # Persist before parsing so failed replies retain their actual receipt.
            save(out / 'llm_receipt.json', receipt)
            save(out / 'llm_returned_content.json', content)
            if content is None:
                raise ValueError('M03_LLM_RESPONSE_UNAVAILABLE:' + str(receipt.get('status')))
            proposals = json.loads(content) if isinstance(content, str) else content
            stage('m2_proposal', 'llm_client_response', receipt=receipt)
        elif a.route == 'P':
            proposals = []
            stage('m2_proposal', 'deterministic_program_relation_candidates')
        else:
            raise ValueError('M03_LLM_NOT_AUTHORIZED')
        if isinstance(proposals, dict):
            proposals = [proposals]
        if not isinstance(proposals, list) or (not proposals and a.route != 'P') or not all(isinstance(x, dict) for x in proposals):
            raise ValueError('M03_PROPOSALS_NOT_NONEMPTY_OBJECT_LIST')
        save(out / 'raw_proposals.json', proposals)
        raw_proposals = proposals
        normalized, conversions, conversion_failures = [], [], []
        for i, original in enumerate(raw_proposals):
            try:
                item = normalize_v2(original) if a.m2_schema == 'v2' and a.route != 'P' else original
                normalized.append(item)
                conversions.append({'proposal': i, 'status': 'normalized', 'schema': a.m2_schema})
            except Exception as error:
                normalized.append(None)
                failure = {'proposal': i, 'stage': 'm2_conversion', 'status': 'failed', 'error': type(error).__name__ + ':' + str(error)}
                conversions.append(failure); conversion_failures.append(failure)
        save(out / 'normalized_proposals.json', normalized)
        save(out / 'proposal_conversion.json', {'version': 'm03-v2-to-v1' if a.m2_schema == 'v2' else 'v1-preserved',
            'original': raw_proposals, 'normalized': normalized, 'results': conversions})
        proposals = normalized
        boundary = evidence_boundary(receipt, bool(a.proposal), a.rpc_module, a.service_root)
        save(out / 'evidence_boundary.json', boundary)
        if a.route != 'P' and not any(p is not None for p in proposals):
            save(out / 'coverage.json', collect_coverage(native, contract['name'], raw_proposals, normalized, conversions, out, boundary))
            return finish('no_completed_rows', rows=0, failures=conversion_failures)
        if a.route == 'P':
            from pr_next_joint.m03_p_route import analyze_program
            if a.p_policy:
                raise ValueError('P_LEGACY_NAME_ONLY_POLICY_NOT_ACCEPTED')
            boundary = {'route':'P','program_material_origin':material_origin,
                        'real_llm':bool(receipt and receipt.get('real_llm')),
                        'proposal_origin':'llm_client_response' if receipt else 'explicit_local_substitute' if a.proposal else 'program_relation_inference',
                        'backend':'not_required','execution_status':'not_run'}
            save(out / 'evidence_boundary.json', boundary)
            stage('m3_m4_p_analysis', 'started')
            if a.targets=='project':
                from pr_next_joint.m04_project import analyze_project
                report=analyze_project(bundle,native,description)
            else:
                report = analyze_program(bundle, contract, native, [x for x in proposals if x is not None], description)
            report['proposal_conversion_failures'] = conversion_failures
            report['evidence_boundary'] = boundary
            save(out / 'p_results.json', report['results'])
            save(out / 'p_report.json', report)
            save(out / 'coverage.json', {k:report[k] for k in ('functions_considered','uncovered','failures','rule_capabilities')})
            stage('m3_m4_p_analysis', report['status'], results=len(report['results']))
            return finish('P_'+report['status'], report='p_report.json', results=len(report['results']), findings=report['reportable_findings'])
        if not a.rpc_module and not a.service_root:
            stage('m4_validation', 'rpc_required')
            save(out / 'coverage.json', collect_coverage(native, contract['name'], raw_proposals, normalized, conversions, out, boundary))
            return finish('rpc_required', failures=conversion_failures)
        rpc = LazyRPC(a.rpc_module) if a.rpc_module else None
        service_factory = None
        if a.service_root:
            from pr_next_joint.m03_service import BoundClient
            def service_factory(item):
                return BoundClient(item, ROOT, a.service_root, a.worker_python, a.worker_script)
        stage('m4_configuration', 'started')
        fp = load_obj(ROOT / 'configs/backend_fingerprint.base.json')
        fp['id'] = 'm03-entry-local'
        fp['input_material_origin'] = material_origin
        fp['m03_evidence_boundary'] = boundary
        settings = {'block_number': 100, 'timestamp': 1000000,
                    'deployment_address_basis': {'sender': '0x00000000000000000000000000000000000000a1',
                    'nonce': 0, 'target': '0x31256cb3d8cb35671f13b5b1680b2cf4fe55fc4f'}}
        source = next(s for s in binding['sources'] if s['file'] == contract['file'])
        all_rows, all_unresolved, failed = [], [], list(conversion_failures)
        for i, original in enumerate(proposals):
            if original is None:
                continue
            stage('m2_binding', 'started', proposal=i)
            try:
                proposal = dict(original)
                if proposal.get('source_sha256') not in (None, source['sha256']):
                    raise ValueError('M03_PROPOSAL_SOURCE_IDENTITY_MISMATCH')
                # Bind outside model content; raw_proposals.json is never changed.
                proposal['source_sha256'] = source['sha256']
                save(out / ('bound_proposal_' + str(i) + '.json'), proposal)
                stage('m3_m4_report', 'started', proposal=i)
                res = run_proposal(proposal, bundle, contract, native, None, settings,
                                   rpc, fp, out / ('proposal_' + str(i)), service_factory=service_factory, project_description=description)
                stage('m3_m4_report', res['status'], proposal=i, rows=len(res.get('rows', [])),
                      unresolved=len(res.get('unresolved', [])))
                all_rows.extend(res.get('rows', []))
                all_unresolved.extend(res.get('unresolved', []))
                if res['status'] != 'completed':
                    failed.append({'proposal': i, 'status': res['status']})
            except Exception as error:
                failure = {'proposal': i, 'error': type(error).__name__ + ':' + str(error)}
                stage(active_stage, 'failed', **failure)
                failed.append(failure)
        save(out / 'coverage.json', collect_coverage(native, contract['name'], raw_proposals, normalized, conversions, out, boundary))
        count = completed_rows(all_rows)
        status = 'no_completed_rows' if not count else 'partial_completed' if failed or count != len(all_rows) else 'completed'
        return finish(status, rows=len(all_rows), unresolved=all_unresolved, failures=failed)
    except Exception as error:
        stage(active_stage, 'failed', error=type(error).__name__ + ':' + str(error))
        return finish('failed', failed_stage=active_stage, error=str(error))


if __name__ == '__main__':
    result = main()
    raise SystemExit(result.get('joint_exit',1 if result['status'] in ('failed', 'no_completed_rows', 'P_no_analyzable_candidates') else 0))

