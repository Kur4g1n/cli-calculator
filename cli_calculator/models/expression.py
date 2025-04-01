from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass

from cli_calculator.models.errors import ComplexConstantError


class ExpressionNode(metaclass=ABCMeta):
    @abstractmethod
    def evaluate(self) -> float: ...


@dataclass
class BinaryOperatorNode(ExpressionNode):
    operation: Callable[[float, float], float]
    left: ExpressionNode
    right: ExpressionNode

    def evaluate(self) -> float:
        return self.operation(self.left.evaluate(), self.right.evaluate())


@dataclass
class UnaryOperatorNode(ExpressionNode):
    operation: Callable[[float], float]
    value: ExpressionNode

    def evaluate(self) -> float:
        return self.operation(self.value.evaluate())


@dataclass
class ConstantNode(ExpressionNode):
    def __init__(self, value: int | float | complex) -> None:
        if isinstance(value, complex):
            raise ComplexConstantError(value)

        self.value = float(value)

    def evaluate(self) -> float:
        return self.value
