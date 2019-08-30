import pytest

from donuts import Polynomial


@pytest.fixture
def bigints():
    """Give a list of integers containing big values."""
    test_int_set = set()
    for i in (-2 ** 127, -2 ** 63, -2 ** 31, 0, 2 ** 31, 2 ** 63, 2 ** 127):
        for j in range(-5, 6):
            n = i + j
            test_int_set.add(n)
    return sorted(test_int_set)


def test_init():
    a = Polynomial()
    assert a == 0
    assert str(a) == "0"

    a = Polynomial("a")
    assert str(a) == "a"


def test_init_with_bigints(bigints):
    for n in bigints:
        a = Polynomial(n)
        b = Polynomial(str(n))
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
    with pytest.raises(ValueError):
        a.as_integer


def test_as_with_bigints(bigints):
    for n in bigints:
        a = Polynomial(n)
        assert a.as_integer == n
