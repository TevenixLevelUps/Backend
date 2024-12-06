import json

import aio_pika
from aio_pika.abc import AbstractChannel

from app.database import async_session_maker
from app.logger import logger
from app.rabbit import get_rabbit_connection
from app.services.dao import ServicesDAO


class ServicesRabbit:
    @classmethod
    async def consume_find_service_by_id_message(cls):
        connection = await get_rabbit_connection()
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue("request_service_by_id", auto_delete=True)

            async for message in queue:
                async with message.process():
                    service_id = json.loads(message.body).get("service_id")

                    await cls.__send_service_for_find_service_by_id_request(service_id, channel)

                    logger.info(f"Received message: {json.loads(message.body)}")

    @staticmethod
    async def __send_service_for_find_service_by_id_request(
            service_id: str,
            channel: AbstractChannel,
        ) -> None:
        try:
            async with async_session_maker() as session:
                service = await ServicesDAO.find_one_or_none(session, id=service_id)
                await session.commit()

            body = {
                "id": str(service.id),
                "title": service.title,
                "description": service.description,
                "price": float(service.price),
                "lead_time": service.lead_time.strftime("%H:%M:%S"),
                "image_id": service.image_id
            }
        except Exception as e:
            body = {
                "status_code": e.status_code,
                "detail": e.detail,
            }

        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(body).encode()),
            routing_key="response_service_by_id"
        )

    @classmethod
    async def consume_find_service_by_title_message(cls):
        connection = await get_rabbit_connection()
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue("request_service_by_title", auto_delete=True)

            async for message in queue:
                async with message.process():
                    service_title = json.loads(message.body).get("service_title")

                    await cls.__send_service_for_find_service_by_title_request(service_title, channel)

                    logger.info(f"Received message: {json.loads(message.body)}")

    @staticmethod
    async def __send_service_for_find_service_by_title_request(
            service_title: str,
            channel: AbstractChannel,
        ) -> None:
        try:
            async with async_session_maker() as session:
                service = await ServicesDAO.find_service_by_title(session, service_title)
                await session.commit()

            body = {
                "id": str(service.id),
                "title": service.title,
                "description": service.description,
                "price": float(service.price),
                "lead_time": service.lead_time.strftime("%H:%M:%S"),
                "image_id": service.image_id
            }
        except Exception as e:
            body = {
                "status_code": e.status_code,
                "detail": e.detail,
            }

        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(body).encode()),
            routing_key="response_service_by_title"
        )
