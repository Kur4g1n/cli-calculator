from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass

from cli_calculator.lexemes import BinaryOpT, FuncT, OperatorSettings, UnaryOpT


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
    validator: Callable
    value: int | float | complex = 0

    def evaluate(self, settings: OperatorSettings) -> float:
        return self.validator(settings, self.value)


@dataclass
class FunctionCallNode(ExpressionNode):
    function: FuncT
    arguments: list[ExpressionNode]

    def evaluate(self, settings: OperatorSettings) -> float:
        return self.function(settings, *[arg.evaluate(settings) for arg in self.arguments])
