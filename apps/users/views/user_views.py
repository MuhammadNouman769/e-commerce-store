from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from django.contrib.auth import get_user_model
from ..services.otp_service import OTPService
from ..services.auth_service import AuthService

User = get_user_model()


class VerifyOTPAPIView(APIView):

    @extend_schema(
        summary="Verify OTP",
        description="Verify OTP and activate user account",

        request={
            "type": "object",
            "required": ["email", "otp"],
            "properties": {
                "email": {
                    "type": "string",
                    "example": "user@gmail.com"
                },
                "otp": {
                    "type": "string",
                    "example": "123456"
                },
            }
        },

        examples=[
            OpenApiExample(
                "Verify OTP Request",
                value={
                    "email": "user@gmail.com",
                    "otp": "123456"
                },
                request_only=True,
            )
        ],

        responses={
            200: OpenApiResponse(
                description="Account verified successfully",
                response={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "example": "Account verified"
                        }
                    }
                }
            ),

            400: OpenApiResponse(
                description="Error response",
                response={
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "example": "Invalid OTP / OTP expired / User not found"
                        }
                    }
                }
            )
        },

        tags=["Authentication"]
    )
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

    @extend_schema(
        summary="Resend OTP",
        description="Resend OTP to user's email with cooldown",

        request={
            "type": "object",
            "required": ["email"],
            "properties": {
                "email": {
                    "type": "string",
                    "example": "user@gmail.com"
                },
            }
        },

        examples=[
            OpenApiExample(
                "Resend OTP Request",
                value={
                    "email": "user@gmail.com"
                },
                request_only=True,
            )
        ],

        responses={
            200: OpenApiResponse(
                description="OTP sent successfully",
                response={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "example": "OTP sent"
                        }
                    }
                }
            ),

            400: OpenApiResponse(
                description="Error response",
                response={
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "example": "Wait before retry / User not found"
                        }
                    }
                }
            )
        },

        tags=["Authentication"]
    )
    def post(self, request):
        email = request.data.get("email")

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "User not found"}, status=400)

        success, msg = OTPService.send_otp(user)

        if not success:
            return Response({"error": msg}, status=400)

        return Response({"message": msg}, status=200)    