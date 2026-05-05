from rest_framework import serializers
from apps.products.models import Product
from drf_spectacular.utils import extend_schema_field


class ProductListSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "short_description",
            "main_image",
            "price",
        ]

    @extend_schema_field(str)
    def get_main_image(self, obj):
        first_image = obj.images.first()
        return first_image.image.url if first_image else ""

    @extend_schema_field(float)
    def get_price(self, obj):
        first_variant = obj.variants.first()
        return float(first_variant.price) if first_variant else 0