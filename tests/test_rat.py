from fractions import Fraction
from pickle import dumps, loads
from typing import Union

import pytest
from conftest import BigIntSeq

from donuts import Polynomial, RationalFunction, Variable
from donuts.poly import PolynomialLike
from donuts.rat import RationalFunctionLike
from donuts.varset import VariableSet, VariableSetLike


def test_init() -> None:
    a: RationalFunctionLike
    b: RationalFunctionLike

    a = RationalFunction()
    assert a == 0
    assert str(a) == "0"

    a = 42
    b = RationalFunction(a)
    assert a == b
    assert str(a) == str(b)

    a = Fraction(3, 2)
    b = RationalFunction(a)
    assert a == b

    a = Variable("x")
    b = RationalFunction(a)
    assert str(a) == str(b)

    a = Polynomial("1+x")
    b = RationalFunction(a)
    assert a == b

    a = RationalFunction("(1+x)/(1-y)")
    b = RationalFunction(a)
    assert a == b

    with pytest.raises(TypeError):
        RationalFunction([1])  # type: ignore[arg-type]  # invalid type

    with pytest.raises(TypeError):
        RationalFunction("1", 2)  # invalid type combinations

    with pytest.raises(TypeError):
        RationalFunction(Fraction(1, 2), 2)  # invalid type combinations

    with pytest.raises(TypeError):
        RationalFunction([1], [2])  # type: ignore[arg-type]  # invalid types

    with pytest.raises(ValueError, match="invalid string for rational function"):
        RationalFunction("(1+x?)/(1-y)")

    with pytest.raises(ZeroDivisionError):
        RationalFunction(1, 0)  # division by zero

    a = Polynomial("1")
    b = Polynomial("0")
    with pytest.raises(ZeroDivisionError):
        RationalFunction(a, b)  # division by zero


def test_init_with_bigints(bigints: BigIntSeq) -> None:
    for n in bigints:
        a = RationalFunction(n)
        b = RationalFunction(str(n))
        assert a == b

    for m in bigints:
        for n in bigints:
            if n != 0:
                a = RationalFunction(m, n)
                b = RationalFunction(Fraction(m, n))
                c = RationalFunction(f"({m})/({n})")
                assert a == b
                assert a == c


def test_state() -> None:
    a = RationalFunction("(1+x+y)^3/(1-z-w)/2")
    s = dumps(a)
    b = loads(s)
    assert a == b
    assert a + b == a * 2


def test_repr() -> None:
    a = RationalFunction("(1+x)/(1+y)")
    b = eval(repr(a))
    assert a == b


def test_hash() -> None:
    a: RationalFunctionLike
    b: RationalFunctionLike

    a = 42
    b = RationalFunction(a)
    assert a == b
    assert hash(a) == hash(b)

    a = Fraction(3, 2)
    b = RationalFunction(a)
    assert a == b
    assert hash(a) == hash(b)

    a = Variable("x")
    b = RationalFunction(a)
    assert a == b
    assert hash(a) == hash(b)

    a = Polynomial("a*d")
    b = RationalFunction("(a+b)*(c+d)-a*c-b*c-b*d")
    assert a == b
    assert hash(a) == hash(b)

    a = RationalFunction("1+x/y")
    b = RationalFunction("(a+b)*(c+d)-(a+b)*(c+d)+1+x/y*(1-z)/(1-z)")
    assert a == b
    assert hash(a) == hash(b)


def test_bool() -> None:
    a = RationalFunction("0")
    assert not a

    a = RationalFunction("(-1+x)/(1-y)")
    assert a


def test_pos() -> None:
    a = RationalFunction("0")
    assert (+a) == a

    a = RationalFunction("(-1+x)/(1-y)")
    assert (+a) == a


def test_neg() -> None:
    a = RationalFunction("0")
    assert (-a) == a

    a = RationalFunction("(-1+x)/(1-y)")
    b = 0 - a
    assert (-a) == b
    assert (-b) == a


