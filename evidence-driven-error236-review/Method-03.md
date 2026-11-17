# 本批实际完整源码与运行器

源文件完整内容；Source ZIP保留原文件树和原字节。

## source/src/pr_next_joint/investigation/engine.py

原文件SHA256 `738706abb19ddf86223e196c5893e6d8b4e7bcc01b8b6afb9b387c67da0c92bf`

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

原文件SHA256 `9dad0e581d0e5b33d57475728d792d55f8373f050df56a0a6ea8df31fffef67d`

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
from .summary import local_delta


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


def direct_final_loss(inv,q,d,row):
    """One final account loss; an inconclusive probe is no normal contribution."""
    from .source_opinion import opinion,dependency_state,blocked_positive
    b=inv.backend;f=inv.f;oid=d['oid'];pid=row['path'];cell=d['cell'];lookup=f.lookup(oid)
    if dependency_state(inv,row,d)!='proved_irrelevant' or blocked_positive(inv,q,pid,'FCR-DESTROY'):
        return None
    prop=q.get('property') or {}
    same_family=[w for w in row['ordered_writes'] if selector_relation(w['path'],cell)=='same_shape']
    if len(same_family)!=1:return None
    def contribution(outcome,value=None,queries=(),stopped_reason=None):
        # Backend.memo expects a dictionary and uses queries/stopped_reason to
        # avoid retaining transient failures as completed computations.
        result={'outcome':outcome,'opinion':value,'queries':list(queries)}
        if stopped_reason:result['stopped_reason']=stopped_reason
        return result
    def calculate():
        try:
            b.check();e=MechanismEncoder(lookup);z=e.z;fr=b.source_frame(oid,pid,0)
            h,old,new,_,_=flow(e,lookup,fr,cell);actor=e.expr(fr['caller']);net=old-new
            qualification=path_qualification(f,oid,f.paths[pid]['raw'])
            if not qualification:return contribution('not_applicable')
            roles,origins=fixed_role_terms(e,qualification,0)
            permit,resolved,basis=consent(b,e,oid,f.paths[pid]['raw'],fr,cell,h,net,interpretation_for(prop,oid,pid,cell))
            if not resolved:
                ans=opinion('open','holder_consent_basis_unresolved',[d['where']]);ans['decisive_consent_gap']=True
                return contribution('open',ans)
            matching=distributed_value(b,e,oid,f.paths[pid]['raw'],fr,cell,h,all_transfers=False)
            paid,settlement=native_settlement(b,e,oid,fr,cell,h)
            commit=encode_frame(e,fr)
            terms=z.And(commit,*roles,actor!=0,h!=0,h!=actor,net>matching+paid,z.Not(permit))
            probe=b._query(e,terms,'scoped_final_holder_loss',{
                'operation':oid,'category':'FCR-DESTROY','target':f.operations[oid]['target'],
                'property_identity':prop.get('id'),'property_validated':True,
                'semantic_version':prop.get('semantic_version'),'use_path':pid,'effect_location':d['where'],
                'same_holder_final_net':True,'holder_consent':basis,'same_holder_settlement':settlement,
                'role_origins':origins,'not_a_global_absence_proof':True})
            if probe.get('bounded_condition_confirmed'):
                ans=opinion('risk','uncompensated_debit',[d['where']])
            elif proved_exclusion(probe):
                ans=opinion('normal','same_scope_loss_excluded',[d['where']])
            else:
                outcome='bounded_unsat' if probe.get('answer')=='unsat' else 'unconfirmed'
                return contribution(outcome,queries=[probe],stopped_reason='scoped_exclusion_or_positive_not_established')
            ans.update(effects=[d['id']] if d.get('id') else [],basis_probe=probe['id'],exact_write=True)
            ans['source_relation']={'family':'final_holder_debit','duty':'same_holder_unit_final_loss_and_applicable_consent',
                                    'support_location':d['where'],'committing_check':probe['id']}
            if ans['status']=='normal':ans['same_scope_authorized']=True
            return contribution(ans['status'],ans,[probe])
        except Unsupported:
            return contribution('unsupported',stopped_reason='source_encoding_unsupported')
        except TimeoutError:
            return contribution('timeout',stopped_reason='source_consumer_timeout')
    try:
        result=b.memo('scoped_final_holder_loss',[oid,pid,cell,prop,inv.semantics.dependency_identity([oid])],calculate)
    except TimeoutError:
        # A memo budget check may expire before its callback starts. The common
        # task clock retains the deadline; this route supplies no safe verdict.
        return None
    return result['opinion']



def purchase_for(b,use,pid,cell):
    """The very same use/position consumed by both financial query routes."""
    rules=getattr(getattr(b,'semantics',None),'rules',None)
    if rules is None:return None
    from .source_opinion import paid_credit
    row=next((r for r in b.f.summaries.rows(use) if r['path']==pid),None)
    if row is None:return None
    w=paid_credit(rules.inv,use,row,cell)
    if w is None:return None
    return {'use':use,'path':pid,'location':w['source'],'ledger_declaration':cell['root'],
            'buyer':'actual_requester','quantity':'same_source_payment_derived_amount',
            'scope':'this_credit_and_payment_branch_only'}


def paid_intervention(inv,q,rows):
    """A rate-only root is normal only for all its actual financial uses."""
    from .source_opinion import opinion,paid_credit,dependency_state
    from .summary import holder
    oid=inv.root(q);prop=q.get('property') or {};uses=prop.get('value_dependence',{}).get('value_uses',[])
    if not uses or any(holder(w['path'],inv.f.lookup(oid)) for r in rows for w in r['ordered_writes']):return None
    checked=[]
    for use in uses:
        for row in inv.f.summaries.rows(use):
            if not row['committing']:continue
            selected=[w for w in row['ordered_writes'] if holder(w['path'],inv.f.lookup(use)) and local_delta(w)[0]=='+']
            if not selected and not row['ordered_writes'] and not row['effects']:continue
            if not selected:return None
            for w in selected:
                if not paid_credit(inv,use,row,w['path']):return None
                checked.append(w['source'])
    if not checked:return None
    # A read dependency is not itself a certificate for a different issuing branch.
    if any(r['effects'] or r['residuals'] for r in rows):return None
    ans=opinion('normal','ordinary_paid_credit',[inv.f.operations[oid]['source']])
    ans['same_scope_authorized']=True
    ans['effects']=list(q['current'].get('_scope_effects',()))
    ans['source_relation']={'family':'payment_derived_credit','duty':'same_request_purchase_not_free_issuance',
                            'support_location':checked[0],'support_locations':checked,'uses':uses}
    return ans


def scoped_final_debit(inv,q,rows):
    """Compare the final same-account debit with the actual ordered, holder-issued cap."""
    from .source_opinion import opinion,role_ids,blocked_positive,feasible_source_guards
    from .summary import holder,local_delta
    from .policy_binding import conjuncts
    f=inv.f;oid=inv.root(q);rules=inv.semantics.rules;lookup=f.lookup(oid)
    reached=[]
    for r in rows:
        if not r['committing']:continue
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
            routes=list(rules.quantity_scopes(e))
            if not routes:
                found=direct_final_loss(inv,q,dict(d,id=e),r)
                if found:results.append(found)
                continue
            from .source_opinion import dependency_state
            if dependency_state(inv,r,d)!='proved_irrelevant':continue
            for route in routes:
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
                paid_scope=purchase_for(b,use,fr['path'],cell)
                condition=z.And(new>old,controlled,*no_debit,z.BoolVal(paid_scope is None))
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
            'ordinary_purchase_scope':purchase_for(b,use,pid,cell) if cat=='FCR-MINT' else None,
            'normal_explanation':'ordinary_paid_credit' if cat=='FCR-MINT' and purchase_for(b,use,pid,cell) else None,
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
                    purchase=purchase_for(b,use,p1,cell)
                    detail['ordinary_purchase_scope']=purchase
                    if purchase:detail['normal_explanation']='ordinary_paid_credit'
                    violation=z.And(end1>start1,end1>end0,total1>0,total1>total0,beneficiary,*no_debit,z.BoolVal(purchase is None))
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

原文件SHA256 `95d5689142d7329752527800490337f844a15a9d691ba2d132b16432804e2ad7`

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

原文件SHA256 `142170601f522170c8c5e9a2d26e15421d73a61e7a3dd076775d1441a12461c6`

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

原文件SHA256 `4a7fb9497b142a11b110ed190ecffc694ed4356990c35a00339d9c4e296318ac`

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

原文件SHA256 `6cfe4fdba590227f406dff418f8f4b0a01a9ed604a39528fc76f76d7fe102f7f`

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

## source/src/pr_next_joint/investigation/ledger.py

原文件SHA256 `4b4c9fe813c4624dc84713183354b40069daeaa73191c2256776c623bc94ef45`

