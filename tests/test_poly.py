from fractions import Fraction

from pytest import raises

from donuts import Polynomial, RationalFunction
from fixtures.bigints import bigints


def test_init():
    a = Polynomial()
    assert a == 0
    assert str(a) == "0"

    a = Polynomial(42)
    assert a == 42
    assert str(a) == "42"

    a = Polynomial("a")
    assert str(a) == "a"

    a = Polynomial(a)
    assert str(a) == "a"

    with raises(TypeError):
        Polynomial([1])  # invalid type

    with raises(ValueError):
        Polynomial("(1+x)/(1-y)")  # not polynomial

    with raises(ValueError):
        Polynomial("x?")  # invalid string


def test_init_with_bigints(bigints):
    for n in bigints:
        a = Polynomial(n)
        b = Polynomial(str(n))
        assert a == b


def test_repr():
    a = Polynomial("1+x")
    b = eval(repr(a))
    assert a == b


def test_hash():
    a = Polynomial(42)
    b = 42

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


def test_as_with_bigints(bigints):
    for n in bigints:
        a = Polynomial(n)
        assert a.as_integer == n


def test_signum():
    a = Polynomial("1-x")
    b = -a

    assert a.signum == -b.signum
    assert a * a.signum == b * b.signum


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


def test_factorize():
    a = Polynomial("-2*x^4*y^3 + 2*x^3*y^4 + 2*x^2*y^5 - 2*x*y^6").factorize()
    b = [
        Polynomial("-2*x*y^2"),
        Polynomial("x-y"),
        Polynomial("x-y"),
        Polynomial("x+y"),
    ]
    assert a == b
