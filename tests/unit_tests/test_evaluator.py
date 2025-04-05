import ast
import pytest

from cli_calculator.evaluator import Evaluator
from cli_calculator.lexemes.errors import ExpressionOverflowError
from cli_calculator.lexemes import constant_registry
from cli_calculator.models.expression import BinaryOperatorNode, ConstantNode
from cli_calculator.lexemes import binary_operator_registry

@pytest.mark.parametrize(
    "op1, op2, val1, val2, val3, expected",
    [
        (ast.Add, ast.Add, 2, 3, 4, 9),           # (2 + 3) + 4 = 9
        (ast.Add, ast.Sub, 5, 3, 2, 6),           # (5 + 3) - 2 = 6
        (ast.Add, ast.Mult, 2, 3, 4, 20),         # (2 + 3) * 4 = 20
        (ast.Add, ast.Div, 6, 4, 2, 5),           # (6 + 4) / 2 = 5
        (ast.Sub, ast.Add, 10, 4, 3, 9),          # (10 - 4) + 3 = 9
        (ast.Sub, ast.Sub, 15, 5, 3, 7),          # (15 - 5) - 3 = 7
        (ast.Sub, ast.Mult, 8, 3, 2, 10),         # (8 - 3) * 2 = 10
        (ast.Sub, ast.Div, 10, 4, 2, 3),          # (10 - 4) / 2 = 3
        (ast.Mult, ast.Add, 3, 2, 4, 10),         # (3 * 2) + 4 = 10
        (ast.Mult, ast.Sub, 4, 3, 1, 11),         # (4 * 3) - 1 = 11
        (ast.Mult, ast.Mult, 2, 3, 4, 24),        # (2 * 3) * 4 = 24
        (ast.Mult, ast.Div, 6, 2, 3, 4),          # (6 * 2) / 3 = 4
        (ast.Div, ast.Add, 8, 2, 3, 7),           # (8 / 2) + 3 = 7
        (ast.Div, ast.Sub, 10, 2, 3, 2),          # (10 / 2) - 3 = 2
        (ast.Div, ast.Mult, 6, 2, 3, 9),          # (6 / 2) * 3 = 9
        (ast.Div, ast.Div, 12, 3, 2, 2),          # (12 / 3) / 2 = 2
        (ast.Pow, ast.Add, 2, 3, 1, 9),        # (2 ^ 3) + 1 = 9
        (ast.Pow, ast.Sub, 3, 2, 1, 8),        # (3 ^ 2) - 1 = 8
        (ast.Pow, ast.Mult, 2, 2, 3, 12),      # (2 ^ 2) * 3 = 12
        (ast.Pow, ast.Div, 4, 2, 2, 8),        # (4 ^ 2) / 2 = 8
        (ast.Add, ast.Pow, 2, 1, 1, 3),        # (2 + 1) ^ 3 = 8
        (ast.Sub, ast.Pow, 5, 2, 2, 9),        # (5 - 2) ^ 2 = 9
        (ast.Mult, ast.Pow, 2, 2, 2, 16),      # (2 * 2) ^ 2 = 16
        (ast.Div, ast.Pow, 4, 2, 2, 4),        # (4 / 2) ^ 2 = 4
    ]
)
def test_evaluator(op1, op2, val1, val2, val3, expected):
    validator = constant_registry[ast.Constant]
    inner_node = BinaryOperatorNode(
        binary_operator_registry[op1],
        ConstantNode(validator, val1),
        ConstantNode(validator, val2)
    )
    outer_node = BinaryOperatorNode(
        binary_operator_registry[op2],
        inner_node,
        ConstantNode(validator, val3)
    )
    evaluator = Evaluator()
    result = evaluator.evaluate_tree(outer_node)
    assert result == pytest.approx(expected, 1e-11)

def test_evaluator_error():
    validator = constant_registry[ast.Constant]
    node = BinaryOperatorNode(
        binary_operator_registry[ast.Div],
        ConstantNode(validator, 1e999),
        ConstantNode(validator, 1)
    )
    evaluator = Evaluator()
    with pytest.raises(ExpressionOverflowError):
        evaluator.evaluate_tree(node)

    evaluator = Evaluator(limit_floats=False)
    assert evaluator.evaluate_tree(node) == float("inf")
