"""Pure compiler expressions, not inferred permission or safety."""
from fractions import Fraction
def constant_integer(node):
    """Bounded constant folding only; caller must establish compiler constant type."""
    budget=[128]
    def visit(n):
        budget[0]-=1
        if budget[0]<0:raise ValueError('constant_budget')
        k=n.get('nodeType')
        if k=='Literal' and n.get('kind')=='number':
            v=n.get('value','').replace('_','')
            value=Fraction(int(v,16)) if v.lower().startswith('0x') else Fraction(v)
            units={'wei':1,'szabo':10**12,'finney':10**15,'gwei':10**9,'ether':10**18,'seconds':1,'minutes':60,'hours':3600,'days':86400,'weeks':604800,'years':31536000}
            if n.get('subdenomination'):
                value*=units[n['subdenomination']]
            return value
        if k=='TupleExpression' and len(n.get('components',[]))==1:return visit(n['components'][0])
        if k=='UnaryOperation' and n.get('operator') in ('+','-'):
            value=visit(n['subExpression']);return value if n['operator']=='+' else -value
        if k=='BinaryOperation':
            a,b=visit(n['leftExpression']),visit(n['rightExpression']);op=n.get('operator')
            if op=='+':return a+b
            if op=='-':return a-b
            if op=='*':return a*b
            if op=='/' and b:return a/b
            if op=='**' and b.denominator==1 and 0<=b<=1024 and abs(a.numerator).bit_length()*int(b)<=8192:return a**int(b)
            if op=='%' and a.denominator==b.denominator==1 and b:return a%b
        raise ValueError('not_a_supported_constant')
    try:
        value=visit(node)
        return value.numerator if value.denominator==1 else None
    except (ValueError,KeyError,ZeroDivisionError,OverflowError):return None

def pure_message_argument(node,lookup):
    # Reading a string variable cannot call out or change storage. Indexing,
    # concatenation, function calls and computed error arguments are not erased.
    if node.get('nodeType')=='Literal':return True
    if node.get('nodeType')=='Identifier':
        decl=lookup.nodes.get(node.get('referencedDeclaration'),{})
        typ=decl.get('typeDescriptions',{}).get('typeString','')
        return decl.get('nodeType')=='VariableDeclaration' and typ.startswith(('string','bytes '))
    return False
