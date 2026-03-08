import asyncio
from dataclasses import dataclass
from datetime import datetime, UTC, timedelta
from domain.entities.customer_entity import CustomerEntity
from domain.entities.otp_entity import OTPEntity
from domain.enums.account_status import AccountStatus
from domain.enums.actor_type import ActorType
from domain.enums.otp_purpose_type import OTPPurposeType
from domain.errors import DomainError, ErrorCodes
from domain.policies.otp_policy import OTPPolicy
from domain.policies.password_policy import assert_password_strong
from domain.ports.i_customer_repository import ICustomerRepository
from domain.ports.i_email_sender import IEmailSender
from domain.ports.i_hasher import IHasher
from domain.ports.i_otp_repository import IOTPRepository
from domain.services.otp_generator import generate_otp
from domain.value_objects.common import EmailVO, PasswordVO
from domain.value_objects.otp_vo import OTPHashVO


@dataclass(slots=True, frozen=True)
class RegisterCustomerHandler:
    customer_repository: ICustomerRepository
    otp_repository: IOTPRepository
    email_sender: IEmailSender
    hasher: IHasher
    otp_policy: OTPPolicy

    async def __call__(
        self,
        name: str,
        email: str,
        password: str
    ) -> None:
        assert_password_strong(password)
        hashed_password = self.hasher.hash(password)
        customer_entity = CustomerEntity(
            name=name,
            email=EmailVO(email),
            status=AccountStatus.PENDING,
            hashed_password=PasswordVO(hashed_password)
        )

        duplicate_error = False
        try:
            await self.customer_repository.save(customer_entity)
        except DomainError as ex:
            if ex.args[0] == ErrorCodes.EMAIL_ALREADY_EXISTS:
                duplicate_error = True
            else:
                raise

        if not duplicate_error:
            now = datetime.now(tz=UTC)
            expires_at = now + timedelta(minutes=self.otp_policy.otp_register_expiration_minutes)
            last_sent_at = now

            otp = generate_otp()
            otp_entity = OTPEntity(
                otp_hash=OTPHashVO(self.hasher.hash(otp)),
                actor_id=customer_entity.id,
                actor_type=ActorType.CUSTOMER,
                purpose=OTPPurposeType.REGISTER_EMAIL_CONFIRM,
                resend_count=0,
                attempts=0,
                last_sent_at=last_sent_at,
                resend_window_started_at=now,
                locked_until=None,
                expires_at=expires_at,
                policy=self.otp_policy
            )
            await self.otp_repository.save(otp_entity)
            await self.email_sender.send_otp_register_email(to=email, otp=otp)
        elif duplicate_error:
            db_customer = await self.customer_repository.get_by_email(email)

            decisions = {
                AccountStatus.DELETING: self.email_sender.send_register_email_deleting_account,
                AccountStatus.BANNED: self.email_sender.send_register_email_banned_account,
                AccountStatus.ACTIVE: self.email_sender.send_register_email_active_account
            }

            req_decision = decisions.get(db_customer.status)
            if req_decision:
                await req_decision(email)

            elif db_customer.status == AccountStatus.PENDING:
                otp_db_entity = await self.otp_repository.get_by_actor_purpose(
                    actor_id=db_customer.id,
                    actor_type=ActorType.CUSTOMER,
                    purpose=OTPPurposeType.REGISTER_EMAIL_CONFIRM,
                    otp_policy=self.otp_policy
                )

                otp_db_entity.normalize_resend_window()
                if not otp_db_entity.is_can_resend():
                    await asyncio.sleep(0.1, 0.3)  # Task sending delay imitating
                    return
                else:
                    new_otp = generate_otp()
                    new_otp_hash = OTPHashVO(self.hasher.hash(new_otp))
                    otp_db_entity.rotate_otp(new_otp_hash)
                    await self.otp_repository.update(otp_db_entity)
                    await self.email_sender.send_otp_register_email(email, new_otp)
