from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from apps.users.serializers import (
    ForgotPasswordSerializer,
    ResetPasswordSerializer
)
from apps.users.services.otp_service import OTPService
from apps.users.schemas import forgot_password_schema, reset_password_schema

User = get_user_model()


class ForgotPasswordAPIView(APIView):

    @forgot_password_schema
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()

        if user:
            OTPService.send_otp(user)

        return Response({"message": "If email exists, OTP sent"})


class ResetPasswordAPIView(APIView):

    @reset_password_schema
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        user = User.objects.filter(email=data["email"]).first()
        if not user:
            return Response({"error": "Invalid request"}, status=400)

        success, msg = OTPService.verify_otp(user, data["otp"])
        if not success:
            return Response({"error": msg}, status=400)

        user.set_password(data["password"])
        user.save()

        return Response(
            {"message": "Password reset successful"},
            status=status.HTTP_200_OK
        )