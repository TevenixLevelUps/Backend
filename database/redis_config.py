from dotenv import load_dotenv
import os
import redis.asyncio as redis_async
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")



redis_client = redis_async.Redis(host='localhost', port=6379, db=0)
