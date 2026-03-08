from pwdlib import PasswordHash

from domain.ports.i_hasher import IHasher


class PasswordHasher(IHasher):
    def __init__(self) -> None:
        self._ph = PasswordHash.recommended()

    def hash(self, string: str) -> str:
        return self._ph.hash(string)

    def verify(self, string: str, string_hash: str) -> bool:
        return self._ph.verify(string, string_hash)
