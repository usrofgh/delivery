import re
from dataclasses import dataclass
from typing import ClassVar

from domain.errors import DomainError, ErrorCodes


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
