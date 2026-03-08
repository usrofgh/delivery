from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.value_objects.common import TaxNumberVO
from domain.value_objects.common import EmailVO


@dataclass(slots=True, kw_only=True)
class BusinessEntity(BaseEntity):
    name: str
    legal_name: str
    legal_address: str
    description: str
    tax_number: TaxNumberVO
    email: EmailVO
