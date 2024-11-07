from barbeshop.db.models.model_experts import Expert, DeletedExpert
from barbeshop.schemas.experts import CreateExpert, ReadExpert
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from barbeshop.db.redis_db import client

class ExpertDAO():
    def __init__(self, engine):
        self._engine = engine

    def _makesession(self):
        try:
            Session = sessionmaker(bind=self._engine)
            session = Session()
            return session
        except Exception as ex:
            print(f"Cant to make session because of: {ex}")

    def create_expert(self, expert: CreateExpert):
        with self._makesession() as session:
            deleted_expert = session.query(DeletedExpert).first()
            if deleted_expert:
                session.add(Expert(id=deleted_expert.id, name=expert.name))
                session.delete(deleted_expert)
            else:
                session.add(Expert(name=expert.name))
            session.commit()   
            return "Expert was sucessfully created."
        
    def return_experts(self):
        with self._makesession() as session:
            experts = session.query(Expert).all()
            if not experts:
                raise HTTPException(status_code=400, detail="Dont have any.")
            for expert in experts:
                yield expert

    def return_expert(self, expert_id: int):
        redis_expert = client.get_obj("experts", expert_id)
        if redis_expert:
            return ReadExpert(id=redis_expert["id"], name=redis_expert["name"])
        with self._makesession() as session:
            expert = session.query(Expert).get(expert_id)
            if not expert:
                raise HTTPException(status_code=400, detail="Expert not found.")
            client.add_hash_to_list("experts", ReadExpert(id=expert.id, name=expert.name).__dict__)
            return ReadExpert(id=expert.id, name=expert.name)
        
    def del_expert(self, expert_id: int):
        with self._makesession() as session:
            removable_expert = session.query(Expert).get(expert_id)
            if not removable_expert:
                raise HTTPException(status_code=400, detail="Expert not found.")        
            session.add(DeletedExpert(id=expert_id))
            session.delete(removable_expert)
            session.commit()
            return "Expert was sucessfully deleted."