```python
"""Bounded same-ledger measurements on committed original-source frames."""
from itertools import product
import re

from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, selector_relation, value_type
from pr_next_joint.verification.program_encoding import MechanismEncoder
from pr_next_joint.verification.sequence import qualify, read
from pr_next_joint.verification.source_worlds import frame, encode_frame
from pr_next_joint.verification.expressions import Unsupported

MEASURES = {
    'ledger_receipt': 'same_debit_recipient_receives_less',
    'ledger_debit': 'same_request_holder_debited_more',
    'ledger_grant': 'actual_debit_exceeds_effective_grant',
}


def unique(items):
    return list({key(x): x for x in items}.values())


def movements(backend, oid, path):
    from .summary import get_summaries
    return get_summaries(backend.f).movements(oid,path)


def legacy_movements(backend, oid, path):
    lookup = backend.f.lookup(oid)
    result = {'-': [], '+': []}
    for w in path['writes']:
        cell, expr = w['path'], w['value']
        args = expr.get('args', [])
        sign = expr.get('op')
        if sign not in result or len(args) != 2 or not value_type(cell, lookup).startswith('uint'):
            continue
        indices = keys(cell)
        if len(indices) != 1 or indices[0].get('kind') not in ('actual_sender', 'parameter'):
            continue
        account = indices[0]
        if account.get('kind') == 'parameter' and account.get('type') not in ('address', 'address payable'):
            continue
        candidates = args[:1] if sign == '-' else args
        if any(key(s) == key(cell) for a in candidates for s in selectors(a)):
            result[sign].append(cell)
    return {sign: unique(cells) for sign, cells in result.items()}


def same_increment(write,cell):
    v=write['value']; args=v.get('args',[])
    return selector_relation(write['path'],cell)=='same_shape' and v.get('op')=='+' and len(args)==2 and key(args[0])==key(write['path'])


def unit_origin(backend, oid, cell):
    from .initial_state import family
    from .key_roles import relation
    if (relation(cell,backend.f.lookup(oid)) or {}).get('kind')=='authorization_quantity':return None
    cache=backend.__dict__.setdefault('_unit_origin_cache',{})
    semantics=getattr(backend,'semantics',None)
    bound=semantics.lookup(oid,cell) if semantics else None
    if bound:
        if bound['meaning']=='financial_right':
            # A field participating in a source clock comparison is not an
            # asset quantity merely because the surrounding claim says token.
            # Independent source asset flow can establish a dual use; without
            # it the semantic/source type conflict stays an explicit obligation.
            temporal=[]
            target=backend.f.operations[oid]['target']
            clock_cache=backend.__dict__.setdefault('_clock_position_cache',{})
            ck=(target,family(cell))
            if ck not in clock_cache:
                for other,o in backend.f.operations.items():
                    if o['target']!=target:continue
                    for pid,p in backend.f.operation_paths(other):
                        for g in walk(p['guards']):
                            if g.get('op') not in ('<','<=','>','>=','==','!='):continue
                            if (any(selector_relation(s,cell)=='same_shape' for s in selectors(g)) and
                                any(n.get('kind') in ('block_timestamp','block_number') or
                                    n.get('kind')=='environment' and n.get('field') in ('timestamp','number') for n in walk(g))):
                                temporal.append({'operation':other,'path':pid,'comparison':g})
                clock_cache[ck]=temporal
            temporal=clock_cache[ck]
            physical_key=(target,family(cell))
            if temporal and physical_key not in cache:cache[physical_key]=_unit_origin(backend,oid,cell)
            if temporal and not cache[physical_key]:
                backend.__dict__.setdefault('unit_conflicts',{})[ck]={'cell':cell,'source_clock_comparisons':temporal,
                    'semantic_binding':bound['id'],'reason':'semantic amount not independently bound against source time dimension'}
                return None
            return {'kind':'source_bound_semantic_unit','binding':bound}
        original=_unit_origin(backend,oid,cell)
        return dict(original,semantic_conflict=bound) if original else None
    token=(backend.f.operations[oid]['target'],family(cell))
    if token not in cache:cache[token]=_unit_origin(backend,oid,cell)
    return cache[token]


def native_only_position(backend,oid,cell):
    if not backend._native_unit_source(oid,cell):return False
    semantics=getattr(backend,'semantics',None)
    binding=semantics.lookup(oid,cell) if semantics else None
    if binding and binding['meaning']=='financial_right' and (binding.get('semantic_assertion') or {}).get('unit_kind')=='token':return False
    cache=backend.__dict__.setdefault('_token_unit_source_cache',{})
    from .initial_state import family
    token=(backend.f.operations[oid]['target'],family(cell))
    if token not in cache:cache[token]=_unit_origin(backend,oid,cell,include_native=False)
    return cache[token] is None


def same_unit_transfers(facts,target,*,include_checked_arithmetic=False):
    """A conserved, spendable account quantity on an actual committing branch."""
    from .summary import holder,local_delta
    from .key_roles import relation
    from .initial_state import family
    from .policy_binding import conjuncts
    cache=facts.summaries.__dict__.setdefault('_transfer_unit_evidence',{})
    stamp=(target,include_checked_arithmetic)
    if stamp in cache:return cache[stamp]
    version=facts.bundle.get('compiler',{}).get('compiler_version','')
    major,minor,*_=version.split('.')+['0','0']
    checked=include_checked_arithmetic and major.isdigit() and minor.isdigit() and (int(major),int(minor))>=(0,8)
    unchecked=[facts.lookups[target].anchor(n) for n in facts.lookups[target].nodes.values()
               if checked and n.get('nodeType')=='UncheckedBlock']
    units={}
    for oid,operation in facts.operations.items():
        if operation['target']!=target:continue
        lookup=facts.lookup(oid)
        for row in facts.summaries.rows(oid):
            writes=row['ordered_writes']
            if len(writes)!=2 or row['residuals'] or row['effects']:continue
            moves={local_delta(w)[0]:w for w in writes}
            if not {'-','+'}<=moves.keys():continue
            debit,credit=(moves[s]['path'] for s in ('-','+'))
            if selector_relation(debit,credit)!='same_shape' or (relation(debit,lookup) or {}).get('kind')=='authorization_quantity':continue
            src,dst=holder(debit,lookup),holder(credit,lookup)
            if not src or not dst or key(src)==key(dst):continue
            if any(a.get('kind') not in ('actual_sender','parameter') for a in [src,dst]):continue
            qty=local_delta(moves['-'])[1]
            if not qty or qty.get('kind')!='parameter' or not qty.get('type','').startswith('uint'):continue
            if key(qty)!=key(local_delta(moves['+'])[1]):continue
            guards=[g for term in row['guards'] for g in conjuncts(term)]
            src_loc=moves['-']['source']
            checked_debit=checked and not any(u['file']==src_loc['file'] and u['start']<=src_loc['start']<u['start']+u['length'] for u in unchecked)
            if not checked_debit and not any((g.get('op') in ('>=','>') and list(map(key,g.get('args',())))==[key(debit),key(qty)])
                       or (g.get('op') in ('<=','<') and list(map(key,g.get('args',())))==[key(qty),key(debit)]) for g in guards):continue
            units.setdefault(family(debit),[]).append({'operation':oid,'path':row['path'],
                'source':moves['-']['source'],'credit_source':moves['+']['source']})
    cache[stamp]=units
    return units


def _unit_origin(backend, oid, cell,include_native=True):
    origins = backend._native_unit_source(oid, cell)
    if origins and include_native:
        return {'kind': 'same_ledger_with_native_deposit_origin', 'origins': origins,'native_redemption_value_proved':False}
    # Issuance-only contracts can identify the token unit via its supply view and
    # the same issuance quantity on the selected holder ledger; no transfer transaction needed.
    facts=backend.f
    target=facts.operations[oid]['target']
    supplies=[(other,pid,p['return_value']) for other,o in facts.operations.items() if o['target']==target
              for pid,p in backend.paths(other) if (p.get('return_value') or {}).get('kind')=='storage' and not keys(p['return_value'])]
    for other,o in facts.operations.items():
        if o['target']!=target:continue
        node=facts.lookup(other).nodes.get(o['source'].get('ast_id'),{})
        if node.get('nodeType')=='VariableDeclaration' and node.get('stateVariable') and node.get('visibility')=='public' and node.get('typeDescriptions',{}).get('typeString','').startswith('uint'):
            supplies.append((other,'public_getter_ast_'+str(node['id']),{'kind':'storage','root':node['id'],'segments':[]}))
    if keys(cell):
        # Financial unit belongs to the applied storage family, not the entry used to query it.
        # Confirm equal increment of a distinct scalar supply view on a real issuance branch.
        from .summary import local_delta
        for use,entry in facts.operations.items():
            if entry['target']!=target:continue
            for pid,p in backend.paths(use):
                moves=[(w,local_delta(w)) for w in p['writes']]
                for w,(sg,qty) in moves:
                    if sg!='+' or selector_relation(w['path'],cell)!='same_shape':continue
                    for sw,(other_sign,other_qty) in moves:
                        if other_sign!='+' or keys(sw['path']) or sw['path']['root']==cell['root'] or key(other_qty)!=key(qty):continue
                        if any(supply['root']==sw['path']['root'] for _,_,supply in supplies):
                            return {'kind':'source_supply_linked_token_unit','issuance_path':pid,'supply_declaration':sw['path']['root']}
    # A public holder-balance query and a holder-initiated transfer of
    # this exact storage family corroborate a token interpretation. A name alone cannot.
    facts = backend.f
    target = facts.operations[oid]['target']
    getter, transfer = [], []
    for other, entry in facts.operations.items():
        if entry['target'] != target:
            continue
        # Query source, independent of the public ABI spelling.
        node=facts.lookup(other).nodes.get(entry['source'].get('ast_id'),{})
        if node.get('nodeType')=='VariableDeclaration' and node.get('visibility')=='public' and cell['root']==node['id']:
            getter.append('public_getter_ast_'+str(node['id']))
        for pid, p in backend.paths(other):
            returned = p.get('return_value') or {}
            if returned.get('kind') == 'storage' and selector_relation(cell, returned) == 'same_shape' and len(keys(returned)) == 1 and keys(returned)[0].get('kind') == 'parameter':
                getter.append(pid)
        for pid, p in backend.paths(other):
            changed = movements(backend, other, p)
            debits = [s for s in changed['-'] if selector_relation(s, cell) == 'same_shape' and keys(s) and keys(s)[0]['kind'] == 'actual_sender']
            credits = [s for s in changed['+'] if selector_relation(s, cell) == 'same_shape' and keys(s)[0]['kind'] == 'parameter']
            if (entry['function']=='transfer(address,uint256)' and debits and credits) or any(key(dw['value']['args'][1])==key(cw['value']['args'][1]) for d in debits for c in credits for dw in p['writes'] for cw in p['writes'] if key(dw['path'])==key(d) and key(cw['path'])==key(c) and len(dw['value'].get('args',[]))==2 and len(cw['value'].get('args',[]))==2):
                transfer.append(pid)
    # A readable address account and an independently reduced aggregate can
    # identify this unit even when the aggregate has no public supply getter.
    # Match the final writes on one committing path, never the spelling of a field.
    if getter:
        from .summary import holder, local_delta
        for use, entry in facts.operations.items():
            if entry['target']!=target:continue
            for pid,p in backend.paths(use):
                if p.get('issues') or p.get('evaluation_gaps') or p.get('sensitive_effects'):continue
                changes=[(w,*local_delta(w)) for w in p['writes']]
                accounts=[(w,sg,q) for w,sg,q in changes if selector_relation(w['path'],cell)=='same_shape']
                if len(accounts)!=1:continue
                w,sg,q=accounts[0]
                if sg!='-' or holder(w['path'],facts.lookup(use)) is None:continue
                for scalar,other,amount in changes:
                    position=scalar['path']
                    if other!='-' or keys(position) or position['root']==cell['root'] or key(q)!=key(amount):continue
                    if value_type(position,facts.lookup(use))!=value_type(cell,facts.lookup(oid)):continue
                    if sum(v['path']['root']==position['root'] for v in p['writes'])!=1:continue
                    return {'kind':'source_synchronized_account_reduction','path':pid,
                            'account_declaration':cell['root'],'supply_declaration':position['root'],
                            'holder_read':getter[0], 'account_location':w['source'], 'supply_location':scalar['source']}
    if getter and transfer:
        return {'kind': 'source_token_ledger_unit', 'balance_query_paths': getter, 'holder_transfer_paths': transfer}
    # A native deposit account also supports redistribution. That fact alone does
    # not establish an additional token unit under E1.
    if keys(cell) and not origins:
        from .initial_state import family
        use=same_unit_transfers(facts,target).get(family(cell))
        if use:return {'kind':'source_disposable_account_shares','unit_source':'program','origins':use}
    return None


def grant_for(backend, oid, path, debit):
    """An on-path numeric allowance with its ordered, holder-issued source writer."""
    facts = backend.f
    from .summary import holder as bound_holder
    holder = bound_holder(debit,facts.lookup(oid))
    if holder is None:return None
    possible = []
    for guard in path['guards']:
        for node in walk(guard):
            args = node.get('args', [])
            if len(args) != 2:
                continue
            if node.get('op') in ('>=', '>'):
                cell = args[0]
            elif node.get('op') in ('<=', '<'):
                cell = args[1]
            else:
                continue
            idx = keys(cell) if cell.get('kind') == 'storage' else []
            holder_indices=[i for i,k in enumerate(idx) if key(k)==key(holder)]
            if len(idx) != 2 or len(holder_indices)!=1 or idx[1-holder_indices[0]].get('kind') != 'actual_sender':
                continue
            holder_index=holder_indices[0]
            for w in facts.writes.values():
                other = w['operation']
                if facts.operations[other]['target'] != facts.operations[oid]['target']:
                    continue
                dst, val = w['raw']['path'], w['raw']['value']
                writer = facts.paths[w['path']]['raw']
                if (selector_relation(dst, cell) == 'same_shape' and len(keys(dst)) == 2
                        and keys(dst)[holder_index].get('kind') == 'actual_sender' and keys(dst)[1-holder_index].get('kind') == 'parameter'
                        and val.get('kind') == 'parameter' and writer['flow'] in ('normal', 'returned')
                        and not writer.get('issues') and not writer.get('evaluation_gaps')):
                    possible.append(cell)
                    break
    cells = unique(possible)
    return cells[0] if len(cells) == 1 else None


def bind_positions(backend, oid, item):
    found = {}
    for pid, p in backend.paths(oid):
        moves = movements(backend, oid, p)
        for debit, credit in product(moves['-'], moves['+']):
            if selector_relation(debit, credit) != 'same_shape':
                continue
            hint = item.get('observation')
            hint = hint if isinstance(hint, dict) else {}
            if any(hint.get(field) and hint[field] != backend._storage_name(oid, cell)
                   for field, cell in [('payer_key', debit), ('recipient_key', credit)]):
                continue
            found[key([debit, credit])] = (debit, credit)
    # A separate recipient parameter remains a separate source position even when its
    # concrete address aliases the payer; a same-expression credit is also measured as a refund.
    if len(found)>1:
        distinct={k:v for k,v in found.items() if key(v[0])!=key(v[1])}
        if len(distinct)==1:found=distinct
    if len(found) != 1:
        return None, 'payer_and_recipient_not_unique_in_one_ledger'
    debit, credit = next(iter(found.values()))
    origin = unit_origin(backend, oid, debit)
    if not origin:
        return None, 'financial_unit_not_source_supported'
    return {'debit': debit, 'credit': credit, 'origin': origin}, None


def flow(encoder, lookup, fr, cell):
    """Translate each already composed write once, including runtime address aliases."""
    z = encoder.z
    history = list(fr['before'])
    probe = qualify(cell, fr['slot'])
    # A parameter/caller key is unchanged during this request.
    from .summary import holder
    account=holder(probe,lookup)
    if account is None:raise Unsupported('ledger_holder_address_not_bound')
    address = encoder.expr(read(account, history, lookup))
    start = encoder.expr(read(probe, history, lookup))
    debits, credits = [], []
    for w in fr['writes']:
        dest = w['path']
        if selector_relation(dest, probe) == 'same_shape' and len(keys(dest)) == len(keys(probe)):
            same = z.And(*[encoder.expr(a)==encoder.expr(read(b,fr['before'],lookup)) for a,b in zip(keys(dest),keys(probe))])
            prior = encoder.expr(read(dest, history, lookup))
            value = encoder.expr(w['value'])
            debits.append(z.If(z.And(same, value < prior), prior - value, 0))
            credits.append(z.If(z.And(same, value > prior), value - prior, 0))
        history.append(w)
    end = encoder.expr(read(probe, history, lookup))
    return address, start, end, z.Sum(debits) if debits else z.IntVal(0), z.Sum(credits) if credits else z.IntVal(0)


def equal_to(e, value, literal):
    if type(literal) is bool and not e.z.is_bool(value) or type(literal) is int and not e.z.is_int(value):
        raise Unsupported('named_assumption_sort_mismatch')
    return value == literal


def scenario_terms(e, lookup, case, before, after, slot):
    terms = []
    for condition in case:
        history = before if condition['frame'] == 'before' else after
        cell = qualify(condition['cell'], slot)
        term = e.expr(read(cell, history, lookup))
        terms.append(equal_to(e, term, condition['value']))
    return terms


def compare_ledger(backend, change, use, context):
    from .behavior import ordered_clocks
    f = backend.f
    spec = context['observable']
    measure, cells = spec['measure'], spec['ledger']
    lookup = f.lookup(use)
    queries, rows, errors = [], [], []
    cases = context.get('premise_cases') or [[]]
    checked = 0
    truncated = False
    baseline_paths=[(None,None)] if measure=='ledger_grant' else backend.paths(use)
    for (cid, cp), (p0, a), (p1, b), case in product(backend.paths(change), baseline_paths, backend.paths(use), cases):
        backend.check()
        if checked >= f.options.max_prefixes:
            truncated = True
            break
        if cid not in spec['change_paths']:continue
        checked += 1
        try:
            if any(backend.condition_dependencies(o, i, p)[k] for o,i,p in ((change,cid,cp),(use,p0,a),(use,p1,b)) if p is not None
                   for k in ('unknown_dependencies','credential_dependencies')):
                raise Unsupported('critical_external_or_credential_on_selected_path')
            e = MechanismEncoder(lookup)
            z = e.z
            cf = frame(f, change, cid, 0)
            w1=frame(f,use,p1,1,cf['writes'])
            w0=frame(f,use,p0,1) if p0 is not None else None
            from .roles import path_qualification, fixed_role_terms
            role_terms, role_origins=fixed_role_terms(e,path_qualification(f,change,cp),0)
            source_constraints = [encode_frame(e,cf), encode_frame(e,w1),*role_terms]
            if measure != 'ledger_grant':
                source_constraints.append(encode_frame(e,w0))
            source_constraints += ordered_clocks(e,1)
            source_constraints.extend(e.expr(fr['caller']) != 0 for fr in (cf,w1))
            for arg in context.get('bindings',[]):
                source_constraints.append(e.expr(qualify(arg['parameter'],1)) == e.expr(arg['value']))
            source_constraints += scenario_terms(e,lookup,case,[],cf['writes'],1)
            for left,right,relation in context.get('request_aliases',[]):
                x,y = (e.expr(qualify(t,1)) for t in (left,right))
                source_constraints.append(x == y if relation == '==' else x != y)
            changed = []
            for control in spec['control_selectors']:
                pos = qualify(control,1)
                changed.append(e.expr(read(pos,[],lookup)) != e.expr(read(pos,cf['writes'],lookup)))
            source_constraints.append(z.Or(*changed))
            h, h1, end1, dr1, _ = flow(e,lookup,w1,cells['debit'])
            r, r1, rend1, _, cr1 = flow(e,lookup,w1,cells['credit'])
            source_constraints.append(h!=0)  # The investigated holder can submit/authorize a request.
            if measure!='ledger_grant':source_constraints.append(r!=0)  # A usable receipt, not a burn sink.
            original_h = e.expr(read(qualify(cells['debit'],1),[],lookup))
            original_r = e.expr(read(qualify(cells['credit'],1),[],lookup))
            values = {'holder':h,'recipient':r,'controller':e.expr(cf['caller']),'requester':e.expr(w1['caller']),
                      'gross_debit_after':dr1,'gross_credit_after':cr1,'request_holder_delta_after':end1-h1,
                      'request_recipient_delta_after':rend1-r1, 'intervention_holder_delta':h1-original_h,
                      'intervention_recipient_delta':r1-original_r,'combined_holder_delta':end1-original_h,
                      'combined_recipient_delta':rend1-original_r}
            if measure == 'ledger_grant':
                grant = grant_for(backend,use,b,cells['debit'])
                if not grant:
                    raise Unsupported('ordered_holder_issued_grant_not_bound_on_commit_path')
                effective = e.expr(read(qualify(grant,1),cf['writes'],lookup))
                source_constraints.extend([e.expr(w1['caller']) != h, dr1 > 0])
                violation = dr1 > effective
                values['effective_grant'] = effective
            else:
                h0, pre0, end0, dr0, _ = flow(e,lookup,w0,cells['debit'])
                r0, rpre0, rend0, _, cr0 = flow(e,lookup,w0,cells['credit'])
                source_constraints += [h==h0, r==r0, dr0>0, dr1>0]
                values.update(gross_debit_before=dr0,gross_credit_before=cr0,request_holder_delta_before=end0-pre0,
                              request_recipient_delta_before=rend0-rpre0)
                if measure == 'ledger_receipt':
                    source_constraints.append(dr0 == dr1)
                    violation = rend1-r1 < rend0-rpre0
                else:
                    violation = dr1 > dr0
            details = {'target':f.operations[use]['target'],'change':change,'observe':use,'change_path':cid,
                       'before_path':p0 if measure!='ledger_grant' else None,'after_path':p1,'unit':cells['origin'],
                       'encoded_writer_role_origins':role_origins,'payer_key':cells['debit'],'recipient_key':cells['credit'],'holder':keys(cells['debit'])[0],
                       'principal_scope':{'holder':'nonzero_authorizing_account','recipient':'unrestricted' if measure=='ledger_grant' else 'nonzero_usable_receiving_account','addresses_may_alias':True},
                       'encoded_case':case,'encoded_request_bindings':context['bindings'],'request_aliases':context.get('request_aliases',[]),
                       'source_assumptions':context.get('declared_assumptions',[]),'unencoded_text_is_not_a_premise':True,
                       'initial_state':'shared symbolic state; no deployment prefix asserted',
                       'scope':'identified ledger and submitted original path(s), no market valuation or universal consent inference'}
            base = z.And(*source_constraints)
            feasible = backend._query(e,base,'ledger_request_feasible',details)
            queries.append(feasible)
            if not feasible['bounded_condition_confirmed']:
                rows.append({'feasible_probe':feasible['id'],'state':'premise_'+feasible['answer'],'scope':details})
                continue
            result = backend._query(e,z.And(base,violation),MEASURES[measure],details)
            queries.append(result)
            if measure=='ledger_grant' and result['bounded_condition_confirmed']:
                # Ask the actual extra predicate, not a test of one extracted
                # assignment. No address, amount or parameter is materialized.
                destination=backend._query(e,z.And(base,violation,h!=r,end1<h1,rend1-r1>effective),
                    'destination_credit_exceeds_grant',dict(details,measurement_only=True))
                queries.append(destination)
                result['predicate_checks']={'destination_credit_exceeds_grant':destination['bounded_condition_confirmed'],
                                            'check_id':destination['id']}
            rows.append({'feasible_probe':feasible['id'],'result_probe':result['id'],'state':result['answer'],
                         'scope':details})
        except Unsupported as error:
            errors.append({'path':p1,'before':p0,'change':cid,'reason':str(error)})
    return {'kind':'causal_compare','observed_measure':measure,'change':change,'observe':use,'queries':queries,
            'ledger_measurements':rows,'comparisons':[],'worlds':[],'alternative_uses':[],'holder_consent_counterexamples':[],
            'local_errors':errors,'net_measurements':[],'net_pair_budget':{'pairs':checked,'truncated':truncated},
            'evidence_scope':{'target':f.operations[use]['target'],'controls':spec['control_selectors'],
                              'request_context':context,'unit_origin':cells['origin']},
            'complete_for_modeled_observe_branches':backend.complete(use),'business_policy_proved':False,
            'no_program_mutation':True}


```

## source/src/pr_next_joint/investigation/local_properties.py

原文件SHA256 `9733c67e1b55723c1a24e3f860d0ea6e8eb2854ed84daa6f75cff1fe1aecc18a`

