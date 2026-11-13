"""Small Draft-2020-12 subset validator for the frozen R2 interfaces.

The local environment does not ship jsonschema. This validator covers the
keywords used by RiskQuery/VerificationPlan (refs, objects, arrays, const,
enum, anyOf/oneOf, required, additionalProperties, types, bounds/patterns).
It is deliberately strict about unknown fields, which is the R5 regression.
"""
import json, pathlib, re
from .core import require

_CONSTRAINTS = {'$ref','type','const','enum','required','properties','additionalProperties','items','minItems','minimum','minLength','pattern','anyOf','oneOf','allOf','not'}

def _resolve(schema, root, seen=None):
    seen = seen or set()
    ref = schema.get('$ref')
    if not ref:
        return schema
    require(ref.startswith('#/$defs/'), 'unsupported_schema_ref:' + str(ref))
    name = ref.split('/')[-1]
    require(name in root['$defs'], 'missing_schema_def:' + name)
    require(ref not in seen, 'schema_ref_cycle:' + ref)
    return _resolve(root['$defs'][name], root, seen | {ref})

def _type_ok(value, typ):
    if isinstance(typ, list):
        return any(_type_ok(value, t) for t in typ)
    return {'object': isinstance(value, dict), 'array': isinstance(value, list), 'string': isinstance(value, str),
            'integer': type(value) is int, 'number': isinstance(value, (int, float)) and not isinstance(value, bool),
            'boolean': isinstance(value, bool), 'null': value is None}.get(typ, True)

def validate(value, name, schema_path):
    root = json.loads(pathlib.Path(schema_path).read_text(encoding='utf-8'))
    require(name in root['$defs'], 'missing_schema_object:' + name)
    _validate(value, {'$ref': '#/$defs/' + name}, root, name)
    return True

def _validate(value, schema, root, path):
    schema = _resolve(schema, root)
    if 'type' in schema:
        require(_type_ok(value, schema['type']), 'schema_type:' + path)
    if 'const' in schema:
        require(value == schema['const'], 'schema_const:' + path)
    if 'enum' in schema:
        require(value in schema['enum'], 'schema_enum:' + path)
    if 'anyOf' in schema:
        errors=[]
        for i, option in enumerate(schema['anyOf']):
            try:
                _validate(value, option, root, path); errors=[]
                break
            except ValueError as error:
                errors.append(str(error))
        require(not errors, 'schema_anyOf:' + path + ':' + ';'.join(errors[:2]))
    if 'oneOf' in schema:
        matches=0
        for option in schema['oneOf']:
            try:
                _validate(value, option, root, path); matches += 1
            except ValueError:
                pass
        require(matches == 1, 'schema_oneOf:' + path)
    for option in schema.get('allOf', []):
        _validate(value, option, root, path)
    if 'not' in schema:
        try:
            _validate(value, schema['not'], root, path)
            raise ValueError('schema_not:' + path)
        except ValueError as error:
            require(str(error) != 'schema_not:' + path, str(error))
    if isinstance(value, dict):
        for key in schema.get('required', []):
            require(key in value, 'schema_required:' + path + '.' + key)
        props = schema.get('properties', {})
        extra = schema.get('additionalProperties', True)
        for key, child in value.items():
            if key in props:
                _validate(child, props[key], root, path + '.' + key)
            elif extra is False:
                raise ValueError('schema_additional_property:' + path + '.' + key)
            elif isinstance(extra, dict):
                _validate(child, extra, root, path + '.' + key)
    if isinstance(value, list):
        if 'minItems' in schema:
            require(len(value) >= schema['minItems'], 'schema_minItems:' + path)
        if 'items' in schema:
            for i, child in enumerate(value):
                _validate(child, schema['items'], root, path + '[' + str(i) + ']')
    if isinstance(value, str):
        if 'minLength' in schema:
            require(len(value) >= schema['minLength'], 'schema_minLength:' + path)
        if 'pattern' in schema:
            require(re.fullmatch(schema['pattern'], value), 'schema_pattern:' + path)
    if type(value) is int and 'minimum' in schema:
        require(value >= schema['minimum'], 'schema_minimum:' + path)
