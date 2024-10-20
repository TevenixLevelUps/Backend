from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from orders.model import Orders
from orders.shema import OrderModel
from orders.OrdersQuery import OrdersQuery


router = APIRouter(tags=["orders"],prefix="/orders")

@router.get("/")
async def get_all():
    orders = await OrdersQuery.find_all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return orders

@router.get("/orders_by_name/{name}")
async def get_by_name(name: str):
    orders = await OrdersQuery.find_all(name=name)
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return orders

@router.post("/add_order")
async def add_order(order: Annotated[OrderModel,Depends()]):
    last_time = await OrdersQuery.get_order_time(order.specialists_id)

    if last_time is None:
        last_time = datetime.now()

    if order.date_time >= last_time:
        await OrdersQuery.make_record(
            name=order.customer_name,
            service_id=order.service_id,
            specialist_id=order.specialists_id,
            date_time=order.date_time,
        )
        return {"success": True}
    else:
        raise HTTPException(status_code=403, detail="Специалист занят")

@router.delete("/remove_order")
async def remove_order(id:int):
     await OrdersQuery.remove_order(id)
     return {"success": True}
