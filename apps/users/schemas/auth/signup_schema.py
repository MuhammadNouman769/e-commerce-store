from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

from apps.users.serializers.request.signup_serializer import UserSignupSerializer
from apps.users.serializers.response.auth_serializer import SignupResponseSerializer, ErrorResponseSerializer


signup_schema = extend_schema(
    operation_id="auth_signup",
    summary="User Signup",
    description="Register new user and send OTP for email verification",

    request=UserSignupSerializer,

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
            request_only=True
        )
    ],

    responses={
        201: OpenApiResponse(
            response=SignupResponseSerializer,
            description="User registered successfully"
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Validation error"
        ),
    },

    tags=["Authentication"]
)