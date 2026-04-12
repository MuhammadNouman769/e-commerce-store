import random
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

        #  RESEND LIMIT CHECK (1 minute)
        if cache.get(f"otp_resend_{email}"):
            return False, "Please wait before requesting another OTP"

        otp = OTPService.generate_otp()

        #  SAVE OTP (5 minutes)
        cache.set(f"otp_{email}", otp, timeout=300)

        #  RESEND LOCK (1 min)
        cache.set(f"otp_resend_{email}", True, timeout=60)

        #  SEND EMAIL
        send_mail(
            "Your OTP Code",
            f"Your OTP is {otp}. It expires in 5 minutes.",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )

        return True, "OTP sent successfully"


    @staticmethod
    def verify_otp(user, code):
        email = user.email

        stored_otp = cache.get(f"otp_{email}")

        if not stored_otp:
            return False, "OTP expired"

        if str(stored_otp) != str(code):
            return False, "Invalid OTP"

        #  DELETE AFTER USE
        cache.delete(f"otp_{email}")

        return True, "OTP verified"