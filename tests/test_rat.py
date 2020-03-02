from fractions import Fraction
from pickle import dumps, loads

from pytest import fixture, raises  # noqa: F401

from donuts import Polynomial, RationalFunction, Variable, VariableSet


def test_init():
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

    with raises(TypeError):
        RationalFunction([1])  # invalid type

    with raises(TypeError):
        RationalFunction("1", 2)  # invalid type combinations

    with raises(TypeError):
        RationalFunction(Fraction(1, 2), 2)  # invalid type combinations

    with raises(TypeError):
        RationalFunction([1], [2])  # invalid types

    with raises(ValueError):
        RationalFunction("(1+x?)/(1-y)")  # invalid string

    with raises(ZeroDivisionError):
        RationalFunction(1, 0)  # division by zero

    with raises(ZeroDivisionError):
        a = Polynomial("1")
        b = Polynomial("0")
        RationalFunction(a, b)  # division by zero


def test_init_with_bigints(bigints):  # noqa: F811
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


def test_state():
    a = RationalFunction("(1+x+y)^3/(1-z-w)/2")
    s = dumps(a)
    b = loads(s)
    assert a == b
    assert a + b == a * 2


def test_repr():
    a = RationalFunction("(1+x)/(1+y)")
    b = eval(repr(a))
    assert a == b


def test_hash():
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


def test_bool():
    a = RationalFunction("0")
    assert not a

    a = RationalFunction("(-1+x)/(1-y)")
    assert a


def test_pos():
    a = RationalFunction("0")
    assert (+a) == a

    a = RationalFunction("(-1+x)/(1-y)")
    assert (+a) == a


def test_neg():
    a = RationalFunction("0")
    assert (-a) == a

    a = RationalFunction("(-1+x)/(1-y)")
    b = 0 - a
    assert (-a) == b
    assert (-b) == a


def test_add():
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


def test_sub():
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


def test_mul():
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


def test_div():
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
    with raises(ZeroDivisionError):
        a / b  # division by zero


def test_pow():
    a = RationalFunction("(1-x)/(1+x)")
    b = 3
    c = RationalFunction("(1-3*x+3*x^2-x^3)/(1+3*x+3*x^2+x^3)")
    assert a ** b == c

    a = RationalFunction("(1-x)/(1+x)")
    b = 0
    c = 1
    assert a ** b == c

    a = RationalFunction("(1-x)/(1+x)")
    b = -3
    c = RationalFunction("(1+3*x+3*x^2+x^3)/(1-3*x+3*x^2-x^3)")
    assert a ** b == c

    a = RationalFunction("0")
    b = 0
    c = 1
    assert a ** b == c  # NOTE: 0^0 = 1 in Python

    a = RationalFunction("0")
    with raises(ZeroDivisionError):
        a ** (-3)  # division by zero


def test_is():
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


def test_as_integer():
    a = 42
    b = RationalFunction(a)
    assert a == b.as_integer

    a = "x"
    b = RationalFunction(a)
    with raises(ValueError):
        b.as_integer  # not integer


def test_as_integer_with_bigints(bigints):  # noqa: F811
    for n in bigints:
        a = RationalFunction(n)
        assert a.as_integer == n


def test_as_fraction():
    a = 42
    b = RationalFunction(a)
    assert a == b.as_fraction

    a = Fraction(2, 3)
    b = RationalFunction(a)
    assert a == b.as_fraction

    a = "1+x"
    b = RationalFunction(a)
    with raises(ValueError):
        b.as_fraction  # not fraction


def test_as_polynomial():
    a = 42
    b = RationalFunction(a)
    assert a == b.as_polynomial

    a = Polynomial("1+2*x")
    b = RationalFunction(a)
    assert a == b.as_polynomial

    a = "x/2"
    b = RationalFunction(a)
    with raises(ValueError):
        b.as_polynomial  # not polynomial


def test_as_variable():
    a = Variable("x")
    b = RationalFunction(str(a))
    assert a == b.as_variable

    a = RationalFunction("x/2")
    with raises(ValueError):
        a.as_variable  # not variable


def test_variables():
    p = Polynomial("(1+x)*(1+y)")
    q = Polynomial("(1-z)*(1+y)")
    a = RationalFunction(p, q)
    assert a.variables == VariableSet("x", "y", "z")
    assert a.min_variables == VariableSet("x", "z")


def test_translate():
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

    with raises(TypeError):
        a.translate(1, 2)  # not variable

    with raises(ValueError):
        a.translate("w", "x", "y")  # doesn't fit


def test_subs():
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

    with raises(TypeError):
        a.subs(1, "x")  # lhs is not a polynomial

    with raises(TypeError):
        a.subs("x", [])  # rhs is not a polynomial

    with raises(ValueError):
        a.subs("2*x", 1)  # invalid lhs

    with raises(ValueError):
        a.subs("1+x", 1)  # invalid lhs

    with raises(ZeroDivisionError):
        a.subs("x", "-1-y")  # denominator becomes zero


def test_evaluate():
    a = RationalFunction("(1+x+y)^3/(1-x)/(1-z)").evaluate("x", 3)
    b = RationalFunction("-(4+y)^3/2/(1-z)")
    assert a == b

    a = RationalFunction("(1+x+y)^3/(1-x)/(1-z)").evaluate(
        [Variable("x"), "y"], [3, -2]
    )
    b = RationalFunction("-4/(1-z)")
    assert a == b

    with raises(TypeError):
        a.evaluate(["x"], 1)  # values must be also a collection

    with raises(ValueError):
        a.evaluate(["x"], [1, 2])  # different sizes

    with raises(TypeError):
        a.evaluate("x", "y")  # value must be an integer

    with raises(TypeError):
        a.evaluate(1, 1)  # invalid variables

    with raises(TypeError):
        a.evaluate(["x"], ["y"])  # values are not integers

    with raises(TypeError):
        a.evaluate([1], [1])  # not variables


def test_evaluate_at_zero():
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

    with raises(TypeError):
        a.evaluate_at_zero(1)  # not variable


def test_evaluate_at_one():
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

    with raises(TypeError):
        a.evaluate_at_one(1)  # not variable


def test_diff():
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

    with raises(TypeError):
        a.diff(1)  # x must be a Variable

    with raises(TypeError):
        a.diff(x, "x")  # n must be an int

    with raises(ValueError):
        a.diff(x, -1)  # n must be non-negative
