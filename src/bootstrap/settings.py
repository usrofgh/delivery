from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            Path(__file__).parent.parent.parent / "envs" / ".env.local.desktop"
        )
    )

    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int

    RABBITMQ_HOST: str
    RABBITMQ_VHOST: str
    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    RABBITMQ_PORT: int

    REDIS_HOST: str
    REDIS_PORT: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

    EMAIL_SENDER: str

    OTP_REGISTER_EXPIRATION_MINUTES: int
    OTP_RESEND_COOLDOWN_SECONDS: int
    OTP_RESEND_WINDOW_SECONDS: int
    OTP_MAX_RESENDS_IN_WINDOW: int
    OTP_MAX_VERIFY_ATTEMPTS: int
    OTP_LOCK_SECONDS: int

    @property
    def db_dsn(self) -> str:
        dsn = (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        return dsn

    @property
    def broker_dsn(self) -> str:
        return (
            f"pyamqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}"
            f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/{self.RABBITMQ_VHOST}"
        )



settings = Settings()
