"""Approved code-execution boundary rule, source-generated and M4-checked.
A positive describes attacker-selectable delegate execution/implementation,
not an executed exploit, asset loss, or inferred owner-only business intention.
"""
import copy,re
from .core import digest
from .m03_p_paths import walk,key,op,lit
from .m03_p_route import selectors,permission_atoms,value_type
from .m05_relation_model_scope import source_term
from .m05_mechanism_core import remap
from .m04_logic import Unsupported

def builtin_delegate(expr,lookup):
    return (expr.get('nodeType')=='MemberAccess' and expr.get('memberName') in ('delegatecall','callcode')
            and expr.get('expression',{}).get('typeDescriptions',{}).get('typeString') in ('address','address payable')
            and expr.get('referencedDeclaration') not in lookup.fns)

def literal_selector(n,lookup):
    if n.get('nodeType')=='Literal':return True
    if n.get('nodeType')!='FunctionCall':return False
    expr=n.get('expression',{});args=n.get('arguments',[])
    if n.get('kind')=='typeConversion' and n.get('typeDescriptions',{}).get('typeString','').startswith('bytes'):
        return len(args)==1 and literal_selector(args[0],lookup)
    from .source_entry_identity import builtin_call
    return builtin_call(n,lookup,('keccak256','sha3','sha256')) and bool(args) and all(a.get('nodeType')=='Literal' for a in args)

def target_links(lookup,fn,bindings=None,depth=0,active=(),declaration=None):
    """Compiler-bound call edges only; this is a dependency, not reachability."""
    if depth>6 or fn in active:return []
    f=declaration or lookup.function(fn)
    if not f or not f.get('body'):return []
    bindings=bindings or {};out=[]
    from .source_entry_identity import builtin_call
    statements=f.get('body',{}).get('statements',[])
    if any(n.get('nodeType')=='ExpressionStatement' and builtin_call(n.get('expression',{}),lookup) and n['expression'].get('arguments',[{}])[0].get('value')=='false' for n in statements):return []
    params={x['id']:x for x in f.get('parameters',{}).get('parameters',[])}
    assigned={v.get('referencedDeclaration') for n in walk(f.get('body',{})) if n.get('nodeType')=='Assignment' for v in walk(n.get('leftHandSide',{}))}
    def lower(n):
        if n.get('nodeType')=='Identifier' and n.get('referencedDeclaration') in params:
            if n['referencedDeclaration'] in assigned:return None
            d=params[n['referencedDeclaration']]
            return {'kind':'parameter','id':d['id'],'type':d.get('typeDescriptions',{}).get('typeString')}
        return source_term(n,lookup,fn,function_node=f)
    for n in walk(f.get('body',{})):
        if n.get('nodeType')=='FunctionCall':
            expr=n.get('expression',{});target=lookup.fns.get(expr.get('referencedDeclaration'))
            if builtin_delegate(expr,lookup):
                v=lower(expr.get('expression',{}))
                if v is not None:out.append({'target_term':remap(v,bindings),'source':lookup.anchor(n),'encoding':'compiler_member_delegatecall'})
            elif target and expr.get('nodeType')=='Identifier':
                args=[lower(a) for a in n.get('arguments',[])];parameters=target.get('parameters',{}).get('parameters',[])
                if len(args)!=len(parameters):continue
                nested={v['id']:remap(a,bindings) for v,a in zip(parameters,args) if a is not None}
                signature='ast_function_'+str(target['id'])
                for link in target_links(lookup,signature,nested,depth+1,active+(fn,),target):
                    out.append({**link,'call_chain':[lookup.anchor(n)]+link.get('call_chain',[])})
        elif n.get('nodeType')=='InlineAssembly':
            # Old solc stores an assembly operation string with compiler-bound
            # external references. Accept only a direct identifier destination.
            text=n.get('operations','')
            if not text:continue
            clean=re.sub(r'/\*.*?\*/|//[^\n]*',' ',text,flags=re.S)
            # Capture the second operand after balanced first-operand parentheses.
            for match in re.finditer(r'\b(delegatecall|callcode)\s*\(',clean):
                at=match.end();level=0;comma=None
                for j in range(at,len(clean)):
                    if clean[j]=='(':level+=1
                    elif clean[j]==')':
                        if level==0:break
                        level-=1
                    elif clean[j]==',' and level==0:comma=j;break
                if comma is None:continue
                name_match=re.match(r'\s*([A-Za-z_$][\w$]*)\s*,',clean[comma+1:])
                if not name_match:continue
                name=name_match.group(1)
                refs=n.get('externalReferences',[])
                if isinstance(refs,dict):refs=list(refs.values())
                refs=[x for r in refs for x in ([r] if 'declaration' in r else r.values())]
                if re.search(r'\blet\s+'+re.escape(name)+r'\b',clean) or re.search(r'\b'+re.escape(name)+r'\s*:=',clean):continue
                ids={r.get('declaration') for r in refs if not r.get('isSlot') and not r.get('isOffset') and lookup.nodes.get(r.get('declaration'),{}).get('name')==name}
                if len(ids)!=1:continue
                ident=next(iter(ids));decl=lookup.nodes[ident]
                if ident in bindings:v=bindings[ident]
                elif decl.get('stateVariable'):v={'kind':'storage','root':ident,'segments':[]}
                elif ident in {x['id'] for x in f.get('parameters',{}).get('parameters',[])}:v={'kind':'parameter','id':ident,'type':decl.get('typeDescriptions',{}).get('typeString')}
                else:continue
                out.append({'target_term':copy.deepcopy(v),'source':lookup.anchor(n),'external_declaration':ident,'encoding':'compiler_bound_assembly_destination','reachability_not_proven':True})
    return out

