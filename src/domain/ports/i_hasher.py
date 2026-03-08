from abc import ABC, abstractmethod


class IHasher(ABC):
    @abstractmethod
    def hash(self, string: str) -> str:
        ...

    @abstractmethod
    def verify(self, string: str, string_hash: str) -> bool:
        ...
