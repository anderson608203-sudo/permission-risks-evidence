# 实际运行源码完整分段

完整文件按原路径列出，哈希指原文件字节。

## source/src/pr_next_joint/investigation/engine.py

SHA-256 `738706abb19ddf86223e196c5893e6d8b4e7bcc01b8b6afb9b387c67da0c92bf`

```python
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
        prepared=program.program_clock_origin
        self.pending_amount_routes={}
        self.wall_origin=prepared
        self.f=program;self.out=Path(out);self.graph=ProgramGraph(program);self.catalog=Catalog(program,self.graph)
        self.context=SourceContext(program,self.catalog,counter);self.session=Session(program,self.context,self.out/'model',client)
        self.backend=Backend(program,self.catalog,self.graph);self.deadline=deadline
        self.backend.pending_amount_routes=self.pending_amount_routes
        from .summary import Semantics
        self.semantics=Semantics(program);self.backend.semantics=self.semantics
        self.issues={};self.initial_proposals={};self.actions=[];self.ready=[];self.shared_reads={};self.refinements=[];self.seen=set();self.evidence={};self.diagnostics=[]
        self.updates=[];self.call_decisions=[];self.model_analysis_available=False;self.explicit_empty_analysis=False
        self.usable_task_opinion=False;self.observed_feedback_ids={};self.task_declaration=None;self.program_seconds=0.;self.high_streak=0;self.order=0
        self.model_read_operations=set()
        self.reading_declarations=[];self.initial_manifest=None
        self.program_seconds=time.monotonic()-prepared
        self.graph.remaining=self.program_remaining
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
        if cat is None and (item.get('_host_source_question') or self.f.options.scope=='FCR' and item.get('_scope_effects')):return False
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
        if action=='compare' and args.get('context',{}).get('observable',{}).get('measure')=='financial_block':
            from .blocking import ordinary_control_uses
            root=self.root(q)
            if (not root or args.get('change')!=root or p.get('category') not in ('FCR-FREEZE','FCR-PAUSE')
                or oid not in ordinary_control_uses(self,root,p['category'])):return None
        if action=='inspect' and not args.get('enhance'):
            if oid in q['binding']['operations'] or oid in p.get('semantic_dependency_operations',[]) or oid in q.get('semantic_read_dependencies',()):
                return 'basic_source_read'
            return None
        if q.get('retired_property_parent'):return None
        relevant=set(p.get('semantic_dependency_operations',[]))|set(q['binding']['operations'])
        if oid not in relevant and not (action=='compare' and oid in getattr(self,'_coverage_control_routes',{}).get((self.root(q),p.get('category')),())):return None
        if not q.get('source_facts'):return 'resolve_source_prerequisite'
        view=scoped_opinion(self,q)
        if view['status']=='excluded':return None
        if view.get('productive_use') and action=='compare' and args.get('context',{}).get('observable',{}).get('measure')=='financial_block':return None
        if q.get('task_conflict') and q['current'].get('assessment')=='normal' and action=='prefix_search':
            return None
        if action=='sources' and view['status'] in ('risk','normal') and not q.get('task_conflict'):
            return None
        if q.get('semantic_recheck_property')==p.get('id') and p.get('id'):
            return 'changed_scope_requires_recheck'
        if args.get('enhance'):return 'critical_guard_or_source_effect'
        if action=='compare':
            measure=args.get('context',{}).get('observable',{}).get('measure')
            if view.get('productive_use') and not q.get('task_conflict') and measure=='callback':
                return None
            if view['status']=='normal' and view['reason'] in ('no_new_controlled_credit','parameter_only','intra_ledger_transfer','same_position_restored','no_debit_in_scope'):
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
        if action=='compare':
            q=self.issues[qid]
            ctx=arguments.get('context',{});bound=ctx.get('compiled_property') or {}
            measure=(ctx.get('observable') or {}).get('measure')
            from .property_model import validation_key
            if bound and any(
                r.get('change')==arguments.get('change') and r.get('observe')==arguments.get('observe')
                and r.get('property_validation_key')==validation_key(bound)
                and any(v.get('label')==measure and v.get('bounded_condition_confirmed') for v in r.get('queries',[]))
                for label in q['evidence'] for r in [self.evidence[label]]):
                self._note_action('reuse',qid,arguments['observe'],'same_validated_effect_for_this_scoped_use')
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
          'direct_read':action=='compare' and self._scoped_direct_read(q,arguments),
          'distinguishing_question':q['plan']['question'],'expected_information':trigger,
          'cost_class':'cheap source' if action in ('inspect','sources') and not arguments.get('enhance') else 'bounded behavior'})
    def _scoped_direct_read(self, q, args):
        context=args.get('context',{})
        prop=context.get('compiled_property') or {}
        root=self.root(q)
        if not root or args.get('change')!=root or args.get('observe')!=root or context.get('observable',{}).get('measure')!='direct_effect':
            return False
        direction={'FCR-MINT':'credit','FCR-DESTROY':'debit','FCR-TRANSFER':'debit'}.get(prop.get('category'))
        if not direction:return False
        return any(e['holder'] is not None and direction in e['may_directions']
                   and (e.get('key_role') or {}).get('kind')!='authorization_quantity'
                   for row in self.f.summaries.rows(root) for e in row['numeric_effects'])

    def _refines_located_amount(self,q,args):
        context=args.get('context',{})
        prop=context.get('compiled_property') or {}
        use=args.get('observe');change=args.get('change')
        if context.get('observable',{}).get('measure')!='financial_value' or not use or not change:return False
        rows=[v for v in prop.get('consent_rows',()) if v.get('operation')==use]
        if not rows:rows=[prop.get('financial_consents',{}).get(use) or {}]
        if not any(row.get('meaning') in ('gross_debit_bound','net_request_with_fee') for row in rows):return False
        return (change,use,prop.get('category')) in self.pending_amount_routes

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
            # A directly anchored amount control with a located holder-issued grant
            # is a stronger pending experiment than an incidental ledger-to-ledger use.
            # Neither the proposed label nor this priority supplies a risk decision.
            prop=context.get('compiled_property') or {}
            use=a['arguments'].get('observe')
            requested_use=bool(question.get('semantic_input') and use in prop.get('value_dependence',{}).get('value_uses',())
                and context.get('observable',{}).get('measure')=='financial_value' and
                (any(s.get('kind')=='financial_consent' and s.get('operation')==use for s in prop.get('semantic_questions',()))
                 or use in prop.get('financial_consents',{}) or any(s.get('operation')==use for s in prop.get('consent_rows',()))))
            relevant_block=(context.get('observable',{}).get('measure')=='financial_block'
                            and use in getattr(self,'_coverage_control_routes',{}).get((self.root(question),prop.get('category')),()))
            first_control=relevant_block and use==((question['plan'].get('observation_choice') or {}).get('selected') or {}).get('observe') and not any(
                self.evidence[label].get('source_control_result') for label in question['evidence'])
            named_control=first_control and bool(question.get('semantic_input'))
            return (not named_control,not first_control,not (requested_use or relevant_block),not self._refines_located_amount(question,a['arguments']),not semantic_recheck,a['priority'],-len(consumers),not a.get('direct_read'),not self.backend.reusable(a['action'],a['arguments']),a['cost_class']!='cheap source',service,o.get('source',{}).get('start',0),a['order'])
        if self.high_streak>=3:
            selected=min(available,key=lambda a:(self.root_service.get(self.root(self.issues[a['question']]) or a['question'],0),
                a['priority'],not a.get('direct_read'),self.issues[a['question']]['last_service'],a['order']));self.high_streak=0
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
        input_reads=set()
        located_issues=set()
        update_start=len(self.updates)
        if model and value.get('usable_analysis') and (not revision or value.get('response_kind')=='substantive'):
            envelope=value.get('original_envelope',{})
            declaration=envelope.get('task_analysis') or {}
            if isinstance(declaration,dict) and declaration.get('task')==self.f.options.scope and isinstance(declaration.get('basis'),str) and declaration['basis'].strip():
                refs=declaration.get('anchors') or value.get('reviewed') or []
                manifest=self.context.last_manifest or {}
                shown=set(manifest.get('expanded_operations',()))-set(manifest.get('partially_expanded_operations',()))
                located={oid for ref in refs if isinstance(ref,str) for oid in self.catalog.resolve(ref) if oid in shown} if isinstance(refs,list) else set()
                input_reads.update(located)
                self.model_read_operations.update(located)
                if located:self.usable_task_opinion=True
        if model and self.context.last_manifest:
            self.semantics.rules.submission=self.context.last_manifest.get('messages_sha256');self.semantics.rules.input_origin=origin
        seed_rows=bool(value.get('annotations') or value.get('policies'))
        if model and seed_rows and self.context.last_manifest:
            rules=self.semantics.rules
            accepted,errors=rules.apply(value,self.context.last_manifest,revision)
            value['semantic_rows_received']=len(value.get('annotations',()))+len(value.get('policies',()))
            self.diagnostics.extend(value.get('binding_diagnostics') or [{'reason':error} for error in errors])
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
                    sent=(self.context.last_manifest or {}).get('sent_semantic_rows',{}).get(sid)
                    current=self.semantics.questions.get(sid) or {}
                    entity=digest([current.get(k) for k in ('id','operation','target','kind','cell','semantic_scope','core_operation','quantity_scope')])
                    if wire and sent and wire['issue']==row['id'] and wire['display']==digest(sent) and wire['entity']==entity:
                        allowed_semantics.add(sid)
            for answer in value['answers']:
                sid=answer.get('question')
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
                q.setdefault('semantic_answers',[]).append(copy.deepcopy(answer))
                if row.get('policy_resolved') is False:
                    self.semantics.answer_dispositions[sid]={'meaning':row['meaning'],'kind':row['kind'],'identity':digest([sid,row['operation'],row['target'],row['scope'],row['quantity_scope']]),'has_scoped_alternative':row['meaning']=='other_source_explanation','resolved':False}
                else:q['version']+=1
                self.updates.append({'issue':q['id'],'event':('source_bound_answer_unresolved' if row.get('policy_resolved') is False else 'source_bound_semantic_answer_consumed'),
                    'answer':copy.deepcopy(answer),'binding':row,'evidence':list(q['evidence']),
                    'initial_state_modified':False})
                if model:self.usable_task_opinion=True
                if row.get('policy_resolved') is not False:answered.add(q['id'])
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
        proposals = list(value['issues'])
        if model and value.get('hypotheses'):
            from .semantic_audit_card import bind as bind_audit_card
            for index, card in enumerate(value['hypotheses']):
                manifest = self.context.last_manifest or {}
                if 'withdraw' in card:
                    ref = card['withdraw']
                    old = self.issues.get(ref)
                    effect = self.semantics.rules.bind(card['effect_ref'],manifest,'effect')
                    if (not revision or ref not in manifest.get('offered_audit_refs',()) or not old
                            or not old['current'].get('_audit_kind') or not effect
                            or effect not in old['current'].get('_scope_effects',())
                            or old.get('retired_property_parent')):
                        self.diagnostics.append({'list':'hypotheses','index':index,'reason':'withdrawal_outside_offered_support'})
                        continue
                    # Only this external hypothesis is withdrawn. A source-only
                    # question at that occurrence keeps its own applicability and evidence.
                    old['retired_property_parent'] = old.get('property',{}).get('id') or ref
                    old['version'] += 1
                    old.pop('_source_opinion', None)
                    cat = old['current'].get('category')
                    if cat:
                        self.semantics.rules.create_consumer(self.root(old),cat,set(old['current']['_scope_effects']))
                    self.updates.append({'issue':ref,'event':'scoped_audit_support_withdrawn','reason_sha256':digest(card['reason'])})
                    value.setdefault('audit_events',[]).append(ref)
                    continue
                proposal, error = bind_audit_card(self, card, manifest)
                if error:
                    self.diagnostics.append({'list':'hypotheses', 'index':index, 'reason':error})
                else:
                    proposals.append(proposal)
                    value.setdefault('audit_events',[]).append(proposal['id'])
        for incoming in proposals:
            if model:
                incoming,error=self.semantics.rules.scoped_issue(incoming,self.context.last_manifest or {})
                if error:
                    self.diagnostics.append({'issue':incoming['id'],'reason':error})
                    continue
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
            asked_scope=set(item.get('_scope_effects',()))
            explicitly_asked=[sid for sid,unit in allowed.items() if asked_scope and asked_scope==set(unit.get('requested_effects',())) and unit.get('sent_message_identity')]
            if revision and len(explicitly_asked)==1 and (qid not in self.issues or qid==explicitly_asked[0]):
                self.observed_feedback_ids[qid]=explicitly_asked[0]
                qid=explicitly_asked[0];old=self.issues[qid]
                item=dict(item,id=qid);applied_target=self.f.operations[self.root(old)]['target']
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
                if item.get('_scope_effects') and old['current'].get('_scope_effects') and set(item['_scope_effects']).isdisjoint(old['current']['_scope_effects']):
                    self.diagnostics.append({'issue':qid,'reason':'revision_outside_displayed_effect'})
                    continue
                for field,previous in old['current'].items():
                    if field not in item and not field.startswith('_host_') and field!='_semantic_consumer':item[field]=copy.deepcopy(previous)
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
            if model and item.get('_scope_effects') and item.get('category') is None and self.f.options.scope=='FCR' and binding.get('core_exact'):
                from .coverage import possible_properties
                oid=binding['core_operation']
                for category in possible_properties(self,[oid]):
                    self.semantics.rules.create_consumer(oid,category,set(item['_scope_effects']))
            if model and not revision and binding.get('core_exact') and item.get('assessment') in ('normal','risk','investigate'):
                located_issues.add(qid)
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
                first_reading=(len(explicitly_asked)==1 and explicitly_asked[0]==qid and old['current'].get('_host_source_question') and old['current'].get('assessment')=='investigate')
                if changed and not first_reading and (not cited or not reason):
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
                if old_key!=new_key and not first_reading and (not cited or not reason):
                    self.diagnostics.append({'issue':qid,'reason':'changed_property_requires_scoped_evidence',
                        'old_key':old_key,'candidate_key':new_key})
                    continue
                if correction or item['claim'].strip()!=before['claim'].strip() and cited and reason:
                    old['claim_source_scope']=self._claim_scope(binding)
                if binding['core_anchor'] is not None and 'root' in item:item['root']=binding['core_anchor']
                old['history'].append(before);old['current']=item;old['binding']=binding;old['version']+=1;old['revision_evidence']=cited
                if model:
                    old['semantic_input']=(origin,self.context.last_manifest.get('messages_sha256'))
                    for e in item.get('_scope_effects',()):self.semantics.rules.local_readers[e].add(qid)
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
                if model:
                    q['semantic_input']=(origin,self.context.last_manifest.get('messages_sha256'))
                    for e in item.get('_scope_effects',()):self.semantics.rules.local_readers[e].add(qid)
                self.issues[qid]=q;self.graph.node('issue:'+qid,'source_semantic_issue',item,'hypothesis')
                for oid in binding['operations']:self.graph.edge(oid,'issue:'+qid,'source_anchor',layer='hypothesis')
                for oid in ([self.root(q)] if q['binding']['core_exact'] else binding['operations']):
                    self.enqueue(qid,'inspect',{'operation':oid,'enhance':False},0 if q['task_conflict'] else 1,'minimum exact candidate source before optional solving')
                self._suggest(qid)
        if model and not revision and self.context.last_manifest:
            for locator in dict.fromkeys(value.get('located_amount_reads',())):
                self.semantics.rules.inspect_untyped_amount(locator,self.context.last_manifest)
        if model:
            attempt=self.session.attempts[-1]
            consumed=bool(input_reads or located_issues or value.get('accepted_semantic_supports') or len(self.updates)>update_start)
            attempt.update(protocol_usable=bool(value.get('usable_analysis')),usable=consumed,
                located_issue_count=len(located_issues),located_read_count=len(input_reads),
                accepted_support_count=len(value.get('accepted_semantic_supports',())),committed_update_count=len(self.updates)-update_start)
            self.model_analysis_available |= consumed and origin=='verified_service'
            self.fixture_analysis_available = getattr(self,'fixture_analysis_available',False) or (consumed and origin=='fixture')
            write(self.session.out/f"attempt_{attempt['index']}.json",attempt)

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
        if q.get('evidence') and any(self.evidence[e].get('property_validation_key') == validation_key(prop)
                                   for e in q['evidence']):
            existing = compose(self, q)
            if existing['reportable'] or existing['scope'].get('route_status') == 'excluded':
                q.setdefault('evidence_revalidations', []).append({
                    'property': prop['id'], 'key': validation_key(prop),
                    'from_properties':sorted({self.evidence[e]['property_identity'] for e in q['evidence']
                        if self.evidence[e].get('property_identity') and self.evidence[e].get('property_validation_key')==validation_key(prop)}),
                    'reason': 'same source, domain, subjects, effects, assumptions and semantic meaning'})
        view=planning_item(q)
        q['plan']=self._plan(q['binding'],view)
        q['task_review']=self._task_review(view,q['binding'])
        q['task_conflict']=self.task_conflict(view) or q['task_review']['status']!='no_explicit_conflict'
        if prop.get('category') in ('FCR-FREEZE','FCR-PAUSE'):
            from .blocking import ordinary_control_uses
            root=self.root(q)
            uses=ordinary_control_uses(self,root,prop['category']) if root else ()
            q['plan'].pop('observation_choice',None)
            if uses:
                use=next(iter(uses))
                ctx={'observable':{'measure':'financial_block'},'compiled_property':prop,'property_identity':prop['id'],'semantic_version':prop.get('semantic_version')}
                q['plan']['observation_choice']={'selected':{'change':root,'observe':use,'measure':'financial_block','context':ctx,'expectations':{},'scope':{'target':prop['target'],'controls':linked_controls(self,root,use),'objects':prop['objects']}},
                    'request_resolution':{'use':use,'possible_uses':list(uses),'unmeasured_uses':list(uses[1:])},
                    'status':'source_property_selected','reason':'ordinary positive outgoing request; baseline requires actual comparison'}
                for reader in uses:
                    self.enqueue(qid,'compare',{'change':root,'observe':reader,'context':ctx},0,'compare the matched outgoing request before optional searches')
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
            from .source_opinion import scoped_opinion
            direct=scoped_opinion(self,q)
            if direct['status']=='risk' and direct['reason'] in ('existing_rights_moved','uncompensated_debit','new_entitlement') and not prop.get('semantic_questions'):
                # Children and existing hard evidence have already been registered.
                # Keep independently queued work; this path needs no new prefixes.
                q.setdefault('source_decisions',[]).append({'reason':'committed_direct_holder_effect','property':prop['id']})
                return
            for use in prop.get('value_dependence',{}).get('value_uses',[]):
                ctx=self._compare_context(q,root,use)
                ctx.update(observable={'measure':'financial_value'},compiled_property=copy.deepcopy(prop),
                           property_identity=prop['id'],semantic_version=prop['semantic_version'])
                self.enqueue(qid,'compare',{'change':root,'observe':use,'context':ctx},2,
                    'follow the actual value dependency into the same holder request, consent and final ledger effect')
        choice=q['plan'].get('observation_choice')
        # A locally compiled policy addresses this entry even when no cross-entry
        # observation was nominated. Preserve its real amount/payment operands.
        authorization=(prop.get('expected_authorization') or {}).get('compiled_authorization') or {}
        if not (choice or {}).get('selected') and (authorization.get('source_requirement') or {}).get('kind')=='source_role_payment_policy':
            context=self._compare_context(q,root,root)
            context.update(observable={'measure':'authorization_violation','authorization':authorization},
                           compiled_property=prop,property_identity=prop['id'],semantic_version=prop['semantic_version'])
            self.enqueue(qid,'compare',{'change':root,'observe':root,'context':context},1,'check the actual committing role or paid path against the bound policy')
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
        if planned and result.get('stopped_reason')=='await_source_bound_consent_interpretation':
            for probe in result.get('queries',()):
                if probe.get('label')!='financial_consent_unresolved' or not probe.get('bounded_condition_confirmed'):continue
                details=probe.get('details') or {}
                pid=details.get('use_path') or details.get('after_path')
                if pid and details.get('ledger') is not None:
                    route=(result['change'],result['observe'],planned.get('category'))
                    self.pending_amount_routes.setdefault(route,set()).add((pid,digest(details['ledger'])))
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
        start=time.monotonic();self.backend.deadline=start+self.program_remaining()
        investigation_deadline=self.backend.deadline
        yielded_to_semantics=False
        try:
            while self.ready and not self.limit():
                # A bounded, located effect is already waiting only on its holder convention.
                # Give its one semantic reply time to be used; other roots have had their basic read.
                if reserve_for_feedback and not basic_only and self.pending_amount_routes:
                    yielded_to_semantics=True;break
                if reserve_for_feedback and self.program_seconds+time.monotonic()-start>=min(300.,self.f.options.seconds/2) and any(
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
                quantum=max(self.f.options.solver_timeout_ms/1000.,min(60.,self.f.options.seconds/6.))
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
    def feedback(self,checkpoint=None):
        questions=[]
        # An entry-level host placeholder can survive even after a sibling issue
        # settled its single actual write. Compare the exact effects at this checkpoint.
        rules=self.semantics.rules
        settled_ac=set()
        for item in (checkpoint or {}).get('inspection_records',()):
            result=item['assessment_result'];d=result['scope']['decision']
            if result['category']!='AC' or d['status'] not in ('risk','normal','excluded'):continue
            for effect in d.get('effects',()):
                entry=rules.effects.get(effect)
                if entry and any(entry['where'].get('ast_id')==p.get('ast_id') and
                    entry['where'].get('file')==p.get('file') for p in d.get('locations',())):
                    settled_ac.add(effect)
        for q in sorted(self.issues.values(),key=lambda q:(not any(x['outcomes'] for x in q.get('observations',[])),not q['task_conflict'],q['id'])):
            if q.get('retired_property_parent') or q.get('source_only_amount_read'):continue
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
                semantic_questions.append(s)
            semantic_questions.extend(self.semantics.rules.semantic_questions_for(q))
            if (q['current'].get('_host_source_question') and not q['task_conflict']
                    and not q['current'].get('alternative') and not q.get('observations')
                    and assessment['category']=='AC' and assessment['scope']['decision'].get('reason')=='policy_missing'):
                oid=self.root(q)
                effect_set=set(q['current'].get('_scope_effects') or rules.by_operation.get(oid,()))
                # Only the same actual object is covered. Other branches, a new
                # scoped dispute, or a genuinely separate holder duty stay eligible.
                if effect_set and effect_set<=settled_ac and len({rules.occurrence(e) for e in effect_set})==1:
                    new_questions=[s for s in semantic_questions if s.get('kind')!='authorization' or s.get('operation')!=oid]
                    if len(new_questions)!=len(semantic_questions):
                        self.feedback_trace.append({'issue':q['id'],'selected':False,'sent':False,'consumed':False,
                            'reason':'same_effect_authorization_already_decided','changed_finding':False})
                        semantic_questions=new_questions
                        if not semantic_questions:continue
            # Prefer the exact unanswered permission at the use where the remaining
            # quantity convention could change a measured effect. This priority is
            # local to selection; the display and binding still use the full entity.
            for idx,question in enumerate(semantic_questions):
                if question.get('kind')!='financial_consent':continue
                routes={(v['path'],digest(v['ledger'])) for v in question.get('quantity_scope',())}
                checked=self.pending_amount_routes.get((self.root(q),question.get('operation'),(q.get('property') or {}).get('category')),set())
                if routes & checked:
                    question=copy.deepcopy(question)
                    question['_observed_amount_dispute']=True
                    semantic_questions[idx]=question
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
               **({'audit_ref':q['id']} if q['current'].get('_audit_kind') and q.get('semantic_input')
                     and q['current'].get('alternative') else {}),
               'semantic_questions':copy.deepcopy(semantic_questions),
              'decision':{'unresolved':gap,'program_observed':measure,'changes':'only the linked property in its recorded scope'},
              'scope_note':'Clarify actual actor, grant and effect.' if q['task_conflict'] else 'Only this question.'})
        if checkpoint and self.f.options.scope=='AC' and self.program_remaining()>0:
            rules=self.semantics.rules
            shown=set(self.initial_manifest.get('displayed_effect_handles',()))
            already={e for q in self.issues.values() if q.get('semantic_input') for e in q['current'].get('_scope_effects',())}
            closed={e for row in checkpoint['inspection_records'] for a in [row['assessment_result']['scope']['decision']]
                    if a['status'] in ('risk','normal','excluded') for e in a.get('effects',())}
            candidates=[e for e in rules.sensitive_effects if e not in closed|already and (e not in shown or not self.session.attempts[0].get('usable'))]
            priority={'qualification':0,'funds':1,'termination':2,'call_authority':3,'credit':4,'account_movement':5}
            for e in sorted(candidates,key=lambda k:(k in shown,rules.overwritten(k),priority[rules.sensitive_effects[k]],rules.effects[k]['where']['start'],k)):
                d=rules.effects[e];es=rules.occurrences[self.semantics.rules.occurrence(e)]
                if set(es)&(closed|already):continue
                q=rules.create_consumer(d['oid'],'AC',set(es))
                if not q:continue
                questions=[row for row in questions if row['id']!=q['id']]
                questions.insert(0,{'id':q['id'],'claim':'Which duty applies at the indicated source effect, who decides, and is there a conflict?',
                    'assessment':'investigate','category':'AC','anchors':[self.catalog.name(d['oid'])],
                    'operations':[d['oid']],'new_evidence_labels':[],'evidence':[],'semantic_questions':[],'requested_effects':list(es),'local_effect_review':True})
                break
        return {'questions':questions}
    def run(self):
        from .decision_output import public_report,context_summary,coverage_summary,receipt,query_summary,evidence_summary,semantic_summary
        started=self.wall_origin;self.out.mkdir(parents=True,exist_ok=True)
        t=time.monotonic()
        self.semantics.rules.register_sensitive_effects()
        bridge = self.semantics.rules.authority_bridges
        # Only structural locations, opaque identities, and typed state leave the host.
        write(self.out/'shared_effects.json', {
            'build':self.f.bundle['build_id'], 'target_scoped':True,
            'edges':{uid:{k:v for k,v in link.items() if k not in ('read_path',)}
                     for uid,link in bridge.items()}})
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
        with budget(self.f.options.seconds,remaining=self.backend.remaining,timeout_ms=self.f.options.solver_timeout_ms) as solver_resource:
            reserve=bool(self.f.options.feedback and len(self.session.attempts)<self.f.options.attempt_limit)
            self.execute(basic_only=True)
            basic=build(self)
            write(self.out/'checkpoint_basic.json',public_report(basic))
            from .candidates import investigate_obligations
            initial_obligations=basic
            write(self.out/'initial_obligations.json',coverage_summary(initial_obligations['task_analysis']['reading_scope']))
            investigate_obligations(self,initial_obligations)
            self.execute(reserve_for_feedback=reserve)
            checkpoint=build(self);write(self.out/'checkpoint_initial.json',public_report(checkpoint))
            feedback=self.feedback(checkpoint)
            first_attempt=self.session.attempts[0] if self.session.attempts else {}
            verified=bool(first_attempt.get('response_identity_verified'))
            recovery=verified and (initial or {}).get('response_kind') in ('empty_body','invalid_protocol')
            feedback_start=len(self.updates)
            reason=None
            queued={q['id'] for q in feedback['questions']}
            for qid in self.issues.keys()-queued:
                self.feedback_trace.append({'issue':qid,'selected':False,'sent':False,'parsed':False,'consumed':False,
                    'reason':'no_new_discriminating_evidence','changed_finding':False})
            manifest={};value=None
            if not self.f.options.feedback:reason='feedback_disabled'
            elif len(self.session.attempts)>=self.f.options.attempt_limit:reason='attempt_limit'
            elif not verified:reason='initial_service_result_unconfirmed'
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
                            q['semantic_questions']=[s for s in q.get('semantic_questions',[]) if s['id'] in manifest['semantic_wire']]
                            q['sent_message_identity']=manifest['messages_sha256']
                    write(self.out/'feedback_receipt.json',receipt(feedback,'scoped_semantic_feedback'))
                    value=self.session.request(feedback=feedback,recovery=recovery,prepared=(preview,manifest))
                    self.call_decisions.append({'phase':'followup','sent':bool(self.session.attempts[-1].get('actual_model_submissions')),
                      'actual_model_submissions':self.session.attempts[-1].get('actual_model_submissions',0),'simulated':self.session.is_simulated(),
                      'reason':'necessary_protocol_recovery' if recovery else 'scoped_distinguishing_evidence_or_task_conflict','attempt_status':self.session.attempts[-1].get('status'),'manifest':manifest})
                    t=time.monotonic();self.accept(value,revision=not recovery,feedback=feedback);self.program_seconds+=time.monotonic()-t
                    if not self.limit():
                        # Service changed source/policy dependencies before optional search.
                        # Freeze the actual reading separately; the initial snapshot stays immutable.
                        self.execute(basic_only=True)
                        revised_basic=build(self)
                        write(self.out/'checkpoint_feedback.json',public_report(revised_basic))
                        investigate_obligations(self,revised_basic)
                        self.execute()
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
                received=value or {}
                selected_refs=manifest.get('shown_supports',{}) if selected and delivered else {}
                selected_sids={sid for sid,row in manifest.get('semantic_wire',{}).items() if row['issue']==qid}
                rules=self.semantics.rules
                effects=set(issue.get('effect_scope') or issue['current'].get('_scope_effects') or ())
                if not effects:
                    effects=set(rules.by_operation.get(self.root(issue),()))
                def relevant(row):
                    if not selected or not delivered:return False
                    wire=selected_refs.get(row.get('ref'),{})
                    fid=wire.get('fact') or row.get('fact')
                    fact=rules.facts.get(fid,{})
                    if not fact:return False
                    if fact.get('scope'):return fact['scope'] in effects
                    h=fact.get('handle')
                    if h in effects:return True
                    return bool(set(rules.by_decl.get(h,())) & effects or
                                any(end in effects and exact for end,_,_,exact in rules.routes.get(h,())))
                events=received.get('semantic_binding_events',())
                touched=[row for row in events if relevant(row)]
                semantic_rows=len(touched)
                accepted_rows=sum(bool(row['accepted']) for row in touched)
                other_accepted=sum(bool(row['accepted']) for row in events)-accepted_rows if selected and delivered else 0
                updates=[u for u in self.updates[feedback_start:] if selected and delivered and u['issue']==qid]
                if accepted_rows:updates.append({'event':'shown_scope_support_committed'})
                arrived=bool(selected and delivered and (touched or qid in received.get('audit_events',()) or any(
                    a['question'] in selected_sids for a in received.get('answers',())) or any(
                    self.observed_feedback_ids.get(row['id'],row['id'])==qid for row in received.get('issues',()))))
                why=next((r['reason'] for r in manifest.get('unexpanded_feedback_issues',[]) if r['issue']==qid and not selected),reason)
                if not why and not arrived:why='response_missing_or_unusable'
                if arrived and not updates:why='not_consumed_or_no_sourced_update'
                if not arrived or not updates and why:
                    self.coverage_gaps.append({'issue':qid,'category':issue['current'].get('category'),'reason':why})
                self.feedback_trace.append({'issue':qid,'selected':selected,'sent':bool(attempted),'parsed':arrived,'consumed':bool(updates),
                    'semantic_rows_received':semantic_rows,'semantic_rows_accepted':accepted_rows,
                    'answered_unresolved':any(u.get('event')=='source_bound_answer_unresolved' for u in updates),
                    'accepted_other_scopes':bool(other_accepted),'other_scope_accepted_rows':other_accepted,
                    'simulated':self.session.is_simulated(),'wire_evidence':manifest.get('wire_evidence',{}).get(qid,{}),
                    'submission_state':attempt.get('submission_state','not_dispatched'),'reason':why,'updates':[u['event'] for u in updates],
                    'changed_finding':in_findings(checkpoint,qid)!=in_findings(after,qid)})
            report=after
            report['provenance']['feedback_trace']=copy.deepcopy(self.feedback_trace)
            report.update(solver_resource=copy.deepcopy(solver_resource),timing={'program_investigation_seconds':max(0.0,time.monotonic()-started-self.session.model_wait_seconds),'clock_scope':'facts_through_final_decision','model_wait_seconds':self.session.model_wait_seconds,'task_wall_seconds':time.monotonic()-started})
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

```