def test_add() -> None:
    a: RationalFunctionLike
    b: RationalFunctionLike
    c: RationalFunctionLike

    a = RationalFunction("(1+x)/(1-z)")
    b = RationalFunction("(-1+y)/(1-z)")
    c = RationalFunction("(x+y)/(1-z)")
    assert a + b == c

    a = RationalFunction("(1+x)/(1-z)")
    b = Polynomial("-1+y")
    c = RationalFunction("(-x-y-z+y*z)/(-1+z)")
    assert a + b == c

    a = Polynomial("1+x")
    b = RationalFunction("(-1+y)/(1-z)")
    c = RationalFunction("(-x-y+z+x*z)/(-1+z)")
    assert a + b == c


def test_sub() -> None:
    a: RationalFunctionLike
    b: RationalFunctionLike
    c: RationalFunctionLike

    a = RationalFunction("(1+x)/(1-z)")
    b = RationalFunction("(-1+y)/(1-z)")
    c = RationalFunction("-(2+x-y)/(-1+z)")
    assert a - b == c

    a = RationalFunction("(1+x)/(1-z)")
    b = Polynomial("-1+y")
    c = RationalFunction("-(2+x-y-z+y*z)/(-1+z)")
    assert a - b == c

    a = Polynomial("1+x")
    b = RationalFunction("(-1+y)/(1-z)")
    c = RationalFunction("(-2-x+y+z+x*z)/(-1+z)")
    assert a - b == c


def test_mul() -> None:
    a: RationalFunctionLike
    b: RationalFunctionLike
    c: RationalFunctionLike

    a = RationalFunction("(1+x)/(1-z)")
    b = RationalFunction("(-1+y)/(1-z)")
    c = RationalFunction("(1+x)*(-1+y)/(-1+z)^2")
    assert a * b == c

    a = RationalFunction("(1+x)/(1-z)")
    b = Polynomial("-1+y")
    c = RationalFunction("-((1+x)*(-1+y)/(-1+z))")
    assert a * b == c

    a = Polynomial("1+x")
    b = RationalFunction("(-1+y)/(1-z)")
    c = RationalFunction("-(1+x)*(-1+y)/(-1+z)")
    assert a * b == c


def test_div() -> None:
    a: RationalFunctionLike
    b: RationalFunctionLike
    c: RationalFunctionLike

    a = RationalFunction("(1+x)/(1-z)")
    b = RationalFunction("(-1+y)/(1-z)")
    c = RationalFunction("(1+x)/(-1+y)")
    assert a / b == c

    a = RationalFunction("(1+x)/(1-z)")
    b = Polynomial("-1+y")
    c = RationalFunction("-(1+x)/(-1+y)/(-1+z)")
    assert a / b == c

    a = Polynomial("1+x")
    b = RationalFunction("(-1+y)/(1-z)")
    c = RationalFunction("-(1+x)*(-1+z)/(-1+y)")
    assert a / b == c

    a = RationalFunction("(1+x)/(1-z)")
    b = RationalFunction("(1+x)*(1-y)/(1+x)-(1-y)")
    with pytest.raises(ZeroDivisionError):
        a / b  # division by zero


def test_pow() -> None:
    a: RationalFunctionLike
    b: int
    c: RationalFunctionLike

    a = RationalFunction("(1-x)/(1+x)")
    b = 3
    c = RationalFunction("(1-3*x+3*x^2-x^3)/(1+3*x+3*x^2+x^3)")
    assert a**b == c

    a = RationalFunction("(1-x)/(1+x)")
    b = 0
    c = 1
    assert a**b == c

    a = RationalFunction("(1-x)/(1+x)")
    b = -3
    c = RationalFunction("(1+3*x+3*x^2+x^3)/(1-3*x+3*x^2-x^3)")
    assert a**b == c

    a = RationalFunction("0")
    b = 0
    c = 1
    assert a**b == c  # NOTE: 0^0 = 1 in Python

    a = RationalFunction("0")
    with pytest.raises(ZeroDivisionError):
        a ** (-3)  # division by zero


