"""Immutable old evidence, with narrowly scoped checked replacement relations."""
import copy
from .core import digest,require


def validate_requests(response,base,extra,ordinary_rows=None):
    old={o['id']:o for o in base['source_obligations']}
    new={o['id']:o for o in extra['source_obligations']}
    old_queries={q['id']:q for q in ordinary_rows or []}
    raw=response.get('revisions',[]);accepted=[];errors=[];seen=set()
    if not isinstance(raw,list):return [],[{'reason':'REVISION_LIST_REQUIRED'}]
    for index,item in enumerate(raw):
        try:
            require(isinstance(item,dict),'REVISION_OBJECT')
            parent=item.get('parent_obligation_id');replacement=item.get('replacement_obligation_id')
            query_ids=item.get('parent_query_ids',[])
            require(replacement in new,'REVISION_REPLACEMENT_REFERENCE')
            require(bool(parent)!=bool(query_ids),'REVISION_ONE_PARENT_KIND')
            require(item.get('action') in ('replace','refute'),'REVISION_ACTION')
            require(isinstance(item.get('explanation'),str) and item['explanation'].strip(),'REVISION_EXPLANATION')
            b=new[replacement]
            if parent:
                require(parent in old and parent not in seen,'REVISION_REFERENCES')
                a=old[parent]
                require(all(a[k]==b[k] for k in ('identity','rule','target','function')),'REVISION_OPERATION_CHANGED')
                require(bool(set(a['source_ast_ids']) & set(b['source_ast_ids'])),'REVISION_SOURCE_SCOPE_CHANGED')
                prior_digest=a['proposal_sha256'];seen.add(parent)
            else:
                require(isinstance(query_ids,list) and query_ids and len(set(query_ids))==len(query_ids) and all(q in old_queries and q not in seen for q in query_ids),'REVISION_QUERY_REFERENCES')
                for qid in query_ids:
                    q=old_queries[qid]
                    require(all(q[k]==b[k] for k in ('rule','target','function')) and all(q[k]==b['identity'][k] for k in ('program_id','build_id')),'REVISION_QUERY_OPERATION_CHANGED')
                prior_digest=digest([old_queries[q] for q in query_ids]);seen.update(query_ids)
            accepted.append({**copy.deepcopy(item),'parent_proposal_sha256':prior_digest,
                'replacement_proposal_sha256':b['proposal_sha256'],'status':'pending_independent_check'})
        except (ValueError,TypeError,KeyError) as ex:errors.append({'index':index,'reason':str(ex),'original_preserved':True})
    return accepted,errors


def apply_checked(requests,obligations,ordinary_rows):
    """Only equal source domains/effects can supersede checked old evidence.

    New permissions may change, but not the original execution conditions or
    target effect. A narrower path cannot erase a finding on another path.
    Unsupported source-model replacements remain separate candidates.
    """
    obs={o['id']:o for o in obligations['source_obligations']}
    rows={r['id']:r for r in ordinary_rows+obligations.get('source_obligation_checks',[])}
    def linked(ob):return list(dict.fromkeys(ob.get('checks',[])+ob.get('legacy_bridge',{}).get('query_ids',[])))
    def domain(row):
        if row.get('source_model'):return None
        if not row.get('effect') or 'conditions' not in row:return None
        return digest({k:row.get(k) for k in ('program_id','build_id','target','function','rule','path_index','effect','conditions')})
    records=[]
    for requested in requests:
        record=copy.deepcopy(requested);records.append(record)
        parent=obs.get(record.get('parent_obligation_id'));replacement=obs[record['replacement_obligation_id']]
        prior=[rows[q] for q in (linked(parent) if parent else record['parent_query_ids']) if q in rows]
        current=[rows[q] for q in linked(replacement) if q in rows]
        record['original_query_ids']=[r['id'] for r in prior];record['replacement_query_ids']=[r['id'] for r in current]
        matches={}
        for before in prior:
            scope=domain(before)
            found=[after for after in current if scope is not None and domain(after)==scope
                and after.get('formal',{}).get('solver_called') is True
                and after.get('formal',{}).get('premise')=='sat'
                and after.get('status') in ('supported','refuted_in_scope') and not after.get('policy_assessment')
                and not any(a.get('assessment')=='query_blocking' for a in after.get('remark_assessments',[]))]
            if len(found)==1:matches[before['id']]=found[0]
        valid=bool(prior) and len(matches)==len(prior)
        if record['action']=='refute':valid=valid and all(r['status']=='refuted_in_scope' for r in matches.values())
        if not valid:
            record.update(status='not_admitted_original_preserved',reason='complete_same_domain_checked_replacement_missing');continue
        for before in prior:
            # The old formal result is retained verbatim; only final admission
            # records that its policy hypothesis has been explicitly replaced.
            before['historical_reportable']=before.get('reportable',False)
            before['reportable']=False;before['superseded_by']=matches[before['id']]['id']
        if parent:parent['superseded_by']=replacement['id']
        record.update(status='checked_replacement_admitted',scope='same source domain/effect, revised inferred policy; no unique-business-intent proof')
    return records
