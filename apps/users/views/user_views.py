from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiResponse

from ..services.otp_service import OTPService
from ..services.auth_service import AuthService

from django.contrib.auth import get_user_model

User = get_user_model()


''' ================= VERIFY OTP ================= '''
class VerifyOTPAPIView(APIView):

    @extend_schema(
        request={
            "type": "object",
            "properties": {
                "email": {"type": "string", "example": "user@gmail.com"},
                "otp": {"type": "string", "example": "123456"}
            },
            "required": ["email", "otp"]
        },
        responses={
            200: OpenApiResponse(
                response={"type": "object", "properties": {"message": {"type": "string"}}},
                description="OTP verified successfully"
            ),
            400: OpenApiResponse(
                response={"type": "object", "properties": {"error": {"type": "string"}}},
                description="Invalid or expired OTP"
            )
        },
        description="Verify OTP and activate account",
        summary="Verify OTP"
    )
    def post(self, request):
        code = request.data.get("otp")
        email = request.data.get("email")

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "User not found"}, status=400)

        success, result = OTPService.verify_otp(user, code)

        if not success:
            return Response({"error": result}, status=400)

        AuthService.activate_user(user)

        return Response({"message": "Account verified"}, status=status.HTTP_200_OK)


''' ================= RESEND OTP ================= '''
class ResendOTPAPIView(APIView):

    @extend_schema(
        request={
            "type": "object",
            "properties": {
                "email": {"type": "string", "example": "user@gmail.com"}
            },
            "required": ["email"]
        },
        responses={
            200: OpenApiResponse(
                response={"type": "object", "properties": {"message": {"type": "string"}}},
                description="OTP resent successfully"
            ),
            400: OpenApiResponse(
                response={"type": "object", "properties": {"error": {"type": "string"}}},
                description="Resend blocked or user not found"
            )
        },
        description="Resend OTP with cooldown (1 min)",
        summary="Resend OTP"
    )
    def post(self, request):
        email = request.data.get("email")

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "User not found"}, status=400)

        success, message = OTPService.send_otp(user)

        if not success:
            return Response({"error": message}, status=400)

        return Response({"message": message}, status=status.HTTP_200_OK)