from barbeshop.db.models.model_services import Service, DeletedService
from barbeshop.schemas.services import CreateService, UpdateService,  ReadService
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from barbeshop.db.redis_db import client

class ServiceDAO():
    def __init__(self, engine):
        self._engine = engine

    def _makesession(self):
        try:
            Session = sessionmaker(bind=self._engine)
            session = Session()
            return session
        except Exception as ex:
            print(f"Cant to make session because of: {ex}")

    def create_service(self, service: CreateService):
        with self._makesession() as session:
            deleted_service = session.query(DeletedService).first()
            if deleted_service:
                session.add(Service(id=deleted_service.id, name=service.name, describe=service.describe, price=service.price, time=service.time))
                session.delete(deleted_service)
            else:
                session.add(Service(name=service.name, describe=service.describe, price=service.price, time=service.time))
            session.commit()
            return "Service was sucessfully created."
        
    def return_services(self):
        with self._makesession() as session:
            services = session.query(Service).all()
            if not services:
                raise  HTTPException(status_code=400, detail="Dont have any.")
            for service in services:
                yield service

    def return_service(self, service_id: int):
        redis_service = client.get_obj("services", service_id)
        if redis_service:
            return ReadService(id=redis_service["id"], name=redis_service["name"], describe=redis_service["describe"], price=redis_service["price"], time=redis_service["time"])
        with self._makesession() as session:
            service = session.query(Service).get(service_id)
            if not service:
                raise HTTPException(status_code=400, detail="Service not found.")
            client.add_hash_to_list("services", ReadService(id=service.id, name=service.name, describe=service.describe, price=service.price, time=service.time).__dict__)
            return ReadService(id=service.id, name=service.name, describe=service.describe, price=service.price, time=service.time)
    
    def update_service(self, service_id: int, update_service: UpdateService):
        with self._makesession() as session:
            old_service = session.query(Service).get(service_id)
            if not old_service:
                raise HTTPException(status_code=400, detail="Service not found.")
            for attr, value in update_service.model_dump().items():
                if value:
                    setattr(old_service, attr, value)
            session.commit()
            return "Service was sucessfully updated."

    def del_service(self, service_id: int):
        with self._makesession() as session:
            removable_service = session.query(Service).get(service_id)
            if not removable_service:
                raise HTTPException(status_code=400, detail="Service not found.") 
            session.add(DeletedService(id=service_id))
            session.delete(removable_service)
            session.commit()
            return "Service was sucessfully deleted."