def test_is() -> None:
    a = RationalFunction("0")
    assert a.is_zero
    assert not a.is_one
    assert not a.is_minus_one
    assert a.is_integer
    assert a.is_fraction
    assert not a.is_variable
    assert a.is_polynomial

    a = RationalFunction("1")
    assert not a.is_zero
    assert a.is_one
    assert not a.is_minus_one
    assert a.is_integer
    assert a.is_fraction
    assert not a.is_variable
    assert a.is_polynomial

    a = RationalFunction("-1")
    assert not a.is_zero
    assert not a.is_one
    assert a.is_minus_one
    assert a.is_integer
    assert a.is_fraction
    assert not a.is_variable
    assert a.is_polynomial

    a = RationalFunction("41")
    assert not a.is_zero
    assert not a.is_one
    assert not a.is_minus_one
    assert a.is_integer
    assert a.is_fraction
    assert not a.is_variable
    assert a.is_polynomial

    a = RationalFunction("41/11")
    assert not a.is_zero
    assert not a.is_one
    assert not a.is_minus_one
    assert not a.is_integer
    assert a.is_fraction
    assert not a.is_variable
    assert not a.is_polynomial

    a = RationalFunction("x")
    assert not a.is_zero
    assert not a.is_one
    assert not a.is_minus_one
    assert not a.is_integer
    assert not a.is_fraction
    assert a.is_variable
    assert a.is_polynomial

    a = RationalFunction("2*x")
    assert not a.is_zero
    assert not a.is_one
    assert not a.is_minus_one
    assert not a.is_integer
    assert not a.is_fraction
    assert not a.is_variable
    assert a.is_polynomial

    a = RationalFunction("1+x/3")
    assert not a.is_zero
    assert not a.is_one
    assert not a.is_minus_one
    assert not a.is_integer
    assert not a.is_fraction
    assert not a.is_variable
    assert not a.is_polynomial


def test_as_integer() -> None:
    a: Union[int, str]

    a = 42
    b = RationalFunction(a)
    assert a == b.as_integer

    a = "x"
    b = RationalFunction("x")
    with pytest.raises(ValueError, match="not an integer"):
        b.as_integer


def test_as_integer_with_bigints(bigints: BigIntSeq) -> None:
    for n in bigints:
        a = RationalFunction(n)
        assert a.as_integer == n


def test_as_fraction() -> None:
    a: Union[Fraction, int, str]

    a = 42
    b = RationalFunction(a)
    assert a == b.as_fraction

    a = Fraction(2, 3)
    b = RationalFunction(a)
    assert a == b.as_fraction

    a = "1+x"
    b = RationalFunction(a)
    with pytest.raises(ValueError, match="not a rational number"):
        b.as_fraction


def test_as_polynomial() -> None:
    a: Union[PolynomialLike, str]

    a = 42
    b = RationalFunction(a)
    assert a == b.as_polynomial

    a = Polynomial("1+2*x")
    b = RationalFunction(a)
    assert a == b.as_polynomial

    a = "x/2"
    b = RationalFunction(a)
    with pytest.raises(ValueError, match="not a polynomial"):
        b.as_polynomial


def test_as_variable() -> None:
    a: RationalFunctionLike

    a = Variable("x")
    b = RationalFunction(str(a))
    assert a == b.as_variable

    a = RationalFunction("x/2")
    with pytest.raises(ValueError, match="not a variable"):
        a.as_variable


def test_variables() -> None:
    p = Polynomial("(1+x)*(1+y)")
    q = Polynomial("(1-z)*(1+y)")
    a = RationalFunction(p, q)
    assert a.variables == VariableSet("x", "y", "z")
    assert a.min_variables == VariableSet("x", "z")


