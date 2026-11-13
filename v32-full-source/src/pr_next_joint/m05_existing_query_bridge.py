"""Validated source questions -> ordinary M3 queries; never copy verdicts."""
import copy
from .core import digest,require
from .m04_joint_context import SCHEMA
from .m04_joint_queries import bind
from .m04_joint_normalize import normalize_response
from .m05_relation_model_scope import check_slot

RULES=frozenset(('AC-01','AC-02','AC-03','AC-04','FCR-MINT'))

class SourceQueryBridge:
    def __init__(self):
        self.records={};self.ids={};self.links=[];self.gaps=[]
    def enqueue(self,obligations,context,state,queries,coverage,origin):
        for ob in obligations['source_obligations']:
            if ob['rule'] not in RULES:continue
            token=digest([ob['identity'],ob['id'],ob['proposal_sha256']])
            if token in self.records:
                ob['legacy_bridge']=copy.deepcopy(self.records[token]);continue
            route={'source_obligation_id':ob['id'],'source_proposal_sha256':ob['proposal_sha256'],
                'origin':copy.deepcopy(origin),'query_ids':[],'derived_proposal_ids':[],
                'status':'not_bound','gaps':[],'original_question_completed':False}
            try:
                require(ob['id'] not in self.ids,'SOURCE_BRIDGE_SOURCE_ID_CONFLICT')
                self.ids[ob['id']]=token
                require(ob.get('source_binding_status')=='source_anchors_bound' and ob['identity']==context['identity'],'SOURCE_BRIDGE_IDENTITY')
                p=ob['original_proposal'];require(digest(p)==ob['proposal_sha256'],'SOURCE_BRIDGE_PROPOSAL_IDENTITY')
                require(all(p.get(k)==ob[k] for k in ('target','function','rule')),'SOURCE_BRIDGE_OPERATION_IDENTITY')
                lookup=state['lookups'][ob['target']]
                require(all(lookup.bundle[k]==context['identity'][k] for k in ('program_id','build_id')),'SOURCE_BRIDGE_BUILD_IDENTITY')
                decision=p.get('policy_decision')
                if ob['rule']=='FCR-MINT' and decision is None and ob.get('review_kind') in ('risk_hypothesis','normal_review'):
                    decision='endorse'
                    route['decision_basis']='M2_requests_source_asset_model_check; not an inferred AC permission'
                require(decision in ('endorse','revise','reject','uncertain'),'SOURCE_BRIDGE_POLICY_DECISION_REQUIRED')
                basis=copy.deepcopy(p.get('basis'))
                require(isinstance(basis,dict),'SOURCE_BRIDGE_POLICY_BASIS_REQUIRED')
                basis.setdefault('source_ast_ids',copy.deepcopy(ob['source_ast_ids']))
                candidate=p.get('candidate_id');write=p.get('write_id');sensitive=p.get('effect_id')
                require(all(v is None or isinstance(v,str) and bool(v.strip()) for v in (candidate,write,sensitive)),'SOURCE_BRIDGE_INVALID_REFERENCE')
                require(sum(bool(v) for v in (candidate,write,sensitive))<=1,'SOURCE_BRIDGE_ONE_REFERENCE_REQUIRED')
                if not candidate and not write and not sensitive and ob['rule'] in ('AC-04','FCR-MINT'):
                    from .m05_source_model_planner import materialize
                    route['source_planned_binding_refs']=materialize(ob,state)
                refs=[candidate or write or sensitive] if candidate or write or sensitive else [ref for ref,item in state['bindings'].items()
                    if item.get('target')==ob['target'] and item.get('function',item.get('row',{}).get('function'))==ob['function']
                    and ('row' in item and item['row'].get('rule')==ob['rule'] if ob['rule'] in ('AC-04','FCR-MINT') else 'write' in item or ob['rule']=='AC-01' and 'sensitive_effect' in item)]
                if not candidate and ob['rule'] in ('AC-01','AC-02','AC-03'):
                    require(p.get('required') is not None or decision in ('reject','uncertain') and bool(write or sensitive),'SOURCE_BRIDGE_REQUIRED_POLICY_NOT_BOUND')
                matched=0
                for ref in refs:
                    try:
                        item=state['bindings'].get(ref)
                        require(isinstance(item,dict),'SOURCE_BRIDGE_UNKNOWN_REFERENCE')
                        fn=item.get('function',item.get('row',{}).get('function'))
                        require((item.get('target'),fn)==(ob['target'],ob['function']),'SOURCE_BRIDGE_REFERENCE_OPERATION')
                        is_candidate=bool(candidate) or ob['rule'] in ('AC-04','FCR-MINT') and 'row' in item
                        if is_candidate:
                            row=item.get('row',{});require(row.get('rule')==ob['rule'],'SOURCE_BRIDGE_REFERENCE_RULE')
                            effect=copy.deepcopy(row['effect']);w={'path':effect['selector'],'value':effect['value'],'operator':effect['operator'],'source':effect['source']}
                        elif 'sensitive_effect' in item:
                            require(ob['rule']=='AC-01','SOURCE_BRIDGE_NONSTORAGE_RULE')
                            effect=copy.deepcopy(item['sensitive_effect']);w={'source':effect['source'],'path':{'kind':'non_storage_effect','source_id':effect['source']['ast_id']}}
                        else:
                            w=copy.deepcopy(item['write']);effect={'selector':w['path'],'value':w['value'],'operator':w['operator'],'source':w['source']}
                        resource=check_slot(ob,lookup,'resources',[effect,w['path']],[w])
                        if not candidate and not write and not sensitive:
                            require(w['source']['ast_id'] in ob['source_ast_ids'] or w['path'].get('root') in ob['source_ast_ids'] or bool(resource['evidence']),'SOURCE_BRIDGE_EFFECT_NOT_ANCHORED')
                        kind='candidate_id' if is_candidate else 'effect_id' if 'sensitive_effect' in item else 'write_id'
                        proposal={k:copy.deepcopy(p.get(k)) for k in ('rule','target','function','policy_decision','required','rationale','alternatives','unresolved')}
                        proposal.update({kind:ref,'basis':basis,'policy_decision':decision})
                        proposal['id']='source_bridge_'+digest([token,kind,ref,proposal])
                        envelope={'schema':SCHEMA,'identity':context['identity'],'proposals':[proposal],'coverage':[]}
                        normalized,conversion=normalize_response(envelope,context,state,authenticated=False)
                        bound,part=bind(normalized,context,state)
                        coverage['proposal_binding_errors'].extend(part['proposal_binding_errors'])
                        coverage['policy_decisions'].extend(part['policy_decisions'])
                        relation_scopes=[]
                        for q in bound:
                            # Only typed, selected rule-model inputs. Never let
                            # retained LLM remarks/basis prose self-attest refs.
                            selected={k:q[k] for k in ('conditions','required_policy_candidate','effect','policy_basis','supply_effects') if k in q}
                            relation_scopes.append({'query_id':q['id'],'selected_input_fields':sorted(selected),'slots':[check_slot(ob,lookup,slot,selected,[w]) for slot in ('participants','credential','consent','control','amount')]})
                        proof={'derived_proposal_id':proposal['id'],'source_obligation_id':ob['id'],
                            'source_proposal_sha256':ob['proposal_sha256'],'origin':copy.deepcopy(origin),
                            'identity':copy.deepcopy(context['identity']),'target':ob['target'],'function':ob['function'],'rule':ob['rule'],
                            'binding_kind':kind,'binding_ref':ref,'effect':effect,'resource_match':resource,
                            'original_policy_decision':decision,'original_required':copy.deepcopy(p.get('required')),
                            'relation_binding_sha256':digest(ob.get('relation_binding',{})),
                            'binding_model_sha256':digest(item.get('row',item.get('write',item.get('sensitive_effect')))),
                            'relation_scope_consumption':relation_scopes,
                            'conversion':conversion,'binding_errors':part['proposal_binding_errors'],
                            'query_ids':[q['id'] for q in bound],
                            'scope':'ordinary source-bound conditional query; original natural-language question remains unresolved'}
                        self.links.append(proof);matched+=1
                        route['derived_proposal_ids'].append(proposal['id'])
                        route['query_ids'] += proof['query_ids']
                        route['gaps'] += part['proposal_binding_errors']
                        existing={q['id'] for q in queries}
                        queries.extend(q for q in bound if q['id'] not in existing)
                    except (ValueError,KeyError,TypeError) as ex:
                        route['gaps'].append({'binding_ref':ref,'reason':str(ex)})
                require(matched>0,'SOURCE_BRIDGE_NO_MATCHED_EFFECT')
                route['status']='bound_pending_ordinary_M4' if route['query_ids'] else 'policy_review_without_query' if decision in ('reject','uncertain') else 'not_bound'
            except (ValueError,KeyError,TypeError) as ex:route['gaps'].append({'reason':str(ex)})
            self.records[token]=copy.deepcopy(route);ob['legacy_bridge']=route
            self.gaps.extend({'source_obligation_id':ob['id'],**g} for g in route['gaps'])
    def report(self,rows):
        actual={r['id']:r for r in rows}
        links=copy.deepcopy(self.links)
        for link in links:
            link['query_execution']=[{'query_id':qid,'solver_called':actual[qid]['formal'].get('solver_called'),
                'status':actual[qid]['status'],'reportable':actual[qid].get('reportable',False)} for qid in link['query_ids'] if qid in actual]
        ids={qid for link in links for qid in link['query_ids']}
        return {'schema':'source-to-ordinary-query-bridge-v1','derivations':links,'gaps':copy.deepcopy(self.gaps),
            'bound_queries':len(ids),'formal_checks_called':sum(bool(actual[q]['formal'].get('solver_called')) for q in ids if q in actual),
            'scope':'queries also counted in ordinary results; never add these counts a second time'}
