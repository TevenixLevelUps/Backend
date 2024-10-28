from datetime import datetime


from sqlalchemy import ForeignKey,String
from sqlalchemy.orm import Mapped,mapped_column,relationship
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
   from .service import Service
   from .specialist import Specialist


class Orders(Base):
   client_name: Mapped[str] = mapped_column(String(25))
   service_id : Mapped[int] = mapped_column(ForeignKey('service.id'))
   specialist_id : Mapped[int] = mapped_column(ForeignKey('specialist.id'))
   order_time : Mapped[datetime] = mapped_column()

   service : Mapped ["Service"] = relationship(back_populates="orders")
   specialist : Mapped ["Specialist"] = relationship( back_populates="orders")