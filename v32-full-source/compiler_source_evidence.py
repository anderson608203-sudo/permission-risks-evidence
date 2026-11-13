"""Bind anchorless source units to original compiler metadata, never to guesses."""
import hashlib,json
from .core import require

class CompilerSourceEvidence(dict):
    """In-process provenance; JSON input cannot supply this evidence type."""
    def __init__(self,program_id,build_id):
        super().__init__();self.program_id=program_id;self.build_id=build_id

def derive_source_evidence(standard,compiled,bundle,output_sha256):
    evidence=CompilerSourceEvidence(bundle['program_id'],bundle['build_id'])
    anchored={r.get('source_anchor',{}).get('file') for r in bundle.get('functions',[])+bundle.get('state_declarations',[])}
    needed=set(standard['sources'])-anchored
    if not needed:return evidence
    claims={path:[] for path in needed};version=bundle['compiler']['compiler_version']
    for file,contracts in compiled.get('contracts',{}).items():
        for name,output in contracts.items():
            raw=output.get('metadata')
            if not raw:continue
            try:metadata=json.loads(raw)
            except (TypeError,ValueError):continue
            relevant=needed.intersection(metadata.get('sources',{}))
            if not relevant:continue
            require(metadata.get('language')=='Solidity','DATASET_METADATA_LANGUAGE')
            require(metadata.get('settings',{}).get('compilationTarget')=={file:name},'DATASET_METADATA_TARGET')
            require(metadata.get('compiler',{}).get('version','').split('+')[0]==version,'DATASET_METADATA_COMPILER')
            for path in relevant:
                claim=metadata['sources'][path].get('keccak256')
                require(isinstance(claim,str) and len(claim)==66 and claim.startswith('0x'),'DATASET_METADATA_SOURCE_HASH')
                claims[path].append({'target':file+':'+name,'keccak256':claim.lower(),'metadata_sha256':hashlib.sha256(raw.encode('utf8')).hexdigest()})
    # Keccak-256 is Ethereum's original hash, not hashlib.sha3_256.
    from Crypto.Hash import keccak
    for path,records in claims.items():
        if not records:continue
        data=standard['sources'][path]['content'].encode('utf8');h=keccak.new(digest_bits=256);h.update(data)
        expected='0x'+h.hexdigest()
        require({r['keccak256'] for r in records}=={expected},'DATASET_METADATA_SOURCE_MISMATCH:'+path)
        evidence[path]={'source_sha256':hashlib.sha256(data).hexdigest(),'source_keccak256':expected,
            'standard_output_sha256':output_sha256,'compiler_version':version,'metadata_sources':records}
    return evidence
