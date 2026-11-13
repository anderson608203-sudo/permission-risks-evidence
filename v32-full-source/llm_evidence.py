"""Validate one real LLM request/response/receipt/ledger bundle.

The check is intentionally relational: four unrelated existing files cannot be
stitched into a successful call. No network or API call occurs here.
"""
import hashlib, json, pathlib
from .core import require, digest

REQUIRED = ['request_path', 'response_path', 'receipt_path', 'ledger_path']

def _path(root, value):
    p = pathlib.Path(value)
    return p if p.is_absolute() else pathlib.Path(root) / p

def validate_llm_evidence(root, evidence, proposal, batch_binding):
    require(isinstance(evidence, dict), 'llm_evidence_object_required')
    require(all(evidence.get(k) for k in REQUIRED), 'llm_evidence_four_files_required')
    paths = {k: _path(root, evidence[k]) for k in REQUIRED}
    for key, path in paths.items():
        require(path.is_file(), 'llm_evidence_missing:' + key)
    request = json.loads(paths['request_path'].read_text(encoding='utf-8'))
    response = json.loads(paths['response_path'].read_text(encoding='utf-8'))
    receipt = json.loads(paths['receipt_path'].read_text(encoding='utf-8'))
    require(receipt.get('status') == 'json_received', 'llm_receipt_not_successful')
    require(isinstance(receipt.get('simulated'), bool), 'llm_receipt_simulation_provenance_missing')
    require(receipt.get('source_nature') in ['real','simulated'], 'llm_receipt_source_nature_missing')
    require(receipt['source_nature'] != 'simulated' or receipt['simulated'] is True, 'llm_receipt_source_nature_mismatch')
    require(receipt.get('request_id') and receipt.get('request_sha256'), 'llm_receipt_identity')
    require(receipt.get('batch') == batch_binding.get('batch'), 'llm_receipt_batch_mismatch')
    require(receipt.get('request_sha256') == digest(request), 'llm_request_digest_mismatch')
    require(digest(response) == digest(proposal), 'llm_response_not_current_proposal')
    require(receipt.get('response_sha256') == digest(response), 'llm_receipt_response_digest_mismatch')
    rows = [json.loads(x) for x in paths['ledger_path'].read_text(encoding='utf-8').splitlines() if x.strip()]
    rid = receipt['request_id']
    reserved = [x for x in rows if x.get('event') == 'api_reserved' and x.get('request_id') == rid]
    returned = [x for x in rows if x.get('event') == 'api_returned' and x.get('request_id') == rid]
    require(len(reserved) == 1 and len(returned) == 1, 'llm_ledger_request_not_unique')
    require(all(x.get('batch') == receipt.get('batch') for x in reserved + returned), 'llm_ledger_batch_mismatch')
    require(all(x.get('simulated') is receipt['simulated'] and x.get('source_nature') == receipt['source_nature'] for x in reserved + returned), 'llm_ledger_simulation_provenance_mismatch')
    require(returned[0].get('status') == 'json_received', 'llm_ledger_return_not_successful')
    require(returned[0].get('response_sha256') == receipt['response_sha256'], 'llm_ledger_response_mismatch')
    require(returned[0].get('request_sha256') == receipt['request_sha256'], 'llm_ledger_returned_request_mismatch')
    require(reserved[0].get('request_sha256') == receipt['request_sha256'], 'llm_ledger_request_mismatch')
    if evidence.get('simulated') is True and receipt['simulated'] is False:
        raise ValueError('llm_evidence_cannot_upgrade_simulated_provenance')
    return {'request_path': str(paths['request_path']), 'response_path': str(paths['response_path']),
            'receipt_path': str(paths['receipt_path']), 'ledger_path': str(paths['ledger_path']),
            'request_id': rid, 'request_sha256': receipt['request_sha256'],
            'response_sha256': digest(response), 'status': receipt['status'],
            'ledger_event_ids': [rid], 'simulated': bool(receipt['simulated']), 'source_nature': receipt['source_nature']}
