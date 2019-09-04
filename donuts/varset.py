"""Routines for sets of variables."""

from __future__ import annotations

from typing import Any, Collection, Iterator, Union

from .jvm import jvm
from .var import Variable as Variable  # explicitly re-export for mypy
from .var import _RawVariable

_RawVariableSet = jvm.find_class("com.github.tueda.donuts.VariableSet")
_JavaError = jvm.java_error_class
_new_array = jvm.new_array


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

        array = _new_array(_RawVariable, len(variables))
        for i, x in enumerate(variables):
            if isinstance(x, str):
                x = Variable(x)
            if not isinstance(x, Variable):
                raise TypeError("not a Variable")
            array[i] = x._raw

        self._raw = _RawVariableSet(array)

    @staticmethod
    def _new(raw: Any) -> VariableSet:
        """Construct a set of variables from a raw object."""
        obj = VariableSet(VariableSet.__NONE)
        obj._raw = raw
        return obj

    def __str__(self) -> str:
        """Return the string representation."""
        # NOTE: somehow str(self._raw) doesn't work.
        return self._raw.toString()  # type: ignore

    def __repr__(self) -> str:
        """Return the "official" string representation."""
        variables = ", ".join(f"Variable('{x.getName()}')" for x in self._raw)
        return f"VariableSet({variables})"

    def __hash__(self) -> int:
        """Return the hash code."""
        return hash(self._raw)

    def __len__(self) -> int:
        """Return the number of variables in this set."""
        return self._raw.size()  # type: ignore

    def __iter__(self) -> Iterator[Variable]:
        """Return an iterator to iterate variables in this set."""
        raw_it = self._raw.iterator()
        while raw_it.hasNext():
            yield Variable._new(next(raw_it))

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
