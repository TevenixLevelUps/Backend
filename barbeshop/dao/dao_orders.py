from barbeshop.db.models.model_orders import Order, DeletedOrder
from barbeshop.schemas.orders import CreateOrder, ReadOrder
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from barbeshop.db.models.model_services import Service
from barbeshop.addition.functions import time_plus_time
from barbeshop.db.redis_db import client

class OrderDAO():
    def __init__(self, engine):
        self._engine = engine

    def _makesession(self):
        try:
            Session = sessionmaker(bind=self._engine)
            session = Session()
            return session
        except Exception as ex:
            print(f"Cant to make session because of: {ex}")

    def create_order(self, order: CreateOrder):
        with self._makesession() as session:
            assotiated_service = session.query(Service).get(order.id_service)
            if not assotiated_service:
                raise HTTPException(status_code=400, detail="Service not found.")
            deleted_order = session.query(DeletedOrder).first()
            if deleted_order:
                new_order = Order(id=deleted_order.id, client_name=order.client_name, expert_name=order.expert_name, time_start=order.time_start, time_end=time_plus_time(order.time_start, assotiated_service.time))
                session.delete(deleted_order)
            else:
                new_order = Order(client_name=order.client_name, expert_name=order.expert_name, time_start=order.time_start, time_end=time_plus_time(order.time_start, assotiated_service.time).__dict__)  
            assotiated_service.orders.append(new_order)
            session.add(new_order)
            session.commit()
            return "Order was sucessfuly aded."
        
    def return_orders(self):
        with self._makesession() as session:
            orders = session.query(Order).all()
            if not orders:
                raise HTTPException(status_code=400, detail="Dont have any.")
            for order in orders:
                yield order

    def return_order(self, order_id: int):
        redis_order = client.get_obj("orders", order_id)
        if redis_order:
            return ReadOrder(id=redis_order["id"], client_name=redis_order["client_name"], expert_name=redis_order["expert_name"], time_start=redis_order["time_start"], time_end=redis_order["time_end"], id_service=redis_order["id_service"])
        with self._makesession() as session:
            order = session.query(Order).get(order_id)
            if not order:
                raise HTTPException(status_code=400, detail="Order not found.")
            client.add_hash_to_list("orders", ReadOrder(id=order.id, client_name=order.client_name, expert_name=order.expert_name, time_start=order.time_start, time_end=order.time_end, id_service=order.id_service).__dict__)
            return ReadOrder(id=order.id, client_name=order.client_name, expert_name=order.expert_name, time_start=order.time_start, time_end=order.time_end, id_service=order.id_service)
        
    def del_order(self, order_id: int):
        with self._makesession() as session:
            removable_order = session.query(Order).get(order_id)
            if not removable_order:
                raise HTTPException(status_code=400, detail="Order not found.")
            session.add(DeletedOrder(id=order_id))
            session.delete(removable_order)
            session.commit()
            return "Order was sucessfully deleted."