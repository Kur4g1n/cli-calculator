import operator
import pytest

from cli_calculator.models.expression import (
    BinaryOperatorNode,
    ConstantNode,
    ExpressionNode,
    UnaryOperatorNode,
)
from cli_calculator.parsing.parser import ExpressionParser


@pytest.mark.parametrize(
    "expression,tree",
    [
        ("2 + 2", BinaryOperatorNode(operator.add, ConstantNode(2), ConstantNode(2))),
        (
            "1234.15 / 1000.5 * (-13 - 100)",
            BinaryOperatorNode(
                operator.mul,
                BinaryOperatorNode(
                    operator.truediv, ConstantNode(1234.15), ConstantNode(1000.5)
                ),
                BinaryOperatorNode(
                    operator.sub,
                    UnaryOperatorNode(operator.neg, ConstantNode(13)),
                    ConstantNode(100),
                ),
            ),
        ),
        (
            "-(-134.12*-13)",
            UnaryOperatorNode(
                operator.neg,
                BinaryOperatorNode(
                    operator.mul,
                    UnaryOperatorNode(operator.neg, ConstantNode(134.12)),
                    UnaryOperatorNode(operator.neg, ConstantNode(13)),
                ),
            ),
        ),
    ],
)
def test_parser_general(expression: str, tree: ExpressionNode):
    root = ExpressionParser.parse_string(expression)
    assert root == tree