## source/src/pr_next_joint/investigation/financial_value.py

SHA-256 `cded0238a599948cb7046d0eeb49b98e69eae6de127dc288cb23e2987ec5111b`

```python
"""Source-bound value intervention and the same holder request in two worlds.

Quantity facts are not consent policies. Every financial capability retains
its own holder, ledger, request, privilege and normal-explanation conditions.
"""
from itertools import product
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import selectors, keys, selector_relation
from pr_next_joint.verification.program_encoding import MechanismEncoder
from pr_next_joint.verification.sequence import qualify, read
from pr_next_joint.verification.source_worlds import encode_frame
from pr_next_joint.verification.expressions import Unsupported
from .ledger import movements, flow, unit_origin, grant_for, native_only_position
from .roles import path_qualification, fixed_role_terms


def family_delta(e, lookup, fr, positions, family):
    """Sum final net changes once per *runtime* position, including aliases."""
    z=e.z;seen=[];parts=[]
    for cell in positions:
        if selector_relation(cell,family)!='same_shape':continue
        probe=qualify(cell,fr['slot'])
        ks=[e.expr(read(k,fr['before'],lookup)) for k in keys(probe)]
        duplicate=z.Or(*[z.And(*[a==b for a,b in zip(ks,prior)]) for prior in seen])
        before=e.expr(read(probe,fr['before'],lookup))
        after=e.expr(read(probe,fr['before']+fr['writes'],lookup))
        parts.append(z.If(duplicate,0,after-before));seen.append(ks)
    return z.Sum(*parts) if parts else z.IntVal(0)


def consent(b,e,oid,path,fr,cell,holder,net_debit,interpretation=None):
    """Sufficient scoped consent and the residual when an amount basis differs.

    Self requests and an exclusively holder-issued bound covering final debit
    can refute an unauthorized-loss claim. An under-covered numeric guard is
    not automatically a normative requirement for gross authorization.
    """
    z=e.z;lookup=b.f.lookup(oid);caller=e.expr(fr['caller'])
    grant=grant_for(b,oid,path,cell)
    allowed=[holder==caller];basis={'self_request_checked':True,'grant':grant}
    if grant is None:
        # Boolean delegation is meaningful only if every non-revocation
        # writer addresses the actual issuer's own ordered holder key.
        from .summary import holder as source_holder
        who=source_holder(cell,lookup)
        def conjuncts(g):
            return [x for a in g['args'] for x in conjuncts(a)] if g.get('op') in ('and','&&') else [g]
        for raw in path['guards']:
            for g in conjuncts(raw):
                if g.get('kind')!='storage' or len(keys(g))!=2:continue
                indices=keys(g);matches=[i for i,k in enumerate(indices) if key(k)==key(who)]
                if len(matches)!=1 or indices[1-matches[0]].get('kind')!='actual_sender':continue
                h=matches[0]
                writers=[w for w in b.f.writes.values() if b.f.operations[w['operation']]['target']==b.f.operations[oid]['target']
                         and selector_relation(w['raw']['path'],g)=='same_shape']
                if writers and all(len(keys(w['raw']['path']))==2 and
                    (keys(w['raw']['path'])[h].get('kind')=='actual_sender' or
                     w['raw']['value'].get('kind')=='literal' and str(w['raw']['value'].get('value')).lower() in ('false','0')) for w in writers):
                    allowed.append(e.expr(read(qualify(g,fr['slot']),fr['before'],lookup)))
                    basis.setdefault('boolean_holder_delegations',[]).append(g)
        return z.Or(*allowed),True,basis
    from .summary import holder as source_holder
    who=source_holder(cell,lookup)
    indices=[i for i,k in enumerate(keys(grant)) if key(k)==key(who)]
    if len(indices)!=1:
        return z.Or(*allowed),False,dict(basis,reason='grant_issuer_key_not_uniquely_source_bound')
    # Direct program consumers already supply the unique path-bound grant. A wire
    # interpretation additionally has to match its explicit issued quantity scope.
    if interpretation and 'quantity_scope' in interpretation and not any(key(route['grant'])==key(grant) and route['issuer_key']==indices[0] and
                                  route['spender_key']==1-indices[0] for route in interpretation.get('quantity_scope',())):
        interpretation=None
    h=indices[0]
    writers=[w for w in b.f.writes.values() if b.f.operations[w['operation']]['target']==b.f.operations[oid]['target']
             and selector_relation(w['raw']['path'],grant)=='same_shape']
    foreign=[]
    for w in writers:
        dst,val=w['raw']['path'],w['raw']['value'];args=val.get('args',[])
        holder_issued=len(keys(dst))==2 and keys(dst)[h].get('kind')=='actual_sender'
        reduction=val.get('op')=='-' and args and key(args[0])==key(dst)
        if not holder_issued and not reduction:foreign.append(w['operation'])
    effective=e.expr(read(qualify(grant,fr['slot']),fr['before'],lookup))
    basis.update(holder_key=h,foreign_writers=sorted(set(foreign)),
        amount_rule='cover the final same-holder debit, including same-path refunds',
        normative_gross_rule_inferred=False)
    if foreign:
        # An installable allowance cannot certify actual holder issuance.
        # Its provenance is a separate obligation, not an invented consent.
        return z.Or(*allowed),False,dict(basis,reason='grant_provenance_has_nonholder_writers')
    allowed.append(effective>=net_debit)
    meaning=(interpretation or {}).get('meaning')
    if meaning=='net_request_with_fee':
        # This H interpretation is scoped to the source-bound grant/use and
        # keeps the actual checked gate and fee computation in the execution.
        # A default/used-up zero slot is not evidence that this holder issued
        # an active fee-bearing authorization. A net-amount interpretation
        # alone cannot turn it into unconditional consent for a positive
        # gross debit. Retain that provenance gap; do not infer a new gross
        # policy or automatically classify the gap as a financial violation.
        allowed.append(effective>0)
    basis.update(interpretation=interpretation,quantity_basis_resolved=meaning in ('gross_debit_bound','net_request_with_fee'),
        positive_active_grant_required_for_net_fee_consent=meaning=='net_request_with_fee',
        zero_grant_is_not_holder_issuance=meaning=='net_request_with_fee')
    return z.Or(*allowed),meaning=='gross_debit_bound',basis


def scoped_final_debit(inv,q,rows):
    """Compare the final same-account debit with the actual ordered, holder-issued cap."""
    from .source_opinion import opinion,role_ids,blocked_positive,feasible_source_guards
    from .summary import holder,local_delta
    from .policy_binding import conjuncts
    f=inv.f;oid=inv.root(q);rules=inv.semantics.rules;lookup=f.lookup(oid)
    reached=[]
    for r in rows:
        if not r['committing']:continue
        if r['effects'] or r['residuals']:return None
        results=[]
        for e in rules.route_scopes(q):
            d=rules.effects[e]
            if d.get('path')!=r['path'] or 'write' not in d:continue
            w=d['write'];cell=w['path'];account=holder(cell,lookup)
            if not account or local_delta(w)[0]!='-' or not unit_origin(inv.backend,oid,cell):continue
            if not role_ids(inv,oid,r) or native_only_position(inv.backend,oid,cell):continue
            if account.get('kind')=='actual_sender':
                ans=opinion('normal','voluntary_holder_debit',[d['where']]);ans['same_scope_authorized']=True
                results.append(ans);continue
            side=[ow for ow in r['ordered_writes'] if selector_relation(cell,ow['path'])=='same_shape']
            # Multi-position settlement is settled by the general final-state comparison.
            if len(side)!=1:continue
            for route in rules.quantity_scopes(e):
                cap=route['grant']
                expressions=f.summaries.dependencies.expressions
                amount=expressions.get(route['debit_expression']);used=expressions.get(route['checked_quantity_expression'])
                if not amount or not used or not feasible_source_guards(r['guards']):continue
                guards=[g for term in r['guards'] for g in conjuncts(term)]
                if not any((g.get('op') in ('>=','>') and [key(a) for a in g.get('args',())]==[key(cap),key(used)])
                        or (g.get('op') in ('<=','<') and [key(a) for a in g.get('args',())]==[key(used),key(cap)])
                        for g in guards):continue
                if not any(key(g['path'])==key(cap) and local_delta(g)[0]=='-' and
                           key(local_delta(g)[1])==key(used) for g in r['ordered_writes']):continue
                source_writers=[v['raw'] for v in f.writes.values() if f.operations[v['operation']]['target']==d['target']
                    and selector_relation(v['raw']['path'],cap)=='same_shape' and local_delta(v['raw'])[0]!='-']
                if not source_writers or any(keys(v['path'])[route['issuer_key']].get('kind')!='actual_sender' for v in source_writers):continue
                bound=rules.financial_consent(oid,route) or {}
                known=bound.get('meaning');qty=local_delta(w)[1]
                same=key(used)==key(qty)
                if same:
                    ans=opinion('normal','covered_holder_grant',[d['where']]);ans['same_scope_authorized']=True
                elif known not in ('net_request_with_fee','gross_debit_bound'):
                    ans=opinion('open','holder_consent_basis_unresolved',[d['where']]);ans['decisive_consent_gap']=True
                else:
                    # A fee policy qualifies the exact grant. A positive active net cap
                    # must be consumed. No consent is inferred from a default zero slot.
                    fee_args=used.get('args',[])
                    short=(used.get('op')=='-' and len(fee_args)==2 and key(fee_args[0])==key(qty)
                           and fee_args[1].get('kind')=='literal' and type(fee_args[1].get('value')) is int
                           and fee_args[1]['value']>0)
                    if not short:continue
                    floor=fee_args[1]['value']
                    guards=[g for group in r['guards'] for g in conjuncts(group)]
                    positive_net=any(g.get('op') in ('>','>=') and len(g.get('args',()))==2 and
                        key(g['args'][0])==key(qty) and type(g['args'][1].get('value')) is int and
                        g['args'][1]['value']+(g['op']=='>')>floor for g in guards)
                    if not positive_net:continue
                    if known=='net_request_with_fee':
                        ans=opinion('normal','scoped_fee_consent',[d['where']]);ans['same_scope_authorized']=True
                    else:
                        # A positive instance must also permit the checked grant to
                        # lie below the debit. Preserve tighter caps and hard refutations.
                        from pr_next_joint.frontend.path_ir import conditions_possible,op
                        if blocked_positive(inv,q,r['path'],'FCR-DESTROY'):continue
                        if not conditions_possible(r['guards']+[op('<',cap,qty), op('!=',account,{'kind':'actual_sender'})]):continue
                        ans=opinion('risk','uncompensated_debit',[d['where']])
                ans['source_relation']={'family':'final_holder_debit','duty':'ordered_holder_cap_and_same_ledger_net_loss',
                                         'support_location':d['where']}
                results.append(ans)
        if not results:return None
        reached.extend(results)
    if not reached:return None
    return next((r for r in reached if r['status']=='risk'),next((r for r in reached if r['status']=='open'),reached[0]))


def interpretation_for(prop,use,pid,cell):
    rows=[c for c in prop.get('consent_rows',()) if c.get('operation')==use and any(s['path']==pid and key(s['ledger'])==key(cell) for s in c.get('quantity_scope',()))]
    if rows and len({c['meaning'] for c in rows})!=1:return None
    row=rows[0] if rows else prop.get('financial_consents',{}).get(use) or prop.get('financial_consent')
    if row and any(s['path']==pid and key(s['ledger'])==key(cell)
                   for s in row.get('quantity_scope',[])):return row
    return None


def proved_exclusion(query):
    return query['answer']=='unsat' and (query.get('exclusion_certificate',{}).get('excludes_only_this_formula') or
        query['details'].get('prestate',{}).get('global_reachability_exhausted'))


def causal_credits(b,oid,path,cell):
    """Same-ledger receivers tied to the debit's source quantity expression."""
    from .summary import local_delta
    debits=[local_delta(w)[1] for w in path['writes'] if key(w['path'])==key(cell) and local_delta(w)[0]=='-']
    result=[]
    for candidate in movements(b,oid,path)['+']:
        if selector_relation(candidate,cell)!='same_shape' or key(candidate)==key(cell):continue
        amounts=[local_delta(w)[1] for w in path['writes'] if key(w['path'])==key(candidate) and local_delta(w)[0]=='+']
        if any(key(a)==key(part) for a in debits for amount in amounts for part in walk(amount)):
            result.append(candidate)
    return result


def payment_part(amount,whole):
    if not isinstance(amount,dict) or not isinstance(whole,dict):return False
    if key(amount)==key(whole):return True
    args=amount.get('args',[])
    if len(args)!=2:return False
    if amount.get('op')=='-':return payment_part(args[0],whole)
    if amount.get('op')=='/' and args[1].get('kind')=='literal' and isinstance(args[1].get('value'),int) and args[1]['value']>0:
        return payment_part(args[0],whole) or (args[0].get('op')=='*' and any(key(v)==key(whole) for v in args[0].get('args',[])))
    return False

def distributed_value(b,e,oid,path,fr,cell,holder,*,all_transfers):
    """Final same-unit distributions. The holder's own credits are already in flow().
    Count all causally paired recipients for a movement check. For destruction,
    allocate only the portion backed by a real transfer of these units; unrelated
    credits, e.g. independent issuance in the same entry, never offset a debit.
    """
    z=e.z;lookup=b.f.lookup(oid);seen=[];parts=[]
    from .summary import local_delta
    related=causal_credits(b,oid,path,cell)
    debits=[local_delta(w)[1] for w in path['writes'] if key(w['path'])==key(cell) and local_delta(w)[0]=='-']
    for c in related:
        if not all_transfers:
            credits=[local_delta(w)[1] for w in path['writes'] if key(w['path'])==key(c) and local_delta(w)[0]=='+']
            # Amount provenance must be a payment or a portion of the debit.
            # Merely mentioning the amount (e.g. minting a multiple) is not allocation.
            if not credits or not all(any(payment_part(amount,whole) for whole in debits) for amount in credits):continue
        h,start,end,_,_=flow(e,lookup,fr,c)
        probe=qualify(c,fr['slot'])
        ks=[e.expr(read(k,fr['before'],lookup)) for k in keys(probe)]
        duplicate=z.Or(*[z.And(*[a==v for a,v in zip(ks,prior)]) for prior in seen])
        from .shared_effect_bridge import zero_key_spendable
        usable_recipient = z.BoolVal(True) if not all_transfers and zero_key_spendable(b, oid, c) else h != 0
        real_credit=z.And(h!=holder,usable_recipient,z.Not(duplicate),end>start)
        if not all_transfers:
            # A credit larger than the entire causally debited quantity may be independent
            # issuance. Count it as payment only in a state where the allocation fits.
            if any(key(amount)!=key(whole) for amount in credits for whole in debits) and not all(
                    amount.get('op')=='-' and any(key(amount['args'][0])==key(whole) for whole in debits)
                    for amount in credits):
                available=sum((e.expr(read(qualify(amount,fr['slot']),fr['before'],lookup)) for amount in debits),z.IntVal(0))
                real_credit=z.And(real_credit,end-start<=available)
        parts.append(z.If(real_credit,end-start,0));seen.append(ks)
    return z.Sum(*parts) if parts else z.IntVal(0)


def native_settlement(b,e,oid,fr,cell,holder):
    """Only exact native-unit provenance can bind a native payment to a debit.

    A token name, a coincident payment or another asset never supplies an
    exchange rate. Success and recipient conditions are those of this same
    committed source frame. A partial payment offsets only its actual amount.
    """
    z=e.z;origin=b._native_unit_source(oid,cell)
    payments=[fx for fx in fr['effects'] if fx.get('kind')=='native_transfer']
    basis={'unit_source':origin,'same_frame_payments':payments,
           'same_holder_required':True,'cross_asset_rate_assumed':False}
    if not origin or not payments:return z.IntVal(0),basis
    from pr_next_joint.frontend.path_ir import lit
    paid=z.Sum(*[z.If(z.And(e.expr(fx['recipient'])==holder,e.expr(fx.get('success',lit(True)))),e.expr(fx['amount']),0) for fx in payments])
    return paid,basis


def post_exclusion(b,change,use,cid,cp,pid,path,cell,prop):
    """Check a necessary harmful effect without assuming W0 could commit.

    Only UNSAT can close this route. SAT here is not a causal intervention
    finding. This prevents an infeasible baseline from becoming 'no risk'.
    """
    def calculate():
        from .behavior import ordered_clocks
        e=MechanismEncoder(b.f.lookup(use));z=e.z;lookup=e.lookup
        cf=b.source_frame(change,cid,0);uf=b.source_frame(use,pid,1,cf['writes'])
        qualification=path_qualification(b.f,change,cp)
        roles,origins=fixed_role_terms(e,qualification,0)
        h,start,end,_,_=flow(e,lookup,uf,cell);actor=e.expr(cf['caller']);requester=e.expr(uf['caller'])
        net=start-end;cat=prop['category']
        permitted,resolved,basis=consent(b,e,use,path,uf,cell,h,net,interpretation_for(prop,use,pid,cell))
        if cat=='FCR-MINT':
            from .relations import beneficiary_condition
            controlled,why=beneficiary_condition(e,uf,cell,h,controller_frame=cf)
            no_debit=[flow(e,lookup,uf,c)[2]>=flow(e,lookup,uf,c)[1] for c in movements(b,use,path)['-']
                      if selector_relation(c,cell)=='same_shape']
            harmful=z.And(end>start,controlled,*no_debit)
        else:
            credited=distributed_value(b,e,use,path,uf,cell,h,all_transfers=cat=='FCR-TRANSFER')
            paid,settlement=native_settlement(b,e,use,uf,cell,h)
            harmful=z.And(net>0,h!=actor,z.Not(permitted),credited>0 if cat=='FCR-TRANSFER' else net>credited+paid)
        detail={'operation':change,'change':change,'observe':use,'target':prop['target'],
            'change_path':cid,'use_path':pid,'ledger':cell,'category_hypothesis':cat,
            'property_identity':prop['id'],'semantic_version':prop['semantic_version'],
            'property_validated':True,'proof_use':'UNSAT necessary post-effect exclusion only',
            'baseline_success_not_assumed':True,'holder_consent':basis,'role_origins':origins}
        q=b._query(e,z.And(encode_frame(e,cf),encode_frame(e,uf),*roles,*ordered_clocks(e,1),
                          actor!=0,requester!=0,h!=0,harmful),'financial_value_post_exclusion',detail)
        return {'queries':[q],'local_errors':[]}
    result=b.memo('value_post_exclusion',[change,use,cid,pid,cell,prop],calculate)
    return result['queries'][0]


def enabled_effect(b,change,use,cid,cp,pid,path,cell,prop):
    """A privileged change newly permits a harmful *same* request.

    A value property must not require the unauthorized request to commit
    before its enabling change. All baseline source branches are considered;
    an unmodeled branch overapproximates possible baseline harm and therefore
    cannot certify that the capability is new. This is separate from the
    increased-loss comparison between two already committing requests.
    """
    def calculate():
        from .local_properties import safe_path
        from .behavior import ordered_clocks
        from .relations import beneficiary_condition
        f=b.f;lookup=f.lookup(use);e=MechanismEncoder(lookup);z=e.z
        cf=b.source_frame(change,cid,0);after=b.source_frame(use,pid,1,cf['writes'])
        controller=e.expr(cf['caller']);requester=e.expr(after['caller'])
        h,start,end,gross,_=flow(e,lookup,after,cell)
        roles,origins=fixed_role_terms(e,path_qualification(f,change,cp),0)
        cat=prop['category'];gaps=[];coverage=[]
        def harmful(p,fr):
            holder,old,new,_,_=flow(e,lookup,fr,cell);net=old-new
            permitted,resolved,basis=consent(b,e,use,p,fr,cell,holder,net,interpretation_for(prop,use,fr['path'],cell))
            if cat=='FCR-MINT':
                controlled,why=beneficiary_condition(e,fr,cell,holder,controller_frame=cf)
                no_debit=[flow(e,lookup,fr,c)[2]>=flow(e,lookup,fr,c)[1] for c in movements(b,use,p)['-']
                          if selector_relation(c,cell)=='same_shape']
                condition=z.And(new>old,controlled,*no_debit)
            else:
                credit=distributed_value(b,e,use,p,fr,cell,holder,all_transfers=cat=='FCR-TRANSFER')
                paid,_=native_settlement(b,e,use,fr,cell,holder)
                condition=z.And(net>0,holder!=controller,z.Not(permitted),
                    credit>0 if cat=='FCR-TRANSFER' else net>credit+paid)
            return z.And(holder==h,condition),resolved,basis
        after_harm,resolved,basis=harmful(path,after)
        baseline=[]
        for before_id,raw in f.operation_paths(use):
            if raw['flow']=='reverted':continue
            snapshot=e.checkpoint();mark=len(e.constraints)
            try:
                before_path=b.source_path(use,before_id,raw)
                if before_path['flow'] not in ('normal','returned') or not safe_path(b,use,before_id,before_path):
                    raise Unsupported('baseline_value_route_unresolved')
                fr=b.source_frame(use,before_id,1)
                commit=encode_frame(e,fr);bad,_,_=harmful(before_path,fr)
                checks=e.constraints[mark:];del e.constraints[mark:]
                baseline.append(z.And(commit,bad,*checks))
                coverage.append({'path':before_id,'state':'original_same_request_branch_encoded'})
            except Unsupported as error:
                e.rollback(snapshot);baseline.append(z.BoolVal(True))
                gaps.append({'path':before_id,'reason':str(error),'projection':'may already allow harm; never assumed harmless'})
        if not b.complete(use):
            baseline.append(z.BoolVal(True));gaps.append({'reason':'incomplete_baseline_source_routes'})
        base=z.And(encode_frame(e,cf),encode_frame(e,after),*roles,*ordered_clocks(e,1),
                   controller!=0,requester!=0,h!=0,after_harm,z.Not(z.Or(*baseline)))
        detail={'operation':change,'change':change,'observe':use,'target':prop['target'],
            'change_path':cid,'use_path':pid,'ledger':cell,'category_hypothesis':cat,
            'property_identity':prop['id'],'semantic_version':prop['semantic_version'],
            'property_validated':resolved or cat=='FCR-MINT','holder_consent':basis,'role_origins':origins,
            'causal_condition':'actual intervention enables harmful same request absent on every modeled baseline route',
            'beneficiary_rule':'controlled_or_self_only' if cat=='FCR-MINT' else None,'baseline_commit_not_assumed':True,'baseline_branch_coverage':coverage,'baseline_residuals':gaps,
            'same_request':'same caller, arguments, holder, asset and environment in both worlds',
            'conditional_call_summary':after.get('source_call_subcases',[])}
        label='financial_value' if resolved or cat=='FCR-MINT' else 'financial_consent_unresolved'
        q=b._query(e,base,label,detail)
        return {'queries':[q],'local_errors':gaps}
    return b.memo('value_enabled_effect',[change,use,cid,pid,cell,prop],calculate)


def compare_intermediate(b,change,use,prop):
    """Carry the same settled transition into both readings of the holder request.

    Only describes supported scoped differences. An incomplete intermediate
    search cannot exclude every effect of a setter.
    """
    from .local_properties import safe_path
    from .behavior import ordered_clocks
    from .relations import beneficiary_condition
    f=b.f; lookup=f.lookup(use); cat=prop['category']
    bridges=f.summaries.dependencies.quantity_bridges(change,use)
    queries=[];gaps=[]; examined=0
    def result(positive=False):
        return {'kind':'causal_compare','observed_measure':'financial_value','change':change,'observe':use,
                'property_identity':prop['id'],'queries':queries,'local_errors':gaps,'property_measurements':[],
                'property_excluded':False,'value_route_checked':bool(queries),'positive_route_sufficient':positive,
                'intermediate_source_checked':bool(queries),'normal_explanations':[]}
    for mid,mpid,cells in bridges:
        middle=f.paths[mpid]['raw']
        for cid,cp in b.paths(change):
            role=path_qualification(f,change,cp)
            if not role:continue
            for pid,p in b.paths(use):
                if b.remaining()<=0 or examined>=f.options.max_prefixes:
                    gaps.append({'reason':'bounded_value_transition_frontier'});return result()
                examined+=1
                if not all(safe_path(b,o,i,path) for o,i,path in [(change,cid,cp),(mid,mpid,middle),(use,pid,p)]):
                    gaps.append({'reason':'relevant_intermediate_semantics_missing'});continue
                try:
                    e=MechanismEncoder(lookup);z=e.z
                    cf=b.source_frame(change,cid,0)
                    before_mid=b.source_frame(mid,mpid,1);after_mid=b.source_frame(mid,mpid,1,cf['writes'])
                    base_writes=before_mid['writes']; post_writes=cf['writes']+after_mid['writes']
                    before=b.source_frame(use,pid,2,base_writes);after=b.source_frame(use,pid,2,post_writes)
                    roles,_=fixed_role_terms(e,role,0)
                    base=z.And(*(encode_frame(e,fr) for fr in (cf,before_mid,after_mid,before,after)),*roles,*ordered_clocks(e,2),
                               *(e.expr(fr['caller'])!=0 for fr in (cf,before_mid,before)))
                    positions=movements(b,use,p);all_cells=positions['+']+positions['-']
                    for cell in positions['+' if cat=='FCR-MINT' else '-']:
                        if not unit_origin(b,use,cell) or native_only_position(b,use,cell):continue
                        h0,start0,end0,_,_=flow(e,lookup,before,cell);h1,start1,end1,_,_=flow(e,lookup,after,cell)
                        controller=e.expr(cf['caller'])
                        matched=[other for other in all_cells if selector_relation(other,cell)=='same_shape']
                        if cat=='FCR-MINT':
                            beneficiary,_=beneficiary_condition(e,after,cell,h1,controller_frame=cf)
                            new=family_delta(e,lookup,after,matched,cell);old=family_delta(e,lookup,before,matched,cell)
                            condition=z.And(end1>start1,end1-start1>end0-start0,new>0,new>old,beneficiary)
                            resolved=True
                        else:
                            net1=start1-end1;net0=start0-end0
                            permitted,resolved,_=consent(b,e,use,p,after,cell,h1,net1,interpretation_for(prop,use,pid,cell))
                            c1=distributed_value(b,e,use,p,after,cell,h1,all_transfers=cat=='FCR-TRANSFER');c0=distributed_value(b,e,use,p,before,cell,h0,all_transfers=cat=='FCR-TRANSFER')
                            if cat=='FCR-TRANSFER':effect=z.And(c1>0,z.Or(net1>net0,c1>c0))
                            else:
                                paid1,_=native_settlement(b,e,use,after,cell,h1);paid0,_=native_settlement(b,e,use,before,cell,h0)
                                effect=z.And(net1-c1-paid1>0,net1-c1-paid1>net0-c0-paid0)
                            condition=z.And(net1>0,h1!=controller,z.Not(permitted),effect)
                        detail={'operation':change,'change':change,'observe':use,'use_path':pid,'property_identity':prop['id'],
                                'category_hypothesis':cat,'property_validated':True,'same_request':True,
                                'intermediate_value_carried':True,'ledger':cell}
                        b.check()
                        check=b._query(e,z.And(base,h1==h0,h1!=0,condition),'financial_value' if resolved else 'financial_consent_unresolved',detail)
                        queries.append(check)
                        if resolved and check['bounded_condition_confirmed']:return result(True)
                except Unsupported:
                    gaps.append({'reason':'intermediate_value_encoding_unsupported'})
    if not queries:gaps.append({'reason':'value_dependency_requires_intermediate_source_transition'})
    return result()


def compare(b,change,use,context):
    from .local_properties import safe_path
    from .behavior import ordered_clocks
    f=b.f;prop=context['compiled_property'];cat=prop['category'];lookup=f.lookup(use)
    if f.operations[change]['target']!=f.operations[use]['target']:
        raise Unsupported('value_intervention_target_mismatch')
    queries=[];rows=[];gaps=[];normal=[];checked=0;truncated=False
    b.active_property_objects={c['root'] for c in prop.get('objects',[])}
    b.active_property_roots=set(b.active_property_objects)
    controls={key(w['path']):w['path'] for _,p in b.paths(change) for w in p['writes']}
    read_cells={key(c):c for _,p in b.paths(use) for c in selectors([p['guards'],p['writes'],p.get('sensitive_effects',[])])}
    linked=[c for c in read_cells.values() if any(selector_relation(c,w)=='same_shape' for w in controls.values())]
    b.active_property_roots.update(c['root'] for c in linked)
    if not linked:
        return compare_intermediate(b,change,use,prop)
    use_paths=list(b.paths(use));change_paths=list(b.paths(change))
    from .summary import local_delta
    jobs=[]
    wanted='+' if cat=='FCR-MINT' else '-'
    # Enumerate only the bounded work actually admitted to this source route.
    # The full path Cartesian product is not materialized before budgeting.
    roles={cid:path_qualification(f,change,cp) for cid,cp in change_paths}
    positions={}
    for p1,after in use_paths:
        positions[p1]=[]
        for cell in movements(b,use,after)[wanted]:
            signs={local_delta(w)[0] for w in after['writes'] if key(w['path'])==key(cell)}
            if signs and None not in signs and wanted not in signs:continue
            unit=unit_origin(b,use,cell)
            if unit and not native_only_position(b,use,cell):positions[p1].append((cell,unit))
            elif not unit:
                semantic=b.semantics.lookup(use,cell) if getattr(b,'semantics',None) else None
                if not semantic or semantic.get('meaning')!='nonfinancial_counter':
                    gaps.append({'path':p1,'position':cell,'reason':'value_position_unit_not_source_bound'})
    total_jobs=sum(bool(r) for r in roles.values())*len(use_paths)*sum(map(len,positions.values()))
    # When semantic feedback rebinds an observed unknown, revisit its exact
    # after-path and ledger first. It is still solved under the new policy.
    from pr_next_joint.core import digest
    prior=getattr(b,'pending_amount_routes',{}).get((change,use,cat),set())
    matched={(pid,ledger) for pid,ledger in prior for cell,_ in positions.get(pid,())
             if digest(cell)==ledger and (interpretation_for(prop,use,pid,cell) or {}).get('meaning') in ('gross_debit_bound','net_request_with_fee')}
    def candidates():
        if matched:
            for cid,cp in sorted(change_paths):
                if not roles[cid]:continue
                for pid,path in sorted(use_paths):
                    for cell,unit in positions[pid]:
                        if (pid,digest(cell)) in matched:
                            yield cid,cp,pid,path,pid,path,cell,roles[cid],unit
        for equal in (True,False):
            for cid,cp in sorted(change_paths):
                if not roles[cid]:continue
                for p0,before in sorted(use_paths):
                    for p1,after in sorted(use_paths):
                        if (p0==p1)!=equal:continue
                        for cell,unit in positions[p1]:
                            if equal and (p1,digest(cell)) in matched:continue
                            yield cid,cp,p0,before,p1,after,cell,roles[cid],unit
    for job in candidates():
        jobs.append(job)
        if len(jobs)>f.options.max_prefixes:break
    cursor=context.get('_value_cursor',0)
    state_key=b.cache_key('financial_value_progress',[change,use,prop,context.get('bindings'),context.get('request_aliases')])
    progress=b.__dict__.setdefault('_financial_value_progress',{})
    if cursor:
        state=progress.get(state_key)
        if not state or state['cursor']!=cursor:raise Unsupported('financial_value_continuation_identity')
        queries,rows,gaps,normal=state['queries'],state['rows'],state['gaps'],state['normal']
    prior_ids={q['id'] for q in queries};prior_rows=len(rows);prior_normal=len(normal)
    def emit(result):
        # Prior slices are immutable evidence already attached to this issue.
        # Keep their identities, not repeated multi-megabyte query receipts.
        result['prior_probe_dependencies']=sorted(prior_ids)
        result['queries']=list({q['id']:q for q in result['queries'] if q['id'] not in prior_ids}.values())
        result['property_measurements']=result['property_measurements'][prior_rows:]
        result['normal_explanations']=result['normal_explanations'][prior_normal:]
        return result
    end=min(cursor+4,len(jobs),f.options.max_prefixes)
    for job_index in range(cursor,end):
            cid,cp,p0,before,p1,after,cell,role,unit=jobs[job_index]
            cells=movements(b,use,after)
            checked=job_index+1
            detail={'operation':change,'change':change,'observe':use,'target':prop['target'],
                'change_path':cid,'before_path':p0,'after_path':p1,'use_path':p1,'ledger':cell,'unit':unit,
                'category_hypothesis':cat,'property_identity':prop['id'],
                'semantic_version':prop['semantic_version'],'property_validated':True,
                'same_request':'same caller, inputs, environment, holder and source ledger in W0/W1',
                'scope':'actual privileged source intervention and committing dependent request',
                'no_universal_gross_allowance_policy':True}
            try:
                b.check()
                if not all(safe_path(b,o,pid,p) for o,pid,p in [(change,cid,cp),(use,p0,before),(use,p1,after)]):
                    raise Unsupported('relevant_value_route_dependency_unresolved')
                post=post_exclusion(b,change,use,cid,cp,p1,after,cell,prop)
                if not any(x['id']==post['id'] for x in queries):queries.append(post)
                if not proved_exclusion(post):
                    enabling=enabled_effect(b,change,use,cid,cp,p1,after,cell,prop)
                    for probe in enabling['queries']:
                        if not any(x['id']==probe['id'] for x in queries):queries.append(probe)
                        if probe['bounded_condition_confirmed']:
                            rows.append({'change_path':cid,'after_path':p1,'position':cell,'result_probe':probe['id'],
                                'state':probe['answer'],'scope':probe['details'],
                                'baseline':'all original branches checked; baseline commit not a premise'})
                            if probe['label']=='financial_value':
                                return emit(finish(b,prop,change,use,queries,rows,gaps,normal,checked,False,positive=True))
                            gaps.append({'path':p1,'position':cell,'reason':'holder_authorization_quantity_basis_unresolved',
                                'measured_probe':probe['id']})
                            result=finish(b,prop,change,use,queries,rows,gaps,normal,checked,True)
                            result['stopped_reason']='await_source_bound_consent_interpretation';return emit(result)
                if proved_exclusion(post) and any(r.get('normal_post_certificate')==post['id'] for r in rows):
                    rows.append({'change_path':cid,'before_path':p0,'after_path':p1,'position':cell,
                        'result_probe':post['id'],'state':'unsat','normal_post_certificate':post['id'],
                        'scope':detail,'reuse':'same post-effect excluded without requiring any baseline path'})
                    continue
                e=MechanismEncoder(lookup);z=e.z
                cf=b.source_frame(change,cid,0)
                w0=b.source_frame(use,p0,1)
                w1=b.source_frame(use,p1,1,cf['writes'])
                roles,origins=fixed_role_terms(e,role,0)
                h0,start0,end0,gross0,credit0=flow(e,lookup,w0,cell)
                h1,start1,end1,gross1,credit1=flow(e,lookup,w1,cell)
                controller=e.expr(cf['caller']);requester=e.expr(w1['caller'])
                base=z.And(encode_frame(e,cf),encode_frame(e,w0),encode_frame(e,w1),*roles,
                    *ordered_clocks(e,1),controller!=0,requester!=0,h0==h1,h1!=0,
                    z.Or(*[e.expr(read(qualify(c,1),[],lookup))!=e.expr(read(qualify(c,1),cf['writes'],lookup)) for c in linked]))
                for arg in context.get('bindings',[]):base=z.And(base,e.expr(qualify(arg['parameter'],1))==e.expr(arg['value']))
                for a,c,relation in context.get('request_aliases',[]):
                    aa,cc=e.expr(qualify(a,1)),e.expr(qualify(c,1));base=z.And(base,aa==cc if relation=='==' else aa!=cc)
                positions=list({key(c):c for c in cells['-']+cells['+']}.values())
                total1=family_delta(e,lookup,w1,positions,cell)
                total0=family_delta(e,lookup,w0,positions,cell)
                net0=start0-end0;net1=start1-end1
                permitted,basis_resolved,consent_basis=consent(b,e,use,after,w1,cell,h1,net1,
                    interpretation_for(prop,use,p1,cell))
                detail.update(role_provenance=role,encoded_role_origins=origins,
                    holder_consent=consent_basis,final_balance_aliases_merged=True,
                    actual_control_selectors=linked)
                values={'holder':h1,'controller':controller,'requester':requester,
                    'balance_before_request':start0,'balance_after_baseline':end0,'balance_after_intervention_request':end1,
                    'gross_debit_before':gross0,'gross_debit_after':gross1,'net_debit_before':net0,'net_debit_after':net1,
                    'family_net_before':total0,'family_net_after':total1,'holder_consent_sufficient':permitted}
                # A quantity observation is retained separately from a main
                # category decision, including fee/receipt-only changes.
                observed=z.And(base,z.Or(net1!=net0,total1!=total0))
                q=b._query(e,observed,'same_request_amount_change',dict(detail,measurement_only=True));queries.append(q)
                if cat=='FCR-MINT':
                    from .relations import beneficiary_condition
                    beneficiary,why=beneficiary_condition(e,w1,cell,h1,controller_frame=cf)
                    detail['beneficiary']=why
                    no_debit=[flow(e,lookup,w1,c)[2]>=flow(e,lookup,w1,c)[1] for c in cells['-']
                              if selector_relation(c,cell)=='same_shape']
                    violation=z.And(end1>start1,end1>end0,total1>0,total1>total0,beneficiary,*no_debit)
                else:
                    # Purely reduced receipt, with unchanged holder debit,
                    # remains an additional quantity fact under the contract.
                    violation=z.And(net1>0,h1!=controller,z.Not(permitted))
                    credited=distributed_value(b,e,use,after,w1,cell,h1,all_transfers=cat=='FCR-TRANSFER')
                    credited0=distributed_value(b,e,use,before,w0,cell,h0,all_transfers=cat=='FCR-TRANSFER')
                    if cat=='FCR-DESTROY':
                        paid1,settlement1=native_settlement(b,e,use,w1,cell,h1)
                        paid0,settlement0=native_settlement(b,e,use,w0,cell,h0)
                        loss1,loss0=net1-credited-paid1,net0-credited0-paid0
                        # Compare uncompensated loss, not just one gross
                        # balance write. Explicit fee consent still excludes
                        # the main category; an unknown norm stays open.
                        violation=z.And(violation,loss1>0,loss1>loss0)
                        detail['same_holder_settlement']={'baseline':settlement0,'intervention':settlement1}
                        values.update(uncompensated_loss_before=loss0,uncompensated_loss_after=loss1)
                    else:
                        violation=z.And(violation,credited>0,z.Or(net1>net0,credited>credited0))
                # An unresolved normative amount basis cannot license an
                # alarm. Test sufficient consent independently so a complete
                # normal source path still closes locally.
                positive_kind='financial_value' if basis_resolved or cat=='FCR-MINT' else 'financial_consent_unresolved'
                if proved_exclusion(post):tested=post
                else:
                    tested=b._query(e,z.And(base,violation),positive_kind,detail);queries.append(tested)
                row={'change_path':cid,'before_path':p0,'after_path':p1,'position':cell,
                     'result_probe':tested['id'],'state':tested['answer'],'scope':detail,
                     'quantity_probe':q['id']}
                if proved_exclusion(post):row['normal_post_certificate']=post['id']
                rows.append(row)
                if tested['answer']=='unsat':
                    normal.append({'probe':tested['id'],'reason':'same_request_no_unauthorized_additional_net_loss_or_issuance',
                                   'scope':detail,'certificate':tested.get('exclusion_certificate')})
                elif positive_kind=='financial_consent_unresolved':
                    gaps.append({'path':p1,'before_path':p0,'position':cell,
                        'reason':'holder_authorization_quantity_basis_unresolved','measured_probe':tested['id']})
                    # More arithmetic variants cannot answer this normative
                    # question. Preserve the measured route and leave time
                    # for the focused H answer and other independent roots.
                    result=finish(b,prop,change,use,queries,rows,gaps,normal,checked,True)
                    result['stopped_reason']='await_source_bound_consent_interpretation'
                    return emit(result)
                if tested['label']=='financial_value' and tested['bounded_condition_confirmed']:
                    return emit(finish(b,prop,change,use,queries,rows,gaps,normal,checked,False,positive=True))
            except Unsupported as error:
                gaps.append({'change_path':cid,'before_path':p0,'path':p1,'position':cell,'reason':str(error)})
            except TimeoutError as error:
                gaps.append({'change_path':cid,'before_path':p0,'path':p1,'reason':str(error)})
                result=finish(b,prop,change,use,queries,rows,gaps,normal,checked,True)
                result['stopped_reason']='shared_program_budget';return emit(result)
    more=end<total_jobs
    result=finish(b,prop,change,use,queries,rows,gaps,normal,end,more)
    result['route_enumeration']={'jobs':total_jobs,'covered':end,'limit':f.options.max_prefixes,
                                 'complete':not more,'source_only_order':True}
    if more and end<f.options.max_prefixes:
        progress[state_key]={'cursor':end,'queries':queries,'rows':rows,'gaps':gaps,'normal':normal}
        result['continuation']={'_value_cursor':end}
        result['stopped_reason']='branch_quantum_yield'
    else:progress.pop(state_key,None)
    return emit(result)


def finish(b,prop,change,use,queries,rows,gaps,normal,checked,truncated,positive=False):
    covered=bool(rows) and not gaps and not truncated and b.complete(change) and b.complete(use)
    post=[q for q in queries if q['label']=='financial_value_post_exclusion']
    excluded=covered and bool(post) and all(proved_exclusion(q) for q in post)
    return {'kind':'causal_compare','observed_measure':'financial_value','change':change,'observe':use,
        'property_identity':prop['id'],'queries':queries,'property_measurements':rows,'local_errors':gaps,
        'normal_explanations':normal,'property_excluded':excluded,'value_route_checked':True,
        'positive_route_sufficient':positive,'pair_budget':{'checked':checked,'truncated':truncated},
        'source_path_coverage':{'change_complete':b.complete(change),'use_complete':b.complete(use)},
        'evidence_scope':{'target':prop['target'],'request_context':'paired actual source frames',
                          'cross_asset_compensation_not_assumed':True}}

```

