import re
from dataclasses import dataclass
from typing import ClassVar

from domain.errors import DomainError, ErrorCodes


@dataclass(slots=True, frozen=True)
class TaxNumberVO:
    LENGTH = 8
    value: str

    def __post_init__(self):
        if not (len(self.value) != self.LENGTH):
            raise DomainError(ErrorCodes.INVALID_BUSINESS_TAX_NUMBER)


@dataclass(slots=True, frozen=True)
class DayOfWeekVO:
    FIRST_DAY: ClassVar[int] = 0
    LAST_DAY: ClassVar[int] = 6
    value: int

    def __post_init__(self):
        if not (
            isinstance(self.value, int)
            and (self.FIRST_DAY <= self.value <= self.LAST_DAY)
        ):
            raise DomainError(ErrorCodes.INVALID_DAY_OF_WEEK)


@dataclass(slots=True, frozen=True)
class PriceVO:
    MIN_VALUE = 0
    value: int

    def __post_init__(self):
        if self.value is None or self.value < self.MIN_VALUE:
            raise DomainError(ErrorCodes.INVALID_PRICE)



@dataclass(slots=True, frozen=True)
class GeoPointVO:
    lat: float
    lon: float

    def __post_init__(self):
        if not (
            (self.lat is not None and self.lon is not None)
            and (-90 <= self.lat <= 90)
            and (-180 <= self.lon <= 180)
        ):
            raise DomainError(ErrorCodes.INVALID_GEO_POINT)



@dataclass(slots=True, frozen=True)
class EmailVO:
    PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,7}$")

    value: str

    def __post_init__(self):
        if self.PATTERN is not None and not self.PATTERN.fullmatch(self.value):
            raise DomainError(ErrorCodes.INVALID_EMAIL)
        object.__setattr__(self, "value", self.value.lower())

@dataclass(slots=True, frozen=True)
class PasswordVO:
    value: str

    def __post_init__(self):
        if not self.value:
            raise DomainError(ErrorCodes.INVALID_PASSWORD_FORMAT)
