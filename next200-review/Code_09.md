# 源码文本 · 9

## source/src/pr_next_joint/investigation/comparison.py

原文件 SHA-256 `29c22b84815fb2bd07375d0f82b8d65fb25d47a8d5bc42458f2bac307a2f5070`

````python
"""Map an already nominated finding to one JANUS capability; never generate a candidate."""
import re
from pr_next_joint.frontend.path_ir import key,walk
from pr_next_joint.frontend.storage import keys,selectors,selector_relation,value_type
from .ledger import movements,grant_for,unit_origin
from .properties import privileged_paths
from .prestate import impossible_role,state_facts
from .request_scope import claim_entries,linked_controls
from .roles import path_qualification
from .summary import holder as bound_holder


GUIDANCE = """FCR blind reading: consider all five conditional capabilities. Unassigned typed address/number inputs may vary under the host state model; explicit initialization, constructors and committed transitions remain binding. Conditional capability does not assert deployment reachability. TRANSFER: privilege can move tokens of another holder without the applicable holder approval. A public use may depend on a privileged upstream change. MINT: a privileged actor can issue tokens to itself or a beneficiary it can control; no other holder debit, user request or price loss is needed. DESTROY: privilege destroys another holder's tokens; distinguish self-burn or actual matching settlement. FREEZE: control can stop outgoing token transfers of a designated holder. PAUSE: common control can stop all ordinary holders transferring tokens; one address, amount, deposit or log failure is insufficient. Administrative purpose, compliance, airdrop, or a cap alone do not negate a capability. Check any claimed consent or compensation against this holder, asset, amount, path and phase. Keep other source-backed financial/business risks as additional, describe the affected use. Keep constructor configuration and runtime power distinct. A pointed transfer, mint, burn or restriction need not be named like those operations."""


def same(a,b):
    return selector_relation(a,b)=='same_shape'


def transfer_shapes(b,oid,path):
    moves=movements(b,oid,path)
    return [(d,c) for d in moves['-'] for c in moves['+'] if same(d,c) and key(keys(d))!=key(keys(c))]


def ledger_routes(b,target):
    if not hasattr(b,'_comparison_routes'):b._comparison_routes={}
    sem=getattr(b,'semantics',None)
    token=(target,sem.dependency_identity([o for o,e in b.f.operations.items() if e['target']==target]) if sem else 0)
    if token in b._comparison_routes:return b._comparison_routes[token]
    routes=[]
    for oid,op in b.f.operations.items():
        if op['target']!=target:continue
        for pid,path in b.paths(oid):
            for debit,credit in transfer_shapes(b,oid,path):
                # The two address-bound entries must have an independently grounded
                # financial use or match the actual standard token transfer interface.
                funded=unit_origin(b,oid,debit)
                abi=op['function'] in ('transfer(address,uint256)','transferFrom(address,address,uint256)')
                if funded or abi:
                    routes.append({'operation':oid,'path':pid,'debit':debit,'credit':credit,'grounding':funded or 'standard_ABI_and_matching_ledger_effect'})
    b._comparison_routes[token]=routes
    return routes


def gates(path,cell):
    """Necessary Boolean controls and conditional alternatives of other global Booleans."""
    def includes(term):
        if term.get('kind')=='storage':return key(term)==key(cell)
        op=term.get('op');args=term.get('args',[])
        if op=='!' and len(args)==1:
            if args[0].get('op') in ('and','&&'):return False
            return includes(args[0])
        if op in ('and','&&'):return any(includes(x) for x in args)
        if op in ('or','||'):
            return any(includes(x) for x in args) and all(includes(x) or
                x.get('kind')=='storage' and not keys(x) for x in args)
        if op in ('==','!=','<','<=','>','>='):return any(key(s)==key(cell) for s in selectors(term))
        return False
    return any(includes(g) for g in path['guards'])


def can_restrict(b,change,use,p,cell):
    """Check the polarity of the control on this actual outgoing route."""
    def blocked_value(g):
        if key(g)==key(cell):return False
        if g.get('op')=='!' and len(g.get('args',[]))==1:
            inner=blocked_value(g['args'][0])
            return None if inner is None else not inner
        if g.get('op') in ('and','&&','or','||'):
            choices={v for child in g.get('args',[]) for v in [blocked_value(child)] if v is not None}
            if len(choices)==1:return choices.pop()
        return None
    needs={v for g in p['guards'] for v in [blocked_value(g)] if v is not None}
    if len(needs)!=1:return False
    needed=needs.pop()
    for _,cp in b.paths(change):
        guards=cp['guards']
        if not path_qualification(b.f,change,cp):continue
        for w in cp['writes']:
            if not same(cell,w['path']):continue
            term=w['value']
            if term.get('kind')=='literal' and str(term.get('value')).lower()==str(needed).lower():return True
            if term.get('kind')=='parameter' and term.get('type')=='bool':
                if not any(key(term)==key(n) for g in guards for n in walk(g)):return True
    return False


def business_only(item):
    text=item.get('claim','')+' '+str(item.get('revision_reason',''))
    purpose=re.search(r'\b(?:maintenance|emergency|compliance|sanctioned|airdrop|administrative purpose|legitimate admin|incident response)\b',text,re.I)
    return bool(purpose)


def literal_balance_zero(p,lookup):
    return [w['path'] for w in p['writes'] if len(keys(w['path']))==1 and value_type(w['path'],lookup).startswith('uint')
            and w['value'].get('kind')=='literal' and str(w['value'].get('value'))=='0']


def conjuncts(g):
    if g.get('op') in ('and','&&'):
        for a in g['args']:yield from conjuncts(a)
    else:yield g


def holder_only(b,oid,p,debit):
    holder=bound_holder(debit,b.f.lookup(oid))
    if holder is None:return False
    if holder.get('kind')=='actual_sender':return True
    return any(g.get('op')=='==' and {key(a) for a in g.get('args',[])}=={key(holder),key({'kind':'actual_sender'})}
               for guard in p['guards'] for g in conjuncts(guard))


def consent_gate(b,oid,p,debit):
    holder=bound_holder(debit,b.f.lookup(oid))
    if holder is None:return False
    # Only a positive holder -> requester grant on the actual committing path,
    # for which the holder controls issuance. A controller's own permission is distinct.
    for raw in p['guards']:
        for g in conjuncts(raw):
            if g.get('kind')!='storage' or value_type(g,b.f.lookup(oid))!='bool':continue
            pos=keys(g)
            if len(pos)!=2 or key(pos[0])!=key(holder) or pos[1].get('kind')!='actual_sender':continue
            writers=[w for w in b.f.writes.values() if b.f.operations[w['operation']]['target']==b.f.operations[oid]['target'] and same(g,w['raw']['path'])]
            if writers and all(keys(w['raw']['path'])[0].get('kind')=='actual_sender' for w in writers):return True
    return allowance_covers(b,oid,p,debit)


def allowance_covers(b,oid,p,debit):
    grant=grant_for(b,oid,p,debit)
    if grant is None:return False
    writes=[w for w in p['writes'] if key(w['path'])==key(debit)]
    if len(writes)!=1:return False
    expr=writes[0]['value'];args=expr.get('args',[])
    if expr.get('op')!='-' or len(args)!=2 or key(args[0])!=key(debit):return False
    # A grant also installable by an outsider/controller does not certify holder consent.
    for w in b.f.writes.values():
        other=w['operation']; dst=w['raw']['path']
        if b.f.operations[other]['target']!=b.f.operations[oid]['target'] or not same(dst,grant):continue
        if keys(dst)[0].get('kind')=='actual_sender':continue
        val=w['raw']['value'];gargs=val.get('args',[])
        if val.get('op')=='-' and gargs and key(gargs[0])==key(dst):continue
        return False
    return any(n.get('op')=='>=' and len(n.get('args',[]))==2 and key(n['args'][0])==key(grant) and key(n['args'][1])==key(args[1])
               for guard in p['guards'] for n in [guard,*([*guard.get('args',[])] if guard.get('op') in ('and','&&') else [])])


