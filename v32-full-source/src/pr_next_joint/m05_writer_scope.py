"""Dependency isolation for incomplete writer scans, conservative on calls."""
from .m03_p_paths import walk


def affected_roots(lookup,function):
    from .operation_scope import source_operation
    facts=source_operation(lookup,function)
    if not facts.get('complete'):return None
    return set(facts.get('writes',[]))


def gaps_for(lookup,roots):
    result=[]
    for gap in getattr(lookup,'writer_scan_gaps',[]):
        affected=affected_roots(lookup,gap.get('function'))
        if affected is None or affected & set(roots):result.append(gap)
    return result
