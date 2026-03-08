from domain.ports.i_email_sender import IEmailSender
from infrastracture.celery_tasks.email_tasks import send_email_msg_task


class EmailSender(IEmailSender):
    async def send_otp_register_email(self, to: str, otp: str) -> None:
        send_email_msg_task.delay(
            to=to,
            subject="Confirm registration",
            body=f"OTP Code: {otp}"
        )

    async def send_register_email_deleting_account(self, to: str) -> None:
        subject = "Registration request"
        body = "We got a registration request on your email. If you want to restore your account - contact our support"
        send_email_msg_task.delay(
            to=to,
            subject=subject,
            body=body
        )

    async def send_register_email_banned_account(self, to: str) -> None:
        subject = "Registration request"
        body = "We got a registration request on your email. Your account is banned"
        send_email_msg_task.delay(
            to=to,
            subject=subject,
            body=body
        )

    async def send_register_email_active_account(self, to: str) -> None:
        subject = "Registration request"
        body = (
            "We got a registration request on your email. You have an account on this email. "
            "You can reset the password if you forgot"
        )
        send_email_msg_task.delay(
            to=to,
            subject=subject,
            body=body
        )
