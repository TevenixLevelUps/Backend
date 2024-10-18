from fastapi import FastAPI
from barbeshop.middleware import SimpleLogging

from barbeshop.api.experts import expert_router
from barbeshop.api.orders import order_router
from barbeshop.api.services import service_router

from barbeshop.database import *

app = FastAPI()

app.add_middleware(SimpleLogging)

app.include_router(expert_router, prefix="/experts")
app.include_router(order_router, prefix="/orders")
app.include_router(service_router, prefix="/services")

@app.get("/")
async def hello():
    return {"Hello": "world"}