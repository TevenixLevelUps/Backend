import uvicorn
from fastapi import FastAPI

from app.config import settings
from app.services.router import router as services_router
from app.services.service_images.router import router as service_images_router
from app.specialists.router import router as specialists_router
from app.specialists.avatars.router import router as specialist_avatars_router
from app.orders.router import router as orders_router

app = FastAPI()

app.include_router(services_router)
app.include_router(service_images_router)
app.include_router(specialists_router)
app.include_router(specialist_avatars_router)
app.include_router(orders_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
