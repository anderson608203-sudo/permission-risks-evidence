"""Per-analysis finite solver budget; UNKNOWN never becomes refutation."""
import time
from contextlib import contextmanager
from contextvars import ContextVar
_current=ContextVar('v20_solver_budget',default=None)

@contextmanager
def budget(seconds=120.0):
    state={'limit_seconds':float(seconds),'used_seconds':0.0,'calls':0,'upgrades':0,'budget_exhausted':0,'events':[]}
    token=_current.set(state)
    try:yield state
    finally:_current.reset(token)

def solve(solver,initial_ms=3000,upgrade=False):
    import z3
    b=_current.get()
    remaining=lambda: max(0,int((b['limit_seconds']-b['used_seconds'])*1000)) if b else initial_ms+10000
    if remaining()<1:
        if b:b['budget_exhausted']+=1
        return z3.unknown
    limit=min(initial_ms,remaining())
    solver.set(timeout=limit,random_seed=0)
    start=time.perf_counter();answer=solver.check();elapsed=time.perf_counter()-start
    if b:b['used_seconds']+=elapsed;b['calls']+=1
    reason=solver.reason_unknown() if answer==z3.unknown else None
    if upgrade and answer==z3.unknown and reason and any(w in reason.lower() for w in ('timeout','canceled')) and remaining()>0:
        limit=min(10000,remaining());solver.set(timeout=limit)
        start=time.perf_counter();answer=solver.check();elapsed2=time.perf_counter()-start
        if b:b['used_seconds']+=elapsed2;b['calls']+=1;b['upgrades']+=1
        if b:b['events'].append({'kind':'bounded_timeout_upgrade','first_seconds':elapsed,'additional_seconds':elapsed2,'answer':str(answer)})
    return answer

def status():
    b=_current.get()
    return dict(b) if b else {'scope':'no_active_analysis_budget'}
