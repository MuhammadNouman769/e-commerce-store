from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

from apps.users.serializers.request.password_serializer import (
    VerifyOTPSerializer,
    ResendOTPSerializer
)
from apps.users.serializers.response.auth_serializer import MessageResponseSerializer, ErrorResponseSerializer


verify_otp_schema = extend_schema(
    operation_id="auth_verify_otp",
    summary="Verify OTP",
    description="Verify OTP for email verification or password reset",

    request=VerifyOTPSerializer,

    examples=[
        OpenApiExample(
            "Verify OTP Example",
            value={
                "email": "user@gmail.com",
                "otp": "123456"
            },
            request_only=True
        )
    ],

    responses={
        200: OpenApiResponse(response=MessageResponseSerializer),
        400: OpenApiResponse(response=ErrorResponseSerializer),
    },

    tags=["Auth"]
)


resend_otp_schema = extend_schema(
    summary="Resend OTP",
    description="Resend OTP to user's email",

    request=ResendOTPSerializer,

    examples=[
        OpenApiExample(
            "Resend OTP Example",
            value={
                "email": "user@gmail.com"
            },
            request_only=True
        )
    ],

    responses={
        200: OpenApiResponse(response=MessageResponseSerializer),
        400: OpenApiResponse(response=ErrorResponseSerializer),
    },

    tags=["Auth"]
)