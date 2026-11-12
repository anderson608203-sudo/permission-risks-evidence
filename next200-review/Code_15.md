# 源码文本 · 15

## source/src/pr_next_joint/investigation/report.py

原文件 SHA-256 `70bc89f219fc78915f687f7c60da17efe950751c39842779ec14ef30a4c2a11f`

````python
"""Source-backed risk prediction, scoped hard counterevidence and dependency output."""
import copy,re
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import walk,key
from pr_next_joint.frontend.storage import selectors,keys,value_type,selector_relation
from .contracts import VERSION,CATEGORIES
from .protocol import category_scope
from .request_scope import coverage_facts, observation_applies, compare_relevant, linked_controls



def evaluate(inv,q):
    from .property_model import planning_item,compose
    inv.semantics.scope(q['current'])
    return compose(inv,q,None)

def reading_scope(inv,blocked,assessments=None):
    from .coverage import obligation_scope
    assessments=assessments or {qid:evaluate(inv,q) for qid,q in inv.issues.items()}
    return obligation_scope(inv,assessments,blocked)



def build(inv):
    findings={};records=[];suppressed=[];decisive_records=[];blocked_categories=set();assessments={}
    for qid,q in sorted(inv.issues.items()):
        assessment=evaluate(inv,q);assessments[qid]=assessment;item=q['current'];records.append({'id':qid,'version':q['version'],
            'current':copy.deepcopy(item),'history':copy.deepcopy(q['history']),'binding':q['binding'],
            'distinguishing_plan':copy.deepcopy(q.get('plan')),'claim_source_scope':copy.deepcopy(q['claim_source_scope']),
            'task_conflict':q.get('task_conflict',False),'semantic_task_review':copy.deepcopy(q.get('task_review')),
            'compiled_property':copy.deepcopy(q.get('property')),'semantic_answers':copy.deepcopy(q.get('semantic_answers',[])),
            'assessment_result':assessment,'evidence_refs':q['evidence'],'revision_evidence':q['revision_evidence'],
            'scoped_observations':copy.deepcopy(q.get('observations',[])),
            'source_observation_reuse':copy.deepcopy(q.get('source_decisions',[]))})
        unknown={'source_identity_ambiguous_or_unresolved','minimum_source_inspection_not_executed',
           'unique_critical_external_guard_not_established','signature_dependent_success_not_verified',
            'E1_cumulative_numeric_bound_mapping_pending','semantic_task_direction_conflict','financial_intervention_source_unresolved',
            'property_task_meaning_unresolved','expected_authorization_not_established','financial_property_conditions_not_established',
            'changed_business_effect_requires_source_rebinding','normal_authorization_source_scope_unresolved'}
        hard={'original_root_has_no_committing_path','original_root_net_effect_is_unchanged',
              'same_scope_actual_full_settlement','single_holder_scope_not_collective_pause','same_control_has_no_dependency_on_declared_entry_effect',
              'matched_direct_effect_impossible_on_all_applicable_positions_and_paths'}
        if set(assessment['reasons'])&unknown and assessment['category'] in CATEGORIES:blocked_categories.add(assessment['category'])
        decisive=(assessment['reportable'] or
                  bool(set(assessment['reasons'])&hard) and not set(assessment['reasons'])&unknown)
        if decisive and not q.get('task_conflict'):decisive_records.append(qid)
        mapping=assessment['scope'].get('comparison_alignment',{})
        if mapping.get('status')=='unresolved' and item['assessment']=='risk' and assessment['category'] in CATEGORIES:blocked_categories.add(assessment['category'])
        if not assessment['reportable']:
            if item['assessment']=='risk':suppressed.append({'issue':qid,'reasons':assessment['reasons']})
            continue
        oid=assessment['root'];o=inv.f.operations[oid]
        location=copy.deepcopy(o['source']);anchor=q['binding'].get('core_anchor') or inv.catalog.name(oid);fine=False
        if anchor in inv.catalog.label_locations:location=copy.deepcopy(inv.catalog.label_locations[anchor]);fine=True
        else:
            m=re.fullmatch(r'(.+\.sol):(\d+)(?:[-:](\d+))?',anchor)
            if m and m[1] in inv.catalog.sources:
                chunks=inv.catalog.sources[m[1]]['content'].encode().splitlines(keepends=True);lo=int(m[2]);hi=int(m[3] or lo)
                start=sum(map(len,chunks[:lo-1]));end=sum(map(len,chunks[:hi]));location={'file':m[1],'start':start,'length':end-start};fine=True
        # Conservative source-root grouping. Do not equate different unlocated
        # business mechanisms merely because they share a variable/function.
        identity=[inv.f.identity,assessment['category'],o['target'],location,assessment['scope'].get('claim_identity'),item.get('object'),item.get('actor'),
                  item.get('phase'),item.get('scope'),item.get('assumptions'),None if fine else ' '.join(item['claim'].split())]
        fid='finding_'+digest(identity)[:20]
        f=findings.setdefault(fid,{'id':fid,'category':assessment['category'],'target':o['target'],
            'root_location':location,'root_cause':{'operation':oid,'source_anchors':[location]},
            'operation':oid,'function':o['function'],'related_operations':q['binding']['operations'],
            'actor':item.get('actor'),'object':item.get('object'),'mechanism':assessment.get('composed_claim',item['claim']),
            'original_model_claim':item['claim'],'original_model_assessment':item['assessment'],
            'normal_explanation_considered':item.get('alternative'),'scope':assessment['scope'],
            'assumptions':item.get('assumptions',[]),'evidence_level':assessment.get('evidence_level','source_prediction'),
            'comparison_scope':mapping.get('status','main'),'formal_risk_query_required':False,'evidence_refs':[],'issue_ids':[]})
        f['evidence_refs']=sorted(set(f['evidence_refs']+q['evidence']));f['issue_ids'].append(qid)
    scope=reading_scope(inv,blocked_categories,assessments)
    blocked_categories={c for gap in scope['known_category_gaps'] for c in gap.get('affected_categories',[])}
    return {'method':VERSION,'program_identity':inv.f.identity,'task':inv.f.options.scope,'options':inv.f.options.record(),
        'implementation_sha256':inv.f.context['implementation_sha256'],
        'findings':list(findings.values()),'main_finding_ids':[k for k,v in findings.items() if v['comparison_scope']=='main'],
        'additional_finding_ids':[k for k,v in findings.items() if v['comparison_scope']=='additional'],
        'unresolved_mapping_ids':[k for k,v in findings.items() if v['comparison_scope']=='unresolved'],'inspection_records':records,
        'diagnostics':{'issues':inv.diagnostics,'unexecuted_actions':copy.deepcopy(inv.ready),
            'suppressed_source_predictions':suppressed,'program_gaps':copy.deepcopy(inv.f.gaps),
            'source_context_scope':inv.initial_manifest,'no_finding_is_not_contract_safety':True,
            'E1_not_formal_FREEZE':True},
        'model_analysis_available':inv.model_analysis_available,
        'prediction_basis_available':bool(findings or scope['negative_eligible_categories'] or decisive_records),
        'prediction_basis_issues':decisive_records,'unresolved_category_judgments':sorted(blocked_categories),
        'task_analysis':{'model_analysis_available':inv.model_analysis_available,
            'empty_response_present':inv.explicit_empty_analysis,
            'explicit_empty_task_reading':bool(inv.explicit_empty_analysis and scope['whole_reading_eligible']),
            'model_declaration':inv.task_declaration,'reading_scope':scope,'local_judgment_not_global_safety':True,
            'unexecuted_actions':len(inv.ready),'task_conflicts':[qid for qid,q in inv.issues.items() if q.get('task_conflict')]},
        'model_reading_declarations_not_proof':inv.reading_declarations,
        'usage':{'attempts':copy.deepcopy(inv.session.attempts),**inv.session.accounting()},
        'provenance':{'source_candidate_investigations':copy.deepcopy(getattr(inv,'candidate_trace',[])),'actions':copy.deepcopy(inv.actions),'revisions':copy.deepcopy(inv.updates),
            'evidence_labels':sorted(inv.evidence),'feedback_trace':copy.deepcopy(inv.feedback_trace),'cache_hits':inv.backend.cache_hits,
            'computation_reuse':copy.deepcopy(inv.backend.cache_stats),'model_call_decisions':copy.deepcopy(inv.call_decisions),
            'mechanism_attribution_not_a_new_detection_admission_gate':True},
        'prediction_frozen_before_gold':True,'scoring_performed':False,
        'risk_absence_statement':'No risk detected in the actual analyzed source scope; not proof of safety.'}

