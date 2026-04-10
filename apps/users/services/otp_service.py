from django.utils import timezone
from ..models.otp import OTP


class OTPService:

    @staticmethod
    def verify_otp(user, code):
        otp = OTP.objects.filter(
            user=user,
            code=code,
            is_used=False
        ).last()

        if not otp:
            return False, "Invalid OTP"

        if otp.expires_at < timezone.now():
            return False, "OTP expired"

        otp.is_used = True
        otp.save()

        return True, otp