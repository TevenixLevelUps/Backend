import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from http.client import HTTPException
from typing import List, Union

from dulwich.porcelain import status
from fastapi import HTTPException, status

from .utils import get_smtp_password, get_smtp_port, get_smtp_server, get_smtp_username


def send_email(
    subject: str,
    body: str,
    recipients: Union[List[str], str],
):
    if isinstance(recipients, str):
        recipients = [recipients]
    elif not isinstance(recipients, list) or not all(
        isinstance(r, str) for r in recipients
    ):
        raise ValueError("Recipients must be a list of strings or a single string.")

    sender_email = get_smtp_username()
    sender_password = get_smtp_password()
    smtp_server = get_smtp_server()
    smtp_port = get_smtp_port()

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipients, message.as_string())
            print(f"Email sent successfully to {recipients}")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to send email, {e}",
        )
