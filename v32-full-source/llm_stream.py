"""Single-dispatch SSE transport and strict semantic/wire identity separation.

Official contract: /api/create-chat-completion, stream + include_usage.
Keep-alive comments are ignored. Reasoning deltas are never persisted.
"""
import hashlib,http.client,json,time
from .core import require,digest

def stream_request(request):
    require(request.get('stream') is False and 'stream_options' not in request,'SSE_BASE_REQUEST_SHAPE')
    return {**request,'stream':True,'stream_options':{'include_usage':True}}

def expected_wire_request(expected,receipt):
    mode=receipt.get('request_transport','json_v1')
    require(mode in ('json_v1','sse_v1'),'LLM_UNKNOWN_TRANSPORT')
    if mode=='json_v1':return expected
    require(receipt.get('semantic_request_sha256')==digest(expected),'LLM_SEMANTIC_REQUEST_IDENTITY')
    require(receipt.get('http_response',{}).get('stream_complete') is True,'LLM_STREAM_NOT_COMPLETE')
    return stream_request(expected)

def read_stream(response,limit,diagnostics,deadline=None,partial_path=None):
    """Do not accept a partial stream, invent usage, or dispatch another HTTP."""
    diagnostics.update(reader='sse_v1',bytes_received=0,events=0,keep_alive_comments=0,
                       content_fragments=0,reasoning_fragments_discarded=0,
                       stream_complete=False,body_text_saved=False)
    total=0;hasher=hashlib.sha256();event=[];parts=[];identity=None;model=None
    usage=None;finish=None;done=False
    def parse_event(lines):
        nonlocal identity,model,usage,finish,done
        if not lines:return
        payload='\n'.join(lines)
        if payload=='[DONE]':
            require(finish is not None,'SSE_DONE_WITHOUT_FINISH')
            require(isinstance(usage,dict),'SSE_DONE_WITHOUT_USAGE')
            done=True;return
        data=json.loads(payload)
        require(isinstance(data,dict) and 'error' not in data,'SSE_INVALID_EVENT')
        require(isinstance(data.get('id'),str) and isinstance(data.get('model'),str),'SSE_IDENTITY_MISSING')
        if identity is None:
            identity=data['id'];model=data['model']
            diagnostics.update(response_id=identity,response_model=model)
        require(data['id']==identity and data['model']==model,'SSE_MIXED_RESPONSE_IDENTITY')
        diagnostics['events']+=1
        if data.get('usage') is not None:
            require(isinstance(data['usage'],dict),'SSE_USAGE_SHAPE')
            require(usage is None or usage==data['usage'],'SSE_CONFLICTING_USAGE')
            usage=data['usage'];diagnostics['usage_received']=True
        choices=data.get('choices')
        require(isinstance(choices,list) and len(choices)<=1,'SSE_CHOICES_SHAPE')
        if choices:
            c=choices[0];require(c.get('index')==0,'SSE_CHOICE_INDEX')
            delta=c.get('delta',{})
            require(isinstance(delta,dict) and not delta.get('tool_calls'),'SSE_DELTA_SHAPE')
            text=delta.get('content')
            if text is not None:
                require(isinstance(text,str),'SSE_CONTENT_SHAPE')
                require(not text or finish is None,'SSE_CONTENT_AFTER_FINISH')
                parts.append(text);diagnostics['content_fragments']+=bool(text)
            if delta.get('reasoning_content'):
                diagnostics['reasoning_fragments_discarded']+=1
            if c.get('finish_reason') is not None:
                require(finish is None,'SSE_DUPLICATE_FINISH');finish=c['finish_reason']
                require(isinstance(finish,str),'SSE_FINISH_SHAPE')
                diagnostics['finish_reason']=finish
    try:
        while not done:
            if deadline is not None and time.monotonic()>=deadline:raise TimeoutError('SSE_deadline')
            # A bounded line read exposes SSE progress without waiting for the
            # full completion. The cumulative limit includes discarded reasoning.
            line=response.readline(min(1048577,limit+1-total))
            require(isinstance(line,bytes),'SSE_LINE_NOT_BYTES')
            total+=len(line);hasher.update(line);diagnostics['bytes_received']=total
            require(total<=limit,'response_byte_limit_exceeded')
            require(len(line)<=1048576,'SSE_LINE_LIMIT')
            if not line:raise http.client.IncompleteRead(b'')
            if not line.endswith(b'\n'):raise http.client.IncompleteRead(b'')
            text=line.decode('utf8').rstrip('\r\n')
            if text=='':parse_event(event);event=[]
            elif text.startswith(':'):diagnostics['keep_alive_comments']+=1
            elif text.startswith('data:'):event.append(text[5:].lstrip(' '))
            else:require(False,'SSE_UNEXPECTED_FIELD')
        diagnostics.update(stream_complete=True,received_body_sha256=hasher.hexdigest())
        return {'id':identity,'model':model,'usage':usage,'choices':[{
            'index':0,'finish_reason':finish,'message':{'role':'assistant','content':''.join(parts)}}]}
    except Exception as error:
        diagnostics.update(transport_error=type(error).__name__,received_body_sha256=hasher.hexdigest(),
                           finish_received=finish is not None,usage_received=usage is not None,
                           automatic_retry_allowed=False,partial_text_is_valid_response=False)
        if partial_path is not None and parts:
            content=''.join(parts).encode('utf8');partial_path.write_bytes(content)
            diagnostics.update(partial_final_text_saved=True,partial_final_text_sha256=hashlib.sha256(content).hexdigest(),
                               partial_final_text_bytes=len(content),partial_text_is_valid_response=False)
        raise
