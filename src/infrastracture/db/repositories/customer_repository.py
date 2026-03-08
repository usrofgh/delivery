from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from domain.entities.customer_entity import CustomerEntity
from domain.errors import DomainError, ErrorCodes
from domain.ports.i_customer_repository import ICustomerRepository
from domain.value_objects.common import EmailVO, PasswordVO
from infrastracture.db.models.customer_model import CustomerModel


class CustomerRepository(ICustomerRepository):
    MODEL = CustomerModel

    def __init__(self, db: AsyncSession):
        self._db = db

    async def save(self, entity: CustomerEntity) -> None:
        model = self._to_orm(entity)
        try:
            self._db.add(model)
            await self._db.flush()
        except IntegrityError as err:
            await self._db.rollback()
            if "email" in err.args[0]:
                raise DomainError(ErrorCodes.EMAIL_ALREADY_EXISTS) from err
            raise


    async def get_by_id(self, id: UUID) -> CustomerEntity | None:
        stmt = select(self.MODEL).where(self.MODEL.id == id)
        model = (await self._db.execute(stmt)).scalar_one_or_none()
        entity = self._to_entity(model) if model else None
        return entity

    async def get_by_email(self, email: str) -> CustomerEntity | None:
        stmt = select(self.MODEL).where(self.MODEL.email == email)
        model = (await self._db.execute(stmt)).scalar_one_or_none()
        entity = self._to_entity(model) if model else None
        return entity

    async def remove(self, id: UUID) -> None:
        stmt = delete(self.MODEL).where(self.MODEL.id == id)
        res = (await self._db.execute(stmt)).returning(self.MODEL.id) # noqa
        return res

    @staticmethod
    def _to_entity(model: CustomerModel) -> CustomerEntity:
        return CustomerEntity(
            id=model.id,
            name=model.name,
            email=EmailVO(model.email),
            hashed_password=PasswordVO(model.hashed_password),
            status=model.status,
            created_at=model.created_at,
            activated_at=model.activated_at
        )

    @staticmethod
    def _to_orm(entity: CustomerEntity) -> CustomerModel:
        return CustomerModel(
            id=entity.id,
            name=entity.name,
            email=entity.email.value,
            hashed_password=entity.hashed_password.value,
            status=entity.status,
            created_at=entity.created_at,
            activated_at=entity.activated_at
        )
