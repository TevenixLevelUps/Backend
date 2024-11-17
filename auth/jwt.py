from datetime import datetime, timedelta
import jwt
from .shemas import TokenData
from .utils import (
    get_private_key,
    get_public_key,
    get_access_token_exp_min,
    get_algorithm,
)  # Новые функции для чтения ключей

ACCESS_TOKEN_EXPIRE_MINUTES = get_access_token_exp_min()
ALGORITHM = get_algorithm()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    private_key = get_private_key()
    encoded_jwt = jwt.encode(
        to_encode, private_key, algorithm=ALGORITHM
    )  # Используем приватный ключ
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        public_key = get_public_key()
        payload = jwt.decode(
            token, public_key, algorithms=[ALGORITHM]
        )  # Используем публичный ключ
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.PyJWTError:
        raise credentials_exception
    return token_data
