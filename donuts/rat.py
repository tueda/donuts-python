"""Routines for rational functions."""

from __future__ import annotations

import functools
from fractions import Fraction
from typing import Any, FrozenSet, Iterable, Sequence, Union, overload

from .array import _create_raw_int_array, _create_raw_var_array
from .jvm import jvm
from .poly import Polynomial
from .var import Variable, VariableLike
from .varset import VariableSet, VariableSetLike

_RawRationalFunction = jvm.find_class("com.github.tueda.donuts.RationalFunction")
_JavaError = jvm.java_error_class


_RAW_ZERO = _RawRationalFunction()
_RAW_ONE = _RawRationalFunction(1)
_RAW_MINUS_ONE = _RawRationalFunction(-1)


def _raw_rationalfunction_from_short_int(value: int) -> Any:
    if value == 0:
        return _RAW_ZERO
    if value == 1:
        return _RAW_ONE
    if value == -1:
        return _RAW_MINUS_ONE
    return _raw_rationalfunction_from_short_int_impl(value)


@functools.lru_cache(maxsize=1024)
def _raw_rationalfunction_from_short_int_impl(value: int) -> Any:
    return _RawRationalFunction(value)


@functools.lru_cache(maxsize=1024)
def _raw_rationalfunction_from_str(value: str) -> Any:
    return _RawRationalFunction(value)


