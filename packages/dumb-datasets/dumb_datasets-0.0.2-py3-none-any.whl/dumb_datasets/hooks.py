"""hooks module for dumb-datasets.

defines a hooks system for extending functionality.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List

_hooks: Dict[str, List[Callable[..., Any]]] = {}


def add_hook(event: str, hook: Callable[..., Any]) -> None:
    """register a hook for a given event."""
    _hooks.setdefault(event, []).append(hook)


def run_hooks(event: str, *args: Any, **kwargs: Any) -> None:
    """execute all hooks registered for the given event."""
    for hook in _hooks.get(event, []):
        hook(*args, **kwargs)