def evaluation_projection(report):
    """No Gold access, scoring or legacy query gate. Preserve positive source predictions."""
    cats=('AC',) if report['task']=='AC' else CATEGORIES[1:]
    found={f['category'] for f in report['findings'] if f.get('comparison_scope','main')=='main'}
    unknown=set(report.get('unresolved_category_judgments',[]))
    task=report.get('task_analysis',{});reading=task.get('reading_scope',{})
    # Archived reports retain their original projection; new reports carry prospective eligibility.
    if 'reading_scope' in task:
        eligible=set(reading['negative_eligible_categories'])
    else:
        eligible=set()
        unknown.update(set(cats) - found)
    return {'predictions':{c:'alarm' if c in found else 'unsupported' if c in unknown else
         'not_detected' if c in eligible else 'not_run' for c in cats},
        'scope':report['diagnostics']['source_context_scope'],
        'coverage_basis':'Finite source obligations, actual semantic/program completion and scoped residuals; delivery/declarations are records, not completion gates.',
        'no_finding_does_not_prove_safety':True,'not_a_score':True,
        'enhancement_unfinished_does_not_erase_source_predictions':True}

````

## source/src/pr_next_joint/investigation/request_scope.py

原文件 SHA-256 `756330123ee084b1e802e36698d1936dbb089a348121df6485a73306cbc9f6c2`

````python
"""Bind an investigation to program uses named in the claim, separately from its finding anchor."""
import re

from pr_next_joint.frontend.path_ir import key, walk
from .roles import path_qualification
from pr_next_joint.frontend.storage import keys, selectors, selector_relation, value_type


def unique_cells(cells):
    return list({key(cell): cell for cell in cells}.values())


def use_reads(path):
    # A destination on the left of an assignment is not a read of its old value.
    values = [w['value'] for w in path['writes']]
    positions = [keys(w['path']) for w in path['writes']]
    return selectors([path['guards'], values, positions, path.get('sensitive_effects', []),
                      path.get('return_value'), path.get('evaluated_terms', [])])


def claim_entries(inv, binding, item):
    root = binding.get('core_operation')
    if not root:
        return set()
    operations = inv.f.operations
    target = operations[root]['target']
    applied = [[oid for oid in ids if operations[oid]['target']==target] for ids in binding['located'].values()]
    located = {ids[0] for ids in applied if len(ids)==1}
    wording = ' '.join(str(item.get(k, '')) for k in ('claim', 'distinguish', 'distinguishing_question'))
    tokens = set(re.findall(r'\b([A-Za-z_$][\w$]*)\s*\(', wording))
    by_name = {}
    for oid, op in operations.items():
        if op['target'] == target:
            by_name.setdefault(op['function'].split('(')[0], []).append(oid)
    # Use the already bound target. A bare overloaded name cannot nominate a use.
    located.update(ids[0] for name, ids in by_name.items() if name in tokens and len(ids) == 1)
    return {root} | {oid for oid in located if operations[oid]['target'] == target}


def holder_effect(inv, oid):
    # Shape of a possible effect, not a judgment that a mapping is a financial right.
    for _, path in inv.f.operation_paths(oid, True):
        if any(fx.get('kind') == 'native_transfer' for fx in path.get('sensitive_effects', [])):
            return True
        for w in path['writes']:
            cell = w['path']
            if keys(cell) and value_type(cell, inv.f.lookup(oid)).startswith(('uint','int')):
                return True
    return False


def linked_controls(inv, change, use):
    writes = [w['path'] for _, p in inv.f.operation_paths(change, True) for w in p['writes']]
    return [cell for cell in inv.graph.request_reads(use) if any(
        selector_relation(cell, w) == 'same_shape' and not inv.graph._disjoint_keys(cell, w) for w in writes)]


def request_target(inv, binding, item, plan, measure):
    """Resolve a claim endpoint before evaluating Boolean predictions on it."""
    root = binding['core_operation']
    claimed = claim_entries(inv, binding, item)
    request = item['observation']
    hint = item.get('next_check')
    hint = hint if isinstance(hint, dict) else {}
    at = request.get('at')
    after = request.get('after')
    target=inv.f.operations[root]['target']
    at_ids=[i for i in inv.catalog.resolve(at) if inv.f.operations[i]['target']==target] if at else []
    after_ids=[i for i in inv.catalog.resolve(after) if inv.f.operations[i]['target']==target] if after else []
    if at and (len(at_ids) != 1 or at_ids[0] not in claimed):
        return None, [], 'observation_entry_outside_or_ambiguous_in_claim'
    if after and (len(after_ids) != 1 or inv.f.operations[after_ids[0]]['target'] != inv.f.operations[root]['target']):
        return None, [], 'intervention_target_ambiguous_or_different'
    pairs = plan['selected_pairs'] + plan['deferred_pairs']
    downstream = list(dict.fromkeys(p['observe'] for p in pairs if p['change'] == root
                                     and p['observe'] != root and p['observe'] in claimed))
    # A financial effect must not silently become a setter's authorization guard.
    if inv.f.options.scope == 'FCR':
        downstream = [u for u in downstream if holder_effect(inv, u)]
    preferred = at_ids or (inv.catalog.resolve(hint.get('observe')) if hint.get('action') == 'compare' else [])
    if len(preferred) == 1 and preferred[0] in downstream:
        downstream.remove(preferred[0])
        downstream.insert(0, preferred[0])
    if at_ids and at_ids[0] != root and at_ids[0] not in downstream:
        return None, downstream, 'no_source_dependency_from_claim_to_requested_use'
    if at_ids == [root]:
        use = root
    elif downstream and (measure not in ('holder_grant','holder_net') or
                         after_ids == [root] or at_ids or not holder_effect(inv, root)):
        use = downstream[0]
    else:
        use = root
    if inv.f.options.scope == 'FCR' and measure in ('opens','blocks') and not holder_effect(inv, use):
        return None, downstream, 'no_claimed_holder_request; role_evidence_only'
    if use == root and measure in ('opens','blocks') and inv.f.options.scope == 'FCR':
        # No invented upstream administrator as a financial intervention.
        if not any(p['observe'] == root and p['change'] in claimed and p['change'] != root for p in pairs) and not after_ids:
            return None, downstream, 'no_identified_intervention_on_holder_request'
    return use, downstream, None


def select_controls(inv, use, candidates, request, item):
    candidates = unique_cells(candidates)
    name = request.get('control')
    if name:
        if not isinstance(name, str):
            return []
        return [c for c in candidates if name in (inv.backend._storage_name(use, c),
                    inv.f.lookup(use).nodes.get(c['root'], {}).get('name'))]
    # Preserve explicit ordered keys in natural-language claims, including this vs msg.sender.
    text = re.sub(r'\s*([.\[\]])\s*', r'\1', str(item.get('claim','')))
    indexed = [c for c in candidates if keys(c) and re.search(
        r'(?<![\w$])' + re.escape(inv.backend._storage_name(use,c)) + r'(?![\w$\[])', text)]
    return indexed or candidates


def compare_relevant(inv, q, evidence):
    root = inv.root(q)
    change, use = evidence.get('change'), evidence.get('observe')
    if not root or not change or not use:
        return False
    choice = q.get('plan', {}).get('observation_choice') or {}
    resolution = choice.get('request_resolution')
    if not resolution:
        if inv.f.options.scope == 'FCR' and use == root and not holder_effect(inv,root):
            # A legacy upstream qualifier is contextual only when a separately
            # sourced downstream holder request is the subject of this claim.
            if any(u != root and holder_effect(inv,u) and linked_controls(inv,root,u)
                   for u in claim_entries(inv,q['binding'],q['current'])):
                return False
        return True
    if resolution['use'] is None and inv.f.options.scope == 'FCR':
        hint=q['current'].get('next_check')
        claimed=use in claim_entries(inv,q['binding'],q['current'])
        scoped_probe=isinstance(hint,dict) and hint.get('action')=='compare' and inv.catalog.resolve(hint.get('change'))==[change] and inv.catalog.resolve(hint.get('observe'))==[use]
        return change==root and holder_effect(inv,use) and (claimed or scoped_probe and bool(linked_controls(inv,change,use)))
    selected=choice.get('selected')
    if selected and selected['measure'] in ('direct_effect','denied_qualified','missing_control','ledger_receipt','ledger_debit','ledger_grant'):
        return (evidence.get('observed_measure'),change,use)==(selected['measure'],selected['change'],selected['observe'])
    if resolution['use'] != root:
        return change == root and use == resolution['use']
    if inv.f.options.scope == 'FCR' and use != root:
        return False
    return True


def observation_applies(inv, q, result):
    pick = (q.get('plan', {}).get('observation_choice') or {}).get('selected')
    if not pick or pick['observe'] != result['observe'] or pick['change'] != result['change']:
        return False
    return (pick['measure'] == result['measure'] and pick['scope'] == result['scope']
            and pick['context'] == result.get('request_context', pick['context'])
            and pick.get('expectations') == result.get('expectations'))


