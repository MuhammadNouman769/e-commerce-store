from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models.users import User
from django.contrib.auth import authenticate, login

from ..serializers.auth_serializer import UserSignupSerializer
from ..services.auth_service import AuthService
from ..services.otp_service import OTPService

#  IMPORT SCHEMAS
from ..schemas.auth_schema import signup_schema, login_schema, forgot_password_schema, reset_password_schema


""" ================= SIGNUP VIEWS ================= """
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

""" ================= LOGIN VIEWS ================= """

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
    

""" ================= FORGOT PASSWORD VIEWS ================= """

class ForgotPasswordAPIView(APIView):

    @forgot_password_schema
    def post(self, request):
        email = request.data.get("email")

        user = User.objects.filter(email=email).first()

        if user:
            OTPService.send_otp(user)

        #  always same response
        return Response({"message": "If email exists, OTP sent"})
    
    
""" ================= RESET PASSWORD VIEWS ================= """    
    
class ResetPasswordAPIView(APIView):
    
    @reset_password_schema
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        if not all([email, otp, password, confirm_password]):
            return Response({"error": "All fields are required"}, status=400)

        if password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "Invalid request"}, status=400)

        success, msg = OTPService.verify_otp(user, otp)

        if not success:
            return Response({"error": msg}, status=400)

        user.set_password(password)
        user.save()

        return Response({"message": "Password reset successful"})