## source/src/pr_next_joint/investigation/goal_search.py

SHA-256 `95d5689142d7329752527800490337f844a15a9d691ba2d132b16432804e2ad7`

```python
"""Bounded backward prerequisites and forward checked symbolic target states.

Search results contain the actual ordered frames, not a list of writer names.
All addresses remain separate symbolic inputs unless the source/request binds
them. A finite queue ending never certifies universal unreachability.
"""
from collections import deque
import copy
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key
from pr_next_joint.frontend.storage import selectors, selector_relation
from pr_next_joint.verification.sequence import read
from .summary import unique


def prerequisites(b, operation, goal=None):
    needed = []
    for _, path in b.f.operation_paths(operation):
        needed.extend(selectors([path['guards'], path.get('evaluated_terms', []),
                                 [w['value'] for w in path['writes']]]))
    needed.extend((goal or {}).get('positions', []))
    return unique(needed)


class TargetSearch:
    def __init__(self, backend, operation, goal=None, plan=None):
        self.b, self.operation = backend, operation
        self.goal, self.plan = goal or {}, plan or {}
        self.record = {'kind': 'target_state_search', 'operation': operation,
                       'goal': self.goal, 'plan': self.plan, 'candidates_executed': [],
                       'pruned': [], 'states': [], 'frontier': [], 'exhausted_is_not_unreachable': True,
                       'depth_limit': backend.f.options.prefix_depth,
                       'candidate_limit': backend.f.options.max_prefixes}
        backend.__dict__.setdefault('target_search_records',[]).append(self.record)

    def __iter__(self):
        b, oid, f = self.b, self.operation, self.b.f
        queue, queued, states = deque([()]), {()}, set()
        target = f.operations[oid]['target']
        goal_cells = prerequisites(b, oid, self.goal)
        # The closure identifies writers of prerequisites of other writers.
        # Ordering is established only by the subsequent source frames.
        closure = list(goal_cells)
        for _ in range(f.options.prefix_depth):
            writers = b.graph.writers(target, closure, 'goal-state backwards prerequisite')
            closure = unique(closure + [c for w in writers for c in prerequisites(b, w)])
        while queue and len(self.record['candidates_executed']) < f.options.max_prefixes:
            b.check()
            sequence = queue.popleft()
            result = b.reach(oid, sequence, plan=self.plan, goal=self.goal)
            self.record['candidates_executed'].append(result)
            if result.get('stopped_reason')=='action_slice_exhausted':
                self.record['stopped_reason']='action_slice_exhausted'
                self.record['pending_prefixes']=[list(sequence)]+[list(s) for s in queue]
                self.record['frontier'].append({'prefix':list(sequence),'reason':'incomplete_source_frame_retained'})
                self.record['search_complete_within_enumerated_scope']=False
                return
            # Expand and record the queue before yielding a target state. The
            # consumer may stop after this state, and must still retain the
            # other untried preparations rather than lose the generator tail.
            if len(sequence) >= f.options.prefix_depth:
                self.record['frontier'].append({'prefix': list(sequence), 'reason': 'depth_bound'})
            else:
                head = prerequisites(b, sequence[0]) if sequence else goal_cells
                before = b.graph.writers(target, head, 'first-frame source prerequisites')
                after = b.graph.writers(target, goal_cells, 'target source prerequisites')
                extensions = [((w,) + sequence,w) for w in before] + [(sequence + (w,),w) for w in after]
                for candidate,added in extensions:
                    if candidate in queued:continue
                    queued.add(candidate)
                    changed = [w['raw']['path'] for w in f.writes.values() if w['operation'] == added]
                    if not any(selector_relation(a, c) == 'same_shape' for a in changed for c in closure):
                        self.record['pruned'].append({'prefix': list(candidate), 'reason': 'no_write_to_prerequisite_closure'})
                        continue
                    queue.append(candidate)
            self.record['pending_prefixes'] = [list(s) for s in queue]
            for world in result.get('worlds', []):
                if not world.get('committed'):
                    continue
                frames = world.get('prefix_frames', [])
                writes = [w for fr in frames for w in fr['writes']]
                # Preserve guards, frame identities and complete keyed values.
                # Only exact equivalent symbolic states are pruned, never a
                # function merely because it has occurred earlier.
                signature = digest([f.identity, self.goal, self.plan,
                    [(c, read(c, writes, f.lookup(oid))) for c in closure],
                    [fr['guards'] for fr in frames], [fr['caller'] for fr in frames]])
                if signature in states:
                    self.record['pruned'].append({'prefix': list(sequence), 'reason': 'identical_typed_state_and_conditions'})
                    continue
                states.add(signature)
                reached = {'id': 'state_' + signature[:20], 'prefix': list(sequence),
                           'frames': copy.deepcopy(frames), 'writes': copy.deepcopy(writes),
                           'target_frame': copy.deepcopy(world['target_frame']),
                           'baseline_probe': world['query'], 'goal': copy.deepcopy(self.goal),
                           'plan': copy.deepcopy(self.plan), 'source_identity': f.identity,
                           'initial_prefix_policy': 'constructor_only_for_explicit_prefix'}
                self.record['states'].append(reached)
                yield reached
        self.record['frontier'] += [{'prefix': list(s), 'reason': 'candidate_bound'} for s in queue]
        self.record['search_complete_within_enumerated_scope'] = not queue
        self.record['unfound_is_not_unreachable'] = True


def search(b, oid, goal=None, plan=None, stop_on_first=True):
    searcher = TargetSearch(b, oid, goal, plan)
    for _ in searcher:
        if stop_on_first:
            searcher.record['stopped_on_target'] = True
            break
    r = searcher.record
    return dict(r, kind='prefix_search', reached_with_nonempty_prefix=any(s['prefix'] for s in r['states']),
                target_property=goal or {}, state_kind='source_checked_ordered_symbolic_target_states',
                providers=sorted({o for x in r['candidates_executed'] for o in x['prefix']}),
                excluded_unrelated_providers=r['pruned'], search_complete=False)

```

