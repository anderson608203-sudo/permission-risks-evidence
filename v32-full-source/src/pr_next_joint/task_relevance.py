"""Lightweight compiler-derived operation/dependency index for task completion.

This index only scopes checks; it never certifies a vulnerability or invents
asset semantics. Unresolved calls and storage aliases stay conservative.
"""
from .m03_p_paths import walk
from .m03_p_route import selectors
from .m05_relation_consumers import _state_root
from .source_entry_identity import builtin_call
from .core import digest
from .task_scope import AC, FCR

def inventory(context,state):
    result={}
    for target in context['targets']:
        tid=target['id'];lookup=state['lookups'][tid];items={}
        roots={i for i,n in lookup.nodes.items() if n.get('stateVariable')}
        ledgers={i for i in roots if 'mapping(address' in lookup.nodes[i].get('typeDescriptions',{}).get('typeString','').replace(' ','') and any(x in lookup.nodes[i].get('typeDescriptions',{}).get('typeString','') for x in ('uint','int','struct '))}
        controls=roots-ledgers  # scalar/record guard controls may be bool, enum, integer or address
        for f in target['functions']:
            fn=f['function'];ast=lookup.function(fn) or {};paths=state['paths'].get((tid,fn),[])
            nodes=list(walk(ast))
            # Compiler-resolved internal/helper and modifier dependencies. This
            # is a lightweight closure; no path re-expansion or policy guessing.
            visited=set();queue=list(nodes)
            for mod in ast.get('modifiers',[]):queue.append(lookup.nodes.get(mod.get('modifierName',{}).get('referencedDeclaration'),{}))
            for n in queue:
                ref=(n.get('expression',{}) if n.get('nodeType')=='FunctionCall' else {}).get('referencedDeclaration')
                decl=lookup.nodes.get(ref,{})
                if decl.get('nodeType') in ('FunctionDefinition','ModifierDefinition') and ref not in visited:
                    visited.add(ref);queue.extend(walk(decl))
            nodes=list({n.get('id',id(n)):n for n in queue}.values());read={n.get('referencedDeclaration') for n in nodes if n.get('referencedDeclaration') in roots}
            writes=set();unknown_alias=False;external=False;reject=False;credential=False;native=False
            for n in nodes:
                if n.get('nodeType') in ('Assignment','UnaryOperation'):
                    if n.get('nodeType')=='UnaryOperation' and n.get('operator') not in ('delete','++','--'):continue
                    left=n.get('leftHandSide',n.get('subExpression',{}));root=_state_root(left,lookup)
                    if root in roots:writes.add(root)
                    elif left.get('nodeType') in ('IndexAccess','MemberAccess'):unknown_alias=True
                if n.get('nodeType')=='FunctionCall':
                    expr=n.get('expression',{});name=expr.get('name',expr.get('memberName',''))
                    if builtin_call(n,lookup,('require','assert','revert')):reject=True;continue
                    if name in ('ecrecover','keccak256','sha256'):credential=True
                    decl=lookup.nodes.get(expr.get('referencedDeclaration'),{})
                    if decl.get('nodeType')=='EventDefinition':continue
                    if expr.get('memberName') in ('call','delegatecall','send','transfer','value'):
                        external=True;native=True
                    elif expr.get('nodeType')=='MemberAccess' and decl.get('visibility') in ('public','external') and not decl.get('stateMutability') in ('pure','view'):
                        external=True
                    elif not decl and expr.get('nodeType')=='MemberAccess':external=True
            for branch in paths:
                writes.update(s['root'] for w in branch.get('writes',[]) for s in [w['path']])
                read.update(s['root'] for s in selectors(branch.get('guards',[])))
                native |= bool(branch.get('native_transfers'))
            # A modifier body is part of this invocation, not an unrelated entry.
            for mod in ast.get('modifiers',[]):
                decl=lookup.nodes.get(mod.get('modifierName',{}).get('referencedDeclaration'),{})
                read.update(n.get('referencedDeclaration') for n in walk(decl) if n.get('referencedDeclaration') in roots)
            items[fn]={'target':tid,'function':fn,'reads':sorted(read),'writes':sorted(writes),
                'potential_ledger_effect':bool(writes&ledgers),'unknown_storage_effect':unknown_alias,
                'external_effect':external,'native_effect':native,'credential_use':credential,
                'rejection_site':reject,'generated_getter':bool(ast.get('generated_getter')),
                'source_ast_id':ast.get('id'),'source_semantics_unknown':not bool(paths) or any(p.get('issues') or p.get('evaluation_gaps') or p.get('flow')=='truncated' for p in paths)}
        from .operation_scope import source_operation,exclusion
        for fn,x in items.items():
            facts=source_operation(lookup,fn);x['operation_facts']=facts
            x['reads']=facts.get('reads',x['reads']);x['writes']=facts.get('writes',x['writes'])
            x['credential_use']=facts.get('credential',False)
            x['source_index_complete']=facts.get('complete',False)
        # A numeric ledger tied to a native transfer need not be mapping(address=>uint).
        # Keep roots consumed by source-bound asset effects in the relevance set.
        ledgers.update(sel['root'] for fn in items for path in state['paths'].get((tid,fn),[])
                       for effect in path.get('native_transfers',[])+path.get('sensitive_effects',[])
                       for sel in selectors(effect) if sel.get('root') in roots)
        asset_actions={fn for fn,x in items.items() if set(x['writes'])&ledgers or x['operation_facts'].get('native')}
        control_roots={r for fn in asset_actions for r in items[fn]['operation_facts'].get('guard_roots',[])
                       if r not in ledgers and lookup.nodes.get(r,{}).get('typeDescriptions',{}).get('typeString') not in ('address','address payable')}
        permission_roots={r for x in items.values() if x['operation_facts'].get('authority_candidate')
                          for r in x['operation_facts'].get('guard_roots',[]) if r not in ledgers}
        lifecycle_roots={r for r in permission_roots if lookup.nodes.get(r,{}).get('typeDescriptions',{}).get('typeString') not in ('address','address payable')}
        for fn,x in items.items():
            facts=x['operation_facts'];possible=set()
            effect=bool(x['writes'] or facts.get('native') or facts.get('destroy') or facts.get('delegate'))
            if not facts.get('complete'):possible.update(AC+FCR)
            if effect:
                possible.add('AC-01')
                if set(x['writes'])&permission_roots:possible.add('AC-02')
                # A caller==single administrator check alone has no mismatched
                # subject/object relation. Parameter/keyed credentials, tx.origin
                # and inferred candidates remain relevant.
                guard_ids=facts.get('guard_sources',[])
                guard_nodes=[n for gid in guard_ids for n in walk(lookup.nodes.get(gid,{}))]
                identity_parameters=any(n.get('nodeType')=='Identifier' and
                    not lookup.nodes.get(n.get('referencedDeclaration'),{}).get('stateVariable') and
                    n.get('typeDescriptions',{}).get('typeString') in ('address','address payable') for n in guard_nodes)
                keyed_identity=any(n.get('nodeType')=='IndexAccess' and
                    n.get('typeDescriptions',{}).get('typeString') in ('address','address payable','bool') for n in guard_nodes)
                origin=any(n.get('nodeType')=='MemberAccess' and n.get('memberName')=='origin' for n in guard_nodes)
                if identity_parameters or keyed_identity or origin:possible.add('AC-03')
                if set(facts.get('guard_roots',[]))&lifecycle_roots:possible.add('AC-04')
            possible.update(c['rule'] for c in context.get('candidate_relations',[]) if c['target']==tid and c['function']==fn)
            if facts.get('credential'):possible.add('AC-05')
            if fn in asset_actions:possible.update(('FCR-MINT','FCR-TRANSFER','FCR-DESTROY'))
            if fn in asset_actions and set(facts.get('guard_roots',[]))&control_roots or set(x['writes'])&control_roots:
                possible.update(('FCR-PAUSE','FCR-FREEZE'))
            x['exclusions']={}
            for rule in AC+FCR:
                proof=exclusion(rule,facts,context['identity'],tid,fn)
                if proof:x['exclusions'][rule]=proof;possible.discard(rule)
            x['possible_rules']=sorted(possible)
            x['certificate_kind']='compiler_operation_dependencies_v2'
            x['classification_meaning']='source necessity and dependencies, not safety'
            result[(tid,fn)]=x
    return result
