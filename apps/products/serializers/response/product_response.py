from rest_framework import serializers
from apps.products.models import Product


class ProductListSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "handle",
            "status",
            "main_image",
            "price",
            "average_rating",
        ]

    def get_main_image(self, obj):
        image = obj.images.first()
        return image.image.url if image else None

    def get_price(self, obj):
        variant = obj.variants.first()
        return variant.price if variant else None