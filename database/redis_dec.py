import json
from functools import wraps

from .redis_config import redis_client

def cache_red(model_class, expiry: int = 660):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{':'.join(map(str, args))}"
            cached_data =  await redis_client.get(cache_key)

            if cached_data:
                result_data = await json.loads(cached_data)

                if isinstance(result_data, list):
                    return [model_class(**item) for item in result_data]
                return model_class(**result_data)

            result = await func(*args, **kwargs)

            if isinstance(result, list):
                await redis_client.set(cache_key, json.dumps([item.model_dump() for item in result]), ex=expiry)
            else:
                await redis_client.set(cache_key, json.dumps(result.model_dump()), ex=expiry)

            return result
        return wrapper
    return decorator



def invalidate_cache(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)

        cache_key = f"{func.__name__}:{':'.join(map(str, args))}"

        await invalidate_related_cache(cache_key)

        return result

    async def invalidate_related_cache(cache_key: str):
        keys_to_delete = [key.decode() for key in await redis_client.keys(f"*{cache_key}*")]
        if keys_to_delete:
            await redis_client.delete(*keys_to_delete)

    return wrapper