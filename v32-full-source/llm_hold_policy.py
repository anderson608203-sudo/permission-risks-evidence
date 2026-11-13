"""Read-only financial-hold policy. This is never a settlement or retry permit."""
import decimal
from .core import require


def check_transport_holds(rows, policy, actual_unknown):
    require(policy.get('approved_by_user') is True and policy.get('user_approval_reference'),
            'TRANSPORT_HOLD_POLICY_NOT_APPROVED')
    schema=policy.get('schema')
    require(schema in ('bounded-incomplete-read-hold-v2','bounded-stream-transport-hold-v3'),'TRANSPORT_HOLD_SCHEMA')
    kinds={'IncompleteRead'} if schema.endswith('-v2') else {'IncompleteRead','RemoteDisconnected'}
    prefix_count=53 if schema.endswith('-v2') else 73
    if schema.endswith('-v3'):
        require(set(policy.get('allowed_failure_classes',[]))==kinds,'TRANSPORT_FAILURE_CLASS_SCOPE')
    require((schema.endswith('-v3') or policy.get('allowed_failure_class')=='IncompleteRead') and
            policy.get('consecutive_failure_stop')==3,'TRANSPORT_HOLD_SCOPE')
    reserved={};settled={};returned={};dispatched=set();order=[]
    for row in rows:
        rid=row.get('request_id');event=row.get('event')
        if event=='api_reserved':
            require(rid not in reserved,'TRANSPORT_DUPLICATE_RESERVATION')
            reserved[rid]=row;order.append(rid)
        elif event=='api_settled':settled[rid]=row
        elif event=='api_returned':returned[rid]=row
        elif event=='api_dispatch_started':dispatched.add(rid)
    unknown=set(reserved)-set(settled)
    require(unknown==set(actual_unknown),'TRANSPORT_UNKNOWN_HISTORY_CHANGED')
    named={x['request_id']:x for x in policy['existing_holds']}
    allowed=set(policy['never_sent_request_digests'])
    prefix=set(policy['original_reserved_request_ids'])
    require(len(prefix)==prefix_count and prefix<=set(reserved),'TRANSPORT_ORIGINAL_ATTEMPTS_CHANGED')
    require(set(named)<=prefix,'TRANSPORT_NAMED_HOLDS_NOT_ORIGINAL')
    for rid,item in named.items():
        require(rid in unknown and reserved[rid]['cost_usd']==item['held_cost_usd'] and
                reserved[rid]['request_sha256']==item['request_sha256'],'TRANSPORT_NAMED_HOLD_CHANGED')
    seen=set()
    for rid in order:
        r=reserved[rid]
        if rid in prefix:continue
        semantic=r.get('semantic_request_sha256',r['request_sha256'])
        require(semantic in allowed and semantic not in seen,
                'TRANSPORT_ONLY_ONCE_NEVER_SENT')
        seen.add(semantic)
    for rid in unknown:
        require(rid in named or (rid not in prefix and reserved[rid].get('semantic_request_sha256',reserved[rid]['request_sha256']) in allowed),
                'TRANSPORT_UNREVIEWED_OLD_HOLD')
        result=returned.get(rid,{})
        require(rid in dispatched and result.get('dispatch_started') is True and
                result.get('status')=='request_failed' and result.get('error_class') in kinds,
                'TRANSPORT_NEW_UNSETTLED_REQUIRES_REVIEW')
    # Consecutive HTTP failures within this continuation stop the batch. Earlier
    # named holds are excluded from this counter, but not from costs/uncertainty.
    streak=0
    for rid in (x for x in order if x not in prefix):
        if rid in unknown:streak+=1
        else:streak=0
        require(streak<3,'TRANSPORT_THREE_CONSECUTIVE_FAILURES_STOP')
    return {'unsettled_requests':sorted(unknown),
            'unsettled_cost_upper':str(sum((decimal.Decimal(reserved[r]['cost_usd']) for r in unknown),decimal.Decimal(0))),
            'new_incomplete_read_holds':len(unknown-set(named)),
            'consecutive_incomplete_read':streak,'is_settlement':False}
