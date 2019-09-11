"""Routines for variables."""

from __future__ import annotations

from typing import Any

from .jvm import jvm

_RawVariable = jvm.find_class("com.github.tueda.donuts.Variable")
_JavaError = jvm.java_error_class


class Variable:
    """Variable."""

    __slots__ = ("_name", "_raw")

    __NONE = "[__PRIVATE_NONE__]"

    def __init__(self, name: str) -> None:
        """Construct a variable."""
        if name == Variable.__NONE:
            # Called from `_new`.
            return

        if not isinstance(name, str):
            raise TypeError(f"invalid argument for variable: `{name}`")

        try:
            self._raw = _RawVariable(name)
        except _JavaError as e:
            raise ValueError(f"invalid string for variable: `{name}'") from e

        self._name = name

    @staticmethod
    def _new(raw: Any) -> Variable:
        """Construct a variable from a raw object."""
        obj = Variable(Variable.__NONE)
        obj._raw = raw
        obj._name = raw.getName()
        return obj

    def __getstate__(self) -> Any:
        """Get the object state."""
        return self._name

    def __setstate__(self, state: Any) -> None:
        """Set the object state."""
        self._name = state
        self._raw = _RawVariable(state)

    def __str__(self) -> str:
        """Return the string representation."""
        return self._name

    def __repr__(self) -> str:
        """Return the "official" string representation."""
        return f"Variable('{self._name}')"

    def __hash__(self) -> int:
        """Return the hash code."""
        return hash(self._name)

    def __eq__(self, other: object) -> bool:
        """Return ``self == other``."""
        if isinstance(other, Variable):
            return self._name == other._name
        return NotImplemented

    def __le__(self, other: object) -> bool:
        """Return `self <= other`."""
        if isinstance(other, Variable):
            return self._raw.compareTo(other._raw) <= 0  # type: ignore
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        """Return `self < other`."""
        if isinstance(other, Variable):
            return self._raw.compareTo(other._raw) < 0  # type: ignore
        return NotImplemented
