from fractions import Fraction

from pytest import fixture, raises

from donuts import Polynomial, RationalFunction
from fixtures.bigints import bigints


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

    a = Polynomial("1+x")
    b = RationalFunction(a)
    assert a == b

    a = RationalFunction("(1+x)/(1-y)")
    b = RationalFunction(a)
    assert a == b

    with raises(TypeError):
        RationalFunction([1])

    with raises(TypeError):
        RationalFunction("1", 2)

    with raises(TypeError):
        RationalFunction([1], [2])


def test_init_with_bigints(bigints):
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


def test_hash():
    a = 42
    b = RationalFunction(a)
    assert a == b
    assert hash(a) == hash(b)

    a = Fraction(3, 2)
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
        b.as_integer


def test_as_integer_with_bigints(bigints):
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
        b.as_fraction


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
        b.as_polynomial
