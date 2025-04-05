import math

from cli_calculator.lexemes.errors import ArgumentNumberError
from cli_calculator.lexemes.registry import OperatorSettings, function_registry, lexeme


@lexeme(
    registry=function_registry,
    lexeme_type="sin",
    allow_settings=OperatorSettings.LIMIT_FLOATS | OperatorSettings.USE_DEGREES,
)
def sin(*args: float):
    if len(args) != 1:
        raise ArgumentNumberError(len(args), 1)
    return math.sin(*args)


@lexeme(
    registry=function_registry,
    lexeme_type="cos",
    allow_settings=OperatorSettings.LIMIT_FLOATS | OperatorSettings.USE_DEGREES,
)
def cos(*args: float):
    if len(args) != 1:
        raise ArgumentNumberError(len(args), 1)
    return math.cos(*args)


@lexeme(
    registry=function_registry,
    lexeme_type="tg",
    allow_settings=OperatorSettings.LIMIT_FLOATS | OperatorSettings.USE_DEGREES,
)
def tg(*args: float):
    if len(args) != 1:
        raise ArgumentNumberError(len(args), 1)
    return math.tan(*args)


@lexeme(
    registry=function_registry,
    lexeme_type="ctg",
    allow_settings=OperatorSettings.LIMIT_FLOATS | OperatorSettings.USE_DEGREES,
)
def ctg(*args: float):
    if len(args) != 1:
        raise ArgumentNumberError(len(args), 1)
    return 1 / math.tan(*args)


@lexeme(
    registry=function_registry,
    lexeme_type="sqrt",
    allow_settings=OperatorSettings.LIMIT_FLOATS
)
def sqrt(*args: float):
    if len(args) != 1:
        raise ArgumentNumberError(len(args), 1)
    return math.sqrt(*args)


@lexeme(
    registry=function_registry,
    lexeme_type="ln",
    allow_settings=OperatorSettings.LIMIT_FLOATS
)
def ln(*args: float):
    if len(args) not in (1, 2):
        raise ArgumentNumberError(len(args), 2)
    return math.log(*args)


@lexeme(
    registry=function_registry,
    lexeme_type="exp",
    allow_settings=OperatorSettings.LIMIT_FLOATS
)
def exp(*args: float):
    if len(args) != 1:
        raise ArgumentNumberError(len(args), 1)
    return math.exp(*args)
