from fastapi import APIRouter
from services.model_service import Service
from services.servicesDAO import Service_DAO
from fastapi_cache.decorator import cache

services_router = APIRouter(prefix="/services")

# Эндпоинт для получения всех услуг
@services_router.get("")
@cache(expire=20)
async def get_services():
    return await Service_DAO.get_all()
    

# Эндпоинт для создания новой услуги
@services_router.post("")
async def create_service(service: Service):
    return await Service_DAO.create_service(service)
    

# Эндпоинт для получения конкретной услуги по ID
@services_router.get("/{service_id}")
@cache(expire=20)
async def get_service(service_id: int):
    return await Service_DAO.get_by_id(service_id)
    