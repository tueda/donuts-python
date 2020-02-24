import pickle

from conftest import random_poly
from donuts import Polynomial, Variable


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


def test_poly_varsubs(benchmark):
    p = random_poly(nterms=10) + Polynomial("x1")
    x = Variable("x1")
    result = benchmark(lambda a, b: a.subs(b, 1), p, x)
    assert result