```python
"""Typed, source-effect queries for a compiled property."""
import copy
import hashlib
from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, selector_relation
from pr_next_joint.verification.sequence import qualify, read
from pr_next_joint.verification.source_worlds import frame, encode_frame
from pr_next_joint.verification.program_encoding import MechanismEncoder
from pr_next_joint.verification.expressions import Unsupported
from .ledger import movements, unit_origin, flow, grant_for
from .roles import path_qualification, fixed_role_terms
from .relations import beneficiary_condition


def audit_use_guards(b,policy):
    """Check each supplied use in its own frame, without synthesizing a grant sequence.

    This is a local well-formedness/consistency check. SAT here is never evidence
    of unauthorized acquisition. No input assignments are read from the solver.
    """
    from pr_next_joint.verification.solver import solve
    from pr_next_joint.core import digest
    results=[]
    for use in policy.get('acquisition_uses',[]):
        if b.remaining()<=0:
            results.append({'operation':use['operation'],'path':use['path'],'status':'not_executed','reason':'shared_budget'})
            continue
        oid,pid=use['operation'],use['path']
        record={'operation':oid,'path':pid,'target':b.f.operations[oid]['target'],
                'status':'open','scope':'individual_use_only','supports_takeover':False}
        results.append(record)
        try:
            p=b.f.paths[pid]['raw']
            if not safe_path(b,oid,pid,p):
                record['reason']='use_has_relevant_residual';continue
            e=MechanismEncoder(b.f.lookup(oid))
            fr=b.source_frame(oid,pid,0)
            term=encode_frame(e,fr)
            effect=_effect(e,fr,b.f.lookup(oid))
            solver=e.z.Solver()
            solver.add(term,effect,*e.constraints,*e.domain_constraints)
            text=solver.sexpr()
            formula_ref=hashlib.sha256(text.encode()).hexdigest()
            b.formulas.setdefault(formula_ref,{'sha256':formula_ref,'text':text,'scope_context':{
                'operation':oid,'path':pid,'scope':'individual use, no acquisition prefix or deployment reachability'}})
            b.check()
            answer=solve(solver,initial_ms=max(1,min(b.f.options.solver_timeout_ms,int(b.remaining()*1000))))
            record.update(status=str(answer),formula_ref=formula_ref,variable_domain='single isolated use frame',
                          source_guard_roots=sorted({s['root'] for s in selectors(p['guards'])}))
        except Unsupported as error:
            record.update(status='unsupported',reason=str(error))
        except TimeoutError:
            record.update(status='not_executed',reason='shared_budget')
        finally:
            evidence_key=digest([b.f.identity,oid,pid,record.get('formula_ref'),record['status']])
            b.__dict__.setdefault('use_guard_evidence',{})[evidence_key]=dict(record)
    return results


def safe_path(b, oid, pid, path):
    deps = b.condition_dependencies(oid, pid, path)
    if not path.get('source_call_subcases') and any(r['operation'] == oid and r['path'] == pid for r in b.f.call_summaries.rows.values()):
        roots = getattr(b,'active_property_roots',None) or {s['root'] for s in selectors([path['guards'],path['writes']])}
        # Demand-driven may analysis is shared between properties by its full
        # source/callpoint/root identity. It never turns an opaque return into
        # a successful call or a source-policy certificate.
        refinement = b.f.call_summaries.refine(b, oid, pid, roots)
        b.call_refinements = getattr(b,'call_refinements',{})
        b.call_refinements[refinement['id']] = refinement
        if any(c.get('same_storage_unresolved') or c.get('callback_projection') in
               ('may_influence','source_callpoint_not_precisely_lowered') for c in refinement['calls']):
            return False
    # Credential formulas are admitted to the backend, which checks exact
    # invalid-return domains and concretely verifies a candidate signature.
    # A symbolic recovered address alone never qualifies as a witness.
    return not deps['unknown_dependencies']


def _effect(e, fr, lookup):
    """Committed net effects, not merely returning from the entry."""
    z = e.z
    cells = {key(w['path']): w['path'] for w in fr['writes']}
    deltas = [e.expr(read(c, fr['before'] + fr['writes'], lookup)) !=
              e.expr(read(c, fr['before'], lookup)) for c in cells.values()]
    deltas += [e.expr(v['amount']) > 0 for v in fr['effects'] if v.get('amount') is not None]
    return z.Or(*deltas)


def necessary_effect_exclusion(b,oid,pid,context):
    """A pure necessary condition can refute a route with an unknown read.

    Unknown STATICCALL results are omitted, never assumed successful/false.
    An unresolved state-changing call cannot use this projection.
    """
    f=b.f;p=f.paths[pid]['raw'];req=context['observable']
    if req.get('measure')!='direct_effect' or p['flow'] not in ('normal','returned'):return None
    calls=[c for c in f.call_summaries.rows.values()if c['operation']==oid and c['path']==pid]
    if not calls or any(c['mode']!='STATICCALL' and c['unresolved_implementation']for c in calls):return None
    role=path_qualification(f,oid,p)
    if not role:return None
    try:
        e=MechanismEncoder(f.lookup(oid));z=e.z
        opaque={'unknown','external_return','read_call','call_unresolved','credential_recovery'}
        projection=dict(p,issues=[],evaluation_gaps=[],evaluated_terms=[],
            guards=[g for g in p['guards']if not any(n.get('kind')in opaque for n in walk(g))])
        fr=frame(f,oid,pid,0,path_override=projection)
        fr['evidence_world']='necessary_condition_projection_not_execution'
        guards=fr['guards']
        terms=[]
        for g in guards:
            mc,md=len(e.constraints),len(e.domain_constraints)
            try:terms.append(e.expr(g))
            except Unsupported:del e.constraints[mc:];del e.domain_constraints[md:]
        effects=[]
        for cell in (context.get('compiled_property')or{}).get('objects',[]):
            holder,start,end,_,_=flow(e,f.lookup(oid),fr,cell)
            effects.append(end>start if req['category']=='FCR-MINT' else end<start)
        if not effects:return None
        roles,origins=fixed_role_terms(e,role,0)
        detail={'operation':oid,'target':f.operations[oid]['target'],'use_path':pid,
            'property_identity':context.get('property_identity'),'semantic_version':context.get('semantic_version'),
            'category':req['category'],'property_validated':True,'necessary_condition_only':True,
            'omitted_read_results_are_unconstrained_not_assumed':True,'retained_guards':guards,
            'role_origins':origins,'unknown_read_cannot_modify_local_storage':True}
        q=b._query(e,z.And(*terms,*roles,e.expr(fr['caller'])!=0,z.Or(*effects)),
                   'source_necessary_condition',detail)
        if q['answer']=='unsat' and (q.get('exclusion_certificate',{}).get('excludes_only_this_formula') or
                q.get('details',{}).get('prestate',{}).get('global_reachability_exhausted')):
            return q
    except Unsupported:pass
    return None


def check_local(b, oid, primary_use, context):
    f = b.f
    lookup = f.lookup(oid)
    req = context['observable']
    kind = req['measure']
    queries, rows, gaps = [], [], []
    prop = context.get('compiled_property') or {}
    if kind in ('authorization_violation','denied_qualified'):
        from .policy_binding import audit_authorization
        audit=audit_authorization(f,oid,req.get('authorization'))
        if any(not r['matches'] for r in audit):
            return {'kind':'causal_compare','change':oid,'observe':primary_use,'queries':[],'property_excluded':False,
                    'local_errors':[{'reason':'source_ir_disagreement','checks':audit}],
                    'worlds':[],'comparisons':[],'property_identity':prop.get('id')}
    b.active_property_roots = {s['root'] for s in selectors([
        prop.get('objects',[]), (req.get('authorization') or {}).get('predicate',{})])}
    if kind in ('authorization_violation','denied_qualified'):
        # AC's effect predicate observes committed writes, including grant and
        # stage cells that are not financial asset objects. Their callbacks
        # must not be declared disjoint merely because objects is empty.
        uses=(req.get('authorization') or {}).get('acquisition_uses',[])
        related=[p for _,p in f.operation_paths(oid)]+[f.paths[u['path']]['raw'] for u in uses]
        b.active_property_roots.update(s['root'] for p in related for s in selectors([p['guards'],p['writes']]))
    b.active_property_objects = {s['root'] for s in selectors(prop.get('objects',[]))}
    necessary_closed={}
    for source_pid,source_path in f.operation_paths(oid):
        if not source_path.get('issues') and not source_path.get('evaluation_gaps'):continue
        exclusion=necessary_effect_exclusion(b,oid,source_pid,context)
        if exclusion:
            necessary_closed[source_pid]=exclusion['id'];queries.append(exclusion)
            rows.append({'state':'necessary_condition_unsat','scope':exclusion['details'],'result_probe':exclusion['id']})
    if any(e['operation']==oid and e['raw'].get('kind') in ('native_transfer','native_selfdestruct')
           for e in f.effects.values()):
        b.active_property_roots.add(-1)
    for source_pid, source_path in f.operation_paths(oid):
        if source_pid in necessary_closed:continue
        if any(c['operation']==oid and c['path']==source_pid for c in f.call_summaries.rows.values()):
            # Unresolved call paths cannot be upgraded to witness paths, but
            # their actual callpoint/guard projections still enter the shared
            # obligation and feedback records rather than vanishing at paths().
            if not b.source_path(oid,source_pid,source_path).get('source_call_subcases'):
                f.call_summaries.refine(b,oid,source_pid,b.active_property_roots)

    def pair(e, base, extra, details, values):
        details = dict(details, property_identity=context.get('property_identity'),
                       semantic_version=context.get('semantic_version'),
                       prefix_state_handoff=reached, prefix=reached.get('prefix',[]),
                       **({'initial_prefix_policy':'constructor_only_for_explicit_prefix'} if reached else {}),
                       property_validated=details.get('property_validated',True), validation='typed source entities and actual committed effect')
        feasible = b._query(e, base, 'local_premises_feasible', details)
        queries.append(feasible)
        if not feasible['bounded_condition_confirmed']:
            rows.append({'feasible_probe': feasible['id'], 'state': 'premise_' + feasible['answer'], 'scope': details})
            return
        tested = b._query(e, e.z.And(base, extra), kind, details)
        queries.append(tested)
        rows.append({'feasible_probe': feasible['id'], 'result_probe': tested['id'],
                     'state': tested['answer'], 'scope': details})

    reached=context.get('reached_state') or {}
    prefix_frames=reached.get('frames',[])
    prefix_writes=reached.get('writes',[])
    slot=len(prefix_frames)
    def current_frame(pid):
        return b.source_frame(oid,pid,slot,prefix_writes)
    def prefix_conditions(e):
        from .behavior import ordered_clocks
        return [encode_frame(e,pf) for pf in prefix_frames]+[e.expr(pf['caller'])!=0 for pf in prefix_frames]+ordered_clocks(e,slot)

    separate_uses=[]
    if kind == 'authorization_violation':
        policy = req.get('authorization')
        if not policy:
            gaps.append({'reason': 'authorization_relationship_not_bound'})
        else:
            acquiring = policy.get('property_family') == 'acquire'
            uses = policy.get('acquisition_uses', []) if acquiring else [None]
            if acquiring and not uses:
                gaps.append({'reason':'acquired_authority_has_no_bound_actual_use'})
            for pid, p in b.paths(oid):
                b.check()
                scoped_write=policy.get('effect_write')
                if scoped_write and scoped_write['path']!=pid:continue
                if not safe_path(b, oid, pid, p):
                    gaps.append({'path': pid, 'reason': 'authorization_path_dependency_unresolved'})
                    continue
                # A joint grant/use query owns its entire encoder. In particular
                # an unsupported sibling cannot leave domains, constraints,
                # credential/hash terms or symbols in a supported sibling.
                for row in uses:
                    b.check()
                    check = {'grant_path':pid,'operation':row['operation'] if row else oid,
                             'path':row['path'] if row else pid,'scope':'joint_grant_then_use',
                             'supports_takeover':False,'status':'open'}
                    if row: separate_uses.append(check)
                    try:
                        e = MechanismEncoder(lookup)
                        z = e.z
                        fr = current_frame(pid)
                        actor = e.expr(fr['caller'])
                        expected = e.expr(read(qualify(policy['predicate'],slot),prefix_writes,lookup))
                        if scoped_write:
                            cell=fr['writes'][scoped_write['version']]['path']
                            before=e.expr(read(cell,fr['before'],lookup))
                            after=e.expr(read(cell,fr['before']+fr['writes'],lookup))
                            effect=before!=after
                            if len(fr['writes'])>1:
                                version=scoped_write['version']
                                earlier=fr['before']+fr['writes'][:version]
                                at_write=e.expr(read(cell,earlier+[fr['writes'][version]],lookup))
                                effect=z.And(effect,at_write!=e.expr(read(cell,earlier,lookup)),at_write==after)
                        else:
                            effect=_effect(e,fr,lookup)
                        detail = {'operation':oid,'target':f.operations[oid]['target'],'use_path':pid,
                            'expected_authorization':policy,'actual_guards':fr['guards'],
                            'argument_domain':'all_source_inputs_on_this_committing_path',
                            'effect_required':True,'acquisition_use_required':acquiring}
                        values = {'caller':actor,'authorization_holds':expected}
                        clocks = []
                        if row:
                            up = f.paths[row['path']]['raw']
                            if not safe_path(b,row['operation'],row['path'],up):
                                raise Unsupported('acquired_authority_use_unresolved')
                            authority = row.get('authority') or policy.get('subject')
                            roots = {s['root'] for s in selectors(authority)}
                            if isinstance(authority,dict) and 'root' in authority: roots.add(authority['root'])
                            def conjuncts(term):
                                return [g for a in term['args'] for g in conjuncts(a)] if term.get('op') in ('and','&&') else [term]
                            gates = [g for guard in up['guards'] for g in conjuncts(guard)
                                     if roots & {s['root'] for s in selectors(g)}]
                            if not gates: raise Unsupported('acquired_authority_not_used_by_downstream_guard')
                            after = b.source_frame(row['operation'],row['path'],slot+1,prefix_writes+fr['writes'])
                            # The same request did not possess this qualification
                            # before the grant. A preexisting successful use is
                            # not evidence of newly acquired authority.
                            mark = len(e.constraints)
                            before_permission = z.And(*[e.expr(read(qualify(g,slot+1),prefix_writes,lookup)) for g in gates])
                            pre_checks = e.constraints[mark:];del e.constraints[mark:]
                            after_permission = z.And(*[e.expr(read(qualify(g,slot+1),prefix_writes+fr['writes'],lookup)) for g in gates])
                            productive = _effect(e,after,lookup)
                            use_caller=e.expr(after['caller'])
                            actor_links=[use_caller==actor];nominees=[]
                            # A requester can explicitly select a fresh
                            # controlled address in an unrestricted address
                            # grant. This is a conditional source subcase,
                            # not control of an arbitrary observed recipient.
                            for w in p['writes']:
                                value=w['value']
                                if w['path']['root'] not in roots or value.get('kind')!='parameter' or value.get('type') not in ('address','address payable'):continue
                                fixed=[g for guard in p['guards'] for g in conjuncts(guard)
                                       if g.get('op')=='==' and any(key(x)==key(value) for x in g.get('args',[])) and
                                       any(x.get('kind') in ('storage','literal','contract_address') for x in g.get('args',[]))]
                                if fixed:continue
                                selected=e.expr(qualify(value,slot))
                                actor_links.append(z.And(use_caller==selected,selected!=0))
                                nominees.append({'argument':value,'kind':'selectable_self_controlled_address',
                                    'conditional':True,'all_actual_source_restrictions_retained':True,
                                    'arbitrary_observed_recipient_control_not_assumed':True})
                            effect = z.And(effect,encode_frame(e,after),productive,
                                *pre_checks,z.Not(before_permission),after_permission,
                                z.Or(*actor_links))
                            from .behavior import ordered_clocks
                            clocks = ordered_clocks(e,slot+1)
                            detail.update(acquired_use=row,authority_gates=gates,
                                acquisition_precondition='same request lacks this authority before the actual grant',
                                actor_scope='same requester or a source-selectable controlled nominee; not a universal identity assumption',
                                nominee_control_subcases=nominees,
                                before_writes=prefix_writes,after_writes=prefix_writes+fr['writes'],
                                new_authority_required=True,downstream_effect_required=True)
                            values.update(use_caller=use_caller,
                                authority_before=before_permission,authority_after=after_permission,
                                downstream_effect=productive)
                        values['sensitive_effect']=effect
                        first=len(queries)
                        pair(e,z.And(encode_frame(e,fr),actor!=0,*prefix_conditions(e),*clocks),
                             z.And(effect,z.Not(expected)),detail,values)
                        checked=queries[first:]
                        check.update(status=checked[-1]['answer'] if checked else 'open',
                            probes=[x['id'] for x in checked],
                            supports_takeover=any(x['label']==kind and x['bounded_condition_confirmed'] for x in checked))
                    except Unsupported as error:
                        check.update(status='unsupported',reason=str(error))
                        gaps.append({'path':pid,'use':row,'reason':str(error)})
    elif kind == 'denied_qualified':
        policy = req.get('authorization')
        if not policy:
            gaps.append({'reason': 'qualified_denial_policy_not_bound'})
        else:
            subject = policy.get('subject')
            denial_roots={s['root'] for s in selectors(policy.get('predicate',{}))}
            if isinstance(subject,dict) and 'root' in subject:denial_roots.add(subject['root'])
            rejecting = [(pid, p) for pid, p in f.operation_paths(oid) if p['flow'] == 'reverted']
            for pid, p in rejecting:
                b.check()
                if not p['guards'] or not safe_path(b, oid, pid, p):
                    continue
                for spid, sp in b.paths(oid):
                  try:
                    if not safe_path(b,oid,spid,sp):
                        raise Unsupported('qualified_denial_productive_path_unresolved')
                    e = MechanismEncoder(lookup)
                    z = e.z
                    actor = e.expr(qualify({'kind': 'actual_sender'}, slot))
                    allowed = e.expr(read(qualify(policy['predicate'], slot),prefix_writes,lookup))
                    controls = {s['root'] for s in selectors(p['guards'][-1])}
                    if not (controls & denial_roots):
                        continue
                    sf = current_frame(spid)
                    def conjuncts(g):
                        return [v for a in g['args'] for v in conjuncts(a)] if g.get('op') in ('and','&&') else [g]
                    def only_authorization(g):
                        roots={s['root'] for s in selectors(g)}
                        return bool(roots & denial_roots) and roots<=denial_roots and any(
                            v.get('sequence_role')=='caller' for v in walk(g))
                    guards=[g for term in sf['guards'] for g in conjuncts(term)]
                    removed=[g for g in guards if only_authorization(g)]
                    if not removed:continue
                    conditioned=dict(sf,guards=[g for g in guards if not only_authorization(g)])
                    productive=z.And(encode_frame(e,conditioned),_effect(e,sf,lookup))
                    original_denial=z.And(*[e.expr(read(qualify(g,slot),prefix_writes,lookup)) for g in p['guards']])
                    detail = {'operation': oid, 'target': f.operations[oid]['target'], 'use_path': pid,
                              'productive_path':spid,'corrected_authorization_guards':removed,
                              'expected_authorization': policy, 'actual_denial': p['guards'],
                              'counterfactual_change': 'only the matched authorization guard is corrected',
                              'other_request_preconditions_retained': True, 'effect_required': True,
                              'argument_domain': 'all_source_inputs_on_this_rejecting_path'}
                    pair(e, z.And(actor != 0, allowed,productive,*prefix_conditions(e)),
                         original_denial, detail, {'caller': actor, 'authorization_holds': allowed})
                  except Unsupported as error:
                    gaps.append({'path':pid,'productive_path':spid,'reason':str(error)})
    elif kind == 'direct_effect':
        cat = req['category']
        if b.complete(oid) and not f.summaries.positions(oid) and all(
                not p.get('sensitive_effects') for _,p in b.paths(oid)):
            rows.append({'state':'not_privileged','operation':oid,
                'reason':'complete_source_has_no_direct_holder_quantity_effect',
                'scope':'local entry only; dependent value uses have separate obligations'})
        for pid, p in b.paths(oid):
            b.check()
            if not safe_path(b, oid, pid, p):
                gaps.append({'path': pid, 'reason': 'effect_path_dependency_unresolved'})
                continue
            qualification = path_qualification(f, oid, p)
            if not qualification:
                # Absence of a privileged path is a scoped exclusion when the
                # source is complete, not a new full-business detector.
                rows.append({'state': 'not_privileged', 'path': pid})
                continue
            try:
                e = MechanismEncoder(lookup)
                z = e.z
                fr = current_frame(pid)
                actor = e.expr(fr['caller'])
                roles, origins = fixed_role_terms(e, qualification, slot)
                moves = movements(b, oid, p)
                for cell in moves['+' if cat == 'FCR-MINT' else '-']:
                    b.check()
                    unit = unit_origin(b, oid, cell)
                    if not unit:
                        gaps.append({'path': pid, 'position': cell, 'reason': 'financial_unit_not_bound'})
                        continue
                    from .ledger import native_only_position
                    if native_only_position(b,oid,cell):
                        rows.append({'state':'not_privileged','path':pid,'position':cell,
                            'reason':'native_account_entitlement_without_source_token_unit_is_additional_scope'})
                        continue
                    holder, start, end, debit, credit = flow(e, lookup, fr, cell)
                    conditions = [end > start] if cat == 'FCR-MINT' else [end < start, holder != actor, holder != 0]
                    details = {'operation': oid, 'target': f.operations[oid]['target'], 'use_path': pid,
                               'role_provenance': qualification, 'encoded_role_origins': origins,
                               'ledger': cell, 'unit': unit, 'category_hypothesis': cat,
                               'argument_domain': 'all_source_inputs_on_this_committing_path',
                               'conditional_call_summary':fr.get('source_call_subcases',[]),
                               'predicate': 'source_bound_financial_effect'}
                    opposite = [c for c in moves['-' if cat == 'FCR-MINT' else '+']
                                if selector_relation(c, cell) == 'same_shape' and key(c) != key(cell)]
                    if cat == 'FCR-MINT':
                        controlled, basis = beneficiary_condition(e, fr, cell, holder)
                        conditions.append(controlled)
                        details['beneficiary'] = basis
                        # A transfer of an existing balance is not issuance.
                        conditions.extend(flow(e, lookup, fr, c)[1] <= flow(e, lookup, fr, c)[2] for c in opposite)
                    elif cat == 'FCR-TRANSFER':
                        destinations = []
                        for c in opposite:
                            from .summary import local_delta
                            debit_amounts = [local_delta(w)[1]
                                             for w in p['writes'] if selector_relation(w['path'],cell)=='same_shape' and
                                             local_delta(w)[0]=='-']
                            credit_amounts = [local_delta(w)[1]
                                              for w in p['writes'] if key(w['path'])==key(c) and
                                              local_delta(w)[0]=='+']
                            if not any(key(d)==key(part) for d in debit_amounts for a in credit_amounts for part in walk(a)):
                                gaps.append({'path':pid,'debit':cell,'credit':c,
                                             'reason':'same_ledger_credit_not_causally_bound_to_debit_quantity'})
                                continue
                            recipient, before, after, _, _ = flow(e, lookup, fr, c)
                            destinations.append(z.And(after > before, recipient != holder, recipient != 0))
                        conditions.append(z.Or(*destinations))
                        details['corresponding_same_ledger_credit'] = opposite
                    elif cat == 'FCR-DESTROY':
                        # Corresponding full token transfers preserve the right.
                        from .financial_value import distributed_value, native_settlement
                        paid,settlement=native_settlement(b,e,oid,fr,cell,holder)
                        conditions.append(start-end>distributed_value(b,e,oid,p,fr,cell,holder,all_transfers=False)+paid)
                        details['same_holder_settlement']=settlement
                    consent_resolved=True
                    if cat!='FCR-MINT':
                        from .financial_value import consent,interpretation_for
                        permitted,consent_resolved,basis=consent(b,e,oid,p,fr,cell,holder,start-end,
                            interpretation_for(prop,oid,pid,cell))
                        details['holder_consent']=basis
                        details['property_validated']=consent_resolved
                        conditions.append(z.Not(permitted))
                    bound = [e.expr(qualify(x['parameter'], slot)) == e.expr(x['value']) for x in context.get('bindings', [])]
                    pair(e, z.And(encode_frame(e, fr), actor != 0, *prefix_conditions(e), *roles, *bound), z.And(*conditions), details,
                         {'actor': actor, 'affected_account': holder, 'before': start, 'after': end, 'gross_debit': debit})
                    if not consent_resolved and queries[-1].get('answer')!='unsat':
                        gaps.append({'path':pid,'position':cell,'reason':'holder_authorization_quantity_basis_unresolved'})
            except Unsupported as error:
                gaps.append({'path': pid, 'reason': str(error)})
    else:
        # Preserve existing finite missing-control and qualified-denial probes.
        # Their output is evidence; the shared property consumer checks its
        # applicability before it can change a finding.
        return auxiliary_property(b, oid, primary_use, context)
    source_rows=list(f.operation_paths(oid))
    covered_with_necessary=bool(necessary_closed) and all(p['flow']=='reverted' or pid in necessary_closed or
        p['flow']in('normal','returned') and not p.get('issues') and not p.get('evaluation_gaps')
        for pid,p in source_rows) and not any(g['kind']=='path_extraction'for g in f.operations[oid]['gaps'])
    exclusion = not reached and bool(rows) and not gaps and (b.complete(oid) or covered_with_necessary) and all(
        r.get('state') in ('unsat', 'not_privileged','necessary_condition_unsat','premise_unsat') for r in rows)
    tested = [x for x in queries if x.get('label') in (kind,'source_necessary_condition') or x.get('label')=='local_premises_feasible' and x.get('answer')=='unsat']
    # Bounded UNSAT closes only its recorded domain unless the source
    # invariant certificate excludes every remaining initial stage.
    exclusion = exclusion and all(x.get('exclusion_certificate', {}).get('excludes_only_this_formula') or
                                  x.get('details', {}).get('prestate', {}).get('global_reachability_exhausted') for x in tested)
    from .quantity_checks import check_quantities
    amount_checks=check_quantities(b,prop) if kind=='direct_effect' else []
    return {'kind': 'causal_compare', 'observed_measure': kind, 'property_identity': context.get('property_identity'),
            'amount_correspondence':amount_checks,
            'independent_use_checks':separate_uses,
            'change': oid, 'observe': primary_use, 'queries': queries, 'property_measurements': rows,
            'property_excluded': exclusion, 'local_errors': gaps or ([] if rows else [{'reason': 'no_applicable_property_path'}]),
            'necessary_condition_route_coverage':{'source_identity':f.identity,'operation':oid,
                'excluded_paths':necessary_closed,'all_source_routes_accounted':covered_with_necessary} if necessary_closed else None,
            'worlds': [], 'comparisons': [], 'evidence_scope': {'target': f.operations[oid]['target'], 'request_context': context},
            'alternative_uses': [], 'holder_consent_counterexamples': [], 'net_measurements': []}

import re
from .request_scope import positive_caller_gate


def auxiliary_property(b,oid,primary_use,context):
    req=context['observable'];kind=req['measure']; f=b.f; lookup=f.lookup(oid)
    queries=[];rows=[];gaps=[]
    def pair(e,base,extra,details,values=None):
        feasible=b._query(e,base,'local_premises_feasible',details); queries.append(feasible)
        if not feasible['bounded_condition_confirmed']:
            rows.append({'feasible_probe':feasible['id'],'state':'premise_'+feasible['answer'],'scope':details});return
        tested=b._query(e,e.z.And(base,extra),kind,details);queries.append(tested)
        rows.append({'feasible_probe':feasible['id'],'result_probe':tested['id'],'state':tested['answer'],'scope':details})
    if kind=='authorization_violation':
        policy=req['authorization']
        for pid,p in b.paths(oid):
            b.check()
            if len(rows)>=f.options.max_prefixes:break
            if not safe_path(b,oid,pid,p):gaps.append({'path':pid,'reason':'authorization_path_dependency_unresolved'});continue
            try:
                e=MechanismEncoder(lookup);z=e.z;fr=frame(f,oid,pid,0)
                actor=e.expr(fr['caller']);expected=e.expr(qualify(policy['predicate'],0))
                detail={'operation':oid,'target':f.operations[oid]['target'],'use_path':pid,
                    'expected_authorization':policy,'actual_guards':fr['guards'],
                    'property_identity':context.get('property_identity'),'semantic_version':context.get('semantic_version',0),
                    'argument_domain':'all_source_inputs_on_this_committing_path'}
                pair(e,z.And(encode_frame(e,fr),actor!=0),z.Not(expected),detail,{'caller':actor,'authorization_holds':expected})
            except Unsupported as err:gaps.append({'path':pid,'reason':str(err)})
    elif kind=='missing_control':
        # Bind a flag to the very holder being debited on a real successful alternative,
        # after a committing writer. Unknowns on that alternative cannot establish a bypass.
        for alt in req['alternatives']:
            use=alt['use'];lookup=f.lookup(use)
            if not b.complete(use):gaps.append({'use':use,'reason':'incomplete_alternative_paths'})
            for cid,cp in b.paths(oid):
                for pid,p in b.paths(use):
                    b.check()
                    if len(rows)>=f.options.max_prefixes:break
                    if not safe_path(b,oid,cid,cp) or not safe_path(b,use,pid,p):
                        gaps.append({'path':pid,'reason':'unknown_on_selected_trace'});continue
                    try:
                        e=MechanismEncoder(lookup);z=e.z;cf=frame(f,oid,cid,0);uf=frame(f,use,pid,1,cf['writes'])
                        for cell in movements(b,use,p)['-']:
                            holder=keys(cell)[0]
                            controls=[w for w in cf['writes'] if len(keys(w['path']))==1 and value_type(w['path'],lookup)=='bool'
                                      and any(x['root']==w['path']['root'] for x in alt['control_writers'])]
                            if len(controls)!=1:continue
                            ctrl=controls[0]; h,_,_,debit,_=flow(e,lookup,uf,cell)
                            zc=e.expr(ctrl['value']);actor=e.expr(cf['caller']);requester=e.expr(uf['caller'])
                            from .behavior import ordered_clocks
                            base=z.And(encode_frame(e,cf),encode_frame(e,uf),*ordered_clocks(e,1),actor!=0,requester!=0,
                                       e.expr(keys(ctrl['path'])[0])==h,h!=0,zc)
                            detail={'change':oid,'observe':use,'change_path':cid,'use_path':pid,'object':cell,'active_holder_control':ctrl['path'],
                                    'control_value':True,'actual_guard_reads':alt['control_reads'],'peer_controlled_uses':alt['peer_controlled_uses'],
                                    'policy_requires_blocking_this_entry':'semantic_hypothesis_only'}
                            pair(e,base,debit>0,detail,{'holder':h,'caller':requester,'gross_debit':debit})
                    except Unsupported as err:gaps.append({'path':pid,'reason':str(err)})
    elif kind=='direct_effect':
        for pid,p in b.paths(oid):
            b.check()
            if len(rows)>=f.options.max_prefixes:break
            if not safe_path(b,oid,pid,p):gaps.append({'path':pid,'reason':'unresolved_dependency'});continue
            qualification=path_qualification(f,oid,p)
            if not qualification:gaps.append({'path':pid,'reason':'no_direct_positive_runtime_role_gate'});continue
            try:
                e=MechanismEncoder(lookup);z=e.z;fr=frame(f,oid,pid,0);actor=e.expr(fr['caller'])
                role_terms, fixed_origins=fixed_role_terms(e,qualification,0)
                moves=movements(b,oid,p); cat=req.get('category')
                for cell in moves['+' if cat=='FCR-MINT' else '-']:
                    origin=unit_origin(b,oid,cell)
                    if not origin:gaps.append({'path':pid,'reason':'unresolved_financial_unit'});continue
                    holder,start,end,dr,cr=flow(e,lookup,fr,cell)
                    detail={'operation':oid,'target':f.operations[oid]['target'],'use_path':pid,'role_guards':[x['guard'] for x in qualification],
                            'role_provenance':qualification,'encoded_role_origins':fixed_origins,'ledger':cell,'unit':origin,
                            'category_hypothesis':cat,'extent':'direct role-gated change of one ledger position; no global supply/consent or compensation judgment'}
                    detail.update(property_identity=context.get('property_identity'),semantic_version=context.get('semantic_version',0))
                    values={'actor':actor,'affected_account':holder,'before':start,'after':end,'gross_debit':dr,'gross_credit':cr}
                    if cat=='FCR-MINT':
                        # This specific probe tests the controller as actual beneficiary.
                        values['self_beneficiary']=holder==actor
                        condition=z.And(end>start,holder==actor)
                    else:condition=z.And(end<start,holder!=actor,holder!=0)
                    if cat=='FCR-TRANSFER':
                        destinations=[]
                        for c in moves['+']:
                            if selector_relation(c,cell)!='same_shape' or key(c)==key(cell):continue
                            recipient,pre,post,_,_=flow(e,lookup,fr,c)
                            destinations.append(z.And(post>pre,recipient!=holder,recipient!=0))
                        condition=z.And(condition,z.Or(*destinations))
                        detail['destination_credit_required']=True
                    bound=[]
                    for binding in context.get('bindings',[]):
                        bound.append(e.expr(qualify(binding['parameter'],0))==e.expr(binding['value']))
                    for a,c,relation in context.get('request_aliases',[]):
                        aa=e.expr(qualify(a,0));cc=e.expr(qualify(c,0));bound.append(aa==cc if relation=='==' else aa!=cc)
                    detail['predicate']='positive_credit_to_caller' if cat=='FCR-MINT' else 'negative_delta_of_other_nonzero_holder'
                    detail['argument_domain']='all_source_inputs_on_this_committing_path'
                    if context.get('request_aliases'):
                        detail.update(argument_domain='recorded_claim_aliases',claim_aliases=context['request_aliases'])
                    pair(e,z.And(encode_frame(e,fr),actor!=0,*role_terms,*bound),condition,detail,values)
            except Unsupported as err:gaps.append({'path':pid,'reason':str(err)})
    elif kind=='denied_qualified':
        # Eligibility is a named source role backed by a positive use on another
        # applied entry. Its applicability to this use remains an explicit hypothesis.
        for pid,p in f.operation_paths(oid):
            if p['flow']!='reverted' or not p['guards'] or len(rows)>=f.options.max_prefixes:continue
            b.check()
            if not safe_path(b,oid,pid,p):gaps.append({'path':pid,'reason':'unknown_rejection_dependency'});continue
            cause=p['guards'][-1]
            leaf=cause
            while leaf.get('op')=='!' and len(leaf['args'])==1:leaf=leaf['args'][0]
            if leaf.get('op') not in ('==','!=') or not any(x.get('kind')=='actual_sender' for x in leaf['args']):continue
            roles=[c for c in selectors(leaf) if not keys(c) and value_type(c,lookup) in ('address','address payable')]
            if len(roles)!=1:continue
            role=roles[0]; name=b._storage_name(oid,role)
            if not re.search(r'(?<![\w$])'+re.escape(name)+r'(?![\w$])',req['claim'],re.I):continue
            peers=[j for j,o in f.operations.items() if j!=oid and o['target']==f.operations[oid]['target'] and any(
                positive_caller_gate(g,lookup) and any(key(c)==key(role) for c in selectors(g)) for _,v in b.paths(j) for g in v['guards'])]
            if not peers:continue
            if p.get('writes') or p.get('sensitive_effects'):gaps.append({'path':pid,'reason':'complex_pre_rejection_effects'});continue
            try:
                e=MechanismEncoder(lookup);z=e.z;actor=e.expr(qualify({'kind':'actual_sender'},0))
                for term in p.get('evaluated_terms',[]):e.expr(qualify(term,0))
                earlier=[e.expr(qualify(g,0)) for g in p['guards'][:-1]]
                policy=actor==e.expr(qualify(role,0))
                base=z.And(actor!=0,policy,*earlier)
                detail={'operation':oid,'revert_path':pid,'role':role,'positive_role_use_sources':peers,'non_authorization_prefix':p['guards'][:-1],
                        'denial_condition':cause,'role_eligibility_at_use':'source-backed semantic hypothesis','failed_request_commits_writes':False}
                pair(e,base,e.expr(qualify(cause,0)),detail,{'caller':actor,'role':e.expr(qualify(role,0))})
            except Unsupported as err:gaps.append({'path':pid,'reason':str(err)})
    return {'kind':'causal_compare','observed_measure':kind,'change':oid,'observe':primary_use,'queries':queries,'property_measurements':rows,
            'local_errors':gaps or ([] if rows else [{'reason':'no_source_supported_path_for_property'}]),'worlds':[],'comparisons':[],
            'evidence_scope':{'target':f.operations[oid]['target'],'request_context':context,'controls':[]},
            'alternative_uses':[],'holder_consent_counterexamples':[],'net_measurements':[],'business_policy_proved':False}

```

