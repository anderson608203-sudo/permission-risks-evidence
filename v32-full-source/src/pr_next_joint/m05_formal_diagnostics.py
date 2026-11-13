"""Stable logical identity and inspectable bounded-model diagnostics.

Raw SMT hashes identify exact artifacts. A separate parsed-artifact DAG identity
removes serializer-local let names. The in-memory AST identity is also retained:
SMT serialization can change associative expression structure without changing
its meaning, so these identities must not be conflated.
"""
from .core import digest

def logical_digest(expression):
    import z3
    memo={}
    def visit(node):
        ident=node.get_id()
        if ident in memo:return memo[ident]
        if node.ctx_ref()!=expression.ctx_ref():raise ValueError('FORMULA_CONTEXT')
        if hasattr(node,'is_forall') or hasattr(node,'is_exists'):
            # Current models are quantifier free; never silently alpha-normalize
            # binders that this serializer has not implemented.
            raise ValueError('FORMULA_QUANTIFIER_NOT_CANONICALIZED')
        decl=node.decl()
        record={'kind':decl.kind(),'name':str(decl.name()),'parameters':[str(x) for x in decl.params()],
                'sort':node.sort().sexpr(),'arguments':[visit(x) for x in node.children()]}
        if z3.is_int_value(node) or z3.is_rational_value(node) or z3.is_bv_value(node):record['literal']=node.sexpr()
        result=digest(record);memo[ident]=result;return result
    return visit(expression)

def artifact_digest(smt):
    import z3
    terms=z3.parse_smt2_string(smt)
    return logical_digest(terms[0] if len(terms)==1 else z3.And(*terms))


def diagnostics(premise,violation,formula,solver,answer,smt):
    result={'encoding':'quantifier-free typed source model',
        'premise_ast_sha256':logical_digest(premise),
        'violation_ast_sha256':logical_digest(violation),
        'constructed_formula_ast_sha256':logical_digest(formula),
        'formula_ast_sha256':artifact_digest(smt),
        'formula_ast_origin':'parsed_saved_smt_assertions',
        'scope':'parsed artifact AST including sorts and source symbols; construction AST recorded separately; neither semantic equivalence nor deployment reachability'}
    if str(answer)=='sat':
        model=solver.model()
        result['bounded_model_assignment']={str(d):str(model[d]) for d in sorted(model.decls(),key=str)}
        result['assignment_is_execution_trace']=False
    return result
