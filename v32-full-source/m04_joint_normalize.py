"""Lossless protocol repair AFTER authentic request/response verification.

No model verdict, scientific policy, or unknown identity is supplied here.
Every conversion is recorded separately from the immutable original response.
"""
import copy
from .core import require,digest
from .m03_p_paths import key,normalize
from .m04_joint_context import SCHEMA,resolve
from .m04_joint_protocol import bind_envelope,route_response

def same_effect(candidate,write):
    if 'row' not in candidate or 'write' not in write:return False
    row=candidate['row'];w=write['write'];e=row['effect']
    return (candidate['target']==write['target'] and row['function']==write['function']
        and row['path_index']==write['path_index']
        and all(key(e[a])==key(w[b]) for a,b in [('selector','path'),('value','value'),('operator','operator'),('source','source')]))

def normalize_response(raw,context,state,authenticated=False):
    require(isinstance(raw,dict),'JOINT_RESPONSE_OBJECT')
    response,envelope=bind_envelope(raw,{'schema':SCHEMA,'identity':context['identity']},authenticated)
    records=envelope['records']
    # Display aliases are accepted only when compiler kind and the selected
    # target identify exactly the same special entry. Never guess a source ID.
    for channel in ('coverage','proposals','source_obligations'):
        for item in response.get(channel,[]):
            if not isinstance(item,dict):continue
            lookup=state['lookups'].get(item.get('target'));name=item.get('function')
            if lookup is None or name in lookup.abi:continue
            if name not in ('()','fallback','receive'):continue
            kind='receive' if name=='receive' else 'fallback'
            node=lookup.entry_identity.special(kind)
            if node is None:continue
            canonical=kind+'()'
            if canonical not in {f['function'] for t in context['targets'] if t['id']==item['target'] for f in t['functions']}:continue
            item['function']=canonical
            records.append({'channel':channel,'item_id':item.get('id'),'conversion':'compiler_special_entry_alias',
                'original_function':name,'canonical_function':canonical,'source_ast_id':node['id']})
    # Keep a source question analyzable when an LLM uses an extra impact
    # label. Preserve text and original label; default conservatively to a
    # blocking concern, never guess that it is unrelated or prove it absent.
    for channel in ('proposals','source_obligations'):
        for item in response.get(channel,[]):
            if not isinstance(item,dict):continue
            for remark in item.get('unresolved',[]) if isinstance(item.get('unresolved',[]),list) else []:
                if isinstance(remark,dict) and isinstance(remark.get('impact'),str) and remark['impact'] not in ('query_blocking','policy_scope','unrelated'):
                    prior=remark['impact'];remark['impact']='query_blocking'
                    records.append({'channel':channel,'item_id':item.get('id'),'conversion':'unrecognized_impact_retained_as_blocking',
                        'original_impact':prior,'text':remark.get('text'),'semantic_resolution':False})
    require(isinstance(response.get('proposals'),list),'JOINT_RESPONSE_LISTS')
    for p in response['proposals']:
        if not isinstance(p,dict):continue
        def references(value,path):
            # Some genuine model responses use a bare ID where the requested
            # schema wraps it in {ref: ID}. Resolve only an exact sourced ID;
            # a natural-language formula or an unknown ID is never invented.
            if isinstance(value,str) and value in state['terms']:
                records.append({'proposal_id':p.get('id'),'field':path,
                                'conversion':'bare_existing_expression_reference','reference':value})
                return {'ref':value}
            if isinstance(value,dict):
                out=copy.deepcopy(value)
                if isinstance(out.get('args'),list):out['args']=[references(x,path+'.args.'+str(i)) for i,x in enumerate(out['args'])]
                if isinstance(out.get('substitute'),dict):out['substitute']={k:references(x,path+'.substitute.'+k) for k,x in out['substitute'].items()}
                return out
            return value
        if p.get('required') is not None:p['required']=references(p['required'],'required')
        c,w=p.get('candidate_id'),p.get('write_id')
        if isinstance(c,str) and isinstance(w,str) and c in state['bindings'] and w in state['bindings'] and same_effect(state['bindings'][c],state['bindings'][w]):
            p['write_id']=None
            records.append({'proposal_id':p.get('id'),'conversion':'equivalent_source_effect_references','candidate_id':c,'write_id':w})
        if (not context.get('protocol_revision') and isinstance(c,str) and c in state['bindings']
                and p.get('rule') in ('AC-04','FCR-MINT') and p.get('required') is not None):
            item=state['bindings'][c]
            try:
                if key(normalize(resolve(p['required'],state,item)))==key(normalize(item['row']['required_policy_candidate'])):
                    records.append({'proposal_id':p.get('id'),'conversion':'explicit_required_equals_source_model','required':p['required']})
                    p['required']=None
            except Exception:pass # Bind reports an actual error; never drops the proposal.
    if 'source_function_anchors' in context:
        response,routing=route_response(response,state)
    else:routing={'records':[],'errors':[]}
    return response,{'schema':'m04-typed-conversion-v2','raw_sha256':digest(raw),'normalized_sha256':digest(response),
                     'authenticated_request':authenticated,'records':records,'routing':routing}
