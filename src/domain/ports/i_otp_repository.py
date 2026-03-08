from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.otp_entity import OTPEntity
from domain.enums.actor_type import ActorType
from domain.enums.otp_purpose_type import OTPPurposeType
from domain.policies.otp_policy import OTPPolicy


class IOTPRepository(ABC):
    @abstractmethod
    async def save(self, entity: OTPEntity) -> None:
        ...

    @abstractmethod
    async def update(self, entity: OTPEntity) -> None:
        ...

    @abstractmethod
    async def get_by_actor_purpose(
        self,
        actor_id: UUID,
        actor_type: ActorType,
        purpose: OTPPurposeType,
        otp_policy: OTPPolicy,
    ) -> OTPEntity:
        pass
