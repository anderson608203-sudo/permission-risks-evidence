## source/src/pr_next_joint/graph/object_equivalence.py

~~~~python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""
import re
from pr_next_joint.checks.credentials.credential_encoding import fixed_literal
from pr_next_joint.verification.expressions import Unsupported


def literal_key(term, declaration):
    raw, length = fixed_literal(term)
    target = declaration.get('keyType', {})
    typ = target.get('name') or target.get('typeDescriptions', {}).get('typeString')
    if declaration.get('nodeType') != 'Mapping':
        raise Unsupported('literal_index_without_mapping_domain')
    if typ in ('string', 'bytes'):
        # Prefixing a byte preserves length, including empty and leading NULs.
        return int('01' + raw, 16)
    match = re.fullmatch(r'bytes([1-9]|[12][0-9]|3[0-2])', typ or '')
    if match and length <= int(match[1]):
        # Solidity pads a string literal with zeros on the right on conversion.
        return int(raw.ljust(2 * int(match[1]), '0'), 16)
    raise Unsupported('literal_key_conversion_outside_mapping_domain')

def selector_equalities(left, right, lookup):
    from pr_next_joint.frontend.path_ir import lit, op
    declaration = lookup.nodes[left['root']].get('typeName', {})
    tests = []
    # Callers have checked storage root, receiver, field sequence and arity.
    if len(left['segments']) != len(right['segments']):
        raise Unsupported('literal_selector_structure')
    for a, b in zip(left['segments'], right['segments']):
        if 'key' in a and 'key' in b:
            x, y = a['key'], b['key']
            if x.get('kind') == y.get('kind') == 'fixed_bytes_literal':
                tests.append(lit(literal_key(x, declaration) == literal_key(y, declaration)))
            else:
                tests.append(op('==', x, y))
            declaration = declaration.get('valueType', declaration.get('baseType', {}))
        elif a == b and 'field' in a:
            declaration = lookup.nodes[a['field']].get('typeName', {})
        elif a != b:
            raise Unsupported('literal_selector_structure')
    return tests

~~~~

## source/src/pr_next_joint/graph/relation_model_scope.py

~~~~python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""
from pr_next_joint.frontend.path_ir import walk

