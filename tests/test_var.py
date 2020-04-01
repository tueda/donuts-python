from pickle import dumps, loads

from pytest import raises

from donuts import Polynomial, RationalFunction, Variable


def test_init():
    x = Variable("x")
    assert str(x) == "x"

    y = Variable(x)
    assert str(y) == "x"

    assert x == y

    with raises(TypeError):
        Variable(42)  # not string

    with raises(ValueError):
        Variable("$x")  # invalid name


def test_state():
    a = Variable("a")
    s = dumps(a)
    b = loads(s)
    assert a == b


def test_repr():
    a = Variable("a")
    b = eval(repr(a))
    assert a == b


def test_hash():
    a1 = Variable("a")
    a2 = Variable("a")

    assert a1 == a2
    assert hash(a1) == hash(a2)


def test_cmp():
    variables = [Variable("a"), Variable("b"), Variable("c")]

    for i, x in enumerate(variables):
        for j, y in enumerate(variables):
            if i == j:
                assert x == y
            if i != j:
                assert x != y
            if i < j:
                assert x < y
            if i <= j:
                assert x <= y
            if i > j:
                assert x > y
            if i >= j:
                assert x >= y


def test_pos():
    a = Variable("a")
    assert (+a) == Polynomial("a")


def test_neg():
    a = Variable("a")
    assert (-a) == Polynomial("-a")


def test_add():
    a = Variable("a")
    b = Variable("b")
    assert a + a == Polynomial("2*a")
    assert a + b == Polynomial("a+b")
    assert a + 1 == Polynomial("a+1")
    assert 1 + a == Polynomial("1+a")


def test_sub():
    a = Variable("a")
    b = Variable("b")
    assert a - a == Polynomial("0")
    assert a - b == Polynomial("a-b")
    assert a - 1 == Polynomial("a-1")
    assert 1 - a == Polynomial("1-a")


def test_mul():
    a = Variable("a")
    b = Variable("b")
    assert a * a == Polynomial("a^2")
    assert a * b == Polynomial("a*b")
    assert a * 2 == Polynomial("2*a")
    assert 2 * a == Polynomial("2*a")


def test_div():
    a = Variable("a")
    b = Variable("b")
    assert a / b == RationalFunction("a/b")
    assert a / 2 == RationalFunction("a/2")
    assert 1 / a == RationalFunction("1/a")


def test_pow():
    a = Variable("a")
    assert a ** 0 == Polynomial("1")
    assert a ** 1 == Polynomial("a")
    assert a ** 2 == Polynomial("a^2")
