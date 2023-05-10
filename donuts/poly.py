"""Polynomial."""

from __future__ import annotations

import functools
from fractions import Fraction
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    FrozenSet,
    Iterable,
    Iterator,
    Optional,
    Sequence,
    Union,
    overload,
)

from .array import _create_raw_int_array, _create_raw_poly_array, _create_raw_var_array
from .jvm import jvm
from .var import Variable, VariableLike
from .varset import VariableSet, VariableSetLike

if TYPE_CHECKING:
    from .rat import RationalFunction

_RawPolynomial = jvm.find_class("com.github.tueda.donuts.Polynomial")
_RawPythonUtils = jvm.find_class("com.github.tueda.donuts.python.PythonUtils")
_JavaError = jvm.java_error_class

_RAW_ZERO = _RawPolynomial()
_RAW_ONE = _RawPolynomial(1)
_RAW_MINUS_ONE = _RawPolynomial(-1)


def _raw_polynomial_from_short_int(value: int) -> Any:
    if value == 0:
        return _RAW_ZERO
    if value == 1:
        return _RAW_ONE
    if value == -1:
        return _RAW_MINUS_ONE
    return _raw_polynomial_from_short_int_impl(value)


@functools.lru_cache(maxsize=1024)
def _raw_polynomial_from_short_int_impl(value: int) -> Any:
    return _RawPolynomial(value)


@functools.lru_cache(maxsize=1024)
def _raw_polynomial_from_str(value: str) -> Any:
    return _RawPolynomial(value)


