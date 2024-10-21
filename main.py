from fastapi import FastAPI
from service import services_router
from specialist import specialists_router
from orders import orders_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(services_router)
app.include_router(specialists_router)
app.include_router(orders_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT", "PATCH", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
    ],
)

