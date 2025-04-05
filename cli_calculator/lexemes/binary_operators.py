import ast
import operator

from cli_calculator.lexemes.registry import binary_operator_registry, lexeme

lexeme(registry=binary_operator_registry, lexeme_type=ast.Add)(operator.add)
lexeme(registry=binary_operator_registry, lexeme_type=ast.Sub)(operator.sub)
lexeme(registry=binary_operator_registry, lexeme_type=ast.Mult)(operator.mul)
lexeme(registry=binary_operator_registry, lexeme_type=ast.Div)(operator.truediv)
lexeme(registry=binary_operator_registry, lexeme_type=ast.Pow)(operator.pow)
