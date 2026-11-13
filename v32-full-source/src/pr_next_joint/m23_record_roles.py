"""Source-complete timestamp-role certificate independent of unrelated path gaps.
Only compiler-bound uses are inspected; no variable/function names as roles.
"""
import copy
from .m03_p_paths import walk,key
from .m03_p_route import keys,value_type
from .m05_relation_model_scope import source_term


def time_record(selector,lookup,assets):
    from .m22_record_roles import shape
    if len(keys(selector))!=1 or selector.get('instance') or not str(value_type(selector,lookup)).startswith('uint'):return None
    if any(shape(a['balance_effect']['path'])==shape(selector) for a in assets):return None
    root=selector['root'];decl=lookup.nodes.get(root,{})
    if decl.get('typeName',{}).get('nodeType')!='Mapping':return None
    if decl['typeName']['valueType'].get('nodeType')!='ElementaryTypeName':return None
    evidence=[];clock_uses=[];seen=set()
    # A modifier or state initializer may contain another use of this record.
    # Auditing only FunctionDefinition bodies would not be source-complete.
    lineage=lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
    declarations=[n for cid in lineage for n in lookup.nodes[cid].get('nodes',[])]
    for fn in declarations:
        def visit(n,parent=None):
            if isinstance(n,list):return all(visit(x,parent) for x in n)
            if not isinstance(n,dict):return True
            if n.get('nodeType')=='Identifier' and n.get('referencedDeclaration')==root:
                if not parent or parent.get('nodeType')!='IndexAccess' or parent.get('baseExpression',{}).get('id')!=n.get('id'):return False
            if n.get('nodeType')=='IndexAccess' and n.get('baseExpression',{}).get('referencedDeclaration')==root:
                seen.add(n['id']);kind=(parent or {}).get('nodeType');accepted=None
                if kind=='Assignment' and parent.get('operator')=='=' and parent['leftHandSide']['id']==n['id']:
                    rhs=parent['rightHandSide']
                    if not any(x.get('referencedDeclaration')==root for x in walk(rhs)):accepted='scalar_replacement'
                elif kind=='UnaryOperation' and parent.get('operator')=='delete':accepted='clear_record'
                elif kind=='Return':accepted='explicit_scalar_getter'
                elif kind=='BinaryOperation' and parent.get('operator') in ('>','>=','<','<=','==','!='):
                    other=parent['rightExpression'] if parent['leftExpression']['id']==n['id'] else parent['leftExpression']
                    value=source_term(other,lookup,'',function_node=fn)
                    if value and value.get('kind')=='environment' and value.get('field') in ('timestamp','number'):
                        accepted='compared_with_source_clock';clock_uses.append(lookup.anchor(parent))
                if not accepted:return False
                evidence.append({'source':lookup.anchor(n),'usage':accepted})
            if n.get('nodeType')=='InlineAssembly':return False
            return all(visit(x,n) for x in n.values() if isinstance(x,(dict,list)))
        if not visit(fn):return None
    if not clock_uses:return None
    return {'selector':copy.deepcopy(selector),'roles':['time_control'],'basis':'complete compiler-AST indexed-use audit; all uses are clock comparisons, replacements or direct getters',
            'evidence':evidence,'clock_comparison_sources':clock_uses,'audited_access_ids':sorted(seen),
            'scope':'record purpose only; does not certify failed callers or whole-contract behavior'}
