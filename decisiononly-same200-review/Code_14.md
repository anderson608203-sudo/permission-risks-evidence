# 实跑源码文本 · 第 14 页

## file-58bab83308470f

`source/src/pr_next_joint/investigation/selection.py` · 原字节 SHA-256 `fd3702be585d8836fbbc8bdf71974750d992cd03f6685be64598e373e104567f`

~~~~python
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

~~~~

## file-3ed09c5d51a0e8

`source/src/pr_next_joint/investigation/semantic_claims.py` · 原字节 SHA-256 `da974255a59bd894c809094d3a0d375a7d5ac3c8fed4b4f7126e33e4e3dc883b`

~~~~python
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

~~~~

## file-507ee64ff6b2b5

`source/src/pr_next_joint/investigation/state_encoding.py` · 原字节 SHA-256 `51d42be24fc7cf77dca41812b2eb0062700c2ce3270c56a28328fc404375ba26`

~~~~python
"""Encode a shared constructor state and only committed bounded prefix writes.

Numerical abstract leaves remain congruent functions. Constructor/prefix branch
obligations are inside their disjunction, never unconditional side effects.
"""
import copy
import itertools
import re
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key, walk, lit
from pr_next_joint.frontend.storage import keys, selectors, value_type
from pr_next_joint.verification.sequence import qualify, read
from pr_next_joint.verification.expressions import Unsupported
from .initial_state import CAPABILITY, DEPLOYMENT, domain, initial_for_lookup, family


def _initial_term(value, model, selected_domain):
    if isinstance(value, list): return [_initial_term(x, model, selected_domain) for x in value]
    if not isinstance(value, dict): return value
    kind = value.get('kind')
    if kind == 'actual_sender':
        return {'kind': 'parameter', 'id': -990000001, 'type': 'address', 'initial_identity': 'deployment_caller'}
    if kind == 'parameter':
        return {**value, 'initial_identity': 'constructor_parameter'} if value.get('constructor_parameter') or value.get('id') in model['constructor_parameters'] else value
    if kind in ('environment', 'transaction_value', 'transaction_origin'):
        return {**value, 'initial_identity': 'constructor_environment'}
    if kind == 'storage' and not value.get('instance'):
        row = model['declarations'].get(value['root'])
        if row is None: raise Unsupported('initial_storage_declaration_unresolved')
        segments = _initial_term(value.get('segments', []), model, selected_domain)
        prepared = {**value, 'segments': segments}
        typ = value_type(prepared, model['_lookup'])
        symbolic = selected_domain == CAPABILITY and not row['explicit_initializer'] and (
            not segments and bool(re.fullmatch(r'(?:address(?: payable)?|u?int\d*)', typ or '')) or
            family(value) in model['_amount_families'])
        if symbolic:
            return {**prepared, 'instance': 'initial_storage:' + selected_domain + ':' + model['identity']}
        if typ == 'bool': return lit(False)
        if re.fullmatch(r'(?:address(?: payable)?|u?int\d*|bytes\d+)', typ or '') or (typ or '').startswith(('contract ', 'enum ')):
            return lit(0)
        raise Unsupported('initial_default_type_not_encoded:' + str(typ))
    return {k: _initial_term(v, model, selected_domain) for k, v in value.items()}


def _runtime_candidates(facts, lookup, model, queried):
    """Only real writers of constrained queried roots and their guard prerequisites."""
    relevant = set()
    for cell in queried:
        row = model['declarations'].get(cell['root'], {})
        if row.get('explicit_initializer') or row.get('constructor_writes') or value_type(cell, lookup) == 'bool' or family(cell) not in model['_amount_families'] and keys(cell):
            relevant.add(cell['root'])
    paths = []
    # Include prerequisite role writers; never seed a default-false role table.
    for _ in range(facts.options.prefix_depth + 1):
        before = set(relevant)
        for oid, entry in facts.operations.items():
            if entry['target'] != model['target'] or entry.get('generated_getter'): continue
            for pid, p in facts.operation_paths(oid, True):
                if not any(w['path']['root'] in relevant for w in p['writes']): continue
                if not any(x[1] == pid for x in paths): paths.append((oid, pid, p))
                relevant.update(s['root'] for s in selectors(p['guards']))
        if relevant == before: break
    paths.sort(key=lambda x: (facts.operations[x[0]]['source']['start'], x[1]))
    return paths, relevant


