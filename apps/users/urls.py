from django.urls import path
from .views.auth_views import SignupAPIView
from .views.user_views import VerifyOTPAPIView, ResendOTPAPIView

urlpatterns = [
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("verify-otp/", VerifyOTPAPIView.as_view(), name="verify_otp"),
    path("resend-otp/", ResendOTPAPIView.as_view(), name="resend_otp"),
]