"""Compiler-bound pure assembly reads, with explicit uses and bounds.
No external call, arbitrary memory write, storage write or signature-validity
assumption is introduced. Raw calldata words remain opaque to risk solving.
"""
import copy,re
from .m03_p_paths import op,lit,key
from .m20_assembly import bound_reference,yul_text
ID=r'[A-Za-z_$][A-Za-z0-9_$]*'
NUM=r'(?:0x[0-9a-fA-F]+|[0-9]+)'
LOAD=re.compile(r'('+ID+r'):=calldataload\(('+NUM+r')\)')
MEM=re.compile(r'('+ID+r'):=(?:mload\(add\(('+ID+r'),('+NUM+r')\)\)|byte\((0),mload\(add\(('+ID+r'),('+NUM+r')\)\)\))')

def length(value):
    return {'kind':'source_bytes_length','input':copy.deepcopy(value),'type':'uint256'}

def summarize(lookup,node,state):
    try:text=node.get('operations') or yul_text(node.get('AST',{}))
    except (ValueError,KeyError,TypeError):return None
    text=re.sub(r'/\*.*?\*/|//[^\n]*',' ',text,flags=re.S)
    text=re.sub(r'\s+','',text)
    if not text.startswith('{') or not text.endswith('}'):return None
    body=text[1:-1]
    parsed=[];position=0
    while position<len(body):
        match=LOAD.match(body,position)
        mode='calldata'
        if not match:match=MEM.match(body,position);mode='memory'
        if not match:return None
        parsed.append((mode,match));position=match.end()
    if not parsed or len(parsed)>8:return None
    updates={};evidence=[]
    for mode,m in parsed:
        dest=bound_reference(node,m[1],lookup);decl=lookup.nodes.get(dest,{})
        if dest is None or decl.get('stateVariable') or dest not in state['env'] or dest in updates:return None
        typ=decl.get('typeDescriptions',{}).get('typeString','')
        if mode=='calldata':
            if typ not in ('bytes32','uint256'):return None
            offset=int(m[2],16 if m[2].startswith('0x') else 10)
            if offset>=2**256:return None
            value={'kind':'source_calldata_word','input':copy.deepcopy(lookup.calldata),'offset':offset,
                   'type':'bytes32','scope':'opaque raw calldata read; no ABI-layout or permission inference'}
        else:
            base_name=m[2] or m[5];raw=m[3] or m[6];size=1 if m[4] else 32
            if typ not in (('uint8','bytes1') if size==1 else ('bytes32','uint256')):return None
            base_id=bound_reference(node,base_name,lookup)
            base_decl=lookup.nodes.get(base_id,{})
            if not base_decl.get('typeDescriptions',{}).get('typeIdentifier','').startswith('t_bytes_memory'):return None
            base=state['env'].get(base_id)
            if not base or base.get('kind')!='parameter' or not base.get('type','').startswith('bytes'):return None
            offset=int(raw,16 if raw.startswith('0x') else 10)-32
            if offset<0 or offset+size>128:return None
            from .m09_shared_policy import implies
            from .m04_logic import Unsupported
            try:valid=implies(lookup,state,op('>=',length(base),lit(offset+size)))
            except (Unsupported,ValueError):return None
            if not valid:return None
            value={'kind':'source_bytes_slice','input':copy.deepcopy(base),'offset':offset,'size':size,
                   'type':typ,'range_validated_at_source':True}
        updates[dest]=value;evidence.append({'declaration':dest,'value':value})
    state['env'].update(updates)
    state.setdefault('source_assembly_summaries',[]).append({'source':lookup.anchor(node),
        'kind':'pure_source_bound_byte_reads','writes':evidence,
        'no_external_or_storage_side_effect':True,'calldata_executable_use_remains_unsupported':True})
    return [state]

def encode(encoder,value):
    kind=value.get('kind')
    if kind=='source_bytes_length':
        base=value.get('input',{})
        if base.get('kind')!='parameter' or not base.get('type','').startswith('bytes'):
            from .m04_logic import Unsupported
            raise Unsupported('dynamic_bytes_length_not_bound')
        return encoder.atom(value,'uint256')
    if kind!='source_bytes_slice':return None
    from .m04_logic import Unsupported
    base=value.get('input',{});offset=value.get('offset');size=value.get('size')
    if base.get('kind')!='parameter' or not base.get('type','').startswith('bytes') or type(offset)is not int or size not in (1,32) or not 0<=offset<=127 or offset+size>128:
        raise Unsupported('dynamic_bytes_slice_not_bound')
    z=encoder.z
    # Byte congruence preserves overlap across reads and same-input recovery.
    parts=[]
    for i in range(size):
        item={'kind':'input_byte','input':base,'offset':offset+i,'type':'uint8'}
        parts.append(encoder.atom(item,'uint8')*256**(size-1-i))
    encoder.constraints.append(encode(encoder,length(base))>=offset+size)
    return z.Sum(*parts)
