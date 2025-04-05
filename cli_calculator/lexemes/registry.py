import ast
import sys
from collections import UserDict
from collections.abc import Callable, Hashable
from enum import IntFlag
from functools import wraps

from cli_calculator.lexemes.errors import ExpressionOverflowError

UnaryOpT = Callable[["OperatorSettings", float], float]
ConstantT = UnaryOpT
BinaryOpT = Callable[["OperatorSettings", float, float], float]

MAX_FLOAT = sys.float_info.max


class OperatorSettings(IntFlag):
    NONE = 0
    LIMIT_FLOATS = 1 << 0


class CallableRegistry[_KT: Hashable, _VT: Callable](UserDict):
    pass


constant_registry = CallableRegistry[type[ast.Constant] | type[ast.Name], ConstantT]()
unary_operator_registry = CallableRegistry[type[ast.operator], UnaryOpT]()
binary_operator_registry = CallableRegistry[type[ast.operator], BinaryOpT]()


def lexeme(
    lexeme_type: type[ast.AST],
    registry: CallableRegistry,
    allow_settings: OperatorSettings = OperatorSettings.LIMIT_FLOATS,
):
    def decorator(func: Callable) -> UnaryOpT | BinaryOpT:
        @wraps(func)
        def wrapper(settings: OperatorSettings, *args: float, **kwargs: float) -> float:
            settings &= allow_settings
            res = func(*args, **kwargs)
            if OperatorSettings.LIMIT_FLOATS in settings and abs(res) > MAX_FLOAT:
                raise ExpressionOverflowError(res)

            return res

        registry[lexeme_type] = wrapper
        return wrapper

    return decorator
