from fractions import Fraction
from pickle import dumps, loads

from pytest import raises

import donuts
from donuts import Polynomial, RationalFunction, Variable, VariableSet


def test_init():
    a = Polynomial()
    assert a == 0
    assert str(a) == "0"

    a = Polynomial(42)
    assert a == 42
    assert str(a) == "42"

    a = Polynomial("a")
    assert str(a) == "a"

    a = Polynomial(Variable("a"))
    assert str(a) == "a"

    a = Polynomial(a)
    assert str(a) == "a"

    with raises(TypeError):
        Polynomial([1])  # invalid type

    with raises(ValueError):
        Polynomial("(1+x)/(1-y)")  # not polynomial

    with raises(ValueError):
        Polynomial("x?")  # invalid string


def test_init_with_bigints(bigints):  # noqa: F811
    for n in bigints:
        a = Polynomial(n)
        b = Polynomial(str(n))
        assert a == b


def test_state():
    a = Polynomial("(1+x+y)^3")
    s = dumps(a)
    b = loads(s)
    assert a == b
    assert a + b == a * 2


def test_repr():
    a = Polynomial("1+x")
    b = eval(repr(a))
    assert a == b


def test_hash():
    a = Polynomial(42)
    b = 42

    assert a == b
    assert hash(a) == hash(b)

    a = Variable("a")
    b = Polynomial(a)

    assert a == b
    assert hash(a) == hash(b)

    a = Polynomial("(a+b)*(c+d)-a*c-b*c-b*d")
    b = Polynomial("a*d")

    assert a == b
    assert hash(a) == hash(b)


def test_hash_as_key():
    d = {}

    a = Polynomial("1+x")
    b = Polynomial("2+x")

    d[a] = "a"
    d[b] = "b"

    a = Polynomial("2+x+y-1-y")
    b = Polynomial("3+x+y-1-y")

    assert d[a] == "a"
    assert d[b] == "b"


def test_len():
    a = Polynomial("0")
    assert len(a) == 0
    assert not a

    a = Polynomial("1+x")
    assert len(a) == 2
    assert a


def test_iter():
    a = Polynomial("(1+x)^3")
    n = 0
    for t in a:
        assert not t.is_zero
        assert t.is_monomial
        n += 1
    assert n == 4


def test_pos():
    a = Polynomial("0")
    assert (+a) == a

    a = Polynomial("1+x")
    assert (+a) == a


def test_neg():
    a = Polynomial("0")
    assert (-a) == a

    a = Polynomial("1+x")
    b = 0 - a
    assert (-a) == b
    assert (-b) == a


def test_add():
    a = Polynomial("2+x")
    b = Polynomial("3+y")
    c = Polynomial("5+x+y")
    assert a + b == c

    a = Polynomial("2+x")
    b = 3
    c = Polynomial("5+x")
    assert a + b == c

    a = 2
    b = Polynomial("3+y")
    c = Polynomial("5+y")
    assert a + b == c


def test_sub():
    a = Polynomial("2+x")
    b = Polynomial("3+y")
    c = Polynomial("-1+x-y")
    assert a - b == c

    a = Polynomial("2+x")
    b = 3
    c = Polynomial("-1+x")
    assert a - b == c

    a = 2
    b = Polynomial("3+y")
    c = Polynomial("-1-y")
    assert a - b == c


def test_mul():
    a = Polynomial("2+x")
    b = Polynomial("3+y")
    c = Polynomial("6+3*x+2*y+x*y")
    assert a * b == c

    a = Polynomial("2+x")
    b = 3
    c = Polynomial("6+3*x")
    assert a * b == c

    a = 2
    b = Polynomial("3+y")
    c = Polynomial("6+2*y")
    assert a * b == c


def test_div():
    a = Polynomial("1+x")
    b = Polynomial("1-y")
    c = RationalFunction("(1+x)/(1-y)")
    assert a / b == c

    a = Polynomial("1+x")
    b = Fraction(3, 2)
    c = RationalFunction("(2+2*x)/3")
    assert a / b == c

    a = Fraction(-4, 5)
    b = Polynomial("1-y")
    c = RationalFunction("-4/(5-5*y)")
    assert a / b == c

    a = 3
    b = Polynomial("1-y")
    c = RationalFunction("3/(1-y)")
    assert a / b == c