class Polynomial:
    """Polynomial."""

    __slots__ = ("_raw", "_cache_factors")

    def __init__(
        self, value: Union[Polynomial, Variable, int, str, None] = None
    ) -> None:
        """Construct a polynomial."""
        self._cache_factors: Optional[Sequence[Polynomial]] = None

        if value is None:
            self._raw = _RAW_ZERO
        elif isinstance(value, int):
            if Polynomial._is_short_int(value):
                self._raw = _raw_polynomial_from_short_int(value)
            else:
                self._raw = _RawPolynomial(str(value))
        elif isinstance(value, str):
            try:
                self._raw = _RawPolynomial(value)
            except _JavaError as e:
                raise ValueError("invalid string for polynomial") from e
        elif isinstance(value, Variable):
            self._raw = _raw_polynomial_from_str(value._name)
        elif isinstance(value, Polynomial):
            self._raw = value._raw
            self._cache_factors = value._cache_factors
        else:
            raise TypeError(f"invalid value for polynomial: `{value}`")

    @staticmethod
    def _new(raw: Any) -> Polynomial:
        """Construct a polynomial from a raw object."""
        obj = Polynomial()
        obj._raw = raw
        obj._cache_factors = None
        return obj

    @staticmethod
    def _is_short_int(n: int) -> bool:
        """Return `True` if the given integer is *short* enough (64 bits)."""
        return -9223372036854775808 <= n <= 9223372036854775807

    def __getstate__(self) -> Any:
        """Get the object state."""
        return str(self._raw.toString())

    def __setstate__(self, state: Any) -> None:
        """Set the object state."""
        self._raw = _RawPolynomial(state)
        self._cache_factors = None

    def __str__(self) -> str:
        """Return the string representation."""
        return str(self._raw.toString())

    def __repr__(self) -> str:
        """Return the "official" string representation."""
        return f"Polynomial('{str(self)}')"

    def __hash__(self) -> int:
        """Return the hash code."""
        if self.is_integer:
            return hash(self.as_integer)
        if self.is_variable:
            return hash(self.as_variable)
        return self._raw.hashCode()  # type: ignore[no-any-return]

    def __len__(self) -> int:
        """Return the number of terms in this polynomial."""
        return self._raw.size()  # type: ignore[no-any-return]

    def __iter__(self) -> Iterator[Polynomial]:
        """Return an iterator to iterate terms in this polynomial."""
        raw_it = self._raw.iterator()
        while raw_it.hasNext():
            yield Polynomial._new(raw_it.next())  # noqa: B305

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
        return NotImplemented  # type: ignore[unreachable]

    def __radd__(self, other: Union[Variable, int]) -> Polynomial:
        """Return ``other + self``."""
        if isinstance(other, (Variable, int)):
            return Polynomial(other) + self
        return NotImplemented  # type: ignore[unreachable]

    def __sub__(self, other: Union[Polynomial, Variable, int]) -> Polynomial:
        """Return ``self - other``."""
        if isinstance(other, Polynomial):
            return Polynomial._new(self._raw.subtract(other._raw))
        elif isinstance(other, (Variable, int)):
            return self - Polynomial(other)
        return NotImplemented  # type: ignore[unreachable]

    def __rsub__(self, other: Union[Variable, int]) -> Polynomial:
        """Return ``other - self``."""
        if isinstance(other, (Variable, int)):
            return Polynomial(other) - self
        return NotImplemented  # type: ignore[unreachable]

    def __mul__(self, other: Union[Polynomial, Variable, int]) -> Polynomial:
        """Return ``self * other``."""
        if isinstance(other, Polynomial):
            return Polynomial._new(self._raw.multiply(other._raw))
        elif isinstance(other, (Variable, int)):
            return self * Polynomial(other)
        return NotImplemented  # type: ignore[unreachable]

    def __rmul__(self, other: Union[Variable, int]) -> Polynomial:
        """Return ``other * self``."""
        if isinstance(other, (Variable, int)):
            return Polynomial(other) * self
        return NotImplemented  # type: ignore[unreachable]

    def __truediv__(
        self, other: Union[Polynomial, Variable, Fraction, int]
    ) -> RationalFunction:
        """Return ``self / other``."""
        from .rat import RationalFunction

        if isinstance(other, (Polynomial, Variable, int)):
            return RationalFunction(self, other)
        elif isinstance(other, Fraction):
            return RationalFunction(self) / RationalFunction(other)
        return NotImplemented  # type: ignore[unreachable]

    def __rtruediv__(self, other: Union[Variable, Fraction, int]) -> RationalFunction:
        """Return ``other / self``."""
        from .rat import RationalFunction

        if isinstance(other, (Variable, int)):
            return RationalFunction(other, self)
        elif isinstance(other, Fraction):
            return RationalFunction(other) / RationalFunction(self)
        return NotImplemented  # type: ignore[unreachable]

    def __pow__(self, other: int) -> Polynomial:
        """Return ``self ** other``."""
        if isinstance(other, int):
            if other <= -1:
                raise ValueError("negative power given for polynomial")
            return Polynomial._new(self._raw.pow(other))
        return NotImplemented  # type: ignore[unreachable]

    def __eq__(self, other: object) -> bool:
        """Return ``self == other``."""
        if isinstance(other, Polynomial):
            return self._raw.equals(other._raw)  # type: ignore[no-any-return]
        elif isinstance(other, (Variable, int)):
            return self == Polynomial(other)
        return NotImplemented

    @property
    def is_zero(self) -> bool:
        """Return `True` if the polynomial is zero."""
        return self._raw.isZero()  # type: ignore[no-any-return]

    @property
    def is_one(self) -> bool:
        """Return `True` if the polynomial is one."""
        return self._raw.isOne()  # type: ignore[no-any-return]

    @property
    def is_minus_one(self) -> bool:
        """Return `True` if the polynomial is minus one."""
        return self._raw.isMinusOne()  # type: ignore[no-any-return]

    @property
    def is_integer(self) -> bool:
        """Return `True` if the polynomial is an integer."""
        return self._raw.isConstant()  # type: ignore[no-any-return]

    @property
    def is_monomial(self) -> bool:
        """Return `True` if the polynomial is monomial."""
        return self._raw.isMonomial()  # type: ignore[no-any-return]

    @property
    def is_monic(self) -> bool:
        """Return `True` if the polynomial is monic."""
        return self._raw.isMonic()  # type: ignore[no-any-return]

    @property
    def is_variable(self) -> bool:
        """Return `True` if the polynomial is a variable."""
        return self._raw.isVariable()  # type: ignore[no-any-return]

    @property
    def as_integer(self) -> int:
        """Cast the polynomial to an integer."""
        if self.is_integer:
            if self._raw.isLongValue():
                return self._raw.asLongValue()  # type: ignore[no-any-return]
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
        return self._raw.signum()  # type: ignore[no-any-return]

    @property
    def variables(self) -> FrozenSet[Variable]:
        """Return the set of variables."""
        return VariableSet._frozenset_from_raw(self._raw.getVariables())

    @property
    def min_variables(self) -> FrozenSet[Variable]:
        """Return the set of actually used variables in this polynomial."""
        return VariableSet._frozenset_from_raw(self._raw.getMinimalVariables())

    @property
    def factors(self) -> Sequence[Polynomial]:
        """Return the factorization of this polynomial."""
        if self._cache_factors is None:
            self._cache_factors = tuple(Polynomial._new(x) for x in self._raw.factors())
        return self._cache_factors

    @overload
    def degree(self) -> int:
        """Return the total degree."""
        ...

    @overload
    def degree(self, *variables: VariableLike) -> int:
        """Return the degree with respect to the given variables."""
        ...

    @overload
    def degree(self, variables: VariableSetLike) -> int:
        """Return the degree with respect to the given variables."""
        ...

    def degree(self, *variables) -> int:  # type: ignore[misc,no-untyped-def]
        """Return the degree with respect to the specified variables."""
        if len(variables) == 0:
            # Return the total degree.
            return self._raw.degree()  # type: ignore[no-any-return]

        if len(variables) == 1:
            x = variables[0]
            if isinstance(x, Variable):
                return self._raw.degree(x._raw)  # type: ignore[no-any-return]
            if isinstance(x, VariableSet):
                return self._raw.degree(x._raw)  # type: ignore[no-any-return]
            if isinstance(x, Iterable) and not isinstance(x, str):
                if not x:
                    # None of the variables are specified.
                    return 0
                return self.degree(*x)

        if any(not isinstance(x, (Variable, str)) for x in variables):
            raise TypeError("not Variable")

        return self._raw.degree(  # type: ignore[no-any-return]
            VariableSet._get_raw(variables)
        )

    @overload
    def coeff(self, x: Union[Variable, str], n: int) -> Polynomial:
        """Return the coefficient of ``x^n``."""
        ...

    @overload
    def coeff(
        self, variables: Sequence[Union[Variable, str]], exponents: Sequence[int]
    ) -> Polynomial:
        """Return the coefficient specified by `variables` and `exponents`."""
        ...

    def coeff(  # type: ignore[misc,no-untyped-def]
        self, variables, exponents
    ) -> Polynomial:
        """Return the coefficient specified by `variables` and `exponents`."""
        # TODO: integer overflow occurs >= 2^31.

        if isinstance(variables, Sequence) and not isinstance(variables, str):
            if not (isinstance(exponents, Sequence) and not isinstance(exponents, str)):
                raise TypeError("exponents must be a sequence")
            if len(variables) != len(exponents):
                raise ValueError("variables and exponents have different sizes")
            return Polynomial._new(
                self._raw.coefficientOf(
                    _create_raw_var_array(tuple(variables)),
                    _create_raw_int_array(tuple(exponents)),
                )
            )

        x = variables
        n = exponents
        if isinstance(x, str):
            x = Variable(x)
        if isinstance(x, Variable):
            if not isinstance(n, int):
                raise TypeError("exponent must be an integer")
            return Polynomial._new(self._raw.coefficientOf(x._raw, n))

        raise TypeError("invalid variables")

    @overload
    def coeff_dict(
        self, *variables: Union[Variable, str]
    ) -> Dict[Sequence[int], Polynomial]:
        """Cast this polynomial to a map from exponents to coefficients."""
        ...

    @overload
    def coeff_dict(
        self, variables: Iterable[Union[Variable, str]]
    ) -> Dict[Sequence[int], Polynomial]:
        """Cast this polynomial to a map from exponents to coefficients."""
        ...

    def coeff_dict(  # type: ignore[misc,no-untyped-def]
        self, *variables
    ) -> Dict[Sequence[int], Polynomial]:
        """Cast this polynomial to a map from exponents to coefficients."""
        array = _create_raw_var_array(variables)
        it = _RawPythonUtils.getCoefficientMap(self._raw, array).entrySet().iterator()
        result: Dict[Sequence[int], Polynomial] = {}
        while it.hasNext():
            entry = it.next()  # noqa: B305
            exponents = tuple(entry.getKey())
            coefficient = Polynomial._new(entry.getValue())
            result[exponents] = coefficient
        return result

    @overload
    def translate(self, *variables: VariableLike) -> Polynomial:
        """Translate the polynomial in terms of the given set of variables."""
        ...

    @overload
    def translate(self, variables: VariableSetLike) -> Polynomial:
        """Translate the polynomial in terms of the given set of variables."""
        ...

    def translate(self, *variables) -> Polynomial:  # type: ignore[misc,no-untyped-def]
        """Translate the polynomial in terms of the given set of variables."""
        if len(variables) == 1:
            xx = variables[0]
            if isinstance(xx, VariableSet):
                return self._translate_impl(xx._raw)
            elif isinstance(xx, Iterable) and not isinstance(xx, str):
                return self.translate(*xx)

        if any(not isinstance(x, (Variable, str)) for x in variables):
            raise TypeError("not Variable")

        return self._translate_impl(VariableSet._get_raw(variables))

    def _translate_impl(self, raw_varset: Any) -> Polynomial:
        try:
            raw = self._raw.translate(raw_varset)
        except _JavaError as e:
            raise ValueError("invalid set of variables") from e
        return Polynomial._new(raw)

    def divide_exact(self, other: Union[Polynomial, Variable, int]) -> Polynomial:
        """Return ```self / other``` if divisible."""
        if isinstance(other, (Variable, int)):
            return self.divide_exact(Polynomial(other))
        if not isinstance(other, Polynomial):
            raise TypeError("other must be a Polynomial")
        try:
            return Polynomial._new(self._raw.divideExact(other._raw))
        except _JavaError as e:
            error = jvm.get_error_message(e)
            if error == "divide by zero":
                raise ZeroDivisionError("division by zero") from e
            elif error.startswith("not divisible"):
                raise ValueError("not divisible") from e
            raise e  # pragma: no cover

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

    @overload
    def evaluate(self, variable: Union[Variable, str], value: int) -> Polynomial:
        """Return the result of setting the given variable to the specified value."""
        ...

    @overload
    def evaluate(
        self, variables: Sequence[Union[Variable, str]], values: Sequence[int]
    ) -> Polynomial:
        """Return the result of setting the given variables to the specified values."""
        ...

    def evaluate(  # type: ignore[misc,no-untyped-def]
        self, variables, values
    ) -> Polynomial:
        """Return the result of setting the given variables to the specified values."""
        # TODO: integer overflow occurs >= 2^31.

        if isinstance(variables, Sequence) and not isinstance(variables, str):
            if not (isinstance(values, Sequence) and not isinstance(values, str)):
                raise TypeError("values must be a sequence")
            if len(variables) != len(values):
                raise ValueError("variables and values have different sizes")
            return Polynomial._new(
                self._raw.evaluate(
                    _create_raw_var_array(tuple(variables)),
                    _create_raw_int_array(tuple(values)),
                )
            )

        if isinstance(variables, Variable):
            x = variables
            if not isinstance(values, int):
                raise TypeError("value must be an integer")
            n = values
            return Polynomial._new(self._raw.evaluate(x._raw, n))

        if isinstance(variables, str):
            return self.evaluate(Variable(variables), values)

        raise TypeError("invalid variables")

    @overload
    def evaluate_at_zero(self, *variables: VariableLike) -> Polynomial:
        """Return the result of setting all the given variables to zero."""
        ...

    @overload
    def evaluate_at_zero(self, variables: VariableSetLike) -> Polynomial:
        """Return the result of setting all the given variables to zero."""
        ...

    def evaluate_at_zero(  # type: ignore[misc,no-untyped-def]
        self, *variables
    ) -> Polynomial:
        """Return the result of setting all the given variables to zero."""
        if len(variables) == 1:
            x = variables[0]
            if isinstance(x, (Variable, VariableSet)):
                return Polynomial._new(self._raw.evaluateAtZero(x._raw))
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
    def evaluate_at_one(self, *variables: VariableLike) -> Polynomial:
        """Return the result of setting all the given variables to unity."""
        ...

    @overload
    def evaluate_at_one(self, variables: VariableSetLike) -> Polynomial:
        """Return the result of setting all the given variables to unity."""
        ...

    def evaluate_at_one(  # type: ignore[misc,no-untyped-def]
        self, *variables
    ) -> Polynomial:
        """Return the result of setting all the given variables to unity."""
        if len(variables) == 1:
            x = variables[0]
            if isinstance(x, (Variable, VariableSet)):
                return Polynomial._new(self._raw.evaluateAtOne(x._raw))
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
    def shift(self, variable: Union[Variable, str], shift: int) -> Polynomial:
        """Return the result of the given variable shift."""
        ...

    @overload
    def shift(
        self, variables: Sequence[Union[Variable, str]], values: Sequence[int]
    ) -> Polynomial:
        """Return the result of the given variable shifts."""
        ...

    def shift(  # type: ignore[misc,no-untyped-def]
        self, variables, values
    ) -> Polynomial:
        """Return the result of the given variable shifts."""
        # TODO: integer overflow occurs >= 2^31.

        if isinstance(variables, Sequence) and not isinstance(variables, str):
            if not (isinstance(values, Sequence) and not isinstance(values, str)):
                raise TypeError("values must be a sequence")
            if len(variables) != len(values):
                raise ValueError("variables and values have different sizes")
            return Polynomial._new(
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
            return Polynomial._new(self._raw.shift(x._raw, n))

        if isinstance(variables, str):
            return self.shift(Variable(variables), values)

        raise TypeError("invalid variables")

    def diff(self, x: Union[Variable, str], n: int = 1) -> Polynomial:
        """Differentiate this polynomial."""
        if isinstance(x, str):
            x = Variable(x)

        if not isinstance(x, Variable):
            raise TypeError("x must be a Variable")
        if not isinstance(n, int):
            raise TypeError("n must be an int")
        if n < 0:
            raise ValueError("n must be non-negative")

        return Polynomial._new(self._raw.derivative(x._raw, n))


@overload  # noqa: A001
def sum(*polynomials: Union[Polynomial, Variable, int]) -> Polynomial:  # noqa: A001
    """Return the sum of the given polynomials."""
    ...


@overload  # noqa: A001
def sum(  # noqa: A001
    polynomials: Iterable[Union[Polynomial, Variable, int]]
) -> Polynomial:
    """Return the sum of the given polynomials."""
    ...


def sum(*polynomials) -> Polynomial:  # type: ignore[misc,no-untyped-def]  # noqa: A001
    """Return the sum of the given polynomials."""
    array = _create_raw_poly_array(polynomials)
    return Polynomial._new(_RawPythonUtils.sumOf(array))


@overload
def product(*polynomials: Union[Polynomial, Variable, int]) -> Polynomial:
    """Return the product of the given polynomials."""
    ...


@overload
def product(polynomials: Iterable[Union[Polynomial, Variable, int]]) -> Polynomial:
    """Return the product of the given polynomials."""
    ...


def product(*polynomials) -> Polynomial:  # type: ignore[misc,no-untyped-def]
    """Return the product of the given polynomials."""
    array = _create_raw_poly_array(polynomials)
    return Polynomial._new(_RawPythonUtils.productOf(array))


@overload
def gcd(*polynomials: Union[Polynomial, Variable, int]) -> Polynomial:
    """Return the GCD of the given polynomials."""
    ...


@overload
def gcd(polynomials: Iterable[Union[Polynomial, Variable, int]]) -> Polynomial:
    """Return the GCD of the given polynomials."""
    ...


def gcd(*polynomials) -> Polynomial:  # type: ignore[misc,no-untyped-def]
    """Return the GCD of the given polynomials."""
    array = _create_raw_poly_array(polynomials)
    return Polynomial._new(_RawPythonUtils.gcdOf(array))


@overload
def lcm(*polynomials: Union[Polynomial, Variable, int]) -> Polynomial:
    """Return the LCM of the given polynomials."""
    ...


@overload
def lcm(polynomials: Iterable[Union[Polynomial, Variable, int]]) -> Polynomial:
    """Return the LCM of the given polynomials."""
    ...


def lcm(*polynomials) -> Polynomial:  # type: ignore[misc,no-untyped-def]
    """Return the LCM of the given polynomials."""
    array = _create_raw_poly_array(polynomials)
    if len(polynomials) == 0:
        raise ValueError("lcm with no arguments")
    return Polynomial._new(_RawPythonUtils.lcmOf(array))


# For static typing.
PolynomialLike = Union[Polynomial, Variable, int]