def source_term(node,lookup,function,function_node=None):
    """Pure, deliberately small AST projection; no calls or local alias guess."""
    fn=function_node or lookup.function(function) or {}
    params={p['id']:p for p in fn.get('parameters',{}).get('parameters',[])}
    def lower(n):
        kind=n.get('nodeType');ref=n.get('referencedDeclaration')
        if kind=='VariableDeclaration' and n.get('stateVariable') and n.get('id') in lookup.decls:
            return {'kind':'storage','root':n['id'],'segments':[]}
        if kind=='VariableDeclaration' and n.get('id') in params:
            return {'kind':'parameter','id':n['id'],'type':params[n['id']]['typeDescriptions']['typeString']}
        if kind=='Identifier':
            # Same authenticated compiler builtins used by the path evaluator.
            # A user declaration named now/block/msg is never a builtin.
            if (n.get('name')=='now' and type(ref) is int and ref not in lookup.nodes
                    and n.get('typeDescriptions',{}).get('typeIdentifier')=='t_uint256'):
                return {'kind':'environment','field':'timestamp','type':'uint256'}
            decl=lookup.nodes.get(ref,{})
            if decl.get('stateVariable'):return {'kind':'storage','root':ref,'segments':[]}
            if ref in params:return {'kind':'parameter','id':ref,'type':params[ref]['typeDescriptions']['typeString']}
        if kind=='Literal':
            if n.get('kind')=='bool':return {'kind':'literal','value':n['value']=='true'}
            if n.get('kind')=='number':
                try:return {'kind':'literal','value':int(n['value'],0)}
                except ValueError:return None
        if kind=='MemberAccess':
            e=n.get('expression',{})
            from pr_next_joint.frontend.source_entry_identity import builtin_object
            if builtin_object(e,lookup,'msg') and n.get('memberName')=='sender':return {'kind':'actual_sender'}
            if builtin_object(e,lookup,'block') and n.get('memberName') in ('timestamp','number'):
                return {'kind':'environment','field':n['memberName'],'type':'uint256'}
            base=lower(e)
            if base and base.get('kind')=='storage' and type(ref)is int and ref>=0:
                return {**base,'segments':base['segments']+[{'field':ref,'label':n['memberName']}]}
        if kind=='IndexAccess':
            base=lower(n.get('baseExpression',{}));index=lower(n.get('indexExpression') or {})
            if base and index and base.get('kind')=='storage':return {**base,'segments':base['segments']+[{'key':index}]}
        if kind=='TupleExpression' and not n.get('isInlineArray'):
            parts=n.get('components',[])
            if len(parts)==1 and parts[0] is not None:return lower(parts[0])
        if kind=='ExpressionStatement':return lower(n.get('expression',{}))
        if kind=='FunctionCall':
            f=n.get('expression',{});ref=f.get('referencedDeclaration')
            from pr_next_joint.frontend.source_entry_identity import builtin_call
            if builtin_call(n,lookup) and n.get('arguments'):
                return lower(n['arguments'][0])
        if kind in ('BinaryOperation','UnaryOperation'):
            nodes=[n.get('subExpression',{})] if kind=='UnaryOperation' else [n.get('leftExpression',{}),n.get('rightExpression',{})]
            args=[lower(a) for a in nodes];operator=n.get('operator')
            if all(a is not None for a in args) and operator in ('!','&&','||','==','!=','<','<=','>','>=','+','-','&','|'):
                from pr_next_joint.frontend.path_ir import normalize
                return normalize({'kind':'op','op':operator,'args':args})
        if kind=='IfStatement':
            condition=lower(n.get('condition',{}))
            if condition is None:return None
            true=n.get('trueBody',{});false=n.get('falseBody')
            def bare_revert(branch):
                statements=branch.get('statements',[]) if branch.get('nodeType')=='Block' else [branch]
                if len(statements)!=1:return False
                x=statements[0];call=x.get('expression',{}) if x.get('nodeType')=='ExpressionStatement' else x
                from pr_next_joint.frontend.source_entry_identity import builtin_call
                return x.get('nodeType')=='RevertStatement' or builtin_call(call,lookup,('revert',))
            from pr_next_joint.frontend.path_ir import normalize, op
            if bare_revert(true) and not false:return normalize(op('!',condition))
            if false and bare_revert(false):return condition
        return None
    if node.get('nodeType') in ('FunctionCall','RevertStatement'):
        from pr_next_joint.frontend.source_entry_identity import builtin_call
        if node.get('nodeType')=='RevertStatement' or builtin_call(node,lookup,('revert',)):
            operation=[fn]
            for modifier in fn.get('modifiers',[]):operation.append(lookup.nodes.get(modifier.get('modifierName',{}).get('referencedDeclaration'),{}))
            candidates=[n for n in walk(operation) if n.get('nodeType')=='IfStatement' and any(v.get('id')==node.get('id') for v in walk(n))]
            candidates.sort(key=lambda n:len(list(walk(n))))
            for ancestor in candidates:
                value=lower(ancestor)
                if value is not None:return value
    return lower(node)

~~~~

## source/src/pr_next_joint/graph/state_relations.py

~~~~python
"""Extracted generic source/encoding helpers; no legacy risk discovery."""
import copy
from pr_next_joint.frontend.path_ir import key, op, lit
from pr_next_joint.frontend.storage import value_type
from pr_next_joint.verification.expressions import Unsupported
from pr_next_joint.checks.access.credential_lifecycle import leaves

def enum_size(lookup,typ):
    if not isinstance(typ,str) or not typ.startswith('enum '):return None
    name=typ[5:]
    found=[n for n in lookup.nodes.values() if n.get('nodeType')=='EnumDefinition'
           and (n.get('canonicalName')==name or n.get('name')==name)]
    if len(found)!=1:raise Unsupported('enum_declaration_not_unique:'+name)
    size=len(found[0]['members'])
    if not 0<size<=256:raise Unsupported('enum_domain_size')
    return size

def scalar(write,lookup):
    if write['value'].get('kind')!='zero_of_storage_type':return write
    typ=value_type(write['path'],lookup)
    if typ=='bool':zero=False
    elif typ and (typ.startswith(('uint','bytes','enum ')) or typ in ('address','address payable')):zero=0
    else:raise Unsupported('container_delete_not_scalar')
    return {**write,'value':lit(zero),'zeroing_source_operator':write.get('operator')}