def account_term(term, lookup):
    if term.get('kind') in ('actual_sender','transaction_origin'):
        return True
    return term.get('kind') == 'storage' and not term.get('segments') and value_type(term, lookup) in ('address','address payable')


def positive_caller_gate(node, lookup):
    if node.get('op') in ('and','&&'):
        return any(positive_caller_gate(v, lookup) for v in node.get('args', []))
    args = node.get('args', [])
    if node.get('op') == '!' and len(args) == 1 and args[0].get('op') == '!=':
        args = args[0]['args']
    elif node.get('op') != '==':
        return False
    return (len(args) == 2 and any(x.get('kind') == 'actual_sender' for x in args) and
            any(x.get('kind') == 'storage' and account_term(x, lookup) for x in args))


def privileged_intervention(inv, binding, item):
    """Scope an explicit mixed actor claim to a real guarded writer and dependent use."""
    if not binding.get('core_exact') or item.get('category') not in (
            'FCR-TRANSFER','FCR-MINT','FCR-DESTROY','FCR-PAUSE','FCR-FREEZE'):
        return []
    claimed = claim_entries(inv, binding, item)
    root = binding['core_operation']
    links = []
    for writer in sorted(claimed):
        paths = list(inv.f.operation_paths(writer, True))
        if not inv.backend.complete(writer) or not paths or not all(
                path_qualification(inv.f,writer,path) for _, path in paths):
            continue
        for use in sorted(claimed - {writer}):
            if root not in (writer,use) or not holder_effect(inv, use):
                continue
            controls = linked_controls(inv, writer, use)
            if controls:
                links.append({'change':writer,'use':use,'controls':controls,'status':'source_dependency_not_proof_of_harm'})
    return links


def opaque_paths(inv, oid):
    """An incomplete effect or actual external dependency cannot certify a local exclusion."""
    if inv.f.operations[oid].get('generated_getter'):
        return False
    if not inv.backend.complete(oid):
        return True
    for pid, path in inv.f.operation_paths(oid, True):
        deps = inv.backend.condition_dependencies(oid, pid, path)
        if deps['unknown_dependencies'] or deps['credential_dependencies']:
            return True
        if any(effect.get('kind') != 'native_transfer' for effect in path.get('sensitive_effects', [])):
            return True
    return False


def bounded_availability_scope(inv, q):
    """Limit an existing availability question only when the control changes admission alone."""
    item = q['current']
    if inv.f.options.scope != 'FCR' or item.get('category') != 'AC':
        return None
    obs = item.get('observation') or {}
    if not isinstance(obs,dict) or obs.get('measure') != 'blocks' or not q['binding'].get('core_exact'):
        return None
    if q['binding'].get('ambiguous') or q['binding'].get('unresolved'):
        return None
    root = inv.root(q)
    if opaque_paths(inv, root) or not any(inv.evidence[k].get('operation') == root
            and inv.evidence[k]['kind'] == 'source_inspection' for k in q['evidence']):
        return None
    cells = unique_cells(w['path'] for _,p in inv.f.operation_paths(root,True) for w in p['writes'])
    if len(cells) != 1 or value_type(cells[0],inv.f.lookup(root)) != 'bool':
        return None
    if any(p.get('sensitive_effects') for _,p in inv.f.operation_paths(root,True)):
        return None
    target = inv.f.operations[root]['target']
    claimed = claim_entries(inv, q['binding'], item)
    matched = []
    for use in sorted(inv.graph.access[(target,cells[0]['root'])]['readers'] - {root}):
        if inv.f.operations[use].get('generated_getter'):
            continue
        if opaque_paths(inv,use):
            return None
        paths = list(inv.f.operation_paths(use,True))
        if not any(s['root']==cells[0]['root'] for _,path in paths for s in use_reads(path)):
            continue
        if use not in claimed or not paths:
            return None
        shapes = set()
        for _,path in paths:
            outputs = [path['writes'],path.get('sensitive_effects',[]),path.get('return_value')]
            if any(s['root']==cells[0]['root'] for s in selectors(outputs)):
                return None
            if not any(s['root']==cells[0]['root'] for s in selectors(path['guards'])):
                return None
            # Only ordinary use of the caller's own right, not a transfer/mint on another's behalf.
            if not any(w['value'].get('op')=='-' and key(w['value']['args'][0])==key(w['path'])
                       and (inv.backend._holder(use,w['path']) or {}).get('kind')=='actual_sender'
                       for w in path['writes']):
                return None
            shapes.add(key(outputs))
        if len(shapes)!=1:
            return None
        matched.append(use)
    if matched:
        return {'reason':'bounded_holder_availability_question','effect_entries':matched,
                'control':cells[0],'affected_categories':['FCR-PAUSE','FCR-FREEZE'],
                'limits':'only this pending blocking observation; no finding or whole-task conclusion'}
    return None


def coverage_facts(inv, q):
    if inv.f.options.scope != 'FCR' or not q.get('task_conflict'):
        return None
    token = (q['version'], tuple(q['evidence']))
    cached = q.get('_coverage_facts')
    if cached and cached[0] == token:
        return cached[1]
    try:
        result = local_task_scope(inv,q) or bounded_availability_scope(inv,q)
        if result is None and explicit_outside_scope(inv,q):
            result = {'reason':'recorded_explicit_non_task_clue','affected_categories':[],
                      'effect_entries':sorted(claim_entries(inv,q['binding'],q['current'])),
                      'limits':'source bounded, independent findings preserved'}
    except (KeyError,ValueError,TypeError,IndexError,NotImplementedError,TimeoutError) as error:
        inv.diagnostics.append({'issue':q['id'],'reason':'coverage_scope_unestablished',
                                'details':str(error),'no_new_negative':True})
        result = None
    q['_coverage_facts'] = token,result
    return result


def explicit_outside_scope(inv, q):
    if q.get('task_review',{}).get('status') != 'explicit_out_of_task_clue':
        return False
    binding = q['binding']
    if not binding.get('core_exact') or binding.get('ambiguous') or binding.get('unresolved'):
        return False
    entries = claim_entries(inv,binding,q['current'])
    for oid in entries:
        if opaque_paths(inv,oid):
            return False
        for _,path in inv.f.operation_paths(oid,True):
            for w in path['writes']:
                readers = inv.graph.access[(inv.f.operations[oid]['target'],w['path']['root'])]['readers']
                if any(opaque_paths(inv,u) for u in readers):
                    return False
    return True


