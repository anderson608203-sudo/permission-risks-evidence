"""Content identities, typed observation expressions and finite-query semantics."""
import hashlib,json,re
from . import SCHEMA_VERSION

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def digest(value):return hashlib.sha256(canonical(value)).hexdigest()
def ref(value):return {'id':value.get('id',digest(value)),'sha256':digest(value)}
class Invalid(ValueError):pass

def require(ok,reason):
 if not ok:raise Invalid(reason)

def expression(e,observers=None,symbols=None,point=None):
 """Return (type,value); type-only observers may use None. No eval/slot/code strings."""
 observers=observers or {};symbols=symbols or {}
 require(isinstance(e,dict),'expression_object')
 node=e.get('node');typ=e.get('type')
 valid_types={'Bool','Address160','IntDelta'}|{f'BV{i}' for i in range(8,257,8)}|{f'Bytes{i}' for i in range(1,33)}
 require(typ in valid_types,'invalid_type')
 if node=='literal':
  require(set(e)=={'node','type','value'},'literal_fields')
  v=e['value']
  if typ=='Bool':require(type(v) is bool,'bool_literal');return typ,v
  require(isinstance(v,str),'integer_strings_only')
  if typ=='IntDelta':require(bool(re.fullmatch(r'-?(0|[1-9][0-9]*)',v)),'int_literal');return typ,int(v)
  if typ.startswith('BV'):
   require(bool(re.fullmatch(r'0|[1-9][0-9]*',v)),'bv_literal')
   n=int(v);require(0<=n<2**int(typ[2:]),'bv_range');return typ,n
  size=20 if typ=='Address160' else int(typ[5:])
  require(bool(re.fullmatch('0x[0-9a-fA-F]{'+str(size*2)+'}',v)),'hex_width');return typ,v.lower()
 if node in ('observer','symbol'):
  key='observer_id' if node=='observer' else 'name'
  require(set(e)=={'node','type',key},'ref_fields')
  registry=observers if node=='observer' else symbols
  require(e.get(key) in registry,'unknown_reference')
  binding=registry[e[key]]
  require(binding['type']==typ,'reference_type')
  if point is not None:require(binding.get('point',0)<=point,'future_observer_precondition')
  return typ,binding.get('value')
 require(node=='op' and set(e)=={'node','type','operator','args'},'op_fields')
 op=e['operator'];args=e['args'];require(isinstance(args,list) and args,'op_args')
 ts,vs=zip(*(expression(a,observers,symbols,point) for a in args))
 unknown=any(v is None for v in vs)
 bools={'and','or'};intcmp={'int_lt','int_le','int_gt','int_ge'}
 bvops={'ult','ule','ugt','uge','slt','sle','sgt','sge','bvadd','bvsub','bvand','bvor','bvxor'}
 if op in bools:require(len(ts)>=2 and set(ts)=={'Bool'} and typ=='Bool','bool_arity_type');return typ,None if unknown else (all(vs) if op=='and' else any(vs))
 if op=='not':require(ts==('Bool',) and typ=='Bool','not_type');return typ,None if unknown else not vs[0]
 if op in {'eq','ne'}:require(len(ts)==2 and ts[0]==ts[1] and typ=='Bool','equality_type');return typ,None if unknown else ((vs[0]==vs[1]) if op=='eq' else (vs[0]!=vs[1]))
 if op=='ite':require(len(ts)==3 and ts[0]=='Bool' and ts[1]==ts[2]==typ,'ite_type');return typ,None if unknown else (vs[1] if vs[0] else vs[2])
 if op in {'to_int_unsigned','to_int_signed'}:
  require(len(ts)==1 and ts[0].startswith('BV') and typ=='IntDelta','int_decode_type')
  if unknown:return typ,None
  n=vs[0];bits=int(ts[0][2:])
  return typ,n-(2**bits if op=='to_int_signed' and n>=2**(bits-1) else 0)
 if op=='delta':require(ts==('IntDelta','IntDelta') and typ=='IntDelta','delta_requires_int');return typ,None if unknown else vs[0]-vs[1]
 if op in intcmp:
  require(ts==('IntDelta','IntDelta') and typ=='Bool','int_compare_type')
  return typ,None if unknown else {'int_lt':vs[0]<vs[1],'int_le':vs[0]<=vs[1],'int_gt':vs[0]>vs[1],'int_ge':vs[0]>=vs[1]}[op]
 if op in bvops:
  require(len(ts)==2 and ts[0]==ts[1] and ts[0].startswith('BV'),'bv_types')
  arithmetic=op.startswith('bv');require(typ==(ts[0] if arithmetic else 'Bool'),'bv_result')
  if unknown:return typ,None
  n=int(ts[0][2:]);a,b=vs
  if arithmetic:return typ,{'bvadd':a+b,'bvsub':a-b,'bvand':a&b,'bvor':a|b,'bvxor':a^b}[op]%(2**n)
  if op[0]=='s':a=a-(2**n if a>=2**(n-1) else 0);b=b-(2**n if b>=2**(n-1) else 0)
  return typ,{'lt':a<b,'le':a<=b,'gt':a>b,'ge':a>=b}[op[1:]]
 raise Invalid('unsupported_operator')

def lit(typ,value):return {'node':'literal','type':typ,'value':value if typ=='Bool' else str(value)}
def operator(op,typ,*args):return {'node':'op','operator':op,'type':typ,'args':list(args)}
def obs(oid,typ='BV256'):return {'node':'observer','observer_id':oid,'type':typ}
def delta(after,before):return operator('delta','IntDelta',operator('to_int_unsigned','IntDelta',after),operator('to_int_unsigned','IntDelta',before))

def interpret_result(form,premise,solver,execution,coverage,fidelity,witness=False):
 if premise=='unsat':return 'infeasible_premise'
 if premise!='sat':return 'inconclusive'
 if solver=='sat' and witness:
  return 'supported' if form in {'EXISTS_VIOLATION','EXPECTED_ACCESS_DENIED'} else 'refuted_in_scope'
 if solver=='unsat' and execution=='completed' and coverage=='complete_for_declared_query' and fidelity in {'exact_for_query','sound_overapprox_for_query'}:
  return 'refuted_in_scope' if form in {'EXISTS_VIOLATION','EXPECTED_ACCESS_DENIED'} else 'supported'
 return 'inconclusive'

def prediction(findings,critical_incomplete):
 if findings:return 'positive'
 return 'abstained' if critical_incomplete else 'no_finding'
