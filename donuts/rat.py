"""Routines for rational functions."""
from __future__ import annotations

from fractions import Fraction
from typing import Union

from .jvm import jvm
from .poly import Polynomial

_RawRationalFunction = jvm.find_class("com.github.tueda.donuts.RationalFunction")


class RationalFunction:
    """Rational function."""

    __slots__ = ("_raw",)

    def __init__(
        self,
        numerator: Union[int, str, Fraction, Polynomial, RationalFunction, None] = None,
        denominator: Union[int, Polynomial, None] = None,
    ) -> None:
        """Construct a rational function."""
        if denominator is None:
            if numerator is None:
                self._raw = _RawRationalFunction()
            elif isinstance(numerator, int):
                if Polynomial._is_short_int(numerator):
                    self._raw = _RawRationalFunction(numerator)
                else:
                    self._raw = _RawRationalFunction(str(numerator))
            elif isinstance(numerator, str):
                self._raw = _RawRationalFunction(numerator)
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
                self._raw = _RawRationalFunction(numerator, denominator)
            else:
                self._raw = _RawRationalFunction(
                    Polynomial(numerator)._raw, Polynomial(denominator)._raw
                )

    def __str__(self) -> str:
        """Return the string representation."""
        return str(self._raw)

    def __hash__(self) -> int:
        """Return the hash code."""
        if self.is_integer:
            return hash(self.as_integer)
        if self.is_fraction:
            return hash(self.as_fraction)
        if self.is_polynomial:
            return hash(self.as_polynomial)
        return hash(self._raw)

    def __eq__(self, other: object) -> bool:
        """Return ``self == other``."""
        if isinstance(other, RationalFunction):
            return self._raw.equals(other._raw)  # type: ignore
        elif isinstance(other, (int, Fraction, Polynomial)):
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
