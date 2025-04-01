class ComplexConstantError(TypeError):
    def __init__(self, value: complex) -> None:
        super().__init__("Value %s of type complex is not supported" % value)
