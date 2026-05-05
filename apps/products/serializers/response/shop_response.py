from rest_framework import serializers
from apps.products.models import Shop


class ShopListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = [
            "id",
            "name",
            "handle",
            "logo",
            "rating",
            "is_verified",
            
        ]


class ShopDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = "__all__"