## source/src/pr_next_joint/investigation/graph.py

SHA-256 `142170601f522170c8c5e9a2d26e15421d73a61e7a3dd076775d1441a12461c6`

```python
"""M1 neutral program graph, M2 hypotheses and M4 evidence in separate layers."""
import copy,collections,re,time
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import walk,key
from pr_next_joint.frontend.storage import selectors,selector_relation,keys
from .contracts import ident
from .request_scope import use_reads, unique_cells

class ProgramGraph:
    def __init__(self,facts):
        self.read_inputs={}
        self.facts=facts;self.nodes={};self.edges={};self.events=[];self.evidence_cache={};self.hypothesis_nodes={};self.ast_locators={}
        def ast_endpoint(target,ast_id,source=None):
            nid=ident('ast',[target,ast_id]);node=facts.lookups[target].nodes.get(ast_id)
            self.ast_locators[nid]={'target':target,'ast_id':ast_id,
                'source':facts.lookups[target].anchor(node) if node else source,
                'declaration_available':node is not None,'synthetic_or_external':node is None}
            return nid
        for target,lookup in facts.lookups.items():
            self.node(target,'contract',{'identity':target})
            for n in lookup.nodes.values():
                nid=ident('ast',[target,n.get('id')])
                if n.get('nodeType') in ('ContractDefinition','FunctionDefinition','ModifierDefinition','VariableDeclaration','EventDefinition','EmitStatement'):
                    self.node(nid,n['nodeType'],{'target':target,'ast_id':n['id'],'source':lookup.anchor(n)})
                if n.get('nodeType')=='ContractDefinition':
                    for base in n.get('linearizedBaseContracts',[])[1:]:self.edge(ast_endpoint(target,n['id']),ast_endpoint(target,base),'inherits')
        for oid,o in facts.operations.items():
            self.node(oid,'operation',o);self.edge(o['target'],oid,'entry')
            body=facts.lookup(oid).function(o['function'])
            if 'id' in body:self.edge(oid,ast_endpoint(o['target'],body['id'],o['source']),'entry_body')
            for n in walk(body):
                if n.get('nodeType')=='ModifierInvocation':self.edge(oid,ast_endpoint(o['target'],n.get('modifierName',{}).get('referencedDeclaration')),'modifier')
                if n.get('nodeType')=='FunctionCall':
                    decl=n.get('expression',{}).get('referencedDeclaration')
                    if type(decl)is int:self.edge(oid,ast_endpoint(o['target'],decl),'calls')
            for p in o['parameters']:
                nid=ident('parameter',[oid,p['ref']]);self.node(nid,'parameter',p);self.edge(oid,nid,'parameter');self.edge(nid,p['term'],'value_expression')
        for rid,r in facts.references.items():
            self.node(rid,'source_reference',r)
            self.edge(rid,ident('ast',[r['target'],r['ast_id']]),'binds_ast')
        for eid,e in facts.terms.items():self.node(eid,'expression',e)
        self.access=collections.defaultdict(lambda: {'writers':set(),'readers':set()})
        for pid,item in facts.paths.items():
            oid=item['operation'];raw=item['raw'];target=facts.operations[oid]['target']
            self.node(pid,'path',{'operation':oid,'flow':raw['flow'],'issues':raw.get('issues',[])})
            self.edge(oid,pid,'has_path')
            for g in raw['guards']:
                gid=ident('e',[target,g]);self.edge(gid,pid,'controls')
            for s in selectors(raw):
                sid=self.storage(target,s);self.edge(pid,sid,'reads');self.access[(target,s['root'])]['readers'].add(oid)
            for wid,w in facts.writes.items():
                if w['path']!=pid:continue
                self.node(wid,'state_effect',{'operation':oid,'path':pid,**w['raw']});self.edge(pid,wid,'commits')
                sid=self.storage(target,w['raw']['path']);self.edge(wid,sid,'writes')
                self.access[(target,w['raw']['path']['root'])]['writers'].add(oid)
                for s in selectors(w['raw']['value']):self.edge(self.storage(target,s),wid,'data_dependency')
            for eid,e in facts.effects.items():
                if e['path']==pid:self.node(eid,'external_effect',{'operation':oid,'path':pid,**e['raw']});self.edge(pid,eid,'external_effect')
            if raw.get('return_value') is not None:
                rid=ident('return',[pid,raw['return_value']]);self.node(rid,'return',{'expression':raw['return_value']});self.edge(pid,rid,'returns')
            for index,term in enumerate(raw.get('evaluated_terms',[])):
                tid=ident('eval',[pid,index]);self.node(tid,'evaluation',{'expression':term});self.edge(pid,tid,'evaluates')
        for (target,root),access in self.access.items():
            for a in access['writers']:
                for b in access['readers']:self.edge(a,b,'may_establish_use',{'target':target,'root':root,'may_alias_only':True})
        for i,g in enumerate(facts.gaps):
            nid=ident('gap',[i,g]);self.node(nid,'program_gap',g);self.edge(g['operation'],nid,'has_gap')
    def node(self,nid,kind,data,layer='program'):
        value={'id':nid,'kind':kind,'layer':layer,'data':copy.deepcopy(data)}
        if nid in self.nodes and self.nodes[nid]!=value:raise ValueError('graph_node_identity_conflict')
        self.nodes[nid]=value;return nid
    def edge(self,a,b,kind,data=None,layer='program'):
        row={'from':a,'to':b,'kind':kind,'layer':layer,'data':data or {}};eid=ident('edge',row);self.edges[eid]=row;return eid
    def storage(self,target,selector):
        nid=ident('object',[target,selector]);self.node(nid,'storage_object',{'target':target,'selector':selector})
        root=ident('ast',[target,selector['root']]);self.edge(nid,root,'storage_root')
        for i,s in enumerate(selector.get('segments',[])):
            kid=ident('selector',[target,selector,i]);self.node(kid,'storage_'+('key' if 'key' in s else 'length' if s.get('length') else 'field'),s);self.edge(nid,kid,'selector_position',{'position':i})
        return nid
    def writers(self,target,selectors_,reason):
        result=set()
        for s in selectors_:result.update(self.access.get((target,s['root']),{}).get('writers',set()))
        self.events.append({'action':'graph_writers','reason':reason,'roots':sorted({s['root'] for s in selectors_}),'operations':sorted(result),'binding_required':True})
        return sorted(result)
    def connected(self,oid,depth=2):
        seen={oid}
        for _ in range(depth):
            seen|={e['to'] for e in self.edges.values() if e['kind']=='may_establish_use' and e['from'] in seen}
            seen|={e['from'] for e in self.edges.values() if e['kind']=='may_establish_use' and e['to'] in seen}
        return sorted(seen)
    def neutral_frontier(self):
        """Index pre-answer source questions. A possible writer is not an authorized actor."""
        if hasattr(self, '_frontier'):
            return self._frontier
        f = self.facts
        writes = collections.defaultdict(list)
        for w in f.writes.values():
            path = w['raw']['path']
            writes[(f.operations[w['operation']]['target'], path['root'])].append(w)
        selected = []
        skipped = []
        # Spend a bounded number of candidate inspections per entry. Source access is independent.
        deadline=time.monotonic()+(self.remaining() if hasattr(self,'remaining') else f.options.seconds)
        for oid, operation in sorted(f.operations.items(), key=lambda x:(x[1]['target'],x[1]['source']['start'],x[0])):
            if time.monotonic()>=deadline:
                skipped.append({'entry':oid,'reason':'neutral_preselection_time_limit; source route open'})
                continue
            if operation['generated_getter']:
                continue
            target = operation['target']
            lookup = f.lookup(oid)
            best = None
            visits = 0
            for pid, path in f.operation_paths(oid, True):
                if not path['writes'] and not path.get('sensitive_effects'):
                    continue
                use = [('guard', s) for s in selectors(path['guards'])]
                use += [('effect_input', s) for s in selectors([w['value'] for w in path['writes']] + path.get('sensitive_effects', []))]
                seen = set()
                for kind, cell in use:
                    signature = kind, key(cell)
                    if signature in seen:
                        continue
                    seen.add(signature)
                    for row in writes.get((target, cell['root']), ()):
                        if visits >= f.options.max_actions:
                            break
                        visits += 1
                        writer = row['operation']
                        ws = row['raw']['path']
                        if writer == oid or selector_relation(ws, cell) != 'same_shape' or self._disjoint_keys(ws, cell):
                            continue
                        raw_writer = f.paths[row['path']]['raw']
                        if raw_writer['flow'] not in ('normal','returned') or raw_writer.get('issues') or raw_writer.get('evaluation_gaps'):
                            continue
                        actor = any(n.get('kind')=='actual_sender' for n in walk([path['guards'], cell, ws, raw_writer['guards']]))
                        rank = (not actor, kind!='guard', not bool(keys(cell)), f.operations[writer]['source']['start'], pid, writer)
                        if best is None or rank < best[0]:
                            best = rank, {'target':target,'writer':writer,'use':oid,'writer_path':row['path'],'use_path':pid,
                                'role_of_read':kind,'declaration':lookup.nodes[cell['root']].get('name'),
                                'ordered_write_key':ws,'ordered_read_key':cell,'write_source':row['raw']['source'],
                                'use_source':operation['source'],'sender_occurs':actor,'writer_guards':raw_writer['guards'],
                                'use_guards':path['guards'],'use_flow':path['flow'],
                                'effect_references':next(({'writes':c['writes'],'effects':c['effects']} for c in operation['paths'] if c['id']==pid),{}),
                                'stage':'possible earlier write then later use; no deployment reachability assertion',
                                'key_binding':'possible common storage position; caller and argument identities require investigation'}
                    if visits >= f.options.max_actions:
                        break
                if visits >= f.options.max_actions:
                    skipped.append({'entry':oid,'reason':'bounded_relation_enumeration'})
                    break
            if best:
                relation=best[1]
                cell=relation['ordered_read_key']
                related=[]
                for record in writes[(target,cell['root'])]:
                    s=record['raw']['path'];raw=f.paths[record['path']]['raw']
                    if raw['flow'] not in ('normal','returned') or raw.get('issues') or raw.get('evaluation_gaps'):
                        continue
                    if selector_relation(s,cell)=='same_shape' and not self._disjoint_keys(s,cell):
                        related.append({'operation':record['operation'],'path':record['path'],'ordered_key':s,
                                        'assigned':record['raw']['value'],'source':record['raw']['source']})
                    if len(related)>=f.options.max_actions:
                        skipped.append({'entry':oid,'reason':'related_write_index_bound'})
                        break
                relation['candidate_prior_writes']=related
                selected.append((best[0],relation))
            else:
                skipped.append({'entry':oid,'reason':'no_supported_cross_entry_meeting; source route open'})
        selected.sort(key=lambda x:(x[0],x[1]['target'],x[1]['use']))
        self._frontier = {'primary':selected[0][1] if selected else None,
                          'relations':[row for _,row in selected], 'limits':skipped,
                          'open_source_entries':sorted(f.operations), 'program_gaps':f.gaps,
                          'meaning':'neutral source relationships; no assertion of entitlement, policy or risk'}
        return self._frontier

    def closure_operations(self,oid,cells):
        """Include other original writers on the same possible key (grants, redemptions, alternative uses)."""
        target=self.facts.operations[oid]['target']
        by_operation={w for s in cells for w in self.access[(target,s['root'])]['writers']}
        return sorted({w['operation'] for w in self.facts.writes.values() if w['operation'] in by_operation
                       and any(selector_relation(s,w['raw']['path'])=='same_shape' and not self._disjoint_keys(s,w['raw']['path']) for s in cells)})

    def request_reads(self, oid):
        if oid not in self.read_inputs:
            self.read_inputs[oid] = unique_cells(cell for _, path in self.facts.operation_paths(oid, True)
                                                 for cell in use_reads(path))
        return self.read_inputs[oid]

    def investigation(self,oid,item,binding):
        """Compile one semantic uncertainty to a small source-grounded plan.

        Matching source names selects dependencies, never a business category.
        Omitted neighbors remain recorded possibilities, not refuted risks.
        """
        f=self.facts;o=f.operations[oid];lookup=f.lookup(oid);hint=item.get('next_check',{})
        hint=hint if isinstance(hint,dict) else {}
        question=item.get('distinguish',item.get('distinguishing_question',hint.get('question','')))
        if isinstance(question,dict):question=question.get('question','')
        text=' '.join(x for x in (item.get('claim'),item.get('alternative'),question) if isinstance(x,str))
        tokens=set(re.findall(r'[A-Za-z_$][\w$]*',text))
        guards=[s for _,p in f.operation_paths(oid) for s in selectors(p['guards'])]
        writes=[w['raw']['path'] for w in f.writes.values() if w['operation']==oid]
        named=[s for s in guards+writes if lookup.nodes.get(s['root'],{}).get('name') in tokens]
        focus=named or guards or writes
        focus=list({key(s):s for s in focus}.values())
        refs=set(binding.get('operations',[]));candidates=[]
        for other,op in f.operations.items():
            if other==oid or op['target']!=o['target']:continue
            ow=[w['raw']['path'] for w in f.writes.values() if w['operation']==other]
            og=self.request_reads(other)
            for change,observe,left,right in ((other,oid,ow,focus),(oid,other,writes,og)):
                shared=[s for s in left if any(selector_relation(s,t)=='same_shape' and not self._disjoint_keys(s,t) for t in right)]
                if not shared:continue
                # Explicit source names/anchors dominate possible root neighbors.
                explicit=other in refs or op['function'].split('(')[0] in tokens
                exact=any(key(s)==key(t) for s in shared for t in right)
                candidates.append({'change':change,'observe':observe,'controls':shared,
                  'rank':[0 if explicit else 1,0 if exact else 1,len(keys(shared[0])),
                          f.operations[change]['source']['start'],f.operations[observe]['source']['start']],
                  'source_reason':'explicit source relation' if explicit else 'matching ordered object in request guard, value, key or call'})
        candidates.sort(key=lambda x:x['rank']);unique={}
        for p in candidates:unique.setdefault((p['change'],p['observe']),p)
        candidates=list(unique.values());selected=candidates[:1]
        plan={'question':question or ('Which source-bound grant/control explains this effect, and does the related normal explanation apply?'),
          'risk_explanation':item['claim'],'normal_explanation':item.get('alternative'),
          'effect_root':oid,'focus_selectors':focus,'selected_pairs':selected,'deferred_pairs':candidates[1:],
          'selection_policy':'source relevance -> exact object shape -> cost; no confidence, Gold or expected score',
          'role_and_request_hints':{k:copy.deepcopy(hint[k]) for k in ('caller_mode','request_bindings') if k in hint}}
        self.events.append({'action':'question_guided_selection','operation':oid,'question':plan['question'],
            'selected':selected,'deferred_count':len(plan['deferred_pairs']),'focus':focus})
        return plan
    @staticmethod
    def _disjoint_keys(a,b):
        aa,bb=keys(a),keys(b)
        if len(aa)!=len(bb):return True
        return any(x.get('kind')==y.get('kind')=='literal' and x.get('value')!=y.get('value') for x,y in zip(aa,bb))
    def evidence(self,qid,record):
        # Store each immutable evidence entity once; graph edges carry its exact
        # scope. The separate evidence store owns formula/world payloads.
        identity=record.get('entity_sha256',digest(record));nid='evidence:'+identity
        card={k:copy.deepcopy(v) for k,v in record.items() if k not in ('worlds','queries','source_card','writer_cards','actual_guards','writes','effects')}
        card={k:v for k,v in card.items() if k not in ('id','question','semantic_version','action')}
        self.node(nid,'behavior_evidence',card,'evidence');self.edge(qid,nid,'supported_or_refuted_by',{'scope':record.get('evidence_scope',{})},layer='evidence')
        for field in ('operation','change','observe'):
            oid=record.get(field)
            if oid in self.facts.operations:self.edge(oid,nid,'evidence_source_operation',layer='evidence')
        def frames(value):
            if isinstance(value,dict):
                if 'operation' in value and 'slot' in value and ('committed_writes' in value or 'writes' in value):yield value
                for v in value.values():yield from frames(v)
            elif isinstance(value,list):
                for v in value:yield from frames(v)
        for fr in frames(record.get('worlds',{})):
            wid=ident('world',fr);self.node(wid,'execution_state_frame',{'sha256':digest(fr),'operation':fr['operation'],'path':fr['path'],'slot':fr['slot'],'full_frame_in':'evidence.json'},'evidence');self.edge(nid,wid,'uses_state_version',layer='evidence');self.edge(fr['operation'],wid,'source_operation_world',layer='evidence')
        return nid
    def record(self):return {'nodes':list(self.nodes.values()),'edges':list(self.edges.values()),'investigation_log':self.events,'semantics_are_not_program_facts':True}

```

