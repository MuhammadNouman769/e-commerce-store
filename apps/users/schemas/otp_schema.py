from drf_spectacular.utils import extend_schema, OpenApiExample


""" ================= VERIFY OTP SCHEMA ================= """
verify_otp_schema = extend_schema(
    summary="Verify OTP",
    description=(
        "Verify OTP sent to user email.\n\n"
        "✔ Activates user account if OTP is correct\n"
        "✔ Marks email as verified\n"
    ),

    request={
        "type": "object",
        "required": ["email", "otp"],
        "properties": {
            "email": {
                "type": "string",
                "example": "user@gmail.com"
            },
            "otp": {
                "type": "string",
                "example": "123456"
            },
        }
    },

    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "example": "Account verified"
                }
            }
        },
        400: {
            "type": "object",
            "properties": {
                "error": {
                    "type": "string",
                    "example": "Invalid OTP / OTP expired / User not found"
                }
            }
        }
    },

    examples=[
        OpenApiExample(
            "Verify OTP Example",
            value={
                "email": "user@gmail.com",
                "otp": "123456"
            },
            request_only=True,
        )
    ],

    tags=["Authentication"]
)


""" ================= RESEND OTP SCHEMA ================= """
resend_otp_schema = extend_schema(
    summary="Resend OTP",
    description=(
        "Resend OTP to user's email.\n\n"
        "✔ Generates new OTP\n"
        "✔ Applies cooldown to prevent spam\n"
    ),

    request={
        "type": "object",
        "required": ["email"],
        "properties": {
            "email": {
                "type": "string",
                "example": "user@gmail.com"
            },
        }
    },

    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "example": "OTP sent"
                }
            }
        },
        400: {
            "type": "object",
            "properties": {
                "error": {
                    "type": "string",
                    "example": "Wait before retry / User not found"
                }
            }
        }
    },

    examples=[
        OpenApiExample(
            "Resend OTP Example",
            value={
                "email": "user@gmail.com"
            },
            request_only=True,
        )
    ],

    tags=["Authentication"]
)