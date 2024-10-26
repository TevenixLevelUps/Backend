from barbeshop.addition.functions import time_plus_time
from fastapi import APIRouter, HTTPException
from barbeshop.db.db_connect import session
from barbeshop.schemas.orders import CreateOrder, ReadOrder
from barbeshop.db.models.model_orders import Order, DeletedOrder
from barbeshop.db.models.model_services import Service

order_router = APIRouter()

@order_router.post("/orders/")
async def create_order(order: CreateOrder):
    assotiated_service = session.query(Service).get(order.id_service)
    if not assotiated_service:
        raise HTTPException(status_code=400, detail="Service not found.")
    deleted_order = session.query(DeletedOrder).first()
    id = lambda deleted_id: deleted_id if deleted_id else None
    new_order = Order(id=id(deleted_order.id), client_name=order.client_name, expert_name=order.expert_name, time_start=order.time_start, time_end=time_plus_time(order.time_start, assotiated_service.time))
    if id(deleted_order.id):
        session.delete(deleted_order)
    assotiated_service.orders.append(new_order)
    session.add(new_order)
    session.commit()
    return new_order

@order_router.get("/orders/")
async def read_orders():
    orders = session.query(Order).all()
    if not orders:
        raise HTTPException(status_code=400, detail="Dont have any.")
    list_orders = []
    for order in orders:
        list_orders.append(ReadOrder(id=order.id, client_name=order.client_name, expert_name=order.expert_name, time_start=order.time_start, time_end=order.time_end, id_service=order.id_service))
    return list_orders

@order_router.get("/orders/{order_id}")
async def read_order(order_id: int):
    order = session.query(Order).get(order_id)
    if not order:
        raise HTTPException(status_code=400, detail="Order not found.")
    return ReadOrder(id=order.id, client_name=order.client_name, expert_name=order.expert_name, time_start=order.time_start, time_end=order.time_end, id_service=order.id_service)


@order_router.delete("/orders/{order_id}")
async def del_order(order_id: int):
    removable_order = session.query(Order).get(order_id)
    if not removable_order:
        raise HTTPException(status_code=400, detail="Order not found.")
    session.add(DeletedOrder(id=order_id))
    session.delete(removable_order)
    session.commit()
    return "Order was sucessfully deleted."