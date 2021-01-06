import pickle

from conftest import Benchmark

from donuts.varset import VariableSet


def example_varset(n: int = 10) -> VariableSet:
    a = [f"x{i}" for i in range(1, n + 1)]
    return VariableSet(*a)


def test_varset_dumps(benchmark: Benchmark) -> None:
    v = example_varset()
    result = benchmark(pickle.dumps, v)
    assert result


def test_varset_loads(benchmark: Benchmark) -> None:
    v = example_varset()
    s = pickle.dumps(v)
    result = benchmark(pickle.loads, s)
    assert result
