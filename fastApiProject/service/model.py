from sqlalchemy import Column, Integer, String, DECIMAL, Time

from models.database import Base


class Services(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String,nullable=False)
    description = Column(String)
    price = Column(DECIMAL,nullable=False)
    time_to_complete = Column(Time,nullable=False)
    picture = Column(String)

    def __str__(self):
        return f"Услуга {self.name}"


