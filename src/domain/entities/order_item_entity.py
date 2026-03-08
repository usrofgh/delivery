from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.enums.order_status import OrderStatus


@dataclass(slots=True, kw_only=True)
class OrderItemEntity(BaseEntity):
    status: OrderStatus
    price: int
    order_id: UUID
    product_id: UUID
