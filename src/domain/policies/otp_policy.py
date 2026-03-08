from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class OTPPolicy:
    otp_max_resends_in_window: int
    otp_resend_window_seconds: int
    otp_resend_cooldown_seconds: int
    otp_register_expiration_minutes: int
