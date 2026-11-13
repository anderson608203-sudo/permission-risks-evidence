"""Relations between existing typed paths; no source-reference discovery.

These operations neither repair M2 anchors nor widen the target/instance set.
They project a previously extracted function's parameter keys onto another
already extracted selector, retaining its source guards and provenance.
"""
import copy
from .m05_writer_scope import gaps_for
from .m03_p_paths import key,op,lit,walk
from .m03_p_route import keys,fields,relocate,value_type,effective_permission
from .m03_p_lifecycle import leaves
from .m04_logic import Unsupported


def family(a,b):
    return (a.get('kind')==b.get('kind')=='storage' and a['root']==b['root']
            and fields(a)==fields(b) and key(a.get('instance'))==key(b.get('instance'))
            and len(keys(a))==len(keys(b)))


def project(value,source,target):
    if not family(source,target):raise Unsupported('typed_relation_family_mismatch')
    # Existing strict key substitution rejects unrelated/free parameters.
    return relocate(value,source,target)


def positive_qualification(lookup,paths,function,predicate):
    """Use an independent positive source interface, not the rejected guard.

    Caller-indexed boolean membership is only a conditional policy hypothesis.
    A parameterized getter is instantiated for the very same typed selector;
    its complete predicate and its own business premises remain intact.
    """
    from .m03_p_route import selectors
    from .m05_mechanism_core import successful
    for selected in selectors(predicate):
        if value_type(selected,lookup)!='bool' or not any(x.get('kind')=='actual_sender' for x in keys(selected)):
            continue
        for peer,branches in paths.items():
            if peer==function:continue
            for branch in branches:
                returned=branch.get('return_value')
                if not successful(branch) or branch['issues'] or not returned:continue
                # A plain positive getter is independent evidence. A negated
                # getter, arbitrary boolean expression or label is not one.
                if not family(returned,selected):continue
                try:
                    q=project(returned,returned,selected)
                    guards=project(branch['guards'],returned,selected)
                except (ValueError,Unsupported):continue
                return op('and',q,*guards),[{'function':peer,'source':branch['entry_source'],
                    'positive_interface':returned,'instantiated_qualification':q,
                    'interface_preconditions':guards}], 'source_positive_membership_interface'
    return None


