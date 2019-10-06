"""Routines for rational functions."""
from __future__ import annotations

from collections.abc import Collection
from fractions import Fraction
from typing import Any, Union, overload

from .jvm import jvm
from .poly import Polynomial
from .varset import Variable, VariableSet, VariableSetLike

_RawRationalFunction = jvm.find_class("com.github.tueda.donuts.RationalFunction")
_JavaError = jvm.java_error_class

# TODO: Remove workaround for F811 once new pyflakes is available.
# See PyCQA/pyflakes#320.


class RationalFunction:
    """Rational function."""

    __slots__ = ("_raw",)

    __RAW_ZERO = _RawRationalFunction()

    def __init__(
        self,
        numerator: Union[
            int, str, Fraction, Variable, Polynomial, RationalFunction, None
        ] = None,
        denominator: Union[int, Variable, Polynomial, None] = None,
    ) -> None:
        """Construct a rational function."""
        if denominator is None:
            if numerator is None:
                self._raw = RationalFunction.__RAW_ZERO
            elif isinstance(numerator, int):
                if Polynomial._is_short_int(numerator):
                    self._raw = _RawRationalFunction(numerator)
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
                self._raw = _RawRationalFunction(numerator._name)
            elif isinstance(numerator, Polynomial):
                self._raw = _RawRationalFunction(numerator._raw)
            elif isinstance(numerator, RationalFunction):
                self._raw = numerator._raw
            else:
                raise TypeError(f"invalid numerator: `{numerator}`")
        else:
            if isinstance(numerator, (str, Fraction, RationalFunction)):
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
        return self._raw.toString()

    def __setstate__(self, state: Any) -> None:
        """Set the object state."""
        self._raw = _RawRationalFunction(state)

    def __str__(self) -> str:
        """Return the string representation."""
        return str(self._raw)

    def __repr__(self) -> str:
        """Return the "official" string representation."""
        return f"RationalFunction('{self._raw}')"

    def __hash__(self) -> int:
        """Return the hash code."""
        if self.is_fraction:
            return hash(self.as_fraction)
        if self.is_polynomial:
            return hash(self.as_polynomial)
        return hash(self._raw)

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
        self, other: Union[RationalFunction, Polynomial, Fraction, int]
    ) -> RationalFunction:
        """Return ``self + other``."""
        if isinstance(other, RationalFunction):
            return RationalFunction._new(self._raw.add(other._raw))
        elif isinstance(other, (Polynomial, Fraction, int)):
            return self + RationalFunction(other)
        return NotImplemented  # type: ignore

    def __radd__(self, other: Union[Polynomial, Fraction, int]) -> RationalFunction:
        """Return ``other + self``."""
        if isinstance(other, (Polynomial, Fraction, int)):
            return RationalFunction(other) + self
        return NotImplemented  # type: ignore

    def __sub__(
        self, other: Union[RationalFunction, Polynomial, Fraction, int]
    ) -> RationalFunction:
        """Return ``self - other``."""
        if isinstance(other, RationalFunction):
            return RationalFunction._new(self._raw.subtract(other._raw))
        elif isinstance(other, (Polynomial, Fraction, int)):
            return self - RationalFunction(other)
        return NotImplemented  # type: ignore

    def __rsub__(self, other: Union[Polynomial, Fraction, int]) -> RationalFunction:
        """Return ``other - self``."""
        if isinstance(other, (Polynomial, Fraction, int)):
            return RationalFunction(other) - self
        return NotImplemented  # type: ignore

    def __mul__(
        self, other: Union[RationalFunction, Polynomial, Fraction, int]
    ) -> RationalFunction:
        """Return ``self * other``."""
        if isinstance(other, RationalFunction):
            return RationalFunction._new(self._raw.multiply(other._raw))
        elif isinstance(other, (Polynomial, Fraction, int)):
            return self * RationalFunction(other)
        return NotImplemented  # type: ignore

    def __rmul__(self, other: Union[Polynomial, Fraction, int]) -> RationalFunction:
        """Return ``other * self``."""
        if isinstance(other, (Polynomial, Fraction, int)):
            return RationalFunction(other) * self
        return NotImplemented  # type: ignore

    def __truediv__(
        self, other: Union[RationalFunction, Polynomial, Fraction, int]
    ) -> RationalFunction:
        """Return ``self / other``."""
        if isinstance(other, RationalFunction):
            if other.is_zero:
                raise ZeroDivisionError("division by zero")
            return RationalFunction._new(self._raw.divide(other._raw))
        elif isinstance(other, (Polynomial, Fraction, int)):
            return self / RationalFunction(other)
        return NotImplemented  # type: ignore

    def __rtruediv__(self, other: Union[Polynomial, Fraction, int]) -> RationalFunction:
        """Return ``other / self``."""
        if isinstance(other, (Polynomial, Fraction, int)):
            return RationalFunction(other) / self
        return NotImplemented  # type: ignore

    def __pow__(self, other: int) -> RationalFunction:
        """Return ``self ** other``."""
        if isinstance(other, int):
            if other <= -1 and self.is_zero:
                raise ZeroDivisionError("division by zero")
            return RationalFunction._new(self._raw.pow(other))
        return NotImplemented  # type: ignore

    def __eq__(self, other: object) -> bool:
        """Return ``self == other``."""
        if isinstance(other, RationalFunction):
            return self._raw.equals(other._raw)  # type: ignore
        elif isinstance(other, (int, Fraction, Variable, Polynomial)):
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
        return self._raw.isZero()  # type: ignore

    @property
    def is_one(self) -> bool:
        """Return `True` if the rational function is one."""
        return self._raw.isOne()  # type: ignore

    @property
    def is_minus_one(self) -> bool:
        """Return `True` if the rational function is minus one."""
        return self._raw.isMinusOne()  # type: ignore

    @property
    def is_integer(self) -> bool:
        """Return `True` if the rational function is an integer."""
        return self._raw.isInteger()  # type: ignore

    @property
    def is_fraction(self) -> bool:
        """Return `True` if the rational function is a rational number."""
        return self._raw.isConstant()  # type: ignore

    @property
    def is_polynomial(self) -> bool:
        """Return `True` if the rational function is a polynomial."""
        return self._raw.isPolynomial()  # type: ignore

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
    def variables(self) -> VariableSet:
        """Return the set of variables."""
        return VariableSet._new(self._raw.getVariables())

    @property
    def min_variables(self) -> VariableSet:
        """Return the set of actually used variables in this polynomial."""
        return VariableSet._new(self._raw.getMinimalVariables())

    @overload
    def translate(self, *variables: Union[Variable, str]) -> RationalFunction:
        """Translate the rational function in terms of the given set of variables."""
        ...

    @overload  # noqa: F811
    def translate(self, variables: VariableSetLike) -> RationalFunction:
        """Translate the rational function in terms of the given set of variables."""
        ...

    def translate(self, *variables) -> RationalFunction:  # type: ignore  # noqa: F811
        """Translate the rational function in terms of the given set of variables."""
        if len(variables) == 1:
            xx = variables[0]
            if isinstance(xx, VariableSet):
                return self._translate_impl(xx._raw)
            elif isinstance(xx, Collection) and not isinstance(xx, str):
                return self.translate(*xx)

        if any(not isinstance(x, (str, Variable)) for x in variables):
            raise TypeError("not Variable")

        return self._translate_impl(VariableSet(*variables)._raw)

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
                    if e.java_exception.getMessage() == "division by zero":
                        raise ZeroDivisionError("division by zero") from e
                    else:
                        raise ValueError("invalid lhs for substitution") from e
                assert not r.denominator.is_zero
                return r
            elif isinstance(rhs, (Polynomial, Variable, Fraction, int, str)):
                return self.subs(lhs, RationalFunction(rhs))
            else:
                raise TypeError("rhs is not a RationalFunction")
        elif isinstance(lhs, (Variable, str)):
            return self.subs(Polynomial(lhs), rhs)
        else:
            raise TypeError("lhs is not a Polynomial")
