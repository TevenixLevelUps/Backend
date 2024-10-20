from fastapi import FastAPI
from decimal import Decimal
from datetime import date
from datetime import datetime, timedelta
from decimal import Decimal
from specialists.router import router as specialist_router
from service.router import router as service_router
from orders.router import router as order_router
from starlette.middleware.cors import CORSMiddleware



app = FastAPI()

app.include_router(specialist_router)
app.include_router(service_router)

app.include_router(order_router)

origins = [
    "site"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUTCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization", "Access-Control-Request-Headers","Set-Cookie","Access-Control-Request-Headers"],
)
