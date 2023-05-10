"""Routines for variables."""

from __future__ import annotations

import functools
from typing import TYPE_CHECKING, Any, Union, overload

from .jvm import jvm

if TYPE_CHECKING:
    from .poly import Polynomial
    from .rat import RationalFunction

_RawVariable = jvm.find_class("com.github.tueda.donuts.Variable")
_JavaError = jvm.java_error_class


@functools.lru_cache(maxsize=1024)
def _raw_variable_from_str(name: str) -> Any:
    return _RawVariable(name)


class Variable:
    """Variable."""

    __slots__ = ("_name", "_raw")

    __NONE = "[__PRIVATE_NONE__]"

    @overload
    def __init__(self, name: str) -> None:
        """Construct a variable."""
        ...

    @overload
    def __init__(self, variable: Variable) -> None:
        """Construct a variable."""
        ...

    def __init__(self, variable: Union[Variable, str]) -> None:  # type: ignore[misc]
        """Construct a variable."""
        if variable == Variable.__NONE:
            # Called from `_new`.
            return

        if isinstance(variable, Variable):
            self._name: str = variable._name
            self._raw: Any = variable._raw
            return

        if not isinstance(variable, str):
            raise TypeError(f"invalid argument for variable: `{variable}`")

        try:
            self._raw = _raw_variable_from_str(variable)
        except _JavaError as e:
            raise ValueError(f"invalid string for variable: `{variable}'") from e

        self._name = variable

    @staticmethod
    def _new(raw: Any) -> Variable:
        """Construct a variable from a raw object."""
        obj = Variable(Variable.__NONE)
        obj._raw = raw
        obj._name = str(raw.getName())
        return obj

    def __getstate__(self) -> Any:
        """Get the object state."""
        return self._name

    def __setstate__(self, state: Any) -> None:
        """Set the object state."""
        self._name = state
        self._raw = _raw_variable_from_str(state)

    def __str__(self) -> str:
        """Return the string representation."""
        return self._name

    def __repr__(self) -> str:
        """Return the "official" string representation."""
        return f"Variable('{self._name}')"

    def __hash__(self) -> int:
        """Return the hash code."""
        return hash(self._name)

    def __pos__(self) -> Polynomial:
        """Return ``+ self``."""
        from .poly import Polynomial

        return Polynomial(self)

    def __neg__(self) -> Polynomial:
        """Return ``- self``."""
        from .poly import Polynomial

        return -Polynomial(self)

    def __add__(self, other: Union[Variable, int]) -> Polynomial:
        """Return ``self + other``."""
        from .poly import Polynomial

        if isinstance(other, (Variable, int)):
            return Polynomial(self) + Polynomial(other)
        return NotImplemented  # type: ignore[unreachable]

    def __radd__(self, other: int) -> Polynomial:
        """Return ``other + self."""
        from .poly import Polynomial

        if isinstance(other, int):
            return Polynomial(other) + Polynomial(self)
        return NotImplemented  # type: ignore[unreachable]

    def __sub__(self, other: Union[Variable, int]) -> Polynomial:
        """Return ``self - other``."""
        from .poly import Polynomial

        if isinstance(other, (Variable, int)):
            return Polynomial(self) - Polynomial(other)
        return NotImplemented  # type: ignore[unreachable]

    def __rsub__(self, other: int) -> Polynomial:
        """Return ``other - self."""
        from .poly import Polynomial

        if isinstance(other, int):
            return Polynomial(other) - Polynomial(self)
        return NotImplemented  # type: ignore[unreachable]

    def __mul__(self, other: Union[Variable, int]) -> Polynomial:
        """Return ``self * other``."""
        from .poly import Polynomial

        if isinstance(other, (Variable, int)):
            return Polynomial(self) * Polynomial(other)
        return NotImplemented  # type: ignore[unreachable]

    def __rmul__(self, other: int) -> Polynomial:
        """Return ``other * self."""
        from .poly import Polynomial

        if isinstance(other, int):
            return Polynomial(other) * Polynomial(self)
        return NotImplemented  # type: ignore[unreachable]

    def __truediv__(self, other: Union[Variable, int]) -> RationalFunction:
        """Return ``self / other``."""
        from .rat import RationalFunction

        if isinstance(other, (Variable, int)):
            return RationalFunction(self, other)
        return NotImplemented  # type: ignore[unreachable]

    def __rtruediv__(self, other: int) -> RationalFunction:
        """Return ``other / self``."""
        from .rat import RationalFunction

        if isinstance(other, int):
            return RationalFunction(other, self)
        return NotImplemented  # type: ignore[unreachable]

    def __pow__(self, other: int) -> Polynomial:
        """Return ``self ** other``."""
        from .poly import Polynomial

        if isinstance(other, int):
            return Polynomial(self) ** other
        return NotImplemented  # type: ignore[unreachable]

    def __eq__(self, other: object) -> bool:
        """Return ``self == other``."""
        if isinstance(other, Variable):
            return self._name == other._name
        return NotImplemented

    def __le__(self, other: object) -> bool:
        """Return `self <= other`."""
        if isinstance(other, Variable):
            return self._raw.compareTo(other._raw) <= 0  # type: ignore[no-any-return]
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        """Return `self < other`."""
        if isinstance(other, Variable):
            return self._raw.compareTo(other._raw) < 0  # type: ignore[no-any-return]
        return NotImplemented


# For static typing.
VariableLike = Union[Variable, str]
