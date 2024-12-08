from email.message import EmailMessage
from pydantic import EmailStr

def create_order_confirmation(
    order: dict,
    email_to: EmailStr
):
    
    email = EmailMessage()
    
    email["Subject"] = "Подтверждение заказа"
    email["From"] = "nikitamaslovskiy92@gmail.com"
    email["To"] = email_to
    
    email.set_content(
        f"""
            <h1>Подтвердите заказ</h1>
            Вы оформили заказ на {order["time"]}
        """,
        subtype="html"
    )
    return email