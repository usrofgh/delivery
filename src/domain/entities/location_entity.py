from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.value_objects.common import GeoPointVO


@dataclass(slots=True, kw_only=True)
class LocationEntity(BaseEntity):
    address_text: str
    geom: GeoPointVO
