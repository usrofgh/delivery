from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.value_objects.common import GeoPointVO


@dataclass(slots=True, kw_only=True)
class CourierLocationHistoryEntity(BaseEntity):
    courier_id: UUID
    geom: GeoPointVO
