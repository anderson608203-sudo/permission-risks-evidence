"""Compiler-width arithmetic; no unsigned widening of signed source values."""
import re
from .m04_logic import Unsupported

def integer_type(typ):
    m=re.fullmatch(r'(u?int)(\d*)',typ or '')
    return (m[1]=='int',int(m[2] or 256)) if m else None

def checked_mode(lookup,state):
    import json
    raw=lookup.bundle.get('compiler',{})
    text=raw.get('version',raw.get('compiler_version','')) if isinstance(raw,dict) else str(raw)
    if not text:text=str(lookup.bundle.get('compiler_version',''))
    m=re.search(r'(\d+)\.(\d+)\.(\d+)',text)
    if not m:raise Unsupported('integer_compiler_version_missing')
    return tuple(map(int,m.groups()))>=(0,8,0) and not state.get('_unchecked_depth',0)

def encode(e,v):
    typ=integer_type(v.get('type'))
    if typ is None:raise Unsupported('integer_type_unresolved')
    signed,bits=typ;z=e.z;low=-2**(bits-1) if signed else 0;high=2**(bits-int(signed))
    if v['kind']=='integer_cast':value=e.expr(v['input'])
    else:
        args=[e.expr(a) for a in v['args']];operator=v['operator']
        if not all(z.is_int(x) for x in args):raise Unsupported('integer_operand_sort')
        if len(args)==1:
            if operator!='-':raise Unsupported('integer_unary_operator')
            value=-args[0]
        else:
            a,b=args
            if operator in ('/','%'):
                e.constraints.append(b!=0)
                absolute=z.Abs(a)/z.Abs(b);quotient=z.If((a<0)!=(b<0),-absolute,absolute)
                value=quotient if operator=='/' else a-quotient*b
            elif operator in ('+','-','*'):value={'+':lambda:a+b,'-':lambda:a-b,'*':lambda:a*b}[operator]()
            else:raise Unsupported('integer_operator_not_lowered')
        if v.get('checked'):
            e.constraints.extend([value>=low,value<high]);return value
    unsigned=value%(2**bits)
    return z.If(unsigned>=2**(bits-1),unsigned-2**bits,unsigned) if signed else unsigned
