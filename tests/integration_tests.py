import pytest
from cli_calculator.evaluator import Evaluator
from cli_calculator.parsing.parser import ExpressionParser
from cli_calculator.parsing.errors import (
    ExpressionFormatError,
    UnsupportedLexemeError,
    UnsupportedNodeTypeError,
)
from cli_calculator.models.errors import ComplexConstantError
from cli_calculator.lexemes.errors import ExpressionOverflowError


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("2.5 + 3.7", 6.2),
        ("-4.2 * 2.5", -10.5),
        ("10.5 / 2 + 3.1", 8.35),
        ("2.0 ^ 3.0 - 1.5", 6.5),
        ("-2.5 * (3.1 + 1.2)", -10.75),
        ("15.7 / -3.0 + 2.1", -3.13333333333),
    ],
)
def test_integration_success(expression: str, expected: float):
    parser = ExpressionParser()
    evaluator = Evaluator()
    tree = parser.parse_string(expression)
    result = evaluator.evaluate_tree(tree)
    assert result == pytest.approx(expected, 1e-11)


@pytest.mark.parametrize(
    "expression, error, message",
    [
        (
            "3.1 ! 2.5",
            ExpressionFormatError,
            "Wrong expression format. Unable to proceed to parsing",
        ),
        ("2.5 + 1.7 ; -3.2", ExpressionFormatError, "Multiple or no expressions are unsupported"),
        ("", ExpressionFormatError, "Multiple or no expressions are unsupported"),
        ("2.1 & 3.2", UnsupportedLexemeError, "Binary operator BitAnd is not supported"),
        ("+2.5", UnsupportedLexemeError, "Unary operator UAdd is not supported"),
        ("await 3.1", UnsupportedNodeTypeError, "Unsupported node type: Await"),
        ("1.5 + 4.2j", ComplexConstantError, "Value 4.2j of type complex is not supported"),
        ("1e999 * 2.5", ExpressionOverflowError, "Value inf exceeds maximum allowed value"),
    ],
)
def test_integration_errors(expression: str, error: type[Exception], message: str):
    parser = ExpressionParser()
    evaluator = Evaluator()
    with pytest.raises(error) as e_info:
        tree = parser.parse_string(expression)
        evaluator.evaluate_tree(tree)
    assert str(e_info.value) == message


def test_integration_no_limit_overflow():
    parser = ExpressionParser()
    evaluator = Evaluator(limit_floats=False)
    tree = parser.parse_string("1e999 * 2.5")
    result = evaluator.evaluate_tree(tree)
    assert result == float("inf")
