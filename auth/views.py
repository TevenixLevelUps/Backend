from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_helper import db_helper
from models.user import User

from .dependencies import get_current_user
from .service import confirm_user_email, login_user, register_user
from .shemas import UserCreate, UserLogin

router = APIRouter()


@router.post("/register")
async def register(
    user: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await register_user(user, session)


@router.post("/confirm_email")
async def confirm_email(
    email: str,
    code: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await confirm_user_email(email, code, session)


@router.post("/login")
async def login(
    user: UserLogin,
    response: Response,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await login_user(user, session, response)


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
