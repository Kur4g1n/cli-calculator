import operator
import pytest

from cli_calculator.models.errors import ComplexConstantError
from cli_calculator.models.expression import BinaryOperatorNode, ConstantNode, UnaryOperatorNode


def test_constant_node():
    assert ConstantNode(1).evaluate() == 1
    assert ConstantNode(12.3).value == 12.3
    assert isinstance(ConstantNode(10000).evaluate(), float)
    assert isinstance(ConstantNode(78.6).value, float)


def test_constant_node_error():
    with pytest.raises(ComplexConstantError) as e_info:
        ConstantNode(12.3 + 3j)
    assert str(e_info.value) == "Value (12.3+3j) of type complex is not supported"


def test_binary_node():
    assert BinaryOperatorNode(operator.add, ConstantNode(1), ConstantNode(1)).evaluate() == 2
    assert BinaryOperatorNode(
        operator.sub, ConstantNode(20), ConstantNode(43.127)
    ).evaluate() == pytest.approx(-23.127, 1e-11)
    assert BinaryOperatorNode(operator.mul, ConstantNode(4), ConstantNode(10)).evaluate() == 40
    assert BinaryOperatorNode(
        operator.truediv, ConstantNode(13), ConstantNode(7)
    ).evaluate() == pytest.approx(1.85714285714, 1e-11)


def test_unary_node():
    assert UnaryOperatorNode(operator.neg, ConstantNode(13.7)).evaluate() == pytest.approx(
        -13.7, 1e-11
    )