## source/src/pr_next_joint/investigation/policy_binding.py

原文件SHA256 `ca3834eda4f4a6174b381116ab14d31cb09de380fec655d4b6a0bbfa97aad145`

```python
"""Scope source explanations before compiling an authorization predicate.

The source signature is derived from the located explanation and the applied
entry's committed paths. The compiled signature is read back from the IR.
Only the supported equivalences of boolean literals and ordered cells are used.
"""
import re

from pr_next_joint.frontend.path_ir import key, lit, op
from pr_next_joint.frontend.storage import keys, value_type
from pr_next_joint.frontend.source_entry_identity import function_kind
from .key_roles import relation as key_role


def mentioned(text, name):
    return bool(name and re.search(r'(?<![\w$])' + re.escape(name) + r'(?![\w$])', text))


def effect_duty(text):
    """Identify the subject of a responsibility, not the subjects of nearby observations.

    Subject phrases are open vocabulary. Only the positive argument of a
    permission, duty, assignment or required consent can enter source binding.
    """
    if not isinstance(text, str): return None
    roles = []
    qualified = False
    alternative = False
    noun = r"(?P<actor>[\w$][\w$.'’ -]*?)"
    frames = (
        r"\bonly\s+" + noun + r"\s+(?:may|can|is entitled to|is allowed to)\s+\w+",
        r"^(?:only\s+)?" + noun + r"\s+(?:is|are|remains?)\s+(?:solely\s+)?(?:responsible for|entrusted with|authorized to|in charge of)\s+\w+",
        r"^" + noun + r"\s+(?:who\s+)?(?:governs?|has authority over|has the right to decide)\s+\w+",
        r"^" + noun + r"\s+(?:must|shall)\s+(?:also\s+)?(?:consent|authorize|approve)\b",
        r"\b(?:assigns?|entrusts?|reserves?)\s+[^,;.!?]*\b(?:decision|responsibility|approval|authority|right|appointment|discretion)\b[^,;.!?]*?\s+to\s+" + noun + r"$",
        r"\b(?:decided by|authorized solely by)\s+" + noun + r"$",
        r"\b(?:decisions?|authority|responsibility)\s+(?:is|are|remains?)\s+" + noun + r"['’]s(?:\s+\w+)?$",
        r"\bat\s+" + noun + r"['’]s\s+discretion\b",
        r"\b(?:responsibility|right|authority|decision)\b[^;,.]*?\b(?:belongs to|lies with|rests with|is reserved for)\s+" + noun + r"$",
        r"\b(?:requires?|needs?|without)\s+" + noun + r"(?:['’]s|\s+)\s*(?:approval|consent|authorization)\b",
        # "also" adds a prerequisite; it must not make the whole consent
        # clause disappear while a different actor's authority remains normal.
        # Keep it inside the positive requirement grammar, so "not required"
        # and "also not required" do not become affirmative holder consent.
        noun + r"(?:['’]s|\s+)\s*(?:approval|consent|authorization)\s+(?:is\s+(?:also\s+)?(?:required|necessary)|must\s+(?:also\s+)?be\s+obtained)\b",
        r"(?:只有|仅限)\s*(?P<actor>[\w$]+?)\s*(?:有权|才可|才能)",
        r"(?:须经|必须经|应由)\s*(?P<actor>[\w$]+?)\s*(?:同意|授权|批准|决定)",
    )
    for part in re.split(r"[;；。!?，,]|\.(?=\s|$)|\b(?:but|yet|whereas|although|however)\b", text, flags=re.I):
        clause = part.strip()
        # The subject of an executable check describes a precondition. It does
        # not assign the authority to make the business decision.
        if re.match(r"^(?:(?:in|under|according to)\s+)?(?:the\s+)?(?:actual\s+|current\s+|implemented\s+)?(?:implementation|source(?:\s+code)?|code|runtime|guard|[\w$]+\s+(?:guard|check))\b", clause, re.I):
            continue
        restriction = re.search(r"\b(only if|if|unless|provided(?: that)?|subject to|together with|in addition to|as well as|with(?= (?:the )?(?:[\w’'-]+\s+){0,4}(?:consent|approval)))\s+(.*)$", clause, re.I)
        additional = None
        if restriction:
            # Separate the approval of another actor from a condition on the
            # first actor's identity. Unknown qualifiers cannot certify a normal.
            rest = restriction[2]
            if restriction[1].casefold() != 'unless':
                agreed = (re.match(r"(?:the\s+)?(?:consent|approval|authorization)\s+(?:of|from)\s+" + noun + r"$", rest, re.I)
                          or re.match(noun + r"(?:['’]s\s+|\s+)(?:also\s+)?(?:consents?|approves?|authoriz(?:es|ation)|approval)\b", rest, re.I))
                if agreed:
                    additional = agreed['actor']
            clause = clause[:restriction.start()].strip()
            if not clause and roles:
                if additional and not alternative:
                    roles.append(additional)
                else:
                    qualified = True
                continue
        for pattern in frames:
            match = re.search(pattern, clause, re.I)
            if not match:
                continue
            if re.search(r"\b(?:not|never|neither|whether|if)\s+(?:solely\s+)?$", clause[:match.start()], re.I):
                continue
            actor = match['actor'].strip()
            if re.search(r"\b(?:not|never|neither|whether|if|unless)\b", actor, re.I):
                continue
            names = re.split(r"\s+(and|or)\s+", actor, flags=re.I)
            joins = {s.casefold() for s in names[1::2]}
            qualified |= len(joins) > 1 or bool(roles and (alternative or 'or' in joins))
            alternative |= 'or' in joins
            actors = names[::2]
            if restriction:
                if additional:
                    actors.append(additional)
                    qualified |= alternative
                else:
                    qualified = True
            for value in actors:
                value = re.sub(r"^(?:(?:only|the|a|an|same)\s+)+", "", value.strip(), flags=re.I)
                if value and value.casefold() not in ('their','his','her','its','it','they'):
                    if value.casefold() not in [v.casefold() for v in roles]:
                        roles.append(value)
            break
    if not roles:
        return None
    return {'actors': roles, 'alternative': alternative, 'qualified': qualified}


def positive_role_reference(text, name):
    """A denial of the relevance of a named role is not a policy in its favour."""
    for part in re.split(r'[;；,，]|(?<=[.!?])\s+|\b(?:but|whereas|however)\b', text, flags=re.I):
        if not mentioned(part, name):
            continue
        qualifier=r'(?:[A-Za-z_$][\w$]*\.)*' if '.' not in name else ''
        token = r'(?<![\w$])' + qualifier + re.escape(name) + r'(?![\w$])'
        denial = (r'\b(?:no|not|without|neither)\s+(?:(?:the|an?|any|require[sd]?|requiring|need[s]?|be|being)\s+){0,4}'
                  + token + r'|' + token + r'.{0,28}\b(?:not (?:required|needed|applicable)|irrelevant)\b')
        if not re.search(denial, part, re.I):
            return True
    return False


def creation_source(text, entry, operations):
    """Bind normative deployment language to its subject, not a distant use."""
    name = entry['function'].split('(')[0]
    names = {o['function'].split('(')[0] for o in operations.values() if o['target']==entry['target']}
    focus = set()
    for clause in re.split(r'[;；，,]|(?<=[.!?。])\s+|\b(?:but|whereas|however)\b', text, flags=re.I):
        creation = re.search(r'\b(?:deployment.only|only (?:at|during) (?:construction|creation|deployment)|'
                             r'(?:intended|meant|supposed|required|should|must)\b.{0,38}\b(?:constructor|deployment|creation)\b|'
                             r'constructor.only|constructor\s+(?:only|semantics))', clause, re.I)
        # Objects listed as effects after "deployment-only" are not the
        # grammatical subject of that restriction.
        head=clause[:creation.start()] if creation else clause
        found={n for n in names if mentioned(head,n)}
        if found:
            focus=found
        elif not re.search(r'\b(?:it|this|the function|required|authorization|deployment.only)\b',clause,re.I):
            focus=set()
        if focus=={name} and creation:
            return clause.strip()
    return None


def boolean_leaf(term):
    """Return the storage atom and truth value for one committing-path guard."""
    if not isinstance(term, dict):
        return None
    if term.get('kind')=='storage':
        return term, True
    args=term.get('args', [])
    if term.get('op') in ('!', 'not') and len(args)==1:
        child=boolean_leaf(args[0])
        return (child[0], not child[1]) if child else None
    if term.get('op') in ('==','!=') and len(args)==2:
        for atom,const in (args, reversed(args)):
            if const.get('kind')=='literal' and type(const.get('value')) is bool:
                child=boolean_leaf(atom)
                if child:
                    return child[0], child[1] == (const['value'] == (term['op']=='=='))
    return None


def conjuncts(term):
    if term.get('op') in ('&&','and'):
        return [a for v in term['args'] for a in conjuncts(v)]
    return [term]


def stated_boolean(text,name):
    token=r'(?<![\w$])'+re.escape(name)+r'(?![\w$])'
    sub=token+r'(?:\s*\[[^\]]+\]){0,3}'
    values=set()
    if re.search(r'!\s*'+sub,text) or re.search(sub+r'\s*(?:==|is|must be)\s*false\b',text,re.I):
        values.add(False)
    if re.search(sub+r'\s*(?:==|is|must be)\s*true\b',text,re.I):
        values.add(True)
    collective=re.search(r'\bboth\s+(?:be\s+)?(true|false)\b',text,re.I)
    if collective and mentioned(text,name):values.add(collective[1].lower()=='true')
    return values


def payment_policy(text, role_name, scope_names):
    """Read the asserted relation between actual role and payment operands."""
    pay = r'\b(?:payment|paying|paid|fee)\b'
    role = r'(?<![\w$])' + re.escape(role_name.lower()) + r'(?![\w$])'
    names = {n.lower() for n in scope_names if n}
    relations = set()
    text = re.sub(r'["“][^"”]*["”]|(?<!\w)\x27[^\x27\n]+\x27(?!\w)', ' ', text.lower())
    # Retain the payment subject through a nominal complement. The modal
    # predicate below still decides sufficiency, denial and contradictions.
    text=re.sub(r'\bpayment of (?:the |a )?(?:fee|charge)\b','payment',text)
    for sentence in re.split(r'[;；。!?\n]|(?<=\.)\s+', text):
        if re.search(role+r'\s+or\s+(?:an? |the )?(?:customer|holder|caller)\s+paying\b',sentence) and re.search(r'\bmay independently authorize\b',sentence):
            relations.add('independent')
        payment_subject = False
        # A role-only requirement in a following contrastive clause still
        # qualifies an earlier claimed payment permission in this sentence.
        sentence_mentions_payment = bool(re.search(pay, sentence))
        for clause in re.split(r'\b(?:but|whereas|however)\b', sentence):
            clause = clause.strip(' ,.'); scoped = re.search(r'\b(?:policy|rule) (?:for|of|on) (?:the )?([\w.$]+)', clause)
            if scoped and scoped[1].split('.')[-1] not in names | {'entry','effect','action','operation'}:
                continue
            if re.search(r'\b(?:implementation|implemented|hypothetically|supposed|mistakenly|incorrectly)\b', clause):
                continue
            if payment_subject and re.match(r'^it\b', clause):
                clause = 'payment' + clause[2:]
            clause = re.sub(r'^(?:under|according to) (?:the )?(?:policy|rule)(?: for [\w.$]+)?,\s*', '', clause)
            payment_subject = bool(re.match(r'^(?:(?:the|a|threshold|qualifying)\s+)*'+pay, clause))
            mentions_pay = bool(re.search(pay, clause))
            if re.search(r'\b(?:unclear|unresolved|unknown|uncertain|whether|undetermined)\b', clause):
                if mentions_pay: relations.add('unresolved')
                continue
            # Modal qualifiers qualify the entitlement itself. An additional
            # condition of unknown meaning cannot yield unrestricted permission.
            restricted = re.search(r'\b(?:if|unless|provided|subject to|except|conditional on)\b',clause)
            same_effect = any(mentioned(clause,n) for n in names) or re.search(r'\b(?:this|same) (?:action|effect|entry)\b',clause)
            exclusive = re.search(r'\bonly\s+(?:(?:the|a|current|authorized|incumbent)\s+)*'+role+
                                  r'(?:\s+holder)?\s+(?:may|can|must|is (?:authorized|permitted) to)\s+\w+',clause)
            if exclusive and not restricted and not re.search(r'\b(?:not|denies|rejects?)\s+$',clause[:exclusive.start()]):
                if same_effect or re.search(r'\b(?:authorize|approve)$',clause):
                    relations.add('role_required')
            if not mentions_pay:
                # Do not let 'payment can substitute, but callers must ALSO
                # hold the office' become an unconditional OR authorization.
                # This expresses a conflict with a purported independent
                # alternative; it does not prove a new authorization policy.
                caller_requires_role = re.search(
                    r'\b(?:caller|applicant|requester)\b.{0,35}\b'
                    r'(?:must|shall|needs? to|is required to)\s+(?:also\s+)?'
                    r'(?:be\s+)?(?:the\s+)?'+role, clause)
                role_is_required = re.search(role+r'\s+(?:is|remains)\s+'
                    r'(?:also\s+)?(?:required|necessary|mandatory)\b', clause)
                if sentence_mentions_payment and (caller_requires_role or role_is_required):
                    relations.add('role_required')
                continue
            policy = re.match(r'^(?:(?:the|this|applicable|approved|authorization|stated|intended|business)\s+)*'
                              r'(?:policy|rule)(?:\s+(?:for|of|on)\s+[\w.$()]+)?\s+'
                              r'(?:(?:expressly|explicitly|strictly|specifically)\s+)?'
                              r'(?:(?:does|can|may)\s+)?'
                              r'(?:(?:expressly|explicitly|strictly|specifically)\s+)?'
                              r'(?P<neg>not\s+|never\s+)?(?P<verb>allows?|permits?|accepts?|forbids?|rejects?|requires?)\b(?P<object>.*)',clause)
            obj = policy['object'] if policy else clause
            has_role = bool(re.search(role,obj))
            joint = has_role and (re.search(r'\b(?:only\s+)?(?:in addition to|together with|in conjunction with)\b',obj)
                    or re.search(r'\bboth\b.+\band\b',obj) and
                    (re.search(r'\b(?:required|necessary|needed)\b',obj) or policy and policy['verb'].startswith('require')))
            denied = bool(policy and (bool(policy['neg']) != policy['verb'].startswith(('forbid','reject'))))
            denies_alternative = re.search(r'\b(?:not|never)\s+(?:as\s+)?(?:an?\s+)?(?:alternative|substitute|authorization|qualification)\b',obj)
            explicit_requirement = re.fullmatch(r'both\s+(?:the\s+)?'+role+
                r"(?:'s)?(?:\s+(?:approval|authorization|consent))?\s+and\s+(?:the\s+)?(?:payment|fee)\s+(?:are|remain)\s+(?:required|necessary)",clause)
            normative_joint = bool(policy or explicit_requirement or same_effect and re.search(r'\b(?:must|required|necessary|needed)\b',obj))
            either_or = bool(has_role and re.search(r'\beither\b.+\bor\b',obj))
            if joint and normative_joint:
                negated_joint = re.search(r'\b(?:not|never)\s+(?:only|together|required|necessary|needed)\b',obj)
                relations.add('unresolved' if restricted or denied or negated_joint or either_or else 'joint')
                continue
            if not policy and not payment_subject: continue
            if policy and policy['neg'] and policy['verb'].startswith(('forbid','reject')):
                relations.add('unresolved')
                continue
            if restricted or re.search(r'\bonly\b(?! (?:the|a|current) )',obj):
                relations.add('unresolved')
                continue
            alternative = re.search(r'\b(?:alternative|either\b.+\bor|in place of|instead of|replace[sd]?|substitut\w*)\b',obj)
            authority = re.search(r'\b(?:authoriz\w*|sufficient|qualif\w*|constitut\w* authorization)\b',obj)
            if not alternative and not authority: continue
            if payment_subject:
                # Only a predication about the payment establishes its force.
                atom = re.match(r'^(?:(?:the|a|qualifying|threshold)\s+)*'+pay+
                                r'(?:\s+(?:the\s+)?threshold)?(?:\s+(?:alone|itself|independently))?\s+'
                                r'(?:(?:does|can|is|may)\s+)?(?P<sign>not\s+|never\s+|cannot\s+)?'
                                r'(?:independently\s+)?(?:authoriz\w*|sufficient|a qualification|constitut\w*|replace\w*|substitut\w*)\b',obj)
                if not atom: continue
                denied = bool(atom['sign'])
            if denied or denies_alternative:
                relations.add('role_required')
            elif policy and policy['verb'].startswith('require'):
                # Being required makes payment necessary; it need not authorize on its own.
                relations.add('independent' if either_or else 'unresolved')
            elif alternative or authority and re.search(r'\b(?:as authorization|to authorize|sufficient|authorizes?|constitut\w* authorization)\b',obj):
                relations.add('independent')
            else:
                relations.add('unresolved')
    if 'unresolved' in relations or 'independent' in relations and len(relations)>1:
        return 'unresolved'
    return next((mode for mode in ('joint','role_required','independent') if mode in relations),None)


def scoped_payment_denial(text, role_name, entry_name, scope_names):
    """Allow role inference only for an explicit policy denying pay on THIS effect.

    The inferred role is a *necessary* guard operand, never a free-standing
    authorization source. Vague claims, alternate authorities or statements
    about a different effect do not qualify.
    """
    if not entry_name or mentioned(text, role_name):
        return False
    clauses = [v.strip() for v in re.split(r'[;；\n]|(?<=[.!?。])\s+', text) if v.strip()]
    if len(clauses) != 1:
        return False
    clause = clauses[0]
    if not mentioned(clause, entry_name) or not re.search(r'\b(?:policy|rule)\b', clause, re.I):
        return False
    # No inference across competing, conditional or hypothetical policy claims.
    if re.search(r'\b(?:but|however|whereas|unless|except|provided|subject to|'
                 r'unknown|unclear|whether|hypothetically|instead|another|other|either|if)\b', clause, re.I):
        return False
    # A second claimed authorizer in the same sentence must not be silently
    # erased by assuming the observed role is the only legitimate source.
    if re.search(r'\band\b.{0,100}\b(?:authoriz\w*|qualif\w*|approv\w*|permitt\w*|grant\w*)\b',
                 clause, re.I):
        return False
    return payment_policy(clause, role_name, scope_names) == 'role_required'


def role_payments(rows, lookup, text, subject=None, *, derive_role_from_source=False):
    """Find actual alternative operands. Their occurrence proves no business permission.

    `derive_role_from_source` may only be used after independently checking a
    narrowly scoped normative payment exclusion and one stable source role.
    """
    scoped = {}
    for _, path in rows:
        for guard in path['guards']:
            for disj in conjuncts(guard):
                if disj.get('op') not in ('or','||') or len(disj.get('args',())) != 2:
                    continue
                for role, condition in (disj['args'], reversed(disj['args'])):
                    args = role.get('args', ())
                    if role.get('op') != '==' or not any(t.get('kind')=='actual_sender' for t in args):
                        continue
                    cell = next((t for t in args if t.get('kind')=='storage' and not keys(t)), None)
                    if not cell or (cell != subject if subject is not None else
                                    not derive_role_from_source and not positive_role_reference(
                                        text, lookup.nodes[cell['root']].get('name'))):
                        continue
                    pay = condition.get('args', ())
                    if len(pay)!=2 or condition.get('op') not in ('>=','>','<=','<'):
                        continue
                    value, threshold = pay if condition['op'] in ('>=','>') else reversed(pay)
                    if value.get('kind')=='transaction_value' and threshold.get('kind') in ('literal','storage'):
                        scoped[key([role,condition,cell])] = (role,condition,cell)
    return list(scoped.values())


def source_requirement(inv, q, explanation, rows):
    entry=inv.f.operations[inv.root(q)]
    lookup=inv.f.lookup(inv.root(q))
    declaration=lookup.nodes.get(entry['source'].get('ast_id'),{})
    text=str(explanation.get('text') or explanation.get('basis') or '')
    signature={'target':entry['target'],'operation':inv.root(q),'declaration':declaration.get('id'),
               'frame':'before_effect','path_sources':[pid for pid,_ in rows]}
    clause=creation_source(text,entry,inv.f.operations)
    if clause and declaration.get('nodeType')=='FunctionDefinition' and function_kind(declaration)!='constructor':
        return dict(signature,kind='creation_only_source_policy',clause=clause,frame='runtime entry')
    # Use the already source-derived role of each ordered key, never a function name.
    grants={}
    if re.search(r'\b(?:allowance|grant|approval|spender)\b|额度|受托|授权额度',text,re.I):
        for _,p in rows:
            for write in p['writes']:
                cell=write['path']
                role=key_role(cell,lookup)
                if role and role['kind']=='authorization_quantity':
                    idx=keys(cell)
                    if len(idx)==2:
                        h=role['holder_key']
                        grants[key(cell)]={'cell':cell,'issuer':idx[h],'spender':idx[1-h],'quantity':write['value']}
    own=re.search(r"\b(?:own|self|issuer|holder.s|on behalf of|someone else.s|another holder.s)\b|本人|持有人",text,re.I)
    additional_policy=any(positive_role_reference(text,n['name']) for n in lookup.decls.values()
                          if n.get('stateVariable') and n.get('name') and
                          (n.get('typeDescriptions',{}).get('typeString') or '').startswith('address'))
    if grants and own and len(grants)==1 and not additional_policy:
        return dict(signature,kind='source_grant_issuer',grant=next(iter(grants.values())))
    # A named source check identifies its precise relation only if every
    # committing branch agrees. Do not promote a branch-specific atom.
    if not rows:
        return None
    # Both interfaces use the same normative relation and the same source operands.
    typed = explanation.get('explicit_policy_kind') == 'current_authority_required'
    entry_name = entry['function'].split('(')[0]
    names = {entry_name} | {lookup.nodes.get(w['path']['root'],{}).get('name')
                            for _, path in rows for w in path['writes']}
    candidates = role_payments(rows, lookup, text, explanation.get('qualified_cell') if typed else None)
    if not candidates and not typed and rows:
        # A legacy issue can locate the exact effect without repeating the
        # source role's identifier. Only derive that role when (a) the policy
        # explicitly excludes payment as authorization for THIS entry, and
        # (b) every committing path has the same unique role-or-pay guard.
        # The derived role is a necessary authorization prerequisite, not a
        # proof that this role alone is sufficient for any other effect.
        inferred = role_payments(rows, lookup, text, derive_role_from_source=True)
        if len(inferred) == 1:
            role, payment, cell = inferred[0]
            role_name = lookup.nodes[cell['root']].get('name')
            same_in_all_paths = all(
                len(row_candidates := role_payments([(pid, path)], lookup, text,
                    derive_role_from_source=True)) == 1 and key(row_candidates[0]) == key(inferred[0])
                for pid, path in rows)
            if same_in_all_paths and scoped_payment_denial(text, role_name, entry_name, names):
                candidates = inferred
    if candidates:
        role, payment, cell = candidates[0]
        sign = (explanation.get('payment_policy') or 'role_required') if typed else payment_policy(text, lookup.nodes[cell['root']]['name'],names)
        if sign in ('independent','joint','role_required') and len(candidates) == 1:
            return dict(signature,kind='source_role_payment_policy',role=role,payment=payment,subject=cell,
                        payment_relation=sign, permits_payment=sign=='independent')
        # Describing the actual guard or naming its role is insufficient to
        # select one of its authorization branches as the governing rule.
        return dict(signature,kind='unresolved_role_payment_policy')
    if typed and explanation.get('payment_policy') in ('unresolved','independent','joint'):
        return dict(signature,kind='unresolved_role_payment_policy')
    paths=[]
    for _,p in rows:
        atoms={}
        for guard in p['guards']:
            for term in conjuncts(guard):
                leaf=boolean_leaf(term)
                if not leaf:continue
                cell,truth=leaf
                if keys(cell) and value_type(cell,lookup)=='bool' and mentioned(text,lookup.nodes[cell['root']].get('name')):
                    atoms[key([cell,truth])]=(cell,truth)
        paths.append(atoms)
    if paths[0] and all(set(p)==set(paths[0]) for p in paths):
        atoms=[]
        for c,observed in paths[0].values():
            name=lookup.nodes[c['root']].get('name')
            truths=stated_boolean(text,name)
            if len(truths)>1:return None
            observed_normal=(explanation.get('meaning')=='normal_authorization' and
                re.search(r'\b(?:own|self|msg\.sender.s)\b',text,re.I) and
                re.search(r'\b(?:checks?|requires?|subject to)\b',text,re.I))
            if not truths and not observed_normal:return None
            truth=next(iter(truths)) if truths else observed
            atoms.append({'cell':c,'permitted_truth':truth,'observed_guard_truth':observed,
                'basis':'explicit_source_bound_condition' if truths else 'stated_normal_use_subject_to_actual_check'})
        return dict(signature,kind='source_guarded_eligibility',atoms=atoms)
    return None


def compile_requirement(requirement,explanation,lookup):
    kind=requirement['kind']
    subject=None
    if kind=='source_role_payment_policy':
        subject=requirement['subject']
        mode=requirement['payment_relation']
        predicate=requirement['role'] if mode=='role_required' else op(
            'and' if mode=='joint' else 'or', requirement['role'], requirement['payment'])
    elif kind=='source_grant_issuer':
        subject=requirement['grant']['issuer']
        predicate=op('==',{'kind':'actual_sender'},subject)
    elif kind=='source_guarded_eligibility':
        terms=[a['cell'] if a['permitted_truth'] else op('!',a['cell']) for a in requirement['atoms']]
        predicate=terms[0] if len(terms)==1 else op('and',*terms)
        if len(terms)==1:subject=requirement['atoms'][0]['cell']
    else:
        predicate=lit(False)
    return {'predicate':predicate,'subject':subject,'kind':kind,'property_family':'use',
            'normal_alternatives':[],'source_bound_alternatives':[],'business_basis':explanation,
            'necessary_only':kind=='source_role_payment_policy' and requirement['payment_relation']!='independent',
            'acquisition_uses':[],'binding':{'declaration':requirement['declaration'],'frame':requirement['frame'],
            'source':lookup.anchor(lookup.nodes[requirement['declaration']])},'source_requirement':requirement}


def compare_requirement(required,compiled,entry_id,declaration,target):
    """Check independent source facts against the expression consumed by M4."""
    p=compiled.get('predicate') or {}
    binding=compiled.get('binding') or {}
    scope_ok=(entry_id==required['operation'] and target==required['target'] and
              binding.get('declaration')==declaration==required['declaration'] and binding.get('frame')==required['frame'])
    if required['kind']=='source_role_payment_policy':
        mode=required['payment_relation']
        if mode=='role_required':
            actual,wanted=key(p),key(required['role'])
        else:
            actual=[p.get('op'),sorted(key(t) for t in p.get('args',[]))]
            wanted=[{'joint':'and','independent':'or'}[mode],sorted(key(required[t]) for t in ('role','payment'))]
        equal=actual==wanted and compiled.get('necessary_only')==(mode!='independent')
    elif required['kind']=='source_guarded_eligibility':
        leaves=[boolean_leaf(t) for t in conjuncts(p)]
        actual=sorted(key([c,b]) for leaf in leaves if leaf for c,b in [leaf])
        wanted=sorted(key([a['cell'],a['permitted_truth']]) for a in required['atoms'])
        equal=len(actual)==len(leaves) and actual==wanted
    elif required['kind']=='source_grant_issuer':
        actual=sorted(key(t) for t in p.get('args',[]))
        wanted=sorted(key(t) for t in ({'kind':'actual_sender'},required['grant']['issuer']))
        equal=p.get('op')=='==' and actual==wanted
    else:
        actual=[p.get('kind'),p.get('value'),compiled.get('acquisition_uses')]
        wanted=['literal',False,[]]
        equal=actual==wanted and type(p.get('value')) is bool
    return {'matches':scope_ok and equal,'scope_matches':scope_ok,'source':wanted,'compiled':actual,
            'frame':binding.get('frame'),'operator':p.get('op',p.get('kind'))}


def audit_authorization(f,oid,compiled):
    """Recheck at consumption, including each independently scoped alternative."""
    if not isinstance(compiled,dict):return []
    alternatives=compiled.get('competing_interpretations')
    if alternatives:
        expected=[p['predicate'] for p in alternatives]
        actual=compiled.get('predicate',{})
        results=[r for p in alternatives for r in audit_authorization(f,oid,p)]
        results.append({'matches':actual.get('op')=='or' and
                        sorted(map(key,actual.get('args',[])))==sorted(map(key,expected)),
                        'scope':'surviving_source_interpretations'})
        return results
    requirement=compiled.get('source_requirement')
    if not requirement:return []
    op_info=f.operations[oid]
    return [compare_requirement(requirement,compiled,oid,op_info['source'].get('ast_id'),op_info['target'])]


def source_excludes_violation(f,oid,compiled):
    """A local proof over all the located committing paths, for this policy only."""
    required=compiled.get('source_requirement') or {}
    # A source-scoped before/after check for a stage flag: once it is true,
    # setting that identical cell to true cannot commit the prohibited change.
    # Independent sibling effects have separate policy/coverage consumers.
    scoped=compiled.get('effect_write')
    if compiled.get('kind')=='scope_bound_initialization_stage' and scoped and not compiled.get('competing_interpretations'):
        cell=scoped['cell']
        if key(cell)!=key(compiled.get('subject')) or compiled.get('predicate')!=op('!',cell):return None
        path=next((p for pid,p in f.operation_paths(oid,True) if pid==scoped['path']),None)
        if not path or path.get('issues') or path.get('evaluation_gaps') or path.get('sensitive_effects'):return None
        writes=[w for w in path['writes'] if w['path'].get('root')==cell['root']]
        if not writes or any(w['path']!=cell for w in writes) or writes[-1]['value']!=lit(True):return None
        return {'basis':'already_set_stage_flag_has_no_further_net_change','source_identity':f.identity,'operation':oid,
                'target':f.operations[oid]['target'],'paths':[scoped['path']],'scope':'only the bound stage flag',
                'other_policies_or_effects_closed':False}
    if compiled.get('competing_interpretations') or required.get('kind') not in ('source_grant_issuer','source_guarded_eligibility'):
        return None
    paths=list(f.operation_paths(oid))
    if not paths or f.operations[oid].get('gaps') or any(
            p['flow'] not in ('normal','returned','reverted') or p.get('issues') or p.get('evaluation_gaps')
            for _,p in paths):return None
    commits=[(pid,p) for pid,p in paths if p['flow'] in ('normal','returned')]
    if not commits or set(required['path_sources'])!={pid for pid,_ in commits}:return None
    if required['kind']=='source_grant_issuer':
        issuer=required['grant']['issuer']
        if issuer!={'kind':'actual_sender'}:return None
        cell=required['grant']['cell']
        # Other state updates/effects require independent policies.
        if any(p.get('sensitive_effects') or any(key(w['path'])!=key(cell) for w in p['writes']) for _,p in commits):
            return None
        reason='exact_caller_owns_written_grant_key'
    else:
        needed={key([a['cell'],a['permitted_truth']]) for a in required['atoms']}
        for _,p in commits:
            actual=set()
            for g in p['guards']:
                for t in conjuncts(g):
                    leaf=boolean_leaf(t)
                    if leaf:actual.add(key(list(leaf)))
            if not needed<=actual:return None
        reason='authorized_boolean_condition_is_necessary_on_each_committing_path'
    return {'basis':reason,'source_identity':f.identity,'operation':oid,'target':required['target'],
            'paths':[pid for pid,_ in commits],'scope':'only this use of this source-verified policy',
            'other_policies_or_effects_closed':False}

```

