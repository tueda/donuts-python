"""Polynomial."""
from __future__ import annotations

from fractions import Fraction
from typing import Any, Iterator, List, Union

from .jvm import jvm

_RawPolynomial = jvm.find_class("com.github.tueda.donuts.Polynomial")
_JavaError = jvm.java_error_class


class Polynomial:
    """Polynomial."""

    __slots__ = ("_raw",)

    __ZERO = _RawPolynomial()

    def __init__(self, value: Union[int, str, Polynomial, None] = None) -> None:
        """Construct a polynomial."""
        if value is None:
            self._raw = Polynomial.__ZERO
        elif isinstance(value, int):
            if Polynomial._is_short_int(value):
                self._raw = _RawPolynomial(value)
            else:
                self._raw = _RawPolynomial(str(value))
        elif isinstance(value, str):
            try:
                self._raw = _RawPolynomial(value)
            except _JavaError as e:
                raise ValueError("invalid string for polynomial") from e
        elif isinstance(value, Polynomial):
            self._raw = value._raw
        else:
            raise TypeError(f"invalid value for polynomial: `{value}`")

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

    def __repr__(self) -> str:
        """Return the "official" string representation."""
        return f"Polynomial('{self._raw}')"

    def __hash__(self) -> int:
        """Return the hash code."""
        if self.is_integer:
            return hash(self.as_integer)
        return hash(self._raw)

    def __len__(self) -> int:
        """Return the number of terms in this polynomial."""
        return self._raw.size()  # type: ignore

    def __iter__(self) -> Iterator[Polynomial]:
        """Return an iterator to iterate terms in this polynomial."""
        raw_it = self._raw.iterator()
        while raw_it.hasNext():
            yield Polynomial._new(next(raw_it))

    def __pos__(self) -> Polynomial:
        """Return ``+ self``."""
        return self

    def __neg__(self) -> Polynomial:
        """Return ``- self``."""
        return Polynomial._new(self._raw.negate())

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

    def __truediv__(self, other: Union[Polynomial, Fraction, int]) -> RationalFunction:
        """Return ``self / other``."""
        if isinstance(other, (Polynomial, int)):
            return RationalFunction(self, other)
        elif isinstance(other, Fraction):
            return RationalFunction(self) / RationalFunction(other)
        return NotImplemented  # type: ignore

    def __rtruediv__(self, other: Union[Fraction, int]) -> RationalFunction:
        """Return ``other / self``."""
        if isinstance(other, int):
            return RationalFunction(other, self)
        elif isinstance(other, Fraction):
            return RationalFunction(other) / RationalFunction(self)
        return NotImplemented  # type: ignore

    def __pow__(self, other: int) -> Polynomial:
        """Return ``self ** other``."""
        if isinstance(other, int):
            if other <= -1:
                raise ValueError("negative power given for polynomial")
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

    @property
    def signum(self) -> int:
        """Return the signum of the leading coefficient."""
        return self._raw.signum()  # type: ignore

    def gcd(self, other: Polynomial) -> Polynomial:
        """Return ``GCD(self, other)``."""
        return Polynomial._new(self._raw.gcd(other._raw))

    def factorize(self) -> List[Polynomial]:
        """Factorize this polynomial."""
        return [Polynomial._new(x) for x in self._raw.factorize()]


# This import should be after the definition of Polynomial.
from .rat import RationalFunction  # isort:skip  # noqa: E402
