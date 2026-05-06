from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers.request.login_serializer import LoginRequestSerializer
from apps.users.serializers.response.auth_serializer import LoginResponseSerializer, ErrorResponseSerializer
from apps.users.schemas.auth.login_schema import login_schema

User = get_user_model()


class LoginAPIView(APIView):

    @login_schema
    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # email verification bypass for admin
        if not user.email_verified and user.role != "admin":
            return Response(
                {"error": "Email not verified"},
                status=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
            }
        }, status=status.HTTP_200_OK)