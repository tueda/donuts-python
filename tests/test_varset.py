from donuts import Variable, VariableSet


def test_init():
    x = Variable("x")
    y = Variable("y")
    z = Variable("z")

    a = VariableSet(x, y, z)
    b = VariableSet(z, y, x, y)

    assert str(a) == "{x, y, z}"
    assert eval(repr(a)) == a
    assert len(a) == 3
    assert hash(a) == hash(b)
    assert a == b


def test_iter():
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


def test_contains():
    x = Variable("x")
    y = Variable("y")
    z = Variable("z")

    a = VariableSet(x, y)

    assert x in a
    assert y in a
    assert z not in a
    assert "x" not in a
