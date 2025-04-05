import ast
import math
import operator

from cli_calculator.lexemes.registry import (OperatorSettings,
                                             constant_registry, lexeme)

lexeme(registry=constant_registry, lexeme_type=ast.Constant)(operator.pos)


@lexeme(registry=constant_registry, lexeme_type="e", allow_settings=OperatorSettings.NONE)
def e(*args, **kwargs) -> float:
    return math.e


@lexeme(registry=constant_registry, lexeme_type="pi", allow_settings=OperatorSettings.NONE)
def pi(*args, **kwargs) -> float:
    return math.pi
