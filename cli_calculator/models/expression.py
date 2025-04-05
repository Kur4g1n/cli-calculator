from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from cli_calculator.lexemes import BinaryOpT, OperatorSettings, UnaryOpT
from cli_calculator.models.errors import ComplexConstantError


class ExpressionNode(metaclass=ABCMeta):
    @abstractmethod
    def evaluate(self, settings: OperatorSettings) -> float: ...


@dataclass
class BinaryOperatorNode(ExpressionNode):
    operation: BinaryOpT
    left: ExpressionNode
    right: ExpressionNode

    def evaluate(self, settings: OperatorSettings) -> float:
        return self.operation(settings, self.left.evaluate(settings), self.right.evaluate(settings))


@dataclass
class UnaryOperatorNode(ExpressionNode):
    operation: UnaryOpT
    value: ExpressionNode

    def evaluate(self, settings: OperatorSettings) -> float:
        return self.operation(settings, self.value.evaluate(settings))


@dataclass
class ConstantNode(ExpressionNode):
    def __init__(self, value: int | float | complex) -> None:
        if isinstance(value, complex):
            raise ComplexConstantError(value)

        self.value = float(value)

    def evaluate(self, settings: OperatorSettings) -> float:
        return self.value