def local_task_scope(inv, q):
    """A local certificate for an explicitly non-financial clue, never a whole-task negative."""
    item, binding = q['current'], q['binding']
    if inv.f.options.scope != 'FCR' or item.get('category') != 'AC' or not binding.get('core_exact'):
        return None
    if binding.get('ambiguous') or binding.get('unresolved'):
        return None
    root = binding['core_operation']
    entries = claim_entries(inv, binding, item)
    lookup = inv.f.lookup(root)
    # A local, scoped normal conclusion requires actual accepted source inspection.
    inspected = {inv.evidence[e].get('operation') for e in q['evidence']
                 if inv.evidence[e]['kind'] == 'source_inspection' and not inv.evidence[e].get('local_errors')}
    if root not in inspected or not entries:
        return None
    pure_event = True
    role_writes = set()
    role_readers = set()
    for oid in entries:
        declaration = lookup.nodes.get(inv.f.operations[oid]['source'].get('ast_id'), {})
        if (oid != root and declaration.get('nodeType') == 'VariableDeclaration'
                and declaration.get('stateVariable') and declaration.get('visibility') == 'public'
                and declaration.get('typeDescriptions', {}).get('typeString') in ('address','address payable')):
            continue  # compiler-generated read-only identity accessor, not an unexamined action
        if not inv.backend.complete(oid):
            return None
        commits = list(inv.f.operation_paths(oid, True))
        if not commits:
            return None
        for pid, path in commits:
            audit = inv.backend.condition_dependencies(oid, pid, path)
            if (path.get('sensitive_effects') or audit['unknown_dependencies'] or audit['credential_dependencies']
                    or path.get('return_value') is not None and not account_term(path['return_value'], lookup)):
                return None
            if path['writes']:
                pure_event = False
                if item.get('assessment') != 'normal' or not path_qualification(inv.f,oid,path):
                    return None
            for w in path['writes']:
                dest, val = w['path'], w['value']
                if not account_term(dest, lookup) or not (account_term(val, lookup) or val.get('kind') in ('parameter','literal')):
                    return None
                role_writes.add(dest['root'])
                role_readers.update(s['root'] for g in path['guards'] for s in selectors(g))
        # payable entry or opaque effects cannot be certified event/role-only.
        if lookup.function(inv.f.operations[oid]['function']).get('stateMutability') == 'payable':
            return None
    if pure_event:
        for oid in entries:
            fn = lookup.function(inv.f.operations[oid]['function'])
            body = fn.get('body') or {}
            if fn.get('modifiers') or not body.get('statements') or any(
                    n.get('nodeType') != 'EmitStatement' for n in body['statements']):
                return None
            # A helper called by another entry can affect an enclosing transaction.
            if any(n.get('nodeType') == 'FunctionCall' and
                   n.get('expression',{}).get('referencedDeclaration') == fn.get('id')
                   for other, op in inv.f.operations.items() if other != oid and op['target'] == inv.f.operations[oid]['target']
                   for n in walk(lookup.function(op['function']))):
                return None
    else:
        # An address-valued setter can also select the recipient of a payout or an external
        # implementation. Only role positions used solely for authorization/role updates qualify.
        for cell in role_writes:
            for use in inv.graph.access[(inv.f.operations[root]['target'], cell)]['readers']:
                if not inv.backend.complete(use):
                    return None
                for _, path in inv.f.operation_paths(use, True):
                    returned = path.get('return_value')
                    plain_getter = not path['writes'] and returned and account_term(returned, lookup)
                    payload = [path.get('sensitive_effects', []), None if plain_getter else returned,
                               [keys(w['path']) for w in path['writes']],
                               [w['value'] for w in path['writes'] if not (use in entries and account_term(w['path'], lookup))]]
                    if any(s['root'] == cell for s in selectors(payload)):
                        return None
                    for guard in path['guards']:
                        if any(s['root'] == cell for s in selectors(guard)) and not positive_caller_gate(guard, lookup):
                            # Nonzero/nominee inequality on the local handover itself is harmless.
                            if use not in entries:
                                return None
        for cell in role_writes:
            writers = inv.graph.access[(inv.f.operations[root]['target'], cell)]['writers']
            if not writers <= entries:
                return None
        if not role_writes & role_readers:
            return None
    return {'reason':'source_local_event' if pure_event else 'source_local_normal_authority',
            'effect_entries':sorted(entries), 'affected_categories':[],
            'limits':'only this issue; external/asset dependencies and other issues assessed independently'}


````

## source/src/pr_next_joint/investigation/roles.py

原文件 SHA-256 `cf7b6d13d1a403a99789140156ab9e3b1694fce42de48a37f1a66e3d229cf169`

````python
"""Source-grounded qualifications for a specific compiled target and committing path."""
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys,selectors


def _roots(node, allowed, positive=True):
    """Return role declarations required by the condition; all arms of a disjunction must qualify."""
    args, op = node.get('args', []), node.get('op')
    if op == '!' and len(args) == 1:
        return _roots(args[0], allowed, not positive)
    if op in ('and', '&&', 'or', '||') and len(args) == 2:
        left, right = (_roots(x, allowed, positive) for x in args)
        conjunction = (op in ('and', '&&')) == positive
        return (left | right) if conjunction or (left and right) else set()
    if op in ('==', '!=') and len(args) == 2:
        equality = (op == '==') == positive
        for side, other in (args, args[::-1]):
            if other.get('kind') == 'literal' and type(other.get('value')) is bool:
                return _roots(side, allowed, equality == other['value'])
            if equality and other.get('kind') == 'actual_sender' and side.get('kind') == 'storage':
                rid = side['root']
                if not side.get('segments') and not side.get('instance') and rid in allowed:
                    return {rid}
    if positive and node.get('kind') == 'storage' and not node.get('instance') and node['root'] in allowed:
        idx = keys(node)
        if len(node.get('segments', [])) == len(idx) == 1 and idx[0].get('kind') == 'actual_sender':
            return {node['root']}
    return set()


def _seed_address(node, parameters):
    if not node:return None
    if node.get('memberName') == 'sender' and node.get('expression', {}).get('name') == 'msg':
        return {'term':'deployer'}
    if node.get('referencedDeclaration') in parameters:
        return {'term':'constructor_parameter','id':node['referencedDeclaration']}
    if node.get('nodeType') == 'FunctionCall' and node.get('kind') == 'typeConversion' and len(node.get('arguments', [])) == 1:
        return _seed_address(node['arguments'][0], parameters)
    if node.get('nodeType') == 'Literal':
        try:value = int(node.get('value',''),0)
        except (ValueError,TypeError):return None
        if 0 < value < 2**160:return {'term':'address_literal','value':value}
    return None


def _is_table(decl):
    typ = decl.get('typeName') or {}
    return (typ.get('nodeType')=='Mapping' and typ.get('keyType',{}).get('name')=='address'
            and typ.get('valueType',{}).get('name')=='bool')


def _role_index(facts, target):
    from .initial_state import model,domain,CAPABILITY
    initial=model(facts,target);lookup=facts.lookups[target]
    token=(target,domain(lookup),initial['identity'])
    cache=facts.__dict__.setdefault('_authority_by_target',{})
    if token in cache:return cache[token]
    decls={rid:lookup.nodes[rid] for rid,row in initial['declarations'].items() if
        _is_table(lookup.nodes[rid]) or row['type'] in ('address','address payable')}
    origins={r:[] for r in decls};writers={r:[] for r in decls};invalid=set();seen={r:set() for r in decls}
    clean=[p for p in initial['constructor_paths'] if p['flow'] in ('normal','returned') and not p.get('issues') and not p.get('evaluation_gaps')]
    def seed(term):
        if term.get('kind')=='actual_sender':return {'term':'deployer'}
        if term.get('kind')=='parameter' and term.get('id') in initial['constructor_parameters']:
            return {'term':'constructor_parameter','id':term['id']}
        if term.get('kind')=='literal' and type(term.get('value')) is int and 0<term['value']<2**160:
            return {'term':'address_literal','value':term['value']}
        return None
    for rid,decl in decls.items():
        row=initial['declarations'][rid]
        if any(p.get('issues') or p.get('evaluation_gaps') for p in initial['constructor_paths']):
            if row['constructor_writes'] or row['explicit_constructor_sites'] or row['explicit_initializer']:invalid.add(rid)
        for pi,p in enumerate(clean):
            relevant=[w for w in p['writes'] if w['path']['root']==rid]
            if not _is_table(decl):relevant=relevant[-1:]
            for w in relevant:
                v=w['value'];idx=keys(w['path'])
                origin=seed(idx[0]) if _is_table(decl) and len(idx)==1 and v.get('kind')=='literal' and v.get('value') is True else seed(v) if not _is_table(decl) else None
                if origin:origins[rid].append(dict(origin,source=w['source'],constructor_path=pi,guards=p['guards'],source_kind='constructor'))
                elif not _is_table(decl) and v.get('kind')=='literal' and v.get('value')==0:pass
                elif not _is_table(decl):invalid.add(rid)
        if not origins[rid] and domain(lookup)==CAPABILITY and row['type'] in ('address','address payable') and not row['explicit_initializer'] and not row['constructor_writes'] and not row['explicit_constructor_sites']:
            origins[rid].append({'term':'abstract_initial_role','declaration':rid,'source':row['source'],
                'source_kind':'declared_conditional_initial_assumption','analysis_domain':CAPABILITY})
    for rid,rows in initial['runtime_writers']['paths'].items():
        if rid not in decls:continue
        for row in rows:
            seen[rid].add(row['source'].get('ast_id'))
            if row['flow']=='reverted':continue
            if not row['complete']:invalid.add(rid);continue
            p=facts.paths[row['path']]['raw'];dst=row['cell'];value=row['value']
            if key(dst)==key(value) or value.get('kind')=='literal' and value.get('value') in (False,0):continue
            writers[rid].append({'operation':row['operation'],'path':row['path'],'guards':p['guards'],'site':row['source'].get('ast_id')})
    for rid in decls:
        missing=set(initial['runtime_writers']['sites'].get(rid,[]))-seen[rid]
        # A source site on a fully known reverting path cannot grant authority.
        if missing:invalid.add(rid)
    known={r for r in decls if r not in invalid and (origins[r] or writers[r])}
    if initial['runtime_writers']['opaque_storage_writes']:known.clear()
    def protected(writer,roots):return set().union(*(_roots(g,roots) for g in writer['guards']))
    def close(s):
        while True:
            keep={r for r in s if all(protected(w,s) for w in writers[r])}
            if keep==s:return keep
            s=keep
    known=close(known);active={r for r in known if origins[r]}
    while True:
        add={r for r in known-active if any(protected(w,active) for w in writers[r])}
        if not add:break
        active.update(add)
    active=close(active)
    records={r:{'declaration':r,'target':target,'kind':'caller_membership' if _is_table(decls[r]) else 'caller_equals_account',
        'source':lookup.anchor(decls[r]),'deployment_origins':[o for o in origins[r] if o['term']!='abstract_initial_role'],
        'abstract_origins':[o for o in origins[r] if o['term']=='abstract_initial_role'],
        'source_origins':origins[r],'analysis_domain':domain(lookup),'initial_model_identity':initial['identity'],
        'guarded_grant_paths':[{'operation':w['operation'],'path':w['path'],'site':w['site'],
            'qualifying_declarations':sorted(protected(w,active)),
            'qualification_guards':[g for g in w['guards'] if _roots(g,active)]} for w in writers[r]],
        'has_runtime_assignment':bool(initial['runtime_writers']['sites'].get(r))} for r in sorted(active)}
    facts.__dict__.setdefault('_authority_diagnostics',{})[target]={'analysis_domain':domain(lookup),'unresolved_declarations':sorted(invalid),
        'reachable_function_ids':initial['runtime_writers']['functions'],'opaque_storage_writes':initial['runtime_writers']['opaque_storage_writes']}
    cache[token]=records
    return records