def expand_write(write,lookup,depth=0):
    """Expand deletion of an already bound finite struct; no source discovery."""
    if depth>8:raise Unsupported('finite_delete_structure_depth')
    if write['value'].get('kind')=='record':
        return [x for leaf in leaves(write) for x in expand_write(leaf,lookup,depth+1)]
    if write['value'].get('kind')!='zero_of_storage_type':return [write]
    typ=lookup.nodes.get(write['path']['root'],{}).get('typeName',{})
    for segment in write['path'].get('segments',[]):
        typ=typ.get('valueType',{}) if 'key' in segment else lookup.nodes.get(segment['field'],{}).get('typeName',{})
    declaration=lookup.nodes.get(typ.get('referencedDeclaration'),{})
    if declaration.get('nodeType')!='StructDefinition':return [scalar(write,lookup)]
    result=[]
    for member in declaration.get('members',[]):
        if member.get('typeName',{}).get('nodeType') in ('Mapping','ArrayTypeName'):
            raise Unsupported('finite_delete_dynamic_member_not_modeled')
        path={**write['path'],'segments':write['path'].get('segments',[])+[{'field':member['id']}]}
        result+=expand_write({**write,'path':path,'expanded_delete_source':copy.deepcopy(write['path'])},lookup,depth+1)
    if not result:raise Unsupported('finite_delete_empty_structure')
    return result

def compose_read(value,writes,lookup):
    """Source-keyed read-over-write, including updates to an aliased key."""
    from pr_next_joint.frontend.storage import fields, keys
    from pr_next_joint.frontend.path_ir import normalize
    if isinstance(value,dict):
        if value.get('kind')=='storage':
            result=copy.deepcopy(value)
            for w in writes:
                p=w['path']
                from pr_next_joint.frontend.storage import selector_relation
                relation=selector_relation(value,p)
                if relation=='disjoint':continue
                if relation!='same_shape':raise Unsupported('transition_container_update_not_scalar:'+relation)
                w=scalar(w,lookup)
                a,b=keys(value),keys(p)
                if len(a)!=len(b):raise Unsupported('transition_selector_arity')
                if any(x.get('kind')=='fixed_bytes_literal' and y.get('kind')=='fixed_bytes_literal' for x,y in zip(a,b)):
                    from pr_next_joint.graph.object_equivalence import selector_equalities
                    tests=selector_equalities(value,p,lookup)
                else:
                    tests=[op('==',x,y) for x,y in zip(a,b)]
                same=normalize(op('and',*tests))
                result=w['value'] if same==lit(True) else op('ite',same,w['value'],result)
            return result
        return {k:compose_read(v,writes,lookup) for k,v in value.items()}
    return [compose_read(v,writes,lookup) for v in value] if isinstance(value,list) else value

~~~~

## source/src/pr_next_joint/investigation/__init__.py

~~~~python
"""Source-led semantic investigation; no legacy relation admission."""

~~~~

## source/src/pr_next_joint/investigation/authorization.py

~~~~python
"""Consume a necessary authorization premise from existing text and actual source.

The certificate excludes an asserted causal acquisition, never all access-control
risks in the same function or contract. It does not invent a business policy.
"""
import re
from pr_next_joint.frontend.path_ir import walk, key
from pr_next_joint.frontend.storage import selectors, keys, value_type
from .request_scope import claim_entries
from .initial_state import runtime_writers


