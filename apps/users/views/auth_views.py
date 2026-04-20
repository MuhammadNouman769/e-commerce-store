from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from ..serializers.auth_serializer import UserSignupSerializer
from ..services.auth_service import AuthService
from ..services.otp_service import OTPService


class SignupAPIView(APIView):

    @extend_schema(
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
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)

        if serializer.is_valid():
            user = AuthService.create_user(serializer)
            OTPService.send_otp(user)

            return Response(
                {
                    "message": "User created. OTP sent.",
                    "email": user.email
                },
                status=status.HTTP_201_CREATED
            )

        return Response({"errors": serializer.errors}, status=400)
    
    
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response


class LoginAPIView(APIView):

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=400)

        login(request, user)  #  IMPORTANT (session create)

        return Response({"message": "Logged in successfully"})    