## source/src/pr_next_joint/investigation/prestate.py

原文件SHA256 `d985f5498edb16ca90e48d4f06b90eb5e07538b8d91f971666a437c01d832239`

```python
"""Narrow initial-state invariants. Never equate a deployment choice with a current value."""
from functools import lru_cache
from pr_next_joint.frontend.path_ir import walk,key
from pr_next_joint.frontend.storage import selectors


def literal(node):
    if not isinstance(node,dict):return None
    if node.get('nodeType')=='FunctionCall' and node.get('kind')=='typeConversion' and len(node.get('arguments',[]))==1:
        type_name=node.get('expression',{}).get('typeName',{})
        target=type_name.get('name') if isinstance(type_name,dict) else type_name if isinstance(type_name,str) else None
        value=literal(node['arguments'][0])
        if type(value)is not int:return None
        import re
        numeric=re.fullmatch(r'uint(\d*)',target or '')
        width=160 if target in ('address','address payable') else int(numeric[1] or 256) if numeric else None
        return value if width and 0<=value<2**width else None
    if node.get('nodeType')!='Literal':return None
    typ=node.get('kind'); v=str(node.get('value',''))
    if typ in ('bool','boolean') and v in ('true','false'):return v=='true'
    if typ in ('number','hexNumber') and not node.get('subdenomination'):
        try:return int(v.replace('_',''),0)
        except ValueError:return None
    return None


def _legacy_state_facts(lookup):
    if hasattr(lookup,'_relational_initial'):return lookup._relational_initial
    bases=lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
    declarations=[n for b in bases for n in lookup.nodes[b].get('nodes',[])]
    # Assembly, delegate execution or a storage-reference alias can defeat AST write exclusion.
    functions=[n for n in declarations if n.get('nodeType') in ('FunctionDefinition','ModifierDefinition')]
    opaque=any(n.get('nodeType') in ('InlineAssembly','YulBlock') or n.get('memberName') in ('delegatecall','callcode')
         or n.get('nodeType')=='VariableDeclaration' and n.get('storageLocation')=='storage' for fn in functions for n in walk(fn))
    table={}
    for var in declarations:
        typ=var.get('typeDescriptions',{}).get('typeString','')
        if not var.get('stateVariable') or not (typ=='bool' or typ.startswith('uint') or typ in ('address','address payable')):continue
        vid=var['id']; row={'declaration':vid,'name':var['name'],'type':typ,'declaration_source':lookup.anchor(var),
            'origin':'conditional_symbolic','encoded':False}
        table[vid]=row; assigns=[]; runtime=False
        for fn in functions:
            is_ctor=fn.get('kind')=='constructor' or fn.get('isConstructor')
            body=fn.get('body') or {}
            for n in walk(body):
                if n.get('nodeType') not in ('Assignment','UnaryOperation'):continue
                lhs=n.get('leftHandSide') or n.get('subExpression') or {}
                if n.get('nodeType')=='UnaryOperation' and n.get('operator') not in ('++','--','delete'):continue
                if not any(x.get('referencedDeclaration')==vid for x in walk(lhs)):continue
                if is_ctor:assigns.append((fn,n))
                else:runtime=True
        if opaque and not var.get('constant'):row['limit']='indirect storage writes not excluded';continue
        if runtime:
            row['origin']='constructor_choice_with_possible_later_write' if assigns else 'conditional_state_with_source_writer'
            row['constructor_sources']=[lookup.anchor(n) for _,n in assigns]
            continue
        v=literal(var.get('value'))
        if var.get('value') is None:v=False if typ=='bool' else 0
        if not assigns:
            if v is not None:row.update(origin='fixed_declared_initializer' if var.get('value') is not None else 'fixed_type_default',value=v,encoded=True)
            continue
        row['origin']='constructor_configuration';row['writes']=[lookup.anchor(n) for _,n in assigns]
        if len(assigns)!=1:continue
        ctor,assignment=assigns[0]
        direct={st.get('expression',{}).get('id') for st in (ctor.get('body') or {}).get('statements',[]) if st.get('nodeType')=='ExpressionStatement'}
        if assignment['id'] not in direct or assignment.get('operator')!='=' or ctor.get('modifiers'):continue
        rhs=assignment.get('rightHandSide') or {}; v=literal(rhs)
        if v is not None:row.update(origin='fixed_constructor_literal',value=v,encoded=True)
        elif rhs.get('memberName')=='sender' and rhs.get('expression',{}).get('name')=='msg':
            row.update(origin='fixed_deployer_address',nonzero=True,encoded=True)
    lookup._relational_initial=table
    return table


def state_facts(lookup, selected_domain=None):
    from .initial_state import domain,initial_for_lookup,CAPABILITY,DEPLOYMENT
    from .state_encoding import _initial_term
    from pr_next_joint.verification.sequence import read
    selected_domain=selected_domain or domain(lookup)
    if selected_domain not in (CAPABILITY,DEPLOYMENT):return _legacy_state_facts(lookup)
    model=initial_for_lookup(lookup)
    if model is None:return {}
    cache=lookup.__dict__.setdefault('_domain_state_facts',{})
    token=(selected_domain,model['identity'])
    if token in cache:return cache[token]
    from .initial_state import family
    context={**model,'_lookup':lookup,'_amount_families':{family(r['cell']) for r in model['candidate_amount_leaves']}}
    table={}
    clean=[p for p in model['constructor_paths'] if p['flow'] in ('normal','returned') and not p.get('issues') and not p.get('evaluation_gaps')]
    for rid,row in model['declarations'].items():
        typ=row['type'];value={'declaration':rid,'name':row['name'],'type':typ,'declaration_source':row['source'],
            'origin':'constructor_configuration' if row['constructor_writes'] or row['explicit_initializer'] else
                     'abstract_initial_scalar' if selected_domain==CAPABILITY and (typ.startswith(('uint','int')) or typ in ('address','address payable')) else 'fixed_type_default',
            'encoded':False,'analysis_domain':selected_domain,'initial_model_identity':model['identity'],
            'runtime_assignment_sites':row['runtime_sites']}
        table[rid]=value
        if row['runtime_sites'] or model['runtime_writers']['opaque_storage_writes']:
            value['origin']='constructor_choice_with_possible_later_write';continue
        if not clean or any(p.get('issues') or p.get('evaluation_gaps') for p in model['constructor_paths']):continue
        cell={'kind':'storage','root':rid,'segments':[]}
        try:values=[_initial_term(read(cell,p['writes'],lookup),context,selected_domain) for p in clean]
        except (ValueError,KeyError,TypeError):continue
        if values and all(v==values[0] for v in values):
            v=values[0]
            if v.get('kind')=='literal' and type(v.get('value')) in (bool,int):value.update(value=v['value'],encoded=True,
                origin='fixed_constructor_or_declaration' if row['constructor_writes'] else 'fixed_type_default')
            elif v.get('initial_identity')=='deployment_caller':value.update(nonzero=True,encoded=True,origin='fixed_deployer_address')
    cache[token]=table
    return table


def encode_state(e,details=None):
    from .initial_state import domain,CAPABILITY,DEPLOYMENT
    if domain(e.lookup) in (CAPABILITY,DEPLOYMENT):
        from .state_encoding import encode
        return encode(e,details)
    items=[];constraints=[]
    for vid,v in state_facts(e.lookup).items():
        if not v['encoded']:continue
        cell=e.expr({'kind':'storage','root':vid,'segments':[]})
        constraints.append(cell!=0 if v.get('nonzero') else cell==v['value'])
        items.append(v)
    return constraints,items


def prestate_receipt(details,initial):
    d=details or {}
    if isinstance(initial,dict):
        return dict(initial,executed_prefix=d.get('prefix',[]),encoded_case=d.get('encoded_case',[]),
            encoded_request_bindings=d.get('encoded_request_bindings',d.get('request_context',{}).get('bindings',[])))
    return {'analysis_domain':'ac_checked_prestate_r1','analysis':'conditional_symbolic_with_checked_fixed_initializers','encoded_invariant_declarations':initial,
            'executed_prefix':d.get('prefix',[]),'encoded_case':d.get('encoded_case',[]),
            'encoded_request_bindings':d.get('encoded_request_bindings',d.get('request_context',{}).get('bindings',[])),
            'explicit_constructor_prefix_executed':False,'author_run_initial_state_verified':False}


def impossible_role(inv,oid):
    """P exclusion only if every clean committing path needs caller == fixed zero."""
    if not inv.backend.complete(oid):return False
    original=inv.backend.paths(oid)
    if not original:return False
    fixed=state_facts(inv.f.lookup(oid))
    from .request_scope import positive_caller_gate
    def zero(g):
        if g.get('op') in ('and','&&'):return any(zero(x) for x in g.get('args',[]))
        return positive_caller_gate(g,inv.f.lookup(oid)) and g.get('op') in ('==','!') and any(
            fixed.get(c['root'],{}).get('encoded') and fixed[c['root']].get('value')==0 for c in selectors(g))
    def value(x):
        if x.get('kind')=='literal':
            a=x.get('value')
            if isinstance(a,bool) or isinstance(a,int):return a
            if str(a).lower() in ('true','false'):return str(a).lower()=='true'
            try:return int(a,0)
            except (ValueError,TypeError):return None
        if x.get('kind')=='storage' and not x.get('segments'):return fixed.get(x.get('root'),{}).get('value')
        op=x.get('op');args=[value(v) for v in x.get('args',[])]
        if op=='!' and len(args)==1 and args[0] is not None:return not args[0]
        if len(args)!=2:return None
        a,b=args
        if op in ('and','&&') and False in args:return False
        if op in ('or','||') and True in args:return True
        if a is None or b is None:return None
        if op=='==':return a==b
        if op=='!=':return a!=b
        if op=='>=':return a>=b
        if op=='<=':return a<=b
        if op=='<':return a<b
        if op=='>':return a>b
        return None
    return all(any(zero(g) or value(g) is False for g in p['guards']) for pid,p in original)


```