def encode(e, details=None, selected_domain=None):
    selected_domain = selected_domain or domain(e.lookup)
    saved = initial_for_lookup(e.lookup)
    if saved is None: raise Unsupported('host_initial_state_model_missing')
    facts = e.lookup._investigation_facts
    # Non-serialized helpers never enter the domain identity.
    model = {**saved, '_lookup': e.lookup, '_amount_families': {family(r['cell']) for r in saved['candidate_amount_leaves']}}
    queried = [v for _, v in sorted(getattr(e, '_state_cells', {}).items()) if not v.get('instance')]
    prefix_limit=getattr(e,'_initial_prefix_limit',1)
    times=list(getattr(e,'_state_times',{}).values())
    token = digest([selected_domain, saved['identity'], queried,times,prefix_limit])
    cache = e.__dict__.setdefault('_initial_encoding_cache', {})
    if token in cache: return cache[token]
    z = e.z; branches = []; receipts = []; limits = []; before_encoding = getattr(e, '_encoding_initial', False)
    e._encoding_initial = True
    candidates, relevant = _runtime_candidates(facts, e.lookup, model, queried)
    sequences = [()]
    max_count = min(facts.options.max_prefixes,prefix_limit)
    for length in range(1, facts.options.prefix_depth + 1):
        for seq in itertools.product(range(len(candidates)), repeat=length):
            if len(sequences) >= max_count:
                limits.append({'reason': 'initial_prefix_frontier_bound', 'maximum': max_count}); break
            sequences.append(seq)
        if len(sequences) >= max_count: break
    incomplete = [r for rid in relevant for r in saved['runtime_writers']['paths'].get(rid, []) if not r['complete'] and r['flow'] != 'reverted']
    if incomplete: limits.append({'reason': 'initial_relevant_writer_path_incomplete', 'paths': sorted({r['path'] for r in incomplete})})
    def expr(v): return e.expr(_initial_term(v, model, selected_domain))
    try:
        for pi, cp in enumerate(saved['constructor_paths']):
            if cp['flow'] not in ('normal', 'returned'): continue
            if cp.get('issues') or cp.get('evaluation_gaps'):
                limits.append({'reason': 'constructor_effect_unresolved', 'constructor_path': pi,
                               'details': cp.get('issues', []) + cp.get('evaluation_gaps', [])}); continue
            for seq in sequences:
                start = len(e.constraints)
                writes = copy.deepcopy(cp['writes']); terms = []; prefix = []
                try:
                    terms.extend(expr(g) for g in cp['guards'])
                    for value in cp.get('evaluated_terms', []): expr(value)
                    for w in writes:
                        typ=value_type(w['path'],e.lookup)
                        if typ in ('string','bytes') and w['value'].get('kind') in ('parameter','literal','fixed_bytes_literal','storage'):continue
                        expr(w['value'])
                    deployer = expr({'kind': 'actual_sender'})
                    terms.append(deployer != 0)
                    for index, candidate in enumerate(seq):
                        oid, pid, path = candidates[candidate]; previous = copy.deepcopy(writes)
                        translate = lambda v: read(qualify(v, 20 + index), previous, e.lookup)
                        terms.extend(expr(translate(g)) for g in path['guards'])
                        for v in path.get('evaluated_terms', []): expr(translate(v))
                        caller = expr(qualify({'kind': 'actual_sender'}, 20 + index)); terms.append(caller != 0)
                        if any(n.get('kind') in ('unknown', 'external_return') for n in walk(path)):
                            raise Unsupported('initial_prefix_critical_external_effect')
                        for w in path['writes']:
                            dst = qualify(w['path'], 20 + index)
                            dst['segments'] = read(dst.get('segments', []), previous, e.lookup)
                            value = translate(w['value']); expr(value)
                            writes.append({**w, 'path': dst, 'value': value})
                        prefix.append({'operation': oid, 'path': pid, 'caller': qualify({'kind': 'actual_sender'}, 20 + index)})
                    # All runtime requests follow the constructor and committed
                    # prefixes. A future setter cannot enable a past request.
                    for field in ('timestamp','number'):
                        relevant_times=[v for v in times if v.get('field',v.get('sequence_role'))==field]
                        if not relevant_times:continue
                        base={'kind':'environment','field':field,'type':'uint256'}
                        previous=expr(base)
                        for index in range(len(seq)):
                            current=expr(qualify(base,20+index));terms.append(current>=previous);previous=current
                        terms.extend(e.expr(v)>=previous for v in relevant_times)
                    for cell in queried:
                        actual = e.expr(cell)
                        expected = expr(read(cell, writes, e.lookup))
                        terms.append(actual == expected)
                    evaluated = e.constraints[start:]; del e.constraints[start:]
                    condition = z.And(*terms, *evaluated)
                    selector = z.Bool('initial_branch_' + token[:16] + '_' + str(len(receipts)))
                    branches.append(z.And(selector, condition))
                    e.__dict__.setdefault('_initial_branch_conditions', {})[str(selector)] = z.And(selector, condition)
                    receipts.append({'selector': str(selector), 'constructor_path': pi, 'prefix': prefix,
                        'explicit_writes': [w['source'] for w in cp['writes']]})
                except (Unsupported, ValueError, KeyError, TypeError) as error:
                    del e.constraints[start:]
                    limits.append({'reason': str(error), 'constructor_path': pi, 'prefix_candidates': list(seq)})
        if not branches:
            # A proved reverting constructor differs from unsupported modeling.
            all_revert = bool(saved['constructor_paths']) and all(p['flow'] == 'reverted' and not p.get('issues') for p in saved['constructor_paths'])
            if not all_revert: raise Unsupported('initial_state_not_encoded:' + str(limits[:2]))
            branches = [z.BoolVal(False)]
        abstract = []
        for cell in queried:
            base = _initial_term(cell, model, selected_domain)
            if any(str(s.get('instance', '')).startswith('initial_storage:') for s in selectors(base)):
                abstract.append({'cell': cell, 'basis': 'uninitialized_typed_scalar_or_frozen_amount_leaf'})
        result = ([z.Or(*branches)], {'analysis_domain': selected_domain, 'initial_model_identity': saved['identity'],
            'analysis': selected_domain, 'shared_constructor_and_prefix': True, 'branches': receipts,
            'encoded_cells': queried, 'abstract_initial_assumptions': abstract, 'limits': limits,
            'prefix_depth_bound': facts.options.prefix_depth, 'prefixes_included': len(sequences),
            'more_prefixes_available':bool(candidates) and prefix_limit<facts.options.max_prefixes,
            'global_reachability_exhausted': not candidates and not limits,
            'explicit_constructor_prefix_executed': False, 'constructor_symbolic_transitions_encoded': True,
            'author_run_initial_state_verified': False})
        cache[token] = result
        return result
    finally:
        e._encoding_initial = before_encoding

~~~~

## file-0ddef75d4c5db8

`source/src/pr_next_joint/investigation/summary.py` · 原字节 SHA-256 `fb166a7d566fad0dd56b1763af91b8179028a740c4055531529637a0fce487eb`

~~~~python
"""Neutral committed effects and source-bound semantic interpretations.

This is one shared access layer for planning, encoding and coverage.  The source
paths already contain compiler-resolved calls/modifiers; no business detector or
new state interpreter is introduced here.  An interpretation never changes M1's
frozen initial-state eligibility.
"""
import copy
import re
from collections import deque
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, value_type, selector_relation
from pr_next_joint.verification.sequence import read
from .initial_state import family, domain
from pr_next_joint.verification.expressions import Unsupported


def unique(values):
    return list({key(v): v for v in values}.values())


def has_basis(text):
    # A short source explanation may be Chinese or another unspaced language;
    # an English word-count threshold is not a semantic protocol requirement.
    return isinstance(text,str) and len(re.sub(r'\W','',text,flags=re.UNICODE))>=6


