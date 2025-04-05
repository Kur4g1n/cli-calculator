from typing import Type


class ExpressionOverflowError(OverflowError):
    def __init__(self, value):
        super().__init__(f"Value {value} exceeds maximum allowed value")

class ArgumentNumberError(TypeError):
    def __init__(self, num: int, expected: int):
        super().__init__(f"Function accepts {expected} arguments. {num} were given.")
