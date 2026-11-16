"""Tolerant local normalization. The model never supplies AST, SMT or host identity."""
import copy,json,re,time
from pr_next_joint.core import digest
from .contracts import VERSION,ident,write
from .decision_output import receipt as body_receipt,context_summary,diagnostic

ANSWER_CHOICES = {
    'resource': ('financial_right', 'nonfinancial_counter', 'other_source_explanation', 'unknown'),
    'authorization': ('required_authorization', 'normal_authorization', 'other_source_explanation', 'unknown'),
    'financial_consent': ('gross_debit_bound', 'net_request_with_fee', 'other_source_explanation', 'unknown'),
}
AMOUNT_ROLES = ('original_request','request','gross_debit','debit','net_receipt','net','compensation')
STAGE_GUIDANCE = 'initialization_stage requires subject (its source stage flag).'
AMOUNT_GUIDANCE = 'amount_role requires role: ' + '/'.join(AMOUNT_ROLES) + '.'


def role_error(row, meaning, inherited=None):
    if 'role' not in row:
        return 'field_absent' if meaning=='amount_role' and inherited not in AMOUNT_ROLES else None
    if not isinstance(row['role'],str):return 'wrong_field_type'
    if row['role'] not in AMOUNT_ROLES:return 'outside_facet_vocabulary'
    return None


REVISION_ACTIONS = ('confirm', 'correct', 'narrow', 'withdraw')
REVISION_GUIDANCE = 'Use the shown support ref in its original facet, with action ' + '/'.join(REVISION_ACTIONS) + ' and a short reason for any change.'
INSTRUCTION = 'Read the displayed source for the actual target. Return one JSON object. Keep actors, ordered grants, phase and units distinct. No concrete actors, arguments, sequences or private reasoning.'

def instruction(task, recovery=False, *, kind=None, annotation_revision=False, policy_revision=False):
    common = INSTRUCTION
    if kind == 'scoped_support_dispute':
        return common + ' ' + REVISION_GUIDANCE + (' ' + AMOUNT_GUIDANCE if annotation_revision else '') + (' ' + STAGE_GUIDANCE if policy_revision else '')
    if kind in ANSWER_CHOICES:
        return common + ' Reply with answers[{question,answer,basis}] for the displayed question, using its choices and a brief source-based reason.' + (' A shown annotation may be revised by ref. ' + AMOUNT_GUIDANCE if annotation_revision else '') + (' ' + STAGE_GUIDANCE if policy_revision else '')
    if kind == 'local_effect':
        return common+' For the displayed effect answer issues[{effect,assessment,claim}]. Compare the applicable duty with who decides; give the actual local reason once.'
    if kind == 'issue':
        return common + ' Revise the displayed issue only. Cite its anchor, new evidence, assessment (risk, normal or investigate) and short reason.'
    meanings = sorted(ANNOTATIONS - (set() if task == 'FCR' else {'price','fee_rule','amount_role','transfer_condition'}))
    policies = sorted(POLICIES - (set() if task == 'FCR' else {'gross_debit_bound','net_request_with_fee'}))
    issue='Use issues[{effect or anchors,assessment,claim,policy_basis?,normal_explanation?}]. Give a short scoped comparison; assessment is risk, normal or investigate.'
    direction=('AC: state the applicable duty, who actually controls the effect and whether they conflict.' if task=='AC' else 'FCR: distinguish unit, holder consent, compensation and productive bypass; category is optional.')
    return ' '.join((common,direction,issue,'Alternatively use annotations[{on,meaning,basis}] or policies[{effect,meaning,basis,subject?}] once.',
        'Annotations: '+', '.join(meanings)+'. Policies: '+', '.join(policies)+'.',
        AMOUNT_GUIDANCE if 'amount_role' in meanings else '',STAGE_GUIDANCE,
        'For a scoped empty reading use task_analysis {task,anchors,basis}.' if not recovery else 'Correct the malformed reply using this source.'))

