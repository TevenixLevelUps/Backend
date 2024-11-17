from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .shemas import UserCreate, UserLogin, Token
from database.db_helper import db_helper
from .service import register_user, confirm_user_email, login_user, simple_login_user


router = APIRouter()


@router.post("/register")
async def register(
    user: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):  # Исправлено на AsyncSession и вызов scoped_session_dependency
    return await register_user(user, session)


@router.post("/confirm_email")
async def confirm_email(
    email: str,
    code: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):  # Исправлено на AsyncSession и вызов scoped_session_dependency
    return await confirm_user_email(email, code, session)


@router.post("/login")
async def login(
    user: UserLogin,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):  # Исправлено на AsyncSession и вызов scoped_session_dependency
    return await login_user(user, session)


@router.post("/simple_login", response_model=Token)
async def simple_login(
    user: UserLogin,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):  # Исправлено на AsyncSession и вызов scoped_session_dependency
    return await simple_login_user(user, session)
