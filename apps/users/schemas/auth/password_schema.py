from drf_spectacular.utils import extend_schema, OpenApiResponse
from apps.users.serializers import (
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    MessageResponseSerializer,
    ErrorResponseSerializer
)

forgot_password_schema = extend_schema(
    summary="Forgot Password",

    request=ForgotPasswordSerializer,

    responses={
        200: OpenApiResponse(response=MessageResponseSerializer)
    },

    tags=["Authentication"]
)


reset_password_schema = extend_schema(
    summary="Reset Password",

    request=ResetPasswordSerializer,

    responses={
        200: OpenApiResponse(response=MessageResponseSerializer),
        400: OpenApiResponse(response=ErrorResponseSerializer)
    },

    tags=["Authentication"]
)