def holder_authorized_request(path,holder,quantity,lookup,program,recipient=None,excluded_roots=()):
    """A consumed quantitative request set exclusively by its holder.

    Extends an existing allowance shape to typed struct fields and reset-to-zero
    consumption. No unconsumed flag, queue label or admin signature counts as
    holder consent. Calls with unknown effects invalidate this certificate.
    """
    from .m05_state_relations import scalar
    from .m05_mechanism_core import successful
    from .m03_p_paths import conditions_possible
    candidates=[]
    original_recipient=copy.deepcopy(recipient)
    for write in path['writes']:
        for leaf in leaves(write):
            try:leaf=scalar(leaf,lookup)
            except Unsupported:continue
            selector=leaf['path'];idx=keys(selector)
            # Ownership/balance data is not an authorization request. The
            # consumer supplies the already established asset/supply roots.
            if selector['root'] in excluded_roots:continue
            if (len(idx) not in (1,2) or key(idx[0])!=key(holder)
                    or len(idx)==2 and idx[1].get('kind')!='actual_sender'
                    or not str(value_type(selector,lookup)).startswith('uint')):continue
            # Consumed state itself is the amount, not an unrelated flag.
            if leaf['value']!=lit(0) or key(quantity)!=key(selector):continue
            if gaps_for(lookup,{selector['root']}):raise Unsupported('holder_request_writer_inventory_incomplete')
            setters=[];invalid=False;destinations={};holder_request_seen=False
            for fn,branches in program.items():
                for path_index,branch in enumerate(branches):
                    if not successful(branch):continue
                    for w in branch['writes']:
                        for update in leaves(w):
                            if not family(update['path'],selector):continue
                            try:update=scalar(update,lookup)
                            except Unsupported:
                                raise Unsupported('holder_request_related_writer_type_unresolved')
                            if update['value']==lit(0):continue
                            own=op('==',keys(update['path'])[0],{'kind':'actual_sender'})
                            if branch['issues']:
                                raise Unsupported('holder_request_related_writer_semantics_unresolved')
                            if conditions_possible(branch['guards'],own):
                                invalid=True;continue
                            holder_request_seen=True
                            if update['value'].get('kind')=='parameter':
                                if recipient is not None and recipient.get('kind')=='unresolved_split_recipient':
                                    raise Unsupported('holder_request_split_destination_scope_unresolved')
                                # Amount and destination are established by
                                # the SAME complete holder operation/path.
                                peers=[]
                                if recipient is not None:
                                    for raw_peer in branch['writes']:
                                        for peer in leaves(raw_peer):
                                            pp=peer['path']
                                            if (pp['root']==update['path']['root'] and
                                                    key(pp.get('instance'))==key(update['path'].get('instance')) and
                                                    keys(pp)==keys(update['path']) and fields(pp)!=fields(update['path']) and
                                                    value_type(pp,lookup) in ('address','address payable') and
                                                    peer['value'].get('kind')=='parameter'):
                                                from .m05_mechanism_core import remap
                                                # This certificate describes a
                                                # different invocation whose
                                                # caller is the request holder.
                                                peers.append(project(remap(pp,sender=holder),
                                                    remap(update['path'],sender=holder),selector))
                                    unique={key(p):p for p in peers}
                                    if len(unique)!=1:invalid=True;continue
                                    destinations.update(unique)
                                setters.append({'function':fn,'source':update['source'],
                                    'path_index':path_index,'setter_invocation_caller':copy.deepcopy(holder),
                                    'write':copy.deepcopy(update),'guards':copy.deepcopy(branch['guards'])})
                            else:invalid=True
            expected=None
            if holder_request_seen and (invalid or not setters):
                raise Unsupported('holder_request_amount_or_recipient_scope_unresolved')
            if recipient is not None and setters and not invalid:
                if len(destinations)!=1:raise Unsupported('holder_request_recipient_not_unique')
                expected=next(iter(destinations.values()))
                for fn,branches in program.items():
                    for branch in branches:
                        if not successful(branch):continue
                        for raw_write in branch['writes']:
                            for update in leaves(raw_write):
                                if not family(update['path'],expected):continue
                                update=scalar(update,lookup)
                                if update['value']==lit(0):
                                    quantity_cleared=any(family(q['path'],selector)
                                        and keys(q['path'])==keys(update['path'])
                                        and scalar(q,lookup)['value']==lit(0)
                                        for raw in branch['writes'] for q in leaves(raw))
                                    if quantity_cleared:continue
                                own=op('==',keys(update['path'])[0],{'kind':'actual_sender'})
                                if (branch['issues'] or conditions_possible(branch['guards'],own)
                                        or update['value'].get('kind')!='parameter' and update['value']!=lit(0)):invalid=True
            if holder_request_seen and invalid:
                raise Unsupported('holder_request_destination_has_unresolved_writer')
            if setters and not invalid:
                predicate=op('>=',selector,quantity)
                if expected is not None:predicate=op('and',predicate,op('==',original_recipient,expected))
                candidates.append({'predicate':predicate,'selector':selector,
                    'certificate':{'kind':'consumed_holder_quantity_request',
                        'holder':holder,'quantity':quantity,'holder_controlled_setters':setters,
                        'consumption':leaf,'recipient':expected,'actual_recipient':original_recipient,
                        'scope':'holder-created quantity request and, for transfer, holder-controlled recipient; finite source operation',
                        'assumptions':['source-bound request amount is interpreted as holder authorization for this declared operation',
                            'current request pre-state; no unbounded queue or off-chain consent claim']}})
    return candidates
