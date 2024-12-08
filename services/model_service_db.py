from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from database.database import Base

class Service_cls(Base):
    __tablename__ ="service"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    descripton: Mapped[str]
    price: Mapped[float]
    time: Mapped[int]
    image: Optional[Mapped[str]] = ""