from rest_framework import serializers
from apps.products.models.category import Category


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "parent",
            "logo",
            "is_visible",
        ]