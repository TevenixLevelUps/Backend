from barbeshop.db.postgresql_db import Base
from barbeshop.db.postgresql_db import engine

origins = [
    "http://localhost",
    "Http://localhost:8000"
]

Base.metadata.create_all(engine)