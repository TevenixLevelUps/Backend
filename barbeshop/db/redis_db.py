import redis
from codecs import decode

cli = redis.Redis(
    host='',
    port=1000,
    password='')

class Redis_db:
    __last_list: str = "None"

    def __init__(self, connection=cli):
        self.__connection = connection
    
    def add_hash_to_list(self, list_name: str, data: dict):
        with self.__connection as conn:
            conn.hset(name=data["id"], mapping=data)
            conn.rpush(list_name, data["id"])

    def get_obj(self, list_name: str, obj_id: int):
        if list_name == self.__last_list:
            with self.__connection as conn:
                dict_of_attr = conn.hgetall(obj_id)
                return {decode(key, "utf-8"): decode(value, "utf-8") for key, value in dict_of_attr.items()}
        else:
            self.__clear_list(self.__last_list)
            self.__last_list = list_name
            return None

    def __clear_list(self, list_name: str):
        with self.__connection as conn:
            if conn.exists(list_name):
                keys_list = conn.lrange(list_name, 0, -1)
                conn.delete(list_name)
                for item in keys_list:
                    conn.delete(item)

    def get_user(self, user_name: str) -> dict | None:
        with self.__connection as conn:
            if conn.exists(user_name):
                dict_user_info = conn.hgetall(name=user_name)
                return {decode(key, "utf-8"): decode(value, "utf-8") for key, value in dict_user_info.items()}
            else:
                conn.hset(user_name, "count", 1)
                conn.expire(user_name, 30)
                return None

    def update_user(self, user_name: str) -> None:
        with self.__connection as conn:
            conn.hincrby(user_name, "count", 1)

client = Redis_db()