def authority(guards,destination,lookup,include_caller=True):
    atoms=[]
    for g in guards:
        if include_caller:atoms.extend(permission_atoms(g,lookup))
        for n in walk(g):
            if n.get('kind')=='op' and n.get('op')=='==' and len(n.get('args',[]))==2:
                for a,b in (n['args'],n['args'][::-1]):
                    if include_caller and a.get('kind')=='actual_sender' and (b.get('kind')=='contract_address' or b.get('kind')=='literal' and b.get('value')!=0):atoms.append(n)
                    if key(a)==key(destination) and (b.get('kind')=='contract_address' or b.get('kind')=='literal' and b.get('value')!=0 or b.get('kind')=='storage' and value_type(b,lookup) in ('address','address payable') and not any(v.get('kind')=='parameter' for v in walk(b))):atoms.append(n)
            if n.get('kind')=='storage' and value_type(n,lookup)=='bool' and any(key(v)==key(destination) for v in walk(n.get('segments',[]))):atoms.append(n)
    return op('or',*list({key(a):a for a in atoms}.values()))

def queries(context,state):
    rows=[];limits=[]
    for tid,lookup in state['lookups'].items():
        program={fn:ps for (t,fn),ps in state['paths'].items() if t==tid};lookup._v18_program=program
        code_nodes=[n for f in lookup.implementations for n in walk(f) if builtin_delegate(n,lookup) or n.get('nodeType')=='InlineAssembly' and ('delegatecall' in n.get('operations','') or 'callcode' in n.get('operations','') or any(x.get('nodeType')=='YulFunctionCall' and x.get('functionName',{}).get('name') in ('delegatecall','callcode') for x in walk(n.get('AST',{}))))]
        if not code_nodes and not any(e.get('kind')=='dangerous_external_call' for ps in program.values() for path in ps for e in path.get('sensitive_effects',[])):continue
        for n in code_nodes:
            if (n.get('nodeType')=='InlineAssembly'
                    and not any(e.get('assembly_binding') and e['source']['ast_id']==n['id'] for ps in program.values() for path in ps for e in path.get('sensitive_effects',[]))):
                limits.append({'target':tid,'phase':'delegate_destination_binding','reason':'assembly_delegate_path_not_bound','source':lookup.anchor(n),'not_safe_evidence':True})
        from .m26_code_paths import committed_invocation,storage_uses,bind_use
        uses=storage_uses(program)
        for fn,paths in program.items():
            for pi,path in enumerate(paths):
                candidates=[]
                for effect in path.get('sensitive_effects',[]):
                    if effect.get('kind')!='dangerous_external_call':continue
                    committed=committed_invocation(path,effect)
                    if committed is None:
                        if path['flow']!='reverted':limits.append({'target':tid,'function':fn,'phase':'delegate_committed_path','reason':'callee_or_path_not_fully_bound','source':effect['source'],'not_safe_evidence':True})
                        continue
                    guards,terms=committed
                    candidates.append((effect['recipient'],guards,[],terms,{**effect,'kind':'protected_delegate_entry','object':'caller_selected_delegate_target','selector':{'kind':'non_storage_effect','source_id':effect['source']['ast_id']}},[],authority(guards,effect['recipient'],lookup)))
                for w in path['writes']:
                    matching=uses.get(w['path']['root'],[])
                    if not matching or path['flow'] not in ('normal','returned') or path.get('evaluation_gaps') or w['value'].get('kind')!='parameter':continue
                    # Conditional successful invocation of caller-selected code.
                    # Only an unused-return call on that exact selected target
                    # can use the constructive no-op-callee witness.
                    issues=[];witness=[]
                    for issue in path['issues']:
                        node=lookup.nodes.get(issue.get('source',{}).get('ast_id'),{});expr=node.get('expression',{})
                        receiver=source_term(expr.get('expression',{}),lookup,fn) if expr.get('nodeType')=='MemberAccess' else None
                        parent=next((a for a in walk(lookup.function(fn)) if a.get('nodeType')=='ExpressionStatement' and a.get('expression',{}).get('id')==node.get('id')),None)
                        if issue.get('reason')=='external_destination_not_bound' and receiver is not None and key(receiver)==key(w['value']) and parent:
                            witness.append({'source':lookup.anchor(node),'kind':'caller_selected_noop_callee_returns_success','not_a_claim_about_fixed_external_contract':True})
                        else:issues.append(issue)
                    terms=[v for v in path.get('evaluated_terms',[]) if v!={'kind':'unknown','reason':'external_destination_not_bound'}] if witness and not issues else path.get('evaluated_terms',[])
                    effect={'object':str(w['path']['root']),'selector':w['path'],'value':w['value'],'operator':w['operator'],'source':w['source']}
                    for use in matching:
                        try:bound=bind_use(lookup,path,w,use)
                        except Unsupported as error:
                            limits.append({'target':tid,'function':fn,'phase':'delegate_sequence','reason':str(error)});continue
                        if bound is None:
                            if w['path'].get('segments'):limits.append({'target':tid,'function':fn,'phase':'delegate_sequence','reason':'indexed_destination_alias_not_verified'})
                            continue
                        use_guards,use_terms,target_policy,trace=bound
                        restriction=op('or',authority(path['guards'],w['value'],lookup),target_policy)
                        candidates.append((w['value'],path['guards']+use_guards,issues,terms+use_terms,effect,[trace]+witness,restriction))
                for dest,guards,issues,terms,effect,links_used,restriction in candidates:
                    if dest.get('kind')!='parameter' or not (dest.get('type','') in ('address','address payable') or dest.get('type','').startswith('contract ')):continue
                    basis={'basis':'source_caller_selected_code_execution_boundary','destination':dest,'binding_evidence':links_used,
                           'scope':'source mechanism of selecting code executed in this contract context; deployment exploit and asset loss not proven',
                           'approved_rule':'v18 D01','caller_and_target_restrictions':restriction}
                    row={'rule':'AC-01','target':tid,'function':fn,'path_index':pi,'conditions':copy.deepcopy(guards),'issues':copy.deepcopy(issues),
                         'effect':copy.deepcopy(effect),'required_policy_candidate':basis['caller_and_target_restrictions'],'policy_basis':basis,
                         'source_evaluation_terms':copy.deepcopy(terms),'program_id':context['identity']['program_id'],'build_id':context['identity']['build_id']}
                    row['id']='q_'+digest(row);rows.append(row)
    return list({r['id']:r for r in rows}.values()),limits

