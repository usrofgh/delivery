from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from domain.enums.account_status import AccountStatus
from infrastracture.db.models.base_model import BaseModel


class CustomerModel(BaseModel):
    __tablename__ = "customers"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    status: Mapped[AccountStatus]
    activated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
