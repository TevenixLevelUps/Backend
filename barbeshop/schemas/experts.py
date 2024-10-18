from pydantic import BaseModel, Field

class Expert(BaseModel):
    id: int
    name: str = Field("Valeri Djmishenko")