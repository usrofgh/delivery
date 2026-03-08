from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity


@dataclass(slots=True, kw_only=True)
class ShopEntity(BaseEntity):
    is_active: bool
    business_id: UUID
    location_id: UUID
