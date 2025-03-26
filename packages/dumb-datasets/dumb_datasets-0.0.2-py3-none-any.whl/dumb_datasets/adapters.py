"""adapters module for dumb-datasets.

defines an adapter architecture for loading datasets from different sources.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional

_registry: Dict[str, Callable[..., Any]] = {}


def register_adapter(name: str, adapter: Callable[..., Any]) -> None:
    """register an adapter for a given name."""
    _registry[name] = adapter


def get_adapter(name: str) -> Optional[Callable[..., Any]]:
    """get the adapter for a given name."""
    return _registry.get(name)
