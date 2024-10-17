from fastapi import FastAPI, HTTPException, Query, Request
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from pydantic import BaseModel, Field
from typing import Annotated, List
import random
import time

from starlette.responses import Response

app = FastAPI()

clients_requests = defaultdict(list)

class SimpleLogging(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        print(f"Фиксируем запрос: {request.method} {request.url}")
        client_ip = request.client.host
        current_time = time.time()

        request_times = clients_requests[client_ip]
        request_times = [t for t in request_times if current_time - t < 60]
        clients_requests[client_ip] = request_times

        if len(request_times) >= 10:
            raise HTTPException(status_code=429, detail="Too many requests")

        clients_requests[client_ip].append(current_time)

        response = await call_next(request)
        print(f"Фиксируем ответ: {response.status_code}")
        return response

app.add_middleware(SimpleLogging)

services_pattern = r"^(?:00|01|02):[0-5]\d$"
orders_pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"

class Expert(BaseModel):
    name: str = Field("Valeri Djmishenko")

list_experts: List[Expert] = []
dict_experts = {"Experts": list_experts}

class Service(BaseModel):
    name: str = Field("Classic haircut")
    describe: str | None = Field("Mojno corotko ili dlino")
    price: float = Field(10.5)
    time: str = Field("01:00", pattern=services_pattern)

list_services: List[Service] = []
dict_services = {"Services": list_services}

class Order(BaseModel):
    client_name: str = Field("P Diddi")
    exper_name: str
    time: str = Field("13:00", pattern=orders_pattern)

list_orders: List[Order] = []
dict_orders = {"Orders": list_orders}

fake_db = [dict_experts, dict_services, dict_orders]

def gener_id_from_list(some_list: List):
    flag = False
    id = int(random.uniform(0,100))
    for i in some_list:
        for k,v in i.items():
            if k == "id":
                if id == v:
                    flag = True
    if flag:
        return gener_id_from_list(some_list)
    else:
        return id

def read_dict_in_list(some_list: List, return_value: str, value: int | str):
    for object in some_list:
            for k,v in object.items():
                if k == return_value:
                    if v == value:
                        return object

@app.get("/")
async def hello():
    return {"Hello": "world"}

@app.post("/experts/")
async def create_expert(expert: Annotated[Expert, Query()]): 
    id = gener_id_from_list(list_experts)
    expert_final = expert.model_dump()
    expert_final.update({"id": id})
    list_experts.append(expert_final)
    return expert_final

@app.post("/services/")
async def create_service(service: Annotated[Service, Query()]):
    id = gener_id_from_list(list_services)
    service_final = service.model_dump()
    service_final.update({"id": id})
    list_services.append(service_final)
    return service_final

@app.post("/orders/")
async def create_order(order: Annotated[Order, Query()]):
    if list_orders:
        if read_dict_in_list(list_orders, "time", order.time):
            raise HTTPException(status_code=403, detail="Forbidden")
    id = gener_id_from_list(list_orders)
    order_final = order.model_dump()
    order_final.update({"id": id})  
    list_orders.append(order_final)
    return order_final
    
@app.get("/objects/{object_name}")
async def read_object(object_name: str):
    if object_name == "experts":
        return list_experts
    elif object_name == "services":
        return list_services
    elif object_name == "orders":
        return list_orders
    else:
        raise HTTPException(status_code=400, detail="Uncorrect input")

@app.delete("/{object_name}/{object_id}")
async def delete_object(object_name: str, object_id: int):
    i = 0
    if object_name == "experts":
        if read_dict_in_list(list_experts, "id", object_id):
            for obj in list_experts:
                if obj == read_dict_in_list(list_experts, "id", object_id):
                    del list_experts[i]
                    return list_experts
                i += 1
    if object_name == "services":
        if read_dict_in_list(list_services, "id", object_id):
            for obj in list_services:
                if obj == read_dict_in_list(list_services, "id", object_id):
                    del list_services[i]
                    return list_services
                i += 1
    if object_name == "orders":
        if read_dict_in_list(list_orders, "id", object_id):
            for obj in list_orders:
                if obj == read_dict_in_list(list_orders, "id", object_id):
                    del list_orders[i]
                    return list_orders
                i += 1
    else:
        raise HTTPException(status_code=400, detail="Uncorrect input")

@app.get("/db/")
async def return_db():
    return fake_db