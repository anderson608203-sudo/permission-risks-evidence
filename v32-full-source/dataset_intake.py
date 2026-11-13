"""Read matched compiler facts using original compiler settings, never labels.

This is an input adapter, not a source-anchor/semantic binding replacement.
The existing strict anchor validator and all M2/M3/M4 checks remain in force.
"""
import copy,hashlib,json,re
from pathlib import Path
from .core import digest,require
from .m03_source import validate_loaded_artifacts
from .m04_project import target_inventory

FILES=('standard-input.json','standard-output.json','ProgramBundle.json','native_ssa.json','extract_receipt.json')

def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def confined(root,name):
    require(isinstance(name,str) and name,'DATASET_PATH_REQUIRED')
    p=(root/name).resolve();require(p.is_relative_to(root.resolve()),'DATASET_PATH_OUTSIDE_ROOT')
    require(p.is_file(),'DATASET_FILE_MISSING:'+name)
    return p

def load_compiled_unit(root,descriptor):
    root=Path(root).resolve();spec_path=confined(root,str(descriptor));spec=read(spec_path)
    require(spec.get('schema')=='dataset-compiled-unit-v1','DATASET_SCHEMA')
    require(set(spec)<={'schema','input_id','unit_id','artifacts','targets','description'},'DATASET_UNEXPECTED_FIELDS')
    for key in ('input_id','unit_id'):
        require(isinstance(spec.get(key),str) and re.fullmatch(r'[A-Za-z0-9_]+',spec[key]),'DATASET_ID')
    artifacts=spec.get('artifacts',{})
    require(set(artifacts)==set(FILES),'DATASET_ARTIFACT_SET')
    paths={}
    for name,item in artifacts.items():
        require(set(item)=={'path','sha256'},'DATASET_ARTIFACT_SHAPE')
        path=confined(root,item['path']);require(sha(path)==item['sha256'],'DATASET_ARTIFACT_CHANGED:'+name);paths[name]=path
    standard,compiled,bundle,native,receipt=[read(paths[n]) for n in FILES]
    retained = receipt.get('status') == 'extracted'
    require(receipt.get('status')=='compiled_and_extracted' or
            retained and receipt.get('compiler_invocations')==0 and receipt.get('native_extractions')==1,
            'DATASET_FACTS_NOT_READY')
    # An original retained-compiler extraction receipt records the actual old
    # extraction. No replacement success receipt or fresh compilation is claimed.
    for field, name in (('bundle_file_sha256','ProgramBundle.json'),('native_file_sha256','native_ssa.json')):
        if field in receipt: require(receipt[field]==sha(paths[name]),'DATASET_RETAINED_FILE_RECEIPT')
    require(receipt.get('standard_input_sha256')==sha(paths['standard-input.json']),'DATASET_INPUT_RECEIPT')
    if not retained or 'standard_input_digest' in receipt:
        require(receipt.get('standard_input_digest')==digest(standard),'DATASET_INPUT_DIGEST')
    require(receipt.get('standard_output_sha256')==sha(paths['standard-output.json']),'DATASET_OUTPUT_RECEIPT')
    require(standard.get('language')=='Solidity' and isinstance(standard.get('settings'),dict),'DATASET_LANGUAGE_SETTINGS')
    require(not any(e.get('severity')=='error' for e in compiled.get('errors',[])),'DATASET_COMPILER_ERRORS')
    texts=standard.get('sources',{})
    require(bool(texts) and all(isinstance(v.get('content'),str) for v in texts.values()),'DATASET_INLINE_SOURCE_REQUIRED')
    source_hashes={k:hashlib.sha256(v['content'].encode('utf-8')).hexdigest() for k,v in texts.items()}
    require(bundle.get('program_id')==digest(source_hashes),'DATASET_PROGRAM_ID')
    expected_build=digest({'input':standard,'compiler':receipt['compiler_binary_sha256']})
    require(bundle.get('build_id')==expected_build,'DATASET_BUILD_ID')
    require(all(receipt.get(k)==bundle.get(k)==native.get(k) for k in ('program_id','build_id')),'DATASET_FACT_IDENTITIES')
    require(receipt.get('native_sha256')==digest(native),'DATASET_NATIVE_RECEIPT')
    require(bundle.get('ast_sources')=={k:v.get('ast') for k,v in compiled.get('sources',{}).items()},'DATASET_AST_OUTPUT_MISMATCH')
    require(bundle.get('compiler',{}).get('compiler_version')==receipt.get('compiler_version'),'DATASET_COMPILER_VERSION')
    case={'standard_input':standard,'sources':[{'path':k,'sha256':v} for k,v in source_hashes.items()]}
    from .compiler_source_evidence import derive_source_evidence
    compiler_sources=derive_source_evidence(standard,compiled,bundle,sha(paths['standard-output.json']))
    binding=validate_loaded_artifacts(case,bundle,native,compiler_sources=compiler_sources)
    # Derive auxiliary evidence only after original artifact identity validation.
    # The original bundle on disk and its receipt remain unchanged.
    from .compiler_entry_evidence import derive
    derived_entries=derive(bundle,compiled,sha(paths['standard-output.json']))
    bundle=copy.deepcopy(bundle)
    from .m31_immutable import restore
    immutable_reconstruction=restore(bundle,standard,compiled)
    bundle.pop('_compiler_entry_evidence',None)
    if derived_entries:
        bundle['_compiler_entry_evidence']=derived_entries
    inventory=target_inventory(bundle)
    available={x['file']+':'+x['contract'] for x in inventory if x['selected']}
    selection=spec.get('targets','auto')
    require(selection=='auto' or isinstance(selection,list) and selection and all(isinstance(x,str) for x in selection),'DATASET_TARGET_SPEC')
    requested=None if selection=='auto' else selection
    require(requested is None or len(requested)==len(set(requested)) and set(requested)<=available,'DATASET_TARGET_NOT_AVAILABLE')
    require(bool(available),'DATASET_NO_CONCRETE_TARGET')
    for item in inventory:
        if requested is not None and item['selected'] and item['file']+':'+item['contract'] not in requested:
            item.update(selected=False,reason='not_selected_by_explicit_scope')
    description=None
    if spec.get('description'):
        item=spec['description'];require(set(item)=={'path','sha256'},'DATASET_DESCRIPTION_SPEC')
        path=confined(root,item['path']);require(sha(path)==item['sha256'],'DATASET_DESCRIPTION_CHANGED')
        description=path.read_text(encoding='utf-8-sig')
    record={'schema':'dataset-intake-receipt-v1','input_id':spec['input_id'],'unit_id':spec['unit_id'],
        'descriptor_sha256':sha(spec_path),'program_id':bundle['program_id'],'build_id':bundle['build_id'],
        'compiler_version':receipt['compiler_version'],'compiler_sha256':receipt['compiler_binary_sha256'],
        'settings':standard['settings'],'source_hashes':source_hashes,'targets_requested':selection,
        'targets_selected':sorted(available if requested is None else requested),'target_inventory':inventory,
        'facts_verified':True,'original_extraction_status':receipt['status'],'compiler_invocations':0,'labels_read':False,'method_execution':'not_run',
        'artifact_sha256':{n:sha(p) for n,p in paths.items()},
        'derived_entry_evidence_targets':sorted(derived_entries),
        'compiler_metadata_bound_sources':sorted(compiler_sources)}
    if immutable_reconstruction:
        record['immutable_reconstruction']=immutable_reconstruction
        record['compiler_invocations']+=immutable_reconstruction['invocations']
    return {'unit_id':spec['unit_id'],'bundle':bundle,'native':native,'binding':binding,
        'sources':[{'file':k,'sha256':source_hashes[k],'content':v['content']} for k,v in texts.items()],
        'description':description,'selected_targets':requested,'receipt':record}
