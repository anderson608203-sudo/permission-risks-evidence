"""Keep child preparation/verification failures when aggregating M03 results."""
import copy

def completed_rows(rows):
    return sum(r.get('execution_status')=='completed' for r in rows)

def aggregate(children, metadata=None):
    rows=[];leads=[];unresolved=[];failures=[];reports=[]
    for index, child in enumerate(children):
        rows.extend(copy.deepcopy(child.get('rows',[])))
        leads.extend(copy.deepcopy(child.get('leads',[])))
        unresolved.extend(copy.deepcopy(child.get('unresolved',[])))
        if child.get('report'):reports.append({'child':index,'path':child['report']})
        if child.get('status')!='completed' or not completed_rows(child.get('rows',[])):
            failures.append({'child':index,'status':child.get('status','missing_status'),
                             'reason':child.get('reason'),'leads':copy.deepcopy(child.get('leads',[]))})
        failures.extend({'child':index,'detail':copy.deepcopy(x)} for x in child.get('failures',[]))
    count=completed_rows(rows)
    status='no_completed_rows' if not count else 'partial_completed' if failures or leads or count!=len(rows) else 'completed'
    return {**copy.deepcopy(metadata or {}),'status':status,'rows':rows,'leads':leads,'unresolved':unresolved,
            'failures':failures,'reports':reports,'completed_rows':count,'inferred':True}
