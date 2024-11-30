import os

from dotenv import load_dotenv

load_dotenv()


def get_smtp_port():
    return int(os.getenv("SMTP_PORT"))


def get_smtp_server():
    return os.getenv("SMTP_SERVER")


def get_smtp_username():
    return os.getenv("SMTP_USERNAME")


def get_smtp_password():
    return os.getenv("SMTP_PASSWORD")
