"""Routines for sets of variables."""

from __future__ import annotations

from typing import Any, Collection, Iterator, Union

from .jvm import jvm
from .var import Variable as Variable  # explicitly re-export for mypy

_RawVariableSet = jvm.find_class("com.github.tueda.donuts.VariableSet")
_JavaError = jvm.java_error_class


class VariableSet:
    """Variable set."""

    __slots__ = "_raw"

    __NONE = Variable("PRIVATENONE")

    __RAW_EMPTY = _RawVariableSet()

    def __init__(self, *variables: Union[Variable, str]) -> None:
        """Construct a set of variables."""
        if len(variables) == 1:
            if variables[0] == VariableSet.__NONE:
                # Called from `_new`.
                return

        if len(variables) == 0:
            self._raw = VariableSet.__RAW_EMPTY
            return

        raw = _RawVariableSet()
        for x in variables:
            if isinstance(x, str):
                x = Variable(x)
            if not isinstance(x, Variable):
                raise TypeError("not a Variable")
            # Somehow the following line doesn't work with pyjnius 1.2.1.
            # Use a temporary variable.
            # raw = raw.union(_RawVariableSet(x._raw))
            raw1 = _RawVariableSet(x._raw)
            raw = raw.union(raw1)
        self._raw = raw

    @staticmethod
    def _new(raw: Any) -> VariableSet:
        """Construct a set of variables from a raw object."""
        obj = VariableSet(VariableSet.__NONE)
        obj._raw = raw
        return obj

    def __getstate__(self) -> Any:
        """Get the object state."""
        return jvm.serialize(self._raw)

    def __setstate__(self, state: Any) -> None:
        """Set the object state."""
        self._raw = jvm.deserialize(state)

    def __str__(self) -> str:
        """Return the string representation."""
        return self._raw.toString()  # type: ignore

    def __repr__(self) -> str:
        """Return the "official" string representation."""
        it = self._raw.iterator()
        xx = []
        while it.hasNext():
            xx.append(it.next().getName())
        variables = ", ".join(f"Variable('{x}')" for x in xx)
        return f"VariableSet({variables})"

    def __hash__(self) -> int:
        """Return the hash code."""
        return self._raw.hashCode()  # type: ignore

    def __len__(self) -> int:
        """Return the number of variables in this set."""
        return self._raw.size()  # type: ignore

    def __iter__(self) -> Iterator[Variable]:
        """Return an iterator to iterate variables in this set."""
        raw_it = self._raw.iterator()
        while raw_it.hasNext():
            yield Variable._new(raw_it.next())  # noqa: B305

    def __contains__(self, item: object) -> bool:
        """Return `True` if the set contains the given variable."""
        if isinstance(item, Variable):
            return self._raw.contains(item._raw)  # type: ignore
        return False

    def __eq__(self, other: object) -> bool:
        """Return ``self == other``."""
        if isinstance(other, VariableSet):
            return self._raw.equals(other._raw)  # type: ignore
        return NotImplemented

    def union(self, other: VariableSet) -> VariableSet:
        """Return the union of this set and the other."""
        if not isinstance(other, VariableSet):
            raise TypeError("not set of variables")
        return VariableSet._new(self._raw.union(other._raw))


# For static typing.
VariableSetLike = Union[VariableSet, Collection[Variable]]
