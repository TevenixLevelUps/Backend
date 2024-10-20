from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from models.database import Base


class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    service_id = Column(ForeignKey('services.id'))
    specialist_id = Column(ForeignKey('specialists.id'))
    date_time = Column(DateTime)