def question_entity(question):
    return digest([question.get(k) for k in ('id','operation','target','kind','cell','semantic_scope','core_operation','quantity_scope')])

def revision_support(item,previous,available):
    """Locate a model-supplied reason; never synthesize its business explanation.

    available is the actual new evidence sent for this issue. Exact probe IDs
    identify their containing evidence without making the model repeat labels.
    """
    texts=[item[k] for k in ('claim','revision_reason','reason','explanation')
           if isinstance(item.get(k),str)]
    refs=item.get('evidence',[])
    if isinstance(refs,str):refs=[refs]
    if not isinstance(refs,list):refs=[]
    locators={x for x in refs if isinstance(x,str)}
    for text in texts:locators.update(re.findall(r'\b(?:E\d+|probe_[a-f0-9]{20})\b',text))
    cited=set();matches=[]
    for label,record in available.items():
        ids={q['id'] for group in ('queries','holder_consent_counterexamples')
             for q in record.get(group,[]) if isinstance(q,dict) and q.get('id')}
        found=locators & ({label}|ids)
        if found:cited.add(label);matches.extend({'locator':x,'evidence':label} for x in sorted(found))
    reason=next((item[k].strip() for k in ('revision_reason','reason','explanation')
                 if isinstance(item.get(k),str) and item[k].strip()),None)
    if reason is None and isinstance(item.get('claim'),str) and item['claim'].strip()!=previous.get('claim','').strip():
        reason=item['claim'].strip()
    if reason and not re.sub(r'\b(?:E\d+|probe_[a-f0-9]{20})\b|[\W_]+','',reason):reason=None
    return sorted(cited),reason,matches


def category_value(category, task=None):
    """Finite spelling normalization, never infer a financial class from an action."""
    if category is None and task == 'AC':
        return 'AC'
    if not isinstance(category, str):
        return category
    token = re.sub(r'[\s_-]+', '-', category.strip().upper())
    if token in ('AC', 'ACCESS-CONTROL', 'ACCESS-CONTROL-VULNERABILITY'):
        return 'AC'
    # Permission/authorization is a single-task alias, not a rule classifying arbitrary prose.
    if task == 'AC' and (token in ('PERMISSION', 'AUTHORIZATION', 'AUTHORISATION') or
                         token.startswith(('ACCESS-CONTROL/', 'AUTHORIZATION/', 'AUTHORISATION/'))):
        return 'AC'
    names = ('TRANSFER', 'MINT', 'DESTROY', 'PAUSE', 'FREEZE')
    if token in names or token in tuple('FCR-' + n for n in names):
        return token if token.startswith('FCR-') else 'FCR-' + token
    m = re.fullmatch(r'FCR[/:]\s*(TRANSFER|MINT|DESTROY|PAUSE|FREEZE)|(TRANSFER|MINT|DESTROY|PAUSE|FREEZE)-?\(FCR\)', token)
    if m:return 'FCR-' + (m[1] or m[2])
    names_in_label=[n for n in names if re.search(r'(?<![A-Z])'+n+r'(?![A-Z])',token)]
    tagged=re.match(r'^FCR[-:/]-?(TRANSFER|MINT|DESTROY|PAUSE|FREEZE)(?:$|[-:/])',token)
    # An explicit namespace/class followed by explanation stays that class;
    # a multi-class label is still unresolved, not split into invented findings.
    return 'FCR-'+tagged[1] if tagged and names_in_label==[tagged[1]] else category


def normal_alternative(item):
    """Return only model-supplied original-program interpretation, with provenance."""
    obs = item.get('observation'); obs = obs if isinstance(obs, dict) else {}
    text = next((v.strip() for v in (item.get('alternative'), item.get('normal_explanation'),
                                    obs.get('normal_explanation')) if isinstance(v, str) and v.strip()), None)
    origin = 'explicit_field'
    if text is None:
        match = re.search(r'(?:relevant\s+)?normal (?:alternative|explanation)\s*:\s*(.+)', item.get('claim', ''), re.I | re.S)
        if match:
            text = match[1].strip(); origin = 'explicit_inline_claim'
    if text is None:
        return {'text': None, 'status': 'not_supplied', 'origin': None}
    hypothetical = re.search(r'\bif\b[^.!?]{0,180}\b(?:were (?:guarded|restricted|added)|had been (?:guarded|set|initialized)|guard were added)\b|'
                             r'\b(?:add|insert|introduce) (?:an? |the )?(?:guard|require|modifier)\b', text, re.I)
    return {'text': text, 'origin': origin,
            'status': 'counterfactual_program_not_normal_path' if hypothetical else 'supplied_not_program_proved'}


