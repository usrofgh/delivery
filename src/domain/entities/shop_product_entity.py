from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity


@dataclass(slots=True, kw_only=True)
class ShopProductEntity(BaseEntity):
    stock_quantity: int
    is_enabled: bool
    product_id: UUID
    shop_id: UUID


