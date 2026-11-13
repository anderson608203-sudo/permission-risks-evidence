"""Asset field identity shared by AC duties and FCR models."""
from .m03_p_paths import key
from .m03_p_route import fields,keys,value_type
from .m03_p_assets import holder_path

def identity(sel):return key([sel.get('root'),fields(sel),sel.get('instance'),len(keys(sel))])
def matches(sel,asset):return identity(sel)==identity(asset['balance_effect']['path'])
def holder(sel,lookup):
    from .m13_financial_relations import component_shape
    return holder_path(sel,lookup) or bool(fields(sel) and component_shape(sel,lookup) is not None)
def unique(models):
    result={}
    for a in models:
        k=identity(a['balance_effect']['path'])
        if k not in result:result[k]=a
        elif a.get('relation_ids'):
            result[k]['relation_ids']=sorted(set(result[k].get('relation_ids',[])+a['relation_ids']))
    return list(result.values())
