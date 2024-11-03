from fastapi import APIRouter, HTTPException
from barbeshop.db.postgresql_db import engine
from barbeshop.schemas.services import CreateService, UpdateService, ReadService
from barbeshop.db.models.model_services import Service, DeletedService
from barbeshop.dao.dao_services import ServiceDAO

service_router = APIRouter()
service_dao = ServiceDAO(engine=engine)

@service_router.post("/services/")
async def create_service(service: CreateService):
    return service_dao.create_service(service=service)

@service_router.get("/services/")
async def read_services():
    return service_dao.return_services()
    

@service_router.get("/services/{service_id}")
async def read_service(service_id: int):
    return service_dao.return_service(service_id=service_id)
    
@service_router.patch("/services/{service_id}")
async def update_service(service_id: int, update_service: UpdateService):
    return service_dao.update_service(service_id=service_id, update_service=update_service)

@service_router.delete("/services/{service_id}")
async def del_service(service_id: int):   
    return service_dao.del_service(service_id=service_id)