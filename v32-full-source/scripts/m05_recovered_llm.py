"""Offline derived parser view of an authentic settled response, never HTTP."""
import os,json,hashlib
from pathlib import Path
from pr_next_joint.core import digest,require
from pr_next_joint.m05_response_recovery import recover
from pr_next_joint.llm_stream import expected_wire_request

class Client:
    def __init__(self):self.packet=Path(os.environ['M05_RAW_RESPONSE_PACKET']).resolve();self.used=False
    def call(self,messages,label,max_tokens=None,timeout=1800,reasoning_effort='high',thinking=True):
        require(not self.used,'RECOVERY_SINGLE_USE');self.used=True
        read=lambda n:json.loads((self.packet/n).read_text(encoding='utf-8-sig'))
        receipt=read('receipt.json');request=read('request.json')
        expected={'model':'deepseek-flash','messages':messages,'response_format':{'type':'json_object'},
                  'thinking':{'type':'enabled'},'reasoning_effort':'high','stream':False}
        require(max_tokens is None and timeout==1800 and reasoning_effort=='high' and thinking is True,'RECOVERY_CALL_POLICY')
        require(digest(expected_wire_request(expected,receipt))==digest(request)==receipt['request_sha256'],'RECOVERY_REQUEST_IDENTITY')
        require(receipt.get('source_nature')=='real' and receipt.get('simulated') is False and
                receipt.get('label')==label and receipt.get('timeout_seconds')==timeout,'RECOVERY_SOURCE_POLICY')
        require(receipt.get('finish_reason')=='stop' and receipt.get('error_class')=='JSONDecodeError','RECOVERY_ONLY_FINISHED_JSON_PARSE_FAILURE')
        if request.get('stream'):
            require(receipt.get('http_response',{}).get('stream_complete') is True,'RECOVERY_STREAM_NOT_COMPLETE')
            require('stream_complete' not in receipt or receipt['stream_complete'] is True,'RECOVERY_CONFLICTING_STREAM_STATUS')
        raw=(self.packet/'final_content_raw.txt').read_bytes()
        require(hashlib.sha256(raw).hexdigest()==receipt['raw_final_content_sha256'],'RECOVERY_RAW_IDENTITY')
        rows=[json.loads(s) for s in (self.packet/'RESOURCE_LEDGER.jsonl').read_text(encoding='utf8').splitlines() if s.strip()]
        rid=receipt['request_id'];reserved=[r for r in rows if r.get('event')=='api_reserved' and r.get('request_id')==rid]
        settled=[r for r in rows if r.get('event')=='api_settled' and r.get('request_id')==rid]
        require(len(reserved)==len(settled)==1 and reserved[0]['request_sha256']==digest(request),'RECOVERY_SETTLEMENT_IDENTITY')
        require(settled[0]['input_tokens']==receipt['usage']['prompt_tokens'] and settled[0]['output_tokens']==receipt['usage']['completion_tokens'],'RECOVERY_USAGE_IDENTITY')
        content,conversion=recover(raw.decode('utf8'))
        return content,{**receipt,'original_status':receipt['status'],'status':'json_received',
            'delivery':'derived_parser_view_of_settled_raw_response','parser_conversion':conversion,
            'original_receipt_sha256':digest(receipt),'response_sha256':digest(content),
            'new_HTTP_call':False,'original_response_was_valid_json':False}