## source/src/pr_next_joint/investigation/program.py

原文件SHA256 `552073da5a81930a326cf0da7f01d48dfc823ea400343e5dc700e5804911c96c`

```python
"""M1: original compiler identities, paths and structural edges only.

There is deliberately no import of an old detector, policy projection,
asset discovery, LLM consumer or report merger in this module.
"""
import copy
import hashlib
import time
from pathlib import Path
from pr_next_joint.core import digest, require
from pr_next_joint.frontend.inventory import target_inventory
from pr_next_joint.frontend.source_entry_identity import entry_functions
from pr_next_joint.frontend.program_paths import MechanismPaths
from pr_next_joint.frontend.path_ir import walk, key, clean, ExpressionLimit
from pr_next_joint.frontend.storage import selectors
from pr_next_joint.graph.state_relations import expand_write
from .contracts import ident


class Facts:
    def __init__(self, bundle, native, sources, options, selected=None, description=None):
        self.program_clock_origin = time.monotonic()
        require(all(bundle[k] == native[k] for k in ('program_id', 'build_id')), 'input_identity_mismatch')
        require(bundle.get('native_ir', {}).get('sha256') == digest(native), 'native_digest_mismatch')
        self.bundle, self.native, self.options = bundle, native, options
        self.lookups, self.operations, self.paths, self.writes, self.effects, self.terms = {}, {}, {}, {}, {}, {}
        self.references, self.gaps = {}, []
        inventory = target_inventory(bundle)
        available = {x['file'] + ':' + x['contract'] for x in inventory if x['selected']}
        self.selected = sorted(set(selected) if selected is not None else available)
        require(bool(self.selected) and set(self.selected) <= available, 'invalid_selected_targets')
        source_by_name = {s['file']: s for s in sources}
        for file, ast in bundle['ast_sources'].items():
            require(file in source_by_name, 'source_missing:' + file)
            content = source_by_name[file]['content'].encode('utf-8')
            require(hashlib.sha256(content).hexdigest() == source_by_name[file]['sha256'], 'source_hash_mismatch')
        for contract in bundle['contracts']:
            target = contract['file'] + ':' + contract['name']
            if target not in self.selected:
                continue
            lookup = MechanismPaths(bundle, contract, options.max_paths)
            lookup.analysis_scope = options.scope
            self.lookups[target] = lookup
            bases = lookup.contract_node.get('linearizedBaseContracts', [lookup.contract_node['id']])
            for n in lookup.nodes.values():
                # All references retain the actual compiler node and file span.
                if n.get('nodeType') in ('VariableDeclaration', 'FunctionDefinition', 'Assignment', 'UnaryOperation',
                                         'FunctionCall', 'BinaryOperation', 'IndexAccess', 'MemberAccess', 'IfStatement'):
                    ref = ident('r', [target, n['id']])
                    self.references[ref] = {'target': target, 'ast_id': n['id'], 'kind': n['nodeType'],
                                            'name': n.get('name', n.get('memberName')), 'source': lookup.anchor(n)}
            for entry in entry_functions(lookup):
                fn = entry['signature']; oid = ident('op', [target, fn])
                body = lookup.function(fn)
                operation = {'id': oid, 'target': target, 'function': fn,
                             'source': lookup.anchor(body.get('generated_getter', body)),
                             'parameters': [], 'paths': [], 'gaps': [], 'generated_getter': bool(body.get('generated_getter'))}
                params = body.get('parameters', {}).get('parameters', [])
                for n in params:
                    operation['parameters'].append({'ref': ident('r', [target, n['id']]), 'name': n['name'],
                        'term': self.term({'kind': 'parameter', 'id': n['id'], 'type': n['typeDescriptions']['typeString']}, target)})
                self.operations[oid] = operation
                try:
                    if time.monotonic()-self.program_clock_origin >= options.seconds:
                        self.gap(oid, 'path_extraction', 'program_time_before_entry')
                        continue
                    paths = lookup.run(fn)
                except ExpressionLimit as error:
                    self.gap(oid,'source_expression_limit',str(error))
                    continue
                except (TypeError, AttributeError):
                    raise
                except Exception as error:
                    self.gap(oid, 'path_extraction', type(error).__name__ + ':' + str(error)); continue
                for index, path in enumerate(paths):
                    pid = ident('path', [oid, index]); path = copy.deepcopy(path)
                    try:
                        path['writes'] = [item for w in path['writes'] for item in expand_write(w, lookup)]
                        # Validate each executable operand independently before publishing
                        # any references. A bounded path cannot poison a sibling path.
                        for expr in [*path['guards'], *(w['path'] for w in path['writes']),
                                     *(w['value'] for w in path['writes']), *path.get('evaluated_terms', []),
                                     path.get('return_value'), *path.get('sensitive_effects', [])]:
                            if expr is not None: clean(expr)
                    except ExpressionLimit as error:
                        self.gap(oid,'source_expression_limit',{'path':pid,'reason':str(error)})
                        continue
                    except (TypeError, AttributeError):
                        raise
                    except Exception as error:
                        path.setdefault('issues', []).append({'reason': 'write_expansion:' + str(error)})
                    self.paths[pid] = {'operation': oid, 'index': index, 'raw': path}
                    card = {'id': pid, 'flow': path['flow'], 'guards': [], 'writes': [], 'effects': [],
                            'issues': copy.deepcopy(path.get('issues', [])), 'evaluation_gaps': path.get('evaluation_gaps', [])}
                    for g in path['guards']:
                        card['guards'].append(self.term(g, target))
                    for wi, w in enumerate(path['writes']):
                        wid = ident('w', [pid, wi]); self.writes[wid] = {'operation': oid, 'path': pid, 'raw': w}
                        card['writes'].append({'id': wid, 'selector': self.term(w['path'], target),
                                              'value': self.term(w['value'], target), 'source': w['source']})
                    for ei, e in enumerate(path.get('sensitive_effects', [])):
                        eid = ident('fx', [pid, ei]); self.effects[eid] = {'operation': oid, 'path': pid, 'raw': e}
                        row = {'id': eid, 'kind': e['kind'], 'source': e['source']}
                        for field in ('recipient', 'amount', 'success'):
                            if e.get(field) is not None: row[field] = self.term(e[field], target)
                        card['effects'].append(row)
                    for value in [path.get('evaluated_terms', []), path.get('return_value')]:
                        for n in walk(value):
                            if n.get('kind'): self.term(n, target)
                    operation['paths'].append(card)
                    if card['issues'] or card['evaluation_gaps']:
                        self.gap(oid, 'program_path', {'path': pid, 'issues': card['issues'], 'evaluation_gaps': card['evaluation_gaps']})
        for target in self.selected:
            self.lookups[target]._investigation_facts=self
            self.term({'kind': 'actual_sender'}, target)
            self.term({'kind': 'transaction_value', 'type': 'uint256'}, target)
        edges = []
        reads={o['id']:{s['root'] for p in o['paths'] for s in selectors(self.paths[p['id']]['raw'])}
               for o in self.operations.values()}
        writes={}
        for w in self.writes.values():
            writes.setdefault(w['operation'],set()).add(w['raw']['path']['root'])
        for a in self.operations.values():
            a_roots=writes.get(a['id'],set())
            if not a_roots:continue
            for b in self.operations.values():
                if a['target'] != b['target']: continue
                b_roots=reads[b['id']]
                roots = sorted(a_roots & b_roots)
                if roots:
                    edges.append({'from': a['id'], 'to': b['id'], 'roots': roots, 'kind': 'may_write_read',
                                  'meaning': 'structural_frontier_not_policy'})
        package = Path(__file__).resolve().parents[1]
        implementation = {p.relative_to(package).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(package.rglob('*.py'))}
        self.context = {'schema': 'scrv-facts-r2-1', 'identity': {k: bundle[k] for k in ('program_id', 'build_id')},
                        'implementation_sha256': digest(implementation), 'finite_options': options.record(),
                        'scope': options.scope, 'sources': sources, 'description': description,
                        'operations': list(self.operations.values()), 'references': self.references,
                        'terms': self.terms, 'frontier': edges, 'program_gaps': self.gaps}
        from .initial_state import model, domain
        self.context['state_analysis']={target:{'analysis_domain':domain(lookup),'initial_model_identity':model(self,target)['identity'],
            'candidate_amount_leaves':model(self,target)['candidate_amount_leaves']} for target,lookup in self.lookups.items()}
        from .summary import get_summaries
        self.summaries=get_summaries(self)
        self.link_unexpanded_effects()
        from .call_summary import CallSummaries
        self.call_summaries = CallSummaries(self)
        self.context['call_summary_identity'] = self.call_summaries.identity
        self.context['effect_summary_identity']=self.summaries.identity
        from .candidates import source_candidates
        self.source_candidates=source_candidates(self)
        self.context['source_candidates']=self.source_candidates
        self.identity = digest(self.context)

    def link_unexpanded_effects(self):
        """Track unavailable storage dependencies without discarding unrelated readers."""
        limited=[g for g in self.gaps if g['kind']=='source_expression_limit']
        for gap in limited:
            entry=self.operations[gap['operation']];lk=self.lookup(entry['id'])
            body=lk.function(entry['function']);pending=[body];seen=set();writes=set();opaque=False
            while pending:
                fn=pending.pop()
                if fn.get('id') in seen:continue
                seen.add(fn.get('id'))
                for n in walk([fn.get('body'),fn.get('modifiers',[])]):
                    if n.get('nodeType') in ('InlineAssembly','YulFunctionCall'):opaque=True
                    if n.get('nodeType') in ('FunctionCall','ModifierInvocation'):
                        expr=n.get('expression',n.get('modifierName',{}))
                        callee=lk.nodes.get(expr.get('referencedDeclaration'),{})
                        if callee.get('body'):pending.append(callee)
                        if expr.get('memberName')=='delegatecall':opaque=True
                    if n.get('nodeType') not in ('Assignment','UnaryOperation'):continue
                    lhs=n.get('leftHandSide',n.get('subExpression',{}))
                    writes.update(v.get('referencedDeclaration') for v in walk(lhs)
                                  if lk.nodes.get(v.get('referencedDeclaration'),{}).get('stateVariable'))
            if body.get('kind')=='constructor':
                raise ExpressionLimit('shared_or_entire_entry_source_expression_unavailable')
            for other in self.operations.values():
                if other['id']==entry['id'] or other['target']!=entry['target'] or other['generated_getter']:continue
                local=gap.get('reason')
                if isinstance(local,dict) and 'declaration' in local:
                    writes={local['declaration']};opaque=False
                reads={s['root'] for card in other['paths'] for s in selectors(self.paths[card['id']]['raw'])}
                if opaque or reads & writes:
                    self.gap(other['id'],'dependent_source_expression_limit',
                             {'source_operation':entry['id'],'scope':'unknown_storage' if opaque else 'shared_declaration'})
        for target in {self.operations[g['operation']]['target'] for g in limited}:
            def usable_scope(operation):
                if operation['target']!=target or operation['generated_getter']:return False
                gaps=[g for g in operation['gaps'] if g['kind']=='source_expression_limit']
                if any(g['kind']=='dependent_source_expression_limit' for g in operation['gaps']):return False
                for card in operation['paths']:
                    here=[g['reason'] for g in gaps if not isinstance(g['reason'],dict) or g['reason'].get('path')==card['id']]
                    if not here:return True
                    # A final-value failure can be isolated from a distinct write in the same path.
                    if all(isinstance(x,dict) and 'declaration' in x for x in here):
                        affected={x['declaration'] for x in here}
                        if any(self.writes[w['id']]['raw']['path']['root'] not in affected for w in card['writes']):return True
                return False
            if not any(usable_scope(op) for op in self.operations.values()):
                raise ExpressionLimit('shared_or_entire_entry_source_expression_unavailable')
    def term(self, value, target):
        ref = ident('e', [target, value])
        self.terms[ref] = {'target': target, 'expression': copy.deepcopy(value)}
        for n in walk(value):
            if n is not value and n.get('kind'):
                nr = ident('e', [target, n]); self.terms[nr] = {'target': target, 'expression': copy.deepcopy(n)}
        return ref

    def gap(self, operation, kind, reason):
        row = {'operation': operation, 'kind': kind, 'reason': reason}
        self.gaps.append(row); self.operations[operation]['gaps'].append(row)

    def operation_paths(self, oid, complete_only=False):
        for card in self.operations[oid]['paths']:
            item = self.paths[card['id']]
            p = item['raw']
            if complete_only and (p['flow'] not in ('normal', 'returned') or p.get('issues') or p.get('evaluation_gaps')):
                continue
            yield card['id'], p

    def lookup(self, oid):
        return self.lookups[self.operations[oid]['target']]

```