def _direct_results(inv,root,category,q=None):
    """Match actual original-program queries, not a label, issue ID or raw UNSAT."""
    target=inv.f.operations[root]['target']
    from .initial_state import domain, initial_for_lookup
    selected_domain=domain(inv.f.lookup(root)); initial=initial_for_lookup(inv.f.lookup(root))
    predicate='positive_credit_to_caller' if category=='FCR-MINT' else 'negative_delta_of_other_nonzero_holder'
    results={}
    for evidence_id,record in inv.evidence.items():
        if q is not None and evidence_id not in q['evidence']:continue
        if record.get('observed_measure')!='direct_effect' or (record.get('change'),record.get('observe'))!=(root,root):continue
        qs={x['id']:x for x in record.get('queries',[])}
        for row in record.get('property_measurements',[]):
            base=qs.get(row.get('feasible_probe'),{});effect=qs.get(row.get('result_probe'),{})
            d=base.get('details',{}); pid=d.get('use_path'); cell=d.get('ledger')
            if (base.get('label')!='local_premises_feasible' or base.get('abstract_hash') or
                    d.get('target')!=target or d.get('operation')!=root or d.get('category_hypothesis')!=category or
                    d.get('predicate')!=predicate or d.get('argument_domain') not in ('all_source_inputs_on_this_committing_path','recorded_claim_aliases') or
                    pid not in inv.f.paths or inv.f.paths[pid]['operation']!=root or not cell or not d.get('unit')):continue
            if d.get('argument_domain')=='recorded_claim_aliases':
                ctx=((q or {}).get('plan',{}).get('observation_choice',{}).get('selected') or {}).get('context',{})
                if not ctx.get('request_aliases') or key(d.get('claim_aliases'))!=key(ctx['request_aliases']):continue
            state=d.get('prestate',{})
            if (state.get('analysis_domain')!=selected_domain or
                    state.get('initial_model_identity')!=(initial or {}).get('identity') or
                    state.get('executed_prefix') or state.get('encoded_case') or state.get('encoded_request_bindings')):continue
            if not effect and base.get('answer')=='unsat':
                tested=base;value=False;kind='source_path_infeasible_in_this_domain'
            elif (base.get('validated_bounded_witness') and effect.get('label')=='direct_effect'
                    and {k:v for k,v in effect.get('details',{}).items() if k!='prestate'}=={k:v for k,v in d.items() if k!='prestate'}
                    and effect.get('details',{}).get('prestate',{}).get('analysis_domain')==selected_domain
                    and effect.get('details',{}).get('prestate',{}).get('initial_model_identity')==(initial or {}).get('identity')
                    and not effect.get('abstract_hash')):
                if effect.get('answer')=='unsat':value=False
                elif effect.get('validated_bounded_witness'):value=True
                else:continue
                tested=effect;kind='effect_on_feasible_source_path'
            else:continue
            # Bounded prefix exhaustion does not exclude an unexamined later stage.
            tested_state=tested.get('details',{}).get('prestate',{})
            bounded_exclusion=value is False and not (tested_state.get('global_reachability_exhausted') or tested.get('exclusion_certificate',{}).get('excludes_only_this_formula'))
            position=(pid,key(cell))
            results[position]={'result':value,'kind':kind,'evidence':evidence_id,'probe':tested['id'],'feasibility_probe':base['id'],
                'formula':tested['formula_ref'],'target':target,'operation':root,'path':pid,'position':cell,'predicate':predicate,
                'actor_scope':'beneficiary_equals_caller' if category=='FCR-MINT' else 'debit_other_nonzero_holder',
                'argument_domain':d['argument_domain'],'prestate':tested_state,'bounded_exclusion_only':bounded_exclusion,
                'observed_values':effect.get('observed_values',{}),'exclusion_certificate':tested.get('exclusion_certificate')}
    return results


def _all_direct_effects_excluded(b,root,category,excluded):
    """Conservative completeness check for this source claim, never for other entries or classes."""
    if not excluded or any(x.get('bounded_exclusion_only') for x in excluded) or not b.complete(root):return False
    covered={(x['path'],key(x['position'])) for x in excluded}
    for pid,path in b.paths(root):
        if path.get('sensitive_effects'):return False
        for w in path['writes']:
            s=w['path']
            if not keys(s):continue
            if not value_type(s,b.f.lookup(root)).startswith('uint') or (pid,key(s)) not in covered:return False
            # A self-credit check does not exclude a different, controlled third-party beneficiary.
            if category=='FCR-MINT' and (bound_holder(s,b.f.lookup(root)) or {}).get('kind')!='actual_sender':return False
    return True


