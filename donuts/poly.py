"""Polynomial."""
from __future__ import annotations

from typing import Any, Union

from .jvm import jvm

_RawPolynomial = jvm.find_class("com.github.tueda.donuts.Polynomial")


class Polynomial:
    """Polynomial."""

    __slots__ = ("_raw",)

    def __init__(self, value: Union[int, str, None] = None) -> None:
        """Construct a polynomial."""
        if value is None:
            self._raw = _RawPolynomial()
        elif isinstance(value, int):
            if Polynomial._is_short_int(value):
                self._raw = _RawPolynomial(value)
            else:
                self._raw = _RawPolynomial(str(value))
        else:
            self._raw = _RawPolynomial(value)

    @staticmethod
    def _new(raw: Any) -> Polynomial:
        """Construct a polynomial from a raw object."""
        obj = Polynomial()
        obj._raw = raw
        return obj

    @staticmethod
    def _is_short_int(n: int) -> bool:
        """Return `True` if the given integer is *short* enough (64 bits)."""
        return -9223372036854775808 <= n <= 9223372036854775807

    def __str__(self) -> str:
        """Return the string representation."""
        return str(self._raw)

    def __hash__(self) -> int:
        """Return the hash code."""
        if self.is_integer:
            return hash(self.as_integer)
        return hash(self._raw)

    def __add__(self, other: Union[Polynomial, int]) -> Polynomial:
        """Return ``self + other``."""
        if isinstance(other, Polynomial):
            return Polynomial._new(self._raw.add(other._raw))
        elif isinstance(other, int):
            return self + Polynomial(other)
        return NotImplemented  # type: ignore

    def __radd__(self, other: int) -> Polynomial:
        """Return ``other + self``."""
        if isinstance(other, int):
            return Polynomial(other) + self
        return NotImplemented  # type: ignore

    def __sub__(self, other: Union[Polynomial, int]) -> Polynomial:
        """Return ``self - other``."""
        if isinstance(other, Polynomial):
            return Polynomial._new(self._raw.subtract(other._raw))
        elif isinstance(other, int):
            return self - Polynomial(other)
        return NotImplemented  # type: ignore

    def __rsub__(self, other: int) -> Polynomial:
        """Return ``other - self``."""
        if isinstance(other, int):
            return Polynomial(other) - self
        return NotImplemented  # type: ignore

    def __mul__(self, other: Union[Polynomial, int]) -> Polynomial:
        """Return ``self * other``."""
        if isinstance(other, Polynomial):
            return Polynomial._new(self._raw.multiply(other._raw))
        elif isinstance(other, int):
            return self * Polynomial(other)
        return NotImplemented  # type: ignore

    def __rmul__(self, other: int) -> Polynomial:
        """Return ``other * self``."""
        if isinstance(other, int):
            return Polynomial(other) * self
        return NotImplemented  # type: ignore

    def __pow__(self, other: int) -> Polynomial:
        """Return ``self ** other``."""
        if isinstance(other, int):
            return Polynomial._new(self._raw.pow(other))
        return NotImplemented  # type: ignore

    def __eq__(self, other: object) -> bool:
        """Return ``self == other``."""
        if isinstance(other, Polynomial):
            return self._raw.equals(other._raw)  # type: ignore
        elif isinstance(other, int):
            return self == Polynomial(other)
        return NotImplemented

    @property
    def is_zero(self) -> bool:
        """Return `True` if the polynomial is zero."""
        return self._raw.isZero()  # type: ignore

    @property
    def is_one(self) -> bool:
        """Return `True` if the polynomial is one."""
        return self._raw.isOne()  # type: ignore

    @property
    def is_minus_one(self) -> bool:
        """Return `True` if the polynomial is minus one."""
        return self._raw.isMinusOne()  # type: ignore

    @property
    def is_integer(self) -> bool:
        """Return `True` if the polynomial is an integer."""
        return self._raw.isConstant()  # type: ignore

    @property
    def is_monomial(self) -> bool:
        """Return `True` if the polynomial is monomial."""
        return self._raw.isMonomial()  # type: ignore

    @property
    def is_monic(self) -> bool:
        """Return `True` if the polynomial is monic."""
        return self._raw.isMonic()  # type: ignore

    @property
    def is_variable(self) -> bool:
        """Return `True` if the polynomial is a variable."""
        return self._raw.isVariable()  # type: ignore

    @property
    def as_integer(self) -> int:
        """Cast the polynomial to an integer."""
        if self.is_integer:
            if self._raw.isLongValue():
                return self._raw.asLongValue()  # type: ignore
            else:
                return int(str(self))
        raise ValueError("not an integer")
