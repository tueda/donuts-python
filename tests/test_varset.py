from pickle import dumps, loads

import pytest

from donuts import Variable
from donuts.varset import VariableSet


def test_init() -> None:
    a = VariableSet()

    assert str(a) == "{}"
    assert eval(repr(a)) == a
    assert len(a) == 0

    x = Variable("x")
    y = Variable("y")
    z = Variable("z")

    assert VariableSet("x") == VariableSet(x, x)
    assert VariableSet("x", "y") == VariableSet(x, y)
    assert VariableSet("xyz") == VariableSet(Variable("xyz"))

    a = VariableSet(x, y, z)
    b = VariableSet(z, y, x, y)
    c = VariableSet("x", "y", y, z)
    d = VariableSet(["x", "y", y, z])
    e = VariableSet(a)

    assert str(a) == "{x, y, z}"
    assert eval(repr(a)) == a
    assert len(a) == 3
    assert hash(a) == hash(b)
    assert hash(a) == hash(c)
    assert hash(a) == hash(d)
    assert hash(a) == hash(e)
    assert a == b
    assert a == c
    assert a == d
    assert a == e

    with pytest.raises(TypeError):
        VariableSet(
            "x", "y", ["z"]
        )  # type: ignore[call-overload]  # neither Variable nor str


def test_state() -> None:
    a = VariableSet("a", "b", "c")
    s = dumps(a)
    b = loads(s)
    assert a == b


def test_iter() -> None:
    x = Variable("x")
    y = Variable("y")
    z = Variable("z")

    a = VariableSet(x, y, z)
    b = []
    for x in a:
        assert isinstance(x, Variable)
        assert x not in b
        b.append(x)
    c = VariableSet(*b)
    assert a == c


def test_contains() -> None:
    x = Variable("x")
    y = Variable("y")
    z = Variable("z")

    a = VariableSet(x, y)

    assert x in a
    assert y in a
    assert z not in a
    assert "x" not in a


def test_union() -> None:
    sa = ["x", "y"]
    sb = ["x", "z"]
    sc = sa + sb
    a = VariableSet(*sa)
    b = VariableSet(*sb)
    c = VariableSet(*sc)
    assert a.union(b) == c

    sa = ["x", "y", "z"]
    sb = ["a", "b", "c"]
    sc = sa + sb
    a = VariableSet(*sa)
    b = VariableSet(*sb)
    c = VariableSet(*sc)
    assert a.union(b) == c

    sa = ["x", "y"]
    sb = ["a", "b", "c", "x", "y", "z"]
    sc = sa + sb
    a = VariableSet(*sa)
    b = VariableSet(*sb)
    c = VariableSet(*sc)
    assert a.union(b) == c

    with pytest.raises(TypeError):
        a.union([])  # type: ignore[arg-type]  # not set of variables
