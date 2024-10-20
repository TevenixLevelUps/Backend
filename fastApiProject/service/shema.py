from copyreg import pickle
from typing import Optional, Annotated

from fastapi import Query
from pydantic import BaseModel, validator, field_validator
from fastapi import UploadFile
from decimal import Decimal
from datetime import date,timedelta,time


class ServiceRegisterModel(BaseModel):
    name: str
    description: Annotated[Optional[str],Query(max_length=100)] = None
    price: float
    time_to_complete: str
    __picture: str | None = None

    @field_validator('time_to_complete')
    def parse_timedelta(cls, value: str) -> time:
        if isinstance(value, str):
            try:
                # HH:MM
                hours, minutes = map(int, value.split(":"))
                return time(hour=hours, minute=minutes)
            except ValueError:
                raise ValueError("Invalid time format. Use 'HH:MM' or ISO 8601 duration")
        return value



class ServiceUpdateModel(ServiceRegisterModel):
    #__annotations__ = {name: Optional[type] for name,type in ServiceRegisterModel.__annotations__.items() if isinstance(type,(str,float))}

    name: Optional[str] = None
    price: Optional[float] = None
    time_to_complete: Optional[str] = None




