from fastapi import APIRouter, HTTPException
from models import Service
from storage import services

services_router = APIRouter()

@services_router.get("/services")
def get_services():
    return list(services.values())

@services_router.post("/services")
def create_service(service: Service):
    if service.id not in services.keys():
        services[service.id] = service
    else:
        return HTTPException(status_code=404, detail="Такой ID уже существует, укажите другой")    
    return service

@services_router.get("/services/{service_id}")
def get_service(service_id: int):
    service = services.get(service_id)
    if service:
        return service
    raise HTTPException(status_code=404, detail="Услуга не найдена")
