import random
from django.core.cache import cache
from django.contrib.auth.hashers import make_password, check_password

from ..common.utils.email import send_otp_email


class OTPService:

    OTP_TIMEOUT = 180
    RESEND_TIMEOUT = 60
    MAX_ATTEMPTS = 5

    # -------------------------
    # Cache Keys Helpers
    # -------------------------
    @staticmethod
    def _otp_key(email):
        return f"otp:{email}"

    @staticmethod
    def _attempt_key(email):
        return f"otp:attempt:{email}"

    @staticmethod
    def _resend_key(email):
        return f"otp:resend:{email}"

    # -------------------------
    # Generate OTP
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

        #  Resend protection
        if cache.get(OTPService._resend_key(email)):
            return False, "Wait before retry"

        otp = OTPService.generate_otp()

        #  Secure storage (hashed OTP)
        hashed_otp = make_password(otp)

        # Cache save
        cache.set(OTPService._otp_key(email), hashed_otp, timeout=OTPService.OTP_TIMEOUT)
        cache.set(OTPService._attempt_key(email), 0, timeout=OTPService.OTP_TIMEOUT)
        cache.set(OTPService._resend_key(email), True, timeout=OTPService.RESEND_TIMEOUT)

        #  EMAIL SEND (clean utility use)
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

        stored = cache.get(OTPService._otp_key(email))
        attempts = cache.get(OTPService._attempt_key(email), 0)

        if not stored:
            return False, "OTP expired"

        if attempts >= OTPService.MAX_ATTEMPTS:
            return False, "Too many attempts"

        #  Check OTP
        if not check_password(code, stored):
            cache.set(
                OTPService._attempt_key(email),
                attempts + 1,
                timeout=OTPService.OTP_TIMEOUT
            )
            return False, "Invalid OTP"

        #  SUCCESS → cleanup
        cache.delete(OTPService._otp_key(email))
        cache.delete(OTPService._attempt_key(email))

        return True, "Verified"