"""Exact compiler-bound internal library receivers, including storage references.

Only top-level storage ref/pointer decoration is normalized. Declaration IDs,
array shapes, mapping key/value types, location and call kind stay distinct.
"""
import re

def storage_identity(typ):
    if not typ.startswith(('t_struct$', 't_array$', 't_mapping$')):
        return None
    return re.sub(r'_storage(?:_ptr|_ref)?$', '_storage', typ) if re.search(r'_storage(?:_ptr|_ref)?$',typ) else None

def receiver_matches(receiver_type, parameter_type):
    if receiver_type and receiver_type==parameter_type:return True
    a,b=storage_identity(receiver_type),storage_identity(parameter_type)
    return a is not None and a==b

def compiler_bound_receiver(lookup,node,target):
    from .m03_p_paths import walk
    if not target or target.get('nodeType')!='FunctionDefinition' or node.get('names') or not target.get('body') or target.get('visibility')!='internal':return False
    scope=lookup.nodes.get(target.get('scope'),{})
    if scope.get('nodeType')!='ContractDefinition' or scope.get('contractKind')!='library':return False
    expr=node.get('expression',{});args=node.get('arguments',[])
    params=target.get('parameters',{}).get('parameters',[])
    if expr.get('nodeType')!='MemberAccess' or len(params)!=len(args)+1:return False
    if expr.get('referencedDeclaration')!=target.get('id'):return False
    signature=expr.get('typeDescriptions',{}).get('typeIdentifier','')
    receiver=expr.get('expression',{})
    typ=receiver.get('typeDescriptions',{}).get('typeIdentifier','')
    parameter=params[0].get('typeDescriptions',{}).get('typeIdentifier','')
    if not receiver_matches(typ,parameter):return False
    if not signature.startswith('t_function_internal_'):return False
    if not any(signature.endswith('$'+marker+'$_'+bound+'_$') for marker in ('bound_to','attached_to') for bound in (typ,parameter)):return False
    return not any(n.get('nodeType')=='Assignment' or n.get('nodeType')=='UnaryOperation' and n.get('operator') in ('++','--','delete') for n in walk([receiver,*args]))
