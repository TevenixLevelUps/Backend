from fastapi import APIRouter, HTTPException
from barbeshop.db.db_connect import session
from barbeshop.schemas.services import CreateService, UpdateService, ReadService
from barbeshop.db.models.model_services import Service, DeletedService

service_router = APIRouter()

@service_router.post("/services/")
async def create_service(service: CreateService):
    deleted_service = session.query(DeletedService).first()
    id = lambda deleted_id: deleted_id if deleted_id else None
    session.add(Service(id=id(deleted_service.id), name=service.name, describe=service.describe, price=service.price, time=service.time))
    if id(deleted_service.id):
        session.delete(deleted_service)
    session.commit()
    return service

@service_router.get("/services/")
async def read_services():
    services = session.query(Service).all()
    if not services:
        raise  HTTPException(status_code=400, detail="Dont have any.")
    list_services = []
    for service in services: 
        list_services.append(ReadService(id=service.id, name=service.name, describe=service.describe, price=service.price, time=service.time))
    return list_services
    

@service_router.get("/services/{service_id}")
async def read_service(service_id: int):
    service = session.query(Service).get(service_id)
    if not service:
        raise HTTPException(status_code=400, detail="Service not found.")
    return ReadService(id=service.id, name=service.name, describe=service.describe, price=service.price, time=service.time)
    
@service_router.patch("/services/{service_id}")
async def update_service(service_id: int, update_service: UpdateService):
    old_service = session.query(Service).get(service_id)
    if not old_service:
        raise HTTPException(status_code=400, detail="Service not found.")
    for attr, value in update_service.model_dump().items():
        if value:
            setattr(old_service, attr, value)
    session.commit()
    return old_service

@service_router.delete("/services/{service_id}")
async def del_service(service_id: int):   
    removable_service = session.query(Service).get(service_id)
    if not removable_service:
        raise HTTPException(status_code=400, detail="Service not found.") 
    session.add(DeletedService(id=service_id))
    session.delete(removable_service)
    session.commit()
    return "Service was sucessfully deleted."