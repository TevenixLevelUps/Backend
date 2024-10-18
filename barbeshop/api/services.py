from barbeshop.addition.functions import gener_id_from_list
from barbeshop.database import list_services
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from barbeshop.schemas.services import Service

service_router = APIRouter()

@service_router.post("/")
async def create_service(service: Service):
    id = gener_id_from_list(list_services)
    service.id = id
    list_services[id] = service
    return service

@service_router.get("/")
async def read_services():
    return list_services

@service_router.get("/{service_id}")
async def read_service(service_id: int):
    try:
        return list_services[service_id]
    except Exception:
        raise HTTPException(status_code=400, detail="Service not found.")

@service_router.patch("/{service_id}")
async def update_service(service_id: int, update_service: Service):
    try:
        old_service_data = list_services[service_id]
        old_service_model = Service(id=old_service_data.id, 
                                    name=old_service_data.name, 
                                    describe=old_service_data.describe, 
                                    price=old_service_data.price, 
                                    time=old_service_data.time)
        update_data = update_service.model_dump(exclude_unset=True)
        print(update_data)
        updated_service = old_service_model.model_copy(update=update_data)
        print(updated_service)
        updated_service.id = old_service_data.id
        list_services[service_id] = jsonable_encoder(updated_service)
        return updated_service
    except Exception:
        raise HTTPException(status_code=400, detail="Service not found.")

@service_router.delete("/{service_id}")
async def del_service(service_id: int):
    try:
        del list_services[service_id]
        return list_services
    except Exception:
        raise HTTPException(status_code=400, detail="Service not found.") 