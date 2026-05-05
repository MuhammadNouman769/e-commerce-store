from rest_framework import serializers
from apps.products.models import Shop


class ShopCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = [
            "name",
            "description",
            "logo",
            "banner",
            "cnic_number",
            "cnic_front",
            "cnic_back",
        ]

        extra_kwargs = {
            "name": {"required": True},
        }