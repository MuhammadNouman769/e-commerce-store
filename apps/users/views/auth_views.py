from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate, login

from ..serializers.auth_serializer import UserSignupSerializer
from ..services.auth_service import AuthService
from ..services.otp_service import OTPService

#  IMPORT SCHEMAS
from ..schemas.auth_schema import signup_schema, login_schema


class SignupAPIView(APIView):

    @signup_schema
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


class LoginAPIView(APIView):

    @login_schema
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=400)

        login(request, user)

        return Response({"message": "Logged in successfully"})