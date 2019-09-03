from pytest import raises

from donuts import Variable


def test_init():
    x = Variable("x")
    assert str(x) == "x"

    with raises(TypeError):
        Variable(42)  # not string

    with raises(ValueError):
        Variable("$x")  # invalid name


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
