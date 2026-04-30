# serializers/request/product.py

from rest_framework import serializers
from apps.products.models.product import Product
from apps.products.models.variant import ProductVariant
from apps.products.models.product_image import ProductImage


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = [
            "sku",
            "price",
            "stock_quantity",
            "track_inventory",
            "allow_backorder"
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image", "alt_text"]


class ProductCreateSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)
    images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        variants_data = validated_data.pop("variants")
        images_data = validated_data.pop("images", [])

        product = Product.objects.create(**validated_data)

        # create variants
        for v in variants_data:
            ProductVariant.objects.create(product=product, **v)

        # create images
        for img in images_data:
            ProductImage.objects.create(product=product, **img)

        return product