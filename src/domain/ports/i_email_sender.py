from abc import ABC, abstractmethod


class IEmailSender(ABC):
    @abstractmethod
    async def send_otp_register_email(self, to: str, otp: str) -> None:
        pass

    @abstractmethod
    async def send_register_email_deleting_account(self, to: str) -> None:
        pass

    @abstractmethod
    async def send_register_email_banned_account(self, to: str) -> None:
        pass

    @abstractmethod
    async def send_register_email_active_account(self, to: str) -> None:
        pass
