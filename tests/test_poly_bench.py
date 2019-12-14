import pickle
import random

from donuts import Polynomial


def random_poly(nvars=10, ndegree=20, nterms=50, ncoeffbits=32, seed=42):
    random.seed(seed)

    variables = ["x" + str(i) for i in range(1, nvars + 1)]

    def random_coeff():
        m = 2 ** ncoeffbits - 1
        if m < 1:
            m = 1
        while True:
            n = random.randint(-m, m)
            if m != 0:
                return n
        return 1

    def random_exponents():
        a = [0] * nvars
        n = ndegree
        while True:
            m = random.randint(0, n)
            i = random.randint(0, nvars - 1)
            a[i] += m
            n -= m
            if n == 0:
                break
        random.shuffle(a)
        return tuple(a)

    def monomial_to_str(v, c):
        e = "".join((f"*{variables[i]}^{n}" if n > 0 else "") for i, n in enumerate(v))
        return f"+({c}{e})"

    monomials = {}

    for _ in range(10):
        for i in range(nterms - len(monomials)):
            e = random_exponents()
            if not e in monomials:
                monomials[e] = random_coeff()
        if len(monomials) == nterms:
            break

    return Polynomial("".join(monomial_to_str(v, c) for v, c in monomials.items()))


def test_poly_to_string(benchmark):
    p = random_poly(nterms=1000)
    result = benchmark(str, p)
    assert result


def test_poly_from_string(benchmark):
    p = random_poly(nterms=1000)
    s = str(p)
    result = benchmark(Polynomial, s)
    assert result


def test_poly_dumps(benchmark):
    p = random_poly(nterms=1000)
    result = benchmark(pickle.dumps, p)
    assert result


def test_poly_loads(benchmark):
    p = random_poly(nterms=1000)
    s = pickle.dumps(p)
    result = benchmark(pickle.loads, s)
    assert result


def test_poly_add(benchmark):
    p1 = random_poly(nterms=100, seed=1)
    p2 = random_poly(nterms=100, seed=2)
    result = benchmark(lambda a, b: a + b, p1, p2)
    assert result


def test_poly_mul(benchmark):
    p1 = random_poly(nterms=100, seed=1)
    p2 = random_poly(nterms=100, seed=2)
    result = benchmark(lambda a, b: a * b, p1, p2)
    assert result


def test_poly_gcd(benchmark):
    g = random_poly(nterms=10)
    p1 = g * random_poly(nterms=10, seed=1)
    p2 = g * random_poly(nterms=10, seed=2)
    result = benchmark(lambda a, b: a.gcd(b), p1, p2)
    assert result


def test_poly_gcd_trivial(benchmark):
    p1 = random_poly(nterms=100, seed=1)
    p2 = random_poly(nterms=100, seed=2)
    result = benchmark(lambda a, b: a.gcd(b), p1, p2)
    assert result


def test_poly_factor(benchmark):
    p1 = random_poly(nterms=4, seed=1)
    p2 = random_poly(nterms=5, seed=2)
    p3 = random_poly(nterms=5, seed=3)
    p = p1 * p2 * p3
    result = benchmark(lambda a: a.factors(), p)
    assert result


def test_poly_factor_trivial(benchmark):
    p = random_poly(nterms=100)
    result = benchmark(lambda a: a.factors(), p)
    assert result