def holder(cell, lookup):
    """A holder is an actual address key, not a field name or arbitrary integer."""
    from .key_roles import relation
    bound=relation(cell,lookup)
    if bound and len(keys(cell))>bound['holder_key']:return keys(cell)[bound['holder_key']]
    addresses=[k for k in keys(cell) if k.get('kind') in ('actual_sender','contract_address') or
               k.get('type') in ('address','address payable')]
    if len(addresses)==1:return addresses[0]
    if len(addresses)>1:return None
    # Reuse the existing source-owned record case: a non-address record ID
    # may contain one unambiguous address field holding the entitlement owner.
    # An integer key itself is never reinterpreted as that owner.
    segments=cell.get('segments',[])
    if keys(cell) and segments and 'field' in segments[-1]:
        node=lookup.nodes.get(segments[-1]['field'],{})
        record=lookup.nodes.get(node.get('scope'),{})
        addresses=[n for n in record.get('members',[]) if
                   n.get('typeDescriptions',{}).get('typeString') in ('address','address payable')]
        if len(addresses)==1:
            return {'kind':'storage','root':cell['root'],
                    'segments':copy.deepcopy(segments[:-1])+[{'field':addresses[0]['id']}]}
    return None


def directions(cell, after):
    # Only a may classification. All positive/negative claims use actual values.
    if key(cell) == key(after):
        return []
    if after.get('kind') == 'literal' and after.get('value') in (0, '0'):
        return ['debit']
    if after.get('kind') == 'op' and len(after.get('args', [])) == 2:
        a, b = after['args']
        if key(a) == key(cell):
            if after['op'] == '+': return ['credit']
            if after['op'] == '-': return ['debit']
        if key(b) == key(cell) and after['op'] == '+': return ['credit']
    return ['debit', 'credit']


def local_delta(write):
    """Source write delta before cross-key alias composition; never a net claim."""
    inc=write.get('local_increment');operator=write.get('operator')
    if inc is not None:
        if inc.get('op')=='-' and len(inc.get('args',[]))==2 and inc['args'][0].get('value')==0:
            return '-',inc['args'][1]
        return '+',inc
    v=write['value'];args=v.get('args',[])
    if v.get('op') in ('+','-') and len(args)==2 and key(args[0])==key(write['path']):return v['op'],args[1]
    if v.get('kind')=='literal' and type(v.get('value')) is int and v['value']==0:
        return '-',write['path']
    return None,None


def debited_positions(f,oid):
    """Who is actually used as the debit operand, with its source quantity."""
    rows=[]
    for pid,p in f.operation_paths(oid,True):
        for w in p['writes']:
            sign,amount=local_delta(w)
            if sign!='-':continue
            account=holder(w['path'],f.lookup(oid))
            from .key_roles import relation
            if account is None or (relation(w['path'],f.lookup(oid)) or {}).get('kind')=='authorization_quantity':continue
            rows.append({'cell':w['path'],'holder':account,'amount':amount,'path':pid,'source':w['source']})
    return unique(rows)


def path_summary(f, oid, pid, p):
    lookup = f.lookup(oid)
    cells = unique(w['path'] for w in p.get('writes', []))
    numeric = [];local_residuals=[]
    for c in cells:
        try:
            typ = value_type(c, lookup)
            if not re.fullmatch(r'u?int\d*', typ or ''): continue
            after = read(c, p['writes'], lookup)
        except (Unsupported,ValueError,TypeError,KeyError) as error:
            local_residuals.append({'cell':copy.deepcopy(c),'reason':'summary_position:'+type(error).__name__+':'+str(error)})
            continue
        from .key_roles import relation
        role=relation(c,lookup)
        numeric.append({'cell': copy.deepcopy(c), 'family': family(c),'key_role':copy.deepcopy(role),
            'before': copy.deepcopy(c), 'after': after, 'type': typ,
            'holder': holder(c, lookup), 'may_directions': directions(c, after),
            'sources': [w['source'] for w in p['writes'] if selector_relation(w['path'], c) == 'same_shape']})
        if len([a for a in keys(c) if a.get('kind') in ('actual_sender','contract_address') or
                a.get('type') in ('address','address payable')])>1 and not role:
            local_residuals.append({'cell':copy.deepcopy(c),'reason':'multiple_address_keys_need_source_holder_binding'})
    gaps = copy.deepcopy(p.get('issues', []) + p.get('evaluation_gaps', []))+local_residuals
    return {'operation': oid, 'path': pid, 'target': f.operations[oid]['target'],
        'flow': p.get('flow'), 'committing': p.get('flow') in ('normal', 'returned'),
        'guards': copy.deepcopy(p.get('guards', [])), 'ordered_writes': copy.deepcopy(p.get('writes', [])),
        'numeric_effects': numeric, 'effects': copy.deepcopy(p.get('sensitive_effects', [])),
        'return_value': copy.deepcopy(p.get('return_value')), 'residuals': gaps,
        'precision': 'path_conditioned' if not gaps else 'may_with_residual',
        'net_effect_not_operation_spelling': True}


