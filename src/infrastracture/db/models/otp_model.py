from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from domain.enums.actor_type import ActorType
from domain.enums.otp_purpose_type import OTPPurposeType
from infrastracture.db.models.base_model import BaseModel


class OTPModel(BaseModel):
    __tablename__ = "otps"
    __table_args__ = (
        UniqueConstraint("actor_id", "actor_type", "purpose", name="uq_otps_actor-type_purpose"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)
    otp_hash: Mapped[str] = mapped_column()
    actor_id: Mapped[UUID]
    actor_type: Mapped[ActorType]
    purpose: Mapped[OTPPurposeType]

    resend_count: Mapped[int]
    attempts: Mapped[int]


    resend_window_started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
