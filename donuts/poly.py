"""Polynomial."""
from __future__ import annotations

from collections.abc import Collection
from fractions import Fraction
from typing import Any, Iterable, Iterator, List, Sequence, Union, overload

from .jvm import jvm

_RawPolynomial = jvm.find_class("com.github.tueda.donuts.Polynomial")
_JavaError = jvm.java_error_class
_new_array = jvm.new_array

# TODO: Remove workaround for F811 once new pyflakes is available.
# See PyCQA/pyflakes#320.


class Polynomial:
    """Polynomial."""

    __slots__ = ("_raw",)

    __RAW_ZERO = _RawPolynomial()

    def __init__(
        self, value: Union[Polynomial, Variable, int, str, None] = None
    ) -> None:
        """Construct a polynomial."""
        if value is None:
            self._raw = Polynomial.__RAW_ZERO
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
        elif isinstance(value, Variable):
            self._raw = _RawPolynomial(value._name)
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

    def __getstate__(self) -> Any:
        """Get the object state."""
        return self._raw.toString()

    def __setstate__(self, state: Any) -> None:
        """Set the object state."""
        self._raw = _RawPolynomial(state)

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
        if self.is_variable:
            return hash(self.as_variable)
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

    def __add__(self, other: Union[Polynomial, Variable, int]) -> Polynomial:
        """Return ``self + other``."""
        if isinstance(other, Polynomial):
            return Polynomial._new(self._raw.add(other._raw))
        elif isinstance(other, (Variable, int)):
            return self + Polynomial(other)
        return NotImplemented  # type: ignore

    def __radd__(self, other: Union[Variable, int]) -> Polynomial:
        """Return ``other + self``."""
        if isinstance(other, (Variable, int)):
            return Polynomial(other) + self
        return NotImplemented  # type: ignore

    def __sub__(self, other: Union[Polynomial, Variable, int]) -> Polynomial:
        """Return ``self - other``."""
        if isinstance(other, Polynomial):
            return Polynomial._new(self._raw.subtract(other._raw))
        elif isinstance(other, (Variable, int)):
            return self - Polynomial(other)
        return NotImplemented  # type: ignore

    def __rsub__(self, other: Union[Variable, int]) -> Polynomial:
        """Return ``other - self``."""
        if isinstance(other, (Variable, int)):
            return Polynomial(other) - self
        return NotImplemented  # type: ignore

    def __mul__(self, other: Union[Polynomial, Variable, int]) -> Polynomial:
        """Return ``self * other``."""
        if isinstance(other, Polynomial):
            return Polynomial._new(self._raw.multiply(other._raw))
        elif isinstance(other, (Variable, int)):
            return self * Polynomial(other)
        return NotImplemented  # type: ignore

    def __rmul__(self, other: Union[Variable, int]) -> Polynomial:
        """Return ``other * self``."""
        if isinstance(other, (Variable, int)):
            return Polynomial(other) * self
        return NotImplemented  # type: ignore

    def __truediv__(
        self, other: Union[Polynomial, Variable, Fraction, int]
    ) -> RationalFunction:
        """Return ``self / other``."""
        if isinstance(other, (Polynomial, Variable, int)):
            return RationalFunction(self, other)
        elif isinstance(other, Fraction):
            return RationalFunction(self) / RationalFunction(other)
        return NotImplemented  # type: ignore

    def __rtruediv__(self, other: Union[Variable, Fraction, int]) -> RationalFunction:
        """Return ``other / self``."""
        if isinstance(other, (Variable, int)):
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
        elif isinstance(other, (Variable, int)):
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
    def as_variable(self) -> Variable:
        """Cast the polynomial to a variable."""
        if self.is_variable:
            return Variable._new(self._raw.asVariable())
        raise ValueError("not a variable")

    @property
    def signum(self) -> int:
        """Return the signum of the leading coefficient."""
        return self._raw.signum()  # type: ignore

    @property
    def variables(self) -> VariableSet:
        """Return the set of variables."""
        return VariableSet._new(self._raw.getVariables())

    @property
    def min_variables(self) -> VariableSet:
        """Return the set of actually used variables in this polynomial."""
        return VariableSet._new(self._raw.getMinimalVariables())

    @overload
    def degree(self) -> int:
        """Return the total degree."""
        ...

    @overload  # noqa: F811
    def degree(self, *variables: Union[Variable, str]) -> int:  # noqa: F811
        """Return the degree with respect to the given variables."""
        ...

    @overload  # noqa: F811
    def degree(self, variables: VariableSetLike) -> int:  # noqa: F811
        """Return the degree with respect to the given variables."""
        ...

    def degree(self, *variables) -> int:  # type: ignore  # noqa: F811
        """Return the degree with respect to the specified variables."""
        if len(variables) == 0:
            # Return the total degree.
            return self._raw.degree()  # type: ignore

        if len(variables) == 1:
            x = variables[0]
            if isinstance(x, Variable):
                return self._raw.degree(x._raw)  # type: ignore
            if isinstance(x, VariableSet):
                return self._raw.degree(x._raw)  # type: ignore
            if isinstance(x, Collection) and not isinstance(x, str):
                if not x:
                    # None of the variables are specified.
                    return 0
                return self.degree(*x)

        if any(not isinstance(x, (Variable, str)) for x in variables):
            raise TypeError("not Variable")

        return self._raw.degree(VariableSet(*variables)._raw)  # type: ignore

    def coeff(self, x: Union[Variable, str], n: int) -> Polynomial:
        """Return the coefficient of ``x^n``."""
        if isinstance(x, str):
            x = Variable(x)
        if not isinstance(x, Variable):
            raise TypeError("x must be a Variable")
        if not isinstance(n, int):
            raise TypeError("n must be an int")

        return Polynomial._new(self._raw.coefficientOf(x._raw, n))

    @overload
    def translate(self, *variables: Union[Variable, str]) -> Polynomial:
        """Translate the polynomial in terms of the given set of variables."""
        ...

    @overload  # noqa: F811
    def translate(self, variables: VariableSetLike) -> Polynomial:  # noqa: F811
        """Translate the polynomial in terms of the given set of variables."""
        ...

    def translate(self, *variables) -> Polynomial:  # type: ignore  # noqa: F811
        """Translate the polynomial in terms of the given set of variables."""
        if len(variables) == 1:
            xx = variables[0]
            if isinstance(xx, VariableSet):
                return self._translate_impl(xx._raw)
            elif isinstance(xx, Collection) and not isinstance(xx, str):
                return self.translate(*xx)

        if any(not isinstance(x, (Variable, str)) for x in variables):
            raise TypeError("not Variable")

        return self._translate_impl(VariableSet(*variables)._raw)

    def _translate_impl(self, raw_varset: Any) -> Polynomial:
        try:
            raw = self._raw.translate(raw_varset)
        except _JavaError as e:
            raise ValueError("invalid set of variables") from e
        return Polynomial._new(raw)

    def gcd(self, other: Union[Polynomial, Variable, int]) -> Polynomial:
        """Return ``GCD(self, other)``."""
        if isinstance(other, (Variable, int)):
            return self.gcd(Polynomial(other))
        if not isinstance(other, Polynomial):
            raise TypeError("other must be a Polynomial")
        return Polynomial._new(self._raw.gcd(other._raw))

    def lcm(self, other: Union[Polynomial, Variable, int]) -> Polynomial:
        """Return ``LCM(self, other)``."""
        if isinstance(other, (Variable, int)):
            return self.lcm(Polynomial(other))
        if not isinstance(other, Polynomial):
            raise TypeError("other must be a Polynomial")
        return Polynomial._new(self._raw.lcm(other._raw))

    def factors(self) -> List[Polynomial]:
        """Return the factorization of this polynomial."""
        return [Polynomial._new(x) for x in self._raw.factors()]

    def subs(
        self,
        lhs: Union[Polynomial, Variable, str],
        rhs: Union[Polynomial, Variable, int, str],
    ) -> Polynomial:
        """Return the result of the given substitution."""
        if isinstance(lhs, Polynomial):
            if isinstance(rhs, Polynomial):
                try:
                    return Polynomial._new(self._raw.substitute(lhs._raw, rhs._raw))
                except _JavaError as e:
                    raise ValueError("invalid lhs for substitution") from e
            elif isinstance(rhs, (Variable, int, str)):
                return self.subs(lhs, Polynomial(rhs))
            else:
                raise TypeError("rhs is not a Polynomial")
        elif isinstance(lhs, (Variable, str)):
            return self.subs(Polynomial(lhs), rhs)
        else:
            raise TypeError("lhs is not a Polynomial")


