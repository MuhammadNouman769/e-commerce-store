from rest_framework import serializers
from apps.products.models import Shop


class ShopCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = [
            "owner",
            "name",
            "description",
            "logo",
            "banner",
            "cnic_number",
            "cnic_front",
            "cnic_back",
        ]

        extra_kwargs = {
            "owner": {"required": True},
            "name": {"required": True},
        }