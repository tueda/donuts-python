from donuts import Polynomial


def test_init():
    a = Polynomial()
    assert a == 0
    assert str(a) == "0"

    a = Polynomial("a")
    assert str(a) == "a"

    # for integers (which may be big)
    for i in (-2 ** 127, -2 ** 63, -2 ** 31, 0, 2 ** 31, 2 ** 63, 2 ** 127):
        for j in range(-5, 6):
            n = i + j
            a = Polynomial(n)
            b = Polynomial(str(n))
            assert a == b


def test_hash():
    d = {}

    a = Polynomial("1+x")
    b = Polynomial("2+x")

    d[a] = "a"
    d[b] = "b"

    a = Polynomial("2+x+y-1-y")
    b = Polynomial("3+x+y-1-y")

    assert d[a] == "a"
    assert d[b] == "b"


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


def test_pow():
    a = Polynomial("1+x")
    b = 3
    c = Polynomial("(1+x)^3")
    assert a ** b == c


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
