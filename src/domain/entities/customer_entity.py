from dataclasses import dataclass
from datetime import datetime

from domain.entities.base import BaseEntity
from domain.enums.account_status import AccountStatus
from domain.value_objects.common import EmailVO, PasswordVO


@dataclass(slots=True, kw_only=True)
class CustomerEntity(BaseEntity):
    name: str
    email: EmailVO
    status: AccountStatus
    hashed_password: PasswordVO
    activated_at: datetime | None = None
