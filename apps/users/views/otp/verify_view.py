from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from apps.users.serializers import VerifyOTPSerializer
from apps.users.services.otp_service import OTPService
from apps.users.services.auth_service import AuthService
from apps.users.schemas import verify_otp_schema

User = get_user_model()

class VerifyOTPAPIView(APIView):

    @verify_otp_schema
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        user = User.objects.filter(email=data["email"]).first()

        if not user:
            return Response({"error": "User not found"}, status=400)

        success, msg = OTPService.verify_otp(user, data["otp"])

        if not success:
            return Response({"error": msg}, status=400)

        AuthService.activate_user(user)

        return Response(
            {"message": "Account verified successfully"},
            status=200
        )