## source/src/pr_next_joint/investigation/initial_state.py

SHA-256 `4a7fb9497b142a11b110ed190ecffc694ed4356990c35a00339d9c4e296318ac`

```python
"""Host-owned initial-state domains, constructor provenance and reachable writers.

This is a source transition summary, not a claim that an abstract state has been
deployed.  Every target freezes its numerical mapping candidates before M2.
"""
import copy
import re
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import key, lit, walk
from pr_next_joint.frontend.storage import keys, selectors, fields, value_type
from pr_next_joint.frontend.source_entry_identity import function_kind
from pr_next_joint.frontend.program_paths import MechanismPaths

CAPABILITY = 'fcr_conditional_capability_r1'
DEPLOYMENT = 'solidity_deployment_r1'
AC_DOMAIN = 'ac_checked_prestate_r1'


def domain(lookup):
    return getattr(lookup, 'state_domain_override', None) or (CAPABILITY if getattr(lookup, 'analysis_scope', None) == 'FCR' else AC_DOMAIN)


def family(cell):
    return key({'root': cell['root'], 'segments': [{'key': '*'} if 'key' in s else s for s in cell.get('segments', [])]})


def reachable_functions(facts, target):
    """Resolve runtime roots first. Uncalled private/internal bodies are not writers."""
    lookup = facts.lookups[target]
    roots = [lookup.function(o['function']) for o in facts.operations.values() if o['target'] == target and not o.get('generated_getter')]
    pending = [n for n in roots if n]; found = {}; unresolved = []
    while pending:
        fn = pending.pop()
        if fn.get('id') in found: continue
        found[fn['id']] = fn
        for n in walk(fn):
            expr = n.get('modifierName') if n.get('nodeType') == 'ModifierInvocation' else n.get('expression') if n.get('nodeType') == 'FunctionCall' else None
            if not expr: continue
            ref = expr.get('referencedDeclaration'); callee = lookup.nodes.get(ref, {})
            if callee.get('nodeType') in ('FunctionDefinition', 'ModifierDefinition'):
                # External typed calls do not execute in the caller's storage.
                if expr.get('nodeType') == 'MemberAccess' and expr.get('expression', {}).get('typeDescriptions', {}).get('typeString', '').startswith('contract '):
                    continue
                if callee.get('body'): pending.append(callee)
                else: unresolved.append({'source': lookup.anchor(n), 'reason': 'runtime_callee_body_missing'})
    return found, unresolved


def assigned_roots(node, lookup):
    if not isinstance(node, dict):
        return set()
    typ = node.get('nodeType')
    if typ == 'Identifier':
        rid = node.get('referencedDeclaration')
        return {rid} if lookup.nodes.get(rid, {}).get('stateVariable') else set()
    if typ in ('IndexAccess', 'IndexRangeAccess'):
        return assigned_roots(node.get('baseExpression'), lookup)
    if typ == 'MemberAccess':
        return assigned_roots(node.get('expression'), lookup)
    if typ == 'TupleExpression':
        return set().union(*(assigned_roots(x, lookup) for x in node.get('components', [])))
    return set()


def runtime_writers(facts, target):
    lookup = facts.lookups[target]
    functions, gaps = reachable_functions(facts, target)
    sites = {}; opaque = []
    for fn in functions.values():
        for n in walk(fn.get('body') or {}):
            lhs = n.get('leftHandSide') if n.get('nodeType') == 'Assignment' else n.get('subExpression') if n.get('nodeType') == 'UnaryOperation' and n.get('operator') in ('delete', '++', '--') else None
            if lhs:
                for rid in assigned_roots(lhs, lookup):
                    sites.setdefault(rid, set()).add(n['id'])
            if n.get('nodeType') == 'InlineAssembly' and any(w in str(n).lower() for w in ('sstore', 'delegatecall', 'callcode')) or n.get('memberName') in ('delegatecall', 'callcode'):
                opaque.append(lookup.anchor(n))
    paths = {}
    for oid, operation in facts.operations.items():
        if operation['target'] != target: continue
        for pid, p in facts.operation_paths(oid):
            for w in p['writes']:
                if w['path'].get('instance'): continue
                # Exact IR roots include supported local storage references.
                # Index expressions remain reads, never declaration writes.
                if w.get('source', {}).get('ast_id') is not None:
                    sites.setdefault(w['path']['root'], set()).add(w['source']['ast_id'])
                paths.setdefault(w['path']['root'], []).append({'operation': oid, 'path': pid,
                    'source': w['source'], 'flow': p['flow'], 'value': w['value'], 'cell': w['path'],
                    'complete': p['flow'] in ('normal', 'returned') and not p.get('issues') and not p.get('evaluation_gaps')})
    return {'functions': sorted(functions), 'sites': {r: sorted(v) for r, v in sites.items()},
            'paths': paths, 'opaque_storage_writes': opaque, 'unresolved_calls': gaps}


def amount_candidates(facts, target):
    """Structural eligibility only: no token names, model decisions or risk labels."""
    result = {}
    def add(cell, oid, pid, reason):
        typ = value_type(cell, facts.lookup(oid))
        if keys(cell) and re.fullmatch(r'u?int\d*', typ or ''):
            result.setdefault(family(cell), {'cell': cell, 'type': typ, 'basis': []})['basis'].append(
                {'operation': oid, 'path': pid, 'reason': reason})
    for oid, operation in facts.operations.items():
        if operation['target'] != target: continue
        for pid, p in facts.operation_paths(oid, True):
            moves = []
            for w in p['writes']:
                cell, value = w['path'], w['value']; args = value.get('args', [])
                if value.get('op') in ('+', '-') and len(args) == 2 and any(key(cell) == key(s) for s in selectors(args[0])):
                    moves.append((w, value['op'], args[1]))
            ledger = []
            for w, sign, amount in moves:
                cell = w['path']
                if len(keys(cell)) != 1: continue
                conserved = any(other['path']['root'] == cell['root'] and family(other['path']) == family(cell)
                    and other_sign != sign and key(other_amount) == key(amount) for other, other_sign, other_amount in moves)
                supply = any(not keys(other['path']) and other_sign == sign and key(other_amount) == key(amount)
                    for other, other_sign, other_amount in moves)
                asset = any(any(key(amount) == key(n) for n in walk(effect)) for effect in p.get('sensitive_effects', []))
                native = any(n.get('kind') == 'transaction_value' for n in walk(amount))
                if conserved or supply or asset or native:
                    add(cell, oid, pid, 'same_quantity_account_flow' if conserved else 'supply_or_asset_linked_account_flow')
                    ledger.append((cell, amount))
            # Holder->spender quantities checked/consumed with an actual account debit.
            # Eligibility is not proof that the holder consented.
            for w, sign, amount in moves:
                if ledger and len(keys(w['path'])) >= 2 and any(key(amount) == key(a) for _, a in ledger):
                    add(w['path'], oid, pid, 'account_flow_related_numeric_grant')
    return [result[k] for k in sorted(result)]


def _constructor_paths(facts, target):
    original = facts.lookups[target]
    lookup = MechanismPaths(facts.bundle, original.contract, facts.options.max_paths)
    lookup.analysis_scope = facts.options.scope
    order = list(reversed(lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']])))
    constructors = {cid: next((n for n in lookup.nodes[cid].get('nodes', []) if n.get('nodeType') == 'FunctionDefinition' and function_kind(n) == 'constructor'), None) for cid in order}
    states = [{'env': {}, 'guards': [], 'writes': [], 'issues': [], 'flow': 'normal', 'evaluated_terms': []}]
    params = {}; derived = constructors[order[-1]]
    if derived:
        params.update({p['id']: {'kind': 'parameter', 'id': p['id'], 'type': p.get('typeDescriptions', {}).get('typeString'), 'constructor_parameter': True}
                       for p in derived.get('parameters', {}).get('parameters', [])})
    errors = []
    # Base arguments are compiler-resolved expressions in the declaring constructor's parameters.
    for cid in reversed(order):
        node = lookup.nodes[cid]; ctor = constructors[cid]
        specs = [(b.get('baseName', {}).get('referencedDeclaration'), b.get('arguments')) for b in node.get('baseContracts', [])]
        if ctor: specs += [(m['modifierName'].get('referencedDeclaration'), m.get('arguments')) for m in ctor.get('modifiers', [])]
        for bid, expressions in specs:
            if bid not in constructors or expressions is None: continue
            base = constructors[bid]; expected = (base or {}).get('parameters', {}).get('parameters', [])
            state = {'env': copy.deepcopy(params), 'guards': [], 'writes': [], 'issues': [], 'flow': 'normal'}
            try:
                lookup.current = state; lookup.source_evaluation_steps = 0
                values = [lookup.expr(a, state) for a in expressions]
                if state['writes'] or state['issues'] or len(values) != len(expected): raise ValueError('base_constructor_argument_effect_or_binding')
                params.update({p['id']: v for p, v in zip(expected, values)})
            except (ValueError, KeyError, TypeError, NotImplementedError) as ex:
                errors.append({'contract': bid, 'reason': str(ex), 'scope': 'constructor_arguments'})
    for cid in order:
        ctor = constructors[cid]; node = lookup.nodes[cid]
        # Solidity initializes each base's declarations immediately before that base body.
        lookup.source_evaluation_steps = 0; lookup.read_calls.summaries = {}; lookup.unknown = []
        lookup.source_execution_context = {'kind': 'constructor', 'entry_ast_id': (ctor or {}).get('id'), 'basis': 'compiled_linearized_constructor_order'}
        for state in states:
            if state['flow'] not in ('normal', 'returned'): continue
            state['flow'] = 'normal'; state['env'] = copy.deepcopy(params)
            for var in node.get('nodes', []):
                if not var.get('stateVariable') or var.get('value') is None: continue
                try:
                    value = lookup.expr(var['value'], state)
                    state['writes'].append({'path': {'kind': 'storage', 'root': var['id'], 'segments': []},
                        'value': value, 'operator': '=', 'source': lookup.anchor(var)})
                except (ValueError, KeyError, TypeError, NotImplementedError) as ex:
                    state['issues'].append({'reason': str(ex), 'declaration': var['id'], 'source': lookup.anchor(var)})
        if not ctor: continue
        clone = copy.deepcopy(ctor)
        clone['modifiers'] = [m for m in clone.get('modifiers', []) if lookup.nodes.get(m['modifierName'].get('referencedDeclaration'), {}).get('nodeType') != 'ContractDefinition']
        expected = ctor.get('parameters', {}).get('parameters', [])
        if any(p['id'] not in params for p in expected):
            errors.append({'contract': cid, 'reason': 'base_constructor_parameter_not_bound', 'scope': 'constructor_arguments'})
            continue
        out = []
        for state in states:
            if state['flow'] not in ('normal', 'returned'): out.append(state); continue
            state['flow'] = 'normal'
            try:
                out.extend(lookup.invoke(clone, [copy.deepcopy(params[p['id']]) for p in expected], state))
            except (ValueError, KeyError, TypeError, NotImplementedError) as ex:
                state['issues'].append({'reason': str(ex), 'source': lookup.anchor(ctor)}); out.append(state)
        states = out[:facts.options.max_paths]
        if len(out) > len(states): errors.append({'reason': 'constructor_path_frontier_bound_exceeded'})
    for state in states:
        state.pop('env', None)
        state['issues'].extend(copy.deepcopy(errors))
    return states, params


def model(facts, target):
    cache = facts.__dict__.setdefault('_initial_states', {})
    if target in cache: return cache[target]
    lookup = facts.lookups[target]
    bases = lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']])
    declarations = {n['id']: n for c in bases for n in lookup.nodes[c].get('nodes', []) if n.get('stateVariable')}
    candidates = amount_candidates(facts, target)
    writers = runtime_writers(facts, target)
    try: paths, parameters = _constructor_paths(facts, target)
    except (ValueError, KeyError, TypeError, NotImplementedError) as ex:
        paths = [{'flow': 'unknown', 'guards': [], 'writes': [], 'issues': [{'reason': str(ex)}]}]; parameters = {}
    rows = {}
    for rid, var in declarations.items():
        typ = var.get('typeDescriptions', {}).get('typeString', '')
        assigned = [w for p in paths for w in p['writes'] if w['path']['root'] == rid]
        # Unknown explicit writes remain explicit: never introduce a replacement abstract role.
        explicit_ctor_sites = [n['id'] for cid in bases for fn in lookup.nodes[cid].get('nodes', []) if fn.get('nodeType') == 'FunctionDefinition' and function_kind(fn) == 'constructor'
            for n in walk(fn.get('body') or {}) if n.get('nodeType') == 'Assignment' and rid in assigned_roots(n.get('leftHandSide', {}), lookup)]
        rows[rid] = {'declaration': rid, 'name': var.get('name'), 'type': typ, 'source': lookup.anchor(var),
            'explicit_initializer': var.get('value') is not None, 'constructor_writes': assigned,
            'explicit_constructor_sites': explicit_ctor_sites, 'runtime_sites': writers['sites'].get(rid, []),
            'runtime_paths': writers['paths'].get(rid, []), 'constant': bool(var.get('constant')),
            'immutable': var.get('mutability') == 'immutable'}
    value = {'schema': 'source_initial_states_r1', 'target': target, 'declarations': rows,
        'candidate_amount_leaves': candidates, 'constructor_paths': paths, 'constructor_parameters': parameters,
        'runtime_writers': writers, 'source_default_rule': 'typed_default_except_explicit_FCR_symbolic_scalar_or_frozen_amount_leaf',
        'domains': [CAPABILITY, DEPLOYMENT], 'exact_author_runtime_state_verified': False}
    value['identity'] = digest(value); cache[target] = value
    return value


def initial_for_lookup(lookup):
    facts = getattr(lookup, '_investigation_facts', None)
    if facts is None: return None
    return model(facts, lookup.contract['file'] + ':' + lookup.contract['name'])


def receipt(lookup):
    value = initial_for_lookup(lookup)
    return {'analysis_domain': domain(lookup), 'initial_model_identity': value['identity'] if value else None,
        'candidate_amount_leaves': value['candidate_amount_leaves'] if value else [],
        'abstract_capability_is_not_deployment': domain(lookup) == CAPABILITY}

```

