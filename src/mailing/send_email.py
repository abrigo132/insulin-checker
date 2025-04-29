from email.message import EmailMessage
import aiosmtplib
from aiosmtplib.errors import SMTPException

from core import settings


async def send_email(recipient: str, subject: str, body: str) -> None:
    admin_email = settings.smtp.host

    message: EmailMessage = EmailMessage()
    message["From"] = admin_email
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)
    try:
        async with aiosmtplib.SMTP(
            hostname=settings.smtp.server,
            port=settings.smtp.port,
            timeout=10,
            username=admin_email,
            password=settings.smtp.password,
            use_tls=True,
        ) as smtp_connect:
            await smtp_connect.send_message(
                message,
                sender=admin_email,
                recipients=[recipient],
            )
    except SMTPException:
        print("Ошибка со стороны SMTP")
