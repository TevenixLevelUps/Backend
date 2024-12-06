import asyncio
from time import time
from typing import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.config import settings
from app.logger import logger
from app.rabbitmq.specialists import SpecialistsRabbit
from app.rate_limiter import rate_limit_user, redis_client
from app.specialists.avatars.router import router as specialist_avatars_router
from app.specialists.router import router as specialists_router


def create_app() -> FastAPI:
    app = FastAPI(
        title='Specialists Service',
        docs_url='/api/docs',
        description='Specialists Service for levelup',
        debug=True,
        lifespan=lifespan,
    )
    app.include_router(specialists_router)
    app.include_router(specialist_avatars_router)

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


    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time()
        response = await call_next(request)
        process_time = time() - start_time
        logger.info("Request handling time", extra={
            "process_time": round(process_time, 4)
        })
        return response

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(RedisBackend(redis_client), prefix="cache")

    asyncio.create_task(SpecialistsRabbit.consume_find_specialist_by_name_message())
    asyncio.create_task(SpecialistsRabbit.consume_find_specialist_by_id_message())
    yield
