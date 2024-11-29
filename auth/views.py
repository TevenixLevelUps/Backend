from typing import Annotated

from fastapi import APIRouter, Depends, Form, Response
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_helper import db_helper
from models.user import User

from . import service
from .dependencies import get_current_user
from .shemas import UserCreate, UserLogin

router = APIRouter()


@router.post("/register")
async def register(
    user: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await service.register_user(user, session)


@router.post("/confirm_email")
async def confirm_email(
    email: Annotated[str, Form()],
    code: Annotated[str, Form()],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await service.confirm_user_email(email, code, session)


@router.post("/login")
async def login(
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    response: Response,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = UserLogin(email=email, password=password)
    return await service.login_user(user, session, response)


@router.post("/log_out")
async def logout(
    response: Response,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    user: User = Depends(get_current_user),
):
    return await service.logout_user(session=session, user=user, response=response)


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