class Summaries:
    def __init__(self, f):
        self.f = f; self.paths = {}; self.operations = {}; self.propagation = []
        from .key_roles import derive
        self.key_roles=derive(f)
        # Worklist propagates source provenance of actually inlined effects.  It
        # does not re-resolve static referencedDeclaration or override dispatch.
        source_users = {}
        for oid, o in f.operations.items():
            rows = [path_summary(f, oid, pid, p) for pid, p in f.operation_paths(oid)]
            self.operations[oid] = {'operation': oid, 'target': o['target'], 'paths': [],
                'residuals': copy.deepcopy(o.get('gaps', [])), 'source_closure': []}
            for row in rows:
                self.paths[row['path']] = row; self.operations[oid]['paths'].append(row['path'])
                for w in row['ordered_writes']:
                    a = w['source']; token = key([o['target'], a.get('file'), a.get('start'), a.get('length')])
                    source_users.setdefault(token, set()).add(oid)
                    self.operations[oid]['source_closure'].append(a)
            self.operations[oid]['source_closure'] = unique(self.operations[oid]['source_closure'])
        # Finite union lattice over compiler-resolved entry effects.  Shared
        # helper provenance can be reused, but effects/guards remain on paths.
        queue = deque(sorted(self.operations)); seen = set(); rounds = 0
        while queue:
            oid = queue.popleft(); rounds += 1
            for a in self.operations[oid]['source_closure']:
                token = key([f.operations[oid]['target'], a.get('file'), a.get('start'), a.get('length')])
                for other in sorted(source_users.get(token, ())):
                    edge = (oid, other, token)
                    if oid == other or edge in seen: continue
                    seen.add(edge); self.propagation.append({'from': oid, 'to': other,
                        'source': a, 'kind': 'shared_resolved_effect_origin',
                        'guards_and_values_not_cross_merged': True})
        self.identity = digest([self.paths, self.propagation])
        self.rounds = rounds
        self._dependencies = None

    @property
    def dependencies(self):
        if self._dependencies is None:
            from .dependencies import Dependencies
            self._dependencies = Dependencies(self)
        return self._dependencies

    def rows(self, oid, committing=True):
        return [self.paths[p] for p in self.operations[oid]['paths']
                if not committing or self.paths[p]['committing']]

    def positions(self, oid):
        return unique(e['cell'] for r in self.rows(oid) for e in r['numeric_effects'] if e['holder'] is not None
                      and (e.get('key_role') or {}).get('kind')!='authorization_quantity')

    def control_only(self,cell,target):
        """A control of another position is not that position's financial unit."""
        from .key_roles import relation
        if (relation(cell,self.f.lookups[target]) or {}).get('kind')=='authorization_quantity':return True
        for oid,o in self.f.operations.items():
            if o['target']!=target:continue
            for r in self.rows(oid):
                if not any(selector_relation(s,cell)=='same_shape' for s in selectors(r['guards'])):continue
                own=[e for e in r['numeric_effects'] if selector_relation(e['cell'],cell)=='same_shape']
                other=[e for e in r['numeric_effects'] if e['holder'] is not None and selector_relation(e['cell'],cell)!='same_shape']
                if other and not own:return True
        return False

    def movements(self, oid, path):
        lookup = self.f.lookup(oid)
        row = path_summary(self.f, oid, 'transient_path', path)
        return {s: unique(e['cell'] for e in row['numeric_effects'] if e['holder'] is not None
                         and (e.get('key_role') or {}).get('kind')!='authorization_quantity'
                         and d in e['may_directions']) for s, d in (('-', 'debit'), ('+', 'credit'))}

    def record(self):
        return {'schema': 'neutral-effect-summary-v1', 'identity': self.identity,
            'operations': self.operations, 'paths': self.paths, 'propagation': self.propagation,'source_key_roles':self.key_roles,
            'value_and_control': {'id':self._dependencies.identity,'artifact':'value_control_dependencies.json'}
            if self._dependencies is not None else None,
            'worklist_rounds': self.rounds, 'fixed_point':not any(r['residuals'] for r in self.paths.values()),
            'finite_extracted_worklist_completed':True,
            'scope': 'finite already compiler-resolved paths; residuals are not completed paths'}


def get_summaries(f):
    if not hasattr(f, 'summaries'): f.summaries = Summaries(f)
    return f.summaries


