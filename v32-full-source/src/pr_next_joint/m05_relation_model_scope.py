"""Consume explicit M2 relation locations against the selected source model.

This is a pre-formula selection gate, not a new policy or solver. Description
strings remain explanations. A location match grants no state/key equality.
"""
import copy
import re
from .core import digest
from .m03_p_paths import key,walk
from .m04_logic import Unsupported


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
            from .source_entry_identity import builtin_object
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
            from .source_entry_identity import builtin_call
            if builtin_call(n,lookup) and n.get('arguments'):
                return lower(n['arguments'][0])
        if kind in ('BinaryOperation','UnaryOperation'):
            nodes=[n.get('subExpression',{})] if kind=='UnaryOperation' else [n.get('leftExpression',{}),n.get('rightExpression',{})]
            args=[lower(a) for a in nodes];operator=n.get('operator')
            if all(a is not None for a in args) and operator in ('!','&&','||','==','!=','<','<=','>','>=','+','-','&','|'):
                from .m03_p_paths import normalize
                return normalize({'kind':'op','op':operator,'args':args})
        if kind=='IfStatement':
            condition=lower(n.get('condition',{}))
            if condition is None:return None
            true=n.get('trueBody',{});false=n.get('falseBody')
            def bare_revert(branch):
                statements=branch.get('statements',[]) if branch.get('nodeType')=='Block' else [branch]
                if len(statements)!=1:return False
                x=statements[0];call=x.get('expression',{}) if x.get('nodeType')=='ExpressionStatement' else x
                from .source_entry_identity import builtin_call
                return x.get('nodeType')=='RevertStatement' or builtin_call(call,lookup,('revert',))
            from .m03_p_paths import normalize,op
            if bare_revert(true) and not false:return normalize(op('!',condition))
            if false and bare_revert(false):return condition
        return None
    if node.get('nodeType') in ('FunctionCall','RevertStatement'):
        from .source_entry_identity import builtin_call
        if node.get('nodeType')=='RevertStatement' or builtin_call(node,lookup,('revert',)):
            operation=[fn]
            for modifier in fn.get('modifiers',[]):operation.append(lookup.nodes.get(modifier.get('modifierName',{}).get('referencedDeclaration'),{}))
            candidates=[n for n in walk(operation) if n.get('nodeType')=='IfStatement' and any(v.get('id')==node.get('id') for v in walk(n))]
            candidates.sort(key=lambda n:len(list(walk(n))))
            for ancestor in candidates:
                value=lower(ancestor)
                if value is not None:return value
    return lower(node)


def outer_selectors(value):
    if isinstance(value,dict):
        if value.get('kind')=='storage':return [value]
        return [s for child in value.values() for s in outer_selectors(child)]
    if isinstance(value,list):return [s for child in value for s in outer_selectors(child)]
    return []

