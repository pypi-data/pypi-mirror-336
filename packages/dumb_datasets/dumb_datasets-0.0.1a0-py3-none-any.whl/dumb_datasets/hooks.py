"""hooks module for dumb-datasets.

provides a mechanism to register and run hook functions.
"""

from typing import Callable, List, Dict, Any

_hooks: Dict[str, List[Callable[..., Any]]] = {}


def add_hook(event: str, hook: Callable[..., Any]) -> None:
    """register a hook for a given event."""
    _hooks.setdefault(event, []).append(hook)


def run_hooks(event: str, *args: Any, **kwargs: Any) -> None:
    """execute all hooks registered for the given event."""
    for hook in _hooks.get(event, []):
        hook(*args, **kwargs)