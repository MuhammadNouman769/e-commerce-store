from ..models.otp import OTP
from ..common.utils.email import send_otp_email


class AuthService:

    @staticmethod
    def create_user(serializer):
        return serializer.save()

    @staticmethod
    def send_otp(user):
        otp = OTP.objects.create(user=user)
        send_otp_email(user.email, otp.code)
        return otp

    @staticmethod
    def activate_user(user):
        user.account_status = "active"
        user.email_verified = True
        user.save()