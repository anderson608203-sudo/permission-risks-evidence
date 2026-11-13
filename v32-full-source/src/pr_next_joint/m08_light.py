"""M1 compiler-bound lightweight operations; no path expansion or labels."""
import copy,json
from .core import digest,require
from .source_paths import SourcePaths
from .source_entry_identity import entry_functions
from .m04_project import target_inventory
from .facts import walk

SCHEMA="joint-task-relations-v20"
RELATIONS=("controlled_by","holder_of","delegates_to","checks_permission",
           "credits_from_deposit","debits_for_redemption","guards_transfer","credential_binds")

def build(bundle,native,sources,selected_targets,scope,description=None):
    require(scope in ("AC","FCR"),"V9_EXPLICIT_SCOPE")
    require(all(bundle[k]==native[k] for k in ("program_id","build_id")),"V9_INPUT_IDENTITY")
    require(bundle.get("native_ir",{}).get("sha256")==digest(native),"V9_NATIVE_IDENTITY")
    inventory=target_inventory(bundle);available={x["file"]+":"+x["contract"] for x in inventory if x["selected"]}
    chosen=set(selected_targets) if selected_targets is not None else available
    require(bool(chosen) and chosen<=available,"V9_TARGET_SELECTION")
    for item in inventory:
        item["selected"]=item["file"]+":"+item["contract"] in chosen
    aliases={t:i for i,t in enumerate(sorted(chosen))}
    refkey=lambda t,n:"n"+str(aliases[t])+"_"+str(n)
    ops=[];lookups={};references={};edges=[];nodes={}
    for contract in bundle["contracts"]:
        tid=contract["file"]+":"+contract["name"]
        if tid not in chosen:continue
        lookup=SourcePaths(bundle,contract);lookups[tid]=lookup
        for f in entry_functions(lookup):
            fn=f["signature"];body=lookup.function(fn)
            require(body is not None,"V9_ENTRY_IDENTITY:"+tid+":"+fn)
            if "generated_getter" in body:body=body["generated_getter"]
            reachable=set();pending=[body];calls=[]
            while pending:
                n=pending.pop()
                if n.get("id") in reachable:continue
                if n.get("id") is not None:reachable.add(n["id"])
                for child in walk(n):
                    if child.get("id") is not None:reachable.add(child["id"])
                    ref=child.get("referencedDeclaration")
                    if child.get('nodeType')=='FunctionCall' and child.get('expression',{}).get('nodeType')=='Identifier':
                        from .m10_dispatch import resolve
                        original=lookup.fns.get(child['expression'].get('referencedDeclaration'))
                        selected=resolve(lookup,original)
                        if selected is not None:ref=selected['id']
                    if ref in lookup.fns and ref not in reachable:
                        pending.append(lookup.fns[ref]);calls.append(ref)
                for mod in n.get("modifiers",[]):
                    ref=mod.get("modifierName",{}).get("referencedDeclaration")
                    if ref in lookup.fns and ref not in reachable:pending.append(lookup.fns[ref])
            oid="op_"+digest([tid,fn])[:20]
            writes=[];conditions=[];effects=[]
            for nid in sorted(reachable):
                n=lookup.nodes.get(nid,{})
                typ=n.get("nodeType")
                if typ=="Assignment" or typ=="UnaryOperation" and n.get("operator") in ("++","--","delete"):writes.append(nid)
                if typ in ("IfStatement","Conditional"):conditions.append(nid)
                if typ=="FunctionCall":effects.append(nid)
                for ref in [n.get("referencedDeclaration")]:
                    if ref in lookup.decls:reachable_declaration=lookup.decls[ref];nodes[(tid,ref)]=reachable_declaration
                nodes[(tid,nid)]=n
            op={"id":oid,"target":tid,"function":fn,"entry_ast_id":body["id"],
                "source":lookup.anchor(body),"source_ast_ids":sorted(reachable),
                "write_ast_ids":writes,"call_ast_ids":effects,"condition_ast_ids":conditions,
                "internal_call_ids":sorted(set(calls)),"generated_getter":body.get("nodeType")=="VariableDeclaration"}
            # Source-shape hints prioritize relationship review without making
            # an authorization/risk decision or omitting read-only context.
            focus=set();state_refs=set()
            for nid in writes:
                node=lookup.nodes[nid];left=node.get('leftHandSide',node.get('subExpression',{}))
                roots={x.get('referencedDeclaration') for x in walk(left) if lookup.nodes.get(x.get('referencedDeclaration'),{}).get('stateVariable')}
                if not roots:continue
                state_refs.update(refkey(tid,r) for r in roots)
                indexed=any(x.get('nodeType')=='IndexAccess' for x in walk(left))
                focus.add('indexed_state_update' if indexed else 'scalar_state_replacement' if node.get('operator')=='=' else 'scalar_state_update')
            if effects:focus.add('source_call_relationships')
            op['relationship_review_focus']=sorted(focus)
            op['affected_state_refs']=sorted(state_refs)
            ops.append(op)
            edges += [{"from":oid,"to":refkey(tid,i),"kind":"calls"} for i in set(calls)]
            edges += [{"from":oid,"to":refkey(tid,i),"kind":"writes"} for i in writes]
    for (tid,nid),n in nodes.items():
        if n.get("nodeType") not in ("VariableDeclaration","FunctionDefinition","ModifierDefinition",
             "Assignment","UnaryOperation","FunctionCall","IfStatement","BinaryOperation","IndexAccess","MemberAccess","Conditional"):continue
        references[refkey(tid,nid)]={"target":tid,"ast_id":nid,"kind":n.get("nodeType"),
            "name":n.get("name",n.get("memberName")),"source":lookups[tid].anchor(n)}
    # Source-level dependency edges are navigation facts, not authorization proofs.
    for operation in ops:
        tid=operation['target'];lookup=lookups[tid]
        for nid in operation['source_ast_ids']:
            node=lookup.nodes.get(nid,{})
            if node.get('nodeType') not in ('Assignment','VariableDeclarationStatement'):continue
            lhs=node.get('leftHandSide')
            destinations=([lhs.get('referencedDeclaration') if lhs.get('nodeType')=='Identifier' else lhs.get('id')] if lhs else [x['id'] for x in node.get('declarations',[]) if x])
            rhs=node.get('rightHandSide',node.get('initialValue'))
            origins={x.get('referencedDeclaration') for x in walk(rhs) if lookup.nodes.get(x.get('referencedDeclaration'),{}).get('nodeType')=='VariableDeclaration'}
            for destination in destinations:
                for origin in origins:
                    a=refkey(tid,origin);b=refkey(tid,destination)
                    if a in references and b in references:
                        edges.append({'from':a,'to':b,'kind':'source_assignment_dependency','operation':operation['id'],
                                      'source':lookup.anchor(node),'not_path_or_authorization_proof':True})
    ops.sort(key=lambda o:(not bool(o['affected_state_refs']),not bool(o['call_ast_ids']),o['target'],o['function']))
    ctx={"schema":SCHEMA,"identity":{k:bundle[k] for k in ("program_id","build_id")},
        "analysis_scope":scope,"sources":sources,"normal_project_description":description,
        "operations":ops,"references":references,"graph":{"nodes":list(references),"edges":edges},
        "relation_kinds":list(RELATIONS),"reference_targets":{"n"+str(i):t for t,i in aliases.items()}}
    from .m20_graph import light_tasks
    ctx["permission_equity_tasks"]=light_tasks(ctx,lookups)
    from .m30_compare import contexts as reverse_effects
    reverse_effects(ctx["permission_equity_tasks"],ctx["operations"])
    return ctx,{"lookups":lookups,"target_inventory":inventory,"selected_targets":sorted(chosen),"bundle":bundle,"native":native}

