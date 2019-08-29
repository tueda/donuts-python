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
            if -9223372036854775808 <= value <= 9223372036854775807:
                self._raw = _RawPolynomial(value)
            else:
                self._raw = _RawPolynomial(str(value))
        else:
            self._raw = _RawPolynomial(value)

    @staticmethod
    def _new(raw: Any) -> Polynomial:
        obj = Polynomial()
        obj._raw = raw
        return obj

    def __str__(self) -> str:
        """Return the string representation."""
        return str(self._raw)

    def __hash__(self) -> int:
        """Return the hash code."""
        return hash(self._raw)

    def __add__(self, other: Union[Polynomial, int]) -> Polynomial:
        """Return `self + other`."""
        if isinstance(other, Polynomial):
            return Polynomial._new(self._raw.add(other._raw))
        elif isinstance(other, int):
            return self + Polynomial(other)
        return NotImplemented  # type: ignore

    def __radd__(self, other: int) -> Polynomial:
        """Return `other + self`."""
        if isinstance(other, int):
            return Polynomial(other) + self
        return NotImplemented  # type: ignore

    def __sub__(self, other: Union[Polynomial, int]) -> Polynomial:
        """Return `self - other`."""
        if isinstance(other, Polynomial):
            return Polynomial._new(self._raw.subtract(other._raw))
        elif isinstance(other, int):
            return self - Polynomial(other)
        return NotImplemented  # type: ignore

    def __rsub__(self, other: int) -> Polynomial:
        """Return `other - self`."""
        if isinstance(other, int):
            return Polynomial(other) - self
        return NotImplemented  # type: ignore

    def __mul__(self, other: Union[Polynomial, int]) -> Polynomial:
        """Return `self * other`."""
        if isinstance(other, Polynomial):
            return Polynomial._new(self._raw.multiply(other._raw))
        elif isinstance(other, int):
            return self * Polynomial(other)
        return NotImplemented  # type: ignore

    def __rmul__(self, other: int) -> Polynomial:
        """Return `other * self`."""
        if isinstance(other, int):
            return Polynomial(other) * self
        return NotImplemented  # type: ignore

    def __pow__(self, other: int) -> Polynomial:
        """Return `self ** other`."""
        if isinstance(other, int):
            return Polynomial._new(self._raw.pow(other))
        return NotImplemented  # type: ignore

    def __eq__(self, other: object) -> bool:
        """Return `self == other`."""
        if isinstance(other, Polynomial):
            return self._raw.equals(other._raw)  # type: ignore
        elif isinstance(other, int):
            return self == Polynomial(other)
        return NotImplemented
