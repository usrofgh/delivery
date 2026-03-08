from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.entities.otp_entity import OTPEntity
from domain.enums.actor_type import ActorType
from domain.enums.otp_purpose_type import OTPPurposeType
from domain.errors import DomainError, ErrorCodes
from domain.policies.otp_policy import OTPPolicy
from domain.ports.i_otp_repository import IOTPRepository
from domain.value_objects.otp_vo import OTPHashVO
from infrastracture.db.models.otp_model import OTPModel


class OTPRepository(IOTPRepository):
    MODEL = OTPModel

    def __init__(self, db: AsyncSession):
        self._db = db

    async def save(self, entity: OTPEntity) -> None:
        model = self._to_orm(entity)
        try:
            self._db.add(model)
            await self._db.flush()
        except IntegrityError as err:
            if "email" in err.args[0]:
                raise DomainError(ErrorCodes.EMAIL_ALREADY_EXISTS) from err
            raise

    async def update(self, entity: OTPEntity) -> None:
        await self._db.merge(self._to_orm(entity))

    async def get_by_actor_purpose(
        self,
        actor_id: UUID,
        actor_type: ActorType,
        purpose: OTPPurposeType,
        otp_policy: OTPPolicy,
    ) -> OTPEntity | None:
        stmt = select(self.MODEL).where(
            self.MODEL.actor_id == actor_id,
            self.MODEL.actor_type == actor_type,
            self.MODEL.purpose == purpose
        )
        model = (await self._db.execute(stmt)).scalar_one_or_none()
        entity = self._to_entity(model, otp_policy)
        return entity

    @staticmethod
    def _to_entity(model: OTPModel, policy: OTPPolicy) -> OTPEntity:
        return OTPEntity(
            id=model.id,
            otp_hash=OTPHashVO(model.otp_hash),
            actor_id=model.actor_id,
            actor_type=model.actor_type,
            purpose=model.purpose,
            resend_count=model.resend_count,
            attempts=model.attempts,
            resend_window_started_at=model.resend_window_started_at,
            last_sent_at=model.last_sent_at,
            locked_until=model.locked_until,
            expires_at=model.expires_at,
            created_at=model.created_at,
            policy=policy
        )

    @staticmethod
    def _to_orm(entity: OTPEntity) -> OTPModel:
        return OTPModel(
            id=entity.id,
            otp_hash=entity.otp_hash.value,
            actor_id=entity.actor_id,
            actor_type=entity.actor_type,
            purpose=entity.purpose,
            resend_count=entity.resend_count,
            attempts=entity.attempts,
            resend_window_started_at=entity.resend_window_started_at,
            last_sent_at=entity.last_sent_at,
            locked_until=entity.locked_until,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
        )
