import json
from uuid import UUID

import aio_pika
from aio_pika.abc import AbstractChannel
from fastapi import HTTPException

from app.rabbit import get_rabbit_connection
from app.logger import logger


class SpecialistsRabbit:
    @classmethod
    async def send_request_for_get_specialist_by_name(cls, name: str) -> dict:
        connection = await get_rabbit_connection()
        async with connection:
            channel = await connection.channel()

            body = {
                "specialist_name": name,
            }
            message_body = json.dumps(body).encode()

            await channel.default_exchange.publish(
                aio_pika.Message(body=message_body),
                routing_key="request_specialist_by_name",
            )
            return await cls.__get_response_for_get_specialist_by_name(channel)

    @staticmethod
    async def __get_response_for_get_specialist_by_name(channel: AbstractChannel) -> dict:
            queue = await channel.declare_queue("response_specialist_by_name", auto_delete=True)

            async for message in queue:
                async with message.process():
                    specialist = json.loads(message.body)

                    logger.info(f"Received message: {specialist}")

                    if specialist.get("status_code"):
                        raise HTTPException(
                            status_code=specialist.get("status_code"),
                            detail=specialist.get("detail"),
                        )
                    
                    return specialist

    @classmethod
    async def send_request_for_get_specialist_by_id(cls, specialist_id: UUID) -> dict:
        connection = await get_rabbit_connection()
        async with connection:
            channel = await connection.channel()

            body = {
                "specialist_id": str(specialist_id),
            }
            message_body = json.dumps(body).encode()

            await channel.default_exchange.publish(
                aio_pika.Message(body=message_body),
                routing_key="request_specialist_by_id",
            )
            return await cls.__get_response_for_get_specialist_by_id(channel)

    @staticmethod
    async def __get_response_for_get_specialist_by_id(channel: AbstractChannel) -> dict:
            queue = await channel.declare_queue("response_specialist_by_id", auto_delete=True)

            async for message in queue:
                async with message.process():
                    specialist = json.loads(message.body)

                    logger.info(f"Received message: {specialist}")

                    if specialist.get("status_code"):
                        raise HTTPException(
                            status_code=specialist.get("status_code"),
                            detail=specialist.get("detail"),
                        )


                    return specialist
