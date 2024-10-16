import uvicorn
from fastapi import FastAPI

from app.config import settings
from app.services.router import router as services_router

app = FastAPI()

app.include_router(services_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