class Semantics:
    """Versioned H bindings. No Gold, source-name rules or mutable state domain."""
    def __init__(self, f):
        self.f = f; self.resources = {}; self.history = []; self.questions = {};self.consents={}
        self.version = 0;self.active_scope={'phase':None,'assumptions':[]}

    def scope(self,item):
        self.active_scope={'phase':copy.deepcopy(item.get('phase')),'assumptions':copy.deepcopy(item.get('assumptions',[]))}
        return self.active_scope

    def lookup(self, oid, cell):
        target=self.f.operations[oid]['target'];scope=self.active_scope
        scoped=self.resources.get(key([target,family(cell),scope]))
        return scoped or self.resources.get(key([target,family(cell)]))

    def dependency_identity(self,operations,consent_operations=None):
        operations=set(operations)
        consent_operations=operations if consent_operations is None else set(consent_operations)
        families={key([self.f.operations[o]['target'],family(c)]) for o in operations for c in get_summaries(self.f).positions(o)}
        bound=[r['id'] for r in self.resources.values() if
               (key([r['target'],r['family']]) in families or operations.intersection(r['operations'])) and
               (not r.get('scope') or r['scope']==self.active_scope)]
        bound += [r['id'] for r in self.consents.values() if consent_operations.intersection(r['operations']) and
                  r.get('scope')==self.active_scope]
        return digest(sorted(bound))

    def lookup_consent(self,oid,cell):
        return self.consents.get(key([self.f.operations[oid]['target'],oid,family(cell),self.active_scope]))

    def _set(self, oid, cell, meaning, basis, issue, source, operations, assertion=None):
        if not has_basis(basis):
            return None
        f = self.f; lookup = f.lookup(oid)
        if holder(cell, lookup) is None or not re.fullmatch(r'u?int\d*', value_type(cell, lookup) or ''):
            return None
        positions = [p for op in operations for p in get_summaries(f).positions(op)
                     if selector_relation(p, cell) == 'same_shape']
        if not positions: return None
        scope=copy.deepcopy(self.active_scope)
        scoped=bool(scope.get('phase') or scope.get('assumptions'))
        k = key([f.operations[oid]['target'], family(cell),scope]) if scoped else key([f.operations[oid]['target'], family(cell)])
        row = {'target': f.operations[oid]['target'], 'family': family(cell),
            'cell': copy.deepcopy(cell), 'meaning': meaning, 'basis': basis,
            'operations': sorted(operations), 'positions': unique(positions), 'issue': issue,
            'source': source, 'evidence_level': 'source_and_semantic_prediction',
            'economic_meaning_formally_proved': False,
            'analysis_domain': domain(lookup), 'semantic_assertion':copy.deepcopy(assertion)}
        row['scope']=scope if scoped else None
        previous = self.resources.get(k)
        if previous and all(previous.get(x) == row.get(x) for x in ('meaning', 'basis', 'operations')):
            return previous
        self.version += 1; row['version'] = self.version; row['id'] = 'sem_' + digest(row)[:20]
        self.history.append({'before': copy.deepcopy(previous), 'after': copy.deepcopy(row),
                             'derived_cache_invalidation': 'affected binding and dependent properties only',
                             'frozen_initial_state_unchanged': True})
        self.resources[k] = row
        return row

    def consume_issue(self, binding, item):
        ops=binding.get('operations',[]);root=binding.get('core_operation')
        if root is None:return []
        from .semantic_claims import resource_assertion,clauses
        text=' '.join(str(item.get(x)or'')for x in ('claim','resource_basis','resource_kind'))
        candidates=unique(c for o in ops for c in get_summaries(self.f).positions(o))
        lookup=self.f.lookup(root);target=self.f.operations[root]['target']
        # Source entities, not a word shared by the whole paragraph, delimit
        # the meaning/negation attached to each individual position.
        all_positions=unique(c for o,v in self.f.operations.items()if v['target']==target
                             for c in get_summaries(self.f).positions(o))
        def labels(c):
            ids=[c['root']]+[s['field']for s in c.get('segments',[])if 'field'in s]
            return [lookup.nodes.get(i,{}).get('name')for i in ids if lookup.nodes.get(i,{}).get('name')]
        def names(part,c):
            return any(re.search(r'(?<![\w$])'+re.escape(n)+r'(?![\w$])',part)for n in labels(c))
        selected=[];parts=[c for c,_ in clauses(text)]
        for cell in candidates:
            if get_summaries(self.f).control_only(cell,target):continue
            anchored=[part for part in parts if names(part,cell)]
            # With one unambiguous source family, the following sentence can
            # refer to "the holder's balance" without repeating its Solidity
            # spelling. Preserve that explanation and its sentence boundaries.
            # Multiple families still require their own named clauses.
            if len({family(c)for c in candidates})==1 and not any(names(text,c)for c in all_positions if family(c)!=family(cell)):
                anchored=[text]
            elif not anchored:continue
            basis='; '.join(anchored);assertion=resource_assertion(basis)
            if not assertion['meaning']:continue
            previous=self.lookup(root,cell)
            if previous and previous.get('source')=='focused_model_answer':selected.append(previous);continue
            row=self._set(root,cell,assertion['meaning'],basis,item['id'],'original_model_source_claim',ops,assertion)
            if row:selected.append(row)
        return selected

    def question(self, q, oid, cell=None, kind='resource'):
        obj = family(cell) if cell is not None else None
        core=q['binding'].get('core_operation')
        sid = 'sq_' + digest([q['id'],core,oid,obj,kind,self.active_scope])[:16]
        # A resource question denotes a typed storage family. Keep its first
        # representative cell stable between registration, actual message and
        # answer consumption; encountering the recipient cell must not mutate
        # the same ID after the sender cell was already delivered.
        if sid in self.questions:return copy.deepcopy(self.questions[sid])
        row = {'id': sid, 'issue': q['id'], 'operation': oid, 'kind': kind,'core_operation':core,
            'cell': copy.deepcopy(cell), 'target': self.f.operations[oid]['target'],
            'semantic_scope':copy.deepcopy(self.active_scope),
            'question': ('What right does this source-bound account field represent, and which shown use supports that meaning?'
                         if kind == 'resource' else 'Which source-backed authorization applies to this effect, including normal alternatives?'),
            'choices': ['financial_right', 'nonfinancial_counter', 'unknown', 'other_source_explanation'] if kind == 'resource'
                       else ['required_authorization', 'normal_authorization', 'unknown', 'other_source_explanation'],
            'source_name': self.f.lookup(oid).nodes.get(cell['root'], {}).get('name') if cell else None,
            'related_uses': [self.f.operations[o]['function'] for o in q['binding']['operations']],
            'answer_contract': 'question + answer + short basis; existing entity is already bound; no risk/AST/SMT required'}
        self.questions[sid] = row
        if kind=='financial_consent':
            row.update(question='For this actual holder-issued authorization and dependent request, what quantity does the holder authorize? Explain whether it bounds the final holder debit including fees, or authorizes the checked net request with its disclosed fee rule; preserve the holder, ordered keys, amount, use and phase. A difference between gross and net alone does not decide this policy.',
                choices=['gross_debit_bound','net_request_with_fee','unknown','other_source_explanation'])
        return row

    def consume_answer(self, answer, allowed, issues):
        sid = answer.get('question'); sq = self.questions.get(sid)
        if not sq or sid not in allowed:
            return None, 'semantic_answer_outside_sent_scope'
        text = str(answer.get('answer') or '').strip(); basis = str(answer.get('basis') or '').strip()
        if not text or not has_basis(basis): return None, 'semantic_answer_missing_explanation'
        q = issues.get(sq['issue'])
        if not q: return None, 'semantic_question_issue_missing'
        if q['binding'].get('core_operation')!=sq.get('core_operation'):
            return None,'semantic_answer_core_changed_since_sent'
        self.scope(q['current'])
        if self.active_scope!=sq['semantic_scope']:return None,'semantic_answer_scope_changed_since_sent'
        if sq['kind'] == 'resource':
            from .semantic_claims import resource_assertion
            assertion=resource_assertion(basis,answer=text)
            if text not in ('financial_right','token_ledger','redeemable_credit','nonfinancial_counter'):
                assertion=resource_assertion(text+' '+basis)
            if not assertion['meaning']: return None, 'semantic_meaning_or_explanation_polarity_unresolved'
            row = self._set(sq['operation'], sq['cell'], assertion['meaning'],
                            basis, q['id'], 'focused_model_answer', q['binding']['operations'],assertion)
            return row, None if row else 'semantic_entity_or_source_effect_not_supported'
        if sq['kind']=='financial_consent':
            if text not in ('gross_debit_bound','net_request_with_fee','unknown'):
                return None,'financial_consent_meaning_unresolved'
            if not sq.get('quantity_scope') or sq['operation'] not in self.f.operations:
                return None,'financial_consent_source_quantity_not_bound'
            row={'id':'consent_'+digest([sq,answer])[:20],'meaning':text,'basis':basis,
                'issue':q['id'],'operation':sq['operation'],'target':sq['target'],'family':family(sq['cell']),
                'quantity_scope':copy.deepcopy(sq['quantity_scope']),'scope':copy.deepcopy(self.active_scope),
                'operations':sorted(set(q['binding']['operations'])|{sq['operation']}),
                'source':'focused_source_bound_semantic_answer','evidence_level':'H',
                'business_policy_formally_proved':False,'original_answer':copy.deepcopy(answer)}
            token=key([sq['target'],sq['operation'],family(sq['cell']),self.active_scope])
            previous=self.consents.get(token);self.consents[token]=row;self.version+=1
            self.history.append({'before':copy.deepcopy(previous),'after':copy.deepcopy(row),
                'derived_cache_invalidation':'dependent quantity properties; other policies unchanged',
                'frozen_initial_state_unchanged':True})
            return row,None
        from .relations import statement
        interpretation = statement(basis + ' ' + text, choice=text)
        row = {'id': 'auth_' + digest([sq, answer])[:20], 'meaning': interpretation['meaning'],
               'text': basis + ' ' + text, 'polarity': interpretation['polarity'],
               'original_answer': copy.deepcopy(answer),
            'basis': basis, 'issue': q['id'], 'operation': sq['operation'],
            'source': 'focused_model_answer', 'target': sq['target'],
            'evidence_level': 'source_and_semantic_prediction'}
        return row, None

    def record(self):
        return {'version': self.version, 'resources': list(self.resources.values()),
                'financial_consents':list(self.consents.values()),
                'questions': list(self.questions.values()), 'history': self.history,
                'initial_state_modified_by_semantics': False}

