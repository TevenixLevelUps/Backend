import json
from uuid import UUID

import aio_pika
from aio_pika.abc import AbstractChannel
from fastapi import HTTPException

from app.logger import logger
from app.rabbit import get_rabbit_connection


class ServicesRabbit:
    @classmethod
    async def send_request_for_get_service_by_id(cls, service_id: UUID) -> dict:
        connection = await get_rabbit_connection()
        async with connection:
            channel = await connection.channel()

            body = {
                "service_id": str(service_id),
            }
            message_body = json.dumps(body).encode()

            await channel.default_exchange.publish(
                aio_pika.Message(body=message_body),
                routing_key="request_service_by_id",
            )
            return await cls.__get_response_for_get_service_by_id(channel)

    @staticmethod
    async def __get_response_for_get_service_by_id(channel: AbstractChannel) -> dict:
            queue = await channel.declare_queue("response_service_by_id", auto_delete=True)

            async for message in queue:
                async with message.process():
                    service = json.loads(message.body)

                    logger.info(f"Received message: {service}")

                    return service

    @classmethod
    async def send_request_for_get_service_by_title(cls, service_title: str) -> dict:
        connection = await get_rabbit_connection()
        async with connection:
            channel = await connection.channel()

            body = {
                "service_title": service_title,
            }
            message_body = json.dumps(body).encode()

            await channel.default_exchange.publish(
                aio_pika.Message(body=message_body),
                routing_key="request_service_by_title",
            )
            return await cls.__get_response_for_get_service_by_title(channel)

    @staticmethod
    async def __get_response_for_get_service_by_title(channel: AbstractChannel) -> dict:
            queue = await channel.declare_queue("response_service_by_title", auto_delete=True)

            async for message in queue:
                async with message.process():
                    service = json.loads(message.body)

                    logger.info(f"Received message: {service}")

                    if service.get("status_code"):
                        raise HTTPException(
                            status_code=service.get("status_code"),
                            detail=service.get("detail"),
                        )

                    return service
