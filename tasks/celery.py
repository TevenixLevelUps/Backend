from celery import Celery
from config import settings

celery = Celery(
    "tasks",
    broker=settings.BROKER,
    include=["tasks.tasks"]
)