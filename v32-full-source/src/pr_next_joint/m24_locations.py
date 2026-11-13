"""Report source-supported root locations alongside the affected entry.
No label/reference is used and no two distinct roots are merged here.
"""
from .m03_p_paths import walk,key
def root_locations(finding,checks,lookup):
    refs=set(finding['evidence_query_ids']);out=[]
    selected=[q for q in checks if q['id'] in refs]
    for q in selected:
        basis=q.get('policy_basis',{})
        out.append({'role':'sensitive_effect','source':q.get('effect',{}).get('source') or q.get('source'),'entry':q['function']})
        for node in walk(basis):
            if set(('file','start','length','ast_id'))<=set(node):
                if node['ast_id'] in lookup.nodes:out.append({'role':'supporting_source_evidence','source':node})
        # tx.origin mistakes reside in a guard/modifier even when that guard
        # reaches several affected functions. Only an actually queried origin
        # comparison is listed; this does not invent a new constructor finding.
        if any(n.get('kind')=='transaction_origin' for n in walk(q.get('conditions',[]))):
            fn=lookup.function(q['function']) or {}
            declarations=[fn]
            for m in fn.get('modifiers',[]):
                d=lookup.nodes.get(m.get('modifierName',{}).get('referencedDeclaration'))
                if d:declarations.append(d)
            for d in declarations:
                for n in walk(d.get('body',{})):
                    if n.get('nodeType')=='BinaryOperation' and n.get('operator') in ('==','!=') and any(x.get('nodeType')=='MemberAccess' and x.get('memberName')=='origin' and x.get('expression',{}).get('name')=='tx' for x in walk(n)):
                        out.append({'role':'authorization_origin_condition','source':lookup.anchor(n),'declaration':lookup.anchor(d),'declaration_name':d.get('name'),'entry':q['function']})
    return list({key(x):x for x in out if x.get('source')}.values())
