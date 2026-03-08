from dataclasses import dataclass

from domain.errors import DomainError, ErrorCodes


@dataclass(slots=True, frozen=True)
class OTPHashVO:
    value: str

    def __post_init__(self):
        if not self.value:
            raise DomainError(ErrorCodes.INVALID_OTP_FORMAT)
