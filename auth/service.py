import uuid
import smtplib
from email.mime.text import MIMEText
from fastapi import HTTPException, status
from sqlalchemy import Select  # Изменено import для select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from . import jwt
from .shemas import UserLogin, UserCreate
from models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_confirmation_code():
    return str(uuid.uuid4())


def send_confirmation_email(email: str, confirmation_code: str):
    smtp_server = "smtp.your_email_provider.com"
    smtp_port = 587
    smtp_username = "your_email@example.com"
    smtp_password = "your_password"

    message = MIMEText(f"Your confirmation code is {confirmation_code}")
    message["Subject"] = "Email Confirmation"
    message["From"] = smtp_username
    message["To"] = email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, [email], message.as_string())


async def register_user(user: UserCreate, session: AsyncSession):
    stmt = Select(User).where(User.email == user.email)
    result = await session.execute(stmt)
    db_user = result.scalars().first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = pwd_context.hash(user.password)
    confirmation_code = generate_confirmation_code()
    send_confirmation_email(user.email, confirmation_code)
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid confirmation code",
        )
    db_user.is_confirmed = True
    db_user.confirmation_code = None  # Remove the confirmation code after confirmation
    session.add(db_user)
    await session.commit()
    return {"message": "Email confirmed"}


async def login_user(user: UserLogin, session: AsyncSession):
    stmt = Select(User).where(User.email == user.email)  # Изменено на select
    result = await session.execute(stmt)
    db_user = result.scalars().first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not db_user.is_confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not confirmed",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = jwt.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


async def simple_login_user(user: UserLogin, session: AsyncSession):
    stmt = Select(User).where(User.email == user.email)
    result = await session.execute(stmt)
    db_user = result.scalars().first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not db_user.is_confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not confirmed",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = jwt.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
