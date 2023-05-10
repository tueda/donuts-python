"""Routines for sets of variables."""

from __future__ import annotations

import functools
from typing import (
    AbstractSet,
    Any,
    Collection,
    FrozenSet,
    Iterable,
    Iterator,
    Union,
    overload,
)

from .array import _create_raw_var_array
from .jvm import jvm
from .var import Variable, VariableLike

_RawVariableSet = jvm.find_class("com.github.tueda.donuts.VariableSet")
_RawPythonUtils = jvm.find_class("com.github.tueda.donuts.python.PythonUtils")


@functools.lru_cache(maxsize=1024)
def _raw_variable_set_from_frozenset(variables: FrozenSet[VariableLike]) -> Any:
    return _RawPythonUtils.variableSet(_create_raw_var_array(tuple(variables)))


class VariableSet(AbstractSet[Variable]):
    """Variable set."""

    __slots__ = "_raw"

    __NONE = "[__PRIVATE_NONE__]"

    __RAW_EMPTY = _RawVariableSet()

    @overload
    def __init__(self) -> None:
        """Construct an empty set of variables."""
        ...

    @overload
    def __init__(self, variables: VariableSet) -> None:
        """Construct a set of variables from the given set."""
        ...

    @overload
    def __init__(self, variable: Union[Variable, str]) -> None:
        """Construct a set of variables containing only the given variable."""
        ...

    @overload
    def __init__(self, *variables: Union[Variable, str]) -> None:
        """Construct a set of variables from the given variables."""
        ...

    @overload
    def __init__(self, variables: Iterable[Union[Variable, str]]) -> None:
        """Construct a set of variables from the given variables."""
        ...

    def __init__(self, *variables) -> None:  # type: ignore[misc,no-untyped-def]
        """Construct a set of variables."""
        if len(variables) == 0:
            self._raw = VariableSet.__RAW_EMPTY
            return

        if len(variables) == 1:
            v = variables[0]
            if v == VariableSet.__NONE:
                # Called from `_new`.
                return

            if isinstance(v, VariableSet):
                self._raw = v._raw
                return

            if isinstance(v, Iterable) and not isinstance(v, str):
                variables = v  # type: ignore[assignment]

        self._raw = _raw_variable_set_from_frozenset(frozenset(variables))

    @staticmethod
    def _new(raw: Any) -> VariableSet:
        """Construct a set of variables from a raw `VariableSet` object."""
        obj = VariableSet(VariableSet.__NONE)
        obj._raw = raw
        return obj

    @staticmethod
    def _frozenset_from_raw(raw: Any) -> FrozenSet[Variable]:
        """Construct a frozen set of variables from a raw `VariableSet` object."""
        return frozenset(x for x in VariableSet._new(raw))

    @staticmethod
    def _get_raw(variables: Iterable[Union[Variable, str]]) -> Any:
        if isinstance(variables, Collection) and len(variables) == 0:
            VariableSet.__RAW_EMPTY

        return _raw_variable_set_from_frozenset(frozenset(variables))

    def __getstate__(self) -> Any:
        """Get the object state."""
        return jvm.serialize(self._raw)

    def __setstate__(self, state: Any) -> None:
        """Set the object state."""
        self._raw = jvm.deserialize(state)

    def __str__(self) -> str:
        """Return the string representation."""
        return str(self._raw.toString())

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
        return self._raw.hashCode()  # type: ignore[no-any-return]

    def __len__(self) -> int:
        """Return the number of variables in this set."""
        return self._raw.size()  # type: ignore[no-any-return]

    def __iter__(self) -> Iterator[Variable]:
        """Return an iterator to iterate variables in this set."""
        raw_it = self._raw.iterator()
        while raw_it.hasNext():
            yield Variable._new(raw_it.next())  # noqa: B305

    def __contains__(self, item: object) -> bool:
        """Return `True` if the set contains the given variable."""
        if isinstance(item, Variable):
            return self._raw.contains(item._raw)  # type: ignore[no-any-return]
        return False

    def __eq__(self, other: object) -> bool:
        """Return ``self == other``."""
        if isinstance(other, VariableSet):
            return self._raw.equals(other._raw)  # type: ignore[no-any-return]
        if isinstance(other, (set, frozenset)) and all(
            isinstance(x, Variable) for x in other
        ):
            return self == VariableSet(other)
        return NotImplemented

    def union(self, other: VariableSet) -> VariableSet:
        """Return the union of this set and the other."""
        if not isinstance(other, VariableSet):
            raise TypeError("not set of variables")
        return VariableSet._new(self._raw.union(other._raw))


# For static typing.
VariableSetLike = Union[VariableSet, Iterable[Union[Variable, str]]]
