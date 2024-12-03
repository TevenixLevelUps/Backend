from fastapi import Cookie, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_helper import db_helper
from app.exceptions import TokenHTTPException
from app.models.user import User

from . import jwt
from .shemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    authorization: str = Header(None),
    access_token: str = Cookie(None),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):

    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    elif access_token:
        token = access_token

    if not token:
        raise TokenHTTPException.credentials_exception

    token_data: TokenData = await jwt.verify_token(
        token, TokenHTTPException.credentials_exception, session
    )

    stmt = Select(User).where(User.id == token_data.user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user is None:

        raise TokenHTTPException.credentials_exception

    return user


async def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise TokenHTTPException.admin_role_exception
    return current_user
