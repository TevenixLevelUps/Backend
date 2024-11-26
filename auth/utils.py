import os

from dotenv import load_dotenv

load_dotenv()


def get_private_key():
    with open("jwt-private.pem", "r") as f:
        return f.read()


def get_public_key():
    with open("jwt-public.pem", "r") as f:
        return f.read()


def get_algorithm():
    return os.getenv("ALGORITHM")


def get_access_token_exp_min():
    return int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