class RationalFunction:
    """Rational function."""

    __slots__ = ("_raw",)

    def __init__(
        self,
        numerator: Union[
            RationalFunction, Polynomial, Variable, Fraction, int, str, None
        ] = None,
        denominator: Union[Polynomial, Variable, int, None] = None,
    ) -> None:
        """Construct a rational function."""
        if denominator is None:
            if numerator is None:
                self._raw = _RAW_ZERO
            elif isinstance(numerator, int):
                if Polynomial._is_short_int(numerator):
                    self._raw = _raw_rationalfunction_from_short_int(numerator)
                else:
                    self._raw = _RawRationalFunction(str(numerator))
            elif isinstance(numerator, str):
                try:
                    self._raw = _RawRationalFunction(numerator)
                except _JavaError as e:
                    raise ValueError("invalid string for rational function") from e
            elif isinstance(numerator, Fraction):
                if Polynomial._is_short_int(
                    numerator.numerator
                ) and Polynomial._is_short_int(numerator.denominator):
                    self._raw = _RawRationalFunction(
                        numerator.numerator, numerator.denominator
                    )
                else:
                    self._raw = _RawRationalFunction(
                        Polynomial(numerator.numerator)._raw,
                        Polynomial(numerator.denominator)._raw,
                    )
            elif isinstance(numerator, Variable):
                self._raw = _raw_rationalfunction_from_str(numerator._name)
            elif isinstance(numerator, Polynomial):
                self._raw = _RawRationalFunction(numerator._raw)
            elif isinstance(numerator, RationalFunction):
                self._raw = numerator._raw
            else:
                raise TypeError(f"invalid numerator: `{numerator}`")
        else:
            if isinstance(numerator, (RationalFunction, Fraction, str)):
                raise TypeError(
                    f"invalid numerator as denominator is given: `{numerator}`"
                )
            if (
                isinstance(numerator, int)
                and isinstance(denominator, int)
                and Polynomial._is_short_int(numerator)
                and Polynomial._is_short_int(denominator)
            ):
                if denominator == 0:
                    raise ZeroDivisionError("division by zero")
                self._raw = _RawRationalFunction(numerator, denominator)
            else:
                num = Polynomial(numerator)
                den = Polynomial(denominator)
                if den.is_zero:
                    raise ZeroDivisionError("division by zero")
                self._raw = _RawRationalFunction(num._raw, den._raw)

    @staticmethod
    def _new(raw: Any) -> RationalFunction:
        """Construct a rational function from a raw object."""
        obj = RationalFunction()
        obj._raw = raw
        return obj

    def __getstate__(self) -> Any:
        """Get the object state."""
        return str(self._raw.toString())

    def __setstate__(self, state: Any) -> None:
        """Set the object state."""
        self._raw = _RawRationalFunction(state)

    def __str__(self) -> str:
        """Return the string representation."""
        return str(self._raw.toString())

    def __repr__(self) -> str:
        """Return the "official" string representation."""
        return f"RationalFunction('{str(self)}')"

    def __hash__(self) -> int:
        """Return the hash code."""
        if self.is_fraction:
            return hash(self.as_fraction)
        if self.is_polynomial:
            return hash(self.as_polynomial)
        return self._raw.hashCode()  # type: ignore[no-any-return]

    def __bool__(self) -> bool:
        """Return `True` for non-zero rational functions."""
        return not self.is_zero

    def __pos__(self) -> RationalFunction:
        """Return ``+ self``."""
        return self

    def __neg__(self) -> RationalFunction:
        """Return ``- self``."""
        return RationalFunction._new(self._raw.negate())

    def __add__(
        self, other: Union[RationalFunction, Polynomial, Variable, Fraction, int]
    ) -> RationalFunction:
        """Return ``self + other``."""
        if isinstance(other, RationalFunction):
            return RationalFunction._new(self._raw.add(other._raw))
        elif isinstance(other, (Polynomial, Variable, Fraction, int)):
            return self + RationalFunction(other)
        return NotImplemented  # type: ignore[unreachable]

    def __radd__(
        self, other: Union[Polynomial, Variable, Fraction, int]
    ) -> RationalFunction:
        """Return ``other + self``."""
        if isinstance(other, (Polynomial, Variable, Fraction, int)):
            return RationalFunction(other) + self
        return NotImplemented  # type: ignore[unreachable]

    def __sub__(
        self, other: Union[RationalFunction, Polynomial, Variable, Fraction, int]
    ) -> RationalFunction:
        """Return ``self - other``."""
        if isinstance(other, RationalFunction):
            return RationalFunction._new(self._raw.subtract(other._raw))
        elif isinstance(other, (Polynomial, Variable, Fraction, int)):
            return self - RationalFunction(other)
        return NotImplemented  # type: ignore[unreachable]

    def __rsub__(
        self, other: Union[Polynomial, Variable, Fraction, int]
    ) -> RationalFunction:
        """Return ``other - self``."""
        if isinstance(other, (Polynomial, Variable, Fraction, int)):
            return RationalFunction(other) - self
        return NotImplemented  # type: ignore[unreachable]

    def __mul__(
        self, other: Union[RationalFunction, Polynomial, Variable, Fraction, int]
    ) -> RationalFunction:
        """Return ``self * other``."""
        if isinstance(other, RationalFunction):
            return RationalFunction._new(self._raw.multiply(other._raw))
        elif isinstance(other, (Polynomial, Variable, Fraction, int)):
            return self * RationalFunction(other)
        return NotImplemented  # type: ignore[unreachable]

    def __rmul__(
        self, other: Union[Polynomial, Variable, Fraction, int]
    ) -> RationalFunction:
        """Return ``other * self``."""
        if isinstance(other, (Polynomial, Variable, Fraction, int)):
            return RationalFunction(other) * self
        return NotImplemented  # type: ignore[unreachable]

    def __truediv__(
        self, other: Union[RationalFunction, Polynomial, Variable, Fraction, int]
    ) -> RationalFunction:
        """Return ``self / other``."""
        if isinstance(other, RationalFunction):
            if other.is_zero:
                raise ZeroDivisionError("division by zero")
            return RationalFunction._new(self._raw.divide(other._raw))
        elif isinstance(other, (Polynomial, Variable, Fraction, int)):
            return self / RationalFunction(other)
        return NotImplemented  # type: ignore[unreachable]

    def __rtruediv__(
        self, other: Union[Polynomial, Variable, Fraction, int]
    ) -> RationalFunction:
        """Return ``other / self``."""
        if isinstance(other, (Polynomial, Variable, Fraction, int)):
            return RationalFunction(other) / self
        return NotImplemented  # type: ignore[unreachable]

    def __pow__(self, other: int) -> RationalFunction:
        """Return ``self ** other``."""
        if isinstance(other, int):
            if other <= -1 and self.is_zero:
                raise ZeroDivisionError("division by zero")
            return RationalFunction._new(self._raw.pow(other))
        return NotImplemented  # type: ignore[unreachable]

    def __eq__(self, other: object) -> bool:
        """Return ``self == other``."""
        if isinstance(other, RationalFunction):
            return self._raw.equals(other._raw)  # type: ignore[no-any-return]
        elif isinstance(other, (Polynomial, Variable, Fraction, int)):
            return self == RationalFunction(other)
        return NotImplemented

    @property
    def numerator(self) -> Polynomial:
        """Return the numerator."""
        return Polynomial._new(self._raw.getNumerator())

    @property
    def denominator(self) -> Polynomial:
        """Return the denominator."""
        return Polynomial._new(self._raw.getDenominator())

    @property
    def is_zero(self) -> bool:
        """Return `True` if the rational function is zero."""
        return self._raw.isZero()  # type: ignore[no-any-return]

    @property
    def is_one(self) -> bool:
        """Return `True` if the rational function is one."""
        return self._raw.isOne()  # type: ignore[no-any-return]

    @property
    def is_minus_one(self) -> bool:
        """Return `True` if the rational function is minus one."""
        return self._raw.isMinusOne()  # type: ignore[no-any-return]

    @property
    def is_integer(self) -> bool:
        """Return `True` if the rational function is an integer."""
        return self._raw.isInteger()  # type: ignore[no-any-return]

    @property
    def is_fraction(self) -> bool:
        """Return `True` if the rational function is a rational number."""
        return self._raw.isConstant()  # type: ignore[no-any-return]

    @property
    def is_polynomial(self) -> bool:
        """Return `True` if the rational function is a polynomial."""
        return self._raw.isPolynomial()  # type: ignore[no-any-return]

    @property
    def is_variable(self) -> bool:
        """Return `True` if the rational function is a variable."""
        return self.is_polynomial and self.numerator.is_variable

    @property
    def as_integer(self) -> int:
        """Cast the rational function to an integer."""
        if self.is_integer:
            return self.numerator.as_integer
        raise ValueError("not an integer")

    @property
    def as_fraction(self) -> Fraction:
        """Cast the rational function to a rational number."""
        if self.is_fraction:
            return Fraction(self.numerator.as_integer, self.denominator.as_integer)
        raise ValueError("not a rational number")

    @property
    def as_polynomial(self) -> Polynomial:
        """Cast the rational function to a polynomial."""
        if self.is_polynomial:
            return self.numerator
        raise ValueError("not a polynomial")

    @property
    def as_variable(self) -> Variable:
        """Cast the rational function to a variable."""
        if self.is_variable:
            return Variable._new(self._raw.getNumerator().asVariable())
        raise ValueError("not a variable")

    @property
    def variables(self) -> FrozenSet[Variable]:
        """Return the set of variables."""
        return VariableSet._frozenset_from_raw(self._raw.getVariables())

    @property
    def min_variables(self) -> FrozenSet[Variable]:
        """Return the set of actually used variables in this polynomial."""
        return VariableSet._frozenset_from_raw(self._raw.getMinimalVariables())

    @overload
    def translate(self, *variables: VariableLike) -> RationalFunction:
        """Translate the rational function in terms of the given set of variables."""
        ...

    @overload
    def translate(self, variables: VariableSetLike) -> RationalFunction:
        """Translate the rational function in terms of the given set of variables."""
        ...

    def translate(  # type: ignore[misc,no-untyped-def]
        self, *variables
    ) -> RationalFunction:
        """Translate the rational function in terms of the given set of variables."""
        if len(variables) == 1:
            xx = variables[0]
            if isinstance(xx, VariableSet):
                return self._translate_impl(xx._raw)
            elif isinstance(xx, Iterable) and not isinstance(xx, str):
                return self.translate(*xx)

        if any(not isinstance(x, (str, Variable)) for x in variables):
            raise TypeError("not Variable")

        return self._translate_impl(VariableSet._get_raw(variables))

    def _translate_impl(self, raw_varset: Any) -> RationalFunction:
        try:
            raw = self._raw.translate(raw_varset)
        except _JavaError as e:
            raise ValueError("invalid set of variables") from e
        return RationalFunction._new(raw)

    def subs(
        self,
        lhs: Union[Polynomial, Variable, str],
        rhs: Union[RationalFunction, Polynomial, Variable, Fraction, int, str],
    ) -> RationalFunction:
        """Return the result of the given substitution."""
        if isinstance(lhs, Polynomial):
            if isinstance(rhs, RationalFunction):
                try:
                    r = RationalFunction._new(self._raw.substitute(lhs._raw, rhs._raw))
                except _JavaError as e:
                    if jvm.get_error_message(e) == "division by zero":
                        raise ZeroDivisionError("division by zero") from e
                    else:
                        raise ValueError("invalid lhs for substitution") from e
                assert not r.denominator.is_zero  # noqa: S101  # just in case
                return r
            elif isinstance(rhs, (Polynomial, Variable, Fraction, int, str)):
                return self.subs(lhs, RationalFunction(rhs))
            else:
                raise TypeError("rhs is not a RationalFunction")
        elif isinstance(lhs, (Variable, str)):
            return self.subs(Polynomial(lhs), rhs)
        else:
            raise TypeError("lhs is not a Polynomial")

    @overload
    def evaluate(self, variable: Union[Variable, str], value: int) -> RationalFunction:
        """Return the result of setting the given variable to the specified value."""
        ...

    @overload
    def evaluate(
        self, variables: Sequence[Union[Variable, str]], values: Sequence[int]
    ) -> RationalFunction:
        """Return the result of setting the given variables to the specified values."""
        ...

    def evaluate(  # type: ignore[misc,no-untyped-def]
        self, variables, values
    ) -> RationalFunction:
        """Return the result of setting the given variables to the specified values."""
        # TODO: integer overflow occurs >= 2^31.

        if isinstance(variables, Sequence) and not isinstance(variables, str):
            if not (isinstance(values, Sequence) and not isinstance(values, str)):
                raise TypeError("values must be a sequence")
            if len(variables) != len(values):
                raise ValueError("variables and values have different sizes")
            try:
                return RationalFunction._new(
                    self._raw.evaluate(
                        _create_raw_var_array(tuple(variables)),
                        _create_raw_int_array(tuple(values)),
                    )
                )
            except _JavaError as e:
                if jvm.get_error_message(e) == "division by zero":
                    raise ZeroDivisionError("division by zero") from e
                raise e  # pragma: no cover

        if isinstance(variables, Variable):
            x = variables
            if not isinstance(values, int):
                raise TypeError("value must be an integer")
            n = values
            try:
                return RationalFunction._new(self._raw.evaluate(x._raw, n))
            except _JavaError as e:
                if jvm.get_error_message(e) == "division by zero":
                    raise ZeroDivisionError("division by zero") from e
                raise e  # pragma: no cover

        if isinstance(variables, str):
            return self.evaluate(Variable(variables), values)

        raise TypeError("invalid variables")

    @overload
    def evaluate_at_zero(self, *variables: VariableLike) -> RationalFunction:
        """Return the result of setting all the given variables to zero."""
        ...

    @overload
    def evaluate_at_zero(self, variables: VariableSetLike) -> RationalFunction:
        """Return the result of setting all the given variables to zero."""
        ...

    def evaluate_at_zero(  # type: ignore[misc,no-untyped-def]
        self, *variables
    ) -> RationalFunction:
        """Return the result of setting all the given variables to zero."""
        if len(variables) == 1:
            x = variables[0]
            if isinstance(x, (Variable, VariableSet)):
                try:
                    return RationalFunction._new(self._raw.evaluateAtZero(x._raw))
                except _JavaError as e:
                    if jvm.get_error_message(e) == "division by zero":
                        raise ZeroDivisionError("division by zero") from e
                    raise e  # pragma: no cover
            if isinstance(x, Iterable) and not isinstance(x, str):
                if not x:
                    # None of the variables are specified.
                    return self
                return self.evaluate_at_zero(*x)

        if len(variables) == 0:
            # None of the variables are specified.
            return self

        if any(not isinstance(x, (Variable, str)) for x in variables):
            raise TypeError("not Variable")

        return self.evaluate_at_zero(VariableSet(*variables))

    @overload
    def evaluate_at_one(self, *variables: VariableLike) -> RationalFunction:
        """Return the result of setting all the given variables to unity."""
        ...

    @overload
    def evaluate_at_one(self, variables: VariableSetLike) -> RationalFunction:
        """Return the result of setting all the given variables to unity."""
        ...

    def evaluate_at_one(  # type: ignore[misc,no-untyped-def]
        self, *variables
    ) -> RationalFunction:
        """Return the result of setting all the given variables to unity."""
        if len(variables) == 1:
            x = variables[0]
            if isinstance(x, (Variable, VariableSet)):
                try:
                    return RationalFunction._new(self._raw.evaluateAtOne(x._raw))
                except _JavaError as e:
                    if jvm.get_error_message(e) == "division by zero":
                        raise ZeroDivisionError("division by zero") from e
                    raise e  # pragma: no cover
            if isinstance(x, Iterable) and not isinstance(x, str):
                if not x:
                    # None of the variables are specified.
                    return self
                return self.evaluate_at_one(*x)

        if len(variables) == 0:
            # None of the variables are specified.
            return self

        if any(not isinstance(x, (Variable, str)) for x in variables):
            raise TypeError("not Variable")

        return self.evaluate_at_one(VariableSet(*variables))

    @overload
    def shift(self, variable: Union[Variable, str], shift: int) -> RationalFunction:
        """Return the result of the given variable shift."""
        ...

    @overload
    def shift(
        self, variables: Sequence[Union[Variable, str]], values: Sequence[int]
    ) -> RationalFunction:
        """Return the result of the given variable shifts."""
        ...

    def shift(  # type: ignore[misc,no-untyped-def]
        self, variables, values
    ) -> RationalFunction:
        """Return the result of the given variable shifts."""
        # TODO: integer overflow occurs >= 2^31.

        if isinstance(variables, Sequence) and not isinstance(variables, str):
            if not (isinstance(values, Sequence) and not isinstance(values, str)):
                raise TypeError("values must be a sequence")
            if len(variables) != len(values):
                raise ValueError("variables and values have different sizes")
            return RationalFunction._new(
                self._raw.shift(
                    _create_raw_var_array(tuple(variables)),
                    _create_raw_int_array(tuple(values)),
                )
            )

        if isinstance(variables, Variable):
            x = variables
            if not isinstance(values, int):
                raise TypeError("value must be an integer")
            n = values
            return RationalFunction._new(self._raw.shift(x._raw, n))

        if isinstance(variables, str):
            return self.shift(Variable(variables), values)

        raise TypeError("invalid variables")

    def diff(self, x: Union[Variable, str], n: int = 1) -> RationalFunction:
        """Differentiate this rational function."""
        if isinstance(x, str):
            x = Variable(x)

        if not isinstance(x, Variable):
            raise TypeError("x must be a Variable")
        if not isinstance(n, int):
            raise TypeError("n must be an int")
        if n < 0:
            raise ValueError("n must be non-negative")

        return RationalFunction._new(self._raw.derivative(x._raw, n))


# For static typing.
RationalFunctionLike = Union[RationalFunction, Polynomial, Variable, Fraction, int]
