from cli_calculator.lexemes import OperatorSettings
from cli_calculator.models.expression import ExpressionNode


class Evaluator:
    def __init__(self, limit_floats: bool = True, use_degrees: bool = False) -> None:
        self.settings = OperatorSettings.NONE
        if limit_floats:
            self.settings |= OperatorSettings.LIMIT_FLOATS
        if use_degrees:
            self.settings |= OperatorSettings.USE_DEGREES

    def evaluate_tree(self, root: ExpressionNode) -> float:
        return root.evaluate(self.settings)
