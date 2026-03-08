from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.entities.order_status_history import OrderStatusHistoryEntity
from domain.enums.actor_type import ActorType
from domain.enums.change_status_reason import ChangeStatusReason
from domain.enums.order_status import OrderStatus


@dataclass(slots=True, kw_only=True)
class OrderEntity(BaseEntity):
    status: OrderStatus
    customer_id: UUID
    business_id: UUID
    shop_id: UUID
    delivery_id: UUID
    payment_id: UUID

    def change_status(
        self,
        *,
        to_status: OrderStatus,
        actor_type: ActorType,
        reason: ChangeStatusReason,
        comment: str = "",
    ) -> OrderStatusHistoryEntity:
        from_status = self.status
        # assert_can_change(from_status, to_status)

        self.status = to_status

        return OrderStatusHistoryEntity(
            order_id=self.id,
            from_status=from_status,
            to_status=to_status,
            actor_type=actor_type,
            reason=reason,
            comment=comment,
        )
