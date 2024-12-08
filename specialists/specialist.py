from fastapi import APIRouter
from specialists.models import Specialist
from specialists.specialist_DAO import SpecialistDAO
from fastapi_cache.decorator import cache

specialists_router = APIRouter(prefix="/specialists")


@specialists_router.get("")
@cache(expire=20)
async def get_specialists():
    return await SpecialistDAO.get_all()
    

@specialists_router.post("", status_code=201)
async def create_specialist(specialist: Specialist):
    return await SpecialistDAO.create_specialist(specialist)


@specialists_router.get("/{specialist_id}")
@cache(expire=20)
async def get_specialist(specialist_id: int):
    return await SpecialistDAO.get_by_id(specialist_id)


@specialists_router.delete("/{specialist_id}", status_code=204)
async def delete_specialist(specialist_id: int):
    return await SpecialistDAO.delete_specialist(specialist_id)