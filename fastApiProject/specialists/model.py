from sqlalchemy import Column, Integer, String

from models.database import Base


class Specialists(Base):
    __tablename__ = 'specialists'

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String,nullable=False)
    avatar = Column(String)
