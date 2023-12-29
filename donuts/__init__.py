"""Python binding to the Donuts wrapper for the Rings library."""

__version__ = "0.0.3"

from .poly import Polynomial, gcd, lcm, product
from .rat import RationalFunction
from .var import Variable

# NOTE: we do not add the "sum" function intentionally because it shadows
#       the built-in function.
__all__ = (
    "Polynomial",
    "RationalFunction",
    "Variable",
    "gcd",
    "lcm",
    "product",
)

# The following attributes are explicitly re-exported for mypy with
# `--no-implicit-reexport`.

# isort: off

from .poly import PolynomialLike as PolynomialLike  # noqa: F401
from .poly import sum as sum  # noqa: A004,F401
from .rat import RationalFunctionLike as RationalFunctionLike  # noqa: F401
from .var import VariableLike as VariableLike  # noqa: F401
from .varset import VariableSet as VariableSet  # noqa: F401
from .varset import VariableSetLike as VariableSetLike  # noqa: F401