def alignment(inv,q,scope):
    b=inv.backend;f=inv.f;i=q['current'];root=inv.root(q);cat=i.get('category')
    result={'definition_reference':'JANUS v2 II-B','nominated_category':cat,'status':'unresolved','conditions':[],
            'prestate_alignment':'authors_per_member_initial_state_not_verified','source_basis':[],
            'normative_hypothesis':i['claim'],'scope':'specified actual targets and routes',
            'constructor_path_executed':False,'candidate_generated_here':False}
    def end(status,reason):
        result.update(status=status,reason=reason)
        return result
    if not root:return end('unresolved','applied_target_unresolved')
    from .initial_state import domain, initial_for_lookup
    state_model=initial_for_lookup(f.lookup(root))
    result['analysis_domain']=domain(f.lookup(root))
    result['initial_model_identity']=(state_model or {}).get('identity')
    result['deployment_reachability']='not_separately_established'
    result['conditional_state_assumptions']=[{'declaration':v['declaration'],'origin':v['origin']} for v in state_facts(f.lookup(root)).values() if v.get('origin')=='abstract_initial_scalar']
    target=f.operations[root]['target'];entries=claim_entries(inv,q['binding'],i)
    choice=q.get('plan',{}).get('observation_choice') or {}
    pick=choice.get('selected') or {}
    if pick:entries.update((pick['change'],pick['observe']))
    hint=i.get('next_check') or {}
    if isinstance(hint,dict) and hint.get('action')=='compare':
        for field in ('change','observe'):
            ids=[o for o in inv.catalog.resolve(hint.get(field)) if f.operations[o]['target']==target]
            if len(ids)==1 and (ids[0] in entries or linked_controls(inv,root,ids[0])):entries.update(ids)
    routes=ledger_routes(b,target); controls=[]
    result['prestate_sources']={v['name']:v['origin'] for v in state_facts(f.lookup(root)).values() if
        any(c['root']==v['declaration'] for o in entries for c in inv.graph.request_reads(o))}
    if not routes:result['asset_scope_limit']='no source-resolved transferable ledger route in compiled scope'
    if any(inv.evidence[e].get('operation')==root and inv.evidence[e].get('no_committing_path') for e in q['evidence']):
        return end('refuted','original_source_has_no_committing_path_for_this_capability')
    if impossible_role(inv,root):return end('refuted','committing_path_incompatible_with_fixed_initial_state_or_zero_role')
    if q.get('task_conflict'):return end('unresolved','task_direction_requires_review')
    for change in sorted(entries):
        if not privileged_paths(inv,change) or impossible_role(inv,change):continue
        for use in entries-{change}:
            qualified=privileged_paths(inv,change)
            writes=[w['path'] for pid,p in b.paths(change) if pid in qualified for w in p['writes']]
            for cell in linked_controls(inv,change,use):
                if any(same(cell,w) and not inv.graph._disjoint_keys(cell,w) for w in writes):
                    controls.append((change,use,cell))
    # A privilege change discovered during property binding need not be a second user-supplied anchor.
    evidence=[e for e in scope.get('scoped_observations',[]) if any(o.get('predicate_value') for o in e['outcomes'])]
    result['condition_probes']=[p for e in evidence for p in e['matched_probes']]
    if cat in ('FCR-FREEZE','FCR-PAUSE'):
        coverage=[];related=set()
        for change,use,cell in controls:
            for route in routes:
                if route['operation']!=use:continue
                path=f.paths[route['path']]['raw'];lookup=f.lookup(use)
                if not gates(path,cell):continue
                observed_block=any(e['measure']=='blocks' and e['change']==change and e['observe']==use and
                    any(o['predicate_value'] for o in e['outcomes']) for e in evidence)
                if not observed_block and not can_restrict(b,change,use,path,cell):continue
                ks=keys(cell);holder=bound_holder(route['debit'],lookup)
                if holder is None:continue
                targeted=len(ks)==1 and key(ks[0])==key(holder)
                shared=not ks or all(k.get('kind') in ('contract_address','literal') for k in ks)
                coverage.append({'writer':change,'use':use,'path':route['path'],'control':cell,
                    'outgoing_position':route['debit'],'targeted':targeted,'common_control':shared})
                related.add((change,use))
        result['source_basis']=coverage
        if cat=='FCR-FREEZE' and any(c['targeted'] for c in coverage):
            return end('main','conditional_source_mechanism_on_designated_outgoing_holder')
        if cat=='FCR-PAUSE' and any(c['common_control'] for c in coverage):
            for c in coverage:
                if not c['common_control']:continue
                gaps=[]
                for r in routes:
                    if not same(r['debit'],c['outgoing_position']) or r['path'] in privileged_paths(inv,r['operation']):continue
                    path=f.paths[r['path']]['raw']
                    if not any(same(x,c['control']) and key(keys(x))==key(keys(c['control'])) and gates(path,x) for x in inv.graph.request_reads(r['operation'])):
                        gaps.append(r['operation'])
                if not gaps:return end('main','common_outgoing_transfer_control_source_prediction_not_universal_proof')
                result['other_transfer_routes']=sorted(set(gaps))
            return end('unresolved','independent_outgoing_route_not_covered_by_common_control')
        affected=[r for r in routes if r['operation'] in entries]
        if not affected and any(holder_effect_for_business(b,o) for o in entries) or not affected and (related or evidence):
            return end('additional','limited_to_non_transfer_business_availability')
        if coverage:return end('additional','single_holder_or_different_side_or_common_scope_only')
        return end('unresolved','specific_outgoing_control_or_group_scope_not_established')
    if cat not in ('FCR-TRANSFER','FCR-MINT','FCR-DESTROY'):return end('additional','outside_five_capabilities')
    direct=privileged_paths(inv,root);claimed_effect=False
    checked=_direct_results(inv,root,cat,q);excluded=[]
    result['matched_counterevidence']=excluded
    for pid,p in b.paths(root):
        lookup=f.lookup(root);m=movements(b,root,p); t=transfer_shapes(b,root,p)
        if pid not in direct:continue
        for d in m['-']+literal_balance_zero(p,lookup):
            actual_holder=bound_holder(d,lookup)
            if actual_holder is None:continue
            right=bool(unit_origin(b,root,d) or any(same(d,r['debit']) for r in routes))
            if not right or holder_only(b,root,p,d) or consent_gate(b,root,p,d):continue
            verified=checked.get((pid,key(d)))
            if cat in ('FCR-TRANSFER','FCR-DESTROY') and verified and not verified['result']:
                excluded.append(verified);continue
            claimed_effect=True
            if cat=='FCR-DESTROY' and not any(same(d,c) and key(d)!=key(c) for c in m['+']) and not any(x['path']==pid and key(x['object'])==key(d) and key(x['holder'])==key(actual_holder) and x['same_holder_and_unit_full_settlement'] for e in q['evidence'] for x in inv.evidence[e].get('settlements',[])):
                result['source_basis'].append({'operation':root,'path':pid,'victim':d,'role_guards':p['guards']})
            if cat=='FCR-TRANSFER':
                for payer,payee in t:
                    if key(payer)==key(d):result['source_basis'].append({'operation':root,'path':pid,'payer':payer,'payee':payee,'permission_path':p['guards']})
        if cat=='FCR-MINT':
            for c in m['+']:
                verified=checked.get((pid,key(c)))
                if not (unit_origin(b,root,c) or any(same(c,r['credit']) for r in routes)) or any(same(c,d) for d in m['-']) and not (verified and verified['result']):continue
                if any(n.get('kind')=='transaction_value' for w in p['writes'] if key(w['path'])==key(c) for n in walk(w['value'])):continue
                beneficiary=bound_holder(c,lookup)
                if beneficiary is None:continue
                source_self=beneficiary.get('kind')=='actual_sender'
                verified=checked.get((pid,key(c)))
                if verified and not verified['result']:
                    excluded.append(verified);continue
                actor_receipt=bool(verified and verified['observed_values'].get('self_beneficiary')=='True')
                parameter=beneficiary.get('kind')=='parameter'
                guard_binds_recipient=any(key(n)==key(beneficiary) for g in p['guards'] for n in walk(g))
                if source_self or actor_receipt or parameter and not guard_binds_recipient:
                    result['source_basis'].append({'operation':root,'path':pid,'credit':c,'role_guard':True,
                        'controller_self_credit':'sender' if source_self else 'verified_self_witness' if actor_receipt else 'free_recipient_argument'})
    if result['source_basis']:return end('main','role_supported_five_class_capability_with_source_effect')
    if _all_direct_effects_excluded(b,root,cat,excluded):
        return end('refuted','matched_direct_effect_impossible_on_all_applicable_positions_and_paths')
    if excluded and any(x.get('bounded_exclusion_only') for x in excluded):
        return end('unresolved','required_positive_effect_not_established_in_checked_transition_scope')
    excess=[o for e in evidence if e['measure']=='ledger_grant' for o in e['outcomes'] if o['predicate_value']]
    routed_excess=any(v['holder']!=v['recipient'] and int(v['request_holder_delta_after'])<0 and
                      int(v['request_recipient_delta_after'])>int(v['effective_grant'])
                      for o in excess for v in [o.get('observed_values',{})] if v)
    if cat=='FCR-TRANSFER' and routed_excess and controls:return end('main','privileged_runtime_intervention_and_destination_credit_above_holder_grant')
    if any(e['measure'] in ('ledger_debit','ledger_receipt','ledger_grant','holder_net') for e in evidence):
        return end('additional','amount_or_redemption_difference_without_matched_five_class_capability')
    if claimed_effect:return end('unresolved','destination_or_consent_scope_not_established')
    return end('unresolved','role_beneficiary_token_or_applicable_effect_not_resolved')


