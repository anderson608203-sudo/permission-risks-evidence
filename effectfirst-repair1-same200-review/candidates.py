"""Small source-located questions about applied extra effects and independent exits."""
from pr_next_joint.frontend.path_ir import walk, key
from pr_next_joint.frontend.storage import selectors
from pr_next_joint.core import digest


def source_candidates(facts):
    result=[]
    for oid,op in sorted(facts.operations.items(),key=lambda x:(x[1]['target'],x[1]['source']['start'],x[0])):
        if op.get('generated_getter'):continue
        lookup=facts.lookup(oid);fn=lookup.function(op['function']);origin=fn.get('scope')
        bases=lookup.nodes.get(origin,{}).get('linearizedBaseContracts',[])[1:]
        peers=[n for c in bases for n in lookup.nodes[c].get('nodes',[]) if n.get('nodeType')=='FunctionDefinition'
               and n.get('scope')!=origin and n.get('body') and n.get('name')==fn.get('name') and fn.get('name')
               and len(n.get('parameters',{}).get('parameters',[]))==len(fn.get('parameters',{}).get('parameters',[]))]
        parent_roots={x.get('referencedDeclaration') for p in peers for n in walk(p.get('body') or {})
            if n.get('nodeType')=='Assignment' for x in walk(n.get('leftHandSide') or {})}
        extra=[];exits=[]
        span=lookup.anchor(fn)
        for pid,p in facts.operation_paths(oid,True):
            for w in p['writes']:
                loc=w['source']
                if peers and loc['file']==span['file'] and span['start']<=loc['start']<span['start']+span['length'] and w['path']['root'] not in parent_roots:
                    extra.append({'path':pid,'position':w['path'],'value':w['value'],'source':loc})
            for effect in p.get('sensitive_effects',[]):
                if 'selfdestruct' in str(effect.get('kind','')) or 'selfdestruct' in str(effect.get('operation','')):
                    exits.append({'path':pid,'effect':effect})
        # Actual source effects use a typed `selfdestruct` kind in this frontend.
        groups={}
        for item in extra:
            identity=('applied_extra_effect',key(item['source']),key(item['position']))
            groups.setdefault(identity,{})[key(item)]=item
        for item in exits:
            identity=('independent_sensitive_exit',key(item['effect'].get('source')),item['effect'].get('kind'))
            groups.setdefault(identity,{})[key(item)]=item
        for identity,occurrences in groups.items():
            kind=identity[0];items=list(occurrences.values())
            row={'operation':oid,'target':op['target'],'kind':kind,
                 'extra_effects':items if kind=='applied_extra_effect' else [],
                 'sensitive_exits':items if kind=='independent_sensitive_exit' else [],
                 'candidate_requires_assessment':True,'not_counterevidence':True}
            row['id']='candidate_'+digest(row)[:16];result.append(row)
    return result


def investigate(inv):
    inv.candidate_trace=[]
    if inv.f.options.scope=='AC':
        rules=inv.semantics.rules
        # One question for each distinct occurrence. Untyped questions do
        # not inherit a model opinion; a real scoped policy can attach later.
        for e,kind in getattr(rules,'sensitive_effects',{}).items():
            if kind not in ('credit','termination') or not inv.program_remaining():continue
            oid=rules.effects[e]['oid']
            if not any(inv.root(q)==oid and e in q['current'].get('_scope_effects',()) for q in inv.issues.values()):
                rules.create_consumer(oid,'AC',{e})
    for candidate in inv.f.source_candidates:
        oid=candidate['operation'];rules=inv.semantics.rules
        positions={(key(w['position']),key(w['source'])) for w in candidate['extra_effects']}
        wanted={e for e in rules.by_operation.get(oid,()) if 'cell' in rules.effects[e] and (key(rules.effects[e]['cell']),key(rules.effects[e]['where'])) in positions}
        # A single terminating effect with no writes needs no second host question when
        # the existing reading already addresses that exact source entry and policy.
        exit_locs={key(x['effect'].get('source')) for x in candidate['sensitive_exits']}
        wanted.update(e for e in rules.by_operation.get(oid,()) if rules.effects[e].get('kind')=='native_selfdestruct'
                      and key(rules.effects[e]['where']) in exit_locs)
        existing=[q for q in inv.issues.values() if inv.root(q)==oid and
                  wanted and set(q['current'].get('_scope_effects',()))==wanted]
        if existing:
            q=existing[0];q['host_source_candidate']=candidate
            inv.enqueue(q['id'],'inspect',{'operation':oid,'enhance':False},1,'inspect applied extra effect against the existing explanation')
        else:
            item={'id':'host_'+candidate['id'],'anchors':[inv.catalog.name(oid)],'assessment':'investigate',
                  'category':'AC' if inv.f.options.scope=='AC' else 'ADDITIONAL',
                  'claim':'The actual applied entry has a committed '+candidate['kind']+'. Determine the affected subject, authorization and asset, and whether the existing explanation covers this effect.',
                  '_host_source_question':True,'_scope_effects':sorted(wanted)}
            inv.accept({'issues':[item],'reviewed':[],'diagnostics':[],'usable_analysis':True},host_target=candidate['target'])
            q=inv.issues.get(item['id'])
            if q:q['host_source_candidate']=candidate
        inv.candidate_trace.append({**candidate,'question':q['id'] if q else None,
            'state':'queued' if q else 'unresolved_binding','generated_risk_claim':False})


def investigate_obligations(inv,report):
    """Give omitted semantic obligations a place in the existing follow-up.

    No extra session, risk label or gold-driven ordering. Shared object groups
    send one source question; unselected entries remain in the coverage ledger.
    """
    scope=report['task_analysis']['reading_scope'];created=[]
    rules=inv.semantics.rules
    for request in scope.get('refinement_requests',()):
        oid=request['operation'];category=request['category'];effects=set(request['effects'])
        if not effects or not inv.program_remaining():continue
        if any(inv.root(q)==oid and (q.get('property') or q['current']).get('category')==category and
               effects<=rules.route_scopes(q) for q in inv.issues.values()):continue
        q=rules.create_consumer(oid,category,effects)
        if not q:continue
        q['host_obligation_question']={'selected_operation':oid,'category':category,'other_entries_not_marked_complete':True}
        created.append(q['id'])
        inv.candidate_trace.append({'operation':oid,'target':inv.f.operations[oid]['target'],'question':q['id'],
            'kind':'unresolved_source_obligation','state':'queued','generated_risk_claim':False})
    return created
