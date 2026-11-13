"""Compiler-scoped necessary conditions, not a whole-contract safety proof."""
import copy
from .core import digest
from .m03_p_paths import walk
from .source_entry_identity import builtin_call

def source_operation(lookup,function):
    cache=getattr(lookup,'_operation_scope_v7_cache',None)
    if cache is None:cache={};lookup._operation_scope_v7_cache=cache
    if function not in cache:cache[function]=_source_operation(lookup,function)
    return copy.deepcopy(cache[function])

def _source_operation(lookup,function):
    try:entry=lookup.function(function)
    except (ValueError,KeyError,TypeError):entry=None
    if not entry:return {'complete':False,'unknown_reasons':['entry_identity_unresolved']}
    if entry.get('generated_getter'):
        return {'complete':True,'generated_getter':True,'source_ast_ids':[entry['generated_getter']['id']],
                'reads':[],'writes':[],'guard_roots':[],'guard_sources':[],
                'credential':False,'authority_candidate':False,'external':False,
                'native':False,'destroy':False,'delegate':False,'unknown_reasons':[]}
    queue=[entry];seen=set();nodes=[];unknown=[];external=False;delegate=False;native=False;destroy=False;credential=False
    while queue:
        tree=queue.pop();ident=tree.get('id')
        if ident in seen:continue
        seen.add(ident)
        if tree.get('body') is None and tree.get('nodeType') in ('FunctionDefinition','ModifierDefinition'):
            unknown.append('missing_function_body')
        part=list(walk(tree));nodes.extend(part)
        for n in part:
            if n.get('nodeType')=='InlineAssembly':unknown.append('assembly_effects_unknown')
            if n.get('nodeType')=='ModifierInvocation':
                mod=lookup.nodes.get(n.get('modifierName',{}).get('referencedDeclaration'))
                if mod:queue.append(mod)
                else:unknown.append('modifier_unresolved')
            if n.get('nodeType')!='FunctionCall' or n.get('kind') in ('typeConversion','structConstructorCall'):continue
            f=n.get('expression',{});decl=lookup.nodes.get(f.get('referencedDeclaration'),{})
            name=f.get('name',f.get('memberName',''))
            if decl.get('nodeType')=='EventDefinition':continue
            if builtin_call(n,lookup,('selfdestruct','suicide')):native=True;destroy=True;continue
            if builtin_call(n,lookup,('ecrecover',)):credential=True;continue
            if builtin_call(n,lookup,('require','assert','revert','keccak256','sha3','sha256','ripemd160','addmod','mulmod','blockhash')):continue
            if f.get('nodeType')=='MemberAccess' and name in ('push','pop'):continue
            parent=lookup.nodes.get(decl.get('scope'),{})
            local=(f.get('nodeType')=='Identifier' or decl.get('visibility') in ('internal','private')
                   or parent.get('contractKind')=='library' or f.get('expression',{}).get('name')=='super')
            if decl.get('nodeType')=='FunctionDefinition' and local:queue.append(decl);continue
            if f.get('nodeType')=='MemberAccess' and name in ('encode','encodePacked','encodeWithSelector','encodeWithSignature') and f.get('expression',{}).get('name')=='abi':continue
            if f.get('nodeType')=='MemberAccess':
                external=True;delegate |= name in ('delegatecall','callcode');native |= name in ('transfer','send','value')
                unknown.append('external_call_permission_or_callback_unknown')
            elif not decl:unknown.append('call_target_unresolved')
    nodes=list({n.get('id',id(n)):n for n in nodes}.values());aliases={}
    for n in nodes:
        if n.get('nodeType')=='VariableDeclarationStatement' and len(n.get('declarations',[]))==1:
            d=n['declarations'][0]
            if d and d.get('storageLocation')=='storage':aliases[d['id']]=n.get('initialValue')
    def root(n,trail=frozenset()):
        if not n:return None,True
        k=n.get('nodeType')
        if k=='Identifier':
            rid=n.get('referencedDeclaration');decl=lookup.nodes.get(rid,{})
            if decl.get('stateVariable'):return rid,False
            if decl.get('storageLocation')=='storage':
                if rid in trail:return None,True
                return root(aliases[rid],trail|{rid}) if rid in aliases else (None,True)
            return None,False
        if k=='MemberAccess':return root(n.get('expression'),trail)
        if k=='IndexAccess':return root(n.get('baseExpression'),trail)
        if k=='TupleExpression' and len(n.get('components',[]))==1:return root(n['components'][0],trail)
        return None,True
    reads={n.get('referencedDeclaration') for n in nodes if lookup.nodes.get(n.get('referencedDeclaration'),{}).get('stateVariable')}
    writes=set();guards=[]
    for n in nodes:
        k=n.get('nodeType')
        if k=='Assignment' or k=='UnaryOperation' and n.get('operator') in ('++','--','delete'):
            r,opaque=root(n.get('leftHandSide',n.get('subExpression')))
            if r is not None:writes.add(r)
            if opaque:unknown.append('write_alias_unresolved')
        if k=='FunctionCall' and n.get('expression',{}).get('memberName') in ('push','pop'):
            r,opaque=root(n['expression'].get('expression'))
            if r is not None:writes.add(r)
            if opaque:unknown.append('array_mutation_alias_unresolved')
        if k in ('IfStatement','ForStatement','WhileStatement','DoWhileStatement') and n.get('condition'):guards.append(n['condition'])
        if k=='FunctionCall' and builtin_call(n,lookup,('require','assert')) and n.get('arguments'):guards.append(n['arguments'][0])
    # Hash/opaque credentials count only when compared as an authorization
    # value, not merely when hashing randomness or encoding event data.
    local_definitions={}
    for n in nodes:
        if n.get('nodeType')=='VariableDeclarationStatement' and len(n.get('declarations',[]))==1 and n['declarations'][0]:
            local_definitions[n['declarations'][0]['id']]=n.get('initialValue')
    def dependencies(node,seen=frozenset()):
        found=list(walk(node))
        for child in list(found):
            rid=child.get('referencedDeclaration')
            if rid in local_definitions and rid not in seen:found+=dependencies(local_definitions[rid],seen|{rid})
        return found
    for guard in guards:
        for comparison in walk(guard):
            if comparison.get('nodeType')!='BinaryOperation' or comparison.get('operator') not in ('==','!='):continue
            deps=dependencies(comparison)
            stored=any(lookup.nodes.get(n.get('referencedDeclaration'),{}).get('stateVariable') and
                n.get('typeDescriptions',{}).get('typeString','').startswith(('bytes','string')) for n in deps)
            credential |= stored and any(n.get('nodeType')=='FunctionCall' and builtin_call(n,lookup,('keccak256','sha3','sha256','ripemd160')) or
                n.get('nodeType')=='Identifier' and not lookup.nodes.get(n.get('referencedDeclaration'),{}).get('stateVariable') and
                n.get('typeDescriptions',{}).get('typeString','').startswith(('bytes','string')) for n in deps)
    gnodes=list(walk(guards))
    groots={n.get('referencedDeclaration') for n in gnodes if lookup.nodes.get(n.get('referencedDeclaration'),{}).get('stateVariable')}
    actor=any(n.get('nodeType')=='MemberAccess' and n.get('memberName') in ('sender','origin')
              and n.get('expression',{}).get('name') in ('msg','tx') for n in nodes)
    return {'complete':not unknown,'generated_getter':False,'source_ast_ids':sorted(seen-{None}),
            'reads':sorted(reads),'writes':sorted(writes),'guard_roots':sorted(groots),
            'guard_sources':sorted({n['id'] for n in guards if 'id' in n}),
            'credential':credential,'authority_candidate':bool(credential or actor and guards or external),
            'external':external,'native':native,'destroy':destroy,'delegate':delegate,
            'unknown_reasons':sorted(set(unknown))}

def exclusion(rule,operation,identity,target,function):
    if not operation.get('complete'):return None
    effect=bool(operation.get('writes') or operation.get('native') or operation.get('destroy') or operation.get('delegate'))
    reason=None
    if not effect and not operation.get('external'):reason='no_sensitive_state_or_external_effect'
    elif rule=='AC-05' and not operation.get('credential'):reason='no_authorization_credential_use_in_resolved_call_closure'
    elif rule in ('AC-03','AC-04') and not operation.get('guard_sources') and not operation.get('credential'):
        reason='no_checked_authorization_or_lifecycle_condition'
    elif rule in ('FCR-MINT','FCR-TRANSFER','FCR-DESTROY') and not operation.get('authority_candidate'):
        reason='no_caller_bound_independent_privilege_in_resolved_operation'
    if reason is None:return None
    return {'kind':'necessary_condition_absent','route':'P','verified':True,'rule':rule,
            'identity':copy.deepcopy(identity),'target':target,'function':function,'reason':reason,
            'operation_sha256':digest(operation),'source_ast_ids':operation['source_ast_ids'],
            'scope':'complete supplied operation and resolved calls only; not contract safety','not_a_safety_proof':True}