def semantic_direction(item, task, source_unrestricted=False):
    """Check a prediction for explicit task contradictions, not discover business risks.

    No missing controller field is required. Source checks can corroborate an explicitly
    ordinary-caller claim; public syntax alone never excludes a privileged branch.
    """
    # A competing, not-yet-accepted normal explanation is not the model's risk assertion.
    text = re.split(r'(?:relevant\s+)?normal (?:alternative|explanation)\s*:', item.get('claim', ''),
                    maxsplit=1, flags=re.I)[0]
    cat = item.get('category'); assessment = item.get('assessment')
    result = {'status': 'no_explicit_conflict', 'reasons': [], 'source_unrestricted': source_unrestricted}
    if task != 'FCR':
        return result
    outside = re.search(r'\b(?:ordinary (?:reentrancy |unprivileged )?attack|non[- ]FCR|not (?:an? |a privileged )?FCR|'
                        r'not a privileged (?:financial )?(?:risk|FCR))\b', text + ' ' + str(cat), re.I)
    no_controller = re.search(r'\b(?:no (?:actual )?privileged controller|attacker is not (?:an? )?privileged|'
                              r'not an? FCR by an actual privileged controller|no (?:normal|real|non-zero) account can (?:call|invoke))\b', text, re.I)
    anycaller = re.search(r'\bany (?:external )?(?:caller|requester|msg\.sender|account)\b', text, re.I)
    ordinary = item.get('risk_direction') in ('ordinary_exploit', 'unprivileged_attack')
    if assessment == 'risk' and (outside or no_controller or ordinary or anycaller and source_unrestricted):
        result.update(status='inconsistent_task_direction', reasons=['ordinary_attack_or_no_privileged_FCR_controller'])
    # Explicit non-task clues remain recorded without poisoning all five task categories.
    if cat not in ('FCR-TRANSFER', 'FCR-MINT', 'FCR-DESTROY', 'FCR-PAUSE', 'FCR-FREEZE') and (outside or no_controller):
        result.update(status='explicit_out_of_task_clue', reasons=['model_explicitly_distinguishes_non_FCR'])
    return result


def category_scope(item, task):
    """Coverage only: a disjunctive label stays unresolved within its named classes."""
    if task == 'AC':
        return ['AC']
    cat = item.get('category')
    if cat in ('FCR-TRANSFER', 'FCR-MINT', 'FCR-DESTROY', 'FCR-PAUSE', 'FCR-FREEZE'):
        return [cat]
    token = str(cat or '').upper()
    named = sorted({'FCR-' + c for c in ('TRANSFER', 'MINT', 'DESTROY', 'PAUSE', 'FREEZE')
                    if re.search(r'(?<![A-Z])' + c + r'(?![A-Z])', token)})
    return named  # Unscoped dependencies are resolved from actual source in coverage.py.

TOP_LISTS = frozenset(('annotations','policies','issues','answers','reviewed'))
WIRE_FIELDS = TOP_LISTS | {'task_analysis'}
ANNOTATIONS = frozenset(('management_role','eligibility_state','financial_right','nonfinancial_counter',
    'authorization_quantity','price','fee_rule','transfer_condition','amount_role','other_source_meaning','unknown'))
POLICIES = frozenset(('current_authority_required','holder_authorization_applies','initialization_stage',
    'gross_debit_bound','net_request_with_fee','other_source_policy','unknown'))


