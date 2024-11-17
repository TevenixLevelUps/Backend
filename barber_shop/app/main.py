from typing import Awaitable, Callable

from app.config import settings
from app.orders.router import router as orders_router
from app.rate_limiter import rate_limit_user, redis_client
from app.services.router import router as services_router
from app.services.service_images.router import router as service_images_router
from app.specialists.avatars.router import router as specialist_avatars_router
from app.specialists.router import router as specialists_router
from fastapi import FastAPI, Request, Response
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


def create_app() -> FastAPI:
    app = FastAPI(
        title='BarberShop',
        docs_url='/api/docs',
        description='Barber Shop for levelup',
        debug=True,
        lifespan=lifespan,
    )
    app.include_router(services_router)
    app.include_router(service_images_router)
    app.include_router(specialists_router)
    app.include_router(specialist_avatars_router)
    app.include_router(orders_router)

    origins = [
        "*",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
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

    @app.middleware("http")
    async def rate_limit_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        if settings.mode.mode != "TEST":
            user = request.client.host
            if user:
                rate_limit_exceeded_response = await rate_limit_user(
                    user=user, rate_limit=settings.redis.rate_limit_per_minute
                )
                if rate_limit_exceeded_response:
                    return rate_limit_exceeded_response

        return await call_next(request)

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(RedisBackend(redis_client), prefix="cache")
    yield
