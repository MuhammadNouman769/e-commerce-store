from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from ..serializers.auth_serializer import UserSignupSerializer


signup_schema = extend_schema(
    summary="User Signup",
    description="Register user and send OTP to email",

    request=UserSignupSerializer,

    examples=[
        OpenApiExample(
            "Signup Example",
            value={
                "email": "user@gmail.com",
                "phone": "03001234567",
                "password": "strongpassword123",
                "role": "customer"
            },
            request_only=True,
        )
    ],

    responses={
        201: OpenApiResponse(
            description="User created successfully",
            response={
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "email": {"type": "string"}
                }
            }
        ),
        400: OpenApiResponse(
            description="Validation error",
            response={
                "type": "object",
                "properties": {
                    "errors": {"type": "object"}
                }
            }
        )
    },

    tags=["Authentication"]
)




login_schema = extend_schema(
    summary="User Login",
    description="Login user using email & password",

    request={
        "type": "object",
        "properties": {
            "email": {"type": "string", "example": "user@gmail.com"},
            "password": {"type": "string", "example": "123456"}
        },
        "required": ["email", "password"]
    },

    responses={
        200: OpenApiResponse(
            description="Login successful",
            response={
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                }
            }
        ),
        400: OpenApiResponse(
            description="Invalid credentials",
        )
    },

    tags=["Authentication"]
)