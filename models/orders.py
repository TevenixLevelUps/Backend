from datetime import datetime


from sqlalchemy import ForeignKey,String
from sqlalchemy.orm import Mapped,mapped_column


from .base import Base




class Orders(Base):
   client_name: Mapped[str] = mapped_column(String(25))
   service_id : Mapped[int] = mapped_column()
   specialist_id : Mapped[int] = mapped_column(ForeignKey('specialist.id'))
   order_time : Mapped[datetime] = mapped_column()