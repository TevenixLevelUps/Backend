from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)  # Обновлено для использования AsyncSession
from . import jwt
from database.db_helper import db_helper
from sqlalchemy import Select
from models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(db_helper.scoped_session_dependency),
):  # Исправлено на AsyncSession
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = jwt.verify_token(token, credentials_exception)
    stmt = Select(User).where(User.email == token_data.email)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user
