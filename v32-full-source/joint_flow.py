"""Reusable joint preparation/frozen-consumption functions, without mock backends.

The caller owns runtime qualification, submission/claims and approval.  A frozen
manifest hash must come from its approved dispatch, never from an untrusted
reply. All filesystem paths are context-relative. This module does not dispatch,
read credentials, supply model answers or construct an execution backend.
"""
import json
import hashlib
import pathlib
import time

from .core import canonical, digest, ref, require
from .llm_limits import validate_default_policy
from .joint_context import load_frozen_inputs, build_messages
from .proposal_consumption import consume_proposal
from .proposal_application import apply_from_config
from .llm_evidence import validate_llm_evidence
from .validation_run import validate_component, report_component_results


def _path(ctx, value):
    ctx.validate()
    require(isinstance(value, str) and value, 'joint_relative_path_required')
    p = pathlib.Path(value)
    require(not p.is_absolute() and '..' not in p.parts, 'joint_relative_path_required')
    return ctx.path(value)


def _rel(ctx, path):
    return pathlib.Path(path).resolve().relative_to(ctx.root).as_posix()


def _json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def _file_ref(ctx, path):
    return {'path': _rel(ctx, path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def _verified(ctx, record):
    require(isinstance(record, dict) and set(record) == {'path', 'sha256'}, 'joint_file_ref_shape')
    path = _path(ctx, record['path'])
    require(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256'],
            'joint_file_identity:' + record['path'])
    return path


def _write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f:
        f.write(canonical(value))


def inference_options(max_tokens, inference=None):
    """Explicit request parameters; a candidate setting is never approval."""
    require(max_tokens is None or (type(max_tokens) is int and 1 <= max_tokens <= 4096), 'joint_inference_output_bound')
    if inference is None:
        inference = {'reasoning_effort': 'high', 'thinking': True}
    require(isinstance(inference, dict) and set(inference) == {'reasoning_effort', 'thinking'},
            'joint_inference_fields')
    require(inference['reasoning_effort'] in ('high', 'low', 'none') and type(inference['thinking']) is bool,
            'joint_inference_values')
    require(inference['thinking'] == (inference['reasoning_effort'] != 'none'), 'joint_inference_mode_mismatch')
    return {'max_tokens': max_tokens, **inference}


def verify_request_options(request, messages, options):
    expected = {'model': 'deepseek-flash', 'messages': messages, 'response_format': {'type': 'json_object'},
                'thinking': {'type': 'enabled' if options['thinking'] else 'disabled'},
                'reasoning_effort': options['reasoning_effort'], 'max_tokens': options['max_tokens'], 'stream': False}
    if options['max_tokens'] is None:
        del expected['max_tokens']
    require(request == expected, 'joint_request_inference_binding')


def prepare_joint(ctx, *, input_id, prepared_dir, output, client,
                  profile_path='configs/c2_component_profile.json', max_tokens=2048, inference=None, call_policy=None):
    """The provided Client performs its ordinary call/budget/receipt logic.

    An injected client must still be bound to this context. Tests replace only
    HTTP and credential boundaries outside this module; no reply argument exists.
    """
    ctx.validate()
    options = inference_options(max_tokens, inference)
    if call_policy is not None:
        validate_default_policy(call_policy)
        require(max_tokens is None and options['thinking'] is True and options['reasoning_effort'] == 'high',
                'joint_provider_default_mode')
    else:
        require(max_tokens is not None, 'joint_provider_default_policy_required')
    out = _path(ctx, output)
    require(not out.exists(), 'joint_output_exists')
    require(pathlib.Path(client.root).resolve() == ctx.root and
            pathlib.Path(client.batch).resolve() == ctx.batch, 'joint_client_context_mismatch')
    require(bool(client.simulated) == (ctx.mode == 'isolated'), 'joint_client_provenance_mode')
    inputs = load_frozen_inputs(ctx.root, input_id, prepared_dir, profile_path)
    context, messages, bound = build_messages(**inputs)
    profile = _json(_path(ctx, profile_path))
    spec = next(s for s in profile['inputs'] if s['id'] == input_id)
    frozen = {
        'profile': _file_ref(ctx, _path(ctx, profile_path)),
        'bundle': _file_ref(ctx, _path(ctx, spec['bundle']['local'])),
        'prepared': _file_ref(ctx, _path(ctx, prepared_dir + '/' + input_id + '.json')),
    }
    out.mkdir(parents=True, exist_ok=False)
    _write(out/'context.json', context)
    _write(out/'messages.json', messages)
    kwargs = dict(options)
    if call_policy is not None:
        kwargs['timeout'] = call_policy['timeout_seconds']
    content, receipt = client.call(messages, 'joint_' + input_id, **kwargs)
    _write(out/'call_receipt.json', receipt)
    if inference is not None:
        request_path = ctx.batch/'api'/receipt['request_id']/'request.json'
        verify_request_options(_json(request_path), messages, options)
    if content is None:
        result = {'status':'call_not_usable','receipt_status':receipt['status'],'input_id':input_id}
        _write(out/'preparation_status.json', result)
        return result
    # Freeze evidence snapshot so later budget events do not change a package.
    api = ctx.batch/'api'/receipt['request_id']
    evidence = {}
    for key, source in [('request_path',api/'request.json'), ('response_path',api/'final_content.json'),
                        ('receipt_path',api/'receipt.json'), ('ledger_path',client.ledger)]:
        require(source.resolve().is_relative_to(ctx.root), 'joint_client_evidence_outside_root')
        dest = out/'llm'/({'ledger_path':'ledger.jsonl'}.get(key,source.name))
        dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('xb') as f:
            f.write(source.read_bytes())
        evidence[key] = _rel(ctx,dest)
    binding = client.batch_binding()
    binding.update(program_id=inputs['bundle']['program_id'],build_id=inputs['bundle']['build_id'])
    _write(out/'proposal.json',content)
    consume = consume_proposal(content,source_kind='llm',batch_binding=binding,
                              output_dir=out/'consume',root=ctx.root,llm_evidence=evidence)
    _write(out/'consume_record.json',consume)
    if not consume['accepted']:
        result={'status':'proposal_rejected','input_id':input_id,'rejected':consume['rejected_fields']}
        _write(out/'preparation_status.json',result)
        return result
    application = apply_from_config(content,input_id=input_id,root=ctx.root,source_kind='llm',
                     output_dir=out/'apply',batch_binding=binding,prepared_dir=prepared_dir,
                     profile_path=profile_path,llm_evidence=evidence,consumption_ref=consume['consumption_ref'])
    if not application['applied']:
        result={'status':'application_rejected','input_id':input_id,'rejected':application['rejected_fields']}
        _write(out/'preparation_status.json',result)
        return result
    for record in frozen.values():
        _verified(ctx,record)  # Detect source mutation during the call.
    item = _json(out/'apply/derived_item.json')
    require(item['mode']=='concrete','joint_symbolic_not_in_scope')
    files = {**frozen,
        'proposal':_file_ref(ctx,out/'proposal.json'),
        'consume':_file_ref(ctx,out/'consume_record.json'),
        'application':_file_ref(ctx,out/'apply/application.json'),
        'derived':_file_ref(ctx,out/'apply/derived_item.json'),
        'messages':_file_ref(ctx,out/'messages.json'),
        **{key:_file_ref(ctx,_path(ctx,path)) for key,path in evidence.items()}}
    manifest = {'schema':'joint-frozen-input-v1','input_id':input_id,
        'program_id':inputs['bundle']['program_id'],'build_id':inputs['bundle']['build_id'],
        'prepared_dir':prepared_dir,'files':files,'batch_binding':binding,
        'selected_item_ref':application['selected_item_ref'],'derived_item_ref':ref(item),
        'plans':2,'transactions':2*len(item['plan']['transactions']),
        'simulated_llm':receipt['simulated'],'source_nature':receipt['source_nature'],
        'input_bound':bound,'r4_a6_credit':False}
    if inference is not None:
        manifest['schema'] = 'joint-frozen-input-v2'
        manifest['inference'] = options
    if call_policy is not None:
        manifest['schema'] = 'joint-frozen-input-v3'
        manifest['call_policy'] = call_policy
    _write(out/'frozen_manifest.json',manifest)
    result={'status':'prepared','input_id':input_id,'manifest_ref':_file_ref(ctx,out/'frozen_manifest.json'),
            'selected_item_ref':manifest['selected_item_ref'],'derived_item_ref':ref(item),
            'plans':manifest['plans'],'transactions':manifest['transactions']}
    _write(out/'preparation_status.json',result)
    return result


def verify_frozen_joint(ctx, manifest_ref, output):
    """Check identity and re-derive from evidence before any RPC/client claim.

    The receipt/ledger source flags remain authoritative. The original full
    plan is re-derived, not reconstructed from the compact model context.
    """
    ctx.validate()
    out = _path(ctx,output)
    require(not out.exists(),'joint_output_exists')
    manifest = _json(_verified(ctx,manifest_ref))
    require(manifest.get('schema') in ('joint-frozen-input-v1', 'joint-frozen-input-v2', 'joint-frozen-input-v3'),'joint_manifest_schema')
    required={'profile','bundle','prepared','proposal','consume','application','derived',
              'messages','request_path','response_path','receipt_path','ledger_path'}
    require(set(manifest.get('files',{}))==required,'joint_manifest_files')
    paths={k:_verified(ctx,v) for k,v in manifest['files'].items()}
    input_id = manifest['input_id']
    require(manifest['files']['prepared']['path'] == manifest['prepared_dir']+'/'+input_id+'.json',
            'joint_prepared_path_binding')
    inputs = load_frozen_inputs(ctx.root,input_id,manifest['prepared_dir'],manifest['files']['profile']['path'])
    require(all(manifest[k]==inputs['bundle'][k] for k in ('program_id','build_id')), 'joint_program_build_binding')
    require(_json(paths['bundle'])==inputs['bundle'],'joint_bundle_binding')
    proposal=_json(paths['proposal']); saved_consume=_json(paths['consume']); saved_app=_json(paths['application'])
    item=_json(paths['derived'])
    binding=manifest['batch_binding']
    require(binding.get('batch')==ctx.batch.relative_to(ctx.root).as_posix(),'joint_batch_binding')
    require(all(binding.get(k)==manifest[k] for k in ('program_id','build_id')),'joint_llm_identity_binding')
    evidence={k:manifest['files'][k]['path'] for k in ('request_path','response_path','receipt_path','ledger_path')}
    call=validate_llm_evidence(ctx.root,evidence,proposal,binding)
    require(call['simulated']==manifest['simulated_llm'] and call['source_nature']==manifest['source_nature'],
            'joint_manifest_provenance')
    require(ctx.mode=='isolated' or not call['simulated'],'joint_simulated_production_forbidden')
    # Historical manifests retain their exact context version. Never regenerate
    # old requests with today's output instructions and then bless new bytes.
    saved_messages = _json(paths['messages'])
    require(isinstance(saved_messages, list) and len(saved_messages) == 2 and
            saved_messages[1].get('role') == 'user', 'joint_saved_context_shape')
    try:
        saved_context = json.loads(saved_messages[1]['content'])
    except (KeyError, TypeError, ValueError):
        require(False, 'joint_saved_context_shape')
    require(isinstance(saved_context, dict), 'joint_saved_context_shape')
    context_version = saved_context.get('schema')
    require(context_version in ('neutral-joint-context-v1', 'neutral-joint-context-v2', 'neutral-joint-context-v3'), 'joint_saved_context_version')
    _,messages,bound=build_messages(**inputs, context_version=context_version)
    require(saved_messages==messages and _json(paths['request_path'])['messages']==messages,
            'joint_request_context_binding')
    if manifest['schema'] in ('joint-frozen-input-v2', 'joint-frozen-input-v3'):
        raw_options = manifest.get('inference')
        require(isinstance(raw_options, dict) and set(raw_options) == {'max_tokens', 'reasoning_effort', 'thinking'},
                'joint_manifest_inference_fields')
        options = inference_options(raw_options['max_tokens'], {k:raw_options[k] for k in ('reasoning_effort', 'thinking')})
        verify_request_options(_json(paths['request_path']), messages, options)
        if manifest['schema'] == 'joint-frozen-input-v3':
            policy = validate_default_policy(manifest.get('call_policy'))
            require(options == {'max_tokens':None, 'thinking':True, 'reasoning_effort':'high'}, 'joint_provider_default_mode')
            receipt = _json(paths['receipt_path'])
            require(receipt.get('request_max_tokens_omitted') is True and
                    receipt.get('timeout_seconds') == policy['timeout_seconds'] and
                    receipt.get('output_tokens_estimate') == policy['estimated_provider_output_tokens'] and
                    receipt.get('token_budget_policy') == policy['policy_id'], 'joint_provider_receipt_binding')
        else:
            require(options['max_tokens'] is not None, 'joint_provider_default_policy_required')
    require(bound==manifest['input_bound'],'joint_input_bound_binding')
    require(saved_consume.get('accepted') is True and saved_app.get('applied') is True,'joint_prior_application_not_accepted')
    require(ref(item)==manifest['derived_item_ref'] and ref(item)==saved_app['derived_item_ref'],
            'joint_derived_identity')
    require(item['input_id']==input_id and all(item[k]==manifest[k] for k in ('program_id','build_id')),
            'joint_derived_input_binding')
    require(manifest['plans']==2 and manifest['transactions']==2*len(item['plan']['transactions']) and item['mode']=='concrete',
            'joint_actual_count_mismatch')
    out.mkdir(parents=True,exist_ok=False)
    consume=consume_proposal(proposal,source_kind='llm',batch_binding=binding,
                            output_dir=out/'recheck_consume',root=ctx.root,llm_evidence=evidence)
    require(consume['accepted'],'joint_reconsumption_rejected')
    require(consume['normalized']==saved_consume['normalized'],'joint_consumption_mismatch')
    # Keep original consumption ref: it identifies the frozen original record.
    # Its diagnostic absolute paths may differ after transport; the evidence
    # snapshot is now independently checked at relative package paths above.
    app=apply_from_config(proposal,input_id=input_id,root=ctx.root,source_kind='llm',
                         output_dir=out/'recheck_apply',batch_binding=binding,
                         prepared_dir=manifest['prepared_dir'],profile_path=manifest['files']['profile']['path'],
                         llm_evidence=evidence,consumption_ref=saved_consume['consumption_ref'])
    require(app['applied'],'joint_reapplication_rejected')
    require(app['selected_item_ref']==manifest['selected_item_ref']==saved_app['selected_item_ref'],
            'joint_selected_item_binding')
    require(_json(out/'recheck_apply/derived_item.json')==item,'joint_derived_reconstruction_mismatch')
    _write(out/'verified_input.json',{'manifest_ref':manifest_ref,'derived_item_ref':ref(item),
        'plans':manifest['plans'],'transactions':manifest['transactions'],'simulated_llm':call['simulated']})
    return manifest,item,inputs['bundle']


def execute_joint(ctx, *, manifest_ref, output, rpc_factory, fingerprint, simulated_execution):
    """Execute verified derived input using a caller-supplied qualified backend.

    Integration must preflight ALL manifests before reserving/claiming a grouped
    run, and bind these manifest refs in dispatch. This one-item helper is not a
    replacement for the existing grouped submission control.
    """
    require(type(simulated_execution) is bool,'joint_execution_provenance_required')
    require(ctx.mode!='isolated' or simulated_execution,'joint_real_execution_in_isolated_forbidden')
    require(ctx.mode!='production' or not simulated_execution,'joint_simulated_production_forbidden')
    manifest,item,bundle=verify_frozen_joint(ctx,manifest_ref,output)
    out=_path(ctx,output)
    client=rpc_factory(item,out/'service')
    try:
        row=validate_component(client,item,bundle,out/'verification',fingerprint,deadline=time.monotonic()+180)
    finally:
        client.close()
    _write(out/'result.json',row)
    report_component_results([row],[],fingerprint,out/'report')
    envelope={'input_id':manifest['input_id'],'manifest_ref':manifest_ref,'derived_item_ref':ref(item),
              'outcome_kind':row['outcome_kind'],'verification_result_ref':row['verification_result_ref'],
              'simulated_llm':manifest['simulated_llm'],'simulated_execution':simulated_execution,
              'runtime_pass':False,'r4_a6_credit':False,'method_acceptance_claimed':False}
    _write(out/'run_provenance.json',envelope)
    return envelope
