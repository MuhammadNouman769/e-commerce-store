# serializers/request/product_request.py

from rest_framework import serializers
from apps.products.models import Product

class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "shop",
            "title",
            "short_description",
            "description_html",
            "categories",
            "brand",
            "status",
            "is_featured",
            "is_best_seller",
            "is_new",
            "is_on_sale"
        ]