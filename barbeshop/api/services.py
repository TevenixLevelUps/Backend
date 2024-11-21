from fastapi import APIRouter
from barbeshop.db.postgresql_db import engine
from barbeshop.schemas.services import CreateService, UpdateService, ReadService
from barbeshop.dao.dao_services import ServiceDAO
from barbeshop.rate_limiter import rate_limiter

service_router = APIRouter()
service_dao = ServiceDAO(engine=engine)

@service_router.post("/services/")
async def create_service(service: CreateService):
    if rate_limiter.compare_count("admin"):
        return service_dao.create_service(service=service)

@service_router.get("/services/")
async def read_services():
    if rate_limiter.compare_count("admin"):
        return service_dao.return_services()
    

@service_router.get("/services/{service_id}")
async def read_service(service_id: int):
    if rate_limiter.compare_count("admin"):
        return service_dao.return_service(service_id=service_id)
    
@service_router.patch("/services/{service_id}")
async def update_service(service_id: int, update_service: UpdateService):
    if rate_limiter.compare_count("admin"):
        return service_dao.update_service(service_id=service_id, update_service=update_service)

@service_router.delete("/services/{service_id}")
async def del_service(service_id: int):   
    if rate_limiter.compare_count("admin"):
        return service_dao.del_service(service_id=service_id)