from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.users.serializers import (
    LoginRequestSerializer,
    MessageResponseSerializer,
    ErrorResponseSerializer
)

login_schema = extend_schema(
    summary="User Login",

    request=LoginRequestSerializer,

    responses={
        200: OpenApiResponse(
            response=MessageResponseSerializer,
            description="Login successful"
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Invalid credentials"
        )
    },

    examples=[
        OpenApiExample(
            "Login Example",
            value={
                "email": "user@gmail.com",
                "password": "123456"
            },
            request_only=True,
        )
    ],

    tags=["Authentication"]
)