def messages(context, *, include_task_graph=True):
    from .m28_prompt import instruction as build_instruction
    from .m30_questions import prompt as behavior_prompt
    instruction=build_instruction(context["analysis_scope"],SCHEMA)+behavior_prompt(context["analysis_scope"])
    wire=copy.deepcopy(context)
    if not include_task_graph:
        wire.pop('permission_equity_tasks',None)
    for operation in wire["operations"]:
        operation.pop("source_ast_ids",None)
    wire["graph"].pop("nodes",None)
    wire['graph']['edges']=list({digest(edge):edge for edge in wire['graph']['edges']}.values())
    for ref in wire["references"].values():
        ref.pop("target",None)
        ref.pop("ast_id",None)
        ref["source"].pop("ast_id",None)
    plain=copy.deepcopy(wire);anchors={};byvalue={};counts={}
    records=wire["operations"]+list(wire["references"].values())
    for record in records:
        if "source" in record:
            signature=digest(record["source"]);counts[signature]=counts.get(signature,0)+1
    for record in records:
        if "source" not in record:continue
        signature=digest(record["source"])
        if counts[signature]<2:continue
        value=record.pop("source")
        if signature not in byvalue:
            ident="a"+str(len(anchors));byvalue[signature]=ident;anchors[ident]=value
        record["anchor_ref"]=byvalue[signature]
    if anchors:wire["source_anchors"]=anchors
    size=lambda value:len(json.dumps(value,ensure_ascii=False,separators=(",",":")).encode("utf8"))
    if size(wire)>=size(plain):wire=plain
    compact=copy.deepcopy(wire)
    rows=[]
    for ref,r in compact['references'].items():
        assert set(r) in ({'kind','name','source'},{'kind','name','anchor_ref'})
        rows.append([ref,r['kind'],r['name'],r['source'] if 'source' in r else r['anchor_ref']])
    compact['reference_table']={'columns':['ref','kind','name','location'],'rows':rows}
    del compact['references']
    if size(compact)<size(wire):wire=compact
    transport=copy.deepcopy(wire)
    graph=transport['graph'];edge_rows=[];locations=[];location_ids={}
    for edge in graph.pop('edges'):
        source=edge.get('source');location=None
        if source is not None:
            signature=digest(source)
            if signature not in location_ids:
                location_ids[signature]=len(locations);locations.append(source)
            location=location_ids[signature]
        edge_rows.append([edge['from'],edge['to'],edge['kind'],edge.get('operation'),location])
    graph['edge_table']={'columns':['from','to','kind','operation','source_location_index'],'rows':edge_rows}
    graph['source_locations']=locations
    graph['assignment_edges_are_navigation_not_permission_proof']=True
    if size(transport)<size(wire):wire=transport
    # Lossless transport only: IDs, source anchors and all operation facts are
    # retained. Use a table only when all rows have the identical field set.
    operations=wire.get('operations',[])
    if operations and all(set(x)==set(operations[0]) for x in operations):
        columns=list(operations[0]);transport=copy.deepcopy(wire)
        transport['operation_table']={'columns':columns,'rows':[[x[c] for c in columns] for x in operations]}
        del transport['operations']
        explanation='\nIf operation_table is present, reconstruct each operation by pairing its columns with the row values; every original ID and field is retained. References to operations refer to these same records.\n'
        if size(transport)+len(explanation.encode('utf8'))<size(wire):
            wire=transport;instruction+=explanation
    return [{"role":"system","content":instruction},{"role":"user","content":json.dumps(wire,ensure_ascii=False,separators=(",",":"))}]
