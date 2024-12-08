# ПЕРЕДЕЛАТЬ

from tasks.celery import celery
from pydantic import EmailStr
from tasks.email_template import create_order_confirmation
import smtplib
from config import settings

password = settings.PASSWORD
user = settings.USER

@celery.task
def create_order_confirmation(order: dict, email_to: EmailStr):
    
    msg_content = create_order_confirmation(order, email_to)
    
    with smtplib.SMTP_SSL() as server:    #   Это потом надо доделать !!!!
        server.login(user=user, password=password)
        server.send_message(msg_content)