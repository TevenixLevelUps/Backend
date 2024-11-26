from fastapi import APIRouter, Depends, Response, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

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
    email: Annotated[str, Form()],
    code: Annotated[str, Form()],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await confirm_user_email(email, code, session)


@router.post("/login")
async def login(
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    response: Response,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = UserLogin(email=email, password=password)
    return await login_user(user, session, response)


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