def _create_raw_poly_array(polynomials: Sequence[Any]) -> Any:
    if len(polynomials) == 1:
        x = polynomials[0]
        if isinstance(x, Sequence) and not isinstance(x, (Polynomial, str)):
            return _create_raw_poly_array(x)
        if isinstance(x, Iterable) and not isinstance(x, (Polynomial, str)):
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


@overload
def gcd(*polynomials: Union[Polynomial, Variable, int]) -> Polynomial:
    """Return the GCD of the given polynomials."""
    ...


@overload
def gcd(polynomials: Iterable[Union[Polynomial, Variable, int]]) -> Polynomial:
    """Return the GCD of the given polynomials."""
    ...


def gcd(*polynomials) -> Polynomial:  # type: ignore
    """Return the GCD of the given polynomials."""
    array = _create_raw_poly_array(polynomials)
    return Polynomial._new(_RawPolynomial.gcdOf(array))


@overload
def lcm(*polynomials: Union[Polynomial, Variable, int]) -> Polynomial:
    """Return the LCM of the given polynomials."""
    ...


@overload
def lcm(polynomials: Iterable[Union[Polynomial, Variable, int]]) -> Polynomial:
    """Return the LCM of the given polynomials."""
    ...


def lcm(*polynomials) -> Polynomial:  # type: ignore
    """Return the LCM of the given polynomials."""
    array = _create_raw_poly_array(polynomials)
    if len(polynomials) == 0:
        raise ValueError("lcm with no arguments")
    return Polynomial._new(_RawPolynomial.lcmOf(array))


# These imports should be after the definition of Polynomial.
from .varset import Variable, VariableSet, VariableSetLike  # isort:skip  # noqa: E402
from .rat import RationalFunction  # isort:skip  # noqa: E402
