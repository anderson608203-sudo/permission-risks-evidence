"""Declared ordinary execution context; pinned engine semantics, not fork conformance."""
from .core import require
FIXED={'chain_id':1,'coinbase':'0x00000000000000000000000000000000000000d4','base_fee':0,'block_gas_limit':30000000,'prev_randao':0}

def environment(block_number=1,timestamp=1000000):
 result={**FIXED,'block_number':block_number,'timestamp':timestamp};validate(result);return result

def validate(value,previous=None):
 require(isinstance(value,dict) and set(value)==set(FIXED)|{'block_number','timestamp'},'environment_fields')
 require(all(type(value[k]) is type(v) and value[k]==v for k,v in FIXED.items()),'unsupported_environment_value')
 require(all(type(value[k])is int and 0<=value[k]<2**64 for k in ['block_number','timestamp']),'environment_range')
 if previous is not None:
  b,t=value['block_number'],value['timestamp'];pb,pt=previous['block_number'],previous['timestamp']
  require((b==pb and t==pt) or (b>pb and t>pt),'invalid_block_time_transition')
 return value
