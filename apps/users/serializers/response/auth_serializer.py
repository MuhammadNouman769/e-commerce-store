from rest_framework import serializers


class SignupResponseSerializer(serializers.Serializer):
    otp = serializers.CharField()
    email = serializers.EmailField()


class MessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()