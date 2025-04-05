import ast
import pytest

from cli_calculator.lexemes import (
    OperatorSettings,
    unary_operator_registry,
    binary_operator_registry,
    constant_registry
)
from cli_calculator.lexemes.errors import ExpressionOverflowError
from cli_calculator.models.errors import ComplexConstantError
from cli_calculator.models.expression import BinaryOperatorNode, ConstantNode, UnaryOperatorNode


def test_constant_node():
    validator = constant_registry[ast.Constant]
    assert ConstantNode(validator, 1).evaluate(OperatorSettings.LIMIT_FLOATS) == 1
    assert ConstantNode(validator, 12.3).value == 12.3
    assert isinstance(ConstantNode(validator, 10000).evaluate(OperatorSettings.LIMIT_FLOATS), float)
    assert isinstance(ConstantNode(validator, 78.6).value, float)
    assert ConstantNode(validator, 1e999).evaluate(OperatorSettings.NONE) == float("inf")


def test_constant_node_error():
    validator = constant_registry[ast.Constant]
    with pytest.raises(ComplexConstantError) as e_info:
        ConstantNode(validator, 12.3 + 3j)
    assert str(e_info.value) == "Value (12.3+3j) of type complex is not supported"
    num = 1e999
    with pytest.raises(ExpressionOverflowError) as e_info:
        ConstantNode(validator, num).evaluate(OperatorSettings.LIMIT_FLOATS)
    assert str(e_info.value) == f"Value {num} exceeds maximum allowed value"


def test_binary_node():
    validator = constant_registry[ast.Constant]
    assert (
        BinaryOperatorNode(
            binary_operator_registry[ast.Add], ConstantNode(validator, 1), ConstantNode(validator, 1)
        ).evaluate(OperatorSettings.LIMIT_FLOATS)
        == 2
    )
    assert BinaryOperatorNode(
        binary_operator_registry[ast.Sub], ConstantNode(validator, 20), ConstantNode(validator, 43.127)
    ).evaluate(OperatorSettings.LIMIT_FLOATS) == pytest.approx(-23.127, 1e-11)
    assert (
        BinaryOperatorNode(
            binary_operator_registry[ast.Mult], ConstantNode(validator, 4), ConstantNode(validator, 10)
        ).evaluate(OperatorSettings.LIMIT_FLOATS)
        == 40
    )
    assert BinaryOperatorNode(
        binary_operator_registry[ast.Div], ConstantNode(validator, 13), ConstantNode(validator, 7)
    ).evaluate(OperatorSettings.LIMIT_FLOATS) == pytest.approx(1.85714285714, 1e-11)


def test_unary_node():
    validator = constant_registry[ast.Constant]
    assert UnaryOperatorNode(unary_operator_registry[ast.USub], ConstantNode(validator, 13.7)).evaluate(
        OperatorSettings.LIMIT_FLOATS
    ) == pytest.approx(-13.7, 1e-11)
