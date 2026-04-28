from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.users.serializers import (
    UserSignupSerializer,
    SignupResponseSerializer,
    ErrorResponseSerializer
)
""" ================= SIGNUP SCHEMA ================= """
signup_schema = extend_schema(
    summary="User Signup",
    description="Register a new user and send OTP for email verification",

    request=UserSignupSerializer,

    examples=[
        OpenApiExample(
            "Signup Request Example",
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

    responses={
        201: OpenApiResponse(
            response=SignupResponseSerializer,
            description="User created successfully"
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Validation error"
        )
    },

    tags=["Authentication"]
)