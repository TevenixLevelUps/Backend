from sqlalchemy import Column, Integer, String
from barbeshop.db.postgresql_db import Base

class Expert(Base):
    __tablename__ = 'experts'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class DeletedExpert(Base):
    __tablename__ = 'deleted_experts'

    id = Column(Integer, primary_key=True)