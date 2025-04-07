import ast
import pytest

from cli_calculator.lexemes import (
    unary_operator_registry,
    binary_operator_registry,
    constant_registry,
    function_registry,
)
from cli_calculator.models.expression import (
    BinaryOperatorNode,
    ConstantNode,
    ExpressionNode,
    FunctionCallNode,
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
        (
            "2 + e",
            BinaryOperatorNode(
                binary_operator_registry[ast.Add],
                ConstantNode(constant_registry[ast.Constant], 2),
                ConstantNode(constant_registry["e"], 0),
            ),
        ),
        (
            "22.45 - 23.89",
            BinaryOperatorNode(
                binary_operator_registry[ast.Sub],
                ConstantNode(constant_registry[ast.Constant], 22.45),
                ConstantNode(constant_registry[ast.Constant], 23.89),
            ),
        ),
        (
            "331.96 * 112.7",
            BinaryOperatorNode(
                binary_operator_registry[ast.Mult],
                ConstantNode(constant_registry[ast.Constant], 331.96),
                ConstantNode(constant_registry[ast.Constant], 112.7),
            ),
        ),
        (
            "1379 / 9782",
            BinaryOperatorNode(
                binary_operator_registry[ast.Div],
                ConstantNode(constant_registry[ast.Constant], 1379),
                ConstantNode(constant_registry[ast.Constant], 9782),
            ),
        ),
        (
            "pi ^ e",
            BinaryOperatorNode(
                binary_operator_registry[ast.Pow],
                ConstantNode(constant_registry["pi"], 0),
                ConstantNode(constant_registry["e"], 0),
            ),
        ),
        (
            "ln(1)",
            FunctionCallNode(
                function_registry["ln"], [ConstantNode(constant_registry[ast.Constant], 1)]
            ),
        ),
        (
            "exp(3.123)",
            FunctionCallNode(
                function_registry["exp"], [ConstantNode(constant_registry[ast.Constant], 3.123)]
            ),
        ),
        (
            "sqrt(12)",
            FunctionCallNode(
                function_registry["sqrt"], [ConstantNode(constant_registry[ast.Constant], 12)]
            ),
        ),
        (
            "sin(90)",
            FunctionCallNode(
                function_registry["sin"], [ConstantNode(constant_registry[ast.Constant], 90)]
            ),
        ),
        (
            "cos(3)",
            FunctionCallNode(
                function_registry["cos"], [ConstantNode(constant_registry[ast.Constant], 3)]
            ),
        ),
        (
            "tg(pi)",
            FunctionCallNode(
                function_registry["tg"], [ConstantNode(constant_registry["pi"], 0)]
            ),
        ),
        (
            "ctg(90.321)",
            FunctionCallNode(
                function_registry["ctg"], [ConstantNode(constant_registry[ast.Constant], 90.321)]
            ),
        ),
        (
            "-786",
            UnaryOperatorNode(
                unary_operator_registry[ast.USub],
                ConstantNode(constant_registry[ast.Constant], 786),
            ),
        ),
        (
            "1234.15 / 1000.5 * -13 - pi",
            BinaryOperatorNode(
                binary_operator_registry[ast.Sub],
                BinaryOperatorNode(
                    binary_operator_registry[ast.Mult],
                    BinaryOperatorNode(
                        binary_operator_registry[ast.Div],
                        ConstantNode(constant_registry[ast.Constant], 1234.15),
                        ConstantNode(constant_registry[ast.Constant], 1000.5),
                    ),
                    UnaryOperatorNode(
                        unary_operator_registry[ast.USub],
                        ConstantNode(constant_registry[ast.Constant], 13),
                    ),
                ),
                ConstantNode(constant_registry["pi"], 0),
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
    ],
)
def test_parser_errors(expression: str, error: type[Exception], message: str):
    with pytest.raises(error) as e_info:
        ExpressionParser.parse_string(expression)
    assert str(e_info.value) == message
