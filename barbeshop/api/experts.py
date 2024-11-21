from fastapi import APIRouter
from barbeshop.schemas.experts import CreateExpert
from barbeshop.db.postgresql_db import engine
from barbeshop.dao.dao_experts import ExpertDAO
from barbeshop.rate_limiter import rate_limiter

expert_router = APIRouter()
expert_dao = ExpertDAO(engine=engine)

@expert_router.post("/experts/")
async def create_expert(expert: CreateExpert): 
        if rate_limiter.compare_count("admin"):
            return expert_dao.create_expert(expert=expert)

@expert_router.get("/experts/")
async def read_experts():
        if rate_limiter.compare_count("admin"):
            return expert_dao.return_experts()

@expert_router.get("/experts/{expert_id}")
async def read_expert(expert_id: int):
        if rate_limiter.compare_count("admin"):
            return  expert_dao.return_expert(expert_id=expert_id)

@expert_router.delete("/experts/{expert_id}")
async def del_expert(expert_id: int):
        if rate_limiter.compare_count("admin"):
            return expert_dao.del_expert(expert_id=expert_id)