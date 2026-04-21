from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample


verify_otp_schema = extend_schema(
    summary="Verify OTP",
    description="Verify OTP and activate user account",

    request={
        "type": "object",
        "required": ["email", "otp"],
        "properties": {
            "email": {"type": "string", "example": "user@gmail.com"},
            "otp": {"type": "string", "example": "123456"},
        }
    },

    examples=[
        OpenApiExample(
            "Verify OTP",
            value={"email": "user@gmail.com", "otp": "123456"},
            request_only=True,
        )
    ],

    responses={
        200: OpenApiResponse(description="Account verified"),
        400: OpenApiResponse(description="Error")
    },

    tags=["Authentication"]
)


resend_otp_schema = extend_schema(
    summary="Resend OTP",
    description="Resend OTP to user's email",

    request={
        "type": "object",
        "required": ["email"],
        "properties": {
            "email": {"type": "string", "example": "user@gmail.com"},
        }
    },

    examples=[
        OpenApiExample(
            "Resend OTP",
            value={"email": "user@gmail.com"},
            request_only=True,
        )
    ],

    responses={
        200: OpenApiResponse(description="OTP sent"),
        400: OpenApiResponse(description="Error")
    },

    tags=["Authentication"]
)