~~~~

## file-daff5e867dd978

`source/src/pr_next_joint/reporting/__init__.py` · 原字节 SHA-256 `87e3e2f1dba261e0999d37d622e45825e4d2763d9091aa860663f27df53e5d17`

~~~~python
"""Source analysis helpers retained by SCRV."""

~~~~

## file-39b8903e248ed8

`source/src/pr_next_joint/reporting/effective_parameters.py` · 原字节 SHA-256 `0124532d4bc73117bc5289fbef053be6407f7031e03a9246b61856ff9da3b0c3`

~~~~python
"""Versioned finite limits; no sample-specific overrides."""
import json
from importlib.resources import files
from functools import lru_cache
@lru_cache(maxsize=1)
def current():
    data=json.loads(files('pr_next_joint').joinpath('resources/method_evidence.r1.json').read_text(encoding='utf8'))
    v=data['effective_parameters'];assert v['normalization_visits_per_operation_max'] in (100000,150000,200000)
    assert v['max_source_paths']==data['P']['max_source_paths']
    fixed={'expression_nodes_max':50000,'expression_depth_max':100,'expression_string_bytes_max':1048576,
        'expression_key_characters_max':262144,'source_evaluations_per_operation_max':2048,'call_depth_max':8,
        'solver_timeout_ms':3000,'variable_loop_frontier':2,'constant_loop_max':32}
    assert all(v[k]==x for k,x in fixed.items()),'UNVALIDATED_FINITE_PARAMETER_CHANGE'
    return {**v,'solver_timeout_upgrade_ms':10000,'solver_sample_seconds':120,'external_sequence_max':3,'dependency_closure_nodes_max':4096,'sequence_checks_per_sample_max':24,'sequence_paths_per_stage_max':8}

~~~~

## file-c6dd904591336b

`source/src/pr_next_joint/resources/method_evidence.r1.json` · 原字节 SHA-256 `c906e1486ec2603ce7d43e7f41232df6d123036279e7b4aff481fe6663d6a34d`

