import json

import aio_pika
from aio_pika.abc import AbstractChannel

from app.database import async_session_maker
from app.exceptions import NoSuchSpecialistException
from app.logger import logger
from app.rabbit import get_rabbit_connection
from app.specialists.dao import SpecialistsDAO


class SpecialistsRabbit:
    @classmethod
    async def consume_find_specialist_by_name_message(cls):
        connection = await get_rabbit_connection()
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue("request_specialist_by_name", auto_delete=True)

            async for message in queue:
                async with message.process():
                    specialist_name = json.loads(message.body).get("specialist_name")

                    await cls.__send_specialist_for_find_specialist_by_name_request(specialist_name, channel)

                    logger.info(f"Received message: {json.loads(message.body)}")

    @staticmethod
    async def __send_specialist_for_find_specialist_by_name_request(
            specialist_name: str,
            channel: AbstractChannel,
        ) -> None:
        try:
            async with async_session_maker() as session:
                specialist = await SpecialistsDAO.find_specialist_by_name(session, specialist_name)
                await session.commit()

            body = {
                "id": str(specialist.id),
                "name": specialist.name,
                "avatar_id": specialist.avatar_id,
            }
        except Exception as e:
            body = {
                "status_code": e.status_code,
                "detail": e.detail,
            }

        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(body).encode()),
            routing_key="response_specialist_by_name"
        )

    @classmethod
    async def consume_find_specialist_by_id_message(cls):
        connection = await get_rabbit_connection()
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue("request_specialist_by_id", auto_delete=True)

            async for message in queue:
                async with message.process():
                    specialist_id = json.loads(message.body).get("specialist_id")

                    await cls.__send_specialist_for_find_specialist_by_id_request(specialist_id, channel)

                    logger.info(f"Received message: {json.loads(message.body)}")

    @staticmethod
    async def __send_specialist_for_find_specialist_by_id_request(
            specialist_id: str,
            channel: AbstractChannel,
        ) -> None:
        try:
            async with async_session_maker() as session:
                specialist = await SpecialistsDAO.find_one_or_none(session, id=specialist_id)
                await session.commit()

            body = {
                "id": str(specialist.id),
                "name": specialist.name,
                "avatar_id": specialist.avatar_id,
            }
        except Exception as e:
            body = {
                "status_code": e.status_code,
                "detail": e.detail,
            }
        
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(body).encode()),
            routing_key="response_specialist_by_id"
        ) 