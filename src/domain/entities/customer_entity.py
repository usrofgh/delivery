from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.value_objects.common import EmailVO, PhoneVO


@dataclass(slots=True, kw_only=True)
class CustomerEntity(BaseEntity):
    name: str
    email: EmailVO
    phone: PhoneVO
    hashed_password: str
