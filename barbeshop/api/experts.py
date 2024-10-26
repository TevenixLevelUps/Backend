from fastapi import APIRouter,  HTTPException
from barbeshop.schemas.experts import CreateExpert, ReadExpert
from barbeshop.db.db_connect import session
from barbeshop.db.models.model_experts import Expert, DeletedExpert

expert_router = APIRouter()

@expert_router.post("/experts/")
async def create_expert(expert: CreateExpert): 
    deleted_expert = session.query(DeletedExpert).first()
    id = lambda deleted_id: deleted_id if deleted_id else None
    session.add(Expert(id=id(deleted_expert.id), name=expert.name))
    if id(deleted_expert.id):
        session.delete(deleted_expert)
    session.commit()   
    return expert

@expert_router.get("/experts/")
async def read_experts():
    experts = session.query(Expert).all()
    if not experts:
        raise HTTPException(status_code=400, detail="Dont have any.")
    list_experts = []
    for expert in experts:
        list_experts.append(ReadExpert(id=expert.id, name=expert.name))
    return list_experts

@expert_router.get("/experts/{expert_id}")
async def read_expert(expert_id: int):
    expert = session.query(Expert).get(expert_id)
    if not expert:
        raise HTTPException(status_code=400, detail="Expert not found.")
    return ReadExpert(id=expert.id, name=expert.name)   

@expert_router.delete("/experts/{expert_id}")
async def del_expert(expert_id: int):
    removable_expert = session.query(Expert).get(expert_id)
    if not removable_expert:
        raise HTTPException(status_code=400, detail="Expert not found.")        
    session.add(DeletedExpert(id=expert_id))
    session.delete(removable_expert)
    session.commit()
    return "Expert was sucessfully deleted."