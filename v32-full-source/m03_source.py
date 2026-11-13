"""M03 source intake: manifest validation, neutral compile inputs, and report adapter boundary.

This module never reads expectations, cases IDs for dispatch, or answer tables. It
accepts ordinary source projects and, once compiled artifacts exist, hands the
result to the existing static/M4/report stack.
"""
import hashlib, json, pathlib, re
from .core import require, digest

def _sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def _read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def inspect_case(root, case, require_entry=True):
    root = pathlib.Path(root)
    cid = case['case_id']
    require(re.fullmatch(r'[A-Za-z0-9_]+', cid), 'M03_CASE_ID')
    require(case.get('compiler_version') == '0.8.20', 'M03_COMPILER_VERSION')
    files = [root / p for p in case['source_files']]
    require(files and all(p.is_file() for p in files), 'M03_SOURCE_MISSING:' + cid)
    texts = {p.relative_to(root).as_posix(): p.read_text(encoding='utf-8') for p in files}
    require(any(re.search(r'pragma\s+solidity\s+\^?0\.8\.20', t) for t in texts.values()),
            'M03_PRAGMA_MISMATCH:' + cid)
    if require_entry or case.get('entry_source') or case.get('entry_contract'):
        require(bool(case.get('entry_source')) and bool(case.get('entry_contract')), 'M03_ENTRY_IDENTITY_INCOMPLETE:' + cid)
        entry = root / case['entry_source']
        require(entry in files and entry.is_file() and ('contract ' + case['entry_contract']) in entry.read_text(encoding='utf-8'),
                'M03_ENTRY_CONTRACT_MISSING:' + cid)
    # Multi-contract relationships are source facts, not one combined project.
    relations = []
    for rel, text in texts.items():
        for name in re.findall(r'new\s+([A-Za-z_][A-Za-z0-9_]*)', text):
            relations.append({'file': rel, 'creates': name})
    return {'schema': 'm03-source-case-v1', 'case_id': cid,
            'entry_contract': case.get('entry_contract'), 'entry_source': case.get('entry_source'),
            'compiler_version': case['compiler_version'],
            'sources': [{'path': p.relative_to(root).as_posix(), 'sha256': _sha(p),
                         'bytes': p.stat().st_size} for p in files],
            'constructor_relations': sorted(relations, key=lambda x: (x['file'], x['creates'])),
            'project_description': case.get('project_description'),
            'source_only': True, 'compiled': False, 'expectations_read': False}

def standard_input(root, case):
    root = pathlib.Path(root)
    sources = {p: {'content': (root / p).read_bytes().decode('utf-8')}
               for p in case['source_files']}
    return {'language': 'Solidity',
            'sources': sources,
            'settings': {'optimizer': {'enabled': True, 'runs': 200},
                         'evmVersion': 'paris',
                         'outputSelection': {'*': {'*': ['abi', 'evm.bytecode.object',
                                                       'evm.deployedBytecode.object', 'evm.bytecode.sourceMap',
                                                       'evm.deployedBytecode.sourceMap', 'metadata',
                                                       'evm.methodIdentifiers',
                                                       'evm.deployedBytecode.immutableReferences',
                                                       'evm.bytecode.linkReferences',
                                                       'evm.deployedBytecode.linkReferences',
                                                       'storageLayout'],
                                                   '': ['ast']}}}}

def inspect_manifest(root, manifest_path, target_mode='entry'):
    root = pathlib.Path(root); manifest = _read(root / manifest_path)
    require(manifest.get('format_version') == 1 and len(manifest.get('cases', [])) >= 1,
            'M03_CASE_SET_EMPTY')
    out = []
    for case in manifest['cases']:
        audit = inspect_case(root, case, require_entry=target_mode!='project')
        audit['standard_input'] = standard_input(root, case)
        audit['standard_input_sha256'] = digest(audit['standard_input'])
        out.append(audit)
    seen = [x['case_id'] for x in out]
    require(len(seen) == len(set(seen)), 'M03_CASE_DUPLICATE')
    return {'schema': 'm03-manifest-inspection-v1', 'cases': out,
            'case_count': len(out), 'source_file_count': sum(len(x['sources']) for x in out)}

