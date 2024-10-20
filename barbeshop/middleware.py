from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException, Request
from collections import defaultdict
import time

clients_requests = defaultdict(list)

class SimpleLogging(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        print(f"Фиксируем запрос: {request.method} {request.url}")
        client_ip = request.client.host
        current_time = time.time()

        request_times = clients_requests[client_ip]
        request_times = [t for t in request_times if current_time - t < 60]
        clients_requests[client_ip] = request_times

        if len(request_times) >= 10:
            raise HTTPException(status_code=429, detail="Too many requests")

        clients_requests[client_ip].append(current_time)

        response = await call_next(request)
        print(f"Фиксируем ответ: {response.status_code}")
        return response