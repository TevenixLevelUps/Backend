from fastapi.openapi.models import Schema
from pydantic import BaseModel, validator, field_validator
from datetime import datetime


class OrderModel(BaseModel):
    customer_name: str
    specialists_id: int
    service_id: int
    date_time: str

    @field_validator('date_time')
    def validate_date_time(cls, value):
        try:
            #  в datetime
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError("Invalid date format. Expected format: YYYY-MM-DD HH:MM:SS")