def test_translate() -> None:
    s: VariableSetLike

    a = RationalFunction("(1-x)/(1+y)+x/(1+y)-1/(1+z)")

    s = ["a", "x", "y", "z"]
    v = VariableSet(*s)
    b = a.translate(s)
    assert b == a
    assert b.variables == v

    s = [Variable("a"), Variable("x"), Variable("y"), Variable("z")]
    v = VariableSet(*s)
    b = a.translate(s)
    assert b == a
    assert b.variables == v

    # expansion
    v = VariableSet("a", "x", "y", "z", "zz")
    b = a.translate(v)
    assert b == a
    assert b.variables == v

    # minimization
    v = VariableSet("y", "z")
    b = a.translate(v)
    assert b == a
    assert b.variables == v

    # minimization and then expansion
    v = VariableSet("a", "y", "z")
    b = a.translate(v)
    assert b == a
    assert b.variables == v

    with pytest.raises(TypeError):
        a.translate(1, 2)  # type: ignore[call-overload]  # not variable

    with pytest.raises(ValueError, match="invalid set of variables"):
        a.translate("w", "x", "y")


def test_subs() -> None:
    a: RationalFunctionLike
    lhs: Union[Polynomial, str]
    rhs: Union[RationalFunctionLike, str]
    b: RationalFunctionLike

    a = RationalFunction("(1+x-y)^2/(1+x+y)^2")
    lhs = Polynomial("x")
    rhs = RationalFunction("1/y")
    b = RationalFunction("(1+y-y^2)^2/(1+y+y^2)^2")
    assert a.subs(lhs, rhs) == b

    a = RationalFunction("(1+x-y)^2/(1+x+y)^2")
    lhs = "x"
    rhs = "1/y"
    b = RationalFunction("(1+y-y^2)^2/(1+y+y^2)^2")
    assert a.subs(lhs, rhs) == b

    with pytest.raises(TypeError):
        a.subs(1, "x")  # type: ignore[arg-type]  # lhs is not a polynomial

    with pytest.raises(TypeError):
        a.subs("x", [])  # type: ignore[arg-type]  # rhs is not a polynomial

    with pytest.raises(ValueError, match="invalid lhs for substitution"):
        a.subs("2*x", 1)

    with pytest.raises(ValueError, match="invalid lhs for substitution"):
        a.subs("1+x", 1)

    with pytest.raises(ZeroDivisionError):
        a.subs("x", "-1-y")  # denominator becomes zero


def test_evaluate() -> None:
    a = RationalFunction("(1+x+y)^3/(1-x)/(1-z)").evaluate("x", 3)
    b = RationalFunction("-(4+y)^3/2/(1-z)")
    assert a == b

    a = RationalFunction("(1+x+y)^3/(1-x)/(1-z)").evaluate(
        [Variable("x"), "y"], [3, -2]
    )
    b = RationalFunction("-4/(1-z)")
    assert a == b

    with pytest.raises(TypeError):
        a.evaluate(
            ["x"], 1
        )  # type: ignore[call-overload]  # values must be also a collection

    with pytest.raises(ValueError, match="variables and values have different sizes"):
        a.evaluate(["x"], [1, 2])

    with pytest.raises(TypeError):
        a.evaluate("x", "y")  # type: ignore[arg-type]  # value must be an integer

    with pytest.raises(TypeError):
        a.evaluate(1, 1)  # type: ignore[call-overload]  # invalid variables

    with pytest.raises(TypeError):
        a.evaluate(["x"], ["y"])  # type: ignore[list-item]  # values are not integers

    with pytest.raises(TypeError):
        a.evaluate([1], [1])  # type: ignore[list-item]  # not variables

    with pytest.raises(ZeroDivisionError):
        RationalFunction("(1+x+y)/(2-x)").evaluate("x", 2)

    with pytest.raises(ZeroDivisionError):
        RationalFunction("(1+x+y)/(5-x-y)").evaluate(["x", "y"], [2, 3])


