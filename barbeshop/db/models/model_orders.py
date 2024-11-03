from sqlalchemy import Column, Integer, String, ForeignKey
from barbeshop.db.postgresql_db import Base
from barbeshop.db.models.base_model import BaseModel

class Order(BaseModel):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    client_name = Column(String(50), nullable=False)
    expert_name = Column(String(50), nullable=False)
    time_start = Column(String(5), nullable=False)
    time_end = Column(String(5), nullable=False)

    id_service = Column(ForeignKey("services.id"))

class DeletedOrder(Base):
    __tablename__ = 'deleted_orders'

    id = Column(Integer, primary_key=True)