class AmbiguousKeys(dict):
    def __init__(self,pairs):
        super().__init__();self.duplicates=set()
        for name,val in pairs:
            if name in self:self.duplicates.add(name)
            self[name]=val


def wire_object(pairs):
    return AmbiguousKeys(pairs)


def ambiguous(value):
    if isinstance(value,AmbiguousKeys) and value.duplicates:return True
    if isinstance(value,list):return any(ambiguous(x) for x in value)
    if isinstance(value,dict):return any(ambiguous(x) for x in value.values())
    return False


def partial_envelope(text):
    decoder = json.JSONDecoder(object_pairs_hook=wire_object)
    size = len(text)
    def space(i):
        while i < size and text[i].isspace():
            i += 1
        return i
    i = space(1)
    value = {}
    seen = set()
    duplicates = set()
    if not text.startswith('{'):
        return {}, False
    while i < size:
        try:
            name, i = decoder.raw_decode(text, i)
        except ValueError:
            break
        i = space(i)
        if not isinstance(name, str) or i >= size or text[i] != ':':
            break
        if name in seen:
            duplicates.add(name)
        seen.add(name)
        i = space(i+1)
        if name in TOP_LISTS and i < size and text[i]=='[':
            rows = []
            value[name] = rows
            i = space(i+1)
            while i < size and text[i] != ']':
                try:
                    row, end = decoder.raw_decode(text,i)
                except ValueError:
                    break
                i = space(end)
                if i < size and text[i] not in ',]':
                    break
                rows.append(row)
                if i >= size or text[i] != ',':
                    break
                i = space(i+1)
            if i >= size or text[i] != ']':
                break
            i = space(i+1)
        else:
            try:
                part,end=decoder.raw_decode(text,i)
            except ValueError:
                break
            if name in WIRE_FIELDS:value[name]=part
            i=space(end)
        if i >= size or text[i] != ',':break
        i=space(i+1)
    for name in duplicates:value.pop(name,None)
    return value, bool(any(value.get(k) for k in WIRE_FIELDS))


def envelope_shape(raw):
    """Content-free structural diagnostic. Never return a key name or response text."""
    if not isinstance(raw,str):
        return {"root_type":"non_text","recognized_keys":0,"unknown_keys":0,"duplicate_keys":0}
    text=re.sub(r'^\x60\x60\x60(?:json)?\s*','',raw.strip(),flags=re.I)
    text=re.sub(r'\s*\x60\x60\x60$','',text)
    try:
        value=json.loads(text,object_pairs_hook=wire_object)
    except (ValueError,RecursionError):
        first=text[:1]
        return {"root_type":"incomplete_or_invalid_json","opening":"object" if first=='{' else "array" if first=='[' else "other",
                "recognized_keys":0,"unknown_keys":0,"duplicate_keys":0}
    if isinstance(value,dict):
        return {"root_type":"object","recognized_keys":len(WIRE_FIELDS.intersection(value)),
                "unknown_keys":len(set(value)-WIRE_FIELDS),
                "duplicate_keys":len(value.duplicates) if isinstance(value,AmbiguousKeys) else 0}
    return {"root_type":"array" if isinstance(value,list) else "scalar",
            "recognized_keys":0,"unknown_keys":0,"duplicate_keys":0}