def acquisition_premise(inv,q):
    if inv.f.options.scope!='AC':return None
    item=q['current'];root=inv.root(q)
    if not root or not q['binding'].get('core_exact'):return None
    text=item['claim']+' '+str((item.get('observation') or {}).get('risk','') if isinstance(item.get('observation'),dict) else '')
    if not re.search(r'\b(?:acquir\w*|gain\w*|install\w*|takeover|becom\w*|owner acquisition|effective.*gate)\b|取得|接管|获得',text,re.I):return None
    entries=claim_entries(inv,q['binding'],item)
    if len(entries)<2 or not inv.backend.complete(root):return None
    target=inv.f.operations[root]['target'];lookup=inv.f.lookup(root)
    writes=[w for _,p in inv.f.operation_paths(root,True) for w in p['writes']]
    address_writes=[w for w in writes if value_type(w['path'],lookup) in ('address','address payable') and not keys(w['path'])
                    and w['value'].get('kind') in ('actual_sender','parameter')]
    if not address_writes:return None
    guarded=[]
    for use in sorted(entries-{root}):
        if inv.f.operations[use]['target']!=target or inv.f.operations[use].get('generated_getter'):continue
        if not inv.f.operations[use]['paths']:return None
        for pid,p in inv.f.operation_paths(use,True):
            if any(n.get('kind') in ('unknown','external_return') for n in walk(p['guards'])):return None
            gates=[]
            for g in p['guards']:
                for term in walk(g):
                    if term.get('op')=='==' and any(a.get('kind')=='actual_sender' for a in term.get('args',[])):
                        gates.extend(c for c in selectors(term) if value_type(c,lookup) in ('address','address payable') and not keys(c))
            if gates:guarded.append({'operation':use,'path':pid,'gates':gates})
    if not guarded:return None
    # Check all committed data/control flow to the requested qualification,
    # including helper-expanded operations. A missing/opaque connection stays open.
    rw=runtime_writers(inv.f,target)
    if rw['opaque_storage_writes'] or rw['unresolved_calls']:return None
    gates_needed={s['root'] for row in guarded for s in row['gates']}
    influenced={w['path']['root'] for w in writes}
    changed=True
    while changed:
        changed=False
        for oid,o in inv.f.operations.items():
            if o['target']!=target:continue
            for _,p in inv.f.operation_paths(oid):
                relevant=any(s['root'] in influenced for s in selectors([p['guards'],[w['value'] for w in p['writes']]]))
                if not relevant:continue
                if (p.get('issues') or p.get('evaluation_gaps')) and any(w['path']['root'] in gates_needed for w in p['writes']):return None
                if p['flow'] not in ('normal','returned'):continue
                for w in p['writes']:
                    if w['path']['root'] not in influenced:influenced.add(w['path']['root']);changed=True
    gates={s['root'] for row in guarded for s in row['gates']}
    if gates&influenced:return None
    return {'status':'refuted','necessary_premise':'the cited public write changes the authority read by the cited protected effect',
        'reason':'different_storage_declarations_and_no_committed_data_or_control_flow',
        'target':target,'change':root,'written_authority_cells':[w['path'] for w in address_writes],
        'protected_effects':guarded,'reachable_write_closure':sorted(influenced),
        'retained_fact':'the separate source field can change; independent entry risks are unchanged',
        'whole_contract_safety':False,'business_policy_invented':False}

~~~~

## source/src/pr_next_joint/investigation/authorization_normal.py

~~~~python
"""Source relations for narrow, reviewable normal authorization alternatives.

The model proposes the business interpretation. These builders require the
corresponding source operands; they never equate an arbitrary guard with policy.
"""
import re
from pr_next_joint.frontend.path_ir import key, op, walk
from pr_next_joint.frontend.storage import keys, selector_relation, value_type
from .summary import unique, directions