def _same_public_effect(facts,oid,path,registry):
    """Both sides of an if can implement an identical operation. A caller test alone then confers no advantage."""
    def effect(p):
        return key([[(w['path'],w['value']) for w in p['writes']],p.get('sensitive_effects',[]),p.get('return_value')])
    guards=set(map(key,path['guards']))
    for _,other in facts.operation_paths(oid,True):
        if other is path or any(_roots(g,registry) for g in other['guards']):continue
        opposite=set(map(key,other['guards']))
        for g in path['guards']:
            if not _roots(g,registry):continue
            neg=g['args'][0] if g.get('op')=='!' else {'kind':'op','op':'!','args':[g]}
            if opposite==(guards-{key(g)})|{key(neg)} and effect(path)==effect(other):return True
    return False


def path_qualification(facts, oid, path):
    cache=facts.__dict__.setdefault('_path_qualifications',{})
    from .initial_state import domain
    token=(oid,id(path),domain(facts.lookup(oid)))
    if token in cache:return cache[token]
    target=facts.operations[oid]['target']
    registry=_role_index(facts,target)
    proof=[]
    for g in path['guards']:
        ids=_roots(g,registry)
        if ids:proof.append({'guard':g,'roles':[registry[i] for i in sorted(ids)]})
    if proof and _same_public_effect(facts,oid,path,registry):proof=[]
    if proof:
        principal_ids={r['declaration'] for row in proof for r in row['roles']}
        # A second source read may alias the very deployer denoted by the qualifying table.
        related={c['root'] for c in selectors([path['guards'],path['writes']]) if c['root'] in registry}
        proof[0]['related_fixed_accounts']=[registry[i] for i in sorted(related-principal_ids)
                    if registry[i]['kind']=='caller_equals_account' and not registry[i]['has_runtime_assignment']]
    cache[token]=proof
    return proof


def fixed_role_terms(encoder, qualification, slot):
    """Use the same deployment identities across fixed membership tables and fixed scalar roles."""
    from pr_next_joint.verification.sequence import qualify
    roles={r['declaration']:r for row in qualification for r in row['roles']+row.get('related_fixed_accounts',[])}
    from .initial_state import domain,CAPABILITY,DEPLOYMENT,initial_for_lookup
    if domain(encoder.lookup) in (CAPABILITY,DEPLOYMENT) and initial_for_lookup(encoder.lookup):
        return [],[{'declaration':rid,'origins':r.get('source_origins',r['deployment_origins']),
            'scope':'constructor and committed prefix encoded by shared initial state model',
            'analysis_domain':domain(encoder.lookup)} for rid,r in roles.items()]
    z=encoder.z;terms=[];receipt=[]
    caller=encoder.expr(qualify({'kind':'actual_sender'},slot))
    for rid,role in roles.items():
        if role['guarded_grant_paths'] or not role['deployment_origins']:continue
        if role['kind']=='caller_equals_account' and len(role['deployment_origins'])!=1:continue
        values=[]
        for origin in role['deployment_origins']:
            if origin['term']=='address_literal':values.append(z.IntVal(origin['value']));continue
            symbol='deployment_caller' if origin['term']=='deployer' else 'deployment_address_parameter_'+str(origin['id'])
            value=z.Int(symbol);terms.extend([value>=0,value<2**160])
            if origin['term']=='deployer':terms.append(value!=0)
            values.append(value)
        cell={'kind':'storage','root':rid,'segments':[]}
        if role['kind']=='caller_membership':
            cell['segments']=[{'key':{'kind':'actual_sender'}}]
            member=encoder.expr(qualify(cell,slot))
            seeded=z.Or(*[caller==v for v in values])
            terms.append(z.Implies(member,seeded) if role['has_runtime_assignment'] else member==seeded)
        else:
            account=encoder.expr(cell)
            terms.append(z.Or(account==0,account==values[-1]) if role['has_runtime_assignment'] else account==values[-1])
        receipt.append({'declaration':rid,'origins':role['deployment_origins'],
                        'scope':'cannot add members; revocation possible' if role['has_runtime_assignment'] else 'fixed original role at queried caller'})
    return terms,receipt


````

## source/src/pr_next_joint/investigation/scope_relevance.py

原文件 SHA-256 `e2f8653673a391cacf0923e982221208fde17c4ca76177aa3fc3b319ad0e658b`

````python
"""Source necessary conditions for per-entry, per-category obligations.

An excluded necessary condition can close a route without resolving an
unrelated call. This is a dependency certificate, not candidate-list emptiness.
"""
from pr_next_joint.frontend.path_ir import walk, key
from pr_next_joint.frontend.storage import keys, selectors, value_type, selector_relation
from .contracts import CATEGORIES


def source_role_may(f,oid):
    """Whole resolved body scan, including statements beyond a loop frontier."""
    cache=f.__dict__.setdefault('_source_role_may',{})
    if oid in cache:return cache[oid]
    lookup=f.lookup(oid);entry=lookup.function(f.operations[oid]['function'])
    pending=[entry];seen=set();bodies=[]
    while pending:
        body=pending.pop();bid=body.get('id')
        if bid in seen:continue
        seen.add(bid);bodies.append(body)
        for n in walk(body):
            if n.get('nodeType')=='ModifierInvocation':
                d=lookup.nodes.get(n.get('modifierName',{}).get('referencedDeclaration'),{})
                if d:pending.append(d)
            if n.get('nodeType')=='FunctionCall':
                exp=n.get('expression',{});d=lookup.nodes.get(exp.get('referencedDeclaration'),{})
                if d.get('body') and (exp.get('nodeType')=='Identifier' or
                    't_function_internal' in exp.get('typeDescriptions',{}).get('typeIdentifier','')):
                    pending.append(d)
    def sender(n):
        return (n.get('nodeType')=='MemberAccess' and n.get('memberName') in ('sender','origin') and
                n.get('expression',{}).get('name') in ('msg','tx'))
    tainted=set()
    nodes=list(walk(bodies))
    while True:
        old=set(tainted)
        for n in nodes:
            rhs=n.get('rightHandSide') if n.get('nodeType')=='Assignment' else n.get('initialValue')
            if rhs and any(sender(t) or t.get('referencedDeclaration') in tainted for t in walk(rhs)):
                dst=n.get('leftHandSide',{}).get('referencedDeclaration')
                if dst is not None:tainted.add(dst)
                tainted.update(d['id'] for d in n.get('declarations',[]) if d)
        if old==tainted:break
    result=False
    for n in nodes:
        if n.get('nodeType')=='BinaryOperation' and n.get('operator') in ('==','!='):
            for a,b in ((n['leftExpression'],n['rightExpression']),(n['rightExpression'],n['leftExpression'])):
                if (sender(a) or a.get('referencedDeclaration') in tainted) and not (
                    b.get('nodeType')=='Literal' and b.get('value') in ('0','0x0')):result=True
        if n.get('nodeType')=='IndexAccess' and n.get('typeDescriptions',{}).get('typeString')=='bool':
            if any(sender(t) or t.get('referencedDeclaration') in tainted for t in walk(n.get('indexExpression'))):result=True
    cache[oid]=result;return result


