from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.serializers import UserSignupSerializer
from apps.users.services.auth_service import AuthService
from apps.users.services.otp_service import OTPService
from apps.users.schemas import signup_schema


class SignupAPIView(APIView):

    @signup_schema
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = AuthService.create_user(serializer)
        OTPService.send_otp(user)

        return Response(
            {
                "message": "User created. OTP sent.",
                "email": user.email
            },
            status=status.HTTP_201_CREATED
        )