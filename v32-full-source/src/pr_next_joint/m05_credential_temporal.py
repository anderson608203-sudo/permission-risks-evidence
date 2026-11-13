"""Bounded validity checks for a deadline present in the source condition.

No default expiry is invented. A later alternative use of the SAME issued
credential is checked against its first-use source deadline, with the actual
second-call checks and typed payload equality retained.
"""
import copy
from .m03_p_paths import key,walk,op,lit
from .m03_p_route import keys
from .m05_mechanism_core import retime,solve


def upper_time_bounds(guards):
    found={}
    def positive_nodes(value):
        if isinstance(value,list):
            for item in value:yield from positive_nodes(item)
        elif isinstance(value,dict):
            if value.get('kind')=='op' and value.get('op') in ('!','not'):
                return
            yield value
            # Only logical operands retain positive predicate polarity.
            # A comparison embedded in arithmetic/equality is not a deadline.
            if value.get('kind')=='op' and value.get('op') in ('and','&&','or','||'):
                yield from positive_nodes(value['args'])
    for node in positive_nodes(guards):
        if node.get('kind')!='op' or node.get('op') not in ('<','<=','>','>=') or len(node['args'])!=2:continue
        a,b=node['args'];comparison=node['op']
        if b.get('kind')=='environment' and b.get('field')=='timestamp':
            a,b=b,a;comparison={'<':'>','<=':'>=','>':'<','>=':'<='}[comparison]
        if comparison not in ('<','<=') or a.get('kind')!='environment' or a.get('field')!='timestamp':continue
        if any(n.get('kind')=='environment' for n in walk(b)):continue
        if b.get('kind') not in ('parameter','storage','literal'):continue
        found[key(node)]={'deadline':b,'strict':comparison=='<','source_predicate':node}
    return list(found.values())


def check_temporal(obligation,lookup,fn,path,credential,effect,alternative,alt_effect,alt_credential,base,same_payload):
    rows=[]
    for bound in upper_time_bounds(path['guards']):
        later={'kind':'environment','field':'timestamp','invocation':'credential_later_use','type':'uint256'}
        second=retime(alternative,later);second_credential=retime(alt_credential,later)
        second_effect=retime(alt_effect,later)
        model={**copy.deepcopy(base),'kind':'credential_source_expiry_use',
            'conditions':path['guards'],'alternative_conditions':second['guards'],
            'alternative_credential':second_credential,'alternative_effect':second_effect,
            'deadline':bound['deadline'],'strict_deadline':bound['strict'],
            'original_time':{'kind':'environment','field':'timestamp'},'later_time':later,
            'source_validity_predicate':bound['source_predicate'],
            'checked_dimensions':['same_issued_payload_later_use_against_source_deadline'],
            'unchecked_dimensions':['business_intent_of_expiry','arbitrary_validity_protocol','cryptographic_validity'],
            'assumptions':base['assumptions']+[
                'first-use source upper time bound is the hypothesized credential deadline',
                'alternative later call, same protected effect and issued payload; no intervening-state or unbounded-history claim']}
        rows.append(solve(lookup,obligation,fn,model,
            lambda e,m:expiry_formula(e,m,same_payload),effect['path']['root'],
            keys(effect['path'])[0] if keys(effect['path']) else None))
    return rows


def expiry_formula(e,inputs,same_payload):
    z=e.z;first=inputs['credential'];second=inputs['alternative_credential']
    effect=inputs['effect'];other=inputs['alternative_effect']
    first_time=e.expr(inputs['original_time']);later=e.expr(inputs['later_time']);deadline=e.expr(inputs['deadline'])
    expired=later>=deadline if inputs['strict_deadline'] else later>deadline
    same_effect=z.And(*[e.expr(a)==e.expr(b) for a,b in zip(keys(effect['path']),keys(other['path']))],
                      e.expr(effect['value'])==e.expr(other['value']))
    premise=z.And(*[e.expr(g) for g in inputs['conditions']],e.expr(first)!=0,
                  e.expr(effect['value'])!=e.expr(effect['path']),later>=first_time)
    violation=z.And(same_payload(e,first,second),same_effect,expired,
                    *[e.expr(g) for g in inputs['alternative_conditions']])
    return premise,violation