def test_pow():
    a = Polynomial("1+x")
    b = 3
    c = Polynomial("(1+x)^3")
    assert a ** b == c

    a = Polynomial("1+x")
    b = 1
    c = a
    assert a ** b == c

    a = Polynomial("1+x")
    b = 0
    c = 1
    assert a ** b == c

    a = Polynomial("0")
    b = 0
    c = 1
    assert a ** b == c  # NOTE: 0^0 = 1 in Python

    a = Polynomial("1+x")
    with raises(ValueError):
        a ** (-3)  # negative power


def test_cmp():
    a = Polynomial("1+x+y-y")
    b = Polynomial("2-1+x")
    assert a == b

    a = Polynomial("1+x+y-x-y")
    b = 1
    assert a == b

    a = 1
    b = Polynomial("2-1")
    assert a == b

    a = Polynomial("1+x")
    b = Polynomial("1+y")
    assert a != b

    a = Polynomial("1+x")
    b = 1
    assert a != b

    a = Polynomial("1+x")
    b = 1
    assert a != b

    a = Polynomial("x")
    b = []
    assert a != b

    a = []
    b = Polynomial("x")
    assert a != b


def test_is():
    a = Polynomial("0")
    assert a.is_zero
    assert not a.is_one
    assert not a.is_minus_one
    assert a.is_integer
    assert a.is_monomial
    assert not a.is_monic
    assert not a.is_variable

    a = Polynomial("1")
    assert not a.is_zero
    assert a.is_one
    assert not a.is_minus_one
    assert a.is_integer
    assert a.is_monomial
    assert a.is_monic
    assert not a.is_variable

    a = Polynomial("-1")
    assert not a.is_zero
    assert not a.is_one
    assert a.is_minus_one
    assert a.is_integer
    assert a.is_monomial
    assert not a.is_monic
    assert not a.is_variable

    a = Polynomial("42")
    assert not a.is_zero
    assert not a.is_one
    assert not a.is_minus_one
    assert a.is_integer
    assert a.is_monomial
    assert not a.is_monic
    assert not a.is_variable

    a = Polynomial("x")
    assert not a.is_zero
    assert not a.is_one
    assert not a.is_minus_one
    assert not a.is_integer
    assert a.is_monomial
    assert a.is_monic
    assert a.is_variable

    a = Polynomial("2*x")
    assert not a.is_zero
    assert not a.is_one
    assert not a.is_minus_one
    assert not a.is_integer
    assert a.is_monomial
    assert not a.is_monic
    assert not a.is_variable

    a = Polynomial("1+x")
    assert not a.is_zero
    assert not a.is_one
    assert not a.is_minus_one
    assert not a.is_integer
    assert not a.is_monomial
    assert a.is_monic
    assert not a.is_variable


def test_as():
    a = Polynomial("42")
    assert a.as_integer == 42

    a = Polynomial("x")
    with raises(ValueError):
        a.as_integer  # not integer

    a = Polynomial("x")
    assert a.as_variable == Variable("x")

    a = Polynomial("1+x")
    with raises(ValueError):
        a.as_variable  # not variable


def test_as_with_bigints(bigints):  # noqa: F811
    for n in bigints:
        a = Polynomial(n)
        assert a.as_integer == n


def test_signum():
    a = Polynomial("1-x")
    b = -a

    assert a.signum == -b.signum
    assert a * a.signum == b * b.signum


def test_variables():
    a = Polynomial("1+x+y+z-y")
    assert a.variables == VariableSet("x", "y", "z")
    assert a.min_variables == VariableSet("x", "z")


def test_degree():
    a = Polynomial("1+x*y+x*y*z^2")
    assert a.degree() == 4  # total degree
    assert a.degree(Variable("x")) == 1
    assert a.degree("z") == 2
    assert a.degree(VariableSet("x", "y")) == 2
    assert a.degree("x", "z") == 3
    assert a.degree(["x", "z", "z"]) == 3
    assert a.degree([]) == 0  # none of variables

    with raises(TypeError):
        a.degree(1, 2, 3)  # not variable


def test_coeff():
    a = Polynomial("(1+x+y)^3")

    assert a.coeff(Variable("x"), 0) == Polynomial("(1+y)^3")
    assert a.coeff("x", 1) == Polynomial("3*(1+y)^2")
    assert a.coeff("x", 4) == 0
    assert a.coeff("z", 0) == a
    assert a.coeff("z", 1) == 0

    assert a.coeff(["x", "y"], [0, 0]) == 1
    assert a.coeff(["x", "y"], [1, 1]) == 6
    assert a.coeff(["x", "y"], [1, 2]) == 3
    assert a.coeff(["x", "y"], [2, 2]) == 0

    with raises(TypeError):
        a.coeff(1, 1)  # x must be a variable

    with raises(TypeError):
        a.coeff("x", "1")  # n must be an integer

    with raises(TypeError):
        a.coeff(["x", "y"], 1)  # exponents must be a collection

    with raises(ValueError):
        a.coeff(["x", "y"], [1, 2, 3])  # different sizes