~~~~text
{
  "schema": "method-evidence-profile-r1",
  "approval": "PR_NEXT_METHOD_REQUIREMENTS_AMENDMENT_20261022_R1",
  "report_schema": "m03-p-report-v2",
  "rules": [
    {
      "id": "AC-01",
      "name_cn": "缺少或绕过授权保护",
      "P": "implemented_bounded",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "适用策略禁止该主体且成功产生受保护效果",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "implementation_scope": "bounded source permissions, program relationship candidates and selective SMT implication; preserves disjunctive authority, callback/caller context; arbitrary dynamic self-calls remain a gap; independently referenced native payout and selfdestruct native disposition; opaque delegatecall effect retained unknown",
      "qualification_scope": "compiler/model engineering contrasts only; new real-pilot performance pending",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof"
    },
    {
      "id": "AC-02",
      "name_cn": "权限状态与管理流程被不当控制",
      "P": "implemented_bounded",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "不具管理资格的受控主体非法修改权限并取得控制",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "implementation_scope": "source-bound role management, scoped grants, bulk-key qualification, nomination and actual successor binding; proxy upgrades and opaque policy modules remain gaps",
      "qualification_scope": "compiler/model engineering contrasts only; new real-pilot performance pending",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof"
    },
    {
      "id": "AC-03",
      "name_cn": "身份资源作用对象错配",
      "P": "implemented_bounded",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "被检查凭据与实际作用对象不匹配且无合法委托",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "implementation_scope": "source resource/subject/delegation/alias and conditionally source-typed read-call relations; unknown proxies and business action-bit interpretation remain gaps",
      "qualification_scope": "compiler/model engineering contrasts only; new real-pilot performance pending",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof"
    },
    {
      "id": "AC-04",
      "name_cn": "条件和生命周期过宽",
      "P": "implemented_bounded",
      "implementation_scope": "same-record boolean validity; issued future expiry and ordered timestamps; epoch snapshots; controlled per-subject additive usage quotas; same-manager enumeration phase exit with persistent issued credential. Arbitrary reopening protocols, nonlinear consumption and cross-contract lifecycles remain gaps",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "撤销/过期/未生效凭据仍被接受并产生效果",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "qualification_scope": "compiler/model engineering contrasts only; new real-pilot performance pending",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof"
    },
    {
      "id": "AC-05",
      "name_cn": "签名凭据使用错误",
      "P": "implemented_bounded",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "合法来源凭据被错误重放或跨域/主体/资源使用，或明确坏签名被接受",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "qualification_scope": "compiler/model engineering contrasts only; new real-pilot performance pending",
      "implementation_scope": "source-bound credential replay/domain/subject/resource/validity models; ordinary random hash excluded; opaque validators retain decisive gaps",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof"
    },
    {
      "id": "FCR-TRANSFER",
      "name_cn": "任意转移",
      "P": "implemented_bounded",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "源码中的特权他人资产/账本权益处分机制，核查持有人同意",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "definition_revision": "fcr-mechanism-r1-20261027",
      "feasibility_reporting": "separate; source mechanism does not prove actual funded exploitability",
      "qualification_scope": "compiler/model engineering contrasts only; new real-pilot performance pending",
      "implementation_scope": "bounded asset/transferable-ledger model, explicit amount consumption, independent privilege and source holder consent; arbitrary compensation and opaque cross-contract assets remain unknown",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof"
    },
    {
      "id": "FCR-MINT",
      "name_cn": "任意增发",
      "P": "implemented_bounded",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "源码中的特权资产或可转移账本权益创建机制",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "implementation_scope": "source-bound native redeemable additive ledgers and exact floor proportional native shares; direct privilege and consumed issuance allowance; bounded administrator-set backing multiplier and same-holder scaled reward-index checkpoint; distinguish equal-value native deposits, correctly priced share deposits and same-holder equal-unit conversion. Record-based notes, cross-contract asset ledgers, arbitrary nonlinear arithmetic and solvency remain gaps; scalar getter-linked migration and holder/face/liability-bound redeemable records; complex cross-contract ledgers and proof-controlled issuance remain gaps",
      "definition_revision": "fcr-mechanism-r1-20261027",
      "feasibility_reporting": "separate; source mechanism does not prove actual funded exploitability",
      "qualification_scope": "compiler/model engineering contrasts only; new real-pilot performance pending",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof"
    },
    {
      "id": "FCR-DESTROY",
      "name_cn": "任意销毁",
      "P": "implemented_bounded",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "特权消减或销毁他人资产权益或可定位主体与数量的抽象账户账本；排除有效同意与已匹配守恒转换",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "definition_revision": "v20-approved-abstract-account-ledger",
      "feasibility_reporting": "separate; source mechanism does not prove actual funded exploitability",
      "qualification_scope": "financial and abstract account mechanisms distinguished; conditional positive prestate not deployment proof",
      "implementation_scope": "bounded asset/transferable-ledger model, explicit amount consumption, independent privilege and source holder consent; arbitrary compensation and opaque cross-contract assets remain unknown",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof",
      "rollback_profile": "strict_financial changes this branch only"
    },
    {
      "id": "FCR-PAUSE",
      "name_cn": "暂停转移",
      "P": "implemented_bounded",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "源码中的特权普通转移阻断机制，声明入口与例外",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "definition_revision": "fcr-mechanism-r1-20261027",
      "feasibility_reporting": "separate; source mechanism does not prove actual funded exploitability",
      "qualification_scope": "compiler/model engineering contrasts only; new real-pilot performance pending",
      "implementation_scope": "same ordinary holder request under privileged control transition, with entry/holder/exception scope; pure issuance/burn excluded from transfer pairing; admin-only service not main FREEZE",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof"
    },
    {
      "id": "FCR-FREEZE",
      "name_cn": "冻结账户",
      "P": "implemented_bounded",
      "M": "implemented_bounded_source_models_engineering_verified",
      "E": "not_executed_in_v7_no_uniform_requirement",
      "main_target": "源码中的特权指定持有人转出阻断机制，声明对象与例外",
      "evidence_requirement": "applicable program-based rule conditions through P/M/E, no uniform E prerequisite",
      "report_scope": "conditional prediction, not whole-program safety",
      "definition_revision": "fcr-mechanism-r1-20261027",
      "feasibility_reporting": "separate; source mechanism does not prove actual funded exploitability",
      "qualification_scope": "compiler/model engineering contrasts only; new real-pilot performance pending",
      "implementation_scope": "same ordinary holder request under privileged control transition, with entry/holder/exception scope; pure issuance/burn excluded from transfer pairing; admin-only service not main FREEZE",
      "P_detail": "source-bound candidates/checks and operation-scoped necessary-condition exclusions; no whole-program proof"
    }
  ],
  "P": {
    "max_source_paths": 48,
    "required": [
      "program_id",
      "build_id",
      "rule",
      "function",
      "required_policy_candidate",
      "effect",
      "conditions",
      "status",
      "route"
    ],
    "forbidden_claims": [
      "actual_execution",
      "whole_program_safety",
      "business_intention_proven"
    ],
    "no_execution_required": true,
    "analyzer": "compiler-source-declaration-and-path-relations",
    "source_loop_scope": "for-loop source expansion 0..2 complete iterations; longer continuation explicit named gap; not whole-loop proof"
  },
  "conditional_fields": {
    "P": [
      "source_identity",
      "analyzer",
      "policy_basis",
      "scope"
    ],
    "M": [
      "model_identity",
      "bounds",
      "approximations"
    ],
    "E": [
      "runtime_identity",
      "execution_plan",
      "backend_identity",
      "actual_execution",
      "replay_when_required"
    ]
  },
  "acceptance": {
    "three_structures": [
      "global_address",
      "per_object_owner",
      "role_membership"
    ],
    "real_analysis_and_synthetic_separated": true,
    "no_name_only_matching": true,
    "no_raw_sat_or_llm_self_certification": true,
    "local_effect_sufficient": true,
    "unknown_not_safe": true,
    "cases_200_all_actual_analysis_not_all_dynamic": true,
    "fixed_normal_risk_ratio_or_zero_errors": false
  },
  "version_boundary": "Task B/C2 originals and prior reports unchanged; only new analysis uses this profile",
  "implementation_revision": "joint-operation-scoped-r1-rq1-v7-20261028",
  "project_input": {
    "mode": "P --targets project",
    "targets": "all concrete compiled contracts; each analyzed in separate storage context",
    "entry_optional_in_project_mode": true,
    "unresolved_external_wiring": "retained, not inferred",
    "compiler_scope": "0.8.20 development input; arbitrary build systems/versions not added"
  },
  "m04_relations_r2": {
    "shared_consumer": true,
    "source_labels_or_case_ids_used": false,
    "hash_terms": "ordered typed encoding, no inversion; dynamic packed encoding unsupported",
    "casts": "unsigned narrowing preserved, erased only when source bound establishes identity",
    "unresolved_controls": "named inconclusive, not public-entry safety",
    "dynamic_execution": "not_required_for_P_and_not_claimed"
  },
  "m04_assets_lifecycle_r3": {
    "proportional_model": "exact structural floor expression, no reassociation or rational cancellation",
    "controlled_arithmetic": "bounded multiplier or same-holder scaled index delta; positive rounded reward explicitly conditional",
    "phase_and_expiry": "program-inferred policy; original definitions unchanged",
    "evidence_route": "P, no new compiler/native/API/EVM"
  },
  "local_tools": {
    "relationship_graph": "networkx 3.4.2",
    "permission_predicates": "z3-solver 4.15.3.0",
    "route": "P",
    "scope": "source predicate checks under declared pre-state; no EVM execution or whole-program reachability"
  },
  "definition_revisions": {
    "FCR": "fcr-mechanism-r1-20261027",
    "AC": "ac-five-directions-r1-20261028"
  },
  "v7_scope": {
    "AC04D_removed": true,
    "active_ac_rules": [
      "AC-01",
      "AC-02",
      "AC-03",
      "AC-04",
      "AC-05"
    ],
    "constant_loop_max": 32,
    "variable_loop_frontier": 2,
    "all_unmodeled_semantics": "decisive local unknown, never safety",
    "real_pilot_status": "not_started",
    "source_evaluations_per_operation_max": 2048,
    "expression_nodes_max": 50000,
    "expression_depth_max": 100,
    "expression_string_bytes_max": 1048576,
    "expression_key_characters_max": 262144
  },
  "effective_parameters": {
    "normalization_visits_per_operation_max": 150000,
    "max_source_paths": 48,
    "expression_nodes_max": 50000,
    "expression_depth_max": 100,
    "expression_string_bytes_max": 1048576,
    "expression_key_characters_max": 262144,
    "source_evaluations_per_operation_max": 2048,
    "call_depth_max": 8,
    "solver_timeout_ms": 3000,
    "variable_loop_frontier": 2,
    "constant_loop_max": 32,
    "fcr_execution_environment": "janus_comparison_pre_eip_6780",
    "arithmetic_query_scope": "explicit nonwrapping uint256 subcases; typed narrow/signed arithmetic encoded separately"
  },
  "current_approved_revision": "joint-concentrated-redesign-rq1-v20-20261031",
  "v20_authorization": "user approved V20_CONCENTRATED_REDESIGN_PLAN_R1_CN and subsequent execution",
  "v20_limits": {
    "maximum_external_operations": 3,
    "sequence_checks_per_sample": 24,
    "composition_paths_per_stage": 8,
    "solver_initial_ms": 3000,
    "solver_one_upgrade_ms": 10000,
    "solver_total_seconds": 120,
    "source_dependency_closure_nodes": 4096
  },
  "v20_scope_notes": {
    "other_FCR_definitions_unchanged": true,
    "LLM_final_classification": false,
    "LLM_formulas": false,
    "default_semantic_followup": 0,
    "additional_training": false
  }
}

