"""Requested detector family, never the expected answer of a sample."""
import copy
from .core import require, digest

AC = ('AC-01','AC-02','AC-03','AC-04','AC-05')
FCR = ('FCR-MINT','FCR-TRANSFER','FCR-DESTROY','FCR-PAUSE','FCR-FREEZE')
ALL = AC + FCR

def rules(scope):
    require(scope in ('AC','FCR','joint'),'ANALYSIS_SCOPE_REQUIRED')
    return AC if scope=='AC' else FCR if scope=='FCR' else ALL

def requested(context):
    return rules(context.get('analysis_scope','joint'))

def attach(context,state,scope):
    active=rules(scope)
    context['analysis_scope']=scope
    context['requested_rules']=list(active)
    context['task_request']={'scope':scope,'rules':list(active),'expected_answer_provided':False,
        'revision':'task-family-ac5-fcr5-r2-20261028'}
    context['candidate_relations']=[c for c in context['candidate_relations'] if c['rule'] in active]
    state['analysis_scope']=scope
    state['requested_rules']=active
    return context

def accepted_labels(rows, scope):
    active=rules(scope)
    return sorted({r['rule'] for r in rows if r.get('rule') in active and r.get('reportable')})

def aggregate(scope, per_rule):
    active=rules(scope)
    positives=[r for r in active if per_rule.get(r,{}).get('status')=='positive']
    negatives=[r for r in active if per_rule.get(r,{}).get('status')=='completed_without_alarm_in_scope']
    pending=[r for r in active if r not in positives+negatives]
    status='positive' if positives else 'negative_no_risk_detected' if not pending else 'unknown'
    return {'scope':scope,'status':status,'classification_available':status!='unknown',
        'positive_labels':positives,'negative_labels':negatives,'unknown_labels':pending,
        'all_requested_labels_classified':not pending,
        'negative_means':'no risk detected by completed requested checks, not a safety proof'}