def test_evaluate_at_zero() -> None:
    a = RationalFunction("(1+x)^3/(3-x-y)").evaluate_at_zero(Variable("x"))
    b = RationalFunction("1/(3-y)")
    assert a == b

    a = RationalFunction("(1+x)^3/(3-x-y)").evaluate_at_zero(["x", "y", "z"])
    b = RationalFunction("1/3")
    assert a == b

    a = RationalFunction("(1+x)^3/(3-x-y)").evaluate_at_zero([])
    b = RationalFunction("(1+x)^3/(3-x-y)")
    assert a == b

    a = RationalFunction("(1+x)^3/(3-x-y)").evaluate_at_zero()
    b = RationalFunction("(1+x)^3/(3-x-y)")
    assert a == b

    with pytest.raises(TypeError):
        a.evaluate_at_zero(1)  # type: ignore[call-overload]  # not variable

    with pytest.raises(ZeroDivisionError):
        RationalFunction("(1+x+y)/x").evaluate_at_zero("x")

    with pytest.raises(ZeroDivisionError):
        RationalFunction("(1+x+y)/(x-y)").evaluate_at_zero(["x", "y"])


def test_evaluate_at_one() -> None:
    a = RationalFunction("(1+x)^3/(3-x-y)").evaluate_at_one(Variable("x"))
    b = RationalFunction("8/(2-y)")
    assert a == b

    a = RationalFunction("(1+x)^3/(3-x-y)").evaluate_at_one(["x", "y", "z"])
    b = RationalFunction("8")
    assert a == b

    a = RationalFunction("(1+x)^3/(3-x-y)").evaluate_at_one([])
    b = RationalFunction("(1+x)^3/(3-x-y)")
    assert a == b

    a = RationalFunction("(1+x)^3/(3-x-y)").evaluate_at_one()
    b = RationalFunction("(1+x)^3/(3-x-y)")
    assert a == b

    with pytest.raises(TypeError):
        a.evaluate_at_one(1)  # type: ignore[call-overload]  # not variable

    with pytest.raises(ZeroDivisionError):
        RationalFunction("(1+x+y)/(1-x)").evaluate_at_one("x")

    with pytest.raises(ZeroDivisionError):
        RationalFunction("(1+x+y)/(x-y)").evaluate_at_one(["x", "y"])


def test_shift() -> None:
    a = RationalFunction("(1+x+2*y)^3/(3-x)").shift("x", 3)
    b = RationalFunction("-(4+x+2*y)^3/x")
    assert a == b

    a = RationalFunction("(1+x+2*y)^3/(3-x)/y").shift([Variable("x"), "y"], [3, -2])
    b = RationalFunction("-(x+2*y)^3/x/(y-2)")
    assert a == b

    with pytest.raises(TypeError):
        a.shift(
            ["x"], 1
        )  # type: ignore[call-overload]  # values must be also a collection

    with pytest.raises(ValueError, match="variables and values have different sizes"):
        a.shift(["x"], [1, 2])

    with pytest.raises(TypeError):
        a.shift("x", "y")  # type: ignore[arg-type]  # value must be an integer

    with pytest.raises(TypeError):
        a.shift(1, 1)  # type: ignore[call-overload]  # invalid variables

    with pytest.raises(TypeError):
        a.shift(["x"], ["y"])  # type: ignore[list-item]  # values are not integers

    with pytest.raises(TypeError):
        a.shift([1], [1])  # type: ignore[list-item]  # not variables


def test_diff() -> None:
    a = RationalFunction("(1+x+y)^2/(1/2+x-y*x^5)")
    x = Variable("x")
    assert a.diff(x) == RationalFunction(
        "(4*(1+x+y)*(x-y+5*x^4*y+3*x^5*y+5*x^4*y^2))/(-1-2*x+2*x^5*y)^2"
    )

    a = RationalFunction("(1+x+y)/(1-x-y)")
    assert a.diff("y") == RationalFunction("2/(1-x-y)^2")

    a = RationalFunction("(1+x)/(1-x)")
    assert a.diff("x", 0) == a
    assert a.diff("x", 1) == RationalFunction("2/(1-x)^2")
    assert a.diff("x", 2) == RationalFunction("4/(1-x)^3")

    with pytest.raises(TypeError):
        a.diff(1)  # type: ignore[arg-type]  # x must be a Variable

    with pytest.raises(TypeError):
        a.diff(x, "x")  # type: ignore[arg-type]  # n must be an int

    with pytest.raises(ValueError, match="n must be non-negative"):
        a.diff(x, -1)