~~~~

## file-40ca6dd77df245

`source/src/pr_next_joint/runtime/__init__.py` · 原字节 SHA-256 `87e3e2f1dba261e0999d37d622e45825e4d2763d9091aa860663f27df53e5d17`

~~~~python
"""Source analysis helpers retained by SCRV."""

~~~~

## file-60203347ecdbdd

`source/src/pr_next_joint/runtime/immutable.py` · 原字节 SHA-256 `7170290a5ac58d0ab7a95e229813744025997c44c372130b511f2b58810fa2dd`

~~~~python
"""Enrich an old compiler artifact only from identical creation code, runtime and complete metadata."""
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

from pr_next_joint.frontend.facts import walk


def restore(bundle, standard, original):
    if not any(n.get("mutability")=="immutable" for a in bundle.get("ast_sources",{}).values() for n in walk(a)):
        return None
    rows=[c for c in bundle["contracts"] if c.get("runtime") and not c.get("immutable_references")]
    if not rows:
        return None
    trusted=os.environ.get("PRNEXT_IMMUTABLE_SOLC_DIR")
    record={"state":"not_reconstructed","invocations":0,"targets":[]}
    if not trusted:
        return {**record,"reason":"local_trusted_compiler_directory_not_configured"}
    version=(rows[0].get("metadata") or {}).get("compiler",{}).get("version","")
    if not re.fullmatch(r"\d+\.\d+\.\d+\+commit\.[0-9A-Fa-f]{8}",version):
        return {**record,"reason":"full_compiler_version_not_available"}
    root=Path(trusted).resolve()
    names=("solc-windows-amd64-v"+version+".exe","solc-linux-amd64-v"+version,"solc-"+version.split("+")[0])
    compiler=next((root/n for n in names if (root/n).is_file() and (root/n).resolve().parent==root),None)
    if not compiler:
        return {**record,"reason":"matching_compiler_not_installed"}
    source=copy.deepcopy(standard)
    selection=source["settings"].setdefault("outputSelection",{}).setdefault("*",{}).setdefault("*",[])
    for key in ("evm.bytecode.object","evm.deployedBytecode.object","metadata","evm.deployedBytecode.immutableReferences"):
        if key not in selection:selection.append(key)
    record["invocations"]=1
    try:
        run=subprocess.run([str(compiler),"--standard-json"],input=json.dumps(source).encode(),capture_output=True,timeout=60,check=True)
        generated=json.loads(run.stdout)["contracts"]
        certificate=hashlib.sha256(compiler.read_bytes()).hexdigest()
        for c in rows:
            old=original["contracts"][c["file"]][c["name"]]
            new=generated[c["file"]][c["name"]]
            if new["metadata"]!=old["metadata"] or any(new["evm"][k]["object"]!=old["evm"][k]["object"] for k in ("bytecode","deployedBytecode")):
                continue
            ranges=new["evm"]["deployedBytecode"].get("immutableReferences",{})
            if ranges and all(isinstance(p.get("start"),int) and isinstance(p.get("length"),int)
                         and 0 <= p["start"] < p["start"]+p["length"] <= len(c["runtime"])//2 for v in ranges.values() for p in v):
                c["immutable_references"]=ranges
                record["targets"].append({"target":c["file"]+":"+c["name"],"locations":ranges})
        return {**record,"state":"certified" if record["targets"] else "no_matching_ranges",
                "compiler":version,"compiler_binary_sha256":certificate}
    except (OSError,subprocess.SubprocessError,ValueError,KeyError) as error:
        return {**record,"reason":"local_reconstruction_unavailable","exception":type(error).__name__}

~~~~

## file-db9e4d34622579

`source/src/pr_next_joint/verification/__init__.py` · 原字节 SHA-256 `87e3e2f1dba261e0999d37d622e45825e4d2763d9091aa860663f27df53e5d17`

~~~~python
"""Source analysis helpers retained by SCRV."""

~~~~
