from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request

from app.auth.views import router as auth_router
from app.core.rate_limit import rate_limit
from app.database import db_helper
from app.models import Base
from app.Orders.views import router as orders_router
from app.service.views import router as services_router
from app.specialist.views import router as specialist_router


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


app.include_router(auth_router)
app.include_router(specialist_router)
app.include_router(orders_router)
app.include_router(services_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
