from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.schemas.auth.logout_schema import logout_schema
from apps.users.serializers.request.logout_serializer import LogoutRequestSerializer


class LogoutAPIView(APIView):

    @logout_schema
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logged out successfully"},
                status=status.HTTP_205_RESET_CONTENT
            )

        except Exception:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )