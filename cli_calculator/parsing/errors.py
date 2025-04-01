from abc import ABCMeta


class ExpressionParsingError(TypeError): ...


class ExpressionFormatError(ValueError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class UnsupportedNodeTypeError(ExpressionParsingError):
    def __init__(self, node_type: str) -> None:
        super().__init__("Unsupported node type: %s" % node_type)


class UnsupportedLexemeError(ExpressionParsingError, metaclass=ABCMeta):
    def __init__(self, lexeme_title: str, operator_name: str) -> None:
        super().__init__("%s %s is not supported" % (lexeme_title, operator_name))
