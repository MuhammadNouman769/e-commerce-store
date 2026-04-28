from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from apps.users.serializers import ResendOTPSerializer
from apps.users.services.otp_service import OTPService
from apps.users.schemas import resend_otp_schema

User = get_user_model()


class ResendOTPAPIView(APIView):

    @resend_otp_schema
    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found"}, status=400)

        success, msg = OTPService.send_otp(user)

        if not success:
            return Response({"error": msg}, status=400)

        return Response({"message": msg})