import ast
import pytest

from cli_calculator.lexemes import OperatorSettings, unary_operator_registry, binary_operator_registry
from cli_calculator.models.errors import ComplexConstantError
from cli_calculator.models.expression import BinaryOperatorNode, ConstantNode, UnaryOperatorNode


def test_constant_node():
    assert ConstantNode(1).evaluate(OperatorSettings.LIMIT_FLOATS) == 1
    assert ConstantNode(12.3).value == 12.3
    assert isinstance(ConstantNode(10000).evaluate(OperatorSettings.LIMIT_FLOATS), float)
    assert isinstance(ConstantNode(78.6).value, float)


def test_constant_node_error():
    with pytest.raises(ComplexConstantError) as e_info:
        ConstantNode(12.3 + 3j)
    assert str(e_info.value) == "Value (12.3+3j) of type complex is not supported"


def test_binary_node():
    assert (
        BinaryOperatorNode(binary_operator_registry[ast.Add], ConstantNode(1), ConstantNode(1)).evaluate(
            OperatorSettings.LIMIT_FLOATS
        )
        == 2
    )
    assert BinaryOperatorNode(binary_operator_registry[ast.Sub], ConstantNode(20), ConstantNode(43.127)).evaluate(
        OperatorSettings.LIMIT_FLOATS
    ) == pytest.approx(-23.127, 1e-11)
    assert (
        BinaryOperatorNode(binary_operator_registry[ast.Mult], ConstantNode(4), ConstantNode(10)).evaluate(
            OperatorSettings.LIMIT_FLOATS
        )
        == 40
    )
    assert BinaryOperatorNode(binary_operator_registry[ast.Div], ConstantNode(13), ConstantNode(7)).evaluate(
        OperatorSettings.LIMIT_FLOATS
    ) == pytest.approx(1.85714285714, 1e-11)


def test_unary_node():
    assert UnaryOperatorNode(unary_operator_registry[ast.USub], ConstantNode(13.7)).evaluate(
        OperatorSettings.LIMIT_FLOATS
    ) == pytest.approx(-13.7, 1e-11)
