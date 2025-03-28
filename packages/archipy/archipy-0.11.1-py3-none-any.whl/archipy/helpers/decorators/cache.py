from collections.abc import Callable
from functools import wraps
from typing import TypeVar

from cachetools import TTLCache

T = TypeVar("T")
R = TypeVar("R")


def ttl_cache_decorator(ttl_seconds: int = 300, maxsize: int = 100):
    """Decorator that provides a TTL cache for methods.

    Args:
        ttl_seconds: Time to live in seconds (default: 5 minutes)
        maxsize: Maximum size of the cache (default: 100)

    Returns:
        Decorated function with TTL caching
    """
    cache = TTLCache(maxsize=maxsize, ttl=ttl_seconds)

    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a key based on function name, args, and kwargs
            key_parts = [func.__name__]
            key_parts.extend(str(arg) for arg in args[1:])  # Skip self
            key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
            key = ":".join(key_parts)

            # Check if result is in cache
            if key in cache:
                return cache[key]

            # Call the function and cache the result
            result = func(*args, **kwargs)
            cache[key] = result
            return result

        # Add a method to clear the cache
        def clear_cache():
            cache.clear()

        wrapper.clear_cache = clear_cache
        return wrapper

    return decorator
