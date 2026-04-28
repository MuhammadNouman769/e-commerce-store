from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.users.serializers import (
    UserSignupSerializer,
    SignupResponseSerializer,
    ErrorResponseSerializer
)

signup_schema = extend_schema(
    summary="User Signup",
    description="Register user & send OTP",

    request=UserSignupSerializer,

    responses={
        201: OpenApiResponse(
            response=SignupResponseSerializer,
            description="User created"
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Validation error"
        )
    },

    examples=[
        OpenApiExample(
            "Signup Example",
            value={
                "email": "user@gmail.com",
                "phone": "03001234567",
                "password": "strongpassword123",
                "confirm_password": "strongpassword123",
                "role": "customer"
            },
            request_only=True,
        )
    ],

    tags=["Authentication"]
)