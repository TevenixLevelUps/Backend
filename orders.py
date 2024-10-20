from fastapi import APIRouter, HTTPException
from models import Order
from storage import orders, specialists, services
from datetime import timedelta

orders_router = APIRouter()

@orders_router.get("/orders")
async def get_orders():
    return list(orders.values())

@orders_router.post("/orders")
async def create_order(order: Order):
    specialist = specialists.get(order.specialist_id)
    service = services.get(order.service_id)
    
    if not specialist or not service:
        return HTTPException(404, detail="Специалист или сервис не найден")
    
    for specialist in specialists.values():
        if specialist["id"] == order.specialist_id:
            for order_i in specialist["orders"]:
                if max(order.time, order_i.time) - min(order.time, order_i.time) < timedelta(minutes=int(services[order.service_id]["time"][:2])):
                    return HTTPException(404, detail="Время уже забранированно, выберите друго время или другого специалиста")
    
    specialists[order.specialist_id]["orders"].append(order)
    orders[order.id] = order
    return order
            