def numeric_delegations(inv, root, subject, explanation=None):
    """Bind both amount versions. Source comparison alone cannot establish consent."""
    f=inv.f;target=f.operations[root]['target'];lookup=f.lookup(root);found=[]
    from .summary import debited_positions
    for row in f.summaries.rows(root):
        for effect in debited_positions(f,root):
            if effect['path']!=row['path'] or key(effect['holder'])!=key(subject):continue
            amount=effect['amount']
            from pr_next_joint.frontend.storage import selectors
            for cell in selectors(row['guards']):
                idx=keys(cell)
                from .key_roles import relation
                role=relation(cell,lookup)
                if not role or role['kind']!='authorization_quantity':continue
                h=role['holder_key']
                if len(idx)!=2 or key(idx[h])!=key(subject) or idx[1-h].get('kind')!='actual_sender':continue
                if not re.fullmatch(r'u?int\d*',value_type(cell,lookup) or ''):continue
                writers=[w for w in f.writes.values() if f.operations[w['operation']]['target']==target and
                    selector_relation(w['raw']['path'],cell)=='same_shape']
                grants=[];bad=False
                for w in writers:
                    dst=w['raw']['path'];v=w['raw']['value']
                    if 'credit' not in directions(dst,v):continue
                    ks=keys(dst);p=f.paths[w['path']]['raw']
                    if (len(ks)!=2 or ks[h].get('kind')!='actual_sender' or ks[1-h].get('kind')!='parameter' or
                         any(c['mode']=='DELEGATECALL' and c['unresolved_implementation'] for c in f.call_summaries.rows.values()
                             if f.operations[c['operation']]['target']==target)):
                        # Ordinary CALL cannot change msg.sender of this
                        # source assignment. Its exit/return uncertainty is
                        # separate from the immutable issuer/key invariant.
                        bad=True;break
                    grants.append({'operation':w['operation'],'path':w['path'],'source':w['raw']['source']})
                from .initial_state import initial_for_lookup
                initial=initial_for_lookup(lookup) or {}
                for cp in initial.get('constructor_paths',[]):
                    if cp.get('issues') or cp.get('evaluation_gaps'):bad=True;break
                    for w in cp['writes']:
                        if selector_relation(w['path'],cell)!='same_shape' or w['value'].get('value') in (0,False):continue
                        kk=keys(w['path'])
                        if len(kk)!=2 or kk[h].get('kind')!='actual_sender':bad=True;break
                if grants and not bad:
                    amounts={key(v['consumed_amount']):v['consumed_amount'] for v in role['origins']
                             if v['path']==row['path'] and key(v['asset'])==key(effect['cell'])}
                    if len(amounts)!=1:continue
                    consumed=next(iter(amounts.values()))
                    basis='same_quantity'
                    if key(amount)!=key(consumed):
                        text=(explanation or {}).get('text') or (explanation or {}).get('basis','')
                        # Only accept a definite amount-specific policy statement.
                        gross=re.search(r'\b(?:allowance|consent|approval) (?:must|should|is required to) cover (?:the )?(?:gross|full debit)',text,re.I)
                        net=re.search(r'\b(?:holder|issuer) explicitly authori[sz]es (?:the )?(?:fee|fees).{0,48}\bnet (?:allowance|amount)',text,re.I)
                        if bool(gross)==bool(net):continue
                        basis='gross' if gross else 'net_with_explicit_fee_consent'
                    expected=consumed if basis=='net_with_explicit_fee_consent' else amount
                    found.append({'predicate':op('>=',cell,expected),'holder':subject,'allowance':cell,
                        'actual_debit':amount,'actual_allowance_consumption':consumed,'policy_basis':basis,
                        'grant_sources':grants,'use_path':row['path'],'kind':'holder_issued_quantity_for_scoped_amount'})
    return unique(found)


def payment_qualification(inv,q,subject,require_proposal=True):
    """Paid acquisition of a scalar authority, explicitly proposed as lawful.

Supported relation: the new holder is the payer, the stored bid equals the
actual payment, and payment exceeds the previous bid. A payment alone is not
authorization. Other business policies remain unresolved.
"""
    item=q['current'];proposal=q.get('authorization_interpretation') or {}
    text=' '.join(str(item.get(k) or '') for k in ('claim','normal_basis','revision_reason','alternative'))+' '+str(proposal.get('basis',''))
    if require_proposal:
        if item.get('assessment')!='normal' and proposal.get('meaning')!='normal_authorization':return []
        if not re.search(r'\b(?:lawful|legitimate|valid|normal)\b.{0,45}\b(?:auction|bid|paid acquisition|business qualification)\b|合法.{0,15}(?:竞价|拍卖)',text,re.I):return []
    if keys(subject):return []
    root=inv.root(q);lookup=inv.f.lookup(root);found=[]
    for pid,path in inv.f.operation_paths(root,True):
        if path.get('issues') or path.get('evaluation_gaps'):continue
        owner_write=any(key(w['path'])==key(subject) and w['value'].get('kind')=='actual_sender' for w in path['writes'])
        if not owner_write:continue
        payment_writes=[w for w in path['writes'] if not keys(w['path']) and
            re.fullmatch(r'u?int\d*',value_type(w['path'],lookup) or '') and
            w['value'].get('kind')=='transaction_value']
        for w in payment_writes:
            for guard in path['guards']:
                # Do not flatten an OR: the comparison must be necessary for
                # this committing path, not a permissive alternative.
                def conjuncts(g):
                    return [x for a in g['args'] for x in conjuncts(a)] if g.get('op') in ('and','&&') else [g]
                for term in conjuncts(guard):
                    a=term.get('args',[])
                    if len(a)!=2:continue
                    payment,bid=(a[0],a[1]) if term.get('op')=='>' else (a[1],a[0]) if term.get('op')=='<' else ({},{})
                    if payment.get('kind')=='transaction_value' and key(bid)==key(w['path']):
                        found.append({'predicate':op('>',payment,bid),'kind':'paid_bid_acquires_same_authority',
                            'holder':subject,'payer':{'kind':'actual_sender'},'payment':payment,'bid':bid,
                            'path':pid,'source':w['source'],'business_basis':text})
    return unique(found)

~~~~
