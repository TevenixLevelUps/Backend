from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import jwt
from .shemas import TokenData
from .utils import get_private_key, get_public_key, get_algorithm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from models.token import Token
import logging

timezone = ZoneInfo("Europe/Moscow")

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

ALGORITHM = get_algorithm()


async def create_access_token(data: dict, session: AsyncSession):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    to_encode["sub"] = str(to_encode["sub"])  # Преобразование user_id в строку
    private_key = get_private_key()
    encoded_jwt = jwt.encode(to_encode, private_key, algorithm=ALGORITHM)
    db_token = Token(
        access_token=encoded_jwt,
        token_type="bearer",
        expiry_time=expire,
        user_id=int(to_encode["sub"]),
    )
    session.add(db_token)
    await session.commit()
    logger.info(f"Access token created and stored in DB: {encoded_jwt}")
    return encoded_jwt


async def verify_token(token: str, credentials_exception, session: AsyncSession):
    credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Exception in verify_token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Error in decode ",
        headers={"WWW-Authenticate": "Bearer"},
    )
    error2 = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Error in db request",
        headers={"WWW-Authenticate": "Bearer"},
    )

    error3 = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Error, token not found",
        headers={"WWW-Authenticate": "Bearer"},
    )

    error4 = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Error, expired",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        public_key = get_public_key()
        try:
            payload = jwt.decode(token, public_key, algorithms=ALGORITHM)
            logger.info(f"Decoded payload: {payload}")
        except jwt.ExpiredSignatureError as e:
            logger.error(f"Expired signature error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.DecodeError as e:
            logger.error(f"Decode error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token decode error",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            logger.error(f"Unknown decode error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unknown decode error",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id: int = int(payload.get("sub"))
        logger.info(f"User ID from token: {user_id}")

        try:
            db_token = await session.execute(
                select(Token).where(Token.user_id == user_id)
            )
            db_token = db_token.scalars().first()
            logger.info(f"Token from DB: {db_token}")
        except Exception as e:
            logger.error(f"DB request error: {e}")
            raise error2

        if db_token is None:
            logger.error("Token not found in DB")
            raise error3

        if db_token.expiry_time < datetime.now():
            logger.error("Token expired")
            raise error4

        token_data = TokenData(user_id=user_id, email="")
        logger.info(f"Returning token data: {token_data}")

    except jwt.PyJWTError:
        logger.error("JWT error")
        raise credentials_exception

    return token_data