def normalize(raw,task=None,*,phase='initial',sent_questions=()):
    """Parse one top-level envelope. Transport validity and semantic binding are independent."""
    diagnostics=[]
    def empty(kind, reason):
        return dict(issues=[],answers=[],annotations=[],policies=[],reviewed=[],usable_analysis=False,
                    response_kind=kind,diagnostics=[dict(d,stage=phase) for d in diagnostics]+[{'reason':reason,'stage':phase}])
    if raw is None or isinstance(raw,str) and not raw.strip():
        return empty('empty_body','empty_response_body')
    recovered=False
    if isinstance(raw,dict):
        value=copy.deepcopy(raw)
    elif isinstance(raw,str):
        text=re.sub(r'^\x60\x60\x60(?:json)?\s*','',raw.strip(),flags=re.I)
        text=re.sub(r'\s*\x60\x60\x60$','',text)
        try:value=json.loads(text,object_pairs_hook=wire_object)
        except (ValueError,RecursionError):
            try:completed,end=json.JSONDecoder().raw_decode(text)
            except (ValueError,RecursionError):pass
            else:
                if text[end:].strip():return empty('invalid_protocol','trailing_unrelated_content')
            value,recovered=partial_envelope(text)
            if not recovered:return empty('invalid_protocol','unparseable_top_level')
            diagnostics.append({'reason':'truncated_envelope_complete_items_only'})
    else:return empty('invalid_protocol','invalid_response_type')
    if isinstance(value,AmbiguousKeys) and value.duplicates:
        for name in value.duplicates:value.pop(name,None)
        diagnostics.append({'reason':'ambiguous_top_level_field'})
    if not isinstance(value,dict) or not WIRE_FIELDS.intersection(value):
        return empty('invalid_protocol','invalid_top_level_or_duplicate_key')
    # Never infer source or host authority from undeclared fields in a model row.
    bad=bool(diagnostics)
    had_content=False
    row_ordinals={}
    for field in TOP_LISTS:
        vals=value.get(field,[])
        if not isinstance(vals,list):
            diagnostics.append({'reason':field+'_not_list'});bad=True;vals=[]
        had_content|=bool(vals)
        valid=[]
        for idx,row in enumerate(vals):
            row_ordinals[(field,id(row))]=idx
            if ambiguous(row) or (isinstance(row,dict) and any(k.startswith('_') for k in row)):
                diagnostics.append({'reason':'duplicate_or_host_reserved_key','list':field,'index':idx});bad=True
            else:valid.append(row)
        value[field]=valid
    seeds={}
    located_amount_reads=[]
    for field,vocab,refkey in [('annotations',ANNOTATIONS,'on'),('policies',POLICIES,'effect')]:
        seeds[field]=[]
        for fallback,row in enumerate(value[field]):
            idx=row_ordinals.get((field,id(row)),fallback)
            if not isinstance(row,dict) or set(row)-{'id','on','effect','subject','scope','meaning','basis','ref','action','role'}:
                diagnostics.append({'reason':'invalid_seed_fields','list':field,'index':idx});bad=True;continue
            if ('effect' if field=='annotations' else 'on') in row:
                diagnostics.append({'reason':'wrong_semantic_locator_kind','list':field,'index':idx});bad=True;continue
            revision='ref' in row or 'action' in row
            action=row.get('action','add')
            located=bool(isinstance(row.get(refkey),str) and row[refkey].strip()) if not revision else (
                isinstance(action,str) and action in REVISION_ACTIONS and isinstance(row.get('ref'),str))
            meaning_ok=(revision and action in ('confirm','narrow','withdraw') and 'meaning' not in row or
                        isinstance(row.get('meaning'),str) and row['meaning'] in vocab)
            if not located or not meaning_ok or (action!='confirm' and not (isinstance(row.get('basis'),str) and row['basis'].strip())):
                missing = refkey if not located else 'meaning' if not meaning_ok else 'basis'
                raw_field = row.get(missing)
                diagnostics.append({'reason':'invalid_semantic_row','list':field,'index':idx,'field':missing,
                    'subreason':'field_absent' if raw_field is None else 'invalid_locator' if not located else 'outside_facet_vocabulary' if not meaning_ok else 'missing_source_reason',
                    'actual_type':type(raw_field).__name__,'value_length':len(raw_field) if isinstance(raw_field,str) else None,'value_sha256':digest(raw_field)})
                bad=True;continue
            if row.get('meaning')=='initialization_stage' and not (revision and 'subject' not in row) and not isinstance(row.get('subject'),str):
                actual=row.get('subject')
                diagnostics.append({'reason':'invalid_semantic_row','list':field,'index':idx,'field':'subject',
                    'subreason':'field_absent' if 'subject' not in row else 'wrong_field_type',
                    'actual_type':type(actual).__name__,'value_sha256':digest(actual)})
                bad=True;continue
            # A reply to a shown support can inherit its current role. Its
            # authenticated object and prior fact are checked by the consumer.
            issue=role_error(row,row.get('meaning')) if 'role' in row or not revision else None
            if issue:
                if field=='annotations' and row.get('meaning')=='amount_role' and not revision and not {'scope','subject'} & row.keys():
                    located_amount_reads.append(row[refkey])
                actual=row.get('role')
                diagnostics.append({'reason':'invalid_semantic_row','list':field,'index':idx,
                    'field':'role','subreason':issue,'actual_type':type(actual).__name__,
                    'value_length':len(actual) if isinstance(actual,str) else None,'value_sha256':digest(actual)})
                bad=True;continue
            bound=dict(row);seeds[field].append(bound)
            row_ordinals[(field,id(bound))]=idx
    answers=[]
    for index,row in enumerate(value.get('answers',[]) if isinstance(value.get('answers',[]),list) else []):
        index=row_ordinals.get(('answers',id(row)),index)
        if not isinstance(row,dict) or not all(isinstance(row.get(k),str) and row[k].strip() for k in ('question','answer','basis')):
            diagnostics.append({'answer':index,'reason':'semantic_answer_missing_question_answer_or_basis','original':row});continue
        if phase!='focused_revision' or row['question'] not in sent_questions:
            diagnostics.append({'list':'answers','index':index,'field':'question','reason':'semantic_answer_outside_sent_scope'})
            continue
        answers.append(copy.deepcopy(row))
    issues=[];seen=set()
    for index,item in enumerate(value['issues']):
        index=row_ordinals.get(('issues',id(item)),index)
        if not isinstance(item,dict):diagnostics.append({'item':index,'reason':'issue_not_object'});continue
        claim=item.get('claim');anchors=item.get('anchors',[])
        if isinstance(anchors,str):anchors=[anchors]
        if not isinstance(claim,str) or not claim.strip() or not isinstance(anchors,list) or not (any(isinstance(x,str) and x.strip() for x in anchors) or isinstance(item.get('effect'),str) and item['effect'].strip()):
            diagnostics.append({'item':index,'reason':'missing_claim_or_source_anchor','original':item});continue
        identifier=item.get('id') if isinstance(item.get('id'),str) and item['id'].strip() else ident('issue',[claim,anchors,item.get('effect')])
        if identifier in seen:
            identifier=identifier+'_'+digest([index,item])[:8];diagnostics.append({'item':index,'reason':'duplicate_id_disambiguated'})
        seen.add(identifier)
        issue=copy.deepcopy(item);issue.update(id=identifier,claim=claim.strip(),anchors=[x.strip() for x in anchors if isinstance(x,str) and x.strip()])
        issue['_host_defaulted_fields']=[k for k in ('assessment','category') if k not in item or item.get(k) is None]
        cat=issue.get('category');normalized=category_value(cat,task)
        if normalized!=cat:
            issue['category']=normalized
            issue['_category_normalization']={'original':cat,'normalized':normalized,'basis':'finite task/spelling alias; no inferred financial class'}
        elif normalized is not None and normalized not in ('AC','FCR-TRANSFER','FCR-MINT','FCR-DESTROY','FCR-PAUSE','FCR-FREEZE'):
            diagnostics.append({'item':index,'issue':identifier,'reason':'category_ambiguous_or_outside_supported_task','original_category':cat})
        raw_assessment=issue.get('assessment')
        token=re.sub(r'[\s-]+','_',raw_assessment.strip().lower()) if isinstance(raw_assessment,str) else None
        aliases={'risk':'risk','confirmed_risk':'risk','risk_confirmed':'risk','vulnerable':'risk',
                 'normal':'normal','no_risk':'normal','not_vulnerable':'normal',
                 'investigate':'investigate','uncertain':'investigate','unknown':'investigate'}
        judgment=aliases.get(token);basis='explicit status vocabulary';problem=None
        # Bare "confirmed" is not itself a positive risk judgment. In
        # particular, a risk noun inside a negated sentence is not evidence
        # of affirmative polarity. Only finite explicit affirmative wording
        # is normalized; other prose stays unresolved with its original text.
        # Old confirmations can carry an explicit proposition. Negation of
        # authorization is different from negation of the risk proposition.
        negative_head = re.match(r'^\s*(?:(?:this|that|there)\s+is\s+)?(?:not (?:a |an )?|no )(?:risk|vulnerabilit\w*|unauthorized access)\b',claim,re.I)
        positive_head = re.match(r'^\s*(?:this (?:is|poses|constitutes) (?:a |an )?(?:risk|vulnerability)|(?:the )?(?:caller|spender|requester|actor) (?:gains unauthorized access|lacks (?:applicable )?authorization)|(?:the )?(?:entry|function|operation) (?:does not check|fails to check|omits) (?:the )?(?:applicable|required|holder.s|incumbent.s) authorization)\b',claim,re.I)
        if token=='confirmed':
            if negative_head:judgment='normal'
            elif positive_head and normalized in ('AC','FCR-TRANSFER','FCR-MINT','FCR-DESTROY','FCR-PAUSE','FCR-FREEZE'):judgment='risk'
            else:problem='ambiguous_confirmation_not_a_risk_judgment'
        explicit_false=item.get('is_vulnerable') is False or item.get('risk') is False
        explicit_true=item.get('is_vulnerable') is True or item.get('risk') is True
        if (judgment=='risk' and (negative_head or explicit_false)) or (judgment=='normal' and explicit_true):
            problem='contradictory_explicit_judgment';judgment=None
        if judgment is None:
            judgment='investigate';problem=problem or ('missing_assessment' if raw_assessment is None else 'unknown_assessment_vocabulary')
            diagnostics.append({'item':index,'issue':identifier,'reason':problem,'original_assessment':raw_assessment,
                                'host_unresolved_not_model_choice':True})
        if raw_assessment!=judgment or problem:
            issue['_assessment_normalization']={'original':raw_assessment,'normalized':judgment,'basis':basis if not problem else problem,
                                               'host_unresolved_not_model_choice':bool(problem)}
        issue['assessment']=judgment
        issues.append(issue)
    reviewed=value.get('reviewed',[])
    if not isinstance(reviewed,list):diagnostics.append({'reason':'reviewed_not_list'});reviewed=[]
    has_reading = isinstance(value.get('task_analysis'),dict) and not ambiguous(value['task_analysis']) and bool(value['task_analysis'].get('basis'))
    empty = not had_content and not recovered and not bad
    kind = 'substantive' if issues or answers or any(seeds.values()) or has_reading else 'explicit_empty' if empty else 'unbound_content' if had_content and not recovered else 'invalid_protocol'
    for row in diagnostics:
        row.setdefault('stage',phase)
        if 'item' in row:row.setdefault('list','issues')
        if 'answer' in row:row.setdefault('list','answers')
    positions={field:[row_ordinals[(field,id(seed))] for seed in entries] for field,entries in seeds.items()}
    return {**seeds,'located_amount_reads':located_amount_reads,'issues':issues,'answers':answers,'reviewed':[x for x in reviewed if isinstance(x,str)],
            'response_kind':kind,'usable_analysis':kind in ('substantive','explicit_empty'),
            'diagnostics':diagnostics,'row_positions':positions,'recovered_partial_envelope':recovered,'original_envelope':value}

