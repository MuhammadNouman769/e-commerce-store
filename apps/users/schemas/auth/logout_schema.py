from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.users.serializers.request.logout_serializer import LogoutRequestSerializer
from apps.users.serializers.response.auth_serializer import MessageResponseSerializer, ErrorResponseSerializer


logout_schema = extend_schema(
    summary="User Logout",
    description="Blacklist refresh token and logout user",

    request=LogoutRequestSerializer,

    examples=[
        OpenApiExample(
            "Logout Request",
            value={
                "refresh": "refresh_token_here"
            },
            request_only=True,
        )
    ],

    responses={
        205: OpenApiResponse(MessageResponseSerializer),
        400: OpenApiResponse(ErrorResponseSerializer),
    },

    tags=["Auth"]
)