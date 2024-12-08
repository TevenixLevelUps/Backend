from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from database.database import Base


class Specialist_cls(Base):
    __tablename__ = "specialist"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    avatar: Optional[Mapped[str]] = ""