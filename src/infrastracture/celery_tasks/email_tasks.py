import smtplib

from email.message import EmailMessage

from bootstrap.celery_app import celery_app
from bootstrap.settings import settings


@celery_app.task(bind=True, max_retries=3)
def send_email_msg_task(self, to: str, subject: str, body: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_SENDER
    msg["To"] = to
    msg.set_content(body)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
