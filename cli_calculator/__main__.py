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
        "--use_inf",
        action="store_true",
        help="Limits the maximum value of numbers in the expression",
    )
    args = parser.parse_args()

    expression: str = args.expr
    limit_floats: bool = not bool(args.use_inf)
    evaluator = Evaluator(limit_floats=limit_floats)
    expr_tree = ExpressionParser.parse_string(expression)
    solution = evaluator.evaluate_tree(expr_tree)

    print(solution)


if __name__ == "__main__":
    main()
