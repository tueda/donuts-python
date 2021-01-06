"""Raw Java arrays."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, Sequence, Union

from .jvm import jvm

if TYPE_CHECKING:
    from .poly import PolynomialLike
    from .var import VariableLike


_RawVariable = jvm.find_class("com.github.tueda.donuts.Variable")
_RawPolynomial = jvm.find_class("com.github.tueda.donuts.Polynomial")
_new_array = jvm.new_array
_new_int_array = jvm.new_int_array


def _create_raw_int_array(values: Sequence[int]) -> Any:
    """Create a Java array of integers."""
    array = _new_int_array(len(values))
    for i in range(len(values)):
        x = values[i]
        if not isinstance(x, int):
            raise TypeError("not integer")
        array[i] = x
    return array


def _create_raw_var_array(
    variables: Sequence[Union[VariableLike, Iterable[VariableLike]]]
) -> Any:
    """Create a Java array of variables."""
    from .var import Variable

    if len(variables) == 1:
        x = variables[0]
        if not isinstance(x, str):
            if isinstance(x, Sequence):
                return _create_raw_var_array(x)
            if isinstance(x, Iterable):
                return _create_raw_var_array(tuple(x))

    array = _new_array(_RawVariable, len(variables))
    for i in range(len(variables)):
        x = variables[i]
        if isinstance(x, Variable):
            array[i] = x._raw
        elif isinstance(x, str):
            array[i] = Variable(x)._raw
        else:
            raise TypeError("not Variable")
    return array


def _create_raw_poly_array(
    polynomials: Sequence[Union[PolynomialLike, Iterable[PolynomialLike]]]
) -> Any:
    """Create a Java array of polynomials."""
    from .poly import Polynomial
    from .var import Variable

    if len(polynomials) == 1:
        x = polynomials[0]
        if not isinstance(x, (Polynomial, str)):
            if isinstance(x, Sequence):
                return _create_raw_poly_array(x)
            if isinstance(x, Iterable):
                return _create_raw_poly_array(tuple(x))

    array = _new_array(_RawPolynomial, len(polynomials))
    for i in range(len(polynomials)):
        x = polynomials[i]
        if isinstance(x, Polynomial):
            array[i] = x._raw
        elif isinstance(x, (Variable, int)):
            array[i] = Polynomial(x)._raw
        else:
            raise TypeError("not Polynomial")
    return array
