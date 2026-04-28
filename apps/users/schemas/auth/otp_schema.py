from drf_spectacular.utils import extend_schema, OpenApiResponse
from apps.users.serializers import (
    VerifyOTPSerializer,
    ResendOTPSerializer,
    MessageResponseSerializer,
    ErrorResponseSerializer
)

verify_otp_schema = extend_schema(
    summary="Verify OTP",

    request=VerifyOTPSerializer,

    responses={
        200: OpenApiResponse(response=MessageResponseSerializer),
        400: OpenApiResponse(response=ErrorResponseSerializer)
    },

    tags=["Authentication"]
)


resend_otp_schema = extend_schema(
    summary="Resend OTP",

    request=ResendOTPSerializer,

    responses={
        200: OpenApiResponse(response=MessageResponseSerializer),
        400: OpenApiResponse(response=ErrorResponseSerializer)
    },

    tags=["Authentication"]
)