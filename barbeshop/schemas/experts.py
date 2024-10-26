from pydantic import BaseModel, Field

class CreateExpert(BaseModel):
    name: str = Field("Valeri Djmishenko")

class UpdateExpert(BaseModel):
    id: int | None = None
    name: str | None = Field("Valeri Djmishenko")

class ReadExpert(BaseModel):
    id: int | None = None 
    name: str | None = None 