def potential_role(f,oid,path):
    from .roles import path_qualification, _roots
    if path_qualification(f,oid,path):return True
    lookup=f.lookup(oid)
    allowed={n['id'] for n in lookup.decls.values() if n.get('stateVariable') and
        (n.get('typeDescriptions',{}).get('typeString') in ('address','address payable') or
         n.get('typeName',{}).get('nodeType')=='Mapping')}
    for guard in path['guards']:
        if _roots(guard,allowed):return True
        for term in walk(guard):
            if term.get('op') in ('==','!=') and any(a.get('kind')=='actual_sender' for a in term.get('args',[])):
                if any(a.get('kind') in ('literal','parameter') for a in term.get('args',[])):return True
            if term.get('kind') in ('unknown','external_return','read_call','call_unresolved'):
                origins=[i for i in path.get('issues',[]) if i.get('reason')==term.get('reason')]
                # A low-level CALL's success flag is not itself a privileged
                # qualification. Callback entry guards are inspected separately.
                if not origins:return True
                for row in origins:
                    node=lookup.nodes.get(row.get('source',{}).get('ast_id'),{})
                    calls=[n for n in walk(node) if n.get('nodeType')=='MemberAccess']
                    if not any(n.get('memberName') in ('call','send','transfer') and
                        n.get('typeDescriptions',{}).get('typeIdentifier','').startswith(('t_function_barecall','t_function_send','t_function_transfer')) for n in calls):
                        return True
    return False


def nonfinancial(backend,oid,cell):
    from .key_roles import relation
    from .ledger import unit_origin,native_only_position
    lookup=backend.f.lookup(oid)
    if (relation(cell,lookup) or {}).get('kind')=='authorization_quantity':return 'holder_authorization_quantity'
    if native_only_position(backend,oid,cell):return 'native_redemption_not_five_class_token_unit'
    semantic=getattr(backend,'semantics',None)
    binding=semantic.lookup(oid,cell) if semantic else None
    if binding and binding['meaning']=='nonfinancial_counter' and not unit_origin(backend,oid,cell):
        return 'source_bound_nonfinancial_interpretation'
    # Clocks and control flags do not become minted tokens merely because a
    # setter changes a numeric value. Require source evidence of dual use.
    temporal=any(any(selector_relation(s,cell)=='same_shape' for s in selectors(g)) and
        any(n.get('kind') in ('block_timestamp','block_number') or n.get('kind')=='environment' and
            n.get('field') in ('timestamp','number') for n in walk(g))
        for other,o in backend.f.operations.items() if o['target']==backend.f.operations[oid]['target']
        for _,p in backend.f.operation_paths(other) for g in p['guards'])
    if temporal and not unit_origin(backend,oid,cell):return 'source_time_dimension_without_asset_use'
    return None


def directory(inv,oid,control_categories):
    from .ledger import unit_origin
    f=inv.f;lookup=f.lookup(oid);operation=f.operations[oid]
    if operation.get('generated_getter'):
        return {'operation':oid,'target':operation['target'],'possible_categories':[],
            'source_routes':[],'excluded_necessary_condition':'compiler_generated_readonly_getter',
            'source':operation['source'],'control_categories':[],
            'unresolved_same_storage_calls':[],'unread_effect_residuals':[]}
    rows=f.summaries.rows(oid,False);cats=set(control_categories);routes=[]
    calls=[r for r in f.call_summaries.rows.values() if r['operation']==oid]
    delegate=[c for c in calls if c['mode']=='DELEGATECALL' and c['unresolved_implementation']]
    if delegate:cats.update(CATEGORIES[1:])
    for row in rows:
        p=f.paths[row['path']]['raw'];possible=set();facts=[]
        if p['flow']=='reverted':
            routes.append({'path':row['path'],'possible_categories':[], 'excluded_necessary_condition':'outer_transaction_does_not_commit'})
            continue
        role=potential_role(f,oid,p) or (p['flow']=='truncated' and source_role_may(f,oid))
        if not role and not delegate:
            facts.append('no_privileged_qualification_on_this_source_route')
        else:
            moves={s:[] for s in ('-','+')}
            for e in row['numeric_effects']:
                if e['holder'] is None:continue
                why=nonfinancial(inv.backend,oid,e['cell'])
                if why:
                    facts.append({'position':e['cell'],'excluded_financial_unit':why});continue
                for sign,direction in (('-','debit'),('+','credit')):
                    if direction in e['may_directions']:moves[sign].append(e['cell'])
            paired=lambda a,others:any(selector_relation(a,b)=='same_shape' and key(a)!=key(b) for b in others)
            if any(paired(d,moves['+']) for d in moves['-']):possible.add('FCR-TRANSFER')
            if any(not paired(d,moves['+']) for d in moves['-']):possible.add('FCR-DESTROY')
            if any(not paired(c,moves['-']) for c in moves['+']):possible.add('FCR-MINT')
            for call in calls:
                if call['path']!=row['path'] or not call['unresolved_implementation']:continue
                n=lookup.nodes.get(call['source'].get('ast_id'),{})
                declaration=lookup.nodes.get(n.get('expression',{}).get('referencedDeclaration'),{})
                # A source-declared ordinary external method can affect its
                # separate asset ledger; native value calls alone cannot mint
                # or destroy a local token ledger. Known callback writes are
                # retained under their own original entries and qualifications.
                if call['mode']=='DELEGATECALL':possible.update(CATEGORIES[1:])
                elif call['mode']!='STATICCALL' and declaration.get('nodeType')=='FunctionDefinition':
                    possible.update(('FCR-TRANSFER','FCR-MINT','FCR-DESTROY'))
        cats.update(possible)
        routes.append({'path':row['path'],'possible_categories':sorted(possible),
            'qualification_may_hold':role,'necessary_condition_facts':facts,
            'residuals':row['residuals'],'flow':p['flow']})
    # A failed frontend or a path abandoned before its body was inspected
    # cannot supply a no-effect certificate. Loop frontier residuals retain
    # the classes of their actual body effects; arbitrary assembly does not.
    hard=[g for g in operation.get('gaps',[]) if g.get('kind')=='path_extraction']
    opaque=[i for _,p in f.operation_paths(oid) for i in p.get('issues',[]) if
        any(s in str(i.get('reason','')) for s in ('unsupported_statement','unresolved_storage','write_expansion','source_path_frontier_bound_exceeded'))]
    if not rows or hard or opaque:cats.update(CATEGORIES[1:])
    return {'operation':oid,'target':operation['target'],'possible_categories':sorted(cats),
        'source_routes':routes,'unresolved_same_storage_calls':[c['id'] for c in delegate],
        'unread_effect_residuals':hard+opaque,'control_categories':sorted(control_categories),
        'callback_entries_have_independent_source_obligations':True}

````

## source/src/pr_next_joint/investigation/selection.py

原文件 SHA-256 `fd3702be585d8836fbbc8bdf71974750d992cd03f6685be64598e373e104567f`

````python
"""Choose a source-bound observation by its power to separate two stated interpretations.

The model supplies expected outcomes, never a witness. Storage identifiers below
are resolved only among selectors of the actual entry. This layer produces actions,
not new risk items. The legacy first-pair order is retained for engineering comparison.
"""
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, selector_relation
from .protocol import normal_alternative
from .request_scope import claim_entries, linked_controls, request_target, select_controls, unique_cells


def _named(inv, oid, selectors_, name):
    if not isinstance(name, str) or not name:
        return []
    nodes = inv.f.lookup(oid).nodes
    return list({key(cell): cell for cell in selectors_ if nodes.get(cell['root'], {}).get('name') == name
                 or inv.backend._storage_name(oid,cell)==name}.values())


