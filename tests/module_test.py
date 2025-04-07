import subprocess
import pytest
import math

CALCULATORCMD = ["python", "-m", "cli_calculator"]


@pytest.mark.parametrize(
    "args, expectedoutput",
    [
        (["2.5 + 3.7"], "6.2"),
        (["-4.2 * 2.5"], "-10.5"),
        (["10.5 / 2 + 3.1"], "8.35"),
        (["2.0 ^ 3.0 - 1.5"], "6.5"),
        (["-2.5 * (3.1 + 1.2)"], "-10.75"),
        (["15.7 / -3.0 + 2.1"], "-3.13333333333"),
        (["sin(0)", "--use_deg"], "0"),
        (["cos(0)", "--use_deg"], "1"),
        (["tg(0)", "--use_deg"], "0"),
        (["ln(1)"], "0"),
        (["exp(0)"], "1"),
        (["ctg(90)", "--use_deg"], "0"),
        (["sqrt(4.0)"], "2"),
        (["sin(90) * 2", "--use_deg"], "2"),
        (["sqrt(2.25) + ln(exp(1))"], "2.5"),
    ],
)
def test_cli_calculator_degrees(args, expectedoutput):
    result = subprocess.run(CALCULATORCMD + args, capture_output=True, text=True, check=True)
    assert float(result.stdout.strip()) == pytest.approx(float(expectedoutput), 1e-11)


@pytest.mark.parametrize(
    "args, expectedoutput",
    [
        (["sin(pi)"], "0"),
        (["cos(pi/2)"], "0"),
        (["tg(pi/4)"], "1"),
        (["ln(e^2)"], "2"),
        (["exp(pi)"], str(math.exp(math.pi))),
        (["ctg(pi/2)"], "0"),
        (["sqrt(4.0)"], "2"),
        (["sin(pi/2) * 2"], "2"),
        (["sqrt(2.25) + ln(exp(1))"], "2.5"),
    ],
)
def test_clicalculator_radians(args, expectedoutput):
    result = subprocess.run(CALCULATORCMD + args, capture_output=True, text=True, check=True)
    assert float(result.stdout.strip()) == pytest.approx(float(expectedoutput), 1e-11)


@pytest.mark.parametrize(
    "args, expectederror, errormessage",
    [
        (["3.1 ! 2.5"], subprocess.CalledProcessError, "Wrong expression format"),
        (["2.5 + 1.7 ; -3.2"], subprocess.CalledProcessError, "Multiple or no expressions"),
        ([""], subprocess.CalledProcessError, "Multiple or no expressions"),
        (["2.1 & 3.2"], subprocess.CalledProcessError, "Binary operator BitAnd"),
        (["+2.5"], subprocess.CalledProcessError, "Unary operator UAdd"),
        (["1e999 * 2.5"], subprocess.CalledProcessError, "Value inf exceeds"),
        (["sin(1, 2)"], subprocess.CalledProcessError, "Function accepts 1 arguments. 2 were given"),
        (["cos()"], subprocess.CalledProcessError, "Function accepts 1 arguments. 0 were given"),
        (
            ["sqrt(1, 2, 3)"],
            subprocess.CalledProcessError,
            "Function accepts 1 arguments. 3 were given",
        ),
    ],
)
def test_clicalculator_errors(args, expectederror, errormessage):
    with pytest.raises(expectederror) as einfo:
        subprocess.run(CALCULATORCMD + args, capture_output=True, text=True, check=True)
    assert errormessage in einfo.value.stderr
