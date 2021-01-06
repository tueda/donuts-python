"""Configuration for testing."""

import random
from typing import Any, Callable, Dict, Sequence

from pytest import fixture

from donuts import Polynomial, RationalFunction


def random_poly(
    nvars: int = 10,
    ndegree: int = 20,
    nterms: int = 50,
    ncoeffbits: int = 32,
    seed: int = 42,
) -> Polynomial:
    """Return a random polynomial."""
    random.seed(seed)

    variables = ["x" + str(i) for i in range(1, nvars + 1)]

    def random_coeff() -> int:
        m = 2 ** ncoeffbits - 1
        if m < 1:
            m = 1
        while True:
            n = random.randint(-m, m)
            if n != 0:
                return n

    def random_exponents() -> Sequence[int]:
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

    def monomial_to_str(v: Sequence[int], c: int) -> str:
        e = "".join((f"*{variables[i]}^{n}" if n > 0 else "") for i, n in enumerate(v))
        return f"+({c}{e})"

    monomials: Dict[Sequence[int], int] = {}

    for _ in range(10):
        for _ in range(nterms - len(monomials)):
            e = random_exponents()
            if e not in monomials:
                monomials[e] = random_coeff()
        if len(monomials) == nterms:
            break

    return Polynomial("".join(monomial_to_str(v, c) for v, c in monomials.items()))


def random_rat(
    nvars: int = 10,
    ndegree: int = 20,
    nterms: int = 50,
    ncoeffbits: int = 32,
    seed: int = 42,
) -> RationalFunction:
    """Return a random rational function."""
    while True:
        r1 = random_poly(nvars, ndegree, nterms, ncoeffbits, seed)
        r2 = random_poly(nvars, ndegree, nterms, ncoeffbits, seed + 1000)
        gcd = r1.gcd(r2)
        if gcd.is_one or gcd.is_minus_one:
            return r1 / r2


@fixture
def bigints():  # type: ignore
    """Give a list of integers containing big values."""
    test_int_set = set()
    for i in (-(2 ** 63), 0, 2 ** 63):
        for j in range(-2, 3):
            n = i + j
            test_int_set.add(n)
    return sorted(test_int_set)


BigIntSeq = Sequence[int]
Benchmark = Callable[..., Any]
