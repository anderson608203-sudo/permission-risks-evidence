"""Narrow, source-mapped legacy dispatcher evidence; no EVM execution or guesses.

Accept only the complete known linear 0.4 dispatcher grammar. Unsupported layouts
yield no evidence. Original compiler artifacts are never changed.
"""
import hashlib

class CompilerEntryEvidence(dict):
    """In-process provenance marker: cannot be supplied by a JSON artifact."""

def legacy_dispatch(runtime, source_map, selectors):
    try:
        code=bytes.fromhex(runtime.removeprefix('0x'))
        if not source_map:return {}
        maps=[];previous=[-1,-1,-1]
        for item in source_map.split(';'):
            fields=item.split(':')
            for j in range(min(3,len(fields))):
                if fields[j]!='':previous[j]=int(fields[j])
            maps.append(tuple(previous))
        ins=[];pc=0
        while pc<len(code) and len(ins)<len(maps):
            op=code[pc];n=op-95 if 96<=op<=127 else 0
            if pc+1+n>len(code):return {}
            ins.append((pc,op,int.from_bytes(code[pc+1:pc+1+n],'big') if n else None,maps[len(ins)]))
            pc+=n+1
        i=0
        def take(op,value=None):
            nonlocal i
            if i>=len(ins) or ins[i][1]!=op or value is not None and ins[i][2]!=value:raise ValueError('grammar')
            result=ins[i];i+=1;return result
        def push():
            nonlocal i
            if i>=len(ins) or not 96<=ins[i][1]<=127:raise ValueError('push')
            result=ins[i];i+=1;return result
        memory=take(0x60)
        if memory[2] not in (0x60,0x80):return {}
        take(0x60,0x40);take(0x52)
        # Two known 0.4 compiler guards: calldata shorter than a selector,
        # or empty calldata. Match the complete grammar, not a loose scan.
        if i<len(ins) and ins[i][1]==0x36:
            take(0x36);take(0x15)
        else:
            take(0x60,4);take(0x36);take(0x10)
        fallback=push()[2];take(0x57)
        take(0x60,0);take(0x35);take(0x7c,1<<224);take(0x90);take(0x04);take(0x63,0xffffffff);take(0x16)
        branches={}
        while i<len(ins) and ins[i][1]==0x80:
            branch_pc=take(0x80)[0];selector=take(0x63)[2].to_bytes(4,'big').hex();take(0x14)
            target=push()[2];take(0x57)
            if selector in branches:return {}
            branches[selector]={'dispatch_pc':branch_pc,'target_pc':target}
        end=take(0x5b)
        if fallback!=end[0] or set(branches)!=set(selectors):return {}
        bypc={row[0]:row for row in ins}
        result={}
        for selector,branch in branches.items():
            destination=bypc.get(branch['target_pc'])
            if not destination or destination[1]!=0x5b:return {}
            start,length,file_id=destination[3]
            if start<0 or length<=0 or file_id<0:return {}
            result[selector]={**branch,'source_start':start,'source_length':length,'source_file_id':file_id}
        return result
    except (ValueError,TypeError,IndexError,OverflowError):
        return {}

def derive(bundle,compiled,output_sha256):
    evidence=CompilerEntryEvidence()
    if not str(bundle.get('compiler',{}).get('compiler_version','')).startswith('0.4.'):
        return evidence
    for contract in bundle['contracts']:
        target=contract['file']+':'+contract['name']
        output=compiled.get('contracts',{}).get(contract['file'],{}).get(contract['name'],{})
        deployed=output.get('evm',{}).get('deployedBytecode',{})
        runtime=deployed.get('object','');source_map=deployed.get('sourceMap','')
        if not runtime or runtime.removeprefix('0x')!=contract.get('runtime','').removeprefix('0x'):continue
        if deployed.get('linkReferences') or contract.get('runtime_link_references'):continue
        selectors={f['selector'] for f in contract['functions']}
        branches=legacy_dispatch(runtime,source_map,selectors)
        if branches:
            evidence[target]={'program_id':bundle['program_id'],'build_id':bundle['build_id'],
                'standard_output_sha256':output_sha256,'runtime_sha256':hashlib.sha256(bytes.fromhex(runtime.removeprefix('0x'))).hexdigest(),
                'source_map_sha256':hashlib.sha256(source_map.encode()).hexdigest(),'grammar':'legacy_linear_dispatch_v2','branches':branches}
    return evidence
