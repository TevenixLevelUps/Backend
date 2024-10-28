from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.db_helper import db_helper
from .shema import Order,CreateOrder
from .dependencies import get_order_by_id
from .import service
router = APIRouter(tags=["Orders"])



@router.get("/orders")
async def get_orders(session : AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await  service.get_all_orders(session=session)


@router.get("/orders/{id}")
async def get_order(order = Depends(get_order_by_id)):
    return order


@router.post("/orders_create",status_code=status.HTTP_201_CREATED)
async def create_order(order_in: CreateOrder, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return  await service.create_order(order_in=order_in , session=session)




@router.delete("/orders_delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(session: AsyncSession = Depends(db_helper.scoped_session_dependency),order = Depends(get_order_by_id)):
    return await  service.delete_order(session=session, order=order )

