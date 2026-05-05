from django.urls import path

from apps.users.views.otp.resend_view import ResendOTPAPIView
from .views.auth.signup_view import  SignupAPIView
from .views.auth.login_view import LoginAPIView
from .views.auth.logout_view import LogoutAPIView
from .views.auth.password_view import (
    ForgotPasswordAPIView,
    ResetPasswordAPIView,
)
from .views.auth.password_view import (
    ForgotPasswordAPIView,
    ResetPasswordAPIView,
)
from .views.otp.verify_view import VerifyOTPAPIView
from .views.otp.resend_view import ResendOTPAPIView
urlpatterns = [
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("verify-otp/", VerifyOTPAPIView.as_view(), name="verify_otp"),
    path("resend-otp/", ResendOTPAPIView.as_view(), name="resend_otp"),
    path("forgot-password/", ForgotPasswordAPIView.as_view(), name="forgot_password"),
    path("reset-password/", ResetPasswordAPIView.as_view(), name="reset_password"),
]