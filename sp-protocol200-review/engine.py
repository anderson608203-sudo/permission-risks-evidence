"""Question-led source checks, scoped differential investigation and one revision."""
import copy,time,traceback,re
from pathlib import Path
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import lit
from pr_next_joint.verification.solver import budget
from .contracts import write,CATEGORIES
from .context import Catalog,SourceContext
from .graph import ProgramGraph
from .protocol import Session,revision_support,REVISION_GUIDANCE,normal_alternative,semantic_direction
from .behavior import Backend
from .report import build
from .selection import plan_observation
from .request_scope import coverage_facts, observation_applies, compare_relevant, privileged_intervention, linked_controls

class Investigation:
    def __init__(self,program,counter,out,client,deadline=None):
        prepared=time.monotonic()
        self.wall_origin=prepared
        self.f=program;self.out=Path(out);self.graph=ProgramGraph(program);self.catalog=Catalog(program,self.graph)
        self.context=SourceContext(program,self.catalog,counter);self.session=Session(program,self.context,self.out/'model',client)
        self.backend=Backend(program,self.catalog,self.graph);self.deadline=deadline
        from .summary import Semantics
        self.semantics=Semantics(program);self.backend.semantics=self.semantics
        self.issues={};self.initial_proposals={};self.actions=[];self.ready=[];self.shared_reads={};self.refinements=[];self.seen=set();self.evidence={};self.diagnostics=[]
        self.updates=[];self.call_decisions=[];self.model_analysis_available=False;self.explicit_empty_analysis=False
        self.usable_task_opinion=False;self.observed_feedback_ids={};self.task_declaration=None;self.program_seconds=0.;self.high_streak=0;self.order=0
        self.reading_declarations=[];self.initial_manifest=None
        self.program_seconds=time.monotonic()-prepared
        self.graph.frontier_deadline=min(prepared+program.options.seconds,deadline) if deadline else prepared+program.options.seconds
        self.coverage_gaps=[];self.feedback_trace=[];self.root_service={}
        self.backend.shared_remaining=self.program_remaining
        self.f.summaries.dependencies.remaining=self.program_remaining
        from .semantic_rules import ScopedRules
        self.semantics.rules=ScopedRules(self)
        self.context.rules=self.semantics.rules
    def program_remaining(self):
        elapsed=max(self.program_seconds,time.monotonic()-self.wall_origin-self.session.model_wait_seconds)
        remaining=max(0.0,self.f.options.seconds-elapsed)
        return min(remaining,max(0.0,self.deadline-time.monotonic())) if self.deadline else remaining
    def limit(self):
        if sum(not a.get('computation_reused',False) for a in self.actions)>=self.f.options.max_actions:return 'noncached_action_limit'
        if self.program_remaining()<=0:return 'program_investigation_seconds'
        if self.deadline and time.monotonic()>=self.deadline:return 'batch_deadline'
        return None
    def root(self,q):return q['binding'].get('core_operation')
    def _claim_scope(self,binding):
        # Explicit source references are a conservative set of possible claim
        # locations, NOT a list copied from a chosen probe or internal callers.
        ops={v[0] for v in binding['located'].values() if len(v)==1}
        if binding.get('core_exact'):ops.add(binding['core_operation'])
        return {'source_operations':sorted(ops),'basis':'claim source anchors and validated core, independent of next_check',
                'ambiguous_references':copy.deepcopy(binding['ambiguous']),
                'unresolved_references':copy.deepcopy(binding['unresolved']),
                'all_anchored_operations_are_affected_not_asserted':True}
    def _core_support(self,operation,cited):
        related=[]
        for label in cited:
            e=self.evidence[label]
            if e['kind']=='source_inspection' and e.get('operation')==operation:related.append(label)
            elif e['kind']=='state_sources' and operation in e.get('writers',[]):related.append(label)
            elif e['kind']=='causal_compare' and operation in (e.get('change'),e.get('observe')) and any(
                p.get('answer') in ('sat','unsat') for p in e.get('queries',[])):related.append(label)
        return related
    def task_conflict(self,item):
        cat=item.get('category')
        if item.get('_host_source_question') and cat is None:return False
        if cat=='ADDITIONAL' and self.f.options.scope=='FCR':return False
        wrong=cat not in CATEGORIES or (cat!='AC' if self.f.options.scope=='AC' else cat=='AC')
        return bool(wrong or self.f.options.scope=='FCR' and item.get('risk_direction') in ('ordinary_exploit','unprivileged_attack'))
    def _task_review(self,item,binding):
        # Reuse original guards to corroborate an explicit ordinary-caller claim.
        # This is a consistency check; no controller/asset is guessed or discovered.
        from pr_next_joint.frontend.path_ir import walk
        root=binding.get('core_operation');unrestricted=False
        if root is not None:
            paths=list(self.f.operation_paths(root))
            unrestricted=any(p.get('flow') in ('normal','returned') for _,p in paths) and not self.f.operations[root].get('gaps') and all(
                p.get('flow') in ('normal','returned','reverted') and not p.get('issues') and not p.get('evaluation_gaps')
                for _,p in paths) and all(not any(n.get('kind') in ('actual_sender','transaction_origin') or
                    n.get('kind')=='environment' and n.get('field')=='origin' for n in walk(p.get('guards',[])))
                    for _,p in paths if p.get('flow') in ('normal','returned'))
        review = semantic_direction(item,self.f.options.scope,unrestricted)
        if unrestricted and review['status'] == 'inconsistent_task_direction':
            # A public transaction can have a separate, source-located privileged intervention.
            # Disable only the "any caller" inference. Explicitly non-FCR assertions still conflict.
            scoped = semantic_direction(item,self.f.options.scope,False)
            links = privileged_intervention(self,binding,item) if scoped['status']=='no_explicit_conflict' else []
            if links:
                scoped.update(source_unrestricted=True, distinct_privileged_interventions=links)
                return scoped
        if self.f.options.scope=='FCR' and root and review['status']=='inconsistent_task_direction' and unrestricted:
            from .properties import interpret,stage
            req=interpret(item) or {}
            if req.get('measure') in ('ledger_receipt','ledger_debit','ledger_grant') and semantic_direction(item,'FCR',False)['status']=='no_explicit_conflict':
                candidates=[{'control':r['cell'],'writer':w['operation'],'use':root,'paths':w['role_guarded_paths']}
                    for r in stage(self,root) for w in r['runtime_writers'] if w['role_guarded_paths']]
                if len(candidates)==1:
                    return dict(semantic_direction(item,'FCR',False),source_unrestricted=True,distinct_privileged_interventions=candidates,
                                extent='runtime control source found; financial effect and consent require separate evidence')
        return review
    def _note_action(self, action, qid, operation, reason, fact=None, consumer=None):
        row={'action':action,'issue':qid,'operation':operation,'reason':reason}
        if fact:row['fact']=fact
        if consumer:row['consumer']=consumer
        self.refinements.append(row)

    def _share_inspection(self, qid, oid, priority, trigger):
        """An unenhanced inspection is a source fact; authorization annotations are per consumer."""
        q=self.issues[qid]
        fact=self.f.summaries.effect_fact_key(oid)
        entry=self.shared_reads.setdefault(fact,{'pending':set(),'result':None,'consumers':set(),'structural':self.f.summaries.structural_fact_key(oid)})
        entry['consumers'].add(qid)
        if entry['result'] is not None:
            self._attach_read(q,oid,fact,entry['result'])
            self._note_action('reuse',qid,oid,'existing_same_source_fact',fact)
            return
        if entry['pending']:
            entry['pending'].add(qid)
            self._note_action('join',qid,oid,'shared_prerequisite',fact)
            return
        entry['pending'].add(qid)
        self._enqueue(qid,'inspect',{'operation':oid,'enhance':False},priority,trigger)

    def _attach_read(self,q,oid,fact,result):
        if fact in q.setdefault('source_facts',{}):return
        entity=dict(result,shared_source_fact=fact)
        if q.get('host_source_candidate'):entity['applied_source_candidate']=q['host_source_candidate']
        if self.f.options.scope=='AC':
            from .authorization import acquisition_premise
            premise=acquisition_premise(self,q)
            if premise:entity['authorization_premise']=premise
        label=self._evidence(q,entity,{'id':'source_'+fact[:20]})
        q['source_facts'][fact]=label
        self._reuse_observation(q,entity,label)
        if (entity.get('authorization_premise') or entity.get('applied_source_candidate') or entity.get('no_committing_path')
                or entity.get('net_effect_proved_unchanged') or entity.get('settlements') or q.get('task_conflict')):
            q['novel'].append(label)
        if (entity.get('unknown_guard_paths') or entity.get('credential_paths')) and not entity.get('no_committing_path'):
            self.enqueue(q['id'],'inspect',{'operation':oid,'enhance':True},1,'source_dependency_requires_refinement')

    def _impact(self, q, action, args):
        from .source_opinion import scoped_opinion
        oid=args.get('operation') or args.get('observe') or self.root(q)
        if not oid:return None
        p=q.get('property') or {}
        if action=='inspect' and not args.get('enhance'):
            if oid in q['binding']['operations'] or oid in p.get('semantic_dependency_operations',[]) or oid in q.get('semantic_read_dependencies',()):
                return 'basic_source_read'
            return None
        if q.get('retired_property_parent'):return None
        relevant=set(p.get('semantic_dependency_operations',[]))|set(q['binding']['operations'])
        if oid not in relevant:return None
        if not q.get('source_facts'):return 'resolve_source_prerequisite'
        view=scoped_opinion(self,q)
        if view['status']=='excluded':return None
        if q.get('task_conflict') and q['current'].get('assessment')=='normal' and action=='prefix_search':
            return None
        if action=='sources' and view['status'] in ('risk','normal') and not q.get('task_conflict'):
            return None
        if q.get('semantic_recheck_property')==p.get('id') and p.get('id'):
            return 'changed_scope_requires_recheck'
        if args.get('enhance'):return 'critical_guard_or_source_effect'
        if action=='compare':
            measure=args.get('context',{}).get('observable',{}).get('measure')
            if view['status']=='normal' and view['reason'] in ('no_new_controlled_credit','parameter_only','intra_ledger_transfer','same_position_restored'):
                return None
            # Quantities, opposing evidence and authorization always keep an independent scoped check.
            return 'check_effect_or_refute_same_scope' if measure else 'distinguish_bound_interpretations'
        if view['status']=='risk' and not q['current'].get('alternative'):
            return None
        return 'joint_prerequisite' if action=='prefix_search' else 'distinguish_bound_interpretations'

    def enqueue(self,qid,action,arguments,priority=2,trigger=None):
        oid=arguments.get('operation') or arguments.get('observe')
        if action=='inspect' and not arguments.get('enhance'):
            if not self._impact(self.issues[qid],action,arguments):
                self._note_action('skip',qid,oid,'no_remaining_decision_impact')
                return
            self._share_inspection(qid,oid,priority,trigger)
            return
        impact=self._impact(self.issues[qid],action,arguments)
        if not impact:
            self._note_action('skip',qid,oid,'no_remaining_decision_impact')
            return
        self._enqueue(qid,action,arguments,priority,trigger)

    def _enqueue(self,qid,action,arguments,priority=2,trigger=None):
        q=self.issues[qid];token=digest([self.f.identity,qid,action,arguments])
        if token in self.seen:return
        self.seen.add(token);self.order+=1
        self.ready.append({'id':'action_'+token[:20],'question':qid,'version':q['version'],'action':action,
          'arguments':arguments,'priority':priority,'order':self.order,'trigger':trigger,
          'distinguishing_question':q['plan']['question'],'expected_information':trigger,
          'cost_class':'cheap source' if action in ('inspect','sources') and not arguments.get('enhance') else 'bounded behavior'})
    def _next(self,basic_only=False):
        for a in list(self.ready):
            q=self.issues[a['question']]
            if q['version']!=a['version'] and a['action']=='inspect' and not a['arguments'].get('enhance'):
                a['version']=q['version']
            if not self._impact(q,a['action'],a['arguments']):
                self.ready.remove(a)
                self._note_action('stop',q['id'],a['arguments'].get('operation') or a['arguments'].get('observe'),'decision_already_resolved')
        available=[a for a in self.ready if a['action']=='inspect' and not a['arguments'].get('enhance') or
                   any(self.evidence[e].get('operation')==(a['arguments'].get('operation') or self.root(self.issues[a['question']])) and
                       self.evidence[e]['kind']=='source_inspection' for e in self.issues[a['question']]['evidence'])]
        if basic_only:
            available=[a for a in available if a['action']=='inspect' and not a['arguments'].get('enhance')]
        if not available:return None
        # Deliver an already-computed fact to its consumer without taking a fresh
        # turn from another root. Restore its semantic context before testing the cache.
        for pending in available:
            question=self.issues[pending['question']]
            self.semantics.scope(question['current'])
            if pending['action'] in ('compare','sources') and self.backend.reusable(pending['action'],pending['arguments']):
                self.ready.remove(pending)
                pending['cached_delivery']=True
                return pending
        def rank(a):
            oid=a['arguments'].get('operation',a['arguments'].get('change'));o=self.f.operations.get(oid,{})
            question=self.issues[a['question']]
            self.semantics.scope(question['current'])
            service=self.root_service.get(self.root(question) or a['question'],0)
            context=a['arguments'].get('context',{})
            oid_for_fact=a['arguments'].get('operation')
            consumers=set()
            if a['action']=='inspect' and oid_for_fact and not a['arguments'].get('enhance'):
                record=self.shared_reads.get(self.f.summaries.effect_fact_key(oid_for_fact),{})
                consumers={((self.issues[qid].get('property') or {}).get('claim_identity'),self.root(self.issues[qid])) for qid in record.get('consumers',())}
            semantic_recheck=(question.get('semantic_recheck_property') is not None and
                context.get('property_identity')==question['semantic_recheck_property'])
            # Apply the exact newly supplied meaning before broad catalog
            # expansion can consume the remaining fixed budget. The 3:1 root
            # rotation below still services independent obligations.
            return (not semantic_recheck,a['priority'],-len(consumers),not self.backend.reusable(a['action'],a['arguments']),a['cost_class']!='cheap source',service,o.get('source',{}).get('start',0),a['order'])
        if self.high_streak>=3:
            selected=min(available,key=lambda a:(self.root_service.get(self.root(self.issues[a['question']]) or a['question'],0),
                self.issues[a['question']]['last_service'],a['order']));self.high_streak=0
        else:selected=min(available,key=rank);self.high_streak+=1
        self.ready.remove(selected);self.issues[selected['question']]['last_service']=self.order+len(self.actions)+1
        self.root_service[self.root(self.issues[selected['question']]) or selected['question']]=self.order+len(self.actions)+1
        return selected
    def _plan(self,binding,item):
        if binding.get('core_exact'):
            plan=self.graph.investigation(binding['core_operation'],item,binding)
            try:
                plan_observation(self,binding,item,plan)
            except (KeyError,ValueError,TypeError,IndexError,NotImplementedError) as error:
                plan['observation_choice']={'selected':None,'pool':[],'status':'unsupported',
                    'reason':'local_observation_binding:'+type(error).__name__+':'+str(error)}
                self.diagnostics.append({'issue':item.get('id'),'reason':plan['observation_choice']['reason']})
            return plan
        hint=item.get('next_check',{});hint=hint if isinstance(hint,dict) else {}
        return {'question':item.get('distinguishing_question',hint.get('question','Which applied target and implementation does this declaration denote?')),
            'risk_explanation':item['claim'],'normal_explanation':item.get('alternative'),'effect_root':None,
            'candidate_roots':binding['operations'],'selected_pairs':[],'deferred_pairs':[],
            'focus_selectors':[],'selection_policy':'retain all exact source contexts; resolve target ambiguity before risk admission'}
    def _direction_contradictions(self,q,proposal=None):
        if self.f.options.scope!='AC':return []
        from pr_next_joint.frontend.path_ir import walk,key
        from pr_next_joint.frontend.storage import selectors,keys,selector_relation
        root=self.root(q);out=[]
        if root is None:return out
        # Identify the actual holder/requester grant in the original guards,
        # rather than assuming every control which opens the entry is consent.
        for label in q['evidence']:
            e=self.evidence[label]
            if e.get('kind')!='causal_compare':continue
            use=e.get('observe')
            pick=(q.get('plan',{}).get('observation_choice') or {}).get('selected') or {}
            if use!=root and not (pick.get('measure')=='holder_grant' and
                    (e.get('change'),use)==(pick.get('change'),pick.get('observe')) and compare_relevant(self,q,e)):
                continue
            for p in e.get('holder_consent_counterexamples',[]):
                d=p.get('details',{});holder=d.get('holder_candidate');obj=d.get('object')
                if not (p.get('bounded_condition_confirmed') and d.get('authorization_gate_transition') and d.get('observe')==use and d.get('change')==e.get('change') and obj is not None and holder is not None):continue
                grants=[]
                path=d.get('observe_path');cpath=d.get('change_path')
                if path not in self.f.paths or cpath not in self.f.paths:continue
                if self.f.paths[path]['operation']!=use or self.f.paths[cpath]['operation']!=d['change']:continue
                if d.get('target')!=self.f.operations[root]['target'] or d.get('caller_mode')!='same_requester':continue
                raw=self.f.paths[path]['raw']
                if not any(key(w['path'])==key(obj) for w in raw['writes']):continue
                for guard in raw['guards']:
                    if not any(n.get('kind')=='actual_sender' for n in walk(guard)):continue
                    for s in selectors(guard):
                        if s['root']==obj['root']:continue
                        if any(key(k)==key(holder) for k in keys(s)):grants.append(s)
                controls=d.get('intervened_controls',[])
                matched=[g for g in grants if any(selector_relation(g,c)=='same_shape' and not self.graph._disjoint_keys(g,c) for c in controls)]
                # The SAT formula establishes requester/holder direction on the
                # recorded path only after the intervention touches this grant.
                if matched:
                    out.append({'id':p['id'],'evidence':label,'observe':use,'observe_path':path,'change':d['change'],
                        'change_path':cpath,'object':obj,'holder':holder,'matched_guard_grants':matched,
                        'intervened_controls':controls,'basis':'same holder/requester guard, ordered object and specific after-path; SAT is not a generic business-policy proof'})
        return out
    def _partial_normal_scope(self,q,cited,proposal=None):
        """A branch certificate cannot withdraw an existential whole-entry claim.

        This consumes existing payment/source certificates; it discovers no new
        business risk. Uncovered branches retain the original source prediction.
        """
        def identity(x):return (x['path'],digest(x['object']),digest(x.get('holder')),digest(x.get('unit_source')))
        inspected=[self.evidence[e] for e in cited if self.evidence[e]['kind']=='source_inspection' and self.evidence[e].get('operation')==self.root(q)]
        debits={identity(x):x for e in inspected for x in e.get('debit_objects',[])}
        covered={identity(x):x for e in inspected for x in e.get('settlements',[]) if x.get('same_holder_and_unit_full_settlement')}
        matched=set(debits)&set(covered);remaining=set(debits)-set(covered)
        if matched and remaining:
            return {'operation':self.root(q),'excluded_debit_scopes':[copy.deepcopy(debits[x]) for x in sorted(matched)],
                    'remaining_debit_scopes':[copy.deepcopy(debits[x]) for x in sorted(remaining)],
                    'basis':'existing exact same-branch/object/holder/unit settlement certificate; uncovered is not independently proved loss'}
        if q['current'].get('category') in ('FCR-PAUSE','FCR-FREEZE'):
            declared=set(q['claim_source_scope']['source_operations']);blocks=[];alternatives=[]
            for label in cited:
                e=self.evidence[label]
                if e.get('kind')!='causal_compare' or e.get('change') not in declared or e.get('observe') not in declared:
                    continue
                local=[p for p in e.get('queries',[]) if p.get('label')=='blocked_by_change' and p.get('bounded_condition_confirmed')]
                usable=[a for a in e.get('alternative_uses',[]) if a.get('usable')]
                text=' '.join(str((proposal or {}).get(k,'')) for k in ('claim','reason','revision_reason','explanation'))
                named=any(re.search(r'(?<![\w$])'+re.escape(self.f.operations[a['operation']]['function'].split('(')[0])+r'(?![\w$])',text)
                          for a in usable if a.get('operation') in self.f.operations)
                broad_use=bool(re.search(r'\b(?:same[- ]right alternative|alternative (?:use|entry|route)|bypass)\b|'
                    r'\bwhole (?:right|asset)\b[^.!?]{0,80}\b(?:not unusable|not blocked|remains usable|still available)\b',text,re.I))
                # Do not freeze all normal revisions just because a bypass exists.
                # This restriction applies to the proposed NORMAL-USE argument,
                # not a distinct consent/policy explanation with its own support.
                if local and usable and (named or broad_use):
                    blocks.extend({'evidence':label,'probe':p['id'],'change':e['change'],'observe':e['observe'],
                                   'scope':copy.deepcopy(p['details'])} for p in local)
                    alternatives.extend(copy.deepcopy(usable))
            if blocks:
                return {'retained_blocking_entry_scopes':blocks,'known_usable_alternatives':alternatives,
                    'whole_right_unusable':False,'reason':'same-right bypass narrows the claim; it does not refute the matched blocked entry',
                    'basis':'existing same-control/declared-entry witness and same-right alternative certificate, not a new risk rule'}
        return None
    def accept(self,value,*,revision=False,feedback=None,host_target=None):
        if value is None:return
        origin = value.get('origin')
        model = not host_target and origin in ('verified_service','fixture')
        if model and value.get('usable_analysis') and (not revision or value.get('response_kind')=='substantive'):
            self.model_analysis_available |= origin=='verified_service'
            self.fixture_analysis_available = origin=='fixture' or getattr(self,'fixture_analysis_available',False)
            envelope=value.get('original_envelope',{})
            declaration=envelope.get('task_analysis') or {}
            if isinstance(declaration,dict) and declaration.get('task')==self.f.options.scope and isinstance(declaration.get('basis'),str) and declaration['basis'].strip():
                refs=declaration.get('anchors') or value.get('reviewed') or []
                if isinstance(refs,list) and any(isinstance(r,str) and self.catalog.resolve(r) for r in refs):
                    self.usable_task_opinion=True
        if model and self.context.last_manifest:
            self.semantics.rules.submission=self.context.last_manifest.get('messages_sha256');self.semantics.rules.input_origin=origin
        seed_rows=bool(value.get('annotations') or value.get('policies'))
        if model and seed_rows and self.context.last_manifest:
            rules=self.semantics.rules
            accepted,errors=rules.apply(value,self.context.last_manifest,revision)
            value['semantic_rows_received']=len(value.get('annotations',()))+len(value.get('policies',()))
            self.diagnostics.extend({'reason':error} for error in errors)
            value['accepted_semantic_supports']=accepted
            if accepted:
                self.usable_task_opinion=True
            if rules.last_changes:
                self.semantics.version+=1
                touched={op for h in rules.last_changes for op in rules.related_ops(h)}
                for q in list(self.issues.values()):
                    prop=q.get('property') or {}
                    dependencies=set(prop.get('semantic_dependency_operations',()))|set(q['binding']['operations'])
                    if dependencies & touched:
                        q['version']+=1;q['semantic_recheck_requested']=True
                        self._suggest(q['id'])
                rules.seed_consumers(rules.last_changes)
        self.diagnostics+=value['diagnostics'];envelope=value.get('original_envelope',{})
        if value.get('answers'):
            answered=set()
            allowed_semantics=set()
            for row in (feedback or {}).get('questions',[]):
                for question in row.get('semantic_questions',[]):
                    sid=question.get('id')
                    wire=row.get('sent_semantics',{}).get(sid)
                    current=self.semantics.questions.get(sid) or {}
                    entity=digest([current.get(k) for k in ('id','operation','target','kind','cell','semantic_scope','core_operation','quantity_scope')])
                    if wire and wire['display']==digest(question) and wire['entity']==entity:
                        allowed_semantics.add(sid)
            for answer in value['answers']:
                sid=answer.get('question')
                if sid not in allowed_semantics and sid not in self.semantics.questions:
                    anchor=answer.get('anchor')
                    oids=self.catalog.resolve(anchor) if isinstance(anchor,str) else []
                    choices=[s for s in allowed_semantics if len(oids)==1 and
                             self.semantics.questions[s]['operation']==oids[0] and self.semantics.questions[s]['kind']==answer.get('kind')]
                    if len(choices)==1:
                        answer=dict(answer,question=choices[0])
                self.semantics.rules.legacy_receipt=(origin,self.context.last_manifest.get('messages_sha256')) if model and self.context.last_manifest else None
                try:row,error=self.semantics.consume_answer(answer,allowed_semantics,self.issues)
                finally:self.semantics.rules.legacy_receipt=None
                if error:
                    self.diagnostics.append({'reason':error,'original_semantic_answer':copy.deepcopy(answer)});continue
                q=self.issues[row['issue']]
                if row.get('meaning') in ('required_authorization','normal_authorization'):
                    previous = q.get('authorization_interpretation')
                    if previous:
                        q.setdefault('authorization_alternatives', []).append(copy.deepcopy(previous))
                    q['authorization_interpretation']=row
                q.setdefault('semantic_answers',[]).append(copy.deepcopy(answer));q['version']+=1
                self.updates.append({'issue':q['id'],'event':'source_bound_semantic_answer_consumed',
                    'answer':copy.deepcopy(answer),'binding':row,'evidence':list(q['evidence']),
                    'initial_state_modified':False})
                if model:self.usable_task_opinion=True
                answered.add(q['id'])
            # Consume the whole short answer envelope before compiling any
            # dependent property. A shared resource must not leave earlier
            # siblings with the previous binding/query identity.
            for q in list(self.issues.values()):
                self.semantics.scope(q['current'])
                previous=q.get('property') or {}
                dependencies=previous.get('semantic_dependency_operations',q['binding']['operations'])
                changed=previous.get('semantic_version')!=self.semantics.dependency_identity(dependencies,
                    consent_operations=previous.get('consent_dependency_operations'))
                if q['id'] in answered or changed:
                    if q['id'] not in answered:q['version']+=1
                    q['semantic_recheck_requested']=True
                    self._suggest(q['id'])
        if model and not revision and value.get('response_kind')=='explicit_empty':
            self.explicit_empty_analysis=True
        if not revision:
            for err in value['diagnostics']:
                if err.get('reason') in ('missing_claim_or_source_anchor','truncated_envelope_complete_items_only','issue_not_object'):
                    raw=err.get('original')
                    self.coverage_gaps.append({'reason':err['reason'],'category':raw.get('category') if isinstance(raw,dict) else None})
        declaration=envelope.get('task_analysis')
        if not revision and isinstance(declaration,dict) and declaration.get('task')==self.f.options.scope:self.task_declaration=copy.deepcopy(declaration)
        self.reading_declarations+=value['reviewed'];allowed={q['id']:q for q in (feedback or {}).get('questions',[])}
        incoming_rows=[]
        for incoming in value['issues']:
            targets=[] if revision or host_target else self.catalog.target_branches(incoming['anchors'],incoming.get('root'))
            if targets:
                incoming=dict(incoming,_target_children=[incoming['id']+'@'+digest(t)[:12] for t in targets])
                for target in targets:
                    fork=dict(incoming,id=incoming['id']+'@'+digest(target)[:12])
                    actual=self.catalog.bind(incoming['anchors'],core=incoming.get('root'),target=target)
                    if not actual.get('core_exact'):
                        fork=dict(fork,assessment='investigate',applied_scope_reason='actual target retains an unresolved source reference',original_assessment=incoming['assessment'])
                    else:
                        fork=dict(fork,applied_scope_reason='core declaration resolved in this target; supplementary references retain individual scope')
                    incoming_rows.append((fork,target))
                self.diagnostics.append({'issue':incoming['id'],'reason':'shared_declaration_in_distinct_applied_contexts',
                    'targets':targets,'children':incoming['_target_children'],'common_anchor':incoming.get('root') or incoming['anchors'][0],
                    'instance_identity_inferred':False,'group_is_not_an_additional_unresolved_target':True})
            else:incoming_rows.append((incoming,host_target))
        for incoming,applied_target in incoming_rows:
            item=copy.deepcopy(incoming);qid=item['id'];old=self.issues.get(qid)
            if model and not revision and len(incoming_rows)>1:
                def same_optional(a,b):
                    ignored={'id','assessment','_assessment_normalization','_host_defaulted_fields'}
                    return {k:v for k,v in a.items() if k not in ignored}=={k:v for k,v in b.items() if k not in ignored}
                if item.get('assessment')=='investigate' and any(t==applied_target and i.get('assessment') in ('risk','normal') and same_optional(i,item) for i,t in incoming_rows):
                    self.diagnostics.append({'issue':qid,'reason':'optional_duplicate_of_scoped_reading'})
                    continue
            if model and not revision:
                # A second label for byte-equivalent semantics is a receipt, not a second investigation.
                # Keep every qualifier (including scope, stage, alternative and application target).
                identity=digest([self.f.identity,applied_target,{k:v for k,v in item.items() if k!='id'}])
                existing=self.initial_proposals.get(identity)
                if existing is not None and existing!=qid:
                    self.diagnostics.append({'issue':qid,'reason':'reused_identical_source_proposal','canonical':existing})
                    continue
                self.initial_proposals[identity]=qid
            if old and revision:applied_target=old['binding'].get('applied_context')
            alternate=normal_alternative(item)
            if not item.get('alternative') and alternate['status']=='supplied_not_program_proved':
                item['alternative']=alternate['text'];item['_alternative_source']=alternate['origin']
            if revision and qid not in allowed and qid not in self.issues:
                proposal = self.catalog.bind(item['anchors'],core=item.get('root'))
                options=[]
                for sid,wire in allowed.items():
                    cand=self.issues.get(sid)
                    if not cand or not proposal.get('core_exact') or self.root(cand)!=proposal['core_operation']:continue
                    if not wire.get('sent_message_identity'):continue
                    wire_anchors=set(wire.get('anchors',[]))
                    if not set(item.get('anchors',[]))<=wire_anchors or item.get('root') and item['root'] not in wire_anchors:continue
                    if any(k in item and item[k]!=cand['current'].get(k) for k in ('actor','object','phase','scope','assumptions')):continue
                    if item.get('category') and item['category']!=cand['current'].get('category'):continue
                    options.append(sid)
                if len(options)==1:
                    self.observed_feedback_ids[qid]=options[0]
                    item=dict(item,id=options[0]);qid=options[0];old=self.issues[qid];applied_target=old['binding'].get('applied_context')
            if revision and qid not in allowed:
                self.diagnostics.append({'issue':qid,'reason':'revision_outside_actual_feedback_scope'})
                continue
            if old and revision:
                # Missing optional feedback fields are not instructions to erase
                # the prior scope/category/judgment. Host normalization records
                # defaults; no missing business explanation is invented here.
                for field,previous in old['current'].items():
                    if field not in item and not field.startswith('_host_'):item[field]=copy.deepcopy(previous)
                for field in item.get('_host_defaulted_fields',[]):
                    if field in old['current']:item[field]=copy.deepcopy(old['current'][field])
            requested_core=incoming.get('root')
            proposal=self.catalog.bind(item['anchors'],core=requested_core,target=applied_target)
            binding=self.catalog.bind(item['anchors'],core=requested_core,prior=old['binding'] if old and revision else None,target=applied_target)
            if not binding['operations']:
                self.diagnostics.append({'issue':qid,'reason':'no_locatable_source','original':item})
                if not revision:self.coverage_gaps.append({'issue':qid,'category':item.get('category'),
                    'assessment':item.get('assessment'),'original_anchors':copy.deepcopy(item.get('anchors',[])),
                    'reason':'unbound_original_claim'})
                continue
            if model and not revision and binding.get('core_exact') and item.get('assessment') in ('normal','risk','investigate'):
                self.usable_task_opinion=True
            if old:
                if not revision:self.diagnostics.append({'issue':qid,'reason':'duplicate_existing_issue'});continue
                permitted=allowed.get(qid)
                if not permitted:self.diagnostics.append({'issue':qid,'reason':'revision_outside_actual_feedback_scope'});continue
                linked=set(old['binding']['operations'])
                for label in permitted['new_evidence_labels']:
                    r=self.evidence[label];linked.update(r.get('writers',[]));linked.update(r[k] for k in ('operation','change','observe') if r.get(k))
                if not set(proposal['operations'])&linked or set(proposal['operations'])-linked:
                    self.diagnostics.append({'issue':qid,'reason':'revision_outside_displayed_source_scope'})
                    continue
                changed=item.get('assessment')!=old['current'].get('assessment') or item.get('category')!=old['current'].get('category')
                wire=permitted.get('sent_evidence')
                available={}
                for label in permitted['new_evidence_labels']:
                    if wire is not None and label not in wire:
                        continue
                    rec=dict(self.evidence[label])
                    if wire is not None:
                        for field in ('queries','holder_consent_counterexamples'):
                            rec[field]=[p for p in rec.get(field,[]) if p.get('id') in wire[label]]
                    available[label]=rec
                cited,reason,locators=revision_support(item,old['current'],available)
                import re as _re
                explicit=item.get('evidence',[])
                explicit=[explicit] if isinstance(explicit,str) else explicit if isinstance(explicit,list) else []
                locators_in_text=set(_re.findall(r'\b(?:E\d+|probe_[a-f0-9]{20})\b', ' '.join(str(incoming.get(k,'')) for k in ('claim','reason','revision_reason'))))
                requested={x for x in explicit if isinstance(x,str)}|locators_in_text
                if requested-{x['locator'] for x in locators}:
                    self.diagnostics.append({'issue':qid,'reason':'reference_outside_displayed_evidence'});continue
                if changed and (not cited or not reason):
                    self.diagnostics.append({'issue':qid,'reason':'changed_judgment_requires_specific_new_evidence_and_reason','proposal':item});continue
                if changed and old['current'].get('category') is not None and item['claim'].strip()==old['current']['claim'].strip() and item.get('category')!=old['current'].get('category'):
                    self.diagnostics.append({'issue':qid,'reason':'label_only_change_does_not_resolve_semantic_direction','proposal':item});continue
                if item.get('assessment')=='normal':
                    from .comparison import purpose_only_change
                    if self.f.options.scope=='FCR' and purpose_only_change(self,old,item,cited):
                        self.diagnostics.append({'issue':qid,'reason':'management_purpose_does_not_refute_the_capability','proposal':item,'evidence':cited})
                        continue
                    from .properties import conflicting_measurements
                    incompatible=conflicting_measurements(self,old,item)
                    if incompatible:
                        self.diagnostics.append({'issue':qid,'reason':'same_scope_witness_contradicts_technical_basis','probes':incompatible,'proposal':item})
                        continue
                    contradictions=self._direction_contradictions(old,item)
                    if contradictions:
                        self.diagnostics.append({'issue':qid,'reason':'claimed_holder_consent_contradicted_by_actual_grant_direction',
                          'counterexample_queries':[c['id'] for c in contradictions],'counterexample_dependencies':contradictions,'independent_judgment_preserved':True});continue
                    observations=[r for r in old.get('observations',[]) if r['measure']=='holder_net'
                                  and r['version']==old['version'] and observation_applies(self,old,r)
                                  and r['evidence'] in cited and r['expectations'].get('normal') is False]
                    contrary=[o for r in observations for o in r['outcomes'] if o['predicate_value']]
                    if contrary and set(cited)<={r['evidence'] for r in observations}:
                        partial={'matching_short_payment_witnesses':[o['probe'] for o in contrary],
                                 'observed_branches':[o['scope'] for o in contrary],
                                 'reason':'same-right positive debit and smaller net payout; evidence cannot establish whole-entry full compensation'}
                        old.setdefault('local_normal_explanations',[]).append({'proposal':item,'evidence':cited,'scope':partial})
                        self.diagnostics.append({'issue':qid,'reason':'local_settlement_does_not_refute_other_observed_branch','scope':partial})
                        continue
                    partial=self._partial_normal_scope(old,cited,item)
                    if partial:
                        old.setdefault('local_normal_explanations',[]).append({'proposal':item,'evidence':cited,'scope':partial})
                        self.updates.append({'issue':qid,'event':'partial_normal_scope_narrows_without_whole_withdrawal',
                            'before':copy.deepcopy(old['current']),'proposed':item,'after':copy.deepcopy(old['current']),
                            'evidence':cited,'scope':partial,'reason':partial.get('reason','normal evidence covers only some original debit branches')})
                        continue
                old_root=self.root(old)
                if requested_core is not None and not proposal['core_exact']:
                    self.diagnostics.append({'issue':qid,'reason':'replacement_core_not_resolved_revision_not_committed','proposal':item});continue
                proposed_root=proposal['core_operation']
                supplied_operations={i for ids in proposal['located'].values() for i in ids}
                implicit_correction=(requested_core is None and old_root not in supplied_operations and
                    item['claim'].strip()!=old['current']['claim'].strip())
                correction=proposed_root is not None and proposed_root!=old_root and (requested_core is not None or implicit_correction)
                core_evidence=self._core_support(proposed_root,cited) if correction else []
                if correction and (not reason or not core_evidence):
                    self.diagnostics.append({'issue':qid,'reason':'core_change_requires_related_evidence_and_explanation',
                        'old_core':old_root,'proposed_core':proposed_root,'cited':cited,'proposal':item});continue
                if correction:binding=proposal;binding['core_selection']='sourced_semantic_core_correction'
                if not binding['core_exact'] and old['binding'].get('core_exact') and old_root in self.f.operations:
                    binding=self.catalog.bind(item['anchors'],core=self.catalog.name(old_root),prior=old['binding'])
                    binding.update(core_operation=old_root,core_exact=True,exact=True);binding['operations']=sorted(set(binding['operations'])|{old_root})
                before=copy.deepcopy(old['current']);previous_binding=copy.deepcopy(old['binding']);previous_scope=copy.deepcopy(old['claim_source_scope'])
                # Compile a detached proposal. Reject evidence-free changes
                # to the actual scope even when the model repeats the same label.
                from .property_model import compile_property, validation_key
                preview=dict(old,current=item,binding=binding,history=old['history']+[before],
                             claim_source_scope=self._claim_scope(binding))
                active=self.semantics.active_scope
                registered=self.semantics.questions
                self.semantics.questions=dict(registered)
                try:
                    self.semantics.scope(item)
                    candidate=compile_property(self,preview)
                finally:
                    self.semantics.questions=registered
                    self.semantics.active_scope=active
                old_key=validation_key(old.get('property'))
                new_key=validation_key(candidate)
                if old_key!=new_key and (not cited or not reason):
                    self.diagnostics.append({'issue':qid,'reason':'changed_property_requires_scoped_evidence',
                        'old_key':old_key,'candidate_key':new_key})
                    continue
                if correction or item['claim'].strip()!=before['claim'].strip() and cited and reason:
                    old['claim_source_scope']=self._claim_scope(binding)
                if binding['core_anchor'] is not None and 'root' in item:item['root']=binding['core_anchor']
                old['history'].append(before);old['current']=item;old['binding']=binding;old['version']+=1;old['revision_evidence']=cited
                if model:old['semantic_input']=(origin,self.context.last_manifest.get('messages_sha256'))
                old['task_review']=self._task_review(item,binding)
                old['task_conflict']=self.task_conflict(item) or old['task_review']['status']!='no_explicit_conflict';old['plan']=self._plan(binding,item)
                node='issue:'+qid+':v'+str(old['version']);self.graph.node(node,'semantic_revision',{'item':item,'evidence':cited},'hypothesis')
                self.graph.edge('issue:'+qid,node,'revised_interpretation',layer='hypothesis')
                for l in cited:self.graph.edge('evidence:'+self.evidence[l]['entity_sha256'],node,'revision_depends_on',layer='evidence')
                self.updates.append({'issue':qid,'event':'sourced_semantic_revision','old_assessment':before['assessment'],'new_assessment':item['assessment'],
                  'before':before,'after':copy.deepcopy(item),'before_binding':previous_binding,'after_binding':copy.deepcopy(binding),
                   'reason':reason,'evidence':cited,'supplied_evidence_locators':locators,'scope':binding['operations'],
                   'validation_before':old_key,'candidate_validation':new_key,'scope_requires_revalidation':old_key!=new_key,
                  'core_decision':{'old':old_root,'new':self.root(old),'selection':binding['core_selection'],
                      'requested_core':requested_core,'related_evidence':core_evidence},
                  'claim_scope_before':previous_scope,'claim_scope_after':copy.deepcopy(old['claim_source_scope']),
                  'update_kind':'scoped judgment revision' if changed else 'source supplement or explanation refinement'})
                if old_root!=self.root(old) and self.root(old) is not None:self.enqueue(qid,'inspect',{'operation':self.root(old),'enhance':False},1,'new validated core source')
                self._suggest(qid)
            else:
                if not binding['core_exact']:
                    self.diagnostics.append({'issue':qid,'reason':'core_unresolved_retained_for_investigation','binding':binding})
                    # Candidate targets are all real; their order must not
                    # silently select the contract on which the risk is judged.
                    binding['core_operation']=None
                plan=self._plan(binding,item)
                task_review=self._task_review(item,binding)
                q={'id':qid,'current':item,'history':[],'version':0,'binding':binding,'plan':plan,
                   'task_review':task_review,'task_conflict':self.task_conflict(item) or task_review['status']!='no_explicit_conflict',
                   'claim_source_scope':self._claim_scope(binding),
                   'evidence':[],'novel':[],'last_service':-1,'revision_evidence':[]}
                if model:q['semantic_input']=(origin,self.context.last_manifest.get('messages_sha256'))
                self.issues[qid]=q;self.graph.node('issue:'+qid,'source_semantic_issue',item,'hypothesis')
                for oid in binding['operations']:self.graph.edge(oid,'issue:'+qid,'source_anchor',layer='hypothesis')
                for oid in ([self.root(q)] if q['binding']['core_exact'] else binding['operations']):
                    self.enqueue(qid,'inspect',{'operation':oid,'enhance':False},0 if q['task_conflict'] else 1,'minimum exact candidate source before optional solving')
                self._suggest(qid)
    def _compare_context(self,q,change,observe):
        hint=q['current'].get('next_check',{});hint=hint if isinstance(hint,dict) else {};context={}
        mode=hint.get('caller_mode')
        if mode in ('same_requester','independent_actors'):context['caller_modes']=[mode]
        context['profile']='authorization' if self.f.options.scope=='AC' else 'blocking' if q['current'].get('category') in ('FCR-PAUSE','FCR-FREEZE') else 'effect'
        context['controls']=[w['raw']['path'] for w in self.f.writes.values() if w['operation']==change];context['bindings']=[]
        params=self.f.lookup(observe).function(self.f.operations[observe]['function']).get('parameters',{}).get('parameters',[])
        requested=hint.get('request_bindings',{})
        if isinstance(requested,dict):
            for p in params:
                v=requested.get(p['name'])
                if type(v) not in (int,bool):continue
                context['bindings'].append({'parameter':{'kind':'parameter','id':p['id'],'type':p['typeDescriptions']['typeString']},'value':lit(v)})
        context['declared_assumptions']=copy.deepcopy(q['current'].get('assumptions',[]))
        return context
    def _suggest(self,qid):
        q=self.issues[qid]
        previous_property=q.get('property')
        self.semantics.scope(q['current'])
        from .property_model import compile_property,planning_item
        self.semantics.rules.legacy_receipt=q.get('semantic_input')
        try:self.semantics.consume_issue(q['binding'],q['current'])
        finally:self.semantics.rules.legacy_receipt=None
        q['property']=compile_property(self,q)
        prop=q['property'] or {}
        self.semantics.rules.planning_read(q)
        for child in q.get('property_children',[]):
            record=self.issues.get(child['issue'])
            if record and (child['category'] not in prop.get('possible_categories',[]) or
                    record['current'].get('_parent_meaning')!=prop.get('claim_identity')):
                record['retired_property_parent']=prop.get('id')
        from .property_model import validation_key, compose
        current_key=validation_key(prop)
        if previous_property and validation_key(previous_property)!=current_key:
            q['changed_validation_key']=current_key
            stale=[]
            for pending in self.ready:
                if pending['question']!=qid:continue
                arguments=pending['arguments'];context=arguments.get('context',{})
                planned=context.get('compiled_property')
                goal=(arguments.get('goal') or {}).get('property_identity')
                if (planned and validation_key(planned)!=current_key or
                    not planned and goal==previous_property.get('id')):
                    stale.append(pending)
            if stale:
                self.ready=[pending for pending in self.ready if pending not in stale]
                q.setdefault('source_decisions',[]).append({'reason':'pending_properties_superseded_by_scoped_semantic_update',
                    'old_validation_key':validation_key(previous_property),'new_validation_key':current_key,
                    'retired_unexecuted_actions':[pending['id'] for pending in stale],
                    'source_inspections_and_unrelated_obligations_preserved':True})
        if q.pop('semantic_recheck_requested',False):q['semantic_recheck_property']=prop.get('id')
        if q.get('evidence') and any(self.evidence[e].get('property_validation_key') == validation_key(prop)
                                   for e in q['evidence']):
            existing = compose(self, q)
            if existing['reportable'] or existing['scope'].get('route_status') == 'excluded':
                q.setdefault('evidence_revalidations', []).append({
                    'property': prop['id'], 'key': validation_key(prop),
                    'reason': 'same source, domain, subjects, effects, assumptions and semantic meaning'})
                return
        if q['property'] is not None and self.f.options.scope=='FCR' and not q['current'].get('_host_property_parent'):
            # One source operation may support two distinct capabilities. Fork
            # only its actually typed effects, never a write-point x five grid.
            for category in prop['possible_categories']:
                if not category.startswith('FCR-') or category==prop.get('category'):continue
                child_id=qid+'::'+category
                if child_id in self.issues:
                    existing=self.issues[child_id]
                    if 'retired_property_parent' not in existing:continue
                    child_id+='@'+prop['id'][9:]
                    if child_id in self.issues:continue
                child=copy.deepcopy(q['current']);child.update(id=child_id,category=category,
                    _host_property_parent=qid,_host_source_question=False,
                    _parent_meaning=prop.get('claim_identity'),
                    _original_model_category=q['current'].get('category'))
                self.accept({'issues':[child],'reviewed':[],'diagnostics':[],'usable_analysis':True},
                    host_target=self.f.operations[self.root(q)]['target'])
                q.setdefault('property_children',[]).append({'issue':child_id,'category':category,
                    'basis':'source_typed_possible_effect','not_a_new_model_statement':True})
        view=planning_item(q)
        q['plan']=self._plan(q['binding'],view)
        q['task_review']=self._task_review(view,q['binding'])
        q['task_conflict']=self.task_conflict(view) or q['task_review']['status']!='no_explicit_conflict'
        if prop.get('category') in ('FCR-FREEZE','FCR-PAUSE'):
            uses = [o for o in set(prop.get('source_linked_control_uses',[])+prop.get('control_use_frontier',[])) if self.f.summaries.positions(o)]
            if uses:
                root = self.root(q)
                uses = sorted(uses, key=lambda o: (
                    o not in prop.get('source_operations', []),
                    self.f.operations[o]['source']['start'], o))
                use = uses[0]
                context = {'observable': {'measure': 'financial_block'}, 'compiled_property': prop}
                q['plan']['observation_choice'] = {'selected': {'change': root, 'observe': use,
                    'measure': 'financial_block', 'context': context, 'expectations': {},
                    'scope': {'target': prop['target'], 'objects': prop['objects'],
                              'controls': [w['path'] for r in self.f.summaries.rows(root) for w in r['ordered_writes']]}},
                    'request_resolution': {'use': use, 'possible_uses': uses, 'unmeasured_uses': uses[1:]},
                    'status': 'source_property_selected', 'reason': 'productive financial use, not entry commitment'}
        pick=(q['plan'].get('observation_choice') or {}).get('selected')
        if pick and q['property']:
            pick['context']['property_identity']=q['property']['id']
            pick['context']['semantic_version']=q['property']['semantic_version']
            pick['context']['compiled_property']=copy.deepcopy(q['property'])
        # Expected-authorization solving does not replace a required provenance
        # check for a proposed grant. Reuse the existing directional comparison
        # only for an exact, actually connected grant/use pair.
        hint=view.get('next_check') or {}
        if self.f.options.scope=='AC' and isinstance(hint,dict) and hint.get('action')=='compare':
            c=self.catalog.resolve(hint.get('change'));u=self.catalog.resolve(hint.get('observe'))
            if len(c)==len(u)==1 and c[0]!=u[0] and linked_controls(self,c[0],u[0]) and (not pick or (pick['change'],pick['observe'])!=(c[0],u[0])):
                self.enqueue(qid,'compare',{'change':c[0],'observe':u[0],'context':self._compare_context(q,c[0],u[0])},2,
                    'check the source grant direction independently of expected-authorization solving')
        if q['current'].get('_host_source_question') and not q['current'].get('_semantic_consumer') and q['version']==0 and q['current']['assessment']=='investigate' and (
                any(s.get('kind')!='financial_consent' for s in prop.get('semantic_questions',[])) or not prop.get('category')):return
        q=self.issues[qid];item=view;root=self.root(q);hint=item.get('next_check');hint=hint if isinstance(hint,dict) else {}
        if q['task_conflict'] or not q['binding']['core_exact']:
            for oid in ([root] if root is not None else q['binding']['operations']):
                self.enqueue(qid,'sources',{'operation':oid},0,'clarify task/actor/effect or source-context ambiguity using source, never rename category')
            return
        from .relations import source_violation
        certificate = source_violation(self, q, prop)
        if certificate:
            self._evidence(q, certificate, {'id':'source_property_'+prop['id']})
            q.setdefault('source_decisions', []).append({'reason':'shared property proved by a straight-line source theorem',
                'property':prop['id'],'no_solver_required':True})
            return
        if prop.get('category') in ('FCR-TRANSFER','FCR-DESTROY','FCR-MINT'):
            for use in prop.get('value_dependence',{}).get('value_uses',[]):
                ctx=self._compare_context(q,root,use)
                ctx.update(observable={'measure':'financial_value'},compiled_property=copy.deepcopy(prop),
                           property_identity=prop['id'],semantic_version=prop['semantic_version'])
                self.enqueue(qid,'compare',{'change':root,'observe':use,'context':ctx},2,
                    'follow the actual value dependency into the same holder request, consent and final ledger effect')
        choice=q['plan'].get('observation_choice')
        if choice:
            pick=choice['selected']
            use=(choice.get('request_resolution') or {}).get('use')
            if use and use != root:
                self.enqueue(qid,'inspect',{'operation':use,'enhance':False},0,
                             'inspect the actual use and its local evidence before comparing it')
            if pick:
                self.enqueue(qid,'compare',{'change':pick['change'],'observe':pick['observe'],'context':pick['context']},2,
                             'check the scoped program condition; business justification is a separate question')
                if pick.get('measure')=='financial_block':
                    # A single use can establish a local witness, but its
                    # exclusion cannot close another source-linked use. Check
                    # each actual dependency, using the same typed property.
                    for other in choice.get('request_resolution',{}).get('unmeasured_uses',[]):
                        if other==pick['observe']:continue
                        self.enqueue(qid,'inspect',{'operation':other,'enhance':False},0,
                            'inspect another source-linked use before closing the control scope')
                        self.enqueue(qid,'compare',{'change':pick['change'],'observe':other,
                            'context':copy.deepcopy(pick['context'])},2,
                            'check the independent affected use; first-use refutation is not whole-control closure')
            else:
                self.enqueue(qid,'sources',{'operation':root},2,'clarify unobservable or nondiscriminating prediction from source')
            if pick:return
        action=hint.get('action')
        if action=='compare':
            c=self.catalog.resolve(hint.get('change'));u=self.catalog.resolve(hint.get('observe'))
            if len(c)==len(u)==1:self.enqueue(qid,'compare',{'change':c[0],'observe':u[0],'context':self._compare_context(q,c[0],u[0])},2,'model distinguishing question on exact source pair')
            else:self.diagnostics.append({'issue':qid,'reason':'compare_name_ambiguous_or_missing','candidates':{'change':c,'observe':u}})
        elif action in ('inspect','sources'):
            ids=self.catalog.resolve(hint.get('function')) if hint.get('function') else [root]
            for oid in ids:self.enqueue(qid,action,{'operation':oid,**({'enhance':False} if action=='inspect' else {})},2,'explicit source fact distinguishes competing explanation')
        elif action in ('prefix','prefix_search'):self.enqueue(qid,'prefix_search',{'operation':root},3,'semantic question requires established prestate')
        elif item['assessment']=='investigate' or item.get('alternative') or item.get('distinguish'):
            self.enqueue(qid,'sources',{'operation':root},2,'source dependencies distinguish risk and relevant normal explanation')
    def _evidence(self,q,result,task):
        entity=copy.deepcopy(result);entity.pop('computation_reused',None)
        entity.setdefault('evidence_scope',{'target':self.f.operations[result.get('operation') or self.root(q)]['target'],
            'operation':result.get('operation'),'source_identity':self.f.identity})
        from .property_model import validation_key
        planned=task.get('arguments',{}).get('context',{}).get('compiled_property')
        if planned:
            entity['property_validation_key']=validation_key(planned)
            entity['property_identity_at_execution']=planned.get('id')
        elif result.get('kind')=='source_inspection' or result.get('property_identity')==(q.get('property') or {}).get('id'):
            entity['property_validation_key']=validation_key(q.get('property'))
        else:
            # A delayed old query cannot acquire the current interpretation
            # merely because it is attached after a semantic revision.
            entity['property_validation_key']=None
            entity['unbound_property_origin_not_relabelled']=True
        entity['source_identity'] = self.f.identity
        h=digest(entity);label='E'+str(len(self.evidence)+1);result=copy.deepcopy(entity)
        result.update(id=label,question=q['id'],semantic_version=q['version'],action=task['id'],entity_sha256=h)
        self.evidence[label]=result;q['evidence'].append(label);self.graph.evidence('issue:'+q['id'],result);return label
    def _reuse_observation(self,q,source,label):
        choice=q['plan'].get('observation_choice') or {}
        picked=choice.get('selected')
        if not picked or picked['measure']!='holder_net' or source['operation']!=picked['observe']:
            return
        if source['local_errors'] or not source['complete_for_bounded_paths'] or source['unknown_guard_paths'] or source['credential_paths']:
            return
        from pr_next_joint.frontend.path_ir import key
        obj={key(s) for s in picked['scope']['objects']}
        def signature(row):
            return row['path'],key(row['object']),digest(row['holder']),digest(row['unit_source'])
        debits={signature(d) for d in source['debit_objects'] if key(d['object']) in obj and d['unit_source']}
        full={signature(s) for s in source['settlements'] if s['same_holder_and_unit_full_settlement']}
        if not debits or not debits<=full:
            return
        queued=[a for a in self.ready if a['question']==q['id'] and a['action']=='compare' and
                a['arguments'].get('context',{}).get('observable',{}).get('measure')=='holder_net']
        if not queued:
            return
        self.ready=[a for a in self.ready if a not in queued]
        choice['execution_decision']={'actual_action':'reuse_source_inspection','evidence':label,
            'saved_actions':[a['id'] for a in queued],'scope_identity':copy.deepcopy(picked['scope']),'matched_paths':sorted(s[0] for s in debits),
            'observed':False,'reason':'all modeled debits of this holder and unit already have exact full source settlement',
            'scope':'conditional on committed positive debit, no reachable deployment asserted'}
        q.setdefault('source_decisions',[]).append(copy.deepcopy(choice['execution_decision']))

    def execute(self,*,reserve_for_feedback=False,basic_only=False):
        start=time.monotonic();self.backend.deadline=start+max(0,self.f.options.seconds-self.program_seconds)
        investigation_deadline=self.backend.deadline
        yielded_to_semantics=False
        try:
            while self.ready and not self.limit():
                if reserve_for_feedback and self.program_seconds+time.monotonic()-start>=self.f.options.seconds/2 and any(
                        s for q in self.issues.values() for s in (q.get('property') or {}).get('semantic_questions',[])
                        if not any(a.get('question')==s['id'] for a in q.get('semantic_answers',[]))):
                    yielded_to_semantics=True;break
                self.backend.check();task=self._next(basic_only)
                if task is None:break
                ta=task['arguments']
                if task.get('cached_delivery'):
                    self._note_action('reuse',task['question'],ta.get('operation') or ta.get('observe'),'cached_evidence_for_independent_consumer')
                else:
                    self._note_action('select',task['question'],ta.get('operation') or ta.get('observe'),
                                      self._impact(self.issues[task['question']],task['action'],ta) or 'final_source_consumer')
                q=self.issues[task['question']];t=time.monotonic()
                # A single prerequisite search must not consume the whole
                # contract budget before unrelated obligations or the one
                # semantic follow-up receive service. Slice only the large
                # search consumers; their completed source states are retained.
                args=task['arguments'];measure=args.get('context',{}).get('observable',{}).get('measure')
                sliced=bool(self.ready) and (task['action']=='prefix_search' or
                    task['action']=='compare' and measure=='financial_block')
                quantum=max(self.f.options.solver_timeout_ms/1000.,self.f.options.seconds/6.)
                self.backend.deadline=min(investigation_deadline,t+quantum) if sliced else investigation_deadline
                records_before=len(self.backend.records)
                def resume_slice():
                    if not sliced or self.program_remaining()<=0:return
                    resumed=copy.deepcopy(task);self.order+=1
                    resumed.update(id=task['id'].split(':slice')[0]+':slice'+str(task.get('slice',0)+1),
                        slice=task.get('slice',0)+1,order=self.order,priority=3,
                        trigger='resume retained source frames after other eligible obligations')
                    for field in ('state','evidence','program_seconds','reason','traceback'):resumed.pop(field,None)
                    self.ready.append(resumed)
                self.semantics.scope(q['current'])
                try:
                    kind=task['action'];a=task['arguments']
                    if kind=='inspect' and not a.get('enhance'):
                        oid=a['operation']
                        result=self.backend.inspect(oid,False)
                        fact=self.f.summaries.effect_fact_key(oid)
                        record=self.shared_reads[fact];record['result']=result
                        for qkey in sorted(record['pending']):
                            self._attach_read(self.issues[qkey],oid,fact,result)
                        task.update(state='recorded',evidence=q['source_facts'][fact],computation_reused=bool(result.get('computation_reused')))
                        self._note_action('read',q['id'],oid,'shared_source_fact_acquired',fact)
                        record['pending'].clear()
                        continue
                    if kind=='inspect':result=self.backend.inspect(a['operation'],a.get('enhance',False))
                    elif kind=='sources':result=self.backend.sources(a['operation'])
                    elif kind=='compare':result=self.backend.compare(a['change'],a['observe'],context=a.get('context'))
                    elif kind=='prefix_search':result=self.backend.prefix_search(a['operation'],plan=a.get('frame_plan'),goal=a.get('goal'))
                    else:raise ValueError('unknown_internal_action')
                    if kind=='inspect':
                        if q.get('host_source_candidate'):result['applied_source_candidate']=q['host_source_candidate']
                        if self.f.options.scope=='AC':
                            from .authorization import acquisition_premise
                            premise=acquisition_premise(self,q)
                            if premise:result['authorization_premise']=premise
                    task['computation_reused']=bool(result.get('computation_reused'));label=self._evidence(q,result,task);task.update(state='recorded',evidence=label)
                    if result.get('stopped_reason')=='action_slice_exhausted':
                        task['unfinished_source_frontier_retained']=True;resume_slice()
                    if kind=='inspect':
                        if result.get('applied_source_candidate') or result.get('authorization_premise'):q['novel'].append(label)
                        self._reuse_observation(q,result,label)
                        if result['no_committing_path'] or result['net_effect_proved_unchanged'] or any(s['same_holder_and_unit_full_settlement'] for s in result['settlements']):q['novel'].append(label)
                        if q['task_conflict'] or not q['binding']['core_exact']:q['novel'].append(label)
                        if not a.get('enhance') and (result['credential_paths'] or result['unknown_guard_paths']) and not result['no_committing_path']:
                            self.enqueue(q['id'],'inspect',{'operation':a['operation'],'enhance':True},1,'critical credential/external-success question needs bounded enhancement')
                    elif kind=='sources':
                        if q['task_conflict'] or not q['binding']['core_exact']:q['novel'].append(label);continue
                        plan=q['plan']
                        if (plan.get('observation_choice') or {}).get('selected'):
                            continue
                        for pair in plan['selected_pairs']:
                            self.enqueue(q['id'],'compare',{'change':pair['change'],'observe':pair['observe'],'context':self._compare_context(q,pair['change'],pair['observe'])},2,'selected graph dependency answers: '+plan['question'])
                        if plan['deferred_pairs']:self.diagnostics.append({'issue':q['id'],'reason':'unrelated_or_secondary_graph_pairs_deferred','pairs':plan['deferred_pairs']})
                        guard_roots={s['root'] for s in result['guard_selectors']}
                        seed_needed=any(s['path']['root'] in guard_roots for s in self.backend.seed(a['operation']))
                        if q['current']['assessment']=='investigate' and guard_roots and seed_needed:
                            self.enqueue(q['id'],'prefix_search',{'operation':a['operation']},3,'current source gap requires an established guard state')
                    elif kind=='compare':
                        if result.get('continuation') and self.backend.remaining()>0:
                            resumed=copy.deepcopy(a)
                            resumed.setdefault('context',{}).update(result['continuation'])
                            self.enqueue(q['id'],'compare',resumed,2,
                                'resume the bounded source branch slice after servicing other roots')
                        if (q.get('property') or {}).get('category') in ('FCR-FREEZE','FCR-PAUSE') and any(
                                x.get('bounded_condition_confirmed') and x.get('label')=='financial_block'
                                for x in result.get('queries',[])):
                            # A confirmed productive-request loss already
                            # establishes this existential capability. Keep
                            # other uses in coverage, but do not repeatedly
                            # construct their large frames just to establish
                            # the same positive claim again. Negative outcomes
                            # still have to check every required use.
                            pending=[x for x in self.ready if x['question']==q['id'] and x['action']=='compare'
                                and x['arguments'].get('context',{}).get('property_identity')==(q.get('property') or {}).get('id')
                                and x['arguments'].get('observe')==a.get('observe') and x['arguments'].get('context',{}).get('observable',{}).get('measure')=='financial_block']
                            if pending:
                                self.ready=[x for x in self.ready if x not in pending]
                                q.setdefault('source_decisions',[]).append({'reason':'same existential financial capability already has a validated witness',
                                    'evidence':label,'saved_actions':[x['id'] for x in pending],
                                    'unmeasured_uses_not_marked_negative':True})
                        choice=q['plan'].get('observation_choice')
                        pick=(choice or {}).get('selected')
                        is_selected=pick and (a.get('change'),a.get('observe'),a.get('context'))==(pick['change'],pick['observe'],pick['context'])
                        if is_selected:
                            row=self._observed(q,label,result,choice['selected'])
                            q.setdefault('observations',[]).append(row)
                            if row['outcomes']:q['novel'].append(label)
                            elif choice.get('ordinary_pairs'):
                                for alt in choice['ordinary_pairs'][:1]:
                                    change,use=alt['change'],alt['observe']
                                    self.enqueue(q['id'],'compare',{'change':change,'observe':use,'context':self._compare_context(q,change,use)},3,'ordinary source comparison after unsupported optional property')
                        elif result.get('queries') or result.get('control_noninterference',{}).get('proved'):
                            q['novel'].append(label)
                        if result.get('observed_measure')=='direct_effect' and not result.get('property_excluded') and not a.get('context',{}).get('reached_state') and not any(
                            x.get('label')=='direct_effect' and x.get('bounded_condition_confirmed') for x in result.get('queries',[])):
                            prop=q.get('property') or {};operation=result.get('observe')
                            state_gap=any(x.get('answer')=='unsat' and
                                not x.get('exclusion_certificate',{}).get('excludes_only_this_formula') and
                                not x.get('details',{}).get('prestate',{}).get('global_reachability_exhausted')
                                for x in result.get('queries',[]) if x.get('label') in ('direct_effect','local_premises_feasible'))
                            # More states cannot repair an unsupported type,
                            # an unresolved consent policy or an unknown call.
                            # Search prefixes only for an actual bounded
                            # prestate exclusion that another state can alter.
                            if state_gap and operation and prop.get('category') in ('FCR-MINT','FCR-TRANSFER','FCR-DESTROY'):
                                self.enqueue(q['id'],'prefix_search',{'operation':operation,
                                    'goal':{'measure':'positive_effect','category':prop['category'],'positions':prop['objects'],'require_privileged':True,
                                            'property_identity':prop['id']}},3,'establish the actual positive effect, not merely a zero-valued committing call')
                    elif kind=='prefix_search':
                        if result.get('states'):
                            q['novel'].append(label)
                            prop=q.get('property') or {}
                            if (a.get('goal') or {}).get('measure')=='positive_effect' and prop.get('category') in ('FCR-MINT','FCR-TRANSFER','FCR-DESTROY'):
                                for state in result.get('states',[]):
                                    context=self._compare_context(q,a['operation'],a['operation'])
                                    context.update(compiled_property=prop,property_identity=prop['id'],
                                        semantic_version=prop['semantic_version'],reached_state=state)
                                    context['observable']={'measure':'direct_effect','category':prop['category']}
                                    self.enqueue(q['id'],'compare',{'change':a['operation'],'observe':a['operation'],'context':context},2,
                                        'consume reached target state in full category property; prefix witness alone is not a finding')
                except TimeoutError as error:
                    stopped='action_slice_exhausted' if sliced and self.program_remaining()>0 else str(error)
                    task.update(state='stopped',reason=stopped);self.diagnostics.append({'issue':q['id'],'reason':stopped,
                        'underlying_diagnostic':str(error),'action':task['id'],'independent_results_preserved':True})
                    partial=self.backend.records[records_before:]
                    if partial:
                        record={'kind':'interrupted_program_action','operation':args.get('change',args.get('operation')),
                            'change':args.get('change'),'observe':args.get('observe'),'queries':copy.deepcopy(partial),
                            'property_identity':args.get('context',{}).get('property_identity'),
                            'coverage_complete':False,'negative_conclusion_allowed':False,
                            'local_errors':[{'reason':str(error)}]}
                        task['partial_evidence']=self._evidence(q,record,task)
                    resume_slice()
                except Exception as error:
                    task.update(state='local_diagnostic',reason=type(error).__name__+':'+str(error),traceback=traceback.format_exc());self.diagnostics.append({'issue':q['id'],'action':task['id'],'reason':task['reason'],'independent_results_preserved':True})
                finally:
                    self.backend.deadline=investigation_deadline
                    task['program_seconds']=time.monotonic()-t;self.actions.append(task)
        except TimeoutError:pass
        finally:
            self.program_seconds+=time.monotonic()-start;self.backend.deadline=None
            if self.ready and not basic_only:self.diagnostics.append({'reason':'yield_to_source_bound_semantic_review' if yielded_to_semantics else self.limit() or 'source_dependency_not_ready',
                'unexecuted_actions':[a['id'] for a in self.ready],
                'total_program_budget_unchanged':True,'remaining_actions_retained':True})
    def _observed(self,q,label,result,pick):
        measure=pick['measure']
        row={'question':q['id'],'version':q['version'],'measure':measure,'evidence':label,
             'scope':pick['scope'],'change':pick['change'],'observe':pick['observe'],'request_context':pick['context'],'outcomes':[],
             'expectations':pick['expectations'],'business_policy_proved':False}
        if (result.get('change'),result.get('observe'),result.get('observed_measure'))!=(pick['change'],pick['observe'],measure):
            row['limit']='observation_scope_mismatch'
            return row
        from .ledger import MEASURES
        if measure in set(MEASURES)|{'missing_control','denied_qualified','direct_effect','authorization_violation'}:
            queries={p['id']:p for p in result.get('queries',[])}
            for pair in result.get('ledger_measurements',result.get('property_measurements',[])):
                feasible=queries.get(pair.get('feasible_probe'),{}); probe=queries.get(pair.get('result_probe'),{})
                if not feasible.get('bounded_condition_confirmed') or not probe:continue
                sat=probe.get('bounded_condition_confirmed'); unsat=probe['answer']=='unsat' and not probe.get('abstract_hash')
                if sat or unsat:
                    row['outcomes'].append({'predicate_value':bool(sat),'probe':probe['id'],'feasibility_probe':feasible['id'],
                        'scope':probe['details'],'predicate_checks':copy.deepcopy(probe.get('predicate_checks',{})),'favors_in_this_scope':None,
                        'use':'local_condition_only','business_policy_proved':False})
            if not row['outcomes']:row['limit']='no_compatible_checked_path_or_unsupported'
            return row
        if measure in ('opens','blocks'):
            if pick['context'].get('observable',{}).get('other_intervention_inputs'):
                row['limit']='coupled_intervention_also_changes_other_request_inputs; cannot isolate this control'
                return row
            if not all(self.backend.complete(oid) for oid in (pick['change'], pick['observe'])):
                row['limit']='incomplete_source_paths; no behavioral polarity'
                return row
            for oid in (pick['change'],pick['observe']):
                for pid,path in self.f.operation_paths(oid, True):
                    deps=self.backend.condition_dependencies(oid,pid,path)
                    if deps['unknown_dependencies'] or deps['credential_dependencies']:
                        row['limit']='unresolved_external_or_credential_in_request'
                        return row
        qname={'financial_block':'financial_block','holder_grant':'requester_opens_other_holders_gate','holder_net':'holder_net_lower_after',
               'opens':'opened_by_change','blocks':'blocked_by_change'}[measure]
        for probe in result.get('queries',[]):
            if probe.get('label')!=qname:
                continue
            # A non-vacuous same-scope feasibility witness is required to interpret UNSAT.
            value=True if probe.get('bounded_condition_confirmed') else None
            feasible_id=None
            if measure=='holder_net':
                matched=next((m for m in result['net_measurements'] if m['result_probe']==probe['id']),None)
                if matched:
                    feasible_id=matched['feasible_probe']
                    if probe['answer']=='unsat' and not probe.get('abstract_hash'):
                        value=False
            elif measure in ('opens','blocks'):
                d=probe['details']
                fp=next((p for p in result['queries'] if p['label']=='scenario_feasible' and
                    all(p['details'].get(k)==d.get(k) for k in ('change_path','encoded_case','prefix','caller_mode'))),{})
                if not fp.get('bounded_condition_confirmed'):continue
                feasible_id=fp['id']
                if probe['answer']=='unsat' and not probe.get('abstract_hash'):value=False
            elif measure=='holder_grant' and probe['answer']=='unsat':
                # A failed grant-transition search is not proof of legitimate delegation.
                value=None
            if value is not None:
                row['outcomes'].append({'predicate_value':value,'scope':probe['details'],'probe':probe['id'],
                    'feasibility_probe':feasible_id,'encoded_case':probe['details'].get('encoded_case',[]),'favors_in_this_scope':next((h for h,v in pick['expectations'].items() if v==value),None)})
        if not row['outcomes']:
            row['limit']='no_supported_discriminating_witness; not a negative prediction'
        return row

    def _source_gate_observation(self,e):
        if self.f.options.scope!='AC' or e.get('kind')!='causal_compare':
            return False
        from pr_next_joint.frontend.path_ir import walk
        from pr_next_joint.frontend.storage import selectors,selector_relation
        change,observe=e['change'],e['observe']
        if self.f.operations[change]['target']!=self.f.operations[observe]['target']:
            return False
        controls=e.get('evidence_scope',{}).get('controls',[])
        for _,p in self.f.operation_paths(observe,True):
            for g in p['guards']:
                if not any(n.get('kind')=='actual_sender' for n in walk(g)):
                    continue
                gates=[s for s in selectors(g) if any(selector_relation(s,c)=='same_shape' and
                       not self.graph._disjoint_keys(s,c) for c in controls)]
                if gates and any(x.get('bounded_condition_confirmed') and x['label']=='opened_by_change' for x in e.get('queries',[])):
                    return True
        return False

    def _feedback_labels(self,q):
        labels=list(dict.fromkeys(q['novel']))
        local = coverage_facts(self,q)
        if local and not local['affected_categories'] and not q.get('host_source_candidate'):
            return []
        observed=[]
        if (q['plan'].get('observation_choice') or {}).get('selected'):
            if q['current']['assessment']=='normal':
                from .report import evaluate
                if 'same_scope_actual_full_settlement' in evaluate(self,q)['reasons']:
                    return []
            observed=[x['evidence'] for x in q.get('observations',[]) if x['version']==q['version'] and x['outcomes'] and observation_applies(self,q,x)]
        hint=q['current'].get('next_check')
        explicit_pair=isinstance(hint,dict) and hint.get('action')=='compare'
        if not (explicit_pair or q['current'].get('alternative') or q['plan'].get('observation_choice') or
                q['current']['assessment']=='investigate' or q['task_conflict'] or q.get('host_source_candidate') or any(self.evidence[e].get('authorization_premise') for e in labels) or not q['binding']['core_exact']):
            return list(dict.fromkeys(observed))
        eligible=list(observed)
        for label in labels:
            e=self.evidence[label]
            if e.get('applied_source_candidate') or e.get('authorization_premise'):
                eligible.append(label)
            elif e.get('operation')==self.root(q) and e['kind']=='source_inspection' and (e.get('no_committing_path') or
                    e.get('net_effect_proved_unchanged') or any(s.get('same_holder_and_unit_full_settlement') for s in e.get('settlements',[]))):
                eligible.append(label)
            elif q['task_conflict'] and e['kind']=='source_inspection' and (e.get('actual_guards') or e.get('effects') or e.get('writes')):
                eligible.append(label)
            elif e['kind']=='causal_compare' and compare_relevant(self,q,e) and (self._source_gate_observation(e) or
                    self._direction_contradictions(q) and e.get('holder_consent_counterexamples') or
                    e.get('control_noninterference',{}).get('proved') or any(a.get('usable') for a in e.get('alternative_uses',[])) or
                    any(p.get('bounded_condition_confirmed') and p['label']=='blocked_by_change' for p in e.get('queries',[]))):
                eligible.append(label)
        return list(dict.fromkeys(eligible))

    def _compact(self,value):
        if isinstance(value,dict):return {k:self._compact(v) for k,v in value.items() if k not in ('formula','worlds','source_card','writer_cards','actual_guards','writes','effects','queries','witness','guard_selectors','used_selectors')}
        if isinstance(value,list):return [self._compact(v) for v in value]
        if isinstance(value,str) and value in self.catalog.operations:return self.catalog.name(value)
        return value
    def feedback(self):
        questions=[];shared_resources={}
        for q in sorted(self.issues.values(),key=lambda q:(not any(x['outcomes'] for x in q.get('observations',[])),not q['task_conflict'],q['id'])):
            if q.get('retired_property_parent'):continue
            labels=self._feedback_labels(q)
            from .report import evaluate
            assessment=evaluate(self,q)
            alternatives=set((q.get('property') or {}).get('possible_categories',[])) - {assessment.get('category')}
            if assessment['scope'].get('route_status')=='excluded' and not q['task_conflict'] and not alternatives:
                self.feedback_trace.append({'issue':q['id'],'selected':False,'sent':False,'consumed':False,
                    'reason':'same_property_source_or_complete_domain_refutation_already_closes_this_scope',
                    'changed_finding':False})
                continue
            semantic_questions=[]
            for s in (q.get('property') or {}).get('semantic_questions',[]):
                if any(a.get('question')==s['id'] for a in q.get('semantic_answers',[])):continue
                if s.get('kind')=='resource':
                    from .initial_state import family
                    resource=digest([s['target'],family(s['cell']),s.get('semantic_scope')])
                    if resource in shared_resources:
                        q.setdefault('semantic_question_reuse',[]).append({'question':s['id'],'shared_question':shared_resources[resource],
                            'basis':'same target, source storage family and semantic scope'})
                        continue
                    shared_resources[resource]=s['id']
                semantic_questions.append(s)
            semantic_questions.extend(self.semantics.rules.semantic_questions_for(q))
            if labels and not semantic_questions and not q['current'].get('alternative') and q['current'].get('assessment')=='risk':
                from .report import evaluate
                if evaluate(self,q)['reportable']:
                    self.feedback_trace.append({'issue':q['id'],'selected':False,'sent':False,'consumed':False,
                        'reason':'existing_source_and_property_already_support_same_uncontested_claim','changed_finding':False})
                    continue
            if not labels and not semantic_questions:continue
            evidence=[]
            for label in labels:
                e=self.evidence[label];r=self._compact(e);seen=set();r['probe_results']=[]
                observations=[x for x in q.get('observations',[]) if x['evidence']==label and x['version']==q['version']]
                keep=None
                if observations:
                    outcomes=[o for row in observations for o in row['outcomes']]
                    keep={o['probe'] for o in outcomes}|{o['feasibility_probe'] for o in outcomes if o['feasibility_probe']}
                    r={'id':label,'kind':'scoped_program_observation','operation':self.catalog.name(e['observe']),
                       'source_names':{k:[self.backend._storage_name(e['observe'],s) for s in observations[0]['scope'].get(k, [])]
                                       for k in ('controls','objects')},
                       'intervention':self.catalog.name(e['change']),'measure':observations[0]['measure'],
                       'finding_source':self.catalog.name(self.root(q)),'interpretation_limit':'Only this matched use, key and measure. Availability alone does not test the amount or consent.',
                       'expected':observations[0]['expectations'],'outcomes':[{k:v for k,v in o.items() if k!='scope'} for o in outcomes],
                       'evidence_scope':self._compact(observations[0]['scope']),'partial_bounds':e.get('net_pair_budget'), 'probe_results':[]}
                elif e['kind']=='causal_compare':
                    # The full comparison stays local. Carry only probes/dependencies of this decision.
                    relevant_tags={'opened_by_change','blocked_by_change','two_distinct_holders_blocked_same_change','requester_opens_other_holders_gate',
                        'same_request_amount_change','financial_consent_unresolved','financial_value','financial_value_post_exclusion',
                        'direct_effect','financial_block','authorization_violation','denied_qualified'}
                    keep={p['id'] for p in e.get('queries',[]) if p.get('label') in relevant_tags and p.get('id')}
                    r={k:self._compact(e[k]) for k in ('id','kind','change','observe','evidence_scope','control_noninterference',
                        'alternative_uses','complete_for_modeled_observe_branches','complete_for_modeled_change_branches') if k in e}
                    r['probe_results']=[]
                for x in e.get('queries',[]):
                    if keep is not None and x.get('id') not in keep:continue
                    d=x.get('details',{});sig=digest([x['label'],x['answer'],x.get('bounded_condition_confirmed'),x.get('formula_ref'),d])
                    if sig in seen:continue
                    seen.add(sig);r['probe_results'].append({k:copy.deepcopy(x[k]) for k in ('id','label','answer','bounded_condition_confirmed','details','formula_ref') if k in x})
                    if keep is not None:
                        card=r['probe_results'][-1]
                        card['details']={k:self._compact(d[k]) for k in ('target','change_path','observe_path','before_path',
                            'after_path','object','holder','holder_candidate','unit','assumptions','caller_mode','intervened_controls',
                            'authorization_gate_transition','observe_guard_selectors','encoded_case','encoded_request_bindings','request_aliases',
                             'payer_key','recipient_key','revert_path','use_path','observe','role','active_holder_control',
                             'ledger','holder_consent','same_holder_settlement','same_request','property_validated',
                             'no_universal_gross_allowance_policy','conditional_call_summary','actor_scope','acquired_use') if k in d}
                evidence.append(r)
            relevant=set(q['binding']['operations'])
            relevant.update(s['operation'] for s in semantic_questions if s.get('operation') in self.f.operations)
            for pair in q['plan']['selected_pairs']:relevant.update((pair['change'],pair['observe']))
            relevant.update(e.get(k) for e in (self.evidence[l] for l in labels) for k in ('change','observe') if e.get(k))
            choice=q['plan'].get('observation_choice',{}).get('selected')
            if choice:
                relevant.update(self.graph.closure_operations(choice['observe'],choice['scope']['controls']+choice['scope']['objects']))
            for l in labels:
                relevant.update(v['operation'] for v in self.evidence[l].get('alternative_uses',[]) if v.get('operation'))
            for e in q['current'].get('_scope_effects',()):
                if e in self.semantics.rules.effects:relevant.add(self.semantics.rules.effects[e]['oid'])
            measure=(choice or {}).get('measure')
            if not semantic_questions and not q['task_conflict'] and not q['current'].get('alternative'):
                continue
            if semantic_questions:
                gap='meaning of the source-bound right or applicable policy'
            elif q['task_conflict']:
                gap='whether the proposed effect depends on privilege rather than ordinary access'
            else:
                gap='whether the normal explanation covers this holder, request and actual effect'
            questions.append({'id':q['id'],'claim':q['current']['claim'],'assessment':q['current']['assessment'],
              'category':q['current'].get('category'),'alternative':q['current'].get('alternative'),'anchors':q['current']['anchors'],
              'distinguishing_question':q['plan']['question'],'task_conflict':q['task_conflict'],'source_context_ambiguous':not q['binding']['core_exact'],
              'internal_external_caller_contexts':q['binding'].get('internal_external_caller_contexts',{}),
              'new_evidence_labels':labels,'evidence':evidence,'operations':sorted(relevant),
               'semantic_questions':copy.deepcopy(semantic_questions),
              'decision':{'unresolved':gap,'program_observed':measure,'changes':'only the linked property in its recorded scope'},
              'scope_note':'Clarify actual actor, grant and effect.' if q['task_conflict'] else 'Only this question.'})
        return {'questions':questions}
    def run(self):
        from .decision_output import public_report,context_summary,coverage_summary,receipt,query_summary,evidence_summary,semantic_summary
        started=time.monotonic();self.out.mkdir(parents=True,exist_ok=True)
        t=time.monotonic()
        messages,self.initial_manifest=self.context.messages()
        write(self.out/'initial_context_manifest.json',context_summary(self.initial_manifest))
        write(self.out/'source_identity.json',{'program_identity':self.f.identity,
              'implementation_sha256':self.f.context['implementation_sha256'],
              'selected_targets':self.f.selected,'source_facts_sha256':digest(self.f.context)})
        self.program_seconds+=time.monotonic()-t
        initial=self.session.request(prepared=(messages,self.initial_manifest))
        t=time.monotonic();self.accept(initial)
        from .candidates import investigate
        self.semantics.rules.scope_offices()
        investigate(self)
        self.program_seconds+=time.monotonic()-t
        with budget(self.f.options.seconds,remaining=lambda:self.backend.remaining() if self.backend.deadline is not None else max(0,self.f.options.seconds-self.program_seconds)) as solver_resource:
            reserve=bool(self.f.options.feedback and len(self.session.attempts)<self.f.options.attempt_limit)
            self.execute(basic_only=True)
            basic=build(self)
            write(self.out/'checkpoint_basic.json',public_report(basic))
            self.execute(reserve_for_feedback=reserve)
            from .candidates import investigate_obligations
            initial_obligations=build(self)
            write(self.out/'initial_obligations.json',coverage_summary(initial_obligations['task_analysis']['reading_scope']))
            if investigate_obligations(self,initial_obligations):self.execute(reserve_for_feedback=reserve)
            checkpoint=build(self);write(self.out/'checkpoint_initial.json',public_report(checkpoint))
            feedback=self.feedback();recovery=not initial or not initial['usable_analysis'] or not self.usable_task_opinion;reason=None
            queued={q['id'] for q in feedback['questions']}
            for qid in self.issues.keys()-queued:
                self.feedback_trace.append({'issue':qid,'selected':False,'sent':False,'parsed':False,'consumed':False,
                    'reason':'no_new_discriminating_evidence','changed_finding':False})
            manifest={};value=None
            if not self.f.options.feedback:reason='feedback_disabled'
            elif len(self.session.attempts)>=self.f.options.attempt_limit:reason='attempt_limit'
            elif self.deadline and time.monotonic()>=self.deadline:reason='batch_deadline'
            elif not recovery and not feedback['questions']:reason='no_decisive_new_evidence_or_task_conflict'
            else:
                if recovery:feedback={'questions':[{'id':'protocol_recovery','new_evidence_labels':[],'operations':[],'claim':'No usable bound analysis; reuse initial source view.'}],
                    'binding_diagnostics':[{'issue':d.get('issue'),'reason':d['reason'],
                        'anchors':d.get('original',{}).get('anchors',[])} for d in self.diagnostics if d.get('reason')=='no_locatable_source']}
                preview,manifest=self.context.messages(feedback,recovery=recovery);write(self.out/'followup_preview_manifest.json',context_summary(manifest))
                if manifest['input_tokens']>self.f.options.input_limit:reason='complete_message_capacity_exceeded'
                elif not recovery and not manifest['selected_issues']:reason='no_whole_scoped_feedback_unit_fits'
                else:
                    if not recovery:
                        chosen=set(manifest['selected_issues']);feedback['questions']=[q for q in feedback['questions'] if q['id'] in chosen]
                        for q in feedback['questions']:
                            q['sent_evidence']=manifest['wire_evidence'].get(q['id'],{})
                            q['sent_semantics']=manifest['semantic_wire']
                            q['sent_message_identity']=manifest['messages_sha256']
                    write(self.out/'feedback_receipt.json',receipt(feedback,'scoped_semantic_feedback'))
                    value=self.session.request(feedback=feedback,recovery=recovery,prepared=(preview,manifest))
                    self.call_decisions.append({'phase':'followup','sent':bool(self.session.attempts[-1].get('actual_model_submissions')),
                      'actual_model_submissions':self.session.attempts[-1].get('actual_model_submissions',0),'simulated':self.session.is_simulated(),
                      'reason':'necessary_protocol_recovery' if recovery else 'scoped_distinguishing_evidence_or_task_conflict','attempt_status':self.session.attempts[-1].get('status'),'manifest':manifest})
                    t=time.monotonic();self.accept(value,revision=not recovery,feedback=feedback);self.program_seconds+=time.monotonic()-t
                    if not self.limit():self.execute()
                    elif self.ready:self.diagnostics.append({'reason':self.limit(),'new_issues_not_executed':True,'not_safe':True})
            if reason:
                self.call_decisions.append({'phase':'followup','sent':False,'reason':reason,'program_limit_does_not_cancel_final_revision':True})
                if self.ready and not self.limit():self.execute()
            after=build(self)
            def in_findings(report,qid):
                return sorted(f['id'] for f in report['findings'] if qid in f['issue_ids'])
            for qid in sorted(queued):
                issue=self.issues[qid]
                selected=qid in manifest.get('selected_issues',[])
                attempt=self.session.attempts[-1] if len(self.session.attempts)==2 and selected else {}
                attempted=attempt.get('submission_state')=='submitted'
                delivered=attempted or bool(attempt.get('simulated') and attempt.get('response_received'))
                semantic_rows=(value or {}).get('semantic_rows_received',0) if delivered and selected else 0
                arrived=bool(delivered and value and (any(self.observed_feedback_ids.get(row['id'],row['id'])==qid for row in value['issues']) or semantic_rows or any(
                    self.semantics.questions.get(a['question'],{}).get('issue')==qid for a in value.get('answers',[]))))
                updates=[u for u in self.updates if u['issue']==qid and (u.get('evidence') or u.get('event')=='source_bound_semantic_answer_consumed')]
                why=next((r['reason'] for r in manifest.get('unexpanded_feedback_issues',[]) if r['issue']==qid),reason)
                if not why and not arrived:why='response_missing_or_unusable'
                if arrived and value and value.get('accepted_semantic_supports') and selected:
                    applicable={entry['support'] for entry in self.semantics.rules.labels_for(self.root(issue),manifest).values()}
                    for ref,entry in manifest.get('shown_supports',{}).items():
                        handle=self.semantics.rules.facts[entry['fact']]['handle']
                        if self.root(issue) in self.semantics.rules.related_ops(handle):applicable.add(entry['support'])
                    if set(value['accepted_semantic_supports']) & applicable:updates=updates+[{'event':'scoped_support_updated'}]
                if arrived and not updates:why='not_consumed_or_no_sourced_update'
                if not arrived or not updates and why:
                    self.coverage_gaps.append({'issue':qid,'category':issue['current'].get('category'),'reason':why})
                accepted_rows=len((value or {}).get('accepted_semantic_supports',())) if semantic_rows else 0
                self.feedback_trace.append({'issue':qid,'selected':selected,'sent':bool(attempted),'parsed':arrived,'consumed':bool(updates),
                    'semantic_rows_received':semantic_rows,'semantic_rows_accepted':accepted_rows,
                    'accepted_other_scopes':bool(accepted_rows and not updates),
                    'simulated':self.session.is_simulated(),'wire_evidence':manifest.get('wire_evidence',{}).get(qid,{}),
                    'submission_state':attempt.get('submission_state','not_dispatched'),'reason':why,'updates':[u['event'] for u in updates],
                    'changed_finding':in_findings(checkpoint,qid)!=in_findings(after,qid)})
            report=after
            report['provenance']['feedback_trace']=copy.deepcopy(self.feedback_trace)
            report.update(solver_resource=copy.deepcopy(solver_resource),timing={'program_investigation_seconds':self.program_seconds,'model_wait_seconds':self.session.model_wait_seconds,'task_wall_seconds':time.monotonic()-started})
        from .report import evaluation_projection
        before_projection=evaluation_projection(report)['predictions']
        write(self.out/'evidence_checks.json',evidence_summary(self.evidence))
        write(self.out/'query_checks.json',[query_summary(q) for q in self.backend.records])
        write(self.out/'semantic_status.json',semantic_summary(self.semantics.record()))
        report=public_report(report)
        if evaluation_projection(report)['predictions']!=before_projection:
            raise ValueError('decision_output_must_preserve_classification')
        h=write(self.out/'report.json',report)
        from .report import evaluation_projection
        projection=evaluation_projection(report)
        write(self.out/'prediction_manifest.json',{'report_sha256':h,'program_identity':self.f.identity,
            'implementation_sha256':self.f.context['implementation_sha256'],'predictions':projection['predictions'],
            'projection_canonical_sha256':digest(projection),'decision_sha256':report['decision_sha256'],'route_coverage_sha256':digest(report['task_analysis']['reading_scope']),
            'prediction_frozen_before_gold':True,'Gold_read':False,'real_model_calls':report['usage']['real_model_calls'],
            'fixture_run':self.session.is_simulated()})
        return report

def analyze(program,out,*,counter,client,deadline=None):return Investigation(program,counter,out,client,deadline).run()
