from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.users.serializers import (
    VerifyOTPSerializer,
    ResendOTPSerializer,
    MessageResponseSerializer,
    ErrorResponseSerializer
)

""" ====================== OTP Schemas ====================== """

verify_otp_schema = extend_schema(
    summary="Verify OTP",

    request=VerifyOTPSerializer,

    examples=[
        OpenApiExample(
            "Verify OTP Request",
            value={
                "email": "test@gmail.com",
                "otp": "123456"
            },
            request_only=True,
        )
    ],

    responses={
        200: OpenApiResponse(response=MessageResponseSerializer),
        400: OpenApiResponse(response=ErrorResponseSerializer)
    },

    tags=["Authentication"]
)

""" ====================== Resend OTP Schema ====================== """

resend_otp_schema = extend_schema(
    summary="Resend OTP",

    request=ResendOTPSerializer,

    examples=[
        OpenApiExample(
            "Resend OTP Request",
            value={
                "email": "test@gmail.com"
            },
            request_only=True,
        )
    ],

    responses={
        200: OpenApiResponse(response=MessageResponseSerializer),
        400: OpenApiResponse(response=ErrorResponseSerializer)
    },

    tags=["Authentication"]
)