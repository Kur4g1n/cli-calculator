from argparse import ArgumentParser

from cli_calculator.evaluator import Evaluator
from cli_calculator.parsing.parser import ExpressionParser


def main():
    parser = ArgumentParser(description="Solves simple mathematical equations")
    parser.add_argument(
        "expr",
        type=str,
        help="Expression to solve. Accepts basic arithmetic operations. "
        "Supports addition, subtraction, multiplication, and division.",
    )
    parser.add_argument(
        "-l",
        "--allow_inf",
        action="store_true",
        help="Allows the use of very large numbers in the expression",
    )
    parser.add_argument(
        "-r",
        "--use_deg",
        action="store_true",
        help="Use degrees instead of radians as the angle unit",
    )
    args = parser.parse_args()

    expression: str = args.expr
    limit_floats: bool = not bool(args.allow_inf)
    use_degrees: bool = args.use_deg
    evaluator = Evaluator(limit_floats=limit_floats, use_degrees=use_degrees)
    expr_tree = ExpressionParser.parse_string(expression)
    solution = evaluator.evaluate_tree(expr_tree)

    print(solution)


if __name__ == "__main__":
    main()
