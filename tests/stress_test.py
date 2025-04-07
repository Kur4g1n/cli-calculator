import pytest
import time
from cli_calculator.evaluator import Evaluator
from cli_calculator.parsing.parser import ExpressionParser

MAX_TIME_MS = 200


@pytest.mark.stress
@pytest.mark.parametrize(
    "expression, expected",
    [
        (" + ".join(["1"] * 250), 250),
        (" * ".join(["2"] * 100), 2**100),
        (" - ".join(["100"] + ["1"] * 150), -50),
        ("2 ^ " + "(" + " + ".join(["1"] * 100) + ")", None),
        ("sqrt(" * 50 + "16" + ")" * 50, 1.000000000000002),
        ("sin(" + " + ".join(["0.1"] * 200) + ")", None),
        (" + ".join(["1"] * 50) + " * 2 + " + " / ".join(["100"] * 50), None),
        ("(" * 100 + "1" + ")" * 100, 1),
        ("pi + " + " + ".join(["e"] * 100), None),
        ("1 + 2 * 3 ^ 2 - " + " / ".join(["5"] * 80), None),
        ("2 + 3 * 4 + " + " & " * 100 + "5", None),
        ("1e50 * " + " * ".join(["2"] * 50), None),
        ("1 + " * 250 + "1", None),
        ("cos(" * 50 + "0" + ")" * 50, 0.7390851321663373),
        ("sqrt(4) + ln(exp(1)) * " + " + ".join(["1"] * 100), None),
    ],
)
def test_stress_evaluator(expression: str, expected: float):
    parser = ExpressionParser()
    evaluator = Evaluator()

    start_time = time.time()
    try:
        tree = parser.parse_string(expression)
        result = evaluator.evaluate_tree(tree)
        duration_ms = (time.time() - start_time) * 1000

        assert duration_ms <= MAX_TIME_MS, f"Time {duration_ms:.2f}ms exceeds {MAX_TIME_MS}ms"
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        assert duration_ms <= MAX_TIME_MS, f"Time {duration_ms:.2f}ms exceeds {MAX_TIME_MS}ms"
        if expected is not None:
            pytest.fail("Unexpected exception: %s" % str(e))

    if expected is not None:
        assert result == pytest.approx(expected, 1e-11), f"Expected {expected}, got {result}"
