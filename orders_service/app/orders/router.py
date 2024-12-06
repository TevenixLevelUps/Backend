from uuid import uuid4

from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import session_getter
from app.exceptions import WrongTimeException
from app.logger import logger
from app.orders.dao import OrdersDAO
from app.orders.schemas import ErrorSchema, SOrderCreate, SOrderGet
from app.rabbitmq.services import ServicesRabbit
from app.rabbitmq.specialists import SpecialistsRabbit

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
        status.HTTP_404_NOT_FOUND: {'model': ErrorSchema},
        status.HTTP_429_TOO_MANY_REQUESTS: {'model': ErrorSchema},
    },         
)
async def post_order(
        order: SOrderCreate,
        session: AsyncSession = Depends(session_getter),
) -> SOrderCreate:
    try:
        await OrdersDAO.create_order(session, order)
    except DBAPIError:
        raise WrongTimeException
    await session.commit()
    return order


@router.get(
    "/",
    responses={
        status.HTTP_429_TOO_MANY_REQUESTS: {'model': ErrorSchema},
    },        
)
@cache(expire=settings.redis.cache_expire_seconds)
async def get_orders(session: AsyncSession = Depends(session_getter)) -> list[SOrderCreate]:
    orders: list[SOrderGet] = await OrdersDAO.find_all(session)

    result_orders = []
    for order in orders:
        service = await ServicesRabbit.send_request_for_get_service_by_id(order.service_id)
        specialist = await SpecialistsRabbit.send_request_for_get_specialist_by_id(order.specialist_id)
        result_orders.append(
            SOrderCreate(
                customer_name=order.customer_name,
                service_title=service.get("title"),
                specialist_name=specialist.get("name"),
                order_time=order.order_time
            )
        )
    return result_orders


@router.delete(
    "/", 
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
        status.HTTP_404_NOT_FOUND: {'model': ErrorSchema},
        status.HTTP_429_TOO_MANY_REQUESTS: {'model': ErrorSchema},
    },
)
async def delete_order(
        order_to_delete: SOrderCreate,
        session: AsyncSession = Depends(session_getter),
) -> None:
    try:
        await OrdersDAO.delete_order(session, order_to_delete)
    except DBAPIError:
        raise WrongTimeException
    await session.commit()
