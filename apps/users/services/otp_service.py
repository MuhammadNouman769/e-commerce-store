# services/otp_service.py

import random
import hashlib
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings


class OTPService:

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    @staticmethod
    def send_otp(user):
        email = user.email

        if cache.get(f"otp:resend:{email}"):
            return False, "Wait before retry"

        otp = OTPService.generate_otp()

        hashed_otp = hashlib.sha256(otp.encode()).hexdigest()

        cache.set(f"otp:{email}", hashed_otp, timeout=180)
        cache.set(f"otp:attempt:{email}", 0, timeout=180)
        cache.set(f"otp:resend:{email}", True, timeout=60)

        send_mail(
            "OTP Verification",
            f"Your OTP is {otp}",
            settings.EMAIL_HOST_USER,
            [email],
        )

        return True, "OTP sent"

    @staticmethod
    def verify_otp(user, code):
        email = user.email

        stored = cache.get(f"otp:{email}")
        attempts = cache.get(f"otp:attempt:{email}", 0)

        if not stored:
            return False, "OTP expired"

        if attempts >= 5:
            return False, "Too many attempts"

        hashed_input = hashlib.sha256(code.encode()).hexdigest()

        if stored != hashed_input:
            cache.set(f"otp:attempt:{email}", attempts + 1, timeout=180)
            return False, "Invalid OTP"

        cache.delete(f"otp:{email}")
        cache.delete(f"otp:attempt:{email}")

        return True, "Verified"