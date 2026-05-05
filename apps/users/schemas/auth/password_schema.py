from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

from apps.users.serializers.request.password_serializer import (
    ForgotPasswordSerializer,
    ResetPasswordSerializer
)
from apps.users.serializers.response.auth_serializer import MessageResponseSerializer, ErrorResponseSerializer


forgot_password_schema = extend_schema(
    summary="Forgot Password",
    description="Send OTP to email for password reset",

    request=ForgotPasswordSerializer,

    examples=[
        OpenApiExample(
            "Forgot Password Example",
            value={
                "email": "user@gmail.com"
            },
            request_only=True
        )
    ],

    responses={
        200: OpenApiResponse(response=MessageResponseSerializer)
    },

    tags=["Authentication"]
)


reset_password_schema = extend_schema(
    summary="Reset Password",
    description="Verify OTP and reset password",

    request=ResetPasswordSerializer,

    examples=[
        OpenApiExample(
            "Reset Password Example",
            value={
                "email": "user@gmail.com",
                "otp": "123456",
                "password": "newpassword123",
                "confirm_password": "newpassword123"
            },
            request_only=True
        )
    ],

    responses={
        200: OpenApiResponse(response=MessageResponseSerializer),
        400: OpenApiResponse(response=ErrorResponseSerializer),
    },

    tags=["Authentication"]
)