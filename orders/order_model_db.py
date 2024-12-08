from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from database.database import Base


class Order_cls(Base):
    __tablename__ = "order"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    client_name: Mapped[str]
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"))
    specialist_id: Mapped[int] = mapped_column(ForeignKey("specialist.id"))
    time: Mapped[datetime]