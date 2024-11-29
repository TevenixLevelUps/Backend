import os
import time

from dotenv import load_dotenv
from fastapi import HTTPException, Request, status
from redis.asyncio import Redis

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

try:
    redis_port = int(REDIS_PORT) if REDIS_PORT is not None else 6379
except ValueError:
    raise ValueError(f"Invalid REDIS_PORT value: {REDIS_PORT}")

redis_client = Redis(host=f"{DB_HOST}", port=redis_port, db=0)


async def rate_limit(request: Request, calls: int, period: int):
    ip = request.client.host
    key = f"rate_limit:{ip}"

    current_count = await redis_client.get(key)

    if current_count is None:

        await redis_client.setex(key, period, 1)
    else:
        current_count = int(current_count)

        if current_count >= calls:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too Many Requests",
            )

        await redis_client.incr(key)