def plan_observation(inv, binding, item, plan):
    from .properties import interpret, plan_property, premise_cases, source_target
    from .ledger import MEASURES
    request = interpret(item)
    if isinstance(request,dict) and request.get('measure') in set(MEASURES)|{'direct_effect','denied_qualified','missing_control','authorization_violation'}:
        plan_property(inv,binding,item,plan,request)
        return
    item = dict(item,observation=request)
    if request is None:
        return
    root = binding.get('core_operation')
    empty = {'pool': [], 'selected': None, 'status':'indeterminate'}
    plan['observation_choice'] = empty
    if not root or not isinstance(request, dict):
        empty['reason'] = 'observation_or_applied_core_not_resolved'
        return
    explanation=normal_alternative(item);empty['normal_interpretation']=explanation
    predictions={k:request[k] for k in ('risk','normal') if type(request.get(k)) is bool}
    distinct=len(predictions)==2 and predictions['risk']!=predictions['normal']
    f = inv.f
    measure = request.get('measure')
    if not isinstance(measure,str) or measure not in ('holder_grant','holder_net','opens','blocks'):
        empty.update(status='unsupported',reason='no_program_observable_for_this_semantic_question')
        return
    finding_root = root
    root, possible_uses, reason = request_target(inv, binding, item, plan, measure)
    empty['request_resolution'] = {'finding_root': finding_root, 'use': root, 'possible_uses': possible_uses,
                                   'unmeasured_uses': [u for u in possible_uses if u != root]}
    if reason:
        empty.update(status='infeasible_scope', reason=reason)
        return
    if (measure=='holder_grant' and f.options.scope!='AC') or (measure=='holder_net' and f.options.scope!='FCR'):
        empty.update(status='infeasible_scope', reason='observation_task_mismatch')
        return
    paths = [p for _,p in f.operation_paths(root,True)]
    guard_cells = [s for p in paths for s in selectors(p['guards'])]
    reads = [s for p in paths for s in selectors([p['guards'],p['writes'],p.get('sensitive_effects',[])])]
    writable=[w['path'] for p in paths for w in p['writes']]
    control_pool=guard_cells if measure=='holder_grant' else reads
    objects=_named(inv,root,writable,request.get('object')) if 'object' in request else [
        o for o in {key(s):s for s in writable}.values() if inv.backend._holder(root,o) is not None]
    controls=_named(inv,root,control_pool,request.get('control')) if 'control' in request else list(
        {key(s):s for s in guard_cells}.values())
    if root != finding_root:
        controls = select_controls(inv, root, linked_controls(inv, finding_root, root), request, item)
    elif f.options.scope == 'FCR' and measure in ('opens','blocks'):
        writers = claim_entries(inv, binding, item) - {root}
        if request.get('after'):
            writers = set(inv.catalog.resolve(request['after']))
        connected = unique_cells(c for w in writers for c in linked_controls(inv, w, root))
        controls = select_controls(inv, root, connected, request, item)
    if 'control' not in request and measure=='holder_grant':
        controls=[s for s in controls if any(n.get('kind')=='actual_sender' for n in walk(keys(s)))]
    if 'control' not in request and measure=='holder_net':
        # A requested payout-mode change may be guarded by a unique non-right state cell.
        controls=[s for s in controls if not any(selector_relation(s,o)=='same_shape' for o in objects)]
    def one_position(cells):
        return len({key(c) for c in cells})==1
    if not one_position(controls) or measure in ('holder_grant','holder_net') and not one_position(objects):
        empty.update(status='infeasible_scope',reason='control_or_right_not_bound_to_unique_source_declaration')
        return
    if measure=='holder_grant':
        # A holder key and immediate caller must occur in the tested guard itself.
        holders = [inv.backend._holder(root,o) for o in objects]
        controls = [g for g in controls if any(h and any(key(k)==key(h) for k in keys(g)) for h in holders)
                    and any(n.get('kind')=='actual_sender' for n in walk(keys(g)))]
    if measure=='holder_net':
        objects = [o for o in objects if inv.backend.net_unit(root,o)]
    if not controls or measure in ('holder_grant','holder_net') and not objects:
        empty.update(status='unsupported',reason='holder_direction_or_financial_unit_not_established')
        return
    after = request.get('after')
    after_ids = source_target(inv,after,f.operations[root]['target']) if after is not None else []
    cases,gaps=premise_cases(inv,root,item)
    if gaps:
        empty.update(status='unsupported',reason='; '.join(gaps));return
    if after is not None and (len(after_ids)!=1 or f.operations[after_ids[0]]['target']!=f.operations[root]['target']):
        empty.update(status='infeasible_scope',reason='intervention_target_ambiguous_or_different')
        return
    graph_pairs = plan['selected_pairs'] + plan['deferred_pairs']
    writers = list(dict.fromkeys(p['change'] for p in graph_pairs if p['observe']==root))
    target=f.operations[root]['target']
    hint=item.get('next_check');hint=hint if isinstance(hint,dict) else {}
    explicit=inv.catalog.resolve(hint.get('change')) if hint.get('action')=='compare' and inv.catalog.resolve(hint.get('observe'))==[root] else []
    # A real explicit prior probe remains in the shared pool even when it tests a different control.
    if len(explicit)==1 and f.operations[explicit[0]]['target']==target:
        writers=list(dict.fromkeys(explicit+writers))
    for control in controls:
        for writer in sorted(inv.graph.access[(target,control['root'])]['writers']):
            if writer!=root and writer not in writers:
                writers.append(writer)
    if root != finding_root:
        writers = [finding_root]
    elif f.options.scope == 'FCR' and measure in ('opens','blocks'):
        allowed = claim_entries(inv, binding, item) - {root}
        if after_ids:
            allowed = set(after_ids)
        writers = [w for w in writers if w in allowed]
    delta = None
    if f.options.scope == 'FCR' and measure in ('opens','blocks'):
        deltas = inv.backend._holder_deltas(root)
        if request.get('object'):
            deltas = [row for row in deltas if any(key(o)==key(row[0]) for o in objects)]
        if len(deltas)!=1:
            empty.update(status='unsupported', reason='holder_position_or_ledger_direction_not_unique; ordinary source use preserved')
            return
        cell, holder, direction = deltas[0]
        delta = {'cell':cell,'holder':holder,'direction':direction}
        objects = [cell]
    if after_ids == [root] and finding_root == root and linked_controls(inv,root,root) and root not in writers:
        writers.append(root)
    pool = empty['pool']
    for writer in writers[:f.options.max_actions]:
        ws=[w['raw']['path'] for w in f.writes.values() if w['operation']==writer]
        matching=[c for c in controls if any(selector_relation(c,w)=='same_shape' and
                  not inv.graph._disjoint_keys(c,w) for w in ws)]
        if measure=='holder_grant':
            # In the same-requester experiment a caller writing their own holder slot
            # cannot install a grant in another holder's slot, even when roots coincide.
            def possible_other_holder(g):
                pos={i for i,k in enumerate(keys(g)) if any(key(k)==key(inv.backend._holder(root,o)) for o in objects)}
                return any(selector_relation(w,g)=='same_shape' and not inv.graph._disjoint_keys(w,g)
                           and all(keys(w)[i].get('kind')!='actual_sender' for i in pos) for w in ws)
            matching=[c for c in matching if possible_other_holder(c)]
        candidates = list(dict.fromkeys(['availability',measure]))
        for kind in candidates:
            context=inv._compare_context({'current':item},writer,root)
            # Generic commit probes have no measured entitlement delta.
            state='indeterminate'
            if after_ids and writer!=after_ids[0] or not matching:
                state='infeasible_scope'
            elif kind==measure:
                state='distinguishing' if distinct else 'shared_technical_fact'
            elif measure=='holder_net':
                # Knowing only that a call commits is compatible with both a full and a short payout.
                state='same_expected_observation'
            if kind!='availability':
                context['premise_cases']=cases
                context['observable']={'measure':kind,'control_selectors':matching,'objects':objects}
                if f.options.scope == 'FCR' and measure in ('opens','blocks'):
                    from .properties import privileged_paths
                    context['observable']['qualified_writer_paths']=privileged_paths(inv,writer)
                    companion = [s for s in linked_controls(inv,writer,root) if s['root'] not in {v['root'] for v in matching}]
                    context['observable'].update(hold_other_request_cells=True,holder_delta=delta,
                                                 other_intervention_inputs=companion)
                if kind=='holder_grant':
                    context['caller_modes']=['same_requester']
            pool.append({'action':'compare','change':writer,'observe':root,'measure':kind,'status':state,
                         'expectations':predictions if distinct and kind==measure else {},
                         'scope':{'target':target,'controls':matching,'objects':objects, 'finding_root':finding_root,
                                   'use':root,'intervention':writer, 'measure':kind, 'holder_delta':delta,
                                   'extent':'one source-bound request; other routes and amounts not certified'},
                         'context':context,
                         'cached':inv.backend.reusable('compare',{'change':writer,'observe':root,'context':context})})
    chosen = [p for p in pool if p['status'] in ('distinguishing','shared_technical_fact')]
    if chosen:
        pick=min(chosen,key=lambda p:(not p['cached'],writers.index(p['change'])))
        empty.update(selected=pick,status=pick['status'],reason='distinct explicit predictions' if distinct else 'grounded common fact; normative alternatives remain open')
    else:
        empty.update(status='infeasible_scope',
                     reason='no scoped test with differing explicit predictions')
    legacy=next((p for p in pool if p['measure']=='availability' and (not explicit or explicit==[p['change']])),None)
    empty['prior_candidate']=legacy
    empty['legacy_graph_first']=plan['selected_pairs']
    if empty['selected']:
        pick=empty['selected']
        plan['selected_pairs']=[{'change':pick['change'],'observe':root,
                                 'source_reason':'same scope and conflicting predicted observation'}]
        plan['deferred_pairs']=[p for p in graph_pairs if (p['change'],p['observe'])!=(pick['change'],root)]
    inv.graph.events.append({'action':'disagreement_selection','operation':root,'question':plan['question'],
                             'status':empty['status'],'selected':None if not chosen else [pick['change'],root,pick['measure']],
                             'pool_size':len(pool),'old_explicit_or_graph_pair':None if legacy is None else [legacy['change'],root]})
    empty['unexamined_writer_count']=max(0,len(writers)-f.options.max_actions)

