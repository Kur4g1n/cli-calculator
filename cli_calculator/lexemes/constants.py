import ast
import operator

from cli_calculator.lexemes.registry import constant_registry, lexeme

lexeme(registry=constant_registry, lexeme_type=ast.Constant)(operator.pos)
