"""Single missing closing delimiter repair; never invent values or drop tokens."""
import json,hashlib

def strict(text):
    def pairs(items):
        result={}
        for k,v in items:
            if k in result:raise ValueError('duplicate_json_key')
            result[k]=v
        return result
    def invalid(x):raise ValueError('nonfinite_json_number')
    return json.loads(text,object_pairs_hook=pairs,parse_constant=invalid)

def recover(text):
    try:
        value=strict(text)
        return value,{'conversion':'none'}
    except json.JSONDecodeError as error:
        position=error.pos
    # Only an unambiguous structural closing token at the parser error or EOF;
    # missing strings/numbers/keys and truncated provider outputs are excluded.
    candidates=[]
    for pos in sorted({position,len(text.rstrip())}):
        for token in (']','}'):
            try:value=strict(text[:pos]+token+text[pos:])
            except (ValueError,TypeError):continue
            if isinstance(value,dict):candidates.append((value,pos,token))
    if len(candidates)!=1:raise ValueError('RESPONSE_REPAIR_NOT_UNIQUE_SINGLE_CLOSE')
    value,pos,token=candidates[0]
    return value,{'conversion':'single_missing_closing_delimiter','position':pos,'inserted':token,
                  'raw_sha256':hashlib.sha256(text.encode()).hexdigest(),
                  'removed_characters':0,'invented_keys_or_values':False}
