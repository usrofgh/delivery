from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.enums.actor_type import ActorType
from domain.enums.change_status_reason import ChangeStatusReason
from domain.enums.delivery_status import DeliveryStatus


@dataclass(slots=True, kw_only=True)
class DeliveryStatusHistoryEntity(BaseEntity):
    delivery_id: UUID
    from_status: DeliveryStatus
    to_status: DeliveryStatus
    actor_type: ActorType
    reason: ChangeStatusReason
    comment: str
