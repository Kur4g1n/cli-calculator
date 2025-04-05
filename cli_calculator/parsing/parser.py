import ast

from cli_calculator.lexemes import (binary_operator_registry,
                                    function_registry, unary_operator_registry)
from cli_calculator.models.expression import (BinaryOperatorNode, ConstantNode,
                                              ExpressionNode, FunctionCallNode,
                                              UnaryOperatorNode)
from cli_calculator.parsing.errors import (ExpressionFormatError,
                                           UnsupportedLexemeError,
                                           UnsupportedNodeTypeError)


class ExpressionParser:
    permitted_unary_operators = unary_operator_registry
    permitted_binary_operators = binary_operator_registry
    permitted_functions = function_registry

    @classmethod
    def parse_string(cls, expression: str) -> ExpressionNode:
        try:
            parsed_expression = ast.parse(cls._format_string(expression))
            body = parsed_expression.body
        # Unexpected errors are supposed to be raised
        except SyntaxError:
            raise ExpressionFormatError("Wrong expression format. Unable to proceed to parsing")

        if len(body) != 1:
            raise ExpressionFormatError("Multiple or no expressions are unsupported")

        return cls._parse_node(body[0])

    @classmethod
    def _parse_node(cls, node: ast.expr | ast.stmt) -> ExpressionNode:
        if isinstance(node, ast.Expr):
            return cls._parse_node(node.value)
        elif isinstance(node, ast.BinOp):
            ast_operator_type = type(node.op)

            if ast_operator_type not in cls.permitted_binary_operators:
                raise UnsupportedLexemeError("Binary operator", node.op.__class__.__name__)
            return BinaryOperatorNode(
                operation=cls.permitted_binary_operators[ast_operator_type],
                left=cls._parse_node(node.left),
                right=cls._parse_node(node.right),
            )

        elif isinstance(node, ast.UnaryOp):
            ast_operator_type = type(node.op)

            if ast_operator_type not in cls.permitted_unary_operators:
                raise UnsupportedLexemeError("Unary operator", node.op.__class__.__name__)

            return UnaryOperatorNode(
                operation=cls.permitted_unary_operators[ast_operator_type],
                value=cls._parse_node(node.operand),
            )

        elif isinstance(node, ast.Call):
            function = node.func
            if not isinstance(function, ast.Name):
                raise UnsupportedNodeTypeError(function.__class__.__name__)

            if function.id not in cls.permitted_functions:
                raise UnsupportedLexemeError("Function", function.id)

            if len(node.keywords) != 0:
                raise UnsupportedLexemeError("Keywords", str(node.keywords))

            func = cls.permitted_functions[function.id]
            args = [cls._parse_node(arg) for arg in node.args]
            return FunctionCallNode(func, args)

        elif isinstance(node, ast.Constant):
            return ConstantNode(value=node.value)

        else:
            raise UnsupportedNodeTypeError(node.__class__.__name__)

    @staticmethod
    def _format_string(string: str) -> str:
        return string.strip().replace("**", "!").replace("^", "**")
