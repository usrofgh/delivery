from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity


@dataclass(slots=True, kw_only=True)
class MenuSectionEntity(BaseEntity):
    name: str
    photo_path: str | None = None
    business_id: UUID
