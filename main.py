from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
from Orders.views import router as orders_router
from service.views import router as services_router
from specialist.views import router as specialist_router
from database.db_helper import db_helper
from models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield





app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(specialist_router)
app.include_router(orders_router)
app.include_router(services_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

