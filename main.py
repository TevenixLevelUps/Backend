from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
import uvicorn
from Orders.views import router as orders_router
from service.views import router as services_router
from specialist.views import router as specialist_router
from database.db_helper import db_helper
from models.base import Base
from database import rate_limit


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def limit_requests(request: Request, call_next):
    await rate_limit(request, calls=10, period=60)  # 10 запросов в минуту
    response = await call_next(request)
    return response


app.include_router(specialist_router)
app.include_router(orders_router)
app.include_router(services_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
