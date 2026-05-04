from rest_framework import serializers
from apps.products.models import Shop


class ShopListSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.username")

    class Meta:
        model = Shop
        fields = [
            "id",
            "name",
            "handle",
            "owner_name",
            "status",
            "rating",
            "is_verified",
        ]


class ShopDetailSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source="owner.email")

    class Meta:
        model = Shop
        fields = "__all__"