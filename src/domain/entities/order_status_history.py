from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.enums.actor_type import ActorType
from domain.enums.change_status_reason import ChangeStatusReason
from domain.enums.order_status import OrderStatus


@dataclass(slots=True, kw_only=True)
class OrderStatusHistoryEntity(BaseEntity):
    order_id: UUID
    from_status: OrderStatus
    to_status: OrderStatus
    actor_type: ActorType
    reason: ChangeStatusReason
    comment: str
