from dataclasses import dataclass

from domain.entities.base import BaseEntity


@dataclass(slots=True, kw_only=True)
class CategoryEntity(BaseEntity):
    name: str
    photo_path: str | None = None
