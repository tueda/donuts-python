from pytest import fixture


@fixture
def bigints():
    """Give a list of integers containing big values."""
    test_int_set = set()
    for i in (-2 ** 63, 0, 2 ** 63):
        for j in range(-2, 3):
            n = i + j
            test_int_set.add(n)
    return sorted(test_int_set)
