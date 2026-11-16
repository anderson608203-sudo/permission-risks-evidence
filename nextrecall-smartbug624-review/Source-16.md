## source/src/pr_next_joint/investigation/selection.py

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

## source/src/pr_next_joint/investigation/semantic_claims.py

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
