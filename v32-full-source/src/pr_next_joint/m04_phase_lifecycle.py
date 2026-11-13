"""Conditional phase-scoped credentials from an issuer and controlled phase exit."""
import copy
from .core import digest
from .m03_p_paths import key,walk,op,lit,normalize,conditions_possible

def analyze_phases(bundle,lookup,program,requested):
 from .m03_p_route import selectors,keys,value_type,effective_permission
 models=[];rows=[]
 for fn,paths in program.items():
  for path in paths:
   if path['flow']=='reverted' or path['issues']:continue
   issuer=effective_permission(path['guards'],lookup)
   if not issuer:continue
   for guard in path['guards']:
    for condition in walk(normalize(guard)):
     if condition.get('kind')!='op' or condition['op']!='==':continue
     for phase,value in (condition['args'],condition['args'][::-1]):
      if phase.get('kind')!='storage' or phase.get('segments') or not str(value_type(phase,lookup)).startswith('enum '):continue
      if value.get('kind')!='literal' or type(value.get('value')) is not int:continue
      if conditions_possible(path['guards'],condition):continue
      for grant in path['writes']:
       if grant['value']!=lit(True) or value_type(grant['path'],lookup)!='bool' or len(keys(grant['path']))!=1:continue
       subject=keys(grant['path'])[0]
       if subject.get('kind')!='parameter' or subject.get('type')!='address':continue
       for transition,other_paths in program.items():
        for other in other_paths:
         if other['flow']=='reverted' or other['issues'] or conditions_possible(other['guards'],condition):continue
         if not set(map(key,issuer))&set(map(key,effective_permission(other['guards'],lookup))):continue
         for write in other['writes']:
          if key(write['path'])!=key(phase) or write['value'].get('kind')!='literal' or write['value']==value:continue
          if any(w['path']['root']==grant['path']['root'] for w in other['writes']):continue
          models.append({'kind':'credential_issued_in_controlled_phase','issuance_function':fn,'grant':grant,'phase':phase,'valid_phase':value,
           'management_permissions':issuer,'transition':{'function':transition,'source':write['source'],'to':write['value']}})
 for fn,paths in program.items():
  for pi,path in enumerate(paths):
   if path['flow']=='reverted':continue
   for model in models:
    role={**model['grant']['path'],'segments':[{'key':{'kind':'actual_sender'}}]}
    if not any(key(s)==key(role) for g in path['guards'] for s in selectors(g)):continue
    if conditions_possible(path['guards'],role):continue
    required=op('==',model['phase'],model['valid_phase']);issues=copy.deepcopy(path['issues'])
    unknown=any(n.get('kind') in ('unknown','call_unresolved','choice','symbol','member','external_return_unresolved') for n in walk(path['guards']))
    status='inconclusive'
    if not issues and not unknown:status='supported' if conditions_possible(path['guards']+[op('==',model['phase'],model['transition']['to'])],required) else 'refuted_in_scope'
    for effect in path['writes']:
     if effect['path']['root'] in (role['root'],model['phase']['root']):continue
     name=lookup.nodes[effect['path']['root']]['name']
     if requested and not any(x.get('rule')=='AC-04' and x.get('function')==fn and str((x.get('effect') or {}).get('object',x.get('effect_state',''))).split('.')[-1]==name for x in requested):continue
     if any(n.get('kind') in ('unknown','call_unresolved','choice','symbol','member','external_return_unresolved') for n in walk(effect['value'])):
      continue
     synthetic=bundle.get('material_origin','compiler_artifacts')!='compiler_artifacts'
     row={'schema':'m03-p-result-v2','route':'P','rule':'AC-04','status':status,
      'reason':'credential_action_survives_controlled_phase_exit' if status=='supported' else 'action_requires_credential_issuance_phase' if status=='refuted_in_scope' else 'phase_action_relation_unresolved',
      'function':fn,'subject':'actual_sender','structure':'phase_scoped_credential','program_id':bundle['program_id'],'build_id':bundle['build_id'],'policy_scope':'inferred_policy',
      'required_policy_candidate':required,'policy_basis':{'basis':model['kind'],'model':model,'credential':role},
      'effect':{'object':name,'selector':effect['path'],'value':effect['value'],'operator':effect['operator'],'source':effect['source']},
      'path_index':pi,'conditions':path['guards'],'derived_prediction_conditions':[op('==',model['phase'],model['transition']['to'])] if status=='supported' else [],'issues':issues,'execution_status':'not_run','solver_status':'not_called','no_execution_required':True,
      'reportable':status=='supported' and not synthetic,'diagnostic_only':synthetic,'material_origin':bundle.get('material_origin','compiler_artifacts'),
      'limitations':['phase restriction inferred from issuance in a controlled phase and same-manager exit; business intent not uniquely proven',
       'same contract and credential family; no transaction, reopening, arbitrary protocol or deployment proof'],
      'coverage':'declared role, phase and action path','not_a_safety_conclusion':True}
     row['id']=digest({k:row[k] for k in ('program_id','build_id','rule','function','effect','conditions','policy_basis')});rows.append(row)
 return list({r['id']:r for r in rows}.values()),[]
