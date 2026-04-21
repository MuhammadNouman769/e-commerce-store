from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from ..services.otp_service import OTPService
from ..services.auth_service import AuthService

from ..schemas.otp_schema import verify_otp_schema, resend_otp_schema

User = get_user_model()


class VerifyOTPAPIView(APIView):

    @verify_otp_schema
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("otp")

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "User not found"}, status=400)

        success, msg = OTPService.verify_otp(user, code)

        if not success:
            return Response({"error": msg}, status=400)

        AuthService.activate_user(user)

        return Response({"message": "Account verified"}, status=200)


class ResendOTPAPIView(APIView):

    @resend_otp_schema
    def post(self, request):
        email = request.data.get("email")

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "User not found"}, status=400)

        success, msg = OTPService.send_otp(user)

        if not success:
            return Response({"error": msg}, status=400)

        return Response({"message": msg}, status=200)