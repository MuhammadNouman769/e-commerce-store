from rest_framework import serializers
from ..models.shop import Shop


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
            "cnic_back"
        ]

    def validate_cnic_number(self, value):
        if len(value) != 13:
            raise serializers.ValidationError("CNIC must be 13 digits")
        return value