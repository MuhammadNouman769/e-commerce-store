from rest_framework import serializers
from apps.products.models import Shop


class ShopVerificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = [
            "id",
            "name",
            "owner",
            "shop_status",
            "is_verified",
            "verified_at",
            "rejection_reason"
        ]