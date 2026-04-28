import random
from django.core.cache import cache
from ..common.utils.email import send_otp_email


class OTPService:

    OTP_TIMEOUT = 180
    RESEND_TIMEOUT = 60
    MAX_ATTEMPTS = 5

    # -------------------------
    # KEY HELPERS (Redis clean structure)
    # -------------------------
    @staticmethod
    def otp_key(email):
        return f"auth:otp:{email}"

    @staticmethod
    def attempt_key(email):
        return f"auth:otp:attempt:{email}"

    @staticmethod
    def resend_key(email):
        return f"auth:otp:resend:{email}"

    # -------------------------
    # GENERATE OTP
    # -------------------------
    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    # -------------------------
    # SEND OTP
    # -------------------------
    @staticmethod
    def send_otp(user):
        email = user.email

        # resend protection
        if cache.get(OTPService.resend_key(email)):
            return False, "Wait before retry"

        otp = OTPService.generate_otp()

        # store OTP in Redis (plain + TTL)
        cache.set(OTPService.otp_key(email), otp, timeout=OTPService.OTP_TIMEOUT)

        # reset attempts
        cache.set(OTPService.attempt_key(email), 0, timeout=OTPService.OTP_TIMEOUT)

        # resend lock
        cache.set(OTPService.resend_key(email), True, timeout=OTPService.RESEND_TIMEOUT)

        # send email
        success, msg = send_otp_email(email, otp)

        if not success:
            return False, "Failed to send OTP"

        return True, "OTP sent"

    # -------------------------
    # VERIFY OTP
    # -------------------------
    @staticmethod
    def verify_otp(user, code):
        email = user.email

        stored = cache.get(OTPService.otp_key(email))
        attempts = cache.get(OTPService.attempt_key(email), 0)

        if not stored:
            return False, "OTP expired"

        if attempts >= OTPService.MAX_ATTEMPTS:
            return False, "Too many attempts"

        if str(stored) != str(code):
            cache.set(
                OTPService.attempt_key(email),
                attempts + 1,
                timeout=OTPService.OTP_TIMEOUT
            )
            return False, "Invalid OTP"

        # cleanup
        cache.delete(OTPService.otp_key(email))
        cache.delete(OTPService.attempt_key(email))

        return True, "Verified"