def validate_loaded_artifacts(case, bundle, native, *, compiler_sources=None):
    """Bind cached facts to inspected compiler-input text before calling M2.

    Existing source anchors hash the entire compiler-input source, not a snippet.
    This cache check is not a compiler execution or runtime qualification.
    """
    for field in ('program_id', 'build_id'):
        require(bool(bundle.get(field)) and bundle[field] == native.get(field),
                'M03_NATIVE_' + field.upper() + '_MISMATCH')
    require(bundle.get('native_ir', {}).get('sha256') == digest(native),
            'M03_NATIVE_CONTENT_MISMATCH')
    sources = case['standard_input']['sources']
    require(set(bundle.get('ast_sources', {})) == set(sources),
            'M03_COMPILED_SOURCE_SET_MISMATCH')
    anchors = {}
    for record in bundle.get('functions', []) + bundle.get('state_declarations', []):
        anchor = record.get('source_anchor', {})
        if anchor.get('file') is not None:
            anchors.setdefault(anchor['file'], set()).add(anchor.get('sha256'))
    require(set(anchors) <= set(sources), 'M03_SOURCE_ANCHOR_OUTSIDE_INPUT')
    refs = []
    disk_hashes = {s['path']: s['sha256'] for s in case['sources']}
    for path, value in sources.items():
        # Windows read_text normalizes newlines for the compiler input; preserve
        # that identity separately from the original file-byte identity.
        source_hash = hashlib.sha256(value['content'].encode('utf-8')).hexdigest()
        proof=None
        if path in anchors:
            require(anchors[path] == {source_hash}, 'M03_COMPILED_SOURCE_MISMATCH:' + path)
        else:
            from .compiler_source_evidence import CompilerSourceEvidence
            valid=isinstance(compiler_sources,CompilerSourceEvidence) and compiler_sources.program_id==bundle['program_id'] and compiler_sources.build_id==bundle['build_id']
            proof=compiler_sources.get(path) if valid else None
            require(proof and proof.get('source_sha256')==source_hash, 'M03_COMPILED_SOURCE_IDENTITY_UNAVAILABLE:' + path)
        row={'file': path, 'sha256': source_hash,
                     'file_bytes_sha256': disk_hashes[path],
                     'hash_scope': 'compiler_input_source_utf8'}
        if proof:row['compiler_metadata_proof']=proof
        refs.append(row)
    return {'status': 'matched', 'program_id': bundle['program_id'],
            'build_id': bundle['build_id'], 'sources': refs,
            'compiled_here': False, 'runtime_pass': False}


def compile_standard(root, case, compiler, output):
    """Compile a raw manifest case or the exact input already inspected."""
    import subprocess
    root = pathlib.Path(root)
    out = pathlib.Path(output)
    out.mkdir(parents=True, exist_ok=True)
    if 'standard_input' in case:
        standard = case['standard_input']
        require(digest(standard) == case['standard_input_sha256'],
                'M03_STANDARD_INPUT_CHANGED')
        require(set(standard['sources']) == {s['path'] for s in case['sources']},
                'M03_STANDARD_SOURCE_SET_CHANGED')
        for source in case['sources']:
            data = (root / source['path']).read_bytes()
            require(hashlib.sha256(data).hexdigest() == source['sha256'],
                    'M03_SOURCE_CHANGED:' + source['path'])
            require(data.decode('utf-8') == standard['sources'][source['path']]['content'],
                    'M03_STANDARD_SOURCE_CHANGED:' + source['path'])
    else:
        standard = standard_input(root, case)
    payload = json.dumps(standard, ensure_ascii=False)
    (out / 'standard-input.json').write_text(payload, encoding='utf-8')

    def preserve_streams(stdout, stderr):
        for name, value in [('compiler.stdout', stdout), ('compiler.stderr', stderr)]:
            if isinstance(value, bytes):
                value = value.decode('utf-8', errors='replace')
            (out / name).write_text(value or '', encoding='utf-8')

    try:
        result = subprocess.run([str(compiler), '--standard-json'], input=payload,
                                capture_output=True, text=True, encoding='utf-8',
                                cwd=out, timeout=120)
    except subprocess.TimeoutExpired as error:
        preserve_streams(error.stdout, error.stderr)
        raise
    preserve_streams(result.stdout, result.stderr)
    # Keep compiler error diagnostics even when no deployable artifact exists.
    compiled = None
    try:
        compiled = json.loads(result.stdout)
    except (ValueError, TypeError):
        pass
    if compiled is not None:
        (out / 'standard-output.json').write_text(json.dumps(compiled), encoding='utf-8')
    require(result.returncode == 0, 'M03_COMPILER_EXIT')
    require(isinstance(compiled, dict), 'M03_COMPILER_OUTPUT_JSON')
    require(not [e for e in compiled.get('errors', []) if e.get('severity') == 'error'],
            'M03_COMPILE_ERROR')
    return standard, compiled


def instance_relations(compiled, contract_file, contract_name):
    """Actual AST new-expression relations, not a name-only source regex."""
    from .facts import walk
    ast = compiled['sources'][contract_file]['ast']
    result = []
    for node in walk(ast):
        if node.get('nodeType') == 'NewExpression':
            name = (node.get('typeName') or {}).get('name') or (node.get('typeDescriptions') or {}).get('typeString')
            result.append({'contract': contract_name, 'creates': name, 'src': node.get('src')})
    return result

def run_compiled_case(bundle, contract, native, policy, actors, settings, rpc, fingerprint, output):
    """Build static material from M1 and run M3/M4/report in the shared stack."""
    from .completion import prepare_static_candidates
    from .component_queries import prepare_queries
    from .validation_run import validate_component, report_component_results
    static = prepare_static_candidates(bundle, contract, native, actors, policy)
    prepared = prepare_queries(bundle, contract, static, policy, settings)
    if not prepared.get('prepared'):
        return {'status': 'no_prepared_queries', 'rows': [], 'leads': prepared.get('leads', [])}
    rows = []
    for item in prepared['prepared']:
        item.setdefault('input_id', contract['name'])
        rows.append(validate_component(rpc, item, bundle, pathlib.Path(output) / 'items' / item['id'], fingerprint))
    report_component_results(rows, prepared.get('leads', []), fingerprint, pathlib.Path(output) / 'report')
    return {'status': 'completed', 'rows': rows, 'leads': prepared.get('leads', []),
            'report': str(pathlib.Path(output) / 'report')}
