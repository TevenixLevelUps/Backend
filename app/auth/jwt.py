import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.logging_conf import configure_logging
from app.models.token import Token

from ..exceptions import TokenHTTPException
from .shemas import TokenData
from .utils import get_algorithm, get_private_key, get_public_key

timezone = ZoneInfo("Europe/Moscow")


logger = configure_logging(logging.INFO)

ALGORITHM = get_algorithm()


async def create_access_token(data: dict, session: AsyncSession):
    user_id = data["sub"]
    try:
        old_tokens = await session.execute(
            select(Token).where(Token.user_id == user_id)
        )
        old_token = old_tokens.scalars().first()
        if old_token:
            await session.delete(old_token)
        await session.commit()
        logger.info(f"Deleted old token for user_id {user_id}")
    except Exception as e:
        (logger.error(f"Error deleting old token for user_id {user_id}: {e}"))

    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    to_encode["sub"] = str(user_id)
    private_key = get_private_key()
    encoded_jwt = jwt.encode(to_encode, private_key, algorithm=ALGORITHM)
    db_token = Token(
        access_token=encoded_jwt,
        token_type="bearer",
        expiry_time=expire,
        user_id=user_id,
    )
    session.add(db_token)
    await session.commit()
    logger.info(f"Access token created and stored in DB: {encoded_jwt}")
    return encoded_jwt


async def verify_token(token: str, credentials_exception, session: AsyncSession):

    try:
        public_key = get_public_key()
        try:
            payload = jwt.decode(token, public_key, algorithms=ALGORITHM)
            logger.info(f"Decoded payload: {payload}")
        except jwt.ExpiredSignatureError as e:
            logger.error(f"Expired signature error: {e}")
            raise TokenHTTPException.expired_token_error
        except jwt.DecodeError as e:
            logger.error(f"Decode error: {e}")
            raise TokenHTTPException.decode_error
        except Exception as e:
            logger.error(f"Unknown decode error: {e}")
            raise TokenHTTPException.decode_error

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
            raise TokenHTTPException.db_error

        if db_token is None:
            logger.error("Token not found in DB")
            raise TokenHTTPException.token_not_found_error

        if db_token.expiry_time < datetime.now():
            logger.error("Token expired")
            raise TokenHTTPException.expired_token_error

        token_data = TokenData(user_id=user_id, email="")
        logger.info(f"Returning token data: {token_data}")

    except jwt.PyJWTError:
        logger.error("JWT error")
        raise credentials_exception

    return token_data
