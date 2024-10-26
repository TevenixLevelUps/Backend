from barbeshop.db.db_connect import Base
from barbeshop.db.db_connect import engine
from barbeshop.db.models.model_experts import Expert
from barbeshop.db.models.model_orders import Order
from barbeshop.db.models.model_services import Service

origins = [
    "http://localhost",
    "Http://localhost:8000"
]

Base.metadata.create_all(engine)