from typing import Annotated

from fastapi import APIRouter, HTTPException, UploadFile,File
from fastapi.params import Depends

from images.loadfie import load_photo
from service.ServiceQuery import ServiceQuery
from service.shema import ServiceRegisterModel, ServiceUpdateModel

router = APIRouter(prefix="/service", tags=["service"])


@router.get("/")
async def get_all_services():
    services =  await ServiceQuery.find_all()
    if not services:
        raise HTTPException(status_code=404, detail="No services found")
    return services


@router.post("/add_service")
async def add_service(service: Annotated[ServiceRegisterModel,Depends()],photo: Annotated[UploadFile | str,File()] = ''):
    path = ''
    if photo:
        path = load_photo(service, photo)

    await ServiceQuery.make_record(name=service.name,description= service.description,price=service.price,time_to_complete=service.time_to_complete,picture=path)
    return {"Success": True}

@router.delete("/delete_service")
async def delete_service(id: int):
    await ServiceQuery.remove_service(service_id=id)
    return {"Success": True}

@router.patch("/update_service")
async def update_service(id:int,update_data:Annotated[ServiceUpdateModel,Depends()],photo: Annotated[UploadFile | str,File()] = ''):
    path = ''
    if photo:
        path = load_photo(update_data, photo)
    updated_service = await ServiceQuery.update_service(id,**{key: value for key,value in update_data.__dict__.items() if value},picture=path)
    return updated_service






