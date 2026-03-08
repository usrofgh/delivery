from dataclasses import dataclass
from datetime import datetime

from domain.entities.base import BaseEntity
from domain.enums.city import City
from domain.enums.delivery_type import DeliveryType
from domain.value_objects.common import EmailVO, GeoPointVO


@dataclass(slots=True, kw_only=True)
class CourierEntity(BaseEntity):
    first_name: str
    last_name: str
    paternal_name: str
    email: EmailVO
    city: City
    vehicle: DeliveryType
    avatar_path: str | None = None
    is_accessible: bool
    is_online: bool
    curr_log_geom: GeoPointVO
    last_seen_at: datetime
    hashed_password: str
