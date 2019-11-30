import pickle

from test_poly_bench import random_poly

from donuts import RationalFunction


def random_rat(nvars=10, ndegree=20, nterms=50, ncoeffbits=32, seed=42):
    while True:
        r1 = random_poly(nvars, ndegree, nterms, ncoeffbits, seed)
        r2 = random_poly(nvars, ndegree, nterms, ncoeffbits, seed + 1000)
        gcd = r1.gcd(r2)
        if gcd.is_one or gcd.is_minus_one:
            return r1 / r2


def test_rat_to_string(benchmark):
    r = random_rat(nterms=1000)
    result = benchmark(str, r)
    assert result


def test_rat_from_string(benchmark):
    r = random_rat(nterms=1000)
    s = str(r)
    result = benchmark(RationalFunction, s)
    assert result


def test_rat_dumps(benchmark):
    r = random_rat(nterms=1000)
    result = benchmark(pickle.dumps, r)
    assert result


def test_rat_loads(benchmark):
    r = random_rat(nterms=1000)
    s = pickle.dumps(r)
    result = benchmark(pickle.loads, s)
    assert result


def test_rat_add(benchmark):
    r1 = random_rat(nterms=100, seed=1)
    r2 = random_rat(nterms=100, seed=2)
    result = benchmark(lambda a, b: a + b, r1, r2)
    assert result


def test_rat_mul(benchmark):
    r1 = random_rat(nterms=100, seed=1)
    r2 = random_rat(nterms=100, seed=2)
    result = benchmark(lambda a, b: a * b, r1, r2)
    assert result
