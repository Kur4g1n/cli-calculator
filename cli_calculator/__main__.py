from argparse import ArgumentParser

from cli_calculator.evaluator import Evaluator
from cli_calculator.parsing.parser import ExpressionParser


def main():
    parser = ArgumentParser(description="Solves simple mathematical equations")
    parser.add_argument("expr", type=str, help="Expression to solve")
    args = parser.parse_args()

    expression: str = args.expr
    evaluator = Evaluator(limit_floats=True)
    expr_tree = ExpressionParser.parse_string(expression)
    solution = evaluator.evaluate_tree(expr_tree)

    print(solution)


if __name__ == "__main__":
    main()
