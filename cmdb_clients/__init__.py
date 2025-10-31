"""Compatibility shim for the package renamed to `one_clients`.

This module re-exports public names from `one_clients` to preserve
backwards-compatibility for code that still imports `cmdb_clients`.
"""
import warnings

warnings.warn(
    "`cmdb_clients` package is deprecated; use `one_clients` instead",
    DeprecationWarning,
)

import one_clients as _one_clients
from one_clients import *  # noqa: F401,F403

__all__ = getattr(_one_clients, '__all__', None) or []
