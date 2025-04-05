class ExpressionOverflowError(OverflowError):
    def __init__(self, value):
        super().__init__(f"Value {value} exceeds maximum allowed value")