def purpose_only_change(inv,q,proposal,cited):
    if not business_only(proposal) or q['current'].get('assessment')!='risk':return False
    # New independent source facts can demonstrate actual consent or settlement.
    # A compliance rationale plus a witness to the very same power cannot.
    return not any(any(x.get('same_holder_and_unit_full_settlement') and inv.evidence[e].get('operation')==inv.root(q) for x in inv.evidence[e].get('settlements',[])) or inv.evidence[e].get('control_noninterference',{}).get('proved')
                   or inv.evidence[e].get('holder_consent_counterexamples') and inv._direction_contradictions(q)
                   for e in cited) and not any(k in proposal and proposal[k]!=q['current'].get(k) for k in ('actor','object','phase','assumptions'))


def holder_effect_for_business(b,oid):
    return any(p.get('sensitive_effects') or any(w['path'].get('segments') for w in p['writes']) for _,p in b.paths(oid))


````

## source/src/pr_next_joint/investigation/context.py

原文件 SHA-256 `d3d4d2b1769c7b8aa9d196f782ba807d1436ccc8896355a30aa9bf278294f329`

````python
"""Source-first, graph-organized views. Complete original facts stay local."""
import copy,json,re
from collections import defaultdict,deque
from pr_next_joint.core import digest
from pr_next_joint.frontend.path_ir import walk
from .contracts import VERSION
from .protocol import INSTRUCTION,instruction,REVISION_GUIDANCE

