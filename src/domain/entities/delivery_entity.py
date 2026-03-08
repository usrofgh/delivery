from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.enums.delivery_status import DeliveryStatus


@dataclass(slots=True, kw_only=True)
class DeliveryEntity(BaseEntity):
    courier_id: UUID
    customer_address_id: UUID
    status: DeliveryStatus