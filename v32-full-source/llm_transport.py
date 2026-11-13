"""Bounded, single-request response reader. Never logs response text or reasoning.

An interrupted HTTP envelope may already contain a complete JSON response. Only
that received document is accepted; missing JSON bytes are never manufactured.
Actual usage and final content are still validated by the original caller.
"""
import hashlib
import http.client
import json
import time
from .core import require


def read_response(response, limit, diagnostics, deadline=None):
    parts=[];size=0;reads=0;interrupted=None
    diagnostics.update(reader='bounded_http_body_v1',bytes_received=0,read_calls=0,
                       body_complete_json=False,body_text_saved=False)
    try:
        while True:
            if deadline is not None and time.monotonic() >= deadline:
                raise TimeoutError('response_read_deadline')
            try:
                reads+=1
                piece=response.read(min(65536,limit+1-size))
            except http.client.IncompleteRead as error:
                piece=error.partial
                interrupted=error
                diagnostics['transport_error']='IncompleteRead'
            require(isinstance(piece,bytes),'response_body_not_bytes')
            parts.append(piece);size+=len(piece)
            diagnostics.update(bytes_received=size,read_calls=reads)
            require(size<=limit,'response_byte_limit_exceeded')
            if interrupted is not None or not piece:break
        raw=b''.join(parts)
        diagnostics['received_body_sha256']=hashlib.sha256(raw).hexdigest()
        try:
            document=json.loads(raw)
        except (ValueError,UnicodeError):
            if interrupted is not None:raise interrupted
            raise
        require(isinstance(document,dict),'response_envelope_not_object')
        # Only fully received JSON is eligible. A transport warning does not
        # prove billing or detection success; the caller separately checks both.
        diagnostics.update(body_complete_json=True,
            complete_json_despite_transport_error=interrupted is not None)
        return document
    except Exception as error:
        diagnostics.setdefault('transport_error',type(error).__name__)
        raise
