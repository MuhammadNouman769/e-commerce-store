from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.users.serializers import (
    LoginRequestSerializer,
    MessageResponseSerializer,
    ErrorResponseSerializer
)

""" ====================== Login Schema ====================== """

login_schema = extend_schema(
    summary="User Login",
    description="Authenticate user using email and password",

    request=LoginRequestSerializer,

    examples=[
        OpenApiExample(
            "Login Request Example",
            value={
                "email": "user@gmail.com",
                "password": "123456"
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