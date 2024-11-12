from dotenv import load_dotenv
import os
import redis.asyncio as redis_async
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

try:
    redis_port = int(REDIS_PORT) if REDIS_PORT is not None else 6379
except ValueError:
    raise ValueError(f"Invalid REDIS_PORT value: {REDIS_PORT}")


redis_client = redis_async.Redis(host='localhost', port= redis_port, db=0)
