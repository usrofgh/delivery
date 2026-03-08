from dataclasses import dataclass
from datetime import datetime, UTC, timedelta
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.enums.actor_type import ActorType
from domain.enums.otp_purpose_type import OTPPurposeType
from domain.policies.otp_policy import OTPPolicy
from domain.value_objects.otp_vo import OTPHashVO


@dataclass(slots=True, kw_only=True)
class OTPEntity(BaseEntity):
    otp_hash: OTPHashVO
    actor_id: UUID
    actor_type: ActorType
    purpose: OTPPurposeType

    resend_count: int
    attempts: int

    resend_window_started_at: datetime
    last_sent_at: datetime
    locked_until: datetime | None
    expires_at: datetime
    policy: OTPPolicy


    @staticmethod
    def _now() -> datetime:
        return datetime.now(tz=UTC)

    def is_sent_recently(self) -> bool:
        diff = (self._now() - self.last_sent_at).total_seconds()
        return diff < self.policy.otp_resend_cooldown_seconds

    def is_too_many_resends(self) -> bool:
        start_window = self.resend_window_started_at
        diff = (self._now() - start_window).total_seconds()

        return (
            self.resend_count >= self.policy.otp_max_resends_in_window
            and diff < self.policy.otp_resend_window_seconds
        )

    def is_locked(self) -> bool:
        if not self.locked_until:
            return False
        return self._now() < self.locked_until

    def is_expired(self) -> bool:
        return self._now() > self.expires_at

    def is_can_resend(self) -> bool:
        return not self.is_sent_recently() and not self.is_too_many_resends()

    def normalize_resend_window(self) -> None:
        now = self._now()
        if (now - self.resend_window_started_at).total_seconds() >= self.policy.otp_resend_window_seconds:
            self.resend_count = 0
            self.resend_window_started_at = now

    def rotate_otp(self, otp_hash: OTPHashVO) -> None:
        now = self._now()
        self.otp_hash = otp_hash
        self.resend_count += 1
        self.last_sent_at = now
        self.expires_at = now + timedelta(minutes=self.policy.otp_register_expiration_minutes)