def check_slot(obligation,lookup,slot,values,writes=(),source_ids=(),substitution=None,question_refs=None,selected_functions=()):
    binding=obligation.get('relation_binding') or {}
    raw=(obligation.get('original_proposal') or {}).get('mechanism',{}).get(slot)
    if not binding:
        # Older callers may omit the IR; explicit references must not disappear.
        explicit=any(any(k.endswith('_ast_id') or k.endswith('_ast_ids') or k in ('ref','expression_ref','source_quote','source_range','src') for k in n) for n in walk(raw))
        if explicit:raise Unsupported('relation_scope_IR_missing:'+slot)
        return {'slot':slot,'status':'no_explicit_reference','evidence':[]}
    if binding.get('identity')!=obligation.get('identity') or binding.get('target')!=obligation['target'] or binding.get('function')!=obligation['function']:
        raise Unsupported('relation_scope_identity_mismatch')
    records=[r for r in binding.get('slots',{}).get(slot,[]) if r.get('status')!='explanation_only']
    deferred=[]
    if slot=='credential' and question_refs is not None:
        from .m05_question_trace import question_id
        credential=(obligation.get('original_proposal') or {}).get('mechanism',{}).get('credential',{})
        declared=credential.get('validity_relations',[]) if isinstance(credential,dict) else []
        retained=[]
        for record in records:
            match=re.match(r'mechanism/credential/validity_relations/(\d+)(?:/|$)',record.get('reference_path',''))
            if match and int(match[1])<len(declared):
                index=int(match[1]);qid=question_id(obligation,'credential.validity_relations',index,declared[index])
                if qid not in question_refs:
                    deferred.append({'question_id':qid,'reference_path':record['reference_path'],'reason':'independent_question_not_part_of_this_model'});continue
            retained.append(record)
        records=retained
    nodes=list(walk(values));terms={key(n) for n in nodes if n.get('kind')}
    selectors=[n for n in nodes if n.get('kind')=='storage']
    if slot=='resources':
        primary=values if isinstance(values,list) else [values]
        selectors=[n for n in primary if isinstance(n,dict) and n.get('kind')=='storage']
        terms={key(n) for n in selectors}
    ids=set(source_ids)
    for n in nodes:
        if type(n.get('source',{}).get('ast_id'))is int:ids.add(n['source']['ast_id'])
        if type(n.get('ast_id'))is int:ids.add(n['ast_id'])
    function_nodes={fn:{n.get('id') for n in walk(lookup.function(fn) or {})} for fn in [obligation['function']]+sorted(set(selected_functions)-{obligation['function']})}
    local=function_nodes[obligation['function']]
    modifiers=set();modifier_origin={}
    for fn in function_nodes:
        for modifier in (lookup.function(fn) or {}).get('modifiers',[]):
            decl=lookup.nodes.get(modifier.get('modifierName',{}).get('referencedDeclaration'),{})
            modifiers.update(n.get('id') for n in walk(decl))
            for n in walk(decl):modifier_origin.setdefault(n.get('id'),fn)
    allowed=set(binding.get('bound_source_ids',[]))
    def instance_term(term):
        if substitution:
            from .m05_mechanism_core import remap,retime
            term=remap(term,substitution.get('parameters',{}),substitution.get('sender'))
            if substitution.get('time'):term=retime(term,substitution['time'])
        return term
    evidence=[]
    for record in records:
        if record.get('status') not in ('source_bound','term_bound'):raise Unsupported('relation_scope_unresolved:'+slot+':'+str(record.get('reference_path')))
        matched=None
        if record.get('status')=='term_bound':
            if key(instance_term(record['term'])) in terms:matched='exact_registered_term'
        else:
            reference_ids=record.get('source_ast_ids',[])
            precise=[aid for aid in reference_ids if lookup.nodes.get(aid,{}).get('nodeType') in ('IndexAccess','IndexRangeAccess','MemberAccess','Assignment','UnaryOperation','ExpressionStatement')]
            def match_id(aid):
                node=lookup.nodes.get(aid,{})
                if aid in ids:return 'exact_selected_model_source'
                if node.get('nodeType')=='VariableDeclaration' and node.get('stateVariable') and any(s['root']==aid and not s.get('instance') for s in selectors):
                    return 'declared_local_root_scope'
                origin=next((fn for fn,ids_ in function_nodes.items() if aid in ids_),modifier_origin.get(aid))
                term=source_term(node,lookup,origin) if origin is not None and aid in allowed else None
                if term is not None and origin==obligation['function']:term=instance_term(term)
                if term is not None and key(term) in terms:return 'exact_operation_term'
                if term is not None and slot in ('control','participants','consent'):
                    from .m03_p_paths import normalize,op
                    if key(normalize(op('!',term))) in terms:return 'same_selected_branch_predicate_opposite_source_polarity'
                # A statement wrapper denotes the same mutation only within
                # this operation. Helper calls require an instantiated term.
                from .m05_relation_consumers import _write_syntax
                mutation,lvalue=_write_syntax(node)
                if mutation and aid in local and any(w.get('source',{}).get('ast_id')==mutation.get('id') and not w.get('path',{}).get('instance') for w in writes):
                    return 'same_local_mutation'
                return None
            groups={}
            for aid in precise or reference_ids:
                node=lookup.nodes.get(aid,{})
                # Multiple compiler wrappers at one byte span are aliases;
                # distinct cited occurrences are separate obligations.
                groups.setdefault(node.get('src') or ('ast',aid),[]).append(aid)
            matches=[next((value for aid in aids if (value:=match_id(aid)) is not None),None) for aids in groups.values()]
            if matches and all(matches):matched=matches
        if matched is None:raise Unsupported('relation_scope_not_consumed:'+slot+':'+str(record.get('reference_path')))
        evidence.append({'reference_path':record.get('reference_path'),'binding':matched,'reference_sha256':digest(record),'usage':'selected source evidence; semantic predicates reconstructed independently'})
    return {'slot':slot,'status':'selected_model_bound' if records else 'no_explicit_reference','evidence':evidence,'deferred_independent_questions':deferred,'selected_values_sha256':digest(values),'grants_semantic_equivalence':False}