## source/src/pr_next_joint/investigation/key_roles.py

SHA-256 `6cfe4fdba590227f406dff418f8f4b0a01a9ed604a39528fc76f76d7fe102f7f`

```python
"""Finite key-role relations derived from source transfers and allowance uses.

Names and key order are not evidence. Ambiguous families retain their residual.
These records annotate positions; they do not change the state interpreter.
"""
import re
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, selector_relation, value_type
from .initial_state import family


def derive(f):
    proposals={}
    for oid,o in f.operations.items():
        lookup=f.lookup(oid)
        for pid,p in f.operation_paths(oid,True):
            if p.get('issues') or p.get('evaluation_gaps'):continue
            writes=p['writes'];debits=[];credits=[]
            for w in writes:
                v=w['value'];a=v.get('args',[]);cell=w['path']
                if not re.fullmatch(r'u?int\d*',value_type(cell,lookup) or ''):continue
                from .summary import local_delta
                sign,amount=local_delta(w)
                if sign in ('-','+'):(debits if sign=='-' else credits).append((cell,amount))
            for cell,amount in debits:
                idx=keys(cell)
                if len(idx)<2:continue
                token=(o['target'],family(cell))
                for dst,add in credits:
                    if selector_relation(cell,dst)!='same_shape' or key(amount)!=key(add):continue
                    ds=keys(dst);different=[i for i,(a,b) in enumerate(zip(idx,ds)) if key(a)!=key(b)]
                    if len(different)!=1:continue
                    h=different[0]
                    if idx[h].get('kind')=='actual_sender' and ds[h].get('type') in ('address','address payable'):
                        proposals.setdefault(token,[]).append({'holder_key':h,'kind':'asset_position',
                            'basis':'same_asset_self_debit_and_recipient_credit','operation':oid,'path':pid})
                for asset,spent in debits:
                    aks=keys(asset)
                    if len(aks)!=1 or len(idx)!=2 or not (amount and spent):continue
                    def parameters(term):
                        return {x['id'] for x in walk(term) if x.get('kind')=='parameter'}
                    same_amount=key(amount)==key(spent)
                    if not same_amount and not parameters(amount)&parameters(spent):continue
                    matches=[i for i,k in enumerate(idx) if key(k)==key(aks[0])]
                    if len(matches)!=1 or idx[1-matches[0]].get('kind')!='actual_sender':continue
                    if not any(key(c)==key(cell) for c in selectors(p['guards'])):continue
                    h=matches[0]
                    issuers=[w for w in f.writes.values() if f.operations[w['operation']]['target']==o['target'] and
                        selector_relation(w['raw']['path'],cell)=='same_shape' and len(keys(w['raw']['path']))==2 and
                        keys(w['raw']['path'])[h].get('kind')=='actual_sender' and w['raw']['value'].get('kind')=='parameter']
                    writers=[w for w in f.writes.values() if f.operations[w['operation']]['target']==o['target'] and
                        selector_relation(w['raw']['path'],cell)=='same_shape' and len(keys(w['raw']['path']))==2 and
                        w['raw']['value'].get('kind')=='parameter']
                    # Meaning and legitimate provenance are separate. A
                    # consumed allowance is still an authorization quantity
                    # when its only setter improperly writes another holder's
                    # key. Requiring a safe issuer here hid that very AC case.
                    if writers:
                        proposals.setdefault(token,[]).append({'holder_key':h,'kind':'authorization_quantity',
                            'basis':'holder_key_and_caller_index_linked_to_consumed_grant','asset':asset,
                            'debit_amount':spent,'consumed_amount':amount,'equal_expression':same_amount,
                            'operation':oid,'path':pid,'issuers':[w['operation'] for w in issuers],
                            'writers':[w['operation'] for w in writers],
                            'holder_provenance_proved_by_role_binding':False})
    records=[]
    for target,lookup in f.lookups.items():lookup.source_key_roles={}
    for (target,fam),rows in proposals.items():
        meanings={(r['holder_key'],r['kind']) for r in rows}
        if len(meanings)!=1:continue
        h,kind=next(iter(meanings));record={'holder_key':h,'kind':kind,'origins':rows,'family':fam,'target':target}
        f.lookups[target].source_key_roles[fam]=record;records.append(record)
    return records


def relation(cell,lookup):
    return getattr(lookup,'source_key_roles',{}).get(family(cell))

```
