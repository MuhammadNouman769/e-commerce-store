from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

from apps.users.serializers.request.login_serializer import LoginRequestSerializer
from apps.users.serializers.response.auth_serializer import LoginResponseSerializer, ErrorResponseSerializer


login_schema = extend_schema(
    operation_id="auth_login",
    summary="User Login",
    description="Authenticate user using email & password and return JWT tokens",

    request=LoginRequestSerializer,

    examples=[
        OpenApiExample(
            "Login Example",
            value={
                "email": "user@gmail.com",
                "password": "strongpassword123"
            },
            request_only=True
        )
    ],

    responses={
        200: OpenApiResponse(
            response=LoginResponseSerializer,
            description="Login successful"
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Invalid credentials"
        ),
    },

    tags=["Auth"]
)