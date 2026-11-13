"""One finite per-entry budget and measurable normalization work."""
from contextvars import ContextVar
active=ContextVar("source_operation_work",default=None)
from .effective_parameters import current
MAX_VISITS=current()["normalization_visits_per_operation_max"]
def begin():return active.set({"visits":0,"clean_calls":0,"shared_subtree_hits":0,"normalization_cache_hits":0,"max_expression_nodes":0,"max_depth":0})
def snapshot():return dict(active.get() or {})
def end(token):active.reset(token)
def metric(name,value=1,maximum=False):
    state=active.get()
    if state is not None:state[name]=max(state.get(name,0),value) if maximum else state.get(name,0)+value
def visit():
    state=active.get()
    if state is not None:
        state["visits"]+=1
        if state["visits"]>MAX_VISITS:raise ValueError("source_operation_normalization_bound_exceeded:"+str(MAX_VISITS))
