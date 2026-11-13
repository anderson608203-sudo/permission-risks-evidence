"""Source-reference resolution, scoped by target and compiler declaration IDs.

Call and shared-storage edges justify locating related source, not substituting
callers, keys or instances. Semantic consumers must reconstruct those separately.
No model prose is interpreted as a graph edge.
"""
import networkx as nx
from .core import digest
from .m03_p_paths import walk


class SourceGraph:
    def __init__(self, lookup):
        self.lookup=lookup
        self.graph=nx.Graph()
        self.owners={}
        bases=set(lookup.contract_node.get('linearizedBaseContracts',[lookup.contract_node['id']]))
        # solc does not attach `scope` to every ModifierDefinition. Ownership
        # comes from the AST parent contract, not a missing optional field.
        member_ids={n['id'] for b in bases for n in lookup.nodes.get(b,{}).get('nodes',[]) if 'id' in n}
        declarations=[n for n in lookup.nodes.values() if n.get('id') in member_ids and
                      n.get('nodeType') in ('FunctionDefinition','ModifierDefinition')]
        callable_ids={n['id'] for n in declarations}
        states={n['id'] for n in lookup.nodes.values() if n.get('stateVariable') and n.get('scope') in bases}
        for f in declarations:
            fid=f['id'];self.graph.add_node(fid,kind=f['nodeType'])
            for n in walk(f):
                if type(n.get('id')) is int:self.owners.setdefault(n['id'],set()).add(fid)
                ref=n.get('referencedDeclaration')
                if ref in states:
                    self.graph.add_node(ref,kind='state')
                    self.graph.add_edge(fid,ref,relation='references_state')
                target=lookup.nodes.get(ref,{})
                # Referenced struct fields, enum values and constants are source
                # declarations too. Bind only declarations actually referenced
                # from this target's function, not every ID in the compilation.
                if (type(ref) is int and ref >= 0 and target.get('nodeType') in
                        ('VariableDeclaration','EnumValue','StructDefinition','EnumDefinition')):
                    self.owners.setdefault(ref,set()).add(fid)
                    for child in walk(target.get('typeName',{})):
                        if type(child.get('id')) is int:self.owners.setdefault(child['id'],set()).add(fid)
                        tr=child.get('referencedDeclaration')
                        if tr in lookup.nodes:
                            self.owners.setdefault(tr,set()).add(fid)
                if ref in callable_ids:
                    self.graph.add_edge(fid,ref,relation='compiler_resolved_call_or_modifier')
        for sid in states:
            self.owners.setdefault(sid,set()).add(sid)
            self.graph.add_node(sid,kind='state')

    def scope(self, signature):
        entry=self.lookup.function(signature)
        start=entry.get('id') or entry.get('generated_getter',{}).get('id')
        allowed=set();proofs=[]
        if start not in self.graph:return allowed,{'engine':'NetworkX','relations':[]}
        # Internal calls can span multiple nodes; shared-state connections only
        # locate peer declarations. No shared state is treated as key equality.
        from collections import deque
        distance={start:[start]};pending=deque([start]);omitted=set()
        while pending:
            current=pending.popleft()
            for nxt in sorted(self.graph.neighbors(current)):
                if nxt in distance:continue
                if len(distance)>=4096:omitted.add(nxt);continue
                distance[nxt]=distance[current]+[nxt];pending.append(nxt)
        for aid,owners in sorted(self.owners.items()):
            candidates=[distance[o] for o in owners if o in distance]
            if not candidates:continue
            route=min(candidates,key=lambda p:(len(p),p));allowed.add(aid)
            if len(route)>1:
                proofs.append({'source_ast_id':aid,'declaration_path':route,
                               'relations':[self.graph.edges[a,b]['relation'] for a,b in zip(route,route[1:])]})
        data={'engine':'NetworkX','target_contract_ast_id':self.lookup.contract_node['id'],
              'entry_ast_id':start,'relations':proofs,'closure_complete':not omitted,'unvisited_boundary':sorted(omitted),
              'scope':'same target/inheritance; source locations only; no instance/key/permission equivalence'}
        data['graph_binding_sha256']=digest(data)
        return allowed,data
