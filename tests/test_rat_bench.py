import pickle

from conftest import random_rat

from donuts import RationalFunction


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
