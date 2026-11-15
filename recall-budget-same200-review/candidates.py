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
        if extra or exits:
            row={'operation':oid,'target':op['target'],'kind':'applied_extra_effect' if extra else 'independent_sensitive_exit',
                 'extra_effects':list({key(x):x for x in extra}.values()),'sensitive_exits':exits,
                 'candidate_requires_assessment':True,'not_counterevidence':True}
            row['id']='candidate_'+digest(row)[:16];result.append(row)
    return result


def investigate(inv):
    inv.candidate_trace=[]
    for candidate in inv.f.source_candidates:
        oid=candidate['operation'];rules=inv.semantics.rules
        positions={key(w['position']) for w in candidate['extra_effects']}
        wanted={e for e in rules.by_operation.get(oid,()) if 'cell' in rules.effects[e] and key(rules.effects[e]['cell']) in positions}
        # A single terminating effect with no writes needs no second host question when
        # the existing reading already addresses that exact source entry and policy.
        entry_rows=inv.f.summaries.rows(oid)
        sole_exit=bool(candidate['sensitive_exits'] and not candidate['extra_effects'] and
                       len({key(x['effect'].get('source')) for x in candidate['sensitive_exits']})==1 and
                       entry_rows and all(not row['ordered_writes'] and not row['residuals'] and len(row['effects'])<=1 for row in entry_rows))
        if sole_exit:wanted.update(e for e in rules.by_operation.get(oid,()) if rules.effects[e].get('kind')=='native_selfdestruct')
        existing=[q for q in inv.issues.values() if inv.root(q)==oid and
                  (wanted and wanted<=rules.route_scopes(q) or sole_exit and not q['current'].get('_scope_effects'))]
        if existing:
            q=existing[0];q['host_source_candidate']=candidate
            inv.enqueue(q['id'],'inspect',{'operation':oid,'enhance':False},1,'inspect applied extra effect against the existing explanation')
        else:
            item={'id':'host_'+candidate['id'],'anchors':[inv.catalog.name(oid)],'assessment':'investigate',
                  'category':'AC' if inv.f.options.scope=='AC' else 'ADDITIONAL',
                  'claim':'The actual applied entry has a committed '+candidate['kind']+'. Determine the affected subject, authorization and asset, and whether the existing explanation covers this effect.',
                  '_host_source_question':True}
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
