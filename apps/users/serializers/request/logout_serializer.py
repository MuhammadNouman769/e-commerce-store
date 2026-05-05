from rest_framework import serializers


class LogoutRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()