class Catalog:
    def __init__(self,program,graph=None):
        self.program=program if hasattr(program,'context') else None
        self.context=program.context if self.program else program
        self.identity=self.program.identity if self.program else digest(program)
        self.graph=graph
        self.sources={s['file']:s for s in self.context['sources']}
        self.operations={o['id']:o for o in self.context['operations']}
        self.targets=sorted({o['target'] for o in self.operations.values()})
        self.target_alias={t:'T'+str(i+1) for i,t in enumerate(self.targets)}
        self.labels={};self.label_locations={};self.aliases=defaultdict(list);self.declarations={};self.declaration_aliases=defaultdict(list)
        for oid,o in self.operations.items():
            for name in (o['target']+'.'+o['function'],self.target_alias[o['target']]+'.'+o['function'],
                         o['function'],o['target'].split(':',1)[-1]+'.'+o['function']):self.aliases[name].append(oid)
        # A declaring base name is not necessarily a selected creation target.
        # Join the exact compiler-selected entry declaration to its source owner;
        # never resolve an overridden body merely by a matching spelling.
        self.declaration_entries=defaultdict(list)
        if self.program and hasattr(self.program,'lookup'):
            for oid,o in self.operations.items():
                lookup=self.program.lookup(oid);node=lookup.function(o['function'])
                node=node.get('generated_getter',node)
                owner=next((c for c in lookup.nodes.values() if c.get('nodeType')=='ContractDefinition'
                    and any(n.get('id')==node.get('id') for n in c.get('nodes',[]))),None)
                if owner is None or node.get('nodeType')!='FunctionDefinition':continue
                actual=lookup.anchor(node)
                if any(actual.get(k)!=o['source'].get(k) for k in ('file','start','length','ast_id')):continue
                aliases=(actual['file']+':'+owner['name']+'.'+o['function'],owner['name']+'.'+o['function'])
                for alias in aliases:
                    self.aliases[alias].append(oid)
                    self.declaration_entries[alias].append({'operation':oid,'declaring_contract':owner['name'],
                        'applied_target':o['target'],'ast_id':node['id'],'source':actual,
                        'basis':'compiler-selected implementation and exact declaration containment/span'})
        # Internal declarations supply source evidence, never external transactions.
        if self.program and hasattr(self.program,'lookups'):
            from pr_next_joint.frontend.source_entry_identity import declared_type_pair
            for target,lookup in self.program.lookups.items():
                bases=lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
                # Old compiler ASTs omit scope on functions. The owning contract
                # is still exact from AST containment, including inherited bases.
                owners={child['id']:c['id'] for c in lookup.nodes.values() if c.get('nodeType')=='ContractDefinition' for child in c.get('nodes',[]) if isinstance(child,dict)}
                for n in lookup.nodes.values():
                    if n.get('nodeType') not in ('FunctionDefinition','ModifierDefinition') or n.get('scope',owners.get(n['id'])) not in bases:continue
                    if n.get('nodeType')=='FunctionDefinition' and n.get('visibility') not in ('internal','private'):continue
                    pairs=[declared_type_pair(p.get('typeName',{}),lookup) for p in n.get('parameters',{}).get('parameters',[])]
                    if any(p is None for p in pairs):continue
                    sig=n.get('name','')+'('+','.join(p[1] for p in pairs)+')';ref='decl_'+digest([target,n['id']])[:20]
                    self.declarations[ref]={'id':ref,'target':target,'ast_id':n['id'],'function':sig,'source':lookup.anchor(n),'external_transaction':False}
                    owner=lookup.nodes.get(n.get('scope',owners.get(n['id'])),{})
                    declared=(lookup.anchor(n)['file']+':'+owner.get('name','')+'.'+sig,owner.get('name','')+'.'+sig)
                    for alias in (target+'.'+sig,target.split(':',1)[-1]+'.'+sig,sig)+declared:
                        self.declaration_aliases[alias].append(ref)
            from pr_next_joint.frontend.dispatch import resolve as dispatch
            for alias,refs in list(self.declaration_aliases.items()):
                targets={self.declarations[r]['target'] for r in refs}
                if len(targets)!=1 or len(refs)<2:continue
                lookup=self.program.lookups[next(iter(targets))]
                resolved={dispatch(lookup,lookup.nodes[self.declarations[r]['ast_id']])['id'] for r in refs}
                chosen=[r for r in refs if self.declarations[r]['ast_id'] in resolved]
                if len(resolved)==len(chosen)==1:self.declaration_aliases[alias]=chosen
        self.internal_callers=defaultdict(list)
        if self.program and hasattr(self.program,'lookup'):
            def reaches(lookup,body,nid,seen):
                from pr_next_joint.frontend.dispatch import resolve as dispatch
                refs=set()
                for n in walk(body):
                    if n.get('nodeType')!='FunctionCall':continue
                    ref=n.get('expression',{}).get('referencedDeclaration');node=lookup.nodes.get(ref,{})
                    if n.get('expression',{}).get('nodeType')=='Identifier' and node.get('nodeType')=='FunctionDefinition':ref=dispatch(lookup,node)['id']
                    refs.add(ref)
                refs|={n.get('modifierName',{}).get('referencedDeclaration') for n in walk(body) if n.get('nodeType')=='ModifierInvocation'}
                if nid in refs:return True
                for ref in refs-seen:
                    node=lookup.nodes.get(ref,{})
                    if node.get('nodeType') in ('FunctionDefinition','ModifierDefinition') and reaches(lookup,node,nid,seen|{ref}):return True
                return False
            for ref,decl in self.declarations.items():
                for oid,operation in self.operations.items():
                    if operation['target']!=decl['target']:continue
                    lookup=self.program.lookup(oid)
                    if reaches(lookup,lookup.function(operation['function']),decl['ast_id'],set()):self.internal_callers[ref].append(oid)
        self.frontier=self.context['frontier'];self.adj=defaultdict(set)
        for edge in self.frontier:
            self.adj[edge['from']].add(edge['to']);self.adj[edge['to']].add(edge['from'])
    def name(self,oid):
        o=self.operations[oid];return o['target']+'.'+o['function']
    def slice(self,anchor):
        s=self.sources[anchor['file']]['content'].encode('utf-8')
        return s[anchor['start']:anchor['start']+anchor['length']].decode('utf-8',errors='replace')
    def lines(self,anchor):
        s=self.sources[anchor['file']]['content'].encode('utf-8')
        return [s[:anchor['start']].count(b'\n')+1,s[:anchor['start']+anchor['length']].count(b'\n')+1]
    def resolve(self,anchor):
        if not isinstance(anchor,str):return []
        if anchor in self.labels:return list(self.labels[anchor])
        if anchor in self.aliases:return sorted(set(self.aliases[anchor]))
        # A literal placeholder is not an ABI type. Resolve its exact qualified
        # declaration family only when the compiler catalog has a single entry.
        # Concrete wrong signatures (including enum/uint mismatches) are NOT repaired.
        placeholder=re.fullmatch(r'(.+)\((?:function|\.\.\.|\?)\)',anchor)
        if placeholder:
            family=placeholder[1]+'('
            return sorted({o for alias,ids in self.aliases.items() if alias.startswith(family)
                           for o in ids})
        # Short names only enumerate exact declarations. Never fuzzy-select one.
        if re.fullmatch(r'[A-Za-z_$][\w$]*',anchor):
            return sorted(o for o,x in self.operations.items() if x['function'].split('(')[0]==anchor)
        m=re.fullmatch(r'(.+\.sol):(\d+)(?:[-:](\d+))?',anchor)
        if m and m[1] in self.sources:
            lo=int(m[2]);hi=int(m[3] or lo)
            return sorted(o for o,x in self.operations.items() if x['source']['file']==m[1] and
                          self.lines(x['source'])[0]<=lo<=self.lines(x['source'])[1] and hi>=lo)
        return []
    def target_branches(self,anchors,core=None):
        initial=core or (anchors[0] if anchors else None)
        rows=self.declaration_entries.get(initial,[])
        ids=self.resolve(initial)
        if len(ids)<2 or set(ids)!={r['operation'] for r in rows}:return []
        if len({(r['ast_id'],str(r['source'])) for r in rows})!=1:return []
        targets=[self.operations[o]['target'] for o in ids]
        return sorted(targets) if len(set(targets))==len(ids) else []
    def bind(self,anchors,core=None,prior=None,target=None):
        def allowed(ids):
            return [oid for oid in ids if target is None or self.operations[oid]['target']==target]

        located={};unresolved=[];ambiguous=[];internal=[]
        for anchor in anchors:
            ids=allowed(self.resolve(anchor))
            if not ids:
                refs=[r for r in self.declaration_aliases.get(anchor,[]) if target is None or self.declarations[r]['target']==target]
                if refs:
                    internal.extend(copy.deepcopy(self.declarations[r]) for r in dict.fromkeys(refs))
                    if len(refs)>1:ambiguous.append({'anchor':anchor,'declaration_contexts':list(dict.fromkeys(refs))})
                else:unresolved.append(anchor)
            elif len(ids)>1:ambiguous.append({'anchor':anchor,'candidates':ids});located[anchor]=ids
            else:located[anchor]=ids
        requested=core if isinstance(core,str) else anchors[0] if anchors else None
        core_ids=allowed(self.resolve(requested)) if requested else []
        protected_ambiguity=len(core_ids)>1 and (self.declaration_entries.get(requested) or
            re.fullmatch(r'.+\((?:function|\.\.\.|\?)\)',requested or ''))
        if core is None and len(core_ids)!=1 and not protected_ambiguity:
            core_ids=next((v for v in located.values() if len(v)==1),[])
        # A valid old core is retained only when the revision did not request a
        # different explicit root. An invalid new core cannot replace it silently.
        internal_contexts={r['id']:self.internal_callers.get(r['id'],[]) for r in internal}
        contexts=sorted({i for ids in internal_contexts.values() for i in ids})
        # An internal-only clue starts in its real external caller context. A
        # unique caller is exact; multiple callers remain ambiguous, never an
        # invented directly callable internal transaction.
        if not core_ids and len(contexts)==1 and requested in self.declaration_aliases:core_ids=contexts
        selection='explicit_root' if core is not None else 'initial_source_anchor'
        old_core=(prior or {}).get('core_operation')
        if core is None and (prior or {}).get('core_exact') and old_core in self.operations:
            # Ordering, adding or dropping supplementary references is not a
            # request to relocate the existing root. accept validates genuine
            # semantic corrections separately, without requiring a root field.
            core_ids=[old_core];selection='preserved_prior_core'
        core_operation=core_ids[0] if len(core_ids)==1 else None
        core_anchor=((prior or {}).get('core_anchor') or self.name(old_core)) if selection=='preserved_prior_core' else (
            core if core is not None and len(self.resolve(core))==1 else next((a for a,ids in located.items() if ids==core_ids),None))
        return {'applied_context':target,'located':located,'operations':sorted({i for ids in located.values() for i in ids}|set(contexts)|set(core_ids)),
                'unresolved':unresolved,'ambiguous':ambiguous,'internal_references':internal,
                'internal_external_caller_contexts':internal_contexts,
                'core_operation':core_operation,'core_exact':core_operation is not None,
                'core_anchor':core_anchor,'core_selection':selection,
                'exact':core_operation is not None,'all_references_exact':bool(located) and not unresolved and not ambiguous,
                'supplementary_gaps':unresolved+ambiguous,
                'declaration_entry_bindings':{a:copy.deepcopy(self.declaration_entries[a]) for a in anchors if a in self.declaration_entries},
                'candidate_core_operations':sorted(set(core_ids or contexts or [i for v in located.values() for i in v])),
                'placeholder_clarifications':[{'original':a,'resolved':self.name(ids[0]),
                    'source':copy.deepcopy(self.operations[ids[0]]['source']),
                    'basis':'literal placeholder; unique exact target/declaration family, not fuzzy ABI matching'}
                    for a,ids in located.items() if len(ids)==1 and re.fullmatch(r'.+\((?:function|\.\.\.|\?)\)',a)]}
    def related(self,oid):return sorted(self.adj[oid])
    def card(self,oid):
        o=self.operations[oid];return {'anchor':self.name(oid),'operation_id_for_host':oid,
            'source':copy.deepcopy(o['source']),'lines':self.lines(o['source']),
            'code':self.slice(o['source']),'parameters':[{k:v for k,v in p.items() if k=='name'} for p in o['parameters']]}
    def support(self,oid):
        """Actual declarations, modifiers and internal calls, not normality templates."""
        if not self.program or not hasattr(self.program,'lookup'):
            # Read-only prepared-message previews can reuse the exact saved M1 graph.
            graph=self.graph if isinstance(self.graph,dict) else {};nodes={n['id']:n for n in graph.get('nodes',[])}
            anchors=[];o=self.operations[oid]
            for edge in graph.get('edges',[]):
                if edge['from']==oid and edge['kind'] in ('calls','modifier'):
                    a=nodes.get(edge['to'],{}).get('data',{}).get('source')
                    if a:anchors.append(a)
            roots={n['root'] for p in o['paths'] for ref in p.get('guards',[])+[w['selector'] for w in p.get('writes',[])]
                   for n in walk(self.context['terms'].get(ref,{}).get('expression',{})) if n.get('kind')=='storage'}
            anchors +=[r['source'] for r in self.context['references'].values() if r['target']==o['target'] and r['ast_id'] in roots]
            return [{'source':a,'code':self.slice(a),'kind':'saved_exact_source_dependency'} for a in {tuple(sorted(a.items())):a for a in anchors if a['file'] in self.sources}.values()]
        lookup=self.program.lookup(oid);o=self.operations[oid];body=lookup.function(o['function'])
        needed=[]
        for n in walk(body):
            if n.get('nodeType')=='ModifierInvocation':needed.append(n.get('modifierName',{}).get('referencedDeclaration'))
            if n.get('nodeType')=='FunctionCall':needed.append(n.get('expression',{}).get('referencedDeclaration'))
        roots={n['root'] for p in o['paths'] for t in p.get('guards',[]) for n in walk(self.context['terms'].get(t,{}).get('expression',{})) if n.get('kind')=='storage'}
        for w in (self.program.writes.values()):
            if w['operation']==oid:roots.add(w['raw']['path']['root'])
        needed+=sorted(roots)
        result=[]
        for nid in dict.fromkeys(needed):
            node=lookup.nodes.get(nid)
            if not node or node.get('nodeType') not in ('VariableDeclaration','ModifierDefinition','FunctionDefinition'):continue
            a=lookup.anchor(node)
            if a['length'] and a['file'] in self.sources:
                result.append({'source':a,'code':self.slice(a),'kind':node['nodeType']})
        return result
    def index(self):
        return {'targets':{a:t for t,a in self.target_alias.items()},'entries':[
            self.target_alias[o['target']]+'.'+o['function'] for o in sorted(self.operations.values(),key=lambda x:(x['target'],x['function']))],
            'meaning':'T aliases denote exact targets; repeated inherited source remains target-specific.'}

    def required_context(self,operations):
        """AST-bound declaration/call closure for one feedback unit, not top-k.

        Include contract headers, base declarations and referenced helpers. If an
        exact closure cannot be built, the caller must not send a partial unit.
        """
        fragments={};identities=[];missing=[]
        def add(anchor,kind,target):
            if not anchor or anchor.get('file') not in self.sources:return
            loc=(anchor['file'],anchor['start'],anchor['length'])
            entry=fragments.setdefault(loc,{'source':{k:v for k,v in anchor.items() if k!='ast_id'},
                'kind':kind,'code':self.slice(anchor),'targets':[]})
            if target not in entry['targets']:entry['targets'].append(target)
        for oid in dict.fromkeys(operations):
            if oid not in self.operations:continue
            o=self.operations[oid]
            if not self.program or not hasattr(self.program,'lookup'):
                missing.append({'operation':oid,'reason':'compiler_declaration_context_unavailable'});continue
            lookup=self.program.lookup(oid);body=lookup.function(o['function'])
            if not body:missing.append({'operation':oid,'reason':'exact_entry_declaration_unavailable'});continue
            declaration=body.get('generated_getter',body)
            from pr_next_joint.frontend.source_entry_identity import function_kind
            owners={n['id']:c for c in lookup.nodes.values() if c.get('nodeType')=='ContractDefinition'
                    for n in c.get('nodes',[]) if isinstance(n,dict)}
            declaring=owners.get(declaration.get('id'),lookup.contract_node)
            identities.append({'anchor':self.name(oid),'entry_kind':'generated_getter' if 'generated_getter' in body else function_kind(body),
                'declaring_contract':declaring.get('name'),'applied_target':o['target'],
                'basis':'compiler AST kind and declaration containment, not function spelling',
                'constructor_declarations':[{'declaring_contract':c.get('name'),'compiler_kind':'constructor',
                    'source':lookup.anchor(n),'external_transaction':False}
                    for c in lookup.nodes.values() if c.get('nodeType')=='ContractDefinition' and
                        c['id'] in lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
                    for n in c.get('nodes',[]) if function_kind(n)=='constructor']})
            bases=lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']])
            queue=[declaration['id']]
            for cid in bases:
                c=lookup.nodes.get(cid,{})
                if not c:continue
                a=lookup.anchor(c);children=[lookup.anchor(n)['start'] for n in c.get('nodes',[]) if lookup.anchor(n).get('file')==a['file']]
                header_length=min(children)-a['start'] if children else a['length']
                if header_length<=0:missing.append({'target':o['target'],'reason':'contract_header_not_locatable'});continue
                add({**a,'length':header_length},'contract_header_and_inheritance',o['target'])
                # Declaration context is conservative and neutral; no business
                # classification is inferred from state-variable names.
                queue += [n['id'] for n in c.get('nodes',[]) if n.get('nodeType') in
                          ('VariableDeclaration','StructDefinition','EnumDefinition','UserDefinedValueTypeDefinition')]
                queue += [n['id'] for n in c.get('nodes',[]) if function_kind(n)=='constructor']
            for n in lookup.nodes.values():
                if n.get('nodeType') in ('PragmaDirective','ImportDirective'):
                    add(lookup.anchor(n),n['nodeType'],o['target'])
            seen=set()
            while queue:
                nid=queue.pop()
                if nid in seen:continue
                seen.add(nid);n=lookup.nodes.get(nid,{})
                if n.get('nodeType') not in ('FunctionDefinition','ModifierDefinition','VariableDeclaration',
                      'StructDefinition','EnumDefinition','EventDefinition','UserDefinedValueTypeDefinition'):continue
                owner=owners.get(nid)
                if owner and owner['id'] not in bases:
                    a=lookup.anchor(owner);children=[lookup.anchor(x)['start'] for x in owner.get('nodes',[]) if lookup.anchor(x).get('file')==a['file']]
                    add({**a,'length':min(children)-a['start'] if children else a['length']},'referenced_declaration_contract_header',o['target'])
                add(lookup.anchor(n),n['nodeType'],o['target'])
                # referencedDeclaration denotes the lexical declaration, not
                # necessarily the implementation executed by this target.
                # Reuse the same dispatch as source execution, including the
                # lexical owner of super and explicit/private bindings.
                from pr_next_joint.frontend.dispatch import resolve,member_target
                call_expressions=set()
                for call in walk(n):
                    if call.get('nodeType')!='FunctionCall':continue
                    expr=call.get('expression',{});ref=expr.get('referencedDeclaration')
                    target=lookup.nodes.get(ref,{})
                    internal=expr.get('typeDescriptions',{}).get('typeIdentifier','').startswith('t_function_internal_')
                    if target.get('nodeType')!='FunctionDefinition':
                        if internal:
                            missing.append({'target':o['target'],'source':lookup.anchor(call),
                                'reason':'internal_call_implementation_context_unresolved'})
                        continue
                    call_expressions.add(expr.get('id'))
                    try:
                        owner=owners.get(ref,{})
                        if (target.get('visibility')!='private' and owner.get('id') in bases and len(bases)>1
                                and (target.get('scope')!=owner.get('id') or any(not p.get('typeDescriptions',{}).get('typeIdentifier')
                                    for p in target.get('parameters',{}).get('parameters',[])))):
                            raise ValueError('compiler_dispatch_metadata_incomplete')
                        if expr.get('nodeType')=='Identifier':bound=resolve(lookup,target)
                        else:bound=member_target(lookup,call,target)
                        if bound is None:
                            # An external/interface declaration is source
                            # context, not a proven implementation binding.
                            queue.append(ref)
                            if internal:raise ValueError('internal_dispatch_not_resolved')
                        else:queue.append(bound['id'])
                    except (ValueError,KeyError,TypeError,AttributeError) as error:
                        queue.append(ref)
                        missing.append({'target':o['target'],'source':lookup.anchor(call),
                            'reason':'required_call_dispatch_context_unresolved',
                            'detail':type(error).__name__+':'+str(error)})
                for child in walk(n):
                    ref=child.get('referencedDeclaration')
                    if ref in lookup.nodes and child.get('id') not in call_expressions:queue.append(ref)
                    if child.get('nodeType')=='ModifierInvocation':
                        queue.append(child.get('modifierName',{}).get('referencedDeclaration'))
            # Exact source closure has no function-name or dataset-ID exceptions.
        ordered=sorted(fragments.items())
        # Do not send nested source twice (e.g. a struct member inside its struct).
        kept=[]
        for loc,entry in sorted(ordered,key=lambda x:(x[0][0],x[0][1],-x[0][2])):
            if any(loc[0]==p['source']['file'] and p['source']['start']<=loc[1] and
                   loc[1]+loc[2]<=p['source']['start']+p['source']['length'] for p in kept):continue
            kept.append(entry)
        return kept,identities,missing

