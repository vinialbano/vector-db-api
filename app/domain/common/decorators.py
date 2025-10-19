from functools import wraps
from typing import Any, Callable


def refresh_timestamp_after(fn: Callable) -> Callable:
    """Decorator that refreshes the aggregate's metadata timestamp after mutation.

    It looks for a `_refresh_timestamp` method on the instance and calls it
    if present.
    """

    @wraps(fn)
    def wrapper(self, *args, **kwargs) -> Any:
        result = fn(self, *args, **kwargs)
        touch = getattr(self, "_refresh_timestamp", None)
        if callable(touch):
            touch()
        return result

    return wrapper
