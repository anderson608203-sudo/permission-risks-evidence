"""Lossless graph-expression DAG for the LLM wire view only."""
import copy,json
from .core import digest, require

def compact(context):
    wire=copy.deepcopy(context);table={}
    def intern(value):
        if isinstance(value,dict):
            compacted={k:intern(v) for k,v in value.items()}
            if value.get('kind'):
                ref='g_'+digest(compacted)[:16]
                require(ref not in table or table[ref]==compacted,'WIRE_GRAPH_COLLISION')
                table[ref]=compacted
                return {'graph_ref':ref}
            return compacted
        return [intern(v) for v in value] if isinstance(value,list) else value
    for target in wire.get('targets',[]):
        target.pop('entry_identity_bindings',None)
        graph=target.get('graph',{})
        for edge in graph.get('edges',[]):
            for field in ('value','guard','predicate'):
                if field in edge:edge[field]=intern(edge[field])
    # Store repeated field names once while preserving every node/edge value
    # and original record order. Each row starts with its layout index.
    for target in wire.get('targets',[]):
        graph=target.get('graph',{})
        for field in ('nodes','edges'):
            values=graph.get(field,[]);layouts=[];rows=[]
            for value in values:
                fields=list(value)
                if fields not in layouts:layouts.append(fields)
                rows.append([layouts.index(fields)]+[value[k] for k in fields])
            graph[field]={'record_layouts':layouts,'rows':rows}
    # The same typed terms also repeat in paths, candidates and the e_*
    # registry. Share them across the entire wire payload, keeping IDs intact.
    for name in list(wire):
        if name not in ('sources','identity','task_request'):wire[name]=intern(wire[name])
    wire['graph_expression_table']=table
    # Repeated path issues/source records are not typed expressions. Intern
    # repeated sizeable structures separately; full roundtrip is verified.
    counts={};fingerprints={}
    def collect(value):
        if isinstance(value,(dict,list)):
            raw=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))
            ref='r_'+digest(value)[:16];fingerprints[id(value)]=(ref,len(raw.encode()))
            if len(raw.encode())>=128:counts[ref]=counts.get(ref,0)+1
            for child in value.values() if isinstance(value,dict) else value:collect(child)
    for name,value in wire.items():
        if name!='sources':collect(value)
    records={}
    def share(value):
        if not isinstance(value,(dict,list)):return value
        ref,size=fingerprints[id(value)]
        child={k:share(v) for k,v in value.items()} if isinstance(value,dict) else [share(v) for v in value]
        if size>=128 and counts.get(ref,0)>1:
            require(ref not in records or records[ref]==child,'WIRE_RECORD_COLLISION')
            records[ref]=child;return {'record_ref':ref}
        return child
    for name in list(wire):
        if name!='sources':wire[name]=share(wire[name])
    wire['shared_record_table']=records
    wire['wire_view']='lossless typed expression DAG across graphs, paths and e_* registry; graph_ref expands through graph_expression_table; record_ref expands through shared_record_table; graph nodes/edges use record_layouts and rows; row[0] selects its field-name layout. Full sources are verbatim. Proposals use sourced e_* expression IDs, never wire table IDs'
    return wire

def expand(wire):
    result=copy.deepcopy(wire);table=result.pop('graph_expression_table',{});records=result.pop('shared_record_table',{})
    def resolve(value, stack=()):
        if isinstance(value,dict):
            if set(value)=={'record_ref'}:
                ref=value['record_ref'];require(ref in records and ref not in stack,'WIRE_RECORD_REFERENCE')
                return resolve(records[ref],stack+(ref,))
            if set(value)=={'graph_ref'}:
                ref=value['graph_ref'];require(ref in table and ref not in stack,'WIRE_GRAPH_REFERENCE')
                return resolve(table[ref],stack+(ref,))
            return {k:resolve(v,stack) for k,v in value.items()}
        return [resolve(v,stack) for v in value] if isinstance(value,list) else value
    result=resolve(result)
    for target in result.get('targets',[]):
        for field in ('nodes','edges'):
            data=target.get('graph',{}).get(field)
            if isinstance(data,dict) and set(data)=={'record_layouts','rows'}:
                target['graph'][field]=[dict(zip(data['record_layouts'][row[0]],row[1:])) for row in data['rows']]
    return result