def test_translate():
    a = Polynomial("(1+x+y)-(1+x+z)")

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


def test_gcd():
    zero = Polynomial("0")

    a = Polynomial("1+x-y")
    b = Polynomial("1+y+z")
    g = Polynomial("1-z-z^2")

    ag = a * g
    bg = b * g

    gcd = ag.gcd(bg)

    assert gcd * gcd.signum == g * g.signum

    assert zero.gcd(zero) == 0
    assert ag.gcd(zero) == ag
    assert zero.gcd(bg) == bg

    a = Polynomial("24*(1+x)")
    assert a.gcd(18) == 6

    with raises(TypeError):
        a.gcd("1")  # not polynomial


def test_lcm():
    zero = Polynomial("0")
    one = Polynomial("1")

    a = Polynomial("24*(1+x)^3*(1+z)")
    b = Polynomial("18*(1+y)^2*(1+z)")
    c = Polynomial("72*(1+x)^3*(1+y)^2*(1+z)")

    assert zero.lcm(zero) == 0
    assert one.lcm(one) == 1

    assert a.lcm(zero) == 0
    assert zero.lcm(a) == 0

    assert a.lcm(one) == a
    assert one.lcm(a) == a

    assert a.lcm(b) == c

    a = Polynomial("24*(1+x)")
    assert a.lcm(18) == Polynomial("72*(1+x)")

    with raises(TypeError):
        a.lcm("1")  # not polynomial


def test_factors():
    a = Polynomial("-2*x^4*y^3 + 2*x^3*y^4 + 2*x^2*y^5 - 2*x*y^6").factors()
    b = [
        Polynomial("-2"),
        Polynomial("y"),
        Polynomial("y"),
        Polynomial("y"),
        Polynomial("x"),
        Polynomial("x-y"),
        Polynomial("x-y"),
        Polynomial("x+y"),
    ]
    assert a == b


def test_subs():
    a = Polynomial("(1+x)^3")
    lhs = Polynomial("x")
    rhs = Polynomial("y")
    b = Polynomial("(1+y)^3")
    assert a.subs(lhs, rhs) == b

    a = Polynomial("(1+x)^3")
    lhs = "x"
    rhs = "y"
    b = Polynomial("(1+y)^3")
    assert a.subs(lhs, rhs) == b

    a = Polynomial("(1+x+y)^7").subs("x*y^2", 1).subs("x", 7).subs("y", 11)
    b = 58609171
    assert a == b

    with raises(TypeError):
        a.subs(1, "x")  # lhs is not a polynomial

    with raises(TypeError):
        a.subs("x", [])  # rhs is not a polynomial

    with raises(ValueError):
        a.subs("2*x", 1)  # invalid lhs

    with raises(ValueError):
        a.subs("1+x", 1)  # invalid lhs


def test_evaluate():
    a = Polynomial("(1+x+y)^3").evaluate("x", 3)
    b = Polynomial("(4+y)^3")
    assert a == b

    a = Polynomial("(1+x+y)^3").evaluate([Variable("x"), "y"], [3, -2])
    b = Polynomial("8")
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
    a = Polynomial("(1+x)^3").evaluate_at_zero(Variable("x"))
    b = 1
    assert a == b

    a = Polynomial("(1+x)^3").evaluate_at_zero(["x", "y", "z"])
    b = 1
    assert a == b

    a = Polynomial("(1+x)^3").evaluate_at_zero([])
    b = Polynomial("(1+x)^3")
    assert a == b

    a = Polynomial("(1+x)^3").evaluate_at_zero()
    b = Polynomial("(1+x)^3")
    assert a == b

    with raises(TypeError):
        a.evaluate_at_zero(1)  # not variable


def test_evaluate_at_one():
    a = Polynomial("(1+x)^3").evaluate_at_one(Variable("x"))
    b = 8
    assert a == b

    a = Polynomial("(1+x)^3").evaluate_at_one(["x", "y", "z"])
    b = 8
    assert a == b

    a = Polynomial("(1+x)^3").evaluate_at_one([])
    b = Polynomial("(1+x)^3")
    assert a == b

    a = Polynomial("(1+x)^3").evaluate_at_one()
    b = Polynomial("(1+x)^3")
    assert a == b

    with raises(TypeError):
        a.evaluate_at_one(1)  # not variable


