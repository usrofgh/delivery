from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.customer_entity import CustomerEntity


class ICustomerRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: UUID) -> CustomerEntity | None:
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> CustomerEntity | None:
        ...


    @abstractmethod
    async def save(self, entity: CustomerEntity) -> None:
        ...

    @abstractmethod
    async def remove(self, id: UUID) -> None:
        ...
