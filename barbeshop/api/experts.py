from barbeshop.addition.functions import gener_id_from_list
from barbeshop.database import list_experts
from fastapi import APIRouter,  HTTPException
from barbeshop.schemas.experts import Expert

expert_router = APIRouter()

@expert_router.post("/")
async def create_expert(expert: Expert): 
    id = gener_id_from_list(list_experts)
    expert.id = id
    list_experts[id] = expert
    return expert

@expert_router.get("/")
async def read_experts():
    return list_experts

@expert_router.get("/{expert_id}")
async def read_expert(expert_id: int):
    try:
        return list_experts[expert_id]
    except Exception:
        raise HTTPException(status_code=400, detail="Expert not found.")

@expert_router.delete("/{expert_id}")
async def del_expert(expert_id: int):
    try:
        del list_experts[expert_id]
        return list_experts
    except Exception:
        raise HTTPException(status_code=400, detail="Expert not found.")        