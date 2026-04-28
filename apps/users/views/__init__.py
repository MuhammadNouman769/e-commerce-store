from .auth.signup_view import SignupAPIView
from .auth.login_view import LoginAPIView
from .auth.password_view import (
    ForgotPasswordAPIView,
    ResetPasswordAPIView,
)

from .otp.verify_view import VerifyOTPAPIView
from .otp.resend_view import ResendOTPAPIView