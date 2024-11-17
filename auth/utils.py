import os
from dotenv import load_dotenv

load_dotenv()


def get_private_key():
    return os.getenv("PRIVATE_KEY")


def get_public_key():
    return os.getenv("PUBLIC_KEY")


def get_algorithm():
    return os.getenv("ALGORITHM")


def get_access_token_exp_min():
    return int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
