from datetime import datetime, timezone
from sqlalchemy.types import LargeBinary
from sqlalchemy.orm import Mapped,mapped_column
from .base import Base
from sqlalchemy import String

class Service(Base):

    name : Mapped[str] = mapped_column(String(25))
    description : Mapped[str] = mapped_column(String(150))
    price:Mapped[float] = mapped_column()
    execution_time:Mapped[datetime] = mapped_column(timezone.utc)
    image: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)