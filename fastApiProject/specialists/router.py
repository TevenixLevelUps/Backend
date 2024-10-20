from fastapi import APIRouter, HTTPException,status,UploadFile,Depends,File
from specialists.shema import SpecialistResponseModel, SpecialistRegisterModel
from typing import Optional,Annotated
from images.loadfie import load_photo
from specialists.SpecialistQuery import SpecialistsQuery

router = APIRouter(prefix="/specialists", tags=["specialists"])

@router.get("/{specialist_id}")
async def get_specialist_by_id(specialist_id: int) -> SpecialistResponseModel:
    specialist = await SpecialistsQuery.find_one_or_none(id=specialist_id)
    if specialist is None:
        raise HTTPException(status_code=404, detail="Specialist not found")
    return specialist

@router.get("/find_by_name/{name}")
async def get_specialist_by_name(name: str) -> list[SpecialistResponseModel]:
    specialists = await SpecialistsQuery.find_all(name=name)
    if specialists is None:
        raise HTTPException(status_code=404, detail="Specialist not found")
    return specialists

@router.get("")
async def get_all_specialists() -> list[SpecialistResponseModel]:
    specialists = await SpecialistsQuery.find_all()
    if specialists is None:
        raise HTTPException(status_code=404, detail="Specialist not found")
    return specialists


@router.post("/add_specialist")
async def create_specialist(specialist:Annotated[SpecialistRegisterModel,Depends()],photo:Annotated[UploadFile|str,File()] = ''):
    path = ''
    if photo:
        path = load_photo(specialist,photo)

    await SpecialistsQuery.make_record(name=specialist.name,avatar=path)
    return {"Success":True}

@router.delete("/delete_specialist/{specialist_id}")
async def delete_specialist(specialist_id: int):
    await SpecialistsQuery.remove_specialist(specialist_id)
    return {"Success": True}