class Session:
    def __init__(self,program,context,out,client):
        self.program,self.context,self.out,self.client=program,context,out,client
        self.attempts=[];self.model_wait_seconds=0.;self.submitted=0
        if hasattr(client,'program_identity') and client.program_identity is None:client.program_identity=program.identity
    def accounting(self):
        if hasattr(self.client,'accounting'):return self.client.accounting()
        return {'real_model_calls':0,'nature':'offline engineering fixture; not a real model experiment'}
    def is_simulated(self):return not bool(getattr(self.client,'live_authorized',False))
    def request(self,*,feedback=None,recovery=False,prepared=None):
        if len(self.attempts)>=self.program.options.attempt_limit:return None
        index=len(self.attempts);messages,manifest=prepared if prepared is not None else self.context.messages(feedback,recovery=recovery)
        if digest(messages)!=manifest['messages_sha256']:raise ValueError('prepared_message_identity_changed')
        row={'index':index,'phase':'protocol_recovery' if recovery else 'initial' if feedback is None else 'focused_revision',
             'messages_sha256':digest(messages),'input_tokens':manifest['input_tokens'],
             'output_limit':self.program.options.output_limit,'actual_model_submissions':0}
        write(self.out/f'request_receipt_{index}.json',{'host_identity':self.program.identity,**body_receipt(messages,'model_request'),'manifest':context_summary(manifest)})
        self.attempts.append(row)
        if manifest['input_tokens']>self.program.options.input_limit:
            row.update(status='not_sent',submission_state='not_dispatched',reason='complete_message_capacity_exceeded');write(self.out/f'attempt_{index}.json',row);return None
        started=time.monotonic()
        try:
            raw,receipt=self.client.call(messages,'semantic_initial' if index==0 else 'semantic_feedback',
              max_tokens=self.program.options.output_limit,thinking=True,reasoning_effort='high',timeout=1800)
            row['response_received']=True
            write(self.out/f'response_digest_{index}.json',{'content_sha256':digest(raw),'body_retained':False});write(self.out/f'receipt_{index}.json',receipt)
            if receipt.get('messages_sha256')!=digest(messages) or receipt.get('response_sha256')!=digest(raw):raise ValueError('bridge_response_identity')
            if receipt.get('program_identity')!=self.program.identity or receipt.get('case_id')!=self.client.case_id:raise ValueError('bridge_program_or_case_identity')
            simulated=receipt.get('simulated')
            if type(simulated)is not bool or not simulated and not getattr(self.client,'live_authorized',False):
                raise ValueError('fresh_runtime_authorization_required')
            row['response_identity_verified']=True
            value=normalize(raw,task=self.program.options.scope,phase=row['phase'],sent_questions=manifest.get('semantic_wire',{}))
            value['origin']='fixture' if simulated else 'verified_service'
            row['response_kind']=value['response_kind'];row['usable']=value['usable_analysis']
            write(self.out/f'normalization_receipt_{index}.json',{'response_kind':value['response_kind'],'normalized_sha256':digest(value),'issues':len(value['issues']),'answers':len(value['answers']),'usable_analysis':value['usable_analysis'],'body_retained':False,
                'envelope_shape':envelope_shape(raw) if not value['usable_analysis'] else None})
            row.update(status='analysis_received' if value['usable_analysis'] else 'protocol_diagnostic',
                       simulated=simulated,usage=receipt.get('usage'),cost_usd=receipt.get('cost_usd'),
                       cost_usd_upper=receipt.get('cost_usd_upper'),service_model=receipt.get('model'),
                       actual_model_submissions=receipt.get('actual_model_submissions',0),
                       normalization_diagnostics=[diagnostic(d) for d in value['diagnostics']])
            return value
        except Exception as error:
            row.update(status='transport_or_identity_error',reason=type(error).__name__,error_sha256=digest(str(error)));return None
        finally:
            if hasattr(self.client,'attempt_record'):
                row['dispatch_accounting']=self.client.attempt_record(index)
                row['actual_model_submissions']=row['dispatch_accounting'].get('actual_model_submissions',0)
            account=row.get('dispatch_accounting') or {}
            # A provider timeout after recording a possible submission is not a confirmed response.
            row['submission_state']=('fixture' if row.get('simulated') or account.get('simulated') else
                'possible' if account.get('state') in ('sent','unknown') and not row.get('response_received') else
                'submitted' if row.get('actual_model_submissions') else 'not_dispatched')
            self.model_wait_seconds+=time.monotonic()-started;write(self.out/f'attempt_{index}.json',row)
