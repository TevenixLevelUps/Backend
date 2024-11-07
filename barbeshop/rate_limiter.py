from barbeshop.db.redis_db import client
from codecs import decode
from fastapi import HTTPException

class RateLimiter:
    LIMIT = 5

    def __init__(self, redis_db=client) -> None:
        self.__conn = redis_db

    def compare_count(self, user_name: str) -> None:
        user_data = self.__conn.get_user(user_name)
        if user_data:
            if int(user_data["count"]) >= self.LIMIT:
                raise HTTPException(status_code=429, detail="Too many requests") 
            else:
                self.__conn.update_user(user_name)
                return True
        return True

rate_limiter = RateLimiter()