"""Compiler-described code identities; never mask unmarked runtime bytes."""
import hashlib,re
from .core import require

def unhex(value):
 require(isinstance(value,str),'code_hex_type')
 value=value[2:] if value.startswith('0x') else value
 require(len(value)%2==0 and re.fullmatch('[0-9a-fA-F]*',value) is not None,'code_hex_encoding')
 return bytes.fromhex(value)

def ranges(references,size,kind):
 result=[]
 for key,entries in references.items():
  require(isinstance(entries,list),'reference_entries')
  for item in entries:
   start,length=item.get('start'),item.get('length')
   require(type(start)is int and type(length)is int and start>=0 and length>0 and start+length<=size,'reference_out_of_bounds')
   result.append({'kind':kind,'key':key,'start':start,'length':length})
 return result

def disjoint(items):
 ordered=sorted(items,key=lambda x:x['start'])
 require(all(a['start']+a['length']<=b['start'] for a,b in zip(ordered,ordered[1:])),'overlapping_code_references')
 return ordered

def link_code(template,references,libraries):
 require(isinstance(template,str) and not template.startswith('0x') and len(template)%2==0,'template_encoding')
 flat={file+':'+name:entries for file,names in references.items() for name,entries in names.items()}
 spans=disjoint(ranges(flat,len(template)//2,'library'));text=template;record=[]
 for item in spans:
  require(item['key'] in libraries,'unresolved_library:'+item['key'])
  address=unhex(libraries[item['key']]);require(len(address)==20 and item['length']==20,'library_address_width')
  lo=item['start']*2;hi=lo+item['length']*2
  record.append({**item,'template_fragment':template[lo:hi],'address':'0x'+address.hex()})
  text=text[:lo]+address.hex()+text[hi:]
 return unhex(text),record

def linked_artifact(contract,libraries=None):
 libraries=libraries or {}
 known={f+':'+n for key in ['creation_link_references','runtime_link_references'] for f,names in contract.get(key,{}).items() for n in names}
 require(set(libraries)==known,'library_binding_set_mismatch')
 creation,cr=link_code(contract['creation'],contract.get('creation_link_references',{}),libraries)
 runtime,rr=link_code(contract['runtime'],contract.get('runtime_link_references',{}),libraries)
 ir=ranges(contract.get('immutable_references',{}),len(runtime),'immutable')
 disjoint(rr+ir)
 return {'creation':creation.hex(),'runtime_template':runtime.hex(),'creation_links':cr,'runtime_links':rr,'immutable_ranges':ir}

def verify_runtime(contract,actual,libraries=None):
 linked=linked_artifact(contract,libraries);template=unhex(linked['runtime_template']);deployed=unhex(actual)
 require(len(template)==len(deployed),'deployed_runtime_length')
 spans=disjoint(linked['immutable_ranges']);cursor=0;values={};record=[]
 require(not spans or sum(x['length'] for x in spans)<len(deployed),'entire_runtime_cannot_be_masked')
 for item in spans:
  start=item['start'];end=start+item['length']
  require(template[cursor:start]==deployed[cursor:start],'runtime_unmarked_difference')
  value=deployed[start:end].hex()
  require(item['key'] not in values or values[item['key']]==value,'inconsistent_immutable_copies')
  values[item['key']]=value;record.append({**item,'template':'0x'+template[start:end].hex(),'deployed':'0x'+value});cursor=end
 require(template[cursor:]==deployed[cursor:],'runtime_unmarked_difference')
 return {'status':'matched_compiler_marked_ranges','runtime_sha256':hashlib.sha256(deployed).hexdigest(),'runtime_template_sha256':hashlib.sha256(template).hexdigest(),'runtime_bytes':len(deployed),'compared_unmasked_bytes':len(deployed)-sum(x['length'] for x in spans),'immutable_values':record,'creation_links':linked['creation_links'],'runtime_links':linked['runtime_links'],'whole_runtime_comparison_skipped':False}

def encode_static(types,arguments):
 require(len(types)==len(arguments),'constructor_arity');out=[]
 for typ,value in zip(types,arguments):
  require(isinstance(value,str),'argument_string_required')
  if typ=='address':
   raw=unhex(value);require(len(raw)==20,'address_width');out.append(raw.rjust(32,b'\0'))
  elif typ=='bool':
   require(value in ['true','false'],'bool_encoding');out.append(int(value=='true').to_bytes(32,'big'))
  elif re.fullmatch(r'u?int([0-9]+)?',typ):
   unsigned=typ.startswith('u');bits=int(re.search('[0-9]+',typ)[0]) if re.search('[0-9]+',typ) else 256
   require(8<=bits<=256 and bits%8==0,'integer_width');n=int(value)
   require(0<=n<2**bits if unsigned else -(2**(bits-1))<=n<2**(bits-1),'integer_range');out.append((n%(2**256)).to_bytes(32,'big'))
  elif re.fullmatch(r'bytes[0-9]+',typ):
   size=int(typ[5:]);raw=unhex(value);require(1<=size<=32 and len(raw)==size,'bytes_width');out.append(raw.ljust(32,b'\0'))
  else:require(False,'unsupported_constructor_abi:'+typ)
 return b''.join(out)

def verify_deployment(contract,receipt,arguments,libraries=None):
 require(receipt['status']=='success','deployment_not_successful')
 linked=linked_artifact(contract,libraries);encoded=encode_static(contract['constructor_types'],arguments)
 creation=unhex(linked['creation']);submitted=unhex(receipt['calldata'])
 require(submitted==creation+encoded,'creation_or_constructor_identity')
 actual=next((x['runtime'] for x in receipt['post'] if x['address'].lower()==receipt['target'].lower()),None)
 require(actual is not None and unhex(actual)==unhex(receipt['output']),'deployment_result_world_code_mismatch')
 verified=verify_runtime(contract,actual,libraries)
 return {**verified,'creation_sha256':hashlib.sha256(creation).hexdigest(),'original_creation_template':contract['creation'],'linked_creation':'0x'+creation.hex(),'constructor_types':contract['constructor_types'],'constructor_arguments':arguments,'constructor_encoding':'0x'+encoded.hex(),'submitted_creation':receipt['calldata'],'actual_deployed_runtime':actual,'target':receipt['target']}
