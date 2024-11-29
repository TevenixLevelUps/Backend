import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def get_private_key():
    file_path = Path(__file__).parent.parent.parent / "jwt-private.pem"
    with open(file_path, "r") as f:
        return f.read()


def get_public_key():
    file_path = Path(__file__).parent.parent.parent / "jwt-public.pem"
    with open(file_path, "r") as f:
        return f.read()


def get_algorithm():
    return os.getenv("ALGORITHM")


def get_access_token_exp_min():
    return int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
