import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings
from app.exceptions import RateLimitException, SecretException
from app.services.router import router as services_router
from app.services.service_images.router import router as service_images_router
from app.specialists.router import router as specialists_router
from app.specialists.avatars.router import router as specialist_avatars_router
from app.orders.router import router as orders_router
from app.token_bucket import TokenBucket

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


@app.get("/secret")
async def get_secret_endpoint():
    raise SecretException

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


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, bucket: TokenBucket):
        super().__init__(app)
        self.bucket = bucket  # Initialize the middleware with a token bucket

    async def dispatch(self, request: Request, call_next):
        # Process each incoming request
        if self.bucket.take_token():
            # If a token is available, proceed with the request
            return await call_next(request)
        # If no tokens are available, return a 429 error (rate limit exceeded)
        raise RateLimitException


# Initialize the token bucket with 4 tokens capacity and refill rate of 2 tokens/second
bucket = TokenBucket(capacity=4, refill_rate=2)

# Add the rate limiting middleware to the FastAPI app
app.add_middleware(RateLimiterMiddleware, bucket=bucket)
