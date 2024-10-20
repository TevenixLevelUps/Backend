from fastapi import APIRouter, HTTPException
from models import Specialist
from storage import specialists

specialists_router = APIRouter()

@specialists_router.get("/specialists")
def get_specialists():
    return list(specialists.values())

@specialists_router.post("/specialists")
def create_specialist(specialist: Specialist):
    specialists[specialist.id] = specialist
    return specialist

@specialists_router.get("/specialists/{specialist_id}")
def get_specialist(specialist_id: int):
    specialist = specialists.get(specialist_id)
    if specialist:
        return specialist
    raise HTTPException(status_code=404, detail="Специалист не найден")