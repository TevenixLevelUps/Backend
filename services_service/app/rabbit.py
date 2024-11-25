import aio_pika
from aio_pika.abc import AbstractRobustConnection

from app.config import settings


async def get_rabbit_connection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(
            f"amqp://{settings.rabbit.user}:{settings.rabbit.password}@{settings.rabbit.host}/"
        )
