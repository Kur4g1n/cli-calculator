import ast
import pytest

from cli_calculator.lexemes import unary_operator_registry, binary_operator_registry
from cli_calculator.models.errors import ComplexConstantError
from cli_calculator.models.expression import (
    BinaryOperatorNode,
    ConstantNode,
    ExpressionNode,
    UnaryOperatorNode,
)
from cli_calculator.parsing.errors import (
    ExpressionFormatError,
    UnsupportedLexemeError,
    UnsupportedNodeTypeError,
)
from cli_calculator.parsing.parser import ExpressionParser


@pytest.mark.parametrize(
    "expression,tree",
    [
        ("2 + 2", BinaryOperatorNode(binary_operator_registry[ast.Add], ConstantNode(2), ConstantNode(2))),
        (
            "22.45 - 23.89",
            BinaryOperatorNode(binary_operator_registry[ast.Sub], ConstantNode(22.45), ConstantNode(23.89)),
        ),
        (
            "331.96 * 112.7",
            BinaryOperatorNode(binary_operator_registry[ast.Mult], ConstantNode(331.96), ConstantNode(112.7)),
        ),
        (
            "1379 / 9782",
            BinaryOperatorNode(binary_operator_registry[ast.Div], ConstantNode(1379), ConstantNode(9782)),
        ),
        (
            "-786",
            UnaryOperatorNode(unary_operator_registry[ast.USub], ConstantNode(786)),
        ),
        (
            "1234.15 / 1000.5 * -13 - 100",
            BinaryOperatorNode(
                binary_operator_registry[ast.Sub],
                BinaryOperatorNode(
                    binary_operator_registry[ast.Mult],
                    BinaryOperatorNode(
                        binary_operator_registry[ast.Div], ConstantNode(1234.15), ConstantNode(1000.5)
                    ),
                    UnaryOperatorNode(unary_operator_registry[ast.USub], ConstantNode(13)),
                ),
                ConstantNode(100),
            ),
        ),
    ],
)
def test_parser_general(expression: str, tree: ExpressionNode):
    root = ExpressionParser.parse_string(expression)
    assert root == tree


@pytest.mark.parametrize(
    "expression,error,message",
    [
        ("3 ! 3", ExpressionFormatError, "Wrong expression format. Unable to proceed to parsing"),
        ("2 + 2 ; -1", ExpressionFormatError, "Multiple or no expressions are unsupported"),
        ("", ExpressionFormatError, "Multiple or no expressions are unsupported"),
        ("2 & 2", UnsupportedLexemeError, "Binary operator BitAnd is not supported"),
        ("+2", UnsupportedLexemeError, "Unary operator UAdd is not supported"),
        ("await 3", UnsupportedNodeTypeError, "Unsupported node type: Await"),
        ("1 + 4j", ComplexConstantError, "Value 4j of type complex is not supported"),
    ],
)
def test_parser_errors(expression: str, error: type[Exception], message: str):
    with pytest.raises(error) as e_info:
        ExpressionParser.parse_string(expression)
    assert str(e_info.value) == message
