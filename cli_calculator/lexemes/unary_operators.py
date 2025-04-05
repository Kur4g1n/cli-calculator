import ast
import operator

from cli_calculator.lexemes.registry import lexeme, unary_operator_registry

lexeme(registry=unary_operator_registry, lexeme_type=ast.USub)(operator.neg)
