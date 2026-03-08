from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity


@dataclass(slots=True, kw_only=True)
class CustomerAddressEntity(BaseEntity):
    label: str | None = None
    floor: int | None = None
    flat: int | None = None
    door: int | None = None
    comment: str | None = None
    is_default: bool

    customer_id: UUID
    location_id: UUID