## source/src/pr_next_joint/investigation/properties.py

原文件SHA256 `cdfff0890436cc5b493a8e3b23f72fe1447b6e416f33d9b711dec2c2a08dc0dd`

```python
"""Finite, source-bound questions. Wording guides investigation, never certifies harm."""
import re
from itertools import product

from pr_next_joint.frontend.path_ir import key, walk
from pr_next_joint.frontend.storage import keys, selectors, selector_relation, value_type
from .request_scope import claim_entries, holder_effect, linked_controls, unique_cells
from .ledger import MEASURES, bind_positions, movements
from .roles import path_qualification


def words(item):
    return ' '.join(str(item.get(k) or '') for k in ('claim','distinguish','distinguishing_question','observation'))


def interpret(item):
    raw = item.get('observation')
    req = dict(raw) if isinstance(raw,dict) else {}
    text = words(item)
    if re.search(r'\b(?:never check|does not (?:read|check)|bypass(?:es)?|missing (?:the )?control)\b',text,re.I) and re.search(r'freez|frozen|guard|control',text,re.I):
        return {**req,'measure':'missing_control'}
    if req.get('measure') in MEASURES or req.get('measure') in ('denied_qualified','direct_effect','authorization_violation'):
        return req
    if req.get('measure') and req['measure'] not in ('opens','blocks'):
        return req
    if re.search(r'allowance.{0,55}(?:gross|actual debit|less than)|more than (?:the |was )?(?:allowance|approved)|(?:gross|actual) debit.{0,70}(?:allowance|grant)',text,re.I):
        return {**req,'measure':'ledger_grant'}
    if re.search(r'(?:recipient|payee|receiver).{0,55}(?:less|zero|smaller|short)|(?:lower|reduced) (?:recipient )?credit|到账减少',text,re.I):
        return {**req,'measure':'ledger_receipt'}
    if re.search(r'(?:debited|debit|charged).{0,22}(?:more|greater|extra)|greater gross debit',text,re.I):
        return {**req,'measure':'ledger_debit'}
    if req.get('measure'):
        return req
    if item.get('category')=='AC' and re.search(r'(?:qualified|entitled|authorized|rightful|rightfully).{0,65}(?:reject|denied|refus)|wrongful.{0,18}(?:denial|reject)',text,re.I):
        return {**req,'measure':'denied_qualified'}
    if item.get('category') in ('FCR-MINT','FCR-TRANSFER','FCR-DESTROY') and re.search(r'\b(mint|issuance|confiscate|seize|destroy|burn|debit|transfer|issu(?:e|es))\b',text,re.I):
        return {**req,'measure':'direct_effect'}
    if item.get('category') in ('FCR-FREEZE','FCR-PAUSE') and re.search(r'block|revert|pause|freeze',text,re.I):
        return {**req,'measure':'blocks'}
    if item.get('category')=='AC' and re.search(r'(?:install|forge|acquire|grant itself).{0,36}(?:grant|allowance|permission)',text,re.I):
        return {**req,'measure':'holder_grant'}
    return None


def conflicting_measurements(inv,q,proposal):
    """Only explicit factual negations of the same measured positive condition conflict."""
    from .request_scope import observation_applies
    factual={
        'ledger_receipt':r'\b(?:recipient|payee)\b.{0,28}\b(?:always|necessarily)\b.{0,20}\b(?:full|unchanged)',
        'ledger_debit':r'\b(?:gross|actual) debit (?:never increases|is always unchanged)',
        'ledger_grant':r'\b(?:actual|gross) debit (?:never exceeds|is always within) (?:the )?(?:allowance|grant)',
        'denied_qualified':r'\b(?:qualified|authorized) (?:caller|role|manager) (?:is never (?:rejected|denied)|always succeeds)',
    }
    if any(proposal.get(k)!=q['current'].get(k) for k in ('observation','assumptions','next_check','actor','object','phase')):
        return []
    text=proposal.get('claim','')
    return [o['probe'] for row in q.get('observations',[]) if row['measure'] in factual and row['version']==q['version']
            and observation_applies(inv,q,row) and re.search(factual[row['measure']],text,re.I)
            for o in row['outcomes'] if o['predicate_value']]


def source_target(inv,anchor,target):
    return [o for o in inv.catalog.resolve(anchor) if inv.f.operations[o]['target']==target]


def premise_cases(inv, use, item, changed=()):
    """Separate expressly different values of the same declared cell. No free Boolean substitute."""
    lookup = inv.f.lookup(use)
    cells = unique_cells(s for s in inv.graph.request_reads(use) if not keys(s))
    text = words(item)
    axes, gaps = [], []
    for cell in cells:
        name = lookup.nodes.get(cell['root'],{}).get('name')
        if not name:
            continue
        regex=r'(?<![\w$])'+re.escape(name)+r'\s*(?:==|=)\s*(true|false|\d+)\b'
        values=list(dict.fromkeys(v.lower() for v in re.findall(regex,text,re.I)))
        if not values:
            continue
        if len({s['root'] for s in cells if lookup.nodes.get(s['root'],{}).get('name')==name})!=1:
            gaps.append('ambiguous source declaration '+name);continue
        typ=value_type(cell,lookup)
        if any((v in ('true','false')) != (typ=='bool') or typ!='bool' and not typ.startswith('uint') for v in values):
            gaps.append('literal sort unsupported: '+name);continue
        at='after' if any(selector_relation(cell,c)=='same_shape' for c in changed) else 'before'
        axes.append([{'cell':cell,'source_name':name,'value':v=='true' if typ=='bool' else int(v),'frame':at} for v in values])
    fixed=[]
    assumptions=item.get('assumptions',[])
    if isinstance(assumptions,str):assumptions=[assumptions]
    named=unique_cells(inv.graph.request_reads(use))
    for a in assumptions:
        match=re.fullmatch(r'(before|after)\s+([A-Za-z_$][\w$]*(?:\[[\w$.]+\])*)\s*(?:==|=)\s*(\d+|true|false)',str(a).strip(),re.I)
        if not match:continue
        at,name,value=match.groups(); found=[s for s in named if inv.backend._storage_name(use,s)==name]
        if len(found)!=1:gaps.append('unbound scoped premise '+name);continue
        fixed.append({'cell':found[0],'source_name':name,'frame':at.lower(),'value':value.lower()=='true' if value.lower() in ('true','false') else int(value)})
    if len(axes)>3 or len(axes)>1 and any(len(axis)>1 for axis in axes):
        return [],gaps+['multiple alternative clauses cannot be independently cross-multiplied']
    return [fixed+list(c) for c in product(*axes)] if axes else [fixed],gaps


def privileged_paths(inv,oid):
    return [pid for pid,p in inv.backend.paths(oid) if path_qualification(inv.f,oid,p)]


def stage(inv,use):
    facts=inv.f; target=facts.operations[use]['target']
    listed=[]
    for cell in unique_cells(inv.graph.request_reads(use)):
        if keys(cell) or not (value_type(cell,facts.lookup(use)) or '').startswith(('uint','bool')):
            continue
        writers=[]
        for oid in sorted(inv.graph.access[target,cell['root']]['writers']):
            matches=[pid for pid,p in inv.backend.paths(oid) if any(selector_relation(cell,w['path'])=='same_shape' for w in p['writes'])]
            if matches:
                writers.append({'operation':oid,'paths':matches,'role_guarded_paths':privileged_paths(inv,oid)})
        listed.append({'cell':cell,'name':inv.backend._storage_name(use,cell),'runtime_writers':writers})
    return listed


def source_graph_holes(inv,binding,item):
    root=binding['core_operation']; target=inv.f.operations[root]['target']
    claimed=claim_entries(inv,binding,item)
    controls=unique_cells(w['path'] for _,p in inv.backend.paths(root) for w in p['writes'] if value_type(w['path'],inv.f.lookup(root))=='bool')
    if not controls:
        return []
    related=[]
    for oid in sorted(claimed-{root}):
        ops=[(pid,movements(inv.backend,oid,p)) for pid,p in inv.backend.paths(oid)]
        debit=unique_cells(c for pid,m in ops for c in m['-'])
        if not debit:
            continue
        peers=[]
        for other,entry in inv.f.operations.items():
            if entry['target']!=target or other==oid:continue
            linked=linked_controls(inv,root,other)
            if not any(selector_relation(c,l)=='same_shape' for c in controls for l in linked):continue
            for pid,p in inv.backend.paths(other):
                m=movements(inv.backend,other,p)
                if any(selector_relation(a,b)=='same_shape' for a in debit for b in m['-']):
                    peers.append({'operation':other,'path':pid,'controls':linked})
        reads=linked_controls(inv,root,oid)
        related.append({'use':oid,'debit_positions':debit,'control_reads':reads,'control_writers':controls,'peer_controlled_uses':peers})
    return related


def plan_property(inv,binding,item,plan,req):
    """Select finite typed questions with compiler-resolved endpoints, or disclose a local gap."""
    measure=req['measure']; root=binding['core_operation']; target=inv.f.operations[root]['target']
    entries=claim_entries(inv,binding,item); contexts=[]
    if measure in MEASURES:
        uses=[oid for oid in sorted(entries) if holder_effect(inv,oid)]
        if req.get('at'):uses=[o for o in source_target(inv,req['at'],target) if o in entries]
        elif root in uses and bind_positions(inv.backend,root,item)[0]:uses=[root]
        reasons=[]
        for use in uses:
            pos,err=bind_positions(inv.backend,use,item)
            if err:reasons.append(err);continue
            edges=stage(inv,use)
            forced=source_target(inv,req.get('after'),target) if req.get('after') else []
            if req.get('after') and len(forced)!=1:reasons.append('requested_intervention_not_unique');continue
            choices={}
            for edge in edges:
                if req.get('control') and req['control']!=edge['name']:continue
                for w in edge['runtime_writers']:
                    change=w['operation']
                    if forced and change not in forced or not forced and root!=use and change!=root:continue
                    if not w['role_guarded_paths']:continue
                    choices.setdefault(change,[]).append(edge['cell'])
            if not choices:reasons.append('no_source_bound_runtime_privileged_writer');continue
            for change,controls in choices.items():
                ctx=inv._compare_context({'current':item},change,use)
                ctx['observable']={'measure':measure,'ledger':pos,'control_selectors':controls,
                                   'change_paths':privileged_paths(inv,change)}
                cases,gaps=premise_cases(inv,use,item,controls)
                if gaps:reasons+=gaps;continue
                ctx['premise_cases']=cases
                # An address alias is admitted only for two actual source parameter names.
                params=inv.f.lookup(use).function(inv.f.operations[use]['function']).get('parameters',{}).get('parameters',[])
                addr={p['name']:{'kind':'parameter','id':p['id'],'type':p['typeDescriptions']['typeString']} for p in params if p['typeDescriptions']['typeString'] in ('address','address payable')}
                ctx['request_aliases']=[]
                for a,op,b in re.findall(r'\b(\w+)\s*(==|!=)\s*(\w+)\b',str(item.get('assumptions',[]))):
                    if a in addr and b in addr:ctx['request_aliases'].append([addr[a],addr[b],op])
                contexts.append((change,use,ctx))
        reason=','.join(dict.fromkeys(reasons)) or 'more_than_one_applicable_request_or_intervention'
    elif measure=='missing_control':
        rows=source_graph_holes(inv,binding,item)
        relevant=[r for r in rows if r['peer_controlled_uses'] and not r['control_reads']]
        if relevant:
            contexts=[(root,relevant[0]['use'],{'observable':{'measure':measure,'alternatives':relevant},'operation':root,
                      'checked_uses':[r['use'] for r in relevant],'frame_type':'committed_intervention_then_actual_alternative'})]
        reason='no_same_target_same_right_comparator_or_unresolved_control'
    else:
        ctx=inv._compare_context({'current':item},root,root)
        ctx.update({'observable':{'measure':measure,'claim':item.get('claim',''),'category':item.get('category')},
                    'operation':root,'stage':stage(inv,root),'frame_type':'single_original_entry'})
        if req.get('authorization'):ctx['observable']['authorization']=req['authorization']
        if measure=='direct_effect' and ctx.get('bindings'):
            ctx['exploratory_request_bindings_not_the_claim']=ctx.pop('bindings')
        params=inv.f.lookup(root).function(inv.f.operations[root]['function']).get('parameters',{}).get('parameters',[])
        addr={p['name']:{'kind':'parameter','id':p['id'],'type':p['typeDescriptions']['typeString']} for p in params if p['typeDescriptions']['typeString'] in ('address','address payable')}
        ctx['request_aliases']=[[addr[a],addr[b],op] for a,op,b in re.findall(r'\b(\w+)\s*(==|!=)\s*(\w+)\b',str(item.get('assumptions',[]))) if a in addr and b in addr]
        contexts=[(root,root,ctx)]
        if measure=='direct_effect':
            contexts[0][2]['privileged_paths']=privileged_paths(inv,root)
        reason='unresolved_direct_property'
    pick=None
    if len(contexts)==1:
        change,use,ctx=contexts[0]
        pick={'action':'compare','change':change,'observe':use,'measure':measure,'status':'source_bound',
              'expectations':{},'context':ctx,'scope':{'target':target,'finding_root':root,'use':use,'intervention':change,
                  'measure':measure,'controls':ctx['observable'].get('control_selectors',[]),'objects':[ctx['observable']['ledger'][k] for k in ('debit','credit')] if 'ledger' in ctx['observable'] else [],
                  'checked_uses':ctx.get('checked_uses',[use]),'frame_type':ctx.get('frame_type','same_request_two_worlds'),
                  'extent':'compiler-selected entries, ordered keys and recorded path conditions only'}}
    inherited_pairs=list(plan.get('selected_pairs',[]))
    plan['observation_choice']={'ordinary_pairs':inherited_pairs,'selected':pick,'pool':[pick] if pick else [],'status':'selected_property' if pick else 'unsupported',
        'reason':'source-resolved finite property' if pick else reason,'property_requested':measure,'claim_text':item['claim'],'possible_compilations':len(contexts),
        'stage_evidence':stage(inv,root),'request_resolution':{'finding_root':root,'use':pick['observe'] if pick else None,
        'possible_uses':sorted(entries),'unmeasured_uses':sorted(entries-{pick['observe'],pick['change']}) if pick else sorted(entries)}}
    if pick:
        plan['selected_pairs']=[{'change':pick['change'],'observe':pick['observe'],'source_reason':'typed property and matching applied target'}]
    inv.graph.events.append({'action':'compile_source_property','measure':measure,'root':root,'selected':bool(pick),'reason':plan['observation_choice']['reason']})


```
