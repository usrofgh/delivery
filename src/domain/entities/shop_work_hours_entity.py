from dataclasses import dataclass
from datetime import time
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.errors import DomainError, ErrorCodes
from domain.value_objects.common import DayOfWeekVO


@dataclass(slots=True, kw_only=True)
class ShopWorkHoursEntity(BaseEntity):
    day_of_week: DayOfWeekVO
    opened_at: time
    closed_at: time
    shop_id: UUID

    def __post_init__(self):
        if not (self.opened_at < self.closed_at):
            raise DomainError(ErrorCodes.INVALID_WORK_HOURS)