def constrain_model(obligation,lookup,model):
    """Called before any formula/solver; all model variants share this gate."""
    rule=obligation['rule'];kind=model['kind']
    if rule in ('FCR-TRANSFER','FCR-DESTROY'):
        debit=model['debit']['write'];credit=(model.get('credit') or {}).get('write')
        writes=model['writes']
        resources=outer_selectors([model['guards'],writes,model['consent'],model['consent_sources']])
        from .m05_equity_relations import linear_quantity
        quantity=linear_quantity(model['amount'])
        roles={'resources':resources,'participants':[debit['path'],credit['path'] if credit else None,model['privilege']],
               'consent':[model['consent'],model['consent_sources'],model['guards'],model['privilege']],'credential':model['consent_sources'],
               'control':[model['privilege'],model['guards']], 'amount':[quantity]}
    elif rule in ('FCR-PAUSE','FCR-FREEZE'):
        request=model['transfer_request'];writes=[request['debit'],request['credit']]+model['writes']
        roles={'resources':outer_selectors([model['pre_action'],model['normal_baseline'],model['control'],writes]),
               'control':[model['control'],model['pre_action'],model['post_action'],model['transition_guards']],
               'participants':[model['holder'],model['recipient'],model['control'],model['privilege']],
               'consent':model['normal_baseline'],'credential':model['normal_baseline'],'amount':[model['amount']]}
    elif rule=='AC-05':
        effect=model.get('effect');writes=[effect] if isinstance(effect,dict) else []
        roles={'resources':effect.get('path') if isinstance(effect,dict) else None,'participants':[effect.get('path') if isinstance(effect,dict) else None,model.get('credential'),model.get('recovered_signers'),model.get('conditions')],
               'credential':[model.get('credential'),model.get('recovered_signers'),model.get('validity_relation_origin'),model.get('deadline'),model.get('validity_before'),effect],
               'consent':model.get('conditions'),'control':model.get('conditions')}
    else:raise Unsupported('relation_scope_rule_not_supported')
    if obligation.get('relation_binding',{}).get('slots',{}).get('amount') and 'amount' not in roles:
        raise Unsupported('explicit_amount_not_supported_by_selected_model')
    selected_functions={obligation['function'],model.get('function'),model.get('action'),model.get('transition')}
    asset=model.get('asset') or model.get('model') or {}
    selected_functions.add(asset.get('transfer_function'));selected_functions.discard(None)
    selected_source_ids={w.get('source',{}).get('ast_id') for w in writes}
    selected_source_ids.update((lookup.function(fn) or {}).get('id') for fn in selected_functions)
    selected_source_ids.discard(None)
    receipts=[]
    for slot,values in roles.items():
        slot_writes=writes
        receipts.append(check_slot(obligation,lookup,slot,values,slot_writes,
            list(selected_source_ids-{None}),
            model.get('relation_operation_substitution'),model.get('question_refs',[]) if rule=='AC-05' else None,selected_functions))
    model['relation_scope_consumption']={'phase':'selected_before_formula','source_binding_sha256':digest(obligation.get('relation_binding',{})),
        'slots':receipts,'operation_substitution':copy.deepcopy(model.get('relation_operation_substitution')),
        'scope':'exact selected source model; no inferred actor/key/instance equivalence'}
    return model
