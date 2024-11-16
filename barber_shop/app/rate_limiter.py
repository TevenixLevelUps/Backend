from datetime import timedelta, timezone, datetime
import hashlib
from fastapi.responses import JSONResponse
from redis import asyncio as aioredis
from fastapi import status

from app.config import settings


redis_client = aioredis.from_url(
    f"redis://{settings.redis.host}:{settings.redis.port}",
    encoding="utf-8",
    decode_responses=True,
)
 

async def rate_limit_user(user: str, rate_limit: int) -> JSONResponse | None:
    username_hash = hashlib.sha256(bytes(user, "utf-8")).hexdigest()
    now = datetime.now(timezone.utc)
    current_minute = now.strftime("%Y-%m-%dT%H:%M")

    redis_key = f"rate_limit_{username_hash}_{current_minute}"
    current_count = await redis_client.incr(redis_key)

    if current_count == 1:
        await redis_client.expireat(name=redis_key, when=now + timedelta(minutes=1))

    if current_count > rate_limit:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "User Rate Limit Exceeded"},
            headers={
                "Retry-After": f"{60 - now.second}",
                "X-Rate-Limit": f"{rate_limit}",
            },
        )

    return None