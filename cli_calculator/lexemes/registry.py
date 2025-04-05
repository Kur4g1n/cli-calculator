import ast
import sys
from collections import UserDict
from collections.abc import Callable, Hashable, Iterable
from enum import IntFlag
from functools import wraps

from cli_calculator.lexemes.errors import ExpressionOverflowError

UnaryOpT = Callable[["OperatorSettings", float], float]
BinaryOpT = Callable[["OperatorSettings", float, float], float]

MAX_FLOAT = sys.float_info.max


class OperatorSettings(IntFlag):
    NONE = 0
    LIMIT_FLOATS = 1 << 0


class CallableRegistry[_KT: Hashable, _VT: Callable](UserDict):
    pass


unary_operator_registry = CallableRegistry[type[ast.operator], UnaryOpT]()
binary_operator_registry = CallableRegistry[type[ast.operator], BinaryOpT]()


def _validate_floats(values: Iterable[float]) -> None:
    for v in values:
        if abs(v) > MAX_FLOAT:
            raise ExpressionOverflowError(v)


def lexeme(
    registry: CallableRegistry,
    lexeme_type: type[ast.AST],
    allow_settings: OperatorSettings = OperatorSettings.LIMIT_FLOATS,
):
    def decorator(func: Callable) -> UnaryOpT | BinaryOpT:
        @wraps(func)
        def wrapper(settings: OperatorSettings, *args: float, **kwargs: float) -> float:
            settings &= allow_settings
            if OperatorSettings.LIMIT_FLOATS in settings:
                _validate_floats(args)
                _validate_floats(kwargs.values())

            return func(*args, **kwargs)

        registry[lexeme_type] = wrapper
        return wrapper

    return decorator
