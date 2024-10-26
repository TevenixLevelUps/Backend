from sqlalchemy import Column, Integer, String, Float
from barbeshop.db.db_connect import Base
from barbeshop.db.models.base_model import BaseModel
from sqlalchemy.orm import relationship

class Service(BaseModel):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    describe = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    time = Column(String(5), nullable=False)

    orders = relationship("Order")

class DeletedService(Base):
    __tablename__ = 'deleted_services'

    id = Column(Integer, primary_key=True)