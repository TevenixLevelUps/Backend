from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from barbeshop.middleware import SimpleLogging
from barbeshop.config import origins

from barbeshop.api.experts import expert_router
from barbeshop.api.orders import order_router
from barbeshop.api.services import service_router

app = FastAPI(docs_url="/")

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["GET", "POST", "PATCH", "DELETE"],
                   allow_headers=["*"])

# app.add_middleware(SimpleLogging)

app.include_router(expert_router)
app.include_router(order_router)
app.include_router(service_router)