````

## source/src/pr_next_joint/investigation/semantic_claims.py

原文件 SHA-256 `da974255a59bd894c809094d3a0d375a7d5ac3c8fed4b4f7126e33e4e3dc883b`

````python
"""Small, polarity-preserving interpretation of source-bound semantic proposals.

This layer does not infer asset meaning from Solidity names.  It distinguishes
an assertion from its negation/question before the existing source binder can
use it. Ambiguous free text requires a focused answer; a keyword is not proof.
"""
import re


FINANCIAL = re.compile(
    r"\b(?:tokens?|tokenized|redeemable|financial\s+(?:assets?|rights?|balances?)|"
    r"holders?['’]?s?\s+(?:balances?|rights?)|asset\s+ledger)\b|代币|可兑付|金融资产|资产权益", re.I)
COUNTER = re.compile(
    r"\b(?:non[- ]?financial(?:\s+counter)?|(?:service|request|usage|event|call)\s+(?:requests?|counts?|counter|number)|"
    r"(?:counts?|records?)\s+(?:only\s+)?(?:service\s+)?requests?)\b|非金融|服务请求|普通计数|调用次数|事件次数", re.I)
UNCERTAIN = re.compile(
    r"\b(?:whether|unclear|unknown|uncertain|determine|investigate|question|might|may\s+(?:be|represent)|"
    r"could\s+(?:be|represent)|not\s+(?:yet\s+)?(?:established|determined|known|clear)|"
    r"assuming|suppos(?:e|ing)|if\s+(?:this|the\s+\w+)\s+(?:is|represents))\b|"
    r"是否|尚不|无法确定|不确定|待确定|含义未明|假设|假如|若.{0,18}(?:代表|表示|属于)", re.I)
NEGATION = re.compile(
    r"\b(?:not|never|neither|nor|no|without|non[- ]|doesn't|isn't|aren't|isnt|doesnt|cannot)\b|"
    r"(?:不|并非|不是|不属于|不表示|不代表|不涉及|无)(?:是|属于|表示|代表|涉及)?", re.I)
NEGATED_NEGATION = re.compile(r"\b(?:not\s+only|not\s+merely|not\s+just)\b|不仅|不只是", re.I)
ASSERTION = re.compile(
    r"\b(?:is|are|represent\w*|record\w*|hold\w*|store\w*|track\w*|balance|ledger|"
    r"mint\w*|issu\w*|burn\w*|destroy\w*|transfer\w*|debit\w*|credit\w*|clear\w*|"
    r"reset\w*|withdraw\w*|redeem\w*|freeze\w*|block\w*|token)\b|"
    r"表示|代表|记录|保存|持有|余额|账本|发行|增发|转账|销毁|冻结|扣减|清零|权益", re.I)
MEANING_VERB=re.compile(r'\b(?:represent\w*|denot\w*|constitut\w*|signif\w*|mean\w*|record\w*|store\w*|track\w*)\b|表示|代表|属于|构成|记录|保存',re.I)
ACTION_VERB=re.compile(r'\b(?:transfer\w*|withdraw\w*|redeem\w*|mint\w*|issu\w*|burn\w*|destroy\w*|freeze\w*|block\w*|debit\w*|credit\w*|reduce\w*|clear\w*|spend\w*)\b|转移|转账|提取|兑付|增发|销毁|冻结|扣减|清零',re.I)


def negates_meaning(prefix):
    """Negation of an operation is not negation of the object's asset meaning."""
    prefix=NEGATED_NEGATION.sub('',prefix[-140:])
    negatives=list(NEGATION.finditer(prefix))
    if not negatives:return False
    tail=prefix[negatives[-1].end():]
    semantic=list(MEANING_VERB.finditer(tail));actions=list(ACTION_VERB.finditer(tail))
    if actions and (not semantic or actions[-1].end()>semantic[-1].end()):return False
    if semantic:return True
    # Direct adjectival/copular negation; long unidentified clauses are not
    # guessed to be asset denials.
    return bool(re.fullmatch(r"\s*(?:(?:a|an|the|any|actual|really|necessarily|genuine|longer|as|be|being|of|assets?|rights?|tokens?|balances?|or|nor|and)\s+){0,8}",tail,re.I)
                or re.fullmatch(r'(?:是|属于|表示|代表|任何|真正的|实际的|一种|一个|可)?\s*',tail))


def clauses(text):
    # Contrast and punctuation delimit negation scope. A question/conditional
    # marks the full sentence, including clauses after a comma or semicolon.
    result=[]
    for sentence in re.split(r'(?<=[.!?。！？])\s*|\n+', str(text or '')):
        if not sentence.strip():continue
        uncertain=bool(UNCERTAIN.search(sentence) or '?' in sentence or '？' in sentence)
        for part in re.split(r';|；|,|，|\bbut\b|\bwhereas\b|\bhowever\b|但是|但(?:是)?|而非',sentence,flags=re.I):
            part=part.strip()
            if part:result.append((part,uncertain))
    return result


def resource_assertion(text, answer=None):
    """Return supported polarity and original spans, never a truth boolean.

    Exact short choices remain supported. Their explanation cannot expressly
    contradict the choice. Mixed/conditional claims are left unresolved.
    """
    text=str(text or '').strip();positive=[];negative=[];questions=[];counter=[];incidental=[]
    for clause,uncertain in clauses(text):
        terms=list(FINANCIAL.finditer(clause))
        counter_terms=list(COUNTER.finditer(clause))
        if uncertain and (terms or counter_terms):
            questions.append(clause);continue
        for match in counter_terms:
            if negates_meaning(clause[:match.start()]):
                continue
            counter.append(clause)
        if not terms:continue
        if uncertain:questions.append(clause);continue
        for term in terms:
            before=clause[:term.start()]
            # Denying that an action is an asset event does not assert either
            # asset ownership or nonfinancial meaning. Preserve an independent
            # explicit meaning statement instead of manufacturing a conflict
            # from the noun inside this denied event relation.
            if re.search(r'\b(?:is|are|constitutes?)\s+(?:not|never)\s+(?:an?\s+)?'
                         r'(?:destruction|transfer|issuance|minting|redemption|withdrawal|'
                         r'freezing|payment|burning)\s+of\s+(?:the\s+)?$',before,re.I):
                incidental.append({'span':clause,'term':term.group(),'relation':'denied_event_not_resource_assertion'})
                continue
            # Negation after an independent finite verb belongs to that other
            # statement. The supported language deliberately avoids guessing
            # through nested explanations and reported speech.
            window=before[-140:]
            if re.search(r"\b(?:claim\w*|alleg\w*|suggest\w*)\b.{0,35}$",window,re.I):
                questions.append(clause);continue
            neg=negates_meaning(window)
            if neg:negative.append({'span':clause,'term':term.group(),'polarity':'negative'})
            elif ASSERTION.search(clause):positive.append({'span':clause,'term':term.group(),'polarity':'positive'})
            else:questions.append(clause)
    choices={'financial_right':'financial_right','token_ledger':'financial_right',
             'redeemable_credit':'financial_right','nonfinancial_counter':'nonfinancial_counter'}
    requested=choices.get(str(answer or '').strip())
    negative_only=bool(negative or counter) and not positive
    if requested=='financial_right':
        meaning=None if negative or counter or questions else requested
    elif requested=='nonfinancial_counter':
        meaning=None if positive or questions else requested
    elif positive and not negative and not questions and not counter:
        meaning='financial_right'
    elif (negative or counter) and not positive and not questions:
        meaning='nonfinancial_counter'
    else:meaning=None
    token_positive=any(re.search(r'\btokens?\b|代币',x['term'],re.I) for x in positive)
    return {'meaning':meaning,'positive_spans':positive,'negative_spans':negative,
        'counter_spans':counter,'unresolved_spans':questions,'nonassertive_event_mentions':incidental,'requested_choice':requested,
        'unit_kind':'token' if token_positive else 'unspecified_financial',
        'polarity_preserved':True,'original_text':text,
        'status':'asserted' if meaning else 'semantic_polarity_or_scope_unresolved'}


def normal_proposal(item, explicit=None):
    if explicit and explicit.get('meaning')=='normal_authorization':
        return {'text':explicit.get('basis',''),'source':'focused_model_answer','id':explicit.get('id')}
    if item.get('assessment')!='normal':return None
    text=' '.join(str(item.get(k) or '') for k in ('claim','alternative','revision_reason','normal_basis'))
    return {'text':text,'source':'model_normal_proposal'} if text.strip() else None

````

