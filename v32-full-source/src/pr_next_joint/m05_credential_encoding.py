"""Exact fixed byte layouts; no hash injectivity or cryptographic oracle."""
import re
from .m04_logic import Unsupported

MAX_FIXED_LITERAL_BYTES = 4096


def fixed_literal(value):
    raw=value.get('hex');length=value.get('byte_length')
    if (value.get('kind')!='fixed_bytes_literal' or type(length) is not int
            or not 0<=length<=MAX_FIXED_LITERAL_BYTES or not isinstance(raw,str)
            or len(raw)!=2*length or re.fullmatch('[0-9a-fA-F]*',raw) is None):
        raise Unsupported('fixed_bytes_literal_layout')
    return raw.lower(),length


def layout(digest):
    if digest.get('kind')!='hash' or digest.get('algorithm')!='keccak256':
        raise Unsupported('credential_digest_not_keccak')
    encoded=digest.get('input',{})
    if encoded.get('kind')=='fixed_bytes_literal':
        _,length=fixed_literal(encoded)
        return {'mode':'raw_fixed_bytes','types':['fixed_bytes_literal:'+str(length)],'arguments':[encoded]}
    if encoded.get('kind')!='abi_encoding' or encoded.get('mode') not in ('encode','encodePacked'):
        raise Unsupported('credential_digest_not_fixed_source_encoding')
    types=encoded.get('types',[]);args=encoded.get('arguments',[])
    if not types or len(types)!=len(args):raise Unsupported('credential_payload_arity')
    typed=[]
    for typ,arg in zip(types,args):
        if arg.get('kind')=='fixed_bytes_literal':
            _,length=fixed_literal(arg)
            # A string literal in abi.encode has dynamic length/offset
            # semantics. Only its packed byte spelling is supported here.
            if encoded['mode']!='encodePacked' or not typ.startswith('literal_string'):
                raise Unsupported('credential_literal_cast_or_dynamic_ABI_not_lowered')
            typed.append('fixed_bytes_literal:'+str(length))
        else:
            if '[' in typ or typ in ('bytes','string') or typ.startswith(('struct ','tuple','literal_string')):
                raise Unsupported('credential_dynamic_payload_not_lowered')
            typed.append(typ)
    return {**encoded,'types':typed}


def certify_total_digest(encoder,digest):
    """Evaluate only scalar domains when r=0 makes the digest irrelevant.

    Arithmetic, indices and calls may fail before ecrecover and are rejected.
    No hash value is created or used as evidence by this certificate.
    """
    def leaf(value):
        kind=value.get('kind')
        if kind=='hash':
            certify_total_digest(encoder,value);return
        if kind=='fixed_bytes_literal':
            fixed_literal(value);return
        if kind=='storage':
            for segment in value.get('segments',[]):
                if 'key' in segment:leaf(segment['key'])
        elif kind not in ('literal','parameter','actual_sender','contract_address','transaction_origin','environment'):
            raise Unsupported('invalid_recovery_digest_evaluation_not_total')
        encoder.expr(value)
    encoded=layout(digest)
    for value in encoded['arguments']:leaf(value)
