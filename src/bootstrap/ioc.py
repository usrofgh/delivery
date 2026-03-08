from typing import AsyncGenerator

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio.engine import create_async_engine

from application.commands.customers.register_customer_handler import RegisterCustomerHandler
from domain.policies.otp_policy import OTPPolicy
from domain.ports.i_customer_repository import ICustomerRepository
from domain.ports.i_email_sender import IEmailSender
from domain.ports.i_hasher import IHasher
from domain.ports.i_otp_repository import IOTPRepository
from infrastracture.db.repositories.customer_repository import CustomerRepository
from infrastracture.db.repositories.otp_repository import OTPRepository
from infrastracture.messaging.email_sender import EmailSender
from infrastracture.security.password_hasher import PasswordHasher


class DBProvider(Provider):

    @provide(scope=Scope.APP)
    def engine(self) -> AsyncEngine:
        from bootstrap.settings import settings
        return create_async_engine(
            url=settings.db_dsn,
            # echo=True
        )

    @provide(scope=Scope.APP)
    def session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @provide(scope=Scope.REQUEST)
    async def session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncGenerator[AsyncSession]:
        async with session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()


class RepositoryProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def customer_repository(self, session: AsyncSession) -> ICustomerRepository:
        return CustomerRepository(session)

    @provide(scope=Scope.REQUEST)
    def otp_repository(self, session: AsyncSession) -> IOTPRepository:
        return OTPRepository(session)


class HandlerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def register_customer_handler(
        self,
        customer_repository: ICustomerRepository,
        otp_repository: IOTPRepository,
        email_sender: IEmailSender,
        hasher: IHasher,
        register_otp_policy: OTPPolicy
    ) -> RegisterCustomerHandler:
        return RegisterCustomerHandler(
            customer_repository,
            otp_repository,
            email_sender,
            hasher,
            register_otp_policy
        )


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    def password_hasher(self) -> IHasher:
        return PasswordHasher()

    @provide(scope=Scope.APP)
    def email_sender(self) -> IEmailSender:
        return EmailSender()

    @provide(scope=Scope.APP)
    def register_otp_policy(self) -> OTPPolicy:
        from bootstrap.settings import settings
        policy = OTPPolicy(
            settings.OTP_MAX_RESENDS_IN_WINDOW,
            settings.OTP_RESEND_WINDOW_SECONDS,
            settings.OTP_RESEND_COOLDOWN_SECONDS,
            settings.OTP_REGISTER_EXPIRATION_MINUTES
        )
        return policy