def formula(e,row,guards,change):
    dest=row['policy_basis']['destination'];encoded=e.expr(dest);z=e.z
    if not z.is_int(encoded):raise Unsupported('code_target_not_address')
    # The request may contain another caller-chosen alias of the destination.
    # Vary source scalar arguments together while keeping caller/storage fixed.
    substitutions=[];other=None
    params={key(v):v for v in walk([row['conditions'],row.get('source_evaluation_terms',[]),dest]) if v.get('kind')=='parameter' and (v.get('type','') in ('address','address payable','bool') or v.get('type','').startswith(('uint','int','contract '))) and '[' not in v.get('type','')}
    for value in params.values():
        if value.get('step') is not None:continue
        original=e.expr(value);fresh=z.FreshConst(original.sort(),'alternative_request_argument');substitutions.append((original,fresh))
        if key(value)==key(dest):other=fresh
    if other is None:raise Unsupported('code_target_not_source_parameter')
    premise=z.And(*guards,*e.constraints)
    twin=z.substitute(premise,*substitutions)
    required=e.expr(row['required_policy_candidate'])
    return z.And(*guards),z.And(change,z.Not(required),encoded!=0,other!=0,other!=encoded,other>=0,other<2**160,twin),{
        'kind':'source_code_execution_boundary','checks':['compiler-bound target dataflow','two request-controlled target choices under same caller/storage','effective caller/target authorization absent','source effect'],
        'not_proven':['actual exploit transaction','deployment reachability','asset loss']}
