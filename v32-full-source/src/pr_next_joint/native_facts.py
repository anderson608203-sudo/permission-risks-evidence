"""Serialize fresh Slither SSA with original source anchors, no classifier."""
import sys
from importlib.metadata import version

def source(x):
 s=x.source_mapping
 return {'file':str(s.filename.relative),'start':s.start,'length':s.length,'lines':s.lines}
def variable(v):return {'name':str(v),'class':type(v).__name__,'type':str(getattr(v,'type',None)),'canonical_name':getattr(v,'canonical_name',None)}
def extract(slither,bundle,receipt):
 functions=[]
 for contract in slither.contracts:
  for f in contract.functions_and_modifiers_declared:
   nodes=[]
   for n in f.nodes:
    ops=[]
    for ir in n.irs_ssa:
     op={'operation':type(ir).__name__,'text':str(ir),'reads':[variable(v) for v in ir.read],'lvalue':variable(ir.lvalue) if getattr(ir,'lvalue',None) is not None else None}
     for k in ['variable_left','variable_right','function','arguments']:
      if hasattr(ir,k):op[k]=[str(a) for a in ir.arguments] if k=='arguments' else str(getattr(ir,k))
     ops.append(op)
    nodes.append({'id':n.node_id,'type':str(n.type),'source':source(n),'expression':str(n.expression),'ssa':ops,'successors':[s.node_id for s in n.sons]})
   functions.append({'contract':contract.name,'signature':f.full_name,'canonical_name':f.canonical_name,'source':source(f),'visibility':f.visibility,'parameters':[variable(v) for v in f.parameters],'reads':[v.canonical_name for v in f.all_state_variables_read()],'writes':[v.canonical_name for v in f.all_state_variables_written()],'modifiers':[m.canonical_name for m in f.modifiers],'nodes':nodes})
 return {'program_id':bundle['program_id'],'build_id':bundle['build_id'],'python':sys.version,'slither':version('slither-analyzer'),'crytic_compile':version('crytic-compile'),'compiler':receipt,'functions':functions,'ssa_operation_count':sum(len(n['ssa']) for f in functions for n in f['nodes']),'fresh':True}
