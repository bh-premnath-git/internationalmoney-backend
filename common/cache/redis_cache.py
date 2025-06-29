import functools
import json
import os

import redis.asyncio as redis

_REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
_redis = redis.from_url(_REDIS_URL, decode_responses=True)


def cache(ttl: int = 60):
    """
    Decorator that caches async function results in Redis.

    Example:
        @cache(ttl=120)
        async def get_user(uid: str): ...
    """

    def decorator(fn):
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            key = f"{fn.__module__}.{fn.__name__}:{hash(frozenset(kwargs.items()))}"
            if (cached := await _redis.get(key)) is not None:
                return json.loads(cached)

            result = await fn(*args, **kwargs)
            # NB: json.dumps will call __str__ on non-serialisable objects.
            await _redis.set(key, json.dumps(result, default=str), ex=ttl)
            return result

        return wrapper

    return decorator


async def invalidate(pattern: str):
    """Delete keys matching a redis pattern (e.g. 'user_service.*')."""
    async for key in _redis.scan_iter(match=pattern):
        await _redis.delete(key)
