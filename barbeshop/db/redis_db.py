import redis
import json
from codecs import decode
from barbeshop.schemas.experts import ReadExpert
from barbeshop.schemas.orders import ReadOrder
from barbeshop.schemas.services import ReadService

cli = redis.Redis(
    host='redis-host',
    port=10000,
    password='password')

class Redis_db:
    def __init__(self, connection=cli):
        self.last_get = None
        self._connection = connection

    def read_data(self, obj_id: int, last_get: str):
        with self._connection as conn:
            if self.last_get != last_get:
                self.delete_keys_by_name()
                self.last_get = last_get
                return None
            obj = conn.get(obj_id)
            if obj:
                return json.loads(decode(obj, encoding="utf-8"))
            return None

    def update_cache(self, obj: ReadExpert | ReadOrder | ReadService):
        with self._connection as conn:
            conn.set(name=obj.id, value=json.dumps(obj.serializer()))

client = Redis_db()