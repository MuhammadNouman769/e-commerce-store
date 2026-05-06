from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.users.serializers.request.signup_serializer import UserSignupSerializer
from apps.users.services.auth_service import AuthService
from apps.users.services.otp_service import OTPService
from apps.users.schemas import signup_schema


class SignupAPIView(APIView):
    permission_classes = [AllowAny]  #  important (public endpoint)
    authentication_classes = []       #  prevents JWT interference

    @signup_schema
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create user via service layer
        user = AuthService.create_user(serializer)

        # Send OTP
        success, msg = OTPService.send_otp(user)

        return Response(
            {
                "message": "User registered successfully",
                "email": user.email,
                "otp_sent": success,
                "otp_status": msg,
            },
            status=status.HTTP_201_CREATED
        )