class SourceContext:
    def __init__(self,program,catalog,counter):
        self.program,self.catalog,self.counter=program,catalog,counter;self.initial_view=None;self.initial_scope=None
    def _messages(self,value,recovery=False):
        return [{'role':'system','content':instruction(self.program.options.scope,recovery)},
                {'role':'user','content':json.dumps(value,ensure_ascii=False,separators=(',',':'))}]
    def _count(self,value):return self.counter.count(self._messages(value))
    def _model_card(self,oid):
        c=self.catalog.card(oid);c.pop('operation_id_for_host');c['support']=self.catalog.support(oid)
        # Fact payloads and expression graphs never re-enter M2 through this view.
        for x in [c,*c['support']]:
            if 'source' in x:x['source']={k:v for k,v in x['source'].items() if k!='ast_id'}
        return c
    def _focus(self):
        graph=self.catalog.graph
        if graph is None:
            return None, []
        front=graph.neutral_frontier()
        r=front['primary']
        if r is None:
            return None, []
        names=self.catalog.name
        focus={'write':names(r['writer']),'use':names(r['use']),'cell':r['declaration'],
               'read_in':r['role_of_read'],'question':'Which actual subject and right are affected? What observable distinguishes the applicable explanations?'}
        use_cells=[w['raw']['path'] for w in self.program.writes.values() if w['operation']==r['use']]
        related=graph.closure_operations(r['use'],[r['ordered_read_key'],*use_cells])
        return focus,list(dict.fromkeys([r['writer'],r['use'],*related]))

    @staticmethod
    def _share(value):
        """Intern only identical rows across questions; branch, key and role are part of identity."""
        if len(value['questions'])<2:
            return value
        value=copy.deepcopy(value)
        occurrences=defaultdict(list)
        for qi,q in enumerate(value['questions']):
            for field in ('entry_identity_facts','evidence'):
                for i,v in enumerate(q.get(field,[])):
                    occurrences[(field,digest(v))].append((qi,i))
        shared={}
        for (field,h),sites in occurrences.items():
            if len(sites)<2:
                continue
            qi,i=sites[0];row=value['questions'][qi][field][i]
            if len(json.dumps(row))<100:
                continue
            ref='s'+str(len(shared)+1);shared[ref]=row
            for qi,i in sites:
                value['questions'][qi][field][i]={'shared':ref}
        if shared:
            value['shared_rows']=shared
        return value

    def initial(self):
        p=self.program;cat=self.catalog;target=p.options.input_target;limit=p.options.input_limit
        base={'presentation':VERSION,'task':p.options.scope,'entry_index':cat.index(),
              'scope_note':'Unexpanded relevant obligations not otherwise resolved remain uncovered; source delivery is not completion.',
              'semantic_focus':'Explain the actual resource/right and applicable authorization using the shown source; category and judgment are proposals.'}
        complete={**base,'source_files':[{'file':f,'content':s['content']} for f,s in cat.sources.items()]}
        focus,focus_ops=self._focus()
        if self._count(complete)<=target:
            manifest={'mode':'complete_source','expanded_operations':sorted(cat.operations),'unexpanded_operations':[],
                      'complete_source_files':sorted(cat.sources),'fragments':[],'requested_reading':'whole_task',
                      'focus_operations':focus_ops,'open_clues_allowed':True}
            if focus and self._count({**complete,'primary_question':focus})<=target:
                complete['primary_question']=focus
                manifest['focus_delivery']='compact_source_locator'
            elif focus:
                short={'write':focus['write'],'use':focus['use']}
                if self._count({**complete,'primary_question':short})<=target:
                    complete['primary_question']=short
                    manifest['focus_delivery']='minimal_two_entry_locator'
                else:
                    manifest['focus_delivery']='summary_omitted_to_preserve_full_source'
            else:
                manifest['focus_delivery']='no_supported_meeting; source open'
            locators=[{'entry':cat.name(r['operation']),'question':r['kind'],'positions':[cat.program.lookup(r['operation']).nodes.get(w['position']['root'],{}).get('name') for w in r['extra_effects']]} for r in p.source_candidates]
            shown=[]
            for locator in locators:
                if self._count({**complete,'additional_source_questions':shown+[locator]})>target:break
                shown.append(locator)
            if shown:complete['additional_source_questions']=shown
            manifest['additional_source_questions']={'delivered':len(shown),'total':len(locators),'full_source_preserved':True}
            return complete,manifest
        # Structural degree and per-target round robin; never labels, file polarity or old hits.
        queues=[]
        for t in cat.targets:
            ordered=sorted((i for i,o in cat.operations.items() if o['target']==t),key=lambda i:(cat.operations[i].get('generated_getter',False),-len(cat.adj[i]),cat.name(i)))
            queues.append(deque(ordered))
        order=[]
        while any(queues):
            for q in queues:
                if q:order.append(q.popleft())
        value={**base,'source_fragments':[]};expanded=[];seen=set();partial=[]
        focus_missing=[];focus_placed=False
        if focus:
            closure,identities,focus_missing=cat.required_context(focus_ops)
            trial={**value,'primary_question':focus,'related_source':closure}
            if not focus_missing and self._count(trial)<=target:
                value=trial;focus_placed=True;expanded.extend(focus_ops)
                for frag in closure:
                    loc=frag['source'];seen.add((loc['file'],loc['start'],loc['length']))
            elif not focus_missing:
                focus_missing=[{'reason':'source_focus_closure_exceeds_soft_target','operations':focus_ops}]
        order=list(dict.fromkeys(focus_ops+order))
        for oid in order:
            c=self._model_card(oid);a=cat.operations[oid]['source'];loc=(a['file'],a['start'],a['length'])
            if loc in seen:
                # Share exact source bytes but retain each target application in the index/manifest.
                expanded.append(oid);continue
            candidate={**value,'source_fragments':value['source_fragments']+[c]}
            if self._count(candidate)<=target or (not value['source_fragments'] and self._count(candidate)<=limit):
                value=candidate;expanded.append(oid);seen.add(loc)
                for neighbor in cat.related(oid):
                    if neighbor in expanded:continue
                    nc=self._model_card(neighbor);na=cat.operations[neighbor]['source'];nl=(na['file'],na['start'],na['length'])
                    if nl in seen:expanded.append(neighbor);continue
                    trial={**value,'source_fragments':value['source_fragments']+[nc]}
                    if self._count(trial)<=target:value=trial;expanded.append(neighbor);seen.add(nl)
            if self._count(value)>=target:break
        # Oversized single functions: use whole AST statements, explicitly recording partial scope.
        if not expanded and cat.program and hasattr(cat.program,'lookup'):
            for oid in order:
                o=cat.operations[oid];lookup=cat.program.lookup(oid);body=lookup.function(o['function'])
                for node in body.get('body',{}).get('statements',[]):
                    a=lookup.anchor(node);c={'anchor':cat.name(oid),'source':{k:v for k,v in a.items() if k!='ast_id'},
                        'code':cat.slice(a),'partial_function':True}
                    trial={**value,'source_fragments':value['source_fragments']+[c]}
                    if self._count(trial)<=target:value=trial;partial.append(oid)
                if partial:break
        for i,c in enumerate(value['source_fragments']):
            c['fragment']='S'+str(i+1);cat.labels[c['fragment']]=cat.resolve(c['anchor'])
            cat.label_locations[c['fragment']]=copy.deepcopy(c['source'])
        missing=sorted(set(cat.operations)-set(expanded))
        value['unexpanded_entry_count']=len(missing)
        # Exact missing IDs stay in the host manifest; all source names already
        # occur in the complete compact entry index, so do not duplicate them.
        return value,{'mode':'graph_source_fragments','expanded_operations':sorted(set(expanded)),
            'partially_expanded_operations':sorted(set(partial)),'unexpanded_operations':missing,
            'requested_reading':'delivered_scope','focus_operations':focus_ops,'focus_context_gaps':focus_missing,
            'focus_delivery':'source_closure' if focus_placed else 'open_source_view','open_clues_allowed':True,
            'complete_source_files':[],'fragments':[{'fragment':c['fragment'],'anchor':c['anchor'],'partial':c.get('partial_function',False)} for c in value['source_fragments']]}
    def focused(self,feedback):
        base={'presentation':VERSION,'task':self.program.options.scope,
              'purpose':'Revise only these issues using the original source and new local evidence; omitted issues remain.',
              'source_and_explanation_are_distinct':True,'questions':[],'revision_rule':REVISION_GUIDANCE}
        complete={**base,'source_files':[{'file':f,'content':s['content']} for f,s in self.catalog.sources.items()]}
        units=[];deduplicated=0
        for q in feedback['questions']:
            item=copy.deepcopy(q);ops=item.pop('operations',[])
            # Only byte/structure-equivalent evidence is merged. Caller, key,
            # branch, assumptions and formula identity remain part of equality.
            for e in item.get('evidence',[]):
                for field in ('probe_results','comparisons'):
                    if not isinstance(e.get(field),list):continue
                    rows={}
                    for v in e[field]:rows.setdefault(digest(v),v)
                    deduplicated+=len(e[field])-len(rows);e[field]=list(rows.values())
            fragments,identity,missing=self.catalog.required_context(ops)
            item['entry_identity_facts']=identity
            units.append((q['id'],item,ops,fragments,missing))
        all_complete={**complete,'questions':[u[1] for u in units]}
        full_mode=self._count(self._share(all_complete))<=self.program.options.input_limit
        # Even when several units do not fit together, preserve complete source
        # if a whole individual unit fits. Oversized units do not block others.
        if not full_mode:
            full_mode=any(self._count({**complete,'questions':[u[1]]})<=self.program.options.input_limit for u in units)
        value=complete if full_mode else {**base,'related_source':[]}
        selected=[];omitted=[];used=set()
        for qid,item,ops,fragments,missing in units:
            if full_mode:
                trial={**value,'questions':value['questions']+[item]}
            else:
                if missing:
                    omitted.append({'issue':qid,'reason':'required_source_context_not_resolved','details':missing});continue
                merged={digest(x['source']):x for x in value['related_source']}
                for f in fragments:
                    k=digest(f['source'])
                    if k in merged:merged[k]['targets']=sorted(set(merged[k]['targets']+f['targets']))
                    else:merged[k]=copy.deepcopy(f)
                trial={**value,'questions':value['questions']+[item],'related_source':list(merged.values())}
            tokens=self._count(self._share(trial))
            if tokens<=self.program.options.input_limit:
                value=trial;selected.append(qid);used.update(ops)
            else:omitted.append({'issue':qid,'reason':'whole_required_source_and_evidence_unit_exceeds_remaining_capacity',
                                 'actual_trial_input_tokens':tokens,'input_limit':self.program.options.input_limit})
        value=self._share(value)
        visible={}
        for question in value['questions']:
            labels={}
            for field in question.get('evidence',[]):
                row=value.get('shared_rows',{}).get(field.get('shared'),field)
                if isinstance(row.get('id'),str):
                    labels[row['id']]=[p['id'] for p in row.get('probe_results',[]) if 'id' in p]
            visible[question['id']]=labels
        return value,{'mode':'focused_evidence','source_mode':'complete_source_once' if full_mode else 'compiler_bound_local_context',
            'wire_evidence':visible,'shared_row_count':len(value.get('shared_rows',{})),
            'selected_issues':selected,'unexpanded_feedback_issues':omitted,'expanded_operations':sorted(used),
            'complete_source_files':sorted(self.catalog.sources) if full_mode else [],'deduplicated_exact_evidence_rows':deduplicated,
            'necessary_context_not_silently_clipped':True,'no_full_facts_or_graph_or_unrelated_history':True}
    def messages(self,feedback=None,recovery=False):
        if recovery:
            if self.initial_view is None:self.initial_view,self.initial_scope=self.initial()
            data=copy.deepcopy(self.initial_view);data['purpose']='Return a consumable final issues JSON; the first response had no usable final analysis.'
            if feedback and feedback.get('binding_diagnostics'):
                data['binding_diagnostics']=copy.deepcopy(feedback['binding_diagnostics'])
            manifest={**copy.deepcopy(self.initial_scope),'mode':'protocol_recovery_reused_source','reused_initial_source_view':True}
        elif feedback is None:
            if self.initial_view is None:self.initial_view,self.initial_scope=self.initial()
            data,manifest=copy.deepcopy(self.initial_view),copy.deepcopy(self.initial_scope)
        else:data,manifest=self.focused(feedback)
        messages=self._messages(data,recovery);manifest.update(input_tokens=self.counter.count(messages),
            counter_identity=self.counter.identity,messages_sha256=digest(messages),
            counting_scope='complete V4.1 text message envelope including high/JSON markers; offline count, service usage recorded separately')
        return messages,manifest

