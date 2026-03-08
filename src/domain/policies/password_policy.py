import re
from domain.errors import DomainError, ErrorCodes

_PATTERN = re.compile(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[#?!@$%^&*\-]).{8,}$")


def assert_password_strong(password: str) -> None:
    if not _PATTERN.fullmatch(password):
        raise DomainError(ErrorCodes.INVALID_PASSWORD_FORMAT)
