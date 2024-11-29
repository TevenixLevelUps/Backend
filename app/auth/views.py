from typing import Annotated

from fastapi import APIRouter, Depends, Form, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_helper import db_helper
from app.models.user import User

from . import service
from .dependencies import get_current_user
from .shemas import UserCreate, UserLogin

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await service.register_user(user, session)


@router.post("/confirm_email", status_code=status.HTTP_200_OK)
async def confirm_email(
    email: Annotated[str, Form()],
    code: Annotated[str, Form()],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await service.confirm_user_email(email, code, session)


@router.post("/login", status_code=status.HTTP_200_OK)
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


@router.get("/me", status_code=status.HTTP_200_OK)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
