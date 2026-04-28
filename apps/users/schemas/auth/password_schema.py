from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.users.serializers import (
    ForgotPasswordSerializer,
    MessageResponseSerializer
)
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.users.serializers import (
    ResetPasswordSerializer,
    MessageResponseSerializer,
    ErrorResponseSerializer
)


""" ====================== Forgot Password Schema ====================== """

forgot_password_schema = extend_schema(
    summary="Forgot Password",
    description="Send OTP to user's email for password reset",

    request=ForgotPasswordSerializer,

    examples=[
        OpenApiExample(
            "Forgot Password Request",
            value={
                "email": "user@gmail.com"
            },
            request_only=True,
        )
    ],

    responses={
        200: OpenApiResponse(
            response=MessageResponseSerializer
        )
    },

    tags=["Authentication"]
)


""" ====================== Reset Password Schema ====================== """


reset_password_schema = extend_schema(
    summary="Reset Password",
    description="Verify OTP and reset user password",

    request=ResetPasswordSerializer,

    examples=[
        OpenApiExample(
            "Reset Password Request",
            value={
                "email": "user@gmail.com",
                "otp": "123456",
                "password": "newpassword123",
                "confirm_password": "newpassword123"
            },
            request_only=True,
        )
    ],

    responses={
        200: OpenApiResponse(
            response=MessageResponseSerializer
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer
        )
    },

    tags=["Authentication"]
)