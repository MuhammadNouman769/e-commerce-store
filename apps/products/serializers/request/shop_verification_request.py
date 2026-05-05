
from rest_framework import serializers


class ShopRejectSerializer(serializers.Serializer):
    reason = serializers.CharField(required=True)