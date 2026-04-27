from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from ..serializers.auth_serializer import UserSignupSerializer


""" ================= SIGNUP SCHEMA ================= """
signup_schema = extend_schema(
    summary="User Signup",
    description=(
        "Register a new user and send OTP to email.\n\n"
        "✔ Creates user in PENDING state\n"
        "✔ Sends OTP for verification\n"
    ),

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
            request_only=True,
        )
    ],

    responses={
        201: OpenApiResponse(
            description="User created successfully",
            response={
                "type": "object",
                "properties": {
                    "otp": {"type": "string"},
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


""" ================= LOGIN SCHEMA ================= """
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
            description="Invalid credentials"
        )
    },

    tags=["Authentication"]
)


""" ================= FORGOT PASSWORD SCHEMA ================= """
forgot_password_schema = extend_schema(
    summary="Forgot Password",
    description=(
        "Send OTP to user's email for password reset.\n\n"
        "✔ OTP is used for password recovery"
    ),

    request={
        "type": "object",
        "properties": {
            "email": {"type": "string", "example": "user@gmail.com"}
        },
        "required": ["email"]
    },

    examples=[
        OpenApiExample(
            "Forgot Password Example",
            value={"email": "user@gmail.com"},
            request_only=True,
        )
    ],

    responses={
        200: OpenApiResponse(
            description="OTP sent successfully",
            response={
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "OTP sent"}
                }
            }
        )
    },

    tags=["Authentication"]
)


""" ================= RESET PASSWORD SCHEMA ================= """
reset_password_schema = extend_schema(
    summary="Reset Password",
    description=(
        "Verify OTP and reset user password.\n\n"
        "✔ OTP verification required\n"
        "✔ Password will be updated securely"
    ),

    request={
        "type": "object",
        "properties": {
            "email": {"type": "string", "example": "user@gmail.com"},
            "otp": {"type": "string", "example": "123456"},
            "password": {"type": "string", "example": "newpassword123"},
            "confirm_password": {"type": "string", "example": "newpassword123"}
        },
        "required": ["email", "otp", "password", "confirm_password"]
    },

    examples=[
        OpenApiExample(
            "Reset Password Example",
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
            description="Password reset successful",
            response={
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Password reset successful"}
                }
            }
        ),
        400: OpenApiResponse(
            description="Error (OTP invalid / mismatch)",
            response={
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        )
    },

    tags=["Authentication"]
)