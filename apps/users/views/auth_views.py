from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiResponse

from ..serializers.auth_serializer import UserSignupSerializer
from ..services.auth_service import AuthService


class SignupAPIView(APIView):

    @extend_schema(
        request=UserSignupSerializer,
        responses={
            201: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"},
                        "email": {"type": "string"}
                    }
                },
                description="User created successfully"
            ),
            400: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "object"}
                    }
                },
                description="Validation error"
            )
        },
        description="User signup API. Creates a new user and sends OTP for verification.",
        summary="User Signup"
    )
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)

        if serializer.is_valid():
            user = AuthService.create_user(serializer)
            AuthService.send_otp(user)

            return Response(
                {
                    "message": "User created. OTP sent.",
                    "email": user.email
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )