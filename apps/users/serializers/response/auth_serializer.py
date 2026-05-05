from rest_framework import serializers
from .user_serializer import UserSerializer


class SignupResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    email = serializers.EmailField()


class LoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()


class MessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()



class LogoutResponseSerializer(serializers.Serializer):
    message = serializers.CharField()    
    logged_out_at = serializers.TimeField()