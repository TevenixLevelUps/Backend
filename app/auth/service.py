import uuid

from fastapi import Response
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Token
from app.models.user import User
from app.notifications import send_email

from ..exceptions import TokenHTTPException, UserHTTPException
from . import jwt
from .shemas import PasswordReset, UserCreate, UserLogin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_confirmation_code():
    return str(uuid.uuid4())


async def register_user(user: UserCreate, session: AsyncSession):
    stmt = Select(User).where(User.email == user.email)
    result = await session.execute(stmt)
    db_user = result.scalars().first()

    if db_user:
        raise UserHTTPException.email_already_registered

    hashed_password = pwd_context.hash(user.password)
    confirmation_code = generate_confirmation_code()
    title: str = "Confirmation code"
    send_email(recipients=user.email, body=str(confirmation_code), subject=title)

    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        confirmation_code=confirmation_code,
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return {"message": "Confirmation code sent to your email"}


async def confirm_user_email(email: str, code: str, session: AsyncSession):
    stmt = Select(User).where(User.email == email)
    result = await session.execute(stmt)
    db_user = result.scalars().first()

    if db_user is None or db_user.confirmation_code != code:
        raise UserHTTPException.email_already_registered

    db_user.is_confirmed = True
    db_user.confirmation_code = None
    session.add(db_user)
    await session.commit()
    return {"message": "Email confirmed"}


async def login_user(user: UserLogin, session: AsyncSession, response: Response):
    stmt = Select(User).where(User.email == user.email)
    result = await session.execute(stmt)
    db_user = result.scalars().first()

    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise UserHTTPException.incorrect_credentials

    if not db_user.is_confirmed:
        raise UserHTTPException.email_not_confirmed

    access_token = await jwt.create_access_token(
        data={"sub": db_user.id}, session=session
    )

    title: str = "LOGIN"
    body: str = "You have successfully logged in!"
    send_email(subject=title, body=body, recipients=user.email)
    response.set_cookie(key="access_token", value=access_token, httponly=True)

    response.headers["Authorization"] = f"Bearer {access_token}"

    return {"message": "Logged in successfully"}


async def logout_user(session: AsyncSession, response: Response, user: User):

    if user is None:
        raise UserHTTPException.not_logged_in

    stmt = Select(Token).where(Token.user_id == user.id)
    result = await session.execute(stmt)
    db_token = result.scalars().first()

    if db_token:
        await session.delete(db_token)
        await session.commit()

    else:
        raise TokenHTTPException.token_not_found_error

    response.delete_cookie(key="access_token")

    return {
        "message": "Logged out successfully",
    }


async def reset_password_request(
    email: EmailStr,
    session: AsyncSession,
):
    stmt = Select(User).where(User.email == email)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if not user:
        raise UserHTTPException.email_not_registered

    reset_code = generate_confirmation_code()
    user.confirmation_code = reset_code
    session.add(user)
    await session.commit()

    title = "Password Reset Request"
    body = f"Your password reset code is: {reset_code}"
    send_email(recipients=user.email, body=body, subject=title)

    return {"message": "Password reset code sent to your email"}


async def reset_password(data: PasswordReset, session: AsyncSession):
    stmt = Select(User).where(User.email == data.email)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if not user:
        raise UserHTTPException.email_not_registered

    if user.confirmation_code != data.reset_code:
        raise UserHTTPException.invalid_confirmation_code

    user.hashed_password = pwd_context.hash(data.new_password)
    user.confirmation_code = None
    session.add(user)
    await session.commit()
    title = "Password was reset successfully"
    body = f"Your password  was reset successfully!,if you did not do this, contact support"
    send_email(recipients=user.email, body=body, subject=title)

    return {"message": "Password was reset successfully"}
