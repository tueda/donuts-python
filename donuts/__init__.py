"""Python binding to the Donuts wrapper for the Rings library."""

# TODO: this is a workaround for python/mypy#7042. Remove it in the next mypy release.
from .poly import Polynomial as Polynomial

__all__ = ["Polynomial"]