````

## source/src/pr_next_joint/investigation/contracts.py

原文件 SHA-256 `202bd5701db7858666257b90c21ca358e945334f18481e51d8f1d54f402a208a`

````python
"""Finite investigation controls and host-owned artifacts; no business detectors."""
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib, json, os, tempfile
from pr_next_joint.core import digest

VERSION = 'permission-risks-relational-properties-r2'
CATEGORIES = ('AC','FCR-TRANSFER','FCR-MINT','FCR-DESTROY','FCR-PAUSE','FCR-FREEZE')

def ident(prefix, value): return prefix+'_'+digest(value)[:20]

def write(path, value):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    data=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
    fd,tmp=tempfile.mkstemp(prefix='.'+path.name,dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as stream:stream.write(data);stream.flush();os.fsync(stream.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
    return hashlib.sha256(data).hexdigest()

@dataclass(frozen=True)
class Options:
    scope: str = 'AC'
    max_paths: int = 48
    input_target: int = 16384
    input_limit: int = 32768
    output_limit: int = 32768
    attempt_limit: int = 2
    feedback: bool = True
    prefix_depth: int = 2
    max_prefixes: int = 24
    max_actions: int = 64
    solver_timeout_ms: int = 3000
    seconds: float = 120
    def __post_init__(self):
        if self.scope not in ('AC','FCR'):raise ValueError('single_AC_or_FCR_task_required')
        if not 1<=self.max_paths<=48:raise ValueError('path_bound')
        if (self.input_target,self.input_limit,self.output_limit)!=(16384,32768,32768):raise ValueError('frozen_message_limits')
        if self.attempt_limit not in (1,2) or not 0<=self.prefix_depth<=2 or not 1<=self.max_prefixes<=24:raise ValueError('frozen_call_or_prefix_bound')
        if not 1<=self.max_actions<=64 or not 0<self.seconds<=120 or not 0<self.solver_timeout_ms<=3000:raise ValueError('frozen_investigation_bound')
    def record(self):return asdict(self)

````

