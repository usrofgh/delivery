from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.enums.inventory_type import InventoryType
from domain.value_objects.common import PriceVO


@dataclass(slots=True, kw_only=True)
class ProductEntity(BaseEntity):
    name: str
    price: PriceVO
    photo_path: str | None = None
    inventory_type: InventoryType
    category_id: UUID
    menu_section_id: UUID