def test_shift():
    a = Polynomial("(1+x+2*y)^3").shift("x", 3)
    b = Polynomial("(4+x+2*y)^3")
    assert a == b

    a = Polynomial("(1+x+2*y)^3").shift([Variable("x"), "y"], [3, -2])
    b = Polynomial("(x+2*y)^3")
    assert a == b

    with raises(TypeError):
        a.shift(["x"], 1)  # values must be also a collection

    with raises(ValueError):
        a.shift(["x"], [1, 2])  # different sizes

    with raises(TypeError):
        a.shift("x", "y")  # value must be an integer

    with raises(TypeError):
        a.shift(1, 1)  # invalid variables

    with raises(TypeError):
        a.shift(["x"], ["y"])  # values are not integers

    with raises(TypeError):
        a.shift([1], [1])  # not variables


def test_diff():
    a = Polynomial("(1+x+y)^3")
    x = Variable("x")
    assert a.diff(x) == Polynomial("3*(1+x+y)^2")

    a = Polynomial("(1+x+y)^3")
    assert a.diff("y") == Polynomial("3*(1+x+y)^2")

    a = Polynomial("(1+x)^9")
    assert a.diff("x", 0) == a
    assert a.diff("x", 1) == Polynomial("9*(1+x)^8")
    assert a.diff("x", 2) == Polynomial("72*(1+x)^7")

    with raises(TypeError):
        a.diff(1)  # x must be a Variable

    with raises(TypeError):
        a.diff(x, "x")  # n must be an int

    with raises(ValueError):
        a.diff(x, -1)  # n must be non-negative


def test_gcd_of():
    p1 = Polynomial("1+x")
    p2 = Polynomial("1+y")
    p3 = Polynomial("1+z")
    q = p1 * p2 * p3
    a = [p1 ** 2 * p2 ** 3 * p3 ** 2, p1 ** 3 * p2 ** 2 * p3, p1 * p2 * p3 ** 3]

    assert donuts.poly.gcd(a) == q
    assert donuts.poly.gcd(*a) == q
    assert donuts.poly.gcd(x for x in a) == q
    assert donuts.poly.gcd(a + [1]) == 1

    assert donuts.poly.gcd() == 0

    assert donuts.poly.gcd(0) == 0
    assert donuts.poly.gcd(1) == 1
    assert donuts.poly.gcd(p1) == p1

    assert donuts.poly.gcd(0, 0) == 0
    assert donuts.poly.gcd(0, 1) == 1
    assert donuts.poly.gcd(0, p1) == p1
    assert donuts.poly.gcd(1, 0) == 1
    assert donuts.poly.gcd(1, 1) == 1
    assert donuts.poly.gcd(1, p1) == 1
    assert donuts.poly.gcd(p1, 0) == p1
    assert donuts.poly.gcd(p1, 1) == 1
    assert donuts.poly.gcd(p1, p1) == p1

    with raises(TypeError):
        donuts.poly.gcd("x")  # not Polynomial


def test_lcm_of():
    p1 = Polynomial("1+x")
    p2 = Polynomial("1+y")
    p3 = Polynomial("1+z")
    q = p1 ** 3 * p2 ** 3 * p3 ** 3
    a = [p1 ** 2 * p2 ** 3 * p3 ** 2, p1 ** 3 * p2 ** 2 * p3, p1 * p2 * p3 ** 3]

    assert donuts.poly.lcm(a) == q
    assert donuts.poly.lcm(*a) == q
    assert donuts.poly.lcm(x for x in a) == q
    assert donuts.poly.lcm(a + [2]) == 2 * q

    assert donuts.poly.lcm(0) == 0
    assert donuts.poly.lcm(1) == 1
    assert donuts.poly.lcm(p1) == p1

    assert donuts.poly.lcm(0, 0) == 0
    assert donuts.poly.lcm(0, 1) == 0
    assert donuts.poly.lcm(0, p1) == 0
    assert donuts.poly.lcm(1, 0) == 0
    assert donuts.poly.lcm(1, 1) == 1
    assert donuts.poly.lcm(1, p1) == p1
    assert donuts.poly.lcm(p1, 0) == 0
    assert donuts.poly.lcm(p1, 1) == p1
    assert donuts.poly.lcm(p1, p1) == p1

    with raises(ValueError):
        assert donuts.poly.lcm()  # no arguments

    with raises(TypeError):
        donuts.poly.lcm("x")  # not Polynomial
